# OB-CTX evidence note, taken 2026-11-25 (17:30 to 18:20 UTC)

Claude Code 2.1.332. Model for Runs A, B, C: claude-gw-tier2 (the tier 1b default hit the 1.50 USD cap on turn 1). Plan: obs-ctx-plan.md in this folder's parent. Synthetic governed session: a hand-written level file `full` named by a fresh UUID in the real `~/.claude/state/launch-level/sessions/`, no launch marker. Run A, B and C used `claude -p --settings <probe>` in a throwaway git repo `/tmp/ll-obs-ctx.CUUi5pwB/work`; the real guard and the real job-identity hook were active beside the probe.

## Runs and cost (USD, from the stream result line)
| Run | Session id | Result | Cost |
|---|---|---|---|
| A1 | 6f640bdf-... | void: stopped at the 1.50 cap on turn 1 (tier 1b) | 1.58 |
| A2 | d61355c4-... | ran 14 turns; plan flaw found (see below) | 0.78 |
| A3 (corrected, the evidence) | 3b70b88c-4387-4c53-9b3e-9dc279e86cb0 | success, 18 turns | 1.14 |
| B resume | 3b70b88c-... (same) | success | 1.26 |
| C fork | cceb3747-5849-4b20-b35a-dfa933a29f96 (new) | success | 1.31 |
Total about 6.1 USD for 5 sessions. The owner confirmed 3 sessions at 17:26 and then, after the A2 finding, said "yes, proceed with all" for up to 3 more (corrected A, B, C).

## Plan flaw found in A2 (kept as a finding)
The guard's TAMPER class refuses every Bash call that names the launch-job-identity hook ("touching the launch-level state, the Claude Code settings or hooks"). So the selector cannot be asked for its verdict inside a governed call. All three Bash calls of A2 were refused before they ran; SendMessage was refused too. Nothing was bypassed. Fix used in A3: plain commands inside the session. Proof that a call was bound as governed is the rewrite `launch-job-identity.sh execute <session id> ...` in the PostToolUse command. Verdicts for the child processes were read from a separate human shell outside the session (`ob-ctx-human-concurrent.txt`).

## Results (Run A3, session 3b70b88c-...)
- Every Bash call of the main thread, the subagent, the nested subagent and the background agent was rewritten with `execute 3b70b88c-...` (6 PostToolUse lines; main, a03609 subagent, acda25 and acd2bb nested or background). Governed on every supported surface.
- Valid ids, event names and shapes on all 42 lines (checker: Run A alone, violations=0).
- Human shell in the same cwd while the background job was alive: `ordinary`. Background job child (`sleep 61`): `governed` with the run's session id. Both at the same time.
- LIM-2 observed live: a `setsid` child inside a governed Bash call reads `ordinary`.
- LIM-1 observed live: the child of a Monitor-started command reads `ordinary`. Monitor Pre and Post lines carry valid ids (R4).
- Run B (resume, `--resume`): same session id 3b70b88c-...; its Bash call was rewritten with `execute 3b70b88c-...` (governed), as design V14 expects.
- Run C (fork, `--resume --fork-session`): new session id cceb3747-...; its Bash call was not rewritten (ordinary); nothing blocked. As design R4 expects.
- R7: SendMessage PreToolUse seen, no PostToolUse (the guard refused it, as in A2). R8: CronCreate, CronDelete and NotebookEdit all in the tool list; CronCreate and CronDelete ran; NotebookEdit was called and failed on a missing file.
- Tools in the session's tool list but not called: Task, Workflow, TaskStop, ScheduleWakeup (R9, R8 partly). RemoteTrigger and MCP push-class names: not in the list. Recorded as not observed.

## Checker runs
- Run A alone: `OB-CTX-CHECK violations=0`.
- Run A plus the governed lines of the live 842 and 829 sessions (ob-ctx-live-842-governed.jsonl), with `--complete --human-file`: `violations=0` (506 governed lines; P8 rows R6 and R7 for the subagent actor come from the 842 and 829 sessions, not from Run A). A first run reported 3 violations; two were the checker not knowing the label `background job child` (fixed in ob_ctx_check.py, test added not needed) and the third was P8 rows missing from Run A alone.
- Existing coverage of the real claims 827, 829, 841: ob-ctx-existing-coverage.tsv, 0 violations.

## Still not observed
`/clear` (owner skipped, Q6), auto mode, persistent cwd, PID reuse, a killed supervisor (LIM-3, covered by the existing real-process test `test_real_git_killed_supervisor_is_unknown_not_proven_human`), Task, Workflow, RemoteTrigger and MCP push-class tools, concurrent-hook composition beyond the three hooks that ran together.

## Rollback done
The synthetic level file `3b70b88c-...` and its `.ok` were removed from `~/.claude/state/launch-level/sessions/`, the two earlier session files were removed after their runs, the jobs folder is empty, and no other file in the real store was touched. Raw logs stay in `/tmp/ll-obs-ctx.CUUi5pwB/logs/`. Claude's own transcripts of the three runs stay in `~/.claude/projects/` under the directory named after `/tmp/ll-obs-ctx.CUUi5pwB/work`.
