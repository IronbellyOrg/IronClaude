# Refactoring Plan: Merge into Base (Variant C)

## Overview
- Base: Variant C (default model:refactorer), `variant-3-original.md` (base-selection.md, "Selected Base")
- Incorporating strengths from: Variant A (`variant-1-original.md`), Variant B (`variant-2-original.md`), and the Round 2.5 invariant probe (`invariant-probe.md`, not adjudicated by the advocates)
- Output: ONE merged verdict card at `R/adversarial/merged-verdict.yaml`, where R = `.dev/reflect/pre-TASK-WF-orcaWorkerContra-20261102-231950-20261102232329`
- Planned changes: 15
- Merged findings: 15 adjudicated (1 blocking, 3 should-fix, 11 minor) plus 1 unadjudicated blocking candidate (INV-002)
- Merged verdict: FAIL. Rule shared by all three advocates: one blocking finding means FAIL (R2-A:91, R2-B:89, R2-C:85).
- Convergence: 0.9615, status BLOCKED_BY_INVARIANTS (debate-transcript.md, "Convergence Assessment")
- Risk level: Medium (overall). Changes 1 and 14 carry text the advocates did not adjudicate.
- Cite keys as in `debate-transcript.md`. Calibrated confidences come from each card's calibration block: A 0.83 (A:209), B 0.87 (B:241), C 0.87 (C:284). Every cite below was opened by the orchestrator.

Severity scale. The cards use only blocking and minor. The merged card uses blocking, should-fix and minor. The debate's blocking test (R2-A:91, with B's clause, R2-B:89) decides blocking. "Should-fix" is the debate's "top should-fix" tier (R2-B:72-76, R2-C:68-71), meaning fix before the first task starts because the plan is hash-pinned once the first task starts (`E-PLAN-CHANGED`, SKILL.md:40). Every other surviving finding is minor. Note that the A-003 answers use "should-fix" loosely for every non-blocking item (R2-A:91 lists F1/R3-F5 as should-fix), but all three contested-point tables grade the Task 3 dependency minor (R2-A:104, R2-B:105, R2-C:100). The tables are used here.

## Planned Changes
### Change 1: Build the one blocking Task 7 finding (from Variants A and C, approval timing from INV-001)
- **Source**: Variant A F3 (A:54-74); Variant C R3-F4 path list (C:63-81); advocates' merged order (R2-A:69, R2-B:51, R2-C:53-62); INV-001 repair (INV:8)
- **Target**: Base R3-F1 (C:7-26) (restructure) -> M-01
- **Rationale**: C-009 and X-005 won by C at 85% (debate-transcript.md, Scoring Matrix); U-002 merged as the consequence (retry.md:41, :44). Basis moved from the commit ID to the "Then ... run it" against "Make the commit the last action of the task" clash in TL:110 (R2-B:9, R2-C:49).
- **Integration point**: replace R3-F1's claim, severity basis, evidence and recommendation. Add F3's `head-moved` consequence, R3-F4's path list, the refusal line and the attended-run Constraint line (A-005, R2-A:92).
- **Risk**: Medium. The approval timing in the fix comes from INV-001, which the advocates did not adjudicate (see (b)).

### Change 2: Cadence-run finding downgraded and merged (from Variants A and B)
- **Source**: Variant A F4 part (a) (A:79-83); Variant B R2-1 (B:7-37), keeping its Goal tie to TL:15 (B:19-20)
- **Target**: Base R3-F2 (C:27-43) (replace severity and recommendation) -> M-02
- **Rationale**: C-002 at 90% and X-002 at 95%; B and C conceded blocking (R1-B:41, R1-C:48); no vacuous fallback (R2-B:18).
- **Integration point**: severity blocking -> should-fix. Recommendation per R2-C:69.
- **Risk**: Low. INV-006 (MEDIUM) asks the fix to choose one reading in writing; carried as an open invariant.

