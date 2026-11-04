# Adversarial Debate Transcript

## Metadata
- Depth: standard
- Rounds completed: 2 (Round 1 parallel statements, Round 2 rebuttals). Round 2.5 (invariant probe) ran. Round 3 skipped because depth=standard (Round 3 runs only at `--depth deep`, ADV-SKILL:193-195).
- Convergence achieved: 96.2% (25 of 26 diff points agreed)
- Convergence threshold: 80%
- Convergence status: BLOCKED_BY_INVARIANTS (INV-001, INV-002 are HIGH and UNADDRESSED, invariant-probe.md:8-9)
- Focus areas: correctness, coverage, deviation-classification
- Advocate count: 3 (default model; personas analyzer, qa, refactorer)
- Interactive: no
- Variants: A = `variant-1-original.md` (reviewer 1, analyzer), B = `variant-2-original.md` (reviewer 2, qa), C = `variant-3-original.md` (reviewer 3, refactorer) (diff-analysis.md:6-8)
- Generated: 2026-11-03T00:39:08Z by the debate-orchestrator (no agents spawned; the orchestrator did not take part in the debate)
- Cite keys: `A:N`, `B:N`, `C:N` = variant line; `R1-A:N` etc. = `round1-advocate-a.md` line; `R2-A:N` etc. = `round2-advocate-a.md` line; `diff:N` = `diff-analysis.md` line; `INV:N` = `invariant-probe.md` line; `TL:N` = plan line; `SRC:N` = `source.md` line; `SKILL.md`, `qa.md`, `retry.md` = files under `~/.claude/skills/sc-implement-protocol/`; `ADV-SKILL:N` = `~/.claude/skills/sc-adversarial-protocol/SKILL.md`. Every cite below was opened by the orchestrator for this transcript.
- Transcript note: the six round statements below are copied in full from the round files. Their own headings are demoted by three levels (`#` becomes `####`) so they nest under this transcript's headings; no other text is changed.

## Round 1: Advocate Statements

### Variant A Advocate (default model:analyzer)
#### Round 1 Advocate Statement: Variant A (reviewer 1, analyzer)

Cite keys as in `diff-analysis.md`: `A:N`, `B:N`, `C:N` = card line; `TL:N` = plan line; `SRC:N` = `source.md` line. Executor files are the installed copies under `~/.claude/skills/sc-implement-protocol/`. Every TL, SRC and executor line cited below was opened for this statement.

##### Position summary

