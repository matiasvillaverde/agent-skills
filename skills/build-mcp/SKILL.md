---
name: build-mcp
description: Build or change an MCP server around useful agent tasks, bounded tool contracts and the protocol versions its clients support. Use for MCP tools, resources, transport or integration changes.
---

# Build MCP

Make the requested task possible with a clear, small tool surface and verifiable effects.
Preserve the project's language, architecture, deployment and supported clients unless the
requested change requires a different choice.

## Establish the contract

Read the owning instructions, existing server, dependency lockfiles and relevant client
configuration. Identify the task, caller, environment, upstream service and allowed effects.
Infer settled choices from the project; clarify only decisions that change implementation.

Record the supported protocol revision, SDK/package version, transport and host combination.
Read [protocol and SDK guidance](references/protocol.md) before choosing lifecycle or auth
APIs. A new specification does not authorize an existing integration's migration. Use
current primary documentation for the chosen versions; do not combine examples from
different SDK majors or protocol eras.

## Design useful operations

Start from representative tasks and the evidence that proves them complete. Reuse the
existing API/domain layer; keep MCP adaptation separate from business rules. Prefer clear
operations with specific schemas. Add workflow tools or discovery for a large catalogue
when they reduce demonstrated task cost, without hiding authorization or partial effects.
Do not expose every upstream endpoint just because it exists.

For each operation, make these decisions explicit where they affect callers:

- When to choose it, especially over similar tools; required inputs, formats and constraints.
- Read/write effects, identity/account scope, preconditions and how completion is observed.
- A useful default result, stable identifiers, result bounds and a continuation/detail path.
- Correctable errors, retry conditions and what an interrupted mutation means.

Use resource or artifact retrieval for large content when the target host can consume it.
Do not return unusable links or arbitrarily cut serialized JSON. Bound collection work as
well as returned bytes; preserve valid schemas and mark incomplete results. Return enough
context to make the next decision without repeated detail fetches. Measure the tradeoff
instead of imposing universal page sizes, totals or character ceilings.

Provide `outputSchema` and conforming `structuredContent` for structured results where
supported. Follow the selected revision's compatibility guidance for text content; inspect
what the actual host shows the model, including duplicate text/JSON. Keep discovery ordering
deterministic and cache scope/freshness accurate for caller-specific data.

## Implement boundaries and recovery

Let the SDK handle protocol mechanics; keep its transport separate from domain execution.
Distinguish a JSON-RPC protocol failure from a tool execution failure (`isError`). Give
errors a stable, bounded explanation and a safe next action; avoid raw upstream bodies,
secrets and stack dumps. Preserve the API's existing error taxonomy rather than creating
a competing one for MCP.

Enforce access per caller and operation in code. Tool annotations describe behavior; they
do not grant authority. Validate resource handles, paths and URLs against the caller's
scope. Use the selected auth specification for token audience, issuer, discovery and
redirect rules. Keep credentials outside model arguments and logs.

Apply explicit timeouts and cancellation to downstream work where supported. A cancelled
request or lost response does not prove a write was undone. Reuse the owning service's
idempotency and reconciliation contract; expose an outcome/status lookup when necessary.
Do not automatically replay an ambiguous mutation. Test cleanup of processes, streams and
other resources the adapter owns.

## Verify the delivered behavior

Run the project's focused checks and exercise the changed operations with an actual MCP
client at each claimed compatibility boundary. Check representative success, invalid
input, upstream failure, result bounds and state effects using owned fixtures. Then use
the requested host when available to check tool discovery and a realistic task. A script
calling RPC methods is useful evidence, but is not an agent task evaluation.

For independent verification or performance claims, use `verify-mcp` when available; this
skill does not require installing another tool or contacting a hosted model. Report the
implemented surface, versions tested, observable outcomes and remaining compatibility gaps.
Building a server does not itself authorize deployment, directory submission or account
configuration.

Save compact verification evidence, stop owned servers/clients and remove task-created
fixtures, raw captures and caches after analysis. Preserve shared data and required failure
evidence; verify cleanup even when a probe fails.
