f4d6930775c1f9b4e8fe0ba8700ac2b02e6fcbbf
Review one task for spec compliance.

Task brief: Task 8 of the plan .dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/TASK-WF-blockerStage3-20261116-030158.md (AC ids T8.AC1 to T8.AC3 in source order).
## Task 8: Re-pin the audit tests for the QA agents

Depends on: Task 4, Task 5

Update `tests/audit/test_nfr_conv_9_zero_trust.py` (byte-exact PASS and FAIL bullets of `src/superclaude/agents/rf-qa.md` and its `.claude/` mirror) to the reworded "any blocking gap" bullets on both surfaces; its `BLOCKING_SEVERITIES = frozenset({"CRITICAL", "IMPORTANT"})` stays, with a one-line comment that it is the label scale of that test's sample-report scorer and does not define the grade, because the scorer reads labels in a fixture report. Update `tests/audit/test_invariant_preservation_NFR_6_through_10.py` (it imports `FAIL_BULLET` and `PASS_BULLET` from the first module) in the same change. Re-pin `tests/audit/test_severity_floor_unweakened.py` (the SHA-256 of the `## Critical Rules` block of `rf-qa-qualitative.md` and its mirror, `RULE_6_TEXT` verbatim, and the 10-line window hash, which must be unchanged because Task 5 does not touch that window) to the Task 5 text. The block hash changes because the block holds the rewritten Rule 6, the rewritten Rule 9 and the L3 text beside rule 10; the rewritten verdict pairs lie outside that block and are not part of the hash. Leave `tests/audit/test_dnsp_all_agents_fail_bypass.py` unchanged unless the cap text moved.

Acceptance criteria:
- `uv run pytest tests/audit -v` passes.
- The re-pinned hash in `test_severity_floor_unweakened.py` matches the new `## Critical Rules` block on both the source and the mirror surface after `make sync-dev`, and its softening-token test passes with the new Rule 6 and Rule 9 text.
- `test_dnsp_all_agents_fail_bypass.py` passes without an edit.

Global constraints:
## Constraints

