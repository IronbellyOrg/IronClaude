# Research: Execution Safety — baseline, sync timing, commit, staging, rollback (gap-fill)

**Topic type:** Gap-fill (closes A.8 gap-detection CRITICAL/IMPORTANT findings Q1/Q3/Q4/Q5/Q6/Q8)
**Scope:** The cross-cutting execution mechanics the 4 primary research files did not cover.
**Status:** Complete
**Date:** 2026-06-28

---

## SF-1 — Step-0 baseline pre-state capture (closes Q1, IMPORTANT)

The reduction's later validations (`uv run pytest tests/cli/reflect`, `tests/swarm`, `make lint`, `ruff format --check`) re-run suites that ALSO carry **pre-existing noise** (R4: `make lint` fails on an unrelated `recommend.md` lint-architecture check; `ruff format --check src/ tests/` reports ~104 worktree-mismatch files). Without a recorded baseline, the executor cannot distinguish a pre-existing failure from a regression the reduction introduced.

**Tasklist requirement (Phase 0 item):** before any edit, capture pre-state to a sink file in the task dir, e.g. `.dev/tasks/to-do/TASK-RF-pr197-reduce-merge-20260628-205943/baseline.md`:
- `uv run pytest tests/cli/reflect tests/swarm -q` → record pass/fail/collected counts (note: this is the PRE-reduction count; `tests/cli/reflect` will legitimately change after Step 2 removes `test_inline_directive.py` + restores master `test_no_nesting_guard.py`).
- `uv run ruff format --check src/ tests/` → record the pre-existing noise file count (R4: ~104).
- `make lint` → record the pre-existing `recommend.md`/lint-architecture failure so it is not mistaken for a regression.
Every later validation item references this baseline: a result is a PASS iff it introduces **no NEW** failures in the files the reduction touched.

## SF-2 — Per-step `make sync-dev` timing (closes Q3, IMPORTANT)

`make verify-sync` checks `src/superclaude/ ↔ .claude/` parity (verified: recipe iterates `src/superclaude/skills/*/` and fails on drift). Step 3 edits `src/` (reflect SKILL.md + refs) but the user's Step-3 validation is pytest+grep only — no sync. If Step 4 runs `make verify-sync` while Step 3's `.claude/` mirror is stale, the result is ambiguous.

**Tasklist requirement:** run `make sync-dev` at the END of every `src/`-editing phase BEFORE that phase's verify-sync — specifically ADD `make sync-dev` after Step 3's edits (cheap, idempotent), even though the user's Step-3 validation is pytest+grep. Steps 1, 4, 5 already run `make sync-dev && make verify-sync` per the user's commands. NEVER edit `.claude/` directly; sync-dev regenerates it.

## SF-3 — Commit strategy (closes Q6, CRITICAL)

The spec is reduce-**then-merge**: Step 6 does `git push origin feat/rf-harness-sync`, but a push ships **commits** — and no step commits the reduction. The branch already carries the #197 content in commits (HEAD = `b01b33e3`); the reduction edits the working tree to remove/restore/reword. Those changes must be committed as a NEW commit on top before push, or the push is a no-op (or ships the un-reduced branch).

**Tasklist requirement (new item, after Step 5 validation, before Step 6 push):**
- ONE conventional commit capturing the reduction. Single-line message, e.g.:
  `git commit -m "refactor(pr197): reduce to additive subset — drop Decision-B runner/guard, reject Decision-A instance-level rewrite, retain EV-1..EV-4 + reflect_post_mode/--cli"`
  followed by the mandated `Co-Authored-By:` trailer (use `-m` twice or a single `-m` with the trailer is multi-line — INSTEAD use `git commit` with a prepared message file is multi-line; SIMPLEST single-line-safe path: `git commit -m "<subject>"` then the trailer is added by the commit template, OR accept a single-line subject-only commit). Per the no-multiline-paste rule, the executor (an agent, not the user) MAY author a multi-line message via the Bash heredoc itself — the single-line constraint applies to commands handed to the USER, not to agent-internal Bash. So the executor uses a normal `git commit -m $'subject\n\nCo-Authored-By: ...'` or a HEREDOC; that is fine inside the agent.

## SF-4 — Staging discipline + `.claude/` trap (closes Q5, IMPORTANT)

VERIFIED: `.claude/skills/sc-reflect-protocol/SKILL.md` is gitignored (`git check-ignore` → match); only `.claude/settings.json` is tracked. After `make sync-dev`, `git status` WILL show `.claude/` as untracked/ignored churn — this is EXPECTED and MUST be left unstaged.

**Positive staging list (the ONLY paths the commit stages):**
- `src/superclaude/cli/reflect/runner.py` (Step 2 restore)
- `tests/cli/reflect/test_no_nesting_guard.py` (Step 2 restore)
- `tests/cli/reflect/test_inline_directive.py` (Step 2 `git rm` — deletion already staged by `git rm`)
- `src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md` (Step 3 restore)
- `src/superclaude/skills/sc-reflect-protocol/refs/reflection-rubric.md` (Step 3 restore)
- `src/superclaude/skills/sc-reflect-protocol/SKILL.md` (Step 3 hunk surgery)
- `src/superclaude/skills/task-builder/SKILL.md` (Step 4 flip + Variant-A reword)

NOTE: `git checkout origin/master -- <path>` and `git rm <path>` BOTH stage their changes into the index immediately. The only un-staged changes after all steps are the manual `Edit`s to the two SKILL.md files → stage them explicitly by path.

