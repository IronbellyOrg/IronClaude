# Refactoring Plan

## Overview

- Base variant: Variant 1 (sonnet:analyzer), `variant-1-original.md`, combined score 0.8314
- Incorporated variants: Variant 3 (opus:refactorer) for the C-001 grounding and the OD10 fact; Variant 2 (haiku:qa) for the mapping-decision gap; the debate transcripts and the invariant probe for the Task 12 match and INV-001 to INV-005
- Planned changes: 9 (merged findings MF1 to MF9), 5 removals from the base
- Overall risk: Low to Medium (the merge rewrites claim text; every citation must be re-read before it stays)
- Output: `../merged-review-card.md` (card format of the reviewer cards: Verdict, Findings, Checked, Self-report) and `merge-log.md`

Citation shorthand used in this plan and in the merged card: PLAN = `.dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md`; SPEC = `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md`; source.md = `.dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md`; stage3-request.md and README.md live in `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/stage-requests/`. In the merged card write every citation as a repo-relative path with the real line range, never the shorthand.

## Planned Changes

### Change #1 — MF1 (C-001): Task 7's grep line false after Task 10, no end point
- Source: Variant 1 F3 (first half), Variant 2 F1, Variant 3 F2; Task 12 match from Variant 1 Round 2; end-point rule from Variant 3 Round 1.
- Target: Findings, first entry. Grade: MAJOR, blocking true, category unpassable-check (all three variants and the debate agree, 3 of 3 unanimous).
- Claim text to use: Task 7's acceptance line says the grep of `follow_ups` under `src/superclaude/cli/review` "shows only the new module and its command wiring", but Task 10 must reuse the Task 7 reader in `classifier_inputs.py` and Task 12 writes the ledger row's `classifier` column, so both files also match; no task builds a command wiring for `follow_ups` itself; and the line has no "until Task N" although the plan and the source request require one for a line a later task makes false. At the final review the line is false.
- Citations (keep exactly, re-Read each): PLAN:115 "shows only the new module and its command wiring"; PLAN:148 "Reuse the reader of Task 7 for ledger rows"; PLAN:171 "writes the verdict, band and judge id with version into the ledger row's `classifier` column"; PLAN:24 "An acceptance line that a later task of this package makes false carries its end point"; source.md:17 "get an end point"; README.md:33 "a line that a later task of the same package makes false is written with its end point".
- Rationale: debate C-001 and X-002 (confidence 92% and 90%).
- Risk: Low.

### Change #2 — MF2 (C-002): stoprule/finding-grader family has no defining file in the repository
- Source: Variant 1 F1 (strongest: the pairing with Task 5), Variant 2 F2, Variant 3 F1 (OD10 fact).
- Target: Findings, second entry. Grade: MAJOR, blocking true, category unpassable-check (unanimous).
- Claim text to use: Task 3 requires each of its 12 family rows to name a defining file that exists in the repository, and Task 15's T4 re-checks that each row names an existing file and a label in it; the stoprule/finding-grader family is defined by `refs/rubric.md` of the `sc-spec-panel-stoprule-protocol` skill and by the `finding-grader` agent, which the spec says exist only installed; neither is under `src/superclaude/` or `plugins/`, the only tracked copies sit under `.dev/experiments/`, and Task 5 forbids any file of the skill folder to cite a `.dev/` path; no task adds the files (owner decision OD10 is undecided), so Task 3, Task 5 and T4 cannot all pass for that row.
- Citations: PLAN:62 "each naming a defining file that exists in the repository"; PLAN:87 "no file of the skill folder cites a `.dev/` or `./artifacts/` path"; PLAN:209 "T4 (each scale-map row names an existing file and a label present in it)"; SPEC:582 "it exists only under `~/.claude/agents/`, not in `src/superclaude/agents/`"; SPEC:145 "installed only".
- Rationale: debate C-002 (90%); Variant 2 and 3 conceded Variant 1's pairing as decisive.
- Risk: Low.

