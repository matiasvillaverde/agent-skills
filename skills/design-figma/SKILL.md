---
name: design-figma
description: Inspect Figma designs and implement their layout, assets, states and interactions using the project's existing UI and design system. Use for Figma URLs, node IDs or design-to-code work.
---

# Design from Figma

Use the requested file, frame or selected node as the design source. Inspect the existing
UI, framework, design system and supported platforms before implementing. Preserve the
user's scope; a request to inspect a design does not authorize changing it or the codebase.

For faithful implementation, the selected design is already the direction: do not substitute
five new options or unrelated Mobbin inspiration. When the user asks to explore alternatives,
use `design-directions` when available for research, five comparable mockups and a recommendation.
Treat any proposed new behavior separately from the current product contract.

## Retrieve the actual design

Discover the available Figma tools and their current arguments. Extract the file and node
identity from the supplied link; use desktop selection only when the available tool supports
it. For setup or access problems, read [MCP configuration](references/figma-mcp-config.md).
For tool capabilities, read [tools and prompts](references/figma-tools-and-prompts.md).

Fetch structured design context and a screenshot of the exact target or variant. If context
is truncated, fetch metadata to identify the needed children and retrieve those nodes; do
not implement missing sections from a partial response. A screenshot supplies appearance,
while component properties and constraints help explain behavior and layout.

Retrieve the supplied assets through the supported asset surface. Use the returned assets,
including valid local asset URLs, instead of adding an icon package or approximating an
available asset. If an asset or state is unavailable, state the gap rather than claiming
fidelity. Do not install or reconfigure the integration incidentally.

## Implement in the existing system

Treat generated React, Tailwind or other output as design evidence. Translate it into the
project's framework and conventions, including native UI when applicable. Reuse existing
components, tokens, typography, layout primitives and interaction patterns. Map Figma
variables to their application-owned equivalents; keep brand decisions in their existing
owner rather than creating another token catalog or scattering constants through views.

Preserve routing, state management and data-fetching architecture. Extract a component or
shared token when it gives a useful reusable concept, not merely because generated code
repeats a value. Add types and comments where they clarify a contract or a real constraint;
do not require boilerplate documentation for every export.

Read the target platform's current official guidance for affected controls and interactions.
Apple work needs the appropriate iOS, iPadOS or macOS HIG and exact supported SDK declarations;
web work needs browser semantics and responsive/accessibility behavior. A Figma frame is not
evidence of API availability or a reason to reproduce phone geometry on a desktop target.

Implement meaningful loading, empty, error, disabled and interactive states within scope.
Keep keyboard access, focus, readable contrast, responsive layout and supported content
sizes intact. Resolve conflicts with existing tokens or accessibility deliberately; explain
material deviations instead of silently changing the design or forcing literal pixels.

## Verify the result

Compare the rendered target with its Figma screenshot: hierarchy, spacing, type, color,
assets and relevant viewport behavior. Exercise the primary interaction and important states;
visual similarity alone does not prove functioning behavior. Use the project's existing
verification tools and required checks. Report what was inspected, what works, and any
unavailable access, assets or states that limit the result.

This skill consolidates the local `figma` and `figma-implement-design` workflows.
The original [license](LICENSE.txt) and supporting Figma references are retained.
