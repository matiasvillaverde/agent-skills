# C/C++, CUDA and Zig

Use real target flags, ABI, include paths, optimization mode and generated inputs. Running a
host parser with invented flags can miss the compiled program. Confirm installed versions,
hardware/runtime support and cost before selecting deeper checks.

## C and C++

- Existing formatting checks and compiler warnings for format strings, conversions,
  uninitialized use, return values and suspicious control flow where actionable. Do not
  impose `-Weverything` or treat all vendor warnings as new product defects.
- clang-tidy or another existing analyzer with the actual compilation database and reviewed
  checks; inspect which translation units/macros/headers were analyzed. Clang Static Analyzer
  adds path-sensitive checks but still has modeling and cross-unit limits.
- ASan for relevant bounds/use-after-free faults; UBSan for selected undefined behavior;
  TSan separately for supported threaded execution. Instrument and link the relevant code
  correctly. MSan requires supported platform and suitably instrumented dependencies; do not
  claim it works on any Apple/third-party binary by adding a flag.
- UBSan often reports and continues by default. A gate needs deliberate non-recovery/trap
  configuration or verified report handling; stderr text with exit zero can otherwise pass.
- Keep parser fuzzing and leak/race scenarios focused on changed memory/ownership boundaries.
  No-error output covers exercised code, not all allocations, inputs or threads.

## CUDA

Separate host C/C++ analysis from device checks. Record CUDA toolkit/driver/GPU, compiled
architecture and tested kernels/launches. A successful host compile or zero GPU activity is
not device analysis. Use the existing GPU qualification environment; do not pretend a CPU
machine validated CUDA.

| Device risk | Compute Sanitizer tool |
| --- | --- |
| Out-of-bounds/misaligned access, supported allocation/leak faults | `memcheck` |
| Shared-memory access hazards | `racecheck` |
| Supported uninitialized memory reads | `initcheck` |
| Invalid synchronization/barrier use | `synccheck` |

Check the installed manual for address-space/architecture support. Racecheck is not a
general global-memory race detector. Establish memory-error cleanliness before relying on
other checker results when memory faults could contaminate them. Build with source line
information and configure a nonzero `--error-exitcode` for a gate. Verify child processes,
kernel filters and launch limits did not remove the workload.

Forced blocking changes concurrency and the official manual says it decreases report count
and precision; do not prescribe it as a general precision fix. Compile-time memcheck
instrumentation and ordinary binaries have checker-specific compatibility constraints.
Read the installed version's guidance before combining modes or enabling suppressions.

## Zig

Use the project's pinned Zig compiler/build API. Existing `zig fmt --check`, declared build
steps and targeted tests cover syntax/types and exercised behavior. Lazy analysis means
unused declarations may remain unchecked; a build is not every generic instantiation.

Debug/ReleaseSafe normally enable runtime safety, while ReleaseFast/ReleaseSmall normally
disable it. Local overrides and unchecked illegal behavior still exist. Compare with the
deployed mode where relevant rather than claiming safety-mode tests prove release behavior.
Use the testing allocator/leak diagnostics and focused allocation-failure/error-path cases
for real ownership risks. FFI and imported C need their own applicable checks. Do not claim
generic text matching supplies a semantic Zig/CUDA linter.

Primary sources, checked 2026-11-15: [ASan](https://clang.llvm.org/docs/AddressSanitizer.html),
[UBSan exit behavior](https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html),
[Compute Sanitizer](https://docs.nvidia.com/compute-sanitizer/ComputeSanitizer/index.html),
[Zig 0.16 build/safety modes](https://ziglang.org/documentation/0.16.0/#Build-Mode).
Match the linked manuals to the installed toolchain; they do not establish local availability.
