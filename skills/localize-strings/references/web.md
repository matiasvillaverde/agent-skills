# Web localization

Preserve the project's i18n stack and locale-selection contract. Inspect server rendering,
client hydration, middleware, worker jobs and cache boundaries; a browser-only setup does
not establish safe server behavior.

- Use extractable complete messages and the existing typed catalog access. Trace UI copy
  in configuration objects, data modules, validation helpers and toast/error maps. A lazy
  message descriptor can resolve when rendered; a translated string stored at module import
  may freeze the first language and fail later switches.
- Bind locale to the request/render context. Concurrent SSR requests must not mutate a
  shared active-language singleton. Server/client initial messages and formatting preferences
  must agree. Check locale-sensitive cache keys and HTTP caching using the owning contract.
- Set document/fragment language and writing direction correctly. Language alone does not
  imply `dir`. Use logical CSS properties where appropriate; isolate unknown-direction
  interpolations with appropriate `bdi`/`dir=auto` markup. Test mixed names, numbers and links.
- Preserve application-owned rich-text placeholders; escape text and validate allowed links
  at their actual trust boundary. Do not turn a translation into unreviewed raw HTML.
- Respect explicit language choice and the supported fallback chain. Do not substitute
  generic browser-language negotiation for a product's country, account or app preference
  policy. Regional variants and Chinese script distinctions can carry intended meaning.
- Format dates/numbers through the existing Intl/ICU boundary with explicit domain currency
  and intended zone. A numeric epoch, locale string and calendar date are different types.

Select the installed stack's checks; these are examples, not a migration prescription:

| Existing stack | Evidence to obtain |
| --- | --- |
| Lingui | `check sync` checks extraction/catalog agreement; `check missing --mode catalog` checks the locale itself before fallback; compilation checks consumable messages. Verify these commands exist in the installed version. |
| FormatJS | Existing extraction, missing/structural verification and compile commands; preserve placeholder types and rich-text tag structure. |
| i18next or another stack | Existing resource/type generation and missing-key/plural checks; inspect fallback and dynamic-key handling explicitly. |
| Product-owned runtime | Its surface manifest, schema/compiler and generated-byte checks; no competing third-party scanner. |

Inspect include/exclude patterns and actual `.tsx`/template coverage. A full catalog only
describes discovered messages. Do not treat warning-only lint as a blocking gate, or
resolve findings by exempting every uppercase/data/config string. Check all required
locales according to product policy without silently accepting English fallback as translation.

Verify a changed message through the running route and its errors, accessible name and
locale switch where present. Inspect reflow and focus after translation; source checks
cannot assess reading order or whether an idiom fits its audience.

Primary sources, checked 2026-11-15: [Lingui CLI](https://lingui.dev/ref/cli),
[ICU messages](https://unicode-org.github.io/icu/userguide/format_parse/messages/),
[W3C inline bidi](https://www.w3.org/International/articles/inline-bidi-markup/).
