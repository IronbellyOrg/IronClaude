# X05 FINAL: who counts as "the owner" for typed answers (OA-6)

Reconciler's verdict, 2026-11-22. A and B ended in agreement (A-3 section 4, B-3 section 4). This is a recommendation until the owner says so in chat. Estimates are marked.

## 1 Unified proposal
Two tiers, then one cutover to a separate agent login.

**Definition.** "The owner" is the person behind GitHub account `ironbelly`, identified by its numeric id.
- Tier 1, chat-only answers (grant rows, `--apply`, cleanup approval, design go): counts only as text the owner types in the live chat of a session the owner opened by hand. Never counted: a `worker-start` worker, a script or watcher session, anything sent with `orca terminal send`, a mailbox message, issue or PR text, anything with a `[sc-launch:v1:...]` marker. The receiving session records the quoted words, date, scope and recorder (SEC-08, SEC-14) and runs `git add .dev/tasks` (no commit). It is spec wording that narrows; it cannot prove who typed (SEC-18, D06 item 9). Needs no account. Do it now.
- Tier 2, a merge or the `Approved` label: the Tier 1 chat go, plus an approving GitHub review by the `ironbelly` id on that exact head sha, newer than the gate output, clicked by the owner in the browser. `answer-check` and the merge verb refuse, with a reason and a failing test, if the live login (`gh api user --jq .id`, read live, not from config) equals the owner id, or if no such review exists. Never a pass on session kind alone.

**Second login: worth it.** Build the id parameter and refusal inside S14 (no account needed to build). The account must exist and be cut over before merge automation, OA-18 (coordinator autostart), OA-19 (real-repo watcher switch-on) and OA-20 (worker binding flip) go live. If the owner declines, those four stay off and every merge stays typed by hand.

**Order.**
1. Owner says the sentence in section 7. An agent records it and amends D16 line 97 (an approval posted "for the owner" by a session can no longer exist; the owner clicks Approve).
2. Owner (account, 2FA and admin are owner-only) reads GitHub's machine-account terms, creates the agent account with 2FA, invites it as outside collaborator with Write on IronClaude only (never Maintain or Admin).
3. Owner sets the OA-5 ruleset after the CODEOWNERS PR merges and Clay accepts the roles: master and integration, pull request required, code-owner review (`@ironbelly`), dismiss stale approvals, no force push, no deletion, admin-role bypass only. The approvals count is choice 1 in section 9.
4. Agent reads both ids and writes per-repo `owner_login`, `agent_login`, watcher keys `owner_account_id` and `approval_excluded_ids` (agent id), approvers file (`ironbelly` id), and lists open issues assigned to `ironbelly` (they read as assigned to someone else until reassigned).
5. Owner switches ONE host: signs `ironbelly` out of `gh`, replaces the Coder `github` secret with the agent credential typed in the owner's own terminal, revokes every old `ironbelly` token (both the `gh` login and any inherited `GH_TOKEN`). Credential type: a `gh` login or classic token, not fine-grained (section 10).
6. Owner says go. Agent runs throwaway tests: login prints the agent in a fresh shell and in an Orca session; permission prints `write`; an unapproved agent PR cannot merge on a gated path and on an ungated path; `gh pr merge --admin` and a push to master are refused; Augment and Codex both review an agent-authored PR (a silent reviewer reads as clean, so test first); claim writes (assignee, issue type, Complexity, `Approved`) work; watcher dry run sees an agent-assigned issue; a `/sc:pr-submit` dry PR works.
7. Owner says "Cut over". Agent records it with the ruleset id and credential expiry date. Other hosts follow one at a time with the first two tests.
8. Rollback: owner says OA-6 is unnamed again; merges by hand. Break-glass is the owner's browser or own laptop, never `ironbelly` logged into a host.

## 2 Context
Today one login, `ironbelly` (admin), is shared by the owner and every agent. I read: `gh api .../rulesets` length 0 (no ruleset); collaborators show `ironbelly` admin, `clayphi` and `IB-JonathanB` maintain, `IB-AIReviewer` and others read. The plan default for OA-6 is "unnamed: `answer-check` cannot pass; S14 ships but every merge stays typed by hand" (SPEC.md:578). SEC-09 (SPEC.md:298) and RK-3 (SPEC.md:647) say `answer-check` cannot tell a person from a script on the shared login. SPEC.md:577 says a separate agent login plus the ruleset is the only way to make "a worker cannot merge" true.

## 3 Implications
- A session-kind rule alone is honest but forgeable: a script on this host can still type as the owner. Only the second login plus the ruleset makes a merge a GitHub fact no agent token can produce.
- `/sc:pr-submit`: same command and `--repo IronbellyOrg/IronClaude`; it never merges (A-0 grep of origin/master found no `pr merge`); PR author, replies and thread resolves become the agent. Its fix pushes dismiss stale approvals, so the owner approves after the last round.
- Workers: same agent login; can push branches, open PRs, comment; cannot approve as the owner or use the admin bypass.
- Coordinator: merges only after the chat go plus the id-matched approval. Before cutover it asks the owner to merge by hand.
- Issues now assigned to `ironbelly` need reassigning. Owner-only actions (settings, ruleset, labels, Approve clicks) move to the owner's browser.
- Stays blocked until cutover: merge automation, OA-18, OA-19, OA-20.

