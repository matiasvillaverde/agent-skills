# Delivery, audits, and alerts

Separate diagnostic severity, metric aggregation, trace sampling, and audit policy. These answer different questions and need not share storage or loss guarantees. Reuse the existing stack and documented operational contracts.

Prefer a bounded completion event at an operation boundary, with context accumulated during the work, when a record is useful. Do not duplicate a metric with a mandatory log for every successful call. [Stripe's canonical events](https://stripe.com/blog/canonical-log-lines) describe the diagnostic value; event frequency still depends on workload and cost.

Record failures according to the operation's outcome. An intermediate failed attempt that recovered is different from a failed user operation. Preserve the cause and classify at the handling boundary without repeating the same exception at every layer. [OpenTelemetry error recording](https://opentelemetry.io/docs/specs/semconv/general/recording-errors/)

Trace sampling can favor slow or failed work, but tail sampling cannot recover data discarded upstream. Use appropriately complete outcome metrics for aggregate reliability; label sampled estimates honestly. Required audit evidence must not depend on ordinary trace sampling. [Sampling](https://opentelemetry.io/docs/concepts/sampling/)

An audit contract identifies the actions that require reconstruction, the actor/target/outcome fields, access, retention, integrity, and delivery failure behavior. Do not audit every function or retain entire before/after objects by default. Queue acceptance, force-keep flags, and transport flushes do not prove durable acknowledgment. Transactional delivery or fail-closed behavior belongs only where the required guarantee justifies its cost and availability impact. [OWASP logging guidance](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)

Record a successful state change only after its authoritative commit; distinguish attempts and denials. When delivery retries can duplicate records, define a stable logical event identity and the consumer's duplicate handling. Do not infer exactly-once delivery from a successful call.

Exporter queues need capacity, backoff/deadline limits, overflow policy, and bounded shutdown. Verify unavailable and slow sinks where delivery changed. Count dropped diagnostics without recursively emitting an error for each drop. Inspect the actual transport guarantee and recovery behavior. [Collector resilience](https://opentelemetry.io/docs/collector/resiliency/)

Alerts need an owner, actionable condition, recovery condition, and runbook. Group/deduplicate related symptoms, inhibit derivative noise, expire maintenance silences, and use appropriate persistence/hysteresis. Explicitly handle sparse traffic and missing data. [Alertmanager](https://prometheus.io/docs/alerting/latest/alertmanager/)

For a meaningful SLO, burn-rate alerts connect symptoms to the rate of error-budget consumption. Google's 30-day example uses a 14.4× burn rate over both one hour and five minutes: that spends 2% of the budget in an hour, exhausting it in roughly 50 hours if sustained. It does not mean two hours to exhaustion. Treat these thresholds as examples to adapt to traffic and response time, not universal defaults. [Google SRE alerting](https://sre.google/workbook/alerting-on-slos/)
