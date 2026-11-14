# Refactoring Plan: Merge into Base (Variant A)

Slot C-10 (pr-review-wire-format-and-slot). Every change below cites the debate (`debate-transcript.md`, Round 1 and Round 2 files, scoring matrix, `invariant-probe.md`) or `diff-analysis.md`; nothing is added that the debate did not conclude. File references: A-R1, A-R2 = `round1-advocate-A.md`, `round2-advocate-A.md`; B-R1, B-R2 likewise for Variant B's advocate; section numbers are theirs. "Probe INV-0xx" means a finding of `invariant-probe.md` (numbered INV-001 to INV-020 in that file); the names INV-003 (R-C01: repair step versus pins) and INV-007 (R-C03: `requested` collapse) without the word probe are the prior-slot invariants both Round 2 files cite; the two numbering sets collide and must not be merged. The plan was reviewed by an independent analytical agent (`plan-review.md`, 18 defects found) and revised for each of them.

## Overview
- Base: Variant A (Proposal A, `variant-1-original.md`), selected by tiebreaker level 1 (debate performance 9 points against 6) after a 2.27% combined margin in B's favour (`base-selection.md`)
- Incorporating strengths from: Variant B (Proposal B, `variant-2-original.md`) and the two Round 2 resolutions (A-R2 section 5, "C10-R"; B-R2 section 6, "C10-R-B" = C10-R plus amendments AM-1 to AM-6)
- Debate status to carry: label agreement 49 of 49 (Round 1: 33 of 49); content-adjusted 44 of 49 (0.90); status BLOCKED_BY_INVARIANTS (5 HIGH UNADDRESSED probe findings); content-unresolved points C-001, C-002, C-006, S-004, S-008; owner items C-008, A-005, A-006 open in both advocates' files
- Planned changes: 17. Settled by both advocates: the slot topology (Change 2), `body` and `reviewer` rules and `confidence` and `original_line` unset (Change 4), the strict `incomplete` core rule (Change 3, first clause), head-SHA binding and cadence (Change 5), report-only first release (Change 6), the corrections of A's factual claims (Change 8), the test and measurement list (Change 9). Contested or unanswered by Variant A, recorded as such: the aggregation rule in Change 1 (B-R2 D1, AM-1), AM-1 to AM-6 (Change 13), the missing-ranges and zero-cluster clauses of the standing rule (Changes 3 and 7), the "CRITICAL never lowered" claim (Change 10), and the test-file choice (Change 2). Open invariant-probe findings touch Changes 1, 3, 5, 6, 7, 9 and 15.
- Planning risk labels below are the orchestrator's labels for how likely the change is to misstate the debate; they are not debate conclusions. The debate's own status is BLOCKED_BY_INVARIANTS.

The merged output is written as `<output>/merged-output.md`: the resolution of slot C-10 as the debate produced it, using A's structure (position, design consequence, evidence, invariants, consistency with C-01 to C-03, tests, effect on PR code review and rf-qa, objection and answer) with the corrections below. Provenance tags follow `refs/artifact-templates.md` Section 6.

## Planned Changes

### Change 1: Replace A's converter input (X-001); aggregation contested (from Variant B, join confirmed by A-R2)
- **Source**: B-R2 section 1.2 and section 2 row 2 and D1; A-R2 section 3 (e) and section 5 condition 3; diff-analysis X-001 (code-contradicted); probe INV-012, INV-018
- **Target**: Base, section 2 and 3.5 (replace)
- **Rationale**: The cluster record holds no severity or category (`cluster.py:352-378`). Settled by both advocates: the converter takes `cluster_v2` output, the same reviewer records joined on `(reviewer_id, id)`, the PR's changed-line ranges, the PR-profile severity table, the requested reviewer ids and the head SHA; path, line, claim and `blocking_any` come from the cluster (member `primary_citation`, representative `claim`); severity and category come from the joined source lines. Contested: A-R2 takes severity as the maximum over joined members with one Finding per cluster; B-R2 accepts the maximum only as "necessary but not sufficient" because it pairs a maximum severity with the representative's category and claim (D1, HIGH; `same_defect_v2` ignores category and claim, `cluster.py:161-181`; the uncalibrated representative is the lowest-ordinal member, `:338-344`) and proposes AM-1; A did not answer; the probe finds AM-1 itself insufficient for same-category clusters (probe INV-012, HIGH). Matrix: C-001 is Hybrid in both Round 2 tables (A 75, B 60); B-R2 row 2 (65) accepts the join and refines the aggregation.
- **Integration point**: Section 2 "`pr_submit` (consumer module)" bullet list; delete the "highest member severity" claim and the "cluster output already holds" sentence in 3.5; state the aggregation as contested.
- **Risk (planning label)**: Medium

