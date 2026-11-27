review: 2 of 3

Saved by the orchestrator from the re-reviewer's final message (reflect-reviewer, opus, read-only). The Step 1 evidence block (the 30-line `diff -w` between the plan before and after the repair) is not copied here; its source is the baseline `.dev/tasks/archive/TASK-WF-designRev1-20261126-141220/TASK-WF-designRev1-20261126-141220.md` against the candidate `.dev/tasks/to-do/TASK-WF-designRev1-20261126-151358/TASK-WF-designRev1-20261126-151358.md`. The reviewer reported its role self-check passed (AFTER text found in the candidate, BEFORE text in the baseline). The report names no private tooling file, folder or function name.

## Prior blocking findings

| id | status | deciding AFTER lines |
|---|---|---|
| G-01 (archived first plan published) | resolved | PLAN:184 "STOP before any staging ... until the lead's written decision ... is quoted"; "the open item for the lead that the STOP above waits on" |
| G-02 (Task 5 checks conflict or pass with an empty guard file) | resolved | PLAN:85 "no blank line"; PLAN:92 `test -s`, `wc -l`; PLAN:93 neutral phrase for the private read; PLAN:91 `-F` |
| G-03 (no re-pin after a later push) | resolved | PLAN:184 "After the monitor settles, and after any later push ... post a NEW comment"; PLAN:193 |
| G-04 (wrong order; ledger missing from the comment file) | resolved | PLAN:184 "Then the comment file ... followed by the draft ledger", "Only then run the `/sc:pr-submit`"; PLAN:189 |

## New findings

**F1. Blocking (Decision). Introduced by this revision.** Task 13 part one (PLAN:184) orders the steps "a rebase onto `origin/integration` if it has commits the branch lacks, the commit, the push". At that point the tracked files `docs/developer-guide/branch-protection.md` and `tests/docs/test_branch_protection_rulesets.py` are changed but not committed, and part of the change may already be staged. In that state `git rebase` refuses to run, staged or not (unless `rebase.autoStash` is set, which the reviewer could not check). So the rebase that the project's pre-PR check requires (CLAUDE.md pre-PR check 2) cannot run as written whenever it is needed. The affected action is the rebase before the push. Fix: commit first, then fetch, check, rebase, push and record the SHA.

**F2. Blocking (Decision). Found now; older in origin (inherited from baseline PLAN:184 and SPEC:274; the first review recorded this class as Medium G-11).** One of the tag-deleting function names in E-2 is an ordinary English word, and `grep -c -F -f` matches substrings, so that word matches wherever it appears. A masked search (no names printed) showed the word already occurs in `.dev/tasks/to-do/TASK-WF-designRev1-20261126-151358/artifacts/prior-findings.md` (4 lines) and in `return-contract.yaml` and `artifacts/archive-undo.txt` under `.dev/tasks/archive/TASK-WF-designRev1-20261126-141220/` (1 line each). None of these hits is the private file or folder name. Both folders are under `.dev/tasks`, which is always staged, the guard's only exclusion is the first archive folder, and "any hit stops the staging". Result: part one can never reach the commit, push, comment or pull request. Revision 1's M-04 says part one must always run. The affected action is the staging step of part one. Fix: the guard patterns must be strings that cannot occur in ordinary text (the file name, the folder name, each function name in its call form), and the plan must say what follows a hit.

Other checks: `grep -c -F -f` instead of Revision 1's `grep -n -f` is not a defect (`-F` treats the names as fixed strings, `-c` keeps matched private lines out of the session). The `wc -l` check can be done without writing names into a staged file. Task 5 line 91 and Task 14 line 209 can pass. No new private detail reached the candidate plan.

## Follow-up candidates (non-gating)

- F3, Medium: "the number of names E-2 lists" is ambiguous (E-2 also names the private repository, and its second function deletes a release, not a tag), and `wc -l` undercounts a file with no final newline.
- F4, Medium: the STOP gives no path forward if the lead answers "do not publish" the archived folder, although `.dev/tasks` is always staged.
- F5, Note: after a second comment is posted, "the SHA in the posted comment" is ambiguous, and the pull request body pointer is not refreshed.
- F6, Note: "Part one, not R6" departs from M-10's "(R6)"; the departure is needed because of M-04 and SPEC:239.

## Verdict

FAIL. All four prior findings are resolved; two new Blocking findings, F1 and F2.

## Coverage

Read in full: the diff and the candidate. Read in part: spec lines 255 to 298; prior report lines 1 to 267. Read but not quoted: E-2. Also checked: the "Decided" block in `issue-summary.md`, and masked searches over `.dev/tasks`, both package folders and the guide. Not read: the archived first plan, spec lines 1 to 254, prior report lines 268 to 392, git configuration.

## Findings block

```findings-v1
{"id": "F1", "severity": "MAJOR", "blocking": true, "category": "unpassable-check", "anchor": "a rebase onto `origin/integration` if it has commits the branch lacks, the commit, the push", "refs": ["PLAN:184", "CLAUDE.md pre-PR check 2"], "claim": "The rebase comes before the commit while tracked files are changed and possibly staged, so git refuses it whenever a rebase is needed."}
{"id": "F2", "severity": "MAJOR", "blocking": true, "category": "unpassable-check", "anchor": "any hit stops the staging; the only path the guard excludes is the archived superseded plan folder", "refs": ["PLAN:85", "PLAN:184", "SPEC:274", "SPEC:275", "prior G-11"], "claim": "A guard string that is an ordinary English word already matches files in both staged package folders, so part one stops at the guard every time and never commits, pushes or posts."}
{"id": "F3", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "`wc -l` of that file equals the number of names E-2 lists", "refs": ["PLAN:85", "PLAN:92"], "claim": "The expected count is ambiguous and wc -l undercounts a file without a final newline."}
{"id": "F4", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "STOP before any staging: do not stage, commit or push until the lead's written decision on the archived first plan folder", "refs": ["PLAN:184"], "claim": "No path is given if the lead says not to publish the archived folder."}
{"id": "F5", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "run `git diff --exit-code <SHA> -- .github/rulesets/other-repos/ .github/rulesets/protect-release-tags.json", "refs": ["PLAN:184", "PLAN:193"], "claim": "Which posted comment's SHA to use after a second comment is unclear, and the pull request body pointer is not refreshed."}
{"id": "F6", "severity": "MINOR", "blocking": false, "category": "contradiction", "anchor": "Part one, not R6, holds the re-pin step", "refs": ["PLAN:193", "SPEC:284", "SPEC:275"], "claim": "Departs from the (R6) placement in M-10, which is needed because R6 runs only for APPLY rows."}
{"prior": "G-01", "status": "resolved"}
{"prior": "G-02", "status": "resolved"}
{"prior": "G-03", "status": "resolved"}
{"prior": "G-04", "status": "resolved"}
```
