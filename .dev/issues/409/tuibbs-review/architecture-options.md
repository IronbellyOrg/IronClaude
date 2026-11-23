# Architecture options: Orca observer and TUIBBS future compatibility

Evidence: notes-1.md (extension architecture), notes-2.md (identity, messaging, write-back), notes-3.md (license, maturity, topology). Design only; nothing built.

## Options

### (a) Standalone Python + Rich observer, versioned snapshot contract, later consumed by a Go TUIBBS module

- **Fit:** High for R1. Matches the brainstorm design (merged-requirements.md:270, :291, :303-347) and IronClaude's toolchain. The later TUIBBS screen fits the in-tree precedent `internal/ailink/lifecycle_overlay.go` (value snapshots in, string out, :46-61, :110-135) and TUIBBS's own additive-only contract habit (internal/plugin/dispatch.go:53-62).
- **Effort:** R1 as already planned, plus one small step: `export(view)` writes a versioned JSON snapshot (fields below). The later Go screen is new work in the TUIBBS repo (a model, an ACS gate, a menu entry, a snapshot reader), estimated as one feature the size of the lifecycle overlay. UNVERIFIED as a size: not measured.
- **Risks:** The snapshot format becomes a second public contract to keep stable. Transport from the Coder host to the TUIBBS host is unexamined (assumptions.md row 4). The view-model rules must be re-implemented in Go; the Python tests become the specification, not reusable code.
- **Licensing:** Python observer stays MIT in IronClaude. The Go screen is AGPL inside TUIBBS (assumptions.md row 9). Whether exchanging only a JSON file keeps them separate works is a legal reading (row 10, UNVERIFIED).
- **R1 Signal Bridge:** Unchanged; ships in Python. **B Attention Ledger / C Decision Desk:** Ship in Python first; each adds optional snapshot fields additively, then the Go screen can follow. **Write-back:** Not in the snapshot. The snapshot is one-way by construction; write-back is a separate gated path (write-back-stage.md).

### (b) Python out-of-process gRPC plugin of TUIBBS

- **Fit:** None today. The plugin contract is one unary call with opaque request and response bytes, no stream and no terminal (proto/v1/plugin.proto:61-68; internal/plugin/dispatch.go:235-237). A plugin cannot draw a screen; a compiled-in Go screen would still be needed to show its output.
- **Effort:** High and outside IronClaude: wire the unwired plugin host into the server (no caller outside tests, assumptions.md row 6), generate Python stubs (only Go stubs exist, buf.gen.yaml:16-24), re-implement the go-plugin handshake and AutoMTLS in Python, and add crash respawn (grpcsub/dispatcher.go:250-251).
- **Risks:** Builds on a TUIBBS surface its own code does not use. Whether Python grpcio accepts the host's content subtype is UNVERIFIED (grpcsub.go:227-236).
- **Licensing:** A separate process over gRPC might stay MIT; a legal reading, UNVERIFIED (notes-3).
- **R1 / B / C:** Adds nothing over (a); every release still needs a Go screen. **Write-back:** A unary call is a natural request/response shape, but the host has no audit or ACS wiring for plugin calls today. Verdict: REFUTED as a route (assumptions.md row 7).

### (c) PTY door

- **Fit:** Good in principle, absent in practice. A door would run the unchanged Python observer as a child process on a PTY inside the BBS session, so no rewrite. But `internal/doors/` holds only a README describing a planned "PTY door supervisor — S8 (v1.x heavy)" (internal/doors/README.md:3-5), and doors are a v1 non-goal (docs/scope.md:31).
- **Effort:** Low for IronClaude (none). Medium to high for TUIBBS: build the door supervisor, its ACS gate and menu entry.
- **Risks:** Depends on a TUIBBS feature the owner has scoped out of v1. The observer would run on the TUIBBS host and need Orca access there (same transport question as assumptions.md row 4, now for the live `worker-list` call). Rich output must survive the BBS's per-session colour and size handling; UNVERIFIED.
- **Licensing:** Strongest separation: a separate program on a PTY, MIT code never compiled into the AGPL binary. That it stays a separate work is still a legal reading, UNVERIFIED.
- **R1 / B / C:** Each release ships once in Python and appears in TUIBBS with no port. **Write-back:** Whatever the Python observer does, the door does; there is no BBS-side ACS or audit around the child's actions, so write-back through a door bypasses TUIBBS's gates. Not suitable for write-back.

