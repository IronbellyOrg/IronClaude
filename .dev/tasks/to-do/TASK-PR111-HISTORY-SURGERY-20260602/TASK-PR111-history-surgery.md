---
id: TASK-PR111-HISTORY-SURGERY-20260602
title: "PR #111 history surgery — drop 2 duplicate commits, replay tokenizer onto master, cherry-pick span-aware dedup"
status: completed
priority: high
completed: 2026-06-02
result: "Force-pushed 861047c2 → 0a6b4ac0 (2 clean commits on origin/master 35af0338). PR #111 mergeable=MERGEABLE (was DIRTY). All gates 11a-11e passed: 1733 passed/13 skipped, lint+format clean, clean FF."
branch: fix/roadmap-md-family-tokenizer-canonicalizer
remote: origin (IronbellyOrg/IronClaude)
base: origin/master
created: 2026-06-02
empirically_trialed: true
---

## Context

PR #111 (branch `fix/roadmap-md-family-tokenizer-canonicalizer`, head `861047c2`, base `master`) is DIRTY:
its branch contains two UNSQUASHED precursor commits of cleanup-audit work that already landed on master
via PR #109 (squash commit `89933922`). The precursor commits cause merge conflicts. The genuinely-new
work is a single tokenizer/canonicalizer fix commit plus a sibling-agent span-aware-dedup fix to cherry-pick.

**The three commits on the branch above master (oldest → newest):**

```
861047c2 fix(roadmap): honor M{n}-D{nn} milestone-prefixed IDs in tokenizer + canonicalizer   ← KEEP (replay)
bf82b257 docs(sc:cleanup-audit): refresh CHANGELOG + report templates for new default excludes ← DROP (in #109)
9ea8be21 feat(sc:cleanup-audit): bake hidden + BMAD scope exclusions into defaults             ← DROP (in #109)
```

**Cherry-pick target (sibling branch `fix/pr111-spec-parser-span-aware-dedup`):**

```
cc08825e fix(roadmap/spec_parser): span-aware D-id dedup ... addresses augmentcode #111  (parent = 861047c2)
```

### Ground truth established (verified, not assumed)

