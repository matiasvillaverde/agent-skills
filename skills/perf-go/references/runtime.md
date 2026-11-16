# Go runtime, goroutines and memory

## Concurrency has an owner and a capacity

For each relevant goroutine, identify who starts it, what makes it finish, what cancels blocked
work, who observes errors, and who waits for completion. A WaitGroup joins; it does not cancel.
Passing a context as an explicit argument does not give it a different cancellation lifetime.
Channel closure, cancellation and joining are distinct responsibilities. Keep channel ownership
clear and test the actual early-return/error path, not just successful steady state.

Bound admission before spawning work when the bottleneck is goroutine accumulation; a semaphore
acquired only inside every newly launched goroutine can leave an unbounded waiting population.
Account for queues, payload sizes, retries and nested fan-out as well as active workers. Pool
size follows CPU entitlement, I/O waiting and downstream capacity; more goroutines do not create
CPU or database capacity. Backpressure/rejection must preserve the product's observable contract.
[Effective Go concurrency](https://go.dev/doc/effective_go#concurrency),
[context](https://pkg.go.dev/context), [errgroup](https://pkg.go.dev/golang.org/x/sync/errgroup).

For a suspected leak, compare stacks/counts before work, under load, after cancellation and after
an appropriate quiescent interval. Check abandoned channel sends/receives, never-closed streams,
forgotten cancel functions, retries, response/rows bodies and shutdown joins. Legitimate pools,
timers and background housekeeping need lifecycle-aware interpretation. A request deadline only
stops work whose implementation observes it. Report what was actually completed or abandoned.

Go 1.27 provides `goroutineleak` profiles without the earlier Go 1.26 experiment. They detect a
subset of permanently blocked synchronization operations, not all lifecycle leaks: reachable
primitives and network/file I/O or direct syscalls can evade classification. Check availability
and use ordinary stacks/lifecycle tests too. An empty leak profile is not a clearance certificate.
[Leak profiler design and limits](https://go.dev/blog/goroutine-leak-profiles).

## Scheduling and contention

GOMAXPROCS limits concurrent Go execution, not the number of goroutines or every OS thread.
Distinguish runnable-to-running delay from blocking and remote latency. Examine executor/worker
load, GC assists, cgo/syscalls, quota throttling and neighboring work before changing concurrency.
On Linux, use the available shared [Linux guide](../../perf-system/references/linux.md) for cgroup,
pressure and VM constraints; official kernel documentation is the fallback if absent.

Go 1.25 introduced container-aware default GOMAXPROCS and periodic updates. Current behavior also
depends on the main module's Go compatibility version, GODEBUG and explicit environment/API
overrides. Older module defaults can disable the new policy; manually setting GOMAXPROCS disables
automatic updates. Quota rounding/default floors mean it is not simply a hard worker count equal
to quota. Record the effective value and actual limits rather than blindly adding an automaxprocs
dependency or setting it to `runtime.NumCPU()`.
[Runtime policy](https://pkg.go.dev/runtime#GOMAXPROCS), [Go 1.25](https://go.dev/doc/go1.25#runtime).

Use block/mutex profiles and short execution traces to locate critical sections or waits. First
consider less shared work, shorter critical sections and less fan-out. Select channels, mutexes,
atomics or sharding by ownership and measured contention; neither channels nor lock-free code are
inherently faster. `sync.Map` has specialized intended workloads, not a blanket read-heavy rule.
Keep memory-ordering/publication invariants and recheck race/cancellation behavior after a change.
[sync contracts](https://pkg.go.dev/sync), [race detector](https://go.dev/doc/articles/race_detector).

## Allocation, retained memory and GC

Distinguish allocation churn from required live data, accidentally retained graphs, allocator
reservation and memory outside Go's management. Correlate the relevant heap sample type with
runtime metrics and process/cgroup memory over equivalent lifecycles. Check large backing arrays
retained by small slices, oversized pooled buffers, caches without eviction, goroutine stacks and
cgo/mmap/native allocations. Do not declare an RSS plateau a Go heap leak without attribution.

Reduce repeated allocation/copying or lifetime before changing GC settings. Allocation placement
depends on escape analysis and compiler decisions: value types are not guaranteed to stay on the
stack, and pointers do not always imply heap allocation. Use scoped compiler escape/inlining
diagnostics and measured allocations in the actual build. Avoid globally disabling inlining or
optimizations just to obtain tidy stacks; diagnostic flags can change the cost being measured.

GOGC trades GC work against heap growth. GOMEMLIMIT is a soft target for Go-managed runtime memory,
not an RSS/container hard limit; external memory is outside that accounting. A too-low target can
cause excessive GC and may be exceeded to preserve progress. It remains relevant with GOGC=off.
Leave measured headroom for native allocations, runtime work and workload bursts. Do not prescribe
a universal container percentage or promise that a setting prevents OOM. Retest latency, throughput,
GC CPU/assists and memory together. [GC guide](https://go.dev/doc/gc-guide).

`sync.Pool` is a temporary-object optimization, not guaranteed retention, a resource pool or a
capacity bound. Pooled backing storage must not escape through a returned slice/string/object
after reuse; copy or transfer ownership correctly. Bound retained buffer sizes and clear sensitive
references where needed. Measure both churn and retained capacity. Prefer straightforward ownership
when pooling adds complexity without useful gain. [sync.Pool](https://pkg.go.dev/sync#Pool).

## Runtime telemetry and test evidence

Discover metrics with `runtime/metrics.All()` and validate kind/units; names available in a new
runtime may not exist in the project. Useful groups include allocation rate, live/goal heap,
memory classes, GC work/assists, goroutines and scheduler latency. Use interval deltas for
cumulative counters/histogram buckets. `/sched/latencies:seconds` measures runnable delay, not
request latency; `/cpu/classes` is runtime accounting and cannot be equated with OS CPU counters.
Snapshot histogram storage when reusing sample buffers.
[runtime/metrics](https://pkg.go.dev/runtime/metrics).

Use the existing supported OTel/Prometheus/runtime integration where present. Some integrations
need a separate producer for scheduler histograms; confirm actual emitted metrics, not just a
successful initialization call. Avoid registering duplicate runtime collectors or scraping every
possible metric. [OTel Go runtime instrumentation](https://pkg.go.dev/go.opentelemetry.io/contrib/instrumentation/runtime).

For concurrency/lifetime changes, exercise the relevant race, cancellation, partial input,
backpressure and repeated shutdown cases. Use supported `testing/synctest` for suitable concurrent
tests instead of brittle sleeps; it is not a substitute for real network integration tests or
performance timing. Fuzz concrete parser/protocol invariants where valuable. Retain a few strong
integration checks and focused low-level oracles; no automatic test matrix or coverage quota.
[synctest](https://pkg.go.dev/testing/synctest), [Go fuzzing](https://go.dev/doc/security/fuzz/).
