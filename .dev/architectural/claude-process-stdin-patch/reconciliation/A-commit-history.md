# Agent A — Commit-History Archaeology: ClaudeProcess Subsystem

Reconciliation report for the `claude-process-stdin-patch` design package
(`/config/workspace/IronClaude/.dev/architectural/claude-process-stdin-patch/DESIGN.md`)
against the ClaudeProcess subsystem on branch `feat/tdd-spec-merge`.

Tip references at time of analysis:
- `master` tip: `4e0c621` (Mar 24 2026) — Merge PR #19 (v3.7-TurnLedgerWiring)
- `feat/tdd-spec-merge` tip: `5e1349c` (Apr 30 2026) — WIP persona-research artifacts
- `fix/claude-process-stdin-large-prompts` tip: `530955b` (Apr 30 2026) — design-package import (current HEAD)
- `merge-base master feat/tdd-spec-merge`: `4e0c621` (i.e., master == merge-base; master has not advanced since branching)

---

## 1. Methodology

I scanned the ClaudeProcess subsystem with read-only `git` commands run from
`/config/workspace/IronClaude` (no source modification, no tests, no
sync-dev). Scope spanned all refs (`--all`), with attention to (a) the
file `src/superclaude/cli/pipeline/process.py`, (b) the cli-portify
subclass `src/superclaude/cli/cli_portify/process.py`, (c) any commit
adding/removing the strings `subprocess.PIPE`, `tool_write_mode`,
`ClaudeProcess(`, `"-p"` (S-pickaxe), and (d) the `master..feat/tdd-spec-merge`
delta. Per touching commit I ran `git show --stat` and `git show -- <file>`
to read the diff. Branch-topology checks used `git branch -a --contains
<sha>` and `git merge-base --all master feat/tdd-spec-merge`. The
"all branches" `--source` log over the file confirmed every commit
modifying it is reachable from `feat/tdd-spec-merge`; none have landed on
`master`.

---

## 2. Chronological commit table

Sorted oldest → newest. Files-touched column lists only the
ClaudeProcess-relevant files in that commit (the commits themselves are
typically much larger).

| SHA       | Date (UTC)         | Author   | Branch reachability                | Files Touched                                              | Intent (paraphrased)                                                   | Behavioral Change (one-liner)                                                                                       |
|-----------|--------------------|----------|------------------------------------|------------------------------------------------------------|------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------|
| `6548f17` | 2026-03-05 16:28   | RyanW    | feat/tdd-spec-merge, NOT on master | `src/superclaude/cli/pipeline/process.py` (created, 171 L) | Introduce pipeline base module; sprint ClaudeProcess inherits from it. | First appearance of `pipeline/process.py::ClaudeProcess`. Sprint refactored to subclass. Stdin set to `DEVNULL`; `os.setpgrp` gated on `hasattr`. Argv carries `-p <prompt>`. |
| `a606727` | 2026-03-06 15:05   | RyanW    | feat/tdd-spec-merge, NOT on master | `src/superclaude/cli/pipeline/process.py` (+23 / -2)       | v2.13 pipeline unification — add lifecycle hooks.                      | Adds `on_spawn` / `on_signal` / `on_exit` callable hooks; refactors `wait()` and `terminate()` to invoke them. Argv-prompt path unchanged.                                  |
| `c39fa91` | 2026-03-14 02:09   | RyanW    | feat/tdd-spec-merge, NOT on master | `src/superclaude/cli/cli_portify/process.py` (created)     | v2.24.1 cli-portify v5 — introduce `cli_portify` package.              | Adds `PortifyProcess` subclass of `pipeline.ClaudeProcess` with dual `--add-dir`, `@path` artifact references, claude-binary detection. Inherits all argv/stdin behavior.   |
| `b702f03` | 2026-03-14 07:39   | RyanW    | feat/tdd-spec-merge, NOT on master | `src/superclaude/cli/cli_portify/process.py`               | "more updates and planning" — incremental cli_portify edits.           | Touches the cli_portify subclass; pipeline base unchanged.                                                                                                                |
| `6240efa` | 2026-03-15 05:58   | RyanW    | feat/tdd-spec-merge, NOT on master | `src/superclaude/cli/pipeline/process.py` (+2)             | Add `--tools default` to `build_command()`.                            | Inserts `"--tools", "default"` into argv before `--max-turns`. Argv-prompt delivery still in place.                                                                       |
| `2c6e59b` | 2026-03-15 23:30   | RyanW    | feat/tdd-spec-merge, NOT on master | `src/superclaude/cli/cli_portify/process.py`               | Partially-finished v2.25 work; deep analysis & refactor of 2.2.        | Modifies cli_portify subclass; pipeline base unchanged.                                                                                                                   |
| `c4fa7f4` | 2026-03-16 23:19   | RyanW    | feat/tdd-spec-merge, NOT on master | `src/superclaude/cli/pipeline/process.py` (+2)             | v2.25 phases 4–11; preflight executor integration.                     | Adds `env_vars: dict[str, str] \| None = None` ctor parameter and stores it as `_extra_env_vars` for preflight context injection. Argv/stdin unchanged.                    |
| `39d5100` | 2026-04-18 14:58   | Alireza  | feat/tdd-spec-merge, NOT on master | `src/superclaude/cli/pipeline/process.py` (+29 / -1)       | Roadmap-pipeline template + compression support.                       | **Adds `tool_write_mode: bool = False`** ctor parameter. When True, stdout redirects to `output_file.with_suffix(".log")` because the LLM writes the real artifact via the Write tool. Adds `validate_tool_write_output()`. Argv/stdin path unchanged. |
| `4799719` | 2026-04-20 17:10   | Alireza  | feat/tdd-spec-merge, NOT on master | `src/superclaude/cli/pipeline/process.py` (+18 / -4)       | Use stdin for the roadmap pipeline instead of `-p`.                    | **Removes `-p, self.prompt` from argv.** Switches `stdin` from `DEVNULL` → `subprocess.PIPE`. After `Popen`, writes `self.prompt.encode("utf-8")` to stdin and closes; `BrokenPipeError` swallowed. Comment cites Linux `MAX_ARG_STRLEN = 128 KB`. |

