# Services, command lines, email and artifacts

Localize at the human rendering boundary. Preserve protocol fields, command names/flags,
exit codes, structured output schemas and stable error identifiers. Prefer structured
error data that a caller renders over concatenating fragments of a translated sentence.
Do not change an API compatibility contract merely to improve displayed wording.

Carry locale/formatting preferences into the actual request or job. Include them in queued
work when needed; avoid inheriting the worker machine's locale or a mutable global language.
Specify the intended time zone for scheduled events and date boundaries. Concurrent jobs
for different people should produce independent results. The locale of an administrator
viewing a record need not be the locale of its original recipient.

| Surface | Inspect and verify |
| --- | --- |
| Backend errors | Stable machine code, localized user message where contracted, escaped parameters, preserved HTTP status and safe recovery action. Debug/provider diagnostics remain separate. |
| CLI/TUI | Human help/prompts/errors and accessible plain output; keep JSON/CSV protocol fields, flags and script behavior stable. Test noninteractive output and Unicode display where relevant. |
| Email | Subject, preview, text and HTML alternatives, links, language/direction, escaped names and recipient-specific formatting. Render locally or use an authorized test sink; localization does not authorize sending mail. |
| PDF/document/export | Actual renderer, embedded font/glyph availability, reading order, selectable text, pagination, date/amount/unit formatting and localized chrome around literal content. |
| Notifications | Truncation, lock-screen wording, accessible text and deep-linked recovery in the receiving platform. |

In an existing gettext workflow, `msgfmt --check --check-format` can detect malformed
catalog/format contracts when entries carry the appropriate format flags. It does not
prove that all callers are extracted, every locale is translated, or the text is correct.
Use the actual stack's plural rules and catalog toolchain; do not introduce a universal
printf/regex placeholder validator over ICU, Apple and gettext grammars.

Verify complete rendered messages, not only key presence. Distinguish source language
fallback from reviewed translation, and translated chrome from literal quoted/published
content. Test a meaningful plural/escaping/time-zone boundary and one allowed literal value
when those are changed. Keep production recipient data and private artifacts out of Git.

Primary sources, checked 2026-11-15: [gettext format checking](https://www.gnu.org/software/gettext/manual/html_node/msgfmt-Invocation.html),
[RFC 9457 human detail versus problem identity](https://www.rfc-editor.org/rfc/rfc9457.html).
