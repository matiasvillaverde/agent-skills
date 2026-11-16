---
name: perf-go
description: Profile and improve Go services, goroutines, CPU, allocations, GC, contention and backend latency using runtime diagnostics and production telemetry. Use for measured Go performance investigations on Linux or other supported targets.
---

# Go performance

Improve the operation users experience, with evidence from its actual deployment target.
Preserve API/UI behavior, output quality, validation, ordering, cancellation, durability and
resource limits. Go's runtime diagnostics work in services as well as local programs; profiling
does not require an IDE or a compiler on the application server. Linux x86-64 and ARM64 are
explicit targets. A local macOS result does not qualify either Linux target.

## Establish the question and environment

Inspect owning instructions, `go.mod`/`go.work`, toolchain selection, dependencies, build flags,
CGO, CPU/architecture and deployment limits. Record the running artifact's Go version and build
identity, not just the operator's `go version`. Match docs/APIs to that release. Consult
[versions and sources](references/sources.md) for current research; recheck release information
when an upgrade matters. Do not upgrade the project or download a toolchain to run an example.

Define representative traffic/input, concurrency, completion semantics and the metric/budget:
request/job latency, completed throughput, CPU per operation, retained memory, or another actual
constraint. Record errors, timeouts and rejected work too. Separate cold/warm behavior, deployment
cohorts and replicas. Use existing evidence first; no automatic production load or profiling
permission changes. Choose a bounded capture on a named instance through its approved access.

## Select the smallest useful observation

| Question | Start with |
| --- | --- |
| Which code consumes CPU? | CPU pprof plus CPU time/completions; inspect flat and cumulative cost. |
| Allocation churn, retained heap or GC cost? | Correct heap/alloc sample type, runtime metrics, lifecycle and process/cgroup memory. |
| Goroutines accumulate or requests hang? | Repeated goroutine stacks, cancellation/ownership evidence, supported leak detection and execution trace. |
| Locks, channels or runnable queues cause delay? | Block/mutex profiles or Go execution trace, matched to the suspected wait. |
| Backend request/job is slow? | Distributed spans, pool/queue metrics, dependency timing and errors; profiles only for the relevant resource cost. |
| Container throughput/tails regress? | Effective GOMAXPROCS, quota/throttling, affinity, GC and runtime/OS scheduling evidence. |

Read [profiling and capture](references/profiling.md) for pprof, traces and representative
benchmarks; [runtime and goroutines](references/runtime.md) for concurrency, memory and GC;
[services and observability](references/services.md) for HTTP/RPC/DB/queues and production
instrumentation. Read only the relevant branches. The available `perf-system` Linux reference
adds PMU, NUMA and cgroup detail; native OS samples do not replace Go's goroutine/runtime view.

## Follow evidence into a bounded change

Inspect the relevant public API, version-matched runtime/library source and actual hot path.
Distinguish running CPU, runnable delay, synchronization waits and remote I/O. Goroutine count
alone is not a leak; an empty sampled profile is not absence of cost. Explain observation scope,
sampling, lost data and diagnostic overhead before choosing an optimization.

Prefer removing repeated parsing, serialization, copying, allocation, duplicate requests and
unbounded fan-out. Pools, caches, batching, custom allocators and synchronization changes need a
measured benefit plus clear ownership, bounds and failure semantics. Avoid universal worker
counts, GOGC/GOMEMLIMIT percentages, channels-over-locks rules or minimum speedup percentages.
Never trade away errors, cancellation, memory safety or required work for a faster benchmark.

For lookup, queue or algorithm candidates, consult the shared [data-structure review](../perf-system/references/algorithms-and-data-structures.md)
when available. Include construction, GC/retention, map order and synchronization in the real
service workload; current built-ins may already implement the proposed optimization.

Use existing instrumentation at transport/job/dependency boundaries and a few meaningful
operation spans. The executable owns SDK/exporter configuration; libraries use existing APIs.
Keep provider choices/configuration out of business logic. The available `observability` skill
owns broader logging, alerts and audits; it is not mandatory for every profiling task.

## Verify and finish

Compare equivalent shipping builds on representative targets with consumed results, realistic
input growth and enough repetitions to see variability. Include the failure/cancellation,
shutdown or overload path affected by the change. Recheck without heavy diagnostics; race,
fuzz and synchronization tests protect correctness but their timings are not production baselines.
Microbenchmarks or a clean leak-profile snapshot do not establish end-to-end health.

Report before/after values, variability, actual commands, target/build/workload identity,
correctness evidence, telemetry overhead and unmeasured paths. Classify accepted, regressed,
inconclusive or not verified. Keep a simpler implementation when benefits do not justify complexity.

Keep compact redacted evidence and reproduction details. Stop owned profilers, listeners,
load generators and children; restore temporary profile rates/configuration. Delete task-owned
profiles, traces, scratch binaries and isolated caches after analysis, including on failure.
Preserve shared Go module/build caches, pre-existing binaries and minimal evidence needed for
unresolved failures. Verify cleanup and disclose leftovers.
