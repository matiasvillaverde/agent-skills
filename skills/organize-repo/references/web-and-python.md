# Web, TypeScript, Node and Python placement

Read the applicable section. Preserve the repository's chosen package manager, lockfile,
framework version and deployment shape; organizing files is not an upgrade or framework migration.

## TypeScript and Node

Start with package/workspace manifests, tsconfig inheritance/references, bundler configuration
and runtime entrypoints. One folder is not automatically one package. Keep public import
subpaths and names stable when changing internal placement. Inspect `exports`, `main`, `types`,
`bin`, package contents and conditional ESM/CJS entrypoints before and after a move. Adding
an `exports` field can remove previously reachable imports; it is not a cosmetic cleanup.
[Node package contracts](https://nodejs.org/api/packages.html#package-entry-points).

TypeScript `paths` does **not** rewrite emitted imports. Align runtime, bundler and test
resolution instead of adding an alias that only satisfies the type checker.
[TypeScript paths](https://www.typescriptlang.org/tsconfig/paths.html).
`rootDir`/`outDir`, include/exclude and project references can change emitted paths; defaults
are compiler-version-sensitive (including the TypeScript 6 rootDir change). Verify emitted
artifacts and the advertised entrypoint, not only `tsc --noEmit`.
[TypeScript 6 changes](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-6-0.html).

## Framework routes and browser assets

Identify the actual router/framework before moving web files. Next.js `app/` and `pages/`
have different discovery rules; `src/` is optional. In the App Router, segment folders and
special files determine routes and layouts. Route groups can omit a URL segment while still
changing layout behavior; private folders opt out of routing. Ordinary colocated components
do not need to become routes. `components/` and `lib/` are conventions, not required framework
directories. [Next.js structure](https://nextjs.org/docs/app/getting-started/project-structure).

Preserve published paths, dynamic parameters, nested layouts, error/loading behavior and
server/client boundaries. Check framework-reserved files for the installed version, public
asset URLs, CSS/font imports, worker entrypoints and generated-route configuration. Review
other frameworks' own docs rather than transplanting Next.js conventions. Exercise affected
URLs and their states with the repository's existing runtime/checks; compile success alone
does not establish route or visual parity.

## Python

Both flat and `src/` layouts are legitimate. A packaged library often benefits from `src/`
isolation because imports from the working directory can mask installation mistakes. A small
script does not need a new package hierarchy. A move to `src/` requires real package discovery
and an appropriate install/run workflow. Preserve public imports and console entrypoints.
[PyPA comparison](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/).

Read the selected build backend's configuration and inspect wheel/sdist contents when packaging
changes. Do not assume setuptools rules apply to every backend. Explicit discovery, implicit
namespaces, data-file inclusion and auto-excluded names can change what ships; adding an
`__init__.py` mechanically can break intended namespace semantics.
[Setuptools discovery](https://setuptools.pypa.io/en/stable/userguide/package_discovery.html).

Keep fixtures and test configuration in the runner's actual discovery scope. Moving tests or
`conftest.py` can change imports and fixture availability. Compare collection/meaningful cases
and run against the installed artifact when relevant, not just a source checkout whose path
happens to make imports succeed. Both in-package and external tests are valid.
[pytest integration](https://docs.pytest.org/en/stable/explanation/goodpractices.html).

Treat bundled resources as part of the package contract. Preserve `importlib.resources` lookup
and data inclusion; resources may live in a zip rather than a normal filesystem directory.
Test resource use from outside the source root if that is a supported usage.
[Python resource API](https://docs.python.org/3/library/importlib.resources.html).
