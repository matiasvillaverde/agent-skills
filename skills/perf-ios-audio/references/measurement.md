# Measure the complete playback path

## Define the observable endpoint

Choose an existing real user action and content fixture, including intentional leading silence,
codec priming, trims and playback speed. Identify cold process, cold session/engine, connection,
decoder and app-cache states separately. A process restart does not reset system/CDN caches.
Track the same playback generation through seek, retry, cancellation and route changes.

| Milestone | What it establishes |
| --- | --- |
| User/app start action | Start of the named experience; retain automation/event delivery delay if relevant. |
| Response headers/first payload | Transport progress, not necessarily a complete decodable packet. |
| Required metadata/key/init available | A dependency may be ready; content may still be absent. |
| First decoded PCM | Decoder readiness, not speaker output. Record format, frame count and media position. |
| First content scheduled/consumed by render | Engine progress; distinguish content from starvation fill/silence. |
| Presentation timestamp plus verified route model | An estimate, with clock, validity and latency scope stated. |
| Calibrated physical/electrical onset | Output evidence for the observed route and detection method; state uncertainty. |

Report request-to-PCM, request-to-render and request-to-audible separately when available.
Do not relabel one as another. Buffer-consumed/rendered/played-back completion callbacks refer
to their specified completion boundary, often the end of a buffer; they are not first onset.
Keep intentional silence intact. Define the signal onset criterion; a nonzero sample alone is
not a perceptual audibility test and a silent asset does not demonstrate failed playback.

## Keep clock and latency semantics explicit

`AVAudioTime` can carry host time, sample time or both. Check validity flags and sample rate.
Its host clock uses `mach_absolute_time`; convert with the supported API/timebase. Do not
subtract wall-clock `Date`, server timestamps, continuous-clock ticks or another device's
clock without a verified mapping. A timestamp for a whole buffer must be related to the
specific sample/frame of interest. Reset anchors when discontinuities or routes invalidate them.
[AVAudioTime contract](https://developer.apple.com/documentation/avfaudio/avaudiotime).

Processing latency, downstream presentation latency, I/O-node hardware latency and session
output latency have different scopes. Inspect the chosen renderer's timestamp contract and
what is already included; do not blindly add all latency properties and buffer durations.
A node's reported processing latency of zero can also mean unknown. Public properties are
useful diagnostics, not a calibrated proof of acoustic output across all wireless routes.
[Processing](https://developer.apple.com/documentation/avfaudio/avaudionode/latency),
[downstream](https://developer.apple.com/documentation/avfaudio/avaudionode/outputpresentationlatency),
[I/O node](https://developer.apple.com/documentation/avfaudio/avaudioionode/presentationlatency),
[session output](https://developer.apple.com/documentation/avfaudio/avaudiosession/outputlatency).

If the decision requires actual output onset, use an existing authorized external audio
capture/loopback rig and known test signal. Record trigger/clock alignment, sample rate,
detection threshold, noise floor, cabling/acoustic distance, rig delay and calibration error.
Report electrical and acoustic endpoints distinctly. Round-trip input→output measurement
does not establish one-way output latency; halving it assumes unsupported symmetry. Recording
with the same phone may activate input or change category, processing and Bluetooth route.
Do not silently change the experience to measure it. A manual listening check helps quality
triage but cannot establish precise latency. Missing physical evidence remains a gap.

## Separate startup, continuity and real-time deadlines

Track encoded queue depth/age and decoded PCM occupancy in frames and seconds at the actual
sample rate. Count only usable contiguous media for the current generation; duplicates,
out-of-order segments, undecoded bytes and stale seek buffers are not playable duration.
Account for playback rate, deliberate pauses and clock reanchors. A controlled replay of
arrival/decode times can diagnose starvation; it does not simulate hardware scheduling.

For a render cycle, nominal frame time is `frameCount / sampleRate`. Use actual frame counts
and known deadlines; requested I/O duration is not proof of the granted cycle. Record callback
start lateness and execution duration separately. Finishing quickly after a late start can
still fail. Producer starvation can also create silence in an otherwise on-time callback.
Count overloads, underruns, affected duration, discontinuities and recovery time, not just
average CPU or engine jitter colors. Correlate Audio Client/Server/Statistics and thread states.
[Apple audio analysis](https://developer.apple.com/documentation/audiotoolbox/analyzing-audio-performance-with-instruments).

Instrumentation must not create the deadline failure. Use existing real-time-safe counters
or a bounded preallocated telemetry channel; export/format on a non-real-time consumer. Check
ownership, overflow and dropped-event counters. Do not put JSON, logging, allocation, actor
hops or blocking queue operations in the callback. Unobserved intervals are missing evidence.
Use request spans/signposts outside that path and correlate off-thread.

## Accept comparable, complete results

Declare quality/functionality, startup, continuity and resource criteria before comparing.
Report all attempted starts, failures, timeouts and missing onset samples beside distributions.
Do not assign missing TTFA zero, silently exclude failures or claim p99 from a handful of runs.
Keep routes, devices, cache populations and fixture lengths separate. Include preloaded work
and retained resources in the declared scenario/cost boundary. A warm comparison can be useful
when explicitly warm; it cannot establish a cold-start improvement.

Keep full output/channel/order/timestamp checks, codec/level/quality, seek and cleanup contracts.
Resource evidence can include decode CPU time per played second, memory high-water/retention,
copy/conversion counts, bytes/request count per playback and measured energy. Instrument
availability or low CPU is not battery evidence. Preserve original sound/UI behavior and
evaluate audible artifacts alongside latency. Choose hypotheses from the critical path, then
recheck the complete operation without tracing overhead; noisy or incomplete results remain
inconclusive rather than inviting a looser gate.
