# Variant 1 (architect): A. Signal Bridge as the Orca observer MVP

## 1. Summary

1. Build **A. Signal Bridge** first: it is the only direction whose largest panel (the fleet slice) is fed entirely by a verified, paged, non-consuming contract (`orca orchestration worker-list --json`) with an explicit `page.total` denominator.
2. B and C both lead with human-question rows, whose JSON fields (`check --peek/--all` rows, `inbox --json`) are UNVERIFIED today; A keeps the question panel but lets it degrade to a verified count (`result.count`) plus an honest "schema UNVERIFIED, latest 100 rows at most" label without leaving the screen empty.
3. Architecture: one read-only adapter, one renderer-independent snapshot model, and thin layout functions. B and C later become extra views over the same snapshot, so choosing A first does not discard their work.
4. Stack: Python with Rich (already a dependency, MIT, best text export) as a `superclaude` subcommand, with a small hand-written key reader; Textual is the fallback if key handling grows; Go Charm v2 is deferred to an owner decision.
5. Every release after the MVP is gated on a named source contract becoming verified; nothing outside the seed brief's Known Context is rendered as fact.

## 2. First buildable slice

One screen plus one detail view, the same panels at every width, only their size changing. Panel names below are the candidate; the synthetic `signal_bridge` layout in `layouts/group_a.py` is the visual reference, not the data contract.

| Panel | 160 columns | 116 columns | 80 columns |
|---|---|---|---|
| Header (scope, run, collected-at, page x/total, warning count) | 1 row, full width | 1 row | 2 rows (scope line, page line) |
| HUMAN QUESTION | top-left, 46 wide, 8 high | full width, 7 high | full width, 7 high |
| SIGNALS | right column, 34 wide, counts plus bars | **one line** under the question panel | **two lines** under the question panel |
| SESSION LEDGER | centre column | left, width minus 38 | full width, titled "SELECTED FLEET SLICE" |
| SOURCE FRESHNESS | under the question panel, 46 wide | right, 34 wide | one line above the footer |
| Footer (keys, filter, denominators) | 1 row | 1 row | 1 row |

Detail view (Enter on a ledger row): every field of the selected worker row with its full identifier (`dispatchId`, `taskId`, `runId`, `resource.id`, `resource.worktreeId`, `agentTerminalHandle`), each field marked "absent" when missing, and the raw `result.warnings[]`. No truncation in detail; long values wrap by cell width.

Keys (inspection and local filtering only): Up/Down or j/k move the selection; Enter opens detail; Esc returns; `/` sets a local text filter; `h` shows or hides historical rows; `r` requests an immediate read; `e` writes a plain-text export; `q` quits. Selection is keyed by `dispatchId`, so a refresh that reorders rows never moves the cursor to another worker; if the selected row disappears the cursor stays on a "selected row no longer observed" placeholder until the user moves.

**SIGNALS-panel discrepancy, resolved.** The design PLAN describes a SIGNALS panel with running/settled/unknown/stale/policy-frozen counts and bars. The built 160-column layout draws it. The built narrow layouts do not keep it: the 116-column branch (and the 144-column branch) drops the counts entirely, and only the under-116 branch keeps one "RUN n SETTLED n UNKNOWN n STALE n" line, which also omits the policy-frozen count. The candidate is the PLAN's intent: **SIGNALS is present at every width**, as a panel at 160 and as a one- or two-line strip at 116 and 80, and it never silently drops a bucket. Reason: the strip is the only place a supervisor sees the fleet denominator next to the question; removing it at 116 hides exactly the "unknown" and "stale" counts the issue says must be disclosed. The bars are decoration and may be dropped at narrow widths; the numbers and their denominators may not.

The MVP SIGNALS content differs from the fixture buckets, because "settled" and "policy frozen" have no verified source:

