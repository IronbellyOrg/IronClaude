# Research: Enforcement surface for a sub-orchestrator / coordinator mode
**Scope:** require-orca-worktree-agent.sh (+ mirror, hooks.json, tests), tests/skills/test_worker_contract.py (grep only), launch-level-guard.sh, launch-job-identity.sh, Orca CLI help (read-only)
**Status:** Complete
**Date:** 2026-11-09
---

## 1. require-orca-worktree-agent.sh (PreToolUse Bash gate)

Files (verified by Glob/Read/diff):
- `src/superclaude/hooks/scripts/require-orca-worktree-agent.sh` (357 lines, read in full) [CODE-VERIFIED]
- `plugins/superclaude/hooks/scripts/require-orca-worktree-agent.sh`: byte-identical to the src copy (`diff -q` printed no difference) [CODE-VERIFIED]
- Dev copy `.claude/hooks/require-orca-worktree-agent.sh` exists (gitignored sync-dev output).
- Registration: `src/superclaude/hooks/hooks.json:105-114` (matcher `Bash`, command `~/.claude/hooks/require-orca-worktree-agent.sh`, timeout 3) and `plugins/superclaude/hooks/hooks.json:80` (same command). The two hooks.json files differ as whole files, but both register this hook [CODE-VERIFIED].

### 1.1 What the hook reads (identity signals)
- Only `.tool_name == "Bash"` and `.tool_input.command` (script lines 345-347: `jq -j 'if .tool_name == "Bash" then (.tool_input.command // "" | strings) else "" end'`). It reads no `session_id`, `agent_id`, `agent_type`, `cwd`, env var or Orca id.
- Conclusion: the hook CANNOT tell a coordinator from a supervised worker, or an orchestrator from a sub-orchestrator. Identity is outside its input surface. [CODE-VERIFIED, lines 342-349]
- Header comment: it also fires inside subagent Bash calls (lines 5-7).

### 1.2 What it blocks / allows
- Blocks one pattern: command word `orca` (or a path ending `/orca`, or a command word starting `$`), first two non-option args `worktree` and `create`, none of `--agent`, `--agent=...`, `--help`, `-h` among that command's own words (header lines 29-33; scanner `fin()` lines 99-103). Exit 2 plus the stderr message at lines 351-357.
- Does NOT block `orca orchestration worker-start`, `orca agent launch`, `dispatch`, `task-create`, or `worktree create --agent claude`. A sub-orchestrator running the CLAUDE.md-prescribed form would pass; the hook is silent on WC-13 and on nesting depth [CODE-VERIFIED].
- The block message names the role: "The session that creates the worktree becomes its orchestrator (or a coordinator under another orchestrator) and owns that agent. Supervised workers use `orca orchestration worker-start`." (lines 354-355). Prose only, no logic keyed to it.
- Declared ceilings (lines 39-61): `bash -c`, `eval`, `xargs`, `claude --bare`, subprocess calls from scripts (orca_worktree.py) are not covered. Even a hook extension that denied a worker's create would be bypassable by design.

### 1.3 Tests pinning this hook
- `tests/hooks/test_require_orca_worktree_agent.py`: the block text is pinned at lines 36-37 (`"coordinator under another orchestrator) and owns that agent.\n"`, `"Supervised workers use \`orca orchestration worker-start\`.\n"`); `"orchestration-worker-start": "orca orchestration worker-start --name x"` is in the allowed table (line 115). Tests: `test_blocked` 129, `test_allowed` 137, `test_fail_open` 156, jq missing 172, awk missing 179, scanner fails 186, `test_script_is_executable_and_runs_no_python` 197 [CODE-VERIFIED via Grep]. Changing the "coordinator under another orchestrator" wording means updating test line 36 plus the same wording in CLAUDE.md files.
- `tests/hooks/test_require_orca_worktree_agent_governed.py` (57 lines, read in full): pins that a bare create is still blocked when the `session_id` is bound in `~/.claude/state/launch-level/sessions/old`. The test event carries `session_id`, `cwd`, `tool_use_id`, which the hook ignores (lines 35-57).
- Other files that mention the hook (found by Grep, not read): `tests/hooks/test_launch_level_guard_registration.py`, `tests/unit/test_cli_install.py`, `tests/cli/test_install_hooks.py`, `tests/hooks/test_freshness_subagent_start_policy.py`, `src/superclaude/cli/install_hooks.py`.

