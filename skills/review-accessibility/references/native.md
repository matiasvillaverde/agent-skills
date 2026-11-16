# Apple and other native interfaces

Confirm the product's OS versions, device families, framework and available assistive
tooling. For Apple platforms, use the installed Accessibility Inspector, simulator/device
tools and existing XCTest/Swift Testing setup as appropriate. Other native platforms need
their own accessibility APIs and assistive technology; Apple's evidence does not transfer.

- Follow a complete task with VoiceOver or the relevant screen reader: discovery, reading
  order, concise localized names/values, traits, custom actions, adjustment, completion and
  recovery. Grouping should preserve meaningful actions rather than collapsing a whole screen.
- Inspect focus when a sheet appears, a view disappears, a list changes or a background task
  completes. Notifications should announce useful state without stealing focus repeatedly.
- Check Dynamic Type, bold text, contrast, differentiate-without-color and Reduce Motion
  where relevant. Enlarged text should preserve essential content and actions rather than
  silently capping sizes. Scrollable/adaptive layouts often solve truncation more honestly.
- Prefer native controls. Giving a gesture-only view a button trait does not itself provide
  the button's keyboard, switch, activation or voice behavior. Verify actual activation.
- Include Voice Control/input labels, Switch Control or keyboard access when the audience,
  interaction or reported bug calls for them. A voice label should remain meaningful when
  its displayed value changes.
- Preserve semantic labels independently from stable automation identifiers. Do not make
  test IDs spoken labels or hide meaningful views just to quiet an audit.
- Check larger text and translations together for the affected screen. Decorative imagery
  should not interrupt reading; essential imagery needs useful equivalent content.

On supported XCTest platforms, `performAccessibilityAudit` inspects the currently displayed
elements. Reach the relevant state before auditing; a launch-screen audit does not cover
the settings sheet or validation error. Configure only justified issue filters and record
what they exclude. Inspector checks and UI automation do not replace actual VoiceOver or
other assistive interaction, even if all selectors and audits pass.

Check the installed SDK for exact API/OS availability. Simulator results do not establish
device-only gestures, camera/media/permission flows, haptics or hardware keyboard behavior.
When hardware or assistive access is unavailable, give precise reproduction steps and mark
the missing verification. Do not convert a screenshot review into a claimed device test.

Primary source, checked 2026-11-15: [Apple accessibility audits and their limits](https://developer.apple.com/videos/play/wwdc2023/10035/).
For SwiftUI implementation, use the existing `design-swiftui` accessibility reference when
available, while verifying version-sensitive APIs in the project's SDK.
