# Data flow, shared state, and property wrappers

Apply this reference only within the owning project's supported SDK, architecture,
and conventions. Verify version-sensitive claims in the SDK or official documentation.
Preserve existing UIKit/Combine integration and file organization where appropriate.

It is important that SwiftUI body code and logic code be kept separate in order to make code easier to read, write, and maintain. That usually means placing code into methods rather than inline in the `body` property, but often also means carving functionality out into separate `@Observable` classes.

These rules help ensure code is efficient and works well in the long term.


## Shared state

- Match actor isolation to actual access and ownership. UI-owned mutable models often belong on `@MainActor`; `@Observable` alone does not require every model to use it. Inspect callers and the project's default isolation before reporting a missing annotation.
- Preserve the existing Observation or Combine architecture. For an Observation model, use `@State` when the view owns its lifetime and `@Bindable` / `@Environment` where their semantics fit.
- Do not migrate working `ObservableObject`, `@Published`, `@StateObject`, `@ObservedObject`, or `@EnvironmentObject` usage merely to modernize a local change. A migration needs an actual requirement and supported deployment target.
- Where possible, give custom value types stored by an `@Observable` class `Equatable` conformance. Observation can then skip notifications for assignments equal to the current value. Structs and enums with associated values need explicit conformance; arrays are equatable only when their elements are.

Observation records the stored properties a view accesses. Reading a computed property also records every stored property used by its getter, so a getter does not narrow dependencies. A stored struct is one dependency: if `library.book` is a struct, reading `library.book.title` also subscribes to changes in `library.book.pageCount`. A computed `var bookTitle: String { book.title }` has the same dependency. Tracking just the title requires separating the fields into stored observable properties or making that nested model observable. These structural changes belong in a deep review or an investigation of excessive updates; see `performance-plus.md`.


## Local state

- If a view stores a class instance that contains expensive-to-recompute data, e.g. `CIContext`, it can be stored using `@State` even though it is not an observable object. This effectively uses `@State` as a cache – storing something persistently, but not doing any change tracking on it since it's not an observable object.


## Bindings

- Prefer bindings projected from `@State`, `@Binding`, or `@Bindable`, including key-path bindings, over `Binding(get:set:)` in `body`. Closure bindings can add allocations and comparison problems that cause unnecessary updates. For conversions or lookups, expose a writable computed model property such as `$model.distanceInMiles`; for a parameterized lookup, use a labeled subscript such as `$model[quantityFor: product]`.
- Preserve behavior when refactoring bindings. A setter handles writes through that binding, including equal-value assignments; `onChange()` responds to observed value changes, including programmatic changes. Do not substitute one for the other without checking effects. Leave a custom binding intact when an equivalent replacement is unclear.
- If the user needs to enter a number into a `TextField`, bind the `TextField` to a numeric value such as `Int` or `Double`, then use its `format` initializer like this: `TextField("Enter your score", value: $score, format: .number)`. Apply either `.keyboardType(.numberPad)` (for integers) or `.keyboardType(.decimalPad)` (for floating-point numbers) as appropriate. Using the modifier alone is *not* sufficient.


## Working with data

- Prefer to make structs conform to `Identifiable` rather than using `id: \.someProperty` in SwiftUI code.
- Never attempt to use `@AppStorage` inside an `@Observable` class, even if marked `@ObservationIgnored` – it will *not* trigger view updates when a change happens.
- In mutable collections displayed by `ForEach`, `List`, or `Table`, identity must come from the element. Indices and offsets describe positions, so inserts, deletes, moves, and filtering can reset row state and disrupt animations. Avoid `ForEach(books.indices, id: \.self)` and `enumerated()` identified by `\.offset`. `ForEach(books.enumerated(), id: \.element.id)` is correct on iOS 26+, and `ForEach(Array(books.enumerated()), id: \.element.id)` below that; fixed ranges and constant collections are not a problem.
- Allocate an element's identity when storing the element, not while evaluating `body`. For example, mapping labels to fresh `Bookmark` values inside `ForEach` recreates every row if each initializer generates a UUID. A stored `let id = UUID()` is valid when its containing value survives body evaluations in `@State` or a model.
- Use a compact, immutable key to identify objects. Avoid `id: \.self` for a full struct, which hashes every field for every row on updates; reserve it for small unique values such as integers, UUIDs, URLs, or short strings. Do not derive identity from editable fields, such as `var id: String { caption }`: changing the caption then replaces the row and loses focus or selection.


## SwiftData

- If you only need the number of items matching a query, consider `ModelContext.fetchCount()` with a fetch descriptor. This will *not* live update if the data changes unless something else triggers the update, such as `@Query`, so it should be used carefully.

For a measured SwiftData bottleneck, use the available `perf-swiftdata` skill or the project's existing profiling guidance. Do not install a companion skill merely to review data flow.

## If the project uses SwiftData with CloudKit

- Never use `@Attribute(.unique)`.
- Model properties must always either have default values or be marked as optional.
- All relationships must be marked optional.
