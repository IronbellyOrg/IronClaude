# QA Report - Research Gate (evidence-quality lens)

**Topic:** GitHub issue watcher research (issue #331, IronbellyOrg/IronClaude)
**Date:** 2026-11-07
**Phase:** research-gate
**Fix cycle:** N/A
**Status:** Complete
**Fix authorization:** false (report only)

---

## Scope

Files in scope (Glob of the task directory): `research/research-notes.md` (incl. ADDENDUM and ADDENDUM 2), `research/01-claim-flow-and-session-launch.md` (288 lines), `research/02-github-surface-and-cli-patterns.md` (211), `research/03-governance-and-security-surface.md` (231). `research/web-01-*` and `research/web-02-*` do not exist yet; they are Phase 4 outputs and are explicitly out of scope for this gate (task file lines 195-233). No analyst report exists at `qa/analyst-completeness-report.md` (it runs in parallel), so full verification was performed.

## Mandatory re-verifications (a) to (d)

| ID | Claim under test | Result | Evidence |
|---|---|---|---|
| (a) | `src/superclaude/pr_submit/ci.py` is a gh subprocess wrapper | CODE-CONTRADICTED, as research 02 section 3.1 says. Research does NOT name a wrapper location. PASS for this item | Read `ci.py:1-60`: imports are only `from __future__ import annotations`, `re`, `.classifier`, `.models` (l.10-15); docstring l.3-4 "Pure: consumes an already-fetched checks payload". Grep `subprocess\|"gh"` over `src/superclaude/pr_submit`: 0 matches. Grep `["']gh["']\|gh (pr\|issue\|api\|repo\|project\|auth\|run\|label)` over `*.py` under `src/superclaude`: the only hit is `skills/sc-issue-protocol/scripts/origin_repo.py:14` (docstring prose). Grep `shutil.which("gh")` over src and tests: 0. Functions at ci.py l.25, 58, 63, 79, 90, 99, 111 match research 02 3.1 |
| (b) | `.github/workflows/` has no `schedule:` trigger | CONFIRMED | Grep `schedule\|cron\|^on:\|push\|pull_request\|workflow_dispatch\|issues\|workflow_run\|pull_request_target\|workflow_call` over the 4 files: only `test.yml:3-8` (push, pull_request, workflow_dispatch), `contract3...yml:22-23` (pull_request), `boundary-guard.yml:25-26` (pull_request). Directory listing: README.md, boundary-guard.yml, contract3-generator-constraint-lint.yml, test.yml |
| (c) | `/sc:issue` is on the never-as-worker list in WORKER-CONTRACT.md | CONFIRMED | Grep + Read `src/superclaude/core/WORKER-CONTRACT.md:23`: "`/sc:agent`, `/sc:git`, `/sc:help`, `/sc:issue`, `/sc:pm`, `/sc:spawn` and `/sc:swarm-wizard`, plus `/sc:pr-submit` while ... D3". Also l.11 (worker run definition), l.16-20 (guard, case 3), l.39 (WC-8), l.40 (WC-9), l.61 (WC-13), l.93, l.112 all say what research 01 and 03 say |
| (d) | `launch-level-guard.sh` exists or not | DOES NOT EXIST, as research 01 and 03 say | Glob `**/launch-level-guard*` over `src`: no files. Glob `**/launch-*` over the worktree: only `launch-job-identity.sh` (src copy, plugins mirror, two .venv copies) plus unrelated task artifacts. Design doc `docs/designs/sc-issue-launch-level-hook.md:40` marks it "proposed"; l.23 states it in present tense (research 03 tags that CODE-CONTRADICTED correctly) |

## Working notes (appended incrementally)

### Research 01 (claim flow and session launch): citation re-check

I re-read every cited source at the cited lines. All of the following matched what the research says:

- `src/superclaude/commands/issue.md` (100 lines by `wc -l`; research says 101, a nit): l.8 argument-hint, l.15, l.18, l.24, l.37, l.43, STOP rules l.45-51 (incl. the note that none checks for an integer), l.68, l.71, l.79-85, Activation l.87-93, Related Commands l.95-100. Grep `pipeline` in issue.md: 0 hits (the "--pipeline is design only" claim holds).
- `refs/claim.md` (91 lines): Wave 0 l.13-18 and l.20; Wave 1 l.26-30; Wave 2 l.37-43; Wave 3 l.47-50; Wave 4 l.54-59; Wave 5 l.78-80; Wave 6 l.84-90. Every row of the wave table in 01 section 3 matches.
- `SKILL.md` (156 lines): l.4, l.52-66, l.70-76, l.82-88, return contract l.101-117, error table l.121-138 (rows at l.130, 131, 133, 134, 135), l.146, l.150. `AskUserQuestion` appears only at `SKILL.md:4` and `refs/create.md:59`; `gh project|projectV2|graphql` has zero hits under `sc-issue-protocol` (both CODE-VERIFIED tags hold).
- `scripts/origin_repo.py` (195 lines of code): `_NUMBER` l.74, `_GITHUB_URL` l.70-73, `check_claim` l.102-153, `read_origin` l.156-174 (no cwd argument, l.159-164), `main` l.177-191, exit-code table l.45-50. I walked `owner/repo#N`, `007`, `0`, `-5` through the code: all end in `E-NOT-AN-ISSUE` exit 4 as stated.
- `scripts/clickup_claim.py` (270 lines): every cited line (l.8-19, 42-48, 50, 74, 76, 109, 114, 119-122, 148-160, 163-170, 184, 203-206, 212-220, 230-231, 239-242, 245-259, 262-266) matches.
- `refs/labels.md` (46 lines): l.7, l.9-13, l.20, l.22-43 match; no trigger or approval label in the set.
- `refs/tiers.md` l.11-15 and l.32-40 match. Templates: `accuracy-check-comment.md:17`, `claim-comment.md:23`, `next-steps.md:5` match (Grep).
- `WORKER-CONTRACT.md`: l.11, l.16-20, l.23, l.39-40, l.61, l.93 match; `issue.md` has no `## Unattended mode` section (read whole file).
- `.dev/issues/331/analysis/analyze-sc-issue-protocol.md`: F3 l.34, F4 l.35, F5 l.36, F7 l.38, F9 l.40, statement 3 l.24 match.
- Orca CLI sources under `/opt/Orca/resources/app.asar.unpacked/out/`: `cli/specs/agent-launch.js` l.9 (usage), l.22-27 (notes); `cli/handlers/agent-launch.js` l.11-35 (existing worktree, `createsWorktree: false`, remote needs `--worktree`, selector resolution l.18-22); `cli/agent-launch-request.js` l.21-37, l.50-51, l.63-65 (`delivery: 'submit'`, empty prompt dropped), l.84-92, l.105-117; `cli/agent-launch-recovery.js` l.54-64 (`agent_session_operation_unknown`, `retrySafe`, `recoveryCommand`); `cli/index.js` l.128-137 (`reportCliError` then `process.exitCode = 1` at l.137); `shared/tui-agent-config.js` l.15-21 (`promptInjectionMode: 'argv'`, `draftPromptFlag: '--prefill'`); `cli/bundled-skill-guides.js` l.2413 and l.3158 contain "best-effort attention only" and "does not interrupt you". `orca agent launch --help` run locally prints the same usage line. `orca orchestration send --help` and `orca terminal send --help` match the table in section 12.
- `ccsession-tag/README.md` l.211-226, l.228-237, l.272, l.278; `ccsession-orca` (249 lines) l.56-125, l.110 (`-*) : ;;`), l.116, l.119; `~/.local/bin/ccsession-orca` is a symlink to `~/.claude/skills/ccsession-tag/ccsession-orca`; `/home/coder/.config/orca/profiles/local-default/orca-data.json` has `agentDefaultArgs.claude = "--dangerously-skip-permissions"` and `agentCmdOverrides = {}`; `src/superclaude/core/CLAUDE.md` "Orca session launches" is l.45-53.
- `src/superclaude/cli/pipeline/process.py` l.91 (`max_turns` 100), l.134-166 (`claude --print --verbose ... --no-session-persistence ... --tools default`, l.152), docstring l.137-138.
- `.dev/orca-command-refactor/inventory/orca-capabilities.md` l.47 and l.66 match.
- `gh issue edit --help`, `gh issue list --help` (`--assignee`, `--label`, `--search`, `--state`, `--json`, `--limit`), `gh project item-list --help` (`--query "assignee:octocat -status:Done"`, `--owner`) all run locally and match section 9.
- `tests/commands/test_issue_command.py`: Grep for `never runs|Will Not|B2|stop after` returns nothing (the UNVERIFIED gap 6 is stated accurately).
- `docs/designs/sc-issue-launch-level-hook.md` l.17, l.23, l.34, l.40, l.349-350 match.

Nits (MINOR, notes only): `issue.md` is 100 lines, not 101; `origin_repo.py` heading says 196 lines and the table says 195 (the file has 195 lines of text).

No fabricated path, function or line was found in file 01. Every UNVERIFIED tag is an honest statement of something that cannot be shown from files.

### Research 02 (GitHub surface and CLI patterns): citation re-check

Matched what the research says:

- Workflows: `test.yml` l.3-8, 17, 20-23, 29, 38, 47, 72, 98, 100-106, 116-123, 127-135, 151-158, 191-200 (`needs` at l.194); `boundary-guard.yml` l.25-33 (5 paths) and header l.19-20; `contract3...yml` l.22-29 and `timeout-minutes: 5` at l.35; `.github/workflows/README.md` l.7-39, l.120-125, l.137-143.
- Issue forms: `bug_report.yml` (`Bug`, label `bug`), `feature_request.yml` (`Feature`, label `enhancement`), `other.yml` (no labels), `config.yml:1 blank_issues_enabled: false`. Live `gh label list --repo IronbellyOrg/IronClaude` returns exactly the 9 default labels; `git remote get-url origin` is `https://github.com/IronbellyOrg/IronClaude`.
- `gh` locations: 136 `gh <subcommand>` matches in 23 non-`.py` files under `src/superclaude` (per-file counts 13, 11, 11, 18, 9, 8, 8 match); line cites in `poll-augment-review.sh` (l.22, 37, 53-55, 91), `poll-ci-checks.sh` (l.44, 52-53, 80-81), `retrigger-review.sh` (l.16, 50, 56), `reply-resolve-thread.sh` (l.15, 57, 73, 131, 141) all match. 21 files under `src/superclaude` import `subprocess` (Grep count = 21, same list). `detection.py:267-275`, `tests/pr_submit/conftest.py:3-8, 38-59, 58`, `test_rate_limit.py:6, 63`, `mock_gh` in exactly 3 test files with 6 hits all match.
- Test stubs: `test_conflict_e2e.py` l.61, 101-106, 118-129, 132-146, 166-169, 178-186; `test_conflict_scripts.py` l.155, 161-179, 1697; `test_codex_reviews.py` l.518-572; `test_static_grep.py` l.30, 106, 167, 225, 339-363, 555-574; `test_cosmos_poll.py` l.101-127, 185; `test_conflict_sync_protocol.py:40`; `tests/skills/test_issue_repo_resolution.py` l.64, 281 all match.
- CLI: `main.py` l.513-516, l.519-561 (11 registrations, same names and order, `cli_portify_group` without `name=`), l.565; `pyproject.toml` l.16, 34-43, 70-71, 78-79, 107-117, 173-186; `recommend/` (12 files, 1,784 lines), `cleanup_audit/` (12 files, 1,820), `swarm/` (11,799), `eval/` (11,367) by `wc`; `init_lite.py` 359 lines with defs at l.81, 129, 221, 285, 324; `recommend/commands.py` l.34-35, 51, 145, 196; `recommend/__init__.py:12` and `tasklist/__init__.py:9` lazy `__getattr__`; `cleanup_audit/commands.py:18`; `swarm/tmux.py` l.87, 91, 95, 126, 140, 180, 202, 221; `sprint/notify.py:21`, `reflect/runner.py:387`, `reflect/commands.py:494`, `install_codegraph.py:104,156`, `install_retired_mcp.py:407`, `reflect/fallback.py:39`, `audit/tool_orchestrator.py:105`, `audit/batch_retry.py:87`, `doctor.py:61-77`, `install_user_setup.py` 34 `orca` hits.
- `tests/cli/test_cli_registration.py` l.28-49 and l.95-106; Grep shows `swarm` and `reflect` are absent from the file while both are registered at `main.py:547-549, 559-561`: the CODE-CONTRADICTED claim about the comment at l.28-30 holds. `tests/recommend/test_cli_registration.py` has 3 tests; `tests/swarm/test_cli_registration.py:74` exists; `tests/recommend/` has 8 `test_*.py`.
- Makefile: `test` l.13, `lint` l.48, `format` l.53, `sync-dev` l.109, `verify-sync` l.166, `verify-deps` l.356, `lint-architecture` l.362 and its checks; `.gitignore:127-128`; `docs/designs/sc-issue-command.md` (477 lines) headings at l.11, 20, 42, 57, 81, 112, 137, 182, 221, 240, 274, 286, 318, 325, 346, 386, 404, 412, 446, 467; l.378-380 name `_OTHER_COMMANDS` and `_POST_REFRESH_ADDITIONS`, and both names exist in the two test files.

Errors found in file 02 (MINOR, they do not feed any conclusion or decision):

| # | Location | What is wrong | Evidence |
|---|---|---|---|
| m1 | 02 Stale Documentation Found, last bullet | Says `feature_request.yml:20,29` carries Orca-style placeholders. It does not | Grep `-i orca` over `.github/ISSUE_TEMPLATE/feature_request.yml`: no match. (`bug_report.yml` does carry them: `orca_version` at l.28, "Orca crashes when ..." at l.43; research cites l.29, off by one) |
| m2 | 02 section 4.2 | "tasklist/ (5 files, 771 lines" then lists 6 files | `ls src/superclaude/cli/tasklist/*.py` = 6 |

### Research 03 (governance and security surface): citation re-check

Matched what the research says:

- Design doc (565 lines by `wc`; research says 566): front matter l.6-10, banner l.17, l.23, l.32, l.34, l.40-41, l.339-347 (two `launch-level-guard.sh` hook entries at l.342, 344), l.349-355, l.359, l.491-506 (B-CTX).
- `launch-job-identity.sh` (566 lines): header l.1-18, fast exit l.20-24, `store` l.102, `governed` l.177, `request` l.189, `identify` l.215, `supervise` l.291, `os.execv` l.319, `run` l.362, `hook` l.414, non-Bash return l.426-428, invalid sid l.429-431, missing `sessions/<sid>` l.435-437, `updatedInput` output l.479-482 with no `permissionDecision`, exit 2 l.484-486, `execute` l.492. Plugins mirror is byte-identical (`cmp`). `tests/hooks/test_launch_job_identity.py` exists. `src/superclaude/hooks/scripts/` holds 14 files.
- `hooks.json` (163 lines): UserPromptSubmit l.44-63 (only `freshness-user-prompt.sh` and `session-name.sh`), PreToolUse l.75-106, launch-job-identity entry l.96-105. `install_hooks.py:42` (`_FRESHNESS_SCRIPTS`) and l.87. `.claude/settings.json` (28 lines, only `hooks`, no `permissions`) l.4-14, l.15-25.
- Workspace state (read-only commands): `/home/coder/.claude/settings.json` top-level keys are exactly as listed, `skipDangerousModePermissionPrompt` true, no `permissions` key, PreToolUse has only `Edit|Write`, `Bash` block-bare-python and one Orca `*` hook; `/home/coder/.claude/hooks/` has 14 scripts and no `launch-job-identity.sh`; `/home/coder/.claude/state/launch-level` does not exist; `hosts.yml` is mode 600 owner `coder`.
- Live GitHub state (read-only): `gh auth status` scopes `gist, read:org, repo, workflow`; repo visibility `PUBLIC`, `isFork: true`, `isPrivate: false`; `branches/master/protection` returns HTTP 404 "Branch not protected"; `rulesets` and `rules/branches/master` are `[]`; collaborators by role 1 admin, 2 maintain, 8 read; `gh project list --owner IronbellyOrg` fails "missing required scopes [read:project]"; issue #331 events list `labeled`, `issue_type_added`, `added_to_project_v2`, `project_v2_item_status_changed`, `issue_field_added`, `assigned` with actor logins; `author_association` is `MEMBER`.
- `block-bare-python.sh` l.4-14, 48-61, 67-74, 338-344; `reject-workspace-writes.sh` l.28-37, 51-62; `hooks/README.md` l.3-19 (stale-doc claim holds).
- GitHub repository roles (external; Tavily MCP tools are not in this agent's tool list, so `WebFetch` was used as the fallback, 1 call): docs.github.com repository-roles page rows: Open issues = Read; Apply/dismiss labels = Triage; Create, edit, delete labels = Write; Close, reopen, assign all issues = Triage; Have an issue assigned = Read. All match the table in 03 section 4.2.
- `ccsession` l.119-141 and l.127; `ccsession-orca` l.66-122; `agents/issue-worker-t3.md` l.5, l.28-29 (the l.21 and l.27 lines are long lines that contain the `gh issue view` and read-only text).

### BLOCKING finding B1: file 03 misstates what decides the permission mode of a launched session, and it contradicts file 01

- Where: `research/03-governance-and-security-surface.md` section 2.2 row "ccsession launch flags" (line 67), section 2.3 first bullet (line 70), Gaps item 5 (line 211, "This decides whether a launched session is bypass-mode (`ccsession:136-141`) or stalls on permission prompts"), and Key Takeaways (line 77, "stalled in default mode, unrestricted under ccsession's default flags").
- What the sources say: `src/superclaude/skills/ccsession-tag/README.md:534` (the `CCSESSION_PERMISSIONS` row, adjacent to the `:535` row 03 cites) ends "flags the caller passes (such as Orca's default `--dangerously-skip-permissions` option) still apply". `/home/coder/.config/orca/profiles/local-default/orca-data.json` has `agentDefaultArgs.claude = "--dangerously-skip-permissions"` (read by this QA run). Research file 01 section 11 (line 189) already records that value. So for a session started by `orca agent launch`, setting `CCSESSION_PERMISSIONS=default` does not by itself make the session permission-gated: Orca's own default argument is passed on top. The permission mode of a poller-launched session is decided by Orca's `agentDefaultArgs` as much as by the ccsession variable.
- Why it blocks: the synthesis (security options, recommendation, "permission-mode decision" open item) will draw on 03's table. As written it would present `CCSESSION_PERMISSIONS=default` as the control that decides bypass versus stall, which the cited README row contradicts. Checklist item 5 (contradictions between research files must be resolved, not left unreconciled) also applies: 01 and 03 each hold half of the fact and neither cross-references the other.
- Required fix: in 03 amend section 2.2 row 67, section 2.3, Gaps item 5 and the Key Takeaway to say that on the Orca route the effective flags are ccsession's defaults plus whatever Orca passes from `agentDefaultArgs` (observed locally: `--dangerously-skip-permissions`; the Coder workspace value is UNVERIFIED), that `CCSESSION_PERMISSIONS=default` alone does not remove it (README:534), and cross-reference 01 section 11. Optionally cite README:534 instead of :535 for the permission row.

## Items Reviewed (10-item research-gate checklist)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | File inventory | PASS | 3 codebase research files exist, each `Status: Complete`, each with a Summary, Key Takeaways and a Gaps and Questions section (Read in full). Web files are Phase 4 and out of scope |
| 2 | Evidence density | PASS (with minor errors m1, m2) | Over 300 cited file:line anchors re-read or re-grepped (sections above); no non-existent path or function; two minor inaccuracies only |
| 3 | Scope coverage | PASS | Every EXISTING_FILES row and every agent Files list maps to a research file: issue.md, SKILL.md, claim.md, labels.md, origin_repo.py, WORKER-CONTRACT.md, ccsession-tag README, core/CLAUDE.md, launch-level design, launch-job-identity.sh (01/03); workflows, ISSUE_TEMPLATE, ci.py, main.py, tests, sc-issue-command.md (02); Makefile (02 section 6); `.claude/settings.json` (03 section 2.1); `clickup_claim.py` (01 section 6) |
| 4 | Documentation cross-validation | PASS | Doc-sourced claims carry CODE-VERIFIED / CODE-CONTRADICTED / UNVERIFIED tags; every CODE-VERIFIED and CODE-CONTRADICTED tag I sampled (ci.py, launch-level-guard.sh, `--pipeline`, `conftest.py` docstring, `test_cli_registration.py` comment, hooks README, CLAUDE.md "private fork" vs PUBLIC) held against source |
| 5 | Contradiction resolution | FAIL | B1: file 03 and file 01 are unreconciled on what decides the launched session's permission mode, and 03's statement is contradicted by README:534 |
| 6 | Gap severity | PASS | Gaps are honest UNVERIFIED or OPEN-DECISION items (slash-command execution of the initial prompt, prompt argv vs paste, Coder workspace config, project token scope, approver allow-list). None is a hallucination risk for synthesis once B1 is fixed; they are carried to the plan as live checks. Minor gaps: `launch-*.sh` Glob statement ignores the plugins mirror copy (harmless) |
| 7 | Depth appropriateness (Standard) | PASS | File-level coverage plus a full end-to-end flow (claim waves, launch contract, validation, governance) |
| 8 | Integration point coverage | PASS | Claim entry (01 sections 1-5), session launch (01 section 12), CLI registration (02 section 4), workflow triggers (02 section 1), label and Project selection (02 section 2, 03 section 4), test mocking (02 sections 3.4, 5) |
| 9 | Pattern documentation | PASS | `gh --repo` convention A and B, `origin_repo.py` error-code pattern, Click lazy registration with the `noqa` marker, PATH-stub test pattern, design-doc family, `.claude/` mirror rules, Python 3.10 and ruff constraints |
| 10 | Incremental writing compliance | UNVERIFIABLE | The files have no write history in the tree; their structure (numbered sections, per-section Key Takeaways, corrected ci.py claim in research-notes) is consistent with iterative work, but I cannot prove it |

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| B1 | IMPORTANT (blocking) | `research/03-governance-and-security-surface.md` lines 67, 70, 77, 211 | States that `CCSESSION_PERMISSIONS=default` (with ccsession-orca) decides whether a launched session is bypass-mode or stalls; the cited README (row l.534) and the locally observed Orca `agentDefaultArgs.claude = --dangerously-skip-permissions` (already in 01 line 189) show Orca's own default flag still applies. Unreconciled with file 01 | See "BLOCKING finding B1" above: amend 03 and cross-reference 01 section 11 |
| m1 | MINOR | `research/02-github-surface-and-cli-patterns.md` line 207 | `feature_request.yml` has no Orca placeholder text; `bug_report.yml` Orca text is at l.28 and l.43, not l.29 | Delete the `feature_request.yml:20,29` reference; change l.29 to l.28 |
| m2 | MINOR | `research/02-github-surface-and-cli-patterns.md` section 4.2 | "tasklist/ (5 files" lists 6 files | Say 6 files |
| m3 | MINOR | 01 line 12 and 03 line 11 | `issue.md` is 100 lines (not 101); design doc is 565 by `wc -l` (not 566) | Wording only |

No finding was fabricated-path or fabricated-function class. No unresolved contradiction other than B1 was found. m1 is technically a false statement, but it is an aside about inherited template text that no conclusion or plan step depends on, so it is graded minor.

## Summary

- Checks passed: 8 / 10 (1, 2, 3, 4, 6, 7, 8, 9); failed: 1 (item 5); unverifiable: 1 (item 10)
- Critical issues: 0; blocking (IMPORTANT) issues: 1 (B1); minor notes: 3 (m1, m2, m3)
- Issues fixed in place: 0 (fix_authorization false; no file other than this report was modified)
- All four mandatory re-verifications (a) ci.py is not a gh wrapper and no Python gh wrapper exists, (b) no `schedule:` trigger, (c) `/sc:issue` on the never-as-worker list at `WORKER-CONTRACT.md:23`, (d) `launch-level-guard.sh` does not exist, were confirmed as the research states them.

**Confidence:** Verified: 9/10 | Unverifiable: 1 | Unchecked: 0 | Confidence: 100.0% (9 / (10 - 1))
**Tool engagement:** Read: ~52 | Grep: ~45 | Glob: 4 | Bash: 6 (read-only: wc, ls, cmp, jq, gh api, gh help, orca help; one call was rejected by the bare-python hook and re-run without python). `tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 1` (Tavily MCP tools are not in this agent's tool list; one WebFetch of the GitHub repository-roles page).
Tool calls exceed the number of checklist items, so the minimum-engagement rule is met.
UNCHECKED items: none. UNVERIFIABLE items: check 10 (no write history to inspect).

## Recommendations

1. Fix B1 in `research/03-governance-and-security-surface.md` (four places) and add a cross-reference to 01 section 11. This is one small edit pass.
2. In the same pass, fix m1 and m2 in file 02 (optional; minor findings are not rechecked).
3. Then run one re-review limited to B1 (fix cycle 1 of 2). Synthesis should not start until B1 is closed.

## QA Complete

VERDICT: FAIL

