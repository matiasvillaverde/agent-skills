# Source and adaptation notice

Reviewed and modified on 2026-11-13 for the shared personal skill library.
Original local instruction prose informed by the following pinned sources; this
is not an unmodified upstream installation or an upstream endorsement.

- [CharlesWiltgen/Axiom / axiom-codex/skills/axiom-profile-performance](https://github.com/CharlesWiltgen/Axiom/blob/ffafd3b3e0dbaaa60b753ca4a835ae6603b873e1/axiom-codex/skills/axiom-profile-performance/SKILL.md), MIT.

Changes:
- Standalone Instruments/xctrace workflow without xcprof or missing plugin references.
- Explicit target hardware, cold/warm modes, matching symbols, export coverage, retention and absolute performance.
- Expanded on 2026-11-14 with original workflow prose covering the 63 locally discovered instruments,
  17 portable capture recipes, a scoped xctrace command helper, public Apple references and local
  package-documentation pointers. See [source review](references/sources.md). This addition does
  not redistribute Apple's native template archives or package documentation.
- Added original acceptance criteria for all 17 modes, product/UI invariants, relevant public
  API review, version-aware source/assembly investigation and a hardware reference map. Public
  sources and access limits are recorded in the source review; no proprietary manuals are bundled.
- Linked official Apple CPU-guide access and selective-reading guidance; the PDF remains
  outside the distributed skill.
- Added original Metal replay/kernel investigation and device regression-testing references,
  grounded in Apple documentation and inspected CLI help; production MetricKit analysis is a
  separate original `perf-apple-production` skill with an optional Datadog/Pup reference.

The applicable upstream permission and copyright text is retained in [LICENSE](LICENSE).
No upstream executable, plugin, hooks, bundled profiler or missing companion skill is included.
Platform tools are runtime requirements to inspect when applying the skill.
