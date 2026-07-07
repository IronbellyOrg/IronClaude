# QA Report — Task Qualitative (Content Verification, Step 4.G7)

**Task:** TASK-RF-t2-fallback-ladder-20260706-050832
**Date:** 2026-07-07
**Phase:** task-qualitative (Step 4.G7 content verification of Phase-4 fix cycle)
**Fix cycle:** verify-only (RETRY after prior content-verifier timeout)
**Fix authorization:** false (report only)

---

## Overall Verdict: PASS

The five Phase-4 fixes are operationally meaningful (not shallow / tautological),
and the two ACCEPTED (no-code-change) findings are justified against actual
`run_fallback_ladder` control flow. All 29 `test_openai_compat.py` tests green.

## Items Reviewed
| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | P4-COMP-F1 asserts real per-slot binding, fails if `model_prefix` ignored | none | PASS | `test_resolve_factory_t1_branch_binds_per_slot_models` (test:500-519) asserts `factory(0).model=="m-a"`, `factory(1).model=="m-b"`. `_factory` binds `pool[slot_index % len(pool)]` (commands.py:723); `.model` is a real per-instance attr (openai_compat.py:284, 726-730). `model_prefix` is honored via `model_prefix if model_prefix is not None else T2_MODEL_ENV_PREFIX` (commands.py:700-702). If ignored → defaults to `T2Model0N`/`T2ProxyUrl`, absent from the T1-only env dict → `TransportEnvError` at build → test fails. Genuine binding + genuine negative behavior. |
| 2 | P4-ACT-M1 asserts specific missing name AND present name NOT in `.missing` | none | PASS | `test_read_env_for_pool_partial_absence_t1_missing_key` (test:465-484): env = `{T1ProxyUrl, T1Model01}`, `T1ProxyKey` absent. Asserts `"T1ProxyKey" in exc.value.missing` (483) AND `"T1ProxyUrl" not in exc.value.missing` (484). Both halves present — proves specific-gap reporting, not all-or-nothing. |
| 3 | P4-ACT-M2 exercises dense-skip / slot-count, not a 2-model happy path | none | PASS | `test_read_env_wrapper_delegates_with_dense_skip_and_slot_count` (test:433-462): env has empty interior `T2Model03=""` (dense-skip) + later `T2Model04="m-d"`. Asserts `via_wrapper == via_pool` AND `models == ("m-alpha","m-beta","m-d")` AND `len==3` (461-462). Load-bearing on slot enumeration + empty-skip + tuple length. Existing 2-model `test_read_env_wrapper_delegates_to_pool_reader` (414-430) preserved intact — M2 is additive. |
| 4 | P4-COMP-F2/F3 acceptance justified — T2-worded msg never operator-surfaced on fallback path | none | PASS | `run_fallback_ladder` resolves the slot transport eagerly in `_dispatch_one_fallback` (fallback.py:372, "eager (may raise)"). Caller catches `(TransportEnvError, ModelPoolTooSmallError)` at fallback.py:471 **with no `as e` binding** — the message string is discarded. Terminal state folds into `terminal_reason="fallback_config_missing"` (473) + `config_missing_slots.append` (472); ledger entry carries `failure_class:"fallback_config_missing"`, `status:"proxy_error"`, `model_id:None` (533-546). The structured `.missing` tuple carries real T1 names (verified by check #2), and `ModelPoolTooSmallError` carries accurate `pool_size`/`workers_requested` (commands.py:719, fallback.py:269). Load-bearing signal = structured fields; the T2-worded string is never surfaced on this path. Acceptance sound. |
| 5 | No new test is tautological / falsely implies behavior | none | PASS | None assert "no exception" only; none write a placeholder and assert against it (no AX-4 trivially-passing pattern). F1-bind asserts distinct models per slot; F1-pool-too-small drives a real `ModelPoolTooSmallError` guard (single-model pool + `workers_requested=2`, test:522-538); M1 asserts a present/absent partition; M2 asserts a 3-tuple + dense-skip. All exercise real behavior with input that would expose the inverse bug. |

## Summary
- Checks passed: 5 / 5
- Checks failed: 0
- Critical issues: 0
- Confidence: Verified 5/5 | Unverifiable 0 | Unchecked 0 | Confidence 100%
- Tool engagement: Read 4 | Grep 2 | Glob 0 | Bash 2 (incl. `uv run pytest tests/swarm/test_openai_compat.py -q` → 29 passed)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| — | — | — | None. | — |

## Observations (non-blocking, no action required)
- F2/F3 acceptance is scoped to "the fallback path," which is verified as the
  only current T1-prefix caller (the reflect fallback resolver folds the
  exception). A *future* caller that passes T1 names to
  `_resolve_run_transport_factory` and lets the exception propagate to a user
  would surface the T2-worded message. Not a current defect — noted for the
  eventual message-parameterization follow-up the verdict already defers.

## Self-Audit
This is a Step 4.G7 content-verification run (no `## Inherited Structural
Verdict` block in the spawn prompt), so standalone behavior applies.

**(a) Reliance list — items taken as given from the fix verdict:**
- Relied on phase4-fix-verdict.md's claim of green full-swarm suite (2259) and
  empty `models.py`/`contract.py` diffs — NOT independently re-run here (scoped
  to the content of the 5 fixes + acceptances per spawn instruction).

**(b) Independent semantic checks (tool-verified, not reliance):**
- Per-slot binding reality: Read commands.py:699-734 + openai_compat.py:284 —
  confirmed `.model` binds `pool[i % len]` and `model_prefix` default-guard,
  proving F1 fails if prefix ignored (not asserted by the verdict itself).
- Fold-not-surface control flow: Read fallback.py:459-474, 533-546 — confirmed
  the `except` discards the message (no `as e`) and folds to
  `fallback_config_missing`, independently substantiating the F2/F3 acceptance.
- Green confirmation: Bash `uv run pytest tests/swarm/test_openai_compat.py -q`
  → 29 passed (own tool engagement, not verdict reliance).

## QA Complete
