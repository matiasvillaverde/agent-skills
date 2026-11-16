---
name: organize-repo
description: Organize repository files, documentation and scoped AGENTS.md instructions using actual platform conventions. Use for tree/layout cleanup, misplaced files, unclear document ownership or instruction hierarchy; preserve build, import and runtime contracts.
---

# Organize a repository

Make the next relevant file or instruction easy to find. Preserve behavior, public interfaces
and the existing toolchain. A useful small move, a clearer pointer or no change can be the
right result; fewer directories and a symmetrical tree are not goals.

## Understand the tree

Establish the requested repository/subtree and whether the user wants an audit or changes.
Read its instruction chain and owner map before edits. Check dirty files, worktrees,
submodules and symlinks; preserve unrelated work and independent repository boundaries.

Start with `rg --files` in scope, manifests, entrypoints and a shallow tree. With an available
compatible `tree`, a useful view is `tree -a -L 3 --gitignore --dirsfirst -I .git <scope>`.
Check local help before adding flags; deepen only relevant branches. An ignored/pruned tree
is a navigation view, not a complete inventory. Inspect selected hidden configuration,
tracked files and ignored outputs separately. Do not follow links or walk dependency/cache
trees by default, or install a tree utility just for this task.

Identify the owners of source, tests/fixtures, assets, generated/vendor files, tool settings,
documentation and private runtime data. Read the actual build/package configuration and
existing checks. Trace a representative build, test or reader journey through the confusing
area before deciding it is misplaced. Filenames, age and identical bytes do not prove that
files are redundant or safe to delete.

## Choose the smallest coherent arrangement

Prefer existing ownership and platform conventions over a new generic hierarchy. Read only
the relevant sections of [compiled platforms](references/compiled-platforms.md) for Swift,
Rust, Go, Zig and C/C++/CUDA, or [web and Python](references/web-and-python.md). Verify
version-sensitive rules against the repository's actual toolchain and primary documentation.
Separate required discovery paths from optional style. Keep related code together without
inventing packages, services, `shared/` layers or a universal `src/` layout.

Use [docs and instructions](references/docs-and-instructions.md) when placing guides or
editing AGENTS.md. Keep one authority for each rule and link to it with a reading trigger.
Add nested instructions only where a durable subtree has materially different commands or
constraints. Do not generate instructions or README files for every ordinary folder.

Before consequential moves, give a compact old → new mapping, the concrete benefit and the
path-dependent contracts/checks. This can stay in the working response; routine authorized
moves do not need a new plan document or approval round. Architecture/API changes deserve
their own explicit scope; `design-codebase` covers those when available. `maintain-docs`
covers substantive documentation reconciliation beyond placement and navigation.
For inconsistent filenames, symbols, domain vocabulary or cross-layer naming, use
`review-conventions` when available. It distinguishes actual requirements from inferred patterns
and compatibility exceptions; a layout cleanup does not require repository-wide renaming.

## Move and verify

Move focused groups and update their consumers together: imports, target membership,
package exports, resources, build scripts, test discovery, command working directories,
CI/cache/path filters, containers, ownership rules and documentation links. Inspect both
paths' instruction scopes; moving a file must not silently drop a required rule. Preserve
public URLs, installed artifact paths, localization/resource identifiers and license notices.
Check case-only renames, destination collisions and executable modes. Do not rewrite Git
history, relocate private data into Git or edit generated output instead of its source.

Run the owning checks affected by the moves. Verify expected tests are still discovered;
a successful run with fewer cases or missing targets needs explanation. When packaging or
resources changed, inspect the produced artifact and exercise its public entrypoint from
an appropriate working directory. Search surviving old-path references and resolve each
as live, historical or intentionally compatible. Check local links/anchors and actual
instruction discovery for the clients in use; a file existing does not prove it was loaded.

Report the affected final tree, why it is easier to navigate, checks actually run and gaps.
Avoid a full repository dump or a second wiki. Keep compact useful evidence, remove only
task-created disposable fixtures/build output, and leave existing caches and source intact.
The [research basis](references/sources.md) explains the community choices and limitations.
