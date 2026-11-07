# Round 1 advocate statement - Variant 2 (reviewer-2 card, qa)

Folder F = `.dev/reflect/pre-TASK-WF-p1LivePlanBrief-20261105-164506-20261105172548/adversarial/`. Plan = `.dev/tasks/to-do/TASK-WF-p1LivePlanBrief-20261105-164506/TASK-WF-p1LivePlanBrief-20261105-164506.md` (586 lines); brief = `source.md` in the same folder.

## Position summary

V2 is the most precise card on brief-to-plan fidelity: every deviation it lists is real, correctly classed and cited, and it alone found the lc18 phase-header contradiction (C-009), the coverage-matrix trace gaps (C-010) and the flag-table advisory (U-006). It missed the Task 1 install-line defect (C-001) and the weaker C-002, C-003 and C-005; C-001 is a real, high-impact defect and its "No Regression found" line (X-001) is wrong on severity, and I concede that. The merged result should take V1/V3's C-001 and V2's C-004 class and C-009/C-010/U-006.

## Steelman

### Variant 1 (reviewer-1, analyzer)
Strongest argument: V1 audited the plan as an executable artifact, not only as a copy of the brief. Its Regression #1 is correct. The plan's install line (plan:58) says to `cmp` "every file under `src/superclaude/commands/` (the whole folder, changed or not) with its installed copy `~/.claude/commands/sc/<name>.md`" and "the line is PASS only when every `cmp` exits 0". I verified the facts: `src/superclaude/cli/install_commands.py:11` has `_EXCLUDE_FILES = {"README.md"}` and `:40` globs only `*.md`; the source folder has 48 entries (including `README.md` and `__init__.py`, both tracked per `git ls-files src/superclaude/commands`), while `~/.claude/commands/sc/` has 46 and contains neither. So two `cmp` calls must exit non-zero, the install line is FAIL, and the Task 1 gate (plan:61) then makes every live task write `not run: install precondition failed`. That would void the whole run. V1 also has the widest coverage (12 rows), a sensible two-part treatment of C-004 (Necessary swap plus a separate quoting concern), and the only report of U-001 (`--parent-worktree active` selector ambiguity) and C-013 (static report covers 7127c247, not the tested tip). Its 5-of-6 Drift calls are mostly low and honest.

What V1 gets right that V2 does not: C-001, C-002 (in some form), C-003 (in some form), C-005, C-013, U-001, U-002.