### (d) Native Go port inside TUIBBS

- **Fit:** The only way to make a first-class TUIBBS screen today (assumptions.md rows 1, 5). Follows `internal/ailink`: compiled in, reached directly from `internal/serve` (internal/serve/spawn_handler_unix.go:91), ACS-gated fail-closed (lifecycle_overlay.go:27-44), inheriting per-session colour, NO_COLOR, WCAG themes and reduced motion (internal/session/caps.go:227-228).
- **Effort:** Highest if done instead of (a) for R1: Go in a different repository, Orca adapter re-implemented in Go, before the design has been proven. Moderate if done after (a) against a frozen snapshot: a read-only screen over a known schema.
- **Risks:** TUIBBS is a hobby, dogfood-only project with no successful release (docs/scope.md:17-18; assumptions.md row 15), so R1 would wait on another project's release process. No team concept exists for staff views (row 14).
- **Licensing:** AGPL-3.0-only for the Go screen, with the section 13 source offer to network users (README.md:60-77; row 9). Nothing from it may be copied back into MIT IronClaude.
- **R1:** Delays it; not recommended as the first form. **B / C:** Ported one at a time after each is proven in Python. **Write-back:** This is where write-back belongs later, because it gets TUIBBS's ACS, per-user identity and audit chain; see write-back-stage.md.

### (e) Other options found

- **(e1) Reuse the AI-session PTY spawn.** TUIBBS already runs an arbitrary command on a PTY for its AI sessions: the command line comes from the `TUIBBS_AI_SPAWN_COMMAND` environment variable, else a dogfood placeholder (internal/serve/spawn_handler_unix.go:354-358), run via `/bin/sh -lc` (:101) through direct `os/exec`, deliberately not the plugin runner (internal/session/spawn/spawn.go:12-20). Setting that variable to the Python observer would show it in the BBS with zero TUIBBS code, but it replaces the AI spawn host-wide and is gated by the `AI[claude]` rule, which is sysop-only. A second, separately gated spawn entry would be a small TUIBBS change. **Fit:** a cheap demo path, not a product path. **Licensing / write-back:** as option (c).
- **(e2) Message Base bridge.** Post snapshot summaries as BBS messages. Rejected: turns live state into stale posts and reopens the Mattermost principal-spoofing risk noted in notes-2 (translate.go:107-112).
- **(e3) Observer as a Go program outside TUIBBS.** Gains nothing: still not a plugin that can draw (row 7), and loses Python reuse.

## Comparison

| Option | Works with TUIBBS code today | IronClaude effort for R1 | TUIBBS effort | Licence separation | Write-back home |
|---|---|---|---|---|---|
| (a) Python + snapshot, Go screen later | Yes (later screen follows the lifecycle overlay precedent) | As planned plus snapshot export | One read-only screen, later | MIT and AGPL kept apart; data-only exchange is a legal reading | No; separate gated stage |
| (b) Python gRPC plugin | No (host unwired, plugins cannot draw) | High | High | Unclear | Unwired |
| (c) PTY door | No (doors not built, v1 non-goal) | None | Medium to high | Strongest | No (bypasses ACS and audit) |
| (d) Go port first | Yes | None in IronClaude; all in Go | Highest, on an unreleased base | AGPL only | Yes, with ACS, identity and audit |
| (e1) AI spawn reuse | Yes, as a sysop-only demo | None | None to small | As (c) | No |

## Recommendation

**Choose (a).** Build R1 Signal Bridge as the standalone Python + Rich observer in IronClaude, and make `export(view)` write a versioned JSON snapshot whose fields are frozen in release 1. If TUIBBS is later chosen, it gets a compiled-in, read-only Go screen (option d, AGPL, in the TUIBBS repository) that reads that snapshot; Attention Ledger and Decision Desk follow the same path one at a time.

