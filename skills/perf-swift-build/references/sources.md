# Swift build research basis

Reviewed 2026-11-15. Original synthesis; no community prompt or code imported. Primary Apple,
Swift, Tuist and parser sources are linked in the focused references. Recheck documentation
against the selected versions; a live guide is not proof an installed CLI supports its recipe.

| Original community / firsthand source | Adopted lesson and deliberate limit |
| --- | --- |
| [Axiom build-performance](https://github.com/CharlesWiltgen/Axiom/blob/ffafd3b3e0dbaaa60b753ca4a835ae6603b873e1/axiom-codex/skills/axiom-build/skills/build-performance.md) and [optimize-build](https://github.com/CharlesWiltgen/Axiom/blob/ffafd3b3e0dbaaa60b753ca4a835ae6603b873e1/axiom-codex/skills/axiom-optimize-build/SKILL.md) (MIT) | Inspect effective settings and critical work. Reject numerical gain promises, blanket settings, implicit package execution and clean/no-op/cache confusion. |
| [Tuist compare-builds](https://github.com/tuist/agent-skills/blob/5da5c0f67df8277de699d64782a3810f9d30ee1b/skills/compare-builds/SKILL.md) (MIT) | Match source, scheme/configuration, compiler, machine and scenario before task/cache comparison. Percent thresholds are triage, not significance. |
| [Tuist compare-cache-runs](https://github.com/tuist/agent-skills/blob/5da5c0f67df8277de699d64782a3810f9d30ee1b/skills/compare-cache-runs/SKILL.md) and [compare-generations](https://github.com/tuist/agent-skills/blob/5da5c0f67df8277de699d64782a3810f9d30ee1b/skills/compare-generations/SKILL.md) (MIT) | Explain direct invalidation and dependency cascades. Nearly duplicate methods are not independent corroboration; Git-diff inference is not measured target telemetry. |
| [Airbnb Dev Apps](https://medium.com/airbnb-engineering/designing-for-productivity-in-a-large-scale-ios-application-9376a430a0bf) (2021) | Focused feature hosts/workspaces can reduce build/index scope. Its Buck architecture, module counts and reported timings are not universal requirements. |
| [Uber Poet](https://www.uber.com/us/en/blog/uber-poet/) (2019) | Test structural hypotheses before expensive refactors; compare equal reachable work. Historical Swift/Xcode settings are not current defaults. |

Compiler timing, pipeline timing, parser categories and runtime profiling answer different
questions. No exhaustive census, universal best configuration or product speedup is claimed.
Use these sources for mechanisms and counterexamples; measure the actual repository's local
iteration before accepting a change.
