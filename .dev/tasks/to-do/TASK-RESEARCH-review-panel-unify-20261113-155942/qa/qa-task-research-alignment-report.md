# QA Report: Task-Research Alignment

**QA mode:** task-integrity
**Lens:** task-research-alignment
**Task file:** `.dev/tasks/to-do/TASK-RESEARCH-review-panel-unify-20261113-155942/TASK-RESEARCH-review-panel-unify-20261113-155942.md` (578 lines, about 440 KB)
**Research inputs:** `research/research-notes.md`, `research/scope/00-05`, `BUILD-REQUEST.md`
**Date:** 2026-11-13
**Stance:** adversarial (assume dropped or misrepresented research findings)

---

## 1. What was checked

- Read in full: `research/research-notes.md`; the "Suggested Phase 2 assignments", "Gaps and questions" and relevant body sections of scope slices 01-05 (slice 01 :150-214, slice 02 :150-239, slice 03 :175-233, slice 04 :215-355, slice 05 :105-191); slice 01 header :1-12.
- Task file: headings and every checklist line; the full text of Phase 1 (:163-167) and Phase 2 agents 1-3 (:182-186); topic, file list and questions of agents 4-12 (:188-204); web items W1-W4 (:260-266); synthesis items (:278-302); adversarial step (:290-294); anti-omission inputs (:422-428); gap compilation (:250); Task Log (:486-578).
- Path spot-checks against the working tree, `origin/master`, local `master` and commit `4a22d74213f93837d00c2c314075dd967b9a98e3` (`ls`, `git cat-file -e`, `git ls-tree`, `git merge-base --is-ancestor`).

## 2. Coverage table (planned item -> covering task item -> result)

PASS = an item's embedded prompt names the topic and its files. PARTIAL = topic present but part of the slice's request is not named (graded minor unless stated). FAIL = no covering item.

### 2.1 Slice 01 (P2-1 .. P2-9)

| Planned item | Covering task item (line) | Result |
|---|---|---|
| P2-1 parser and merge drop behaviour, master vs this branch | Agent 1 Q3 (:182), Agent 2 Q1-Q2 (:184) | PASS (master-vs-branch diff of `findings.py`/`ledger.py` not asked; the 3 branch commits do not touch them, so no loss) |
| P2-2 which `review` subcommands exist on master, on 4a22d742, on this branch | Agent 9 Q4, Q7 (:198) | PARTIAL: 4a22d742 not compared (minor m-1); and the `git show master:` ref is wrong (blocking B-2) |
| P2-3 reflect findings block vs findings-v1 incl. `coverage_rows`, calibration fields | Agent 1 Q1, Q5, Q8 (:182) | PARTIAL: `coverage_rows` never named (minor m-2) |
| P2-4 generic reviewer runner and identity, S-ID spike | Agent 4 Q6 (:188) | PASS (`s-id-results.md` not in the file list; reached via slice 04 s2, minor m-3) |
| P2-5 brief unification and `{{SOURCE}}` | Agent 6 Q1-Q7 (:192) | PASS |
| P2-6 panel config evidence vs packaged tiers (HANDOFF:240, CR:363-371) | Agent 4 Q5 + hand-off 5.3 (:188); Agent 11 reads CR :363-371, :428 (:202) | PASS |
| P2-7 blocking/verdict policy | Agent 5 Q2, Q6-Q8 (:190); Agent 2 Q5 (:184) | PASS |
| P2-8 regression suite from the study | Agent 11 Q1 (:202) | PASS |
| P2-9 audits A and D as built-in checks | Agent 8 Q5 (:196); Agent 2 reads audit2/anch/bok (:184) | PASS |

### 2.2 Slice 02 (7 assignments)

