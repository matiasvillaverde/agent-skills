# Choose the real user interface

Select the relevant rows; mixed products may need more than one. Record versions and environment.
Use repository commands and supported tools; do not invent flags, selectors, transports or API names.

| Interface | Exercise | Evidence and limits |
| --- | --- | --- |
| Web | Real navigation and core flows; keyboard/focus when relevant; reload/back, stale tabs, loading/empty/error states and supported viewports. Discover controls from the rendered page. | Actual visible outcome plus response/state/content proof where needed. Wait for a named state, not arbitrary sleeps or universal network idleness. A successful direct API request does not prove the browser flow works. |
| iOS/iPadOS/macOS or another native app | Installed named build on the intended device/Simulator. Launch, interact, dismiss/cancel, background/foreground and relaunch when relevant. Exercise denied/granted permissions using existing test controls. | Screenshots/accessibility state, observable saved data and crash/hang evidence. Record OS/build/device and simulator status. XCTest UI tests or available device automation can drive Apple apps; Swift Testing unit success is not UI evidence. Simulator observations do not prove real-device performance, radio, GPU or hardware behavior. |
| CLI/TUI | Execute the actual binary with representative args/stdin/files; inspect exit status, stdout and stderr separately. Try cancellation, noninteractive input, malformed data, paths/permissions or broken downstream pipe when relevant. | Parse output/artifact content, compare before/after state and check child-process termination. Piped shell status can hide a failing command. PTY and non-PTY behavior are distinct; do not declare a prompt broken merely because it legitimately requires interaction. |
| API/backend | Use documented auth and schemas; complete multi-step operations, read back state, paginate and check wrong-owner/invalid-input rejection where relevant. | Status/body plus durable effect; a 202 or queued ID is not job completion. Do not assume every repeated POST must deduplicate: test the specified guarantee. |
| MCP | Connect through the intended supported client and transport. Discover the server's advertised tools/resources/prompts as applicable, then use their actual schemas to complete a user task. | Record protocol/client/server versions, capability scope, tool result and actual effect. Successful JSON-RPC transport is not successful tool execution: inspect tool errors, partial/input-required results and structured content under that revision. A discovery-only run does not validate calls. |
| Job/pipeline/artifact/library | Trigger through its documented entrypoint, follow completion, inspect produced content and downstream state. For a library use a small consumer through its public API. | Check selected recovery/restart/retry and content correctness, not file existence or process launch alone. Mock-only wiring must remain labeled; unavailable real integrations stay unverified. |

## MCP version and capability checks

Inspect the protocol revision actually used and its matching official specification. Do not apply
one era's handshake rules to all servers: legacy revisions use initialize/capability negotiation,
while newer revisions use per-request version/capability metadata and discovery. Test the supported
compatibility contract; a tool does not need every optional capability in the latest specification.
For claimed pagination, cancellation, progress, resources, prompts, elicitation or task extensions,
exercise a representative flow using the client's actual support and report unsupported paths.

Check whether tool names/descriptions and schemas let a fresh caller choose and call the right
operation. Inspect bounded, actionable output: truncation, pagination and partial results must be
clear; avoid a fixed universal token limit. Test error recovery without silently changing args,
permissions or server configuration. Stdio diagnostic output must not corrupt protocol stdout.
Direct server calls cannot prove an MCP App's embedded UI or the intended host's approval flow.

## A new platform

Identify its public entrypoint, user goal, completion signal, persistent effect, lifecycle and
observable failure. Map the same experiment to those capabilities. If tools or hardware are absent,
report the missing evidence and continue independent checks; do not manufacture a simulated pass.
