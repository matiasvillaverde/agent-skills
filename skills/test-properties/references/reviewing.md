# Reviewing Property-Based Tests

A property test can pass for years while asserting nothing. These are the ways that
happens, worst first.

Report demonstrated gaps with their consequence and evidence. Rank them by the protected
contract and plausible failure, not a fixed severity assigned to a test-writing style.

| Candidate gap | What to establish |
|---|---|
| Tautology | Assertion is true regardless of a plausible wrong implementation |
| Inadequate domain | Excessive discards, unreachable preconditions, or failures ignored by the runner |
| No useful assertion | Neither a result assertion nor a meaningful error/crash contract is checked |
| Reimplementation | Expected results reproduce the implementation's logic and can share its defect |
| Missing property | A required behavior, such as sorted order, is not constrained by retained evidence |
| Over-filtering | Generation spends its useful budget discarding values that a direct strategy could produce |
| Unsuitable settings | The actual budget misses important coverage or permits unbounded work; a small count alone is not a defect |

## Tautological

```python
@given(st.integers())
def test_useless(x):
    result = compute(x)
    assert result == result
```

Nothing about `compute` can make this fail.

**But `f(x) == f(x)` is not automatically tautological.** It is a real determinism
property whenever `f` is not obviously pure — serializers over dicts or sets, anything
touching iteration order, hashing, or time. `pickle.dumps(obj) == pickle.dumps(obj)`
genuinely fails for objects with a nondeterministic `__reduce__`. Ask whether a broken
implementation could falsify it. If yes, it is a property; if no, it is noise.

## Vacuous

```python
@given(st.integers())
def test_vacuous(x):
    assume(x > 100)
    assume(x < 50)
    assert compute(x) > 0
```

The assumptions cannot both hold: no generated value reaches the assertion. Inspect
the actual framework's health/exhaustion result and ensure CI propagates failure;
do not count discarded attempts as passing cases. A satisfiable filter such as
`assume(x == 42)` can still collapse the exercised domain to one value. Generate the
intended domain directly and preserve important explicit examples separately.

## Reimplementation

```python
@given(st.integers(), st.integers())
def test_reimplements(a, b):
    assert add(a, b) == a + b
```

If `add` is `a + b`, this asserts `a + b == a + b`. The test survives any bug the two
expressions share. Reach for an algebraic property instead — commutativity, identity,
associativity — which constrains the function without restating it.

## Finding the tests

```bash
rg "@given\(|from hypothesis import" --type py
rg "fc\.(assert|property)" --type ts --type js
rg "proptest!|#\[quickcheck\]" --type rust
```

## What to push for

Compare each test against the property catalog in SKILL.md and identify a plausible
wrong implementation that its assertions would miss. A suite that checks
`len(sort(xs)) == len(xs)` and never checks ordering is the common case.

Also worth flagging: floating-point equality without a tolerance, assertions on
dict/set iteration order, and anything reading the clock — these produce flakes that
get blamed on Hypothesis and then get deleted.