The plan is not ready to run, so FAIL holds. But my card's blocking finding F1 does not survive: `/sc:implement` runs tasks in source order, so Task 3 runs before Task 4. The FAIL should rest on Task 7, by merging my F3 (a QA failure after the commit halts with `head-moved`) with C's R3-F1 (the task's own order cannot be followed). The cadence-run gap (C-002) is should-fix, not blocking.

##### Steelman

**Variant B (qa).** B's strongest argument is R2-1. SRC:291 puts an unconditional duty on "each phase report": name at least one checked run longer than the heartbeat cadence. Task 8's acceptance criteria (TL:124-128) never mention it, and the Goal (TL:15) claims every P0 check passes. B is right that a run made only of short smoke runs would leave the WC-10 check passing vacuously. B is also right on R2-5: an ID-only test would pass on a file that names rules without stating them. Its `matrix_omissions` block is careful work. And B's self-audit honestly names the one assumption its R2-4 depends on (B:232-234).

**Critique of B.** R2-1's blocking grade contradicts B's own R2-2 reasoning. Both clauses sit in SRC:291, and the same TL:122 sentence brings both in by reference. B calls R2-2 minor *because* of that delegation (B:46-49) and denies the same delegation to R2-1 (X-003). The "unsatisfiable after the fact" claim (B:22-23) is wrong: one more longer run can be added. B's proposed fix, a long troubleshoot Tier-2 run (B:34), would not count. SRC:291 excludes time "inside an Agent-tool call" from the spacing rule, and SRC:78 names troubleshoot Tier 2 ("+4-15 min") as exactly that kind of Agent-tool fan-out. The dependency half of R2-4 and all of U-005 rest on the executor assumption that SKILL.md:79 and :97 contradict.

**Variant C (refactorer).** C's strongest argument is R3-F1. TL:110 says to commit, then ask for and run the `--force` install, then "Make the commit the last action of the task". TL:113 also wants the commit ID inside `t7-approvals.md`. No order meets every instruction: installing after the commit breaks "commit last", and committing last means installing first, against the stated order. C is right, and this lands on the task that runs an owner-approved overwrite of `~/.claude`. C also has the widest coverage: U-007 (Task 1's whole-file criterion against Task 2's section 2.3 content), U-008 (`--only` with an unlisted path set), U-009, U-010 and U-011 are all real, and none of them appear in my card.

**Critique of C.** Its own calibrator downgraded R3-F2 (C:285), which leaves R3-F1 as C's only blocking finding. R3-F9 tells the test to pin "the four `guard refused:` texts" (C:166), but SRC:60 defines only three exact texts, so C's fix would make the executor invent a string (X-004). R3-F6 is labelled `regression` (C:102), but nothing in the repo breaks. The finding is about a test run the AC leaves out, which is drift. Calling R3-F12, a stale line cite, `drift` (C:206) ignores that the spec's own cite is stale too (SRC:59: `install_core.py:13-24`). The dependency half of R3-F4 (C:69-71) rests on the same executor assumption as B's R2-4.

##### Strengths claimed

1. **Only card that checks how the executor behaves (U-002, High).** F3 (A:54-74) shows that Task 7's commit moves HEAD inside an implement task window. Retry check 3 requires HEAD to equal `q0-head`, and a mismatch counts as moved (retry.md:41). When A2 fails, the executor writes `halt review=2 reason=head-moved` and stops with `E-HALT-QA`, and no adviser is spawned (retry.md:44). Task 7 is not a batch task, because the plan marks nothing `independent` (a grep of the plan finds no hit; SKILL.md:97), so the ladder applies. This is the half of the Task 7 defect that C does not see: whatever order is chosen, QA runs after the commit (SKILL.md:126, Q3 after Q1).
2. **F2 is correct, and C repeats the error F2 warns about (X-004).** SRC:60 quotes three exact texts (case 1, case 2, copies-disagree). Case 3 has only its condition and the body prefix. TL:41 and TL:87 demand "the four `guard refused:` reason texts". Meeting the AC means inventing a case-3 string, which strains TL:21 ("adds no rule the spec lacks"). AC-1.7 checks case 3 only by its prefix (SRC:312).
3. **The cadence gap gets the right severity (C-002, X-002).** I graded it minor (A:76). That is consistent with how the executor reviews: QA compares the diff with the task's AC, the plan's Constraints and the explicit task instructions (qa.md:13-17), and TL:122 brings step 5 in by reference. C's calibrator came to the same conclusion (C:285), and B's own logic implies it (X-003). F4 also covers the AC-0.6 fallback in the same finding (A:83-86), which all three cards agree is minor.
4. **The most complete fix for the phase-end gaps (C-004).** F7 (A:134-153) is the only recommendation that re-runs AC-C4 as well as AC-C1 and AC-C2, records AC-C5 as vacuous, and writes one P0 pass/fail report. SRC:216 makes that report the gate for P1, and SRC:241 sets the rule it applies. R2-3 and R2-4 cover only parts of this. R3-F11 matches F7 and adds the file name.
5. **F5 names the safe-target problem (C-005),** and F6 is the only finding that ties the AC-0.9 classification to the claim gate in SRC:305 ("WC-9's 'a worker writes no git state' is claimed only once this passes"). A P0 pass built on free-text allowlist entries would make that claim while outward defaults are still live (SRC:222, P2 row).
6. **The only card that uses `necessary` where it fits.** Task 7's commit itself is required by SRC:282 ("the phase's edits are committed ... with the user's authorization"). Calling the commit drift (C:9) mixes the forced commit with the wording defect around it (X-006).
7. **It states its own uncertainty.** A:16-17 says the order "depends on task numbering, which the plan does not state", and A:202-205 lists what was not verified. The concessions below follow from those stated gaps.

##### Weaknesses identified in others

1. **B, R2-1 vs R2-2:** the delegation argument is applied to one clause of SRC:291 and not to the other (B:46-49 vs B:10-23). The grade is inconsistent with B's own reasoning.
2. **B, R2-1 fix:** the suggested Tier-2 run would not exercise heartbeat spacing (SRC:291 Agent-tool exception; SRC:78).
3. **B, R2-4 and U-005:** these rest on a dependency-driven executor. SKILL.md:79 says "Ignore MDTM fields (`depends-on`, ...) except `independent`", and SKILL.md:97 says "Default sequential in source order ... Unmarked = sequential". Task 4 (the AC-C3 after-comparison runs in Task 6) always runs before Task 6.
4. **B, R2-3 cite:** the calibrator notes it cites TL:17 for text at TL:20 (B:243).
5. **C, R3-F9:** "the four `guard refused:` texts" (C:166) pins a string the spec never defines (SRC:60).
6. **C, R3-F2:** graded blocking, then downgraded by its own calibrator (C:285). C kept the blocking grade in its card, and that grade drives C's FAIL.
7. **C, R3-F6 class:** `regression` needs a working behaviour that breaks. The finding describes an AC that runs too few tests (TL:77), which is drift. Its calibrator also says the count and one cite are overstated (C:285).
8. **C, R3-F4 dependency half:** this has the same executor flaw as B's R2-4. The path-list half (U-008) is right and stands on its own.
9. **Both B and C miss the executor's retry ladder.** Neither card says what happens when Task 7 fails QA after the commit (retry.md:41, :44).

##### Concessions

1. **F1 is neither blocking nor a regression.** The plan's executor is `/sc:implement` (SRC:238). It ignores Depends-on (SKILL.md:79) and runs tasks in source order (SKILL.md:97), and the plan marks nothing `independent`. Task 3 therefore runs before Task 4, and the AC at TL:77 passes. My own text admits the order "depends on task numbering" (A:16-17), and the executor rules settle that question against me. What remains is C's R3-F5: `tests/cli` is red between Task 1 and Task 3, but no AC observes that window (TL:40-43, TL:51-54). Merged grade: minor, drift. The fix is to add Task 3 to the Depends-on lines anyway, as documentation, or to move the registration into Task 1. F1's other half, that the commit could leave out `install_core.py`, is really C's U-008 (the paths are never listed, TL:110). It does not depend on order.
2. **My reading of "commit last" was too generous (X-005).** A:60-61 treated it as a partial mitigation. C is right that TL:110 cannot be followed as written, because the install comes after the commit.
3. **F6's class should be `drift`, not `none`.** TL:97 uses a classification the spec permits (SRC:305) but which is empty at P0. That is a gap in what the plan delivers.
4. **Coverage gaps in my card:** it has nothing on rule-substance assertions (R2-5, R3-F9), Task 1's whole-file criterion against Task 2's content (U-007), the unlisted commit paths (U-008), other tests that read HOW-WE-WORK.md (U-009), the stale "after P0, none" line (U-010) or the `--report-dir` flag in the template before P1 (U-011). All of these should be in the merged list.
5. **F8 is weaker than I graded it.** Part (a) misquotes Task 8 ("at any depth setting" is WC-13 text, SRC:81) and D5's order. Part (b) overstates: "no new push" can be checked without a before-state by confirming that the Task 7 commit ID is absent from `git ls-remote origin`. The plan should say so in one line. Part (c) is only a clarification: the implement session runs each task in its own session (SKILL.md:118, Q1), so a person-opened implement session is the coordinator TL:122 asks for.
6. **My deviation-classification sub-score (0.65, A:208) was the lowest on any card, and that was earned.** The `regression` label on F1 was wrong.

##### Positions on diff points

| Point | Preferred variant or merged position | Reason with cite |
|---|---|---|
| S-006 (calibration) | Merged: after calibration and the executor rules, exactly one blocking finding remains: Task 7 (A's F3 merged with C's R3-F1). | F1 falls to SKILL.md:79,97. R3-F2 was downgraded by C's own calibrator (C:285). R2-1 holds only as "borderline" (B:242), and X-003 removes its basis. R3-F1 holds (C:285). |
| C-001 (Task 3 not a dependency) | B/C grade: minor, drift. Merged finding = R3-F5 (red window from Task 1 to Task 3), plus "add Task 3 to the Depends-on lines of Tasks 4 and 7 as documentation". | Source-order execution (SKILL.md:97). TL:77 passes because Task 3 has already run. The window from Task 1 to Task 3 is real (`tests/cli/test_how_we_work_install.py:44`) but no AC observes it. |
| C-002 (cadence run) | A: minor, should-fix before running. Use C's AC wording (C:42-43) and add B's fallback clause "or record vacuous and flag" (B:35-37). Drop B's Tier-2 suggestion. | TL:122 delegates step 5, and QA checks only the AC and instructions (qa.md:13-17). The requirement can still be met by adding a run. Agent-tool time is excluded (SRC:291, SRC:78). |
| X-001 | B and C are right (minor). I concede. | SKILL.md:79,97. No `independent` marker in the plan. |
| X-002 | A is right (minor). | Same as C-002. C's calibrator agrees (C:285). |
| X-003 | B is inconsistent. This supports minor for both R2-1 and R2-2. | Both clauses are in SRC:291 and both are delegated by TL:122. B:46-49 vs B:10-23. |
| X-004 | A is right. The merged fix: "the three exact texts of SRC:60, plus for case 3 the `guard refused:` prefix and a statement that the command is on the never-as-worker list". Note the spec erratum. | SRC:60 gives three texts. TL:41 and TL:87 say four. SRC:306 says "four ... reason texts", and SRC:312 checks case 3 by prefix only (see A-007). |
| X-005 | C is right that the wording is incoherent. A's F3 adds the retry consequence. Merge both into one Task 7 finding, graded **blocking**. | TL:110: commit, then install, then "commit last". TL:113 wants the commit ID in a file. No order meets every instruction. Whatever order is chosen, QA runs after the commit, so a failed A2 halts `head-moved` (retry.md:41, :44). Fix: make the commit the final step of its own task, or reorder to install, record, then commit, and add a line saying that a QA failure after the commit goes to the person. |
| X-006 | Task 3 gap: drift (concede). AC-0.9 label gap: drift (concede). Stale cite: none (B). Task 7: one finding classed drift for the wording, with a note that the commit itself is a necessary deviation (SRC:282). | Diff-analysis resolution for X-006. SRC:59 has its own stale range. TL:60 edits by symbol name. |
| U-002 | Keep. Merge into the blocking Task 7 finding. | retry.md:41 (moved HEAD, a missing file counts as moved). retry.md:44 (`halt review=2 reason=head-moved`, STOP). SKILL.md:97 (not a batch task). |

##### Shared-assumption responses

- **A-002 (the executor follows Depends-on edges): REJECT.** SKILL.md:79 ignores `depends-on`, and SKILL.md:97 runs "sequential in source order" unless a set is marked `independent`. The plan has no such marker. This removes the trigger for my F1, for U-005 and for the dependency halves of R2-4 and R3-F4. I relied on this assumption, and it was wrong.
- **A-003 (one blocking finding means FAIL, with "blocking" undefined): QUALIFY.** No rule in the reviewer brief defines "blocking" (reviewer-briefs/reviewer-1.md:1-35 has no severity rule). I propose this test, modelled on the executor's own severity model (qa.md:41, :49-52): a plan finding is **blocking** when following the plan as written, in source order under `/sc:implement`, forces the executor either to break one of the plan's own explicit instructions or Constraints, or to leave a P0 pass condition unmet (SRC:241), and no executor choice satisfies all of them. Everything an attentive executor can still satisfy is should-fix. Under this test, Task 7 is blocking (no order fits TL:110 and TL:113). F1 is not (source order). C-002 is not (a longer run can be added). F2 and U-007 are not (an executor can write three exact texts plus a prefix, and can restate section 2.3's rules while pointing to the preamble for verb syntax), but both should be fixed before the run, because they set the plan's ACs against TL:21. One blocking finding means FAIL.
- **A-005 (the run is attended): QUALIFY.** The executor is designed for an attended session. It accepts "a clear user confirmation in the current conversation" (qa.md:256), so Task 7's two approval pauses (TL:25, TL:110) can work. The implement session runs each task in its own session (SKILL.md:118), so a person-opened implement session satisfies D5 for Task 8 (TL:122). The plan never says the run must be attended and must not run headless (`claude -p`). Add one Constraint line. Minor.
- **A-007 (the spec is a consistent authority): ACCEPT that it is contradicted.** SRC:60 (three exact texts) conflicts with SRC:306 ("four refusal conditions and reason texts"), and SRC:59 cites `install_core.py:13-24` where the set spans 13-27. Consequence for the merge: F2 and the stale-cite findings should say that the plan inherits looseness from the spec. Fix the plan with a recorded decision, and log a spec erratum. Do not treat the plan's copy of the spec's wording as an invented rule.
- **A-008 (artifacts after the commit need no staging): QUALIFY, leaning REJECT as a plan defect.** The executor already applies the always-staged rule: "`.dev/tasks/` is always staged (`git add .dev/tasks`): the package, its `progress.md` ledger and `artifacts/` included" (managed-workspace.md:36; also ledger.md:3). TL:22 says staging is not committing, so Task 8 and Task 9 artifacts left staged but uncommitted are consistent with the rule. The real staging defect sits at the commit: TL:110 commits with `git commit --only -- <paths>` but never lists the paths, so a staged `.dev/tasks` is left out unless it is named (U-008). Keep U-008 as should-fix. Do not add A-008 as a separate finding.

### Variant B Advocate (default model:qa)
#### Round 1 Advocate Statement: Variant B (reviewer 2, qa)

Cite keys: `A:N`, `B:N`, `C:N` = card line; `TL:N` = plan line; `SRC:N` = `source.md` line; `SKILL:N` = `~/.claude/skills/sc-implement-protocol/SKILL.md`; `qa:N`, `retry:N`, `mw:N` = that skill's `refs/qa.md`, `refs/retry.md`, `refs/managed-workspace.md`. Every TL, SRC and file cite below was opened for this statement.

##### Position summary

B found the defect all three cards agree matters most for a live phase: a P0 heartbeat check that can pass without testing anything (R2-1). B also found the only rule-substance gap that is grounded in the spec's own wording (R2-5), and B is the only card that flagged the L3 staging rule (B:179-182). B graded R2-1 too high and reasoned about it inconsistently (X-003), and the dependency half of R2-4 rests on an executor assumption that is wrong. Once the executor's real rules are applied, no finding on any card stays blocking. The merged result should be one list of must-fix minors, led by the cadence run (R2-1), with no blocking item.

##### Steelman

**Variant A (analyzer).** A's best argument is F1. It names a real test, `tests/cli/test_how_we_work_install.py:44` (`KNOWN_CORE_FILES == frozenset(install_core.list_core_files())`), that goes red as soon as Task 1 creates the file. It shows that the plan's own dependency lines (TL:58, TL:72, TL:108) never put Task 3 before Task 4 or Task 7. A is also the only card that checked the executor's mechanics. Its U-002 (F3) is verified: the retry ladder requires "HEAD has not moved" (retry:41), so a QA retry after Task 7's commit halts with `head-moved` (retry:334). A is right that the spec gives three exact refusal texts, not four (F2; SRC:60). These are the most precise findings on any card.

**Variant C (refactorer).** C's best argument is breadth with verification. It has 14 findings and several verified ones no other card has: `git commit --only -- <paths>` leaves a staged `.dev/tasks` out of the commit unless it is named (U-008, TL:110). The `--report-dir` flag in the brief template is not accepted by any command until P1 (U-011; SRC:143, SRC:152, SRC:221). A scratch skill left behind by Task 6's negative check would break `make verify-sync` (R3-F8). R3-F5 is the part of the Task 3 dependency issue that holds under any executor: `tests/cli` is red between Task 1 and Task 3, and no acceptance criterion in that window runs it (TL:40-43, TL:51-54).

##### Strengths claimed

1. **R2-1 is the right finding, and it is about a false pass.** SRC:291 says "A run shorter than the cadence passes the heartbeat part vacuously, so each phase report names at least one checked run that lasted longer than the cadence." Task 8's acceptance criteria (TL:124-128) record "each 7.2 step's result" and require "all listed steps pass". Three short runs satisfy TL:125 while the spec says the heartbeat check was never exercised. All three cards found this gap (A F4a, C R3-F2). B tied it to the plan Goal at TL:15 ("every P0 check ... passing"), which no other card did. B's recommendation (B:31-37) is the most usable of the three: name the long run, or record the clause as vacuous and carry it to the next phase. The second option keeps the record honest even when no long run is possible.
2. **R2-5 is grounded in the spec's exact wording.** SRC:59 says that for the worker-session duties the file "states only the IronClaude-specific rule (outcome mapping from `worker_status`, top-level only, ask only when the brief allows it)". TL:38 lists those duties only by ID ("WC-3, WC-5, WC-7, WC-12, WC-13"). B names exactly the phrases a test should look for (B:135-138). C's matching finding R3-F9 instead asks the test to pin "the four `guard refused:` texts" (C:166), which the spec does not define (see Weakness 7). B's version can be adopted without that error.
3. **B is the only card that noticed the L3 staging rule.** B's `matrix_omissions` says "L3's staging rule has no direct row despite binding Task 7's commit" (B:179-182; SRC:396: "the coordinator stages `.dev/tasks` at every commit and at the end of the run"). That is the root of shared assumption A-008, which the diff analysis says "no card notices". B noticed the rule but did not raise it as a plan finding.
4. **B states its executor assumption openly.** B's self-audit says it "assumed /sc:implement executes tasks honoring only stated Depends-on edges ... a strictly sequential executor would mask them" (B:232-234). That sentence is what let the diff analysis check the assumption against SKILL:79 and SKILL:97 and settle X-001. A relies on the same assumption with only a hedge (A:16-17), and C relies on it without saying so (C:69-71).
5. **R2-6 has the right class.** B classes the stale "lines 13-25" cite (TL:60) as `none` (B:141), because the edit is made by symbol name and the spec's own cite is also stale (SRC:59 cites `install_core.py:13-24`). C calls the same thing drift (C:206). Drift means the plan departs from the spec. Here the plan simply repeats a stale range the spec also has.
6. **B's self-audit cleared several things correctly.** B checked that Task 2's 12-command list matches section 3.1, that Task 6's verb list matches AC-0.9, that there is no AC-0.8 in the spec, and that step-4 deferral is authorized by AC-0.4's pass condition (B:224-229; SRC:301). These are negative results that stop the merged list from gaining false findings.
7. **R2-3 is the narrowest correct form of the AC-C5 gap.** AC-C5 appears nowhere in the plan. SRC:241 says "A phase passes only when every check in its block and every common check passes", and AC-C5 (SRC:271-274) is a common check. B asks only for one record line marking it vacuous (B:78-79). A (F7) and C (R3-F11) fold this into a larger phase-report task. That task is also worth adding, but B's version is the smallest correct fix.

##### Weaknesses identified in others

1. **A, F1: blocking and regression both rest on the wrong executor model.** The plan runs under `/sc:implement`, which says "Ignore MDTM fields (`depends-on`, ...) except `independent`" (SKILL:79) and "Default sequential in source order ... Unmarked = sequential" (SKILL:97). Nothing in the plan is marked `independent`, so Task 3 runs before Task 4. Task 4's AC (TL:77) therefore passes. The defect is in the dependency text, and the only red window (Tasks 1 to 3) is not checked by any AC. That is minor drift (C's R3-F5), not a blocking regression.
2. **A, F6: class `none` is wrong.** TL:97 adds a classification ("refused under `--unattended` by the phase that converts its command") that is empty at P0, because no command has the section yet (TL:20). The plan departs from what the spec can mean at P0, so the class is drift (C's R3-F13), not none.
3. **A, F8(a): weak.** A's own calibrator says "at any depth setting" is not in Task 8 and that D5 orders the trace before a raise, not before live runs (A:210; SRC:394). Parts (b) and (c) hold.
4. **C, R3-F1: "cannot pass" is overstated.** C's calibrator says so (C:285). `t7-approvals.md` can be written after the commit, and that file sits in `.dev/tasks`, so writing it changes nothing the commit needs. The real defect is that the wording at TL:110 is ambiguous: the order is commit, install, then "Make the commit the last action". That should be merged with A's F3 `head-moved` risk as one minor finding on Task 7.
5. **C, R3-F2: blocking.** C's own calibrator downgrades it to minor because TL:122 brings in step 5 by reference (C:285). I accept that downgrade for both R3-F2 and my own R2-1 (see Concessions).
6. **C, R3-F3: overstated.** TL:42 forbids "`orca orchestration` verb syntax **copied from Orca's guides**". The verb syntax Task 2 adds comes from the spec's section 2.3 (SRC:84 `worker-start --worktree new-child --base-branch`; SRC:88 `orca worktree rm`), not from Orca's guides. A literal grep-based check would still trip, so the finding is a real ambiguity. It is minor, and the fix is the qualifier TL:42 already has, made explicit.
7. **C, R3-F9: asks the test to pin text the spec does not define.** SRC:60 gives three exact texts: `brief lacks --unattended`, `loaded command has no Unattended mode section (...)` and `command copies disagree (stale copy): <paths>`. Case 3 has only the `guard refused:` prefix, and AC-1.7 checks case 3 only by that prefix (SRC:312). Pinning "the four `guard refused:` texts" (C:166) would make the executor invent a fourth string, which breaks TL:21 ("adds no rule the spec lacks"). A's F2 is right here.
8. **C, R3-F12: drift is the wrong class for the stale cite.** See Strength 5.
9. **C, R3-F6: count and one cite overstated** (C's calibrator, C:285). The underlying point holds: Task 4 edits HOW-WE-WORK.md but its AC runs three test files (TL:77), and AC-C3 covers only `tests/skills/` (SRC:263).
10. **A and C both missed the rule-substance gap B raises for the worker-session duties.** C's R3-F9 reaches it, but not the SRC:59 parenthetical. A has no finding on it.

##### Concessions

1. **X-003 is a real inconsistency in B.** B grades R2-2 (the `--source terminal` fallback) minor *because* TL:122 brings in the spec's 7.2 text by reference (B:46-49, B:199-203). B then grades R2-1 blocking even though the cadence sentence is in the same SRC:291 step and is brought in by the same TL:122 sentence. B's stated difference, that one clause is unconditional and the other conditional (B:20-21), explains why R2-1 is more likely to be missed. It does not explain why delegation counts for one clause and not the other. The consistent grading is: both minor, with R2-1 first in priority because it applies on every run.
2. **R2-1 is not blocking.** B's own calibrator held it only as "borderline" (B:242). It is in scope by reference (TL:122). It is not "unsatisfiable after the fact" (B:22-23): SRC:291 asks for one checked run longer than the cadence, and another run can be added later in the phase.
3. **B's suggested way to make a long run does not work.** B proposes "a troubleshoot symptom needing Tier-2 fan-out" (B:34). SRC:291 excludes time "while the session is inside an Agent-tool call" from the heartbeat rule, and SRC:78 names troubleshoot Tier 2 as exactly that kind of Agent-tool fan-out. A Tier-2 run would be long but would still test no heartbeat spacing. The recommendation should ask for a run whose top-level session, outside Agent-tool calls, lasts longer than the cadence.
4. **The dependency half of R2-4, and U-005, are void under the real executor.** Under source-order execution (SKILL:97), Task 4 runs before Task 6, and Task 3 runs before Task 7. What survives of R2-4 is the phase-end re-run: SRC:241 judges the phase's final state, and AC-C1 and AC-C2 run only in Task 4 (TL:79). This part matters more than B said, because C's R3-F8 shows Task 6's negative check could leave a scratch skill that breaks `make verify-sync` after AC-C2 has already passed.
5. **R2-3 cites TL:17; the "P0 edits no command file" text is at TL:20** (B:243). This is a cite error that does not change the finding.
6. **B missed findings that hold:** A's U-002 (`head-moved`, retry:41, retry:334), A's F2 (three texts), the safe target for the negative checks (A F5, C R3-F8), the empty AC-0.9 class (A F6, C R3-F13), C's U-008 (`--only` pathspec), U-011 (`--report-dir` before P1) and R3-F5 (red window). B's coverage was narrower than A's or C's.

##### Positions on diff points

| Point | Preferred variant or merged position | Reason with cite |
|---|---|---|
| S-006 | Merged: after calibration and the executor check, no card keeps a firm blocking finding | B's R2-1 is "borderline" (B:242). C's R3-F2 is downgraded (C:285), and its R3-F1 "cannot pass" is called overstated (C:285). A's F1 does not fire under SKILL:79 and SKILL:97. The three FAIL verdicts rest on three different defects, and none survives. |
| C-001 | C (R3-F5 plus the dependency text in R3-F4), minor drift | The test at `test_how_we_work_install.py:44` is real, but source-order execution (SKILL:97) runs Task 3 before Task 4 and Task 7. The surviving defect is the unchecked red window between Task 1 and Task 3, plus dependency lines (TL:72, TL:108) that would mislead any other executor. Fix: move the registration into Task 1, or add Task 3 to the Depends-on lines of Tasks 4 and 7. |
| C-002 | B's recommendation (B:31-37) with Concession 3 applied, graded minor and listed first | SRC:291 makes the duty unconditional. TL:124-128 does not name it, and QA checks the task's AC, the plan's Constraints and explicit task instructions (qa:13-17), so QA may well not check it. It is the likeliest false pass in the plan. It is not blocking because TL:122 brings it in by reference and a further run can be added. |
| X-001 | B and C: minor | SKILL:79 ("Ignore MDTM fields (`depends-on` ...)") and SKILL:97 ("Unmarked = sequential"). A's "cannot pass at the point Task 4 runs" (A:11) does not happen under this executor. |
| X-002 | A: minor, but listed first among the minors | See C-002. B's blocking grade is withdrawn (Concessions 1 and 2). |
| U-002 | A's F3, merged with C's R3-F1 into one minor finding on Task 7 | retry:41 requires that HEAD has not moved, and retry:334 refuses with `head-moved`. The outcome is a safe halt that waits for a person's Ruling, not harm, so it is minor. Merged fix: state one order (install, write `t7-approvals.md`, commit last), and add one line saying that a QA failure after the commit stops the run and reports to the person. The class is necessary for the commit itself (SRC:282 requires it) and drift for the wording at TL:110. |
| X-003 | Against B | See Concession 1. Both clauses come from SRC:291 through the same TL:122 sentence, so both are graded minor. |
| X-004 | A | SRC:60 gives three exact texts. Case 3 is defined by its condition plus the prefix, and AC-1.7 checks case 3 by prefix only (SRC:312). TL:41 and TL:87 say "four". The plan should say three texts plus the case-3 prefix. The spec's own looseness (SRC:306, "four refusal conditions and reason texts") should be logged as a spec note, not charged to the plan. |
| X-005 | Merged (see U-002) | C is right that TL:110 is ambiguous. A is right that "commit last" only reduces the `head-moved` exposure. Neither makes the AC at TL:113 impossible. |
| X-006 | Task 3 gap: drift (B and C). AC-0.9 label gap: drift (C). Stale cite: none (B). Task 7: necessary for the commit, drift for the wording | A's "regression" needs a checked point that breaks, and none exists under SKILL:97. TL:97 adds a class that is empty at P0, which is drift. SRC:59 has the same stale range, so the plan did not drift. SRC:282 requires the commit. |

##### Shared-assumption responses

- **A-002 (executor follows Depends-on edges): REJECT.** SKILL:79 tells the executor to ignore `depends-on`, and SKILL:97 runs tasks in source order unless they are marked `independent`. The plan marks nothing `independent`. B stated this assumption (B:232-234) and it was wrong. The merged list should keep the dependency lines only as a minor clarity fix, and should drop U-005.
- **A-003 (one undefined "blocking" means FAIL): QUALIFY.** No card cites a rule that defines blocking, and the reflect protocol's blocking rules concern reachability and durable sinks (`~/.claude/skills/sc-reflect-protocol/SKILL.md:501`), not plan readiness. I propose this test: a finding is blocking only if the plan, run by `/sc:implement` in source order, (a) has an AC that cannot pass, or (b) causes an irreversible or outward effect with no guard. Under that test no finding on any card is blocking. Task 7's `--force` install and commit are guarded by owner approval (TL:25, TL:110), and `head-moved` halts safely (retry:334). The merged verdict should report 0 blocking findings and a must-fix list. Whether must-fix minors alone fail the plan is a verdict rule the debate should settle explicitly. My view as qa: fix them before running, because Tasks 7 and 8 are costly to repeat (owner approvals, a `--force` overwrite of `~/.claude`, live Orca runs), while each fix is one line of plan text.
- **A-005 (the run is attended): QUALIFY.** `/sc:implement` neither provides nor forbids an in-task question to the owner. A search of SKILL.md and its refs finds no rule about asking the user mid-task. Task 7 needs two approvals at the moment of action (TL:25, TL:110), and Task 8 needs the executing session to be the person-opened coordinator (TL:26, TL:122). Both work only if a person attends the run. The plan should say so in its Constraints, as a minor finding next to A's F8(c). It is not blocking, because a refused or absent approval makes Task 7 "stop this task and report" (TL:110), which is a safe stop.
- **A-007 (`source.md` is consistent and complete for P0): REJECT.** SRC:60 gives three exact refusal texts, SRC:306 speaks of "four refusal conditions and reason texts", and SRC:59 cites `install_core.py:13-24` against the real range of 13-27. Findings caused by the spec's own looseness (F2/R3-F9 text count, the R2-6/R3-F12 stale cite) should be graded as the plan inheriting a spec defect: class none or a spec note, not plan drift.
- **A-008 (post-commit artifacts need no staging): QUALIFY.** The gap is real at the plan level: TL:22 says `.dev/tasks/` is always staged, SRC:396 (L3) stages `.dev/tasks` "at the end of the run", and no task after Task 7 stages anything (TL:118-136). B's `matrix_omissions` already noted that L3 has no matrix row (B:179-182). But the executor covers most of it: `mw:36` says the package, its `progress.md` and `artifacts/` are always staged with `git add .dev/tasks`, and that the new path is staged again after the move to `done/`. Staging is not committing, so artifacts left uncommitted after Task 7 are expected. The merged list should carry this as one minor finding: add a closing line, or a closing step in the phase-report task (C's R3-F11), that runs `git add .dev/tasks` after Tasks 8 and 9.

### Variant C Advocate (default model:refactorer)
#### Round 1 Advocate Statement: Variant C (reviewer 3, refactorer)

Cite keys as in `diff-analysis.md`: `A:N`, `B:N`, `C:N` = card line; `TL:N` = plan line; `SRC:N` = `source.md` line. Executor files are cited by their installed path under `~/.claude/skills/sc-implement-protocol/`. Every TL, SRC and executor line below was opened for this statement.

##### Position summary

The verdict should stay FAIL ("not ready to run"), but for a different reason than any single card gives. The plan's real defects are internal contradictions that the plan's own executor will check at the end and cannot fix mid-run. The plan is hash-pinned after the first task starts (SKILL.md:40, `E-PLAN-CHANGED`), and the managed FINAL review is blocking and re-checks every acceptance criterion and every Constraints item against the end state (refs/qa.md:310). C is the only card that reads the plan for internal consistency, and that is where the blocking-grade defects are: Task 7's step order (R3-F1, merged with A's F3) and the clash between Task 2's content and the file-wide "no verb syntax" rule (R3-F3, which I now argue was under-graded). Most of the other findings, including my own R3-F2, are should-fix.

##### Steelman

**Variant A (analyzer).** A's strongest contribution is F3 (U-002): it is the only card that checks how the executor actually runs a task. It shows that a commit inside a `/sc:implement` task window disables the retry ladder, because ladder check 3 needs HEAD unchanged since Q0 ("A missing file ... counts as moved", refs/retry.md:41) and the revert code refuses with `head-moved` (refs/retry.md:333-334). That is verified, and it is the single most important executor fact in the debate. A also gets X-004 right: the spec quotes only three exact `guard refused:` texts (SRC:60), so "the four ... reason texts" (TL:41) makes the executor invent a case-3 string. A's F1 reasoning is also right as far as the text goes: Task 3 is missing from the Depends-on lines of Tasks 4 and 7 (TL:72, TL:108), and `tests/cli/test_how_we_work_install.py:44` will fail between Task 1 and Task 3.

Critique: A's only blocking finding (F1) depends on an executor that follows Depends-on edges. `/sc:implement` ignores `depends-on` (SKILL.md:79) and runs tasks "sequential in source order" (SKILL.md:97). Task 3 therefore always runs before Task 4 and Task 7, and Task 4's acceptance criterion passes. A half-concedes this ("the order depends on task numbering, which the plan does not state", A:16-17), but the executor does state it. F1 is minor, and "regression" is the wrong class: no checked behaviour breaks.

**Variant B (qa).** B's strongest argument is R2-1: the spec puts an unconditional duty on every phase report to name one checked run longer than the heartbeat cadence (SRC:291), Task 8's acceptance criteria (TL:124-128) never mention it, and the Goal (TL:15) claims every P0 check passes. B also adds `matrix_omissions` (U-004), which is useful for the reflect tool even if it is not a plan defect, and R2-5 on rule-substance assertions, which matches my R3-F9.

Critique: B grades R2-2 minor because TL:122 delegates step 5 to the spec text (B:46-49), then grades R2-1 blocking although the cadence sentence sits in the same delegated step (SRC:291). That is inconsistent (X-003). B's recommendation also lets the report "record the heartbeat clause as vacuous for P0" (B:35-37), which SRC:291 forbids: the sentence exists precisely so the check is not passed vacuously. B's example of a long troubleshoot Tier-2 run (B:34) would not count either, because SRC:291 excludes time "inside an Agent-tool call" and SRC:78 names troubleshoot Tier 2 as that kind of fan-out. B's R2-4 (dependency gaps) rests on the same dependency-driven-executor assumption as A's F1, which B itself names (B:232-234).

##### Strengths claimed

1. **C is the only card that tests the plan against itself, which is where the executor's blocking gate looks.** The managed FINAL returns `issues` when "an AC is unmet at the end state ... a later change contradicts it, a plan `## Constraints` item is violated" (refs/qa.md:310), and `issues` stops the run with `E-ARCHIVE-BLOCKED` (refs/qa.md:286; refs/managed-workspace.md:54, :61). This is a managed package (path shape `<id>/<id>.md` under `.dev/tasks/to-do/`, SKILL.md:55), so the FINAL is "not advisory and never skipped" (SKILL.md:160). Findings about one part of the plan contradicting another part are therefore checked by a gate that cannot be waived.

2. **R3-F3 is stronger than my card stated, and should be raised.** Task 1's acceptance criterion (TL:42) and the plan's Constraints item TL:21 both apply to the whole file: "for Orca verb syntax and heartbeat cadence it points to the dispatch preamble instead of copying them". The spec limits that rule to the worker-session duties (SRC:59: "For the worker-session duties (WC-3, WC-5, WC-7, WC-12, WC-13 and heartbeats) ... it never copies them"). Task 2 (TL:49) then requires WC-6 and section 2.3 "in full", and that text contains Orca verb syntax: `task-create --spec` and `worker-start --retry-of` (SRC:74), `worker-start --worktree new-child --base-branch` (SRC:84), `orca worktree rm` (SRC:88). My card cited TL:42 only; the TL:21 Constraints item makes it worse, because Constraints are checked by every review and by the FINAL (refs/qa.md:16, :310). The plan has widened a spec rule into a Constraint that its own Task 2 must break. A defender can point to the qualifier "copied from Orca's guides" (TL:42) and say spec-sourced text is not a copy; that reading may survive, but it leaves the non-waivable FINAL to decide an ambiguity the plan created.

3. **R3-F1 (Task 7 order) is a real self-contradiction on the one irreversible step.** TL:110 orders commit, then install, then says "Make the commit the last action of the task". TL:113 needs `t7-approvals.md` to hold the commit ID and the install output. No order satisfies all three literally: if the commit is last, the commit ID is written after it, so the commit is not last. QA compares the diff with "explicit instructions on the task" (refs/qa.md:17), so the executor must break one instruction a reviewer is told to check. Combined with A's F3, any blocking review finding on Task 7 after the commit halts the run with `head-moved` (refs/retry.md:41, :333-334). This task runs an owner-approved commit and a `--force` overwrite of `~/.claude`, including `~/.claude/CLAUDE.md` (TL:25, TL:110).

4. **Plan hash-pinning raises the bar for "ready to run".** Once the first task starts, any change to the plan stops the run (`E-PLAN-CHANGED`, SKILL.md:40). So every should-fix item in the merged list must be applied before the run, not discovered and patched during it. This is why a plan with many cheap wording fixes is "not ready" even when only one or two findings are blocking.

5. **Finest-grained finding list, which makes the merge easier.** C splits the cadence duty (R3-F2) from the AC-0.6 fallback (R3-F14) and the Task 7 path list (R3-F4) from the red-test window (R3-F5) (S-002). Each recommendation names concrete text: the full Task 7 path list including `.dev/tasks` inside the `--only` pathspec (C:77-81), which no other card gives (U-008); the `gh api` post patterns (C:229-230); and the stable HOW-WE-WORK.md wording that does not go stale each phase (C:130-132, U-010).

6. **Unique, verified coverage gaps.** R3-F10: the brief template copies `--report-dir` for cleanup-audit and workflow (SRC:143, :152), a flag no command accepts until P1 (SRC:221). R3-F6: Task 4's AC runs three test files (TL:77), but nine files under `tests/` mention HOW-WE-WORK (re-checked by grep for this statement). Five of them are covered neither by Task 4's AC nor by AC-C3: tests/recommend/test_cache.py, tests/recommend/test_routing_refresh.py, tests/unit/test_cli_install.py, tests/commands/test_routing_plugin_parity.py and tests/commands/test_help_command.py. AC-C3 covers only `tests/skills/` (SRC:263).

7. **R3-F5 is the part of the dependency finding that survives the executor rules.** Under source-order execution, `tests/cli/test_how_we_work_install.py:44` is red between Task 1 and Task 3, and no acceptance criterion runs `tests/cli` in that window (TL:40-43, TL:51-54). This is the diff analysis's own conclusion for X-001.

##### Weaknesses identified in others

1. **A's F1 is graded on the wrong executor.** Blocking/regression requires Task 4 to run before Task 3, which SKILL.md:79 and :97 rule out. The class "regression" needs a checked behaviour to break; none does (X-006).
2. **A's F2 and my R3-F9 disagree, and A is right** (see Concessions). A's F6 class "none" is wrong: TL:97 adds a classification the spec allows (SRC:305) that is empty at P0, which is drift.
3. **A's F8(a) is weak**, as its own calibrator says (A:210): "at any depth setting" is WC-13 text (SRC:81), not Task 8 text, and D5 orders the trace before a depth raise, not before live runs (SRC:394).
4. **A misses the internal contradictions entirely.** A treats "commit last" as a mitigation it can follow (A:60-61) without noticing that the body's order and TL:113 contradict it, and it does not see the TL:21/TL:42 versus TL:49 clash.
5. **B's R2-1 severity contradicts B's own delegation argument** (X-003; B:46-49 versus B:10-23), and its "record as vacuous" fallback is ruled out by SRC:291.
6. **B's R2-4 and U-005 rest on a dependency-driven executor** that B itself flags as an assumption (B:232-234); SKILL.md:97 removes the trigger.
7. **B omits whole areas**: the unsafe negative checks (C-005), the AC-0.9 empty class (C-006), the Task 7 mechanics (C-009), and the brief-template flag problem (U-011).
8. **B's R2-3 cites TL:17**; the "P0 edits no command file" text is at TL:20 (B:243).

##### Concessions

1. **R3-F2 is should-fix, not blocking.** My calibrator was right (C:285). TL:122 makes step 5 an explicit instruction on Task 8, and QA checks "explicit instructions on the task" (refs/qa.md:17). The gap is that TL:124-128 does not name the clause, so QA may not check it. It stays the highest-priority should-fix, and the fix should require the run (add or extend one, outside any Agent-tool call), not allow "vacuous".
2. **R3-F1's phrase "the acceptance criterion cannot pass" is overstated.** TL:113 can be met by writing `t7-approvals.md` after the commit. What cannot be met is the full set of task instructions together. I keep it blocking on that narrower ground and on irreversibility, merged with A's F3.
3. **R3-F9's "four `guard refused:` texts" is wrong.** SRC:60 gives three exact texts; case 3 has only the prefix. The merged recommendation should be A's: three exact texts plus the case-3 prefix and condition.
4. **R3-F4's dependency sentence relied on a dependency-driven executor** ("a dependency-driven executor could commit before ...", C:69-70). Under SKILL.md:97 that cannot happen. The path-list part of R3-F4 stands; adding Task 3 to the Depends-on lines is documentation only.
5. **R3-F12 should be class none, not drift.** The spec's own cite is stale too (SRC:59, `install_core.py:13-24`), and the edit is made by symbol name (TL:60).
6. **R3-F6 is mis-classed as regression.** It is a test-coverage gap (drift); nothing has broken. My calibrator also flagged the count and the test_help_command cite as overstated (C:285). The finding stays minor.
7. **My self-confidence (0.72) was the lowest of the three**, and my self-audit admits partial reads of two test files and no codegraph use (C:270-273).

##### Positions on diff points

| Point | Preferred variant or merged position | Reason (with cite) |
|---|---|---|
| S-006 (calibration) | Apply every calibration: R3-F2 to should-fix; R3-F1 kept blocking with narrowed wording; R2-1 to should-fix for consistency; F1 to minor | C:285 and B:242 already signal the downgrades; F1's calibrator "yes" (A:210) did not test the executor (SKILL.md:79, :97) |
| C-001 / X-001 (Task 3 dependency) | B and C: minor / drift. Keep R3-F5's red window as the residual; fix by moving the KNOWN_CORE_FILES edit into Task 1 or adding Task 3 to the Depends-on lines | Source-order execution (SKILL.md:97) runs Task 3 before Tasks 4 and 7; `tests/cli/test_how_we_work_install.py:44` is red only between Task 1 and Task 3 |
| C-002 / X-002 (cadence run) | Merged: should-fix / drift, top of the should-fix list; fix as C recommends (C:42-43) | TL:122 delegates step 5; QA checks task instructions (refs/qa.md:17); SRC:291 forbids the "vacuous" fallback B offers; Agent-tool time does not count (SRC:291, SRC:78) |
| C-003 (AC-0.6 fallback) | All agree: minor / drift | SRC:291 holds the fallback; TL:127 records the answer only |
| X-003 (B's delegation reasoning) | Diff analysis is right: B is inconsistent | Both clauses sit in SRC:291 and are delegated by the same TL:122 sentence |
| X-004 (number of exact refusal texts) | A | SRC:60 quotes three texts; case 3 is defined by condition and prefix only; AC-1.7 checks case 3 by prefix (SRC:312) |
| X-005 (Task 7 "commit last") | Merge C's R3-F1 with A's F3 into one Task 7 finding, blocking | The wording forces a breach of a task instruction QA checks (TL:110, TL:113, refs/qa.md:17); a blocking finding after the commit halts `head-moved` (refs/retry.md:41, :333-334); the step is irreversible (TL:25) |
| X-006 (classes) | Task 3 gap: drift (B, C). AC-0.9 empty class: drift (C). Stale cite: none (B). Task 7: the commit is necessary (A), the wording is drift (C); the merged finding is drift because the defect is the wording, not the commit | SRC:305; SRC:59; SRC:282; TL:110 |
| U-002 (retry ladder after the commit) | A, verified; merged into the Task 7 finding | refs/retry.md:41, :333-334; Task 7 is not a batch task (SKILL.md:97) |
| U-007 / R3-F3 (verb-syntax rule versus Task 2) | Raise to blocking candidate, at least top should-fix | TL:21 and TL:42 apply file-wide; SRC:59 limits the rule to worker-session duties; Task 2 must add text with verb syntax (TL:49; SRC:74, :84, :88); Constraints and end-state ACs are checked by the non-waivable FINAL (refs/qa.md:310; SKILL.md:160) |

##### Shared-assumption responses

**A-002 (executor follows Depends-on edges): REJECT.** `/sc:implement` ignores `depends-on` (SKILL.md:79) and runs "sequential in source order"; "Unmarked = sequential" (SKILL.md:97). The plan marks no task `independent`. Every finding whose severity depends on out-of-order execution (A's F1, B's R2-4 and U-005, the dependency sentence of my R3-F4) is minor at most. R3-F5's window between Task 1 and Task 3 is the only part that survives.

**A-003 (one undefined "blocking" means FAIL): QUALIFY.** One blocking finding should fail the plan, but "blocking" needs a test, and the executor supplies one. I propose: a finding is blocking when, under `/sc:implement` as it will actually run (source order, hash-pinned plan per SKILL.md:40, non-waivable managed FINAL per refs/qa.md:310), following the plan as written forces a breach of its own AC, Constraints item or explicit task instruction, or leaves a section 7 P0 pass condition with no task that performs it. A spec duty that is delegated by reference but not named in an AC is should-fix. Under this test, F1, R2-1 and R3-F2 are should-fix, and the blocking set is the merged Task 7 finding (R3-F1 plus F3) and, as a candidate, R3-F3. The verdict stays FAIL, but on defects the debate can check.

**A-005 (execution is attended, so mid-task owner approvals work): QUALIFY.** The approvals are required (SRC:282; TL:25), and a person runs `/sc:implement`, so someone is present. But the executor's interrupt list is closed: "No other path may stop automation or prompt the user" (refs/qa.md:288), and its STOP table has no row for "the owner refused an approval" (SKILL.md:24-42). TL:110's "stop this task and report" is not an executor outcome. If the owner refuses, Task 7's AC is unmet, QA fails, and the retry ladder may re-attempt the task and ask again. If the commit was made and the install refused, the ladder halts `head-moved`. Task 7 should say what a refusal produces: record the refusal in `t7-approvals.md` and expect the halt and a Ruling, not a retry. The coordinator half (Task 8 run from a person-opened session, TL:26, TL:122) is plausible because the executing session is the one the person opened, but no task records that check (A's F8(c)).

**A-007 (the spec is consistent and complete for P0): REJECT.** SRC:60 gives three exact refusal texts, and SRC:306 speaks of "four refusal conditions and reason texts". SRC:59 cites `install_core.py:13-24`, but the frozenset spans 13-27. Two consequences for the merge: the plan should not be faulted for copying the spec's stale range (R3-F12 and R2-6 are class none), and the plan should not pin a case-3 text the spec does not define (A's F2 is right, my R3-F9 wording is wrong).

