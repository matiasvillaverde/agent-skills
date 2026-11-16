# Rust source, graph, parallelism and prevention

## Remove avoidable work

Inspect critical-path crates, reverse dependencies, change frequency and feature propagation.
Prefer small stable interfaces between real responsibilities. Splitting a crate into a long
serial chain does not expose independent work; tiny crates add overhead. Cargo must still have
an acyclic graph. A source module and a separately compiled crate are different boundaries.
[rust-analyzer's build experience](https://matklad.github.io/2021/09/04/fast-rust-builds.html),
[TiKV compilation-unit tradeoffs](https://www.pingcap.com/blog/rust-huge-compilation-units/).

Reduce dependencies or features only after checking supported consumers, cfg combinations,
runtime registration and build-time use. Resolver v2 separates some feature contexts; unifying
features solely for reuse can mask a missing declaration or expand product behavior.
[Feature resolution](https://doc.rust-lang.org/cargo/reference/resolver.html#feature-resolver-version-2).

Build scripts must declare real file/environment inputs, write within `OUT_DIR` and retain
correct invalidation. That directory can persist across invocations. Avoid rewriting generated
output when content is unchanged; do not suppress required tracking. Test an unchanged repeat
and a changed real input. Scope expensive generators to their actual consumers.
[Build scripts and change detection](https://doc.rust-lang.org/cargo/reference/build-scripts.html#change-detection).

For heavy macro expansion or LLVM work, inspect expansion/IR with already available compatible
tools. Nightly macro statistics and cargo-llvm-lines can locate volume, not prove time savings.
A thin generic wrapper around a concrete heavy implementation can reduce instantiations when
semantics permit. Avoid blanket bans on generics, derives, async or iterators; dynamic dispatch
and erased types can change runtime behavior and maintainability.
[Compile-time investigation](https://nnethercote.github.io/perf-book/compile-times.html).

Many integration test targets can make linking expensive even when tests execute quickly.
Consolidation is conditional: preserve distinct cases, fixtures, process isolation, discovery
and failure attribution. Do not prune assertions or bypass tests to reduce executable count.

## Use cores where the graph permits

Cargo already defaults its job budget to logical CPUs and coordinates rustc with a jobserver.
Native parallel work launched by a build script should participate rather than create another
independent all-cores pool. Check memory, links, I/O, editor work and container/host limits before
tuning a few useful job budgets. More occupied cores are not a success metric.
[Jobserver contract](https://doc.rust-lang.org/cargo/reference/build-scripts.html#jobserver).

Compiler frontend, codegen and linker parallelism are different. At Rust 1.100, newer rustc
`--jobs-frontend`/backend/linker controls remain unstable despite appearing in ordinary online
documentation; older nightly recipes use `-Zthreads`. Verify the selected compiler's support.
Historical parallel-frontend results include regressions and extra memory, not universal gains.
[Release-tagged controls](https://github.com/rust-lang/rust/blob/1.100.0/compiler/rustc_session/src/config.rs),
[historical experiment](https://blog.rust-lang.org/2023/11/09/parallel-rustc.html).

Inspect rust-analyzer/watchers before adding another checker. Align meaningful targets/features
and flags. Separate target directories can reduce lock contention but duplicate compilation and
storage. Narrowing editor checks must retain diagnostics for the selected work; do not simply
disable checking or automatically change global editor settings.
[rust-analyzer configuration](https://rust-analyzer.github.io/book/configuration.html).

## Checks that prevent a demonstrated regression

Use existing format/check/Clippy gates with explicit target/feature scope. Clippy is not a
compile-time profiler; avoid enabling its entire restriction group. On Cargo >=1.97, the
documented `CARGO_BUILD_WARNINGS=deny` policy can avoid cache churn from toggling warning flags;
verify its scope and the owner's policy before replacing a command.
[Clippy usage](https://doc.rust-lang.org/clippy/usage.html),
[Cargo warning policy](https://doc.rust-lang.org/cargo/reference/config.html#buildwarnings).

Target useful dependency checks: unwanted duplicate versions can use Clippy's
`multiple_crate_versions` with justified exceptions. Cargo 1.100 adds an unused-dependency
lint; earlier Cargo lacks it, and target selection, unchecked dev-dependencies and transitive
feature use limit the finding. Verify actual consumers before deletion. Keep check-cfg and
generated cfg declarations when simplifying feature/platform code.
[Cargo lint limits](https://doc.rust-lang.org/cargo/reference/lints.html#unused_dependencies),
[release evidence](https://blog.rust-lang.org/2026/11/12/Rust-1.100.0/),
[check-cfg](https://doc.rust-lang.org/rustc/check-cfg.html).

For a proven generator/freshness defect, a focused no-op and changed-input check is more useful
than a file-length rule. Keep a small representative edit benchmark when it can prevent a
recurrence; calibrate timing budgets to workload/hardware instead of treating milliseconds as
a deterministic lint. Never prescribe a maximum crate count, function size or generic count
as a substitute for observed compiler work.
