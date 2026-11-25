# Scope 4: /sc:issue --claim flow
**Scope:** src/superclaude/commands/issue.md; skills/sc-issue-protocol/*; docs/designs/sc-issue-*.md; agents/issue-worker-t{1,2,3}.md
**Source root:** /home/coder/.cache/ic-snap-20261120/master (origin/master 61ac2c2e6). Paths below are relative to it.
**Status:** Complete
**Date:** 2026-11-20
---

Note on terms: the `--pipeline` values are `worktree | full | none` (plus `--submit` as a modifier of `full`), NOT "L1/L2". L1 and L2 are the two ENFORCEMENT layers of the launch-level guard (L1 = `launch-level-guard.sh` hook, L2 = pre-push hook), reported in launch output. [CODE-VERIFIED: commands/issue.md:9,43; orca_worktree.py:1822-1831,1885]

## 1. File inventory (all under src/superclaude/ unless noted)

| File | Lines | Role |
|---|---|---|
| commands/issue.md | 117 | Command front: flags, STOP rules (:50-59), outputs table (:76-81), Will/Will-Not, Activation = invoke `Skill sc:issue-protocol` (:104-110). v1.1.0 |
| skills/sc-issue-protocol/SKILL.md | 197 | Orchestrator protocol: files table (:24-50), worker spawn rule (:54-68), GH call rules (:70-78), claim Waves 0-8 (:80-92), create Waves 0-5 (:94-103), return contract (:105-150), errors (:152-177) |
| skills/.../refs/claim.md | 150 | Claim Waves 0-8 detail, effort rubric (:65-73), level-pick rule (:81), remedy tables (:106-115, :127-132), final output (:138-150) |
| skills/.../refs/tiers.md | 58 | Tier map T3/T2/T1 -> picker IDs (:11-15), T1->T2 fallback (:34-42), E-TIER-UNAVAILABLE (:44-52) |
| skills/.../refs/chains.md | 40 | Six default next-step chains (feature/bug x simple/medium/complex) (:9-16), goal passed to `/sc:recommend` (:27-38) |
| skills/.../refs/create.md (99), refs/labels.md (67) | | --create only; out of this scope except as pointers |
| skills/.../scripts/origin_repo.py | 195 | Wave 0: `origin` -> owner/repo; `--claim` arg check; exit 1/3/4 (:45-50) |
| skills/.../scripts/clickup_claim.py | 270 | Wave 3: ClickUp assignee only (stdlib urllib) |
| skills/.../scripts/orca_worktree.py | 1906 | Only file that calls `orca`; subcommands preflight/worktree/prompt/launch/pending (parser :1857-1894) |
| skills/.../templates/ (claim) | | scout-report(61), accuracy-check-comment(20), issue-summary(23), recommend-record(10), next-steps(14), claim-comment(23), launch-prompt(34); create-only: description, flags-decision, issue-{feature,bug}-{simple,complex}, draft-notes, create-review-comment |
| agents/issue-worker-t1.md / -t2.md / -t3.md | 35 each | Workers. Pins (frontmatter line 6): t1 `claude-gw-tier1b`, t2 `claude-gw-tier2`, t3 `claude-gw-tier2b` + `effort: low` (t3:7). tools: Read, Grep, Glob, Write, Bash |
| docs/designs/sc-issue-claim-pipeline-flag.md | 470 | Design of `--pipeline` / `--submit` |
| docs/designs/sc-issue-command.md | 509 | Original design (B*/D* decision IDs cited in skill) |
| docs/designs/sc-issue-launch-level-hook.md | 627 | NOT in assigned list but cited as normative by issue.md:16 and refs/claim.md:136 (L1/L2 guard, IR-4/IR-6/IR-7, OB-H gates); belongs to the launch-level-hook slice |

