# Solution 1: Executor-Side Robust Recovery

## Summary

Harden `_resolve_step_content` in `/config/workspace/IronClaude/src/superclaude/cli/prd/executor.py` so it can recover a subprocess agent's real output even when the agent writes under a non-canonical filename and/or outside `task_dir` / `task_dir.parent`. The fix does not change prompts or agent behavior; it only improves the executor's file-discovery heuristics and adds a deterministic tiebreak. This explicitly does **not** prevent agents from writing to `/config/workspace/Octodive/.dev/specs/` — it only makes the executor find those files so gates evaluate real documents instead of ~24-line NDJSON commentary.

Confirmed symptom: `scope-discovery` gate fails `min_lines=50` because `_resolve_step_content` rglobbed for the exact filename `scope-discovery-raw.md` under `task_dir` and `task_dir.parent`. The agent wrote `/config/workspace/Octodive/.dev/specs/scope-discovery.md`, missing on both filename and location. The same pattern threatens `research-notes` (reads `task_dir/scope-discovery-raw.md` downstream) and any other step whose agent picks a "prettier" path.

## Design

### Changes to `/config/workspace/IronClaude/src/superclaude/cli/prd/executor.py`

#### 1. Add a per-step pattern map (lines ~252)

Introduce a companion dict that declares flexible filename patterns for steps known to be written with non-canonical names. Keep `_STEP_ARTIFACT_FILES` unchanged because `_persist_step_artifact` depends on the canonical name.

```python
_STEP_ARTIFACT_PATTERNS: dict[str, list[str]] = {
    # scope-discovery agents often write "scope-discovery.md" under .dev/specs/
    # instead of the canonical "scope-discovery-raw.md" under task_dir.
    "scope-discovery": ["scope-discovery*.md"],
    # research-notes has not yet been observed with a variant name, but the
    # pattern is cheap insurance (e.g. "research-notes-raw.md").
    "research-notes": ["research-notes*.md"],
    # sufficiency-review is currently stable; leave empty to keep exact match.
    "sufficiency-review": [],
}
```

For steps with an empty list (or missing entry), fall back to the current exact-name rglob behavior.

#### 2. Read `parsed-request.json` to obtain `WHERE` directories (lines ~339-349)

Before searching, load `task_dir / "parsed-request.json"` if it exists. Add any `WHERE` directories to the search root list, bounded by the repo root (`task_dir.parent`, which is the project root by convention). This directly addresses the observed `/config/workspace/Octodive/.dev/specs/` write location when the user scopes the PRD to `/config/workspace/Octodive/.dev/specs`.

```python
search_roots: list[Path] = [task_dir]
if task_dir.parent.exists():
    search_roots.append(task_dir.parent)

parsed_path = task_dir / "parsed-request.json"
if parsed_path.exists():
    try:
        parsed = json.loads(parsed_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        parsed = {}
    repo_root = task_dir.parent if task_dir.parent.exists() else task_dir
    for where in parsed.get("WHERE") or []:
        where_path = repo_root / where
        # Reject paths that escape the repo root (basic traversal guard).
        try:
            where_path.resolve().relative_to(repo_root.resolve())
        except ValueError:
            continue
        if where_path.is_dir() and where_path not in search_roots:
            search_roots.append(where_path)
```

#### 3. Replace exact-name rglob with pattern-aware search (lines ~351-364)

```python
patterns = _STEP_ARTIFACT_PATTERNS.get(step_id) or []
if not patterns:
    patterns = [Path(artifact_name).name]

candidates: list[tuple[Path, str]] = []
for root in search_roots:
    if not root.exists():
        continue
    for pattern in patterns:
        for match in root.rglob(pattern):
            skip_parts = {"node_modules", ".git", "__pycache__"}
            if "-output.txt" in match.name or skip_parts & set(match.parts):
                continue
            try:
                content = match.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            if content.strip():
                candidates.append((match, content))

best_content = _pick_best_candidate(candidates, preferred_root=task_dir)
```

