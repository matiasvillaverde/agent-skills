---
name: design-ui
description: Research, build or refine web interfaces with coherent typography, layout, interaction and accessible states. Use for new frontend screens, visual redesigns or implementing a selected direction.
license: Apache-2.0
---

# UI design

Read the brief, existing interface, design system, real content, and supported devices. Preserve established visual language unless redesign is requested. Identify the audience and the main task; resolve material uncertainty from available context before asking. Do not invent a different product to make the design more interesting.

For a new interface or unresolved visual direction, research comparable shipped interfaces with Mobbin MCP when available and read the relevant official browser/framework guidance. Inspect the returned images and link the sources that inform decisions; do not infer interactions from a screenshot. Follow unanswered questions into flows or states instead of collecting unrelated screenshots. Disclose access gaps and use available primary references. For exploration, use `design-directions` when available to present five meaningfully different mockups and a recommendation before selection. Honor another requested count, an existing selection or a delegated choice. A focused fix or implementation of an approved design proceeds directly.

Read [web platform guidance](references/web-platform.md) for source selection, browser/input differences and focused validation. Choose a concise visual idea grounded in the subject. Describe the palette, type roles, hierarchy, spacing and layout before building; a small change needs only a small plan. Use emphasis where it helps the task. Prefer deliberate choices to a recurring template of cards, gradients, ornamental labels and section animations. Familiar patterns are useful when they suit the task.

Use typography and spacing to express hierarchy. Keep body text comfortably readable, with an appropriate line length, contrast, and line height. Structural devices should communicate grouping, sequence, or interaction. Do not add numbering to content that has no order, or badges and labels that merely repeat a heading. Reuse existing tokens and components before introducing more.

When typography is the requested exploration, compare real licensed/available fonts using identical representative content, weights, sizes and fallback glyphs. Evaluate readability and personality in the product, not a specimen word alone. Do not blacklist common fonts or substitute the brand font merely to look original.

Write concrete interface copy using the user's vocabulary. Action labels name what happens; keep that name consistent through confirmation and feedback. Explain failures with a useful recovery action. Give loading, empty, offline, success, and disabled states the attention their actual flow requires. Avoid fabricated testimonials, statistics, or product capabilities.

Implement the real interaction with the project's existing stack. Keep semantic structure, keyboard access, visible focus, responsive layout, usable touch targets, and reduced-motion behavior. Use motion to explain a state change or direct attention sparingly. Avoid dependencies, font payloads, or persistent animation whose cost exceeds their purpose. Keep CSS ownership and selector specificity understandable.

Inspect the rendered result on relevant viewport sizes using available browser or native tooling. Exercise the primary task and its meaningful states; check overflow, long content, keyboard behavior, and readable contrast. A screenshot can expose layout problems but cannot prove an interaction works. Refine the weakest part, remove decoration that adds no information, and report actual validation and any unavailable checks. Do not introduce an automation framework solely for this review.
