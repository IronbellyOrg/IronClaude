# Variant 2 (analyzer): B. Attention Ledger as the MVP for the Orca read-only observer (#409)

## 1. Summary

1. Root cause of #409: a human question gets lost because chat is ordered by recency and because reading a message is treated as handling it. Only B makes that failure mode its primary object: questions oldest first, and "seen is not resolved".
2. All three directions put a human-question panel at their centre, and all three depend on the same UNVERIFIED message row contract. They differ in how they degrade without it. B shows the gap as its headline. A falls back to a fleet slice that looks complete. C has nothing to select.
3. Recommendation: B as the screen, plus A's source-freshness strip as its header. Release 0 is offline fixture replay. Release 1 is live on `worker-list` only. The live question list is gated on verifying `check --all` row fields.
4. Until that gate passes, the live ledger shows "Human questions: source contract unverified, 0 rows interpreted". Below it, in a separately labelled panel, it shows raw worker-reported `projection.nextAction.kind` values. These are never called questions, and they are ranked by oldest observation, not by question age.
5. Stack: Python Rich (already a dependency, MIT) inside this repo, with a small stdlib key reader. Go Charm v2 stays possible later, because the renderer is a pure function from model to lines.

### Evidence chain behind the recommendation

- `check --help` (read 2026-11-08): `--peek` returns "only unread messages". When a coordinator runs plain `check` and then `--ack`, those messages stop being unread, so they leave the peek view even if the human never answered. A panel built on `--peek` would therefore resolve questions when they are read. That is exactly the defect #409 describes. The only non-consuming verb that keeps read rows is `--all` ("every message for the handle; does not mark read"), and it is capped at 100 rows.
- Conclusion: an honest question view has to keep, in the observer, every question it has observed until explicit closure evidence appears. That is B's "RETAIN CONTEXT" design (`layouts/agent_focus.py` `attention`: original question, original age, acting owner, requesting orchestrator, affected stable IDs, source coverage, explicit closure evidence). A and C do not specify retention. They render the current row set.
- No verified source records explicit closure today. So every retained question stays "open, closure source unavailable". It is never shown as resolved, and it is never quietly dropped.

## 2. First buildable slice

The slice is one screen (the Ledger), one detail inspector and a text export, in two data modes. `fixture` mode reads the package's synthetic fixtures. `live` mode reads `worker-list` only. Panel geometry follows the built `attention` layout. At 116 columns or more it draws the full frame, with `right = width - 43`. Below 116 it falls back to `narrow()`.

### Common to every width

- **Header line 1:** `ORCA OBSERVER  mode=fixture|live  scope=<result.scope.source>  as of <local time of last good poll>`. In fixture mode this always reads `SYNTHETIC FIXTURE <variant>, not Orca data`.
- **Header line 2, the freshness strip (taken from A):** one cell per source, `worker-list OK 4s` / `STALE 52s` / `FAILED (exit 2) 1m` / `NOT POLLED`. A second cell, `messages UNVERIFIED (not read)`, stays in the strip until Release 2.
- **Footer:** `j/k move  Enter detail  Esc back  m mark looked  e export  q quit`, plus `shown x/y | fetched y of page.total z`.
- **Selection** is keyed by a stable ID: `dispatchId` for proxy rows, the source message ID for questions from Release 2. It is never keyed by row index. A refresh that reorders rows keeps the cursor on the same ID. If that ID disappears, the cursor moves to the next row, and the status line reports `selected <id> no longer in source window`.
- **Detail inspector (Enter)** shows every field untruncated, wrapped by cells: `dispatchId`, `taskId`, `runId`, `resource.worktreeId`, `resource.ownerDispatchId`, `resource.originDispatchId`, `projection.host.id`, `projection.workspace.id`. Each absent field reads `unknown (absent in source)`.

### 160 columns

