# sc:reflect UC-1 report: Phase 2 codegraph plan

```yaml
contract_version: 1.8.0
status: partial
mode: pre
tier_reached: 2
confidence_calibrated: 0.71
citations_total: 193
citations_revalidated: 189
citations_dropped: 0
citations_inferred: 0
citation_budget_policy: sampled
coverage_degraded: parsed-sparse
```

Plan: `.dev/tasks/to-do/TASK-WF-phase2CodegraphI-20261029-192001/TASK-WF-phase2CodegraphI-20261029-192001.md` ("plan:"). Spec: `source.md` in the same package ("source.md:"). Merge: `adversarial/merged-verdict.yaml` (method adversarial, convergence 1.0, BLOCKED_BY_INVARIANTS; INV-001 and INV-006 applied as corrections in M-02 and M-18, not re-debated). Coverage: Pass 1 0 ids, Pass 2 104 rows, containment 64/104 (0.6154), manual triage leaves 0 real gaps (`artifacts/unmapped-triage.yaml`); spans §2.1-§2.11, §3.1, §3.3-§3.4 and §4.2 have no matrix rows and rest on the by-reference triage (M-16).

Status `partial`: the evidence gate dropped 0 of 189 re-read citations (zero-drop flag recorded, §11.2), but the adversarial merge reports BLOCKED_BY_INVARIANTS: INV-001 and INV-006 were applied as corrections (M-02, M-18) without a further debate round.

> **Citation budget: sampled mode**
> - `citations_revalidated: 189` of 193.
> - `citations_dropped: 0` (sample count).
> - `citations_dropped_extrapolated: 0`.
> The extrapolated value is telemetry, not a verdict. The sample-count is what the validator actually examined; the extrapolation is what it would have found if the budget had permitted a full re-Read.

## Deviations

### Deviation D-M-01: The guard implements the §7 hard rule (source.md:755, plan:23) but is not in the spec's T0 acceptance (source.

- **Location:** plan:48; plan:21
- **Spec section:** source.md:436; source.md:440-442; source.md:445; source.md:755
- **Classification:** authorized (origin: plan; severity: important)
- **Sources:** R1-01, P2R2-7 (Task 1 part), X-001, A-001, INV-019
- **Evidence / claim:** - The guard implements the §7 hard rule (source.md:755, plan:23) but is not in the spec's T0 acceptance (source.md:440-442). - As written, `git diff --name-only HEAD~1 HEAD | rg '^\.claude/' | rg -v '^\.claude/settings\.json$'` exits 1 under pipefail on a clean commit and on a settings.json-only commit, and exits 0 when it prints a violation (orchestrator run). It contradicts plan:21. - The `test -z "$(pipeline)"` repair in R1-01 passes vacuously when `HEAD~1` cannot resolve (Round 2, both advocates).
- **Default remediation:** One fenced block, both lines in the same shell: git diff --name-only HEAD~1 HEAD > /tmp/p2-t1-files.txt if rg '^\.claude/' /tmp/p2-t1-files.txt | rg -v '^\.claude/settings\.json$'; then exit 1; fi

### Deviation D-M-02: The user-scope (plan:277) and local-scope (plan:278) `jq -e` lines open the exit-0 block, which is copied from

- **Location:** plan:275-286 (plan:277, 278, 286); plan:27
- **Spec section:** source.md:197; source.md:209-211; source.md:705; source.md:709-716; source.md:757-765
- **Classification:** necessary (origin: inherited-from-spec; severity: important)
- **Sources:** R1-02, P2R2-1, advocate A Round 1 concession 10, advocate A Round 2 New evidence 2, advocate B Round 2 item 7, INV-001, INV-002, INV-003, INV-004, INV-005
- **Evidence / claim:** - The user-scope (plan:277) and local-scope (plan:278) `jq -e` lines open the exit-0 block, which is copied from source.md:709-716. A hit aborts lines 279-284, so the registration, version, `mcp get`, `--list` and doctor outputs that the G6 comment needs are lost. - A local-scope hit is a user action, not a plan failure (plan:286, source.md:211). - A user-scope failure from a kept entry keeps T12 open until the user acts (source.md:210, 705). But no human item covers it (plan:27, source.md:757-765), and the executor cannot see the retire step's printed commands, which were shown in the human's `./update.sh` terminal.
- **Default remediation:** (a) Run each scope check as a recorded line: `rc=0; jq -e '<filter>' ~/.claude.json || rc=$?`, then save rc to `/tmp/p2-t16-us.rc` (user) or `/tmp/p2-t16-ls.rc` (local), then `test "$rc" -le 1`. rc 1 means a hit. A missing or corrupt file (rc 2 or 5) still fails. (b) Add read-only `jq` lines that print `claude mcp remove <key> --scope user` for each offending user-scope key, and `cd <project-key> && claude mcp remove <name> --scope local` for each local hit. Put these in the G6 comment. (c) End the block with `test "$(cat /tmp/p2-t16-us.rc)" -eq 0`. User scope stays gating; local scope stays report-only. (d) Add a seventh, non-blocking human item: the user runs the printed user-scope command. Task 16 stays open and is reported in G6.

### Deviation D-M-03: plan:107 uses `$E`, which only source.md:534 defines. The plan dropped the definition, and under `set -u` the 

- **Location:** plan:107
- **Spec section:** source.md:533-534; source.md:540
- **Classification:** drift (origin: plan; severity: minor)
- **Sources:** R1-03, P2R2-2, X-002, INV-023
- **Evidence / claim:** plan:107 uses `$E`, which only source.md:534 defines. The plan dropped the definition, and under `set -u` the line aborts on an unbound variable.
- **Default remediation:** One fenced block: MT=$(sed -n 's/^Selected MCP_TOOLS: //p' .dev/codegraph-migration/evidence/P2-mcp-tools-schema.md); test -n "$MT" E=$(jq -cn --arg t "$MT" …)   # exactly as source.md:534 jq -e --argjson e "$E" '. == $e' .dev/codegraph-migration/evidence/P2-add-json-shape.json

### Deviation D-M-04: Blocks run from the repo root, so `./artifacts/...` resolves to the project-root `artifacts/` instead of the p