**Staging requirement (hard):**
- Stage EXPLICITLY by path (`git add <the 7 paths above>`), NEVER `git add -A` / `git add .` — a blanket add risks (a) staging `.claude/` if any path slips the gitignore and (b) hijacking a concurrent session's files (see SF-5).
- If `git add` ever requires `-f` on a `.claude/` path → STOP (CLAUDE.md siren).
- Before commit: `git status --short` and confirm ONLY the 7 expected paths (+ deletion) are staged and NO `.claude/` path appears staged. `git diff --cached --name-only | grep -c '/\.claude/'` MUST be `0`.

## SF-5 — Shared-index / concurrent-session guard (closes Q4 partial, CRITICAL safety)

VERIFIED: a sibling task dir `TASK-RF-reflect-ac-hybrid-20260628-205715` exists in THIS worktree → a concurrent session may share this worktree's single git index/HEAD (memory `feedback_parallel_sessions_share_index`: HEAD SHA changed twice in 90s in a past incident).

**Tasklist requirement:**
- Do NOT `git reset --hard` or `git stash`/`stash clear` at any point (clobbers concurrent work / other sessions' stashes — memory `reference_worktree_merge_head_path`).
- Rollback is PER-FILE only: `git checkout HEAD -- <path>` restores the branch's pre-reduction version of a single file (HEAD anchor = `b01b33e3`, recorded at Step 0).
- Before the Step-SF-3 commit, re-verify HEAD is still `b01b33e3` (the recorded anchor); if HEAD moved, a concurrent session committed — STOP and reconcile rather than committing on an unexpected base.

## SF-6 — Rollback / recovery on validation failure (closes Q4, CRITICAL)

Step 3 hunk surgery on `sc-reflect-protocol/SKILL.md` is the highest-risk, most error-prone edit (R2: ~12 hunks, 9 restore + 4 retain). It needs a known-good recovery path.

**Tasklist requirement (embed in Step 3 + Step 4 items):**
- Recovery anchor for the surgery files = the branch HEAD version: `git checkout HEAD -- src/superclaude/skills/sc-reflect-protocol/SKILL.md` restores the pre-surgery (#197) state of that one file so surgery can be redone from scratch. (NOT `git checkout origin/master --` — that would drop EV-1/EV-2.)
- For the restore files (runner.py, refs, test_no_nesting_guard.py): if the wrong blob lands, re-run the exact `git checkout origin/master -- <path>` one-liner (idempotent).
- If Step-3 post-surgery greps (R2 V1–V6) FAIL: do NOT proceed to Step 4; recover the SKILL.md via `git checkout HEAD --`, re-apply the hunk map, re-validate.

## SF-7 — SKILL.md ↔ refs consistency after Step 3 (closes Q8, IMPORTANT)

Step 3 restores BOTH `refs/reviewer-spec.md` + `refs/reflection-rubric.md` (full master checkout) AND hunk-restores SKILL.md §7.1/§11.3 to master. Both come from the same master commit, so they are consistent **by construction** — but the surgery is PARTIAL (EV hunks retained), so a light post-Step-3 consistency check is warranted.

**Tasklist requirement (light check in Step 3 validation):** after surgery, confirm the restored SKILL.md does not reference a refs section/name that the restored master refs do not contain. Practically: grep the restored SKILL.md for the reviewer-spec / reflection-rubric section anchors it cites and confirm they exist in the restored refs (or simply confirm both refs now byte-match master via `git diff origin/master -- <refs>` → empty). The empty-diff check is the strongest and cheapest: `git diff origin/master -- src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md src/superclaude/skills/sc-reflect-protocol/refs/reflection-rubric.md` MUST output nothing (refs == master).

## SF-8 — Step-6 rebase-if-behind + push + auggie review (closes the Q6 push→meaningful loop)

VERIFIED earlier (R4): origin = `IronbellyOrg/IronClaude` (fork); currently `HEAD..origin/master` = 0 (no rebase needed now, but re-check at execution time since time will have passed). PR #197 OPEN, head `feat/rf-harness-sync`.

**Tasklist requirement (Step 6, single-line each):**
- `git rev-list --count HEAD..origin/master` — if `>0`, `git fetch origin && git rebase origin/master` (NOT merge; keep linear). If a rebase conflict arises in the reduction files, recover per SF-6.
- `git push origin feat/rf-harness-sync` (push the reduction commit from SF-3).
- `gh pr comment 197 --repo IronbellyOrg/IronClaude --body "auggie review"` (pushes do NOT re-trigger Augment — memory `reference_augment_review_triggers`).
- Confirm PR URL: `gh pr view 197 --repo IronbellyOrg/IronClaude --json url --jq .url` MUST print `https://github.com/IronbellyOrg/IronClaude/pull/197`.

## Summary for the builder

Add to the tasklist, beyond the user's 6 steps:
- **Phase 0** baseline-capture item (SF-1) + record HEAD anchor `b01b33e3` (SF-5).
- **`make sync-dev` after Step 3 edits** (SF-2).
- **SKILL↔refs empty-diff check** in Step 3 validation (SF-7).
- **A commit item** (SF-3 + SF-4 staging discipline) AFTER Step 5, BEFORE Step 6 push.
- **Rollback notes** (per-file `git checkout HEAD --`; no `reset --hard`/`stash`) in Steps 2/3/4 (SF-5/SF-6).
- **Step 6** rebase-if-behind + push + `gh pr comment ... auggie review` + URL assert (SF-8).
- **Broadened EV-2 grep** in Step 3 (CF-2: `ORCHESTRATOR-VERIFIES-ON-DISK\|LEGAL VALUES ARE EXACTLY\|merged-verdict.yaml`).
- **Variant-A Family-B reword** folded into Step 4 (per `adversarial-family-b/recommendation.md`).
