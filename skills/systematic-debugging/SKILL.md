---
name: systematic-debugging
description: Diagnose a bug, regression or repeated agent/tool failure using concrete evidence, focused hypotheses and a minimal verified fix.
license: MIT
---

# Systematic debugging

Establish the exact symptom, affected scope and last known working behavior. Read the
actual error and relevant code before editing. Scale the investigation to uncertainty;
an obvious local defect does not need a hypothesis document or a fixed number of trials.

## Find a discriminating observation

Reproduce the real failure when possible. Record the input, environment and observable
result. If reproduction is unavailable, continue with source, existing traces or a
smaller safe experiment while distinguishing evidence from inference.

Classify the observed failure: deterministic result, crash, race/flakiness, state/order
dependence, resource exhaustion, timing or external availability. Reduce input and setup
without deleting the trigger. Use [reproduction and regression isolation](references/reproduction.md)
when seeds, environment differences, bisect or intermittent behavior matter.

Check recent relevant changes and a working sibling path. Trace the failing value,
state transition or resource back to its owner. For multi-component failures, inspect
the boundary where the evidence changes rather than adding logging everywhere.
Use minimal redacted instrumentation and remove temporary probes after diagnosis.

State a specific hypothesis and what observation would falsify it. Change one relevant
variable at a time. If the observation disagrees, revise the hypothesis instead of
stacking speculative patches. Repeated failures are a signal to recheck assumptions
and scope, not proof that the entire architecture must be replaced.

For agent/tool loops, verify the current directory, branch, actual files, tool result
and service state. Stop repeating an unchanged failing action. Preserve useful evidence,
reduce the failing scope and retry only when the cause or conditions changed. An
ambiguous external mutation needs reconciliation before another attempt.

## Fix and verify

Fix the responsible owner, preserving the requested behavior and unrelated work.
Validate at actual trust boundaries; do not add defensive checks at every internal
layer or introduce a new recovery framework for one failure.

Choose a regression case that would detect this bug, with an independently derived
expected result. Reuse an existing test when it can express the case clearly. A
runtime reproduction or targeted integration check may be the appropriate evidence;
do not manufacture a unit test that cannot exercise the real failure.

Run the checks affected by the fix and the required project gates. Reuse valid evidence
when neither its inputs nor the relevant environment changed. Confirm the original
symptom is resolved, not just that a related test passes.

Report the cause, focused change, verification and remaining uncertainty. Do not claim
complete diagnosis when only a mitigation was established.
