# Serving and scaling inference

Use the existing engine and deployment first. A replacement needs a measured limitation and a
compatibility comparison, not a leaderboard win. Verify the installed version, model revision,
tokenizer/processor, adapters, quantization, generation contract and actual loaded configuration.

## Match the engine to the work

| Existing system | Useful controls to inspect | Fit boundary |
| --- | --- | --- |
| vLLM | Iteration batching, chunked prefill, token/sequence budgets, paged KV, prefix caching, parallelism | Check the exact supported architecture, endpoint and feature combination. |
| SGLang | Radix/prefix reuse, scheduler, router, parallelism, optional disaggregation | Compatibility of workers, KV layouts and stateful APIs can constrain a topology. |
| TensorRT-LLM | In-flight scheduler, packed inputs, workspace/KV budget, executor/build configuration | Distinguish current PyTorch executor from legacy engine-build guidance; model/GPU/precision support varies. |
| Triton Inference Server | Dynamic batching, model instances, sequence scheduling, backend metrics | Dynamic batching assumes stateless requests; sequence/iterative scheduling has different ownership. This is not the Triton kernel language. |
| Dynamo | Routing, prefill/decode pools, KV transfer, workload sizing and planner | An orchestration layer using an engine; it does not make unsupported models or incompatible KV states interoperable. |
| Ray Serve or the existing platform | Admission, replica placement, queue limits, cancellation, autoscaling | Inspect the engine queue as well as the serving queue; adding a second batcher can add waiting. |

