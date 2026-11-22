# Section 09 analysis: What the orchestrator handles itself and what goes to the human
Counts: COVERED 20, CONFLICT 10, NOT-COVERED 6 (36 features)

Source: issue 655 body lines 117-141 plus Acceptance Criteria lines 224-225 (what reaches Clay, limits).

Abbreviations. SPEC = /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/spec/SPEC.md. DEC = .../20261120-pr686-unify/DECISIONS.md. V(x) = .../20261120-pr686-unify/debates/x/VERDICT.md. WC = the worker contract as read from the snapshot /home/coder/.cache/ic-snap-20261120/master/src/superclaude/core/WORKER-CONTRACT.md (line numbers are from that snapshot; the current checkout was not used for WC). "Clay's design" = docs/designs/orchestrator.md (removed from master by PR 700, SPEC Appendix B line 758). "The person" in the plan means the owner (ironbelly).

### S09-F1 Default: the orchestrator handles itself everything outside the table; in doubt a case does not reach Clay
- 655 says: "The orchestrator handles itself everything not in the table below ... When in doubt, a case does not reach Clay" (body line 121). Also "Agents may close issues" in the same line.
- Status: CONFLICT
- Current plan: The plan keeps several actions behind the person's own typed go, so "everything else is handled alone" is false: merge (SEC-01, SPEC:290), the close of an issue (SEC-12, SPEC:301; FR-38, SPEC:240), a push of worker commits (FR-32, SPEC:234), grants (SEC-07, SPEC:296), cleanup `--apply` (FR-38). Silence is never a yes (SEC-14, SPEC:303). V(D15) row D7 rejects standing merge and close (V(D15):91).
- Depends on: S09-F7, S09-F8 (the two biggest cases)
- Evidence from our documents: SPEC:290 "Merge only on a person's typed go for that PR naming repo, PR, full 40-character head sha"; owner rule in memory index (/home/coder/.claude/projects/-home-coder-workspaces-IronClaude/memory/MEMORY.md) "Approvals through chat, never files".
- Concerns: 655's rule works only if the table is the complete list of human gates; the plan has more gates than the nine rows (merge go, push go, close go, grant, apply). A builder must not copy the "in doubt, do not reach Clay" default.

### S09-F2 The orchestrator records what it decided and why in the report entry
- 655 says: every self-handled decision is recorded with the reason in the issue's report entry (body line 121).
- Status: COVERED
- Current plan: FR-48 `report-entry` is the only writer of an entry file (SPEC:259); FR-37 write an entry first (SPEC:239); merged-requirements lists `report-entry` as a verb (brainstorm/run/merged-requirements.md:201). The content "what it decided and why" is not spelled out, only the writer and the entry lines for waiting items (FR-49, SPEC:260).
- Depends on: 655 section 7 (the living report)
- Evidence from our documents: n/a (COVERED)
- Concerns: PR 700 removed the work-report skill from master, so FR-45, FR-46 and FR-48 are "blocked until the skill is restored" (SPEC:778; owner action B.3 item 1, SPEC:786). The entry cannot be written until the owner decides to restore it.

### S09-F3 Sorting each worker into one of Clay's FR-9 states
- 655 says: the orchestrator sorts every worker into an FR-9 state (body line 121).
- Status: COVERED
- Current plan: the worker contract already has the states S0 to S11 with trigger and response per state (WC:116-129) and a sweep after every wake at most once per 5 minutes (WC:110); the plan keeps this (FR-38 "Each cycle run `/sc:sweep`", SPEC:240; FR-40, SPEC:242). The names differ from Clay's FR-9 (our documents do not contain Clay's FR-9 text: UNVERIFIED which states it lists).
- Depends on: 655 section 7 (worker status check)
- Evidence from our documents: n/a (COVERED)
- Concerns: a builder should map Clay's FR-9 names to S0-S11 once, not add a second state list.

### S09-F4 The unsticking playbook (FR-23), a file in the skill
- 655 says: the orchestrator unsticks a worker "by the FR-23 playbook", "a file in the skill" (body lines 119, 121).
- Status: NOT-COVERED
- Current plan: none found; searched: the word "playbook" and "D:507" across all *.md under /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify (one hit only, below), "unstick", "check-in" in SPEC.md, DECISIONS.md and V(D15). The worker contract's ladder L0-L5 and its state table (WC:116-129, WC:182-192) already say what to do per state, which overlaps part of a playbook, but no coordinator skill reference file is planned.
- Component: COORDINATOR (a ref file of the coordinator skill, the skill that does check-ins)
- Feature statement: The coordinator skill carries one playbook reference file that lists, per worker state, the allowed unsticking steps (nudge, probe, typed copy) and the steps that are never allowed.
- Done when: the file exists under the skill's refs, a test checks that every state of WC S0-S11 has a row and that no row approves a permission prompt or interrupts a worker.
- Depends on: S09-F3, S09-F6
- Evidence from our documents: V(D15) debate file .../debates/D15/adversarial/adversarial/rounds/round2-rebuttal-1-ours.md:198 "the playbook ref (D:507) loses its 'approval' rows" (the playbook is assumed to exist but no verdict adopts or rejects the file itself).
- Concerns: the playbook must not contain approval rows (see S09-F6). Clay's playbook text is in the archived design, not on master (SPEC:759).

