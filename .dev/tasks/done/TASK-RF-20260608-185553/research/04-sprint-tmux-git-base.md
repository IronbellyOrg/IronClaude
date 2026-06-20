# Research: Sprint tmux + git-base idioms
**Status:** Complete
**Date:** 2026-06-08

**Scope:** `src/superclaude/cli/sprint/tmux.py` (detached-window + sentinel idiom for the
wrapper's `--tmux` opt-in, spec §5) + the `<BASE>..HEAD` git-base resolution idiom for FR-3.
Wrapper default is foreground-blocking (no window); `--tmux` is opt-in reusing sprint's pattern.

**TL;DR headline finding:** `git merge-base HEAD <integration>` does **NOT exist in Python
source anywhere in the repo** — it lives only as prose in `task-builder/SKILL.md:1996`. The
wrapper's FR-3 base-resolution chain (`start_commit` → `merge-base HEAD <integration>` →
fail `base-unresolved`) must be **written fresh** in the wrapper; there is no reusable
`merge-base` helper to import. The closest precedent is `drift.py`'s `_git()` subprocess
shape (which uses `@{upstream}`, not a named integration branch). The tmux idiom in
`tmux.py` IS directly reusable (adapt session-name prefix + sentinel filename).

---

## 1. tmux detached-window + sentinel idiom (`cli/sprint/tmux.py`)

The single reusable launch function is `launch_in_tmux(config)` at
`src/superclaude/cli/sprint/tmux.py:81-173`. It implements the exact
**detached-session → attach (operator watches live) → sentinel-exit-code readback** pattern
the spec §5 calls for under `--tmux`.

### 1a. Availability guard + session naming

```python
# tmux.py:50-55
def is_tmux_available() -> bool:
    """Check if tmux is installed and we are not already inside tmux."""
    if shutil.which("tmux") is None:
        return False
    return "TMUX" not in os.environ   # already-inside-tmux → unavailable
```

```python
# tmux.py:58-61
def session_name(release_dir: Path) -> str:
    """Deterministic session name from release directory."""
    h = hashlib.sha1(str(release_dir.resolve()).encode()).hexdigest()[:8]
    return f"sc-sprint-{h}"
```

- **Session naming** = `sc-sprint-` + first 8 hex of `sha1(resolve(release_dir))`
  (`tmux.py:60-61`). Deterministic per release dir → re-attach + collision-avoidance.
  For the wrapper, adapt the prefix to e.g. `sc-reflect-` and hash the pinned `--output`
  dir (FR-4) instead of `release_dir`.
- `find_running_session()` (`tmux.py:64-78`) scans `tmux list-sessions -F '#{session_name}'`
  for any line `startswith("sc-sprint-")` — the prefix is the discovery key.

### 1b. Detached launch — how the command string is passed

The command is **NOT** passed as a shell string; it's an argv list spliced directly into the
`tmux new-session` argv (`tmux.py:94-108`):

```python
# tmux.py:91-108
sprint_cmd = _build_foreground_command(config)   # returns list[str]
subprocess.run(
    [
        "tmux", "new-session",
        "-d",                # detached  ← the key flag
        "-s", name,          # session name
        "-x", "120", "-y", "40",   # default geometry
        *sprint_cmd,         # the inner command, argv-spliced
    ],
    check=True,
)
```

`_build_foreground_command` (`tmux.py:176-210`) builds the **inner blocking command** that
runs inside the window — crucially it re-invokes the SAME CLI with `--no-tmux` so the inner
process runs foreground and writes the sentinel:

```python
# tmux.py:178-190
cmd = [
    "superclaude", "sprint", "run",
    str(config.index_path),
    "--no-tmux",                       # inner = foreground, writes sentinel
    "--start", str(config.start_phase),
    "--max-turns", str(config.max_turns),
    "--permission-flag", config.permission_flag,
]
# ... plus --state-dir forwarded so sentinel path matches (see 1d) ...
```

**Idiom for the wrapper:** the `--tmux` path launches `superclaude reflect run <task> --no-tmux ...`
inside the detached window; the `--no-tmux` (foreground-blocking) path is the default and is
what writes the sentinel. This mirrors the spec §5 exactly: foreground-blocking is the
primitive, `--tmux` wraps it.

### 1c. Attach (operator watches live) → then recover exit code

