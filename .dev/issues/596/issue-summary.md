# Summary: #596 [ob-442 disposable T4] launch-level observation target

- Issue: https://github.com/IronbellyOrg/IronClaude/issues/596
- Type: feature
- Complexity: simple (rubric: `refs/claim.md`; one area, under 4 hours, no security implementation or data migration)
- Effort estimate: 0.25 hours

## What the issue asks for

Create only `ob-442/T4.txt`, containing exactly one line: `ob-442 T4`. This is a disposable target for the T4 governed-session observation associated with #442, not a change to the launch-level guard. Touch no other implementation files and close the disposable issue without merging anything. The estimate covers creating and checking the one-line file, not running the broader #442 observation campaign; the live session's status and duration are Not known yet.

## Relevant files and systems (cheatsheet)

| Path or system | Why it matters |
|---|---|
| `/home/coder/workspaces/IronClaude/ob-442/T4.txt` | The only requested implementation file; absent from the checked checkout and origin/master at 3206bdb9cb6b0fe3c81e6cdbeadcc1455aeeffda. Contents must be the single line `ob-442 T4`. In a separately launched worktree, use the equivalent path under that worktree's root. |
| https://github.com/IronbellyOrg/IronClaude/issues/442 | Parent live-observation context. This disposable fixture does not itself prove any observation passed. |
| Governed launch-level session T4 | Intended user of the disposable target. No guard, approval logic, test-suite or configuration changes are requested. |
| https://github.com/IronbellyOrg/IronClaude/pull/592 | Only merge after #596's exact creation time; changes the observer and its documentation/tests, not this target. |
| `/home/coder/workspaces/IronClaude/.dev/issues/596/accuracy-check.md` | Evidence and relevance checks for all 12 scout-listed PRs. Verdict: current. |

## Analysis

None: the accuracy check found the issue current, so no analysis ran.
