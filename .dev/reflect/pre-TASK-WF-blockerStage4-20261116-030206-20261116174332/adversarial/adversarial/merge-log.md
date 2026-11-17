# Merge log: merged review card, stage 4 plan (second review)

- Plan: `refactor-plan.md` (this folder), review status auto-approved.
- Base: V3 (`variant-3-original.md`).
- Output: `.dev/reflect/pre-TASK-WF-blockerStage4-20261116-030206-20261116174332/adversarial/merged-review-card.md`.
- Shape model: the first review's card, `.dev/reflect/pre-TASK-WF-blockerStage4-20261116-030206-20261116030426/adversarial/merged-review-card.md` (Keys block, finding-line format, Source comments, the six sections).

## Planned changes

| Id | Status | Grade (unchanged) | Source | Notes |
|----|--------|-------------------|--------|-------|
| H1 | applied | MEDIUM | V3 F1 (lowered from blocking), V1 F1, V2 F2; C-001, X-001; Round 2 V1 "New evidence 1", Round 2 V3 on C-001 | category kept as the plan gives it (`unpassable-check`), although Round 2 V1 conceded that label was wrong for its own F1 (see Dropped); the merge executor does not re-label |
| H2 | applied | MEDIUM | V1 F6, V2 F1, V3 F8; C-002, X-002; Round 2 V2 (roadmap SKILL.md:563), Round 2 V3 | 10 plan citations, 6 kept on the line (cap); SPEC:948, SPEC:1105 and P4:74 moved to the C-002 bullet of Reviewer disagreement |
| H3 | applied | MEDIUM | probe INV-001, Round 3 and the orchestrator ruling | `agent_template_qa.md:140` on the line; the other three S5 lines (skill_template.md:831, 01 MDTM :647, 02 MDTM :658) moved to the INV-001 bullet of Reviewer disagreement (6-citation cap) |
| H4 | applied | MEDIUM | probe INV-002, Round 3 V1 and V3 | added V1's test-simulation note (variant-1:39) as the evidence for "re-check the `artifacts` pins" |
| H5 | applied | MEDIUM | V3 F6; C-009; Round 2 V1 (S1:214), Round 2 V3; probe INV-007 | |
| H6 | applied | minor | V1 F2, V2 F3, V3 F2; C-003 | added MW:59 (the `FINAL: <pass|issues>` ledger line) to show the line the fix should name |
| H7 | applied | minor | V1 F3, V3 F3; C-004 | added P4:47 (V1's "equals the heading words") and S3:154 (Critical Rules block) |
| H8 | applied | minor | V1 F4; C-005; Round 2 V1 | |
| H9 | applied | minor | V1 F5; C-006; Round 2 V1 | |
| H10 | applied | minor | V3 F4; C-007 | |
| H11 | applied | minor | V3 F5; C-008 | added S1:66 (stage 1 lists no plugin path) |
| H12 | applied | minor | V3 F7; C-010 | added P4:120 and P4:122 to show Task 6 writes the summary after Task 5 |
| H13 | applied | minor | probe INV-006, INV-008, INV-010 | Who line written as "the executors of Tasks 1 and 5" (the plan row gave none) |
| Earlier-review findings | applied | n/a | plan statuses; V1, V2, V3 Checked | plain bullet list, not a table; one P4 quote per point added from the plan's line references |
| Reviewer disagreement | applied | n/a | debate-transcript.md, round2-rebuttals.md, round3-invariant-resolution.md | C-001, C-002, INV-001, overall verdict, V2 dissent |
| Dropped | applied | n/a | plan "Changes NOT Being Made" | C-011, X-004 with V1's F1 label, X-005, V2 identity note |
| Checked | applied | n/a | V1, V2, V3 Checked; probe ADDRESSED rows | the eight required items plus paths and commands, tests outside the run list, limits |

Skipped plan steps: none.

Plan discrepancy resolved: the plan's Overview says "5 MEDIUM warnings and 7 minor notes", but its table lists 8 minor findings (H6 to H13) and the task brief says 8. The card follows the table: 5 MEDIUM and 8 minor.

## Post-merge validation

### Structural
- Sections present in order: title, Keys, `## Verdict`, `## Findings`, `## Earlier-review findings`, `## Reviewer disagreement, as settled by the debate`, `## Dropped`, `## Checked`. No other heading.
- 13 finding lines H1 to H13, each a single line in the form `H<n> | blocking false | grade | category | Who: ... Wrong result: ... | citations: ...`, each followed by a `<!-- Source: ... -->` comment.
- Longest finding line 1696 characters (H3); all under 1800. At most 6 citations per finding line.
- Verdict is two sentences (PASS with counts; the dissent).
- No em dash in the card (grep count 0). No markdown table inside a finding.
- Keys include ADV = `.dev/reflect/pre-TASK-WF-blockerStage4-20261116-030206-20261116174332/adversarial/adversarial`; every key used in a citation (P4, SRC4, S1, S1SRC, S2, S3, SPEC, README, MAP, PANEL, MW, ADV) is defined.

### Citations re-read
- Every cited line was re-read in the repository with Read or Grep during this merge, and every quote is a verbatim substring of that line (inner double quotes escaped as `\"`).
- Kept: 171 citations (findings 68, earlier-review findings 24, reviewer disagreement 25, dropped 8, checked 46).
- Dropped as unverifiable: 0.
- Line numbers corrected: 0. Every line number taken from a variant, the probe or Round 2/3 still holds. Where a source gave no line, the line was found and quoted: S1:110 (registry counts; V3 said "stage 1 Task 6"), S3:227 (summary name; V3 said "S3 Task 13"), tests/skills/test_worker_contract.py:924 and :925 (V3 gave the range 909-925), the fixture rows (cap_edits.yaml:164, :188; sweep_edits.yaml:930), Makefile:109 and :166.
- Not carried: V1's Checked citation "plan line 87" for the plugin decision (wrong line, X-004; the card cites P4:23).
- Re-counts by Grep this merge: 11 files under `src/` and `plugins/` hold "Grade every review finding as blocking or minor"; the cap sentence "runs at most 2 fix cycles (3 reviews), then escalate..." is in the same 11 files; `review-severity:digest v2 begin` occurs 0 times under `src/superclaude`; case-insensitive cap counts 5, 6, 1, 2; HALT counts 2, 5, 6; "follow-up candidates|once per loop" occurs in one file under `tests/` (MAP); `src/superclaude` occurs 0 times in the eight template and rule-prompt carriers; "strict" occurs once in S1; the S5 sentence is at agent_template_qa.md:140, skill_template.md:831, 01 MDTM :647, 02 MDTM :658.

### No grade changed
- H1 to H5 MEDIUM, H6 to H13 minor, exactly as the plan's Grade column; no finding is blocking; `blocking false` on every line.
- No finding was added beyond H1 to H13; dropped points stay in `## Dropped`.

### Contradiction re-scan
- The Verdict (PASS, no blocking) agrees with every finding line (`blocking false`) and with the Reviewer disagreement section (settled: none blocking; V2 dissent recorded).
- The H1 category `unpassable-check` sits beside the Dropped note that V1 conceded that label for its own F1; this is the plan's choice and is recorded here rather than changed.