```python
# tmux.py:162-173
# Attach — blocks until the user detaches or the session ends
subprocess.run(["tmux", "attach-session", "-t", name])

# Read the exit code written by execute_sprint() inside the tmux session
sentinel = config.state_dir / ".sprint-exitcode"
exit_code = 0
try:
    exit_code = int(sentinel.read_text().strip())
except (OSError, ValueError):
    pass  # session may have been killed externally; assume success
if exit_code != 0:
    raise SystemExit(exit_code)
```

The **watch-live → recover** flow is exactly these 12 lines:
1. `tmux attach-session -t <name>` blocks (operator sees the live TUI/output);
2. when the operator detaches OR the inner process exits, `attach-session` returns;
3. the outer process reads `<state_dir>/.sprint-exitcode`, the sentinel file the inner
   `--no-tmux` process wrote;
4. non-zero sentinel → `raise SystemExit(exit_code)` propagates the inner rc to the caller.

**Notable failure-tolerance:** a missing/garbage sentinel is swallowed → **assumes success
(exit 0)** (`tmux.py:170-171`). This is a fail-OPEN default. For the reflect wrapper this is
**the wrong posture** (spec is fail-CLOSED, FR-8/NFR-4): the wrapper must treat a
missing/unreadable `.reflect-exitcode` sentinel as `blocked` (exit 2), NOT success. This is
a **required adaptation**, not a verbatim reuse.

### 1d. Sentinel path coupling — the desync footgun (verified)

`tmux.py:196-202` forwards `--state-dir` into the inner command **specifically** so the inner
writer and outer reader agree on the sentinel path:

```python
# tmux.py:196-202
cmd.extend(["--state-dir", str(config.state_dir)])
# Forward state_dir so the inner --no-tmux process writes its
# .sprint-exitcode sentinel to the SAME path the outer (this) process
# reads from at line 166. Without this, an outer --state-dir override
# (or env-derived non-default) silently desyncs from the inner default
# and exit-code propagation breaks.
```

**Lesson for the wrapper:** if `--tmux` re-invokes `reflect run ... --no-tmux`, it MUST pass
the same output/state dir to the inner call so the inner process writes `.reflect-exitcode`
where the outer one reads it. The spec already pins `--output` (FR-4), so reuse that pinned
dir as the sentinel location and forward it to the inner invocation.

### 1e. Where the sentinel is WRITTEN

`launch_in_tmux` only READS the sentinel (`tmux.py:166`). The WRITE happens inside
`execute_sprint()` (per the comment at `tmux.py:165`) — i.e. the inner `--no-tmux` foreground
run owns writing `.sprint-exitcode`. The writer is NOT in tmux.py.

The writer is `_write_exit_sentinel(config, exitcode)` at
`src/superclaude/cli/sprint/executor.py:2252-2264`, called from the foreground execute path
at `executor.py:2244-2249`:

```python
# executor.py:2244-2249
_exitcode = 0 if sprint_result.outcome == SprintOutcome.SUCCESS else 1
_write_exit_sentinel(config, _exitcode)
if _exitcode != 0:
    raise SystemExit(_exitcode)
```

```python
# executor.py:2252-2264
def _write_exit_sentinel(config: SprintConfig, exitcode: int) -> None:
    """Write the .sprint-exitcode sentinel to config.state_dir for tmux IPC."""
    try:
        state_dir = config.state_dir
        state_dir.mkdir(parents=True, exist_ok=True)
        (state_dir / ".sprint-exitcode").write_text(str(exitcode))
    except OSError:
        pass   # best-effort; swallow so write failure doesn't mask real exit code
```

**Full sentinel cycle (verified end-to-end):**
1. Foreground run finishes → `_write_exit_sentinel` writes `str(exitcode)` to
   `<state_dir>/.sprint-exitcode` (`executor.py:2262`), then `raise SystemExit(_exitcode)`.
2. The outer `--tmux` parent's `attach-session` returns → reads the same file
   (`tmux.py:166-169`) → `raise SystemExit` on non-zero.

**State-dir semantics (verified):** `--state-dir` defaults to `$SPRINT_STATE_DIR` or
`.dev/sprint-state/<tasklist-id>/` (`commands.py:188`; default resolved in
`SprintConfig.__post_init__`, `models.py:572`). It is a **non-tracked transient** path —
never the tracked archive dir. The wrapper's `.reflect-exitcode` should likewise live under a
transient/output path (the pinned `--output` dir from FR-4 is the natural home).

