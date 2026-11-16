# Dependencies and vulnerability research

Establish exact resolved and shipped versions before querying advisories. Inspect
lockfiles, workspace overrides, vendored code, binary frameworks, images/digests,
toolchains and deployment artifacts. Separate runtime, build/install, developer and
test exposure. A build-only dependency can still compromise release credentials.

For each relevant match, retain package/ecosystem, installed version or commit,
dependency path, advisory ID/aliases, publication/update/retrieval dates, affected
range, fixed release, required features/platforms and source URL. Check whether the
fix is released; a merged patch alone is insufficient. Account for withdrawn reports,
distro backports and differences between source locks and the running artifact.

Read the upstream/vendor advisory first when available, and follow its references.
Use these sources for complementary evidence, not as independent votes:

| Source | Use |
| --- | --- |
| [OSV](https://osv.dev/) and [GitHub Advisory Database](https://github.com/advisories) | Exact ecosystem/version or commit matches and advisory aliases. Coverage differs across ecosystems; duplicated CVE/GHSA/RUSTSEC records describe one issue. |
| [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog), with [CISA's official data mirror](https://github.com/cisagov/kev-data) | Evidence of known exploitation to prioritize applicable issues. Absence is not evidence of safety. |
| [NIST NVD](https://nvd.nist.gov/) | CVE enrichment and references. Confirm product identity and affected ranges with the owning vendor; broad CPE matches can mislead. |
| [RustSec](https://rustsec.org/) | Rust crate advisories and ecosystem tooling. Distinguish vulnerabilities from maintenance notices. |
| [Go vulnerability database](https://go.dev/doc/security/vuln/) | Curated package/symbol/version data; govulncheck adds call-path evidence for supported builds. |
| [PyPA pip-audit](https://github.com/pypa/pip-audit) | Python dependency checks; read its input/resolution limitations. |
| [Apple releases](https://support.apple.com/en-us/100100), [NVIDIA PSIRT](https://www.nvidia.com/en-us/security/), OS distributor and library advisories | Match platform, driver, toolkit, architecture and support branch. Check running versions separately from installed packages. |

Search older applicable issues too. A “last seven days” search is not an audit of an
old dependency tree. If the database is stale or a source is blocked, record the gap
and use an official alternative; do not manufacture a clean result.

## Research inputs

The [community dependency-audit skill](https://github.com/jpoindexter/security-skills/blob/012784a4ca5ab8b6737a6fc1e73771e0d0addbf6/dependency-audit/SKILL.md)
provides a focused scan/triage workflow. Its automatic patch fixes and blanket low urgency
for dev dependencies were not adopted. The [Snyk dependency workflow](https://github.com/snyk/studio-recipes/blob/3752dd05a462184dcce44af3c247f287b41e35de/plugins/codex/skills/secure-dependency-health-check/SKILL.md)
supplied selection questions; no hosted-service requirement, age score or popularity-based
security verdict was adopted. This skill is original synthesis.
