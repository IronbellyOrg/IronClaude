# Diff Analysis: reviewer-card comparison (stage 4 plan, third review)

## Metadata

- Generated: 2026-11-16 (orchestrator, inline analytical pass)
- Variants compared: 3 (V1 = reviewer-1, analyzer, sonnet; V2 = reviewer-2, qa, haiku; V3 = reviewer-3, refactorer, opus)
- Total differences found: 22
- Categories: structural (2), content (11), contradictions (3), unique (4), shared assumptions (4 surfaced, 2 UNSTATED promoted)
- Finding ids are quoted as `V<n>-F<m>` (variant n, finding m). P4 = the stage 4 plan, S1 and S3 = the stage 1 and 3 plans, SPEC = the merged spec.
- Severity vocabulary used below and by the advocates: blocking (a requirement or check that cannot be met, a wrong or missing result, or data loss), Medium (a real but non-blocking weakness), minor (wording or format).

## Structural Differences

| # | Area | V1 | V2 | V3 | Severity |
|---|------|----|----|----|----------|
| S-001 | Verdict | PASS (0 blocking, 6 minor) | NEEDS-REVISION (3 blocking, 1 minor) | NEEDS-REVISION (1 blocking, 6 minor) | High |
| S-002 | Card shape | Verdict, 6 findings, 10 Checked bullets | Verdict, 4 findings, 5 Checked bullets, absolute paths, one packed citation | Verdict, 7 findings, 8 Checked bullets | Low |

## Content Differences

| # | Topic | V1 | V2 | V3 | Severity |
|---|-------|----|----|----|----------|
| C-001 | Cap-sentence count after the edit (P4:45, P4:64 "prints 1 in each") | V1-F1 minor: prints 2 if the old cap bullet is kept (natural), 1 if folded but then it also printed 1 before; says PRIOR H9 is not really fixed | Checked bullet: "not proved unpassable"; the existing sentence can become the digest's closing sentence | V3-F1 blocking: the old cap bullet S3 stays, so the count is 2 in all 8 carriers and both checks fail | High |
| C-002 | Constraints doubt wording "close enough or probably fine" against the Task 2 grep that prints 0 (P4:25, P4:65) | V1-F2 minor | not raised | V3-F2 minor | Low |
| C-003 | Doubt-line positive greps are satisfied by the digest alone, so they cannot show the rewrite (P4:51, P4:65) | not raised | V2-F3 blocking (three prompts' principle 8) | V3-F3 minor | Medium |
| C-004 | Rule 6 bold heading: Task 1 needs it changed by stage 3; stage 3 never requires it (P4:49, S3:183) | not raised (marks H7 fixed) | not raised | V3-F4 minor | Medium |
| C-005 | Stale premise "Stage 1 ... did not name the switch" (P4:114 against S1:234 `STRICT_T2`) | V1-F3 minor | not raised | V3-F5 minor | Low |
| C-006 | Plugin mirror and parity test dropped by the revision (P4:23 against SPEC:948) | not raised (checked, decided by brief) | V2-F1 blocking: Drift without authorization | not raised | High |
| C-007 | Roadmap and tech-research cap-line pointers not edited (P4:26 against SPEC:867) | not raised (H2 marked recorded) | V2-F2 blocking: obligation undelivered | not raised | Medium |
| C-008 | Sibling doubt or label lines that stay beside the digest | V1-F5 minor: `automated_qa_workflow_qa_prompt.md:125`, `doc_code_analyst_qa_prompt.md:206`, `skill_template.md:815, 824, 834`, `agent_template_qa.md:268` | not raised | V3-F7 minor: `skill_template.md:824, 834` only | Medium |
| C-009 | "CRITICAL is blocking" kept in the spec-panel Grading bullet (P4:90 against SPEC:739) | V1-F4 minor (PRIOR H8 unchanged) | not raised | not raised | Low |
| C-010 | Wording gaps: allow-list survivors list, "names the rule once", plugin FR-8 reason, "L1 merge text in all four templates" | V1-F6 minor (three items) | not raised | V3-F6 minor (merge line only in `agent_template_qa.md`) | Low |
| C-011 | Completeness of the coverage matrix itself | not raised | V2-F4 minor: 26 rows omit the entry gate, spec-panel re-pin, final pinning run, the new dimensional-mismatch test | not raised | Low |

## Contradictions

| # | Point of Conflict | V1 Position | V2 Position | V3 Position | Impact |
|---|-------------------|-------------|-------------|-------------|--------|
| X-001 | Can the cap-count check be met? | minor; meets only if the bullet is folded, and then proves nothing | can be met (fold the bullet into the digest) | cannot be met without deleting S3 "without authority" | High |
| X-002 | Is dropping the plugin mirror a defect? | not a defect (checks the plugin decision holds) | blocking Drift (author's reassessment is not authorization) | not a defect | High |
| X-003 | Are the digest-satisfied greps a blocking gap? | not raised | blocking | minor | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | V1 | Sibling "No benefit of doubt: If you cannot verify ... it FAILS" lines in two rule prompts (`:125`, `:206`) | Medium |
| U-002 | V3 | Rule 6 heading may stay unchanged after stage 3, making Task 1's two label checks contradict each other | Medium |
| U-003 | V2 | Matrix completeness gap and the two spec-obligation dropouts (plugin mirror, section 10.5 pointers) | Medium |
| U-004 | V1 | Per-earlier-finding status H1 to H13 with live recounts (H7 awk, H6 `FINAL: pass`, H4 `_artifacts_clause`) | Medium |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|-----------|------------------|--------|--------|
| A-001 | The digest inserted by stage 1/3 text ends with the cap sentence verbatim and its flattened body is what T1 compares (so the cap sentence is in the digest) | all three treat the cap sentence as part of the digest | Decides C-001 | STATED (SPEC:207; S1 Task 2) |
| A-002 | Stage 1 and stage 3 will run as written and create the files P4 reads (registry, scale-map allow-list, `Kept mechanical gates`, the dispatching `test_review_severity_rule.py`) | all three read cross-stage facts from plans only | Any stage deviation breaks P4 checks | UNSTATED, promoted |
| A-003 | An executor follows each acceptance grep literally and halts on a non-matching count (rather than reinterpreting) | all three grade by "what the grep prints" | Decides how severe a wrong count is | UNSTATED, promoted |
| A-004 | The spec's stage 4 cell is superseded by the brief and the owner answers of 2026-11-16 where they differ | V1 and V3 assume it; V2 does not | Decides C-006 | STATED (brief decision 4; OPEN-QUESTIONS 2.3, 3.4) |

### Promoted [SHARED-ASSUMPTION] diff points

| # | Assumption | Impact | Status |
|---|-----------|--------|--------|
| A-002 | Earlier stages deliver exactly what P4 reads | Medium | open for debate |
| A-003 | Executors treat a wrong acceptance count as a failed task | High | open for debate |

## Summary

- Total structural differences: 2
- Total content differences: 11
- Total contradictions: 3
- Total unique contributions: 4
- Total shared assumptions surfaced: 4 (UNSTATED: 2, STATED: 2, CONTRADICTED: 0)
- Highest-severity items: S-001, C-001, C-006, X-001, X-002