### 1f. Cleanup on partial-setup failure

`launch_in_tmux` wraps all post-`new-session` pane setup in `try/except` and kills the partial
session before re-raising (`tmux.py:157-160`):

```python
# tmux.py:157-160
except Exception:
    # Kill the partial session before re-raising
    subprocess.run(["tmux", "kill-session", "-t", name], check=False)
    raise
```

The wrapper's `--tmux` path is far simpler than sprint's 3-pane layout — it needs only ONE
window (no `split-window` / summary / tail panes; those are `tmux.py:116-156` and are
sprint-TUI-specific, NOT reusable). So the wrapper's `--tmux` reduces to:
`new-session -d -s <name> <inner cmd>` → `attach-session` → read `.reflect-exitcode`. The
multi-pane machinery (`update_tail_pane`, `update_summary_pane`, `TUI/SUMMARY/TAIL_PANE`
constants) is **not** needed and should not be copied.

### 1g. Kill / escalation (`kill_sprint`, tmux.py:264-323) — optional reuse

`kill_sprint(force)` implements SIGTERM→wait 10s→SIGKILL via the pane PID
(`#{pane_pid}` from `tmux display-message`, `tmux.py:274-285`), falling back to a `C-c`
send-keys. This is **only relevant** if the wrapper offers a `reflect kill`-style verb; the
spec §5/§9 does not list one, so this is informational, not required.

---

## 2. `<BASE>..HEAD` git-base resolution idiom (FR-3)

### 2a. CRITICAL: `git merge-base` is NOT implemented in Python — anywhere

Exhaustive search (`grep -rn 'merge-base\|merge_base' src/`) returns exactly **one** hit, and
it is **prose inside a skill markdown file**, not executable Python:

```
src/superclaude/skills/task-builder/SKILL.md:1996
  ... where `<BASE>` is the commit recorded at task start (frontmatter `start_commit`,
  or `git merge-base HEAD <integration>` if unset) ...
```

