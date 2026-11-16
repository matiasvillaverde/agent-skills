---
name: build-api-connector
description: Add an API connector or provider using the repository's existing integration architecture, implementing only the needed operations.
license: MIT
---

# Build an API connector

Start with the host repository's current integration pattern. Inspect representative
connectors and their callers: layout, configuration, authentication, error semantics,
pagination, timeouts, retries, registration and test fixtures. Prefer the current
maintained pattern over a legacy example. If there is no existing pattern, use the
owning contract and the simplest integration that satisfies the request.

Identify the required operations and verify their actual vendor API/version. Do not
implement the entire provider API or add another generic client framework for one
integration. Reuse existing transport, auth and mapping facilities where they fit.

Keep external input validation at the integration boundary. Preserve rate limits,
cancellation and deadline propagation. Bound pagination and concurrency. Retry only
when the failure and operation permit it; a timed-out mutation may have succeeded and
needs reconciliation or established idempotency before replay.

Complete the wiring the application actually needs: configuration, discovery or
registration, mapping, errors and useful examples. Keep credentials in the project's
existing stores; avoid logging headers, tokens or whole provider payloads.

Verify one meaningful success path and the important provider failures using existing
fixtures or an authorized sandbox. Derive expected results independently; do not test
only a mock that repeats the implementation. Add a focused contract/regression test
where it provides durable evidence. No mandatory new test framework or fixture matrix.

The result should look native to the repository. Report the implemented surface,
verification, provider assumptions and any live behavior not exercised.
