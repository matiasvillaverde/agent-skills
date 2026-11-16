# Native profiling by mechanism

Rust, Zig, C and C++ binaries use many of the same OS/hardware profilers. Language and
allocator details determine how to build, symbolize and interpret them. Select a row for a
measured question; collecting every instrument at once adds overhead and obscures causality.
For Linux execution, use the [Linux workflow](linux.md): x86-64/ARM64, ELF symbols, containers,
quotas, NUMA, memory/I/O diagnosis and fallbacks when PMU sampling is unavailable.

## Match the observation to the question

| Question | macOS | Linux / other native targets | What establishes the finding |
| --- | --- | --- | --- |
| Where is CPU time spent? | Instruments Time Profiler / CPU Profiler; samply when available | `perf record` / report; samply; Windows WPR/WPA or supported vendor profiler | Symbolized stacks for the correct binary, absolute CPU and wall time, sufficient samples. A wide flamegraph frame is aggregate cost, not necessarily one slow call. |
| Why does a CPU hotspot stall? | CPU Counters, supported Processor Trace; match chip/instrument availability | `perf stat`, supported precise sampling, VTune or AMD uProf on supported hardware | Cycles/instructions and appropriate frontend, branch, cache/TLB or backend events, matched to the processor's definitions. |
| Is it waiting or ready but unscheduled? | System Trace, Thread Activity; samply's supported off-CPU sampling | Scheduler/futex/I/O tracing, targeted eBPF or perf sched with existing permissions | Distinguish blocked, runnable and running; identify wakeup/lock owner, queue delay and starvation. CPU-only samples cannot explain all wall time. |
| Allocation churn, retention or a leak? | Allocations, Leaks, VM Tracker / vmmap with allocator visibility checked | heaptrack, allocator-native statistics, DHAT / Massif where supported | Allocation count/bytes per operation, peak and live bytes, owners and release after repeated lifecycles. Retained arena capacity and RSS alone are not leaks. |
| Slow files or networking? | File Activity, System Call Trace, Network; framework-specific tracks only where actually emitted | Scoped syscall, filesystem/block or socket tracing; operation spans | Requests/syscalls, bytes, queueing, cache/page faults, fsync and final completion. Fewer calls may increase latency or weaken durability. |
| Contention or multicore scaling? | Thread states and counters; operation/task spans | Scheduler evidence, lock profiles, supported `perf c2c` / vendor memory analysis | Throughput and tail latency over relevant concurrency, waiting/runnable time, cache-line contention, NUMA locality where applicable. |
| Realtime audio, frames or GPU work? | Signposts/Tracy zones, deadline traces, Metal tools | Tracy and supported graphics/compute profilers | Deadline distribution, CPU submission vs GPU completion and synchronization. CPU speed alone does not prove reduced GPU work. |
| Did generated code change? | Matching disassembler, DWARF/dSYM and compiler output | Same, plus supported compiler remarks / llvm-mca | Identify actual hot machine code, inlining, dispatch, vectorization and copies. Assembly appearance is not an end-to-end benchmark. |

SwiftUI/Swift Actors, Core Data and other framework-specific tracks do not automatically expose
Rust or Zig internals. They can apply to a mixed-language host that actually uses those frameworks.
Allocator interposition can miss custom allocators, direct mappings or arena suballocations;
state the observation boundary and combine allocator-level accounting when needed.

## Record a bounded profile

Discover the selected Xcode, targets and installed capabilities first:

```sh
xcrun xctrace version
xcrun xctrace list templates
xcrun xctrace list instruments
xcrun xctrace help record
xcrun xctrace help export
```

For a task-owned optimized binary with matching symbols, a discovered template can be used as:

```sh
xcrun xctrace record --template 'Time Profiler' --time-limit 10s \
  --output '<private-task-directory>/cpu.trace' --launch -- '<absolute-binary>' <args>
xcrun xctrace export --input '<private-task-directory>/cpu.trace' --toc
```

Use `--attach <pid>` for a selected running process. Match exported schema/XPath to the actual
table of contents; parse XML references, not grep counts. Confirm samples contain the intended
work and resolved symbols. A trace bundle, empty table or successful export alone proves little.
See the available `perf-apple` capture guidance for deeper Instruments workflows.

On an already permitted Linux target, discover `perf version`, `perf list` and command help.
Illustrative forms below require supported events and a bounded command/workload:

```sh
perf stat -r 5 -e cycles,instructions,branches,branch-misses -- '<binary>' <args>
perf record -F 99 --call-graph dwarf -o '<private-task-directory>/perf.data' -- '<binary>' <args>
perf report --stdio -i '<private-task-directory>/perf.data'
```

Choose DWARF or frame-pointer unwinding based on the actual binary and perf build. DWARF can
increase capture size; missing/truncated stacks and lost samples must remain visible. Limit
scope to the owned process. Permission refusal, unavailable PMU or virtualized counters is a gap,
not permission to lower `perf_event_paranoid`, grant capabilities, disable SIP or collect the
whole host. Read kernel guidance and use the infrastructure owner's process for access changes.

`samply record <binary> <args>` is a useful native CPU route where already installed. Check its
current help for bounded/headless recording and file placement. At reviewed revision
`dea56099`, macOS/Windows collect on- and off-CPU samples; Linux collects on-CPU samples only.
Keep profiles/symbol servers local and do not upload proprietary source/captures by default.
Signed protected macOS executables can prevent launch/attach. Do not rewrite global Cargo
configuration or re-sign an unrelated executable just to work around that restriction.

## Interpret hardware evidence