---

## 2. WORKER-CONTRACT.md text and the tests that pin it

Source: `src/superclaude/core/WORKER-CONTRACT.md` (installed to `~/.claude/WORKER-CONTRACT.md`). Read lines 1-66 plus Grep.

### 2.1 Rule text a sub-orchestrator mode would touch
- Line 5: "A coordinator plans the work, creates Tasks, starts one worker per Task and reads each worker's report. Each `/sc:` command stays a self-contained unit of work: one worker (a top-level Claude session in its own Orca terminal) runs one command and reports it with `worker_done`." Two levels only; no role for a coordinator that is itself directed.
- Line 11 "Worker run": "a session that received an Orca preamble carrying a Task ID and a Dispatch ID. Only such a session may send lifecycle messages". A sub-orchestrator that was dispatched by an orchestrator IS a worker run by this definition, so WC-13 binds it.
- Line 40, WC-8: "A command never calls `worker-start`, `dispatch` or `task-create`. Fan-out that needs Orca records is split into separate Tasks by the coordinator." (command-level; a sub-orchestrator mode is a session, not a command, but `/sc:orchestrator` would be a command that calls these, so WC-8 also needs an exemption or the mode would be a never-as-worker, coordinator-only command).
- Line 62, WC-13: "The worker's top-level session never calls `worker-start`, `dispatch` or `task-create`, Orca's low-level dispatch, or `orca-cli` `worktree create --agent` or `agent launch`, at any depth setting. Work it finds that needs another worker is stated in its `worker_done` body; the coordinator decides (section 4)." "at any depth setting" means the contract forbids fan-out even if Orca depth were raised. This is a contract-level rule, independent of Orca's setting [CODE-VERIFIED].
- Line 69: "These bind the coordinator: an Orca coordinator session the person opened." So the coordinator is defined as person-opened; a sub-orchestrator is not person-opened. Section 4 coordinator rules would not apply to it as written.
- Line 246: "The coordinator starts only Tasks it created itself ... records each follow-up Task it created because a worker's result showed work that could not be planned before dispatch, with the extra time that cost. This is the evidence decision D5's revisit trigger reads." So the contract already has a defined evidence trigger for revisiting D5 (the depth decision) [CODE-VERIFIED line 246].
- Line 23, never-as-worker list: `/sc:agent`, `/sc:git`, `/sc:help`, `/sc:issue`, `/sc:pm`, `/sc:spawn`, `/sc:swarm-wizard` (+ `/sc:pr-submit` under D3). `/sc:orchestrator` is not on it; a coordinator-only command that must not run as worker would have to be added here ("The list changes only when the coordinator-only command set or D3 changes").
- Line 16 Brief guard: case 3 refuses never-as-worker commands by name alone; the guard is the mechanical place a worker-launched `/sc:orchestrator` would be refused.

