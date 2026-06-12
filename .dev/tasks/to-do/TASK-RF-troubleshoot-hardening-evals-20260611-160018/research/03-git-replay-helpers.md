# Research 03 — Git-Replay / Integration Mechanics

**Status: Complete**
**Topic:** Hermetically checking out a pre-fix parent commit into an isolated throwaway worktree; the subprocess mock seam; try/finally cleanup; mock-target string.
**Scope:** `src/superclaude/cli/sprint/process.py` (`get_git_diff_context`, `build_task_context`, the module-level `_subprocess` seam) + how `tests/sprint/test_process.py` mocks it; the `git worktree add --detach` pattern; prior-art grep.

All claims below are verified against the live repo at `/config/workspace/IronClaude/` on 2026-06-11 unless marked **Unverified**.

---

## 1. The subprocess mock seam (the pattern the user told us to mirror)

### 1.1 Module-level alias — the seam itself

`src/superclaude/cli/sprint/process.py:17`:

```python
import subprocess as _subprocess
```

This is the **deliberate seam**. The module imports `subprocess` under the private alias `_subprocess` so that every git call inside the module dereferences `_subprocess.run`. Tests patch the alias on the *module object*, never the global `subprocess`.

### 1.2 The producer that uses it

`src/superclaude/cli/sprint/process.py:371-393` — `get_git_diff_context(start_commit)`:

```python
def get_git_diff_context(start_commit: str) -> str:
    try:
        result = _subprocess.run(
            ["git", "diff", "--stat", start_commit],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode != 0 or not result.stdout.strip():
            return ""
        return (
            f"### Git Changes Since Sprint Start\n\n```\n{result.stdout.strip()}\n```"
        )
    except (FileNotFoundError, _subprocess.TimeoutExpired, OSError):
        return ""
```

Key properties to mirror in the backtest harness:
- `capture_output=True, text=True` — string stdout/stderr.
- `timeout=10` — bounded.
- NO `check=True` here; it inspects `result.returncode` manually and returns `""` on non-zero.
- Exception tuple caught: `(FileNotFoundError, _subprocess.TimeoutExpired, OSError)`. `TimeoutExpired` is referenced **through the alias** (`_subprocess.TimeoutExpired`).

### 1.3 The exact patch-target string (load-bearing)

`tests/sprint/test_process.py` patches **`superclaude.cli.sprint.process._subprocess.run`** — the alias attribute on the module, not `subprocess.run` globally. Confirmed at these call sites:

- `tests/sprint/test_process.py:399` — `with patch("superclaude.cli.sprint.process._subprocess.run") as mock_run:` (inside `build_task_context` git-diff test)
- `tests/sprint/test_process.py:434` — success case
- `tests/sprint/test_process.py:446` — empty-diff case
- `tests/sprint/test_process.py:453` — non-zero-exit case
- `tests/sprint/test_process.py:460-463` — `side_effect=FileNotFoundError` (git-not-installed)
- `tests/sprint/test_process.py:471-474` — `side_effect=subprocess.TimeoutExpired(cmd="git", timeout=10)`

**Mock return shape** (`tests/sprint/test_process.py:435-438`):

```python
mock_run.return_value = MagicMock(
    returncode=0,
    stdout=" src/models.py | 15 +++++++++\n 1 file changed\n",
)
```

So a `MagicMock` with `.returncode` and `.stdout` attributes is sufficient — no real `CompletedProcess` needed.

### 1.4 Mirror prescription for the backtest harness

To make the backtest harness unit-testable WITHOUT real git, the harness git helper must:

1. Live in a module that does `import subprocess as _subprocess` at module top (mirror `process.py:17`), and
2. Call `_subprocess.run([...])` (never `subprocess.run` directly), so the unit test patches `<harness.module>._subprocess.run`.

The *seam shape* is fixed: a module-level `_subprocess` alias + `.run` attribute patch. The dotted-module path of the helper (whether under `src/superclaude/...` or `tests.troubleshoot.backtest...`) is an impl decision deferred to R6.

