# Rust performance source basis

Original guidance synthesized on 2026-11-15. No upstream executable helpers, default installs,
benchmark dependencies or automatic host changes are included. Tool examples require the actual
project/host version; source reading is not runtime qualification.

Primary sources and read scope:

- [Cargo profiles](https://doc.rust-lang.org/cargo/reference/profiles.html): workspace ownership,
  optimization, symbols, stripping, LTO. Local Rust/Cargo 1.99.1 help was compared with live docs.
- [rustc codegen](https://doc.rust-lang.org/rustc/codegen-options/index.html) and
  [PGO](https://doc.rust-lang.org/rustc/profile-guided-optimization.html): target/features, frame
  pointers, generation/use workflow and compatibility. Newer web sampling-PGO guidance was not
  offered as supported by the locally installed compiler.
- [cargo-show-asm](https://github.com/pacak/cargo-show-asm): artifact selection, emitted forms,
  missing/inlined functions and wrapper caveat.
- [heaptrack](https://github.com/KDE/heaptrack) and [dhat 0.3.3](https://docs.rs/dhat/0.3.3/dhat/):
  collector/platform boundaries, Rust use, profiler lifetime and perturbation.
- [Tokio Console](https://github.com/tokio-rs/console): root, subscriber and UI documentation;
  prerequisites and task timing. Inspect exact dependency versions before instrumentation.
- [black_box](https://doc.rust-lang.org/std/hint/fn.black_box.html) and
  [Criterion 0.8.2](https://docs.rs/criterion/0.8.2/criterion/struct.Bencher.html): optimization
  barrier limits and timing/setup/Drop boundaries.

Community sources read include
[Mnwa's native measurement/SIMD skill](https://github.com/Mnwa/performance-engineering/tree/1f8c23164f35c4c5868e765753904202ac4fe834/skills/performance-engineering),
[madebyhost's Rust layout/I/O references](https://github.com/madebyhost/rust-performance-skills/tree/2afcbcc2296a658d88cd0816d221679ad84d2170/skills), and
[po4yka's benchmark guidance](https://github.com/po4yka/rust-skills/tree/0d0b9462c8f51532253af6e20458d934b24c8bf7/skills/rust-performance).
Selected ideas were independently synthesized; no source prose/code or numeric acceptance policy
was copied. The shared library's dated research records useful mechanisms and rejected advice;
no community skill is treated as a validated performance oracle. The shared native profiling
reference owns OS/PMU source links. Hardware-specific improvements, unsafe transformations,
PGO training quality and custom allocator visibility still need evidence from the actual target.
