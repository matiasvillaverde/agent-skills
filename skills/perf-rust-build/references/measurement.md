# Measure and explain Rust build work

## Capture the right scenario

Use the actual package/target/profile/features and the repository's existing command. Separate
outer command elapsed time from Cargo's reported build phase and test execution. Warm each
configuration before comparing edits: changing flags, wrappers or profiles itself invalidates
artifacts. A source touch is a freshness experiment, not a representative code edit. Keep the
baseline source and edit reproducible; do not reset unrelated working changes.

These are command shapes; substitute inspected package/target names and preserve required flags:

```sh
cargo check -p PACKAGE --lib --timings
cargo build -p PACKAGE --bin APP --timings
cargo test -p PACKAGE --test INTEGRATION --no-run --timings
CARGO_LOG=cargo::compiler::fingerprint=info cargo build -p PACKAGE --bin APP
cargo tree -d
cargo tree -e features -i DEPENDENCY
```

Inspect the report path printed by Cargo instead of hardcoding its internal output layout.
Plain `--timings` is the current portable form; old `--timings=json` recipes no longer apply
to current Cargo. `-Zsection-timings` and `-Zbuild-analysis` are nightly options as reviewed
2026-11-15, not requirements. Build analysis can persist sessions/rebuild reasons; do not assume
ordinary stable builds already recorded that history.
[Timings](https://doc.rust-lang.org/cargo/reference/timings.html),
[versioned unstable options](https://github.com/rust-lang/cargo/blob/3acc79c0c841844675bc53a605922dbfc441e750/doc/book/src/reference/unstable.md).

Cargo's lanes distinguish running work, work waiting for a job slot and work blocked by
dependencies. They do not show all threads within rustc. Do not add overlapping durations,
interpret one active crate as one core, or equate a codegen/IR count with elapsed time. Correlate
the limiting path with CPU, memory pressure/swap, I/O and competing processes when relevant.
Use native process profiling only for a question the build timeline cannot answer.

## Catch unwanted rebuilds while they happen

Capture fingerprint logs during the surprising build; use `-vv` for exact invocations when
needed. Logs can expose source paths, commands and environment values, so keep them private
and summarize only relevant redacted evidence. Do not clean first and erase the useful state.
[Cargo FAQ](https://doc.rust-lang.org/cargo/faq.html#why-is-cargo-rebuilding-my-code).

Check changed feature/package selections, profile/target flags, build-script inputs, timestamps,
rewritten generated files, deleted outputs and lock contention. A missing watched input can
force recurring work. Cargo freshness, rustc incremental reuse and compiler-cache reuse are
different layers. Host build scripts/proc macros and target code may require separate builds;
an explicit host-equivalent `--target` still changes configuration separation.
[Build cache](https://doc.rust-lang.org/cargo/reference/build-cache.html).

`cargo tree -d` shows duplicate versions, not every repeated build unit. A single version can
be compiled for different features, roles, profiles or architectures. Read reverse feature
edges and actual timing units together before concluding a duplicate can be removed.
[Cargo tree](https://doc.rust-lang.org/cargo/commands/cargo-tree.html).

## Inspect an expensive crate only as needed

A compatible installed nightly can provide `-Zself-profile`; measureme reports query self time,
counts, blocked/incremental-load time and query-cache activity. Match analyzer and file format.
Query-cache hits are not sccache hits. Scope profiling to the expensive crate first and confirm
any improvement on the supported project toolchain afterward. Do not overwrite existing
RUSTFLAGS or install nightly just to follow an example.
[Compiler profiling](https://rustc-dev-guide.rust-lang.org/profiling.html),
[measureme interpretation](https://github.com/rust-lang/measureme/blob/d3d4cac8b18d53b55e6d5425371a4422c9d83c86/summarize/README.md).

Build/test/lint are separate endpoints: `check` skips final codegen/linking; `test --no-run`
builds executables; execution adds fixture/runtime cost. A test-name filter alone does not avoid
compiling other selected targets. Record package and target selection, discovered tests and
required doctests when reducing local work.
[Check](https://doc.rust-lang.org/cargo/commands/cargo-check.html),
[test selection](https://doc.rust-lang.org/cargo/commands/cargo-test.html).
