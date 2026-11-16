---
name: design-evals
description: Design or audit evaluations for AI features, models and agents. Propose useful cases, reviewed golden datasets, calibrated graders, comparisons and a minimal runner or framework choice before interpreting scores.
---

# Design evaluations

Start with the decision: what change is being assessed, whose tasks matter, and what failure
would change the decision? Inspect the product contract, current runner, tests, redacted traces
and known failures. Reuse the existing stack. Ordinary deterministic software behavior belongs
in ordinary tests; model quality and agent outcomes need explicit evaluation evidence too.

## Propose the smallest useful evaluation

Map the real path from input through retrieval, inference, tools and persisted effects.
Identify the uncertain claim and observable oracle at each relevant boundary. Choose a few
discriminating cases before growing coverage. If the request is a proposal, return a concrete
plan and draft cases; do not silently launch paid trials, export data or replace the framework.

For each proposed check, name the behavior/risk, case source, observable evidence, grader,
baseline, intended use and remaining uncertainty. Distinguish a blocker from a diagnostic or
exploratory score. Derive acceptance from the product's consequences and existing requirements;
label proposed thresholds for review. No universal score, dataset size or repetition count
establishes readiness. Keep UI, product semantics and existing acceptance criteria intact.

Read [cases and golden datasets](references/cases-and-goldens.md) for evaluation types,
case structure, representative sampling, reviewed labels and contamination controls.
Expected behavior can be a set of valid outcomes or constraints; do not demand one wording
or trajectory when alternatives satisfy the task. Include the appropriate refusal, clarification
or no-action outcomes, not just successful execution.

## Establish trustworthy grading

Use execution/state/schema checks for objective facts; semantic rubrics only for what those
cannot establish. Calibrate subjective graders against independently reviewed examples,
including known failures, valid alternatives and plausible shortcuts. Synthetic references
are candidates until reviewed. Missing references, judge outages, malformed grades and skips
must remain visible and cannot become passes. Separate hard constraints from quality averages.

Read [graders and comparisons](references/graders-and-analysis.md) when writing rubrics,
validating a judge, selecting repeats or interpreting a score. A model's claim of completion
is not the oracle. A high average can conceal a serious failing slice or rejected trials.

## Fit the runner to the problem

Pin the dataset, task/harness, tools, prompt/model settings and grader versions. Preserve
case/trial identities and distinguish fresh inference, cached responses, replay and simulation.
Use paired cases for comparisons; state what changed together and cannot be attributed separately.

Read [framework and runner choices](references/frameworks-and-runner.md) only when choosing
or implementing infrastructure. Prefer a small adapter around the current runner over a new
platform. Use [evaluate-agents](../evaluate-agents/SKILL.md) for controlled full-harness
execution and [evaluate-swift](../evaluate-swift/SKILL.md) for Apple's Evaluations APIs.
Framework availability does not grant data access, production mutations or model spending.

## Deliver useful evidence

Leave a concise evaluation proposal or the authorized implementation in the existing owner
location: question, cases/slices, graders, failure policy, comparison and budget, decision rule,
and next unresolved evidence. Keep private source material and raw traces in approved storage;
version only permitted sanitized cases or opaque references. Keep a representative quality set
and targeted failure regressions distinguishable. After a real failure, review the oracle before
adding a durable case. Remove task-created disposable outputs after retaining minimal redacted
evidence; preserve shared caches, source datasets and recovery artifacts.

[Sources and scope](references/sources.md) records the research behind these choices.
