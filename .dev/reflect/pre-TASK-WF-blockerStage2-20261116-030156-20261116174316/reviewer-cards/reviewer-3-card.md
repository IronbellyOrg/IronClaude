# Reviewer card 3 (persona refactorer, model class opus) - persisted by the orchestrator (the "Checked, no defect" bullets are condensed; every finding is unchanged)

reviewer: 3
persona: refactorer
model_class: opus

## Findings

id: R3-1
severity: blocking
claim: The plan's flow writes a safety-vocabulary row into the ledger as a plain follow-up first, and nothing in the flow ever writes the `protected-risk-dispute` tag back. Task 4 runs `follow-ups write` and then `follow-ups safety`. Task 2's `write` does not call the safety route, and `safety` only prints what the route returns. Task 8 counts a safety miss as "a confirmed row without the tag", and `show_user` counts the tag, so both rely on a tag that is never stored.
citations: plan:56; plan:88; plan:138; stage1 plan:196; merged-requirements.md:932
quote: plan:56 "`safety --ledger <path> [--judge-answers <file>] [--unattended]` runs the stage 1 safety route over the ledger and prints what it returns"; plan:88 "the run owner writes `${TASK_DIR}qa/follow-ups.md` with `superclaude review follow-ups write` ... then runs `superclaude review follow-ups safety` over the ledger"; plan:138 "the count is the confirmed rows that lack the `protected-risk-dispute` tag"; spec:932 "is written as a plain follow-up instead of `protected-risk-dispute` (GR12)"
consequence: Every real run breaks GR12 and fails T17 by construction. Any confirmed safety row counts as a miss even when `safety` showed it to the person. The stage 3 entry needs "safety misses 0", so it becomes unreachable as soon as one safety row is confirmed. `show_user` also undercounts. The sweep and summary tests use fixtures, so they will not catch this.
confirms_t1: none
confidence: 0.75

id: R3-2
severity: blocking
claim: For tech-research reports, the tier lookup that `write` depends on has no defined answer, and the report-table format is not defined either. The spec's row for the CRITICAL/IMPORTANT/MINOR lens scale (which covers tech-research) gives no label-to-outcome mapping. Labels like IMPORTANT and MINOR also appear in other families with different outcomes, yet `write` has no family or scale option. Research QA and Synthesis QA send reviewers to an agent-file output format that this plan may not edit, so no table format ties real reports to the parser.
citations: plan:56; merged-requirements.md:737; merged-requirements.md:739; stage1 plan:62; src/superclaude/skills/tech-research/SKILL.md:902; plan:26
quote: plan:56 "the tier of a row is the shared outcome that `refs/scale-map.md` gives its native label"; spec:737 "the label is information; the outcome comes from the three conditions"; spec:739 "MINOR: Note"; SKILL.md:902 "Use the full QA report output format from your agent definition."
consequence: For every tech-research row, `write` cannot tell Medium from Note. So the "Medium row without `why not blocking` is refused" rule, the Items `tier` column and the `follow_up` and `note` counts from `summary` are either undefined or invented by whoever builds it. Fixture tests will pass while real reports produce wrong tiers or end up `capture_state: incomplete`.
confirms_t1: F4
confidence: 0.70

id: R3-3
severity: blocking
claim: In phases 3 and 5, two of the five reviewers are rf-analyst agents, and their reports go into the consolidation that Task 4 feeds to `follow-ups write`. The rf-analyst prompt template ("Research Analyst Agent Prompt") is not one of the five templates Task 4 edits. As a result, analyst findings never carry `rests_on` or `why not blocking`.
citations: plan:88; src/superclaude/skills/tech-research/SKILL.md:480; :487; :507; :819; :848; merged-requirements.md:318; merged-requirements.md:648
quote: plan:88 "Five reviewer prompt templates (Research QA, Synthesis QA, Report Validation QA, Qualitative QA, Lens-Specific QA)"; SKILL.md:487 "Read ALL reports from Step 3.1, consolidate into"; SKILL.md:819 "### Research Analyst Agent Prompt (rf-analyst — Completeness Verification)"; spec:318 "Each reviewer writes every finding with the fields of section 6.2, including `rests_on`"
consequence: GR2 makes analyst Minor findings invalid, so `write` refuses or drops them, and phase 3 and 5 ledgers come out incomplete on every run. Task 6's T9 test checks only the five templates, so the gap passes the tests. Two of the five edited templates (Report Validation and Qualitative) are marked LEGACY and are not used for Phase 6, so the edit misses an active reviewer while covering unused ones.
confirms_t1: none
confidence: 0.60

id: R3-4
severity: minor
claim: Task 1's entry check is narrower than the Constraints promise. The Constraints say Task 1 checks that the `classify` command exists. Task 1 imports only three modules and never checks `classify_cmd`/`classifier`, `refs/scale-map.md` (read by Tasks 2 and 4) or `refs/registry.yaml` (read by Task 6).
citations: plan:20; plan:44; plan:113; plan:126
quote: plan:20 "its modules `follow_ups.py`, `safety_route.py`, `classifier_inputs.py` and the `classify` command exist; Task 1 checks that"; plan:44 "`uv run python -c \"from superclaude.cli.review import follow_ups, safety_route, classifier_inputs\"`"
consequence: If one of these stage 1 parts is missing, the run fails at Task 4, 6 or 7, after edits have already been made. The failure is loud and causes no data loss, which is why this is minor.
confirms_t1: F3
confidence: 0.85

