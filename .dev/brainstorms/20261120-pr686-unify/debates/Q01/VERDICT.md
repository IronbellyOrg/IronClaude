# Verdict Q01: Who writes a per-issue grant row

Line references "D:nnn" are to `docs/designs/orchestrator.md` in the master snapshot `/home/coder/.cache/ic-snap-20261120/master` (Clay's merged design from PR 681, the design document). "owner-answers" is `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/owner-answers.md`. "The memory rule" is `/home/coder/.claude/projects/-home-coder-workspaces-IronClaude/memory/approvals-through-chat-never-files.md`.

## Question

The owner's record (OWNER-ANSWERS line 285 in the issue-339 brainstorm folder, see D04 verdict) says PR 585 narrowed the "Ruling in chat" rule and that "other owner records, such as a grant row, are still written by the owner". The owner's memory rule (2026-11-17, `approvals-through-chat-never-files`: /home/coder/.claude/projects/-home-coder-workspaces-IronClaude/memory/approvals-through-chat-never-files.md) says every approval, go and Ruling is given in chat, the agent records it, and the owner is never asked to write a file. Which governs a per-issue grant row (and the cleanup-design approval and `--apply` grants raised by D13)? Read D04 and D13 VERDICT.md first. Context: D04 recommends `answer-check`, a validator that checks a typed chat answer.

## Winner

HYBRID: the owner's chat rule governs who writes the record (the owner says it in chat, the agent records it, nobody hand-writes a file), the owner's rule that only the owner may give the consent stays, and Clay's `answer-check` tests, end-of-go rule and fail-closed default are adopted as checks on the recorded go.

## Winning recommendation

The unified spec must say all of the following; each can be checked.

1. **Governing rule.** A per-issue grant row, the owner's go for `--apply`, and the owner's approval of the cleanup design (issue 687) are each the owner's consent, given by the owner in chat. The agent in that session records it from that chat message. The owner is never asked to write a file. Decision 8's words "the grant row is written by the owner, not by an agent" (owner-answers line 130) mean "owner-sourced, never agent-created". Test: no sentence in the spec, the contract or a brief says the owner writes, types or fills in a grant row or a pass record.
2. **Fix line 57.** `src/superclaude/core/WORKER-CONTRACT.md:57` (master) says "other owner records, such as a grant row or a pass record, are still written by the owner". It becomes: other owner records, such as a grant row or a pass record, are given by the owner in chat and recorded by the agent from that confirmation, naming the exact scope. Test: a search of the contract for "still written by the owner" finds nothing, and the contract test file that PR 585 ran (`tests/skills/test_worker_contract.py`) pins the new sentence. Do this only after the owner's one chat confirmation (Actions, row 1), because the owner's own words behind the current sentence were only "narrow d2".
3. **What a record holds.** The owner's quoted words, the date, the exact scope (issue or PR number; for a merge the head sha; the list of writes) and who recorded it. A go missing any field is refused, and an agent-made record with no owner chat confirmation of that exact scope is "executor-invented approval" (same rule as a Ruling line, `~/.claude/skills/sc-implement-protocol/refs/qa.md:248-249`).
4. **Checks on a recorded go (adopted from `answer-check`, D:694).** Accepted only if: typed by a person in their own session or terminal and never relayed by an agent; it names the right issue or entry; it is newer than that entry's last edit; its question key matches (for a merge `merge_safety:<PR>:<head sha>`, D:598). The owner identity is a parameter, not Clay (D:694 names Clay). Until the script exists these four checks are what the coordinator does by hand against the record's fields. Test: a relayed, stale, wrong-entry or wrong-key go is refused in a test of the future verb.
5. **A go ends.** It ends when the named action is done, for a merge also when the PR head moves, and when the owner revokes it in chat. Test: a merge go for head X does not release a merge of head Y.
6. **Fail closed and a use log.** With no recorded go there is no write; each use names the go it relied on (D:696 for the log; `src/superclaude/cli/issue_watch/repos.py:295` in PR 686's head snapshot reads a missing `grants` key as an empty list).
7. **Standing versus per action.** The old per-issue row has no reader in master since PR 682 (the writes it covered are the plan reply, marker, mention, label and Status). Per the D04 verdict four low-stakes writes are standing (`issue.assign`, `issue.comment`, `issue.body.append_plan_sections`, `issue.hold`). Merge, close, `--apply` and the cleanup-design approval are per-action chat goes. The debate left the standing-versus-per-action split on the four low-stakes writes unresolved (point C-002), so this item rests on D04, not on a debate win. The per-issue row is not restored as an owner-written file.
8. **`--apply` and the cleanup design (D13).** `--apply` runs only on a recorded owner go that names that action. The owner's approval of the cleanup design is recorded the same way before any build of issue 687. The agent records it locally and posts to issue 687 only on an instruction that names that post.

## Strongest points

**OURS**
1. The consent must come from the owner, never from an agent: Decision 8 ("the grant row is written by the owner, not by an agent", owner-answers line 130), and the contract's "executor-invented approval" rule (`WORKER-CONTRACT.md:57`; `qa.md:248-249`).
2. The owner's own order covers grants, and the line-57 grant-row sentence has no owner words behind it: the owner said only "narrow d2" and "publish narrow d2"; owner-answers line 285 says the row "is NOT an owner approval of the rest of the D2 amendment"; the sentence came from the fix agent's reading of Decision 8 (PR 585 body). Memory rule: "every approval, written acceptance, go, input ... and Ruling is given ... in chat".
3. A chat route for outward actions is already built: master `WORKER-CONTRACT.md:241` ("only when the user's instruction names that action", possibly in its live conversation); `issue-pipeline-fu1.md:106` ("the owner never has to write a file"). And the Ruling-line rule already works from a chat confirmation (`qa.md:248-249`).

**CLAY**
1. `answer-check` gives a check on the source, entry and freshness of a typed answer, where an agent-recorded go has none (D:694). OURS admits "no script checks the recorded row today".
2. The question key `merge_safety:<PR>:<head sha>` (D:598) gives the go an end when the head moves; neither paper had an expiry (shared assumption A-003).
3. Fail closed and logged: a missing `grants` key reads as empty (`repos.py:295`, PR 686 head), `E-NO-GRANT` refuses and logs each use (D:696). Also, D:116 retires the old per-issue row, which no code in master reads (PR 682, commit `01e7a9e23`).

## Clay strengths to adopt

- **The four `answer-check` tests (source is a person's own typed input and never relayed; right entry; newer than the entry's last edit; question key).** Why: fills the gap that a recorded go has no check. Merge: required of any recorded go; owner identity parameterised (D:694 hardwires Clay).
- **Question-key and head-sha binding, and an end for every go.** Why: neither paper had an expiry or a revocation path (A-003); a merge go for one head must not release another. Merge: add as recommendation 5.
- **Fail-closed default and a use log.** Why: separable, cheap, both advocates accepted it (C-006). Merge: recommendation 6. Do not rely on `E-NO-GRANT` as the main control: it covers at most two of the six entries (D:696; D04 verdict item 6).
- **Standing grants for the four low-stakes writes.** Why: there is no person at each step of the plan agent's writes (D:116). Merge: as in D04 (four standing; merge and close per action).
- **Explicit coverage of the cleanup-design approval and `--apply` (the D13 items).** Why: the OURS paper omitted the cleanup design (both scorers). Merge: recommendation 8.

## Our strengths that must be kept

- Consent comes only from the owner: an agent never creates its own permission, and "executor-invented approval" stays refused.
- The chat-only rule of 2026-11-17: the owner gives every approval in chat and never hand-writes a record.
- No standing merge or close: per-action chat goes (D04 verdict; contract lines 241 and 245 as they literally read).
- The Ruling-line pattern (agent records from the person's own chat confirmation naming the exact scope) as the built precedent.

## Actions

| Action | Type | Target (file, PR or issue number) | Order or dependency |
|---|---|---|---|
| Owner confirms in chat the one reading: grant rows, `--apply` goes and the cleanup-design approval are given in chat and recorded by the agent, and "narrow d2" did not restore an owner-written file row | DECISION | Repository owner `ironbelly`; `src/superclaude/core/WORKER-CONTRACT.md:57` | First |
| Replace the "still written by the owner" clause with the chat-and-record wording; keep the "executor-invented approval" sentence | LOCAL CHANGE | `src/superclaude/core/WORKER-CONTRACT.md:57` (source of truth; later `make sync-dev`) and its test `tests/skills/test_worker_contract.py` | After row 1; new PR from the owner's line, not a revert of PR 585 |
| Write recommendations 3 to 6 into the unified spec; parameterise the owner identity in `answer-check` | DOC | `docs/designs/orchestrator.md` D:688, D:694, D:696 (inside the unified rewrite, topic D14) | Before PR B is built |
| Reword "a separate live-test grant row" so the live-test go is a chat go recorded by the agent | DOC | `docs/designs/issue-pipeline-fu1.md:24,26` | With row 2 |
| Add to issue 687's acceptance: `--apply` needs a recorded owner go that names the action; the cleanup-design approval is recorded from chat | PR KEEP-ADAPT | Issue 687 (a request, nothing built) | After row 1; before any build |
| Keep the `grants` reading as written (missing key is an empty list); remove `pr.merge` and `issue.close` from the default list per D04 | PR KEEP-ADAPT | PR 686 (`repos.py:295`) | With the D04 action |
| Decide who "the owner" is for `answer-check` and for changing grants | DECISION | Topics D06 and D16 | With D06 |
| No revert or close of a PR is recommended by this topic | PR KEEP | PRs 681 to 686 | None |

## Implications

- **Watcher.** The poll writes nothing to GitHub, so a recorded go does not change it. If a standing list is used for the four low-stakes writes, its file must sit outside the orchestrator's write reach or be guarded by a hook (D:688; D04 verdict).
- **Coordinator or orchestrator.** Every merge, close, `--apply` and cleanup run starts from a recorded go; the merge gate gains the reason "no recorded merge go" (D04 verdict) and the go ends when the PR head moves. The coordinator reads the record and refuses a go with a missing field.
- **Dashboard and observer.** None decided; whether the open goes should show in the observer report is UNVERIFIED.
- **Claim pipeline.** `/sc:issue --claim` is unchanged. PR 682 already deleted the old plan-approval and grant-row machinery from master, and nothing replaced the human approval of a plan (FULL-REPORT.md section 3); this verdict does not restore it.
- **What breaks.** Any text that tells the owner to write a row (line 57 of the contract, `issue-pipeline-fu1.md:24,26`); Clay's `answer-check` for any person other than Clay until the owner identity is a parameter. The installed copy on this host, `/home/coder/.claude/WORKER-CONTRACT.md`, is the version from before PR 682: it still has WC-17 and line 300 ("post an issue write without that issue's grant row"), so a coordinator session here can still be told to require a row that nothing writes until the next `superclaude install`.
- **What the owner must know.** The sentence that keeps the grant row owner-written came from the fix agent's reading of Decision 8, not from owner words (PR 585 body; owner-answers line 285); the owner decides it with one chat message. `ironbelly` is a login shared with every session on this host (owner-answers line 162), so a chat go does not by itself prove who gave it.

## Confidence

75 percent. The debate did not converge (64.3 percent against 80, status partial; in four of the five unresolved points both advocates endorse adopting the same Clay element), but both advocates agree on the governing rule, on rejecting a standing merge and close, and on adopting the checks. It would change if the owner says "narrow d2" was meant to keep an owner-written row, or if the order and timezone of the memory rule (00:21Z) against "narrow d2" (04:46) show the narrowing came later and was meant to restore it.

## Unverified

- Whether the owner meant "narrow d2" to keep an owner-written grant row. The order and timezone of the owner's messages that day are not shown (memory modified 2026-11-17T00:21Z; owner-answers times 04:46 and 04:51 carry no timezone).
- `answer-check`, `E-NO-GRANT` and the `repos` verbs are read from the design text (D:688, D:694, D:696) and are not built (PR B, D:1020).
- U37 (D:1295): that any agent on the host can type into an orchestrator terminal; read from the design, not tested.
- The commit `bfabf1d63` for PR 585 comes from owner-answers line 285; one scorer could not confirm it. The merge time (2026-11-17T05:03:09Z) and the PR text were read with a read-only `gh pr view 585 --repo IronbellyOrg/IronClaude`.
- One scorer said `docs/designs/orchestrator.md` lines 37 and 76 also contain "grant row"; a case-insensitive search of the master snapshot found only `orchestrator.md:116` (plus the contract line 57 and `issue-pipeline-fu1.md:24,26`). Not resolved; it does not change the verdict.
- The debate agents and scorers were same-family agents run by one orchestrating session; the quantitative scores were estimated by hand. Clay's `RULINGS.md` and chat or call agreements were not read.
- The names of the four standing low-stakes entries are read from Clay's six-entry list minus `pr.merge` and `issue.close`; they are not quoted from the D04 verdict.

## Debate artifacts

All under `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/Q01/`:
- `position-OURS.md`, `position-CLAY.md`
- `adversarial/return-contract.yaml` (worker contract), `adversarial/merged-hybrid-position.md`
- `adversarial/adversarial/diff-analysis.md`, `debate-transcript.md`, `base-selection.md`, `refactor-plan.md`, `merge-log.md`, `return-contract.yaml`
- `adversarial/adversarial/variant-1-original.md`, `variant-2-original.md`
- Adversarial status: partial (depth quick, one round, two advocates, two scoring passes, merge-executor; Round 2, Round 2.5 and Round 3 skipped by depth).
