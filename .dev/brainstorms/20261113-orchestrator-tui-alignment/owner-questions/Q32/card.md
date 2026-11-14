# Should helper sessions save their own work as a local commit? (Q32)

**Question in one sentence:** When a supervised helper session finishes a code change, should it save the change as one local git commit (never pushed)? Or should it leave the change uncommitted for the session that later opens the pull request?

**Why you are being asked:** The checked-in worker rules let a helper commit only if its instructions quote your own words allowing a commit for that specific job. No one can supply those words but you. Nothing is blocked. If you do not answer, helpers simply do not commit. The plan asks this when the first code-changing helper is about to start.

**Background you need:**
- A supervised helper ("worker") is an agent session that the Orca app starts in its own working copy of the repository (a "worktree") to do one job. It reports back when done. It never pushes or opens pull requests.
- After the helper ends, a separate session (the "PR session") opens the pull request from that same worktree. Today's plan has that session make the commit. Before any push, you are shown the change.
- This program has up to nine code-changing jobs.
- Unverified: whether one reusable sentence from you counts as "your words for that job", and whether Orca's helper worktree meets the rule's other condition.

**Your options:**

1. **No. Helpers never commit; the PR session commits.**
   - If you pick this: helpers leave changes as uncommitted files. The PR session commits only the named files after you have seen the change. The coordinator (the session running the program) also promises not to delete or clean a helper's worktree until that commit is made.
   - Upside: one way of committing, one review, no extra questions, and it does not depend on the unverified rule readings.
   - Downside: until the PR session commits, the change exists only as loose files. The cleanup promise protects them, but it is not yet a written rule in the plan.
2. **Decide job by job.**
   - If you pick this: each time a code-changing helper is about to start, you are asked "may this job end with one local commit?" Your reply is quoted in its instructions.
   - Upside: meets the rule exactly, and you can add a safety commit only for risky jobs.
   - Downside: up to nine more questions, and waiting on you is already the program's main delay.
3. **Yes, with one sentence for every code-changing job.**
   - If you pick this: you give one sentence now, for example "Each of the nine program jobs may end with one local commit in its own worktree, without pushing". It is quoted in every such helper's instructions.
   - Upside: each change is saved as a commit the moment it succeeds, and it has an exact id to review.
   - Downside: whether one sentence satisfies the rule is unverified. If the rule's check refuses it, you get option 1 plus refusal reports. You must also review helper commits before each push.

**What the debate found:**
- All three debaters, including those assigned to argue for options 2 and 3, chose option 1.
- Its one real weakness is the loose-files gap, so the debate added the "do not clean the worktree before the commit" promise.
- Option 3's benefit depends on two readings of the rule that nobody has checked.

**Recommendation:** Option 1, with the cleanup promise. About 65 percent confidence. This is the plan's recommended answer, plus that promise.

**If you do not answer:** Same as option 1, without the written cleanup promise.

**What this answer does not authorize:** any push, pull request, merge or post by a helper. Pushing still needs you to see the change and say go.

**How to answer:** type `Q32: option 1` (or `option 2`; or `option 3` with your sentence).
