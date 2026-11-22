# Verdict QG2: Escalation channel and naming rule (OD-3, OD-4, OD-5)

## Question
QG2 Escalation channel and naming rule: OD-3 (scope of the naming rule: A, B or C), OD-4 (a refused mandatory escalation: fail open on delivery or fail closed), OD-5 (channel for audit escalations: entry lines only, or entry lines plus the notice step with the nine-row list and a cap)

Terms: "D:nnn" is line nnn of `docs/designs/orchestrator.md` (Clay's merged design text, PR 681, snapshot `/home/coder/.cache/ic-snap-20261120/master`). D15 is `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D15/VERDICT.md` (the verdict that left OD-1 to OD-13 open). The "naming rule" is ruling 15 (D:830-847): nothing the coordinator or its workers write where a person reads it may name the agent or model. `names_check` is the planned function that enforces it. AU4a, AU4c and AU5 are the three post-merge audit findings (merged over a change request; merged with an unresolved review thread; conflict markers in the merge) that D:825 item 2 says reach the person.

## Winner
HYBRID: OURS carries all three answers (OD-3 B, OD-4 fail open, OD-5 entry lines first); five small CLAY elements are adopted, the largest being a reserved push notice for AU4a, AU4c and AU5.

## Winning recommendation
1. **OD-3 (scope of the naming rule): B.** Scan only the coordinator's own two writers, `report-entry` and `escalate`; workers' PR bodies keep today's practice; run the measurement U54 (D:1312: how often the deny list wrongly refuses real text, over the last 50 issue and PR titles) before the check is switched on. Reason: no check can read a worker's PR body before it is written (D:847), 25 of the last 30 merged PR bodies carry "Generated with" (read-only re-count: clayphi 17 of 21, ironbelly 8 of 9), and ruling 15 is Clay's ruling, not shown to be an owner ruling (D:830; both advocates answered QUALIFY on that). Source: D:847, `gh pr list --repo IronbellyOrg/IronClaude --state merged --limit 30`, debate points C-001, C-002. Not adopted: the handoff-prompt line that tells workers never to add an attribution line (D:841 item 5); it stays out until the owner rules on it in chat.
2. **OD-4 (a refused mandatory escalation): fail open on delivery.** The escalation is always written; the matched span is replaced by a visible marker, for example "[name removed by naming rule]"; the original match is kept in the action log; the refusal is logged; a match inside a path, sha or number is written unmasked and logged. The escalation template fences paths, shas and numbers so the scan skips them (UNVERIFIED against the real template). Reason: a refused escalation leaves the person never told and the hold on silently (INV-013, `debates/D15/adversarial/adversarial/invariant-probe.md:21`), and D:692 says an unanswered item waits for the person, not for nobody. Fail closed stays only for a structurally bad call such as an entry naming no row (D:684), where the caller gets a loud error and can fix it at once. Source: INV-013, D:684, D:692, points C-003, X-001.
3. **OD-5 (channel for audit escalations): entry lines only in the first build, with a reserved notice.** AU4a, AU4c and AU5 are written as lines of the issue's own entry in the living report (D:825 item 2), marked so the sweep lists them as waiting on a person. Rules of this channel (adopted from Clay): one escalation per pull request, never one per finding; warnings never reach the person; the entry is always written; a cap never drops an entry (D:825, D:686). The push notice (ClickUp message or Orca unread mark, D:682) is reserved for these three findings only and is built when all three triggers hold: the owner says in chat that a push is wanted and gives the cap number (the design recommends 5, D:877); a notice sender is built and tested (none exists in master, pr-a or pr-p); the verb accepts row 8 of the escalation table without a ruling on the other eight rows (UNVERIFIED; D:684 says `escalate` refuses an entry that names no row or an unknown row). Reason: entry lines are enough for held items but not for a finding that arrives after a merge on an unprotected `master` (INV-014, both advocates on A-003), yet the sender, the nine-row list and the cap are not built or not ruled by the owner. Source: D:825 item 2, D:682, D:686, INV-014, points C-004, C-005, A-003. Note: this is narrower than D15's OD-5 wording, which waited on the whole nine-row list; the notice no longer waits on the other eight rows if the verb allows row 8 alone.

### Implications per sub-question
- **OD-3.** D:847 and D:841 need amending: `names_check` runs in two verbs, not in "every writer"; the handoff line is removed or marked pending the owner. The claim comments written by `/sc:issue` itself are not scanned (D:838). The watcher poll is unaffected. The offline scan of every template, fixture and end-to-end body, and the fake `launch.effective` test, stay (they do not depend on scope). The owner is asked once in chat whether the rule applies to workers at all (A, B or C); B is the default if no answer comes.
- **OD-4.** D:847 "refuse (exit 2)" becomes "write with a visible marker and log" for style failures only; the D:684 refusal stays for a missing or unknown row. The audit log of the coordinator carries the original match. The sweep and the dashboard see the marker text, not the original; a person who needs the original reads the log.
- **OD-5.** The dashboard (living report and sweep) is the first-build delivery path, so the sweep must list entries with a "waiting on a person" status (D11: sweep has only "waiting a or b" without a reason). A conflict marker found by AU5 can sit until the report is read (known limit, INV-014). The claim pipeline is untouched. The cap key stays at 0 (no cap) until the owner records a number; code default 0 (`pr-a/src/superclaude/cli/issue_watch/repos.py:262-269`) differs from the design default 5 (D:877), so no generator writes 5 before the owner rules (D15 D17 row).

## Strongest points
**OURS**
1. A refused escalation can fail silently: under scope B both writers refuse a text that fails the check, and the merge-safety escalation lists `.claude/settings.json` in an IronClaude repo; no text says whether refusal fails open or closed (INV-013, `debates/D15/adversarial/adversarial/invariant-probe.md:21`). CLAY's advocate conceded it.
2. Scope A cannot be enforced on a worker's PR body ("cannot be scanned before it is written", D:847) and breaks current practice: 25 of the last 30 merged PR bodies carry the line (my `gh` count, 8 of 9 for the owner's own PRs). CLAY's advocate conceded both.
3. The push notice has no built sender and no owner ruling on its cap: none of `escalate`, `asks.json` or a notice sender exists in master, pr-a or pr-p (D15 Strongest points OURS 3); the cap is settled only by Clay's ruling 39 (D:686, D:877, D:1170, D:1177).

