---
name: design-codebase
description: Design module boundaries or review a diff for structural regressions, unnecessary complexity and maintenance costs. Use for architecture decisions, boundary refactors or code-structure review.
license: MIT
---

# Codebase design

Prefer a small, understandable interface that hides useful implementation detail.
Judge the design by what callers must know and what a maintainer must hold in mind,
not by file size, number of classes, or minimum line count.

## Establish the actual pressure

For a design or refactor request, use the workflow below. For a review-only request,
inspect the named diff or module and report findings without editing. Implement only
within the user's authorized scope; a review does not replace correctness, security
review or runtime verification.

Read the owning guides, callers, current implementation and relevant tests. Identify
what is hard to change or understand today. Preserve existing behavior and public
contracts unless changing them is part of the request. A clear implementation is a
valid outcome; do not invent an architecture problem to solve.

## Choose the simplest useful boundary

- Keep a coherent responsibility together. A function or module may be a better
  boundary than another service, package, protocol or class.
- Try the deletion test: if a wrapper disappeared, would callers lose a useful
  concept, invariant or compatibility boundary? If not, it may only add indirection.
- Keep helpers that give a domain concept a useful name, even when called once.
- Expose operations callers need; keep incidental representation and sequencing
  inside the owner. Do not move complexity into a larger configuration object.
- Add variation points for real requirements or an existing external boundary.
  Hypothetical future implementations do not justify a factory or interface.
- A little obvious repetition can be cheaper than an abstraction joining unrelated
  responsibilities. Share stable meaning, not merely similar syntax.
- Prefer composition and language-native functions, enums and data types. A named
  design pattern is useful only when its benefit exceeds its additional concepts.
- Validate at real trust boundaries. Avoid repeating validation between internal
  calls that already share a proven invariant.

For a consequential decision, compare the simplest direct design with the strongest
alternative. Explain caller complexity, ownership, compatibility and the cost of
changing course. Do not create design panels or documents unless useful to the task.

## Verify the boundary

Exercise observable behavior through the meaningful interface. Tests should survive
internal refactoring while still detecting wrong results and important failures.
Remove an old test only when its distinct contract or regression is covered by
surviving evidence, or the behavior was deliberately removed. A smaller interface
can need fewer tests; test count is not a design target.

Keep the refactor within the requested scope, preserve unrelated work, and run the
owning checks affected by the change. Report the reduced complexity and any tradeoff.

## Review an existing change

Check the diff, surrounding code, real callers and owning contracts. Look for a concrete
burden: pass-through layers, speculative variation, feature policy in shared infrastructure,
duplicated sources of truth, deep nesting, hidden side effects, or tests coupled to private
mechanics. Consider resource and telemetry costs only where a real path supports the concern;
unmeasured performance suspicions remain hypotheses.

Verify each finding against contrary evidence. Give its location, consequence and smallest
useful remedy; separate new regressions from existing debt and required fixes from optional
improvements. Preserve error behavior, side effects, ordering and compatibility in proposed
changes. File size and repeated conditionals are clues, not mandates to split or abstract.
Zero findings is valid. Do not add stylistic nits, review panels or extra approval rounds.