| Planned item | Covering task item (line) | Result |
|---|---|---|
| 1 finding-contract unification (findings.py :205-320, card_convert :240-517, D1 limit policy) | Agent 1 (:182) | PASS |
| 2 ledger on v2 (D2, D3, D4, D16, `annotate`, pinned tests) | Agent 2 Q1, Q3, Q6 (:184) | PASS |
| 3 clustering merge (cluster.py :184-447, section-empty, D7) | Agent 3 (:186) | PASS |
| 4 panel resolution policy (D11, D12, tier update, reflect profile, identity) | Agent 4 (:188) | PASS |
| 5 CLI surface and callers incl. `scripts/reflect_shadow_exit.py`, `scripts/reflect_stage0a_replay.py` as callers | Agent 9 (:198) | PARTIAL: the D14 Grep covers only `src/superclaude/{skills,commands,core}`; reflect scripts as CLI callers not named (minor m-5) |
| 6 telemetry convergence (D15, merge/resolve records, manifest attempts) | Agent 8 Q1-Q3, Q7 (:196) | PASS |
| 7 test migration plan | Agent 12 (:204) | PASS |

### 2.3 Slice 03 (7 assignments)

| Planned item | Covering task item (line) | Result |
|---|---|---|
| 1 blocking rule per lens (MEDIUM-drift, two-word label gap) | Agent 5 Q1 (:190) | PASS |
| 2 calibrator as a panel role, `calibration_coverage` values | Agent 5 Q3-Q5 (:190) | PASS |
| 3 merge path: debate vs script | Agent 7 Q1-Q2 (:194) | PASS |
| 4 why Stage 2 fails today (per-run classification) | Agent 11 Q3 (:202); Agent 7 Q7 (:194) | PASS |
| 5 driving-document delivery (D8), recorded reviewer briefs | Agent 6 (:192) | PASS |
| 6 UC-2 `reflect-post` readiness incl. recorded post-* cards | Agent 7 Q6 (:194) | PARTIAL: recorded post-* cards not named (minor m-6) |
| 7 test-pin migration (C1, C6 vs HEAD) | Agent 12 Q5, Q7 (:204) | PASS |

### 2.4 Slice 04 (10 assignments)

| Planned item | Covering task item (line) | Result |
|---|---|---|
| 1 input contract per consumer | Agent 6 Q2, Q5 (:192) | PASS |
| 2 identity and dispatch (raw-id, swarm `T2Model0N`, Agent-tool class, parity after 9874d63fb) | Agent 4 Q6 (:188) | PARTIAL: swarm-lens `T2Model0N` dispatch mode not named (minor m-4) |
| 3 merge code on master, >200-char anchor drop | Agent 2 Q2 (:184); Agent 1 Q3 (:182) | PASS |
| 4 finding format unification + finding-level T-9 checker (NOT BUILT) | Agent 1 (:182) | PARTIAL: T-9 checker not named (minor m-7; reaches Section 8 via slice 04 in synth-06) |
| 5 shadow-run exit diagnosis 08-15 | Agent 11 Q3, Agent 7 Q7 | PASS |
| 6 blind GT scoring of the 15 combo runs (needs owner spend approval) | Agent 11 Q4 records "not approved" | PASS (correctly not run) |
| 7 generic shadow/manifest harness, overlap with `cli/eval`, `eval_runner.py`, `ab_test_workflows.py` | Agent 11 Q2 (:202) | PASS |
| 8 calibration (0/689, card-level output, id matching) | Agent 5 Q5 (:190) | PASS (`F1` vs `R1-F1` id mismatch not named; minor) |
| 9 orchestrator role (speed, dispatch collapse, compliance; prose vs code) | Agent 11 Q4, Agent 4 Q6 | PARTIAL: "orchestrator model policy / move dispatch from prose to code" not asked (minor m-17) |
| 10 cost/worth (H-A): E2 ceiling ~2.5/14, "sonnet alone most catches per token", T2 cost 37/38 escalate, fewer reviewers vs fix rubric (O-8) | none | **FAIL (blocking B-4)** |

### 2.5 Slice 05 (9 assignments)

