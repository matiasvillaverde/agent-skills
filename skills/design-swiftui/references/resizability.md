# Resizable SwiftUI layouts

Apply this reference only within the owning project's supported SDK, architecture,
and conventions. Verify version-sensitive claims in the SDK or official documentation.
Preserve existing UIKit/Combine integration and file organization where appropriate.

Treat window dimensions as changeable throughout a scene's lifetime. Inspect the
actual deployment targets, available SDK, and supported device families first.

- Base layout on available space and appropriate size classes, not a hardcoded
  screen size or device model. Account for windows, multitasking, and rotation.
- Preserve important features and controls in compact and short windows. Use
  scrolling or a suitable `ViewThatFits` alternative when content may not fit.
- Prefer system navigation, tabs, and toolbars where they meet the product design.
  Respect safe areas and the keyboard; measure geometry only when needed.
- Keep per-window selection and navigation state separate when multiple scenes
  are supported. Sharing domain data does not require sharing navigation state.
- Check Dynamic Type, right-to-left text, VoiceOver order, pointer and keyboard
  access, sheets, and popovers at the supported size extremes.
- Confirm any new adaptive-layout API against the installed SDK and current Apple
  documentation. Do not change deployment targets or build settings to apply a tip.

Report device and window configurations actually tested, and any remaining gaps.
