# Refactoring Plan: merge of reviewer cards (sc:adversarial Step 4)

## Overview

- Base variant: **V1** (`variant-1-original.md`, reviewer 1, analyzer, sonnet); combined 0.838, selected by score and confirmed by the level-1 tiebreaker (see `base-selection.md`).
- Non-base sources: V2 (`variant-2-original.md`, qa, glm-5.3), V3 (`variant-3-original.md`, refactorer, opus), and `invariant-probe.md`.
- Output of the merge: one consolidated reviewer card with the same schema as the base (findings with id/claim/citation/class/severity/recommendation, verdict, self_audit), each finding annotated with its provenance (`source: R1-Fn` / `R2-Fn` / `R3-Fn` / `INV-nnn`).
- Planned changes: **22** (PC-01 to PC-22): 1 routing header, 8 for the C-001 remedy (including 6 invariant additions), 6 Round-2 concessions, 7 classification fixes and incorporations.
- Debate state: 13/13 points agreed; status BLOCKED_BY_INVARIANTS. Depth was standard (no Round 3), so INV-001, INV-002 and INV-008 are resolved here as required additions to the C-001 remedy, and the merged verdict carries them.
- Taxonomy rule applied throughout (X-001, 90%): an enumerated in-scope item with no task is `drift`; a missing dependency or ordering line is `grounding-gap`; a consistency note carries no class.
- Merged verdict: **FAIL** (one blocking finding, C-001). Remedies are routed off-plan (A-002): the plan file `<id>.md` is not edited from these findings.

## Planned Changes

### PC-01: Merged-card header, verdict and routing note

- Source: diff-analysis A-002; debate A-002 (QUALIFY x3, 90%); A-001 (95%).
- Target in base: top of the card (above `findings:`), plus `verdict:`.
- Integration approach: insert a `routing:` field stating that the plan is advisory-reviewed and not edited from findings (sc-workflow-protocol SKILL.md:60); remedies are delivered by a user re-run of `/sc:workflow` with the remedy text, and no remedy may add a verification-only task (`~/.claude/skills/sc-workflow-protocol/refs/quality-gates.md:22`). Keep `verdict: FAIL`; add `status: partial (BLOCKED_BY_INVARIANTS: INV-001, INV-002, INV-008 resolved as remedy additions PC-03..PC-05)`.
- Rationale: all three advocates accepted A-001 and qualified A-002 in Round 1; unchanged in Round 2.
- Risk: Low. Text-only header.

### PC-02: Replace R1-F1's remedy with the ranked V2 remedy (C-001)

- Source: V2 R2-F1 (evidence and remedy); V1 R1-F1 (finding kept); V3 R3-F1 (concession).
- Target in base: R1-F1 `claim`, `citation`, `recommendation`.
- Integration approach: keep R1-F1's claim and `drift`/`blocking` class; append R2-F1's evidence to the claim and citation (`src/superclaude/commands/implement.md:11` "Lint and tests are extras, never the pass/fail"). Replace the recommendation with: "(1) Task 66 AC: run the smoke selection `uv run pytest tests/ -q -k \"doc or primitive or how_we_work or severity\"`, then the full `make test` once (source.md:49-50); (2) a Constraint line restating the same as reinforcement." Delete the "Add a final task" option. Record the R3-F1 concession: its proposed Task 67 is replaced by the Task 66 AC (this change) and the Task 26 AC (PC-03).
- Rationale: C-001 won by V2 at 95% (unanimous); V1 conceded the final-task half and V3 conceded Task 67 in Round 2 (quality-gates.md:22).
- Risk: Medium. Without PC-04 to PC-09 the remedy is not sufficient (INV-008).

### PC-03: Add the smoke run to Task 26's AC (R3-F1 surviving half)

- Source: V3 R3-F1 (Round 2 rebuttal: "surviving half: smoke pytest on Task 26 AC").
- Target in base: R1-F1 recommendation (new bullet).
- Integration approach: add "Task 26 AC: run the smoke selection after the edit to `src/superclaude/rules/core/changelog_maintenance.md`; `make sync-dev`/`make verify-sync` do not count as verification of that file (PC-21)." Cite tasklist:255-258.
- Rationale: C-001 scoring-matrix entry "V2 (+ Task 26 smoke AC from V3)", 95%; V3 Round 2 new evidence that sync checks never touch Tasks 6 and 26's files.
- Risk: Low on its own; INV-004 (PC-08) shows the smoke selection barely covers this file.

