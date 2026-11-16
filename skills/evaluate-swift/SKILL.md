---
name: evaluate-swift
description: Build, run or debug evaluations of Swift intelligence features with Apple's Evaluations framework. Use for Foundation Models quality, model judges, tool trajectories and trustworthy evaluation results; ordinary Swift tests belong to test-swift.
---

# Evaluate Swift intelligence features

Measure the feature that ships, using the project's existing service and test target.
Preserve UI, product behavior, supported deployment targets and model configuration unless
the user has requested a change. An evaluation proposal does not authorize a prompt rewrite.

## Choose the right boundary

Inspect Xcode/Swift/SDK versions, the actual model backend, test targets, existing evaluation
data and required devices. Apple **Evaluations** is a distinct developer framework integrated
with Swift Testing, introduced with Xcode/OS 27. Check installed interfaces and current Apple
documentation for the symbols in use; framework availability does not establish model,
hardware, locale or entitlement availability. Keep imports in test/evaluation tooling.

For older SDKs or Linux, reuse a small compatible runner and portable fixtures; do not raise
the app deployment target just to obtain Evaluations. Do not confuse Apple's framework with
the SwiftEval code-generation benchmark or ModelScope's Python `ms-swift` project.

Use [design-evals](../design-evals/SKILL.md) for the decision, cases, oracles, dataset splits
and grader calibration. Use [evaluate-agents](../evaluate-agents/SKILL.md) when the claim is
about a complete agent harness and real effects. Use [test-swift](../test-swift/SKILL.md) for
ordinary code contracts; XCTest/UI and performance checks remain separate evidence.

## Implement and prove the evaluation

Read [the framework recipe](references/framework.md) for `Evaluation`, Swift Testing and
result validity. Start with code-based metrics where the expected behavior is computable.
Make `subject(from:)` call the real feature; a fake subject validates the harness only.
Record stable case IDs, provenance and feature/model/dataset/grader revisions outside the
prompt as appropriate. Start a fresh session per independent case; preserve intentional
multi-turn state within its case.

Before applying a quality threshold, prove that intended cases loaded, subjects were
produced and required metrics were scored. Inspect `EvaluationResult.errors`, row counts,
per-metric scored/ignored counts and aggregate registration. A thrown subject, failed judge,
missing transcript or `.ignore` can leave a favorable score over only the surviving cases.
Missing aggregates return `-1`; validate metric presence and its domain before comparison.
Never let a missing latency/error metric pass a lower-is-better gate.

Separate expected refusals/abstentions, product failures and infrastructure failures. Model
unavailability is a visible unsupported/skipped run or a failed required lane, according to
the owning contract. It is never a passing product-quality result. Do not turn every refusal
into a failure or silently remove it from the denominator.

Read [judges, trajectories and datasets](references/advanced.md) only for those modes.
Calibrate semantic judges against independent labels and valid alternatives before trusting
their scores. Check final outcomes as well as tool selection; a correct stubbed call does
not prove persistence, authorization or real device behavior.

## Run and report

Reuse the project's test command, scheme and result-bundle convention. Limit dataset size,
trials, concurrency and model/judge spending to the decision and existing authorization.
Keep deterministic harness checks usable without downloading models or calling providers.
Run quality comparisons under matched conditions and evaluate relevant device/OS/model and
locale differences; a simulator or a single Mac does not establish fleet-wide behavior.

Report quality by meaningful slice, completion/scoring coverage, failures, uncertainty and
resource cost separately. Name the actual backend and distinguish stub, local model and
remote model evidence. Preserve a small redacted result/receipt, then remove task-owned
builds, traces and temporary datasets when no longer needed; keep shared caches, approved
datasets and required private evidence. [Sources and verified limits](references/sources.md)
record the researched version and the local diagnostic coverage.