- **Left, `OPEN HUMAN QUESTIONS`** (x=1, width 114). In fixture mode it lists one block per question: `NN MIN`, the question, `requester requests / owner`, and `Affected: id, id`, oldest first. In live mode (Release 1) it shows one fixed block: `Question rows: source contract UNVERIFIED. 0 rows interpreted. This is not "no questions".`
- **Left lower, `WORKER-REPORTED NEXT ACTIONS (not questions)`** (live mode only). One line per worker whose `projection.nextAction.kind` is present: `<kind>  <dispatchId>  stage=<stage.worker>/<stage.dispatch>  liveness=<verdict> (<liveness.source>)  last observed <evidence.lastObservedAt>`. Rows are ranked oldest `lastObservedAt` first, and the panel title says `ranked by oldest observation, NOT question age`. A row whose timestamp is absent goes into a final `observation time unknown` group. Its age is never shown as 0.
- **Right top, `SEEN IS NOT RESOLVED`** (x=117, width 42). It shows a big count of observed open items. A sub-line breaks it down as `marked looked: a | not marked: b | closed by evidence: unavailable`.
- **Right lower, `RETAIN CONTEXT`.** The seven retained attributes from the built layout. In live mode each one carries its availability: `original question: UNVERIFIED source`, `acting owner: resource.ownerDispatchId (worker-list)`, `explicit closure evidence: no source`.

### 116 columns

The structure is the same, with `right = 73`. The question panel is 70 columns wide and the right column stays 42. The proxy panel shows `<kind> <dispatchId> <liveness.verdict> <age>` and moves `stage` into the detail inspector.

### 80 columns

`narrow()` produces a single column: the header, the freshness strip, the `SEEN IS NOT RESOLVED n` line, the question lines (fixture) or the UNVERIFIED notice (live), then the proxy list. Each list line holds `kind`, a dispatch ID truncated by cell width with a trailing `~`, and an age. The two built invariant lines stay: "Questions stay until explicit resolution." and "No reply observed is not delivery failure." RETAIN CONTEXT is reachable only through the inspector.

### "Changes since last look"

`m` records an observer-local snapshot, held in memory for this process only. Every row added, removed, or changed in `stage`, `nextAction.kind` or `liveness.verdict` since that snapshot shows a `*` and appears in a `changed since HH:MM (k)` count. Marking a look never changes the open count. That is the "seen is not resolved" rule made mechanical.

## 3. Verified sources needed

The MVP (Release 0 and Release 1) needs exactly one live source. Everything else stays fixture-only or is labelled UNVERIFIED.

| Need | Verb | Fields used (verified in the seed brief, 2026-11-08) |
|---|---|---|
| Worker rows | `orca orchestration worker-list --json --limit 100` | `result.workers[].dispatchId, taskId, runId, workerState, dispatchStatus, terminalState` |
| Ownership and worktree (shown verbatim, never joined across hosts) | same | `resource.{id, ownershipState, releaseState, worktreeId, ownerDispatchId, originDispatchId, recoveryAttemptCount}` |
| Attention proxy | same | `projection.nextAction.kind`, `projection.stage.{worker,dispatch,activity,detail}` |
| Freshness and liveness | same | `projection.liveness.{verdict,source,observedAt}`, `projection.evidence.{durable,liveStatus,lastObservedAt}` |
| Outcome, kept separate from lifecycle | same | `projection.outcome` (shown raw; never merged with `workerState` or `terminalState`) |
| Placement | same | `projection.host.{id,kind}`, `projection.workspace.{id,kind}`, `projection.provider.id`, `projection.role` |
| Paging and denominators | same, with `--cursor <page.nextCursor>` | `result.page.{limit,total,hasMore,nextCursor}`, `result.counts.{active,reclaimable,retained,released}`, `result.scope.source`, `result.warnings[]` |
| Binary | existing `_find_orca()` in `cli/install_user_setup.py` | validated through `skills list --json` |

Verbs and flags read from `--help` today (flags only, no new fields): `worker-list` accepts `--run`, `--terminal-state`, `--include-remote`, `--cursor`, `--limit <1-100>`. Its help says rows are "newest first", and that without `--run` the scope is the bound Run, or every Run when nothing is bound, as reported in `scope.source`. `check` accepts `--peek`, `--all`, `--types`, `--run`, `--terminal`. `inbox` accepts `--limit`, `--terminal`, `--full`.

Mappings that are **UNVERIFIED** and must be shown that way:

