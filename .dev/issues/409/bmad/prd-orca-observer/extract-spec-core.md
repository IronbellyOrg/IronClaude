# Extract: spec core (orca-observer)

Source folder: `_bmad-output/specs/spec-orca-observer/`. Files read: SPEC.md (113 lines), acceptance-tests.md (54), rendering-rules.md (88), stack.md (28), adapter-contract.md (63). Quotes are verbatim; `file:line` cites the source line. Notes marked `[extractor]` are mine, not source text.

## 1. Product statement, users, scale, jobs

- Title: "Orca Read-Only Terminal Observer (IronbellyOrg/IronClaude issue 409)" (SPEC.md:22)
- Users and scale: "One human supervising 5-10 Orca orchestrators and 50-100 sessions/worktrees loses human questions in recency-ordered chat, and \"read\" gets treated as \"handled\"." (SPEC.md:26)
- Source limits: "Orca's non-consuming reads keep little history (`check --peek` returns unread messages only; `check --all` is capped at 100 rows), so an honest view must keep every observed question until explicit closure evidence appears, and must say plainly what it cannot see." (SPEC.md:26)
- Product statement: "The observer is a read-only terminal companion that separates verified outcomes from activity and discloses unknown, stale, unavailable and partial data instead of implying completeness. Orca and coordinator policies keep authority." (SPEC.md:26)
- Success signal: "In R1, replaying the redacted golden `worker-list` samples through the fake runner (and live once the owner clears the integration boundary), a supervisor sees on one screen collected/reported, freshness, scope, the worker ledger and the explicit \"questions not observed\" notice, the JSON snapshot passes its schema test, and the argv log shows only the allow-listed `worker-list` calls and the one discovery probe." (SPEC.md:89)
- Jobs: `[extractor]` no separate "jobs" section exists; jobs are the CAP intents in section 2. Questions the views answer: A "answers \"is the fleet alive?\" at a glance" (rendering-rules.md:85); C "answers \"who is affected, and what is the evidence?\"" (rendering-rules.md:86).
- Assumptions (SPEC.md:93-95): "The AC-1..AC-10 to test mapping comes from the seed brief via the merged requirements, not a fresh read of the issue's acceptance list." / "Orca timestamps (`liveness.observedAt`, `evidence.lastObservedAt`) are ISO-8601 on one clock; UNVERIFIED." / "Stack-table facts in `stack.md` were researched from primary sources but not run (UNVERIFIED)."

## 2. Capabilities

`[extractor]` SPEC.md gives no per-CAP evidence label; "Release" is quoted from the intent wording, else "not stated" (no CAP is labelled B or C; views A/B/C are in section 4).

