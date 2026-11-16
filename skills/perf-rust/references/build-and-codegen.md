# Build, inspect and measure the actual Rust artifact

## Profile parity and symbols

Cargo profile tables belong at the workspace root. Reuse the existing profiling profile or a
task-local override inheriting the actual shipping profile. A diagnostic profile often needs:

```toml
[profile.profiling]
inherits = "release" # use the actual shipping parent
debug = true
strip = "none"
```

Preserve target, features, panic mode, allocator, LTO, codegen units and other flags. Do not write
user-wide Cargo configuration. Record diagnostic differences and remeasure the shipping artifact.
Keep matching dSYM/DWARF/PDB and binary identity; split-debuginfo behavior is platform-specific.
Line tables can be sufficient for locations but not every source/inline analysis. Missing standard
library or dependency symbols do not justify fabricated attribution or a toolchain rebuild by default.

Check `rustc -C help` and `rustc --print target-cpus` when those controls matter. Force frame
pointers only when needed for the chosen unwinder; compare the resulting binary separately.
Do not copy an unconditional `lto=true`, `codegen-units=1`, `opt-level=3` recipe. Cargo notes that
3 can lose to 2; `lto=false` can retain local ThinLTO, while `lto="off"` disables it. A host-native
CPU build may be unsuitable for distributed binaries. Changing panic/overflow behavior changes
the contract, not just performance.

## Code generation and SIMD

Inspect the concrete hot specialization and its caller. With installed `cargo-show-asm`, the
command is `cargo asm`; distinguish it from older packages that expose the same command name.
Check installed help and preserve the actual target/profile/features. Example selection:

```sh
cargo asm -p PACKAGE --bin APP --profile PROFILE FUNCTION
cargo asm -p PACKAGE --bin APP --profile PROFILE --llvm FUNCTION
```

The compiler's own emission options and final-binary disassembler are alternatives. A missing
standalone function can be inlined, eliminated or never instantiated. An `inline(never)` wrapper
may help inspection but changes optimization and is not proof of the original timing. Use remarks
to investigate a missed transform; do not force vectorization from a source-level guess.

Validate scalar equivalence, odd/tail lengths, supported alignment, overlapping/aliased inputs
where legal, overflow, NaN/rounding requirements and CPU-feature fallback. Check the actual
monomorphized layout with `size_of`/`align_of` or available tooling before prescribing field order;
`repr(Rust)` does not promise declaration order. `repr(C)` or packed layout changes ABI/alignment
constraints and is not a generic optimization. Larger inline buffers and wider SIMD can increase
copies, stack pressure, cache footprint or frequency costs.

## PGO as a separate experiment

Use PGO only after the ordinary profile identifies a worthwhile case. Instrumentation PGO needs
fresh private profiles, representative training inputs and a compiler-compatible `llvm-profdata`.
Inspect the selected toolchain's documented workflow. Preserve existing flags; use absolute
profile paths and explicit `--target` so instrumentation is not accidentally applied to host build
scripts. Keep target/features/optimization choices consistent between generate and use phases.

The sequence is: build with `-Cprofile-generate=<directory>`, run representative workloads, merge
raw profiles, rebuild with `-Cprofile-use=<file>`, then compare held-out representative workloads.
Check profile coverage and missing-function warnings. Keep training-only improvements separate
from results on realistic untrained cases. Do not install components or replace shipped profiles
automatically. Sampling and instrumentation profiles are different formats/workflows.

On 2026-11-15, local Rust 1.99.1 supported instrumentation PGO but did not list
`profile-sample-use`; live 1.100 documentation already described it. This is a concrete reason
to inspect the chosen compiler instead of pinning every project to the newest online recipe.

## Benchmark boundaries

`std::hint::black_box` is a best-effort optimization barrier, not a correctness or constant-time
guarantee. Apply it to runtime-like inputs and consume outputs; an already-folded constant cannot
be rescued by wrapping only its result. Verify the compiled work if timing is suspicious.

Use the existing harness. In Criterion, `iter` includes returned-value destruction; batched loops
separate setup, and `iter_batched_ref` can exclude dropping the setup input. Keep that choice
consistent with the real operation. Retaining outputs or large batches changes memory pressure;
creating a runtime or cloning input inside one variant only invalidates the comparison. Use
custom loops for real coordinated work when necessary, without counting setup as a speedup.

Sources: [Cargo profiles](https://doc.rust-lang.org/cargo/reference/profiles.html),
[rustc controls](https://doc.rust-lang.org/rustc/codegen-options/index.html),
[PGO](https://doc.rust-lang.org/rustc/profile-guided-optimization.html),
[cargo-show-asm](https://github.com/pacak/cargo-show-asm),
[Rust layout](https://doc.rust-lang.org/reference/type-layout.html),
[black_box](https://doc.rust-lang.org/std/hint/fn.black_box.html),
[Criterion 0.8.2 timing API](https://docs.rs/criterion/0.8.2/criterion/struct.Bencher.html).
Consult matching versions before applying examples.
