# Investigating Apple APIs and hardware

Use this when choosing an optimization, interpreting an unexplained profile, or investigating
an API/hardware limit. Follow the evidence to useful depth; do not require an SDK-wide audit for
every task. Contents: public API review, implementation experiments, hardware map, evidence record.

## Review the relevant public API surface

Start with a falsifiable question from the trace, such as whether repeated decoding, executor
hops, connection setup or CPU/GPU synchronization explains the delay. Search current Apple docs,
release notes, WWDC transcripts and sample code, then inspect the installed SDK. Follow new
symbols and conflicting claims until the question is answered or a concrete access gap remains.

For each implicated framework/type, review all public members that could affect the operation:
methods and overloads, initializers, properties/defaults, inherited members, protocol requirements,
delegates, callbacks, async variants and relevant extensions. Include neighboring APIs for reuse,
batching, streaming, cancellation, diagnostics and capability detection. Record the types/member
groups reviewed and exclusions; do not claim to have inspected every public Apple method.

For plausible candidates, check deployment/platform availability, deprecation, entitlement or
device requirements, error/fallback behavior, thread/actor isolation, ownership, copying,
buffering, ordering, lifetime and cancellation semantics. A method's existence does not establish
its performance, or that it runs on a particular accelerator.

Read public headers, `.swiftinterface` files and Xcode generated interfaces for the actual target
SDK; compiler diagnostics from a minimal call site resolve import/availability questions. For
example, locate Foundation's installed declarations with:

```sh
task_sdk="$(xcrun --sdk macosx --show-sdk-path)"
rg --files "$task_sdk/System/Library/Frameworks/Foundation.framework" \
  | rg 'NSURLSession\.h$|\.swiftinterface$'
```

Select the correct SDK instead of copying `macosx` into an iOS investigation. Read the relevant
declarations and comments around a hit, not just its name. Examples checked in the macOS 27 SDK:
URLSession's `multipathServiceType` has different iOS/macOS availability; `MTLDevice` exposes
`supportsFamily`, `hasUnifiedMemory`, nullable `counterSets` and `recommendedMaxWorkingSetSize`.
The last is a recommendation, not a guaranteed memory entitlement. Recheck these on the target.

Treat old tutorials as versioned evidence. In particular, do not infer execution placement from
`async`, `await` or `nonisolated` alone: inspect compiler version, default isolation and enabled
features. [SE-0461](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0461-async-function-isolation.md)
introduces caller-actor behavior behind `NonisolatedNonsendingByDefault` and explicit `@concurrent`.
Confirm actual execution in the selected build; preserve structured cancellation and isolation
instead of mechanically replacing work with detached tasks.

## Inspect implementation and test hypotheses

Use the least invasive evidence that resolves the question:

1. **Contracts and capability queries:** current public docs, SDK declarations and a small
   representative reproduction. This is the basis for supported shipping behavior.
