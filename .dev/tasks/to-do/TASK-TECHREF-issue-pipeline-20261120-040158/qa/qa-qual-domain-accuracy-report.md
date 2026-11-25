# QA Report - Domain Accuracy (Gate 3, qual-domain-accuracy)

**Document:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/techref/ISSUE-TO-WORK-PIPELINE-TECHNICAL-REFERENCE.md (2369 lines)
**QA phase:** qual-domain-accuracy
**Lens:** domain accuracy
**Report status:** complete (see the final line)
**Date:** 2026-11-20
**Fix authorization:** false (report only)

Source root used for every code check: /home/coder/.cache/ic-snap-20261120/master (read only; nothing was written there). Removed code was read only with `git -C /home/coder/workspaces/IronClaude show 01e7a9e23^:<path>` and `git ls-tree`/`git show --stat`. No file other than this report was written.

Adversarial stance: I started from "at least N=23 errors in the domain-accuracy lens". I looked for them in 100+ behavioural facts (65 numbered claims), 21 ledger rows, 13 absent-caller and artefact searches and 22 removed-code facts. I could evidence zero BLOCKING defects. The MINOR notes below are real but wording-level. Where I write CONFIRMED I read the cited line in the snapshot in this session.

Result in one line: 0 BLOCKING, 7 MINOR, verdict PASS (the final verdict line is at the end of the report).

## Part 1. Claim verification table (lens checklist item 1)

Claim = a behavioural claim in the document. Where = the document section. "WD" = watcher dir `src/superclaude/cli/issue_watch/`, "OW" = `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py`, "GD" = `src/superclaude/hooks/scripts/launch-level-guard.sh`. All paths are under the snapshot root.

### 1A. What the watcher writes to GitHub (weighted check requested by the prompt)

| # | Claim | Where | Code evidence path:line | Result |
|---|-------|-------|-------------------------|--------|
| 1 | The watcher writes nothing to GitHub: the only `"gh"` argv literals are five lines in github.py (177, 183, 204, 231, 255) | 4.5, 5.1.2, 8.1 | grep over all of WD for `"gh"`, `gh issue`, `gh api`, `--method`, `-X`, `POST`, `PATCH`, `PUT`, `DELETE`, `mutation`: hits only `github.py:107-108` (comment), `:177,183,204,231,255` (literals), `:206,257` (`--method GET`), `cycle.py:134` (comment) | CONFIRMED |
| 2 | Every REST call carries `--method GET`; GraphQL calls carry no `--method` and hold query text only | 4.5, 5.1.2 | `github.py:201-220` (`_argv_rest_page` has `"--method","GET"`), `:228-244` (`_argv_graphql` has none), `:74-103` (queries start `query(`, no `mutation`) | CONFIRMED |
| 3 | G1 argv is `gh api user --include` | 5.1.2, 8.1 | `github.py:175-177` | CONFIRMED |
| 4 | G2 argv ends `--json number,labels,assignees,state -L 100` and repo is the literal `IronbellyOrg/IronClaude` | 5.1.2 | `github.py:180-198`, `:37` | CONFIRMED |
| 5 | G7 argv is `gh api --method GET repos/<R>/issues/<N> --jq <REREAD_JQ>` | 5.1.2 | `github.py:252-262` | CONFIRMED |
| 6 | Only `runner.py` imports `subprocess`; `shell=False`, stdin DEVNULL, stderr cap 500 | 5.1, 12.1 | `runner.py:10, 15, 93, 99`; grep of `import subprocess` over WD gives only `runner.py:10` | CONFIRMED |
| 7 | The watcher's one outward effect is `orca agent launch`; the claim comments are written by the launched session | 5.1, 2.1 | `launch.py:84-116`, `cycle.py:1099` | CONFIRMED |
| 8 | Claim write: `gh issue edit <N> --repo <R> --add-assignee @me` (Wave 3) | 4.5, 5.2 | `refs/claim.md:48`; `SKILL.md:74` | CONFIRMED |
| 9 | Claim ClickUp write: one `PUT .../task/{task_id}` with `{"assignees":{"add":[id]}}`, only when exactly one task matches, env-gated | 4.5, 5.2 | `clickup_claim.py:164-169` (skip without token/workspace), `:225-237` (`already_assigned` returns before the PUT; PUT body) | CONFIRMED |
| 10 | Claim comments: `gh issue comment ... --body-file` or `gh api -X PATCH repos/<R>/issues/comments/<id> -F body=@file`; markers make a re-run edit | 4.5, 5.2 | `refs/claim.md:88-93`; `templates/claim-comment.md` last line `<!-- sc:issue:claim -->` (checked with `tail`) | CONFIRMED |
| 11 | Workers are read-only on GitHub and write only under `.dev/issues/`; only git write is `git fetch origin` | 4.2, 4.5 | `agents/issue-worker-t1.md:26-35` (same text in t2, t3) | CONFIRMED |
| 12 | `orca_worktree.py` has no `gh` call; its `run([...])` first words are `git` and `orca` only | 4.5 | grep for `"gh"` / `gh api|issue|pr` in OW: no hit; `run([` lines 211, 416, 619, 671, 672, 1348, 1593 | CONFIRMED |
| 13 | Create path writes `gh issue create`, `gh api -X POST .../issue-field-values`, `gh issue comment` (X1-X3) | 4.5, 5.2 | `SKILL.md:74, 103` | CONFIRMED |
| 14 | At level `full --submit` the guard allows `gh pr comment/edit/ready/create --repo` and `gh issue create/edit/comment`, still blocks merge, main/master push and free-form `gh api` | 4.5 C5 | `GD:650` (SUBMIT set), `:554-578` (GHWRITE), `:781-803` (SUBMIT:FS allowed; MERGE/GHWRITE/PROTECTED blocked at FS) | CONFIRMED |
| 15 | install_hooks, install_ccsession and ccsession-orca make no GitHub call | 4.5 | grep for `gh`, `urllib`, `requests`, `http` over the three files: no hit | CONFIRMED |

### 1B. The `enabled` default, launch command, constants, exit codes