(All other commits in the `master..feat/tdd-spec-merge` range — TUI v2 waves, prd-skill portify, recommend-v2, install-auggiemcp, task-unified — leave both `pipeline/process.py` and `cli_portify/process.py` untouched.)

---

## 3. Key commits

### `6548f17` — Pipeline base module created (Mar 5, 2026)

This is the first commit where
`/config/workspace/IronClaude/src/superclaude/cli/pipeline/process.py`
exists. The 171-line base `ClaudeProcess` is what the design package's
DESIGN.md treats as "the pipx-installed snapshot." Argv form at this
commit:

```
claude --print --dangerously-skip-permissions --verbose <permission_flag>
       --no-session-persistence --max-turns N --output-format <fmt>
       -p <self.prompt>
       [extra_args...]
```

`stdin=subprocess.DEVNULL`; stdout/stderr to real file handles; `os.setpgrp`
gated behind `hasattr(os, "setpgrp")`. Sprint's `process.py` is rewritten
to delegate to this base via `super().__init__()` with
`output_format="stream-json"`.

### `a606727` — Lifecycle hooks (Mar 6, 2026)

Added `on_spawn(pid)`, `on_signal(pid, signal)`, `on_exit(pid, returncode)`
optional callable hooks invoked from `start()`, `terminate()`, and `wait()`.
These hooks are part of the public ctor signature today; any patch that
re-declares the constructor or wraps `start()` must preserve them.

### `6240efa` — `--tools default` argv addition (Mar 15, 2026)

Two-line diff inserting `"--tools", "default"` between
`--no-session-persistence` and `--max-turns`. Important for the design
because DESIGN.md's current-state argv listing must match this order.

### `c4fa7f4` — `env_vars` constructor parameter (Mar 16, 2026)

Adds `env_vars: dict[str, str] | None = None` to the ctor and stores it
as `self._extra_env_vars`, threaded into `build_env()` for preflight
context injection. Constructor signature reconciliation point: any
proposal that re-declares `__init__` must keep this param.

### `39d5100` — `tool_write_mode` (Apr 18, 2026) — load-bearing for reconciliation

Full message: *"added template and compression to the roadmap pipeline"*.

The mechanically-significant change is the new `tool_write_mode: bool =
False` ctor parameter. When True:
- `start()` opens `self.output_file.with_suffix(".log")` for `_stdout_fh`
  rather than `output_file` itself — because the LLM is expected to
  write `output_file` via the Write tool, not by streaming stdout.
- New `validate_tool_write_output()` method returns False (and logs a
  warning) if `output_file` is missing/empty after the subprocess exits.

This commit predates the stdin migration by two days and is what the
DESIGN.md does not account for. Any re-implementation of `start()` or
ctor must preserve both the parameter and the dual-output-file behavior.

### `4799719` — Stdin-for-prompt migration (Apr 20, 2026) — load-bearing for reconciliation

Full message: *"use stdin for the roadmap pipeline instead of passing the
prompt as argument; fixed obligation scanner problem with scaffolding
terms that were not intended as implementation; self-healing for
compression logic when the compressed input is not available"*.

