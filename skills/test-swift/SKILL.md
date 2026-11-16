---
name: test-swift
description: 'Write, review and debug meaningful Swift tests using the existing Swift Testing or XCTest setup. Use for assertions, async waiting, parallel isolation, test-plan filtering or an authorized XCTest migration.'
---

# Swift testing

## Overview

Use this skill to write, review, migrate, and debug Swift tests with modern Swift Testing APIs. Prioritize readable tests, robust parallel execution, clear diagnostics, and incremental migration from XCTest where needed.

Inspect the owning project's instructions, installed toolchain, and test targets first.
Keep its deployment targets and supported test frameworks. Add tests for meaningful
behavior and regressions; do not add tests that merely mirror trivial implementation.
Load only the references relevant to the task. Confirm version-sensitive APIs in the
installed SDK or current official documentation before recommending them.

For stochastic AI/model-quality measurement with Apple's separate Evaluations framework,
use [evaluate-swift](../evaluate-swift/SKILL.md). Swift Testing assertions and passing UI tests
alone do not establish model quality; evaluation scores do not replace those deterministic checks.

## Agent behavior contract (follow these rules)

1. Prefer Swift Testing for Swift unit and integration tests, but keep XCTest for UI automation (`XCUIApplication`), performance metrics (`XCTMetric`), and Objective-C-only test code.
2. Treat `#expect` as the default assertion and use `#require` when subsequent lines depend on a prerequisite value.
3. Default to parallel-safe guidance. If tests are not isolated, first propose fixing shared state before applying `.serialized`.
4. Prefer traits for behavior and metadata (`.enabled`, `.disabled`, `.timeLimit`, `.bug`, tags) over naming conventions or ad-hoc comments.
5. Preserve the project's test style. Prefer explicit named cases for distinct behaviors; use parameterization when requested, required by the project or maintaining an existing useful table. Do not convert tests merely to reduce their count.
6. Use `@available` on test functions for OS-gated behavior instead of runtime `#available` checks inside test bodies; never annotate suite types with `@available`.
7. Keep an authorized migration incremental, preserving the same assertions, lifecycle and coverage. Traits or parameterization are separate choices, not mandatory migration stages.
8. Only import `Testing` in test targets, never in app/library/binary targets.

## First 60 seconds (triage template)

- Clarify the goal: new tests, migration, flaky failures, performance, CI filtering, or async waiting.
- Collect minimal facts:
  - Xcode/Swift version and platform targets
  - Whether tests currently use XCTest, Swift Testing, or both
  - Whether failures are deterministic or flaky
  - Whether tests access shared resources (database, files, network, global state)
- Branch quickly:
   - repetitive tests -> inspect distinct contracts and shared setup before considering consolidation
  - noisy or flaky failures -> known issue handling and test isolation
  - migration questions -> XCTest mapping and coexistence strategy
  - async callback complexity -> continuation/await patterns

## Routing map (read the right reference fast)

- Test building blocks and suite organization -> `references/fundamentals.md`
- `#expect`, `#require`, and throw expectations -> `references/expectations.md`
- Traits, tags, and Xcode test-plan filtering -> `references/traits-and-tags.md`
- Parameterized test design and combinatorics -> `references/parameterized-testing.md`
- Default parallel execution, `.serialized`, isolation strategy -> `references/parallelization-and-isolation.md`
- Test speed, determinism, and flakiness prevention -> `references/performance-and-best-practices.md`
- Async waiting and callback bridging -> `references/async-testing-and-waiting.md`
- XCTest coexistence and migration workflow -> `references/migration-from-xctest.md`
- Test navigator/report workflows and diagnostics -> `references/xcode-workflows.md`
- Index and quick navigation -> `references/_index.md`

## Common pitfalls -> next best move

- Repetitive methods -> retain distinct failure modes; consolidate only genuine duplication using the project's conventions.
- Failing optional preconditions hidden in later assertions -> `try #require(...)` then assert on unwrapped value.
- Flaky integration tests on shared database -> isolate dependencies or in-memory repositories; use `.serialized` only as a transition step.
- Disabled tests that silently rot -> prefer `withKnownIssue` for temporary known failures to preserve signal.
- Unclear failure values for complex types -> conform type to `CustomTestStringConvertible` for focused test diagnostics.
- Test-plan include/exclude by names -> use tags and tag-based filters instead.

## Verification checklist

- Confirm each test has a single clear behavior and expressive display name when needed.
- Confirm prerequisites use `#require` where failure should stop the test.
- Confirm each case protects distinct behavior and independently derives its expected result; existing tables stay bounded and diagnosable.
- Confirm tests are parallel-safe or intentionally serialized with rationale.
- Confirm async code is awaited and callback APIs are bridged safely.
- Confirm migration keeps unsupported XCTest-only scenarios on XCTest.

## References

- `references/_index.md`
- `references/fundamentals.md`
- `references/expectations.md`
- `references/traits-and-tags.md`
- `references/parameterized-testing.md`
- `references/parallelization-and-isolation.md`
- `references/performance-and-best-practices.md`
- `references/async-testing-and-waiting.md`
- `references/migration-from-xctest.md`
- `references/xcode-workflows.md`
