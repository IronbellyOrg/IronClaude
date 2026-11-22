<!-- Base: Variant A (variant-1-original.md, Position OURS) -->
<!-- Incorporated: Variant B (variant-2-original.md, Position CLAY), per refactor-plan.md Changes 1 to 5 -->
<!-- Merge date: 2026-11-20 -->

<!-- Source: Base (original) -->
# Position OURS (QG2): escalation channel and naming rule

<!-- Source: Base (original) -->
Paths: D:nnn = `docs/designs/orchestrator.md` on master (snapshot `/home/coder/.cache/ic-snap-20261120/master`). D15 = `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D15/VERDICT.md`.

<!-- Source: Base (original, modified) - OD-4 sentence extended with the visible mask marker and fenced paths (Change #1); OD-5 extended with the entry-line shape rules (Change #3). OD-3 sentence unchanged. -->
## Claim
OD-3: scope B (scan only the coordinator's own two writers, `report-entry` and `escalate`; workers' PR bodies keep today's practice; measure false refusals first with U54). OD-4: fail open on delivery (the escalation is always written, the matched span masked with a visible marker such as "[name removed by naming rule]", the original match kept in the log, the refusal logged; the escalation template fences paths, shas and numbers so the scan skips them, which is UNVERIFIED against the real template). <!-- Source: Variant B (Cited facts 4, What it risks; Variant A advocate steelman), merged per Change #1 --> OD-5: audit escalations go as entry lines only, until the owner rules on the nine-row list and the daily notice cap. Rules of the entry-lines channel: one escalation per pull request, never one per finding; warnings never reach the person; the entry is always written; a cap never drops an entry (D:825 item 2, D:686). <!-- Source: Variant B (Mechanism OD-5, What it gets right, Cited fact 7), merged per Change #3 -->

<!-- Source: Base (original, modified) - OD-3 bullet extended with the scope-independent offline scan (Change #2). OD-4 and OD-5 bullets unchanged. -->
## Mechanism
- OD-3: `names_check` runs inside two verbs. A worker's own PR body cannot be scanned before it is written, so scope A cannot be enforced by a check on the thing it names; only a prompt line stands behind it. The offline scan does not depend on the scope: a test over every template, fixture and `gh`/`orca` body the end-to-end tests produce, and a fake `launch.effective` test, stay in place for either scope (D:847). <!-- Source: Variant B (Mechanism, Cited fact 8; D:847), merged per Change #2 -->
- OD-4: an escalation is the only channel by which a held merge or a bad merged result reaches a person. A rule about wording must not be able to silence it. Mask the matched span, write, log the refusal in the action log.
- OD-5: AU4a, AU4c and AU5 become lines of the issue's own entry in the living report (D:825 item 2). The notice (ClickUp DM or Orca unread mark) is a second, separate step that waits for rulings that do not exist yet.

<!-- Source: Base (original, modified) - facts 3 and 8 restated to say that ruling 39 is Clay's ruling, not an owner ruling, and to give the two cap defaults (Change #5). Facts 1, 2, 4, 5, 6, 7 and 9 unchanged. -->
## Cited facts
1. 25 of the last 30 merged PR bodies carry "Generated with" (D15 G-4). I re-counted read-only with `gh pr list --repo IronbellyOrg/IronClaude --state merged --limit 30`: 25 of 30; clayphi 17 of 21, ironbelly 8 of 9. Both authors follow the practice; scope A would make most recent PRs non-compliant.
2. D:847 says a worker's PR body "cannot be scanned before it is written; the handoff line above is its rule (AD-X1, decided by ruling 28: no ninth audit check unless it happens)". So scope A has no mechanical check, only a prompt line.
3. D:832 allows the `Co-Authored-By: Claude Code` commit trailer (ruling 39, which is Clay's ruling, not an owner ruling) but not a "generated with" line in a PR body; the harness for this very session instructs both (commit trailer and PR-body line). The rule and the tool conventions disagree. <!-- Source: Base (original, modified) - ruling 39 attributed to Clay (Change #5) -->
4. The deny list holds "any `claude-...`" and "the product name of an agent or model family" (D:832). This repository is called IronClaude and its settings file is `.claude/settings.json`, which is in the default merge-safety list (D:817). R2-OURS in D15 measured 1 of 50 titles with "IronClaude" and 6 with "Jev" (D15 INV-013 text); U54 (D:1312) is the unrun measurement.
5. INV-013 (`debates/D15/adversarial/adversarial/invariant-probe.md:21`): under scope B both writers "refuse (exit 2, nothing written, nothing sent)"; the merge-safety escalation lists matched files; no text says whether a refusal fails open or closed. Closed means the person is never told and the hold stays on silently.
6. D:692 and ruling 24: an unanswered question waits and nothing proceeds on that item. A dropped escalation turns "waits for the person" into "waits for nobody".
7. Owner memory `orchestration-decision-ledger-only` (2026-11-09): automated checks show outstanding decisions only. An entry line in the report is the outstanding-decision ledger; a DM on every audit hit is chatter by default (cap key default 0 means no cap, `pr-a/src/superclaude/cli/issue_watch/repos.py:262-269`).
8. The cap is settled only by Clay's ruling 39, which is not an owner ruling (design default 5, D:877; parser default 0, `pr-a/src/superclaude/cli/issue_watch/repos.py:262-269`): D:1177 says "not ruled on; open", D:686 and D:877 say "settled as recommended" (ruling 39); D11 and D06 item 11 call the nine-row list an inventory, not a rule. No `escalate` verb, `asks.json` or notice sender exists in master, pr-a or pr-p (D15 Strongest points OURS 3). <!-- Source: Base (original, modified) - cap and ruling source restated (Change #5) -->
9. INV-014: AU5 is not held by the merge gate; the audit arrives after the merge, so what matters is that the line exists and is visible, not that a second channel exists.

<!-- Source: Base (original) -->
## What it costs
- Scope B leaves workers' PR bodies uncovered: a model name could appear in a worker-written body (accepted: that is today's practice and the owner's PRs carry it).
- Fail open means a masked agent name can occasionally appear as "[removed]" in an escalation; the rule is weakened for that text.
- Entry lines only means no push to a person who is away from the report; a violation can sit until the report is read.

<!-- Source: Base (original, modified) - first bullet extended with the visible marker and fenced paths (Change #1); second bullet's notice clause replaced by the reserved notice and its triggers (Change #4) -->
## What it risks
- Masking could damage a path, sha or number the person needs. Condition: the mask touches only the deny-list match, and a match inside a path, sha or number is written unmasked and logged. The mask is a visible marker, not a silent edit, and the original match stays in the log (Variant B's objection that a mask edits text without saying so is accepted); paths such as `.claude/settings.json` hit the deny list (INV-013), so the template should fence paths, shas and numbers so the scan skips them. <!-- Source: Variant B (Cited fact 4, What it risks), merged per Change #1 --> Whether the escalation template fences paths is UNVERIFIED (INV-013).
- Without a push, a conflict marker on an unprotected `master` (D01: `protected: false`) can wait. Mitigation: the entry is the "waiting on a person" item that the sweep lists. Entry lines are enough for held items but not for a post-merge hit (INV-014), so a notice for AU4a, AU4c and AU5 is reserved, not built. Proposed triggers, all UNVERIFIED because no notice sender exists in master, pr-a or pr-p: the owner says in chat that a push is wanted and gives the cap number; a notice sender is tested; row 8 can be used without a ruling on the other eight rows. <!-- Source: Variant B (OD-5 claim; both advocates' C-004 hybrid), merged per Change #4 -->

<!-- Source: Base (original, modified) - closing sentence added pointing to the reserved notice (Change #4) -->
## What it gets right
Nothing in the safety channel depends on a style rule. Every added control keeps the owner's ledger-only rule and the approvals-in-chat rule. Each deferred piece has a named trigger: U54 result for scope, owner ruling on the nine rows and the cap, a tested notice sender. The reserved notice for AU4a, AU4c and AU5 has its proposed triggers listed under "What it risks". <!-- Source: Variant B (OD-5 claim), merged per Change #4 -->