### orca_worktree.py function map (1906 lines; `def` line numbers)
- Header/docstring :1-66 (contract of every subcommand). Constants :88-91 (timeouts 120/30/15 s, env `SC_ORCA_TIMEOUT`).
- A. Subprocess + IO helpers: `Result` class :95, `_timeout` :120, `run` :132 (no shell, captured, timeout never raises), `_text` :169, `parse_json` :175, `atomic_write_text` :183 (mkstemp+os.replace, symlink-safe), `emit` :204 (one JSON object, exit 0).
- B. preflight: `cmd_preflight` :210 (`orca status --json`; ok + `result.runtime.reachable`).
- C. worktree create/reuse: `WARNING_ORDER` :230, `RECORD_NAME="worktree.json"` :240, `Outcome` :244; `real` :283, `git_common_dir` :287, `main_checkout` :294, `row_id` :299, `row_basename` :303, `short_branch` :307, `list_rows` :314 (refuses truncated / host-omitting / zero-row / no-main lists), `read_record` :353, `guarded_record_path` :361, `lookup` :373 (reuse keys in order marker, record, basename, branch), `tracked_under` :414, `first_symlink` :424, `copy_issue_dir` :439 (file-by-file, never through symlink, never overwrites tracked, older copy -> `.prev`), `write_record` :507, `finish` :527, `close_first_tab` :568, `cmd_worktree` :625.
- D. prompt render: `BLOCK_MARKER` :743, `render_prompt` :746, `cmd_prompt` :764 (keeps prompt if `launch` entry exists and out file exists).
- E. IR-4 enforcement preflight (L1): constants :791-874 (`PENDING_PARTS`, `SHIM_*`, `REMEDY` :802, `IR7_REFUSE=False` :822, `GOVERNED_TOOLS` :841), `remedy` :829, `process_interface_gaps` :877 (pidfd_open + prctl SUBREAPER), `home_dir` :910, `read_settings` :914, `matchers_for` :930, `fires_for` :944, `enforcement_preflight` :955.
- F. L2 pre-push hook (install + verify): `l2_status` :1048, `_l2_as_install` :1070, `clean_git_env` :1113, `publish_no_replace` :1123, `l2_data_expected` :1162, `_l2_read_capped` :1183, `_l2_packaged` :1195, `_l2_data_ok` :1214, `_l2_conflict` :1241, `_l2_entry_verdict` :1249, `_l2_selftest` :1278, `_l2_preconditions` :1335, `install_l2` :1386.
- G. Launch record + launch: `session_report` :1445 (release line + L1/L2 layer lines), `publish_pending` :1488 (writes `$HOME/.claude/state/launch-level/pending/<nonce>`, 0600), `cmd_pending` :1515 (coordinator-started workers), `find_handle` :1526, `shim_interval` :1544, `ccsession_title` :1551, `behind_ccsession` :1564, `launch_mirror` :1586, `read_mirror` :1600, `record_launch` :1619, `launch_result` :1646, `stale_prompt` :1666, `cmd_launch` :1696.
- H. CLI: `issue_number` :1837, `repo_name` :1843, `origin_ref` :1851, `build_parser` :1857, `main` :1897 (`--submit` needs `--level full`, exit 2).

## 2. Behaviour map

### 2.1 Pipeline levels (the `--pipeline` flag)
| Level | Creates worktree | Launches agent | Agent boundary | Source |
|---|---|---|---|---|
| `worktree` | yes (`issue-<N>`) | yes, `--level worktree` | runs `next-steps.md` up to `Plan boundary: after step K`, prints plan path + "Waiting for approval"; human approves ONLY by running `/sc:implement`/`/sc:task`/`/task` as first line of a prompt in that session; then rest, still no commit/push/pr-submit | templates/launch-prompt.md:20-23 |
| `full` | yes | yes, `--level full` | all steps, no commit, no push, no PR, nothing staged; prints `git status --short` | launch-prompt.md:25-26 |
| `full` + `--submit` | yes | yes, pending word `full-submit` (orca_worktree.py:1759) | adds `submit` block: check no PR open/merged, conventional commit (stage `.dev/tasks` + changed files, never `.claude/`, never `.dev/issues/`), `git push origin <branch>`, `/sc:pr-submit --monitor 3`; never merge | launch-prompt.md:28-34 |
| `none` | no | no | claim stops after comments; person (or coordinator) runs `next-steps.md` | SKILL.md:90, refs/claim.md:94 |
| (omitted) | picks `full` or `worktree` | | bug -> full; simple/medium feature <=16 h -> full; complex feature or >16 h or unreadable type/complexity/hours -> worktree. Rule is PROSE ONLY in refs/claim.md:81 (the orchestrating LLM applies it; no Python implements it) [CODE-VERIFIED: grep of `src/` finds no .py hit] | refs/claim.md:81 |
`--submit` requires explicit `--pipeline full` (STOP `E-SUBMIT-NEEDS-FULL`, issue.md:59); the script also rejects `--submit` with level != full (orca_worktree.py:1900-1901). The issue watcher always passes `--pipeline none` (issue.md:48; see coordinator handoff issue.md:85).

