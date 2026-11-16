---
name: skill-audit
description: "Codex/OpenClaw skill audit: live budget, usage, duplicates, compact descriptions."
---

# Skill Audit

Use this when trimming skill prompt budget, finding duplicate skills, auditing enabled/disabled skill roots, or deciding which skills/plugins to remove.

## Workflow

1. Resolve this skill's actual directory from the available-skills catalog. Run the
analyzer by that absolute path, or change into this skill directory first. Start
without session-log access unless usage history is relevant to the requested audit:

```bash
node --experimental-strip-types scripts/skill-audit.ts --no-logs
```

Useful variants:

```bash
node --experimental-strip-types scripts/skill-audit.ts --no-live --no-logs
node --experimental-strip-types scripts/skill-audit.ts --root ~/.agents/skills --root-only --no-logs
node --experimental-strip-types scripts/skill-audit.ts --months 3 --max-log-mb 100
```

2. Read the report in this order:
- `Skill Budget`: inventory source, context source, assumed budget and description pressure.
- `Description candidates`: long descriptions where relaxed grammar saves prompt budget.
- `Duplicates`: same skill name or near-identical description/body across Codex, plugin cache, repo siblings, and personal skill roots.
- `Unused candidates`: no recent user mention or actual `SKILL.md` read in recent Codex/OpenClaw logs.
- `Root summary`: where skills came from and whether config marks them disabled.

3. Before deleting or editing:
- Verify the kept copy exists and is loaded.
- Prefer deleting repo-local or `agent-scripts` duplicates when Codex built-ins cover them.
- Keep repo-local OpenClaw maintainer skills when they encode repo policy or live operations.
- Preserve trigger nouns in descriptions: product, tool, action, object.
- Check purpose and behavior before merging similar names or deleting copies; similarity
  and missing log mentions are candidates for inspection, not proof of redundancy.

## Analyzer Notes

- When supported, `codex debug prompt-input` supplies the CLI's rendered skill list,
  order, names and aliased paths for this cwd/configuration. It does not prove another
  client's or an already-running conversation's inventory. `--no-live` uses filesystem discovery.
- The broad filesystem scan remains for duplicate, disabled, and archived-cache diagnostics; it is not treated as the loaded inventory.
- The script mirrors Codex's model-visible line shape: `- name: description (file: path)`.
- It applies Codex-like frontmatter rules: YAML frontmatter only, default name from parent dir, single-line sanitized `name` and `description`.
- The budget model estimates 2% of raw `context_window` and `ceil(utf8_bytes / 4)`,
  including alias-table cost. Verify the installed client's rendering policy before
  treating simulated truncation or omission as actual behavior.
- Pass `--model` with the observed model identifier to consult `~/.codex/models_cache.json`,
  or `--context-tokens` with a verified limit. Otherwise the 272,000-token fallback
  is explicitly hypothetical. Do not infer the current session's model or budget from it.
- It scans only normal Codex/plugin/repo skill roots by default. Extra folders such as Dropbox archives are included only with `--root <path>`.
- `--root-only` requires at least one `--root <path>`, skips the live Codex inventory, and scans only those supplied roots.
- It realpath-dedupes roots, so symlinked roots such as `~/.codex/skills/agent-scripts -> ~/Projects/agent-scripts/skills` do not create false duplicates.
- For duplicate names, it reports description/body similarity and suggests deletion candidates only when bodies are near copies. Keep priority defaults to direct Codex system skills, then direct Codex skills, then plugin skills, then personal/repo copies.
- It scans `~/.codex/history.jsonl` and recent `~/.codex/sessions/**/*.jsonl` by default. Add `--deep-logs` for archived sessions and common OpenClaw/Clawd log folders.
- Usage evidence is heuristic: user `$skill`/`use skill` mentions and paths observed in tool-call arguments.

## Output Policy

- Suggest first; edit only when the user asks.
- If asked to apply cleanup, make small reviewable changes. Commit or publish only
  within the user's requested scope; preserve unrelated work.
- Do not delete ignored/untracked skill dirs without naming the destination or confirming they are disposable.
