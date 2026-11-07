<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 1 (reviewer-1 card, analyzer class; variant-1-original.md) -->
<!-- Merge date: 2026-11-05 -->

# Merged reviewer card (P1 live plan) - 11 deviations (Regression 1, Drift 5, Necessary 3, Authorized 2)

<!-- Source: Base (original) - path key, with spec/WORKER-CONTRACT/APPROVED/help paths added from Variants 2 and 3 and the round 2 rebuttals -->
Plan = `.dev/tasks/to-do/TASK-WF-p1LivePlanBrief-20261105-164506/TASK-WF-p1LivePlanBrief-20261105-164506.md` (`plan:NN` = line NN); brief = `source.md` in the same folder (`source.md:NN`).
Other paths as cited by the sources: spec = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`; `WORKER-CONTRACT.md` = the worker contract (`src/superclaude/core/WORKER-CONTRACT.md` installs to `~/.claude/WORKER-CONTRACT.md`); `APPROVED.md` = the owner decisions file (G1, H1); `p0-live-orca-help.txt` = `.dev/orca-command-refactor/review/p0-live-orca-help.txt`; `post-fix-rechecks.md` = the fix list of the round it is named for (the round-1 file lives in the `...165021` reflect folder; the file one level up from the debate folder lists revision 2 and did not exist when this card was written).
Finding IDs in brackets (C-nnn, U-nnn, INV-nnn, X-nnn) are the debate IDs in `diff-analysis.md` and `invariant-probe.md`.

## Findings

<!-- Source: Base (Variant 1) table structure, 11 rows; per-row origin and the changes applied are listed in the comment block after the table -->
| # | Class | Location | Finding | Fix | Evidence | Sev |
|---|---|---|---|---|---|---|
| 1 | Regression | plan:58 (Task 1 install line) | [C-001] `cmp` of "every file under src/superclaude/commands/" includes README.md and __init__.py, which the installer never copies, so the install line can never pass and every live task records `not run: install precondition failed`. It contradicts the plan's own definition of failure ("installed files differ", source.md:17 and plan:21). The strict wording ("the whole folder, changed or not", "PASS only when every `cmp` exits 0") was added to the plan by revision 1; source.md:87 already says "every file under". | Compare only `*.md` except `README.md` (consensus fix, as probed in invariant-probe.md) | src/superclaude/cli/install_commands.py:11 (_EXCLUDE_FILES = {"README.md"}), :40 (glob("*.md")); plan:21, :36, :61; source.md:17, :87. Reproduced by three advocates: `cmp` rc=2 on README.md and `__init__.py`; introduced by revision 1 of the plan (round-1 `post-fix-rechecks.md` row 2, in `.dev/reflect/pre-TASK-WF-p1LivePlanBrief-20261105-164506-20261105165021/`, as cited in round2-advocate-3 E1; repointed after evidence validation, see `artifacts/evidence-validation.md`) | HIGH |
| 2 | Drift | plan:58, :61, :65 | [C-002] Task 1 requires `git status --porcelain` to show no modified tracked file. The check fails for any uncommitted edit to a tracked file (INV-001): every fix to the plan, including the C-001 fix at plan:58 and the owner sentence at plan:52, leaves the plan file modified or staged (staged still prints `M `). plan:61 allows only the install line as a recorded FAIL, so Task 1 itself would fail its acceptance. plan:24 is a no-commit rule and nothing in plan:52 asks for a commit before launch. The tree is clean at 0b443745, so the check is dormant until the first plan edit. plan:65 tolerates baseline-modified files, so the checks do not conflict. | Scope the clean-tree check to `src plugins tests`. Alternative: commit every plan edit before launch (needs the user's explicit request, INV-015) | plan:58,61,65; plan:24, :52; invariant-probe.md INV-001 (`git ls-files` lists the plan file as tracked) | MEDIUM |
| 3 | Drift | plan:52, :556 (Task 24 brief substitution) | [C-004, quoting half] `<OWNER INSTRUCTION>` is replaced by the whole Constraints bullet "as it stands", which also holds plan prose beside the owner's words, so the brief may not quote the owner's instruction word for word. plan:52 does not say which text the owner edit replaces; the gate at plan:552 ("still reads NOT YET GIVEN") misfires if the sentence is added beside the token instead of replacing it. | Mark the owner sentence with markers in plan:52, state there that it replaces `NOT YET GIVEN`, and have plan:556 copy only the marked sentence | spec WC-9 (spec line 77); WORKER-CONTRACT.md:183; APPROVED.md:71 ("The brief copies it as given", as cited in round2-advocate-1 row 5) | LOW |
| 4 | Necessary | plan:14, :52, :552, :556-566 | [C-004, swap half] Owner grant file replaced by a Constraints bullet; documented inline (plan:14, plan:52) and justified by owner decision G1 (APPROVED.md:66-71). Not Drift (X-002 resolved): Drift is a silent change with no inline rationale. Consequence: the swap makes the plan:52 edit the expected path, which is what row 2 fires on. Provenance gap: the plan cites APPROVED.md only for H1 (plan:31), never G1. Authorized (owner decision) is the equal-effect alternative label. | None needed (not a defect); provenance note only | source.md:79; APPROVED.md:66-71 (G1) | LOW |
| 5 | Drift | plan:584 (Task 25 acceptance) | [C-005] Still says AC-1.8 "not run for lack of the owner grant file", contradicting plan:52, :552, :580. | Not stated in the sources; implied: make plan:584 agree with plan:52, :552, :580 | plan:51, :552, :584 | LOW |
| 6 | Necessary | plan:554 | [C-006] Child worktree created with `orca worktree create --parent-worktree active`, then sync, then `worker-start --worktree path:`, no `--setup`; justified by spec 7.2 step 1 and the slot rule. | None needed (not a defect) | spec 7.2 step 1; WORKER-CONTRACT.md:174; source.md:79; p0-live-orca-help.txt:36,49,69 | LOW |
| 7 | Drift | plan:541, :544 (Task 23) | [C-003] The PASS clause "the find output is empty" cannot be met literally: the branch tracks 325 `return-contract.yaml` paths (INV-009; the 326 in round 1 came from an unanchored grep) and no pre-run baseline is subtracted. plan:541 keeps the exemption ("tracked files that existed before the runs do not count") in the find-saving sentence, but the PASS clause drops the exemption that source.md:78 keeps inside it. `ac13-status-before.txt` and `ac13-status-after-N.txt` (plan:544) already hold the data for the subtraction. | Baseline diff: compare `ac13-find.txt` with `git ls-files '*return-contract.yaml'` taken in the same worktree, or put the exemption inside the PASS clause (as source.md:78 does) | plan:541,544; spec AC-1.3 (spec line 319, "no return-contract.yaml appears"); source.md:78; invariant-probe.md INV-009 | LOW |
| 8 | Necessary | plan:19, :33, :58 | [C-007] Tip pin replaced by branch-tip.txt plus an ancestor check; justified. | None needed (not a defect) | source.md:30 | LOW |
| 9 | Authorized | plan:36, :38 | [C-012] Gate line and Section check added. | None needed (not a defect) | spec 7.2 step 1 | LOW |
| 10 | Authorized | plan:44, :473, :495 | [C-011] "Command not invoked" check extended to guard cases 1 and 2. | None needed (not a defect) | spec AC-1.7 | LOW |
| 11 | Drift | plan:405 | [C-008] The extra cites D-P1-5 for "worker did not stage .dev/tasks"; D-P1-5 is about skipping --handoff implement; the staging rule is WC-9. The requirement is right, the decision cited is wrong. | Not stated in the sources; implied: cite WC-9 instead of D-P1-5 | .dev/tasks/done/TASK-WF-writeTheP1Static-20261105-033458/artifacts/p1-static-report.md:29; plan:405 | LOW |

<!--
Per-row origin (change numbers refer to refactor-plan.md):
row 1  Base (Variant 1 #1), modified - change 2 (evidence appended), plus plan:21,:36,:61 from Variant 3 #1 and the label wording from base-selection.md
row 2  Base (Variant 1 #2), modified - change 1 (restated per INV-001; plan:24,:52 from Variant 3 #3)
row 3  Base (Variant 1 #3), modified - change 4 (quoting half; severity MEDIUM -> LOW, "fuzzy test" removed, marker fix added)
row 4  Base (Variant 1 #4) merged with Variant 2 #1 - change 4 (swap half; G1 cited, APPROVED.md:66-71; consequence note from Variant 3 #5)
row 5  Base (Variant 1 #5), unchanged apart from evidence plan:51 from Variant 3 #6
row 6  Base (Variant 1 #6) plus evidence from Variant 2 #2 and Variant 3 #7
row 7  Base (Variant 1 #7), modified - change 3 (severity LOW, baseline-diff fix)
row 8  Base (Variant 1 #9), unchanged
row 9  Base (Variant 1 #10), unchanged
row 10 Base (Variant 1 #11), unchanged
row 11 Base (Variant 1 #12), unchanged
Base row #8 (Variant 1, C-013) removed from the table - change 5 (see Notes)
Fix column: new in the merged card; text comes from the invariant probe, the round 2 rebuttals and base-selection.md; "implied" marks a fix the sources do not state.
-->

## Advisory

<!-- Source: Base (Variant 1 "Advisory correctness gaps" 1 and 2), plus Variant 3 advisory 1 and 2 (changes 6 and 7), the invariant probe (change 8) and Variant 2 advisory (change 9) -->
Advisory items are not deviations from the plan; they are risks to the run or to the trust in its verdicts.

1. **[U-001] `--parent-worktree active` may resolve to the Orca UI's active worktree, not the coordinator's.** Unverified. Fix: Task 24 reads the parent field of `lc22-worktree.json` once. Evidence: plan:554; p0-live-orca-help.txt:36,49,69. (Base, Variant 1 advisory 1; restated per round2-advocate-1 row 7.)
2. **[U-002] Live tasks depend only on Task 1.** A concurrent run would pollute `check --run` and the machine-wide `pgrep`. Evidence: plan:41, :451. (Base, Variant 1 advisory 2.)
3. **[U-003] The lc18 watcher check can fail with nothing wrong (LOW-MEDIUM).** `pgrep -af -- '--watch'` matches the Bash tool's own wrapper shell, whose PID differs on every call, so the lc18 rule "the second output has no new process" can fail falsely. Reproduced by advocates 1 and 3 and by the probe (INV-010). Scope: lc18 only; the lc08 wording (plan:227) says "started by the worker", which tolerates a wrapper line. Fix: filter out `pgrep`, its parents and the Bash wrapper, or match on the `claude` processes only. Evidence: plan:451, :465; source.md:72. (Variant 3 advisory 1, scoped per round2-advocate-3 E5.)
4. **[U-004] No rule compares the worker's `--report-path` with `<R>/return-contract.yaml` after normalising it (LOW-MEDIUM).** `<R>` ends in a slash (`.dev/p1-live/<name>/`), so the literal string is `...//return-contract.yaml`, and a worker that passes a single-slash or absolute path gets a false step-3 FAIL (INV-011). Fix: normalise both paths with `realpath -m` before comparing. Evidence: plan:41, :43, :73. (Variant 3 advisory 2.)
5. **[INV-012] A retry of Task 1 creates a second Orca run (MEDIUM).** The "never repeat" rule (plan:28) covers only live tasks, but Task 1 also runs `orca orchestration run-create` and overwrites `./artifacts/live-run.json` (plan:58). If Task 1 fails its acceptance (for example through row 2) and `/sc:implement` retries it, the first run is orphaned and `status-baseline.txt` is re-taken with the Task 1 artifacts already present. Fix: add a rule that a retry reuses an existing `live-run.json` instead of calling `run-create` again. Evidence: plan:28, :58. (Invariant probe.)
6. **[U-006] Flag-table coverage (LOW).** lc13 uses `--report-dir` where the WORKER-CONTRACT.md table names `--output-dir` (WORKER-CONTRACT.md:195); lc15 omits `--output <file>` (WORKER-CONTRACT.md:197). Spec 2.1 permits both and no rule is breached (the refusal at WORKER-CONTRACT.md:36 needs both a directory-valued output flag and `--report-dir`); the own-flag form for impact is never exercised live. Evidence: source.md:65, :67; WORKER-CONTRACT.md:36, :195, :197. (Variant 2 advisory, scoped per round2-advocate-2 N5.)

