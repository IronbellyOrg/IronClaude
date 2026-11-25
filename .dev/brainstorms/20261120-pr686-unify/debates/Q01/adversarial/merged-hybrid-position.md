<!--
Provenance: merged from two debated positions using refactor-plan.md (8 planned changes).
Base: Variant 1 (OURS)
Non-base source: Variant 2 (CLAY)
Merge date: 2026-11-20
-->
# Merged hybrid position (Q01): who writes a per-issue grant row

<!-- Source: Base (original, modified): abbreviations kept; "pr-a" added from Variant 2 Abbreviations because Change 5 cites repos.py in pr-a -->
Abbreviations: "master" = `/home/coder/.cache/ic-snap-20261120/master`; "owner-answers" = `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/owner-answers.md`; "D:nnn" = `docs/designs/orchestrator.md` line nnn in master (Clay's design from PR 681, the design document); "pr-a" = `/home/coder/.cache/ic-snap-20261120/pr-a` (Clay's PR 686 head, the poll rewrite).

## Claim

<!-- Source: Base (original, modified): opening rewritten per Change 1 (widened to the three consents the topic names, Variant 2 cited fact 8) and Change 2 (ruling on which record governs; owner intent marked UNVERIFIED) -->
A per-issue grant row, and the other per-action consents named in the Scope section below, are the owner's own consent for one named action and one named list of writes. Each must come from the owner and must never be created by an agent on its own. That provenance rule is the owner's line.

Which record governs: the owner's order of 2026-11-17 (every approval is given in chat) governs the mechanics. The owner says the go in chat, the agent records it from that chat message, and the record names the exact scope. The owner is never asked to write a file. Decision 8's words "the grant row is written by the owner, not by an agent" are read as "owner-sourced, never agent-created", because that limit is aimed at an agent creating its own permission (cited fact 1).

Open point, UNVERIFIED: whether the owner's "narrow d2" (11-17 04:46) was meant to restore an owner-written file row. The order of that message against the 2026-11-17 chat rule, and the timezone, are not shown in the record. One chat confirmation from the owner settles it.

## Scope

<!-- Source: Variant 2 cited fact 8 (D13 and D04 verdicts), Change 1: three consents the topic names; Change 6: standing versus per-action, taken from the D04 verdict, with C-002 left unresolved -->
Three consents are in scope: the per-issue grant row, the owner go for `--apply`, and the owner approval of the cleanup design (issue 687).

<!-- Source: Variant 2 mechanism step 1 and cited fact 1 (D:291, D:872, D:116), Change 6; base (original) cited facts 7 and 8 for the per-action side -->
Which of these are standing and which are per action:

- The writes the old per-issue row covered (plan reply, marker, mention, label, Status) are covered, per the D04 verdict, by four standing low-stakes grants. In Variant 2's list these are `issue.assign`, `issue.comment`, `issue.body.append_plan_sections` and `issue.hold` (D:291, D:872; DQ6 at D:116).
- Merge, close, `--apply` and the cleanup-design approval are per-action goes, given in chat by the owner (D04 verdict for merge and close per PR; D13 verdict for `--apply` and the cleanup design).
- The old per-issue row has no reader in master since PR 682 (cited fact 7). The question is therefore reframed from "who writes the per-issue row" to "who records a per-action owner go". It is not dropped: line 57 of the contract still names the row, and the issue 687 approvals are the same kind of consent.
- Whether the four low-stakes writes should be a standing list at all was not settled in the debate (point C-002 stayed unresolved). This text takes the split from the D04 verdict and claims no debate win for it.

## Mechanism

