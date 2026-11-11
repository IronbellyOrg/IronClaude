# Extract: TUIBBS review + observer brainstorm (inputs for architecture)

Read-only extract, 2026-11-08. Base path `IC=/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev`.
Sources: `AO=$IC/issues/409/tuibbs-review/architecture-options.md` (111 lines), `SU=…/summary.md` (25), `AS=…/assumptions.md` (29), `MR=$IC/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md` (492; §7-9 = lines 212-356).
Evidence labels are copied as the source writes them.

## 1. Frozen snapshot contract (verbatim, AO:75-111)

The field list lives in one place only (AO:75-111). Copied verbatim; blank source lines omitted; left column is the source line number.

```text
75  ## Snapshot contract fields to freeze in release 1
77  Source names are the live `orca orchestration worker-list --json` keys, checked read-only on Orca 1.4.245 (2026-11-08). Rules: additive-only (new optional fields may appear; no field is removed, renamed or retyped without a new major `schemaVersion`); a value the source did not give is the string `UNKNOWN`, never a guess or an empty string; no message bodies, prompts, file contents or credentials in R1.
79  **Envelope (one per cycle)**
81  | Field | Meaning |
82  |---|---|
83  | `schemaVersion` | Contract version, `1` for release 1. Consumers reject an unknown major. |
84  | `producer` | Producer name and version, e.g. the observer package version. |
85  | `cycle` | The collector's monotonic cycle number (merged-requirements.md section 9). |
86  | `generatedAt` | When the snapshot was written (UTC, ISO 8601). |
87  | `source.namespace` | Which Orca the rows came from; part of row identity. |
88  | `source.status` | `OK`, `STALE` (older than 45 s), `ERROR` or `UNKNOWN`, with `source.observedAt` and a short `source.error` code (no raw stderr). |
89  | `page.hasMore`, `page.total`, `page.limit` | From `result.page`; `total` is optional upstream, so it may be `UNKNOWN`. |
90  | `scope` | From `result.scope`, optional upstream. |
91  | `counts` | From `result.counts`, passed through as a map of state to number. |
93  **Row (one per worker)**
95  | Field | Source key |
96  |---|---|
97  | `dispatchId` (row identity with `source.namespace`) | `dispatchId` |
98  | `taskId`, `runId` | `taskId`, `runId` |
99  | `workerState`, `dispatchStatus`, `terminalState` | same names |
100 | `role` | `projection.role` |
101 | `provider` | `projection.provider.id` |
102 | `hostKind`, `hostId` | `projection.host.kind`, `projection.host.id` |
103 | `stage.worker`, `stage.dispatch`, `stage.detail`, `stage.activity` | `projection.stage.*` |
104 | `outcome` | `projection.outcome` |
105 | `liveness.verdict`, `liveness.observedAt`, `liveness.source` | `projection.liveness.*` |
106 | `evidence.durable`, `evidence.liveStatus`, `evidence.lastObservedAt` | `projection.evidence.*` (note the `projection.` prefix; merged-requirements.md:328 omits it) |
107 | `nextAction` | `projection.nextAction.kind` |
109 Ordering: by `liveness.observedAt`, else `evidence.lastObservedAt`, newest first, ties by `dispatchId` (merged-requirements.md section 9).
111 Not frozen in R1 (left out deliberately): terminal handles (`agentTerminalHandle`, `resource.terminalHandle`), worktree and endpoint ids, ownership and release state. They identify resources an attacker could target and are not needed to display the ledger. Attention Ledger and Decision Desk add their own optional field groups later, additively.
```

Live shape (AS:28): `result` keys `counts, page, scope, warnings, workers`; `page` keys `hasMore, limit, nextCursor, total`. Observation (mine): `warnings` and `page.nextCursor` exist upstream but are absent from the frozen list (AO:79-107). AS:9 says the brainstorm defines only what the adapter parses, "not a versioned export schema; one is proposed in architecture-options.md". MR:220 says "the PROPOSED schema is used only inside fixture mode" (which schema is not named there).

## 2. Rules around the contract

- **Producer:** the Python observer's `export(view)` writes "a versioned JSON snapshot" (AO:10, AO:57); `export(view)` is also the lossless `e`/`--once` record form, carrying full IDs, no truncation (MR:291, MR:294).
- **Reader:** "a compiled-in, read-only Go screen (option d, AGPL, in the TUIBBS repository) that reads that snapshot" (AO:57); modelled on `internal/ailink/lifecycle_overlay.go:46-61` (SU:6; AO:9 "value snapshots in, string out"). New TUIBBS work: "a model, an ACS gate, a menu entry, a snapshot reader"; size UNVERIFIED (AO:10).
- **Version field:** `schemaVersion`, `1` for release 1; "Consumers reject an unknown major" (AO:83).
- **Compatibility:** additive-only; no remove/rename/retype without a new major `schemaVersion`; missing value = string `UNKNOWN` (AO:77). Matches TUIBBS habit, content-typed JSON frozen additive-only (`internal/plugin/dispatch.go:53-62`, `:146-151`; AO:61, AS:9 VALIDATED).
- **One-way:** "Write-back: Not in the snapshot. The snapshot is one-way by construction" (AO:13; SU:6).
- **Risk:** "The snapshot format becomes a second public contract to keep stable"; Python tests become the spec, not reusable code (AO:11).
- **Transport / file location:** not stated. Transport is UNVERIFIED (AS:10 row 4: TUIBBS exposes only SSH on 2222; pushing the file from Coder host "is the simplest route, but no joint deployment was examined"; AO:11 "unexamined"). No file path is given in any source.
- **Open (owner decisions):** confirm Python + Rich (AO:70); confirm snapshot export in R1 scope, "one function and one schema file, plus a schema test" (AO:71; SU:16); TUIBBS as staff platform later (AO:72); licence opinion before any Go screen reads the output (AO:73; SU:18).

