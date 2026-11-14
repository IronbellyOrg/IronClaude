# Should this program's coordinator run your 10-minute read-only check? (Q31)

**Question in one sentence:** Does your 2026-11-05 order to run a check about every 10 minutes apply to the coordinator of this program, as a read-only check?

**Why you are being asked:** Your order exists only in a memory note, which the plan ranks as its least reliable source, so the plan will not assume it either way. Nothing is blocked. Your answer sets whether one extra recurring check runs.

**Background you need:**
- The coordinator is the Claude session that runs this program and supervises its helper sessions.
- Orca is the app that runs those sessions and carries their messages. The checked-in coordinator rule (WC-16, in the worker contract) already makes the coordinator keep waiting on Orca, and run a status sweep at most once every 5 minutes.
- Your 2026-11-05 order adds a timer, about every 10 minutes, that reads: the Orca job's messages, the list of live sessions, open pull requests on IronbellyOrg/IronClaude and IronbellyOrg/Coder, and renews "tell me when you go idle" requests on busy sessions. You gave it after sessions went unwatched. Sessions that are not Orca workers never show up in Orca's message queue.
- This program will have such sessions: the sessions that open pull requests, and the session that owns PR #539. The sweep command that could list them does not work yet. It needs PR #539 merged and installed first.
- The timer tool stops after 7 days and only fires while the coordinator is idle.

**Your options:**

1. **Yes, read-only, for this program only.**
   - If you pick this: the coordinator starts one timer at the start of the program, records its id and expiry in the decision record, and restarts it after 7 days or after a restart. It reports only when you need to decide something. It never writes and never runs the sweep more often than the 5-minute limit allows.
   - Upside: the program's non-worker sessions and pull requests are seen within about 10 minutes. It matches your order.
   - Downside: a second clock, about 144 reads a day, and the timer can quietly stop if a restart is missed.
2. **No, keep only the checked-in coordinator rule.**
   - If you pick this: no timer. Pull requests are read at phase gates and when the coordinator wakes.
   - Upside: one rule in one checked-in file, less load, nothing to restart.
   - Downside: sessions that are not Orca workers go unwatched until the sweep command works, which is the failure your order was meant to prevent.
3. **Yes, and also write it into the coordinator rules for every project.**
   - If you pick this: same as option 1 now, plus a separate small pull request that adds the check to the worker contract.
   - Upside: future coordinators get the rule without being asked.
   - Downside: changes a file every project receives, on the basis of a one-program question. Adds a pull request now. Its wording is not settled.

**What the debate found:**
- All three debaters, including those assigned to argue for options 2 and 3, chose option 1.
- Option 2 leaves non-worker sessions unseen before the sweep command works.
- Option 3's contract change is sound, but it should be asked as its own item.
- The debate added these details: the check runs only while the coordinator is idle, it sends no messages to the sessions, and it is silent unless a decision is needed.

**Recommendation:** Option 1, about 70 percent confidence. This is the same as the plan's recommended answer.

**If you do not answer:** The coordinator follows only the checked-in rule (no timer). Q31 stays listed as open at the top of the decision record.

**What this answer does not authorize:** running the sweep more often than once every 5 minutes, any write of any kind, or any grant of permission.

**How to answer:** type `Q31: option 1` (or `option 2`, or `option 3`).