| CAP | Release | Intent (verbatim) | Evidence label | Cite |
|---|---|---|---|---|
| CAP-1 | R0 ("synthetic fixtures (R0)") | "A reviewer can replay synthetic fixtures (R0) to see the Signal Bridge, Attention Ledger and Decision Desk directions at 160, 116 and 80 columns, each with realistic degraded versions, before any live Orca call." | none stated | SPEC.md:31 |
| CAP-2 | R1 ("verified `worker-list` source (R1)") | "A supervisor can see one ledger row per worker dispatch from the verified `worker-list` source (R1), with lifecycle fields, outcome, `nextAction.kind`, liveness and evidence age shown raw." | source called "verified" | SPEC.md:34 |
| CAP-3 | R1 ("not observed in R1") | "A supervisor is told, above the ledger, that human questions are not observed in R1, so an empty screen is never read as \"no questions\"." | question source UNVERIFIED (SPEC.md:38) | SPEC.md:37 |
| CAP-4 | not stated | "A supervisor can tell how complete and how fresh every fact is: known, unknown, unavailable or stale; collected versus reported; scope; poll age versus evidence age." | none stated | SPEC.md:40 |
| CAP-5 | not stated | "A supervisor sees lifecycle, outcome, report status, acceptance, current tests and human approval as separate facts, and nothing is inferred from missing evidence." | none stated | SPEC.md:43 |
| CAP-6 | not stated | "A supervisor can select a row and inspect its full evidence, with selection anchored to identity rather than position." | none stated | SPEC.md:46 |
| CAP-7 | not stated | "A supervisor can see what changed since they last looked within a session." | none stated | SPEC.md:49 |
| CAP-8 | not stated | "Untrusted source text cannot corrupt the terminal, and the view stays legible at 160, 116 and 80 columns, under NO_COLOR and in ASCII." | none stated | SPEC.md:52 |
| CAP-9 | not stated | "A user on any platform can get a readable plain-text export of the same view the screen shows." | none stated | SPEC.md:55 |
| CAP-10 | R1 ("Each R1 cycle") | "Each R1 cycle can write a versioned, additive-only JSON snapshot of the view so a later read-only Go screen inside TUIBBS can read it without depending on the Python code." | none stated | SPEC.md:58 |
| CAP-11 | R2 ("After QUESTION-OBSERVATION passes (R2)") | "After QUESTION-OBSERVATION passes (R2), a supervisor sees every observed open human question retained until explicit closure evidence, with \"seen is not resolved\"." | gated | SPEC.md:61 |
| CAP-12 | R3 ("After QUESTION-LINK passes (R3)") | "After QUESTION-LINK passes (R3), a supervisor can see, for one selected question, the affected sessions with their worker-list evidence (Decision Desk)." | mapping must be "verified on this host" (SPEC.md:65) | SPEC.md:64 |

Release scope of views: "Recorded owner decision 1: R1 = A's worker ledger + COUNTS strip + B's one-line question-source gap notice; B after QUESTION-OBSERVATION with A's ledger one key away; C only behind QUESTION-LINK." (rendering-rules.md:6). R4: "Remote fleet rows (`--include-remote`) before R4" are a non-goal (SPEC.md:82).

## 3. Acceptance tests

Header: "AC-1..AC-10 are restated from the seed brief; the issue's acceptance list was not re-read for this mapping (UNVERIFIED against #409)." (acceptance-tests.md:3). Harness: "Render with `Console(width=W, record=True, color_system=None or \"standard\")` and read `export_text()`. The adapter runs against a fake runner returning recorded JSON from the redacted golden sample. No TTY, no live Orca." (acceptance-tests.md:5). Fixture variants: "`base`, `uneven`, `shared-unmapped`, `historical`, `long-identifiers`, `source-loss`, `missing-fields`, `duplicate-out-of-order`, `empty`, `injection`." (acceptance-tests.md:7)

`[extractor]` CAP column = the CAPs whose SPEC.md success line cites the test (SPEC.md:32-65); "none cited" means no CAP names it. Cites are acceptance-tests.md line numbers.