Reasons:
1. Every TUIBBS screen is compiled-in Go and plugins cannot draw (assumptions.md rows 1, 6, 7), so no choice made in IronClaude now avoids a Go screen later; the cheapest thing R1 can do for TUIBBS is a stable data contract.
2. TUIBBS's own extension habit is exactly this: content-typed JSON across a boundary, frozen additive-only (internal/plugin/dispatch.go:53-62, :146-151).
3. It keeps MIT and AGPL code apart and copies nothing (rows 8, 9).
4. It does not make R1 wait on a hobby project with no successful release (row 15) or on the unbuilt door supervisor (option c).
5. Write-back stays out of the snapshot and out of R1; it lands later in the Go screen, where TUIBBS's ACS, user identity and audit chain exist (write-back-stage.md).

Keep (e1) in reserve as a sysop-only demo of the Python observer inside the BBS; it needs no code but replaces the AI spawn host-wide.

## Owner decisions this needs

1. Confirm Python + Rich for R1 (still only a recommendation; owner-decisions-20261108.md item 2).
2. Confirm the snapshot export is in R1 scope (one function and one schema file, plus a schema test).
3. Decide later, not for R1, whether TUIBBS is the staff platform; it currently has no team concept (row 14).
4. Get a licence opinion before any Go screen reads the MIT observer's output (row 10).

## Snapshot contract fields to freeze in release 1

Source names are the live `orca orchestration worker-list --json` keys, checked read-only on Orca 1.4.245 (2026-11-08). Rules: additive-only (new optional fields may appear; no field is removed, renamed or retyped without a new major `schemaVersion`); a value the source did not give is the string `UNKNOWN`, never a guess or an empty string; no message bodies, prompts, file contents or credentials in R1.

**Envelope (one per cycle)**

| Field | Meaning |
|---|---|
| `schemaVersion` | Contract version, `1` for release 1. Consumers reject an unknown major. |
| `producer` | Producer name and version, e.g. the observer package version. |
| `cycle` | The collector's monotonic cycle number (merged-requirements.md section 9). |
| `generatedAt` | When the snapshot was written (UTC, ISO 8601). |
| `source.namespace` | Which Orca the rows came from; part of row identity. |
| `source.status` | `OK`, `STALE` (older than 45 s), `ERROR` or `UNKNOWN`, with `source.observedAt` and a short `source.error` code (no raw stderr). |
| `page.hasMore`, `page.total`, `page.limit` | From `result.page`; `total` is optional upstream, so it may be `UNKNOWN`. |
| `scope` | From `result.scope`, optional upstream. |
| `counts` | From `result.counts`, passed through as a map of state to number. |

**Row (one per worker)**

| Field | Source key |
|---|---|
| `dispatchId` (row identity with `source.namespace`) | `dispatchId` |
| `taskId`, `runId` | `taskId`, `runId` |
| `workerState`, `dispatchStatus`, `terminalState` | same names |
| `role` | `projection.role` |
| `provider` | `projection.provider.id` |
| `hostKind`, `hostId` | `projection.host.kind`, `projection.host.id` |
| `stage.worker`, `stage.dispatch`, `stage.detail`, `stage.activity` | `projection.stage.*` |
| `outcome` | `projection.outcome` |
| `liveness.verdict`, `liveness.observedAt`, `liveness.source` | `projection.liveness.*` |
| `evidence.durable`, `evidence.liveStatus`, `evidence.lastObservedAt` | `projection.evidence.*` (note the `projection.` prefix; merged-requirements.md:328 omits it) |
| `nextAction` | `projection.nextAction.kind` |

Ordering: by `liveness.observedAt`, else `evidence.lastObservedAt`, newest first, ties by `dispatchId` (merged-requirements.md section 9).

Not frozen in R1 (left out deliberately): terminal handles (`agentTerminalHandle`, `resource.terminalHandle`), worktree and endpoint ids, ownership and release state. They identify resources an attacker could target and are not needed to display the ledger. Attention Ledger and Decision Desk add their own optional field groups later, additively.
