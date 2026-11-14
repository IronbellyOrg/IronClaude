# QA Report — Fix-cycle verification: Phase 6 source-document fidelity gate

**Topic:** Orchestrator mode Phase 1 (issue #339), research report source fidelity
**Date:** 2026-11-07
**Phase:** fix-cycle
**Fix cycle:** 1
**Fix authorization:** false (report only; no file other than this one was edited)
**Inputs:** `qa/qa-fidelity-consolidated-findings.md` (`|F_0| = 21`), `qa/qa-fidelity-fix-log.md`
**Report under review:** `RESEARCH-REPORT-orchestrator-mode.md`

---

## Per-finding verification (written incrementally)

### F0-01 (IMPORTANT) — OPEN

- **Source re-read:** `src/superclaude/core/WORKER-CONTRACT.md:52-55` (WC-3) and `:30-32` (WC-2 / WC-4). WC-2 (c) at `:30`: a blocked gate writes `worker_status: blocked` **and the exact question in `blocked_question`**; WC-4 `:32` lists `blocked_question` "when blocked". So every blocked contract carries `blocked_question`.
- **What the fix did:** report :58 (new 2.1 row), :113 (2.2 rule 1), :371-374 (diagram rule 1), :1219 (step 1.3 rule 1), :1229 (step 1.8 rule-1 fixtures) all carry the WC-3 condition and say a live row under `ask the coordinator` "falls through to 5 or 7".
- **Why it is still open:** the fall-through cannot reach rule 5 or 7. Step 1.3 (:1219) defines rule 4a detection as "`worker-show --json` key `observation.agentWait` non-null, **or `return-contract.yaml` `worker_status: blocked` with `blocked_question`**", and step 1.8 (:1229) keeps "a `blocked` contract with `blocked_question` (4a)" as a 4a fixture. Since every blocked contract has `blocked_question` (WC-2 `:30`), a live `ask the coordinator` row that skips rule 1 is caught by rule 4a and labelled waiting on a person (a), which is exactly the F0-01 defect. Step 1.8's rule-1 fixture ("not waiting on a person: working or could not determine") and its 4a fixture now assert opposite results for the same input. The diagram (:380) lists rule 4 without the contract path, so diagram and step 1.3 also disagree.
- **Required fix:** apply the same WC-3 condition to rule 4a's contract path (or drop the contract path from 4a, since rule 1 already handles it), in 2.2 rule 4, step 1.3 4a detection and the step 1.8 4a fixture.
- **Minor note (not counted):** the policy line is "read from the Task spec" (:1219), but step 1.2's `OrcaObservation`/`SessionRow` has no field for it and the 3.1 data-source row for `task-list` (:357) lists only kind (b).

### F0-02 (IMPORTANT) — RESOLVED

- **Source re-read:** `WORKER-CONTRACT.md:125-126`.
- **Report:** :64 (2.1 row, caveat and :126 path), :118 (rule 6, "partial: usable not yet judged"), :385 (diagram), :438 (3.1 G5 includes the unusable-partial path), :1219 (step 1.3 rule 6), :1229 (step 1.8 `partial` fixture), :1249 (step 1.17 G5 draft clause includes "a `partial` result it has judged unusable (handled like `failed`)", cited `:125`-`:126`). All locations named in the finding carry the caveat and agree with the source.

### F0-03 (IMPORTANT) — RESOLVED

- **Source re-read (grep):** `reflect/config.py` — `_git` defined `:64`, its only `subprocess.run` `:71`; uses `:104`, `:127`, `:130`, `:137`, `:181`, `:189`, `:194`, `:202`, `:222`, `:312`; `:158-159` is a docstring. `reflect/commands.py:570-577` calls `subprocess.run` (tmux). `reflect/runner.py:31` imports `ClaudeProcess`; launches at `:549`, `:598`.
- **Report:** :196 and :1077 (K-4) now say `config.py` routes its git calls through one `_git` seam and that `commands.py:570-577` and `runner.py` start processes outside it. Grep for `single \`_git\``, `one subprocess seam`, `config.py:158`: 0 hits.
- **Minor notes (not counted):** `runner.py:31` is the import line, not a launch site (`:549`, `:598`); :1060 still calls the design "the single probe module (reflect pattern)", which is loose but no longer the false package-wide claim.

### F0-04 (IMPORTANT) — RESOLVED

- **Source re-read:** `tests/cli/reflect/test_contract_status_cli.py:44-66` patches `ReflectRunner`, `resolve_config`, `ClaudeProcess` with `side_effect=AssertionError`; the only write check is the lock path (`_LOCK_REL` `:41`, `:139-140`).
- **Report:** :1164 (plan summary), :967 (A1 Risk), :1077 (K-4), :1444 (X-3) and :451 (SC-1) all say the pattern covers the subprocess and entry-point half only and that the filesystem half is the step 1.11 snapshot diff with no in-repo precedent; grep `already proven`: 0 hits. Consistent with step 1.11 (:1232).
- **Minor note (not counted):** :966 (A1 Effort) still lists "a read-only proof test (`test_contract_status_cli.py:44-66` pattern)" without the half qualifier; also the precedent patches entry points, not `subprocess.run` itself, so "subprocess half" is an application of its style, as step 1.11 says.

### F0-05 (IMPORTANT) — RESOLVED

- **Source re-read:** `recommend/commands.py:73-74` (`[recommend cache get] ...` on stderr, `sys.exit(1)`); `reflect/commands.py:42` (`_BLOCKED_EXIT = 2`), `:391` (`Error: {exc}`), `:428` (`sys.exit(_BLOCKED_EXIT)`).
- **Report:** step 1.6 (:1222) now reads "(recommend pattern, `recommend/commands.py:73-74`; not reflect, which prints `Error: {exc}` and exits 2 on a config STOP)". Grep `reflect pattern` returns only :1060 (classifier split, unrelated to exit codes).

### F0-06 (IMPORTANT) — RESOLVED

- **Source re-read (`git show 495eb96d:`):** `concepts.md:3-31` (two sets of 10), `:43` ("Provisional design judgment, not user approval or measured comprehension"), `:45-49` (picks Signal Bridge / Proof Gate / Fleet Quilt; Leverage Board / Collision Lens / Revision Drift); `PLAN.md:62`; `README.md:13-15`, `:48`; `enrichment/codebase-context.md:55` (Attention Ledger and Shift Brief "the closest matches to the #339 periodic report").
- **Report:** 2.5 heading and lead (:265, :267) say #409 has no single layout, 20 alternatives, no direction chosen, #409's own picks, and that the pair is this research's selection; 2.6 diagram (:314-315) and row (:326); 3.1 Report bullet (:411); new S9 row 98c (:1642). All agree with the sources.

### F0-07 (IMPORTANT) — RESOLVED

- **Source re-read:** `agent_focus.py:105-114` (Outcome Ledger: `SESSION LIFECYCLE REPORT PACKET ADMISSION` header, rows for sessions with a result, `{min(...)}/{len(entries)} shown`), `:100-102` (Collision Lens worktree cards), `concepts.md:7`, `:9`, `:26`.
- **Report:** "no session or worktree inventory view" is gone (grep: 0 hits). :281 limits the claim to the two selected views and names Outcome Ledger as "its nearest in-package precedent" plus Fleet Quilt, Worktree Atlas and Collision Lens; :326 repeats it. "One row per reported session" matches `entries=[s ... if s['result']]`.

### F0-08 (IMPORTANT) — RESOLVED

- **Source re-read:** `agent_focus.py:17` (`listbox` prints `{shown}/{len(lines)} lines shown`), `:114` (Outcome Ledger `.../N shown`), `:127` (`{min(7,len(stale))}/{len(stale)} mismatches shown`), `:46-50` and `:164-167` (loops without a count or slice).
- **Report, all seven locations plus row 85:** 2.5 omission row (:278), 2.6 row (:326), 3.1 report rule (:431), K-6 (:910), 4.6 C7 (:587), 4.7 S-11 (:614, revised: "not stale"), 5.8 (:825), S9 row 85 (:1621, S-11 revised). Each now says listboxes, wide Outcome Ledger and wide Revision Drift print the count and only the two request loops lack it and are unbounded. Grep for "only in `listbox`" / "wide views omit": 0 hits.
- **Minor note (not counted):** :431 says "A static file must bound them", while S9 row 28 (:1541) keeps "List everything, so shown equals total" as the plan default; both are compatible only if "bound" means printing `<shown>/<total>`. Wording, not a fidelity defect.

### F0-09 (IMPORTANT) — RESOLVED

- **Source re-read:** `agent_focus.py:43` (narrow: "Questions stay until explicit resolution.", "No reply observed is not delivery failure."), `:48` (`q['requester']+" requests / "+q['owner']`), `:51` ("SEEN IS NOT RESOLVED"), `:53` (RETAIN CONTEXT, seven entries including "acting owner" and "requesting orchestrator"); `concepts.md:23` ("seen/delivered is not answered").
- **Report:** 2.5 Attention Ledger row (:273) says "requester and owner (shown separately ...)", keeps the seven retained-context facts with acting owner and requesting orchestrator apart, adds both narrow-view sentences and "seen/delivered is not answered". Grep "requester or owner": 0 hits.

### F0-10 (IMPORTANT) — RESOLVED

- **Source re-read:** `DESIGN-CONTRACT.md:11` (full text); `seed-brief.md:66` ("a recommended next action"), `:67` ("follows the #409 layout").
- **Report:** 2.5 "Required semantics" row (:277) lists all ten semantics with rule 5 quoted verbatim; [CONTRADICTION, sources disagree; owner decision] note (:283); 3.1 "Recommendations only" bullet (:444) names the conflict; S9 row 98b (:1641) records it as an owner decision with a working default. Grep "greyed" and "Navigation only" now hit :277, :283, :444, :1641.
- **Minor note (not counted):** rule (8) at :277 drops "use selected_summary helper if needed"; rule (3) groups five inequalities as one rule, so "ten" is the report's own grouping (the source is unnumbered).

### F0-11 (CRITICAL) — RESOLVED (see new finding N-01 for the test step)

- **Source re-read:** `seed-brief.md:68` ("covered by mock-based tests (liveness verdicts, attention, git cleanliness, unpushed commits, unfinished ledgers)"); `issue-summary.md:10` ("nothing of value is uncommitted or unpushed"); `analyze-worker-contract.md:36` (F5: "All commits pushed" is missing).
- **Report:** 3.1 worktree removable (:406-407) adds an unpushed-commits refusal (ahead of upstream or no upstream, `git status --branch --porcelain`) citing all three sources; 3.1 data-source row (:363); 3.3 constraint (:480); step 1.2 `WorktreeState.unpushed` (:1218); step 1.3 `safe_to_close` (:1219). Step 1.4 (:1220) allows `git -C <worktree> status`, so the read is within the allowlist. The removal-recommendation hole is closed.

### F0-12 (IMPORTANT) — RESOLVED

- **Source re-read:** `issue-summary.md:10` (comment 2: same permission mode, fixed message types, signed narrow grants); `analyze-worker-contract.md:51-55` (S1-S5), `:60-62`; `seed-brief.md:70`, `:80`.
- **Report:** later-phases Phase 4 row (:1303) now defines the trust layer as the sources do and its blockers name `CCSESSION_PERMISSIONS=default` (S1), the Claude Code cross-session channel (S2), Macaroon/Biscuit (S3) and comment 3's bypass-marking and hook questions (S5). OTP restart budgets moved to a separate "Not a source phase: bounded automatic recovery" row (:1306); exclusions (:1471), 8.3 (:1424) and (:1467) agree. Grep "moved to Phase 4": 0 hits.

### F0-13 (IMPORTANT) — RESOLVED

- **Source re-read:** `issue-summary.md:6` (40 h = sweep ~20 + `/sc:close` ~14 + comment-3 research ~6; version 2 = grants + orchestrator of orchestrators); `analyze-worker-contract.md:60-62` (Phase 1 sweep, Phase 2 close, Phase 3 trust + orchestrator of orchestrators); `seed-brief.md:53`, `:70`, `:78`.
- **Report:** [CONTRADICTION, sources disagree on phase grouping] note (:1297) names the disagreement, says the report follows the analysis for Phases 1-2 and why it departs from both; the later-phases table (:1299-1306) has a Blockers column for every phase; Problem Statement (:37) notes the 40 h includes the 14 h `/sc:close` work outside the sweep-only first PR.

### F0-14 (IMPORTANT) — RESOLVED

- **Source re-read:** `analyze-worker-contract.md:34` (F3: stop may be recommended "only on `exited` liveness or a final turn without `worker_done`").
- **Report:** 2.3 (:163) "**This departs from analysis F3**" with the quote and the reason (transcript has no end-of-turn or exit signal; WC-10 accepts only Orca's stall proofs); R2 (:877) and step 1.3 rule 2 (:1219) name the departure and point to 2.3.

### F0-15 (IMPORTANT) — RESOLVED

- **Source re-read:** `seed-brief.md:33` ("`ccsession --list` lists named sessions"), `:75`; `issue-summary.md:22` ("`ccsession --list` as a sweep input"); `analyze-worker-contract.md:60` (sweep reads "`ccsession --list`").
- **Report:** 2.3 (:174) "**This overrides three sources**", GQ-21 row (:555) and exclusions (:1471) each name `seed-brief.md:33`, `:75`, `issue-summary.md:22` and `analyze-worker-contract.md:60` and give the reason (it writes via `ensure_names_migrated`).

### F0-16 (IMPORTANT) — RESOLVED

- **Source re-read:** `BUILD-REQUEST.md:21` (A4 CODE-CONTRADICTED; "do not build task items on it"); `analyze-worker-contract.md:42` (F11: "reuse crash-recovery's signals rather than re-implementing them"); `issue-summary.md:21`.
- **Report:** 2.3 (:167) "**Tension between sources**" paragraph separates the skill as home (rejected) from its signals (reused by step 1.4) and re-implements only the buggy scanner and whole-file parser; K2 row (:538) and exclusions (:1471) agree.
- **Minor note (not counted):** the A4 option table (:1047, :1052) still says only "the report shape and SAFE/REVIEW vocabulary are safe to reuse", without the signals; not contradictory, since it speaks about A4's scripts.

### F0-17 (IMPORTANT) — OPEN

- **Source re-read:** `BUILD-REQUEST.md:12` ("supervise every Orca worker and ccsession"); `seed-brief.md:66`, `:75`; `analyze-worker-contract.md:33` (F2); `research/research-notes.md:310` (AMBIGUITY 8).
- **What the fix did:** :68, :175, :324, :439 (G6 with the AMBIGUITY 8 conflict named), :527, :645, :1071, :1211 (step 1.0b: "GQ-09 ... is not asked"), :1249, :1319, :1389, :1520 (S9 row 7 settled), :1591, :1655 now treat person-started sessions as settled in scope.
- **Why it is still open:** Section 8.2 "Open Questions carried by the plan", row "S9 rows 7, 8, 9, 30, 51, 53" (:1409), still reads "Owner decisions: **report person-started sessions (G6)**, 6 h window ...; step 1.0b asks for **all six** before 1A", and lists "WC-14 G6 wording" under Blocks. This is the exact framing the finding required removed from the open-question locations, and it now contradicts step 1.0b (:1211, five decisions, GQ-09 "not asked") and :1389 ("None left to the owner"). A builder reading 8.2 will ask the owner about G6 or wait on it.
- **Required fix:** in :1409 drop S9 row 7 and "report person-started sessions (G6)" from the owner-decision list, change "all six" to the five decisions step 1.0b asks (GQ-10, GQ-11, GQ-35, GQ-61, GQ-63), and remove "WC-14 G6 wording" from Blocks (or say it is drafted in step 1.17, as :1389 does).

### F0-18 (IMPORTANT) — RESOLVED

- **Source re-read:** `seed-brief.md:42` ("the approved child-worktree trigger rule (CR-01)"); `analyze-worker-contract.md:43` (F12, `CR-01...:12-21`); `.dev/orca-command-refactor/decisions/APPROVED.md:25` (CR-01 under "Also apply in this round"); `changes/CR-01-feature-worktree-hierarchy.md:3` ("Status: PROPOSED"), `:12-21` (T1-T4 triggers).
- **Report:** 4.4 (:560), 8.1 (:1343), 8.2 (:1388), S9 rows 57 (:1571) and 109 (:1658) record GQ-67 as settled by CR-01, give T1-T4 correctly, and name the residual header-status conflict (`:3` PROPOSED vs `APPROVED.md:25`). Grep "CR-01 unread": 0 hits.

### F0-19 (IMPORTANT) — RESOLVED (see new finding N-01 for the test step)

- **Source re-read:** `seed-brief.md:60` ("`.dev/tasks/` content is never classed as disposable"); `analyze-worker-contract.md:35` (F4: refuse while it holds untracked or unstaged content).
- **Report:** 3.3 constraint row "`.dev/tasks/` never disposable" (:481); 3.1 refusal (:408); data-source row (:363); step 1.2 `dev_tasks_unsaved` (:1218); step 1.3 (:1219, `git status --porcelain -- .dev/tasks`). All cite seed-brief :60 and F4.

### F0-20 (IMPORTANT) — RESOLVED

- **Source re-read:** `seed-brief.md:35` (HOW-WE-WORK "Orca coordination" lines 396-405 and its plugin copy change); `issue-summary.md:18`; `src/superclaude/core/HOW-WE-WORK.md:396-405` (`:396` heading, `:403` "Some commands are never workers").
- **Report:** step 1.21 part (b) (:1258) is "Required, not optional", edits `:396-405`, adds a `/sc:sweep` bullet and extends the `:403` bullet, and ties it to the #422 gate; step 1.23 (:1260) byte-copies both parts. Verified: `grep -rln 'Orca coordination' tests/` returns nothing (rc 1) and `tests/core/test_orca_session_launch_guidance.py` exists, as step 1.21 states.

### F0-21 (IMPORTANT) — RESOLVED

- **Source re-read:** `gaps-and-questions.md:84` (GQ-61 open owner decision; "The window should bound activity only, not open Tasks or unread reports (N-41)"); `seed-brief.md:79` (6 h vs 72 h still a question).
- **Report:** 5.5 Camunda relationship (:776) now attributes the point to "QA finding N-41, recorded at GQ-61 (`gaps-and-questions.md:84`)" and says "N-41 is a QA finding, not an owner statement"; the window length stays an open owner decision. Grep "owner note": 0 hits.

---

## Preservation checks

- **NB-4 exception record:** preserved at :13 ("coordinator-approved exception at the Phase 3 research gate") and S9 9.6 row (:1664); 23 NB-4 mentions remain.
- **[CONTRADICTION] markers:** both earlier markers are intact (:1109 HOW-WE-WORK range, P6-06; :1580 GQ-26 allowed-tools); the fix cycle added two more (:283 rule 5, :1297 phase grouping).

---

## New findings introduced or exposed by the fixes

### N-01 (IMPORTANT, blocking) — the two new refusal conditions have no tests

- **Source:** `seed-brief.md:68` requires the classification to be "covered by mock-based tests (liveness verdicts, attention, git cleanliness, unpushed commits, unfinished ledgers)".
- **Report:** the F0-11 and F0-19 fixes add `unpushed` and `dev_tasks_unsaved` to step 1.2 (:1218) and the safe-to-close rule in step 1.3 (:1219). The test step 1.9 (:1230) still lists only "Safe-to-close cases for each of the five `:108` conditions and the `:133-136` freeze", and SC-4 (:454) lists only classifier rules. `grep -nE 'unpushed|dev_tasks_unsaved'` hits only :363, :407, :480, :1218 and :1219; no test step or success criterion mentions them.
- **Why blocking:** the refusal that fixed the CRITICAL F0-11 (and F0-19) is a data-loss guard the seed brief explicitly requires tests for. A builder following step 1.9 would ship it untested.
- **Required fix:** in step 1.9 add safe-to-close cases for (a) a worktree ahead of its upstream, (b) a worktree with no upstream, (c) untracked or unstaged content under `.dev/tasks/`, and (d) `unpushed: None` (status unreadable -> not safe); name them in SC-4 or the step 1.9 success criterion.

### Minor notes (not counted, not rechecked)

- `runner.py:31` cited as behaviour is an import line.
- :1060 still says "single probe module (reflect pattern)"; it is about the classifier split, not exit codes, so it does not reopen F0-05.
- A1 effort (:966) lacks the "half" qualifier used elsewhere.
- F0-01 note: the WC-3 "ask the coordinator" policy line has no field in step 1.2, so rule 1's skip has nothing to read.
- S9 row :1591 and row :1529 disagree on what `scope-02:165` says.
- The minor notes under F0-08, F0-10 and F0-16 above.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| F0-01 | WC-3 `blocked_question` routing | FAIL (OPEN) | step 1.3 :1219 rule 4a and step 1.8 :1229 fixture still class a blocked contract with `blocked_question` as 4a |
| F0-02 to F0-05 | (see entries above) | PASS | re-greps listed in each entry |
| F0-06 to F0-16 | (see entries above) | PASS | `git show 495eb96d:` re-reads and report windows listed in each entry |
| F0-17 | person-started sessions settled | FAIL (OPEN) | 8.2 row :1409 still lists G6 as an owner decision and "all six" |
| F0-18 to F0-21 | (see entries above) | PASS | source and report reads listed in each entry |
| P-1 | NB-4 record preserved | PASS | :13, :1664 |
| P-2 | [CONTRADICTION] markers preserved | PASS | :283, :1109, :1297, :1580 |
| N-01 | new: tests for new refusal conditions | FAIL (new) | step 1.9 :1230, SC-4 :454; grep above |

## PASS set

F0-02, F0-03, F0-04, F0-05, F0-06, F0-07, F0-08, F0-09, F0-10, F0-11, F0-12, F0-13, F0-14, F0-15, F0-16, F0-18, F0-19, F0-20, F0-21 (19 of 21), plus preservation checks P-1 and P-2.

## Summary

- Findings resolved: 19 / 21
- Findings open: 2 (F0-01 IMPORTANT, F0-17 IMPORTANT)
- New blocking findings: 1 (N-01 IMPORTANT)
- Critical open: 0 (F0-11, the only CRITICAL, is resolved; N-01 covers its missing tests)
- Issues fixed in-place: 0 (fix authorization false; the report and sources were not edited)

## Fix-cycle accounting

- `|F_0|` = 21
- `|F_1|` = 3 (F0-01, F0-17, N-01)
- Regression check: no item in a prior PASS set fails now (cycle 0 had no PASS set for these items). No regression halt.
- Monotonicity: 3 < 21, strictly shrinking. No `[HALT-MONOTONICITY]`.
- Cycle cap: this is fix cycle 1 of 2; one more fix cycle is allowed before escalation.

## Confidence gate

- **Confidence:** Verified: 24/24 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (21 findings, 2 preservation checks, 1 new-finding scan)
- **Tool engagement:** Read: 13 | Grep: 11 | Glob: 1 | Bash: 23 (counts across both context windows of this run; Bash includes the `git show 495eb96d:` source reads)
- Unchecked items: none. Unverifiable items: none.

## Verdict: FAIL

