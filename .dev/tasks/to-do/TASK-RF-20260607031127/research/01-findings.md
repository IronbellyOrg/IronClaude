# Research: Verified findings + proposed fixes (PR #140 r3367342586, r3367342583)

**Topic type:** Consolidated findings (from /sc:troubleshoot Tier 1, evidence-validated)
**Scope:** `src/superclaude/cli/prd/executor.py`, `src/superclaude/cli/prd/commands.py`, `tests/cli/prd/test_spec_flag.py` on branch `origin/feature/prd-input-spec`
**Status:** Complete
**Date:** 2026-06-07

---

## Finding 1 — duplicate `--spec` values produce duplicate SPECS (LOW, r3367342586)

**Evidence:**
- `executor.py:1209` — `spec_files = list(self._config.spec_files or [])` [CODE-VERIFIED]
- `executor.py:1215` — `for sp in spec_files:` appends one `SPECS` object per element; only `parent_dirs` is deduped (L1233-1237), not the spec paths. [CODE-VERIFIED]
- Docstring (L1205-1206) promises idempotency / no duplicates — so this is a contract gap.

**Proposed fix (verbatim, insert after the empty-guard `return parsed` at ~L1211, before building `specs`):**

```python
spec_files = list(self._config.spec_files or [])
if not spec_files:
    return parsed

# Dedup duplicate --spec values (order-preserving): identical inputs must
# not produce duplicate SPECS entries / repeated --file attachments.
_seen: set[str] = set()
_deduped: list[str] = []
for sp in spec_files:
    key = str(Path(sp))
    if key not in _seen:
        _seen.add(key)
        _deduped.append(sp)
spec_files = _deduped
```

`Path` is already imported (used at L1216). Behavior is identical when no duplicates exist.

---

## Finding 2 — R5 resume-path WARN never fires (MEDIUM, r3367342583)

**Evidence:**
- `executor.py:645` — `if step_id == "scope-discovery" and self._config.spec_files:` [CODE-VERIFIED]
- `commands.py:47` — `--spec` declared only on `prd run`. [CODE-VERIFIED]
- `commands.py:204-214` — `prd resume` → `resolve_config(...)` omits `spec=`, so `config.spec_files` is empty on every resume. [CODE-VERIFIED]
- `executor.py:1245` `_persist_bound_specs` — bound `SPECS` persist in `parsed-request.json` (durable across resume). [CODE-VERIFIED]
- `executor.py:1274` — `specs = ", ".join(self._config.spec_files)` (message also empty on resume). [CODE-VERIFIED]

Conclusion: on `prd resume scope-discovery`, `self._config.spec_files` is empty though `SPECS` are bound → WARN never fires, defeating R5's intent.

**Proposed fix — new helper + route gate & message through it:**

```python
def _bound_spec_paths(self) -> list[str]:
    """Authoritative spec paths for this run: from config, else from the
    persisted SPECS array in parsed-request.json. On `prd resume`, --spec is
    not re-passed, so config.spec_files is empty even though the original run
    bound SPECS; reading the persisted array makes R5 fire on any run path."""
    if self._config.spec_files:
        return list(self._config.spec_files)
    parsed_path = self._config.task_dir / "parsed-request.json"
    try:
        parsed = json.loads(parsed_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    specs = parsed.get("SPECS") or []
    return [s["path"] for s in specs if isinstance(s, dict) and s.get("path")]
```

- Gate (`executor.py:645`): `if step_id == "scope-discovery" and self._bound_spec_paths():`
- Message (`executor.py:1274`): `specs = ", ".join(self._bound_spec_paths())`

`json` is already imported (used in `_persist_bound_specs` at L1255). Fail-closed on missing/corrupt JSON preserves current behavior.

**Rejected alternative:** adding `--spec` to `prd resume` — puts burden on the operator and leaves the gate blind if they forget. Persisted `SPECS` is the durable source of truth. [CODE-VERIFIED rationale]

---

## Regression tests to add — `tests/cli/prd/test_spec_flag.py`

1. **Dedup:** construct an executor/config with `spec_files=["foo.md", "foo.md"]`, call `_bind_specs({})`, assert exactly one `SPECS` entry for `foo.md` and `WHERE` is idempotent (one parent dir).
2. **Resume WARN:** with `config.spec_files` empty and a `parsed-request.json` (in `task_dir`) containing a non-empty `SPECS` array, drive a STANDARD scope-discovery gate failure (or call the gate branch / `_warn_spec_degradation` directly) and assert the WARN is emitted and lists the persisted spec path(s).
3. **Fail-closed:** `_bound_spec_paths()` returns `[]` when `parsed-request.json` is missing, and `[]` when it is corrupt (invalid JSON).

Match the existing fixture/mock patterns already used in `test_spec_flag.py` (read it first to mirror how the executor/config are constructed).
