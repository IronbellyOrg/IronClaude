eaeef33bc37a3a9bd2d83de670fca5241008e74e
family lc18-step4-contract-extras: the result file or the AC says a step-4 file shows the contract's worker_status and reason, but the file only holds the generic commands.
command: grep -n -e worker_status -e reason .dev/tasks/to-do/TASK-WF-p1LivePlanBrief-20261105-164506/artifacts/lc18-step4.txt .dev/tasks/to-do/TASK-WF-p1LivePlanBrief-20261105-164506/artifacts/lc18-result.md
before:
.dev/tasks/to-do/TASK-WF-p1LivePlanBrief-20261105-164506/artifacts/lc18-step4.txt:3:$ uv run python -c "import sys, yaml; d = yaml.safe_load(open(sys.argv[1])); assert d['worker_contract_version'] == '1'; assert d['worker_status'] in {'succeeded','partial','failed','blocked'}; assert d['command']; assert d['worker_status'] != 'blocked' or d.get('blocked_question')" .dev/p1-live/watch/return-contract.yaml
.dev/tasks/to-do/TASK-WF-p1LivePlanBrief-20261105-164506/artifacts/lc18-result.md:7:- Step 3: PASS (`lc18-step3.json`: 1 worker_done, outcome `failed` vs contract worker_status `failed`; report path `.dev/p1-live/watch/return-contract.yaml` vs `.dev/p1-live/watch/return-contract.yaml`; acknowledged in `lc18-step3-ack.json`)
.dev/tasks/to-do/TASK-WF-p1LivePlanBrief-20261105-164506/artifacts/lc18-result.md:8:- Step 4: PASS (`lc18-step4.txt`). Extra: PASS. Contract conditions of spec 7.3 AC-1.6: `lc18-step4.txt` shows `worker_status: failed` and `reason` naming `--watch` ("Refused person-mode flag --watch under --unattended: watch mode never ends, so it is refused before any work. No test runner was started."); `worker_done` has `--outcome failed` (`lc18-step3.json`).
coupled sites: .dev/tasks/to-do/TASK-WF-p1LivePlanBrief-20261105-164506/artifacts/lc18-result.md:8 (the sentence that cites lc18-step4.txt)
after:
.dev/tasks/to-do/TASK-WF-p1LivePlanBrief-20261105-164506/artifacts/lc18-step4.txt:3:$ uv run python -c "import sys, yaml; d = yaml.safe_load(open(sys.argv[1])); assert d['worker_contract_version'] == 
.dev/tasks/to-do/TASK-WF-p1LivePlanBrief-20261105-164506/artifacts/lc18-step4.txt:6:2:worker_status: failed
.dev/tasks/to-do/TASK-WF-p1LivePlanBrief-20261105-164506/artifacts/lc18-step4.txt:7:4:reason: "Refused person-mode flag --watch under --unattended: watch mode never ends, so it is refused before any w
.dev/tasks/to-do/TASK-WF-p1LivePlanBrief-20261105-164506/artifacts/lc18-step4.txt:8:worker_status is failed: yes
.dev/tasks/to-do/TASK-WF-p1LivePlanBrief-20261105-164506/artifacts/lc18-step4.txt:9:reason names --watch: yes
.dev/tasks/to-do/TASK-WF-p1LivePlanBrief-20261105-164506/artifacts/lc18-result.md:7:- Step 3: PASS (`lc18-step3.json`: 1 worker_done, outcome `failed` vs contract worker_status `failed`; report path `
.dev/tasks/to-do/TASK-WF-p1LivePlanBrief-20261105-164506/artifacts/lc18-result.md:8:- Step 4: PASS (`lc18-step4.txt`). Extra: PASS. Contract conditions of spec 7.3 AC-1.6: `lc18-step4.txt` shows `work
