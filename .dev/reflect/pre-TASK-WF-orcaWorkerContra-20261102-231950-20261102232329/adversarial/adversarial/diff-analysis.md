# Diff Analysis: Reviewer Card Comparison

## Metadata
- Generated: 2026-11-02T23:58:57Z
- Variants compared: 3
  - Variant A = `variant-1-original.md` (reviewer 1, analyzer, sonnet; findings F1-F8)
  - Variant B = `variant-2-original.md` (reviewer 2, qa, haiku; findings R2-1 to R2-6)
  - Variant C = `variant-3-original.md` (reviewer 3, refactorer, opus; findings R3-F1 to R3-F14)
- Total differences found: 37 (34 in S/C/X/U, plus 3 promoted shared assumptions)
- Categories: structural (8), content (9), contradictions (6), unique (11), shared assumptions (8 surfaced; 3 promoted)
- Focus areas: correctness, coverage, deviation-classification
- Cite keys: `A:N`, `B:N`, `C:N` = card line; `TL:N` = plan `TASK-WF-orcaWorkerContra-20261102-231950.md` line; `SRC:N` = `source.md` line. Other repo files are cited by path:line. Every TL/SRC/file cite below was opened for this analysis.
- Matching rule: findings are the topics. Two findings match when they name the same plan task and the same defect, regardless of wording.

## Structural Differences

| # | Area | Variant A | Variant B | Variant C | Severity |
|---|------|-----------|-----------|-----------|----------|
| S-001 | Finding count and severity mix | 8 findings: 1 blocking (F1), 7 minor (A:6-174) | 6 findings: 1 blocking (R2-1), 5 minor (B:6-154) | 14 findings: 2 blocking (R3-F1, R3-F2), 12 minor (C:6-243) | Medium |
| S-002 | Bundling granularity | Bundles several defects per finding: F4 has parts (a) cadence and (b) AC-0.6 fallback (A:79-86); F7 bundles AC-C1/C2 re-run, AC-C4, AC-C5 and the phase report (A:137-143); F8 bundles three issues (A:157-164) | Splits the F4 pair into R2-1 and R2-2, and splits phase-end checks into R2-3 (AC-C5) and R2-4 (ordering) (B:7-110) | Finest split: cadence R3-F2 vs fallback R3-F14; dependency gap split across R3-F4 and R3-F5 (C:27-99, C:231-243) | Medium |
| S-003 | Deviation-class vocabulary in use | Four classes: regression (F1), drift (F2, F4, F5, F7), necessary (F3), none (F6, F8) (A:9-157) | Two classes: drift (R2-1 to R2-5), none (R2-6) (B:9-142) | Two classes: drift (13 findings), regression (R3-F6) (C:9-235) | Medium |
| S-004 | Extra blocks beyond findings | `agreements_with_t1_card`, `disagreements_with_t1_card`, `self_audit` (A:175-205) | Same three plus a unique `matrix_omissions` block of 6 coverage-matrix gaps (B:155-185) | Same three blocks (C:244-280) | Medium |
| S-005 | Evidence format | Relative paths, line ranges allowed (`:56-60`, `:106-108`) (A:22-28) | Absolute quoted paths, single lines (B:25-30) | Relative paths, single lines; cites more non-plan repo files (Makefile, tests/commands, tests/recommend) (C:91-112, C:147-148) | Low |
| S-006 | Calibration result | Confidence 0.83; every severity holds; F8 part (a) marked weak; lowest sub-score is deviation_classification_clarity 0.65 (A:207-210) | Confidence 0.87; R2-1 holds only "borderline"; one cite note (R2-3 cites TL:17, text is at TL:20) (B:238-243) | Confidence 0.87; R3-F2 downgraded blocking to minor; R3-F1 "AC cannot pass" called overstated; R3-F6 count called overstated (C:281-285) | High |
| S-007 | Verdict, self-confidence, persona | FAIL, 0.80, analyzer/sonnet (A:1-5) | FAIL, 0.78, qa/haiku (B:1-5) | FAIL, 0.72, refactorer/opus (C:1-5) | Low |
| S-008 | Stated limits in self-audit | Did not verify Orca install layout or how `/sc:implement` runs task bodies (A:202-205) | Assumed `/sc:implement` honours only stated Depends-on edges, and says a sequential executor would mask R2-4 (B:232-234) | Did not use codegraph; partial reads of two test files (C:270-273) | Medium |

