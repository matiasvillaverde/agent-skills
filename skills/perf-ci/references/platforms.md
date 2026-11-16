# Platform-specific checks

Consult only the stack involved. These are decision aids and source entrypoints, not a list
of tools to install. Check the repository's actual version/configuration and current official
semantics before applying flags. Preserve typechecking, sanitizers, security and supported
platform checks even when compilation/test execution moves to separate jobs.

## Rust

Keep Cargo downloads, build artifacts, compiler cache and test results distinct. Inspect
profile, features, target, compiler, build scripts and runtime fixtures when reusing outputs.
The [Cargo cache guide](https://doc.rust-lang.org/cargo/reference/build-cache.html) describes
artifact locations; do not assume one directory or current option applies to every release.

When nextest is already appropriate, [archives](https://nexte.st/docs/ci-features/archiving/)
can separate build from execution and [partitions](https://nexte.st/docs/ci-features/partitioning/)
can divide test execution. Partitioning alone can still repeat compilation. Preserve required
runtime data and compatible environments, and check complete assignments. nextest runs tests
in separate processes: an in-process mutex cannot protect a shared database/device across
them. Use existing test groups or isolated resources. Inspect applicable doctest/other runner
coverage rather than assuming a runner switch executes exactly the same inventory.

[sccache's Rust limitations](https://github.com/mozilla/sccache/blob/7df8044dcabc3f7a0948e3df30678bf6f7b72eae/docs/Rust.md)
make it a fit decision, not a universal replacement for local incremental compilation.

## Go

The [Go command](https://pkg.go.dev/cmd/go) distinguishes build/package concurrency from
parallel test functions within a binary. Budget both and any child goroutines/processes.
Cached successful tests are not new executions; use the supported fresh-run option when
checking changed external services or validating a new cache policy. Toolchain, flags and
test inputs matter. Changes in cgo-linked system libraries are a documented cache gap:
refresh the affected outputs rather than trusting an unrelated dependency-cache hit.

## Python

[pytest-xdist scheduling](https://pytest-xdist.readthedocs.io/en/latest/distribution.html)
can favor duration balance or fixture locality. Choose against observed startup/straggler
cost, not a default of one worker per reported core. Its
[worker/session guidance](https://pytest-xdist.readthedocs.io/en/latest/how-to.html) explains
that session fixtures normally execute per worker. Reuse worker-local immutable setup while
giving tests independent state. Use run/worker identities for external resources where needed;
shared coordination must survive failures and process boundaries.

For existing uv environments, [cache inputs and economics](https://docs.astral.sh/uv/concepts/cache/)
include dynamic package metadata and built versus downloaded wheels. Transporting every cached
wheel can cost more than downloading it. Apply pruning only to the owned CI cache scope;
do not clean a persistent shared host's caches as an incidental test optimization.

## TypeScript and JavaScript

Read the actual runner's controls. [Vitest performance](https://vitest.dev/guide/improving-performance)
distinguishes aggregate phase work from elapsed time and shards by file. Combining all tests
into one file can remove scheduling freedom. [In-file concurrency](https://vitest.dev/guide/parallelism)
does not create more workers; asynchronous tests can still race over shared state. Check
environment setup and memory before increasing worker count or disabling isolation.

Use [TypeScript project references](https://www.typescriptlang.org/docs/handbook/project-references.html)
when they fit genuine dependency boundaries and incremental checking. References alone do
not promise multicore execution. Keep explicit typechecking when bundlers only transpile.
Since [TypeScript 5.6](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-5-6.html#allow---build-with-intermediate-errors),
build mode can emit best-effort output after intermediate errors; output existence is not a
passing check. Verify exit propagation and the installed
[stop-on-error option](https://www.typescriptlang.org/tsconfig/stopBuildOnErrors.html), not stale handbook wording.

## C and C++

With existing [ccache](https://ccache.dev/manual/latest.html) or sccache, inspect compiler
identity, wrapper behavior, headers, defines, target/flags and generated inputs. Do not weaken
input tracking or enable sloppiness just to raise hits. Depend-mode/header exclusions can
miss relevant changes; use a representative invalidation probe for the chosen mode.

Use build-graph evidence to reduce broad header churn and expensive serial compile/link work.
[Ninja pools](https://ninja-build.org/manual.html#ref_pool) and
[CMake JOB_POOLS](https://cmake.org/cmake/help/latest/prop_gbl/JOB_POOLS.html) can bound heavy
links separately from compilation; the CMake property is generator-specific. Coordinate
nested builds through supported jobserver/resource mechanisms and actual memory limits.
Keep debug/sanitizer/release configurations distinct and preserve their required coverage.

## Zig

Use the existing [build graph and cache](https://ziglang.org/learn/build-system/) with the
pinned Zig release; live tutorial examples can target a newer compiler. Inspect per-step
time and memory to identify large serial steps or redundant generated work. Budget resource
controls against real capacity. A required step skipped because of memory limits is missing
validation; do not accept an OOM-skipping option as an optimization that makes CI green.

## CUDA

Separate CPU-heavy compilation from GPU-dependent testing. Use existing
[compile-phase measurements](https://docs.nvidia.com/cuda/cuda-programming-guide/05-appendices/compile-time.html)
to locate expensive templates, headers, device linking or unnecessary architecture variants.
Preserve supported targets; do not reduce optimization or architecture coverage for a faster
build without checking the changed product requirements and runtime behavior.

Budget outer build jobs, NVCC threads/split compilation and device-link memory together;
budget GPU tests separately by available devices/memory. Check the installed
[NVCC reference](https://docs.nvidia.com/cuda/cuda-compiler-driver-nvcc/): at review its extended
split-compilation mode was explicitly outside jobserver limits, despite broader prose in
another guide suggesting otherwise. Do not assume one outer job limit controls all work.
