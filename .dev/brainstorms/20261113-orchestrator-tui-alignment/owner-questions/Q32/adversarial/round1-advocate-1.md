# Round 1 Advocate Statement: Variant 1 (Proposal A, decide each Task's commit at dispatch)

## Position

Variant 1 answers Q32 with "not as a standing rule": at each code-changing dispatch the coordinator asks the owner whether that one Task may end with one local commit, quotes the owner's own reply in that Task's brief, and records `GRANT(<item>,commit)`; with no yes, the worker leaves its changes uncommitted and the PR session commits (variant-1, "Answer").

Its case rests on three verified points:

1. It is the only "yes" path that meets WC-9 at its strictest. WC-9 allows a worker commit only when "the brief quotes, word for word, the user's instruction naming a local commit for that Task" (`WORKER-CONTRACT.md:42`). A per-Task owner reply is, literally, the user's instruction for that Task. Nothing has to be interpreted.
2. It matches the contract's own grain. "A commit grant covers one Task and ends at that Task's `worker_done`" (`WORKER-CONTRACT.md:244`). A per-Task question gives a per-Task grant with no standing permission in the ledger.
3. Its fallback is exactly the spec's default. With no yes or no reply, the result is spec 6.4 rule 14: "by default a supervised worker leaves its changes uncommitted and unstaged outside WC-9's grant; the PR session (6.3) stages and commits named paths" (`merged-requirements.md:987`). So Variant 1 never does worse than Variant 2 when the owner is silent.

It also fits the spec's question cadence: "Ask one question at a time ... Q27, Q28, Q29, Q30, Q32 are asked when their item is next" (`merged-requirements.md:523`). Variant 1's questions arrive one at a time, each at the dispatch it governs.

## Steelman of Variant 2

The strongest version of Variant 2: one program, one commit path, zero extra owner questions. The session that pushes is the session that committed, so "what is pushed is exactly what that session committed and checked" (variant-2, "What it unlocks"). The person reviews the diff once, before the commit, instead of reviewing worker commits before the push as `WORKER-CONTRACT.md:244` would require. It is the spec's recommended answer and the default if unanswered (`merged-requirements.md:559`), so choosing it changes nothing in the spec text, the brief rule (`merged-requirements.md:1070`) or the gate list. And the PR session already makes commits in the worktree anyway: a `pr-submit` row lists "local fix commits ... in the worktree" (`merged-requirements.md:1050`). It also respects the stated bottleneck, "Owner latency is the real schedule" (`merged-requirements.md:523`), better than any alternative. Finally, if Q25 is answered with its alternative ("a top-level agent per PR item ... and no worker", `merged-requirements.md:552`), a plain "no" costs nothing, while the other two variants would have spent owner attention for no workers.

What it gets right: simplicity, zero added owner load, a single review point, and alignment with every existing spec rule.

## Steelman of Variant 3

The strongest version of Variant 3: the uncommitted gap is real and a commit closes it. Between `worker_done` and the PR session's commit, the change is only loose files; a commit makes it a fixed revision whose id travels in the `worker_done` body (`WORKER-CONTRACT.md:43`, "gives the commit ID in its `worker_done` body"), so the coordinator, the person and the PR session all look at the same thing. A pre-commit hook failure (`verify-sync`) surfaces in the session that wrote the change rather than in a later session that has to reconstruct intent. And it costs one owner answer for all nine Tasks instead of nine. It also directly answers the question as asked: "If yes, give the sentence to quote" (`merged-requirements.md:559`); Variant 3 is the only variant that hands the owner that sentence.

What it gets right: durability of the change across the handoff, a fixed revision for review, early hook failures, and minimal owner load for a "yes".

## Key strengths claimed

- **Strict WC-9 compliance.** The quoted text is the owner's own words for that Task (`WORKER-CONTRACT.md:42`). No reader of the brief can doubt it, so no commit is refused on a wording technicality. Variant 3 itself flags that its filled-in template's fit is UNVERIFIED (variant-3, "What it costs or risks").
- **No standing permission.** The ledger never holds a reusable commit sentence that could be applied to a Task the owner never considered (variant-1, "What it unlocks").
- **Judgment where it matters.** The owner can grant a commit for a large or risky change that benefits from a checkpoint and decline it elsewhere. This is the only variant that lets the commit decision follow the actual Task.
- **Safe default.** Silence or "no" falls back to spec 6.4 rule 14 (`merged-requirements.md:987`), the same outcome as Variant 2.
- **Fits the existing question schedule.** Q32 is already asked "only when the first code-changing worker is dispatched" (`merged-requirements.md:559`); Variant 1 extends that same moment to later dispatches.

## Weaknesses identified in Variant 2