Notes:
- S-006 is High because the calibrator's downgrade of R3-F2 changes C's blocking count from 2 to 1, and B's only blocking finding holds only as "borderline". After calibration, the cards' FAIL verdicts rest on F1 (A), R2-1 (B) and R3-F1 (C), which are three different defects.
- S-003 matters for the deviation-classification focus: A is the only card that uses `necessary`, and the cards give the same defects different classes (see X-006).

## Content Differences

| # | Topic | Variant A Approach | Variant B Approach | Variant C Approach | Severity |
|---|-------|-------------------|-------------------|-------------------|----------|
| C-001 | Task 3 (KNOWN_CORE_FILES) is not a dependency of Task 4 or Task 7 | F1, **blocking / regression**: Task 4's AC runs `tests/cli/test_how_we_work_install.py`, whose set-equality test fails once Task 1 adds the file and before Task 3 runs. Task 7 may commit without install_core.py. Fix: add Task 3 to the Depends-on lines of Tasks 4 and 7 (A:7-32) | R2-4, **minor / drift**: Task 7 can commit before Task 3, and Task 6 can run before Task 4. Folded into a wider "common checks mid-plan" finding (B:83-110) | R3-F4 (dependency part), **minor / drift**: add Task 3 to Task 7's deps (C:69-81). R3-F5, **minor / drift**: Task 1 leaves `test_known_core_set_matches_shipped` red until Task 3. Fix: move the registration into Task 1 (C:85-99) | High |
| C-002 | Task 8 does not require a smoke run longer than the heartbeat cadence (SRC:291) | F4 part (a), **minor / drift**, bundled with the fallback issue (A:79-83) | R2-1, **blocking / drift**: requirement is unconditional, all three runs may be short, and the Goal (TL:15) claims every P0 check passes (B:7-37) | R3-F2, **blocking / drift** (C:27-43); calibrator downgrades it to minor because TL:122 brings in 7.2 step 5 by reference (C:285) | High |
| C-003 | Task 8 does not carry the AC-0.6 `--source terminal` fallback into step 5 | F4 part (b), minor / drift (A:83-86) | R2-2, minor / drift; minor because TL:122 delegates to the spec text that holds the fallback (B:38-62) | R3-F14, minor / drift (C:231-243) | Low |
| C-004 | Phase-end state: AC-C5 never recorded, AC-C1/C2 not re-run, no single P0 phase report | F7, minor / drift: one final task re-runs AC-C1, AC-C2, AC-C4, records AC-C5 as vacuous, writes a P0 phase report (A:134-153) | R2-3 (AC-C5 unrecorded) and R2-4 (re-run AC-C1, AC-C2 and the AC-C3 after-comparison), both minor / drift; no explicit phase-report task (B:63-110) | R3-F11, minor / drift: final task writing `artifacts/p0-phase-report.md` with PASS/FAIL per check (C:185-203) | Low |
| C-005 | Negative checks in Tasks 5 and 6 have no safe target | F5, minor / drift: make path and scan roots monkeypatchable to a tmp_path copy (A:96-113) | Omitted | R3-F8, minor / drift: same fix, plus the risk that a leftover scratch skill breaks `make verify-sync` (Makefile:171,174 cited) (C:133-152) | Low |
| C-006 | AC-0.9 classification "refused under --unattended by the converting phase" is empty at P0 | F6, minor / **none**: add a "deferred to P<n>" class and restrict the WC-9 no-git-state claim to classified hits (A:114-133) | Omitted (B only checks the verb list matches AC-0.9, B:224-225) | R3-F13, minor / **drift**: every hit must be WC-9-allowed or allowlisted with its converting phase; also define `gh api` post patterns (C:216-230) | Medium |
| C-007 | Task 5 test may assert rule labels, not rule substance | Omitted | R2-5, minor / drift: list load-bearing phrases for WC-3, WC-5, WC-7, WC-9 (B:111-138) | R3-F9, minor / drift: one distinctive phrase per rule, including "the four `guard refused:` texts" (C:153-167) | Low |
| C-008 | Stale cite "lines 13-25" for KNOWN_CORE_FILES (TL:60); real span is install_core.py:13-27 | Inside F1's recommendation, no finding of its own (A:32) | R2-6, minor / none (B:139-154) | R3-F12, minor / drift (C:204-215) | Low |
| C-009 | Task 7 commit mechanics | F3, minor / **necessary**: the commit inside an implement task window makes any QA retry halt `head-moved`; "commit last" reduces but does not remove exposure (A:54-74) | Omitted (only the Task 3 dependency, see C-001) | R3-F1, **blocking / drift**: body order and "commit last" conflict with the AC (C:7-26). R3-F4, minor / drift: paths not listed; `--only` drops a staged `.dev/tasks` unless named (C:63-81) | Medium |

