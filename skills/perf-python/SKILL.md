---
name: perf-python
description: Profile and improve Python CPU, allocations, native memory, asyncio, threads and processes, server queues and production telemetry using version-aware bounded experiments.
---

# Python performance

Identify the actual interpreter/build, environment, dependencies/native extensions,
OS/container limits, operation and representative workload. Record Python version,
GIL/free-threaded and JIT state when relevant; a development interpreter may differ from
the server. Preserve outputs, ordering, numerical tolerances, data isolation and recovery.

Set a metric, correctness oracle and bounded experiment. Separate startup/imports,
warmup and steady state. Read existing queue/latency/resource evidence before collecting
more. Measure wall time, process CPU and downstream/queue waits separately. Include
timeouts, rejected work and errors in the workload report; do not infer service p99 from
a short `timeit` run.

## Select evidence, then change code

Read [profilers and measurement](references/profiling.md) for deterministic, statistical,
native and allocation tools. Use installed capabilities first, matching target/runtime
support and attach permissions. A profiler identifies hypotheses; compare variants
without it. Python 3.15's new profiler does not exist on every deployed interpreter.

Read [memory and concurrency](references/memory-concurrency.md) for retained memory,
asyncio, GIL/free-threading, process pools and backend instrumentation. Distinguish Python
heap from native/RSS/GPU memory; distinguish async task elapsed time from execution.
Do not label every growing RSS graph a leak or assume async code is automatically bounded.

Test one hypothesis at a time. Remove redundant queries, repeated parsing, unnecessary
copies and unsuitable algorithm/data choices before adding caches, vectorization, native
extensions or concurrency. Those choices need measured benefit and ownership, memory,
cancellation and correctness analysis. Avoid broad rewrites or runtime upgrades disguised
as small optimizations.

For an algorithm or container shortlist, use the shared [data-structure review](../perf-system/references/algorithms-and-data-structures.md)
when available. Prefer existing native implementations; preserve duplicate resolution, order,
numeric semantics and concurrency. Include index construction and conversion in the measurement.

## Prove the improvement

Use representative sizes/distributions and the same interpreter, dependencies, limits,
cache state and work. Repeat enough to expose noise; alternate variants if drift matters.
Check correctness independently, including numeric/ordering behavior when optimization
changes representation. Report cold and warm results separately and show memory/CPU or
tail-latency tradeoffs. Run focused regression checks and required project gates.

Production captures need bounded duration/rate, private storage and an approved target.
Do not relax ptrace/host security, install tools, change global thread settings or load
production merely to get a profile. Reuse existing telemetry with bounded attributes and
context propagation; measure its cost. A missing profiler is a coverage gap, not evidence
of acceptable performance.

Report baseline, diagnosis, change, measured result and limits. Save compact evidence and
reproduction; stop owned profilers/load/workers, restore temporary settings and delete
task-owned raw captures, fixtures and caches after preserving required failure evidence.
Verify cleanup on failure too. Preserve shared caches/user data.
[Research sources](references/sources.md) explain selection and version-sensitive claims.
