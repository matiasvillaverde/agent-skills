# iOS and Apple CI with Tuist

Use Tuist for the iOS optimization path, selecting the layer that fits the existing project.
Inventory the pinned Tuist, Xcode and Swift versions, project-generation ownership, schemes,
build configurations, destinations, signing requirements and current caches. Consult the
matching CLI help and release documentation before changing commands or settings.

Live documentation can describe unreleased behavior. At the 2026-11-13 review, the observed
stable CLI was 4.216.6 while live guides discussed features from 4.218.0; the repository's
`releases/latest` endpoint pointed to a Helm release. Neither a current web example nor that
endpoint alone establishes the correct CLI. Do not upgrade tools or credentials implicitly.

## Choose the cache layer

| Layer | Fit and important constraints |
| --- | --- |
| Dependency downloads | Reuse resolved packages with the existing lockfile/toolchain checks. This avoids downloads, not compilation or tests. |
| [Tuist compilation cache](https://tuist.dev/en/docs/guides/features/cache/xcode-cache) | Uses Xcode compilation caching, introduced in Xcode 26. Works with ordinary Xcode projects; a generated-project migration is not required. Verify effective settings, proxy reachability and actual hits. A successful build does not establish remote cache use. |
| [Tuist module cache](https://tuist.dev/en/docs/guides/features/cache/module-cache) | Replaces eligible modules in the generated graph with compatible binaries. Match compiler/configuration/coverage/platform inputs. Test support may be cacheable while test bundles are not. Warming can change the generated workspace; isolate it from simultaneous consumers. |
| [Selective testing](https://tuist.dev/en/docs/guides/features/selective-testing/generated-xcode-project) | Reuses successful target/dependency evidence to avoid execution. It is a separate correctness decision from compilation reuse. Inspect selected, executed and reused targets; retain full required validation paths. |

Tuist documents module caching for development/test, **not release archives**. Preserve the
documented source-built archive path and the project's release qualification. Do not equate
fast cached simulator tests with a signed, supported release artifact.

Inspect [hash inputs](https://tuist.dev/en/docs/guides/features/projects/hashing) and per-target
run evidence to explain misses. Match toolchains and resolved configurations; account for
resources, generated files, dependencies and coverage builds. Test a relevant edit that
must invalidate reuse. Never remove a meaningful input merely to improve hit percentages.

On persistent runners, coordinate the cache proxy's lifecycle and configuration. The current
proxy is shared per machine; concurrent jobs for the same project can share upload policy.
Do not stop another job's proxy, race configuration updates or assume per-job read-only
settings isolate all writers. Reuse approved access scopes and isolate writable workspaces.
Stale socket settings can cause long stalls; inspect effective settings from the pinned CLI.
Path normalization can affect debug paths, source-relative fixtures and coverage as well as
hits. Change it only with corresponding validation.

## Build once and preserve test meaning

Where supported, build once and distribute the same compatible products and test metadata
to equivalent workers. With Tuist's build-only/without-building flow, preserve the selection
graph alongside products and use the exact source commit. Missing metadata may trigger
regeneration; mismatched metadata can incorrectly omit work. Check portable product support
and any paths referenced by older test-run files. Measure transfer versus rebuild cost.

Keep sharding separate from destination coverage. Apple's distributed testing partitions
work among destinations; it does not run every test on every OS/device. Current Tuist docs
also describe destination variants sharing selective hashes. Preserve the owner's required
matrix explicitly, using fresh execution when a previous destination cannot qualify it.

Coverage-based selective testing is version/service-sensitive and was early access at review.
Its current XCTest/XCUITest behavior is not function-level selection for Swift Testing;
Swift Testing remains target-granular. Do not enable instrumentation, upload source-derived
coverage or add its attribution package by default. For any selection change, inspect why
tests run/skip and validate new, failed, unmeasured and shared-change fallback cases.

## Use parallelism that the machine can sustain

Distinguish compiler scheduling, concurrent CI jobs, simulator workers and in-process test
tasks. Observe memory pressure, CPU, I/O, startup and the longest test groups before changing
worker limits. Do not give every nested layer all available cores. Preserve independent
databases, ports, temporary directories, app containers and device state where relevant.

[Swift Testing](https://developer.apple.com/documentation/testing/parallelization.md) runs
tests concurrently by default. `.serialized` limits its own suite/cases; it does not exclude
unrelated tests or separate processes from a shared resource. Prefer isolation, or coordinate
the constrained resource at the actual process/job boundary. Keep retries visible and use
bounded readiness conditions rather than fixed sleeps or indefinite waits.

## Modularize against the build graph

Use Xcode build timelines and Tuist per-target evidence to find the dependency chain that
gates completion and the edits causing broad rebuilds. A timeline is not a CPU/memory profile.
Remove unnecessary edges and stabilize small useful interfaces. Split a measured expensive
feature only when the resulting targets are cohesive and expose independent/reusable work.
Tuist's [modular architecture](https://tuist.dev/en/docs/guides/features/projects/tma-architecture)
is a source of ideas, not a requirement for five targets per feature. Include planning,
linking, startup and maintenance costs when comparing changes.

Declare the real inputs and outputs of scripts/generators; missing declarations can cause
races or stale results, while unconditional work can defeat incremental builds. Prevent
concurrent writers to generated paths. Verify both relevant incremental behavior and the
actual product when changing module linkage or resources.

Primary background: Apple's [build parallelization](https://developer.apple.com/videos/play/wwdc2022/110364/),
[distributed versus destination testing](https://developer.apple.com/videos/play/wwdc2020/10221/)
and [reliable test design](https://developer.apple.com/videos/play/wwdc2022/110361/) talks explain
the mechanisms; their older defaults/flags are not current prescriptions. Use the current
[Tuist CI guide](https://tuist.dev/en/docs/guides/integrations/continuous-integration) against
the pinned release. Existing CI ownership and required gates remain authoritative.