- The value set of `projection.nextAction.kind`, and whether any value means "a human must answer". The MVP shows the raw string and never classifies it.
- Whether `projection.stage.activity` or `.detail` carries question text. The MVP shows these only in the inspector, sanitized and labelled `worker-reported`.
- The meaning of `projection.evidence.durable` beyond its presence. It is shown raw.
- Whether `page.total` counts historical dispatches. The live warning example "Showing 2 of 287 Dispatches" suggests it does, which is not proven. The MVP labels it `page.total (source)` and does not call it "workers".

Not used in the MVP: `check --peek`, `check --all`, `inbox`. Their row fields are UNVERIFIED (seed brief: only an empty peek, `result.{count,dispatchId,runId}`, was observed), and parsing an unknown shape into "questions" would invent a contract.

## 4. Shown as unknown / stale / partial

Rendering rules. Each is pinned by a test in section 10.

- **Absent field:** shows the literal `unknown`, in muted style. Under NO_COLOR it reads `unknown` with no colour. It is never `0`, `false`, `-` or blank. A counter that includes any unknown member is written `n+? (k unknown)`, never as a clean `n`.
- **Lifecycle vs outcome vs report vs acceptance vs tests vs approval:** these are separate columns or inspector lines. `workerState`, `dispatchStatus`, `terminalState` and `projection.outcome` are shown as separate raw values. Report status, acceptance, tests and human approval have no verified source, so every one of them reads `no source`. A `terminalState=released` row is never shown as "done". Help text: "a completed Task can still own a live terminal".
- **Stale:** the source is stale when the last successful poll is older than 3x the poll interval. The freshness cell then reads `STALE <age>`, and every value keeps its last-known reading with a qualifier `as of HH:MM:SS`. Source loss never closes a question, never changes the open count and never turns any value into `failed`. A failed poll shows `FAILED (<exit code or timeout>) <age>`, and stderr is shown sanitized in the inspector.
- **Partial pages:** when `page.hasMore` is still true at the page cap, the footer reads `PARTIAL: fetched 300 of page.total 412 (newest first; oldest 112 not read)`. Every derived count then states its denominator, for example `nextAction present: 17 of 300 fetched (412 in source)`.
- **Filtered vs global counts:** a filter (for example `--terminal-state active`, or a local text filter) always shows `filter <expr>: k of n fetched`, next to the unfiltered `result.counts` line, `source counts: active a / reclaimable r / retained t / released l`. Those source counts are a different scope (terminal accounting), and they are never summed into "workers".
- **The 100-row cap.** It is disclosed in two places. (a) `worker-list` returns at most 100 rows per page, and the observer follows `nextCursor` up to the page cap. (b) From Release 2, `check --all` and a Run `--peek` "show at most 100 rows" (help). The question panel title will then read `latest <=100 message rows per Run observed; older history not available`. When a retained question drops out of that window, it stays open with `no longer in source window (last seen HH:MM)`.
- **"Seen is not resolved":** the big count in `SEEN IS NOT RESOLVED` is the number of observed open items. `m` (mark looked) moves an item from `not marked` to `marked looked`, and the big count stays the same. `closed by evidence` shows `unavailable` until a closure source exists (Release 3). No key, timer or source loss can lower the open count. Only explicit closure evidence can, and that is not available in the MVP.
- **Empty states:** `0 rows interpreted (contract UNVERIFIED)` is not `no questions`. `worker-list returned 0 workers in scope=bound` names the scope, because a bound Run is not the fleet. The fixture variant `empty` must render `no observed items in this source window; not proof none exist`.
- **Cost and tokens:** these are not shown. The header reads `cost: no source`. No progress bar is derived from tokens or from activity.
- **Policy-frozen:** there is no verified field for it in `worker-list`. In fixture mode a frozen item keeps a `FROZEN` marker that no other state overrides. In live mode the word does not appear, because there is no source for it.

## 5. Deliberately left out

