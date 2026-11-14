# Where should the program's coordinator session live?

## Question in one sentence
In which folder should the coordinator session run, and on which branch should its always-staged decision ledger sit?

## Why you are being asked
Nothing that hands work to a worker can start until the coordinator exists, and the coordinator cannot start until you name its home. That blocks 15 planned changes (sweep follow-ups, the observer switch, watcher changes, the observer-sweep contract note, Orchestrator v2 work). Ruling on the git safety question for PR #539 does not wait for this.

## Background you need
- The coordinator is a Claude session that keeps the decision ledger, creates worktrees with agents through Orca (the local agent-orchestration app) and starts workers. The project's rules say it must be a session "the person opened", and it must never run in the PR #539 folder.
- The ledger is a folder under `.dev/tasks/`. Project rule: that folder is always staged (added to git's index), never committed unless you ask.
- Staged files belong to a folder's index, not to a branch: if that folder later switches branch, the staged ledger goes with it.
- Your main folder `/home/coder/workspaces/IronClaude` is on the docs branch `docs/409-orca-dashboard-designs`: pushed, no open PR, no unsaved tracked changes, 21 untracked items. It is 60 commits behind master.
- Checked 2026-11-14: switching that folder to a branch made from master aborts today, because 34 untracked files there have the same paths as files on master (identical copies). Git refuses until they are moved or removed. The abort is safe.
- Orca did not answer on 2026-11-13; it must answer before any worker can start.

## Your options

### 1. A dedicated program worktree you create through Orca (recommended)
- If you pick this: you run `orca worktree create --name <name> --base-branch origin/master --agent claude --prompt "<coordinator brief>"`; that agent is the coordinator and the ledger is staged there. You also confirm that a session you launch this way and then watch counts as "person-opened".
- Upside: the ledger never moves to another branch; your main folder is untouched; nothing else shares the coordinator's folder.
- Downside: no file confirms the "person-opened" reading, so it rests on your statement; it needs Orca to be up; one more worktree on the host.

### 2. Your main folder, switched to a new program branch
- If you pick this: you move or remove the 34 blocking untracked copies, switch the main folder to a new branch from master, and open the coordinator session there yourself.
- Upside: certainly "person-opened"; it is the spec's own recommendation and matches the project's "open the main checkout" guidance; the ledger can start before Orca is back.
- Downside: while the ledger is staged, the main folder must not switch branch, take any other commit, or host your other Claude sessions; otherwise the ledger can end up on the wrong branch.

### 3. No coordinator yet
- If you pick this: you keep the ledger in your own notes; nothing is written to any branch; you are asked again when the first worker task is next.
- Upside: no move made before Orca and the "person-opened" reading are settled.
- Downside: all 15 worker tasks wait; agents cannot read your approvals from disk, so you restate them in every session.

## What the debate found
- Three advocates agreed on every point, but the points split between options 1 and 2, and the scores tied (option 1 won the tiebreak).
- Option 1 won on keeping the ledger in place and the coordinator alone in its folder; option 2 won on being certainly "person-opened".
- The debate found that option 2's branch switch currently aborts until the 34 identical copies are cleared.

## Recommendation and confidence
Option 1, with your statement that it counts as person-opened; option 2 with its three rules if you will not make that statement. Confidence 60 percent.

## If you do not answer
Option 3 applies: no coordinator starts, you keep the ledger by hand, and your ruling on the PR #539 git question goes only on its PR thread.

## What this answer does not authorize
No merge, push, PR, issue post or commit. It does not let any session create a worktree for itself, and it does not let the coordinator switch a folder's branch on its own.

## How to answer
"Q26: option 1, and yes, a session I launch through Orca and watch counts as person-opened" (or "Q26: option 2", or "Q26: option 3").
