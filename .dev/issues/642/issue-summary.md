# Summary: #642 [ob-442 disposable T1] launch-level observation target

- Issue: https://github.com/IronbellyOrg/IronClaude/issues/642
- Type: feature
- Complexity: simple (rubric: installed `refs/claim.md`, effort and complexity section; one area, up to 4 hours)
- Effort estimate: 0.25 hours

## What the issue asks for

Create only `ob-442/T1.txt`, containing the single line `ob-442 T1`. This is a disposable target for the T1 governed-session observations associated with #442, not a change to application behavior or session controls. Touch nothing else and close without merging anything. The estimate covers creating the text file and checking its exact content and one-file scope; it does not include running the wider live-observation suite, and this accuracy check performs neither implementation nor closure.

## Relevant files and systems (cheatsheet)

| Path or system | Why it matters |
|---|---|
| `ob-442/T1.txt` | The only requested new file. No `ob-442/` entries exist in fetched `origin/master` at `3f3b34a26280fd3fd64649f5d010f874b1905b65`; local discovery also finds no target files. |
| `.gitignore` | Checked in the default-branch tree; no target ignore rule was introduced by #640. The local target ignore check also returns no matches. No ignore-file change is requested or needed. |
| `src/superclaude/commands/task.md` and `src/superclaude/skills/sc-task-protocol/SKILL.md` in the default-branch tree | The earlier claim comment names `/sc:task`; both primitives survive the 6.0.0 release. Their presence is not authorization to bypass any governed-session gate. |
| #442 live observations / T1 governed sessions | Stated purpose of the disposable target. #442 remains open; actual observation results are Not known yet. No guard or test changes belong in #642. |
| `src/superclaude/hooks/scripts/launch-level-guard.sh` in the default-branch tree | #640 changes classification of retired commands but retains `task`; relevant observation context, not a requested edit. The older local checkout does not contain this path, so its release version was checked through Git. |
| PRs #640, #646 and #649 | Reviewed for relevance. #640 is on `master`; #646 and #649 merged into `integration` and are not in the checked default-branch tip. None adds, removes or ignores the target, or removes `/sc:task`. |
| Issue completion | Explicit instruction: touch no other implementation file and close without merging anything. This review does not create the target, commit, push, merge or close the issue. |

## Analysis

None: the accuracy check found the issue current, so no analysis ran. The earlier accuracy comment's zero merged-PR count and old baseline have been corrected in [accuracy-check.md](accuracy-check.md); these were stale review metadata, not changes to the requested work. Verification used static Git/tree and file inspection because Codegraph and Augment tools are unavailable in this worker; no live observations or runtime tests were run.
