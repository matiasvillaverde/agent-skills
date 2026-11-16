# Qualification and limits

Verified 2026-11-15. These checks establish bounded skill/harness behavior, not product readiness.

An independent agent received only this skill, a synthetic archive-assistant contract, JSONL cases,
recorded outcomes and the old phrase-matching grader. It produced a small standard-library replay
grader, revised draft cases and a concrete proposal without changing the original inputs.

Observed behavior:

- Rejected a queue-only completion claim and a forbidden write despite a matching refusal sentence.
- Accepted alternate wording but withheld full completion when the expected object hash had no
  independent source; a result hash was not promoted into its own golden answer.
- Preserved an unresolved timeout, missing case, original failed attempt and unknown cost.
- Identified paraphrase leakage across the split and kept exposed material in development.
- Separated deterministic evidence, ungraded response semantics, reviewed goldens and live behavior.

Twenty-one focused offline checks passed. Replay exited 1 as intended: one bounded deterministic
pass, two failures and two insufficient recorded outcomes, plus one missing-case slot. All five
original fixture inputs were byte-identical. The agent's proposed labels remain drafts; no human
golden adjudication, model inference, judge calibration or product run occurred.

Native Apple diagnostics and an independent Swift gate trial are recorded by the
[Swift skill](../../evaluate-swift/references/sources.md). Ordinary skill/link/format validators
also passed. A source-grounded prompt and these small trials cannot guarantee all future behavior.
Revalidate against a real system's permitted cases before treating the suite as release evidence.
