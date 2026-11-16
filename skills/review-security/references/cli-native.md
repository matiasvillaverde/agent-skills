# CLI and native boundaries

First establish whether the tool runs as the user, as a service, in CI or with elevated
rights. A user deliberately running their own command is different from a downloaded
file, remote response or repository hook selecting a command under that user's authority.

Inspect subprocess APIs, executable lookup, inherited environment, config discovery,
plugins, archive extraction, temporary files, terminal output and local listeners.
Use argument arrays and validated operands; avoiding a shell does not prevent option
injection or an attacker selecting an executable. Use an option terminator only when
supported. [OWASP's command-injection guidance](https://cheatsheetseries.owasp.org/cheatsheets/OS_Command_Injection_Defense_Cheat_Sheet.html)
distinguishes argument injection from shell metacharacters.

Check traversal, symlinks, check-then-open races, overwrites, special files, permissions
and archive expansion limits. Prefer appropriate filesystem primitives at the final
open/use boundary; string normalization alone does not prove confinement. Review
update/download signatures and trust roots, cancellation/partial-write recovery,
redirects, TLS and secrets in command arguments/history. Render untrusted terminal
text without allowing control-sequence side effects where relevant.

For loopback servers, establish caller authentication, origin checks, binding addresses
and exposure to other users/processes. “Localhost only” is not the same as a trusted caller.

## Language-specific investigation

| Language | Useful questions and deterministic evidence |
| --- | --- |
| Rust | Inspect unsafe contracts at safe entry points, FFI, lifetimes, aliasing, Send/Sync, parser bounds, panic/abort paths and async cancellation. Clippy is supplementary; use targeted Miri/sanitizer/fuzz evidence where supported, plus RustSec checks. A crate without `unsafe` can still have exploitable logic or availability defects. |
| Go | Trace exec/path handling, HTTP timeouts and limits, goroutine/channel lifetime, races, cancellation and unsafe/cgo. Use existing vet/static analysis, focused race tests and govulncheck. Explain source/build-tag/platform coverage. |
| C/C++ | Inspect allocation-size arithmetic, bounds, lifetime, ownership, format strings, parser states, concurrency and FFI. Use relevant Clang static analysis and separate supported sanitizer configurations. A crash alone does not establish code execution. |
| Zig | Inspect allocation ownership, error cleanup, slices/pointers, integer operations, C interop and build mode. [Runtime safety (0.15.2 example)](https://ziglang.org/documentation/0.15.2/#Illegal-Behavior) differs by mode; Debug/ReleaseSafe checks do not prove ReleaseFast behavior. Match docs to the pinned compiler and use leak/error-path tests. |
| CUDA | Inspect untrusted shapes/dimensions, host/device buffer sizes, initialization, synchronization and cross-request buffer reuse. [Compute Sanitizer](https://docs.nvidia.com/compute-sanitizer/ComputeSanitizer/index.html) offers memcheck, racecheck, initcheck and synccheck; choose relevant tools with small fixtures. Racecheck is not a general proof of race freedom. Check host code separately. |

[AddressSanitizer](https://clang.llvm.org/docs/AddressSanitizer.html) detects selected
memory defects in executed paths; it is neither a complete audit nor a production
hardening runtime. Match supported checks to target/toolchain. Keep bounded fixtures
for the actual invariant instead of building a combinatorial sanitizer/test matrix.
Kernel, cryptographic and privileged-driver work may require a specialist assessment;
state the limitation without declaring uninspected code safe.
