# SwiftUI Views

Apply this reference only within the owning project's supported SDK, architecture,
and conventions. Verify version-sensitive claims in the SDK or official documentation.
Preserve existing UIKit/Combine integration and file organization where appropriate.

- Flag `body` properties that are excessively long; they should be broken into extracted subviews.
- If the user has created a handful of small, private helper `some View` properties for structural readability, and they both belong to the same concern as `body` and would fit in `body` at an acceptable length if inlined, these can be left alone. Otherwise, they should be extracted to new `View` structs.
- Button actions should be extracted from view bodies into separate methods, to avoid mixing layout and logic.
- Similarly, general business logic should not live inline in `task()`, `onAppear()` or elsewhere in `body`.
- Prefer to place view logic into view models or similar, so it can be tested. Use the installed swift-testing-expert skill when testing guidance is needed.
- Unless a full-screen editing experience is required, prefer using `TextField` with `axis: .vertical` to using `TextEditor`, because it allows placeholder text. If a specific minimum height is required for `TextField`, use something like `lineLimit(5...)`.
- If a button action can be provided directly as an `action` parameter, do so. For example: `Button("Label", systemImage: "plus", action: myAction)` is preferred over `Button("Label", systemImage: "plus") { action() }`.
- When rendering SwiftUI views to images, strongly prefer `ImageRenderer` over `UIGraphicsImageRenderer`.
- `#Preview` should be used for previews, not the legacy `PreviewProvider` protocol.
- When using `TabView(selection:)`, use a binding to a property that stores an enum rather than an integer or string. For example, `Tab("Home", systemImage: "house", value: .home)` is better than `Tab("Home", systemImage: "house", value: 0)`.
- Remove a `Group` that merely wraps one view; attach its modifiers to that view directly. For example, `Group { Image(systemName: "leaf") }` adds no visual behavior, but gives the compiler another type to check throughout the modifier chain. Groups containing siblings, a `ForEach`, or conditional branches serve a purpose and should stay, except around branches inside a `List` row, where a `VStack` is needed instead so that the row's shape does not depend on which branch ran.



## Animating views

- Strongly prefer the `@Animatable` macro: it supplies `Animatable` conformance and `animatableData` automatically. Mark properties that cannot or should not animate, such as integers and Booleans, with `@AnimatableIgnored`. Write `animatableData` manually only when its setter needs behavior the macro cannot generate, such as range limiting or normalization; use `AnimatableValues` on iOS 26+, or `AnimatablePair` for earlier targets.
- For an animated `ViewModifier`, use `@Animatable` rather than the deprecated `AnimatableModifier` protocol.
- Never use `animation(_ animation: Animation?)`; always provide a value to watch, such as `.animation(.bouncy, value: score)`.
- Chaining animations must be done using a `completion` closure passed to `withAnimation()`, rather than trying to execute multiple `withAnimation()` calls using delays.

For example:

```swift
Button("Animate Me") {
    withAnimation {
        scale = 2
    } completion: {
        withAnimation {
            scale = 1
        }
    }
}
```