### PC-04: INV-001 (HIGH) — the delivery path must put the AC in the plan

- Source: `invariant-probe.md` INV-001.
- Target in base: R1-F1 recommendation, and the PC-01 `routing:` field.
- Integration approach: add "Delivery: only a `/sc:workflow` re-run that writes the AC into Task 66 (and Task 26) puts the remedy under the executor's gate. An orchestrator instruction alone does not: `/sc:implement` grades each task only against its AC and the plan Constraints (`~/.claude/skills/sc-implement-protocol/refs/qa.md:15`) and will not treat tests as pass/fail (`implement.md:91`)." Remove the Round-2 wording that treats the two delivery paths as equivalent.
- Rationale: blocking invariant from Round 2.5; the debate's agreed remedy (C-001, 95%) assumed equivalence that the probe falsified.
- Risk: Medium. Requires a plan regeneration by the user; mitigation is that PC-06 provides a fallback when it is not done.

### PC-05: INV-002 (HIGH) — record a `make test` baseline and use "no new failures"

- Source: `invariant-probe.md` INV-002.
- Target in base: R1-F1 recommendation.
- Integration approach: add "Before Task 1, record a `make test` baseline to `./artifacts/baseline-make-test.log` (`make test` = `uv run pytest` over all of `tests`, Makefile:13-15, pyproject.toml:108). Word the Task 66 AC as 'no failures beyond the baseline', not 'exit 0', because the plan forbids code changes (tasklist:23) and a pre-existing unrelated failure would halt Task 66 (E-HALT-QA, sc-implement-protocol SKILL.md:33)."
- Rationale: blocking invariant; without it the remedy can halt the run on failures the plan may not fix.
- Risk: Medium. The baseline must come from the same branch head; a baseline recorded after doc edits would hide new failures.

### PC-06: INV-008 (HIGH) — make the remedy sufficient against early halts

- Source: `invariant-probe.md` INV-008.
- Target in base: R1-F1 recommendation (closing sentence) and the merged `verdict` note.
- Integration approach: add "Sufficiency: the Task 66 AC alone does not satisfy source.md:47-50. It also needs PC-04 (delivery), PC-05 (baseline) and PC-07 (evidence log). If any earlier task halts, Task 66 never runs; the post-release orchestrator must then run the smoke selection and `make test` before it commits (source.md:51), compared against the baseline. The markdownlint half of the verification stays per task (tasklist:27); `make lint` is ruff only (Makefile:48-50)."
- Rationale: blocking invariant; the probe listed four falsifiers (early halt, baseline, delivery, evidence).
- Risk: Medium. The orchestrator fallback is outside the plan's executor and relies on the orchestrator following the card.

### PC-07: INV-003 (MEDIUM) — name the evidence logs

- Source: `invariant-probe.md` INV-003.
- Target in base: R1-F1 recommendation (replaces "log to ./artifacts/final-make-test.log").
- Integration approach: state the AC evidence as files: `./artifacts/t26-smoke.log`, `./artifacts/t66-smoke.log`, `./artifacts/t66-make-test.log`, following the Task 6 precedent `./artifacts/t6-tests.log` (tasklist:89). The AC cites the log's result line (`path:line`), because qa.md:9 and :31 reject "tests pass" without one.
- Rationale: V1's original remedy named one log; the probe shows QA needs a citable line per run.
- Risk: Low.

### PC-08: INV-004 (MEDIUM) — the smoke selection does not cover Task 26's file

- Source: `invariant-probe.md` INV-004.
- Target in base: PC-03 bullet in R1-F1.
- Integration approach: add "No test selected by `-k \"doc or primitive or how_we_work or severity\"` reads `src/superclaude/rules/core/changelog_maintenance.md`; the only test that reads it is `tests/unit/test_cli_install.py:172`. Task 26's AC runs that file explicitly (`uv run pytest tests/unit/test_cli_install.py -q`) in addition to the smoke selection, and re-reads the edited file against item B-W1."
- Rationale: without it, the Task 26 smoke AC (PC-03) is near-empty for the file it is meant to check.
- Risk: Low.

### PC-09: INV-006 (MEDIUM) — catch whole-docs test failures before Task 66

