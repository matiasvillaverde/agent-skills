# Build reuse, scheduling and module boundaries

## Explain the measured pipeline

Use actual start/end times and dependency edges, not a sum of overlapping stage durations.
Measure queueing separately from execution. Compare equivalent source, test inventory,
toolchain, runner allocation, cache state and retry policy. Distinguish a clean build, a
warm no-op, a representative source change and a toolchain/dependency change when relevant.
Do not clean all caches on a shared machine to manufacture a baseline; use an isolated
workspace/cache namespace or an existing controlled run.

Consider wall time and total resource cost independently. Building once and distributing
outputs can save compilation while adding a serial prerequisite and expensive transfers.
Running a setup process once can help, but sharing mutable fixtures can introduce flakes.
Removing an unnecessary barrier can help only if capacity and isolation support overlap.
Existing job locks and release sequencing are real constraints, not accidental overhead.

The [Bazel build study](https://arxiv.org/html/2405.00796v1) found workload-dependent gains
and cache-transfer tradeoffs. Its measured experiments concern compilation of a buildable
subset of public projects, not test execution or guaranteed gains in this repository.
Use its distinction between cache types and measured net benefit, not its speedup numbers.

## Identify what is being reused

| Mechanism | What a hit establishes | What still needs verification |
| --- | --- | --- |
| Download/package cache | Previously retrieved dependency content is available. | Locked resolution, integrity and any install/build steps still required. A restored archive is not a completed build. |
| Compiler/action/module cache | Outputs for an allegedly equivalent build action or target exist. | All effective inputs, compiler/SDK/architecture/flags, generated files, dependencies and output compatibility. |
| Incremental workspace | Local state can avoid some work in a compatible workspace. | Stale paths, concurrent writes, changed toolchain/configuration and actual invalidation. It is not automatically portable between machines. |
| Test-result cache or selective tests | A prior result or dependency analysis permits skipping selected execution. | Valid input/environment scope, actual previously passed result, external state, required platform coverage and conservative fallback. |
| Build artifact | A named output is available to another job or reviewer. | Producing source/configuration identity, integrity, target compatibility and complete required contents. Missing artifacts must not silently choose an unrelated older build. |

Inspect the current cache implementation before changing keys. Include inputs that actually
affect outputs: source and transitive dependencies, lockfiles, build/test configuration,
compiler/SDK, target, features, generators and their inputs, relevant environment and fixtures.
Use the build system's dependency/fingerprint model where reliable. Do not indiscriminately
hash the entire environment or remove legitimate inputs merely to raise the hit rate.

Investigate misses at the responsible target/action: direct change, dependency cascade,
unstable generated input, incompatible configuration, local-only hit, eviction, transfer
failure or unavailable credentials. A correct miss after changed input is healthy. Inspect
restore/save/compression times and bytes; even a valid hit can cost more than recomputation.
Make cache absence recoverable. Keep growth/retention under the existing owner.

Treat restored executable outputs as part of the build trust boundary. Restrict writes to
trusted producers and reads to compatible scopes; a digest alone does not authenticate the
producer. Never upload credentials, signing material or private logs. Broad fallback keys
must not turn incompatible outputs into accepted results: rerun the package/build system's
validation after a dependency-cache fallback. Do not share one mutable output directory
between concurrent builds. Preserve cache publication rules for failed/cancelled runs.

[Bazel's remote-cache model](https://bazel.build/remote/caching) makes action inputs explicit
and documents pitfalls involving environment, external tools and concurrent source changes.
[GitHub's cache guidance](https://docs.github.com/en/actions/concepts/workflows-and-actions/dependency-caching)
also separates artifacts from caches and explains poisoning risks. Apply the actual provider's
contract; these links do not prescribe either provider or a new remote cache.

## Parallelism and selected work

Budget the whole host: CI jobs × runner workers × subprocess/compiler threads is a useful
oversubscription warning, not an exact CPU model. Include simulator RAM, database connections,
GPU memory and storage bandwidth where relevant. Tune against observed contention and
throughput; preserve other jobs' capacity. Limit an unsafe resource group instead of serializing
the entire suite. A language-level lock may not protect separate worker processes.

Use stable test identities and recent timings to balance shards; account for fixture startup
and indivisible long tests. New or unknown-duration tests still need assignment. Verify the
union of shard assignments matches the intended inventory, with no unexplained omissions or
duplicates. Do not optimize by test-file count if one file dominates the run.

Keep each worker's status and report unique. Aggregation must detect a failed, cancelled,
missing or unexpectedly empty worker; merging reports must not overwrite colliding filenames
or test identities. A final shell command exiting zero must not mask earlier failures.
Expected empty shards need an explicit explanation, not a blanket no-tests-is-success setting.
Keep cleanup and useful diagnostics after failures without turning them into success.

Affected-test selection must include reverse dependencies, shared configuration, schemas,
fixtures, build scripts, generators and platform/toolchain changes. Directory filters alone
are rarely that graph. Unknown impact or unavailable history needs a broader fallback. Compare
selected execution with a fresh appropriate full run before relying on new selection rules;
retain the owner's reconciliation/full-run policy. Cached success cannot qualify changing
external services, hardware or a new required OS/device by assumption.

[Buildkite's parallel-build guidance](https://buildkite.com/docs/pipelines/best-practices/parallel-builds)
illustrates capacity limits and shared-resource interference. Provider-specific worker counts
and commercial splitting tools are examples, not defaults to install.

## Make modularization earn its cost

Inspect the measured target graph: serial chains, largest compile/link actions, change
frequency, dependency fan-out and cache invalidation. Prefer cohesive independently buildable
components, a small stable public interface and explicit dependencies. A volatile catch-all
module can invalidate many consumers; generated output that changes unnecessarily can do
the same. Share stable work only where source and configuration are equivalent.

Splitting a large target may expose parallel work and smaller rebuilds, but adds graph setup,
interfaces, linking and maintenance. Measure a representative incremental change as well as
clean-build behavior; check runtime/link behavior when module linkage changes. Avoid cycles,
speculative interface packages and a target-per-file policy. Improve CPU use by removing the
actual serialization or contention, not by maximizing the module count or CPU percentage.
