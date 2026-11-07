# Merge Log

## Metadata
- Pipeline: /sc:adversarial via sc:reflect-protocol Wave 4, depth standard
- Base: variant-1-original.md (reviewer 1, analyzer, sonnet-class), selected in base-selection.md (score 0.813, level-1 tiebreaker over V3 at 0.797)
- Plan executed: refactor-plan.md, Planned Changes 1-17 (auto-approved, non-interactive)
- Other inputs: variant-2-original.md, variant-3-original.md, debate-transcript.md, invariant-probe.md
- Output: merged-verdict.yaml (17 findings M-01..M-17, 3 unaddressed invariants, 4 limits, plan_verdict FAIL-ADVISORY)
- Merge date: 2026-11-07
- Executor mode: read-only; no repository file written; both deliverables returned as text
- Reviewed plan file: not changed (advisory review)

## Changes Applied
| # | Merge item | Applied | Final severity | Provenance tag |
|---|---|---|---|---|
| 1 | M-01 PASS predetermined; pick one fix | yes | HIGH | Planned Changes #1; V1 R1-04; V2 QA-1; V3 R3-F1, R3-F13; INV-003, INV-004 |
| 2 | M-02 old governed child must outlive first process | yes | HIGH | Planned Changes #2; V1 R1-03; V3 R3-F4; V2 QA-3 (medium, reworded); INV-002 |
| 3 | M-03 throwaway HOME lifetime | yes | HIGH | Planned Changes #3; INV-001 |
| 4 | M-04 Task 4 foreground-reparent shape | yes | HIGH (that shape only) | Planned Changes #4; V1 R1-01 (scoped); V2 QA-2; V3 R3-F11 |
| 5 | M-05 Task 7 depth data and dependency | yes | MEDIUM | Planned Changes #5; V1 R1-05; V3 R3-F2 |
| 6 | M-06 third Task 8 state; dead branches | yes | LOW to MEDIUM | Planned Changes #6; V1 R1-06, R1-07; V3 R3-F9, R3-F10 |
| 7 | M-07 run budget; refused runs; skip on refused preflight | yes | MEDIUM | Planned Changes #7; V1 R1-08; V3 R3-F12; INV-010, INV-011 |
| 8 | M-08 session persistence for resume and fork | yes | MEDIUM | Planned Changes #8; V1 R1-02 |
| 9 | M-09 tool list for subagent and Monitor | yes | MEDIUM | Planned Changes #9; V1 R1-09 |
| 10 | M-10 unavailable branches (Task 2 c1, Task 6, Task 7) | yes | MEDIUM | Planned Changes #10; V2 QA-4 (narrowed) |
| 11 | M-11 selector-output record by run id | yes | MEDIUM | Planned Changes #11; V2 QA-5; A-001; INV-008 |
| 12 | M-12 Task 8 case list additions | yes | MEDIUM | Planned Changes #12; V3 R3-F3; V2 QA-6 |
| 13 | M-13 Task 6 pusher, shell label, existing test, same-ref race | yes | MEDIUM | Planned Changes #13; V1 R1-10; V3 R3-F7, R3-F8; INV-007 |
| 14 | M-14 git-status baseline and staging scope | yes (conflict flagged below) | MEDIUM | Planned Changes #14; V1 R1-11; V3 R3-F6 |
| 15 | M-15 session id across resume/fork//clear; reused process | yes | MEDIUM | Planned Changes #15; INV-005, INV-006 |
| 16 | M-16 orphan and supervisor cleanup | yes | MEDIUM | Planned Changes #16; V1 R1-12; INV-009 |
| 17 | M-17 settings checksum per real run | yes | LOW | Planned Changes #17; V3 R3-F5 |

Changes NOT Being Made (refactor-plan.md) were honored: R3-F13 folded into M-01 rather than kept on its own; QA-3 kept at medium inside M-02; R1-01 limited to the reparent shape in M-04; R1-06 lowered to low inside M-06.

## Post-Merge Validation

### Structural integrity
- Top-level keys present in the order requested: merge_method, base_variant, convergence_status, convergence_score (+ convergence_note), calibrated_confidence, plan_verdict, findings, unaddressed_invariants, limits. PASS.
- findings has 17 entries, M-01..M-17, unique ids in plan order. Each carries id, severity, claim, citations, recommendation and provenance (source_findings + Source tag). PASS.
- Severities match refactor-plan.md column "Final severity" exactly, including the two qualified values ("HIGH (foreground-reparent shape only)", "LOW to MEDIUM"). PASS.
- calibrated_confidence values V1 0.79, V2 0.70, V3 0.81 as instructed; self-reports carried from the cards. PASS.

