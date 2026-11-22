# X06 (OA-7) FINAL: wording of the worker contract lines 57, 70 and 245

Read on origin/master 2ea524514 (local ref, no fetch run; whether newer exists is UNVERIFIED). File: `src/superclaude/core/WORKER-CONTRACT.md`. Test: `tests/skills/test_worker_contract.py`. I opened the contract lines, the test pin, SPEC.md SEC-15 and SEC-22, and PR 707 myself.

## 1 Unified proposal
Action: the owner confirms line 57 and the push rule (master line 246) now, and holds the script-started coordinator sentence (master line 71). One pull request, two commits (line 57 first, line 246 second), through `/sc:pr-submit --monitor 3`. Line 71 stays drafted in the record, not in the tree.

Real line numbers on master: 57 as the plan says; the plan's "70" is a blank line, the sentence is line 71; the plan's "245" is line 246. Line 294 also says "person-opened".

Line 57, replace the bracket and the last sentence: "(decision D2, amended 2026-11-17 by the owner: the person is never required to write a Ruling line into a file; other owner records, such as a grant row or a pass record, are likewise given by the owner in chat and recorded by the agent in that session from that confirmation, naming the exact scope, the owner's quoted words and the date, and the owner is never asked to write a file). A Ruling line, grant row or pass record that the coordinator or a worker records without the person's own chat confirmation of that exact scope is "executor-invented approval"."

Line 246:
1. First sentence ends: "...pushes only on the person's go; no earlier pre-authorization waives this, except the person's own typed `/sc:pr-submit --monitor 3` line or the Full Submit go in the next sentence, which belong to the launched agent's own run and never to the coordinator."
2. The Full Submit sentence stays word for word (the test pins it).
3. New: "That go is given before the commits exist. It covers only that issue's first push, its pull request and the fast-forward fix pushes of the one `/sc:pr-submit --monitor 3` run the launched agent starts in its own top-level session; it never covers a merge, a force push, a push to the default or a protected branch, a branch deletion or any other push. A worker or the coordinator never types the run line."
4. New: "The go ends when that run ends, when the pull request is merged or closed, or when the branch head moves to a commit the run did not make; the next push, and a new run, then need the person's own typed go."

Line 71, drafted only: "These bind the coordinator: an Orca coordinator session the person opened, or one a script started at depth 0 (a terminal plus `ccsession`, never `worker-start`) only when its launch prompt cites an authorization the owner gave in chat for that repository, an agent recorded, and which lists only the duties that record names. That citation is self-attested, because the script writes the prompt: it is a statement, not a check, and every push and merge still needs the person's own typed go."

Order: owner message; agent records it; `git fetch origin`; new Orca worktree with `--agent` from origin/master; recheck lines and the pin; commit 1 (line 57 plus test); commit 2 (line 246 plus test); `uv run pytest tests/skills/test_worker_contract.py tests/issue_pipeline/test_brief.py tests/core tests/hooks -q`; `/sc:pr-submit --monitor 3 --head <branch>`; confirm the URL is IronbellyOrg/IronClaude; no merge without the owner's own go on the head sha; after merge amend R25's "nothing else is pushed" in SPEC.md (SEC-15) and show a per-host diff before any `superclaude install`. All before stage S8 and before anything reads `coordinator_autostart`.

## 2 Context
Line 57 says other owner records "are still written by the owner". DECISIONS.md (line 660 and 674) says that came from a fix agent's reading of "narrow d2", not the owner's words; the owner's rule is chat approval recorded by an agent. The plan says lines 70 and 245 "are not in force". For 246 that is stale: PR 707 (merged 2026-11-20, commit 2ea524514) already put the Full Submit sentence on master, and the test pins it (test lines 3298 to 3312). Master line 246 now says "no earlier pre-authorization waives this" and, two sentences on, treats a field set before the commits exist as a go, with no end and no merge exclusion. I found no mention of PR 707 in the plan record that bears on this (not searched exhaustively).

