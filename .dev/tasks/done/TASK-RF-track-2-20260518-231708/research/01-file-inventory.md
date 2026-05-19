# Research Track 2 — File Inventory (reflexion.py + callers)

**Task**: TASK-RF-track-2-20260518-231708 (FU-002: reflexion writer test pollution)
**Scope**: `src/superclaude/pm_agent/reflexion.py` + every caller of `ReflexionPattern`
**Goal**: Add output-dir override + env-var fallback so tests can redirect writes to `tmp_path`
**Status**: Complete (gap-filled 2026-05-18)
**Researcher**: Track 2 of 3
**File audited**: `/config/workspace/IronClaude/src/superclaude/pm_agent/reflexion.py` (345 lines)

---

## CANONICAL ENV-VAR NAME DECISION (gap-fill 2026-05-18)

**Canonical env-var name for this fix: `REFLEXION_OUTPUT_DIR`**

**Evidence / rationale** (verified by grep on `src/superclaude/cli/` and `src/superclaude/pm_agent/`, 2026-05-18):

- `grep -rE 'os\.environ\.get\("SUPERCLAUDE_|os\.getenv\("SUPERCLAUDE_' src/superclaude/` → **zero matches.** No `SUPERCLAUDE_*` namespace precedent exists in production code.
- `grep -rE 'os\.environ\.get\("REFLEXION_|os\.getenv\("REFLEXION_' src/superclaude/` → **zero matches.** Neither name has precedent.
- All existing env-var reads under `src/superclaude/cli/` + `src/superclaude/pm_agent/` are bare names (no shared prefix): `CLAUDE_MODEL` (commands.py:220), `SHELL` (install_mcp.py), `TMUX` (tmux.py:55).
- Per gap-fill rule: "If no `SUPERCLAUDE_*` precedent exists → use `REFLEXION_OUTPUT_DIR`." ✅

**This contradicts the name used in `02-test-fixtures.md` §4 / §5 (`SUPERCLAUDE_REFLEXION_MEMORY_DIR`)** — the builder must use `REFLEXION_OUTPUT_DIR` everywhere (production code, fixture, autouse safety net, and regression test docstrings). File 02 has been updated in this same gap-fill pass to match.

---

---

## 1. ReflexionPattern class anatomy

**File**: `src/superclaude/pm_agent/reflexion.py`
**Class declared**: L32
**Class docstring**: L33–54

### Instance attributes (set in `__init__`)
| Attribute | Line | Type | Default |
|---|---|---|---|
| `self.memory_dir` | L68 | `Path` | `Path.cwd() / "docs" / "memory"` |
| `self.solutions_file` | L69 | `Path` | `<memory_dir>/solutions_learned.jsonl` |
| `self.mistakes_dir` | L70 | `Path` | `<memory_dir>.parent / "mistakes"` → i.e. `docs/mistakes` when default |

### Methods (signature + 1-line purpose)
| Method | Lines | Signature | Purpose |
|---|---|---|---|
| `__init__` | L56–74 | `(self, memory_dir: Optional[Path] = None)` | Resolves dirs, calls `mkdir(parents=True, exist_ok=True)` on both `memory_dir` and `mistakes_dir` |
| `get_solution` | L76–100 | `(self, error_info: Dict[str, Any]) -> Optional[Dict[str, Any]]` | Public: lookup known solution via mindbase then local file search |
| `record_error` | L102–128 | `(self, error_info: Dict[str, Any]) -> None` | Public: append JSONL + optionally create mistake .md |
| `_create_error_signature` | L130–162 | `(self, error_info: Dict[str, Any]) -> str` | Build pipe-joined signature `type|message|test_name` (digits → "N") |
| `_search_mindbase` | L164–176 | `(self, error_signature: str) -> Optional[Dict[str, Any]]` | TODO stub; returns `None` |
| `_search_local_files` | L178–211 | `(self, error_signature: str) -> Optional[Dict[str, Any]]` | Reads solutions JSONL line-by-line, fuzzy match |
| `_signatures_match` | L213–236 | `(self, sig1: str, sig2: str, threshold: float = 0.7) -> bool` | Word-overlap Jaccard-style similarity |
| `_create_mistake_doc` | L238–308 | `(self, error_info: Dict[str, Any]) -> None` | Generate `<test_name>-YYYY-MM-DD.md` in `self.mistakes_dir` |
| `get_statistics` | L310–344 | `(self) -> Dict[str, Any]` | Read-only count of records in solutions_file |