### 2.2 Claim waves in order (orchestrator = the Claude session running the skill; "W" = worker)
0. Prerequisites (refs/claim.md:11-21): `origin_repo.py --claim <arg>` -> `{repo, number}` (exit 1 E-NO-ORIGIN, 3 E-FOREIGN-REPO, 4 E-NOT-AN-ISSUE); `gh auth status` (E-GH-AUTH); `orca_worktree.py preflight` = `orca status --json` (orca_worktree.py:210-223; `ok:false` -> STOP E-ORCA-REQUIRED, runs even for `none`); default branch via `gh repo view <R> --json defaultBranchRef`; mkdir `.dev/issues/<N>/`. No GH/ClickUp write before Wave 3.
1. Lookup (W = issue-worker-t3, read-only): `gh issue view`, `gh api user`, `gh pr list --state merged --search "merged:>=<date>" --limit 200`, `git fetch origin`, `git log --since --name-only origin/<B>`, finds earlier comments with markers `<!-- sc:issue:claim -->` / `<!-- sc:issue:accuracy-check -->` -> writes `scout.md` (agents/issue-worker-t3.md:22).
2. Edge cases (orchestrator): PR -> E-NOT-AN-ISSUE; CLOSED -> stop; assigned to other login -> stop; already mine -> continue (idempotent re-claim) (refs/claim.md:38-44). No writes on any of these stops.
3. Assign (orchestrator): `gh issue edit <N> --repo <R> --add-assignee @me` (fail -> E-ASSIGN-FAILED); then `clickup_claim.py` -> `clickup.json`.
4. Accuracy + summary (W = t2, or t1 if scout says `complex`; t1 falls back once to t2): writes `accuracy-check.md` (verdict `current|out_of_date`), `issue-summary.md` (effort in hours), and `analysis/analyze-<scope>.md` when out of date (refs/claim.md:53-73). Rubric: simple <=4 h, medium 4-16 h, complex >16 h / >1 subsystem / security or data migration.
5. Next steps (orchestrator): `Skill sc-recommend` with default chain row (refs/chains.md) -> `recommend.md`; writes `next-steps.md` (first line `/model claude-gw-tier2` for simple, `claude-gw-tier1b` for medium/complex; `Plan boundary: after step K`, K = last step before first `/sc:implement` or `/task`); resolves level `<L>`; runs `orca_worktree.py prompt ... --out .dev/issues/<N>/launch-prompt.md` (not for `none`).
6. Post (orchestrator): accuracy-check comment then claim comment; edits earlier marked comment via `gh api -X PATCH repos/<R>/issues/comments/<id> -F body=@file`, else `gh issue comment --body-file`. Fail -> E-POST-FAILED. `none` ends here.
7. Worktree (script, no worker): `orca_worktree.py worktree --repo <R> --number <N> --base origin/<B> --source <D>`.
8. Launch (script, no worker): `orca_worktree.py launch --number <N> --source <D> --level <L> [--submit]`.
Then final output + return contract (SKILL.md:105-150; claim adds 10 fields pipeline_level..enforcement_hook, :123-134).

### 2.3 What is written to GitHub and ClickUp (all by the orchestrator; workers never write)
- GitHub: (1) assignee `@me` on the issue (SKILL.md:74; refs/claim.md:48). (2) ONE accuracy-check comment (body = `accuracy-check.md`, ends `<!-- sc:issue:accuracy-check -->`). (3) ONE claim comment (templates/claim-comment.md: "Claimed by @login", ClickUp result, accuracy verdict, summary, effort, complexity, type, first next step, repo-relative links, ends `<!-- sc:issue:claim -->`). Re-claim edits both in place. NO labels, NO issue fields, NO issue type, NO status change, NO PR on claim itself (issue.md:96-99). `--submit` PR is opened later by the launched agent via `/sc:pr-submit --monitor 3`.
- ClickUp (clickup_claim.py): only `PUT /task/{id}` body `{"assignees":{"add":[user_id]}}` (:232-237). Reads: `GET /user`, paged `GET /team/{ws}/task?page&subtasks=true&include_markdown_description=true[&list_ids[]]` (:176-191). Matching: rule 1 description/custom-field contains the issue URL; rule 2 task name has `#<N>` (:148-160). Outputs `skipped(no_token|no_workspace) | not_found | ambiguous | already_assigned | assigned | error(auth|rate_limited|page_cap|...)`. Env: `CLICKUP_API_TOKEN`, `CLICKUP_WORKSPACE_ID` (both required), `CLICKUP_LIST_IDS`, `CLICKUP_MAX_PAGES` (default 20). No ClickUp comment, status, or custom field is written.

