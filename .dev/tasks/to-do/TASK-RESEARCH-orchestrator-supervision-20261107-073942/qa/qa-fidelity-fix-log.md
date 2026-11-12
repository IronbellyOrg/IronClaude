# Fix log: Phase 6 source-document fidelity gate, fix cycle 1

- **Report fixed:** `RESEARCH-REPORT-orchestrator-mode.md`
- **Findings input:** `qa/qa-fidelity-consolidated-findings.md` (`|F_0| = 21`, F0-01 to F0-21)
- **Date:** 2026-11-07
- **Phase:** fix-cycle (fix authorization: true)
- **Scope:** CRITICAL and IMPORTANT findings only; MINOR notes left unchanged. Only the report was edited; no source file was edited. #409 files were read with `git show 495eb96d:<path>` to stdout.
- **Preserved:** NB-4 exception record; both [CONTRADICTION] markers and their resolutions.

## Entries

### F0-01 (IMPORTANT) FIXED
- **Sections:** 2.1 contract table; 2.2 precedence rule 1; 3.1 classification diagram rule 1; 8 step 1.3 rule 1; 8 step 1.8 fixtures.
- **Change:** Added a 2.1 row carrying WC-3 `ask the coordinator` (:52, :54-55: ask, wait, re-invoke in the same session, second contract replaces the blocked one, ask at most once). Rule 1 now applies only when the Orca row is settled or the brief policy is `report blocked`; a live row under `ask the coordinator` falls through to working or could not determine with the note "blocked contract under ask the coordinator; may be re-running" (could not determine when the policy line cannot be read). Diagram and step 1.3 carry the same condition; step 1.8 adds three rule-1 fixtures.
- **Evidence:** `src/superclaude/core/WORKER-CONTRACT.md:52-55` re-read this cycle (Read tool).

### F0-02 (IMPORTANT) FIXED
- **Sections:** 2.1 "Reading a result" row; 2.2 rule 6; 3.1 diagram rule 6; 3.1 WC-14 G5 item; 8 step 1.3 rule 6; 8 step 1.8 fixtures; 8 step 1.17 G5 draft clause.
- **Change:** Restored the :125 caveat (dependents wait until the coordinator has read `report_path` and recorded whether the partial deliverable is usable; unusable is handled like `failed`, then :126). `partial` rows are finished with the note "partial: usable not yet judged". The unusable-partial path is added to the G5 trigger list in 3.1 and in the step 1.17 draft clause (cited `:125`-`:126`); step 1.8 adds a `partial` fixture.
- **Evidence:** `WORKER-CONTRACT.md:125-126` re-read this cycle.

### F0-03 (IMPORTANT) FIXED
- **Sections:** 2.4 CLI structure line and its Evidence line; 6 K-4 row.
- **Change:** Replaced "one subprocess seam" / "single `_git` seam" with "`config.py` routes all of its git calls through one `_git` seam (`config.py:64-78`, used at `:104`, `:127-137`, `:181-222`, `:312`)" and stated that `commands.py:570-577` (tmux `subprocess.run`) and `runner.py:31` (`ClaudeProcess`) start processes outside it. Dropped the docstring citation `config.py:158-159`. Grep confirms no "single `_git`", "one subprocess seam" or `config.py:158` remains.
- **Evidence:** Grep of `src/superclaude/cli/reflect/` for `_git`, `subprocess`, `ClaudeProcess` this cycle (`config.py:64` def and the use lines above; `commands.py:570-577`; `runner.py:31`).

### F0-04 (IMPORTANT) FIXED
- **Sections:** 8 intro (plan summary for A1); 6 A1 Risk row; 6 K-4 row; 7 X-3 row.
- **Change:** Each location now says the `side_effect=AssertionError` pattern covers the subprocess and entry-point half only, and that filesystem read-only is the new step 1.11 snapshot diff with no in-repo precedent. K-4 no longer calls the read-only proof "already proven". Now agrees with step 1.11 and SC-1, which were already correct.
- **Evidence:** `tests/cli/reflect/test_contract_status_cli.py:44-66` re-read this cycle: the three patches target `ReflectRunner`, `resolve_config`, `ClaudeProcess` (entry points); the only write check is `_LOCK_REL` (:41, :121-142).