**Implication for FR-3:** the spec's chain — `start_commit` (frontmatter) → else
`git merge-base HEAD <integration>` → else fail `base-unresolved` — has **no existing helper
to import**. The wrapper must author the `merge-base` subprocess call itself in
`cli/reflect/` (the spec's §8 file list: `runner.py`/`contract.py`/etc.). This is a
**fresh-write**, not a reuse. The task SKILL.md prose is the behavioral spec for it.

### 2b. The reusable shape is `drift.py`'s `_git()` (uses `@{upstream}`, not a named branch)

The only git-base-style resolution in Python is the **Tier-2 git annotation** in
`src/superclaude/cli/sprint/resume/drift.py`, method `_annotate_git` (`drift.py:253-297`).
It does NOT use `merge-base` and does NOT use a named integration branch — it uses the
tracking-branch ref `@{upstream}`. But its **subprocess call shape is the model to copy**:

```python
# drift.py:262-272
import subprocess
cwd = str(phase_file.parent)

def _git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-C", cwd, *args],
        capture_output=True,
        check=True,
        text=True,
    )
```

```python
# drift.py:274-288
try:
    # Require an upstream (skips detached-HEAD / no-upstream) and a tracked file.
    _git("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}")
    _git("ls-files", "--error-unmatch", str(phase_file))
    diff = _git(
        "diff", "--ignore-all-space", "--stat", "@{upstream}", "--", str(phase_file),
    )
except (OSError, subprocess.SubprocessError):
    return assessment  # git unavailable / detached / no upstream / untracked
```

**Reusable idioms from this shape:**
- `["git", "-C", cwd, *args]` — pin the repo dir with `-C` (the wrapper should pin the
  project root per FR-10 "cwd stays the project root so `--diff` resolves against the same
  repo"). `capture_output=True, text=True, check=True`.
- The **probe-before-use** pattern: run a cheap `rev-parse`/`merge-base` first; catch
  `(OSError, subprocess.SubprocessError)` and route to a defined fallback. For the wrapper,
  the fallback is NOT "silently skip" (drift's fail-open) — it is **fail `base-unresolved`**
  (FR-3) → `blocked` verdict (FR-5/§6, exit 2). Another required posture inversion.

### 2c. The other git call in scope — `get_git_diff_context` (process.py:371-393)

`src/superclaude/cli/sprint/process.py` does NOT contain `merge-base`. Its only git usage is
`get_git_diff_context(start_commit)` (`process.py:371-393`):

```python
# process.py:380-392
result = _subprocess.run(
    ["git", "diff", "--stat", start_commit],
    capture_output=True, text=True, timeout=10,
)
if result.returncode != 0 or not result.stdout.strip():
    return ""
...
except (FileNotFoundError, _subprocess.TimeoutExpired, OSError):
    return ""
```

This consumes a **pre-resolved `start_commit`** (a SHA or branch ref) and runs
`git diff --stat <start_commit>` for prompt context — it never *resolves* the base. Note the
`timeout=10` guard and the `FileNotFoundError/TimeoutExpired/OSError` catch — good hygiene to
copy for the wrapper's own git calls. **`start_commit` here is the SAME concept as FR-3's
frontmatter `start_commit`** (the first arm of the base chain), confirming the frontmatter
field name is the project-canonical one.

### 2d. Which integration branch name does the project use? (master vs integration)

Both branches exist; **`master` is the default**:
- `git symbolic-ref refs/remotes/origin/HEAD` → `refs/remotes/origin/master` (origin default
  = `master`).
- `git rev-parse --verify integration` succeeds → an `integration` branch DOES exist locally.
- CLAUDE.md "Git Workflow" documents the structure as
  `master (production) ← integration (testing) ← feature/*`.
- The repo CLAUDE.md PR rule mandates `--base master` for PRs (master is the merge target of
  record).

**Recommendation for FR-3's `<integration>` token:** the spec writes `git merge-base HEAD <integration>`
but the project's actual stable trunk is **`master`** (origin/HEAD), with `integration` as an
intermediate. There is **no code constant** naming either as "the integration branch" — the
choice is unencoded. The wrapper should either (a) make the base branch a configurable
parameter defaulting to `master` (matches origin/HEAD and the PR target), or (b) resolve
`origin/HEAD` dynamically via
`git rev-parse --abbrev-ref origin/HEAD` rather than hardcoding. Hardcoding `integration`
would diverge from the actual default trunk. **[Decision deferred to wrapper author — flag in
task as an Open Question: "FR-3 `<integration>` literal — `master` (origin/HEAD) or
`integration`?"]**

---

## 3. Reuse vs. Adapt matrix (verbatim / adapt / fresh-write)

| Capability | Source (file:line) | Wrapper disposition |
|---|---|---|
| `is_tmux_available()` guard | `tmux.py:50-55` | **Verbatim** (copy or import) |
| Deterministic session name | `tmux.py:58-61` | **Adapt** — prefix `sc-reflect-`, hash the pinned `--output` dir |
| `find_running_session()` prefix scan | `tmux.py:64-78` | **Adapt** — change prefix to `sc-reflect-` |
| Detached `new-session -d -s <name> *argv` | `tmux.py:94-108` | **Verbatim shape** — splice the inner `reflect run --no-tmux` argv |
| Inner `--no-tmux` re-invocation builder | `tmux.py:176-210` | **Adapt** — build `reflect run` argv; forward pinned `--output` |
| `attach-session` → read sentinel | `tmux.py:162-173` | **Adapt** — sentinel = `.reflect-exitcode`; **invert fail-open → fail-closed** (missing/garbage → `blocked` exit 2, NOT success) |
| Sentinel writer `_write_exit_sentinel` | `executor.py:2252-2264` | **Adapt** — write `.reflect-exitcode` to pinned `--output`; foreground (default) path owns the write |
| Partial-setup session cleanup | `tmux.py:157-160` | **Verbatim** (simpler — only one window to clean) |
| 3-pane layout / `update_*_pane` / pane constants | `tmux.py:116-156, 213-252, 40-42` | **DO NOT reuse** — sprint-TUI-specific; wrapper needs one window |
| `kill_sprint` SIGTERM→SIGKILL escalation | `tmux.py:264-323` | **Skip** unless a `reflect kill` verb is added (not in spec) |
| `_git()` subprocess shape (`git -C cwd ... check=True text=True`) | `drift.py:262-272` | **Adapt as the model** for the wrapper's git calls |
| probe-then-fallback try/except `(OSError, SubprocessError)` | `drift.py:274-288` | **Adapt** — fallback is `base-unresolved` → `blocked`, NOT silent skip |
| `git diff --stat <ref>` w/ `timeout=10` + error catch | `process.py:380-392` | **Pattern reuse** for hygiene; consumes already-resolved base |
| `git merge-base HEAD <integration>` | **NONE in Python** — only `task-builder/SKILL.md:1996` (prose) | **FRESH-WRITE** the resolution chain in `cli/reflect/` |

---

## 4. Foreground-blocking default (spec §5) — no tmux involved

Per spec §5 + §8, the wrapper's default mode is `proc.start(); rc = proc.wait()` on a bare
`ClaudeProcess` — **no tmux, no sentinel round-trip**. The sentinel/window machinery in §1 is
ONLY engaged by `--tmux`. The sprint precedent for the inner foreground writer
(`executor.py:2244-2249`) confirms the pattern: the foreground process computes its own
exit code and (under tmux) drops a sentinel; standalone it just exits. The reflect wrapper's
foreground path returns its derived exit code directly to the shelling Bash item (spec §5),
making `--tmux` strictly additive. (ClaudeProcess lifecycle itself is R01's scope, not mine.)

---

## 5. Completeness / Unverified notes

- The `<integration>` literal for FR-3 is **unencoded in code** — flagged in §2d as an Open
  Question for the wrapper author. Verified facts: `origin/HEAD → master`, `integration`
  branch exists, PR target is `master`.
- The fail-OPEN sentinel-readback behavior (`tmux.py:170-171`) and fail-OPEN git fallback
  (`drift.py:287-288`) are both **intentional for their interactive contexts** but
  **contradict the wrapper's fail-closed posture** (FR-8/NFR-4). The required inversions are
  called out in §1c, §2b, and the §3 matrix. **Verified** from source, not assumed.
- No `.reflect-exitcode` references exist yet in the repo (the wrapper is greenfield); the
  filename is the spec's (§5), to be created by the wrapper.

---

## Summary

**tmux idiom (`tmux.py`):** `launch_in_tmux` (`tmux.py:81-173`) is the reusable template —
`tmux new-session -d -s <name> *argv` (argv-spliced inner command, `tmux.py:94-108`) →
`tmux attach-session -t <name>` (blocks while operator watches live, `tmux.py:163`) → read
`<state_dir>/.sprint-exitcode` and `raise SystemExit(rc)` (`tmux.py:166-173`). Session name =
`sc-sprint-` + 8-hex sha1 of the resolved dir (`tmux.py:58-61`). The sentinel is WRITTEN by
the foreground `--no-tmux` inner run via `_write_exit_sentinel` (`executor.py:2252-2264`), and
the inner/outer agree on the path because `--state-dir` is forwarded (`tmux.py:196-202`). The
wrapper reuses the launch+attach+sentinel shape but: (a) one window only (drop the 3-pane
TUI), (b) prefix `sc-reflect-`, sentinel `.reflect-exitcode` under the pinned `--output`,
(c) **invert fail-open → fail-closed** (missing sentinel = `blocked` exit 2, not success).

**git-base idiom:** `git merge-base HEAD <integration>` **does not exist in Python anywhere** —
only as prose in `task-builder/SKILL.md:1996`. FR-3's base chain is a **fresh-write**. The
reusable model is `drift.py`'s `_git()` shape (`drift.py:262-272`,
`["git", "-C", cwd, *args]`, `capture_output/text/check=True`) and its probe-then-catch
`(OSError, SubprocessError)` pattern (`drift.py:274-288`) — but `drift.py` uses `@{upstream}`,
not a named branch, and fails open; the wrapper must use `merge-base` against a chosen base
branch and fail closed (`base-unresolved` → `blocked`). `process.py` has NO merge-base; its
`get_git_diff_context` (`process.py:371-393`) only *consumes* a pre-resolved `start_commit`
(same field name as FR-3's frontmatter arm) with a `timeout=10` hygiene guard worth copying.

**Branch name:** project default trunk is **`master`** (`origin/HEAD → master`, PR `--base master`);
`integration` also exists. The `<integration>` token in FR-3 is **unencoded** — recommend
making it configurable (default `master`) or resolving `origin/HEAD` dynamically rather than
hardcoding `integration`. Flagged as an Open Question.

**Status:** Complete.