## Notes and not checked

<!-- Source: Variant 1 #8 (C-013, demoted per change 5), Variant 2 #4 and #6 (C-009 and C-010, change 9), Variant 3 notes and round 2 rebuttals (change 10) -->
### Notes (not counted in the title)

- **[C-013] Static report covers 7127c247, not the tested tip; Task 25 does not require stating that.** Demoted from a Drift row: spec line 238 has no "same tree" clause (it says the phase passes when both plans' checks pass), the coordinator commits and installs outside any plan run so the tip is expected to move, plan:19 documents the move and Task 1 checks that 7127c247 is an ancestor of HEAD. Evidence: plan:19, :22, :580; spec line 238. (Base, Variant 1 #8; round2-advocate-2 section 2; round2-advocate-3 section 2.)
- **[C-009] Task 19 (lc18) keeps step 3's pass rule and does not require "step 6 shows nothing written" (no deviation; Necessary if filed).** The brief's phase header (source.md:70) contradicts lc18's own row, which expects a written contract (source.md:72; spec AC-1.5 and AC-1.6, spec lines 321-322). The plan resolves it inline at plan:41 ("Task 19 keeps it"). Residue (LOW wording): the verdict rule at plan:49 ("steps 3 and 4 as replaced for the refusal checks") does not name the Task 19 exception. Evidence: plan:41, :49, :447-467; source.md:70, :72. (Variant 2 #4, round2-advocate-2 N1.)
- **[C-010] Process note: seven requirement-bearing spans of source.md have no coverage-matrix row (lines 16, 23, 30, 36-44, 70, 78, 87).** The reviewer verified the plan implements each (plan:20, 29, 33-49, 54-58, 541), so this is matrix trace debt, not a plan defect. The uncovered spans include source.md:78 and source.md:87, the lines that carry rows 7 and 1, which is why a cross-check built on the matrix never examined them. Remedy: add matrix rows for those spans. Evidence: source.md; coverage-matrix.yaml. (Variant 2 #6, round2-advocate-2 N2.)

### Not checked

- The run-time effect of `--parent-worktree active` (advisory 1); not re-checked on Orca 1.4.245 (p0-live-orca-help.txt:36,69). (Variant 3 #7, Variant 1 advisory 1.)
- The `coordinator_handle` field name (plan:64): `orca orchestration run-create --help` does not document it; the P0 receipt `.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/live-run.json` contains it; not checked on a P1 run. (Invariant probe INV-005.)
- How `/sc:implement` reacts to a failed Task 1 acceptance (it decides how serious row 2 and advisory 5 are). (round2-advocate-3 E4.)
- A second possible source of the lc18 self-match, the worker's own `claude` process if its argv carries the brief text; the argv of an Orca-launched worker could not be seen. (round2-advocate-3 E5.)
- All `cmp`, `pgrep` and `git` results above come from runs on one machine on 2026-11-05 at HEAD 0b443745 (invariant-probe.md, round 2 rebuttals); they were not re-run for this merge.
