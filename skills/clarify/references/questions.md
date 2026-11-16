# Asking questions worth answering

The question should make the next decision easier. Its value comes from how it changes
the work, not from sounding challenging. Do not read a generic discovery checklist aloud.

## Host delivery

Inspect the current tools and mode. On Codex hosts exposing
`functions.request_user_input_async`, it supports Default-mode questions and free-text
input by omitting `options`. Its question uses `title` and optional string options;
don't send `header`/`id`/`question` or option-description objects from the different
`request_user_input` tool, which is Plan-mode-only on those hosts. Use current tool
documentation if the interface changes. Other clients may expose `AskUserQuestion` or
another schema; use the available one. Only use plain-text questions if no suitable tool
is available. In a simulated test, capture the tool name and valid payload without dispatch.

Put enough context, the actual decision and any recommendation/rationale in the question
itself so it still makes sense when shown separately. Keep source notes nearby and short.
For a genuine choice, label the recommended option and use meaningful alternatives.
For a request for a story or fact, omit forced options when supported. Do not add an
“Other” choice when the host already provides free text.

## Match the question to the uncertainty

| Need | Useful move | Avoid |
| --- | --- | --- |
| Understand the problem | Ask for a recent concrete incident, workflow or consequence. | Leading with a preferred feature and asking whether they like it. |
| Choose a tradeoff | Name realistic options, recommend one with a reason, and explain the main sacrifice. | “Should we use the scalable, secure option?” or unexplained A/B/C choices. |
| Clarify a vague goal | Tie “fast,” “simple” or “reliable” to the actual operation and acceptable outcome; inspect existing budgets first. | Making the user invent technical numbers with no baseline or consequence. |
| Expose a contradiction | Point to the two conflicting requirements and the behavior each would imply. | Silently dropping one constraint, or reopening settled choices without new evidence. |
| Stress-test a plan | Walk one important journey/failure through the proposed design and locate the missing decision. | Exhaustive speculative edge cases unrelated to the intended scope. |
| Resolve a fact | Inspect available code/docs/data, then ask only if it remains essential and inaccessible. | Asking for language, deployment target, roles or storage already documented. |

For example, if offline edits and shared access are both requested but precedence is
unset: “When two people edit the same item offline, should the first version keep both
copies for review or overwrite one? I recommend keeping both because losing edits would
break the stated promise; the cost is a conflict-resolution step.” Research relevant
platform constraints before offering options. Don't present this as a universal sync rule.

For discovery, prefer “Tell me about the last time you lost track of an experiment” over
“Would a dashboard solve that?” A person's story is evidence about their experience, not
proof of demand across the market. A product owner’s preference does not replace user
research when the actual uncertainty concerns other users.

## Use dependencies and prior answers

Suppose audience determines the sharing model, and sharing determines permissions. Resolve
audience before asking detailed permission questions. Independent budget and compatibility
constraints may fit in one small round. If a question tool limits the batch, follow it;
don't hide multiple decisions inside one long title.

After a correction, state the consequence briefly and retire obsolete branches. Do not
keep defending a recommendation whose assumptions changed. Don't re-ask a resolved scope
question simply because the user answered in free text instead of selecting an option.
If “yes” could refer to different pending choices, clarify that specific ambiguity.

An explicit “use your recommendation” delegates the shown choice; “you decide the technical
details” delegates that class of work. Neither resolves an unknown production target nor
authorizes destruction or disclosure. Optional assumptions can support reversible progress;
essential unresolved decisions must remain visible. A chosen default is not user testimony.

## Finish without another interview

No fixed number of rounds, confidence percentage or mandatory “anything else?” question
defines completion. Check whether another plausible answer would materially change the
next step. If not, summarize and proceed according to the request. If the user ends the
interview with blockers remaining, record them and the next safe action instead of claiming
full agreement or continuing to interrogate them.

Keep the final brief proportional. A small change can use a paragraph; a consequential
project may need a short decision record with sources and acceptance checks. Describe
verification outcomes rather than prescribing a large test inventory. Keep one owner for
the brief; amend contradictory current statements instead of appending competing answers.
