---
name: clarify
description: Research and sharpen a product idea, design or technical plan through focused questions and grounded recommendations. Use when the user asks to be interviewed, grilled, challenged or helped resolve consequential ambiguity; skip an interview for already clear routine work.
---

# Clarify

Help the user make the decisions that matter. Go as deep as the uncertainty warrants,
while spending their attention on questions you cannot responsibly answer yourself.
The outcome is shared, actionable understanding, not a large questionnaire.

## Understand before interrupting

Use the active request and prior answers. Read the relevant instructions, existing brief,
code, configuration and authorized connected context. Preserve the user's chosen product,
constraints and earlier decisions. Distinguish intended behavior from today's implementation;
code can reveal a defect rather than settle a product-policy question.

Keep a small working map of what is known, what was decided, what you propose and what
remains unresolved. Identify dependencies between decisions. Do not ask the user to
choose a framework already specified in the project, repeat a stated budget, find a file
you can locate, or approve ordinary research/process choices. If the active subject itself
cannot be identified from context, ask that before researching a guessed product.

For each possible question, ask internally: **Would plausible different answers change
the scope, user experience, architecture, acceptance check or next useful investigation?**
If not, drop it. Resolve discoverable facts yourself. Make delegated, reversible technical
choices and state consequential assumptions. Reserve questions for unresolved intent,
preferences, tradeoffs, contradictions or consequential facts only the user can supply.

## Bring evidence and a recommendation

When an open choice depends on platform behavior or prior art, research current official
documentation, existing implementations and relevant similar products. Compare the specific
workflow or constraint, not a list of famous products. Follow new evidence when it changes
the decision. Use [research and recommendations](references/research.md) to keep this
bounded, current and honest. Do useful discovery before asking, but don't delay a real
user decision with unrelated research.

For a decision question, offer a clear recommendation, its reason and the main cost or
tradeoff. Ground it in this user's goals and verified evidence; cite material external
claims. Present credible alternatives fairly, including reuse or a smaller solution when
appropriate. A recommendation remains a proposal until accepted or delegated. Never turn
competitor behavior, a convention or an unsupported “best practice” into a requirement.

When discovering the user's actual problem or past experience, ask neutrally instead of
suggesting the answer. For example, ask about the last time the workflow failed before
recommending a dashboard. Don't guess their preferences to manufacture agreement. If the
evidence cannot support a recommendation, explain the uncertainty and the smallest useful
research step or experiment rather than inventing a ranking or confidence percentage.

## Ask in useful rounds

Start with the highest-impact unresolved decision whose prerequisites are known. Usually
ask one question, or a small batch of two or three independent questions when easier to
answer together. Keep dependent follow-ups for after the answer. There is no minimum
question count or fixed total: a complex plan can need many rounds; a clear request needs
none. Use [question patterns](references/questions.md) when framing or pacing is difficult.

Make each question self-contained and specific: what must be decided, why it matters,
the recommendation with its rationale, and the meaningful alternatives. Use plain language
and a concrete scenario. Offer concise mutually exclusive options when they fit, while
allowing a free-form response. Avoid leading yes/no wording, bundled unrelated decisions,
false dilemmas and generic “anything else?” rounds.

Use the host's available question tool and its actual schema. Prefer asynchronous input
when independent work can continue. Keep required answers pending and don't execute work
that depends on them. Silence, a preselected option and elapsed time are not acceptance.
If no question tool is available, ask concisely in the host's permitted response channel.
In noninteractive work, report genuine blockers and continue only within supported scope;
do not fabricate answers or wait in an unanswerable interview.
Use only a question tool available in the current mode. For an open discovery question,
use free-text input when supported; don't invent choices such as “tell a story” versus
“no example” just to fill an options field.
Follow the [host delivery guidance](references/questions.md#host-delivery) rather than
substituting a different tool's schema or falling back to prose when a valid tool exists.

After each answer, update the working understanding, retire answered questions and
recompute what is worth asking next. Accept corrections and revise affected recommendations.
Probe a vague or contradictory answer only where the unresolved distinction matters.
“I don't know” is useful information: propose a default, investigation or explicit deferral
as appropriate. Respect “you decide,” “proceed” and “stop asking” within existing authority.
Do not require ritual confirmation of an otherwise clear answer.

## Finish with something usable

Stop when the next authorized step is clear and remaining details can be delegated,
researched or explicitly deferred, or when the user ends the interview. Briefly capture
the outcome/users, scope and non-goals, important decisions and rationale, constraints,
observable success checks and unresolved blockers. Separate user decisions from your
assumptions. Update an existing owning brief when persistence is useful and authorized;
don't create a parallel spec or commit/publish it by default.

If implementation was requested, continue the authorized work without another approval
loop. If the request was only to interview or challenge the idea, deliver the brief and
stop there. Unresolved authority, destructive scope or essential private facts remain
unresolved even when the user delegates ordinary design choices. The existing
`intent-driven-development` skill handles routine clarification during implementation;
this skill adds a focused research and interview workflow, not a mandatory planning phase.

[Research basis](references/sources.md) records useful community ideas and rejected rules.