### F0-05 (IMPORTANT) FIXED
- **Sections:** 8 step 1.6 exit codes.
- **Change:** "(reflect pattern, scope-03)" replaced by "(recommend pattern, `recommend/commands.py:73-74`; not reflect, which prints `Error: {exc}` and exits 2 on a config STOP)". Now agrees with Section 2.
- **Evidence:** `src/superclaude/cli/recommend/commands.py:73-74` re-read (`[recommend cache get] ...` on stderr, `sys.exit(1)`); grep of `reflect/commands.py`: `_BLOCKED_EXIT = 2` (:42), `Error: {exc}` (:391), `sys.exit(_BLOCKED_EXIT)` (:428).

### F0-06 (IMPORTANT) FIXED
- **Sections:** ToC row 2; 2.5 heading and lead; 2.6 diagram and #409 row; 3.1 "Report" bullet; new 9.4 row 98c.
- **Change:** 2.5 now states #409 has no single layout: 20 alternative compositions in two sets, ranking labelled "Provisional design judgment, not user approval or measured comprehension", and "User chooses the visual direction before any production integration", so no direction is chosen; #409's own picks are Signal Bridge / Proof Gate / Fleet Quilt and Leverage Board / Collision Lens / Revision Drift; Attention Ledger + Shift Brief are a research selection (`codebase-context.md:55`). "The #409 layout" is defined as that selection everywhere in the report. Diagram, 2.6 row and 3.1 bullet say the same; 9.4 row 98c records the choice as an owner decision.
- **Evidence:** `git show 495eb96d:` `concepts.md:3-15`, `:19-31`, `:43-49`; `PLAN.md:62`; `README.md:13-15`, `:48`; `.dev/brainstorms/20261107-073115-orchestrator-mode/enrichment/codebase-context.md:55` (read this cycle).

### F0-07 (IMPORTANT) FIXED
- **Sections:** 2.5 paragraph after the table; 2.6 #409 row.
- **Change:** Removed "no session or worktree inventory view". 2.5 now limits "no full inventory" to the two selected views and names the in-package inventory views: Outcome Ledger (per-session rows with `shown/total`, `agent_focus.py:105-114`) as the nearest precedent, Fleet Quilt (`concepts.md:7`), Worktree Atlas (`:9`) and Collision Lens (`:26`; `agent_focus.py:100-102`). The "not inherited from #409" sentence now reads "not inherited from the two selected views, and Outcome Ledger is its nearest in-package precedent".
- **Evidence:** `git show 495eb96d:.../layouts/agent_focus.py` lines 95-127 and `concepts.md:7-9`, `:26` read this cycle.

### F0-08 (IMPORTANT) FIXED
- **Sections:** 2.5 Omission rule row; 2.6 #409 row; 3.1 report rule; 4.6 C7 row; 4.7 S-11 row; 5.8 relationship bullet; 6 K-6 row; 9.3 row 85.
- **Change:** Every "only `listbox()` / wide views omit" claim corrected: `listbox` prints `shown/total` (`:17`) in wide and narrow views, wide Outcome Ledger (`:114`) and wide Revision Drift (`:127`) print it; only the wide Attention Ledger and Shift Brief request loops (`:46-50`, `:164-167`) print none, and they do not truncate. C7 kept as a weaker [CODE-CONTRADICTED] (unbounded, not limited without a count). S-11 and row 85 revised: omission counts are not a stale doc; docs and code agree. S-10 (age ranking) stays [STALE DOC]. Grep for "listbox", "wide views", "S-11", "C7" re-run after the edits; no old wording remains.
- **Evidence:** `git show 495eb96d:.../layouts/agent_focus.py` lines 10-60, 95-130, 158-170 read this cycle; `DESIGN-CONTRACT.md:11` ("Show omission counts when limited").

### F0-09 (IMPORTANT) FIXED
- **Sections:** 2.5 Attention Ledger row.
- **Change:** "requester or owner" changed to "requester and owner (shown separately, `<requester> requests / <owner>`, `:48`)"; added that RETAIN CONTEXT keeps acting owner and requesting orchestrator apart (`:53`), the narrow-view lines "Questions stay until explicit resolution." and "No reply observed is not delivery failure." (`:43`), and the failure mode "seen/delivered is not answered" (`concepts.md:23`).
- **Evidence:** `git show 495eb96d:.../layouts/agent_focus.py:41-53`; `concepts.md:23` read this cycle.

