# Sources and qualification

Researched 2026-11-15. This is an original, condensed workflow; no third-party skill text or
sample implementation was copied. Recheck the installed SDK before using changed APIs.

- [Apple Evaluations](https://developer.apple.com/documentation/evaluations): framework index
  and availability read through Apple's Markdown endpoint; Xcode/OS 27, tvOS excluded.
- [Meet Evaluations, WWDC26/298](https://developer.apple.com/videos/play/wwdc2026/298/):
  relevant transcript and code read for framework structure and Swift Testing integration.
- [Robust agentic evaluations, WWDC26/299](https://developer.apple.com/videos/play/wwdc2026/299/)
  and [hill-climbing, WWDC26/335](https://developer.apple.com/videos/play/wwdc2026/335/):
  overview/chapter routing inspected; the linked API/design articles support the procedures.
- Apple articles linked from [the framework recipe](framework.md) and [advanced modes](advanced.md)
  were read in the relevant API/design sections. The generic framework is broader than
  language models; the subject can be another stochastic feature with suitable metrics.
- [Axiom evaluation guidance](https://github.com/CharlesWiltgen/Axiom/blob/ffafd3b3e0dbaaa60b753ca4a835ae6603b873e1/axiom-codex/skills/axiom-ai/skills/foundation-models-evaluations.md),
  [diagnostics](https://github.com/CharlesWiltgen/Axiom/blob/ffafd3b3e0dbaaa60b753ca4a835ae6603b873e1/axiom-codex/skills/axiom-ai/skills/foundation-models-evaluations-diag.md)
  and [API reference](https://github.com/CharlesWiltgen/Axiom/blob/ffafd3b3e0dbaaa60b753ca4a835ae6603b873e1/axiom-codex/skills/axiom-ai/skills/foundation-models-evaluations-ref.md):
  selected sections read at commit `ffafd3b3e0dbaaa60b753ca4a835ae6603b873e1` (2026-11-08).
  Useful diagnostic leads were checked against Apple documentation and a local executable
  probe. Fixed sample/variance/agreement quotas were not adopted. Older raw-column error
  checks were replaced with the current structured error API.
- [MLX Swift LM](https://github.com/ml-explore/mlx-swift-lm): README and adapter guide read;
  latest release endpoint returned [3.32.3](https://github.com/ml-explore/mlx-swift-lm/releases/tag/3.32.3)
  (2026-09-30). The adapter was not installed or executed.
- [SwiftEval paper](https://arxiv.org/html/2505.24324v1), 2025-05-30: abstract, motivation,
  design and limitations read. This evaluates generated Swift code and is not Apple's
  evaluation framework. [ModelScope SWIFT evaluation](https://swift.readthedocs.io/en/v4.1/Instruction/Evaluation.html)
  uses Python/EvalScope and is also a different system.

## Local evidence and limits

A dependency-free SwiftPM probe ran on Xcode 27.0 (`27A266a`), Swift 6.4
(`swiftlang-6.4.0.34.1`) and macOS 27.0.1 ARM64. Seven meaningful diagnostic tests passed:
direct run, missing aggregate, thrown subject, failed grader, empty dataset, missing tool
transcript, ignored-metric coverage and `.evaluates` trait integration were covered across
those tests. The independent documentation example was also compiled and executed.

In particular, a two-case run with one throwing subject retained two rows and reported a
mean of `1` over the successful metric while `inferenceFailureCount == 1`. An intentionally
ignored metric similarly left a mean of `1` with no run error, but only one scored row.
Therefore errors, rows and scored counts are complementary checks.

These probes used deterministic subjects and made no model/provider requests. They validate
framework mechanics, not Foundation Models quality, model-judge calibration, physical-device
execution, entitlement availability, Linux behavior or the reliability of any product.
Private receipts remain outside Git; temporary builds are deleted after retaining small
source/log records.

A separate fresh-context agent then used this skill on an incomplete integer-parser gate.
The original test passed with one required metric ignored. Its repaired gate retained the
parser/target/dependencies and the fixture's existing threshold while rejecting incomplete
coverage, missing/invalid metrics, errors, empty runs and same-count input substitution.
Twelve native regression tests passed, including expected rejection of invalid runs. Final
source and concise logs were inspected; task-owned scratch/build caches were removed.
This is independent skill-usage evidence, still with no model calls or live-quality claim.
