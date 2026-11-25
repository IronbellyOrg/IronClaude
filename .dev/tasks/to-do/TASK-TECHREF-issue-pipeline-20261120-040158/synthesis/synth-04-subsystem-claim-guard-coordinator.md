# Synthesis 04: Claim Flow, Guard Stack, Coordinator Text
**Sections:** 5.2, 5.3, 5.4
**Status:** Complete
**Date:** 2026-11-20

Sources: research files 04, 05, 06 (part A in full; part B Summary and Defect Candidates only), their Gap-fill sections (c1 B-2, c1 F-2, c1 B-3, c2 N-1, all marked ERRATUM or ADDENDUM and applied below), and `gaps-and-questions.md`. All line numbers are for snapshot 61ac2c2e6 and were taken from the research files.

**Path key (used by every citation in 5.2 to 5.4; every short form expands to a repository-relative path):**
`SK/` = `src/superclaude/skills/sc-issue-protocol/`; `OW` = `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py`; `GD` = `src/superclaude/hooks/scripts/launch-level-guard.sh`; `ID` = `src/superclaude/hooks/scripts/launch-job-identity.sh`; `PP` = `src/superclaude/hooks/scripts/launch-level-pre-push.sh`; `HJ` = `src/superclaude/hooks/hooks.json`; `WC` = `src/superclaude/core/WORKER-CONTRACT.md`; `T/` = `tests/`; `CMD` = `src/superclaude/commands/issue.md`; `AG` = `src/superclaude/agents/`. A bare file name followed by `:line` (for example `claim.md:81`) means the file under `SK/refs/` or `CMD` as named in the same row.

**Status words used here:** BUILT-ON, BUILT-OFF (enabled:false), NOT BUILT, REMOVED. Verification tags: [CODE-VERIFIED], [CODE-CONTRADICTED], [UNVERIFIED], [STALE DOC]. Remediation is not created here; capabilities that are unwired, switched off, retired or caller-less carry a "see Section 14" pointer.

---

### 5.2 `/sc:issue --claim` flow and `orca_worktree.py`

**Purpose:** `/sc:issue --claim <N>` takes a GitHub issue on the repository that `origin` points at, assigns it, checks its accuracy, writes a summary and a next-step prompt, and (unless `--pipeline none`) creates an Orca worktree and launches a Claude agent in it at a chosen level. It is a prose protocol run by the orchestrating model, backed by three helper scripts; the only code that calls `orca` is `orca_worktree.py` (SKILL.md:35).

**Status lines**

| Piece | Status | Evidence |
|---|---|---|
| `/sc:issue` command (version 1.1.0) and skill protocol | BUILT-ON | `issue.md:2-3`, Activation `issue.md:104-110`; run by the model, no switch |
| `origin_repo.py`, `clickup_claim.py` | BUILT-ON (ClickUp conditional: `skipped` without `CLICKUP_API_TOKEN` or `CLICKUP_WORKSPACE_ID`) | `clickup_claim.py:164-169` |
| `orca_worktree.py` preflight, worktree, prompt, launch, IR-4 preflight, L2 install, shim detection | BUILT-ON | no gating flag; `build_parser` `OW:1857-1894` |
| IR-7 refusal of a launch when the L2 hook is not owned | BUILT-OFF (a constant, not an `enabled` key) | `IR7_REFUSE = False` `OW:822`; refusal branch `OW:1757-1758` and text `OW:829-831` unreachable; pinned off by `T/skills/test_issue_l2_install.py:639` (see Section 14) |
| IR-3 `pipeline.json` level file | NOT BUILT | grep `pipeline\.json` over `src` and plugins: no match; stated as not built at `docs/designs/sc-issue-claim-pipeline-flag.md:58` (see Section 14) |
| Any caller of `orca_worktree.py pending` | NOT BUILT (binding and caller); the `pending` verb itself is BUILT-ON (`OW:1515-1523`, `OW:1886-1893`) | grep of `src` and plugins: no caller; only tests run it, `T/hooks/test_launch_level_guard_worker.py:287` and `T/skills/test_issue_orca_worktree.py:2472-2498` (see Section 14) |
| Default `--pipeline` pick from type, complexity, hours | NOT BUILT as code (prose rule only) | `claim.md:81`; no `.py`, `.sh`, `.json` holds the reason strings (see Section 14) |
| Ship gate "no governed claim until OB-H1 item 1, OB-H2, OB-H3 pass" | NOT BUILT as a mechanism (prose) | `issue.md:16`, `claim.md:136`; no code reads it (see Section 14) |
| Coordinator hand-off after a `--pipeline none` claim | NOT BUILT (prose at `issue.md:85`, `SKILL.md:140`, `claim.md:96`) | no caller of the `worktree` subcommand besides the claim prose (see Section 14) |
| Automatic close of an agent that is not behind the shim | NOT BUILT (warning only) | `OW:1803-1811` (see Section 14) |

**Key Files**

| File | Purpose |
|---|---|
| `CMD` (117 lines) | Command front: seven flags (`issue.md:36-44`), STOP rules before Activation (`issue.md:50-59`), outputs table (`issue.md:74-81`), Will / Will Not (`issue.md:89-102`) |
| `SK/SKILL.md` (197 lines) | Orchestrator protocol: files table `SKILL.md:24-50`, worker spawn rule `:54-64`, GitHub call rules `:70-78`, claim waves `:80-92`, return contract `:105-150`, error table `:152-177` |
| `SK/refs/claim.md`, `refs/tiers.md`, `refs/chains.md` (40 lines) | Wave text; tier pins and T1-to-T2 fallback (`tiers.md:34-42`); default next-step rows (`chains.md:9-16`) |
| `SK/scripts/origin_repo.py` (195 lines) | Resolves `<R>` and `<N>` from `origin` only (`:156-174`, `:102-153`) |
| `SK/scripts/clickup_claim.py` (270 lines) | Read-then-assign ClickUp lookup; the single write is `:232-237` |
| `SK/scripts/orca_worktree.py` (1906 lines) | Preflight, worktree create/reuse, prompt render, IR-4 preflight, L2 install, launch, `pending` |
| `SK/templates/` (15 files, not 17) | Posted comments (`claim-comment.md` 23 lines, `accuracy-check-comment.md` 20), `issue-summary.md`, `next-steps.md`, `launch-prompt.md` (34 lines, four blocks `:11,:20,:25,:28`) |
| `AG/issue-worker-t1.md`, `-t2.md`, `-t3.md` (35 lines each; erratum applied) | Tier workers; `tools` line 5, `model:` line 6 |

**How It Works**

The "orchestrator" is the Claude session that invoked the skill, not a program: no Python runs the waves in order (SKILL.md:80-92). Workers run in waves 1 and 4 only; every write to GitHub, ClickUp or Orca is the orchestrator's. Worker rules: read-only GitHub, write only under `.dev/issues/`, return only file paths (`t*.md:28-35`); an empty or missing worker file is retried once, then STOP `E-WORKER-NO-OUTPUT` (SKILL.md:66).

```
 /sc:issue --claim N [--pipeline L] [--submit]
   W0 orch   origin_repo.py, gh auth, orca_worktree.py preflight, default branch   (claim.md:11-21)
   W1 T3     scout.md  (lookup)                                                    (claim.md:23-34)
   W2 orch   edge cases: closed / assigned-to-other => STOP, no writes             (claim.md:36-44)
   W3 orch   gh issue edit --add-assignee @me ; clickup_claim.py                   (claim.md:46-51)
   W4 T2|T1  accuracy-check.md, issue-summary.md (+ analysis if out of date)       (claim.md:53-63)
   W5 orch   Skill sc-recommend -> next-steps.md ; resolve level L ; prompt render (claim.md:75-84)
   W6 orch   post/edit accuracy-check + claim comments        <- --pipeline none ends here (claim.md:86-96)
   W7 orch   orca_worktree.py worktree  (create/reuse issue-<N>, copy .dev/issues/<N>/)  (claim.md:98-115)
   W8 orch   orca_worktree.py launch  -> pending/<nonce> + agent with [sc-launch:v1:<nonce>]  (claim.md:117-136)
```

**Waves and owners**

