# Worktree review, 2026-11-22 (read-only; nothing was changed, saved, committed or deleted)

Facts come from git, gh and `orca-ide worktree list` read at about 11:40 UTC on 2026-11-22. "Unsaved" means a file that exists only in that folder (untracked, or staged but never committed). Repository roots (the main checkout of each repo) cannot be removed as worktrees.

## A. Delete now (nothing unsaved, nothing unpushed that matters)

| Worktree | Why safe |
|---|---|
| /home/coder/workspaces/worktrees/Ironbrain/ironbrain-alt-b-compose | Pull request 6 on IronbellyOrg/Ironbrain merged 2026-11-14; clean; branch pushed and in step with its remote. |
| /home/coder/workspaces/worktrees/Ironeye/main (branch ironbelly/main) | Clean; no commit that is not already on origin/main; last activity 2026-10-27. |
| /home/coder/workspaces/worktrees/IronClaude/open-decisions | Clean; its 7 commits (one 368-line file, OPEN-DECISIONS.md, 2026-11-15 and 16) are pushed to origin/ironbelly/open-decisions and no pull request exists. Deleting the folder keeps the commits on the remote branch. 84 commits behind master. Owner question: still wanted? |

## B. Delete after saving a few files

| Worktree | Unsaved | Why it is complete |
|---|---|---|
| /home/coder/workspaces/worktrees/IronClaude/issue-691-part-b | 1 untracked folder, .dev/reflect/pre-planIssue691Part-20261120204445 (3 files, not on master) | Pull request 709 merged 2026-11-20; issue 691 is closed; branch pushed and in step. |
| /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb | 6 untracked .dev folders (about 138 files: implement ledgers apply-owner-decision-r36, issue-pipeline-guard-g2, plan-b-gated-tasks; reflect reports post-zero-setup-watcher and two pre-planDecision6BFo) plus a 1-line edit to .dev/releases/backlog/issue-watcher-zero-setup/requirements.md. None of the 6 folders is on master. The release folder .dev/releases/backlog/issue-watcher-zero-setup/ is not on master either (it lives on this branch only, which is pushed). | Pull request 707 merged 2026-11-20 (the zero-setup watcher). Follow-ups already exist: issues 716, 717, 718, 722, 723; the rehearsal (X09) is running. |

## C. Complete but holds a lot of unsaved work (commit and push, or archive, before any delete)

| Worktree | Unsaved | State |
|---|---|---|
| /home/coder/workspaces/worktrees/Ironeye/feature-laminar-synthetic-pilot-2 (branch research/laminar-ironbrain-overlap-20261108) | 400 staged new files, 1 staged edit, 4 untracked folders (.claude/, .dev/eval-workspaces/, .dev/preflight/.../stack/, claudedocs/); 12 MB; no commit of its own and no remote branch | Orca says completed. Its own final review (2026-11-09) says pass, all 18 acceptance checks met. I did not re-verify the 18 checks. |
| /home/coder/workspaces/worktrees/Ironbrain/ironbrain-alt-c-agent-native | 174 staged new files; 6 MB; no remote branch | Task file status Done; RESEARCH-REPORT-agent-native-alternatives.md exists. Alternatives A and B were published as pull request 6 (B only). |
| /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp (docs/409-observer-sweep-user-docs) | 26 untracked paths: .dev/brainstorms/20261108-132433-orca-observer-mvp (760 KB), .dev/issues/409 (24 MB: visual-parity rounds, mockups, tuibbs review), .dev/issues/606 draft, 6 reflect folders, task TASK-RESEARCH-observer-visual-parity | Pull request 708 merged 2026-11-20, but issue 409 (TUI dashboard) is still open. Not finished as a whole. |

## D. In progress, keep

