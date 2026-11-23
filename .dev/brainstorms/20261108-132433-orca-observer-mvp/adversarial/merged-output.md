<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant B (opus:analyzer) -->
<!-- Merge date: 2026-11-08 -->

# Orca read-only observer MVP (#409): merged design, base B (Attention Ledger)

<!-- Source: Base (original, modified) — title widened because the visual direction is now an owner decision (Change 21, Change 23) -->

## 1. Summary

<!-- Source: Base (original), section 1 items 1-2 -->
1. Root cause of #409: a human question gets lost because chat is ordered by recency and because reading a message is treated as handling it. Only B makes that failure mode its primary object: questions oldest first, and "seen is not resolved".
2. All three directions put a human-question panel at their centre, and all three depend on the same UNVERIFIED message row contract. They differ in how they degrade without it. B shows the gap as its headline. A falls back to a fleet slice that looks complete. C has nothing to select.

<!-- Source: Base (original, modified) — items 3-7 rewritten per Change 21 (default screen as a recommendation), Change 22 and Change 31 (gates, production integration), Change 24 (candidate verb), Change 23 (stack as owner decision); convergence-r3 Changes to the Round 2 Consensus 1-5 -->
3. **The visual direction is owner decision 1 (section 11). The debate only recommends.** Recommended sequence, pending the owner's dated selection record: for R1, A's worker ledger with the source-reported COUNTS strip and B's one-line question-source gap notice; after the QUESTION-OBSERVATION gate passes, B's Attention Ledger, with A's ledger one key away as the fleet view; C's Decision Desk only behind the QUESTION-LINK gate. V3 dissents: it recommends C as the post-link composition (section 12). No direction is the default until the owner selects it.
4. **Release order:** R0 is offline fixture replay, which also produces renders of A, B and C for the owner. The DIRECTION-SELECTED gate sits between R0 and R1. It has NOT passed: no owner selection exists. R1 is live on `worker-list` only. Question rows come only after QUESTION-OBSERVATION, and `orca orchestration check --all --run <runId> --json` is only a candidate verb for that gate, with three UNVERIFIED proofs (section 7). Even after admission the question area is labelled "bounded best effort; coverage unknown".
5. Until QUESTION-OBSERVATION passes, the question area reads `source UNVERIFIED, 0 rows interpreted, not "no questions"`. Worker-reported `projection.nextAction.kind` values appear only as a verbatim ledger column. They are never called questions.
6. Stack: Python Rich (already a dependency, MIT) inside this repo, with a small stdlib key reader, is recommended. It departs from the issue's stated Go preference, so the owner confirms it (owner decision 2). Go Charm v2 stays possible later, because the screen and export renderers are pure functions over one view model.
7. "Production integration" has two UNVERIFIED readings (section 7). The stricter one applies until the owner confirms: only offline work (fixture replay, the key-reader spike, renders) happens before the selection record.

### Evidence chain behind the retention design

<!-- Source: Base (original) — preserved per refactor-plan "Preserve unchanged" (evidence chain for retention); heading narrowed from "the recommendation" because the direction is now an owner decision (Change 21) -->
- `check --help` (read 2026-11-08): `--peek` returns "only unread messages". When a coordinator runs plain `check` and then `--ack`, those messages stop being unread, so they leave the peek view even if the human never answered. A panel built on `--peek` would therefore resolve questions when they are read. That is exactly the defect #409 describes. The only non-consuming verb that keeps read rows is `--all` ("every message for the handle; does not mark read"), and it is capped at 100 rows.
- Conclusion: an honest question view has to keep, in the observer, every question it has observed until explicit closure evidence appears. That is B's "RETAIN CONTEXT" design (design-package prototype `layouts/agent_focus.py` `attention`, a visual reference only: original question, original age, acting owner, requesting orchestrator, affected stable IDs, source coverage, explicit closure evidence). A and C do not specify retention. They render the current row set.
- No verified source records explicit closure today. So every retained question stays "open, closure source unavailable". It is never shown as resolved, and it is never quietly dropped.

## 2. First buildable slice

<!-- Source: Base (original, modified) — opening rewritten per Change 21 (default screen pending the owner, start-up view rule from INV-021), Change 22 (R0 renders for the selection), convergence-r3 Changes 1-2; prototype note per refactor-plan "Changes NOT Being Made" X-001 -->
The slice has one view model, three views over it, a detail inspector and a text export, in two data modes. `fixture` mode reads the package's synthetic fixtures. `live` mode reads `worker-list` only.

