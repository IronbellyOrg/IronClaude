review: 2 of 3
# Re-review 2 of /sc:spec-panel --mode critique --focus requirements,architecture

- candidate: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md, sha256 88c067212b041e0b99f6fda10c231eb231ba347817f3cb28916d81f4045efd50 (291 lines, 59544 bytes)
- baseline: .dev/orca-command-refactor/specs/history/spec-v1.md, sha256 d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d (286 lines, 57763 bytes). This hash equals the candidate hash recorded in round1.md:3, so the baseline is the text round 1 reviewed.
- prior: .dev/orca-command-refactor/review/round1.md, sha256 e27a14ff484a926572413451afba2955e9b7d3d65f3e7ad5e65579c5f29d8cb3; header `review: 1 of 3` (round1.md:1), `verdict: FAIL` (round1.md:264); N = 1 + 1 = 2.
- reviewer model actually used: claude-sonnet-5-5
- roles (fixed by the brief, not inferred): CANDIDATE = specs/orca-worker-contract-spec.md; BASELINE = specs/history/spec-v1.md; PRIOR = review/round1.md.
- panel: the round-1 report was a four-reviewer panel merged by script (round1.md:1-8). `superclaude` is not installed in this sandbox, so this re-review is one reviewer with no merge step and no ledger; the coordinator merges.
- spec-panel experts applied in the command's fixed order for the requirements and architecture focus: Wiegers, Adzic, Cockburn (requirements); Fowler, Nygard, Whittaker (architecture and attack). No `--format` was given; this report uses the Critique-mode layout.
- citation scope: only `.dev/orca-command-refactor/` files are checkable here. Every `sk/`, `cmd/`, `CLAUDE.md`, `src/` and `.dev/codegraph-migration/` line the spec cites is UNVERIFIED here; I rely on them only through the inventory lines that quote them. Short names: CAND = the candidate, BASE = the baseline, INV-A/INV-B/CAPS = `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`.

## Step 1: evidence block

`diff -w BASE CAND` gives 16 hunks (CAND lines: 23, 43, 52, 61-64, 73, 83, 87, 92, 116, 147, 159, 172 plus new 178-182, 186-189, 199-200, 204-205). The changed lines, copied verbatim (BEFORE = diff lines starting `<`, AFTER = diff lines starting `>`):

### BEFORE (baseline)

