# Independent review of PR 697 (revert of PR 682)

Reviewer: independent reviewer (did not produce PR 697). Read-only on the repository; work in /tmp/pr697-review/.
Head reviewed: fd23c01a9ca1f5aee44522f8107a07104f780c4f (origin/ironbelly/revert-pr-682). origin/master at review time: 7f0919345479007ad72724dd16b4e4cf08136e65.
Base compared: 01e7a9e23^ = c2a1395522239429dd21f19cadd206fd643fec03.

## Q1 Inverse check on the 36 files

Result: YES, with exactly the declared differences and nothing UNEXPLAINED.

Commands run (all from /home/coder/workspaces/IronClaude, `H=origin/ironbelly/revert-pr-682`):

1. `git diff --name-status 01e7a9e23^ 01e7a9e23` gave 36 paths (28 deleted, 8 modified; PR 682 author `clayphi`; 35 insertions, 4599 deletions).
2. For every one of the 36 paths: `git rev-parse "01e7a9e23^:<path>"` against `git rev-parse "$H:<path>"`. Output summary: 33 SAME, 3 DIFFER. The three that differ are `CHANGELOG.md`, `src/superclaude/core/WORKER-CONTRACT.md`, `tests/skills/test_worker_contract.py`. The 33 identical blobs include the whole `src/superclaude/cli/issue_pipeline/` package, `tests/issue_pipeline/` with fixtures, `src/superclaude/cli/main.py`, both copies of `launch-level-guard.sh`, `tests/hooks/test_launch_level_guard_worker.py`, `tests/cli/test_issue_pipeline_registered.py`, `docs/user-guide/cli-groups.md` and `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md`.
3. Independent mechanical cross-check: in a throwaway index (`GIT_INDEX_FILE=/tmp/pr697-review/y`) I ran `git read-tree origin/master` then `git apply -R --cached --exclude=CHANGELOG.md archive/pr-682/pr-682-forward.patch` (exit 0), wrote the tree (`dc07f7de29f8152b539e65b58cf240c840188b6e`) and compared it with the PR head: `git diff --name-only <that tree> $H` printed only `CHANGELOG.md`, `src/superclaude/core/WORKER-CONTRACT.md`, `tests/skills/test_worker_contract.py`. So the pure inverse of 682, applied to today's master, equals PR 697 on 33 of 36 files. (The same reverse apply with CHANGELOG.md included fails on that file's context, which is why CHANGELOG is declared and was resolved by hand.)

Line classification of the three differing files (full diff base to head printed with `git diff 01e7a9e23^ $H -- <file>`):

