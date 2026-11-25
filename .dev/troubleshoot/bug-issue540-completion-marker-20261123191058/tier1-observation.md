# Tier 1 observation

## Reported symptom
Issue 540 (read via gh issue view --repo IronbellyOrg/IronClaude) reports a stub foreground run exits 0, writes success/terminal artifacts, but omits done.json. Historical remote observations are not treated as fresh runtime proof.

## Source grounding
The writer is defined at src/superclaude/cli/swarm/reduce.py:383-440. The normal CLI reduces at commands.py:2145 then sets terminal at :2165-2169; the resume branch reduces at :2578 and sets terminal at :2591. Neither calls the writer. Detached launches the same CLI without --detached at :1297-1304. Source-wide Python search found one production caller, reflect/ensemble.py:421, read and verified. Helper-only tests are in tests/swarm/test_done_sentinel.py:47-101.

## Captured local output
Run: local-foreground-1; arm: failing; environment: current worktree, dedicated artifacts/home; transport: stub. CLI executable resolved by uv run --no-sync which superclaude to this worktree's .venv/bin/superclaude. Independent import-location check `uv run --no-sync python -I -c 'import superclaude.cli.swarm.commands as c; import superclaude.cli.swarm.reduce as r; print(c.__file__); print(r.__file__)'` printed this worktree's src/superclaude/cli/swarm/commands.py and reduce.py, not another checkout or installed wheel.
Command: uv run --no-sync env HOME=<this run>/artifacts/home superclaude swarm run --lens bare-review --transport stub --target <this run>/artifacts/target.txt --output <this run>/artifacts/foreground
Observed exit: 0
Observed stdout:
```text
swarm run: dispatched job (mode=lens, workers=3, results=3)
```
Captured artifacts: artifacts/foreground/return-contract.yaml:2 status=success; :19-20 workers_requested=3, workers_succeeded=3; artifacts/foreground/.swarm-state.json:3 state=terminal.
Read-only filesystem inspection command: uv run --no-sync python -I -c 'import json; from pathlib import Path; p=Path(".dev/troubleshoot/bug-issue540-completion-marker-20261123191058/artifacts/foreground"); print(json.dumps({"done_exists":(p/"done.json").exists(),"state":json.loads((p/".swarm-state.json").read_text())["state"]}))'
Observed stdout:
```json
{"done_exists": false, "state": "terminal"}
```
A direct Read of artifacts/foreground/done.json failed with File does not exist; Glob of that output directory likewise showed no marker. A prior silent test -f result was ambiguous in the tool display and was not used alone as evidence.

## Captured resume output
Run: local-resume-1; arm: failing; same dedicated HOME; separate artifacts/resume output, preserving original foreground evidence. Created a second stub bare-review job with the same target and a new output path. Job id read from its .swarm-state.json before resume: lens-bare-review-0a1cf709.
Command: uv run --no-sync env HOME=<this run>/artifacts/home superclaude swarm run --resume lens-bare-review-0a1cf709 --transport stub --output <this run>/artifacts/resume
Observed exit: 0
Observed stdout:
```text
swarm run --resume: job_id=lens-bare-review-0a1cf709 workers=3 skipped=3 redispatched=0
```
Read-only filesystem inspection (same Path.exists/json-state command with artifacts/resume):
```json
{"done_exists": false, "state": "terminal"}
```
Captured contract artifacts/resume/return-contract.yaml:2 status=success; :19-20 requested=3 succeeded=3. This verifies successful resume with all workers already successful, not redispatch/failure completion or detached tmux execution. Detached remains source-only inspection.

## Effective policy and negative search evidence
The fresh lens shortcut explicitly sets runtime.on_completion.write_done_sentinel=True at src/superclaude/cli/swarm/commands.py:931-937, before JobSpec construction at :1929. A content search for runtime/on_completion/write_done_sentinel in the captured foreground manifest returned no matches; the manifest is not claimed to preserve that flag. preflight.resume_mode:1902-1919 documents incomplete rehydration and :1965-1976 constructs a JobSpec without an explicit runtime policy, so defaults apply on the inspected path. Preservation of arbitrary original runtime overrides on resume is not reproduced here and is not silently added to this issue's repair scope. A guessed source read at preflight.py:1470-1481 located manifest emission, not resume policy; the subsequent definition search located resume_mode at :1888 and the actual body was read.

## Behaviour definitions
Pending only if a hypothesis asserts unobserved external/runtime primitive behavior. Current evidence uses live project function bodies and directly observed filesystem results, not assumed provider semantics.
