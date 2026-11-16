# Rust memory, scheduling and I/O

## Allocation and retention

Identify the allocator and observation boundary before trusting counts. Measure allocations per
operation, cumulative bytes, peak live bytes and retained capacity separately. Include stacks,
mappings and child processes when they belong to the requested budget. Repeated lifecycle runs
should establish warmup, release and retained owners; RSS alone cannot distinguish useful cache,
fragmentation, allocator reservation and a leak.

On macOS, available Instruments allocation/VM tools can inspect a native Rust host. On Linux,
heaptrack can collect allocation stacks; run it on the built executable, not `cargo run`. A
malloc-family collector can miss custom allocator or pool suballocations. Keep symbols and Rust
demangling available, and inspect unresolved frames honestly. Use allocator-native metrics or
bounded explicit accounting only when the existing collector cannot answer the question.

Rust `dhat` is an optional feature-gated diagnostic. Version 0.3.3 calls itself experimental and
can perturb or fail workloads; it wraps the system allocator and needs source changes. Respect
the profiler's lifetime, including explicit destruction before `process::exit` where applicable.
Its observations do not equal all memory access/copy activity. Global counting also makes parallel
heap-test attribution fragile. Do not replace the product allocator or permanently serialize the
test suite just to make a diagnostic easy.

Look for repeated clones/serialization, oversized owned buffers, Vec/String capacity retained
after bursts, Arc cycles or references, tasks/channels that retain payloads, and caches without
eviction semantics. Borrowing, reuse, arenas or small inline containers are candidates, not defaults.
Check backing-storage lifetime, error/cancel cleanup, peak burst behavior, copying and retained
capacity. Fewer allocation calls can coexist with more memory and worse latency.

## Async and threads

Measure whether elapsed time comes from computation, blocking, ready-but-unscheduled work or
an external dependency. Correlate operation spans, OS thread states and runtime task identity.
CPU samples show where threads run; an async task's end-to-end lifetime is different.

For a Tokio application with supported diagnostics, Console distinguishes time being polled
(`Busy`), runnable awaiting a poll (`Sched`), and awaiting wakeup (`Idle`). Inspect long polls,
wake/poll rates, queue delay, fan-out and resource waits. A long poll is not itself a measurement
of hardware CPU time. Existing `tracing` spans can be enough for a scoped question.

Console setup is version-sensitive and may require Tokio tracing, `--cfg tokio_unstable`, a
subscriber and enabled runtime/TRACE targets. Keep these in a diagnostic build, preserve flags
and bind diagnostic endpoints privately. A trace filter that suppresses runtime events creates
an observation gap. Do not retrofit Console into unrelated executors or infer Swift actor tracks
describe Rust tasks.

Bound queues, captured results, fan-out and worker concurrency together. Moving blocking work
off async workers is useful only if the replacement pool and backlog are controlled. Tokio
`spawn_blocking` work that has started cannot simply be aborted: preserve cancellation and
resource ownership. Check fairness and oversubscription across nested thread pools. Lock-free
structures, weaker atomics or spin loops need correctness proof and measured benefit; they can
increase contention, power and tail latency.

Off-CPU samples can include both blocking and scheduler delay. Check the profiler's actual OS
support and state filters. Do not attribute every off-CPU interval to a mutex or network wait.

## I/O and native boundaries

Count work through final completion: syscalls, bytes, requests, queries, retries and flushes.
Distinguish page-cache hits from storage work, mmap setup from demand faults, queued writes from
durable completion, and a submitted asynchronous operation from a completed one. Buffering,
batching and zero-copy must preserve ordering, lifetimes, backpressure, deadlines and final errors.
Vary input sizes and slow-consumer behavior where the mechanism can change them.

For FFI, match ABI, alignment, ownership and allocator/free pairing. Cross-language copies and
callbacks can dominate an apparently small Rust function. Keep host and Rust symbols together;
missing foreign frames are a limit. GPU-backed work needs its API's real completion and memory
lifetime evidence; a fast Rust submission call does not measure GPU execution.

Sources: [heaptrack usage and limitations](https://github.com/KDE/heaptrack),
[dhat 0.3.3](https://docs.rs/dhat/0.3.3/dhat/),
[Tokio Console](https://github.com/tokio-rs/console),
[subscriber setup](https://github.com/tokio-rs/console/tree/main/console-subscriber),
[task UI fields](https://github.com/tokio-rs/console/tree/main/tokio-console),
[spawn_blocking](https://docs.rs/tokio/latest/tokio/task/fn.spawn_blocking.html).
