---
name: design-agent-interface
description: Build or review websites, CLIs, APIs and tool interfaces that agents can discover, understand and use reliably. Use for agent-friendly content, actionable contracts and observable task completion.
---

# Design Agent Interfaces

Make the intended task understandable and completable through the interfaces the product
already owns. Treat readable content, usable actions and verified outcomes as distinct
requirements. Preserve human usability and the existing access policy.

## Start with the consumer and task

Identify the actual consumer: a fetch-only reader, browser agent, shell agent, API client
or MCP host. Inspect the existing surface, schemas, documentation and available tools.
Define the user's starting point, information needed, allowed effects and evidence of
completion. A general request to improve agent usability does not imply a new public API,
anonymous access or a new agent runtime.

Choose representative tasks that reveal current friction. Follow the interface from a
normal entrypoint and record where discovery, interpretation, action or verification fails.
Work from that evidence instead of adopting every item in an agent-readiness scorecard.

## Make capabilities and state understandable

Use clear action names and distinct descriptions. Explain when to choose nearby commands
or tools, exact input formats/constraints, identity/account scope and useful outputs.
Reuse the existing schema as authority; examples and generated docs must agree with it.
Use realistic fixture values, and distinguish placeholders from literal working values.

Provide stable references for entities and operations. Separate an empty result, missing
object, filtered subset, partial result and completed traversal. Offer bounded search,
filters and continuation when useful; make larger details retrievable without forcing
every caller to ingest them. Keep enough context to make the next decision correctly.

For public websites and documentation, read [web surfaces](references/web.md). For CLI,
API and tool actions, apply the contract appropriate to that surface:

- **CLI:** discoverable help, explicit noninteractive arguments, stable machine-readable
  output, useful exit status, diagnostics separate from result data, and bounded output.
  Do not require an interactive prompt when the task already supplies its inputs.
- **API:** accurate schemas and examples, scoped authentication, typed responses and
  errors, and documented pagination/rate-limit behavior. Reuse established HTTP semantics.
- **MCP/tools:** discriminating names/descriptions, validated inputs, bounded structured
  results and correct tool/protocol errors. Use `build-mcp` or `verify-mcp` when available
  for protocol-specific implementation or verification.

Do not replace a working interface with search/execute, code execution or another protocol
without evidence that the intended consumers benefit. A small surface often needs only
better names, examples, output and status reporting.

## Make actions and recovery observable

Expose actual state: ready, invalid input, pending, completed, failed or unknown where those
distinctions exist. Tie success to a durable record, artifact, receipt or independent read;
avoid generic success text that hides pending work. Errors should identify a correctable
condition and safe next step, with stable codes when the interface supports them.

Preserve authorization outside the model. Identity, permissions and destructive effects
must not depend on a description, UI label or read-only annotation. Reuse the owning
service's preconditions, idempotency and reconciliation rules. A timeout after dispatch
must not invite an unsafe repeat. Preview or dry-run support is useful only when it
accurately represents the subsequent action and does not weaken authorization.

## Verify usefulness through tasks

Repeat representative tasks through the real consumer surface with normal context.
Check the correct answer/state, wrong-target avoidance, recovery and unintended effects.
For web readers, inspect the returned content; for browser agents, inspect visible and
accessible state; for writes, read the durable outcome. Do not substitute a schema pass,
HTTP 200 or accessibility snapshot for completed work.

Compare observed calls/steps, returned bytes, time and repeated recovery where relevant.
Keep model/client/settings and fixtures constant for a useful before/after comparison.
Report scripted probes separately from agent-run trials and label missing coverage.

Deliver the smallest useful change and the tested outcomes, with remaining blockers.
Accessibility review, security qualification and agent-harness design remain separate
specialties; this skill does not impose those full workflows on every interface edit.

After saving compact evidence, stop task-owned helpers and remove disposable fixtures,
raw captures and task-only caches. Preserve shared data and unresolved failure evidence.