### 2.4 Launch record (two different "records")
- `.dev/issues/<N>/worktree.json` in the ORIGIN checkout: `{path, status, launch?:{level,submit,at}}` written by `write_record` (:507) and `record_launch` (:1619); never copied into the worktree (:466).
- Mirror `<wt git dir>/sc-issue-launch-<N>.json` `{path, launch}` (`launch_mirror` :1586; written :1638) so a re-claim from inside the worktree also sees `already_launched`.
- Enforcement-hook launch record `$HOME/.claude/state/launch-level/pending/<nonce>`: one word (`worktree|full|full-submit`), mode 0600, dirs 0700 (`publish_pending` :1488-1512, `PENDING_PARTS` :791). Written in `cmd_launch` AFTER IR-4 preflight and L2 install (:1759-1761) and BEFORE `orca agent launch`; removed if the launch call fails (:1783). `pending` subcommand (:1515) lets a coordinator write one for a worker it starts itself. Never pruned if unconsumed (design 18.1 A7).

### 2.5 How orca_worktree.py creates a worktree (`cmd_worktree` :625-738)
1. `git rev-parse --path-format=absolute --git-common-dir` -> main checkout. 2. `orca worktree list --repo path:<main> --limit 500 --json` (:316-327); unusable list -> reuse guarded `worktree.json` path (key `record`, W-ORCA-LIST-FAILED) or fail. 3. `lookup` keys marker (`comment` contains `sc:issue <R>#<N>`), record, basename `^issue-<N>(-|$)`, branch; 1 live hit = reused, stale = W-WORKTREE-STALE, >1 = W-WORKTREE-AMBIGUOUS (:649-668). 4. No hit: `git fetch origin`, `git rev-parse --verify origin/<B>` (W-ORIGIN-BASE-MISSING stops; failed fetch = W-ORIGIN-BASE-STALE note), then
`orca worktree create --repo path:<main> --name issue-<N> --base-branch origin/<B> --no-parent --comment "sc:issue <R>#<N>" --json` (:684-700; NO `--agent`, NO `--issue`/`--pr` link flag). 5. relist, new-row-id diff, exactly one new `^issue-<N>` row (:704-735). 6. `finish` (:527): common-dir check, `git ls-files .dev/issues/<N>`, `copy_issue_dir` (excludes worktree.json; tracked files skipped; differing untracked -> `.prev`), `write_record`. 7. `close_first_tab` (:568) only for newly created: `orca terminal list --worktree path:<wt> --json` then `orca terminal close --terminal <h> --tab --json` when exactly one terminal without `agentIdentity`.
### 2.6 How it launches the agent (`cmd_launch` :1696-1834)
Order: read record (guarded) -> `already_launched` if `launch` entry in record or mirror (:1706-1721) -> `stale_prompt` byte-compare of worktree vs source `launch-prompt.md` (:1722) -> `enforcement_preflight` IR-4 (:1730; failure = `W-ENFORCEMENT-ABSENT`, no record, no agent) -> `install_l2` + `l2_status` (:1754-1756; not `owned` = `W-L2-ABSENT`, refusal gated by `IR7_REFUSE=False` :822/:1757) -> `publish_pending` -> 
`orca agent launch --agent claude --worktree path:<wt> --surface terminal --prompt "[sc-launch:v1:<nonce>] Read .dev/issues/<N>/launch-prompt.md and follow it." --json` (:1777-1779; no `--model`/`--effort`) -> `find_handle` -> `behind_ccsession` (up to 5 reads, 2 s apart: `orca terminal read --terminal <h> --screen --json` for `[ccsession]` / `Session name (Enter or Ctrl+C`, else `orca terminal show --terminal <h> --json` title matches `sc-launch-v1-<hex>-<MMDD>-<HHMMSS>-<hex4>`; :1551-1583) -> `W-LAUNCH-NOT-CCSESSION` note if not -> `record_launch` -> `session_report` (release rm line + `L1 guard: effective` + `L2 pre-push: owned|<state>` lines).
IR-4 checks (`enforcement_preflight` :955-1045): `jq`, `uv`, cat/sed/tr/mkdir/mv/ln/rm on PATH; Linux `pidfd_open` + `prctl(PR_GET_CHILD_SUBREAPER)`; `~/.claude/hooks/launch-level-guard.sh` exists, executable, has `# launch-level-guard-version: 1`; `CLAUDE_CONFIG_DIR` unset or == `$HOME/.claude`; no `disableAllHooks`; guard registered on `UserPromptSubmit` and on `PreToolUse` for 23 governed tool names (`GOVERNED_TOOLS` :841); `launch-job-identity.sh` registered on Bash PreToolUse.
L2 hook: installed to `<git-common-dir>/hooks/pre-push` (SHARED hooks dir of the clone, not per-worktree; :1365,1402) with data file `pre-push.launch-level`; never replaces an existing entry; refuses when `core.hooksPath` is set (:1348-1350).