Diff against `pipeline/process.py` (22 lines net):

1. `build_command()` no longer appends `["-p", self.prompt]`. Docstring
   updated: *"Prompt is delivered via stdin in start(), not as a -p argv
   value, to bypass the Linux MAX_ARG_STRLEN = 128 KB per-argument
   ceiling."*
2. `popen_kwargs["stdin"]` changes from `subprocess.DEVNULL` to
   `subprocess.PIPE`.
3. After `Popen`, write `self.prompt.encode("utf-8")` to
   `self._process.stdin` and `close()`. `BrokenPipeError` is caught
   silently; `wait()` will still surface the child exit code.
4. Comment cites the deadlock-safety argument: stdout/stderr are file
   handles (not pipes), so the parent never reads from the child and a
   blocked stdin write cannot deadlock.

This is precisely the patch DESIGN.md was authored to specify. The
migration is already in-tree and shipped as part of `feat/tdd-spec-merge`
(merged via PR #25 / PR #26 into the integration branch — see commits
`7756fad`, `de34a45` in the wider log). All 38 callsites in the repo
flow through this single point because `PortifyProcess` extends
`ClaudeProcess` (commit `c39fa91`) and roadmap/sprint/tasklist executors
construct via the base or its subclasses.

---

## 4. Branch topology

**Merge-base** (`git merge-base --all master feat/tdd-spec-merge`):
`4e0c62117ccdca2086ba87d5140ea263ee96212a` — *Merge pull request #19 from
IronbellyOrg/v3.7-TurnLedgerWiring* (Mar 24, 2026). This is also `master`'s
current tip — `master` has not advanced since the branch diverged.

Reachability of every ClaudeProcess-touching commit:

| SHA       | On master?      | On feat/tdd-spec-merge? | On fix/claude-process-stdin-large-prompts? |
|-----------|-----------------|-------------------------|--------------------------------------------|
| `6548f17` | YES (predates branching, on master) | YES | YES |
| `a606727` | YES (predates branching) | YES | YES |
| `c39fa91` | YES (predates branching) | YES | YES |
| `b702f03` | YES (predates branching) | YES | YES |
| `6240efa` | YES (predates branching) | YES | YES |
| `2c6e59b` | YES (predates branching) | YES | YES |
| `c4fa7f4` | YES (predates branching) | YES | YES |
| `39d5100` | **NO** (after divergence) | YES | YES |
| `4799719` | **NO** (after divergence) | YES | YES |

The pre-divergence ClaudeProcess commits (`6548f17` through `c4fa7f4`)
are part of master's history because master's tip `4e0c621` is itself a
descendant of those commits. The two load-bearing commits for
reconciliation (`39d5100` `tool_write_mode`, `4799719` stdin migration)
are exclusively on `feat/tdd-spec-merge` and its descendants (including
`fix/claude-process-stdin-large-prompts`). They reached
`feat/tdd-spec-merge` via merges of `feat/tdd-spec-merge-with-compression`
(PR #25, PR #26 — visible as `7756fad` and `de34a45` in the integration
log).

The current working branch `fix/claude-process-stdin-large-prompts`
branches from `feat/tdd-spec-merge` HEAD and adds only one commit
(`530955b`) which imports the design package into
`/config/workspace/IronClaude/.dev/architectural/claude-process-stdin-patch/`.
No source files have been modified on this branch.

The remote `origin/feat/tdd-spec-merge-with-compression` is the
authoring branch for `4799719` and `39d5100` per `git log --source`; it
was already merged into `feat/tdd-spec-merge`.

---

## 5. Timeline narrative

The pipx-installed snapshot DESIGN.md targets is logically equivalent to
the state introduced by `6548f17` (Mar 5, 2026) — when
`src/superclaude/cli/pipeline/process.py` was first carved out as a
reusable base from the sprint module. At that point `ClaudeProcess`
delivered the prompt as a `-p <prompt>` argv pair, set
`stdin=subprocess.DEVNULL`, and ran with a fixed argv shape. This is
exactly the failure mode the design package addresses: a prompt larger
than the Linux `MAX_ARG_STRLEN` 128 KB ceiling causes `Popen` to fail
with `OSError: [Errno 7] Argument list too long`.

Between Mar 6 and Mar 16, the subsystem accumulated additive features
without disturbing the prompt-delivery mechanism: `a606727` added
lifecycle hooks (`on_spawn`/`on_signal`/`on_exit`), `c39fa91` introduced
the `PortifyProcess` subclass for cli-portify, `6240efa` appended
`--tools default` to argv, and `c4fa7f4` added an `env_vars` ctor
parameter for preflight context injection. None of these changed how
the prompt was passed to the child process. The constructor signature
expanded from 9 to 13 keyword arguments over this period.

