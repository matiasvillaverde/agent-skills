# Implementation plan template

Use the owning project's plan location and format. Keep small changes small.
A plan must be understandable without the conversation that produced it.

## Problem and outcome

State the observed problem, affected users or system, and behavior after the fix.
Cite the strongest file/line evidence. Separate confirmed facts from assumptions.

## Current state and constraints

Identify relevant files/symbols, architecture decisions, supported versions, and
existing changes. Record the source revision and any relevant uncommitted content;
a commit ID alone does not describe a dirty working tree. Link the owning guides.
Never include secret values or private customer content.

## Scope and approach

Name the affected component and necessary changes. Explain dependencies and risks.
Reuse existing contracts, patterns, and tools. Preserve unrelated work. Do not
invent a branch, worktree, commit, issue-publication, or approval requirement.

## Steps and verification

For each meaningful step, state the change and the check that establishes its
behavior. Use commands actually found in the owning guide or project metadata.
Include behavioral regression tests where warranted, not tests that restate the
implementation. Avoid redundant checks that add no evidence.

## Completion and unresolved decisions

List observable completion criteria, checks actually run, and remaining gaps.
When source or assumptions have changed, reassess the plan against current evidence.
Resolve routine changes within existing authorization; ask only for consequential
missing decisions. Follow the owning workflow for any release or live operation.
