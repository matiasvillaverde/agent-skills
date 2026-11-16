# Operational surfaces

Choose existing approved tools for the current environment. Inspect tool/version help before
using command examples from documentation. Tool installation and service changes are separate
from a request to test a feature. None of these rows is a mandatory full checklist.

| Surface | Useful observations | Common false proof |
| --- | --- | --- |
| Browser/web | Console and failed requests, network initiators/waterfalls, request/byte count, server correlation, long tasks and retained DOM/listeners across navigation. | Screenshot or 2xx without persisted effect; browser snapshot formatting mistaken for a product defect; high RSS called a leak; sampled traces called complete coverage. |
| Apple/native | Unified logs/signposts and crash reports for the named app; Instruments/xctrace CPU, allocations, hangs, network or frame evidence as relevant; lifecycle and permissions. | Debugger/Simulator timing presented as device-release performance; wrong process/build, lost symbols, profiler overhead or empty capture ignored. MetricKit production aggregates cannot prove a particular local run. |
| CLI/TUI | Exit status and separate stdout/stderr, wall time/CPU/peak memory, output files, subprocesses/descriptors, stdin EOF, interruption and terminal lifecycle. | Success from the final pipeline stage; a still-running child overlooked; buffered first output mistaken for total duration; prompt waiting for legitimate input labeled a hang. |
| Backend/API | Correlated request/trace and datastore readback, query count, auth boundary, retry attempts, timeouts and downstream effects. | A server success log before transaction commit; all retries aggregated into one request; wrong tenant/cache endpoint queried for readback. |
| MCP/tool server | Actual client/transport version, discovery and tool invocation, tool result/error, payload size, elapsed time, upstream calls, cancellation/disconnection and owned child cleanup. | JSON-RPC success counted as tool success; tool listed but never called; stdout logs corrupt stdio framing; optional capability assumed from a newer specification. |
| Worker/job/pipeline | Enqueue/start/completion identities, lag, bounded backlog, retry/dead-letter states, input/output content, restart recovery and duplicate durable effects. | Accepted ID or successful enqueue called completion; a stale artifact from a previous run; worker death mistaken for cancellation of downstream effects. |
| Library/embedded/other | Public consumer/harness with representative inputs; output correctness, lifecycle ownership and platform-supported diagnostics. | Mock wiring or host emulation presented as hardware qualification; unsupported instrumentation silently omitted from a pass. |

## MCP specifics

Read the supported revision's transport/result rules and advertised capabilities. Record the
actual compatibility path, including initialization or per-request metadata as applicable.
Separate transport errors, application/tool errors, pending/input-required results and final
business effects. Check cancellation and retries only under the actual revision/extension contract;
loss of the client connection need not guarantee the underlying mutation stopped.

For large results, measure actual bytes/content and pagination/truncation behavior. A successful
first page is not complete coverage. Check whether bounded output remains sufficient to act on
the result; do not replace a functional requirement with a universal token cap. Protocol traces
may contain arguments, tokens and customer content: use synthetic inputs and scoped redaction.

## Faults and profiles

Existing fault hooks, test proxies or local fixture servers can control the relevant boundary.
Toxiproxy is one option for TCP faults; it is not a universal HTTP/application failure simulator.
Use known fault activation and recovery observations. Preserve invalid-input versus upstream-error
semantics; don't call the feature faulty because a deliberate injection behaved as specified.

Map any unfamiliar platform to operation identity, start/end signals, persistent effects, owned
resources and observable errors. Missing probes remain blocked or unmeasured. Do not replace
real-device/network evidence with fabricated fixtures while retaining a real-world claim.