| # | Claim | Where | Code evidence path:line | Result |
|---|-------|-------|-------------------------|--------|
| 16 | `enabled` defaults to false, must be a JSON boolean | 5.1, 9.1 | `cycle.py:228-230` | CONFIRMED |
| 17 | The real cycle stops `not_enabled` (exit 0) when not enabled and not dry-run; dry-run ignores `enabled` | 2.3, 4.1, 5.1 | `cycle.py:685-686` | CONFIRMED (see MINOR M6 on the words "before validation") |
| 18 | Launch argv has exactly 12 elements, agent `claude`, surface `terminal`, prompt `/sc:issue --claim <N> --pipeline none`, `--json` last | 5.1.3, 8.1 | `launch.py:84-116`; `launch.py:33` pattern `^/sc:issue --claim [1-9][0-9]{0,8} --pipeline none$` | CONFIRMED |
| 19 | Launch runs with `cwd=<worktree>` and a 120 s timeout | 5.1.3 | `launch.py:358-370`, `cycle.py:40, 1099` | CONFIRMED |
| 20 | Orca binary is `orca-ide` then `orca`, accepted only if `skills list --json` has topic `orca-cli`; relative paths skipped; nothing cached | 5.1.3 | `install_user_setup.py:36` (`_ORCA_CLIS = ("orca-ide","orca")`), `launch.py:144-203` | CONFIRMED |
| 21 | Origin must equal `ironbellyorg/ironclaude` lower-cased via `git -C <wt> remote get-url origin` | 5.1.3 | `launch.py:50, 233-251` | CONFIRMED |
| 22 | Constants: MAX_CANDIDATES 10, DAY_CAP 6, GH 20 s, probe 10, git 10, launch 120, deadline 240, floor 5, cutoff 120, SKEW_WARN 60, HEALTH 900, STALE 86400, DISCOVERY_WARN 80 | 11.1 | `cycle.py:34-47` | CONFIRMED |
| 23 | CALL_CAP 35, RESERVED_CALLS 3, PAGE_SIZE 100, PAGE_CAP 5, DISCOVERY_BOUND 100, RATE_LIMIT_MAX_WAIT 3600; shared G1/G2 never refused, so 37 max | 5.1.2, 11.1 | `github.py:40-49, 376, 437-463, 486` | CONFIRMED |
| 24 | MAX_ATTEMPTS 3, backoff 10 min, lease 60 min, day-cap window 24 h | 5.1.3, 11.1 | `record.py:434-443` | CONFIRMED |
| 25 | `SKEW_TOLERANCE_S = 300` is the claim-marker window; the clock-skew warning is 60 s | 14.1.2 KW-1 | `predicates.py:14-18, 274-296`; `cycle.py:44, 772-775` | CONFIRMED |
| 26 | Exit precedence 2, 6, 7, 5, 3, 4; 75 only as sole non-zero condition | 5.1.1, 10.1 | `cycle.py:461-478` | CONFIRMED |
| 27 | 59 reason words: 27 cycle + 17 skip + 9 entry + 1 note + 4 warning + 1 operator; exit mapping per word | 5.1.6, 10.2 | `audit.py:26-102` (counted word by word) | CONFIRMED |
| 28 | Exit 7 cannot combine with 5 or 3 through `_Cycle` (halt after the launch step); only 7 with 6 | 5.1.8 row 4, 10.1 | `_cond` callers only at `cycle.py:592, 1021, 1108, 1111`; halt `:833-834`; commit failure `:1126` | CONFIRMED |
| 29 | Five verbs; `status` has no platform check, the others do; `reset` rules; exit codes 0/1/2/6/75 | 5.1.4, 8.2 | `cli.py:84-91, 111-137, 164-182, 185-198, 201-214, 282-348`, `_EXIT_*` `:34-38` | CONFIRMED |
| 30 | `reset --rate-limit --forfeit-guarantee` silently ignores the second flag | 5.1.8 | `cli.py:309-313` | CONFIRMED |
| 31 | Config: eight top-level keys, unknown keys rejected, label rules, `project_id` regex, `owner_account_id` range, absolute paths, network-fs refusal | 9.1 | `cycle.py:58-76, 127-139, 195-283` | CONFIRMED |
| 32 | `dispatch.json`: 7 top-level keys, 17-field entries, 6 states, mode 0600, atomic write, flock lock with `O_NOFOLLOW` and inode re-check, `lexists` DISABLED | 5.1.3, 6 | `record.py:34-36, 68-131, 370-423`; `swarm/atomic.py:22-32` | CONFIRMED |
| 33 | Transitions T-1..T-13 (fail, mark_pending, launched/unknown/spawn_error, sweep, claimed, reset) | 5.1.3 | `record.py:503-720` | CONFIRMED |
| 34 | `init-state` creates dir 0700, lock 0600, store 0600; refuses an existing store | 5.1.4 | `record.py:753-802` | CONFIRMED |
| 35 | Gate order E1..E14 and launch-step order (probe, prompt, re-read, day cap, DISABLED, cut-off, origin, pending save, launch) | 4.1, 5.1.1.1-2 | `cycle.py:915-961, 979-1016, 1026-1112` | CONFIRMED |
| 36 | `status` is a local read only, healthy iff last stop-free exit-0 cycle <= 900 s, prints but never runs the retry argv | 5.1.4 | `cycle.py:1251-1335` (audit "accepted ... not read") | CONFIRMED |
| 37 | Approval rules (`User` actor, not `[bot]`, id in approvers, after trigger and store creation, later unlabel voids, same-second tie = events_incomplete) | 4.6, 5.1.5 | `predicates.py:185-234` | CONFIRMED |
| 38 | Marker window: own login, later of created/updated, at/after `pending_at` - 300 s else strictly after approval | 4.2 | `predicates.py:274-296` | CONFIRMED |

### 1C. Claim flow, launch levels and what each blocks

