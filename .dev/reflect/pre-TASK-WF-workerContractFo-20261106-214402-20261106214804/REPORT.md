# Reflection report: worker contract follow-ups plan (pre-execution)

- Mode: pre (UC-1). Tier reached: 2. Status: partial (the evidence gate dropped 1 stray citation; no finding was dropped).
- Spec: `.dev/tasks/to-do/TASK-WF-workerContractFo-20261106-214402/source.md`
- Plan: `.dev/tasks/to-do/TASK-WF-workerContractFo-20261106-214402/TASK-WF-workerContractFo-20261106-214402.md`
- Caller: `/sc:workflow` Wave 4 (advisory; the plan is not edited from these findings).
- Coverage: 15 of 15 inferred requirements mapped (coverage_pct_union 1.0); spec has no labelled IDs, so coverage is inference-assisted (coverage_degraded: parsed-sparse).
- Confidence: Tier 1 self 0.90, blind 0.75; Tier 2 cards 0.85 / 0.82 / 0.82 (blind).
- Debate: 3 heterogeneous reviewers (sonnet analyzer, haiku qa, opus refactorer), 2 rounds + invariant probe, convergence 1.0, merge_method adversarial.
- Citations: 73 checked, 72 founded, 1 dropped, 0 inferred in the merged verdict (1 [INFERRED] half-claim noted below).

## Verdict

The plan covers every part of the brief, and every line anchor it cites matches the files. Two planned tests would pass on wrong text (P1), and one wording choice in the brief (M-3) is false for `/sc:workflow` and needs an owner decision before Task 1 runs. None of the findings is a problem in the code under change; all are in the plan's acceptance checks and wording.

Grading rule (adopted in the debate): P1 = a false pass shown under the plan's literal instruction, or a blocker; P2 = needs a reading choice, or a coverage or rule-text defect without a literal false pass; P3 = vacuous, cosmetic or owner note.

## Findings

### P1

**M-1. Task 5's status check passes with the old rule still in place.** Plan :76 asks only that both init-lite texts contain "exited 0"; `init-lite.md:92` ("The run is succeeded when the audit finished, and failed otherwise") and `SKILL.md:61` ("`succeeded` when the audit finished, else `failed`") would still pass; no pin at test_worker_contract.py:787-797 rejects them. Fix: pin the exact phrase "`succeeded` when `superclaude init-lite` exited 0" on the line carrying `worker_status` (SKILL.md:61, where it precedes `artifacts`) and on init-lite.md's Contract line; assert "when the audit finished" absent from those lines; keep the new init-lite.md wording free of "failed tool run" (test_worker_contract.py:792) as well as "on a failed run". Sources: R1-1, INV-001, INV-002.

**M-2. Task 4's test.md pin accepts a clause that lists ignored coverage output.** Plan :66 checks only WC-4, `[]` and no write verb; "lists `htmlcov/`; see WC-4; `[]` when none" passes while contradicting plan :69. Fix: require an exact exclusion phrase (e.g. "paths git ignores are left out") plus WC-4 and `[]` in the clause, mirroring build (test_worker_contract.py:799) and workflow (:808), and add "left out" to `UNATTENDED_EXPECT["test"]["phrases"]` (:349-353) so the removal test (:561-570) covers it. No report-location wording in the pin. Sources: QA-1 (narrowed), INV-003.

### P2

**M-3. The new WC-4 sentence "the report names where those files were written" is false for workflow (owner decision).** Task 1 writes it unconditionally (plan :30, source.md:13); workflow's `report_path` is the plan `<id>.md` (sc-workflow-protocol/refs/return-contract.md:51), which may not be edited after reflect (sc-workflow-protocol/SKILL.md:62). Options: (a) WC-4 states only the exclusion and its reason, and build and test each keep one short local sentence that their report names the ignored files (source.md:19 requires this for test); (b) keep the sentence and name workflow as the exception. Task 1 sets this wording and Tasks 2-4 depend on it, so it must be decided before `/sc:implement`. Sources: R1-2, R3-A1, INV-005, INV-006.