| Test | AC | One line (verbatim fragment) | CAP | Line |
|---|---|---|---|---|
| T1 | AC-1 | "across every adapter path, argv equals one exact template" | none cited | 11 |
| T2 | AC-1 | "`--ack`, `--wait`, `--retry-request` do not appear in the adapter module and `check` appears only in the gated R2 template" | none cited | 11 |
| T3 | AC-1 | "no key maps to an Orca call" | none cited | 11 |
| T4 | AC-2 | "stops at the 5-call cap and renders `PARTIAL: collected 500 of reported T`" | CAP-4 | 12 |
| T5 | AC-2 | "shows `FAILED (timeout)`; the cycle ends within the 15 s budget" | none cited | 12 |
| T6 | AC-2 | "same input renders byte-identical text twice" | CAP-1 | 12 |
| T7 | AC-3 | "`base` (8 orchestrators, 80 sessions) in fixture mode lists every question oldest first with requester/owner and affected IDs" | none cited | 13 |
| T8 | AC-3 | "after `m`, a fixture step changing one `nextAction.kind` stars exactly that row and shows `changed since HH:MM (1)`" | CAP-7 | 13 |
| T9 | AC-3 | "live mode with no message source shows `Human questions: source UNVERIFIED, 0 rows interpreted, not \"no questions\"`" | CAP-2, CAP-3 | 13 |
| T10 | AC-4 | "`m` on every item leaves the open count unchanged" | CAP-7, CAP-11 | 14 |
| T11 | AC-4 | "`source-loss` keeps the open count and every retained item" | CAP-11 | 14 |
| T12 | AC-4 | "an item missing next cycle stays, marked `no longer in source window`" | CAP-11 | 14 |
| T13 | AC-5 | "`missing-fields` renders `unknown` for every absent field" | CAP-5 | 15 |
| T14 | AC-5 | "`terminalState=released` with `outcome` absent never renders `done`, `complete` or `settled`" | CAP-5 | 15 |
| T15 | AC-5 | "report, acceptance, tests and approval each render `unavailable (no source)` live" | CAP-5 | 15 |
| T16 | AC-6 | "matrix {5, 8, 10 orchestrators} x {50, 80, 100 sessions} x {160, 116, 80 columns} (27 renders)" | CAP-1 | 16 |
| T17 | AC-6 | "`uneven` per-owner counts sum to the global count" | none cited | 16 |
| T18 | AC-6 | "`page.total=287` with 100 rows shows `collected 100 / reported 287`, never `287 workers`" | CAP-4 | 16 |
| T19 | AC-6 | "(R2 placeholder, skipped until QUESTION-OBSERVATION)" | CAP-11 | 16 |
| T20 | AC-7 | "`shared-unmapped` shows two sessions sharing one `worktreeId` as two rows each naming it" | CAP-2 | 17 |
| T21 | AC-8 | "released/retained rows hidden by default with `k historical hidden (h)`" | CAP-2 | 18 |
| T22 | AC-8 | "`duplicate-out-of-order` shows `k duplicate rows ignored`" | CAP-2 | 18 |
| T23 | AC-9 | "at 160/116/80 every screen line has `cell_len <= W`" | CAP-8 | 19 |
| T24 | AC-9 | "`long-identifiers` truncates with `>` in lists; inspector shows the full ID" | CAP-6 | 19 |
| T25 | AC-9 | "reorder between cycles keeps selection on the same row ID" | CAP-6 | 19 |
| T26 | AC-9 | "`NO_COLOR=1` and `NO_COLOR=yes` emit no SGR colour" | CAP-8 | 19 |
| T27 | AC-9 | "`e`/`--once` writes the record export: no ESC byte, full IDs, no truncation" | CAP-9 | 19 |
| T28 | AC-9 | "SGR 5/6 (blink) never appears" | CAP-8 | 19 |
| T29 | AC-10 | "`injection` (CSI, OSC 8 hyperlink, unterminated OSC, 8-bit C1 `\x9b`, BEL, bidi Cf such as U+202E, terminal title set) leaves no ESC, C1 or Cf byte in render or export" | CAP-8 | 20 |
| T30 | AC-10 | "CJK/emoji identifiers truncate by cells; no overflow, no split double-width char" | CAP-8 | 20 |
| T31 | AC-10 | "cost renders `cost unavailable`, never `$0`; no progress from tokens or activity" | CAP-5 | 20 |
| T32 | Contract | "redacted golden `worker-list --json` sample parses" | CAP-2 | 21 |
| T33 | AC-3 | "`empty` renders `no observed items in this source window; not proof none exist`, never `no questions`" | CAP-3 | 27 |
| T34 | AC-5 | "live mode renders SETTLED and POLICY FROZEN as `unavailable (no source)`, never blank or zero" | CAP-5 | 28 |
| T35 | AC-9 | "COUNTS strip appears at 80, 116 and 160; priority tokens never truncated; below 80 reads `terminal too narrow (min 80)`" | CAP-4 | 29 |
| T36 | AC-1, AC-9 | "Real subprocess call patched to raise so any unlisted argv fails loudly" | none cited | 30 |
| T37 | AC-1 | "Argv validation rejects a value starting with `-`, a malformed `runId` and every forbidden prefix" | none cited | 31 |
| T38 | AC-5 | "Aggregate with k unknown members renders `n+? (k unknown)`, never a clean `n`" | CAP-4 | 32 |
| T39 | AC-8 | "Same `dispatchId` from different source namespaces stays two rows" | CAP-2 | 33 |
| T40 | AC-2 | "STALE at 45 s without success, unaffected by wall-clock jumps; backoff caps at 60 s" | CAP-4 | 34 |
| T41 | AC-3 | "First observation is the baseline with no change flags; a row dropping out shows `not reobserved`" | CAP-7 | 35 |
| T42 | AC-5 | "shows poll age and evidence age separately and does not mark the source STALE" | CAP-4 | 36 |
| T43 | AC-6 | "With the selected row visible and others hidden, `+N more` excludes the selected row" | CAP-6 | 37 |
| T44 | AC-10 | "Worker text containing Rich markup (e.g. `[bold]`) renders literally" | CAP-8 | 38 |
| T45 | AC-3 | "Default view chosen at start-up, never switches mid-session; header shows `read k of N Runs since start`" | none cited | 39 |
| T46 | AC-4 | "At 1,001 retained questions, eviction does not lower the open total" | CAP-11 | 40 |
| T47 | AC-3, AC-6 | "Before QUESTION-OBSERVATION the question area reads `source UNVERIFIED, 0 rows interpreted, not \"no questions\"`; no count from `result.count`" | CAP-3 | 41 |
| T48 | AC-9 | "Screen renderer and record export read the same view model" | CAP-9 | 42 |
| T49 | AC-9 | "When height cannot hold coverage, scope and PARTIAL ahead of optional panels, a too-small diagnostic shows" | CAP-8 | 43 |
| T50 | AC-S input | "R0 renders of A, B, C at 160/116/80 each carry \"synthetic fixture, not live evidence\" with a degraded version beside each" | CAP-1 | 44 |
| T51 | AC-1 | "R2 placeholder, skipped until the gate: quiet-scope side-effect test" ... "(INV-022)" | CAP-11 | 45 |
| Snapshot schema | owner decision 2 | "Validates every R1 snapshot against `snapshot-export-schema.md`; rejects an unknown `schemaVersion` major" ... "Test ID not yet assigned." | CAP-10 | 49 |
| AC-S | reviewer-checked | "a reviewer checks the owner's dated selection record exists" ... "No agent writes the record." | none cited | 53 |
| Manual CJK | manual | "reported as a manual check, not a test pass" | CAP-8 | 54 |