- Spec and cuts: the merged spec `02-brainstorm/merged-requirements.md` inside the program folder `BLOCKER-CLASSIFICATION-PROGRAM-20261115` (found by that folder name under the repository's task folder). This plan calls that folder PF and the spec file the spec. Section numbers, requirement ids (REQ-nn), loop changes (L1 to L6), guardrails (GR1 to GR12), revert triggers (RT1 to RT8) and owner decisions (OD1 to OD17) refer to the spec. The cuts that shaped this plan are in `cuts-debate/final-cuts.md` in PF (rows C1 to C14, the S3 table of its section (b), the cross-package facts of its section (c)); where that file and the spec disagree about scope, the cuts file wins. Evidence of earlier stages is read from their packages by package id (the ids are in the stage ledger `stage-requests/README.md` in PF), found by that folder name in the to-do or done subfolder of the repository task folder. The stage 0 package is `TASK-WF-blockerStage0-20261116-021044` and the stage 1 package `TASK-WF-blockerStage1-20261116-030154`. The stage 2 package is withdrawn: its one survivor, the `/sc:implement` print, is task 2 of the stage 1 package.
- One package, one stage. This is stage 3 of the packages that remain (stage 0, stage 1, this one, stage 4). It changes the live review rule. Entry check, read from files and not from memory: the stage 0 package's `./artifacts/stage0c-regrade.md` exists; the stage 1 package is done (it is in the done subfolder of the repository task folder, or it is in the to-do subfolder with a `complete` line for every task in its `progress.md` and a latest `FINAL:` line that reads `FINAL: pass`); the stage 0 errata task has reworded the spec's RT1 row to read "any real blocker found in a Medium list" (`grep -c -F "any real blocker found in a Medium list"` over the spec prints 1 or more; Task 10 quotes it); the stage 3 row of `stage-requests/README.md` in PF holds the owner's go with a date (the go is a chat message recorded there by the session that received it; no hash and no line ruling are part of it). Task 1 runs this check before it creates any file under `src/` or `tests/`, and Task 2 runs it again before the first rule-file edit. A failed check stops the task before any edit and halts the run for the owner. While the check fails, no fix pass, repair, retry or adviser step edits a file under `src/`, `tests/` or `plugins/`, and the acceptance lines of that task that describe the edit do not apply. No task edits the ledger row. Stage 4 starts only after the owner has read the first five runs' Medium lists after the switch and RT1 did not trip (the stage 3 note says how), and the owner's go in chat.
- Limit of what this package shows. The stage 0 regrade is a lower bound: it regrades findings that were already supplied and cannot measure whether a reviewer would have found a defect. The stage 0 result, as its control test supports it, is only that the new text does not change grades on a table already filed as blocking (310 of 318 stay blocking under both texts, 82 of 82 panel blockers kept); both arms carried the old rule through the same hook, so no task here and no sentence of the Task 10 note cites that regrade as evidence that the new text works. No seeded-defect experiment is run here (the earlier one was confounded: both arms carried the old output style through the SubagentStart hook). What covers discovery is RT1 (spec section 13.2) read by the owner on the first five runs' Medium lists and one small planted-defect check run as part of the live RT1 audit after the switch; both go into the Task 10 note and neither is a build task.
- Owner decisions use the spec's recommendations unless the owner changes them, and none of them is converted into an owner answer here: OD1 no new skill folder, the S1 to S5 bullets of `pragmatic.md` are the one source; OD2 the Medium offer once per run plus at any escalation halt; OD9 reviewer-named consumer; OD11 replace label-max merging, staged (this stage the three agents; the rest is stage 4); OD14 a finding with an unknown consumer keeps the reviewer's label (no deferral); OD16 option (b) for Rule 6 of `rf-qa-qualitative.md`. OD3 (finding text leaving the machine) is open and no task depends on its answer; OD4 stands (no classifier in version 1).
- Retired carriers are not edited. The owner is retiring `/sc:task` and the task-builder: no task here edits `src/superclaude/skills/task/`, `src/superclaude/skills/task-builder/` or `src/superclaude/agents/rf-task-builder.md`. Tests that exist only to pin those files are not re-pinned here; where one test pins both a retired and an active carrier, only the active carrier's part is re-pinned.
- Follow-up list. The list of minors is the reviewers' own `follow-up candidates` section plus each task's `notes.md`; no list file, codec, sweep or registry is built. The stage 1 package prints that list at the end of `/sc:implement` (one paragraph titled "Follow-up print (record and print only).", command `superclaude review safety-scan`). This package edits no `sc-implement-protocol` file, no plugin file and no `refs/qa.md`. The once-per-run offer question stays with the top-level session through the output style (the Medium rule of `pragmatic.md`, changed from per loop to per run in Task 2), so no command gains a question.
- Plugin surface. IronClaude is installed from the Coder template or from a clone plus `superclaude install`, not as a plugin, so this package edits nothing under `plugins/` and creates no plugin mirror, parity test or plugin registry row. `src/superclaude/commands/spec-panel.md` and its plugin twin keep their "once per loop" wording, pinned by `tests/skills/test_review_severity_mapping.py`, `tests/skills/test_review_loop_extension.py` and `tests/skills/test_spec_panel_review_loop.py`; that wording moves in stage 4.
- Not built here: no classifier (`superclaude review classify` does not exist), no follow-up list file or `follow-ups` command group, no `sc-review-severity` skill folder, scale map, carrier registry, doctor check or registry drift test, no seeded-recall run, hash-bound owner ruling, shadow stage or baseline file, no Jev or other external judge call, no change to `src/superclaude/skills/sc-implement-protocol/refs/qa.md` (it keeps its own scale), to `src/superclaude/cli/review/ledger.py` or `review-ledger/1`, to the own-scale primitives of spec section 9.3, to code-assigned severity in `src/superclaude/cli/**/*.py`, to the cap of 2 fix cycles, or to the 35 percent target. Stage 4 edits the doubt wording and the merge text of the templates and rule prompts; this package only copies the S1 to S3 and S5 bullets into the ten tuple files (Task 3).
- Pins are by content. An acceptance check that must survive a task's own edit quotes the sentence it protects; it does not name a line number, because the edit moves the line. Line numbers in a task body are where the text sits today and are re-read before editing. An acceptance line that a later task of this package makes false carries its end point ("until Task N").
- `src/superclaude/` is the source of truth. Edit there, then run `make sync-dev` (it copies skills, agents, commands, hooks and templates; it does not copy `output-styles/`, `core/` or `rules/`). The installed `~/.claude/output-styles/pragmatic.md` therefore changes only at a refresh (Task 10 says how). Staging anything under the project `.claude/` folder is forbidden (only `.claude/settings.json` is tracked). Installed primitives name installed paths (`~/.claude/...`) first and project `.claude/...` second, never a `src/superclaude/` path.
- Kept mechanical gates (fixed FAIL triggers that stay as named gates) are recorded in the editing task's own `./artifacts/kept-mechanical-gates.md`, one bullet per gate: path relative to `src/superclaude/`, the gate's quoted words, the condition it maps to (the Missing condition of the digest), the reason. No `refs/scale-map.md` exists and none is created.
- Python work uses UV only: `uv run pytest ...`, never `python -m` or bare `pip`.
- Task-owned evidence and generated outputs go under `./artifacts/` in this package. `.dev/tasks/` is always staged (`git add .dev/tasks`), packages and their `./artifacts/` included, and no document a task writes says it is left out of staging. Staging is not committing.

Start sha: f4d6930775c1f9b4e8fe0ba8700ac2b02e6fcbbf

Diff against the start snapshot:
```diff
diff --git a/tests/audit/test_nfr_conv_9_zero_trust.py b/tests/audit/test_nfr_conv_9_zero_trust.py
index 827b80d52..0b384330b 100644
--- a/tests/audit/test_nfr_conv_9_zero_trust.py
+++ b/tests/audit/test_nfr_conv_9_zero_trust.py
@@ -78,20 +78,21 @@ NFR_CONV_2_DOC = REPO_ROOT / "docs" / "reference" / "nfr-conv-2-prose-determinis
 # index.
 # ---------------------------------------------------------------------------
 PASS_BULLET = (
-    "- **PASS** — No CRITICAL or IMPORTANT gaps; any MINOR gaps are listed "
+    "- **PASS** — No blocking gap exists; any Medium or Note gaps are listed "
     "as notes. Green light for synthesis."
 )
 FAIL_BULLET = (
-    "- **FAIL** — Any CRITICAL or IMPORTANT gap exists. List each with a "
+    "- **FAIL** — Any blocking gap exists. List each with a "
     "specific remediation action. All blocking gaps must be resolved before "
-    "proceeding; MINOR gaps never fail the gate."
+    "proceeding; Medium and Note gaps never fail the gate."
 )
 
 # Roadmap anchor — the CRITICAL / IMPORTANT / MINOR scale the research-gate
 # verdict rule grades against.
 SEVERITY_TRIPLE = ("CRITICAL", "IMPORTANT", "MINOR")
 
-# Blocking severities under the review severity rule: only these fail the gate.
+# Label scale of this test's sample-report scorer; it does not define the grade
+# (the scorer reads labels in a fixture report).
 BLOCKING_SEVERITIES = frozenset({"CRITICAL", "IMPORTANT"})
 
 
diff --git a/tests/audit/test_severity_floor_unweakened.py b/tests/audit/test_severity_floor_unweakened.py
index 20ecb0208..ff2979c8b 100644
--- a/tests/audit/test_severity_floor_unweakened.py
+++ b/tests/audit/test_severity_floor_unweakened.py
@@ -51,13 +51,19 @@ BASELINE_SLICE_SHA = "770f439517cab45a605f0e098561946f04485d406393567fa8bbeaba9d
 # findings. All blocking findings must be resolved; minor findings are
 # recorded as notes." (cap-edits.yaml row C-003). Rules 1-9 and 11,
 # including Rule 6, are unchanged.
-BASELINE_BLOCK_SHA = "be18e2cf2194b3232c83c77ee6d08c30ad707d10304ff592e5d7e78872e46b1b"  # pragma: allowlist secret
+# Re-pinned 2026-11-17 (stage 3 of issue 552): Rule 6 now grades a
+# contradiction by the review severity rule (a decision basis stays
+# Blocking), Rule 9 carries "Unknown is not no", and Rule 10 carries the
+# three choices at the cap. The 10-line window hash above is unchanged.
+BASELINE_BLOCK_SHA = "e505e83ee712743081088af011e43a714d2ec6cb0e8984a7e068be9cc8c806e7"  # pragma: allowlist secret
 
 # Rule #6 verbatim text (the explicit severity floor).
 RULE_6_TEXT = (
-    "**Contradictions are always IMPORTANT or CRITICAL** — If two sections "
-    "say different things about the same topic, that's never minor. Always "
-    "surface contradictions."
+    "**A contradiction a decision rests on stays Blocking** — If two sections "
+    "say different things about the same topic, always surface it. A "
+    "contradiction nothing rests on is a follow-up; a contradiction that "
+    "touches a decision basis, a quoted number or a required deliverable "
+    "stays Blocking under the Decision condition."
 )
 
 CRITICAL_RULES_HEADER = "## Critical Rules"
diff --git a/.dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/artifacts/t8-pytest-excerpt.txt b/.dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/artifacts/t8-pytest-excerpt.txt
new file mode 100644
index 000000000..7b84d6762
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/artifacts/t8-pytest-excerpt.txt
@@ -0,0 +1,34 @@
+Excerpt of ./artifacts/t8-pytest.log (full log: 1212 lines, one PASSED/FAILED line per test)
+PASSED lines: 1159
+FAILED lines: 0
+tests/audit/test_dnsp_all_agents_fail_bypass.py::TestR122WrapperTextGuards::test_all_wrapper_sources_exist PASSED [ 25%]
+tests/audit/test_dnsp_all_agents_fail_bypass.py::TestR122WrapperTextGuards::test_rf_team_lead_source_exists PASSED [ 25%]
+tests/audit/test_dnsp_all_agents_fail_bypass.py::TestR122WrapperTextGuards::test_r122_label_named_at_every_site PASSED [ 25%]
+tests/audit/test_dnsp_all_agents_fail_bypass.py::TestR122WrapperTextGuards::test_path_a_label_present_at_every_site PASSED [ 25%]
+tests/audit/test_dnsp_all_agents_fail_bypass.py::TestR122WrapperTextGuards::test_path_b_label_present_at_every_site PASSED [ 25%]
+tests/audit/test_dnsp_all_agents_fail_bypass.py::TestR122WrapperTextGuards::test_path_c_label_present_at_every_site PASSED [ 25%]
+tests/audit/test_dnsp_all_agents_fail_bypass.py::TestR122WrapperTextGuards::test_rf_team_lead_fix_cycles_pointer_present_at_every_site PASSED [ 25%]
+tests/audit/test_dnsp_all_agents_fail_bypass.py::TestR122WrapperTextGuards::test_rf_team_lead_fix_cycles_sha256_pin_present_at_every_site PASSED [ 25%]
+tests/audit/test_dnsp_all_agents_fail_bypass.py::TestR122WrapperTextGuards::test_guard_rejection_symbol_present_at_every_site PASSED [ 25%]
+tests/audit/test_dnsp_all_agents_fail_bypass.py::TestR122WrapperTextGuards::test_mutual_exclusivity_phrasing_present_at_every_site PASSED [ 25%]
+tests/audit/test_dnsp_all_agents_fail_bypass.py::TestR122WrapperTextGuards::test_zero_successes_and_zero_exhausts_rejected_in_text PASSED [ 25%]
+tests/audit/test_dnsp_all_agents_fail_bypass.py::TestRfTeamLeadFixCyclesByteStability::test_fix_cycles_rule_present_and_byte_stable PASSED [ 26%]
+tests/audit/test_dnsp_all_agents_fail_bypass.py::TestRfTeamLeadFixCyclesByteStability::test_fix_cycles_line_contains_max_2_cycles_token PASSED [ 26%]
+tests/audit/test_dnsp_all_agents_fail_bypass.py::TestRfTeamLeadFixCyclesByteStability::test_fix_cycles_line_contains_halt_and_ask_user_token PASSED [ 26%]
+tests/audit/test_dnsp_all_agents_fail_bypass.py::TestPathAActivatesRfTeamLeadNoSynthetic::test_path_selector_returns_path_a PASSED [ 26%]
+tests/audit/test_dnsp_all_agents_fail_bypass.py::TestPathAActivatesRfTeamLeadNoSynthetic::test_path_a_activates_rf_team_lead_fix_cycles PASSED [ 26%]
+tests/audit/test_dnsp_all_agents_fail_bypass.py::TestPathAActivatesRfTeamLeadNoSynthetic::test_path_a_emits_zero_synthetic_blocks PASSED [ 26%]
+tests/audit/test_dnsp_all_agents_fail_bypass.py::TestPathAActivatesRfTeamLeadNoSynthetic::test_path_a_scales_with_cohort_size[1] PASSED [ 26%]
+tests/audit/test_dnsp_all_agents_fail_bypass.py::TestPathAActivatesRfTeamLeadNoSynthetic::test_path_a_scales_with_cohort_size[2] PASSED [ 26%]
+tests/audit/test_dnsp_all_agents_fail_bypass.py::TestPathAActivatesRfTeamLeadNoSynthetic::test_path_a_scales_with_cohort_size[3] PASSED [ 26%]
+tests/audit/test_dnsp_all_agents_fail_bypass.py::TestPathAActivatesRfTeamLeadNoSynthetic::test_path_a_scales_with_cohort_size[5] PASSED [ 26%]
+tests/audit/test_dnsp_all_agents_fail_bypass.py::TestPathAActivatesRfTeamLeadNoSynthetic::test_path_a_scales_with_cohort_size[8] PASSED [ 26%]
+tests/audit/test_dnsp_all_agents_fail_bypass.py::TestPathBEmitsSyntheticNoEscalation::test_mixed_cohort_routes_to_path_b[2-1-1] PASSED [ 26%]
+tests/audit/test_dnsp_all_agents_fail_bypass.py::TestPathBEmitsSyntheticNoEscalation::test_mixed_cohort_routes_to_path_b[3-1-2] PASSED [ 27%]
+tests/audit/test_dnsp_all_agents_fail_bypass.py::TestPathBEmitsSyntheticNoEscalation::test_mixed_cohort_routes_to_path_b[3-2-1] PASSED [ 27%]
+tests/audit/test_dnsp_all_agents_fail_bypass.py::TestPathBEmitsSyntheticNoEscalation::test_mixed_cohort_routes_to_path_b[4-2-2] PASSED [ 27%]
+tests/audit/test_dnsp_all_agents_fail_bypass.py::TestPathBEmitsSyntheticNoEscalation::test_mixed_cohort_routes_to_path_b[5-3-2] PASSED [ 27%]
+tests/audit/test_dnsp_all_agents_fail_bypass.py::TestPathBEmitsSyntheticNoEscalation::test_path_b_does_not_activate_rf_team_lead PASSED [ 27%]
+tests/audit/test_dnsp_all_agents_fail_bypass.py::TestPathBEmitsSyntheticNoEscalation::test_path_b_emits_one_synthetic_per_exhaust PASSED [ 27%]
+tests/audit/test_dnsp_all_agents_fail_bypass.py::TestPathCBaselineMerge::test_all_success_routes_to_path_c[1] PASSED [ 27%]
+================= 1159 passed, 1 skipped, 5 warnings in 4.01s ==================
```

Codegraph context
index_state: fresh
checked_at: 2026-11-17T00:49:50Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel
projectPath: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel
call codegraph only when index_state: fresh, never to widen scope
Q2b dependents not in the diff: none for code; the audit tests read rf-qa.md and rf-qa-qualitative.md (and their .claude mirrors made by make sync-dev, which are gitignored). test_invariant_preservation_NFR_6_through_10.py imports the bullets from the first module and needed no edit of its own.

Delta diff from the previous reviewed tree (empty on the first review): 

Earlier blocking findings of this start (empty on the first review): 

Saved-probe re-check hit locations (may be empty): 

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
