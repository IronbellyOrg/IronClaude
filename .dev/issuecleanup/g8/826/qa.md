VERDICT: PASS

QA of /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g8/826/findings.md, checked 2026-11-25 against live gh and the local refs origin/integration (4e35750e7) and origin/master (f2894fc44). No fetch was run.

## Verified claims

- Owner decision comment: exact match. Issue 826 is OPEN, label `enhancement`, issue type Feature, no assignees, no closing PR. Its single comment (author ironbelly) records the release PR from `integration` to `master`, opened by a person, merged as a merge commit, tagged on that commit. Options 2 and 3 dropped. Steps 2 to 5 can start.
- `docs/developer-guide/release-procedure.md` on origin/integration: line 3 (CI triggers on `master` and `integration`), line 22 ("Every merge to `master`"), line 59 (`--base master`), line 71 (G2, `--branch master`), line 88 ("never a later `master` commit"). All five line numbers are exact, and these are the only master mentions.
- `src/superclaude/skills/sc-post-release-protocol/SKILL.md:91` uses `git merge-base --is-ancestor <tag> <default-branch>`, and the default branch is auto-detected ("do not assume main/master"). The `gh repo view` default branch is `integration`. Line 74 and line 304 repeat the WARN rule. `commands/post-release.md` has no master, base-branch or ancestor text (grep: only unrelated "Default" and "Integration" table words).
- Ancestry reasoning is sound. A tag on the merge commit M (parents: master tip, integration tip) is not an ancestor of integration until master is merged back. Today `origin/master` is an ancestor of `origin/integration` (checked), so the problem appears only after the first release PR.
- `impact.md:23`, `auggie-review.md:37` and `:113` use `origin/master`. Exact.
- `CLAUDE.md` on origin/integration: line 290 branch structure, line 297 "Merge to `integration` -> validate -> merge to `master`", and lines 290 to 297 match the issue's range. No release-PR commands.
- No post-release base-branch test. The only hits are `tests/skills/test_worker_contract.py:2371-2384`, `tests/core/test_how_we_work_routing_table.py`, `tests/unit/test_cli_install.py` (file lists) and `tests/recommend/fixtures`. The eval suite `post_release_command_contract.yaml` has no branch or ancestor assertions. The `--is-ancestor` tests that exist are for pr-submit and closeout, not post-release.
- PRs: 824 MERGED (base integration, 2026-11-24T23:25:39Z); 658 MERGED into master (release 6.1.0); 640 MERGED into master (release 6.0.0); 639 MERGED into integration; 663 CLOSED unmerged; 634 MERGED into integration. #702, #723 and #571 are all OPEN.
- Complexity medium, size M, P2 are consistent with the issue's own "Medium" priority and the work listed. Next steps 2 to 6 match the issue's Fix approach and add one justified item (the ancestry check).

## Blocking defects

None.

## Non-blocking notes

1. Wrong history claim (findings line 13). It says the project merged master back into integration "after 6.0.0 and 6.1.0: PR 639 merged, PR 663 closed". PR 639 (merged 2026-11-18T15:46Z) landed BEFORE release PR 640 (16:30Z). It was a conflict-resolution merge of master into integration done before the release, not a post-tag merge-back. PR 663 was closed unmerged, so no merge-back after 6.1.0 happened. The git-semantics conclusion and step 2 ("decide whether master is merged back") still hold. Only the precedent is misdescribed. Suggested fix: "no post-tag merge-back is recorded; 639 was a pre-release conflict merge and 663 was closed".
2. Unmentioned history point. PR 663's title says "6.1.0 squash", so 6.1.0 was squashed into master. The owner's rule (merge commit) therefore differs from the 6.1.0 practice. The tag-ancestry problem also existed then (a squash commit is never an ancestor either). Worth one line in step 2.
3. "A gap the issue does not name" is slightly strong. The issue's acceptance criterion "`/sc:post-release` reads the right base for the release it checks, and a test covers it" does cover it in general. The findings add the specific mechanism, which is useful.
4. The findings already flag that the refs were not fetched. This QA used the same refs plus live gh. The PR and issue states are live. File content is as of the local origin/integration.
5. Step 4's note that `impact.md` and `auggie-review.md` likely need `origin/integration` is a judgment, correctly hedged.