## 3. TUIBBS constraints relevant to architecture

- **FR-X-13:** TUIBBS's own rule, quoted as "FR-X-13: no write-back" (`internal/serve/menu.go:637-640`; AS:17, SU:9). Row 11 VALIDATED: watch sink never writes to the child; `{control}` reserved, not built (AS:17). Owner write-back "needs a boundary change in both issue 409 and TUIBBS" (AS:17); "ask the TUIBBS owner to amend FR-X-13, before any build" (SU:17).
- **Licence:** TUIBBS is "AGPL-3.0-only with stock text and no additional terms or exceptions" (AS:14). A Go screen inside TUIBBS cannot be non-AGPL: REFUTED (AS:15 row 9; AO:36). JSON-only exchange keeps MIT/AGPL separate: UNVERIFIED, "a legal reading, not a code fact; no counsel or FSF text was checked" (AS:16 row 10; AO:12). Opinion still open (AO:73, SU:18).
- **No code copied:** VALIDATED, "The observer design copies nothing; this review copied no code into IronClaude" (AS:14 row 8). "TUIBBS-scp is AGPL, so no code is copied from it, whatever the stack" (MR:301). "Nothing from it may be copied back into MIT IronClaude" (AO:36).
- **Option chosen:** "**Choose (a).**" standalone Python + Rich observer + versioned snapshot; later read-only Go screen (AO:57). Rejected: (b) gRPC plugin REFUTED (AO:21), (c) PTY door v1 non-goal (AO:25), (d) first delays R1 (AO:37). (e1) AI-spawn reuse kept "in reserve as a sysop-only demo" (AO:66).
- **Why a Go screen is unavoidable:** "Every TUIBBS screen is compiled-in Go and plugins cannot draw" (AO:60; `proto/v1/plugin.proto:61-68`).

## 4. Assumptions (AS:5-21; counts AS:25, SU:8)

| # | Assumption | Verdict | Line |
|---|---|---|---|
| 1 | Python + Rich for R1 does not close off a TUIBBS future | VALIDATED | AS:7 |
| 2 | One view model + two pure renderers = small Go port surface | VALIDATED | AS:8 |
| 3 | Versioned JSON snapshot is a sound bridge (shape) | VALIDATED | AS:9 |
| 4 | TUIBBS host can obtain the snapshot (transport) | UNVERIFIED | AS:10 |
| 5 | Observer can become an in-tree TUIBBS feature (compiled-in Go) | VALIDATED | AS:11 |
| 6 | Drop-in separately shipped module without changing TUIBBS | REFUTED | AS:12 |
| 7 | Python out-of-process gRPC plugin can show the observer | REFUTED | AS:13 |
| 8 | No code copied, so IronClaude MIT unaffected | VALIDATED | AS:14 |
| 9 | Go screen inside TUIBBS can be non-AGPL | REFUTED | AS:15 |
| 10 | JSON-only exchange keeps MIT and AGPL separate | UNVERIFIED | AS:16 |
| 11 | Observer has no write path into Orca (read-only boundary) | VALIDATED | AS:17 |
| 12 | Charm v2 NO_COLOR handling needs overriding | VALIDATED | AS:18 |
| 13 | Charm v2 lacks cell-width truncation out of the box | UNVERIFIED | AS:19 |
| 14 | TUIBBS can host per-team staff views | REFUTED | AS:20 |
| 15 | TUIBBS is a stable base now | REFUTED | AS:21 |

Totals: 7 VALIDATED, 5 REFUTED, 3 UNVERIFIED (AS:25; SU:8). Correction: evidence timestamp is `projection.evidence.lastObservedAt` (SU:12; AS:28).

## 5. Brainstorm sections 7-9 (MR:212-356)

