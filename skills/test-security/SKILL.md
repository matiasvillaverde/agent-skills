---
name: test-security
description: Verify security boundaries with deterministic analysis, focused abuse cases and regression tests. Use after a feature or security fix, or to add useful SAST, authorization, audit-log and native-safety checks to existing CI.
---

# Test security

Turn a concrete security contract into reproducible evidence and a durable check.
Test depth follows exposure and the change; a large generic test matrix is not the goal.

## Choose the contract and environment

Read repository instructions, the change, known findings and existing test/CI ownership.
Identify the relevant principal, resource, operation, untrusted input and required outcome.
Inspect source and configuration to choose meaningful cases. If the boundary is unclear,
use `review-security` when available; do not substitute a scanner pack for understanding.

Establish a local or explicitly authorized test environment with synthetic accounts/data,
bounded time/concurrency/resources and observable side effects. Inspect build hooks and
test setup before execution. Isolate untrusted code without ambient credentials; a new
directory alone is not a sandbox. Do not scan third-party targets, attack production,
send real notifications or mutate customer data under a generic testing request.

Load [analysis tools](references/analysis.md) for SAST/native checks and
[boundary tests](references/boundaries.md) for scenario selection. Use existing tools and
frameworks. Do not implicitly install scanners, upload source or enable hosted analysis.

## Gather deterministic evidence

Run the smallest relevant existing analysis configuration. Record tool/rules versions,
language/target coverage, files checked, parse errors, timeouts, exclusions and suppressions.
For unfamiliar rules, inspect them first. A successful command with no parsed files or
applicable rules is incomplete. Keep raw findings/source excerpts in private reports.

Trace each important match through input, guards and privileged use. A regex match is
not an exploit; a generic type/schema check is not necessarily a valid sanitizer.
Explain preconditions and counterevidence. Preserve unknown deployment state as unknown.
Route credential scanning to `scan-secrets` and published package issues to
`audit-dependencies` when available; do not count their outputs as SAST coverage.

## Exercise the broken boundary and a legitimate path

Prefer a realistic integration test for authorization, tenant isolation, webhook handling
or audit delivery. Use a small unit/property/fuzz test for an isolated parser, encoding or
policy invariant where it adds distinct evidence. Choose the fewest cases that protect
different failure modes; avoid Cartesian parameterized suites and snapshot-only checks.

Demonstrate the unsafe behavior before the fix when feasible in the isolated fixture,
then demonstrate rejection after it. Verify absence of unauthorized side effects and
continued legitimate behavior, not only an error code. Include a relevant failure/retry
or concurrency path when it can bypass the same control. Bound fuzzing and fault injection;
retain a minimal regression input when a real defect is found.

Validate required audit events through the actual test sink, including trusted identity,
redaction and delivery failure. Required security evidence must survive diagnostic level
changes and sampling. Check availability abuse when relevant: bounded payload/work,
timeouts, cancellation, fan-out, retry amplification and memory/CPU/GPU use. Avoid arbitrary
universal limits; use the product's actual contract and supported clients.

## Keep the gate useful

For requested CI changes, reuse the owner and existing required checks. Qualify detection
with a positive fixture, a safe neighboring case and a scanner/configuration failure.
Separate tool failure or incomplete coverage from findings; do not hide either with
`|| true`. Use changed-surface checks for feedback and an appropriate wider cadence.
Pin reviewed rules/tools, review narrow exceptions and prevent PR configuration from
silently disabling the gate. Do not create a new CI system or weaken mandatory checks.

Return the contracts exercised, commands/versions, outcomes, findings, gaps and evidence
location. Passing checks establish only their tested scope. Preserve UI and legitimate
product behavior; escalate a required product-policy change rather than quietly changing
it to make a test pass. Remove task-created disposable fixtures/caches after preserving
useful evidence, without deleting existing logs, incident evidence or recovery artifacts.
