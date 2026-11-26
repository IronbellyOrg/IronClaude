# Round 2 findings: issue #801 (C20) Limits and escalation rules: file deletion, skill and agent deletion, scope questions, transcript cap, credentials

Checked 2026-11-24 against master `f2894fc44f6e68a7dd6a78c75f59683cb0b5acb9` (worktree `/home/coder/workspaces/worktrees/IronClaude/Realign`). Live state: OPEN, label `enhancement`, no comments, sub-issue of umbrella #716 (read in full with comments and the closing backlog review). Round 1 findings read: `/home/coder/workspaces/worktrees/IronClaude/Analyze716/.dev/issuecleanup/a716/7/801/findings.md`. Static command: `/sc:analyze src/superclaude/cli/issue_pipeline --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/b/6/analyze` (report `/home/coder/workspaces/worktrees/IronClaude/Realign/.dev/issuecleanup/b/6/analyze/analyze-report.md`, finding 3: no refuse list in the package). Plan files read-only from `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/` (SPEC = `spec/SPEC.md`, DEC = `DECISIONS.md`); per-row analysis `/home/coder/workspaces/IronClaude/.dev/implement/reference-our-research-a-3463b8ef/sections/section-09.md` and `section-10.md`.

## Alignment with architectural decisions

| Decision or rule | Verdict | Evidence |
|---|---|---|
| **R38** (owner, 2026-11-21; `.dev/releases/backlog/issue-watcher-zero-setup/requirements.md:64`): merged watcher is the design; Clay's "read-only merge gate" and other rows "not adopted"; it "supersedes the 'Clay strengths adopted' rows of the unification spec (section 7 and the HYBRID rows of section 2)" | **Partly in conflict (round 1 missed the scope of this)** | The closed list `refuse(argv)` is Clay's design decision D8, adopted ADOPT+CHANGE in spec section 7 (SPEC:459; section header :435). The merge-time hold that S09-F14 needs is Clay's D1/D2 `merge-gate` and `merge_safety` (SPEC:457), which R38 names ("read-only merge gate") and `design-comparison-655.md:3` voids. The nine-row "what reaches the person" list (D16 row numbering) is adopted "only as an inventory" (DEC:302) and "in the notice step only" (FR-47, SPEC:258). So the vehicle for four of the six rows is a superseded Clay row; the *goal* (limits on a coordinator) matches R38(D) "the coordinator never merges or closes on its own". Whether the owner re-adopts `refuse(argv)` is UNVERIFIED (no record found). |
| **FR-26 / S13** (SPEC:228, :497; D8 SPEC:459): one verb group with a closed `refuse(argv)` list and a failing test per pattern; `tests/coordinator/test_refuse_argv.py` | **Partly aligned** | This is the home the item assumes. SPEC:62 lists `refuse(argv)` as NOT BUILT anywhere; its contents are not given in the plan (`section-10.md:369`), which is the gap this item fills. The home is itself under R38's supersede. |
| **FR-39** (SPEC:241; DEC:504) and **PR #711**: the cleanup script uses a positive allowlist and never `--force`, `git branch -D`, `rm`, `prune`, remote delete; "Nobody removes by judgment" | **In conflict on the allow side** | S09-F10/S10-F47 would let the coordinator's `rm` of "ordinary files" pass. "Ordinary files" is defined nowhere; ruling 25 is Clay's, not shown to be an owner ruling (`debates/QG4/VERDICT.md:14`; `QG2:63`). Refusals of all other `rm` forms are consistent with FR-39. |
| **WORKER-CONTRACT.md:237-238**: the coordinator removes its own child worktree with `orca worktree rm` and deletes its branch after merge-back; never removes a worktree or branch with unmerged commits, an open PR or uncommitted changes without the user's instruction | **Aligned; the refuse list must allow line 237** | A blanket refusal of "any deletion of a worktree or branch" (S10-F47) would contradict the contract's own child-worktree cleanup. The item must carve out `orca worktree rm` of a coordinator-created child and refuse every other form. |
| **WORKER-CONTRACT.md:183-191** (never act on silence) | **Aligned** | No row asks to act on silence. |
| **Owner records in chat** (PR #724; `WORKER-CONTRACT.md:57`) | **Aligned** | The definition of "ordinary files" is an owner decision to be given in chat and recorded by the agent. |
| **VERDICT D16** (`debates/D16/VERDICT.md:99`, point 3): a pure deletion touching no gated path (PR 682) is not caught by a path-based gate; only the written rule, the hold and the tripwire cover it | **Aligned (S09-F14 is wanted)** | But the hold lives in the merge gate (#797), which R38 supersedes; the row has no confirmed host. |
| **VERDICT QG3** (`debates/QG3/VERDICT.md:61`; DEC:847): `refuse(argv)` sees only commands the verbs run; a command typed in the coordinator's own shell stays unseen | **Aligned; states the limit** | Even built, the list narrows and does not close (SPEC wording "narrows", DEC:302 point 10). |
| **Launch-level guard** (`src/superclaude/hooks/scripts/launch-level-guard.sh`; PRs #432, #469, issue #441/#394): blocks classes of commands in claim-launched sessions | **Different mechanism, no coverage of S09-F34** | Grep of the guard for `systemctl`, `automations`, `coder` found no hit; the guard governs launched agents, not the standing coordinator. S09-F34 is not covered on master. |
| **Zero-setup watcher decisions** (R38(B): cron, not an Orca automation) | **Aligned** | Refusing `orca automations create|edit|remove|run` for the coordinator fits "Clay's Orca automation ... not adopted"; the refusal must bind the coordinator's verbs only, since the owner or `/sc:worktrees` automation docs may use them by hand (`scripts/worktree_cleanup_orca_automation.md`, PR #711). |

Searched DECISIONS.md, SPEC.md and the verdicts for `refuse(argv)`, `ordinary file`, `rm`, `delete`, `credential`, `transcript`, `200 messages`, `systemctl`, `escalat`, `row 5`, `row 8`: hits are D8 (SPEC:459), FR-26, FR-39, FR-47, D15 nine-row table (DEC:302), D16 VERDICT:99, QG3 VERDICT:61, FOLLOW-UPS:22 (token rotation has no stage). No plan file defines "ordinary files" or a 200-message cap (the 200 is Clay's number, `section-09.md:228`, not measured).

## Complementary issues

- **#787** (C6): the per-step verb list is tested against the refuse list; C6 needs C20's list, C20 needs C6's verb set. Same stage S13 (SPEC:497); interface: the list file and the per-step verb set.
- **#793** (C12): the playbook; S09-F16 (the order a worker's question must fail, then row 8) is the question-answering rule C12 holds ("how to answer a worker's question and when to escalate", S04-F9).
- **#797** (C16, now carrying C17 via #798): the merge gate; S09-F14's held entry ("naming row 5") needs a gate; the "safety files list" is path-based and does not catch skill deletions outside it.
- **#785** (C4) and **#791** (C10): they rely on the same list (the list must not widen when Orca's skill text changes; refuse typing into a busy terminal).
- **#802** (C21) and **#808** (C27): secrets and notices; compatible with S09-F34's credential refusals.
- **#698** (open): text-matching guards are best effort; this item inherits that.
- **#771** (open): its `/sc:worktrees` safety rules (`commands/worktrees.md`) must match the `rm` rules.
- **#322** (open): worktree write boundary design; same intent as the "inside its own work area" test.
- **#702 / #723 / #722** (open): protection of master and the shared-login limit; they close what S10-F47's "never delete a shared branch" only narrows.
- **#818** (W10, watcher): permissions of launched sessions; different sessions (launched agents, not the coordinator).

## Closest overlap

**#793** (C12, playbook for unsticking a worker and answering its questions). Shared: row S09-F16 (the ordered procedure a worker's question must fail before it is escalated as row 8) is the question-answering rule of #793's S04-F9; #801 itself says "read together with C12". Share of #801's done-when it covers: about 15 percent (the topic of one of six rows; none of #793's tests is the `row 8` fixture, so it covers the rule, not the test). Next closest: **#787** (about 10 percent; consumer of the refuse list and same S13 stage and test file) and **#797** (about 10 percent; the only possible host of the S09-F14 hold).

## Standalone or merge

**Verdict: stand alone, with one row (S09-F16) moved to #793.** Test against #793:
- *Owner*: both belong to the coordinator-skill author; #801's rows need two owner definitions ("ordinary files", the transcript call), #793 none.
- *Acceptance test*: #793 tests a playbook file (every state maps to an allowed action, no approval step); #801 tests `refuse(argv)` patterns one by one, a held-entry fixture and a question fixture.
- *Files touched*: #793 a skill ref and its test; #801 a limits/refuse module, `tests/coordinator/test_refuse_argv.py` and the merge-gate output.
- *Build phase*: #793 is Phase 2 and #801 is Phase 3 in #716's order.
- *Risk if merged*: a Phase 3 safety list that waits on owner definitions would drag a Phase 2 playbook, or the playbook's "no approval step" test would carry unrelated `rm` tests.
When merging would be right: if the owner does not re-adopt Clay's `refuse(argv)` (R38), the refusal rows lose their home and #801 shrinks to S09-F16 (into #793) and S09-F14 (into #797); then it should be closed with those rows redistributed. Merging the whole item into #787 would be wrong: C6 is a test of a verb set, C20 is the content of the list, and C20's rows have four different homes.

## Closed issues and merged PRs checked

- **#798** (C17, merged into #797 on 2026-11-24): the safety-files list; S09-F14 is a different check (skill/agent deletion the issue does not name), not covered by it (`D16 VERDICT:99`).
- **#796** (C15), **#804** (C23), **#806** (C25), **#809** (W1) (closed 2026-11-24): the owner closed rows that rest on R38-rejected architecture; the same test applies to #801's refuse-list rows.
- **#687 / PR #711** (merged): `scripts/worktree_cleanup.py` has a positive allowlist of exact argument shapes and no `rm`; the pattern to follow, and the rule the `rm` allow side contradicts.
- **#394 / #441 / PRs #432, #469** (merged): the launch-level guard for claim agents; it does not cover the standing coordinator or `coder`/`systemctl`/`orca automations`.
- **#668 / PR #683** (merged): `/sc:closeout` boundaries (never edits or deletes GitHub text, never releases a worker); consistent with the limits.
- **PR #700, #729** (merged): rolled back Clay's orchestrator design (where D8 and the nine-row table lived) and recorded R38.
- **PR #724** (merged): owner records in chat; the route to define "ordinary files".
- **#444, #507** (closed): no bearing.

## Updated recommendation

**Keep open with changes, P2, medium, size M. Unchanged from round 1 on action, priority, complexity and size; one reason added.**
Changes: (1) merge S10-F47 into S09-F10 as one `rm` rule and keep S10-F47's extra refusals; build the refusals first and ask the owner to define "ordinary files" in chat before the allow side; carve out `orca worktree rm` of a coordinator-created child (`WORKER-CONTRACT.md:237`). (2) Name the "session-read call" for S09-F27, or move the 200-message cap to the sweep reader (`src/superclaude/cli/sweep/probes.py:865` reads a 256 KiB tail, a size cap, not a message cap). (3) Move S09-F16 to #793 (C12) or cross-link it. (4) Mark S09-F14 blocked by #797 and by the owner's R38 ruling on the merge gate. (5) New: before the build, the owner states whether Clay's D8 `refuse(argv)` is re-adopted or the limits go into contract text and the existing guard instead; if not re-adopted, redistribute the rows as above. Priority stays P2 because the safety limits are wanted whatever the host, but nothing can be built before the coordinator substrate stage exists.

## Scan record

- Lists read in full: open-issues.tsv 134 of 134 lines, closed-issues.tsv 157 of 157, merged-prs.tsv 508 of 508.
- Search terms: refuse, rm, delete, deletion, limit, escalat, scope, transcript, credential, secret, guard, worktree, branch, protect master, permissions, write boundary, playbook, merge gate, closed list.
- Opened in full (read-only `gh`): open issues #716, #787, #793, #797, #785, #791, #802, #808, #698, #771, #322 (statement and references; design body only skimmed), #678, #702, #723, #722, #818 (16); closed issues #798, #796, #804, #806, #809, #394, #441, #687, #668, #507, #444 (11); merged PRs #432, #469, #711, #683, #700, #729, #724, #591 (8).
- Plan files read: SPEC lines 62, 228, 241, 258, 435-463, 497; DEC 302, 504; D16 VERDICT:99; QG3 VERDICT:61; `section-09.md:118,137,228,287`; `section-10.md:369-372`; R38. UNVERIFIED: Clay's design text for "row 5" and "row 8" (the row numbers come from `section-09.md:118` and `:137`; the design file lives only on the archive branch); whether the owner re-adopts D8; whether the guard hook ever sees coordinator commands (round 1).
