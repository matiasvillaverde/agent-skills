# Secrets and audit evidence

## Credentials

Inventory credential types, owners, consumers, scopes and storage locations without
printing values. Trace exposure through source/history, fixtures, bundles, artifacts,
CI output, process arguments/environment, crash reports, traces and local permissions.
Use an existing redacting secret scanner where appropriate; distinguish real credentials
from public identifiers and dummy fixtures. Do not verify suspected keys by making
live authenticated calls unless that validation is specifically in scope.
For a dedicated exposure scan, use the installed `scan-secrets` skill; it owns current,
staged, historical and artifact coverage, scanner output handling and recurrence gates.

Review separation by environment and role, expiry/revocation, recovery and dependency
impact. Reuse platform secret stores and workload identities where supported. Environment
variables are a delivery mechanism, not proof of confidentiality. A committed-secret
fix includes the owner's containment/rotation plan; deleting a string does not revoke
it. Preserve incident evidence and recovery access, and do not blindly rotate a shared
key. [OWASP secrets guidance](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
covers lifecycle, consumers, auditing and recovery.

## Audit the operation, then its delivery

Start with sensitive operations and the existing audit contract. Representative events
include privileged permission/configuration changes, credential lifecycle, account
recovery, sensitive export/delete, and security-relevant authentication/authorization
outcomes. Identify actual gaps by tracing the write and reading back a redacted fixture
from its intended sink. Infrastructure access logs alone may not show the actor or
business resource involved.

Check actor/authority, action, target, environment/tenant, timestamp, actual outcome
and correlation. Derive identity from trusted context, bound field sizes and exclude
secrets/payload dumps. Prevent log injection. Required audit events must survive
diagnostic level changes and sampling. Restrict reading/deleting records and define
retention, integrity and access monitoring. Use
[OWASP logging guidance](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)
for event selection and protection; proportionate collection avoids noise and leakage.

Use the existing application's policy for persistence failures. Determine whether the
operation must stop before committing, has a durable outbox or can continue with an
explicit detectable gap. Do not assume that queue acceptance or `flush()` proves
persistence, or that catching an exporter error preserves audit completeness. Replaying
an ambiguous business mutation to regenerate a missing log can duplicate the mutation.
Do not add synchronous remote logging to every business operation by default.

Keep optional debug verbosity configurable and cheap while preserving required audit
evidence. Bound queues, retries and event volume; expose dropped/delayed records without
recursive logging. Avoid high-cardinality metric labels. Alert on actionable patterns
or loss of required evidence with an owner and response, rather than every denial or
malformed request. Check false positives, missing-data behavior and alert recovery.

Validate a representative sensitive success and denial, redaction, level/sampling
independence and the relevant delivery failure. Add a focused integration check when
it protects a real contract. If the `observability` skill is installed, use it for
authorized implementation of signals and delivery; this review can operate without it.
Report absent code, disabled configuration and unverified sink retention as different
observations. Do not invent a compliance obligation or retention period.
