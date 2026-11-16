# Source basis

Original instructions, reviewed 2026-11-15. No community runtime or templates bundled.

- [Autocraft inspector](https://github.com/sunfmin/autocraft/blob/a6ad0f68518db40b1ebd4cbb31b80fa51f204ea7/skills/autocraft/inspector.md): inspect whether artifacts support the verdict and catch vacuous assertions. Omit automatic permission bypass, compulsory role count and universal test-removal rules.
- [Darwin](https://github.com/Akanoa/skill-darwin/blob/7b5de355e215be63709b1dcaaae50e175108ce3e/SKILL.md): replay defect-shaped mutations independently. Classify build/setup/timeout separately from behavioral detection; worktrees are not execution sandboxes.
- [TestPrism / TestHelix v2](https://arxiv.org/html/2610.12289v2): cross-validation and requirements-only assertion review.
- [SWEPatchTest v1](https://arxiv.org/html/2610.18004v1): reproducing one bug and passing one fix can still accept wrong alternatives or reject correct ones.
- [Test-suite auditors v1](https://arxiv.org/html/2608.01715v1): validate inputs and expected-output oracles; reproducible false positives and correlated model mistakes remain possible.
- [Anthropic evaluation guidance](https://www.anthropic.com/research/demystifying-evals-for-ai-agents): actual environment outcome, stable trials and clear criteria.
- [MCP specification](https://modelcontextprotocol.io/specification/latest): inspect the actual revision's result and capability semantics before judging interoperability.

The papers are benchmark research, not demonstrated production efficacy for these skills.
Qualification needs realistic broken and correct controls, actual evidence and explicit gaps.