---

## 2. Default-path computation

Exact code (L64–70):
```python
if memory_dir is None:
    # Default to docs/memory/ in current working directory
    memory_dir = Path.cwd() / "docs" / "memory"        # L66

self.memory_dir = memory_dir                            # L68
self.solutions_file = memory_dir / "solutions_learned.jsonl"  # L69
self.mistakes_dir = memory_dir.parent / "mistakes"      # L70
```

| Resolved path | File:line | Default (when `memory_dir=None` and cwd = repo root) |
|---|---|---|
| `memory_dir` | reflexion.py:66 | `<cwd>/docs/memory` |
| `solutions_file` | reflexion.py:69 | `<cwd>/docs/memory/solutions_learned.jsonl` |
| `mistakes_dir` | reflexion.py:70 | `<cwd>/docs/mistakes` |

Both directories are unconditionally `mkdir`'d at L73–74 — meaning **construction alone** creates `docs/memory/` and `docs/mistakes/` under the cwd. No env-var resolution exists today.

---

## 3. Write sites in reflexion.py

| Line | Operation | Target | Payload |
|---|---|---|---|
| L73 | `mkdir(parents=True, exist_ok=True)` | `self.memory_dir` | (directory creation) |
| L74 | `mkdir(parents=True, exist_ok=True)` | `self.mistakes_dir` | (directory creation) |
| L123 | `self.solutions_file.open("a")` | `solutions_learned.jsonl` | one JSONL record per `record_error` |
| L124 | `f.write(json.dumps(error_info) + "\n")` | (same as L123) | serialized error_info |
| L308 | `filepath.write_text(content)` | `<mistakes_dir>/<test_name>-<date>.md` | mistake markdown doc |

Read-only sites (not pollution sources but confirm path coupling): L190 `self.solutions_file.exists()`, L194 `self.solutions_file.open("r")`, L320, L330.

---

## 4. Callers of `ReflexionPattern` across the project

Result of `grep -rn "ReflexionPattern\|reflexion_pattern" src/ tests/ --include="*.py"`:

### Source (`src/`)
| File:line | Code | Instantiation args |
|---|---|---|
| `src/superclaude/__init__.py:13` | `from .pm_agent.reflexion import ReflexionPattern` | (re-export) |
| `src/superclaude/__init__.py:19` | `"ReflexionPattern"` in `__all__` | (re-export) |
| `src/superclaude/pm_agent/__init__.py:12` | `from .reflexion import ReflexionPattern` | (re-export) |
| `src/superclaude/pm_agent/__init__.py:18` | `"ReflexionPattern"` in `__all__` | (re-export) |
| `src/superclaude/pytest_plugin.py:15` | import | — |
| `src/superclaude/pytest_plugin.py:81` | `return ReflexionPattern()` (inside `reflexion_pattern` fixture, L71–81) | **no args -> defaults to cwd** |
| `src/superclaude/pytest_plugin.py:173` | `reflexion = ReflexionPattern()` (inside `pytest_runtest_makereport` hook, L160–184) | **no args -> defaults to cwd** |