### S09-F5 Answering a worker's question when the sources answer it
- 655 says: the orchestrator answers a worker's question when the sources answer it (body line 121).
- Status: COVERED
- Current plan: the contract says a `question` "is answered with `reply --id` or forwarded to the person" (WC:108) and S5 "blocked in ask ... Answer it, then the ack timeline" (WC:123), plus the ack rules A1-A4 (WC:131-138). The plan keeps the contract (FR-40 typing rules, SPEC:242; V(D15) row D12 one supervised route, V(D15):96).
- Depends on: none
- Evidence from our documents: n/a (COVERED)
- Concerns: the test for "when the sources answer it" (issue, code, docs, web search) is the row 8 criterion, a separate feature (S09-F16).

### S09-F6 Approving a permission prompt under FR-24 (an approval answered once)
- 655 says: the orchestrator approves a permission prompt under FR-24 when the action is not in rows 1 to 7; it may "answer an approval once" (body lines 121, 140).
- Status: CONFLICT
- Current plan: FR-40 "Type into worker terminals only under the four typing rules (never approve a permission prompt)" (SPEC:242). V(D15) row D14: "Reject approving permission prompts (WC:122, WC:137); drop approval rules and test cases" (V(D15):98). Contract: S4 "never answer the prompt" (WC:122), "never answer a person prompt" (WC:137), and "answers a permission or person-only prompt" is on the never-on-silence list (WC:188). The sentence in DEC:603 "never answers a permission prompt". 655's version is REJECTED. A closed list of approvable prompt classes is only a possible later owner decision.
- Depends on: none
- Evidence from our documents: .../round2-rebuttal-1-ours.md:196 "WC:122 says state S4 ... is a person-only state: 'never answer the prompt'"; same file :203 "Owner decision (optional, later): a closed list of prompt classes the coordinator may approve".
- Concerns: S4 stays a report line, re-reported every 15 minutes (WC:122), so a blocked worker waits for a person.

### S09-F7 Merging when every merge condition holds, without the person (and "merging is not in the table")
- 655 says: the orchestrator merges alone "when every merge condition holds" and "Merging and closing issues are not in the table (ruling 13)" (body lines 121, 138).
- Status: CONFLICT
- Current plan: SEC-01 merge only on a person's typed go naming repo, PR, 40-character head sha and method, one-shot (SPEC:290); "A passing gate never triggers a merge" (SPEC:290); SEC-06 no standing `pr.merge` (SPEC:295); V(D15) row D7 rejects "autonomous merge (DQ8, R10, wave 7)" (V(D15):91). A PR waiting for the go is shown as "waiting on a person" with its age (SEC-21, SPEC:310). 655's version is REJECTED. The merge conditions themselves are adopted as a read-only `merge-gate` (SEC-02, SPEC:291; SEC-03, SPEC:292).
- Depends on: 655 section 7 (merge conditions)
- Evidence from our documents: V(D15):91 "a person's go is the only brake on an unprotected `master`".
- Concerns: master has no ruleset today, so the typed go is a procedure, not a block (SPEC:48).

### S09-F8 Closeout self-handled and agents may close issues; closing is not in the table
- 655 says: the closeout is self-handled and "Agents may close issues ... as their work needs"; closing is not in the table (body lines 121, 138).
- Status: CONFLICT
- Current plan: SEC-06 no standing `issue.close` (SPEC:295); SEC-12 one per-PR go covers merge and close, "no standing close" (SPEC:301); FR-38 call `/sc:closeout <PR>` "under a go naming the close" and never run it as a worker (SPEC:240; SEC-05, SPEC:294). Contract line "only when the user's instruction names that action" (WC:241). 655's version is REJECTED for the close. Running `/sc:closeout` itself is adopted as is (V(D15) row F1, V(D15):120).
- Depends on: 655 section 7/8 (closeout wave)
- Evidence from our documents: WC:241 "only when the user's instruction names that action".
- Concerns: a `Fixes` line in a PR body still closes the issue at merge with no coordinator write (SPEC:301).