- `TERMINAL` line: `result.counts.{active,reclaimable,retained,released}` verbatim, labelled "process accounting, not task status" (the CLI help says so), plus `other n` for rows whose `terminalState` is outside those four (the filter accepts `release_pending` and `release_unknown`, which the counts block does not list).
- `LIVENESS` line: a histogram of `projection.liveness.verdict` values over the rows fetched this cycle, printed verbatim, with `of N fetched / page.total T`.
- `FROZEN` and `SETTLED`: printed as `unavailable` until a verified field exists; never `0`.

At 80 columns the two strip lines are `TERMINAL act 12 recl 3 ret 40 rel 230 other ? | scope bound` and `LIVENESS <v1> 9 <v2> 4 unknown 3 | 16 of 287`, truncated by display-cell width with a visible `>` marker.

## 3. Verified sources needed

Only two CLI verbs, both non-consuming. Field names come from the seed brief's Known Context (verified 2026-11-08 against Orca 1.4.245-aidev02.780594c521aa). Field **names** are verified; the value vocabularies (the set of strings `workerState`, `liveness.verdict`, `outcome` and `nextAction.kind` can take) are not enumerated in Known Context, so every value is printed verbatim and never mapped to a colour meaning "good" or "bad" until an enumeration is verified.

| Panel | Verb | Fields used |
|---|---|---|
| Header | `orca orchestration worker-list --json [--run <id>] --limit 100 [--cursor <c>]` | `result.scope.source` (flag, bound or all), `result.page.{limit,total,hasMore,nextCursor}`, `result.warnings[]` |
| SIGNALS | same call | `result.counts.{active,reclaimable,retained,released}`; per row `terminalState`, `projection.liveness.verdict` |
| SESSION LEDGER, line 1 | same call | `dispatchId`, `workerState`, `dispatchStatus`, `projection.stage.{worker,dispatch,activity}`, `projection.role` |
| SESSION LEDGER, line 2 | same call | `terminalState`, `projection.liveness.{verdict,observedAt}`, `projection.evidence.{durable,liveStatus,lastObservedAt}`, `projection.outcome`, `projection.nextAction.kind` |
| Grouping and placement | same call | `runId`, `taskId`, `resource.{ownerDispatchId,originDispatchId,worktreeId,ownershipState,releaseState}`, `projection.host.{id,kind}`, `projection.workspace.{id,kind}`, `projection.provider.id` |
| Detail view | same call | every field above plus `agentTerminalHandle`, `resource.{id,terminalHandle,recoveryAttemptCount}`, `projection.stage.detail` |
| HUMAN QUESTION | `orca orchestration check --peek --run <runId> --json` | `result.{count,dispatchId,runId}` (verified); row fields UNVERIFIED |
| HUMAN QUESTION, opt-in | `orca orchestration check --all --terminal <handle> --json` | same; capped at 100 rows by the CLI's own help |
| SOURCE FRESHNESS | both calls | local collection start/end time, exit status, duration, the `observedAt` / `lastObservedAt` ages above |

Grouping uses `runId` and labels it "run", never "orchestrator": the run-to-orchestrator join is not established. `resource.ownerDispatchId` is shown as a dispatch identifier, not as an owner person or mission. `--include-remote` is an explicit opt-in that adds `projection.host` grouping; it is not a cross-host ownership join.

Not used: `inbox` (JSON shape UNVERIFIED), plain `check`, `check --ack`, `check --wait` (it waits on the consuming path), any verb that writes.

## 4. Shown as unknown / stale / partial

Rendering rules live in the snapshot model, not in each layout, so B and C inherit them later.

