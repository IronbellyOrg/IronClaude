# Research Notes: Issue-to-work pipeline (IronClaude, origin/master 61ac2c2e6)

**Date:** 2026-11-20
**Scenario:** A (explicit request from team-lead: files, packages, docs and output path all named)
**Depth Tier:** Standard (requested by team-lead; scope is cross-cutting, so the 6-agent top of the Standard band is used and the line target is allowed to run to about 1,300 lines plus the removed-code appendix; recorded here as a deliberate tier decision, not a downgrade)
**Status:** Complete

**SOURCE ROOT (READ-ONLY, all agents):** `/home/coder/.cache/ic-snap-20261120/master` (export of origin/master 61ac2c2e6, same layout as the repo root). Every path below is relative to it unless it starts with `/`. Removed-code appendix only: `git -C /home/coder/workspaces/IronClaude show 01e7a9e23^:<path>` (read-only).
**Task folder:** `/home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-issue-pipeline-20261120-040158/`
**Final output:** `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/techref/ISSUE-TO-WORK-PIPELINE-TECHNICAL-REFERENCE.md`
**Per-slice scope-discovery files (detail, with file:line and doc-vs-code tables):** `${TASK_DIR}scope/scope-1-cycle-runner-cli.md`, `scope-2-github-predicates-audit.md`, `scope-3-launch-record.md`, `scope-4-sc-issue-claim.md`, `scope-5-launch-guard-ccsession.md`, `scope-6-coordinator-removed.md`. Research agents MUST read the scope file(s) of their area first and then verify against code (scope files are hints, code wins).

Out of scope (state in one sentence in the final document): PR 686 and the Clay rewrite design. Do not describe them anywhere.

---

## EXISTING_FILES