| Worktree | State and next step |
|---|---|
| x06-contract-wording | Pull request 724 open; 3 commits; clean; most checks green when read. Owner merges. Then delete. |
| issue-442-runbook | Issue 442 open: live observations OB-H1 (9 items), OB-H2, OB-H3, OB-CTX are not run. 36 staged new files (23 in .dev/reflect, 13 in .dev/tasks) and 1 untracked folder, none on master. Next: the X10 early probe, then record results and close 442. |
| issue-712, issue-713, issue-714, issue-715 | Disposable observation targets for issue 442 (issues 712 to 715 open). Only claim files untracked (about 7 files each; 712 also has an ob-442 folder). Keep until the X10 probe has run, then delete all four. |
| /home/coder/workspaces/worktrees/orchestrator-sandbox/Coordinator and rehearsal-r1 | Clean, at the seed commit. The rehearsal is running. Keep. |
| /home/coder/workspaces/worktrees/Coder/issue-515 | Coder issue 515 (cron in the image) open; 4 edited files and 4 untracked items not committed; branch equals main. ORCH-Coder's work; do not touch. |
| /home/coder/workspaces/worktrees/Coder/main (branch Orchestration) | ORCH-Coder's coordinator worktree; 3 untracked issue folders. Keep. |
| /home/coder/workspaces/IronClaude (ORCH-IronClaude, branch docs/409-orca-dashboard-designs) | This session. 1 commit (495eb96d1, the Orca dashboard design package) is pushed with no pull request, and the branch is 147 commits behind master. 263 staged and 53 untracked files, 37 MB in .dev/brainstorms and 36 MB in .dev/tasks/to-do. |

## E. Needs an owner answer before anything is done

| Worktree | Question |
|---|---|
| Ironbrain/ironbrain-alt-a-platforms | Task status is Blocked (the reason is in the task file's blocker_reason, not read). 122 staged new files, 21 MB, no remote branch. Resume, cancel, or save and close? |
| Coder/dashboard-bmad | Branch has no commits of its own (32 behind main); 2 untracked folders from 2026-11-08: _bmad-output/planning-artifacts/orca-observer (1.5 MB) and _bmad-output/specs/spec-orca-observer (176 KB). Idle 14 days. Keep or archive? |
| /home/coder/workspaces/Coder (root, branch feat/494-release-b) | Pull request 502 merged; 9 untracked items (232 KB: .dev/issues/477 for a closed issue, pr-monitor folders, research). It is the repo root: save the files, then switch it to main. |
| /home/coder/workspaces/Ironbrain (root, main) | 5 untracked research drafts (ANYTHINGLLM-RECHECK 2026-11-08) and .dev/brainstorms. Open Ironbrain issues 2 and 4 (open decisions) are unanswered. |

IronOrca (main, clean, 150 commits behind), Ironeye root (clean, 11 behind) and orchestrator-sandbox root (clean): nothing to do.

## F. Does /sc:worktrees (pull request 711, merged 2026-11-22 10:08 UTC) cover these questions?

Read: the pull request body and `src/superclaude/commands/worktrees.md` on origin/master, plus an outline of `scripts/worktree_cleanup.py`. I did not read the script rule by rule.

1. In progress, next steps, questions: not covered. The tool only says kept or removable, with a reason.
2. Complete, objectives met, follow-up issues: not covered. Rule 4 checks that related issues are closed, not that the objectives were met. It files nothing.
3. Cleanup and saving: partly. `archive` saves untracked and ignored .dev files to IronbellyOrg/run-evidence (exists, private) and checks the copy. It does not save staged or edited tracked files or later commits (the patch-and-bundle step is not built, per the pull request), and it never commits or pushes. A worktree with such work is kept.
4. Safe to delete: partly. Eight rules, including a merged pull request of its own (so a clean worktree with no pull request, such as Ironeye main, is kept), 7 days idle (everything from 2026-11-20 and 21 is kept until about 2026-11-27 to 28), no pin. Open problem in the pull request: while Orca runs, an unreadable Orca helper process makes every worktree that reaches rule 6 be kept and the run exit 69. A what-if run found only 5 removable worktrees, all in Coder.

Conclusion: it covers question 4 and half of 3. It does not replace this review.