| # | Claim | Where | Code evidence path:line | Result |
|---|-------|-------|-------------------------|--------|
| 39 | Seven flags; STOP rules; `--submit` needs explicit `--pipeline full` (STOP `E-SUBMIT-NEEDS-FULL`; script exit 2) | 5.2, 8.2 | `issue.md:36-59`; `OW:1900-1901` | CONFIRMED |
| 40 | Default level is prose-only (bug `full`; simple/medium feature <=16 h `full`; complex or >16 h `worktree`; unreadable `worktree`); no code computes it | 5.2, 9.2, D-20 | `refs/claim.md:81`, `issue.md:43`; no `.py` holds the rule | CONFIRMED |
| 41 | `--pipeline none` ends after Wave 6; preflight still runs; no worktree, agent or `worktree.json` | 4.2, 5.2 | `refs/claim.md:17, 94`; `issue.md:80, 83` | CONFIRMED |
| 42 | `cmd_launch` order: record, already-launched, stale prompt, IR-4, `install_l2`, `l2_status`, IR-7, `publish_pending`, `orca agent launch`, shim check, `record_launch` | 4.3, 5.2 | `OW:1696-1834` | CONFIRMED |
| 43 | `IR7_REFUSE = False`; the refusal branch never runs | 2.3 row 12, 5.2 | `OW:822, 1757-1758` | CONFIRMED |
| 44 | IR-4 checks: jq, uv, guard commands, Linux interfaces, guard installed+executable+version line, `CLAUDE_CONFIG_DIR`, `disableAllHooks`, registrations, 23 governed tools | 5.2 | `OW:841-873, 955-1045` (GOVERNED_TOOLS counted: 14 names + 9 mcp = 23) | CONFIRMED |
| 45 | Governed launch prompt: `[sc-launch:v1:<nonce>] Read .dev/issues/<N>/launch-prompt.md and follow it.` | 4.3, 8.1 | `OW:1776-1779` | CONFIRMED |
| 46 | `pending` verb exists, writes one pending record, prints nonce, no production caller | 5.2, D-18 | `OW:1515-1523, 1886-1893`; callers grep: tests only (`test_launch_level_guard_worker.py:287`, `test_issue_orca_worktree.py:2472-2489`) | CONFIRMED |
| 47 | Shim detection: 5 tries x 2.0 s, screen text or tab-title regex; absence is a warning only | 5.2 | `OW:792-800, 1551-1583, 1802-1811` | CONFIRMED |
| 48 | Worker model pins: t3 `claude-gw-tier2b` (+`effort: low`), t2 `claude-gw-tier2`, t1 `claude-gw-tier1b`, line 6; 35 lines each | 5.2 | agent files `:1-8`; `wc -l` = 35 each | CONFIRMED |
| 49 | Guard grid: IMPL/TURN blocked at W only; COMMIT/PUSH/SUBMIT/SKILL blocked below FS; ten classes blocked at every level | 5.3, 4.6 | `GD:781-803` | CONFIRMED |
| 50 | Typed approval regex `^[[:space:]]*/(sc:implement|task)([[:space:]]|$)` at level W writes `sessions/<sid>.ok`; `/sc:task` is not accepted; template line 23 still names it | 5.3, D-23 | `GD:347-360`; `templates/launch-prompt.md:23`; `grep -c 'sc:task' GD` = 0 | CONFIRMED |
| 51 | Skill IMPL list is `implement|task|cleanup` (design lists six) | 5.3, KW-6 | `GD:409`; design `sc-issue-launch-level-hook.md:106,179,236,391` | CONFIRMED |
| 52 | Binding: marker `[sc-launch:v1:<32 hex>]`, `mv pending/<nonce> sessions/.take-<sid>`, hard link to `sessions/<sid>`, subagent prompts never bind, bad word = degraded = W + note | 4.3, 5.3 | `GD:264-272, 299-313, 314-385` | CONFIRMED |
| 53 | Fail-open for ordinary sessions, fail-closed for bound sessions; exit codes 0 and 2 only | 5.3, 10.4 | `GD:135-163, 208-238, 386-392`; header `:4-6` | CONFIRMED |
| 54 | 18 block words | 5.3 | `GD:36-133` (counted) | CONFIRMED |
| 55 | G2 rule 2: only `orca orchestration send|ask` as one plain call with no `--to`, `--run`, `--environment`, `--pairing-code`; max 8192 bytes and 64 args | 5.3 | `GD:485, 496-537` | CONFIRMED |
| 56 | The guard matches the command word `orca` only; `orca-ide` is not constrained | 5.3, D-25 | `GD:457` (`orca)` arm on the basename); `grep -c 'orca-ide' GD` = 0 | CONFIRMED by code reading (I did not repeat the "observed exit 0" run: I may create no file, so I did not execute the script) |
| 57 | Hook registrations: guard on UserPromptSubmit (63-71) and PreToolUse (115-124), identity on Bash PreToolUse (125-134), timeout 5, no `onFailure`; plugin hooks.json 154 lines; three scripts byte-identical | 5.3, 8.4 | `hooks.json` read whole; `cmp -s` identical x3; plugin file `wc -l` 154 | CONFIRMED |
| 58 | L2 hook: protected refs main/master only, `L2-PROTECTED`/`L2-UNKNOWN` exit 1, `L2-MALFORMED` exit 2, ordinary actor exits 0 at once, identity lookup under `env -i ... timeout 10` | 5.3 | `launch-level-pre-push.sh:9-10, 17, 65, 187-208` | CONFIRMED |
| 59 | Identity: rewrites only Bash, silent exit 0 above 1 MiB/unparseable/non-Bash, exit 2 on wrap failure, `identify` returns ordinary/released/governed/unknown(+reason); 32768-byte command limit | 5.3, 11.1 | `launch-job-identity.sh:20-24, 142, 197, 215-260, 430-505, 572-582` | CONFIRMED |
| 60 | `install_hooks` copies skip-if-exists unless force; `install` passes `force`, `update` passes `force=True`; the L2 template is copied but not registered | 5.3, 8.4 | `install_hooks.py:42-97, 280-289`; `main.py:219, 412`; `hook_adapter.py:230` | CONFIRMED |
| 61 | ccsession shim carries no launch level (zero hits for `launch-level|sc-launch|LAUNCH_LEVEL|launch_level` under `skills/ccsession-tag`); `ccsession-orca` sets `CCSESSION_ORIGIN`, unsets `CCSESSION_NAME`/`ASK_TIMEOUT` | 5.3, KW-8 | grep: zero hits; `ccsession-orca:249, 253-255` | CONFIRMED |
| 62 | WORKER-CONTRACT: 339 lines, WC-2..WC-16 (15 rules), no WC-1, no WC-17, no "Issue pipeline duties", "grant row" once at line 57 | 5.4, 2.3 row 7 | `wc -l` 339; presence count per rule number; grep | CONFIRMED |
| 63 | `CHANGELOG.md:17` records the removal of `issue-pipeline`, WC-17 and "Issue pipeline duties" | 2.3 row 8 | `CHANGELOG.md:15-17` | CONFIRMED |
| 64 | `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:268` says the duties were removed and no contract rule says who starts the worker | 5.4 | line 268 read | CONFIRMED |
| 65 | `test_launch_level_observations.py`: one test parametrized over 12 entries that `pytest.skip`s unconditionally | 2.3 row 13, 5.3 | `test_launch_level_observations.py:79-84`; 6 `def test_` | CONFIRMED (see MINOR M3 on the words "never run") |

