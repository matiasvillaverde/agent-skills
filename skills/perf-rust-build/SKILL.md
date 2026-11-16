---
name: perf-rust-build
description: Measure and improve Rust edit-check-build-test iteration and compilation time. Use for slow Cargo builds, unnecessary rebuilds, linking, build scripts, dependency features, crate boundaries, parallelism or compiler caches on Linux and macOS.
---

# Rust build performance

Optimize the developer's actual feedback loop: an edit to useful diagnostics, a runnable
program or a focused test result. Preserve behavior, safety checks, supported targets and
debugging needs. `perf-ci` owns pipeline scheduling; `perf-rust` owns runtime performance.
Use this workflow for build costs in either environment without requiring those companions.

## Identify and measure the loop

Read the owning commands, Cargo workspace/configuration, lockfile, toolchain and IDE/task
configuration. Record `rustc -Vv`, Cargo version, target, selected packages/features/profile,
wrapper/cache state and actual host CPU/memory constraints. A monorepo root command may build
much more than the feature being edited; an IDE, watcher and terminal may duplicate that work.

Read [measurement and rebuild attribution](references/measurement.md) before collecting data.
Separate fresh build artifacts, a warm no-op, a representative implementation edit, a public
interface/dependency edit and branch reuse when relevant. Name which caches remain warm.
Use private task-owned outputs for controlled experiments; do not clean shared Cargo caches
to manufacture a cold baseline. A cache hit, high CPU percentage or a shorter compiler phase
is not the same as faster edit-to-feedback time.

Compare like commands with the same target/test inventory and enough repeated/interleaved
runs to see variation. Record elapsed time and the build units actually executed; inspect
memory pressure or CPU evidence if it changes the diagnosis. Keep diagnostic verbosity and
profiling overhead separate from the final timing. Report a hypothesis when no baseline exists.

## Explain the expensive or unnecessary work

Use Cargo timings for crate scheduling and verbose/fingerprint evidence for invalidation.
Separate dependency resolution/downloads, build scripts/proc macros, frontend checking,
code generation, linking, test discovery and test execution. Cargo's crate lanes do not show
all compiler-internal parallelism. More jobs cannot remove a dependency barrier and may
increase swapping, contention or latency for the developer.

For source, graph or execution changes, read [code and scheduling](references/code-and-scheduling.md).
For incremental state, sccache, build profiles or linkers, read
[caches and profiles](references/caches-and-profiles.md). Follow current primary sources and
the selected toolchain's help: ordinary online documentation can describe unstable features.
Do not switch toolchains, install a cache service or write user-wide flags merely to use a recipe.

Prefer a demonstrated reduction in work: correct generator inputs, stable generated output,
unused dependency/feature removal, less repeated macro/generic expansion, fewer unnecessary
test binaries, or a smaller relevant command. Preserve required verification elsewhere and
validate feature/target consumers before removing an edge. `cargo check` and Clippy do not
replace code generation, linking, execution or the owner's final checks.

Change crate boundaries only when measured dependency fan-out, volatility and critical-path
evidence justify the extra interfaces and build units. A small cohesive crate can improve
reuse; many tiny crates or a universal shared crate can make it worse. Do not trade readable
code for speculative compiler tricks, erase types or reduce runtime correctness to win a build.

## Verify and retain the improvement

Make one coherent change and repeat the relevant loop. Verify intended no-op reuse, an edit
that must invalidate, the supported artifact and meaningful tests. Compare actual work as well
as elapsed time; disconnected targets, stale generated data or missing tests are failures.
Check debugging and runtime consequences of profile/linker changes in the affected configuration.

Use the existing compiler, formatting, Clippy and dependency checks to prevent demonstrated
regressions. Do not invent line-count rules, ban all generics/macros or create a duplicate lint
framework. Performance budgets should reflect representative hardware and noise; ordinary lint
success is not evidence that compilation is fast.

Report the bottleneck, build identity, before/after scenarios and variation, verified behavior,
tradeoffs and coverage gaps. Classify results as improved, regressed, inconclusive or unverified.
Keep compact evidence; remove task-owned targets, profiles and scratch data, stop owned workers
and restore temporary settings. Preserve shared compiler/download caches and required artifacts.
[Research and provenance](references/sources.md).
