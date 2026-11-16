# Rust

Use the pinned toolchain, MSRV, workspace packages, targets and supported features. Build
scripts/proc macros execute code; an offline command is not an execution sandbox.

- Existing `cargo fmt --check`, `cargo check` and Clippy supply different evidence. Preserve
  locked resolution and use offline mode only when dependencies are already available.
- Choose the actual supported default/no-default/feature combinations. `--all-features` can
  enable mutually exclusive backends and does not prove the deployed combination works.
  `--all-targets` on one host does not compile every cross-target platform.
- Favor relevant Clippy correctness/suspicious checks, must-use/error handling and existing
  lint policy. Pedantic/nursery/restriction groups are not a universal quality switch; some
  restriction rules conflict. Keep documented narrow allowances instead of whole-module silence.
- Check schema/serialization compatibility, generated clients/resources, SQL/offline metadata
  and public API commitments through their owners when changed. `cargo check` alone does
  not prove linking, runtime behavior or all conditional code paths.
- Use cargo-audit/cargo-deny or the existing dependency owner for advisories, license/source
  policy and duplicate versions as applicable. These are distinct contracts; record database
  freshness and locked inventory instead of declaring all dependencies safe.
- For unsafe code/FFI/aliasing risks, use targeted Miri or supported sanitizer builds when
  available. Miri's platform/FFI limits and nightly/toolchain requirements matter; do not
  claim it runs arbitrary production workloads. Native sanitizers need executed paths.

Do not create a rustc-private lint plugin for a syntax rule that an existing parser/checker
can express. For symbol or dataflow rules, establish compiler API/toolchain coupling and
maintenance cost before adopting custom infrastructure. Use focused compile-fail fixtures
for compiler-enforced public contracts where they add unique value.

Primary sources: [Clippy lint catalog](https://clippy.rust-lang.org/master/index.html),
[Cargo check](https://doc.rust-lang.org/cargo/commands/cargo-check.html),
[Miri supported behavior and limits](https://github.com/rust-lang/miri).
Match documentation to the project's pinned toolchain; the master catalog is not the
installed lint set.
