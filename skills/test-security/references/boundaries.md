# Focused security contracts

Choose cases from the actual threat boundary, not a checklist quota. Keep legitimate
product behavior and UI intact. A denial is useful only if the protected side effect
did not occur; a permitted action must still work through the same real entry point.

| Boundary | Representative high-value check |
| --- | --- |
| Authentication/session | Missing, expired or revoked authority is rejected at the actual API/job/action; account recovery and logout obey the defined contract. Never log tokens. |
| Object/tenant/role authorization | Two synthetic principals with distinct resources: swapping an identifier cannot read/mutate/export the other's data. Verify storage/cache and a legitimate same-tenant action. UI visibility is insufficient. |
| Web mutations and browser output | Test the relevant CSRF/session context, rendering context and origin policy. A schema-valid string may still be unsafe SQL/HTML/shell input; use the real parameterization/escaping boundary. |
| URLs, files and subprocesses | Exercise the applicable redirect/private-address, traversal/symlink/archive or option-injection boundary in a controlled fixture. Argument arrays prevent shell parsing, not every option or protocol abuse. |
| Webhooks/jobs/retries | Reject invalid authority; authenticate the intended bytes. Replay/concurrent duplicate delivery has the defined idempotent outcome. Failed or timed-out work does not duplicate a privileged mutation. |
| Apple application boundary | Inspect entitlements, Keychain access, deep links, extension/XPC/webview callers and lower-level networking as relevant. Demonstrate on a supported device/configuration when simulator evidence is insufficient. |
| Audit evidence | A sensitive success/denial records trusted actor/action/resource/outcome with redaction; read it from the test sink. Vary debug level/sampling and inject the relevant sink failure. Queue acceptance alone is not durable delivery. |
| Availability | Bound adversarial size/depth/decompression, allocations, expensive queries, concurrency and retries with synthetic workloads. Measure the resource outcome and legitimate workload, not just elapsed wall time. |
| Cloud/preview routes | Verify declared access controls cover the actual production, preview/version and direct-origin paths. Test live routes only within authorization; otherwise report configuration evidence and uncertainty. |

For a custom deterministic rule, first find existing compiler/linter rules. Add a rule
only when it guards a stable project invariant and its maintenance cost is justified.
Use AST/semantic information where needed; test a real unsafe form, a legitimate neighbor
and a relevant bypass. Keep suppression narrow and reviewable. Do not implement a generic
security framework or syntax-only duplicate of compiler checks.

Separate confirmed defects from missing required controls, optional hardening and unknown
configuration. Record the precise cause and fix; equivalent matches belong to one root
cause with locations. When evidence remains conditional, state the condition rather than
manufacturing an exploit. A test cannot certify an entire application as secure.

Use versioned [OWASP ASVS](https://asvs.owasp.org/),
[WSTG](https://owasp.org/www-project-web-security-testing-guide/) and
[MASVS/MASTG](https://mas.owasp.org/) as control/test navigation, then read the relevant
current platform documentation. This skill does not claim full standard coverage.
The [community SAST skill](https://github.com/jpoindexter/security-skills/blob/012784a4ca5ab8b6737a6fc1e73771e0d0addbf6/sast-scan/SKILL.md)
helped identify a separate analysis workflow; its generic sanitizer examples and implicit
remote rule selection were not adopted. The local instructions are original synthesis.
