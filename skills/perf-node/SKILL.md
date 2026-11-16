---
name: perf-node
description: Profile and improve Node.js and TypeScript server or CLI performance, including event-loop stalls, CPU, heap and native memory, streams, workers, queues and production observability.
---

# Node.js performance

Identify the operation, deployed Node/V8 version, compiled artifact, runtime flags,
OS/container CPU and memory limits, representative workload and correctness contract.
Preserve product behavior, output, access controls and durability. Browser rendering
belongs to `perf-web` or `perf-react`; do not infer server behavior from a browser trace.

## Measure the actual bottleneck

Read existing latency, errors, throughput, queue age/depth and resource evidence first.
Set a bounded experiment with a useful success criterion and stop condition. Separate
startup, warmup, steady state and overload. Include all attempts, timeouts and rejected
work; a closed-loop client slowing its own requests can conceal overload. Record offered
and achieved load, concurrency and sample count. Do not manufacture p99 from a few runs.

Use [runtime profiling](references/runtime.md) to distinguish JavaScript execution,
native/libuv work, scheduling, garbage collection and downstream waits. Event-loop
utilization is not process CPU, and an idle loop does not prove healthy requests.
Validate units, measurement windows and profiler coverage, including worker isolates
and child processes. Prefer installed core tools before adding profiling dependencies.

For retained memory, buffers, streams and concurrency, read
[memory and services](references/memory-services.md). RSS, V8 heap, allocation rate and
external memory answer different questions. A large heap or flat RSS after freeing
objects does not by itself establish a leak.

## Improve and verify

Follow one evidence-backed hypothesis at a time. Remove unnecessary work, repeated
serialization, redundant queries and avoidable allocation first. Bound queues and
admission; propagate deadlines/cancellation and preserve backpressure. Workers, caches,
pools and larger heap/thread-pool settings need measured benefit and explicit lifecycle,
ownership, invalidation and overload behavior. Moving work off the main loop can simply
move contention or increase memory.

For lookup, sorting, queue or layout candidates, use the shared [data-structure review](../perf-system/references/algorithms-and-data-structures.md)
when available. Preserve key identity, duplicate resolution and order; include index construction,
updates, numeric conversion and GC. Verify engine behavior rather than assuming TypeScript changes it.

Compare baseline and candidate without the profiler using the same workload, runtime,
limits and cache state. Alternate variants when drift matters; show distributions and
resource tradeoffs. Check the real result and failure recovery independently. Run focused
regressions and required project gates; retain changes that improve the target beyond
noise without degrading relevant tails, correctness or maintainability.

For production, reuse the existing telemetry stack and `observability`: bounded metric
labels, route templates, queue/downstream spans and sampled captures. Inspect one approved
replica before increasing coverage. Profiling endpoints and artifacts require private
access; heap snapshots can pause or crash a process. No automatic production load,
public inspector, host permission changes or tool installation.

Report the bottleneck, evidence, change, before/after results, workload limits and
unmeasured risks. Track task-owned artifacts; save compact measurements/reproduction,
stop owned load and profilers, restore temporary settings, then remove private raw
profiles, snapshots, fixtures and task-only caches. Preserve shared caches and required
evidence. Check cleanup on failures too. [Sources and selection](references/sources.md)
record the research basis; recheck target-version documentation when using an API.