## Part 2. Ledger re-verification (lens checklist item 2)

Every row of Section 2.3 was re-checked by reading the deciding code: the config default or constant, or an absent-caller search over `src`, `tests`, `plugins`, `scripts`, `.github`, Makefile, pyproject and package.json. Status word judged against the definitions in the document (BUILT-ON = code exists and is wired into a path that runs in a normal install; BUILT-OFF = a switch keeps it from running; NOT BUILT = no code in the snapshot; REMOVED = existed and was deleted).

| Ledger row | Status word in document | Deciding code I read | CONFIRMED / WRONG |
|------------|-------------------------|----------------------|-------------------|
| 1 Watcher, real cycle | BUILT-OFF (enabled:false) | `cycle.py:228` default `False`; `:685-686` stop `not_enabled`; `main.py:577-579` registers the group; no `issue-watch*.json` in the snapshot (grep of whole tree outside docs/tests/.git/.dev finds the word only in code, CHANGELOG and agent-work-report) | CONFIRMED |
| 1b Watcher verbs and `once --dry-run` | BUILT-ON | `cli.py:111-348`; `cycle.py:685` (dry-run skips gate), `:1029-1035` (stops before probe/launch) | CONFIRMED |
| 2 Claim | BUILT-ON | `commands/issue.md` exists and activates the skill (`:104-110`); skill, scripts, agents exist; no gating flag in `orca_worktree.py` `build_parser` (`:1857-1894`) | CONFIRMED |
| 3 L1 guard | BUILT-ON | `hooks.json:63-71, 115-124`; `install_hooks.py:93`; guard header `GD:4-6` | CONFIRMED |
| 4 L2 pre-push hook | BUILT-ON | `install_l2` called only from `cmd_launch` (`OW:1754`); hook script `launch-level-pre-push.sh`; not in `hooks.json` (grep) | CONFIRMED |
| 5 Job identity | BUILT-ON | `hooks.json:125-134`; `install_hooks.py:90`; `launch-job-identity.sh` | CONFIRMED |
| 6 G2 rule 2 | BUILT-ON | `GD:485, 496-537`; `WORKER-CONTRACT.md:66` | CONFIRMED |
| 7 Coordinator text, issue-pipeline duties | NOT BUILT | contract read: no "Issue pipeline duties", no WC-17, no watcher/adopt/COORD- text; only issue lines at 23, 57, 66, 242-243 | CONFIRMED |
| 7b Coordinator text, general rules | BUILT-ON (as instruction text) | WC-2..WC-16 present; no code loads the file (document tags this [UNVERIFIED], which is the honest status) | CONFIRMED |
| 8 Removed package `issue_pipeline` | REMOVED | `ls` of the directory at the snapshot: No such file; present at `01e7a9e23^` (10 files); `CHANGELOG.md:17`; commit message read with `git log` | CONFIRMED |
| 9 G2 rule 1 / route A (`release-worker`) | REMOVED | zero files in `src`, `tests`, `plugins` contain `release-worker`; `GD:496-497` retired comment; old TAMPER case read at `01e7a9e23^` guard lines 441-444 | CONFIRMED |
| 10 Caller of `orca_worktree.py pending` | NOT BUILT (caller); verb BUILT-ON | verb `OW:1515-1523, 1886-1893`; callers: tests only (grep) | CONFIRMED |
| 11 IR-3 `pipeline.json` | NOT BUILT | zero files in `src` and `plugins` contain `pipeline.json` | CONFIRMED |
| 12 IR-7 refusal | BUILT-OFF (constant, not the `enabled` key) | `OW:822` `IR7_REFUSE = False`, `:1757-1758`; the document says plainly it is a constant | CONFIRMED |
| 12b IR-4 preflight | BUILT-ON | `OW:955-1045`, call `:1730-1747`, no flag | CONFIRMED |
| 13 OB-H1..3, OB-CTX; ship gate | NOT BUILT | 12 parametrized cases always skip (`test_launch_level_observations.py:79-84`); gate is prose (`issue.md:16`, `claim.md:136`); `cmd_launch` reads no observation record | CONFIRMED (wording note M3) |
| 14 Scheduler for `issue-watch once` | NOT BUILT | no cron/timer/plist/systemd/workflow/automation artefact: `find` for `*.cron *.timer *.plist crontab*` empty; `.github/workflows` has only boundary-guard, contract3-generator-constraint-lint, test; grep of `.github`, `scripts`, Makefile, pyproject, plugins, `.claude` for `issue-watch`: no hit | CONFIRMED |
| 15 Dispatcher, `COORD-<RepoName>`, zero-setup install | NOT BUILT / "not found in snapshot" | `COORD-` zero hits outside `.git`/`.dev`; `dispatcher` hits in `src` are eval-suite text only | CONFIRMED |
| 16 Live-test record | NOT BUILT | `docs/designs/` listing has no `issue-watcher-live-test.md`; `test_github.py:573-598` asserts 19 `_assumed_shape` fixtures (`ls` = 19) | CONFIRMED |
| 17 Hand-off from a `--pipeline none` claim | NOT BUILT | prose at `issue.md:85`, `SKILL.md:140`, `claim.md:96`; the only `worker-start` hit in `.py`/`.sh` under `src` is a message string in `require-orca-worktree-agent.sh:356` | CONFIRMED |
| 18 Binding of coordinator-started workers | NOT BUILT (binding and caller); verb BUILT-ON | old `brief.py:60-74` built the marker; no old verb imports `brief` (old `cli.py:1-27` imports); contract template `:299-312` has no marker slot, `grep -c sc-launch` = 0 | CONFIRMED |

