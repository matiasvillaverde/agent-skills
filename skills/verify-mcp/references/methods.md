# MCP verification methods

## Select the instrument

| Question | Useful instrument | What it does not prove |
| --- | --- | --- |
| Can this client discover and invoke the operation? | Installed [MCP Inspector](https://modelcontextprotocol.io/docs/tools/inspector) or SDK client at a recorded version | Agent tool choice, business correctness or every supported protocol revision |
| Is the wire behavior conformant? | Relevant [official conformance](https://github.com/modelcontextprotocol/conformance) scenarios and schema checks | Production configuration, correct business effects or extensions excluded from scoring |
| Did the requested operation work? | Existing service fixture, RPC client and independent state/receipt inspection | A real model could discover and compose it |
| Can an agent complete the task efficiently? | Available host/evaluation runner with frozen tasks and outcome checks | Broad reliability from one successful trial |

Read tool help and the selected version's documentation before constructing commands.
An `npx`/`uvx` example can download and execute code; it is not evidence that the tool is
already installed. Prefer the project's existing dependencies and test entrypoints. Never
execute a third-party server just to inspect its README or schema.

## Protocol claims

Use the claimed revision of the [specification](https://modelcontextprotocol.io/specification/latest),
especially [versioning](https://modelcontextprotocol.io/specification/2026-07-28/basic/versioning),
[tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools) and the chosen
transport. At the 2026-11-15 review, `2026-07-28` uses per-request metadata and discovery;
`2025-11-25` and earlier use initialization. A test harness must send the requested wire
revision, not merely print it in its report.

The [conformance README at the reviewed revision](https://github.com/modelcontextprotocol/conformance/blob/96a6f9478b7f2e125cf0360a213383cf57533893/README.md)
documents frozen per-revision requirement sets. Inspect a set and its fixtures before
running it. Some server scenarios expect specific conformance tools, so a production
application may need a separate fixture adapter; do not add those tools to production.
Record that distinction and test the actual application surface separately.

The harness can return a successful exit status with expected failures or skipped cases.
Read the detailed checks and applicability, including wire-schema errors attributed to
the harness itself. Distinguish a required failure, optional extension failure, known
failure baseline, unsupported scenario and no executed traffic. Pin the harness revision
and preserve its output privately. A narrow focused check is not a full conformance claim.

## Outcome and task cases

Choose cases that expose a decision or state boundary. Examples to adapt:

- Two similarly named objects: the agent must select the right immutable ID from task
  context, not guess from a title.
- A result beyond the first page: the continuation must preserve filters and scope and
  make completion distinguishable from truncation or an expired cursor.
- A correctable validation error: the response identifies the failed field/constraint
  without leaking secrets; the agent can recover without broadening the request.
- A reversible fixture write: verify the durable record and caller scope; repeat only
  under the documented idempotency contract.
- An upstream timeout after a committed write: the operation remains reconcilable and
  the caller does not create a duplicate by treating silence as failure.
- A slow or cancelled operation: observe prompt cancellation handling, terminal state
  and resource cleanup; do not infer rollback from a closed socket.

Use existing evaluation infrastructure when available. Define fixture reset, allowed
tools, call/time budget and outcome checks appropriate to the task. Repeated trials are
useful when comparing model behavior; disclose sample counts and variance. Keep the agent
that performs a task from seeing expected answers or hidden fixture state.

Score observable results and harmful/unintended effects. String comparison fits a stable
identifier; it is weak for semantically correct prose, ordered workflows or durable state.
An agent's self-reported success is not an independent outcome oracle. Read-only fixtures
are convenient but cannot qualify a server's write behavior.

For security-sensitive integrations, consult the relevant
[official security guidance](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices)
and the owning product policy. This workflow checks the relevant boundaries; it does not
replace a complete security review.
