start=1e33f422dadf9034876adec8c03894ab6ccfca76 tree=eb8eee348a680d29fc2280eaf40b6850529f164b
**Earlier findings**
- F3.1 resolved. The child argv now carries `--output <abs>` and an absolute snapshot path (`src/superclaude/cli/swarm/commands.py:1297-1306`). That makes `output_dir` non-None in `run_preflight`, so the manifest is written (`preflight.py:1871-1873`). The state output root is then set (`commands.py:1846-1850`). The post-fix runs in `artifacts/completion-compatibility.txt:66-77` show 121 and 123 passed. The live check in `artifacts/detached-check.txt:31-80` shows `done.json`, `return-contract.yaml` and `.swarm-state.json` all present, with `terminal_status` and `contract_status` both "success" and state "terminal".

**AC marks**
- T3.AC1 met. `tests/swarm/test_tmux_detached.py:~71-131` (the added test block):
  - It intercepts `swarm_tmux.launch_detached`, asserts no `done.json` before and after the parent runs, and reads the policy flag from the snapshot.
  - It then runs the captured `requests[0][5:]` through the real `run_cmd`. The slice is correct: indices 5-7 are `--output`, the output path and the snapshot (`commands.py:1297-1305`).
  - It asserts `done.json` exists exactly when the policy is enabled. When enabled, it also asserts `terminal_status` equals the contract's status, `contract_path` matches, and state is "terminal".
  - Both enabled and disabled variants run, each with a relative and an absolute `--output`.
- T3.AC2 met. `tests/swarm/test_tmux_detached.py:~134-193` (the live test):
  - It uses `uv run`, captures output, and waits on a fixed 10-second deadline.
  - It validates the marker, contract status "success" and terminal state, and it kills only its own session.
  - It is gated by `requires_tmux` and `NOT_NESTED`.
  - `artifacts/detached-check.txt:31-80` records the command, the tmux and nesting capability (`tmux_available: true`, `nested: false`), stdout, stderr, the artifact list and the PASS result.
  - The first run is kept as a FAIL record at lines 1-30.
- T3.AC3 met. `artifacts/completion-compatibility.txt:40-77` records the exact command, the two failing runs, and the final 123 passed with 2 skipped. The skips are listed only as a count, with no test names.
- T3.AC4 met. The only production change is the argv in `_launch_detached_run` (`commands.py:1297-1306`). `_emit_killed_done_sentinel`, `kill_cmd` and `reflect/ensemble.py` are not in the diff. The launcher still only stages the snapshot and calls `launch_detached`. The `--output` change was authorized by the user's 2026-11-23T20:53:20Z instruction, which the task quotes.

**Findings (non-blocking)**
F3.2 ac=T3.AC2 at=artifacts/detached-check.txt:41 anchor="Save command, environment capability (without secret values), stdout/stderr, observed artifacts and result under `./artifacts/detached-cli/`" chk=n,n,n,n family=evidence-location fix=Note the `detached-cli-launcher-fix/` location, or copy the passing evidence under `detached-cli/`: Note. The passing live evidence is under `artifacts/detached-cli-launcher-fix/`, while `detached-cli/` holds only the earlier failing run. `detached-check.txt` names both paths, so the evidence is findable.

F3.3 ac=scope at=artifacts/detached-cli-launcher-fix/home/.cache/uv/CACHEDIR.TAG anchor=path chk=n,n,n,n family=artifact-hygiene fix=Optionally prune the uv cache from the isolated HOME: Note. The isolated HOME contains a uv cache that is staged with the package. It holds no secrets and is in the declared artifacts folder.

F3.1 resolved

Parent: paperwork-only rejection. AC1/AC2 use approximate diff-relative line ranges (~71-131 and ~134-193), not valid current file:line citations. Per qa.md one fresh reviewer is respawned with exactly the same saved input. This does not fail the task or reopen the ladder. The first response is preserved verbatim above; no finding severity or compliant verdict is derived from this invalid review.

## Fresh paperwork respawn, verbatim response

