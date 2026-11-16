# Choose a runner without rebuilding the product

Reuse the installed evaluation/test stack, case store and telemetry first. Choose a new
framework only for a demonstrated need: adapters, controlled agent execution, annotation,
resuming runs or comparing artifacts. Check the installed package version and current primary
documentation before writing API calls. A framework supplies mechanics; it cannot establish
that the cases represent users or that a grader measures the intended outcome.

## Framework fit

These are conditional choices, not a popularity ranking or an exhaustive catalog.

| Need | Candidate and boundary |
| --- | --- |
| Small existing application with ordinary test infrastructure | A thin runner around the real entrypoint may suffice; use the contract below before adding a platform. |
| Declarative provider/prompt/API comparisons, especially TypeScript | [Promptfoo](https://www.promptfoo.dev/docs/configuration/reference/): datasets, assertions and custom app providers. Explicitly bound requests and runtime; distinguish default cached responses from fresh trials. |
| Typed Python evaluation functions | [Pydantic Evals](https://ai.pydantic.dev/evals/): cases, datasets, reports and span/trajectory checks; `pydantic-ai` is not required and Logfire is optional. |
| Metric-rich app, RAG or conversational evaluation | [DeepEval](https://deepeval.com/docs/evaluation-introduction): Python and TypeScript documentation; verify language-specific support. Many metrics invoke models. Synthetic goldens still require review. |
| Multi-step agents, controlled environments and detailed logs | [Inspect AI](https://inspect.aisi.org.uk/tutorial.html): datasets, solvers, scorers, sandboxes and analysis. Configure execution boundaries rather than assuming a task runner is containment. |
| Existing LangChain/LangGraph evaluation workflow | [LangSmith](https://docs.langchain.com/langsmith/evaluation-types), [OpenEvals](https://github.com/langchain-ai/openevals) and [AgentEvals](https://github.com/langchain-ai/agentevals): Python/TypeScript evaluators and comparisons. Match trajectories only where the sequence itself is contractual. |
| Existing experiment/annotation service | [Braintrust](https://docs.braintrust.dev/evaluate/run-in-code): task/data/scorers, SDKs including TypeScript, Python and Go. Local execution can upload experiments; set concurrency rather than relying on an unset default. |
| Existing trace-to-dataset/experiment workflow | [Phoenix](https://arize.com/docs/phoenix/datasets-and-experiments/concepts-datasets), [Langfuse](https://langfuse.com/docs/evaluation/overview), or [MLflow](https://mlflow.org/docs/latest/genai/eval-monitor/): use the one already deployed. Check storage, SDK/server compatibility and result export. |
| Retrieval component diagnosis | [Ragas](https://docs.ragas.io/en/stable/concepts/metrics/overview/): retrieval, groundedness and reference metrics; keep an end-to-end outcome measure. Reference-free scoring is not independent ground truth. |
| Existing optimized model program | [DSPy](https://dspy.ai/): use its evaluation/optimization workflow with separate tuning and assessment data. Do not adopt an optimizer merely to run a few assertions. |
| Academic or local-model benchmark comparison | [lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness): pin backend, task and tokenizer revisions. A model score does not validate the product harness. |
| Existing Google ADK agent | [ADK evaluation](https://google.github.io/adk-docs/evaluate/): inspect support in the actual SDK language/version; grade state effects as well as final response and relevant tool use. |
| Native Swift evaluation | Read the available `evaluate-swift` skill if installed, or Apple's current Evaluations documentation and installed SDK. Keep native app/device execution in its owning harness; an external runner can consume its results. |

Status checked 2026-11-15: OpenAI's **hosted Evals dashboard/API and graders for eval
workflows** are read-only with shutdown scheduled for **November 30, 2026**; consult the
[deprecation notice](https://developers.openai.com/api/docs/deprecations) before recommending
them. The separate `openai/evals` Python repository is not the hosted service. Matt Pocock's
[Evalite](https://github.com/mattpocock/evalite) is archived and no longer maintained; its
recommended Langfuse migration adds a server and has feature gaps. Recheck status when used.

## Minimal custom runner contract

Keep the runner in the existing project and language. Swift, Rust, Go or Zig applications can
expose an existing CLI/API or artifact adapter without relocating business logic into Python.
Preserve the production prompt/tool definitions, response processing, session semantics and
relevant effects. A simplified prompt call is a component eval, not the full product harness.

- Freeze a run manifest: case/dataset and grader revisions, candidate/baseline revisions,
  environment/fixtures, model/configuration and limits. Record requested and served model when
  available. Hash relevant artifacts; a mutable model alias or seed alone is not reproducibility.
- Give each scheduled `(run, case, repetition, attempt)` a stable identity. Keep all scheduled
  cases visible, including skipped, cancelled, unavailable and errored ones. Do not silently
  replace an earlier attempt, omit an empty result, or count zero executed cases as passing.
- Keep candidate inputs separate from held-out labels, grading instructions and expected
  effects. Reset workspace, database, conversation, memory and relevant caches between trials;
  identify intentionally shared state. A worktree isolates edits, not untrusted execution.
- Bound concurrency, case/run deadlines, model/tool/judge calls and spend using authorized
  limits. A timeout must cancel or contain ongoing work and attempt cleanup; merely stopping
  the caller's wait leaves cost and effects running. Record unresolved cleanup explicitly.
- Validate outputs, then run deterministic graders and the needed calibrated semantic judges.
  Distinguish candidate failures, serving/harness failures, grader failures and missing evidence.
  Apply critical requirements independently of weighted quality scores.
- Persist redacted per-attempt evidence before aggregation. Keep raw outputs/logs in the
  approved private store, with artifact references in the result. Report observed usage/cost;
  unknown cost stays unknown. Include judges, retry overhead and cached usage where applicable.
- Retry only under a declared policy with safe reset/idempotency. Preserve the original error
  and attempt, and distinguish infrastructure recovery from giving the candidate another try.
  Never automatically repeat an ambiguous external mutation.

Conceptual flow, **not a framework API**:

```text
manifest = freeze(cases, candidate, baseline, graders, environment, limits)
schedule = identify_every_case_and_repetition(manifest)
for each scheduled trial within bounded concurrency and budget:
    record_started(trial)
    try: reset_state(); outcome = invoke_actual_adapter(trial, deadline)
    catch: record_execution_error(trial)  # retained in run accounting
    if output/effect evidence exists: record_independent_grades(trial, outcome)
    finally: cancel_remaining_work(); record_cleanup_result(trial)
mark_never_started_trials_with_reason(schedule)
report_attempts_errors_coverage_and_paired_outcomes(schedule)
exit_using_the_declared_policy_without_hiding_missing_evidence()
```

Compare baseline/candidate on matching cases and report relevant slices and uncertainty.
Repeated attempts on one case are not additional independent cases. Rescoring recorded
outputs can validate grader changes but cannot establish fresh model behavior or latency.
For Inspect, use its [log API](https://inspect.aisi.org.uk/eval-logs.html.md), starting with
headers/summaries; consult [error and retry semantics](https://inspect.aisi.org.uk/errors-and-limits.html).
Preserve the small result manifest and failure evidence required for reproduction, then remove
only task-owned temporary environments, transient traces and caches under the agreed retention.
