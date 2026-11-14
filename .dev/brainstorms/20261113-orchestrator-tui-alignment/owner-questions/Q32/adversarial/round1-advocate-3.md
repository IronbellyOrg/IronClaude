# Round 1 statement: Advocate for Variant 3 (Proposal C, one standing sentence, every code-changing worker commits once)

## Position

Variant 3 answers Q32 "yes" and supplies the sentence the question asks for. The question row itself reads "May supervised workers make one end-of-Task local commit? If yes, give the sentence to quote" (`merged-requirements.md:559`). Variant 3 is the only answer that fills in that second half: "Task <task id> (work item <item>): when the command has succeeded, make one local commit of the paths you changed, in your own worktree, and do not push." (variant-3, Answer).

The case for it rests on three things the contract already provides and the other answers leave unused:

1. A safe, fully specified commit path already exists. WC-9 (`WORKER-CONTRACT.md:42-43`) limits the commit to after `worker_status: succeeded`, in the worker's own child worktree, refuses on a detached HEAD or the default branch, stages only named paths plus `.dev/tasks`, uses `git commit --only -- <paths>`, never `--no-verify`, never pushes, and puts the commit id in `worker_done`. Source changes are within that scope: `artifacts` is "every other file written" (`WORKER-CONTRACT.md:33`), and WC-9 stages "every listed path" (`WORKER-CONTRACT.md:34`).
2. The person still controls publication. "Before any push that would publish worker commits the person has not seen, the coordinator shows them to the person and pushes only on the person's go; no earlier pre-authorization waives this" (`WORKER-CONTRACT.md:244`). A standing commit sentence therefore authorizes nothing outward.
3. The commit closes a real gap. Under the default, the change sits as uncommitted files from `worker_done` until a later PR session commits it (spec 6.4 rule 14, `merged-requirements.md:987`). The spec states "Owner latency is the real schedule" (`merged-requirements.md:523`), so that gap can be long, and its length is not measured anywhere (variant-2, costs: "UNVERIFIED").

## Steelman of Variant 1

Strongest version: Variant 1 keeps commits available but meets WC-9 at its strictest reading. WC-9 asks that "the brief quotes, word for word, the user's instruction naming a local commit for that Task" (`WORKER-CONTRACT.md:42`). Variant 1 has the owner speak once per Task, so the quoted text is the owner's own words about that exact Task, and no brief guard can doubt it (variant-1, unlocks). It also lets the owner spend the commit only where a checkpoint is worth it, and leaves no standing permission in the ledger that a later, unforeseen Task could ride on. This mirrors the contract's design that "A commit grant covers one Task and ends at that Task's `worker_done`" (`WORKER-CONTRACT.md:244`). It is the most conservative way to say "yes".

## Steelman of Variant 2

Strongest version: Variant 2 is the spec's recommended answer and its default (`merged-requirements.md:559`), so it costs zero owner questions in a program whose bottleneck is owner latency (`merged-requirements.md:523`). It keeps one commit path: the session that pushes is the session that commits and checks, so "what is pushed is exactly what that session committed" (variant-2, unlocks). The person reviews the diff once, before the commit, instead of reviewing worker commits before a push. It sidesteps the unresolved question of whether a filled-in template meets "word for word" (question.md fact 8, UNVERIFIED). It also matches the brief rule already written into the spec: every worker brief says the worker "leaves its changes uncommitted unless the brief quotes, word for word, the owner's instruction" (`merged-requirements.md:1070`). And the PR session commits anyway, since its grant row lists "local fix commits ... in the worktree" (question.md fact 5, spec line 1050). Nothing new must be built or checked.

## Key strengths claimed

- **Answers the question as asked.** Only Variant 3 gives "the sentence to quote" (`merged-requirements.md:559`). Variant 1 gives an example question, not a sentence; Variant 2 needs none.
- **One owner answer covers all nine Tasks.** The nine program-PR items (SW-07, SW-08, SW-10, SW-14, OB-06, OB-07, WA-01, WA-03, XC-07; question.md fact 6) get a grant without nine extra owner round trips, which matters under "Owner latency is the real schedule" (`merged-requirements.md:523`).
- **Durable checkpoint.** A commit on the worktree's branch survives a stray `git checkout -- .`, a clean, or removal of the worktree directory, where uncommitted files do not. Variant 2 names this exact risk itself: "Removing or cleaning that worktree, or a stray checkout in it, would lose it" (variant-2, costs).
- **Fixed revision to review.** The commit id in `worker_done` (`WORKER-CONTRACT.md:43`) gives the coordinator and the person a fixed object to review and the PR session a fixed object to push, rather than a `git diff` of a working tree that could still change.
- **Hook failures land with the writer.** The repo runs a pre-commit `verify-sync` hook (project CLAUDE.md, `.claude/` rule) and WC-9 forbids `--no-verify`. Under Variant 3 a hook failure is reported in the worker's own `worker_done` (WC-5 per `WORKER-CONTRACT.md:43`), by the session that wrote the change. Under Variant 2 it lands on the PR session, adding to the load INV-001 already places there (question.md fact 4).
- **No outward risk added.** Push stays with the coordinator and the person's go (`WORKER-CONTRACT.md:244`); WC-9 still says "never pushes".

## Weaknesses identified in Variant 1