**A-008 (post-commit artifacts need no staging): REJECT.** TL:22 says `.dev/tasks/` is always staged, and spec decision L3 has the coordinator stage `.dev/tasks` "at every commit and at the end of the run" (SRC:396). The Constraints item binds every task in principle (refs/qa.md:16), but no task after Task 7 stages anything (TL:118-136), and no AC checks it, so Task 8 and Task 9 artifacts, and `t7-approvals.md` if it is written after the commit, can be left unstaged. All three cards missed this. Fix: the closing phase-report task I proposed (R3-F11) should end with `git add .dev/tasks` and record that it ran. Grade: should-fix, drift.

## Round 2: Rebuttals

### Variant A Rebuttal
#### Round 2 Rebuttal: Variant A (reviewer 1, analyzer)

Cite keys as in Round 1: `A:N`, `B:N`, `C:N` = card line; `TL:N` = plan line; `SRC:N` = `source.md` line; `qa:N`, `retry:N`, `mw:N`, `SKILL:N` = the installed `~/.claude/skills/sc-implement-protocol/` files (`refs/qa.md`, `refs/retry.md`, `refs/managed-workspace.md`, `SKILL.md`); `R1-A:N`, `R1-B:N`, `R1-C:N` = Round 1 statement lines. Every TL, SRC and executor line below was opened for this statement.

