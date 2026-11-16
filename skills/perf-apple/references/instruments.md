# Apple instrument catalog and workflows

Verified against `xctrace 27.0 (27A266a)` on 2026-11-14: **63 standard instruments**.
This is a bounded inventory for that installation, not a promise about every Xcode,
OS, simulator or device. Run `xcrun xctrace list instruments` on the actual host.
An available name, accepted configuration, populated track and successful measurement
are four different checks. Empty data is not a passing result.

Choose the relevant section only. The paired [capture recipes](../assets/capture-recipes.json)
use standard templates, with optional instruments for specific follow-up questions.
[CLI and native-template instructions](capture.md) explain execution, export and cleanup.
Read the common measurement and cleanup rules in [the skill](../SKILL.md) first.
Use [acceptance criteria](acceptance.md) for the selected mode before changing code;
[API and hardware investigation](investigation.md) explains how to research an unresolved cause
without changing product behavior or mistaking undocumented observations for supported APIs.

All rows include the exact installed name, how to use it, and a limitation. **Local**
references mean Apple's documentation shipped in the selected Instruments app, not
a public webpage. See [source locations and review limits](sources.md). Recommendations
about workload selection and verification are our synthesis of these sources.

## CPU — computation and hardware efficiency

Recipe: `cpu`, based on **Time Profiler**. Begin with a bounded, symbolicated sample of
the slow operation. Select its time range and compare self/inclusive work, absolute
duration and total work. Use CPU Profiler, CPU Counters or Processor Trace as separate
focused follow-ups; do not turn every CPU facility on by default. Capture a repeatable
test case before changing algorithms, layout, allocation or dispatch.

