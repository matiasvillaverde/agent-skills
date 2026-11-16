# Research basis

Reviewed 2026-11-15. Original synthesis; community prompt/code was not copied.

- [Python profiling](https://github.com/fgmacedo/agent-skills/blob/37d8a4d29e89dba432618237d29231b76dc79431/skills/python-profiling/SKILL.md) (MIT): adopted question-driven profiling and repeated measurement; excluded CPU-first mandates, universal round counts, disabled-GC defaults and profiling-as-benchmark claims.
- [py-perf](https://github.com/stevenke1981/python_skills/blob/60198993a133d8a9b994bdf7a5bbbaf66340c14d/py-perf/SKILL.md) (license not established from root LICENSE lookup): useful interpreter, native-extension, async and free-threading distinctions; research only.
- [Performance profiler](https://github.com/alirezarezvani/claude-skills/blob/08cd8a9fc86cc370e2c0d448e8171fbcfdbc5a30/engineering/skills/performance-profiler/SKILL.md) (MIT): broad comparison only; static source rules cannot establish measured performance.
- Official Python 3.15 documentation, pyperf and Memray sources are linked where used. Python 3.15.2 was observed locally; this does not require upgrading a deployed runtime.

Refresh profiler compatibility, command flags and build semantics for the target. Official
claims of very low overhead are not a measured guarantee for the user's workload.
