---
name: design-directions
description: "Research and compare visual directions for an app, website, screen or feature using current-product inspection, Mobbin inspiration and platform guidelines. Propose five distinct mockups by default, recommend one and refine the selection."
---

# Design directions

Use for exploring a visual direction or comparing alternatives on web or native platforms.
Keep implementation/review of an already chosen design in its existing platform workflow;
a small fix or faithful Figma implementation does not need five alternatives.

Produce reviewable mockups in the requested design tool or a local prototype using available
tools. A design-only request stops with the selected design and its decisions. If the user
also authorized implementation or delegated the choice, continue within that scope.

**The user's prompt wins.** Prompts are usually long and specific: the apps to research,
the number of directions, the range, what stays fixed, the product rules. Treat everything
in the prompt as settled. The defaults below apply only to what it leaves out. Ask only
about gaps that would change the design.

## 1. Brief

Read the actual product, its instructions, design-system owner and relevant current screens.
Write a compact brief on the overview page or alongside the mockups:

- **Problem and audience:** what the user should be able to do, and who it is for.
- **Area:** the exact screen or part of a screen being explored ("the bottom area only",
  "Home only"), or, for a new feature, that its placement is open.
- **Fixed:** what must stay as it is, and the product rules the user gave (for example,
  "Recent opens the chat, Created opens the detail, so they must look different").
- **Platform:** intended device, input methods, supported OS/SDK or browser and layout range.
  Infer from the project; do not default every task to iPhone or impose web conventions on Mac.
- **Defaults** unless the prompt says otherwise: five numbered directions, from an evolution
  of today to a more exploratory but usable alternative. Keep all five credible candidates.

## 2. Audit, research and mock

Read [research and comparison](references/research-and-comparison.md) for Mobbin screen/flow
research, evidence limits, five-direction differentiation and rendered verification. Inspect
the returned images; turn relevant observations into explicit decisions for this product.
Read current official guidance for the target platform before choosing its navigation,
controls or materials. For Apple work use the relevant HIG pages and, when available,
`design-swiftui`'s platform reference; for web use semantic HTML, WCAG and the existing stack.

Read the selected project’s design-system and asset guidance before building mockups.
An iteration can reuse valid research and boards.

Preserve the distinction between today's supported behavior and proposed additions.
Directions should differ in meaningful structure, hierarchy or interaction, respect the
requested area and use the existing design system. Hold the user task, content and constraints
constant so comparisons are fair. Color swaps alone are not distinct directions. If source or assets are unavailable, identify assumptions
rather than presenting a speculative mockup as the shipping app.

## 3. Present

Show all five mockups with stable numbers. For each: its idea, linked reference and what was
adapted, main tradeoff, and any behavior/data beyond today. Recommend one using the actual
task, brand, platform fit, accessibility and implementation cost; do not invent usability scores.
Invite a number or combination when selection is needed. Honor a selection or delegated
choice already given. The detailed comparison stays with the artifact.

## 4. Branch and refine

Keep earlier comparison rounds reviewable using the tool's pages or versions. Name the new
round after the move ("Shelves · pills on top"); do not overwrite alternatives still in use.
Support these moves:

- **Keep / replace:** "keep 1 and 2, replace 3–5". Copy kept directions unchanged, and give
  replacements new numbers.
- **Combine:** "B with the pills from C". One direction built from the named parts.
- **Expand:** "do the 5 steps again" or "five more based on this". A new set from tame to
  extreme, with the chosen direction as the base.
- **Tweak:** a specific change to one direction. Show it next to the version before it.

Also, while refining:

- Apply new product rules ("all items use consistent labels") across the whole round, and add them to
  the brief sticky.
- When a decision applies beyond this screen ("this avatar treatment should work
  everywhere"), record it with the design decision and link to the existing design-system
  owner. Do not create a competing brand guide or write private product details to global memory.
- Answer conceptual questions ("what categories could smart shelves use?") in chat. Add
  boards only when asked.
- After changing boards, read them back from the canvas to check that they render and that
  the numbered additions match their legend.

## 5. When the user picks

Add a **Decision** page to the canvas:

- the chosen boards and version (for example, "G2-A/B, with additions");
- behavior: what each tap, filter, and state does;
- visual rules and reusable rules;
- components to reuse, and new ones needed;
- open questions, and corrections (for example, a "today" claim that turned out to be
  false).

Save the choice and artifact link in the product's existing decision location, when within
scope. Report verified rendered states and any missing access. Continue implementation only
when already authorized; otherwise finish the design deliverable.
