---
name: test-behavior
description: Independently explore a running product through its real interface to find incomplete features and false success. Use for fresh-user testing of web, native apps, CLIs, APIs, MCPs and jobs after implementation.
---

# Test behavior independently

Find where a user goal fails in the running product. Work from observable requirements,
not the builder's explanation of how the code ought to work. Preserve the intended UI,
product functionality and permission boundaries; this role reports findings, not fixes.

## Establish an honest starting point

Obtain the user goal, required outcomes, relevant preserved behavior, target/build identity,
test environment and allowed fixture/account references. Infer these from authorized context;
ask only for a missing decision or prerequisite that materially blocks execution. Separate
requirements from assumptions. Do not invent a product feature or universal guarantee.

If you built or inspected the implementation, use a fresh-context tester when delegation is
available and authorized. Pass only the contract, runtime entrypoints, public/operator docs,
fixtures, permitted actions and budget. Do not forward builder reasoning, diffs, test answers,
prior success claims or a prescribed happy-path script. Select the host's actual option for
starting without inherited conversation; a prompt to forget context is insufficient. If fresh
execution is unavailable, proceed with useful source-informed checks and disclose the limitation.
Do not claim a fresh context is an OS sandbox or an independent model.

Use a unique session and private evidence directory per tester; separate mutable fixture state
when agents run concurrently. Keep credentials in approved tooling. Stay out of source, tests,
Git history and implementation notes during discovery. If source exposure occurs, disclose it;
use a separate diagnostic role when code inspection becomes necessary.

Read the relevant section of [interface guidance](references/interfaces.md). Use installed,
approved capabilities and current target documentation. Lack of a browser/device/transport blocks
that interface; an API substitute cannot establish its UI behavior.

## Explore the actual product

Start with an important end-to-end user goal. Establish initial state, act through the intended
entrypoint, and observe the promised final result. Inspect file content, fresh-session state or
documented downstream effects when relevant; a toast, accepted request or existing file alone
does not prove completion. Vary realistic data to expose static, stale and fixture-specific output.

Choose a few consequential boundaries and failure hypotheses. Relevant examples include empty
or malformed input, denied permissions, offline/deadline failure, interruption, stale state,
cancellation and duplicate actions under the documented retry contract. Follow surprising results:
form a new hypothesis, change a relevant factor, record the observation, and decide the next probe.
Do not run a Cartesian matrix or require a bug count. Correct behavior is an acceptable finding.

Reconcile uncertain mutations before retrying. Do not resend a payment, message, publish or job
merely because its response was lost. Use owned synthetic data and bounded faults in an authorized
test environment. Do not install dependencies, provision services, bypass confirmation or expand
test scope just to avoid reporting a blocker. Existing approved test actions need no new approval.

Capture reproduction evidence while exploring: precondition, exact action/input, expected result
and its source, actual result, target identity, and useful screenshots/outputs/correlation IDs.
Inspect rendered output as well as accessibility/DOM snapshots when they disagree. Console or
transport errors may belong to the tool/environment; establish their user-visible consequence.
Keep intermittent findings with observed frequency and conditions instead of discarding them.
Read exposed diagnostic signals when helpful; deeper source-informed investigation can run
separately without feeding implementation answers back into the fresh tester.

## Finish with attributable results

Give each scoped outcome a status: **passed, failed, blocked, not run, inconclusive**, or
**not applicable with a reason**. Passed means executed with sufficient evidence on the named
target. Separate an expected rejection that passed from an unavailable prerequisite that blocked.
Missing evidence and exhausted budgets never imply success. Report scope and independence limits.

For defects, provide the smallest useful reproduction, impact and evidence; distinguish confirmed
from suspected failures. A separate reviewer may adjudicate them. After an authorized builder fix,
recheck the original failing journey and relevant adjacent behavior against the original contract.
Do not change requirements to fit the repair. Preserve owning checks; source-aware review and
existing tests complement runtime findings.

Keep exploration disposable. Recommend a permanent regression only for a meaningful uncovered
failure, with explicit assertions that would catch it. Stop when scoped high-risk goals are
exercised, findings are reproducible or appropriately qualified, and remaining gaps are visible.
Retain minimal redacted evidence needed to act on findings; close owned sessions/processes and
remove task-created fixtures, transient captures and caches. Preserve unresolved failure evidence
and unrelated data; report any leftovers. Never claim the whole product is bug-free.

[Research basis](references/sources.md). This skill works alone; companion operational observation
or evidence review is useful when risk warrants it, not a mandatory three-agent ceremony.
