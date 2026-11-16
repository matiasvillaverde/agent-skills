# Documentation ownership and instruction scope

## Put information where its reader and owner meet

Keep the repository README as orientation and a reliable route to development instructions.
Use the existing repository map in a monorepo; do not duplicate a full source tree in several
files. Product-specific guides belong with that product unless the established owner says
otherwise. Shared operational policy belongs in its shared owner, with local links. Use an
existing `docs/`, `Docs/` or equivalent; casing and discoverability matter more than a new name.

Choose a document by a real reader task: setup, a procedure, a contract, or rationale. API
comments belong beside the API; generated reference belongs with its generator/input; tool
configuration owns executable settings. Preserve established ADR numbering, supersession
links and dated research evidence. Keep private logs, credentials and receipts out of tracked
documentation. Do not create empty tutorials/how-to/reference/explanation folders merely to
apply [Diátaxis](https://diataxis.fr/how-to-use-diataxis/).

Move a guide with its inbound links, relative outbound links, site navigation and relevant
anchors. Inspect repository-relative versus file-relative link conventions. Published URLs
may need an established redirect rather than a silent break. Keep historical paths in dated
evidence when they describe what was true then. Do not replace useful history with the current
tree or claim that a newer timestamp proves accuracy.

## Instruction placement and discovery

Use exact `AGENTS.md` casing. Add a nested file only where a durable subtree has materially
different commands or constraints; ordinary source/test folders do not each need one. State
local differences and link the owning guide instead of copying ancestor rules. Respect existing
length budgets and preserve required instructions at both ends of a file move.

The shared library's [agent-instruction guidance](../../maintain-docs/references/agent-instructions.md)
owns instruction content and client discovery. Read it when editing the hierarchy. If that
companion is unavailable, inspect installed-client discovery and current vendor documentation;
keep one canonical body and only compatibility adapters the supported clients need.

A Markdown link is not necessarily an import, a root-started session may not preload children,
and file existence does not prove loading. Verify root and affected-subtree behavior without
changing trust, permissions, hooks or global context limits. Preserve existing adapters until
all supported clients are checked. `maintain-docs` covers substantive reconciliation of the
instruction body; this skill owns placement and preservation across moves.