- **Absent field** renders as `absent` (text), never blank, `0`, `false` or `-`. A present field with an empty string renders as `empty`. The two are different states in the model (`Missing` versus `""`).
- **Unknown value** (a string outside any verified vocabulary, which today is every value) renders verbatim in the muted style, with no good/bad colour.
- **Stale row**: `projection.liveness.observedAt` or `projection.evidence.lastObservedAt` older than the stale threshold (default 3 poll intervals, owner-adjustable) adds a `STALE 4m` tag. Stale is never shown as failed, and a stale row keeps its last-known values with "as of HH:MM:SS".
- **Stale source**: when a call fails, times out or returns unparsable JSON, the source row in SOURCE FRESHNESS turns to `STALE since HH:MM:SS (reason)`; all panels fed by it keep last-known values under a `last known` banner. Source loss never resolves a question, fails a session or clears a count.
- **Partial collection**: if `page.hasMore` is still true after the page budget (section 9), the header shows `PARTIAL 300 of 412 fetched` and every derived count says `of 300 fetched`, not `of 412`.
- **Denominators**: every count names its scope. Global (CLI) counts: `TERMINAL ... | scope bound` from `result.counts`, labelled with `scope.source`. Fetched counts: `LIVENESS ... | 300 of page.total 412`. Filtered counts: ledger footer `12 shown / 40 match filter "x" / 300 fetched / 412 total`. Historical rows hidden by default: `140 historical hidden (h)`.
- **100-row cap**: the HUMAN QUESTION panel always carries the line `messages: non-consuming peek, at most 100 rows, row schema UNVERIFIED`. When `result.count` is 100 or more it says `100+ unread (cap reached; older rows not visible)`. When it is 0 it says `0 unread in this run's peek; absence is not complete message coverage`, mirroring the prototype's wording.
- **Unavailable sources**: SETTLED, POLICY FROZEN, cost, admission and test evidence print `unavailable (no verified source)` where a slot exists, and are absent from totals.
- **Warnings**: `result.warnings[]` strings are shown sanitized in the header count and in full in a warnings line of the detail view.

## 5. Deliberately left out

| Left out | Why |
|---|---|
| Classifying a message as a "human question", with requester and owner | Row fields of `check --peek/--all` are UNVERIFIED; any classifier would be a guess. Gated to release R2. |
| Message history, "changes since last look" for messages | No durable non-consuming history beyond 100 rows; no replay or ordering contract. A local "seen" marker for worker rows only is in R1. |
| Orchestrator, mission and owner-person names | No authoritative cross-host mission/owner/task/session/worktree join. `runId` and dispatch IDs are shown instead. |
| SETTLED and POLICY FROZEN counts from the PLAN | No verified field. Slots show `unavailable`. |
| Admission, report validation, test results, human approval | No admission or revision-pinned verification feed. `projection.outcome` is shown verbatim and labelled "outcome as reported, not admission". |
| Cost, tokens, usage | Coverage not established. No slot at all in the MVP, so a partial number can never be read as a total. |
| Deep links, clickable destinations | No native deep-link format. Full identifiers are shown and exported as text instead. |
| Any operational control | Read-only by the issue's rule. No key sends anything to Orca except the two read verbs. |
| `inbox` verb | JSON shape UNVERIFIED; `check --peek/--all` covers the same need with a known top level. |
| Time-history, quilt and atlas views | Not part of Signal Bridge; they are later views over the same snapshot model. |
| Windows key input | The hand-written key reader is POSIX-only in the MVP (owner decision 11.5). Text export still works everywhere. |

## 6. Where B (Attention Ledger) and C (Decision Desk) are stronger

Honest concessions, each checked against the built layouts:

- **B is the better answer to the issue's first sentence.** The issue's core pain is human decisions buried in chat. `attention` in `layouts/agent_focus.py` lists every open question with its age, requester, owner and affected IDs; Signal Bridge's `_request` shows only the first question (`qs[0]`) and a count of the others. Once message rows are verified, B surfaces the second and third question without a key press; A does not.
- **B models the "seen is not resolved" rule explicitly.** Its SEEN IS NOT RESOLVED panel and RETAIN CONTEXT list (original question, original age, acting owner, requesting orchestrator, affected stable IDs, source coverage, explicit closure evidence) are the right retention contract for questions. A has no equivalent panel and would have to borrow it.
- **C gives the most decision-relevant evidence per screen.** `decision_desk` filters the ledger to the affected sessions of the selected request and reports `x/y other questions shown`. For the moment of answering one question, that is denser and less noisy than A's whole-fleet slice, which at 100 workers mostly shows rows unrelated to the question.
- **C's bounded "other questions" panel is a better denominator pattern** than A's single "n other questions" line, and should be copied into A's question panel at 160 columns in R2.
- **Where A is stronger, for the MVP only:** both B and C are empty or meaningless until message rows are verified, because their primary panel is built from `requests`. A's largest panel and its SIGNALS strip run on the verified worker-list contract today, and its question panel degrades to a verified count instead of an empty frame. A also shows stale and unknown workers that nobody has asked about, which B and C hide by design. The trade-off is that A answers "what is happening" better than "what must I decide"; R2 closes that gap once the message contract is verified.