CAP-12 cites no test (SPEC.md:65).

## 4. Rendering and quality rules

- Views and modes: "One view model, three views over it (A Signal Bridge, B Attention Ledger, C Decision Desk), a detail inspector and a text export, in two data modes: `fixture` (the package's synthetic fixtures) and `live` (`worker-list` only)." (rendering-rules.md:3)
- Start-up rule: "the view is picked once at start-up from the runtime state of the question source." ... "The view never switches automatically mid-session." (rendering-rules.md:7)
- Widths: "At 116 columns or more B draws the full frame with `right = width - 43`. From 80 to 115 it uses the single-column narrow layout. Under 80 every view shows `terminal too narrow (min 80)` above the COUNTS strip, and the strip's denominators still print." (rendering-rules.md:12). B 160: left "x=1, width 114", right "x=117, width 42" (rendering-rules.md:37,39); 116: "`right = 73`; question panel 70 wide; right column stays 42" (rendering-rules.md:41).
- Height: "Coverage, scope and `PARTIAL` are minimum content, kept ahead of every optional panel; if height cannot hold them a too-small diagnostic shows instead. No per-panel scrolling, no multi-pane focus." (rendering-rules.md:13)
- Header line 1: "`ORCA OBSERVER  mode=fixture|live  scope=<result.scope.source or \"scope unknown\">  as of <local time of last good poll>`" (rendering-rules.md:17)
- Freshness strip: "`worker-list OK 4s` / `STALE 52s` / `FAILED (exit 2) 1m` / `NOT POLLED`. A second cell `messages UNVERIFIED (not read)` stays until QUESTION-OBSERVATION passes." (rendering-rules.md:18)
- COUNTS strip: "numbers and denominators only, no bars, no health name." ... "`collected n / reported T`, `PARTIAL` and scope are never truncated." ... "It is a minimum row and is never dropped." (rendering-rules.md:19)
- Keys: "Up/Down or `j`/`k` move, `Enter` opens detail, `Esc` returns, `/` local text filter, `h` show/hide historical rows, `m` mark a look, `e` write an export, `q` quit. No `r` key: refresh runs on the fixed 15 s cycle. No key maps to an Orca call." (rendering-rules.md:20)
- Footer: "the key list plus `shown x/y | collected n / reported T`." (rendering-rules.md:21)
- Selection: "anchored to identity, never a row index." (rendering-rules.md:23)
- Truncation / ASCII: "list cells truncate by display-cell width with a visible `>`. Non-UTF-8 terminals use `--ascii`, which replaces box drawing with `+-|`." (rendering-rules.md:24)
- NO_COLOR: "NO_COLOR is honoured for both `1` and `yes`." (stack.md:25); absent field "muted (plain under NO_COLOR)" (rendering-rules.md:51)
- Sanitizing: "every source string passes it before reaching the model. Removes CSI/OSC sequences (terminated and unterminated), 8-bit C1 controls, bare C0 controls except newline in the inspector, and Unicode Cf format characters." ... "Strings render as literal text, never Rich markup. Truncation uses `rich.cells.cell_len`, never `len()`." (adapter-contract.md:51)
- Polling: "Interval 15 s; cycle budget equals the interval; cycles never overlap." / "At most 5 subprocesses per cycle; each call's output capped at 8 MiB." / "After failures the interval backs off, up to 60 s." / "Per-call timeout is measured in R0, not guessed; UNVERIFIED until then." (adapter-contract.md:24-28)
- No LLM: "Deterministic, bounded collection: no LLM in the loop, fixed 15 s cycle, at most 5 subprocesses per cycle and 8 MiB output per call." (SPEC.md:70); "No LLM in the loop. The earlier 30 s cycle deadline is withdrawn." (adapter-contract.md:31)
- Read-only: "Read-only. No write path into Orca: no approve, retry, terminate, spawn, merge, rebase, delete-worktree, instruct or reply." (SPEC.md:69)
- Unknown: "Unknown is never rendered as 0, false, `-` or blank. Source loss never closes a question, lowers an open count or turns a value into `failed`." (SPEC.md:72); "Four states per fact: `known`, `unknown` (source omitted it), `unavailable` (no verified source exists), `stale` (not read successfully within 3 intervals)." (rendering-rules.md:50)
- Stale: "STALE after 3 intervals (45 s at 15 s) with no successful poll, on a local monotonic clock" ... "A failed poll shows `FAILED (<exit code or timeout>) <age>` with sanitized stderr in the inspector." (rendering-rules.md:53)
- Collection vs evidence: "source STALE depends on poll success only; a worker's evidence age is a plain age, with no per-row STALE until Orca's timestamp cadence is measured." (rendering-rules.md:54)
- Partial: "`PARTIAL: collected n of reported T (newest first; oldest rows not read; long-running active workers may be among them)`" (rendering-rules.md:55)
- Errors: "a non-zero exit, a timeout or invalid JSON marks the source `FAILED` for that cycle; the last good snapshot stays, qualified `as of`. Stderr is sanitized and kept to 2 KiB for the inspector." (adapter-contract.md:50)
- Gap notice: "`Human questions: source UNVERIFIED, 0 rows interpreted, not \"no questions\"`" (rendering-rules.md:31)
- Cost: "`cost unavailable`, never `$0`; no progress bar from tokens or activity." (rendering-rules.md:62)
- Changes since last look: "`m` records an observer-local mark in memory for this process only." ... "Marking never changes the open count." (rendering-rules.md:46)
- Data hygiene: "R1 output (screen, text export, snapshot) contains no message bodies, prompts, file contents or credentials; raw source output never goes into logs, fixtures or exports." (SPEC.md:76)

