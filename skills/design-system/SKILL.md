---
name: design-system
description: Organize a product's brand, tokens, assets and shared UI around clear source ownership. Use to consolidate scattered styling, evolve a design system, propagate theme changes across platforms or prevent design drift.
---

# Design System

Make each shared design decision editable in one authoritative place, with a traceable
path to the interfaces that use it. Preserve the product's identity and native behavior.

When the user requests a new brand or visual direction, research comparable products and use
`design-directions` when available to compare five grounded proposals before consolidating the
selected rules. An existing approved design or token-only consolidation does not need a redesign.
Use platform guidance to share semantic intent while retaining native controls, type scaling,
input and window behavior; one token source does not imply pixel-identical interfaces.

## Find the existing authority

Identify the requested product, brand, surfaces and scope. Read its guides, actual theme
and component code, asset sources, generators and checks. Inspect relevant Figma libraries
when available. Follow imports and build paths; a file named `tokens` is not proof it is
used. Include applicable websites, native apps, emails and exported documents in the
inventory without silently expanding the implementation scope.

Map **decision → editable source → derived output/import → consumers → check**. Distinguish
current authority, generated artifacts, historical examples and accidental copies.
Resolve conflicts from owner guidance and actual usage; ask only when a consequential
brand or ownership choice remains ambiguous. Do not create a parallel theme because the
existing one has an unfamiliar shape.

Keep distinct product brands independent unless unification was requested. A shared
component contract can support different palettes and typography. Equal values do not
establish shared meaning: a brand accent and an error color may need to change separately.

## Establish the smallest useful system

Reuse the existing module, stylesheet, asset catalog or design library where practical.
One source of truth means one owner per decision, not one enormous file or package.
Separate concerns only where they have different owners, consumers or change reasons.

- **Brand foundations:** own approved marks, color definitions, type choices, font files
  and licensing, icon/illustration conventions and relevant spacing, shape and motion rules.
  Link to canonical assets and guidance; avoid manually maintained copies of values in docs.
- **Semantic roles:** expose purpose such as surface, content, action, on-action and danger,
  including required states and appearances. Use existing naming conventions. Keep raw
  primitives private where consumers should choose intent. Add component-specific tokens
  only when a component needs an independently controlled decision.
- **Components:** reuse proven components and native controls. Extract a shared component
  for a recognizable recurring behavior with a small API and clear states. Keep layout and
  product logic local when they are not shared. Tokens alone do not define interaction,
  keyboard behavior or accessibility.

Avoid universal theme factories, speculative brand axes, giant variant matrices and
tokenizing every literal. Local geometry, content-derived values and platform system
semantics can be intentional. Centralize values whose meaning should change together.

Choose an explicit update direction between code, design tools and generated artifacts.
Mark generated outputs and regenerate them; do not edit both sides independently. Keep
handwritten platform adapters small. Introduce generation or a shared package only when
real consumers justify its maintenance cost. DTCG is an optional interchange format;
check the released specification and the installed tool's actual feature support before
adopting it. No particular design tool, CSS framework or generator is required.

For platform integration, themes, assets or enforcement, read the relevant sections of
[platforms and checks](references/platforms-and-checks.md).

## Consolidate without redesigning by accident

Migrate a coherent slice from existing values to the chosen authority while preserving
appearance and behavior, unless a design change was requested. Distinguish structural
consolidation from intentional visual changes in the diff. Update known consumers and
remove superseded sources after checking references; do not leave competing fallback
palettes. For public token/component APIs, preserve a documented migration path when
consumers cannot move together.

Keep a short owner guide at the existing documentation entrypoint: where to change brand
decisions, which consumers derive from them, the generation/check commands and how to add
a justified exception. Link agent instructions to that guide instead of copying the rules.
If design tools or other repositories are outside the authorized scope, record those
unmigrated consumers and their update path.

## Prove propagation and prevent drift

Extend existing checks at the ownership boundary. Prioritize valid references/types,
required theme coverage, fresh generated outputs and unauthorized brand definitions in
consumers. Prefer an existing parser/linter to broad text bans. Make intentional exceptions
specific and reviewable; do not hide new violations in an expanding baseline.

Verify a representative change travels from its source to real consumers. Use a safe
fixture or isolated copy for a temporary value change, or the requested change itself;
leave no demonstration edits behind. Compile affected targets and inspect representative
rendered states, supported appearances and text sizes. Check actual asset/font loading,
foreground/background combinations and interactions. Generated-file equality alone does
not prove the application uses them or that the interface is accessible.

Use focused checks for the risks changed, not a snapshot for every token or every possible
variant combination. Report covered consumers, checks actually run and skipped/unavailable
surfaces. Finish with the authoritative edit location, how updates propagate, remaining
migration debt and any intentional design changes. Do not claim codebase-wide consistency
from a partial migration.
