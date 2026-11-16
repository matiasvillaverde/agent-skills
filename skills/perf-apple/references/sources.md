# Instrument documentation and review limits

Reviewed 2026-11-14 against **xctrace 27.0 (27A266a)**. The exact inventory comes from the
installed CLI and Instruments Library. All 63 individual
`--instrument NAME --show-recording-options` calls succeeded without starting a recording.
This is discovery/configuration evidence, not device recording qualification.

## Best starting points

| Source | Used for / read scope |
| --- | --- |
| [Apple Instruments tutorials](https://developer.apple.com/tutorials/instruments/getting-started-with-hang-analysis) | Hang workflow, optimized Profile builds, timeline inspection; relevant tutorial sections |
| [Xcode 27 release notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-27-release-notes) | Instruments section: CLI options, SwiftUI layout, concurrency history, StateReporting, native-template import |
| [CPU call-tree analysis](https://developer.apple.com/documentation/xcode/analyzing-cpu-profiles-with-call-tree-views) | Different profile meanings, Call Tree/Top Functions/flame graph |
| [CPU bottlenecks](https://developer.apple.com/documentation/xcode/addressing-cpu-bottlenecks) | Guided counters, remarks and Suggested Next; relevant procedural sections |
| [Processor Trace](https://developer.apple.com/documentation/xcode/analyzing-cpu-usage-with-processor-trace) | Hardware/OS recording requirements and call/instruction/cycle interpretation |
| [SwiftUI performance](https://developer.apple.com/documentation/xcode/understanding-and-improving-swiftui-performance) | Update lanes and cause/effect analysis; relevant sections |
| [HTTP analysis](https://developer.apple.com/documentation/foundation/analyzing-http-traffic-with-instruments) | Request hierarchy, transaction phases, URL Loading System scope and unencrypted capture |
| [Disk writes](https://developer.apple.com/documentation/xcode/reducing-disk-writes) | Logical/physical I/O and filesystem advice; profiling sections |
| [Audio analysis](https://developer.apple.com/documentation/audiotoolbox/analyzing-audio-performance-with-instruments) | Audio Client/Server/Statistics, engine jitter and correlation workflow |
| [Metal performance](https://developer.apple.com/documentation/xcode/analyzing-the-performance-of-your-metal-app) | Game Performance composition, optional counters, frame pacing; capture/analysis sections |
| [Metal memory](https://developer.apple.com/documentation/xcode/analyzing-the-memory-usage-of-your-metal-app) | Allocations/private resources, resource events, VM footprint |
| [visionOS performance](https://developer.apple.com/documentation/visionos/analyzing-the-performance-of-your-visionos-app) | RealityKit tracks, pipeline bottlenecks, device-versus-simulator limits |
| [Foveated streaming](https://developer.apple.com/documentation/foveatedstreaming/analyzing-the-performance-of-a-foveated-streaming-session) | Instrument setup and meanings of streaming/pose/frame metrics |
| [Power Profiler](https://developer.apple.com/documentation/xcode/measuring-your-app-s-power-use-with-power-profiler) | Device scope, charging/sleep effects, app/system attribution and cross-device limits |
| [Core AI profiling](https://developer.apple.com/documentation/coreai/analyzing-model-runtime-performance-with-instruments) | Specialization/load/setup/inference and compute-unit correlation; full article |
| [Foundation Models profiling](https://developer.apple.com/documentation/foundationmodels/analyzing-the-runtime-performance-of-your-foundation-models-app) | Request/tool/model tracks, token categories, first-token versus generation latency and sensitive capture |
| [Recording performance data](https://developer.apple.com/documentation/os/recording-performance-data) | OSSignposter intervals/IDs and instrument usage |

Apple's JavaScript documentation pages expose **View Markdown**. Use that linked version
when the HTML reader only sees a JavaScript notice. Do not count a successfully opened shell
page as having read the article. The catalog also links targeted WWDC sessions; these were
reviewed by topic/selected transcript sections, not every minute of every linked talk.

## Acceptance, API and hardware research

The follow-up [acceptance rules](acceptance.md) and [investigation guide](investigation.md) are
original local synthesis. Their hardware table is a source map, not a claim to have audited all
Apple hardware or all public methods. Additional material reviewed on 2026-11-14:

| Evidence | Read scope and consequence |
| --- | --- |
| [Responsiveness](https://developer.apple.com/documentation/xcode/improving-app-responsiveness) | Rough timing thresholds and pipeline caveats; these inform targets without defining a universal SLO |
| [Performance tests](https://developer.apple.com/documentation/xcode/writing-and-running-performance-tests) | Release/test-plan configuration, baseline/tolerance and reporting; separate diagnostic correctness runs from timing |
| [CPU guide overview](https://developer.apple.com/documentation/apple-silicon/cpu-optimization-guide) and [guide access and reading guidance](#apple-cpu-and-metal-references) | Use the public overview and an authorized guide copy; detailed technical chapters remain task-specific reading |
| [GPU/TBDR](https://developer.apple.com/documentation/metal/tailor-your-apps-for-apple-gpus-and-tile-based-deferred-rendering), [storage modes](https://developer.apple.com/documentation/metal/choosing-a-resource-storage-mode-for-apple-gpus), [device inspection](https://developer.apple.com/documentation/metal/device-inspection), [feature tables](https://developer.apple.com/metal/Metal-Feature-Set-Tables.pdf) | Relevant architecture, storage and capability sections; PDF family table selectively reviewed, not the complete specification |
| [MLComputePlan](https://developer.apple.com/documentation/coreml/mlcomputeplan-1w21n) | Overview and member groups; estimated costs/anticipated devices remain distinct from recorded execution |
| [VideoToolbox supported properties](https://developer.apple.com/documentation/videotoolbox/vtsessioncopysupportedpropertydictionary%28_%3Asupportedpropertydictionaryout%3A%29) | Function declaration and returned property metadata; inspect the actual session's capabilities |
| [SE-0461](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0461-async-function-isolation.md) | Status, motivation, proposed semantics and feature gating; old nonisolated-async advice needs toolchain/settings qualification |
| [XNU README](https://github.com/apple-oss-distributions/xnu/blob/main/README.md), [Asahi subsystem introduction](https://asahilinux.org/docs/platform/introduction/), [AGX notes](https://asahilinux.org/docs/hw/soc/agx/) | Subsystem map and selected original research with explicit uncertainty; no release-pinned implementation audit or hardware reverse-engineering experiment performed |
| Installed SDK and compiler/debugger help | Selected `NSURLSession.h` and `MTLDevice.h` declarations in macOS 27.0; `swiftc` emission options and LLDB disassembly help. This does not establish availability on every deployment target. |

No product binary was disassembled, no app behavior was changed, and no additional performance
claim was measured for this documentation follow-up. Research advanced from acceptance thresholds
to platform availability and hardware capabilities, then checked conflicting concurrency advice
against the language proposal. Unavailable detailed hardware semantics remain explicitly unknown.

## Apple CPU and Metal references

Obtain the Apple Silicon CPU Optimization Guide through
[Apple Developer Downloads](https://developer.apple.com/download/all/?q=Apple%20Silicon%20CPU%20Optimization%20Guide)
using your own developer access where required. This repository does not distribute it.
Follow the document’s access and redistribution terms. If it is unavailable, use Apple’s
public CPU profiling documentation and report the missing reference.

For a locally available authorized copy, record its version and read only the sections
relevant to the measured bottleneck and target hardware. Use `pdfinfo` to inspect metadata
and `pdftotext -f START -l END PATH -` for selected pages when Poppler is available.
Check printed versus PDF page numbers and render tables or diagrams when needed.
Keep read depth explicit; possession of a guide does not establish a complete review.

Public Metal references are available directly from Apple:

| Official reference | Consult for |
| --- | --- |
| [Metal Performance Primitives Programming Guide](https://developer.apple.com/download/files/Metal-Performance-Primitives-Programming-Guide.pdf) | Matrix kernels, tiling, accumulation, synchronization and GPU ML performance |
| [Metal Shading Language Specification](https://developer.apple.com/metal/Metal-Shading-Language-Specification.pdf) | Shader semantics, address spaces, atomics, synchronization and language features |
| [Metal Feature Set Tables](https://developer.apple.com/metal/Metal-Feature-Set-Tables.pdf) | GPU-family support and resource limits; corroborate with actual `MTLDevice` queries |

Check the downloaded version and target SDK/device support. MPP GPU neural accelerators
are distinct from the Neural Engine. Cite the version, section and page actually used.
Apple’s terms govern these documents; the skill license does not apply to them. Keep
PDF binaries and full-text mirrors outside this repository. Persistent reference copies
are not disposable profiling traces and should survive trace/cache cleanup.

## Documentation shipped with Xcode

In the selected Xcode, these files are alongside the Developer directory:

```text
Applications/Instruments.app/Contents/Packages/
  <package>.instrdst/Contents/Documentation/overview.html
  <package>.instrdst/Contents/Documentation/fulldoc.html
```

Prefix this with the **parent** of the selected `Contents/Developer` directory, respecting
an explicit `DEVELOPER_DIR` (for example, `Xcode.app/Contents/Applications/Instruments.app`).
In this Xcode, **28 packages** contain these documents. Relevant descriptions/schema
sections were inspected for ActivityMonitor, Audio, CPU Profiler, CoreAnimation, CoreML,
DataPersistence, Dispatch, GPU/GPUBase/GPUCounters, HTTPTracing, Hangs, Hitches, IOKit,
Neural Engine, RealityKit, RunloopInstrument, Sampling, SceneKit, SwiftUI, SystemTrace,
Thermal and dyld. This was targeted schema review, not a review of every internal modeler.

Useful details include cycle weights versus time weights; Core Animation phase/frame
identifiers; audio callback/jitter fields; estimated run-loop boundaries; SwiftData/Core Data
fault/fetch/save schemas; VM/thread states; and driver-dependent graphics counters. These
bundled documents are primary evidence for this build, but internal schemas are not a public
stability promise or proof that a table exports from a particular trace. Do not copy Apple's
full documentation into the skill or construct parsers from guessed table identifiers.

## Gaps and version conflicts that matter

- **Sampler, Advanced Graphics Statistics, SceneKit Application, Location Energy Model**:
  dedicated current public how-to material is sparse. The catalog distinguishes Library/schema
  descriptions from our practical interpretation; exact target support still needs a trace.
- Legacy **View Body / View Properties** remain installed for older target OS versions;
  current SwiftUI guidance should not be retroactively assumed to apply to them.
- Older documentation uses **Thread State Trace**, **Core Data**-prefixed names or **Energy Log**.
  Use the actual current inventory; Energy Log is absent from this installation.
- The Library describes Metal Performance Overview as coarse aggregation, but this version's
  CLI exposes `perFrameMetrics` and `shaderCompilationMetrics`. Inspect the chosen configuration
  before interpreting resolution.
- Xcode 27 release notes mention export time-range options that this RC's `help export` does
  not list. The helper does not invent those flags. Actual installed help and successful
  execution take precedence over an assumed command shape.
- A template may include additional context tracks and hardware requirements. A CLI options
  query returning `{}` means no exposed configurable options, not that the instrument is empty
  or fully supported on the chosen device.
- HTTP and Foundation Models captures can contain unencrypted sensitive data. Use approved
  test data, private storage and the skill's cleanup/retention rules.

## Reuse and refresh

The [Metal workflow](metal.md) and [regression workflow](regression-testing.md) were added on
2026-11-14 using current Apple documentation linked alongside the guidance. Selected sections
reviewed include [Metal profiling modes](https://developer.apple.com/documentation/xcode/optimizing-gpu-performance),
[per-pass counters](https://developer.apple.com/documentation/xcode/analyzing-apple-gpu-performance-using-counter-statistics),
[agent trace investigation](https://developer.apple.com/documentation/xcode/investigating-gpu-issues-with-ai-agents),
[performance-test setup and baselines](https://developer.apple.com/documentation/xcode/writing-and-running-performance-tests)
and [measurement options](https://developer.apple.com/documentation/xctest/xctmeasureoptions).

Local `gpudebug` v1.0 help/manual and `xcresulttool get test-results metrics` help/schema were
inspected. The latter returned schema 0.4.0; the former's manual documents `-c` commands omitted
from short help. No product GPU capture/replay or device benchmark was run for this prose update.
`perf-apple-production` owns MetricKit/provider analysis separately; it is optional for local
profiling and does not add another native Instruments template.

The workflow prose and capture helper are original local work. The existing Axiom attribution
remains in [NOTICE](../NOTICE.md); no third-party profiler runtime was installed. Community
skill comparisons and the wider WWDC catalog live in the owning repository research record,
not as another dependency of this portable skill.

Refresh when Xcode/target OS/hardware changes. Compare the new CLI inventory against recipe
`covers`, investigate additions/removals, update source/version notes, query each changed
instrument's options, and run a representative capture. Keep unsupported-device and missing
export cases explicit; do not present documentation coverage as measurement coverage.