## 3 Implications
Changes: contract text only. Line 57 stops telling the owner to write records. Line 246 gets a named exception with limits and end conditions. A test pins the new line 57 text (old "still written by the owner" absent) and the new line 246 phrases.
Workers: no change; they never run `/sc:pr-submit` and never record approvals alone. `/sc:pr-submit`: no code change; the text states what its push fence should enforce (UNVERIFIED that the tool matches). `coordinator_autostart` does not exist on master, so script-started coordinators stay off. Stays blocked: line 71 and the six other "person-opened" places (line 294, `HOW-WE-WORK.md:355`, `core/CLAUDE.md:58`, a guard comment, `ccsession-tag/README.md:423`, two tests) wait for the live check U3, per-repo consent OA-18 and the FR-27 pull request.

## 4 Benefits
Removes a rule the owner never made. Closes the open-ended Full Submit go. Lets an agent record an approval from chat without asking for a file. Unblocks the line 57 part of S8. Additive test change; each commit reverts alone.

## 5 Risks (containment)
- Shared login `ironbelly`: anyone with it can set the field or type a go, so the text narrows the risk and does not close it (SEC-22, D06). Containment: named limits and end conditions; no merge without a typed go on the head sha.
- Master has no ruleset (OA-5): a bad merge is one click. Containment: the owner's own go on the head sha.
- An agent reads "recorded by the agent" as licence. Containment: quoted words, date and exact scope are required, and the unrecorded case is named "executor-invented approval".
- A reader widens the Full Submit go to the coordinator. Containment: line 246 sentence 1 says it never belongs to the coordinator.
- Other hosts keep the old text until installed. Containment: per-host diff first; the owner picks each install.
- SEC-22 also says "while the tool's fence holds". I left it out (see 9).

## 6 Costs (estimates)
Agent 1.5 to 2.5 hours; owner about 15 minutes (one chat reply, one merge go). Basis: two sentence edits, about three small tests, one test run and one `/sc:pr-submit --monitor 3` cycle; no measure taken. Line 71 later: 3 to 4 hours, estimate, inside the FR-27 work (six places plus tests).

## 7 The sentence the owner says in chat
The agent first prints the three full texts in that same chat turn under plain labels: A "who records owner approvals (line 57)", B "the one exception to the push rule, with its limits (line 246)", C "script-started coordinators (line 71)". The owner replies: "Yes to A as shown. Yes to B as shown. No to C, hold it."
Rules: a yes counts only for texts printed in that turn; an item not named is a no; an unclear reply ships nothing and the agent asks once; a reply naming only a code ("R25", "SEC-22", "line 246") is not accepted.

## 8 What an agent does after it
Copies the reply, the date and the exact printed texts into the unification ledger under `.dev/tasks/` and stages it (no commit until told). Then follows the order in section 1. Line 71 stays in the record only. Nothing is edited before the reply.

## 9 Consensus and residual
Consensus: full. Both agents sign the same three texts and message rule; they dropped the "second run" and "after a rebase" clauses from the text (covered by "the one run", "never a force push" and the end conditions), and I kept "and a new run" in sentence 4 because SEC-22 lists it. I chose agent B's first sentence for line 246 because agent A's "except the one Full Submit go named next" could be read as letting the coordinator push; the pinned sentence says it never does.
Residual owner choices:
- C (line 71). No (recommended): script-started coordinators stay off until U3 and OA-18; cost is a later small pull request. Yes: a script may start a coordinator on a prompt it writes itself once code reads the field; more automation, weaker check, and the wording needs rework when FR-27 is built.
- Optional: "B: add the fence clause". Yes: one more phrase ("while the tool's fence holds") and one more pinned test; no change to who may push. No (default): a launched agent cannot test the fence at run time, so the end conditions carry the control.

## 10 Not verified
Nothing run: no test passes were executed, the added sentences were checked against the pinned loop by reading only. Whether origin/master is newest (no fetch). The tool's push fence behaviour (`push_range_mismatch`, one fix commit per cycle) read from design, not run. That no plugin mirror of the contract exists (agents report one live copy; I only saw experiment snapshots under `.dev/experiments`). That the other "person-opened" places are as listed (from agent rounds 1 and 2). That the ledger route under `.dev/tasks/` (OA-24) is settled.