Verification of the shared facts behind these rows:
- C-001: `tests/cli/test_how_we_work_install.py:43-44` asserts `KNOWN_CORE_FILES == frozenset(install_core.list_core_files())`. TL:58 makes Task 3 depend on Task 1 only, TL:72 makes Task 4 depend on Task 2 only, TL:77 runs that test in Task 4's AC, and TL:108 makes Task 7 depend on Tasks 4 and 6 only. The defect exists in the plan's dependency text. Whether it fires depends on the executor (see X-001, A-002).
- C-002/C-003: SRC:291 contains both the cadence sentence and the `--source terminal` fallback in one step. TL:122 runs "steps 1-3 and 5-7" by reference. TL:124-127 records "each 7.2 step's result" and the AC-0.6 yes/no, but names neither clause.
- C-004: a grep of the plan for `AC-C5` returns no hit. AC-C1 and AC-C2 appear only at TL:79 (Task 4). SRC:241: "A phase passes only when every check in its block and every common check passes."
- C-008: install_core.py:13 opens `frozenset(` and :27 closes it. Note that the spec's own cite is also stale (`install_core.py:13-24`, SRC:59).
- C-009: TL:110 orders commit first, then the install, then says "Make the commit the last action of the task." TL:113 requires `t7-approvals.md` to hold the commit ID and the install output.

## Contradictions

| # | Point of Conflict | Variant A Position | Variant B Position | Variant C Position | Impact |
|---|-------------------|-------------------|-------------------|-------------------|--------|
| X-001 | Severity of the Task 3 dependency gap (C-001) | Blocking: "Task 4's acceptance criterion cannot pass at the point Task 4 runs" (A:11) | Minor; B adds that "a strictly sequential executor would mask them" (B:232-234) | Minor (R3-F4, R3-F5) (C:63-99) | High |
| X-002 | Severity of the missing longer-than-cadence run (C-002) | Minor (F4) (A:76) | Blocking (R2-1) (B:8); calibrator "yes (borderline)" (B:242) | Blocking (R3-F2) (C:28); its own calibrator says "no (downgrade to minor)" (C:285) | High |
| X-003 | B's own reasoning on delegation to the spec (intra-variant) | n/a | R2-2 is minor **because** TL:122 delegates to spec 7.2, which holds the fallback (B:46-49, B:199-203). R2-1 is blocking even though the cadence sentence sits in the same delegated step (B:10-23, B:234-236) | n/a (C's calibrator uses B's R2-2 argument to downgrade R3-F2, C:285) | Medium |
| X-004 | How many exact `guard refused:` reason texts exist | The spec gives three exact texts. Case 3 has only the prefix, so "four exact texts" forces the executor to invent one (F2, A:37-43) | Not addressed | R3-F9 tells the test to pin "the four `guard refused:` texts" (C:166) | Medium |
| X-005 | Whether Task 7's "Make the commit the last action" is coherent | Treats it as a real but partial mitigation of the retry-ladder risk (A:60-61) | Not addressed | Treats it as contradicting the body's own order and the AC, so blocking (C:11-17) | Medium |
| X-006 | Deviation class given to the same defects | Task 3 gap = regression (A:9); AC-0.9 label gap = none (A:116); Task 7 commit = necessary (A:57) | Task 3 gap = drift (B:82); stale cite = none (B:141) | Task 3 gap = drift (C:65); AC-0.9 label gap = drift (C:218); stale cite = drift (C:206); Task 7 commit = drift (C:9) | Medium |

Resolution evidence (which side the text supports):

