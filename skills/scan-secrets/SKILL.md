---
name: scan-secrets
description: Find exposed credentials in working files, staged changes, Git history and release artifacts using scoped, redacted secret scans. Use before sharing or releasing code, after suspected leaks, or when adding secret-scanning gates.
---

# Scan secrets

Find credential exposure without spreading the credential. Use deterministic scanners
and contextual triage; report the exact surfaces covered and what remains unknown.

## Establish scope and safe output

Read repository instructions and the existing scanner configuration or wrapper. Identify
the repository/revision, intended sharing or deployment, relevant artifacts and credential
types. Inspect installed tool versions and help before choosing commands. A wrapper can
contact credential providers even when its input is a local folder; inspect verification,
result filters, uploads, ignore rules and error handling.

Select the necessary surfaces explicitly: working files (including relevant ignored and
untracked files), staged index, history/refs, submodules, generated bundles, source maps,
images or authorized logs. A scan of one does not cover the others. Do not traverse the
whole home directory, secret stores or symlinks outside the requested scope by default.

Use a private report directory outside Git with restricted permissions. Redirect both
scanner reports and stdout/stderr there before inspection. Do not print environment
values, diffs containing candidates, full JSON findings, token fragments or private keys.
Summarize only reviewed metadata: detector, safe location, commit, category and status.
Even paths, commit messages and error strings can contain sensitive material.

Use [scanner recipes and coverage checks](references/scanners.md) for Gitleaks or
TruffleHog. Prefer existing tooling; do not silently install a pack or send private
files to hosted scanning. Passive pattern scanning is the default. Provider verification
uses the candidate credential and needs scope that authorizes that contact. Respect
existing authorization; do not ask again when it already covers the operation.

## Run, verify coverage, then triage

Check target existence, inventory, scanner configuration and expected file/ref counts
before running. Record omissions, shallow history, absent refs, LFS pointers, unexpanded
archives, size/decode limits, suppressed findings and timeouts. Do not fetch extra private
repositories or large artifacts implicitly. Check actual scan counts and diagnostics;
success with zero useful coverage is incomplete, not clean.

Distinguish scanner candidates from confirmed exposure. Inspect the smallest necessary
context locally without reproducing the value. Determine whether it is a credential,
public identifier, synthetic fixture or unresolved candidate; record owner/environment
and likely privileges without reading unrelated secrets. An unverified result can still
be a real credential. A verification error says nothing about validity. Deduplicate
occurrences using the scanner's private identifiers; do not publish hashes of low-entropy
secrets as a substitute for redaction.

For false positives, use a narrow, explained suppression only when authorized. Fixture
directories and example files can contain real keys; never exempt them wholesale. A
baseline records accepted findings, not remediation. Preserve existing mandatory gates.

## Contain and prevent recurrence

For a credible exposure, describe the provider/owner, affected consumers and next
containment steps. Do not postpone urgent containment merely to finish the scan. Deleting
a string or rewriting history does not revoke it. Follow the incident owner's authorized
revocation/rotation and recovery plan; account for dependent services. History rewriting,
force-pushing, deleting evidence and contacting other people are separate actions, not
automatic scan cleanup. Use [response and prevention](references/response.md).

When adding a gate, verify a synthetic positive, a clean input, an execution failure and
nonempty intended coverage. Test redaction with a made-up marker rather than a real key.
Keep fast changed-surface checks plus a suitably scoped historical/artifact check; report
their different coverage. Reuse the owning CI/pre-commit mechanism.

Return findings, coverage, scanner/rules versions, sanitized evidence locations and the
specific next action. Never conclude that the repository is secret-free. Remove only
task-created disposable fixtures/caches after retaining useful redacted evidence; preserve
incident records and existing logs. Use `review-security` for credential architecture
or missing audit controls; this skill owns exposure scanning.
