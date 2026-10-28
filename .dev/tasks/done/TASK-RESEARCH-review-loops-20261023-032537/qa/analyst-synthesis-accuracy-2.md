# Synthesis Quality Review - Accuracy, Partition 2

**Topic:** Phase 5 synthesis gate
**Date:** 2026-10-24
**Status:** Complete (report-only review; text returned for parent persistence because this reviewer's instructions prohibit writing report files)
**Files reviewed:** 3 target synthesis files (`synthesis/synth-04-options-recommendation.md`, `synthesis/synth-05-implementation-plan.md`, `synthesis/synth-06-questions-evidence.md`), plus 5 supporting hypothesis cards and 10 debate and recovery artifacts listed in Self-Audit
**Lens:** synthesis-accuracy
**Task item:** Step 5.14
**Partition:** 2 of 2
**Governing template:** Project rf-analyst Synthesis Quality Review Output Format; tech-research synthesis checklist (`/config/.claude/skills/tech-research/SKILL.md:1506-1521`, Report Structure `:1311-1487`)

## Overall Verdict: FAIL (7 issues: 0 critical, 0 important, 7 minor)

## Per-File Review

### synth-04-options-recommendation.md
**Sections covered:** 6 and 7
**Verdict:** FAIL (5 issues)

| Check # | Check | Result | Evidence/Issue |
|---------|-------|--------|---------------|
| 1 | Section headers match template | PASS | `## 6. Options Analysis`, `### Option A-E`, `**Description:**`, `**How it works:**`, `### Options Comparison`, `## 7. Recommendation`, `**Recommended approach:**` and `**Rationale:**` are all present (lines 14-195). The added 6.0 and 7.1-7.8 subsections are extra content, and the adaptations are declared in the header at line 5. |
| 2 | Table column structure | PASS | Each option table uses Aspect/Assessment and keeps Effort, Risk, Reuse, Files, Pros and Cons. The comparison table uses Criterion / Option A-E and keeps Effort, Risk, Maintainability, Integration complexity and Reuse potential (lines 179-191). Maintainability is N/A with a reason. |
| 3 | No fabricated content | FAIL | Two statements claim more than their cited sources say. Line 215: "Narrow reach in one work family" is cited to `debate-transcript.md:381,384`, but line 381 limits "one work family" to the credential packages. (Issue 1.) Line 240: says the refactor plan "cited ... the V4 advocate's own reversal", but `refactor-plan.md:32` does not mention the reversal. (Issue 2.) |
| 4 | Citations to actual evidence | FAIL | Line 58: the credential clause cites `evidence-deck.md:647-648` (oracle and monitor controls) and `hypothesis-01.md` section 6 (no credential text). The supporting row is deck `:649`. (Issue 3.) Line 90: attributes a critique to the V3, V4 and V5 advocates but cites only V3 (`:129,343`) and V5 (`:425`). (Issue 4.) About 60 other anchors were rechecked and are correct (see Self-Audit). |
| 5 | At least 2 options with pros/cons tables | PASS | Five options, each with Pros and Cons rows (lines 69-70, 96-97, 123-124, 150-151, 174-175). |
| 6 | Plan steps are specific (applied only to the 7.6 cross-reference to Section 8) | FAIL | Line 286 says "Step-level targets are in Section 8". That is false for two steps: step 1 includes the monitor, which is absent from the synth-05 acceptance-check row (synth-05 line 72), and step 4 has no Section 8 row at all. (Issue 5.) |
| 10 | Key-finding coverage | PASS | The 7.7 table maps every case report, the deck, the rule map and the gap register. The exclusion of the screening slices is justified at line 311. Checked against each case report's Summary. |
| S1 | Five causes genuinely assessed | PASS | Each of the five options has its own mechanism, support, opposition, alternatives, scope, falsification and strength. The content matches cards 01-05 (counterevidence and scope sections read directly). |
| S2 | Actual debate support | PASS (except Issues 2 and 4) | Final orders (7.2) match `debate-transcript.md:477-484` exactly. The pairwise tallies match `:486` and `invariant-probe.md:43`. The "positions held" per rank are correct. The Round 2 A-001 responses at `:277,316,356,397,438` are correct. |
| S3 | Comparative likelihood kept distinct from artifact quality; no probabilities | PASS | 6.0 and 7.3 separate writing convergence, writing base and process confidence from causal order. The writing-score order V4, V5, V2, V3, V1 matches `base-selection.md:150`. A search for `%` found none. |
| S4 | No lost case or control, invented run or implemented fix | PASS | All proposed checks are labelled unexecuted (lines 61, 88, 115, 142, 166, 286). The oracle, monitor Tasks 10/11, initial credential and 14-accepted controls are retained. |

### synth-05-implementation-plan.md
**Sections covered:** 8
**Verdict:** PASS (no defect located inside this file; see Self-Audit. Issue 5 is a defect in synth-04's claim about this file.)

| Check # | Check | Result | Evidence/Issue |
|---------|-------|--------|---------------|
| 1 | Section headers match template | PASS | `## 8. Implementation Plan`, `### Phase 1-3` with `**Goal:**` and `**Dependencies:**`, and `### Integration Checklist` are present. The research-only adaptation is declared at line 5. |
| 2 | Table column structure | PASS | Every phase table uses Step / Action / Files / Details. The Integration Checklist is a table of N/A items with reasons, which fits the declared research-only scope. |
| 3 | No fabricated content | PASS | Record anchors match the deck transition matrix (`evidence-deck.md:378-391`): 544/545, 841, 585, 759-762, 1240, 849, 874/884, 893/902, 906, 383/450, 521/573/668, 430/443/450 and 506. The three current rendering targets exist, and their cited lines match: plan `:81-87` (Task 6 and "when `man` is available"), log `:1-3` (no renderers, 275-byte notice) and progress `:14-18` (cannot-verify, head-moved, ruling, FINAL pass). |
| 4 | Citations to actual evidence | PASS | Rule map `:66-88`, gap register `:33-59`/`:43-59`, web-01 `:97-148` and deck `:814-847` were rechecked; each supports the statement it is attached to. |
| 5 | Options | N/A | Not in this section. |
| 6 | Plan steps are specific, with file paths | PASS | Every input name resolves to an absolute path (lines 29-41). Each step states its expected observation and what would strengthen or weaken the explanation. Nothing invents a function or signature (line 128). |
| 10 | Key-finding coverage | PASS | The required-input table (lines 111-122) covers all nine inputs. Its claims match the case Summaries and the deck. |
| S4 | No invented run or implemented fix | PASS | Every check is marked UNEXECUTED (lines 4, 132). Controls are preserved (line 88). |

### synth-06-questions-evidence.md
**Sections covered:** 9 and 10
**Verdict:** FAIL (2 issues)

| Check # | Check | Result | Evidence/Issue |
|---------|-------|--------|---------------|
| 1 | Section headers match template | FAIL | The Report Structure (`SKILL.md:1471-1486`) expects `### Codebase Research`, `### Web Research` (File / Topic) and `### Gaps Log`. synth-06 replaces them with custom 10.1-10.8 subsections: the web record is placed in the research table (line 83) and the gaps log in 10.7 (line 206). No adaptation is stated. (Issue 6.) |
| 2 | Table column structure | PASS | Section 9 uses # / Question / Impact / Suggested Resolution. The Section 10 tables use File / Topic / Agent Type. |
| 3 | No fabricated content | FAIL | Statements about named current files are now false. Line 123 says hypothesis-04 has a "debate pending" header, but it now reads "Post-debate format-only presentation" (`hypothesis-04.md:7`); the wording exists only in `variant-4-original.md:5,8`. Line 126 says card ten-section format acceptance is unresolved, but all five cards are now ten-section (each has a 10.5 persistence record). Lines 128 and 223 say synth-04 is absent, but it now exists. Line 190 says the intake is an unfinished skeleton, but it is now `Status: Complete`. The 22:14:30Z snapshot is disclosed, but these rows describe files that have since changed. (Issue 7.) |
| 4 | Citations to actual evidence | PASS | Rechecked: web-01 `:97-123` (zero queries, sources and findings), fix-log `:95-116` (records 48-49 map to 50-51), phase-3 gate `:67-103` (20:48:38, cycle 2 of 3, no reset) and phase-4 gate `:134-177`. |
| 5 | Options | N/A | Not in this section. |
| 6 | Plan | N/A | Not in this section. |
| 10 | Key-finding coverage | PASS | Questions 2-17 map one-to-one to deck gaps `:831-845`. Questions 1, 18, 19 and 20 trace to the gap register and the return contract. All 191 QA, 9 phase-output and 4 resume files listed exist (204/204 tested). The counts add up: 133+58=191; 23+10+191+17+9+4+4=258. The current QA count of 202 equals 191 plus 11 files created after the snapshot. |
| S4 | No invented run | PASS | The post-merge PASS and the partial contract status are stated accurately (`return-contract.md:14`; `run-evidence.md:23`). |

## Supporting Cards and Actual Debate Evidence

- **Cards.** All five cards were read directly, chapters 1-9 at least. Their counterevidence, scope and falsification text matches the synth-04 options: card 01 `:97-106`, card 02 `:98-107`, card 03 `:98-107`, card 04 `:101-114`, card 05 `:99-112`. Each card states it is a post-debate format-only presentation of the immutable `variant-N-original.md`. The variant headers for 4 and 5 still carry the pre-debate "pending" status.
- **Debate run is real.** All Round 1 and Round 2 advocate texts carry source-record comments (`debate-transcript.md:17-407`). The Round 2.5 probe has a recorded source (`invariant-probe.md:75`). Round 3 was not run, and the reason is recorded (`:449-450`). The base selection uses tiebreak arithmetic (`base-selection.md:142-155`). The refactor plan has an independent review PASS (`plan-review-evidence.md:9-16`). The merge was recovered from record 71 (`return-contract.md:29`), and the post-merge validation is a PASS.
- **Ranking kept separate from writing quality.** The displayed order V1 > V3 > V2 > V5 > V4 is the refactor plan's provisional judgment (`refactor-plan.md:27-35`). Only V1 first is unanimous. V3 above V2 has 3 of 5 advocates; V4 above V5 has 3 of 5, so the displayed V5-above-V4 follows the 2-of-5 side. synth-04 discloses all of this correctly (lines 238-243).

## Issues Requiring Fixes
| # | File | Check | Issue | Required Fix |
|---|------|-------|-------|-------------|
| 1 | synth-04 | 3 | Line 215 (rank 5 rationale) says "Narrow reach in one work family". The cited `debate-transcript.md:381` says only that the credential packages are one work family. V4's support also includes the documentation baseline case (session 6f744b87), as the file's own line 182 ("Credential (one work family), documentation baseline") and `hypothesis-04.md:109` ("two selected sessions and three package/task contexts") state. Severity: MINOR. | Reword to match the source, for example "narrow reach: credential packages (one work family) plus one documentation baseline context". |
| 2 | synth-04 | 3 | Line 240 says the refactor plan "cited the direct continuation evidence and the V4 advocate's own reversal (`ADV/refactor-plan.md:32`; ...)". `refactor-plan.md:32` cites only the direct continuation evidence; the reversal is in `debate-transcript.md:384-385`, not in the plan. Severity: MINOR. | Attribute only the continuation rationale to the plan, and cite the V4 reversal separately to the transcript. |
| 3 | synth-04 | 4 | Line 58 (Option A Opposition): "The credential proof-only rejection happened while delivery already met the lint criterion" is cited to `hypothesis-01.md` section 6 (no credential text, lines 97-101) and `evidence-deck.md:647-648` (oracle and monitor rows). The supporting deck row is `:649` (also `:389`, `:557`). Severity: MINOR. | Add `research/evidence-deck.md:649` (or `:389`) for the credential clause. |
| 4 | synth-04 | 4 | Line 90 (Option B Debate record) attributes the critique to "the V3, V4 and V5 advocates" but cites only V3 (`:129,343`) and V5 (`:425`). The V4 position exists at `debate-transcript.md:168` and `:379` but is not cited. Severity: MINOR. | Add the V4 citations `:168,379`. |
| 5 | synth-04 (claim about synth-05) | 6 | Line 286 says "Step-level targets are in Section 8". Step 1 names the monitor, but the synth-05 acceptance-check row (line 72) lists only the oracle, Orca planning, CI and the deck. Step 4 (additional independently selected sessions) has no Section 8 row. Severity: MINOR. | Either qualify line 286 (steps 1-3 map to the synth-05 Phase 2 rows; step 4 is a scope decision with no Section 8 target, see synth-06 Question 1), or add the monitor case to the synth-05 acceptance-check Files cell. |
| 6 | synth-06 | 1 | Section 10 omits the template subsections `### Codebase Research`, `### Web Research` (File / Topic) and `### Gaps Log` (`SKILL.md:1475-1486`) and gives no stated adaptation. The web-applicability record sits in the research table (line 83) and the gaps log in 10.7 (line 206). Severity: MINOR. | Add the three template subsections (the 10.x tables may stay beneath them), or state the adaptation in the header the way synth-04 does at line 5. |
| 7 | synth-06 | 3 | Section 10.4 and 10.8 statements about named files are now false for current disk state: the "debate pending" header (line 123), unresolved ten-section format (lines 126, 220), synth-04 absent (lines 128, 223) and the intake being an unfinished skeleton (lines 52, 190). The cards were reformatted and synth-04 was persisted on 2026-10-24. The snapshot time is disclosed, but these rows will mislead if assembled unchanged. Severity: MINOR. | Refresh 10.1, 10.4, 10.6 and 10.8 against current disk. Alternatively, re-point the "debate pending" wording to `variant-4-original.md:5,8` and `variant-5-original.md:5,8` and label each row as true only at 22:14:30Z. |

## Summary
- Files passed: 1 (synth-05)
- Files failed: 2 (synth-04, synth-06)
- Total issues: 7
- Critical issues (block assembly): 0. All seven are MINOR, but under the gate rule any issue of any severity fails the gate.

## Self-Audit

What I checked, and how:

1. **Governing template.** Read the task file Step 5.14 (lines 317-319) and its neighbours 5.13-5.22. Read the SKILL Report Structure through the Synthesis Quality Review Checklist (lines 1311-1531) and the prepared stub.
2. **Targets.** Read all three targets in full: synth-04 (341 lines), synth-05 (139) and synth-06 (231).
3. **Debate evidence.** Read the full debate transcript (lines 1-490), invariant probe, refactor plan, plan-review evidence, diff analysis, return contract, run evidence and merged analysis. Read `base-selection.md` lines 1-180.
4. **Cards and originals.** Read cards 01-05 (01: 39-148; 02: 27-160; 03: 27-160; 04: 1-160; 05: 1-165). Read the variant-4 and variant-5 original headers.
5. **Research sources.** Read `scope-rules.md` and `gaps-and-questions.md` in full. Read `evidence-deck.md` lines 40-134, 370-429, 555-739 and 805-900.
6. **Primary-source spot checks.** Checked the oracle 67/78 test counts at `02:228`, the monitor 640-line write at `05:56`, `/usr/bin/man` at `03:72-88`, the Git tree hashes at `03:216-237`, record 2028 at `06:222`, records 150/151 at `01:64`, records 1164-1170 at `05:160`, the CI downgrades at `04:16,187,199`, the same-source-hash claim at `01:340` and the held-back fixture at `02:63`.
7. **Package-wide and external checks.** Tested existence of all 204 files listed in synth-06 and recounted every directory. Compared synth-05/06 hashes with the intake record (both match: `d5cdf596…`, `8ac285ee…`). Read the external Coder rendering-package lines, read-only.

Why synth-05 is clean: every record anchor, path and line range it cites resolved to supporting text; its inputs exist; its checks stay unexecuted and research-only; and its controls survive.

## Partition Limits and Evidence Boundaries

- [PARTITION NOTE: Cross-file checks limited to assigned subset. Full cross-file analysis requires merging all partition reports.] synth-01 to synth-03 are out of scope, and cross-references into them were not verified.
- **Lens boundary.** This lens covers checklist items 1-5 and 10 plus the Step 5.14-specific checks. Issue 5 overlaps the source-tracing check (item 7, Step 5.16) and is reported because it is a real error. Items 8-9 belong to other lenses and were not applied exhaustively.
- **Not read:** `base-selection.md` lines 181-577 (raw forward/reverse pass records), `score-source-manifest.json`, `variant-1/2/3-original.md` bodies, card Section 10 Evidence Trails beyond hypothesis-05's opening lines, and screening slices `scope-01` to `scope-05`.
- **Not replayed:** historical JSONL records and nested transcripts. Anchors were checked against the case reports, deck and cards, not against the raw logs.
- **Graph coverage:** unavailable for every package file, so all conclusions come from direct reads.
- **Edits:** none. No target or other file was modified, and no agent, test, Git, staging, archive or publication action was taken.

| Status | Result |
|---|---|
| DONE | Reviewed the three target files against the template, the cards and the debate: FAIL with 7 minor issues (5 in synth-04, 2 in synth-06); synth-05 passes. |
| NEXT | Parent persists this exact text at `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/qa/analyst-synthesis-accuracy-2.md` and routes the 7 issues to the serialized fix step. |