For speech/diffusion, inspect every stage rather than treating the model as text generation.
The current vLLM-Omni VibeVoice recipe supports a particular native checkpoint, offline eager
single-speaker synthesis and an optional reference voice. That is not evidence of support for
the original checkpoint schema, streaming, multiple speakers or the application's full contract.
[Supported models](https://docs.vllm.ai/projects/vllm-omni/en/latest/models/supported_models/),
[VibeVoice recipe](https://github.com/vllm-project/vllm-omni/blob/704c158f747f60708a3771b34f0f4c5d19d8d4bd/recipes/Microsoft/VibeVoice-1.5B-H100.md).

## Tune the scheduler without hiding latency

Separate maximum simultaneous sequences, tokens per iteration, context limits and queue delay.
They constrain different resources. Test the relevant input/output length distribution and bursts.
Increasing batch capacity can improve throughput while worsening first-output or inter-output
latency, workspace demand and admission fairness. Do not silently shorten inputs or outputs.

For autoregressive models, continuous batching replaces completed sequences between iterations.
Chunked prefill can protect ongoing decodes from a long prompt; smaller chunks also add repeated
work and launch overhead. Compare token budgets against the actual latency objective. vLLM V1
often enables chunked prefill already: inspect effective settings before recommending a flag.
[vLLM tuning](https://docs.vllm.ai/en/stable/configuration/optimization/),
[TensorRT-LLM scheduling](https://nvidia.github.io/TensorRT-LLM/features/paged-attention-ifb-scheduler.html).

For Triton, start with the backend's supported scheduler. Measure any batching delay against
the queue budget. Preferred batch sizes need a measured advantage; stateful streams need verified
sequence affinity and lifecycle. Iterative sequence support is version-sensitive.
[Triton batchers](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/batcher.html).

## Treat caches as correctness-sensitive state

Distinguish KV prefix reuse, multimodal processor caches, response caches, compile caches and
model-weight storage. For reuse, establish the owning model/adapters/processor revision, exact
input identity, layout/dtype, lifecycle, tenant boundary and supported invalidation rules.
Test changed content of equal length, mixed adapters, concurrent tenants, cancellation and eviction.
Never key solely by length or a client-provided identity. A cache salt must reflect trusted tenant
policy; a salt is not authorization. Inspect the engine's actual key construction.
[vLLM cache design](https://docs.vllm.ai/en/stable/design/prefix_caching/).

Measure both warm reuse and realistic misses. A fixed repeated prompt is a best-case experiment.
Include token-weighted hit/miss accounting, cache lookup/transfer cost, recomputation/preemption
and available KV capacity after weights, workspaces, graphs and co-tenants. A larger cache can
reduce request capacity; offloading can shift the limit to host memory or network bandwidth.

## Choose replicas and parallelism from the topology

Independent replicas usually scale separate requests; TP distributes tensor work, PP partitions
layers, and EP distributes MoE experts. They have different communication, memory and latency
costs. Verify model divisibility, GPU memory, NUMA/PCIe/NVLink placement, inter-node fabric and
actual collectives. More GPUs and higher utilization do not establish better cost or latency.
Compare the smallest fitting deployment against a justified alternative; reserve headroom for KV
and workspaces. Record per-rank bottlenecks, not only rank zero or an averaged GPU number.
[vLLM parallelism](https://docs.vllm.ai/en/stable/serving/parallelism_scaling/).

Disaggregate prefill/decode only when independent resource sizing outweighs transfer and routing
cost. Keep an aggregated baseline. Small models, short requests, low load or slow transfer can
favor aggregation. Verify KV layout/version compatibility and the observed transfer path before
changing replica ratios. Long prompts can consume memory in both pools during handoff.
[Dynamo architecture](https://docs.nvidia.com/dynamo/kubernetes/disaggregated-serving/overview),
[SGLang constraints](https://docs.sglang.io/docs/advanced_features/pd_disaggregation).

## Bound admission and release abandoned work

Locate every queue: gateway, router, replica, engine and stage connector. Give each an owner,
capacity, deadline and observable rejection. Count rejected, expired, failed and canceled requests
alongside completed ones. Do not increase queues merely to hide drops or retry every overload.
Derive retry eligibility from the request contract; preserve a bounded overall deadline and avoid
duplicate generations or a replay after partial streaming unless explicitly supported.

Test disconnect and cancellation before admission, while queued, during generation and between
stages. Verify eventual KV/buffer/session release and reclaimed capacity. Async task cancellation
may arrive only at an await; it does not prove an already launched GPU operation stopped. Drain
old replicas without truncating accepted streams, and verify actual engine abort propagation.
[Ray cancellation](https://docs.ray.io/en/latest/serve/http-guide.html#request-cancellation).

Scale using the bottleneck's demand signals and latency objective. Inspect queue age/work,
running work, available KV and arrival mix; GPU utilization alone misses queueing and CPU stalls.
Measure image/model loading, compilation, graph capture and readiness separately. Replica and
node scaling have distinct delays. Retain warm capacity where the objective needs it; compare
startup improvements with steady-state cost. Verify scaling down and recovering from a burst.
[Ray autoscaling](https://docs.ray.io/en/latest/serve/advanced-guides/advanced-autoscaling.html),
[Dynamo tuning](https://docs.nvidia.com/dynamo/kubernetes/operations/performance-tuning).

## Observe the existing system

Join request/stage traces to engine and GPU evidence with bounded identifiers and sampling.
Keep model/version and bounded outcome labels; do not put prompts, voice data, credentials or
unbounded request IDs into metric labels. Reuse the installed telemetry pipeline.
Track offered/admitted/completed work, queue time, first output, output gaps, completion latency,
errors, abandoned work, KV usage/preemption/cache transfer, CPU/RSS and GPU memory/activity.
Read live metric help and units; missing metrics are unknown, not zero. Separate allocator
retention from live-object leaks. Narrow traces explain mechanisms; unprofiled runs decide wins.
[vLLM metrics](https://docs.vllm.ai/en/stable/usage/metrics/).

Keep protocol, stream order, output quality and feature behavior unchanged. Propose one mechanism
at a time, record the effective configuration diff, and reject gains that move cost to another
stage or violate the product objective. No universal queue size, cache fraction, batch size,
utilization threshold, replica ratio or TTFT target belongs in a reusable recommendation.
