---
name: design-swiftui
description: Review and improve SwiftUI views, state, accessibility, layout, and measured performance while preserving the project's supported SDKs and architecture. Use for SwiftUI implementation or review tasks.
license: MIT
metadata:
  author: Paul Hudson
  version: "2.0.0"
---

Review Swift and SwiftUI code for correctness, modern API usage, and adherence to project conventions. Report only genuine problems – do not nitpick or invent issues.

Include deprecated API in review findings. During feature work or bug fixes, complete the requested change and suggest unrelated modernization separately; do not apply it without being asked.

Choose the references that match the changed behavior or requested review. A full review
may use several; ordinary implementation does not require loading the whole library.
Keep `references/performance-plus.md` for a requested deep review or an established
performance problem. Read only the relevant sections of the references listed below.


## Core Instructions

- Check the project's deployment target before applying version-specific advice. Use newer runtime APIs only when the target supports them or within an appropriate `#available` check. Keep the existing target unchanged. Requirements tied to an Xcode version also need that toolchain; a runtime check cannot make an older SDK recognize a new declaration.
- Read the owning project instructions and installed Swift/SDK versions first. Confirm version-sensitive advice against that SDK or current official Apple documentation; a community reference is not proof of API availability.
- Preserve the existing Swift language mode, UIKit integration, architecture, file organization, and dependency policy unless the requested change requires otherwise.
- Reuse existing dependencies. Resolve routine choices within the user's authorization; ask only when a material dependency decision remains unapproved.
- Report demonstrated correctness, accessibility, or performance problems. Prefer measured improvements over speculative restructuring.

## Platform design and inspiration

For a new screen or visual redesign, inspect the current product and its design-system owner,
then read the target platform's current Apple Human Interface Guidelines and affected components.
Use [platform design](references/platform-design.md) for separate iOS, iPadOS and macOS decisions,
exact API availability and rendered verification. A shared SwiftUI view is not evidence that one
navigation model, density or input treatment fits every platform.

Use Mobbin MCP for relevant screen/flow inspiration when available; inspect images and cite their
canonical links. Missing native coverage calls for Apple resources and actual native examples,
not a fabricated platform filter. For an open visual exploration, use `design-directions` when
available: five distinct mockups by default, tradeoffs and a recommendation. Preserve chosen designs,
brand and behavior; a source review or small bug fix does not require a design exploration.


## Report findings or implemented changes

For a review, give each demonstrated issue's file/line, affected behavior and smallest
useful correction. Distinguish correctness or accessibility failures from optional
modernization and measured performance from hypotheses. An API preference or custom
binding alone is not a defect. Include a short code example only when it clarifies the
remedy; no per-file output or before/after block is required for every finding.

For authorized implementation, make the scoped change, run the owning checks and inspect
the affected interaction or rendered states when tools are available. Report what was
verified and any unavailable runtime evidence. A clean source review does not establish
VoiceOver behavior or a measured performance gain.


## References

- `references/accessibility.md` - Dynamic Type, VoiceOver, Reduce Motion, and other accessibility requirements.
- `references/api.md` - API modernization to check against the project's SDK.
- `references/platform-design.md` - current HIG research and separate iOS, iPadOS and macOS design/validation paths.
- `references/design.md` - applying the existing design system with native, accessible controls.
- `references/hygiene.md` - making code compile cleanly and be maintainable in the long term.
- `references/localization.md` - localizable text, resource bundles, and locale-aware presentation.
- `references/navigation.md` - navigation using `NavigationStack`/`NavigationSplitView`, plus alerts, confirmation dialogs, and sheets.
- `references/performance.md` - optimizing SwiftUI code for maximum performance.
- `references/performance-plus.md` - deeper restructuring to narrow what views depend on, reserved for deep performance reviews or diagnosed performance issues.
- `references/resizability.md` - changing window sizes, adaptive layout, and safe areas.
- `references/data.md` - data flow, shared state, and property wrappers.
- `references/swift.md` - tips on writing modern Swift code, including using Swift Concurrency effectively.
- `references/views.md` - view structure, composition, animation, reordering, and swipe actions.