- **Location:** plan:79, 85, 237, 253, 272, 287; plan:24
- **Spec section:** none (the spec has no ./artifacts paths); user rule: the project-root artifacts/ is never staged
- **Classification:** drift (origin: plan; severity: important (minor for the prose-only refs at plan:79 and plan:237))
- **Sources:** R1-04 (path part), P2R2-4, C-004, X-003, INV-008, INV-009
- **Evidence / claim:** - Blocks run from the repo root, so `./artifacts/...` resolves to the project-root `artifacts/` instead of the package's `artifacts/` that plan:24 stages. - The package folder has no `artifacts/` directory yet (verified), so a copy into it fails under `-e`. - Task 3's client runs from `$W/repo`, which is deleted (source.md:527), so relative outputs are lost.
- **Default remediation:** - Use the literal path `.dev/tasks/to-do/TASK-WF-phase2CodegraphI-20261029-192001/artifacts/<file>` in each block, not a Constraints `$ART`, which is unbound in separate blocks. - `mkdir -p` that directory in Task 3 and Task 14. - Task 3 captures the absolute worktree root before entering `$W` and writes `t3-run1.json` and `t3-run2.json` there before `rm -rf "$W"`.

### Deviation D-M-05: The block writes only `/tmp`, but plan:253 requires `t14-final-run.txt` and `t14-new-failures.txt` under artif

- **Location:** plan:237; plan:242-253; plan:259
- **Spec section:** source.md:669-684
- **Classification:** drift (origin: plan; severity: important)
- **Sources:** R1-04 (Task 14 part), X-004, INV-007, INV-010
- **Evidence / claim:** - The block writes only `/tmp`, but plan:253 requires `t14-final-run.txt` and `t14-new-failures.txt` under artifacts. - Copy lines added after plan:247 never run when the gate fails. A failing plan:247 also skips the plan:248 `perf.json` restore. - Task 14 commits only when a fix was needed, so its staged evidence blocks Task 15's `rebase onto origin/master`.
- **Default remediation:** - Copy `/tmp/p2-final-run.txt` right after plan:243, and `/tmp/p2-new-failures.txt` right after plan:246, into the package artifacts path. - Move the `perf.json` restore ahead of `test ! -s`. - Always commit the Task 14 evidence (for example `test(codegraph): record final gate evidence`).

### Deviation D-M-06: The before/after hash criterion is backed by the §7 hard rule and the Leg B H0/H1 guard, but no step records a

- **Location:** plan:86; plan:73-77; plan:23
- **Spec section:** source.md:522; source.md:525; source.md:755
- **Classification:** authorized (origin: plan; severity: minor)
- **Sources:** R1-04 (hash part), P2R2-3, C-002, INV-012, INV-013
- **Evidence / claim:** - The before/after hash criterion is backed by the §7 hard rule and the Leg B H0/H1 guard, but no step records a before-hash outside Leg B, so the criterion is unverifiable. - Task 3 runs as several shell invocations, so a shell variable H0 does not survive to the end. - Leg A uses a sandbox HOME, so the real risk is near zero.
- **Default remediation:** - First action: `jq -S '.mcpServers' ~/.claude.json | sha256sum > /tmp/p2-t3-h0.txt`. - Last line: `test "$(jq -S '.mcpServers' ~/.claude.json | sha256sum)" = "$(cat /tmp/p2-t3-h0.txt)"`.

### Deviation D-M-07: Task 16 writes `./artifacts/t16-live-verify.txt`, although T12 is "Files: none in the repository; the outputs 

- **Location:** plan:272; plan:287; plan:24
- **Spec section:** source.md:706; source.md:719
- **Classification:** drift (origin: plan; severity: minor)
- **Sources:** P2R2-7 (calibrator note), A-003 (CONTRADICTED), advocate A A-003 comment, advocate B A-003 comment, INV-022
- **Evidence / claim:** Task 16 writes `./artifacts/t16-live-verify.txt`, although T12 is "Files: none in the repository; the outputs go only into the issue-#323 comment". After the merge there is no commit point, so the file would stay untracked, against the always-staged rule.
- **Default remediation:** Write to `/tmp/p2-t16-live-verify.txt`. Paste it, with the M-02 markers, into the G6 comment. Drop the file clause from plan:272 and plan:287.

### Deviation D-M-08: U11 tests the `claude --version` check that source.md:101 places in the phase function Task 5 creates (`instal

- **Location:** plan:92; plan:96; plan:104
- **Spec section:** source.md:101; source.md:296; source.md:466; source.md:486
- **Classification:** necessary (origin: inherited-from-spec; severity: important)
- **Sources:** R1-05, INV-016
- **Evidence / claim:** U11 tests the `claude --version` check that source.md:101 places in the phase function Task 5 creates (`install_mcp.py`). Yet Task 4's gate must pass U1-U11 (copied from source.md:466).
- **Default remediation:** - Move U11 to Task 5: the plan:92 list, the plan:96 gate ("U1-U10, U20-U22, U24") and plan:104 ("U11-U19, U23, U25"). - Check whether U22 (source.md:307, "the version dir's launcher is registered") also needs Task 5. UNVERIFIED.

### Deviation D-M-09: Under `bash -euo pipefail`, errexit ignores a failing left side of `&&` and any `! cmd` (orchestrator run). Th

- **Location:** plan:162, 163, 165, 202, 203, 244
- **Spec section:** source.md:601, 602, 604, 636, 637, 675; source.md:625
- **Classification:** necessary (origin: inherited-from-spec; severity: important)
- **Sources:** R1-07, INV-015, INV-020, orchestrator run
- **Evidence / claim:** Under `bash -euo pipefail`, errexit ignores a failing left side of `&&` and any `! cmd` (orchestrator run). These checks therefore do not fail the block mid-way. source.md:625 knows this rule but applies it only to T6.
- **Default remediation:** One condition per line. Write negatives as `if cmd; then exit 1; fi`. Keep the positive grep before its negative.

### Deviation D-M-10: pyyaml is a project dependency (pyproject.toml). The probe found that `--no-project` still works in this check

