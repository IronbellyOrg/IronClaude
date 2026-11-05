# Merge Log

## Metadata
- Executor: merge-executor (adversarial pipeline Step 5)
- Merge date: 2026-11-04T14:19:26Z
- Base: variant-1-original.md (reviewer 1, sonnet:analyzer)
- Incorporated: variant-2-original.md (haiku/glm-5.3:qa), variant-3-original.md (opus:refactorer), round2-variant-3.md (new evidence 1-3), invariant-probe.md
- Plan: refactor-plan.md (9 planned changes, 4 rejected under "Changes NOT Being Made")
- Output: merged-verdict.yaml
- Convergence: 0.92, BLOCKED_BY_INVARIANTS (INV-004, INV-027), carried from debate-transcript.md
- Subject plan (not edited, A-002): .dev/tasks/to-do/TASK-WF-implementIronbel-20261104-130647/TASK-WF-implementIronbel-20261104-130647.md

## Applied Changes

| # | Change | Status | Target | What changed | Provenance tag |
|---|--------|--------|--------|--------------|----------------|
| 1 | Regrade R1-F5 to blocking, merge R3-F5 | applied | R1-F5 | Severity minor -> blocking. Title is now the quoted-substitution Done-when violation. Fix is now a nested `$(`/backtick context in M-SCANNER with blocked tests; document-and-pin withdrawn. The bash -c/eval/xargs/find -exec half stays a minor ceiling and moves to M-CEILINGS. | Base (original, modified) — regraded minor -> blocking and merged with V3 R3-F5 per Change #1 |
| 2 | Single-scanner amendment (blocking) | applied | new M-SCANNER (+ M-HEREDOC-TEXT) | Inserted M-SCANNER: one stateful awk scanner on stdin with rules (a)-(f) for R3-F2 and R3-F3 desync halves, Round 2 evidence 1-3, and INV-002, 004-010, 013. It lists the E-case tests and the condition for INV-027 to clear. The R3-F2 text half became a separate minor finding, M-HEREDOC-TEXT (corrected header doc and one pinning test), as "Changes NOT Being Made" requires. | Variant 3, findings R3-F2 and R3-F3 (desync halves) with Round 2 evidence 1-3 and INV-002/004-010/013 — merged per Change #2 |
| 3 | Replace C-001 fix with the allowlist | applied | R1-F1 fix | The freshness-/counter narrowing became the allowlist: Bash-matcher PreToolUse commands == {block-bare-python.sh}, for INV-001's reason. The tests/hooks/ run in Task 4 and the PR-body supersession note are kept. INV-001 evidence was added. | Base (original, modified) — fix replaced by the INV-001 allowlist per Change #3 |
| 4 | Fail-open by construction + jq-missing test | applied | R1-F6 | Merged R3-F7 (exit 2 only on a positive result), R2-F3 (PATH-shim jq-missing test), INV-021 (jq-branch-only stderr marker) and INV-017 (install warning or stated precondition). Severity stays minor. | Base (original, modified) — merged ... per Change #4 |
| 5 | Large-command case | applied | R1-F11 | Kept the plan's under-1-second precedent and dropped the "flaky" framing and the < 2.5 s bound. Added a ~200 KB stdin case ending in `; python3 x` that must exit 2, timed against the full scanner. | Base (original, modified) — ... ~200 KB stdin case added per Change #5 |
| 6 | Task 7 hardening | applied | new M-TASK7 | Inserted R3-F9 together with INV-016: --allowedTools Bash,Agent, --append-system-prompt, no --bare, a refusal recorded as blocked, side effects recorded, artifacts reviewed before staging. | Variant 3, finding R3-F9 — merged with INV-016 per Change #6 |
| 7 | Constraints mislabel, array and ceiling notes | applied | new M-CONSTRAINTS, M-ARRAY, M-CEILINGS, M-AWK-LOCALE; documented_ceilings | Inserted R3-F11 (M-CONSTRAINTS); R3-F10 + INV-015 (M-ARRAY); R3-F6 + R1-F5 ceiling half + R2-F6 + INV-011/012/014/022 (M-CEILINGS, including the L40 vs L58 contradiction); and INV-026 (M-AWK-LOCALE). Built the documented_ceilings list (11 entries). R1-F4's wrapper half now points to M-CEILINGS. | Variant 3, finding R3-F11 / R3-F10 / R3-F6 — merged per Change #7; Invariant probe, finding INV-026 — merged per Change #7 |
| 8 | Coverage-matrix note | applied | new M-COVERAGE (minor) | Inserted R2-F5 with the coverage-matrix.yaml line refs verified in Round 2. | Variant 2, finding R2-F5 — merged per Change #8 |
| 9 | Extend Goal-wording finding | applied | R1-F8 | Added INV-019 and merged R2-F4. Template line 965 is recorded as an out-of-scope follow-up. The rewording lands in progress.md and the PR body, not the plan. | Base (original, modified) — extended with INV-019 ... per Change #9 |

