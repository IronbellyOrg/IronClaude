---
card: reflect-t1
mode: pre
claim_class: static_defect
evidence_class: source_static
hypothesis_source: inline (orchestrator self-review, one agent)
---

# Tier 1 card: pre-execution review of the stage 3 plan (re-review after revision 2)

Plan: .dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/TASK-WF-blockerStage3-20261116-030158.md (PLAN). Driving file: .dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/source.md (SRC). Program spec: .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md (SPEC). Stage 2 plan (S2): .dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/TASK-WF-blockerStage2-20261116-030156.md. Stage 1 plan (S1): .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md. Stage 0 plan (S0): .dev/tasks/to-do/TASK-WF-blockerStage0-20261116-021044/TASK-WF-blockerStage0-20261116-021044.md. The first review (card F1 to F7 blocking) is at .dev/reflect/pre-TASK-WF-blockerStage3-20261116-030158-20261116030420/adversarial/merged-review-card.md.

## Coverage (mechanical, Step 1B.0)

parsed_count 0 (no REQ-nn, R-nn, SPEC-nn or T-nn id in SRC), inferred_count 41 (all quotes verbatim in SRC), coverage_pct_union 0.9024, S_dev_density 0.0976 (4 rows unmatched mechanically: INF-004, INF-006, INF-032, INF-038; read by hand all four are covered: Task 1 "Earlier evidence exists", the renumbering itself, Task 4, Task 10). Table: artifacts/coverage-matrix.yaml. coverage_degraded: parsed-sparse forbids a Tier-1 stop.

## Observations (each re-read against the live file)

O1. The seeded-recall gate is checked after the edit it protects. PLAN:125 (Task 5) edits `pragmatic.md`; the gate is acceptance line 1 of Task 5 (PLAN:128). `/sc:implement` runs Q1 EXEC (edit) before Q3 REVIEW (src/superclaude/skills/sc-implement-protocol/SKILL.md:131 and :140), so the live rule file is already changed when the R-lines and the owner ruling are first read. PLAN:20 says "no later task starts unless Task 1 and the seeded-recall gate of Task 5 pass", which is true for Tasks 6 to 13 only. SRC:3 and SRC:13 ask for "an acceptance line, not a dependency line", so the plan follows the source; the question is whether the plan should also say "read the gate before the first edit" in the Task 5 body (the same ordering reason that made the first review move the entry checks into Task 1).

O2. The two arms of Task 3 do not hold the same scope. PLAN:76 old arm = the lines of `pragmatic.md` from the "Every review agent MUST review as an independent reader" bullet (line 221) to the spec-panel scale bullet (line 231), about ten bullets: reviewer brief, zero-finding rule, conflict rule, binary verdict, the five definition bullets, Medium and spec-panel. New arm = "the digest section of refs/rule.md" only (the REQ-01 block, SPEC:195-207). PLAN:76 says "only the rule text differs", but the new arm lacks the reviewer-brief, zero-finding and binary-verdict bullets the old arm has, and Task 5 ships a REQ-04 reviewer-brief change (PLAN:125) and the Medium cadence change that no arm tests.

O3. PLAN:78 tells the executor to "report the recall lines both with and without" a reviewer whose quoted sentences come from the old rule; PLAN:82-92 define exactly one outcome word per line. Nothing says which variant decides the outcome word that Task 5 reads.

O4. A fixed grading line outside the freeze patterns stays in both QA agents. src/superclaude/agents/rf-qa.md:100 reads "an unverified or 'probably fine' claim is blocking" (rule 8, NO LENIENCY) and src/superclaude/agents/rf-qa-qualitative.md:99 carries the same sentence. S0:34 freezes the REQ-30 patterns plus "Any CRITICAL or IMPORTANT issue exists"; "it FAILS" and "is blocking" in rule 8 match none. Tasks 6 and 7 edit S1, S2, S5 (about line 108), the merge rule, the fixed FAIL triggers of the freeze and (Task 7) Rule 6, so rule 8 would stand beside a digest that makes an unverified claim blocking only under a named condition (an unverified safety claim stays open, SPEC:199).

O5. A pinned sentence sits inside the bullet Task 5 rewrites. pragmatic.md:221 holds "never to meet a quota"; tests/skills/test_review_prompt_overrides.py:244 asserts it in the flattened style file. PLAN:125 asks only that reviewers "hunt for defects and name their consequence instead of hunting for false claims" and PLAN:195 requires that test to pass unchanged, but Task 5 neither names the sentence nor runs that test (PLAN:134).

