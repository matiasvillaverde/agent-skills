---
name: verify-mcp
description: Verify an MCP server or client against its claimed protocol, real operation outcomes and representative agent tasks. Use for compatibility, failure recovery, response bounds or measured MCP performance checks.
---

# Verify MCP

Separate protocol compatibility, business correctness and agent usefulness. Report each
claim at the level the evidence supports; connection success or a high audit score cannot
stand in for all three.

## Define the claim and safe target

Identify the implementation/revision, SDK, protocol version, transport, target host,
environment and requested behavior. Read existing checks and the owning contract. If the
scope is a particular regression, test that boundary instead of creating an exhaustive
matrix. Preserve the baseline and reproduction before any requested fix.

Discover installed tools and their supported versions. Use an existing SDK client or MCP
Inspector for focused requests; use official conformance scenarios when they fit the
claim. Read [verification methods](references/methods.md) for tool selection, conformance
limits and task evaluation. Do not silently install a probe, launch a paid agent evaluation
or load-test an external service.

Use disposable fixtures or an explicitly authorized target for writes and fault injection.
Establish actual tool effects from the contract; names and `readOnlyHint`/
`destructiveHint` annotations do not make live probing harmless. A local process can still
reach production through its credentials.

## Exercise the relevant boundaries

Choose cases from changed behavior and plausible failures, recording what is inapplicable
or untested. Typical boundaries include:

- Discovery, selected version/lifecycle, capability/extension fallback, schemas and errors.
- Correct arguments/results, empty or missing objects, bounded pages and continuation;
  filtered subsets must not be described as complete inventories.
- Caller/account isolation, unauthorized resources or handles, expired credentials and
  applicable HTTP Origin/header/token checks.
- Upstream rejection, throttling, malformed responses, timeouts, cancellation and cleanup.
- Persisted effects, duplicate/replayed requests, interrupted writes and reconciliation.

Validate actual wire results against the selected revision, not only SDK return types.
Distinguish HTTP/JSON-RPC failures, tool-level `isError`, and a successful empty result.
Check the model-visible content as well as structured output. Inspect whether pagination,
artifact links, MIME types and partial-result markers work in the intended client.

For mutations, compare before/after state through an independent read or receipt. An
accepted request is not necessarily completed work. If a timeout occurs after dispatch,
reconcile status before any repeat. For cancellation, observe downstream state and owned
resource cleanup separately from the client's cancellation notification.

## Check agent usefulness

Select realistic tasks that distinguish the tools under review: finding a precise item,
following a bounded continuation, correcting an input error, or completing a reversible
fixture mutation. Define the answer/state and allowed effects before running them. Include
an unavailable or unauthorized case when it is relevant to the contract.

Give the agent the interface and normal task context, not an implementation answer key.
Measure tool choice, valid arguments, recovery, final answer/state and prohibited effects.
Record client/model/settings, fixtures and tool surface so comparisons are meaningful.
Do not require ten questions, many calls, exact wording or a particular model by default.
If no agent runner is available, report scripted checks as scripted checks.

For latency, load or context-cost questions, read
[performance measurement](references/performance.md). Keep server overhead separate from
model/task cost, and preserve correctness while comparing output size or tool granularity.

## Report supported conclusions

Lead with the tested claim and important findings. Attach the target/revision, executed
cases, observable evidence, failures and untested boundaries. Separate required checks,
optional extensions, skipped checks and baselined failures. Do not widen a known-failure
baseline to manufacture a pass. Keep raw payloads, credentials and private traces in the
owning evidence store; publish only the necessary sanitized summary.

Save compact reproduction/results, stop owned clients/servers/load and restore temporary
settings. Remove task-owned raw captures, fixtures and caches after analysis; preserve
required failure evidence and shared data. Verify cleanup on failed probes too.