### 2.7 Approval and gate points
- Orca-down gate before any write (E-ORCA-REQUIRED). Re-claim idempotency by markers. T1->T2 fallback is the only non-STOP tier fallback.
- NO confirmation prompt for posting (B1, SKILL.md:76); the only user prompt in the whole command is `--create`'s contradiction question.
- Plan approval (level `worktree`): in the launched agent's terminal only; a human types the printed `/sc:implement <plan>` (launch-prompt.md:23). Enforced by the L1 guard hook (issue 394), not by the prompt alone (design 15: "the instruction alone is not enforcement").
- Ship gate: no governed claim (`worktree`/`full`) on a real issue until OB-H1 item 1, OB-H2, OB-H3 pass (issue.md:16; refs/claim.md:136). Prose gate; no code enforces it [CODE-VERIFIED: no such check in orca_worktree.py].
- `--submit`: agent-side commit/push/PR; nothing ever merges at any level.

### 2.8 Orchestrator vs workers
- Orchestrator (main session, runs the skill): all Bash/`gh`/ClickUp writes, edge-case decisions, `/sc:recommend` call, level pick, `next-steps.md`, `claim-comment.md`, all `orca_worktree.py` calls (SKILL.md:74,191).
- Workers (subagents, `subagent_type: issue-worker-t<N>`, never a `model` param): read-only `gh`/git (`git fetch origin` only), write only under `.dev/issues/`, return file paths (agents/issue-worker-t3.md:28-35). Claim: t3 = scout.md; t2/t1 = accuracy-check.md + issue-summary.md + analysis. Create-mode drafting jobs are for the --create slice.
- Launched agent (separate Claude CLI session in the worktree, behind ccsession): runs `next-steps.md` steps through the Skill tool (never by hand, never inside a subagent; launch-prompt.md:14).

