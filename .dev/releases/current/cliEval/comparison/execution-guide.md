# Worktree Execution Guide — Parallel Pipeline A vs Pipeline B Run

**Purpose:** Step-by-step playbook to execute the **task portion** of both pipelines for `cliEval` in parallel, each in its own git worktree, with isolated working directories so they cannot interfere.

**Audience:** Maintainer (RyanW) or operator with shell access to the IronClaude repo.

**Outcome:** Two completed runs (Pipeline A's MDTM task-files executed via `/task`, Pipeline B's tasklist bundle executed via `superclaude sprint run`) sitting in separate worktrees on separate branches, ready for the post-execution code-audit comparison (see `prompts/post-execution-audit-prompt.md`).

---

## 0. Preconditions

```bash
cd ~/github/IronClaude   # or wherever the canonical repo lives
git fetch origin
git status               # confirm clean enough; existing dirty state will carry into worktrees
```

You need:
- ~6-10 GB free disk space (two worktrees + harness outputs + per-eval HOMEs if Pipeline B's executor goes that far)
- A second terminal multiplexer pane (tmux/screen) so you can watch both runs simultaneously
- The 4 Pipeline A task files already built (`.dev/tasks/to-do/TASK-RF-20260518-cliEval-P{1,2,3,4}-*/`)
- The 4 Pipeline A BUILD_REQUEST files persisted (`.dev/releases/current/cliEval/build-requests/`)
- The design spec persisted (`.dev/releases/current/cliEval/design-spec.md`) — shared input to both pipelines

If Pipeline B's tasklist bundle has NOT been generated yet, see **Section 3** below before proceeding to Section 4.

---

## 1. Create the two worktrees

Pick a fresh base branch from `origin/master`. Both pipelines will execute against the same starting tree so artifact differences cannot be blamed on base-state divergence.

```bash
# from the canonical repo root
git fetch origin
BASE_SHA=$(git rev-parse origin/master)
echo "Base SHA: $BASE_SHA"

# Worktree A — task-builder pipeline execution
git worktree add ../IronClaude-cliEval-A "$BASE_SHA"
cd ../IronClaude-cliEval-A
git checkout -b run/cliEval-pipelineA-$(date -u +%Y%m%dT%H%M%S)
cd -

# Worktree B — Sprint CLI pipeline execution
git worktree add ../IronClaude-cliEval-B "$BASE_SHA"
cd ../IronClaude-cliEval-B
git checkout -b run/cliEval-pipelineB-$(date -u +%Y%m%dT%H%M%S)
cd -

git worktree list
# Expect 3 entries: the main repo + the two new worktrees
```

**Why this matters:** worktrees share the `.git` object store but have independent working trees + indexes + branches. They cannot accidentally write to each other.

---

## 2. Pre-populate shared inputs into each worktree

Both pipelines need the design spec + task files (Pipeline A) or the tasklist bundle (Pipeline B). Since both worktrees check out the same base SHA, anything not yet on master must be copied in.

```bash
# Pipeline A — task files exist in the canonical repo's working tree (uncommitted on feat/hook-sync-and-matcher-fix branch).
# Copy them into the A worktree.
rsync -a ../IronClaude/.dev/tasks/to-do/TASK-RF-20260518-cliEval-P{1,2,3,4}-*/ \
        ../IronClaude-cliEval-A/.dev/tasks/to-do/

# Design spec + decisions + BUILD_REQUESTs go into BOTH worktrees as read-only context
for WT in ../IronClaude-cliEval-A ../IronClaude-cliEval-B; do
  mkdir -p "$WT/.dev/releases/current/cliEval"
  rsync -a ../IronClaude/.dev/releases/current/cliEval/{README.md,design-spec.md,decisions.md,build-requests/} \
          "$WT/.dev/releases/current/cliEval/"
done
```

**Important:** the actual `cli/eval/` source code that the task files create does NOT yet exist on either worktree. That is what the pipelines will produce.

---

## 3. (Pipeline B only — if not yet generated) Produce Pipeline B's tasklist bundle

If you have not yet run Pipeline B's generation step, do it now FROM A FRESH CHAT (not from inside either worktree's Claude Code session — Pipeline B's generation also produces artifacts at `.dev/releases/current/cliEval/`, and you want those to live in the canonical repo first, then be copied into worktree B for execution).

In the canonical repo (`../IronClaude`), open a fresh Claude Code session and run:

```
/sc:spec-panel @.dev/releases/current/cliEval/design-spec.md --mode critique --focus requirements,architecture,testing --downstream roadmap
```

Then:

```
superclaude roadmap run .dev/releases/current/cliEval/design-spec.md --output .dev/releases/current/cliEval/roadmap/
```

Then:

```
/sc:tasklist .dev/releases/current/cliEval/roadmap/ --output .dev/releases/current/cliEval/tasklist/
```

Once the tasklist bundle exists at `.dev/releases/current/cliEval/tasklist/`, copy it into worktree B:

```bash
rsync -a ../IronClaude/.dev/releases/current/cliEval/{roadmap,tasklist}/ \
        ../IronClaude-cliEval-B/.dev/releases/current/cliEval/
```

If Pipeline B's tasklist already exists on the canonical repo, skip Section 3 and go to Section 4.

---

## 4. Launch the two execution streams (parallel)

Open **two tmux panes** (or two terminal tabs). One per worktree. Each runs Claude Code in `bypassPermissions` mode against its own working tree.

### Pane 1 — Pipeline A execution

```bash
cd ../IronClaude-cliEval-A
claude --permission-mode bypassPermissions
# inside Claude Code:
/task .dev/tasks/to-do/TASK-RF-20260518-cliEval-P1-pty-isolation-gates/TASK-RF-20260518-cliEval-P1-pty-isolation-gates.md
```

When P1 finishes (frontmatter → 🟢 Done, branch + PR per Phase 7), repeat for P2, then P3, then P4. The hard merge-prereq gates in each task file enforce ordering.

**Branch naming pattern (per task file):** `feat/cliEval-P{1,2,3,4}-<slug>`. After each phase merges to master (or to the comparison branch — see Section 5 below), the next phase can start.

### Pane 2 — Pipeline B execution

```bash
cd ../IronClaude-cliEval-B
claude --permission-mode bypassPermissions
# inside Claude Code:
superclaude sprint run .dev/releases/current/cliEval/tasklist/tasklist-index.md
```

The Sprint CLI orchestrates the bundle end-to-end; one command should drive the entire Pipeline B execution (unlike Pipeline A which requires manual /task invocations per phase).

**If Sprint CLI fails on a phase:** consult the per-phase artifact under `.dev/releases/current/cliEval/tasklist/runs/<run-id>/` for the failure log. Re-run with `superclaude sprint resume <run-id>`.

---

## 5. Merge strategy decision

For a clean comparison, both worktrees should reach a "harness complete" state on their own branches. **Do not merge them to master during the comparison run** — that would conflate one pipeline's artifacts with the other.

```bash
# When Pipeline A is fully done (P1-P4 all merged into the A branch via `/task` Phase 7 commits)
cd ../IronClaude-cliEval-A
git log --oneline run/cliEval-pipelineA-... ^"$BASE_SHA"
# Expect 4 commits (one per phase) plus any fix commits

# When Pipeline B is fully done (Sprint CLI completes the bundle)
cd ../IronClaude-cliEval-B
git log --oneline run/cliEval-pipelineB-... ^"$BASE_SHA"
# Expect N commits depending on tasklist granularity
```

Both branches stay LOCAL during comparison. Push to remote only after the comparison verdict is in and you have chosen the winner (or a hybrid).

---

## 6. Monitoring the parallel runs

While both runs are executing, watch for:

```bash
# In a third pane: watch artifact growth
watch -n 30 'du -sh ../IronClaude-cliEval-A/.dev ../IronClaude-cliEval-B/.dev; echo "---"; tail -5 ../IronClaude-cliEval-A/.dev/tasks/to-do/TASK-RF-20260518-cliEval-P*/TASK-*.md 2>/dev/null | head -30'

# Detect stalls
ps -ef | grep claude | grep -v grep
# If a Claude Code process has been idle for >10 min without a notification, suspect a hang
```

If either run hangs, the worktree isolation guarantees the OTHER run is unaffected. Kill the stuck pane's Claude Code process; the other continues uninterrupted.

---

## 7. Convergence point — both runs complete

You know both pipelines are done when:

- **Pipeline A:** All 4 task files' frontmatter shows `status: "🟢 Done"`, and `git log` on `run/cliEval-pipelineA-...` has the expected commit graph
- **Pipeline B:** `superclaude sprint status <run-id>` shows COMPLETED, and the artifact tree under `.dev/releases/current/cliEval/tasklist/runs/<run-id>/` contains a `summary.md` with all phases PASSED

At that point, **stop**. Do not commit comparison artifacts into either worktree. The post-execution audit (Section 8) writes its outputs to a NEW comparison run dir in the canonical repo.

---

## 8. Hand off to the post-execution code audit

Open a fresh Claude Code session **in the canonical repo** (not in either worktree). Paste in `post-execution-audit-prompt.md` (sibling file in this directory) with template variables substituted:

```
RELEASE_ID="cliEval"
WORKTREE_A_PATH="../IronClaude-cliEval-A"
WORKTREE_B_PATH="../IronClaude-cliEval-B"
OUTPUT_DIR=".dev/releases/current/cliEval/comparison/audit-$(date -u +%Y%m%dT%H%M%S)"
```

The audit prompt drives a 7-phase comparison: code-quality audit per pipeline (parallel), e2e test suite execution per pipeline (parallel), mock + synthetic + real-world data injection, adversarial debate of the two audit reports, final delta verdict.

---

## 9. Cleanup (after the audit is complete)

```bash
# If Pipeline X won (or you have chosen a hybrid):
cd ~/github/IronClaude
git checkout master
git merge --no-ff run/cliEval-pipeline<X>-...
# OR cherry-pick specific commits into a new "winner" branch

# Remove the losing worktree
git worktree remove ../IronClaude-cliEval-<loser>

# Keep the winning worktree until master has the changes
# Then:
git worktree remove ../IronClaude-cliEval-<winner>
```

---

## 10. Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `git worktree add` fails with "already checked out" | A previous worktree wasn't removed | `git worktree list` then `git worktree remove <path>` |
| Pipeline A's P2 task starts before P1 is merged | The hard-prereq gate in the task file is missing | Re-run task-builder for that phase with the explicit `git ls-tree master` gate |
| Sprint CLI fails on first phase | Tasklist bundle malformed or path mismatch | `superclaude sprint validate <tasklist-index>` before running |
| Both worktrees write to the same `~/.claude/` cache and collide | Claude Code shares state at the user level | Set `CLAUDE_STATE_DIR=<per-worktree-path>` in each pane's environment before launching `claude` |
| Disk fills mid-run | Per-eval HOMEs (for Pipeline B's harness executions) accumulate | `--keep-home false` (default) deletes successful HOMEs; failed ones stay for post-mortem |
| The two pipelines produced ZERO overlapping source files | Pipelines diverged so heavily that there is nothing to compare | Inspect the design spec — both should reach the same `cli/eval/` target. If they didn't, that itself is a finding for the audit. |

---

## Appendix A — Quick reference: which artifacts live where

| Path | Owner | Purpose |
|---|---|---|
| `.dev/releases/current/cliEval/design-spec.md` | Shared (read-only) | Input to both pipelines |
| `.dev/releases/current/cliEval/decisions.md` | Shared (read-only) | Locked architectural decisions |
| `.dev/releases/current/cliEval/build-requests/` | Pipeline A (read-only) | task-builder inputs |
| `.dev/tasks/to-do/TASK-RF-20260518-cliEval-P{1,2,3,4}-*/` | Pipeline A | task-builder outputs (executed by `/task`) |
| `.dev/releases/current/cliEval/roadmap/` | Pipeline B | `/sc:roadmap` output |
| `.dev/releases/current/cliEval/tasklist/` | Pipeline B | `/sc:tasklist` output (executed by `superclaude sprint run`) |
| `src/superclaude/cli/eval/` | **Both** (the actual harness code produced by each pipeline — what we compare) | Output of execution |
| `tests/cli/test_eval/` | **Both** (test files produced by each pipeline) | Output of execution |
| `.dev/releases/current/cliEval/comparison/run-*/` | Comparison harness | Scoring + adversarial + final verdict |