**Earlier finding**
F3.1 resolved. The child argv now carries `--output <resolved output dir>` before the resolved snapshot path (`src/superclaude/cli/swarm/commands.py:1303-1305`). The child's output override is applied at `commands.py:1742`. The latest `detached-check.txt` run shows `.swarm-state.json`, `return-contract.yaml` and `done.json` created under `detached-cli/verified/out`.

**Acceptance criteria**
- T3.AC1 met. Evidence: `tests/swarm/test_tmux_detached.py:296-300` (the stubbed `launch_detached` asserts no `done.json` at launch), `:303` (no marker after the parent exits), `:308-313` (the snapshot keeps `write_done_sentinel`), `:315-316` (the captured child argv is run through `run_cmd`), and `:317-326` (marker present only when enabled, status and contract path match, state is terminal). The `.swarm-state.json` terminal state is asserted twice: unconditionally at `:319` and again inside the enabled branch at `:129-131`. Production order is the terminal-state write at `commands.py:2168`, then the marker at `commands.py:2183`.
- T3.AC2 met. Evidence: the live test at `tests/swarm/test_tmux_detached.py:338-393` launches through `uv run ... superclaude swarm run --detached`. It captures stdout and stderr, waits to a fixed 10-second deadline that breaks early if the session dies, then validates the marker, contract status and terminal state. It cleans up only its own session. The saved record is `artifacts/detached-check.txt:1-130`: the command, `tmux_available`, `nested` and stdout/stderr are present, with no secrets. Observed artifacts are listed in the file (`:102-117`) and stored under `artifacts/detached-cli/verified/out/`. Record 1 shows the earlier FAIL and records 2 and 3 show PASS (`:79`, `:129`). Record 2 points at `detached-cli-launcher-fix/`, which does not exist under `artifacts/` (it was not in the artifacts listing). That is a label and retention Note only, because record 3 carries the same PASS evidence under `detached-cli/verified/`.
- T3.AC3 met. `artifacts/completion-compatibility.txt:1-77` holds four runs with the exact module list and the failures kept. The final run ends `123 passed, 2 skipped, EXIT: 0` (`:75-77`). The skips come from the existing tmux-absent and nested-tmux guards at `tests/swarm/test_tmux_detached.py:112` and `:125`. The reasons are not itemised because `-rs` was not used. That is a Note, because the AC asks only that skips be included.
- T3.AC4 met. `_launch_detached_run` only stages the snapshot and launches (`commands.py:1278-1338`) and writes no marker. `_emit_killed_done_sentinel` (`commands.py:3543`) and its caller (`:3712`) are untouched by the diff. The diff touches no reflect or ensemble file.

**Findings (non-blocking)**
- F3.2 ac=T3.AC3 at=artifacts/completion-compatibility.txt:75 anchor="save results including skips" chk=n,n,n,n family=skip-reasons fix=optional rerun with `-rs` to list skip reasons: Note, skip reasons not itemised.
- F3.3 ac=T3.AC2 at=artifacts/detached-check.txt:41 anchor="Save ... under `./artifacts/detached-cli/`" chk=n,n,n,n family=artifact-path fix=optional, move or relabel the `detached-cli-launcher-fix/` record: Note, record 2 cites a path outside `detached-cli/`, and the PASS evidence is duplicated in the compliant record 3.

F3.1 resolved

Parent: all four AC have valid current file:line citations and no unmet mark or checklist yes. Reviewed findings F3.2/F3.3 derive note (cosmetic, all no); retain both in notes.md. Read-back corrects reviewer pointer drift without changing the verified claims: parent absence is test:308, snapshot policy :313-318, child execution :319-324, enabled marker comparisons :328-335, live terminal assertion :393-395. Later appended log :83-85 itemises the two capability-branch skip reasons; neither is the live completion check. Glob confirmed detached-cli-launcher-fix/out/done.json exists, contrary to the reviewer's incidental listing claim; the required nested verified capture also exists. F3.1 is resolved in the current end state. Verdict: compliant. No acceptance of a gap and no Ruling.
