---
name: deterministic-checks
description: Run, improve or author compiler, type, lint, schema, generated-output and analysis checks across Swift, TypeScript, Go, Rust, Python, C/C++, CUDA and Zig. Use to turn concrete defects into useful existing gates with verified coverage and low noise.
---

# Deterministic checks

Build useful coverage around actual failure modes. Prefer a reliable existing check to
another scanner that reports the same thing; add distinct checks where they close real gaps.

For naming or convention rules, first establish the owning scope and intentional exceptions.
The available `review-conventions` can supply that evidence; frequency alone does not define
a requirement. Enforce an agreed invariant with the existing language-aware checker.

## Discover the owner and missing coverage

Read repository instructions, build/check entrypoints, manifests, lockfiles, compiler
versions and existing configuration. Identify the language, targets/features, changed
surface and concrete defect classes. Inspect hooks/plugins before running untrusted builds.
Use trusted local fixtures for intentional defects; do not execute them against live data.

Find the project’s authoritative check commands and profiles, and inspect their planned
scope before execution. Reuse its existing local or hosted CI instead of adding a parallel
runner. Preserve the localization owner’s source coverage and debt contract.

Select checks from the relevant reference rather than enabling every rule:

- [Swift](references/swift.md)
- [TypeScript/JavaScript](references/typescript.md)
- [Go](references/go.md)
- [Rust](references/rust.md)
- [Python](references/python.md)
- [C/C++, CUDA and Zig](references/native.md)
- [Custom rules](references/rules.md), only for a concrete invariant existing tools cannot express.

Keep the evidence types separate:

| Check | Establishes within its actual coverage |
| --- | --- |
| Compiler/types | Syntax, type and compiler-enforced language constraints for compiled targets/configurations |
| Formatter/lint/static analysis | Formatting or selected structural/semantic rules, with parser and rule limits |
| Schema/catalog/generated output | Data shape, declared cross-field constraints or reproducibility against an owning source |
| Sanitizer/race detector | Supported runtime faults on exercised paths; schedules and inputs still matter |
| Dependency/secrets analysis | Advisory or credential evidence with inventory/database scope; separate from source correctness |

## Run enough checks to answer the task

Start with applicable existing gates. Use the actual project context for type-aware checks;
single-file parsing or bundler transpilation is not a project build/type check. Respect
supported feature combinations, generated code and target-specific branches. Scope fast
feedback to changed files only when the analyzer's semantics permit it; keep required wider
checks and measured deeper cadence. Avoid automatic tool migrations or duplicate formatters.

Capture tool/rule/config revisions, commands, analyzed files/targets, exclusions, diagnostics,
exit status and duration. Treat zero selected files, skipped targets, parser errors, missing
rules/databases and timeouts as incomplete, even if the process exits zero. Preserve exit
codes through wrappers/pipelines; warning output alone may not fail a gate. Use structured
output where available and keep raw source-bearing reports private.

For a new/changed gate or unfamiliar configuration, verify a small intentional failing case
and a nearby legitimate case in an isolated fixture. Exercise a relevant configuration or
coverage failure too. Existing qualified checks need not be re-proven for every ordinary
code edit. New tests should guard independent behavior, not mirror implementation or form
a large language-by-rule matrix.

## Improve the gate without creating noise

Fix the actual defect, then rerun the affected checks on final files. Prefer narrow,
actionable rules with known false-positive limits. Explain each exception with its scope
and reason; do not silence whole folders, expand debt or weaken required checks to get green.
Autofix only where behavior is preserved; inspect the diff and verify it is stable on rerun.

When security boundaries are the task, use the existing `test-security` workflow if available;
use `audit-dependencies`/`scan-secrets` for their specific inventories. Do not upload source,
enable hosted scanning or install an entire rule pack under an ordinary local check request.
Advisory results depend on a changing database: record its freshness with the resolved inputs.

Report checks and defects actually demonstrated, remaining scope gaps, exceptions and cost
when measured. A clean compiler, scanner or sanitizer is bounded evidence, not product
qualification, security certification or proof that all behavior is correct.
