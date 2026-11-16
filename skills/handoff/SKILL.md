---
name: handoff
description: Write a concise continuation handoff when switching sessions, agents or machines, preserving decisions, working state and verified evidence.
license: MIT
---

# Handoff

Summarize the active goal, accepted scope, decisions, current working state, completed
work, verification results, remaining work and the next useful action. Preserve any
unresolved question or ambiguous external operation that must not be replayed.

Reference existing specs, issues, files, diffs and evidence instead of duplicating
them. Record uncommitted work and distinguish observation from assumption. Include
suggested skills only when they will help the next session.

Use the user-specified location, or a private temporary document outside the workspace
when no durable location is needed. Redact credentials and private payloads. Do not
start another agent, upload the file, commit changes or claim cross-machine sharing
merely because the handoff was written.

Return its path and the next step. Tailor the content to any stated focus of the next
session; the next agent should check actual repository state before continuing.