## 7. Build order from MVP to later releases

Component boundaries first, because they decide what later releases cost. Proposed package `src/superclaude/cli/observe/` (name is owner decision 11.4):

```text
sources  ->  Snapshot (immutable, per poll)  ->  View(snapshot, width) -> Rich renderable  ->  Live screen | text export
  worker_list.py   model.py (Missing, Stale,        views/signal_bridge.py                     screen.py, keys.py, export.py
  message_peek.py  Partial, denominators)           (later: attention.py, decision_desk.py)
  fixture.py       sanitize.py, cells.py
```

Two seams only: a source returns `SourceResult(data | error, collected_at, duration, partial)`, and a view is a pure function from `Snapshot` and width to a renderable. Sanitizing and cell-width truncation happen once, when the snapshot is built, so no view can forget them. No plugin registry, no config file, no abstract base classes beyond those two signatures.

| Release | Contents | Gate (must be verified before work starts) |
|---|---|---|
| **R0 Offline** | Snapshot model, sanitizer, cell-width truncation, Signal Bridge view at 160/116/80, key handling, text export, NO_COLOR; fed by a fixture source built from the prototype `fixtures.py` variants, re-shaped to the verified worker-list field names | Owner selects the visual direction (the issue requires a human selection before production integration). No Orca contract needed. |
| **R1 Live MVP** | `worker_list` source with bounded paging, `message_peek` source with count only, SOURCE FRESHNESS, stale and partial handling, local "seen since last look" marker on worker rows (keyed by `dispatchId` plus changed fields) | Already verified: worker-list fields and paging, `check --peek/--all` top level. One more check: that `check --peek --run <id>` works from an unbound observer terminal (UNVERIFIED). |
| **R2 Questions** | Message rows rendered; human-question classification; C's bounded "other questions x/y" panel inside A's question area; B's `attention` added as a second view over the same snapshot | Row fields of `check --peek/--all` (and, if used, `inbox --json`) verified from real rows, including which fields identify a human question, its requester and its owner; a recorded sanitized fixture pinned by a schema test. |
| **R3 Affected scope** | C's `decision_desk` as a third view: question to affected sessions | A verified link from a message row to `dispatchId` / `taskId` / `resource.worktreeId`. |
| **R4 Fleet across hosts** | Grouping by host with `--include-remote`; owner/mission names instead of `runId` | Authoritative cross-host mission/owner/task/session/worktree join. |
| **R5 Evidence** | Admission, report validation and test-result columns, kept separate from `outcome` | Admission and revision-pinned verification feed with human-owner linkage. |
| **R6 History** | Message history beyond 100 rows, "changes since last look" for messages, ordering | Durable event replay and ordering across restarts. |
| **R7 Cost** | Cost/usage with coverage disclosure | Cost/usage accounting with complete coverage, currency and deduplication identity. |
| **R8 Links** | Deep links from detail view | Native deep-link format. |

R4 to R8 are independent of each other and can be reordered by whichever contract Orca verifies first. If the owner later selects Go (decision 11.2), the R0 `Snapshot` becomes a versioned JSON document (`superclaude observe --snapshot-json`) and a Go renderer consumes it; the Python sources and sanitizer stay. That export is not built until the owner asks for it.

## 8. Stack recommendation

Figures from the seed brief's stack table (primary sources read 2026-11-08, nothing run).

