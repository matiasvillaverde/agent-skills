# Memory, concurrency and services

Start `tracemalloc` before the suspected lifecycle and compare snapshots after equivalent
phases. Track current/peak traced bytes separately from process RSS. Traceback depth costs
time and memory. Objects allocated before tracing are absent; native extensions can use
domains but do not all expose every allocation. Check retaining owners, caches, queues,
closures, task results and exception tracebacks. Freed memory may remain in allocator
arenas; a retained-byte plateau and an RSS plateau mean different things.
[tracemalloc](https://docs.python.org/3.15/library/tracemalloc.html).

Memray can attribute native allocation stacks when supported. Default allocator tracking
does not necessarily show every Python object allocation; tracing Python allocators adds
detail and overhead. Use output coverage/symbol quality to qualify conclusions and never
upload raw captures with application data to a public viewer.
[Memray run modes](https://bloomberg.github.io/memray/run.html).

Asyncio needs bounded admission as well as structured task ownership. A TaskGroup cleans
up related tasks but does not limit how many are created. Use the repository's bounded
worker/queue pattern; a semaphore around work can still leave millions of waiting tasks.
Propagate deadlines and cancellation; verify resource closure and partial effects.
Do not swallow `CancelledError` or assume cancelling a waiting coroutine kills a running
thread. `to_thread` usually helps blocking I/O under the GIL, while extensions that release
it may also parallelize CPU work. [Tasks](https://docs.python.org/3.15/library/asyncio-task.html).

Async debug/slow-callback diagnostics can locate stalls; their configured threshold is a
diagnostic setting, not the service's acceptance target. Bound debug duration and log
volume; check synchronous logging and blocking library calls on the event loop.
[Asyncio development](https://docs.python.org/3.15/library/asyncio-dev.html).

Check build support and actual GIL state after importing extensions; free-threaded builds
can re-enable it for incompatible extensions. Do not rely on container internals making
compound shared-state operations atomic. Use synchronization based on ownership and
test races. Compare single-thread overhead, memory and scaling on the actual workload.
[Free threading](https://docs.python.org/3.15/howto/free-threading-python.html).

For process pools, measure serialization, startup, queueing and aggregate memory. Inspect
the target OS/Python start method; do not assume fork or copy-on-write behavior. Native
BLAS/OpenMP pools multiplied by process/thread workers can oversubscribe CPU. Scope any
thread-limit experiment to the owned process and verify throughput, latency and results.
Vectorization can increase temporary arrays; batching can increase peak memory or delay.

Services need bounded queues, age, rejected/timed-out/completed counts, pool acquisition,
downstream spans and retry amplification. Preserve request context through jobs and
executors using the existing telemetry stack. Use bounded metric labels, sampled traces
and configurable diagnostics; avoid payloads/IDs in metric dimensions. Measure overhead
and dropped telemetry. Profile an approved representative worker/replica; do not treat
one process as the whole deployment or average replica p99 values.
