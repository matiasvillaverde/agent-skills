# Author a useful custom rule

Start with a recurring concrete defect or explicit invariant. Write down the bad behavior,
safe alternative, scope, owner and actionable diagnostic. If an existing compiler, schema
or selected linter rule already enforces it, configure that owner instead of duplicating it.

Choose the smallest analysis that establishes the claim:

| Needed fact | Suitable approach |
| --- | --- |
| Literal spelling or simple file format | Bounded text/schema check with clear exclusions |
| Syntax shape | Existing AST framework, SwiftSyntax, ast-grep or language-aware Semgrep where supported |
| Actual import/symbol/type identity | Compiler/type-aware ESLint, `go/analysis`, Clang or another existing semantic extension |
| Untrusted value reaching a sink | Reviewed dataflow/taint analysis with explicit source, propagation, sanitizer and sink models |

Do not label a structural match an exploit or assume any `validate()` function sanitizes
every context. Confirm engine/language/edition limits, especially cross-file flow, macros,
generated code and foreign-language boundaries. Rules and configurations are executable
inputs in some tools: review them before loading or uploading source.

Build a minimal fixture set around distinct risks: the actual bad case, its legitimate
neighbor, and a relevant alias/shadowing/escaping/control-flow variant if it can defeat the
rule. Include configuration/parse failure where the gate could silently skip input. Avoid
dozens of cosmetically varied cases or one giant language-by-pattern matrix.

Use the framework's rule test runner. Semgrep `ruleid`/`ok` annotations check expected
findings/non-findings, and `.fixed` fixtures check fixes. Pending/TODO annotations are not
passing coverage. ESLint RuleTester, Go analysistest and existing compile-fail harnesses
serve analogous purposes; do not create an additional runner without need.

Run the rule on a bounded representative real source set before promotion. Inspect false
positives and actual selected/parsed files; no matches alone says little. Measure cost if
it affects ordinary CI. Prefer a precise finding and narrow documented limitation over
expanding a heuristic until every unusual program fails.

Test any autofix for preserved evaluation order, escaping, comments and behavior. Rerunning
the fix should make no further edits. For semantic changes, provide a suggestion rather
than an unsafe automatic rewrite. Wire failure states into the existing gate, with a
reviewed pinned tool/rule version and scoped exceptions. Keep rule source, tests and
configuration at the owning product/tool location.

Primary sources, checked 2026-11-15: [Semgrep rule tests](https://semgrep.dev/docs/writing-rules/testing-rules),
[ESLint extension API](https://eslint.org/docs/latest/extend/custom-rules).
