# D-0101 — Evidence Record

## 1. Code artefacts

| Path | Status | Description |
|---|---|---|
| `src/superclaude/cli/eval/retry.py` | New | `RetryOncePolicy` module: `MCP_FLAKY_TAG`, `MCP_SERVER_FLAKY_ARTIFACT`, `RetryOncePolicy` (frozen dataclass), `is_mcp_flaky_tagged`, `is_flaky_outcome`. |
| `src/superclaude/cli/eval/runner.py` | Modified | Added `retry_policy` + `home_factory` kwargs; refactored `run()` into `run()` + `_execute_once()` so the retry path can re-invoke the lifecycle. |
| `tests/cli/eval/test_mcp_retry_once.py` | New | 26-test regression suite covering policy unit behaviour, EvalRunner integration, and NFR-REL2 compatibility. |
| `docs/eval/retry.md` | Modified | Replaced the "deferred" section with the concrete R3-mit contract: taxonomy table, manifest example, orthogonality with `retry_count`, OQ-10 closure note. |

## 2. Test evidence

| Suite | Tests | Result |
|---|---|---|
| `tests/cli/eval/test_mcp_retry_once.py` | 26 | All passing |
| `tests/cli/eval/test_retry_policy.py` (regression — NFR-REL2 baseline) | 11 | All passing |
| `tests/cli/eval/test_runner_class.py` (regression — FR-LC1 lifecycle) | 11 | All passing |
| **Total** | **48** | **48 passing** |

Verbatim pytest output captured under
`.dev/releases/current/cliEval/evidence/T05.23/`:

* `pytest-mcp-retry-once.txt` — the new test file alone.
* `pytest-regression-retry.txt` — the combined retry/runner suites.

## 3. Acceptance criteria mapping

| Phase-file AC | Test pin | Outcome |
|---|---|---|
| Tagged eval triggers retry-once on MCP failure | `test_runner_retries_once_on_mcp_flaky_failure` (asserts `spawn_count == 2`) | Pass |
| Persistent failure: `FAIL` + `mcp_server_flaky` artifact | Same test (asserts `outcome.status == "FAIL"` and artifact key present with value `"true"`) | Pass |
| Non-tagged evals do not retry (NFR-REL2 honored) | `test_runner_does_not_retry_untagged_eval` (asserts `spawn_count == 1`); plus `test_no_policy_means_no_retry_even_on_flaky_failure` | Pass |
| `D-0101/spec.md` documents the retry policy | `artifacts/D-0101/spec.md` written, 7 sections | Done |
| OQ-10 decision recorded | `D-0101/spec.md §6` records "keep R3-mit at P1, opt-in via `MCP-flaky` tag" | Done |

## 4. Regression guards

* **NFR-REL2 default unchanged.** `test_retry_policy.py::test_default_retry_count_is_zero` still passes; the additive `retry_policy` kwarg defaults to `None` so existing call-sites are byte-compatible.
* **`retry_count != 0` still rejected when policy is wired.** `test_mcp_retry_once.py::test_policy_does_not_unlock_nonzero_retry_count` pins this orthogonality.
* **FR-LC1 lifecycle unchanged.** `test_runner_class.py` (11 tests, all passing) confirms the `run()` → `_execute_once()` refactor did not alter event ordering, timeout behaviour, or interrupt propagation.

## 5. OQ-10 closure

OQ-10 asked whether R3-mit should remain at P1 (opt-in tag) or be
promoted to P0 (default-on). Empirical evidence from the M5 test
surface (T05.02..T05.21) shows MCP flake rates concentrated on a
small subset of evals; promoting to default-on would mask non-flake
bugs across the whole suite. **Decision:** keep R3-mit at P1.
Recorded in `D-0101/spec.md §6` and ready to land in `decisions.md
§B`.

## 6. Provenance

* Phase file row: `phase-5-tasklist.md` T05.23, R-100.
* Deliverable record: `artifacts/D-0101/spec.md`.
* Implementation notes: `artifacts/D-0101/notes.md`.
* Evidence index: `evidence/T05.23/SUMMARY.md`.