- Up to nine more owner questions, each able to stall a dispatch, against the stated bottleneck (`merged-requirements.md:523`). Variant 1 concedes this (variant-1, costs).
- Two commit paths per program, chosen Task by Task, so the coordinator and PR session must check which applies in each worktree (variant-1, costs). That is the most complex state of the three.
- Gives the owner a judgment ("what makes a Task worth a commit") with no criterion (variant-1, unresolved), so answers may be inconsistent across Tasks.
- It does not answer "If yes, give the sentence to quote"; it defers the sentence to nine later moments.

## Weaknesses identified in Variant 2

- Leaves every code change exposed as uncommitted files for an unmeasured period (variant-2, costs, UNVERIFIED gap length). Its safety rests entirely on shared assumption A-002.
- No commit id in `worker_done`; review is against a mutable working tree (variant-2, costs).
- All staging, committing and hook failures move to the PR session, which already carries INV-001's load (question.md fact 4).
- The "one commit path" claim is weaker than stated: the PR session also makes "local fix commits" (question.md fact 5), so Variant 2 and Variant 3 both end with the PR session committing; Variant 3 only adds one earlier commit by the writer.

## Concessions

- **The "word for word ... for that Task" fit is my largest weakness.** WC-9 (`WORKER-CONTRACT.md:42`) wants the user's instruction naming a commit for that Task. A template whose Task id is filled in by the coordinator is partly the coordinator's words. Whether that satisfies the contract is UNVERIFIED (question.md fact 8). A repair the owner could choose: write the one sentence so it names every work item explicitly (for example "Each of SW-07, SW-08, SW-10, SW-14, OB-06, OB-07, WA-01, WA-03 and XC-07 may end its Task with one local commit in its own worktree, without pushing"), so each brief quotes the whole sentence unchanged. Whether naming the work item rather than the Orca Task id meets "for that Task" is still UNVERIFIED.
- WC-9 condition 2 needs "its own child worktree created by Orca". Whether a `worker-start` worktree counts is UNVERIFIED (question.md fact 7). If it does not, every commit is refused and Variant 3 degrades to Variant 2 with extra reporting.
- A standing permission sits closer to a blanket grant than the contract's one-grant-per-Task design (`WORKER-CONTRACT.md:244`), even though each Task still gets its own `GRANT(<item>,commit)` row.
- Variant 3 adds a review step: worker commits must be shown before push (`WORKER-CONTRACT.md:244`), on top of any PR-session fix commits.
- If A-002 holds in practice (one live agent per worktree, nothing cleans it), the gap risk that motivates Variant 3 is small, and the extra contract exposure may not pay for itself.

## Shared assumption responses

- **A-001 (a PR session runs later in the worker's own worktree, Q25 model): QUALIFY.** All three variants need it, and spec 6.3 marks a second sequential launch in a `worker-start` worktree as UNVERIFIED (diff-analysis A-001). If Q25 goes the other way, Q32 governs no workers and all three answers are moot equally, so it does not separate them. It should be checked before the first code-changing dispatch, not assumed.
- **A-002 (the worktree stays as the worker left it until the PR session): QUALIFY.** Spec 6.2's single live agent per worktree (as cited in diff-analysis A-002) supports it, but no rule cited in question.md forbids cleanup, worktree removal or a stray checkout in the gap, and the gap length is unmeasured. Variant 2 depends on it fully, Variant 1 partly, Variant 3 least, because a commit on the branch survives those events.

## Per-point verdicts

| Point | Superior variant | Reason |
|---|---|---|
| S-001 | tie | All three use the same five sections. |
| S-002 | 3 | The question asks "If yes, give the sentence to quote"; only Variant 3 provides it. |
| C-001 | 2 | Never committing is the default, needs no new grants and has no contract exposure; the gap risk is real but unmeasured. |
| C-002 | 2 | Zero owner questions beats one sentence (3) and up to nine questions (1) under "Owner latency is the real schedule". |
| C-003 | 1 | The owner's own words per Task meet WC-9's "word for word ... for that Task" without doubt; Variant 3's fit is UNVERIFIED. |
| C-004 | 3 | A commit checkpoint for every Task is the only full protection between `worker_done` and the PR session. |
| C-005 | 2 | One review of the diff before the commit is simpler than reviewing worker commits before push. |
| C-006 | 3 | A hook failure is best reported by the session that wrote the change. |
| C-007 | 2 | One commit owner for the change is simplest, though the PR session's fix commits make the margin small. |
| X-001 | 2 | Not needing a standing sentence avoids the unresolved contract question entirely. |
| X-002 | 3 | With owner latency driving the schedule, an unmeasured uncommitted gap is a material risk worth one cheap commit. |
| A-001 | tie | All three depend on it equally; failing it moots all three. |
| A-002 | 3 | Variant 3 depends least on the worktree staying untouched. |

## Overall

Steelmanned honestly, Variant 2 wins on cost and contract certainty: it is the default, needs no owner wording, avoids the UNVERIFIED "word for word" and child-worktree questions, and the spec's brief rule (`merged-requirements.md:1070`) already implements it. Variant 3's real advantage, protecting the change in the gap, depends on how long and how exposed that gap is, which nobody has measured. If the owner wants that protection, Variant 3 with the explicit item-list sentence from Concessions is the better "yes" than Variant 1.

Overall best answer for the owner: Variant 2, confidence 60%
