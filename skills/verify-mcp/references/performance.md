# Measure MCP performance

Use this branch for a concrete latency, capacity, resource or context-cost question.
Start with a bounded workload and comparison, not an arbitrary grade threshold.

## Separate the costs

Record transport, implementation/SDK/client revision, payloads, upstream fixture, machine,
concurrency and warmup. Separate cold startup/discovery/authentication from warm operations.
A fresh connection or process per call measures a different workload from persistent use.
State which work is included in each measurement.

Use a controlled upstream fixture to isolate server overhead. Measure real upstream calls
separately when authorized, respecting provider limits and costs. Do not report fixture
latency as end-to-end production latency.

| Layer | Measurements that answer useful questions |
| --- | --- |
| Operation | Latency distribution with sample count, successes, protocol/tool errors, timeouts, throughput and queue delay where relevant |
| Context | Request/result bytes; schema/discovery bytes; model-visible text/JSON duplication; tokens only with the tokenizer or runner that produced the count |
| Resource | CPU time, peak and retained memory, active processes/threads/connections/handles, cleanup after cancellation or repeated work |
| Agent task | Correct completion, prohibited effects, total calls, retries, time and measured token/model cost |

A shorter result can require more calls or omit decisive evidence. Compare task success
and total cost alongside per-response size. Do not use character counts as exact token
counts or fabricate cost when the runner supplies none.

## Workload and interpretation

For concurrency tests, state whether callers wait for replies before sending more work
(closed loop) or requests arrive at a specified rate. Waiting clients can hide demand
during stalls; measure queued/late requests when arrival-rate capacity is the question.
Include only bounded overload, slow-upstream or disconnect cases needed by the claim.

Report the actual observations and spread. A few samples do not support a reliable p99.
Compare like-for-like fixtures and account for caches, model variation and upstream noise.
Do not trade validation or access checks for speed.

Measure resource ownership directly. Error messages are not evidence of a memory leak,
connection leak or process crash. Observe retained resources across work/cleanup cycles
and distinguish normal caches from continuing growth. Use the project's existing profiler
and observability hooks for deeper investigation; keep payloads and high-cardinality
identifiers out of telemetry.

The [MCP tools contract](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)
and [transport binding](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http)
remain correctness constraints throughout the comparison. A load tool's successful exit
status says little if it ignores `isError`, invalid JSON, dropped requests or partial SSE.
