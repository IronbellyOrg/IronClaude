# QA Report - Synthesis Content Quality, Partition 1

**Topic:** Phase 5 synthesis gate
**Date:** 2026-10-24
**Status:** Complete (report-only; returned as text for parent persistence because this reviewer may not write report files)
**Phase:** synthesis-gate
**Lens:** content-quality
**Task item:** Step 5.19
**Partition:** 1 of 2
**Fix cycle:** N/A
**Fix authorization:** false
**Governing template:** Project rf-qa Output Format (All Phases); tech-research Synthesis QA Agent Prompt

---

## Overall Verdict: FAIL

## Criteria and Partition Scope
- **Assigned files:** `synthesis/synth-01-problem-current-state.md` (sections 1-2), `synthesis/synth-02-target-gaps.md` (sections 3-4), `synthesis/synth-03-external-findings.md` (section 5). Also read: the corresponding research (`research/01`-`06` case files, `evidence-deck.md`, `scope-rules.md`, `web-01-gap-applicability.md`) and `gaps-and-questions.md`.
- **Criteria applied:** Synthesis Gate checks 7-12 from `/config/.claude/skills/tech-research/SKILL.md:925-937`: cross-section consistency, no claims backed only by documentation in Section 2, stale documentation surfaced in Section 4 or 9, content rules (`SKILL.md:1579-1601`), section completeness with no placeholders, and real paths with existing parent directories. Step 5.19 adds four more requirements: protocol instructions must be kept apart from proven runtime behavior, definitions/counts/causal classes must stay faithful, uncertainty must be kept, and no edits are allowed.
- **Cross-partition reads:** Check 7 (every Section 4 gap has a Section 8 step) and check 9 (stale items in Section 4 or 9) depend on partition-2 files. Only for those two checks, I read `synth-05-implementation-plan.md` §8 in full and searched `synth-06-questions-evidence.md`.

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 7 | Cross-section consistency | FAIL | **Consistent:** counts and definitions in all three files and `gaps-and-questions.md:11,43-44,56`. These include 30 slots, seven synthetic, three strict, Orca 16→14/2→20 items, CI 18 → 5 medium/11 low/0 high, monitor 7 verdicts/5 reviewers/5 repairs/4 `fix`, oracle 67/78 tests, credential 3 results/8 observations. They match the deck (`evidence-deck.md:36-58,94-105,149-158,495`), `05-session:18-20,56,501` and `04-session:283`. All primary raw anchors cited in synth-01 §2.2 appear in the matching case file (checked mechanically for all 6 cases). **Defect:** two Section 4 gaps have no Section 8 step (Issue 2). |
| 8 | No claims backed only by documentation in Section 2 | PASS | §2.3 labels protocol rows "[SOURCE-VERIFIED checkout protocol instructions]" and says they are not runtime proof (synth-01:75,102). I checked each row against live source: `sc-workflow-protocol/SKILL.md:48-72`, `refs/quality-gates.md:24-41`, `sc-implement-protocol/refs/qa.md:9-17,25-52,62-68,80-90`, `refs/retry.md:142-146`, `refs/ledger.md:138-158`, `refs/managed-workspace.md:42-68,78-85`. Each claim is supported, or comes from `scope-rules.md:43,54-58`. Historical rule changes are tied to captured loads (`scope-rules.md:66-73`), not current files. |
| 9 | Stale documentation surfaced in Section 4 or 9 | FAIL | The research has no `[CODE-CONTRADICTED]`/`[STALE DOC]` tags (search of `research/` returned nothing). So I checked each "Stale Documentation Found" section. The deck lists nine items (`evidence-deck.md:855-863`). Both Orca `[CONTRADICTION]` markers are in §4 row 3 and §2.5. Two Orca items reach neither Section 4 nor Section 9 (Issue 1). |
| 10 | Content rules (tables over prose, no full code) | FAIL | No code reproduction. One ASCII diagram (synth-01:86-100), labeled as an instruction diagram. **Defect:** lists of controls written as prose paragraphs (Issue 3). |
| 11 | All expected sections populated, no placeholders | FAIL | Searching the three files for `RF_PLACEHOLDER\|TODO\|TBD\|FIXME\|[...]` found nothing. All template fields are present: §1 question/why/trigger, §2.N summary (§2.7), §3 desired behavior/success criteria/constraints, §4 table, §5 justified N/A with 5.N summary (§5.4). **Defect:** out-of-date delivery-status lines and handoff tables (Issue 4). |
| 12 | No made-up paths (parent directories exist) | PASS | All cited files exist and every cited line range is within file length. This covers six protocol sources, `qa/qa-research-verification-structural.md` (282 lines; timestamps confirmed at 101-108), all research files and the task file. All six primary JSONL logs from `evidence-deck.md:123-128` exist. |

