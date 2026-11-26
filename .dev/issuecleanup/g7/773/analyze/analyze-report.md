# /sc:analyze report: src/superclaude/skills/sc-issue-protocol/ (focus architecture, depth quick)

Run: 2026-11-24T20:44:08Z, HEAD a7ae3dd30, worktree Issuecleanup. Static pass (Grep/Read/gh read-only); no code changed.

Codegraph: index_state=fresh, checked_at=2026-11-24T20:44:08Z; degraded: graph:unlisted (status checked once; lookups were done with Grep/Read, no graph rows cited)

## Findings (architecture)
1. [Info] The skill has three scripts only: `scripts/clickup_claim.py`, `orca_worktree.py`, `origin_repo.py`. No Project-field, label-apply or Approved helper exists.
2. [Info] Only Project-field writer in src/: `src/superclaude/cli/issue_pipeline/complete.py:124` (`updateProjectV2ItemFieldValue`, Status to In review). The watcher reads the Pipeline field (`cli/issue_watch/github.py:109`) but nothing writes it.
3. [Info] Create never assigns: `refs/create.md:97` "No self-assignment". Claim assigns `@me` (`SKILL.md:87`, `refs/claim.md:48`).
4. [Info] Boundary: `commands/issue.md:102-103` "Will Not: create labels... Write any issue field other than Complexity". Any setup feature must change this contract.
5. [Note] Name clash: `--pipeline` on `/sc:issue --claim` (commands/issue.md:43) is the launch level (worktree/full/none), not the Project "Pipeline" field the watcher reads. A setup feature needs a different flag name.
6. [Info] `cli/issue_watch/repo_init.py` creates the trigger label on the repo only (`ensure_trigger_label`), never applies it to an issue.

## Recommendation
No change until the owner answers issues 722 and 698 (identity and approver rule). Then add a setup helper under `scripts/`, keep watcher code unchanged.