### Tests (`tests/`)
| File:line | Instantiation args |
|---|---|
| `tests/unit/test_reflexion.py:17` | `ReflexionPattern()` — no args |
| `tests/unit/test_reflexion.py:25` | `ReflexionPattern()` — no args |
| `tests/unit/test_reflexion.py:39` | `ReflexionPattern()` — no args |
| `tests/unit/test_reflexion.py:52` | `ReflexionPattern()` — no args |
| `tests/unit/test_reflexion.py:73` | `ReflexionPattern()` — no args |
| `tests/unit/test_reflexion.py:100` | `ReflexionPattern(memory_dir=temp_memory_dir)` — **already overrides** |
| `tests/unit/test_reflexion.py:118` | `ReflexionPattern()` — no args |
| `tests/unit/test_reflexion.py:165` | `ReflexionPattern()` — no args |
| `tests/unit/test_reflexion.py:139` | uses `reflexion_pattern` fixture (no args from plugin) |
| `tests/integration/test_pytest_plugin.py:25,27,28,29,46` | uses `reflexion_pattern` fixture |

### Note on `self_correction.py`
`src/superclaude/execution/self_correction.py` references `reflexion_file` / `reflexion.json` but **does NOT use `ReflexionPattern`** — it has its own `self.memory_path / "reflexion.json"` flow. Out of scope for this fix.

---

## 5. Production vs test classification

| Caller | Class | Rationale |
|---|---|---|
| `src/superclaude/__init__.py` (re-export) | N/A | Just an import; no instantiation. Behavior preserved. |
| `src/superclaude/pm_agent/__init__.py` (re-export) | N/A | Same — import only. |
| `src/superclaude/pytest_plugin.py:81` (`reflexion_pattern` fixture) | **TEST-INFRA** | Lives in the pytest plugin; only fires when pytest is collecting tests. Currently `ReflexionPattern()` with no args -> writes to cwd `docs/memory/`. Must redirect to `tmp_path`. |
| `src/superclaude/pytest_plugin.py:173` (`pytest_runtest_makereport` hook) | **TEST-INFRA** | Auto-record on test failures with `@pytest.mark.reflexion`. Same cwd default -> same pollution. Must redirect when running tests. |
| `tests/unit/test_reflexion.py:17,25,39,52,73,118,165` | **TEST** | All bare `ReflexionPattern()` calls inside unit tests — write to repo `docs/memory/` today. Must redirect. |
| `tests/unit/test_reflexion.py:100` | **TEST (already safe)** | Passes `memory_dir=temp_memory_dir`; pattern to emulate. |
| `tests/integration/test_pytest_plugin.py` | **TEST** | Consumes fixture; safe once fixture is fixed. |

**Production callers requiring cwd-default preservation**: **None inside this codebase.** The class is currently only invoked by the pytest plugin and tests. External downstream consumers (anyone importing `superclaude.pm_agent.ReflexionPattern` in their own project code) is the implicit "production" surface that must keep working — i.e. `ReflexionPattern()` with no args must still resolve to `Path.cwd() / "docs" / "memory"` in absence of the env var.

---

## 6. Recommended override surface

### Resolution chain (priority order)
1. **Explicit constructor arg** `memory_dir=<Path>` — already exists; behavior unchanged.
2. **Env var** `REFLEXION_OUTPUT_DIR` — NEW; if set, treat as the memory_dir.
3. **cwd default** `Path.cwd() / "docs" / "memory"` — unchanged fallback.

### Exact patch for `reflexion.py` L56–74

```python
    def __init__(self, memory_dir: Optional[Path] = None):
        """
        Initialize reflexion pattern

        Args:
            memory_dir: Directory for storing error solutions.
                Resolution order:
                  1. Explicit `memory_dir` argument (if provided)
                  2. `REFLEXION_OUTPUT_DIR` environment variable (if set)
                  3. Default: ``Path.cwd() / "docs" / "memory"``
        """
        if memory_dir is None:
            env_override = os.environ.get("REFLEXION_OUTPUT_DIR")
            if env_override:
                memory_dir = Path(env_override)
            else:
                # Default to docs/memory/ in current working directory
                memory_dir = Path.cwd() / "docs" / "memory"

        self.memory_dir = memory_dir
        self.solutions_file = memory_dir / "solutions_learned.jsonl"
        self.mistakes_dir = memory_dir.parent / "mistakes"

        # Ensure directories exist
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self.mistakes_dir.mkdir(parents=True, exist_ok=True)
```

