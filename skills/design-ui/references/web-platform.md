# Web design sources and checks

Use for responsive web, including React/TypeScript, server-rendered HTML and embedded web
surfaces. Framework choice does not replace browser semantics. Native app conventions belong
to their platform guides; a narrow browser window is not automatically an iPhone application.

Read the relevant parts of [responsive design guidance](https://web.dev/articles/responsive-web-design-basics),
[WCAG 2.2](https://www.w3.org/TR/WCAG22/) and the current documentation of the installed framework.
Set accessibility criteria from the product's requirements. WCAG success criteria are normative;
Understanding pages and techniques explain them. Community checklists are aids, not universal rules
for title capitalization, autocomplete, font choice, virtualization or a particular component stack.

Prefer native semantic HTML. For a custom interaction, consult the applicable
[ARIA Authoring Practices pattern](https://www.w3.org/WAI/ARIA/apg/patterns/) and implement its
keyboard behavior; ARIA attributes do not supply it. The
[APG introduction](https://www.w3.org/WAI/ARIA/apg/practices/read-me-first/) explains example and
browser/assistive-technology limits. Reuse the project's proven component before creating one.

Adapt to content, available width/height and input capabilities. Do not assume large means mouse
or small means touch. Preserve browser history, meaningful links, text selection, zoom and native
form/autofill behavior unless the actual task requires an exception. Mobile browser viewport,
onscreen keyboard and safe-area changes need actual checks where affected. Include long/RTL text
and localized content, keeping strings in their existing owner.

For changed flows, inspect the rendered page and exercise its real action/recovery states. Choose
representative evidence: narrow/wide layout, keyboard-only operation and focus, text enlargement,
reduced motion and readable composed colors. Reflow at 320 CSS px/equivalent 400% zoom for vertical
content has [criterion-specific exceptions](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html).
[Target size at AA](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html) is distinct
from the enhanced target criterion and includes exceptions; do not apply Apple's point dimensions
as CSS pixel rules. Native HTML and automated accessibility checks do not certify the whole journey.

Keep font payloads, image sizing and motion proportional to their purpose. Diagnose demonstrated
performance problems through existing tools rather than enforcing a universal list-length threshold.
Use the available browser/devtools/automation surface; do not install a new test framework just
for screenshots. State precisely which browsers, states and interactions were checked.
