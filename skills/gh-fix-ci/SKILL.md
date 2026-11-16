---
name: "gh-fix-ci"
description: "Diagnose and fix failing GitHub Actions PR checks using gh and the existing project checks. Use for GitHub Actions failures; identify external CI providers and route them to their owning workflow."
---


# Fix GitHub Actions checks

## Overview

Use gh to locate failing PR checks, read the actionable logs, trace the cause and verify a focused repair. A diagnosis-only request stays read-only. An explicit fix request authorizes scoped implementation; ask only about a missing consequential decision or action outside that scope.

Use existing GitHub authentication. Check access to the requested repository; an authentication problem is not a reason to broaden scopes automatically.

## Inputs

- `repo`: path inside the repo (default `.`)
- `pr`: PR number or URL (optional; defaults to current branch PR)
- `gh` authentication for the repo host

## Quick start

- `python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --pr "<number-or-url>"`
- Add `--json` if you want machine-friendly output for summarization.

## Workflow

1. Verify gh authentication.
   - Run `gh auth status` in the repo.
   - If access is unavailable, explain the required repository access and authentication step. Continue useful local inspection; do not replace credentials or expand permissions incidentally.
2. Resolve the PR.
   - Prefer the current branch PR: `gh pr view --json number,url`.
   - If the user provides a PR number or URL, use that directly.
3. Inspect failing checks (GitHub Actions only).
   - Preferred: run the bundled script (handles gh field drift and job-log fallbacks):
     - `python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --pr "<number-or-url>"`
     - Add `--json` for machine-friendly output.
   - Manual fallback:
     - `gh pr checks <pr> --json name,state,bucket,link,startedAt,completedAt,workflow`
       - If a field is rejected, rerun with the available fields reported by `gh`.
     - For each failing check, extract the run id from `detailsUrl` and run:
       - `gh run view <run_id> --json name,workflowName,conclusion,status,url,event,headBranch,headSha`
       - `gh run view <run_id> --log`
     - If the run log says it is still in progress, fetch job logs directly:
       - `gh api "/repos/<owner>/<repo>/actions/jobs/<job_id>/logs" > "<path>"`
4. Scope non-GitHub Actions checks.
   - If `detailsUrl` is not a GitHub Actions run, label it as external and only report the URL.
   - Use the provider's existing workflow when available and within the user's request; this skill's helper only diagnoses GitHub Actions. In repositories with local CI, follow the owning runner and receipt rules rather than adding Actions workflows.
5. Summarize failures for the user.
   - Provide the failing check name, run URL (if any), and a concise log snippet.
   - Call out missing logs explicitly.
6. Trace and scope the repair.
   - Match the failing run's commit and job to the checked-out change. Inspect the workflow, implementation and relevant tests; separate product defects from runner, dependency or access failures. State the cause and smallest useful fix.
7. Implement within the request.
   - Preserve unrelated work and required checks. Do not weaken assertions, disable jobs or add a new CI provider merely to obtain a green result. Creating or updating a PR uses existing task authorization.
8. Verify the result.
   - Run the relevant local check and required owning gates. Recheck `gh pr checks` when useful, matching its head SHA to the repaired code. A historical green run cannot validate an unpushed repair. Report local evidence separately from CI results; trigger remote reruns or push only when authorized.

## Bundled Resources

### scripts/inspect_pr_checks.py

Fetch failing PR checks, pull GitHub Actions logs, and extract a failure snippet. Exits non-zero when failures remain so it can be used in automation.

Usage examples:
- `python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --pr "123"`
- `python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --pr "https://github.com/org/repo/pull/123" --json`
- `python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --max-lines 200 --context 40`
