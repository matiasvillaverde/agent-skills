# Geographic measurement and replica decisions

Read for regional differences, network attribution or topology changes. Use the user's
existing providers and authorized test infrastructure. This is not a deployment recipe.

## Measure the path users actually take

Choose locations from affected users and a useful comparison cohort. Record actual origin
region, ASN/network, datacenter versus residential/mobile access, IP family, resolver,
VPN/proxy/Private Relay state, time window, method/payload, protocol, cache and connection
reuse. Record the responding edge and origin/data placement when observable; a connected
IP can identify a proxy or CDN, not the application server.

Keep user telemetry, regional synthetic probes and local lab emulation separate. Throttling
can model delay/bandwidth, but not reproduce another region's DNS, peering, CDN selection or
mobile radio. Country headers change application inputs, not the physical route. A VPN adds
its own path and exit behavior. State the coverage achieved, including unavailable probes;
one city or one cloud ASN does not represent a continent's users.

Repeat comparable measurements within the authorized budget and across relevant time
windows. Compare regional distributions separately; weight a combined population only when
the actual user mix is known. A few remote requests can reveal a lead, not establish p99.
Separate availability failures from incomplete/absent measurement results.

## Choose tools with known boundaries

| Tool | Useful use and limits |
| --- | --- |
| Existing RUM/native client telemetry | Establish affected populations and real interaction latency. Preserve collection/sampling/privacy policy; missing regions are not passing results. |
| Installed curl or equivalent | Controlled HTTP timing from a known host. Match actual method, response validation and body boundary; record redirects, connection reuse and protocol. A fresh CLI process usually measures a new connection. |
| [Globalping](https://github.com/jsdelivr/globalping/blob/7b28a4fc9d94380f3be828b056288668efb9abd7/public/v1/spec.yaml) | Public outside-in HTTP/DNS/ping/traceroute/MTR. Creating a measurement sends traffic and can use credits; reading an existing result is different. Inspect current capabilities, limits, selected networks and returned probe count. Its HTTP default is HEAD; request a supported representative method explicitly. |
| [RIPE Atlas](https://atlas.ripe.net/docs/getting-started/user-defined-measurements/) | Existing public measurements or authorized active network measurements. New work requires access/credits. HTTP measurement eligibility is restricted; its presence in a schema is not permission or availability. |
| Existing private regional runners | Authenticated journeys or non-public targets, with actual network origin recorded. Do not provision new regions or buy a service merely to complete a review. |

Globalping's [terms](https://github.com/jsdelivr/globalping/blob/master/docs/terms/Terms%20of%20Use.md)
make inputs/results public; they can include response data. Keep credentials, signed URLs,
secret headers, confidential hostnames and private response contents out. A reachable URL
is not necessarily safe to disclose. Use an approved non-sensitive diagnostic target or an
authorized private runner. Atlas non-public results do not make volunteer probe execution
a trusted private environment. Verify current visibility before creating measurements.

Ping and traceroute answer network questions, not application completion. Intermediate
non-responses or ICMP rate limiting alone do not establish end-to-end packet loss or a
service outage. Correlate with destination responses, HTTP behavior and server evidence.

## Normalize timings before comparing them

Record units and exact start/end events from the actual tool version. The
[curl manual](https://curl.se/docs/manpage.html) describes cumulative timers in seconds:
`time_namelookup`, `time_connect`, `time_appconnect`, `time_starttransfer`, `time_total`.
For a simple fresh direct HTTPS request, adjacent differences can help estimate phases;
the markers themselves must not be added. Redirects, proxy setup, uploads, reuse,
multiplexing and protocol changes require more careful transaction-level interpretation.

Globalping's [schema](https://github.com/jsdelivr/globalping/blob/7b28a4fc9d94380f3be828b056288668efb9abd7/public/v1/components/schemas.yaml)
defines `firstByte` in milliseconds from established TCP/TLS connection to the first byte.
It is not the same boundary as curl `time_starttransfer`. Neither isolates origin CPU.
Do not label the unexplained remainder as network RTT or divide it by two to assert one-way
latency. Preserve absent, failed and unreported phases instead of converting them to zero.

## Decide whether replicas or placement can help

Draw the current critical path with locations, routing unit and consistency requirements.
Count serial remote round trips and distinguish edge hits, origin misses and private data
operations. [Workers placement](https://developers.cloudflare.com/workers/configuration/placement/)
illustrates why compute near its backend can outperform compute near the user. Pooling
can avoid setup but does not erase the distance of subsequent queries.

| Proposed change | Evidence and tradeoff to examine |
| --- | --- |
| More app replicas | Per-replica admitted work, CPU/wait/queue distributions, readiness and warmup; shared database/provider limits and multiplied pools. Existing HTTP/2/gRPC connections may stay pinned; connection count is not work balance. |
| Geographic routing | Actual eligible endpoints, user network routes, affinity/session state, data location and health. DNS/connection caches can delay adoption. Nearest region is not necessarily the fastest complete operation. |
| Read replicas | Whether this operation can use a replica, observed visibility lag, read-your-writes and fallback behavior. A lower read time is not a win if it violates freshness. |
| Synchronous replicas/quorum | Required acknowledgements, leader location, network distance, durability and failure behavior. A nearby read replica does not necessarily shorten the write or strong-read path. |
| Cache/CDN | Cache key/isolation, hit/miss cohorts, freshness and invalidation; a cache hit improvement says little about uncached writes or private misses. |

[PostgreSQL replication](https://www.postgresql.org/docs/18/warm-standby.html) distinguishes
asynchronous visibility from synchronous commit/replay waits. Its reported replay lag is
not a forecast of catch-up time; check current monitoring semantics and workload activity.
[Spanner](https://docs.cloud.google.com/spanner/docs/replication) illustrates another limit:
a local strong read can still need leader communication, and read-only replicas do not
enlarge write quorum. Apply the selected database's actual contract, not a generic replica rule.

Balance admission/routing against surviving capacity. Ejecting slow replicas or aggressive
failover can overload the remainder. Consider recovery, rebalancing and warm caches in a
bounded test when changing those policies; do not introduce a multi-region architecture by default.

Retries and hedging need a shared deadline, safe operation semantics and aggregate limits
on attempts, concurrency and residual work. Cancellation acknowledgement does not prove
remote execution stopped. Measure useful completions, duplicate cost and overload; a hedge
against the same congested dependency may worsen the tail. The original
[Tail at Scale](https://www.barroso.org/publications/TheTailAtScale.pdf) motivates such
techniques in particular workloads, not a universal speedup or a free resilience layer.
