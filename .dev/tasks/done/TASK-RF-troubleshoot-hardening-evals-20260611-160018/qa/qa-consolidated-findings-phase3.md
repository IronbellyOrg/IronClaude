# Phase 3 QA — Consolidated Findings

**Consolidated verdict: FAIL** (2 of 6 lens agents reported issues; FAIL if ANY agent reports ANY issue).

## Lens verdicts (6 lens agents)

| Lens | Agent | Report | Verdict |
|------|-------|--------|---------|
| Structural — backtest_status enum + derivation | rf-qa | `qa-structural-status-derivation-report.md` | PASS |
| Structural — run_report.py model-idiom conformance | rf-qa | `qa-structural-report-idiom-report.md` | **FAIL** |
| Structural — JSON Schema + Draft202012Validator fidelity | rf-qa | `qa-structural-schema-fidelity-report.md` | PASS |
| Content — separation invariant + advisory signoff | rf-qa-qualitative | `qa-content-separation-report.md` | PASS |
| Content — proxy honesty + no-oversell | rf-qa-qualitative | `qa-content-proxy-honesty-report.md` | **FAIL** |
| Domain — ReplayExecutor seam fidelity | rf-qa-qualitative | `qa-domain-replay-executor-report.md` | PASS |

## Deduplicated issues

| # | Severity | File(s) | Issue | Required fix | Lens |
|---|----------|---------|-------|--------------|------|
| P3-1 | CRITICAL | `catch_rate_report.py` `write_catch_rate_report` | Writer runs `out.mkdir(...)` with no top-of-writer `_check(report)` → a broken invariant still creates the dir (partial artifact). Idiom (`write_aggregated_report` run_report.py:438) guards BEFORE mkdir. | Add `_check(report)` as the FIRST statement of `write_catch_rate_report` (before `Path(output_dir)`/`mkdir`), mirroring run_report.py:438. ALSO render both json+md payloads BEFORE writing either (atomicity: a render failure leaves no file). | report-idiom |
| P3-2 | CRITICAL | `catch_rate.py` (`_PROXY_NOTE` in `catch_rate_report.py`, docstrings) | OVERSELL-1: the `card_path` conjunct enforces only NON-NULL, not impl-ref-LANDED (no `.exists()`), yet wire text claims "complete only reachable once impl refs land". All three `is_fully_caught` conjuncts (CATCH/witness/card) are producer-asserted, not executed-gate observations. | (a) Reword `_PROXY_NOTE` + model/writer docstrings so wire text matches code: the model is a bookkeeping contract of PRODUCER-ASSERTED claims; card_path NON-NULLNESS is the data invariant, while card EXISTENCE (impl ref landed) is enforced UPSTREAM by the Phase 4 `requires_impl_ref` skip-guard + the aggregation (which only sets card_path from a verified-existing ref). (b) Add a pure, no-IO-in-model module-level helper `unresolved_card_paths(report, *, base_dir) -> tuple[str,...]` returning card paths that do NOT exist under base_dir, giving a real testable existence gate; add a test for it. Do NOT put filesystem IO inside the frozen `__post_init__`. | proxy-honesty |
| P3-3 | IMPORTANT | `catch_rate.py` `__post_init__`; `catch_rate.schema.json` | OVERSELL-2: `proxy_limitation` is required-present but not required-honest — default `""`, schema has no `minLength`; the JSON SoT can ship an empty caveat. | Add `"minLength": 1` to `proxy_limitation` in the schema AND a `__post_init__` guard on `CatchRateReport` rejecting an empty/whitespace `proxy_limitation` (raise ValueError). Confirm all fixtures + tests pass non-empty values. | proxy-honesty |
| P3-4 | IMPORTANT | `catch_rate_report.py` `render_catch_rate_markdown` | OVERSELL-3: the markdown headline `## Catch rate: X/5 (status)` foregrounds the number; the proxy caveat is only a trailing blockquote a skimmer misses → reads as executed-gate coverage. (Do NOT change the JSON schema `required[]` set — it is pinned by the fidelity test.) | Make the markdown headline carry the proxy qualifier inline (e.g. `## Catch rate (documentation-presence proxy): X/5 (status)`) and place the proxy-limitation note directly under the headline, not only at the end. JSON `catch_rate` interpretation stays bound by the serialized `proxy_limitation` field. | proxy-honesty |
| P3-5 | IMPORTANT | `catch_rate_report.py` `_check` / `CatchRateContractViolation` docstrings | The writer's `CatchRateContractViolation` is unreachable for any constructible (frozen) `CatchRateReport` because `__post_init__` already enforces both count checks. It is NOT dead code overall — the fidelity test exercises it via a duck-typed `SimpleNamespace` that bypasses the model. The "defense in depth" docstring overstates the path. | Reword the `_check` / `CatchRateContractViolation` docstrings to state precisely: the guard protects inputs that BYPASS the frozen model (duck-typed / mutated reports), which the fidelity test exercises directly; it is intentionally redundant for constructible `CatchRateReport`s (whose `__post_init__` enforces the same). Keep the guard. | report-idiom |
| P3-6 | MINOR | `catch_rate_report.py` exit-code constant | `CATCH_RATE_CONTRACT_VIOLATION_EXIT_CODE = 2` is an untyped bare literal vs run_report.py:56 sourcing `: int = _exit_codes.USAGE_ERROR`. | Annotate `: int` and add a comment pinning it to `superclaude.cli.eval.exit_codes.USAGE_ERROR` (= 2). Do NOT import the eval module into this test-tree file (keep it self-contained); the comment is sufficient. | report-idiom |

## Notes for the fix agent

- Touch ONLY files under `tests/troubleshoot/backtest/` (model, writer, schema, and the test file if adding the `unresolved_card_paths` test). Collision boundary + G1 no-caret preserved.
- Do NOT change the JSON Schema `required[]` array (pinned by the fidelity test) — minLength is a property constraint, not a required-set change.
- Keep the model PURE (no filesystem IO in `__post_init__`); the existence check is a separate module-level helper.
- After fixes: `uv run pytest tests/troubleshoot/backtest/ -v` (0 failed/0 errored), `uv run ruff check` + `uv run ruff format --check` clean.