| Planned item | Covering task item (line) | Result |
|---|---|---|
| 1 finding contract v3 design input | Agent 1 (:182) | PASS (but path to `pr_submit/models.py` is wrong: B-3) |
| 2 ledger generalization (verify-only, PROFILES, moving path+line) | Agent 2 Q4 (:184), Agent 3 Q8 (:186) | PASS |
| 3 panel template lens/role binding, `--kind` | Agent 4 Q7 (:188) | PASS |
| 4 telemetry strata and kinds; "strata are never pooled" (owner decision D3) | Agent 8 Q2 (:196) | PARTIAL: the "never pooled" rule not named (minor m-11) |
| 5 rf-qa call-site census | Agent 10 Q3 (:200) | PASS |
| 6 pr-submit integration seam | Agent 10 Q1 (:200) | PASS (wrong path, B-3) |
| 7 reflect as tasklist reviewer (Tier 2 escalation by default) | Agent 9 Q6 (:198) | PASS |
| 8 spec-review hook for brainstorm/design | Agent 9 Q2 (:198) | PASS |
| 9 experiment bundle verdicts (FINAL-REPORT, `builds/*/repo-files/docs/designs/`, variants incl. minfix) | Agent 11 Q6 (:202) | PARTIAL: design docs and variant list not named; `sc-diffgate` / `sc-fix-audit` bodies never read (Agent 9 lists names only) (minor m-8) |

### 2.6 Research-notes Phase 2 agents 1-12

All twelve rows of `research-notes.md` SUGGESTED_PHASES (:118-129) map one-to-one onto task items :182-204 with the same output file names, investigation types and core files. PASS, except the path defects B-1, B-2, B-3 inherited from or introduced against the notes.

### 2.7 Web topics

| Planned topic | Task item | Result |
|---|---|---|
| W1 panel aggregation | :260 (`web-01-panel-aggregation.md`, reads research 02 and 05) | PASS |
| W2 severity harmonization | :262 (`web-02-...`, reads 01 and 10) | PASS |
| W3 judge calibration | :264 (`web-03-...`, reads 05 and 11) | PASS |
| W4 finding fingerprinting | :266 (`web-04-...`, reads 03 and 10) | PASS |

### 2.8 Synthesis files and required content (a)-(e)

| Planned synth file (notes :146-152) | Task item | Carries | Inputs vs plan | Result |
|---|---|---|---|---|
| synth-01 S1-S2 | :278 | (a) 18-row matrix, 9 columns | research 01-12 + all six slices + gaps log (matches) | PASS |
| synth-02 S3-S4 | :280 | D1-D16 rows, (e) blockers | research + web + gaps + slices 02 s5, 05 s3-4 (superset) | PASS |
| synth-03 S5 | :282 | external | web 01-04 (matches) | PASS |
| synth-04 S6 | :284 | (c) C01-C13 + "any further" | research + web + gaps + SOLUTION_RESEARCH; adversarial results written back by :290-292 | PASS (enumerated list omits cost/panel size: B-4; invalid-block policy: m-10) |
| synth-05 S7 | :298 | (d) core + module tables, (e) exposure list | synth-04 + adversarial outputs + research + web (matches) | PASS |
| synth-06 S8 | :302 | (b) inventory, M1-M4, gate list, branch options with the ref-naming constraint, no roadmap | synth-04, 05, 02, gaps, research, all six slices (matches) | PASS |
| synth-07 S9-S10 | :286 | open questions, evidence trail | gaps + research/web Gaps + AMBIGUITIES (matches) | PASS (ordering note m-14) |

### 2.9 Adversarial step

| Planned | Task item | Result |
|---|---|---|
| for each UNDECIDED-BY-EVIDENCE conflict: proposal-a/b in `reviews/adversarial/<slug>/`, `/sc:adversarial --compare a b --depth standard --focus correctness,risk,test-coverage --output <slug>/`, write back before synth-05; "no adversarial run needed" path | :290 (index + sub-checklist template, exact args), :292 (process in order), :294 (gate: no `pending` marker before synth-05) | PASS |

## 3. Fabrication and path check

No task item introduces a topic, file or requirement absent from the research inputs: every file list traces to `research-notes.md` EXISTING_FILES or a slice, and every question traces to a slice assignment, a slice gap or SOLUTION_RESEARCH. No fabricated item found.

Path spot-check (about 90 paths checked; all exist except the ones below):