```text
< | E3 | It has worked before: in the codegraph planning run, Orca workers invoked `/sc:adversarial`, and that work landed as PR #329. | `.dev/codegraph-migration/orchestration/README.md:31,33`; `.dev/orca-command-refactor/README.md:12`; return contract `invocation_method: "skill-direct"` at `.dev/codegraph-migration/decisions/P3-command-set/adversarial/return-contract.yaml:10` |
< 1. **No command in scope has been run end to end as an Orca worker in this run.** Every verdict in both inventories comes from reading files (`INV-B:323`). The only end-to-end proof is the PR #329 run, and its brief told workers to run `/sc:adversarial` through an Agent-tool subagent (`.dev/codegraph-migration/orchestration/README.md:31`), so it proves the nested route, not the direct route this spec requires. Whether every such spawn succeeded is UNVERIFIED (`CAPS:156`, `CAPS:187`). Phase 0 (section 6) therefore starts with live smoke runs.
< - **Contract file**: one shared document, proposed as `src/superclaude/core/WORKER-CONTRACT.md`, installed to `~/.claude/WORKER-CONTRACT.md`. Core `.md` files install to `~/.claude/` (`src/superclaude/cli/install_core.py:4,33`; `CLAUDE.md:83,408`), and the new name must be added to `KNOWN_CORE_FILES` (`src/superclaude/cli/install_core.py:13-24`). Each changed command adds a short `## Unattended mode` section that lists only its own gate resolutions and report file and points to the installed contract path, so the shared rules are written once.
< | WC-3 | **Questions go to the coordinator, not to a local prompt.** When a gate would resolve as blocked and the worker session holds a preamble, the session may instead ask the coordinator once with the preamble's `ask` command, wait, then re-invoke or resume the command with the answer as a flag. On an `ask` timeout it resumes the same message ID and never creates a duplicate. No heartbeat is sent while blocked in `ask`. | Worker session | `CAPS:58-61` (`[H:ask]` lines 3-5, 23-24; `[G]` lines 80-82); `CAPS:64` (`[G:worker-contract]` lines 10-11) |
< | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
< | WC-5 | **Outcome mapping.** The worker sends `worker_done` exactly once from its own top-level session. `--outcome failed` when the report says `failed` or `blocked`, or no report exists; `--outcome succeeded` otherwise, including `partial` and including an audit whose verdict is FAIL (the audit itself succeeded). The first sentence of the body states the report's status and verdict. | Worker session | `CAPS:73` (`[G]` lines 88-90, "Never encode failure only in prose"); `CAPS:76-77` |
< | WC-6 | **Resume or safe re-run.** A retry worker (`worker-start --retry-of`) must not corrupt the first attempt's output. A command either resumes from its on-disk state when given its resume flag, or, if it has none, writes each run into a fresh output directory so a re-run starts clean. Section 3 names which applies per command. | Command | `CAPS:116` (retry and circuit breaker); resume mechanisms in column (e) of `INV-A:35-55`, `INV-B:31-52` |
< The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
< | adversarial | `--output <dir>`; never `--interactive` | contract, but filename not fixed | `--pipeline-resume` (pipeline mode only); else fresh dir | Fix the contract filename to `<output>/adversarial/return-contract.yaml` (P1) | `sk/sc-adversarial-protocol/SKILL.md:427-429,605,1908,2806-2833`; `INV-A:35,60-61` |
< | init-lite | `--output <file>` | `.dev/superclaude/context-audit.md` or `--output` | Re-run overwrites its marked report | None | `cmd/init-lite.md:32`; `sk/sc-init-lite-protocol/SKILL.md:66,70`; `INV-A:55` |
< | workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | Write the contract for pre-creation STOPs too (WC-4 "every outcome") (P1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
< | research | `--unattended` pins `--strategy planning` (the strategy that runs without clarification) | contract naming the generated `claudedocs/research_*.md` path | fresh file | none | `cmd/research.md:25,103,123-132`; `src/superclaude/agents/deep-research-agent.md:40-56`; `INV-B:38,127-135` | P2 |
< | SA-2 | No command, skill or agent file runs an `orca` or `orca-ide` command, and none requires Orca to be installed or running. The only allowed mention of Orca in a changed command is as an example of a caller's question channel inside the contract file. | Commands run in other projects (`CLAUDE.md:74`); without Orca the calls fail with `runtime_unavailable` (`CAPS:147`). | `CAPS:145-149`; today's baseline: only `sk/ccsession-tag/` mentions Orca (section 1.2, E5) |
< | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
< | AC-C1 | `grep -rnE '\borca(-ide)?[[:space:]]+(orchestration\|worktree\|terminal\|agent)\b' src/superclaude/commands src/superclaude/skills src/superclaude/agents src/superclaude/core \| grep -v '^src/superclaude/skills/ccsession-tag/'` | prints nothing (SA-2, WC-8) |
< 2. While it runs, `ORCA orchestration worker-show --dispatch <dispatch_id> --json` at least once per 5 minutes. **Pass:** `observation.agentWait` is never non-null (a non-null value means the worker is parked on a prompt only a person can answer, `[H:worker-show]` Notes).
< 3. `ORCA orchestration check --wait --types "worker_done,escalation,question" --timeout-ms 900000 --json` until `worker_done` arrives. **Pass:** exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path.
< 4. `test -s <contract>` and `uv run python -c "import sys, yaml; d = yaml.safe_load(open(sys.argv[1])); assert d['status'] in {'succeeded','partial','failed','blocked'}; assert d['command']" <contract>` (PyYAML is a declared dependency, `pyproject.toml:38`). **Pass:** both exit 0.
< 5. `ORCA orchestration worker-read --dispatch <dispatch_id> --source transcript --json` and search the transcript for `AskUserQuestion`. **Pass:** no `AskUserQuestion` call.
< | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1. Record the results in the phase report; a failure here reopens section 1 |
< | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
< | P2 | AC-2.1 | `test_worker_contract.py` gains one assertion per gate listed in the section 3 row, for example the auggie-review section names both `--no-post-pr` and `--no-remediation-offer` | passes |
< | P2 | AC-2.2 | Gate-trigger run per P2 command: a 7.2 live check with input that hits the gate (for example `/sc:tdd "auth" --unattended --output <file>` with a bare topic; `/sc:cli-eval run --unattended` with no `--suite`) | `worker_done --outcome failed`; contract `status: blocked` with a non-empty `blocked_question`; step 2 never shows `agentWait` |
```

### AFTER (candidate)

```text
> | E3 | It has worked before: in the codegraph planning run, Orca workers invoked `/sc:adversarial`, and that work landed as PR #329. | `.dev/codegraph-migration/orchestration/README.md:31,33`; `.dev/orca-command-refactor/README.md:12`; return contract `invocation_method: "skill-direct"` (route UNVERIFIED, section 1.4 (1)) at `.dev/codegraph-migration/decisions/P3-command-set/adversarial/return-contract.yaml:10` |
> 1. **No command in scope has been run end to end as an Orca worker in this run.** Every verdict in both inventories comes from reading files (`INV-B:323`). The only end-to-end proof is the PR #329 run. Its brief told workers to run `/sc:adversarial` through an Agent-tool subagent (`.dev/codegraph-migration/orchestration/README.md:31`), but its return contract records `invocation_method: "skill-direct"` (E3); which route ran is UNVERIFIED (both files are outside this workspace), so the direct route this spec requires is not shown to work. Whether every such spawn succeeded is UNVERIFIED (`CAPS:156`, `CAPS:187`). Phase 0 (section 6) therefore starts with live smoke runs.
> - **Contract file**: one shared document, proposed as `src/superclaude/core/WORKER-CONTRACT.md`, installed to `~/.claude/WORKER-CONTRACT.md`. Core `.md` files install to `~/.claude/` (`src/superclaude/cli/install_core.py:4,33`; `CLAUDE.md:83,408`), and the new name must be added to `KNOWN_CORE_FILES` (`src/superclaude/cli/install_core.py:13-24`). Each changed command adds a short `## Unattended mode` section that lists only its own gate resolutions and report file and points to the installed contract path, so the shared rules are written once. The section sits in the command file; each gate it lists is edited where the gate is written, in the command file or its activated skill.
> | WC-3 | **Questions go to the coordinator, not to a local prompt.** When a gate would resolve as blocked and the worker session holds a preamble, the session may instead ask the coordinator once with the preamble's `ask` command, wait, then re-invoke or resume the command with the answer as a flag, except where the command's section 3 row says to stop (implement's Ruling gates, D2). On an `ask` timeout it resumes the same message ID and never creates a duplicate. No heartbeat is sent while blocked in `ask`. | Worker session | `CAPS:58-61` (`[H:ask]` lines 3-5, 23-24; `[G]` lines 80-82); `CAPS:64` (`[G:worker-contract]` lines 10-11) |
> | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes the contract at the path the brief fixes: `<output-dir>/return-contract.yaml` when `--output` / `--output-dir` names a directory, or `<file>.return-contract.yaml` beside the file when `--output` names a file (tdd, init-lite). A command with no output option gets one in its section 3 row. It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`; an existing status field with other values is kept under its own name), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
> | WC-5 | **Outcome mapping.** The worker sends `worker_done` exactly once from its own top-level session. `--outcome failed` when the contract is absent, empty or unparseable, has no `status` or a value outside the four, or says `failed` or `blocked`; `--outcome succeeded` only when `status` is `succeeded` or `partial`, including an audit whose verdict is FAIL (the audit itself succeeded). The first sentence of the body states the report's status and verdict. | Worker session | `CAPS:73` (`[G]` lines 88-90, "Never encode failure only in prose"); `CAPS:76-77` |
> | WC-6 | **Resume or safe re-run.** A retry worker (`worker-start --retry-of`) must not corrupt the first attempt's output. A command either resumes from its on-disk state when given its resume flag, or, if it has none, writes each run into a fresh output directory so a re-run starts clean. The coordinator's brief gives every attempt, each `--retry-of` retry included, its own new output directory or file path (section 2.3). Section 3 names which applies per command. | Command | `CAPS:116` (retry and circuit breaker); resume mechanisms in column (e) of `INV-A:35-55`, `INV-B:31-52` |
> The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line, with `--unattended` from Phase 1 on for the commands Phase 1 lists (Phase 0 runs the ready commands without it) and every flag section 3 lists as required; a new output directory or file path for every attempt, retries included (WC-6), so the report path is known before dispatch (WC-4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
> | adversarial | `--output <dir>`; never `--interactive` | contract, but filename not fixed | `--pipeline-resume` (pipeline mode only); else fresh dir | Fix the contract filename to the WC-4 path `<output>/return-contract.yaml` (P1) | `sk/sc-adversarial-protocol/SKILL.md:427-429,605,1908,2806-2833`; `INV-A:35,60-61` |
> | init-lite | `--output <file>` | `.dev/superclaude/context-audit.md` or `--output` | Re-run overwrites its marked report, so each attempt gets its own `--output` path (WC-6) | None | `cmd/init-lite.md:32`; `sk/sc-init-lite-protocol/SKILL.md:66,70`; `INV-A:55` |
> | workflow | `--handoff none`; `--output <dir>` | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | Add `--output <dir>` and write the contract there for pre-creation STOPs too (WC-4 "every outcome"); the package contract is unchanged (P1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |
> | research | `--unattended` pins `--strategy planning` (the strategy that runs without clarification) | add `--output <dir>`; contract there naming the generated `claudedocs/research_*.md` path | fresh file | none | `cmd/research.md:25,103,123-132`; `src/superclaude/agents/deep-research-agent.md:40-56`; `INV-B:38,127-135` | P2 |
> | SA-2 | No command, skill or agent file runs an `orca` or `orca-ide` command, and none requires Orca to be installed or running. No changed command, skill or agent file mentions an Orca command; only the contract file under `src/superclaude/core/` may, as an example of a caller's question channel. | Commands run in other projects (`CLAUDE.md:74`); without Orca the calls fail with `runtime_unavailable` (`CAPS:147`). | `CAPS:145-149`; today's baseline: only `sk/ccsession-tag/` mentions Orca (section 1.2, E5) |
> | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag and `## Unattended mode` section on the commands listed here and no others (a no-op where a command has no gate), so a gated command does not accept the flag before its gate resolves in P2-P4; output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, brainstorm, init-lite, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
> | AC-C1 | The command in the block below the table | prints nothing (SA-2, WC-8) |
> AC-C1 command (L2):
> ```bash
> grep -rnE '\borca(-ide)?[[:space:]]+(orchestration|worktree|terminal|agent)\b' src/superclaude/commands src/superclaude/skills src/superclaude/agents | grep -v '^src/superclaude/skills/ccsession-tag/'
> ```
> 
> 2. While it runs, `ORCA orchestration worker-show --dispatch <dispatch_id> --json` at least once per 5 minutes. **Pass:** every read returns `observation.agentWait: null`. A non-null value means the worker is parked on a prompt only a person can answer (`[H:worker-show]` Notes); an absent field means Orca never looked and does not pass (`CAPS:129`).
> 3. `ORCA orchestration check --wait --types "worker_done,escalation,question" --timeout-ms 900000 --json` until `worker_done` arrives. **Pass:** exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path (P0: AC-0.4).
> 4. `test -s <contract>` and `uv run python -c "import sys, yaml; d = yaml.safe_load(open(sys.argv[1])); assert d['status'] in {'succeeded','partial','failed','blocked'}; assert d['command']" <contract>` (PyYAML is a declared dependency, `pyproject.toml:38`). **Pass:** both exit 0 (P0: AC-0.4).
> 5. `ORCA orchestration worker-read --dispatch <dispatch_id> --source transcript --json` and search the transcript for `AskUserQuestion` and for an Agent-tool call whose prompt carries the `/sc:` command line. **Pass:** neither found (WC-2, WC-7).
> | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, checked in step 5) | steps 1, 2 and 5-7 pass. The P0 runs have no contract, so step 3 requires exactly one `worker_done` with `--outcome succeeded` and the section 3.1 "Report today" file as its report path, and step 4 is only `test -s` on that file. Record the results in the phase report; a failure here reopens section 1 |
> | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command section 6 lists for P1, except `/sc:load`, has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that `/sc:load` and no section-4 command has one | passes |
> | P2 | AC-2.1 | `test_worker_contract.py` gains one assertion per gate listed in the section 3 row, for example the auggie-review section names both `--no-post-pr` and `--no-remediation-offer`, read in the file (command or skill) where the gate is written | passes |
> | P2 | AC-2.2 | Gate-trigger run per P2 command: a 7.2 live check with input that hits the gate (for example `/sc:tdd "auth" --unattended --output <file>` with a bare topic; `/sc:cli-eval run --unattended` with no `--suite`), with a brief that forbids `ask` | `worker_done --outcome failed`; contract `status: blocked` with a non-empty `blocked_question`; step 2 never shows `agentWait` |
```

Self-check (run): each of the 28 AFTER lines (without `>`) was found with `grep -F` in CAND, and each of the 23 BEFORE lines (without `<`) in BASE; 0 misses either way. Roles are not swapped. The diff is not empty.

## Prior blocking findings

round1.md:260 names the blocking ids L1, L2, L16 (round1.md:14-15, 29). Each is decided by comparing its defect with the AFTER text only.

| id | prior defect | status | deciding AFTER text |
|---|---|---|---|
| L1 | Contract-path, flag-timing, retry, outcome-mapping and P0 check defects (cluster of 40 sub-claims, round1.md:35-197) | resolved | see the sub-claim table below |
| L2 | AC-C1 grep over `core` fails on the P0 Orca text, and its `\|` never matches under `grep -E` (round1.md:218-232) | resolved | CAND:172, CAND:178-182, CAND:147 |
| L16 | Section 1.4 says PR #329 is the only proof and no direct run was seen, while E3 cites a skill-direct contract (round1.md:238-240) | resolved | CAND:23, CAND:43 |

### L2 check
- The grep moved out of the table cell into a fenced block (CAND:178-182), so the pipes are plain ERE alternation. I ran the same pattern with `grep -nE` on sample lines: `orca worktree create` and `orca-ide orchestration ask` match, `orca-ide skills get` does not. Under `grep -r` the output lines start with the path, so `grep -v '^src/superclaude/skills/ccsession-tag/'` works.
- `src/superclaude/core` is no longer scanned (CAND:179 vs BASE:172), and SA-2 now lets only the contract file under `core/` name an Orca command (CAND:147). The P0 contract file and the routing-guide Orca section can no longer fail AC-C1 by construction. Resolved.

### L16 check
- E3 now marks the route UNVERIFIED and points to 1.4 (1) (CAND:23). Section 1.4 (1) says the brief told workers to use an Agent-tool subagent, the return contract records `skill-direct`, and "which route ran is UNVERIFIED" (CAND:43). The two statements no longer disagree; neither claims a direct run was seen. INV-A:35 calls the same run "proven" direct; the spec is the more cautious reading and is internally consistent. Resolved.

### L1 sub-claims (round1.md ids; "F" = reviewer finding number)

| sub-claim | outcome | evidence |
|---|---|---|
| t1b-1 F1 adversarial contract one level too deep | resolved | CAND:83 now `<output>/return-contract.yaml` = the WC-4 path (CAND:62) |
| t1b-1 F2 AC-1.1 requires a contract section in `/sc:load` | resolved | CAND:200 excludes `/sc:load`; CAND:112 and CAND:270 keep it without a report |
| t1b-1 M2, t2-1 F6, t3-1 F2 retry overwrites first attempt | resolved | CAND:64, CAND:73 (coordinator supplies a new path per attempt), CAND:87 (init-lite) |
| t1b-1 M3, t2-1 F12 flag accepted on gated commands before the gate exists | resolved | CAND:159 (flag and section only on the listed P1 commands, "and no others") |
| t1b-1 M4, t3-1 F8 pre-creation STOP and run-time paths (workflow, research) | resolved | CAND:92 (`--output <dir>`), CAND:116 (`--output <dir>`), CAND:62 |
| t2-1 F1, t3-2 F2 `--unattended` required in P0 briefs | resolved | CAND:73 ("Phase 0 runs the ready commands without it") |
| t2-1 F3, t3-1 F9, t3-2 F1 missing/unknown status maps to succeeded | resolved | CAND:63 (`failed` unless `status` is `succeeded` or `partial`) |
| t2-1 F7, t3-1 F1 AC-0.4 cannot pass on REPORT.md | resolved | CAND:199 (step 3 and step 4 rewritten for P0); two residual gaps are N1 and N3 below |
| t2-1 F8 optional ask makes AC-2.2 non-deterministic | resolved | CAND:205 ("with a brief that forbids `ask`") |
| t2-1 F13 flag does not reach the skills where gates live | resolved | CAND:52 (gate edited "in the command file or its activated skill"), CAND:204 |
| t2-1 F16 absent `agentWait` passed | resolved | CAND:186 (absent does not pass; CAPS:129 confirms absent = Orca never looked) |
| t3-1 F3 tdd contract at `<file>/return-contract.yaml` | resolved | CAND:62 (`<file>.return-contract.yaml`) |
| t3-1 F4 implement Ruling relayed through `ask` | resolved | CAND:61 (exception for the implement Ruling gates), CAND:109 |
| t3-1 F5 brainstorm gets no Unattended section | resolved | CAND:159 lists brainstorm and init-lite; CAND:200 asserts them |
| t3-2 F4 no-wrapper rule not checked in step 5 | resolved | CAND:189 (step 5 also searches for an Agent-tool call carrying the `/sc:` line) |
| t1b-1 M5 existing contract status vocab may leave the four values | partly addressed, now N4 | CAND:62 adds "kept under its own name"; the result is ambiguous, and the real vocabularies are outside the workspace (INV-B:272 gives the keys only) |
| t2-1 F15, t3-1 F11 no coordinator policy for a missing `worker_done`, an unanswered ask, no cap | not changed, now N8 | requirement the document never states, not a stated text that does harm |
| t3-1 F10 no order between contract write and `worker_done` | not changed, now N8 | the worker sends `worker_done` after the command finishes (CAND:63, CAND:62); needs a guess to be wrong |
| t3-1 F12 no rule when `~/.claude/WORKER-CONTRACT.md` is missing | not changed, now N8 | missing requirement |
| t2-1 F17 no schema version, F18 two sources of truth | not changed, now N8 | missing requirement; WC-5 (CAND:63) now fixes the mapping |
| t2-1 F9 unattended run with no output directory | reworded; remainder is N2 | CAND:62 "the path the brief fixes"; CAND:73 makes the brief carry it |
| t3-1 F13 spec-panel row looks stale | unchanged, N7 | UNVERIFIED which command copy is current |

Why L1 is `resolved` and not `open`: every sub-claim that names a stated text producing a wrong outcome (the contradictions, the unpassable checks, the retry overwrite, the succeeded-on-failure mapping, the wrong contract path) is repaired in the AFTER text. The sub-claims the reviser left untouched are requirements the document never states (policy for timeouts, a schema version, a missing core file). Under the grading rule those are Medium, not blocking, and they appear below as N8. No sub-claim regressed.

## REQUIREMENTS ANALYSIS (Wiegers, Adzic, Cockburn; changed lines)

### N1. AC-0.4 and WC-5 give opposite outcomes for a P0 run (Medium; Wiegers, Adzic)
- WC-5 sets `--outcome failed` "when the contract is absent" (CAND:63). AC-0.4 says "The P0 runs have no contract, so step 3 requires ... `--outcome succeeded`" (CAND:199). The P0 brief template comes from the contract file written in P0 (CAND:158), so a worker briefed from WC-5 sends `failed` for a troubleshoot run that wrote only REPORT.md.
- Grade: Medium. AC-0.4 names itself as the P0 exception, so an implementer can read the pair consistently; the text just does not say that WC-5 yields to AC-0.4 before P1.
- Whittaker (divergence attack): I can break this specification by the **Divergence Attack**. The invariant at **WC-5 vs AC-0.4** fails when **the command ran correctly in P0 and wrote REPORT.md**. Concrete attack: before, worker holds REPORT.md and no contract; after, WC-5 sends `failed`, AC-0.4 step 3 expects `succeeded`, so the gate fails on correct work.
- Origin: changed (both lines).

### N2. WC-4 promises an output option that two ready rows never give (Medium; Wiegers)
- WC-4: "A command with no output option gets one in its section 3 row." (CAND:62). The cleanup-audit row says "output dir is fixed" and only names the final report (CAND:85); index-repo only "State the output location" (CAND:86). INV-A:42 and INV-A:53 confirm neither has an output option and that the contract location is open. Several 3.2 rows (save CAND:119, task CAND:121, review-translation CAND:117) also name no contract path.
- Both cleanup-audit and index-repo are in the P1 command list (CAND:159) and so are covered by AC-1.1 (CAND:200); AC-1.2 runs each P1 command "with `--unattended --output <dir>`" (CAND:201), an option those two do not have. An implementer must invent the contract path.
- Grade: Medium. The P1 list says "fixes to" for these four, which can also be read as not adding the flag; the text allows both readings. Origin: changed (WC-4 sentence, CAND:159).

### N3. AC-0.4 step 3 compares against a file that is not fixed (Medium; Adzic)
- Step 3 requires the report path to be "the section 3.1 \"Report today\" file" (CAND:199). For adversarial that cell says "contract, but filename not fixed" (CAND:83; INV-A:35 and INV-A:60 report two different on-disk paths). For workflow it is `.dev/tasks/to-do/<id>/return-contract.yaml` with a run-time `<id>` (CAND:92). The coordinator cannot state the expected path before dispatch for those two P0 runs.
- Grade: Medium; the coordinator can read the output directory afterwards. Origin: changed (CAND:199).

### N4. "Kept under its own name" cannot hold for a field that is already named `status` (Medium; Wiegers)
- WC-4 says an existing status field with other values "is kept under its own name" (CAND:62) while the same row requires a `status` key in the four values, and WC-5 sends any other value to `failed` (CAND:63). Workflow's contract already has a key `status` (INV-B:272). If its values are outside the four, the two rules cannot both hold, and 7.2 step 4 would assert on the wrong vocabulary (CAND:188). The actual values are in a file outside the workspace: UNVERIFIED.
- Grade: Medium (depends on the unseen vocabulary). Origin: changed.

## ARCHITECTURE ANALYSIS (Fowler, Nygard, Whittaker; changed lines)

### N5. Section 3.1 still says only the last column changes commands (minor)
- "The only command changes are the small fixes in the last column" (CAND:79) while P1 adds the flag and section to brainstorm and init-lite (CAND:159), whose small-fix cells read "None" (CAND:84, CAND:87). Section 2.3 also states when to pass `--unattended` only for "the commands Phase 1 lists" (CAND:73) and is silent for P2-P4 commands, which AC-2.2 then runs with the flag (CAND:205). Origin: changed. Note only.

### N6. Workflow keeps two contracts (minor)
- The workflow row adds a `<dir>` contract "for pre-creation STOPs too" and says "the package contract is unchanged" (CAND:92). Whether the `<dir>` file is also written on post-creation outcomes, and what it holds, is not said. WC-4 says the worker passes the contract path, so the report path is the `<dir>` file (CAND:62). Origin: changed. Note only.

### N7. spec-panel row may be stale (minor, UNVERIFIED)
- The row asks to "add `--output`" and make `target_release` a flag (CAND:120). The command definition supplied with this task already has `--output <file>`, `--target-release`, `--improve`, `--unattended`, `--report-dir` and its own contract (command.md:22-23, 455-465). Whether `cmd/spec-panel.md` in the spec's repo equals this file is UNVERIFIED. If it does, the WC-4 rule that file-valued `--output` is only tdd and init-lite (CAND:62) misses it. Origin: unchanged; it quotes the changed WC-4 line, so it is listed. Note only.

### N8. Carried-over missing requirements from L1 (minor, origin=unchanged)
- No cap on `ask` retries and no coordinator action for a missing `worker_done`, a parked worker or a `check` timeout (CAND:61; CAND:187); no order between writing the contract and `worker_done` (CAND:62-63); no rule if `~/.claude/WORKER-CONTRACT.md` is not installed (CAND:51-52); no contract schema version (CAND:62). Each is a requirement never stated, none a stated text that does harm.

### N9. A fresh path per attempt sits beside resume flags (minor)
- WC-6 now makes the brief give "every attempt ... its own new output directory or file path" (CAND:64, CAND:73), while many rows resume from on-disk state (`--resume`, `--resume-from`, ledger, `progress.json`; CAND:84, CAND:85, CAND:109, CAND:105). How a resume attempt reaches the earlier state in a new directory is not stated, and commands with a fixed output directory cannot take a new one (CAND:85). Origin: changed. Note only.

## Guard Condition Boundary Table (re-review: guards on changed lines only)

Classes not listed for a guard cannot occur for it; the reason is given in the last column of the note below the table.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| outcome mapping | WC-5 (CAND:63) | Zero/Empty | empty or unparseable contract | true (failed) | `--outcome failed` | OK |
| outcome mapping | WC-5 (CAND:63) | Sentinel Value Match | `status` outside the four | true (failed) | `failed`; conflicts with WC-4 "kept under its own name" for workflow (N4) | GAP |
| outcome mapping | WC-5 (CAND:63) | Legitimate Edge Case | P0 run with REPORT.md and no contract | true (failed) | WC-5 says `failed`; AC-0.4 says `succeeded` (N1) | GAP |
| contract path | WC-4 (CAND:62) | Zero/Empty | no output option, none given in the row | unspecified | cleanup-audit, index-repo (N2) | GAP |
| contract path | WC-4 (CAND:62) | Typical | `--output` names a directory | true | `<output-dir>/return-contract.yaml` | OK |
| contract path | WC-4 (CAND:62) | Legitimate Edge Case | `--output` names a file | true | `<file>.return-contract.yaml` | OK |
| agentWait check | 7.2 step 2 (CAND:186) | Zero/Empty | field absent | false | does not pass | OK |
| agentWait check | 7.2 step 2 (CAND:186) | Typical | `null` | true | passes | OK |
| agentWait check | 7.2 step 2 (CAND:186) | Maximum/Overflow | non-null | false | worker parked on a prompt, fails | OK |
| flag acceptance | P1 row (CAND:159) | Typical | command in the P1 list | true | flag and section added | OK |
| flag acceptance | P1 row (CAND:159) | Legitimate Edge Case | command named only as "fixes to" | unspecified | adversarial, cleanup-audit, index-repo, workflow (N2) | GAP |
| fresh path per attempt | WC-6 (CAND:64) | Maximum/Overflow | retry of a command with a fixed output dir | unspecified | cleanup-audit (CAND:85) (N9) | GAP |
| AC-C1 grep | CAND:178-182 | Zero/Empty | no match | true | prints nothing = pass | OK |
| AC-C1 grep | CAND:178-182 | Sentinel Value Match | `ccsession-tag` path | excluded | `grep -v` removes it | OK |

Left out: AC-C1 One/Minimal and Maximum (a single or very many matches print the same); agentWait Sentinel (the field has three states, all listed). GAP rows are graded under FR-8: each names no concrete wrong outcome an implementer would produce without a guess, so each is Medium and sits under follow-up candidates. FR-9 (blank behavior): the two "unspecified" entries are the same N2 and N9 findings. FR-10: the table is complete for the changed guards; it does not cover unchanged guards, by the re-review scope rule.

Pipeline Dimensional Analysis: not triggered (the spec describes no data pipeline whose stage counts differ). `--focus correctness` was not requested, so no State Variable Registry is produced.

## Coverage

Covered: all 16 diff hunks; the three prior blocking ids and all 40 round-1 sub-claims under L1, L2 and L16 (round1.md:33-240); the dependencies of the changed lines (WC-4 to WC-6, section 2.3, AC-0.4, AC-1.1, AC-1.2, AC-C1, 7.2 steps 2-5, P1 row, 3.1 rows adversarial, init-lite, workflow, research, section 1.4 and E3); the INV-A and CAPS lines those changes quote (INV-A:35,42,53,60; INV-B:272; CAPS:129). Not covered: unchanged text beyond the dependencies above; every citation into `src/`, `.claude/`, `CLAUDE.md` and `.dev/codegraph-migration/` (UNVERIFIED here); whether Orca behaves as the spec expects (no live run exists in this sandbox).

New severe defect found that is older than the revision: none.

## Follow-up candidates (Medium and minor; none blocks)

Medium: N1, N2, N3, N4. Minor: N5, N6, N7, N8, N9. These never trigger a revision. The coordinator's session asks the user once whether to open an issue for them; this worker asked nobody and created no issue.

## Findings block

```findings-v1
{"id": "N1", "severity": "MAJOR", "blocking": false, "category": "contradiction", "anchor": "The P0 runs have no contract, so step 3 requires exactly one `worker_done` with `--outcome succeeded`", "anchor2": "`--outcome failed` when the contract is absent, empty or unparseable", "refs": ["WC-5", "AC-0.4"], "claim": "WC-5 sends a P0 run with no contract to failed while AC-0.4 requires succeeded, and the spec never says WC-5 yields before P1."}
{"id": "N2", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "A command with no output option gets one in its section 3 row.", "anchor2": "Name the `--pass all` final report; output dir is fixed, so one audit per worktree at a time (WC-11) (P1)", "refs": ["WC-4", "AC-1.1", "AC-1.2", "P1"], "claim": "cleanup-audit and index-repo are P1 commands with no output option and no contract path, so an implementer must invent the path and AC-1.2's --output <dir> run cannot be issued."}
{"id": "N3", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "the section 3.1 \"Report today\" file as its report path", "anchor2": "contract, but filename not fixed", "refs": ["AC-0.4", "3.1"], "claim": "The P0 step 3 expected report path is undefined for adversarial and has a run-time id for workflow, so the coordinator cannot state it before dispatch."}
{"id": "N4", "severity": "MAJOR", "blocking": false, "category": "contradiction", "anchor": "an existing status field with other values is kept under its own name", "anchor2": "has no `status` or a value outside the four", "refs": ["WC-4", "WC-5"], "claim": "A contract that already has a key named status with other values cannot be kept as is and also satisfy the four-value status the checks assert (vocabulary UNVERIFIED)."}
{"id": "N5", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "The only command changes are the small fixes in the last column.", "anchor2": "section on the commands listed here and no others", "refs": ["3.1", "P1", "2.3"], "claim": "Section 3.1 says only the last column changes commands while P1 adds the section to brainstorm and init-lite, and section 2.3 is silent on --unattended for P2-P4 commands."}
{"id": "N6", "severity": "MINOR", "blocking": false, "category": "missing-requirement", "anchor": "the package contract is unchanged (P1)", "refs": ["WC-4"], "claim": "Workflow ends with two contracts and the spec does not say what the new one holds on post-creation outcomes."}
{"id": "N7", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "`target_release` required as a flag for TDD inputs, else blocked; the improved-spec step stays off unless the brief asks", "refs": ["WC-4", "3.2"], "claim": "The spec-panel row may be stale against a command that already has --output <file>, --target-release, --improve and its own unattended section (copy currency UNVERIFIED)."}
{"id": "N8", "severity": "MINOR", "blocking": false, "category": "missing-requirement", "anchor": "On an `ask` timeout it resumes the same message ID and never creates a duplicate.", "refs": ["WC-3", "WC-4", "2.1"], "claim": "No cap on ask retries, no coordinator action for a missing worker_done, no write-before-report order, no rule for a missing contract file and no schema version."}
{"id": "N9", "severity": "MINOR", "blocking": false, "category": "missing-requirement", "anchor": "its own new output directory or file path (section 2.3)", "refs": ["WC-6", "2.3"], "claim": "A new path per attempt is not reconciled with resume flags or with commands whose output directory is fixed."}
{"prior": "L1", "status": "resolved"}
{"prior": "L2", "status": "resolved"}
{"prior": "L16", "status": "resolved"}
```

scoped PASS: changed lines + prior blockers

Reviser brief: none. No blocking finding is open; Medium and minor findings are not briefed.

verdict: PASS
