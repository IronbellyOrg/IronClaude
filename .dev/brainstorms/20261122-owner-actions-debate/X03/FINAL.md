# X03 FINAL: server-side protection for master and integration (OA-5)
Reconciler's text, written 2026-11-22 from A-0, B-0, A-3, B-3 and my own gh reads. Everything here is a recommendation until the owner says so in chat. Hour figures are ESTIMATES.

## 1 Unified proposal
**Action:** three pieces, in this order. (a) A `.github/CODEOWNERS` file, by pull request. (b) A branch ruleset `gate-master` on master. (c) A branch ruleset `guard-integration` on integration. The owner creates both rulesets by hand in the GitHub web page (Settings, Rules, Rulesets), because the bypass line is the one setting that can fail silently and the API role id for it is UNVERIFIED.

**CODEOWNERS** (the file says who must approve a change to a path). Sole owner `@ironbelly`, one path per line:
`/.github/CODEOWNERS`, `/docs/designs/`, `/src/superclaude/core/WORKER-CONTRACT.md`, plus two temporary lines `/src/superclaude/cli/issue_watch/` and `/src/superclaude/skills/sc-issue-protocol/` (they cover held draft PRs 686 and 690; removed by pull request once each is merged or closed).

**gate-master** (target `refs/heads/master` only; created with Enforcement Disabled).
- ON: restrict deletions; block force pushes; require a pull request with required approvals 0; dismiss stale approvals when new commits are pushed; require review from code owners.
- OFF: approval of the most recent push (the shared login pushes fixes, so the owner could never satisfy it); conversation resolution; required status checks; linear history; signed commits; any limit on merge methods.
- Bypass list: one entry, role Repository admin, mode "For pull requests only". Nobody else.

**guard-integration** (target `refs/heads/integration`; created Disabled). ON: restrict deletions; block force pushes. Nothing else. No bypass entry.

**Integration pull-request rule:** not now. The owner decides it at the day-14 review, in chat. It would then be approvals 0, code-owner review, the same admin bypass.

**Order.**
1. Owner says the sentence in section 7.
2. Agent drafts a heads-up to Clay (what is covered; merges like PR 684 are not; force push and deletion on integration will be refused, does Clay use either; rollback; 3 working day ask-again timer; a request for a throwaway PR). Owner says send.
3. Agent opens the CODEOWNERS PR with `/sc:pr-submit --monitor 3` and checks the URL names IronbellyOrg/IronClaude. Owner reads it and says merge. Agent reads `codeowners/errors` and expects none (that endpoint is UNVERIFIED).
4. Owner creates both rulesets Disabled. Agent reads `rulesets` and each `rulesets/<id>`, lists every value in plain English against this section, and saves the JSON beside the decision record. Owner checks the bypass line on screen (exactly one Repository admin entry, pull requests only), then switches both on in one step.
5. Tests (owner says go first because they write to GitHub; nothing is merged; every PR is closed and its branch deleted). T1: Clay or IB-JonathanB opens a throwaway PR adding only `docs/designs/GATE-TEST.md`; expect `mergeStateStatus` BLOCKED and `reviewDecision` REVIEW_REQUIRED. T2: a PR from the owner login on the same path; confirm the bypass option shows. T3: a PR from Clay changing one line outside the five paths; expect not blocked. If T1 is not blocked or T3 is blocked, set gate-master to Disabled on the owner's typed go and report. No move to one required approval without a new owner ruling.
6. When T1 to T3 pass and Clay has replied, the owner says in chat that the gate is live and binds non-owners.
7. Day 7: agent tells Clay the day-14 date and reports open PR bases. Day 14: report gated PRs, median wait, waits over 3 working days, gated PRs merged with no second-login approval, bypass uses (Rule insights on the Free plan UNVERIFIED). Owner decides the integration rule, required checks and the two temporary lines.

## 2 Context
OA-5 is one of nine owner-only items. It stays open because only the admin `ironbelly` can set a ruleset. I re-read on 2026-11-22: the rulesets list is `[]`; master protection returns 404 "Branch not protected"; integration `protected` is false; CODEOWNERS is 404 on master and on integration. Roles: ironbelly admin; clayphi and IB-JonathanB maintain. PR 700 (clayphi, 63 files) was opened 2026-11-20T14:46:34Z and merged by its author at 15:07:32Z, review decision empty. It changed `docs/designs/orchestrator.md` and `src/superclaude/core/WORKER-CONTRACT.md`, both on the gated list. PR 684 (28 files, author-merged 2h29m after opening) touches none. Source of the settings: D16 (`debates/D16/VERDICT.md`, rank 5 and the test paragraph).

## 3 Implications
- Clay: a PR on a gated path shows "Review required" until ironbelly approves, and each later push drops the approval. Other PRs behave as today. Direct push, force push and deletion on master stop; force push and deletion on integration stop. Clay cannot approve or bypass.
- Agents on the shared login: opening PRs is unchanged. A gated PR they author cannot be approved by anyone (an author cannot approve their own), so it merges only through the bypass, and only when the owner types "merge PR N with bypass". About a third of recent merges are owner-authored, so this will happen.
- `/sc:pr-submit`: no change, it never merges (no `gh pr merge` in its files, per A-0 and B-0). Its fix pushes drop the approval, so the owner approves after the monitor ends.
- Still open: INV-025. A push to a feature branch is not stopped, and any session on the shared login can run `gh pr merge --admin` or edit a ruleset. Only OA-6 (a separate agent login) makes "a worker cannot merge" true. OA-6 is not a precondition. Organisation-level rulesets cannot be read with the token.
- Stays blocked: nothing in the plan waits on this, since the spec assumes no ruleset. Claims of "gated" stay worded as "narrows".

