---
name: localize-strings
description: Localize user-facing strings and verify source, catalog and rendered coverage across Apple apps, web, services, CLIs and generated content. Use for new copy, missing translations, plural/formatting defects or localization regression checks.
---

# Localize strings

Follow the message from its definition to the person reading or hearing it. A complete
catalog can coexist with untranslated callers, inaccessible labels or incorrect formatting.

## Establish the existing contract

Read the owning product instructions, localization guide, surface inventory, catalogs,
required locales and generation/check commands. Preserve the current library, keys,
translation review states and fallback policy. Adding copy does not imply migrating the
localization framework or enabling an external translation service.

Classify strings by their actual use: authored interface copy, literal user/provider data,
machine identifiers or developer diagnostics. Trace ambiguous data/config values to their
consumers. Include errors, empty/loading states, notifications, accessibility text, permission
descriptions, emails and exported artifacts where the task reaches them. Do not translate
wire enums, JSON field names, command flags, paths or a person's original content.

The project’s localization guide and manifests own source coverage, catalog compilation
and debt. Use the existing gate and registered check profiles. Extend its
parser or surface contract for a demonstrated gap; do not add a competing regex scanner,
broad directory exemption or growing baseline. A green regression gate with existing debt
does not establish completion.

## Author complete messages

Use the existing extractable API with named/typed substitutions and translator context:
where the message appears, intended action or meaning, placeholder roles and protected
terms. Keep sentences and plural/select branches translatable as units. Preserve existing
key identity unless meaning changes; update source/context bindings when it does.

Use the runtime's locale plural rules, including relevant zero/fraction/ordinal behavior.
Keep message language, formatting region, calendar, time zone and currency independent.
An amount's currency comes from its domain data; a locale only changes its presentation.
Do not parse localized display strings back into machine values.

Keep rich-text slots and escaping under application control. Translator text and interpolated
content are data, not arbitrary HTML, commands or format programs. For mixed-direction text,
use platform bidi isolation at presentation boundaries; preserve original identifiers/data.

Read the matching reference:

- [Apple](references/apple.md): catalogs, extraction, bundles, native rendering and review.
- [Web](references/web.md): extraction, request isolation, fallback, HTML language/direction.
- [Services and artifacts](references/renderers.md): backend errors, CLI output, mail and documents.

## Verify and report

Check source discovery, catalog validity, required-locale completeness, typed placeholders,
context freshness and generated output separately with existing tooling. Compile the actual
resources and build the affected targets. Successful extraction or a dry run is not compilation.
When changing a gate, demonstrate a real missing/invalid message is caught and its legitimate
neighbor accepted; include a relevant parser/configuration failure so skipped files stay visible.

Exercise the affected journey with representative supported language/region combinations:
a longer translation, applicable RTL/mixed text, plural boundaries, a time-zone boundary or
locale switch only where each addresses a different risk. Inspect visible and assistive text,
layout and error paths. Avoid multiplying every locale by every screen without a reason.
Pseudolocalization finds extraction/layout defects; it does not prove idiomatic translation.

Report changed surfaces and locales, checks actually run, translation review state, remaining
debt and runtime/language-review gaps. AI-produced translations remain drafts until the
owning review process establishes otherwise. Never mark catalog entries reviewed merely
because a compiler or another model accepted their shape.
