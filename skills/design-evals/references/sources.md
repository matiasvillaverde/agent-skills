# Sources and scope

Reviewed 2026-11-15. Original synthesis; no upstream code, prompt pack, hook or service is installed.
Recheck package/API status before implementation. Framework versions and source read extents are
recorded in the repository's dated evaluation research; this portable skill keeps decision sources.

## Primary methods

- [Anthropic: agent evaluation anatomy](https://www.anthropic.com/research/demystifying-evals-for-ai-agents),
  2026-01-09: case/trial/outcome distinctions, agent-harness scope and capability/regression suites.
- [Anthropic: statistical approach](https://www.anthropic.com/research/statistical-approach-to-model-evals),
  2024-11-19: paired comparisons, within-case variation and clustered uncertainty.
- [Anthropic: safety evaluations](https://www.anthropic.com/research/building-strong-safety-evaluations),
  2026-11-13: validity, benign behavior, human calibration and failures; numeric program thresholds
  are not universal requirements for small engineering evaluations.
- [OpenAI: evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices):
  task-specific datasets and calibrated assessment. Methodology is distinct from its hosted Evals
  service, [marked for shutdown on 2026-11-30](https://developers.openai.com/api/docs/deprecations).
- [CheckList](https://aclanthology.org/2020.acl-main.442/), ACL 2020: behavior, invariance and directional
  tests; only use transformations whose task semantics are justified.
- [MT-Bench](https://arxiv.org/html/2306.05685v4) and [LLMBar](https://arxiv.org/html/2310.07641v2):
  judge agreement in one setting does not establish robustness to instruction violations and bias.
- [Human Feedback is not Gold Standard](https://arxiv.org/html/2309.16349v2): human ratings can also
  inherit confounds. [Rephrased contamination](https://arxiv.org/html/2311.04850v2): overlap checks
  and synthetic generation do not prove independence from benchmark training exposure.

## Community workflows examined

- [Braintrust eval library](https://github.com/braintrustdata/eval-library/tree/04486b39047b5ba230f795e52f2935fef651e789/skills):
  read build-eval-dataset, validate-eval-scorer, design-eval-experiment and size-eval-dataset.
  Useful provenance, reviewed constraints, leakage controls, dangerous false acceptances and paired
  experiments. Do not import fixed repeat quotas, platform writes or universal agreement cutoffs.
- [ECC eval-harness](https://github.com/affaan-m/ECC/blob/0765f7a2ca2bd5df214d3aa7ba7e7ac19db8b189/skills/eval-harness/SKILL.md):
  capability/regression distinction; reject grep-as-behavior proof and automatic ship thresholds.
- [Anthropic skill-creator](https://github.com/anthropics/skills/blob/b0cbd3df1533b396d281a6886d5132f623393a9c/skills/skill-creator/SKILL.md):
  compare actual artifacts under old/new or absent skills; no prescribed agent count or forced UI.
- [SkillMedev evaluation](https://github.com/SkillMedev/skills/blob/bea4ea5d81f5003e01447855df0ca0002dfed60c/skills/llm-evaluation/SKILL.md):
  rubric anchors and separate development/assessment; avoid numeric defaults without a decision basis.

The [qualification note](verification.md) records independent fixture evidence and its limits.
The framework reference links the owning docs for current implementation choices. This is a bounded
engineering selection, not an exhaustive index of every evaluation framework or a quality ranking
from benchmark scores. Qualification records describe offline fixture behavior, not product readiness.