| Wave | Actor | Action | Output |
|---|---|---|---|
| 0 | orchestrator | origin, `gh auth status`, `orca_worktree.py preflight` (runs for `none` too), default branch via `gh repo view`, mkdir `<D>` | `<D>` = `.dev/issues/<N>/` (`claim.md:11-21`) |
| 1 | worker T3 | issue, comments, merged PRs, git log lookup | `scout.md` |
| 2 | orchestrator | edge cases from `scout.md` | STOP or continue |
| 3 | orchestrator | assign on GitHub, then ClickUp script | `clickup.json` |
| 4 | worker T2 (T1 when scout sizes `complex`) | accuracy check, summary, optional `/sc:analyze` | `accuracy-check.md`, `issue-summary.md`, `analysis/analyze-<scope>.md` |
| 5 | orchestrator | `Skill sc-recommend`, level pick, plan boundary, `orca_worktree.py prompt` | `recommend.md`, `next-steps.md`, `launch-prompt.md` |
| 6 | orchestrator | post or edit two marked comments | `claim-comment.md`, comments on the issue |
| 7 | orchestrator (script) | create or reuse the worktree | `worktree.json` |
| 8 | orchestrator (script) | launch the agent | `launch` entry in `worktree.json` |

**GitHub and ClickUp writes (all by the orchestrator; no write before Wave 3; none before the Orca preflight passes, `claim.md:21`)**

| # | Path | Exact command | Wave | Evidence |
|---|---|---|---|---|
| C1 | claim | `gh issue edit <N> --repo <R> --add-assignee @me` | 3 | `claim.md:48`, `SKILL.md:74,87` |
| C2 | claim | ClickUp `PUT https://api.clickup.com/api/v2/task/{task_id}` body `{"assignees": {"add": [<user id>]}}` via `uv run --no-project python "<skill base>/scripts/clickup_claim.py" --issue-url <url> --issue-number <N> --repo <R>` (only when exactly one task matches) | 3 | `clickup_claim.py:232-237`, `claim.md:50` |
| C3 / C3' | claim | `gh issue comment <N> --repo <R> --body-file <D>/accuracy-check.md`; or edit `gh api -X PATCH repos/<R>/issues/comments/<id> -F body=@<D>/accuracy-check.md` | 6 | `claim.md:89,91` |
| C4 / C4' | claim | same two forms with `claim-comment.md` | 6 | `claim.md:92` |
| C5 | launched agent, not the claim | at `full --submit` only: commit, `git push origin <branch>`, `/sc:pr-submit --monitor 3 --head <branch> ...` | after W8 | `templates/launch-prompt.md:28-34` |
| X1 | create | `gh issue create --repo <R> --title "[FEATURE|BUG] <title>" --body-file <D>/issue-body.md [--label ...] [--type ...]` | create W5 | `create.md:92`, `SKILL.md:103` |
| X2 | create | `gh api -X POST repos/<R>/issues/<N>/issue-field-values --input .dev/issues/<N>/complexity-field.json` | create W5 | `create.md:95`, `labels.md:43` |
| X3 | create | `gh issue comment <N> --repo <R> --body-file .dev/issues/<N>/create-review.md` (marker `<!-- sc:issue:create-review -->`) | create W5 | `create.md:96` |

The claim writes no label, issue type, issue field, status change or PR (`issue.md:93-102`, `labels.md:7`). Posts go up directly, never shown for approval (`SKILL.md:76`); markers `<!-- sc:issue:claim -->` (`claim-comment.md:23`) and `<!-- sc:issue:accuracy-check -->` (`accuracy-check-comment.md:20`) make a re-run edit instead of duplicate. Workers never write to GitHub or ClickUp. `create` makes no ClickUp call and no self-assignment (`create.md:9`). Every `gh` write passes `--repo <R>` with `<R>` from `origin_repo.py` only (`SKILL.md:72-73`); `origin_repo.py` resolves the fork only when the clone's `origin` URL is the fork (`origin_repo.py:14-15`; the guarantee is a property of the clone, not of the script).

**STOP codes (prose, executed by the model) and exit codes**

| Code | Condition | Source |
|---|---|---|
| `E-CREATE-ONLY-FLAG` / `E-CLAIM-ONLY-FLAG` | `--depth/--mode/--type` with `--claim` / `--pipeline/--submit` with `--create` | `issue.md:53,57` |
| `E-SUBMIT-NEEDS-FULL` | `--submit` with a value, without `--pipeline full`, or with no `--pipeline`; the script re-checks (exit 2) | `issue.md:59`, `OW:1900-1901` |
| `E-NO-ORIGIN` (exit 1), `E-FOREIGN-REPO` (3), `E-NOT-AN-ISSUE` (4) | origin missing or not GitHub; claim URL on another repo; `/pull/<N>` or non-issue argument | `origin_repo.py:47-50,114-153` |
| `E-GH-AUTH`, `E-ORCA-REQUIRED` | `gh auth status` fails; preflight `ok:false` (before any write, even for `none`) | `claim.md:16,17` |
| `E-WORKER-NO-OUTPUT`, `E-TIER-UNAVAILABLE` | worker file missing after one retry; tier not served (no alias fallback) | `SKILL.md:66,167`, `tiers.md:44-52` |
| `E-ASSIGN-FAILED`, `E-POST-FAILED`, `E-CREATE-FAILED` | assignee failure (before ClickUp and comments); comment post failure; `gh issue create` failure | `claim.md:48,93`, `create.md:92` |
| (no code) | usage errors, closed issue, assigned to another login: "not claimed", no writes | `issue.md:52,54-56,58`, `claim.md:41-42` |

Exit codes: `origin_repo.py` 0/1/3/4 and 2 (argparse); `clickup_claim.py` 2 only for bad arguments (the GitHub assignment stays, `claim.md:51`); every other `orca_worktree.py` outcome prints one JSON object and exits 0, exit 2 only for argparse (`OW:11-12`). Warning codes (never STOP; claim `status` stays `success`): 8 worktree codes in rank order `W-ORCA-LIST-FAILED`, `W-ORIGIN-BASE-MISSING`, `W-WORKTREE-CREATE-FAILED`, `W-WORKTREE-AMBIGUOUS`, `W-WORKTREE-STALE`, `W-WORKTREE-COPY-FAILED`, `W-ORIGIN-BASE-STALE`, `W-FIRST-TAB-LEFT` (`OW:230-239`); 4 launch codes `W-LAUNCH-FAILED`, `W-LAUNCH-NOT-CCSESSION`, `W-ENFORCEMENT-ABSENT`, `W-L2-ABSENT` (`REMEDY` `OW:802-817`); ccsession note stays first, `also W-L2-ABSENT` goes to `detail` (`claim.md:134`, `OW:1825`).

**`--pipeline` levels**

| Level | What the launched agent does | In code (`orca_worktree.py`) | Source |
|---|---|---|---|
| `worktree` | Orca worktree plus agent; runs `next-steps.md` up to `Plan boundary`, prints the plan path and `Waiting for approval`; a person approves by running a prompt whose first line starts `/sc:implement` or `/task` (the template at `launch-prompt.md:23` also names `/sc:task`; [CODE-CONTRADICTED], the guard regex at `GD:347` does not accept it, see 5.3 and Section 14 D-23); still no commit, push, `/sc:pr-submit` | `--level worktree` (`OW:1873,:1883`); pending word `worktree` | `launch-prompt.md:20-23`, `issue.md:43` |
| `full` | every step; no commit, push or PR; stages nothing; prints `git status --short` | `--level full`; word `full` | `launch-prompt.md:25-26` |
| `full --submit` | adds: no open or merged PR for the branch, conventional commit (stage `.dev/tasks` and changed files, never `.claude/`, never `.dev/issues/`), `git push origin <branch>`, `/sc:pr-submit --monitor 3 ...`, never merge | `--submit` with `--level full`; word `full-submit` (`OW:1759-1761`); `prompt` adds the `submit` block | `launch-prompt.md:28-34`, `issue.md:44` |
| `none` | no worktree, no agent; the claim ends after Wave 6 | not a `--level` value; only `preflight` runs | `issue.md:43,83`, `claim.md:94` |

Default-level rule (prose only, `claim.md:81`; no code): an explicit `--pipeline` wins; if Type, Complexity or Effort estimate cannot be read from `issue-summary.md` the level is `worktree`; else `full` for every bug, `full` for a simple or medium feature of 16 hours or less, `worktree` for a complex feature or one over 16 hours; the printed line is `Level: <L> (explicit)` or `Level: <L> (default: <reason>)`. The watcher always passes `--pipeline none` (`issue.md:48`; `src/superclaude/cli/issue_watch/launch.py:84-92`). **Contradiction [CODE-CONTRADICTED]:** `docs/designs/sc-issue-claim-pipeline-flag.md:21,43,66` still lead with "default `worktree`" before later amendments; `claim.md:81` and `issue.md:43` are the stronger evidence (they are what the model executes). Pinned only as text: `T/skills/test_issue_protocol.py:774`, `:791`; `T/commands/test_issue_command.py:182`.

