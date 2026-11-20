# T1 reflection card (UC-1, pre-execution)

- Spec: `.dev/tasks/to-do/TASK-WF-scriptThe442Obse-20261108-061618/source.md` (1 line)
- Tasklist: `.dev/tasks/to-do/TASK-WF-scriptThe442Obse-20261108-061618/TASK-WF-scriptThe442Obse-20261108-061618.md` (266 lines, 6 phases, 11 tasks)
- Card author: inline orchestrator

## Coverage section

- Pass 1: 0 parsed IDs. Pass 2: 6 quote-pinned rows INF-001 to INF-006 (`artifacts/inferred-requirements.json`), all citing source.md:1.
- All 6 covered (`artifacts/coverage-matrix.json`): setup by Tasks 1, 2, 5 (plan:31-55, plan:107-128); driver by Tasks 3, 4, 6 (plan:59-82); evidence by Task 7 (plan:166-191); cleanup by Tasks 8, 11 (plan:195-215, plan:255-266); authorization by Constraints (plan:19) and Task 10 (plan:236-253); orchestration investigated and rejected with reasons (plan:25).
- `coverage_pct: null` (parsed-only, 0 parsed), `coverage_pct_union: 1.0`, `S_dev_density: 0.0`, `coverage_degraded: parsed-sparse` (Tier-1 stop forbidden).

## Deviation / risk section

- T1-F1 (gap): Task 11 requires the store diff `ls -A ~/.claude/state/launch-level/sessions | diff /tmp/ob/baseline-sessions.txt -` to run before step 7 deletes `/tmp/ob` (plan:263), but Task 8 does not build that check into `cleanup.sh` (plan:199-210) and `--apply` runs every step in one call (plan:201), so the operator has no point to run it in between.
- T1-F2 (authorization ambiguity): Task 5 creates four GitHub issues (plan:114) and session `e` opens a pull request and writes repository contents with `gh api -X PUT` (plan:148-149). The authorization line (plan:19) names "governed claims on the four disposable issues"; it does not say in words that the agent may create the issues and the pull request. Creation is implied by the source (source.md:1) but is outward-facing.
- T1-F3 (risk, acknowledged): Task 10 lets the agent answer tool permission dialogs "only for a command the runbook prompt itself asked for" (plan:243). That is a judgement step and the R15 risk the plan names (plan:24).
- T1-F4 (unstated source): session `b` restores `$WT_T1/.claude/settings.local.json` from `/tmp/ob/t1-local.json` (plan:137), but no task says which step writes that backup.
- T1-F5 (minor): Task 11 stages `./artifacts/ob-logs/` (plan:185, plan:259), which holds full screen captures; the secret scan covers four token patterns only.
- Honest UNVERIFIED labels: governed handle field (plan:138), O-10 web-edit equivalence (plan:149).

## Structural section

- 6 phases, 11 tasks numbered 1 to 11; every `Depends on` names a lower task; acceptance criteria present on every task.
- Line-number extraction: prompts (lines 228-697) and setup blocks (43-169) sit before the Task 9 edit at runbook:764, so the edit does not shift them.

## Self-reported confidence

0.80 (not used by the rubric).
