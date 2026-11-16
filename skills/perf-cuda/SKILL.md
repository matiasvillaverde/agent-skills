---
name: perf-cuda
description: Diagnose NVIDIA CUDA workload and kernel performance with Nsight Systems, targeted Nsight Compute, compilation and CUDA graphs. Review kernel selection, asynchronous buffer ownership, precision and sanitizer evidence while preserving correctness and representative end-to-end timing.
license: Apache-2.0
---

# CUDA performance

Use this for supported NVIDIA CUDA workloads, including kernels produced by PyTorch or Triton. It does not profile Apple Metal or AMD ROCm. Identify the GPU, driver, runtime, compiler/framework and profiler versions. Inspect installed `nsys` and `ncu` help and supported sections rather than assuming another version's flags or metrics.

Define the operation, representative shapes/dtypes, concurrency, correctness reference and experiment budget. Record build flags, device allocation, inputs, cache state and power/thermal conditions. Keep a clean baseline. Separate startup, JIT compilation/autotuning and steady execution; do not exclude cold costs when those are the problem.

For PyTorch host overhead, compilation, CUDA graphs, stream ownership or cache behavior, read
[compilation and graphs](references/compilation-and-graphs.md). For kernel selection, precision,
quantization, communication dependencies or Compute Sanitizer, read
[kernels and correctness](references/kernels-and-correctness.md). Read only the relevant reference.
For whole-model inference, scheduling, serving and output-quality qualification, use
`perf-inference` when available; this skill owns the CUDA diagnosis beneath that workflow.

## Find the consequential work

When the bottleneck is unknown, use Nsight Systems before detailed kernel counters. Reuse an existing suitable trace instead of recording again.

Capture a bounded relevant region with CUDA/NVTX tracing, supported profiler markers or a duration limit. Start with the installed reports for kernel totals, CUDA API activity and memory transfers; add CPU scheduling, library or communication detail only to answer a concrete question. Correlate GPU idle intervals with submission, dependencies, transfers and CPU work. Zero queue time alone does not establish starvation.

Rank kernels by contribution to the representative operation, including launch frequency. Examine transfer and communication overlap and per-rank imbalance where relevant. CPU API time and GPU execution overlap: subtracting their totals does not yield host overhead. Preserve the trace and identify each reported number's source.

## Explain selected kernels

Use Nsight Compute only for the kernels or ranges that matter. Discover sections with `ncu --list-sections`; collect a small relevant set, such as SpeedOfLight, MemoryWorkloadAnalysis, LaunchStats or Occupancy, when available. Filter kernel names and bound launch count before broad collection.

Treat throughput, occupancy, memory hierarchy and warp-stall metrics as evidence for a hypothesis. No fixed SOL percentage, occupancy target or duration cutoff proves a bottleneck or warrants a rewrite. Higher utilization is not inherently a faster user operation.

Confirm warmup/autotuning finished and the measured configuration is the intended one. A fixed launch-skip count can still select autotuning. Understand replay mode: repeated kernels or applications, serialization, memory save/restore, cache flushing and clock control can change behavior and cost. Record these settings; preserve required cross-stream/rank dependencies and avoid replaying external effects.

## Time and validate correctly

For sparse/dense representation, layout or algorithm alternatives, the shared
[data-structure review](../perf-system/references/algorithms-and-data-structures.md) adds candidates
when available. Include conversion, temporary memory, transfers and synchronization; preserve
index and numerical semantics rather than judging a kernel in isolation.

GPU submission is asynchronous. Use completion-aware timing or appropriate GPU events; wait for the measured work before reading elapsed time. A single-stream event pair does not establish multi-stream or host end-to-end latency: include relevant terminal dependencies and transfers through the consumer boundary. Synchronization added to isolate a diagnostic kernel may destroy normal overlap, so do not carry it into the representative final benchmark.

Keep buffers, pinned host memory and tensors alive until dependent transfers/kernels finish. Preserve stream dependencies and allocator ownership when changing concurrency. Distinguish live allocated memory from reserved allocator pools and device-reported usage; clearing caches does not fix retained tensors.

Validate against the trusted reference before accepting speed. Use relevant shapes, strides, dtypes and boundary cases, with explicit tolerances appropriate to the operation. Finite output or successful execution alone is insufficient. Do not relax accuracy, enlarge workload dimensions or change semantics to manufacture a win.

Re-run the original unprofiled end-to-end workload with the candidate. Report absolute latency/throughput, variability, correctness and memory effects; reject kernel-only wins that regress the actual objective.

## Bound operations and conclusions

Do not automatically use sudo/privileged containers, change counter-access policy, stop DCGM or another profiler, alter host clocks, or replace drivers. Report unavailable measurements and continue independent analysis within existing authorization.

Keep reports private. Retain improvements exceeding noise and maintenance cost. Distinguish measured facts, derived calculations, hypotheses and unverified coverage.

## Finish and clean up

Save the compact measurements and reproduction commands, then stop owned profiling/benchmark processes and remove task-created Nsight captures, exports, scratch binaries and isolated compilation/autotuning caches. Track exact task-owned paths; preserve shared driver/compiler caches, model weights, datasets and other users' GPU work. Remove temporary instrumentation and restore task-changed settings even on failure or cancellation. Keep only requested/required evidence or the minimum needed for unresolved failures. Verify cleanup and report leftovers with the reason.

Sources, modifications and licensing: [NOTICE.md](NOTICE.md).
