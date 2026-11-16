# Rust caches, profiles and linkers

## Select the cache for the iteration

Keep downloaded sources, Cargo artifact freshness, rustc incremental state and sccache separate.
Stable local incremental state often helps edited workspace crates; a remote compiler cache
reuses eligible complete invocations. Neither establishes that linking or required tests ran.
Preserve meaningful input tracking, trusted producers and compatible toolchain/target/flags.

Inspect sccache's installed version and hit/miss/non-cacheable reasons before changing wrappers.
Current upstream Rust guidance excludes linker-invoking binaries/dynamic libraries/proc macros
and ordinary metadata-only `cargo check`; a high hit percentage can coexist with expensive links.
Incremental compilation is not itself cached. Newer `SCCACHE_ALLOW_INCREMENTAL` behavior can
pass workspace incremental invocations through while caching eligible dependencies; verify the
installed release rather than copying a current-main option. Do not globally disable incremental
compilation for a local workflow just to make sccache accept it.
[Pinned sccache limitations](https://github.com/mozilla/sccache/blob/0fa9cf207d070ab7ea783025db8d2a8375226e47/docs/Rust.md).

Proc-macro external inputs and path remapping can create correctness gaps. Do not hide paths or
environment differences simply to increase hits. Use an existing scoped cache, inspect transfer
cost and prove a relevant input invalidates correctly. Do not start/stop a shared cache server,
change credentials or zero its shared statistics as an incidental measurement. A new remote
cache service is a separate operational decision.

## Preserve the development contract

Record effective dev/test profile values before experimenting. Reduced debug information can
save codegen/link work but removes variable inspection; retain an intentional debug-capable
path when that tradeoff is acceptable. `line-tables-only` is not full debugger information.
Cargo's macOS split-debuginfo default differs from bare rustc; inspect effective output rather
than copying a Linux profile. Stripping afterward does not avoid generation costs.
[Cargo profiles](https://doc.rust-lang.org/cargo/reference/profiles.html),
[rustc codegen controls](https://doc.rust-lang.org/rustc/codegen-options/index.html#split-debuginfo).

Do not reduce debug assertions, overflow checks, unwinding or supported targets as a speed fix.
LTO and a single codegen unit are not generic iteration defaults. Dependency optimization can
make a development app usable or an expensive macro faster while increasing fresh build cost;
high optimization can also inhibit generic sharing and introduce duplicate host/runtime units.
Evaluate the combined build-and-run loop, keeping release evidence separate.
[Overrides and generics](https://github.com/rust-lang/cargo/blob/3acc79c0c841844675bc53a605922dbfc441e750/doc/book/src/reference/profiles.md#overrides-and-generics),
[Bevy's workload-specific setup](https://bevy.org/learn/quick-start/getting-started/setup/#enable-fast-compiles-optional).

## Inspect the actual linker and platform

Rust >=1.90 uses LLD by default on `x86_64-unknown-linux-gnu`; that statement does not cover
all Linux architectures/ABIs. Inspect the actual invocation, distinguishing the compiler driver
from its linker. Compare warm incremental links as well as fresh builds, memory, symbols and
behavior before changing an existing tool. Historical linker benchmarks are leads, not guarantees.
[LLD transition](https://blog.rust-lang.org/2025/09/01/rust-lld-on-1.90.0-stable/).

Mold's Linux benchmarks on Apple hardware running Asahi are not evidence of macOS support.
Do not transplant Linux linker flags or recommend an obsolete macOS linker from an old blog.
Existing platform linker improvements may already be present. Avoid user-wide configuration
and preserve FFI, dylib, debugger, packaging and deployment requirements.
[Mold platform/configuration evidence](https://github.com/rui314/mold/blob/331ac663668dc0b1f4949403854613b9b1913025/README.md).

Cranelift is an optional compatible-nightly experiment when LLVM codegen is the measured
cost. Its supported architectures do not imply interchangeable behavior: SIMD and unwinding
have limitations, including macOS unwinding restrictions at review. A faster build can produce
slower tests, and changed panic behavior invalidates parity. Keep the ordinary backend's required
checks. Do not install or select a nightly/backend automatically.
[Cranelift compatibility](https://github.com/rust-lang/rustc_codegen_cranelift/blob/c8fadca8eda3b276b69a40904118ce6150a0e10e/Readme.md).
