# D-0063 — Evidence (T03.22)

## Verification commands

### 1. Run the new integration tests

```
$ uv run pytest tests/cli/eval/test_pty_lifecycle.py tests/cli/eval/test_ban_import_rule.py -v
```

Result: **8 passed in 1.83s** on 2026-05-20. Full log:
`TASKLIST_ROOT/evidence/T03.22/pytest-pty-lifecycle-and-ban-import.txt`.

| Test | Verdict |
|---|---|
| `test_real_claude_help_spawn_and_transcript` | PASSED — real `claude` binary present at `/config/.local/bin/claude` (v2.1.145). |
| `test_lifecycle_prompt_ready_and_input_injection` | PASSED |
| `test_lifecycle_timeout_reaps_child` | PASSED |
| `test_lifecycle_transcript_persisted_end_to_end` | PASSED |
| `test_eval_package_does_not_import_anthropic_at_runtime` | PASSED |
| `test_clean_tree_passes_ruff_check` | PASSED |
| `test_synthetic_import_anthropic_is_flagged_by_ruff` | PASSED |
| `test_ban_message_references_fr_g1` | PASSED |

### 2. Clean-tree ruff check

```
$ uv run ruff check src/superclaude/cli/eval/
All checks passed!
```

Full log: `TASKLIST_ROOT/evidence/T03.22/ruff-clean-tree.txt`.

### 3. Synthetic `import anthropic` injection

Probe file created at
`src/superclaude/cli/eval/_probe_evidence_synth/probe.py` with body:

```python
import anthropic
_ = anthropic
```

Then:

```
$ uv run ruff check src/superclaude/cli/eval/
TID251 `anthropic` is banned: FR-G1: in-process anthropic SDK imports are banned. Use the real `claude` subprocess via PtyDriver (cli/eval/pty_driver.py) or ClaudeProcessAdapter (cli/eval/claude_process.py).
 --> src/superclaude/cli/eval/_probe_evidence_synth/probe.py:1:8
  |
1 | import anthropic
  |        ^^^^^^^^^
2 | _ = anthropic
  |
Found 2 errors.
exit=1
```

Full log: `TASKLIST_ROOT/evidence/T03.22/ruff-synthetic-import-anthropic.txt`.

Probe directory deleted after capture; subsequent `uv run ruff check src/superclaude/cli/eval/` returns `All checks passed!` again.

## AC verification table

| AC | Requirement | Evidence |
|----|-------------|----------|
| AC1 | `test_pty_lifecycle.py` runs a fixture spawning the real claude binary via PTY and exits 0. | `pytest-pty-lifecycle-and-ban-import.txt`: 5/5 PTY tests passed; `test_real_claude_help_spawn_and_transcript` PASSED (not skipped). |
| AC2 | Asserts: prompt readiness observed, input injected, transcript file written, timeout reaps child. | Same log: `test_lifecycle_prompt_ready_and_input_injection`, `test_lifecycle_transcript_persisted_end_to_end`, `test_lifecycle_timeout_reaps_child` all PASSED. |
| AC3 | `uv run ruff check src/superclaude/cli/eval/` exits 0 on clean tree AND exits non-zero on synthetic `import anthropic`; `banned-api` declares the rule. | `ruff-clean-tree.txt` shows exit 0; `ruff-synthetic-import-anthropic.txt` shows exit 1 with TID251 + FR-G1 message; `pyproject.toml` carries `[tool.ruff.lint.flake8-tidy-imports.banned-api]` (lines 205-208). |
| AC4 | `artifacts/D-0063/spec.md` documents the lifecycle test matrix and ban-import rule configuration. | `spec.md` written (this directory). |

## Regression check

```
$ uv run pytest tests/cli/eval/ -q
```

Run as a follow-up to confirm the new tests did not regress neighbouring
suites; result captured in
`TASKLIST_ROOT/evidence/T03.22/pytest-cli-eval-regression.txt`.
