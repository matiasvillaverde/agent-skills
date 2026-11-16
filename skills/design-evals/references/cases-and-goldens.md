# Cases, evaluation types and golden datasets

## Select the evidence by claim

These are dimensions, not competing framework names. A suite may combine several.

| Claim | Useful evaluation | Common false conclusion |
| --- | --- | --- |
| Required shape or exact calculation | Parser, schema, executable assertion, reference implementation | Valid JSON proves useful content |
| Correct answer, extraction, summary or classification | Task-specific reference facts, labels or anchored rubric | Text similarity or polished wording proves correctness |
| Retrieval provides evidence | Relevant-document labels and recall/precision at the consumed cutoff; answerability | A fluent answer proves retrieval worked |
| Answer is grounded | Check claims against supplied sources, separately from task completeness | Grounded but irrelevant content solves the task |
| Agent completes a job | Initial state, allowed tools, actual final-state/effect checks | A success message or prescribed sequence proves completion |
| Constraints hold under attack or ambiguity | Controlled adversarial cases, unauthorized/no-action outcomes, boundary evidence | No observed bypass proves absence of vulnerabilities |
| Performance is usable | End-to-end latency, first useful output, requests, cost and resource budgets | A fast mock predicts production latency |
| Related inputs preserve behavior | Metamorphic/property checks with justified invariants | Every paraphrase must have identical text |
| Improvement reaches users | Reviewed shadow/online observations; randomized experiments for causal evidence | A changed production score proves the deployment caused it |
| Multimodal quality | Original permitted audio/image/video and task-specific expert or executable checks | Grading extracted text establishes audio/visual quality |

Capability cases discover headroom; regression cases protect established behavior. A deliberately
hard challenge set and a representative production sample answer different questions. Keep their
scores separate unless a declared weighting represents the target population.

## Case anatomy

Adapt the existing schema. A useful conceptual shape is:

```json
{
  "id": "job-timeout-01",
  "group": "job-timeout-family",
  "input": {"request": "Archive this model", "fixture": "archive-timeout-v2"},
  "expected": {
    "constraints": ["No false completion claim", "No duplicate archive"],
    "observable_state": "pending reconciliation after ambiguous provider timeout"
  },
  "metadata": {
    "source": "sanitized incident fixture",
    "review_status": "draft",
    "split": "development",
    "slices": ["network-timeout", "ambiguous-write"]
  }
}
```

This is illustrative data, not an executable contract or reviewed golden. Tie every constraint
to a grader and observation before running. An unknown external mutation cannot be declared
absent merely because a local record is missing.

Store environment/fixture revision, allowed effects, reset behavior and time/spend limits at the
suite level when common. Use per-case overrides only where necessary. Gold/reference data belongs
to the evaluator, not automatically in the candidate prompt or tools. Trial output is separate:
case ID, attempt, actual result/effects, status, evidence reference, metrics, usage and provenance.
The expected answer is never manufactured from that same trial's output.

## Build goldens from defensible evidence

1. Define the intended population and product contract. Inspect existing feedback, failures and
   examples before inventing more. Use permitted production samples, domain-expert cases, known
   regressions and synthetic gap-fillers, with source and selection rationale. Public benchmarks
   can test plumbing or offer anchors; they do not establish product validity.
2. Review labels independently where consequences warrant it. Record reviewer/source, rubric
   version, rationale, uncertainty and adjudication. Agreement can coexist with shared
   misunderstanding. Keep disputed or insufficient-evidence labels explicit; resolve or separate
   them rather than choosing whichever label rewards the candidate. Recheck stale facts.
3. Sample by task type and relevant risk slices: language, permissions, input size, incomplete data,
   recovery or user cohort. Preserve ordinary successes as well as failures. Oversampling rare
   severe cases is useful; report them separately or use justified population weights. Do not infer
   population frequency from a handpicked challenge set.
4. Split by independent source unit (document, customer, conversation, repository or task family)
   before paraphrasing/augmentation. Near-duplicates and later turns of the same session must not
   cross an independent holdout. Separate development, grader-calibration and final assessment
   roles; share reviewed material only when the limitation is explicit.
5. Record dataset and transform versions. Keep immutable source references with availability
   controls or permitted stable snapshots so reproduction does not silently read changed content.
   Validate joins, IDs, missing labels and transforms. Do not store customer data in Git by default.
6. Freeze a holdout before comparing candidates. Record assessment exposures; repeated selection
   on that set turns it into development evidence. Refresh for material population, policy or
   rubric changes and compare against the same new version, retaining old results as historical.

There is no magic minimum corpus size. Start small enough to inspect every case, then expand for
uncovered behavior or precision needed by the decision. Many correlated variants are not many
independent tasks. Keep synthetic status visible even when an expert approves the label.