**CLAY**
1. The notice reaches a person away from the report, and the audit findings arrive after the merge on an unprotected `master` (D:682, D:825 item 2, INV-014). OURS' advocate answered QUALIFY on "entry lines are read in time" (A-003).
2. A mask silently edits text a person relies on (D:832, D:684 refusal style); a fail-open path is a bypass. OURS' advocate accepted a visible marker as the fix.
3. The escalation shape is careful: one per pull request, warnings never reach the person, the entry is always written, a cap never drops an entry (D:825 item 2, D:686), and the template and fixture tests are scope-independent (D:847).

## Clay strengths to adopt
- **Visible mask marker and fenced paths in the escalation template.** Why: removes the objection that a mask edits trusted text unseen and lowers false hits on `.claude/settings.json` and the repo name. Merge: OD-4 text carries the marker and the original match goes to the log; template fencing is UNVERIFIED against the real template.
- **Offline scan of every template, fixture and end-to-end body, plus the fake `launch.effective` test (D:847).** Why: it checks the largest part of written text without needing scope A. Merge: kept under scope B.
- **Escalation shape rules (D:825 item 2, D:686).** Why: they give the entry-lines channel clear volume rules. Merge: written as rules of the first-build channel.
- **A reserved notice for AU4a, AU4c, AU5 only.** Why: closes the post-merge gap that entry lines leave (INV-014). Merge: reserved with three triggers (owner says a push is wanted and the cap number; sender tested; row 8 usable alone, UNVERIFIED); not built in the first build.
- **Cap value 5 as the recommended number to record.** Why: it is the design's value and fits the push limit; Merge: the owner records it in chat when the notice is switched on; until then the key stays 0.