- Source: `invariant-probe.md` INV-006.
- Target in base: R1-F1 recommendation (new bullet).
- Integration approach: add "Add the smoke selection to the ACs of the MCP-doc tasks (Tasks 2, 13, 29 and the D02 guide task), because `tests/docs/test_tavily_doc_alignment.py:77-114` and `tests/docs/test_retired_docs_absent.py:37-49` scan all docs; a failure introduced at Task 2 should surface at Task 2, not at Task 66."
- Rationale: smoke-per-item, full-suite-once (INV-007, ADDRESSED) holds only if the item-level smoke runs where docs tests can break.
- Risk: Low. Adds run time to four tasks.

### PC-10: R1-F11 carries no class (concession)

- Source: V1 Round 2 rebuttal ("R1-F11: conceded; a consistency note should not carry a deviation class"); S-002 (75%).
- Target in base: R1-F11.
- Integration approach: move R1-F11 from `findings:` to a new `consistency_notes:` list without `class:`/`severity:`; reword the claim to "tasks 1-66 map to items and gaps 1-70 except B-W22.6 (see the C-003 finding)", which removes the IC contradiction with R1-F9.
- Rationale: S-002 resolved unanimously: non-deviation records are kept but carry no class.
- Risk: Low.

### PC-11: Import R3-F10 as an unclassed consistency note (concession)

- Source: V3 R3-F10; V3 Round 2 rebuttal ("R3-F10 conceded: consistency note, no class").
- Target in base: `consistency_notes:` (new, PC-10).
- Integration approach: add "Tasks 3 and 4 both add a README upgrading.md link (CONSOLIDATED-PLAN.md:248, :579; tasklist:54, :67); suggested split: Task 3 links from installation.md only." No class, no severity.
- Rationale: S-002 (75%); mirrors R1-F11.
- Risk: Low.

### PC-12: R2-F5 goes out of the deviation register (concession)

- Source: V2 R2-F5; V2 Round 2 rebuttal (coverage-matrix.md is a reviewer artifact in the reflect output dir).
- Target in base: new `reviewer_artifact_notes:` list (not under `findings:`).
- Integration approach: add "The coverage matrix states 53/53 where it enumerates 66 deliverables (artifacts/coverage-matrix.md:244 vs :44-109); correct the reflect artifact's count. Not a plan deviation." No class.
- Rationale: V2 conceded beyond the criticism in Round 2; no advocate objected.
- Risk: Low.

### PC-13: R1-F10 reclassed drift, merged with R2-F6's evidence (C-006)

- Source: V1 R1-F10 (concession: "R1-F10 and the B-W22.6 sub-item are drift"); V2 R2-F6.
- Target in base: R1-F10.
- Integration approach: change `class: grounding-gap` to `class: drift`; add R2-F6's evidence to the claim and citation: CONSOLIDATED-PLAN.md:636 (section 6) instructs filing O1-O22 issues and the executor is sent to CONSOLIDATED-PLAN.md by tasklist:19, against source.md:36. Keep V1's wider list (release/tag, report/manifest, [EXTERNAL] steps written never run). Recommendation: one Constraint sentence covering all of them.
- Rationale: C-006 won by V2 at 95%; V1 conceded the class in Round 2.
- Risk: Low.

### PC-14: Split B-W22.6 out of R1-F9 as a drift finding (C-003)

- Source: V1 R1-F9 (concession); V2 R2-F3; V3 R3-F3.
- Target in base: new finding after R1-F9; R1-F9 sub-item list.
- Integration approach: remove B-W22.6 from R1-F9's list. Add a `drift`/`minor` finding: "B-W22 #6 git-standards-protocols.md section-6 pointer has no task; the Goal claims gaps 1-70 fixed" with V3's citations (CONSOLIDATED-PLAN.md:209, :544; docs/developer-guide/git-standards-protocols.md:593-595; tasklist:416-420) and V3's remedy (one-line pointer in Task 46 with a grep AC; the gap-71 rewrite stays deferred). Note V2's imprecision: git-standards-protocols.md is named at tasklist:426 (Task 47) for a different purpose. The remaining R1-F9 sub-items stay `grounding-gap` because the "Read the named item" constraint covers them.
- Rationale: C-003 won by V2+V3 at 90%; V1 dropped its label in Round 2.
- Risk: Low.

### PC-15: Split R1-F8 — B-W12 #6 link omission becomes drift (C-004)

- Source: V1 R1-F8 (Round 2: "B-W12 #6 link omission is drift"); V3 R3-F4; V2 R2-F4.
- Target in base: new finding after R1-F8.
- Integration approach: add a `drift`/`minor` finding: "Task 37 omits B-W12 #6 (link the four new technical notes) and runs before Tasks 43-46" (CONSOLIDATED-PLAN.md:481; tasklist:340-346). Remedy from V3: fold the four-note links into Task 47, which already depends on Task 46 (tasklist:424), with a target-exists AC.
- Rationale: C-004 won by V3 at 90%.
- Risk: Low.

