---
name: perf-swift-build
description: Measure and improve local Swift, Xcode, SwiftPM and Tuist edit-build-run-test iteration. Use for slow or unnecessary compilation, type checking, target graphs, scripts, previews, parallelism, linking or compilation and module caches.
---

# Swift build performance

Reduce the time from a representative edit to useful diagnostics, a working preview/app or
a focused test result. Preserve UI, product behavior, API/ABI and resource contracts, supported
destinations, signing requirements and debugging quality. `perf-ci` covers pipeline orchestration;
`perf-apple` covers application runtime profiling. This build workflow works independently.

## Establish the real development loop

Read the owner instructions and actual Xcode/SwiftPM/Tuist entrypoint. Identify who owns the
project: checked-in project files or generator inputs. Record selected Xcode/SDK/Swift/Tuist,
build backend, scheme/product, configuration, destination, architecture, resolution state and
effective flags. Include generation, indexing, previews, launch or test startup only when they
are part of the chosen loop; report those costs separately from compilation.

Read [instrumentation](references/instrumentation.md) to select evidence. Compare fresh build
artifacts, a warm no-op, a representative implementation edit, an interface/dependency edit
and branch reuse when relevant. State which SDK, package, compiler and module caches remain
warm. A clean build can still hit compilation caches. Use isolated task-owned outputs for
experiments; do not purge shared DerivedData or package caches as a routine optimization.

Measure outer elapsed time and executed tasks under matching source/configuration/hardware
conditions. Repeat/interleave enough runs to distinguish variation. Do not add overlapping
task durations and label the sum build latency. A parser's clean/incremental label or reported
cache hit is not proof of the experiment's actual state or a faster developer workflow.

## Find the critical work

Inspect the build timeline/dependency graph, slow actions and reasons work reruns. Separate
planning/resolution, generated work, dependency scanning/module variants, Swift type checking,
code generation, linking/signing and execution. An activity timeline is not a CPU/memory profile;
collect scoped host/process evidence only when needed to distinguish work, waiting or pressure.

Read [code, modules and scheduling](references/code-and-modules.md) for source or graph changes,
and [Tuist and cache reuse](references/caches-and-tuist.md) for caching or generation changes.
Prefer fixing inaccurate inputs, unnecessary dependency edges, duplicate module variants and
measured expensive expressions before adding infrastructure. Keep generators deterministic
and avoid rewriting unchanged output. Edit the generator input, not derived project files.

Choose cohesive module boundaries using change frequency, stable interfaces and actual target
costs. Splitting a large target can expose parallel work but adds scanning, module emission,
linking and maintenance. Do not make a target per file or remove a real dependency for a prettier
timeline. Preserve resource lookup, SwiftUI identity/state and runtime linking when restructuring.

Budget compiler operations together with concurrent builds, indexers, previews and simulators.
Tune against wall time, memory pressure and developer responsiveness; maximizing core use is
not the acceptance criterion. Do not change compiler mode, SDK, architectures or project format
without understanding compatibility and the user's scope. Version-check every proposed flag.

## Verify and make the result durable

Repeat the same scenarios after one coherent change. Verify no-op reuse and an input change
that must rebuild; inspect the executed targets and resulting app/resource/test behavior. A
cache miss must still produce correct output. Run owning checks and keep release/archive and
device coverage separate from a fast cached simulator or preview build.

Use existing deterministic checks for real dependency declarations, generated-file drift and
supported build settings. Optional compiler timing warnings help locate expensive expressions;
they are not a universal stable lint threshold. Avoid filename/line-count bans, blanket type
erasure or large speculative test matrices. Keep measured build budgets distinct from linting.

Report configuration, source, cache/scenario identity, before/after duration and variability,
work eliminated, correctness evidence and remaining gaps. No measured gain is a valid result.
Save compact redacted findings, then remove task-owned DerivedData, module-cache experiments,
logs/traces and fixtures; stop owned helpers and restore temporary diagnostics/settings. Preserve
shared caches, existing builds and required receipts. [Research and provenance](references/sources.md).