## 4 Benefits
The exact PR 700 pattern (a non-owner merges a design or contract file unreviewed) is stopped. Accidental history rewrite and deletion of master and integration are stopped. The words-only rule that already failed once (PR 681 said the owner reviews and merges, its author merged) gets a server-side backstop. Rollback is one click, so the trial is cheap. Money: none expected.

## 5 Risks and how to contain each
1. Gate is narrow: PR 684-type merges pass. Say this to the owner and Clay in plain words before "live". Widen paths only on day-14 evidence.
2. INV-025 stays open. Contain with the owner-typed-go rule in the sentence; close it with OA-6 later.
3. Code-owner review at 0 approvals may not block a non-owner author. UNVERIFIED. T1 tests it; on failure disable and re-rule.
4. Owner becomes a review queue (D16: about 17 Clay PRs in about 10 days on both branches, its estimate; owner median response on Clay PRs was 4.4 hours per D16). Contain with the 3 working day ask-again timer and the day-14 count.
5. Clay disputes "sole owner is ironbelly". Heads-up goes first; the ruleset can be disabled in one click.
6. A mistaken ruleset locks merges. Contain with Disabled-first, read-back, the owner checking the bypass line, and saved JSON to recreate it.
7. Clay may use force push or deletion on integration (UNVERIFIED). The heads-up asks directly; undo is one click.
8. Stale-approval loop with `/sc:pr-submit`. The owner approves once, after the monitor ends; put that line in each gated PR body.
9. Departure from D16: D16 puts the integration pull-request rule on from day 0. Here it waits (section 9). Master is still gated when integration is merged into master (PR 664 was that), so the cost is a late, bulk review, not an unreviewed merge to master.

## 6 Costs (ESTIMATES; basis: D16's own figures plus the agents' sums, no measurement)
- Owner about 45 min: chat 5, create two rulesets 15, switch-on and bypass check 5, announce 5, tests go 5, day-14 review 10 to 20.
- Agents about 60 min plus `--monitor 3` waiting: heads-up draft, CODEOWNERS PR about 15, read-back and plain-English list about 20, tests and report about 15, day-7 and day-14 reports.
- Clay about 10 min: reply and two throwaway PRs.
- Ongoing: the owner's review of gated PRs (measured at day 14).

## 7 The sentence the owner says in chat
"Go on X03: sole code owner @ironbelly on the five paths; I create gate-master on master and guard-integration on integration in the web page, both Disabled first; I switch both on after the read-back; the integration pull-request rule is decided at the day-14 review; no agent uses the admin bypass or switches a ruleset off unless I type 'merge PR N with bypass' or 'disable <ruleset>' in chat for that one case; tell Clay first."

## 8 What an agent does after it
Records the sentence word for word in the plan's decision record and marks OA-5 "owner go given, not yet applied". Drafts the heads-up to Clay for the owner's "send". Opens the CODEOWNERS PR with `/sc:pr-submit --monitor 3` after `git remote get-url origin` shows IronbellyOrg/IronClaude. Merges nothing without the owner's typed go. After the owner creates the rulesets, reads them back and lists every value. Runs T1 to T3 only after a separate owner go. Reports the three PR states in chat, schedules the day-7 and day-14 reports, and updates the spec's Appendix and STATE only on the owner's say.

## 9 Consensus and residual
**Full** between A and B on settings, paths, order, tests, rollback and roles. Where their last texts still differed (guard-integration Active on day 0 versus Disabled until one switch-on; who creates the rulesets; how day 14 triggers) I chose: Disabled until one switch-on (fewer steps, the read-back covers both); owner on the web page (both agents' default); owner decides at day 14 and nothing runs by timer (matches the rule that approvals are given in chat).
**Residual owner choice: when does integration get the pull-request rule?**
- (a) Day-14 review, owner decides (recommended). Consequence: integration has only no-delete and no-force-push for about two weeks; Clay's 12 of 12 recent integration PRs are not slowed meanwhile; gated files still meet the gate at the PR into master.
- (b) On now, as D16 says. Consequence: earlier review of Clay's integration work and an owner queue from day 0; CLAUDE.md line 294 on origin/master still tells contributors to branch from integration, so Clay feels it at once.

## 10 What could not be verified
- The admin role id for the bypass line via API (neither agent found it), so the web page is used.
- Whether code-owner review at 0 approvals blocks a non-owner author (T1 decides).
- Whether "Evaluate" (dry run) is offered on Free (agents read it as Enterprise only; I did not re-fetch).
- Whether a partial API update keeps the other rules (so rollback by API sends the full saved JSON).
- The `codeowners/errors` endpoint; Rule insights on Free; organisation-level rulesets (token lacks the scope); Clay's view of "owner = ironbelly"; whether Clay uses force push or deletion on integration.
- I verified myself: empty rulesets, master 404, no CODEOWNERS on either branch, integration unprotected, PR 700 and 684 times and authors, PR 700's two gated files, the last 12 merged integration PRs all by clayphi, roles, and open PRs 711, 690, 686 all by clayphi against master. I did not re-count the "15 of 40 merged PRs touch gated paths" figure.