**Build order / gates (§7).**
- Every data gate needs recorded, redacted samples of four kinds, "**success**, **missing**, **stale** and **contradictory**", each pinned in a contract test; else the gate stays closed (MR:215).
- R0 offline only; fixtures labelled SYNTHETIC (MR:220). DIRECTION-SELECTED gate: "**This gate has NOT passed: no owner selection exists.**" (MR:221; status NOT passed MR:239). R1 = live `worker-list` with a contract test that "fails on any missing required field" (MR:222). R2 behind QUESTION-OBSERVATION (MR:223); R3 QUESTION-LINK (MR:224); R4 remote, "Not established" (MR:225).
- "Production integration" has two readings, both UNVERIFIED; until owner confirms, "the stricter reading applies: offline work only (R0)" (MR:244-249). Reading 1 = registering `superclaude observe` or running a live Orca subprocess outside the fake runner (MR:246).
- Candidate message verb `orca orchestration check --all --run <runId> --json`, "a candidate, never an available source" until proofs (a)-(c) (all UNVERIFIED), INV-022 non-consumption, question identity and owner inputs are recorded (MR:254-262).

**Stack (§8).**
- "Recommendation, pending owner confirmation: **Python + Rich** in this repository" (MR:270); departs from issue's Go/Bubble Tea v2 preference, so owner confirms (MR:270).
- Rich gap = keyboard: "a small stdlib reader, POSIX-only" (`termios`, `tty`, `select`), new code with its own tests (MR:276, MR:288).
- One view model, two renderers: `render(view, W)` (width-bounded) and `export(view)` (lossless record) (MR:291). Screen truncates by cells with one `>` marker; `--ascii`; export never truncates (MR:294).
- Placement: `click` subcommand in `cli/main.py`; recommended name `superclaude observe`, owner's choice (MR:297).
- **Key-reader spike / switch rule (quote, MR:298):** "**Switch rule:** the R0 spike tests Rich Live with the raw key reader. If the spike fails, switch to Textual. Never build both. Textual is not first because of its maintenance risk and its UNVERIFIED plain-text export." (also MR:220).

**Adapter (§9).**
- Scope: R0 nothing runs against Orca; R1 "one verb, `orca orchestration worker-list --json --limit 100` with optional `--run <runId>` and `--cursor <c>`" (MR:306).
- Structure: `observe` package; each call returns a `SourceResult` (ok, failed or partial); "A single-flight collector runs one cycle at a time and publishes each snapshot atomically, tagged with a monotonic cycle number"; seams = subprocess runner (fake in tests) and pure snapshot-to-view function (MR:309).
- Binary discovery: reuse `_find_orca()` (`cli/install_user_setup.py`), tries `orca-ide` then `orca`, validates with `skills list --json`, 10 s timeout; else `worker-list NOT AVAILABLE (orca binary not found)` (MR:312).
- **Allow-list (MR:315):** "The R1 template is `(orca, "orchestration", "worker-list", "--json", "--limit", "100")`, plus an optional `("--run", runId)` and an optional `("--cursor", value)`." `--include-remote` not allowed until R4; `subprocess.run` with a list, no shell.
- **Forbidden set (MR:316):** "prefix-matched, and it never shrinks: plain `check` (without `--peek`/`--all`), `--ack`, `--wait`, `--retry-request`, `dispatch`, `inbox`, and any other verb."
- Values: `runId` format check; cursor copied unchanged from `page.nextCursor`, byte-bounded; any value starting with `-` rejected; "V1's numeric bounds and regexes are PROPOSED, not verified Orca formats" (MR:317). No `--opt=value` form until recorded (MR:318). Fake runner fails on non-allow-listed argv (MR:319).
- **Bounds (MR:322):** interval 15 s, cycle budget = interval; max 5 subprocesses per cycle; 8 MiB output cap per call; overrun killed and reaped, strip shows `cycle overran (Ns)`; backoff up to 60 s; STALE after 3 intervals (45 s) on a local monotonic clock; cycles never overlap; daemon thread waiting on `threading.Event` (mirrors `sprint/monitor.py` `OutputMonitor`); no LLM in loop; earlier 30 s cycle deadline withdrawn.
- **Timeouts:** "The per-call timeout is measured in R0, not guessed; until then its value is UNVERIFIED" (MR:322). Only fixed timeout stated: 10 s for binary discovery (MR:312).
- Parsing: JSON only, one envelope per call; required `result`, `result.workers`, `result.page.hasMore`, else `FAILED (shape)` and last good snapshot kept; `result.scope` / `page.total` optional (open disagreement, V1 wants `page.total` required); missing key = `UNKNOWN` sentinel; extra keys counted (MR:325).
- Identity/order: namespace + `dispatchId`; newer `projection.liveness.observedAt` (or `evidence.lastObservedAt`) wins, else newer cycle + `order unknown`; backward time shows `conflict (time went back)` (MR:328).
- Errors: non-zero exit, timeout or invalid JSON = `FAILED`; last good snapshot shown `as of`; stderr sanitized, 2 KiB (MR:334). Own sanitizer strips CSI/OSC, C1, C0 (except newline in inspector), Unicode Cf; render as literal text, never Rich markup; truncate with `rich.cells.cell_len` (MR:337).
- Several observers: caps are per process, no singleton lock, label QUALIFY (V3: REJECT); owner decision 9 (MR:352).
