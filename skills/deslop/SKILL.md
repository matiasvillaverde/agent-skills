---
name: deslop
description: Simplify completed code changes and prune low-value tests while preserving behavior. Use for an end-of-task cleanup pass or an explicitly scoped simplification.
---

# Deslop

Leave the work easier to read, change, and trust. Prefer a small, clear implementation
and a few meaningful tests. Readability matters more than fewer lines; deletion counts
and coverage percentages are not success criteria.

## Scope and approach

- Use the user's named scope; otherwise review the changes made for the current task.
  Inspect the diff and surrounding code, callers, and tests before editing. A dirty
  worktree is not permission to clean up everyone else's work. If the task's changes
  cannot be identified, ask for scope rather than assuming the whole repository.
- Follow the owning project instructions. Preserve behavior, public contracts, error
  semantics, side effects, and meaningful ordering. Keep security, validation at trust
  boundaries, data integrity, accessibility, and supported compatibility intact.
- Apply clear improvements directly within the authorized scope. An explicit review
  or audit-only request stays read-only. Keep uncertain cases and briefly explain why.
- Use one focused pass. Do not add a review framework, new dependencies, permanent
  audit documents, or unrelated refactors. An already-clear change needs no edits.

## Simplify the implementation

- Remove wrappers, indirection, speculative configuration, and abstractions that add
  no useful policy, boundary, or clarity. Single-use code often belongs inline, but a
  well-named helper can still make a complex operation understandable.
- Reduce unnecessary nesting with clear guard clauses or straightforward control flow.
  Preserve cleanup paths and evaluation order. Avoid dense one-liners and nested ternaries.
- Reuse an existing implementation when it fits. Keep small duplication when extracting
  it would couple unrelated concepts or require flags, callbacks, or generic machinery.
- Remove unreachable branches and redundant internal checks only when their redundancy
  is established. Keep real recovery paths; do not turn a supported failure into success
  or remove a fallback merely because the happy path works.
- Remove comments that restate the code and names that obscure intent. Keep explanations
  of constraints, tradeoffs, surprising behavior, and necessary workarounds.
- Remove imports, helpers, and test support made unused by this cleanup. Do not rename,
  reformat, or reorganize unrelated code for consistency alone.

## Fewer, better tests

For a candidate test, identify the observable behavior it protects, the plausible
regression that makes it fail, and where its expected result comes from. Prefer an
independent specification, known example, or external contract over the implementation
computing its own expected answer.

- Keep distinct behaviors and failure modes. Multiple layers need separate tests only
  when they expose different risks, such as transport, persistence, or lifecycle behavior.
  A broad integration test does not automatically replace a focused regression test.
- Remove or consolidate duplicate scenarios, assertions that cannot detect a failure,
  tests of implementation mechanics, and mocks that supply the very behavior asserted.
  Read the full test and its owner first. Before deletion, identify the surviving proof
  of the same behavior or establish that the assertion has no meaningful contract.
- Prefer explicit, named tests. Do not introduce parameterized tests or generated
  matrices unless requested or required by the project. For existing tables, prune rows
  only when they add no distinct boundary or failure mode; do not expand useful tables
  into duplicated tests solely to change their style.
- Keep fixtures and setup understandable locally. Remove test-only exports, wrappers,
  flags, and helpers when no surviving contract or caller needs them. Do not redesign
  production code just to make a test easier to write.
- Add a test only for a concrete gap in retained behavior or a credible regression
  existing coverage cannot catch. Prefer improving existing coverage. Do not add tests
  for trivial mechanical edits, to mirror a deleted helper, or to restore a coverage number.
- Preserve independent security, API, protocol, migration, storage, concurrency, and
  historical regression contracts. Slow, static, or private does not mean worthless.
  A failing test is a possible defect, not a cleanup opportunity; never delete or weaken
  it, its assertions, or snapshots merely to make the suite pass.

## Verify and finish

Establish relevant baseline behavior before changing a nontrivial path or removing its
tests, using trustworthy results from the current task when available. If a candidate
test fails or cannot run, investigate or leave it in place and report the limitation.

After edits, run checks appropriate to the changed behavior and all required project
checks. Reuse still-valid results; repeat or broaden checks only when changes or failures
justify it. If cleanup causes a regression, fix it or undo that cleanup. Do not change
test gates, coverage thresholds, or project policy to make this pass succeed.

Briefly report the meaningful simplifications, why removed tests were redundant, and
the checks actually run or relevant gaps. If nothing warranted a change, say so.
When invoked within a larger task, return to that task's remaining work.

## Inspiration

Original local synthesis of [Karpathy Guidelines](https://github.com/multica-ai/andrej-karpathy-skills/blob/main/skills/karpathy-guidelines/SKILL.md),
[Sentry Code Simplifier](https://github.com/getsentry/skills/blob/main/skills/code-simplifier/SKILL.md),
and [Deslop's test-value guidance](https://github.com/MrZoyo/deslop-GPT/blob/v0.3.4/skills/deslop/references/test-smells.md).
These are provenance links, not runtime dependencies.