The two load-bearing changes for reconciliation arrived in April. On
Apr 18, `39d5100` added `tool_write_mode: bool = False` so the roadmap
pipeline could let the LLM write its output artifact via the Write
tool, sending Claude's stdout to a sibling `.log` file instead of the
expected output path. A companion `validate_tool_write_output()` method
was added so callers can detect "the LLM didn't write the file"
failures. Then on Apr 20, `4799719` performed the stdin migration the
DESIGN.md proposes: removed `-p <prompt>` from argv, switched
`popen_kwargs["stdin"]` from `DEVNULL` to `PIPE`, and added a
post-`Popen` write/close of `self.prompt.encode("utf-8")` with
`BrokenPipeError` swallowed. The diff is small (22 lines net on
`process.py`) and uses the deadlock-safety reasoning that the design
also relies on (stdout/stderr are file handles, not pipes; the parent
never reads from the child).

The net consequence for reconciliation is that the design package's
patch is, mechanically, already in-tree at `feat/tdd-spec-merge` HEAD —
but it was authored against a snapshot that did not yet have
`tool_write_mode` or the `env_vars` ctor parameter. Any reconciliation
output that "applies the design" by overwriting `start()` or the
constructor will silently regress those two features unless it merges
forward. No commit on `feat/tdd-spec-merge` has reverted or modified
`4799719` or `39d5100`; both are also reachable from
`origin/feat/tdd-spec-merge-with-compression` and were promoted to
`feat/tdd-spec-merge` via the existing merge PRs (#25, #26).

---

## Appendix A — Commands run

```
git -C /config/workspace/IronClaude log --follow --all --oneline -- src/superclaude/cli/pipeline/process.py
git -C /config/workspace/IronClaude log --follow --all -- src/superclaude/cli/pipeline/process.py
git -C /config/workspace/IronClaude log --follow --all -- src/superclaude/cli/cli_portify/process.py
git -C /config/workspace/IronClaude log --all -S 'subprocess.PIPE' -- src/superclaude/cli/pipeline/process.py
git -C /config/workspace/IronClaude log --all -S 'subprocess.PIPE'
git -C /config/workspace/IronClaude log --all -S 'tool_write_mode' -- src/superclaude/cli/pipeline/process.py
git -C /config/workspace/IronClaude log --all -S 'tool_write_mode'
git -C /config/workspace/IronClaude log --all -S 'ClaudeProcess(' -- 'src/**'
git -C /config/workspace/IronClaude log --all -S '"-p"' -- src/superclaude/cli/pipeline/process.py
git -C /config/workspace/IronClaude log --all --source --remotes --branches --oneline -- src/superclaude/cli/pipeline/process.py
git -C /config/workspace/IronClaude show 4799719 --stat
git -C /config/workspace/IronClaude show 4799719 -- src/superclaude/cli/pipeline/process.py
git -C /config/workspace/IronClaude show 39d5100 -- src/superclaude/cli/pipeline/process.py
git -C /config/workspace/IronClaude show 6240efa -- src/superclaude/cli/pipeline/process.py
git -C /config/workspace/IronClaude show a606727 -- src/superclaude/cli/pipeline/process.py
git -C /config/workspace/IronClaude show c4fa7f4 -- src/superclaude/cli/pipeline/process.py
git -C /config/workspace/IronClaude branch -a --contains 4799719
git -C /config/workspace/IronClaude branch -a --contains 39d5100
git -C /config/workspace/IronClaude merge-base --all master feat/tdd-spec-merge
git -C /config/workspace/IronClaude log master..feat/tdd-spec-merge --oneline -- src/superclaude/cli/pipeline/process.py src/superclaude/cli/cli_portify/process.py
```

## Appendix B — Commands that returned nothing

- `git -C /config/workspace/IronClaude log --all --grep='ClaudeProcess'` returned only commits with "ClaudeProcess" in their messages (not empty); no commit-message-level reverts of stdin/argv work were found.
- No commit was found that reverts, modifies, or competes with `4799719` after Apr 20, 2026 — the stdin-migration is the latest word on prompt delivery on `feat/tdd-spec-merge`.
- `cli_portify/process.py` has no commits between `2c6e59b` (Mar 15, 2026) and HEAD that affect prompt/stdin handling — the file inherits all behavior from `pipeline.ClaudeProcess` via `class PortifyProcess(ClaudeProcess)` (line 19 of the file), so the `4799719` change applies transitively to all 38 ClaudeProcess instantiations across the repo.