### F0-10 (IMPORTANT) FIXED
- **Sections:** 2.5 Required semantics row and a new [CONTRADICTION] note after the 2.5 table; 2.6 #409 row; 3.1 "Recommendations only" bullet; new 9.4 row 98b.
- **Change:** All ten DESIGN-CONTRACT:11 semantics are now listed (synthetic values; result is not admission; dirty != dangerous, stale != failed, overlap != conflict, partial cost != total spend, tokens != progress; revision equality; rule 5 "Do not show approval/dispatch/retry/merge actions, even greyed. Navigation only."; messages unavailable vs partial; header scope/freshness; narrow-view retention; omission counts; proposed fixture schema). The conflict between rule 5 and the Phase 1 recommendations (safe-to-close REVIEW, "new Task" resume, WC-14 item 8, "what to check next") and seed-brief :66 "recommended next action" is surfaced in 2.5, 3.1 and 9.4 row 98b as an owner decision; the report states it follows the seed brief as the working default.
- **Evidence:** `git show 495eb96d:.../DESIGN-CONTRACT.md:11`; `.dev/brainstorms/20261107-073115-orchestrator-mode/seed-brief.md:66-67` read this cycle.

### F0-11 (CRITICAL) FIXED
- **Sections:** 3.1 "Worktree removable" bullet; 3.1 data-source row for `git -C`; 3.3 "Freeze and cleanup refusal" row; 8 step 1.2 `WorktreeState`; 8 step 1.3 worktree-removable rule.
- **Change:** Added an unpushed-commits refusal (branch ahead of its upstream, or no upstream) read with `git status --branch --porcelain`, stated as going beyond the five conditions at `WORKER-CONTRACT.md:108`, with analysis F5's reason quoted. Step 1.2 gains `unpushed: bool | None`; step 1.3 prints "no" with the condition named. Cited `seed-brief.md:68`, `issue-summary.md:10`, analysis F5 (`analyze-worker-contract.md:36`).
- **Evidence:** `WORKER-CONTRACT.md:103-118` (no push check in the :108 list); `seed-brief.md:68`; `issue-summary.md:10`; `analyze-worker-contract.md:36` read this cycle.

### F0-19 (IMPORTANT) FIXED
- **Sections:** 3.1 "Worktree removable" bullet; 3.3 new row "`.dev/tasks/` never disposable"; 3.1 data-source row; 8 step 1.2 `WorktreeState`; 8 step 1.3 worktree-removable rule.
- **Change:** "`.dev/tasks/` content is never classed as disposable" added as a constraint and as a removable refusal (any untracked or unstaged path under `.dev/tasks/`, from `git status --porcelain -- .dev/tasks`). Step 1.2 gains `dev_tasks_unsaved: bool | None`. Cited `seed-brief.md:60`, analysis F4 (`analyze-worker-contract.md:35`), `WORKER-CONTRACT.md:117`.
- **Evidence:** `seed-brief.md:60`; `analyze-worker-contract.md:35`; `WORKER-CONTRACT.md:117` read this cycle.

### F0-12 (IMPORTANT) FIXED
- **Sections:** 8 "Later phases" table; 8.x external-pattern row ("restart budget deferred"); 10 web-01 row; exclusions line after the evidence table.
- **Change:** "Phase 4: trust layer" now carries the sources' meaning: one permission mode, fixed message types, signed narrow grants, with S1-S5 as blockers (`CCSESSION_PERMISSIONS=default`, Claude Code cross-session channel gap, no Macaroon/Biscuit design, comment-3 research and debate). The OTP-style restart budget moved to its own row "Not a source phase: bounded automatic recovery". Every "moved to / deferred to Phase 4" reference now points to that row.
- **Evidence:** `issue-summary.md:10`; `seed-brief.md:70`, `:80`; `analyze-worker-contract.md:51-55`, `:62` read this cycle.