## Summary
- Checks passed: 2 / 6
- Checks failed: 4
- Critical issues: 0 (Important: 2, Minor: 2)
- Issues fixed in-place: 0 (report-only, no edits made)
- **Confidence:** Verified: 6/6 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 21 | Grep: 0 (content searches ran inside Bash) | Glob: 0 | Bash: 16. No web research was done (none needed). The 21 Read calls exceed the 6 checklist items.

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | IMPORTANT | synth-02 §4 table (lines 48-61); synth-01 §2.5 (128) and §2.6 Orca row (145); synth-02 coverage Orca row (79) | **Check 9.** Two research stale-documentation findings are missing from Section 4 and Section 9. The case lists three (`research/01-session-ac2cd1fd.md:356`) and the deck repeats two of them (`evidence-deck.md:858-859`): an inaccurate review-closure count and a condensed persisted targeted verdict that drops detail kept only in the JSONL return (`01-session:81,253`). (a) The 13-fixed/3-partial versus 14/2 closure error appears only in Section 2.5 (synth-01:128), not Section 4. (b) The condensed-verdict omission appears nowhere in synth-01/02/03. A search of synth-06 for "condens", "omit", "thirteen" and "three partial" finds neither item in Section 9. synth-01:141 says "exclusions are explicit rather than silent", but this item is neither represented nor listed as excluded. | Add both items to a Section 4 row, for example by extending "Ledger history alone cannot reconstruct every review" (synth-02:57) to cover persisted summaries/verdicts that drop detail. Cite `01-session-ac2cd1fd.md:81,90-103,253` and `evidence-deck.md:613`. Alternatively, have partition 2 add them to Section 9. Then update the Orca rows in synth-01 §2.6 and the synth-02 coverage table. |
| 2 | IMPORTANT | synth-02 §4 rows 6 (line 55) and 9 (line 58) ↔ `synth-05-implementation-plan.md` §8 | **Check 7.** Every Section 4 gap must have a Section 8 step. Ten of twelve gaps map to a Phase 1-3 step. Two do not. Row 6 covers consent/scope/ruling records: the credential Task 10 correction going beyond its named authority, and the missing ruling-ledger entry. Row 9 covers `head-moved` being read as actual HEAD movement. Neither has a Phase 1-3 step. They appear only as "retain" notes in the §8 coverage table (synth-05:115,118). The closest step, "Check feasibility and correction authority" (synth-05:76), lists only the oracle and rendering cases and never the credential overreach. | Either add explicit §8 rows (for example, "Separate consent, authorized repair scope and ruling records", bound to the credential case and `evidence-deck.md:564-569`; and "Interpret guard categories by their mapped condition", bound to `evidence-deck.md:631,709,729`), or have synth-02's Notes name the §8 row/constraint that handles each gap. synth-05 belongs to partition 2; the consolidator should route this item to both. |
| 3 | MINOR | synth-01:69; synth-02:69; synth-01:48 | **Check 10** (`SKILL.md:1598` "Tables over prose whenever presenting multi-item data"). synth-01:69 lists seven or more separate controls in one paragraph: oracle repairs, monitor Tasks 10/11, initial credential, missing comment, retry-feature, seven compliant tasks, nine compliant reviews. synth-02:69 lists four controls in prose. synth-01:48 puts two cases' observation windows (four timestamps/records) in prose. | Turn the control lists into a Control / Observed evidence / What it challenges / Limit table (the deck table at `evidence-deck.md:645-658` already has this shape). Put the two observation windows into the §2.1 table or a small boundary table. |
| 4 | MINOR | synth-01:4,7,173-176; synth-02:5,8,91-94; synth-03:5-6,85-88 | **Check 11.** The components still describe their pre-persistence handoff as current. synth-01:4 says "parent persistence ... pending", and the NEXT rows ask for "Parent persistence at the intended ... destination". All three files are on disk, and the persistence is logged at task file lines 651-657. The sibling artifacts carry a dated Parent Persistence Record that resolves this (`evidence-deck.md:898-900`, `web-01-gap-applicability.md:180-182`, `synth-04:339`, hypothesis cards §10.5). These three do not, so their in-file status contradicts disk. The chat-style DONE/NEXT tables are also not report content and would carry into assembly. | Append a dated Parent Persistence Record to each file, in the same form as `web-01:180-182` (a receipt, not an approval). Mark the header persistence lines and the DONE/NEXT tables as excluded from assembly. Do not rewrite the producers' original text. |

