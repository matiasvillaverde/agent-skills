# Apple localization

Read the installed Xcode/SDK and deployment targets before choosing APIs. Retain existing
`.strings`, `.stringsdict`, String Catalog or generated-accessor conventions. Newer catalog
features do not by themselves authorize raising a deployment target or migrating resources.

- Find actual targets, packages, frameworks, extensions, resource tables and bundles. A
  translation in the application bundle does not prove a package/extension loads it.
- Build the affected supported targets to refresh compiler-discovered strings. Extraction
  can miss plain `String` values, dynamic keys and custom APIs; inspect their render sites.
  `Text`'s runtime `String` overload differs from its localizable-key overload. Casting a
  runtime value to a key does not make it statically extractable.
- Keep deferred localizable resources/descriptors where supported when text must resolve
  under the consumer's locale. Resolve in the correct bundle/table. Use generated symbols
  only when enabled in the owning project and supported by its toolchain.
- Add comments and typed interpolations before translation. Preserve plural/device
  variations, substitution identity and source review state. Do not manually mark compiler
  extraction states or generated files contrary to the project's generator.
- Include permission descriptions, widgets, menus, settings, accessibility labels/values,
  error recovery and App Intent presentation where owned. Accessibility identifiers are
  stable test identities; they are not localized spoken labels.
- Use the view/request's intended locale, calendar and time zone for formatting. Global
  `.current` values can ignore preview or per-view overrides. Inspect the existing formatter
  boundary rather than replacing an explicitly chosen domain time zone with device defaults.

Use the owner's export/import/generation process. Review removed keys before cleaning
catalogs: another target, dynamic caller or distribution variant may still use them.
`xcstringstool compile --dry-run` only describes prospective output. Real resource compilation
and a target build establish different evidence from catalog JSON validation.

Run the changed journey using scheme language/region overrides or the existing test plan.
Check expanded text, Dynamic Type, plural branches and relevant RTL behavior. Do not mirror
every image or media control mechanically. Review the actual exported/compiled bundle when
debug and release package paths differ. Keep native-language/region review separate from
machine draft, syntax and screenshot checks.

Xcode 27's agent translation workflow adds contextual generation; it still calls for review
and iteration. Use only if the project has it and external model use is within scope. An
older toolchain remains a valid supported workflow.

Primary sources, checked 2026-11-15: [Apple's catalog workflow](https://developer.apple.com/videos/play/wwdc2025/225/),
[agent translation and review](https://developer.apple.com/videos/play/wwdc2026/213/).
Match API availability to the installed SDK. For SwiftUI implementation details, use the
existing `design-swiftui` localization reference when that skill is available.