- `git show --stat` confirms `9ea8be21` + `bf82b257` are cleanup-audit-protocol files (REPORT.md, reviewer-cards,
  CHANGELOG.md, `sc-cleanup-audit-protocol/{SKILL.md,rules,scripts/repo-inventory.sh,templates}`,
  `commands/cleanup-audit.md`). `89933922` (#109) is their squash-merge — same logical change, slightly different
  final form (it also added `tests/skills/test_repo_inventory_nongit.py` and 53 vs 42 line `repo-inventory.sh`
  delta). Dropping them keeps master's authoritative version. CONFIRMED equivalent-in-intent, superseded by master.
- `861047c2` touches ONLY: `KNOWLEDGE.md`, `src/superclaude/cli/roadmap/spec_parser.py`,
  `src/superclaude/cli/roadmap/structural_checkers.py`, `tests/roadmap/test_structural_checkers.py`.
  It does **NOT** touch `repo-inventory.sh`.

### CRITICAL DISCREPANCY vs the prior audit's prescribed resolution

The prior audit (which merged the WHOLE branch including the duplicate commits) prescribed resolving
`src/superclaude/skills/sc-cleanup-audit-protocol/scripts/repo-inventory.sh` → take master's version.
**Under the DROP/replay approach that conflict DOES NOT EXIST.** `repo-inventory.sh` is only touched by the
dropped commits, so once they are dropped it is never in the changeset. **EMPIRICALLY VERIFIED in trial:** the
only conflict during the replay is `KNOWLEDGE.md`. `spec_parser.py`, `structural_checkers.py`, and
`test_structural_checkers.py` apply cleanly. **Do NOT attempt to resolve repo-inventory.sh — there is nothing to
resolve.**

### Empirical trial result (disposable worktree, discarded)

- `git rebase --onto origin/master bf82b257 <branch>` replayed only `861047c2` → new sha; both precursors dropped.
- Single conflict: `KNOWLEDGE.md` (end-of-file; both master #110 and `861047c2` append an entry). Resolved as
  union (keep both entries, `---`-separated).
- `git cherry-pick cc08825e` applied **cleanly, no conflict** (master never touches `spec_parser.py`).
- `git merge-base --is-ancestor origin/master HEAD` → exit 0 (clean fast-forward; branch exactly 2 commits ahead).
- `uv run pytest tests/roadmap/ -q` → **1733 passed, 13 skipped**.
- `uv run ruff check src/ tests/` → All checks passed.
- `uv run ruff format --check` → **`spec_parser.py` would be reformatted** (one missing blank line). Root cause:
  PRE-EXISTING in `cc08825e` itself (the sibling commit), NOT introduced by the merge. Requires a `ruff format`
  + `--amend` step after the cherry-pick (see checklist item 9).

### Safety

- No git worktree currently holds `fix/roadmap-md-family-tokenizer-canonicalizer` (verified via `git worktree list`).
- No in-flight work depends on the OLD `861047c2` sha. The sibling `fix/pr111-spec-parser-span-aware-dedup` branch
  is the cherry-pick SOURCE only; it is not consumed/mutated.
- Uncommitted work in the main checkout is the unrelated octocode-investigation backlog deletions; it does not
  touch any file in this surgery. Do the surgery on a **fresh worktree or a clean checkout of the target branch**.
- History rewrite → `git push --force-with-lease` is required and safe here (single-author PR branch, no shared
  downstream).

## Pre-surgery rollback anchor

Before doing anything destructive, record the current remote tip:

- **Pre-surgery target tip:** `origin/fix/roadmap-md-family-tokenizer-canonicalizer` = `861047c2`
- **Rollback:** if anything goes wrong before the force-push, `git reset --hard 861047c2` (or
  `git checkout fix/roadmap-md-family-tokenizer-canonicalizer && git reset --hard origin/fix/roadmap-md-family-tokenizer-canonicalizer`).
- **Post-push rollback:** the force-pushed-over sha `861047c2` is still recoverable from `git reflog` / the PR's
  pre-push commit; `git push --force-with-lease origin 861047c2:fix/roadmap-md-family-tokenizer-canonicalizer`
  restores it if needed.

## Execution checklist (execute in order; each item is a single-line bash command unless noted)

- [ ] 1. Fetch latest refs: `git fetch origin`
- [ ] 2. Confirm remote tip is still `861047c2` (lease anchor): `git rev-parse origin/fix/roadmap-md-family-tokenizer-canonicalizer` — MUST print `861047c233fbd7728e8c055f96c2a7e7840b4894`. If it differs, STOP — someone moved the branch; re-trial before proceeding.
- [ ] 3. Create an isolated surgery worktree at the branch head: `git worktree add /tmp/pr111-surgery --detach 861047c2`
- [ ] 4. Enter it and create a working branch off the head: `git -C /tmp/pr111-surgery checkout -b pr111-surgery 861047c2`
- [ ] 5. Replay only the tokenizer commit onto master, dropping both precursors: `git -C /tmp/pr111-surgery rebase --onto origin/master bf82b257 pr111-surgery` — this WILL stop with a `KNOWLEDGE.md` conflict (expected; the ONLY conflict).
- [ ] 6. Resolve the `KNOWLEDGE.md` conflict as a **union of both additive entries**. The conflict is at end-of-file: the HEAD side is master's obligation_scanner entry (`## obligation_scanner Layer 2 vs Layer 5 surface overlap ...`), the incoming side is the new tokenizer entry (`## 2026-05-31: Roadmap Spec-Fidelity Validator — M{n}-D{nn} ...`). Keep BOTH, in order: HEAD entry first, then a `---` separator line, then the tokenizer entry. Delete all three conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`). Verify zero markers remain: `grep -c -E '^(<<<<<<<|=======|>>>>>>>)' /tmp/pr111-surgery/KNOWLEDGE.md` MUST print `0`.
- [ ] 7. Stage and continue the rebase: `git -C /tmp/pr111-surgery add KNOWLEDGE.md && GIT_EDITOR=true git -C /tmp/pr111-surgery rebase --continue`
- [ ] 8. Cherry-pick the span-aware dedup fix (applies cleanly, no conflict expected): `git -C /tmp/pr111-surgery cherry-pick cc08825e`
- [ ] 9. **Format gate fix (required — `cc08825e` ships a pre-existing format violation).** Apply ruff format and amend it into the cherry-pick: `cd /tmp/pr111-surgery && uv run ruff format src/superclaude/cli/roadmap/spec_parser.py && git -C /tmp/pr111-surgery add src/superclaude/cli/roadmap/spec_parser.py && git -C /tmp/pr111-surgery commit --amend --no-edit`
- [ ] 10. **`make sync-dev` gate.** This surgery touches NO `src/superclaude/{skills,commands,agents}` file (only `cli/roadmap/*.py`, `tests/`, `KNOWLEDGE.md`), so `sync-dev` is a no-op here — but run `git -C /tmp/pr111-surgery status --short` to CONFIRM no `src/superclaude/skills|commands|agents` path was modified. If (unexpectedly) one was, run `make sync-dev` from `/tmp/pr111-surgery` and stage only `src/` side; NEVER stage `.claude/` paths.
- [ ] 11. **VERIFICATION GATE — all must pass before the force-push:**
  - [ ] 11a. Tests green: `cd /tmp/pr111-surgery && uv run pytest tests/roadmap/ -q` — expect `1733 passed, 13 skipped` (or strictly ≥ that pass count, 0 failures).
  - [ ] 11b. Lint clean: `cd /tmp/pr111-surgery && uv run ruff check src/ tests/` — expect `All checks passed!`.
  - [ ] 11c. Format clean (touched files — matches what the trial verified): `cd /tmp/pr111-surgery && uv run ruff format --check src/superclaude/cli/roadmap/spec_parser.py src/superclaude/cli/roadmap/structural_checkers.py tests/roadmap/test_structural_checkers.py tests/roadmap/test_spec_parser.py` — expect `4 files already formatted`. (Whole-tree `ruff format --check src/ tests/` was confirmed clean on master at plan time — 693 files already formatted — so a whole-tree check is also expected to pass; scoping to the 4 touched files keeps this gate immune to any unrelated pre-existing format drift that might land on master before execution.)
  - [ ] 11d. Fast-forward relationship: `git -C /tmp/pr111-surgery merge-base --is-ancestor origin/master HEAD; echo $?` — MUST print `0` (origin/master is an ancestor → clean FF into master).
  - [ ] 11e. Exactly the intended commits: `git -C /tmp/pr111-surgery log --oneline origin/master..HEAD` — MUST show exactly 2 commits: the span-aware dedup fix (tip) and the tokenizer fix. NO cleanup-audit / `bf82b257` / `9ea8be21` content.
- [ ] 12. **DESTRUCTIVE STEP — force-push with lease (only after 11a–11e all pass).** `git -C /tmp/pr111-surgery push --force-with-lease=fix/roadmap-md-family-tokenizer-canonicalizer:861047c233fbd7728e8c055f96c2a7e7840b4894 origin HEAD:fix/roadmap-md-family-tokenizer-canonicalizer` — the explicit lease sha guarantees the push aborts if the remote moved since step 2.
- [ ] 13. **Post-push verification.** `git fetch origin && git log --oneline origin/fix/roadmap-md-family-tokenizer-canonicalizer -3` — confirm the new 2-commit history is on the remote. Then confirm PR #111 is now mergeable: `gh pr view 111 --repo IronbellyOrg/IronClaude --json mergeable,mergeStateStatus` — **success criterion is `mergeable: MERGEABLE`** (conflicts gone). `mergeStateStatus` MAY still be `UNSTABLE` due to 57 PRE-EXISTING `tests/sprint/test_tui_monitor.py` + `test_watchdog.py` failures that are orthogonal to this PR (flagged by the CI-fix agent; PR #117 already fixed the `invoke_haiku` breakage but not these). UNSTABLE-from-those is NOT a surgery failure. The surgery's own gate is 11a (green `tests/roadmap/`) + 11d (clean FF) — both already passing.
- [ ] 14. **Cleanup.** Remove the surgery worktree: `cd /config/workspace/IronClaude && git worktree remove /tmp/pr111-surgery --force`. Optionally delete the sibling branch once its commit is confirmed in #111: leave `fix/pr111-spec-parser-span-aware-dedup` for the human to delete.

## ABSOLUTE RULES (binding during execution)

- FORK only: `origin` = `IronbellyOrg/IronClaude`. NEVER push `upstream` / `SuperClaude-Org`. Any `gh` PR op uses `--repo IronbellyOrg/IronClaude`.
- NEVER commit to master. NEVER stage `.claude/` paths (only `.claude/settings.json` is ever trackable, and it is not in scope here).
- UV only for tests/lint (`uv run pytest`, `uv run ruff`).
- Single-line bash; no heredocs / multi-line quoted strings.
- The force-push (step 12) is the ONLY destructive action and is gated behind 11a–11e.

## Notes / open items for the executor

- The `KNOWLEDGE.md` union in step 6 may be done by hand or with a small `uv run python` one-liner; either is fine as long as step 6's marker-count check passes and both entries survive verbatim.
- If `cc08825e` ever stops applying cleanly (e.g., master gains a `spec_parser.py` change before execution), STOP and re-trial — do not force a resolution blind.

## Post-debate updates (orchestrator review, 2026-06-02)

- **Master-drift risk empirically NULLIFIED at review time.** `git log 861047c2..origin/master -- src/superclaude/cli/roadmap/spec_parser.py src/superclaude/cli/roadmap/structural_checkers.py` returns EMPTY → master (now `35af0338`, post-#115) has NOT touched either file since the base. The trial ran against this same master tip, so the clean cherry-pick (step 8) is guaranteed, not assumed. The step-2 lease check + step-8 re-trial guard remain as defense against drift between review and execution.
- **PR #117 (master CI fix) is MERGED.** The repo-wide `invoke_haiku`→`invoke_sonnet` ImportError that reddened all PRs is resolved on master. After this surgery, `tests/roadmap/` is green (11a) and the sprint-import breakage is gone; the only residual CI red is the 57 pre-existing TUI/watchdog failures (orthogonal — see step 13).
- **Post-merge follow-ups (NOT part of this surgery; do after #111 merges):**
  1. Resolve augmentcode review thread `databaseId 3334998823` (the span-aware dedup finding) — the fix is now in #111 via the cherry-pick.
  2. Delete the now-redundant sibling branch `fix/pr111-spec-parser-span-aware-dedup` (its sole commit `cc08825e` is folded into #111).
