# Research Acknowledgement — Phase 1.4

**Timestamp:** 2026-05-19 02:03 UTC
**Files read:**
- `.dev/tasks/to-do/TASK-RF-track-2-20260518-231708/research/01-file-inventory.md`
- `.dev/tasks/to-do/TASK-RF-track-2-20260518-231708/research/02-test-fixtures.md`
- `.dev/tasks/to-do/TASK-RF-track-2-20260518-231708/research/03-template-examples.md` (acknowledged structural reference; no new decisions)

## Canonical decisions confirmed

- `ENV_VAR_NAME=REFLEXION_OUTPUT_DIR` — confirmed in `01-file-inventory.md` top section (no `SUPERCLAUDE_*` precedent in `src/superclaude/cli/` or `src/superclaude/pm_agent/`; bare-name convention prevails). Used uniformly across production code, fixture, autouse safety net, and regression test docstrings.
- `BARE_CONSTRUCTOR_COUNT=7` — confirmed in `01-file-inventory.md` §4 and `02-test-fixtures.md` §1/§2 at `tests/unit/test_reflexion.py` lines L17, L25, L39, L52, L73, L118, L165.
- `PRESERVE_CWD_DEFAULT=YES` — confirmed in `01-file-inventory.md` OQ-2 and `02-test-fixtures.md` OQ-2. Resolution order: `explicit memory_dir arg > REFLEXION_OUTPUT_DIR env var > Path.cwd() / "docs" / "memory"`.
- `REGRESSION_TEST_USES_DYNAMIC_SNAPSHOT=YES` — confirmed in `02-test-fixtures.md` §5a and OQ-4. No hard-coded `"84"` or `"588"`; capture `pre_count`/`pre_size` at session-scoped fixture start via `stat`/`glob`, yield, then assert `post_count == pre_count` and `post_size == pre_size`.

## Layout note (Task Step 2.4/2.5 override)

The autouse safety-net fixture MUST use `tmp_path / "docs" / "memory"` (NOT the older `tmp_path / "reflexion_memory"` from `02-test-fixtures.md` §4) so that `mistakes_dir = memory_dir.parent / "mistakes"` resolves to `tmp_path / "docs" / "mistakes"`, mirroring production layout and matching the upgraded `reflexion_pattern` fixture in `src/superclaude/pytest_plugin.py`.
