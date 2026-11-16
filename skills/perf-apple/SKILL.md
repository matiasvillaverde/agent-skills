---
name: perf-apple
description: Profile native Apple apps with Instruments and xctrace. Diagnose CPU, UI, memory, networking, audio, GPU, energy, storage, concurrency and model latency using scoped captures and measured comparisons.
license: MIT
---

# Profile Apple apps

Start with the named operation, target device, correctness requirement and measurement budget. Reuse existing traces and benchmarks. Record build configuration, selected Xcode, symbols, input, concurrency and thermal/power conditions. Prefer an optimized representative build with matching symbols. Simulator measurements can diagnose code paths but do not establish physical-device CPU, GPU, memory or energy behavior.

Separate cold launch, first-use initialization and warmed steady work. Define the cold/reset state and launch endpoint, such as the first usable interactive screen; a fresh process does not imply cold system caches. Do not warm away a startup regression or mix these populations in one comparison.

## Define acceptable results

Before optimizing, use [acceptance criteria](references/acceptance.md) to state the target metric,
baseline, workload budget, product invariants and relevant resource guardrails. Preserve UI,
functionality, accessibility, output quality, cancellation and durability unless the user
explicitly includes a product change. A speedup obtained by reducing quality or skipping required
work is not an optimization success. If no product budget exists, establish a baseline and label
the proposed target; do not invent universal thresholds.

## Choose the workflow

The [instrument catalog](references/instruments.md) covers all 63 instruments discovered in
Xcode 27. Read only the section matching the evidence; each explains capture, interpretation,
pitfalls and documentation. Refresh the installed inventory instead of treating this count as
universal. Available, configurable, recorded and successfully measured are different states.

| Evidence / question | Catalog mode and paired recipe |
| --- | --- |
| Computation, cycles, cache/branch bottlenecks | `cpu` |
| Hangs, blocked/runnable threads, syscalls, run loops | `scheduling` |
| Task fan-out, actor/executor contention, GCD | `concurrency` |
| Allocation churn, leaks, retained objects, VM footprint | `memory` |
| Startup, dynamic loading, first usable content | `launch` |
| Scroll/animation hitches, Core Animation phases | `scroll` |
| SwiftUI update causes, body/layout work, legacy targets | `swiftui` |
| File descriptors, storage access and write amplification | `io` |
| SwiftData/Core Data faults, fetches and saves | `persistence` |
| Connections, HTTP phases, bytes and request counts | `network` |
| Audio render callbacks, engine jitter and deadlines | `audio` |
| Metal work, GPU counters/resources and display pacing | `gpu` |
| RealityKit, SceneKit and foveated streaming | `spatial` |
| Power, thermal changes and location activity | `energy` |
| Core AI/Core ML execution and Neural Engine | `ml` |
| Foundation Models requests, tools and tokens | `foundation-models` |
| Signposts, state, unified logs and process output | `logging` |

[Capture guidance](references/capture.md) provides 17 portable CLI recipes, native user-template
creation, device/UI automation and export procedures. `scripts/capture.py --list` lists recipes;
it previews recording commands unless `--run` is supplied. Add an instrument only for a concrete
follow-up; coverage does not mean collecting every track together. Sources and documentation
gaps are recorded in [sources.md](references/sources.md).

## Research the mechanism

