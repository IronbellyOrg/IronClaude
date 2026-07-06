---
status: success
tier_reached: 1
confidence: 0.92
escalation_reason: none
fix_authorized: true
test_is_wrong: false
behavior_is_documented: false
---

# Troubleshoot Report — PR #140 review comments (r3367342586, r3367342583)

| Field | Value |
|-------|-------|
| Target | 2 augmentcode[bot] review comments on PR #140 (`feature/prd-input-spec`) |
| Type | bug (PRD CLI correctness) |
| Tier reached | 1 (single-domain, high confidence → no escalation) |
| Confidence | 0.92 |
| Branch | `feature/prd-input-spec` (NOT the current checkout `feature/prd-spec-flag`) |
| File | `src/superclaude/cli/prd/executor.py` |
| Fix authorized | yes (`--fix`) — but not auto-applied; see Next Steps |

## Summary

Both review comments are **confirmed real defects** in the `--spec` deterministic-ingestion feature. **Finding 1 (low):** `_bind_specs()` does not deduplicate the input `spec_files`, so passing the same `--spec FILE` twice emits duplicate `SPECS` entries (and later duplicate `--file` attachments). **Finding 2 (medium):** the R5 "make silent degradation loud" WARN is gated on `self._config.spec_files`, which is **always empty on a `prd resume` run** (resume never accepts `--spec`), so the warning can never fire on the resume path even though bound `SPECS` are present in `parsed-request.json`.

## Documentation Context

No conflicting documented contract found. The code's own R5 comment (`executor.py:641-644`: "make silent degradation loud … despite the operator naming specs") and the `_bind_specs` docstring (`executor.py:1205-1206`: "Idempotent … never duplicates") corroborate the reviewer intent for both findings. No release/spec doc contradicts the proposed fixes; the fixes restore the *stated* contract rather than change it.

## Diagnosis

### Finding 1 — duplicate `--spec` values produce duplicate `SPECS` (low) — r3367342586

`_bind_specs()` iterates `for sp in spec_files` and appends one `specs` object per element. The only dedup present is on **parent directories** (`parent_dirs`), not on the spec paths themselves. Two identical `--spec foo.md --spec foo.md` therefore yield two identical `SPECS` objects, which downstream subprocesses attach twice via `--file` → wasted tokens/IO and noisier prompts/logs. The docstring already promises idempotency, so this is a contract gap, not a design choice.

### Finding 2 — resume-path WARN never fires (medium) — r3367342583

The `--spec` option is declared **only on `prd run`** (`commands.py:47`). The `resume` command (`commands.py:171`) calls `resolve_config(...)` **without a `spec=` argument** (`commands.py:204-214`), so `config.spec_files` is empty/`None` on every resume. Meanwhile the original run persisted the bound `SPECS` array into `parsed-request.json` (`_persist_bound_specs`, `executor.py:1245`). The gate `if step_id == "scope-discovery" and self._config.spec_files:` (`executor.py:645`) thus evaluates falsy on resume → `_warn_spec_degradation()` is never called, defeating R5's intent ("surface specs-present + scope-gate-failed regardless of how the run got there"). `_warn_spec_degradation()` itself also sources its message from `self._config.spec_files` (`executor.py:1274`), so it would print an empty spec list even if reached on resume.

## Evidence

- `src/superclaude/cli/prd/executor.py:1209` — `spec_files = list(self._config.spec_files or [])` (no dedup of paths)
- `src/superclaude/cli/prd/executor.py:1215` — `for sp in spec_files:` builds one `SPECS` entry per element; parent-dir dedup only
- `src/superclaude/cli/prd/executor.py:645` — `if step_id == "scope-discovery" and self._config.spec_files:` (resume-blind gate)
- `src/superclaude/cli/prd/executor.py:1245` — `_persist_bound_specs()` writes `SPECS` into `parsed-request.json` (the durable source of truth)
- `src/superclaude/cli/prd/executor.py:1274` — `specs = ", ".join(self._config.spec_files)` (message also empty on resume)
- `src/superclaude/cli/prd/commands.py:47` — `--spec` declared on `run` only
- `src/superclaude/cli/prd/commands.py:204-214` — `resume` → `resolve_config(...)` omits `spec=`

## Proposed Fix

### Fix 1 — dedup `spec_files` (order-preserving) in `_bind_specs`

In `executor.py` after `spec_files = list(self._config.spec_files or [])` / the empty guard, insert an order-preserving dedup keyed on the normalized `Path` string, then iterate the deduped list:

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

### Fix 2 — make the R5 WARN resume-aware via a `_bound_spec_paths()` helper

Add a helper that returns the authoritative spec paths from config **or** from the persisted `SPECS` array, then route both the gate and the message through it:

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

## Alternative Fixes Considered

- **Add `--spec` to `prd resume`** (so `config.spec_files` is repopulated): rejected as primary — places the burden on the operator to re-pass flags and still leaves the gate blind if they forget. The persisted `SPECS` array is the durable source of truth and the more robust gate input. (Could be added later as an ergonomic extra, out of scope here.)

## Risk + Rollback

- **Fix 1**: pure narrowing of inputs; behavior identical when no duplicates. Low risk. Verify idempotency test still passes; add a duplicate-input test.
- **Fix 2**: adds a soft-failing disk read on the scope-discovery gate-fail branch only (already an error path). `_bound_spec_paths()` fails closed (returns `[]`) on missing/corrupt `parsed-request.json`, preserving today's behavior. Verify the WARN now fires on a resumed scope-discovery gate failure and the message lists the persisted spec paths.

## Next Steps

`--fix` is set. Tier 3 remediation is **offered, not applied** (see prompt below). The MDTM task must target branch **`feature/prd-input-spec`**, not the current `feature/prd-spec-flag`. Per project rules, source edits go to `src/superclaude/...`; this file is already canonical source (not a `.claude/` mirror), so no sync-dev concern. Add/extend tests in `tests/cli_prd/` (or the existing spec-binding test module) for: duplicate `--spec` dedup, and resume-path WARN firing from persisted `SPECS`.
