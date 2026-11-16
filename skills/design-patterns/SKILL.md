---
name: design-patterns
description: Select or review a design pattern against a concrete change problem, including when a plain function, enum or conditional is sufficient.
license: MIT
---

# Design patterns

Start with the current problem, not the name of a pattern. Identify what variation,
ownership conflict or repeated coordination is actually making changes difficult.
If no such pressure exists, keep the straightforward implementation.

Before adding indirection, check whether the language already provides the needed
mechanism: a function argument, closure, enum with exhaustive matching, struct,
iterator, protocol or existing framework facility. GoF patterns describe reusable
design ideas; they do not require reproducing class hierarchies in every language.

| Actual pressure | Candidate | Simpler alternative to consider |
| --- | --- | --- |
| Interchangeable behavior used by current callers | Strategy | Pass a function; keep a clear conditional |
| Meaningful state transitions and state-dependent operations | State | Enum and explicit transition function |
| External interface cannot be changed to match the caller | Adapter | Translate directly at the existing integration boundary |
| Callers repeatedly coordinate a complicated subsystem | Facade | A small function exposing the common operation |
| Construction has ordering or validation requirements | Builder | Constructor or options struct |
| Independent consumers react to an event | Observer | Direct calls or the existing event facility |
| Optional behaviors combine dynamically | Decorator | Put fixed behavior in its existing owner |
| An action needs queuing, replay or undo semantics | Command | Function plus explicit data |
| Creation really selects among implementations | Factory | Direct construction or a function |

For the selected pattern, explain the benefit and cost: additional types, interfaces,
lifetime management, ordering, debugging or compatibility obligations. Keep the
smallest form that solves the actual problem. Prefer composition where inheritance
does not provide a necessary guarantee.

Observer lifetimes, queued commands and wrappers still require explicit failure and
cancellation semantics. A pattern name does not establish those guarantees.

Review-only requests produce a recommendation, not an unsolicited rewrite. For an
authorized implementation, preserve the public contract, check real callers, and
verify the behavior that motivated the change. Do not introduce unused extension
points, a DI container, a new event bus or a parallel framework merely to fit a pattern.
