# Memory, streams and backend services

Measure process RSS, V8 heap used/total, external and array-buffer memory across repeated
create/use/release cycles. `arrayBuffers` is included in `external`; do not add it twice.
RSS is process-wide; with worker threads the other `memoryUsage()` fields describe the
calling thread's isolate. Allocator fragmentation can keep RSS high after memory becomes
reusable. For multi-process servers report per-process and aggregate values without
double-counting shared memory. [Node process API](https://nodejs.org/api/process.html).

Compare retained object graphs after equivalent lifecycle phases; examine dominators,
retaining paths, listeners, timers, pending work, caches and response/body ownership.
Distinguish churn/GC pressure from growing retention. Heap allocation samples locate
allocation sites; snapshots answer retention questions and may miss native allocations.
A snapshot pauses the main thread and can roughly double heap requirements. Use an
approved sacrificial instance with headroom; do not take repeated snapshots on a critical
replica. Forced GC is diagnostic and changes workload behavior. Native/GPU allocations
need matching allocator/OS evidence.
[Heap snapshots](https://nodejs.org/learn/diagnostics/memory/using-heap-snapshot),
[heap profiling](https://nodejs.org/learn/diagnostics/memory/using-heap-profiler).

Streams need end-to-end backpressure, bounded payload/chunk sizes and cancellation.
Respect `.write()` returning false and wait for drain; use the existing `pipeline`
ownership/error path when appropriate. `highWaterMark` is a threshold, not a hard memory
cap; a transform has both read and write buffers, and object-mode counts objects rather
than bytes. Observe slow consumers, disconnects and aborted producers; assert resources
close and queued data stays bounded. [Streams](https://nodejs.org/api/stream.html).

Worker threads can help CPU-intensive JavaScript; ordinary async I/O usually gains
little. Include pool startup, queue wait, structured-clone/transfer cost and cleanup in
the comparison. Transferred ArrayBuffers can detach other views; preserve ownership.
Resource limits apply to the JS engine, not a process RSS guarantee. Do not spawn a
worker per request or assume a pool automatically provides backpressure.
[Workers](https://nodejs.org/api/worker_threads.html).

For services, correlate queue age, active requests, completed/failed/timed-out operations,
pool acquisition, query/remote spans, response sizes and retry amplification. Bound
parallel promises and retry attempts; enforce admission before allocating large payloads.
Propagate the caller's remaining deadline through queueing and downstream calls. Verify
abort actually stops work rather than only rejecting the caller's promise.

Use existing OpenTelemetry/metrics integration. Instrument logical operations and useful
boundaries; avoid every function, request-body labels and user IDs in metrics. Check
context propagation through queues, worker messages and custom async abstractions.
Measure telemetry overhead with an uninstrumented or appropriately sampled comparison;
exporter queues and dropped telemetry need bounded behavior. Production percentiles
need suitable distributions, aggregation and workload segmentation, not averages of
replica percentiles. Use `perf-latency` for cross-region/replica analysis.
