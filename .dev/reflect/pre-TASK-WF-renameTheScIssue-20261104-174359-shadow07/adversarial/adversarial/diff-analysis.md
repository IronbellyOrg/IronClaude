# Diff Analysis: Reviewer-Card Comparison (Mode A, UC-1 pre-execution plan audit)

## Metadata

- Generated: 2026-11-13T00:30:00Z
- Variants compared: 3 (round1-card1.md = reviewer-1 analyzer, calibrated 0.80; round1-card2.md = reviewer-2 qa, calibrated 0.82; round1-card3.md = reviewer-3 refactorer, calibrated 0.72)
- Audited plan: `.dev/tasks/done/TASK-WF-renameTheScIssue-20261104-174359/TASK-WF-renameTheScIssue-20261104-174359.md`
- Driving spec: `.dev/tasks/done/TASK-WF-renameTheScIssue-20261104-174359/source.md`
- Debate focus: correctness, coverage, deviation-classification
- Total differences found: 13
- Categories: structural (2), content (6), contradictions (3), unique (5), shared assumptions (1)

## Structural Differences

| # | Area | Card 1 (analyzer) | Card 2 (qa) | Card 3 (refactorer) | Severity |
|---|------|-------------------|-------------|---------------------|----------|
| S-001 | Findings count / shape | 2 findings (F1, F2), per-hypothesis verdicts H1-H6 | 4 findings (F1-F4), organized by audit dimension (coverage matrix / ACs / test-spec-vs-disk) | 2 findings (F1, F2), topic-numbered analysis 1-4 | Low |
| S-002 | Hypothesis disposition style | Explicit H1-H6 verdicts incl. named non-findings | Hypotheses folded into analysis; explicit "No finding." verdicts inline | Explicit agreement/non-finding statements per brief item | Low |

All three cards share the panel skeleton (persona header, analysis body, findings-v2 block, self-report line). No incompatible organizational models.

## Content Differences

Content points are the substantive topics the eight findings cluster into. Topic F exists because reviewer-3's F2 is outside the caller's five-topic map; it is retained for merge fidelity.

| # | Topic | Card 1 (analyzer) | Card 2 (qa) | Card 3 (refactorer) | Severity |
|---|-------|--------------------|-------------|---------------------|----------|
| C-001 | A: missing sync-dev/verify-sync step + stale old template in local `.claude/` mirror | F1: no task runs sync-dev/verify-sync; sync-dev never deletes, so stale `templates/summary.md` lingers and a local verify-sync reports it "present only in .claude/"; CI unaffected (CI runs sync-dev first) | not addressed | F1: same gap; CI regenerates mirror so no CI break; local mirror stays stale; "anything reading `.claude/` during development would see the old names"; no task AC detects it | Medium |
| C-002 | B: T1.AC3 grep substring ambiguity (`summary\.md` matches inside `issue-summary.md`) | F2: AC works only if read as "every matched line is an issue-summary.md occurrence"; a line holding both names would pass; the real guard is `test_old_summary_path_is_gone` | F1: as literally written self-contradictory; no stated pass condition; needs unstated `grep -v issue-summary` or `(^|[^-])summary\.md`; same phrasing in T2 (plan:56) and T4 (plan:94) | not addressed | Medium |
| C-003 | C: T3 red-check weaker than it reads (ad-hoc `uv run python`, no expected exit code, duplicates pinned test) | H3 resolved non-finding: name-pattern checks make the 10 pre-fix copies adequate | F2: ad-hoc import with "exit code recorded" and no expected value = pass not defined; pinned `test_checks_flag_pre_fix_text` (tests:493-501) proves the same deterministically, so the ad-hoc step adds little | not addressed | Medium |
| C-004 | D: T1.AC2 "otherwise unchanged" names no verifier | not addressed | F3: no verifier named; a diff against `artifacts/pre/template-summary.md` would work but is not commanded | not addressed | Low |
| C-005 | E: coverage gaps (no separate INF row for the guide-row no-edit; design-doc old-path check is a one-off grep, not a regression test) | not addressed (H6 resolved non-finding: guides carry no reference) | F4: old-path requirement pinned deterministically only for worker texts and templates; design doc checked by one-off grep; matrix has no separate row for the guide-row no-edit resolution | rebutted in substance: guide no-edit is "a reasoned, evidenced non-edit rather than an omission. Nothing is missing" | Medium |
| C-006 | F: plan relies on the existing exactly-once/under-heading test as the paragraph drift guard but never says so | not addressed | not addressed | F2: sync of the three agent paragraphs and the test literal is kept only by a verbatim-copy instruction and a manual "exactly once" AC; `tool_input_rule_problems` (tests:281-284) is the real guard and the plan never states it relies on it | Low |

