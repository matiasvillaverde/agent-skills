---
name: review-accessibility
description: Review accessibility through complete user journeys on web, Apple/native apps and command-line interfaces. Use for keyboard/focus, screen-reader, text-size, contrast, motion, form and media barriers, with explicit automated and manual evidence limits.
---

# Review accessibility

Find barriers that prevent people from understanding, operating or completing the requested
journey. Match the review to the actual platform, audience and product requirements.

## Define the review surface

Read repository instructions, supported platforms, design/accessibility requirements and
existing findings. Identify the changed or requested journey, its entry point, completion,
errors and recovery. Include dialogs, overlays, authentication, third-party handoffs and
generated content that are necessary to finish it. Select representative states by risk;
do not invent an all-platform/device matrix for a small change.

Discover the available browser/native tools, assistive technologies and existing test
harness. Use the configured tools, read their current capabilities and respect the
project’s tool restrictions. If only source or an accessibility tree is available,
continue useful inspection and mark runtime, spoken-output and human usability gaps.

An audit request permits review; apply fixes when the user requested them. Preserve product
behavior and existing authorization for test data or external actions. A checkout or send
journey can be exercised through a safe test endpoint; do not submit real transactions or
messages just to demonstrate accessibility.

Read only relevant platform guidance:

- [Web](references/web.md): WCAG scope, native semantics, keyboard, ARIA and browser evidence.
- [Apple/native](references/native.md): VoiceOver, Dynamic Type, Inspector/XCTest and device limits.
- [CLI/TUI](references/terminal.md): terminal interaction, plain output and assistive compatibility.

## Gather complementary evidence

Walk the journey with the relevant input/assistive mode. Check discoverability, names,
roles, values, reading/focus order, activation, state changes, errors and completion.
Inspect the rendered interface alongside the semantic tree; an element's presence in a
test selector does not establish a useful name, spoken sequence or operable action.

Run existing automated checks on meaningful reached states. Record tool/version, rules,
context, exclusions and incomplete/manual-review results. Inspect keyboard operation,
screen-reader output, text enlargement/reflow, contrast, motion and non-color cues where
they affect the journey. Automated scans, static lint, screenshots and direct assistive
testing are different evidence; never relabel one as another.

Follow failures to the shared component or content source. Prefer native semantics and
preserve platform interaction conventions. Fix the underlying focus/action/state problem
rather than hiding an essential control from accessibility or adding a label that masks
misleading behavior. Localize new accessible copy through the existing catalog.

## Retest and report

For an authorized fix, repeat the failed step through completion and a relevant neighboring
path; rerun the affected check. Add a focused regression assertion when it can reliably
protect the defect. Keep manual steps for meaning, announcements or physical interaction
that the harness cannot establish. Narrow suppressions need the actual false-positive reason.

Report each material barrier with affected people/task, reproducible state and environment,
observed versus expected behavior, evidence and actionable fix. Reference the applicable
criterion/platform guidance when supported; distinguish a usability recommendation from a
standards failure. State completed journeys, tested assistive combinations and gaps.

Do not give a universal accessibility score, fixed percentage of defects automation catches,
or a compliance guarantee from sampled checks. WCAG conformance involves full pages and
complete processes; a component fix or clean scan supports only its demonstrated scope.