- **X-001: the text supports B and C (minor).** The defect exists in the dependency lines (TL:58, TL:72, TL:77, TL:108; `tests/cli/test_how_we_work_install.py:44`). But the plan's executor is `/sc:implement` (TL:19 and SRC:238 route each phase through `/sc:workflow` then `/sc:implement`). That executor ignores dependency fields: "Ignore MDTM fields (`depends-on`, ...) except `independent`" (`src/superclaude/skills/sc-implement-protocol/SKILL.md:79`) and "Default sequential in source order ... Unmarked = sequential" (SKILL.md:97). The plan marks nothing `independent`, so Task 3 runs before Task 4 and Task 7, and Task 4's AC passes. What remains is C's R3-F5 point: `tests/cli` is red between Task 1 and Task 3, and no AC runs it in that window (TL:40-43, TL:51-54). A's "regression" class and "blocking" severity rest on a dependency-driven executor that the plan's own route does not use. A itself names that uncertainty ("the order depends on task numbering, which the plan does not state", A:16-17).
- **X-002: the text supports "required but not enforced by the AC", which leans to should-fix, not blocking.** SRC:291 puts the duty on "each phase report", and TL:122 brings in step 5 by reference. So the requirement is in scope, as C's calibrator says. But the executor's QA compares the diff with "that task's AC", the plan's Constraints section and "explicit instructions on the task" (`src/superclaude/skills/sc-implement-protocol/refs/qa.md:13-17`). TL:124-128 does not name the clause, so QA may not check it, as B and C say. B's claim that it is "unsatisfiable after the fact" (B:22-23) overstates the problem: SRC:291 asks for one checked run longer than the cadence, and a further run can be added. Also, B's suggestion of a long troubleshoot Tier-2 run (B:34) may not count: SRC:291 excludes time "inside an Agent-tool call" from the heartbeat rule, and SRC:78 names troubleshoot Tier 2 as exactly that kind of Agent-tool fan-out.
- **X-003: B is inconsistent with itself.** Both clauses sit in SRC:291, and both are delegated by the same TL:122 sentence. B's stated difference is that the fallback is conditional and the cadence duty is not (B:20-21). That difference explains why one is more likely to be missed. It does not explain why delegation counts for one and not the other.
- **X-004: the text supports A for P0, with a spec caveat.** SRC:60 quotes three texts: `brief lacks --unattended`, `loaded command has no Unattended mode section (...)` and `command copies disagree (stale copy): <paths>`. Case 3 is defined only by its condition and the `guard refused:` body prefix. The plan says "the four `guard refused:` reason texts" (TL:41; also TL:36, TL:87). The spec is loose too: the P1 row AC-1.1 says "its four refusal conditions and reason texts" (SRC:306), and AC-1.7 checks case 3 only by the prefix (SRC:312). C's recommendation would pin a string the spec does not define.
- **X-005: the text supports C that the wording is inconsistent. It does not support "cannot pass".** TL:110 describes commit, then install, then "Make the commit the last action of the task." A reads the last sentence as an instruction it can follow. C reads it as clashing with the stated order. Both readings are possible, which is C's point. C's own calibrator notes the AC at TL:113 can still be met by writing `t7-approvals.md` after the commit (C:285), and A's F3 risk applies whichever order is chosen.
- **X-006: the text supports drift for the Task 3 gap.** A's "regression" needs an existing behaviour to break at a checked point. Under source-order execution (SKILL.md:97), the only red window is between Task 1 and Task 3, and no AC observes it. For the AC-0.9 label gap, TL:97 adds a classification the spec allows ("refused under `--unattended`", SRC:305) but which is empty at P0. That fits drift (C) better than none (A). For the stale cite, none (B) fits better than drift (C), because SRC:59 itself cites a stale range and the edit is made by symbol name (TL:60). For the Task 7 commit, A's "necessary" fits the commit itself, which SRC:282 requires before Orca can build a worktree. C's "drift" fits the wording conflict in TL:110. These are different aspects, not a true disagreement.

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | A | F2: the spec defines only three exact refusal texts. The plan's "four exact texts" (TL:41) makes the executor invent a case-3 string, which breaks TL:21 ("adds no rule the spec lacks"). Confirmed at SRC:60; see X-004 (A:36-53) | Medium |
| U-002 | A | F3: a commit inside a `/sc:implement` task window makes any later QA retry or revert of Task 7 refuse with `head-moved`. Confirmed: retry.md:41 ("HEAD has not moved ... A missing file ... counts as moved") and retry.md:333-334 (`_sc_retry_refuse head-moved`). Task 7 is not a batch task (SKILL.md:97), so the retry ladder would apply. No other card looks at the executor's mechanics (A:54-74) | High |
| U-003 | A | F8: (a) run AC-C6 before the live runs; (b) `git ls-remote origin` in Task 7's AC (TL:116) has no before-state; (c) no step confirms the coordinator is a person-opened session. Part (a) is weak: "at any depth setting" is WC-13 text (SRC:81), not Task 8 text (TL:122), and D5 orders the trace before a depth raise, not before live runs (SRC:394). Parts (b) and (c) hold (A:154-174, A:210) | Medium |
| U-004 | B | `matrix_omissions`: six spec spans with no coverage-matrix row, including SRC:241 (the phase-pass rule) and L3's staging rule (SRC:396). This is about the reflect coverage matrix, not the plan (B:155-185) | Low |
| U-005 | B | Part of R2-4: Task 6 does not depend on Task 4, so the AC-C3 after-comparison could run before the HOW-WE-WORK.md edit (B:88-92). This rests on the dependency-driven executor assumption, which SKILL.md:79,97 contradict (A-002) | Low |
| U-006 | C | R3-F1: Task 7's step order (commit, then install) conflicts with "Make the commit the last action" (TL:110), on the task that runs an owner-approved `--force` install. Calibrator: blocking holds but "cannot pass" is overstated (C:7-26, C:285) | Medium |
| U-007 | C | R3-F3: Task 1's AC "no `orca orchestration` verb syntax" covers the whole file (TL:42). Task 2 must then add section 2.3 and WC-6 content (TL:49), and that content contains Orca verb syntax (SRC:84 `worker-start --worktree new-child --base-branch`; SRC:88 `orca worktree rm`). The spec's no-copy rule covers only the worker-session duties (SRC:59). A final review that re-checks Task 1's AC would fail it (C:44-62) | Medium |
| U-008 | C | Part of R3-F4: TL:110 never lists "the explicit P0 paths", and `git commit --only -- <paths>` leaves out a staged `.dev/tasks` unless it is named in the pathspec. C supplies the concrete path list (C:66-81) | Medium |
| U-009 | C | R3-F6: Task 4 changes HOW-WE-WORK.md but its AC runs only three test files (TL:77). A grep of `tests/` finds 9 files that mention HOW-WE-WORK, including `tests/commands/test_routing_plugin_parity.py`, `tests/commands/test_help_command.py`, `tests/recommend/test_routing_refresh.py` and `tests/unit/test_cli_install.py`. AC-C3 covers only `tests/skills/` (SRC:263). The calibrator says the count and one cite are overstated (C:100-116, C:285) | Medium |
| U-010 | C | R3-F7: the HOW-WE-WORK.md line "after P0, none" (TL:74) goes stale every phase. Each fix then edits a guide line and its plugin copy, which works against the additive SA-5 approach (SRC:212) (C:117-132) | Low |
| U-011 | C | R3-F10: Task 2's brief template copies the section 3.1 "Brief must pass" flags as written (TL:49). Those include `--report-dir <dir>` for cleanup-audit (SRC:143) and workflow (SRC:152), but no command accepts that flag until P1 (SRC:221). An installed template used between P0 and P1 would pass an unknown flag (C:168-184) | Medium |

