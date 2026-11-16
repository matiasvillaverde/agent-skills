# Research basis

Reviewed 2026-11-15. This is original synthesis, not a bundled community skill or copied manual.
Primary naming/tool sources are linked next to their claims in [platforms](platforms.md) and
[inventory and tools](inventory-and-tools.md); check the project's selected versions at use time.

| Community source read | Useful idea | Deliberate boundary |
| --- | --- | --- |
| [Stencila software-code-review](https://github.com/stencila/stencila/blob/bccab73af0d8c183de38a3e3bf48fe11cbec7ad5/.stencila/skills/software-code-review/SKILL.md) | Learn conventions from peers outside the suspect files; handle generated code separately | Its full correctness/security review and fixed small sample do not establish a complete convention inventory |
| [Intense Visions naming-craft](https://github.com/Intense-Visions/harness-engineering/blob/490335754a80adb7119671ac608c759ea5f40359/agents/skills/claude-code/naming-craft/SKILL.md) | Distinguish mechanical casing from semantic naming quality; use parsed identifiers and report uncertainty | Its TS/JS pipeline, fixed majority threshold, scope-length cutoffs and per-identifier model workflow are not universal requirements |
| [big-code-analysis audit-naming](https://github.com/dekobon/big-code-analysis/blob/ca56098dab67897d17d17e1d19447c9d680b491b/.claude/skills/audit-naming/SKILL.md) | Compare names with actual behavior; distinguish misleading names from mere style; record coverage | Repository-specific vocabulary, mandatory issue creation, audit-state machinery and all-features recipes are not imported |
| [ilia-izmailov conventions](https://github.com/izmailovilya/ilia-izmailov-plugins/blob/064a1153d631bc9377a7a4343ec39bc4b2c37db7/plugins/agent-teams/skills/conventions/SKILL.md) | Ground guidance in concrete local exemplars | Rejected mandatory `.conventions/` scaffolding, copying examples, minority-as-anti-pattern and add-only documentation |

GitHub repository metadata identified Apache-2.0, MIT and MPL-2.0 respectively for the first
three; no license was identified for the fourth. This is a metadata observation, not a complete
license audit. No source text/code was copied and no community setup/tooling was executed.

The main counterevidence is practical: PEP 8 forbids breaking compatibility merely for style;
the C++ guidance preserves imported conventions; typescript-eslint cautions against excessive
strictness; ast-grep distinguishes syntax from semantic analysis. Consequently this skill
requires comparable scopes and concrete effects, not a universal naming score or automated
repository-wide normalization. The survey is bounded and does not establish community popularity
or prove that every language tool can safely rename every consumer.
