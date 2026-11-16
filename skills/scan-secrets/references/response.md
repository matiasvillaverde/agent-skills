# Exposure response and recurrence prevention

Use the existing incident owner and credential lifecycle. Record locations and exposure
window without copying the credential. Establish whether the value was committed,
published, downloaded, included in CI output or distributed in an artifact. An absence
of observed misuse does not prove that nobody obtained it.

Identify the credential's provider, authority, consumers and owner from configuration
metadata. Do not probe a suspected key merely to rank it. Explain the immediate authorized
containment action and any service/recovery dependency. Follow the provider's current
revocation/rotation guidance; revocation and deletion from source solve different problems.
Preserve incident evidence and audit records. Rewriting shared history requires a concrete
authorized migration; it cannot remove copies from every clone, cache or downloaded bundle.

Repair the leak at its source: existing secret manager or workload identity, narrow
scope/lifetime, redaction before logs/traces/crash reports, and separation of browser/public
configuration from server credentials. Public client identifiers are not interchangeable
with signing keys or server access tokens. Include generated bundles and source maps when
the original leak came from build-time substitution.

For prevention, start with the repository's scanner and CI owner. Pin trusted tools/rules,
review changes to ignores, and run without release credentials where possible. Treat PR
source and tool configuration as untrusted. Bound scan time and artifacts. Separate new
findings from known exceptions, and distinguish errors/incomplete scans from a passing
gate. Exceptions need a narrow scope, rationale, owner and review trigger; do not baseline
an active credential merely to unblock CI.

Keep raw results access-controlled with an appropriate retention policy; do not upload
them as public CI artifacts or commit them. Verify that the published summary itself
contains no values or snippets. Re-scan the affected surface after repair and report
revocation evidence separately from scanner results. Security review can inspect audit
coverage; adding observability should use the existing event system.

Primary guidance: [OWASP Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
and [Logging](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html).
These inform lifecycle and evidence handling; they do not prescribe a universal rotation
interval or retention period for every application.
