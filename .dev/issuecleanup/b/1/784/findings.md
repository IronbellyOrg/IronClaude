# Round 2 findings for issue 784 (C3): Return contract printed last

Checked on master f2894fc44 (branch ironbelly/Realign, clean), 2026-11-24. Round 1: `/home/coder/workspaces/worktrees/IronClaude/Analyze716/.dev/issuecleanup/a716/1/784/findings.md`. Command run: `/sc:analyze src/superclaude/skills/sc-closeout-protocol --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/b/1/analyze` (succeeded). Master check: no coordinator skill or contract. The pattern exists: result block printed last, also after a stop, in `src/superclaude/skills/sc-closeout-protocol/SKILL.md:69` with the fixed shape `templates/result.md` (`closeout:` YAML, `status: complete | partial | stopped`) and test `tests/skills/test_closeout_protocol.py:3301`.

## Alignment with architectural decisions

- **R38** (`.dev/releases/backlog/issue-watcher-zero-setup/requirements.md:64`, clause D): "the coordinator never merges or closes on its own". PARTLY ALIGNED: a printed contract is read-only reporting and breaks nothing, but its `outcome` words must not suggest an autonomous merge or close; `outcome` should reuse the existing `succeeded|failed|blocked|partial` words of `superclaude issue-pipeline complete` (`src/superclaude/core/WORKER-CONTRACT.md:302`) and carry no "merged" word of its own.
- **SPEC.md:228 (FR-26)**: one JSON contract for the verbs, NOT BUILT. UNRESOLVED CONFLICT in format: closeout and claim skills print YAML; FR-26 says JSON for verbs. The plan does not say which one C3 uses (as the issue says, UNVERIFIED). No decision record settles it (searched DECISIONS.md, D15 and SPEC for "return contract": no hit).
- **WORKER-CONTRACT.md WC-16** (`:288-290`): the coordinator "never stops watching on its own". PARTLY ALIGNED: "when an issue's workflow ends" must mean one issue ending, not the session; the issue does not say when the block prints for a standing session.
- **WORKER-CONTRACT.md WC-4 / return-contract.yaml** (section 2) and never-as-worker list (`:23`): the worker `return-contract.yaml` is for commands run as workers; the coordinator is never a worker (`/sc:coordinator` is not yet on the list or in `tests/skills/test_worker_contract.py:474-485`). The new block must be named differently to avoid a reader mixing the two. PARTLY ALIGNED.
- **D08** (`debates/D08/VERDICT.md:63-66`): names `/sc:coordinator`, `sc-coordinator-protocol`. ALIGNED.
- **D15 G6** (`debates/D15/VERDICT.md:134`): wave detail from the 681 design is not owner-approved; the contract's fields (issue, PR, outcome, round, escalations, Run id) come from 655 row S02-F55. PARTLY ALIGNED: round and Run id belong to items (#799 C18, #786 C5) not yet built, and the fields may print as `null` until then.
- **Owner decision 2026-11-24 closing #796, #798, #804, #806**: none changes C3's fields. `escalations` depends on C12 and C13, still open.

## Complementary issues

- #782 (C1) and #783 (C2): C1 hosts the wave that prints the block; C2 supplies the `stop` code. C3 is blocked by both.
- #800 (C19): settles each worker; C3 reports what C19 settled. Paired; the umbrella puts them in one cluster.
- #786 (C5) supplies the Run id; #799 (C18) supplies the round; #793/#794 (C12, C13) supply `escalations`. C3 prints their values, `null` before they exist.
- #771: "not done" result from closeout needs somewhere to go; C3's block is a candidate destination. #770: results flow worker to coordinator (the opposite direction).

## Closest overlap

**#771 "Wire /sc:closeout and /sc:worktrees into the coordinator's finish, and give a 'not done' result somewhere to go".** Shared: both define what the coordinator reports at the end of an issue, including the hand-back of unmet criteria (closeout's `issue.handback: remaining`). It covers about 20 percent of C3's done-when (the end-of-issue report and where an unfinished result goes), and none of the parse-test or early-stop path. Next two: #800 (C19, about 10 percent: the settled-worker part of the contract) and #770 (about 5 percent: results coming back to the coordinator, different direction).

## Standalone or merge

**Stand alone.** Tested against #771: owner, #771 is owned by the owner's coordinator-duty decision (three open questions, including merging into #716 C16-C19), C3 by the skill author; acceptance test, different (C3: a fixture run prints a contract a test parses, a stopped run still prints one; #771: closeout runs after a person's merge and a not-done result reaches the coordinator); files, C3 in `SKILL.md` plus `templates/` plus a test, #771 in WORKER-CONTRACT duties and a wake step; build phase, C3 is phase 2 after C19, #771 phase 3 (C16-C19 area); risk if merged, C3's format question (YAML or JSON) would be held up by #771's owner questions, and #771's duty change would be dragged into a template item. Merging would be right only if the owner chooses to have closeout's own result block be the contract; that is a design choice not made anywhere.

## Closed issues and merged PRs checked

- PR #683 / #668: closeout prints a fixed result block last, from wave 0, with `status` words and `escalations`; the pattern C3 copies. It is the nearest existing "contract" and could even be nested in C3's block.
- `sc-issue-protocol` claim skill contract (`SKILL.md:105-150`, `tests/skills/test_issue_protocol.py:646,664`): YAML, `status: success | stopped | failed`.
- PR #693 / #691 (launch-result.json): a launch file, not a coordinator contract (same note as the #716 backlog review).
- PR #411, #422, #508, #507: worker `--unattended` contract and per-command return contracts; not for the coordinator.
- #796, #798, #804, #806, #809, #813 (closed 2026-11-24): do not affect C3.
- #655 (closed not planned) and PR #700, #729: R38 context; PR #681's design text with the original contract wording is gone from master.

## Updated recommendation

Suggested action: **keep open with changes**: (1) decide and write whether the block is YAML like the claim and closeout skills or the FR-26 JSON; (2) state when it prints for a standing coordinator (when one issue's workflow ends, and after any stop), and name the block so it is not mistaken for the worker `return-contract.yaml`; (3) reuse `succeeded|failed|blocked|partial` for `outcome` and add no word that implies the coordinator merged or closed (R38 clause D); (4) allow `null` for round, Run id and escalations until C18, C5 and C12 exist; (5) keep it behind C1, C2, C19 and say how #771's hand-back result reaches it. Priority **P3** (unchanged). Complexity **medium, size M** (unchanged). Unchanged from round 1; added: R38 clause D constraint, the WC-4 naming clash and #771 as the closest overlap.

## Scan record

Lists read in full: open-issues.tsv 134 of 134, closed-issues.tsv 157 of 157, merged-prs.tsv 508 of 508 (titles). Search terms: return contract, result, contract, closeout, outcome, handback, settle, escalation, worker_done, complete. Opened with gh: open #716, #782, #783, #785, #786, #788, #790 to #792, #799, #800, #801, #771, #770, #761, #767, #774, #776, #777 (about 19); closed #668, #507, #450, #796, #798, #804, #806, #809, #813, #655; PRs #683, #411, #700, #701, #729, #735. Plan files: R38, SPEC lines 62, 228, 498, WORKER-CONTRACT lines 23, 288-302. UNVERIFIED: the contents of WC-4's `return-contract.yaml` field list (not reread in round 2); whether the owner wants the closeout block nested in the contract.
