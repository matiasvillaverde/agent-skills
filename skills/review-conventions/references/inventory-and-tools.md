# Inventory, search and safe semantic changes

Start at the requested subtree, not the whole disk. These commands are examples for an existing
trusted checkout; substitute its real scope and inspect local help before using optional flags.

```sh
rg --files path/to/scope
git status --short -- path/to/scope
git ls-files -- path/to/scope
tree -a -L 3 --gitignore --dirsfirst -I .git path/to/scope
rg -n -F -- 'DomainTerm' path/to/scope
```

`tree` is a readable navigation view. `rg --files` normally honors ignore rules and omits hidden
files; Git's tracked list answers a different question. Reconcile them when coverage matters,
inspect selected hidden config explicitly and account for relevant untracked source. For
programmatic inventories use NUL-delimited `rg --files -0` or `git ls-files -z`; don't split
filenames on whitespace. Avoid following symlinks or scanning dependencies/caches by default.
No tree installation is required: the file list plus manifests is an adequate fallback.

Use filenames and text to locate candidate families; inspect complete relevant declarations and
calls before classifying them. For repeated patterns, choose the cheapest sufficient tool:

| Evidence needed | Appropriate tool class | Limitation to record |
| --- | --- | --- |
| Paths, literal keys, spelling variants | `tree`, `rg`, Git's file inventory | Text hits do not distinguish comments, strings, bindings or symbol identity |
| Declaration/call shapes within parsed source | Existing AST query tool, e.g. ast-grep/Tree-sitter | Grammar/language/version and parse errors matter; structural matching is not type or scope resolution |
| Actual symbol identities, references, export visibility | Project-aware compiler/index or language server | Build configuration, selected targets, indexing and generated code affect coverage |
| Rename one symbol and its references | Existing IDE/LSP rename with preview/prepare support where available | Review the returned edit set; dynamic lookup, wire strings and external clients need separate checks |
| Repeatable local rule | Existing compiler, formatter or narrowly configured linter | A rule being enabled does not establish nonzero coverage or semantic naming quality |

[ast-grep's concepts](https://ast-grep.github.io/advanced/core-concepts.html) explain structural
matching; its [FAQ](https://ast-grep.github.io/advanced/faq.html#does-ast-grep-support-some-advanced-static-analysis)
explicitly excludes scope/type/control-flow analysis. Do not treat an AST match as a resolved
call graph. [LSP rename](https://github.com/microsoft/language-server-protocol/blob/gh-pages/_specifications/lsp/3.17/language/rename.md)
returns workspace edits and can reject unsupported renames; protocol support does not prove a
particular server has indexed every consumer.

Before adding a rule, check the effective configuration and existing diagnostics. Prefer one
small proven invariant over a custom convention engine or a blanket all-rules preset. Distinguish
actual findings from parser failures, excluded files and empty selections. Test the proposed rule
against an intentional violation and a legitimate boundary/override case; inspect autofixes and
their second-run stability. Use existing checks for the rest rather than duplicating their output.

For renames, include case-only path collisions, language-reserved identifiers, imports/exports,
serialization mappings, selectors/reflection, public headers, generator inputs and test/resource
discovery as relevant. Search old spellings afterward, but preserve intentional compatibility
keys and dated evidence. A compile alone can miss an unchanged string-based consumer.
