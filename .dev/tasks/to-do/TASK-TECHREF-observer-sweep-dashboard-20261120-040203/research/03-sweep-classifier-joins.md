# Research: what each sweep row means (sweep classifier, joins, C8 candidates)
**Investigation type:** Code Tracer
**Scope:** src/superclaude/cli/sweep/classify.py, models.py; tests/sweep/test_classify.py and tests/sweep/fixtures/; docs/designs/orchestrator-mode.md (sections 7.2, 12-14); commands/sweep.md; skills/sc-sweep-protocol/SKILL.md; core/WORKER-CONTRACT.md; sweep/report.py
**Status:** Complete
**Date:** 2026-11-20
---

Path convention: every code path below is relative to the repo root of the read-only export of origin/master 61ac2c2e6 (`/home/coder/.cache/ic-snap-20261120/master`) unless it says "checkout". Files that exist only under `.dev/` on origin/master (the SPEC) were read with `git -C /home/coder/workspaces/IronClaude show origin/master:<path>` and are cited as `SPEC` = `.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md` (653 lines; origin/master only, not in the snapshot). Nothing under `.dev/research/orca-dashboard-20261105/` is cited in this file.

Method note: the task prompt asks for an Agent subagent; I am that agent, so I did the reading myself with Read/Grep/Glob, read-only `git show`, `git grep` and `git ls-tree` calls on `origin/master`, and read-only `gh issue view`/`gh issue list`/`gh search issues` calls with `--repo IronbellyOrg/IronClaude` (issues #534 and #590 and two searches). I did not run any code under study. One scratch copy of the SPEC was written to `/tmp` while reading and deleted again.

## 0. Verification of the starting facts (staleness check)

| Claim (source) | Verdict | Evidence |
|---|---|---|
| "`src/superclaude/cli/sweep/` does not exist yet" (docs/designs/orchestrator-mode.md:27) | **[CODE-CONTRADICTED]** **[STALE DOC]** | The folder exists with `__init__.py`, `commands.py`, `models.py`, `probes.py`, `classify.py`, `report.py` (Glob of `src/superclaude/cli/sweep/`: 6 files, i.e. 5 modules plus `__init__.py`). The sentence is a dated fact ("checked on this host on 2026-11-08", design line 25). |
| Rule names and order of `RULES` (design 7.2 table, lines 478-488) | **[CODE-VERIFIED]** | `classify.py:345-355` lists exactly: blocked_contract, orca_exit_proof, fenced, waiting_signal, working, finished, idle, person_active, fallback. Pinned by `tests/sweep/test_classify.py:378-379` (`test_rules_order_pin`). |
| Class constants (design line 474) | **[CODE-VERIFIED]** | `models.py:50-59` holds the 8 `CLASSES`; `classify.py:42-51` unpacks them as C_WAITING, C_STALLED, C_FENCED, C_WORKING, C_FINISHED, C_IDLE, C_PERSON_ACTIVE, C_UNKNOWN. |
| `classify_all` is the only entry from the command (design 4) | **[CODE-VERIFIED]** | `commands.py:23` imports it, `commands.py:269-271` calls `probes.collect` then `classify_all`. |
| `JOIN_PATH` decides the join path (design 7.2 "Which path applies ... decided from the step 1.0a capture") | **[CODE-VERIFIED] with a nuance** | `classify.py:40` sets `JOIN_PATH = "B"`. The constant is read in exactly one place, `_guard` (`classify.py:745`). `_join_transcripts` tries path A and then path B on every transcript regardless of the constant (`classify.py:667-682`). So `JOIN_PATH` only changes the guard cases (see section 4). |
| CHANGELOG "Known limits (sweep, Phase 1)": "`working` is never produced" (CHANGELOG.md:170) | **[CODE-CONTRADICTED]** **[STALE DOC]** | `classify.py:251-269` produces `working` when the four conditions hold; `tests/sweep/test_cli_contract.py:1133-1140` classifies the captured running worker (`captured-worker-show-running.json`) as `working`. Design D7 (docs/designs/orchestrator-mode.md:841) records "Update 2026-11-16 ... Rule 5 is active". The CHANGELOG line (section dated 2026-11-12) was not updated. The same CHANGELOG line is right about `stalled (proved)` and `fenced`. |

Key Takeaways
- The design doc's "does not exist yet" line is stale; the sweep package is live code.
- The CHANGELOG known-limits line over-states: `working` IS produced since 2026-11-16; only `stalled (proved)` and `fenced` stay unobserved.
- `JOIN_PATH` is read once (in `_guard`), not at the join itself.

## 1. The 9 rules: exact firing conditions (first match wins)

`classify(row, ctx)` (`classify.py:369-386`) walks `RULES` (`classify.py:345-355`) in order and stops at the first rule that returns a value. Rule 9 always returns, so every row gets exactly one class. Four post-steps follow the rule walk (they can change the outcome, see section 3). Terms: "settled" = `orca.outcome in ("succeeded","partial","failed")` (`_settled`, `classify.py:113-114`, `_SETTLED_OUTCOMES` at `:98`). "STOP code" = a token matching `\bE-[A-Z0-9]+(?:-[A-Z0-9]+)*\b` in `contract.reason` plus `contract.blocked_question` (`_STOP_CODE` `:101`, `_stop_codes` `:117-119`). "Ruling halt" = STOP code `E-HALT-QA` or `E-NO-RULING` (`:97`, `:126-127`). "Freeze code" = any STOP code except `E-RESUME-NEEDED` (`:96`, `:122-123`).

Proof column: "inline" means the test builds `OrcaObservation`/`ContractRecord`/`SessionRow` objects in memory with the helpers `orca()`, `contract()`, `row()` (`tests/sweep/test_classify.py:143-169`); no file under `tests/sweep/fixtures/` is read by `test_classify.py` (Grep for `captured-` and `fixtures/` in `test_classify.py`: no use; the disk-source builders `SweepRoot` write real files under pytest `tmp_path`, `conftest.py:196-205`). Captured fixtures are read only by `test_cli_contract.py` and `test_probes_allowlist.py`.

| # | Rule name (`classify.py`) | Class and kind | Exact firing condition | Proving test(s) | Proving fixture |
|---|---|---|---|---|---|
| 1 | `blocked_contract` (`_blocked_contract` `:161-188`, wrapper `:211-212`) | waiting on a person, kind `a` | Needs ALL of: `row.contract` not None; `contract.worker_status == "blocked"`; `row.transcript_readable is not False`. Then, in this order: (i) `orca is None`: match only if a Ruling halt is present (evidence "Ruling halt ...; no Orca row"), else decline with note "blocked contract; Orca state not observed"; (ii) Orca row settled: match; (iii) `row.gate_policy == "report blocked"`: match; (iv) Ruling halt present: match; (v) otherwise decline, adding note "blocked contract under ask the coordinator; may be re-running" only when `orca.liveness_verdict == "live"` and `gate_policy in ("ask the coordinator", None)`. | Case `blocked_contract` at `test_classify.py:288-295` run by `test_rule_case_per_rule_1_to_9` (`:364-368`); `test_rule1_matches` (`:728-760`: settled, report-blocked, ruling-halt); decline tests `:687`, `:698`, `:714`, `:763`; end to end `tests/sweep/test_cli_contract.py:1085-1115` (`test_waiting_lists_hold_row_ids_only`). | inline; the end-to-end test builds a contract file with `env.sweep_root.contract(...)` and canned Orca replies (no captured file) |
| 2 | `orca_exit_proof` (`_exit_proof` `:191-208`, wrapper `:215-216`) | stalled (proved), no kind | Needs ALL of: Orca row present; `liveness_verdict == "exited"`; `transcript_readable is not False` (None passes); `worker_done_seen is False` (identity test, so None does not pass); `fenced_evidence == "absent"`. Otherwise decline; the decline adds note "Orca: exited; fenced evidence not readable" when `fenced_evidence == "unreadable"` or `transcript_readable is False` (the note is attached by `classify` at `:378`, not by the rule). | Case `orca_exit_proof` at `:296-307`; `:587-592` (worker_done_seen None declines); `:595-606` (no joined transcript still stalled; unreadable transcript gives fallback); `:609-624` (same through `classify_all`); `:581-584` (FR-008 four inputs never stalled); `:763-777`. | inline only. The hand-set `worker_done_seen=False` plus `fenced_evidence="absent"` exists only in test code (see section 7) |
| 3 | `fenced` (`_rule_fenced` `:219-223`) | fenced, no kind | Orca row present and `fenced_evidence == "present"`. Nothing else is tested (no liveness, no transcript test inside the rule). | Case `fenced` at `:308` (one parametrized case). `tests/sweep/test_report.py:353` renders a hand-built `fenced` row. | inline only |
| 4 | `waiting_signal` (`_rule_waiting_signal` `:226-248`) | waiting on a person, kind `a` or `b` | Three alternatives, tried in order: (a) Orca row present and `agent_wait is not None` (evidence "agent_wait is non-null (worker-show agentWait)"; adds "; waiting since <iso>" only when `agent_wait_since` is set and not after `ctx.now`; adds note "timestamp in the future" when it is after `now`); (b) `contract.worker_status == "failed"` and at least one freeze code (evidence "frozen plan: ..."); (b) Orca row present and `orca.status == "ready"` (a Task row the sweep builds itself, evidence "ready Task: creator not observable; needs ownership review"). | Case `waiting_signal` `:309-319`; `:382-389` (age, future); `:405-411` (kind b: frozen plan, ready Task); `:414-417` (E-RESUME-NEEDED alone is not frozen); `:476-485` (non-null agent_wait beats rule 5); `:1076-1125` (explicit-wait exemption). | inline; `captured-task-list-ready.json` is an EMPTY task list (`SOURCES.md:26`), so no captured ready Task exists |
| 5 | `working` (`_rule_working` `:251-269`) | working, no kind | Needs ALL of: Orca row present; `liveness_verdict == "live"`; `outcome == "in_progress"`; `agent_wait_present is True`; `agent_wait is None`. `dispatch.status` is NOT tested. | Case `working` `:320`; `:444-447`, `:461-463` (each condition), `:466-473` (status not tested), `:476-485`; end to end `test_cli_contract.py:1133-1160` (captured running worker is `working`) and `:1163-1169` (captured exited worker is not); parser `test_probes_allowlist.py:1639-1651`. | `tests/sweep/fixtures/captured-worker-show-running.json` (live, `projection.outcome` in_progress, `agentWait` null; `SOURCES.md:25`); negative: `captured-worker-show-1.json` (exited) |
| 6 | `finished` (`_rule_finished` `:272-292`) | finished, no kind | Either (i) `orca.body_text` is not None and its FIRST line (`splitlines()[0]`) starts with `guard refused:`; or (ii) Orca row settled AND `contract` not None AND `contract.worker_status in ("succeeded","partial","failed")`. Adds note "partial: usable not yet judged" when either `orca.outcome` or `contract.worker_status` is `partial`. | Case `finished` `:321-328`; `:627-635` (guard refused, exited, with the exited note); `:645-654` (settled row without a contract is NOT finished); `:785-788` (guard text on a later line is not finished); `:791-800` (wording never "admitted"/"accepted"); `:803-806` (partial note). | inline |
| 7 | `idle` (`_rule_idle` `:295-311`) | idle, no kind | Needs ALL of: `person_started is True`; `orca is None`; `transcript_readable is True`; `last_activity` not None; `last_activity <= ctx.now`; `last_activity < ctx.window_start`. Evidence is later extended with "; last_activity from <source>" by `classify_all` (`:958-959`). | Case `idle` `:329-337`; `:493-502` (5 h old row is idle only when the window is under 5 h); `:505-522` (last_record_ts versus st_mtime source); `:525-540` (future timestamp never idle); `:957-968` (complete-list control, counted as historical); `:1076-1125` (exemptions). | inline |
| 8 | `person_active` (`_rule_person_active` `:314-327`) | person session (active) | Needs ALL of: `person_started is True`; `transcript_readable is True`; `last_activity` not None; `last_activity >= ctx.window_start`. It does NOT test `orca is None` and does NOT test `last_activity <= now`, so a future-dated transcript that is the person's own lands here with the note "timestamp in the future". | Case `person_active` `:338-346`; `:493-502`; `:1734-1756` (FR-005 fixture, active person row counted as visible). | inline |
| 9 | `fallback` (`_rule_fallback` `:330-342`) | could not determine, no kind | Always matches. Evidence "no rule 1 to 8 matched (<liveness, outcome, status or 'no Orca row'>; person_started <value>)". Adds note "no contract read for this row; finished needs a parsed contract" when the Orca row is settled and `row.contract is None`. | Case `fallback` `:347` (empty row); `:581-584`; `:638-642`; `:645-654`; `:672-673` (the no-contract note has four negative cases). | inline |

Rule-walk details that are easy to miss
- Rule 1's `_blocked_contract` and rule 2's `_exit_proof` are called a SECOND time by `classify` (`:378`) only to harvest their decline notes; the notes appear even when a later rule matches (example `:698-711`, `:638-642`).
- Rule 4(a) reads `orca.agent_wait_since`, but nothing in production sets it: `models.py:111-112` ("Reserved ... No code sets it"), `probes.py:481` ("`agent_wait_since` stays unset"), `test_probes_allowlist.py:1651`, `:1687`. So the "waiting since" evidence and the Waiting (a) age from an agentWait never print in a live run; the contract file mtime is the other age source (`ContractRecord.mtime`, `models.py:124-125`).
- What a non-null `agentWait` means was never captured: `models.py:98-99`, `probes.py:458-462`, design 7.2 line 493, open item 6 (design line 1003). Rule 4(a) treats any non-null value as "waiting on a person (a)".

Key Takeaways
- Nine rules, strict order, first match wins; every row gets one class; `fallback` is a real rule (not an absence of one).
- Rules 2 and 3 have no input that can make them fire in a real run (section 7); rules 1, 4, 5, 6, 7, 8, 9 can.
- All rule tests use in-memory builders; the captured Orca fixtures are exercised only by the end-to-end and parser tests (rule 5 positive and negative).

## 2. The 8 classes: what a row's class means and which rules can print it

Class strings are `models.CLASSES` (`models.py:50-59`), printed as they are. Counts per class (zeros included) come from `classify_all` (`classify.py:974-977`). `test_every_class_name_is_reached` (`test_classify.py:371-375`) proves each of the 8 is reachable from `classify()`, but only with hand-built rows (including the hand-set stalled and fenced inputs).

| # | Class (`models.py`) | Produced by | Plain meaning of the row | Printable in a real `sweep run` today? | "Next inspection" text per rule (`report.py:54-68`) |
|---|---|---|---|---|---|
| 1 | `waiting on a person` (`CLASSES[0]`) | rule 1 (kind a), rule 4 (kind a or b) | (a): a contract says `blocked` under a settled/report-blocked/Ruling-halt condition, or Orca shows a non-null `agentWait`. (b): a frozen plan (failed contract with a STOP code) or a ready Task with no observable creator. Listed in `result.waiting_a` / `waiting_b` by row id (`classify.py:994-999`). | Yes: rule 1 and rule 4(b) need only contract and Task data; rule 4(a) needs a non-null `agentWait` that was never captured. | rule 1: "read the contract's blocked question and the worker's last transcript lines"; rule 4: "read what the Evidence cell names ..." |
| 2 | `stalled (proved)` (`CLASSES[1]`) | rule 2 only | An Orca row whose liveness is `exited`, with proof that no `worker_done` arrived and no fencing evidence exists. | **No.** No code sets `worker_done_seen` to False or `fenced_evidence` to "absent" (section 7). | rule 2: "read the worker's last transcript lines and its Orca worker-show result" |
| 3 | `fenced` (`CLASSES[2]`) | rule 3 only | An Orca row with `fenced_evidence == "present"`. | **No.** No code sets `fenced_evidence` to "present" (section 7). | rule 3: "read the fencing evidence named in the row" |
| 4 | `working` (`CLASSES[3]`) | rule 5 only | Orca says the worker is live, its outcome is `in_progress`, and `agentWait` is present and null. | Yes, since the 2026-11-16 capture (`test_cli_contract.py:1133-1160`). | rule 5: "read the worker's last transcript lines to confirm it is active" |
| 5 | `finished` (`CLASSES[4]`) | rule 6 only | Orca outcome settled AND a parsed contract with a settled `worker_status` (or a body that starts with `guard refused:`). Never means admitted or accepted (`test_classify.py:791-800`). | Yes, but only when a contract was found for the row (see `_contract_for`, section 4); without a contract a settled row prints `could not determine` with the note "no contract read for this row; finished needs a parsed contract" (`classify.py:86`, `:341`; `test_classify.py:645-654`). | rule 6: "read the worker's report file and its contract" |
| 6 | `idle` (`CLASSES[5]`) | rule 7 only | A person-started transcript with no activity inside the window. Printed under `## Historical sessions`; counted as `historical` (`classify.py:977`), and `visible = total - historical` (`:983`). | Yes, but `person_started` is True only in narrow conditions (section 4), under join path B only when no non-ready Orca Dispatch row exists at all (`_guard` `earlier_pane`, `classify.py:756`). | rules 7 and 8: "read the session's last transcript lines" |
| 7 | `person session (active)` (`CLASSES[6]`) | rule 8 only | Same True origin as idle but with activity inside the window. | Same condition as idle. | same |
| 8 | `could not determine` (`CLASSES[7]`) | rule 9, plus forcing (section 3) | Nothing proved the row's state, or an input needed for the proof could not be read or joined. | Yes: the common outcome. | rule 9: "read the row's Evidence and Notes cells, then the sources marked unscanned in Source coverage ..." |

Per-row dimensions that `classify_all` fills in (the rest stay `unknown`)
- `lifecycle` (`_lifecycle` `classify.py:793-798`): `unknown` when there is no Orca row or no outcome; `settled` when the outcome is settled; else `running`.
- `health` (`:801-806`): `failed result` when the contract `worker_status == "failed"`; otherwise `unknown` ("no issue observed has no Phase 1 source", comment `:803-804`).
- `result` (`:809-814`): `unknown` when no contract or no status; `null` for `blocked`; else the contract's `worker_status`.
- `freshness` and `freshness_age_s`: set only on transcript-only rows with `person_started is True` and `last_activity <= now` (`:921-935`): `stale` when before `window_start`, else `fresh`.
- `phase`, `approval`, `admission`, `evidence_packet` stay `unknown` and `tests_review` stays None: `models.py:164-173` defaults and no assignment in `classify.py`. (Grep of `classify.py` for those names: only `row_id`, `lifecycle`, `health`, `result`, `freshness`, `freshness_age_s` are passed to `SessionRow(...)`, `:894-907` and `:924-936`.)
- `policy` is computed apart from the class by `policy_of` (`:389-401`): `frozen` when the contract is `failed` with a freeze code, or `blocked` with a freeze code or a `command` containing `sc:implement`; else None. Tests `:414-432`.

Key Takeaways
- Six of the eight classes can print in a live run today; `stalled (proved)` and `fenced` cannot (section 7).
- `idle` rows are the ONLY rows counted `historical`; "visible" excludes them.
- Five of the ten #409 dimensions (phase, approval, admission, evidence packet, tests/review) are always `unknown` in Phase 1; only lifecycle, health, result, freshness (transcript rows) and policy carry data.

## 3. After the rule walk: notes, and the could-not-determine forcing

A row's printed class is not always the class of the rule that matched. Three later steps can replace it with `could not determine` (rule name `fallback`, `waiting_kind` None, the matched rule's evidence kept, notes extended): `_force_unknown` (`classify.py:358-366`).

