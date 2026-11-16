# TypeScript and JavaScript

Read package scripts, lockfile, workspace boundaries, tsconfig inheritance, framework
generation and the installed lint configuration. Use the package manager's existing local
binary path; do not let a convenience command download the latest tool implicitly.

| Risk | Useful existing check |
| --- | --- |
| Type/contract drift | Project/framework typecheck with generated types and references; strict-null and indexed/optional access checks where already configured or deliberately adopted |
| Dropped async work | Type-aware promise/misused-promise rules; verify actual Promise type context and intentional fire-and-forget policy |
| Accidental unsafe typing | Selected unsafe assignment/call/return rules or boundary schema checks; avoid casting external data merely to satisfy types |
| UI defects | Existing hooks, accessibility and framework lint rules; runtime keyboard/assistive testing still needed |
| Imports/architecture | Existing dependency-boundary/cycle rules and export/package validation; resolve aliases and type-only imports correctly |
| Build/resource drift | Generated schema/client/catalog checks, supported bundler build and missing assets; compile all affected workspace consumers where required |
| Security | Reviewed source/dataflow rules for actual sources/sinks, and resolved dependency audit separately |

Typed ESLint rules need the appropriate TypeScript project context and cost more than
syntax-only lint. Inspect the effective config for `.ts`, `.tsx`, JS and framework files;
an excluded file or parser-service error is not clean coverage. Preserve an existing Biome
workflow where it covers the requirement; introduce another linter only for a concrete gap.

Transpilers can erase types without checking them. A passing bundle or syntax parser cannot
establish that types passed. Conversely, types do not validate untrusted runtime input.
Test runtime schemas with malformed and legitimate data when changing that boundary.

For new rules, use ESLint's supported custom-rule/RuleTester interfaces; TypeScript parser
services when type identity matters. Do not import unstable core-rule internals. Inspect
autofix results for changed evaluation order and comments; require a focused valid/invalid
fixture and an idempotent fix. Avoid a universal no-`any`/complexity quota without a product
reason and migration plan.

Primary sources, checked 2026-11-15: [typed linting](https://typescript-eslint.io/getting-started/typed-linting/),
[ESLint custom rules](https://eslint.org/docs/latest/extend/custom-rules).
