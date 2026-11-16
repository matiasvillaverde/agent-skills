# Write only what helps the reader

## Choose the document's job

Use [Diátaxis](https://diataxis.fr/how-to-use-diataxis/) to distinguish learning, doing,
lookup and explanation. Improve the current material in small steps; do not generate four
empty sections or force every release note, index or mixed landing page into one category.

| Surface | Keep | Remove or relocate |
| --- | --- | --- |
| README / entrypoint | Purpose, supported starting path, one useful example, links to owners | Full API inventory, implementation tour, duplicated setup procedures |
| How-to / setup | Prerequisites, ordered actions, expected outcome, relevant failure path | Unrelated history, several competing ways to perform the same ordinary task |
| Reference | Exact contracts, units, defaults, bounds, compatibility and errors | Repeated tutorials or source-derived signatures maintained by hand |
| Explanation / decision | Why, constraints, consequential alternatives and tradeoffs | Session narration, abandoned trivia; preserve accepted decision history |
| Runbook | Trigger, safe actions, observable success and stop/escalation conditions | Generic troubleshooting lists, copied dashboards and raw incident logs |

Begin with the action or answer. Name actors and objects; replace vague pronouns and promotional
adjectives with concrete facts. Cut repetition without removing necessary qualifications.
[Google's technical-writing guidance](https://developers.google.com/tech-writing/one/short-sentences)
supports focused sentences and direct verbs; it does not establish a numeric prose quality gate.
Use tables for lookup and diagrams only when relationships are materially clearer. Check actual
rendering and provide useful text equivalents when changing visuals.

## A runbook must work under pressure

Start from the actual owner, service, environment and operational command. A useful procedure
makes the following clear, using only the sections needed for this task:

- What symptom or operation it covers, when it applies and who owns escalation.
- Preconditions: scope/account, access, tools, current directory and required recovery state.
- The next action, expected observation and branch if the observation differs. Mark placeholders;
  never invent a flag or a production identifier. Link diagnostic queries/dashboards at their owner.
- Which actions change state, their limits, and whether retry is safe after partial/unknown results.
- How to verify recovery externally, when to stop, and rollback/recovery limits when relevant.

Separate inspection from remediation. A quiet command or cleared alert is not enough to prove
recovery; identify the affected user operation or durable state to check. Prefer an existing
safe automation entrypoint over duplicating its internal commands. Automation that repeatedly
performs a fixed sequence may be a better follow-up than an ever-longer manual recipe.

[AWS runbook guidance](https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/ops_ready_to_support_use_runbooks.html)
calls for outcomes, prerequisites, error handling, ownership and another person's validation.
[Google SRE](https://sre.google/workbook/on-call/#maintaining-playbooks) describes a real tradeoff
between general playbooks and detailed steps: choose the detail needed by the intended operator.
Rehearse permitted work in an isolated environment and record scope/date/results at the existing
owner. Mark unrehearsed or externally blocked steps honestly; do not exercise live recovery merely
because a documentation task includes commands. Update after a relevant system change or use.

## Comments and API documentation

Implementation comments should explain a constraint, invariant, workaround, ownership rule,
algorithm choice or non-obvious ordering. Public API docs explain use without requiring the
implementation: units, valid inputs, mutation, ownership/lifetime, errors, cancellation,
thread/actor safety and meaningful complexity when relevant. Do not manufacture guarantees.

Delete narration such as “increment the counter” beside the increment. Keep a concise API
summary when generated reference or IDE help needs it. A useful repeated summary in separate
API entries is different from competing long-form authorities. Inspect before removing license
notices, safety rationales, generation/build directives, lint suppressions, coverage pragmas or
tool annotations: comment syntax does not mean the text is behaviorally inert.

| Platform | Useful documentation distinction |
| --- | --- |
| Swift | [API design guidelines](https://www.swift.org/documentation/api-design-guidelines/) prioritize clarity over brevity and useful summaries. Retain consumer-facing docs and relevant actor/ownership/precondition behavior; avoid expanding every trivial local into boilerplate. |
| Rust | [rustdoc](https://doc.rust-lang.org/rustdoc/how-to-write-documentation.html) distinguishes crate/module `//!` from item `///`, renders summaries and examples, and calls out reachable panics. Preserve safety requirements for unsafe APIs and error semantics; don't duplicate types already rendered in signatures. |
| Go | [Go doc comments](https://go.dev/doc/comment) cover exported names and packages; document meaningful zero values and stronger concurrency guarantees. Use the existing example tests and inspect `go doc` output where useful. |
| Python | [PEP 257](https://peps.python.org/pep-0257/) treats docstrings as runtime-visible API documentation and covers side effects, exceptions and call restrictions. Don't repeat signatures or assume deleting a docstring is a semantically inert comment edit. |
| TypeScript / JavaScript | Preserve the project's JSDoc/TSDoc dialect and supported tags. [TSDoc](https://tsdoc.org/) documents parser interoperability problems: tags can affect generated APIs and tools, so verify the consumer before changing them. |
| Zig | [Zig 0.17.1](https://ziglang.org/documentation/0.17.1/#Doc-Comment-Guidance) favors omitting name-derived repetition yet permits duplication across similar APIs for IDE help. Preserve `assume` versus `assert` invariant meaning; use the project's actual language version. |
| C / C++ / CUDA | Put caller contracts beside declarations and implementation rationale beside definitions. Preserve pointer ownership, nullability, lifetimes and synchronization assumptions; follow the project's Doxygen/other dialect. [Google C++ comments guidance](https://google.github.io/styleguide/cppguide.html#Comments) is one concrete style, not a language mandate. |

Check documentation with the project's existing renderer/compiler/example runner. A comment
cleanup must not change runtime statements, supported APIs or product behavior. Keep unresolved
contract discrepancies visible rather than silently editing code or promising untested behavior.
