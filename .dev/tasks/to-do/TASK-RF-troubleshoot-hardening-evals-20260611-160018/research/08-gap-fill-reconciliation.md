# 08 — Gap-Fill Reconciliation Note

**Status: Complete**

Authoritative reconciliation closing the 3 research-gate gaps with hard git evidence. All git output below was produced by running the commands against `/config/workspace/IronClaude/` (full-depth local clone, full history present). Where research files 03 and 05 contradict, **this note is the tie-breaker.**

Evidence-collection environment: cwd was the `ReflectGateWiring` worktree; `git rev-parse --git-common-dir` → `.git` and history/objects are shared across all worktrees of the repo, so the SHA resolutions below are identical from any worktree.

---

## G1 (IMPORTANT) — Authoritative checkout-target pinning

### The contradiction being resolved

- **Research file 03 (git-replay)** framed the replay as: *"the listed SHA is the FIX commit, check out `<sha>^`"* and hardcoded the example `_resolve_prefix_parent("94d5baa0") → ac80f176`.
- **Research file 05 (replay-targets)** says: the harness checks out each escape's **PRE-FIX PARENT SHA DIRECTLY (no `^`)**.

**File 05 is CORRECT. File 03 is WRONG on the data shape** (it conflates "the stored value is the fix sha" with "the stored value is the parent sha"). File 03's worked example `94d5baa0 → ac80f176` is the **smoking gun of the bug**: `94d5baa0` is already a *parent* (it is E1's checkout target), so resolving `94d5baa0^` double-decrements to `ac80f176` and replays one commit too early.

### Ground-truth evidence

Command:
```bash
for fix in 7601ad25 e97aa4fd eb9a2633 b97c9960 10723863; do
  parent=$(git rev-parse --short "${fix}^")
  subj=$(git log -1 --format='%s' "$fix")
  echo "FIX=$fix  PARENT(^)=$parent  SUBJECT=$subj"
done
```

Verbatim output:
```
FIX=7601ad25  PARENT(^)=94d5baa0  SUBJECT=fix(prd): deliver specs/refs inline instead of via cloud-only --file flag (#151)
FIX=e97aa4fd  PARENT(^)=10723863  SUBJECT=fix(prd): exempt sequential completion phase from parallel-instructions gate (#154)
FIX=eb9a2633  PARENT(^)=e97aa4fd  SUBJECT=fix(prd): make parallel-instructions gate advisory (warn, don't halt) (#155)
FIX=b97c9960  PARENT(^)=1b0264f1  SUBJECT=fix(prd): honor advisory checks in the executor's _evaluate_gate (live PRD path)
FIX=10723863  PARENT(^)=d878bc6d  SUBJECT=fix(task-builder): base POST-reflect --diff on merge-base working-tree, not start_commit (#153)
```

Supporting checks:
```
# double-decrement hazard demonstrated
git rev-parse --short '94d5baa0^'   → ac80f176     (this is the WRONG target — one commit too early)

# E4 fix is unmerged
git merge-base --is-ancestor b97c9960 master → NOT merged into master (UNMERGED)

# every checkout target is a real, resolvable commit
94d5baa0 -> commit   10723863 -> commit   e97aa4fd -> commit   1b0264f1 -> commit   d878bc6d -> commit
```

### THE single authoritative per-escape table

