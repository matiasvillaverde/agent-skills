# Measure useful inference capacity

## Define the boundary and denominator

| Workload | Useful measurements | Do not substitute |
| --- | --- | --- |
| Interactive text | First useful output, completion latency, token delivery gaps, output length, successful requests/s meeting the declared SLO | First empty event, HTTP headers, acceptance or mean GPU time |
| Offline text/embedding | Correct completed items or tokens per wall second, latency distribution, cost per accepted result | Requested tokens, padded work or summed per-worker rates over unequal windows |
| Streaming speech | First playable audio, per-chunk arrival and audio duration, playback gaps/underruns, completion/alignment/quality | Internal model frames, first bytes of a header or aggregate real-time factor |
| Image/video/diffusion | Complete accepted outputs at required shape/quality, latency, memory and cost | Fewer solver steps, resolution or frames without an explicit quality comparison |

Define goodput as completed requests satisfying all declared criteria divided by the common
measurement window. Also show the passing fraction over offered/attempted work, with admission
rejects, errors, timeouts, cancellations and incomplete outputs visible. A tool's latency-goodput
metric does not automatically check semantic/model quality. Zero executed cases is not a pass.

Keep stage timings distinct from end-to-end latency. Parallel spans and GPU work overlap; sums
of stage p99 values or host API totals do not reconstruct the request's critical path. Distinguish
host submission, device completion and client receipt. A chunk may contain several tokens, so
average time per token and actual inter-chunk gaps answer different questions. Record which
tokenizer or provider usage produced counts; malformed or missing counts are unknown, not zero.

## Reproduce the actual load

Pin model/artifact, runtime, prompt/data mixture, lengths, sampling, quality settings, hardware,
memory allocation, network path, driver/compiler and relevant build flags. Keep a representative
mix of short/long requests, shared/unique prefixes, adapters, cache states and output lengths.
Synthetic repeated prompts can exaggerate cache gains. Do not compare a warmed candidate with
a cold baseline or remove cold loading/JIT/capture from a cold-start claim.

Choose arrival rate, fixed concurrency, trace replay or a bounded burst because it matches the
question. Closed-loop clients wait for completion and reduce offered load as the server slows;
they do not establish an externally imposed arrival-rate capacity. For open-loop/replay loads,
record scheduled versus actual send times and generator lag. If the client cannot send/read on
schedule, the intended workload was not achieved. HTTP connection limits, parsing, tokenization,
audio consumers and CPU/GIL/GC can bottleneck the generator independently of the model.

At relevant levels, include low occupancy, saturation knee, bursts, long-context pressure and
mixed-length churn. Record offered/admitted/completed counts, queue age, timeout/cancel rates,
inflight work and per-request quality. A throughput plateau with rising tails is not more capacity.
Bound total requests, duration, concurrency, output length, GPU memory and spending. Do not load
production just because an example benchmark command defaults to a reachable endpoint.

Separate loading, JIT/autotuning, graph capture, warmup and steady execution. Warm the actual
request path, including codecs/postprocessing and shape buckets. Declare the warmup policy before
comparison; do not discard a variable number of bad runs until results look good. Benchmark without
profiler instrumentation for final claims and use repeated comparable runs where noise matters.

## Use tools as measurement adapters

- [NVIDIA AIPerf metrics](https://docs.nvidia.com/aiperf/reference/ai-perf-metrics-reference):
  inspect the installed version, parser and record exports. TTFT depends on what counts as content;
  inter-token estimates can differ from inter-chunk timing. Its documented audio RTFx uses **input**
  duration for ASR; it does not automatically measure generated TTS audio or playback.
- [GenAI-Perf goodput](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/perf_analyzer/genai-perf/docs/goodput.html):
  configure the actual SLOs and inspect failures. Example latency limits are not recommendations.
- [NVIDIA TTS measurement](https://docs.nvidia.com/nim/speech/latest/reference/performances/tts/performance.html):
  useful first/inter-chunk boundaries and output-duration throughput; its closed-loop methodology
  and hardware-specific tables are not a substitute for a product's arrival pattern.
- Use the existing engine's benchmark/export tools when they preserve these boundaries. CLI success
  is not proof of correct parsing or full coverage. Do not introduce a second load harness casually.

Inspect one raw permitted request timeline and verify the exporter arithmetic before a large sweep.
Do not average replica/region percentiles or combine different load modes into one result. Preserve
sample counts and censoring. Tail estimates from a handful of requests are exploratory only.

## Acceptance and evidence

Numerical equivalence, model quality and delivery correctness are separate checks. Keep a trusted
operation reference and product-specific golden cases: valid text, full audio, speaker/content,
timestamps, image fidelity or whichever output the user relies on. Near-identical logits or finite
tensors do not prove semantic parity. Approximate methods require explicit acceptable tradeoffs.

Report absolute baseline/candidate numbers, variation, known regressions, successful goodput per
allocated GPU and actual monetary/energy cost only when measured. Include idle replicas, warmup,
retries, CPU work and transfer overhead in the relevant cost boundary. GPU utilization is diagnostic,
not a goal. Keep request-level failures visible even when the aggregate improves.

Minimum receipt: scenario/config identities; timing boundary/window; load and actual offered counts;
completed/quality-valid/SLO-valid counts; latency and output distributions; resource allocation;
quality results; a causal hypothesis and keep/revert decision; retained evidence and gaps. A local
replay validates the measurement logic, not actual GPU speed or deployed capacity.
