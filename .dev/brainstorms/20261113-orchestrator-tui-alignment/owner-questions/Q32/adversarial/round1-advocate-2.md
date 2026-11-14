# Round 1: Advocate for Variant 2 (No. Workers never commit; the PR session commits)

## Position

Variant 2 answers Q32 "No": in this program no worker brief carries a commit grant, workers leave changes uncommitted and unstaged, and the PR session stages and commits named paths with exclusive use of the worktree after the coordinator has shown the person the change.

This is the answer that needs the fewest new assumptions. It uses only rules that already exist and are already verified:

- `WORKER-CONTRACT.md:44`: "Outside that grant a worker never runs `git add` (including `git add .dev/tasks`), never commits, never moves HEAD and never touches a remote". Variant 2 is simply this rule with no exception switched on.
- Spec section 6.4 rule 14 (`merged-requirements.md:987`): "by default a supervised worker leaves its changes uncommitted and unstaged outside WC-9's grant; the PR session (6.3) stages and commits named paths with exclusive use of the worktree, after the coordinator has shown the person any change they have not seen". Variant 2 is that default, made permanent for this program.
- `WORKER-CONTRACT.md:245` already describes the safe commit steps (explicit paths plus `.dev/tasks`, `git commit --only -- <paths>`, stop on hook failure, never `--no-verify`) for a session that is not a worker.
- The PR session already commits anyway: a `pr-submit` row lists "local fix commits and `sc:troubleshoot` artifacts in the worktree" (`merged-requirements.md:1050`). So there is already one session with commit rights in every PR worktree; Variant 2 does not add a second.

It also costs the owner nothing: it equals the spec's recommendation ("No; the PR session commits") and its default if unanswered (`question.md` lines 9-15), in a program where "Owner latency is the real schedule" (`merged-requirements.md:523`).

## Steelman of Variant 1

Strongest version: Variant 1 is not "yes" and not "no"; it is the spec's own default (rule 14 already says a worker commit happens "only when its brief quotes, word for word, an owner instruction naming a local commit for that Task", `merged-requirements.md:987`) with the per-Task door left open. It is the only variant that meets WC-9's text at its strictest, because the quoted words really are "the user's instruction naming a local commit for that Task" (`WORKER-CONTRACT.md:42`). It lets the owner buy a checkpoint exactly where it is worth it (a large or risky change) and pay nothing elsewhere, since an unanswered or "no" reply falls back to Variant 2's behaviour. It never leaves a standing permission in the ledger. In short, it is Variant 2 plus an optional escape hatch, and it gets the contract reading right.

## Steelman of Variant 3

Strongest version: Variant 3 treats the uncommitted gap as the real risk and closes it for every Task. The change becomes a commit "the moment the worker succeeds", the `worker_done` body carries a commit id (`WORKER-CONTRACT.md:43`: "gives the commit ID in its `worker_done` body"), so the person reviews a fixed revision and the PR session pushes exactly that. Pre-commit hook failures surface in the session that wrote the change. One owner sentence covers all nine Tasks, so no extra questions are asked during the program. Each Task still gets its own `GRANT(<item>,commit)` row and the grant still ends at that Task's `worker_done` (`WORKER-CONTRACT.md:244`), so it does not literally create a cross-Task permission. It also answers the question as asked: Q32 says "If yes, give the sentence to quote", and Variant 3 is the only one that gives it.

## Key strengths claimed

1. **Zero contract-reading risk.** Variant 2 never relies on two UNVERIFIED readings that Variant 3 depends on (`question.md` facts 7 and 8): whether a coordinator-filled template meets "quotes, word for word ... for that Task", and whether a `worker-start` worktree is "its own child worktree created by Orca" (WC-9 condition 2, WC-11 at `WORKER-CONTRACT.md:47`). Variant 1 also depends on the second.
2. **One commit path.** The session that commits is the session that pushes. There is never a mix of worker commits and PR-session commits in one PR worktree, so nobody has to work out per worktree which rule applies.
3. **One review, before the commit.** The coordinator shows the person the uncommitted change once (rule 14). There are no "worker commits the person has not seen" to show again before the push (`WORKER-CONTRACT.md:244`).
4. **Hook failures land in a session that can fix them.** A worker that hits a failed commit can only report it ("a refused or failed commit is reported as WC-5 states", `WORKER-CONTRACT.md:43`); someone else must then fix and commit anyway. The PR session is an attended top-level session that can fix a `verify-sync` failure and retry, never with `--no-verify`.
5. **No owner latency, no new wording.** Equals the default; asking costs one "yes, as recommended".
6. **Degrades cleanly.** If Q25 is answered the other way (no workers on PR items), Variant 2 leaves nothing behind; no grant rows or sentence go unused.

## Weaknesses identified in Variant 1

