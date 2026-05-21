# R3 — Integration Points (Branch Lineage + Merge Conflicts + Stale Branches)

**Task**: TASK-RF-20260518-181333 (Branch QA + commit + PR workflow for `feat/hook-sync-and-matcher-fix`)
**Researcher**: R3 of 7
**Scope**: Git topology — branch refs, merge bases, merge-tree conflict prediction, stale branch identification, sub-branch recommendations, manifest path bug
**Status**: Complete

---

## 1. Integration Branch Existence — VERDICT: DOES NOT EXIST

**Local refs** (`git branch -a | grep -i integration`):
```
(no output, exit 1)
```

**Branch config** (`git config --get-regexp "^branch\." | grep -i integration`):
```
(no output, exit 1)
```

**Remote** (`git ls-remote origin | grep integration`):
- No `refs/heads/integration` on origin. Only `refs/heads/master` + many `refs/heads/feat/*`, `refs/heads/chore/*`, `refs/heads/fix/*`, plus closed `refs/pull/*/head` refs.

**CI / docs references**:
- `.github/workflows/test.yml`: `branches: [master, integration]` (push + pr triggers)
- `.github/workflows/quick-check.yml`: `branches: [master, integration]`
- `.github/workflows/README.md`: documents `master` or `integration` as triggers
- The CI is configured to *accept* an integration branch but no such branch was ever created on this repo.

