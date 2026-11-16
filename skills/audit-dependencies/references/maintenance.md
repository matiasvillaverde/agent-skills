# Upgrades, removal and owned code

Start with actual direct/transitive and shipped usage. Static import searches miss dynamic
plugins, CLI entrypoints, templates, optional platform features, generated code and build
hooks. Inspect those boundaries before calling a dependency unused. `go.sum` records
checksums; it is not a complete lockfile. A package-manager count is not a shipped-byte,
attack-surface or maintenance metric.

Compare concrete options: remove unused functionality, use the supported standard library,
keep the dependency, update it compatibly, or own a small implementation. Favor the
simplest option that preserves the actual contract. Measure material startup, bundle,
build or runtime savings when those motivate the change. Avoid arbitrary LOC cutoffs or
a universal dependency score.

Before copying, establish permission from the actual license and file provenance. Record
upstream URL/revision, retained notices, local changes and why ownership is preferable in
the existing inventory/notice location. Keep attribution and applicable obligations.
Unknown licensing is unresolved permission to copy, not a security rating. Vendored
fragments remain components for advisory tracking even if scanners no longer recognize
their package name. Own future fixes and compatibility tests. Do not hand-roll crypto,
authentication, complex parsers or locale handling solely to remove a package.

For upgrades, record runtime/compiler/MSRV/ABI/platform constraints and supported release
lines. Read relevant release/migration notes and inspect changed hooks, permissions,
transitive resolution and distribution sources. Prefer a focused compatible change over
an all-at-once latest-version jump. Update manifest and resolution consistently through
the existing approved package workflow; inspect the actual diff, shipped artifact and
affected compatibility tests. Avoid unrelated formatting or generated churn.

Private registry order is not always priority. pip evaluates candidate locations together;
adding a private `--index-url` plus public `--extra-index-url` does not reserve internal
names and can enable dependency confusion. Use the repository's vetted source mapping,
controlled mirror or exact approved artifacts/hashes for its ecosystem, verifying actual
resolver semantics. [pip resolution](https://pip.pypa.io/en/stable/cli/pip_install/).

Vendoring records need to agree with dependency metadata; in Go, inspect `vendor/modules.txt`
and the supported vendor workflow. Do not assume a vendored tree is complete for every
build or that editing it removes upstream tracking obligations.
[Go vendoring](https://go.dev/ref/mod#go-mod-vendor).

Verify removal against real entrypoints, optional features and packaging plus required
gates. Small pure helpers deserve focused contract examples, not a test for each line.
Keep failure recovery/rollback concrete; a lockfile-only edit without a resolution or
compatibility check is not a completed upgrade.

Research reviewed 2026-11-15: [managing-dependencies](https://github.com/andrew/managing-dependencies/blob/e6c13bd7246f13bab6510790ca6378e8660bf50f/skills/managing-dependencies/SKILL.md)
(CC0) usefully prioritizes need/ownership, but its private-index ordering advice conflicts
with pip documentation and its fixed size/age thresholds were excluded.
[secure-dependencies](https://github.com/david-a-wheeler/secure-dependencies/blob/ec00d7a85a7018d49ad144c27fa786061c3a0523/SKILL.md)
(MIT declared in skill; root license lookup unavailable) usefully distinguishes update/new/current
reviews; mandatory AI tiers and detector scores were not adopted. Original synthesis only.