### S09-F9 Hand-back of a not-done issue is self-handled
- 655 says: the hand-back is done by the orchestrator without reaching Clay (body line 121).
- Status: COVERED
- Current plan: FR-35 runs the hand-back loop (`HANDBACK_MAX` 3 "not measured", `no_progress`, old worker final first) but round 2 re-plans and enters `waiting_reapproval`, so the person approves again before a new worker starts (SPEC:237); V(D15) row D18 (V(D15):102). Different from 655 in that the owner re-approval gate stays.
- Depends on: none
- Evidence from our documents: n/a (COVERED, with that one change)
- Concerns: the re-approval makes a hand-back not fully self-handled; a builder must follow FR-35, not 655.

### S09-F10 Agents may delete ordinary files as their work needs
- 655 says: "Agents may ... delete ordinary files as their work needs"; the orchestrator may "delete the ordinary files its work needs (ruling 25; removal of that line was rejected)" (body lines 121, 140; acceptance line 224).
- Status: NOT-COVERED
- Current plan: none found; searched: "delete", "ordinary file", "rm" in SPEC.md, DEC, V(D15), V(QG3), V(D04). Only cleanup has a delete rule: local `git branch -d` only, never `-D`, `--force`, `rm`, `prune` (FR-39, SPEC:241). The contract bars removing a worktree or branch with unmerged work without the user's instruction (WC:237).
- Component: COORDINATOR (a line of the "may do" list in the refuse(argv) rules)
- Feature statement: The refuse(argv) list states which delete commands the coordinator's own verbs may run on ordinary files inside its own work area, and refuses all others.
- Done when: a test passes an `rm` of an ordinary file inside the declared work area and is allowed, and `rm` of a path outside it, of a worktree or of a shared branch is refused.
- Depends on: S09-F31 (the refuse function), S09-F33
- Evidence from our documents: SPEC:241 "(never `-D`, `--force`, `rm`, `prune`, remote delete)"; WC:237 "It never removes a worktree or branch that holds unmerged commits ... without the user's instruction".
- Concerns: "ordinary files" is not defined in 655 or the plan; `rm` is exactly what FR-39 forbids for cleanup. Ruling 25 is Clay's ruling, not shown to be an owner ruling (V(QG2):63 says rulings 15, 27, 28 and 39 are Clay's; ruling 25 is "one of Clay's rulings 23 to 35" per V(QG4):14).

### S09-F11 One table of nine rows decides what reaches Clay; a case reaches him only when it fits one row, and the entry names the row
- 655 says: one nine-row table replaces the old eight rules; a case reaches Clay "only when it fits one row, and its entry names that row" (body lines 123-136).
- Status: COVERED
- Current plan: V(D15) row D16 "Nine-row 'what reaches the person' table ... Adopt with change: Notice step only; 'the person' instead of Clay; sweep and observer never pick a row; keep the 'exactly nine rows' test" (V(D15):100); FR-47 (SPEC:258); V(D11) lines 35 and 58. Change: the table lives in the notice step only and the wording is "the person". Whether the table is the gate for all escalations is narrower in the plan than in 655.
- Depends on: none
- Evidence from our documents: n/a (COVERED)
- Concerns: the table is owner-undecided on cap and notice (V(D11):59); see S09-F23 and S09-F24.

### S09-F12 Rows 1 to 4, 6 and 7 (identity, a secret, money, a legal act, other people's access or data, a breaking change)
- 655 says: these six needs always reach Clay (body lines 126-129, 132-133). Row 2 also says any request to write a secret anywhere reaches him.
- Status: COVERED
- Current plan: they are rows of the adopted table (V(D15):100; FR-47, SPEC:258). The secret and access rules also match SEC-10 (config protection, SPEC:299) and the rule that no GitHub text reaches a prompt or argv (SEC-16, SPEC:305). Row text itself was not re-read from Clay's design (it is archived, SPEC:759): UNVERIFIED that the plan's nine rows equal 655's wording.
- Depends on: S09-F11
- Evidence from our documents: n/a (COVERED)
- Concerns: none