| Criterion | Go: Bubble Tea v2.1.1 / Lip Gloss v2.0.6 / Bubbles v2.2.1 | Python Rich 15.0.0 | Python Textual 8.2.8 | Rust Ratatui 0.30.2 |
|---|---|---|---|---|
| License | MIT | MIT | MIT | MIT |
| New toolchain | Go compiler, per-platform binary release pipeline | none (already a dependency) | one pure-Python dependency | Rust toolchain plus maturin or a binary |
| Keyboard and focus | strong, built in | **none**: raw key reading must be hand-written | strong, built in | strong |
| Plain-text export | none built in | best: `Console(record=True)`, `export_text()` | UNVERIFIED | plain-text snapshots |
| Width-fixed tests | `teatest/v2` untagged under `x/exp` | width-fixed test consoles | headless `run_test(size=...)`, SVG snapshots | yes |
| Cell width | wide-character width UNVERIFIED | `rich.cells.cell_len` | via Rich | yes |
| NO_COLOR | parsed as a boolean; `NO_COLOR=yes` ignored, contrary to no-color.org | must be honoured explicitly (no house TUI does so today) | inherits Rich behaviour (UNVERIFIED) | manual |
| Maintenance | low risk, monthly releases | medium, same maintainer, very widely used | medium: company wound down May 2025, community-maintained, last release June 2026 | low-medium, pre-1.0 |
| Fit with this repo | second language, second test runner, second CI path | matches four existing Rich TUIs (`sprint/tui.py`, `sprint/monitor.py`, `prd/tui.py`, `cleanup_audit/tui.py`) and `uv run pytest` | Python, but a new framework style | second language |

**Recommendation: Python Rich for R0 and R1, inside this repository.** Reasons:

1. Zero new dependencies and zero new toolchains; the repository is Python under MIT and already ships Rich TUIs with the `Live` plus `_render()` pattern.
2. The issue's text-export and NO_COLOR requirements are the hardest to retrofit, and Rich is strongest at export while Bubble Tea has no export and a known NO_COLOR deviation.
3. Tests run with the existing `uv run pytest` at fixed widths, with no untagged experimental test package.
4. The cost is the key reader. Scope it small: POSIX `termios`/`tty` cbreak mode on a daemon thread feeding a queue, the same thread-plus-`Event` shape as `sprint/monitor.py`'s `OutputMonitor`; about nine keys; restore the terminal in a `finally` block and on SIGINT/SIGTERM. Non-TTY stdin falls back to a one-shot text export, as `prd/tui.py` and `cleanup_audit/tui.py` already fall back when `sys.stderr.isatty()` is false.

**Switch rule:** if R2 or R3 needs scrolling panes, multi-pane focus or mouse input, move the view layer to Textual (same language, MIT, keeps sources and snapshot); accept its medium maintenance risk then, not now. Go is the issue's preference; it is an owner decision (11.2), and the snapshot seam in section 7 keeps that path open without a rewrite of the sources. TUIBBS-scp is AGPL: nothing is copied from it under any stack.

## 9. Smallest trustworthy read-only adapter

**Binary discovery.** Reuse `_find_orca()` in `src/superclaude/cli/install_user_setup.py` (defined at line 198; tries `orca-ide` then `orca` from `_ORCA_CLIS`, validates with `skills list --json` under a 10 s timeout so the GNOME screen reader named `orca` is never run). Call it once at start-up; cache the path for the session. If it returns `None`, the screen opens in an "Orca CLI not found" state with every source `unavailable`, and `--fixture <name>` remains usable. Importing a private helper across modules is acceptable for R1; move it to a shared module only if a third caller appears.

**Allow-list, enforced in code.** The adapter builds argument vectors only from these two templates, with `subprocess.run([...], shell=False)`; any other verb or flag raises before a process starts, and a unit test asserts the forbidden set (`--ack`, `--wait`, bare `check`, `dispatch`, `inbox`, any other verb) can never be produced:

