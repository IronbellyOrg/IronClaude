# Branch Audit — `fix/claude-process-stdin-large-prompts`

**Date:** 2026-06-10 · **Mode:** read-only, evidence-gated · **Auditor:** /sc:cleanup-audit (single-branch adaptation)
**Question:** merge risk/conflicts vs. what is lost on deletion.

/ Merge-base: `ad07353e` (2026-04-30, PR #28) · branch is **154 commits behind** master · 12 commits ahead · **never pushed (no remote tracking ref).**

---

## Verdict: DO NOT DELETE — PRESERVE IMMEDIATELY

The asymmetry is extreme: **preservation cost ≈ seconds** (`git push`), **deletion loss = a complete, tested, adversarially-reviewed reliability fix + an entire skill + its 68-file research corpus, none of which exist on any remote.** Merge is mechanically clean; the only real "merge cost" is scope pollution from inherited WIP artifacts, which a cherry-pick avoids.

---

## A. Merge risk & conflicts

| Check | Result | Evidence |
|---|---|---|
| Textual conflicts vs current master | **NONE** | `git merge-tree --write-tree --name-only origin/master <branch>` → exit 0, tree `ea5b3e80`, no conflicted-file list |
| Semantic drift — `pipeline/process.py` (core fix target) | **ZERO** | `git rev-list --count ad07353e..origin/master -- …/pipeline/process.py` = **0** (master never touched it in 154 commits) |
| Semantic drift — `cli_portify/process.py` | **Negligible** | 1 master commit since base: `ad72b1bb` ruff F401/I001 lint sweep. Branch change touches `build_command()` body only, **not imports** → no overlap |
| New test file collision | **None** | `tests/pipeline/test_process_stdin.py` absent from master tree (new file) |
| `.claude/skills/skill-creator` committed path | **No-op, not a risk** | It was a symlink (mode 120000) the branch *deleted* (status `D`); master already lacks it |

**The real merge cost (not a conflict):** merging the *whole branch* pulls in all 12 commits, including the inherited 70-file persona-research WIP base (`5e1349c5`) and **137 `.dev/` force-committed artifacts** (`.dev/architectural/claude-process-stdin-patch/` ×35, `.dev/tasks/to-do/` ×67, `.dev/releases/current/` ×1). These paths are excluded-by-scope/gitignored but were force-added on this branch; merging writes them into master history permanently. **A cherry-pick of the code+test commits avoids this entirely.**

### Code quality (read of actual diffs)
- `pipeline/process.py` (+~150): `PROMPT_MAX_BYTES` (16 MiB, env-overridable) + typed `PromptTooLargeForArgv(ValueError)` pre-spawn guard; prompt encoded once and reused; naive `stdin.write()` replaced by `_write_prompt_to_stdin()` — chunked `os.write` on raw FD with explicit **EINTR retry**, BrokenPipe/OSError captured to `self._stdin_error`, **stdin closed in `finally`** (guarantees EOF to `claude --print`), error surfaced via `_log.warning` in both `wait()` and `terminate()`. Production-grade, accurately commented, references prior commit `4799719` + DESIGN.md for traceability.
- `cli_portify/process.py` (+119/-4): **real bug fix** — replaces dead `cmd.index("-p")` lookup (always fell through to append-at-end) with `--output-format`+2 anchor splice. Correct given prompt-via-stdin (no `-p` in argv).
- **Tests: 393 lines, 14 test fns across 5 classes** — portify anchor adjacency/repeat-resilience, `PROMPT_MAX_BYTES` over+under cap, 400 KB stdin round-trip, UTF-8 emoji round-trip, terminate-during-write no-hang, empty-prompt zero-bytes, broken-pipe→log surfacing, tool_write_mode redirect, argv byte-size invariant. Directly exercises every added code path.
- Supporting docs: DESIGN.md/RECONCILED_DESIGN.md, baseline-reconciliation, STRICT-tier verification review, /sc:adversarial coverage analysis → this was a structured, vetted effort, not a sketch.

**Not executed in this audit** (read-only, no checkout): the test suite. Recommend `uv run pytest tests/pipeline/test_process_stdin.py` post-cherry-pick.

## B. What is lost on deletion

| Asset | Files | Unique / recoverable? |
|---|---|---|
| **stdin reliability fix** (`pipeline/process.py`, `cli_portify/process.py`) | 2 | **UNRECOVERABLE** — not in master, not in any remote (`PROMPT_MAX_BYTES` grep on origin/master = absent) |
| **stdin test suite** (`test_process_stdin.py`) | 1 | **UNRECOVERABLE** — new file, nowhere else |
| **stdin design/verification corpus** (`.dev/architectural/claude-process-stdin-patch/`) | 35 | **UNRECOVERABLE** — only on this branch |
| **persona-research skill source** (`src/superclaude/skills/sc-persona-research-protocol/SKILL.md`, 1911 ln) | 1 | **Single-copy-in-VCS** — commit `5e1349c5` exists in only 2 refs, both **local + unpushed** (this branch + `feat/tdd-spec-merge`); zero remotes. A gitignored `.claude/skills/` synced copy survives on disk but is not SoT and is wipeable by sync/install/clean |
| **persona-research workspace** (research/qa/spec under `.dev/tasks/to-do/`) | 67 | **Single-copy-in-VCS** — same two local branches only |

**Recoverability nuance:** deleting *this branch alone* does not lose persona-research (it also lives in `feat/tdd-spec-merge`). But `feat/tdd-spec-merge` is *also* local, unpushed, remote-gone — so deleting *both* (the stated cleanup intent) destroys persona-research permanently.

## C. Recommended action sequence

1. **Rescue now (seconds):** `git push -u origin fix/claude-process-stdin-large-prompts` — ends single-copy-on-disk risk for *both* the stdin fix and persona-research (this branch contains `5e1349c5`).
2. **Preferred integration (clean PR, no sprawl):** cherry-pick the 6 substantive commits onto a fresh branch off `origin/master`:
   `526a6061` (cli_portify anchor) · `c42139b2` (PROMPT_MAX_BYTES) · `be465202` (size guard) · `5a8e5e78` (chunked write) · `01cf2ef9` (tool_write_mode test) · `dda68d9d` (argv invariant test). Optionally add the design docs. Run pytest, then `gh pr create --repo IronbellyOrg/IronClaude --base master`.
3. **persona-research:** decide independently (finish+land via its own branch, or keep archived on the pushed branch). Must NOT block the stdin fix.
4. **Only after** the fix is merged AND persona-research is preserved → safe to delete the local branch (and `feat/tdd-spec-merge`).

**Bottom line:** merging is low-risk and high-value; deleting is high-loss and irreversible. Preserve first, integrate via cherry-pick, clean up last.

---

## D. Verification executed (2026-06-10)

1. **Rescue push** — `git push -u origin fix/claude-process-stdin-large-prompts` → new branch on `origin` (IronbellyOrg fork), upstream tracked. Remote head `2c212794`. **No longer single-copy-on-disk.**
2. **Empirical clean-merge proof** — cherry-picked the 6 substantive commits (`526a6061 c42139b2 be465202 5a8e5e78 01cf2ef9 dda68d9d`) onto fresh `origin/master` (`e97aa4fd`) in an isolated `/tmp` worktree → **all 6 applied with zero conflicts**, confirming the `merge-tree` finding.
3. **Targeted tests** — `uv run pytest tests/pipeline/test_process_stdin.py` → **13 passed** (PromptMaxBytes guard, 400 KB + UTF-8-emoji stdin round-trip, terminate-no-hang, broken-pipe→log, portify anchor, argv invariant, tool_write_mode).
4. **Regression sweep** — `uv run pytest tests/pipeline/ tests/cli_portify/` → **1296 passed, 1 skipped, 0 failed** (2 pre-existing `invariant_pass.py` warnings, unrelated).
5. Temp worktree + `verify/stdin-cherry-pick` branch removed; main working tree (`fix/prd-parallel-gate-advisory`, unrelated in-progress work) left untouched.

**Conclusion: GREEN.** The cherry-pick path is proven clean and fully tested against current master. Ready to open a PR whenever desired.