| Cited path / ref | Task lines | Actual | Origin of the error |
|---|---|---|---|
| `git show 4a22d742...:.dev/eval-workspaces/tasklist-review-panel/<path>` for `manifest.md`, `tools/run-reviewer.sh`, `COMBO-REPORT.md`, `PILOT-REPORT.md`, `combos/SPEC.md`, `analysis/final-table.py`, `analysis/audits/audit-D/summary.md`, `tools/tmp-scripts/judge-one.sh` | 118, 167, 182-204 (all 12 agents), 224, 240, 372, 406 | `fatal: path ... does not exist`. The files are under `.dev/eval-workspaces/tasklist-review-panel/20261111-a1/<path>` (each confirmed with `git cat-file -e`; `20261111-a1/manifest.md` has 16 lines). Only `HANDOFF-review-panel-unification.md` is at the top level. | `research-notes.md:32` dropped the `20261111-a1/` segment that slice 01's header (:5 "relative to `.dev/eval-workspaces/tasklist-review-panel/20261111-a1/`") states. **Blocking B-1.** |
| `git show master:src/superclaude/cli/review/__init__.py` | 198 (Agent 9 Q7) | Local `master` is `80f361804` (2026-11-05, #402). It has no `src/superclaude/cli/review/` and does not contain the #346 commit `9163bd1c7`. `origin/master` = `d2d8a2d16` (#519) has both. | Builder. Phase 1 (:167) runs `git fetch origin`, which updates `origin/master` only. **Blocking B-2.** |
| `src/superclaude/cli/pr_submit/{models.py,reviewers.py,fsm.py,severity_router.py}` | 122, 182 (Agent 1), 200 (Agent 10), 372, 408 (fidelity 4) | No such directory. The package is `src/superclaude/pr_submit/` (`models.py`, `reviewers.py`, `fsm.py`, `severity_router.py` all present). | `research-notes.md:68` and slice 05. **Blocking B-3.** |
| "the twelve files in `tests/cli/reflect/`" | 194 (Agent 7), 204 (Agent 12) | 39 `test_*.py` files | `research-notes.md:46`. Agent 12 collects the whole directory, so its count corrects itself; Agent 7's wording misleads. Minor m-12. |

## 4. Research caveats

| Caveat from research | Where the task keeps it | Result |
|---|---|---|
| Stale line numbers (D7 `telemetry.py:22`, D11 `panel.py:536-543`, D12 `panel.py:485-494`) | Key Constraints :131; Agent 3 cites `telemetry.py:22`; Agent 4 cites :536-543, :485-494; synth-01/02/04/05/06 "hand-off line numbers for D7/D11/D12" rule | PASS |
| [CODE-CONTRADICTED] items (variants also in `~/.claude/`, merge_round docstring vs D2, UC-2 reviewer, 6- vs 5-dimension calibrator) | :131; Task Log row 7 (:504); Agent 2 Q1; Agent 5 Q3; every synth prompt | PASS |
| `source.md` not committed (copied at run time from another worktree) | Agent 11 Q1 (:202); Agent 6 reads `run-reviewer.sh:10` (:192) | PASS |
| Only audits A and D have summaries; audit D names 3 flips; once-found issue is GT1 (B6) | :131; Agent 8 (:196); Agent 2 Q2; Agent 11 Q5; synth rules | PASS |
| HEAD-relative pins C1/C6 | Agent 7 Q5 (:194); Agent 12 Q5 (:204); synth-06 8.3 (:302) | PASS |
| Installed-only experiment variants; bundle has no valid-success verdict | :120, :131; Agent 2 Q7; Agent 9; Agent 11 Q6; Task Log row 1 | PASS |
| Model evidence is time-bound (valid era from 2026-11-12 13:02, one gateway) | every Phase 2 prompt "date-stamp"; Agent 4 Q5; synth-04 | PASS |
| `expected_model` overwritten by the fallback; Bash allowed under bypassPermissions | Agent 4 Q6; Agent 6 Q6 | PASS |
| E2 citation base is `20261111-a1/` (slice 01 header) | not kept | **FAIL (B-1)** |
| E3 lives on `origin/master`, not the stale local `master` | not kept (Agent 9 uses `master:`) | **FAIL (B-2)** |

## 5. Dependencies and ordering

| Research dependency | Task ordering | Result |
|---|---|---|
| Adversarial step after synth-04 and before synth-05 | synth-04 :284 -> :290, :292, :294 (hard gate on `pending`) -> synth-05 :298 | PASS |
| synth-05 reads synth-04 and adversarial outputs | :298 reads synth-04 first plus `reviews/adversarial/` | PASS |
| synth-06 after synth-04 and synth-05 | :302 after :298, reads synth-04, synth-05, synth-02 | PASS |
| Web research before the synth files that read it | Phase 4 (:260-270) before Phase 5 | PASS |
| Anti-omission inputs include the six scope slices (BUILD-REQUEST:69) | 00 in :422, 01+02 in :424, 03 in :426, 04+05 in :428 | PASS |
| synth-07 Evidence Trail lists all produced files | synth-07 (:286) runs in the parallel batch with synth-01..04, before the debates and synth-05/06, so its Globs of `synthesis/` and `reviews/` cannot list them, and a failed debate's open question (:294) cannot reach Section 9 | PARTIAL (minor m-14) |
| Gap log covers slice gaps | :250 reads research files, QA reports and AMBIGUITIES, not the slices' Gaps sections; anti-omission gate reads the slices | PARTIAL (minor m-15) |

## 6. Findings

### Blocking

**B-1. Every E2 path is missing the `20261111-a1/` folder.** Task lines 118, 167, 182-204, 224, 240, 372, 406 read E2 files as `git show 4a22d74213f93837d00c2c314075dd967b9a98e3:.dev/eval-workspaces/tasklist-review-panel/<path>`. At that commit these paths do not exist; the files are under `.../tasklist-review-panel/20261111-a1/<path>` (checked for manifest, runner, judge, COMBO, PILOT, SPEC, final-table, audit-D summary). Slice 01 states the base in its header (:5); `research-notes.md:32` dropped it and the builder copied the error. Impact: the Phase 1 check (:167) fails by construction ("expected: the 16-line study manifest"), and its fallback tells every Phase 2 agent to mark E2 reads [UNVERIFIED]. That would strip the E2 evidence (65 vs 38 blocking result, 49 lost blockers, 156/665 source-blind runs, audits A and D) from the overlap matrix, conflict log and value inventory. Fix: replace `.dev/eval-workspaces/tasklist-review-panel/<path>` with `.dev/eval-workspaces/tasklist-review-panel/20261111-a1/<path>` in all 18 lines, keep `HANDOFF-review-panel-unification.md` at the top level, and change the `git ls-tree` targets in Agents 2, 6 and 8 the same way.

**B-2. Agent 9 compares against a stale local `master`.** Line 198, Q7: `git show master:src/superclaude/cli/review/__init__.py`. Local `master` is `80f361804` (2026-11-05); it has no `src/superclaude/cli/review/` and does not contain #346 (`9163bd1c7`). `origin/master` is `d2d8a2d16` and has both. The agent would conclude the E3 review CLI does not exist on master, which is wrong and feeds the overlap matrix and D13/D14. Fix: use `origin/master` (refreshed by the Phase 1 fetch) and say once in Key Constraints that "master" in this task means `origin/master`.

**B-3. `src/superclaude/cli/pr_submit/` does not exist.** Lines 122, 182 (Agent 1), 200 (Agent 10), 372 and 408 (fidelity agent 4) name `src/superclaude/cli/pr_submit/{models.py,reviewers.py,fsm.py,severity_router.py}`. The package is `src/superclaude/pr_submit/`. The error comes from `research-notes.md:68` and slice 05. Impact: the PR-review seam and the `Finding` schema in the (e) exposure list could be reported as missing, and fidelity agent 4 would check report citations against a path that does not exist. Fix: replace `src/superclaude/cli/pr_submit/` with `src/superclaude/pr_submit/` in all five lines.

**B-4. Slice 04 assignment 10 (cost and worth, H-A) has no covering item.** Slice 04 :333 asks to combine the E2 ceiling (about 2.5 of 14 defects), "sonnet alone most catches per token", and the T2 cost (37 of 38 pre runs escalate, 34 from parsed-sparse) to decide whether the unified panel should default to fewer reviewers or fix the rubric (O-8). No Phase 2 question asks this; `H-A`, `O-8` and `37 of 38` appear nowhere in the task. The synth-04 conflict list C01-C13 (:284) has no panel-size or cost conflict. synth-04 and synth-05 do not read slice 04, so the question cannot reach the conflict log or the architecture through any other route. Pieces exist (Agent 6 Q2 parsed-sparse; Agent 11 Q5 E2 headline), but nobody is asked to decide. Fix: add a question to Agent 11 (or Agent 5): "cost and worth of Tier 2: E2 ceiling and per-token result, the 37 of 38 escalation rate, MR's 3-reviewer cap and the T2 >= T1 + 15 pp rule, and O-8 (fix the rubric) as the cheaper lever; give design input for the default panel size", and add `C14 panel size and cost (panel-size-cost)` to the synth-04 conflict list.

### Minor (notes; do not fail the review)

- m-1 Slice 01 P2-2: the subcommand surface at 4a22d742 is not compared (Agent 9 compares this branch with master only).
- m-2 Slice 01 P2-3: `coverage_rows` and reflect calibration fields are not named in Agent 1.
- m-3 `s-id-results.md` is not in Agent 4's file list (its facts reach Agent 4 through slice 04 s2).
- m-4 Slice 04 #2: the swarm-lens `T2Model0N` dispatch mode is not named in Agent 4.
- m-5 Slice 02 #5: reflect scripts (`reflect_stage0a_replay.py`, `reflect_shadow_exit.py`) as `superclaude review` callers fall outside Agent 9's D14 Grep (`src/` only).
- m-6 Slice 03 #6: recorded `post-*` reviewer cards are not named in Agent 7 Q6.
- m-7 Slice 04 #4: the finding-level T-9 checker (NOT BUILT) is not named; it reaches the inventory only through slice 04 in synth-06.
- m-8 Slice 05 #9: bundle design docs (`builds/*/repo-files/docs/designs/`) and the variant list (incl. minfix) are not named; the `sc-diffgate` and `sc-fix-audit` bodies are never read (Agent 9 lists names and descriptions only).
- m-9 Slice 03 s4: the Qwen/kimi/deepseek removal from §7.1, `reviewer-spec.md:97` and the §11.3 class list, and the "tier file as the only model source vs `ANTHROPIC_DEFAULT_*`" question are not named.
- m-10 Slice 01 s4: invalid-block handling (E2 full rerun vs reflect block-only re-ask) is not in the enumerated C01-C13 list; it reaches Agent 4 only through slice 01 s4.
- m-11 Slice 05 #4: "strata are never pooled" (owner decision D3) is not named in Agent 8 Q2.
- m-12 Agent 7 (:194) says "the twelve files in `tests/cli/reflect/`"; there are 39 test files (count from `research-notes.md:46`).
- m-13 `evidence-validator` (slice 05 1D, a shared grounding-gate candidate used by reflect, pr-submit and troubleshoot) is read by no Phase 2 agent; synth-05 has only a "citation checks" core row.
- m-14 synth-07 (:286) runs before the debates and synth-05/06, so its Evidence Trail cannot list them and a failed-debate open question cannot reach Section 9. Moving synth-07 after :302, or having the assembler add the missing entries, fixes it.
- m-15 The gap log (:250) does not read the slices' Gaps sections; only the anti-omission gate covers them.
- m-16 Slice 01 s3: the E2 sandbox snapshot vs reflect `--isolate-reviewers` comparison is not named (inventory reaches it through slice 01 in synth-06).
- m-17 Slice 04 #9: "orchestrator model policy" and "move dispatch from prose into code" are not asked (speed and collapse evidence is covered).

## 7. Summary

- Planned items checked: 42 slice assignments, 12 research-notes agents, 4 web topics, 7 synth files, 1 adversarial step, 10 caveats, 7 ordering rules.
- Of the 42 slice assignments: 32 PASS, 9 PARTIAL (minor), 1 FAIL (B-4). Web topics, synth files and the adversarial step all PASS. There are 3 path/ref defects (B-1, B-2, B-3), each of which would lead to a wrong or lost conclusion. No fabricated item was found.
- B-1 and B-3 come from `research-notes.md` and were copied into the task; B-2 is the builder's own. All four blocking fixes are text replacements or one added question plus one added conflict row.

VERDICT: FAIL