**Conclusion**: The `master ← integration ← feature/*` model documented in `CLAUDE.md` "Git Workflow" section is **aspirational only**. Actual repo practice (visible via merged PRs #47, #48, #49) is **`master ← feat/*` directly via squash-merge PRs**. The PR plan for `feat/hook-sync-and-matcher-fix` MUST target `master` directly. CI workflows on `integration` branch never fire (the branch does not exist).

---

## 2. Merge-Base & Conflict Prediction Against `master`

### 2.1 Topology

| Ref | SHA | Notes |
|---|---|---|
| `HEAD` (feat/hook-sync-and-matcher-fix) | `efaa33d` | current branch tip |
| `master` (local) | `516bb46` | identical to merge-base — **local master is stale** |
| `origin/master` | `ff99449` | actual integration target — 3 commits ahead of local master |
| `origin/feat/hook-sync-and-matcher-fix` | `efaa33d` | identical to HEAD — **no unpushed commits** |
| merge-base(`HEAD`, `master`) | `516bb46` | i.e., merge-base = local master tip |
| merge-base(`HEAD`, `origin/master`) | `516bb46` | i.e., branch diverged BEFORE origin/master moved |

### 2.2 Master has moved 3 commits since branch point

`git log --oneline 516bb46..origin/master`:
```
ff99449 feat(hooks): widen auggie-flag-clear matcher and add verify-sync hook coverage (#49)
c18879c chore(tasks): triage and archive 22 completed task tracks to done/ (#48)
9574788 fix(hooks): widen auggie-flag-clear matcher to include mcp__auggie-mcp__* (#47)
```
- PR #47 (`9574788`): hooks fix — 2 files (`hooks.json` + `auggie-flag-clear.sh`)
- PR #48 (`c18879c`): task triage — 667 files, all renames `.dev/tasks/to-do/ → done/`
- PR #49 (`ff99449`): hooks + task-builder MIG-002..MIG-006 + tests — **805 files, +22,881/-139 lines**

### 2.3 Branch has 15 commits + uncommitted modifications

`git log --oneline 516bb46..HEAD | wc -l` → **15 commits ahead**
`git diff --stat origin/master...HEAD` → **143 files changed, +22,994/-155 lines**

Note: branch's 143 files vs origin/master's 805 files means **138 of branch's 143 files OVERLAP with origin/master's PR #49 changes**. The branch contains a near-superset of PR #49's content, since PR #49 cherry-picked from this same line of work then squash-merged ahead.

### 2.4 Live merge-tree test (worktree at origin/master)

Performed in isolated worktree `/tmp/merge-test-hooksync` (since cleaned up):
```
$ git merge --no-commit --no-ff feat/hook-sync-and-matcher-fix
Auto-merging .claude/agents/rf-qa-qualitative.md
Auto-merging .claude/agents/rf-qa.md
Auto-merging .claude/skills/task-builder/SKILL.md
Auto-merging src/superclaude/agents/rf-qa-qualitative.md
Auto-merging src/superclaude/agents/rf-qa.md
Auto-merging src/superclaude/skills/task-builder/SKILL.md
Auto-merging tests/cli/test_verify_sync_hooks.py
CONFLICT (add/add): Merge conflict in tests/cli/test_verify_sync_hooks.py
Automatic merge failed; fix conflicts and then commit the result.
```

### 2.5 Conflict inventory

**EXACTLY ONE FILE** carries a real conflict against `origin/master`:

| File | Conflict type | Severity | Resolution path |
|---|---|---|---|
| `tests/cli/test_verify_sync_hooks.py` | add/add (both sides added the file independently) | LOW — docstring-only divergence at lines 128–144 | Keep branch version (it supersedes master's "test will fail until OQ-2/OQ-3 fixed" note with an "OQ-2/OQ-3 now resolved" note that describes the actual landed state) |

Six other files auto-merged cleanly (no manual intervention needed):
- `.claude/agents/rf-qa-qualitative.md`
- `.claude/agents/rf-qa.md`
- `.claude/skills/task-builder/SKILL.md`
- `src/superclaude/agents/rf-qa-qualitative.md`
- `src/superclaude/agents/rf-qa.md`
- `src/superclaude/skills/task-builder/SKILL.md`

**Conflict region preview** (`tests/cli/test_verify_sync_hooks.py` lines 128–144):
- HEAD (origin/master) docstring says: "This test will fail until the auggie-bash-gate.sh sync-orphan and reject-workspace-writes.sh installer-orphan are resolved per release-spec §6 / Open Questions OQ-2 / OQ-3."
- Branch docstring says: "OQ-2 (auggie-bash-gate.sh sync-orphan) was resolved on 2026-05-18 via ARCHIVE-then-DELETE… OQ-3 (reject-workspace-writes.sh installer-orphan) was resolved on 2026-05-18 by adding reject-workspace-writes.sh to _FRESHNESS_SCRIPTS… With both OQs resolved, this test should now PASS on a clean tree."

Branch wins — it reflects the actual remediation state (commit `efaa33d` "chore(hooks): resolve OQ-2 and OQ-3").

**Cleanup performed**: `git merge --abort` + `git worktree remove --force /tmp/merge-test-hooksync` (verified — current worktree list shows only the canonical workspace).

### 2.6 Overall conflict risk

**LOW**. One docstring conflict, deterministic resolution (take branch). No code-logic conflicts. No data-flow conflicts. No build-system conflicts.

---

## 3. Stale Local Branches — Cleanup Recommendations

For each non-current local branch, `git log --oneline <branch> --not feat/hook-sync-and-matcher-fix`:

| Local branch | Unique commits vs HEAD | Status | Recommendation |
|---|---|---|---|
| `master` | 0 | identical to merge-base (`516bb46`); origin/master is 3 commits ahead | `git fetch && git branch -f master origin/master` (fast-forward local master to track upstream) |
| `chore/task-cleanup-20260517` | 1 (`c9c35c3` — task triage) | content-identical to merged PR #48 (`c18879c`); diffstat matches (667 files, +110 lines) — **superseded** | **Delete: `git branch -D chore/task-cleanup-20260517`** |
| `chore/task-merge-consolidate-roadmap-to-release` | 1 (`c1c1447` — consolidate docs/docs-product/tech/task-merge → roadmap) | NOT obviously merged into master or current branch — appears to be an orphan PR-style branch | **Investigate before delete** — need R1's file inventory to confirm whether its 1 commit is needed; if `git log origin/master..chore/task-merge-consolidate-roadmap-to-release` shows the commit is also missing from origin/master, this branch is pending PR work that should either be (a) PR'd separately or (b) deleted if stale |
| `feat/mig-002-execution-context-header` | 0 | fully merged into current branch (commits `2648be8` MIG-002 + `79644fa` D-0025 evidence both present on HEAD) | **Delete: `git branch -D feat/mig-002-execution-context-header`** |
| `fix/auggie-flag-clear-mcp-prefix` | 2 (`f9a7e34` fix + `adb7d36` regression test, 175 lines) | `f9a7e34` is content-identical to merged PR #47 (`9574788`); `adb7d36` adds `tests/hooks/test_auggie_flag_clear_mcp_prefix.py` (175 lines) — **NOT YET MERGED anywhere** (not in current HEAD's `tests/hooks/`, not in origin/master's `tests/hooks/`) | **DO NOT DELETE YET** — `adb7d36` is unique work. Either (a) cherry-pick onto current branch / new sub-branch before deleting, or (b) raise as separate PR. PR #49 description explicitly promised "Regression test coverage for the mcp__auggie-mcp__* path will land with Parts 1+3 of the bundled release" — this is the missing test suite |

### 3.1 Critical preservation note

`fix/auggie-flag-clear-mcp-prefix@adb7d36` contains **`tests/hooks/test_auggie_flag_clear_mcp_prefix.py`** (175 lines) that is not present in:
- current HEAD's `tests/hooks/` (only `__init__.py`, `test_auggie_first.py`, `test_freshness_pre_edit_create_case.py`)
- origin/master's `tests/hooks/` (same three files only)

This test file should be cherry-picked into the hooks sub-branch (see §5 below) before deleting `fix/auggie-flag-clear-mcp-prefix`.

---

## 4. Remote Refs Status

`git rev-parse` results:
- local HEAD = `efaa33d`
- `origin/feat/hook-sync-and-matcher-fix` = `efaa33d`

**Local branch fully pushed; remote tracking branch is up to date.** No unpushed commits, no force-push pressure.

Origin also has many other `feat/*` branches (none named `integration`):
```
refs/heads/feat/3.7-task-unified-v2
refs/heads/feat/confidence-check-trigger-surface
refs/heads/feat/freshness-auggie-closeout
refs/heads/feat/freshness-system
refs/heads/feat/install-auggiemcp
refs/heads/feat/recommend-v2
refs/heads/feat/roadmap-spec-fidelity-fix
… (etc., ~16 stale-looking feature branches on origin)
```

These remote branches are outside this task's scope but should be flagged for a separate `git remote prune origin` + branch retirement audit.

---

## 5. Sub-Branch Recommendation Matrix

R1 owns the authoritative file-grouping inventory; R3 contributes the **branching topology** and per-group anticipated rebase conflicts. Coordinate logical groups (presumed from `.dev/releases/current/` directory structure + commit messages):

| Sub-branch | Branch from | Cherry-pick scope | Anticipated rebase conflicts onto origin/master |
|---|---|---|---|
| `fix/hooks-mcp-prefix-and-verify-sync` | `origin/master` | (a) `efaa33d` ("chore(hooks): resolve OQ-2 and OQ-3"); (b) `5439ea1` ("feat(hooks): widen auggie-flag-clear matcher to mcp__auggie-mcp__; verify-sync hook coverage; cross-consistency checks"); (c) cherry-pick `adb7d36` from `fix/auggie-flag-clear-mcp-prefix` for regression tests | The single `tests/cli/test_verify_sync_hooks.py` docstring conflict identified in §2.5 |
| `feat/task-builder-merge-mig-002-through-006` | `origin/master` | The 13 task-builder commits from the branch: `2648be8`..`87c8254` (MIG-002..MIG-006 implementation, tests, docs) | None expected on `src/superclaude/skills/task-builder/SKILL.md` if rebased after PR #49 already merged the MIG-002 portion (origin/master `ff99449` already contains MIG-002 content from PR #49's squash). **Risk**: MIG-002 may already be on master via #49 — cherry-pick will fail or produce empty diff. Verify with `git diff origin/master..2648be8 -- src/superclaude/skills/task-builder/SKILL.md` before cherry-picking |
| (optional) `chore/sprint-runner-c1-c4` | `origin/master` | If R1 identifies sprint-runner CLI fixes among uncommitted modified files (e.g., `src/superclaude/cli/sprint/checkpoints.py` TASKLIST_ROOT bug, see §6), branch this from origin/master with only those files | Depends on R1's grouping; expected low — sprint CLI was not touched on master since branch point |

**Author's recommendation**: Given (1) origin/master `ff99449` already absorbed MIG-002 content via PR #49 squash, (2) the branch's task-builder commits (MIG-003 through MIG-006) build on MIG-002 internally, and (3) only ONE small conflict exists for the whole branch — **the simplest, lowest-risk path is a single PR** of `feat/hook-sync-and-matcher-fix → master` with the single docstring conflict resolved during the PR. Splitting into sub-branches adds cherry-pick risk for marginal review-clarity gain.

If the team insists on sub-branches for review hygiene, the **`fix/hooks-mcp-prefix-and-verify-sync` sub-branch is the only one with truly independent scope** — the task-builder MIG-003..MIG-006 work shares a SKILL.md baseline with the hooks branch and is harder to cleanly isolate.

---

## 6. Manifest Path Bug — Informational (NOT a Blocker)

**File**: `/config/workspace/IronClaude/.dev/releases/current/task-builder-merge/manifest.json` (179 lines)

**Bug**: All 21 entries report `expected_path` containing the literal substring `TASKLIST_ROOT/checkpoints/`:
```json
"expected_path": "/config/workspace/IronClaude/.dev/releases/current/task-builder-merge/TASKLIST_ROOT/checkpoints/CP-P01-T01-T05.md"
```

**Actual checkpoint location**: `/config/workspace/IronClaude/.dev/releases/current/task-builder-merge/checkpoints/` (no `TASKLIST_ROOT` segment). Directory exists and contains 18 of the 21 expected checkpoints:
```
CP-P02-END.md, CP-P02-T01-T05.md, CP-P03-END.md, CP-P03-T01-T05.md, CP-P03-T07-T11.md,
CP-P04-END.md, CP-P04-T01-T05.md, CP-P04-T07-T11.md, CP-P05-END.md, CP-P05-T01-T05.md,
CP-P05-T07-T11.md, CP-P06-END.md, CP-P06-T01-T05.md, CP-P06-T07-T11.md, CP-P07-END.md,
CP-P07-T01-T05.md, CP-P07-T07-T11.md, CP-P07-T13-T17.md
```
(Missing: `CP-P01-T01-T05.md`, `CP-P01-T07-T11.md`, `CP-P01-END.md` — Phase 1 checkpoints. R6 should confirm whether Phase 1 was actually executed or was a no-op.)

**Root cause** — templating leak in `src/superclaude/cli/sprint/checkpoints.py`:

The sprint-runner reads `Checkpoint Report Path:` lines from phase files via `extract_checkpoint_paths(phase_file, release_dir)` (line 36–86). The function does:
```python
candidate = Path(raw_path)
if candidate.is_absolute():
    resolved = candidate
elif candidate.exists():
    resolved = candidate.resolve()
else:
    resolved = (release_dir / candidate).resolve()
```

**No `TASKLIST_ROOT` substitution occurs.** Meanwhile, phase files such as `phase-1-tasklist.md` contain literal `TASKLIST_ROOT/checkpoints/CP-P01-T01-T05.md` paths inherited from the template at `src/superclaude/skills/sc-tasklist-protocol/templates/index-template.md` line 41 (`| Checkpoint Reports | TASKLIST_ROOT/checkpoints/ |`).

Result: `release_dir / "TASKLIST_ROOT/checkpoints/CP-P01-T01-T05.md"` → `<release>/TASKLIST_ROOT/checkpoints/CP-P01-T01-T05.md` → never exists → all 21 entries report `"exists": false`.

**Fix scope** (out of scope for this task but documented for PR description): one of
- (a) sc-tasklist-protocol templates substitute `TASKLIST_ROOT` with the release path at tasklist generation time
- (b) `extract_checkpoint_paths` performs `raw_path.replace("TASKLIST_ROOT", str(release_dir))` before the `Path(raw_path)` construction
- (c) tasklist generator emits resolved absolute paths in phase files at sprint init

**Impact for PR description**: the task-builder-merge manifest showing 0/21 checkpoints "found" is a **path-resolution bug, not actual missing work**. 18/21 checkpoint files physically exist on the branch under `.dev/releases/current/task-builder-merge/checkpoints/` and were committed by the task-builder MIG-003..MIG-006 commits. Reviewers reading the manifest should not interpret the `"summary": { "missing": 21 }` as evidence of incomplete work.

This bug is not in scope for the current PR — it pre-exists this branch in the sprint runner code paths.

---

## Summary — Key Decisions Surfaced

1. **No integration branch exists** anywhere (local, remote, config). CI workflows on `integration` are dead code. **PR target = `master` directly.**

2. **Branch is fully pushed to origin** (`efaa33d` == `origin/feat/hook-sync-and-matcher-fix`); no force-push needed for PR creation, just `gh pr create`.

3. **Origin/master is 3 commits ahead** of local master (PRs #47, #48, #49). Local master should be fast-forwarded before any rebase work: `git fetch && git branch -f master origin/master`.

4. **Conflict surface against `origin/master` is exactly one file** (`tests/cli/test_verify_sync_hooks.py`) — a small docstring-only `add/add` conflict at lines 128–144. Branch version wins (reflects actual OQ-2/OQ-3 remediation state). Verified live via worktree merge test (cleaned up).

5. **Stale local branches safe to delete**: `chore/task-cleanup-20260517` (= merged PR #48), `feat/mig-002-execution-context-header` (0 unique commits vs HEAD).

6. **`fix/auggie-flag-clear-mcp-prefix` MUST NOT BE DELETED YET** — contains unique commit `adb7d36` adding `tests/hooks/test_auggie_flag_clear_mcp_prefix.py` (175 lines) that exists nowhere else. Cherry-pick into the hooks sub-branch (or current branch) before deletion.

7. **`chore/task-merge-consolidate-roadmap-to-release`** has 1 unique commit (`c1c1447`) — needs R1 file-inventory cross-check before disposition decision.

8. **Recommended PR strategy**: single PR `feat/hook-sync-and-matcher-fix → master` with the docstring conflict resolved at PR time. Sub-branch splitting adds cherry-pick risk for marginal gain because PR #49 already absorbed the MIG-002 baseline.

9. **Manifest `TASKLIST_ROOT` bug is informational only** — pre-existing sprint-runner templating leak. Flag in PR description so reviewers don't misread `manifest.json` as evidence of missing work. Real fix lives outside this branch's scope.
