# X02 FINAL: report decisions that need no code (718 D3, 718 D4, two questions for Clay)

Reconciled 2026-11-22 from A-0, B-0, A-3, B-3. Everything here is a recommendation until the owner says so in chat. Nothing was posted. Hours are estimates.

## 1 Unified proposal
Order: (1) owner says D3 and D4 in chat; (2) owner approves the Clay comment text in chat; (3) an agent posts it; (4) the owner gives one go for the issue edits; (5) an agent makes them.

**D3 sentence:** "Report state, run records and settings live in a per-user folder under ~/.config/superclaude/, outside every repository and checkout. They are never kept in IronOrchestrator, in any other repository or in .dev/coordinator/, and no agent commits them. The report keeps the session name coordinator; only the name stays."
**D4 sentence:** "Until the report skill is restored, the daily report runs from Clay's own copy, if it runs at all, and Clay alone updates it. IronClaude does not track or compare against it. No agent edits the IronFlow repository, the two automations or anything else in Clay's setup; re-pointing them is a separate go from me. Whether that copy is retired is my decision, taken in chat when the restore starts and recorded in the restore pull request."

**Asking Clay (they/them, clayphi):** ONE comment on issue 720, not 718, not PR 700, with `gh issue comment 720 --repo IronbellyOrg/IronClaude --body-file <copy>`. An agent first checks the text for ids, paths and tokens. Text:
> Posted by an agent on the owner's instruction (the GitHub account is shared). @clayphi, two short questions about the work-report skill (`agent-work-report`, added by PR 684, taken off by PR 700). One line each is enough; there is no deadline.
> 1. PR 700 rolled back three pull requests together "at Clay's request" and gives no reason. Was the report skill removed for a reason of its own, or only because it came in with that group?
> 2. Does your daily report still run? If yes, from which copy: the IronFlow copy (PR 684 names its commit a04c2754; I cannot see that repository from here), a copy under ~/.claude/skills/agent-work-report/, or something else? And do the automations coordinator-morning-wake and coordinator-missed-check still point at it (yes or no)?
> This repository is public, so please paste no ids, tokens, channel ids, file contents or prompts; you may answer the owner privately instead. Nothing is restored, changed or checked in your setup because of these questions.

Decided where the agents differed: question 2 ends "still point at it (yes or no)", not "still exist". Issue 720 asks "which two automations point at it", and an automation can exist while pointing elsewhere. The `$AWR_ROOT` override and the "refuse a path inside a git work tree" guard stay out of the owner's sentence; they go into the 718 D3 test and 720 commit 2.

**Edits after the answers (each a GitHub write; read the live body first, stop if `updatedAt` moved):**
- 718 D3: add "decided <date>, owner, chat" and the sentence; keep the box open for its config test (fresh host puts state under ~/.config/superclaude/, in no git work tree; skill refuses a state path inside one; no person or ClickUp id in shipped config); replace the shared-private-repo Watch-out with "rejected: a state folder in a repository can be committed or pushed".
- 718 D4: add sentence and date, tick the box (its Done-when allows "or the owner drops the copy"), drop the post-restore diff check, change the review text "blocks D3 and D4" to "decisions done; only the D3 config test waits".
- 720: mark "Ask first" 2 "answered, recorded <date>"; mark item 1 "answered, see comment" only once Clay replies. Edit commit 2: replace "folder `.dev/coordinator/`" with "name `coordinator` only; state in the per-user folder"; name ~/.config/superclaude/ as the state path.
- Record in the plan that D3 replaces the folder half of decision D08 (D08 kept `.dev/coordinator/`).

## 2 Context
Issue 718 D3 asks where report state lives; D4 asks which copy runs the daily report until a restore. Issue 720 (restore the report skill) lists both under "Ask first" with two facts only Clay knows: why the skill was in the PR 700 rollback, and whether Clay's daily report still runs. The report-skill debate verdict (VERDICT.md lines 86-88) names the per-user folder as the D3 default. Both issues have 0 comments.

## 3 Implications
Changes: two owner items close today; 718 D3 and D4 shrink to the config test; 720's commit 2 changes its state path. Stays blocked: the restore itself (owner trigger, separate go), the post-restore config test, and the localhost report server fix (issue 719, still the merge gate). No code, no IronFlow change, no automation change.

## 4 Benefits
No state folder can reach a public repository through an agent slip. No agent edits a setup it cannot see. The unknowns are asked once, in the place the questions already live, with a record. D3 and D4 do not wait for Clay.

## 5 Risks and containment
- Public comment reads as pointed after Clay self-merged PR 700: neutral text, no deadline, private answer allowed; owner may ask in person and have an agent record it as "relayed by the owner".
- A reply contains an id or path: the agent records one-line facts only, stops and tells the owner; hiding a comment needs the owner's go.
- Clay does not answer: both sentences still stand, facts stay UNVERIFIED, one re-ask when stage S15c nears.
- Clay says "keep my copy" or "do not restore": the agent changes nothing more and reports it as a new owner decision (SPEC Appendix B.3 action 1).
- State is per host account and not backed up: accepted, it is rebuilt from GitHub and ClickUp reads.
- D3 is not a security fix for the page server: 719 stays the gate.

## 6 Costs (estimates; basis: short chat turns, one comment, three small text edits)
Owner about 10 minutes. Agent about 0.5 hour. Clay about 5 minutes. No build hours.

## 7 The sentence the owner says in chat
"D3 and D4 as written in X02 FINAL are my answers; post the Clay comment on issue 720 as drafted and then make the 718 and 720 edits." (Say the two sentences from section 1 in full, or point to them.)

## 8 What an agent does after it
Record both answers in the local ledger first. Check the comment for ids, paths, tokens; post it on 720 with --repo IronbellyOrg/IronClaude and confirm the URL. Edit 718 and 720 as in section 1. When Clay replies, record one-line facts and mark "Ask first" 1 answered. Do not start the restore, touch IronFlow or change an automation.

## 9 Consensus
Full. Both agents agreed on channel, wording, D3, D4 and the edits; the one wording point (question 2) is decided above. Residual owner choice: none required. Optional: ask Clay in person instead of by comment; the answers then reach 720 as "relayed by the owner" and nothing else changes.

## 10 What could not be verified
Whether Clay's copy exists and where (IronFlow is private; agents saw no a04c2754 or skill there). Why PR 700 included the skill (body says only "at Clay's request"; its five comments are bot reviews and "auggie review", "@codex review" lines from Clay). Which Orca holds the two automations (no Orca command run). Whether `superclaude update` removed a leftover installed copy of the skill. Cited line numbers in the plan files were read by me for VERDICT.md 86-88 and 720 lines 39-52; the rest rely on the agents' reads.