## 5. Stack

- Decision: "**Recorded owner decision 2 (CONFIRMED 2026-11-08):** Python + Rich, as a `superclaude observe`-style subcommand in the IronClaude repository." ... "This supersedes issue 409's stated preference for Go with Bubble Tea v2, Lip Gloss v2 and Bubbles v2." (stack.md:3)
- Comparison table label: "(seed brief stack table, 2026-11-08, primary sources, nothing run: UNVERIFIED as run facts)" (stack.md:5); Rich listed as "Python Rich 15 (installed)" (stack.md:7)
- Key reader: "a small POSIX stdlib reader (`termios`/`tty`/`select`) for the navigation keys and `/ h m e q`." ... "restores the terminal in `finally` and on SIGINT/SIGTERM." (stack.md:22)
- Spike and switch rule: "**Spike first (R0):** Rich Live with the raw key reader. If the spike fails, switch to Textual. Never build both." (stack.md:23); "Textual replaces Rich only if the spike fails, never both" (SPEC.md:74)
- Renderers: "the collector produces a snapshot; a pure function builds one view model; `render(view, W)` draws the width-bounded screen and `export(view)` writes the `e`/`--once` record form" (stack.md:24)
- Platform: "interactive mode is POSIX only; `--once` (text export) works everywhere, including Windows." (stack.md:26)
- Command name: "Recommended name `superclaude observe`; final name is open owner decision 3. Registering it in the shipped CLI is production integration under reading 1 (`release-gates.md`)." (stack.md:27)
- Never build / never use: "No dependency on TUIBBS, no AGPL code copied, and the design prototype (`canvas.py`) is never imported." (SPEC.md:75); "TUIBBS-scp is AGPL-3.0; no code is copied from it." (stack.md:28); "the design package's mock-up action buttons are not built." (rendering-rules.md:69)