### PC-16: Keep R1-F8's dependency lines as grounding-gap and merge R3-F5 (C-005, concession)

- Source: V1 R1-F8; V3 R3-F5 (Round 2: "reclassed grounding-gap per the X-001 rule"; tasklist:65 cite conceded).
- Target in base: R1-F8.
- Integration approach: keep `grounding-gap`; add R3-F5's forward-link case: Tasks 4 and 13 link to `docs/user-guide/codegraph.md`, created only in Task 17; cite CONSOLIDATED-PLAN.md:249 via the Task 4 item reference at tasklist:67 (not tasklist:65, which is "Depends on: Task 3"), and CONSOLIDATED-PLAN.md:308. Extend the recommendation with V3's "list full dependency sets on 47 and 66". Discard R3-F5's `drift` class.
- Rationale: C-005 won by V1 at 90%, unanimous after V3's Round 2 concession.
- Risk: Low.

### PC-17: R1-F3 remedy uses a per-linking-file AC (C-002)

- Source: V3 R3-F2; V2 R2-F2.
- Target in base: R1-F3 recommendation.
- Integration approach: replace "check all three" with "Link from README.md, commands.md and mcp-servers.md; the AC greps each linking file for the codegraph.md link" (V3 wording). Add the R2-F2 alternative: if a target is dropped, record it in `./artifacts/deviations.md`.
- Rationale: C-002 won by V3 at 85%; V1 moved its vote to V3 in Round 2.
- Risk: Low.

### PC-18: Narrow R1-F5 and absorb R3-F8 (C-007, X-002)

- Source: V1 R1-F5 (Round 2 narrowed); V3 R3-F8.
- Target in base: R1-F5.
- Integration approach: split the claim. (a) The markdownlint pin (`-c`, markdownlint-cli v0.38.0, matching .pre-commit-config.yaml:74-77) is a `necessary` deviation from the spec wording (from R3-F8). (b) The "record pre-existing violations" relaxation clause (tasklist:27) stays minor `drift` against source.md:47-48. Add V1's Round 2 qualification: the executor commits nothing (tasklist:28), but the pre-commit hook runs `markdownlint --fix` on whole staged files (.pre-commit-config.yaml:74-78), so a recorded violation resurfaces at the orchestrator's commit.
- Rationale: C-007 and X-002 won by V1 at 85%, unanimous after V3 switched in Round 2.
- Risk: Low.

### PC-19: Correct R1-F4's citation

- Source: V1 calibration note; V1 Round 2 concession.
- Target in base: R1-F4 `citation`.
- Integration approach: replace tasklist:281 with tasklist:273 for the Task 28 `install --fresh` grep; keep tasklist:143, :146, :265 and add :281 only if it is the Task 29 grep.
- Rationale: conceded in Round 2; calibrator spot check.
- Risk: Low.

### PC-20: Add R3-F6 (Task 42 paraphrases B-W18)

- Source: V3 R3-F6 (unique U-010).
- Target in base: new finding after R1-F4.
- Integration approach: import verbatim with class `drift`/`minor`: the item says replace `git stash` in CONTRIBUTING.md with a worktree (`git worktree add .dev/worktrees/master-check master`) and, for KNOWLEDGE.md, `./update.sh` or `pipx install --force ./`; Task 42 says "safe form" and "editable/update.sh" (CONSOLIDATED-PLAN.md:510-511; tasklist:382, :385). Recommendation: apply the item's wording; AC requires `git worktree add` in CONTRIBUTING.md.
- Rationale: V2 and V1 advocates both steelmanned it in Round 1; no rebuttal against it.
- Risk: Low.

### PC-21: Add R3-F9 with corrected citation (sync checks do not cover core/ or rules/)

- Source: V3 R3-F9 (unique U-012); confirmed by V1 Round 2 ("Makefile grep for core|rules returns nothing").
- Target in base: new finding after R1-F1.
- Integration approach: import with class `grounding-gap`/`minor` and corrected citations: sync-dev Makefile:109, verify-sync Makefile:166; grep for `core|rules` in the Makefile returns nothing. Claim: `make sync-dev`/`make verify-sync` verify nothing about `src/superclaude/core/HOW-WE-WORK.md` (Task 6) or `src/superclaude/rules/core/changelog_maintenance.md` (Task 26). Recommendation: keep the steps (source.md:43 requires them) but do not count them as verification; pair with PC-03 and PC-08. Note that Task 6's `cmp` mirror check (tasklist:88) still holds.
- Rationale: V3 Round 2 narrowed the citation; V1 withdrew its "cite off" objection.
- Risk: Low.