```text
<orca> orchestration worker-list --json --limit 100 [--run <runId>] [--cursor <opaque>] [--include-remote]
<orca> orchestration check --peek --run <runId> --json
```

`check --all --terminal <handle>` is a third template, off by default, enabled per terminal from the detail view (owner decision 11.6). `--cursor` is passed back unchanged, as the help requires; `runId` and handles are validated against a conservative character set before use as arguments.

**Polling bound.** One poll cycle at a time (single flight; a new cycle never starts while one runs). Default interval 5 s, minimum 2 s, no LLM anywhere in the loop. Per cycle: worker-list up to 3 pages (300 rows; owner-adjustable to at most 10 pages), then one `check --peek` per distinct `runId` seen, capped at 10 runs (the issue's 5-10 orchestrators); runs beyond the cap are listed as `not peeked (cap 10)`. Manual `r` triggers one cycle immediately, still single flight.

**Timeouts.** 10 s per call (the same bound as `_find_orca()`), 25 s per cycle. A timed-out call is killed, its source marked `STALE (timeout)`, and the cycle continues with the next source. After two consecutive failures of a source the interval for that source doubles, up to 60 s; one success resets it.

**Parsing.** `json.loads` on stdout only; stderr is kept (sanitized, truncated) for the detail of a failure. The top-level shape is validated: `result.workers` must be a list and `result.page.total` an integer, else the whole response is `unparsable` and last-known values stay. Individual rows are tolerant: an unexpected type or missing field becomes `Missing` for that field only, never a crash and never a default value. Rows without `dispatchId` are kept, counted in `rows without id: n`, and excluded from selection.

**Duplicates and ordering.** Rows are keyed by `dispatchId`. Because pages are newest first and the fleet changes between page reads, a row can appear on two pages or be skipped; duplicates keep the one with the newer `projection.liveness.observedAt` (ties: the later page) and add `duplicates merged: n` to the header. A possible skip is disclosed by the existing partial rule whenever `fetched` is lower than `page.total`. Rows from an older cycle never overwrite a newer cycle (each snapshot carries a monotonic cycle number), so a slow call that finishes late cannot roll the screen back.

**Sanitizing.** Every string from Orca passes one sanitizer when the snapshot is built: strip CSI, OSC (terminated or not), DCS/APC/PM/SOS, 8-bit C1 controls (0x80-0x9F), every bare C0 control and DEL (a newline inside a single-line cell becomes the visible ASCII text `\n`), and Unicode format characters (category Cf, including bidirectional overrides). Base it on the stricter prototype `canvas.py` `sanitize`, not on `eval/pty_stream.py`'s `ANSI_ESCAPE_RE`, which the enrichment found misses C1, bare controls, Cf and unterminated OSC. Truncation uses `rich.cells.cell_len`, never `len()`, and never cuts inside a wide character.

## 10. MVP acceptance tests mapped to issue acceptance criteria

The issue's criteria are paraphrased from the seed brief (problem statement, constraints, success criteria); the issue text itself was not re-read for this proposal. All tests run offline with `uv run pytest`, through a fixture source whose rows use the verified worker-list field names, rendered on a Rich `Console(width=W, record=True, color_system=None)` and compared as plain text. Fixture generators are seeded and deterministic.

| # | Issue criterion (paraphrased) | Test |
|---|---|---|
| T1 | Fits 160/116/80 columns | Every scenario below rendered at 160, 116 and 80: no line exceeds W cells (`cell_len`), every panel title from section 2 is present, SIGNALS is present at all three widths. |
| T2 | Base fleet: 8 orchestrators, 80 sessions | 8 `runId`s, 80 rows: header says `80 of page.total 80`, TERMINAL counts equal the fixture's `result.counts`, ledger footer denominators correct, 8 runs peeked. |
| T3 | Scale grid 5/8/10 x 50/80/100 | All nine combinations x three widths (27 renders): denominators correct; at 10 runs every run peeked; at 100 rows exactly one page; a 101-row variant forces a second page and a `page.hasMore` path. |
| T4 | Uneven ownership | 10 runs with 1, 1, 2, 3, 5, 8, 13, 20, 22, 25 rows: per-run counts correct; no run is hidden at 80 columns without a `n runs not shown` line. |
| T5 | Shared and unmapped worktrees | Three rows share one `resource.worktreeId`, two rows have none: detail shows `shared by 3 rows` and `worktree: absent`; nothing asserts a one-to-one mapping. |
| T6 | Historical records separate from live | 140 rows with `terminalState` released: hidden by default with `140 historical hidden (h)`; `h` shows them; TERMINAL counts unchanged by the toggle. |
| T7 | Duplicates | Same `dispatchId` on two pages with different `observedAt`: one row kept (newer), `duplicates merged: 1` shown. |
| T8 | Out-of-order events | Cycle 7's result delivered after cycle 8's: screen still shows cycle 8 values. A row whose `observedAt` goes backwards keeps the newer value. |
| T9 | Stale sources disclosed | worker-list times out after a good cycle: SOURCE FRESHNESS shows `STALE since`, ledger shows `last known`, no row changes state, no count becomes 0. Peek fails: question panel says `messages: unavailable`, not `0 unread`. |
| T10 | Missing fields: unknown is never zero or false | Rows missing `projection`, `liveness.verdict`, `outcome`, `resource.worktreeId`, `page.total`: each renders `absent`; a missing `page.total` makes the header `total unknown`, never `0`. A row without `dispatchId` is counted and not selectable. |
| T11 | Lifecycle, outcome, acceptance, tests and approval stay separate | Ledger and detail render `workerState`, `dispatchStatus`, `terminalState` and `outcome` in separate labelled cells; SETTLED, POLICY FROZEN, admission and tests read `unavailable`; a test asserts no code path derives one from another. |
| T12 | ANSI/OSC/control injection | The prototype `injection` variant plus CSI, terminated and unterminated OSC 8/52, DCS, 8-bit C1, bare C0, DEL and bidi-override strings in `stage.detail`, `warnings[]` and IDs: rendered text and export contain none of them; geometry unchanged. |
| T13 | Truncation by display-cell width | CJK, emoji and combining-mark identifiers: no line exceeds W cells, no wide character is split, truncated cells end in `>`; detail view shows the full identifier. |
| T14 | NO_COLOR | With `NO_COLOR` set to any non-empty value (including `yes`), output has no colour codes and state is still readable from text labels alone; with it unset or empty, colour is allowed. |
| T15 | ASCII/text export | `e` and `--export` write UTF-8 plain text with no escape sequences, identical to the recorded console text; an `--ascii` export replaces box-drawing characters with `+-|`. |
| T16 | Stable keyboard selection | Select row X, refresh with rows reordered and two inserted above: X stays selected. X disappears: placeholder shown, no jump. |
| T17 | Read-only, non-consuming | Adapter allow-list test: every generated argument vector matches a template in section 9; `--ack`, `--wait`, bare `check` and every other verb are rejected before `subprocess` is called (patched to fail the test if reached). |
| T18 | Bounded, deterministic collection | With a fake clock and fake runner: at most 3 worker-list pages and 10 peeks per cycle, no overlapping cycles, backoff doubles to 60 s and resets. |
| T19 | 100-row cap disclosed | Peek fixture with `result.count` 100: panel says `100+ unread (cap reached; older rows not visible)`; count 0 says absence is not coverage. |
| T20 | No blinking | Rendered segments never carry the blink style; a check over all styles used. |
| T21 | Full identifiers in detail | The `long-identifiers` variant: every identifier appears untruncated in detail and in export. |

Prototype fixture variants (`base`, `uneven`, `shared-unmapped`, `historical`, `long-identifiers`, `source-loss`, `missing-fields`, `duplicate-out-of-order`, `empty`, `injection`) seed T2 to T21 after re-shaping to the verified field names; the PROPOSED fixture schema itself is not adopted.

## 11. Open owner decisions

Only decisions that need the human; each with this proposal's recommendation.

1. **Visual direction.** The issue requires a human selection before production integration. Recommendation: Signal Bridge, with the SIGNALS strip kept at every width (section 2), and C's bounded "other questions x/y" panel folded into the question area at R2.
2. **Production stack.** Recommendation: Python Rich for R0 and R1; revisit at R2 with Textual as the in-language step up. Choose Go Charm v2 only if the owner wants a standalone binary outside this repository and accepts a second toolchain, a release pipeline and the NO_COLOR and export gaps.
3. **Is a question panel honest when it can only say "latest 100 rows, schema UNVERIFIED"?** Recommendation: yes for R1, provided the panel shows only the verified `result.count` and the cap line, and classifies nothing; no for R2 until row fields are verified from real rows.
4. **Where the MVP lives.** Recommendation: a `superclaude observe` subcommand in this repository, registered the house way (deferred import plus `main.add_command(...)` in `cli/main.py`, group in its own `commands.py`); final command name is the owner's.
5. **Platform scope.** Recommendation: POSIX terminals only for interactive mode in R1; text export everywhere. Windows key input deferred.
6. **`check --all --terminal <handle>`.** It returns every message for a handle (up to 100 rows) and could expose message content on screen. Recommendation: off by default, opt-in per terminal from the detail view, never in text export unless a flag says so.
7. **Fixture replay before live.** Recommendation: yes, R0 offline first; it ships the sanitizer, width and export tests with no Orca dependency and lets the owner run the synthetic walkthrough `integration-gaps.md` asks for.
8. **Polling defaults.** Recommendation: 5 s interval, 3 pages, 10 runs, stale after 3 intervals; the owner confirms these against real fleet size.

## 12. Risks and UNVERIFIED items

| Item | Status | Effect on this proposal | Mitigation |
|---|---|---|---|
| Message row fields of `check --peek/--all` | UNVERIFIED | Question panel limited to a count in R1 | R2 gate: record real rows, pin a schema test |
| `inbox --json` shape | UNVERIFIED | Not used | Re-evaluate at R2 |
| Whether `result.count` is total unread or rows returned (and whether it stops at 100) | UNVERIFIED | Cap wording in section 4 may need adjusting | Test against a run with more than 100 unread before R1 ships |
| `check --peek --run <id>` from an unbound observer terminal | UNVERIFIED | Question count may be unavailable for other runs | R1 gate check; fallback: panel shows `unavailable` |
| Value vocabularies of `workerState`, `dispatchStatus`, `liveness.verdict`, `outcome`, `nextAction.kind` | UNVERIFIED | No good/bad colours, verbatim values only | Add colour mapping only after an enumeration is verified |
| Cursor stability while the fleet changes (newest-first pages) | UNVERIFIED | Possible duplicates or skips across pages | Dedupe by `dispatchId`; partial disclosure whenever fetched < total |
| `--include-remote` behaviour on hosts without fleet listing | UNVERIFIED (help says "when the host supports") | Remote rows may silently not appear | Off by default; header shows `scope: local only` |
| Run-to-orchestrator mapping | Not established | "5-10 orchestrators" shown as runs | Label "run", never "orchestrator" |
| Cross-host ownership, admission feeds, cost coverage, event replay, deep links | Not established | Excluded from MVP | Gated releases R4-R8 |
| Hand-written key reader on Rich | Risk | Terminal left in raw mode after a crash | `finally` restore plus signal handlers; non-TTY falls back to export; Textual switch rule |
| Prototype has no independent post-correction review PASS | Risk | Its layouts and fixtures may carry defects into R0 | Use them as references and test seeds only; R0 tests are written against this spec |
| Signal Bridge shows the whole fleet, so at 100 workers most ledger rows are unrelated to the open question | Design risk | Supervisor may still miss a decision | Question panel stays on top at every width; R2 adds C's bounded other-questions list |
| Load on Orca from polling | Risk | 3 pages plus up to 10 peeks every 5 s | Single flight, caps, backoff, owner-tunable defaults |
