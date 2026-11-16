---
name: perf-inference
description: Diagnose and improve NVIDIA model inference from the real application through batching, scheduling, caches and distributed serving. Use for latency, useful throughput, GPU capacity or streaming speech performance while preserving model quality and product behavior.
---

# Inference performance

Optimize the useful result delivered to the user under representative load. Inspect the actual
model pipeline, serving code, configuration, traces, benchmark harness and previous experiments.
Reuse the current runtime unless evidence supports replacing it. A language backbone inside a
speech or multimodal model does not make the complete pipeline a stock text-generation server.

## Establish the workload and evidence

Identify model/weights/tokenizer/adapter revisions, architecture, inputs/output lengths, sampling,
precision, runtime/compiler/driver versions, GPU SKU and memory, interconnect, replicas and resource
limits. Inspect the installed CLI/API and model support matrix before proposing flags or kernels.
Separate source implementation, checked-in configuration, historical results and live deployment.
Read reverted experiments as well as successful changes; a commit title does not establish a win.

Define the user boundary and existing quality/latency/cost objectives. Preserve UI, product output,
streaming semantics, authorization and cancellation. Reduced diffusion steps, quantization,
distillation, approximate caching or altered sampling are quality-sensitive proposals, not free
execution optimizations. Do not silently switch models, truncate output or relax numerical oracles.

Read [measurement and acceptance](references/measurement-and-acceptance.md) before choosing a
benchmark or interpreting a speedup. Record offered, admitted, completed and useful work, errors,
queueing and tails. Verify the load generator and output consumer actually sustain the target load.
Fast kernels, high GPU utilization and successful HTTP status alone cannot establish capacity.

## Follow the bottleneck through the pipeline

Map admission → CPU preparation → prefill → decode/denoise → codec/postprocessing → transfers →
output delivery. Include model loading, compilation and graph warmup where they affect the task.
Correlate representative slow requests with existing traces and aggregate resource measurements.
Shared batch work appears in several requests; do not sum duplicate attribution into GPU cost.

Use [perf-cuda](../perf-cuda/SKILL.md) for Nsight timelines, selected kernel counters, asynchronous
timing, compilation/graphs and kernel correctness. Diagnose launch/synchronization, bandwidth,
compute, allocation or communication limits before choosing a technique. Host scheduling,
serialization, transport and CPU postprocessing can dominate after GPU work is optimized.

For batching, KV/prefix reuse, replicas or parallelism, read
[serving and scaling](references/serving-and-scaling.md). For stateful audio, streaming codec,
playback or a coupled language/diffusion pipeline, read
[speech and multimodal inference](references/speech-and-multimodal.md). Load only relevant modes.
Larger batches, more streams, more replicas or prefill/decode disaggregation can regress the goal.

## Run a discriminating experiment

Choose one measured cause, a bounded change and the expected affected interval. Keep comparable
workload, quality criteria, hardware allocation and build settings. Start with removal of repeated
work or unnecessary synchronization when supported; prefer maintained library kernels to custom
ones unless the measured gap justifies ongoing correctness and architecture support.

Use existing authorized hardware, target environment and workload limits. Research or a skill
invocation does not authorize paid GPU rentals, production stress, downloads of large weights,
cluster scaling, privileged containers, driver changes or disruption of other GPU users. Continue
source/trace analysis when execution is unavailable and state the missing GPU evidence.

Check relevant shape/dtype, lane reuse, cache isolation, cancellation, mixed load and failure
boundaries. Compare the original unprofiled full operation after microbenchmarks; include cold
and low-occupancy costs when relevant. Reuse [design-evals](../design-evals/SKILL.md) for
quality-sensitive changes and [evaluate-agents](../evaluate-agents/SKILL.md) when the model is
inside an agent harness. Avoid expanding a focused speed investigation into a new eval platform.

## Keep only supported improvements

Report the baseline/candidate with units, sample counts, quality, useful throughput, latency
distributions, memory/cost and important tradeoffs. Distinguish measurement, inference and proposal.
Reject gains caused by dropped work, incomplete output, easier inputs, hidden retries, weaker
quality or a saturated load generator. Keep, revise or revert based on the actual objective.

Retain minimal redacted measurements and reproduction details, then stop task-owned probes/jobs
and remove owned profiles, exports, temporary audio, builds and isolated caches. Preserve shared
compiler/KV/model caches, weights, datasets, other users' jobs and required failure/recovery
artifacts. Verify cleanup, including cancellation after partial failure. Source selection and
qualification are recorded in [sources](references/sources.md).