### Variant 3 (reviewer-3, refactorer)
Strongest argument: V3 reasons about the plan's internal consistency and state mechanics, which is where this plan is weakest. It found the same Regression as V1 and framed C-002 better than V1: the clean-tree check (plan:58) conflicts with the plan's own planned edit (plan:52, the AC-1.8 owner-instruction bullet is to be replaced "before the first task starts"), and the plan's own no-commit rule (plan:24) means the tree cannot be made clean again. V3 also added three non-obvious items: U-003 (`pgrep -af -- '--watch'` can match the Bash tool's own shell, plan:227, :451, :465), U-004 (no rule to normalise the worker's `--report-path` against `<R>/return-contract.yaml`) and U-005 (`install_skills.py:88-98` skips sc-* skills served by a command; I read that code and the skip is real: `_has_corresponding_command` -> `continue` and even removes a stale install, so a skills `cmp` for such a skill would hit a missing file). Its notes are the most careful about what it did not check.

What V3 gets right that V2 does not: C-001, C-002, C-003, C-005, U-003, U-004, U-005.

## Strengths claimed (V2)

1. **Accurate classification of C-004 (X-002).** The grant-file swap is Necessary, not Drift. The reason is stated in the plan itself: `/sc:implement` may not prompt the owner during the run (plan:52), so a grant file "created by the owner, not by the plan" (source.md:79) has no creator at run time; the owner's sentence is given in the session beforehand. Plan:14 says the plan governs where it differs, and names the swap. V3 calls this Drift because "the reason does not explain" it; but plan:52 does explain it, and the collision with C-002 is a separate defect that belongs under C-002, not a reason to reclassify the swap.
2. **Unique finding C-009 (lc18 vs the phase header).** `source.md:70` says the refusals phase is "steps 3 and 4 replaced ... step 6 must show nothing written", yet the lc18 row at `source.md:72` expects a contract with `worker_status: failed`, which is a write. The plan (Task 19, lc18) resolves this by keeping step 3's pass rule. V2 correctly classed that as Necessary, and the contradiction is real in the brief. No other card noticed.
3. **Unique finding C-010 (coverage matrix).** Seven spans of source.md have no matrix row; V2 also checked that the plan implements each, so this is trace debt and not a plan defect. `artifacts/coverage-matrix.yaml` exists in the reflect run (confirmed by glob), so the claim is checkable by the merge step.
4. **U-006 flag-table advisory.** lc13 uses `--report-dir` on `/sc:impact`, whose row in `src/superclaude/core/WORKER-CONTRACT.md:195` names `--output-dir`; lc15 omits `--output <file>` (the row at `:197`). The brief (source.md:65, :67) is the origin. This is Low, but it is a real doc/brief mismatch a maintainer would want. The spec's rule that is relevant is the "both a directory-valued output flag and `--report-dir`" error at WORKER-CONTRACT.md:36: lc13 passes only `--report-dir`, so no refusal is triggered.
5. **Calibrated severity.** Only 2 Drift rows, both LOW, and every row cites a source line that I re-read (source.md:30, :70, :72, :79; p1-static-report.md:29). No row in V2 overstates. By contrast V1 #3 and V3 #5 rely on weak reasons (see Weaknesses 2 and 3).
6. **Correct C-008.** D-P1-5 (the workflow handoff skip) is cited at plan:405 for "the worker did not stage `.dev/tasks`". I read plan:405 and the D-P1 list in `p1-static-report.md`: D-P1-5 is "workflow skips `--handoff implement`", not a staging rule. V1 and V2 caught it; V3 missed it.

## Weaknesses identified in the other variants

1. **V1 and V3 label C-001 "Regression" although the brief says the same.** `source.md:87` already reads "install precondition by `cmp` of every file under `src/superclaude/commands/`". The plan copies the brief, so under the 4-category taxonomy there is no plan-versus-brief divergence; the defect is inherited from the brief and the plan then sharpens it with "the whole folder" and "PASS only when every `cmp` exits 0". The impact rating (HIGH) is right; the class label is arguable. Neither card says the defect is in the brief too, and the fix (exclude README.md and `__init__.py`, and handle skills served by a command) must be applied in the plan and flagged to the brief owner.
2. **V1 #2 relies on stale state.** V1 says the tree "already had tracked changes (APPROVED.md, plan file)". `git status --porcelain` right now shows only two untracked `.dev/reflect/...` folders; the plan file is tracked and clean (HEAD `0b443745`, which committed the plan). So "the tree is already dirty" is not true at this moment. The durable form of the finding is V3's: the planned edit at plan:52 would dirty a tracked file and plan:24 forbids committing. V1's own wording on plan:65 (baseline-tolerant) also shows the plan author knew the tree could be dirty.
3. **V1 #3 treats a fuzzy test as a deviation of Medium severity.** "still reads NOT YET GIVEN" (plan:552) is a literal string test on a bullet whose placeholder text is fixed at plan:52; it is not fuzzy. The quoting concern (the whole bullet vs the owner's sentence) is a valid LOW wording point only. MEDIUM overstates it.
4. **V1 #7 and V3 #2 (C-003) overstate "can never pass".** `source.md:78` and plan:541 both say "excluding tracked files that existed before" / "tracked files that existed before the runs do not count", and the plan saves `ac13-status-before.txt` and `ac13-status-after-N.txt`. There are 326 tracked `return-contract.yaml` files on the branch (`git ls-files | grep -c return-contract.yaml` = 326), so the literal "find output is empty" is unsatisfiable. But the exclusion sentence tells the executor how to reconcile it. The defect is a contradictory pass rule that an executor must interpret, not a certain false FAIL. Real, Low-to-Medium.
5. **V3 #5 (grant-file reason "weak") is a mis-class** (see Strength 1) and its "not listed in post-fix-rechecks.md" is unverifiable from the three files given.
6. **V3 U-005 is explicitly unchecked** by its own note ("not checked"), and V3 U-003 is plausible but unverified empirically; neither should be promoted above Low-Medium without a test.
7. **V1 U-001 is weaker than it looks.** `--parent-worktree` accepts `active/current` (p0-live-orca-help.txt:36, :49, :69) as a documented selector. Whether it picks the coordinator's worktree or the UI's is a real runtime question, but the plan already runs `worker-start` from the coordinator terminal and saves help in Task 1, so it is a Low advisory, not a deviation.

## Concessions (genuine weaknesses of V2)

1. **C-001 is a real, high-impact defect and V2 missed it.** I checked it against `install_commands.py:11,40`, the plan text at line 58 and the live directory listing (48 source entries vs 46 installed; no README.md or `__init__.py` installed). V2's line "No Regression found (every command line in Tasks 2-24 matches source.md:51-79)" is wrong in substance: it compared command lines to the brief and never ran the install line against the installer. V2's own note admits it did not find it. This is the card's single largest failing and it drives the S-002/X-001 contradiction.
2. **C-002 is real in its V3 form** (planned edit at plan:52 plus no-commit rule at plan:24 versus "no modified tracked file" at plan:58; the end-of-task check at plan:65 tolerates baseline-modified files, so the checks conflict). Missed by V2.
3. **C-003 is a real wording defect** (326 tracked files; pass rule "find output is empty"), though softer than V1/V3 claim. Missed by V2.
4. **C-005 is real.** Plan:584 still says AC-1.8 was not run "for lack of the owner grant file" while plan:52, :552 and :580 use the owner-instruction bullet. Missed by V2.
5. V2 has the thinnest findings table (7 rows, S-001) and the fewest advisories; its "Haiku class" analysis stayed inside the brief-to-plan frame and did not execute the plan's commands mentally against the repository. That is why it missed all of C-001, C-002 and C-003.
6. C-010 is trace debt, not a plan defect, so it adds little to the verdict.

## Shared assumptions

- **A-001: QUALIFY.** The grounding hunks may be stale in one respect: the plan names tip `f0e307eb` as the branch state, but `git log -1` now prints `0b443745` (the commit that added the plan). The plan avoids a pin (Task 1 records `git rev-parse HEAD` and uses `git merge-base --is-ancestor 7127c247 HEAD`), so the stale tip does not break anything. The load-bearing facts for C-001 to C-003 are current: I re-read `install_commands.py` (lines 11, 40) and the plan lines (58, 61, 65, 541) in this round. Condition: any card statement about the working-tree state (V1 #2) must be re-read at merge time, because the tree is clean for tracked files today.
- **A-002: QUALIFY.** The brief is the authority for the audit of deviations, and the plan's header says the plan governs where they differ (plan:14), so "brief wins" holds only for undocumented differences. Conditions: (a) a documented, owner-decision-backed difference (C-004 by G1/D4; C-007 by the no-pin design) is Necessary, not Drift; (b) the brief is not a shield: C-001 is present in both brief (source.md:87) and plan, so a faithful copy of a wrong brief is still a defect, and the merge should record it under a plan-quality finding, not under deviation-from-brief.
- **A-003: QUALIFY.** The installed Orca is `1.4.245-aidev02.dfe1eb410300` (ran `orca --version`), and the P0-era help (`p0-live-orca-help.txt:36,49,69`) documents `--parent-worktree active/current`. Condition: the assumption holds if the executor checks the Task 1 `orca-help.txt` (plan:58 saves `worktree create --help`) for `--parent-worktree` and the `active` selector before Task 24 (plan:554) runs. The plan does not state that check; adding it is a one-line fix. Until then it is UNVERIFIED for 1.4.245, as the diff-analysis says.
- **A-004: ACCEPT.** I spot-checked eight cited lines against the current 586-line plan: plan:24 (no-commit rule), :52 (owner-instruction bullet), :58 (install line), :405 (D-P1-5), :541 (Task 23 find rule), :552 (lc22 gate), :584 (stale wording), :554/:563 (`--parent-worktree`). Every one lands on the content the cards describe, so there is no one-line shift in the post-17:26 file.

## Per-point judgements

Content points
- C-001: V1/V3 superior. Real and HIGH (installer excludes README.md; `__init__.py` is not `.md`; installed dir lacks both). Add that the same wording is in source.md:87.
- C-002: V3 superior. The planned plan-file edit plus no-commit rule is the durable conflict; V1's "already dirty" is stale (tracked tree clean at HEAD 0b443745).
- C-003: V1/V3 right that the rule is contradictory, but severity should be Low-Medium: source.md:78 and plan:541 carry an exclusion sentence (326 tracked contract files exist).
- C-004: V2 superior on class (Necessary); V1's separate quoting point is a valid LOW wording note.
- C-005: V1/V3 right (plan:584); fix is one phrase.
- C-006: tie, all three agree Necessary LOW.
- C-007: tie, all three agree Necessary LOW.
- C-008: V1/V2 right (plan:405 cites D-P1-5; the staging rule is WC-9); V3 missed it.
- C-009: V2 only, and valid (source.md:70 vs :72); keep as Necessary LOW.
- C-010: V2 only; valid but trace debt, Low; keep as a note.
- C-011: tie, Authorized.
- C-012: V1 superior (V2 folded it into #7); both Authorized.
- C-013: V1 only; plausible Low (plan:19, :22, :580), no counter-evidence found.

Contradictions
- X-001: V1/V3 superior (Regression exists in effect: HIGH). I withdraw V2's "No Regression found". Note the class label is debatable because the brief has the same text, so the merge should say "inherited defect, plan must fix" and keep HIGH.
- X-002: V2 superior (Necessary), because plan:52 states the reason (no prompting during `/sc:implement`); the collision with the clean-tree check is a C-002 matter.
- X-003: V3 superior (clean-tree check is MEDIUM and V3 adds the no-commit rule); V1 agrees on severity; V2 absent.

Unique items
- U-001: Low advisory (documented selector). U-002: Low. U-003: Medium-plausible, needs an empirical test. U-004: Medium, plausible gap. U-005: Medium, verified at `install_skills.py:88-98` as a real skip path, impact only if a changed skill is served by a command. U-006: Low, valid.