### 2.2 Tests that pin it (tests/skills/test_worker_contract.py, 3195 lines; Grep only)
- Header lines 1-22: contract read via `CONTRACT_PATH = src/superclaude/core/WORKER-CONTRACT.md` (line 19), commands via `COMMANDS_DIR` (line 20). Each rule is pinned by phrases in `RULE_PHRASES` (line 25).
- `RULE_PHRASES["WC-13"]` at line 155: `("WC-13", ["No Orca fan-out from the worker session"])`. Only the title phrase is pinned. The body ("never calls worker-start ... at any depth setting") is not phrase-pinned, so body edits would not fail this entry, but renaming/removing the title would.
- `RULE_PHRASES["WC-8"]` at line 123: `("WC-8", ["No Orca fan-out from inside a command"])`.
- `RULE_PHRASES["WC-6"]` at lines 181-189 pins "the coordinator never uses `worker-start --retry-of`", "A crashed or stalled attempt is settled by the coordinator".
- `RULE_PHRASES["WC-7"]` line 150, `["WC-9"]` 124, `["WC-12"]` 151, `["WC-14"]` 156-164 (pins "The one exception is a coordinator interrupt ... (the S6 nudge, section 4)"), WC-15 165-172.
- Coordinator-definition and coordinator-rule phrases pinned in the same table: "liveness-wait" (lines 199-208: the exact `orca orchestration check --wait --types ... --timeout-ms 300000` string, "After three empty waits in a row, the coordinator enumerates its workers with `worker-list`"), "liveness-sweep-and-states" (209+), "wc6-live-attempt-settlement" (190-197).
- Parametrized rule tests: line 907 (`@pytest.mark.parametrize("rule", sorted(RULE_PHRASES))`, rule text check using `RULE_PHRASES[rule]` at line 756) and line 1044 (same parametrization; the negative variant that removes each phrase and expects failure). Any phrase added to or changed in RULE_PHRASES is automatically covered by both.
- Test hits for the words "coordinator under" / "Sub-workers": none in test_worker_contract.py (the Grep for `coordinator|worker-start|nested|Sub-workers|depth` returned no "Sub-workers" or "coordinator under" lines) [CODE-VERIFIED by absence in the first 150 hits; hits were truncated at 150, later hits at 2349-2980 are all about `.dev/tasks` staging deferral to the coordinator (WC-9) and the never-as-worker list, e.g. line 2972 "/sc:git is on the never-as-worker list; its commit and merge examples run only in the coordinator or person session"].
- "nested" in this test file means nested `/sc:` command invocations with `<report-dir>/nested/<cmd>-<n>/` (lines 93-97, 436-740, 1399-1411, 1621-1641), NOT nested Orca workers. Do not confuse the two when scoping a change.
- Order-dependent tests: `test_guard_order_check_fails_when_guard_follows_command` (1093) and `..._guard_line_removed` (1105) pin the brief-guard ordering in command files (brief guard text at contract line 16).
- Static pin of the build-time brief template: contract lines 91 and 293 include `worker-start --worktree new-child --base-branch <feature branch>`; test lines 1057-1072 check child-setup wording; any new coordinator-under-orchestrator brief variant would extend that.

---

## 3. Launch-level hooks (launch-level-guard.sh, launch-job-identity.sh)

Files: `src/superclaude/hooks/scripts/launch-level-guard.sh` (747 lines; read 1-130 and 380-510), `src/superclaude/hooks/scripts/launch-job-identity.sh` (566 lines; read 1-90 and 415-484). Design: `docs/designs/sc-issue-launch-level-hook.md` (Grep only).

### 3.1 What "governed" means (not worker/coordinator)
- The guard governs ONLY a session that `/sc:issue --claim` launched and bound in the store `~/.claude/state/launch-level/sessions/<session_id>` (guard header lines 4-7; fast path lines 393-394: `[ "$LL_GOVERNED" = 1 ] || exit 0 # unbound or identity loss`). Levels: worktree (W), worktree approved (WA), full (F), full --submit (FS) (lines 115-120). Every other session, including Orca coordinators and Orca supervised workers, is ordinary and never blocked (header line 7) [CODE-VERIFIED].
- Identity input: `session_id` only. The comment at line 391 says "agent_id is never read here and there is no cwd fallback". launch-job-identity.sh line 431: "do not guess from agent_id, parent fields, cwd or environment" [CODE-VERIFIED]. So no hook in this repo reads Orca env (`ORCA_TERMINAL_HANDLE`, `ORCA_WORKTREE_ID`, `ORCA_AGENT_LAUNCH` are all set in this very session per `env`) nor a Task/Dispatch id.
- Design doc lists "U7 Orca preamble" and "U28 Orca hooks" as UNVERIFIED (docs/designs/sc-issue-launch-level-hook.md:457) [UNVERIFIED]: nobody has verified that a hook can see the Orca preamble.

