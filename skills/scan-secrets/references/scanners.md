# Scanner execution and coverage

Reviewed 2026-11-14 against Gitleaks 8.30.1 and TruffleHog 3.99.9. Check the installed
version's help; do not translate old `detect`/`protect` examples blindly. Treat downloaded
rules, repository configuration and custom verifier endpoints as untrusted inputs.

## Gitleaks

Use reviewed configuration and a pre-created private output directory. The variables
below represent absolute paths established for this task. `secret_report_dir` must be
outside `secret_scan_root`. Validate that the root and rules exist before execution.
Select only the relevant modes; these are separate scans, not a required bundle.

```sh
gitleaks dir "$secret_scan_root" --config "$secret_rules" --redact=100 \
  --exit-code=10 --report-format=json --report-path="$secret_report_dir/files.json" \
  >"$secret_report_dir/files.log" 2>&1

gitleaks git "$secret_scan_root" --staged --config "$secret_rules" --redact=100 \
  --exit-code=10 --report-format=json --report-path="$secret_report_dir/staged.json" \
  >"$secret_report_dir/staged.log" 2>&1

gitleaks git "$secret_scan_root" --log-opts=--all --config "$secret_rules" --redact=100 \
  --exit-code=10 --report-format=json --report-path="$secret_report_dir/history.json" \
  >"$secret_report_dir/history.log" 2>&1
```

Capture each exit status immediately using the owning runner; do not pipe through a
command that masks failure, or use `|| true` as a success verdict. Here 10 means findings;
other nonzero statuses need diagnosis. Zero still requires valid coverage evidence.
The local qualification found that a nonexistent directory could return zero.

The staged mode reads the index; a clean working copy can differ. `--all` concerns
locally available refs: it does not obtain remote refs or scan unreachable Git objects,
external forks, LFS contents or separate repositories. Establish whether those matter.
Inspect path/config allowlists, inline ignores, `.gitleaksignore`, baselines, archive,
decoding and size limits. Do not silently trust target-supplied rules that suppress the
entire scope. Retain a reviewed default rule set when adding organization-specific rules.

The redaction check passed for a synthetic rule in this version, including JSON output.
This does not establish that every output field or future version is safe. Keep raw
reports private and construct summaries from an allowlist of safe metadata.

## TruffleHog

It can verify candidates through provider APIs. For passive filesystem scanning, current
help supports this shape; confirm the flags and result classes on the installed version:

```sh
trufflehog filesystem "$secret_scan_root" --no-update --no-verification \
  --results=verified,unknown,unverified --fail --fail-on-scan-errors --json \
  >"$secret_report_dir/trufflehog.jsonl" 2>"$secret_report_dir/trufflehog.log"
```

Do not combine disabled verification with a verified-only result filter. No verification
does not itself prove zero network activity from every optional feature/configuration;
inspect them and use enforced network isolation when that guarantee is required.
`Raw` and other result fields can contain credentials. Never assume that a field named
`Redacted` is safe to publish. Findings and scan errors require distinct handling.

Hosted GitHub scanning is another option when already authorized and available. Establish
whether private content is transmitted, supported token classes, repository/plan coverage
and result access. Existing GitHub push protection complements local scans; it does not
establish that ignored files, release bundles or all historical refs were checked.

## Sources

- [Gitleaks commands and configuration](https://github.com/gitleaks/gitleaks#usage)
- [TruffleHog verification and output](https://github.com/trufflesecurity/trufflehog#usage)
- [GitHub's secret-scanning skill](https://github.com/github/copilot-advanced-security-plugin/blob/9c8cd1a00c1290bf89db8f068aded1fb5dace200/skills/secret-scanning/SKILL.md): useful detection/context workflow; hosted content transfer is a real boundary.
- [Community secret-scan](https://github.com/jpoindexter/security-skills/blob/012784a4ca5ab8b6737a6fc1e73771e0d0addbf6/secret-scan/SKILL.md): useful separate history/staged coverage; deprecated commands and blanket fixture exclusions were not adopted.
