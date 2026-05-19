# Research Notes — TASK-RF-track-2 (FU-002: reflexion writer test pollution)

**Scenario:** A (Explicit — stubs gave hypotheses, references, acceptance criteria)
**Depth Tier:** Standard
**Track Count:** 3 of 3 (multi-track build)
**Template:** 02 (Complex — discovery + fix + test + validation phases)

---

## GOAL

Add an output-dir override to `ReflexionPattern` constructor so tests can redirect writes to `tmp_path` and stop polluting `docs/mistakes/` + `docs/memory/solutions_learned.jsonl`.

## WHY

The reflexion writer's default `memory_dir = Path.cwd() / "docs" / "memory"` (`reflexion.py` L67) means every `uv run pytest tests/` run pollutes the actual repo files. Phase 3 cleanup is undone on every test run. Tracked tests at `tests/unit/test_reflexion.py`.

---

## 1. EXISTING_FILES

- `src/superclaude/pm_agent/reflexion.py` (10095 bytes)
  - L67-78: `__init__` with `memory_dir` default `Path.cwd() / "docs" / "memory"` — THE BUG
  - L242: writes `docs/mistakes/[feature]-YYYY-MM-DD.md`
  - L15, L107-108: docstring references
- `tests/unit/test_reflexion.py` — reflexion unit tests
- `tests/conftest.py` — pytest fixtures (likely `reflexion_pattern` fixture per CLAUDE.md)
- `tests/integration/test_pytest_plugin.py` — integration tests including reflexion
- Reference stub: `.dev/tasks/to-do/follow-ups/FU-002-reflexion-test-pollution-source-fix.md`

## 2. PATTERNS_AND_CONVENTIONS

- Pytest plugin fixtures: `reflexion_pattern`, `pm_context`, etc. per CLAUDE.md docs
- Test isolation pattern in the project: pytest's `tmp_path` builtin
- Env var override pattern: project uses `os.environ.get(...)` in CLI/config code

## 3. GAPS_AND_QUESTIONS

- Is the bug solvable by ONLY changing the conftest.py fixture (pass `tmp_path` to `ReflexionPattern`), or does it also need a constructor change? (Likely both for defense-in-depth.)
- Are there callers in production that depend on the cwd-default behavior?
- Should the override be env-var-based (`REFLEXION_OUTPUT_DIR`) or constructor-param-only?

## 4. RECOMMENDED_OUTPUTS

3 researchers:

- `research/01-file-inventory.md` — `reflexion.py` exhaustive (all methods, all writes, all callers via grep)
- `research/02-test-fixtures.md` — read `conftest.py` + `test_reflexion.py` + `test_pytest_plugin.py`; document existing fixture pattern and identify exact monkeypatching needed
- `research/03-template-examples.md` — read `.claude/templates/workflow/02_mdtm_template_complex_task.md` PART 1 + identify project's existing env-var-override pattern (e.g., grep `os.environ.get` in `src/superclaude/cli/`)

## 5. SUGGESTED_PHASES

1. Inventory + caller map (every place that constructs `ReflexionPattern`)
2. Add `REFLEXION_OUTPUT_DIR` env-var override + keep constructor param
3. Update test fixtures to use `tmp_path` (`conftest.py` + test files)
4. Add regression test (assert no `docs/mistakes` pollution after pytest)
5. Production-callers verification (make sure no breakage)
6. Test phase + Validation phase
7. Completion

## 6. TEMPLATE_NOTES

Template 02. Standard tier.

## 7. AMBIGUITIES_FOR_USER

- Env-var name (`REFLEXION_OUTPUT_DIR` vs `REFLEXION_MEMORY_DIR`)
- Whether tests should also set env-var as defense-in-depth or only rely on constructor injection