**orca_worktree.py subcommands** (stdlib only, no shell; timeouts `DEFAULT_TIMEOUT=120`, `PREFLIGHT_TIMEOUT=30`, `TERMINAL_READ_TIMEOUT=15`, env `SC_ORCA_TIMEOUT`, `OW:88-91`; `run()` never raises, `OW:132-166`)

| Subcommand | Behaviour | Evidence |
|---|---|---|
| `preflight` | argv `orca status --json`; prints `{"ok": true}` only when the runtime is reachable, else `{"ok": false, "detail": ...}` | `cmd_preflight` `OW:210-223` |
| `worktree` | find main checkout via `git rev-parse --path-format=absolute --git-common-dir`; `orca worktree list --repo path:<main> --limit 500 --json`; reuse lookup keys in order `marker` (`sc:issue <R>#<N>` in the row comment), `record`, `basename` (`^issue-<N>(-\|$)`), `branch`; none: `git fetch origin`, verify base, create with `orca worktree create --repo path:<main> --name issue-<N> --base-branch <base> --no-parent --comment "sc:issue <R>#<N>" --json` (no `--agent`, `--issue`, `--pr`); relist; `finish()` copies `<D>` into `<wt>/.dev/issues/<N>/` (skips `worktree.json`, refuses symlinks, never overwrites a tracked file, a differing untracked file becomes `<name>.prev`); writes `<D>/worktree.json`; closes the first plain tab only for a new worktree | `cmd_worktree` `OW:625-738`, `lookup` `:373-411`, `finish` `:527-563`, `copy_issue_dir` `:439-504`, `close_first_tab` `:568-622` |
| `prompt` | keeps blocks `common` + level (+ `submit`), replaces `<N>`, `<R>`; `kept` (writes nothing) when a launch entry exists and the file exists | `cmd_prompt` `OW:764-784` |
| `launch` | see order below | `cmd_launch` `OW:1696-1834` |
| `pending --level worktree\|full\|full-submit` | writes one pending record, prints `{"ok": true, "nonce": ...}`; meant for a coordinator that starts a worker itself | `OW:1515-1523`; no production caller |

**Launch order ("refuse early, write the record last")**

| Step | Check or action | Failure result | Evidence |
|---|---|---|---|
| 1 | usable worktree record | `failed`, `W-LAUNCH-FAILED` | `OW:1700-1702` |
| 2 | `launch` entry in `<D>/worktree.json` or mirror `<wt git dir>/sc-issue-launch-<N>.json` | `already_launched`, no Orca call | `OW:1704-1721`, `:1586-1616` |
| 3 | worktree `launch-prompt.md` byte-identical to `<D>/launch-prompt.md` | `failed`, `W-LAUNCH-FAILED`, no agent | `stale_prompt` `OW:1666-1693`, `:1722-1724` |
| 4 | IR-4 `enforcement_preflight(wt)` (read-only: `jq`, `uv`, guard commands `cat sed tr mkdir mv ln rm`, Linux process interfaces, `~/.claude/hooks/launch-level-guard.sh` executable with line `# launch-level-guard-version: 1`, `CLAUDE_CONFIG_DIR`, `disableAllHooks`, guard registered on `UserPromptSubmit` and on `PreToolUse` for all 23 `GOVERNED_TOOLS`, identity hook registered for `Bash`) | `failed`, `W-ENFORCEMENT-ABSENT`, no pending record, no agent | `OW:955-1045`, `:1730-1747`, `GOVERNED_TOOLS` `:841-867` |
| 5 | `install_l2(wt)` then `l2_status(wt)`; not `owned` adds a `W-L2-ABSENT` note; `if IR7_REFUSE and l2_notes:` would refuse | with `IR7_REFUSE = False` never refuses | `OW:1754-1758`, `:822` |
| 6 | `publish_pending(word)` writes `~/.claude/state/launch-level/pending/<32-hex nonce>` (dirs 0700, file 0600, `.tmp-<nonce>` then `os.replace`) | `failed`, `W-LAUNCH-FAILED` | `OW:1488-1512`, `:1759-1775` |
| 7 | `orca agent launch --agent claude --worktree path:<wt> --surface terminal --prompt "[sc-launch:v1:<nonce>] Read .dev/issues/<N>/launch-prompt.md and follow it." --json` (no `--model`, `--effort`, link flag) | not-ok reply: pending record removed, `failed` with a `hand_command` | `OW:1776-1793` |
| 8 | shim detection `behind_ccsession(handle)`: up to 5 tries, 2.0 s apart (`SC_ORCA_SHIM_INTERVAL`), `orca terminal read --terminal <h> --screen --json` for `[ccsession]` or `Session name (Enter or Ctrl+C`, else `orca terminal show` title regex `sc-launch-v1-<hex>-<MMDD>-<HHMMSS>-<hex4>` | `W-LAUNCH-NOT-CCSESSION` note; launch still counts as `launched`; the agent is not closed | `OW:792-800`, `:1564-1583`, `:1802-1811` |
| 9 | `record_launch` writes `{level, submit, at}`; `session_report` returns `release` text and `layers` | write failure adds text, does not fail | `OW:1619-1643`, `:1445-1485`, `:1814-1833` |

L2 install (`install_l2` `OW:1386-1442`, read-only `l2_status` `:1048-1067`): puts `pre-push` and data file `pre-push.launch-level` into `<git-common-dir>/hooks/`, shared by every worktree of the clone; an existing entry is never replaced; the staged copy is self-tested (`_l2_selftest` `:1278-1332`) before `os.link` (`:1428`); `core.hooksPath` set, hooks dir not the common one, or an unsafe dir gives `unsupported`. [STALE DOC] `claim.md:125` and `sc-issue-claim-pipeline-flag.md:59` say "the worktree's `pre-push` hook" (code: shared hooks dir, `OW:1365,1402`); `claim.md:125` says IR-4 runs "before anything else" (code: record, already-launched and stale-prompt checks run first, `OW:1700-1724`) and names `git rev-parse --git-path hooks/pre-push` (code asks `--git-path hooks`, `OW:1357`); `pending` is not named in `SKILL.md:35`.

**Worker tiers and models**

| Agent file (35 lines each; erratum applied) | `model:` (line 6) | Other frontmatter | Jobs |
|---|---|---|---|
| `AG/issue-worker-t3.md` | `claude-gw-tier2b` | `effort: low` (line 7) | claim lookup (`scout.md`), create lookup, quick body |
| `AG/issue-worker-t2.md` | `claude-gw-tier2` | tools `Read, Grep, Glob, Write, Bash` (line 5; no Edit) | claim Wave 4 simple or medium; quick flag choice; standard flag validation and body |
| `AG/issue-worker-t1.md` | `claude-gw-tier1b` | same tools | claim Wave 4 when scout sizes `complex`; standard and deep flag choice; deep body |

The skill passes only `subagent_type: issue-worker-t<N>`, never `model` (`SKILL.md:54-64`, picker table `:58-62`). The only fallback is T1 to T2, once, on a not-served spawn (`tiers.md:34-42`); T2 and T3 have none. **Contradiction [CODE-CONTRADICTED]:** `docs/designs/sc-issue-command.md:58,107,129,391,423,449` pin T3 to `claude-gw-tier3`; the agent file (`issue-worker-t3.md:6`), `tiers.md:17` (issue 488 decision) and `T/skills/test_issue_worker_agents.py:22-23` say `tier2b`, the stronger evidence; no test scans `docs/designs/`. Proxy behaviour and the model order behind the pins are [UNVERIFIED] (`tiers.md:23-26,36`).

**Local artefacts** (`<D>` = `.dev/issues/<N>/`, never staged, `issue.md:100`): `scout.md`, `clickup.json`, `accuracy-check.md`, `issue-summary.md`, `analysis/analyze-<scope>.md`, `recommend.md`, `next-steps.md`, `launch-prompt.md` (not for `none`), `claim-comment.md`, `worktree.json` (origin checkout only, `{"path","status","launch":{...}}`, atomic 0644; not written for `none`) (`issue.md:80`). Outside `<D>`: the `<wt>/.dev/issues/<N>/*` copy, mirror `<wt git dir>/sc-issue-launch-<N>.json`, `pending/<nonce>` (written by the claim), `<git-common-dir>/hooks/pre-push[.launch-level]`. `sessions/`, `requests/`, `jobs/` are never written by the claim (grep of `OW`).

