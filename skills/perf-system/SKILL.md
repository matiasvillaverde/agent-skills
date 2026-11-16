---
name: perf-system
description: Investigate measured latency, throughput, CPU/GPU work and memory use, or review algorithm and data-structure opportunities. Use bounded experiments and preserve correctness.
license: MIT
---

# System performance

Define the operation, representative workload, primary metric, correctness constraint
and experiment budget. Inspect existing performance evidence before collecting more.
Do not optimize from a style preference or an unmeasured suspicion alone.
For a requested opportunity review, inspect the operation, input growth and existing evidence,
then suggest candidates as hypotheses. Missing measurements do not justify invented gains or
prevent a useful shortlist; distinguish investigation from an accepted implementation change.

Establish a reproducible baseline: build mode, toolchain, device, input size, concurrency,
cache state and measurement command. Separate warmup from steady work; measure cold
startup separately when it is part of the objective. Compare like
with like and repeat enough to understand run-to-run noise; use the existing budget
or a small local experiment, not an open-ended benchmark campaign.

Measure the relevant resource. Distinguish CPU execution from waiting, GPU work from
CPU submission, allocations from live retained memory, and throughput from tail
latency. Queue depth and data freshness may matter even when responses appear fast.
Read [profiling guidance](references/profiling.md) when selecting or interpreting tools.
For native Rust, Zig, C or C++ workloads, read the relevant sections of
[native profiling](references/native.md): OS tools, hardware counters, memory, scheduling,
I/O, code generation and benchmark validity. Language-specific `perf-rust` and `perf-zig`
can add compiler/runtime details when available; no fixed skill sequence is required.
For Go services or programs, the available `perf-go` adds runtime profiles, goroutine/GC
diagnosis, production tracing and backend instrumentation; native OS tools are complementary.
For Node.js/TypeScript servers or CLIs, `perf-node` adds event-loop, V8/native-memory,
stream and worker diagnosis. `perf-python` adds interpreter-aware CPU/allocation,
asyncio, GIL/native-extension and process-pool profiling. Select `perf-postgres`,
`perf-clickhouse`, `perf-sqlite` or `perf-swiftdata` for the actual database/API layer;
each owns its plans, workloads and storage tradeoffs. SwiftData-owned stores use public
SwiftData APIs rather than direct SQLite tuning. Do not run all specialists by default.

Find the bottleneck and test one hypothesis per variant. Consider removing repeated
work, redundant requests, unnecessary serialization or unbounded concurrency before
introducing caches, pools or custom scheduling. Those mechanisms need measured benefit
and explicit freshness, ownership and overload semantics.

When repeated scans, sorting, lookup, queueing or representation dominate, read
[algorithms and data structures](references/algorithms-and-data-structures.md), then only the
relevant [platform considerations](references/collections-by-platform.md). Compare work avoided,
operation mix, construction/update cost, memory locality and semantic contracts. There is no
universally fastest container. Prefer standard or existing implementations before custom ones.
For an ideas request, return a short ranked set with the code location, mechanism, conditions
where it helps or loses, correctness constraints and the smallest experiment that could decide.
Do not silently turn suggestions into a rewrite or a new benchmark framework.

Reject a variant that breaks correctness, required validation, data isolation or
reproducibility. Keep a change only when the relevant improvement exceeds measurement
noise and earns its maintenance cost. Revert neutral complexity; preserve any unrelated
user changes. Do not weaken the correctness gate to win the benchmark.

For a substantial investigation, keep a compact record of baseline, hypothesis,
command, result and keep/revert decision in the existing task evidence. Do not add a
new performance ledger for every small edit. Recheck the winner against the baseline
under the same conditions. Add a regression budget or monitor only when a stable,
useful signal and its owner exist.

Report measured results with their workload and limits. A quiet smoke run is not
evidence of no leak or a universal performance guarantee. Do not start production
load, change host profiling permissions or make paid calls merely to get a number.

## Finish and clean up

Track task-created artifacts in an isolated directory. Save the compact results and reproduction commands, then stop owned profilers/load generators, restore temporary settings and remove diagnostic instrumentation, raw captures, scratch builds, fixtures and task-only caches. Verify exact path ownership before deletion; preserve shared caches and user data. Retain only requested/required evidence or the minimum needed for unresolved failures. Restore settings and stop owned work even on failure or cancellation; report any leftovers and why.