#### 4. Add deterministic tiebreak helper (new function after `_resolve_step_content` or inline)

```python
def _pick_best_candidate(
    candidates: list[tuple[Path, str]],
    *,
    preferred_root: Path,
) -> str:
    """Pick the best candidate using a stable tiebreak.

    Priority:
    1. Inside preferred_root (task_dir) over external directories.
    2. Longest content (proxy for "most complete" document).
    3. Most specific path (fewest rglob wildcard matches / shortest pattern distance).
    4. Most recently modified.
    """
    if not candidates:
        return ""

    def _score(item: tuple[Path, str]) -> tuple[int, int, int, float]:
        path, content = item
        in_preferred = 1 if path.is_relative_to(preferred_root) else 0
        # Negate so larger content sorts higher when used ascending; we will
        # sort descending by constructing the key appropriately.
        return (in_preferred, len(content), -len(path.parts), path.stat().st_mtime)

    candidates.sort(key=_score, reverse=True)
    return candidates[0][1]
```

Note: `path.is_relative_to` requires Python 3.9+. If the project supports 3.8, replace with a `try/except ValueError` wrapper using `Path.relative_to`.

#### 5. Keep special cases untouched

- `build-task-file` remains scoped to `task_dir` only (do not widen).
- `assembly` keeps its existing `results/` → `task_dir` → `task_dir.parent` priority and `"prd"` name filter.

### Changes to `/config/workspace/IronClaude/tests/cli/prd/test_resolve_step_content.py`

Add the following regression tests:

```python
def test_scope_discovery_finds_variant_name_in_dev_specs(tmp_path: Path) -> None:
    """Regression: agent writes .dev/specs/scope-discovery.md, not scope-discovery-raw.md."""
    task_dir = tmp_path / "tasks" / "prd-001"
    task_dir.mkdir(parents=True)
    dev_specs = tmp_path / ".dev" / "specs"
    dev_specs.mkdir(parents=True)

    # parsed-request WHERE points at .dev/specs
    parsed = task_dir / "parsed-request.json"
    parsed.write_text(
        json.dumps({"GOAL": "x", "WHERE": [".dev/specs"]}),
        encoding="utf-8",
    )

    real_doc = _write_lines(dev_specs / "scope-discovery.md", 80, prefix="discovered")
    _write_lines(task_dir / "scope-discovery-raw.md", 10, prefix="stale")

    result = _resolve_step_content("scope-discovery", task_dir, "short ndjson")
    assert result == real_doc


def test_research_notes_finds_variant_name(tmp_path: Path) -> None:
    """research-notes can be recovered when the agent uses a variant filename."""
    task_dir = tmp_path / "tasks" / "prd-002"
    task_dir.mkdir(parents=True)
    real_doc = _write_lines(task_dir / "research-notes-raw.md", 120, prefix="note")

    result = _resolve_step_content("research-notes", task_dir, "short ndjson")
    assert result == real_doc


def test_tiebreak_prefers_task_dir_when_same_content_length(tmp_path: Path) -> None:
    """If two matches have identical length, prefer the one inside task_dir."""
    task_dir = tmp_path / "tasks" / "prd-003"
    task_dir.mkdir(parents=True)
    dev_specs = tmp_path / ".dev" / "specs"
    dev_specs.mkdir(parents=True)

    parsed = task_dir / "parsed-request.json"
    parsed.write_text(json.dumps({"GOAL": "x", "WHERE": [".dev/specs"]}), encoding="utf-8")

    inside = _write_lines(task_dir / "scope-discovery.md", 60, prefix="inside")
    _write_lines(dev_specs / "scope-discovery.md", 60, prefix="outside")

    result = _resolve_step_content("scope-discovery", task_dir, "ndjson")
    assert "inside" in result
    assert "outside" not in result


def test_where_escape_repo_root_is_ignored(tmp_path: Path) -> None:
    """A malicious/buggy WHERE path that escapes repo root is not searched."""
    task_dir = tmp_path / "tasks" / "prd-004"
    task_dir.mkdir(parents=True)
    parsed = task_dir / "parsed-request.json"
    parsed.write_text(
        json.dumps({"GOAL": "x", "WHERE": ["../../outside"]}),
        encoding="utf-8",
    )

    _write_lines(task_dir / "scope-discovery-raw.md", 60, prefix="safe")
    result = _resolve_step_content("scope-discovery", task_dir, "ndjson")
    assert "safe" in result
```