### S09-F13 Tag or publish a release always needs a recorded human OK (row 5 and the "may never" list)
- 655 says: "Tagging or publishing a release always needs a recorded human OK"; the orchestrator may "tag or publish a release only with a recorded OK"; never without one (body lines 131, 137, 140; acceptance line 224).
- Status: CONFLICT
- Current plan: SEC-11 "Refuse unconditionally the tag and publish commands ... (`git tag`, `gh release create`, `uv publish`, `npm publish` and the others; N6), one test each, none passable by `--answer-ref`" (SPEC:300); V(QG3) item 1 "OD-6: Yes. The coordinator never tags or publishes a release" (V(QG3):14); DEC OD-6 row (SPEC:102). A person or the release flow tags; merging a release PR stays allowed on the per-PR go. 655's version (a pass path with a recorded OK) is REJECTED.
- Depends on: none
- Evidence from our documents: V(QG3):14 "the pass path rests on `answer-check`, which cannot tell a person from a script".
- Concerns: `refuse(argv)` sees only commands the verbs run, so a tag typed in the coordinator's own shell stays unseen (V(QG3):61, UNVERIFIED how to cover).

### S09-F14 Row 5: deleting a skill or an agent that the issue does not name reaches Clay
- 655 says: row 5 covers "deleting a skill or an agent the issue does not name (2)"; acceptance says deleting a skill or agent needs the issue to name it (body line 131; acceptance line 224).
- Status: NOT-COVERED
- Current plan: none found; searched: "delete" and "skill or an agent" in SPEC.md, DEC, V(D15), V(D14), V(D16). The nearest rule is the review rule that reversing or deleting someone else's merged work needs their written yes and a different merger (V(D16):30, process rule in root CLAUDE.md, human authors only).
- Component: COORDINATOR (an escalation rule in the escalation template and the refuse list)
- Feature statement: The coordinator escalates, naming the row, before it lets a worker's change delete a skill or agent file that the issue text does not name.
- Done when: a fixture PR that deletes `src/superclaude/skills/x/` with an issue that does not name it produces a held entry naming row 5; the same PR with the issue naming it does not.
- Depends on: S09-F11, S09-F19; 655 section 8 (audit checks on the pull request file list)
- Evidence from our documents: V(D16):71 "Reversing or deleting someone else's merged work needs their written yes and a merger other than the author" (the nearest existing rule, a human-process rule).
- Concerns: PR 682 deleted recent work with a single contract edit and passed because no gated path rule saw a pure deletion (V(D16):99 point 3); a path-based CODEOWNERS gate does not catch skill deletions outside the named paths.

### S09-F15 Row 5: other irreversible or shared-settings acts (deleting a shared branch, a force push, a settings change)
- 655 says: these need Clay (body line 131); the "may never" list forbids deleting a shared branch (line 140).
- Status: COVERED
- Current plan: merge never uses `--auto`, `--admin` or `--delete-branch` (SEC-02, SPEC:291); cleanup is local `git branch -d` only and keeps the branch if any PR with that head is open or foreign (FR-39, SPEC:241); the per-repo config keys are guarded (SEC-10, SPEC:299); the ruleset blocks force push and deletion on master and integration (FR-75, SPEC:339).
- Depends on: S09-F31
- Evidence from our documents: n/a (COVERED)
- Concerns: the ruleset is admin-only and not yet set (SPEC:48).

### S09-F16 Row 8 judgement criteria (scope creep into peripheral features, a product-changing choice, a question unanswered after issue, code, docs and a web search)
- 655 says: row 8 "a decision only he can make" covers a scope that creeps into peripheral features, a question still unanswered after the issue, the code, the docs and a web search, and a choice that changes what the product does; acceptance adds "a scope change escalates only when it creeps into peripheral features; a question only after the issue, code, docs and a web search" (body line 134; acceptance line 224).
- Status: NOT-COVERED
- Current plan: none found; searched: "peripheral", "scope creep", "web search", "question still unanswered", "changes what the product" in SPEC.md, DEC, V(D15), V(D16), V(QG2); no hit. The rows of the table are adopted (S09-F11) but the tests for when a case is "row 8" are not described in any verdict.
- Component: COORDINATOR (rules in the escalation template and the playbook)
- Feature statement: The coordinator has a written, ordered procedure that a worker's question must fail (issue text, code, docs, then web search) before it is escalated as row 8, and a rule that a scope change escalates only when it adds peripheral features.
- Done when: a test fixture with a question the issue answers produces no escalation; a fixture the issue, code, docs and a search leave open produces an entry naming row 8.
- Depends on: S09-F11, S09-F5, S09-F4
- Evidence from our documents: no evidence found in our documents
- Concerns: the "web search" step reaches a third-party service and could carry project text; the owner's rule is that project details are not sent to outside services without the owner's ask. The scope rules (4) to (6) are Clay's rulings; the owner has not confirmed them (V(QG2):63).

