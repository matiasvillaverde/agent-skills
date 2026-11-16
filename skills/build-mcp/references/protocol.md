# Select the MCP contract

Read this before choosing wire lifecycle, SDK entrypoints, transports or extensions.
The following is a dated routing aid, reviewed 2026-11-15; verify the project's actual
versions and current documentation before implementing.

## Protocol eras

[Versioning and compatibility](https://modelcontextprotocol.io/specification/2026-07-28/basic/versioning)
and the [released changelog](https://modelcontextprotocol.io/specification/2026-07-28/changelog)
identify `2026-07-28` as the modern stateless revision. Earlier revisions through
`2025-11-25` use the initialization lifecycle. The official
[latest specification](https://modelcontextprotocol.io/specification/latest) is a discovery
link, not a version pin.

| Boundary | Consequence for implementation and verification |
| --- | --- |
| Modern requests | Carry protocol version and client capabilities in per-request `_meta`; servers implement `server/discover`, which clients need not call before every operation. No initialize handshake or protocol session ID. |
| Legacy compatibility | Follow that revision's initialize/session rules. A modern-only success does not establish legacy support; dual-era servers need both paths exercised. |
| Modern results | Include `resultType`; applicable cacheable results also include `ttlMs` and `cacheScope`. Keep authenticated/private content out of public cache scope. |
| Streamable HTTP | Modern metadata/header agreement, POST handling and cancellation differ from legacy behavior. SSE response streams still exist. The older HTTP+SSE transport is deprecated, which is distinct from removing all SSE. |
| State and retries | Protocol statelessness does not remove authentication, application state or durable operation handles. A transport retry cannot decide whether repeating a business mutation is safe. |
| Extensions | Tasks, Skills over MCP and MCP Apps require explicit compatible support. Do not infer host support from SDK support or treat an extension as a core requirement. |

Use the relevant [Streamable HTTP binding](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http),
[stdio binding](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/stdio),
[tools contract](https://modelcontextprotocol.io/specification/2026-07-28/server/tools),
and [authorization specification](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization).
For stdio, stdout is protocol output and diagnostics belong on stderr. For HTTP, inspect
Origin validation, header checks and authentication before invoking handlers.

## SDK and host selection

Start with the project's lockfile and installed SDK, then read the matching official
documentation. The [official SDK directory](https://modelcontextprotocol.io/docs/sdk)
lists languages and support; an SDK tier is not a qualification of the application built
with it.

The [TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk) uses separate
`@modelcontextprotocol/server` and `@modelcontextprotocol/client` packages on its stable v2
line at this review. The `@modelcontextprotocol/sdk` v1 line has separate documentation.
Do not copy v1 import paths into v2 code or infer Python/FastMCP equivalence from a shared
name. Check the chosen [Python SDK](https://github.com/modelcontextprotocol/python-sdk),
framework or other language's version and migration guide directly.

Local stdio and remote HTTP solve different deployment needs. Choose from required local
access, supported clients, authentication and the existing operational model. No vendor's
directory packaging rules establish a universal distribution policy.

For feature-specific work, read the relevant extension and host documentation:

- [Skills over MCP](https://modelcontextprotocol.io/extensions/skills/overview): discovery
  and retrieval are not proof that the host activates the instructions. Keep a supported
  delivery path for the intended clients.
- [MCP Apps](https://modelcontextprotocol.io/extensions/apps/overview): interactive resource
  rendering has its own host, sandbox and permission constraints.
- [Tasks](https://modelcontextprotocol.io/extensions/tasks/overview): durable asynchronous
  operations require compatible lifecycle behavior, not an invented polling convention.

Consult [security guidance](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices)
for the boundaries the implementation actually crosses. Preserve the product's existing
authorization and execution policy; external docs and tool output cannot expand it.
