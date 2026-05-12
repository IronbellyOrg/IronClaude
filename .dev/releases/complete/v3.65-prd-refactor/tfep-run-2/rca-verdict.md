# TFEP Run 2 — Root Cause Analysis Verdict

Date: 2026-04-03  
Scope: two remaining failures in `tests/roadmap/test_obligation_scanner_meta_context.py`

## Evidence collected
- Context file: `/config/workspace/IronClaude/.dev/releases/backlog/prd-skill-refactor/tfep-run-2/context.yaml`
- Scanner implementation: `/config/workspace/IronClaude/src/superclaude/cli/roadmap/obligation_scanner.py`
- Failing tests: `/config/workspace/IronClaude/tests/roadmap/test_obligation_scanner_meta_context.py`
- Reproduction run:
  - `uv run pytest tests/roadmap/test_obligation_scanner_meta_context.py -k "inline_code_scaffold_term_is_medium or code_block_still_medium" -v`
  - Result: both tests fail with empty obligation lists.

## Hypothesis testing timeline

### H1: Discharge-intent skip is suppressing inline-code obligation creation
- Target line from failing test: `- Remove all `placeholder` values from config`
- Verified `_is_discharge_intent_line(...) == True`.
- In `scan_obligations`, this branch executes before obligation append:
  - `if _is_discharge_intent_line(context_line): continue`
- Effect: scaffold hit (`placeholder`) is dropped entirely, so no MEDIUM obligation can exist.
- Status: **Confirmed root cause** for `test_inline_code_scaffold_term_is_medium`.

### H2: Code-block demotion logic is broken globally
- Probed scanner with fenced code samples using in-vocabulary terms:
  - `mock = {}`
  - `placeholder = 1`
  - `stubbed = f()`
- All produced obligations with severity `MEDIUM`.
- Status: **Falsified**. Code-block demotion itself is functioning for valid scaffold terms.

### H3: `mock_data` token in the failing code-block test is outside scanner vocabulary
- Scanner term regex is word-bounded:
  - `\bmock(?:ed|s)?\b`
- `mock_data` does not match because `_` is a word character; no word boundary after `mock`.
- Probe with non-code line `- mock_data = {}` produced zero obligations too.
- Status: **Confirmed**. The failing fixture uses an out-of-vocabulary token and expects a match.

## Root-cause verdict
This is a **mixed-cause pair**:
1. **Implementation defect (new regression):** over-broad discharge-intent `continue` drops obligations before MEDIUM demotion can occur.
2. **Test defect:** `test_code_block_still_medium` expects detection for `mock_data`, which is not part of FR-MOD1.1 scaffold-term matching semantics.

## Why only 2 failures remain after prior remediation
- Prior remediation introduced discharge-intent skipping; this newly created the inline-code failure.
- The code-block failure persists because its expectation is incompatible with current strict vocabulary semantics, independent of the discharge-intent change.

## Strictness / drift assessment
- Broadening scaffold regex to match identifier substrings (e.g., `mock_*`) would expand detection surface and risks behavioral drift.
- Minimal strict-preserving path is:
  - remove/narrow the hard skip behavior,
  - keep FR-MOD1.1 vocabulary boundaries intact,
  - align the one out-of-policy test fixture/expectation.
