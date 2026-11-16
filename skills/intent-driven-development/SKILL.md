---
name: intent-driven-development
description: Turn ambiguous or consequential feature requests into brief observable outcomes and scope boundaries, then continue authorized implementation.
license: MIT
---

# Intent-driven development

Use this when the intended result or a consequential constraint is unclear. Clear
requests, small edits and active debugging do not need another specification phase.

Read existing instructions, product contracts, callers and relevant behavior before
asking for facts. Distinguish what the code does today from what the user requires.
Do not infer business policy, retention, budgets or service guarantees from naming.

Capture only what helps execution:

- The observable outcome.
- The behavior in scope and the tempting adjacent work outside it.
- Material assumptions and existing contracts that must survive.
- A small set of meaningful acceptance checks, using the existing test or runtime
  facilities. Several criteria may be established by one check.

Use a few sentences or a short list. Reuse an existing issue, plan or owning document
when one already records this. Do not create a new registry or formal acceptance
document for routine work.

Ask only when a missing answer materially changes the result or cannot be safely
resolved from available evidence. Group related questions and continue independent
work. Existing authorization remains valid; clear implementation requests proceed
without another approval turn.

Choose verification by consequence: a focused regression test, runtime observation,
integration check, manual UX review or required project gate. Do not equate the number
of tests with evidence quality or impose universal coverage percentages.

When implementation reveals a genuine constraint, explain the changed assumption and
its effect. Update the existing plan if needed; do not silently weaken the promised
behavior. Seek a decision only when the unresolved change alters authorized scope,
cost, compatibility or an important safety boundary.

Finish against the original outcome, with concrete evidence and any remaining gap.
