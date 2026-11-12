# Step 1.16a record: PR #422 and #409 (item 7.19, record-only)

Run 2026-11-11T22:33Z in the worktree `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode` (HEAD `5dc29d23b15eb7db4ead50623bb409f696a0d7d3`; the local `origin/master` ref is `35073356ec1a7f28f8e6c9619eb30eb6b7cc0c84`, not refreshed: the item forbids fetch). Reference: research/09 Gap 3 "1.16a": #422 is MERGED at `2327fbd3`, and `495eb96d` is not an ancestor of `origin/master`. No fetch, rebase, push or PR action was run; the three commands below only read.

## 1. PR #422 state (the `gh` state line)

Command: `gh pr view 422 --repo IronbellyOrg/IronClaude --json state,mergedAt,mergeCommit`

Exit: 0. Output:

~~~
{"mergeCommit":{"oid":"2327fbd37819d4013ffc57511dc4ef5011c3bf27"},"mergedAt":"2026-11-07T14:15:58Z","state":"MERGED"}
~~~

Result: `state` is `MERGED`, merge commit `2327fbd37819d4013ffc57511dc4ef5011c3bf27` (its first 8 characters are `2327fbd3`, the commit research/09 names), merged 2026-11-07T14:15:58Z. This matches research/09.

## 2. First ancestor check (expect exit 0)

Command: `git merge-base --is-ancestor 2327fbd3 HEAD; echo "exit=$?"`

Output: `exit=0`

Result: `2327fbd3` (the #422 merge commit; `git cat-file -t 2327fbd3` prints `commit`) is an ancestor of HEAD. As expected.

## 3. Second ancestor check (expect exit 1)

Command: `git merge-base --is-ancestor 495eb96d origin/master; echo "exit=$?"`

Output: `exit=1`

Result: `495eb96d` (`git cat-file -t 495eb96d` prints `commit`) is NOT an ancestor of `origin/master`. As expected, so the `495eb96d` pin stands and no layout diff is needed. The `origin/master` used is the local ref named above; it was not fetched.

## 4. Note

Every `WORKER-CONTRACT.md` and `test_worker_contract.py` line cited by steps 1.17 to 1.19 is re-read at HEAD before it is edited (items 12.1 to 12.3).

## Verification

Four points recorded with the command outputs. PR #422 is MERGED and check 2 passed (exit 0) and check 3 matched (exit 1), so the HALT with `blocker_reason: "Step 1.16a: PR #422 state or ancestry differs from research/09; DESIGN step 1.16a needs a revision"` does not apply.
