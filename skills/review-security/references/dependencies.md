# Dependency findings during a security review

Establish exact resolved and shipped package identities/versions, including build tools,
images, static libraries and binary SDKs. A development-only component can compromise
release credentials or outputs. Match advisories to the actual feature/platform and
distribution; deduplicate aliases and check vendor fixes/backports.

Use the installed `audit-dependencies` skill for a complete inventory, scanner execution,
current advisory research and remediation workflow. This review remains usable without
it: consult [OSV](https://osv.dev/), [GitHub advisories](https://github.com/advisories),
the upstream/vendor notice and the relevant ecosystem database. Record exact versions,
source URLs, affected/fixed ranges, exposure, dates and unresolved coverage.

Do not call an unsupported ecosystem, stale database or zero-package scan clean. A
missing call path is not proof that a package is safe. Distinguish vulnerabilities from
license/maintenance policy. Classify applicability with evidence; no automatic package
repair, mass upgrade or new hosted workflow as a side effect of review.