No row carries a status word that the code contradicts. The two rows that could be argued (row 7b BUILT-ON for instruction text; row 12 BUILT-OFF for a constant) are labelled in the document with the exact qualification.

## Part 3. Lens checklist items 3 to 8

### Item 3. Aspirational or designed-only features described as current

I read every claim in the document that is sourced from `docs/designs/`, `docs/architecture/` or `docs/reference/` and compared it with the code. Result: every design-sourced statement is either tagged [CODE-CONTRADICTED] / [STALE DOC] / [UNVERIFIED] or is confirmed by code. Specific checks that could have failed and did not:

- Design `issue-watcher.md` "max_launches_per_cycle = 1 as a default" (DES:380, 819): document says the constant is dead and the halt does the work. Code: `cycle.py:35` defined, grep over `src` and `tests` finds only that line (and one doc/design mention elsewhere). CONFIRMED.
- Design `issue-watcher.md:406` "audit.jsonl read by status and the SLO reducer": document says no reader. Code: `cycle.py:1279-1281`; `slo_numbers` has no production caller (grep). CONFIRMED.
- Design `issue-watcher-setup.md:170` cites WORKER-CONTRACT section 4 "Issue pipeline duties": the document calls it stale. Code: no such heading in `WORKER-CONTRACT.md` (grep of `src` finds the phrase nowhere; under `docs/` it appears only in the setup design, the architecture reference at line 268 and the rewrite design file; `CHANGELOG.md:15-17` records the removal). CONFIRMED.
- Design `sc-issue-launch-level-hook.md` IMPL list of six skills and "typed `approved` writes `.ok`" (rows 4 and 34): document says the code has three skills and accepts only `/sc:implement` or `/task`. Code `GD:347, 409`. CONFIRMED. Design `:189` really does say plain `approved` was removed (read).
- Design `sc-issue-claim-pipeline-flag.md:58` `pipeline.json`: document says NOT BUILT. Code: zero hits. CONFIRMED.
- "L2 costs about 100 ms per push" (design `:617-623`): document tags [UNVERIFIED] and does not use it as a fact. CONFIRMED as handled.
- FU-1 RECORDED lines a-k (`issue-pipeline-fu1.md:108-119`): document keeps them as [UNVERIFIED] text. I read them; they exist as stated.
- The document never describes the IR-7 refusal, the OB-H gate, the coordinator hand-off, a dispatcher, a scheduler or a live-test record as working. CONFIRMED by reading Sections 1, 2.1, 2.3, 4.4, 5.2, 5.4, 14.

### Item 4. The eight staleness warnings of BUILD-REQUEST.md in Section 14.1.2

| BUILD-REQUEST warning | Where in document | Is it represented correctly? | Evidence |
|-----------------------|-------------------|------------------------------|----------|
| 1 Clock skew 300 s vs 60 s | KW-1 (and 5.1.8 row 1, 11.1) | YES. The document refutes the hint with code: 300 s is `SKEW_TOLERANCE_S` (claim-marker window), 60 s is `SKEW_WARN_S` (warning). Design row `issue-watcher.md:827` "skew tolerance 300 s" and `:510` (marker window 300 s; warning 60 s) read: consistent with that reading. Tagged [CODE-VERIFIED] with "label ambiguous". | `predicates.py:17, 295`; `cycle.py:44, 774` |
| 2 MAX_LAUNCHES_PER_CYCLE dead | KW-2, D-01 | YES, [STALE DOC] plus DEFECT CANDIDATE row | `cycle.py:35`, grep; halt `:833-834` |
| 3 setup doc: missing contract section, `--pipeline none`, dispatcher, live-test file | KW-3 | YES. The document notes `SET:170` and `:575` do mention `--pipeline none` and that the capture sheet `SET:616-619` omits it (I read all three lines) | `issue-watcher-setup.md:170, 575, 616-620` |
| 4 fu1 uses `issue-pipeline plan-hash/check-approval` | KW-4, D-28 | YES | `issue-pipeline-fu1.md:64` |
| 5 guard-g2 line drift, route A retired, `pending` uncalled | KW-5, D-18, D-27 | YES | `issue-pipeline-guard-g2.md:13, 22, 45-51`; `GD:480-491, 496-497` |
| 6 launch-level-hook IMPL list and typed `approved` contradiction | KW-6 | YES | design `:106,123,189`; `GD:347, 409` |
| 7 sc-issue-command "Design only", T3 pin, level table default | KW-7 | YES | `sc-issue-command.md:3, 58`; `issue-worker-t3.md:6`; `claim.md:81` |
| 8 ccsession shim does not carry the level | KW-8 | YES | zero grep hits under `skills/ccsession-tag` |

### Item 5. Unwired, switched-off, retired or caller-less capabilities in Section 14.2

Absent-caller searches I re-ran (all over the snapshot, `src` and `tests` unless stated):

