---
name: perf-ci
description: Review and improve CI build/test speed without weakening its signal. Use for redundant tests, slow pipelines, parallelism, cache misses, affected-test selection, modular builds or Tuist-based iOS CI.
---

# Faster, trustworthy CI

Reduce time to useful feedback and wasted work while preserving the behavior CI must verify.
Use the existing provider, runner, build system and project checks. A review stays read-only;
an improvement request permits scoped changes, not a replacement CI platform.

For compiler and local edit-build-test bottlenecks, use `perf-rust-build` or
`perf-swift-build` when available. They own build instrumentation, invalidation and local
iteration experiments; this skill retains pipeline scheduling, cache trust and required checks.

## Find where the time and work go

Read the owning instructions, pipeline/command definitions, pinned toolchains, dependency
graph and recent run evidence. Identify required tests, platforms, security checks and release
gates before proposing cuts. Follow the repository's CI entrypoint and receipt rules.

Separate queue wait, setup/dependency restore, build/generation, test discovery/fixtures,
test execution, artifact/cache transfer and report aggregation. Record source/configuration,
runner CPU/memory limits, cache state, selected tests and retries. Compare like runs; distinguish
submission-to-required-result wall time from job duration, summed CPU work and runner minutes.
Use available run variation rather than a best run or an arbitrary percentage threshold.

Draw the actual dependency path to the required result. A long job need not be the limiter,
though reducing other work can relieve contention on a shared runner. Find the smallest
supported cause: duplicate work, idle dependency barriers, slow setup, uneven shards, cache
invalidation, a serial build target, oversubscription or flaky retries. No timing data means
a hypothesis and measurement plan, not a claimed speedup.

## Fewer tests with stronger behavioral coverage

Favor an integration-heavy application suite: most behavior checks should exercise real
collaborating components through a useful public boundary. Keep the scope bounded: a service
with its real test database, a UI component with its real state logic, or a CLI and its output.
Use controlled doubles at external/unavailable boundaries, with contract checks where needed.
Keep a small set of actual end-to-end journeys. Retain focused unit tests for algorithms,
parsers, numerical boundaries and hard-to-reproduce failures; do not manipulate counts to
achieve a ratio or replace every cheap test with a full-stack startup.

For each removal or merge, identify the scenario, protected behavior, plausible regression
and surviving assertion. Equal assertion text or unchanged line coverage does not prove
redundancy. Combine repeated setup/action and complementary assertions about the **same
outcome** into one readable test. Keep distinct inputs, boundary conditions, failure modes
and independent contracts separately diagnosable. A successful save can check both its
response and persisted state; two different reasons for rejection remain different cases.

Prefer explicit named tests. Do not introduce parameterized matrices, generic assertion
frameworks or a giant sequential journey to reduce the test count. Readability and useful
failure messages matter more than minimum lines. Never delete a failing test to get green.
Preserve security, migration, concurrency and historical regression protection. For a
consequential consolidation, use a small representative fault or known-bug fixture to check
that the surviving test can still fail for the protected behavior; no blanket mutation suite.

Optimize expensive setup independently of test semantics. Reuse immutable fixtures or a
worker-owned service when safe, isolate mutable records/ports/files per case, and clean up
after failure and cancellation. Shared setup must not introduce order dependence. Investigate
flake causes; retries and quarantine must remain visible under the owner's existing policy.

## Schedule and cache useful work

Read [builds, caches and parallelism](references/builds-and-caches.md) when changing execution,
selection, cache keys or module boundaries. Parallelize independent jobs/tests with explicit
dependencies and isolation. Budget concurrent jobs, test workers, compiler threads and child
processes together against actual CPU, RAM, I/O and device capacity. More workers are not
automatically faster. Balance shards by observed duration and setup cost, not just file count.

Reuse a compatible build across tests when transfer and coordination cost justify it.
Distinguish dependency downloads, compiler/build outputs, test-result reuse and artifacts.
Verify cache inputs, compatibility and trust before widening reuse; a cache hit is not proof
that the required tests ran. Affected-test selection needs a trustworthy dependency graph,
conservative fallback and validation of omitted work, including shared config and generators.

Inspect modularization for both build critical path and change invalidation. Split a measured
large/volatile target along cohesive boundaries when this exposes independent work or
preserves reusable outputs. Avoid umbrella dependencies, unnecessary public coupling and
always-running generators. Do not create a target for every file or a module abstraction
solely to occupy more cores; extra graph, compile and link overhead can erase the benefit.

For **iOS**, use the [Tuist and Apple guidance](references/apple-tuist.md). Prefer the existing
Tuist integration or the smallest compatible Tuist integration; compilation caching does
not necessarily require migrating an Xcode project to generated projects. Check installed
versions and capabilities before adopting live-documentation commands. Preserve actual
device/OS coverage, signing and archive/release requirements.

For other stacks, consult only the relevant row in
[platform checks](references/platforms.md). Reuse the cache and test runner already owned by
that CI; do not install every tool mentioned or introduce a new remote service by default.

## Prove the change improves CI

Make one coherent change against a recorded baseline. Validate the affected behavior and
the owning required checks. When changing cache or test selection, exercise a representative
hit, miss/invalidation and fresh execution; when changing shards, verify the expected test
inventory is complete and reports preserve every worker's failures. Scale these probes to
the change, reusing existing evidence rather than repeatedly running the entire suite.

Compare wall time, resource/runner cost, cache transfer cost, selected/executed tests and
first-attempt failures under matching conditions. Do not report a gain caused by skipped
required tests, a weaker platform matrix, hidden retries, stale results or omitted setup.
Keep the improvement only if its benefit justifies its complexity and reliability remains
intact. Keep cancellation cleanup, failure propagation and required-check aggregation working.

Report the bottleneck, change, before/after conditions and measurements, preserved coverage,
and remaining gaps. Separate implemented configuration from an observed CI improvement.
Keep private logs/receipts with their existing owner. Do not alter deployment gates, signing
access, paid runner capacity or cache trust boundaries without applicable task authorization.

## Finish and clean up

Save the results and reproduction commands, then stop task-owned runners/services and
remove scratch worktrees, disposable build outputs, traces and isolated cache experiments
created for this investigation. Establish exact ownership before deletion and preserve
uncommitted work, shared CI/dependency/compiler caches and required receipts/artifacts.
Remove temporary diagnostics and restore task-changed settings even on failure or
cancellation. Keep only requested/required evidence or the minimum needed for unresolved
failures; verify cleanup and report any leftovers with the reason.
