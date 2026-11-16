---
name: perf-zig
description: Diagnose and improve low-level Zig CPU, allocator, memory-layout, SIMD, concurrency and I/O performance with version-matched builds and native profiling. Use for Zig libraries, services and native programs.
---

# Zig performance

Optimize a measured operation while preserving its behavior, UI/output quality, error handling,
safety, ordering, cancellation and durability. Work from the repository's compiler and deployment
contract on Linux (x86-64 and ARM64) and macOS; this skill does not migrate Zig versions or
impose a particular coding style. Select tools for the execution host, and measure on the Linux
deployment target when that is where the program runs; Apple Silicon timings cannot qualify it.

## Establish what is being measured

Inspect owning instructions, compiler pin, build files and existing benchmarks. Record `zig version`
and `zig env`, target/CPU features, optimization/safety mode, backend, linker, allocator and artifact
identity. Build-script `-D` options are project-defined: discover help and source instead of assuming
every repository accepts `-Doptimize`, `-Dstrip`, `-Dcpu` or profiling flags.

Read [compiler and profiling setup](references/compiler-and-profiling.md) for version-dependent
mode names, symbols, backend choices and emitted code. Use matching standard-library/compiler
source when documentation disagrees with the installed release. Keep compilation speed, runtime
speed and incremental/cache behavior as separate questions.

Define a representative operation, input distribution/size, concurrency, cold/warm state and
bounded measurement budget. Use existing acceptance budgets or establish a baseline with an
explicit proposed target. Preserve all required work; a faster unsafe build, lost output or
changed floating-point result is not an accepted optimization.

## Choose evidence by mechanism

| Concern | Useful evidence |
| --- | --- |
| CPU hotspot, cache/TLB, branches or bandwidth | Symbolized native samples, then target-supported PMU events; Instruments on macOS or perf on Linux, with compatible alternatives where installed. |
| Allocation, arena growth or leak | Requests and backing allocations separately, peak/live bytes, reset/deinit ownership and repeated workload retention. |
| SIMD/layout/codegen | Actual size/alignment/stride, hot access pattern, scalar oracle, emitted machine code and realistic input/tail cases. |
| Threads, locks, I/O or deadlines | Running/runnable/blocked states, queue/completion timing, syscalls/bytes, retries and operation correlation. |

The shared library's [native profiling guide](../perf-system/references/native.md) adds OS
recipes, counter interpretation and hardware documentation. If unavailable, use the official
tool references linked in this skill. For Linux, read its [Linux workflow](../perf-system/references/linux.md)
for ELF symbols, containers/VMs, scheduling, NUMA and restricted-counter fallbacks.
Native profilers are language-independent; framework tracks
only apply when the program actually uses that framework. Keep captures scoped to the owned
binary/host and report unsupported tools, PMUs, symbols or permissions. Do not install a profiler,
change host security, add a benchmark dependency or select a new allocator just to avoid a gap.

## Follow the cost into the mechanism

Read [memory, kernels and I/O](references/memory-and-kernels.md) when the profile points there.
Inspect relevant public APIs, their exact-version implementation and generated code before
choosing a fix. Separate documented guarantees, observed results and hypotheses. Check profiler
metric provenance: rendered charts or folded stacks are not evidence that sampling occurred.

Prefer removing repeated work, copies, allocation, parsing and synchronization. Buffering,
batching, arenas, SoA, prefetching and vectorization are workload-specific hypotheses. Account for
conversion cost, retained capacity, maximum wait-to-fill, ownership and end-to-end latency.
Do not treat `comptime`, `inline`, `packed`, more threads or wider vectors as automatic wins.

For collection or algorithm alternatives, the shared [data-structure review](../perf-system/references/algorithms-and-data-structures.md)
adds workload candidates when available. Verify selected-version source, allocator ownership,
removal order and pointer invalidation; field-separated storage must earn its conversion cost.

Preserve scalar/reference behavior and validate changed invariants: tails, bounds, alignment,
aliasing, initialized range, overflow, FP/NaN rules, ownership, thread safety and CPU fallback.
Do not hide illegal behavior with `@setRuntimeSafety(false)`, turn recoverable errors into
`unreachable`, or weaken atomics to win a timing. Safety-enabled builds help diagnosis but cannot
prove every illegal behavior absent. Select focused checks for the mechanism and keep required gates.

## Compare, accept and clean up

Build outside timing. Compare equivalent shipping modes/allocators/backends and representative
workloads; make diagnostic differences explicit. Use existing benchmark machinery, runtime-like
inputs and observable outputs. Check timer resolution, batching, hooks, cleanup and compiler
elimination when results are tiny or surprising. Sample counts and microbenchmark percentiles do
not establish service tail latency. Pair/interleave runs when drift matters and retain variability.

Retest a candidate in the real operation without heavy diagnostics. Keep only a gain beyond noise
that earns its complexity and preserves behavior/resource budgets. Report build/workload identity,
commands, values/units/sample counts, correctness evidence, tradeoffs and gaps; classify accepted,
regressed, inconclusive or not verified. A source-verified command is not a runtime-tested command.

Save compact findings and reproduction details. Stop owned profilers/helpers, remove temporary
instrumentation, traces, exports, scratch binaries and isolated Zig cache/output directories,
and restore task settings even on failure. Preserve shared/global caches, existing build outputs,
reference PDFs and necessary unresolved-failure evidence. Verify cleanup and report leftovers.
[Sources and scope](references/sources.md).