### F0-13 (IMPORTANT) FIXED
- **Sections:** 1 Problem Statement "Why it matters"; 8 "Later phases" (new [CONTRADICTION] note and a Blockers column).
- **Change:** Named the grouping disagreement (issue summary v1 = sweep + `/sc:close` + research, v2 = grants + orchestrator of orchestrators; analysis Phase 2 = close, Phase 3 = trust + orchestrator of orchestrators). The report follows the analysis for Phases 1-2 (owner's first-PR scope is the sweep alone, `seed-brief.md:53`) and states its numbering beyond that is its own. Section 1 notes the 40 h includes about 14 h for `/sc:close` and about 6 h of research. Every later phase now lists its blockers per `seed-brief.md:70`.
- **Evidence:** `issue-summary.md:6`; `analyze-worker-contract.md:36`, `:39`, `:45`, `:54`, `:60-62`; `seed-brief.md:53`, `:55`, `:70`, `:78` read this cycle.

### F0-14 (IMPORTANT) FIXED
- **Sections:** 2.3 paragraph after the crash-recovery table; 3.1 classification diagram rule 2; 6 R2 row; 8 step 1.3 rule 2.
- **Change:** Each narrowing now names analysis F3 (`analyze-worker-contract.md:34`) as the source it departs from. 2.3 states the reason: the report keeps F3's `exited` half; a "final turn" counts only when Orca observed the exit, because the transcript has no end-of-turn or process-exit signal (`parse_session_log.py:45-55`, `:85-102`) and WC-10 (`WORKER-CONTRACT.md:45`), which F3 itself cites, accepts only Orca's stall proofs.
- **Evidence:** `analyze-worker-contract.md:34` read this cycle; parse_session_log line citations are the report's existing [CODE-VERIFIED] citations at 2.3.

### F0-15 (IMPORTANT) FIXED
- **Sections:** 2.3 ccsession `--list` bullet; 4.4 GQ-21 row; exclusions line after the evidence table.
- **Change:** Named the override of `seed-brief.md:33`, `:75`, `issue-summary.md:22` and `analyze-worker-contract.md:60`, which make `ccsession --list` an input. The exclusion wins because `--list` writes (`ensure_names_migrated`, scope-02 `:165`) and Phase 1 is read-only (`seed-brief.md:53`); labelled sessions still come from the `topics/*.txt` store.
- **Evidence:** `research/scope-02-orca-recovery.md:165`; `seed-brief.md:33`, `:53`, `:75`; `issue-summary.md:22`; `analyze-worker-contract.md:60`; grep of `ccsession` for `topics` read this cycle.

### F0-16 (IMPORTANT) FIXED
- **Sections:** 2.3 new paragraph after "Rejected option A4"; 4.3 K2 row; exclusions line.
- **Change:** Named the tension between `BUILD-REQUEST.md:21` (A4 rejected) and analysis F11 / `issue-summary.md:21` (reuse the signals). Resolution: rejecting A4 rejects the skill as the sweep's home, not its signals; step 1.4 reuses the same on-disk signals (`refs/pipelines.md:19`, `:52-68`, `:102-116`, `:177-201`) and re-implements only the code, which cannot be reused as it stands (`bootstrap_scan.sh:31`, `:73`, `:136`; `parse_session_log.py:31-40`, `:45-55`; `SKILL.md:4` not read-only).
- **Evidence:** `BUILD-REQUEST.md:21`; `analyze-worker-contract.md:42`; `issue-summary.md:21`; report step 1.4 disk readers re-read this cycle.

### F0-17 (IMPORTANT) FIXED
- **Sections:** 2.x person-started note (~:68); 2.3; 2.6 ccsession row; 3.1 G6 item; 4.2 G6 row; 4.3 K1 row; 4.9 G6 and S9 lists; 6 recommendation ("five open owner decisions"); 8 steps 1.0b, 1.3 and 1.17 (G6 draft clause); 8.1; 8.x later-phase text; 9 rows 7, 66 and 106.
- **Change:** Person-started sessions are now recorded as in scope for the Phase 1 report, settled by the sources: they appear in the report, observed from transcripts and ccsession files, and are never messaged. The "whether to report them at all" framing was removed from GQ-09 and every open-question location; GQ-09 is no longer an asked owner decision in step 1.0b nor a blocker. Each location names the conflict with research-notes AMBIGUITY 8 (`research-notes.md:310`, "or limit Phase 1 to Orca workers") and states the report follows BUILD-REQUEST, the seed brief and analysis F2.
- **Evidence:** `BUILD-REQUEST.md:12`; `seed-brief.md:66`, `:75`; `analyze-worker-contract.md:33`; `research/research-notes.md:310`, all read this cycle.

### F0-18 (IMPORTANT) FIXED
- **Sections:** 4.x GQ-62/66/67/100 row (~:560); 8 gap-to-step table GQ-66/67/100 row (~:1343); 8 "Gaps sent to Open Questions" row (~:1388); 9 rows 57 and 109.
- **Change:** Removed the "CR-01 unread" / "Read CR-01; owner decision" framing. GQ-67 is recorded as settled: CR-01 is the approved child-worktree trigger rule (child worktree only on T1-T4, otherwise the shared feature worktree), and the issue's "new worktree is always first choice" is not adopted. GQ-67 no longer goes to Open Questions. Named the source-to-source conflict: the CR-01 file header says "Status: PROPOSED" (`CR-01-feature-worktree-hierarchy.md:3`), while `decisions/APPROVED.md:25` and `seed-brief.md:42` record it as approved; the report follows `APPROVED.md:25`.
- **Evidence:** `seed-brief.md:42`; `analyze-worker-contract.md:43`; `CR-01-feature-worktree-hierarchy.md:3`, `:12-21`; `decisions/APPROVED.md:25`, all read this cycle. Post-edit grep for `CR-01 unread`, `worktree-first`, `AMB 11`: no remaining open framing.

### F0-20 (IMPORTANT) FIXED
- **Sections:** 8, phase 1E, steps 1.21 and 1.23.
- **Change:** Step 1.21 now has a required part (b) that edits the HOW-WE-WORK "Orca coordination" section (`:396-405`). It adds a bullet that the coordinator runs `/sc:sweep` itself as a read-only report (WC-14, step 1.17) and names `/sc:sweep` in the "Some commands are never workers" bullet (`:403`), matching step 1.18. This replaces the former "Optional" bullet. Part (b) follows the #422 gate of steps 1.17-1.18 (step 1.16a). Step 1.23 now states that the byte copy to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` carries this edit, and that it is copied again if part (b) moves to a follow-up PR. The step also says no test pins the section today, and it now cites the existing pin pattern correctly as `test_orca_session_launch_guidance.py:14-31`; that test pins `core/CLAUDE.md` and the ccsession README, not HOW-WE-WORK.
- **Evidence:** `seed-brief.md:35`; `issue-summary.md:18`; `src/superclaude/core/HOW-WE-WORK.md:396-405` read this cycle; `tests/core/test_orca_session_launch_guidance.py:10-31` read; grep of `tests/` for "Orca coordination": no match.

### F0-21 (IMPORTANT) FIXED
- **Sections:** 5.x external findings, Camunda finding, Relationship line (~:776).
- **Change:** Replaced "the owner note at GQ-61 that the 6 h window bounds activity only" with QA finding N-41, recorded at GQ-61 (`gaps-and-questions.md:84`): the window should bound activity only, not open Tasks or unread reports. The line now says N-41 is a QA finding, not an owner statement, and that the window length (6 h versus 72 h) is still an open owner decision (`seed-brief.md:79`; GQ-61, S9 row 51). This is consistent with the report's existing GQ-61 rows (~:1335, :1381, :1449, :1565).
- **Evidence:** `gaps-and-questions.md:84`; `seed-brief.md:79`, both read this cycle. Post-edit grep for "owner note": no match.

## Summary
- Blocking findings: 21 (CRITICAL 1, IMPORTANT 20).
- Fixed: 21 (F0-01 to F0-21). Not fixed: 0.
- MINOR findings were not fixed, as instructed.
- Kept: the NB-4 exception record and both [CONTRADICTION] markers with their resolutions. Two new source-conflict markers were added: phase grouping (F0-12/F0-13) and CR-01 status (F0-18).
- No source file was edited.

