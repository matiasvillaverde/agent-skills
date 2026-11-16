# Sources and qualification

Original local synthesis reviewed 2026-11-16. No upstream player, DSP code, hooks, packages or
measurement application is bundled. The focused references link the actual Apple/API/standards
contracts; inspect the current target's versions before applying them.

## Community and measurement ideas

- [sonic-skills audio-performance-debug](https://github.com/kunitoki/sonic-skills/blob/8b6dcfe89030d7de9ba9d6afcc2d927fb11fe7fa/skills/audio-performance-debug/SKILL.md)
  (Unlicense): entrypoint, linked performance patterns and sibling DSP review read. Useful
  worst-cycle and real-time review questions. Callback logging, universal ARM denormal claims,
  incomplete SIMD tails and exclusive-hotspot-only analysis were not adopted.
- [Axiom AVFoundation reference](https://github.com/CharlesWiltgen/Axiom/blob/ffafd3b3e0dbaaa60b753ca4a835ae6603b873e1/axiom-codex/skills/axiom-media/skills/avfoundation-ref.md)
  (MIT): full reference read for lifecycle/route/API leads. Its input-port example is not an
  output selector; current Apple contracts govern. These reproducible pins are not a claim
  that all current upstream skills were audited.
- [WALT methodology](https://github.com/google/walt/blob/9f39d398b7fc54c970b9772f1320299e909f576d/docs/AudioLatency.md)
  (Apache-2.0): full audio-method page, not iOS implementation qualification. Its synchronized
  electrical warmed enqueue-to-output measurement excludes some user-action startup work.
- [SuperpoweredLatency](https://github.com/superpoweredSDK/SuperpoweredLatency/tree/693e3a19f186136386166567ec35d963914f3139)
  (GPL-2.0): README and shared detector read as measurement-method leads only; no code copied.
  Round trip is not one-way output latency. Retry/outlier selection must not hide failures.

## Primary contracts and scope

Apple runtime sources cover parser/converter contracts, PCM source/sink nodes, workgroups,
timestamps, session preferences, route/voice processing, sample generation and thermal signals.
Selected public headers were inspected in iPhoneOS27.0 SDK, Xcode 27.0 build 27A266a:
`AudioConverter.h`, `AudioFileStream.h`, `AVAudioSourceNode.h`, `AVAudioSinkNode.h`,
`AVAudioIONode.h`, `AVAudioNode.h`, `AVAudioSession.h`, `CoreAudioBaseTypes.h`,
`AUComponent.h`, `AudioUnitProperties.h`, `AUAudioUnit.h` and `os/workgroup_object.h`.
This is selected API-surface inspection, not all Apple methods or framework implementation.
The installed Xcode bundle has a Release.Candidate name; its availability is not proof of
device deployment support. Recheck evolving Swift/realtime annotations rather than copying them.

Networking review read relevant current Apple authoring/LL-HLS/API material, WWDC20/21
transcripts and June 2026 HLS update/preliminary draft sections. RFC8216 is the published
Informational baseline; on review date the later -22 remained in the RFC Editor queue.
Version observations are not a runtime compatibility matrix or authorization to change streams.
Archived Apple examples provide context, not current hardware targets.

The vDSP API listing was inspected for returning versus caller-supplied output storage;
the complete DFT setup page was read for allocation, supported lengths, ownership and shared
setup alignment. No Accelerate/DSP kernel was run or certified real-time safe.

Measurement sources include Apple Audio System Trace, CPU/HTTP/power profiling, latency and
completion contracts, XCTest and physical-device guidance. Context7 and search results led
to original documents; Apple Markdown links supplied content when HTML/Exa returned shells.
No reviewed Apple source supplied a turnkey calibrated acoustic-TTFA procedure. The proposed
physical method requires validation of the rig, clock, route and detector uncertainty.

## Execution evidence

Read-only tool discovery confirmed Audio System Trace and the three audio instruments
in Xcode 27. No physical-device benchmark was performed while authoring this skill.
Instrument discovery does not establish target support, populated tracks or valid exports.

An independent agent received this skill and raw synthetic fixtures without the author's
conclusions or conversation. It rejected a candidate with faster response timing but slower
PCM/render milestones, a timeout and underruns. It retained all attempted starts and unknown
acoustic-onset measurements, separated warm Bluetooth from cold speaker results, accounted for
late callback start, and rejected cross-clock and round-trip arithmetic. It also caught false
HLS/parser, input/output routing, real-time logging and Simulator-qualification claims.
The author inspected the report and independently checked original fixture hashes,
deterministic offline regeneration and arithmetic. This is bounded instruction-following
evidence, not comprehensive agent coverage or execution of audio/DSP code.

Real-device TTFA, acoustic onset, decoder/container compatibility, deadlines, battery use and
sustained thermal performance remain unverified until a product-specific experiment runs.
