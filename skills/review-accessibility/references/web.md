# Web journeys

Use the product's required WCAG version/level and audience. When unspecified, WCAG 2.2 A/AA
is a useful review lens, not an invented legal or release requirement. Map a confirmed issue
to its actual criterion; APG patterns are implementation guidance, not conformance certification.

Start with the user's task and select relevant observations:

| Area | Evidence that matters |
| --- | --- |
| Keyboard and focus | Reach and operate controls, logical order, visible/unobscured focus, skip/repeated-region navigation, no unintended trap. Composite widgets follow their keyboard model, not necessarily one Tab stop per item. |
| Dialog/navigation | Focus enters an appropriate element, background is unavailable while modal, closing restores a sensible location; route changes and removed triggers have a deliberate focus destination. |
| Semantics | Actual accessible name/role/state, headings/landmarks and reading order. Native buttons/links before custom roles. Accessible name includes the visible label where required for speech input. |
| Forms/authentication | Persistent labels/instructions, programmatically associated errors, useful recovery and retained data. Inspect password-manager/paste support, redundant entry and accessible authentication requirements when relevant. |
| Dynamic results | Status/loading/error announcements arrive at the right time without flooding speech. Focus moves only when the workflow calls for it. Visible and accessible state agree. |
| Visual access | Contrast in actual states/backgrounds, non-color cues, text resize/reflow, text spacing, focus/target geometry. Check the criterion's exceptions instead of imposing arbitrary pixel rules. |
| Motion/media | Reduced-motion behavior, pause/stop controls, captions/transcripts/audio description appropriate to the content and applicable criterion. No essential information available only as motion, color or sound. |
| Touch/drag | Operable target size/spacing and alternatives to dragging or complex gestures where required; test mobile assistive behavior separately from desktop keyboard access. |

For WCAG 2.2 AA, distinguish text resize (1.4.4), reflow (1.4.10), focus not obscured
(2.4.11), dragging alternatives (2.5.7) and target size minimum (2.5.8). Read their exact
thresholds and exceptions when reporting a violation. Tables/maps can have meaningful
two-dimensional exceptions; a blanket ban on all horizontal scrolling is inaccurate.

Use the installed axe integration or equivalent in the existing harness. If none exists,
do useful browser/semantic/manual inspection before proposing a dependency. Capture the
actual route, viewport, state, frames/shadow roots reached and tool results including
`incomplete`/needs-review items. A scan of the initial DOM misses dialogs and later errors.
Do not enable reduced motion solely to conceal an animation's real accessibility defect.

Exercise relevant browser/screen-reader combinations with actual speech/braille observations
when available. A DOM snapshot or role selector is not a screen-reader session. Record
browser/OS/AT versions and which interaction was observed; leave unavailable combinations
untested. W3C explicitly notes that APG examples need interoperability testing and do not
establish mobile/touch support.

Primary sources, checked 2026-11-15: [WAI evaluation](https://www.w3.org/WAI/test-evaluate/),
[WCAG 2.2](https://www.w3.org/TR/WCAG22/),
[conformance scope](https://www.w3.org/WAI/WCAG22/Understanding/conformance),
[APG support limitations](https://www.w3.org/WAI/ARIA/apg/practices/read-me-first/).