2. **Published implementation:** inspect relevant release-tagged code in
   [Apple XNU](https://github.com/apple-oss-distributions/xnu),
   [libdispatch](https://github.com/apple-oss-distributions/libdispatch), or
   [Swift compiler/runtime](https://github.com/swiftlang/swift). Pin the revision and explain any
   mismatch with the deployed OS/toolchain. Open-source code may not match the shipping binary.
3. **Compiler and binary inspection:** examine your optimized build's SIL, LLVM IR, assembly,
   symbolicated call stacks and call sites for copying, retain/release, specialization, allocation,
   vectorization or synchronization. Match real optimization/target settings and symbols.
   `xcrun swiftc -help` exposes `-emit-sil`, `-emit-ir` and `-emit-assembly`;
   `xcrun lldb` provides `disassemble --name <symbol> --mixed`. Inspect offline where sufficient;
   these help commands were checked locally, not a claim that a product was disassembled.
4. **Controlled black-box investigation:** when public explanations are incomplete, vary one
   factor (input size, batch size, alignment, concurrency or warm state), predict the result,
   and measure with the appropriate counters/timeline. Consume outputs to prevent dead-code
   elimination; preserve representative data and distinguish harness overhead. Seek a competing
   explanation and corroborate with a second observable before assigning a mechanism.
5. **Deeper reverse engineering:** read original hardware/implementation research or inspect
   authorized binaries when this can change the decision. Record the chip, OS, toolchain and
   reproducible observation. Undocumented behavior is a hypothesis to validate, not a stable
   Apple contract or a reason to ship private APIs. Do not expand ordinary app profiling into
   firmware modification, boot/security-setting changes or driver injection.

There is no need to reverse engineer a framework when a public API and measured fix answer the
question. Stop when added depth is unlikely to change the decision; retain unresolved mechanisms
explicitly. A single benchmark cannot establish every internal cache, core or accelerator detail.

## Hardware and subsystem reading map

Read the row relevant to the bottleneck, then follow its primary references. Resource limits,
capabilities and microarchitecture vary by generation and device; avoid hard-coded chip folklore.

| Subsystem | Questions and sources | Interpretation limit |
| --- | --- | --- |
| CPU, caches, P/E cores, SIMD/SME | [Apple CPU guide](sources.md#apple-cpu-and-metal-references), [public overview](https://developer.apple.com/documentation/apple-silicon/cpu-optimization-guide), [CPU tuning](https://developer.apple.com/documentation/apple-silicon/tuning-your-code-s-performance-for-apple-silicon), [CPU profiling session](https://developer.apple.com/videos/play/wwdc2025/308/): compute versus memory/branch limits, scheduling and useful instruction support | Obtain an authorized guide copy when available and read the relevant sections. Generic Arm ISA semantics do not establish Apple microarchitectural latencies or cache sizes. |
| GPU, tiles, memory bandwidth | [Apple GPU/TBDR architecture](https://developer.apple.com/documentation/metal/tailor-your-apps-for-apple-gpus-and-tile-based-deferred-rendering), [storage modes](https://developer.apple.com/documentation/metal/choosing-a-resource-storage-mode-for-apple-gpus), [device queries](https://developer.apple.com/documentation/metal/device-inspection), [feature tables](https://developer.apple.com/metal/Metal-Feature-Set-Tables.pdf): pass structure, tile traffic, supported families and counters | Unified memory does not remove bandwidth, synchronization or lifetime costs. Use current feature queries; private/memoryless resources have specific access and lifetime rules. |
| Neural Engine and ML placement | [MLComputePlan](https://developer.apple.com/documentation/coreml/mlcomputeplan-1w21n), [Core AI Instruments guide](https://developer.apple.com/documentation/coreai/analyzing-model-runtime-performance-with-instruments): supported execution, setup, copies and inference | Plans report anticipated devices and estimated costs. Confirm actual execution and end-to-end cost; no complete public Neural Engine microarchitecture is claimed here. |
| Media engines and audio | [VideoToolbox session properties](https://developer.apple.com/documentation/videotoolbox/vtsessioncopysupportedpropertydictionary%28_%3Asupportedpropertydictionaryout%3A%29), [Audio Workgroups](https://developer.apple.com/videos/play/wwdc2020/10224/), [audio tracing](https://developer.apple.com/documentation/audiotoolbox/analyzing-audio-performance-with-instruments): actual codec capabilities, buffer deadlines and scheduling | Enumerate supported properties on the real session; do not infer hardware acceleration from an API name. Keep codec/format quality, routes and interruption behavior. |
| Display and compositor | [Variable refresh](https://developer.apple.com/videos/play/wwdc2021/10147/), [visionOS pipeline](https://developer.apple.com/documentation/visionos/analyzing-the-performance-of-your-visionos-app): app/render/display phases and deadline misses | Display refresh, app FPS and generated/reprojected frames are different measurements; simulator results do not establish physical display behavior. |
| Storage, VM and networking | [Storage performance](https://developer.apple.com/videos/play/wwdc2019/419/), [network latency](https://developer.apple.com/videos/play/wwdc2022/10078/), [XNU subsystem map](https://github.com/apple-oss-distributions/xnu/blob/main/README.md): page faults, filesystem work, transport phases and queueing | Logical I/O is not identical to physical storage traffic; HTTP timing alone cannot identify radio firmware or remote-server internals. Measure the relevant boundary. |
| Power, thermal and sustained load | [Power Profiler](https://developer.apple.com/documentation/xcode/measuring-your-app-s-power-use-with-power-profiler): app/system attribution, thermal state and time spent active | A short burst on a cool device does not establish sustained capacity; charging and device conditions can change interpretation. |
| Undocumented hardware | [Asahi subsystem introduction](https://asahilinux.org/docs/platform/introduction/), [AGX research](https://asahilinux.org/docs/hw/soc/agx/): original reverse-engineering notes and implementation leads | These are independent, version-specific observations, sometimes explicitly tentative. They are not Apple API contracts or instructions to reproduce invasive experiments on the user's machine. |

For offline Metal research, use the [official Metal PDFs](sources.md#apple-cpu-and-metal-references):
MPP for matrix kernels and GPU ML, the language specification for shader contracts, and the
feature tables for family limits. Match their versions to the selected SDK and hardware.

The feature-table family mapping was reviewed selectively; this is not a complete specification
audit. Read source sections relevant to the actual target and identify unavailable/gated material.
Use [the instrument catalog](instruments.md) for per-instrument workflows and additional WWDC
links, rather than duplicating every manual here.

## Keep a useful evidence record

For each decision-changing finding, retain: question; source URL and version or SDK header;
exact API/type group; **documented / observed / inferred** status; reproduction and workload;
counterevidence; applicability limits; and resulting decision. Resolve conflicts using actual
target behavior and current contracts. Do not claim full-source review from a search snippet or
an inaccessible page, and do not copy entire SDKs or manuals into the skill.

Preserve compact findings and source links. Remove task-owned probes, disassembly exports,
captures and isolated caches under the main skill's cleanup rules. Keep dependencies on private
implementation details out of production code and record any unresolved documentation gaps.