| Step | Where | Condition | Effect |
|---|---|---|---|
| A. Note harvest in `classify` | `classify.py:378-383` | always | Adds the rule-1 and rule-2 decline notes; adds "WC-13 violation, review" when `orca.parent is not None` (class unchanged, `test_classify.py:809-816`); adds "timestamp in the future" when `last_activity > ctx.now`. |
| B. Unreadable transcript | `classify.py:384-385` | `row.transcript_readable is False` | Forces `could not determine` for ANY matched rule, adds "unscanned: transcript not readable". Tests `:763-777`, `:819-827`, `:834-842`. |
| C. Join and source outcomes | `classify_all` `classify.py:908-914`, applied at `:960-961` | the row's `forced` tuple is non-empty | Forces `could not determine`. `forced` holds: the path-A several-rows note and the path-B notes of section 4 (`Dispatch time window not observable`, `session started before this Dispatch window`, `pane moved to a later session`, `session start not observable: transcript tail only`, `conflict: one pane session matches several Dispatch rows`); `conflict: duplicate Dispatch rows disagree` (rows that share a Dispatch id but differ, merged by `_merge_group` `:512-525`, which also nulls the three Dispatch time fields); and source-row flags from `_source_flags` (`:817-836`): an `unscanned` source named `contract <dispatch>` gives "unscanned: contract not readable", one named `transcript <path>` gives "unscanned: transcript not readable", and an `unscanned` text containing "inconsistent" gives "conflict: inconsistent observation". Producers of those two source names: `probes.py:1411` and `:1475`. |
| D. Rule 9 | `classify.py:330-342` | no rule 1 to 8 matched | The ordinary could-not-determine path. |

