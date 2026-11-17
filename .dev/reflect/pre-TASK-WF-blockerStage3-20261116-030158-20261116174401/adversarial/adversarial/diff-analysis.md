# Diff Analysis: reviewer-card comparison (stage 3 plan re-review)

## Metadata
- Generated: 2026-11-16T18:35:00Z
- Variants compared: 2 (Variant 1 = reviewer-1 card, analyzer persona, haiku class; Variant 2 = reviewer-2 card, qa persona, opus class)
- Aliases: PLAN = .dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/TASK-WF-blockerStage3-20261116-030158.md; SRC = .../source.md (same folder); SPEC = .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md; S0, S1, S2 = the stage 0, 1, 2 plan files; README = .../BLOCKER-CLASSIFICATION-PROGRAM-20261115/stage-requests/README.md
- Total differences found: 18 (structural 1, content 3, contradictions 2, unique 12; shared assumptions 3, counted separately)
- Convergence denominator: S + C + X + A = 1 + 3 + 2 + 3 = 9

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Severity |
|---|------|-----------|-----------|----------|
| S-001 | Card structure | Findings carry a **Category** line (all "Drift") and bold fields; 4 findings (3 blocking) | Plain "F1. Blocking: yes/no" lines without a category; 10 findings (3 blocking) | Low |

## Content Differences

| # | Topic | Variant 1 Approach | Variant 2 Approach | Severity |
|---|-------|--------------------|--------------------|----------|
| C-001 | Lines left in the QA agents that contradict the new digest | F2 (blocking): only rule 8 "an unverified or 'probably fine' claim is blocking" at rf-qa.md:100 and rf-qa-qualitative.md:99; fix = add rule 8 to Tasks 6 and 7 | F1 (blocking): rule 8 plus rf-qa.md:548 "When in doubt, fail it", rf-qa-qualitative.md:796 and :810 (label-counting lines), SPEC:853 lists 548; fix = add all of them with grep acceptance lines | Medium |
| C-002 | Completeness of the test re-pins (Tasks 10 and 11) | "Checked and sound": Tasks 10 and 11 name replacements, keep legacy pins and fixture equality | F4 (pinned "never to meet a quota" not named in Task 5), F8 (re-pinned zero-trust scorer still grades by label), F9 (missing end points; wrong description of the hash re-pin) | Medium |
| C-003 | First-review F7 (baselines) status | "fixed for the cited baseline gaps" (M1, M12, M10b, RT5) | "fixed for M1, M12, M10b" plus a new finding F7: M6 baseline missing from Task 2 although Task 13 says "from Task 2 or none exists" | Low |

## Contradictions

| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Impact |
|---|-------------------|--------------------|--------------------|--------|
| X-001 | Is the seeded-recall gate, an acceptance line of Task 5 (PLAN:128), an adequate gate for the rule-file edit at PLAN:125? | No. F1 (blocking): `/sc:implement` edits first (SKILL.md:131 Q1 EXEC) and reviews against acceptance lines after (SKILL.md:140 Q3 REVIEW), so the edit precedes the check; first-review F3 "partly fixed" | Yes by implication: first-review F3 "fixed" citing PLAN:92, PLAN:94, PLAN:128; no finding on ordering | High |
| X-002 | Is the Task 11 re-pin description correct? | "Task 7 defers the qualitative block hash until Task 11. Tasks 10 and 11 name the corresponding replacements" (sound) | F9: PLAN:203 says the hash is re-pinned "including the rewritten verdict pairs", but those pairs (lines 240 to 784) lie outside `## Critical Rules` (rf-qa-qualitative.md:983) | Low |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | 1 | F1: gate-after-edit ordering of Task 5 (see X-001) | High |
| U-002 | 1 | F3: no controlling variant for recall lines "with and without" a reviewer who quoted the old rule (PLAN:78 vs PLAN:82) | High |
| U-003 | 1 | F4: Task 12 (PLAN:214) still says stage 4 adds a plugin mirror of `refs/rule.md`, against revision2-brief.md:16 | Low |
| U-004 | 2 | F3: the two arms of Task 3 differ in scope (old arm pragmatic.md:221 to :231, new arm digest only; REQ-04 and Medium cadence in neither arm) | High |
| U-005 | 2 | F2: Task 6 acceptance checks only frozen-inventory lines, so named triggers (rf-qa.md:170, :327, :389, :476) can be skipped; Task 7 has no inventory check | Medium |
| U-006 | 2 | F4: Task 5 rewrites a bullet holding "never to meet a quota", pinned by test_review_prompt_overrides.py:244; the test is not run in Task 5 | Medium |
| U-007 | 2 | F5: Task 1 digest comparison does not say how to treat blockquote markers or fence lines | Low |
| U-008 | 2 | F6: L5 "Medium and Note findings are never rechecked" (SPEC:274, pragmatic.md:226) disappears when the bullet is replaced | Medium |
| U-009 | 2 | F7: M6 baseline source (S2:138) not counted by Task 2 | Low |
| U-010 | 2 | F8: tests/audit/test_nfr_conv_9_zero_trust.py:95 label-based scorer stays | Low |
| U-011 | 2 | F9: Task 6 has no "until Task 10 or 11" end point | Low |
| U-012 | 2 | F10: README:11 does not tell the owner to record the folder list and confirmation file on the stage 3 row | Low |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Impact | Classification | Status |
|-------|------------|------------------|--------|----------------|--------|
| A-001 | The stage 0, 1 and 2 packages, once executed, create the files and options Task 1 reads, under the names the plans give | Both cards: producers exist, absence now is expected | A wrong name would halt Task 1 | STATED | Documented |
| A-002 | The set of lines in the three edited agent and style files that contradict the digest is the set the plan (and the stage 0 freeze) lists | Both treat the plan's edit list as the baseline and add only some lines | A line left contradicting the digest ships next to it | UNSTATED | Promoted |
| A-003 | A failing acceptance line that halts the run (PLAN:20, PLAN:128) is a sufficient gate even though the edit happens first | Both accept PLAN:20's statement that later tasks do not start | If the halt leaves the edited file in the tree, the pilot's rule file changed without the gate | UNSTATED | Promoted |

## Summary
- Total structural differences: 1
- Total content differences: 3
- Total contradictions: 2
- Total unique contributions: 12
- Total shared assumptions surfaced: 3 (UNSTATED: 2, STATED: 1, CONTRADICTED: 0)
- Highest-severity items: X-001, U-001, U-002, U-004