### Change 2: New pure module, no `REVIEWERS` entry (base kept; slot axis conceded by B in Round 1)
- **Source**: A-R2 section 4 row 1 and section 5; B-R1 Concession 4; B-R2 sections 1.1 and 2 row 1; matrix S-003, C-004, C-005 (Variant A), S-002 and S-004 (Hybrid)
- **Target**: Base, sections 1 and 2 (keep, add rationale)
- **Rationale**: B conceded the slot axis (S-002, S-003, S-004, C-004, C-005) in B-R1 Concession 4 and accepted a new module "on size and import fan-in, not on purity" in B-R2 1.1. The zero-token rule applies to a module only if it is listed (`test_static_grep.py:37-55, :136-147`). Test-file choice is contested and unanswered by A: B-R2 AM-5 prefers appending the module to `CORE_PURE_FILES` (an additive edit to an existing test file; B says either is acceptable and the stake is low); A-R2 keeps `test_static_grep.py` unedited and all new tests in new files.
- **Integration point**: Section 2; add the pin facts: one ```python fence pinned in four test files; `reviewer_activity` is a literal two-key dict (X-002).
- **Risk (planning label)**: Low

### Change 3: Strict `incomplete` rule, drop the quorum helper (from Variant B, adopted by A); extra clauses contested
- **Source**: A-R2 section 1.1 W5, section 4 row 6, section 5 condition 4; B-R2 section 2 row 6, AM-3, AM-4, D3; X-009, A-013; probe INV-007, INV-008, INV-011
- **Target**: Base, section 2 (the panel presence bullet) and section 5 C-03 paragraph (replace the `min(2, requested)` helper)
- **Rationale**: No quorum rule exists in `cli/review` or `pr_submit` (0 matches); `evaluate_quorum` (`cli/reflect/fallback.py:161-179`) exists but has the wrong shape (swarm `WorkerResult`, model-class diversity). Settled: `incomplete` when any requested reviewer is not `complete` (requested ids minus `complete_reviewers`). A-R2's full standing rule also marks the panel `incomplete` when `changed_ranges` is missing and when every cluster was dropped; B-R2 amends both (AM-3 degrade instead of drop; D3: "every cluster dropped" is vacuously true for zero clusters, AM-4); A did not answer; C-006 is content-unresolved. The probe adds: "requested" defined as the dispatched count lets a partial panel read present (INV-007 probe, HIGH), a reviewer with an empty findings block is invalid without Coverage rows so a clean panel cannot read present (INV-008 probe, HIGH), and an empty requested set reads present (INV-011 probe, HIGH).
- **Integration point**: Section 5 C-03; section 2 standing bullet.
- **Risk (planning label)**: High (three HIGH probe findings touch the rule)

### Change 4: `body`, `in_diff`, `confidence`, `original_line`, `reviewer` rules (from B, adopted by A)
- **Source**: A-R2 section 1.1 W2, W3, W6, section 4 rows 3, 5, 7; B-R2 sections 1.3, 1.4, 2 rows 3 to 5, 7; matrix C-002 (Hybrid 60/60), C-010, C-016, X-010
- **Target**: Base, section 2 (adapter owns list) and 3.4
- **Rationale**: `body` is the representative's `claim` verbatim (`fix_key` hashes path, line, body, `models.py:196-207`); `confidence` unset (a `disputed`-derived "low" would lower a tier, `severity_router.py:173-175`); `original_line` unset (a panel finding always has an integer line); `reviewer = "panel"` set by code (`severity_router.py:118` defaults to `"augment"`). `in_diff` is computed by the converter from `changed_ranges`; `pr_submit` has no hunk parser, so this is new code and A's premise that the pre-step holds the diff is [UNVERIFIED] (A-R1 Concession 5, X-010); reviewer-stated values are only compared (M2). The converter owns these keys; no key is added to the findings-v2 line and the record is never mutated (B withdrew harness injection and T0 unless keys are promoted). What to do when ranges are missing is contested (Change 7, AM-3).
- **Integration point**: Section 2 adapter bullets; section 3.4 (replace the "set from cluster facts" sentence).
- **Risk (planning label)**: Low

### Change 5: Head-SHA binding and cadence (from Variant B, adopted by A)
- **Source**: A-R2 section 1.1 W7 and section 4 row 11; B-R2 section 2 row 11; A-008; probe INV-001
- **Target**: Base, section 4 last bullet (replace "needs a cycle id")
- **Rationale**: The `panel` field carries the reviewed head SHA; a result is valid only for that SHA; the panel runs once per PR head SHA; no automatic re-run after a fix push in the first release (cost unmeasured, GQ-177). The probe records that the standing enum has no stale value (probe INV-001, MEDIUM) and that standing, SHA and dropped list have no durable home across `--resume` (probe INV-002, HIGH).
- **Integration point**: Section 4 and section 2 (sibling field definition).
- **Risk (planning label)**: Medium

### Change 6: First release is report-only; bots-silent and thread-less defaults (from both Round 2 files)
- **Source**: A-R2 section 4 rows 8 and 9 and section 5 conditions 1 and 7; B-R2 sections 1.5 and 2 rows 8 and 9, D5; probe INV-014, INV-015
- **Target**: Base, new subsection in section 2 and section 4 (new)
- **Rationale**: Both advocates: panel findings are converted, remapped and routed, listed in the summary and the `panel` field, but are not appended to `decision["used"]` (`SKILL.md:175-178`) and drive no push until the owner decides A-005, C-008 and INV-J. Thread-less rule on promotion: one PR conversation follow-up (`refs/thread-reply.md:92-99`), callbacks skip findings with no integer `comment_id` (`fsm.py:1203-1205`). `terminal_augment_no_response` stays keyed to the two bots because the panel is not in `merge_wait`. B adds D5 (a `present` panel with blocking clusters beside `terminal_clean`), handled by AM-4 (contested). The probe finds the report-only guarantee not enforced against the dedup group (probe INV-014) and the `terminal_clean` wording rule narrower than the posted thread and status value (probe INV-015).
- **Integration point**: New "Release scope" subsection after section 2.
- **Risk (planning label)**: Medium

### Change 7: Per-cluster conversion, dropped list (from both); missing-ranges rule contested
- **Source**: A-R2 section 3 (c) and section 5 condition 2; B-R2 section 3 row (c), D4, AM-3; probe INV-009
- **Target**: Base, section 2 (new bullet)
- **Rationale**: The bot gate drops a whole batch on one `ValueError` (`SKILL.md:118-124, 143-149`); correct for bots (re-poll), wrong for a panel (no re-poll). Settled: convert per cluster, each in its own `try`; a malformed primary citation, join miss or empty claim is counted in `dropped` with a reason; B adds that a dropped cluster names its `cluster_id` and the reviewer-stated severity. Contested: A-R2 counts a missing `changed_ranges` as a drop reason (nothing converts, panel `incomplete`); B-R2 D4/AM-3: convert with `in_diff` unset and standing `incomplete`, never drop (see Change 13). The probe notes the unit of "dropped" (cluster, category group or chain member) is undefined (probe INV-009, MEDIUM).
- **Integration point**: Section 2.
- **Risk (planning label)**: Medium

### Change 8: Correct A's factual claims (X-002, X-003, X-004, A-004) (from diff analysis and both advocates)
- **Source**: diff-analysis X-002, X-003, X-004, A-004; A-R1 Concessions 2 and 3; B-R1 strength 8
- **Target**: Base, sections 3.3, 6.1, 8 (replace)
- **Rationale**: 47 `test_*.py` files (49 `.py`), not 50; `reviewers` appears 13 times in 4 files including one fixture; no test pins the Output Contract `reviewers` row (only the `merge_guard` row and heading order are sliced, `test_merge_guard_protocol.py:498-508`); A's pin claim (`test_codex_reviews.py:285-295, :705`) holds only for a B that edits `reviewer_activity`, which B does not; downstream also reads `in_diff`, `verification_status`, `fix_key` and `comment_id`/`thread_id` (`fsm.py:902-906, :1064-1074`, `models.py:196-207`). A's slot argument becomes semantic: five two-name functions carry carve-outs (`reviewers.py:47-78, :276, :395-424`), `list_review_threads` has no caller and `reviewer_identities` no test, and `merge_wait` needs guards at `:412` and `:420`.
- **Integration point**: Sections 3.3, 3.4, 6.1, 8 (the "four fields" sentence).
- **Risk (planning label)**: Low

### Change 9: Adopt B's tests and measurements (from Variant B)
- **Source**: B section 6; B-R2 section 6; A-R2 section 5 "Tests and measurements"; probe INV-019
- **Target**: Base, section 6 (append and restate)
- **Rationale**: T1 parity of the converter's output dict through `finding_from_comment`; T3 pin that `merge_wait`, `reviewer_activity` and the python-fence count are unchanged and `terminal_augment_no_response` stays keyed to the two bots; T4 grounding; M1 cost per round (needed by both positions); M2 reviewer-stated versus hunk-computed `in_diff` (only if the template asks for the optional key, B D7); M3 later-wave use of `quote`, a second citation, `blocking`; M4 (B-R2: share of clusters spanning more than one category); U-001 equivalence run on fixtures that hold source blocks; golden fixtures including CRITICAL in a non-representative member, join miss, empty claim, missing ranges; T0 only on promotion. A's R2 keeps all new tests in new files (see Change 2 for the contested append). Fix A's inconsistency: 6.1 "no existing test edited" versus 6.2 "add to the static check". The probe adds that T1 compares against a hand-written dict and would not catch the converter's real key set (probe INV-019, MEDIUM).
- **Integration point**: Section 6.
- **Risk (planning label)**: Low

### Change 10: Router facts from B (U-008, U-009, U-010); "CRITICAL never lowered" contested
- **Source**: diff-analysis U-004, U-008 to U-010; B sections 3.2 item 3b, 3.4, 3.1 item 3; B-R2 D2, AM-2
- **Target**: Base, sections 2 and 4 (insert)
- **Rationale**: A local always-answering reviewer in the pair set would make `terminal_augment_no_response` unreachable (`reviewers.py:420`), which A avoids by construction and now says so; a MAJOR mapped to High takes `--depth deep --fix` (`severity_router.py:56-58`); `ROLES` already contains `diff` and `source` (`findings_v2.py:35`). Severity table default in A-R2 row 10: CRITICAL to `critical`; MAJOR with `blocking_any` to `medium`; else `low`; the table is the PR module's choice (INV-J, owner-decidable, confidence 55 in A-R2). A's claim that this table "never lowers a CRITICAL" (base strength, U-004) is challenged by B-R2 D2 (router category ceilings and the `in_diff` drop act after the table: `severity_router.py:34-53, :171, :178-189`); A did not answer; the merged text must state it as contested and not as fact.
- **Integration point**: Section 2 and section 4.
- **Risk (planning label)**: Medium

### Change 11: Prerequisites owned elsewhere (from A-R2 section 3 "found on the way" and B-R2 section 3)
- **Source**: A-R2 section 5 condition 5; B-R2 AM-6, D7; diff-analysis A-003; probe INV-005, INV-018
- **Target**: Base, section 2 (shared core bullets)
- **Rationale**: The core category set (6 values, `findings.py:15-22`) shares no value with the router's 18 (`severity_router.py:34-53`); one out-of-set category invalidates a reviewer's whole block (`findings_v2.py:109-110, :299-303`), after which `cluster_v2` ignores it. FX-5 parameters on `check_finding` with today's constants as defaults are prerequisite work for both positions; B-R2 states the minimum is the category set (severity and `lens=None` work today; A-R2 asked for category, severity and lens). `snapshot_file_list` must list the PR head tree, because only resolved citations cluster (`cluster.py:115, :170-179`) (AM-6, unanswered by A). The PR template says the first citation is the defect location (C-07). The probe adds that the parameter must also reach `parse_block` and the CLI or an in-process pre-step (probe INV-018, MEDIUM).
- **Integration point**: Section 2.
- **Risk (planning label)**: Medium

### Change 12: Restate the invariant table (A, B, INV ids)
- **Source**: A-R1 and B-R1 "Invariants"; A-R2 section 5; B-R2 section 6
- **Target**: Base, section 4 (replace)
- **Rationale**: Held: INV-E HIGH (no edit to `Finding`, `Severity`, FSM, `reviewers.py`; an additive list entry in an existing test file only if AM-5 is taken), INV-A, INV-B, INV-D, INV-C (not engaged, no key added to a line). Open in both Round 2 files: INV-G HIGH (C-07); INV-I HIGH (held as reporting only: nobody traced `terminal_clean`, set at eight sites in `fsm.py`: 241, 805, 872, 1026, 1085, 1120, 1145, 1253); INV-007 (R-C03) HIGH (`requested` collapse); INV-003 (R-C01) HIGH (repair step versus pins; in a PR one bad line invalidates a reviewer's whole block); INV-J MEDIUM; INV-K MEDIUM (thread-less skip is prose and callback behaviour, unpinned); INV-F MEDIUM (open until the prose exists). B-R2 only: INV-L (new, HIGH before promotion, MEDIUM in the report-only release: cluster conversion must not collapse distinct defects) and INV-M (new, MEDIUM: routed tier versus reviewer tier), both closed only by AM-1 and AM-2 (contested).
- **Integration point**: Section 4.
- **Risk (planning label)**: Low

### Change 13: Contested items from B's Round 2 (unanswered by A at standard depth)
- **Source**: B-R2 section 4 (D1 to D7) and section 6 (AM-1 to AM-6)
- **Target**: Base, new section "Contested amendments" (new)
- **Rationale**: Recorded as B's proposals with B's evidence, labelled "not answered by Variant A (standard depth has no Round 3)". AM-1: one Finding per (cluster, category), chained clusters per member (D1). AM-2: side record per Finding `{cluster_id, reviewer_severity_max, blocking_any, disputed, reviewers}`; strike "never lowers a CRITICAL" (D2). AM-3: missing `changed_ranges` degrades to `in_diff` unset with standing `incomplete`, never drop (D4); A had proposed fail-closed. AM-4: standing rule excludes the vacuous "every cluster dropped" for zero clusters, adds `blocking_clusters`, run summary may not say "clean" while the panel is not `present` or `blocking_clusters > 0` (D3, D5). AM-5: append the module to `CORE_PURE_FILES`. AM-6: FX-5 prerequisite is the category set only and `snapshot_file_list` is the PR head tree (D7). D6 (LOW): the converter's invocation path is unspecified: SKILL.md may not take a second python fence (four pins), the converter has no CLI entry, and importing through `superclaude.pr_submit` would edit the package `__init__.py` exports, so the pre-step ref imports by full module path and keeps its own fence; probe INV-018 depends on it. The probe's findings against these amendments are quoted next to them (Change 15).
- **Integration point**: New section after section 5.
- **Risk (planning label)**: Medium

### Change 14: Consistency with C-01, C-02, C-03 (keep, update)
- **Source**: A section 5; B section 2; ADJUDICATION-RESULT files of C-01, C-02, C-03
- **Target**: Base, section 5 (update)
- **Rationale**: Keep A's three paragraphs; update the C-03 paragraph for Change 3 (no quorum helper); keep "requested, not served" until C-08 and R-C03 INV-007; keep A's statement that A does not fire C-01's trigger T-a; add B's dependencies (C-06 over-limit lines: `claim` over 300 characters is rejected, `findings_v2.py:111`; the C-03 quorum refusal does not exist at HEAD outside the ledger).
- **Integration point**: Section 5.
- **Risk (planning label)**: Low

### Change 15: Carry the Round 2.5 findings (from `invariant-probe.md`)
- **Source**: `invariant-probe.md` (20 findings: 6 ADDRESSED, 14 UNADDRESSED; HIGH UNADDRESSED probe INV-002, INV-007, INV-008, INV-011, INV-012; MEDIUM UNADDRESSED probe INV-001, INV-003, INV-006, INV-009, INV-010, INV-014, INV-015, INV-018, INV-019)
- **Target**: Base, new section "Invariants left open by the debate" (new)
- **Rationale**: Quote each finding's assumption and the probe's evidence without resolving it; the debate did not resolve them (standard depth has no Round 3). Prefix every probe id with "probe" in the merged text so it cannot be confused with the prior-slot INV-003 and INV-007 (see the numbering note at the top of this plan). The slot's named invariants (INV-E, INV-F, INV-C, INV-G, INV-I, INV-J, INV-K) keep those names.
- **Integration point**: New section before "Changes not made".
- **Risk (planning label)**: Low

### Change 16: Winner, conditions, convergence and what would change the outcome (from A-R2 section 5, B-R2 section 6, `debate-transcript.md`)
- **Source**: A-R2 section 5 ("What would change my mind"), B-R2 section 6 ("What would change my mind"), convergence assessment
- **Target**: Base, section 1 (replace the one-paragraph position with the resolution statement)
- **Rationale**: State the resolution as the debate produced it: C10-R (A's naming), with B's amendments recorded as contested; both advocates name the same label on all 49 points; content-adjusted 44 of 49; BLOCKED_BY_INVARIANTS; unresolved points and owner items as listed in the Overview. Promotion triggers for the converter's PR keys ("adapter now, extensible v2 later"): M3 nonzero, a second consumer needs the same per-finding key, or M2 shows reviewer-stated `in_diff` is more accurate than the hunk computation (A-R2); `original_line` is dropped outright and `confidence` is unset, so the triggers concern the keys that remain. B's change-my-mind conditions: M4 near zero would simplify AM-1 to a fixture-only guard; a decision that the first release has no summary would shrink D2 and D5 to wording.
- **Integration point**: Section 1.
- **Risk (planning label)**: Low

### Change 17: Form points where the debate named Variant B (S-006, S-009, S-010)
- **Source**: matrix S-006 (B, 58), S-009 (B, 58), S-010 (B, 55); A-R2 section 7 and B-R2 section 8 rows
- **Target**: Base, section 4 and a closing "Limits and open items" section (insert)
- **Rationale**: S-006: A's "preserved by construction" overclaimed (X-001, X-004, X-005) and B's "endangered in a narrow sense" row was more accurate, so the merged invariant table uses B's wording. S-009 and S-010: B's numbered, tagged evidence and its list of open objections and unread files are easier to audit; the merged output keeps a "Limits and open items" section. These are the debate's labels; both advocates give "easier to audit" as the reason.
- **Integration point**: Section 4 and the closing section.
- **Risk (planning label)**: Low

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|------------|-------------------|---------------------------|
| S-003, C-004, C-005 | Third name `panel` in `REVIEWERS`, third key in the `reviewers` object, optional third `merge_wait` pair, edits to five functions and three prose copies | B conceded the slot axis in B-R1 Concession 4; the panel has none of a bot's four GitHub facts; B's own hybrid drops it (B-R1 "Hybrid I would accept"). |
| C-011, C-016 | Four model-emitted keys (`in_diff`, `confidence`, `original_line`, `reviewer`) as optional findings-v2 line keys | B withdrew harness injection (B-R2 1.4) and `original_line` (B-R2 1.3); the converter owns the keys; promotion only on a trigger (A-R2 section 4 row 4, accepted in B-R2 row 4). |
| C-003 | `finding_from_v2` inside `severity_router.py` | B accepted a new module on size and import fan-in (B-R2 1.1). |
| C-006, X-009, A-013 | A `min(2, requested)` quorum floor shared helper (A's own Round 1 idea) and B's "C-03 quorum refusal" derivation | No quorum rule exists in `cli/review` or `pr_submit` (0 matches; `evaluate_quorum` in `cli/reflect/fallback.py` has the wrong shape); both advocates took "any requested reviewer not complete" (the other standing clauses are contested, Change 3). |
| C-010 | `confidence` derived from `disputed` (A) or a model-stated `confidence` key (B) | A conceded (a derived "low" lowers a CRITICAL, `severity_router.py:173-175`); B dropped the key until a threshold is measured. |
| C-007 | Per-round panel inside pr-submit's round cap | Per-round cost unmeasured (GQ-177, OQ-18); once per head SHA is the cheaper default (A-R2 row 11, accepted in B-R2 row 11). |
| C-013, X-007 | `verify-citations` as a differentiator | Both read the same advisory sidecar; it does not separate the designs (X-007). |
| S-005 | Either document spine | The debate labelled it Neither (document form does not bear on correctness). |

## Risk Summary

| Change # | Planning risk | Impact if Failed | Rollback |
|----------|---------------|------------------|----------|
| 1 | Medium | Contested aggregation stated as settled | Keep the "contested" label and B-R2 D1 beside it |
| 3 | High | Rule stated as safe while three HIGH probe findings touch it | Keep the probe findings adjacent; do not drop the strict rule |
| 5 | Medium | A stale panel shown as current | Flag as open (probe INV-001, INV-002) |
| 6 | Medium | Prose guard unpinned (INV-K) | Keep wording as default, flagged owner-decidable |
| 7, 10, 13 | Medium | Contested content presented as settled | Keep the "not answered by Variant A" label on every amendment |
| 15 | Low | Probe items lost | Reinsert from `invariant-probe.md` |
| others | Low | Additive or corrective | Revert the specific paragraph |

## Review Status
- [x] Auto-approved (default; `--interactive` not set)
- [ ] User-approved (--interactive)
- Approved by: auto
- Approval timestamp: 2026-11-14T17:21:11Z
- Plan review: `plan-review.md` (independent analytical agent; 18 defects, all addressed in this revision)