| # | Search | Result | Matches document |
|---|--------|--------|------------------|
| 1 | `MAX_LAUNCHES_PER_CYCLE` | only `cycle.py:35` in `src`; no test | D-01 |
| 2 | `slo_numbers` / `SloNumbers` | defined `cycle.py:1339, 1359, 1401`; used only in `test_slo_helper.py` | D-03 |
| 3 | `disabled_present` | defined `record.py:748`; used only in `test_record.py:861, 864, 870` | D-09 |
| 4 | `.detail` of `LaunchOutcome` | only validation inside `launch.py:269`; no reader | D-10 |
| 5 | `launch_login` / `launch_account_id` | written `cycle.py:1087-1088`, `record.py:197-198, 479-480, 550-553`; no consumer | D-11 |
| 6 | `retry_argv` | one caller, `cycle.py:1310`, which only prints | D-12 |
| 7 | `orca_worktree.py pending` | defined `OW:1515, 1893`; callers are tests | D-18, ledger row 10 |
| 8 | `pipeline.json` | zero hits in `src`, `plugins` | D-22 |
| 9 | `release-worker` | zero hits in `src`, `tests`, `plugins` | D-27 |
| 10 | `COORD-`, `dispatcher` for the pipeline | zero / unrelated hits | D-16 |
| 11 | `worker-start`, `task-create` in `.py`/`.sh` under `src` | one hit: a message string `require-orca-worktree-agent.sh:356`, not a call | D-16 |
| 12 | scheduler artefacts for `issue-watch` | none (see ledger row 14) | D-04 |
| 13 | symbol scan: every top-level function, class and constant of the nine watcher modules and the three claim scripts that occurs once in `src` | only `MAX_LAUNCHES_PER_CYCLE`, `slo_numbers`, `disabled_present` (plus Click command functions used by decorators) | complete; no dead symbol is missing from Section 14.2 |

Section 14.2 states that no remediation tasks were created and why. Rows are classed DEFECT CANDIDATE / NOT BUILT / BUILT-OFF / REMOVED with a declaring doc line. Rows D-04, D-05, D-06, D-12, D-13, D-14, D-15, D-19, D-22, D-27 cite a decision file; all other rows say "No decision found" and are not relabelled "known gap" or "future phase". A search of the document for `known gap`, `future phase`, `roadmap`, `TODO` finds no relabelling. Decision citations I opened: `DES:33`, `DES:856-871`, `SET:288`, `SET:669-686`, `OW:818-822`, `CHANGELOG.md:15-17`, `pipeline-flag.md:58`. All say what the document says they say.

### Item 6. Appendix B facts against the old tree (spot-check of 15 required; 22 done)

All read with `git -C /home/coder/workspaces/IronClaude show 01e7a9e23^:<path>` or `git ls-tree` / `git log` / `git show --stat`.

| # | Appendix B fact | Old-tree evidence | Result |
|---|-----------------|-------------------|--------|
| 1 | Package has 10 files | `git ls-tree -r --name-only 01e7a9e23^ -- src/superclaude/cli/issue_pipeline/` lists 10 paths | CONFIRMED |
| 2 | 1,597 lines in total (5/62/416/74/395/90/161/66/301/27) | `wc -l` of each blob: exact match; sum 1597 | CONFIRMED |
| 3 | Commit time 2026-11-19 18:02 -0600, PR #682, message "Nothing ran this code ... enabled: false and never ran live" | `git log -1`: 2026-11-19 18:02:35 -0600, subject ends `(#682)`, message text as quoted | CONFIRMED |
| 4 | `main.py` old lines 581 and 583 are the import and `add_command(... name="issue-pipeline")` | `sed -n 579,584p` of the old file | CONFIRMED |
| 5 | Group `click.group(name="issue-pipeline")` at `cli.py:56-58`; exit codes `_EXIT_REFUSED=1`, `_EXIT_CONFIG=2`, `_EXIT_LOCK_HELD=75` at `:29-32` | old `cli.py:28-33, 56-58` | CONFIRMED |
| 6 | Ten verbs at lines 61, 76, 96, 108, 117, 134, 161, 179, 200, 335 | `grep -n` of `command(` in old `cli.py` | CONFIRMED |
| 7 | `release.py:57-62` creates `<store>/sessions/<sid>.ok` with `O_WRONLY|O_CREAT|O_EXCL|O_NOFOLLOW`, mode 0600 | old `release.py:55-63` | CONFIRMED |
| 8 | Accepted approval texts `approved` and `approved ap-<issue>-plan-<12 hex> plan-sha256=<64 hex>` (`approval_line.py:18-21, 33-40`) and check words ok/bare/mismatch/malformed | old `approval_line.py:15-62` | CONFIRMED |
| 9 | Plan hash has 11 refusal words (`plan_hash.py:24-36`) | old `plan_hash.py:22-37` lists 11 | CONFIRMED |
| 10 | Plan reply marker `<!-- sc:stage:plan id=<record id> plan=<64 hex> -->` (`reads.py:42`) | old `reads.py:40-44` | CONFIRMED |
| 11 | Old WORKER-CONTRACT was 350 lines; WC-17 at old `:59`; "### Issue pipeline duties" at old `:291-300`; six duties; "grant row" at old `:57` and `:300` | old file: 350 lines; grep lines 57, 59, 291, 300; text read | CONFIRMED |
| 12 | WC-17 steps (1)-(6) with `plan-hash`, `ask`, wait, `check-approval`, `ack`, continue only on `applied`; bare `approved` never approval | old contract line 59 read | CONFIRMED |
| 13 | Old guard was 811 lines; G2.1 TAMPER case words `release-worker`, `release_worker`, `issue-pipeline*adopt-`, `issue-pipeline*record-`, `issue_pipeline*release*`, `issue_pipeline*approval_record*` at `:441-444` | old guard `wc -l` 811; lines 438-448 read | CONFIRMED |
| 14 | The old contract never named `release-worker` or `.ok` | `grep -c 'release-worker\|\.ok'` on the old contract = 0 | CONFIRMED |
| 15 | `brief.build` was not called by any verb | old `cli.py` imports (`approval_line, approval_record, plan_hash, reads, release, stage_predicates`) do not include `brief`; grep for `brief` imports in old `src`: none | CONFIRMED |
| 16 | 116 tests in 10 files (2,391 lines) plus `test_issue_pipeline_registered.py` (15 lines, 1 test) | per-file `wc -l` and `grep -c 'def test_'` at `01e7a9e23^`: 116 and 2391; registered test 15 lines | CONFIRMED |
| 17 | Per-file test counts in B.8 (2/3/9/21/12/10/10/7/29/13) | same loop | CONFIRMED |
| 18 | Commit also changed CHANGELOG (+4), architecture doc (1 line), cli-groups (10), main.py (-4), contract (13), guard + plugin copy (7 each), tests | `git show --stat --format= 01e7a9e23` | CONFIRMED |
| 19 | `stage-status` calls no `orca`; pinned by `test_the_command_only_reads_and_never_calls_orca` at old `test_stage_status.py:451` | line 451 read (def at 451) | CONFIRMED |
| 20 | Old verbs' `adopt-create` / `adopt-mark` options (`--stage`, `--state started|uncertain`, `--dispatch-id`) | old `cli.py:108-131` | CONFIRMED |
| 21 | `release-worker` has `--store` option defaulting to `~/.claude/state/launch-level` | old `cli.py:200-217` | CONFIRMED |
| 22 | Old gh lines were reads (`gh api user --include`, `--method GET ...`, GraphQL) | old `cli.py` imports `issue_watch.github` argv builders; no write verb | CONFIRMED (structure of imports) |