### S09-F17 Row 8: merging over a failing check, or a PR that changes a merge-safety file, waits for his explicit OK
- 655 says: those two merges wait for Clay's explicit OK (body line 134; acceptance line 223).
- Status: COVERED
- Current plan: SEC-03 only `checks_failing` and `merge_safety` can be overridden, each with its own key, by the person's go; the other eleven reasons never (SPEC:292); SEC-08 the recorded go carries the key `merge_safety:<PR>:<head sha>` (SPEC:297); V(D15) row D2 (V(D15):86).
- Depends on: S09-F7
- Evidence from our documents: n/a (COVERED)
- Concerns: none

### S09-F18 Row 9: stuck cases reach him (worker not unstuck same day, failed handoff, PR held for a review agent or `changes_requested`, a merge his rights forbid, unclear or failed closeout, hand-back at its bound)
- 655 says: row 9 is a stop, not a decision, for these six cases (body line 135).
- Status: COVERED
- Current plan: worker stalls go to the person by L5 at set minute thresholds (WC:118-129; "never on silence" list WC:182-192); failed handoff: stop and escalate (FR-30, SPEC:232); review agent that never ran: merge-time hold then escalate, `review_stalled` and `changes_requested` not overridable (SEC-04, SPEC:293); closeout: `/sc:closeout` adopted (V(D15):120; the skill's own contract of a stated final status or an escalation is taken from its description, not re-read: UNVERIFIED); hand-back bound: `HANDBACK_MAX` 3 stop (FR-35, SPEC:237). "A merge his rights forbid" has no matching item: UNVERIFIED (the plan has the merge only on the person's go, so a forbidden merge would show as a refusal of the verb).
- Depends on: S09-F11
- Evidence from our documents: n/a (COVERED)
- Concerns: "not unstuck the same day" is a day threshold; the contract uses minutes (L5 by 15 minutes). A builder keeps the contract thresholds.

### S09-F19 `escalate` refuses an entry that names no row; the rules are on from the start (no warn phase, no ladder)
- 655 says: `superclaude orchestrator escalate` refuses an entry that names no row; rules are on from the start (body line 137; acceptance line 224).
- Status: COVERED
- Current plan: FR-26 verb `escalate` (SPEC:228); FR-37 "fail closed only on a structurally bad call" (SPEC:239); V(QG2):13 "Fail closed stays only for a structurally bad call such as an entry naming no row (D:684)". Differences: the verb is `superclaude coordinator escalate`; a refused naming-rule check fails open (OD-4, SPEC:100); whether `escalate` accepts row 8 alone is UNVERIFIED (V(QG2):71).
- Depends on: S09-F11
- Evidence from our documents: n/a (COVERED)
- Concerns: none

### S09-F20 An unanswered question waits; nothing is decided for Clay; the entry says "If you do not answer:" what stays blocked and what continues
- 655 says: body line 137.
- Status: COVERED
- Current plan: V(D15) row D16 keeps "'if you do not answer' waits, no default" (V(D15):100); SEC-14 "silence is never a yes" (SPEC:303); SEC-21 a waiting go keeps its slot and never expires; shown as "waiting on a person" with its age (SPEC:310); V(OAG1) OA-25b (V(OAG1):40).
- Depends on: none
- Evidence from our documents: n/a (COVERED)
- Concerns: none

