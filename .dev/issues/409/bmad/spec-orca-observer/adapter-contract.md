# Adapter contract (smallest trustworthy read-only adapter)

**Scope.** R0 runs nothing against Orca. R1 has one verb: `orca orchestration worker-list --json --limit 100`, with optional `--run <runId>` and `--cursor <c>`, plus the one-time binary discovery below (run once before the first cycle, at most one `skills list --json` probe per candidate, so at most two, and not among a cycle's 5 subprocesses). The one R2 message template (below, "Argv allow-list") is used only after the QUESTION-OBSERVATION gate record exists (`release-gates.md`; status: not passed as of 2026-11-11).

## Structure

- An `observe` package. Each call returns a `SourceResult` (ok, failed or partial, with parsed data and a sanitized diagnostic).
- A single-flight collector runs one cycle at a time and publishes each snapshot atomically, tagged with a monotonic cycle number, so snapshots are ordered without trusting wall clocks.
- Two seams: the collector seam (subprocess runner, replaced by a fake runner in tests) and the view seam (a pure function from snapshot to view model, `stack.md`).
- **Binary discovery:** reuse `_find_orca()` (`cli/install_user_setup.py`): tries `orca-ide`, then `orca`, running at most one `skills list --json` probe per candidate found on `PATH` (so at most two), 10 s timeout each, and accepts a candidate only if the probe exits 0 and lists the `orca-cli` topic. A bare `orca` may be the GNOME screen reader, so the probe can execute it once before rejecting it. `_find_orca()` calls `subprocess.run` itself, outside the collector's runner seam, so T1 and T36 intercept discovery by replacing `_find_orca()`'s `subprocess.run`, not through the fake runner. `_find_orca()` returns nothing both when no candidate exists and when every candidate fails validation, so the freshness cell reads `worker-list NOT AVAILABLE (no Orca CLI validated)`, never an empty fleet.

## Argv allow-list

- Argv is built from exact templates only. R1 template: `(orca, "orchestration", "worker-list", "--json", "--limit", "100")` plus optional `("--run", runId)` and optional `("--cursor", value)`. Discovery template (once per candidate, inside `_find_orca()`): `(<candidate binary>, "skills", "list", "--json")`. Calls use `subprocess.run` with a list, no shell.
- **R2 message template (one only, behind the gate record):** `(orca, "orchestration", "check", "--all", "--types", "question", "--run", runId, "--json")`, every item a separate argument, `runId` through the existing format check, used only after the gate record exists. The allow decision is made on the whole argv, not on the token `check`. `--peek` and an unfiltered `check --all` (without `--types question` or without `--run`) are not allowed in any argv.
- Following a cursor goes through a guard that marks the view PARTIAL when the per-cycle cap stops it.
- `--include-remote` is not in the allow-list until R4.
- **Forbidden set** (prefix-matched, never shrinks): plain `check`, `--ack`, `--wait`, `--retry-request`, `--peek`, `dispatch`, `inbox`, and the added `run-use`, `run-create`, `send`, `ask`, `reply`, `reset`, and any verb other than the templates above (worker-list, discovery, and the one R2 message template). `check` is allowed only as the verb of the exact R2 message template.
- **Values:** `runId` gets a format check. The cursor is copied unchanged from `page.nextCursor`, bounded by bytes, passed as its own argument, never checked against an inferred grammar. Any value starting with `-` is rejected. A cursor rejected by this guard (leading `-`, over the byte bound, or containing NUL) stops paging for the cycle, and the cycle shows `PARTIAL (cursor rejected, page k)` (T32). V1's numeric bounds and regexes are PROPOSED, not verified Orca formats.
- **Form:** flags and values are separate arguments; `--opt=value` only after Orca's parser support is recorded.
- **Test seam:** the fake runner fails the test on any argv not in the allow-list.

## Bounds per cycle

- Interval 15 s; cycle budget equals the interval; cycles never overlap.
- At most 5 subprocesses per cycle; each call's output capped at 8 MiB.
- An overrunning call is killed and reaped; the strip shows `cycle overran (Ns)`.
- After failures the interval backs off, up to 60 s.
- Per-call timeout is measured at the first permitted live read (R0 makes no Orca calls), not guessed; UNVERIFIED until then. T5 injects a configured timeout into the fake runner.
- STALE after 3 intervals (45 s) with no success, on a local monotonic clock.
- Message calls per cycle: exactly one (the R2 template), no paging. When questions are on, worker-list paging is limited to 4 calls, so the cycle total stays at most 5 (PROPOSED; one call is about 0.2 s on a probe Run, real traffic UNVERIFIED).
- The poll runs in a daemon thread waiting on a `threading.Event`, mirroring `sprint/monitor.py` `OutputMonitor`. No LLM in the loop. The earlier 30 s cycle deadline is withdrawn.

## Parsing

- JSON only, from stdout, exactly one envelope per call.
- Required: `result`, `result.workers`, `result.page.hasMore`. Any missing: the cycle is `FAILED (shape)` and the last good snapshot is kept. Type checks, not just presence: `result.workers` must be a JSON list and `result.page.hasMore` a JSON boolean (the string `"false"` fails), else `FAILED (shape)`; a JSON `null` counts as absent (T32).
- Optional: `result.scope` (absent: `scope unknown`) and `page.total` (absent: `reported unknown`). V1 dissents that `page.total` should be required (`owner-decisions-and-risks.md`).
- Rows are read field by field with absent-tolerant access; a missing key becomes `UNKNOWN`, a sentinel that is not `None`, 0 or `False`. Unknown extra keys are ignored and counted in the inspector (`n unrecognised keys`).

- **Message rows (R2):** `result.messages` is required and must be a JSON list, else the question source is `FAILED (shape)`. Rows are read field by field with the `UNKNOWN` sentinel; a row that is not an object is counted and skipped; a row whose `type` is not `question`, or whose `run_id` differs from the requested Run, is dropped and counted as `contradictory rows ignored`. `body`, `payload` and `to_handle` are not kept.
- **Error envelopes (R2):** `{ok:false, error:{code, message}}` is decoded whatever the exit status. `consumer_fenced` (exit status 1) maps to source code `consumer-fenced` and `no_active_terminal` to `no-active-terminal`. Either one fails the cycle for the question source only: the worker-list state is unchanged and the retained questions stay. Any other error code maps to `exit:<n>` or `json`.

## Identity, duplicates, order

- Row identity = source namespace + `dispatchId`; rows from two hosts or Runs never merge. Each component keeps its own clock.
- **Source namespace (observer-derived, PROPOSED; not an Orca field):** the resolved absolute path of the Orca CLI that `_find_orca()` validated. R1 reads one local source (no `--include-remote`), so the namespace is constant for an observer process; R4 must extend it with `projection.host.id` before remote rows are admitted. It is written to the snapshot as `source.namespace` (`snapshot-export-schema.md`); T39 uses two fake sources with different resolved paths.
- Deduplicated by identity within a cycle; each dropped duplicate counted (`k duplicate rows ignored`). A row whose `dispatchId` is absent or blank has no identity: it is never deduplicated, is flagged `identity unknown`, and is not counted as a duplicate.
- Across cycles the newer `projection.liveness.observedAt` (or `projection.evidence.lastObservedAt`) wins. Either timestamp absent: the newer cycle wins and the row is flagged `order unknown`. A backward timestamp shows `conflict (time went back)`. Only like fields are compared (`liveness.observedAt` with `liveness.observedAt`, `evidence.lastObservedAt` with `evidence.lastObservedAt`); if the two cycles carry no common timestamp field the newer cycle wins and the row is flagged `order unknown`. An unparsable timestamp counts as absent and flags `order unknown`. On equal timestamps the newer cycle wins.
- Questions use only a verified source-scoped question identity, never a worker `dispatchId`.

## Paging, errors, sanitizing

- **Paging integrity:** the cursor is opaque, never built by hand. `page.total` changing between pages: `reported T1-T2 (changed during read)`. An empty page while T is above 0: `PARTIAL (empty page k)`. `page.hasMore` true with `page.nextCursor` absent, empty or equal to a cursor already used in this traversal: paging stops and the cycle shows `PARTIAL (cursor missing or not advancing, page k)` (T32).
- **Errors:** a non-zero exit, a timeout, invalid JSON or an `OSError` when spawning the process (`FAILED (spawn error)`) marks the source `FAILED` for that cycle; the last good snapshot stays, qualified `as of`. Stderr is sanitized and kept to 2 KiB for the inspector.
- **Sanitizer (trust boundary, the observer's own):** every source string passes it before reaching the model. Removes CSI/OSC sequences (terminated and unterminated), 8-bit C1 controls, bare C0 controls except newline in the inspector, and Unicode Cf format characters. At least as strict as the prototype `canvas.py` `sanitize` (reference only); `pty_stream.py` `ANSI_ESCAPE_RE` is too weak. Strings render as literal text, never Rich markup. Truncation uses `rich.cells.cell_len`, never `len()`.

## R2 onward

- **Question retention:** kept until closure evidence is seen; bounded at 1,000 records; eviction never lowers the open total; beyond the bound the count reads `unknown (retention exceeded)` with the retained count; overflow never shown as closed; oldest first. Retention is keyed by Run plus `message.id`. A question absent from a later successful read is marked `no longer in source window` and never closed. A read of exactly 100 rows is flagged `window full` (the source gives no total or truncation field).
- **One named Run, no rotation:** R2 reads one named Run only. The observer never binds to a Run (it never runs `run-use`); it must run where it already holds the Run, because a caller bound to another Run is fenced (`consumer_fenced`) and a caller with no terminal identity gets `no_active_terminal`. The rotation set and the `revisit ~Ns` token are removed. For messages the header reads `one Run only` plus the named Run; `read k of N Runs since start` is not a message-source behaviour.
- **Acquisition permission (INV-017):** decision 6 is granted for one named Run (OWNER, `owner-decisions-20261111.md`, 2026-11-11: one named Run, `--types question`, never `run-use`), and the Run must be named before the first call (the owner has not named it yet; no message call is made until then). Permission must cover the actual read scope before a message call, separately from display and export permission. Dropping a body at parse time cannot undo its receipt, so the design never claims bodies were not acquired, only that they are not kept or shown; if a narrow read cannot honour the permission the call is skipped. Raw output never enters logs, fixtures or exports. Run-wide consent is not substituted for terminal consent while terminal-attribution fields are UNVERIFIED.

## Accepted risks and scope honesty

- **INV-007 (accepted risk):** rows seen this session that drop out stay listed as `not reobserved`; the strip discloses `oldest rows not read; long-running active workers may be among them`. Whether `worker-list` has a state filter is UNVERIFIED.
- **A-008 (QUALIFY; V3 dissent REJECT):** caps are per observer process, and help and the inspector say so. No singleton lock, so several observers multiply load on Orca. Any restriction is open owner decision 9.
- **Scope honesty:** `result.scope.source` (`flag`, `bound` or `all`, per help) is shown in the header; absent reads `scope unknown`; `bound` adds `one Run only`. With R2 questions on, the header reads `one Run only` plus the named Run and carries no `read k of N Runs since start` for messages, because there is no rotation set (the placement of that token for worker reads stays an open question in `SPEC.md`).
