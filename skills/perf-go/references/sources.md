# Source basis and version boundaries

Research checked 2026-11-15. These are original instructions synthesized from selected primary
documentation and reviewed community workflows, not an imported skill pack or upstream endorsement.
No community code, hooks or expressive instruction text was copied or executed.

## Toolchain snapshot

The official [download feed](https://go.dev/dl/?mode=json) and
[release history](https://go.dev/doc/devel/release) list **Go 1.27.4** and the maintained older
line **1.26.11**, both released 2026-11-10. The research machine has Go 1.27.4 darwin/arm64.
Recheck these sources when currency matters; retain the project's actual version and target.
Module/workspace directives and automatic toolchain selection can differ from the shell binary.
Read [toolchain selection](https://go.dev/doc/toolchain) before interpreting a version mismatch.

| Change | Relevance and boundary |
| --- | --- |
| Go 1.24 `testing.B.Loop` | Benchmark-loop API; Go 1.26 removed its earlier inlining restriction. Keep compiler version and benchmark structure comparable. |
| Go 1.25 container-aware GOMAXPROCS | Linux cgroup-aware policy and updates depend on module compatibility/defaults and explicit overrides. |
| Go 1.25 flight recorder / synctest | Version-gated diagnostics/testing; check recorder concurrency, memory and supported test behavior. |
| Go 1.26 Green Tea GC default | Collector changes can affect comparisons; published GC improvements are not universal application speedups. |
| Go 1.27 goroutine leak profile | Generally available, with documented detection gaps; no experiment is needed on this line. |
| Go 1.27 allocation / JSON changes | Small-object codegen/runtime changes; `encoding/json` is v2-backed while preserving v1 semantics except possible error text. New v2 APIs have different defaults; do not silently migrate application behavior. |

Primary release references: [1.24](https://go.dev/doc/go1.24), [1.25](https://go.dev/doc/go1.25),
[1.26](https://go.dev/doc/go1.26), [1.27](https://go.dev/doc/go1.27).
Specific runtime/profile/GC and instrumentation APIs are linked beside their guidance. Installed
1.27.4 source/help corroborated selected pprof, trace, metrics, HTTP and benchmark semantics.

## Community comparison

The strongest useful contributions were investigation breadth, symptom-driven tool selection,
reproducible benchmarks and bounded telemetry overhead. These immutable revisions identify the
reviewed material; primary API contracts override inaccurate or outdated community examples.

- [Samber Go performance](https://github.com/samber/cc-skills-golang/blob/d68d80aec298e1b74b37c2a472c002b5217248b3/skills/golang-performance/SKILL.md): broad runtime/service map; MIT. Avoid blanket ownership/GC tuning rules.
- [AeonDave performance](https://github.com/AeonDave/malskill/blob/f0c978690250b59a1068eb9ecfabe2ea0935c1e6/coding/golang-performance/SKILL.md): compact symptom routing. MIT declared in skill frontmatter; no root license found. No text/code copied.
- [Eduardo Go performance review](https://github.com/eduardo-sl/go-agent-skills/tree/e25b517bbd0c11db35f75a83a14f18848c1abdb0/skills): useful workload/benchmark detail; MIT. Correct confidence-interval language and reject OOM guarantees.
- [OllyGarden OTel Go](https://github.com/ollygarden/opentelemetry-agent-skills/blob/eac2a29a7979f10eb429092b2655f28b85129e6c/skills/otel-go/SKILL.md): telemetry queues, overhead and lifecycle; Apache-2.0. Match actual installed modules instead of automatic latest installs.

Also reviewed Gopher Guides, ECC, Jeffallan, Dash0 and Curiositech. Excluded mandatory CPU-first
routing, fixed speedup/coverage thresholds, universal pool sizes, AlwaysOn sampling requirements,
incorrect block-rate units and unsupported stack-allocation claims. Curiositech's repository is
BSL 1.1 with commercial restrictions; it was comparison evidence only. Full provenance/query
and qualification records live in the shared library's dated research/rollout documentation.

## Scope of evidence

Source review establishes tool/API guidance, not a product performance gain. Native execution,
profiler availability and instrumentation overhead must be verified on each relevant deployment
target. OTel SDK signal stability, continuous-profiler features and eBPF/build instrumentation
support differ; consult their current primary docs and project pins. Do not assume a provider's
CPU overhead claim, successful profile upload or clean diagnostic snapshot proves application health.