---

## 2. Prior art: existing git-via-subprocess helper (`_git` in drift.py)

`src/superclaude/cli/sprint/resume/drift.py:262-297` is the closest existing pattern and a second model to mirror. It uses `git -C <dir>` (directory targeting) + `check=True` + a tuple-catch:

```python
import subprocess
cwd = str(phase_file.parent)

def _git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-C", cwd, *args],
        capture_output=True,
        check=True,
        text=True,
    )

try:
    _git("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}")
    _git("ls-files", "--error-unmatch", str(phase_file))
    diff = _git("diff", "--ignore-all-space", "--stat", "@{upstream}", "--", str(phase_file))
except (OSError, subprocess.SubprocessError):
    return assessment  # git unavailable / detached / no upstream / untracked
```

Reusable lessons for the replay harness:
- **`git -C <dir>`** is the idiomatic way to run git against a specific tree (the scratch worktree) without `os.chdir`. Use `git -C <scratch_worktree> rev-parse HEAD` to assert the checkout.
- A small `_git(*args)` closure with `check=True` + catching `subprocess.SubprocessError` (base class of `CalledProcessError` and `TimeoutExpired`) is the clean control-flow shape.
- `drift.py` imports `subprocess` *inside the method* (line 262), NOT aliased at module top — that style is NOT unit-test-mockable via a module attribute. **For the backtest harness, prefer the `process.py` module-top `import subprocess as _subprocess` seam** (Section 1) so unit tests can patch it.

### 2.1 Grep results — is there any existing `git worktree` subprocess code?

`grep -rn "worktree" src/superclaude/` → **NO code adds/removes git worktrees via subprocess.** All hits are docs/skills or worktree-*aware path resolution* (recommend/prompts.py, cache.py). Notable:
- `src/superclaude/cli/roadmap/convergence.py:393` — comment "Replaces git worktrees (BF-4: checkers don't need git repo)." Roadmap deliberately moved *away* from worktrees.
- `src/superclaude/pr_submit/recovery.py:115` — references a "worktree edit" but in the PR-submit sense, not `git worktree add`.

`grep "rev-parse|merge-base|--detach"`:
- `--detach` hits are all **`swarm run --detached`** (tmux flag in `cli/swarm/commands.py`), unrelated to `git worktree --detach`.
- `git rev-parse` appears only in hook shell scripts (`freshness-*.sh`) and drift.py.
- **No `merge-base` anywhere in `src/`.**

**Conclusion:** the replay harness introduces a NEW pattern (`git worktree add --detach`); there is no in-repo Python helper to import. Mirror the *subprocess seam shape* from `process.py`, not an existing worktree helper.

---

## 3. Verified `git worktree` roundtrip (real-git mechanics)

Executed live from `/config/workspace/IronClaude` (main checkout) on 2026-06-11:

```
SCRATCH=$(mktemp -d)
git worktree add --detach "$SCRATCH/wt" 94d5baa0
  → "Preparing worktree (detached HEAD 94d5baa0)" ... "HEAD is now at 94d5baa0 ..."
git -C "$SCRATCH/wt" rev-parse HEAD   → 94d5baa05f6319b8ff6f2e1db8e8b7737465daaf
git rev-parse HEAD                    → 20693bb8... (LIVE TREE UNCHANGED ✓)
git worktree remove --force "$SCRATCH/wt"  → removed-ok
git worktree prune
```

Verified facts:
- `git worktree add --detach <path> <sha>` checks out a **full tree** (13,612 files here) in detached-HEAD mode; takes a few seconds.
- The live working tree's HEAD is **NOT mutated** — true isolation.
- `git worktree remove --force <path>` succeeds even with the checkout present; `--force` is needed because the worktree is non-empty / detached.
- `git worktree prune` cleans any dangling admin entries (belt-and-suspenders after `rm -rf`).

### 3.1 Argument-order caveat