### Change #3 — MF3 (C-003): allow-list narrower than the stage 3 scan
- Source: Variant 1 F2 (only variant that raised it); Variant 1 regraded it non-blocking in Round 2, Variant 2 conceded, Variant 3 agreed.
- Target: Findings. Grade: MAJOR, blocking false, category contradiction (the base said blocking true; the debate settled non-blocking, 3 of 3 after Round 2).
- Claim text to use: Task 3's "Merge-rule allow-list" lists the auggie file, `refs/rule.md` and the six stage 4 files, and the stage 3 request has the scan test read exactly that list, but the scan covers all of `src/`, and `cli/roadmap/remediate_parser.py` (lines 55 and 301) and `cli/pipeline/fmea_classifier.py` (lines 304 and 323) hold the phrases and are listed as not changed; the stage 3 scan will fail on them unless the section lists them or the code-assigned scale-map row feeds the scan. No check of this package fails, because the plan copies the request and T5 is not a stage 1 exit test, so the gap shows at stage 3.
- Citations: PLAN:65 "lists the auggie file, `refs/rule.md` and the six stage 4 files"; stage3-request.md:14 "allow-lists only files that exist in this stage: the auggie file, `refs/rule.md` and the six stage 4 files"; SPEC:845 "assigns severity in code and is out of scope with the roadmap checkers"; SPEC:920 "outside the scale-map allow-list"; src/superclaude/cli/roadmap/remediate_parser.py:55 "higher severity wins (BLOCKING > WARNING > INFO)"; src/superclaude/cli/pipeline/fmea_classifier.py:304 "Silent corruption from either signal = highest severity."
- Rationale: debate C-003 (85%); the finder is Variant 1, the grade follows the debate.
- Risk: Medium (grade changed from the base).

### Change #4 — MF4 (C-004, X-001): no recorded decision on the review-ledger/1 mapping or the "ledger adapters"
- Source: Variant 2 F3 (blocking), Variant 1 F6 first half (minor); debate: 2 of 3 non-blocking, Variant 2 dissents.
- Target: Findings. Grade: MAJOR, blocking false, category missing-requirement.
- Claim text to use: no task records a decision on the mapping from follow-up rows to `review-ledger/1` rows that the spec leaves to the plan, or on the "ledger adapters" listed in the stage 1 row; Task 7 runs only the reuse audit, which detects overlap and decides nothing. No stated check fails without it, because "none in version 1" builds the same result, so one recorded sentence closes it. One reviewer graded this blocking; the debate settled 2 of 3 non-blocking (dissent: Variant 2).
- Citations: SPEC:404 "A mapping rule from its rows to `review-ledger/1` rows is left to the `/sc:workflow` plan"; SPEC:945 "ledger adapters"; PLAN:110 "share code only where it says reuse-by-import"; PLAN:113 "covers each T7 failure condition above".
- Rationale: debate C-004 and X-001 (70%).
- Risk: Medium (the dissent is recorded in the report).

### Change #5 — MF5 (C-005, INV-002, INV-003): scale-map layout, path root and label-less rows are not fixed
- Source: Variant 1 F4 (grade MAJOR non-blocking), invariant probe INV-002 and INV-003.
- Target: Findings. Grade: MAJOR, blocking false, category other.
- Claim text to use: Task 9's `ReviewerJudge` and Task 12's disagreement matrix read the reviewer's label "through the scale map" and Task 15's T4 parses its rows, but Task 3 fixes only the column meanings in prose: no table layout, no rule whether paths are install-root-relative or repository-relative (installed primitives must not name `src/superclaude/` paths), no rule for a row without a native label (the code-assigned family is "not mapped" in the spec), and Tasks 9 and 12 do not depend on Task 3. An executor may hardcode the mapping in `classifier.py`, and the map and the code then drift. Do NOT repeat the base's wording "Task 12 reaches it only through Task 9": Task 12 depends on Tasks 7, 9 and 10 (PLAN:169), none of which depends on Task 3.
- Citations: PLAN:136 "the reviewer's own label read through the scale map as 0 or 1"; PLAN:134 "Depends on: Task 5"; PLAN:59 "each native label, the shared outcome per label"; PLAN:209 "T4 (each scale-map row names an existing file and a label present in it)"; PLAN:25 "never a `src/superclaude/` path"; SPEC:748 "yes: code-assigned or not a review loop".
- Rationale: debate C-005 (80%, unanimous) plus probe items.
- Risk: Low.

### Change #6 — MF6 (C-007): Task 10 lacks `Depends on: Task 7`
- Source: Variant 1 F6 second half. Grade: MINOR, blocking false, category other.
- Claim text to use: Task 10 declares `Depends on: Task 9` only but reuses Task 7's reader; file order supplies the edge, so no failure follows.
- Citations: PLAN:146 "Depends on: Task 9"; PLAN:148 "Reuse the reader of Task 7 for ledger rows".
- Rationale: debate C-007 (85%, unanimous).