### Internal references
- Every source finding id resolves in an input. All of R1-01..R1-12, QA-1..QA-6 and R3-F1..R3-F13 are used at least once. INV-001..INV-011 are used; INV-012 and INV-013 (ADDRESSED, meta) are deliberately not carried. A-001 resolves in debate-transcript.md. PASS.
- Plan row 6 lists R1-06 twice (cosmetic duplicate in refactor-plan.md); counted once in M-06.
- Citations re-read and confirmed on 2026-11-07: helper:7-9, :16-17, :83, :102-106, :149, :219-223, :220-225, :234, :251-265, :253, :292, :333-337, :343-344, :427-428, :429-437; live_probe.py:108-123, :134, :142-143, :160, :235-236, :237-240, :252, :271, :275, :279, :280-286; plan:22, :25, :31, :35, :36, :44, :47, :48, :55, :58-60, :66, :69, :79, :82, :84, :88, :90, :93-94, :99, :101, :104, :114, :118, :119, :120; test:473-488, :1291-1354, :1306-1331, :1347-1348, :1472-1474; design:501, :504, :506, :551, :555, :559.
- Tagged [INFERRED] (not read by the executor): review-2.md:9, :10, :12; actor-context-probe.sh:37-39; coverage-matrix.yaml:23; the blocked package's existing modification (session snapshot); the Claude Code behaviors behind INV-005, INV-006 and INV-008.
- Citations dropped: none. Plan row 3's "helper:220-225" and plan row 8's "live_probe.py:235-236" confirmed as stated. One citation was narrowed: helper:16-17 is the header comment and design:555 states the same contract.

### Contradiction re-scan (new contradictions introduced by the merge)
1. M-01 option (a) vs option (b). The two fixes exclude each other in effect, and the debate left both open. The V3 advocate rated C-001 "medium if the plan states FAIL is expected", so choosing (b) would lower M-01 below the HIGH the verdict records. Resolution in the verdict: HIGH applies to the plan as written, and M-01 requires exactly one option. Under (a), PASS stays meaningful only if the accepted-documented-limit class never counts toward PASS; otherwise INV-003 comes back.
2. M-06 vs M-01 and plan:119. M-06's new "superseded or not applicable (cite)" state is not one of the classes plan:119 permits for PASS ("every required case is observed"). Unless M-01's fix lists it as a class that neither blocks nor supports PASS, it becomes a new FAIL trigger. Not resolved inside the verdict (the plan gives no rule); escalated to the orchestrator.
3. M-02 vs M-04. Both rest on the supervisor waiting for descendants (helper:16-17). The only shapes documented to escape that wait (setsid, supervisor kill; helper:7-9) select ordinary or unknown, not governed. So M-02's "say how the child outlives the first process" may have no answer that keeps the child governed, and the decisive case may resolve only to unavailable. This is a tension, not a contradiction in the verdict text; recorded for the orchestrator.
4. M-14 vs the repository's standing rule. M-14's "limit staging to this package's folder" (from R3-F6) conflicts with the project rule that `.dev/tasks/` is always staged (`git add .dev/tasks`). Applied as planned and escalated. R3-F6's own alternative ("state that existing blocked-package changes are left as they are") avoids the conflict.
5. M-08 vs plan:22. M-08 requires the runs to differ from live_probe, while plan:22 says "exactly like" it. This contradicts the reviewed plan, not the verdict; it is stated in M-08's citations so the plan author sees it.
6. Severity overrides, recorded rather than contradictory: M-16 is MEDIUM per INV-009, while the debate matrix scored C-015 low. M-13 is MEDIUM although R1-10 and R3-F8 were low. M-14 is MEDIUM although R1-11 was low. In each case refactor-plan.md governs.
7. M-10 vs M-13. If M-13 names a prepare/run job as the governed pusher, Task 6 makes no Claude run, and M-10's refusal-based unavailable branch for Task 6 would never fire. Minor; no change.

## Summary
- Planned: 17
- Applied: 17
- Failed: 0
- Skipped: 0
- Escalations to orchestrator: 2 (re-scan item 2, M-06 state vs the PASS rule; item 4, M-14 staging vs the `.dev/tasks` always-staged rule). One tension recorded (item 3, M-02 vs M-04).
