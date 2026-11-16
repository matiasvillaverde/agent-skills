# Audio delivery and streaming prerequisites

Use this after the trace shows time before usable compressed audio/PCM. Preserve the player's
chosen architecture. Source review: 2026-11-16; see the [source and qualification notes](sources.md).
This reference proposes investigations, not measured gains or universal startup targets.

## Identify the delivery contract

- Direct file/progressive stream, HLS VOD/event/live, LL-HLS, or a custom framed protocol?
- Record container, codec, channels, encryption, initial rendition and media timestamp.
- For HLS, retain the selected multivariant and media playlist roles, map/init section,
  segment/part dependency, discontinuity state and key/license prerequisites.
- Pin deployed client/OS features and current authoring/specification versions before changing them.

`AudioFileStream` parses supported file data as it arrives; `AudioConverter` converts formats.
Neither is a documented complete HLS client. Do not feed a playlist, MPEG-TS or arbitrary fMP4
fragments into these APIs merely because the underlying audio is AAC. Establish the container,
demux/parser, decoder configuration and timestamp contracts independently. The archived and current
parser overviews have different format lists; qualify the exact combination instead of extrapolating.
[Parser contract](https://developer.apple.com/documentation/audiotoolbox/audio-file-stream-services),
[converter contract](https://developer.apple.com/documentation/audiotoolbox/audio-converter-services).

## Mark what actually arrives

Track request dispatch → response/first body → required metadata and first complete packet → first
decoded PCM → render handoff. Keep these separate from the parent skill's audible-output endpoint.
Timestamp first useful body data in the existing incremental receive path, not only task completion.
Record application queue/handoff delays so they are not attributed to transport.

URLSession's data delegate may receive multiple chunks. Those boundaries are neither codec packet
boundaries nor HLS part boundaries. Buffer partial input correctly and bound pending bytes/work.
In an existing NWConnection path, inspect receive minimum length, completion rearming, framing,
errors and cancellation: each `receive` call schedules one completion.
[URLSession delivery](https://developer.apple.com/documentation/foundation/urlsessiondatadelegate/urlsession(_:datatask:didreceive:)),
[NWConnection contract](https://developer.apple.com/documentation/network/nwconnection/receive(minimumincompletelength:maximumlength:completion:)).

HLS fMP4 requires its applicable initialization section; packed audio has different metadata and
timestamp rules. Check whether startup waits for bytes, complete packets, format information,
decryption, or a whole-resource accumulation step. A successful response does not prove decodability.
[HLS media formats](https://www.rfc-editor.org/rfc/rfc8216.html#section-3).

## Resolve the request dependency path

For every request needed before first PCM, record role, task/attempt identity, dispatch and body
timing, status, redacted destination, bytes, cache evidence, redirects and result consumption.
Draw serial dependencies and overlap. Do not add all concurrent durations as startup cost.

| Suspected gate | Inspect | Bounded candidate |
| --- | --- | --- |
| Authorization/key/license | Refresh, challenge and key dependency timing | Reuse valid authorized state or overlap independent prerequisites |
| Discovery/redirects | Host changes, redirect transactions, serial playlist loads | Remove avoidable dependency only when its semantics remain intact |
| Init/media layout | Map applicability, required metadata position, first packet availability | Fix packaging or incremental consumption for the actual parser |
| Range/retry | Returned status/range, resource identity, duplicate bytes, retry reason | Correct offset/version handling and bounded retry policy |
| CDN/origin | Cache headers, playlist age, upstream evidence, stalled cache fill | Correct relevant cache/freshness behavior with the delivery owner |
| Stale seek/cancel work | Generation identity and canceled-result use | Stop obsolete delivery and prevent stale data entering the active stream |

These are hypotheses. Preserve authentication/DRM and supported failover; redact signed URLs,
cookies and keys. Do not classify local-cache metrics as evidence of a CDN cache hit.

## Separate live delay from startup

Report request-to-audio and distance behind live independently. For VOD, the content is already
produced; LL-HLS does not remove a live-encoding wait that does not exist. For live, parts,
blocking reloads, preload hints and rendition reports work together with the origin and CDN.
An older cached playlist may start quickly while placing playback farther from live.
[LL-HLS operation](https://developer.apple.com/documentation/http-live-streaming/enabling-low-latency-http-live-streaming-hls).

Before shortening parts, check independent decoding boundaries, audience RTT, delivery support,
request overhead, playlist update costs and subsequent stalls. Follow the applicable Apple part
duration and hold-back rules; example part sizes are not TTFA targets. Current HLS draft Appendix
B permits HTTP/2 or HTTP/3 and specifies additional delivery behavior; Appendix C handles CDN
tune-in. HTTP/2 Push from early LL-HLS material was replaced by blocking preload hints.
[Authoring rules](https://developer.apple.com/streaming/hls-authoring-specification-for-apple-devices.html),
[draft -22](https://datatracker.ietf.org/doc/html/draft-pantos-hls-rfc8216bis-22),
[WWDC20 correction](https://developer.apple.com/videos/play/wwdc2020/10228/).

Apple's June 2026 preliminary draft adds `TYPE=KEY` preload hints to distribute key-rotation load.
Treat that as versioned capability, not proof every OS preloads keys or that startup improves.
On the review date, IETF's -22 was still an Informational independent submission in the RFC Editor
queue; Apple's `-wwdc2026` PDF is a newer preliminary text, not the published replacement RFC.
[2026 update](https://developer.apple.com/streaming/Whats-new-HLS.pdf),
[preliminary draft](https://developer.apple.com/streaming/HLS-draft-pantos.pdf).

## Interpret transport measurements

For app-owned URLSession work collect task metrics and every transaction's available timing,
`networkProtocolName`, `isReusedConnection` and `resourceFetchType`. Keep missing values as missing;
incomplete work and reused/proxied connections can change the timing fields. `responseStartDate`
is first response byte, not first decoded PCM. Correlate with body/parser markers.
[Transaction metrics](https://developer.apple.com/documentation/foundation/urlsessiontasktransactionmetrics),
[task metrics](https://developer.apple.com/documentation/foundation/urlsessiontaskmetrics).

Check actual protocol, service-discovery state and reuse before suggesting transport changes.
Alt-Svc learned on one run can change the next; HTTP/3 being enabled does not prove it was used.
Profile bounded independent concurrency; more requests/connections can compete with startup media.
Use URLSession for existing HTTP work; custom Network APIs need their own framing and telemetry.
Do not rewrite networking solely to obtain QUIC or lower the API layer.
[Apple transport/discovery explanation](https://developer.apple.com/videos/play/wwdc2021/10094/).

## Reject misleading improvements

- Compare equivalent content, selected quality/codec/channels, start timestamp and leading silence.
- Separate cold/warm app, connection/discovery, client cache and CDN cache conditions.
- Keep actual network/path conditions and the fraction of failed/canceled starts with latency results.
- Require first-PCM/audible improvement at the intended boundary, not just faster request completion.
- Report startup together with stalls/underruns, bytes, requests and live-edge delay where applicable.
- Include canceled prefetch, retry and quality-switch costs; retain the simplest measured improvement.
