# Proposal C: Yes. One standing sentence lets every code-changing worker end with one local commit

## Answer

Yes. The owner gives one sentence now, and the coordinator quotes it word for word in every code-changing worker's brief and records a commit grant for that Task: "Task <task id> (work item <item>): when the command has succeeded, make one local commit of the paths you changed, in your own worktree, and do not push."

## What happens next if the owner picks it

- The ledger records Q32 = yes, with the sentence and the date.
- For each code-changing worker (up to nine Tasks: SW-07, SW-08, SW-10, SW-14, OB-06, OB-07, WA-01, WA-03, XC-07), the coordinator fills in only the Task id and item, quotes the sentence in the brief, and writes `GRANT(<item>,commit)`; the grant ends at that Task's `worker_done` (`WORKER-CONTRACT.md:244`).
- The worker follows WC-9 exactly: only after `worker_status: succeeded`, only in its own worktree, stages named paths plus `.dev/tasks`, `git commit --only -- <paths>`, never `--no-verify`, never pushes, and puts the commit id in its `worker_done` body (`WORKER-CONTRACT.md:42`).
- Before the PR session pushes, the coordinator shows the person the worker's commit and pushes only on the person's go (`WORKER-CONTRACT.md:244`).

## What it unlocks

- The change is saved as a commit the moment the worker succeeds, so it survives the gap until the PR session starts; cleaning or a stray checkout cannot silently lose it.
- The worker's `worker_done` names an exact commit id, so the coordinator and the person review a fixed revision, and the PR session pushes exactly that.
- Pre-commit hook failures (`verify-sync`) surface inside the worker, which wrote the change and can report it, rather than later in the PR session.
- One owner answer covers all nine Tasks, with no extra questions during the program.

## What it costs or risks

- WC-9 asks for "the user's instruction naming a local commit for that Task". Whether one sentence with the Task id filled in by the coordinator counts as "word for word" is not settled by the contract (UNVERIFIED). If a brief guard reads it strictly, the commit is refused and the worker reports it.
- Requires each worker to run alone in "its own child worktree created by Orca" (WC-9 condition 2). Whether a `worker-start` worktree meets that is UNVERIFIED.
- A standing permission is broader than the contract's one-grant-per-Task design intends, even though each Task still gets its own row.
- The person must review worker commits before every push (`WORKER-CONTRACT.md:244`), and the PR session may still add its own fix commits on top.

## What stays unresolved

- The exact sentence (the owner may reword it).
- Whether a strict reading of "for that Task" needs a separate owner sentence per Task after all.
