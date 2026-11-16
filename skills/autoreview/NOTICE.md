# Source and local adaptations

Adapted from [OpenClaw agent-skills](https://github.com/openclaw/agent-skills),
distributed under the included [MIT license](LICENSE). Original authors retain
their copyright; no upstream endorsement is implied.

This is a locally maintained compatibility snapshot, not an unmodified upstream
release. Adaptations include passive secret scanning, bounded review bundles,
credential-safe reporting and scoped behavior checks. The upstream license was
verified at revision `91bf14bc19e8e4c1d5ba9a11c3cfb753dc759711`; that revision is
license evidence, not a claim that every helper file matches that upstream revision.

The helper supports explicit model selection. Its inherited defaults may not be
available to every account; select a model supported by your configured engine.
Included regression fixtures contain intentionally synthetic credential-like strings.
They do not authorize ignoring real credentials in test files.