## 6. Adapter contract: sources and evidence labels

`[extractor]` adapter-contract.md does not tag individual `worker-list` fields VERIFIED; the only "verified" wording for the source is SPEC.md:34 ("the verified `worker-list` source"). Labels below are those written in the files.

| Source | Status / label (verbatim) | Cite |
|---|---|---|
| `worker-list` (R1 data verb) | "R1 has one verb: `orca orchestration worker-list --json --limit 100`, with optional `--run <runId>` and `--cursor <c>`" | adapter-contract.md:3 |
| Discovery probe | "reuse `_find_orca()` (`cli/install_user_setup.py`): tries `orca-ide`, then `orca`, validates with `skills list --json` (rejecting the GNOME screen reader named `orca`), 10 s timeout. No binary: the freshness cell reads `worker-list NOT AVAILABLE (orca binary not found)`, never an empty fleet." | adapter-contract.md:10 |
| Message source (R2 candidate) | "`check --all --run <runId> --json` is only a candidate verb behind the gate." / "Row fields UNVERIFIED" | rendering-rules.md:71 |
| Message source in R1 | "`messages UNVERIFIED (not read)`" | rendering-rules.md:18 |
| `--include-remote` | "not in the allow-list until R4." | adapter-contract.md:16 |

Fields:
- Required: "`result`, `result.workers`, `result.page.hasMore`. Any missing: the cycle is `FAILED (shape)` and the last good snapshot is kept." (adapter-contract.md:36)
- Optional: "`result.scope` (absent: `scope unknown`) and `page.total` (absent: `reported unknown`). V1 dissents that `page.total` should be required" (adapter-contract.md:37)
- Missing key: "a missing key becomes `UNKNOWN`, a sentinel that is not `None`, 0 or `False`. Unknown extra keys are ignored and counted in the inspector (`n unrecognised keys`)." (adapter-contract.md:38)
- Ledger row fields: "`dispatchId`, run (labelled \"run\", never \"orchestrator\"), `workerState`, `dispatchStatus`, `terminalState`, `projection.outcome` (raw), `projection.nextAction.kind`, `liveness.verdict (liveness.source)`, evidence age." (rendering-rules.md:29)
- Inspector fields: "`dispatchId`, `taskId`, `runId`, `resource.worktreeId`, `resource.ownerDispatchId`, `resource.originDispatchId`, `projection.host.id`, `projection.workspace.id`, and `projection.stage.{worker,dispatch,activity,detail}`" (rendering-rules.md:25)
- `result.counts`: "`source counts: active a / reclaimable r / retained t / released l` (from `result.counts`, never summed with page-derived counts)" (rendering-rules.md:19)
- Scope values: "`result.scope.source` (`flag`, `bound` or `all`, per help)" (adapter-contract.md:63)
- PROPOSED: "V1's numeric bounds and regexes are PROPOSED, not verified Orca formats." (adapter-contract.md:18); "The source-to-dashboard schema is PROPOSED, not an Orca contract (`unverified-register.md`)." (SPEC.md:71)
- UNVERIFIED: "Per-call timeout is measured in R0, not guessed; UNVERIFIED until then." (adapter-contract.md:28); "Whether `worker-list` has a state filter is UNVERIFIED." (adapter-contract.md:61); timestamps "ISO-8601 on one clock; UNVERIFIED" (SPEC.md:94); "terminal-attribution fields are UNVERIFIED" (adapter-contract.md:57)
- Forbidden set: "(prefix-matched, never shrinks): plain `check` (without `--peek`/`--all`), `--ack`, `--wait`, `--retry-request`, `dispatch`, `inbox`, and any verb other than the two templates above." (adapter-contract.md:17)
- Identity: "Row identity = source namespace + `dispatchId`; rows from two hosts or Runs never merge." (adapter-contract.md:42)
- Ordering: "Across cycles the newer `projection.liveness.observedAt` (or `projection.evidence.lastObservedAt`) wins." (adapter-contract.md:44)
- R2 retention: "bounded at 1,000 records; eviction never lowers the open total" (adapter-contract.md:55)

