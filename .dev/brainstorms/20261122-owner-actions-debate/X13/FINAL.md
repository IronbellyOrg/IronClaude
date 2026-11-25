# X13 FINAL: how to handle Clay's self-merge of PR 700 (Appendix B.3 action 3)
Reconciler's note, 2026-11-22. Read-only work. Everything here is a recommendation until the owner says so in chat. "Clay" is login clayphi (they/them). Agents A and B ended round 3 with no disagreement on substance; I checked the heaviest claims myself (section 10).

## 1 Unified proposal
Answer B.3 action 3 with a third option. PR 700 stands as merged. Record it as a repair and a gap in the safeguards, not a rule breach and not a precedent. Tell Clay privately, with thanks. Apply a short interim request until the review gate on master (X03) is live and its test has passed. Use PR 700's two gated files as the replay case for that test. Post nothing public now.

Order:
1. Before the owner answers, an agent shows the file comparison in chat (read only, about 15 min, ESTIMATE): the 87 files that PRs 681 to 684 touched, before PR 681 against after PR 700.
2. Owner says the sentence in section 7.
3. Agent records one entry in the interim ledger of owner answers (SPEC.md line 354, row L-01, rule SEC-14): the owner's quoted words, date, scope "X13 / B.3 action 3", recorder. It marks SPEC.md line 788 (B.3 action 3) and the DECISIONS.md row at line 1369 as answered, pointing at L-01. In that DECISIONS.md row it removes the stray comma and replaces "not re-checked" with the 2026-11-22 reading (no ruleset, no branch protection, no CODEOWNERS file). FR-75 to FR-78 stay untouched (Appendix B was not re-reviewed).
4. Agent adds a replay case to the throwaway-test plan (FR-77): one line under `docs/designs/` and one in `src/superclaude/core/WORKER-CONTRACT.md`. Expected result: merge blocked, review required. The throwaway PRs still need their own owner go.
5. Agent queues one public line for `docs/decisions.md` (FR-78), wording approved in chat: "PR 700 (2026-11-20) rolled back PRs 681, 682 and 684 and was merged without an owner review. No review rule or server setting existed then. It stands as a repair, not a precedent." No login, no timing, no "would have been blocked". After the throwaway test passes, one sentence naming the rule then in force is added.
6. Agent drafts the note to Clay. The owner approves the wording and sends it; an agent never posts it. Draft (about 85 words): "Thank you for the rollback in PR 700. I accept it as merged. It also showed a gap: a 63-file change to design and contract files merged and nothing in the repository asked for a second look. That is a gap in our setup, not a fault of yours. I will propose a review rule on a few paths and ask you to accept the roles text first; tell me before I announce the roles if you disagree. Until it is live, please ask me in chat before merging a change under `docs/designs/`, to `WORKER-CONTRACT.md`, or to `.github/CODEOWNERS`. This does not decide the plan-approval gates or the report skill; I will tell you when it does."
7. Timing: send it with the roles chat (D16 rank 1) if that chat happens within 3 working days of the answer; otherwise send it alone.

Interim request (until the ruleset is active and the replay test has passed):
- Clay asks the owner in chat before merging a PR on the three paths. The owner's typed go naming the PR number is the permission. Silence is never a yes; after 3 working days the asker asks again.
- Agents on the shared `ironbelly` login never merge a PR on those paths without that typed go and never pass `--admin`. This binds our side only; it goes in the ledger, not in the note.
- If the ruleset is not active 14 days after the answer, the open-decisions list shows X03 as overdue. The request is neither dropped nor extended silently.
- No "second approval" clause for Clay and no hold on drafts 686 and 690 in the note: both are rule text or status Clay has not accepted (FR-76).

## 2 Context
- PR 700 (Clay, 63 files, +4599 -11935) was opened 2026-11-20 14:46:34Z and merged by Clay at 15:07:32Z, 20 min 58 s later. Reviews were Augment and Codex bot comments only. PR 682 was merged by Clay 66 min after opening; PR 684 by its author after 2h29m (A and B; I re-read PR 700, 682).
- No rule was in force: branch protection on master returns 404, rulesets return `[]`, no CODEOWNERS file, no `docs/decisions.md` on origin/master. FR-76 needs Clay's written acceptance of the roles first, which has not happened.
- PR 700 changed two gated paths: `docs/designs/orchestrator.md` (removed) and `src/superclaude/core/WORKER-CONTRACT.md`. D16 exempts a revert only for "one named PR in full" and never from the gate; PR 700 reverted three PRs.
- The owner merged PR 701 on top of PR 700 at 16:53Z on the same day, and closed their own PR 697 (same aim for PR 682 only). Self-merge is the norm: 89 of the last 100 merged PRs were self-merged (D16 section E).

