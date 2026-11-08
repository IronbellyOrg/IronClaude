# Synthesis 04: Implementation Plan, Open Questions and Evidence Trail (Report Sections 8 to 10)

**Issue:** IronbellyOrg/IronClaude#331 "Automated Github Issue / Task Watcher and Routing Service"
**Date:** 2026-11-07
**Status:** Complete
**Scope of this file:** report Section 8 (Implementation Plan), Section 9 (Open Questions) and Section 10 (Evidence Trail) only.
**Binding owner decision (ADDENDUM 2, 2026-11-07T07:12Z):** Q1 = option A (workspace-side poller), Q2 = claim-only, Q3 = only an integer issue number reaches the session prompt. IronbellyOrg/Coder#477 was filed assuming a push design; option A makes it unnecessary unless the push-design alternatives are revisited. The plan below targets option A only.

## Source key and evidence tags

All paths are under `.dev/tasks/to-do/TASK-RESEARCH-issue-watcher-20261107-064950/` unless they start with `src/`, `tests/`, `docs/`, `.github/` or `Makefile` (those are repository paths relative to the worktree root `/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/`).

| Key | File |
|---|---|
| R01 | `research/01-claim-flow-and-session-launch.md` (Code Tracer) |
| R02 | `research/02-github-surface-and-cli-patterns.md` (Integration Mapper) |
| R03 | `research/03-governance-and-security-surface.md` (Architecture Analyst) |
| W01 | `research/web-01-github-events-projects-and-limits.md` |
| W02 | `research/web-02-coder-claude-dispatch-and-security.md` |
| GAPS | `gaps-and-questions.md` (rows cited as "GAPS n") |
| NOTES | `research/research-notes.md` (ADDENDUM and ADDENDUM 2) |
| S03 | `synthesis/synth-03-options-recommendation.md` (Section 7 is the recommendation this plan follows) |

"R01 §12" means numbered section 12 of that file. Tags: [CODE-VERIFIED] traced in repo code or run locally; [CODE-CONTRADICTED] a doc or earlier claim that code contradicts (corrected here); [EXTERNAL-VERIFIED] confirmed on an official external page (external context, never overriding verified code behavior); [UNVERIFIED] not confirmed; [PROPOSAL] or [DERIVED] a design suggestion or arithmetic taken from the research files. In Section 8 a detail the research could not settle is written `open: <detail> (Qn)`, where Qn is the row in Section 9. Nothing marked `open` is stated as fact in a plan step.

---

## 8. Implementation Plan

### 8.0 Conventions of the plan

| Rule | Meaning |
|---|---|
| Existing versus NEW | A file named without a label exists and is cited from the research with file:line. A path labelled NEW does not exist yet; its parent directory exists per the research. No file chose any NEW name, so every NEW name is a [PROPOSAL] for the design doc to confirm |
| Nothing runs live | No step deploys anything, schedules anything, calls GitHub for real, or launches a real Orca session. All tests mock `gh`, `git` and `orca` (NOTES ADDENDUM 2) |
| Python rules | Python 3.10-compatible (`from __future__ import annotations`; no `tomllib`; `requires-python = ">=3.10"`, `pyproject.toml:16`), ruff `line-length = 88` (`pyproject.toml:173-181`), stdlib only so `make verify-deps` is unaffected, all runs through `uv run` (R02 §4.2, §6) |
| External context | Facts from W01/W02 are marked "external context" with their source URL where the plan relies on them |

### 8.1 What the plan builds and what it does not

| Builds (repo-side deliverable named by the owner, NOTES ADDENDUM 2) | Does not build (recorded as follow-up in the closing table) |
|---|---|
| 1. A design doc under `docs/designs/` | A listener, an address registry, an inbound port (none exist under A) |
| 2. A tested poller CLI package: one Click group, one verb `once` that runs a single poll cycle (the scheduler, not this code, supplies the 5-minute cadence) | The scheduler entry (`coder_script` cron) that runs it, which lives in the Coder repo template (W02 A1) |
| 3. Mocks for `gh` and `orca agent launch`; no live run | Any live deployment or live poll; the owner-run live test is written as a checklist, not executed |
| 4. Trigger and approval label setup instructions, approver allow-list setup, per-developer scope setup | Any change to `/sc:issue` itself, any pipeline after the claim (`--claim --pipeline` is design only: R01 §11, R03 §1.2) |

### 8.2 Poll cycle at a glance

```
 scheduler (Coder template, Coder repo, follow-up)  every 5 min
      |   plain process, never a Claude session, never a worker Task (WC-13: R01 §7, R03 §5)
      v
 superclaude issue-watch once --worktree-path <checkout> ...              [NEW commands.py]
      |
      |-- lock (flock on a lock file)  -> overlapping run exits 0          [NEW state.py]
      |-- gh api user -q .login              -> own login                  [NEW github.py]
      |-- ONE discovery query (Project items, Status Backlog, trigger label, assignee @me)
      |        -> issue NUMBERS only (ints)                                [NEW github.py]
      |-- per candidate (capped):
      |     issue view  --json number,state,labels,assignees   (no title/body)   -> filters 1,5 + open
      |     issue events (label actor)           -> filter 2 (allow-listed approver of latest `labeled`)
      |     issue comments (jq keeps ids only)   -> own claim marker already posted? -> skip
      |     issue view again right before launch -> state/assignees unchanged?
      |-- write dispatch record BEFORE launch                              [NEW state.py]
      v
 orca agent launch --agent claude --worktree path:<abs> --surface terminal
                   --prompt "/sc:issue --claim <int>" --json              [NEW launch.py]
      v
 ordinary top-level session -> /sc:issue --claim N -> assign @me, accuracy check,
 summary, two marked comments -> STOP at next-steps.md (the person runs the rest)   [R01 §3]
 (no inbound port, no listener, no registry; GitHub is the only network peer)
```

### 8.3 Proposed NEW paths (all labelled NEW wherever they appear below)

| NEW path | Kind | Parent exists per | Modelled on |
|---|---|---|---|
| `docs/designs/issue-watcher.md` | design doc | `docs/designs/` holds `prd-spec-flag.md`, `sc-issue-command.md`, `sc-issue-launch-level-hook.md` (R02 §7) | `docs/designs/sc-issue-command.md` sections and header block (R02 §7) |
| `src/superclaude/cli/issue_watch/` with `__init__.py`, `commands.py`, `runner.py`, `models.py`, `github.py`, `selection.py`, `launch.py`, `state.py`, `cycle.py` | Click package | `src/superclaude/cli/` holds `recommend/`, `tasklist/`, `cleanup_audit/`, `init_lite.py` (R02 §4.2) | `cli/recommend/` layout: thin `commands.py` plus pure-logic modules (R02 §4.2) |
| `tests/issue_watch/` with `__init__.py`, `conftest.py`, `fixtures/`, `test_*.py` | tests | `tests/` holds `recommend/`, `swarm/`, `pr_submit/` (R02 §5) | `tests/recommend/`, `tests/pr_submit/` (R02 §5) |

Top-level verb: `issue-watch` (group function `issue_watch_group`, subcommand `once`). [PROPOSAL: no research file names the verb; R02 §4.1 records only that the house convention is a top-level verb.] The verb does not collide with the 15 names in `EXPECTED_TOP_LEVEL_COMMANDS` or with `swarm` and `reflect` (R02 §4.1, §4.3).

### 8.4 Owner decisions the plan implements (full table in Section 9)

| ID | Decision | How the plan implements it |
|---|---|---|
| D1 | Option A: each workspace polls every 5 minutes with its own `gh` login and starts the claim through `orca agent launch`; no listener, no inbound port, no registry | One CLI verb `once`, run by a scheduler; identity from `gh api user -q .login`; the only network peer is GitHub (Phase 4, 5) |
| D2 | Claim-only | The launch prompt is exactly `/sc:issue --claim <int>`; nothing after the claim is started (Phase 3) |
| D3 | Only an integer issue number reaches the session prompt | `build_claim_prompt` accepts only a Python `int` in range, every `gh --json` field list excludes title, body and comments (Phase 3, 4) |

### Phase 1: Design doc

**Goal:** Write `docs/designs/issue-watcher.md` (NEW) in the house format so that `/sc:workflow` and the brainstorm can start from it. The doc records the owner decisions, the Coder#477 statement, the integer-only prompt rule, the security model, the launch contract with its UNVERIFIED parts, the defaults, the acceptance criteria and the follow-up.
**Dependencies:** none (research is complete). Later phases may refine the doc; Phase 7 adds the setup instructions to it.

House format facts used (R02 §7): `docs/designs/sc-issue-command.md` has a bold-label header block (`**Status:**` l.3, `**Issue:**` l.4, `**Branch:**` l.5, `**Source of truth:**` l.6, `**Produced by:**` l.7), then numbered sections (Purpose and scope; Binding decisions table with IDs `B1..B15`; Corrections to the issue text; interface; architecture; GitHub call rules; Error handling; Files to create or change; Tests; Sync and registration; Defaults with IDs `D1..D27`; Acceptance criteria). `docs/designs/sc-issue-launch-level-hook.md` section 16 is the model for "Residual risks and UNVERIFIED items". `docs/` is excluded from ruff (`pyproject.toml:173-181`), so the doc is never linted.