Consequences worth stating plainly
- A live worker whose pane transcript is longer than 256 KiB cannot print `working` when a tab-map entry joins it by path B. `probes.py:840-848` reads only the last 256 KiB of such a file and sets `tail_complete=False`; `_join_path_b` (`classify.py:619-628`) then forces the Dispatch row to `could not determine` with the note "session start not observable: transcript tail only". Test `test_classify.py:1405-1412`. (The same holds for `finished` rows whose transcript matched.) Whether real worker transcripts exceed that size was not measured here.
- A terminal Dispatch row (status not `pending` or `dispatched`) with no `completedAt` has no observable window; if a transcript matched it by path B, the row is forced to `could not determine` ("Dispatch time window not observable"). Test `:1385-1391`.
- `could not determine` therefore mixes three different meanings: no rule proved anything (rule 9), an input could not be read (B, source flags), and a join was ambiguous (C). The notes cell is the only place the difference shows.

Key Takeaways
- Class = first matching rule, then possibly overridden by transcript readability, join ambiguity, duplicate Dispatch ids, or an unscanned source named for that row.
- The 256 KiB tail limit is a hidden precondition of `working` and `finished` for any row whose transcript joined by path B.

## 4. Joins: how an Orca row and a transcript become one row (`person_started`)

Notation: `session_join` is `OrcaObservation.session_join`, set by `parse_worker_show` from `dispatch.assigneeHandle` (`probes.py:486`); the captured value is a terminal handle of the form `term_<uuid>` (`SOURCES.md:9`). `tab_map` entries come from the ccsession `orca-tabs` files (`models.TabMapEntry` `:143-148`): `file_name` (pane key with `+`), `session_id`, `launch_dir`, `terminal_handle`. `person_started` is `bool | None` (`models.py:154`).