### Item 7. Runtime-state claims

I searched the document for wording that states runtime state as fact (`never run`, `has not been run`, `only a person`, `no schedule is installed`, `in production`, `real config`). The document is disciplined: "never run live", PRs #447/#448, the real `enabled` value, whether anything runs `once` on a schedule, the FU-1 recorded lines and the L2 timing are all tagged [UNVERIFIED] and listed in 14.3.1. I found three places where a runtime-flavoured sentence is not tightened to "in the snapshot"; I grade them MINOR (M1, M2, M3 below) because each is either attributed to a source or sits beside an [UNVERIFIED] statement of the same fact. No PR number, live run, scheduler presence or config value is asserted as fact without a source or a tag.

### Item 8. PR 686 and the rewrite design

`grep -i -E '686|rewrite|orchestrator\.md|orchestrator-mode|unify'` over the document: one sentence at line 218 ("PR 686 and the rewrite design are out of scope for this reference."). The other hits are the number 686 inside line ranges (`cycle.py:685-686`, `record.py:654-686`) and the word "rewrites" about the identity hook. The snapshot contains `docs/designs/orchestrator.md` (the rewrite design) and the document does not describe it. The one place the document touches that design indirectly is the quote of `SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:268`, where the document replaced "the orchestrator design replaces them" by "[its replacement]" so no description leaks. CONFIRMED.

## Part 4. Findings

Severity rule applied: BLOCKING = a behavioural claim that does not match the code, a wrong status word, an aspirational feature described as current, a defect or NOT BUILT capability missing from Section 14.2 or relabelled without a cited decision, a runtime-state claim stated as fact. MINOR = wording, formatting, citation, moved line number on a true claim.

BLOCKING findings: none.

MINOR findings (notes; they do not fail the review). Line numbers below are lines of the document under review.

| ID | Severity | Location | Issue | Evidence | Required fix |
|----|----------|----------|-------|----------|--------------|
| M1 | MINOR | document line 185 (Section 1) | "As built, the watcher ships switched off and nothing in the snapshot schedules it, so only a person typing a command starts any part of the pipeline." The premise is about the snapshot; the conclusion is about who starts the pipeline in the world. The document itself says at lines 220 and 674 that whether anything outside the snapshot runs `once` on a schedule is [UNVERIFIED], and lines 231-232 and 562 name "a person or an external scheduler". | `cycle.py:228` (default false) and the absent-artefact searches support only "no scheduler artefact ships". | Reword to "so, in the snapshot, only a person's command starts any part of the pipeline". |
| M2 | MINOR | line 1978 (14.3.1 U-1) | "`enabled` ships false and no schedule is installed ARE [CODE-VERIFIED]". Code can verify that the default is false and that no scheduler artefact ships; whether a schedule is installed on a machine is runtime state. | `cycle.py:228`; ledger row 14 searches (no artefact). | Reword to "no scheduler artefact ships in the snapshot". |
| M3 | MINOR | lines 1297, 1981, 2123, 2178 (and 2.3 row 13 at line 338) | "never run" for the OB-H1..3 / OB-CTX observations is stated as a plain fact at 2123 and 2178 ("the live observations were never run"), while row 13 says whether the observations passed is [UNVERIFIED]. The only sources are the skip text ("has not been run") and the design line "Pending, none run". | `test_launch_level_observations.py:79-84`; `sc-issue-launch-level-hook.md:625`. | Write "recorded as not run (skip message; design 'Pending, none run')" at 2123 and 2178 so the glossary and Appendix A match row 13. |
| M4 | MINOR | line 1293 (5.3 ledger of guard items) | The label "FU-1" is used for two different things. In 5.3 `FU-1 (first live-test runbook for the claim hand-off)` has status REMOVED; in 14.1.1, 14.2.1 D-05 and 14.3 "FU-1" is the owner-run watcher live test, NOT BUILT. The runbook file `docs/designs/issue-pipeline-fu1.md` is still present (119 lines); only its commands are gone (D-28 says so correctly: "REMOVED (the commands)"). | `docs/designs/issue-pipeline-fu1.md:3, 64`; `issue-watcher.md:33, 860`. | In 5.3 call the row "issue-pipeline-fu1.md runbook" with status "STALE DOC (file present; its commands REMOVED)". |
| M5 | MINOR | line 1439 (8.1 "L2 install probes") | The probe list names three git commands but omits `git -C <wt> rev-parse --path-format=absolute --git-common-dir`, which `_l2_preconditions` also runs. The same row's "git rev-parse --git-path hooks" is shown without the `-C <wt>` prefix the code uses. | `OW:1345, 1356-1362` | Add the fourth probe and the `-C <wt>` prefix. |
| M6 | MINOR | line 667 (5.1 fact table) and the `not_enabled` wording at 700 | "the real cycle stops `not_enabled` (exit 0) before validation, lock and any external call". The CLI loads and validates the configuration file (`load_config`) before the cycle starts, so a malformed config exits 2 `config_invalid` even when `enabled` is false; only the setup validation (worktree directory, approvers file) is skipped. | `cli.py:84-91, 120`; `cycle.py:195-283, 685-693`. | Say "before the setup validation (worktree, approvers file), the lock and any external call". |
| M7 | MINOR | Section 14 (rows D-16, 14.1.2) | The live command and skill text that the document marks NOT BUILT (hand-off, `issue.md:85`, `claim.md:96`, `SKILL.md:140`) also tells the coordinator to look for "its adoption row still `reserved`" and to settle it as `started`. That adoption row belonged to the removed package (Appendix B.3, B.9). The document lists the removal but does not say that this live prose still names the removed row. | `issue.md:85`; `claim.md:96`; `SKILL.md:140`; old `approval_record.py` rows at `01e7a9e23^`. | Add one sentence to D-16 or to 14.1.2: "the hand-off prose also refers to an adoption row that no longer exists (removed with `issue-pipeline`)". |