<!-- Source: Base (original): steps 1 to 3 -->
1. The owner types the go for one issue in chat, naming the issue and the writes.
2. The agent in that session records the row (quoting the owner's words and the date) in its ledger.
3. A row an agent writes without the owner's own chat confirmation of that exact scope is "executor-invented approval" and is refused. This is the same rule that already governs a Ruling line.

<!-- Source: Variant 2 mechanism step 4 (D:694, D:598) and cited fact 6, Change 3: tests from answer-check adopted as requirements for the recorded go -->
4. Checks on the recorded go. These are taken from the `answer-check` design (D:694), which is designed but not built (PR B, D:1020). A recorded go is accepted only if all of these hold:
   - It was typed by a person in their own session, never relayed by an agent. (Variant 2's form of this test: the person's own typed input in the orchestrator's terminal, or a ClickUp reply from their id.)
   - It names the right entry or issue.
   - It is newer than the entry's last edit.
   - Its question key matches. For a merge the key is `merge_safety:<PR>:<head sha>` (D:598).

   The owner identity must be a parameter. D:694 names Clay as the source of an accepted answer (D04 verdict, "parameterise the owner identity"), which is wrong for this repository. Until a script exists, the agent records the owner's quoted words, the date and the exact scope, and a go without those fields is refused.

<!-- Source: Variant 2 key binding (merge_safety:<PR>:<head sha>, D:598) and base (original) precedent that a Task-scoped grant ends at that Task's worker_done (contract line 245, as cited in the refactoring plan), Change 4 -->
5. How a recorded go ends. It ends when the named action is done. For a merge it also ends when the PR head moves, because the key in step 4 includes the head sha. It also ends when the owner revokes it in chat.

<!-- Source: Variant 2 cited facts 3 and 4 (D:696, repos.py:295 in pr-a), Change 5 -->
6. Fail closed, and keep a use log. With no recorded go there is no write. Each use names the go it relied on. (Variant 2's design logs each grant use, D:696, and reads a missing `grants` key as an empty list, `src/superclaude/cli/issue_watch/repos.py:295` in pr-a, as recorded in the D04 verdict.)

## Cited facts

<!-- Source: Base (original): facts 1 to 6 and 9 -->
1. Decision 8, answered "Approved" by the owner: "one grant row per pipeline issue, created when the issue is claimed ... the grant row is written by the owner, not by an agent" (owner-answers line 130). The limit is aimed at an agent creating its own permission.
2. The owner's rule of 2026-11-17 (memory file `/home/coder/.claude/projects/-home-coder-workspaces-IronClaude/memory/approvals-through-chat-never-files.md`): every approval, written acceptance, go, input and Ruling is given by the owner in chat, the agent records it, and the owner is never asked to "hand-write a ledger record". The owner ordered the file-writing requirement "removed from the whole framework".
3. The merged contract text keeps the grant row owner-written: `src/superclaude/core/WORKER-CONTRACT.md:57` in master says "other owner records, such as a grant row or a pass record, are still written by the owner". PR 585 (docs fix that narrowed the D2 wording, merged 2026-11-17 05:03:09 UTC, commit `bfabf1d63`) put it there.
4. The tech-reference twin, `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:722` in master, does not carry the grant-row sentence: it says only that "the person never has to write the Ruling line themselves".
5. The owner's own words for PR 585 were only "narrow d2" (11-17 04:46) and "publish narrow d2" (11-17 04:51). The owner-answers record says the row "is NOT an owner approval of the rest of the D2 amendment" (owner-answers line 285). The grant-row sentence came from the fix agent's reading of Decision 8 (PR 585 body: "Decision 8, the observer release-gate rule"); no owner words naming the grant row on 11-17 are recorded.
6. The built, tested precedent for "agent records from chat": `~/.claude/skills/sc-implement-protocol/refs/qa.md:248-249`: "clear user confirmation of the explained scoped acceptance ... Executor records the Ruling"; "executor-invented approval ... STOP `E-NO-RULING`".

<!-- Source: Base (original, modified): fact 7 corrected per Change 8 (the grep of master for "grant row" also finds docs/designs/orchestrator.md:116) -->
7. The old per-issue row was removed from master by PR 682 (Clay's deletion of the issue-pipeline package, merged 2026-11-20 00:02 UTC, commit `01e7a9e23`). Old `WORKER-CONTRACT.md` line 300 ("post an issue write without that issue's grant row") is gone in master. A grep of master for "grant row" finds `WORKER-CONTRACT.md:57`, `docs/designs/issue-pipeline-fu1.md:24,26` and `docs/designs/orchestrator.md:116`.

<!-- Source: Base (original, modified): fact 8 corrected per Change 8 (lines 241 and 245 do not refuse bulk standing grants; that conclusion comes from the D04 verdict) -->
8. Master line 241 of the contract says the coordinator makes every outward action "only when the user's instruction names that action", and the instruction may be in its live conversation. Line 245 says no pre-authorization waives a push. A chat go is therefore already the built route for merge, close and `--apply`. The conclusion that there is no standing merge and close comes from the D04 verdict, not from lines 241 and 245.

<!-- Source: Base (original) -->
9. `docs/designs/issue-pipeline-fu1.md:106` (master): "The owner's go and the written acceptance ... are given in chat; the owner never has to write a file." The same document, line 24, still lists "a separate live-test grant row".

## What it costs

<!-- Source: Base (original) -->
- One chat sentence per grant. The agent keeps the ledger.
- The contract sentence at line 57 needs a one-line correction so it stops contradicting the chat rule.

## What it risks

<!-- Source: Base (original): first three risks -->
- The merged text (line 57) and the owner's chat rule disagree today. An agent reading line 57 could ask the owner to write a row, which the owner already ruled out.
- A chat message does not prove who typed it: `ironbelly` is the login shared by the owner and every session on this host (D04 verdict, citing owner-answers line 162). Agent-recorded rows from chat rest on the agent's honesty unless a validator checks the source.
- No script checks the recorded row today (the validator is only designed, D:694; PR B is not built).

<!-- Source: Variant 2 What it risks (U37 at D:1295; grants file inside the write reach, D:688; E-NO-GRANT coverage, D:696 and D04 verdict item 6), Change 7, reworded to apply to this position's own mechanism -->
- The same-host problem applies to any chat go: any agent with the Orca CLI can type into a terminal (design unknown U37, D:1295, accepted there as a v1 risk).
- If a standing `grants` list is used for the four low-stakes writes, that file lies inside the orchestrator's own write reach, guarded only by a verb and a test (D:688). A ledger of recorded goes is likewise writable by the agent that keeps it.
- `E-NO-GRANT` (D:696) covers only the orchestrator's own verbs. Assignment and claim comments come from `/sc:issue`, `pr.merge` is a raw `gh pr merge` and `issue.close` comes from `/sc:closeout` (D04 verdict item 6), so that refusal covers at most two of the six entries. This position does not rely on it as the main control.

## What it gets right

<!-- Source: Base (original, modified): first bullet corrected per Change 8 (the "no bulk standing merge and close" conclusion is from the D04 verdict; lines 241 and 245 are described as they read); bullets 2 and 3 are Base (original) -->
- Consent is per issue, per action, named, and sourced from the person. Bulk standing grants for merge and close are refused (D04 verdict; contract line 241 requires the user's instruction to name the outward action, and line 245 says no pre-authorization waives a push).
- It matches the owner's order that approvals are given in chat.
- It rests on a rule that already runs (the Ruling-line rule, `qa.md`).
