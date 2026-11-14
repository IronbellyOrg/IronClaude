# Adversarial Debate Transcript (Q32)

## Metadata
- Depth: quick
- Rounds completed: 1 (Round 2, Round 2.5 invariant probe and Round 3 skipped: depth=quick)
- Convergence achieved: 100% by majority rule (13 of 13 points have at least 2 of 3 advocates agreeing); unanimous on 9 of 13 (69%)
- Convergence threshold: 80%
- Focus areas: All
- Advocate count: 3 (each a spawned general-purpose agent on the session's default model; Variant 1 = proposal-A, Variant 2 = proposal-B, Variant 3 = proposal-C)
- Taxonomy coverage: L1 surface (S-001, S-002), L2 structural (C-005, C-007), L3 state mechanics (C-003 guard, C-004, A-002) all covered; no forced round
- Advocate statements were written by the advocates to `round1-advocate-1.md`, `round1-advocate-2.md`, `round1-advocate-3.md` in this folder and are reproduced below unchanged except heading levels.

## Round 1: Advocate Statements

### Variant 1 Advocate (general-purpose, default model)



#### Position

Variant 1 answers Q32 with "not as a standing rule": at each code-changing dispatch the coordinator asks the owner whether that one Task may end with one local commit, quotes the owner's own reply in that Task's brief, and records `GRANT(<item>,commit)`; with no yes, the worker leaves its changes uncommitted and the PR session commits (variant-1, "Answer").

Its case rests on three verified points:

1. It is the only "yes" path that meets WC-9 at its strictest. WC-9 allows a worker commit only when "the brief quotes, word for word, the user's instruction naming a local commit for that Task" (`WORKER-CONTRACT.md:42`). A per-Task owner reply is, literally, the user's instruction for that Task. Nothing has to be interpreted.
2. It matches the contract's own grain. "A commit grant covers one Task and ends at that Task's `worker_done`" (`WORKER-CONTRACT.md:244`). A per-Task question gives a per-Task grant with no standing permission in the ledger.
3. Its fallback is exactly the spec's default. With no yes or no reply, the result is spec 6.4 rule 14: "by default a supervised worker leaves its changes uncommitted and unstaged outside WC-9's grant; the PR session (6.3) stages and commits named paths" (`merged-requirements.md:987`). So Variant 1 never does worse than Variant 2 when the owner is silent.

It also fits the spec's question cadence: "Ask one question at a time ... Q27, Q28, Q29, Q30, Q32 are asked when their item is next" (`merged-requirements.md:523`). Variant 1's questions arrive one at a time, each at the dispatch it governs.

#### Steelman of Variant 2

The strongest version of Variant 2: one program, one commit path, zero extra owner questions. The session that pushes is the session that committed, so "what is pushed is exactly what that session committed and checked" (variant-2, "What it unlocks"). The person reviews the diff once, before the commit, instead of reviewing worker commits before the push as `WORKER-CONTRACT.md:244` would require. It is the spec's recommended answer and the default if unanswered (`merged-requirements.md:559`), so choosing it changes nothing in the spec text, the brief rule (`merged-requirements.md:1070`) or the gate list. And the PR session already makes commits in the worktree anyway: a `pr-submit` row lists "local fix commits ... in the worktree" (`merged-requirements.md:1050`). It also respects the stated bottleneck, "Owner latency is the real schedule" (`merged-requirements.md:523`), better than any alternative. Finally, if Q25 is answered with its alternative ("a top-level agent per PR item ... and no worker", `merged-requirements.md:552`), a plain "no" costs nothing, while the other two variants would have spent owner attention for no workers.

What it gets right: simplicity, zero added owner load, a single review point, and alignment with every existing spec rule.

#### Steelman of Variant 3

The strongest version of Variant 3: the uncommitted gap is real and a commit closes it. Between `worker_done` and the PR session's commit, the change is only loose files; a commit makes it a fixed revision whose id travels in the `worker_done` body (`WORKER-CONTRACT.md:43`, "gives the commit ID in its `worker_done` body"), so the coordinator, the person and the PR session all look at the same thing. A pre-commit hook failure (`verify-sync`) surfaces in the session that wrote the change rather than in a later session that has to reconstruct intent. And it costs one owner answer for all nine Tasks instead of nine. It also directly answers the question as asked: "If yes, give the sentence to quote" (`merged-requirements.md:559`); Variant 3 is the only variant that hands the owner that sentence.

What it gets right: durability of the change across the handoff, a fixed revision for review, early hook failures, and minimal owner load for a "yes".

#### Key strengths claimed

- **Strict WC-9 compliance.** The quoted text is the owner's own words for that Task (`WORKER-CONTRACT.md:42`). No reader of the brief can doubt it, so no commit is refused on a wording technicality. Variant 3 itself flags that its filled-in template's fit is UNVERIFIED (variant-3, "What it costs or risks").
- **No standing permission.** The ledger never holds a reusable commit sentence that could be applied to a Task the owner never considered (variant-1, "What it unlocks").
- **Judgment where it matters.** The owner can grant a commit for a large or risky change that benefits from a checkpoint and decline it elsewhere. This is the only variant that lets the commit decision follow the actual Task.
- **Safe default.** Silence or "no" falls back to spec 6.4 rule 14 (`merged-requirements.md:987`), the same outcome as Variant 2.
- **Fits the existing question schedule.** Q32 is already asked "only when the first code-changing worker is dispatched" (`merged-requirements.md:559`); Variant 1 extends that same moment to later dispatches.

#### Weaknesses identified in Variant 2

- **The uncommitted gap is accepted, not bounded.** Variant 2 itself says the gap length is UNVERIFIED and lists "How long uncommitted work may wait" as unresolved. If the PR session is late (Q25's sequential launch in a `worker-start` worktree is itself UNVERIFIED, `merged-requirements.md:552`), loose files sit longest exactly where nothing protects them.
- **No fixed revision.** The coordinator reviews with `git status` and `git diff` rather than a commit id (variant-2, "What it costs or risks"), so what the person reviewed and what the PR session later commits are linked only by the worktree staying untouched.
- **All hook and commit load on the PR route.** It adds to the load INV-001 already places on the PR session (variant-2 says so). The PR session must commit someone else's change and handle any `verify-sync` failure it did not cause.
- **Minor citation error.** Variant 2 cites `WORKER-CONTRACT.md:42` for "Outside that grant a worker never runs `git add` ... never commits"; that sentence is at line 44. The substance is correct.
- **Closes the door entirely.** For this program the grant table can never hold a worker commit row, even for a Task where the owner would want one.

#### Weaknesses identified in Variant 3

- **WC-9 fit is unproven.** WC-9 requires "the user's instruction naming a local commit for that Task" quoted "word for word" (`WORKER-CONTRACT.md:42`). In Variant 3 the coordinator, not the owner, fills in the Task id and item. A strict brief guard can read that as the coordinator's instruction, refuse the commit, and leave the worker reporting a refused commit (variant-3 admits this). The design's main benefit then fails silently in the worst case.
- **Standing permission against a per-Task design.** `WORKER-CONTRACT.md:244` makes each grant end at one `worker_done`; Variant 3 concedes that a standing permission "is broader than the contract's one-grant-per-Task design intends".
- **Two review steps instead of one.** Worker commits must be shown before every push (`WORKER-CONTRACT.md:244`), and the PR session still adds its own fix commits (`merged-requirements.md:1050`), so the person sees worker commits plus PR-session commits.
- **Contradicts the spec's recommendation and default** (`merged-requirements.md:559`), so it requires changing spec 6.4 rule 14's framing from default-uncommitted to default-committed for code workers.
- **Child worktree condition unverified.** WC-9 condition 2 needs "its own child worktree created by Orca"; whether a `worker-start` worktree qualifies is UNVERIFIED (question.md fact 7). This applies to Variant 1 too, but Variant 3 bets all nine Tasks on it.

#### Concessions

- **Owner latency is my biggest weakness.** Up to nine extra questions in a program where "Owner latency is the real schedule" (`merged-requirements.md:523`). A dispatch can wait on an answer, and that delay is a direct schedule cost. Variant 2 has none of it; Variant 3 has one question.
- **Two commit paths.** Some worktrees end with a worker commit and some without, so the coordinator and the PR session must check which applies in each (variant-1 says so). Variant 2 has one path.
- **Variant 1 does not answer the question in the form asked.** Q32 asks "If yes, give the sentence to quote". Variant 1 gives neither a firm no nor a sentence; it defers. An owner who wants one decision now gets nine later.
- **The child worktree condition (WC-9 (2), WC-11) is UNVERIFIED for Variant 1 as well.**
- **The flexibility may be unused.** Nothing in the spec identifies a Task among the nine that needs a mid-handoff checkpoint, so the benefit of per-Task judgment is speculative.

#### Shared assumption responses

- **A-001 (the PR session runs later in the worker's own worktree, Q25 model): QUALIFY.** All three variants depend on it, and the spec itself marks "that Orca permits a second, sequential agent launch in a `worker-start` worktree" as UNVERIFIED (`merged-requirements.md:552`). If the owner picks Q25's alternative (no worker), Q32 governs nothing; that outcome favors the cheapest answer, which is Variant 2. The assumption should be confirmed by Q25's answer before Q32 is asked, which the spec's ordering (Q25 in W0 intake, Q32 at first code-changing dispatch, `merged-requirements.md:523`) already does.
- **A-002 (the worktree stays as the worker left it until the PR session): QUALIFY.** It is supported by the single-live-agent-per-worktree rule (spec 6.2, per the diff analysis) and by `WORKER-CONTRACT.md:245` ("The coordinator commits or merges in a worktree only when no worker runs there"), but nothing bounds the time, and a coordinator clean, a stray checkout or a shared-stash pop is not mechanically prevented. It holds well enough to make Variant 2 acceptable, not well enough to make the gap zero risk.

#### Per-point verdicts

| Point | Superior variant | Reason |
|---|---|---|
| S-001 | tie | All three use the same five sections. |
| S-002 | 3 | Only Variant 3 supplies the sentence the question explicitly asks for if the answer is yes. |
| C-001 | 2 | One rule for every Task, matching spec 6.4 rule 14, with the gap risk held down by A-002. |
| C-002 | 2 | Collects no wording at all, the best fit for "Owner latency is the real schedule". |
| C-003 | 1 | Among variants that use the grant, only Variant 1 meets "word for word ... for that Task" without interpretation. |
| C-004 | 3 | Every Task's change becomes a commit the moment the worker succeeds. |
| C-005 | 2 | One review, before the commit, instead of worker commits plus PR-session commits before a push. |
| C-006 | 3 | A hook failure surfaces in the session that wrote the change (low severity). |
| C-007 | 2 | A single commit path in every worktree. |
| X-001 | 1 | Asking per Task removes the UNVERIFIED reading of a filled-in template. |
| X-002 | 2 | The gap is real but held down by single-agent-per-worktree and `WORKER-CONTRACT.md:245`; it does not justify extra commits or questions. |
| A-001 | 2 | If Q25's alternative removes workers, a plain "no" wastes nothing. |
| A-002 | 3 | Only Variant 3 stays safe if the stable-worktree assumption fails. |

#### Overall

After steelmanning, Variant 2 is the better answer for this program: it adds no owner questions in a latency-bound program, keeps one commit path and one review point, and matches the spec text already written. Variant 1's real advantage (strict WC-9 fit with per-Task judgment) matters only if the owner actually wants worker commits for some Tasks, and the owner can still get that later by revising Q32 for a specific Task. Variant 3's durability gain is real but rests on an UNVERIFIED reading of WC-9.

Overall best answer for the owner: Variant 2, confidence 65%

### Variant 2 Advocate (general-purpose, default model)



#### Position

Variant 2 answers Q32 "No": in this program no worker brief carries a commit grant, workers leave changes uncommitted and unstaged, and the PR session stages and commits named paths with exclusive use of the worktree after the coordinator has shown the person the change.

This is the answer that needs the fewest new assumptions. It uses only rules that already exist and are already verified:

- `WORKER-CONTRACT.md:44`: "Outside that grant a worker never runs `git add` (including `git add .dev/tasks`), never commits, never moves HEAD and never touches a remote". Variant 2 is simply this rule with no exception switched on.
- Spec section 6.4 rule 14 (`merged-requirements.md:987`): "by default a supervised worker leaves its changes uncommitted and unstaged outside WC-9's grant; the PR session (6.3) stages and commits named paths with exclusive use of the worktree, after the coordinator has shown the person any change they have not seen". Variant 2 is that default, made permanent for this program.
- `WORKER-CONTRACT.md:245` already describes the safe commit steps (explicit paths plus `.dev/tasks`, `git commit --only -- <paths>`, stop on hook failure, never `--no-verify`) for a session that is not a worker.
- The PR session already commits anyway: a `pr-submit` row lists "local fix commits and `sc:troubleshoot` artifacts in the worktree" (`merged-requirements.md:1050`). So there is already one session with commit rights in every PR worktree; Variant 2 does not add a second.

It also costs the owner nothing: it equals the spec's recommendation ("No; the PR session commits") and its default if unanswered (`question.md` lines 9-15), in a program where "Owner latency is the real schedule" (`merged-requirements.md:523`).

#### Steelman of Variant 1

Strongest version: Variant 1 is not "yes" and not "no"; it is the spec's own default (rule 14 already says a worker commit happens "only when its brief quotes, word for word, an owner instruction naming a local commit for that Task", `merged-requirements.md:987`) with the per-Task door left open. It is the only variant that meets WC-9's text at its strictest, because the quoted words really are "the user's instruction naming a local commit for that Task" (`WORKER-CONTRACT.md:42`). It lets the owner buy a checkpoint exactly where it is worth it (a large or risky change) and pay nothing elsewhere, since an unanswered or "no" reply falls back to Variant 2's behaviour. It never leaves a standing permission in the ledger. In short, it is Variant 2 plus an optional escape hatch, and it gets the contract reading right.

#### Steelman of Variant 3

Strongest version: Variant 3 treats the uncommitted gap as the real risk and closes it for every Task. The change becomes a commit "the moment the worker succeeds", the `worker_done` body carries a commit id (`WORKER-CONTRACT.md:43`: "gives the commit ID in its `worker_done` body"), so the person reviews a fixed revision and the PR session pushes exactly that. Pre-commit hook failures surface in the session that wrote the change. One owner sentence covers all nine Tasks, so no extra questions are asked during the program. Each Task still gets its own `GRANT(<item>,commit)` row and the grant still ends at that Task's `worker_done` (`WORKER-CONTRACT.md:244`), so it does not literally create a cross-Task permission. It also answers the question as asked: Q32 says "If yes, give the sentence to quote", and Variant 3 is the only one that gives it.

#### Key strengths claimed

1. **Zero contract-reading risk.** Variant 2 never relies on two UNVERIFIED readings that Variant 3 depends on (`question.md` facts 7 and 8): whether a coordinator-filled template meets "quotes, word for word ... for that Task", and whether a `worker-start` worktree is "its own child worktree created by Orca" (WC-9 condition 2, WC-11 at `WORKER-CONTRACT.md:47`). Variant 1 also depends on the second.
2. **One commit path.** The session that commits is the session that pushes. There is never a mix of worker commits and PR-session commits in one PR worktree, so nobody has to work out per worktree which rule applies.
3. **One review, before the commit.** The coordinator shows the person the uncommitted change once (rule 14). There are no "worker commits the person has not seen" to show again before the push (`WORKER-CONTRACT.md:244`).
4. **Hook failures land in a session that can fix them.** A worker that hits a failed commit can only report it ("a refused or failed commit is reported as WC-5 states", `WORKER-CONTRACT.md:43`); someone else must then fix and commit anyway. The PR session is an attended top-level session that can fix a `verify-sync` failure and retry, never with `--no-verify`.
5. **No owner latency, no new wording.** Equals the default; asking costs one "yes, as recommended".
6. **Degrades cleanly.** If Q25 is answered the other way (no workers on PR items), Variant 2 leaves nothing behind; no grant rows or sentence go unused.

#### Weaknesses identified in Variant 1

- Up to nine extra owner questions (SW-07, SW-08, SW-10, SW-14, OB-06, OB-07, WA-01, WA-03, XC-07; `question.md` fact 6), each able to hold a dispatch, against `merged-requirements.md:523` ("Owner latency is the real schedule").
- Two commit paths in one program; the coordinator and each PR session must check which applies per worktree, which is the kind of per-case branching that causes mistakes.
- Still depends on the UNVERIFIED child-worktree reading for every Task the owner approves.
- The judgment "is this Task worth a commit" is pushed to the owner each time with no criterion (Variant 1's own "What stays unresolved").
- In practice, a "no reply" at dispatch yields Variant 2's behaviour anyway, so much of Variant 1's machinery buys little.

#### Weaknesses identified in Variant 3

- Its core mechanism rests on an UNVERIFIED reading: a sentence with "<task id>" filled in by the coordinator may not be "the user's instruction naming a local commit for that Task" quoted "word for word" (`WORKER-CONTRACT.md:42`). Variant 3 admits a strict brief guard would refuse the commit. If that happens on every Task, the program gets Variant 2's outcome plus nine refused-commit reports.
- Also depends on the UNVERIFIED child-worktree reading (WC-9 condition 2).
- Adds a review step: worker commits must be shown before every push (`WORKER-CONTRACT.md:244`), on top of the PR session's own fix commits.
- A standing sentence is broader than the contract's "A commit grant covers one Task" design intends (Variant 3 concedes this).
- Hook failures surface in the worker, but the worker can only report them, so the fix still lands elsewhere.

#### Concessions

- Variant 2 has a real gap: between `worker_done` and the PR session's commit the change exists only as uncommitted files. A worktree removal, clean or stray checkout loses it. The spec does not measure the gap (UNVERIFIED). Variant 3 is genuinely better on this one point.
- Variant 2 gives no fixed revision to review; the person reviews `git diff` of a working tree, which can in principle change between showing and committing. Variant 3's commit id is stronger review evidence.
- Variant 2 is stricter than spec rule 14, which keeps the per-Task worker commit available via Q32. Saying "no" closes that door for this program; reopening it later means re-asking Q32. Variant 1 keeps the door open at the cost of latency.
- Variant 2 adds commit and hook work to the PR route that INV-001 already loads (`question.md` fact 4).
- Variant 2 does not answer "give the sentence to quote"; it does not need to, but Variant 3 is more complete against the question's literal form.

#### Shared assumption responses

- **A-001 (PR session runs later in the same worktree, Q25 model): QUALIFY.** All three variants depend on it, and per the diff analysis spec 6.3 marks a second sequential launch in a `worker-start` worktree UNVERIFIED (I did not re-read that line). Variant 2 is least harmed if it fails: it creates no grant rows or standing sentence that would be left unused, whereas Variant 3 would have collected a sentence for workers that do not exist.
- **A-002 (worktree stays as the worker left it until the PR session): QUALIFY.** The single-live-agent rule (spec 6.2, per the diff analysis) supports it, but nothing guarantees it, and Variant 2 is the most exposed if it fails. Accepting Variant 2 should come with one guard: the coordinator never removes or cleans a worker's worktree until its PR session has committed. That guard is not yet written anywhere I verified (UNVERIFIED).

#### Per-point verdicts

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

#### Overall

Variant 2 wins on the high-severity points (C-001, C-002, X-001) because it removes the two UNVERIFIED contract readings and the owner latency at once; its main cost, the uncommitted gap, is real but can be bounded by a "never clean before the PR session commits" guard. Variant 1 is a respectable fallback if the owner wants checkpoints for specific risky Tasks.

Overall best answer for the owner: Variant 2, confidence 70%

### Variant 3 Advocate (general-purpose, default model)



#### Position

Variant 3 answers Q32 "yes" and supplies the sentence the question asks for. The question row itself reads "May supervised workers make one end-of-Task local commit? If yes, give the sentence to quote" (`merged-requirements.md:559`). Variant 3 is the only answer that fills in that second half: "Task <task id> (work item <item>): when the command has succeeded, make one local commit of the paths you changed, in your own worktree, and do not push." (variant-3, Answer).

The case for it rests on three things the contract already provides and the other answers leave unused:

1. A safe, fully specified commit path already exists. WC-9 (`WORKER-CONTRACT.md:42-43`) limits the commit to after `worker_status: succeeded`, in the worker's own child worktree, refuses on a detached HEAD or the default branch, stages only named paths plus `.dev/tasks`, uses `git commit --only -- <paths>`, never `--no-verify`, never pushes, and puts the commit id in `worker_done`. Source changes are within that scope: `artifacts` is "every other file written" (`WORKER-CONTRACT.md:33`), and WC-9 stages "every listed path" (`WORKER-CONTRACT.md:34`).
2. The person still controls publication. "Before any push that would publish worker commits the person has not seen, the coordinator shows them to the person and pushes only on the person's go; no earlier pre-authorization waives this" (`WORKER-CONTRACT.md:244`). A standing commit sentence therefore authorizes nothing outward.
3. The commit closes a real gap. Under the default, the change sits as uncommitted files from `worker_done` until a later PR session commits it (spec 6.4 rule 14, `merged-requirements.md:987`). The spec states "Owner latency is the real schedule" (`merged-requirements.md:523`), so that gap can be long, and its length is not measured anywhere (variant-2, costs: "UNVERIFIED").

#### Steelman of Variant 1

Strongest version: Variant 1 keeps commits available but meets WC-9 at its strictest reading. WC-9 asks that "the brief quotes, word for word, the user's instruction naming a local commit for that Task" (`WORKER-CONTRACT.md:42`). Variant 1 has the owner speak once per Task, so the quoted text is the owner's own words about that exact Task, and no brief guard can doubt it (variant-1, unlocks). It also lets the owner spend the commit only where a checkpoint is worth it, and leaves no standing permission in the ledger that a later, unforeseen Task could ride on. This mirrors the contract's design that "A commit grant covers one Task and ends at that Task's `worker_done`" (`WORKER-CONTRACT.md:244`). It is the most conservative way to say "yes".

#### Steelman of Variant 2

Strongest version: Variant 2 is the spec's recommended answer and its default (`merged-requirements.md:559`), so it costs zero owner questions in a program whose bottleneck is owner latency (`merged-requirements.md:523`). It keeps one commit path: the session that pushes is the session that commits and checks, so "what is pushed is exactly what that session committed" (variant-2, unlocks). The person reviews the diff once, before the commit, instead of reviewing worker commits before a push. It sidesteps the unresolved question of whether a filled-in template meets "word for word" (question.md fact 8, UNVERIFIED). It also matches the brief rule already written into the spec: every worker brief says the worker "leaves its changes uncommitted unless the brief quotes, word for word, the owner's instruction" (`merged-requirements.md:1070`). And the PR session commits anyway, since its grant row lists "local fix commits ... in the worktree" (question.md fact 5, spec line 1050). Nothing new must be built or checked.

#### Key strengths claimed

- **Answers the question as asked.** Only Variant 3 gives "the sentence to quote" (`merged-requirements.md:559`). Variant 1 gives an example question, not a sentence; Variant 2 needs none.
- **One owner answer covers all nine Tasks.** The nine program-PR items (SW-07, SW-08, SW-10, SW-14, OB-06, OB-07, WA-01, WA-03, XC-07; question.md fact 6) get a grant without nine extra owner round trips, which matters under "Owner latency is the real schedule" (`merged-requirements.md:523`).
- **Durable checkpoint.** A commit on the worktree's branch survives a stray `git checkout -- .`, a clean, or removal of the worktree directory, where uncommitted files do not. Variant 2 names this exact risk itself: "Removing or cleaning that worktree, or a stray checkout in it, would lose it" (variant-2, costs).
- **Fixed revision to review.** The commit id in `worker_done` (`WORKER-CONTRACT.md:43`) gives the coordinator and the person a fixed object to review and the PR session a fixed object to push, rather than a `git diff` of a working tree that could still change.
- **Hook failures land with the writer.** The repo runs a pre-commit `verify-sync` hook (project CLAUDE.md, `.claude/` rule) and WC-9 forbids `--no-verify`. Under Variant 3 a hook failure is reported in the worker's own `worker_done` (WC-5 per `WORKER-CONTRACT.md:43`), by the session that wrote the change. Under Variant 2 it lands on the PR session, adding to the load INV-001 already places there (question.md fact 4).
- **No outward risk added.** Push stays with the coordinator and the person's go (`WORKER-CONTRACT.md:244`); WC-9 still says "never pushes".

#### Weaknesses identified in Variant 1

- Up to nine more owner questions, each able to stall a dispatch, against the stated bottleneck (`merged-requirements.md:523`). Variant 1 concedes this (variant-1, costs).
- Two commit paths per program, chosen Task by Task, so the coordinator and PR session must check which applies in each worktree (variant-1, costs). That is the most complex state of the three.
- Gives the owner a judgment ("what makes a Task worth a commit") with no criterion (variant-1, unresolved), so answers may be inconsistent across Tasks.
- It does not answer "If yes, give the sentence to quote"; it defers the sentence to nine later moments.

#### Weaknesses identified in Variant 2

- Leaves every code change exposed as uncommitted files for an unmeasured period (variant-2, costs, UNVERIFIED gap length). Its safety rests entirely on shared assumption A-002.
- No commit id in `worker_done`; review is against a mutable working tree (variant-2, costs).
- All staging, committing and hook failures move to the PR session, which already carries INV-001's load (question.md fact 4).
- The "one commit path" claim is weaker than stated: the PR session also makes "local fix commits" (question.md fact 5), so Variant 2 and Variant 3 both end with the PR session committing; Variant 3 only adds one earlier commit by the writer.

#### Concessions

- **The "word for word ... for that Task" fit is my largest weakness.** WC-9 (`WORKER-CONTRACT.md:42`) wants the user's instruction naming a commit for that Task. A template whose Task id is filled in by the coordinator is partly the coordinator's words. Whether that satisfies the contract is UNVERIFIED (question.md fact 8). A repair the owner could choose: write the one sentence so it names every work item explicitly (for example "Each of SW-07, SW-08, SW-10, SW-14, OB-06, OB-07, WA-01, WA-03 and XC-07 may end its Task with one local commit in its own worktree, without pushing"), so each brief quotes the whole sentence unchanged. Whether naming the work item rather than the Orca Task id meets "for that Task" is still UNVERIFIED.
- WC-9 condition 2 needs "its own child worktree created by Orca". Whether a `worker-start` worktree counts is UNVERIFIED (question.md fact 7). If it does not, every commit is refused and Variant 3 degrades to Variant 2 with extra reporting.
- A standing permission sits closer to a blanket grant than the contract's one-grant-per-Task design (`WORKER-CONTRACT.md:244`), even though each Task still gets its own `GRANT(<item>,commit)` row.
- Variant 3 adds a review step: worker commits must be shown before push (`WORKER-CONTRACT.md:244`), on top of any PR-session fix commits.
- If A-002 holds in practice (one live agent per worktree, nothing cleans it), the gap risk that motivates Variant 3 is small, and the extra contract exposure may not pay for itself.

#### Shared assumption responses

- **A-001 (a PR session runs later in the worker's own worktree, Q25 model): QUALIFY.** All three variants need it, and spec 6.3 marks a second sequential launch in a `worker-start` worktree as UNVERIFIED (diff-analysis A-001). If Q25 goes the other way, Q32 governs no workers and all three answers are moot equally, so it does not separate them. It should be checked before the first code-changing dispatch, not assumed.
- **A-002 (the worktree stays as the worker left it until the PR session): QUALIFY.** Spec 6.2's single live agent per worktree (as cited in diff-analysis A-002) supports it, but no rule cited in question.md forbids cleanup, worktree removal or a stray checkout in the gap, and the gap length is unmeasured. Variant 2 depends on it fully, Variant 1 partly, Variant 3 least, because a commit on the branch survives those events.

#### Per-point verdicts

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

#### Overall

Steelmanned honestly, Variant 2 wins on cost and contract certainty: it is the default, needs no owner wording, avoids the UNVERIFIED "word for word" and child-worktree questions, and the spec's brief rule (`merged-requirements.md:1070`) already implements it. Variant 3's real advantage, protecting the change in the gap, depends on how long and how exposed that gap is, which nobody has measured. If the owner wants that protection, Variant 3 with the explicit item-list sentence from Concessions is the better "yes" than Variant 1.

Overall best answer for the owner: Variant 2, confidence 60%

## Scoring Matrix

| Diff Point | V1 adv | V2 adv | V3 adv | Winner | Confidence | Evidence Summary |
|------------|--------|--------|--------|--------|------------|-----------------|
| S-001 | tie | tie | tie | tie | 90% | Same five sections |
| S-002 | 3 | 3 | 3 | Variant 3 | 90% | Only Variant 3 supplies "the sentence to quote" the question asks for on a yes |
| C-001 | 2 | 2 | 2 | Variant 2 | 90% | Never committing avoids both UNVERIFIED WC-9 readings and adds no owner latency; Variant 1 and 3 advocates conceded |
| C-002 | 2 | 2 | 2 | Variant 2 | 95% | No wording to collect under "Owner latency is the real schedule" (line 523) |
| C-003 | 1 | 1 | 1 | Variant 1 | 90% | Owner's own words per Task meet "word for word ... for that Task" without interpretation |
| C-004 | 3 | 3 | 3 | Variant 3 | 90% | A commit at `worker_done` is the only full protection across the handoff gap |
| C-005 | 2 | 2 | 2 | Variant 2 | 85% | One review, before the commit, by the session that pushes |
| C-006 | 3 | 2 | 3 | Variant 3 | 60% | Writer reports the hook failure; Variant 2 advocate: a worker can only report, the PR session can fix |
| C-007 | 2 | 2 | 2 | Variant 2 | 80% | One commit path per worktree; margin small because the PR session also makes fix commits |
| X-001 | 1 | 2 | 2 | Variant 2 | 65% | Not needing a standing sentence makes the unresolved reading moot |
| X-002 | 2 | 2 | 3 | Variant 2 | 60% | Gap is real but boundable by a "do not clean before the PR session commits" guard; Variant 3 advocate holds it is material |
| A-001 | 2 | tie | tie | tie | 65% | All QUALIFY; all depend on Q25's model equally; a "no" leaves least behind if it fails |
| A-002 | 3 | 3 | 3 | Variant 3 | 90% | All QUALIFY; Variant 3 depends least on the worktree staying untouched |

Overall votes (each advocate's honest judgment after steelmanning): Variant 2 at 65% (Variant 1's advocate), Variant 2 at 70% (Variant 2's advocate), Variant 2 at 60% (Variant 3's advocate). 3 of 3 agree.

Shared-assumption responses: A-001 QUALIFY x3; A-002 QUALIFY x3. No omissions.

Notable evidence raised in Round 1: (1) Variant 2 cites `WORKER-CONTRACT.md:42` for a sentence that is at line 44 (Variant 1 advocate; minor). (2) Variant 2's advocate proposes a guard: the coordinator never removes or cleans a worker's worktree until its PR session has committed; the orchestrator checked `merged-requirements.md` and found no such general rule (only `issue-409-mvp` "Never remove or clean" at line 898, and line 1074 "or clean evidence before reconciliation" on resume). (3) Variant 3's advocate offers a stricter "yes" sentence that names all nine work items so each brief quotes it unchanged (fit still UNVERIFIED).

## Convergence Assessment
- Points resolved: 13 of 13 (majority rule)
- Alignment: 100% (unanimous on 9 of 13)
- Threshold: 80%
- Status: CONVERGED
- Unresolved points: none. Residual minority positions: C-006 (Variant 2 advocate), X-001 (Variant 1 advocate), X-002 (Variant 3 advocate).