- Up to nine extra owner questions (SW-07, SW-08, SW-10, SW-14, OB-06, OB-07, WA-01, WA-03, XC-07; `question.md` fact 6), each able to hold a dispatch, against `merged-requirements.md:523` ("Owner latency is the real schedule").
- Two commit paths in one program; the coordinator and each PR session must check which applies per worktree, which is the kind of per-case branching that causes mistakes.
- Still depends on the UNVERIFIED child-worktree reading for every Task the owner approves.
- The judgment "is this Task worth a commit" is pushed to the owner each time with no criterion (Variant 1's own "What stays unresolved").
- In practice, a "no reply" at dispatch yields Variant 2's behaviour anyway, so much of Variant 1's machinery buys little.

## Weaknesses identified in Variant 3

- Its core mechanism rests on an UNVERIFIED reading: a sentence with "<task id>" filled in by the coordinator may not be "the user's instruction naming a local commit for that Task" quoted "word for word" (`WORKER-CONTRACT.md:42`). Variant 3 admits a strict brief guard would refuse the commit. If that happens on every Task, the program gets Variant 2's outcome plus nine refused-commit reports.
- Also depends on the UNVERIFIED child-worktree reading (WC-9 condition 2).
- Adds a review step: worker commits must be shown before every push (`WORKER-CONTRACT.md:244`), on top of the PR session's own fix commits.
- A standing sentence is broader than the contract's "A commit grant covers one Task" design intends (Variant 3 concedes this).
- Hook failures surface in the worker, but the worker can only report them, so the fix still lands elsewhere.

## Concessions

- Variant 2 has a real gap: between `worker_done` and the PR session's commit the change exists only as uncommitted files. A worktree removal, clean or stray checkout loses it. The spec does not measure the gap (UNVERIFIED). Variant 3 is genuinely better on this one point.
- Variant 2 gives no fixed revision to review; the person reviews `git diff` of a working tree, which can in principle change between showing and committing. Variant 3's commit id is stronger review evidence.
- Variant 2 is stricter than spec rule 14, which keeps the per-Task worker commit available via Q32. Saying "no" closes that door for this program; reopening it later means re-asking Q32. Variant 1 keeps the door open at the cost of latency.
- Variant 2 adds commit and hook work to the PR route that INV-001 already loads (`question.md` fact 4).
- Variant 2 does not answer "give the sentence to quote"; it does not need to, but Variant 3 is more complete against the question's literal form.

## Shared assumption responses

- **A-001 (PR session runs later in the same worktree, Q25 model): QUALIFY.** All three variants depend on it, and per the diff analysis spec 6.3 marks a second sequential launch in a `worker-start` worktree UNVERIFIED (I did not re-read that line). Variant 2 is least harmed if it fails: it creates no grant rows or standing sentence that would be left unused, whereas Variant 3 would have collected a sentence for workers that do not exist.
- **A-002 (worktree stays as the worker left it until the PR session): QUALIFY.** The single-live-agent rule (spec 6.2, per the diff analysis) supports it, but nothing guarantees it, and Variant 2 is the most exposed if it fails. Accepting Variant 2 should come with one guard: the coordinator never removes or cleans a worker's worktree until its PR session has committed. That guard is not yet written anywhere I verified (UNVERIFIED).

## Per-point verdicts

| Point | Superior variant | Reason |
|---|---|---|
| S-001 | tie | All three use the same five sections. |
| S-002 | 3 | The question literally asks for "the sentence to quote" if yes; only Variant 3 supplies one. |
| C-001 | 2 | Never committing avoids both UNVERIFIED WC-9 readings and owner latency; the gap risk is containable by a coordinator guard. |
| C-002 | 2 | Collects no wording and asks no extra questions in a latency-bound program. |
| C-003 | 1 | Of the variants that actually commit, only per-Task owner words surely meet "word for word ... for that Task". |
| C-004 | 3 | A commit checkpoint at `worker_done` is real protection that Variant 2 lacks. |
| C-005 | 2 | One review before one commit by the pushing session is simpler; Variant 3's fixed revision is a close second. |
| C-006 | 2 | A worker can only report a failed commit (WC-5); the attended PR session can fix and retry. |
| C-007 | 2 | One commit path for every PR worktree, no per-Task branching. |
| X-001 | 2 | Makes the unresolved standing-sentence reading moot instead of betting on it. |
| X-002 | 2 | Names the gap honestly; its size depends on coordinator discipline, which a guard can bound, rather than justifying commits everywhere. |
| A-001 | tie | All depend equally; Variant 2 leaves the least behind if it fails. |
| A-002 | 3 | Only Variant 3 stays safe if the worktree is disturbed before the PR session. |

## Overall

Variant 2 wins on the high-severity points (C-001, C-002, X-001) because it removes the two UNVERIFIED contract readings and the owner latency at once; its main cost, the uncommitted gap, is real but can be bounded by a "never clean before the PR session commits" guard. Variant 1 is a respectable fallback if the owner wants checkpoints for specific risky Tasks.

Overall best answer for the owner: Variant 2, confidence 70%