## 7. Open owner questions and open decisions

SPEC.md "Open Questions" (SPEC.md:97-113): 15 items. The source gives them no ids; `OQ-n` below is `[extractor]` numbering in source order.

| Id | Question (verbatim) | Cite |
|---|---|---|
| OQ-1 | "Does the owner's staged choice satisfy DIRECTION-SELECTED, and where is the dated owner-written selection record?" | SPEC.md:99 |
| OQ-2 | "Which production-integration reading applies (1: registering the command or any live subprocess outside the fake runner; 2: wiring into the shipped product)?" | SPEC.md:100 |
| OQ-3 | "Final command name (recommended `superclaude observe`)?" | SPEC.md:101 |
| OQ-4 | "Fallback date for QUESTION-OBSERVATION?" | SPEC.md:102 |
| OQ-5 | "Sample capture and acquisition permission for live reads (open owner decision 6)?" | SPEC.md:103 |
| OQ-6 | "Message-content exposure (open owner decision 7)?" | SPEC.md:104 |
| OQ-7 | "What identifies a human question (open owner decision 8)?" | SPEC.md:105 |
| OQ-8 | "Multi-observer restriction (open owner decision 9)?" | SPEC.md:106 |
| OQ-9 | "Licence opinion before any Go screen reads the snapshot?" | SPEC.md:107 |
| OQ-10 | "Does TUIBBS become the staff platform?" | SPEC.md:108 |
| OQ-11 | "Is the write-back boundary change (issue 409 plus TUIBBS FR-X-13 amendment) approved?" | SPEC.md:109 |
| OQ-12 | "Which row order is authoritative for snapshot consumers: the snapshot's timestamp order or the ledger's source \"newest first\" order?" | SPEC.md:110 |
| OQ-13 | "Does `read k of N Runs since start` belong in the B view header only (merged-requirements rendering rule) or in every header (its adapter scope-honesty rule, T45 and the risks table)? CONTRADICTION in the source; see `rendering-rules.md`." | SPEC.md:111 |
| OQ-14 | "What are the contents of A's width matrix, B's x/width coordinates beyond those copied, and C's 44-row height contract (drop order, minimum rows)? The sources name them but do not define them." | SPEC.md:112 |
| OQ-15 | "Which `projection.stage.*` subfield drives change detection, and may `stage.detail`/`stage.activity` enter the snapshot (architecture-options.md lists them; merged requirements keep them inspector-only)?" | SPEC.md:113 |

