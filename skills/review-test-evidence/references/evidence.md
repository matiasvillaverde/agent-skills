# Match the evidence to the claim

| Surface | Evidence that can support the claim | Countercheck |
| --- | --- | --- |
| Web/native UI | Actual rendered state and interaction on the named build, meaningful accessibility/DOM observations, lifecycle and persisted-result checks. | An image may be stale; a snapshot may serialize text differently. API-only success does not prove the user could complete the UI flow. Device/Simulator evidence has different scope. |
| iOS/iPadOS/macOS | UI automation receipts/screenshots, app/device/build identity, relaunch state, relevant crash/log evidence; measured device performance when claimed. | Swift unit tests do not cover UI. Do not turn a Simulator pass into real hardware qualification or silently bypass a permission/confirmation dialog. |
| CLI/TUI | Exact invocation and input, independent exit status/stdout/stderr, output content, file/state changes and child cleanup. | Final pipeline status, shell-wrapper success or expected text alone may hide failure. Noninteractive mode cannot prove terminal interaction. |
| API/backend | Actual request/response, valid fixture/auth identity, readback or durable effect, appropriate pagination/completion. | 2xx is not business success; wrong account/read replica/stale cache can confuse evidence. Repeated POST is a bug only under the specified contract. |
| MCP | Version/client/transport identity, discovery plus actual invocation, complete result/error semantics and tool effect. | JSON-RPC success or tool listing is not tool success. Match protocol-era/capability rules; partial/input-required/pending output is not completed work. An MCP App's UI requires host/UI evidence too. |
| Job/pipeline/artifact | Related run IDs, terminal outcome, content/format validation and downstream effect; recovery/duplicate checks where claimed. | Job accepted, file present, or old successful log cannot prove this run finished correctly. |
| Tests/scans/profilers | Actual executed scope, valid baseline, failure/skip/error counts, tool version, raw relevant result and target. | Exit zero with zero files/cases, fabricated counts, missing samples, parse errors or unrelated targets cannot establish coverage. |

Use a claim ledger only as detailed as the task needs. A useful row contains the claim and
requirement source, target, evidence inspected/replayed, actual outcome, limits and next action.
Do not build a second reporting system when the project has a suitable existing format.

## Contradictions worth resolving

- A save toast conflicts with fresh-session readback: inspect the stored effect and cache scope.
- An empty report conflicts with known matching input: check execution coverage and tool failure.
- Tests pass but a documented workflow fails: reproduce the workflow; inspect what tests omit.
- A test fails on a legitimate alternative: check whether the assertion encoded implementation
  choices or an invented requirement.
- Agents agree on an expected answer: independently check the requirement/oracle; agreement is
  not correctness. For numerical results include relevant tolerance/unit assumptions.
- A failure disappears on retry: keep the original observation; check timing, reset and resources.
- A tool's error payload is wrapped in a successful transport: preserve the application error.

For any new surface, identify its public contract and observable final effect. Review that
evidence using the same logic; unsupported tools/hardware stay gaps, not simulated passes.
