# Graders, measurement and comparisons

## Choose an oracle that can fail for the right reason

Prefer real state, execution, schema and domain calculations for objective requirements. Inspect
write/readback evidence for jobs, database changes, artifacts or tool actions. Regexes and substring
matches cannot establish an implemented feature. Grade outcomes and relevant constraints; use
trajectory checks only when the process itself is required or as diagnostics.

A semantic rubric states the criterion, available evidence, anchored judgments, valid alternatives,
and insufficient-evidence behavior. Split independently actionable criteria; avoid a blended score
that hides which requirement failed. Binary, ordinal, continuous and pairwise scoring fit different
decisions. Exact equality suits a stable identifier, not every valid summary. Pairwise judges need
randomized order, tie handling and a record of the actual comparison.

Keep candidate content untrusted and separate from evaluator instructions. Blind candidate identity
when feasible. Ask for a short criterion-specific justification and source/effect evidence, not
private chain-of-thought. Pin rubric, evaluator code/model/configuration and dataset. A different
model family may reduce correlated errors but does not replace calibration or prove independence.

## Calibrate before trusting

Exercise the grader with independently reviewed positive, negative, borderline and alternative-valid
examples. Include known-bad outputs that look polished, missing results, irrelevant long answers,
injection aimed at the judge, wrong IDs and plausible fabricated facts. Change a relevant fact and
an irrelevant style detail: the scorer should respond to the former without blindly rewarding the
latter. A scorer that never rejects cannot certify success.

Inspect false acceptances and false rejections by criterion, severity and useful slice. Report
agreement and uncertainty appropriate to the label type (confusion counts with precision/recall,
or kappa/alpha where assumptions fit). High accuracy under skew and high inter-rater agreement
do not establish validity. There is no universally acceptable kappa, accuracy or F1. State whether
evidence supports exploration, monitoring or a release gate. Recalibrate on material grader, model,
rubric or population changes. Its tuning examples cannot be its only validation set.

## Keep denominators honest

Retain a row for every scheduled trial, including missing output, cancellation, timeout, provider
error, grader error, unavailable reference and skipped/unsupported case. Separate an expected product
refusal from infrastructure failure. Record whether failure belongs to the candidate or harness;
unknown attribution stays unknown. Failed or ungradable rows cannot disappear or become 1.0.

Report intended, attempted, completed, gradable and passing counts with relevant rates. Conditional
quality among gradable trials and operational success over attempted trials may both be useful;
label denominators. Never average missing sentinel values or NaN into a score. Missing usage means
unknown cost, not zero. Apply declared exclusions with counts/reasons; a partial run cannot quietly
become a release pass.

## Compare fairly

Pair the same case IDs and conditions across baseline and candidate. Preserve first attempts; retries
are recorded trials, not erased failures. Choose repetitions from variance, consequence and budget.
Repeated draws estimate within-case variability; independent cases estimate generalization. They
cannot be interchanged by multiplying sample counts. Seeds or temperature zero do not guarantee
deterministic hosted inference.

Use an effect size meaningful to the task and report uncertainty. Intervals must respect independent
case/group units when trials or variants are correlated. For binary paired comparisons, inspect
discordant pairs rather than two unrelated percentages. Zero observed failures still leaves
uncertainty: under independent Bernoulli trials, a one-sided 95% upper bound is
`1 - 0.05^(1/n)`, approximately `3/n`. Many variants of one attack rarely justify those assumptions.

Separate exploratory sweeps from declared final assessment. State stopping and selection rules;
do not stop on a favorable noisy score or report only the winning arm. If model, prompt and retrieval
change together, the result evaluates the bundle, not an isolated cause. Report per-case regressions,
important slices, first-attempt success, latency and actual cost/tool counts. Hard constraints cannot
be offset by better style or speed.

`pass@k` asks whether at least one of k attempts succeeds; use it when that many attempts and selection
fit the use case. All-k success (`pass^k` in agent-eval literature) asks a different reliability question.
Never relabel best-of-k as first-attempt success. An inconclusive comparison is valid; propose the next
discriminating evidence instead of manufacturing a ship decision.