## 4 Benefits
"A worker cannot merge" becomes true (with OA-5). INV-003 and INV-025 move from open to checked for merges and the label. A leaked agent credential is worth Write, not Admin. The log shows who acted. Step 1 alone makes the check definable now and makes the coordinator refuse relayed or worker "gos".

## 5 Risks and containment
- An `ironbelly` credential survives on the host: revoke old tokens, `--admin` and master-push tests, live-id refusal.
- Owner logs back in under pressure (as for revert PR 662): written break-glass rule; the refusal makes it visible.
- Review bots go silent on the new account and that reads as clean: test before cutover; keep the SEC-04 hold.
- Write role cannot do the claim's org-level field writes (UNVERIFIED): step 6 test decides; then widen the role or do those writes by hand.
- Credential expiry or suspension stops all agents: fails safe; put the expiry date in the ledger; the owner's browser path remains.
- At 0 required approvals a worker can `gh pr merge` an ungated path unseen by `answer-check`: choice 1 below.
- Chat-only answers still leave no GitHub trace: stays a recorded procedure with the residual stated.

## 6 Costs (all estimates; basis: D16's own figures of about 20 min owner chat and 15 to 30 min ruleset, plus ordinary account setup)
- Tier 1 now: owner about 0.25 h; agent about 1 h (ledger row, two spec edits).
- Second login: owner about 1 to 1.5 h once, about 0.25 h per extra host, about 1 to 2 min per gated merge, about 15 min per credential renewal if it expires. Agent about 3 to 4 h (id refusal and keys 1 to 2 h inside S14, tests 1 h, ledger, config, migration list 1 h).
- Ruleset time belongs to OA-5. Host count is UNVERIFIED.

## 7 The sentence the owner says in chat
"OA-6: by 'the owner' I mean the person behind the GitHub account ironbelly only. My typed answer counts only when I type it in a session I opened myself, never from workers, script-started sessions, relays or GitHub text. Create a separate agent GitHub account for the agents; I will set it up and the ironbelly login comes off the agent hosts. Record it."
Later, two short sentences: "The agent account is called <login>." and, after the tests pass, "Cut over."

## 8 What an agent does after it
Records each sentence word for word with date, scope and recorder in the interim ledger and runs `git add .dev/tasks` (no commit). Carries the Tier 1 text and the limit sentence into SEC-09 and RK-3 when the owner approves spec edits. Amends D16 line 97. Builds the id parameter and refusal in S14 with a failing test first. Until `answer-check` exists, the coordinator does the by-hand checks and refuses a go that came by an excluded route. Reads the two ids, writes config and the migration list, runs the throwaway tests only after the owner's go. It never creates the account, never holds the `ironbelly` credential, never sets the ruleset.

## 9 Consensus and residual owner choices
Consensus: full on substance. Three small choices stay with the owner, each one chat sentence and reversible:
1. Required approvals on master after cutover. 1 (my recommendation, both agents lean this way): an agent PR cannot self-merge on any path; Clay or Jonathan (maintain) can approve each other's PRs, but each PR needs a non-author approver and the queue size is UNVERIFIED. 0 (D16's setting): no wait, but a worker can merge ungated paths with plain `gh pr merge`.
2. Whether the agent account also joins IronbellyOrg/Coder. Yes: agents can file Coder issues, a leaked credential reaches a second repo. No (my recommendation to start): Coder issues stay with the owner until needed.
3. Whether `IB-AIReviewer` (existing read collaborator, purpose UNVERIFIED) becomes the agent account. Yes: no new account, but upgrading it changes whatever it does now. No (my recommendation): create a new one.
If the owner declines the whole second login: Tier 1 still applies, merges stay typed by hand, and the four go-live items stay off.

## 10 Could not be verified
- Verified by me: ruleset count 0; collaborator roles; SPEC.md lines 298, 577, 578, 647; D16 VERDICT lines 23, 61, 85, 106, 113; GitHub's token page says fine-grained tokens cannot support contribution by an "outside or repository collaborator" and org owners may restrict classic tokens (fetched).
- UNVERIFIED: whether a Write-role account can do the claim's issue type, Complexity and `Approved` field writes; whether the org blocks classic tokens; whether an org-member route would allow a fine-grained token; whether Augment and Codex review an agent-authored PR; GitHub machine-account terms wording and free login names; whether rulesets work on this Free-plan org with code-owner review; where else an `ironbelly` credential lives (keyring, Orca's own auth); number of hosts; whether the harness marks sent text differently from typed text; whether Clay and Jonathan want to review each other's PRs.