| Instrument | How to use and interpret it | Limitation / documentation |
| --- | --- | --- |
| Activity Monitor | Record the operation and idle recovery; compare process CPU, memory, thread and I/O trends. Use spikes to choose a more specific profiler. | Process totals do not identify the responsible stack. Local `ActivityMonitor` schemas define the counters. |
| Time Profiler | Select the operation interval; inspect Call Tree, Top Functions and flame graph, then the expensive symbol's callers and source. Compare sampled weight and elapsed time. | Statistical CPU evidence can miss brief calls and blocked time. Local `Sampling`; [CPU views](https://developer.apple.com/documentation/xcode/analyzing-cpu-profiles-with-call-tree-views). |
| Sampler | Add it for user-space process stack sampling, reproduce the suspected hot path, and inspect recurring stacks in the selected interval. | It is not hardware branch tracing or proof of every call. Dedicated current public guidance is sparse; use the local Library description and actual recorded tables. Prefer Time Profiler for ordinary CPU diagnosis. |
| CPU Profiler | Use its standard template on supported hardware; rank stacks by cycle weight and compare equivalent workloads. | Cycles are not seconds, especially across cores or frequency changes. Local `CPU Profiler` explicitly defines cycle-weight samples; [WWDC25 CPU](https://developer.apple.com/videos/play/wwdc2025/308/). |
| CPU Counters | Start with the guided CPU Bottlenecks mode; select the costly interval and use its remarks/Suggested Next to choose a targeted counter collection. | Counter sets and availability depend on the CPU. Do not optimize a ratio while slowing the operation. [CPU bottlenecks](https://developer.apple.com/documentation/xcode/addressing-cpu-bottlenecks). |
| Processor Trace | Capture a short selected operation; inspect time-ordered calls, call counts, instructions, cycles and IPC. Use it to find tiny frequent calls that sampling misses. | Recording requires supported hardware: Apple currently lists iPhone 16+, M4+ iPad Pro/Mac and minimum OS versions; analysis can run elsewhere. Keep trace volume bounded. [Processor Trace](https://developer.apple.com/documentation/xcode/analyzing-cpu-usage-with-processor-trace). |

## Scheduling — hangs, waits and resource contention

Recipe: `scheduling`, based on **System Trace**. Start from an interaction or signposted
operation, then ask whether its critical thread was running, runnable, blocked or asleep.
Follow the dependency that delayed it. System-wide context can appear even when selecting
one process; do not expand the target scope merely to get more data. Confirm a proposed
fix reduces end-to-end delay rather than just moving the wait elsewhere.

| Instrument | How to use and interpret it | Limitation / documentation |
| --- | --- | --- |
| Hangs | Reproduce the stalled interaction; select a marked interval and inspect the main thread with Time Profiler and scheduling evidence. Choose a reporting threshold appropriate to the interaction. | Detection thresholds classify observations, not product acceptance budgets. Priority-inversion detection injects diagnostics and changes conditions. [Hang tutorial](https://developer.apple.com/tutorials/instruments/getting-started-with-hang-analysis); local `Hangs`. |
| Thread Activity | Inspect thread states, priority/QoS, syscalls and faults around the delay; correlate runnable time with competing work and blocked time with dependencies. | A waiting worker may be healthy; prove it lies on the critical path. Older guides call a related track Thread State Trace. Local `SystemTrace`; [System Trace in depth](https://developer.apple.com/videos/play/wwdc2016/411/). |
| System Call Trace | Filter the selected thread/interval; inspect repeated or long calls and their callers, then correlate with I/O or synchronization. | A long call is elapsed wait as well as execution; duration alone is not CPU cost. Local `SystemTrace`. |
| Virtual Memory Trace | Examine faults and VM activity per thread while reproducing stalls, allocation bursts or first-use behavior; correlate with scheduling and file access. | This records activity; use VM Tracker for region/footprint snapshots. Local `SystemTrace`; [Metal memory](https://developer.apple.com/documentation/xcode/analyzing-the-memory-usage-of-your-metal-app). |
| Run Loops | Expand the main thread's iterations, busy/wait intervals and nested runs. Align unusually long iterations with the affected event or frame. | Attach-late boundaries can be estimated, not recorded; local `RunloopInstrument` documents timestamp accuracy. A nested loop alone is not a bug. |
| System Load | Record alongside the symptom to see whether unrelated load or resource contention explains run-to-run variation. | Context, not attribution to your app. Local `SystemTrace`/Library; [Audio analysis](https://developer.apple.com/documentation/audiotoolbox/analyzing-audio-performance-with-instruments). |

## Concurrency — tasks, actors, executors and GCD

Recipe: `concurrency`, based on **Swift Concurrency**. Reproduce the real task fan-out,
cancellation and contention. Compare creation, queued, running and suspended work.
Distinguish useful parallelism from excessive tasks or blocking on the cooperative pool.
After a change, verify isolation, cancellation, ordering and bounded resource use as well
as speed. Read the project's Swift language mode and isolation settings before recommending
an executor change. [Apple's workflow](https://developer.apple.com/videos/play/wwdc2022/110350/).

| Instrument | How to use and interpret it | Limitation / documentation |
| --- | --- | --- |
| Swift Tasks | Follow a slow task's lifetime, parent/child work and suspension points; inspect task-creation stacks when task counts explode. | Task duration includes waiting. In Xcode 27, attach-late tasks may have Unknown state; incomplete history stays incomplete. [Xcode 27 notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-27-release-notes). |
| Swift Actors | Inspect work queued for a busy actor and the tasks executing on it; identify expensive isolated work or unnecessary serialization. | Serialization may protect required state. Do not remove actor isolation simply to reduce a queue. [Swift concurrency](https://developer.apple.com/videos/play/wwdc2022/110350/). |
| Swift Executors | Compare Main Actor, custom-executor and pool activity to locate saturation, blocking and costly executor transitions. | An executor is not a permanently assigned OS thread. Correlate with Thread Activity when scheduler behavior matters. [Swift concurrency](https://developer.apple.com/videos/play/wwdc2022/110350/). |
| GCD Performance | Add to a dispatch-heavy reproduction; inspect the reported event, queue/source, severity and backtrace before changing queue topology or synchronization. | Diagnostic events are evidence of particular API patterns, not a complete concurrency correctness audit. Local `Dispatch`; [Modernizing GCD](https://developer.apple.com/videos/play/wwdc2017/706/). |

## Memory — allocation, leaks and footprint

Recipe: `memory`, based on **Allocations**; use Leaks as a targeted addition. Repeat the
same open/use/close or start/stop cycle, allowing expected asynchronous teardown. Compare
generations and retained growth, then inspect owners with Memory Graph when appropriate.
Keep allocation churn, reachable retention, unreachable leaks, VM reservations and charged
footprint separate. [Heap workflow](https://developer.apple.com/videos/play/wwdc2024/10173/).

| Instrument | How to use and interpret it | Limitation / documentation |
| --- | --- | --- |
| Allocations | Mark generations around repeated lifecycles; inspect surviving objects and allocation/free stacks. Enable reference-count history only when needed for ownership diagnosis. | Extra stack/refcount recording adds overhead; allocator caches and private Metal resources complicate interpretation. Local recording options; [heap analysis](https://developer.apple.com/videos/play/wwdc2024/10173/). |
| Leaks | Take checks after the operation and after teardown; inspect leaked allocation stacks and cycles with Allocations/Memory Graph. | No reported leak does not exclude reachable abandoned objects or other growth. A short trace is insufficient. [Heap analysis](https://developer.apple.com/videos/play/wwdc2024/10173/). |
| VM Tracker | Enable snapshots and compare region tags, resident, dirty and compressed/swapped sizes before/after a lifecycle. Use this when heap totals cannot explain footprint. | Virtual address space, RSS and memory footprint are different quantities. The system can charge compressed memory at its original size. [Metal memory](https://developer.apple.com/documentation/xcode/analyzing-the-memory-usage-of-your-metal-app). |

## Launch — dynamic loading and first usable content

Recipe: `launch`, based on **App Launch**. Launch under recording; attaching after launch
cannot establish pre-main cost. Specify first run, cold/warm conditions, prewarming and
the user-visible endpoint. Pair initialization with application signposts so that delaying
work does not merely move the same stall to the first tap. [App launch](https://developer.apple.com/videos/play/wwdc2019/423/).

| Instrument | How to use and interpret it | Limitation / documentation |
| --- | --- | --- |
| dyld Activity | Inspect image loads, `dlopen`/`dlclose` and static initializer intervals; follow the recorded library/symbol/backtrace to expensive startup dependencies. | dyld duration is only part of launch. The local `dyld` schema includes library and nesting information; the instrument replaced Static Initializer in [Xcode 15](https://developer.apple.com/documentation/xcode-release-notes/xcode-15-release-notes). |

## Scrolling — frames and the Core Animation pipeline

Recipe: `scroll`, based on **Animation Hitches**. Use a repeatable gesture, data set,
image-cache state, screen size and refresh-rate condition. Locate bad frames and determine
whether the app commit, render server or GPU missed the deadline. Compare hitch time/rate
and user-visible completion, not just average FPS. Use XCUITest to replay the scenario.
[Render-loop explanation](https://developer.apple.com/videos/play/tech-talks/10855/).

| Instrument | How to use and interpret it | Limitation / documentation |
| --- | --- | --- |
| Hitches | Record the scrolling/animation scenario; select hitch intervals and inspect their phase and duration alongside CPU/GPU evidence. | Not the same as Hangs. Refresh rate and pipeline stage affect the budget; do not impose a universal 16.67 ms rule. [Hitch measurement](https://developer.apple.com/videos/play/wwdc2020/10077/). |
| Core Animation Activity | Expand context/layer phases for a bad frame; locate expensive client-side layout/display activity and correlate it with app stacks. | Layer count alone does not identify a regression. Local `CoreAnimation` context/layer schemas. |
| Core Animation Commits | Inspect long or numerous commit intervals and their initiating stacks; distinguish large updates from repeated small transactions. | A fast commit does not establish fast server rendering. Local `CoreAnimation`; [commit hitches](https://developer.apple.com/videos/play/tech-talks/10856/). |
| Core Animation Server | Inspect server render intervals and correlate display/swap identifiers with delayed surfaces and app commits. | Server work can serve several clients; avoid assigning every server spike to the target. Local `CoreAnimation`; [render hitches](https://developer.apple.com/videos/play/tech-talks/10857/). |
| Core Animation FPS | Use its estimated FPS graph to locate broad pacing changes, then investigate individual frame/hitch evidence. | Explicitly an estimate based on available driver statistics; average FPS hides isolated stalls. Local `IOKit`. |
| Frame Lifetimes | Follow a frame across client commit, server rendering and presentation; inspect hitch, event-latency and render intervals for the selected frame. | Overlapping pipeline stages are not durations to blindly sum; attach-late or dropped events can leave incomplete lifetimes. Local `CoreAnimation` frame-lifetime schema. |

## SwiftUI — update causes and layout

Recipe: `swiftui`, based on **SwiftUI**. Identify whether the problem is expensive updates,
too many updates, or downstream rendering. Select the relevant update group and use the
cause graph/view hierarchy to find the source. Reduce the specific dependency fan-out or
measured body/layout work. Stable identity and predictable row geometry matter during
scrolling; use the scroll workflow to verify that improvement reaches the screen.

| Instrument | How to use and interpret it | Limitation / documentation |
| --- | --- | --- |
| SwiftUI | Inspect update groups, long body/platform updates and cause/effect. Xcode 27 exposes layout tracing as an opt-in recording option; use it for measured layout issues. | A body call is not automatically a rendered frame or wasted work. Use deployment-appropriate data. [SwiftUI analysis](https://developer.apple.com/documentation/xcode/understanding-and-improving-swiftui-performance); [Xcode 27](https://developer.apple.com/documentation/xcode-release-notes/xcode-27-release-notes). |
| View Body (Legacy) | For older target OS versions, add this instrument and compare body invocation frequency/duration by view type during the same interaction. | Retained for older SwiftUI tracing; do not expect the modern cause graph or substitute invocation count for frame quality. Local `SwiftUI`. |
| View Properties (Legacy) | Record changes to dynamic properties and correlate them with body updates to investigate unexpectedly broad invalidation on older OS versions. | Recorded values can be sensitive; tracing capabilities differ from the modern instrument. Local `SwiftUI` property schemas. |

## I/O — files, descriptors and storage

Recipe: `io`, based on **File Activity**. Reproduce the selected save/load/import path with
documented cache state. Correlate logical operations, physical I/O and user-visible delay.
Inspect descriptor lifetimes for repeated open/close cycles, exhaustion or missing cleanup.
Reduce redundant work or batch where semantics permit; preserve durability, atomicity and
crash recovery. [Storage workflow](https://developer.apple.com/videos/play/wwdc2019/419/).

| Instrument | How to use and interpret it | Limitation / documentation |
| --- | --- | --- |
| Filesystem Activity | Inspect read/write/open/close/mapping events, size, duration and backtrace; trace repeat access and descriptor ownership to code. | Logical reads/writes can be served by caches; they are not physical device traffic. [Reducing disk writes](https://developer.apple.com/documentation/xcode/reducing-disk-writes). |
| Disk Usage | Examine physical read/write volume and timing during the same workload; look for write amplification and bursts that outlive the request. | Filesystem caching and block granularity prevent a one-to-one mapping to application byte counts. [Reducing disk writes](https://developer.apple.com/documentation/xcode/reducing-disk-writes). |
| Disk I/O Latency | Find long completion times and saturation bursts; correlate them with app requests, competing load and the critical thread. | Physical I/O completion is not the whole logical request duration. [Reducing disk writes](https://developer.apple.com/documentation/xcode/reducing-disk-writes). |
| Filesystem Suggestions | Select emitted suggestions, inspect the associated operation/backtrace and reproduce the pattern before changing it. | Advisory heuristics are not a complete file-system audit or permission to weaken persistence. [Storage workflow](https://developer.apple.com/videos/play/wwdc2019/419/). |

## Persistence — SwiftData and Core Data

Recipe: `persistence`, based on **Data Persistence**. Use realistic store size, relationships
and concurrency. Profile load, relationship traversal and save separately. Look for N+1
faults, repeated fetches and oversized transactions, then verify fetched results, ordering,
model-context confinement and persistence after restart. Local `DataPersistence` explicitly
covers **both SwiftData and Core Data**; older [Core Data performance guidance](https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/CoreData/Performance.html)
uses older instrument names and is not a current SwiftData API guide.

| Instrument | How to use and interpret it | Limitation / documentation |
| --- | --- | --- |
| Data Faults | Inspect object and relationship fault duration, thread and caller during traversal; investigate repeated expensive faults before choosing prefetch/batching. | A model fault is not a VM page fault or necessarily a disk read. Local `core-data-fault` and relationship-fault schemas. |
| Data Fetches | Compare fetch count, returned count/entity, duration and callers for one user operation; detect duplicated or overly broad requests. | Fewer fetches can increase memory/latency if each becomes too large. Local `core-data-fetch` schema. |
| Data Saves | Inspect save duration and caller/thread; correlate large or frequent saves with UI stalls and physical writes. | Reduced save frequency changes the durability window. Local `core-data-save` schema; verify the app's required semantics. |

## Networking — connections and HTTP transactions

Recipe: `network`, based on **Network**. Count tasks, transactions, connections and bytes
for one operation. Compare cold/reused connections, caches, cancellation and a bounded
offline/loss/slow-server test. Relate client phases to server traces when available;
geographic latency needs remote test locations, not just this Mac. Use synthetic or
approved test traffic: HTTP captures can contain decrypted headers and bodies.

| Instrument | How to use and interpret it | Limitation / documentation |
| --- | --- | --- |
| Network Connections | Expand connection/address/path tracks; inspect TCP/UDP activity, connection churn and transfer patterns around the slow request. | Connection-level data does not identify every app-level retry or server computation. [Network workflow](https://developer.apple.com/documentation/foundation/analyzing-http-traffic-with-instruments). |
| HTTP Traffic | Expand process/session/domain/task/transaction tracks; inspect cache lookup, blocked, sending, waiting and receiving phases. Name URLSession instances to distinguish their work. | URL Loading System coverage is not arbitrary socket coverage. Redirects can make one task several transactions; HTTPS data is stored decrypted. [HTTP analysis](https://developer.apple.com/documentation/foundation/analyzing-http-traffic-with-instruments). |

## Audio — callback deadlines and engine behavior

Recipe: `audio`, based on **Audio System Trace**. Reproduce the actual route, sample rate,
buffer size, interruption and workload. Select a glitch, align the three audio tracks with
thread states, and distinguish late scheduling from an over-budget render callback. Worst
case matters more than mean CPU use. For streaming startup/rebuffering also inspect
AVMetrics and the network workflow; those are different from a real-time DSP deadline.

| Instrument | How to use and interpret it | Limitation / documentation |
| --- | --- | --- |
| Audio Client | Inspect the app's I/O cycle/IOProc intervals and warnings at the glitch; compare work against the available cycle and correlate locks, allocations or waits. | A short callback can still start too late. Local `Audio` client schemas; [Audio analysis](https://developer.apple.com/documentation/audiotoolbox/analyzing-audio-performance-with-instruments). |
| Audio Server | Inspect engine I/O cycles, timestamp changes and system-side points of interest; locate timing problems outside the app callback. | Do not assign system-wide engine behavior wholly to one client. Local `Audio` server schemas; [Audio analysis](https://developer.apple.com/documentation/audiotoolbox/analyzing-audio-performance-with-instruments). |
| Audio Statistics | Expand Engine Jitter and I/O Threads; correlate jitter spikes and concurrent thread counts with the failing cycle. | Jitter is cadence variation, not average DSP utilization or perceptual audio quality. Local `Audio`; [audio workgroups](https://developer.apple.com/videos/play/wwdc2020/10224/). |

## GPU — submission, execution, resources and display

Recipe: `gpu`, based on **Metal System Trace**. Diagnose whether the app feeds the GPU too
late, the GPU is saturated, synchronization stalls overlap, or presentation misses deadlines.
Use a frame capture/Metal debugger for pass/shader detail and Game Memory for footprint.
Validate rendering and resource lifetimes separately from timing; expensive validation and
counter collection should not contaminate the final speed comparison.

| Instrument | How to use and interpret it | Limitation / documentation |
| --- | --- | --- |
| Metal Application | Follow CPU-side Metal work and command submission; align it with GPU execution to find starvation, expensive encoding or synchronization. | Submission duration is not GPU execution time. Local `GPU`; [Metal performance](https://developer.apple.com/documentation/xcode/analyzing-the-performance-of-your-metal-app). |
| GPU | Inspect device execution intervals and queue overlap; correlate idle gaps or saturation with app submissions and frame deadlines. | A busy GPU does not by itself identify the costly shader. Local `GPU`/`GPUBase`; [Metal performance](https://developer.apple.com/documentation/xcode/analyzing-the-performance-of-your-metal-app). |
| Metal GPU Counters | Select a supported counter set for the suspected limiter; compare the same pass/workload and use the GPU debugger for attribution. | Counters vary by GPU and collection mode; they are not all enabled by adding a track. Local `GPUCounters`; [GPU counters](https://developer.apple.com/videos/play/wwdc2020/10603/). |
| Metal Resource Events | Follow creation/destruction and labels of textures/buffers during repeated scene loads; compare lifetimes with GPU completion. | Not every listed resource survives the interval; allocations differ from charged footprint. [Metal memory](https://developer.apple.com/documentation/xcode/analyzing-the-memory-usage-of-your-metal-app). |
| Metal Performance Overview | Use for trends across sustained gameplay/work, then narrow to a representative bad interval for detailed capture. Inspect per-frame and shader-compilation options on the installed version. | Aggregation can hide individual hitches; current CLI options differ from older one-second descriptions. [WWDC26 Metal performance](https://developer.apple.com/videos/play/wwdc2026/388/) and local recording options. |
| Display | Select long presentation intervals and inspect skipped VSync/presentation events; correlate them with CPU and GPU work. | Requested frame rate, display rate and delivered frames differ. Local `GPU`; [Metal performance](https://developer.apple.com/documentation/xcode/analyzing-the-performance-of-your-metal-app). |
| Advanced Graphics Statistics | Choose the available driver counters relevant to the device; correlate trends with a known graphics workload. | Low-level meanings are driver/OS/hardware dependent; no stable cross-device counter contract. Local `IOKit` is the strongest located reference; validate counter meanings before relying on them. |

For deeper Metal replay, shader/counter interpretation and kernel optimization, use
[Metal investigation](metal.md) alongside the GPU workflow above.

## Spatial — RealityKit, SceneKit and foveated streaming

Recipe: `spatial`, based on **RealityKit Trace**, for visionOS. Select the affected frame,
follow app/render-server CPU and GPU stages, then isolate costly content, systems or
streaming phases. SceneKit on other Apple platforms should start from the GPU workflow
with SceneKit Application added; the visionOS template is not a requirement for SceneKit.
Real-device timings are essential; simulator traces can still explain code paths.

| Instrument | How to use and interpret it | Limitation / documentation |
| --- | --- | --- |
| RealityKit Frames | Follow frame lifespan and render stages; locate deadline misses and compare app/server CPU and GPU rates. | visionOS render-server data; a simulator cannot establish device timing. [visionOS performance](https://developer.apple.com/documentation/visionos/analyzing-the-performance-of-your-visionos-app); local `RealityKit`. |
| RealityKit Metrics | Inspect timing and bottleneck remarks for commits, animation, physics, spatial systems and content complexity; select the implicated subsystem for a focused fix. | Complexity and power indicators are not universal pass/fail thresholds. Local `RealityKit`; [WWDC23 RealityKit](https://developer.apple.com/videos/play/wwdc2023/10099/). |
| Foveated Streaming Statistics | Add to a visionOS client connected to an active endpoint; compare bandwidth/stream rate, receive/reprojection/pose rates and pose-to-frame latency stages. | Reprojection rate is not the rate of new rendered frames; healthy average bandwidth does not exclude jitter/loss. [Streaming analysis](https://developer.apple.com/documentation/foveatedstreaming/analyzing-the-performance-of-a-foveated-streaming-session). |
| SceneKit Application | Reproduce the SceneKit scene and inspect frame IDs, stages and event intervals; correlate the slow stage with Time Profiler or GPU evidence. | Local `SceneKit` documents events/frames, but detailed current public instrument guidance is sparse. Do not infer RealityKit metrics or API behavior from this older framework's track. |

## Energy — power, thermal state and location

Recipe: `energy`, based on **Power Profiler** on a supported iPhone/iPad. Reproduce a
sustained use/background cycle with matched brightness, radios, battery and thermal state.
Compare the same device model. Charging makes the reported overall power usage zero;
connected Xcode also changes sleep behavior. Use disconnected on-device recording for
sleep investigations. Mac availability of a template does not establish Power Profiler
recording support. [Power Profiler guide](https://developer.apple.com/documentation/xcode/measuring-your-app-s-power-use-with-power-profiler).

| Instrument | How to use and interpret it | Limitation / documentation |
| --- | --- | --- |
| Power Profiler | Target the app and compare CPU/GPU/display/network impact alongside system consumption; expand the highest contributor and capture its domain-specific work. | App impact is not battery percentage. All Processes omits app attribution; current docs scope the feature to iOS/iPadOS 26+. [Power guide](https://developer.apple.com/documentation/xcode/measuring-your-app-s-power-use-with-power-profiler). |
| Thermal State | Record state transitions during sustained work and correlate throughput/latency changes with them; compare runs started in equivalent states. | State is not a precise temperature measurement or proof that the app caused the pressure. Local `Thermal` distinguishes induced state. |
| Location Energy Model | Reproduce the authorized location use and background lifecycle; correlate modeled activity with requested accuracy, update frequency and service lifetime. | A model, not a direct joule meter. Target support and detailed current public guidance remain gaps; inspect actual tracks and Core Location configuration before conclusions. Library description; [energy principles](https://developer.apple.com/library/archive/documentation/Performance/Conceptual/EnergyGuide-iOS/LocationBestPractices.html). |

## Model execution — Core AI, Core ML and Neural Engine

Recipe: `ml`, based on **Core AI** for that framework. For existing Core ML workloads,
use Time Profiler plus Core ML and supported hardware tracks; migrating frameworks is not
a profiling prerequisite. Keep specialization/compilation, loading, setup and steady inference
separate. Compare real inputs/shapes, precision, memory, output quality and compute units.
Never delete shared downloaded model weights or specialization caches as routine cleanup.

| Instrument | How to use and interpret it | Limitation / documentation |
| --- | --- | --- |
| Core AI | Expand model/function tracks and compare Specialization, Load, Setup and Inference. Investigate repeated loads and first-use specialization before optimizing steady inference. | Xcode/OS/framework dependent. Compare on actual hardware with competing compute controlled. [Core AI profiling](https://developer.apple.com/documentation/coreai/analyzing-model-runtime-performance-with-instruments). |
| Core ML | Add it to a Core ML app's reproduction; inspect model/submodel event intervals and correlate prediction cost with CPU/GPU/Neural Engine activity. | Framework intervals do not guarantee every operation ran on the preferred compute unit. Local `CoreML`; [Core ML performance](https://developer.apple.com/videos/play/wwdc2023/10049/). |
| Neural Engine | Inspect hardware activity intervals alongside model events to locate execution and gaps. Compare supported-device traces for the same input. | ANE activity alone is not complete model latency, correctness or exclusive app attribution. Local `Neural Engine`; [Core AI profiling](https://developer.apple.com/documentation/coreai/analyzing-model-runtime-performance-with-instruments). |

## Foundation Models — requests, tools and tokens

Recipe: `foundation-models`, based on **Foundation Models**. Use synthetic prompts and a
repeatable task. Compare cold loading, time to first token, generation, tool latency and
total request completion. Keep model/provider and request quality comparable when reducing
context or outputs. Prompt/response traces contain unencrypted content; keep them private
and remove task-owned captures after retaining sanitized findings.

| Instrument | How to use and interpret it | Limitation / documentation |
| --- | --- | --- |
| Foundation Models | Expand session/request/inference/tool/loading tracks; inspect total, consumed, generated and cached tokens, first-token latency and tool outputs. Separate model work from slow tools. | Provider capabilities and caching differ; fewer tokens do not prove equivalent quality. It covers this framework, not every arbitrary LLM client. [Runtime analysis](https://developer.apple.com/documentation/foundationmodels/analyzing-the-runtime-performance-of-your-foundation-models-app). |

## Logging — operation context and signposts

Recipe: `logging`, based on **Logging**. Add a small number of semantic intervals around
the operation's boundaries, with distinct IDs for overlapping instances. Use `OSSignposter`
where supported and stable subsystem/category names. Balance ends on success, failure and
cancellation; avoid logging on real-time callbacks or emitting a span per tiny inner-loop
iteration. A custom instrument/modeler is justified only when repeated analysis needs it.

| Instrument | How to use and interpret it | Limitation / documentation |
| --- | --- | --- |
| Points of Interest | Align app/system signposted events and intervals with resource tracks. Xcode 27 also displays StateReporting domains/transitions here. | It supplies context; not every signpost category automatically appears in this lane. [Xcode 27 notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-27-release-notes); [signposts](https://developer.apple.com/documentation/os/recording-performance-data). |
| os_signpost | Inspect interval/event rows by subsystem/category/name; correlate unique interval IDs with slow operations and compare duration distributions. | The instrument name remains valid even when new Swift code uses OSSignposter. Missing begin/end events produce incomplete intervals. [Recording performance data](https://developer.apple.com/documentation/os/recording-performance-data). |
| os_log | Filter subsystem/category/level to explain events around a failure; enable only the detail required for the investigation and check privacy formatting. | High-volume logging perturbs timing and may omit private data or filtered levels. Absence is not proof of absence of an event. [Structured logging](https://developer.apple.com/videos/play/wwdc2023/10226/). |
| stdout/stderr | Use a launch recording to correlate the launched process's textual output with the trace; capture concise diagnostic errors when unified logging is unavailable. | Buffered output timing can lag the event; attach cannot recover historical output. Library description and `xctrace help record` stream-redirection options. |

## Coverage boundaries

Every one of the 63 discovered names has an owning workflow above. This does **not** mean
all instruments were recorded, exported or validated against a real product. Some tracks
require framework activity, target OS support, hardware counters, symbols or additional
recording options. Discover actual export schemas with `xctrace export --toc`; never promise
an XML table solely from the instrument name. Apple framework fields and internal package
schemas are evidence for this version, not a stable parser API.

Non-instrument complements include Xcode Memory Graph, MetricKit/Organizer, AVMetrics,
Metal validation/frame debugging, XCTest performance metrics, XCUITest and RocketSim.
They remain useful even though they are not separate entries in `xctrace list instruments`.
