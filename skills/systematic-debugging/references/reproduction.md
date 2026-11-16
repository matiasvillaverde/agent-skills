# Reproduction, flakiness and regression isolation

Capture the real command, revision/artifact, input, clock/locale/config and relevant runtime
conditions privately. Preserve the failing seed/order when available. Separate a product
failure from a wrong oracle, missing tool, stale build, unavailable dependency or harness
bug. Minimize input and setup while demonstrating that the reduced case still fails.

Compare a working and failing case along a plausible axis: revision, data, feature flag,
dependency, concurrency, architecture or configuration. A difference identifies a lead,
not automatically a cause. Verify the hypothesis with a discriminating experiment and
recheck the original case. Use temporary instrumentation with bounded volume; observation
can perturb scheduling, so disappearance under a debugger is evidence with alternatives.

For intermittent tests, retain every attempt and actual failure rate/sample count. A
single rerun pass does not resolve the bug. Examine shared state, order dependence, clocks,
ports/files, background tasks and cleanup. Prefer observable synchronization to longer
sleeps. Check that assertions express the contract before relaxing them. Quarantine or
retry is a temporary mitigation with an owner and follow-up, not correctness evidence.
[pytest flakiness](https://docs.pytest.org/en/stable/explanation/flaky.html).

Use bisect when known-good/bad revisions and a stable oracle exist. Prefer an isolated
worktree so unrelated changes remain intact; account for old toolchain/dependency state.
`git bisect run` treats 0 as good, 1–127 except 125 as bad, 125 as untestable, and other
statuses as abort. Shell 126/127 errors can therefore misclassify a revision. Validate
the harness/tools first and map infrastructure failures explicitly. A build failure is
bad if that is the bug being investigated; otherwise justify skip. Do not use universal
`make || exit 125` when investigating a build regression. Inspect real producer exit
status through logging pipelines. Finish/reset only the owned bisect state.
[Git bisect](https://git-scm.com/docs/git-bisect).

Keep one independent expectation for the failure and recovery; do not derive expected
output by calling the same implementation. Do not fix nondeterminism by sorting user-visible
results unless the contract permits it. Report root cause versus mitigation clearly.
Clean owned artifacts after retaining minimal unresolved evidence; never erase the only
reproducer or shared caches as a generic debugging step.

2026-11-15 additional source review (original additions, no text copied):
[playbook debugging](https://github.com/syv-ai/agentic-coding-playbook/blob/102450ad0d89d281a1b5f6a383ce5e8bb0f9cc82/skills/systematic-debugging/SKILL.md)
(root license not established) and
[Loom debugging](https://github.com/cosmix/loom/blob/45b04001d708072a3484be7c32a80d5bd6a78c89/skills/loom-debugging/SKILL.md)
(MIT) contribute useful taxonomy, minimization and differential-testing ideas. Fixed
attempt limits, mandatory TDD/full-suite loops, overconfident cause claims and incorrect
bisect/pipeline advice were excluded. Existing imported attribution remains in NOTICE.
