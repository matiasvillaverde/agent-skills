# Rust build research basis

Reviewed 2026-11-15. Original synthesis; no community prompt or executable code imported.
Primary mechanisms and version limits are linked in the three focused references. Local
research observed Rust/Cargo 1.99.1 while rolling documentation already described 1.100;
recheck the actual project's toolchain rather than treating this review date as compatibility.

| Community / firsthand original | Adopted lesson and limit |
| --- | --- |
| [po4yka build-time reference](https://github.com/po4yka/rust-skills/blob/0d0b9462c8f51532253af6e20458d934b24c8bf7/skills/rust-performance/references/build-time-optimization.md) (BSD-3-Clause) | Measure generic/target/cache work. Synthetic IR reductions are not product latency gains; avoid blanket incremental or dependency-optimization prescriptions. |
| [rust-ci-performance](https://github.com/russellromney/rust-ci-performance/blob/8a824ea4e908d08c7a6de8d4fe5f58c53c6d71c2/SKILL.md) (MIT) | Many test binaries and expensive links can dominate despite compiler-cache hits. Do not inherit global flags, unverifiable OS-specific gains or blanket removal of checks. |
| [Rejected rust-build-times candidate](https://github.com/mohitmishra786/low-level-dev-skills/blob/d0d0a13d4e3caec7afb2d647a1fffdb7cb1ee058/skills/rust/rust-build-times/SKILL.md) (MIT) | A relevant name is insufficient. Rejected unsupported commands, universal speedup percentages, all-cores prescriptions and the false equation of one crate with one CPU. |
| [rust-analyzer / Matklad](https://matklad.github.io/2021/09/04/fast-rust-builds.html) | Broad useful dependency graphs and change locality; old nightly command syntax is historical. |
| [TiKV compilation units](https://www.pingcap.com/blog/rust-huge-compilation-units/) | Crate splits can improve partial builds while increasing full-build work. |
| [Zed settings redesign](https://zed.dev/blog/settings-ui) | Compilation-friendly decentralization can lose clarity and correctness; architecture quality remains a constraint. |
| [Feldera generated DAG](https://www.feldera.com/blog/cutting-down-rust-compile-times-from-30-to-2-minutes-with-one-thousand-crates) | Stable generated boundaries enabled reuse in a particular dataflow workload. Not a recommendation for thousands of hand-maintained crates. |
| [Zed linker experiment](https://github.com/zed-industries/zed/pull/37717) | Measure fresh builds, edited builds, runtime and tests separately. Old versions and conflicting headline/table figures prevent universal gain claims. |

No exhaustive catalog or comparative skill-effectiveness claim is made. Reuse the workflow,
not another team's timings, crate counts or hardware budgets. General collection searches
mostly found runtime/CI guidance rather than specialized local-build diagnosis.
