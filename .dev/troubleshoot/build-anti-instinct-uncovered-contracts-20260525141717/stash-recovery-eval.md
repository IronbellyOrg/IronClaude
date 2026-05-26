# Stash Recovery — `src/superclaude/cli/eval/` (15 files)

**Stash**: `stash@{0}` — `7185ed32` "pre-existing dirty state (262 files) — park for Fix B rebase"
**Created**: 2026-05-25 20:10:55 +0000 (immediately before rebase of Fix B onto `origin/master`)
**Parent**: `505975ed` "fix(roadmap): mechanism-signature refactor for anti-instinct integration_contracts"
**Branch**: `fix/integration-contracts-mechanism-signature`
**Investigator stance**: read-only inspection; nothing popped, applied, or modified.

---

## A. Per-file summary table

| File (`src/superclaude/cli/eval/…`) | Last commit on master | Stash diff one-liner (with `-w`) | Verdict |
|---|---|---|---|
| `artifact_layout.py` | `0365a055` (3d ago, #75) | 1 collapse: `raise ValueError(…)` joined onto one line | **STALE** — formatter only |
| `capabilities.py` | `1ca25953` (5d ago, #66) | `_CapabilitySpec(…)` calls reflowed to one-arg-per-line; `if … and …` collapsed; blank lines added before nested `def` | **STALE** — formatter only |
| `claude_process.py` | `1ca25953` (5d ago, #66) | 1 collapse: `raise ClaudeProcessAdapterError(…)` joined | **STALE** — formatter only |
| `commands.py` | `0365a055` (3d ago, #75) | Several string/f-string collapses, `if a or b or c:` flattened, `datetime.now(…).iso…` joined | **STALE** — formatter only |
| `coverage.py` | `0365a055` (3d ago, #75) | List/dict comprehensions reflowed to one-liners | **STALE** — formatter only |
| `exit_codes.py` | `0365a055` (3d ago, #75) | Pure whitespace: trailing comments re-aligned (`1            #` → `1  #`) | **STALE** — whitespace only |
| `expect.py` | `1ca25953` (5d ago, #66) | Multi-value `return False, msg, {…}, _make_failure(…)` reformatted into wrapped tuple-returns — 503 raw lines, 241 non-ws | **STALE** — formatter only (highest line count, but mechanical) |
| `isolation.py` | `0365a055` (3d ago, #75) | 1 comprehension collapsed to single line | **STALE** — formatter only |
| `loader.py` | `0365a055` (3d ago, #75) | 1 f-string concat collapsed | **STALE** — formatter only |
| `orchestrator.py` | `0365a055` (3d ago, #75) | 2 `raise … f"…"` calls joined | **STALE** — formatter only |
| `pty_driver.py` | `1ca25953` (5d ago, #66) | Two ternary expressions wrapped with `(\n … \n)` | **STALE** — formatter only |
| `pty_stream.py` | `1ca25953` (5d ago, #66) | Aligned comments on regex lines normalized; nested `def` blank-lines added | **STALE** — formatter only |
| `runner.py` | `1ca25953` (5d ago, #66) | Long `if …:` and Protocol signatures wrapped; set literal `{"setup", "deploy_hooks", …}` reformatted | **STALE** — formatter only |
| `run_report.py` | `0365a055` (3d ago, #75) | 1 call joined to one line | **STALE** — formatter only |
| `schemas/__init__.py` | `1ca25953` (5d ago, #66) | `resources.files(…).joinpath(…).read_text(…)` reformatted as chained method call | **STALE** — formatter only |

**Aggregate diff stat (entire eval/ subset, ignoring whitespace):** 14 files, +291 / −127 lines — all attributable to `black`-style reflow at `line-length = 88` (matches `pyproject.toml [tool.black]` config, `pyproject.toml:~tool.black` block).

---

## B. The originating workstream

**These changes do NOT belong to a tracked workstream.** Investigation evidence:

1. **Branch context**: `fix/integration-contracts-mechanism-signature` (current) is a roadmap-side fix targeting `src/superclaude/cli/roadmap/integration_contracts.py` per `.dev/troubleshoot/build-anti-instinct-uncovered-contracts-20260525141717/fix-b-opus.md:8` — *not* eval/.
2. **Commit author intent**: the only commit on this branch (`505975ed`) touches roadmap contracts; eval/ files were never staged.
3. **Stash subject line**: `"pre-existing dirty state (262 files) — park for Fix B rebase"` — author explicitly labels this as accumulated, unrelated working-tree drift, not Fix B work.
4. **Diff signature**: every eval/ hunk is a black/ruff-format reflow (line-wrap normalization, no identifier changes, no new logic, no TODOs). Sample: `git diff 'stash@{0}^' 'stash@{0}' -w -- src/superclaude/cli/eval/exit_codes.py` shows only `#`-alignment whitespace.
5. **Recent eval/ work is already merged**:
   - PR #75 `feat(cliEval): exit_codes module + H1-H5/M1-M6/CC1-CC3/T1-T9 remediation` → `0365a055` (2026-05-22) — completed, no follow-up branch active.
   - PR #66 `feat(cliEval): land cliEval CLI module + task track + supporting infra changes` → `1ca25953` (2026-05-20) — completed.
   - No open task folder under `.dev/tasks/to-do/` references `exit_codes`, `cliEval`, `eval/expect`, or `eval/capabilities`.
6. **No semantic markers**: the added lines contain zero `TODO`/`FIXME`/`XXX`/`stub` markers (`grep` on additions returned empty). The 17 hits in `runner.py` are pre-existing `noqa`/`pragma` annotations untouched by the diff.

**Most likely origin**: An earlier session ran `black src/` (or an editor format-on-save) across the working tree without committing. When Fix B needed a clean rebase, the formatter-dirty files were parked into the stash alongside ~247 other unrelated dirty files.

---

## C. Aggregate verdict

**DROP** (do not re-apply).

Rationale:
- No new identifiers, constants, exit codes, branches, error types, or semantic logic introduced.
- HEAD copies (last touched by PRs #66/#75) already represent the canonical committed state.
- Re-applying would create a no-op-but-noisy `style: black reformat` commit that bloats diffs for any future eval/ change.
- If the project later decides to enforce black globally, that should be a deliberate repo-wide `chore(format): apply black` PR — not a quiet salvage from a parking-lot stash.
- No file in the stash is "more current" than HEAD in any behavioural sense; the rebase erased zero real work for these 15 files.

**Confidence**: very high. Every hunk inspected is mechanical wrap/unwrap at column 88. No counter-evidence found in task folders, recent commits, PR titles, or branch-name context.

---

## D. Recommended recovery commands (read-only inspection + drop)

Run from `/config/workspace/IronClaude`:

```bash
# 1. (Optional) Re-confirm the eval-only subset is whitespace/format only
git diff 'stash@{0}^' 'stash@{0}' -w --stat -- src/superclaude/cli/eval/
# Expect: 14 files, ~291 ins / ~127 del, all formatter reflow

# 2. (Optional) Verify HEAD eval/ files are clean per ruff/black
uv run ruff check src/superclaude/cli/eval/
uv run black --check src/superclaude/cli/eval/

# 3. Drop nothing yet — the stash also holds 247 other unrelated files.
#    Do NOT `git stash drop` on the whole stash blindly; that would lose any
#    real work parked in the other 247 entries. Audit those separately.

# 4. If a future session wants to formally re-run formatters as a deliberate
#    chore commit (recommended path forward, NOT salvage):
git switch -c chore/black-format-eval
uv run black src/superclaude/cli/eval/
git add src/superclaude/cli/eval/
git commit -m "chore(cliEval): apply black line-length=88 reflow"
```

**Do NOT**:
- `git stash pop` (would dirty the working tree with 262 files mid-Fix-B PR).
- `git checkout 'stash@{0}' -- src/superclaude/cli/eval/` (re-applies formatter noise as uncommitted changes on the Fix B branch).
- Cherry-pick any subset — there is no subset worth preserving.

---

## Citations

- Stash metadata: `git stash list` → `stash@{0}: On fix/integration-contracts-mechanism-signature: pre-existing dirty state (262 files) — park for Fix B rebase`
- Stash commit/time: `git log -1 stash@{0}` → `7185ed32 2026-05-25 20:10:55 +0000`
- Black config: `pyproject.toml` `[tool.black]` block, `line-length = 88`, `target-version = ["py310","py311","py312"]`
- Last-touched commits per file: `git log -1 --pretty=… -- src/superclaude/cli/eval/<file>` (matrix above)
- PR #75 / #66 SHAs: `git log --oneline -20 master -- src/superclaude/cli/eval/`
- Reflog snapshot of rebase window: `git reflog --date=iso | head -10` (entries `HEAD@{2026-05-25 20:04:37 … 20:30:43}`)
- Fix B scope evidence: `.dev/troubleshoot/build-anti-instinct-uncovered-contracts-20260525141717/fix-b-opus.md:8` (target = `roadmap/integration_contracts.py`, not eval/)