### 4.1 Order of work in `classify_all` (`classify.py:880-1009`)

1. `_merge_dispatches` (`:528-545`): rows with the same `dispatch` id are grouped; a group of one passes through; a group of several becomes one merged identity (conflict set), no row wins.
2. Transcripts are sorted by `(session_id or "", str(path))` (`:883`), so the result does not depend on input order.
3. `_join_transcripts` (`:655-683`) per transcript with a session id: path A, else path B (4.2, 4.3).
4. `_guard` (`:741-757`) computes the completeness flags once (4.4).
5. One `SessionRow` per Orca row: `person_started = False` when a transcript joined, else None (`:896`). One `SessionRow` per un-joined transcript: `person_started` from `_person_origin` (4.5), `orca=None`, `contract=None`.

### 4.2 Path A (`classify.py:667-676`)

For a transcript with `session_id`: `a_rows = [r for r in rows if r.session_join == sid]`. One match joins that row (`joined`, `taken`); several matches put the note "conflict: one pane session matches several Dispatch rows" on each row (forcing, step C) and leave the transcript unjoined with that note. Path A is tried FIRST and independently of `JOIN_PATH`. With the production `session_join` (a terminal handle) path A matches only if a transcript's session id equals a handle string; the tests exercise path A by `monkeypatch`-ing `JOIN_PATH` to "A" and giving `session_join` a session id (`test_classify.py:116-119`, `:1212-1227`).

### 4.3 Path B (`classify.py:677-682`, `_join_path_b` `:609-652`)

`keys` = every `file_name` and `terminal_handle` of tab-map entries whose `session_id` equals the transcript's. `b_rows` = Orca rows whose `session_join` is in `keys`. If none match, the transcript is left for 4.5. Otherwise, per matching row, an observable time window is required (`_window` `:548-558`):

| Row state | Window |
|---|---|
| Dispatch id in the conflict set, or `dispatch_started is None` | None (not observable) |
| `dispatch_ended` set | `[dispatch_started, dispatch_ended]` |
| `dispatch_ended` None and `dispatch_status in ("pending","dispatched")` | `[dispatch_started, collected_start]` |
| anything else | None |

Then (`:617-652`): (i) tail incomplete (`not tail_complete` or `first_record_ts is None`): matching rows with a window get "session start not observable: transcript tail only", others "Dispatch time window not observable"; nobody joins; (ii) otherwise `cut = first_record_ts` with microseconds dropped; a row misses with "Dispatch time window not observable" (no window), "pane moved to a later session" (`cut` after the window end) or "session started before this Dispatch window" (`cut` before the start), bounds inclusive (`test_classify.py:1364-1382`); (iii) exactly one holder: the transcript joins it, the row gets the informational (non-forcing) note "joined by pane: latest session of the pane"; several holders: each holder gets "conflict: one pane session matches several Dispatch rows" and the transcript stays unjoined; no holder: the transcript stays unjoined with the first of the three miss notes in the order moved, before-window, window-not-observable. All miss notes force the missed Dispatch rows to `could not determine`.

### 4.4 The completeness guard `_guard` (`classify.py:728-757`, `_origin_unknown` `:690-725`)

Rows considered exclude `status == "ready"` Task rows (`:747`). Flags:
- `origin`: the five list-incomplete notes in this order: "origin unknown: Orca unavailable" (`orca_available` False), "...: worker list truncated" (`truncated`), "...: worker list call failed" (an `orca worker-list <run>` source is `unscanned` while Orca is available), "...: Run not confirmed" (no row for the Run, its `orca task-list <run>` source `unscanned`), "...: tab map unreadable" (`ccsession orca-tabs` source `unscanned`). Tests `test_classify.py:971-1068`. Known gap stated in code: a worker-list row with a missing or empty Dispatch id is dropped and no case reads it (`classify.py:693-695`, `probes.py:1222-1224`).
- `unobservable`: any considered row has `session_join is None`.
- `no_join`: considered rows exist and no transcript joined any row.
- `unmatched` (path B only): a considered row has a `session_join` that matches no tab-map key.
- `earlier_pane` (path B only): any considered row exists at all.

### 4.5 `person_started` for a transcript that joined no Orca row (`_person_origin` `classify.py:760-779`)

In order: start with the `origin` notes. If the transcript was left by a tail, window or several-rows rule: add that note, return None. Add "could not join Orca workers to transcripts (tab map empty or stale)" when `no_join` or `unmatched`; add "tab map join not observable" when `unobservable`; add "earlier pane session not joinable (tab map keeps only the latest session)" when `earlier_pane` and the transcript has no tab-map entry; add "Orca pane session, not in scoped Runs" when it has an entry. Return None if any of: `origin` non-empty, any guard flag set, or it has an entry. Otherwise return True and add "origin not proved: no tab-map entry; may be a worker of a Run outside the scope".

Consequence under the shipped `JOIN_PATH = "B"`: `earlier_pane` is true whenever any non-ready Orca Dispatch row exists, so True (and thus `idle` or `person session (active)`) occurs only in a sweep with no non-ready Dispatch rows in the scoped Runs, a readable tab map and a complete worker list, for a transcript with no tab-map entry. With any Dispatch row present, every un-joined transcript is None and prints `could not determine`. Tests: `test_classify.py:1230-1249`, `:1186-1198`, `:1200-1209`, `:1264-1273`, `:957-968` (control, path A).

### 4.6 `_contract_for` (`classify.py:570-591`): which contract belongs to an Orca row