Gate status: "DIRECTION-SELECTED has not passed, and until the owner confirms a production-integration reading the stricter one applies: offline R0 work only. Issue 409 does not authorize production code changes or deployment." (SPEC.md:73)

Open items in the other four files:
- rendering-rules.md:8: "The sources name these three artifacts but do not define their contents; only the values copied below are specified, the rest is UNVERIFIED and an open question (`SPEC.md`)." (= OQ-14)
- rendering-rules.md:17 and adapter-contract.md:63: CONTRADICTION on `read k of N Runs since start` (= OQ-13); acceptance-tests.md:39 T45: "(which views carry it is an open question, `SPEC.md`)"
- rendering-rules.md:46: "(which `projection.stage.*` subfield is an open question)" (= OQ-15)
- rendering-rules.md:87: "**Dissent (V3):** once explicit-link rows exist, C should be the post-link composition. Two of three advocates recommend B as the post-link default. Not settled; the optional owner re-confirm at QUESTION-LINK exists for this choice."
- stack.md:27: "final name is open owner decision 3" (= OQ-3)
- adapter-contract.md:28: "Per-call timeout is measured in R0, not guessed; UNVERIFIED until then."
- adapter-contract.md:30: "Message calls per cycle: open parameter set by measurement; V3 default at most 1."
- adapter-contract.md:37: "V1 dissents that `page.total` should be required (`owner-decisions-and-risks.md`)."
- adapter-contract.md:62: "**A-008 (QUALIFY; V3 dissent REJECT):** caps are per observer process" ... "Any restriction is open owner decision 9." (= OQ-8)
- adapter-contract.md:19: "`--opt=value` only after Orca's parser support is recorded."
- acceptance-tests.md:49: snapshot schema test "Test ID not yet assigned."
- acceptance-tests.md:3: AC mapping "UNVERIFIED against #409"

## 8. Non-goals and out of scope

SPEC.md "Non-goals" (SPEC.md:80-85):
- "Any operational control or write-back in R1, including confirmations or corrections sent to agents; that is a future stage needing a boundary change (`write-back-future-stage.md`)." (SPEC.md:80)
- "A scheduler, session manager, or fork of another agent manager." (SPEC.md:81)
- "Remote fleet rows (`--include-remote`) before R4; closure evidence, history beyond the 100-row window, admission, cost, durable replay and deep links before their own feeds exist." (SPEC.md:82)
- "Parsing message rows (`check --peek/--all`, `inbox --json`) before QUESTION-OBSERVATION; the Decision Desk before QUESTION-LINK." (SPEC.md:83)
- "Fleet SIGNALS bars, an `r` refresh key, persisted \"last look\" across runs, mouse, themes, animation, blinking, and Windows interactive keyboard input." (SPEC.md:84)
- "The TUIBBS Go screen itself." (SPEC.md:85)

rendering-rules.md "Deliberately left out" table (rendering-rules.md:67-81) adds: "Plain `check`, `--ack`, `--wait`, `--retry-request`" (:70); "Live question age, requester, owner" (:72); "C's affected-session ledger before QUESTION-LINK" (:73); "Deleting historical rows" (:75); "Complete message history, cost/usage, admission, revision-pinned verification, durable replay, deep links" (:79).