## Actions Taken
None. This is a report-only review (fix_authorization: false). No target file, task file or other artifact was edited, and no agents, tests, Git, staging, archive, move, delete or external publication were used.

## Self-Audit
- **Counts and causal classes:** I checked every count in synth-01 §2.1-2.2 and synth-02 §3 against the deck and the case files, plus all 54 primary raw record numbers in synth-01 §2.2. The six-class taxonomy in synth-01:11 and synth-02:20 matches `evidence-deck.md:36-43`. The strict-subset definitions match `evidence-deck.md:51-56`. No faithfulness defect was found.
- **Uncertainty:** unknowns are kept as unknowns, not rewritten. Examples: rubric updater (synth-01:104), earlier-miss reasons (synth-01:162), credential confounding (synth-02:52), v4 not reviewed (synth-01:62), rendering not verified (synth-01:118). Each matches `evidence-deck.md:831-845` and `gaps-and-questions.md:57-59`.
- **Instruction versus runtime:** I read every protocol source range cited in synth-01 §2.3 directly. One claim ("fresh subagents", synth-01:80) is worded "always subagents" at `qa.md:86`. "Fresh" is supported for operator and re-run reviews by `ledger.md:152-154`, and as "independent" by `scope-rules.md:43`. I judged it not a defect.
- **External N/A (synth-03):** the five-row deck table plus the extra limits are all mapped. All 15 deck questions (`evidence-deck.md:831-845`) map to the nine grouped rows in synth-03 §5.1 and to the 18 rows at `web-01:32-49`. The provider record matches `web-01:99-113`.
- **Doc-only scan:** synth-01:137 correctly states that no case establishes stale production-documentation architecture as a cause, which agrees with each case's "Stale Documentation Found" section (`01:356`, `02:302`, `03:310`, `04:272`, `05:308`).

## Partition Limits and Evidence Uncertainty
- [PARTITION NOTE: Cross-file checks are limited to the assigned subset. Full cross-file verification requires merging all partition reports.] Section 6 options reflecting Section 2 evidence, and Section 9 questions not being answered elsewhere, belong to partition 2 and were not judged here.
- Issue 2 and part of Issue 1 involve partition-2 files (synth-05, synth-06). I read synth-05 §8 in full and only searched synth-06. Partition 2 should confirm the Section 9 absence.
- Graph coverage was unavailable for these generated files (hook reported `coverage_unavailable`). All conclusions come from direct reads and literal searches.
- **Out-of-lens observations** (structure lens, checks 1-2 and 4). These are not counted in my verdict and are routed to `qa/qa-synthesis-structure-1.md` reviewers:
  - (a) synth-03:73 adds an H2 heading "## Evidence and Limits" outside the ten-section report structure. synth-01/02 use H3 for the same kind of material.
  - (b) synth-02:60-61 Severity values "Important evidence limit" add a qualifier to the template's Critical/Important/Minor values.
  - (c) synth-01:15 cites task lines 64-75 for a question that names `/sc:workflow` and `/sc:implement`. Those command names appear in `BUILD-REQUEST.md:12`, not in the cited task lines.

## Recommendations
- Before assembly, one serialized fix pass (Step 5.24) should apply all four fixes in this order: Issue 1, then 2, then 3, then 4. The Issue 2 fix needs either a synth-05 change or a synth-02 Notes change. Then re-verify checks 7, 9, 10 and 11 against the sources, not the fix log.
- No re-debate is needed. None of these issues changes a hypothesis identity, a count or a causal classification.

## QA Complete
QA synthesis-gate (content-quality, partition 1 of 2) is complete. **Verdict: FAIL.** 2 of 6 checks passed and 4 failed. Issues: 4 (CRITICAL: 0, IMPORTANT: 2, MINOR: 2). All 4 must be resolved before proceeding.

| Status | Result |
|---|---|
| DONE | Reviewed synth-01, synth-02 and synth-03 against checks 7-12 using primary sources. Verdict FAIL with 4 issues. No files edited. |
| NEXT | Parent persists this exact text at `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/qa/qa-synthesis-content-1.md`, replacing the prepared stub, for Step 5.23 consolidation. |