##### Position summary

The verdict stays FAIL, with **one blocking finding: Task 7** (my F3 merged with C's R3-F1). B's "0 blocking" uses a test that is narrower than the executor's own: the executor treats a breach of an explicit task instruction as a blocker on the same footing as an unmet AC (qa:45-52), and Task 7's instructions cannot all be met in any order. C's R3-F3 is a **real conflict but not blocking**: the exact guard line that Task 2 must copy does contain Orca syntax, but the plan points to a reading under which every instruction holds, and a halt on Task 2 lands before anything irreversible and with the adviser's dispute route still open. It is the top should-fix item, next to the cadence run. I correct one Round 1 claim of my own (U-007) and accept C's point that "record as vacuous" cannot satisfy the cadence duty.

##### 1. Responses to criticisms of Variant A

| Criticism (source) | Response |
|---|---|
| F1 blocking/regression rests on the wrong executor model (R1-B:27, R1-C:13, :37) | **Conceded in Round 1, unchanged.** SKILL:79 ignores `depends-on`; SKILL:97 runs unmarked tasks in source order. F1 becomes C's R3-F5 (red window Task 1 to Task 3, no AC observes it): minor, drift. |
| F6 class `none` is wrong (R1-B:28, R1-C:38) | **Conceded.** TL:97 uses a class that is empty at P0. Drift. |
| F8(a) is weak (R1-B:29, R1-C:39) | **Conceded.** "at any depth setting" is WC-13 text (SRC:81), and D5 orders the trace before a depth raise, not before live runs. F8(b) and F8(c) stand as minor. |
| A treats "commit last" as a followable mitigation (R1-C:40; A:60-61) | **Conceded in Round 1** (R1-A:44). Section 3 below goes further: the instruction cannot be met in any order. |
| A misses the TL:21/TL:42 versus TL:49 clash (R1-C:40) | **Conceded as a coverage gap, and I correct my own Round 1 reasoning.** At R1-A:68 I said an executor "can restate section 2.3's rules while pointing to the preamble for verb syntax". That is wrong for one item: TL:52 requires "the exact guard line text from section 2.3", and that line contains `worker_done --outcome failed` (SRC:86). The executor cannot paraphrase it away. See section 2 for the grade. |
| A relies on the executor assumption "with only a hedge" (R1-B:20) | **Conceded.** The hedge at A:16-17 named the right question; the executor rules answered it against me. |
| U-002 (head-moved) is only a "safe halt", so minor (R1-B:56) | **Partly conceded.** B is right that the halt harms nothing: the revert refuses before any change (retry:333-334), and no adviser runs (retry:44). But "safe" is not the test for plan readiness. The halt arrives *after* the owner-approved commit and the `--force` overwrite of `~/.claude`, and it can only be cleared by a person's Ruling. Section 3 shows the halt is the expected outcome of an attentive review, not a remote risk. U-002 stays part of the blocking Task 7 finding, as its consequence rather than its cause. |
| My C-002 merged fix added B's "or record vacuous and flag" (R1-A:56); C says SRC:291 forbids it (R1-C:17, :62) | **Conceded to C.** SRC:291 says a short run "passes the heartbeat part vacuously, so each phase report names at least one checked run that lasted longer than the cadence". A vacuous record is exactly what the sentence exists to prevent. Merged fix: Task 8's AC requires at least one checked run whose top-level session, outside Agent-tool calls, lasts longer than the cadence; if none is achieved, the report records the duty as unmet and P0 does not pass. |

##### 2. Ruling on R3-F3 (Task 2 versus the no-verb-syntax rule)

**The text.**
- TL:21 (Constraints): "for Orca verb syntax and heartbeat cadence it points to the dispatch preamble instead of copying them (section 2.1, "Contract file")". As worded, it covers the whole file.
- TL:42 (Task 1 AC): "no `orca orchestration` verb syntax **copied from Orca's guides** and no fixed heartbeat cadence".
- TL:49 and TL:52 (Task 2): section 2.3 "in full", and the AC demands "the exact guard line text from section 2.3 'Brief layout'".
- SRC:86, the guard line: "... on a refusal run nothing and send worker_done --outcome failed with a body starting "guard refused:"."
- SRC:59 limits the no-copy rule to "the worker-session duties (WC-3, WC-5, WC-7, WC-12, WC-13 and heartbeats)", and in the same sentence puts "the template's guard line" in the file.
- TL:54 (Task 2 AC): "The file mentions Orca commands only as the coordinator's and worker session's channel, which `./source.md` SA-2 permits for this file."

**Is the conflict real? Yes, but narrower than C says.**
1. TL:42 is not breached. Its qualifier "copied from Orca's guides" excludes text copied from the spec, and the guard line comes from SRC:86.
2. Most of the Orca syntax C lists can be paraphrased, because no AC asks for it verbatim: `worker-start --worktree new-child --base-branch` (SRC:84), `orca worktree rm` (SRC:88), `--retry-of` and `task-create --spec` (SRC:74).
3. One item cannot be paraphrased: the guard line's `worker_done --outcome failed`, which TL:52 requires byte for byte. If TL:21 is read literally, as covering the whole file, no executor choice satisfies both TL:21 and TL:52.
4. If TL:21 is read with its own cite, the conflict disappears. The plan points to that reading in four places: TL:21 cites section 2.1 "Contract file" (SRC:59, scoped to worker-session duties, and the guard line is explicitly included); TL:38 scopes "pointing to the dispatch preamble" to the worker-session duties; TL:42 restricts the AC to syntax "copied from Orca's guides"; and TL:54 anticipates Orca commands in this file.

So the plan widened a scoped spec rule in one Constraint sentence. This is a plan defect, not one inherited from the spec (SRC:59 is consistent here). Class: drift.

**Is it blocking under the executor's QA rules? No. It is the top should-fix item.**
- What makes it more than cosmetic: the Read-back for `quoted-constraint-breach` only checks that the quote is byte-present in the Constraints (qa:61). It does not weigh the reading. A Task 2 reviewer who reads TL:21 literally can raise a confirmed blocker. So can the managed FINAL, which returns `issues` when "a plan `## Constraints` item is violated" (qa:310). The fixer then cannot meet TL:52 and the literal TL:21 together.
- Why it is still not blocking under the test I proposed (R1-A:68; section 5, A-003): a compliant path exists, and it is the reading the plan's own text points to four times. The executor is not forced to breach anything. A halt needs a reviewer to adopt a reading the plan contradicts.
- Why the consequence is lighter than Task 7's: Task 2 does not move HEAD, so a failed A2 reaches the adviser, whose `dispute` outcome covers "the AC is contradictory or infeasible" (retry:72). That stops the run for a Ruling (retry:107) before any commit or install has happened. On Task 7 the ladder is off (retry:41, :44).
- One-line fix, which must be made before the run because the plan is hash-pinned once the first task starts (SKILL:40): scope TL:21 as SRC:59 does ("for the worker-session duties ... it points to the dispatch preamble"), and add to TL:52 "copied verbatim from SRC:86, including its `worker_done` text".

##### 3. Ruling on B's "0 blocking" claim for Task 7

**No order of Task 7's steps meets every instruction and every AC.** These are the instructions, all in TL:110 unless noted:

- (i) On approval, stage and commit with `git commit --only -- <paths>`.
- (ii) "**Then** ask the owner to approve `uv run superclaude install --force` ...; on approval, run it."
- (iii) "Make the commit the last action of the task."
- (iv) TL:113: `t7-approvals.md` records "both questions, the owner's answers verbatim, **the commit ID** and the install output".
- (v) TL:25 (Constraints): commits need the owner's approval at the moment of action.

| Order | What breaks |
|---|---|
| A. As written: commit, then install, then write `t7-approvals.md` | (iii): the install and the file write both come after the commit. |
| B. Install first, then commit last, writing the file before the commit | (iv): the file cannot hold the ID of a commit that does not exist yet. (ii): the install comes before the commit, against "Then". |
| C. Install, commit, then write the file with the ID (B's reading, R1-B:30) | (iii): the file write is an action after the commit. (ii): "Then". |
| D. Commit, install, write the file, then commit again so a commit is last | (v): the second commit was never approved by the owner. And it is not "the commit" of (iii). |

The core is self-referential. No file can hold the ID of a commit and also be written before that commit. So (iii) and (iv) cannot both hold under any reading in which writing the evidence file counts as an action. B's 0-blocking result needs two loosenings that the plan never invites: "action" must exclude a file write, and "Then" in (ii) must be read as "after the commit approval" rather than "after the commit".

**Why this is blocking under the executor's rules, and why B's test is too narrow.** B's test counts only (a) an AC that cannot pass or (b) an unguarded irreversible effect (R1-B:65). The executor has four co-equal blocking triggers, and one of them is a breach of "an explicit task instruction" that the reviewer can quote (qa:52; also qa:17). "Make the commit the last action of the task" is such an instruction. Its quote passes the Read-back (qa:61). The evidence file that TL:113 requires proves the breach by itself: the commit ID in it shows it was written after the commit. So following the plan as written hands an attentive reviewer a confirmable B4 blocker that no fix pass can close. After the commit, a failed A2 halts `head-moved` with no adviser (retry:41, :44). The run therefore ends in `E-HALT-QA` on the task that has already committed and overwritten `~/.claude/CLAUDE.md` (TL:25). That is the plan not being ready to run, even though the halt itself is safe.

**What I concede to B.** TL:113 on its own can pass (C's calibrator, C:285, and R1-C:49 agree). The halt causes no damage. A Ruling can clear it. My blocking call rests on instruction conflict plus the stage at which the halt arrives, not on harm.

**Merged fix.** Rewrite TL:110 in one order: ask both approvals; run the install; write `t7-approvals.md` without the ID; stage the listed P0 paths plus `.dev/tasks`; commit as the last product action, naming `.dev/tasks` in the `--only` pathspec (U-008); then append the commit ID to `t7-approvals.md` and stage it, and say explicitly that this record step follows the commit. Add one line: a QA failure after the commit, or an owner refusal, ends the task in a halt for the person's Ruling and is never retried. Class: drift for the wording. The commit itself is a necessary deviation (SRC:282).

##### 4. Updated assessment of the other variants and new evidence

**Variant B.** R2-1 is the right gap with the wrong grade, as B now admits (R1-B:40-41). Two problems remain in Round 1. First, B's "0 blocking" test drops the executor's B4 trigger (section 3). Second, B keeps "record the clause as vacuous" as a fallback (R1-B:17), which SRC:291 rules out. B's staging point (A-008) and its R2-5 phrase list are sound and belong in the merge.

**Variant C.** C is the strongest card on internal consistency. Its two new Round 1 points both hold up:
- R3-F3 is real, though over-graded (section 2).
- A-005 is better than my own Round 1 answer. qa:288 closes the list of interrupts ("No other path may stop automation or prompt the user"), so TL:110's "stop this task and report" is not an executor outcome. If the commit is refused, TL:113 is unmet, which gives a B1 blocker. The ladder can then run and ask the owner again, or the adviser disputes. If the commit is made and the install is refused, the task halts `head-moved`. This strengthens the Task 7 finding.

C's R3-F9 "four texts" remains wrong, and C conceded it (R1-C:50).

**New evidence this round:**
1. SRC:86's guard line contains `worker_done --outcome failed`, and TL:52 requires it verbatim. That is the one unavoidable point of the R3-F3 conflict.
2. SRC:59 explicitly places "the template's guard line" in the contract file. So the spec is consistent, and the plan's TL:21 is the sentence that widened the rule.
3. TL:54 already anticipates Orca commands in the file, which supports the scoped reading.
4. The adviser's dispute route exists for Task 2 (retry:72, :107) but is skipped for Task 7, where a head-moved halt comes first with no adviser (retry:44). The same kind of defect therefore has different consequences on the two tasks.
5. The self-referential commit ID (section 3) makes the Task 7 conflict a logical one, not only a matter of wording.

##### 5. Shared assumptions

- **A-002 (the executor follows Depends-on edges): REJECT. Unchanged.** SKILL:79, SKILL:97, and nothing in the plan is marked `independent`.
- **A-003 (one undefined "blocking" means FAIL): QUALIFY. Sharpened.** A plan finding is blocking when following the plan as written, in source order under `/sc:implement`, leaves the executor no compliant choice. That is the case when every reading of the plan's own words forces either an unmet AC (B1) or a breach of a Constraint or explicit task instruction (B4), the executor's own blocking triggers (qa:41, :49, :52), or leaves a P0 pass condition with no task that performs it (SRC:241). When a compliant reading exists and the plan's own text points to it, the finding is should-fix, even if a literal-minded reviewer could still confirm a blocker. One blocking finding means FAIL. Result: Task 7 is blocking. R3-F3, C-002, F1/R3-F5, F2 and U-008 are should-fix.
- **A-005 (the run is attended): QUALIFY. Changed in substance, adopting C's point.** Attendance is needed, and a person-opened implement session is the coordinator TL:122 asks for (SKILL:118). But a refusal does not produce the clean "stop and report" that TL:110 promises. Under qa:288 it becomes a B1 blocker on TL:113, which leads to a retry or dispute, or to `head-moved` after the commit. Fix: add one Constraint line saying the run must be attended and never headless. Task 7 should record a refusal in `t7-approvals.md` and expect a halt for a Ruling, not a retry. Folded into the Task 7 finding.
- **A-007 (the spec is a consistent authority): REJECT the assumption. Unchanged,** with one boundary. SRC:60 against SRC:306 (three exact texts against "four") and the stale SRC:59 range are spec defects the plan inherits. R3-F3 is not one of them: there the spec is consistent (SRC:59), and the plan's TL:21 caused the conflict.
- **A-008 (post-commit artifacts need no staging): QUALIFY. Slightly changed.** The executor already applies the always-staged rule (mw:36), and staging is not committing (TL:22). So artifacts left uncommitted after Task 7 are expected. I now accept B's and C's fix as one closing line in the phase-report task (`git add .dev/tasks` after Tasks 8 and 9, recorded), graded minor, not a separate should-fix. U-008 (`--only` must name `.dev/tasks`) stays should-fix inside the Task 7 finding.

##### 6. Contested points

| Point | Current preferred variant or merged position | Confidence |
|---|---|---|
| S-006 / A-003 (blocking count) | Merged: exactly 1 blocking finding (Task 7). Against B's 0, because B's test drops the executor's B4 trigger (qa:52). Against C's 2, because R3-F3 has a compliant reading that the plan points to. | 0.80 |
| X-005 / U-002 / U-006 (Task 7) | A + C merged, **blocking**, drift for the wording and necessary for the commit. The fix is the reordered TL:110 in section 3, plus U-008 and the refusal line. | 0.85 |
| U-007 / R3-F3 (verb syntax) | C's finding, graded **should-fix (top)**, drift. The only unavoidable point is the guard line (SRC:86, TL:52). Fix: scope TL:21 as SRC:59 does. | 0.75 |
| C-002 / X-002 / X-003 (cadence run) | Should-fix (top), with C's wording. Require a run longer than the cadence outside Agent-tool calls; no "vacuous" fallback (concession to C). | 0.85 |
| C-001 / X-001 (Task 3 dependency) | B and C: minor, drift. The residual is R3-F5. | 0.90 |
| X-004 (number of exact refusal texts) | A: three exact texts plus the case-3 prefix, and a spec erratum note. | 0.90 |
| X-006 (classes) | Task 3: drift. AC-0.9: drift. Stale cite: none. Task 7: drift for the wording, necessary for the commit. R3-F3: drift. | 0.80 |
| A-005 | QUALIFY, adopting C's refusal-path point (qa:288). Folded into Task 7. | 0.75 |
| A-008 | QUALIFY. One closing staging line in the phase-report task, minor. | 0.70 |
| A-002 / A-007 | REJECT the assumption in both cases. Unchanged. | 0.90 |

### Variant B Rebuttal
#### Round 2 Rebuttal: Variant B (reviewer 2, qa)

Cite keys as in earlier rounds: `A:N`, `B:N`, `C:N` = card line; `TL:N` = plan line; `SRC:N` = `source.md` line; `qa:N`, `retry:N`, `SKILL:N` = the installed `~/.claude/skills/sc-implement-protocol/` files (`refs/qa.md`, `refs/retry.md`, `SKILL.md`); `R1-A:N`, `R1-B:N`, `R1-C:N`, `R2-A:N` = debate statement lines. Every TL, SRC and executor line below was opened for this statement.

##### Position summary

I move from 0 blocking to **1 blocking: Task 7**. A is right that my Round 1 test was narrower than the executor's own. The executor treats a breach of an explicit task instruction (B4) as blocking on the same footing as an unmet AC (qa:41, and the B4 row at qa:52). Task 7's body order and its "commit last" sentence cannot both be followed, whatever the executor does. I do not move on R3-F3: it is a real conflict, but the plan gives a compliant reading and points to it, so it is should-fix, at the top of the list with the cadence run. I accept A's narrower reading of R3-F3: the guard line is the only text that cannot be paraphrased. I also withdraw my "record the heartbeat clause as vacuous" fallback.

One correction to A's Task 7 argument: the commit-ID problem on its own would not make Task 7 blocking, because TL:113 itself points to writing the record after the commit. The clash that cannot be removed is between "Then ask ... run it" (the install after the commit) and "Make the commit the last action". Both the install and the commit are actions under any reading.

##### 1. Responses to criticisms of Variant B

| Criticism (source) | Response |
|---|---|
| X-003: B grades R2-2 minor because TL:122 delegates step 5, then grades R2-1 blocking although it sits in the same delegated step (R1-A:31, R1-C:41, diff X-003) | **Conceded, as in Round 1 (R1-B:40).** Both clauses are in SRC:291, and the same TL:122 sentence ("steps 1-3 and 5-7") brings both in. Under the merged test in section 5 both are should-fix. R2-1 ranks above R2-2 because it applies on every run, while R2-2 applies only if AC-0.6 answers no. That is a difference in priority, not in grade. |
| R2-1 is "unsatisfiable after the fact" (B:22-23; R1-A:13) | **Conceded.** SRC:291 asks for one checked run longer than the cadence. Another run can be added within the phase. |
| B's Tier-2 troubleshoot suggestion would not count (R1-A:32, R1-C:17) | **Conceded.** SRC:291 excludes time "while the session is inside an Agent-tool call", and Tier 2 is Agent-tool fan-out. The fix must ask for a run whose top-level session, outside Agent-tool calls, lasts longer than the cadence. |
| B's "or record the clause as vacuous and flag it" fallback is ruled out by SRC:291 (R1-C:17, R2-A:20, R2-A:73) | **Conceded now.** I kept this fallback in Round 1 (R1-B:17). That was wrong. SRC:291 reads "A run shorter than the cadence passes the heartbeat part vacuously, **so** each phase report names at least one checked run that lasted longer than the cadence." The duty exists to stop a vacuous pass. I adopt A's merged wording (R2-A:20): Task 8's AC requires at least one such run; if none is achieved, the report records the duty as unmet and P0 does not pass. |
| R2-4's dependency half and U-005 rest on a dependency-driven executor (R1-A:33, R1-C:42) | **Conceded, as in Round 1 (R1-B:43).** SKILL:79 ignores `depends-on`; SKILL:97 runs unmarked tasks in source order. What remains of R2-4 is the phase-end re-run of AC-C1 and AC-C2 (SRC:241). |
| R2-3 cites TL:17 for text at TL:20 (R1-A:34, R1-C:44) | **Conceded.** Cite error only; the finding stands. |
| B omits whole areas: negative-check targets, AC-0.9 class, Task 7 mechanics, `--report-dir` (R1-C:43) | **Conceded, as in Round 1 (R1-B:45).** B's coverage was the narrowest of the three cards. |
| B's 0-blocking test drops the executor's B4 trigger (R2-A:65, R2-A:73) | **Conceded.** My Round 1 test counted only (a) an AC that cannot pass and (b) an unguarded irreversible effect (R1-B:65). The executor's severity model has four co-equal blocking answers. `quoted-constraint-breach` is "yes" when the diff breaks "a parent `## Constraints` ... item or an explicit task instruction" and the reviewer can quote that text (qa:52). Its Read-back only checks that the quote is byte-present (qa:61). A plan that forces the executor to break a quotable task instruction hands any attentive reviewer a confirmed blocker. I adopt A's test and keep my irreversible-effect clause as one more trigger (section 5). |
| B's "0 blocking" needed two loosenings the plan never invites (R2-A:63) | **Half conceded.** See section 2. The "Then" loosening cannot be supported, and that alone makes Task 7 blocking. The other loosening, that writing the record file after the commit is not "an action", is invited by the plan's own AC (TL:113), so I do not accept that half of A's argument. |

What I keep from Round 1, which A and C did not dispute: R2-5's phrase list for the ID-only rules (R2-A:73 accepts it), R2-3 as the smallest correct AC-C5 fix, R2-6 class `none` (C conceded, R1-C:52), the L3 staging point behind A-008 (R2-A:94 now accepts the fix), and the phase-end re-run half of R2-4.

##### 2. Ruling on A's Task 7 argument

I opened TL:106-116. The instructions in TL:110 and the AC at TL:113:

- (i) Ask approval 1; "on approval, stage ... and commit with `git commit --only -- <paths>`".
- (ii) "**Then** ask the owner to approve `uv run superclaude install --force` ...; on approval, run it."
- (iii) "If either approval is refused, stop this task and report that the live checks cannot run."
- (iv) "Make the commit the last action of the task."
- (v) TL:113: `t7-approvals.md` records "both questions, the owner's answers verbatim, the commit ID and the install output".

**Does any order meet every instruction and AC? No.**

The clash that no reading removes is (ii) against (iv). The body puts the commit at approval 1 and the install after it ("Then ... run it"). The last sentence puts the commit after everything. The install and the commit are both actions under any meaning of the word. So either the install comes after the commit, which breaks (iv), or the commit comes after the install, which breaks the order that (i) and (ii) set. My Round 1 reading (R1-B:30, :56) needed "Then" to mean "after asking approval 1", not "after the commit". The sentence puts "Then" directly after the commit clause, so that reading is strained. A reviewer can quote either sentence against either order, and the quote passes the Read-back (qa:61).

The commit-ID clash, (iv) against (v), is weaker than A says (R2-A:63). It is true that no file can hold the ID of a commit and also be written before it. But TL:113 is the plan's own AC, and it can only be met by writing the record after the commit. So the plan itself points to the reading "the commit is the last *product* action; the record is written after it". Under A's own should-fix rule ("a compliant reading exists and the plan's own text points to it", R2-A:91), this half alone would be should-fix. It does not change the verdict, because the (ii)/(iv) clash stands without it.

**Do I concede it is blocking under the executor's real QA rules? Yes.**
- A B4 answer is a blocking trigger, the same as B1 (qa:41, qa:52).
- Following Task 7 as written forces a breach of a quotable explicit task instruction, so no executor choice is compliant.
- The consequence lands at the worst point. Task 7's commit moves HEAD. When A2 fails and HEAD has moved, the executor writes `halt review=2 reason=head-moved` and stops, and "no adviser is spawned" (retry:41, retry:44). So the adviser's `dispute` route (retry:72, retry:107) is not available. The run halts for a person's Ruling after the owner-approved commit, and possibly after the `--force` overwrite of `~/.claude/CLAUDE.md` (TL:25).
- A and C are also right that (iii) is not an executor outcome. The closed interrupt list ends "No other path may stop automation or prompt the user" (qa:288). A refusal becomes an unmet TL:113 (B1), not a clean stop.

My Round 1 point still holds as a limit on harm, not on grade: the halt damages nothing, and a Ruling can clear it. But a plan that is certain to hand its executor a confirmable blocker on the irreversible task is not ready to run.

**Merged fix (A's order, with one addition from me).** Rewrite TL:110 as one order: ask both approvals up front, stating the `--force` effect; run the install; write `t7-approvals.md` without the ID; stage the listed P0 paths plus `.dev/tasks`; commit with `--only`, naming `.dev/tasks` in the pathspec (U-008); then append the commit ID to `t7-approvals.md` and stage it, and say in the task text that this record step follows the commit on purpose. Replace (iii) with: a refusal is recorded in `t7-approvals.md`, and the task ends in a halt for the person's Ruling, never a retry. Add: a QA failure after the commit is never retried. My addition: list the P0 paths in the task text (the Task 1-6 outputs, `install_core.py`, any plugin copies), so the `--only` pathspec can be checked. Class: drift for the wording; the commit itself is a necessary deviation (SRC:282).

##### 3. Ruling on C's R3-F3 and A's narrower reading

**The text.** TL:21 says the contract file, "for Orca verb syntax and heartbeat cadence ... points to the dispatch preamble instead of copying them (section 2.1, "Contract file")". TL:42 bans verb syntax "copied from Orca's guides". TL:52 requires "the exact guard line text from section 2.3 'Brief layout'". The guard line (SRC:86) contains "send worker_done --outcome failed with a body starting "guard refused:"". SRC:59 limits the never-copy rule to "the worker-session duties (WC-3, WC-5, WC-7, WC-12, WC-13 and heartbeats)", and the same sentence puts "the template's guard line" in the file. TL:54 expects Orca commands in the file "as the coordinator's and worker session's channel".

**A's narrower reading is correct.** In Round 1 I called R3-F3 "overstated" and minor (R1-B:32). I was right that TL:42's qualifier protects text taken from the spec. I missed that TL:21 has no such qualifier and is a Constraints item, which every review and the managed FINAL check (qa:16, qa:310). Most of the syntax C lists can be paraphrased, because no AC asks for it word for word (SRC:74, SRC:84, SRC:88). The guard line cannot be paraphrased, because TL:52 demands it exactly. So a literal reading of TL:21 makes TL:21 and TL:52 impossible to meet together.

**Grade: should-fix, top tier. Not blocking.** Three reasons:
1. A compliant reading exists, and the plan points to it four times: TL:21 cites SRC:59, which is scoped to worker-session duties and includes the guard line; TL:38 scopes "pointing to the dispatch preamble" to those duties; TL:42 limits the ban to text "copied from Orca's guides"; TL:54 expects Orca commands in the file. A careful reviewer answers B4 "no". This is the opposite of Task 7, where the plan's own sentences point to two incompatible orders.
2. If a literal reviewer does confirm it at Task 2, HEAD has not moved. The ladder runs, and the adviser can return `dispute` because "the AC is contradictory or infeasible" (retry:72). That stops the run for a Ruling before any commit or install (retry:107).
3. The one late risk is C's: the managed FINAL is never waived, and it returns `issues` when "a plan `## Constraints` item is violated" (qa:310; SKILL:160). A literal FINAL could block the archive after the live runs. That is why R3-F3 must be fixed before the run, because the plan is hash-pinned once the first task starts (SKILL:40). It is not a reason to grade it blocking, because the FINAL applies the same severity test (qa:294) and needs the same contradicted reading.

New supporting point: the guard line is text that Task 2 adds, so it is task-owned, and "a blocker on task-owned text is never capped" (qa:186). The inherited cap (qa:41, qa:166) gives no protection here. That is one more reason to fix it before the run.

Fix (A's, which I accept): scope TL:21 as SRC:59 does ("for the worker-session duties ... it points to the dispatch preamble"), and add to TL:52 "copied verbatim from SRC:86, including its `worker_done` text". Class: drift. The spec is consistent here; the plan's TL:21 widened the rule.

##### 4. Updated assessment and new evidence

**Blocking set: 1 (Task 7).** Not 0, because my Round 1 test dropped B4 (section 1). Not 2, because R3-F3 has a compliant reading that the plan points to (section 3).

**Top should-fix items, to be applied before the run because of the hash pin (SKILL:40):**
1. Cadence run (R2-1 / R3-F2 / F4a): C's wording, outside Agent-tool calls, no vacuous fallback; if no such run is achieved, P0 does not pass.
2. R3-F3: scope TL:21 and pin the guard line to SRC:86.
3. U-008 and the refusal line, folded into the Task 7 fix.
4. X-004: three exact refusal texts plus the case-3 prefix (A's F2), with a spec erratum note.

**Minor items B still owns:** R2-2 (carry the fallback into Task 8's step 5), R2-3 (record AC-C5 as run with an empty edit set), the phase-end half of R2-4 (re-run AC-C1, AC-C2 and the AC-C3 comparison at phase end; C's R3-F8 scratch-skill risk makes this more needed), R2-5 (name the load-bearing phrases for WC-3, WC-5, WC-7 and WC-9), R2-6 (stale cite, class none).

**New evidence this round:**
1. TL:113 can only be met by a record written after the commit. So the plan itself invites the "the record step is not an action" reading. Task 7's blocking basis is the install-versus-commit order clash in TL:110, not the self-referential commit ID.
2. qa:186: task-owned text is never capped. The guard line Task 2 adds gets no inherited-cap protection, either at Task 2's review or at the FINAL.
3. qa:274-276: the closed interrupt list sits in the QA chapter and covers finding-driven stops ("The only non-finding interrupts are the STOP rows"). Read strictly, "No other path may stop automation or prompt the user" (qa:288) would also cover Task 7's own approval questions. I read it as covering halts, not task actions that the spec requires (SRC:282). The text does not say so explicitly, which is one more reason for an explicit attended-run Constraint line (A-005).
4. retry:44 confirms the asymmetry A states: on Task 7 the ladder-off halt comes before any adviser, so the `dispute` route (retry:72) exists for Task 2 but not for Task 7.

##### 5. Shared assumptions

- **A-002 (the executor follows Depends-on edges): REJECT. Unchanged.** SKILL:79 and SKILL:97; nothing in the plan is marked `independent`.
- **A-003 (one undefined "blocking" means FAIL): QUALIFY. Changed.** I adopt A's sharpened test (R2-A:91), with one clause added from my Round 1 test. A plan finding is blocking when following the plan as written, in source order under `/sc:implement`, leaves no compliant choice. That is the case when every reading the plan's own text supports forces (a) an unmet AC (B1), (b) a breach of a Constraint or explicit task instruction (B4, qa:52), (c) an irreversible or outward effect with no guard, or (d) a P0 pass condition that no task performs (SRC:241). When a compliant reading exists and the plan's text points to it, the finding is should-fix. One blocking finding means FAIL. Result: Task 7 is blocking; R3-F3, the cadence run, F1/R3-F5, F2 and U-008 are should-fix.
- **A-005 (the run is attended): QUALIFY. Changed in substance, adopting C's point.** The approvals need a person present (TL:25, TL:110). TL:110's "stop this task and report" is not an executor outcome (qa:288). Fix: one Constraint line saying the run must be attended and never headless, plus the Task 7 refusal line from section 2. Folded into the Task 7 finding.
- **A-007 (the spec is a consistent authority): REJECT the assumption. Unchanged,** with A's boundary. SRC:60 against SRC:306 (three exact texts against "four") and the stale SRC:59 range are spec defects the plan inherits. R3-F3 is not one of them: SRC:59 is consistent, and TL:21 caused the conflict.
- **A-008 (post-commit artifacts need no staging): QUALIFY. Unchanged.** The executor already stages `.dev/tasks` as a package rule, and staging is not committing (TL:22). Add one closing `git add .dev/tasks` line, recorded, after Tasks 8 and 9 (SRC:396, L3). Minor. U-008 stays inside the Task 7 finding.

##### 6. Contested points

| Point | Current preferred variant or merged position | Confidence |
|---|---|---|
| S-006 / A-003 (blocking count) | Merged: exactly 1 blocking finding (Task 7), under A's test plus my irreversible-effect clause. B's Round 1 count of 0 is withdrawn. | 0.85 |
| X-005 / U-002 / U-006 (Task 7) | A + C merged, **blocking**. Basis: the install-versus-commit order clash in TL:110 (B4, qa:52), plus the `head-moved` halt with no adviser (retry:41, :44). The commit-ID point alone is should-fix, since TL:113 invites it. Fix: A's reordered TL:110, U-008, the refusal line and an explicit path list. | 0.85 |
| U-007 / R3-F3 (verb syntax) | C's finding with A's narrower reading. **Should-fix (top)**, drift. The only unavoidable point is the guard line (SRC:86, TL:52). Fix: scope TL:21 as SRC:59 does. | 0.80 |
| C-002 / X-002 / X-003 (cadence run) | Should-fix (top), C's wording: a run longer than the cadence outside Agent-tool calls; no vacuous fallback (my concession). | 0.90 |
| C-003 (AC-0.6 fallback) | Minor, drift (all agree). | 0.90 |
| C-004 (phase-end checks) | Merged: one closing phase-report task (A's F7 / C's R3-F11) that re-runs AC-C1, AC-C2 and the AC-C3 comparison, records AC-C5 as vacuous (R2-3), and ends with `git add .dev/tasks` (A-008). Minor. | 0.80 |
| C-007 (rule substance in the test) | B's R2-5 phrase list, with A's three-texts correction in place of C's "four". Minor. | 0.80 |
| C-001 / X-001 (Task 3 dependency) | B and C: minor, drift; the residual is R3-F5. | 0.90 |
| X-004 (number of exact refusal texts) | A: three exact texts plus the case-3 prefix, and a spec erratum note. | 0.90 |
| X-006 (classes) | Task 3: drift. AC-0.9: drift. Stale cite: none. Task 7: drift for the wording, necessary for the commit. R3-F3: drift. | 0.80 |
| A-005 | QUALIFY, adopting C's qa:288 point: an attended-run Constraint line plus the Task 7 refusal line. | 0.75 |
| A-008 | QUALIFY. One closing staging line, minor. | 0.75 |
| A-002 / A-007 | REJECT the assumption in both cases. | 0.90 |

### Variant C Rebuttal
#### Round 2 Rebuttal: Variant C (reviewer 3, refactorer)

Cite keys as in earlier rounds: `A:N`, `B:N`, `C:N` = card line; `TL:N` = plan line; `SRC:N` = `source.md` line; `qa:N`, `retry:N`, `mw:N`, `SKILL:N` = the installed `~/.claude/skills/sc-implement-protocol/` files (`refs/qa.md`, `refs/retry.md`, `refs/managed-workspace.md`, `SKILL.md`); `R1-A:N`, `R1-B:N`, `R1-C:N`, `R2-A:N`, `R2-B:N` = debate statement lines. Every TL, SRC and executor line below was opened for this statement (TL:14-116, SRC:55-90, SRC:289-292, SRC:394-397, qa:10-65, qa:186, qa:240-256, qa:284-310, retry:38-46, retry:72, retry:107, mw:34-38, SKILL:40, :79, :97, :160).

##### Position summary

The verdict stays FAIL with **exactly one blocking finding: Task 7**. I **concede R3-F3 to should-fix**, top tier. My Round 1 case for raising it (R1-C:23, :69) rested on TL:21 being file-wide. Testing A's narrower reading against the literal text, TL:21 itself, not only its cite, supports a compliant reading: its first clause orders the file to restate spec text, and its "instead of copying them" names the dispatch preamble as the thing not copied. The guard line comes from the spec, not the preamble. Under the blocking test all three advocates now share (a finding is blocking only when no reading the plan's text supports is compliant), R3-F3 does not qualify. I confirm the Task 7 consensus and adopt B's correction of its basis: the irreducible clash is "Then ... run it" against "Make the commit the last action" (TL:110), with the commit-ID point as supporting evidence only.

##### 1. Responses to criticisms of Variant C

| Criticism (source) | Response |
|---|---|
| R3-F3 is over-graded; a compliant reading exists that the plan points to four times (R2-A:36, :42; R2-B:60) | **Conceded.** See section 2. I add a fifth pointer the others did not use: TL:21's own wording. |
| R3-F3's list of Orca syntax is too broad; only the guard line cannot be paraphrased (R2-A:34-35; R2-B:57) | **Conceded.** `task-create --spec`, `--retry-of` (SRC:74), `worker-start --worktree new-child --base-branch` (SRC:84) and `orca worktree rm` (SRC:88) have no verbatim AC; Task 2 asks for the rules "in full" (TL:49), not the words. Only TL:52's "exact guard line text" pins `send worker_done --outcome failed` (SRC:86). One addition: the pin is double, because Task 5's test must assert that the template "carries the guard line" (TL:87), so the verbatim text is also fixed by a test. |
| R3-F1's "the acceptance criterion cannot pass" is overstated (C:285; R2-B:41) | **Conceded in Round 1 (R1-C:49), and I now go further with B.** TL:113 itself can only be met by a record written after the commit, so it invites the reading that the record step is not "the last action". The commit-ID point alone would be should-fix. The blocking basis is the install-versus-commit order (section 3). |
| R3-F9 "four `guard refused:` texts" is wrong (R2-A:79) | **Conceded in Round 1 (R1-C:50).** SRC:60 gives three exact texts (case 1, case 2, copies-disagree) and case 3 has no text. Merge A's three-plus-prefix wording, with B's R2-5 phrase list. |
| R3-F2 blocking was wrong (C:285) | **Conceded in Round 1 (R1-C:48).** Should-fix, top tier, with no "vacuous" fallback (now agreed by A, R2-A:20, and B, R2-B:18). |
| R3-F4's dependency half, R3-F6 class, R3-F12 class | **Conceded in Round 1 (R1-C:51-53).** R3-F4 keeps only the path list and the `--only` pathspec point (U-008). R3-F6 is drift. R3-F12 is class none. |
| A-008 graded should-fix by C (R1-C:81); A and B grade it minor (R2-A:94; R2-B:92) | **Conceded to minor.** mw:36 binds the executor itself to "`.dev/tasks/` is always staged", and staging is not committing (TL:22). The gap is only that no AC records the final `git add` after Tasks 8 and 9, so it is a minor recording gap, folded into the closing phase-report task. |

##### 2. R3-F3 tested against the literal text: conceded to should-fix

**The lines.**
- TL:21 (Constraints): "`WORKER-CONTRACT.md` restates only what `./source.md` sections 2.1, 2.2 and 2.3 already say; it adds no rule the spec lacks, and for Orca verb syntax and heartbeat cadence it points to the dispatch preamble instead of copying them (section 2.1, "Contract file")."
- TL:42 (Task 1 AC): "no `orca orchestration` verb syntax copied from Orca's guides and no fixed heartbeat cadence; it points to the dispatch preamble for both."
- TL:49 (Task 2): section 2.3 "in full", including "the brief layout with the exact guard line"; a brief template "that carries the guard line".
- TL:52 (Task 2 AC): "including the exact guard line text from section 2.3 'Brief layout'".
- TL:54 (Task 2 AC): "The file mentions Orca commands only as the coordinator's and worker session's channel".
- SRC:59: the no-copy rule is scoped "For the worker-session duties (WC-3, WC-5, WC-7, WC-12, WC-13 and heartbeats)", and the file holds "WC-6 and section 2.3, including its brief template and the template's guard line".
- SRC:86: the guard line ends "send worker_done --outcome failed with a body starting "guard refused:"."

**Testing A's narrower reading.**
1. TL:42 is not breached by the guard line. Its qualifier "copied from Orca's guides" excludes spec text. Agreed with A and B.
2. TL:21 has no such qualifier, which was my Round 1 point (R1-C:23). But reading the sentence literally, end to end, it does not ban spec-sourced syntax either. Its first clause *requires* the file to restate what sections 2.1-2.3 say, and SRC:86 is section 2.3 text. Its second clause says the file "points to the dispatch preamble instead of copying them": the thing not copied is the preamble's own syntax. The guard line is not copied from the preamble. So the compliant reading sits in TL:21's own words, not only in its cite to SRC:59. That is a fifth pointer, beside the four A and B list (TL:21's cite, TL:38, TL:42, TL:54).
3. A literal-minded reviewer can still quote "for Orca verb syntax ... it points to the dispatch preamble instead of copying them" against a file that contains `worker_done --outcome failed`. The B4 Read-back only checks that the quote is byte-present (qa:61), and severity is derived mechanically from the reviewer's yes/no answer (qa:37, :56). So the risk is real. But it needs the reviewer to read "copying" as "containing", against the sentence's own first clause.

**Why that is should-fix under the shared test.** The test all three advocates now use (R2-A:91, R2-B:89, and my R1-C:75) makes a finding blocking only when every reading the plan's text supports forces a breach. Here a supported compliant reading exists, and it is the more natural one. Task 7 is different: no reading of TL:110 lets both the install-after-commit order and "commit last" hold.

**What I keep from Round 1.** The late risk is real and is the reason to fix before the run, not to grade higher. A blocker on task-owned text is never capped (qa:186), and the managed FINAL is never waived (SKILL:160) and returns `issues` when "a plan `## Constraints` item is violated" (qa:310). If a literal FINAL confirms it, the archive stops with `E-ARCHIVE-BLOCKED` (qa:286) after the commit, the install and the live runs. The plan is hash-pinned once Task 1 starts (SKILL:40), so the fix cannot be made mid-run.

**Correction to A's and B's mitigation.** Both say that at Task 2 the adviser's `dispute` route "stops the run for a Ruling before any commit or install" (R2-A:43, R2-B:61). That is right, but it is still a stop: a `dispute` naming the AC appends `halt reason=dispute` and STOPs `E-HALT-QA` (retry:72, :107). It is a safer stop than Task 7's, not a non-event. This does not change the grade.

**Fix (A's, accepted).** Scope TL:21 as SRC:59 does ("for the worker-session duties (WC-3, WC-5, WC-7, WC-12, WC-13 and heartbeats) it points to the dispatch preamble for Orca verb syntax and cadence instead of copying them"), and add to TL:52 "copied verbatim from `./source.md` section 2.3 'Brief layout', including its `worker_done` text". Class: drift; the spec is consistent here and TL:21 widened it.

##### 3. Task 7: blocking consensus confirmed, merged form

**Confirmed: blocking.** I opened TL:106-116 again. TL:110 orders: approval 1, then "stage ... and commit with `git commit --only -- <paths>`"; "Then ask the owner to approve `uv run superclaude install --force` ...; on approval, run it"; "If either approval is refused, stop this task and report"; "Make the commit the last action of the task." Both the install and the commit are actions under any reading, so "Then ... run it" and "commit last" cannot both hold. A reviewer can quote either sentence against either order and pass the B4 Read-back (qa:52, :61). Under qa:41 a confirmed B4 is blocking.

**On the basis, I side with B (R2-B:9, :41).** The commit-ID point (TL:113) is supporting, not the core, because TL:113 can only be met by a record written after the commit, which invites "the commit is the last product action". The install-versus-commit order is the clash no reading removes. My Round 1 wording (R1-C:25) led with the commit ID; I move the weight to the order clash.

**Consequence, verified.** The commit moves HEAD inside Task 7's window. When A2 fails, ladder check 3 fails ("HEAD has not moved", retry:41), the executor appends `halt review=2 reason=head-moved` and STOPs `E-HALT-QA`, and "no adviser is spawned" (retry:44). So the `dispute` route (retry:72) is closed on this task. The halt lands after the owner-approved commit and possibly after the `--force` overwrite of `~/.claude/CLAUDE.md` (TL:25). The refusal sentence is not an executor outcome either: "No other path may stop automation or prompt the user" (qa:288).

**Merged form (A F3 + C R3-F1, with B's additions).** Rewrite TL:110 in one order:
1. Ask both approvals up front, stating the `--force` effect.
2. Run the install.
3. Write `t7-approvals.md` with both questions, the answers verbatim and the install output.
4. Stage the listed P0 paths plus `.dev/tasks` (never `.claude/` mirrors), check AC-C4, then commit with `git commit --only -- <paths> .dev/tasks`, so `.dev/tasks` is named in the pathspec (U-008, R3-F4). This is the last product action.
5. Append the commit ID to `t7-approvals.md` and stage it; say in the task that this record step follows the commit on purpose.
6. List the P0 paths in the task text (R3-F4 and B's addition): `src/superclaude/core/WORKER-CONTRACT.md`, `src/superclaude/cli/install_core.py`, `src/superclaude/core/HOW-WE-WORK.md`, `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`, `tests/skills/test_worker_contract.py`, any plugin copy Task 3 adds, and `.dev/tasks`.
7. Replace "stop this task and report" with: a refusal is recorded in `t7-approvals.md` and the task ends in a halt for the person's Ruling; a QA failure after the commit is never retried.

Class: drift for the wording; the commit itself is a necessary deviation (SRC:282).

##### 4. Updated assessment and new evidence

**Blocking set: 1 (Task 7).** My Round 1 count of 2 (R1-C:75, "and, as a candidate, R3-F3") is withdrawn.

**Top should-fix items, all to be applied before the run because of the hash pin (SKILL:40):**
1. Cadence run (R3-F2 / R2-1 / F4a): Task 8's AC requires at least one checked run whose top-level session, outside Agent-tool calls, lasts longer than the preamble cadence, with start and end times; if none is achieved, P0 does not pass. SRC:291 forbids the vacuous fallback.
2. R3-F3: scope TL:21 and pin the guard line to SRC:86 (section 2).
3. X-004: three exact refusal texts plus the case-3 prefix, with a spec erratum note (A's F2).

**Minor items C still owns, unchanged:** R3-F5 (red `tests/cli` window between Task 1 and Task 3), R3-F6 (Task 4 runs too few test files), R3-F7 (stale phase-state line in HOW-WE-WORK.md), R3-F8 (unsafe negative checks), R3-F10 (`--report-dir` in the P0 template), R3-F11 (closing phase-report task, now also carrying B's AC-C5 record and the final `git add .dev/tasks`), R3-F13 (`gh api` post patterns), R3-F14 (AC-0.6 fallback).

**New evidence this round:**
1. TL:21's own first clause ("restates only what ... sections 2.1, 2.2 and 2.3 already say") and its object "instead of copying them" (the preamble) give the compliant reading inside the Constraint itself. This is why I concede R3-F3.
2. TL:87 makes Task 5's test assert that the template carries the guard line, so the verbatim `worker_done --outcome failed` text is pinned twice (TL:52 and TL:87). The fix to TL:21 must therefore scope the rule; it cannot be met by paraphrasing.
3. Severity is mechanical: the parent derives it from the reviewer's yes/no answers and a byte-presence Read-back (qa:37, :56, :61). The plan's readiness therefore depends on whether a reasonable reviewer can say yes with no compliant reading available. That is the line between Task 7 and R3-F3.
4. The Task 2 `dispute` route is itself a STOP `E-HALT-QA` (retry:107), so it is a safer halt, not an absence of one.
5. mw:36 puts the always-staged rule on the executor, which is why A-008 drops to minor.

##### 5. Shared assumptions

- **A-002 (the executor follows Depends-on edges): REJECT. Unchanged.** SKILL:79 ignores `depends-on`; SKILL:97 runs unmarked tasks in source order; no task is marked `independent`.
- **A-003 (one undefined "blocking" means FAIL): QUALIFY. Converged.** I accept the shared test (R2-A:91 with B's irreversible-effect clause, R2-B:89). Blocking = following the plan as written, in source order under `/sc:implement`, leaves no compliant choice under any reading the plan's text supports: an unmet AC (B1), a breach of a Constraint or explicit task instruction (B4, qa:52), an unguarded irreversible or outward effect, or a P0 pass condition no task performs (SRC:241). When a compliant reading exists and the plan points to it, should-fix. One blocking finding means FAIL. Result: Task 7 only.
- **A-005 (the run is attended): QUALIFY. Unchanged in substance, now shared.** Approvals need a person (TL:25, TL:110), and the person-opened implement session is the coordinator (TL:26). But "stop this task and report" is not an executor outcome (qa:288). Fix: one Constraint line that the run must be attended and never headless, plus the Task 7 refusal line. On B's point (R2-B:83) that a strict reading of qa:288 would cover Task 7's own approval questions: I read qa:288 as closing the list of halts, not banning questions a task's own AC requires, but the attended-run line removes the doubt.
- **A-007 (the spec is a consistent authority): REJECT the assumption. Unchanged,** with A's boundary: SRC:60 against SRC:306 (three texts against "four") and the stale `install_core.py:13-24` range in SRC:59 are spec defects. R3-F3 is not one: SRC:59 is consistent and TL:21 widened it.
- **A-008 (post-commit artifacts need no staging): QUALIFY. Changed from REJECT.** mw:36 binds the executor to stage `.dev/tasks`, and staging is not committing (TL:22). Add one recorded `git add .dev/tasks` at the end of the closing phase-report task. Minor. U-008 stays inside the Task 7 finding.

##### 6. Contested points

| Point | Current preferred variant or merged position | Confidence |
|---|---|---|
| S-006 / A-003 (blocking count) | Merged: exactly 1 blocking finding (Task 7), under the shared test. C's Round 1 count of 2 withdrawn. | 0.85 |
| X-005 / U-002 / U-006 (Task 7) | A + C merged, **blocking**. Basis: the install-versus-commit order clash in TL:110 (B4, qa:52), per B; the commit ID is supporting. Consequence: `head-moved` halt with no adviser (retry:41, :44). Fix: the seven-step order in section 3, with the path list and `.dev/tasks` in the `--only` pathspec. Drift for the wording, necessary for the commit. | 0.85 |
| U-007 / R3-F3 (verb syntax) | C's finding with A's narrower reading. **Should-fix (top)**, drift. Only the guard line is unavoidable (SRC:86, pinned by TL:52 and TL:87). Fix: scope TL:21 as SRC:59 does. | 0.80 |
| C-002 / X-002 / X-003 (cadence run) | Should-fix (top), C's wording: a run longer than the cadence outside Agent-tool calls; no vacuous fallback; if none, P0 does not pass. | 0.90 |
| X-004 (exact refusal texts) | A: three exact texts plus the case-3 prefix, with a spec erratum note. | 0.90 |
| C-004 (phase-end checks) | One closing phase-report task (R3-F11 / A's F7) re-running AC-C1, AC-C2 and the AC-C3 comparison, recording AC-C5 with an empty edit set (R2-3), ending with a recorded `git add .dev/tasks`. Minor. | 0.80 |
| C-001 / X-001 (Task 3 dependency) | Minor, drift; residual is R3-F5's red window. | 0.90 |
| X-006 (classes) | Task 3: drift. AC-0.9: drift. Stale cite: none. Task 7: drift for wording, necessary for the commit. R3-F3: drift. | 0.80 |
| A-005 | QUALIFY: attended-run Constraint line plus the Task 7 refusal line (qa:288). | 0.80 |
| A-008 | QUALIFY (moved from REJECT): one recorded closing staging line, minor (mw:36). | 0.75 |
| A-002 / A-007 | REJECT the assumption in both cases. | 0.90 |

## Round 2.5: Invariant Probe (summary)
Full table: `invariant-probe.md`. Summary (INV:25-29): 16 probe findings; 6 ADDRESSED; 10 UNADDRESSED, of which 2 HIGH (INV-001, INV-002), 5 MEDIUM (INV-003 to INV-007) and 3 LOW (INV-009, INV-013, INV-015).

- INV-001 (HIGH, sufficiency_challenge): the merged Task 7 fix asks both approvals up front, so the commit approval is not "at the moment of action" as TL:25 requires (INV:8; TL:25 reads "Commits and installs need the owner's approval at the moment of action").
- INV-002 (HIGH, sufficiency_challenge): at P0 no command writes a WC-4 contract, so 7.2 step 3 (SRC:285: "its `--outcome` matches the contract's `worker_status` under WC-5; its report path is the WC-4 contract path") can pass only by reporting `failed` under WC-5's no-contract rule (SRC:73). AC-0.4 swaps in the existing report only for step 4 (SRC:301). No card, diff row or advocate raised it (INV:9).

## Round 3: Final Arguments (if applicable)
Not run. Round 3 is conditional on `--depth deep AND convergence < threshold` (ADV-SKILL:193-195). This run is depth standard, and convergence (96.2%) is above the 80% threshold.

## Shared-Assumption Omission Check
Promoted points to answer: A-003, A-005, A-008 (diff:106-110). Each advocate had to answer each with ACCEPT, REJECT or QUALIFY, and an unanswered point is flagged `[OMISSION]` (ADV-SKILL:985-1002).

| Advocate | Round | A-003 | A-005 | A-008 |
|---|---|---|---|---|
| A | 1 | QUALIFY (R1-A:68) | QUALIFY (R1-A:69) | QUALIFY, leaning REJECT (R1-A:71) |
| B | 1 | QUALIFY (R1-B:65) | QUALIFY (R1-B:66) | QUALIFY (R1-B:68) |
| C | 1 | QUALIFY (R1-C:75) | QUALIFY (R1-C:77) | REJECT (R1-C:81) |
| A | 2 | QUALIFY (R2-A:91) | QUALIFY (R2-A:92) | QUALIFY (R2-A:94) |
| B | 2 | QUALIFY (R2-B:89) | QUALIFY (R2-B:90) | QUALIFY (R2-B:92) |
| C | 2 | QUALIFY (R2-C:85) | QUALIFY (R2-C:86) | QUALIFY, moved from REJECT (R2-C:88) |

Result: no `[OMISSION]` flags. Every advocate answered every promoted A-NNN point in both rounds. Omission count: 0.

The non-promoted flagged assumptions A-002 and A-007 (diff:96, diff:101) were also answered by all three in both rounds, each as REJECT (R1-A:67, :70; R1-B:64, :67; R1-C:73, :79; R2-A:90, :93; R2-B:88, :91; R2-C:84, :87). They are not in the convergence denominator because they were not promoted.

## Taxonomy Tagging and Coverage
Rule (ADV-SKILL:133-177): scan each diff-point row for level signal terms; L3 beats L2 beats L1; no signal means L2. L1 signals: naming, formatting, wording, style, cosmetic, presentation. L2: architecture, API, component, module, interface, dependency, organization. L3: state, guard, boundary, invariant, concurrency, race condition, validation rule, transition. Row text is from diff:19-26, diff:36-44, diff:57-62, diff:108-110. Where the signal is a direct synonym, the matched words are shown.

| Point | Level | Signal matched in the row |
|---|---|---|
| S-001 | L2 | none (default) |
| S-002 | L2 | "granularity" / bundling = organization |
| S-003 | L2 | none (default) |
| S-004 | L2 | "Extra blocks" = organization |
| S-005 | L1 | "Evidence format" = formatting |
| S-006 | L2 | none (default) |
| S-007 | L1 | "Verdict, self-confidence, persona" = presentation |
| S-008 | L2 | "Depends-on edges" = dependency |
| C-001 | L2 | "not a dependency" = dependency |
| C-002 | L3 | "longer than the heartbeat cadence" = boundary (a time threshold) |
| C-003 | L3 | conditional fallback on the AC-0.6 answer = guard |
| C-004 | L3 | "Phase-end state" = state |
| C-005 | L2 | "make path and scan roots monkeypatchable" = interface |
| C-006 | L3 | classification that is empty at P0 = validation rule, boundary (empty set) |
| C-007 | L3 | what the test must assert = validation rule |
| C-008 | L1 | "Stale cite" (B:145 calls it "Cosmetic") = cosmetic |
| C-009 | L3 | commit inside the task window moves HEAD = state, transition |
| X-001 | L2 | "Task 3 dependency gap" = dependency |
| X-002 | L3 | "longer-than-cadence run" = boundary |
| X-003 | L2 | none (default) |
| X-004 | L3 | "`guard refused:` reason texts" = guard |
| X-005 | L3 | "commit the last action" = transition (step order) |
| X-006 | L2 | none (default) |
| A-003 | L2 | none (default) |
| A-005 | L3 | mid-task approval pause = guard (approval gate) |
| A-008 | L3 | post-commit staging = state |

Coverage: L1 = 3 points (S-005, S-007, C-008), L2 = 12 points, L3 = 11 points. Total 26.

Addressed in debate per level: L1 by S-007 (R2-A:7, R1-C:54) and C-008 (R1-B:21, R1-C:52); L2 by, for example, C-001 and A-003 (R2-A:91, :104); L3 by, for example, C-009 and A-005 (R2-B:39, :90). All three levels have coverage greater than zero. The taxonomy gate passes, and no forced round is needed (ADV-SKILL:1405-1427).

## Scoring Matrix
Confidence rules (ADV-SKILL:1511-1526): unanimous 90-100%, majority 60-89%, split 50%; +10% when the losing advocate conceded; never 100% unless all conceded. Positions are taken from the Round 2 contested-point tables (R2-A:98-109, R2-B:96-110, R2-C:92-104) and, where a point is not in those tables, from Round 1.

| Diff Point | Level | Winner | Confidence | Agreed | Evidence Summary |
|------------|-------|--------|------------|--------|-----------------|
| S-001 | L2 | Variant C | 85% | yes (3/3) | C's 14 findings give the widest verified coverage; A credits C's breadth (R1-A:15) and A and B concede gaps in their own cards (R1-A:46, R1-B:45). C's 2-blocking mix did not survive (R2-C:66). |
| S-002 | L2 | Variant C | 75% | yes (3/3) | Every Round 2 table follows C's split, with R3-F5 as the dependency residual (R2-A:104, R2-B:105, R2-C:100); C argues the split eases the merge (R1-C:29). |
| S-003 | L2 | Variant A | 65% | yes (3/3) | All three adopt A's `necessary` class for the Task 7 commit (R2-A:106, R2-B:107, R2-C:101). A's own `regression` (F1) and `none` (F6) labels were conceded wrong (R1-A:45, :48). |
| S-004 | L2 | Variant B | 80% | yes (3/3) | A and C credit `matrix_omissions` (R1-A:11, R1-C:15), and its L3 staging note is the root of A-008 (R1-B:19). It targets the coverage matrix, not the plan (diff:80). |
| S-005 | L1 | unresolved | 50% | no | No advocate took a position on evidence path format in either round. |
| S-006 | L2 | Variant C | 80% | yes (3/3) | Each C calibrator note (C:285) was adopted: the R3-F2 downgrade and "cannot pass" overstated (R1-C:48-49, R2-B:15). All three end at exactly 1 blocking finding (R2-A:100, R2-B:98, R2-C:94). |
| S-007 | L1 | Shared (A = B = C) | 90% | yes (3/3) | All three keep FAIL (R2-A:7, R2-B:7, R2-C:7). C concedes its 0.72 self-confidence was the lowest (R1-C:54). |
| S-008 | L2 | Variant B | 75% | yes (3/3) | B's open statement of its executor assumption (B:232-234) let the debate settle X-001 (R1-B:20); A concedes its own hedge was weaker (R2-A:18); C notes B named it (R1-C:17). |
| C-001 | L2 | Variant C | 95% | yes (3/3, A conceded) | `/sc:implement` ignores `depends-on` and runs unmarked tasks in source order (SKILL.md:79, :97), so only R3-F5's unchecked red window from Task 1 to Task 3 remains (R1-A:43, R2-A:13). |
| C-002 | L3 | Variant C (wording; A's grade) | 90% | yes (3/3, B conceded) | Should-fix at the top of the list, with C's wording, a run outside Agent-tool calls and no vacuous fallback (R2-A:103, R2-B:101, R2-C:97). B withdrew blocking (R1-B:41) and the vacuous fallback (R2-B:18). |
| C-003 | L3 | Variant B | 70% | yes (3/3) | All grade it minor, drift (R2-B:102, R1-C:63). B's R2-2 gives the delegation reason and the one-line fix (B:46-49, B:60-62); C's R3-F14 is equivalent. |
| C-004 | L3 | Variant C | 80% | yes (3/3) | One closing phase-report task per R3-F11 and F7, carrying B's AC-C5 record and the closing staging line (R2-B:103, R2-C:99). A says R3-F11 matches F7 and adds the file name (R1-A:24). |
| C-005 | L2 | Variant C | 70% | yes (2/3: B, C) | C's R3-F8 adds the risk that a leftover scratch skill breaks `make verify-sync` (C:140-141); B accepts it (R1-B:13, :43). A claims F5 but does not compare (R1-A:25). |
| C-006 | L3 | Variant C | 90% | yes (3/3, A conceded) | The empty AC-0.9 class is drift (R1-A:45, R2-A:14, R1-B:28, R1-C:38). C's R3-F13 also defines the `gh api` post patterns (C:229-230). |
| C-007 | L3 | Variant B | 85% | yes (3/3, C conceded wording) | B's R2-5 phrase list with A's three-texts correction (R2-B:104). C merges them (R2-C:16) and A accepts the list (R2-A:73). |
| C-008 | L1 | Variant B | 90% | yes (3/3, C conceded) | Class none: SRC:59 cites the same stale range and the edit is made by symbol name (R1-B:21, R1-C:52, R2-A:106). |
| C-009 | L3 | Variant C | 85% | yes (3/3) | Task 7 is blocking: TL:110's "Then ask ... on approval, run it" and "Make the commit the last action of the task" cannot both hold (R2-B:39, R2-C:47). A's F3 `head-moved` halt is the consequence (retry.md:41, :44; R2-A:101). |
| X-001 | L2 | Variant C (with B) | 95% | yes (3/3, A conceded) | Minor, not blocking: source-order execution (SKILL.md:97) runs Task 3 before Task 4 (R1-A:57, R2-A:104). |
| X-002 | L3 | Variant A | 95% | yes (3/3, B and C conceded) | Should-fix, not blocking: TL:122 brings step 5 in by reference (R1-B:41, R1-C:48, R2-A:103). |
| X-003 | L2 | Variant A | 95% | yes (3/3, B conceded) | B applied the delegation argument to one SRC:291 clause and not the other (R1-A:13, R1-B:40, R2-B:15). |
| X-004 | L3 | Variant A | 95% | yes (3/3, C conceded) | SRC:60 gives three exact refusal texts and case 3 has only the prefix (R1-C:50, R2-B:106, R2-C:98). |
| X-005 | L3 | Variant C | 85% | yes (3/3) | TL:110's wording cannot be followed; merged blocking finding (R2-A:101, R2-B:99, R2-C:95). A conceded its "commit last as mitigation" reading (R1-A:44). |
| X-006 | L2 | Variant C | 70% | yes (3/3) | Shared class table: Task 3 drift, AC-0.9 drift, stale cite none, Task 7 drift for the wording and necessary for the commit (R2-A:106, R2-B:107, R2-C:101). C's classes win 3 of the 4 items. |
| A-003 | L2 | Variant A | 85% | yes (3/3) | All QUALIFY and converge on A's sharpened blocking test (R2-A:91) plus B's irreversible-effect clause (R2-B:89, R2-C:85). |
| A-005 | L3 | Variant C | 80% | yes (3/3) | All QUALIFY. A and B adopt C's point that "stop this task and report" is not an executor outcome under qa.md:288 (R2-A:92, R2-B:90, R2-C:86). |
| A-008 | L3 | Variant B | 80% | yes (3/3, C moved from REJECT) | Minor: one recorded closing `git add .dev/tasks` (R2-A:94, R2-B:92, R2-C:88). B first flagged the L3 staging rule (R1-B:19). |

Unique contributions (optional rows, not in the convergence denominator):

| Point | Disposition | Evidence |
|---|---|---|
| U-001 (A, F2) | Kept, should-fix | Same as X-004 (R2-B:76, R2-C:71) |
| U-002 (A, F3) | Kept, merged into the blocking Task 7 finding | R2-A:101, R2-B:99, R2-C:95 |
| U-003 (A, F8) | Parts (b) and (c) kept as minor; part (a) dropped | R2-A:15 (A concedes part (a)) |
| U-004 (B, matrix_omissions) | Not a plan finding; route to the reflect coverage matrix | diff:80 |
| U-005 (B, Task 6 before Task 4) | Dropped: rests on the rejected A-002 | R1-B:43, R2-B:19 |
| U-006 (C, R3-F1) | Kept, core of the blocking Task 7 finding | R2-C:95 |
| U-007 (C, R3-F3) | Kept, should-fix (top); blocking candidate withdrawn | R2-C:7, R2-A:102, R2-B:100 |
| U-008 (C, path list and `--only`) | Kept, inside the Task 7 finding | R2-A:94, R2-C:57 |
| U-009 (C, R3-F6) | Kept, minor, class drift (not regression) | R1-C:53 |
| U-010 (C, R3-F7) | Kept, minor | R2-C:73 |
| U-011 (C, R3-F10) | Kept, minor | R2-C:73 |

Debate points won (for the Step 3 tiebreaker): Variant C 13, Variant B 6, Variant A 5, shared 1, unresolved 1 (26 total).

## Convergence Assessment
Formula (ADV-SKILL:1385-1389): convergence = agreed points / (count S + count C + count X + count A).

- Denominator: S-NNN 8 (diff:19-26) + C-NNN 9 (diff:36-44) + X-NNN 6 (diff:57-62) + A-NNN 3 promoted (A-003, A-005, A-008; diff:106-110) = 26.
- Agreed points: 25. Agreement is unanimous or a 2-of-3 majority (ADV-SKILL:1429-1432).
- Points resolved: 25 of 26
- Alignment: 25 / 26 = 0.9615 = 96.2%
- Threshold: 80%
- Score gate: passed (96.2% >= 80%)
- Taxonomy gate: passed (L1 3, L2 12, L3 11; all levels addressed)
- Invariant gate: failed (see next section)
- Status: BLOCKED_BY_INVARIANTS ("Agreement >= threshold AND taxonomy covered BUT HIGH-severity UNADDRESSED invariants exist", ADV-SKILL:1496)
- Unresolved points: S-005 (evidence path format; not debated)
- Oscillation: none. Every Round 2 movement is one-way toward the shared position (B from 0 to 1 blocking, R2-B:7; C from 2 to 1, R2-C:66).

## Invariant Probe Gate
Gate rule (ADV-SKILL:1455-1477): any row with Status UNADDRESSED and Severity HIGH blocks convergence regardless of the agreement score; UNADDRESSED MEDIUM rows are warnings; LOW rows need no action.

```text
CONVERGENCE BLOCKED: 2 HIGH-severity UNADDRESSED invariant(s) detected
Blocking items: INV-001, INV-002
These invariant violations must be resolved before convergence can be declared.
Action: Address the flagged items in a subsequent debate round or acknowledge as accepted risk.
```

- INV-001 (INV:8): the prescribed Task 7 fix asks both approvals up front, which breaks TL:25's "at the moment of action" and brings back a quotable B4 conflict on the task that moves HEAD.
- INV-002 (INV:9): Task 8 cannot reach a passing AC-0.4 at P0, because step 3 needs a WC-4 contract that no P0 command writes (SRC:285, SRC:301, SRC:73). This is a candidate second blocking finding under the debate's own clause (d), "a P0 pass condition that no task performs" (R2-B:89, R2-C:85). The advocates never adjudicated it.

```text
WARNING: 5 MEDIUM-severity UNADDRESSED invariant(s) detected
Items: INV-003, INV-004, INV-005, INV-006, INV-007
These items do not block convergence but should be reviewed.
```

- INV-003 (INV:10): "a QA failure after the commit is never retried" in plan text cannot turn off the executor's Q5 fix pass or halt table.
- INV-004 (INV:11): an "attended, never headless" Constraint line does not make Task 7's approval questions legal under qa.md:288.
- INV-005 (INV:12): `--force` overwrites more than TL:25 tells the owner, and Task 7 has no rule for a non-zero install exit.
- INV-006 (INV:13): the merged cadence fix has two readings under the executor; it must pick one in writing and name the long run.
- INV-007 (INV:14): TL:114, TL:116 and TL:128 name no saved artifact, so a managed FINAL that sees only files and logs cannot confirm them.

LOW and UNADDRESSED (no action required by the gate): INV-009, INV-013, INV-015 (INV:16, INV:20, INV:22).
