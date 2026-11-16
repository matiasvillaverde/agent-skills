# Small, scoped agent instructions

Use the portable spelling `AGENTS.md`. Start by reading the applicable root/ancestor and nested
instruction chain, including selected files outside Git. Keep one owner for each rule and link
required guides with a clear reading trigger. The file should change what an agent does here,
not summarize everything that searches, manifests and formatters already reveal.

Useful content includes a nonstandard command with its working directory, an ownership boundary,
a required guide, a compatibility constraint or a recurring failure with a verified remedy.
Omit generic “write clean code” advice, copied source trees, task logs, speculative rules and
duplicated formatter settings. Respect an existing repository length budget; do not invent a
universal line cap or delete important constraints simply to fit one.

Add a nested file only when a durable subtree has materially different commands or constraints.
State its differences and point to the owned guide. A `src/` or `tests/` directory alone does not
justify another instruction file. Moving or deleting guidance must preserve its applicability;
a child does not grant permissions or override higher-priority user/system instructions.

Verify the actual clients rather than assuming identical discovery:

- A Markdown link is a navigational pointer, not necessarily an automatic import.
- Working directory, ancestor overrides, adapters, ignored files and context limits can affect
  what loads. Check the supported client/version from root and the affected subtree.
- [Claude Code](https://code.claude.com/docs/en/memory#agentsmd) documents version-dependent native
  AGENTS support and interaction with CLAUDE files. Its supported `@path` import differs from a
  prose redirect; preserve compatibility adapters until all supported clients are checked.
- [Grok project rules](https://docs.x.ai/build/features/project-rules) document root-to-working-
  directory discovery and `grok inspect`. Inspect only relevant paths, avoiding credential dumps.
- For Codex, use installed discovery evidence and the current
  [official guide](https://developers.openai.com/codex/guides/agents-md) when needed. Do not infer
  that a root-started session has preloaded all descendant files.

For a Codex discovery discrepancy, inspect the root-to-working-directory chain, per-directory
`AGENTS.override.md` precedence, configured fallback filenames and the effective project context
budget. For Claude, inspect ancestor/working-directory CLAUDE-family selection and conditional
descendant loading. For Grok, `grok --cwd <scope> inspect --json` can inspect selected instructions;
filter the result to paths and trust state. Match these checks to the installed version instead
of assuming every client or old release follows the same rules.

The [format site](https://agents.md/) establishes the intended role and nesting convention;
client documentation and observed discovery establish what a specific installation loads.
File existence, loaded instructions and successful behavior are separate checks. Do not change
trust, hooks, permissions or global configuration just to make an instruction audit pass.

For a consequential change, use a fresh bounded task to see whether the agent finds the owner,
selects the correct command and preserves the boundary without extra hints. The
[CTXbench study, v3](https://arxiv.org/html/2602.11988v3) found no general task-success gain from
context files in its Python task evaluation, despite higher costs. It did not establish an
optimal file length or evaluate every language, security property or current agent. This supports
testing useful guidance, not a blanket claim that instructions are harmful or shorter is always better.
