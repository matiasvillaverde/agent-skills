# Judges, trajectories and datasets

## Model judges

Use `ModelJudgeEvaluator`, `ScoreDimension`, `ScoringScale` and `ModelJudgePrompt` for
qualities a deterministic oracle cannot establish. Choose observable rubric levels and
separate independent dimensions. Explicitly select the judge backend when reproducibility,
privacy or spending depends on it; the installed SDK defaults to a system model.

Pointwise judging scores one output. Pairwise judging compares it with a baseline; preserve
case identity and reverse order when position bias could change the decision. Keep reference
labels out of the subject's prompt and expose only the intended evidence to the grader.
Treat prompts, responses and retrieved text as untrusted content, including attempts to
instruct the judge to award a passing score.

Calibrate on outputs independently labeled under the same rubric, including bad, borderline
and valid alternative answers. Compare judge disagreement with human disagreement; inspect
false approvals and important slices. Choose the agreement statistic for nominal or ordinal
labels and their prevalence. Neither a universal kappa cutoff nor a minimum score variance
proves a judge is good. An all-equal score can be correct on an all-equal calibration set.

Apple's [judge API guide](https://developer.apple.com/documentation/evaluations/scoring-with-model-as-judge-evaluators)
and [judge design guide](https://developer.apple.com/documentation/evaluations/designing-effective-model-judges)
provide the API and calibration workflow. Use short evidence-grounded rationales to audit
scores; avoid collecting private reasoning traces or unnecessary source content.

## Tool-calling and agentic features

Return `ModelSubject(value: ..., transcript: session.transcript.structuredTranscript)` when
grading tool calls. Attach an appropriate `TrajectoryExpectation` to each eligible sample
and add `ToolCallEvaluator`. A response without a transcript can compile and still yield
grader failures. A transcript without expectations does not establish trajectory coverage.

Choose ordered calls only when ordering is part of the behavior; otherwise use unordered
expectations and permitted argument ranges/alternatives. Declare disallowed tools where the
contract needs them. The installed `TrajectoryExpectation(ordered:unordered:allowsAdditionalToolCalls:)`
defaults to permitting extra calls; make that choice explicit for consequential workflows.
Do not forbid harmless alternate paths simply to match a recorded trace.

Apple's [tool-call guide](https://developer.apple.com/documentation/evaluations/evaluating-tool-calling-behavior)
uses stub tools to examine selection and arguments. Such evidence does not establish
authorization, durable side effects, error recovery or UI integration. Add the relevant
real-boundary check through the existing harness when making those claims. Reset isolated
state and enforce deadlines/cancellation, tool-call ceilings and repeat limits.

## Datasets, multimodal inputs and model comparisons

Use a curated golden set, representative traffic or task samples, known failures and
purposeful challenge cases. The shared [design-evals skill](../../design-evals/SKILL.md)
owns provenance, independent reference validation and development/holdout separation.
For locale-sensitive tasks retain language, locale, time zone and a fixed reference date.

`SampleGenerator` and `makeSamples(...targetCount:sessionProvider:validator:)` expand seeds;
`targetCount` includes seeds. Validate expected answers and metadata, remove duplicates and
inspect whether the generated distribution covers the intended cases. Keep generated
siblings in one split to prevent paraphrase leakage. Synthetic generation is candidate
production, not automatic gold labeling. See [synthetic datasets](https://developer.apple.com/documentation/evaluations/generating-synthetic-evaluation-datasets)
and [dataset design](https://developer.apple.com/documentation/evaluations/designing-evaluation-datasets).

For image/audio or large inputs, stream bounded data with a `Loader`; include decode failures,
skipped entries and counts in the receipt. Do not copy a sample loader's silent `continue`
branches into a mandatory quality gate. Apple demonstrates streamed image evaluation in
[Grub Gander](https://developer.apple.com/documentation/evaluations/evaluating-multimodal-prompts).
Do not treat a model's self-reported confidence as calibrated probability without evidence.

Use the same feature path and cases across model comparisons. Apple documents
[Core AI versus system-model evaluation](https://developer.apple.com/documentation/evaluations/evaluating-a-core-ai-model).
The official [MLXFoundationModels adapter](https://github.com/ml-explore/mlx-swift-lm/tree/main/Libraries/MLXFoundationModels)
bridges MLX models to Foundation Models on supported SDKs; inspect the pinned package's
capabilities and resource limits. Do not download weights or add a runtime solely to use
this skill. Record model/OS/SDK/weights/configuration and distinguish cold loading from
generation latency. Quality scoring and runtime profiling answer different questions.