- **R0 (fixture mode)** renders all three directions, A (Signal Bridge), B (Attention Ledger) and C (Decision Desk), at 160, 116 and 80 columns, each marked "synthetic fixture, not live evidence", with realistically degraded versions beside them. These are the input to the owner's selection (DIRECTION-SELECTED gate, section 7).
- **R1 onward** builds the view the owner selects. The recommendation, pending the owner, is: A's worker ledger plus the COUNTS strip plus B's one-line question-source gap notice while no question rows can be read; B's Attention Ledger after QUESTION-OBSERVATION passes, with A's ledger one key away; C's desk only behind QUESTION-LINK. The B screen described below is therefore the recommended post-QUESTION-OBSERVATION view, and the way B renders in degraded form for the owner's comparison before that gate.
- **Start-up rule (INV-021):** the view is picked once at start-up from the runtime state of the question source. If the question source has not succeeded in this process, the observer starts on A with the gap notice, even in a release whose gate passed. The view never switches automatically mid-session, because that would move the human's place.
- **Prototype status (X-001):** the design-package prototype is a visual reference only. There is no production import of prototype code. Its 116-column collapse claim does not match the built prototype, so width rules come from the Round 2 consensus (A's width matrix, B's x/width coordinates, C's 44-row height contract), not from the prototype or the seed brief's collapse description.

<!-- Source: Base (original), section 2 geometry sentence; Change 4 (INV-013) adds the under-80 rule -->
B's panel geometry: at 116 columns or more it draws the full frame, with `right = width - 43`. From 80 to 115 columns it uses the single-column narrow layout. Under 80 columns every view shows `terminal too narrow (min 80)` above the COUNTS strip, and the strip's denominators still print.

### Common to every width

<!-- Source: Base (original, modified) — header and freshness strip from base; Change 16 (collection vs evidence freshness); Change 20 (cost); read-k-of-N header per Change 21 (INV-021) -->
- **Header line 1:** `ORCA OBSERVER  mode=fixture|live  scope=<result.scope.source or "scope unknown">  as of <local time of last good poll>`. In fixture mode this always reads `SYNTHETIC FIXTURE <variant>, not Orca data`. In the B view the header adds `read k of N Runs since start; oldest among Runs read` until every Run in the rotation set has been read once.
- **Header line 2, the freshness strip (taken from A):** one cell per source, `worker-list OK 4s` / `STALE 52s` / `FAILED (exit 2) 1m` / `NOT POLLED`. A second cell, `messages UNVERIFIED (not read)`, stays in the strip until QUESTION-OBSERVATION passes. The strip shows collection freshness (when the observer last polled successfully). Evidence freshness (when a worker last reported, `evidence.lastObservedAt`) is a different fact and is shown per row as a plain age, never merged into the source cell.

<!-- Source: Variant 1 (opus:architect), counts strip — merged per Change 4 (INV-013, INV-014); SETTLED/FROZEN per Change 7; cost per Change 20 -->
- **COUNTS strip (source-reported), at every width of 80 columns or more:** numbers and denominators only, no bars and no health name. Tokens: `collected n / reported T`, `PARTIAL` when it applies, the scope, `source counts: active a / reclaimable r / retained t / released l` (from `result.counts`, never summed with page-derived counts), `SETTLED unavailable (no source)`, `FROZEN unavailable (no source)`, `cost unavailable`. Priority order: `collected n / reported T`, `PARTIAL` and scope are never truncated. At narrow widths the strip wraps to a second line before anything is cut, and the `>` marker applies only to lower-priority tokens (source age, the `unavailable (no source)` tokens). The strip is one of the minimum rows of the height contract and is never dropped.

<!-- Source: Variant 1 (opus:architect), keys and selection — merged per Change 8 (keys, ID-anchored selection), Change 6 (historical rows), Change 9 (truncation marker), Change 13 (identity), Change 32 item 11 (question identity); base footer modified -->
- **Keys (inspection and local filtering only):** Up/Down or `j`/`k` move, `Enter` opens detail, `Esc` returns, `/` sets a local text filter, `h` shows or hides historical rows, `m` marks a look, `e` writes an export, `q` quits. There is no `r` refresh key: refresh runs on the fixed 15 s cycle. No key maps to an Orca call.
- **Footer:** the key list, plus `shown x/y | collected n / reported T`.
- **Historical rows:** rows with a historical `terminalState` (released or retained) are hidden by default, with a visible `k historical hidden (h)` count. `h` shows them. The toggle never changes the source counts. Historical evidence that is explicitly linked to a shown item is never hidden.
- **Selection** is anchored to a stable identity, never to a row index. Worker rows use source namespace plus `dispatchId`. Questions (from QUESTION-OBSERVATION) use a verified source-scoped question identity, never a worker `dispatchId`; that identity is a QUESTION-OBSERVATION gate requirement. A refresh that reorders rows keeps the cursor on the same identity. If that identity disappears, the cursor stays on a placeholder, `selected <id> no longer in source window`, until the user moves. It never jumps to a different worker.
- **Truncation:** list cells are truncated by display-cell width with a visible `>` marker. Non-UTF-8 terminals use the `--ascii` path, which replaces box-drawing characters with `+-|`.

<!-- Source: Base (original) -->
- **Detail inspector (Enter)** shows every field untruncated, wrapped by cells: `dispatchId`, `taskId`, `runId`, `resource.worktreeId`, `resource.ownerDispatchId`, `resource.originDispatchId`, `projection.host.id`, `projection.workspace.id`. Each absent field reads `unknown (absent in source)`.

### Worker ledger (A's ledger; the recommended R1 view, pending the owner)

<!-- Source: Variant 1 (opus:architect), session ledger, with the base's proxy panel replaced by a verbatim column — merged per Change 1; Round 2 consensus (label "run") -->
- One row per worker from `worker-list`, in source order: `dispatchId`, run (labelled "run", never "orchestrator"), `workerState`, `dispatchStatus`, `terminalState`, `projection.outcome` (raw), `projection.nextAction.kind`, `liveness.verdict (liveness.source)`, and the evidence age.
- **`projection.nextAction.kind` is a verbatim column.** It shows exactly the string the source reported. Absent or blank reads `unknown`. It is never classified, never executed, never ranked as an action list and never called a question. It may be used as a labelled local filter.
- Above the ledger, at every width, sits B's one-line question-source gap notice: `Human questions: source UNVERIFIED, 0 rows interpreted, not "no questions"`.
- At 116 columns the ledger shows `<kind> <dispatchId> <liveness.verdict> <age>` and moves `stage` into the detail inspector. At 80 columns each line holds `kind`, a dispatch ID truncated by cell width with `>`, and an age.

### Attention Ledger (B), 160 columns

<!-- Source: Base (original, modified) — live-mode text per Change 28 and Change 24; lower-left panel replaced per Change 1; SEEN IS NOT RESOLVED live text per Round 2 consensus (C-003, INV-008), carried through Change 28 -->
- **Left, `OPEN HUMAN QUESTIONS`** (x=1, width 114). In fixture mode it lists one block per question: `NN MIN`, the question, `requester requests / owner`, and `Affected: id, id`, oldest first. In live mode before QUESTION-OBSERVATION it shows one fixed block: `Question rows: source UNVERIFIED. 0 rows interpreted. This is not "no questions".` After QUESTION-OBSERVATION the title reads `bounded best effort; coverage unknown; at most 100 rows per read, not 100 questions`.
- **Left lower, the worker ledger** (live mode only), with `projection.nextAction.kind` as a verbatim column, titled `worker-reported, not questions`. It replaces the base's separate "next actions" proxy panel.
- **Right top, `SEEN IS NOT RESOLVED`** (x=117, width 42). It shows a big count of observed open questions. A sub-line breaks it down as `marked looked: a | not marked: b | closed by evidence: unavailable`. In live mode with no question source it reads `unknown (no question source)`, never 0.
- **Right lower, `RETAIN CONTEXT`.** The seven retained attributes from the prototype layout. In live mode each one carries its availability: `original question: UNVERIFIED source`, `acting owner: resource.ownerDispatchId (worker-list)`, `explicit closure evidence: unavailable (no source)`.

### Attention Ledger (B), 116 columns

<!-- Source: Base (original, modified) — proxy panel reference replaced per Change 1 -->
The structure is the same, with `right = 73`. The question panel is 70 columns wide and the right column stays 42. The worker ledger uses its 116-column line form.

### Attention Ledger (B), 80 columns

<!-- Source: Base (original, modified) — `~` marker replaced by `>` per Change 9; COUNTS strip per Change 4 -->
A single column: the header, the freshness strip, the COUNTS strip, the `SEEN IS NOT RESOLVED n` line, the question lines (fixture) or the UNVERIFIED notice (live), then the worker ledger in its 80-column line form. The two invariant lines from the prototype stay: "Questions stay until explicit resolution." and "No reply observed is not delivery failure." RETAIN CONTEXT is reachable only through the inspector.

### Height

<!-- Source: Variant 3 (haiku:backend), Round 3 INV-014 refinement — merged per Change 32 item 9; Round 2 consensus layout (C's 44-row height contract) -->
Height follows C's 44-row height contract (drop order, minimum rows). Coverage, scope and `PARTIAL` are minimum content, kept ahead of every optional panel. If the terminal height cannot hold them, the screen shows a too-small diagnostic instead of a view that hides them. The Rich MVP has no per-panel scrolling and no multi-pane focus.

### "Changes since last look"

<!-- Source: Base (original, modified) — baseline rule from Variant 3 per Change 15 -->
The first observation in a process is the baseline, and a restart discloses that a new baseline was taken. `m` records a new observer-local mark, held in memory for this process only. Every row added, removed, or changed in `stage`, `nextAction.kind` or `liveness.verdict` since the mark shows a `*` and appears in a `changed since HH:MM (k)` count. Rows on pages not read in this cycle read `not reobserved`, not "unchanged". Marking a look never changes the open count. That is the "seen is not resolved" rule made mechanical.

## 3. Verified sources needed

<!-- Source: Base (original), section 3 table — preserved; "Fields used" denominators unchanged -->
The MVP (R0 and R1) needs exactly one live source. Everything else stays fixture-only or is labelled UNVERIFIED.

| Need | Verb | Fields used (verified in the seed brief, 2026-11-08) |
|---|---|---|
| Worker rows | `orca orchestration worker-list --json --limit 100` | `result.workers[].dispatchId, taskId, runId, workerState, dispatchStatus, terminalState` |
| Ownership and worktree (shown verbatim, never joined across hosts) | same | `resource.{id, ownershipState, releaseState, worktreeId, ownerDispatchId, originDispatchId, recoveryAttemptCount}` |
| Next action (verbatim column, Change 1) | same | `projection.nextAction.kind`, `projection.stage.{worker,dispatch,activity,detail}` |
| Freshness and liveness | same | `projection.liveness.{verdict,source,observedAt}`, `projection.evidence.{durable,liveStatus,lastObservedAt}` |
| Outcome, kept separate from lifecycle | same | `projection.outcome` (shown raw; never merged with `workerState` or `terminalState`) |
| Placement | same | `projection.host.{id,kind}`, `projection.workspace.{id,kind}`, `projection.provider.id`, `projection.role` |
| Paging and denominators | same, with `--cursor <page.nextCursor>` | `result.page.{limit,total,hasMore,nextCursor}`, `result.counts.{active,reclaimable,retained,released}`, `result.scope.source`, `result.warnings[]` |
| Binary | existing `_find_orca()` in `cli/install_user_setup.py` | validated through `skills list --json` |

Verbs and flags read from `--help` today (flags only, no new fields): `worker-list` accepts `--run`, `--terminal-state`, `--include-remote`, `--cursor`, `--limit <1-100>`. Its help says rows are "newest first", and that without `--run` the scope is the bound Run, or every Run when nothing is bound, as reported in `scope.source`. `check` accepts `--peek`, `--all`, `--types`, `--run`, `--terminal`. `inbox` accepts `--limit`, `--terminal`, `--full`.

### What is verified today, and what is not

<!-- Source: refactor-plan Overview "Evidence rule for the merge"; Change 24 (INV-020); Change 27 (required and optional fields); convergence-r3 Change 5 -->
- **Verified sources today, and only these:** `orca orchestration worker-list --json` (`result.workers[]`, `result.page.{limit,total,hasMore,nextCursor}`, limit 1-100, paged by cursor), and the non-consuming `check --peek` / `check --all` reads, which help says are capped at 100 rows. Plain `check` consumes deliveries, so the observer never calls it.
- `page.total` is verified as a field the source can return, but the adapter treats it as optional: when absent it reads `reported unknown` (Change 27; V1 dissents, section 12).
- **Message row fields and the inbox JSON shape are UNVERIFIED.** The only message shape seen is an empty peek, `result.{count,dispatchId,runId}`.
- **Not established, never presented as available:** complete message history, cross-host ownership joins, admission and revision-pinned evidence feeds, cost/usage accounting, durable event replay, native deep links.

### Candidate message verb (behind QUESTION-OBSERVATION only)

<!-- Source: Base (original, modified) — base "R2 uses check --all" reworded to a candidate per Change 24 (INV-020); acquisition rule per Change 32 item 4 and convergence-r3 Change 8; label per convergence-r3 Change 5 -->
`orca orchestration check --all --run <runId> --json` is a **candidate** verb for the question area, never an available one. It is admitted only if the QUESTION-OBSERVATION gate passes, and that gate needs three UNVERIFIED proofs:

1. Does `--run` narrow `--all`? Shown with at least 2 Runs.
2. Which handle receives human-addressed messages?
3. The measured message rate, recorded so the per-cycle message-call budget and the 100-row exposure can be set. A measured rate does not prove completeness.

Even if it is admitted, the question area stays labelled "bounded best effort; coverage unknown; bursts over 100 rows between reads may be lost". Acquisition permission is checked before any message call, separately from display and export permission (section 9). Not used in R0 or R1: `check --peek`, the candidate `check --all` read, `inbox`. Parsing an unknown row shape into "questions" would invent a contract.

### Mappings that are UNVERIFIED and must be shown that way

<!-- Source: Base (original) -->
- The value set of `projection.nextAction.kind`, and whether any value means "a human must answer". The MVP shows the raw string and never classifies it.
- Whether `projection.stage.activity` or `.detail` carries question text. The MVP shows these only in the inspector, sanitized and labelled `worker-reported`.
- The meaning of `projection.evidence.durable` beyond its presence. It is shown raw.
- Whether `page.total` counts historical dispatches. The live warning example "Showing 2 of 287 Dispatches" suggests it does, which is not proven. The MVP labels it `reported T` and does not call it "workers".

## 4. Shown as unknown / stale / partial

<!-- Source: Variant 3 (haiku:backend), four states per fact — merged per Change 12 as the governing rule -->
**Governing rule: four states per fact.** Every rendered fact is one of `known`, `unknown` (the source omitted it), `unavailable` (no verified source exists for it) or `stale` (the source has not been read successfully within 3 intervals). An aggregate with any unknown member is written `n+? (k unknown)`, never as a clean `n`. Unknown is never shown as zero or false.

Rendering rules. Each is pinned by a test in section 10.

<!-- Source: Base (original, modified) — "no source" aligned to the four-state `unavailable (no source)` per Change 12 and Change 7 -->
- **Absent field:** shows the literal `unknown`, in muted style. Under NO_COLOR it reads `unknown` with no colour. It is never `0`, `false`, `-` or blank.
- **Lifecycle vs outcome vs report vs acceptance vs tests vs approval:** these are separate columns or inspector lines. `workerState`, `dispatchStatus`, `terminalState` and `projection.outcome` are shown as separate raw values. Report status, acceptance, tests and human approval have no verified source, so every one of them reads `unavailable (no source)`. A `terminalState=released` row is never shown as "done". Help text: "a completed Task can still own a live terminal".

<!-- Source: Base (original, modified) — monotonic clock and 45 s per convergence-r3 Change 6 (INV-023); collection vs evidence freshness per Change 16 -->
- **Stale:** the source is STALE when 3 intervals (45 s at the 15 s cycle) pass with no successful poll, counted on a local monotonic clock. Wall-clock time is used only to print `HH:MM`. The freshness cell then reads `STALE <age>`, and every value keeps its last-known reading with a qualifier `as of HH:MM:SS`. Source loss never closes a question, never changes the open count and never turns any value into `failed`. A failed poll shows `FAILED (<exit code or timeout>) <age>`, and stderr is shown sanitized in the inspector.
- **Collection freshness vs evidence freshness:** "polled 4 s ago" and "worker last reported 20 min ago" are different facts. Source STALE is based on poll success only. A worker's evidence age is shown as a plain age, with no per-row STALE verdict until Orca's timestamp cadence is measured.

<!-- Source: Base (original, modified) — denominator wording preserved; count notation per Change 28 (INV-005); INV-007 disclosure per Change 29 -->
- **Partial pages:** when `page.hasMore` is still true when the per-cycle call cap is reached, the strip reads `PARTIAL: collected n of reported T (newest first; oldest rows not read; long-running active workers may be among them)`. Every derived count then states its denominator, for example `nextAction present: 17 of 300 collected (reported 412)`. The strip shows T from the last page read, as `reported T (page k)`. If `page.total` changed during the traversal it shows `reported T1-T2 (changed during read)`. A finished traversal (`hasMore=false`) where n is not T shows `collected n / reported T (mismatch)`. A page with `workers=[]` while T is above 0 ends the traversal as `PARTIAL (empty page k)`.
- **Filtered vs global counts:** a filter (for example `--terminal-state active`, or a local text filter) always shows `filter <expr>: k of n collected`, next to the unfiltered `source counts: active a / reclaimable r / retained t / released l`. Those source counts are a different scope (terminal accounting), and they are never summed into "workers".

<!-- Source: Variant 3 (haiku:backend), overflow denominator — merged per Change 17; base `x/y shown` wording (taken from C) preserved -->
- **Overflow:** a hidden overflow shows `x/y shown`, and the `+N more` token counts only rows not shown, so the selected visible row is never counted twice.

<!-- Source: Base (original, modified) — 100-row disclosure reworded per Change 24 (candidate verb) and Change 28 (100 rows, not 100 questions) -->
- **The 100-row cap.** (a) `worker-list` returns at most 100 rows per page, and the observer follows `nextCursor` up to the per-cycle call cap. (b) If the candidate `check --all` read is admitted at QUESTION-OBSERVATION, help says it returns at most 100 rows. The question panel title then reads `at most 100 rows per read, not 100 questions; older history not available`. When a retained question drops out of that window, it stays open with `no longer in source window (last seen HH:MM)`.

<!-- Source: Round 2 consensus, Unknowns — merged per Change 28 (question-area wording, INV-005, INV-009); rotation set per Change 32 item 8 -->
- **Question area:** before QUESTION-OBSERVATION it reads `source UNVERIFIED, 0 rows interpreted, not "no questions"`, with no number. No count is ever derived from `result.count`, whose meaning is UNVERIFIED. After the gate the area shows `collected n unique / reported T`. A row that changed while being read carries a `changed during read` note, and a count mismatch carries a mismatch note. Rows that cannot all be read in one cycle rotate, and each scope shows a `revisit ~Ns` token. An empty rotation set reads `message source not read: no eligible scope; coverage unknown`.

<!-- Source: Base (original, modified) — live-mode wording per Round 2 consensus (C-003); test IDs added per Change 2 -->
- **"Seen is not resolved":** the big count in `SEEN IS NOT RESOLVED` is the number of observed open questions; with no question source it reads `unknown (no question source)`. `m` (mark looked) moves an item from `not marked` to `marked looked`, and the big count stays the same. `closed by evidence` shows `unavailable` until a closure source exists (a later release, section 7). No key, timer or source loss can lower the open count. Only explicit closure evidence can, and that is not available in the MVP.
- **Empty states (pinned by T33):** `0 rows interpreted (contract UNVERIFIED)` is not `no questions`. `worker-list returned 0 workers in scope=bound` names the scope, because a bound Run is not the fleet. The fixture variant `empty` must render `no observed items in this source window; not proof none exist`.

<!-- Source: Variant 3 (haiku:backend) — merged per Change 20 (cost) and Change 7 (SETTLED, FROZEN); base policy-frozen rule modified; test ID per Change 2 -->
- **Cost and tokens:** cost renders `cost unavailable`, never `$0`. No progress bar is derived from tokens or from activity.
- **SETTLED and POLICY FROZEN (pinned by T34):** no verified source reports settlement or a policy freeze, so in live mode both render `unavailable (no source)`, never blank or zero. In fixture mode a frozen item keeps a `FROZEN` marker that no other state overrides.

## 5. Deliberately left out

<!-- Source: Base (original, modified) — gate names updated per Change 22 and Change 24; historical-row row per Change 6; `r` row per Change 8; release references renumbered per Change 22 -->
| Left out | Why |
|---|---|
| Any operational control (approve, retry, terminate, spawn, merge, rebase, delete-worktree, worker instruction, reply) | Constraint. The observer has no write path into Orca. The design package's mock-up action buttons are not built. |
| `check` without `--peek`/`--all`, `--ack`, `--wait`, `--retry-request` | Plain `check` and `--ack` consume a delivery. `--wait` returns the bound Run's FIFO delivery and is a listener, not an observation. These sit in a forbidden set that never shrinks (section 9). |
| Parsing `check --peek/--all` or `inbox --json` rows before QUESTION-OBSERVATION | Row fields are UNVERIFIED. `check --all --run <runId> --json` is only a candidate verb behind that gate (section 7), and it needs three UNVERIFIED proofs (section 3). |
| Question age, requester and owner in live mode | They exist only in message rows. `lastObservedAt` is an observation time, not a question open time. |
| Affected-session evidence ledger (C's core) before QUESTION-LINK | It needs authoritative joins from question to dispatch to worktree. Cross-host joins are not established. It ships only behind QUESTION-LINK (R3, section 7). |
| Fleet SIGNALS bars (A's 160-column panel) | Its running/settled/unknown/stale/frozen buckets need a verified mapping from `workerState`/`outcome` to "settled", and there is none. The source-reported COUNTS strip is shown instead, and SETTLED and POLICY FROZEN read `unavailable (no source)` (section 4). |
| Deleting historical rows | Released and retained rows are hidden by default behind `h`, with the count `k historical hidden (h)` always shown. They are never deleted from the snapshot. |
| An `r` (refresh) key | Refresh runs on the fixed 15 s cycle. A manual refresh key would add a second polling path. `m` (since-last-look marker) takes its place in the key list. |
| `--include-remote` | Remote rows have no verified cross-host ownership join. Merging them would invent fleet totals. Off until R4 (section 7). Settled by engineering in section 11. |
| Persisted "last look" across runs | It is local state with no agreed retention or location. Session memory only. Settled by engineering in section 11. |
| Complete message history, cost/usage, admission, revision-pinned verification, durable replay, deep links | Not established (seed brief, `integration-gaps.md`). Never presented as available. |
| Windows keyboard input | The stdlib `termios`/`tty` reader is POSIX-only. On Windows, `--once` prints a text export. |
| Mouse, themes, blinking, animation | Out of scope. No blinking is a constraint. |

## 6. Where A (Signal Bridge) and C (Decision Desk) are stronger

<!-- Source: Base (original, modified) — "B from day one" framing removed per Change 21; R1 recommendation follows the Round 2 consensus (C-001) and convergence-r3 Change 1 -->
**A is stronger on day-one live data.** Every A panel except the request panel can be filled from `worker-list` today: the freshness strip, the worker ledger, and the source-reported counts, provided nothing is derived that the source does not report. Before any question rows can be read, a B screen would be mostly an honest notice and A would show more. A also answers "is the fleet alive?" at a glance. That is why the recommendation for R1, pending the owner's selection record, is A's worker ledger plus the COUNTS strip plus B's one-line question-source gap notice (sections 1 and 2).
- Weakness of A on the root cause: it puts one request on top (`_request` in `signal_bridge`). With 5-10 orchestrators, many questions are open at once, so the single-panel slot repeats the recency bias #409 complains about. That is why the recommendation moves to B once QUESTION-OBSERVATION passes. Its 116- and 80-column builds also drop the SIGNALS panel (seed brief discrepancy), and the built prototype does not match the brief's collapse claim (X-001). The prototype is a visual reference only. The merged width rules come from the consensus (A's width matrix, B's coordinates, C's 44-row contract), not from the prototype.

**C is stronger once one question has been chosen.** C answers "who is affected, and what is the evidence?" for one request, filtering the ledger to the affected IDs only. It also ships the most honest overflow line of the three: `x/y other questions shown`. B needs that same arithmetic, and this design copies it. When the human is about to decide, C is the better screen.
- Weakness of C for an MVP: it needs both unverified contracts at once, message rows and an authoritative mapping from affected ID to dispatch. If either is missing, the desk is empty or shows wrong sessions. It also selects `requests[0]` by default, so the question shown first depends on source order, which is UNVERIFIED (out-of-order events). The recommendation therefore puts C's desk behind QUESTION-LINK only.

<!-- Source: Round 3 (debate-r3-variant-3.md), V3 dissent on C-001 — recorded per Change 21 and refactor-plan "Changes NOT Being Made" -->
**Dissent (V3, Decision Desk):** once explicit-link rows exist, C's Decision Desk should be the post-link composition, not a view beside B. Two of three advocates recommend B as the post-link default with C as a view behind the link gate. This is not settled: the owner's selection record (section 11, decision 1) can pick C, and the optional owner re-confirm at QUESTION-LINK (section 7) exists for exactly this choice.

<!-- Source: Base (original, modified) — gate renamed per Change 22; fallback statement preserved -->
**B's own weakness, stated plainly:** if the message contract never verifies, B's headline panel stays empty forever, and the product turns into A with different labels. The QUESTION-OBSERVATION gate (section 7) is therefore the most important owner action after the selection record. If the owner cannot get that row shape verified, A becomes the better MVP, and this design says so.

## 7. Build order from MVP to later releases

<!-- Source: Variant 3 (haiku:backend), gate vocabulary — merged per Change 18 -->
Each data gate passes only on recorded, redacted samples of four kinds: **success**, **missing**, **stale** and **contradictory**, each pinned in a contract test. Without all four the gate stays closed. If a gate fails, the screen stays on the previous release's view.

<!-- Source: Base (original, restructured) — per Change 22 (DIRECTION-SELECTED first, R0-R4 renumbered), Change 11 (R0 spike and Textual switch rule), Change 24 (candidate verb), Change 29 (INV-022), Change 32 items 1-3 and 7 -->
| Release | Adds | Gate (what must be verified first) |
|---|---|---|
| R0 Fixture replay and design material | Ledger screen, inspector, text export at 160/116/80, sanitizer, cell-width truncation, NO_COLOR, ID-anchored selection, every fixture variant. A redacted golden `worker-list` fixture. A spike of Rich Live with the raw stdlib key reader: if it fails, switch to Textual, and never build both. Render timing and per-call timeouts measured. Renders of A, B and C at 160, 116 and 80 columns, each marked "synthetic fixture, not live evidence", with realistically degraded versions beside them (unavailable, PARTIAL, the gap notice, `read k of N Runs since start`, "bounded best effort", "affected scope unknown"), plus C's walkthrough task "find the oldest question and inspect its evidence". | None from Orca. Offline work only. Fixtures are labelled SYNTHETIC, and the PROPOSED schema is used only inside fixture mode. |
| DIRECTION-SELECTED (a gate, not a release) | Nothing ships. | The owner's dated selection record (below). **This gate has NOT passed: no owner selection exists.** |
| R1 Live worker-list | COUNTS strip, freshness strip, worker ledger with the verbatim `nextAction.kind` column, `result.counts`, capped paging, stale handling, "changes since last look", the view the owner selected | DIRECTION-SELECTED passed, and production integration permitted under the reading the owner confirms (below). `worker-list --json` fields and paging are already verified (seed brief); add a redacted golden sample of each of the four kinds and a contract test that fails on any missing required field (section 9). |
| R2 Question ledger | `OPEN HUMAN QUESTIONS` with observer-side retention, the 100-row disclosure and the label "bounded best effort; coverage unknown" | **QUESTION-OBSERVATION** (below). The candidate verb is used only after it passes. |
| R3 Links and C's decision inspector | For the selected question, the affected sessions with their worker-list evidence (C's Decision Desk) | **QUESTION-LINK**: an authoritative mapping from the IDs in a message to `dispatchId`/`worktreeId`, verified on this host first. Optional owner re-confirm of the post-link default (B or C). |
| R4 Remote fleet | `--include-remote` rows grouped by `projection.host.id` | Cross-host ownership joins. Not established. |
| Later: closure evidence | `closed by evidence` count; closed items move to a closed list | A source that records explicit resolution of a question (for example a reply row linked to the question ID). Not established. |
| Later: history | Questions older than the 100-row window | Durable, non-consuming message history or event replay. Not established. |
| Later | Admission and verification, cost, deep links | Each needs its own feed, none established. |

<!-- Source: Round 3 (debate-r3-variant-1.md DIRECTION-SELECTED; debate-r3-variant-3.md lines 15-24) — merged per Change 22, Change 23 and Change 32 items 1-2 -->
### DIRECTION-SELECTED gate (between R0 and R1)

- **Evidence:** a dated selection record written by the owner, never by an agent. It names the date, the option and who decided, and it says where the owner's statement lives (agents may cite that statement but never write it). It holds the default while no question rows exist, the default after QUESTION-OBSERVATION, the post-link choice or an explicit deferral, a fallback date, the stack confirmation, the command name and the confirmed production-integration reading (section 11).
- **Input:** the R0 renders of A, B and C at 160, 116 and 80 columns, marked "synthetic fixture, not live evidence", with the degraded versions beside them and C's find-and-inspect task.
- **Missing:** no production integration. R0 work continues.
- **Stale:** a later gate that changes what a direction can show triggers a re-confirm. The fallback date passing also triggers a re-confirm. Expiry never grants permission to switch direction.
- **Contradictory:** a selection whose data gate has not passed ships only an owner-accepted gated fallback, with the reason on screen, or stays blocked. An unsupported selection never clears a gate, and a gate is never bypassed to honour a selection.
- **Acceptance:** a reviewer checks that the record exists and is complete (section 10, AC-S). This check is never reported as an automated test.
- **Status:** NOT passed.

<!-- Source: Round 3 (debate-r3-variant-1.md line 32; debate-r3-variant-3.md) — merged per Change 31 and Change 32 item 3 -->
### What "production integration" means here

The issue requires the owner's visual-direction selection before production integration. Two readings exist, and both are UNVERIFIED as the issue's intent:

1. **Reading 1 (V1):** the first change that registers `superclaude observe` in the shipped CLI, or lets the adapter run a live Orca subprocess outside the fake runner.
2. **Reading 2 (V3):** the first change that wires or enables the observer in the shipped product. Separately authorized read-only capture counts as research.

Until the owner confirms one in the selection record, the stricter reading applies: offline work only (R0). All three advocates accept this.

<!-- Source: Round 2 consensus and Round 3 — merged per Change 24 (candidate verb, three proofs), Change 29 (INV-022), Change 32 items 5, 7 and 11; convergence-r3 Change 5 overrides the plan's proof (c) wording -->
### QUESTION-OBSERVATION gate (before R2)

The candidate verb is `orca orchestration check --all --run <runId> --json`. It is a candidate, never an available source, until all of these are recorded:

- **Proof (a), UNVERIFIED:** `--run` narrows `--all`, shown with samples from at least 2 Runs.
- **Proof (b), UNVERIFIED:** which handle receives human-addressed messages, and whether the read works from an unbound observer terminal.
- **Proof (c), UNVERIFIED:** the measured message rate, recorded. A measured rate does not prove completeness, so the question area label stays "bounded best effort; coverage unknown; bursts over 100 rows between reads may be lost" even after the gate passes.
- **Non-consumption (INV-022):** repeated before-and-after readings on a quiet scope show the read does not consume. The test first establishes readable identity fields, because message IDs, the inbox shape and lease fields are UNVERIFIED. Help text and an empty peek `count` alone cannot clear the gate. A pass covers only the visible effects tested.
- **Question identity:** a verified source-scoped question identity is recorded. A worker `dispatchId` is never used as a question's identity.
- **Owner inputs:** the owner names what identifies a human question (section 11, decision 8) and grants acquisition permission for the actual read scope before any call (section 11, decision 6).
- **Budget:** the number of message calls per cycle is an open parameter set by measurement, inside the five-call cap (section 9). V3's default is at most 1.

<!-- Source: Base (original, modified) — fallback rule preserved; deadline expiry narrowed per Change 32 item 2 -->
**Fallback rule:** if QUESTION-OBSERVATION is not verified by the owner's fallback date, the owner re-confirms the direction. If the owner picks A, A becomes the default on the same adapter and renderer. B's retention model stays in the code for when the contract arrives. That costs one layout function, not a rewrite.

## 8. Stack recommendation

<!-- Source: Base (original, modified) — stated as a recommendation pending owner confirmation per Change 23 (owner decision 2) -->
Recommendation, pending owner confirmation: **Python + Rich** in this repository. It departs from the issue's stated preference for Go with Bubble Tea v2, Lip Gloss v2 and Bubbles v2 (MIT), so the owner confirms it (section 11, decision 2). The comparison uses the seed brief's stack table (2026-11-08, primary sources, nothing run).

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

<!-- Source: Base (original) -->
- The two hardest MVP requirements are text export and cell-width truncation, and both are tested headlessly. Rich already does both. Go Charm v2 does neither out of the box, and its NO_COLOR parsing breaks the no-color.org rule, so we would have to override it anyway.
- Rich's one real gap is keyboard input: a small stdlib reader, POSIX-only, needed for the navigation keys and `/ h m e q`. That reader is new non-trivial code and gets its own tests. It costs less than a new language toolchain and binary pipeline.

<!-- Source: Base (original, modified) — one view model, two renderers per Change 3 and convergence-r3 Change 7 -->
- **One view model, two renderers.** The collector produces a snapshot; a pure function builds one view model from it. Two renderers read that view model: `render(view, W)` draws the interactive screen and is bounded by width, and `export(view)` writes the `e`/`--once` record form, which is lossless for every value the export permission allows and carries full IDs. Tests assert on the view model and on each renderer separately. A later Go port re-implements this small, test-pinned surface and does not need to rediscover behaviour.

<!-- Source: Variant 1 (opus:architect), truncation marker and ASCII mode — merged per Change 9 -->
- **Export and terminal rules:** the screen renderer truncates by cells with a single visible `>` marker, which survives ASCII output. `--ascii` selects the ASCII path for non-UTF-8 terminals. The record export does not truncate.

<!-- Source: Variant 1 (opus:architect), placement and switch rule — merged per Change 11; command name is an owner decision per Change 23 -->
- **Placement:** the MVP lives in this Python repository as a `click` subcommand registered like the others in `cli/main.py` (deferred import, then `add_command`). The recommended name is `superclaude observe`; the name is the owner's choice (section 11, decision 3). Registering it in the shipped CLI is production integration under reading 1 (section 7).
- **Switch rule:** the R0 spike tests Rich Live with the raw key reader. If the spike fails, switch to Textual. Never build both. Textual is not first because of its maintenance risk and its UNVERIFIED plain-text export.

<!-- Source: Base (original, modified) — sanitizer provenance replaced by "sanitizer of our own" per Change 19 -->
- **Licensing and reuse:** TUIBBS-scp is AGPL, so no code is copied from it, whatever the stack. The sanitizer is written in the observer package. The design package's prototype `canvas.py` is never imported by production code; it stays a visual reference only.

## 9. Smallest trustworthy read-only adapter

<!-- Source: Base (original, modified) — scope extended for the gated R2 candidate verb per Change 24 -->
**Scope:** in R0 nothing runs against Orca. In R1 there is one verb, `orca orchestration worker-list --json --limit 100` with optional `--run <runId>` and `--cursor <c>`. The candidate message verb (section 7) enters the allow-list only after QUESTION-OBSERVATION passes.

<!-- Source: Round 2 consensus, Data adapter — merged per Change 27; Variant 1 (opus:architect) snapshot model per Change 5 -->
- **Structure:** an `observe` package. Each call returns a `SourceResult` (ok, failed or partial, with the parsed data and a sanitized diagnostic). A single-flight collector runs one cycle at a time and publishes each snapshot atomically, tagged with a monotonic cycle number, so snapshots are ordered without trusting wall clocks. There are two seams: the collector seam (the subprocess runner, replaced by a fake runner in tests) and the view seam (a pure function from a snapshot to the view model, section 8).

<!-- Source: Base (original) -->
- **Binary discovery:** reuse `_find_orca()` (`cli/install_user_setup.py`). It tries `orca-ide`, then `orca`, and validates with `skills list --json` so that the GNOME screen reader named `orca` is rejected, with a 10 s timeout. If no binary is found, the freshness cell reads `worker-list NOT AVAILABLE (orca binary not found)`. That is not shown as an empty fleet.

<!-- Source: Base (original, modified) — hardened per Change 25 (INV-004), qualified per Change 32 item 6 -->
- **Argv allow-list:** argv is built from exact templates only. The R1 template is `(orca, "orchestration", "worker-list", "--json", "--limit", "100")`, plus an optional `("--run", runId)` and an optional `("--cursor", value)`. Following a cursor goes through a guard that marks the view PARTIAL when the per-cycle cap stops it. `--include-remote` is not in the allow-list until R4. Calls go through `subprocess.run` with a list and no shell.
  - **Forbidden set:** prefix-matched, and it never shrinks: plain `check` (without `--peek`/`--all`), `--ack`, `--wait`, `--retry-request`, `dispatch`, `inbox`, and any other verb.
  - **Values:** `runId` gets a format check. The cursor is copied unchanged from `page.nextCursor`, as the help requires; it is bounded by bytes and passed as its own argument, not checked against an inferred grammar. Any value that starts with `-` is rejected. V1's numeric bounds and regexes are PROPOSED, not verified Orca formats.
  - **Form:** flags and values are separate arguments. The `--opt=value` form is used only after Orca's parser support is recorded.
  - **Test seam:** a fake runner fails the test if it is reached with an argv that is not in the allow-list.

<!-- Source: Variant 3 (haiku:backend), per-cycle caps — replaces base polling bounds per Change 14; convergence-r3 Change 6; Change 32 item 7 -->
- **Bounds per cycle:** the interval is 15 s, and the cycle budget equals the interval. A cycle runs at most 5 subprocesses, and each call's output is capped at 8 MiB. A call that overruns is killed and reaped, and the strip shows `cycle overran (Ns)`. After failures the interval backs off, up to 60 s. The per-call timeout is measured in R0, not guessed; until then its value is UNVERIFIED. The source is STALE after 3 intervals (45 s) with no success, counted on a local monotonic clock. The number of message calls per cycle is an open parameter set by measurement; V3's default is at most 1. Cycles never overlap. The poll runs in a daemon thread and waits on a `threading.Event`, mirroring `sprint/monitor.py` `OutputMonitor`. There is no LLM in the loop. The earlier 30 s cycle deadline is withdrawn.

<!-- Source: Base (original, modified) — required and optional fields per Change 27 (INV-003) -->
- **Parsing:** JSON only, from stdout, and exactly one JSON envelope per call. Required fields: `result`, `result.workers` and `result.page.hasMore`. If any is missing, the cycle counts as `FAILED (shape)` and the last good snapshot is kept. Optional fields: `result.scope` (absent reads `scope unknown`) and `page.total` (absent reads `reported unknown`). V1 holds that `page.total` should be required; that open disagreement is recorded in section 12. Each row is read field by field with absent-tolerant access, and a missing key becomes `UNKNOWN`, a sentinel that is not `None`, 0 or `False`. Unknown extra keys are ignored and counted in the inspector (`n unrecognised keys`).

<!-- Source: Base (original, modified) — identity and clocks per Change 13 (INV-002); question identity per Change 32 item 11 -->
- **Identity, duplicates and order:** a row's identity is its source namespace plus `dispatchId`, so rows from two hosts or Runs never merge. Each component keeps its own clock. Rows are deduplicated by identity within a cycle. Across cycles, the row with the newer `projection.liveness.observedAt` (or `evidence.lastObservedAt`) wins. If either timestamp is absent, the newer cycle wins and the row is flagged `order unknown`. A timestamp that moves backward shows `conflict (time went back)`. Each dropped duplicate is counted (`k duplicate rows ignored`). Questions are identified only by a verified source-scoped question identity, never by a worker `dispatchId`.

<!-- Source: Base (original, modified) — paging notes aligned to section 4 (Change 28, INV-005) -->
- **Paging integrity:** the cursor is opaque and never built by hand. If `page.total` changes between pages of one cycle, the strip shows `reported T1-T2 (changed during read)`. A page with no workers while T is above 0 ends the traversal as `PARTIAL (empty page k)`.

<!-- Source: Base (original, modified) — STALE timing per Change 14 -->
- **Error and stale handling:** a non-zero exit, a timeout or invalid JSON marks the source `FAILED` for that cycle. The last good snapshot stays on screen, qualified `as of`. After 3 missed intervals (45 s, monotonic) the source shows `STALE`. Stderr is sanitized and kept to 2 KiB for the inspector.

<!-- Source: Base (original, modified) — sanitizer of our own and literal rendering per Change 19 -->
- **Sanitizing at the trust boundary:** every string from the source passes the observer's own sanitizer before it reaches the model. The sanitizer removes CSI/OSC sequences (terminated and unterminated), 8-bit C1 controls, bare C0 controls except newline in the inspector, and Unicode Cf format characters. It is at least as strict as the prototype's `canvas.py` `sanitize`, which stays a reference only; `pty_stream.py` `ANSI_ESCAPE_RE` is too weak, per the seed brief. Every string is rendered as literal text, never parsed as Rich markup. Truncation uses `rich.cells.cell_len`, never `len()`.

<!-- Source: Round 2 consensus, Retention — merged per Change 26; overflow notation per convergence-r3 Change 9 (Change 32 item 10) -->
- **Question retention (R2 onward):** each question is kept until closure evidence is seen. Retention is bounded at 1,000 records. Eviction never lowers the open total. When the bound is exceeded, the count reads `unknown (retention exceeded)` with the retained count beside it; overflow is never shown as closed. Questions list oldest first.

<!-- Source: Round 3 (debate-r3-variant-3.md, INV-009) — merged per Change 32 item 8 -->
- **Rotation set (R2 onward):** the scopes read for messages are the permissioned scopes from the configured set, the discovered non-historical worker scopes and the scopes of retained questions, deduplicated. Scopes that do not fit in one cycle rotate, each with a `revisit ~Ns` token. An empty set reads `message source not read: no eligible scope; coverage unknown`.

<!-- Source: Round 3 (debate-r3-variant-3.md, INV-017) — merged per Change 29 and Change 32 item 4; convergence-r3 Change 8 overrides the plan's "dropped before rendering" wording -->
- **Acquisition permission (R2 onward):** permission must cover the actual read scope before a message call, separately from display permission and export permission. Dropping a body at parse time cannot undo its receipt into the stdout buffer, so this design never claims that unauthorized bodies were not acquired. If a narrow read cannot honour the permission, the call is skipped. Raw output never enters logs, fixtures or exports. Run-wide consent is not substituted for terminal consent while the terminal-attribution fields are UNVERIFIED.

<!-- Source: Round 3 (debate-r3-variant-2.md, INV-007) — accepted risk per Change 29 -->
- **Rows that drop out (INV-007, accepted risk):** rows seen this session that drop out of the source stay listed as `not reobserved`, and the strip discloses `oldest rows not read; long-running active workers may be among them` (section 4). Whether `worker-list` offers a state filter is UNVERIFIED.

<!-- Source: Round 2 consensus, A-008 — label QUALIFY (V3 dissent: REJECT), per convergence-r3 Per-Point table -->
- **Several observers (A-008, label QUALIFY):** the caps above are per observer process, and help and the inspector say so. There is no singleton lock, so several observers multiply the load on Orca. Any restriction is an owner decision (section 11, decision 9). V3 labels this point REJECT; that dissent is recorded in section 12.

<!-- Source: Base (original, modified) — "scope unknown" per Change 27; Runs-read header per Change 21 (INV-021) -->
- **Scope honesty:** `result.scope.source` (`flag`, `bound` or `all`, per help) is shown in the header; if it is absent the header reads `scope unknown`. If the value is `bound`, the header adds `one Run only`. The header also shows `read k of N Runs since start`.

## 10. MVP acceptance tests

<!-- Source: Base (original) — mapping caveat preserved -->
The acceptance criteria below (AC-1 to AC-10) are restated from the seed brief's Problem, Constraints and Success Criteria. The issue text was not re-read, so this mapping is UNVERIFIED against #409.

<!-- Source: Base (original, modified) — harness per Change 30 (recorded console, fake runner, golden sample) -->
Harness: render with `Console(width=W, record=True, color_system=None or "standard")` and read `export_text()`. The adapter runs against a fake runner that returns recorded JSON from the redacted golden sample. No TTY and no live Orca are needed. Fixture variants are the package's: `base`, `uneven`, `shared-unmapped`, `historical`, `long-identifiers`, `source-loss`, `missing-fields`, `duplicate-out-of-order`, `empty`, `injection`.

<!-- Source: Base (original, modified) — T1, T2, T4, T5, T9, T13, T15, T18, T19, T21-T24, T27, T31, T32 modified per Changes 1, 3, 6, 9, 13, 14, 20, 24, 25, 27, 28 (see merge-log) -->
| AC | Requirement | Tests |
|---|---|---|
| AC-1 | Read-only, no consuming check | T1: argv allow-list. Across every adapter code path, argv equals one of the exact templates in section 9. T2: a static test that `--ack`, `--wait` and `--retry-request` do not appear in the adapter module, and that `check` appears only in the gated R2 template. T3: no key binding maps to an Orca call. |
| AC-2 | Deterministic, bounded collection | T4: with a fake that always says `hasMore=true`, a cycle stops at the 5-call cap and renders `PARTIAL: collected 500 of reported T`. T5: a fake that sleeps past the measured per-call timeout shows `FAILED (timeout)`, and the cycle ends within the 15 s cycle budget. T6: the same input renders byte-identical text twice. |
| AC-3 | Attention items with reasons, scope, changes since last look, evidence | T7: `base` (8 orchestrators, 80 sessions) in fixture mode lists every question oldest first with requester/owner and affected IDs. T8: after `m`, a fixture step that changes one `nextAction.kind` marks exactly that row `*`, and `changed since (1)` appears. T9: in live mode with no message source, the question area shows `0 rows interpreted (contract UNVERIFIED)`, and the worker ledger is titled `worker-reported, not questions`. |
| AC-4 | Seen is not resolved | T10: pressing `m` on every item leaves the big open count unchanged. T11: the `source-loss` variant keeps the open count and every retained item. Nothing becomes resolved or failed. T12: an item missing from the next cycle stays, marked `no longer in source window`. |
| AC-5 | Lifecycle, outcome, report, acceptance, tests and approval kept separate; unknown is never 0 or false | T13: `missing-fields` renders `unknown` for every absent field, and the strings `0` and `false` never stand in for one (asserted per field). T14: a row with `terminalState=released` and `outcome` absent never renders `done`, `complete` or `settled`. T15: report, acceptance, tests and approval each render `unavailable (no source)` in live mode. |
| AC-6 | Filtered and global counts with denominators; the 100-row cap disclosed | T16: the scenario matrix {5, 8, 10 orchestrators} x {50, 80, 100 sessions} x {160, 116, 80 columns} (27 renders). Every count line matches `k of n`, and every hidden overflow shows `x/y shown`, with y equal to the fixture total. T17: `uneven` (one orchestrator owns most sessions) keeps per-owner counts that sum to the global count. T18: a fake with `page.total=287` and 100 rows shows `collected 100 / reported 287`, never `287 workers`; with `page.total` absent it shows `reported unknown`. T19 (R2 placeholder, skipped until QUESTION-OBSERVATION passes): the question panel title contains `at most 100 rows per read, not 100 questions` and the label `bounded best effort; coverage unknown`. |
| AC-7 | No one-to-one session/worktree assumption | T20: `shared-unmapped` shows two sessions sharing one `worktreeId` as two rows that each name the worktree, and a session with no worktree as `worktree unknown`. No count divides one by the other. |
| AC-8 | Historical records, duplicates, out-of-order events | T21: `historical` rows (released or retained) are hidden by default with `k historical hidden (h)`; after `h` they are listed with their `terminalState` and are not counted as active. T22: `duplicate-out-of-order` shows `k duplicate rows ignored`, an older `observedAt` never overwrites a newer one, a row missing both timestamps is flagged `order unknown`, and a timestamp that moves backward shows `conflict (time went back)`. |
| AC-9 | Widths, keyboard, NO_COLOR, export, full IDs, no blinking | T23: at 160, 116 and 80 columns, every line of the screen renderer has `cell_len <= W`. T24: `long-identifiers` truncates with `>` in lists, while the inspector shows the full ID. T25: a reorder between cycles keeps the selection on the same row ID. T26: `NO_COLOR=1` and `NO_COLOR=yes` both produce output with no SGR colour codes, and the meaning is still readable (`STALE` and `unknown` are words, not colours). T27: `e`/`--once` writes the record export: no ESC byte, full IDs, no truncation. T28: the blink attribute (SGR 5/6) never appears. |
| AC-10 | Sanitize untrusted text; cell-width truncation | T29: `injection` (CSI, OSC 8 hyperlink, unterminated OSC, 8-bit C1 `\x9b`, BEL, a bidi Cf character such as U+202E, and a terminal title set) leaves no ESC, C1 or Cf byte in the rendered or exported output. T30: CJK and emoji identifiers are truncated by cells, so no line overflows and no double-width character is split. T31: cost renders `cost unavailable`, never `$0`, and no progress value comes from tokens or activity. |
| Contract | Shape of the worker-list source | T32: the redacted golden `worker-list --json` sample parses. Removing `result`, `result.workers` or `result.page.hasMore` produces `FAILED (shape)` with the last good snapshot kept. Removing `result.scope` shows `scope unknown`; removing `page.total` shows `reported unknown`. Removing an inner `projection.*` field produces `unknown`, not an error. |

<!-- Source: Merge — tests added after T32 per Change 30, drawn from Changes 2, 3, 4, 10, 12-17, 19, 21, 25, 26, 28 and Change 32 items 2, 5, 9, 10 -->
### Tests added after T32

| Test | Pins | AC |
|---|---|---|
| T33 | The `empty` variant renders `no observed items in this source window; not proof none exist`, never `no questions` (Change 2). | AC-3 |
| T34 | Policy frozen renders `FROZEN` in fixture mode, and SETTLED and POLICY FROZEN render `unavailable (no source)` in live mode, never blank or zero (Changes 2, 7). | AC-5 |
| T35 | The COUNTS strip appears at 80, 116 and 160 columns; priority tokens are never truncated; below 80 columns the screen reads `terminal too narrow (min 80)` (Change 4). | AC-9 |
| T36 | The adapter runs with the real subprocess call patched to raise, so any unlisted argv fails loudly; `NO_COLOR=yes` and the colour-enabled case are both pinned (Change 10). | AC-1, AC-9 |
| T37 | Argv validation: a value starting with `-`, a malformed `runId` and every forbidden prefix are rejected; the fake runner fails on an unlisted argv (Change 25). | AC-1 |
| T38 | An aggregate with k unknown members renders `n+? (k unknown)`, never a clean `n` (Change 12). | AC-5 |
| T39 | Two rows with the same `dispatchId` from different source namespaces stay two rows (Change 13). | AC-8 |
| T40 | With a fake monotonic clock: STALE at 45 s without success, unaffected by wall-clock jumps; backoff reaches 60 s and no further; an overrunning call is killed and the strip shows `cycle overran (Ns)` (Change 14). | AC-2 |
| T41 | The first observation is the baseline with no change flags; a row that drops out of the source shows `not reobserved` (Change 15). | AC-3 |
| T42 | A successful poll with old worker evidence shows the poll age and the evidence age separately, and does not mark the source STALE (Change 16). | AC-5 |
| T43 | With the selected row visible and others hidden, `+N more` excludes the selected row (Change 17). | AC-6 |
| T44 | Worker text containing Rich markup (for example `[bold]`) renders literally (Change 19). | AC-10 |
| T45 | The default view is chosen at start-up and never switches mid-session; the header shows `read k of N Runs since start` (Change 21). | AC-3 |
| T46 | At 1,001 retained questions, eviction does not lower the open total, the count reads `unknown (retention exceeded)` with the retained count, and questions stay oldest first (Change 26, Change 32 item 10). | AC-4 |
| T47 | Before QUESTION-OBSERVATION the question area reads `source UNVERIFIED, 0 rows interpreted, not "no questions"`; no count comes from `result.count`; the `changed during read`, mismatch, `revisit ~Ns` and empty-rotation-set notes render as in section 4 (Change 28). | AC-3, AC-6 |
| T48 | The screen renderer and the record export read the same view model; an ID the screen truncates with `>` appears in full in the export (Change 3). | AC-9 |
| T49 | When the height cannot hold coverage, scope and PARTIAL ahead of optional panels, a too-small diagnostic is shown (Change 32 item 9). | AC-9 |
| T50 | R0 renders of A, B and C at 160, 116 and 80 columns each carry "synthetic fixture, not live evidence", with a degraded version beside each (Change 32 item 2). | AC-S input |
| T51 | R2 placeholder, skipped until the gate: the quiet-scope side-effect test first establishes readable identity fields, then repeats before-and-after readings; a pass covers only the visible effects tested (Change 32 item 5, INV-022). | AC-1 |

<!-- Source: Round 3 (debate-r3-variant-1.md; convergence-r3 S-006) — reviewer-checked AC per Change 23 -->
### Reviewer-checked and manual checks (not automated tests)

- **AC-S (selection record):** a reviewer checks that the owner's dated selection record exists and names the date, the option, who decided, where the owner's statement lives, the pre-observation default, the post-observation default and the post-link choice or deferral (section 7). It is never reported as an automated test, and no agent writes the record.
- **Manual CJK check:** one run in a real terminal confirms that a CJK identifier is truncated by cells as T30 asserts headlessly. It is reported as a manual check, not a test pass.

## 11. Open owner decisions

<!-- Source: Round 3 (debate-r3-variant-2.md line 71, owner-list rule) — merged per Change 23 -->
**Owner-list rule.** A decision belongs on this list if only a human can decide it, the issue assigns it to a human, or the recommendation departs from a preference the issue states. Each decision carries a recommendation; none is settled until the owner records it.

<!-- Source: Base (original, restructured) — per Change 23 (INV-019), Change 31, Change 32 items 1-3; base decisions 1, 2, 3, 5, 6, 12 kept, decisions 7, 8, 9 added from Round 3 -->
1. **Visual direction (the issue requires it before production integration).** Written by the owner as a dated selection record (date, option, who, and where the statement lives), never by an agent. It names (a) the default while no question rows exist, (b) the default after QUESTION-OBSERVATION and (c) the post-link choice or an explicit deferral. The owner reviews the R0 renders of A, B and C at 160, 116 and 80 columns, marked "synthetic fixture, not live evidence", each beside its degraded state (gap notice, `read k of N Runs since start`, "bounded best effort", "affected scope unknown"), with the walkthrough task "find the oldest question and inspect its evidence". Recommendation: A's worker ledger plus the COUNTS strip for R1; B after QUESTION-OBSERVATION, with A one key away; C behind QUESTION-LINK. V3 dissents and recommends C as the post-link composition (section 6). This is the DIRECTION-SELECTED gate (section 7), which has NOT passed.
2. **Stack confirmation.** Recommend Python + Rich in this repository, with one view model and two renderers so a Go Charm v2 port stays possible. This departs from the issue's stated Go Bubble Tea v2 preference, so the owner confirms it. Choose Go only if a separate distributable binary is itself a goal.
3. **Command name and placement.** Recommend a `superclaude` subcommand registered like the others in `cli/main.py` (deferred import, then `add_command`). Recommended name: `superclaude observe`. The name is the owner's choice.
4. **Production-integration boundary.** Two UNVERIFIED readings (section 7): V1's (registering the command, or any live Orca subprocess outside the fake runner) and V3's (first wiring or enabling in the shipped product, with authorized read-only capture as research). Until the owner confirms one, the stricter reading applies: offline only.
5. **Fallback deadline.** The owner sets the date by which QUESTION-OBSERVATION must pass. When it passes, the owner re-confirms the direction; expiry never grants permission to switch. Recommend A on the same adapter as the re-confirm option (section 7).
6. **Sample capture and acquisition permission.** Permission to capture one non-empty sample from the candidate `check --all` read for the QUESTION-OBSERVATION contract, redacted before commit, because message bodies may hold sensitive content. Acquisition permission must cover the actual read scope before any message call, separately from display and export permission (section 9). Recommend yes, with redaction rules set by the owner. This is the decision that unblocks B's headline panel.
7. **Message-content exposure.** What message content may be displayed on screen and what may be exported. The debate makes no recommendation beyond keeping display and export as separate permissions; the owner sets the policy.
8. **Question-type choices.** What makes a message a "human question", which `type` values are accepted, and which handle or Run carries it. This needs an answer from the owner or from Orca. Recommend agreeing on an explicit message type, and not inferring one from text.
9. **Multi-observer restriction.** Caps are per observer process and there is no singleton (section 9). Recommend disclosure only; any restriction on running several observers is the owner's call.

<!-- Source: Base (original, modified) — base decisions 4, 7, 8, 9, 10, 11 moved here per the owner-list rule (Change 23); polling bounds updated per Change 14 -->
### Settled by engineering under the owner-list rule (not owner votes)

- **Fixture replay before the live adapter:** yes. R0 proves every rendering invariant with no Orca dependency (base decision 4).
- **The 100-row window for the question panel:** accepted with the section 4 disclosure and observer-side retention, until a durable history source exists (base decision 7).
- **`--include-remote` default:** off until cross-host ownership joins are verified, at R4 (base decision 8).
- **Persisting "last look" across runs:** not in the MVP; session memory only (base decision 9).
- **Polling bounds:** 15 s cycle, at most 5 subprocesses per cycle, STALE after 3 intervals (45 s, monotonic), per-call timeout measured in R0, message calls per cycle set by measurement (base decision 10, updated per section 9).
- **Platform support:** POSIX interactive mode plus `--once` text export on every platform for the MVP (base decision 11).

## 12. Risks and UNVERIFIED items

<!-- Source: Base (original, modified) — risks, dissents and UNVERIFIED list per Changes 24, 27, 29 and Change 32 items 3, 12, 13; convergence-r3.md -->

### Risks

<!-- Source: Base (original, modified) — decision references renumbered per Change 23; proxy-panel row per Change 1; retention row per Change 26; rows for INV-007, INV-017, INV-022 added per Change 29 -->
| Risk | Effect | Mitigation |
|---|---|---|
| The message row contract never verifies | B's headline panel stays empty, and the product becomes a relabelled A | Owner decision 6 (capture permission) and decision 5 (fallback deadline). The adapter and renderer are shared, so switching costs one layout. |
| A user reads the worker ledger as "questions" | False sense that human attention is covered | The ledger is titled `worker-reported, not questions`, the gap notice sits above it, and T9 pins both. |
| `page.total` includes historical dispatches | Denominators look larger than the live fleet | Label it `reported T`, and show `result.counts` separately (T18). |
| Bound scope shows one Run as if it were the fleet | Missed orchestrators | Show `scope.source` in the header, plus the `one Run only` qualifier, and `read k of N Runs since start`. |
| The hand-written key reader misbehaves (terminal modes, signals) | Terminal left in raw mode | Restore in `finally` and on SIGINT/SIGTERM. The `--once` path needs no raw mode. The R0 spike decides; Textual is the switch-rule fallback. |
| Sanitizer gaps | Escape-sequence injection from worker text | The observer's own allow-printable sanitizer at the adapter boundary, literal text rendering, tested against the `injection` fixture (T29, T44). |
| Observer-local retention grows without limit in a long session | Memory, and a cluttered list | Bound of 1,000 records; past it the count reads `unknown (retention exceeded)` with the retained count. Never dropped silently, and eviction never lowers the open total (T46). |
| Fixture schema mistaken for an Orca API | Code that couples to PROPOSED fields | Fixture mode is a separate loader. The live model is built only from the fields in section 3. |
| `_find_orca()` lives in `install_user_setup.py` | An observer import that pulls in installer code | Import it as is in the MVP. Moving it to a shared module is a separate, owner-approved refactor. |
| Oldest rows not read when paging stops at the cap (INV-007, accepted risk) | Long-running active workers may be missed | The strip says `oldest rows not read; long-running active workers may be among them`; rows seen earlier stay as `not reobserved`. Whether a state filter exists is UNVERIFIED. |
| Message bodies acquired without permission (INV-017) | Sensitive content received into the stdout buffer | Acquisition permission is checked before the call; the call is skipped if a narrow read cannot honour it; raw output never enters logs, fixtures or exports (section 9). |
| The "non-consuming" read consumes after all (INV-022) | Deliveries lost to their real recipients | The quiet-scope before-and-after test is part of QUESTION-OBSERVATION (section 7, T51). |

<!-- Source: convergence-r3.md Per-Point Final Positions and Summary — dissents recorded per Change 27 and Change 32 items 3, 12, 13 -->
### Open disagreements and dissents

- **`page.total` (C-008 / A-003, 2 of 3):** V1 holds that `page.total` must be a required field and that a response without it is rejected. The merge keeps it optional and renders `reported unknown`, because rejecting the envelope would hide the workers that were returned.
- **Post-link default (C-001, 2 of 3):** V3 recommends C's Decision Desk as the post-link composition. The owner decides (section 11, decision 1).
- **A-008 label (2 of 3):** V1 and V2 label it QUALIFY; V3 labels it REJECT. The merge applies QUALIFY: caps are per process and disclosed, with no singleton.
- **Message calls per cycle (C-002 / X-007, 2 of 3):** an open parameter set by measurement. V3's default is at most 1.
- **Production-integration boundary (S-007, 2 of 3):** V1's reading and V3's reading are both UNVERIFIED; the stricter one applies until the owner confirms (section 7).

<!-- Source: invariant-probe.md and convergence-r3.md Invariant Gate Re-Check — count note -->
### Notes on the debate record

- **Invariant probe count:** the probe recorded 16 MEDIUM findings. The Round 3 advocate texts refer to 14, which is the number left unaddressed after Round 2. Both counts are correct for what they describe; the advocate texts are not altered.
- **X-001:** the design package's prototype does not match the seed brief's claim that Signal Bridge collapses at 116 columns. The prototype is a visual reference only.
- **DIRECTION-SELECTED has NOT passed.** The design defect behind INV-019 is resolved, but no owner selection record exists.

### UNVERIFIED items (not to be presented as available)

<!-- Source: Base (original, modified) — reworded per Change 24 (candidate verb, three proofs); state-filter item per Change 29 -->
- Verified today: only `worker-list --json` (`result.workers[]`, `result.page.{limit,total,hasMore,nextCursor}`) and the non-consuming `check --peek` / `check --all` reads, capped at 100 rows. Plain `check` consumes deliveries, so the observer never calls it.
- Row fields of `check --peek` and `check --all`, and the whole JSON shape of `inbox --json`. The only shape seen is an empty peek, `result.{count,dispatchId,runId}`.
- The meaning of `result.count` in check output: rows returned, or unread total.
- The three proofs for the candidate verb `check --all --run <runId> --json`: (a) whether `--run` narrows `--all`; (b) which handle receives human-addressed messages, and whether the read works from an unbound observer terminal; (c) the measured message rate. Even with all three, coverage stays unknown.
- Whether any `--types` value (for example `escalation`, seen only as a help example) identifies a human question.
- Message IDs, lease fields and terminal-attribution fields.
- The value set and meaning of `projection.nextAction.kind`, of `projection.stage.*` and of `projection.evidence.durable`.
- Whether `page.total` counts historical dispatches, and the exact semantics of `result.counts` relative to the rows in the page.
- Whether `worker-list` offers a state filter.
- Whether `projection.liveness.observedAt` and `evidence.lastObservedAt` share a clock or a timezone format (assumed ISO-8601; to be checked against the golden sample).
- The per-call timeout value (measured in R0) and Orca's support for the `--opt=value` form.
- Which reading of "production integration" the issue intends.
- Not established at all: complete message history beyond 100 rows; authoritative cross-host owner/task/session/worktree joins; admission and revision-pinned verification feeds and human-owner linkage; cost/usage accounting; durable event replay and ordering; native deep links.
- Stack facts from the seed brief table (versions, Textual text export, Charm wide-character width) were researched but not run here.
- The AC-1 to AC-10 mapping comes from the seed brief, not from a fresh read of the #409 text.