## 3 Implications
- Changes: B.3 action 3 closes; the replay test gets a real case; Clay gets one clear message and a narrow request.
- Stays blocked or open: B.3 actions 1, 2 and 4 (restore the design text, restore the report skill, answer OA-1) are not answered here. X03 is not delayed. The words "would have been blocked" stay unproven until the throwaway test passes. PR 711 (Clay, open, not draft, 266 files, no gated path) is covered by nothing and is a separate owner question.

## 4 Benefits
Clay keeps credit for a repair that matches the owner's intent, which makes accepting the roles (needed by X03) likelier. No public text blames anyone. The plan row closes at near zero cost, and the answer is reversible in one chat sentence.

## 5 Risks and containment
- A request binds nobody (PR 681's own text said "the owner reviews" and it was self-merged). Contain: say so openly; X03 carries the weight; the 14-day overdue flag.
- Clay may read thanks as licence. Contain: "gap" and "ask first" are in the note; the record says "not a precedent".
- Owner and agents look the same on the shared login, so an owner go cannot be told from an agent act. Contain: the go must name the PR number; out of scope to fix here.
- The comparison could show a surprise. Contain: it runs before the owner answers.
- The ledger sits under `.dev/tasks/`, which is tracked and may become public. Contain: neutral wording, no blame words, in the ledger too.
- Appendix B was not re-reviewed. Contain: edit only the answered marks.

## 6 Costs (ESTIMATES; basis: steps counted by A and B, similar ledger edits in this plan)
Owner: about 10 min in chat plus sending the note. Agent: 45 to 60 min including the 15 min comparison. The `docs/decisions.md` line adds nothing beyond FR-78's 1 to 2 h.

## 7 The sentence the owner says in chat
"X13: PR 700 stands as merged. It is a repair and shows a gap, not a breach, because no rule was in force. It is not a precedent and it does not answer OA-1. Record it, use it as the replay case, and draft the note to Clay for me to send. The interim rule applies from now. Go."

## 8 What an agent does after it
Steps 3 to 6 above: local files only, no GitHub write. It writes L-01, marks the two plan rows, adds the replay case, queues the `docs/decisions.md` line, shows the draft note and waits for the owner's approval of the wording. It runs `git add .dev/tasks` and commits only when asked. It opens no PR for the `docs/decisions.md` line until X03 work needs one, and then only with `/sc:pr-submit --monitor 3`.

## 9 Consensus
Full. Agents A and B state no residual disagreement. Three choices stay with the owner:
1. Channel to Clay. Owner's own private channel (which one: UNVERIFIED): the note goes as drafted. None exists: a neutral comment on issue 290 (assigned to Clay) giving only the interim request and not naming PR 700, which is a GitHub write needing its own go; Clay gets a weaker message and no thanks.
2. One message or two. Combined with the roles chat: Clay hears once. Alone: Clay hears sooner, the roles announcement comes later.
3. PR 711. "Ask Clay to wait": add one line to the note; costs a delay on 266 files and treats Clay differently from the rule. "Leave it": it proceeds with no owner look.

## 10 What could not be verified
- Which private channel the owner and Clay use.
- Whether the gate would have blocked PR 700 (needs the throwaway test).
- I verified by gh reads today: PR 700 times, size, merger and bot-only reviews; PR 682, 701 times and mergers; PR 711 state; branch protection 404; rulesets `[]`; no CODEOWNERS or `docs/decisions.md` on origin/master; the two gated files in PR 700; SPEC.md line 354 and DECISIONS.md line 1369; D16 sections B, E, G.
- File comparison, my run (before PR 681's parent against PR 700's merge, 87 files): 27 differ. 17 are added files that belong to `/sc:closeout` (kept on purpose, per the plan) and its tests and design doc; 10 are edits (CHANGELOG, NOTICE, two guides, two HOW-WE-WORK copies, WORKER-CONTRACT, three tests). This matches B's count of 10. I did not read those 10 line by line, so "only expected differences" is UNVERIFIED. SPEC.md line 788 (B.3 action 3), the closing of PR 697 and the 89-of-100 figure come from the agents and the plan files; I did not re-read or re-run them.
