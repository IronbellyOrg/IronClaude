# X08 FINAL: script-started coordinators and the typed wake line (OA-18)
Reconciler's recommendation, 2026-11-22. A recommendation until the owner says so in chat. PLAN = /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/ (SPEC = spec/SPEC.md, FU = spec/FOLLOW-UPS.md). WC = src/superclaude/core/WORKER-CONTRACT.md on origin/master.

## 1 Unified proposal
1. Typed wake line: NO for every repository. A script never types into a Claude session. No key, no code, no review date. A coordinator learns of work from the wake file it reads each time a wait returns (at most every 5 minutes, FR-28) and from the Orca mailbox if live test U5 passes. The Orca "unread" mark types nothing.
2. coordinator_autostart (a script, not the owner, starts the project coordinator): false for every repository today. An absent key means false (FR-27).
3. Later, per repository, one at a time, in this order: (a) one throwaway repo the owner names (candidate IronbellyOrg/orchestrator-sandbox, private; whether Orca has it registered is UNVERIFIED); (b) IronbellyOrg/IronClaude; (c) any other repo, Coder included, only when the owner names it.
4. Conditions, each shown in chat before the owner is asked about a repo:
   - Owner approves, in chat, the contract wording for a script start (OA-7: the two WC amendments in D06 item 7).
   - Live tests U3 (a script start counts as depth 0) and U25 (the launch carries the ccsession tag and the first prompt) pass and are written down. If U25 fails, autostart stays off. No typed fallback start.
   - Coder issue 516 has landed for that repo and Clay's hold on it is lifted by the owner, or the owner names a hand-made COORD-<repo> worktree whose origin equals the repo. Until then the hand-opened ORCH-IronClaude holds the duty and nothing restarts it (FR-34).
   - The loader reads the key; restart is conditional on the same key (FU row F5); cap of 3 restarts with a stored counter; an unreadable process list starts nothing; the three off switches (key absent, enabled false, DISABLED) each report coordinator_absent.
   - The start prompt comes from a pattern-checked builder: repo name, the read-back duty list, the words "self-attested", no GitHub text (SEC-16; IronClaude is public).
   - That repo's watcher is already on by the owner's separate OA-19 yes.
   - First throwaway start runs with CCSESSION_PERMISSIONS=default (the mode commit 843df6ac4 added); any stall is reported.
   - Before IronClaude only: on the throwaway, one script start, one forced stop that restarts inside the cap, and the three off switches, all seen working.
5. Stop rule: a duplicate or unexpected session, or an unreadable process list, sets the key to false and reports in chat. Nothing restarts until the owner says so.

## 2 Context
OA-18 asks two per-repo consents. The plan default is both off (SPEC OA-18 row; DECISIONS.md around line 1358). D10 makes the typed line only a nudge, never the guarantee. D06 item 6 allows a script start only at depth 0, with an owner authorization recorded in chat, stated as self-attested. FR-27 also needs U3 and the contract amendments first. Coder 516 (open, no assignee) is on hold at Clay's request until the designs in IronClaude issue 655 are compared.

## 3 Implications
Changes: FR-14 becomes "id-only mailbox and file nudges; no script types into any session". The typed step is dropped from stage S11. F5 goes into the plan. An agent drafts, but does not post, a note on Coder 516 that restart must read the key and stop at 3.
Stays blocked: any script start of a coordinator, until every condition holds for that repo. While off, the poll reports coordinator_absent and wakes wait in the wake folder until a person opens the session.
Untouched: WC line 136, where an agent in a session types one copy of an answer to a silent worker on a positively idle prompt.

## 4 Benefits
The coordinator terminal, where merge and push goes are typed, stays a person-only channel. No new code that types. Autostart reaches the owner's "nothing manual" goal one proven repo at a time. Every answer is undone by one chat sentence.

## 5 Risks and how to contain them
- Start prompt is self-attested (a script writes the claim of owner authority): list only the read-back duties, never merge or close; state "self-attested". It cannot be made verified.
- Runs on the shared ironbelly login: first run in default permission mode; stop rule above.
- Restart loops spend tokens or duplicate sessions: cap 3, stored counter, unknown process list starts nothing.
- Default permission mode may stall on a prompt nobody sees (UNVERIFIED): measured on the throwaway first.
- Latency: an idle person-opened coordinator may wait one to two pull cycles (about 5 to 10 minutes, estimate). Contained by the unread mark and the dashboard.
- Mailbox (U5) may fail outside a Run: then the file pull alone carries wakes, which D10 accepts.

## 6 Costs (all estimates)
Owner: 1 to 2 minutes per sentence. Agent now: about 0.25 h (record, edit plan, draft note; basis: no code). Key, conditional restart, coordinator_absent, off-switch and forced-restart tests: about 4 h, inside planned stages S14 to S16 (basis: size of FR-27, FR-34, FR-17, FR-20). U3 and U25 probes: about 2 h (two probes). Watching the three throwaway events: about 1 h. Typed path avoided: about 5 to 7 h (basis: D10 calls the helper about 100 lines).

## 7 The sentence the owner says in chat
Now: "No typed wake line for any repository, and coordinator_autostart stays off for every repository until I say otherwise. Record it."
Later, per repo: "Turn coordinator_autostart on for IronbellyOrg/<repo> with exactly the duties you read back, restart at most 3 times." Off: "Turn coordinator_autostart off for <repo>."

## 8 What an agent does after it
Now: records the quote with its date, marks OA-18 answered, sets no key, edits FR-14, drops the typed step from S11, adds F5, drafts the note for Coder 516 (not posted). Later, per repo: shows the conditions, writes the key through the protected config verb (SEC-10), starts nothing itself, and reports the first start or coordinator_absent in chat. The owner writes no file.

## 9 Consensus
Full. Agents A and B ended with no difference on substance. I verified and agree. One choice stays with the owner, at the later IronClaude sentence: a calendar wait after the three throwaway events.
- "No extra days" (my recommendation): IronClaude goes on once the events and conditions are shown. A slow failure that stays under the cap of 3 shows up only afterwards, limited by the stop rule.
- "N days clean first": a slow failure has time to show, but ORCH-IronClaude stays hand-opened and the idle wait continues for N days. No source gives N.

## 10 Not verified
- Whether orchestrator-sandbox is registered in Orca or is the intended throwaway (no Orca commands run).
- U3, U25, U5 and the default-mode stall: not run.
- WC line numbers: the plan cites WC:70 and WC:245, but on origin/master the "person opened" text is at line 71 and line 245 is a different rule (pr-submit). Locate the amendments by text, not line.
- Owner decision "R38" (one COORD per project, typed line not adopted): no source found.
- Cost hours are estimates; no S17 line was found that tests a start, restart or off switch (S17 listed as "a proposal, not built", SPEC line 684).
- Verified myself: SPEC lines 204, 229, 236, 581, 668 to 669; FU F5; D06 items 6, 7, 9; D10 items 2, 3, 8, 13; WC lines 71, 136, 138, 200 on master; Coder 516 body and Clay's hold comment.