| Escape | Wave | FIX sha    | `git rev-parse --short <fix>^` → **PRE-FIX PARENT (checkout target)** | Fix subject |
|--------|------|------------|----------------------------------------------------------------------|-------------|
| **E1** | H1   | `7601ad25` | **`94d5baa0`**                                                        | fix(prd): deliver specs/refs inline instead of via cloud-only --file flag (#151) |
| **E2** | H3   | `e97aa4fd` | **`10723863`**                                                        | fix(prd): exempt sequential completion phase from parallel-instructions gate (#154) |
| **E3** | H3   | `eb9a2633` | **`e97aa4fd`**                                                        | fix(prd): make parallel-instructions gate advisory (warn, don't halt) (#155) |
| **E4** | H2   | `b97c9960` (**UNMERGED**) | **`1b0264f1`**                                          | fix(prd): honor advisory checks in the executor's _evaluate_gate (live PRD path) |
| **E5** | H4   | `10723863` | **`d878bc6d`**                                                        | fix(task-builder): base POST-reflect --diff on merge-base working-tree, not start_commit (#153) |

This **confirms the known mapping in the task brief exactly** (E1→94d5baa0, E2→10723863, E3→e97aa4fd, E4→1b0264f1, E5→d878bc6d).

**Chain note (cross-check):** E5's fix `10723863` *is* E2's checkout parent, and E2's fix `e97aa4fd` *is* E3's checkout parent. The escapes are interleaved on the same linear history; this is why per-escape parent pinning (not a single global `^`) is required.

### EXPLICIT RULE (state prominently in the harness)

> **The harness MUST store the PRE-FIX PARENT sha per escape and check it out with NO `^` suffix.**
>
> Applying `^` to a parent sha (e.g. `94d5baa0^` = `ac80f176`) **double-decrements** and replays one commit too early — producing a **green-but-meaningless backtest** (the escape's bug isn't even present at `ac80f176`).
>
> The `<sha>^` resolution is correct **only if the stored value is the FIX sha**. To remove all ambiguity, **store the already-resolved PARENT sha directly** (resolve `<fix>^` once, at table-authoring time, and pin the result) so the runtime checkout is a bare `git checkout <prefix_parent_sha>` with zero `^` arithmetic.

### Recommended data shape (per escape)

```python
# Pinned at authoring time — runtime does NOT apply `^`.
REPLAY_ESCAPES = [
    # escape_id, fix_sha,     prefix_parent_sha (CHECKOUT TARGET), wave, §8.3 scenario
    ("E1", "7601ad25", "94d5baa0", "H1", "<§8.3 scenario ref for E1>"),
    ("E2", "e97aa4fd", "10723863", "H3", "<§8.3 scenario ref for E2>"),
    ("E3", "eb9a2633", "e97aa4fd", "H3", "<§8.3 scenario ref for E3>"),
    ("E4", "b97c9960", "1b0264f1", "H2", "<§8.3 scenario ref for E4>"),  # fix UNMERGED
    ("E5", "10723863", "d878bc6d", "H4", "<§8.3 scenario ref for E5>"),
]
# Runtime: git checkout <prefix_parent_sha>   ← no caret, ever.
```

Fields: `escape_id`, `fix_sha` (provenance/audit only), `prefix_parent_sha` (**the bare checkout target**), `wave`, `§8.3 scenario`.

---

## G2 (IMPORTANT) — CI shallow-clone skip-guard

### (a) Actual fetch depth used by the test CI job(s)

The pytest suite runs in the **`test`** job of `.github/workflows/test.yml`:

- `.github/workflows/test.yml:11` — `test:` job
- `.github/workflows/test.yml:20-21` — `- name: Checkout code` / `uses: actions/checkout@v4` — **NO `fetch-depth` key**
- `.github/workflows/test.yml:54-56` — `Run tests` → `pytest -v --tb=short --color=yes`
- `.github/workflows/test.yml:58-61` — `Run tests with coverage` → `pytest --cov=...` (Python 3.10 only)

`grep -rn 'fetch-depth' .github/workflows/` shows `fetch-depth: 0` is set **only** in:
- `contract3-generator-constraint-lint.yml:32`
- `publish-pypi.yml:37`
- `boundary-guard.yml:43`

**None of those run the integration replay test.** Every checkout in `test.yml` (lines 21, 85, 115, 145, 175, 201) omits `fetch-depth`.

**Conclusion:** `actions/checkout@v4` with no `fetch-depth` defaults to **`fetch-depth: 1` — a shallow single-commit clone.** On CI, the 5 replay parent SHAs (`94d5baa0`, `10723863`, `e97aa4fd`, `1b0264f1`, `d878bc6d`) are **absent** from local history. The replay test **MUST skip, not fail.** Locally (full clone) all 5 are present — verified: `git cat-file -e '94d5baa0^{commit}'` → present.

### (b) Exact skip-guard predicate (copy-pasteable pytest)

```python
import subprocess
import pytest

# Pinned PRE-FIX PARENT checkout targets (see G1 table). NOT fix shas.
REPLAY_CHECKOUT_TARGETS = {
    "E1": "94d5baa0",
    "E2": "10723863",
    "E3": "e97aa4fd",
    "E4": "1b0264f1",
    "E5": "d878bc6d",
}


def _missing_replay_shas():
    """Return [(escape_id, sha), ...] for any checkout target absent from local history.

    `git cat-file -e <sha>^{commit}` exits 0 iff the object exists locally AND is a
    commit. On a shallow CI clone (actions/checkout@v4 default fetch-depth: 1) these
    historical commits are not fetched, so the probe exits non-zero.
    """
    missing = []
    for escape_id, sha in REPLAY_CHECKOUT_TARGETS.items():
        proc = subprocess.run(
            ["git", "cat-file", "-e", f"{sha}^{{commit}}"],
            capture_output=True,
        )
        if proc.returncode != 0:
            missing.append((escape_id, sha))
    return missing


def _not_a_git_worktree():
    proc = subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"],
        capture_output=True, text=True,
    )
    return proc.returncode != 0 or proc.stdout.strip() != "true"


# Module-level guard: applied to the whole replay module.
_GIT_UNAVAILABLE = _not_a_git_worktree()
_MISSING = [] if _GIT_UNAVAILABLE else _missing_replay_shas()

pytestmark = pytest.mark.skipif(
    _GIT_UNAVAILABLE or bool(_MISSING),
    reason=(
        "Not inside a git work-tree — replay requires repo history."
        if _GIT_UNAVAILABLE
        else (
            "Integration replay requires a full-depth clone; the following pre-fix "
            "parent commit(s) are absent from local history (shallow CI clone, "
            f"actions/checkout@v4 default fetch-depth: 1): {_MISSING}. "
            "Set `fetch-depth: 0` on the checkout step to enable."
        )
    ),
)
```

**Notes:**
- The `^{commit}` peel in `cat-file -e` is deliberate: it asserts the object exists **and** is a commit (a bare `git cat-file -e <sha>` would also pass for a loose blob/tree of the same prefix). The `{{` / `}}` are f-string-escaped literal braces.
- **`git rev-parse --is-inside-work-tree` IS needed** as a first-line guard: it prevents the suite from erroring (vs. cleanly skipping) when pytest is run outside a git checkout (e.g. an unpacked sdist, a Docker layer with no `.git`). Without it the `cat-file` probes would surface git's "not a git repository" stderr instead of a clean skip.
- Cited workflow evidence: `.github/workflows/test.yml:21` (no `fetch-depth` on the pytest job's checkout) vs. `.github/workflows/boundary-guard.yml:43` / `publish-pypi.yml:37` / `contract3-generator-constraint-lint.yml:32` (the only `fetch-depth: 0` jobs, none of which run the replay).

---

## G3 (MINOR) — No-leaked-worktree post-condition

### Mechanism

1. Capture `git worktree list --porcelain` **baseline** before the replay.
2. Run the replay inside **try/finally**; the `finally` block force-removes the temp worktree and **prunes** the admin records: `git worktree remove --force <dir>` then `git worktree prune`.
3. Assert the post-replay `git worktree list --porcelain` **equals baseline** (no leaked stanzas), proving teardown fired even when the body raised.

### Why `prune` is mandatory (evidence)

```
git rev-parse --git-common-dir → .git
```

The `.git/worktrees/<name>/` administrative records live in the **common-dir**, which is **shared across all worktrees of the repo** and is **independent of where the worktree checkout directory lives**. Even when the checkout dir is under pytest's `tmp_path` (auto-deleted at test exit), deleting that directory does **not** remove the `.git/worktrees/<name>/` admin stanza — git would still list it as a (now-broken) worktree. `git worktree prune` is the only thing that reaps those stale admin records. Hence: **`remove --force` to detach + delete the checkout, then `prune` to clear the admin record — both, always, in `finally`.**

The live `git worktree list --porcelain` output confirms the stanza shape the assertion compares: blank-line-separated stanzas of `worktree <path>` / `HEAD <sha>` / `branch <ref>` (or `detached`).

### Copy-pasteable assertion shape

```python
import subprocess
import pytest


def _worktree_list_porcelain():
    return subprocess.run(
        ["git", "worktree", "list", "--porcelain"],
        capture_output=True, text=True, check=True,
    ).stdout


def test_replay_leaves_no_leaked_worktree(tmp_path):
    baseline = _worktree_list_porcelain()
    wt_dir = tmp_path / "replay-wt"

    try:
        subprocess.run(
            ["git", "worktree", "add", "--detach", str(wt_dir), "94d5baa0"],
            check=True, capture_output=True, text=True,
        )
        # ... run the replay assertions against wt_dir here ...
        # (an AssertionError raised in this block must NOT leak the worktree)
    finally:
        subprocess.run(
            ["git", "worktree", "remove", "--force", str(wt_dir)],
            capture_output=True, text=True,
        )
        # MANDATORY: reap the .git/worktrees/<name>/ admin record in the common-dir.
        subprocess.run(["git", "worktree", "prune"], capture_output=True, text=True)

    after = _worktree_list_porcelain()
    assert after == baseline, (
        "Leaked git worktree after replay — teardown did not fully fire.\n"
        f"baseline:\n{baseline}\nafter:\n{after}"
    )
```

The `baseline == after` equality (rather than a substring/count heuristic) is what proves teardown fired on the assertion-failure path: any leaked checkout *or* any leaked admin stanza changes the porcelain output and trips the assertion.

---

## Summary of resolutions

- **G1:** File 05 is authoritative; File 03's `<fix>^` framing + `94d5baa0→ac80f176` example is the double-decrement bug. Harness stores the **pre-fix PARENT sha** per escape and checks it out with **NO `^`**. Confirmed table: E1→`94d5baa0`, E2→`10723863`, E3→`e97aa4fd`, E4→`1b0264f1` (fix UNMERGED), E5→`d878bc6d`.
- **G2:** The pytest `test` job (`.github/workflows/test.yml:21`) uses `actions/checkout@v4` with **no `fetch-depth`** → shallow `fetch-depth: 1`; replay commits absent on CI → MUST skip. Skip-guard = module-level `pytest.mark.skipif` probing `git cat-file -e <parent>^{commit}` per escape + `git rev-parse --is-inside-work-tree` first-line guard.
- **G3:** Post-condition = capture `git worktree list --porcelain` baseline, replay in try/finally with `git worktree remove --force` + `git worktree prune`, assert `after == baseline`. `prune` mandatory because admin records live in the common-dir (`git rev-parse --git-common-dir → .git`), unaffected by tmp_path cleanup.
