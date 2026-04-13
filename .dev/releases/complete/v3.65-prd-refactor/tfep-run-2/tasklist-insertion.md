# Tasklist Insertion — TFEP Run 2 (Two Remaining Failures)

- [ ] **T1: Revert over-broad discharge-intent dropping behavior**
  - File: `/config/workspace/IronClaude/src/superclaude/cli/roadmap/obligation_scanner.py`
  - Change scope: remove/narrow unconditional `continue` on `_is_discharge_intent_line` so obligation records are still created and can be demoted to MEDIUM.
  - Exit criteria: inline-code placeholder case yields at least one MEDIUM obligation.

- [ ] **T2: Align code-block regression fixture with strict vocabulary contract**
  - File: `/config/workspace/IronClaude/tests/roadmap/test_obligation_scanner_meta_context.py`
  - Change scope: update `mock_data` fixture token to an FR-MOD1.1 scaffold term while preserving fenced-code MEDIUM assertion.
  - Exit criteria: test validates code-block demotion, not identifier-substring matching.

- [ ] **T3: Focused verification run**
  - Command:
    - `uv run pytest tests/roadmap/test_obligation_scanner_meta_context.py -k "inline_code_scaffold_term_is_medium or code_block_still_medium" -v`
  - Exit criteria: both tests pass.

- [ ] **T4: Guardrail regression check (scanner baseline)**
  - Command:
    - `uv run pytest tests/roadmap/test_obligation_scanner.py -q`
  - Exit criteria: no new failures in core obligation scanner suite.