- **Location:** plan:216
- **Spec section:** source.md:649-651
- **Classification:** necessary (origin: inherited-from-spec; severity: minor)
- **Sources:** R1-08, INV-014
- **Evidence / claim:** pyyaml is a project dependency (pyproject.toml). The probe found that `--no-project` still works in this checkout because uv finds `.venv`, so it fails only where no `.venv` exists.
- **Default remediation:** Optional: make `uv run python -c …` the primary command.

### Deviation D-M-11: `grep -i connected` also matches Disconnected / Not connected; no negative check as in layer 2 step 5.

- **Location:** plan:282
- **Spec section:** source.md:714; source.md:374-375
- **Classification:** necessary (origin: inherited-from-spec; severity: minor)
- **Sources:** R1-09, INV-024
- **Evidence / claim:** `grep -i connected` also matches Disconnected / Not connected; no negative check as in layer 2 step 5.
- **Default remediation:** After the positive grep, add `if grep -iE 'disconnected|not connected|failed' /tmp/p2-t12-get.txt; then exit 1; fi`, as in layer 2 step 5.

### Deviation D-M-12: Spec T0b requires the outcome to be reported to the coordinator in the completion message; Task 2 drops it.

- **Location:** plan:54
- **Spec section:** source.md:448
- **Classification:** drift (origin: plan; severity: minor)
- **Sources:** R1-10
- **Evidence / claim:** Spec T0b requires the outcome to be reported to the coordinator in the completion message; Task 2 drops it.
- **Default remediation:** The Task 2 completion message states whether Phase 1 already carried the amendments or this task made them.

### Deviation D-M-13: The §2.8 block includes the "Ready for Serena retirement" line, which needs `codegraph_ready()` from Task 7. T

- **Location:** plan:120; plan:125; plan:131
- **Spec section:** source.md:142; source.md:561-563; source.md:573
- **Classification:** necessary (origin: inherited-from-spec; severity: minor)
- **Sources:** R1-06 (calibrator: overstated)
- **Evidence / claim:** The §2.8 block includes the "Ready for Serena retirement" line, which needs `codegraph_ready()` from Task 7. Task 6's acceptance does not check that line, so this is an ordering ambiguity only.
- **Default remediation:** Task 6 states that the Ready line lands in Task 7, and Task 7's acceptance checks it.

### Deviation D-M-14: The §4.2 Notes fallback for `claude mcp get` is included only through plan:19 and plan:223.

- **Location:** plan:223-227
- **Spec section:** source.md:416
- **Classification:** drift (origin: plan; severity: minor)
- **Sources:** R1-11 (calibrator: overstated)
- **Evidence / claim:** The §4.2 Notes fallback for `claude mcp get` is included only through plan:19 and plan:223.
- **Default remediation:** One sentence naming the fallback (stdio `initialize` + `tools/list`, `serverInfo.name == codegraph`), recorded in `P2-layer2.md`.

### Deviation D-M-15: INF-037 (U4) is matched to Task 7, and INF-056 (U23) is matched to Task 3. The true carriers are Task 4 and Ta

- **Location:** artifacts/coverage-matrix.yaml:319-325; artifacts/coverage-matrix.yaml:454-461
- **Spec section:** source.md:289; source.md:308
- **Classification:** drift (origin: reflect-artifact; severity: minor)
- **Sources:** P2R2-5 (calibrator U23 correction), C-003
- **Evidence / claim:** INF-037 (U4) is matched to Task 7, and INF-056 (U23) is matched to Task 3. The true carriers are Task 4 and Task 5. No requirement is lost.
- **Default remediation:** Correct `matched_task_ids` (INF-037 → Task 4, INF-056 → Task 5).

### Deviation D-M-16: These spans have no matrix rows, and their coverage rests on the by-reference triage.

- **Location:** artifacts/coverage-matrix.yaml
- **Spec section:** source.md:59-193, 216-234, 254-272, 323-418, 727-741 (§6 has INF-093 and §8 has INF-104)
- **Classification:** drift (origin: reflect-artifact; severity: minor)
- **Sources:** P2R2-6 (calibrator: overstated)
- **Evidence / claim:** These spans have no matrix rows, and their coverage rests on the by-reference triage.
- **Default remediation:** Annotate the T1 card that these spans have no matrix rows, and that their coverage rests on the by-reference triage.

### Deviation D-M-17: The conditional commit is an authorized addition, because it avoids an empty commit. But with `.dev/tasks` alw

- **Location:** plan:54
- **Spec section:** source.md:459
- **Classification:** authorized (origin: plan; severity: minor)
- **Sources:** P2R2-7, INV-018
- **Evidence / claim:** The conditional commit is an authorized addition, because it avoids an empty commit. But with `.dev/tasks` always staged, a ledger-only change satisfies "a file changed".
- **Default remediation:** The condition names `phase-1-removal-spec.md` or the facts file.

### Deviation D-M-18: If `$(rg -l install_retired_mcp tests)` is empty (true in this checkout today), plan:134 runs only the other t

- **Location:** plan:131; plan:134-135
- **Spec section:** source.md:572; source.md:576-577
- **Classification:** necessary (origin: inherited-from-spec; severity: important)
- **Sources:** reviewer 1 calibrator extra_risk, INV-006, orchestrator check (rg -l install_retired_mcp tests rc 1; install_retired_mcp.py absent; pyproject.toml:108 testpaths = ["tests"])
- **Evidence / claim:** If `$(rg -l install_retired_mcp tests)` is empty (true in this checkout today), plan:134 runs only the other two files, and plan:135 runs the whole suite with `-k "codegraph and serena"`. That is a false pass on the Serena-retirement gate.
- **Default remediation:** F=$(rg -l -g '*.py' install_retired_mcp tests)   # the assignment aborts under -e when nothing matches test -n "$F" uv run pytest $F …

### Deviation D-M-19: `test -z "$(comm -13 <baseline> <fail>)"` (plan:167) passes if the baseline is missing.