The working form is `git worktree add [--detach] <path> [<commit-ish>]` — **path first, then commit-ish**. (**Verified** by the successful run above.)

---

## 4. Commit/parent verification — all 5 escapes resolvable

The task lists, per escape, a SHA. All resolve to commits AND have resolvable `^` parents:

| Escape | Given SHA | `<sha>^{commit}` resolves | `<sha>^` (its parent) resolves |
|---|---|---|---|
| E1 | `94d5baa0` | `94d5baa05f63…` ✓ | `ac80f1763895…` ✓ |
| E2 | `10723863` | `10723863389b…` ✓ | `d878bc6d04f9…` ✓ |
| E3 | `e97aa4fd` | `e97aa4fd2a9d…` ✓ | `10723863389b…` ✓ |
| E4 | `1b0264f1` | `1b0264f13eda…` ✓ | `eb9a2633bfc4…` ✓ |
| E5 | `d878bc6d` | `d878bc6d04f9…` ✓ | `7601ad2548e2…` ✓ |

**Semantic note (flag for R5/R6):** The task frames these as "E1 **parent** 94d5baa0…" while also saying "replay against **pre-fix commits**" and "resolve each escape's pre-fix parent (`<fix-sha>^`)". Two readings:
- (a) The listed SHA is **the fix commit**; replay against `<sha>^`; OR
- (b) The listed SHA **is already the pre-fix parent**; check it out directly.

Commit subjects suggest (a): `94d5baa0` = "fix(sprint): recovery deliverable-stranding…(#150)" — that IS a fix commit, so its *pre-fix* state is `94d5baa0^`. R5 (replay semantics) must pin this down per-escape. The git mechanics work identically either way — the harness needs the correct commit-ish string; `git rev-parse "<sha>^"` is the resolver. (Cross-check the prior commit list in session context: `1b0264f1` and `d878bc6d` both appear as recent `fix(...)` commits, reinforcing reading (a).)

---

## 5. The reusable git-replay helper pattern (prescription)

A single context-manager-style helper is the cleanest shape. Mirror the `process.py` seam (`import subprocess as _subprocess`), `git -C` targeting from drift.py, and a guaranteed `try/finally` teardown.

### 5.1 Recommended shape (contextmanager + try/finally)

```python
import subprocess as _subprocess          # the mock seam (mirror process.py:17)
import tempfile
import shutil
from contextlib import contextmanager
from pathlib import Path


def _resolve_prefix_parent(fix_sha: str) -> str:
    """Resolve the pre-fix parent commit-ish ('<fix-sha>^') to a full SHA."""
    out = _subprocess.run(
        ["git", "rev-parse", "--verify", f"{fix_sha}^"],
        capture_output=True, text=True, timeout=10, check=True,
    )
    return out.stdout.strip()


@contextmanager
def checkout_worktree(commitish: str, *, scratch_root: Path | None = None):
    """Add a detached throwaway worktree at `commitish`, yield its path,
    and guarantee removal (even on exception)."""
    base = Path(tempfile.mkdtemp(prefix="backtest-wt-", dir=scratch_root))
    wt = base / "wt"
    try:
        _subprocess.run(
            ["git", "worktree", "add", "--detach", str(wt), commitish],
            capture_output=True, text=True, timeout=120, check=True,
        )
        yield wt
    finally:
        # Force-remove the worktree; never let teardown raise.
        _subprocess.run(
            ["git", "worktree", "remove", "--force", str(wt)],
            capture_output=True, text=True, timeout=60, check=False,
        )
        shutil.rmtree(base, ignore_errors=True)
        _subprocess.run(
            ["git", "worktree", "prune"],
            capture_output=True, text=True, timeout=30, check=False,
        )
```

Usage in a backtest assertion:

```python
parent = _resolve_prefix_parent("94d5baa0")        # → ac80f176…
with checkout_worktree(parent) as wt:
    head = _subprocess.run(
        ["git", "-C", str(wt), "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    assert head == parent           # sanity: checkout landed on pre-fix state
    # ... OLD=MISS assertion against the checkout at `wt` ...
```