The design says it names no key between a contract and its row (docstring `:571`). Algorithm: `texts` = non-empty `task_spec_text` and `body_text`. `folders` = report folders named by `--report-dir`, `--output-dir` or `--output` values (`models.report_folders` `:29-42`; relative values resolve against `worktree_path`, none if no worktree path). `named` = contracts whose parent folder is in `folders` or whose full path string occurs in a text. If `named` is non-empty: return the single contract, or None when several. Otherwise: needs `worktree_path`; exactly one Orca row in the whole sweep may use that worktree path; exactly one contract may lie under it; return it, else None. A row with no contract cannot be `finished` via rule 6(ii), cannot match rule 1 and cannot be `frozen`. Tests `test_classify.py:1698-1705`, `:1708-1731`.

Key Takeaways
- Both join paths run on every transcript; `JOIN_PATH` only decides the guard cases, which with `"B"` make `person_started True` rare whenever Orca Dispatch rows exist.
- A path-B join needs the Dispatch row's start (and end or open status), a transcript read from byte 0, and exactly one row whose window holds the transcript's first record.
- A contract is attached to an Orca row only by a report folder or path named in the Task text, or by being the only contract under the only row's worktree.

## 5. Safe to close, Removable, package states and shared packages

### 5.1 `safe_to_close(row, worktree)` (`classify.py:479-504`)

Two review values, each from `SAFE_VALUES = ("yes","no","could not determine")` (`models.py:71`), plus a joined reason "terminal: <...>; worktree: <...>".

| Part | Condition (first match) | Value |
|---|---|---|
| terminal | no Orca row | `could not determine` ("no Orca row; terminal not observed") |
| terminal | `terminal_state == "retained"` | `no` ("terminal retained") |
| terminal | `terminal_state is None` or `next_action is None` | `could not determine` ("not observed") |
| terminal | `terminal_state == "reclaimable"` and `next_action == "release"` | `could not determine` ("result read not observable") |
| terminal | anything else | `no` ("not releasable") |
| worktree | worktree None | `could not determine` ("worktree not observed") |
| worktree | else | `removable(worktree)` (5.2) |

