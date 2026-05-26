# Task — PR #79 Medium-Findings Remediation

Source: `REVIEW.md` (M1 + M2 only; Lows/Nits deferred to follow-up PRs)
Branch: `fix/roadmap-template-and-cosmetic-remediation`
HEAD: `4a647c44`
Time budget: ~10 minutes

## Context

PR #79 ships a 9× `u2014` template fix plus a cosmetic-failure auto-remediation lane. The auggie review flagged two Mediums worth addressing in-PR. M1 is a perf refactor on `cosmetic_remediator.py`; M2 is defensive error-handling on the pipeline executor's remediation call site. Lows and Nits are explicitly out of scope.

**Pre-existing analysis note (semantic preservation — load-bearing):** The current `_is_in_fenced_block(lines, idx)` counts fence markers in `lines[:idx]` (i.e. `range(idx)`), so the **opener-marker line returns False (excluded)** and the **closer-marker line returns True (included)**. The reviewer's quoted `inside = not inside` skeleton would change this. The M1 refactor MUST preserve the existing truth function bit-for-bit — the new `_compute_fenced_indices(lines)` must satisfy `(idx in _compute_fenced_indices(lines)) == _is_in_fenced_block(lines, idx)` for every idx. The new test should pin this equivalence rather than asserting a single interpretation.

## M1 — Eliminate O(N²) in `_is_in_fenced_block`

- [ ] Edit `src/superclaude/cli/roadmap/cosmetic_remediator.py`:
  - Add helper `_compute_fenced_indices(lines: list[str]) -> set[int]` right after the existing `_is_in_fenced_block` definition (after line 210). Implement via test-before-increment over `enumerate(lines)`: track a running fence count, set membership = (count is odd at this point, BEFORE bumping it for the current line if it's a fence delimiter). This preserves the asymmetric semantics.
  - Replace each `_is_in_fenced_block(lines, idx)` call (7 sites: L253 inside `_detect_cosmetic_violations`, plus L446, L538, L583, L616, L640, L712 inside the 5 `_apply_*` helpers) with `idx in fenced_indices`. Each enclosing function already constructs its own `lines = content.splitlines(...)` so insert `fenced_indices = _compute_fenced_indices(lines)` immediately after that local — no parameter threading needed.
  - Keep `_is_in_fenced_block` itself as a thin wrapper: `return idx in _compute_fenced_indices(lines)` — it stays available as the equivalence oracle for the new test. (Deletion is acceptable but only after the equivalence test is committed and green.)
- [ ] Add a unit test in `tests/roadmap/test_cosmetic_remediator.py`:
  - Name: `test_compute_fenced_indices_matches_is_in_fenced_block` (or follow existing `TestX` class style).
  - Build a markdown sample with 3-4 fenced regions (some adjacent text, some empty lines, at least one region of length 1 between fences).
  - Assert: for every `idx in range(len(lines))`, `(idx in _compute_fenced_indices(lines)) == _is_in_fenced_block(lines, idx)`.

## M2 — Wrap remediator call in try/except

- [ ] Edit `src/superclaude/cli/pipeline/executor.py` around the cosmetic-remediation block (currently L286-341 inside `_execute_single_step`):
  - Wrap the entire `if config.allow_cosmetic_remediation and config.cosmetic_remediator is not None and step.gate is not None:` body — including the `config.cosmetic_remediator(...)` call AND the post-remediation `gate_passed` recheck — in a single `try / except Exception as exc:  # noqa: BLE001` block at the same indent level.
  - On exception: `_log.warning("Cosmetic remediator raised %s for step '%s'; falling through to FAIL", exc.__class__.__name__, step.id)`. Do NOT mutate `reason` — let it fall through to the existing FAIL path at L343-365 with the original gate failure reason intact.
  - Logger is `_log = logging.getLogger("superclaude.pipeline.executor")` declared at L38 — already in scope, no import change.
- [ ] Add a test in `tests/roadmap/test_executor.py` (existing test file that imports `execute_pipeline` from `superclaude.cli.pipeline.executor`):
  - Inject a `cosmetic_remediator` callable that does `raise RuntimeError("test")` into a `PipelineConfig` with `allow_cosmetic_remediation=True` and a step whose `gate.semantic_checks` fails.
  - Assert the resulting `StepResult.status == StepStatus.FAIL` (no crash, no propagated exception).
  - Assert `result.gate_failure_reason` is the original gate failure reason (NOT empty, NOT the exception text).
  - Optionally use `caplog` (caplog idiom already present in this file around L1126/L1156-1162) to assert a WARNING was emitted from logger `"superclaude.pipeline.executor"` mentioning `RuntimeError`.

## Verification

- [ ] `cd /config/workspace/IronClaude && uv run pytest tests/roadmap/test_cosmetic_remediator.py tests/roadmap/test_executor.py tests/roadmap/test_pipeline_integration.py tests/roadmap/test_halt.py tests/roadmap/test_gates_data.py -q` — all must pass.
- [ ] `make lint` — clean on the two source files and the two test files.
- [ ] `make sync-dev` — succeeds (no `.claude/` mirror drift).

## Out of scope (leave for follow-up PRs)

L1 (CRLF blank-line collapse), L2 (`\xa0` regex tightening), L3 (`--allow-cosmetic-remediation` user docs), L4 (multi-milestone test coverage), L5 (CRLF test), and N1-N7 (all Nits) from `REVIEW.md`.

## Hard constraints

- Stay on `fix/roadmap-template-and-cosmetic-remediation`. No new branch, no rebase, no force-push.
- Stage files individually by name. Never `git add -A`, `git add .`, or `git add .claude/...`.
