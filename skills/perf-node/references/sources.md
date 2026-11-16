# Research basis

Reviewed 2026-11-15. Original synthesis, no community code or prompt text copied.

- [Lanterna profiler skill](https://github.com/arkerone/lanterna/blob/ee48e5891d5ba7f7eb0f3e3e17ed811da3602ca9/skills/lanterna-profiler/SKILL.md) (MIT): useful separation of CPU/async/heap evidence and map coverage. Tool-specific mandatory reports, automatic package execution and heuristic findings as proof were excluded.
- [Performance profiler](https://github.com/alirezarezvani/claude-skills/blob/08cd8a9fc86cc370e2c0d448e8171fbcfdbc5a30/engineering/skills/performance-profiler/SKILL.md) (MIT): broad diagnostic branches. Static risk scripts are not measurements, and fixed query-duration thresholds do not define every service's performance budget.
- Primary Node runtime, process, stream, worker and diagnostics references are linked at their point of use. The research observed Node documentation 26.13.1 and local Node 26.13.0; these are a dated observation, not a permanent required version.

Recheck maintained tools, supported flags, sampling semantics and actual runtime deployment
before execution. No profiler is universally zero overhead. Framework profiling, native
OS profiling and service traces complement one another; neither a local microbenchmark
nor a source-only review proves production performance.