id: R3-5
severity: minor
claim: The plan never says what the "call line" is. Task 3 asks for one paragraph that contains the call and also says "never `--promote` and never `--write`". This file writes each paragraph as one physical line. Task 3 AC3 and the stage 3 entry check, however, test the line holding the call for the absence of `--promote` and `--write`.
citations: plan:72; plan:79; src/superclaude/skills/sc-implement-protocol/SKILL.md:192; stage3 plan:42
quote: plan:72 "`--kind auto`, never `--promote` and never `--write`"; plan:79 "neither call line holds `--promote` or `--write`"; stage3:42 "shows one call line in each file, and neither line holds `--promote` or `--write`"
consequence: If the paragraph follows house style, Task 3 AC3, Task 6's mutation test and stage 3's entry check all fail on the plan's own wording. The fix is to state that the command sits on its own line or in a code block.
confirms_t1: none
confidence: 0.60

id: R3-6
severity: minor
claim: The Constraints say "after Task 2 two more files mention it", but three files will match `grep -rln "follow_ups"`. `sweep.py` (from Task 1) reads through the stage 1 reader, `follow_ups_cmd.py` is new, and `__init__.py` gains the string "follow_ups_cmd".
citations: plan:27; plan:49; src/superclaude/cli/review/__init__.py:19; stage1 plan:125
quote: plan:27 "after Task 2 two more files mention it"; plan:49 "its only file reads are deliverables and the stage 1 reader"
consequence: Anyone who re-runs the stage 1 acceptance grep will see a count that does not match. No test pins it.
confirms_t1: none
confidence: 0.80

id: R3-7
severity: minor
claim: tech-research is told to "record and not wait" when nobody is reachable. It has no unattended mode, though, and no rule says when the run owner passes `--unattended` to `follow-ups safety`.
citations: plan:88; plan:102
quote: plan:88 "with nobody reachable it records and does not wait"; plan:102 "tech-research has no unattended mode and no contract"
consequence: The skill text has no way to choose the unattended branch, so that branch never runs from tech-research.
confirms_t1: F6
confidence: 0.60

id: R3-8
severity: minor
claim: Task 2 gives `safety` a `--judge-answers <file>` option but also says no subcommand calls a judge. Recorded answers can only be read through stage 1's `FixtureJudge`.
citations: plan:56; stage1 plan:146
quote: plan:56 "No subcommand calls `gh`, a network or a judge."
consequence: The ban should name live judges. As written, a strict reading forbids the wiring that `--judge-answers` needs.
confirms_t1: none
confidence: 0.50

## Refuted T1 findings
None refuted. F3 is confirmed as R3-4 but downgraded to minor, because a missing part fails loudly later and loses no data. F4 is confirmed and extended in R3-2 (no tier mapping exists for the tech-research scale). F6 is confirmed as R3-7.

## Checked, no defect (condensed)
- Registration: __init__.py:19-36 optional tuple plus add_command; `follow-ups` does not clash with panel, merge, ledger, telemetry, cluster, verify, manifest; tests/review/test_review_cli.py:44-49 checks only four names.
- tech-research targets exist: five prompt headings (SKILL.md:859, 906, 950, 1001, 1048), three consolidation items (487, 516, 549), Output Locations table (129-150), "INDEPENDENT STANCE ... no minimum count" (1063); exactly two full cap sentences (490, 555), phase 5 says only "then HALT" (519).
- Add-only edits keep the pins: test_lens_prompts_state_no_minimum_count (test_review_prompt_overrides.py:271-283), NO_CONDITIONAL_PASS (test_review_severity_rule.py:344-359), banned phrases (112-125), F1-F6 sweep patterns (398-405), at-cap clauses (215-219); multi-line pin S-106 (fixtures/review_severity_sweep_edits.yaml:877-878) holds if the new paragraph is not placed between the Synthesis QA PASS and FAIL lines.
- Task 4 AC2 (no "sweep" in added lines) matches its own instruction; test_review_severity_mapping.py reads only pragmatic.md and spec-panel.md.
- Static scan regex (test_implement_severity_static.py:296) does not match "STOP"; the allow-list pins steps 2, 3 and 6 (331-333).
- Archive digest skips `./artifacts/` paths (archive_workspace.py:396-405), so the sweep record does not make FINAL stale.
- pragmatic.md:225 holds the sentence Task 6 pins; stage 3 line 134 expects the Task 6 skip once the row is v2.
- Stage 3 consumes sweep.py, follow_ups_cmd.py, test_review_sweep.py, test_review_brief_rests_on.py, test_implement_follow_up_sweep.py (stage3:41) and one call line per file (stage3:42); Tasks 3 and 6 produce all of these.

## Follow-up candidates
- In stage 2 nothing writes a `follow-ups.md` under a `/sc:implement` package. tech-research writes to its own `${TASK_DIR}qa/` (plan:88), and `refs/qa.md` is unchanged, so the stage 2 sweep call (plan:72) will always find no ledger. Stage 3 then adds `--promote` to a call that has no input. The limits in plan:138 say "mostly reports skips" but should say "finds no ledger".
- Stage 1 names no public functions for `follow_ups.py` or `safety_route.py`, so Task 2's wiring artifact (plan:56) fixes the interface only after the fact; function names should be pinned in the stage 1 plan.
- Two of the five edited templates are LEGACY and unused for Phase 6 (SKILL.md:952, 1003). It is also unclear which prompt the phase 3 and 5 rf-qa-qualitative agents use.

verdict: NEEDS-REVISION
self_confidence: 0.70

## Calibration (blind, confidence-calibrator, class opus; calibrator_diversity: degraded)
dims: citation 0.85, coverage 0.80, clarity 0.85, risk 0.85, actionability 0.70
C: 0.81
per_finding: R3-1=0.72, R3-2=0.68, R3-3=0.60, R3-4=0.85, R3-5=0.62, R3-6=0.70, R3-7=0.58, R3-8=0.45
