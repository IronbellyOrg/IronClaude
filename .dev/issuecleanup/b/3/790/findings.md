# #790 (C9) round 2: Handoff prompt template: fixed nine-section order, Fixes or Refs rule, no secrets, hand-back round block, regression gate

Checked against master f2894fc44 (2026-11-24). Round 1: /home/coder/workspaces/worktrees/IronClaude/Analyze716/.dev/issuecleanup/a716/3/790/findings.md. Static run (Command line): /home/coder/workspaces/worktrees/IronClaude/Realign/.dev/issuecleanup/b/3/analyze/analyze-report.md. Plan files read read-only from /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/; owner records from /home/coder/workspaces/worktrees/IronClaude/Realign/.dev/releases/backlog/issue-watcher-zero-setup/requirements.md.

## Alignment with architectural decisions
Searched DECISIONS.md, SPEC.md, the VERDICT files D15, QG1 and the owner records R36 to R38 and WORKER-CONTRACT.md. Verdicts:

- **R38** (`.dev/releases/backlog/issue-watcher-zero-setup/requirements.md:64`) part D (a typed go for every push and merge; the coordinator never merges or closes on its own): ALIGNED for the Fixes/Refs rule. GitHub closes an issue at merge on a `Fixes` line without any coordinator action; SEC-12 (SPEC.md:301) says to state that, and D15 R-5 (`debates/D15/VERDICT.md:31`) records it. The rule is the only prevention on the PR side.
- **SEC-16** (SPEC.md:305) and **`brief.py:1-10`** ("No issue text can reach the brief"): ALIGNED for a fixed Fixes/Refs sentence. A template slot filled with the issue's criteria would be IN CONFLICT, and would break `tests/issue_pipeline/test_brief.py` (`test_output_holds_only_template_characters_plus_the_issue_number`).
- **Contract brief layout** (`WORKER-CONTRACT.md:203-217`, template `:313-335`; `worker-brief.txt`): the nine-section order is IN CONFLICT. The nine sections come from the 655 design (Clay), which R38 does not adopt; adopting them replaces the owner-accepted layout and needs an owner ruling. D15 row D12 (`debates/D15/VERDICT.md:96`) adopted the check-in, not a template. The Fixes/Refs rule does not need the nine sections.
- **Worker brief versus PR text**: PARTLY ALIGNED. S07-F25 puts the rule in the worker brief, but every brief row ends with `Outward actions: none` (`WORKER-CONTRACT.md:324`) and stops before a commit or push, so a level-none worker opens no PR. The real place that tells an agent to write PR text is the `submit` block of `src/superclaude/skills/sc-issue-protocol/templates/launch-prompt.md:30-36` (step 4, `/sc:pr-submit --monitor 3 ... --body "..."`); it has no Fixes/Refs sentence.
- **Closeout** (`sc-closeout-protocol/SKILL.md:24`, `refs/done-check.md:30`, `PROVENANCE.md:48`): ALIGNED and complementary. Closeout reads `Fixes`, `Closes` and `Refs` as data and decides done from the criteria; it cannot stop GitHub closing the issue first. S14-F27's `already_closed` report already exists (`refs/settle.md:28`).
- **Hand-back round block** (S04-F24): UNRESOLVED owner decision. QG1 OD-2 (`debates/QG1/VERDICT.md:26`) makes re-plan and re-approve the default and calls leaving the body alone and carrying the remaining list in the round block (what S04-F24 builds) "the owner's cheaper alternative, not the default". `HANDBACK_MAX` 3 is "not measured" (SPEC.md:237, FR-35). The hand-back loop itself is a Clay strength (D15 D18), so R38 doubts it.
- **Regression gate in `worker_done`** (S02-F27): PARTLY ALIGNED. WC-5 (`WORKER-CONTRACT.md:60`) fixes the `worker_done` body; a new field belongs in C11. Level-none rows stop before `/sc:implement` (`:297`), so the gate has nothing to run until an implement worker exists (#733).
- **No secrets line** (S04-F26): ALIGNED as a sentence to the worker. FR-37 (SPEC.md:239) scans only `report-entry` and `escalate`, so a handoff scan would go beyond the plan; that is C21's call, not C9's.
- **Audit of `Fixes` after merge** (S10-F53): UNVERIFIED and unowned. SPEC.md:62 lists AU1-AU8 as "NOT BUILT anywhere"; FR-36 (SPEC.md:238) is the plan row; no open item builds it (round 1 named C16, but #797's text has no audit).
- **Orca task-field names** (S04-F22): UNVERIFIED. `orca orchestration worker-start --help` lists `--task-title`, `--spec`, `--deps`, `--comment`, and no field called target, change, constraints, ownership or acceptance.
- **Reachability** (analyze report, finding 1): `brief.build` has no CLI verb and no production caller (only two test files use `brief.py`), so UNVERIFIED how the coordinator reaches the template these tests pin.

## Complementary issues
- **#792 (C11)**: C9 writes the instruction line ("run the gate, report it in `worker_done`"); C11 defines and validates the field. Interface: the `worker_done` fields of WC-5.
- **#799 (C18)**: the round loop that S04-F24's round block describes; C9's block waits for it.
- **#771**: closeout's `issue.handback: remaining` produces the remaining list that a round block would carry; it also owns the finish side of the Fixes/Refs risk.
- **#802 (C21)**: text hygiene; the secrets sentence should live in one place.
- **#782 (C1)**: took over C25's template tests (#806 merged into it); C9 keeps its own golden tests (owner comment on #806).
- **#733**: an implement worker is what makes the regression gate meaningful. **#797 (C16)**: the merge gate, after the PR exists.
- **#776**: asks what workers do at the plan-approval line of the same brief file (`worker-brief.txt`); a file-level neighbour.

## Closest overlap
**#792 (C11: Define and validate a valid worker_done message).**

Shared: S02-F27 (the regression-gate result in `worker_done`); the two items name each other as related. Estimate: about 10% of #790's done-when, which is 1 of its 9 rows and none of its three checks (C9's checks test Fixes/Refs, section order and the round block, not the gate). No open issue overlaps the Fixes/Refs rule itself, which is 5 of the 9 rows.

Next two: **#799 (C18)**, about 10%: the round loop behind S04-F24, a dependency more than an overlap. **#802 (C21)**, about 10%: secrets and text hygiene (S04-F26), which C21 states for "handoff prompts" among other texts.

## Standalone or merge
**Verdict: stand alone, cut down.** Tested against #792:

- **Owner**: same. No reason either way.
- **Acceptance test**: different. C9: golden prompt tests (Fixes versus Refs, section order, round block). C11: a table-driven `worker_done` validator.
- **Files touched**: C9: `launch-prompt.md`, `worker-brief.txt`, `brief.py` and their tests. C11: the WC-5 text, a validator and its tests.
- **Build phase**: the Fixes/Refs sentence needs no skeleton and can ship now. C11 is in the Phase 2 cluster and rests on a `worker_done` shape that is UNVERIFIED (#792's own watch-out).
- **Risk if merged**: the wrong-close protection would wait for the Phase 2 cluster, while any `--submit` run can still write `Fixes` on a partial PR in the meantime; the owner's closeout judgement only runs after GitHub has closed the issue.

Merging would be right for two pieces only: S02-F27 belongs in #792 (the field) and #733 (an implement worker), and S04-F24 belongs in #799 (the loop). If the owner wants all nine rows as one template PR with the nine-section order, C9 stays whole and moves to Phase 2.

## Closed issues and merged PRs checked
- **PR #683 and issue #668** (merged 2026-11-20, completed 2026-11-20): `/sc:closeout` reads `Fixes`, `Closes` and `Refs` as data, decides done from the criteria, reports `already_closed` and `left_open`, and hands back `remaining`. Delivers the closeout half of S14-F27. Does not stop GitHub closing at merge.
- **PR #661 and issue #651** (merged and completed 2026-11-19): Priority, Fix approach and Test plan sections in the issue templates. The PR body itself says `Closes #651`, a person's own practice; no Fixes/Refs rule was added to any template.
- **PR #425 and PR #636** (merged 2026-11-07, 2026-11-18): the launch prompt with its `submit` block, and the default claim level. The `submit` block is where PR text is written; it has no Fixes/Refs sentence.
- **PR #584 and PR #591** (merged 2026-11-17): `brief.py` and `worker-brief.txt` with closed slots, golden tests per status. Deliver the template machinery for the level-none brief, not the items C9 adds.
- **PR #724** (merged 2026-11-23): bounds the Full Submit push go to the first push, the PR and the fast-forward fix pushes of one `/sc:pr-submit` run; constrains the `submit` block, changes no C9 behaviour. **PR #707**: the watcher; no PR-text rule.
- **#806 (C25)** (closed not planned 2026-11-24, merged into #782): C9 and C10 keep their own per-template tests. **#798 (C17)** merged into #797. **#689** (closed not planned 2026-11-23): plan everything at creation; its proposed goal and approach sections at filing time are a different layer from the handoff prompt. **#507** (completed 2026-11-11): `--unattended` on each `Command:` line, already applied to the brief rows.

## Updated recommendation
- **Action**: keep open with changes. (1) Cut the item to the Fixes/Refs rule, the no-secrets sentence and golden tests, placed in the `submit` block of `launch-prompt.md` and, only if a worker route can ever open a PR, in the worker brief; today none can. (2) Defer S04-F24 to #799 (and the owner's OD-2 choice), S02-F27 to #792 and #733. (3) S10-F53's audit has no open item: AU1-AU8 are not built (SPEC.md:62); say so in the item or drop that half (this corrects round 1, which sent it to #797). (4) Drop the nine-section order and the Orca task-field names unless the owner rules otherwise. (5) State in the skill, as S07-F25 asks, that no script checks the Fixes/Refs choice. (6) Before the golden tests, decide how the coordinator reaches `brief.build` (no verb, no production caller today).
- **Priority**: P2, unchanged from round 1.
- **Complexity and size**: simple, S after the cut. Changed from round 1 (medium, M, which round 1 itself said assumed the rest is deferred): the cut is now the recommendation, so there is one real edit place plus golden tests. As written, the item is complex, L.
- **What is new since round 1**: the template has no production caller; the audit half has no owner item; the worker brief cannot carry a PR rule today; the nine-section order conflicts with R38's general sentence; the owner merged C25 into #782 and said C9 keeps its own tests.

## Scan record
- Lists read in full: open-issues.tsv 134 of 134 rows, closed-issues.tsv 157 of 157, merged-prs.tsv 508 of 508.
- Title search terms: handoff, brief, template, prompt, Fixes, Refs, closeout, secret, hygiene, round, hand-back, regression, worker_done, validate, test, plan approval, submit, launch.
- Opened with `gh issue view` / `gh pr view` (bodies read to their first 1500 to 1900 characters, C-items from their `###` heading; text beyond that is UNVERIFIED): open 792, 799, 797, 802, 733, 771, 776, 782, 791, 758, 805, 772, 773, 761 (14); closed 806, 798, 668, 651, 689, 507 (6); merged PRs 683, 661, 425, 636, 584, 591, 724, 707 (8). Also read: #790 and #716 (body, closing review, all 5 comments); comments of #806 and #798.
- Master check: Command line `/sc:analyze src/superclaude/cli/issue_pipeline --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/b/3/analyze`, succeeded; Grep for `secret|token|credential` in the package found none; Grep for `Fixes`/`Refs` in `sc-pr-submit-protocol` and the launch prompt found no rule. UNVERIFIED: which acceptance lines of #771 overlap (its Acceptance Criteria section was not read beyond its heading).
