# iOS audio execution and rendering

Use this reference when evidence points below player buffering: custom packet decoding,
PCM scheduling, graph processing, missed render deadlines, or route-dependent latency.
It describes an investigation method, not a measured optimization or universal buffer target.

## Map the actual path

Draw the path that exists: acquired bytes → parser → compressed packets → decoder → PCM
queue → engine/player/source node → DSP/mixer/conversion → output unit → route. Name each
queue's owner, capacity, units, timestamps, and empty/full policy. A byte queue, packet queue,
PCM queue, scheduled-player buffer and device I/O buffer solve different problems.

Keep the current framework until a trace locates its limiting behavior. `AVAudioEngine`
already exposes custom PCM through `AVAudioSourceNode`; a whole RemoteIO rewrite is an
experiment only when the missing control justifies owning buffering, formats and recovery.
Source nodes support PCM conversions; a compressed stream still needs a decoder.
[Apple's engine session](https://developer.apple.com/videos/play/wwdc2019/510/)

## Parse and decode away from the render deadline

- `AudioFileStream` parses arriving data and retains partial-packet state; it does not fetch
  network bytes or decode compressed audio. Feed sequential bytes and process properties and
  packet callbacks. Diagnose late/missing container metadata before reducing render buffers.
  A container can be unstreamable when required metadata follows its audio payload.
  [Parser contract](https://developer.apple.com/documentation/audiotoolbox/audio-file-stream-services)
- For `AudioConverter`, preserve the source ASBD, channel layout, packet descriptions and
  required magic cookie. Keep packet counts, byte capacities and returned byte counts
  consistent; preserve input-buffer lifetime through the next converter input callback.
  Distinguish temporary starvation (zero packets plus a specific nonzero status) from final
  EOF (zero packets/bytes and `noErr`); consume any output returned with a temporary error.
  [Converter example](https://developer.apple.com/documentation/audiotoolbox/encoding-and-decoding-audio)
- Use a bounded producer/consumer PCM buffer when separating decode from rendering. Record
  decoded frames available, decode duration, refill delay and underrun counts outside the
  callback. Preallocate storage, define ownership and publish indices with a reviewed
  synchronization protocol. A lock-free name alone does not prove bounded execution.
- On seek/discontinuity, invalidate obsolete queued generations, apply the parser's
  discontinuity contract, reset/rebuild decoder state as required, and establish a new
  timeline. Validate priming, leading/trailing frames and completion; do not remove converter
  priming blindly. These are correctness conditions for an optimization experiment.

`AudioConverterFillComplexBufferRealtimeSafe` is available from iOS 26. Its documented
guarantee covers PCM conversions, and unsupported non-real-time-safe work returns an error.
Do not infer that arbitrary compressed decoding can safely run in the render callback.
[Realtime converter contract](https://developer.apple.com/documentation/audiotoolbox/audioconverterfillcomplexbufferrealtimesafe(_:_:_:_:_:_:))

## Protect the render callback

Preallocate for the supported maximum render frame count, while honoring the actual count
on every invocation. Avoid allocation/deallocation, file/network I/O, ordinary locks,
dispatching tasks, actor hops, logging, graph mutation and unpredictable object-runtime
work. Keep diagnostic samples in bounded preallocated storage and aggregate elsewhere.
Review the complete call chain: C/C++ can still allocate or block. Swift can own configuration
and UI while an audited C/C++ kernel owns the callback. Apple's sample uses that boundary.
[Signal-generator guidance](https://developer.apple.com/documentation/avfaudio/building-a-signal-generator)

The inspected iPhoneOS 27 SDK adds source/sink/manual-input `RealtimeSafe` block variants
using `CA_REALTIME_API`, and marks those AVFAudio interfaces unavailable to Swift. Select
APIs against the actual deployment target and SDK; do not use `@Sendable`, a newer compiler,
or successful compilation as proof of bounded render execution. The attribute can enable
compiler checks but does not prove a deadline will be met.
[Manual-input declaration](https://developer.apple.com/documentation/avfaudio/avaudioionodeinputblockrealtimesafe)

Measure callback execution and start/cadence variation, including tails and overloads,
against the observed cycle. `frames / sampleRate` describes audio duration, not the whole
app's CPU entitlement. Shared DSP, scheduling and the route also consume the deadline.
On shortage, execute the product's explicit silence/rebuffer policy without waiting for
network/decode work; count the event so a silent callback cannot masquerade as success.

## Format, time and route correctness

- Read actual `sampleRate`, `ioBufferDuration`, channel counts and route after session
  activation and after changes. Preferences are requests; changing them can interrupt I/O.
  Never hard-code one rate or use the preferred rate as the negotiated format.
  [Session preferences](https://developer.apple.com/library/archive/qa/qa1631/_index.html)
- Inventory conversions at every edge: sample rate, channel layout/count, sample type and
  interleaving. Remove redundant conversions only after checking audio fidelity and graph
  compatibility. Smaller buffers increase callback frequency and reduce time per cycle;
  larger buffers may help stability but add latency. Compare the actual product workload.
- Respect `AudioTimeStamp.mFlags`. Host time uses the Mach clock, not assumed nanoseconds;
  sample time is in the relevant sample-rate domain. A source-node sample timestamp can be
  invalid downstream of sample-rate conversion or time stretching. Rebase after reset/seek.
- Treat session input/output latency, node processing latency and downstream presentation
  latency as distinct observations. A zero node latency can mean unknown. Re-read after
  graph/route changes and avoid double-counting downstream totals. These APIs do not replace
  an external end-to-end measurement when acoustic or accessory latency is the question.
- RemoteIO connects to the iOS audio system. VoiceProcessingIO adds voice processing for
  duplex/echo-cancellation use cases. In an engine, changing voice-processing mode requires
  a stopped engine and affects both I/O nodes. Preserve required voice behavior while
  testing; voice processing is not a general playback-speed setting.

## Optimize measured DSP work

For a consequential mixer/filter/transform, compare the existing kernel with an applicable
Accelerate/vDSP operation before hand-written SIMD or GPU offload. Inspect whether the chosen
API creates output storage; preallocate and prepare reusable transform state outside rendering.
DFT setup can allocate, has supported-length constraints and imposes alignment requirements
when sharing setup memory. Preserve ownership and destruction; library branding alone is no
real-time guarantee. Measure actual small buffer sizes, interleaving/stride conversion, SIMD
tails, numerical/audio equivalence and whole-cycle cost. Do not assume a published denormal
slowdown or flushing policy applies to the target CPU.
[vDSP API forms](https://developer.apple.com/documentation/accelerate/vdsp),
[DFT setup contract](https://developer.apple.com/documentation/accelerate/vdsp_dft_zop_createsetup).

## Scheduling and device limits

Framework-owned render threads already join Audio Workgroups. Only investigate custom
workers when measured DSP parallelism warrants them. Workers sharing the I/O deadline join
the device workgroup; asynchronous real-time work uses its own interval/workgroup. Handle
join errors, leave membership correctly, and refresh changing render contexts.
[Workgroup model](https://developer.apple.com/videos/play/wwdc2020/10224/),
[parallel-thread contract](https://developer.apple.com/documentation/audiotoolbox/adding-parallel-real-time-threads-to-audio-workgroups)

Use `os_workgroup_max_parallel_threads` as a hardware/workgroup recommendation, not a live
load sensor or permission to create that many workers. More threads can add synchronization
and contention. Do not set CPU affinity or assume performance-core residency/fixed clocks.
Compare deadline tails, glitches, energy and sustained thermal behavior with fewer workers.
Record device/OS, route, power mode and thermal state; defer optional work under pressure.
[Power/thermal guidance](https://developer.apple.com/documentation/xcode/responding-to-power-notifications)

Source/version details and qualification limits are preserved in [sources](sources.md).