## Contradictions

| # | Point of Conflict | Position A | Position B | Impact |
|---|-------------------|------------|------------|--------|
| X-001 | Is the guide-row/design-doc coverage a finding? (topic E) | Card 2 F4: traceability gap — no separate INF row; design-doc check not deterministic | Card 3 (analysis §2): "Nothing is missing and nothing extra is edited" — reasoned, evidenced non-edit | Medium — resolvable: both positions are true at different altitudes (documentation/traceability vs substance) |
| X-002 | Is the T3 red-check adequate? (topic C) | Card 1 (H3): non-finding — name-based checks make pre-fix copies sufficient | Card 2 F2: finding — pass condition undefined; duplicates the pinned negative test | Low — resolvable: under-specification (card 2) and copy sufficiency (card 1) are compatible |
| X-003 | The T1 brief's H1 consequence ("verify-sync fails for every later contributor") | Card 1: "the T1 card's stated consequence is wrong"; CI runs sync-dev then verify-sync | Card 3: same correction, independently ("stale local mirrors cannot fail CI") | None — both variants converge against the brief's premise; no card-vs-card conflict |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | Card 1 | Names the exact verify-sync detection mechanism for the stale mirror: local verify-sync reports the old file "as present only in `.claude/`" (diff -rq "Only in" semantics) | Medium |
| U-002 | Card 2 | The phrasing-reuse detail: the ambiguous "prints only issue-summary.md occurrences" is reused in the T2 AC (plan:56) and T4 AC (plan:94), tripling the ambiguity surface | Medium |
| U-003 | Card 2 | Topic D: T1.AC2 "otherwise unchanged" has no named verifier despite a pre-fix copy being available for a diff | Low |
| U-004 | Card 3 | Reader-impact angle on the stale mirror: "anything reading `.claude/` during development would see the old names"; and "no task AC would catch this" (both task test runs read `src/`) | Medium |
| U-005 | Card 3 | Topic F: the plan's unstated reliance on `tool_input_rule_problems` (tests:281-284) as the paragraph drift guard | Low |

## Shared Assumptions

| # | Agreement Source | Assumption | Classification | Promoted |
|---|------------------|------------|----------------|----------|
| A-001 | All three cards cite the post-execution on-disk state (executed tests, current Makefile/CI) as evidence when auditing the plan-as-written (C-001..C-006 all do this) | The on-disk post-execution repository state is admissible evidence for a UC-1 pre-execution plan audit: "the plan does not say/command X" remains a valid plan-gap finding even when the executed repo already does X | UNSTATED | Yes — [SHARED-ASSUMPTION] diff point; advocates must ACCEPT/REJECT/QUALIFY |

STATED assumptions (not promoted): all three cards treat every finding as MINOR/non-blocking (explicit `blocking: false`).

## Summary

- Total structural differences: 2 (both Low)
- Total content differences: 6 (4 Medium, 2 Low)
- Total contradictions: 3 (X-001 Medium, X-002 Low, X-003 none — convergence point)
- Total unique contributions: 5 (3 Medium, 2 Low)
- Total shared assumptions surfaced: 1 (UNSTATED: 1, STATED: 1, CONTRADICTED: 0)
- Highest-severity items: C-001, C-002, C-003, C-005, X-001 (Medium)
- Similarity check: differences are substantive (8 findings across 5 converged/divergent topics + 1 unclustered); the <10% similarity skip does not apply.
- Convergence denominator: count(C-NNN) + count(A-NNN) = 6 + 1 = 7 diff points.

Orchestrator probe note (pre-debate, evidence-verified): Card 2's in-body and findings-block citations for the Task 1 ACs read plan:50/51/52; the quoted texts sit at plan:43/44/45 (grep-verified this run). The claims themselves verify. This is carried into the debate as a citation-accuracy fact, not a new finding.
