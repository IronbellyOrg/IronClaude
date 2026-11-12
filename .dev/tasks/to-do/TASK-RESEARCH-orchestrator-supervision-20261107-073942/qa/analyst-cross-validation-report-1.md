# Cross-Validation Report (Partition 1 of 2)

**Topic:** Orchestrator mode Phase 1 (issue #339), read-only coordinator `/sc:sweep`
**Date:** 2026-11-07
**Analysis type:** cross-validation (checklist items 6, 7, 8)
**Depth tier:** Deep
**Fix authorization:** false (read-only; no research file edited)
**Assigned files:** `research/scope-01-contract.md` (152 lines), `research/scope-02-orca-recovery.md` (235 lines), `research/05-orca-row-schema.md` (201 lines)
**Reference input:** `research/research-notes.md` (306 lines; AMBIGUITIES 1-11, contradictions C1-C12)

Pre-run sha256 of the assigned files (to prove no edit):

- `scope-01-contract.md` `5ed83912...b3c719`
- `scope-02-orca-recovery.md` `b8ceb020...0d8fa8d`
- `05-orca-row-schema.md` `8d444571...82ba6`

[PARTITION NOTE: Cross-file checks limited to assigned subset. Full cross-file analysis requires merging all partition reports.]

---

## Item 6. Contradiction detection

Each finding cites both sides. Line numbers were re-read in this run. Capture files are under `.dev/tasks/done/TASK-WF-p1LivePlanBrief-20261105-164506/artifacts/`. Help lines are numbered `orca-ide orchestration <verb> --help` output on CLI 1.4.245.

### F1. IMPORTANT. Three classifier mappings disagree, and none places every row in exactly one class

| Class | research-notes.md C (:184-193) | scope-02 (:97-103) | 05 (:167-176) |
|---|---|---|---|
| waiting on a person | agentWait non-null, OR `worker_status: blocked` + `blocked_question`, OR Ruling halt, OR frozen implement plan, OR foreign ready Task (:186) | agentWait non-null, or "an `ask` pending" (:100) | non-null agentWait only (:172) |
| finished | outcome settled AND contract read; sub-states include `failed` and `blocked` (:190) | outcome succeeded/failed + settled + attention (:102) | outcome succeeded/failed (:171) |
| could not determine | unverifiable, stale, Orca down, late heartbeat, unreadable log (:189) | unverifiable (:101) | unverifiable, **or agentWait absent** (:175) |
| idle | person-started session, no Orca Task, no activity in window (:191) | not defined | **settled and terminalState retained or released** (:176) |
| safe to close | separate dimension: reclaimable + nextAction release + all five refusal conditions clear (:193) | reclaimable + nextAction release, **no refusal conditions** (:103) | not mapped |

The contradictions:

- (a) **Blocked is in two classes in the notes.** A `blocked` contract matches both "waiting on a person" (:186) and the "finished" sub-state `blocked` (:190). WC-5 also maps `blocked` to Orca outcome `failed` (`WORKER-CONTRACT.md:58`), so a blocked worker's Orca row reads as finished. 05:171 and scope-02:102 send it to "finished" with no contract read, and the person who needs to answer it never sees it.
- (b) **Idle has two meanings.** In the notes, idle is a person-started session (:191). In 05, idle is a settled Orca worker (:176). 05's idle also overlaps its own "finished" row: every settled row with terminalState `retained` or `released` meets both :171 and :176. The capture `lc16-show-4.json:145-151` shows a **working** worker (outcome `in_progress`, :134) with `terminalState: retained` and `releaseState: retained` (`retainedReason: user_takeover`, :191). So `retained` does not mean idle (see F12).
- (c) **scope-02 safe-to-close drops the refusal list.** scope-02:103 treats reclaimable + `nextAction release` as enough. `WORKER-CONTRACT.md:108` refuses removal while there are unmerged commits, an open PR, uncommitted changes, an unfinished implement ledger, or an unread report. The `lc17-show-1.json:145-160` failed worker is reclaimable with a release nextAction, yet its report may be unread. The notes (:193) are correct; scope-02 is not.
- (d) **05 treats agentWait absent as "could not determine".** At 05:175, an absent agentWait makes the row "could not determine". The `worker-show --help` line 16 text says absent means "it never looked", not "worker state unknown". On a settled row the outcome is still known, so 05 would wrongly move finished rows to "could not determine" wherever agentWait is missing.
- (e) **None of the three is checked against the issue's five literal classes.** 05 never maps the issue's classes. scope-02 maps neither "idle" nor "timed out". Only the notes do (:184-191), and they label the mapping DERIVED.

**Remediation:** synthesis must adopt one mapping with a written precedence order:

1. Read the contract before outcome: a `blocked` contract becomes "waiting on a person" and is never listed as finished.
2. Proved stall.
3. Waiting on a person.
4. Working.
5. Finished.
6. Could not determine.

Keep "idle" only for person-started sessions (the notes' meaning) and drop 05:176. Keep safe-to-close as a separate dimension that requires all five `WORKER-CONTRACT.md:108` conditions. Record scope-02:103 and 05:175-176 as superseded in C13 (F4).

### F2. IMPORTANT. The transcript stall proof does not say what "final" means, which risks breaking WC-10

The notes (:188) and scope-02 (:101) accept "a final transcript turn with no `worker_done`" as positive stall proof. Both cite the guide text at `orca-capabilities.md:126`. For a live worker, the latest transcript turn is always one "with no `worker_done`" until the worker finishes. Without a rule that the turn is *final* (the agent process ended, or the turn ended with the agent idle at its prompt), a sweep would label every busy worker "stalled". That is the death-from-absence inference that WC-10 forbids (`WORKER-CONTRACT.md:45`).

05:174 cites `[G]` 156-158 for "other positive proof" and does not spell the proof out.

**Remediation:** define "final turn" before synthesis. Either require it together with `exited` liveness or a process-exit observation, or define an observable end-of-turn marker from a `worker-read --source transcript` capture. Until then, treat the transcript test alone as "could not determine".

### F3. MINOR. `liveness.reason` is listed as a captured field but is guide-only

The scope-02 field table at :64 lists `projection.liveness.{verdict,reason,observedAt,source}` under a header that claims "CODE-VERIFIED for every row except the parts marked UNVERIFIED" (:53). `reason` is not marked. No capture has it: `lc16-show-4.json:135-139`, `lc17-show-1.json:135-139` and `lc01-show-1.json:135-139` all hold only `verdict`, `observedAt` and `source`. scope-02's own open question 2 (:218) and 05 gap 3 (:184) admit this, so the error is the missing tag, not hidden ignorance.

**Remediation:** tag `reason` as `[UNVERIFIED: guide text orca-capabilities.md:127; absent from every capture]`, and require the sweep to tolerate a missing `reason`.

### F4. IMPORTANT. The Orca command names in data sources B are wrong, and C1-C12 does not record it

The notes' data-sources table writes `orca-ide worker-list ...` (:168), `orca-ide worker-show ...` (:169) and `orca-ide worker-read ...` (:170). On 1.4.245 these are subcommands of `orchestration`, and top-level `orca-ide worker-list` prints "Unknown command". scope-02 itself cites the correct `orchestration worker-list --help` (:40, :91), yet its summary leads with the short form, so the notes table copied the short form.

Contradictions C1-C12 (notes :291-304) do not record this, nor the F1 mapping conflicts.

**Remediation:** add C13 (command name: always `orca-ide orchestration <verb>`) and C14 (the F1 mapping conflicts) to the notes during synthesis. Every command a sweep design prints must use the full form.

### F5. IMPORTANT. Nested-worker rules are left unreconciled; a sweep must handle a non-null `parent`

05 gap 8 (:189) and its stale-doc list (:197) report that current guide `[G]` 130-131 says a dispatched worker starts helpers with `worker-start --spec`. `orca-capabilities.md:97-102` (depth 1, `nested_worker_depth_exceeded`) says it cannot. WC-8 and WC-13 (`WORKER-CONTRACT.md:39`, `:61`) forbid it at any depth setting. scope-01's sweep-bound rule list (item 3) cites WC-8 and WC-13 but not the guide change. Neither file says what the sweep does with a row whose `parent` is non-null (`lc16-show-4.json:115` shows `parent: null`).

**Remediation:** synthesis records the guide change as a contradiction. The sweep reports a non-null-`parent` row as a WC-13 violation for review, and never treats it as a normal worker.

### F6. IMPORTANT. No research shows how the sweep enumerates every Run

05 recommends always passing `--run` (05 summary). scope-02:113 says that without `--run` the list covers the Run bound to the calling terminal, or every Run when there is no binding (`worker-list --help` line 22). The sweep's goal is every worker in the tree. Neither file shows:

- how a coordinator terminal that is bound to one Run lists the others;
- how Run IDs are discovered;
- whether the unbound "all" scope includes context-only Dispatches (help line 20 says they appear as unsupervised and retained).

Under the notes' table (:168), `[--run <id>]` is optional, which hides the problem.

**Remediation:** research or decide Run discovery before design. Options: a read-only Run listing verb, if one exists, or always running the sweep from an unbound context and printing `scope.source`. Record the choice as an open question.

### F7. IMPORTANT. No capture of a populated worker-list row (G-A residual)

05 gap 1 (:182), scope-02 open question 1 (:217) and the notes' row B (:168) all agree that no capture has a non-empty `workers[]` (`lc01-step7.txt:28` is `[]`). The whole row-first classifier rests on rows carrying `projection.outcome`, `liveness` and `resource`: 05:165 narrows its cost on that basis, and scope-02:99-103 uses the fields. If rows carry only the four guide-named fields, the mapping changes.

**Remediation:** before synthesis fixes the design, the coordinator makes one read-only `orca-ide orchestration worker-list --run <id> --include-remote --json` capture with a live worker and stores it in `artifacts/`. Until then, the design marks the row shape UNVERIFIED and falls back to worker-show per row.

### F8. MINOR. Line drift in cited ranges

- scope-02:68 cites the lc17 attention block at `:162-165`. The object spans `lc17-show-1.json:161-166`. The notes (:63) copy `:162-165`.
- scope-02:66 cites the lc17 resource block at `:145-150`. It spans `:145-151`, and terminalState is at `:150`.
- scope-02:115 cites help lines 10-11 and 21 for remote behaviour. Those lines are `--pairing-code` (:10) and `--environment` (:11). The row's own recommendation, "always pass `--include-remote`", does not cite that flag's line (14).
- 05:174 cites `[G]` 156-158 while the notes (:188) cite `orca-capabilities.md:126` (`[G]` 143-145 in the 1.4.237 numbering). This matches the 13-line guide shift 05 reports (:194), but the synthesis must cite one numbering.

**Remediation:** use the corrected ranges in synthesis and state the guide version beside every `[G]` line.

### F9. MINOR. The notes list stale input line counts

notes:9 gives `scope-01-contract.md (147 lines)` and `scope-02-orca-recovery.md (220)`. The files are now 152 and 235 lines, because scope-02 grew with the 2026-11-07 re-verification notes. So scope line numbers the notes cite from earlier versions may be off.

**Remediation:** re-record the counts, and re-check every scope-01 and scope-02 line the notes cite against the current files.

### F10. MINOR. scope-02 lists "an `ask` pending" as a waiting signal with no observable read

scope-02:100 uses "an `ask` pending", but notes row B (:171) says no non-consuming read path for pending questions is known, and `check --wait` consumes messages (:178, UNVERIFIED). A sweep cannot evaluate the signal. The underlying gap belongs to partition 2 (G-B).

**Remediation:** mark it "no read path (G-B)" in the merged mapping.

### F11. MINOR. 05's cost model depends on an unverified row shape

05:165 skips worker-show for settled rows only "if the row carries outcome/stage", which is UNVERIFIED. This depends on F7.

**Remediation:** state the worst case for the 50-500 session scale: ceil(N/100) list calls plus N show calls.

### F12. MINOR (evidence for F1b). `retained` is not idle

`lc16-show-4.json` is a live, in-progress worker whose `resource` (`:145-151`) reads `state: user_owned`, `releaseState: retained`, `terminalState: retained`, after a user takeover (`:191`). 05:176 would call a settled row with the same resource "idle". terminalState is process accounting, "reported separately from Task status" (`worker-list --help` line 19).

**Remediation:** never derive a state class from `terminalState`. Use it only for the safe-to-close dimension.

---

## Claim cross-validation (sampled, adversarial)

| # | Claim | Source | Checked against | Verdict | Notes |
|---|---|---|---|---|---|
| 1 | `stage.activity` stays `working` after settlement | scope-02:74; 05:178 | lc17-show-1.json:132; lc01-show-1.json:132 | VERIFIED | Both settled captures read `working` |
| 2 | liveness has `reason` | scope-02:64 | lc16/lc17/lc01 `:135-139` | CONTRADICTED (captures) | Guide-only (F3) |
| 3 | lc17 is reclaimable with a release nextAction | scope-02:66-67, :198 | lc17-show-1.json:150, :152-160 | VERIFIED | Range drift (F8) |
| 4 | lc01 attention is `root_completion`, `requiresAction: false` | notes:64; scope-02:68 | lc01-show-1.json:161-166 | VERIFIED | |
| 5 | Without `--run`, the list scope is the bound Run or all Runs | scope-02:113 | `worker-list --help` line 22 | VERIFIED | Enumeration still open (F6) |
| 6 | Max 100 rows per page; `nextCursor` | scope-02:114 | `worker-list --help` lines 16, 21 | VERIFIED | Multi-page behaviour never captured (05 gap 5) |
| 7 | `orca-ide worker-list` is the read command | notes:168 | Live CLI 1.4.245 | CONTRADICTED | Needs `orchestration` (F4) |
| 8 | Safe-to-close = reclaimable + release | scope-02:103 | WORKER-CONTRACT.md:108 | CONTRADICTED (incomplete) | Five refusal conditions missing (F1c) |
| 9 | WC-10: a missing heartbeat is absence, never death | scope-01 rules; notes:182 | WORKER-CONTRACT.md:45 | VERIFIED | F2 risks breaking it |
| 10 | WC-5: blocked maps to outcome failed | scope-01 | WORKER-CONTRACT.md:58 | VERIFIED | Drives F1a |
| 11 | WC-8/WC-13: no fan-out from a command or worker | scope-01 item 3 | WORKER-CONTRACT.md:39, :61 | VERIFIED | Guide change unreconciled (F5) |
| 12 | Depth 1 forbids workers starting workers | 05:189 (via orca-capabilities) | orca-capabilities.md:97-102 | VERIFIED (inventory text; 1.4.237) | Conflicts with current `[G]` 130-131 per 05 |
| 13 | A waiting worker is healthy; null agentWait means looked and found nothing; absent means never looked | scope-02:100; 05:172, :175 | `worker-show --help` line 16; orca-capabilities.md:129 | VERIFIED | 05:175 misapplies "absent" (F1d) |

---

## Item 7. Compiled gaps (deduplicated)

Sources merged:

- this report's findings F1-F12;
- scope-01 gaps G1-G7 (:78-84) and open questions 1-7 (:142-148);
- scope-02 open questions (:217-218);
- 05 gaps 1-9 (:182-190).

Duplicates are collapsed into one row that lists every source.

| # | Gap | Sources | Severity | Remediation |
|---|---|---|---|---|
| 1 | One classifier mapping with precedence; blocked is double-classified; two meanings of idle; safe-to-close without the refusal list | F1, F12; scope-01 G4 (:81), item 9 (:64); scope-02:97-103; 05:167-176; notes C (:184-193) | IMPORTANT | Single mapping with contract-first precedence; idle only for person-started sessions; safe-to-close as a separate five-condition dimension |
| 2 | "Final transcript turn" stall proof is undefined | F2; notes:188; scope-02:101; 05:174 | IMPORTANT | Require exited/process-exit evidence or a defined end-of-turn marker; otherwise "could not determine" |
| 3 | Wrong command form `orca-ide worker-*`, and missing from C1-C12 | F4; notes:168-170 | IMPORTANT | Add C13/C14; always use `orca-ide orchestration <verb>` |
| 4 | Nested workers: current guide vs depth fence vs WC-8/WC-13; handling a non-null `parent` | F5; 05 gap 8 (:189), stale doc (:197); scope-01 item 3 (:58) | IMPORTANT | Record the contradiction; flag non-null-`parent` rows for review |
| 5 | Run enumeration across the tree | F6; scope-02:113; 05 summary (`--run` always) | IMPORTANT | Decide the discovery path; print `scope.source` |
| 6 | No populated worker-list row capture (row shape, cost narrowing) | F7, F11; 05 gap 1 (:182); scope-02 Q1 (:217); notes:168 | IMPORTANT | One read-only coordinator capture; worker-show fallback until then |
| 7 | Person-started sessions: whether the sweep may report them, and from what evidence; the pane-key join is UNVERIFIED | scope-01 G6 (:83), Q7 (:148), item 1 (:56); notes:175 | IMPORTANT | Decide in WC-14; verify the `orca-tabs` to `assigneePaneKey` join |
| 8 | No non-consuming read of a pending `ask` | F10; scope-01 item 8 (:63); scope-02:100; notes:171 | MINOR here (owned by partition 2 as G-B) | Mark "no read path" in the mapping |
| 9 | `liveness.reason`, `unverifiable` and `exited` shapes never captured | F3; 05 gaps 3-4 (:184-185); scope-02 Q2 (:218) | MINOR | Tag guide-only; tolerate missing fields |
| 10 | Non-null `agentWait` shape unknown | 05 gap 2 (:183) | MINOR | Capture when one occurs |
| 11 | Paging past 100 and `counts` keys unproven | 05 gaps 5-6 (:186-187) | MINOR | Loop on `nextCursor`; print the totals |
| 12 | Capture CLI version not recorded (captures predate 1.4.245) | 05 gap 9 (:190) | MINOR | Record the version with any new capture |
| 13 | `stage.activity` meaning after settlement | 05 gap 7 (:188) | MINOR | Already resolved: do not use it |
| 14 | Contract text for WC-14 (re-arm after expiry, periodic sweep, when to tell the person, report location) | scope-01 G1-G3, G5, G7 (:78-84) | MINOR | Insertion points already identified; design work |
| 15 | Rule ID (WC-14 vs WC-1); never-as-worker list update with tests; report folder; write-verb audit entries | scope-01 Q2-Q5 (:143-146) | MINOR | Design decisions; Q5 already answered (`test_worker_contract.py:1090-1094`) |
| 16 | Whether a test requires every command to appear in `/sc:help`/HOW-WE-WORK | scope-01 Q6 (:147) | MINOR | Check before adding `sweep.md` |
| 17 | Line drift and stale input counts | F8, F9; notes:9, :63 | MINOR | Correct the citations in synthesis |

Critical (blocks synthesis): **0**. Important: **7** (rows 1-7). Minor: **10** (rows 8-17).

---

## Item 8. Depth assessment

**Expected depth:** Deep: data-flow traces, integration-point mapping, pattern analysis.

**Achieved depth:** Mostly Deep.

- scope-01 maps every sweep-bound contract rule to a `WORKER-CONTRACT.md` line and gives insertion points (G1-G7).
- scope-02 traces each data source to a capture or help line, with re-verification stamps.
- 05 gives a field-level schema, a cost model and a stale-doc audit.

The evidence tagging is dense, and the errors found are mostly in the derived mappings, not in the raw evidence.

**Missing depth elements:**

1. A populated worker-list row capture (gap 6).
2. Run enumeration across the tree (gap 5).
3. An end-to-end trace of the pane-key join from `orca-tabs` to `dispatch.assigneePaneKey` (gap 7).
4. A defined, observable stall proof from a transcript (gap 2).
5. A reconciled, single classifier with precedence (gap 1). The three files each derive one and none checks the others.

## Recommendations

1. Before synthesis, the orchestrator records C13 (command form) and C14 (classifier conflicts) beside C1-C12 in the merged notes. Research files stay unedited.
2. Synthesis adopts the contract-first classifier from F1, with `idle` reserved for person-started sessions and safe-to-close as a five-condition dimension.
3. Treat the transcript stall test as "could not determine" until "final" is defined (F2).
4. Schedule one read-only, coordinator-run `orca-ide orchestration worker-list --include-remote --json` capture with a live worker (F7), and decide Run discovery (F6).
5. List nested-worker rows (non-null `parent`) as WC-13 review items (F5).
6. Correct the drifted citations (F8, F9) in every synthesis section that reuses them.

## Post-run integrity check

These are the full sha256 values recomputed after writing the report:

- `scope-01-contract.md` `5ed8391297b3e510e1ddf40c00b6f69eb91cf1e1abda4cca5fd7d8cde2b3c719`. It matches the header.
- `scope-02-orca-recovery.md` `b8ceb020dd4f326f9c470a8ab50ade1c253905a3ca17a5cc24383da2fa48fd8d`. The prefix matches; the header's abbreviated suffix `0d8fa8d` does not.
- `05-orca-row-schema.md` `8d444571770273da41de645d7836ffcd46a16591df0beaef22f38ca3ac765b3f`. The prefix matches; the header's abbreviated suffix `82ba6` does not.

The three line counts (152/235/201) are unchanged. The last modification times are 19:01:59, 19:04:42 and 19:05:45 UTC on 2026-11-07, all earlier than this report's final edits. This analyst made no edit to any research file. The two suffix mismatches are most likely transcription errors in the header abbreviations; a concurrent edit by another agent before the header was written cannot be ruled out. Either way, the findings above cite line numbers re-read against the current files.

## Verdict: FAIL