Use the target's event definitions. Generic `cache-misses` is not a portable L1D-miss counter;
raw encodings, precise-sampling support and units differ by CPU. Capture fewer compatible
events, inspect running/enabled time and multiplexing, and group events for ratios when the
hardware can schedule them together. `<not supported>` and `<not counted>` are not zero.
Instruction/cycle ratios on unlike cores or differently scaled intervals are not comparable.

Separate total work from efficiency per unit of work. More IPC, fewer instructions or a lower
miss percentage can coexist with worse latency. Distinguish dependent-load latency from memory
bandwidth saturation, frontend/code-size pressure from data-cache pressure, and false sharing
from true shared-data contention. Validate the causal hypothesis with a bounded change, not
padding every structure or adding prefetches from a single counter.

Read the relevant hardware chapter and public library/compiler API before changing the mechanism.
Record chip family, core topology, architecture features, power/thermal state and applicable
limits. Follow public implementation source or disassembly when needed; separate documented
contracts, measurements and inference. No private API dependency or universal instruction-cost
constant follows from a reverse-engineered experiment.

- Apple Silicon: use the installed `perf-apple` skill's `references/sources.md` for the provisioned CPU guide location and terms, or the [public overview](https://developer.apple.com/documentation/apple-silicon/cpu-optimization-guide) when unavailable. The same CPU rules apply to Rust and Zig machine code; match the chip family.
- Intel: [optimization manuals and current processor supplements](https://www.intel.com/content/www/us/en/developer/articles/technical/intel64-and-ia32-architectures-optimization.html).
- AMD: [uProf documentation and supported systems](https://www.amd.com/en/developer/uprof.html); use the target processor's programming reference for event meanings.
- Arm servers: [Neoverse performance analysis](https://learn.arm.com/learning-paths/servers-and-cloud-computing/profiling-for-neoverse/performance-analysis-concepts/). Do not transplant Neoverse event formulas to Apple cores.

## Benchmarks and instrumentation

Use a representative operation and explicit correctness oracle. Separate setup, allocation,
input generation and teardown only when they are outside that operation. Keep results observable
and vary inputs; inspect optimized code if constant folding or dead-code removal is plausible.
Use interleaved/paired baseline and candidate runs when drift matters. Retain variance and
per-workload regressions; a favorable aggregate does not excuse a critical slow case. Define
cache state, concurrency and completion semantics. Avoid unbounded load or global cache flushes.

Cachegrind/Callgrind instruction counts and optional cache/branch simulations can stabilize
relative experiments on supported systems. They are not measured modern-cache, elapsed-time
or hardware energy results. llvm-mca uses a CPU scheduling model and lacks a real cache hierarchy;
use it to generate a hypothesis about a hot loop, then measure on the target.

Existing Tracy zones, signposts or tracing spans can expose cross-thread work and waits. Keep
instrumentation sparse, correlate operation identity, check client/viewer/binding versions, and
measure its overhead separately. A generated flamegraph with hardcoded stacks is not sampling.
Tracy's current source has Apple arm64 sampling, but source availability does not establish that
the installed binding/release supports it or that permissions permit it. Do not run a process
as root solely to activate the sampler.

Accept a change only with preserved output/UI/quality, ordering, cancellation, durability and
safety plus a gain beyond noise and acceptable resource tradeoffs. Retest the shipping build
without heavy diagnostics. Retain compact measurements, commands and unresolved-failure evidence;
remove only task-owned traces, binaries, temporary instrumentation and caches. Preserve shared
build caches, installed reference PDFs and unrelated processes.

## Source scope

Reviewed 2026-11-15: installed Xcode 27 command help and template inventory; selected Linux
[`perf stat`](https://github.com/torvalds/linux/blob/23c62304dde29abe92013d85910d03a77dada35d/tools/perf/Documentation/perf-stat.txt),
[`record`](https://github.com/torvalds/linux/blob/23c62304dde29abe92013d85910d03a77dada35d/tools/perf/Documentation/perf-record.txt)
and [`list`](https://github.com/torvalds/linux/blob/23c62304dde29abe92013d85910d03a77dada35d/tools/perf/Documentation/perf-list.txt)
sections; [kernel access guidance](https://www.kernel.org/doc/html/latest/admin-guide/perf-security.html);
full [samply README](https://github.com/mstange/samply/blob/dea56099bba34dfc5da4a8c9365d90b6eabffac7/README.md);
[LLVM MCA model and limitations](https://llvm.org/docs/CommandGuide/llvm-mca.html);
[Cachegrind overview and simulation limits](https://valgrind.org/docs/manual/cg-manual.html);
[Microsoft WPR/WPA overview](https://learn.microsoft.com/en-us/windows-hardware/test/wpt/);
Tracy [README](https://github.com/wolfpld/tracy/blob/aa5240ca19dd4978784b76f769f067cdda647615/README.md)
and selected [Apple sampler source](https://github.com/wolfpld/tracy/blob/aa5240ca19dd4978784b76f769f067cdda647615/public/client/apple/TracyMach.cpp).
Hardware links are entrypoints, not claims that entire manuals have been reviewed. These are
tool-selection recipes, not a declaration that every tool/platform has been executed locally.

Community measurement/SIMD ideas were compared with
[Mnwa's focused references](https://github.com/Mnwa/performance-engineering/tree/1f8c23164f35c4c5868e765753904202ac4fe834/skills/performance-engineering/references)
and [madebyhost's native guidance](https://github.com/madebyhost/rust-performance-skills/tree/2afcbcc2296a658d88cd0816d221679ad84d2170/skills).
No fixed numerical gates, mandatory templates or upstream code/prose were imported.