### Change 3: Verb-syntax finding promoted to should-fix and narrowed (from the debate)
- **Source**: R2-A:22-44, R2-B:53-66, R2-C:21-43
- **Target**: Base R3-F3 (C:44-62) (replace) -> M-03
- **Rationale**: U-007 graded should-fix (top) by all three (R2-A:102, R2-B:100, R2-C:96); only the guard line (SRC:86) cannot be paraphrased.
- **Integration point**: severity minor -> should-fix; claim narrowed to TL:21 against TL:52 and TL:87; fix per R2-C:43.
- **Risk**: Low.

### Change 4: Three exact refusal texts as a standalone finding (from Variant A)
- **Source**: Variant A F2 (A:33-53)
- **Target**: Base, new finding after R3-F3 (insert) -> M-04
- **Rationale**: X-004 won by A at 95%; C conceded (R1-C:50). Listed as should-fix by B and C (R2-B:76, R2-C:71).
- **Integration point**: new entry; class drift, with a spec-erratum note for SRC:306.
- **Risk**: Low (additive).

### Change 5: Task 3 dependency reduced to the red-window residual (from Variants A and B)
- **Source**: Variant A F1 (A:7-32); Variant B R2-4 dependency half (B:83-92)
- **Target**: Base R3-F5 (C:82-99) (append contributors); remove R3-F4's dependency sentence (C:69-71)
- **Rationale**: C-001 and X-001 at 95%; A conceded (R1-A:43). `/sc:implement` ignores `depends-on` and runs in source order (SKILL.md:79, :97).
- **Integration point**: M-05 keeps R3-F5's fix and adds "add Task 3 to the Depends-on lines of Tasks 4 and 7 as documentation".
- **Risk**: Low.

### Change 6: AC-0.6 fallback merged (from Variants A and B)
- **Source**: Variant A F4 part (b) (A:83-86); Variant B R2-2 (B:38-62)
- **Target**: Base R3-F14 (C:231-243) (append contributors) -> M-06
- **Rationale**: C-003 at 70%, all minor.
- **Risk**: Low.

### Change 7: Closing phase-report task extended (from Variants A and B)
- **Source**: Variant A F7 (A:134-153); Variant B R2-3 (B:63-79) and R2-4 phase-end half (B:93-96, B:107-110); B's L3 staging note (B:179-182)
- **Target**: Base R3-F11 (C:185-203) (append) -> M-07
- **Rationale**: C-004 at 80%; A-008 at 80% (one recorded closing `git add .dev/tasks`, R2-A:94, R2-B:92, R2-C:88).
- **Risk**: Low (additive).

### Change 8: Negative-check finding merged (from Variant A)
- **Source**: Variant A F5 (A:96-113)
- **Target**: Base R3-F8 (C:133-152) (append contributor) -> M-08
- **Rationale**: C-005 at 70%.
- **Risk**: Low.

### Change 9: AC-0.9 finding merged, class fixed (from Variant A)
- **Source**: Variant A F6 (A:114-133), class `none` -> `drift` as A conceded (R1-A:45, R2-A:14)
- **Target**: Base R3-F13 (C:216-230) (append the WC-9 claim restriction) -> M-09
- **Rationale**: C-006 at 90%.
- **Risk**: Low.

### Change 10: Rule-substance finding takes B's phrase list (from Variant B)
- **Source**: Variant B R2-5 (B:111-138)
- **Target**: Base R3-F9 (C:153-167) (replace recommendation) -> M-10
- **Rationale**: C-007 won by B at 85%; C's "four `guard refused:` texts" (C:166) replaced (R2-C:16).
- **Risk**: Low.

### Change 11: Stale-cite class set to none (from Variant B)
- **Source**: Variant B R2-6 (B:139-154)
- **Target**: Base R3-F12 (C:204-215) (replace class) -> M-11
- **Rationale**: C-008 won by B at 90%; C conceded (R1-C:52). SRC:59 cites the same stale range.
- **Risk**: Low.