### S09-F21 `answer-check` runs before any answer is acted on (typed input, newer than the entry, right question; no tap, click or reaction)
- 655 says: every answer is checked first for source, freshness and the right question; no tap, click or reaction answers anything (body line 137; acceptance line 224).
- Status: COVERED
- Current plan: SEC-08 four checks (typed by a person in their own session, never relayed; right entry; newer than the entry's last edit; question key matches) (SPEC:297); SEC-09 `answer-check` validates entry, key, head sha and freshness, owner identity a parameter, and "state it cannot tell a person from a script" (SPEC:298; RK-3, SPEC:647); V(D15) row D4 (V(D15):88).
- Depends on: none
- Evidence from our documents: n/a (COVERED)
- Concerns: OA-6 (name the session kind that counts as the owner) is open: without it `answer-check` cannot pass (SPEC:578).

### S09-F22 A ClickUp reply counts as an answer
- 655 says: an answer is "Clay's own typed input or his ClickUp reply, newer than the entry" (body line 137).
- Status: CONFLICT
- Current plan: SEC-08 accepts only an answer "typed by a person in their own session, never relayed" (SPEC:297); V(D04):41 "the source test must be 'typed in the orchestrator's own terminal by a person', not a login". A ClickUp reply is a relayed text on a shared login, so it is not accepted. 655's version is REJECTED. (No ClickUp mention exists in SPEC.md at all: searched "ClickUp".)
- Depends on: S09-F21
- Evidence from our documents: V(D04) line 41 (path .../debates/D04/VERDICT.md) "refuses relayed, wrong-entry, stale and unknown-source answers".
- Concerns: SEC-09 admits no check can tell a person from a script on the shared `ironbelly` login.

### S09-F23 Notices (a ClickUp DM, else the Orca unread mark) on from the start
- 655 says: notices reach Clay by a ClickUp DM, else the Orca unread mark, with the rules on from the start (body line 137).
- Status: CONFLICT
- Current plan: first build has no push notice: SEC-21 "no push notice in the first build" (SPEC:310); FR-49 "reserve a push notice until the owner asks with a cap number, a sender is built and tested, and the verb accepts row 8 alone (UNVERIFIED)" (SPEC:260); V(QG2):14 reserved for AU4a, AU4c, AU5 only under three triggers; V(QG2):70 "none seen in master, pr-a or pr-p" for any notice sender. Entry lines in the report are the first channel. 655's version is REJECTED for the first build; the reserved path remains.
- Depends on: S09-F24
- Evidence from our documents: MEMORY.md index "Orchestration decision ledger only: automated checks display outstanding user decisions only; no heartbeat/timeout chatter"; V(QG2):42 "Entry lines as the first channel ... no outward message by default".
- Concerns: a post-merge finding can sit unread until the report is opened (V(QG2):19, INV-014).

### S09-F24 Notice cap `reach_daily_max`: 5 per repo per 24 hours; an entry is never dropped
- 655 says: notices are capped at `reach_daily_max` (5 per repo per 24 hours, ruling 39); an entry is never dropped (body line 137).
- Status: CONFLICT
- Current plan: for the default of 5. FR-12 "`reach_daily_max` absent or 0 means no notice cap" (SPEC:202); FR-47 "keep the 5-a-day cap a proposal (default 0; no generator writes 5)" (SPEC:258); V(D15) row D17 "Defer ... Key default stays 0" (V(D15):101). 655's value of 5 is REJECTED as a default until the owner records a number. The part "an entry is never dropped" is COVERED (V(QG2):13-14 "a cap never drops an entry"). The key itself is carried (SEC-10, SPEC:299).
- Depends on: S09-F23
- Evidence from our documents: V(D15):101 "Clay's ruling 39; the design says both 'open' (D:1177) and 'settled' (D:686)".
- Concerns: a bad cap value must not silently read as "no cap" (C-INV-3, SPEC:299).

### S09-F25 The ways to reach him: lines of the issue's own entry, an Orca decision gate, the notice
- 655 says: three ways (body line 137).
- Status: COVERED
- Current plan: entry lines (FR-49, SPEC:260); a `decision_gate` message goes to the person (WC:108); the notice is S09-F23 (reserved).
- Depends on: S09-F23
- Evidence from our documents: n/a (COVERED)
- Concerns: none

### S09-F26 Orca session control: list, read, send work, wait on its own mailbox
- 655 says: the orchestrator controls Orca sessions by listing, reading, sending work and waiting on its own mailbox (body line 140).
- Status: COVERED
- Current plan: `worker-list`, prompt-wait listing and mailbox wait are the contract's sweep (WC:110); FR-28 pull wakes at every `check --wait` return (SPEC:230); FR-30 `worker-start` (SPEC:232); FR-40 typing rules (SPEC:242); each cycle `/sc:sweep` (FR-38, SPEC:240).
- Depends on: none
- Evidence from our documents: n/a (COVERED)
- Concerns: none

### S09-F27 Transcript reads are capped at 200 messages
- 655 says: "read (at most 200 transcript messages)" (body line 140).
- Status: NOT-COVERED
- Current plan: none found; searched: "200 transcript", "transcript messages", "read at most", "orca terminal read" across the pr686-unify folder. The only transcript rule is that costly probes (transcript tail, screen read) run only for workers a trigger fired for (WC:110), and the report reader reads transcripts for the sweep's session ids (FR-45, SPEC:256).
- Component: COORDINATOR (a limit in the verb that reads sessions)
- Feature statement: The coordinator's session-read call never asks for more than 200 transcript messages and refuses a larger request.
- Done when: a test with a request for 201 messages is refused or clipped to 200.
- Depends on: S09-F31
- Evidence from our documents: no evidence found in our documents
- Concerns: the number 200 is Clay's; it has no source or measurement in our documents (UNVERIFIED).

### S09-F28 The one interrupt: `escalate --interrupt` when a major issue must be escalated
- 655 says: the orchestrator may interrupt a worker's current turn in one case, `escalate --interrupt`, only after the escalation is written; this send is exempt from the 60-second typing hold; five coordinator-spec places change (C25 to C29) (body line 140; acceptance line 225).
- Status: CONFLICT
- Current plan: OD-7 "No interrupt of a running worker" (SPEC:103); V(QG4) item 1 "`escalate --interrupt` (N7) is not built" (V(QG4):14); V(D15) row D9 Reject (V(D15):93); FR-26 "no lease, no interrupt" (SPEC:228); FR-40 "never interrupt a worker" (SPEC:242); R-7 (SPEC:601). Reasons: no incident cited, Orca gives no receipt that the interrupt landed (U40), and the contract's nudge would undo the stop. 655's version is REJECTED. C25 to C29 are not applied. A later reopen needs a contract exception, the C25-C29 changes, a nudge-suppression rule and a receipt check (V(QG4):31). The existing context-exhaustion interrupt of the contract (S6, WC:124) is a different case and stays.
- Depends on: S09-F29
- Evidence from our documents: V(QG4):14 "the next liveness nudge says 'If your turn ended before worker_done, continue with your next Command: line now' (WC:164), which would undo the stop".
- Concerns: the brake for an irreversible worker action is the launch guard and the person's go, not a coordinator interrupt (V(QG4):59).

### S09-F29 Write the escalation first; send nothing if the escalation is refused
- 655 says: the interrupt is sent only after its escalation is written (body line 140); general rule that an entry is never dropped (line 137).
- Status: COVERED
- Current plan: FR-37 "Write an escalation or entry first, send nothing if refused" (SPEC:239); V(QG4):30 adopts the escalation-first ordering rule as separable from the interrupt.
- Depends on: none
- Evidence from our documents: n/a (COVERED)
- Concerns: none

### S09-F30 Restarting a dead agent stays as FR-23 says (ruling 29)
- 655 says: restarting a dead agent stays as FR-23 says (body line 140).
- Status: COVERED
- Current plan: FR-34 restart a dead coordinator with a resume wake, at most 3 times; an unreadable terminal list restarts nothing (SPEC:236). A dead worker: S8 exited, "Settle under WC-6, then L4 or L5" (WC:126); the contract's never-on-silence list bars creating a retry Task or releasing a worker on silence (WC:182-190).
- Depends on: none
- Evidence from our documents: n/a (COVERED)
- Concerns: until Coder issue 516 the duty holder is `ORCH-IronClaude` and nothing restarts (SPEC:236).

### S09-F31 The one refusal function `refuse(argv)` in `limits.py`, every verb's `gh`, `git` and `orca` call passes through it, one test per line of the "may never" list
- 655 says: body line 140; acceptance line 225 "every line of the 'may never' list has a test and passes through `refuse`".
- Status: COVERED
- Current plan: FR-26 "a closed `refuse(argv)` list with a failing test per pattern" (SPEC:228); `tests/coordinator/test_refuse_argv.py` (SPEC:228); V(D15) row D8 adopt with change (V(D15):92); D04 and D05 adopt it for the coordinator (V(D04):43, V(D05):23). Changes: N6 unconditional (SEC-11), no N7 (S09-F28). The module name `limits.py` is not named in the plan (UNVERIFIED).
- Depends on: none
- Evidence from our documents: n/a (COVERED)
- Concerns: `refuse(argv)` "binds the verbs, not a command the model types itself" (V(D05):31); the coordinator's own shell stays outside it (SEC-18, SPEC:307).

### S09-F32 Never a permanent "always allow"
- 655 says: body line 140; acceptance line 222 (not in my section's range but cited for this line).
- Status: COVERED
- Current plan: the plan never approves a permission prompt at all (S09-F6), which includes any "always allow"; the older rule "the single-use yes, never 'always allow'" was Clay's rule 4 of FR-24 and is subsumed (round2-rebuttal-1-ours.md:192).
- Depends on: S09-F6
- Evidence from our documents: n/a (COVERED)
- Concerns: none

### S09-F33 Never delete a shared branch, another person's data, or a worktree or session it did not start
- 655 says: body line 140.
- Status: COVERED
- Current plan: FR-39 local `git branch -d` only, never `master`, `main`, `integration` or the default branch; keep the branch for an open or foreign-head PR; refusals keep the whole worktree (SPEC:241); SEC-02 never `--delete-branch` (SPEC:291); WC:237 no removal of a worktree or branch with unmerged work. The matching exact refusal patterns for "worktree or session it did not start" are not listed in the plan (UNVERIFIED).
- Depends on: S09-F31
- Evidence from our documents: n/a (COVERED)
- Concerns: `orca worktree rm` without `--force` has an unproven effect on the branch and a dirty worktree (SPEC:672).

### S09-F34 Never change credentials, mint or rotate secrets, or control machine lifecycle (`coder`, `systemctl`, `orca automations create`, `edit`, `remove`, `run`)
- 655 says: body line 140 (a named refusal list); row 2 says a secret only Clay holds reaches him.
- Status: NOT-COVERED
- Current plan: none found; searched: "systemctl", "machine lifecycle", "credential", "automations", "mint", "rotate" in SPEC.md, V(D04), V(D05), V(QG3). Hits: SPEC:78 (D02 cron stays the scheduler, so no Orca automation exists in the plan); SPEC:307 SEC-18 lists the coordinator's own shell as a residual risk; and the spec-panel finding F13 says rotating the exposed Orca token has no stage (FOLLOW-UPS.md:22). SEC-16 and SEC-17 limit what reaches a prompt (SPEC:305-306) but do not refuse commands.
- Component: COORDINATOR (entries of the refuse list in `limits.py`-equivalent code)
- Feature statement: The coordinator's refuse list refuses commands that change credentials or secrets, or control the machine (`coder`, `systemctl`, `orca automations create|edit|remove|run`), each with its own test.
- Done when: a test per pattern passes the argv and is refused; the list is checked by a test that scans the skill text for a command outside the "may do" list.
- Depends on: S09-F31
- Evidence from our documents: V(QG3):61 "`refuse(argv)` sees only commands the verbs run (D:769), so a tag run in the coordinator's own shell stays unseen"; FOLLOW-UPS.md:22 "Rotating the exposed Orca token has no stage and is not a precondition of S17".
- Concerns: these refusals protect only verb calls; a model-typed shell command bypasses them. Do not read or log the Orca runtime file or any token while building the tests.

### S09-F35 Never stop a worker (`worker-stop`, `worker-abandon`) apart from the one interrupt
- 655 says: body line 140.
- Status: COVERED
- Current plan: the contract's never-on-silence list begins "stops a worker" (WC:184) and says "never interrupt" (WC:137); FR-40 "never interrupt a worker" (SPEC:242). The terms `worker-stop` and `worker-abandon` do not appear in our documents (searched the pr686-unify folder); the plan's rule is stricter than 655 (no exception).
- Depends on: S09-F28
- Evidence from our documents: n/a (COVERED)
- Concerns: a stop on the person's instruction ("recorded stop") is allowed by the contract (WC:124 S6 text), so a refusal test must not block a person-instructed stop.

### S09-F36 Never write outside `grants` or `repos.yaml`
- 655 says: the orchestrator may never write outside `grants` or `repos.yaml` (body line 140).
- Status: CONFLICT
- Current plan: no `repos.yaml` exists in the plan: "no registry repository, no `repos.yaml`" and the config is per-repo JSON (FR-11, SPEC:201; FR-12, SPEC:202). The coordinator may not write the grant list or the guarded keys without an accepted record: SEC-07 grants start empty and the owner grants once in chat, recorded with `repos grant` (SPEC:296); SEC-10 `repos` verbs refuse to write `reach_daily_max`, `grants`, `merge_safety_files`, `reviewers` without an accepted record, plus a Write/Edit hook (SPEC:299). So 655's wording (the orchestrator may write `grants`) is REJECTED; the idea of a bounded write area is kept.
- Depends on: none
- Evidence from our documents: V(QG3):17 "the coordinator runs as the same OS user, so the file cannot be put out of its reach".
- Concerns: both layers of SEC-10 only narrow the gap.

## Section summary
- 36 features. 20 are covered, mostly through the adopted nine-row table (V(D15) D16), `answer-check`, the merge gate, `refuse(argv)` and the worker contract states.
- 10 conflicts, all decided by the current plan: no autonomous merge or close (SEC-01, SEC-06, SEC-12), no permission-prompt approval (FR-40), no interrupt (OD-7), release tag and publish refused outright (SEC-11), no push notice and no default cap of 5 in the first build (SEC-21, FR-47), no ClickUp answers (SEC-08), no `repos.yaml` or orchestrator-written grants (FR-11, SEC-10).
- 6 remaining features: playbook file, deleting ordinary files, skill/agent deletion escalation, row 8 judgement criteria, the 200-message read cap, and the credential and machine-lifecycle refusals. All fit the COORDINATOR.
- Builders must also know: the report skill that holds the entry writer is gone from master after PR 700, so the `report-entry` features wait for the owner's restore decision (SPEC:786).


