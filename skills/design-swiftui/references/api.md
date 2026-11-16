# Using modern SwiftUI API

Apply this reference only within the owning project's supported SDK, architecture,
and conventions. Verify version-sensitive claims in the SDK or official documentation.
Preserve existing UIKit/Combine integration and file organization where appropriate.

Many older SwiftUI declarations use `deprecated: 100000.0` in their SDK availability attributes. These are soft deprecations: Xcode stays quiet, so a warning-free build does not establish that the code uses current API. Review the source, and inspect a symbol's `@available` declaration in the SDK when its status is unclear.

Also check the Dynamic Type deprecations in `accessibility.md` and animatable modifier deprecations in `views.md`.

- Always use `foregroundStyle()` instead of `foregroundColor()`.
- Replace soft-deprecated `accentColor()` with `tint()`. Configure the asset catalog's accent color for an app-wide default.
- Always use `clipShape(.rect(cornerRadius:))` instead of `cornerRadius()`.
- Always use the `Tab` API instead of `tabItem()`.
- Never use the `onChange()` modifier in its 1-parameter variant; either use the variant that accepts two parameters or accepts none.
- Use `toolbarVisibility()` in place of `toolbar(_:for:)` with a visibility or `navigationBarHidden()`, and `toolbarBackgroundVisibility()` in place of the visibility overload of `toolbarBackground(_:for:)`. The older names became soft-deprecated with the iOS 18 renames. For example, `.toolbarVisibility(.visible, for: .navigationBar)`. Keep `toolbarBackground()` when it supplies a background style.
- Replace soft-deprecated `colorScheme()` with an environment override, such as `.environment(\.colorScheme, .light)`. Despite Apple's rename annotation, `preferredColorScheme()` is not equivalent: it affects the entire screen or sheet, whereas the environment override preserves the original view-and-descendants scope.
- Prefer `textInputAutocapitalization()` and `autocorrectionDisabled()` to the soft-deprecated `autocapitalization()` and `disableAutocorrection()`.
- Define a named coordinate space with `.coordinateSpace(.named("canvas"))`, replacing soft-deprecated `coordinateSpace(name:)`. Lookups still use `frame(in: .named("canvas"))`.
- Obtain color components with `color.resolve(in:)`, passing the relevant environment. It resolves red, green, blue, and opacity correctly for appearances such as light and dark mode without UIKit. Avoid soft-deprecated `Color.cgColor`, which returns `nil` for dynamic colors, including asset colors.
- When designing haptic effects, prefer using `sensoryFeedback()` over older UIKit APIs such as `UIImpactFeedbackGenerator`.
- Use the `@Entry` macro to define custom `EnvironmentValues`, `FocusedValues`, `Transaction`, and `ContainerValues` keys. This replaces the legacy pattern of manually creating a type conforming to (for example) `EnvironmentKey` with a `defaultValue`, then extending `EnvironmentValues` with a computed property.
- Prefer to rely on automatic grammar agreement when dealing with English, French, German, Portuguese, Spanish, and Italian. For example, use `Text("^[\(people) person](inflect: true)")` to show a number of people.
- You can fill and stroke a shape with two chained modifiers; you do *not* need an overlay for the stroke. The overlay was required previously, but this is fixed in iOS 17 and later.
- When referencing images from an asset catalog, prefer the generated symbol asset API when the project is configured to use them: `Image(.avatar)` rather than `Image("avatar")`.
- When targeting iOS 26 and later, SwiftUI has a native `WebView` view type that replaces almost all uses of hand-wrapped `WKWebView` inside `UIViewRepresentable`. To use it, make sure to include `import WebKit`.
- iOS 26+: `ForEach` over an `enumerated()` sequence should not convert to an array first; use `ForEach(items.enumerated(), id: \.element.id)` directly. The `RandomAccessCollection` conformance that allows this is gated to iOS 26, so earlier targets keep `ForEach(Array(items.enumerated()), id: \.element.id)`.
- When hiding scroll indicators, use `.scrollIndicators(.hidden)` rather than `showsIndicators: false` in the initializer.
- Never concatenate `Text` values or construct a `Text` label by adding strings. For example, use `Text("Folder: \(folderName)")` instead of `Text("Folder: " + folderName)`: interpolation retains a localization key, while string addition produces a plain `String` whose literal prefix is not localized.

For example, the usage of `+` here is bad and deprecated:

```swift
Text("Hello").foregroundStyle(.red)
+
Text("World").foregroundStyle(.blue)
```

Instead, use text interpolation like this:

```swift
let red = Text("Hello").foregroundStyle(.red)
let blue = Text("World").foregroundStyle(.blue)
Text("\(red)\(blue)")
```


## Using ObservableObject

If using `ObservableObject` is absolutely required – for example if you are trying to create a debouncer using a Combine publisher – you should always make sure `import Combine` is added. This was previously provided through SwiftUI, but that is no longer the case.
