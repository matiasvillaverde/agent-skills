# Zig performance source basis

Original synthesis reviewed 2026-11-15. No upstream scripts, mandatory dependency, blanket
startup-only allocation rule or project style policy was imported. Compiler-sensitive claims
were checked in official tagged source; local Zig was unavailable during research, so those
commands and third-party integrations were not locally compiled or profiled.

- [Official releases](https://ziglang.org/download/), [0.17.1 announcement](https://ziglang.org/news/0.17.1-released/)
  and [language reference](https://ziglang.org/documentation/0.17.1/): version identity, optimization,
  ownership, vectors and illegal behavior. Tagged compiler/stdlib sources linked from the other
  references resolve observed stale API examples.
- [tkersey's Zig skill and references](https://github.com/tkersey/dotfiles/tree/0021ec1b98d171fe9fd5a64e1fbf381fa2d7b381/agents/skills/zig):
  exact-version selection, correctness references and measured profiler evidence; omit its default
  compiler pin. Read the skill plus performance and profiling playbooks.
- [MatthieuMv's Zig performance reference](https://github.com/MatthieuMv/zig-ai-skill/blob/a5f710bfd7b1092ab18c0ecc0d5074f8ec4e9e0b/skills/zig-017-tiger/references/performance.md):
  useful version/lifetime questions; no license file found in reviewed tree, so no prose/code copied.
  Guidance here was written from the independently checked language/compiler contracts.
- [ztracy manifest](https://github.com/zig-gamedev/ztracy/blob/a08122d65f2aede9fd088a512c942acf56735062/build.zig.zon),
  [zBench implementation](https://github.com/hendriknielaender/zBench/blob/f12a2262bcd9d300207890555c577da5e29de453/src/benchmark.zig)
  and [testingx](https://baskingspot.dev/testingx/): scoped compatibility/timing research, not endorsements
  or proof of runtime compatibility. Prefer the project's existing harness.
- [Synthetic folded-stack exporter](https://github.com/zig-utils/zig-benchmarks/blob/ec774cefc370950ec2a3d684beca283e07be3a98/src/flamegraph.zig):
  inspected implementation writes fixed frames and a supplied count; it is not execution sampling.

The shared native profiling guide owns OS/PMU and hardware source links. Report actual tool and
compiler versions, symbols, target coverage and executed checks each time; research-time source
availability does not establish support on the current machine.