### 5.2 try/finally guarantees (the critical contract)

- **`add`** uses `check=True` + `timeout=120` (full-tree checkout is slow — §3 measured 13k files).
- **Teardown is in `finally`** and uses `check=False` so a failed `remove` never masks the test's real failure; `shutil.rmtree(..., ignore_errors=True)` + `git worktree prune` are belt-and-suspenders. This satisfies the task's "cleanup guaranteed even on failure (try/finally)" requirement.
- Removal order: `git worktree remove --force` FIRST (lets git update its admin metadata), THEN `rmtree` the temp parent, THEN `prune` to drop any stale admin record.

### 5.3 Scratch-root choice (tmp_path vs dedicated)

| Option | Where | Verdict |
|---|---|---|
| pytest `tmp_path` fixture | `/tmp/pytest-of-*/…` | **Best for the helper signature**: pass `scratch_root=tmp_path` so pytest owns lifecycle + auto-cleans. BUT the worktree admin entry lives in the repo's `.git/worktrees/`, NOT in `tmp_path`, so `git worktree remove`/`prune` is still mandatory even if pytest nukes `tmp_path`. |
| `tempfile.mkdtemp()` | system `$TMPDIR` | Default when no `scratch_root`; fine for the integration variant run outside pytest. |
| Dedicated dir under repo (e.g. `.dev/backtest-scratch/`) | inside repo | **Avoid** — risks being picked up by globs / git status / nested-worktree confusion. |

**Recommendation:** helper takes optional `scratch_root: Path | None`; integration test passes `tmp_path`; helper still ALWAYS issues `git worktree remove --force` + `prune` because the worktree bookkeeping lives in `.git/worktrees/<name>/` (the shared common-dir), not under `tmp_path`. Verified: `git rev-parse --git-common-dir` → `.git`, shared across all worktrees.

### 5.4 Worktree-from-a-worktree note (freshness)