Before choosing a fix, consult current Apple documentation and the relevant public API surface.
Use [API and hardware investigation](references/investigation.md) to inspect SDK declarations,
availability, defaults and isolation; follow references into release-tagged source, optimized
assembly or controlled experiments when needed. Review relevant methods, properties, protocols
and callbacks, not only the currently used method. Record what was reviewed and distinguish
documented contracts, observed behavior and inference. Hardware references and reverse-engineering
guidance live there; an unexplained profile is not permission for private API dependencies or
unrelated system changes.
For CPU microarchitecture, instruction costs, caches or asymmetric scheduling, consult the
[Apple CPU guide](references/sources.md#apple-cpu-and-metal-references) when present.
Read the relevant sections and match their chip family to the target; access does not imply
that the entire guide has already been reviewed.
When collection, lookup or repeated sorting work matters, use the shared
[data-structure review](../perf-system/references/algorithms-and-data-structures.md) when available.
Account for copy-on-write, ARC and representation conversion; preserve UI identity and ordering.
For Metal kernels, GPU ML or hardware limits, consult the [official Metal PDFs](references/sources.md#apple-cpu-and-metal-references).
Use the MPP guide for matrix operations, the language specification for shader semantics, and
the feature tables for family capabilities; verify SDK and device support before adopting a feature.

Read [Metal investigation](references/metal.md) for frame replay, `gpudebug`, shader/counter analysis
or kernel changes. Read [performance regression testing](references/regression-testing.md) for
repeatable device benchmarks and CI performance gates. For MetricKit reports and release/cohort
evidence, use `perf-apple-production` when available; field telemetry and local profiles have
different coverage and time semantics.

## Select and capture

Discover the installed capabilities before constructing commands:

```sh
xcrun xctrace version
xcrun xctrace list templates
xcrun xctrace list instruments
xcrun xctrace list devices
xcrun xctrace help record
xcrun xctrace help export
```

Use the selected Xcode's available templates and instruments; names, export schemas and device support vary. If unavailable, inspect the selected developer directory and report the gap. Do not install tooling or change the project's deployment target to make a profile run.

Choose the smallest useful capture:

- CPU sampling for repeated computation; thread states and scheduling for busy-versus-blocked hangs.
- Allocations, Leaks and Memory Graph for allocation stacks, retaining owners and lifecycle cleanup.
- SwiftUI instruments for update frequency, paired with CPU evidence for expensive work.
- Metal debugger/system trace for GPU timing, passes, synchronization, resource dependencies and memory.

Attach to an existing selected process for steady work. A bounded recording has this shape, using actual discovered values:

```sh
xcrun xctrace record --template '<installed-template>' \
  --attach '<pid>' --time-limit '<duration>' --output '<private-path>.trace'
```

Add the selected device explicitly when needed. For startup, use the installed tool's supported launch workflow and capture initialization. Reproduce the relevant interaction during recording. Keep duration, output size and process scope bounded; do not switch to all-process capture, restart unrelated apps or change profiling permissions to overcome a refusal. Reuse existing authorization for scoped recording and launch.

## Interpret what was measured

Discover exportable tables from the actual trace:

```sh
xcrun xctrace export --input '<trace>.trace' --toc
```

Select relevant tables with the installed export command's XPath support. Parse XML with an XML parser that resolves referenced entries; grepping rows can misattribute stacks and samples. If a family is absent, unexportable or unsupported by the parser, label it unmeasured or partial and inspect it in Instruments when useful.

Match dSYMs to the recorded build. Consult `xcrun xctrace help symbolicate` and write a separate symbolicated output to preserve the original. Unresolved addresses remain unresolved; do not invent function attribution.

Compare absolute operation duration and CPU work as well as inclusive/self samples. A function's CPU percentage can rise because other work disappeared; percentage-share changes alone do not establish a regression.

Distinguish allocation churn, live retained objects, allocator/cache retention and RSS. Repeat representative open/close or start/stop cycles after the relevant warmup, identify the retaining owner, then verify release. A short quiet trace or missing leak warning does not prove absence of leaks. Preserve buffer/texture ownership and synchronization until GPU work completes.

## Accept and report

Change one evidenced bottleneck at a time. Apply the selected workflow's acceptance criteria:
verify affected UI/behavior, compare relevant resource costs, and recheck under the same workload
without heavy diagnostic overhead. Repeat enough to distinguish improvement from noise. Keep
only gains that justify maintenance cost; reuse a few meaningful regression tests.

Report workload, commands, before/after values with variability, budget, correctness evidence and
coverage gaps. Label claims accepted, inconclusive, regressed or not verified; recording success
does not prove a product improvement. Keep raw traces private while investigating; report a trace
location only if the trace is retained.

## Finish and clean up

Put new captures, exports and disposable build/cache data in an identified task-owned directory. After verification, save the compact findings, measurements and reproduction commands, then stop owned recordings/helpers and close loaded captures before deleting the task's temporary `.trace`, `.gputrace`, memory graphs, XML/HAR exports, probe binaries and isolated caches/DerivedData. Remove temporary instrumentation and restore profiling or network settings changed for the task.

Delete only exact paths whose ownership is established; never sweep shared Xcode, simulator, package or application caches. Keep evidence explicitly requested or required by retention rules, and the minimum capture still needed for an unresolved failure. On failure or cancellation, still stop owned work and restore settings. Verify cleanup and report any retained artifacts or leftovers with the reason.

Sources, modifications and licensing: [NOTICE.md](NOTICE.md).
