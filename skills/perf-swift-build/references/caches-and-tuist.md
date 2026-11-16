# Swift caches and Tuist

## Choose the reuse mechanism

| Mechanism | Meaning and check |
| --- | --- |
| Package/download cache | Avoids retrieving dependencies; does not prove they were compiled. Preserve resolved versions and integrity. |
| Incremental build state | Skips unchanged local actions. Explain input/output changes and retain stable paths/configuration for the experiment. |
| Xcode compilation cache | Reuses equivalent compiler actions; can help after branch switches or artifact cleaning. Check effective enablement and actual task hits for the installed Xcode. |
| Tuist module cache | Substitutes compatible built modules in a generated graph. Edited modules may remain source; verify which implementation/resources the workspace actually uses. |
| Selective tests | Reuses prior result/impact evidence to omit execution. This is a separate qualification decision, not compiler caching. |

Xcode introduced compilation caching in 26; later defaults and support vary. Check effective
settings rather than assuming an enablement flag changed behavior. Compare a valid hit, an
expected miss and meaningful edit latency. A clean-artifact build can still use compiler or
SDK caches; label the state precisely.
[Xcode 26 release notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-26-release-notes).

Prefer the current owned cache/generator before adding a platform or service. Tuist compilation
caching can work with ordinary Xcode projects; it does not require converting the project to
generated manifests. Module caching and generated-project test selection have different
requirements. Do not assume one Tuist feature enables all layers.
[Compilation cache](https://tuist.dev/en/docs/guides/features/cache/xcode-cache),
[module cache](https://tuist.dev/en/docs/guides/features/cache/module-cache).

## Verify the installed Tuist contract

Record `tuist version` and inspect the relevant subcommand help before executing a web example.
At review the local CLI was 4.216.0 while live guides described newer features. Bare
`tuist cache` defaulted to **warming local and remote caches**; it is not a read-only inspection
command. Use existing authorization and project service access. Do not create accounts, upload
source-derived logs, change cache credentials or start an infrastructure migration implicitly.

Module warming/generation can change the generated workspace. Isolate it from simultaneous
consumers, modify authoritative manifests/helpers and preserve the source-built release/archive
path. Tuist documents module caching for development/test, not release archives. Keep configuration,
compiler/SDK, target, coverage and generated/resource inputs compatible.

Inspect target hashes and detailed run evidence to separate direct changes from downstream
invalidation. If only a Git diff is available, label the inferred cause rather than inventing
target-level telemetry. Compare equivalent runs, not merely the latest on each branch. Inspect
cache transfer and generation overhead; high hit percentages can hide a critical link/script.
[Tuist hashing](https://tuist.dev/en/docs/guides/features/projects/hashing),
[build comparison skill](https://github.com/tuist/agent-skills/blob/5da5c0f67df8277de699d64782a3810f9d30ee1b/skills/compare-builds/SKILL.md).

## Protect correctness and the shared developer environment

Keep all real inputs in the reuse decision. Source, dependencies, resources, generated inputs,
compiler/SDK, architectures, effective flags and relevant environment can change outputs.
Do not normalize semantically different paths/settings or remove inputs to raise hit rates.
Cache entries need trusted producers as well as compatible keys. Preserve the existing scope
of remote writes and publication rules for failed/cancelled builds.

Treat a machine-wide proxy and shared caches as shared resources. Do not restart them, race
their configuration or delete stores while other builds use them. Use task-owned cache namespaces
for experiments where supported, and make cache absence recover by building correctly.
Measure remote lookup/download costs separately from work saved.

If experimenting with selective testing, verify selected/executed/reused targets and required
destination coverage. A prior simulator result cannot qualify a new device/OS by assumption.
Keep mandatory full/fresh checks and failure propagation. Pipeline sharding and admission remain
with `perf-ci` where available.
[Tuist selective-testing contract](https://tuist.dev/en/docs/guides/features/selective-testing/generated-xcode-project).
