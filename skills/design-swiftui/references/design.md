# Design

Apply this reference only within the owning project's supported SDK, architecture,
and conventions. Verify version-sensitive claims in the SDK or official documentation.
Preserve existing UIKit/Combine integration and file organization where appropriate.

## Creating a uniform design in this app

Use the existing design-system owner for shared typography, semantic colors, spacing and motion.
Keep native adaptive semantics and local geometry where appropriate. Do not add a parallel enum
of constants or tokenize every literal merely for uniformity. Read [platform design](platform-design.md)
when selecting platform conventions or consulting current HIG/API guidance.


## Requirements for flexible, accessible design

- Prefer flexible frames unless a fixed size can comfortably hold the content. Where an arrangement might run out of room, use `ViewThatFits` to attempt the preferred layout and then a smaller-space alternative, such as a horizontal control row followed by a vertical arrangement. Account for longer translations, larger Dynamic Type, and narrower windows.
- Aim for 44×44 pt hit regions for ordinary iOS touch controls, with adequate separation, following
  current Buttons HIG and any stricter product requirement. Distinguish hit area from visible size
  and platform/context-specific guidance; do not present this as a universal rejection rule.


## Standard system styling

- Strongly prefer to use `ContentUnavailableView` when data is missing or empty, rather than designing something custom.
- When using `searchable()`, you can show empty results using `ContentUnavailableView.search` and it will include the search term they used automatically – there's no need to use `ContentUnavailableView.search(text: searchText)` or similar.
- If you need an icon and some text placed horizontally side by side, prefer `Label` over `HStack`.
- Prefer system hierarchical styles (e.g. secondary/tertiary) over manual opacity when possible, so the system can adapt to the correct context automatically.
- When using `Form`, wrap controls such as `Slider` in `LabeledContent` so the title and control are laid out correctly.
- `LabeledContent` also works outside `Form` for any title-value display; it might be necessary to define a custom `LabeledContentStyle` for consistent layout across views.
- When using `RoundedRectangle`, the default rounding style is `.continuous` – there is no need to specify it explicitly.


## Ensuring designs work for everyone

- Use the project's semantic type roles and deliberate weights. Medium, semibold and bold can
  all be appropriate; a modifier preference alone is not a defect.
- Reuse shared spacing roles when they express the same intent; local layout values can be valid.
- Prefer adaptive native/asset colors. Preserve legitimate UIKit color bridging in mixed code;
  investigate actual appearance or ownership failures instead of banning it categorically.
- The font size `.caption2` is extremely small, and is generally best avoided. Even the font size `.caption` is on the small side, and should be used carefully.
