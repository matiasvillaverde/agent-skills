# Apple platform design and evidence

Read for native UI design or a review involving platform conventions. Select the target and
affected topics; do not load every HIG page for a local edit. Shared brand roles and behavior
can coexist with platform-specific navigation, density, controls and input.

| Target | Read before choosing the design | Verify where the change affects it |
| --- | --- | --- |
| iOS | [iOS HIG](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios.md), [layout](https://developer.apple.com/design/human-interface-guidelines/layout.md), relevant [tabs](https://developer.apple.com/design/human-interface-guidelines/tab-bars.md)/controls. Prioritize reachable actions, content and navigation continuity. | Small/large supported layouts, orientation/keyboard transitions, back navigation, Dynamic Type, long/RTL text and VoiceOver. Device-specific layouts need their current guidance; do not hardcode one phone size or navigation position. |
| iPadOS | [iPadOS HIG](https://developer.apple.com/design/human-interface-guidelines/designing-for-ipados.md), [windows](https://developer.apple.com/design/human-interface-guidelines/windows.md), [WWDC iPad design](https://developer.apple.com/videos/play/wwdc2025/208/). Choose tabs, sidebar or split hierarchy for the task and available space. | Continuous narrow/wide and short/tall resizing, collapsed columns and selection continuity, touch/keyboard/pointer, relevant menus and multiwindow behavior. iPad is not an enlarged phone mockup. |
| macOS | [macOS HIG](https://developer.apple.com/design/human-interface-guidelines/designing-for-macos.md), [menu bar](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar.md), [typography](https://developer.apple.com/design/human-interface-guidelines/typography.md). Preserve useful density, window behavior, standard commands and precision input. | Resizing, active/inactive windows, menus/shortcuts, keyboard focus, pointer targeting and supported input modes, text legibility and VoiceOver. Native Mac and iPad-on-Mac are different targets. macOS does not offer iOS Dynamic Type; verify the app's actual text-size accommodations. |

For watchOS, tvOS or visionOS, read the corresponding
[HIG platform entry](https://developer.apple.com/design/human-interface-guidelines) before applying
phone assumptions. For UIKit/AppKit integration, preserve the existing framework and inspect its
official component guidance. Do not rewrite it in SwiftUI merely to use this skill.

## Follow official design guidance into supported APIs

Read the relevant platform overview plus the affected component/foundation, then follow its
developer links to exact API declarations. Apple pages may expose **View Markdown**, which is
readable without the JavaScript documentation shell. Follow that link or a verified official
alternate; a search snippet or mirror does not establish an overload's availability.

Check project deployment targets, installed SDK and exact member availability separately. Current
samples can require a newer SDK than the containing type. For example,
[`TabView`](https://developer.apple.com/documentation/swiftui/tabview.md) and
[`Tab`](https://developer.apple.com/documentation/swiftui/tab.md) have different introduction versions.
[`sidebarAdaptable`](https://developer.apple.com/documentation/swiftui/tabviewstyle/sidebaradaptable.md)
also demonstrates different platform presentations of one API. Confirm current details rather than
freezing version numbers in recommendations. A runtime guard cannot make an old SDK know a new API.

Use [Apple Design Resources](https://developer.apple.com/design/resources/) for the appropriate
platform/version kit and official examples. Inspect actual assets and licenses before using them;
reading the resource index is not inspecting the kit. HIG recommendations, product requirements,
API constraints and tested runtime behavior are different kinds of evidence.

## Materials, typography and interaction

[Materials guidance](https://developer.apple.com/design/human-interface-guidelines/materials.md) and
[Liquid Glass adoption](https://developer.apple.com/documentation/technologyoverviews/adopting-liquid-glass.md)
distinguish controls/navigation from content. Prefer supported standard components and preserve
content legibility. Do not spread custom glass over every card, reproduce system materials with
sampled static colors or raise deployment targets to match the latest sample. Check transparency,
contrast and motion preferences in relevant states.

Use semantic type/color roles and the product's existing tokens. Custom fonts are valid when
licensed, correctly loaded and legible with the necessary glyphs and scaling. No universal font
or weight ban follows from HIG. Platform text sizing and units differ; preserve deliberate hierarchy.

[Buttons HIG](https://developer.apple.com/design/human-interface-guidelines/buttons.md) recommends
44×44 pt hit regions as a general rule for ordinary touch controls; hit area and drawn size differ.
Check adequate separation as well as size. Context-specific smaller-control guidance is not a
reason to shrink ordinary controls or a universal App Store minimum. Desktop precision input,
visionOS and other platforms have their own guidance. Preserve a stricter product requirement.

## Verify the intended native experience

Inspect actual previews or a running app at relevant layout extremes, then exercise the changed
task and meaningful loading/empty/error/recovery states. Use available Xcode previews, Simulator,
RocketSim, device or UI-test tooling; check installed capabilities instead of inventing commands.
Combine screenshots with interaction/accessibility evidence. HTML/canvas approximations do not
prove native layout, VoiceOver, focus, keyboard, gesture or material behavior.

Report the target/OS and states actually checked, implementation/API gaps and untested device
behavior. Retain useful design artifacts and compact evidence; delete only task-owned temporary
builds/captures when finished. Do not purge shared simulator data or global caches.