CHANGELOG.md (3 hunks)
- `+### agent-work-report: ...` entry (4 lines): later master commit d7d645ddd (#684) (`git log -S` confirms).
- `+### Restored: the plan-approval gate removed by PR 682 ...` entry: declared difference (a). It replaces 682's `### Removed: the old plan-approval gate` entry in place (`git diff origin/master $H -- CHANGELOG.md` is a 2-line swap and nothing else).
- `+### New command: /sc:closeout ...` entry: later master commit 8b2ce556c (#683).
- UNEXPLAINED: none.

src/superclaude/core/WORKER-CONTRACT.md (4 hunks)
- line 23, `/sc:closeout` added to the never-as-worker list: later master commit 8b2ce556c (#683).
- line 59, WC-17 step 4 gains `--issue <N>` and the parenthetical `(<N> is the issue number in the brief's Report directory line; --issue makes an approval for another issue with the same plan hash refuse)`: fd23c01a9.
- line 66/67, new bullet `**Messages carry no --to.**`: the no-`--to` carry-over. Text is byte-identical to the line 682 added (`diff` of the two `grep -F` lines printed "identical").
- line 298, "Worktree, then worker" duty reworded (`without launching an agent of its own (it must copy the claim's issue folder in first)` and `so the worker is that worktree's agent and the worktree is never left without one or used by anyone else`): fd23c01a9.
- UNEXPLAINED: none.

tests/skills/test_worker_contract.py (8 hunks)
- never-as-worker phrase and the `NEVER_AS_WORKER` tuple gain `/sc:closeout`: 8b2ce556c (#683).
- `_CLOSEOUT_LANDED`, `_CLOSEOUT_SETTLE`, `_CLOSEOUT_REASON` constants and 13 closeout rows in `WRITE_VERB_CLASSIFICATION`: 8b2ce556c (#683).
- the `agent-work-report/SKILL.md` `git add+git commit` classification row: d7d645ddd (#684).
- phrase `so the worker is that worktree's agent` (rule `issue-pipeline-duties`) and phrase `--issue <N> --line <the reply text>` (rule `wc17-plan-approval`): fd23c01a9.
- `messages-carry-no-to` rule entry and `test_the_no_to_rule_sits_in_the_worker_session_duties`: the no-`--to` carry-over.
- UNEXPLAINED: none.

The reverse-apply cross-check of item 3 above independently shows the same residue for the two non-CHANGELOG files: only the WC-17 line, the "Worktree, then worker" line and the no-`--to` bullet in the contract, and only two phrases, the `messages-carry-no-to` entry and its test in the test file.

Also: the guard script blob at the PR head equals the blob before 682 (`77d52e6fe0c81f671f009b4b207e73cdcc5dba65` on both sides), and `diff` shows the src and plugin copies of the guard byte-identical at the head (and on master).

## Q2 Diff against current master and mergeability

Result: YES to both.

- `git fetch origin` run first. `origin/master` = 7f0919345479007ad72724dd16b4e4cf08136e65 at review time (it is also the merge base of the PR head, so the PR head is master plus two commits).
- `git diff --name-only origin/master $H | sort` against the 36 paths of PR 682, with `comm -23` and `comm -13`: both empty. The PR touches exactly the 36 files PR 682 touched and no other file (`git diff --shortstat origin/master $H`: 36 files changed, 4614 insertions, 24 deletions; the line counts depend on diff alignment and prove nothing by themselves; Q1 is the proof).
- `git diff --summary origin/master $H | grep mode` shows only file creates (mode 100644); no mode change on an existing file.
- `git merge-tree --write-tree origin/master $H` printed tree `5d057fef3310e7b5bf3c668969d496c79b59f43a`, exit 0, no conflict. `git merge-base origin/master $H` equals `origin/master`, so the merge is a fast-forward.
- `gh pr view 697 --repo IronbellyOrg/IronClaude --json ...` (read-only): state OPEN, mergeable MERGEABLE, mergeStateStatus CLEAN, headRefOid fd23c01a9, checks Test on Python 3.10, both Swarm acceptance lanes, Lint/Plugin/Sync/Dependency, Doctor and Test Summary all SUCCESS.

## Q3 Saved copy completeness

Result: COMPLETE.

- `GIT_INDEX_FILE=/tmp/pr697-review/x git read-tree 01e7a9e23^ && git apply --cached .dev/brainstorms/20261120-pr686-unify/archive/pr-682/pr-682-forward.patch && git write-tree` printed `4c1aa20989ad8729d994d58260b5db307ac9f999`.
- `git rev-parse 01e7a9e23:` (tree of the PR 682 squash commit) printed `4c1aa20989ad8729d994d58260b5db307ac9f999`. Identical, so the patch applied to the pre-682 tree reproduces PR 682 exactly.
- The pre-682 tree was `2849c14cc7f5a3d3a18d52bcd816402efeb07380` (different, as expected).
- `git ls-remote --tags origin | grep pr-682` printed `6eee32bfd084b612d275eaa01c28b165271224e9 refs/tags/archive/pr-682-issue-pipeline-removal` and the peeled line `01e7a9e23519fd54bc438bb1a1a0e03dcdae5baf refs/tags/archive/pr-682-issue-pipeline-removal^{}`. `git for-each-ref refs/tags/archive` shows an annotated tag object pointing at the PR 682 squash commit. The tag exists on origin.
- The archive folder also holds JSON of commits, conversation comments, inline review comments and reviews (`ls` confirms the files exist); I did not compare their content with GitHub (UNVERIFIED beyond file presence).

## Q4 Dangling references and test run

Result: no dangling reference; all requested tests pass; `issue-pipeline` is listed.

Static checks (on `git archive` exports under /tmp/pr697-review/head and /tmp/pr697-review/master):

- Registration: `git diff origin/master $H -- src/superclaude/cli/main.py` is exactly the 4 lines `from superclaude.cli.issue_pipeline.cli import issue_pipeline_group ...` and `main.add_command(issue_pipeline_group, name="issue-pipeline")`, placed between `issue-watch` and `sweep`, the same blob as before 682. The package's imports (`superclaude.cli.issue_watch.cycle`, `.github as gh`, `.runner.Runner/SubprocessRunner`) exist at the head, and no commit after 682 touched `src/superclaude/cli/issue_watch` (empty `git log` output, see Q6).
- Guard: `src/superclaude/hooks/scripts/launch-level-guard.sh` and `plugins/superclaude/hooks/scripts/launch-level-guard.sh` are byte-identical at the head (`diff` printed nothing) and on master. The only diff of either against master is the restored G2 TAMPER `case` line plus two comment lines (printed in full during the review).
- Contract copy: `find . -name WORKER-CONTRACT.md` outside `.dev/` finds only `src/superclaude/core/WORKER-CONTRACT.md`; there is no plugin or docs mirror to keep in sync (the brief template in `src/superclaude/cli/issue_pipeline/templates/worker-brief.txt` is checked against the contract by `tests/issue_pipeline/test_brief.py`, which passes).
- Mentions of the pipeline elsewhere (`grep -rIl -E 'issue-pipeline|issue_pipeline'` outside the package, excluding `.dev/`): CHANGELOG, `docs/designs/*`, `docs/user-guide/cli-groups.md`, the guard scripts, `main.py`, the contract and the three test files. No skill or command file under `src/superclaude/skills` or `src/superclaude/commands` mentions `issue-pipeline`, `WC-17` or the plan-approval gate, so `/sc:closeout`, `/sc:issue` and the agent-work-report skill carry no stale instruction (see N4 for the one soft interplay and M1 for `docs/designs/orchestrator.md`).

Test run:

- First run in a plain `git archive` export (no `.git`): `uv run pytest tests/issue_pipeline tests/cli/test_issue_pipeline_registered.py tests/hooks tests/skills/test_worker_contract.py -q -x -p no:cacheprovider` stopped at `tests/issue_pipeline/test_approval_record.py::test_the_watcher_record_module_is_not_edited` (`CalledProcessError: ['git', 'diff', '--stat', 'HEAD', '--', 'src/superclaude/cli/issue_watch/record.py'] returned non-zero exit status 1`). Cause: that restored test runs `git diff --stat HEAD` and an export has no repository; it is environmental, not a defect of the PR. It cannot fail on master because master has no such test (the test file is one of the restored ones), so a clean master export is not a comparison for it. UNVERIFIED only in the sense that I did not run it on master (it does not exist there).
- Second run in a throwaway clone with a work tree (`git clone --no-hardlinks` of the local repo into /tmp/pr697-review/headgit, `git checkout fd23c01a9`), same selection without `-x`: `5540 passed, 13 skipped in 565.75s`, exit 0. No failure.
- The PR description's own figure: `uv run pytest tests/issue_pipeline tests/cli/test_issue_pipeline_registered.py tests/hooks/test_launch_level_guard_worker.py tests/skills/test_worker_contract.py -q` in the same clone: `1013 passed in 10.78s`. Matches the "1013 passed" claim.
- `uv run superclaude --help` (head export): exit 0 and the Commands list contains `issue-pipeline  Approval core for a coordinator-started plan-writing...` between `install-skill` and `issue-watch`. `uv run superclaude issue-pipeline --help`: lists `adopt-create`, `adopt-mark`, `check-approval`, `init`, `plan-hash`, `record-create`, `record-mark`, `record-show`, `release-worker`, `stage-status`.
- Same `--help` on a clean export of `origin/master`: `issue-pipeline` is absent (`superclaude --help | grep issue-` shows only `issue-watch`) and `superclaude issue-pipeline --help` prints `Usage: ... Try 'superclaude --help' for help.` (no such command). So the restore is what makes the group appear.
- Not run: the full repository suite (`uv run pytest` over all of `tests/`) and `make verify-sync` (UNVERIFIED by me). The PR's checks on GitHub for head fd23c01a9 are all SUCCESS (see Q2), which covers the CI suite.

## Q5 Review of fd23c01a9

`git show --stat fd23c01a9`: 2 files, 4 insertions, 2 deletions (`src/superclaude/core/WORKER-CONTRACT.md` two lines changed, `tests/skills/test_worker_contract.py` two lines added). The commit was read line by line and each claim checked against the restored code in the PR head.

1. WC-17 step 4 now reads `superclaude issue-pipeline check-approval <report-dir> <plan file names> --issue <N> --line <the reply text>` and adds `(<N> is the issue number in the brief's Report directory line; --issue makes an approval for another issue with the same plan hash refuse)`.
   - `--issue` exists: `src/superclaude/cli/issue_pipeline/cli.py` lines 76 to 93, `@click.option("--issue", type=click.IntRange(min=1), default=None, help="Also require this issue number in the record id.")`. `--line` is required, `--issue` optional. Click accepts the options in either order, so the written order is valid.
   - What it enforces: `approval_line.py` `check()` returns `refused:malformed` for a non-matching line, `refused:bare` for the short word `approved`, `refused:<reason>` for a plan-hash failure, `refused:mismatch` when the claimed hash differs from the computed hash, and (only when `issue` is given) `refused:mismatch` when the record id does not start with `ap-<issue>-plan-`. The id is `ap-<issue>-plan-<first 12 hex of the hash>`, so `ap-12-plan-` does not satisfy `--issue 1` (the hyphen closes the number). The parenthetical states exactly this: true.
   - Without `--issue` an approval minted for issue 9 passes for issue 10's worker when both have identical plan files (test `tests/issue_pipeline/test_approval_line.py` lines 71 and 95 cover the issue=9 pass and issue=10 refusal). The change closes a real gap in the contract text.
   - Where the worker gets N: `src/superclaude/cli/issue_pipeline/templates/worker-brief.txt` has `Report directory: .dev/issues/{N}/worker-plan`, rendered by `brief.py` with a validated issue number. So N is readable from the brief's `Report directory` line, as the parenthetical says. Correct. The coordinator's reply form `approved <record-id> plan-sha256=<hash>` (contract line 299) matches what the check expects.
2. "Worktree, then worker" duty now reads: the worktree step `creates or reuses the worktree without launching an agent of its own (it must copy the claim's issue folder in first)`, then `worker-start ... straight after it, so the worker is that worktree's agent and the worktree is never left without one or used by anyone else`.
   - Against `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` docstring lines 23 to 40: "finds or creates the Orca worktree issue-<N>" (creates or reuses: true); "`orca worktree create` (no link flag, no agent flag)" and "The create has no agent because the claim must copy <D> into the worktree before its agent starts" (without an agent and the copy-first reason: true); the script then closes the plain first terminal tab (so no agent runs there). All true.
   - "so the worker is that worktree's agent and the worktree is never left without one or used by anyone else" is a stated intent, not a mechanism: if `worker-start` does not return ready the same section marks the row `uncertain`, and the worktree then has no agent until the coordinator settles it via `worker-list`. As a duty ("straight after it") it is consistent with contract line 233 (every worktree created by Orca) and with line 282; as a literal invariant "never" is slightly stronger than the failure path allows. Wording only: see Note N1.
3. Added test phrases. I ran `git show a6d0889c2:src/superclaude/core/WORKER-CONTRACT.md` (the contract without the fd23c01a9 text) into the throwaway export and ran `uv run pytest tests/skills/test_worker_contract.py -q -p no:cacheprovider`: 2 failed, 674 passed. The failures were `test_contract_states_rule[issue-pipeline-duties]` (`missing phrase "so the worker is that worktree's agent"`) and `test_contract_states_rule[wc17-plan-approval]` (`missing phrase '--issue <N> --line <the reply text>'`). Restoring the fd23c01a9 contract (blob `dfaac01c4737c986a6b73911740de5dde00c8616`, equal to `git rev-parse fd23c01a9:<path>`) passes. So the added test entries fail without the change: meaningful as text pins.
   - Limit: they pin wording, not behaviour (a phrase `--issue <N>` could survive while the CLI changes). The CLI behaviour itself is covered by `tests/issue_pipeline/test_approval_line.py`. Acceptable.
4. Contradictions with other contract lines: none found. WC-17 step 4 now matches the CLI help; the duties section line 299 `approved <record-id> plan-sha256=<hash>` and the brief template line `Plan approval: ... follow rule WC-17` agree with it. The `Messages carry no --to` bullet repeats the sentence already inside WC-17 (same words twice in section 3); see Note N2.
5. Process: PR 697's description still says "It is one new commit on top of current master", but the branch now has two commits (a6d0889c2 and fd23c01a9). Wording only: Note N3.

## Q6 Other problems

Checks and results (none produced a blocking item):

- Stale line numbers: `src/superclaude/cli/main.py` registration sits at lines 581 to 583 of the head (diff hunk `@@ -578,6 +578,10 @@` against master), which is the position `docs/designs/orchestrator.md` line 1017 names for PR D. No other restored file cites a line number of a file that changed since 682: `git log --oneline 01e7a9e23..origin/master -- src/superclaude/cli/issue_watch src/superclaude/skills/sc-issue-protocol src/superclaude/hooks tests/hooks plugins/superclaude/hooks src/superclaude/cli/main.py` printed nothing, so no later commit touched anything the restored package, guard or hook tests depend on. The only later commits that touched the three declared files are 8b2ce556c (#683) and d7d645ddd (#684).
- Lost `/sc:closeout` or agent-work-report mention: none. `/sc:closeout` is in the contract never-as-worker list (line 23), in `NEVER_AS_WORKER` and in the tests; the agent-work-report CHANGELOG entry and the `agent-work-report/SKILL.md` classification row are present at the head. `git diff origin/master $H` shows no deletion of either.
- Duplicated CHANGELOG headings: `grep -n '^#' CHANGELOG.md | sort | uniq -d` printed only `#### Changed`, which is in older released sections, not in `[Unreleased]`. The four `[Unreleased]` headings are unique.
- Anchor in `docs/user-guide/cli-groups.md`: lines 21 and 22 link `#superclaude-issue-pipeline-and-superclaude-review`; the heading at line 80 is `## \`superclaude issue-pipeline\` and \`superclaude review\``, whose GitHub slug is exactly that. The subcommand list on line 84 (`init`, `adopt-create`, `adopt-mark`, `check-approval`, `plan-hash`, `record-create`, `record-mark`, `record-show`, `release-worker`, `stage-status`) matches the ten commands `uv run superclaude issue-pipeline --help` prints. Other docs link no anchors into this file or into SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md (`grep` for `cli-groups.md#` printed nothing).
- Tests pinning text that no longer exists: none; the Q4 run passes with the restored pins. Two weaknesses are listed below.
- PR 697 description facts: "1013 passed" is for the four test targets of the PR; my Q4 count is in section Q4.

Findings (non-blocking):

- M1 (Medium). `docs/designs/orchestrator.md` on master still records the retirement of the plan-approval gate as the decided design and plan: line 33 ("One system replaces ... the plan-approval gate"), line 73 (R1 "no plan-approval gate after the claim"), line 991 and 1017 (PR D row listing `src/superclaude/cli/issue_pipeline/` and `main.py:581-583` for removal), line 1095, line 1381 ("Dropped: plan-approval gate (WC-17 ...)"). After PR 697 merges, that design contradicts the code and the contract, and anyone following it will try to remove the package again. Consequence if corrected: the design carries a note that PR D was reverted by 697 at the owner's request and the gate decision is open. No named decision or acceptance check of PR 697 rests on this; the PR text itself says the owner will decide later. Follow-up candidate.
- N2 (Note). The no-`--to` rule is now stated twice in section 3 of the contract (WC-17 and the standalone bullet), and `test_the_no_to_rule_sits_in_the_worker_session_duties` passes even with the bullet deleted because WC-17's sentence lies inside the same section (shown by deleting the bullet in the throwaway export: `-k 'no_to or messages'` gave 1 failed `messages-carry-no-to` entry and 2 passed, the passing ones including that test). The bullet is pinned only by the rule entry `messages-carry-no-to`. The comment above that test, `# --- The no-to rule, kept after the plan-approval gate was retired (issue 655) ---`, is false after the restore (`tests/skills/test_worker_contract.py` near the end of the file).
- N3 (Note). PR 697's description says "It is one new commit on top of current master"; the branch has two commits (a6d0889c2, fd23c01a9). The description and the CHANGELOG also call the guard rule "G2.1"; no restored file uses that label (the guard comments say "G2", and `docs/designs/issue-pipeline-guard-g2.md` is the reference). The label comes from PR 682's own comment wording.
- N4 (Note). Interplay with `/sc:closeout`: the restored duties line `Never: ... post an issue write without that issue's grant row` applies to a watcher-claimed issue the coordinator owns, and `/sc:closeout` writes a closing note and closes the issue. `docs/designs/sc-closeout.md` line 685 says the orchestrator calling it is "a coordinator with grants", and the skill itself does not mention a grant row. No contradiction in text; the two documents just do not point at each other. I found no code path that makes closeout skip or check a grant row (UNVERIFIED beyond a grep of the skill, command and design for `grant`).

## Findings summary

Blocking: 0
Medium: 1 (follow-up candidate, not a reviser item)
Note: 4

Medium
- M1. `docs/designs/orchestrator.md` on master still records the gate retirement as the decided design (lines 33, 73, 991, 1017, 1095, 1381). Evidence in Q6.

Notes
- N1. "the worktree is never left without one" in the reworded "Worktree, then worker" duty is stronger than the `uncertain` failure path of the same section. Evidence in Q5.
- N2. The no-`--to` rule is stated twice in contract section 3; the test `test_the_no_to_rule_sits_in_the_worker_session_duties` passes without the bullet and its comment says the gate was retired. Evidence in Q6.
- N3. PR description says "one new commit" (two exist) and both it and the CHANGELOG call the guard rule "G2.1", a label no restored file uses. Evidence in Q6.
- N4. `/sc:closeout` and the restored "post an issue write without that issue's grant row" line do not reference each other. Evidence in Q6.

What was checked and why there is no blocking finding: every one of the 36 files of PR 682 by blob (33 identical to the pre-682 tree) and by an independent reverse-apply of the saved patch on current master (residue is only the three declared files); every changed line of the three declared files classified to a later master commit (8b2ce556c, d7d645ddd), the no-`--to` carry-over or fd23c01a9, none unexplained; no file outside the 36 changed; merge onto current master is a clean fast-forward and GitHub shows MERGEABLE and CLEAN with all checks green; the saved patch reproduces PR 682's tree exactly and the annotated tag is on origin; the restored package, registration, guard (both copies identical), docs anchor and subcommand list agree with the CLI; 5540 tests passed and `issue-pipeline` is listed by `superclaude --help`; fd23c01a9's `--issue` text matches the CLI option and its enforcement, the brief gives the worker N, the worktree rewording matches the `orca_worktree.py` docstring, and the new test phrases fail without the change. No named decision, acceptance check, required piece or safety boundary changes if any of M1 or N1 to N4 is corrected.

verdict: PASS