**Test pins per behaviour** (files under `T/`; read by name, not run)

| Behaviour | Pinning file and key tests |
|---|---|
| Protocol text, waves, file inventory, codes, return contract, default-level text, fork safety | `skills/test_issue_protocol.py` (1055 lines, 62 tests): `test_every_named_path_exists_and_every_file_is_named` :147, `test_st6_preflight_is_in_wave_0_and_worktree_is_wave_7_after_the_posts` :251, `test_every_worktree_warning_code_is_listed_with_a_remedy_line` :350, `test_st10_claim_return_contract_has_the_ten_fields_and_keeps_the_old_ones` :560, `test_default_level_rule_is_bug_full_complex_feature_worktree` :791, `test_every_gh_issue_pr_label_mention_carries_repo` :833 |
| Command front: seven flags, STOP rules, version `1.1.0` | `commands/test_issue_command.py` (212 lines, 15 tests): `test_st1_options_table_lists_exactly_the_seven_flags` :84, `test_submit_rule_stops_a_bare_submit_and_keeps_its_message` :191 |
| `orca_worktree.py` against a fake `orca` (create argv, lookup keys, copy rules, launch argv, IR-4, IR-7 warns, shim detection, `pending`) | `skills/test_issue_orca_worktree.py` (2501 lines, 109 tests): `test_la1_launch_argument_list_is_exact`, `test_fo18_exact_commands_and_no_forbidden_flag` :837, `test_ir4_each_failing_condition_refuses_the_launch`, `test_ir7_l2_absent_warns_and_the_launch_proceeds` :1838, `test_la5_launch_shim_check_failure_keeps_the_launch_and_warns`, `test_pending_writes_one_private_record_and_prints_its_nonce` (:2472-2496) |
| L2 install and the IR-7 switch | `skills/test_issue_l2_install.py` (716 lines, 26 tests): `test_ir7_shipped_switch_is_off` :639, `test_hookspath_is_unsupported` :312, `test_l2_status_never_writes` :575 |
| Repo resolution, exit codes 1/3/4 | `skills/test_issue_repo_resolution.py` (291 lines, 18 tests): `test_claim_url_on_another_repo_is_e_foreign_repo`, `test_pull_url_on_origin_is_rejected_not_parsed` |
| ClickUp: the one PUT, no-PUT outcomes, caps, token never printed | `skills/test_clickup_claim.py` (569 lines, 29 tests, 41 collected cases): `test_assign_sends_assignees_add_body` :311, `test_ambiguous_returns_candidates_and_makes_no_put` :277, `test_token_never_printed_on_any_outcome` :548 (its fake server rejects any other request type, :145-146) |
| Worker pins, tools, read-only rules | `skills/test_issue_worker_agents.py` (559 lines, 24 tests): `test_worker_file_exists_with_pinned_picker_id` :77, `test_t3_effort_is_low` :85, `test_tools_exclude_edit` :102; `skills/test_model_alias_policy.py` (249 lines, 11 tests; 4 touch this pipeline, the other seven are repository-wide alias policy): `test_frontmatter_model_is_an_alias_when_present` :83 |
| T1 to T2 fallback | `skills/test_issue_t1_fallback.py` (69 lines, 8 tests) |

**Extension points**

| File | Function or case | What to change | Pinning test file |
|---|---|---|---|
| `CMD`, `claim.md:81`, `templates/launch-prompt.md`, `OW` choices `:1873,:1883,:1891` | add a pipeline level | option rows and STOP rules (`issue.md:43,58`), the level rule, a new block (`BLOCK_MARKER` regex `[a-z]+`, `OW:743`), the three `choices`, then the guard word table `GD:264-269` | `test_issue_protocol.py` (4-block check :295), `test_issue_command.py` :84, `test_issue_orca_worktree.py` |
| `OW` `REMEDY` `:802-817` or `WARNING_ORDER` `:230-239` | add a warning code | the code, its remedy line in `claim.md` (`:106-115`, `:127-132`) and the `SKILL.md` error table (`:161-162`) | `test_every_worktree_warning_code_is_listed_with_a_remedy_line` |
| `AG/issue-worker-tN.md`, `SKILL.md:58-62`, `tiers.md:11-15` | add a worker tier | new agent file with `model:` picker id, tier key in `ccsession-models.json` | `T/skills/test_issue_worker_agents.py:21-26` (`WORKERS`) |
| `SK/templates/`, `SKILL.md:36-50` | add a template | the file plus a files-table row | `test_every_named_path_exists_and_every_file_is_named` |

---

### 5.3 Guard stack and launch levels

**Purpose:** A claim launched at `worktree`, `full` or `full --submit` starts an agent whose permitted actions are limited by a level. The level travels only as files under `~/.claude/state/launch-level/`; a Claude Code hook (L1 guard) reads it on every prompt and tool call, a second hook rewrites governed Bash calls so a git hook (L2) can tell the agent from a person. The prompt text itself (`launch-prompt.md`) is advisory; only L1 and L2 enforce.

**Status lines**