- **The uncommitted gap is accepted, not bounded.** Variant 2 itself says the gap length is UNVERIFIED and lists "How long uncommitted work may wait" as unresolved. If the PR session is late (Q25's sequential launch in a `worker-start` worktree is itself UNVERIFIED, `merged-requirements.md:552`), loose files sit longest exactly where nothing protects them.
- **No fixed revision.** The coordinator reviews with `git status` and `git diff` rather than a commit id (variant-2, "What it costs or risks"), so what the person reviewed and what the PR session later commits are linked only by the worktree staying untouched.
- **All hook and commit load on the PR route.** It adds to the load INV-001 already places on the PR session (variant-2 says so). The PR session must commit someone else's change and handle any `verify-sync` failure it did not cause.
- **Minor citation error.** Variant 2 cites `WORKER-CONTRACT.md:42` for "Outside that grant a worker never runs `git add` ... never commits"; that sentence is at line 44. The substance is correct.
- **Closes the door entirely.** For this program the grant table can never hold a worker commit row, even for a Task where the owner would want one.

## Weaknesses identified in Variant 3

- **WC-9 fit is unproven.** WC-9 requires "the user's instruction naming a local commit for that Task" quoted "word for word" (`WORKER-CONTRACT.md:42`). In Variant 3 the coordinator, not the owner, fills in the Task id and item. A strict brief guard can read that as the coordinator's instruction, refuse the commit, and leave the worker reporting a refused commit (variant-3 admits this). The design's main benefit then fails silently in the worst case.
- **Standing permission against a per-Task design.** `WORKER-CONTRACT.md:244` makes each grant end at one `worker_done`; Variant 3 concedes that a standing permission "is broader than the contract's one-grant-per-Task design intends".
- **Two review steps instead of one.** Worker commits must be shown before every push (`WORKER-CONTRACT.md:244`), and the PR session still adds its own fix commits (`merged-requirements.md:1050`), so the person sees worker commits plus PR-session commits.
- **Contradicts the spec's recommendation and default** (`merged-requirements.md:559`), so it requires changing spec 6.4 rule 14's framing from default-uncommitted to default-committed for code workers.
- **Child worktree condition unverified.** WC-9 condition 2 needs "its own child worktree created by Orca"; whether a `worker-start` worktree qualifies is UNVERIFIED (question.md fact 7). This applies to Variant 1 too, but Variant 3 bets all nine Tasks on it.

## Concessions

- **Owner latency is my biggest weakness.** Up to nine extra questions in a program where "Owner latency is the real schedule" (`merged-requirements.md:523`). A dispatch can wait on an answer, and that delay is a direct schedule cost. Variant 2 has none of it; Variant 3 has one question.
- **Two commit paths.** Some worktrees end with a worker commit and some without, so the coordinator and the PR session must check which applies in each (variant-1 says so). Variant 2 has one path.
- **Variant 1 does not answer the question in the form asked.** Q32 asks "If yes, give the sentence to quote". Variant 1 gives neither a firm no nor a sentence; it defers. An owner who wants one decision now gets nine later.
- **The child worktree condition (WC-9 (2), WC-11) is UNVERIFIED for Variant 1 as well.**
- **The flexibility may be unused.** Nothing in the spec identifies a Task among the nine that needs a mid-handoff checkpoint, so the benefit of per-Task judgment is speculative.

## Shared assumption responses

- **A-001 (the PR session runs later in the worker's own worktree, Q25 model): QUALIFY.** All three variants depend on it, and the spec itself marks "that Orca permits a second, sequential agent launch in a `worker-start` worktree" as UNVERIFIED (`merged-requirements.md:552`). If the owner picks Q25's alternative (no worker), Q32 governs nothing; that outcome favors the cheapest answer, which is Variant 2. The assumption should be confirmed by Q25's answer before Q32 is asked, which the spec's ordering (Q25 in W0 intake, Q32 at first code-changing dispatch, `merged-requirements.md:523`) already does.
- **A-002 (the worktree stays as the worker left it until the PR session): QUALIFY.** It is supported by the single-live-agent-per-worktree rule (spec 6.2, per the diff analysis) and by `WORKER-CONTRACT.md:245` ("The coordinator commits or merges in a worktree only when no worker runs there"), but nothing bounds the time, and a coordinator clean, a stray checkout or a shared-stash pop is not mechanically prevented. It holds well enough to make Variant 2 acceptable, not well enough to make the gap zero risk.

## Per-point verdicts

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

## Overall

After steelmanning, Variant 2 is the better answer for this program: it adds no owner questions in a latency-bound program, keeps one commit path and one review point, and matches the spec text already written. Variant 1's real advantage (strict WC-9 fit with per-Task judgment) matters only if the owner actually wants worker commits for some Tasks, and the owner can still get that later by revising Q32 for a specific Task. Variant 3's durability gain is real but rests on an UNVERIFIED reading of WC-9.

Overall best answer for the owner: Variant 2, confidence 65%