## Shared Assumptions

Surfaced assumptions (all classifications):

| # | Agreement Source | Assumption | Classification | Promoted |
|---|------------------|-----------|----------------|----------|
| A-001 | All cards defer P1-P4 without objection | P0-only scope is an authorized limit, not drift (TL:19; SRC:216, SRC:238) | STATED (A:191-192, B:187-190) | No |
| A-002 | C-001, R2-4, R3-F4, F1 all reason about Depends-on edges | The executor runs tasks by their Depends-on edges and may run them out of source order | CONTRADICTED: B states it (B:232-234), A and C rely on it (A:16-17, C:69-70). `/sc:implement` ignores `depends-on` (SKILL.md:79) and runs "sequential in source order" (SKILL.md:97). Flagged for debate: it decides X-001 and U-005 | No (flagged) |
| A-003 | All three verdicts are FAIL, each driven by a "blocking" finding | "Blocking" means a spec requirement the plan's AC does not enforce, or an AC that cannot pass, and one such finding fails the plan. No card cites a rule in the plan or the review brief that defines blocking | UNSTATED | Yes |
| A-004 | C-002, C-003 | Spec text that a task brings in only by reference is not reliably done unless restated in the AC | STATED (B:49-52); partly backed by qa.md:13-17 (QA compares against task AC, plan Constraints and task instructions) | No |
| A-005 | No card questions whether Tasks 7-8 can run inside the executor | The `/sc:implement` run is attended: the owner is present to answer Task 7's two approvals (TL:25, TL:110), and the executing session can be the person-opened coordinator for Task 8 (TL:26, TL:122) | UNSTATED for the approval pause. A states the coordinator part as unverified (A:163-164, A:203-205) | Yes |
| A-006 | No card disputes Task 8-9 feasibility | Orca is installed and reachable (`orca-ide`, `/opt/Orca/...`, profiles path) when the plan runs | STATED as unverified (A:202-203) | No |
| A-007 | All cards treat spec deviations as plan defects | `source.md` is a consistent and complete authority for P0 | CONTRADICTED: SRC:60 gives three exact refusal texts while SRC:306 speaks of "four refusal conditions and reason texts", and SRC:59 cites a stale line range (`install_core.py:13-24`, versus :13-27 on disk). A (F2) and C (R3-F9, "the spec's own pass condition ... is weak too", C:160) partly notice this | No (flagged) |
| A-008 | The phase-end recommendations (F7, R2-3/R2-4, R3-F11) ask for a final record but no staging | Artifacts written after Task 7's commit (Task 8 and Task 9 outputs, the proposed phase report, and `t7-approvals.md` if written after the commit) need no further staging step | UNSTATED. TL:22 says `.dev/tasks/` is always staged, and L3 has the coordinator stage `.dev/tasks` "at every commit and at the end of the run" (SRC:396). No task after Task 7 stages anything (TL:118-136), and no card notices this | Yes |

