# Websites and documentation for agents

## Readable content and discovery

Check the site's normal entrypoint, links, final HTTP status and returned body. Public
information intended for fetch-only agents must be present without executing JavaScript.
Use SSR, prerendering or an existing content endpoint where appropriate; browser-capable
agents have different requirements. A 200 response containing an empty app shell or an
access challenge is not readable documentation.

Keep accurate first-party content at stable canonical URLs. Provide real navigable links
to relevant docs, capabilities and workflows. Make examples executable against documented
fixtures and explain relevant error recovery. Derived formats should share the same
content owner so that Markdown, HTML and schemas do not silently drift.

Optional `llms.txt`, sitemaps, Markdown alternates and JSON-LD can help a known consumer.
They are not substitutes for reachable, accurate pages or proof of task success. Add them
when discovery or representation needs justify their maintenance. Keep indexes bounded,
links working and critical facts visible; some converters omit script-based JSON-LD.

Preserve deliberate robots, firewall and authentication policies. Search/training crawlers
and user-directed agents are different audiences. A spoofed user-agent header is neither
authentication nor proof that a real provider can reach the site. Use authorized server
evidence when diagnosing actual blocking; do not disable protections to raise a score.

## Optional Markdown negotiation

If the existing framework supports a useful alternate representation, use its actual
request path and cache behavior. Check server-rendered and prerendered/static routes
separately; middleware may not run for both.

Test explicit HTML and Markdown preferences, quality values and `q=0` rejection, normal
browser requests and missing pages. Return correct `Content-Type`, status and canonical
metadata. A missing page must remain a real 404/410, not a successful prose response with
a fabricated canonical. Preserve important links, tables, code and units in both formats.

Verify cache variation for every request field that changes the representation, on both
HTML and Markdown responses. `Vary: Accept` covers Accept-driven selection; user-agent or
other detection requires its own correct cache strategy. Preserve existing `Vary` fields,
private/no-store behavior and authenticated content boundaries. Test both request orders
through the relevant cache when cache correctness is part of the claim.

Prefer explicit format negotiation to assuming every detected bot wants Markdown. Check
total task cost: smaller responses can still be worse if conversion discards needed facts.

## Browser operation

Use semantic links, buttons, labels and forms with meaningful accessible names and state.
Prefer visible text as the naming source. The same submit controls, validation messages,
loading states and completion evidence should work for people and browser agents. Avoid
controls distinguishable only by position, hover or decorative icon when the task needs
a clear target.

Verify the actual browser accessibility/DOM surface and visible result with the available
approved browser tool. An element reference from a snapshot is a temporary observation,
not a permanent product identifier. Re-observe after navigation or material state changes.
Keyboard/focus and full accessibility conformance have their own testing requirements.

## Primary sources and their limits

- [Vercel Agent Readability skill, package 0.7.0](https://cdn.jsdelivr.net/npm/@vercel/agent-readability@0.7.0/skill/SKILL.md)
  and [published package](https://www.npmjs.com/package/@vercel/agent-readability/v/0.7.0):
  useful implementation ideas, not a requirement to install its package or accept its
  crawler-policy and score defaults.
- [Vercel/Ora research guide](https://vercel.com/kb/guide/make-your-site-readable-by-ai-agents):
  distinguishes fetched answer availability from task completion, and recommendations
  from observations. Its samples do not establish universal agent behavior.
- [Vercel agent-friendly API course reference](https://github.com/vercel-labs/academy-skills/blob/8976d898ae7ddb3a648aa71c97e64eb8af9fe0f9/skills/agent-friendly-apis/references/doc-patterns.md):
  exact request, response and recovery examples; formatting prescriptions are design
  recommendations, not independently measured requirements.
- [HTTP semantics, RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html):
  media preference/quality and `Vary` semantics.
- [W3C accessible names and descriptions](https://www.w3.org/WAI/ARIA/apg/practices/names-and-descriptions/):
  distinguish controls through meaningful names and verify the computed result.

Sources reviewed 2026-11-15. Check the chosen framework, tool and provider's current
documentation when implementing; this reference does not pin a new project dependency.
