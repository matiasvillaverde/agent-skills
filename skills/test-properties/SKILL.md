---
name: test-properties
description: "Write, review and debug property-based tests for meaningful invariants, transformations, parsers and stateful contracts. Use for generator design, weak properties or shrunk counterexamples in the project's existing PBT framework; not for binary fuzzing or UI testing."
---

# Property-based testing

Use the owning project's instructions and existing test framework. Apply this skill
when a meaningful invariant or regression warrants it; do not create tests that
mirror trivial implementation or add an unrelated refactor to expose a property.

An example test asserts one point. A property asserts a rule over the whole input
domain and lets the generator hunt for the counterexample. That trade is worth making
when the code has an algebraic shape — an inverse, an invariant, an oracle — and not
otherwise. Code with no such shape gets example tests; saying so is a valid outcome.

Check first whether the shape is missing or merely buried. A calculation wrapped in I/O,
a string built by concatenation, an in-place mutation — each has a property and no seam
to assert it through. See [references/refactoring.md](references/refactoring.md) before
concluding there is nothing to assert.

## Property catalog

| Property | Formula | Where it applies |
|---|---|---|
| Roundtrip | `decode(encode(x)) == x` | Serialization, conversion pairs |
| Inverse | `f(g(x)) == x` | encrypt/decrypt, compress/decompress |
| Oracle | `new(x) == reference(x)` | Optimization, refactoring, reimplementation |
| Idempotence | `f(f(x)) == f(x)` | Normalization, formatting, sorting |
| Invariant | Holds before and after | Any transformation, contract state |
| Easy to verify | `is_sorted(sort(x))` | Complex algorithms with cheap checkers |
| Commutativity | `f(a, b) == f(b, a)` | Binary and set operations |
| Associativity | `f(f(a,b), c) == f(a, f(b,c))` | Combining operations |
| Identity | `f(x, e) == x` | Operations with a neutral element |

Choose properties by the wrong behavior they exclude; there is no universal strength
ordering. A roundtrip can pass when encoder and decoder share the same mistake, and a
sorting check needs value preservation as well as order. Use independently specified
examples or an independent oracle where algebraic properties leave a meaningful gap.
For an untrusted parser, documented rejection and freedom from unexpected crashes can
be a useful contract. Do not add a dependency or restructure production solely to invent
a stronger-looking property.

## The two ways a property test asserts nothing

- **Tautology.** `assert add(a, b) == a + b` restates the implementation; no bug they
  share can fail it. Pick a property that constrains the function without recomputing
  it. Note the exception: `f(x) == f(x)` is a genuine determinism property when `f`
  is not obviously pure — serializers over dicts or sets, hashing, anything reading
  the clock.
- **Inadequate exercised domain.** Heavy filtering can leave little useful coverage or
  trigger the runner's health/exhaustion failure; contradictory assumptions must not be
  counted as a pass. Inspect accepted cases, discards, skips and final status using the
  selected framework. Prefer generators that produce valid inputs directly, and check
  that an implication's precondition is reached when its assertion matters.

## Where to look next

Load the one that matches the task in front of you:

| Task | File |
|---|---|
| Writing new tests, designing strategies | [references/generating.md](references/generating.md) |
| The code has no property to assert yet | [references/refactoring.md](references/refactoring.md) |
| Reviewing existing property tests | [references/reviewing.md](references/reviewing.md) |
| A property test just failed | [references/interpreting-failures.md](references/interpreting-failures.md) |
| Library choice, Echidna and Medusa | [references/libraries.md](references/libraries.md) |

## Introducing PBT to a project that lacks it

If the project already uses a PBT library, write the tests in it. Otherwise follow
the project's dependency policy and existing user authorization. Explain the property
and dependency cost; ask only when that decision is not already authorized. An
ordinary example-based regression test may be sufficient.
