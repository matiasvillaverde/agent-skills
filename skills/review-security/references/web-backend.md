# Web, backend and deployment boundaries

Use the relevant version of [OWASP ASVS](https://asvs.owasp.org/) as a control map,
and [WSTG](https://owasp.org/www-project-web-security-testing-guide/) for test design.
Record the version when citing requirement IDs. A Top 10 list is useful orientation,
not a complete verification standard or certification.

## Follow sensitive operations

- Derive identity and tenant from verified authentication, not submitted user IDs,
  headers or form fields. Check object, action and field authorization on reads,
  writes, bulk operations, exports, subscriptions, jobs and administrative paths.
  Random IDs make guessing harder; they never replace access control.
- Inspect session expiry/revocation and recovery flows, OAuth state/PKCE/redirects,
  and JWT signature, issuer, audience and allowed algorithm. An authenticated caller
  is not automatically authorized. A hidden button is not an enforcement point.
- Trace SQL/command/template injection, unsafe deserialization, dynamic evaluation,
  mass assignment and path handling. Bind query values; validate dynamic identifiers
  separately. File metadata is attacker controlled: check actual content, limits,
  storage permissions and safe serving of uploads and extracted archives.
- For URL fetchers, validate scheme, destination and every redirect; account for DNS
  changes, IPv6 and private/link-local addresses. Restrict credential forwarding and
  response size/time. A hostname regex alone does not establish SSRF protection.
- Check transaction boundaries, duplicate webhook/job delivery, races, idempotency
  keys and ownership of retries. Validate webhook signatures against the original
  body, replay constraints and the actual destination account/environment.
- Bound decompression, parsing, pagination, query complexity, uploads, queues,
  subprocesses and outbound requests. Test representative limits with fixtures,
  not a flood of traffic. A missing rate limiter is not automatically an exploit;
  establish which shared resource an attacker can exhaust or bill.

## Browser and framework details

Review output encoding by context, sanitized rich content, DOM sinks, URL schemes,
message origins and target origins. Assess CSP and framing restrictions against the
actual app; do not mechanically add a policy that breaks required flows. Cookie,
CSRF, CORS and cache policy depend on the authentication and cross-origin model.
Choose cookie attributes deliberately; forcing SameSite=Strict everywhere can break
legitimate navigation or authentication. CORS is not server authorization.

Check personalized CDN/framework cache keys and response caching, cross-tenant
reuse, logout behavior and exposure through bundles, source maps, error payloads,
debug endpoints or serialized server objects. TypeScript types do not validate runtime
input. Fetch framework documentation for the installed version, including server-side
validation and production security configuration for Django, FastAPI or the actual stack.

[Next.js data security](https://nextjs.org/docs/app/guides/data-security) treats Server
Actions as directly callable endpoints. Verify authorization within the action or its
trusted data access boundary, minimize returned fields, and keep privileged modules
server-only. Inspect route handlers and jobs too; layout/proxy checks do not establish
all-path coverage. Account for the installed version's caching and origin behavior.

## Cloudflare and Vercel

Inspect source configuration and available live read-only evidence. If a dashboard-only
control is unavailable, list it as unverified rather than assuming it is enabled or absent.

For Cloudflare, enumerate custom domains, routes, `workers.dev`, version/preview URLs,
service bindings, storage and scheduled/queue handlers. Check authorization on every
reachable path, scoped bindings and private cache handling. Current
[routing documentation](https://developers.cloudflare.com/workers/configuration/routing/workers-dev/)
distinguishes disabling `workers.dev` from disabling other generated URLs. Verify
Access/JWT enforcement and audience for the selected route; a zone rule is not proof
that every alternate hostname shares that rule. Store credentials in
[secret bindings](https://developers.cloudflare.com/workers/configuration/secrets/),
not plain Wrangler `vars`; keep local secret files out of Git.

For Vercel, inspect preview/production environment separation, branch access, generated
URLs, deployment-protection exceptions/bypass credentials, function auth and server
bundle exposure. Verify the project's actual
[protection mode](https://vercel.com/docs/deployment-protection), including its URL
coverage. The platform's [Config/Secret types](https://vercel.com/changelog/environment-variables-now-use-config-and-secret-types)
supersede the old Sensitive toggle; verify current behavior before prescribing CLI flags.
A Secret still reaches its deployment, so application code or a public framework prefix
can disclose it. Do not download environment values just to inventory their presence.

For agents and MCPs, trace who can cause each tool action and which credential it uses.
Enforce permissions outside model-generated text. Retrieved content cannot authorize
execution, change persistent skills or expand access. Check session ownership, OAuth
resource/audience, output limits and private-network fetch boundaries. A prompt-injection
classifier or skill-marketplace badge does not prove isolation.
