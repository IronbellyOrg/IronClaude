# Task-Integrity Validation (consolidated) — orchestrator direct pass

**Date:** 2026-07-02
**Method:** Direct orchestrator validation against the mandatory task-file checklist (A.10 structural +
A.10.25 research-alignment + A.10.5 operational). Chosen because parallel subagent spawns hit repeated
infra operation-timeouts this session; a direct Read-and-check pass is more reliable than timeout-prone
subagents for a structural/alignment audit and was performed adversarially against the checklist.

## Items Reviewed

| Check | Verdict | Evidence |
|---|---|---|
| Frontmatter gate keys (start_commit / executor_model_class / task_type / reflect_post room-comment / template_schema_doc) | PASS | frontmatter L2-27 |
| 26 B2 self-contained items (context+action+output+verification+gate) | PASS | all `- [ ]` items carry the 5 elements |
| Execution Context (References / Source-areas dir-names-only / Key-constraints); TB-Add-7/8 | PASS | L103-136; per-item Context carries monitor.py:LINE or evidence-absence comments |
| Granularity A3 (one item per fixture/hunk/test group) | PASS | 3 fixture items, 2 hunk items, contract-table + 4 parity + F5 items |
| Anti-orphaning (Done is sole item after reflect wrapper) | PASS | Step 4.9 wrapper → Step 4.10 Done (L263→L267) |
| HUNK 1 exact: `if is_error and (api_error_status == 429 or "rate_limit_error" in body):` inline, aes-first | PASS | Step 2.2 (L205) |
| HUNK 2 exact: drop `via provider`, keep `(?P<model>.+?)`; `_RE_SINGLE_ACCOUNT` unchanged | PASS | Step 2.1 (L201) |
| Load-bearing fixture VERBATIM from research/shape2-verbatim-transcript.jsonl; anti-fabrication explicit | PASS | Step 1.3 (L165) |
| 12-row contract table asserting (kind, resolved_model incl. None) per OQ4 | PASS | Step 1.x + research/04 table |
| Parity 7a/7b/7c(negative `is not`)/7d | PASS | Step 1 offline-parity item (L185) |
| F5 two directional assertions (no impossible dual-signal fixture) | PASS | F5 item (L189) |
| RED→GREEN discipline (rows 4/5/6 + 7b RED pre-fix) | PASS | Phase 1 RED-confirm + Phase 3 GREEN |
| Regression (6 legacy fixtures + test_recovery_policy + full sprint suite) + ruff check + ruff format + verify-sync | PASS | Phase 3 items |
| Scope-discipline "CHANGES WE ARE NOT MAKING" encoded | PASS | L197, L126 |
| QA gate = 6 agents (3 rf-qa + 3 rf-qa-qualitative), serialized fix (I19/I20) | PASS | Steps 4.1-4.x (L235, L239) |
| POST reflect flat wrapper (`--depth deep --fix --promote`, recursion guard, exit-code consumed, no --base/--reflect/--max-turns/subagent) + `.claude/` staging guard | PASS | Step 4.9 (L263) |

**VERDICT: PASS** (0 CRITICAL, 0 IMPORTANT, 0 MINOR). No in-place fixes required.

## Note on A.10.7 PRE reflect gate
A `--spec` resolves (merged-requirements.md), so the protocol mandates a reflect run. It was NOT run
in-session due to observed infra operation-timeouts (two consecutive subagent timeouts this session) —
recorded honestly as deferred, NOT fabricated as pass and NOT substituted by this direct validation
(the protocol forbids substituting another coverage check for a reflect run). The task file's embedded
POST reflect wrapper (Step 4.9) remains the executor-disjoint anti-bias gate that runs at execution.
Operator action: run the PRE gate independently in a fresh session (command in the results banner).
