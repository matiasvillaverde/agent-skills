# Apple Evaluations: implementation and result validity

Use this for native API work. The [Apple walkthrough](https://developer.apple.com/documentation/evaluations/evaluating-language-model-responses)
defines the four parts of `Evaluation`: a `Loader` dataset, `subject(from:)`, evaluators and
aggregation. `ModelSample<Expected>` holds input/reference data; `ModelSubject<Value>` wraps
the actual response and optional transcript. `Metric` supports pass, fail, numeric score and
ignore. An ignored metric is absent from its aggregate denominator.

`@Test(.evaluates(evaluation, info: ..., recordTranscripts: false))` runs the evaluation before
the test body. Read the result from `EvaluationContext.current.result`. Direct `try await
evaluation.run(info:)` is also available. `info` identifies the run; it is not the prompt.
Use the Xcode Report navigator's Evaluations and Compare views for inspection.

## A small diagnostic before a live model

This original fixture verifies framework wiring without inference. Its subject parses the
input independently of the expected answer. Replace the diagnostic with the real feature
when measuring product quality; a passing fixture says nothing about a language model.
The explicit aliases also make associated types clear to the compiler.

```swift
import Evaluations
import Testing

struct IntegerProbe: Evaluation {
    typealias Sample = ModelSample<Int>
    typealias Subject = ModelSubject<Int>
    let samples = [
        ModelSample(prompt: "17", expected: 17),
        ModelSample(prompt: "-4", expected: -4),
    ]
    var dataset: ArrayLoader<Sample> { ArrayLoader(samples: samples) }
    let exact = Metric("Exact")

    func subject(from sample: Sample) async throws -> Subject {
        let value = try #require(Int(sample.promptDescription))
        return ModelSubject(value: value)
    }
    var evaluators: Evaluators {
        Evaluator { sample, subject in
            guard let expected = sample.expected else {
                return exact.failing(rationale: "Required reference missing")
            }
            return subject.value == expected ? exact.passing() : exact.failing()
        }
    }
    func aggregateMetrics(using aggregator: inout MetricsAggregator) {
        aggregator.computeMean(of: exact)
    }
}

struct IntegerProbeTests {
    static let evaluation = IntegerProbe()
    @Test(.evaluates(evaluation, recordTranscripts: false))
    func frameworkWiring() throws {
        let result = EvaluationContext.current.result
        try #require(!result.errors.hasFailures)
        try #require(result.errors.anyInferenceProduced)
        try #require(result.detailed.shape.rows == Self.evaluation.samples.count)
        let scores = result.detailed[metric: Self.evaluation.exact]
            .compactMap { $0?.doubleValue }
        try #require(scores.count == Self.evaluation.samples.count)
        let accuracy = result.aggregateValue(.mean(of: Self.evaluation.exact))
        try #require(accuracy.isFinite && (0...1).contains(accuracy))
        #expect(accuracy == 1)
    }
}
```

The `1` above is the expected result of two deterministic parser cases, not a universal
AI-quality threshold. Use product-owned acceptance criteria for live evaluations. Keep
individual cases identifiable even when a single evaluation test processes the dataset.
For a reusable gate, reconcile actual case identities as well as counts: replacing an input
with a duplicate can preserve the row count and perfect mean. Check that a required metric
column exists before subscripting it; an absent column can otherwise trap instead of producing
a useful invalid-run result. The fixed diagnostic above always constructs that metric.

## Interpret errors and coverage before quality

| Signal | Meaning and action |
| --- | --- |
| `errors.inferenceFailureCount` | Subjects threw. Investigate unavailable model, cancellation or product failure; do not count the surviving mean as all-case success. |
| `errors.evaluatorFailureCount` / `failingEvaluatorTypes` | Graders threw. Fix missing evidence, parsing or service failures before interpreting affected scores. |
| `errors.anyInferenceProduced == false` | No evaluated subject was produced. Inspect empty/filtered datasets and backend availability. |
| `errors.metricsNotFound` | Aggregation referenced metrics that were not produced. Repair wiring; do not substitute zero. |
| Rows differ from the intended case count | Loading, filtering or execution changed coverage. Account for every case ID. |
| Scored counts differ from eligible counts | `.ignore`, missing references or metric eligibility changed the denominator. Report coverage per metric. |
| Aggregate `-1` | The requested statistic was not found; ensure the same operation was registered. For a legitimately negative-valued statistic use presence and error checks, not a blanket `score != -1` rule. |

See [EvaluationRunErrors](https://developer.apple.com/documentation/evaluations/evaluationrunerrors)
and [aggregateValue](https://developer.apple.com/documentation/evaluations/evaluationresult/aggregatevalue(_:)).
`.ignore` can represent an explicitly inapplicable metric. It cannot stand in for a required
answer the system failed to produce. A valid refusal should have its own expected outcome
and a refusal/abstention metric, not disappear from coverage.

For expected operational outcomes, a small typed outcome wrapper can preserve results and
failure categories in the sample. Keep unexpected harness exceptions visible through the
run-error checks. Avoid a catch-all that converts cancellation and broken infrastructure
into indistinguishable low-quality model responses.

## Runner and deployment details

Check `xcodebuild -version`, `xcrun swift --version` and the selected SDK before authoring
version-sensitive code. Evaluations lives in the developer frameworks with testing tools;
an app-target import is the wrong packaging boundary. A separate dataset-generation CLI may
need `ENABLE_TESTING_SEARCH_PATHS=YES` and the documented developer runpath, as described in
[Apple's generator guide](https://developer.apple.com/documentation/evaluations/generating-synthetic-evaluation-datasets).

The local diagnostic used a dependency-free SwiftPM test target with `swift test` on Xcode 27.
For an app, use its actual `xcodebuild test` scheme/destination and existing `.xcresult` storage.
Inspect current `xcrun xcresulttool --help` before exporting; do not invent evaluation-export
subcommands. Persist a small portable summary with explicit statuses when cross-run tooling
needs it. Test any framework save/load round trip before relying on typed reloaded columns.
