# Command-line and terminal interfaces

Review the human task in the actual terminal, terminal accessibility implementation and
screen reader when available. WCAG web conformance is not a blanket certification for a
CLI; report concrete barriers and applicable product/platform requirements.

- Check help discovery, readable errors, clear prompts, default/selected choices and recovery.
  Meaning must survive disabled color, Unicode glyph replacement and plain output.
- Verify keyboard-only operation, documented shortcuts, sensible focus/selection, escape/back
  behavior and cancellation. A prompt should not require a pointer or a timed gesture.
- Inspect ANSI cursor movement, progress spinners, full-screen redraws and live updates with
  assistive output. They can overwhelm speech or lose context even when visually attractive.
  Prefer the existing plain/noninteractive mode for linear output; JSON is useful to scripts
  but is not automatically a readable human alternative.
- Test narrow terminals and enlarged fonts without clipping essential action/error text.
  Avoid assuming character count equals displayed width for emoji or combining scripts.
- Inspect non-TTY behavior separately: no interactive prompt in a pipe, no control sequences
  where plain machine output is promised, stable stdout/stderr and exit statuses. Preserve
  the CLI protocol while improving human messages.
- Respect existing color/no-color preferences. Verify status is also conveyed by text or
  structure, not just green/red. Confirm links and selection state remain understandable.

A captured text transcript can establish output order and escape sequences. It cannot prove
what VoiceOver, NVDA or another screen reader announces, nor that a TUI's cursor model is
usable. Record actual terminal/OS/AT versions and tested modes; retain the manual gap when
only shell execution is available. Do not add a new universal accessibility harness to
demonstrate a small CLI wording fix.

Source checked 2026-11-15: [Command Line Interface Guidelines](https://clig.dev/).
This practitioner guidance informs output design; platform assistive testing establishes
the actual experience.