- **Location:** plan:21; plan:167; plan:217; plan:228
- **Spec section:** source.md:606; source.md:661
- **Classification:** necessary (origin: inherited-from-spec; severity: minor)
- **Sources:** INV-011, INV-017
- **Evidence / claim:** - `test -z "$(comm -13 <baseline> <fail>)"` (plan:167) passes if the baseline is missing. - `tail -1 … P2-layer2.md` (plan:228) exits 0 whatever the last line is. - `rg -n codegraph` (plan:217, plan-added) passes on any mention.
- **Default remediation:** - plan:21 says acceptance commands "exit 0 if and only if the criterion passes". - plan:167 becomes `comm -13 … > /tmp/p2-t5-new.txt` followed by `test ! -s /tmp/p2-t5-new.txt`. - plan:228 becomes `test "$(tail -1 .dev/codegraph-migration/evidence/P2-layer2.md)" = LAYER2_OK`.

## Inferred requirements (Pass 2)

| INF id | Verbatim quote (truncated to 120 chars) | Citation | Match result |
|---|---|---|---|
| INF-001 | \| F1 \| `src/superclaude/cli/install_codegraph.py` (new) \| Pin constants (`VERSION = "1.6.2"`, `TAG = "v1.6.2"`, `SHA2 | source.md:33 | none (see unmapped-triage.yaml) |
| INF-002 | \| F2 \| `src/superclaude/cli/install_mcp.py` \| (a) Registry entry `"codegraph"` in `MCP_SERVERS` (shape of the old `co | source.md:34 | none (see unmapped-triage.yaml) |
| INF-003 | \| F3 \| `src/superclaude/cli/main.py` \| `install()`: help/docstring text naming codegraph; phase block "Installing cod | source.md:35 | none (see unmapped-triage.yaml) |
| INF-004 | \| F4 \| `src/superclaude/cli/doctor.py` \| `_check_codegraph()` appended to `run_doctor` checks (`:26-44`); behaviour i | source.md:36 | Task 8 |
| INF-005 | \| F5 \| `update.sh` \| **No change.** Line 8 `superclaude install --force` already reaches the new phase; the four comm | source.md:37 | none (see unmapped-triage.yaml) |
| INF-006 | \| F6 \| `src/superclaude/core/CLAUDE.md` \| Add a `codegraph` row to the "MCP Servers" table (`:17-25`; keep the `\\| F | source.md:38 | Task 10 |
| INF-007 | \| F7 \| Indexing hook files (only if §3 ships a hook): `src/superclaude/hooks/scripts/codegraph-session-start.sh` (new) | source.md:39 | Task 9 |
| INF-008 | \| F8 \| `docs/user-guide/mcp-installation.md` \| New top section "Default setup: codegraph" (pin, verified download, re | source.md:40 | none (see unmapped-triage.yaml) |
| INF-009 | \| F9 \| `docs/reference/mcp-server-guide.md` \| `codegraph` row in "Available MCP Servers" (`:9`); new "codegraph lifec | source.md:41 | none (see unmapped-triage.yaml) |
| INF-010 | \| F10 \| `README.md` \| Install description (`:64`) and the dev-install comment (`:75`) say codegraph instead of Codeba | source.md:42 | none (see unmapped-triage.yaml) |
| INF-011 | \| F11 \| `CHANGELOG.md` \| `## [Unreleased]` entry "codegraph installed by default" (Added/Changed). \| **Phase 1** (it | source.md:43 | none (see unmapped-triage.yaml) |
| INF-012 | \| F12 \| `.github/workflows/test.yml` (`doctor-check`, `:130-171`) \| Keep the `Install Claude CLI` step (Phase 1's W1  | source.md:44 | none (see unmapped-triage.yaml) |
| INF-013 | \| F13 \| `tests/cli/test_install_codegraph.py` (new) \| Unit tests for F1 and the phase function (§4.1). \| no \| | source.md:45 | Task 4 |
| INF-014 | \| F14 \| `tests/cli/test_update_command.py` \| Autouse fixture also stubs `install_mcp.install_codegraph_mcp` (Phase 1  | source.md:46 | Task 6 |
| INF-015 | \| F15 \| `tests/cli/test_install_mcp_registry.py` \| Registry entry contract for `codegraph` and dispatch to `install_c | source.md:47 | Task 5 |
| INF-016 | \| F16 \| `tests/unit/test_cli_doctor.py` \| Tests for `_check_codegraph` (§2.7). \| no \| | source.md:48 | Task 8 |
| INF-017 | \| F17 \| `tests/cli/test_install_hooks.py`, `tests/unit/test_cli_install.py` (hook script listing, `:140-145`) \| Only  | source.md:49 | none (see unmapped-triage.yaml) |
| INF-018 | \| F18 \| `src/superclaude/cli/install_retired_mcp.py` (Phase 1's retire step), its Phase 1 test file, `src/superclaude/ | source.md:50 | Task 7 |
| INF-019 | \| F19 \| `.gitignore` \| Add `.codegraph/`. codegraph's own `.codegraph/.gitignore` is `*` plus `!.gitignore`, so the f | source.md:51 | none (see unmapped-triage.yaml) |
| INF-020 | - `codegraph_ready()` (in `install_mcp.py`): one read-only predicate on current state, shared by `install`, `install --l | source.md:194 | none (see unmapped-triage.yaml) |
| INF-021 | - When ready, the retire step also removes: (a) every user-scope entry other than `serena-local`, matched by shape rathe | source.md:195 | none (see unmapped-triage.yaml) |
| INF-022 | - When not ready: Phase 1's behaviour is unchanged (Tier K kept, hint printed); Tier R rows and the `/usr/local/bin/code | source.md:196 | Task 7 |
| INF-023 | - Local-scope (`projects.*.mcpServers`) and `.mcp.json` entries are reported with the exact command, never removed (Phas | source.md:197 | Constraints |
| INF-024 | - Kept by policy and stated in docs and CHANGELOG: `~/.serena`, project `.serena/`, `~/.cache/codebase-memory-mcp`, the  | source.md:198 | none (see unmapped-triage.yaml) |
| INF-025 | - user scope, by name and by launcher shape: `jq -e '(.mcpServers // {}) \| (has("serena") or has("codebase-memory-mcp") | source.md:210 | Task 16 |
| INF-026 | - local scope (`projects.*.mcpServers`, never removed automatically, §3.3 of Phase 1): `jq -e '[(.projects // {}) \| .[] | source.md:211 | Task 16 |
| INF-027 | - on Coder, as user `coder`, once the image's IronClaude pin includes the merge and the step-5 image is running: `! comm | source.md:212 | none (see unmapped-triage.yaml) |
| INF-028 | 1. Exit if `SUPERCLAUDE_CODEGRAPH_AUTOINIT=0`. | source.md:241 | Task 9 |
| INF-029 | 2. Binary: `cg=$(cat "$HOME/.codegraph/.superclaude-bin" 2>/dev/null)` (the installer's pointer to the registered binary | source.md:242 | Task 9 |
| INF-030 | 3. `top=$(git -C "${CLAUDE_PROJECT_DIR:-$PWD}" rev-parse --show-toplevel 2>/dev/null)` or exit; exit if `top` is empty,  | source.md:243 | Task 9 |
| INF-031 | 4. Exit if `$top/.codegraph/codegraph.db` exists (any state: complete, building, truncated, built by anyone). | source.md:244 | none (see unmapped-triage.yaml) |
| INF-032 | 5. `log="${XDG_STATE_HOME:-$HOME/.local/state}/superclaude/codegraph-init.log"`; `mkdir -p "${log%/*}" \|\| exit 0`. | source.md:245 | Constraints |
| INF-033 | 6. `nohup "$cg" init --yes "$top" </dev/null >>"$log" 2>&1 &` (every descriptor redirected so Claude Code does not wait; | source.md:246 | none (see unmapped-triage.yaml) |
| INF-034 | \| U1 \| `asset_name()` for Linux x86_64/amd64/aarch64/arm64 and Darwin x86_64/arm64 \| the four asset names; Windows/Fr | source.md:286 | none (see unmapped-triage.yaml) |
| INF-035 | \| U2 \| `SHA256` table has exactly the four assets and 64-hex values; `TAG == "v" + VERSION`; `MCP_TOOLS` equals the va | source.md:287 | Task 4 |
| INF-036 | \| U3 \| PATH has a `codegraph` printing `1.6.2` \| reused; `_download` never called \| | source.md:288 | none (see unmapped-triage.yaml) |
| INF-037 | \| U4 \| PATH copy prints `1.5.0`, `~/.local/bin/codegraph` prints `1.6.2` \| the `~/.local/bin` one wins \| | source.md:289 | Task 7 (false match, corrected to Task 4 per M-15) |
| INF-038 | \| U5 \| no matching copy; download bytes match the pinned hash \| extracted to `~/.codegraph/versions/v1.6.2/`, `~/.loc | source.md:290 | none (see unmapped-triage.yaml) |
| INF-039 | \| U6 \| download bytes do not match \| stage `checksum` failure; nothing left under `~/.codegraph/versions/`; no link c | source.md:291 | none (see unmapped-triage.yaml) |
| INF-040 | \| U7 \| tarball member with `..` or absolute path or a symlink escaping the target \| rejected before extraction (stage | source.md:292 | none (see unmapped-triage.yaml) |
| INF-041 | \| U8 \| download raises `URLError`/timeout \| stage `download` failure, message names the URL and the manual recovery,  | source.md:293 | none (see unmapped-triage.yaml) |
| INF-042 | \| U9 \| unsupported platform with no matching PATH copy \| failure names the platform; no download attempted \| | source.md:294 | none (see unmapped-triage.yaml) |
| INF-043 | \| U10 \| unsupported platform **with** a matching PATH copy \| success (reuse is platform-neutral) \| | source.md:295 | none (see unmapped-triage.yaml) |
| INF-044 | \| U11 \| `claude --version` fails \| failure before discovery or download (same rule as `install_mcp.py:830-843`) \| | source.md:296 | none (see unmapped-triage.yaml) |
| INF-045 | \| U12 \| registration absent \| one `claude mcp add-json codegraph <json> --scope user`; JSON equals §2.4 with the real | source.md:297 | Task 5 |
| INF-046 | \| U13 \| registration already equal \| no `claude mcp` call after `--version` (idempotent) \| | source.md:298 | none (see unmapped-triage.yaml) |
| INF-047 | \| U14 \| registration differs (old path, missing `alwaysLoad`, old version dir, env without `CODEGRAPH_MCP_TOOLS` as Co | source.md:299 | none (see unmapped-triage.yaml) |
| INF-048 | \| U15 \| add fails / verification fails \| previous entry restored; message says so \| | source.md:300 | none (see unmapped-triage.yaml) |
| INF-049 | \| U16 \| user-managed entry (extra env key, `headers`, `url`, other args): command resolves / does not resolve \| kept, | source.md:301 | none (see unmapped-triage.yaml) |
| INF-050 | \| U17 \| `~/.claude.json` unreadable or has duplicate keys \| lookup failure; no `claude mcp` mutation \| | source.md:302 | none (see unmapped-triage.yaml) |
| INF-051 | \| U18 \| `dry_run=True` \| describes the plan; no download, no `claude` call, no file written \| | source.md:303 | none (see unmapped-triage.yaml) |
| INF-052 | \| U19 \| second run after a successful download \| reuse, zero downloads, zero registry mutations \| | source.md:304 | none (see unmapped-triage.yaml) |
| INF-053 | \| U20 \| receipt written only after a verified download (not for a reused PATH copy); corrupt receipt deletes nothing a | source.md:305 | none (see unmapped-triage.yaml) |
| INF-054 | \| U21 \| pin bump: new dir installed, owned links flipped, previous owned dir kept; next run deletes it only when nothi | source.md:306 | none (see unmapped-triage.yaml) |
| INF-055 | \| U22 \| a non-owned `~/.local/bin/codegraph` pointing elsewhere is left alone and the version dir's launcher is regist | source.md:307 | none (see unmapped-triage.yaml) |
| INF-056 | \| U23 \| `superclaude mcp --servers codegraph --dry-run` \| no download, no `claude mcp` call \| | source.md:308 | Task 3 (false match, corrected to Task 5 per M-15) |
| INF-057 | \| U24 \| pointer file `~/.codegraph/.superclaude-bin` holds the winner's realpath (baked and downloaded cases); rewritt | source.md:309 | none (see unmapped-triage.yaml) |
| INF-058 | \| U25 \| the bounded runner kills a `claude` stub that ignores SIGTERM after the timeout (process group gone) \| §2.4 \ | source.md:310 | none (see unmapped-triage.yaml) |
| INF-059 | **T0. Commit the planning files and hand off to Coder.** | source.md:435 | Task 1 |
| INF-060 | Change: commit and push the branch so the Coder agent can fetch the handoff (`.dev/codegraph-migration/` is untracked wh | source.md:437 | Task 1 |
| INF-061 | **T0b. Align Phase 1's spec and facts file with §2.12.** | source.md:447 | Task 2 |
| INF-062 | Change: edit each listed Phase 1 row so it states the §2.12 gate (the current-pin Serena entry is kept only until `codeg | source.md:449 | Task 2 |
| INF-063 | **T1. Pin and verified acquisition module.** | source.md:463 | Task 4 |
| INF-064 | Change: §2.2, §2.3, §2.6 (receipt and pruning), §2.11 module shape, `MCP_TOOLS` set from the `Selected MCP_TOOLS:` line  | source.md:466 | Task 4 |
| INF-065 | **T2. Phase function, registry entry, dispatch, registration helpers.** | source.md:484 | Task 5 |
| INF-066 | Change: F2 (a)-(e); §2.4 table and bounded runner; tests U12-U19, U23, U25 and the registry/dispatch tests (§4.1). | source.md:486 | Task 5 |
| INF-067 | 1. Save this stdio client as `.dev/codegraph-migration/evidence/p2-mcp-tools.mjs` (committed with T2; layer 2 step 5b re | source.md:488 | Task 3 |
| INF-068 | 2. Leg A (always runs, no login, no real HOME): `W=$(mktemp -d)`; with `HOME="$W/home" CLAUDE_CONFIG_DIR="$W/home" CODEG | source.md:522 | Task 3 |
| INF-069 | 3. X-25 check, a hard stop: run 2's tool names are exactly the seven `codegraph_*` names (no `codegraph_explore`) and ru | source.md:523 | Task 3 |
| INF-070 | 4. Bands on D: `D <= 6000` bytes → seven tools; `D > 8000` → `status`; in between → Leg B decides (merged method §3; the | source.md:524 | Task 3 |
| INF-071 | 5. Leg B (undecided band only; merged method §4-§5): needs `timeout 10 claude --version` to succeed; two codegraph-only  | source.md:525 | none (see unmapped-triage.yaml) |
| INF-072 | 6. Decision: pass or fail band → as banded (decided by A); undecided with valid Leg B → seven tools if `T <= 2000`, else | source.md:526 | none (see unmapped-triage.yaml) |
| INF-073 | 7. Write `.dev/codegraph-migration/evidence/P2-mcp-tools-schema.md` with the 16 one-fact lines of the merged method §7,  | source.md:527 | Task 3 |
| INF-074 | **T3. `superclaude install` phase, exit term, `--list` block.** | source.md:561 | Task 6 |
| INF-075 | Change: F3; §2.1, §2.8; the test additions listed in §4.1 for this file. | source.md:563 | Task 6 |
| INF-076 | **T3b. Retire Serena once codegraph is ready.** | source.md:571 | Task 7 |
| INF-077 | Change: F18; §2.12. Tests: codegraph failed keeps the current-pin Serena entry and install exits 1; ready (owned pinned  | source.md:573 | Task 7 |
| INF-078 | **T4. Doctor check.** | source.md:582 | Task 8 |
| INF-079 | Change: F4; §2.7. Tests: dangling registered command fails; missing entry, version drift, prompt-hook leftover, `CODEGRA | source.md:584 | Task 8 |
| INF-080 | **T5. SessionStart hook.** | source.md:595 | Task 9 |
| INF-081 | Change: §3.2 behaviour and its listed tests. | source.md:597 | Task 9 |
| INF-082 | **T6. Core guidance.** | source.md:615 | Task 10 |
| INF-083 | Change: F6; §3.4 row and block. | source.md:617 | Task 10 |
| INF-084 | **T7. User docs, README, CHANGELOG.** | source.md:629 | Task 11 |
| INF-085 | Change: F8-F11, F19; include §2.6 removal commands, §2.10 failure table (short form), the registered tool list (`CODEGRA | source.md:631 | Task 11 |
| INF-086 | **T8. CI doctor job.** | source.md:644 | Task 12 |
| INF-087 | Change: F12. First check whether the step is still there: `rg -n 'name: Install Claude CLI' .github/workflows/test.yml`. | source.md:646 | Task 12 |
| INF-088 | **T9. Live sandbox proof (layer 2).** | source.md:654 | Task 13 |
| INF-089 | Change: save the §4.2 script as `.dev/codegraph-migration/evidence/p2-layer2.sh` and run it (it includes the offline-reu | source.md:656 | Task 13 |
| INF-090 | **T10. Full gate.** | source.md:669 | Task 14 |
| INF-091 | **T11. PR (shared with Phase 1, one merge unit).** | source.md:686 | Task 15 |
| INF-092 | **T12. Prove "completely absent" on the real workspace.** | source.md:704 | Task 16 |
| INF-093 | After each task-group commit in §5 (G0 to G5), and after G6's checks, post one comment. Never post anywhere else (no PR  | source.md:725 | Constraints |
| INF-094 | \| Simple: one obvious answer, or forced by a pinned test or a verified constraint \| helper name, message wording, test | source.md:749 | Constraints |
| INF-095 | \| Mid: two or more viable options with real trade-offs, local to one task \| where the receipt lives; whether `--list`  | source.md:750 | Constraints |
| INF-096 | \| Complex: changes the installer contract in §2, the indexing design in §3, the release order in §8, or crosses Phase 1 | source.md:751 | Constraints |
| INF-097 | Hard rules (no decision can override them): never run `claude mcp add/remove` or `superclaude install` against the real  | source.md:755 | Constraints |
| INF-098 | 1. A GitHub auth failure for `gh` (the executor cannot log in for the user). | source.md:758 | Constraints |
| INF-099 | 2. A release with a different `SHA256SUMS` than §0 for `v1.6.2` (possible tampering): stop, report on issue #323 and ask | source.md:759 | Constraints |
| INF-100 | 3. Merging the PR to `master` (ordering in §8 depends on the Coder bake; merge is the user's call; T11's merge-gate comm | source.md:760 | Task 15 |
| INF-101 | 4. Running `./update.sh` on the real workspace after merge (it mutates the live environment) and restarting the Claude s | source.md:761 | Task 16 |
| INF-102 | 5. After T0: giving `.dev/codegraph-migration/handoff/coder-handoff-prompt.md` to an agent working in the IronbellyOrg/C | source.md:762 | Constraints |
| INF-103 | 6. Non-blocking (the executor does not wait): when T2 step 0 ends in the undecided band with Leg B not run or invalid, t | source.md:763 | Constraints |
| INF-104 | \| 3 \| IronClaude \| Merge the Phase 1 + Phase 2 PR (human, §7 item 3), only after steps 1-2 are merged on Coder `main` | source.md:780 | Constraints |

Postscript: evidence-validator checked all 104 rows; 0 dropped.

## Inferred-claim audit

- `citations_inferred: 0`
- Inferred-fraction: `0 / 193` = 0.00

## Recommendations

### Recommendation R-M-01: apply the M-01 fix
- **File:** plan (and the spec when origin is inherited-from-spec)
- **Change:** One fenced block, both lines in the same shell: git diff --name-only HEAD~1 HEAD > /tmp/p2-t1-files.txt if rg '^\.claude/' /tmp/p2-t1-files.txt | rg -v '^\.claude/settings\.json$'; then exit 1; fi
- **Verifier:** re-Read plan:48; plan:21 after the edit and run the edited acceptance line under `bash -euo pipefail` where it is a command
- **Linked deviation(s):** D-M-01
- **Priority:** P1

### Recommendation R-M-02: apply the M-02 fix
- **File:** plan (and the spec when origin is inherited-from-spec)
- **Change:** (a) Run each scope check as a recorded line: `rc=0; jq -e '<filter>' ~/.claude.json || rc=$?`, then save rc to `/tmp/p2-t16-us.rc` (user) or `/tmp/p2-t16-ls.rc` (local), then `test "$rc" -le 1`. rc 1 means a hit. A missing or corrupt file (rc 2 or 5) still fails. (b) Add read-only `jq` lines that print `claude mcp remove <key> --scope user` for each offending user-scope key, and `cd <project-key> && claude mcp remove <name> --scope local` for each local hit. Put these in the G6 comment. (c) End the block with `test "$(cat /tmp/p2-t16-us.rc)" -eq 0`. User scope stays gating; local scope stays report-only. (d) Add a seventh, non-blocking human item: the user runs the printed user-scope command. Task 16 stays open and is reported in G6.
- **Verifier:** re-Read plan:275-286 (plan:277, 278, 286); plan:27 after the edit and run the edited acceptance line under `bash -euo pipefail` where it is a command
- **Linked deviation(s):** D-M-02
- **Priority:** P1

### Recommendation R-M-04: apply the M-04 fix
- **File:** plan (and the spec when origin is inherited-from-spec)
- **Change:** - Use the literal path `.dev/tasks/to-do/TASK-WF-phase2CodegraphI-20261029-192001/artifacts/<file>` in each block, not a Constraints `$ART`, which is unbound in separate blocks. - `mkdir -p` that directory in Task 3 and Task 14. - Task 3 captures the absolute worktree root before entering `$W` and writes `t3-run1.json` and `t3-run2.json` there before `rm -rf "$W"`.
- **Verifier:** re-Read plan:79, 85, 237, 253, 272, 287; plan:24 after the edit and run the edited acceptance line under `bash -euo pipefail` where it is a command
- **Linked deviation(s):** D-M-04
- **Priority:** P1

### Recommendation R-M-05: apply the M-05 fix
- **File:** plan (and the spec when origin is inherited-from-spec)
- **Change:** - Copy `/tmp/p2-final-run.txt` right after plan:243, and `/tmp/p2-new-failures.txt` right after plan:246, into the package artifacts path. - Move the `perf.json` restore ahead of `test ! -s`. - Always commit the Task 14 evidence (for example `test(codegraph): record final gate evidence`).
- **Verifier:** re-Read plan:237; plan:242-253; plan:259 after the edit and run the edited acceptance line under `bash -euo pipefail` where it is a command
- **Linked deviation(s):** D-M-05
- **Priority:** P1

### Recommendation R-M-08: apply the M-08 fix
- **File:** plan (and the spec when origin is inherited-from-spec)
- **Change:** - Move U11 to Task 5: the plan:92 list, the plan:96 gate ("U1-U10, U20-U22, U24") and plan:104 ("U11-U19, U23, U25"). - Check whether U22 (source.md:307, "the version dir's launcher is registered") also needs Task 5. UNVERIFIED.
- **Verifier:** re-Read plan:92; plan:96; plan:104 after the edit and run the edited acceptance line under `bash -euo pipefail` where it is a command
- **Linked deviation(s):** D-M-08
- **Priority:** P1

### Recommendation R-M-09: apply the M-09 fix
- **File:** plan (and the spec when origin is inherited-from-spec)
- **Change:** One condition per line. Write negatives as `if cmd; then exit 1; fi`. Keep the positive grep before its negative.
- **Verifier:** re-Read plan:162, 163, 165, 202, 203, 244 after the edit and run the edited acceptance line under `bash -euo pipefail` where it is a command
- **Linked deviation(s):** D-M-09
- **Priority:** P1

### Recommendation R-M-18: apply the M-18 fix
- **File:** plan (and the spec when origin is inherited-from-spec)
- **Change:** F=$(rg -l -g '*.py' install_retired_mcp tests)   # the assignment aborts under -e when nothing matches test -n "$F" uv run pytest $F …
- **Verifier:** re-Read plan:131; plan:134-135 after the edit and run the edited acceptance line under `bash -euo pipefail` where it is a command
- **Linked deviation(s):** D-M-18
- **Priority:** P1

### Recommendation R-M-03: apply the M-03 fix
- **File:** plan (and the spec when origin is inherited-from-spec)
- **Change:** One fenced block: MT=$(sed -n 's/^Selected MCP_TOOLS: //p' .dev/codegraph-migration/evidence/P2-mcp-tools-schema.md); test -n "$MT" E=$(jq -cn --arg t "$MT" …)   # exactly as source.md:534 jq -e --argjson e "$E" '. == $e' .dev/codegraph-migration/evidence/P2-add-json-shape.json
- **Verifier:** re-Read plan:107 after the edit and run the edited acceptance line under `bash -euo pipefail` where it is a command
- **Linked deviation(s):** D-M-03
- **Priority:** P2

### Recommendation R-M-06: apply the M-06 fix
- **File:** plan (and the spec when origin is inherited-from-spec)
- **Change:** - First action: `jq -S '.mcpServers' ~/.claude.json | sha256sum > /tmp/p2-t3-h0.txt`. - Last line: `test "$(jq -S '.mcpServers' ~/.claude.json | sha256sum)" = "$(cat /tmp/p2-t3-h0.txt)"`.
- **Verifier:** re-Read plan:86; plan:73-77; plan:23 after the edit and run the edited acceptance line under `bash -euo pipefail` where it is a command
- **Linked deviation(s):** D-M-06
- **Priority:** P2

### Recommendation R-M-07: apply the M-07 fix
- **File:** plan (and the spec when origin is inherited-from-spec)
- **Change:** Write to `/tmp/p2-t16-live-verify.txt`. Paste it, with the M-02 markers, into the G6 comment. Drop the file clause from plan:272 and plan:287.
- **Verifier:** re-Read plan:272; plan:287; plan:24 after the edit and run the edited acceptance line under `bash -euo pipefail` where it is a command
- **Linked deviation(s):** D-M-07
- **Priority:** P2

### Recommendation R-M-10: apply the M-10 fix
- **File:** plan (and the spec when origin is inherited-from-spec)
- **Change:** Optional: make `uv run python -c …` the primary command.
- **Verifier:** re-Read plan:216 after the edit and run the edited acceptance line under `bash -euo pipefail` where it is a command
- **Linked deviation(s):** D-M-10
- **Priority:** P2

### Recommendation R-M-11: apply the M-11 fix
- **File:** plan (and the spec when origin is inherited-from-spec)
- **Change:** After the positive grep, add `if grep -iE 'disconnected|not connected|failed' /tmp/p2-t12-get.txt; then exit 1; fi`, as in layer 2 step 5.
- **Verifier:** re-Read plan:282 after the edit and run the edited acceptance line under `bash -euo pipefail` where it is a command
- **Linked deviation(s):** D-M-11
- **Priority:** P2

### Recommendation R-M-12: apply the M-12 fix
- **File:** plan (and the spec when origin is inherited-from-spec)
- **Change:** The Task 2 completion message states whether Phase 1 already carried the amendments or this task made them.
- **Verifier:** re-Read plan:54 after the edit and run the edited acceptance line under `bash -euo pipefail` where it is a command
- **Linked deviation(s):** D-M-12
- **Priority:** P2

### Recommendation R-M-13: apply the M-13 fix
- **File:** plan (and the spec when origin is inherited-from-spec)
- **Change:** Task 6 states that the Ready line lands in Task 7, and Task 7's acceptance checks it.
- **Verifier:** re-Read plan:120; plan:125; plan:131 after the edit and run the edited acceptance line under `bash -euo pipefail` where it is a command
- **Linked deviation(s):** D-M-13
- **Priority:** P2

### Recommendation R-M-14: apply the M-14 fix
- **File:** plan (and the spec when origin is inherited-from-spec)
- **Change:** One sentence naming the fallback (stdio `initialize` + `tools/list`, `serverInfo.name == codegraph`), recorded in `P2-layer2.md`.
- **Verifier:** re-Read plan:223-227 after the edit and run the edited acceptance line under `bash -euo pipefail` where it is a command
- **Linked deviation(s):** D-M-14
- **Priority:** P2

### Recommendation R-M-15: apply the M-15 fix
- **File:** reflect artifacts
- **Change:** Correct `matched_task_ids` (INF-037 → Task 4, INF-056 → Task 5).
- **Verifier:** re-Read artifacts/coverage-matrix.yaml:319-325; artifacts/coverage-matrix.yaml:454-461 after the edit and run the edited acceptance line under `bash -euo pipefail` where it is a command
- **Linked deviation(s):** D-M-15
- **Priority:** P2

### Recommendation R-M-16: apply the M-16 fix
- **File:** reflect artifacts
- **Change:** Annotate the T1 card that these spans have no matrix rows, and that their coverage rests on the by-reference triage.
- **Verifier:** re-Read artifacts/coverage-matrix.yaml after the edit and run the edited acceptance line under `bash -euo pipefail` where it is a command
- **Linked deviation(s):** D-M-16
- **Priority:** P2

### Recommendation R-M-17: apply the M-17 fix
- **File:** plan (and the spec when origin is inherited-from-spec)
- **Change:** The condition names `phase-1-removal-spec.md` or the facts file.
- **Verifier:** re-Read plan:54 after the edit and run the edited acceptance line under `bash -euo pipefail` where it is a command
- **Linked deviation(s):** D-M-17
- **Priority:** P2

### Recommendation R-M-19: apply the M-19 fix
- **File:** plan (and the spec when origin is inherited-from-spec)
- **Change:** - plan:21 says acceptance commands "exit 0 if and only if the criterion passes". - plan:167 becomes `comm -13 … > /tmp/p2-t5-new.txt` followed by `test ! -s /tmp/p2-t5-new.txt`. - plan:228 becomes `test "$(tail -1 .dev/codegraph-migration/evidence/P2-layer2.md)" = LAYER2_OK`.
- **Verifier:** re-Read plan:21; plan:167; plan:217; plan:228 after the edit and run the edited acceptance line under `bash -euo pipefail` where it is a command
- **Linked deviation(s):** D-M-19
- **Priority:** P2


## Input drift

`input_drift_detected: true`. At the Wave 5 recompute one input changed: `.dev/codegraph-migration/specs/phase-1-removal-spec.md` (sha256 `4f25d464…2259` at Wave 0 → `f2f1f489…7037`, modified 2026-10-29T20:28:20Z, during this run; owned by the Phase 1 finalizer F1, not by this run). It is referenced only by plan Task 2 (the T0b check); no finding above depends on its content. Status stays `partial`.
