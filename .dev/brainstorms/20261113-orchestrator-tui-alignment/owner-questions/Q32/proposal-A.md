# Proposal A: No standing rule; decide each Task's commit when that worker is dispatched

## Answer

Not as a standing rule. Each time the coordinator dispatches a code-changing worker, it asks the owner whether that one Task may end with a local commit, and if the owner says yes, the owner's own words for that Task are quoted in the brief and recorded as that Task's commit grant; without a yes, that worker leaves its changes uncommitted.

## What happens next if the owner picks it

- The ledger records Q32 = "per Task, ask at dispatch". No commit row exists yet.
- At each dispatch of a code-changing worker (up to nine Tasks: SW-07, SW-08, SW-10, SW-14, OB-06, OB-07, WA-01, WA-03, XC-07), the coordinator asks one plain question, for example: "Task OB-06: may the worker make one local commit at the end, in its own worktree, without pushing?"
- If yes, the owner's reply is quoted word for word in that Task's brief and written as `GRANT(<item>,commit)` with the date; the grant ends at that Task's `worker_done` (`WORKER-CONTRACT.md:244`).
- If no or no reply, the worker leaves its changes uncommitted, and the PR session commits named paths later (spec 6.4 rule 14).

## What it unlocks

- Meets WC-9's wording at its strictest: the quoted text is the owner's own instruction "for that Task" (`WORKER-CONTRACT.md:42`), so the brief guard has nothing to doubt.
- Lets the owner use a commit where it helps (a large or risky change worth a checkpoint before the PR session takes over) and skip it where it does not.
- No standing permission sits in the ledger that could be reused for a Task the owner never thought about.

## What it costs or risks

- Up to nine more owner questions, during a program whose stated bottleneck is owner latency ("Owner latency is the real schedule", spec line 523). A dispatch can wait on the answer.
- Two commit paths in one program (some Tasks committed by the worker, some by the PR session), so the PR session and the coordinator must check which applies in each worktree.
- If a worker commit happens, the commit-before-push review rule applies (`WORKER-CONTRACT.md:244`), adding a show-the-person step before the PR session pushes.

## What stays unresolved

- What makes a Task "worth" a commit; the owner judges each time.
- Whether a `worker-start` worktree counts as the "child worktree created by Orca" that WC-9 requires (UNVERIFIED).