| Piece | Status | Evidence |
|---|---|---|
| L1 guard `launch-level-guard.sh` (808 lines, version line `GD:10`) | BUILT-ON | registered on `UserPromptSubmit` (`HJ:63-71`) and `PreToolUse` (`HJ:115-124`); copied by `install_hooks.py:93`; required by the claim's IR-4 preflight (`OW:975-988`) |
| Job identity `launch-job-identity.sh` (582 lines) | BUILT-ON | `PreToolUse` matcher `Bash`, after the guard (`HJ:125-134`); `install_hooks.py:90`; IR-4 requires it (`OW:1037-1044`); Linux and `uv` needed |
| L2 pre-push hook `launch-level-pre-push.sh` (208 lines) | BUILT-ON, claim-installed only; not in `hooks.json` | template copied to `~/.claude/hooks/` (`install_hooks.py:96`); written into a clone by `install_l2`, called only from `cmd_launch` (`OW:1754`) |
| G2 rule 2 (a bound worker may run `orchestration send` or `ask` only with no `--to`) | BUILT-ON | `GD:485`, `GD:496-537`; plugin copy identical; stated at `WC:66`; pinned by `T/hooks/test_launch_level_guard_worker.py` |
| G1 (a worker started by a coordinator runs with no marker, so no guard) | NOT BUILT as a guard; it is the live condition for such workers | no caller of `orca_worktree.py pending`; the guard design says it does not govern such a worker (`docs/designs/sc-issue-launch-level-hook.md:23`; see Section 14) |
| G2 rule 1 / route A (coordinator writes the worker's `.ok`) | REMOVED | zero hits for `release-worker`; guard comment `GD:496-497` says the rule 1 text is retired; the only `.ok` writer left is the guard's typed-prompt branch `GD:358`; see Appendix B |
| G2 route B (signed approval file) | NOT BUILT | no `signature`/`hmac`/`openssl` in `GD` or `ID` |

**Key Files**

| File | Purpose |
|---|---|
| `GD` | L1: binds a pending launch, classifies each tool call, exits 0 or 2 |
| `ID` (bash prologue `:1-54`, embedded Python `:55-581`, `exec uv run --no-project python -I` `:582`) | PreToolUse(Bash) rewriter; `identify`, `prepare`, `run`, `execute` subcommands |
| `PP` (`#!/bin/bash -p`) | git `pre-push` hook: refuses pushes to `refs/heads/main` and `refs/heads/master` from a governed or unknown actor |
| `HJ` (192 lines), `plugins/superclaude/hooks/hooks.json` (154 lines) | registrations |
| `src/superclaude/cli/install_hooks.py` (614 lines) | copies scripts, merges registrations into `~/.claude/settings.json` |
| `src/superclaude/cli/install_ccsession.py` (161 lines), `src/superclaude/skills/ccsession-tag/ccsession-orca` (263 lines) | ccsession wiring and Orca's Claude command; no launch level |

**Which launch paths each layer governs**

| Launch path | Pending record and marker | L1 and L2 | Evidence |
|---|---|---|---|
| `/sc:issue --claim` at `worktree`, `full`, `full --submit` | yes, `launch` writes `pending/<nonce>` and the prompt carries `[sc-launch:v1:<nonce>]` | L1 binds on the agent's first prompt; L2 installed in the clone and consulted on `git push` | `OW:1754-1779` |
| Watcher session (`/sc:issue --claim <N> --pipeline none`) | no: for `none` only `preflight` runs, so no launch step, no `pending` record, no `install_l2`; the watcher prompt pattern has no marker | no L1/L2 binding: the session is ordinary (guard exit 0) | `launch.py:33,84-92` (prompt pattern), `OW` `none` handling (`claim.md:94`), `GD:391` |
| Worker started by a coordinator (`worker-start`) | no: nothing calls `orca_worktree.py pending` and the brief template (`WC:303-311`) has no marker slot (0 hits for `sc-launch`) | no L1/L2 binding; by the code reading a process with no job record is `ordinary` (`ID:228-229`) and `PP` exits 0 at once (`PP:188`) | `docs/designs/sc-issue-launch-level-hook.md:23` says the guard does not govern such a worker (see Section 14) |
| Any other session | no | L1 exits 0 for every event (`GD:391`) | observed S01, S03 |

**Binding state machine** (first prompt binds a pending launch to a session; `GD:314-385`)

```
 claim launch                                   L1 guard, agent's FIRST UserPromptSubmit
 publish_pending --> pending/<nonce> ----------> prompt matches \[sc-launch:v1:([0-9a-f]{32})\]  (GD:318)
   (word: worktree | full | full-submit)           subagent prompt (agent_id set) => exit 0, never binds (GD:315)
                                                   mv pending/<nonce> sessions/.take-<sid>   (one rename wins, GD:372-375)
                                                   ln .take-<sid> sessions/<sid>             (hard link; first binding wins, GD:299-313)
 level word -> W (worktree) | F (full) | FS (full-submit) | other word => "degraded" read as W + LL-STATE note (GD:264-269,306)
 W + typed first line  ^[[:space:]]*/(sc:implement|task)([[:space:]]|$)  => sessions/<sid>.ok  => WA   (GD:347-360)
 release (kill switch): a person deletes sessions/<sid> and sessions/<sid>.ok; approval lasts until then (GD:361)
```

A marker that cannot be bound is `LL-NOBIND` (exit 2): empty session id, unowned or symlinked `sessions/`, no regular session file afterwards (`GD:366-384`). Empty-store fast exit: no `sessions/` directory and no `[sc-launch:` in the input gives exit 0 (`GD:168-173`).

**State stores** (root `$HOME/.claude/state/launch-level/`, three literals `GD:20-23`; the guard reads only `HOME`)

| Path | Writer | Reader | Format |
|---|---|---|---|
| `pending/<32 hex>` | `publish_pending` (`OW:1488-1512`) | guard (`GD:334-337`, `mv` `:374`); claim deletes it on launch failure (`OW:1783`) | one level word, no newline; file 0600, dir 0700 |
| `sessions/<sid>`, `.take-<sid>`, `.tmp-<sid>-<pid>` | guard (`GD:289-313`) | guard, identity `governed()` (`ID:177-186`), `identify` | level word (read as 13 bytes); `degraded` read as W |
| `sessions/<sid>.ok` | guard approval branch, noclobber (`GD:356-359`) | guard (`GD:270`) | empty file; observed mode 600 |
| `requests/<32 hex>` | identity `publish()` (`ID:164-174`) | identity `run`, consumed once under flock | JSON `{session_id, tool_use_id, command}`, 0400 |
| `jobs/<kernel sid>.json` | identity supervisor (`ID:307-375`) | `identify` (`ID:215-260`), `PP` via `identify` | keys `pid, start, boot, kernel_sid, session_id`, 0400 |

No pruning of `pending/` or `sessions/` (design `docs/designs/sc-issue-launch-level-hook.md:627`, owner decision O-15). The installer never creates the store (`install_hooks.py`; the claim and the two hooks do).

**LEVEL MATRIX** (W = `worktree`, WA = `worktree` approved, F = `full`, FS = `full --submit`). Source of decisions: `GD:783-803`; oracle `EXPECTED` `T/hooks/test_launch_level_guard.py:806-854`. Every pin below is a case of `T/hooks/test_launch_level_guard.py::test_grid_policy[<id>]` (:3394); all 16 cells were OBSERVED to match in the run below.

| Level | IMPL (Skill `sc:implement`) | COMMIT (`git commit -m x`) | PUSH (`git push -u origin feature`) | SUBMIT (Skill `sc:pr-submit`, `gh pr comment/create`) |
|---|---|---|---|---|
| W | block `LL-IMPL`; `GRID-IMPL-skill-implement-W` | block `LL-COMMIT`; `GRID-COMMIT-git-commit-W` | block `LL-PUSH`; `GRID-PUSH-git-push-canonical-W` | block `LL-SUBMIT`; `GRID-SUBMIT-skill-pr-submit-W` |
| WA | allow; `GRID-IMPL-skill-implement-WA` | block; `GRID-COMMIT-git-commit-WA` | block; `GRID-PUSH-git-push-canonical-WA` | block; `GRID-SUBMIT-skill-pr-submit-WA` |
| F | allow; `GRID-IMPL-skill-implement-F` | block; `GRID-COMMIT-git-commit-F` | block; `GRID-PUSH-git-push-canonical-F` | block; `GRID-SUBMIT-skill-pr-submit-F` |
| FS | allow; `GRID-IMPL-skill-implement-FS` | allow; `GRID-COMMIT-git-commit-FS` | allow; `GRID-PUSH-git-push-canonical-FS` | allow; `GRID-SUBMIT-skill-pr-submit-FS` |

Other classes (all rows pinned by the same `test_grid_policy` with ids `GRID-<CLASS>-<case>-<level>`; the research gives the class rows, not each id): TURN (Cron*/Schedule* tools) blocks at W only, like IMPL (`GD:786,788`); SKILL (a skill name that cannot be read) blocks at W, WA, F and allows at FS (`GD:787,790`); REPO, PUSHFORM, PROTECTED, MERGE, GHWRITE, UNKNOWN, MCP, ESCAPE, TAMPER, BIG block at every level including FS (`GD:791-800`). A cell with no match, or an empty level, is `LL-BROKEN` (`GD:801`). So F cannot commit, push or open a PR; only FS can; nothing at any level can merge, push main or master, or make a free-form `gh api` write. Second pins: `test_grid_level_steps` (:3457, ids such as `GRID-step-W-skill-implement`, `GRID-step-F-git-commit`, `GRID-step-FS-git-push`; no WA step); WA is also held by `test_skill_grid_matches_oracle` (:905) and `test_apr_approval_never_unlocks_commit_push_submit` (:3852). Block precedence (first class wins, `GD:783`): BIG TAMPER MERGE GHWRITE PROTECTED ESCAPE MCP UNKNOWN SUBMIT REPO PUSH PUSHFORM COMMIT TURN IMPL SKILL.

**Classifiers** (`GD:398-754`)

| Tool | Rule | Evidence |
|---|---|---|
| Skill | name normalised (first word, lower case, strip one `/`, text after last `:`, strip one `sc-` and one `-protocol`); `implement`, `task`, `cleanup` give IMPL; `pr-submit` SUBMIT; `issue` ESCAPE; unreadable SKILL | `GD:398-413`, IMPL line `:409` |
| Bash, Monitor | over 65536 bytes BIG; normalisation NM1a-NM7; TAMPER tokens; ESCAPE words (`ccsession*`, tmux, screen, xdotool, ydotool, `claude` plus a launch flag); orca allow-list; G2 rule 2; git; gh; canonical push | `GD:414-726` |
| git | `merge`, `pull` MERGE; `push` family PUSH; `commit`, `cherry-pick`, `am`, `commit-tree`, `revert` COMMIT; `update-ref` on HEAD, `--stdin`, `refs/heads/*` COMMIT; unknown subcommand or alias/config forms UNKNOWN; only `git push [-u\|--set-upstream] origin <branch>[:<dst>]` is canonical, dst `master`/`main` PROTECTED, `HEAD` or other forms PUSHFORM | `GD:580-725`, regex `:716` |
| gh | `gh api` allowed only as one plain GET else GHWRITE; `merge`, `update-branch`, `sync` MERGE; `pr create/edit/comment/ready`, `issue create/edit/comment` SUBMIT; `pr create` without `-R/--repo <value>` REPO | `GD:550-663` |
| Edit, Write, NotebookEdit | path only (after `/+` squeeze); a `..` segment is TAMPER; contents never read | `GD:727-735` |
| Agent, Task, others | `isolation == remote` ESCAPE; Cron*/Schedule* TURN; RemoteTrigger, Workflow, SendMessage ESCAPE; `mcp__*` write-like suffix MCP (MERGE if it contains merge) unless `list_/get_/search_/read_` | `GD:736-754` |
| TAMPER tokens | `.claude/state`, `.claude/settings`, `.claude/hooks`, `disableAllHooks`, `.gitconfig`, `.git/config`, `.config/git`, `.git/hooks`, `hooks/pre-push`, `pre-push.launch-level`, `--no-verify`, `hookspath`, `hook.pre-push`, `install_hooks`, `superclaude ... install` | `GD:440,451,760-775` |

IMPL list: code has three skills (`implement`, `task`, `cleanup`, `GD:409`); the design lists six (`implement`, `task`, `improve`, `cleanup`, `spawn`, `build`, `docs/designs/sc-issue-launch-level-hook.md:106,179,236,391`). [CODE-CONTRADICTED] by the guard, by `ls src/superclaude/commands` (`improve`, `spawn`, `build` absent) and by `test_lookalike_skill_names_stay_none` (`T/hooks/test_launch_level_guard.py:934-936`); the code is the stronger evidence. Pins: `test_impl_name_spellings` :927, `test_skill_grid_matches_oracle` :905.

**Typed approval versus the `/sc:task` mismatch.** The approval regex (`GD:347`) accepts a first line `/sc:implement` or `/task`, not `/sc:task`. `templates/launch-prompt.md:23` tells the agent that a first line starting `/sc:task` also approves. [CODE-CONTRADICTED]: grep of the guard for `sc:task` finds nothing, so a typed `/sc:task ...` does not create `<sid>.ok`; the code is the stronger evidence, and no file says which side is intended (Q-14, see Section 14). Note the Skill-tool classifier still treats a Skill call named `sc:task` as IMPL (blocked at W), so only the typed-prompt release differs. The design row that typed `approved` writes `.ok` (`sc-issue-launch-level-hook.md:123`) is [CODE-CONTRADICTED] by the design's own `:189`, by `GD:347` and by `test_apr_plain_approved_releases_nothing` (:3800).

**Fail-closed versus fail-open; exit codes; block words**

| Rule | Behaviour | Evidence |
|---|---|---|
| Exit codes | L1 and identity use only 0 (allow) and 2 (block); never 1, no `onFailure`; `ll_on_exit` trap turns any other rc into exit 0 (ordinary) or LL-NOBIND / LL-BROKEN exit 2 (governed) | `GD:4-6,135-163`; `ID:435-502,580` |
| Governed means only | valid session id AND `sessions/<id>` exists; a tool call with no governed record exits 0 | `GD:257,391` |
| Fail-open (ordinary session) | missing or invalid session id on a tool event ("identity loss"), no jq or unparseable JSON with no bound id, unrelated event | `GD:208-238,386-391` |
| Fail-closed (governed session) | jq failure on a payload containing a bound id, non-string tool field or NUL, unknown event, internal error, default deny | `GD:218-232,392,807-808` |
| Block words (18) | `LL-IMPL LL-COMMIT LL-PUSH LL-PUSH-FORM LL-PROTECTED LL-MERGE LL-GH-WRITE LL-SUBMIT LL-REPO LL-UNKNOWN LL-MCP LL-ESCAPE LL-TURN LL-TAMPER LL-SKILL LL-BIG LL-NOBIND LL-BROKEN`; LL-TAMPER prints the release `rm` command; notes `LL-STATE`, `LL-TEXT` | `GD:36-133`; pinned by `test_design_table_holds_all_eighteen_ids` (:1712) |
| Hook time limit | `timeout: 5` on both guard registrations and the identity hook; a killed hook allows the call (design V8/R2, not testable here) | `HJ:68,121,131` |

**G2 rule 2.** A bound worker may run `orca orchestration send` or `ask` only as one raw command of plain words and quoted strings, no expansion, no newline, at most 8192 bytes and 64 arguments; any option starting `--to`, `--run`, `--environment` or `--pairing-code`, a name that is a prefix of `--to` or `--run`, a bare word or a lone `--` is ESCAPE (`GD:496-537`, `LL_SA` set at `:485`). Allowed at every level, so a bound worker at W may send. The orca allow-list is `status`, `help`, `--version`, `worktree current|list|show`, `terminal list|show|read`, `orchestration check|inbox|run-current|task-list|worker-show`; any glob character turns the read verbs into ESCAPE; every other orca call is ESCAPE (`GD:480-491`). Pins: `test_a_bound_worker_may_send_and_ask_its_coordinator` (:74), `test_a_bound_worker_cannot_address_another_worker_or_a_group` (:187), `test_every_other_orca_word_stays_blocked_for_a_bound_worker` (:213), `test_a_forged_release_from_the_workers_own_session_is_blocked_as_tampering` (:262), all in `T/hooks/test_launch_level_guard_worker.py`; doc pin `messages-carry-no-to` (`T/skills/test_worker_contract.py:423-431`).

**orca-ide command-word gap.** The guard matches the basename `orca` only (`GD:457`); grep for `orca-ide` in the guard finds nothing. OBSERVED: a bound session at W ran `orca-ide terminal send --text hi` and `orca-ide orchestration send --to run:run_1 --body hi` with exit 0 (cases EXTRA-2, EXTRA-3), while `orca terminal send` and `/usr/local/bin/orca terminal send` were blocked. `orca-ide` is the default binary of `src/superclaude/cli/sweep/probes.py:43` and first in `src/superclaude/cli/install_user_setup.py:36`. `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:83` already records this as a DEFECT with a draft plan; no decision to fix was found (Q-17, see Section 14). Consequence: G2 rule 2 and the ESCAPE class do not constrain the `orca-ide` spelling.

**Job identity** (`ID`; not a sandbox, `ID:2`)

| Item | Behaviour | Evidence |
|---|---|---|
| Rewrite | PreToolUse(Bash) only; once `sessions/<sid>` exists, replaces the command with `shlex.join(['/bin/bash', script, 'execute', sid, tool_use_id, original])` through `hookSpecificOutput.updatedInput`; sets no `permissionDecision` | `ID:430-505`, output `:491-497` |
| Silent (exit 0) | input over 1 MiB, unparseable JSON, tool other than `Bash` (Monitor has no adapter), invalid session id, no session record, no `HOME` or store | `ID:20-24,433-453` |
| Closed (exit 2) | governed Bash call that cannot be wrapped: stderr `launch job: governed Bash call cannot be wrapped safely`; no `uv`: `launch job: UV is required for this invocation`; other: `launch job: invalid invocation or unavailable private state` | `ID:25-54,500-502,572-580` |
| `identify [PID]` | one JSON line: `ordinary`, `ordinary`+`released`, `governed`+`session_id`, `unknown` (with reason `stale\|orphaned\|foreign\|unreadable`) | `ID:215-260,546-553` |
| Declared limits | `setsid` or daemonising escapes selection; Monitor and pipelines unsupported; `cd` does not persist across governed Bash calls; ordering with other hooks unspecified | `ID:7-18` |

Writes to GitHub: none in the identity hook. Pins: `T/hooks/test_launch_job_identity.py` (1530 lines, 56 tests), `T/hooks/test_launch_level_guard_with_identity.py` (212 lines, 5 tests; Linux only; the guard must see the original command, :135; a `degraded` record blocks all Bash through the identity hook, :187).

**L2 pre-push hook** (`PP`): installed by the claim (`install_l2`, `OW:1754`) as `<git-common-dir>/hooks/pre-push` next to data file `pre-push.launch-level` (line 1 pinned `HOME`, line 2 `uv` directory); it is a git hook, not a Claude Code hook, so it is not in `hooks.json`, and a plain `superclaude install` only copies the template (`install_hooks.py:96`). Actor from `ID identify $$` under `env -i`, `timeout 10`; ordinary exits 0 at once (`PP:188`); protected refs `refs/heads/main` and `refs/heads/master` only (`PP:17`); governed plus protected `L2-PROTECTED` exit 1; unknown actor plus protected `L2-UNKNOWN` exit 1; malformed record from a non-ordinary actor `L2-MALFORMED` exit 2; pushes to other refs allowed for every actor (`PP:187-208`). It is the only hook here that exits 1 (`PP:9-10`). The feature-branch push control (commit, push, submit) lives in L1 only. Pins: `T/hooks/test_launch_level_pre_push.py` (1194 lines, 34 tests), `test_launch_level_pre_push_records.py` (230 lines, 8 tests).

**Registrations and installer** (`HJ`)

| Event | Matcher | Command | Timeout | Lines |
|---|---|---|---|---|
| UserPromptSubmit | none | `~/.claude/hooks/launch-level-guard.sh` | 5 | `HJ:63-71` |
| PreToolUse | `^(Bash\|Skill\|Agent\|Task\|Edit\|Write\|NotebookEdit\|Monitor\|Workflow\|RemoteTrigger\|SendMessage\|Cron[A-Za-z]*\|Schedule[A-Za-z]*)$\|^mcp__.*(merge\|push\|commit\|pull_request\|create_or_update_file\|delete_file\|update_ref\|create_ref\|create_branch)` | same guard | 5 | `HJ:115-124` |
| PreToolUse | `Bash` | `~/.claude/hooks/launch-job-identity.sh` (after the guard in file order) | 5 | `HJ:125-134` |

`install_hooks(target_path=None, force=False)` copies scripts to `~/.claude/hooks/` skip-if-exists unless `force` (`install_hooks.py:282-289`), merges registrations additively by command-path ownership, keeps the identity hook last (`:460-473`), writes `settings.json.bak.<UTC stamp>` first and refuses a malformed target (`:336-367`). Callers: `main.py:219` (install, `force` flag), `main.py:412` (update, `force=True`), `cli/eval/hook_adapter.py:230` (`force=False`). So a plain install keeps an older guard on disk; update or `install --force` refreshes it, and IR-4 refuses a guard without the version line (`OW:986-988`). A governed agent cannot re-run the installer (TAMPER, `GD:440,451`). Plugin copies: the three scripts are byte-identical (`cmp -s`; pinned by `T/hooks/test_launch_level_guard_l2_tokens.py:149`, `T/cli/test_install_hooks.py:1086-1109`); the plugin `hooks.json` has the same three launch-level registrations but also lacks the ccsession-tag entries, the `pragmatic-subagent.js` SubagentStart entry, and carries `"async": true` on `freshness-subagent-start.sh` (the scope hint saying "only ccsession-tag entries" is [CODE-CONTRADICTED], verified by `diff`). Registration pins: `T/hooks/test_launch_level_guard_registration.py` (127 lines, 7 tests).

**ccsession coupling.** The ccsession shim carries NO launch level: grep for `launch-level|sc-launch|LAUNCH_LEVEL|launch_level` over `src/superclaude/skills/ccsession-tag` returns zero lines; `ccsession-orca` sets `CCSESSION_ORIGIN` and unsets `CCSESSION_NAME`/`CCSESSION_ASK_TIMEOUT` (`ccsession-orca:198-256,249`) and never touches the store; `install_ccsession.py` registers no hooks and has no launch-level text (`install_ccsession.py:11-142`). The level travels only by files: `pending/<nonce>` then marker `[sc-launch:v1:<nonce>]` then `sessions/<sid>`. The claim only DETECTS the shim after launch (`behind_ccsession`, `OW:1564-1583`) and warns `W-LAUNCH-NOT-CCSESSION` (a warning, not a refusal); without the shim the guard still binds through the prompt marker. The shim passes the prompt through, which is how the marker reaches Claude and why the tab title starts `sc-launch-v1-<nonce12>-...` (`OW:793-797`). The word "shim" also names ccsession's `--shim` model-alias proxy; the claim does not check that proxy (Q-20). No test pins "the shim carries no level" (grep over `T/` finds none in ccsession test files).

**Ledger of guard items**

| Item | Status | Evidence |
|---|---|---|
| G1 (coordinator-started worker has no marker, so no guard) | NOT BUILT (as a guard) | see launch-path table; `docs/designs/sc-issue-launch-level-hook.md:23` says the guard does not govern such a worker |
| G2 rule 1 / route A | REMOVED | `GD:496-497`; `CHANGELOG.md:17` records the removal; see Appendix B |
| G2 rule 2 | BUILT-ON | `GD:485,496-537` |
| FU-1 (first live-test runbook for the claim hand-off) | REMOVED (its run steps name commands that no longer exist); the file's RECORDED lines a-k dated 2026-11-17 remain as text, [UNVERIFIED] | `docs/designs/issue-pipeline-fu1.md:64,108-119`; no `issue_pipeline` in `cli/main.py` |
| IR-3 `pipeline.json` | NOT BUILT | `sc-issue-launch-level-hook.md:34,615`; grep empty |
| IR-4 enforcement preflight | BUILT-ON | `OW:955-1045`, refusal `:1730-1747` |
| IR-7 refusal when L2 is not owned | BUILT-OFF | `IR7_REFUSE = False` `OW:822` (comment "owner decision 2026-11-08", turn on only after the #442 observations pass); `T/skills/test_issue_l2_install.py:639-641` |
| OB-H1 items 1-9, OB-H2, OB-H3, OB-CTX (live observations) | NOT BUILT (never run) | `T/hooks/test_launch_level_observations.py:79-84`: one test parametrized over 12 entries, body `pytest.skip(...: needs a real governed session and has not been run)`; design `sc-issue-launch-level-hook.md:6,625` "Pending, none run"; no code reads an observation record (see Section 14) |

**Observation run (OBSERVED versus READ-ONLY-READING).** OBSERVED: the unmodified guard script from the snapshot was run against 44 sample payloads with `env -i HOME=<sandbox> PATH=/usr/bin:/bin` (bash 5.2.37, jq 1.7; sandbox `research/05-guard-run-sandbox/` inside the task folder; `find -newer` found no change under the snapshot). All 44 matched the code reading: the 16 matrix cells; binding for W, F, FS and a `badword` record (became `degraded`); typed approval `/sc:implement x` creating `gov-w.ok` (mode 600) and moving W to WA; PROTECTED, MERGE and REPO blocked at FS; G2-A and G2-B allowed, G2-C (`--to`) and G2-D (`orca terminal send`) blocked; TAMPER on `rm -rf ~/.claude/state/launch-level`; fail-open for an ordinary id, identity loss, non-JSON with an ordinary id, event `Stop` for an ordinary session; fail-closed for non-JSON with a bound id (LL-BROKEN), marker in non-JSON (LL-NOBIND), event `Stop` for a bound session; the `orca-ide` gap. READ-ONLY-READING (not run): the identity hook, the L2 hook (they need `uv`, a live supervisor and git state outside the sandbox), the claim, both installers, the live observations OB-H1..3 and OB-CTX; no pytest was run.

**Test pins** (files under `T/`; 14 files in the research table plus 3 claim-side files, 17 in all; counts by `grep` of `def test_`)

| File | Pins |
|---|---|
| `hooks/test_launch_level_guard.py` (4631 lines, 162 tests) | binding B1-B13, classifiers, `test_grid_policy` :3394, `test_grid_complete` :3401, `test_precedence_order` :4520, 18 message texts, typed approval `test_apr_matching_prompt_writes_ok_at_w` :3737 |
| `hooks/test_launch_level_guard_l2_tokens.py` (160, 7) | hook-file and `--no-verify`/`hookspath` TAMPER tokens; mirror byte-identical :149 |
| `hooks/test_launch_level_guard_registration.py` (127, 7), `test_launch_level_guard_with_identity.py` (212, 5), `test_launch_level_guard_worker.py` (300, 11) | registrations; guard with identity; G2 rule 2 |
| `hooks/test_launch_job_identity.py` (1530, 56), `test_launch_level_pre_push.py` (1194, 34), `test_launch_level_pre_push_records.py` (230, 8) | identity; L2 matrix T-01..T-24 |
| `hooks/test_launch_level_observations.py` (84, 6) | nine fixtures, log-only probe; 12 skipped live cases |
| `cli/test_install_hooks.py` (1246, 37), `unit/test_install_ccsession.py` (417, 22), `core/test_orca_session_launch_guidance.py` (62, 3), `unit/test_ccsession_tag.py` (7101, 277), `unit/test_ccsession_tiers.py` (3821, 149) | installer; ccsession wiring and wrapper (no launch-level content) |
| claim-side: `skills/test_issue_l2_install.py`, `skills/test_issue_orca_worktree.py`, `hooks/test_require_orca_worktree_agent_governed.py` (56, 1) | L2 install, launch; governed-session block of bare `worktree create` |

**Extension points**

| File | Function or case | What to change | Pinning test file |
|---|---|---|---|
| `GD:783-803`, `ll_say` `:36-133` | add or change a block class or word | decision table, message, then the oracle `EXPECTED` | `hooks/test_launch_level_guard.py` (:806-854, :1712, :4520) |
| `GD:409` | add an IMPL skill | the `implement\|task\|cleanup` case | `test_impl_name_spellings` :927, `test_skill_grid_matches_oracle` :905 |
| `GD:480-491`, `GD:496-537` | add an allowed orca verb or change G2 rule 2 | allow-list or rule | `hooks/test_launch_level_guard_worker.py` :213, :187 |
| `GD:760-775` | add a TAMPER token | token list | `hooks/test_launch_level_guard_l2_tokens.py` |
| `HJ:115-124`, `OW:841-867` | guard a new tool name | matcher and `GOVERNED_TOOLS` (IR-4 checks every one) | `hooks/test_launch_level_guard_registration.py:68` |
| `GD:10`, `PP:2`, `install_hooks.py:90-96`, plugin copies | change a hook script | bump the version line, keep plugin copies byte-identical | `cli/test_install_hooks.py:1086-1118` |

---

### 5.4 Coordinator contract text (`WORKER-CONTRACT.md`)

**Purpose:** `WC` (339 lines) is the text a supervised coordinator and its workers follow. Sections: `## 1. Terms` :9, `## 2. Command-side rules` :27, `## 3. Worker-session duties` :49, `## 4. Coordinator rules` :68, `## 5. Coordinator brief template` :299. This subsection records what it says about the issue pipeline today: nothing issue-specific. The contract is documentation text; the technical reference states that no code runs the coordinator loop or distinguishes a coordinator from a worker (`docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:186`, doc claim, [UNVERIFIED] by the research).

**Rules present (WC-2 to WC-16: 15 rules; there is no WC-1)**

| Rule | Line | Content |
|---|---|---|
| WC-2 | 31 | no person-blocking step under `--unattended`; each gate resolves to a documented default, caller flag, or blocked |
| WC-3 | 53-58 | questions go to the coordinator; ask at most once per Task; a Ruling halt (`E-HALT-QA`, `E-NO-RULING`) is never asked; the person gives a Ruling in chat |
| WC-4 | 32-39 | one `return-contract.yaml` per outcome in the one report directory the brief names |
| WC-5 | 59 | worker sends `worker_done` once; `failed` for `failed`/`blocked`/no contract, `succeeded` for `succeeded`/`partial` |
| WC-6 | 72-80 | every retry is a new Task (never `worker-start --retry-of`); three-failed-starts cap |
| WC-7 | 60 | run at top level, never inside a subagent |
| WC-8, WC-13 | 40, 62 | a command or worker never calls `worker-start`, `dispatch`, `task-create` (WC-13 adds `worktree create --agent`, `agent launch`) |
| WC-9 | 41-45 | no outward action from a worker; only git write a brief may authorize is an end-of-Task local commit; coordinator stages `.dev/tasks` |
| WC-10, WC-11 | 46, 47 | liveness heartbeats, waits of at most 4 minutes; parallel-safe writes |
| WC-12, WC-14, WC-15 | 61, 63, 64 | follow-ups pulled and acked; no turn ends between chain steps; context-safe reading and handoff files |
| WC-16 | 287-289 | coordinator loop: never stops watching its Run, re-arms waits, runs the sweep and read-only `/sc:sweep` on each wake, escalates a closed list of states to the person; "Phase 1 adds this duty, not a scheduler" |

**Explicit finding.** `WC` has no WC-17 and no heading or sentence "Issue pipeline duties" (0 grep hits each), and no "issue pipeline", "watcher", "adopt", "claim" or "COORD-" text; "dispatcher" and "zero-setup watcher" are likewise not found in snapshot. The removal is recorded at `CHANGELOG.md:17` (see Appendix B). Several documents still name the missing section as live: `docs/designs/issue-watcher-setup.md:170` and `docs/designs/issue-watcher.md:43` [CODE-CONTRADICTED / STALE DOC], and `docs/designs/issue-pipeline-guard-g2-no-to.md:48` tells an editor to edit a rule that does not exist.

**Issue-related lines in the contract** (grep of `issue`, `grant row`)

| Line | Text | Relevance |
|---|---|---|
| 23 | `/sc:issue` is on the never-as-worker list (with `/sc:agent`, `/sc:closeout`, `/sc:git`, `/sc:help`, `/sc:pm`, `/sc:sweep`, `/sc:swarm-wizard`): never dispatched as a worker, no `--unattended` | the claim command may not run as a worker |
| 57 | WC-3 sub-bullet: "other owner records, such as a grant row or a pass record, are still written by the owner" | the phrase "grant row" occurs exactly once; the contract defines no store, writer verb or schema for it (a grep finds it also at `docs/designs/issue-pipeline-fu1.md:24,26`); no decision found in the files this reference cites about retiring it |
| 66 | "Messages carry no `--to`": a worker's `ask` and `send` carry no `--to`; the launch-level guard blocks any `--to` from a bound worker | the contract side of G2 rule 2 (see 5.3) |
| 242-243 | Git and GitHub ownership: actions target `IronbellyOrg/IronClaude`, never upstream, never through Orca issue or PR linking; "Progress posts (issue comments, project fields)" are coordinator actions; workers report only by heartbeats and `worker_done` | the only text on coordinator issue comments; names no issue-number source and no watcher |
| 258, 289 | "The coordinator starts only Tasks it created itself"; a ready Task it did not create is reported to the person (WC-16 lists it as an escalation) | bounds what a coordinator may start |

**Who starts a worker after a claim: not defined.** No contract rule says that a coordinator adopts a claimed issue, reads `.dev/issues/<N>/issue-summary.md` or `next-steps.md`, creates the issue worktree or starts a worker. The technical reference says so directly at `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:268`: the section "Issue pipeline duties" "was removed in issue 655 ... and until [its replacement] lands no contract rule says who starts that worker" [CODE-VERIFIED by reading the line]. The command side of the hand-off is prose only (`issue.md:85`, `SKILL.md:140`, `claim.md:96`: run `orca_worktree.py worktree`, then `worker-start --worktree path:<printed path>`); no Python in `src/` calls `worker-start` or `task-create`. Status: NOT BUILT (see Section 14). The binding of such a worker to the guard is the G1 row in 5.3; the brief template (`WC:299-312`) has no launch-marker slot. [STALE DOC] the same reference states "WC-2 to WC-15 ... 327-line contract" (`:196`) and ranges `:67-282`, `:283-327` (`:285`); the snapshot has WC-2 to WC-16, 339 lines, coordinator rules `:68-297`, template `:299-339`; its "739 tests" for the contract test (`:208`) is [UNVERIFIED] (the file has 59 `def test_`).

**Test pin.** `tests/skills/test_worker_contract.py` (3220 lines, 59 tests) pins the contract as text: `RULE_PHRASES` (:25-436, about 80 entries incl. WC-2 to WC-16, `messages-carry-no-to` :423-431), consumed by `test_contract_states_rule` (:876-878); the never-as-worker list including `/sc:issue` (:444-454); a write-verb audit of `src/superclaude/{skills,commands,agents}` (:1840-3141) that classifies the issue flow as read-only or never-worker (`agents/issue-worker-t*.md` :2890-2913, `sc-issue-protocol` :2914-2960, orchestrator-writes-only statement :3021); and `test_the_no_to_rule_sits_in_the_worker_session_duties` (:3216-3220). It contains no WC-17, "Issue pipeline duties", `issue-pipeline` or `watcher` text (0 grep hits) and has no test of absence.

---

**Open items for this synthesis (all listed in Section 14 and in the gap log):** whether OB-H1 item 1, OB-H2, OB-H3 have passed (Q-12); who runs `orca_worktree.py pending` (Q-13); which side of the `/sc:task` mismatch is intended (Q-14); whether coordinator-started workers should be bound (Q-11); whether the guard should recognise `orca-ide` (Q-17); live behaviour of the Orca flags, tier models and FU-1 RECORDED lines remains [UNVERIFIED] (C-36 to C-38, C-64).