`terminal_state` and `next_action` are parsed from `projection.resource.terminalState` (or the list row's `terminalState`) and `projection.nextAction.kind` (`probes.py:502-514`). The captured exited worker carries `terminalState "released"` and `nextAction.kind "none"` (`captured-worker-show-1.json:146`, `:149`), so its terminal value would be `no` ("not releasable"). Tests: `test_classify.py:1613-1633` (seven parametrized terminal cases; the `reclaimable` + `release` case is `could not determine`).

### 5.2 `removable(worktree)` (`classify.py:455-476`)

Returns `("no", <first condition>)` or `("could not determine", <reason>)`. Order: `uncommitted is True` ("uncommitted changes"); `unpushed is True` ("unpushed branch: <upstream_note or ahead>"); `upstream_note == "no upstream"` ("unpushed branch: no upstream"); `dev_tasks_unsaved is True` ("unsaved path under .dev/tasks/"); `frozen is True` ("frozen plan"); first package (sorted by id, location) whose recomputed state is `unfinished`, `archive-blocked`, `interrupted-archive` or `conflict` ("package <id> is <state>"); non-empty `shared_package_ids` ("active package <id> shared with another worktree"); then `status_read` False gives `could not determine` ("unscanned: worktree not readable"); else `could not determine` ("report read, open PR and unmerged commits not observable", `REASON_NOT_OBSERVABLE` `:88-90`). Tests: `:1636-1695` (one per condition, first condition wins, archived does not block). `frozen` is set by `_prepare_worktrees` (`:843-867`) on a worktree that hosts a row with `policy_of == "frozen"` (`:941-948`; test `:1708-1731`).

### 5.3 Package states (`package_state` `classify.py:423-429`, tests table `:408-414`, order `models.PACKAGE_STATES` `:62-69`)

| State | Firing condition (`PackageRecord`) | Blocks worktree removal | Proving test |
|---|---|---|---|
| `conflict` | `location == "both"` (same id under `to-do/` and `done/`) | yes | `test_classify.py:1787-1790` (fixture `PACKAGE_FIXTURES["conflict"]` `:1773-1776`), `:1806-1817` |
| `interrupted-archive` | `archiving_marker` True (any location) | yes | `:1772`, `:1810-1811` |
| `archive-blocked` | `location == "to-do"` and `has_final_line is True` | yes | `:1771`, `:1797`, `:1812` |
| `unfinished` | `location == "to-do"` and `has_final_line is False` | yes | `:1770`, `:1796` |
| `archived` | `location == "done"` | no | `:1777` |
| `unknown` | none of the above (for example `to-do` with `has_final_line None`, an unreadable ledger) | no | `:1764-1767`, `:1778`, `:1813` |

`FINAL:` counts only at the start of a line after optional spaces (`:1793-1803`). Shared packages: `mark_shared_packages` (`:432-452`) flags an id that is `active is True` in two or more worktrees; tests `:1833-1871`.

Key Takeaways
- `Safe to close` and `Removable` can only print `no` or `could not determine`; no branch in `safe_to_close` or `removable` returns `yes` (section 7 applies the C8 test).
- The one terminal combination that comes closest to `yes` (`reclaimable` plus `release`) is deliberately held at `could not determine` because "result read" has no data source.

## 6. Which test and which fixture proves what (consolidated map)

Fixture folder `tests/sweep/fixtures/` holds 20 `captured-*.json` files and `SOURCES.md` (Glob: 21 entries). Capture date of the 5 exited workers: 2026-11-11 (Run `run_a4723d345399`, Orca `1.4.245-aidev02.9cfecdd30b2a`); `captured-worker-show-running.json` from the second Q24 capture, 2026-11-16 (`SOURCES.md:3`, `:25`, `:42`).

| Fixture | Used by (file:line) | What it proves for the classifier |
|---|---|---|
| `captured-worker-show-running.json` | `test_cli_contract.py:1134`; `test_probes_allowlist.py:1640`, `:1693` | Real live worker parses to `live` / `in_progress` / `agentWait` present and null, and prints `working` (rule 5). |
| `captured-worker-show-1.json` (exited, `outcome succeeded`, `liveness.verdict exited`, `source resource_release`) | `test_cli_contract.py:1164`; `test_probes_allowlist.py:1655`, `:1719` | A real exited worker parses with no `agentWait` key and is NOT `working` (it prints `could not determine`: rule 2 declines because `worker_done_seen` is None, rule 6 needs a contract). It carries no key that could feed `worker_done_seen` or `fenced_evidence`: Grep of the file for done/fence/settle/report/outcome/exit keys returns only `projection.stage.detail "settled"`, `projection.outcome`, `projection.liveness.verdict`, `terminal.exitCause.kind "operator_close"` and `observation.status "exited"`. |
| `captured-worker-show-2.json` to `-5.json`, `captured-worker-list.json`, `captured-task-list.json`, `captured-task-list-ready.json` (empty), `captured-worktree-ps.json` | `test_cli_contract.py:813-826`; `test_probes_allowlist.py:349-356` | The five-worker world used by the collect and end-to-end tests; no classifier-rule claim of their own. |
| `captured-tab-map-1.json` to `-5.json` | not referenced by any `tests/**/*.py` (Grep for `captured-tab` and `tab-map` over `tests/**/*.py`: only comments and note strings in `test_classify.py` and `test_report.py`, no file load) | They exist as the record of the join facts in `SOURCES.md:9`; the path-B join tests use synthetic `entry()` objects (`test_classify.py:194-197`). **[CODE-VERIFIED]** no test reads them. |
| `captured-worker-list-unknown-run.json`, `captured-task-list-unknown-run.json` | `test_cli_contract.py:336-337` | The "Run not confirmed" source pair of the guard (4.4). |
| `captured-run-current.json`, `captured-worktree-*.json` | not classifier inputs | Run binding and worktree discovery. |

Key Takeaways
- Only rule 5 has a captured-fixture proof; every other rule is proven by in-memory fixtures built from field names the captures confirmed.
- No fixture, captured or synthetic file, shows a stalled or fenced worker; stalled/fenced exist only as hand-set `OrcaObservation` fields in test code.

## 7. Producer search: does anything set `worker_done_seen` or `fenced_evidence`?

Answer: **no producer exists anywhere in the snapshot.** Evidence (all on origin/master 61ac2c2e6 snapshot):

1. Whole-snapshot Grep for `worker_done_seen|fenced_evidence` (every file type, including skills, scripts, hooks and tests) returns only: `src/superclaude/cli/sweep/models.py:108-109` (the two field declarations, defaults `None` and `"unreadable"`); `src/superclaude/cli/sweep/classify.py:198-199`, `:202`, `:206`, `:221-222` (readers only); `tests/sweep/test_classify.py` lines 300-301, 308, 589, 599, 613-614, 630, 639, 766-767 (11 hits, all constructor arguments in hand-built test objects); `tests/sweep/test_report.py:353` (the text "fenced_evidence present" inside a hand-built report row); `docs/designs/orchestrator-mode.md:60` and `:493` (prose). A second pass over the whole tree for the phrase forms (`stalled (proved)`, `stalled and fenced`) found only docs, the command, the skill, the report footnote and the CHANGELOG, never code that sets the inputs. `skills/`, `scripts/` and `hooks/` contain no hit.
2. The only two places that construct an `OrcaObservation` in production code are `probes.parse_worker_show` (`probes.py:483-515`) and the ready-Task row (`probes.py:1255-1260`). Neither passes either field. The two `dataclasses.replace` calls on observations (`probes.py:1239-1242`, `:1303-1305`) change only `dispatch_status`, `task_spec_text` and `body_text`. `classify._merge_group` (`classify.py:512-525`) only copies equal values or falls back to field defaults. No `setattr`, `object.__setattr__` or `__dict__` write appears in `classify.py` or `probes.py` (Grep in probes: no match; classify read in full).
3. Call graph of the readers: `commands.py:269` `probes.collect` -> `commands.py:271` `classify_all` -> `classify()` -> `RULES` -> `_rule_orca_exit_proof` / `_rule_fenced` (`classify.py:215-223`) and the decline-note harvest `_exit_proof` (`:378`). Nothing between `collect` and `classify_all` writes the fields.
4. Therefore in every real run `worker_done_seen is None` and `fenced_evidence == "unreadable"` for every Orca row. Rule 2 needs `worker_done_seen is False` AND `fenced_evidence == "absent"`; rule 3 needs `fenced_evidence == "present"`; none of the three values can occur. A side effect that does occur on every exited row with a readable transcript: the decline note "Orca: exited; fenced evidence not readable" (`classify.py:205-208`), which the live check recorded on all five exited workers (task-package file `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/sweep-live-check-1.4.md:29`, read via `git show origin/master:`).
5. Neighbouring data that exists but is not used for these two fields: the captured Task `result` JSON of completed Tasks carries `"provenance":"worker_report"`, `"outcome":"succeeded"`, `"messageId"` and `"reportedBy"` (`tests/sweep/fixtures/captured-task-list.json:21`, `:38`, `:55`, `:72`, `:89`). The sweep reads only the `body` key of that JSON (`probes._task_body` `probes.py:1080-1084`). This shows presence of a worker report for completed Tasks; it is not proof of ABSENCE of a `worker_done`, which rule 2 needs. Whether Orca exposes an absence proof is **[UNVERIFIED]** here; the SPEC says "no named live source establishes its absence" (SPEC line 232).

Key Takeaways
- Rule 2 and rule 3 are real engines with no production input: dead-guarded on live data, live only with hand-set fixtures.
- The only visible effect of the missing producer on live rows is the decline note on exited rows.

## 8. C8 candidate analysis (behavioral reachability)

C8 test applied: an in-scope capability that a spec or design names, whose engine exists, but whose guard can never be true at the runtime entrypoint. Four candidates, as the brief requires: `stalled (proved)`, `fenced`, `Safe to close`, `Removable`. I quote the declaring text, give the code evidence, and quote any on-record scope decision. This research created no remediation task and opened nothing on GitHub (read-only brief).

### 8.1 `stalled (proved)` (rule 2 `orca_exit_proof`)

Declared by (quotes are exact):
- `src/superclaude/commands/sweep.md:14`: "The report puts every session into one of eight classes (for example working, waiting on a person, idle, finished, stalled (proved), or could not determine)."
- `src/superclaude/commands/sweep.md:16`: "In Phase 1 the classes stalled (proved) and fenced are not observed, so a zero count there means nothing; the report says so."
- `src/superclaude/skills/sc-sweep-protocol/SKILL.md:26`: "In Phase 1 the classes stalled (proved) and fenced are not observed, so a zero count there means nothing; the report says so. Print each of those two counts with the mark `(not observed in Phase 1)` after the number".
- `src/superclaude/core/WORKER-CONTRACT.md:289` (WC-16): "The `/sc:sweep` classes follow WC-10: only Orca's stall proofs make a worker stalled; anything else it cannot prove is could not determine." WC-16 names the stalled behavior; the word `fenced` does not occur in WC-16 (Grep: `fenced` appears in that file only at lines 61 and 63, both as Orca's `consumer_fenced`, a different thing). So the brief's premise that WC-16 names both classes is half right: stalled yes, `fenced` no.
- `docs/designs/orchestrator-mode.md:481` (rule table, rule 2 -> stalled (proved)) and SPEC FR-009 (`SPEC` line 103): "Stalled (proved) only from Orca's own exit proof with no `worker_done` and no fencing evidence".
- `src/superclaude/cli/sweep/report.py:42-45` (`SP24_LINE`), printed in `## Sessions` (`report.py:411`), pinned by `tests/sweep/test_report.py:73`, `:1066-1067`: "Stalled and fenced are not observed in Phase 1; a zero count does not mean none occurred."

Code evidence it cannot fire in Phase 1: section 7 (no producer; defaults `None` and `"unreadable"`; rule 2 needs `False` and `"absent"`).

On-record scope decision (spec level): SPEC (`origin/master:.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md`) line 232: "`worker_done_seen` is None on live rows, because no named live source establishes its absence. Stalled (proved) stays fixture-only until a source mapping exists. Missing proof never becomes False. [V1R3:41, V2R3:43, V3R3:52; INV-006; Change 10]". SPEC line 231: `fenced_evidence` is "always `unreadable` on live rows in Phase 1, REPORT step 1.3 rule 3". Carried into the design at `docs/designs/orchestrator-mode.md:493` ("`worker_done_seen` is None on every live row; `fenced_evidence` is `unreadable` on every live row (SPEC line 231)") and as deviation D7 (`:841`: "the report adds the footnote that stalled and fenced are not observed in Phase 1 and a zero count does not mean none occurred", source SP-24, applied in 7.2 and 7.5; panel-notes row `:877`). Public-facing statements: `CHANGELOG.md:170`, `docs/user-guide/commands.md:619`.

Determination: **not a DEFECT-CANDIDATE under the C8 rule, because a cited, spec-level scope decision exists** (SPEC:232 plus design D7). The capability is a documented deferral "until a source mapping exists". Residual points for the owner (statements of fact, no recommendation):
1. The deferral is conditional on "a source mapping" and no work item owning that mapping was found: `gh search issues --repo IronbellyOrg/IronClaude "worker_done_seen"` and `"sweep stalled fenced"` returned no issue (a search, not an exhaustive scan); issue #534 (open) lists owner-ruled limitations FIN-F7 and D-01 only and its text does not name stalled or fenced; its later comments are about paging and Rule 5. Remediation task not created (read-only brief); flagged for the owner.
2. The spec-level decision is attributed to review inputs (V1R3, V2R3, V3R3, INV-006, Change 10), not to a dated owner ruling. I found no owner ruling that names stalled or fenced (searched the Phase 1 plan files on origin/master for `worker_done_seen|fenced_evidence|stalled (proved)|stalled and fenced`: no hit).
3. The reason printed in `CHANGELOG.md:170` and `docs/user-guide/commands.md:619-620` for stalled/fenced ("because the live `agentWait` names were never captured (design open item 6)") does not match the SPEC's reason ("no named live source establishes its absence"). Design open item 6 (`orchestrator-mode.md:1003`) is about `agentWait`, `liveness.verdict` and `status` names and is marked resolved 2026-11-16 for a running worker. **[STALE DOC]** (reason misattributed).

### 8.2 `fenced` (rule 3)

Declared by: the same `commands/sweep.md:14`/`:16`, `SKILL.md:26`, `report.py:42-45`, `report.py:59` (`NEXT_INSPECTION["fenced"] = "read the fencing evidence named in the row"`), design rule table `orchestrator-mode.md:482`, SPEC rule table line 251. Not in WC-16 (see 8.1). Code evidence: section 7; `fenced_evidence` is `"unreadable"` on every live row (`models.py:109`), rule 3 requires `"present"` (`classify.py:221`). On-record scope decision: SPEC line 251: "`fenced_evidence == "present"` (synthetic fixtures only in Phase 1)"; SPEC line 231 (always `unreadable` on live rows in Phase 1); design `:493`, D7 `:841`. Determination: **same as 8.1; not a DEFECT-CANDIDATE, cited spec-level scope decision exists.** One extra fact: unlike `stalled`, the SPEC rule text for `fenced` gives no "until" condition at all (no named future source mapping). Remediation task not created (read-only brief); flagged for the owner.

### 8.3 `Safe to close`

Declared by: SPEC FR-012 (line 106): "Safe-to-close is a separate two-part REVIEW value (terminal, worktree), each `yes`, `no` or `could not determine`. Phase 1 never prints `worktree removable: yes`."; SPEC FR-017 (line 111) and line 167: "`safe_to_close` is never yes in Phase 1"; design traceability row FR-012 (`orchestrator-mode.md:794`); `commands/sweep.md:16` and `SKILL.md:66` name `Safe to close` as a stated fact to review (neither file says it never prints yes); `report.py:46-49` (`SAFE_TO_CLOSE_LINE`): "Safe to close never prints yes in Phase 1: each cell gives the terminal value, the worktree value and, in parentheses, the reason for both."; `CHANGELOG.md:171`; `docs/user-guide/commands.md:621`. Code evidence: `safe_to_close` (`classify.py:479-504`) has no branch that returns `"yes"` for `terminal` or `worktree`; the closest branch (`reclaimable` + `release`) returns `could not determine` with reason "result read not observable" (`:491-493`). Tests pin the never-yes outcome (`test_classify.py:246-248` inside the `run()` helper for every classify fixture, `:1613-1633`; `test_report.py:1172`). On-record scope decision: SPEC line 274: "Terminal releasable needs `terminal_state == "reclaimable"`, `next_action == "release"` and the result already read; the read is not observable, so Phase 1 prints `could not determine (result read not observable)` plus the Orca values". Determination: **not a DEFECT-CANDIDATE; cited spec-level scope decision.** Note for the reader: only the report footnote and the CHANGELOG/user guide say "never yes"; the command and the skill do not.

### 8.4 `Removable`

Declared by: SPEC FR-012 (line 106) and FR-013 (`SPEC` line 107, the "removable: no with the condition named" list); SPEC line 274: "Worktree removable prints `no` with the first observed condition from FR-013, else `could not determine (report read, open PR and unmerged commits not observable)`."; SPEC line 338: "Unmerged commits and open PRs are not observed in Phase 1; that is acceptable because worktree removable is never `yes` (FR-012)."; design `orchestrator-mode.md:795`; `CHANGELOG.md:171` ("`Safe to close` and `Removable` never say `yes`"). Code evidence: `removable` (`classify.py:455-476`) returns only `"no"` or `"could not determine"`; the last return is the constant reason `REASON_NOT_OBSERVABLE` (`:88-90`, `:476`); `WorktreeState.removable` defaults to `"could not determine"` (`models.py:208`). Tests: `test_classify.py:247-248`, `:1679-1695`. On-record scope decision: SPEC lines 106, 274 and 338 (quoted above). Determination: **not a DEFECT-CANDIDATE; cited spec-level scope decision, with the stated reason that the open-PR and unmerged-commit facts have no Phase 1 source** (`git log`, `git branch`, `git rev-parse` and `gh` reads are excluded, SPEC line 338 and design section 1 "Out of scope for Phase 1 ... `gh` reads").

### 8.5 Adjacent in-scope items that share the same shape (not requested; stated so synthesis does not miss them)

- Rule 4(a) and the Waiting (a) age from `agentWait`: `OrcaObservation.agent_wait_since` is never set (`models.py:111-112`, `probes.py:481`); a non-null `agentWait` was never captured, so rule 4(a) cannot be shown to fire on live data (`models.py:98-99`; design open item 6 `:1003`). Scope text exists: SPEC "the `agentWait` timestamp field captured in step 1.0a (UNVERIFIED field). With no `t`, the row is in the unknown-age group". Not a defect candidate on the same basis.
- `phase`, `approval`, `admission`, `evidence_packet` and `tests_review` dimensions: always `unknown` or None (section 2). SPEC section 7 (line 235) says the ten #409 dimensions default to `unknown`.

Key Takeaways
- For all four candidates a cited spec-level scope decision exists (SPEC lines 106, 231-232, 251, 274, 338; design D7 and line 493), so none is recorded as a DEFECT-CANDIDATE; remediation task not created (read-only brief); flagged for the owner where the deferral has no tracked owner.
- WC-16 names `stalled` only; `fenced` appears in no contract text.
- The public wording of the reason for stalled/fenced (CHANGELOG, user guide) is out of line with the SPEC's reason.

## 9. What real runs reported (recorded evidence, not re-run by me)

| Source | Reported result | How it bears on row meaning |
|---|---|---|
| Task-package record `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/sweep-live-check-1.4.md:19` and `:29`, and its Step 4 result paragraph (origin/master; live run 2026-11-12 on Run `run_a4723d345399`, 5 exited workers) | All 180 rows (5 Orca rows plus 175 transcript rows) printed `could not determine`; the 5 workers carried the notes "Orca: exited; fenced evidence not readable" and "session start not observable: transcript tail only"; the record states the transcript tails were longer than 256 KiB (`tail_complete` false). | Confirms sections 3 and 7 on real data: no contract read gives no `finished`; the 256 KiB tail limit forced the join to `could not determine`. This file predates the 2026-11-16 Rule 5 restoration. |
| Issue IronbellyOrg/IronClaude#590 (open, 2026-11-17, `gh issue view` body) | A live run over Run `run_93bfa00cae2b` found 264 sessions: waiting 1, could not determine 263, working 0, finished 0, idle 0. Two causes named by the reporter: the show cap of 50 (rows never looked up have `liveness_verdict None, outcome None, status None`) and "no contract read" for looked-up finished rows. The reporter says the cause split was not measured (about 10 rows read) and that `working 0` was not checked row by row. | Third-party report of the same fall-through paths (rule 9 and the no-contract note). **[UNVERIFIED]** by me: I did not open the report file or re-run the sweep. |
| Issue #534 comments (read in part; each comment body cut to 400 characters by my query) | Owner decision 2026-11-17: page past the 50-read cap; #590 named the first wave 3 sweep follow-up. | Planned change to the show cap; no comment seen about a producer for stalled or fenced. |

Key Takeaways
- Both live reports show the same dominant outcome: almost every row prints `could not determine`; a cap, a missing contract or a join limit usually explains it, never a stalled/fenced proof.

## Gaps and Questions

Open questions and everything marked UNVERIFIED or CODE-CONTRADICTED above.

1. **[UNVERIFIED]** Whether Orca exposes any field that proves the absence of a `worker_done` (needed for `worker_done_seen is False`) or evidence of fencing. The SPEC says "no named live source" (SPEC line 232). The captured Task `result` JSON shows `provenance: worker_report` for completed Tasks (presence only), and `consumer_fenced` is a state of Orca's `check` call in WORKER-CONTRACT (`WORKER-CONTRACT.md:61`, `:63`), not a field the sweep reads. Nobody in the files read has mapped either to `worker_done_seen` / `fenced_evidence`.
2. No work item owns the "source mapping" that SPEC line 232 makes the condition for lifting `stalled (proved)`. `gh search issues` found none (search not exhaustive). Remediation task not created (read-only brief); flagged for the owner.
3. No dated owner ruling that names `stalled (proved)` or `fenced` as out of scope was found. The scope text is spec-level (SPEC lines 231-232, 251; design D7). Issue #534's owner-ruled limitations are FIN-F7 and D-01 only.
4. **[CODE-CONTRADICTED]** `CHANGELOG.md:170` and `docs/user-guide/commands.md:620` say `working` is never produced; code and tests show it is (section 0). Both also give the `agentWait` capture gap as the reason for stalled/fenced, which differs from the SPEC reason (8.1 point 3).
5. **[CODE-CONTRADICTED]** `docs/designs/orchestrator-mode.md:27` ("`src/superclaude/cli/sweep/` does not exist yet").
6. **[UNVERIFIED]** `agentWait` non-null shape and meaning (never captured; `models.py:98-99`); therefore rule 4(a) is unproven on live data and `agent_wait_since` is never set.
7. **[UNVERIFIED]** How often real worker transcripts exceed 256 KiB. One recorded check (5 workers, 2026-11-12) says all five did; issue #590's live run did not report it.
8. **[UNVERIFIED]** Whether production ever produces a path-A join: `session_join` holds `dispatch.assigneeHandle` (`term_<uuid>` in the captured data); path A matches only if a transcript session id equals that string. I read no run where it did.
9. Issue #534's body still says Rule 5 is inert (body item 2); its own later comment says PR #579 restored it. I read only the first 400 characters of each comment, so the exact wording is **[UNVERIFIED]**.
10. Not read: `probes.py` outside the lines cited (collect, budget, allowlist), `report.py` beyond lines 1-120 and the cited lines, `commands.py` beyond its import/call lines. The class meanings above do not depend on them.
11. The sweep's `person_started` True case (idle and person-active rows) was only checked by reading code and tests; I found no recorded live row of either class.

## Stale Documentation Found

| Doc | Line | Stale statement | Current code | Marker |
|---|---|---|---|---|
| `docs/designs/orchestrator-mode.md` | 27 | `src/superclaude/cli/sweep/` does not exist yet | package exists (6 `.py` files) | **[STALE DOC]** **[CODE-CONTRADICTED]** |
| `CHANGELOG.md` | 170 | `working` is never produced; reason for stalled/fenced is the `agentWait` capture gap | rule 5 active (`classify.py:251-269`, `test_cli_contract.py:1133-1140`); reason in SPEC:232 differs | **[STALE DOC]** **[CODE-CONTRADICTED]** |
| `docs/user-guide/commands.md` | 620 | `working` is never produced yet; healthy workers read `could not determine`; rows waiting from an agent wait cannot match on live data | rule 5 active (same evidence); the agent-wait part of the sentence is still unverified | **[STALE DOC]** (first clause) |
| `docs/designs/orchestrator-mode.md` | 1003 vs CHANGELOG 170 | Open item 6 says resolved 2026-11-16 while the CHANGELOG cites it as the reason for a current limit | n/a | inconsistency between docs |
| Issue #534 body | item 2 | Rule 5 inert | superseded by PR #579 (per its comment) | **[STALE DOC]** (comment-level verification only) |

## Summary

The classifier has nine ordered rules and eight classes; the first matching rule wins, but a later step can still turn a row into `could not determine` when its transcript is unreadable, a join is ambiguous or limited by the 256 KiB tail, Dispatch ids conflict, or a named source is unscanned. `working` fires on live data since the 2026-11-16 capture; `waiting on a person`, `finished`, `idle` and `person session (active)` fire from contract, Task and transcript data, with `person_started True` rare whenever Orca Dispatch rows exist because the shipped join path is B. `stalled (proved)` and `fenced` cannot fire in any real run: nothing in the snapshot sets `worker_done_seen` or `fenced_evidence`, and the SPEC (lines 231-232, 251) and design D7 record that as a Phase 1 limit, so I record no DEFECT-CANDIDATE, while flagging that no work item owns the missing source mapping and that CHANGELOG and the user guide state a different reason and wrongly say `working` is never produced. `Safe to close` and `Removable` never print `yes` by construction, with SPEC lines 106, 274 and 338 as the on-record decision. No fixture file proves rules 1 to 4 or 6 to 9; they are proven by in-memory builders, and only rule 5 has a captured-fixture proof.


see gapfill-c1-GF4-public-entry-points.md for the resolution of GF-4 (public entry-point signatures and the rule contract; `_classification` is at classify.py:130, not :222).

- see gapfill-c1-GF1-c8-reconciliation.md for the resolution of GF-1 and gapfill-c1-GF2-commands-md-claim.md for the resolution of GF-2 (the commands.md:619-620 claim in s8.1 point 3, s8 Takeaways and Gaps 4 is narrowed to CHANGELOG.md:170).
