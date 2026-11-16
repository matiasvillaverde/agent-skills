# Comparing financial numbers

Keep inputs, dates, units and transformations attached to the result. Use executable
arithmetic for material calculations; a source's displayed precision is not proof of accuracy.

- **Price return:** ending comparable price / starting comparable price − 1. Adjust
  consistently for splits. Add distributions only if the input series has not already
  included them; an adjusted close is provider-defined, not automatically a total-return index.
- **FX:** state the quotation direction. For a foreign-currency asset valued in the
  home currency, `(1 + local return) × (ending home-value of one foreign unit / starting
  home-value) − 1`. A 5% dollar fall is not the same as a 5% euro rise. Cross-rates using
  rates quoted per EUR require consistent division. Include actual conversion spreads
  when estimating an attainable net result.
- **Yield:** distinguish coupon, current yield, yield to maturity, APY/effective annual
  yield, simple annualized yield and fund distribution/7-day yields. A six-month security
  with a 4% annualized simple yield does not earn 4% over six months. Derive cash proceeds
  from actual price, face amount, dates, day-count and fees; do not treat all conventions
  as interchangeable.
- **Fees:** identify whether published returns already include fund expenses. Deduct only
  remaining platform, account, dealing, FX or other costs. A fixed subscription matters
  incrementally only if adopting the product changes it. Avoid deducting a fund TER twice.
- **Real return:** `(1 + nominal return) / (1 + inflation over the same period) − 1`.
  A backward-looking inflation print and today's annualized yield can illustrate a
  scenario but do not establish a realized return or next year's forecast.
- **Rate sensitivity:** approximate bond price return is `−modified duration × change
  in yield as a decimal`. A one-percentage-point move is 0.01, or 100 basis points.
  Duration is not maturity. This excludes carry, convexity, spread, FX, costs and taxes;
  label it a local sensitivity rather than a predicted total return.
- **Statement arithmetic:** align units, fiscal periods and accounting basis. To derive
  a single quarter from year-to-date flows, subtract the comparable prior cumulative
  period on the same accounting basis. Avoid subtracting across restatements without
  reconciling them. Do not sum balance-sheet instants into a yearly total.
- **Ratios:** show numerator, denominator and relevant dates. Missing or economically
  meaningless denominators produce unavailable/not-meaningful results, not zero.
  Do not combine current market capitalization with an unexplained stale share count,
  quarterly earnings, or forward estimates labelled as trailing results.

For changing inputs, retain base, downside and upside assumptions with the variable
that drives each difference. Do not assign numerical probabilities without a defensible
basis. Exact calculations do not make uncertain assumptions certain.