### Required import addition (top of file, after L26)
```python
import os
```
(currently imports: `json`, `datetime`, `Path`, `typing.Optional/Any/Dict` — `os` is missing)

### Lines touched
- L26 area: add `import os` (1 new line)
- L64–66: expand 3-line `if memory_dir is None:` block into 6-line env-var-aware block

Total delta: ~6 added lines, 0 removed (purely additive; backward-compatible for any external caller).

### Why this surface is sufficient
- The conftest/fixture changes (Track 02) can simply `monkeypatch.setenv("REFLEXION_OUTPUT_DIR", str(tmp_path / "memory"))` autouse-style, and **every** call site — fixture, plugin hook, bare `ReflexionPattern()` in tests — will redirect.
- No need to modify call sites individually.
- External consumers calling `ReflexionPattern()` with no args and no env var still get the documented cwd behavior.

---

## Summary

- `ReflexionPattern` writes occur at 3 lines (L73 mkdir, L74 mkdir, L123-124 append, L308 write_text) — all rooted in `self.memory_dir` / `self.mistakes_dir` computed at L66/L69/L70.
- All in-repo instantiations except `tests/unit/test_reflexion.py:100` use bare `ReflexionPattern()` and pollute repo `docs/memory/` + `docs/mistakes/`.
- The fix surface is a 6-line additive change inside `__init__` introducing an `os.environ` lookup for `REFLEXION_OUTPUT_DIR`, leaving the existing `memory_dir` param and cwd default intact.

---

## Gaps and Questions (gap-fill 2026-05-18)

Open Questions surfaced during research re-verification — flagged for the builder to resolve in the generated task file, not blocking research handoff:

1. **OQ-1 (resolved): Canonical env-var name** — see top of this file. Use `REFLEXION_OUTPUT_DIR`.

2. **OQ-2: Preserve cwd default? (recommended: YES)**
   - Question: should the absence of both `memory_dir=` arg and `REFLEXION_OUTPUT_DIR` env var continue to fall back to `Path.cwd() / "docs" / "memory"`, OR should we move the default to `Path.home() / ".superclaude" / "memory"` (XDG-style)?
   - Recommendation: **preserve cwd default**. External downstream consumers (anyone who pip-installed `superclaude` and imports `ReflexionPattern()` with no args) currently rely on cwd resolution; changing it is a silent behavior break. The pollution problem is solved by tests setting the env var, not by changing the default.
   - **Builder default**: preserve cwd unless explicit user request otherwise.

3. **OQ-3 (load-bearing): Phase 1 baseline cleanse**
   - Question: should the FU-002 task include a Phase 1 item to remove the **pre-existing pollution** (84 polluted `docs/mistakes/*.md` files + 588 polluted lines in `docs/memory/solutions_learned.jsonl` — re-measured 2026-05-18) before adding the regression test?
   - Recommendation: **YES, include in Phase 1.** The regression test (per `02-test-fixtures.md` §5) needs a clean baseline. Without cleansing, the regression test must either snapshot the dirty baseline (fragile, drift-prone) or fail on landing.
   - Concrete actions for Phase 1 of the generated task:
     1. `git rm docs/mistakes/test_*-*.md docs/mistakes/unknown-*-*.md` (or whichever subset is test pollution — verify each file before deleting; some may be legitimate human-authored mistakes docs).
     2. `git restore --source=<pre-pollution-sha> -- docs/memory/solutions_learned.jsonl` OR construct a clean baseline by filtering out test-shaped error records.
     3. Run `uv run pytest tests/unit/test_reflexion.py` with the fix applied; confirm no new files appear.

4. **OQ-4: Should the regression test use a DYNAMIC snapshot rather than hard-coded numbers?**
   - Recommendation: **YES, dynamic.** Don't hard-code "84 files" or "588 lines" — capture `pre_count`/`pre_size` at fixture-start via stat, yield, then assert `post_count == pre_count`. See `02-test-fixtures.md` §5a for the exact pattern.
