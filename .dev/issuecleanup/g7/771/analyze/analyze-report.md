# /sc:analyze report: src/superclaude/core/WORKER-CONTRACT.md (architecture, quick)

Codegraph: index_state=fresh, checked_at=2026-11-24T20:42:27Z; degraded: graph:empty (the contract is markdown, which codegraph does not index; Grep and Read used)

Evidence (HEAD a7ae3dd30; contract last changed in 784254002, PR 736):
- AN-1 (medium): "Issue pipeline duties" (WORKER-CONTRACT.md:292-303) ends at `issue-pipeline complete` (Completion bullet, line 302) and the Never bullet (line 303). Nothing names a post-merge step, `/sc:closeout`, `/sc:worktrees` or a `handback` recipient.
- AN-2 (medium): `/sc:closeout` appears in the contract only in the never-as-worker list (line 23). `grep closeout|sc:worktrees` over src/superclaude/cli/issue_watch, cli/issue_pipeline, skills/sc-issue-protocol and docs/designs/issue-watcher* returns nothing.
- AN-3 (low): no merged-pull-request signal in the watcher or pipeline: the only "merged" hits in cli/issue_watch and cli/issue_pipeline are an approval-event merge (reads.py:165) and a brief file name; commands/sweep.md has none.
- AN-4 (info): boundaries that stay: Full Submit "never covers a merge" (line 246); worktrees `--apply` only when the person typed it (commands/worktrees.md, lines 17-21, 38-42); contract line 238 forbids removing worktrees with unmerged commits or an open PR without the user's instruction.
- AN-5 (info): D22 (docs/designs/sc-closeout.md:78) and result schema lines 205-215 define `issue.handback: remaining`; no coordinator rule reads it.
- No contract mirror exists under plugins/ (find plugins -name 'WORKER-CONTRACT*' printed nothing).