### Change 12: Test-coverage finding reclassed (from the debate)
- **Source**: R1-C:53
- **Target**: Base R3-F6 (C:100-116) (replace class `regression` -> `drift`; note the calibrator's "count overstated", C:285) -> M-12
- **Risk**: Low.

### Change 13: Live-evidence finding added (from Variant A)
- **Source**: Variant A F8 parts (b) and (c) (A:161-164, A:172-174); part (a) dropped (R2-A:15)
- **Target**: Base, new finding (insert) -> M-15
- **Rationale**: U-003 parts (b) and (c) hold (diff:79).
- **Risk**: Low (additive).

### Change 14: Unaddressed invariants and the INV-002 candidate (from the invariant probe)
- **Source**: `invariant-probe.md` rows INV-001 to INV-007, INV-009, INV-013, INV-015 (INV:8-22)
- **Target**: new `unaddressed_invariants` list; new findings entry `INV-002` with `adjudicated: false`
- **Rationale**: the invariant gate blocks convergence on INV-001 and INV-002 (debate-transcript.md, "Invariant Probe Gate").
- **Risk**: Medium. These items were never debated.

### Change 15: Verdict header and provenance
- **Source**: debate-transcript.md, base-selection.md, this plan
- **Target**: top-level keys `merge_method`, `verdict`, `base_variant`, `convergence_score`, `convergence_status`, `blocking_count`, `rejected_changes`, `provenance`
- **Risk**: Low.

Base findings kept with no content change apart from contributor and confidence fields: R3-F7 -> M-13, R3-F10 -> M-14.

## (a) Merged Finding List
Deduplication key: the matched C-NNN topic (plus the X-, U- and A-points that the debate folded into it). Two card findings merge when they name the same plan task and the same defect (diff:13). Contributor confidence = the contributing card's calibrated confidence.

| ID | Finding | Final severity | Class | Topics | Contributors (calibrated confidence) | Debate confidence |
|---|---|---|---|---|---|---|
| M-01 | Task 7's instructions cannot all be followed in any order, on the task that commits and runs `--force` | blocking | drift (wording); the commit itself is a necessary deviation (SRC:282) | C-009, X-005, U-002, U-006, U-008, A-005 | C R3-F1 (0.87), C R3-F4 path half (0.87), A F3 (0.83) | 85% |
| M-02 | Task 8 never requires a checked run longer than the heartbeat cadence | should-fix | drift | C-002, X-002, X-003 | A F4a (0.83), B R2-1 (0.87), C R3-F2 (0.87) | 90% |
| M-03 | TL:21 widens the spec's no-copy rule to the whole file, against the guard line TL:52 requires verbatim | should-fix | drift | U-007 | C R3-F3 (0.87) | 80% (R2-B:100, R2-C:96) |
| M-04 | Tasks 1 and 5 demand "four" exact `guard refused:` texts; the spec gives three plus a case-3 prefix | should-fix | drift (inherits spec looseness; spec erratum) | X-004, U-001 | A F2 (0.83) | 95% |
| M-05 | `tests/cli` is red between Task 1 and Task 3; Depends-on lines omit Task 3 | minor | drift | C-001, X-001 | C R3-F5 (0.87), A F1 (0.83; was blocking/regression), B R2-4 dep half (0.87), C R3-F4 dep sentence (0.87) | 95% |
| M-06 | Task 8 does not carry the AC-0.6 `--source terminal` fallback into step 5 | minor | drift | C-003 | A F4b (0.83), B R2-2 (0.87), C R3-F14 (0.87) | 70% |
| M-07 | No closing task: AC-C5 never recorded, common checks not re-run at phase end, no P0 report, no closing staging | minor | drift | C-004, A-008 | C R3-F11 (0.87), A F7 (0.83), B R2-3 (0.87), B R2-4 phase-end half (0.87) | 80% |
| M-08 | Negative checks in Tasks 5 and 6 have no safe target | minor | drift | C-005 | C R3-F8 (0.87), A F5 (0.83) | 70% |
| M-09 | AC-0.9's "refused under `--unattended`" class is empty at P0; `gh api` posts undefined | minor | drift | C-006 | C R3-F13 (0.87), A F6 (0.83; was class none) | 90% |
| M-10 | Task 5's test may assert rule labels, not rule substance | minor | drift | C-007 | B R2-5 (0.87), C R3-F9 (0.87; "four texts" wording dropped) | 85% |
| M-11 | Stale cite "lines 13-25" for KNOWN_CORE_FILES | minor | none (spec has the same stale range) | C-008 | B R2-6 (0.87), C R3-F12 (0.87; was drift), A F1 recommendation (0.83) | 90% |
| M-12 | Task 4 edits HOW-WE-WORK.md but runs only three test files | minor | drift (was regression) | U-009 | C R3-F6 (0.87; calibrator: count overstated) | not contested (R1-C:53) |
| M-13 | "after P0, none" in HOW-WE-WORK.md goes stale every phase | minor | drift | U-010 | C R3-F7 (0.87) | not contested (R2-C:73) |
| M-14 | Brief template passes `--report-dir`, which no command accepts until P1 | minor | drift | U-011 | C R3-F10 (0.87) | not contested (R2-C:73) |
| M-15 | Task 7's `ls-remote` check and Task 8's coordinator check name no evidence | minor | none | U-003 (b, c) | A F8 parts b and c (0.83) | not contested (R2-A:15) |
| INV-002 | Task 8 cannot reach a passing AC-0.4 at P0 (step 3 needs a WC-4 contract) | blocking candidate, NOT ADJUDICATED | not classified (gap comes from the spec, SRC:301) | none (probe only) | invariant probe (INV:9); no reviewer | none: never debated |

Citations to keep and one-line fix per finding (every TL and SRC line below was opened):

- **M-01**. Keep: TL:25, TL:110, TL:113, SRC:282, `retry.md:41`, `retry.md:44`, `qa.md:52`, `qa.md:61`, `qa.md:288`. Fix: rewrite TL:110 as one order with each approval asked just before its own action (INV-001): install approval, install, write `t7-approvals.md` without the ID, commit approval, stage the listed P0 paths (C:77-81) plus `.dev/tasks` and commit with `git commit --only -- <paths> .dev/tasks` as the last product action, then append the commit ID and stage it; a refusal or any QA failure after the commit ends in a halt for the person's Ruling and is never retried; add a Constraint line that the run is attended and never headless.
- **M-02**. Keep: SRC:291, SRC:78, TL:15, TL:122, TL:124-128. Fix: Task 8's AC requires `ac-0.4-smoke.md` to name one checked run whose top-level session, outside Agent-tool calls, lasted longer than the preamble cadence, with start and end times; if none qualifies, add or extend a run, and if none is achieved the report records the duty as unmet and P0 does not pass (R2-C:69).
- **M-03**. Keep: TL:21, TL:42, TL:52, TL:87, SRC:59, SRC:86. Fix: scope TL:21 to the worker-session duties as SRC:59 does, and add to TL:52 "copied verbatim from `./source.md` section 2.3 'Brief layout', including its `worker_done` text" (R2-C:43).
- **M-04**. Keep: SRC:60, SRC:306, SRC:312, TL:21, TL:36, TL:41, TL:87. Fix: in TL:41 and TL:87 require "the three exact `guard refused:` texts of section 2.1 plus, for case 3, the `guard refused:` prefix and the never-as-worker condition", and log SRC:306's "four ... reason texts" as a spec erratum.
- **M-05**. Keep: `tests/cli/test_how_we_work_install.py:44`, TL:58, TL:72, TL:77, TL:108, SKILL.md:79, SKILL.md:97. Fix: move the KNOWN_CORE_FILES edit into Task 1 (or state that `tests/cli` stays red until Task 3), and add Task 3 to the Depends-on lines of Tasks 4 and 7 as documentation.
- **M-06**. Keep: SRC:291, SRC:303, TL:122, TL:127. Fix: Task 8 reads `ac-0.6-transcript.md` first; if it says no, step 5 for all three runs uses `--source terminal` output and the gap is recorded in `ac-0.4-smoke.md`.
- **M-07**. Keep: SRC:216, SRC:241, SRC:271, SRC:396, TL:15, TL:22, TL:79. Fix: add a final task that re-runs AC-C1, AC-C2, the AC-C3 comparison and AC-C4, records AC-C5 as run with an empty edit set, writes `artifacts/p0-phase-report.md` with one PASS or FAIL line per P0 check, and ends with a recorded `git add .dev/tasks`.
- **M-08**. Keep: TL:87, TL:91, TL:97, TL:100, `Makefile:171`, `Makefile:174`. Fix: the test takes the contract path and scan roots from fixtures that the negative checks monkeypatch to `tmp_path` copies, so no scratch file lands under `src/superclaude/`.
- **M-09**. Keep: TL:97, SRC:305. Fix: at P0 every hit must be allowed by WC-9 or allowlisted with the phase that converts it; define `gh api` posts as `-X POST`, `--method POST`, `-f`, `-F`, `--input`; state that WC-9's no-git-state claim covers only classified hits.
- **M-10**. Keep: SRC:59, SRC:77, TL:38, TL:87, TL:91. Fix: Task 5 lists one load-bearing phrase per rule (WC-5 outcome mapping, WC-7 top level only, WC-3 ask only when the brief allows and the one-ask bound, WC-9's three grant conditions, the WC-4 error text, "at most 10", "at least 2", the guard line).
- **M-11**. Keep: TL:60, SRC:59, `src/superclaude/cli/install_core.py:13`, `install_core.py:27`. Fix: cite `KNOWN_CORE_FILES` by symbol name, or as lines 13-27.
- **M-12**. Keep: TL:77, SRC:263. Fix: extend Task 4's AC to `uv run pytest tests/core tests/commands tests/recommend tests/cli -q`, compared with a baseline taken in Task 1.
- **M-13**. Keep: TL:74, SRC:212. Fix: say a command accepts `--unattended` only when its file has an `## Unattended mode` section, and point to `~/.claude/WORKER-CONTRACT.md` for the never-as-worker list.
- **M-14**. Keep: TL:49, SRC:143, SRC:152, SRC:221. Fix: the template marks `--report-dir` as "from P1".
- **M-15**. Keep: TL:116, TL:122, TL:26. Fix: Task 7 saves the `git ls-remote origin` output to an artifact and checks that the Task 7 commit ID is absent from it; Task 8 states that the coordinator is the person-opened implement session and records that check.
- **INV-002**. Keep: SRC:73, SRC:285, SRC:301, TL:122, TL:125. Fix (probe's repair, not adjudicated): Task 8 states a P0 version of step 3, with the outcome taken from the command's own status through the WC-4 mapping (SRC:72) and the report path equal to the existing report file, and puts it in each brief so the worker does not apply WC-5's no-contract rule; log SRC:301 as a spec gap.

## (b) Carrying INV-001 and INV-002 into the Merged Verdict
Both are HIGH and UNADDRESSED in the probe (INV:8-9). Neither was argued by any advocate: the probe ran after Round 2, and Round 3 did not run (depth standard). The merged card must say so plainly.

**INV-001 (HIGH, sufficiency_challenge).**
- Carry it as an entry in `unaddressed_invariants` with severity HIGH, using the probe's assumption text (INV:8).
- Link it from M-01 through `open_invariants: [INV-001, INV-003, INV-004, INV-005, INV-007]`.
- It is not a new defect. It says the advocates' prescribed Task 7 fix ("ask both approvals up front", R2-B:51, R2-C:54) is not enough: TL:25 requires approval "at the moment of action", so a reviewer can quote TL:25 against the fixed order and pass the byte-present Read-back (`qa.md:52`, `qa.md:61`). The commit still moves HEAD inside Task 7, so a failed A2 halts `head-moved` with no adviser (`retry.md:41`, `retry.md:44`).
- M-01's fix text uses the probe's repair order (each approval asked just before its own action). The action order is the same as the advocates' fix; only the approval timing differs. Mark M-01 `fix_source: "advocates' merged order (R2-A:69, R2-B:51, R2-C:53-62) with approval timing from INV-001 (not adjudicated)"`.
- M-01 stays blocking either way. INV-001 does not change the blocking count.

**INV-002 (HIGH, sufficiency_challenge). A candidate second blocking finding.**
- Carry it twice: as an `unaddressed_invariants` entry (severity HIGH), and as a `findings` entry with `id: INV-002`, `severity: blocking`, `adjudicated: false`, `counted_in_blocking_count: false`.
- The entry's `status_note` must read: "Candidate second blocking finding raised by the Round 2.5 invariant probe. Not adjudicated by the advocates. Not counted in blocking_count."
- Why it is a candidate: AC-0.4 needs 7.2 steps 1-3 and 5-7 to pass and swaps in the existing report only for step 4 (SRC:301; TL:122). Step 3 passes only when the outcome "matches the contract's `worker_status` under WC-5" and the report path "is the WC-4 contract path" (SRC:285). No P0 command writes a WC-4 contract, and WC-5 sends `--outcome failed` when no contract exists (SRC:73). TL:125's escape lets Task 8 complete, but the phase cannot pass (SRC:241). Under the debate's own clause (d), "a P0 pass condition that no task performs" (R2-B:89, R2-C:85), this would be blocking.
- `blocking_count` = 1 (adjudicated findings only). If INV-002 is later confirmed, it becomes 2. The verdict is FAIL either way, because M-01 alone fails the plan.

**MEDIUM warnings.** INV-003, INV-004, INV-005, INV-006 and INV-007 (INV:10-14) go into `unaddressed_invariants` with severity MEDIUM. INV-006 is linked from M-02. They do not change the verdict.

**LOW.** INV-009, INV-013 and INV-015 (INV:16, :20, :22) go into `unaddressed_invariants` with severity LOW. The ADDRESSED rows (INV-008, INV-010, INV-011, INV-012, INV-014, INV-016) are left out of the card and recorded only in `provenance`.

## Changes NOT Being Made (with rationale)
These go into `rejected_changes` in the merged card.

| Diff Point | Non-Base or Card Approach | Rationale for Not Adopting |
|------------|-------------------|---------------------------|
| C-001, X-001 | A's F1 as blocking, class regression (A:8-9) | `/sc:implement` ignores `depends-on` and runs unmarked tasks in source order (SKILL.md:79, :97), so Task 4's AC passes; A conceded (R1-A:43). |
| C-002, X-002 | B's R2-1 (B:8) and C's R3-F2 (C:28) as blocking | TL:122 brings step 5 in by reference and another run can be added; both conceded (R1-B:41, R1-C:48). |
| C-002 | B's fallback "record the heartbeat clause as vacuous for P0" (B:35-37) | SRC:291 exists to stop a vacuous pass; B withdrew it (R2-B:18). |
| C-002 | B's suggested long troubleshoot Tier-2 run (B:33-34) | SRC:291 excludes time inside an Agent-tool call, and SRC:78 names Tier 2 as Agent-tool fan-out; B conceded (R2-B:17). |
| U-007 | C's Round 1 call to raise R3-F3 to blocking (R1-C:23, :69) | A compliant reading exists and the plan points to it; C withdrew (R2-C:7). |
| S-006, A-003 | B's Round 1 count of 0 blocking (R1-B:65) | B's test dropped the executor's B4 trigger (`qa.md:52`); B withdrew (R2-B:7). |
| C-007, X-004 | C's "the four `guard refused:` texts" (C:166) | SRC:60 gives three exact texts and AC-1.7 checks case 3 by prefix only (SRC:312); C conceded (R1-C:50). |
| U-003 | A's F8 part (a), run AC-C6 before the live runs (A:158-161) | "at any depth setting" is WC-13 text (SRC:81), not Task 8 text, and D5 orders the trace before a depth raise (SRC:394); A conceded (R2-A:15). |
| U-005 | B's R2-4 fix "Task 6 depends on Task 4" (B:107) | Rests on the rejected A-002; Task 4 always runs before Task 6 (SKILL.md:97); B conceded (R1-B:43). |
| U-004 | B's `matrix_omissions` as plan findings (B:155-185) | They concern the reflect coverage matrix, not the plan (diff:80). Route them to the reflect tool, not this card. |
| A-008 | A separate should-fix for post-commit staging (R1-C:81) | Downgraded to one closing line inside M-07; C moved (R2-C:19). |
| X-006 | Class `regression` for R3-F6 (C:102), `drift` for R3-F12 (C:206), `none` for F6 (A:116) | All conceded (R1-C:52-53, R1-A:45). |
| C-009 | R3-F1's basis "the acceptance criterion cannot pass" (C:15-16) | TL:113 can be met by writing the record after the commit; the blocking basis is the install-versus-commit order clash (R2-B:41, R2-C:49). |
| C-009 | The advocates' wording "ask both approvals up front" (R2-B:51, R2-C:54) | Replaced by per-action approval timing because of INV-001 (TL:25, INV:8). Not adjudicated; flagged in M-01's `fix_source`. |
| C-001 | Treat "add Task 3 to the Depends-on lines" as a required fix (B:107; C:80-81) | Documentation only under source-order execution (R1-C:51); kept as part of M-05's fix text, not as its own finding. |

## (d) merged-verdict.yaml Schema
Target file: `.dev/reflect/pre-TASK-WF-orcaWorkerContra-20261102-231950-20261102232329/adversarial/merged-verdict.yaml`. The ten top-level keys below are required and must appear in this order. Each row of section (a) becomes one `findings` entry; each row of "Changes NOT Being Made" becomes one `rejected_changes` entry.

```yaml
merge_method: adversarial                 # const
verdict: FAIL                             # PASS | FAIL. FAIL when blocking_count >= 1 (R2-A:91, R2-B:89, R2-C:85)
base_variant:                             # the Step 3 selection
  label: C
  file: variant-3-original.md
  reviewer: 3
  persona: refactorer
convergence_score: 0.9615                 # float in [0,1]; 25 agreed / 26 points
convergence_status: BLOCKED_BY_INVARIANTS # CONVERGED | NOT_CONVERGED | BLOCKED_BY_TAXONOMY | BLOCKED_BY_INVARIANTS
blocking_count: 1                         # int; adjudicated findings with severity blocking only (INV-002 excluded)
findings:                                 # list; 16 entries: M-01..M-15, then INV-002
  - id: M-01                              # M-NN for adjudicated findings; INV-NNN for probe-only entries
    title: "Task 7's instructions cannot all be followed in any order"
    severity: blocking                    # blocking | should-fix | minor
    deviation_class: drift                # drift | necessary | none | regression | authorized
    class_note: "the commit itself is a necessary deviation (SRC:282)"   # optional
    adjudicated: true                     # false only for probe-only entries
    counted_in_blocking_count: true       # true iff severity == blocking and adjudicated == true
    topics: [C-009, X-005, U-002, U-006, U-008, A-005]
    contributors:                         # one item per merged card finding
      - {reviewer: 3, card_finding: R3-F1, calibrated_confidence: 0.87, original_severity: blocking, original_class: drift}
      - {reviewer: 3, card_finding: R3-F4, calibrated_confidence: 0.87, original_severity: minor, original_class: drift}
      - {reviewer: 1, card_finding: F3, calibrated_confidence: 0.83, original_severity: minor, original_class: necessary}
    debate_confidence: 0.85               # from the scoring matrix; null when not contested
    citations: ["TL:25", "TL:110", "TL:113", "SRC:282", "retry.md:41", "retry.md:44", "qa.md:52", "qa.md:61", "qa.md:288"]
    fix: "<one line from section (a)>"
    fix_source: "advocates' merged order (R2-A:69, R2-B:51, R2-C:53-62) with approval timing from INV-001 (not adjudicated)"   # optional
    open_invariants: [INV-001, INV-003, INV-004, INV-005, INV-007]   # optional
  # ... M-02 to M-15 in the same shape ...
  - id: INV-002
    title: "Task 8 cannot reach a passing AC-0.4 at P0"
    severity: blocking
    deviation_class: unclassified
    adjudicated: false
    counted_in_blocking_count: false
    status_note: "Candidate second blocking finding raised by the Round 2.5 invariant probe. Not adjudicated by the advocates. Not counted in blocking_count."
    topics: []
    contributors: []                      # no reviewer raised it (INV:9)
    debate_confidence: null
    citations: ["SRC:73", "SRC:241", "SRC:285", "SRC:301", "TL:122", "TL:125"]
    fix: "<probe repair from section (a)>"
unaddressed_invariants:                   # list; exactly these four fields per item
  - {id: INV-001, category: sufficiency_challenge, assumption: "<INV:8 assumption text>", severity: HIGH}
  - {id: INV-002, category: sufficiency_challenge, assumption: "<INV:9 assumption text>", severity: HIGH}
  - {id: INV-003, category: sufficiency_challenge, assumption: "<INV:10>", severity: MEDIUM}
  - {id: INV-004, category: guard_conditions, assumption: "<INV:11>", severity: MEDIUM}
  - {id: INV-005, category: state_variables, assumption: "<INV:12>", severity: MEDIUM}
  - {id: INV-006, category: interaction_effects, assumption: "<INV:13>", severity: MEDIUM}
  - {id: INV-007, category: guard_conditions, assumption: "<INV:14>", severity: MEDIUM}
  - {id: INV-009, category: guard_conditions, assumption: "<INV:16>", severity: LOW}
  - {id: INV-013, category: collection_boundaries, assumption: "<INV:20>", severity: LOW}
  - {id: INV-015, category: interaction_effects, assumption: "<INV:22>", severity: LOW}
rejected_changes:                         # list; one item per row of "Changes NOT Being Made"
  - {diff_point: C-001, proposal: "F1 blocking, class regression", source: "A:8-9", reason: "source-order execution (SKILL.md:79, :97); conceded R1-A:43"}
  # ... remaining rows ...
provenance:
  diff_analysis: adversarial/adversarial/diff-analysis.md
  debate_transcript: adversarial/adversarial/debate-transcript.md
  invariant_probe: adversarial/adversarial/invariant-probe.md
  base_selection: adversarial/adversarial/base-selection.md
  refactor_plan: adversarial/adversarial/refactor-plan.md
  variants: {A: variant-1-original.md, B: variant-2-original.md, C: variant-3-original.md}
  calibrated_confidences: {A: 0.83, B: 0.87, C: 0.87}   # A:209, B:241, C:284
  rounds_completed: 2
  round_2_5: ran
  round_3: skipped (depth standard)
  omissions: 0
  base_scores: {A: 0.810, B: 0.845, C: 0.812, tiebreaker: "level 1, debate points C 13 vs B 6"}
  addressed_invariants: [INV-008, INV-010, INV-011, INV-012, INV-014, INV-016]
  blocking_count_note: "1 adjudicated (M-01). INV-002 is an unadjudicated candidate; if confirmed, 2. Verdict FAIL either way."
  approved_by: auto
  approval_timestamp: "2026-11-03T00:39:08Z"
```

Validation the merge-executor must run on the written file: all ten top-level keys present; `blocking_count` equals the number of findings with `severity: blocking` and `adjudicated: true` (expected 1); every `unaddressed_invariants` item has exactly `id`, `category`, `assumption`, `severity`; every finding has at least one citation; `verdict` is FAIL when `blocking_count >= 1`.

## Risk Summary
| Change # | Risk | Impact if Failed | Rollback |
|----------|------|------------------|----------|
| 1 | Medium | The blocking finding's fix carries probe text the advocates never weighed (INV-001) | Revert M-01's `fix` to the advocates' merged order (R2-C:53-62) and keep INV-001 only in `unaddressed_invariants` |
| 2 | Low | Cadence fix stays ambiguous (INV-006) | Keep R3-F2's original recommendation (C:41-43) with severity should-fix |
| 3-13 | Low | Local wording, class or contributor changes to single findings | Restore the base finding text from `variant-3-original.md` |
| 14 | Medium | An unadjudicated item could be read as a debate result | Keep `adjudicated: false` and `counted_in_blocking_count: false`; if contested, drop the INV-002 findings entry and keep only the `unaddressed_invariants` row |
| 15 | Low | Header fields drift from the transcript | Recompute from `debate-transcript.md` and `base-selection.md` |

## Review Status
- [x] Auto-approved (default)
- [ ] User-approved (--interactive)
- Approved by: auto
- Approval timestamp: 2026-11-03T00:39:08Z
