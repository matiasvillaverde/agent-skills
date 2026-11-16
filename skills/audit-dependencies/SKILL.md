---
name: audit-dependencies
description: Audit, upgrade or simplify resolved and shipped dependencies, toolchains and images. Use for advisories, supply-chain risks, unused packages, small owned replacements and compatible dependency changes across ecosystems.
---

# Audit dependencies

Determine which published issues and supply-chain weaknesses apply to this build or
deployment. Exact inventory, current evidence and exposure matter more than scanner counts.

## Establish what is actually used

Read repository instructions and existing dependency/CI policy. Record source revision,
target environment, resolved lockfiles, package identities/registries, overrides, enabled
features, platform and architecture. Compare source inventory with the shipped artifact:
vendored code, static libraries, binary frameworks, plugins, image digests, OS packages,
toolchains and drivers can escape a package-manager scan. Do not regenerate lockfiles
or install dependencies merely to inventory them when resolved metadata is available.

Separate runtime, build/install, test and developer exposure. Build tools can execute
with release credentials or alter shipped code. A dependency labeled dev is not
automatically low priority or absent from an output bundle. Mark missing inventory as
unknown and follow references that could materially change the conclusion.

## Scan and research

Discover existing tools and inspect their configuration, ignore lists, database freshness
and supported inputs. Use [ecosystem checks](references/checks.md) to select the smallest
useful set. Capture actual extracted packages and errors, not just the vulnerability count.
A successful scan of zero packages or an unsupported lockfile is incomplete. Existing
SBOMs help only when their identity and completeness match the target artifact.

Read the current upstream/vendor advisory and its references. Use
[advisory research](references/advisories.md) for OSV, GHSA, RustSec, Go, CISA, Apple,
NVIDIA and distributor sources. Search all applicable dates. Record package/version,
dependency path, advisory aliases, affected/fixed ranges, required feature/platform,
publication/update/retrieval dates and source URL. Confirm a fix is released and applicable
to the actual distribution; a patch commit or upstream version comparison alone may mislead.

Treat resolution, builds, package plugins and downloaded scanning rules as executable
trust decisions. Inspect hooks; isolate untrusted work without ambient credentials and
with bounded resources. A temporary folder is not isolation. Do not silently install
tools, upload private inventories/source or run package-manager repair commands.
Use existing authorization for approved registries and advisory services.

## Triage the exposure

Deduplicate CVE/GHSA/OSV/RUSTSEC aliases. Classify each issue as applicable, conditional,
excluded with evidence or unresolved. Explain attack preconditions and consequence;
check configuration, code paths, distribution backports and actual exploitation evidence.
Absence from a known-exploitation catalog or failure to prove reachability is not proof
of safety. Distinguish vulnerabilities, maintenance notices and license policy findings.

Inspect supply-chain entry points too: wrong package/registry identity, unpinned downloads,
mutable Git references, install scripts, build plugins/macros, binary provenance and
excessive CI authority. Compare a changed dependency's scripts, permissions and delivery
path. Popularity and age alone neither prove trust nor establish maliciousness. A clean
advisory scan does not detect every backdoor or undisclosed flaw.

## Repair and prevent recurrence

For maintenance or simplification, read [upgrades and removal](references/maintenance.md).
Prefer fewer necessary dependencies, the supported standard library and small clear owned
implementations when they reduce total cost. Copied/vendored code still needs provenance,
license obligations, tests and a maintenance owner; it does not become vulnerability-free.
Do not trade a mature security-sensitive implementation for an unreviewed rewrite merely
to lower the manifest count.

When authorized to fix, choose a supported, compatible update/removal/configuration
change that addresses the cause. Review the resolved diff and release notes; even patch
upgrades can break behavior. Re-run the relevant scanner and owning compatibility tests.
No blanket latest-version upgrades, automatic `audit fix --force`, unexplained overrides
or silent acceptance. Deferred issues need evidence, owner and review trigger/expiry.

For requested CI integration, reuse the existing runner: changed-dependency checks plus
a suitable full inventory and refreshed-advisory cadence. Preserve required gates; make
missing tools, stale data, parse errors and skipped ecosystems visible. Keep policy
ownership and exceptions in one place, without adding a second vulnerability database.

Return prioritized issues, proposed fixes, exact coverage and unresolved gaps, with
sanitized evidence. Preserve legitimate product behavior. Clean only task-created
disposable outputs after retaining necessary evidence. Use `scan-secrets` for exposed
credentials and `review-security` for source/deployment flaws; do not repeat those audits.
