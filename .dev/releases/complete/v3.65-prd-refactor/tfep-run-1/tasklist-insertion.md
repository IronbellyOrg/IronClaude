# Tasklist Insertion — TFEP Run 1 (Obligation Scanner Meta-Context)

## Insert after current in-flight obligation-scanner tasks

- [ ] **T1: Correct expectation defects in meta-context param tests**
  - File: `/config/workspace/IronClaude/tests/roadmap/test_obligation_scanner_meta_context.py`
  - Update expected outcomes for:
    - `Do not remove the mock yet`
    - second-term case in `Remove old stubs and add new placeholder` (or split fixture per clause)
  - Exit criteria: these two parameterized cases align with chosen policy (line-level vs clause-level).

- [ ] **T2: Exclude discharge-intent lines from obligation creation**
  - File: `/config/workspace/IronClaude/src/superclaude/cli/roadmap/obligation_scanner.py`
  - Add narrow guard so scaffold matches on explicit discharge lines are not emitted as new obligations.
  - Exit criteria: mixed-document and simple discharge fixtures stop accumulating spurious obligations.

- [ ] **T3: Strengthen component extraction/matching for discharge linkage**
  - File: `/config/workspace/IronClaude/src/superclaude/cli/roadmap/obligation_scanner.py`
  - Improve component anchor quality (avoid verb-only anchors like `create`/`replace`).
  - Exit criteria: `create stub handler` -> `replace stub handler` marks at least one discharged obligation.

- [ ] **T4: Fix code-block MEDIUM demotion regression on compact fenced fixtures**
  - File: `/config/workspace/IronClaude/src/superclaude/cli/roadmap/obligation_scanner.py`
  - Ensure fenced code detection remains correct through phase slicing and absolute position mapping.
  - Exit criteria: `test_code_block_still_medium` passes consistently.

- [ ] **T5: Regression validation run**
  - Commands:
    - `uv run pytest tests/roadmap/test_obligation_scanner_meta_context.py -q`
    - `uv run pytest tests/roadmap/test_obligation_scanner.py -q`
  - Exit criteria: no failures in either file.
