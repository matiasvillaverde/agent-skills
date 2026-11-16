---
name: review-conventions
description: Find missing, conflicting or misleading codebase conventions across filenames, symbols, domain vocabulary and boundary patterns. Use for a scoped consistency audit or focused normalization with evidence from local code and platform rules.
---

# Review codebase conventions

Make similar concepts predictable without flattening meaningful differences. Audit requests
produce findings, not edits. For authorized cleanup, change a coherent set with its consumers;
preserve product behavior and compatibility. Zero findings or a documented exception is valid.

## Establish what governs this scope

Read the instruction chain, owner guides, manifests, generated-file markers and effective
formatter/linter configuration. Identify language, framework, target, public boundary and
subtree before deciding what is inconsistent. Preserve dirty work, submodule boundaries and
vendor ownership. A repository-wide majority is not authority over an independently owned package.

Use [inventory and tools](references/inventory-and-tools.md) for a shallow `tree`, `rg --files`,
tracked-file reconciliation and focused symbol searches. Read callers and representative peer
files outside the suspected outliers. Separate production, test, generated, vendor and legacy
surfaces. A filtered tree or regex match is a lead, not complete semantic coverage.

Classify a proposed rule as a language/framework requirement, an explicit local decision, an
observed local pattern, or a new recommendation. Record a legitimate exception when it explains
the difference. Resolve conflicting instructions/configuration before calling one side wrong;
do not silently promote an inferred convention to policy.

## Compare like with like

Read [convention categories](references/categories.md) to choose the useful dimensions: paths,
symbols, domain terms, API/data contracts, errors, observability, tests and documentation.
Read only the relevant [platform guidance](references/platforms.md). Distinguish language rules
from ecosystem advice, framework discovery names and a company's optional house style.

For each material candidate, inspect its declaration, use sites and a comparable exemplar.
Explain the practical confusion: misleading effect/ownership, inconsistent domain meaning,
ambiguous units, discovery failure or avoidable reader search. Different spellings can represent
different operations; do not merge `fetch`, `load` and `get` without comparing their contracts.
Use types and context before adding prefixes/suffixes. A short local index or familiar domain
abbreviation is not a defect merely because it is short.

For a larger audit, sample by owner, language and role, then expand around demonstrated drift.
State selected files/symbols, exclusions and whether coverage is sampled or complete. Quantify
only what was actually counted with a meaningful denominator. Check counterexamples and planned
migrations; frequency alone does not make the minority an anti-pattern. Missing documentation
is a convention gap only when a consequential choice is otherwise unclear or keeps diverging.

## Report or make the smallest useful correction

Give each finding a location, category, governing evidence, concrete consequence, smallest remedy
and compatibility cost. Separate required fixes, useful consistency improvements and optional taste;
do not inflate cosmetic issues into security/correctness failures. Consolidate repeated instances
of one problem. A compact rule/example/exception table is enough when durable guidance is needed.

For authorized renames, prefer a project-aware symbol rename with a reviewed edit set. Inspect
exports, serialization keys, reflection/selectors, database names, routes, resources, test discovery,
external consumers and case-sensitive paths. Source references are not all consumers. Preserve
established wire names through the existing mapping where appropriate; do not add aliases or
compatibility layers without an actual compatibility need. Edit generators, not generated output.

Run affected owning checks and meaningful consumer/serialization/resource checks. Verify the
intended target/test inventory and search remaining old names, distinguishing compatibility and
history from missed edits. Formatter success is not semantic rename evidence. If a stable rule
deserves automation, prefer the existing compiler/linter; qualify a narrow check with a real
violation and a legitimate exception. `deterministic-checks` can help when available.

Use `organize-repo` for substantial file moves, `maintain-docs` for documentation reconciliation,
and `design-codebase` for architectural changes when available; this audit does not require them.
Keep any instruction update in the existing owner, with nested `AGENTS.md` only for a durable
subtree-specific difference. Do not generate a second conventions wiki or instructions per folder.
Report actual changes/checks and unresolved scope. Remove only task-created disposable outputs.
[Research and provenance](references/sources.md).