### Watcher package `src/superclaude/cli/issue_watch/` (4,389 lines in 8 modules; registered at `src/superclaude/cli/main.py:577-579` as `issue-watch`)
| File | Lines | Role |
|---|---|---|
| `cycle.py` | 1406 | Config and validators (l.34-483), one poll cycle `_Cycle` (l.485-1222), status report and SLO reducer (l.1225-1406). Constants l.34-47 (`MAX_CANDIDATES=10`, `DAY_CAP=6`, deadlines 240 s, `SKEW_WARN_S=60`...). `MAX_LAUNCHES_PER_CYCLE` is a dead constant. |
| `github.py` | 960 | 7 read-only `gh` calls (G1-G7), `CallBudget` (35 calls, 3 reserved), rate-limit handling, `REPO="IronbellyOrg/IronClaude"` l.37. Never writes to GitHub. |
| `record.py` | 865 | `FileStore`: `state_dir/dispatch.json` (17 fields per entry, 6 states, transitions T-1..T-13), flock, atomic write, pending-before-launch, DISABLED file, dry-run shadow. |
| `launch.py` | 370 | One fixed command: `orca agent launch --agent claude --worktree path:<abs> --surface terminal --prompt "/sc:issue --claim <N> --pipeline none" --json` (12-element argv, l.95-116). Creates no worktree. |
| `predicates.py` | 312 | Pure eligibility checks (`approval_of`, `eligibility_order`, `is_intended_owner`, `unchanged_since`, `project_check`). |
| `audit.py` | 404 | `audit.jsonl` writer, `REASON_TABLE` (59 reasons, l.24-96), rotation 5 MiB x 4. |
| `cli.py` | 348 | Click group `issue-watch`, 5 verbs: `once [--dry-run]`, `status [--json]`, `check-config`, `init-state`, `reset ISSUE --forfeit-guarantee | --rate-limit`. Exit codes 0/1/2/3/4/5/6/7/75. |
| `runner.py` | 130 | Only module importing `subprocess`; `shell=False`, stderr cap 500 bytes. |
| Design docs | 942 + 706 | `docs/designs/issue-watcher.md` (status line says merged in PRs #447/#448, never run live, `enabled` ships false, no schedule installed) and `docs/designs/issue-watcher-setup.md` (owner runbook). |

### `/sc:issue --claim` flow
| File | Lines | Role |
|---|---|---|
| `src/superclaude/commands/issue.md` | 117 | Command file. |
| `src/superclaude/skills/sc-issue-protocol/SKILL.md` + `refs/{claim,create,chains,tiers,labels}.md` | 197 + 414 | Orchestrator protocol; default pipeline level chosen by prose at `refs/claim.md:81`, no code. |
| `.../scripts/orca_worktree.py` | 1906 | Worktree create/reuse, launch, IR-4 enforcement preflight, L2 install (`install_l2`/`l2_status`), `publish_pending` (l.1488-1512), `cmd_pending` (l.1515-1523), shim check. `IR7_REFUSE = False` (l.822). |
| `.../scripts/clickup_claim.py` 270, `origin_repo.py` 195 | | ClickUp claim and origin-repo resolution. |
| `.../templates/` (17 files) | | claim-comment, accuracy-check-comment, issue-summary, next-steps, launch-prompt etc. |
| `src/superclaude/agents/issue-worker-t{1,2,3}.md` | | Tier-pinned workers (design says T3 = `claude-gw-tier3`, agent file pins `claude-gw-tier2b`: stale doc). |
| Design docs | 509 + 470 | `docs/designs/sc-issue-command.md` (status line says "Design only" but code exists: stale) and `sc-issue-claim-pipeline-flag.md`. |
| `--pipeline` levels (code) | | `worktree`, `full`, `full --submit`, `none`. "L1/L2" in this system mean guard LAYERS, not pipeline levels. |

### Launch-level guard stack
| File | Lines | Role |
|---|---|---|
| `src/superclaude/hooks/scripts/launch-level-guard.sh` | 808 | L1 guard on UserPromptSubmit + PreToolUse; levels W, WA, F, FS stored as files under `~/.claude/state/launch-level/{pending,sessions}`; fail-closed for governed sessions, fail-open for ordinary; plugin copy byte-identical. |
| `.../launch-job-identity.sh` | 582 | PreToolUse(Bash) command rewriter + `identify` (job identity for Linux same-user). |
| `.../launch-level-pre-push.sh` | 208 | L2 git pre-push hook template (installed by the claim, not registered in hooks.json). |
| `src/superclaude/hooks/hooks.json` 192, `src/superclaude/cli/install_hooks.py` 614 | | Registrations and install (skip-if-exists unless `force`). |
| `src/superclaude/cli/install_ccsession.py` 161, `skills/ccsession-tag/{ccsession,ccsession-orca,hooks/*,unseed-env.py}` | | Launch shim. It carries NO launch level; the claim only DETECTS the shim by screen text or tab title (`orca_worktree.py:792,797`, warning `W-LAUNCH-NOT-CCSESSION`). |
| Design docs | 627, 51, 57, 119 | `sc-issue-launch-level-hook.md`, `issue-pipeline-guard-g2.md`, `issue-pipeline-guard-g2-no-to.md`, `issue-pipeline-fu1.md`. |

### Coordinator duties
`src/superclaude/core/WORKER-CONTRACT.md` (339 lines; WC-2..WC-16; no WC-17; no "Issue pipeline duties" section; only issue-related hits l.23, l.57, l.66, l.241-245).

### Removed on 2026-11-20 (appendix; commit 01e7a9e23 = PR 682, parent holds old files)
`src/superclaude/cli/issue_pipeline/` (10 verbs, 1,597 lines: `approval_line.py` 62, `approval_record.py` 416, `brief.py` 74, `cli.py` 395, `plan_hash.py` 90, `reads.py` 161, `release.py` 66, `stage_predicates.py` 301, `templates/worker-brief.txt` 27, `__init__.py` 5), WC-17 and "Issue pipeline duties", the guard's G2 rule 1 TAMPER case, 116 tests under `tests/issue_pipeline/` plus `tests/cli/test_issue_pipeline_registered.py`, edits to `tests/skills/test_worker_contract.py` and `tests/hooks/test_launch_level_guard_worker.py`.

### Tests that pin behaviour (agents must give a row per file in the reference)
- `tests/issue_watch/` (20 .py files, ~16,900 lines): `conftest.py` 1155, `test_cycle.py` 4982 (237 tests), `test_github.py` 2161, `test_record.py` 2377, `test_cli.py` 1672 (60), `test_security_invariants.py` 1013, `test_no_text.py` 971, `test_launch.py` 952, `test_audit.py` 849, `test_predicates.py` 732, `test_cli_e2e.py` 443, `test_slo_helper.py` 421, `test_module_boundaries.py` 413, `test_crash_injection.py` 373, `test_find_orca_parity.py` 288, `test_concurrency.py` 275, `test_no_shell.py` 266, `test_runner.py` 226, `test_origin_parity.py` 179, `test_marker_contract.py` 53, plus `fixtures/_assumed_shape/*.json` (all reply shapes still assumed: no live-test record exists).
- `tests/hooks/`: `test_launch_level_guard.py` 4631 (162), `_l2_tokens.py` 160, `_registration.py` 127, `_with_identity.py` 212, `_worker.py` 300, `test_launch_job_identity.py` 1530, `test_launch_level_pre_push.py` 1194, `test_launch_level_pre_push_records.py` 230, `test_launch_level_observations.py` 84 (one skipped live test).
- `tests/skills/`: `test_issue_protocol.py` 1055, `test_issue_orca_worktree.py` 2501, `test_issue_l2_install.py` 716, `test_issue_repo_resolution.py` 291, `test_issue_worker_agents.py` 559, `test_issue_t1_fallback.py` 69, `test_worker_contract.py`; `tests/commands/test_issue_command.py` 212; `tests/cli/test_issue_body_templates.py` 97, `test_install_hooks.py`; `tests/unit/test_install_ccsession.py`, `test_ccsession_tag.py`, `test_ccsession_tiers.py`; `tests/core/test_orca_session_launch_guidance.py`.

## PATTERNS_AND_CONVENTIONS
- Closed vocabularies everywhere: reason words (`REASON_TABLE`), exit codes, guard class words (LL-*), warning codes; tests pin closed key sets (`test_no_text.py`: GitHub text never reaches state, argv or prompt).
- Write-ahead state: `pending` is saved durably BEFORE the Orca launch; crash points C1-C5 pinned by `test_crash_injection.py`.
- Single module may import `subprocess` (`runner.py`), enforced by AST tests (`test_no_shell.py`, `test_module_boundaries.py`).
- Hook scripts exit 0 allow / 2 block, never 1; plugin copies under `plugins/superclaude/hooks/` must be byte-identical (pinned by tests).
- Level and identity travel by FILES under `~/.claude/state/launch-level/`, never by env var.
- Doc drift is common: design docs cite older line numbers and removed commands. Code wins; label every doc claim [CODE-VERIFIED] / [CODE-CONTRADICTED] / [UNVERIFIED].

## FEATURE_ANALYSIS
Four cooperating pieces plus a removed fifth:
1. **Watcher** (`issue-watch once`): polls GitHub (read-only) for issues carrying trigger label `issue-watch:trigger` and approval label `issue-watch:approved` applied by an allow-listed approver; launches ONE Orca agent per cycle with `/sc:issue --claim N --pipeline none`; writes only local state. Trigger: only a human or external scheduler running `once`; no scheduler artefact exists in the snapshot; `enabled` defaults to `false`; kill switch DISABLED file.
2. **Claim** (`/sc:issue --claim`): orchestrator skill with tier-pinned workers; the orchestrator performs every GitHub and ClickUp write (assign, comments, summary, next-step prompt), then creates an Orca worktree and launches an agent at the `--pipeline` level, writing a `pending/<nonce>` launch record.
3. **Guard** (L1/L2/identity/G2 rule 2): binds a launched session to its level on first prompt, blocks implement/commit/push/submit classes per level; G2 rule 2 allows a bound worker `orchestration send|ask` only with no `--to`.
4. **Coordinator text** (WORKER-CONTRACT): contains no issue-pipeline duties now; "who starts a worker after a claim" is not defined in the contract (`docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md` l.268 says so).
5. **Removed** (appendix): `issue-pipeline` CLI, approval rows, plan hash, `release-worker`, WC-17.

Built vs not built (to be verified by the agents, then stated in an explicit ledger): built = watcher (disabled, never run live), claim flow, L1, L2, job identity, G2 rule 2. Not built or unwired = G2 rule 1 / route A or B release, any caller of `orca_worktree.py pending`, IR-3 `pipeline.json`, IR-7 refusal (switched off), OB-H1..3 and OB-CTX live observations, dispatcher / cron / `COORD-<RepoName>` coordinator worktree / zero-setup install (not in any file read), live-test record `docs/designs/issue-watcher-live-test.md` (does not exist).

Doc-vs-code contradictions already found (agents must re-verify): issue-watcher.md skew 300 s vs code 60 s; setup doc cites a WORKER-CONTRACT section "Issue pipeline duties" that does not exist; setup doc launch commands omit `--pipeline none`; FU-1 runbook uses the removed `issue-pipeline` commands; G2 line numbers drifted; design IMPL skill list (implement, task, improve, cleanup, spawn, build) vs code (implement|task|cleanup); `sc-issue-command.md` status "Design only"; pipeline-flag design table still names `worktree` default.

## RECOMMENDED_OUTPUTS
Research files (Phase 2, one per agent), `${TASK_DIR}research/`:
- `01-watcher-decision-engine.md`
- `02-watcher-io-github-launch-record.md`
- `03-watcher-operator-surface-and-setup.md`
- `04-claim-flow-and-orca-worktree.md`
- `05-guard-stack-and-ccsession.md`
- `06-coordinator-text-and-removed-code.md`

Synthesis files (Phase 5), `${TASK_DIR}synthesis/` (mapped to the technical_reference_template sections; N/A sections stated with rationale):
- `synth-01-overview-architecture.md` (1 Overview, 2 Architecture: whole-pipeline diagram, built vs not-built ledger)
- `synth-02-directory-dataflow.md` (3 Directory Structure, 4 Data Flow: triggers, state stores, GitHub writes per component)
- `synth-03-subsystem-watcher.md` (5.1 watcher)
- `synth-04-subsystem-claim-guard-coordinator.md` (5.2 claim, 5.3 guard stack and launch levels, 5.4 coordinator text)
- `synth-05-integration-config-tests.md` (8 API & Integration incl. every `gh`/`orca` command, 9 Configuration, 10 Error Handling incl. exit codes, 11 Performance (budgets), test-pin matrix)
- `synth-06-conventions-extension-debt-appendix.md` (12 Conventions, 13 Extension Guide, 14 Tech Debt incl. doc-vs-code contradiction table and unwired/not-built defects, appendix "Removed on 2026-11-20")
Sections 6 State Management and 7 Component Inventory: state stores belong in Section 4 and 5; Section 6 states the three on-disk stores as a table; Section 7 N/A with rationale (not a UI feature).

## SUGGESTED_PHASES
Phase 2 agents (all Code Tracer unless stated; all source under the read-only SOURCE ROOT; each reads its scope file first, then code, and verifies by reading the live lines):

| # | Topic | Type | Files | Output |
|---|---|---|---|---|
| 01 | Watcher decision engine: per-cycle flow, every skip/stop reason, entry-state transitions, exit codes, dry-run vs real, 35-call budget arithmetic, `enabled` gate | Code Tracer | `cycle.py` l.485-1222, `predicates.py`, `audit.py` (`REASON_TABLE`, audit line schema, rotation), `docs/designs/issue-watcher.md` sec 6-8; tests `test_cycle.py`, `test_predicates.py`, `test_audit.py`, `test_marker_contract.py`, `conftest.py` | `research/01-watcher-decision-engine.md` |
| 02 | Watcher I/O: every `gh` call (exact argv, read/write, `--repo`), budget classes, rate limit; launch argv and reply handling; `dispatch.json` schema, states, T-1..T-13, locks, atomic writes, crash recovery, DISABLED, dry-run shadow; who reads `dispatch.json` | Code Tracer + Integration Mapper | `github.py`, `launch.py`, `record.py`, `runner.py`; tests `test_github.py`, `test_launch.py`, `test_record.py`, `test_concurrency.py`, `test_crash_injection.py`, `test_find_orca_parity.py`, `test_origin_parity.py`, `test_runner.py`, `fixtures/` | `research/02-watcher-io-github-launch-record.md` |
| 03 | Watcher operator surface and setup: CLI verbs, config schema and validation, approvers file rules, status and SLO, on-disk layout and modes, runbook-vs-code reconciliation, what a real deployment must provide (scheduler, persisted state_dir) and what is absent (no scheduler, no dispatcher, no live-test record) | Doc Analyst + Code Tracer | `cli.py`, `cycle.py` l.34-483 and l.1225-1406, `docs/designs/issue-watcher.md` sec 4, 7, 10, 14, 18, `docs/designs/issue-watcher-setup.md`, `docs/user-guide/cli-groups.md`; tests `test_cli.py`, `test_cli_e2e.py`, `test_slo_helper.py`, `test_no_shell.py`, `test_no_text.py`, `test_security_invariants.py`, `test_module_boundaries.py` | `research/03-watcher-operator-surface-and-setup.md` |
| 04 | `/sc:issue --claim` end to end: waves and owners, every GitHub and ClickUp write with exact command, STOP and warning codes, `--pipeline` levels and default-level rule, worker tiers, return contract, `orca_worktree.py` (worktree create/reuse, launch argv, IR-4 preflight, L2 install, `publish_pending`, `pending`, shim detection), doc staleness | Code Tracer + Doc Analyst | `commands/issue.md`, `skills/sc-issue-protocol/**`, `agents/issue-worker-t*.md`, `docs/designs/sc-issue-command.md`, `sc-issue-claim-pipeline-flag.md`; tests `test_issue_protocol.py`, `test_issue_orca_worktree.py`, `test_issue_repo_resolution.py`, `test_issue_worker_agents.py`, `test_issue_t1_fallback.py`, `test_issue_l2_install.py`, `test_issue_command.py`, `test_issue_body_templates.py` | `research/04-claim-flow-and-orca-worktree.md` |
| 05 | Guard stack: L1 guard (binding state machine, level matrix with test pin per cell, classifiers, G2 rule 2), job identity, L2 pre-push, hooks.json and installer, ccsession shim coupling, G1/G2/route built-vs-retired ledger, stale-doc list. Run the guard script against 10 sample payloads in a TEMP dir with HOME set to that temp dir (read-only on the snapshot; never touch the real ~/.claude) to turn reading into observation, or state why not | Code Tracer + Integration Mapper | `hooks/scripts/launch-*.sh`, `hooks.json`, `install_hooks.py`, `install_ccsession.py`, `skills/ccsession-tag/{ccsession-orca,hooks/*}`, `docs/designs/sc-issue-launch-level-hook.md`, `issue-pipeline-guard-g2*.md`, `issue-pipeline-fu1.md`; tests `tests/hooks/test_launch_*`, `tests/cli/test_install_hooks.py`, `tests/unit/test_install_ccsession.py`, `test_ccsession_tag.py` (launch-relevant parts), `tests/core/test_orca_session_launch_guidance.py` | `research/05-guard-stack-and-ccsession.md` |
| 06 | Coordinator duties text (current) AND the removed package (appendix): what the snapshot contract says a coordinator does with a claimed issue; removed `issue-pipeline` package, WC-17, "Issue pipeline duties", guard rule 1, tests removed, with data flow and safety properties. Removed code read ONLY via `git -C /home/coder/workspaces/IronClaude show 01e7a9e23^:<path>` | Code Tracer | `core/WORKER-CONTRACT.md`, `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md` (l.151-290, 1052-1145 only), `tests/skills/test_worker_contract.py`; old tree `src/superclaude/cli/issue_pipeline/**`, `tests/issue_pipeline/**`, old WORKER-CONTRACT.md, old launch-level-guard.sh | `research/06-coordinator-text-and-removed-code.md` |

Web research (Phase 4): none. Rationale: the subject is repo-internal; external docs cannot change any verified code finding, and sending repo details to outside services is not permitted. The phase is marked skipped with this rationale.

QA intensity: standard (Gate 1: 1 rf-analyst + 1 rf-qa + 1 rf-qa-qualitative; Gate 2: same; Gate 3: 7 agents; Gate 4: 2 fidelity agents). Partition thresholds apply (>6 research files / >4 synthesis files; here 6 and 6).

## TEMPLATE_NOTES
- Template: `.claude/templates/documents/technical_reference_template.md`; MDTM template 02.
- Tier Standard (800-1,200 lines target; allowed to about 1,300 plus the removed-code appendix because the lead asked for test files, triggers, state stores, gates, launch levels, guard layers, live-vs-off state, and GitHub writes for each piece). Subsystem sections 40-200 lines.
- Section 6 State Management: table of the three stores (`dispatch.json` and siblings under `state_dir`; `~/.claude/state/launch-level/{pending,sessions,requests,jobs}`; `.dev/issues/<N>/` claim artefacts). Section 7 Component Inventory: N/A (not a UI feature).
- Required content beyond template, to place in Sections 1, 2, 4, 5, 14: (a) a "what runs live vs switched off" ledger with one row per piece, evidence and status words BUILT-ON / BUILT-OFF (`enabled:false`) / NOT BUILT / REMOVED; (b) a "writes to GitHub" table per piece; (c) a trigger table; (d) test-pin matrix, one row per test file; (e) doc-vs-code contradiction table.
- Evidence rule: every claim cites `path:line` against the 61ac2c2e6 snapshot. Lines quoted from design docs that disagree with code are tagged.
- Privacy: the owner's memory notes (zero-setup watcher, COORD-, grant rows) are NOT sources; only files may be cited. Where the contract or code lacks them say "not found in snapshot".
- PR 686 / Clay design: one sentence "out of scope" in Section 1 and nothing else.
- C8 adaptation (lead constraint "write nothing outside the task folder and the output file"): unwired or retired in-scope capabilities are recorded as DEFECT candidates in Section 14 with evidence, and the document states plainly that no remediation tasks were created because this run may not write outside its folder; they are listed for the owner to decide.

## AMBIGUITIES_FOR_USER
None for intent. Open evidence limits to carry into Section 14 as [UNVERIFIED]: no runtime or live state exists in the snapshot ("never run live", PR numbers #447/#448 cannot be verified here); Orca reply shapes are `_assumed_shape`; OB-H1..3 live observations not run; whether any scheduler, dispatcher or coordinator currently triggers `issue-watch once` is not visible in the snapshot; `orchestration` skill location not in snapshot src (not needed for this reference).