M1 to M7 are seven MINOR notes in total.

## Checks performed (counts)

| Lens checklist item | Done | Count |
|---------------------|------|-------|
| 1. Behavioural claims verified against the snapshot (focus: watcher writes to GitHub, `enabled` default, launch command, claim writes and actors, launch levels and what each blocks, fail-closed vs fail-open, exit codes, hooks.json registrations, what `orca_worktree.py` does) | yes | 65 numbered claims in Part 1 (each with path:line), each covering several sub-facts; 100+ individual facts counted. Zero WRONG |
| 2. Ledger re-verification (rows 1, 1b, 2, 3, 4, 5, 6, 7, 7b, 8, 9, 10, 11, 12, 12b, 13, 14, 15, 16, 17, 18) | yes | 21 rows (the document has rows 1-18 plus 1b, 7b and 12b); 21 CONFIRMED, 0 WRONG |
| 3. Aspirational or designed-only content described as current | yes | 8 design-sourced claim groups traced to code; 0 defects |
| 4. Eight staleness warnings in 14.1.2 | yes | 8 of 8 represented correctly (KW-1..KW-8) |
| 5. Unwired / switched-off / retired / caller-less capabilities in 14.2 and absent-caller re-runs | yes | 13 searches (11 absent-caller greps, scheduler artefact search, whole-module dead-symbol scan); minimum of 5 required; 0 missing rows |
| 6. Appendix B facts against the old tree | yes | 22 facts checked via read-only git; minimum of 15 required; 0 wrong |
| 7. Runtime state stated as fact | yes | wording scan plus reading of all [UNVERIFIED] rows; 0 BLOCKING, 3 MINOR (M1, M2, M3) |
| 8. PR 686 / rewrite design | yes | one sentence at line 218; no other description |
| Extra: test counts and line counts in Appendix A and Section 1 | yes | all 20 watcher test files (19 tests + conftest: 19,801 lines, 867 tests) and 26 other test files re-counted with `wc -l` and `grep -c 'def test_'`; every figure matched |

Tool engagement (approximate): Read 49 | Grep 10 (2 of them failed with EACCES on `rg` and were repeated with another pattern or with Bash `grep`) | Glob 0 | Bash about 40 (read-only `grep`, `sed -n`, `wc`, `ls`, `cmp`, `git show`, `git log`, `git ls-tree`). Read+Grep+Glob (59) is at least the 8 lens items. No Bash command wrote anything; one Bash call that contained a bare `python3` was blocked by the hook and had no effect (it was a no-op probe, not part of any check).

Confidence: Verified: 8/8 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%.
Limit that is not a checklist item: the document's "observed exit 0" results for the `orca-ide` gap (D-25) and the "44 sample payloads" guard run come from an execution in the research phase. I did not repeat that execution because the task forbids creating files (the guard needs a store directory). I verified the same conclusion by reading the guard code (`GD:457` arm `orca)` on the word basename; zero `orca-ide` in the script). The identity hook, L2 hook, installers and claim scripts were read, not executed, by me as by the document; tests were read, not run.

## Self-Audit

(a) Reliance list: this lens has no inherited structural verdict in my prompt, so there is no rf-qa PASS item I relied on. I did not rely on any research file or synthesis file either; every code claim was re-read in the snapshot.

(b) Independent semantic checks (zero would be an INV-019 violation; there are many):
- "The watcher writes nothing to GitHub": verified by grep over all of `issue_watch/` for every non-read `gh` verb and method string, not by reading the document's evidence list.
- Ledger status words: verified by reading the config default, the constant, and re-running absent-caller greps and a whole-module dead-symbol scan.
- Appendix B: 22 facts re-read with `git show` at `01e7a9e23^`, including line counts of all ten files and all ten test files.
- Staleness warnings: re-read the design lines the document cites (DES:3, 33, 75, 103, 173, 331, 360, 406, 485, 510, 621, 640, 722, 752, 827, 856-871; SET:5, 170, 198, 270-290, 575, 586-626, 669-686; guard-g2, fu1, command and flag designs).
- Test counts: `wc -l` and `grep -c 'def test_'` over 46 test files.

Questions I asked of myself before writing the verdict:
1. How many factual claims did you verify independently? 65 numbered claims in Part 1 plus 21 ledger rows, 13 absent-caller searches, 22 removed-code facts, 8 staleness warnings, 46 test files counted.
2. Which files did you read? In the snapshot: `issue_watch/{cycle,github,record,launch,predicates,audit,cli,runner}.py`, `orca_worktree.py`, `clickup_claim.py`, `origin_repo.py`, `commands/issue.md`, `SKILL.md`, `refs/{claim,tiers}.md`, templates, three agent files, `hooks.json` (and the plugin copy by grep and `cmp`), `launch-level-guard.sh`, `launch-job-identity.sh`, `launch-level-pre-push.sh`, `install_hooks.py`, `main.py`, `ccsession-orca`, `WORKER-CONTRACT.md`, `CHANGELOG.md`, design and architecture docs named above, and 46 test files by count or by line. In git: 30 blobs at `01e7a9e23^` plus the commit stat.
3. Why trust a result with zero BLOCKING? Because the document was attacked at the places where such documents usually fail (dead constants, default values, exit codes, absent callers, removed code, design-vs-code drift, status words) and each was re-derived from code. Seven MINOR wording issues were found, which shows the search was not a rubber stamp.
4. Web research: none performed (the task forbids sending repository details to external services). Tavily was not used and no fallback tool was used.

## Verdict: PASS

BLOCKING findings: 0. MINOR notes: 7 (M1 to M7, wording and completeness; none changes a status word, a constant, a default, an exit code or a behavioural statement).

Status: Complete