### Change #7 — MF7 (INV-001): Task 11's tests need code built in Tasks 12 and 13
- Source: invariant probe INV-001 (MEDIUM, UNADDRESSED). Grade: MAJOR, blocking false, category other (a warning, not a blocker: the executor can place the gating code in Task 9's module).
- Claim text to use: Task 11 (`Depends on: Task 9, Task 10`) must test that a finding without a supplied required-item list never gets an M answer from the judge and that a classifier verdict changes no gate outcome except through the safety route, but the plan places the code that asks M, C and E only for supplied inputs in Task 12 and the safety route in Task 13, which run later; the tests pass only if the Task 11 executor writes gating code the plan assigns elsewhere.
- Citations: PLAN:157 "Depends on: Task 9, Task 10"; PLAN:165 "A test asserts that a finding without a supplied required-item list never gets an M answer from the judge."; PLAN:171 "asks M, C and E only for findings whose inputs `classifier_inputs.py` supplied"; PLAN:159 "a classifier verdict changes no gate outcome except through the safety route".
- Risk: Medium (single-source finding, not debated).

### Change #8 — MF8 (INV-004, INV-005): two acceptance and wording nits
- Source: invariant probe. Grade: MINOR, blocking false, category other.
- Claim text to use: Task 2's check `grep -n "src/superclaude" refs/rule.md` names a path that does not exist from the repository root, so grep errors and prints nothing and the check passes without testing anything (the other greps use the full path); Task 12 lists `lint` and `estimate` among the "existing" review subcommands although `lint_cmd.py` and `estimate_cmd.py` do not exist, so `review --help` shows 7 subcommands, not 9.
- Citations: PLAN:53 "`grep -n \"src/superclaude\" refs/rule.md` prints nothing"; PLAN:171 "the existing `panel`, `merge`, `ledger`, `telemetry`, `lint`, `estimate`, `cluster`, `verify` and `manifest` subcommands"; src/superclaude/cli/review/__init__.py:24-25 "lint_cmd" and "estimate_cmd" (read the real lines and quote the exact text).
- Risk: Low.

### Change #9 — MF9 (T1 observation O7, not debated): `sweep-flagged` is not in the spec's item-state table
- Source: the T1 card only (calibrator confidence 0.60); label it "[T1-only, not debated]". Grade: MINOR, blocking false, category other.
- Claim text to use: Task 4 and Task 7 name `sweep-flagged` as an item state, but the spec's ledger item-state table has eight states and not this one; it comes from the stage 2 request. The installed reference would also name rollout stages.
- Citations: PLAN:78 "The file states the `sweep-flagged` rule"; SPEC:383 "`recorded` | stored, not yet offered" (read SPEC:379-390 and quote one real row); PLAN:72 (read the real line and quote the `sweep-flagged` sentence).
- Risk: Low.

### Removals from the base (record in the merge log)
1. Variant 1 F3 second half (Task 1 `verify-sync` line false after Tasks 2 to 6): refuted, PLAN:25 is a standing order to run `make sync-dev` after editing.
2. Variant 1 F5 (`.dev/pr-monitor/` versus Task 5's grep): refuted, PLAN:72 asks for the location rule only and the PLAN:87 grep catches a verbatim copy (C-006, NOT-A-DEFECT, unanimous).
3. Variant 1 F4 wording "Task 12 reaches it only through Task 9": wrong, see Change #5.
4. Variant 1 Checked "9 `review` subcommands": wrong, 7 exist (see Change #8).
5. Variant 1 F2's "blocking true" grade: replaced by non-blocking (Change #3).

## Changes NOT Being Made

| Diff point | Non-base approach | Why the base or the debate outcome stands |
|------------|-------------------|-------------------------------------------|
| C-004 / X-001 | Variant 2 grades the missing mapping blocking | 2 of 3 advocates moved to non-blocking after reading that no stated check fails and a one-sentence decision closes it; the dissent is recorded in the card text |
| C-008 | Variant 3 F3 (fence-opener text in `doctor.py` versus the T2 scan) | judged NOT-A-DEFECT by 2 of 3 (PLAN:197 asks for a version comparison, not a literal); not carried into the card |
| C-009 | Variant 3 F4 (sketch test location) | NOT-A-DEFECT unanimously after Round 2 (PLAN:139 is a one-off check, PLAN:159 imports no sketch) |
| C-010 | Variant 1 F3 second half | NOT-A-DEFECT unanimously (PLAN:25) |
| S-002 | Variant 2's absolute citation paths | cosmetic; the merged card uses repo-relative paths |

## Risk Summary

| Change | Risk | Impact | Rollback |
|--------|------|--------|----------|
| #1 to #2 | Low | blocking findings; wording must stay faithful to the cited lines | restore from the variant text |
| #3 | Medium | regrades a base finding from blocking to non-blocking | restore the base grade if the validator cannot verify the citations |
| #4 | Medium | records a dissent | none needed |
| #5 to #9 | Low to Medium | non-blocking findings; #7 and #9 rest on one source | drop the entry if its citations fail the evidence gate |

## Review Status

Auto-approved (non-interactive). Timestamp 2026-11-16T03:55:02Z.