O6. Baselines. PLAN:230 asks that M1, M4, M5, M6, M9, M10b, M11 and M12 each carry "its baseline from Task 2 or the statement that none exists", but Task 2 counts only M1, M12 and M10b (PLAN:59-61). M6's baseline source is stage 2 (SPEC:967); the share of `consumer-unknown` rows is a number the stage 2 script prints (S2:138), so it lands in Task 1's `./artifacts/shadow-recount.md`, not in Task 2's file. M9 and M11 baselines are in the spec text (SPEC:970, SPEC:973); M5's is Task 3.

O7. Task 12 scans seven directories (PLAN:214); SPEC:920 (T5) scans "`src/` or `plugins/`". Today's grep over all Markdown under src/superclaude and plugins/superclaude hits only the expected files (rf-qa, rf-qa-qualitative, rf-analyst, the auggie file, readme, tdd, tech-reference, operational-guide, agent_template_analysis, agent_template_qa, skills/task/SKILL.md), so nothing is missed today.

O8. Task 1 compares the digest section of `refs/rule.md` with "the REQ-01 block of the spec ... once whitespace is collapsed" (PLAN:43); the spec block is a blockquote with `> ` markers and bold (SPEC:195-207). The comparison rule (strip quote markers) is implied, not stated. S1:49 says the digest is that block word for word, so the check can pass.

O9. Task 9's third acceptance line (PLAN:182) uses `git diff -U0 -- src/superclaude/skills/sc-implement-protocol` (PLAN:182), without `HEAD`; stage 2 uses `git diff -U0 HEAD` (S2:80). With stage 2's edits uncommitted and unstaged, the diff would include stage 2's added lines too; they are already free of the words (S2:80), so no false failure results.

## Fixes of the first review that hold (checked)

F1 (entry checks before any spawn or edit): Task 1 reads files only, writes `./artifacts/stage3-entry-check.md`, recounts with `shadow_summary.py --confirmed-misses` (S2:138 builds that script with that option and the "not computable" line), and checks the stage 0, 1 and 2 files by the names those plans create (S0:37 inventory freeze, S0:44 escape test, S0:69 regrade, S0:106 seeded set, S1:49 rule.md, S1:66 scale-map, S1:223 registry test, S2:41 sweep.py, S2:56 follow_ups_cmd.py, S2:113 and S2:79). F2: PLAN:78 states the hook confound (hooks.json:173 runs pragmatic-subagent.js; the installed style holds the old rule), identical model class and brief, and the lower-bound reading. F3: PLAN:82-94 define the five lines, the outcome words and the owner ruling that must cite the file's SHA-256. F4: Task 13 (PLAN:232) names release, refresh and install check; Makefile `sync-dev` copies skills, agents, commands, hooks and templates and has no step for output-styles (Makefile:109-157; SPEC:885). F5: the registry test sits in Tasks 5, 6, 7 and 10 and each of those tasks checks the row reads `v2`; Task 1 and Task 3 compare one digest SHA-256. F6: PLAN:231 judges RT1 (seeded part) and RT3 now. F7: Task 2 counts M1, M12, M10b baselines and the RT5 threshold.

Live-line checks that hold: pragmatic.md:225, :226, :229 are the three definition bullets; rf-qa.md:83 and rf-qa-qualitative.md:84 and rf-analyst.md:75 carry the merge rule; rf-qa.md:152, :162, :168-170, :182-183, :327, :389, :402, :476, :549 and rf-qa-qualitative.md:240, :291, :362, :429, :500, :567, :746, :784, :809, :990, :994 match PLAN:140 and PLAN:154; skills/task/SKILL.md:252 and :361 are the only retired hits; tests/skills/test_review_severity_rule.py holds `test_ej_fixtures_are_byte_copies_of_the_plan_tables` (:275) and `test_h_implement_protocol_plugin_twins_byte_equal` (:371); the twins are equal today; src/superclaude/cli/review/__init__.py lists nine names (panel_cmd, merge_cmd, ledger_cmd, telemetry_cmd, lint_cmd, estimate_cmd, cluster_cmd, verify_cmd, manifest_cmd; lint_cmd and estimate_cmd have no module), so the seven subcommands Task 4 expects to see in `--help` exist.

## Recommendations

R1. Task 5 body: read the seeded-recall result and the ruling before the first edit (O1). R2. Task 3: one sentence stating what the new arm holds besides the digest, and which variant decides each outcome word (O2, O3). R3. Tasks 6 and 7: add rule 8 "an unverified or probably fine claim is blocking" to the rewrite list (O4). R4. Task 5: name "never to meet a quota" as kept and run `test_review_prompt_overrides.py` (O5). R5. Task 13: M6 baseline source (O6).

## Self-report

confidence: 0.80