| Step | Action | Files | Details |
|---|---|---|---|
| 1.1 | Create the doc with the header block and sections 1 and 2 | `docs/designs/issue-watcher.md` (NEW) | Header: `**Status:**` design draft, `**Issue:**` IronbellyOrg/IronClaude#331, `**Branch:**` `ironbelly/issue-331-github-issue-watcher` (current branch per the session git status), `**Source of truth:**` the research report built from this task folder, `**Produced by:**` this research. Section 1 Purpose and scope: the watcher selects tagged, human-approved, in-Project, Backlog, intended-owner issues and starts `/sc:issue --claim <N>` in the workspace, then stops. Section 2 Binding decisions table with IDs `B1..`: D1, D2, D3 of 8.4 quoted from NOTES ADDENDUM 2; the repo-side deliverable (design doc, tested poller, label setup instructions); "nothing run live" |
| 1.2 | Record the Coder#477 statement and the repo boundary | same file, section 2 and a closing "Follow-up and revisit conditions" section | Text to record, from NOTES: IronbellyOrg/Coder#477 (workspace listener and registration, open, read 2026-11-07) was filed assuming a push design; option A makes #477 unnecessary unless the push-design alternatives are revisited; the listener, registration and transport live in the Coder repo, not in IronClaude. Copy the nine revisit conditions from the closing table of this plan (S03 "Revisit conditions") |
| 1.3 | Section 3 "Corrections to the issue text" (Issue text, Problem (verified), This design) | same file | Rows: (a) issue text expects `/sc:issue --claim` to start the full path; [CODE-CONTRADICTED] by `src/superclaude/commands/issue.md:15, :79, :83`, `refs/claim.md:80` (R01 §1, §3); design = claim-only. (b) `src/superclaude/pr_submit/ci.py` is not a `gh` wrapper (R02 §3.1); design = new runner. (c) project CLAUDE.md calls the fork private; live check shows PUBLIC (R03 §3.3). (d) `docs/designs/sc-issue-launch-level-hook.md:23` states `launch-level-guard.sh` as enforcing while the file does not exist (R03 §1.2); design = governed levels are out of scope |
| 1.4 | Sections 4 and 5: interface and component architecture | same file | Usage block for `superclaude issue-watch once` with the option table and exit-code table of Phase 5 step 5.3; ASCII module tree and responsibilities for the nine modules of 8.3; the diagram of 8.2. Every open value is written "open (Qn)" |
| 1.5 | Section 6: selection (five filters) and GitHub call rules | same file | Filter table of Phase 4 step 4.3 (rule, query used, extra calls, source). GitHub call rules, from R01 §9, R02 §3.3 and W01 §5, §10 (external context): always `--repo IronbellyOrg/IronClaude` or a `repos/IronbellyOrg/IronClaude/...` api path, never gh's default repo (Convention B of R02 §3.3 is unsafe for the fork); `gh api` calls carry `--method GET` explicitly; request `number,labels,assignees,state` only; explicit `--limit 100` because the default is 30; sequential calls; honor `retry-after` and `x-ratelimit-reset`; cap retries. Cost: 12 polls per hour is 0.24 percent of the 5,000 per hour user allowance per call type [DERIVED, W01 §14.2] |
| 1.6 | Section 7: security model | same file | Integer-only prompt (rule below); approver allow-list from the latest `labeled` event actor (W01 §11, W02 G2); plain-process launch (WC-13); identity is the workspace's own `gh` login read each cycle, not assumed equal to the Coder owner (W02 recommendation 4). Residual risks, stated not solved (R03 §3.2, §3.3, §6): the claim itself reads title, body and comments live and posts unreviewed worker output to a public issue; no hook, permission rule or branch protection constrains the launched session; Orca's default `--dangerously-skip-permissions` may apply (Q6); the policy for the claim's own reads of untrusted text is open (Q12) |
| 1.7 | Section 8: at-most-once and the dispatch record | same file | Layers (W02 G7 table): GitHub assignee plus own claim marker comment as durable record; local dispatch record as throttle; pre-launch re-read (step 8 of the `run_cycle` algorithm in Phase 5). Record that a post-write re-read (after the poller adds `@me`, W02 G7 [PROPOSAL], `research/web-02-coder-claude-dispatch-and-security.md:186`; R01 §9 reservation, `research/01-claim-flow-and-session-launch.md:157`) belongs only to routing candidate 4 and is not built, because the poller never writes to GitHub (SC-13, step 4.5). State what cannot be guaranteed: no atomic exclusion across logins (assignment is additive, no compare-and-set: W02 G1, external context https://docs.github.com/en/rest/issues/assignees); same-login multi-workspace case unsolved (Q4, Q14); a lost local record must never cause a second launch of an issue that already carries the claim marker (W02 recommendation 3) |
| 1.8 | Section 9: the `orca agent launch` argument contract | same file | The contract table of Phase 3 step 3.2, with `[UNVERIFIED]` rows kept as written in R01 §12 |
| 1.9 | Sections 10 to 14: error handling, files, tests, sync, defaults | same file | Error table (Scenario, Behavior) from Phase 5 step 5.2; Files-to-create table from 8.3; Tests table from Phases 2 to 6; sync statement: a pure `cli/` package is not mirrored to `.claude/`, so no `make sync-dev` step; a future `/sc:` command or skill would need it (R02 §6); Defaults table with IDs `D1..` marking each value [PROPOSAL] or open (per-cycle launch cap, attempt cap, lease length: Q13) |
| 1.10 | Sections 15 and 16: residual risks, UNVERIFIED items, owner-run live test checklist, acceptance criteria | same file | UNVERIFIED section in the style of `sc-issue-launch-level-hook.md` section 16: copy the open rows of Section 9 of this report. Live test checklist (written, not run): Q1, Q2, Q3, Q6, Q7, Q8, Q15 as the owner-run checks. Acceptance criteria (numbered, testable): see Phase 6 step 6.4 |

**Integer-only prompt rule recorded in the doc:** the only issue-derived text in any launch argument is `str(number)` where `number` is a Python `int` from `gh` JSON with `1 <= number <= 999999999`; the prompt is the fixed string `/sc:issue --claim ` followed by that integer; it is passed as one element of an argv list, never through a shell (R01 §13; R03 §3.1; W02 F4 pattern `^[1-9][0-9]{0,8}$`, external context https://docs.github.com/en/actions/reference/security/secure-use). `origin_repo.py` (`src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:74` `_NUMBER`, `:102-153` `check_claim`) validates only inside the session after the prompt arrived, so it is a second check, not the first (R01 §5, §13).

### Phase 2: Package skeleton, command runner seam and Click registration

**Goal:** A registered, empty `issue-watch` group and the injectable subprocess runner that every later module takes as a parameter, with tests that pin both.
**Dependencies:** Phase 1 is not a code dependency, but the module list of 8.3 comes from the design doc.

The runner is NEW code: no Python module under `src/superclaude` builds or runs a `gh` call; `src/superclaude/pr_submit/ci.py` is a pure classifier with no `subprocess` import, so the earlier "mockable gh wrapper" claim is [CODE-CONTRADICTED] (R02 §3.1, §3.2). The nearest Python subprocess pattern is `src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py`: `read_origin()` (l.156-174) calls `subprocess.run(["git","remote","get-url","origin"], capture_output=True, text=True, check=False)`, catches `OSError` and non-zero returns and maps them to a typed `ClaimError(code, exit_code, message)` (l.77-83); `main(argv)` (l.177-191) returns an int exit code (R02 §3.2). That file's subprocess call is hard-wired, so the new runner takes the call as a parameter. Precedent for passing a callable as a parameter: `cli/reflect/fallback.py:39` `FallbackTransportFactory = Callable[[str], Transport]`, `cli/audit/tool_orchestrator.py:105`, `cli/audit/batch_retry.py:87` (R02 §3.2). Timeout precedent: `cli/sprint/notify.py:21,25` `subprocess.run(cmd, timeout=5, check=False)`.

| Step | Action | Files | Details |
|---|---|---|---|
| 2.1 | Create the package `__init__` with a lazy export | `src/superclaude/cli/issue_watch/__init__.py` (NEW) | First line `"""Issue watcher module -- ``superclaude issue-watch`` CLI command.` (docstring convention of `tasklist/__init__.py:1`, `recommend/__init__.py:1`). Module `__getattr__` that imports `.commands` only when `issue_watch_group` is accessed, as in `recommend/__init__.py:12-20` and `tasklist/__init__.py:9-17`, to keep `superclaude --help` import time down (R02 §4.2) |
| 2.2 | Create the runner seam | `src/superclaude/cli/issue_watch/runner.py` (NEW) | `@dataclass(frozen=True) class CommandResult: returncode: int; stdout: str; stderr: str`. `Runner = Callable[[Sequence[str]], CommandResult]`. `class CommandError(Exception)` with `code: str` and `message: str` (shape of `ClaimError`, `origin_repo.py:77-83`). `def run_command(argv: Sequence[str], *, timeout: float = 60.0) -> CommandResult`: `subprocess.run(list(argv), capture_output=True, text=True, check=False, timeout=timeout)`, never `shell=True`; `FileNotFoundError`/`OSError` becomes `CommandError("E-TOOL-MISSING", ...)`, `subprocess.TimeoutExpired` becomes `CommandError("E-TIMEOUT", ...)`. The 60 second default is a [PROPOSAL]; no research value exists |
| 2.3 | Create the Click group (no verbs yet) | `src/superclaude/cli/issue_watch/commands.py` (NEW) | `@click.group("issue-watch") def issue_watch_group() -> None:` with a one-paragraph docstring, the form of `recommend/commands.py:34-35`. The verb `once` is added in step 5.3 |
| 2.4 | Register the group in the root CLI | `src/superclaude/cli/main.py` (existing) | Add one block after the `reflect` registration at l.559-561 and before `if __name__ == "__main__": main()` at l.564-565: `from superclaude.cli.issue_watch import issue_watch_group  # noqa: E402,I001  # intentional: deferred subcommand registration to avoid circular imports` then `main.add_command(issue_watch_group, name="issue-watch")`. The `noqa` marker is required or ruff flags the import (`select = ["E","F","I","N","W","TID"]`, `pyproject.toml:183-184`). No `pyproject.toml` change: `[tool.hatch.build.targets.wheel] packages = ["src/superclaude"]` (`pyproject.toml:78-79`) already ships any new subpackage (R02 §4.1, §4.2) |
| 2.5 | Create the test package and the fake runner | `tests/issue_watch/__init__.py` (NEW), `tests/issue_watch/conftest.py` (NEW), `tests/issue_watch/fixtures/` (NEW directory) | `conftest.py` provides `class FakeRunner` (callable with the `Runner` signature): records every argv in `calls: list[list[str]]`, returns scripted `CommandResult`s chosen by a predicate list, and returns a loud failure (`returncode=99`, stderr `unexpected call`) for any argv no script matches, the fail-loudly behavior of the repo's PATH stubs (R02 §3.4: exit 1, 99, 91-93). Fixture loading helper `load_fixture(name)` for `tests/issue_watch/fixtures/*.json`, modelled on `tests/pr_submit/conftest.py:28-35` (that helper is local to `tests/pr_submit/`, so it is re-created, not imported) |
| 2.6 | Registration and import tests | `tests/issue_watch/test_cli_registration.py` (NEW), `tests/issue_watch/test_runner.py` (NEW) | Registration: `CliRunner().invoke(main, ["--help"])` lists `issue-watch`, and `["issue-watch", "--help"]` exits 0, as in `tests/recommend/test_cli_registration.py` (3 tests, R02 §4.3) and `tests/swarm/test_cli_registration.py:74`. `test_runner.py`: a missing executable raises `CommandError("E-TOOL-MISSING")`; a sleeping child raises `E-TIMEOUT`; the argv is passed as a list (monkeypatch `subprocess.run` and assert `shell` is absent or false). Stdlib-only test for the package modeled on `tests/skills/test_issue_repo_resolution.py:281` `test_script_imports_only_standard_library` (R02 §3.2, applied to the files of `src/superclaude/cli/issue_watch/`, with `click` allowed in `commands.py` only) |

Not needed: `tests/cli/test_cli_registration.py` freezes `EXPECTED_TOP_LEVEL_COMMANDS` but only runs `<name> --help` for each member, so adding a group does not break it; `swarm` and `reflect` are registered yet absent from that set, so the set is a floor and its "forces an update" comment is [CODE-CONTRADICTED] (R02 §4.3).

### Phase 3: Integer-only prompt, `orca agent launch` function and its mock contract

**Goal:** The only code that builds the launch prompt and the only code that calls `orca agent launch`, with the argument contract pinned in a mock that imitates the real CLI as far as the research documents it.
**Dependencies:** Phase 2 (runner seam, `FakeRunner`).

**The `orca agent launch` argument contract the function and the mock must imitate** (R01 §12, from `orca agent launch --help` run locally and the Orca files `specs/agent-launch.js:9-33`, `handlers/agent-launch.js:11-35`, `agent-launch-request.js:38-117`, `agent-launch-recovery.js:54-64`; repo rule in `src/superclaude/core/CLAUDE.md` "Orca session launches" l.45-53 and `src/superclaude/skills/ccsession-tag/README.md:228-237`):

| Part of the contract | What the research shows | Tag | What the code and the mock do |
|---|---|---|---|
| Invocation | `orca agent launch --agent <id> [--worktree <selector>] [--prompt <text>] [--model <id>] [--effort <level>] [--surface chat\|terminal] [--focus] [--retry-launch <operationId>] [--json]` | [CODE-VERIFIED] | argv list, never a shell string: `["orca","agent","launch","--agent","claude","--worktree","path:<abs>","--surface","terminal","--prompt","/sc:issue --claim <int>","--json"]`. `--model`, `--effort`, `--focus` are not passed |
| Agent id | `--agent` required; `claude` is a known agent (`shared/tui-agent-config.js:15`); unknown agent gives `invalid_argument` | [CODE-VERIFIED] | the mock rejects any other `--agent` value with exit 1 |
| Which worktree or repo | `--worktree <selector>`: `identity:`, `id:`, `name:`, `branch:`, `issue:<n>`, `path:<abs>`, `active`, `current`; omitted/`active`/`current` resolve from the caller's cwd; there is no `--repo` flag | [CODE-VERIFIED] | `path:<abs>` only. `issue:<n>` is not used until the Orca-to-GitHub linking behavior is tested (Q17; project rule forbids Orca link flags for this repo). The mock rejects a non-`path:` selector in the poller's own tests and has a "cwd not inside an Orca workspace" failure for a missing selector |
| Needs an existing worktree | `createsWorktree: false`; a new checkout needs `orca worktree create --agent` | [CODE-VERIFIED] | the function never creates a worktree; `--worktree-path` must be an existing Orca workspace (Q17 for which one) |
| Surface | `--surface terminal` always runs the agent CLI; other values than chat or terminal are refused | [CODE-VERIFIED] | `--surface terminal` always passed |
| How the prompt is passed | `--prompt <text>` becomes `{text, delivery: 'submit'}`: submitted, not left as a draft; an empty or whitespace-only prompt is dropped silently and the agent starts with no prompt; a valueless `--prompt` is rejected | [CODE-VERIFIED] | the prompt is never empty; the mock records the `--prompt` element and the tests assert it equals `/sc:issue --claim <int>` exactly |
| Argv versus typed paste to Claude | Claude's config has `promptInjectionMode: 'argv'`; which path `agent launch` takes lives in the host runtime | [UNVERIFIED] | not modelled; open: Q2 |
| Does a leading `/sc:issue` run as a slash command | not shown by any file | [UNVERIFIED] | not modelled; open: Q1 (one owner-run live test) |
| Agent command | Orca runs the configured Claude command; `ccsession-orca` only when set in Orca Settings (README:216-223); a prompt starting with `/` is read as the task by `ccsession-orca` (`:110` skips `-*` options, `:116-119`) | [CODE-VERIFIED] locally; Coder host [UNVERIFIED] | open: Q5 |
| Success output | text mode lines `agent: terminal`, `handle`, `worktreeId`, `operationId`, `prompt: <outcome>`, `warning`; with `--json` an object `{outcome{kind,handle,sessionId?}, receipt{detail}, worktreeId, operationId, prompt{outcome}, warning}` | fields [CODE-VERIFIED]; exact JSON key nesting [UNVERIFIED] | exit 0 plus JSON on stdout; the code treats exit 0 as "started" and reads `operationId` only if present at the top level; the raw stdout (truncated) goes to the dispatch record. open: Q2 |
| Exit status | error: `reportCliError` then `process.exitCode = 1`; success leaves 0 | [CODE-VERIFIED] by reading, not executed | mock: exit 0 on success, exit 1 on error |
| Lost reply | `--retry-launch <operationId>` replays the same launch, "Never retry as a fresh launch"; an unconfirmed outcome throws `agent_session_operation_unknown` with `launchOutcome: 'unknown'`, `retrySafe`, `operationId`, `recoveryCommand`, and the message "the agent may already be running and the prompt may already be submitted" | [CODE-VERIFIED]; real JSON error body [UNVERIFIED] | the mock has an "unknown outcome" mode: exit 1 and a body containing `agent_session_operation_unknown` and an `operationId`; the code recognises it by that code string and keeps the id. Whether `--retry-launch` must repeat the original `--agent/--worktree/--prompt` is not shown: open: Q3 |
| Other refusals | `incompatible_runtime` when the host cannot start agents; `Setup decision required for this repository` passes through | [CODE-VERIFIED] | the mock has an `incompatible_runtime` mode (exit 1); the code reports `failed` |

| Step | Action | Files | Details |
|---|---|---|---|
| 3.1 | Constants and outcome type | `src/superclaude/cli/issue_watch/models.py` (NEW) | `REPO = "IronbellyOrg/IronClaude"` (explicit, never gh's default; R02 §3.3 Convention A and project CLAUDE.md fork rule); `MAX_ISSUE_NUMBER = 999_999_999`; `@dataclass(frozen=True) class LaunchOutcome: kind: Literal["started","unknown","failed"]; operation_id: str \| None; detail: str`. Phase 4 adds the issue models to this file |
| 3.2 | The prompt builder (Q3 of the owner: integer only) | `src/superclaude/cli/issue_watch/launch.py` (NEW) | `def build_claim_prompt(number: object) -> str`: raise `ValueError` unless `type(number) is int` (rejects `bool`, `str`, `float`, `None`) and `re.fullmatch(r"[1-9][0-9]{0,8}", str(number))`; return `"/sc:issue --claim " + str(number)`. This is stricter than the `str(int(number))` of R01 §13 because `int()` also accepts strings with spaces or non-ASCII digits [PROPOSAL, hardening]; the pattern is W02 F4. The number must come from the `number` field of `gh --json` output (Phase 4), never from title or body |
| 3.3 | Origin check of the target checkout (research finding F5) | same file | `def check_worktree_origin(worktree: Path, git: Runner) -> None`: runs `["git","-C",str(worktree),"remote","get-url","origin"]`, accepts only the two URL forms `parse_origin_url` accepts in `origin_repo.py:66-69` (`https://github.com/o/r[.git][/]`, `git@github.com:o/r[.git][/]`; mirrored, not imported, because skill scripts are installed primitives and not package code), compares owner/repo case-insensitively to `REPO` (as `origin_repo.py:135`), else `CommandError("E-WRONG-ORIGIN")`. Reason: `/sc:issue --claim` reads only the `origin` of the session's working directory and writes `.dev/issues/<N>/` into that checkout; a checkout whose origin is not the fork stops the claim with `E-NO-ORIGIN` or `E-FOREIGN-REPO` (R01 §1, §5, §11; analysis finding F5). Which checkout or Orca worktree in the workspace is used is open: Q17 (no research file shows code that picks one; the CLI takes it as `--worktree-path`) |
| 3.4 | The launch function | same file | `def build_launch_argv(number: int, worktree: Path, *, retry_operation_id: str \| None = None) -> list[str]` (requires `worktree.is_absolute()`; `"path:" + str(worktree)`; appends `["--retry-launch", id]` when given, original arguments kept: Q3). `def launch_claim(number: int, worktree: Path, *, orca: Runner, retry_operation_id: str \| None = None) -> LaunchOutcome`: builds the argv with `build_claim_prompt(number)`, calls `orca(argv)`; exit 0 gives `started` (operation id read tolerantly from the JSON); non-zero with `agent_session_operation_unknown` in stdout/stderr gives `unknown` with the id; any other non-zero gives `failed`. A `CommandError` from the runner (orca missing, timeout) gives `failed`. The function never retries by itself and never launches fresh after `unknown` |
| 3.5 | The mock | `tests/issue_watch/conftest.py` (extend), `tests/issue_watch/fixtures/orca-launch-ok.json`, `orca-launch-unknown.json`, `orca-launch-incompatible.json` (all NEW) | `class FakeOrca(FakeRunner)` implements the contract table: validates the argv shape (subcommand `agent launch`, `--agent claude`, `--worktree path:<abs>` with an absolute path, `--surface terminal`, a non-empty `--prompt`), then returns the scripted mode: `ok` (exit 0, JSON), `error` (exit 1), `unknown` (exit 1 with `agent_session_operation_unknown` and `operationId`), `incompatible` (exit 1), `no_workspace` (exit 1, for a missing `--worktree`). Fixture JSON shapes are marked in a comment as "assumed from R01 §12, replace after the live test (Q2)" |
| 3.6 | Tests for the prompt and the launch contract | `tests/issue_watch/test_prompt_validation.py` (NEW), `tests/issue_watch/test_launch_contract.py` (NEW) | Prompt: parametrized accept `1`, `331`, `999999999`; reject `0`, `-1`, `1000000000`, `True`, `3.0`, `None`, `"331"`, `"331 extra"`, `"#331"`, `" 331"`, a non-ASCII digit string, and a string such as `"331; echo x"`. Contract: the recorded argv equals the list in the contract table exactly; the `--prompt` value is a single element equal to `/sc:issue --claim 331`; the only issue-derived element of the argv is that integer; the runner was called with a list; `ok` gives `started`; `error` and `incompatible` give `failed`; `unknown` gives `unknown` with the id and a second call with `retry_operation_id` contains `--retry-launch <id>`; a relative worktree path raises. `check_worktree_origin`: accepts both URL forms for `IronbellyOrg/IronClaude` in either letter case; rejects another owner, rejects a URL containing `SuperClaude-Org`, rejects a failing `git` |

**Mocking style for these tests:** injected runner (`FakeOrca`, `FakeRunner`), because the unit under test takes the runner as a parameter. The repo's existing way of mocking `gh` is different and is used in Phase 6: a stub `gh` executable placed on `PATH` and run through `subprocess.run` (for example `tests/pr_submit/test_conflict_e2e.py`, which builds `["gh", *args]` and runs it against a PATH stub; four other `tests/pr_submit/` files write `gh` stubs too: R02 §3.4).

### Phase 4: Read-only GitHub queries and the five-filter selection

**Goal:** Pure selection logic with five filters plus a thin read-only `gh` layer. No write-shaped `gh` call exists anywhere in the package, and no `--json` field list contains title, body or comments.
**Dependencies:** Phase 2 (runner, `FakeRunner`). Independent of Phase 3 except for the shared `models.py` file (Phase 3 creates it; this phase extends it).

**The five filters, each applied through the cheapest correct query the research found** (W01 §14.3, external context; R01 §9; R02 §2c; R03 §4):

| # | Filter | Rule | Where it is evaluated | Extra `gh` calls | Evidence and open points |
|---|---|---|---|---|---|
| 1 | Tagged | the trigger label is on the issue and the issue is open | server side in the discovery query, then re-checked client-side on the `issue view` snapshot | 0 beyond the snapshot | label names do not exist yet (fork has only the 9 default labels, R02 §2): names are required options, open: Q9 |
| 2 | Human-approved | the approval label is currently on the issue, and the latest `labeled`/`unlabeled` event of that label is a `labeled` event whose `actor.login` is on the approver allow-list | client side, only for issues that passed filters 1, 3, 4, 5 | 1 or more events calls per survivor (pages of 100, up to the page cap; reaching the cap fails closed: step 4.2) | actor of the label event: W01 §11, W02 G2 (external context https://docs.github.com/en/rest/issues/events); Triage role or higher can label, so role alone is too weak (R03 §4.2); allow-list location and rule open: Q10; edit-after-approval not detectable: Q11 |
| 3 | In the Project | the issue is an item of the configured Project | server side: the Project items query is the discovery query | 0 | needs `read:project` on the poller's login, which the observed token lacks (R03 §4.2): Q7; `--label-only` mode drops filters 3 and 4 and is a degraded mode the owner must allow: Q9 |
| 4 | Status Backlog | the item's Status is Backlog | server side `status:Backlog` in `--query`; client side fail closed: an item whose status cannot be read from the JSON is rejected | 0 | `status:Backlog` is documented for UI filtering only; acceptance by `gh project item-list --query` and the JSON schema are [UNVERIFIED]: Q8. The claim leaves the item in Backlog (R01 §3), so the dispatch record, not the status, prevents repeats |
| 5 | Intended owner | the issue is assigned to the own login and to nobody else | server side `assignee:@me` in the query, client side on the snapshot's `assignees` | 0 | routing candidate 1 of R01 §9 / S03 §7.4, the one the research supports; the claim stops when the issue is "assigned to anyone other than the current login" (`refs/claim.md:41`) and continues when assigned to the current login (`:42`), so the shared predicate "skip an issue assigned to a login other than the own login" holds (R02 §2c). The owner has not chosen the routing rule: open: Q4. The predicate is one replaceable function |

Calls the package makes (argv after the program name; all read-only; all with an explicit repo or `repos/IronbellyOrg/IronClaude/...` path; `gh api` always with `--method GET`, the pattern of `skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh` l.53-55 `--method GET -F per_page=100 -F page=...`, R02 §3.3):

| Call | argv | Returns / projects | Evidence |
|---|---|---|---|
| Own login | `gh api user -q .login` | the login, validated against `[A-Za-z0-9][A-Za-z0-9-]*` before it is used in a jq string [PROPOSAL] | R01 §9; `refs/claim.md:26` |
| Discovery, Project mode | `gh project item-list <N> --owner <project-owner> --query "<q>" --format json -L 100` where `<q>` is built only from operator options and fixed words: `is:issue status:Backlog label:<trigger> assignee:@me` | issue numbers (must be `int`) of items whose content repository equals `IronbellyOrg/IronClaude`; an item without a readable repository is rejected, because the Project may hold issues of other repos and `issue view <N> --repo` would otherwise read a different issue with the same number [PROPOSAL, fail closed; JSON schema unverified: Q8] | W01 §7, §8 (external context https://cli.github.com/manual/gh_project_item-list); default `-L` is 30, so `-L 100` is explicit |
| Discovery, label-only mode | `gh issue list --repo IronbellyOrg/IronClaude --label <trigger> --assignee @me --state open --json number --limit 100` | issue numbers | flags verified by running `gh issue list --help` (R01 §9, R02 §2c) |
| Snapshot | `gh issue view <N> --repo IronbellyOrg/IronClaude --json number,state,labels,assignees` | `Candidate` | subset of `refs/claim.md:26`; title, body and comments are never requested (R02 §3.3) |
| Label events | `gh api --method GET repos/IronbellyOrg/IronClaude/issues/<N>/events -F per_page=100 -F page=<p> --jq <events-jq>` | per page `{n, items}`: the raw page length and the `LabelEvent` list (id, event, actor, label name) of that page | W01 §11, W02 G2. The REST events list comes back oldest first (read-only `gh api` call on issue #331 on 2026-11-07: first event 2026-10-30, last 2026-11-07), so a page cap drops the newest events; the list is read to its end or the read fails (step 4.2). The repo's own precedent is `poll-augment-review.sh:47` ("fail incomplete at the cap, never silently truncate") with 1000 pages (`:51`) |
| Own claim marker | `gh api --method GET repos/IronbellyOrg/IronClaude/issues/<N>/comments -F per_page=100 -F page=<p> --jq <marker-jq>` | per page `{n, items}`: the raw page length and the list of comment ids only | marker `<!-- sc:issue:claim -->` and the own-login rule of `refs/claim.md:29, :84-88`; field name of the comment author in the REST object is not shown by the research (it shows `author_association` and `since`): open: Q11 |

```
events-jq : {n: length, items: [.[] | select(.event=="labeled" or .event=="unlabeled") | {id, event, actor: .actor.login, label: .label.name}]}
marker-jq : {n: length, items: [.[] | select(.user.login == "<own-login>") | select(.body | contains("<!-- sc:issue:claim -->")) | .id]}
```

Each filter returns the raw page length `n` (taken before any `select`) together with the filtered `items`. The page-end test uses `n`, never the length of `items`, because a raw page of 100 events that holds 40 label events comes back with 40 items: counting the filtered items would read that full page as a short last page and stop early on partial data [DESIGN, the logic of the plan itself; the repo precedent tests the raw page, `poll-augment-review.sh:69-70`: `count="$(jq 'length' ...)"` then `if [ "$count" -lt 100 ]` ends the read, and `:74` fails when the end was not reached].

The comment text is consumed inside `gh --jq` and only ids leave it, so no comment body reaches the poller or any prompt (owner decision D3).

| Step | Action | Files | Details |
|---|---|---|---|
| 4.1 | Issue models | `src/superclaude/cli/issue_watch/models.py` (extend) | `@dataclass(frozen=True) class Candidate: number: int; state: str; labels: frozenset[str]; assignees: tuple[str, ...]`. `@dataclass(frozen=True) class LabelEvent: event_id: int; event: str; actor: str; label: str`. `@dataclass(frozen=True) class Decision: number: int; selected: bool; rejected_by: str \| None; detail: str`. `@dataclass(frozen=True) class SelectionConfig: trigger_label: str; approval_label: str; approvers: frozenset[str]; own_login: str` |
| 4.2 | The read-only GitHub layer | `src/superclaude/cli/issue_watch/github.py` (NEW) | `def whoami(gh: Runner) -> str`; `def discover_project(gh: Runner, *, owner: str, project_number: int, trigger_label: str) -> list[int]`; `def discover_label_only(gh: Runner, *, trigger_label: str) -> list[int]`; `def snapshot(gh: Runner, number: int) -> Candidate`; `def label_events(gh: Runner, number: int, *, label: str, max_pages: int = 5) -> list[LabelEvent]`; `def own_claim_comment_ids(gh: Runner, number: int, *, login: str, max_pages: int = 5) -> list[int]`. Each builds `["gh", ...]` as in the table above and calls the injected `gh`; a non-zero return or invalid JSON raises `CommandError("E-GH-FAILED")`. Every number placed in an argv is first checked with `type(n) is int`. `max_pages = 5` is a [PROPOSAL]; no research value. **Fail closed on truncation:** the events and comments lists come back oldest first, so a cap would drop the newest entries. Each page is read through the jq filters above, which return `{n, items}` with `n` the RAW page length before filtering. The loop reads page 1, 2, ... and stops with a complete list when a page has `n < 100`; it continues while `n == 100`. If page `max_pages` is read and its `n` is still 100 (the end of the list was not reached), `label_events` and `own_claim_comment_ids` raise `CommandError("E-GH-TRUNCATED")`; they never return a partial list. The test is on `n`, not on `len(items)`: a filtered page is usually shorter than 100 even when the raw page is full, so a test on the filtered length could never fire and would read a short filtered page as the end of the list. A page whose output is not an object with an integer `n` and a list `items` raises `CommandError("E-GH-FAILED")` [PROPOSAL; same rule as `poll-augment-review.sh:47`, which fails incomplete at its page cap, and the same raw-count test as `poll-augment-review.sh:69-70`]. A module-level `READ_ONLY_VERBS` check is not added: read-only behavior is asserted in tests (step 4.5), where the repo's own precedent for it lives (`assert_no_retrigger_call`, `tests/pr_submit/test_conflict_e2e.py:178-186`) |
| 4.3 | The pure selection logic | `src/superclaude/cli/issue_watch/selection.py` (NEW) | `def passes_cheap_filters(c: Candidate, cfg: SelectionConfig) -> Decision` (filters 1, 5 and open state; filters 3 and 4 are decided by discovery and recorded by the caller). `def is_intended_owner(c: Candidate, own_login: str) -> bool` (assignees equal to `(own_login,)`; the single replacement point for the routing rule, Q4). `def is_approved(events: Sequence[LabelEvent], cfg: SelectionConfig) -> Decision` (latest event for `cfg.approval_label` by `event_id` order; approved only if it is `labeled` and its actor is in `cfg.approvers`; the approval label must also be in the snapshot's labels). `is_approved` is called only with a complete event list: the cycle maps `E-GH-TRUNCATED` from `label_events` to `Decision(selected=False, rejected_by="approval-unverifiable")`, so approval is never decided on partial data (fail closed). `def load_approvers(path: Path) -> frozenset[str]` (one login per line, `#` comments; an empty or missing file raises `CommandError("E-NO-APPROVERS")`, so a missing list never approves everything; the file format and location are a [PROPOSAL]: open Q10). No `gh` call in this module |
| 4.4 | Fixtures | `tests/issue_watch/fixtures/issue-view-*.json`, `events-*.json`, `project-items.json`, `list-numbers.json`, `comments-marker.json` (all NEW) | Hand-written JSON in the shape `gh` documents for the fields requested. The events and comments fixtures are RAW REST pages (full event or comment objects, before any jq filter) so the filters and the raw page length `n` are exercised (step 4.5). `project-items.json` carries a header comment-field `"_assumed_shape": "replace after the owner-run live call (Q8)"` so the assumption is visible |
| 4.5 | Selection and read-only tests | `tests/issue_watch/test_selection.py` (NEW), `tests/issue_watch/test_github_reads.py` (NEW) | Selection (pure, JSON fixtures, the style of `tests/pr_submit/test_ci_classify.py`, R02 §5): each of the five filters rejects on its own with `rejected_by` naming it; an issue assigned to another login is rejected; assigned to own login plus another is rejected; unlabeled after labeled is not approved; labeled by a non-allow-listed actor is not approved; the latest event wins when labeled, unlabeled, labeled again; a missing allow-list file raises; truncation fails closed, and the tests exercise the jq filter rather than skip it: the fixtures are RAW pages of 100 events that hold fewer than 100 label events (for example 40 `labeled`/`unlabeled` events among 60 other events), and the `FakeRunner` serves the page through the same filter semantics as `events-jq`/`marker-jq`, giving `{n: 100, items: [40 entries]}` (the unit-level `FakeRunner` helper applies the filter string it receives in `--jq` to the raw fixture page with `jq -c`, so a wrong filter fails a test; the PATH stub does the same in Phase 6, step 6.1) [DESIGN]. A `FakeRunner` that returns such a raw page of 100 (filtered to fewer than 100 items) for every page up to `max_pages` makes `label_events` raise `E-GH-TRUNCATED`, and the same for `own_claim_comment_ids`; a raw last page of 100 events whose filtered `items` are fewer than 100 does NOT end the read (only `n < 100` does); a raw last page with `n < 100` is read to its end and decided normally (the cycle-level assertion is in `test_cycle.py`, "Truncated read" below). Reads: with `FakeRunner`, every recorded argv starts with `gh`; contains `--repo IronbellyOrg/IronClaude` or a `repos/IronbellyOrg/IronClaude/` path or is `api user` or `project item-list --owner`; every `gh api` call has `--method GET`; no `--json` list contains `title`, `body` or `comments`; no argv contains `SuperClaude-Org` or a `{owner}` placeholder; no argv has a whole token equal to `edit`, `comment`, `create`, `-X` or `--add-assignee`, and none uses `--method` with POST, PATCH, PUT or DELETE (the token list is modelled on `assert_no_retrigger_call`; a path such as `repos/.../comments` is one token and is allowed because it is a GET read); the `-L`/`--limit` value is explicit and 100; a non-integer in a discovery result is dropped and reported; an item with another repository is dropped |

### Phase 5: Dispatch record, at-most-once guards, the poll cycle and the `once` verb

**Goal:** One complete poll cycle: lock, identity, discovery, five filters, GitHub-side and local at-most-once checks, dispatch record written before the launch, launch through the Phase 3 function, and an audit line per decision. Exposed as `superclaude issue-watch once`.
**Dependencies:** Phases 2, 3 and 4.

**What at-most-once can and cannot be under this design** (R01 §9, §10; R03 §7; W02 G1, G7 table): the claim is check-then-act and `--add-assignee @me` adds rather than replaces, so no atomic exclusion exists across logins; GitHub assignment has no compare-and-set (external context https://docs.github.com/en/rest/issues/assignees). The achievable guarantee is: at most one launch per workspace per issue within the lease and the attempt cap, plus best-effort exclusion across logins (intended-owner filter, own claim marker, pre-launch re-read at step 8 of the algorithm below). A post-write re-read of the assignees (W02 G7 [PROPOSAL]) would exist only for routing candidate 4, in which the poller adds `@me` itself; this plan's poller never writes to GitHub (SC-13, step 4.5), so that layer is not built. The claim comment is posted last (Wave 6, `refs/claim.md:84-88`), minutes after the assignment (Wave 3, `:47`), so the marker is a late record and the local record covers the gap. A claim that fails after Wave 3 leaves the issue assigned to the own login with no marker, so it is selected again every cycle; the attempt cap and an "abandoned" report handle it (R01 §10, R02 §2c).

| Step | Action | Files | Details |
|---|---|---|---|
| 5.1 | The dispatch record and the lock | `src/superclaude/cli/issue_watch/state.py` (NEW) | `@dataclass class DispatchEntry: issue: int; state: Literal["pending","launched","unknown","failed","abandoned"]; attempts: int; first_at: str; last_at: str; operation_id: str \| None; approver: str \| None; approval_event_id: int \| None; detail: str`. `class DispatchStore: __init__(self, path: Path); load(self) -> dict[int, DispatchEntry]; save(self, entries: dict[int, DispatchEntry]) -> None` writing a temp file in the same directory and `os.replace` (atomic write via temp file plus rename, W02 A4; same technique as `_atomic_write` in `src/superclaude/cli/init_lite.py` l.221, R02 §4.2, mirrored not imported). A corrupt or missing file loads as empty and the GitHub-side marker check still protects (below). `@contextmanager def poll_lock(path: Path) -> Iterator[bool]`: `fcntl.flock(fd, LOCK_EX \| LOCK_NB)` on `<state-file>.lock`; yields `False` when another run holds it (overlap of a slow run with the next tick is [UNVERIFIED] for `coder_script` cron: W02 A1, Q15). `def may_dispatch(entry: DispatchEntry \| None, *, now: datetime, lease: timedelta, max_attempts: int) -> tuple[str, str]` returning an action (`launch`, `retry-launch`, `wait`, `abandon`) and a reason: no entry gives `launch`; `pending` and `launched` give `wait` until `now - last_at >= lease`, then `launch` while `attempts < max_attempts`, else `abandon`; `unknown` gives `retry-launch` with the stored id while `attempts < max_attempts`, else `abandon` and never a fresh `launch`; `failed` gives `launch` while `attempts < max_attempts`, else `abandon`; `abandoned` gives `wait`. A `pending` record means the process may have died after the launch started, so it is treated like `launched` (the launch reply can be lost after the session started: R01 §12). Defaults [PROPOSAL, the research gives no value for any of these]: lease 60 minutes, `max_attempts` 3, `max_launches` per cycle 1 (W02 recommendation 7 asks for a cap and a retry cap without numbers): open Q13 |
| 5.2 | The poll cycle | `src/superclaude/cli/issue_watch/cycle.py` (NEW) | `@dataclass(frozen=True) class CycleConfig: worktree: Path; trigger_label: str; approval_label: str; approvers: frozenset[str]; project_owner: str \| None; project_number: int \| None; label_only: bool; max_candidates: int; max_launches: int; max_attempts: int; lease: timedelta; dry_run: bool`. `@dataclass class CycleReport: own_login: str; decisions: list[Decision]; launched: list[int]; waiting: list[int]; abandoned: list[int]; failed: list[int]; dropped: list[str]`. `def run_cycle(cfg: CycleConfig, *, gh: Runner, git: Runner, orca: Runner, store: DispatchStore, now: Callable[[], datetime]) -> CycleReport`. The ordered algorithm is the table below |
| 5.3 | The `once` verb and exit codes | `src/superclaude/cli/issue_watch/commands.py` (extend step 2.3) | `@issue_watch_group.command("once")` with the options below. `def build_runners() -> tuple[Runner, Runner, Runner]` returns `(gh, git, orca)` wrappers of `run_command` and is the seam tests replace with `monkeypatch.setattr`, as `tests/pr_submit/conftest.py:58` patches `detection._fetch_payload` (R02 §3.1). The verb takes the lock, builds `CycleConfig`, calls `run_cycle`, prints one JSON object per decision to stdout (the audit line) and exits with the table's code through `sys.exit(...)` (the `cleanup_audit/commands.py` style, R02 §4.2). `--dry-run` runs the read-only GitHub calls, then prints what would be launched and returns before any record write or launch, the precedent of `cleanup_audit/commands.py:85-87` (`_print_dry_run`, R02 §4.2) |
| 5.4 | State and cycle tests | `tests/issue_watch/test_state.py` (NEW), `tests/issue_watch/test_cycle.py` (NEW), `tests/issue_watch/test_cli_once.py` (NEW) | See the scenario list below |

**Ordered algorithm of `run_cycle`:**

| # | Action | On failure or skip |
|---|---|---|
| 1 | `check_worktree_origin(cfg.worktree, git)` (step 3.3) before any GitHub call | `CommandError("E-WRONG-ORIGIN")`, exit 1 |
| 2 | `own_login = whoami(gh)` | exit 2 |
| 3 | Discovery (`discover_project` or, with `--label-only`, `discover_label_only`); keep only values with `type(n) is int` and `1 <= n <= MAX_ISSUE_NUMBER`, report the others in `dropped`; sort ascending; keep the first `max_candidates` (default 10, [PROPOSAL]) | discovery error: exit 2 |
| 4 | For each number: `snapshot(gh, n)`, then `passes_cheap_filters` (filters 1, 5, open) | rejected with the filter name |
| 5 | For survivors: `label_events` then `is_approved` (filter 2) | rejected with the actor and event id in the detail; `E-GH-TRUNCATED` from `label_events` rejects the issue with reason `approval-unverifiable` (fail closed) |
| 6 | `own_claim_comment_ids(gh, n, login=own_login)`: any id means the claim already ran for this login | skip, reason `already-claimed`; this check runs even when the local record is missing (W02 recommendation 3); `E-GH-TRUNCATED` skips the issue with reason `claim-marker-unverifiable` (fail closed) |
| 7 | `may_dispatch(store entry, ...)` | `wait`, `abandon` (reported) or proceed |
| 8 | Final `snapshot(gh, n)` right before the launch, the pre-launch re-read and the only re-read in the cycle (W01 §14.3 step 3): still open, still assigned to the own login only, approval label still present | skip, reason `changed-before-launch` |
| 9 | If `cfg.dry_run`: record the decision `would-launch` and continue | no record, no launch |
| 10 | If launches this cycle `>= max_launches`: skip with `cycle-cap` | |
| 11 | Write the entry (`pending`, `attempts + 1`, approver login and approval event id from step 5) with `store.save` before launching | save error: do not launch, exit 1 |
| 12 | `launch_claim(n, cfg.worktree, orca=orca, retry_operation_id=...)` where the id is set only for the `retry-launch` action | update the entry to `launched`, `unknown` (keep the id) or `failed` |
| 13 | Emit the audit record: `issue`, `decision`, `reason`, `approver`, `approval_event_id`, `operation_id`, `attempts` (subset of the audit fields W02 J2 proposes, [PROPOSAL]); never any issue text | |

There is no sleep or in-cycle retry. A `CommandError` from a per-issue call skips that issue and is reported; a failure of steps 2 or 3 ends the cycle. The 5-minute cadence is the back-off. How to honor `retry-after` and `x-ratelimit-reset` through `gh` is not shown by the research: open Q23.

**Options of `once`** (names and defaults are [PROPOSAL] unless a source is given):

| Option | Required | Meaning |
|---|---|---|
| `--worktree-path PATH` | yes | absolute path of the existing Orca checkout of the fork; becomes `--worktree path:<abs>` (Q17) |
| `--trigger-label TEXT`, `--approval-label TEXT` | yes | label names; none exist yet and no file chose them (R02 §2; Q9) |
| `--approvers-file PATH` | yes | approver allow-list file (location open: Q10) |
| `--project-owner TEXT`, `--project-number INT` | yes unless `--label-only` | the Project to read (owner and number appear in no file: Q9) |
| `--label-only` | no | skip filters 3 and 4; a degraded mode that is allowed only if the owner accepts it (Q9; W01 §14.3 fallback) |
| `--state-file PATH` | no | default `~/.local/state/superclaude/issue-watch/dispatched.json` (path shape from W02 A4; whether `$HOME` persists across a workspace stop is unknown: Q15) |
| `--max-candidates INT`, `--max-launches INT`, `--max-attempts INT`, `--lease-minutes INT` | no | defaults 10, 1, 3, 60 (Q13) |
| `--dry-run` | no | read-only calls only; no record, no launch |

**Exit codes of `once`** [PROPOSAL, in the table form of `origin_repo.py:45-50`]:

| Code | Meaning |
|---|---|
| 0 | cycle completed (including nothing to do, a held lock, dry-run, per-issue skips) |
| 1 | usage or configuration error: bad option, missing or empty approver file, wrong origin of the checkout, record could not be saved |
| 2 | a GitHub read needed for the whole cycle failed (login or discovery) |
| 3 | the cycle completed but at least one launch failed, ended `unknown`, or an issue was abandoned |

**Test scenarios** (`FakeRunner` for `gh` and `git`, `FakeOrca` for `orca`, a `tmp_path` store, an injected `now`):

| Test | Asserts |
|---|---|
| Happy path | one candidate passes all five filters; exactly one `orca` call with the exact argv of Phase 3; the store file already contains the `pending` entry when `FakeOrca` is called (the mock reads the file inside the call); final entry `launched` |
| Second cycle | same GitHub state, inside the lease: no second `orca` call; after the lease and with no marker: exactly one retry; after `max_attempts`: `abandoned`, reported, exit 3, no further launch |
| Lost record | empty store but the marker comment id list is non-empty: no launch |
| Changed before launch | the final snapshot shows a second assignee: no launch |
| Cycle cap | two eligible issues, `max_launches=1`: one launch, one `cycle-cap` skip |
| Dry run | gh reads happen; no `orca` call; no store file |
| Unknown outcome | entry `unknown` with the id; next cycle's `orca` argv contains `--retry-launch <id>`; no call without it |
| Launch failure | `failed`, attempts incremented, exit 3 |
| Lock held | a second `poll_lock` held by the test: exit 0 with zero calls |
| GitHub failure | login or discovery returns exit 1: exit 2, zero `orca` calls |
| Wrong origin | `git` returns another repo: exit 1 before any `gh` call |
| Hostile text | the snapshot and events fixtures contain a hostile `title`, `body` and comment text although none was requested; no `orca` argv element and no audit line contains it; the prompt is exactly `/sc:issue --claim <int>` |
| Non-integer discovery value | `"331"`, `3.0`, `True` from discovery are dropped and listed in `dropped`; no call is made for them |
| Truncated read | the events fixture is a raw page of 100 events for every page up to `max_pages`, each page holding fewer than 100 label events (for example 40), so the filtered `items` are shorter than 100 while `n == 100`: the issue is rejected with `approval-unverifiable`, no `orca` call, no store write; the comments fixture (raw pages of 100 comments, few of them own claim comments) likewise gives `claim-marker-unverifiable`; a page with `n == 100` but fewer than 100 filtered items followed by a page with `n < 100` is read to its end and decided normally; a single raw page with `n < 100` is read to its end and decided normally |
| Registration of the verb | `["issue-watch", "--help"]` lists `once` (extends step 2.6) |

### Phase 6: End-to-end tests with PATH stubs, acceptance criteria and quality gates

**Goal:** Prove with the repo's own `gh` mocking style that the real entry point, the real `subprocess` runner and the real argv reach fake `gh`, `git` and `orca` executables, and run every gate the repo applies. Nothing live.
**Dependencies:** Phases 2 to 5.

The repo's actual way of mocking `gh` is a bash executable named `gh` written into a temp directory that is prepended to `PATH` in the child's environment, with the code under test run as a real subprocess and the stub logging its argv for the test to read back (R02 §3.4, [CODE-VERIFIED]): `tests/pr_submit/test_conflict_e2e.py:118-146,166-169` (`_GH_STUB`, `install_gh_stub`, `gh(repos, *args)` running `["gh", *args]`), `tests/pr_submit/test_conflict_scripts.py:161-200` (`make_repos`, the `bin_dir` and `PATH` prefix at l.179), `test_codex_reviews.py:554-581`, `test_static_grep.py:341-378`, `test_cosmos_poll.py:100-190` (a stub that logs argv as JSON with `jq -nc --args '$ARGS.positional' -- "$@"` and rejects calls lacking `--repo` with exit 91). No Python-level `gh` mock exists to reuse; `mock_gh` patches a payload function (R02 §3.1). **The new tests use both styles:** the injected runner for unit and cycle tests (Phases 2 to 5) and the PATH stub for the end-to-end tests below, so the argv that actually reaches an executable is asserted.

| Step | Action | Files | Details |
|---|---|---|---|
| 6.1 | Stub installer | `tests/issue_watch/conftest.py` (extend) | `def install_stubs(tmp_path: Path, *, gh_script: str, git_script: str, orca_script: str) -> Path`: writes executables `gh`, `git`, `orca` into `tmp_path / "bin"`, `chmod(0o755)`, returns the directory; a `monkeypatch.setenv("PATH", f"{bin_dir}{os.pathsep}{os.environ['PATH']}")` fixture, as in `make_repos` (`test_conflict_scripts.py:161-180`). Each stub logs its argv to a calls file as one JSON line (the `test_cosmos_poll.py:100-190` technique, which needs `jq`; skip the e2e tests with `pytest.skip` when `shutil.which("jq")` is `None`), serves canned JSON from `tests/issue_watch/fixtures/` (for a `gh api ... --jq <filter>` call the stub pipes the raw fixture page through `jq -c "<filter>"` with the filter it received, so the real `events-jq`/`marker-jq` are exercised and `{n, items}` is produced from raw pages [DESIGN]), and exits 99 with `unexpected call` for any argv it does not recognise. The `gh` stub exits 91 when a call lacks `--repo IronbellyOrg/IronClaude` and is not `api user`, `project item-list --owner ...` or a `repos/IronbellyOrg/IronClaude/...` path (the `test_cosmos_poll.py` rule) |
| 6.2 | End-to-end tests | `tests/issue_watch/test_e2e_pathstub.py` (NEW) | `CliRunner().invoke(main, ["issue-watch", "once", "--worktree-path", str(tmp_path / "checkout"), ...])` with the stubs on `PATH` (the invocation style of `tests/recommend/test_cli_registration.py` and `tests/cli/test_init_lite.py:34-35`, R02 §5). Asserts: exit 0; the `orca` calls file has exactly one line and its argv equals the list in the Phase 3 contract table; the `gh` calls file contains no write-shaped call (token check in the style of `assert_no_retrigger_call`, `test_conflict_e2e.py:178-186`, whole tokens: `edit`, `comment`, `create`, `-X`, `--add-assignee`, and a `--method` other than `GET`); no recorded argv contains `SuperClaude-Org`; the audit lines on stdout contain the issue number and approver and no issue text; a second invocation with the same stub state produces no second `orca` line |
| 6.3 | Static guard tests | `tests/issue_watch/test_static_guards.py` (NEW) | Reads the package source files and asserts: no `shell=True`, no `os.system`, no `os.popen` (the poller is a plain argv-list caller); no string `SuperClaude-Org`; the only occurrence of the literal `IronbellyOrg/IronClaude` as a repo constant is in `models.py` (`REPO`). The repo already asserts repo-scoping of `gh` lines in bash scripts with regex helpers (`test_static_grep.py:30,:106`, R02 §3.4); here the argv are Python lists, so the dynamic checks of steps 4.5 and 6.2 carry that rule and this test adds only the no-shell checks |
| 6.4 | Acceptance criteria (copied into the design doc, step 1.10) | `docs/designs/issue-watcher.md` | 1. `superclaude issue-watch --help` lists `once`. 2. The only text derived from an issue in any launch argument is one integer from 1 to 999999999, and the prompt equals `/sc:issue --claim <int>`. 3. No `gh` call made by the package is write-shaped, and every call pins `IronbellyOrg/IronClaude`. 4. An issue is selected only if it passes all five filters (tagged, human-approved by an allow-listed actor, in the Project, Status Backlog, assigned to the own login only), or `--label-only` is given and logged. 5. The dispatch record exists before the launch is called. 6. A second cycle on unchanged state starts no second session. 7. A lost record with an own claim marker on the issue starts no session. 8. `--dry-run` makes no launch and writes no record. 9. An unknown launch outcome is retried only with `--retry-launch <operationId>`. 10. `uv run pytest tests/issue_watch/ -v` passes with `gh`, `git` and `orca` mocked and nothing run live; ruff, `make lint-architecture` and `make verify-deps` pass |
| 6.5 | Run the gates | none (commands) | `uv run pytest tests/issue_watch/ -v`; `uv run pytest tests/cli/test_cli_registration.py tests/issue_watch/test_cli_registration.py -v`; `make format` then `uv run ruff format --check src/ tests/`; `uv run ruff check src/ tests/`; `uv run pytest` (CI runs `pytest -v --tb=short --color=yes -n auto --maxfail=3 --ignore=tests/cli/test_verify_sync_hooks.py` after `make sync-dev`, `.github/workflows/test.yml:38,46-47`); `make lint-architecture`; `make verify-deps`. Smoke check only: `uv run superclaude issue-watch --help` and `uv run superclaude issue-watch once --help` (no GitHub call). Only declared pytest markers may be used (`--strict-markers`, `pyproject.toml:107-117`); tests write only under `tmp_path`, never under `docs/mistakes` or `docs/memory/solutions_learned.jsonl` (`tests/conftest.py` pollution guard, R02 §5) |

### Phase 7: Trigger and approval label setup instructions, approver and scope setup, operator notes

**Goal:** Instructions a maintainer can follow later; nothing in this phase is run. They go into the design doc as a section, so no new file type or index is needed.
**Dependencies:** Phases 1 and 5 (option names).

| Step | Action | Files | Details |
|---|---|---|---|
| 7.1 | Label creation lines in the house format | `docs/designs/issue-watcher.md` (section "Label and approver setup") | One-time maintainer lines in the form of `src/superclaude/skills/sc-issue-protocol/refs/labels.md:22-42`: `gh label create "<trigger-label>" --repo IronbellyOrg/IronClaude` and `gh label create "<approval-label>" --repo IronbellyOrg/IronClaude`. The names are placeholders because none exists and no file chose them (the fork has only the 9 default labels: R02 §2): open Q9. State who may do what: creating a label needs Write, applying a label needs Triage or higher, 3 accounts hold such a role today (R03 §4.2, observed 2026-11-07). State that `/sc:issue` never creates labels and `--claim` changes none (`refs/labels.md:7`), so these lines are the only way the labels come to exist. Also state that the `type: *` and `complexity: *` labels `/sc:issue --create` expects are missing on the fork and are not part of this work (R02 §2b; owner choice) |
| 7.2 | Approver allow-list setup | same section | The file read by `--approvers-file`: one GitHub login per line, `#` comments, to be filled with the Triage-or-higher accounts that may approve. Where the file lives (repo file, org team, CODEOWNERS-like list) is open: Q10. Explain the rule the poller applies (latest `labeled` event of the approval label by an allow-listed actor) and its limits: an edit of the issue body after approval is not detectable (Q11), and the claim reads title, body and comments live (Q12) |
| 7.3 | Per-developer Project read scope | same section | Each polling `gh` login needs `read:project` to read the org Project; the observed workspace token lacks it and `gh project list --owner IronbellyOrg` failed with "missing required scopes [read:project]" (R03 §4.2). Documented command form: `gh auth refresh -s read:project` (external context https://cli.github.com/manual/gh_auth_refresh; acceptance of this exact scope name and the `GH_TOKEN`-injected case are [UNVERIFIED]: Q7). A fine-grained token with organization Projects = Read is the least-privilege alternative (W01 §9, external context). `--label-only` avoids the scope at the cost of filters 3 and 4 (Q9) |
| 7.4 | Routing and Project set-up | same section | Intended-owner rule as implemented (routing candidate 1): a Triage-or-higher person assigns the issue to the developer, and the issue must be in the Project with Status Backlog; the Project owner, number and Status name are open: Q9, Q4. State the consequence the research records: the assignee persists after the claim, so it cannot mark "already dispatched" (R01 §9) |
| 7.5 | Scheduler follow-up text (Coder repo, not built here) | same section, "Follow-up" | The in-workspace scheduling primitive that the research documents (external context https://registry.terraform.io/providers/coder/coder/latest/docs/resources/script): a `coder_script` with `cron = "0 */5 * * * *"` (six fields, seconds first; the provider's own example is a five-minute job) whose `script` runs the verb. Facts to state: the cron job runs only while the workspace runs and is not Coder "activity", so it neither keeps a workspace alive nor polls while stopped (W02 A2, A3); issues approved meanwhile wait on GitHub until the next start; the verb takes its own lock because overlap behavior of a still-running cron script is [UNVERIFIED] (Q15); whether `$HOME`, hence the default state file, survives a stop is unknown (Q15). Example command line shown as text only: `superclaude issue-watch once --worktree-path <checkout> --trigger-label <name> --approval-label <name> --approvers-file <path> --project-owner <org> --project-number <n>` |
| 7.6 | Owner-run live test checklist (written, not run) | same section | Each check is a single read-only or single-launch action by the owner, with the question it closes: (1) launch with a harmless leading slash command as `--prompt` and see whether it runs, and whether argv or typed paste (Q1, Q2); (2) `orca agent launch --retry-launch` argument needs (Q3); (3) `gh project item-list <n> --owner <org> --query "status:Backlog label:<name> assignee:@me" --format json -L 100` accepts the filter and show its JSON shape (Q8); (4) `gh auth refresh -s read:project` works on a workspace login (Q7); (5) one workspace's permission mode for a launched session (Q6); (6) scheduler availability, overlap and `$HOME` persistence in the target template (Q15); (7) the REST comment object's author field name (Q11); (8) whether the `--worktree` path used is the right checkout (Q17) |

### Test plan summary

| Test file (all NEW, under `tests/issue_watch/`) | Style | Pins |
|---|---|---|
| `test_cli_registration.py` | CliRunner against `main` | group in `--help`, verb `once` listed |
| `test_runner.py` | monkeypatched `subprocess.run` | argv list, no shell, missing tool and timeout mapped to `CommandError` |
| `test_prompt_validation.py` | parametrized pure function | integer-only prompt (owner decision D3) |
| `test_launch_contract.py` | `FakeOrca` | exact `orca agent launch` argv, outcomes `started`, `failed`, `unknown`, `--retry-launch`, origin check |
| `test_selection.py` | pure functions over JSON fixtures | each of the five filters, approver rule, shared "assigned to someone else" predicate |
| `test_github_reads.py` | `FakeRunner` | read-only calls, repo pin, `--method GET`, no title, body or comments requested, explicit limit |
| `test_state.py` | `tmp_path` | atomic save, corrupt file, lock contention, `may_dispatch` table |
| `test_cycle.py` | `FakeRunner` plus `FakeOrca` | record-before-launch, no relaunch, lost record, caps, dry run, hostile text, failures |
| `test_cli_once.py` | CliRunner with `build_runners` monkeypatched | options, exit codes, audit lines |
| `test_e2e_pathstub.py` | PATH-stub executables for `gh`, `git`, `orca` | real subprocess path and recorded argv |
| `test_static_guards.py` | source scan | no shell, no upstream repo string |

Commands: see step 6.5. Nothing in the test plan calls GitHub, Orca or Coder for real.

### Rollback and disable considerations

| Situation | Action | Evidence |
|---|---|---|
| The code is merged but nothing schedules it | Nothing runs; removing the two-line registration block in `src/superclaude/cli/main.py` and the package directory reverts it with no effect on other commands | R02 §4.1: registrations are independent blocks; no `pyproject.toml` change |
| A scheduler entry exists (follow-up in the Coder repo) | Disable by removing or disabling the `coder_script` cron entry in the template; the verb has no daemon mode, so nothing keeps running after the entry is gone | W02 A1 (external context) |
| Stop selection without touching the scheduler | Remove the approval label from the issue, unassign the developer, or empty the approver file (an empty or missing file makes the cycle exit 1 and approve nothing, step 4.3) | R03 §4.3 |
| Inspect without acting | `superclaude issue-watch once --dry-run` makes read-only calls, no launch and no record | step 5.3 |
| Bound the damage of a bad cycle | `max_launches` (default 1) and `max_attempts` (default 3) cap sessions per cycle and per issue [PROPOSAL values: Q13] | W02 recommendation 7 |
| Reset the local record | Delete the state file; an issue that already carries the own claim marker is still not relaunched because the marker check runs first | W02 recommendation 3 |
| A session was already launched | Nothing in this design recalls or closes it: a started Orca session stays open after the claim stops [UNVERIFIED inference, Q21]; the person closes it | R01 §12, §Gaps |

### Follow-up, not in this plan

The owner decided option A. These items are recorded, not planned. Nothing here is built, scheduled or deployed by this plan.

| Item | Why it is not in this plan | Boundary or source |
|---|---|---|
| Option B: GitHub Action selects and calls an authenticated workspace listener | Not the owner's choice; needs the Coder#477 listener, registration and transport plus the first `schedule:`/`issues:` workflow in this repo (none exists: R02 §1) and a privileged token | The listener, registration and transport are Coder repo work (IronbellyOrg/Coder#477); this repo would own only the selector/sender side and the contract (S03 §6.2; W02 J1, J2) |
| Option C: central microservice (GitHub App, webhooks) plus the same listener | Not the owner's choice; needs a service to host (hosting not established), a GitHub App and the Coder#477 listener | Same boundary (S03 §6.3; W01 §12) |
| IronbellyOrg/Coder#477 | Filed assuming a push design; option A makes it unnecessary unless B or C is revisited. Whether to relabel, narrow or close it is a decision for its owner in the Coder repo | NOTES ADDENDUM 2 |
| Option D: label relay (a scheduled Action writes a "ready" marker, workspaces poll it label-only) | Adds a workflow, a secret and a label while keeping the poller; first fallback if workspace tokens cannot read the org Project (revisit condition 6) | S03 §6.4 |
| Scheduler entry and persisted state in the Coder template | Lives in the Coder repo (`coder_script` cron, `$HOME` persistence); only the instruction is written here (step 7.5) | W02 A1, A4; GAPS 9 |
| Headless launch variant `claude -p "/sc:issue --claim <int>"` | Changes only the launch step; the owner chose the Orca route; whether the claim completes under `-p` is untested | W02 C1 to C3; GAPS 8 |
| A "wake a stopped workspace" design | Mentioned for push designs only (`coder ssh` auto-start); no research file evaluates it as its own design | S03 §6.4 "Further hybrids" |
| Live deployment and the owner-run live test | Out of scope by the owner decision; the checklist is written in step 7.6 | NOTES ADDENDUM 2 |
| A claim-side change to how `/sc:issue --claim` reads untrusted issue text | Not part of a claim-only watcher; the policy is open (Q12) | R03 §3.2 |
| `/sc:issue --claim --pipeline <level>` and the launch-level guard | Design only; B-CTX gates only that later extension | R03 §1.2, §1.3 |

**Revisit conditions for options B and C** (the owner decided A; revisit only if one of these is shown to hold; none has been observed; from S03 "Revisit conditions"):

| # | Condition | Option it would favor | Source |
|---|---|---|---|
| 1 | Workspaces are mostly stopped and approved issues wait too long; the owner wants a design that can start a stopped workspace | B or C (wake through the Coder control plane at the price of a privileged token; a push design does not recover missed webhooks by itself) | W02 J3 item 1, B2; W01 §12, §14.5 |
| 2 | Poll latency or API use becomes a problem (many workspaces share one login, a very large unfiltered Project, GraphQL-only polling) | B or C | W02 J3 item 2; W01 §14.2 |
| 3 | A need for central audit and one approver policy that per-workspace pollers cannot enforce consistently | B or C | W02 J3 item 3; R03 §7 |
| 4 | Double claims by the same login in several workspaces, or by two logins, occur despite the best-effort checks | B or C (single decision point plus durable idempotency key) | W02 J3 item 4, G1, G7; R01 §9 |
| 5 | Coder ships the workspace-to-account binding as a platform feature | B or C | W02 J3 item 5, E1 |
| 6 | The workspace `gh` token cannot read the org Project while a central credential can | D first; B or C if a GitHub App with org Projects read is preferred | W01 §14.5, §9; R03 §4.2 |
| 7 | A need to react to a Project Status change at event time or to see who moved an issue to Backlog | C (`projects_v2_item` webhook with `changes`) | W01 §3, §14.5 |
| 8 | A need for a shared at-most-once ledger across logins or workspaces | B or C | W01 §14.5 |
| 9 | Workspaces cannot run a recurring poller (the cron primitive is unusable in the target template or state cannot persist) | Not settled by the research; a central selector would be considered | W02 A1, A4, A5; GAPS 9 |

If none holds, option A stays and Coder#477 is unnecessary (S03; NOTES ADDENDUM 2).

### Integration Checklist

- [ ] Design doc `docs/designs/issue-watcher.md` exists in the house format and records D1, D2, D3, the Coder#477 statement, the integer-only prompt rule, the `orca agent launch` contract with its UNVERIFIED rows, and the follow-up table
- [ ] `src/superclaude/cli/issue_watch/` contains `__init__.py`, `commands.py`, `runner.py`, `models.py`, `github.py`, `selection.py`, `launch.py`, `state.py`, `cycle.py`
- [ ] `src/superclaude/cli/main.py` has exactly one new block after the `reflect` registration (l.559-561) with the `# noqa: E402,I001` marker and `main.add_command(issue_watch_group, name="issue-watch")`
- [ ] No `pyproject.toml` change, no new dependency, no `.claude/` mirror change, no workflow change
- [ ] The `gh` runner is the NEW `runner.py`; nothing imports `src/superclaude/pr_submit/ci.py` as a `gh` wrapper
- [ ] The only issue-derived launch text is one integer built by `build_claim_prompt`; no `--json` list requests title, body or comments
- [ ] All five filters (tagged, human-approved, in the Project, Status Backlog, intended owner) are implemented and tested; `--label-only` is logged as degraded
- [ ] Every `gh` call pins `IronbellyOrg/IronClaude`, every `gh api` call has `--method GET`, no write-shaped call exists
- [ ] The dispatch record is written before `orca agent launch`; a lost reply is retried only with `--retry-launch <operationId>`
- [ ] Tests mock `gh`, `git` and `orca` (injected runner and PATH stubs); nothing runs live; tests write only under `tmp_path`
- [ ] `uv run pytest tests/issue_watch/ -v`, `uv run ruff check src/ tests/`, `uv run ruff format --check src/ tests/`, `uv run pytest`, `make lint-architecture`, `make verify-deps` pass
- [ ] Label creation lines, approver file, `read:project` setup, scheduler follow-up text and the owner-run live test checklist are in the design doc
- [ ] Every `open:` item of this plan has a row in Section 9; none is stated as fact in the design doc
- [ ] `.dev/tasks/` is staged; `.claude/` content is not staged; the PR is opened only with `/sc:pr-submit --monitor 3` (project CLAUDE.md rules)

---

## 9. Open Questions

### 9.1 Decided by the owner (not open questions)

Source: NOTES ADDENDUM 2 (2026-11-07T07:12Z, relayed by the coordinator, message sent 2026-11-07T07:04:56Z). It supersedes point 1 of the addendum of 07:03Z.

| ID | Decision | Consequence recorded in the plan |
|---|---|---|
| D1 | Q1 = option A, the workspace-side poller: each workspace polls GitHub every 5 minutes with its own `gh` login and starts the claim via `orca agent launch`; no listener, no inbound port, no address registry | The plan targets A only (Section 8) |
| D2 | Q2 = claim-only: the watcher's job ends at starting `/sc:issue --claim <N>`; the pipeline after the claim stays manual (NOTES ADDENDUM point 3) | The launch prompt is exactly `/sc:issue --claim <int>` |
| D3 | Q3 = only a validated integer issue number reaches the session prompt, never issue title or body text (NOTES ADDENDUM point 3) | `build_claim_prompt` (step 3.2) |
| D4 | Repo-side deliverable: design doc, a tested poller script or CLI (mock `gh` and mock `orca agent launch`, nothing run live), trigger and approval label setup instructions | Phases 1 to 7 |
| D5 | **IronbellyOrg/Coder#477 (workspace listener and registration, open, read 2026-11-07) was filed assuming a push design; option A makes #477 unnecessary unless the push-design alternatives are revisited.** Its listener, registration and transport live in the Coder repo, not in IronClaude | Recorded in the design doc (step 1.2) and in the closing follow-up table of Section 8 |
| D6 | The push-design alternatives (Action plus listener, central microservice plus listener) and any live deployment are recorded as follow-up | Closing table and nine revisit conditions in Section 8 |

### 9.2 Open questions

Each row is an [UNVERIFIED] item, an open decision, or a detail the addenda leave open. Section 8 flags the plan steps that depend on a row with `open: ... (Qn)`.

| # | Question | Impact | Suggested Resolution |
|---|---|---|---|
| Q1 | [UNVERIFIED] Does `/sc:issue --claim <N>` given as the initial `--prompt` of `orca agent launch` run as a slash command and get submitted? No file shows it; `WORKER-CONTRACT.md:93` arranges that Task text "never starts with `/sc:`" without saying why (R01 §12, §13; GAPS 1) | High: if it does not execute, the whole launch route fails, though every test would still pass because `orca` is mocked | One owner-run live launch with a harmless leading command (checklist item 1, step 7.6). Until then the design doc states the route as unproven |
| Q2 | [UNVERIFIED] Argv versus typed paste for `--prompt` (Claude has `promptInjectionMode: 'argv'` but the `agent launch` path lives in the host runtime); exact JSON key nesting of `--json` success output; real JSON error body of `reportCliError`; values of the `prompt{outcome}` field, including what the output shows when an empty prompt is dropped (R01 §12; R03 gap 4 on prefill; GAPS 2) | Medium: the mock shapes are assumptions; a prefilled prompt would not run unattended | Capture one real success and one real failure output during the live test and replace `fixtures/orca-launch-*.json` |
| Q3 | [UNVERIFIED, derived from R01 §12 spec note] Does `--retry-launch <operationId>` replay the whole launch by itself, or must `--agent`, `--worktree` and `--prompt` be repeated? The plan repeats them | Medium: a wrong form could start a fresh launch or be refused | Check `orca agent launch --help` text for `--retry-launch` on the target host, then the live test |
| Q4 | Open decision: the intended-owner rule. Four candidates (assigned to own login, per-person label, Project field, first-come); the research supports candidate 1 and no file shows the owner's choice (R01 §9; R02 §2c; W01 §14.4; S03 §7.4; GAPS 3, 15). The plan implements candidate 1 behind one replaceable function | High: decides who must assign issues and whether a race exists | Owner chooses; if candidate 1, document that a Triage-or-higher person assigns the developer |
| Q5 | [UNVERIFIED per host] Coder workspace facts: an Orca runtime reachable by a scheduler-started process (`orca agent launch` needs a running Orca runtime: R01 §12), `ccsession-orca` configured, `claude-gw-tier3/2/1a` picker IDs served (else the claim stops at Wave 1 for every issue), `gh` authenticated as the person, ClickUp variables (R01 §2, §11, §12; GAPS 4) | High: a misconfigured host fails every issue; the attempt cap then abandons each one | Per-host preflight checklist in the design doc; first live test on one workspace |
| Q6 | [UNVERIFIED] Permission mode of the launched session. `CCSESSION_PERMISSIONS=default` does not by itself prevent bypass because Orca's default `--dangerously-skip-permissions` still applies (`ccsession-tag/README.md:534`); on the observed machine `agentDefaultArgs.claude` is that flag; whether the `orca agent launch` CLI route applies `agentDefaultArgs` was not traced (R03 §2.2, §2.3, gap 5; R01 §11; GAPS 4) | High (security): an injected session may run with the owner's full access | Owner decision on the permission posture; trace the CLI route; state the posture in the design doc |
| Q7 | [UNVERIFIED] Can each polling `gh` login read the org Project? The observed token lacks `read:project`; `gh auth refresh -s read:project` is the documented command form but acceptance of that scope name and the case of a `GH_TOKEN`-injected login are not shown (R03 §4.2; W01 §7, §9, §13, gaps 8; GAPS 5) | High for filters 3 and 4 | Per-developer scope refresh (step 7.3) or the owner allows `--label-only` |
| Q8 | [UNVERIFIED] Does `gh project item-list --query "status:Backlog ..."` (or the REST items route `q`) accept the UI filter syntax? JSON schema of `item-list`, whether items carry the content repository, Status, and whether `gh issue list --json projectItems` exposes a Status name (only secondary cli/cli issue evidence) (W01 §7, §8, §13, gaps 3, 4; R02 gaps 2; GAPS 11) | High: discovery depends on it; the plan fails closed on unreadable status or repository | The owner-run call in checklist item 3; replace `project-items.json` |
| Q9 | Open decision: trigger label name, approval label name, Project owner, Project number, the Status field name, and whether `--label-only` (dropping filters 3 and 4) is acceptable. Nothing defines them; the fork has only the 9 default labels and none of the `type:*` / `complexity:*` labels (R02 §2, §2b; GAPS 12, 5) | High: required options have no defaults | Owner supplies the names; the design doc Defaults table records them |
| Q10 | Open decision: the approver allow-list. The repo has none. Where is it kept (repo file, org team, CODEOWNERS-like list) and is "latest `labeled` event by an allow-listed account" the rule? Under A each workspace holds its own copy (R03 §4; W02 J3 item 3; GAPS 14) | High (security): approval strength | Owner decides location and rule; the plan reads a file passed with `--approvers-file` |
| Q11 | [UNVERIFIED] Trust signals for approval: whether a post-approval edit of the issue body is detectable (no documented field; a body hash at approval is a [PROPOSAL]); issue-event retention (no period stated); whether a Projects v2 Status change appears in the issue timeline; the author-login field name in the REST comment object used by the marker check (the research shows `author_association`, `since` and the PATCH route only); `gh` coverage of issue events without `gh api` (W01 §11, gaps 9; W02 G2, gap 12; R03 gap 7; GAPS 10) | Medium: approval does not freeze the text the claim reads | Accept as documented residual risk (Q12) or add a body-hash check later; confirm the field name in the live test (checklist item 7) |
| Q12 | Open decision: policy for the claim's own reads of issue title, body and comments. The integer-only rule protects the prompt, not the session; the repo is public; the claim posts worker output to a public issue without review. Options: accept as a documented risk, restrict to approved authors by `author_association`, lock the conversation on approval, change the claim to read less (R03 §3.2, §3.3, gap 6; W02 F1, F3, F5; GAPS 13) | High (security) | Owner decision recorded in the design doc; a claim-side change is a separate piece of work |
| Q13 | Open decision: at-most-once parameters. Lease length, `max_attempts`, `max_launches` per cycle and `max_candidates` (the plan uses 60 minutes, 3, 1, 10 as [PROPOSAL] values; the research gives none) and the real race window between claim Wave 1 and Wave 3, which was not measured (W02 G4, recommendation 7; R01 §9; GAPS 15) | Medium: too short a lease can relaunch a running claim; too long delays a retry | Owner confirms values in the Defaults table; measure one claim's duration in the live test (ClickUp alone can take up to 20 pages at 30 s each: R01 §6) |
| Q14 | [UNVERIFIED] Same-login multi-workspace case and multi-assignee behavior: one person with several workspaces polling with one login is not stopped by any assignee check; the double-claim outcome is derived from code and from the additive assignment API, not observed (R01 §9; W02 G1; GAPS 3, 24) | Medium: duplicate sessions and comments | Ask whether anyone runs several workspaces; if yes, the GitHub-side marker check is the only cross-workspace guard |
| Q15 | [UNVERIFIED] Where the 5-minute poller runs and keeps its record in the target template (`VSCode-AIDev02`, known only through the sibling issue text): whether a still-running `coder_script` cron job overlaps the next tick, what the agent does with cron on stop, whether `$HOME` is persisted, systemd or system cron availability, whether a daemonized child of a `run_on_start` script survives, and whether an Orca-launched Claude session counts as Coder "activity" (W02 A1 to A5, gaps 2 to 5; R01 gaps 9; R03 gap 15; GAPS 9) | High: decides whether the poller runs at all and whether its record survives | Check the template in the Coder repo; the verb already takes its own lock and treats a lost record as safe because of the marker check |
| Q16 | [UNVERIFIED outside this repo] Does the Coder workspace owner always equal the `gh` login of the workspace? Coder external auth is documented per user but the pages do not guarantee the owner's identity is always used (R03 gap 14; W02 B3, gap 10; GAPS 19) | Medium: the binding is the `gh` login read each cycle, not the Coder owner | Keep reading the login each cycle (plan step 4.2); ask the Coder repo whether a check is wanted |
| Q17 | [UNVERIFIED] Which existing Orca checkout of the fork the launch uses (the CLI takes `--worktree-path`; no file shows code that picks one; the claim writes `.dev/issues/<N>/` into it); whether the `issue:<number>` selector triggers the Orca-to-GitHub linking the project rule forbids (so `path:` is used); how the poller learns its path since there is no `--repo` flag (R01 §12, F5; R03 §5, gap 12; GAPS 16) | Medium | Owner names the checkout per workspace in the scheduler entry; keep `path:` |
| Q18 | [UNVERIFIED] Does a claim re-run tolerate an already existing `.dev/issues/<N>/` directory? `refs/claim.md:18` says only "Create `<D>`" (R01 §10, gaps 7; GAPS 7) | Low to medium: matters for a retry after a partial claim | Run one claim twice in the live test |
| Q19 | Do tests pin the claim-stops-after-`next-steps.md` text? `tests/commands/test_issue_command.py` has no hit; other test files were not read (R01 gaps 6; GAPS 6) | Low: claim-only leaves the stop text unchanged | `grep` the other test files if the stop text is ever changed |
| Q20 | [UNVERIFIED] Does `/sc:issue --claim` work under `claude --print`? The official page says custom commands expand in `-p`; end-to-end behavior of this command is untested (W02 C1 to C3, gap 15; R01 gaps 8; GAPS 8) | Low: only for the headless variant listed as follow-up | Test only if the owner revisits the launch route |
| Q21 | [UNVERIFIED] A poller-launched ordinary session is outside the never-as-worker list as owner intent (the reading is the researcher's, from `WORKER-CONTRACT.md:11, :23`); an Orca-started Claude session stays open after the claim stops (inference from `SKILL.md:88`) (R01 §7, §12, gaps; GAPS 24) | Medium: governance reading; tabs may accumulate | Owner confirms the reading in the design doc review |
| Q22 | [NOT READ] Bodies of `freshness-pre-edit.sh`, `sc-recommend-phase0.sh`, `issue-worker-t2.md`, `issue-worker-t1.md`, `tests/cli/test_install_hooks.py` (R03 gap 13; GAPS 18) | Low | Read them before the design doc states what constrains a launched session |
| Q23 | [UNVERIFIED] Rate-limit handling through `gh`: how to read `retry-after` and `x-ratelimit-reset`; whether `gh` high-level commands can send `If-None-Match`; whether GraphQL supports conditional requests; ETag/304 behavior of the Projects items route (W01 §5, §6, §8, §14.2, gaps 5, 6) | Low at 12 polls per hour (0.24 percent of the allowance per call type) | The plan does no in-cycle retry and uses the cadence as back-off; revisit only if limits are hit |
| Q24 | [UNVERIFIED] Organization policies that could block tokens (classic token restrictions, fine-grained token approval, SSO authorization) and who may create a fine-grained token or App for the org (W01 gaps 7; S03 revisit condition 6) | Medium for filters 3 and 4 | Ask the org owner; fall back to `--label-only` or option D (follow-up) |
| Q25 | [UNVERIFIED] Whether organization owners outside the collaborator list can apply labels, and the permission to edit another user's issue body (R03 §4.2, gap 9; W01 gaps 12; GAPS 17) | Low to medium: widens who can approve | Enumerate org owners before fixing the allow-list |
| Q26 | [UNVERIFIED] Push-design details, relevant only to the revisit conditions: mTLS through Coder, the `Coder-Session-Token` header for non-browser app callers (seen only in Go package docs), the endpoint that starts a workspace, `coder exec` (not found), webhook redelivery window and delivery ordering, hosting of a central service (W02 H3, I2, gaps 6 to 9; W01 gaps 10) | None for A | Research again only if a revisit condition holds |
| Q27 | [UNVERIFIED] No primary-page sentence that `projects_v2_item` is not a workflow trigger, or that `GITHUB_TOKEN` cannot read an org Project (only absence and a secondary gh-aw page) (W01 gaps 1, 2) | None for A | Context only |
| Q28 | [UNVERIFIED] Actions per-job billing rounding, whether search shares the 5,000 per hour bucket, private-repo differences of `schedule` (W01 gaps 11) | None for A | Context only |
| Q29 | [UNVERIFIED] Alternative runtimes and dispatchers not researched or only from snippets: Copilot assignment steps, Codex issue path, Sweep (W02 gaps 11, E3 to E6) | None | Context only |
| Q30 | A "wake a stopped workspace" design was mentioned for push designs and not evaluated (S03 §6.4; W02 J3 item 1) | Low | Evaluate only if revisit condition 1 holds |
| Q31 | Plan-level, not from the research: no research file checked whether any test under `tests/docs/` or elsewhere pins the contents of `docs/designs/`, and the plan's registration needs no routing-table test change only because no command or skill file is added (R02 §6 (c)) | Low | Run the full suite after Phase 1 (step 6.5) |
| Q32 | Plan-level: the PATH-stub style the repo uses logs argv with `jq` (`test_cosmos_poll.py:100-190`); the research does not show that `jq` is present on every CI runner or developer host. The e2e tests skip when `jq` is absent | Low | Confirm in CI output that the e2e tests ran, not skipped |
| Q33 | Is the installed hook set stale on every Coder workspace? The packaged `hooks.json:96-105` registers `launch-job-identity.sh` but this workspace has neither the script nor the registration; what installs hooks on a Coder workspace is unknown (R03 gaps 3) | Low for a claim-only poller (the hook is dormant) | Ask the Coder repo; not needed for the plan |

### 9.3 Corrected carry-overs ([CODE-CONTRADICTED] and stale documentation, handled in the plan, not open)

| # | Claim found false or stale | Correct fact and evidence | How the plan handles it |
|---|---|---|---|
| C1 | Issue text: `/sc:issue --claim` kicks off the full orchestration path (GAPS 20) | The claim stops after `next-steps.md` and never runs next steps: `issue.md:15, :79, :83`, `refs/claim.md:80, :90` (R01 §1, §3) | Claim-only scope (D2); design doc correction row (step 1.3) |
| C2 | `launch-level-guard.sh`, `/sc:issue --claim --pipeline`, the `[sc-launch:v1:<nonce>]` marker and the pre-push layer exist (`docs/designs/sc-issue-launch-level-hook.md:23`) (GAPS 21) | Design only; `launch-level-guard.sh` is absent; `issue.md:35-41` has no `--pipeline`; B-CTX gates only a later pipeline extension (R03 §1.2, §1.3) | Out of scope; recorded in the follow-up table |
| C3 | `launch-job-identity.sh` is installed and registered (hooks.json, installer) | Not installed on the observed workspace; dormant anyway (R03 §2.1) | Not relied upon; Q33 |
| C4 | `src/superclaude/pr_submit/ci.py` is a mockable `gh` subprocess wrapper (GAPS 22) | A pure classifier with no `subprocess` import; no Python `gh` wrapper exists under `src/superclaude` (R02 §3.1, §3.2) | NEW `runner.py` (step 2.2). The same wrong claim was corrected in `.dev/brainstorms/20261107-064825-github-issue-watcher/enrichment/codebase-context.md` (line 21) and in `research/research-notes.md` (lines 30, 37) |
| C5 | `tests/pr_submit/conftest.py:3-8` describes `mock_gh` as a gh-wrapper seam that asserts the `--repo` pin; `tests/cli/test_cli_registration.py:28-30` calls the top-level set a frozen snapshot that forces updates (GAPS 23) | `mock_gh` patches `detection._fetch_payload` and records PR numbers; `swarm` and `reflect` are registered but absent from the set (R02 §3.1, §4.3) | The plan neither imports `mock_gh` nor edits the frozen set |
| C6 | Project CLAUDE.md calls the fork private | `IronbellyOrg/IronClaude` is PUBLIC, checked 2026-11-07 (R03 §3.3) | Security model treats issue text as written by the public (step 1.6) |
| C7 | `src/superclaude/hooks/README.md:3-19` says the hooks directory holds only configuration; `.dev/orca-command-refactor/inventory/orca-capabilities.md:66` is a team-written inventory; the issue forms still carry Orca text (R03 stale list; R01; R02) | The hooks directory also holds `scripts/`; the pull-only statement was re-found in `bundled-skill-guides.js:3158, :2413`; forms are inherited | Not relied upon; excluded from the plan as irrelevant to the deliverable |
| C8 | "Slash commands are only available in interactive mode" (old third-party mirror) | The official headless page says user-invoked skills and custom commands work in `-p` (W02 C1) | Official page governs; the headless variant is follow-up only |
| C9 | W02 J3 item 2: GitHub rate-limit numbers "not researched" | W01 §4, §14.2 and W02 K give the limits (S03 contradiction 3) | W01 governs; used in step 1.5 |
| C10 | Option letters in the web files (W01 "alternative C" for an Action, W02 "option C" for an Action) | The binding naming is B = Action plus listener, C = central microservice plus listener (S03 contradiction 1) | Web findings are mapped by description |
| C11 | R02 §2b earlier text "skip issues that already have an assignee" | One predicate: skip an issue assigned to a login other than the own login (R02 §2c; R01 §9; R03 §4.3) | `is_intended_owner` (step 4.3) |

---

## 10. Evidence Trail

All paths are under `.dev/tasks/to-do/TASK-RESEARCH-issue-watcher-20261107-064950/`. Web research used WebSearch and WebFetch because the Tavily tools were not available to the web agents (W01 and W02 headers: provider=WebSearch/WebFetch, reason=tavily-unavailable). WebFetch returns model-written summaries of pages, so quoted wording is as returned (W02 header note). Web findings are external context and never override verified code behavior.

### Codebase Research

| File | Topic | Agent Type |
|---|---|---|
| `research/01-claim-flow-and-session-launch.md` | `/sc:issue --claim` flow wave by wave, argument validation in `origin_repo.py`, `clickup_claim.py`, never-as-worker list, which `gh` login assigns and routing candidates, idempotence and at-most-once, environment a claim needs, why the claim stops, ways to start a session and the `orca agent launch` argument contract, integer-only prompt | Code Tracer |
| `research/02-github-surface-and-cli-patterns.md` | Workflow triggers, issue forms and labels, where `gh` is invoked and how tests mock it, Click group creation and registration in `main.py`, test layout, Makefile and CI gates and the `.claude/` mirror rule, house design-doc format | Integration Mapper |
| `research/03-governance-and-security-surface.md` | Launch-level hook design versus code, registered hooks and permission settings, untrusted issue text paths, who decides approval and routing, Worker Contract implications, what an injected session could do, security properties provided versus missing | Architecture Analyst |

Binding inputs: `research/research-notes.md` sections "ADDENDUM 2026-11-07T07:03Z" and "ADDENDUM 2 2026-11-07T07:12Z" (owner decision, claim-only, integer-only, Coder#477 statement). Sibling issue IronbellyOrg/Coder#477 is a read-only dependency summarized in the first addendum; its content was not re-read here.

### Web Research (external context)

| File | Topic |
|---|---|
| `research/web-01-github-events-projects-and-limits.md` | Actions `schedule` limits (https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows), `issues` events and `projects_v2_item` webhooks (https://docs.github.com/en/webhooks/webhook-events-and-payloads), REST and GraphQL rate limits and conditional requests (https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api, https://docs.github.com/en/rest/using-the-rest-api/best-practices-for-using-the-rest-api), Projects v2 read access and token types (https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-api-to-manage-projects, https://cli.github.com/manual/gh_project_item-list), issue search and `gh issue list`, issue events for "who applied the label" (https://docs.github.com/en/rest/issues/events), webhook delivery facts, `gh auth refresh` (https://cli.github.com/manual/gh_auth_refresh), cost and filter analysis for option A |
| `research/web-02-coder-claude-dispatch-and-security.md` | Where a 5-minute poller runs in a Coder workspace: `coder_script` cron (https://registry.terraform.io/providers/coder/coder/latest/docs/resources/script), stop behavior and persistence (https://coder.com/docs/admin/templates/extending-templates/resource-persistence), autostop and activity (https://coder.com/docs/user-guides/workspace-scheduling); Coder reachability, CLI, tokens, external auth (https://coder.com/docs/admin/networking); `claude -p` and the Claude Code GitHub Action (https://code.claude.com/docs/en/headless, https://code.claude.com/docs/en/github-actions); comparable dispatchers (https://github.com/coder/create-task-action); prompt-injection guidance (https://code.claude.com/docs/en/security, https://genai.owasp.org/llmrisk/llm01-prompt-injection/); at-most-once patterns (https://docs.github.com/en/rest/issues/assignees); sender authentication, `coder_app` sharing and the minimal contract for the push-design alternatives |

### Synthesis files

| File | Report sections | Used by this file |
|---|---|---|
| `synthesis/synth-01-problem-current-state.md` | 1 Problem Statement, 2 Current State Analysis | Owner decisions, Coder#477 boundary, claim flow facts |
| `synthesis/synth-02-target-gaps-external.md` | 3 Target State, 4 Gap Analysis, 5 External Research Findings | Target flow, gap table, external findings |
| `synthesis/synth-03-options-recommendation.md` | 6 Options Analysis, 7 Recommendation | Recommendation (option A), intended-owner filter, poller rules, repo fit, revisit conditions |
| `synthesis/synth-04-plan-questions-evidence.md` (this file) | 8 Implementation Plan, 9 Open Questions, 10 Evidence Trail | |

Gaps Log: `.dev/tasks/to-do/TASK-RESEARCH-issue-watcher-20261107-064950/gaps-and-questions.md` (24 numbered gaps and the merged stale-documentation list; every row is mapped to a Section 9 row or a Section 9.3 correction).

### Coverage of research-file key findings

Every key finding in the Summary and Key Takeaway sections of the assigned research files appears in Section 8, 9 or this table, or is excluded here with a reason.

| Source | Key finding | Where used, or exclusion rationale |
|---|---|---|
| R01 | Explicit-only command; first message must be the literal `/sc:issue --claim <N>` | 3.2, 8.2 |
| R01 | Only `origin_repo.py` validates the argument in code; bare integer is strictest; build the prompt from `int`; script is a second check | 3.2, integer-only rule in Phase 1 |
| R01 | Claim never runs the pipeline | 1.3, D2, C1 |
| R01 | Claim writes `.dev/issues/<N>/` into the checkout; workspace must be a checkout of origin | 3.3, Q17 |
| R01 | No machine-readable result; completion visible on GitHub only | Phase 5: GitHub marker plus local record |
| R01 | Waves 0 to 2 write nothing; claim does not gate on labels or Projects and leaves Backlog unchanged | Phase 4 filter table; Phase 5 intro |
| R01 | Tier picker IDs are a hard prerequisite | Q5, attempt cap |
| R01 | No trigger or approval label exists | 7.1, Q9 |
| R01 | Races across logins and for one login; dispatch record before launch; lost reply | Phase 5, Q4, Q14 |
| R01 | ClickUp is optional and never blocks the claim | Excluded: does not change any plan step; per-host fact under Q5 |
| R01 | Never-as-worker list; poller must be a plain process (WC-13) | 8.2, 1.6, Q21 |
| R01 | `orca agent launch` contract; prompt submitted; existing worktree required; exit 1; `--retry-launch`; slash command and delivery unverified | Phase 3 table, Q1 to Q3 |
| R01 | Integer-only protects the prompt, not the claim's own reads | 1.6, Q12 |
| R02 | No schedule or issue-event workflow; option A needs none | 8.1, closing table |
| R02 | Existing labels cannot express approval; new labels need `gh label create` instructions | 7.1 |
| R02 | `ci.py` is not a `gh` wrapper; nearest pattern `origin_repo.py`; mocking is PATH stubs | Phase 2, Phase 6, C4 |
| R02 | Click registration block, package model, tests layout, gates, mirror scope | 2.1 to 2.6, 6.5, 1.9 |
| R02 | Design-doc house format | Phase 1 |
| R02 | Reconciled assignee predicate | 4.3, C11 |
| R02 | Convention B `gh repo view` fallback unsafe for the fork | 1.5, 3.1 |
| R02 | Stale test comments (`mock_gh`, frozen snapshot), Orca-inherited issue forms | C5, C7; excluded from the plan: they do not affect any step |
| R03 | Only the Bash job-identity adapter exists; guard, `--pipeline`, marker binding, pre-push are design only; B-CTX gates only a later extension | C2, C3, follow-up table |
| R03 | Nothing registered constrains a launched session; permission posture undefined; `master` unprotected; readable token; repo is public | 1.6, Q6, C6 |
| R03 | The identity hook is not installed on this host | C3, Q33; excluded from the plan: dormant and irrelevant to a claim-only watcher |
| R03 | The claim reads title, body and comments live and posts unreviewed output | 1.6, Q11, Q12 |
| R03 | Approval authority is Triage or higher; label-event actor allows a poller-side check; assignee is the one routing input the claim enforces | Phase 4, 7.1, 7.2, Q10 |
| R03 | The Worker Contract does not govern a plain `orca agent launch` session; no category for a standing authorization by a label | 8.2, 1.6; the policy gap is stated for the design doc review (Q21) |
| R03 | Properties provided versus missing (at-most-once, audit, pre-launch integer validation, permission-mode decision) | Phase 3 to 5 (audit lines, validation, caps), Q6 |
| W01 | Scheduled Action limits | Closing table (revisit conditions), option D row |
| W01 | No `issues` type for a Project Status change; `projects_v2_item` is an org webhook | Closing table condition 7 |
| W01 | Read tokens for Projects v2; `GITHUB_TOKEN` cannot read an org Project | 7.3, Q7, Q27 |
| W01 | REST `q`, `gh project item-list --query`, issue search has no Status qualifier | Phase 4 discovery, Q8 |
| W01 | Rate limits, cost arithmetic, ETag/304, secondary limits | 1.5, Q23 |
| W01 | Who applied the label; `author_association`; Triage can label | Phase 4 filter 2, Q10, Q11 |
| W01 | Webhook facts for the push designs | Closing table; Q26 |
| W01 | Actions minutes cost | Excluded: option A runs no Action |
| W01 | Intended-owner candidates costed | Phase 4 filter 5, Q4 |
| W02 | `coder_script` cron; stop behavior; activity; durable state; systemd availability | 7.5, Q15 |
| W02 | Agents connect outbound; `coder ssh`, `port-forward`, `external-auth`; `coder exec` not found | Closing table; Q26 |
| W02 | External auth does not guarantee the owner's identity | Q16 |
| W02 | `claude -p` expands custom commands; `--bare` skips them | Closing table (headless row), Q20, C8 |
| W02 | `claude-code-action` and comparable dispatchers (Copilot, OpenHands, Codex) | Excluded: run on vendor or runner infrastructure and are not usable for the Orca flow; `create-task-action` appears in the push-design follow-up row |
| W02 | Prompt-injection guidance | 1.6, Q12 |
| W02 | At-most-once patterns (assign is not a lock, marker comment, idempotency key, lease, `concurrency`) | Phase 5 intro and `may_dispatch`; idempotency key and `concurrency` apply to the push designs only (closing table) |
| W02 | Sender authentication options, `coder_app` sharing, minimal watcher-to-listener contract, revisit conditions J3 | Closing table and Q26; not planned (Coder repo boundary) |
| GAPS | All 24 rows | Q1 to Q33 and C1 to C11 cover each row; row 6 is Q19; row 18 is Q22 |
