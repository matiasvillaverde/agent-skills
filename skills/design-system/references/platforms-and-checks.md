# Platform mappings and regression checks

Read the sections relevant to the current consumers. Verify installed versions and supported
platforms before choosing APIs. Preserve the repository's existing build and CI ownership.

## Interchange and design tools

Pin an actual published DTCG version when using the format. At the 2026-11-13 review,
[2025.10](https://www.designtokens.org/tr/2025.10/) is the latest published Community Group
Report; it is not a W3C Standard. Later drafts are not a new stable release. Its
[format](https://www.designtokens.org/tr/2025.10/format/),
[color](https://www.designtokens.org/tr/2025.10/color/) and
[resolver](https://www.designtokens.org/tr/2025.10/resolver/) modules are distinct.
For example, final color values carry a color space and components; a hex string under
`$value` does not establish conformance. Validate the types and reference features actually
used, including missing aliases, cycles and name collisions after platform conversion.

Themes/brands need deterministic override precedence and complete required roles. Resolve
contextual overrides before dependent aliases according to the chosen format. Avoid
flattening relationships so early that changing one theme cannot update its dependents.
Check every declared output, including outputs unused by the local default build.

[Style Dictionary's support page](https://styledictionary.com/info/dtcg/) reports incomplete
2025.10 support at this review. Verify the installed release and required subset; dollar
prefixed keys, basic token conversion and full resolver support are different capabilities.
Use an existing generator or direct module imports if that fits better.

Figma variables, modes, aliases and code syntax can map to code roles, but are not a lossless
representation of every token type. Code syntax is a naming aid, not generated application
code. [Variables REST access](https://developers.figma.com/docs/rest-api/variables/) has
plan, permission and scope requirements; discover actual tool access first. Use stable
IDs/mappings when reconciling existing libraries. Keep one editable owner per decision and
an explicit direction for each export; publishing shared-library changes is a separate
external action within the user's authorized scope.

## Web and server-rendered surfaces

Use the existing CSS/theme module and component library. Semantic custom properties can
express appearance without duplicating component rules. Check nested scopes and computed
values: CSS variable resolution and inheritance are not identical to static token aliases.
In installed Tailwind v4 projects, [`@theme`](https://tailwindcss.com/docs/theme) defines
utility APIs; ordinary CSS variables suit values without utility APIs. Reference-dependent
utilities may need `@theme inline`. Do not prescribe v4 syntax to a v3 project.

Include inline styles, SVG fills/strokes and application theme overrides in drift discovery,
not just hex values in CSS. Preserve intentional data visualization palettes and user content.
Use relative text sizing, suitable fallbacks and the product's font-loading approach. Verify
long text, zoom/reflow, supported writing directions and reduced-motion behavior where affected.

Email, PDF and image exports may need generated fixed values because their renderers do not
support the app's CSS/runtime. Derive those values from the same brand owner and verify their
actual output. Do not import frontend runtime dependencies into a backend merely for branding.

## Apple and other native surfaces

Keep semantic colors dynamic in their rendering environment. Map roles to named asset colors
or native system colors; do not replace system-adaptive colors with sampled hex constants.
Custom palettes need the supported appearance/contrast variants. Preserve platform spacing,
materials and controls where appropriate rather than forcing pixel-identical web rendering.

Verify resource ownership and loading. Swift package assets use their
[package resource bundle](https://developer.apple.com/documentation/xcode/bundling-resources-with-a-swift-package.md),
not an assumed app main bundle. Share approved vector/font masters; generate required formats
and sizes through the existing asset pipeline, retaining licenses and platform variants.

Use native text roles and scaling behavior. Custom fonts need correct registration/name,
weights, fallback glyphs and supported accessibility scaling. Rendering text is not proof the
intended font loaded. Apple's [typography guidance](https://developer.apple.com/design/human-interface-guidelines/typography)
distinguishes platforms; macOS does not support Dynamic Type. Do not apply one universal
scaling or px-to-pt conversion policy across Apple targets.

For other native toolkits, adapt semantic roles to their theme/resources and units. For
example, Android color/on-color pairs must stay matched; wallpaper-derived dynamic color is
a product choice. Preserve shared intent while allowing deliberate platform behavior.

## Select checks that catch real regressions

| Failure | Useful evidence |
| --- | --- |
| Broken token contract | Parse the chosen format; reject missing references, incompatible types, cycles and emitted-name collisions. Check required modes/roles and override behavior. |
| Stale or manually edited outputs | Regenerate into an isolated output directory and compare all declared outputs. Distinguish deterministic output from environment-dependent metadata. |
| Components bypass the source | Extend the existing CSS/TS/Swift or native linter at the appropriate syntax boundary. Allow literals in the owning definitions and narrowly justified exceptions. Include inline styles and assets where relevant. |
| Checks silently cover nothing | Assert intended input coverage; report missing tools, skipped targets and excluded paths. When adding a rule, exercise a real violation and a legitimate exception. |
| Runtime ignores correct generated values | Build a representative real consumer and inspect computed/rendered output or resolved native resources after a source edit. |
| Visual or behavioral regression | Review representative changed states in applicable themes/text sizes, keyboard focus and reduced motion; retain a few useful visual/interaction checks in existing tooling. |

Assess contrast on the colors actually presented together, including opacity and background
composition. [WCAG 2.2](https://www.w3.org/TR/WCAG22/) includes criteria beyond contrast and
exceptions by content/state; do not test every arbitrary palette pair or round a failing
ratio up to pass. Native accessibility needs the applicable platform/project criteria too.
Keep state distinguishable without color alone. A token validator cannot certify accessibility.

Use current tools already present when sufficient. Add a generator, custom lint rule or new
visual-test harness only for an observed gap that justifies its ongoing cost. Do not turn
design-system consolidation into a framework migration or a full new testing stack.
