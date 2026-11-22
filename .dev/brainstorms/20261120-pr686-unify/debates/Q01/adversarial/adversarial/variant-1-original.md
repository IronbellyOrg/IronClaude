# Position OURS (Q01): who writes a per-issue grant row

Abbreviations: "master" = `/home/coder/.cache/ic-snap-20261120/master`; "owner-answers" = `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/owner-answers.md`; "D:nnn" = `docs/designs/orchestrator.md` line nnn in master (Clay's design from PR 681, the design document).

## Claim

A per-issue grant row is the owner's own consent for one named issue and one named list of writes. It must come from the owner and must never be created by an agent on its own. That provenance rule is the owner's line. The owner's later order (2026-11-17) fixes the mechanics: the owner says the go in chat, and the agent records the row from that chat message, naming the exact scope. The owner is never asked to write a file.

## Mechanism

1. The owner types the go for one issue in chat, naming the issue and the writes.
2. The agent in that session records the row (quoting the owner's words and the date) in its ledger.
3. A row an agent writes without the owner's own chat confirmation of that exact scope is "executor-invented approval" and is refused. This is the same rule that already governs a Ruling line.

## Cited facts

1. Decision 8, answered "Approved" by the owner: "one grant row per pipeline issue, created when the issue is claimed ... the grant row is written by the owner, not by an agent" (owner-answers line 130). The limit is aimed at an agent creating its own permission.
2. The owner's rule of 2026-11-17 (memory file `/home/coder/.claude/projects/-home-coder-workspaces-IronClaude/memory/approvals-through-chat-never-files.md`): every approval, written acceptance, go, input and Ruling is given by the owner in chat, the agent records it, and the owner is never asked to "hand-write a ledger record". The owner ordered the file-writing requirement "removed from the whole framework".
3. The merged contract text keeps the grant row owner-written: `src/superclaude/core/WORKER-CONTRACT.md:57` in master says "other owner records, such as a grant row or a pass record, are still written by the owner". PR 585 (docs fix that narrowed the D2 wording, merged 2026-11-17 05:03:09 UTC, commit `bfabf1d63`) put it there.
4. The tech-reference twin, `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:722` in master, does not carry the grant-row sentence: it says only that "the person never has to write the Ruling line themselves".
5. The owner's own words for PR 585 were only "narrow d2" (11-17 04:46) and "publish narrow d2" (11-17 04:51). The owner-answers record says the row "is NOT an owner approval of the rest of the D2 amendment" (owner-answers line 285). The grant-row sentence came from the fix agent's reading of Decision 8 (PR 585 body: "Decision 8, the observer release-gate rule"); no owner words naming the grant row on 11-17 are recorded.
6. The built, tested precedent for "agent records from chat": `~/.claude/skills/sc-implement-protocol/refs/qa.md:248-249`: "clear user confirmation of the explained scoped acceptance ... Executor records the Ruling"; "executor-invented approval ... STOP `E-NO-RULING`".
7. The old per-issue row was removed from master by PR 682 (Clay's deletion of the issue-pipeline package, merged 2026-11-20 00:02 UTC, commit `01e7a9e23`). Old `WORKER-CONTRACT.md` line 300 ("post an issue write without that issue's grant row") is gone in master (a grep of master for "grant row" finds only `WORKER-CONTRACT.md:57` and `docs/designs/issue-pipeline-fu1.md:24,26`).
8. Master line 241 of the contract already says the coordinator makes every outward action "only when the user's instruction names that action", and the instruction may be in its live conversation. A chat go is therefore already the built route for merge, close and `--apply`.
9. `docs/designs/issue-pipeline-fu1.md:106` (master): "The owner's go and the written acceptance ... are given in chat; the owner never has to write a file." The same document, line 24, still lists "a separate live-test grant row".

## What it costs

- One chat sentence per grant. The agent keeps the ledger.
- The contract sentence at line 57 needs a one-line correction so it stops contradicting the chat rule.

## What it risks

- The merged text (line 57) and the owner's chat rule disagree today. An agent reading line 57 could ask the owner to write a row, which the owner already ruled out.
- A chat message does not prove who typed it: `ironbelly` is the login shared by the owner and every session on this host (D04 verdict, citing owner-answers line 162). Agent-recorded rows from chat rest on the agent's honesty unless a validator checks the source.
- No script checks the recorded row today (the validator is only designed, D:694; PR B is not built).

## What it gets right

- Consent is per issue, per action, named, and sourced from the person. Bulk standing grants for merge and close are refused (contract lines 241 and 245; D04 verdict).
- It matches the owner's order that approvals are given in chat.
- It rests on a rule that already runs (the Ruling-line rule, `qa.md`).