## "Changes NOT Being Made" — honoured

| Rejected item | How it was honoured |
|---------------|---------------------|
| V2's positive pin argued for coverage reasons | Not adopted on V2's rationale. The allowlist in R1-F1 cites INV-001 only, and V2 R2-F1 is listed as a source. |
| R3-F4 blocking grade for continuation | R1-F4 stays **minor**. Its fix moved inside the scanner, per state (INV-005), with one allowed and one blocked continuation test. |
| R3-F2 text-half blocking grade | M-HEREDOC-TEXT is **minor**. The fix corrects the header comment and adds one pinning test. |
| R1-F11 / R3-F8 "flaky" framing | Dropped. R1-F11 keeps the under-1-second bound (test_freshness_subagent_start_policy.py:86 precedent). |

## Base edits outside the 9 changes (structural only, no new content)
- R1-F3, R1-F7 and R1-F9 had no `fix` field in the base. A fix was written from each finding's own title text (keep and explain / order Tasks 1 -> 5 -> 6 / record as scope addition). Because the plan is not edited (A-002), each fix is routed to progress.md. Each is tagged "Base (original, modified)".
- Every base finding got an `evidence` list copied from the round-1/round-2 statements and debate rows. No line number was invented: each one is quoted from a source artifact, which is cited.

## Escalation notes (not applied; outside the plan)
- The R3-F8 test-runner jq guard (skip or fail clearly when jq is missing in the test environment) appears in the debate (round1-variant-3.md:34, round2-variant-2.md:32) but not in the plan's 9 changes. It was not added.
- An awk-missing test case was proposed in round2-variant-1.md:29 and round2-variant-2.md:20 but is not in the plan. It was not added. R1-F6's "every other path exits 0" covers the behaviour, not the test.

## Post-Merge Validation

| Check | Result |
|-------|--------|
| YAML parses; top-level keys exactly provenance, merge_method, convergence_score, convergence_status, blocking_invariants, findings, implement_time_amendments, documented_ceilings | PASS (parsed with PyYAML) |
| Every finding has id, severity, task, title, evidence, fix, sources, source_tag | PASS (19/19) |
| Every source finding is represented (R1-F1..F11, R2-F1..F6, R3-F1..F11) | PASS |
| Every invariant is represented or ADDRESSED | PASS. 24 of 27 cited. INV-018, INV-023 and INV-024 are ADDRESSED in invariant-probe.md and need no action. INV-020 (ADDRESSED) is cited as evidence for R1-F10. |
| Severity vs debate final positions | PASS. R1-F5 is blocking (C-006/X-002 95%). M-SCANNER is blocking (C-003 90%, C-004 85%, C-006 95%). Continuation (R1-F4) is minor (X-001 95%). The heredoc text half (M-HEREDOC-TEXT) is minor (X-003 split). R1-F1 and R1-F2 stay blocking (C-001, C-002). |
| No new contradictions vs sources | PASS. The R1-F1 fix no longer uses the freshness- filter, which INV-001 showed was ineffective. R1-F4 no longer says "join before splitting", which INV-005 contradicts. R1-F11 no longer bounds at 2.5 s, which conflicted with the rejected flaky framing. M-HEREDOC-TEXT's header text matches M-SCANNER rule (e). The bash -c ceiling resolves the L40/L58 contradiction instead of adding one. |
| Internal references resolve | PASS. M-SCANNER, M-CEILINGS, M-AWK-LOCALE, M-TASK7 and AMD-01..08 are all defined. |
| Every blocking item and every MEDIUM invariant has an amendment | PASS. Blocking: R1-F1 (AMD-01), R1-F2 (AMD-02), M-SCANNER (AMD-03, AMD-05), R1-F5 (AMD-04). HIGH: INV-004 (AMD-03), INV-027 (AMD-05). MEDIUM: INV-001 (AMD-01); INV-002, 005, 006, 007, 008, 010 (AMD-03); INV-003 (AMD-06); INV-017 (AMD-07); INV-016 (AMD-08). |
| Plan file untouched; amendments recorded in progress.md | PASS (A-002; every amendment has `record: progress.md`) |

## Summary
- Findings: 19 (blocking 4, minor 15)
  - Base kept unchanged: 2 (R1-F2, R1-F10)
  - Base modified: 9 (R1-F1, R1-F3, R1-F4, R1-F5, R1-F6, R1-F7, R1-F8, R1-F9, R1-F11)
  - New: 8 (M-SCANNER, M-HEREDOC-TEXT, M-TASK7, M-CONSTRAINTS, M-ARRAY, M-CEILINGS, M-AWK-LOCALE, M-COVERAGE)
- Implement-time amendments: 8 (5 blocking, 3 medium)
- Documented ceilings: 11
- Planned changes: 9 applied, 0 skipped. Rejected items honoured: 4.
- Convergence: 0.92, BLOCKED_BY_INVARIANTS. It clears only when AMD-03 (INV-004) and AMD-05 (INV-027) are satisfied at implement time.