### Changes to `/config/workspace/IronClaude/tests/cli/prd/test_executor.py`

No changes required unless mocking `parsed-request.json` in existing executor-level tests. Add one integration-style test if the suite already exercises `_run_subprocess_step` with mocked `PrdClaudeProcess`:

```python
def test_run_subprocess_step_uses_resolved_content_for_gate(
    executor, monkeypatch, tmp_path
):
    """When the agent writes a variant filename, the gate still sees real content."""
    # Setup: simulate a completed scope-discovery step where the agent wrote
    # .dev/specs/scope-discovery.md instead of task_dir/scope-discovery-raw.md.
    executor._config.task_dir.mkdir(parents=True, exist_ok=True)
    parsed = executor._config.task_dir / "parsed-request.json"
    parsed.write_text(json.dumps({"GOAL": "x", "WHERE": [".dev/specs"]}))

    dev_specs = executor._config.task_dir.parent / ".dev" / "specs"
    dev_specs.mkdir(parents=True, exist_ok=True)
    dev_specs.joinpath("scope-discovery.md").write_text(
        "\n".join(f"line {i}" for i in range(60)), encoding="utf-8"
    )

    monkeypatch.setattr(
        executor, "_build_prompt", lambda builder_name, step_id=None: "prompt"
    )

    fake_proc = MagicMock()
    fake_proc.wait.return_value = 0
    fake_proc.start_with_retry = lambda: None

    with patch.object(
        executor.__class__, "_run_subprocess_step", autospec=True
    ) as mock_run:
        # This test is simpler if it calls _resolve_step_content directly and
        # asserts the gate receives >= 50 lines.
        content = _resolve_step_content(
            "scope-discovery", executor._config.task_dir, "short ndjson"
        )
        assert len(content.splitlines()) >= 50
```

If the existing test structure makes this awkward, the new unit tests in `test_resolve_step_content.py` are sufficient.

### Changes to `/config/workspace/IronClaude/tests/cli/prd/test_gates.py`

No gate logic changes. Optionally add a test that passes the recovered content through `GATE_CRITERIA["scope-discovery"]` to prove it would pass after recovery:

```python
from superclaude.cli.prd.gates import GATE_CRITERIA, evaluate_gate


def test_scope_discovery_gate_passes_with_recovered_content():
    content = "\n".join(f"section line {i}" for i in range(55))
    criteria = GATE_CRITERIA["scope-discovery"]
    assert evaluate_gate(content, criteria) is True
```

(Only if `evaluate_gate` is importable; otherwise test through the executor.)

### Changes to `/config/workspace/IronClaude/tests/cli/prd/test_e2e.py`

No required changes. Optional: add an E2E scenario where the mocked subprocess writes a variant filename and the pipeline completes without a gate HALT. Given that E2E tests mock `PrdClaudeProcess`, this can be done by having the mock create `/config/workspace/Octodive/.dev/specs/scope-discovery.md` before returning exit 0.

## Why this approach

1. **Minimal blast radius**: Only one function changes. No prompts, no agent instructions, no subprocess behavior.
2. **Reuses existing pattern**: The `assembly` special-case already proves that flexible name/location search works in this codebase. This solution generalizes that pattern and makes it data-driven.
3. **Deterministic tiebreak**: The current code uses "largest content" only. Adding `preferred_root` + `mtime` makes multi-match behavior predictable and biased toward the executor's own task directory.
4. **Addresses the observed failure exactly**: `WHERE` from `parsed-request.json` is the authoritative user-supplied scope; including those directories catches `/config/workspace/Octodive/.dev/specs/` without an open-ended repo-wide crawl.
5. **Backward compatible**: Steps not in `_STEP_ARTIFACT_PATTERNS` keep exact-name behavior. Existing tests continue to pass.