### PC-22: Add R3-F7 (Task 47 adds unrequested index links)

- Source: V3 R3-F7 (unique U-011).
- Target in base: new finding after PC-15's finding.
- Integration approach: import with class `drift`/`minor` (CONSOLIDATED-PLAN.md:487, :199; tasklist:426). Recommendation: keep the links and record them in `./artifacts/deviations.md`, or drop them.
- Rationale: unique contribution, low value, uncontested in debate.
- Risk: Low.

## Changes NOT Being Made

| Item | Source | Reason |
|---|---|---|
| Verification-only Task 67 | V3 R3-F1 | Forbidden by quality-gates.md:22 ("no verification-only task"); conceded by V3 in Round 2 (A-001, 95%). Replaced by the Task 66 and Task 26 ACs (PC-02, PC-03). |
| "Add a final task" half of R1-F1 | V1 R1-F1 | Same gate; conceded by V1 in Round 2. |
| Treat orchestrator instruction and `/sc:workflow` re-run as equivalent delivery | debate Round 2 (V2 rebuttal) | Falsified by INV-001; only a re-run puts the AC under the executor's gate (PC-04). |
| Edit `<id>.md` directly from these findings | all three cards' phrasing | A-002 (90%): sc-workflow-protocol SKILL.md:60 forbids it; remedies route through a re-run. |
| `drift` class for R3-F5 | V3 R3-F5 | Ordering/dependency defects are `grounding-gap` under the X-001 rule; conceded (PC-16). |
| `authorized` class for R1-F11 and R3-F10 | V1, V3 | Consistency notes carry no class (S-002); conceded (PC-10, PC-11). |
| R2-F5 as a plan deviation | V2 R2-F5 | It is about a reviewer artifact; conceded (PC-12). |
| Reclass all of R1-F9 as drift | V1 R1-F9 | Only B-W22.6 lacks a task; the other sub-items are covered by the "Read the named item" constraint, so they remain a grounding-gap risk (PC-14). |
| Withdraw R1-F5 | V3 R3-F8, V2 (no finding) | Narrowed, not withdrawn: the relaxation clause is still drift (C-007, 85%) (PC-18). |
| INV-005 remedy (narrow the `-k doc` selection) | invariant-probe INV-005 | LOW; doctor tests are extra noise only, and changing the spec-given selection would deviate from source.md:49. |
| R2-F1 "do not rely on /sc:implement" wording | V2 R2-F1 | Reconciled by V2 in Round 1: the remedy instructs the executor through the AC rather than bypassing it. |

## Risk Summary

| Change | Risk | Impact if wrong | Mitigation |
|---|---|---|---|
| PC-02 C-001 remedy | Medium | Spec verification (source.md:47-50) still not enforced | PC-04 to PC-09 |
| PC-04 INV-001 delivery | Medium | Remedy given only as an instruction, never graded | Requires a `/sc:workflow` re-run; PC-06 orchestrator fallback |
| PC-05 INV-002 baseline | Medium | Pre-existing failure halts Task 66, or a stale baseline hides new failures | Baseline from the same head, before Task 1, saved as a log |
| PC-06 INV-008 sufficiency | Medium | Early halt skips the full suite | Orchestrator runs smoke + `make test` against the baseline before committing |
| PC-03, PC-07, PC-08, PC-09 | Low | Weak or uncitable evidence; late detection | Named logs; explicit test file for Task 26; smoke on MCP-doc tasks |
| PC-01, PC-10 to PC-22 | Low | Classification or citation errors in the merged card | Each change follows a unanimous debate result or a conceded point |

Overall: 4 Medium, 18 Low. No High-risk change remains once PC-04 to PC-06 are applied; the three HIGH invariants are closed only if the user re-runs `/sc:workflow` with the remedy text.

## Review Status

- Status: auto-approved (non-interactive run; no `--interactive` checkpoint)
- Approved at: 2026-11-03T00:18:24Z
- Base: V1; planned changes: 22; next step: hand base + this plan to merge-executor (Step 5)