**M-4. The plan's search for other WC-4 copies skips the design spec the brief names.** source.md:14 names "a spec copy"; plan :30 searches only tests/ and plugins/; `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:72` restates WC-4. Fix: record that the planning spec (header :3, "Planning only") stays unchanged; search src/, plugins/, tests/ and that spec, excluding specs/history/, .dev/tasks/done/, .dev/orca-command-refactor/decisions/ and .dev/reflect/; record the decision in progress.md or the commit body. Sources: R3-1, INV-010.

**M-5. The WC-4 assertion can pass on a misplaced sentence.** `_contract()` returns the whole file (test_worker_contract.py:383-394). Fix: assert on the WC-4 span only ("- **WC-4." at WORKER-CONTRACT.md:31 to "- **WC-8." at :38) and add the new key phrase to `RULE_PHRASES["WC-4"]` (:102-108) so `test_rule_check_fails_when_rule_removed` (:586-593) covers it. Sources: R1-4, R3-3, INV-008.

**M-6. The new global exclusion conflicts with init-lite's unconditional `artifacts` list.** init-lite.md:92 and SKILL.md:61 list every printed `Scaffold:` file; `--project-root` accepts any directory (init_lite.py:294-298, :338), so a scaffold path can be outside the repository or ignored. Fix: one WC-4 clause that the exclusion applies to every command's `artifacts` list. [INFERRED] The same shape exists for index-repo's fixed `PROJECT_INDEX.json` (index-repo.md:189); nothing shows that file is ignored. Sources: INV-007, R3-A3.

### P3

- **M-7.** Task 1 acceptance criterion 3 is vacuous: the write-verb scan covers only skills, commands and agents (test_worker_contract.py:1054-1058). Drop it or reword it to "the new WC-4 sentence holds no literal `git add`"; M-5's pins are the real guard. Sources: R1-3, QA-2, R3-2, INV-009.
- **M-8.** build.md:104 still restates parts of WC-4 after Task 3; keep local text only where M-3's decision needs it. Source: R3-4.
- **M-9.** return-contract.md never names WORKER-CONTRACT.md; use the input-parse.md:16 form "`~/.claude/WORKER-CONTRACT.md` (rule WC-4)", and add no backticked `artifacts` above return-contract.md:52, or `_artifacts_clause` (test_worker_contract.py:769-774) reads the wrong line. Sources: R3-5, INV-004.
- **M-10.** "`[]` when nothing else was written" is wrong for a `--coverage` run that wrote only ignored files (.gitignore:37, :40, :44, :48); say "nothing else listable". Source: INV-011.
- **M-11.** State that the tool's exit code is the only basis for init-lite's `succeeded` (SKILL.md:63 allows non-CLI work). The mapping agrees with the CLI: `--dry-run` exits 0 (init_lite.py:348-352); a report-write refusal raises ClickException (:247-262); a failed scaffold write raises a raw OSError (:278), so `reason` carries a traceback. Sources: R1-5, INV-015, INV-016.

### Tier 1 notes (P3)

- RF-1: the developer guide restates WC-4 `artifacts` (docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:1002); not pinned; optional one-clause update.
- RF-2: `plugins/superclaude/commands/test.md` has no Unattended section and stays unchanged, like build.md.
- RF-3: plan :81's `./artifacts/t5-checks.txt` means the package's artifacts folder.

## Advisory (non-gating)

- R3-A2: WC-9 also stages `report_path`; a report under an ignored path is outside this brief.

## Delivery

`/sc:workflow` never edits the plan from these findings. M-3 needs the owner's choice; the other P1 and P2 fixes need no decision and can be applied by revising the plan before `/sc:implement` or in-task.

## Grounding Gaps

None. The one dropped citation was a stray duplicate (M-1 cited test_worker_contract.py:102-108, which supports M-5, not M-1).

## Inferred requirements (Pass 2)

15 rows, all quote-pinned to source.md and all matched: see `artifacts/coverage-matrix.yaml`. None dropped by the evidence gate.

## Artifacts

audit.log; artifacts/{input-snapshot.yaml, grounding.txt, coverage-matrix.yaml, calibration.yaml, tier_decision.yaml, evidence-validation.md}; reflection-card.yaml; reviewer-briefs/; reviewer-cards/; adversarial/ (diff-analysis, rounds/, invariant-probe, debate-transcript, base-selection, refactor-plan, merged-verdict.yaml, merge-log, return-contract.yaml).
