# Stateful speech and coupled multimodal inference

## Preserve the whole model path

Identify the exact variant and supported execution mode. A speech system can combine a language
backbone, continuous acoustic/semantic tokens, a diffusion head, codec state, speaker conditioning,
alignment and an output transport. The same backbone in a stock text server is not equivalent.
ASR, offline multi-speaker TTS and real-time single-speaker TTS have different support and metrics.
Read the current engine's actual model recipe, not only a family-name checkmark.

The public [VibeVoice repository](https://github.com/microsoft/VibeVoice) and
[Realtime design](https://github.com/microsoft/VibeVoice/blob/16fb2cb1217c9934a886e1948ffb06120caa2df5/docs/vibevoice-realtime-0.5b.md)
illustrate these differences. Research claims about a variant's first-audio latency or languages
are not evidence for an application's serving integration. Preserve the exact model, voice/adapter,
codec, sampling, guidance/solver settings and delivery contract unless a change is authorized.

## Batch without corrupting streams

Stateful batching needs request/lane identity, valid-length masks, KV positions, codec history,
RNG ownership and terminal-state isolation. Test lane joins, exits, cancellation and reuse with
different lengths; a stale buffer can produce plausible output from another request. Keep a lane
generation/ownership boundary so a late callback cannot write into its replacement.

Fixed shapes and preallocated slots can reduce dispatch and permit graph replay. They can also
execute padding/inactive rows, reserve more KV memory and worsen sparse traffic. Choose bounded
shape/KV buckets from measured occupancy and context lengths, including overflow handling.
Capture/warmup can mutate positions, masks, codec state or random generators; restore/reset the
required state before admitting actual work. See the graph reference in `perf-cuda` when available.

New prefills and resumed streams compete with continuing decode/denoise. Group compatible work
and cap admission/prefill work per scheduling opportunity when needed to protect delivery deadlines.
Do not optimize initial batch throughput while starving existing streams. Test burst joins and
replacement soaks as well as an all-at-once steady batch. Keep request-level fairness observable.

## Remove overhead at the right boundary

Potential measured improvements include hoisting invariant projections/embeddings, fusing repeated
elementwise operations, compiling a stable codec/denoiser region and batching small transfers.
They still require reference equivalence. More CUDA streams or overlapped branches may contend
for bandwidth, scratch memory and scheduling resources; retain overlap only after an end-to-end win.

Pinned host buffers and asynchronous D2H can overlap work until a consumer needs samples. A device
completion event must precede host reads and buffer reuse. Avoid per-lane host synchronization when
one completed batch boundary suffices. Keep a bounded pool and explicit ownership through queued
delivery; a request ending does not mean its last copy or playback callback has completed.

Inspect alignment, encoding, transport, serialization, logging, GC and consumer scheduling. CPU
processes can avoid some Python GIL contention but introduce IPC/copy/lifecycle cost. Do not add
threads, processes or device synchronization without evidence. Bound queues; never silently drop
audio, terminal chunks or alignment to report a faster result. Stop a cancelled/closed consumer's
work according to the contract and verify resource reclamation.

## Measure audio delivered and heard

Track request/admission, first generated sample, first playable chunk at the client, subsequent
arrival times and audio seconds, final delivery and required alignment. With a declared initial
playback buffer, compare cumulative received playable duration against elapsed playback time;
negative buffer margin indicates a starvation interval. Account for chunk ordering, gaps, overlap,
sample rate and the actual consumer. Generation alone cannot prove uninterrupted playback.

Define RTF explicitly: compute or elapsed seconds / audio seconds; inverse RTF reverses that ratio.
For TTS use generated valid output duration; for ASR the relevant audio is input. Aggregate output
seconds / benchmark wall seconds measures capacity, not any single listener's continuity. Sum only
validated, nonduplicate completed output under the declared quality policy; keep truncated/failed
audio and completion counts separate. No universal RTF or first-audio target applies to every use.

Hold text, voices, language, lengths and quality settings constant when comparing execution changes.
Check content completeness, intelligibility, speaker identity where required, artifacts, loudness/
clipping, timing and long-form drift. Independent listening or a calibrated task-quality evaluation
may be needed; ASR/WER alone misses prosody and artifacts. A limiter improving delivered audio does
not prove the raw model became more accurate. Keep raw and delivered quality boundaries explicit.

Fewer diffusion steps, changed guidance, reduced precision, intermediate-feature reuse and
distillation can alter quality. Evaluate separately with representative and difficult cases.
Do not change seed/tolerances or copy the optimized output into the reference to force a match.
Per-request seeds do not guarantee bitwise identity across GPUs, compilers or batch schedules;
state the reproducibility promise actually tested.

For broader model support, inspect [vLLM-Omni's current support table](https://docs.vllm.ai/projects/vllm-omni/en/latest/models/supported_models/)
and the exact recipe's online/offline, speaker, chunking and execution-mode constraints. Do not
replace a coupled production path merely because a related model has a successful demo.