Promoted [SHARED-ASSUMPTION] diff points:

| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|-----------|------------------|--------|--------|
| A-003 | [SHARED-ASSUMPTION] One "blocking" finding means FAIL, with "blocking" undefined. The three cards then disagree about which findings are blocking (X-001, X-002), and two of the three blocking calls are weakened by calibration or by the executor's rules (C:285; SKILL.md:97) | Unanimous FAIL verdicts (A:4, B:4, C:4) | High | Open: debate should fix a blocking test (for example: the plan as written cannot reach a passing P0 under its own executor) before scoring severities |
| A-005 | [SHARED-ASSUMPTION] Plan execution is attended, so mid-task owner approvals and the person-opened coordinator role work inside `/sc:implement` | Every card reviews Tasks 7-8 only for content, not for whether the executor can pause | Medium | Open: A's F8(c) is the nearest finding; no card checks the approval pause |
| A-008 | [SHARED-ASSUMPTION] Post-commit artifacts need no staging | All phase-end recommendations stop at "write the report" | Medium | Open: a gap all three cards missed; it is relevant to the TL:22 always-staged constraint |

## Summary
- Total structural differences: 8
- Total content differences: 9
- Total contradictions: 6
- Total unique contributions: 11
- Total shared assumptions surfaced: 8 (UNSTATED: 3, STATED: 3, CONTRADICTED: 2)
- Highest-severity items: S-006, C-001, C-002, X-001, X-002, U-002, A-003

Key points for the debate:
1. All three cards are FAIL, but each rests on a different blocking defect: A on the Task 3 dependency (F1), B on the cadence run (R2-1), and C on the Task 7 order (R3-F1) plus the cadence run (R3-F2, downgraded by its calibrator).
2. The executor's own rules (`sc-implement-protocol/SKILL.md:79,97`) run tasks in source order and ignore Depends-on. That removes the trigger for A's F1 and B's U-005 and weakens the dependency parts of R2-4 and R3-F4. R3-F5's red window between Task 1 and Task 3 still exists.
3. Every card finds the cadence-run gap (C-002). The disagreement is only about severity, and B's own reasoning is inconsistent (X-003).
4. A's U-002 (retry ladder `head-moved` after Task 7's commit) is a verified risk that only one card raises.