## Our strengths that must be kept
- Scope B plus U54 before the rule is switched on.
- Fail open on delivery for style failures, with a log; fail closed only for a structurally bad call.
- Entry lines as the first channel (the ledger-only rule from the owner's memory `orchestration-decision-ledger-only`); no outward message by default.
- The owner decides in chat; the agent records it; the owner writes no file (memory `approvals-through-chat-never-files`).
- No handoff line that conflicts with the owner's own PR practice until the owner rules.

## Actions
| Action | Type | Target | Order or dependency |
|---|---|---|---|
| Owner answers in chat: OD-3 scope (A, B or C; default B), OD-4 (fail open; default), OD-5 (entry lines first; is a push wanted and which cap number); agent records the answers | DECISION | owner (`ironbelly`); D15 section 7 rows OD-3 to OD-5 | before the spec text is final |
| Run U54: read-only count of deny-list refusals over the last 50 issue and PR titles of the three listed repos | LOCAL CHANGE | design test U54 (D:1312); a read-only script run by the owner or a live-test session | before `names_check` is switched on |
| Amend the naming text: scope B, fail open with visible marker and logged original, fenced paths, remove or hold the D:841 handoff line | DOC | `docs/designs/orchestrator.md` D:830-847, D:841, D:684 note | with the design amendment PR (D15 order O2) |
| Write the entry-lines rules (one per PR, warnings never, entry always, cap never drops an entry) and the reserved notice triggers into the spec | DOC | unified spec in `.dev/brainstorms/20261120-pr686-unify/` then the design text D:825 | O1, after the owner's chat answers |
| Build `names_check` as fail open in the coordinator verb group with the offline template scan and fake `launch.effective` test | LOCAL CHANGE | coordinator verb group (`names.py`) | O4 to O6 per D15, after the design amendment PR merges |
| Keep `reach_daily_max` at 0 until the owner records a number; align the design text D:877 (default 5) with the parser default 0 | DOC | D:877; `pr-a/src/superclaude/cli/issue_watch/repos.py:262-269` | with the amendment PR; no code change in PR 686 |
| Build and test a notice sender, then enable the notice for AU4a, AU4c, AU5 | DECISION | later PR after the three triggers hold | reserved; not before the first build is live |

## Implications
- **Watcher (poll).** No change: the poll writes nothing to GitHub; the naming rule covers the coordinator's writers only (scope B), so no poll code is affected.
- **Coordinator.** `report-entry` and `escalate` must write even when `names_check` fails; the D:684 refusal of an unknown row stays. A style failure is logged, never a block. The coordinator tells nobody by push in the first build.
- **Dashboard (living report, sweep, observer).** Audit escalations appear as entry lines; the sweep must list them as waiting on a person. A post-merge finding can sit until the report is read; the reserved notice is the fix.
- **Claim pipeline.** Claim comments written by `/sc:issue` are not scanned under scope B (D:838); the claim chain is unchanged.
- **What breaks.** D:847 text ("refuse, exit 2" for style failure) and D:841 item 5 (handoff line) contradict this verdict and need amendment; D15 OD-5 wording ("wait for the whole nine-row list") is narrowed.
- **Owner must know.** The owner has not ruled on the naming rule at all; rulings 15, 27, 28 and 39 are Clay's. The same Clay-ruling status applies to the cap of 5.

## Confidence
About 70 percent overall: OD-3 75, OD-4 75, OD-5 60. Would change: the owner's chat answer on scope (a ruling for A); the U54 result (a high false-refusal rate would move the rule to C); evidence that a notice sender exists or that `escalate` accepts row 8 alone (would pull the notice into the first build); an owner statement that a push is wanted for post-merge findings.

## Unverified
- Whether the real escalation template fences paths, shas and numbers.
- Whether any notice sender (ClickUp message, Orca unread mark) exists or works; none seen in master, pr-a or pr-p.
- Whether `escalate` accepts an entry for row 8 alone without a ruling on the other rows (D:684 only states the refusal rule).
- Whether rulings 15, 27, 28 and 39 were agreed by the repository owner outside GitHub (no ironbelly record found).
- The R2-OURS measurement "1 of 50 titles with IronClaude, 6 with Jev" (taken from D15, not re-run).
- The 25-of-30 count is mine for the 30 most recent merged PRs on 2026-11-20; the 30-PR window and the body text at merge time were not audited further.
- The advocates' own re-checks of D:nnn lines (partly confirmed by the orchestrator: D:686, D:877, D:1170, D:1177).
- The debate ran at quick depth: one round, no invariant probe, one scorer, no second ordering pass.

## Debate artifacts
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/QG2/position-OURS.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/QG2/position-CLAY.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/QG2/adversarial/adversarial/diff-analysis.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/QG2/adversarial/adversarial/debate-transcript.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/QG2/adversarial/adversarial/base-selection.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/QG2/adversarial/adversarial/refactor-plan.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/QG2/adversarial/adversarial/merge-log.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/QG2/adversarial/adversarial/return-contract.yaml`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/QG2/adversarial/merged-qg2-position.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/QG2/adversarial/return-contract.yaml`