## 3. Doc-vs-code checks
| # | Claim (source) | Verdict | Evidence |
|---|---|---|---|
| 1 | `orca worktree create` carries no `--agent`, no link flag, uses `--no-parent`, `--comment "sc:issue <R>#<N>"` (pipeline-flag design 8.3; issue.md:85) | [CODE-VERIFIED] | orca_worktree.py:684-700 |
| 2 | Agent launch is `orca agent launch --agent claude --worktree path:<wt> --surface terminal --prompt "[sc-launch:v1:<nonce>] Read ... and follow it." --json`, no model/effort (design 8.4 step 5) | [CODE-VERIFIED] | orca_worktree.py:1776-1780 |
| 3 | First plain tab closed only for a newly created worktree, only when exactly one terminal without `agentIdentity` (design 8.3 step 8) | [CODE-VERIFIED] | orca_worktree.py:568-622, :736-737 |
| 4 | Pending record is 0600, written before launch, removed on launch failure, level word `full-submit` for `--submit` (design acceptance 4) | [CODE-VERIFIED] | :1505, :1759-1761, :1783 |
| 5 | `W-ENFORCEMENT-ABSENT` refuses launch, writes no record; `W-L2-ABSENT` warns only (`IR7_REFUSE = False`) (issue.md:16; design Update) | [CODE-VERIFIED] | :822, :1730-1758 |
| 6 | Re-claim: launch entry in `worktree.json` OR worktree git-dir mirror gives `already_launched` (design A9) | [CODE-VERIFIED] | :1704-1721, :1586-1616 |
| 7 | Worktree reuse lookup order marker, record, basename, branch (issue.md:85; design 8.3 step 3) | [CODE-VERIFIED] | :399-404 |
| 8 | Stale-prompt refusal compares worktree and source `launch-prompt.md` byte for byte (design A16) | [CODE-VERIFIED] | :1666-1693, :1722-1724 |
| 9 | ClickUp rules/outputs/env (sc-issue-command.md section 12) | [CODE-VERIFIED] (minor: code's `ambiguous` also returns `rule`, :213-219) | clickup_claim.py:148-160, :163-242 |
| 10 | `--pipeline` omitted -> level picked from the issue (issue.md:43; refs/claim.md:81) | [CODE-VERIFIED] as prose-only: no Python/shell implements it; the orchestrating LLM applies the rule | no `.py` match in `src/` for the reason strings |
| 11 | `pipeline.json` is not built (design section 3, IR-3 "documentation only") | [CODE-VERIFIED] | no code in `src/` mentions it (only md) |
| 12 | `sc-issue-claim-pipeline-flag.md` section 1 table calls `worktree` "(default)"; P2 says default `worktree` | [CODE-CONTRADICTED] by its own inline amendments (2026-11-18) and by issue.md:43/48: default is picked, `full` for person-typed bug/small feature, watcher passes `none` | doc lines 21, 43, 66 carry stacked amendments; table row text is stale at its head |
| 13 | `sc-issue-command.md` Status "Design only (nothing implemented)" (line 3) | [CODE-CONTRADICTED] | all files in section 1 exist and are tested |
| 14 | `sc-issue-command.md` section 6 pins T3 to `claude-gw-tier3` (line 129) | [CODE-CONTRADICTED] | agents/issue-worker-t3.md:6 pins `claude-gw-tier2b`; refs/tiers.md:17 records the issue-488 change |
| 15 | `sc-issue-command.md` Wave 0 (lines 154-158) has no Orca check; pr-list lacks `--limit 200` | [CODE-CONTRADICTED] (amended elsewhere: header note at :150) | refs/claim.md:17, :28 |
| 16 | SKILL.md:92 / issue.md:16 say the L2 hook is installed "in the clone's shared hooks directory", while refs/claim.md:125 says "as the worktree's `pre-push` hook" | [CODE-VERIFIED] shared is right: hook goes to `<git-common-dir>/hooks/pre-push`, so it covers every worktree of the clone; the refs/claim.md wording is loose | orca_worktree.py:1365,1402 |
| 17 | `orca ... --surface terminal`, `agent launch`, `terminal close --tab`, `worktree create --no-parent` flags exist in the installed Orca CLI | [UNVERIFIED] here (Orca is external; design 15 says verified 2026-11-07 against live CLI) | tests use a fake `orca` only (test_issue_orca_worktree.py:1-6) |
| 18 | Tier pins resolve to the named models (GPT-6.1 Terra etc., refs/tiers.md:17) | [UNVERIFIED] (lives in ccsession-models.json, out of slice) | |
| 19 | OB-H1/OB-H2/OB-H3 ship gate "passed" status | [UNVERIFIED] (observation records live elsewhere; see launch-level-hook design sections 7, 11, 14) | |

## 4. Tests that pin this slice (counts = `def test_`/class-method matches)
- tests/commands/test_issue_command.py (15): static pins of commands/issue.md: frontmatter, version 1.1.0, exactly-seven-flags options table, defaults, STOP rules before Activation, `E-SUBMIT-NEEDS-FULL`, default-level wording, no `src/superclaude` path, rule-10 line verbatim.
- tests/skills/test_issue_protocol.py (62): static pins of the skill package: SKILL.md frontmatter/size, two-way inventory of refs/templates/scripts, spawn rule, posted-template markers, issue-template headings, chain flags vs source command files, fork-safety (`gh_lines_missing_repo`).
- tests/skills/test_issue_orca_worktree.py (109): behaviour of orca_worktree.py against a fake `orca` on PATH and temp HOME; test-name groups PF (preflight), FO (worktree create/reuse), PR (prompt), LA (launch, `test_la5_launch*` has 8), `test_pr425_*` regression pins from PR 425 review rounds 1-3 (~25), plus a few IR-4 enforcement-preflight cases (6 names match). Design A4 says a flag-whitelist test (ST-4) parses the script with `ast`; not checked in the test file.
- tests/skills/test_issue_l2_install.py (26): `install_l2` / `l2_status` on real git under temp HOME with copies of the packaged hook (FR-102).
- tests/skills/test_issue_repo_resolution.py (18): `origin_repo.py` forms of origin URL, claim-arg parse, exit codes 1/3/4, stdlib-only import.
- tests/skills/test_issue_worker_agents.py (24): static pins of the three worker agents (per docstring): tier pinning, repo/GitHub call rules, no Edit tool (D27), writable under `.dev/issues/` (C1); `gh_lines_missing_repo` fork-safety scan lives here and test_issue_protocol.py imports it.
- tests/skills/test_issue_t1_fallback.py (8): T1 -> T2 fallback text present in SKILL/tiers/claim/templates; no T2/T3 fallback; no alias fallback; no tier1a left.
- tests/cli/test_issue_body_templates.py (5): NOT a claim test; pins ISSUE-HANDOFF/ISSUE-BACKLOG core files and the rule-10 line in the distributed CLAUDE.md (installer check).
- Related but outside the assigned list: tests/skills/test_clickup_claim.py (ClickUp script), tests/skills/test_worker_contract.py (classifies `gh`/`git` lines in primitives), tests/hooks/test_launch_level_pre_push.py (L2 hook itself), tests/skills/test_model_alias_policy.py (pin policy, cited at refs/tiers.md:54).

## 5. Proposed deep-research assignments (2 max)
1. **Claim flow end to end (orchestrator contract, GitHub/ClickUp writes, levels, worker tiers).**
   Files: commands/issue.md, skills/sc-issue-protocol/{SKILL.md,refs/claim.md,refs/tiers.md,refs/chains.md}, templates/{scout-report,accuracy-check-comment,issue-summary,claim-comment,next-steps,launch-prompt}.md, scripts/{origin_repo,clickup_claim}.py, agents/issue-worker-t{1,2,3}.md, docs/designs/sc-issue-command.md and sc-issue-claim-pipeline-flag.md (read for history only; mark stale parts).
   Output: `research/r4a-claim-flow.md` (wave table with owner of each step, every GitHub/ClickUp write with exact command, STOP/warning code table, level-pick rule, return contract, doc staleness list from section 3 here).
2. **orca_worktree.py: worktree create/reuse, launch, enforcement preflight, L2 install.**
   Files: scripts/orca_worktree.py (all 1906 lines; focus :625-738 worktree, :955-1045 IR-4, :1048-1442 L2, :1488-1834 launch), docs/designs/sc-issue-launch-level-hook.md sections 3, 7, 11, 14, 19 (for IR-n/OB-H meanings), hooks `launch-level-guard.sh`, `launch-level-pre-push.sh`, `launch-job-identity.sh`, `require-orca-worktree-agent.sh` (only to describe what the script presupposes), tests/skills/test_issue_orca_worktree.py and test_issue_l2_install.py (as behaviour evidence).
   Output: `research/r4b-orca-worktree-launch.md` (exact orca/git argv per step, JSON result schemas of each subcommand, warning-code table with trigger lines, state files and their lifecycles, failure/race notes, `pending` subcommand use by coordinators).

## 6. Gaps
- `orca_worktree.py pending` (writes a launch record for a coordinator-started worker, :1515) is documented only in the script docstring (:7-9); no SKILL.md, refs or command text names it. Its callers (coordinator, `hooks/scripts/require-orca-worktree-agent.sh` references the script) are outside this slice: needs the observer/coordinator slice.
- The default-level rule (refs/claim.md:81) is prose executed by an LLM; no code or test computes it, so its behaviour is untested beyond text pins (test_issue_command.py:182).
- The L1 guard and L2 hook scripts (`hooks/launch-level-guard.sh` etc.) and `launch-level-hook.md` (627 lines) were not read; IR-n / OB-H meanings are taken from citations only.
- Issue watcher side (who passes `--pipeline none`, coordinator `worker-start`, adoption rows) is not in this slice; only its contract paragraph (issue.md:85) was read.
- `/sc:recommend` behaviour inside Wave 5 and `/sc:analyze` inside worker jobs not inspected.
- Not read in depth: `refs/create.md`, `refs/labels.md`, create templates, create-mode design sections 8, 10, 11 (--create is outside this slice). `orca_worktree.py` lines 877-950 (`process_interface_gaps`, settings readers) and 1081-1330 (L2 internals) were mapped by signature only.
- No live evidence: no Orca runs were made; Orca CLI flag validity is taken from design section 15 and the fake-orca tests.
- Test counts are `grep` counts of `def test_` lines, not collected-test counts (parametrization expands them).
