# L2 pre-push refusal observation (scratch run), 2026-11-26

Worker for COORD-IronClaude, owner approval 2026-11-26. Sonnet-class model. Nothing was pushed to, fetched into or written on any GitHub repository by the tests; the only remote was a local bare repository.

## What was run
- Scratch: `/tmp/l2-refusal-test` with `work/` (repo), `remote.git/` (local bare remote, the only remote), `home/` (a scratch HOME so the real `~/.claude` was not touched). `IR7_REFUSE` was not changed (still False, `orca_worktree.py` line 859); every run printed `IR7_REFUSE = False`.
- Install: the real `install_l2(wt)` from `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py`, with HOME set to the scratch HOME. It took the packaged hook `launch-level-pre-push.sh` (version 2, three protected refs) and `launch-job-identity.sh` from `src/superclaude/hooks/scripts/` and returned `('installed', '')`. `l2_status(wt)` before: `('absent', 'no pre-push hook')`; after: `('owned', '')`.
- Governed actor: a launch record `sessions/l2test-governed-1` holding `worktree` in the scratch store. Each push was wrapped by the real identity hook (`launch-job-identity.sh hook`, the same rewrite the guard makes for a governed Bash call) and run as `git push origin <ref>` in `work/`. Scripts: `ob-l2-run-case.sh`, `ob-l2-install-l2.py`, `ob-l2-healthy.py`. Raw outputs: `ob-l2-cases-T1-T3.txt`, `ob-l2-cases-T4-H1.txt`.

## Results
| Case | What | Exact refusal or result | Exit | Result |
|---|---|---|---|---|
| T1 | governed, push `master` | `launch-level pre-push: L2-PROTECTED: a governed launch session may not push to refs/heads/master; the whole push was refused. A person releases the session as the claim's launch result describes.` then `error: failed to push some refs to '/tmp/l2-refusal-test/remote.git'` | 1 | PASS (refused, remote has no refs) |
| T2 | governed, push `integration` | same text with `refs/heads/integration` | 1 | PASS (refused, remote has no refs) |
| T3 | governed, push feature branch `feat-l2` (control, must be allowed) | `* [new branch] feat-l2 -> feat-l2` | 0 | PASS (allowed; remote got only `feat-l2`) |
| T4 | data file tampered (`chmod 666 pre-push.launch-level`), governed record kept, push `master` | `launch-level pre-push: L2-UNKNOWN: could not classify this push (no valid data file) and it targets refs/heads/master; the whole push was refused, and pushes to other refs are allowed.` plus the line `to push there, a person fixes the cause (...)`. Real `l2_status` on the tampered setup: `('conflict', 'data-file-differs: remove both files with rm ... and claim again; the claim never deletes them')` | 1 | PASS (fails closed; remote unchanged) |
| H1 | healthy claim: `install_l2` then `l2_status` | `('owned', '')`, `l2_notes = []`, refused at the L2 gate: False, so the launch goes on to the pending record and the agent launch | n/a | PASS |
| H1b | after restoring the data file (chmod 644), governed push `master` | same L2-PROTECTED text | 1 | PASS |

H1 runs the two real calls of the launch (lines 1797-1798) and copies the one-line note test of lines 1799-1800; it does not run the whole `cmd_launch`, which needs Orca and GitHub.

## Findings to know
1. Version gap on this machine: `~/.claude/hooks/launch-level-pre-push.sh` is version 1 (protects only `main` and `master`); the repo's packaged hook is version 2 (adds `integration`). The observation used the version 2 file from the repo. A real claim today installs version 1 until `superclaude install` is re-run, so T2 would not refuse there.
2. Disagreement between files: `.dev/issues/442/handoff-runbook.md` ("Not built, so the runbook cannot observe it: the L2 pre-push layer") and `.dev/issues/442/observation-results.md` (E protected push pending) predate PR 851; the 2026-11-25 evidence (`ob-h2-real-claim-827-notes.md`: "L2 owned" on a real claim; `ob-h3-FS-notes.md`: L2's own refusal never reached) shows L2 installed, and this run is the first sight of its refusal text.
3. L2 only sees pushes that reach git; on real sessions the L1 guard refuses push forms first (as the 2026-11-25 notes record).

## NOT done (not run, on purpose)
Auto mode; `/clear`; persistent working directory; PID reuse; the Task, Workflow, RemoteTrigger and MCP push-class tools; a real merge conflict through pr-submit. Also not done: a real claim on a real issue, a governed push from a live Claude session, and the whole `cmd_launch`.

## Recommendation
This evidence shows L2 installs, reads as `owned`, refuses governed pushes to master and integration, fails closed on a tampered data file, allows feature branches and does not block a healthy launch, so it supports turning `IR7_REFUSE` on for the L2 part, but only after the installed hook is updated to version 2 and with the not-done items above still open; the owner decides in chat.