The cwd at execution time may itself be a worktree (`.claude/worktrees/<name>/`). `git worktree add` from inside any linked worktree still registers the new worktree against the **shared common dir** (`git rev-parse --git-common-dir` resolves to the repo's real `.git`). So the helper works whether invoked from the main checkout or a linked worktree — no special-casing needed. The 5 target commits live in the shared object store, reachable from any worktree. (**Verified**: roundtrip in §3 ran from the main checkout; common-dir is shared by design.)

---

## 6. Unit-test (mocked) vs integration (real-git) variants

### 6.1 Unit variant — no real git

Patch `<harness_module>._subprocess.run` exactly as `tests/sprint/test_process.py:399/434` does. Drive `mock_run.return_value`/`side_effect` to simulate:
- `worktree add` success → `MagicMock(returncode=0, stdout="…")`.
- `rev-parse HEAD` → the expected parent SHA.
- failure paths (`side_effect=subprocess.CalledProcessError(...)` / `FileNotFoundError`) to assert the `finally` teardown still fires.

Keeps the harness's control-flow (resolve → add → assert → remove) testable in milliseconds with zero git side effects. `MagicMock(returncode=…, stdout=…)` from §1.3 is the proven mock contract.

### 6.2 Integration variant — real git against the actual repo

The 5 commits are confirmed present (§4), so an integration test (mark `@pytest.mark.integration`; auto-applied for tests under an `/integration/` path per CLAUDE.md "Auto-markers") can:
1. `git rev-parse --verify <sha>^` to get the pre-fix parent,
2. real `git worktree add --detach`,
3. run the OLD-protocol assertion against the checkout (expect MISS),
4. real `git worktree remove --force` in `finally`.

Guard it to skip when not in a git repo or commits absent: module-level `pytest.mark.skipif` checking `git rev-parse --is-inside-work-tree` (pattern at `src/superclaude/skills/sc-cleanup-audit-protocol/scripts/repo-inventory.sh:62`) + a `git cat-file -e <sha>` existence probe keeps CI green on shallow clones. **Flag for R2 (pytest conventions):** if CI does shallow `fetch-depth: 1`, these 5 commits won't be present and the integration test must `skip`, not `fail`. (**Unverified** — CI checkout depth not inspected here; R2/R6 should confirm.)

### 6.3 Performance note

Each `git worktree add` does a full working-tree checkout (~13.6k files measured, a few seconds each). Five escapes × full checkouts ≈ tens of seconds of real I/O. Mitigations the impl may consider (defer to R6):
- `git worktree add --no-checkout --detach` then `git -C <wt> checkout <pathspec>` to materialize only needed files — **Unverified** that `--no-checkout` suffices for the OLD-protocol assertions (depends on what R5 says the assertion reads).
- Reuse a single worktree and `git -C <wt> checkout <sha>` between escapes — trades isolation for speed.
- Keep the integration suite behind a marker so the default `make test` fast path can exclude it.

---

## 7. Summary / hand-off facts

1. **Mock seam:** `import subprocess as _subprocess` at module top (`process.py:17`); patch target = dotted-module path + `._subprocess.run`. Proven at `tests/sprint/test_process.py:399,434,446,453,460,471`. Mock return = `MagicMock(returncode=…, stdout=…)`.
2. **No existing worktree Python helper** — grep confirms `src/` has zero `git worktree add` subprocess calls; `merge-base` absent. New pattern; mirror the `process.py` seam + drift.py `git -C` style.
3. **Worktree roundtrip verified live:** `git worktree add --detach <path> <commitish>` → assert via `git -C <wt> rev-parse HEAD` → `git worktree remove --force <path>` → `git worktree prune`. Live HEAD untouched.
4. **All 5 escapes resolvable:** both `<sha>` and `<sha>^` resolve for E1–E5 (table §4). **Open question for R5:** is the listed SHA the fix commit (replay `<sha>^`) or already the parent (replay `<sha>`)? Subjects ("fix(sprint)…") favor replay `<sha>^`.
5. **try/finally teardown contract:** `add` with `check=True`; teardown in `finally` with `check=False` + `rmtree(ignore_errors=True)` + `prune` — cleanup guaranteed even on assertion failure (§5.1/5.2).
6. **Scratch root:** parametrize `scratch_root: Path | None`; integration test passes `tmp_path`; admin records still require `worktree remove`+`prune` because they live in the shared `.git/worktrees/` common-dir, not under `tmp_path`.
7. **Unit vs integration:** unit patches `_subprocess.run` (ms, no git); integration uses real git, must `skipif` not in a work-tree / commits absent — **verify CI fetch-depth (R2)**.

### Key file:line citations
- `src/superclaude/cli/sprint/process.py:17` — `import subprocess as _subprocess` (the seam)
- `src/superclaude/cli/sprint/process.py:371-393` — `get_git_diff_context` (mirror producer)
- `src/superclaude/cli/sprint/process.py:381-386` — the `_subprocess.run([...], capture_output, text, timeout)` call
- `src/superclaude/cli/sprint/process.py:392` — exception tuple `(FileNotFoundError, _subprocess.TimeoutExpired, OSError)`
- `tests/sprint/test_process.py:399,434,446,453,460-463,471-474` — patch-target + mock shapes + side_effect patterns
- `tests/sprint/test_process.py:435-438` — `MagicMock(returncode=0, stdout=…)` mock-return contract
- `src/superclaude/cli/sprint/resume/drift.py:262-297` — `_git()` `git -C` prior-art (check=True, SubprocessError catch)
- `src/superclaude/cli/roadmap/convergence.py:393` — repo deliberately moved away from worktrees (context)
- `src/superclaude/skills/sc-cleanup-audit-protocol/scripts/repo-inventory.sh:62` — `git rev-parse --is-inside-work-tree` skip-guard pattern
