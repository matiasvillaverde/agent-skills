---
name: perf-ios-audio
description: Measure and improve low-level iOS audio playback on real devices, from networking and HLS segments through parsing, decoding, PCM buffers, render threads and the output route. Use for time to first audio (TTFA), underruns, CPU, memory, energy or playback latency below AVPlayer while preserving sound and product behavior.
---

# iOS audio playback performance

Follow the audio from the user's action to the actual output route. Work with the existing
pipeline: URLSession/custom transport, container parser, decoder/converter, PCM storage and
AVAudioEngine, Audio Units or another supported renderer. This is not an AVPlayer tuning
checklist or a request to replace a correct player with a custom one. AVAudioSession and
AVFAudio remain relevant below AVPlayer. Verify platform and deployment availability.

## Define what faster means

Identify the app/build, device/OS, audio route, session category/mode, actual sample rate and
I/O buffer duration, codec/container, content, transport and cache/startup state. Read the
implementation and existing measurements before changing the engine. Preserve UI, sound,
channels, quality, playback speed, seek/gapless behavior, accessibility, background behavior,
interruptions and cancellation. Lower quality, skipped samples, changed routes and hidden
preloading are not equivalent comparisons.

Read [measurement](references/measurement.md) first. Separate first response byte, first
decodable packet, first PCM, first content render and estimated or measured audible output.
Name the exact TTFA endpoint. A successful request, enqueue, render callback or playback
completion callback does not establish first audible sound. Define existing product budgets
and guardrails; when absent, measure a baseline and label proposed targets. No universal
buffer size, CPU percentage, TTFA target or instrument color establishes acceptance.

## Locate the delay or deadline miss

Map action → session/engine readiness and request dependencies → parser/decoder → buffered
PCM → scheduled/rendered content → hardware/route. These stages can overlap. Correlate
playback generation, resource requests, buffer occupancy and audio timeline; do not add
overlapping durations or subtract unrelated clocks. First-byte time is not all network time.

| Evidence | Focused reference |
| --- | --- |
| Slow first audio, misleading timing, silence or unexplained glitches | [Measurement and acceptance](references/measurement.md) |
| Playlist/key/init/segment waits, transfers, cache or retry behavior | [Network and streaming](references/network-and-streaming.md) |
| Decode, conversion, buffers, callbacks, scheduling or route changes | [Runtime and hardware](references/runtime.md) |
| Physical-device captures, UI automation, reproducible comparisons | [Device workflow](references/device-workflow.md) |

Distinguish network/producer starvation, decoder delay, render scheduling lateness and work
that exceeds a render deadline. Low average CPU can coexist with audible failure. Use the
actual route and frame deadline; a short callback that started late can still miss it.
Inspect current Apple docs and relevant public SDK declarations, defaults, errors and
availability before proposing API changes. Source contracts, observed behavior and inferred
hardware mechanisms are different evidence. Do not depend on private APIs or undocumented
thread/core affinity, and do not assume a codec uses hardware on a particular device.

## Change and verify one cause

Choose a bounded experiment tied to an observed delay. Prefer removing repeated parsing,
copies, allocations, conversion or synchronization before introducing a new framework,
custom kernel or scheduler. Smaller buffers, more decoding threads, smaller HLS segments,
LL-HLS, GPU offload and more prefetching all require an end-to-end tradeoff measurement.
Keep network, decoding, logging and unbounded coordination outside the real-time render path.

Reuse [perf-apple](../perf-apple/SKILL.md) for the existing Audio System Trace recipe,
Instruments catalog, hardware references and capture/export helpers. Use the few tracks
that answer the question; inspect actual populated evidence. Simulator runs can validate
logic and automation, not qualify iPhone hardware, route, radio or energy performance.
Use existing authorized apps/devices and fixtures; do not change device security, production
streams, codecs or network settings simply to obtain a benchmark. Report unavailable devices.

Compare baseline and candidate without heavy diagnostics on the same relevant conditions.
Retain failed starts, timeouts, dropouts and missing measurements. Check complete audio and
meaningful lifecycle cases, including delayed consumers, seek/cancel, route/interruption,
recovery and sustained memory/thermal behavior as relevant. Keep a few discriminating tests
in the existing harness; avoid a Cartesian device/route/network test suite.

Report absolute TTFA with endpoint/evidence type, tails and sample counts, underrun duration,
deadline misses, decode/CPU work, buffers/memory, bytes/requests and energy evidence. Keep
only improvements exceeding observed noise while preserving the product and resource budget.
Mark estimates, missing coverage and inconclusive outcomes explicitly.

Save compact redacted results, stop task-owned captures/runners and remove owned traces,
HARs, temporary audio, exports, DerivedData and isolated caches after triage. Preserve shared
caches, source media, golden cases, required failure evidence and other users' processes.
Restore task-changed routes/network settings. [Sources and qualification](references/sources.md)
record provenance and what has actually been verified.