### 3.2 Interaction with a sub-orchestrator that was launched by /sc:issue --claim
- Class ESCAPE (guard lines 455-478; design lines 175, 247): in a governed session any `orca` command is ESCAPE (blocked at every level, message LL-ESCAPE "starting or messaging another agent or session (claude, ccsession, orca, SendMessage, /sc:issue, ...)") EXCEPT `status`, `help`, `--version`, `worktree current|list|show`, `terminal list|show|read`, `orchestration check|inbox|run-current|task-list|worker-show`, and `--help/-h` tails.
- Therefore: `worker-start`, `dispatch`, `task-create`, `send`, `reply`, `run-create`, `worktree create`, `agent launch` are all blocked in a governed session, as are `SendMessage` and `claude -p`. Tests: `tests/hooks/test_launch_level_guard.py:3047-3055` (ESCAPE list: `orca agent launch --name w`, `orca orchestration send x`, `orca orchestration dispatch x`, `orca worktree create --name x`) and `:3087-3091` (NONE list: the read-only orchestration verbs) [CODE-VERIFIED].
- Local subagents are allowed in a governed session (LL-ESCAPE "You can" text line 89; design line 180: Agent/Task NONE unless `isolation: remote`).
- Consequence: a sub-orchestrator mode that ran inside a session launched by `/sc:issue --claim` (the issue-to-worktree path from issue #444) could not delegate through Orca at all; a sub-orchestrator mode only works in sessions that are not launch-level governed, or the guard's allowlist must change. Note this is a policy fact for the specific `/sc:issue --claim` path, not for ordinary Orca sessions.
- Exposure of identity to the guard: it is keyed to session_id, so granting a "sub-orchestrator" exemption is feasible mechanically only through a new launch record kind (store file content = level) or through an Orca-derived signal that no hook reads today; neither exists [inference from lines 391-394, 431].

### 3.3 launch-job-identity.sh
- Wraps a governed session's Bash calls in a fresh bash job (`updatedInput`) so descendants are attributable (header lines 1-19, output at 479-482). Reads `agent_id`/`agent_type` only to reject non-string shapes (lines 448-450). No worker/coordinator logic. Its rewrite of the command is why `test_require_orca_worktree_agent_governed.py` exists: the Orca gate might see the wrapped command; the test only pins the original-command case (governed test header lines 1-10).

---

## 4. Orca itself (read-only commands; nothing started or changed)

Commands run: `orca orchestration --help`, `orca orchestration worker-start --help`, `orca orchestration run-create --help`, `orca orchestration reset --help`, `orca skills list`, `orca skills get orchestration` (+ `--reference references/worker-contract.md`, `references/coordinator-loop.md`), `orca skills get orca-cli`, and file reads under `/opt/Orca/resources/app.asar.unpacked/out/` and `~/.config/orca/profiles/*/orca-data.json`. No setting was changed; no session, worktree, run or worker was started.

### 4.1 No CLI for the depth setting
- `orca orchestration --help` lists: run-create, run-use, run-current, run-list, run-show, send, check, reply, inbox, task-create/list/update, worker-start/show/read/stop/abandon/release/retain/list, dispatch, request-show, dispatch-show, ask, coordinator-start/stop (retired), gate-create/resolve/list, reset. No config/settings verb. `orca --help` top-level (first 60 lines) showed no settings command; `orca agent-context | grep -i depth|nested|parent` printed nothing. The only setting surface is the desktop app: Settings -> Orchestration -> "Nested worker depth" (text in `nested-worker-depth.js` NEXT_STEPS) [CODE-VERIFIED].
- Current value: `grep -ho '"nestedWorkerMaxDepth":[0-9]*' "$ORCA_RUNTIME_SOURCE_PROFILE_PATH"/profiles/*/orca-data.json` printed `"nestedWorkerMaxDepth":1` (exit 0) [CODE-VERIFIED today, 2026-11-09]. Setting is per Orca profile (machine-wide here; `local-default` is the only profile per `.dev/orca-command-refactor/inventory/orca-capabilities.md:98`).
- Default and fence: `/opt/Orca/resources/app.asar.unpacked/out/shared/nested-worker-depth.js:7-11` default 1, "Root coordinators are depth 0; the first generation of workers is depth 1"; `resolveNestedWorkerMaxDepth` returns 1 for anything not a safe integer >= 1 (lines 26-35), so a bad value cannot disable the limit. Refusal code `nested_worker_depth_exceeded`, message "Sub-worker dispatch is not permitted at depth N (max M). Complete this task yourself." [CODE-VERIFIED].

### 4.2 Where Orca enforces depth
- Bundled main chunk `out/main/chunks/orcad-migration-source-retention-B_-OYaBD.js` (minified; grepped snippets): `createStartingWorkerDispatch({creator: ..., maxDepth: r.getNestedWorkerMaxDepth(), requiredCreatorDispatchId: e.helperCreator?.id, ..., taskParentId: t.parent ?? e.helperCreator?.task_id, ...})` in the worker-start path; the dispatch preamble builder is called with `canDispatchSubWorkers: dispatchDepth < t.getNestedWorkerMaxDepth()` and `subWorkersInOwnRun: true`; the dry-run path calls `c.resolveChildDispatchDepth(jK(i,e.from,r), t)` [CODE-VERIFIED by quoted minified text; call-site coverage for `dispatch` (low-level) is inferred from `canDispatchSubWorkers` and the dryRun branch, `task-create` from a depth-1 worker still UNVERIFIED as in orca-capabilities.md:103].
- So Orca enforces depth ONLY on orchestration dispatches (worker-start / dispatch) by computing the child's depth from the creator's Dispatch. It does NOT see `orca worktree create --agent` or `orca agent launch` (those are `orca-cli` launches; the orchestration guide's role table says the "Handoff owner" route is "Use `orca-cli`; create no Run, Task, or Dispatch and do not monitor completion") [CODE-VERIFIED from the guide text; the conclusion that depth does not apply to them is an inference]. WC-13 (contract line 62) explicitly lists those two verbs, which is the gap WC-13 fills.
- `--parent` on `worker-start` is a TASK parent (`taskParentId`), not a depth or worktree parent. `orca worktree create --parent-worktree/--no-parent` is worktree lineage only (orca-cli guide lines 88-125: "`--no-parent` only controls Orca lineage; it does not choose the Git base"). Neither limits who may orchestrate [CODE-VERIFIED from help text].

### 4.3 Orca already has a native "helper worker" concept (contradicts the contract's tone)
- `orca skills get orchestration` line 130: "A dispatched worker starts its own helpers with `worker-start --spec` on the Run it works for, without `run-create`; the helpers report to that worker." `references/worker-contract.md` section "Helper workers" (lines 74-90): "When the preamble has a SUB-DISPATCH section, start helpers on your own Dispatch's Run ... `worker-start --from <worker_handle> --spec "<sub-task>" --worktree current --agent <agent>` ... Their questions, escalations, and `worker_done` arrive in your own `check`, next to your coordinator's mail ... wait for every helper's `worker_done` before sending yours. After you settle, a helper still running reports to your coordinator's Run." [CODE-VERIFIED: printed by this Orca build]
- The preamble carries a SUB-DISPATCH section only when `canDispatchSubWorkers` is true (depth < max). At the current max 1, a depth-1 worker gets no SUB-DISPATCH section, so Orca itself says "Complete this task yourself". If the setting were raised to 2, Orca would hand depth-1 workers a native sub-dispatch path with reporting to the parent worker, and only WC-13 (contract text, "at any depth setting") would still forbid it [CODE-VERIFIED for mechanics; consequence is inference].
- Orca's role table (guide "Classify the role") has: Coordinator, Dispatched worker, Handoff owner, Compatibility operator, Ordinary terminal agent. No "sub-coordinator" or "sub-orchestrator" role. The nearest native fits are (a) a dispatched worker with helpers (needs depth >= 2) and (b) a handoff owner via `orca-cli` (no supervision, no reporting back) [CODE-VERIFIED].
- Roles are decided from prompt context (the live injected preamble), not from env: this session's env carries `ORCA_TERMINAL_HANDLE`, `ORCA_WORKTREE_ID`, `ORCA_AGENT_LAUNCH` etc., but the guide says "Workers use the exact executable, handle, Task ID, and Dispatch ID in the live preamble". A hook cannot see the preamble [CODE-VERIFIED for hook input fields (section 1.1); the preamble-in-prompt is per the Orca guide].

### 4.4 What Orca enforces vs. leaves to WC-13
| Concern | Orca enforces | Left to IronClaude (WC-13 / hooks) |
|---|---|---|
| worker-start / dispatch from a worker | yes, via depth fence (max 1: refuses at depth 1 with `nested_worker_depth_exceeded`) | WC-13 also forbids it "at any depth setting" |
| `worktree create --agent`, `agent launch` from a worker | no (not Dispatches) | WC-13 prose only; the hook requires `--agent` on create but does not check who is calling |
| `task-create` from a worker | UNVERIFIED | WC-13 prose |
| Who a creator "owns" / reports to for a non-Dispatch launch | nothing (worktree lineage `--parent-worktree` is cosmetic grouping) | CLAUDE.md prose ("creator becomes its orchestrator, or a coordinator under another orchestrator") |
| Reporting channel upward | Run inbox + `worker_done` for Dispatch workers; helper mail goes to the creating worker's `check` | n/a |
| Raising the limit | one profile-wide desktop setting; no per-run override found (inferred, `.dev/orca-command-refactor/decisions/D5/debate/adversarial/merged-output.md:35`) | D5 keeps it at 1; AC-C6 grep checks it is 1 |

### 4.5 D5 context (doc-sourced; verified where marked)
- `.dev/issues/444/analysis/analyze-orchestration.md:39`: raising depth "would change the safety floor for every Orca run, not only IronClaude's"; "Lowering it while deeper workers run is UNVERIFIED". The setting value 1 is [CODE-VERIFIED] above; the statement about raising's blast radius is [CODE-VERIFIED] in the sense that the setting is in one profile file that `local-default` shares, but whether the running app re-reads the file is [UNVERIFIED] (per merged-output.md:167).
- WORKER-CONTRACT line 246 defines D5's revisit trigger: follow-up Tasks the coordinator creates because "a worker's result showed work that could not be planned before dispatch", with extra time cost recorded in run notes [CODE-VERIFIED line 246]. I did not search for recorded run notes under this trigger (outside slice).

---

## Gaps and Questions

1. [UNVERIFIED] Whether Orca's depth fence covers `task-create` from a depth-1 worker (also open in orca-capabilities.md:103). Not tested because it would mutate Orca state.
2. [UNVERIFIED] Whether the running Orca app re-reads `nestedWorkerMaxDepth` from `orca-data.json` live, and whether any per-run override exists (no CLI verb found; inferred only).
3. [UNVERIFIED] Whether any hook can observe the Orca preamble or a Task/Dispatch id (design doc U7/U28 open). Hook inputs read today: `tool_name`, `tool_input.command`, `session_id` (and `agent_id`/`agent_type` only for shape checks). Env carries `ORCA_TERMINAL_HANDLE`/`ORCA_WORKTREE_ID`/`ORCA_AGENT_LAUNCH` here, but no repo hook reads env, and nothing shows env distinguishes a dispatched worker from a coordinator terminal. Not tested (would need a live worker).
4. Depth enforcement call sites were read only from minified grep snippets in one bundle chunk; the full call graph for `dispatch` and `resolveChildDispatchDepth` was not traced.
5. I did not read the other test files that mention the hook (`test_launch_level_guard_registration.py`, `test_cli_install.py`, `test_install_hooks.py`, `test_freshness_subagent_start_policy.py`) beyond Grep; the Grep for coordinator/worker-start in `test_launch_level_guard_registration.py` found nothing.
6. test_worker_contract.py Grep was capped at 150 lines; hits after line ~1700 were only skimmed (2349-2980 are WC-9/never-as-worker). A sub-orchestrator change should rerun a full grep of that file for `coordinator`, `WC-13`, `worker_done` before editing.
7. Doc/code tension to flag: WORKER-CONTRACT WC-13 says "at any depth setting", while Orca's own bundled guide (`orca skills get orchestration` line 130 and `references/worker-contract.md` "Helper workers") instructs dispatched workers to start helpers whenever the preamble offers SUB-DISPATCH. Not a staleness issue (both are current), but the two authorities disagree on intent if depth is ever raised.
8. "A coordinator under another orchestrator" appears only as prose in 4 places (root CLAUDE.md:312, src/superclaude/core/CLAUDE.md:58, skills/ccsession-tag/README.md:242, the hook message at script line 354, pinned by test line 36); it has no definition in WORKER-CONTRACT.md and no mechanical meaning [CODE-VERIFIED by Grep].

## Key Takeaways

- No hook in the repo can distinguish a coordinator, a supervised worker, or a sub-orchestrator. `require-orca-worktree-agent.sh` reads only the Bash command text; it neither blocks nor allows by role, and it allows `worker-start`, `agent launch` and `worktree create --agent` from anyone. WC-13 is therefore enforced by contract text and the worker's compliance, not by any mechanism.
- The only mechanical depth fence is Orca's `nestedWorkerMaxDepth` (currently 1, profile-wide, desktop-app setting only, no CLI). It governs orchestration dispatches (`worker-start`/`dispatch`) and not `orca-cli` launches (`worktree create --agent`, `agent launch`), so a sub-orchestrator built on `orca-cli` launches would not be stopped by Orca at all, while one built on `worker-start` needs depth >= 2 (and Orca then provides native helper-worker reporting to the parent's inbox).
- `/sc:issue --claim` governed sessions are blocked from every state-changing `orca` verb (ESCAPE class, `launch-level-guard.sh:455-478`; tests `test_launch_level_guard.py:3047-3055`), so a sub-orchestrator mode cannot run there without changing the guard allowlist or adding a new launch-record kind.
- A contract change touches: WORKER-CONTRACT.md lines 5, 11, 16-23 (never-as-worker list), 40 (WC-8), 62 (WC-13), 69 (coordinator definition), 246 (D5 trigger); `RULE_PHRASES` entries at test_worker_contract.py lines 123, 155 (title phrases only for WC-8 and WC-13), the coordinator phrases at 181-209, the parametrized tests at 907 and 1044; the hook message and its test line 36; the CLAUDE.md wording in 4 files; the launch-level ESCAPE lists if governed sessions must be supported.
- Orca's role model has no sub-coordinator; the nearest native paths are depth-2 helper workers (supervised, reports upward) or `orca-cli` handoff (unsupervised, no report channel). "A coordinator under another orchestrator" has no mechanical definition anywhere.

## Summary

The enforcement surface for a sub-orchestrator mode is thin and mostly prose. The Orca-worktree hook inspects only the Bash command text and cannot tell any role from another, and the launch-level guard keys on a bound session id and blocks all state-changing Orca verbs only for sessions launched by `/sc:issue --claim`. Orca itself enforces depth solely on orchestration dispatches (limit 1 today, a profile-wide desktop setting with no CLI), and its native helper-worker path would activate if depth were raised, while WC-13 forbids fan-out "at any depth setting" and also covers the `orca-cli` launch verbs Orca does not fence. A contract change would need coordinated edits to WORKER-CONTRACT.md, a few phrase-pinned tests in test_worker_contract.py, the hook message and its test, CLAUDE.md wording in four files, and possibly the launch-level ESCAPE allowlist; nothing mechanical currently defines "a coordinator under another orchestrator".