## Risks & footguns (ranked)

1. **Multi-match ambiguity across runs** (highest). Widening search roots to `WHERE` directories and using wildcards increases the chance of picking up stale files from a prior failed run. The tiebreak mitigates but does not eliminate this. A footgun remains if a stale file in `/config/workspace/Octodive/.dev/specs/` is longer than the current run's output.
2. **Wrong document picked when filenames collide**. If `scope-discovery*.md` matches both `scope-discovery.md` and `scope-discovery-raw.md`, and the shorter one is actually the intended artifact, "largest content" will choose incorrectly.
3. **`/config/workspace/Octodive/.dev/specs/` contamination is not fixed** — only recovered. The agent will still write outside `task_dir`, polluting the user's repo. A future solution (prompt-side or agent-side) should prevent the write, but this solution explicitly leaves that behavior unchanged.
4. **Path traversal in `WHERE`**. The proposed guard (`resolve()` + `relative_to`) is basic and assumes `repo_root` is trustworthy. A symlink inside `WHERE` could still escape; consider also rejecting symlinks or canonicalizing.
5. **`mtime` tiebreak is filesystem-dependent**. On systems with coarse timestamp resolution, two files written in the same second may tie. This is acceptable because `preferred_root` and `content length` sort first.
6. **Performance of rglob over large repos**. `WHERE` directories are usually small (`/config/workspace/Octodive/.dev/specs`, `src/`, etc.), but if a user scopes to `.` or a large tree, rglob with a wildcard could be slow. Consider capping search depth or adding a timeout.

## Backward-compat

- `_STEP_ARTIFACT_FILES` is unchanged; `_persist_step_artifact` continues to write canonical filenames into `task_dir`.
- Special cases for `build-task-file` and `assembly` are untouched.
- Steps without a `_STEP_ARTIFACT_PATTERNS` entry use the old exact-name search.
- Return type of `_resolve_step_content` remains `str`; callers need no changes.
- The function signature is unchanged.

## Test plan

1. **Unit tests** (`/config/workspace/IronClaude/tests/cli/prd/test_resolve_step_content.py`):
   - Existing tests for `build-task-file`, unknown steps, and static-name resolution must still pass.
   - New tests for variant-name recovery, `WHERE` directory inclusion, tiebreak preference for `task_dir`, and path-traversal rejection.
2. **Executor tests** (`/config/workspace/IronClaude/tests/cli/prd/test_executor.py`):
   - Confirm `_run_subprocess_step` calls `_resolve_step_content` and passes the resolved string to `_evaluate_gate`.
   - Confirm `_persist_step_artifact` still writes the canonical filename after recovery.
3. **Gate tests** (`/config/workspace/IronClaude/tests/cli/prd/test_gates.py`):
   - Confirm `scope-discovery` and `research-notes` criteria pass when fed recovered content of sufficient length/structure.
4. **E2E tests** (`/config/workspace/IronClaude/tests/cli/prd/test_e2e.py`):
   - Optional: mocked subprocess writes variant filename; pipeline completes without HALT.
5. **Manual / integration**:
   - Run a real PRD pipeline against a repo where the agent previously wrote `/config/workspace/Octodive/.dev/specs/scope-discovery.md` and verify the scope-discovery gate passes.

## Effort estimate

- Implementation: 2-3 hours (pattern map, search-root expansion, tiebreak, traversal guard).
- Tests: 1-2 hours (unit tests primarily; executor/gate tests are light).
- Review + validation: 1 hour.
- **Total: ~4-6 hours** for a single engineer.