| Left out | Why |
|---|---|
| Any operational control (approve, retry, terminate, spawn, merge, rebase, delete-worktree, worker instruction, reply) | Constraint. The observer has no write path into Orca. |
| `check` without `--peek`/`--all`, `--ack`, `--wait`, `--retry-request` | Plain `check` and `--ack` consume a delivery. `--wait` returns the bound Run's FIFO delivery and is a listener, not an observation. |
| Parsing `check --peek/--all` or `inbox --json` rows in the MVP | Row fields are UNVERIFIED. This is the gate for Release 2. |
| Question age, requester and owner in live mode | They exist only in message rows. `lastObservedAt` is an observation time, not a question open time. |
| Affected-session evidence ledger (C's core) | It needs authoritative joins from question to dispatch to worktree. Cross-host joins are not established. |
| Fleet SIGNALS bars (A's 160-column panel) | Its running/settled/unknown/stale/frozen buckets need a verified mapping from `workerState`/`outcome` to "settled", and there is none. Raw `result.counts` are shown instead. |
| `--include-remote` | Remote rows have no verified cross-host ownership join. Merging them would invent fleet totals. Off by default (owner decision 8). |
| Persisted "last look" across runs | It is local state with no agreed retention or location. Session memory only (owner decision 9). |
| Cost/usage, admission, revision-pinned verification, durable replay, deep links | Not established (seed brief, `integration-gaps.md`). |
| Windows keyboard input | The stdlib `termios`/`tty` reader is POSIX-only. On Windows, `--once` prints a text export. |
| Mouse, themes, blinking, animation | Out of scope. No blinking is a constraint. |

## 6. Where A (Signal Bridge) and C (Decision Desk) are stronger

**A is stronger on day-one live data.** Every A panel except the request panel can be filled from `worker-list` today: the freshness strip, the session ledger, and the 80-column `RUN n SETTLED n UNKNOWN n STALE n` line, provided "settled" is defined. The live Release 1 B screen is mostly an honest notice plus a proxy list. A user opening it before Release 2 sees less than A would show. A also answers "is the fleet alive?" at a glance, which B does not try to answer. That is why this proposal borrows A's freshness strip outright.
- Weakness of A on the root cause: it puts one request on top (`_request` in `signal_bridge`). With 5-10 orchestrators, many questions are open at once, so the single-panel slot repeats the recency bias #409 complains about. Its 116- and 80-column builds also drop the SIGNALS panel (seed brief discrepancy), so its intended design is not even pinned.

**C is stronger once one question has been chosen.** C answers "who is affected, and what is the evidence?" for one request, filtering the ledger to the affected IDs only. It also ships the most honest overflow line of the three: `x/y other questions shown`. B needs that same arithmetic, and this proposal copies it. When the human is about to decide, C is the better screen.
- Weakness of C for an MVP: it needs both unverified contracts at once, message rows and an authoritative mapping from affected ID to dispatch. If either is missing, the desk is empty or shows wrong sessions. It also selects `requests[0]` by default, so the question shown first depends on source order, which is UNVERIFIED (out-of-order events).

**B's own weakness, stated plainly:** if the message contract never verifies, B's headline panel stays empty forever, and the product turns into A with different labels. Release 2's gate (section 7) is therefore the single most important owner action. If the owner cannot get that row shape verified, A becomes the better MVP, and this proposal says so.

## 7. Build order from MVP to later releases

Each release ships only after its named source contract is verified by a recorded, redacted sample pinned in a contract test.

| Release | Adds | Gate (the source contract that must be verified) |
|---|---|---|
| R0 Fixture replay | Ledger screen, inspector, text export at 160/116/80, sanitizer, cell-width truncation, NO_COLOR, stable selection, every fixture variant | None from Orca. Fixtures are labelled SYNTHETIC, and the PROPOSED schema is used only inside fixture mode. |
| R1 Live worker-list | Freshness strip, proxy panel, `result.counts`, paging with a cap, stale handling, "changes since last look" | `worker-list --json` fields and paging. Already verified (seed brief). Add a redacted golden sample and a contract test that fails on any missing top-level key. |
| R2 Live question ledger | `OPEN HUMAN QUESTIONS` from `check --all --run <runId> --json`, for each Run seen in worker-list, with observer-side retention and the 100-row disclosure | A non-empty `check --all --json` row, captured and verified, showing: a stable message ID, message type, sender, recipient, creation time, body. The owner must also name what identifies a human question (for example a `--types` value; `escalation` appears in help as an example, and its meaning is UNVERIFIED), and confirm that `--run <id>` works from an unbound observer terminal. |
| R3 Closure evidence | `closed by evidence` count, closed items move to a closed list | A source that records explicit resolution of a question (for example a reply row linked to the question ID). Not established. |
| R4 Decision inspector (C's strength) | For the selected question, the affected sessions with their worker-list evidence | An authoritative mapping from the IDs in a message to `dispatchId`/`worktreeId`, verified on this host first. |
| R5 Remote fleet | `--include-remote` rows grouped by `projection.host.id` | Cross-host ownership joins. Not established. |
| R6 History | Questions older than the 100-row window | Durable, non-consuming message history or event replay. Not established. |
| Later | Admission and verification, cost, deep links | Each needs its own feed, none established. |

Fallback rule: if R2's gate fails after an owner-set deadline, swap the default screen to A (Signal Bridge) built on the same adapter and renderer. B's retention model stays in the code for when the contract arrives. That costs one layout function, not a rewrite.

## 8. Stack recommendation

Recommendation: **Python + Rich**, as a `superclaude` subcommand in this repository. The comparison uses the seed brief's stack table (2026-11-08, primary sources, nothing run).

| Criterion | Go Bubble Tea v2 / Lip Gloss v2 / Bubbles v2 | Python Rich 15 (installed) | Textual 8.2.8 | Ratatui 0.30.2 |
|---|---|---|---|---|
| License | MIT | MIT | MIT | MIT |
| Toolchain added | Go toolchain plus a per-platform binary release pipeline | None | One pure-Python dependency | Rust toolchain plus maturin or a binary |
| Keyboard and focus | Strong, built in | None. Needs a hand-written POSIX key reader (`termios`, `tty`, `select`; stdlib) | Built in | Strong |
| Text export (required) | Not built in | `Console(record=True)` + `export_text()`, best of the four | UNVERIFIED | Plain-text snapshots |
| NO_COLOR | Parsed as boolean (`NO_COLOR=yes` ignored, contrary to no-color.org). Needs our own check | Must be handled explicitly (no house TUI does it today) | UNVERIFIED | UNVERIFIED |
| Cell width | Wide-char width UNVERIFIED | `rich.cells.cell_len` available | Via Rich | Built in |
| Headless tests | teatest/v2 untagged under `x/exp` | Fixed-width `Console(width=W)`, no TTY | `run_test(size=...)` | Snapshots |
| Maintenance | Low risk, monthly releases | Medium, same maintainer, very widely used | Medium. Company wound down May 2025; community-maintained | Low-medium, pre-1.0 |
| Fit with this repo | Second language, separate CI and release; cannot ship via `pipx install` | House pattern (`sprint/tui.py` `Live(...)`, `_render() -> Panel`); `click` registration in `cli/main.py` | New dependency to vet | Third language |

Reasoning:

- The two hardest MVP requirements are text export and cell-width truncation, and both are tested headlessly. Rich already does both. Go Charm v2 does neither out of the box, and its NO_COLOR parsing breaks the no-color.org rule, so we would have to override it anyway.
- Rich's one real gap is keyboard input: a small stdlib reader, POSIX-only, needed for j/k/Enter/Esc/m/e/q. That reader is new non-trivial code and gets its own tests. It costs less than a new language toolchain and binary pipeline.
- The issue prefers Go. That preference is satisfied best by keeping the renderer a pure function, `(model, width, color) -> list[str]`, with the adapter separate. A later Go port then re-implements a small, test-pinned surface. It does not need to rediscover behaviour. Textual is the fallback if the hand key reader proves fragile. Its maintenance risk is the reason it is not first.
- TUIBBS-scp (AGPL): no code is copied, whatever the stack. The design package's `canvas.py` `sanitize` sits in this MIT repository, and its logic may be reused once its provenance is confirmed. I did not re-check that it was written for this repository.

## 9. Smallest trustworthy read-only adapter

**Scope:** one verb. `orca orchestration worker-list --json --limit 100 [--cursor <c>]`. Nothing else is executed against Orca in R0 or R1.

- **Binary discovery:** reuse `_find_orca()` (`cli/install_user_setup.py`). It tries `orca-ide`, then `orca`, and validates with `skills list --json` so that the GNOME screen reader named `orca` is rejected, with a 10 s timeout. If no binary is found, the freshness cell reads `worker-list NOT AVAILABLE (orca binary not found)`. That is not shown as an empty fleet.
- **Argv allowlist:** the adapter builds argv from a fixed tuple, `(orca, "orchestration", "worker-list", "--json", "--limit", "100")`, plus an optional `("--cursor", value)`. The value is copied unchanged from `page.nextCursor`, as the help requires. Calls go through `subprocess.run` with a list and no shell. One test asserts that no argv ever contains `check`, `--ack`, `--wait`, `dispatch`, `inbox` or any other verb.
- **Bounds per poll cycle:** at most 3 pages (300 rows), a 10 s timeout per call, a 30 s deadline for the cycle, and an interval of 15 s (minimum 5 s, set by flag). Cycles never overlap: the next one starts only after the previous one finishes or hits its deadline. The poll runs in a daemon thread and waits on a `threading.Event`, mirroring `sprint/monitor.py` `OutputMonitor`. There is no LLM in the loop.
- **Parsing:** JSON only, from stdout. Each row is read field by field with absent-tolerant access, and a missing key becomes `UNKNOWN`, a sentinel that is not `None`, 0 or `False`. Top-level keys `result.workers`, `result.page` and `result.scope` are required. If any is missing, the cycle counts as `FAILED (shape)` and the last good snapshot is kept. Unknown extra keys are ignored and counted in the inspector (`n unrecognised keys`).
- **Duplicates and order:** rows are deduplicated by `dispatchId` within a cycle. Across cycles, the row with the newer `projection.liveness.observedAt` (or `evidence.lastObservedAt`) wins. If either timestamp is absent, the newer cycle wins, and the row is flagged `order unknown`. Each dropped duplicate is counted (`k duplicate rows ignored`).
- **Paging integrity:** if `page.total` changes between pages of one cycle, the cycle is marked `PARTIAL (total changed during read)`. The cursor is opaque and never built by hand.
- **Error and stale handling:** a non-zero exit, a timeout or invalid JSON marks the source `FAILED` for that cycle. The last good snapshot stays on screen, qualified `as of`. After 3 missed intervals the source shows `STALE`. Stderr is sanitized and kept to 2 KiB for the inspector.
- **Sanitizing at the trust boundary:** every string from the source passes the sanitizer before it reaches the model. The sanitizer removes CSI/OSC sequences (terminated and unterminated), 8-bit C1 controls, bare C0 controls except newline in the inspector, and Unicode Cf format characters. It is at least as strict as `canvas.py` `sanitize`; `pty_stream.py` `ANSI_ESCAPE_RE` is too weak, per the seed brief. Truncation uses `rich.cells.cell_len`, never `len()`.
- **Scope honesty:** `result.scope.source` (`flag`, `bound` or `all`, per help) is shown in the header. If the value is `bound`, the header adds `one Run only`.

## 10. MVP acceptance tests

The acceptance criteria below (AC-1 to AC-10) are restated from the seed brief's Problem, Constraints and Success Criteria. I did not re-read the issue text, so the merge step should check this mapping against #409.

Harness: render with `Console(width=W, record=True, color_system=None or "standard")` and read `export_text()`. The adapter runs against a fake runner that returns recorded JSON. No TTY and no live Orca are needed. Fixture variants are the package's: `base`, `uneven`, `shared-unmapped`, `historical`, `long-identifiers`, `source-loss`, `missing-fields`, `duplicate-out-of-order`, `empty`, `injection`.

| AC | Requirement | Tests |
|---|---|---|
| AC-1 | Read-only, no consuming check | T1: argv allowlist. Across every adapter code path, argv equals the fixed tuple plus an optional cursor. T2: a static test that the strings `--ack`, `"check"` and `--wait` do not appear in the adapter module. T3: no key binding maps to an Orca call. |
| AC-2 | Deterministic, bounded collection | T4: with a fake that always says `hasMore=true`, a cycle stops after 3 pages and renders `PARTIAL: fetched 300 of page.total N`. T5: a fake that sleeps past 10 s shows `FAILED (timeout)`, and the cycle ends within 30 s. T6: the same input renders byte-identical text twice. |
| AC-3 | Attention items with reasons, scope, changes since last look, evidence | T7: `base` (8 orchestrators, 80 sessions) in fixture mode lists every question oldest first with requester/owner and affected IDs. T8: after `m`, a fixture step that changes one `nextAction.kind` marks exactly that row `*`, and `changed since (1)` appears. T9: in live mode with no message source, the panel shows `0 rows interpreted (contract UNVERIFIED)`, and the word "questions" never labels the proxy panel. |
| AC-4 | Seen is not resolved | T10: pressing `m` on every item leaves the big open count unchanged. T11: the `source-loss` variant keeps the open count and every retained item. Nothing becomes resolved or failed. T12: an item missing from the next cycle stays, marked `no longer in source window`. |
| AC-5 | Lifecycle, outcome, report, acceptance, tests and approval kept separate; unknown is never 0 or false | T13: `missing-fields` renders `unknown` for every absent field, and the strings `0` and `false` never stand in for one (asserted per field). T14: a row with `terminalState=released` and `outcome` absent never renders `done`, `complete` or `settled`. T15: report, acceptance, tests and approval each render `no source` in live mode. |
| AC-6 | Filtered and global counts with denominators; the 100-row cap disclosed | T16: the scenario matrix {5, 8, 10 orchestrators} x {50, 80, 100 sessions} x {160, 116, 80 columns} (27 renders). Every count line matches `k of n`, and every hidden overflow shows `x/y shown`, with y equal to the fixture total. T17: `uneven` (one orchestrator owns most sessions) keeps per-owner counts that sum to the global count. T18: a fake with `page.total=287` and 100 rows shows `fetched 100 of page.total 287`, never `287 workers`. T19 (R2 placeholder, skipped until the gate): the question panel title contains `<=100`. |
| AC-7 | No one-to-one session/worktree assumption | T20: `shared-unmapped` shows two sessions sharing one `worktreeId` as two rows that each name the worktree, and a session with no worktree as `worktree unknown`. No count divides one by the other. |
| AC-8 | Historical records, duplicates, out-of-order events | T21: `historical` rows (released or retained) are listed with their `terminalState` and are not counted as active. T22: `duplicate-out-of-order` shows `k duplicate rows ignored`, and an older `observedAt` never overwrites a newer one. A row missing both timestamps is flagged `order unknown`. |
| AC-9 | Widths, keyboard, NO_COLOR, export, full IDs, no blinking | T23: at 160, 116 and 80 columns, every exported line has `cell_len <= W`. T24: `long-identifiers` truncates with `~` in lists, while the inspector shows the full ID. T25: a reorder between cycles keeps the selection on the same `dispatchId`. T26: `NO_COLOR=1` and `NO_COLOR=yes` both produce output with no SGR colour codes, and the meaning is still readable (`STALE` and `unknown` are words, not colours). T27: `e`/`--once` writes plain ASCII-safe text and contains no ESC byte. T28: the blink attribute (SGR 5/6) never appears. |
| AC-10 | Sanitize untrusted text; cell-width truncation | T29: `injection` (CSI, OSC 8 hyperlink, unterminated OSC, 8-bit C1 `\x9b`, BEL, a bidi Cf character such as U+202E, and a terminal title set) leaves no ESC, C1 or Cf byte in the rendered or exported output. T30: CJK and emoji identifiers are truncated by cells, so no line overflows and no double-width character is split. T31: cost renders `no source`, and no progress value comes from tokens or activity. |
| Contract | Shape of the worker-list source | T32: the redacted golden `worker-list --json` sample parses. Removing `result.page` produces `FAILED (shape)` with the last good snapshot kept. Removing an inner `projection.*` field produces `unknown`, not an error. |

## 11. Open owner decisions

Only decisions the human must make. Each has a recommendation.

1. **Visual direction (required by the issue before production integration).** Recommend B (Attention Ledger), with A's freshness strip as the header and C's `x/y shown` overflow line.
2. **Production stack.** Recommend Python + Rich in this repository, with the renderer kept pure so a Go Charm v2 port stays possible. Choose Go only if a separate distributable binary is itself a goal.
3. **Where it lives.** Recommend a `superclaude` subcommand registered like the others in `cli/main.py` (deferred import, then `add_command`). The command name is the owner's choice; suggestion: `superclaude orca observe`.
4. **Fixture replay before the live adapter.** Recommend yes. R0 proves every rendering invariant with no Orca dependency.
5. **Permission to capture one non-empty `check --all --json` sample** for the R2 contract, redacted before commit. Message bodies may hold sensitive content. Recommend yes, with redaction rules set by the owner. This is the decision that unblocks B's headline panel.
6. **What makes a message a "human question", and which handle or Run carries it.** This needs an answer from the owner or from Orca. Recommend agreeing on an explicit message type, and not inferring one from text.
7. **Is "latest 100 rows per Run, with older history not available" acceptable for the question panel?** Recommend yes, with the disclosure from section 4 and observer-side retention, until a durable history source exists.
8. **`--include-remote` default.** Recommend off until cross-host ownership joins are verified.
9. **Persisting "last look" across runs** (a local file, where, and how long kept). Recommend not in the MVP; session memory only.
10. **Polling bounds.** Recommend 15 s interval, 3 pages, 10 s per-call timeout and 30 s cycle deadline, adjustable by flag within fixed limits.
11. **Platform support.** Recommend POSIX interactive mode plus `--once` text export on every platform for the MVP.
12. **Fallback deadline.** Recommend: if R2's gate is not verified within a date the owner sets, switch the default screen to A on the same adapter (section 7).

## 12. Risks and UNVERIFIED items

### Risks

| Risk | Effect | Mitigation |
|---|---|---|
| The message row contract never verifies | B's headline panel stays empty, and the product becomes a relabelled A | Owner decision 5 and decision 12 (fallback deadline). The adapter and renderer are shared, so switching costs one layout. |
| A user reads the proxy panel as "questions" | False sense that human attention is covered | The panel title says `not questions`, the notice above it, and T9. |
| `page.total` includes historical dispatches | Denominators look larger than the live fleet | Label it `page.total (source)`, and show `result.counts` separately (T18). |
| Bound scope shows one Run as if it were the fleet | Missed orchestrators | Show `scope.source` in the header, plus the `one Run only` qualifier. |
| The hand-written key reader misbehaves (terminal modes, signals) | Terminal left in raw mode | Restore in `finally` and on SIGINT/SIGTERM. `--once` path needs no raw mode. Textual is the fallback stack. |
| Sanitizer gaps | Escape-sequence injection from worker text | A strict allow-printable sanitizer at the adapter boundary, tested against the `injection` fixture (T29). |
| Observer-local retention grows without limit in a long session | Memory, and a cluttered list | Cap retained items (for example 1,000), with `older retained items dropped: k` disclosed. Never drop silently. |
| Fixture schema mistaken for an Orca API | Code that couples to PROPOSED fields | Fixture mode is a separate loader. The live model is built only from the fields in section 3. |
| `_find_orca()` lives in `install_user_setup.py` | An observer import that pulls in installer code | Import it as is in the MVP. Moving it to a shared module is a separate, owner-approved refactor. |

### UNVERIFIED items (not to be presented as available)

- Row fields of `check --peek` and `check --all`, and the whole JSON shape of `inbox --json`. The only shape seen is an empty peek, `result.{count,dispatchId,runId}`.
- The meaning of `result.count` in check output: rows returned, or unread total.
- Whether `check --all --run <runId>` works from an unbound observer terminal, and which handle receives human-addressed messages.
- Whether any `--types` value (for example `escalation`, seen only as a help example) identifies a human question.
- The value set and meaning of `projection.nextAction.kind`, of `projection.stage.*` and of `projection.evidence.durable`.
- Whether `page.total` counts historical dispatches, and the exact semantics of `result.counts` relative to the rows in the page.
- Whether `projection.liveness.observedAt` and `evidence.lastObservedAt` share a clock or a timezone format (assumed ISO-8601; to be checked against the golden sample).
- Not established at all: complete message history beyond 100 rows; authoritative cross-host owner/task/session/worktree joins; admission and revision-pinned verification feeds and human-owner linkage; cost/usage accounting; durable event replay and ordering; native deep links.
- Stack facts from the seed brief table (versions, Textual text export, Charm wide-character width) were researched but not run here.
- The AC-1 to AC-10 mapping comes from the seed brief, not from a fresh read of the #409 text.
