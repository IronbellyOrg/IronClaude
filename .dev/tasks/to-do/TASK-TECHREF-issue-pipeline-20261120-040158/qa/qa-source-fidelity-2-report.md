# QA Report - Source Fidelity (Detail-Preservation Lens)

**Topic:** IronClaude issue-to-work pipeline technical reference
**QA phase:** source-fidelity
**Lens:** detail-preservation
**Partition:** source-fidelity-2
**Date:** 2026-11-20
**Status:** Complete (see the final Status line and `## Verdict` at the end)

Document: /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/techref/ISSUE-TO-WORK-PIPELINE-TECHNICAL-REFERENCE.md (2436 lines)
Source root: /home/coder/.cache/ic-snap-20261120/master (read-only)

(Sections appended incrementally below.)

## Detail-comparison table (continuous numbering)

Legend: `@R` = `git -C /home/coder/workspaces/IronClaude show 01e7a9e23^:<path>`; `snap` = /home/coder/.cache/ic-snap-20261120/master. Document locations are line numbers in the document.

### Part 1 - Appendix B (removed code), read via git show

| # | Document claim | Doc loc | Source value | Result |
|---|---|---|---|---|
| 1 | removed dir: 10 files, 1,597 lines | :2285 | @R wc: 5+62+416+74+395+90+161+66+301+27 = 1597 | MATCH |
| 2 | per-file lines 5/62/416/74/395/90/161/66/301/27 | B.1 table | same wc output | MATCH |
| 3 | commit 01e7a9e23, PR #682, 2026-11-19 18:02 -0600 = 2026-11-20 00:02 UTC | :2281 | `git show -s`: 2026-11-19 18:02:35 -0600, subject (#682) | MATCH |
| 4 | commit message quote "Nothing ran this code: ... issue_watch is unchanged." | :2281 | commit body verbatim | MATCH |
| 5 | CHANGELOG +4, architecture ref 1 line, cli-groups 10 lines, main.py -4 (old :581 import, :583 add_command) | :2300 | numstat 4/0, 1/1, 4/6, 0/4; hunk positions 581 and 583 | MATCH |
| 6 | WORKER-CONTRACT +1/-12, 350 to 339 lines | :2300 | numstat 1/12; @R 350; snap 339 | MATCH |
| 7 | guard and plugin copy: 5 removed, 2 added each | :2300 | guard diff -5 +2 | MATCH |
| 8 | group `issue-pipeline` at cli.py:56-58; exit consts :29-32 (1, 2, 75) | B.2 | @R cli.py:29-32, 56-58 | MATCH |
| 9 | "No verb printed file or GitHub text" | B.2 | @R cli.py:3-4 | MATCH |
| 10 | `plan-hash` :61, `REPORT_DIR NAMES...`, output `file: <name>`..`plan-sha256: <hex>`, `refused:<reason>` exit 1 | row 1 | @R cli.py:61-73 | MATCH |
| 11 | `check-approval` :76, `--line` required, `--issue N`, `ok` exit 0 or word exit 1 | row 2 | @R cli.py:76-93 | MATCH |
| 12 | `init` :96, `ok`, `refused:<reason>` exit 1, 0700/0600 | row 3 | @R cli.py:96-105; approval_record.py:81-98 | MATCH |
| 13 | `adopt-create` :108, `--stage` default `plan`, JSON `created`, `refused:already-started`/`uncertain-launch` exit 1, `lock-held, retry` exit 75 | row 4 | @R cli.py:35-45, 108-114; approval_record.py:235-265 | MATCH |
| 14 | `adopt-mark` :117, `--state started|uncertain`, `--dispatch-id`, JSON `marked` | row 5 | @R cli.py:117-131; approval_record.py:298 | MATCH |
| 15 | `record-create` :134, `--plan-hash`, `--channel label|comment|reply`, `--evidence-id`, `--actor`, JSON `created`/`exists` | row 6 | @R cli.py:134-158; approval_record.py:43, 359-371 | MATCH |
| 16 | `record-show` :161 | row 7 | @R cli.py:161-176 | MATCH |
| 17 | `record-mark` :179, `--state instructed|acked|revoked` | row 8 | @R cli.py:179-197; approval_record.py:45 | MATCH |
| 18 | `release-worker` :200, `SESSION_ID`, `--store` default `~/.claude/state/launch-level`, `released`/`already-released` | row 9 | @R cli.py:200-214; release.py:30-31 | MATCH |
| 19 | `stage-status` :335, ISSUE, `--json`, `--config` (default `~/.config/superclaude/issue-watch.json`), `--approvals-dir`, `--plan-dir`, `--plan-file`; config error exit 2; read failure exit 1 | row 10 | @R cli.py:335-395 | MATCH |
| 20 | accepted texts `approved` (comment channel only) / long form; whole-text, no trim (approval_line.py:18-21, 33-40) | B.3 | @R approval_line.py:18-21, 33-40, 51 | MATCH |
| 21 | check results `ok`, `refused:bare`, `:mismatch`, `:malformed`, `refused:<plan-hash reason>` (:43-62) | B.3 | @R approval_line.py:23-26, 43-62 | MATCH |
| 22 | plan hash framing: sorted names, 8-byte big-endian length + name + 8-byte length + bytes | B.3 | @R plan_hash.py:84-89 | MATCH |
| 23 | 11 refusal words (plan_hash.py:24-36) | B.3 | @R plan_hash.py:24-36 same order | MATCH |
| 24 | store: caller-named dir, 0700, lock 0600, symlink refused (:81-98) | B.3 | @R approval_record.py:81-98 | MATCH |
| 25 | adoption row name, keys, states (:126-139, :44) | B.3 | @R approval_record.py:44, 126-139 | MATCH |
| 26 | approval row name, keys, states, evidence keys (:132-153) | B.3 | @R approval_record.py:45, 132-153 | MATCH |
| 27 | writes: `write_prepared_bytes`, chmod 0600, dir fsync, flock, exit 75 (:108-123, :225-229) | B.3 | @R approval_record.py:108-123, 225-229 | MATCH |
| 28 | plan reply marker `<!-- sc:stage:plan id=.. plan=.. -->` (reads.py:42) | B.3 | @R reads.py:42 | MATCH |
| 29 | release: zero-length `.ok`, `O_WRONLY|O_CREAT|O_EXCL|O_NOFOLLOW`, 0600 (release.py:57-62) | B.4 | @R release.py:57-62 | MATCH |
| 30 | refusals `bad-session-id`, `no-store`, `not-bound`, `not-worktree-level`; second call `already-released` | B.4 | @R release.py:45-64 | MATCH |
| 31 | guard read `.ok`: W+`.ok` = WA; IMPL and TURN allowed (snapshot GUARD:270-272, :786) | B.4 | snap guard :270-272, :786 | MATCH |
| 32 | release.py:3-4 docstring: coordinator calls it after recording approval | B.4 | @R release.py:3-4 | MATCH |
| 33 | package `gh` lines were reads; builders `P/github.py:175-262` used by reads.py | B.4 | @R reads.py:24-36, 142-148; cli.py:276-282 | MATCH |
| 34 | `test_the_command_only_reads_and_never_calls_orca` at test_stage_status.py:451 | B.4 | @R :451 | MATCH |
| 35 | contract text quotes (old WCT:298 plan reply / mirror label and Status; :300 grant row) | B.4 | @R WORKER-CONTRACT.md:298, 300 | MATCH |
| 36 | WC-17 at old :59 in section 3; steps 1-6; bare `approved` never approval; mismatch reported in `worker_done` | B.5 | @R WORKER-CONTRACT.md:59 | MATCH |
| 37 | "Issue pipeline duties" old :291-300, 6 rows at :295-300 with the stated contents | B.5 | @R :291-300 | MATCH |
| 38 | duties name adopt-create, adopt-mark, stage-status, record-create, record-mark (WC-17: plan-hash, check-approval), never release-worker or brief | B.5 | @R grep release-worker = 0 | MATCH |
| 39 | `COORD-` 0 hits in old contract; "grant row" at old :57 and :300 only | B.5 | @R grep counts and line list | MATCH |
| 40 | old guard 811 lines; TAMPER comment :441-444, case :444, normalised text :428 | B.6 | @R guard | MATCH |
| 41 | TAMPER patterns (`release-worker`, `release_worker`, `issue-pipeline`..`adopt-`/`record-`, `issue_pipeline`..`release`/`approval_record`) | B.6 | @R guard :444 | MATCH |
| 42 | `plan-hash`, `check-approval` stayed allowed | B.6 | @R guard :441-443 | MATCH |
| 43 | after removal: G2 rule 2 remains; store TAMPER GUARD:761; one comment left at GUARD:496 | B.6 | snap guard :496-497, :761 | MATCH |
| 44 | removed tests: 10 files, 2,391 lines, 116 tests; per-file lines and counts (78/2, 88/3, 135/9, 424/21, 224/12, 116/10, 295/10, 89/7, 466/29, 476/13) | B.8 | @R wc and `grep -c def test_` | MATCH |
| 45 | `test_issue_pipeline_registered.py` 15 lines, 1 test | B.8 | @R | MATCH |
| 46 | test_worker_contract.py 3,181/61 before, 3,135/59 after (+8/-54); 3 dropped, 1 added, RULE_PHRASES keys removed | B.8 | @R/@C counts; git diff names | MATCH |
| 47 | test_launch_level_guard_worker.py 330/13 before, 300/11 after, -30 net | B.8 | @R/@C counts; numstat 13/43 | MATCH |
| 48 | dropped tests old :270-287 (6 commands) and :290-299; chain test types `/sc:implement plan.md` (current :255-257) replacing `release.release` (old :254) | B.8 | @R :254, 270-299; @C :255-257 | MATCH |
| 49 | fixtures: issue 452 responses, no label event, plan reply or approval comment | B.8 | @R fixtures/recorded/README.md | MATCH |
| 50 | `brief.build` not called by any verb; brief.py:71-73 builds marker | B.7, 2.3 row 18 | @R cli.py imports; brief.py:71-73 | MATCH |
| 51 | safety cites stage_predicates.py:145-244, :171-177; reads.py:138-139; approval_record.py:235-265, :389-416; brief.py:5-8; plan_hash.py:39-90 | B.7 | @R each range | MATCH |

(Part 1: 51 items, 0 mismatches. Further parts appended below.)

### Part 2 - Guard stack (snap `src/superclaude/hooks/...`)

| # | Document claim | Doc loc | Source value | Result |
|---|---|---|---|---|
| 52 | guard 808 lines, version line GD:10 `# launch-level-guard-version: 1`; identity 582; pre-push 208; hooks.json 192 (plugin 154); install_hooks.py 614; install_ccsession.py 161; ccsession-orca 263 | 1 stats, 3.1, 5.3 | `wc -l` snap: 808/582/208/192/154/614/161/263; guard :10 | MATCH |
| 53 | L1 exits only 0 or 2, never 1; header :4-6 | 5.3, 1 | guard :4-6; `ll_on_exit` :147-162 | MATCH |
| 54 | 18 block words LL-IMPL..LL-BROKEN, `ll_say` GD:36-133 | 5.3 | guard :41-114 (17 ids + default `*` = LL-BROKEN) | MATCH |
| 55 | level matrix W/WA/F/FS x IMPL/COMMIT/PUSH/SUBMIT (16 cells): IMPL blocked only at W; COMMIT, PUSH, SUBMIT blocked at W, WA, F and allowed at FS | 5.3 matrix | guard :786-790 (`IMPL:WA|F|FS` allow; `SUBMIT/COMMIT/PUSH:FS` allow; the rest deny) | MATCH |
| 56 | TURN blocks at W only; SKILL blocks W/WA/F, allows FS (GD:786-790) | 5.3 | guard :786-790 | MATCH |
| 57 | REPO, PUSHFORM, PROTECTED, MERGE, GHWRITE, UNKNOWN, MCP, ESCAPE, TAMPER, BIG block at every level incl. FS (GD:791-800); no match/empty level = `LL-BROKEN` (:801) | 5.3 | guard :791-801 | MATCH |
| 58 | block precedence BIG TAMPER MERGE GHWRITE PROTECTED ESCAPE MCP UNKNOWN SUBMIT REPO PUSH PUSHFORM COMMIT TURN IMPL SKILL (GD:783) | 5.3 | guard :783 loop list | MATCH |
| 59 | typed approval regex `^[[:space:]]*/(sc:implement|task)([[:space:]]|$)` at W only writes `sessions/<sid>.ok`; no-clobber; `.ok` makes WA (GD:347-360, 270-272) | 4.3, 4.6, 5.3 | guard :347-360, :270-272 | MATCH |
| 60 | `/sc:task` not accepted by approval regex; Skill classifier treats `sc:task` as IMPL | 5.3 | guard :347; :405-409 (`task` after normalisation) | MATCH |
| 61 | marker regex `\[sc-launch:v1:([0-9a-f]{32})\]` (:318); subagent prompt exit 0 (:315); `mv pending/<nonce> sessions/.take-<sid>` (:372-375); hard link first binding wins (:299-313); bad word becomes `degraded` read as W + LL-STATE note (:264-269, :306) | 4.3, 5.3 | guard :315, 318, 299-313, 372-376, 264-269 | MATCH |
| 62 | `LL-NOBIND` conditions (empty sid, unowned or symlinked `sessions/`, no regular session file) GD:366-384; empty-store fast exit :168-173; level word read as 13 bytes | 5.3 | guard :366-384, :168-173, :262 | MATCH |
| 63 | classifier IMPL = `implement`, `task`, `cleanup` (GD:409); `pr-submit` SUBMIT; `issue` ESCAPE; unreadable SKILL | 5.3 | guard :408-413 | MATCH |
| 64 | Bash over 65536 bytes is BIG | 5.3 | guard :419 | MATCH |
| 65 | G2 rule 2: allow-list `status`, `help`, `--version`, `worktree current|list|show`, `terminal list|show|read`, `orchestration check|inbox|run-current|task-list|worker-show`; glob turns read verbs into ESCAPE; short help call (last word `--help`/`-h`, at most 4 words from `orca`, no glob) allowed (GD:480-491) | 2.4 #6, 5.3 | guard :480-491 | MATCH |
| 66 | G2 rule 2 limits: raw command at most 8192 bytes, 64 arguments, no newline; `--to*`, `--run*`, `--environment*`, `--pairing-code*`, prefixes of `--to`/`--run`, bare word, lone `--` = ESCAPE (GD:496-537, `LL_SA` :485) | 5.3 | guard :485, :501-537 | MATCH |
| 67 | guard matches basename `orca` only (GD:457), so `orca-ide` is not constrained | 5.3 | guard :457 `orca)` case; no `orca-ide` token in script | MATCH |
| 68 | git classes: merge/pull MERGE; push family PUSH; commit/cherry-pick/am/commit-tree/revert COMMIT; update-ref on HEAD/--stdin/refs/heads COMMIT; canonical push regex only `git push [-u|--set-upstream] origin <branch>[:<dst>]`; dst master/main PROTECTED, HEAD PUSHFORM (GD:580-725, regex :716) | 5.3 | guard :580-725 | MATCH |
| 69 | gh classes: `gh api` allowed only as one plain GET else GHWRITE; merge/update-branch/sync MERGE; `pr create/edit/comment/ready`, `issue create/edit/comment` SUBMIT; `pr create` without repo operand REPO (GD:550-663) | 5.3 | guard :550-663 | MATCH |
| 70 | Edit/Write/NotebookEdit path-only, `..` segment TAMPER; Agent/Task `isolation == remote` ESCAPE; Cron*/Schedule* TURN; RemoteTrigger/Workflow/SendMessage ESCAPE; `mcp__*` write-like MCP (MERGE if merge) unless list_/get_/search_/read_ (GD:727-754) | 5.3 | guard :727-754 | MATCH |
| 71 | TAMPER tokens `.claude/state`, `.claude/settings`, `.claude/hooks`, `disableAllHooks`, `.gitconfig`, `.git/config`, `.config/git`, `.git/hooks`, `hooks/pre-push`, `pre-push.launch-level`, `--no-verify`, `hookspath`, `hook.pre-push`, `install_hooks`, `superclaude ... install` (GD:440, 451, 760-775) | 5.3 | guard :440, 451, 761, 767 | MATCH |
| 72 | hooks.json: UserPromptSubmit (no matcher) guard HJ:63-71; PreToolUse matcher regex and guard HJ:115-124; PreToolUse `Bash` identity HJ:125-134; `timeout: 5` on all three (HJ:68, 121, 131) | 5.3, 8.4 | hooks.json :63-71, 115-134 | MATCH |
| 73 | identity: bash prologue :1-54, embedded Python :55-581, `exec uv run --no-project python -I` :582; header :2 "not a sandbox" | 5.3 | identity :1-2, 25-54, 55, 581-582 | MATCH |
| 74 | identity rewrite `shlex.join(['/bin/bash', script, 'execute', sid, tool_use_id, original])` via `hookSpecificOutput.updatedInput`, no `permissionDecision` (ID:430-505, :491-497) | 5.3 | identity :491-498 | MATCH |
| 75 | silent exit 0: input over 1 MiB, unparseable JSON, tool not Bash, invalid sid, no session record, no HOME/store | 5.3 | identity :20-24, 433-453 | MATCH |
| 76 | closed exit 2 texts `launch job: governed Bash call cannot be wrapped safely`, `launch job: UV is required for this invocation`, `launch job: invalid invocation or unavailable private state` | 5.3, 4.6 | identity :501, :52, :579 | MATCH |
| 77 | `identify [PID]` JSON: `ordinary`, `ordinary`+`released`, `governed`+`session_id`, `unknown` + reason `stale|orphaned|foreign|unreadable`; no record is `ordinary` (ID:228-229) | 5.3 | identity :215-260 | MATCH |
| 78 | stores: `requests/<32 hex>` JSON `{session_id, tool_use_id, command}` 0400; `jobs/<kernel sid>.json` keys `pid, start, boot, kernel_sid, session_id` 0400 | 5.3 | identity :164-174, 189-199, 231, 315-316 | MATCH |
| 79 | L2 pre-push: `#!/bin/bash -p`, version line :2, protected refs `refs/heads/main`, `refs/heads/master` (:17), exit 0/1/2, `L2-PROTECTED`/`L2-UNKNOWN` exit 1, `L2-MALFORMED` exit 2, ordinary exits 0 at once (:188), selector run under `env -i`, `timeout 10` (:65) | 5.3 | pre-push :1-2, 9-10, 17, 65, 187-208 | MATCH |
| 80 | plugin copies of the three scripts byte-identical; plugin hooks.json lacks ccsession-tag entries and pragmatic-subagent.js entry, carries `async: true` on freshness-subagent-start.sh | 5.3 | `cmp -s` all identical; plugin hooks.json grep | MATCH |
| 81 | `install_hooks(target_path=None, force=False)`; skip-if-exists unless force (:282); callers main.py:219 (`force`), 412 (`force=True`), hook_adapter.py:230 (`force=False`); `.bak.<UTC stamp>` backup; template copies at :90, 93, 96 | 5.3, 9.2 | install_hooks.py :156, 282, 531-532, 90-96; main.py :219, :412; hook_adapter.py:230 | MATCH |
| 82 | registration of issue-watch at main.py:577-579; no `issue_pipeline` import | 1, 2.2 | snap main.py :577-579 | MATCH |
| 83 | WORKER-CONTRACT 339 lines; sections `## 1. Terms` :9, `## 2.` :27, `## 3.` :49, `## 4.` :68, `## 5.` :299; WC-2 :31, WC-3 :53-58, WC-5 :59, WC-7 :60, WC-12 :61, WC-13 :62, WC-14 :63, WC-15 :64, "Messages carry no --to" :66, WC-6 heading :72, WC-16 :287-289; never-as-worker list :23; "grant row" only :57; 242-243 ownership lines | 5.4 | snap WORKER-CONTRACT.md (grep -n of headings and lines) | MATCH |
| 84 | WC has no WC-17, "Issue pipeline duties", watcher, adopt, COORD-, dispatcher text; no "claim" word | 5.4, 4.4 | grep counts 0; `claim` 0 | MATCH |
| 85 | `CHANGELOG.md:17` records the removal | 2.3, B | snap CHANGELOG.md :15 heading, :17 bullet | MATCH |
| 86 | zero hits for `COORD-`, `release-worker`, `pipeline.json` in snapshot src/tests/plugins; `docs/designs/issue-watcher-live-test.md` absent | 2.3 rows 9, 11, 15, 16 | grep and ls on snap | MATCH |

### Part 3 - Claim flow (`/sc:issue --claim`, orca_worktree.py)

| # | Document claim | Doc loc | Source value | Result |
|---|---|---|---|---|
| 87 | issue.md 117 lines, version 1.1.0; seven flags :36-44; STOP rules :50-59 (E-CREATE-ONLY-FLAG :53, E-CLAIM-ONLY-FLAG :57, E-SUBMIT-NEEDS-FULL :59); Activation :104-110; hand-off prose :85; watcher always passes `--pipeline none` :48 | 5.2, 4.2 | snap issue.md | MATCH |
| 88 | default-level rule claim.md:81: explicit wins; unreadable type/complexity/effort = `worktree`; `full` for every bug; `full` for simple/medium feature <= 16 h; `worktree` for complex or > 16 h; printed `Level: <L> (explicit)` / `(default: <reason>)` | 5.2 | claim.md :81 | MATCH |
| 89 | claim waves: W0 :11-21, W1 :23-34, W2 :36-44, W3 :46-51, W4 :53-63, W5 :75-84, W6 :86-96, W7 :98-115, W8 :117-136; `--pipeline none` ends after W6 (:94); preflight runs for `none` (:17) | 4.2, 5.2 | claim.md | MATCH |
| 90 | exit codes origin_repo.py 0/1/3/4 (E-NO-ORIGIN, E-FOREIGN-REPO, E-NOT-AN-ISSUE), clickup_claim exit 2 only bad arguments | 5.2 | origin_repo.py :47-50, 61-63; clickup_claim.py :50-58 | MATCH |
| 91 | ClickUp `PUT .../task/{task_id}` body `{"assignees": {"add": [<user id>]}}` at clickup_claim.py:232-237; skipped without `CLICKUP_API_TOKEN`/`CLICKUP_WORKSPACE_ID` (:164-169); `CLICKUP_MAX_PAGES` default 20 | 4.5, 5.2 | clickup_claim.py :74, 164-170, 232-237 | MATCH |
| 92 | worker pins: t1 `claude-gw-tier1b`, t2 `claude-gw-tier2`, t3 `claude-gw-tier2b` + `effort: low` (line 7); `model:` line 6; tools line 5 `Read, Grep, Glob, Write, Bash`; 35 lines each; rule lines :28-30 | 5.2, 3.1 | agents/issue-worker-t{1,2,3}.md | MATCH |
| 93 | launch-prompt.md 34 lines, four blocks at :11, :20, :25, :28; `:23` names `/sc:task`; claim-comment.md 23 lines marker at :23; accuracy-check-comment.md 20 | 5.2, 4.3 | templates | MATCH |
| 94 | templates dir 15 files; refs claim 150 / create 99 / labels 67 / tiers 58 / chains 40; SKILL.md 197; scripts 270 / 1906 / 195 | 3.1, 5.2 | `ls`/`wc -l` snap | MATCH |
| 95 | timeouts `DEFAULT_TIMEOUT=120`, `PREFLIGHT_TIMEOUT=30`, `TERMINAL_READ_TIMEOUT=15`, env `SC_ORCA_TIMEOUT` (OW:88-91); `SC_ORCA_SHIM_INTERVAL`, `SHIM_TRIES=5`, `SHIM_INTERVAL=2.0` | 5.2 | orca_worktree.py :88-91, 798-800 | MATCH |
| 96 | `preflight`: argv `orca status --json`; `{"ok": true}` only when runtime reachable, else `{"ok": false, "detail": ...}` (OW:210-223) | 5.2 | orca_worktree.py :210-223 | MATCH |
| 97 | `worktree`: lookup order marker, record, basename, branch (:373-411); create argv `orca worktree create --repo path:<main> --name issue-<N> --base-branch <base> --no-parent --comment "sc:issue <R>#<N>" --json`; list `--limit 500 --json` | 5.2 | orca_worktree.py :316-327, 399-404, 684-700 | MATCH |
| 98 | `finish()` copies `<D>` into worktree, skips `worktree.json`, refuses symlinks, never overwrites a tracked file, differing untracked becomes `.prev`; first tab closed only for new worktree | 5.2 | orca_worktree.py :439-504, 527-563, 568-622, 736-737 | MATCH |
| 99 | warning order (8 codes) `W-ORCA-LIST-FAILED` .. `W-FIRST-TAB-LEFT` (OW:230-239); launch codes REMEDY :802-817 (4) | 5.2 | orca_worktree.py :230-239, 802-817 | MATCH |
| 100 | launch order: record (:1700-1702); already-launched (:1704-1721); stale prompt (:1722-1724); IR-4 (:1730-1747); install_l2 + l2_status (:1754-1758); publish_pending (:1759-1775); agent launch argv 12 elements with `[sc-launch:v1:<nonce>] Read .dev/issues/<N>/launch-prompt.md and follow it.` (:1776-1779); failure removes pending, `hand_command` (:1783-1801); shim detection (:1802-1811); record_launch `{level, submit, at}` (:1626) | 4.3, 5.2 | orca_worktree.py :1696-1834 | MATCH |
| 101 | `IR7_REFUSE = False` at OW:822, refusal branch :1757-1758; word `full-submit` when `--submit` (:1759) | 2.3, 5.2 | orca_worktree.py :822, 1757-1759 | MATCH |
| 102 | IR-4 checks: jq, uv, `cat sed tr mkdir mv ln rm`, Linux process interfaces, guard executable + version line, `CLAUDE_CONFIG_DIR`, `disableAllHooks`, guard registered for UserPromptSubmit and all 23 GOVERNED_TOOLS, identity hook for Bash (OW:955-1045, GOVERNED_TOOLS :841-867) | 5.2 | orca_worktree.py :841-871, 955-1045 (14 + 9 mcp names = 23) | MATCH |
| 103 | `publish_pending`: dirs 0700, file 0600, `.tmp-<nonce>` then `os.replace`, nonce 32 hex (OW:1488-1512); `pending --level worktree|full|full-submit` prints `{"ok": true, "nonce": ...}` (:1515-1523, 1886-1893) | 5.2 | orca_worktree.py | MATCH |
| 104 | `behind_ccsession`: up to 5 tries x 2.0 s, `orca terminal read --terminal <h> --screen --json` for `[ccsession]` / `Session name (Enter or Ctrl+C`, else `orca terminal show` title regex `sc-launch-v1-<hex>-<MMDD>-<HHMMSS>-<hex4>` (OW:792-800, 1564-1583) | 5.2, 4.3 | orca_worktree.py :792-800, 1551-1583 | MATCH |
| 105 | `install_l2`: staged self-test (`_l2_selftest` :1278-1332) before `os.link` (:1428); existing entry never replaced; `core.hooksPath`/non-common hooks dir gives `unsupported`; `--git-path hooks` at :1357; common-dir hooks :1365/1402 | 5.2 | orca_worktree.py :1348-1367, 1386-1442 | MATCH |
| 106 | argparse choices `prompt --level worktree|full` (:1873), `launch` (:1883), `pending` adds `full-submit` (:1891); `--submit needs --level full` exit 2 (:1900-1901); `build_parser` :1857-1894 | 5.2 | orca_worktree.py :1857-1902 | MATCH |

### Part 4 - Watcher (snap `src/superclaude/cli/issue_watch/`)

| # | Document claim | Doc loc | Source value | Result |
|---|---|---|---|---|
| 107 | module sizes cycle 1406, github 960, record 865, audit 404, launch 370, cli 348, predicates 312, runner 130; total 4,795; `__init__.py` empty | 1, 3.1, 5.1 | `wc -l` | MATCH |
| 108 | G1..G7 argv, exact element lists (G1 `gh api user --include`; G2 `gh issue list --repo IronbellyOrg/IronClaude --state open --label <t> --assignee <l> --json number,labels,assignees,state -L 100`; G3/G4 REST `--method GET ... -F per_page=100 -F page=<P> --jq`; G5/G6 `gh api graphql -f query=<Q> -F number=<N> [-f after=<c>]`; G7 `gh api --method GET repos/.../issues/<N> --jq`) | 4.5, 5.1.2 | github.py :175-262 | MATCH |
| 109 | `REPO` github.py:37; `PAGE_SIZE` 100, `PAGE_CAP` 5, `CALL_CAP` 35 (:46), `RESERVED_CALLS` 3 (:49); non-reserved refuse at 32, reserved up to 35; G1+G2 shared => max 37, idle 2 | 5.1.2 | github.py :37, 40-49, 437-463 | MATCH |
| 110 | classify kinds: timeout, non_json, ok, auth_failed, scope_missing, rate_limited, transient, failed (345-371); `GH_ERROR_SIGNS` 267-277 | 5.1.2 | github.py :269-277, 345-371 | MATCH |
| 111 | rate limit: `Retry-After` or `x-ratelimit-reset` within 1..3600 s = `rate_limited`, else now+3600 s `rate_limit_clamped` (github.py:418-431); both exit 5 | 5.1.2 | github.py :376, 418-431; audit.py :51-52 | MATCH |
| 112 | cycle constants cycle.py:34-47: MAX_CANDIDATES 10, MAX_LAUNCHES_PER_CYCLE 1 (:35), DAY_CAP 6, GH_TIMEOUT_S 20, DEADLINE_TOTAL_S 240, GH_FLOOR_S 5, LAUNCH_CUTOFF_S 120, SKEW_WARN_S 60, HEALTH_AGE_S 900, STALE_AGE_S 86400, DISCOVERY_WARN 80 (14 constants) | 5.1.1, 5.1.7 | cycle.py :34-47 | MATCH |
| 113 | config: 8 top-level keys; `enabled` default false, must be JSON boolean (:228-230); `schema_version` 1; labels 1-50 chars, no comma/quote/control/leading `-`, must differ; `project_id` `PVT_[A-Za-z0-9_-]{1,64}`; `owner_account_id` 1..10**20-1; abs paths; `state_dir` default `$XDG_STATE_HOME` or `~/.local/state` + `superclaude/issue-watch`; network fs refused | 5.1.4, 9.1 | cycle.py :58-75, 127-139, 187-192, 195-283 | MATCH |
| 114 | approvers file rules (regular, O_NOFOLLOW + inode recheck, euid owner, no group/other write, <= 1 MiB, UTF-8, ids `[1-9][0-9]{0,19}`, >= 1 id) cycle.py:298-361 | 5.1.4, 4.6 | cycle.py :73-75, 298-361 | MATCH |
| 115 | exit resolution precedence 2, 6, 7, 5, 3, 4; 75 only as sole condition; cycle never produces exit 1 (cycle.py:462-483) | 5.1.1 | cycle.py :462-477; cli.py:123-129 | MATCH |
| 116 | cycle step order: enabled gate :685-686; validate_setup :687-693; flock :694-702; DISABLED :712-713; load :739-750; login :752-775; origin :716-722; sweep :777-792; discovery :794-808; order [:10] :725-737; candidates :812-834; launch :1026-1112; commit :1116-1144; conclude :1176-1211 | 4.1, 5.1.1 | cycle.py line ranges inspected | MATCH |
| 117 | per-candidate gates E1..E15 words and line cites (919-961), re-approved note :646-661, `_rate_stop` +3600 s :663-668, `halt` :833-834 | 5.1.1.1 | cycle.py :646-668, 815-834, 915-961 | MATCH |
| 118 | launch step order: dry-run return :1029-1035; probe :1048-1052; prompt :1054-1056; `_revalidate` :979-1016 (edits not re-read :1006); day cap :1061; DISABLED :1063-1064; cutoff :1069/1078/1095; origin :1074-1075; pending save :1091-1092; `launcher.launch(orca, worktree, prompt, 120.0)` :1099 | 5.1.1.2, 4.1 | cycle.py :979-1112 | MATCH |
| 119 | launch argv 12 elements, `ORCA_AGENT` `claude`, `PROMPT_PATTERN` `^/sc:issue --claim [1-9][0-9]{0,8} --pipeline none$` (:33), `build_claim_prompt` :84-92, `launch_argv` :95-116, `retry_argv` :119-132 (`--retry-launch <id>` before `--json`), cwd=worktree, 120 s | 5.1.3, 2.1 | launch.py :28-132, 352-370; cycle.py:40 | MATCH |
| 120 | `find_orca`: `_ORCA_CLIS = ("orca-ide","orca")`, absolute path only, `skills list --json` must list `orca-cli`, not cached (launch.py:163-203) | 5.1.3 | launch.py :163-203; install_user_setup.py:36 | MATCH |
| 121 | origin check `git -C <worktree> remote get-url origin` = `ironbellyorg/ironclaude` lower-cased (launch.py:233-251, ORIGIN_REPO :50) | 5.1.3, 4.6 | launch.py :50, 233-251 | MATCH |
| 122 | `outcome_of` (326-349), `OPERATION_ID_PATHS` 42-45, `OP_UNKNOWN_TEXT` 47, `LaunchOutcome.detail` 8 words 58-70 | 5.1.3, 5.1.7 | launch.py | MATCH |
| 123 | `dispatch.json`: 7 top-level keys; 17 entry fields in listed order (record.py:69-88); 6 states (:34-36); extra/missing key = `store_invalid` | 5.1.3, 6 | record.py :34-36, 69-88, 120-130 | MATCH |
| 124 | transitions T-1..T-13 with functions and line cites (fail 503-525, backoff 528-535, sweep 627-651, mark_claimed 654-686, reset_entry 706-720); MAX_ATTEMPTS 3, BACKOFF 10 min, LEASE 60 min, DAY_CAP_WINDOW 24 h | 5.1.3 | record.py :434-443, 503-720 | MATCH |
| 125 | save: sorted JSON indent 2 ASCII, `write_prepared_bytes`, chmod 0600, dir fsync (:370-378); lock: `flock(LOCK_EX|LOCK_NB)`, `O_NOFOLLOW`, regular file owned by euid, inode re-check (:380-419); DISABLED via `os.path.lexists` (:421-423) | 5.1.3 | record.py | MATCH |
| 126 | `init-state`: `state_dir` 0700, `lock` 0600 (`O_EXCL|O_NOFOLLOW`), exits 6 on existing store (cli.py:201-214; record.py:753-802) | 5.1.4 | record.py :753-802; cli.py :201-214 | MATCH |
| 127 | 59-word REASON_TABLE (audit.py:26-102) with group counts 4/7/5/2/2/5/1/1 cycle, 17 skip, 9 entry, 1 note, 4 warning, 1 operator; exit per word | 5.1.6, 10.2 | audit.py :26-102 counted | MATCH |
| 128 | audit rotation `ROTATE_BYTES` 5 MiB keeping `.1`-`.4`, file 0600, one `os.write` per line | 5.1.4 | audit.py :106-107, 123-160 | MATCH |
| 129 | cli: five verbs; `_EXIT_UNHEALTHY=1`, `_EXIT_CRASH=1`, `_EXIT_CONFIG=2`, `_EXIT_STORE=6`, `_EXIT_LOCK_HELD=75`; `--config` default `~/.config/superclaude/issue-watch.json`; `once` prints `cycle:`, `exit:`, dry-run `probe:` and `would_launch:`; `status` exit 1 when unhealthy; `reset` rules | 5.1.4 | cli.py :31-38, 111-348 | MATCH |
| 130 | status report: healthy = age <= 900; stale = unknown or abandoned `pending_orphan` older than 86400 s; `retry` argv printed not run; `slo_numbers` p95, 7-day exit-0 share, lease share, stale count (cycle.py:1270-1406) | 5.1.4 | cycle.py :1227, 1251-1335, 1359-1406 | MATCH |
| 131 | predicates: `SKEW_TOLERANCE_S` 300 (:17); approval_of :185-234; is_intended_owner :162-174; unchanged_since :237-259; project_check :262-271; marker window :274-296; eligibility_order :299-312 | 5.1.5 | predicates.py | MATCH |
| 132 | `runner.py` 130 lines, `STDERR_CAP_BYTES = 500`, `shell=False`, stdin closed, mandatory timeout | 5.1, 11.1 | runner.py :15, 91-101 | MATCH |
| 133 | discovery: >= 100 results = `truncated`; repeated number = `discovery_duplicate` (github.py:823-830); bad number rejected first (:827-828) | 5.1.1, 5.1.7 | github.py :486, 823-830 | MATCH |
| 134 | test-file counts: guard 4631 lines/162 tests; 17 files 24,388 lines, 921 plain-grep (920 strict) tests; tests/issue_watch 867 tests, 19,801 lines, 19 fixtures; worker_contract 3220/59; claim test files (62, 15, 109, 26, 18, 29, 24, 11, 8 tests; 1055/212/2501/716/291/569/559/249/69 lines); hooks/cli/unit/core file counts in 5.3 | 1, 5.2, 5.3 | `wc -l` and `grep -c` on snap tests | MATCH |

(Parts 2 to 4: 83 items. Parts 5 and 6 follow.)

### Part 5 - Sections 6 to 14 and Appendix A (restated facts, tables, counts)

| # | Document claim | Doc loc | Source value | Result |
|---|---|---|---|---|
| 135 | state stores: `dispatch.json` 0600, sorted JSON indent 2 ASCII; `lock` 0600; `DISABLED` by `lexists`; `audit.jsonl` 0600 rotated at 5 MiB keeping four; `dry-run.json` 0600 keys `schema_version, considered, shadow_launches`; `sessions/<sid>.ok` empty; `requests/` and `jobs/` 0400; `worktree.json` atomic 0644 with `{path,status,launch{level,submit,at}}`; mirror `{path,launch}` | 6 | record.py :281-283, 370-378, 421-423, 805-806, 864; audit.py :106-133; identity :171; orca_worktree.py :507-524, 1626-1638; atomic write chmod 0644 | MATCH |
| 136 | retry argv is the launch argv with `--retry-launch <id>` before `--json` = 14 elements, printed only (cycle.py:1308-1312) | 8.1 | launch.py :119-132 (12+2); cycle.py :1308-1325 | MATCH |
| 137 | worktree-step commands: `git rev-parse --verify <base>`, `git -C <wt> ls-files .dev/issues/<N>`, `orca terminal list --worktree path:<wt> --json`, `orca terminal close --terminal <h> --tab --json`; preflight 30 s | 8.1 | orca_worktree.py :316-327, 416, 591-619, 672, 684-700 | MATCH |
| 138 | hooks.json rows: SessionStart 10/5/5/5; UserPromptSubmit 3/5/5; SessionEnd 5; PreToolUse Edit|Write 1, Bash 3/3, guard 5, identity 5; PostToolUse 1 (async)/1; SubagentStart 1/5, SubagentStop 1 (async); line ranges `:3-42`, `:45-71`, `:73-83`, `:85-94`, `:95-114`, `:115-124`, `:125-134`, `:136-157`, `:159-190` | 8.4 | hooks.json read in ranges | MATCH |
| 139 | 8.2 verb exits: `status` 0/1/2/6; `check-config` 0/2; `init-state` 0/2/6; `reset` 0/2/6/75; `orca_worktree.py` 0 or 2; `origin_repo.py` 0/1/2/3/4; `clickup_claim.py` 0 or 2 | 8.2, 10.4 | cli.py :164-348; orca_worktree.py :204-207, 1897-1902; origin_repo.py :47-50; clickup_claim.py :50-58 | MATCH |
| 140 | 8.3 L2 install: hook 0755 hard link plus data file `pre-push.launch-level` 0644 (line 1 HOME, line 2 uv dir); never replaces an existing entry | 8.3 | orca_worktree.py :1411, 1421-1422, 1428; pre-push.sh :5, 29-48 | MATCH |
| 141 | config table (9.1): defaults and rules for 8 keys, line cites (:222-226, 228-230, 240-243, 245-249, 251-255, 257-259, 261-272, 187-192) | 9.1 | cycle.py | MATCH |
| 142 | env/paths (9.3): `CLICKUP_MAX_PAGES` default 20 with fallback; `skipped` reasons `no_token`, `no_workspace`; `SC_ORCA_TIMEOUT` seconds float; `SC_ORCA_SHIM_INTERVAL` 2.0; `CLAUDE_CONFIG_DIR` check :989-997; `CCSESSION_ORIGIN` values `human`/`agent` (ccsession-orca :198-213, 249-256) | 9.3 | clickup_claim.py :74, 88-94, 164-170; orca_worktree.py :120-131, 989-997; ccsession-orca | MATCH |
| 143 | 10.1 exit-code table words per exit (0, 1, 2, 3, 4, 5, 6, 7, 75) and evidence cites | 10.1 | audit.py :26-102; github.py :489-496; cycle.py :663-668, 748-750, 764-765, 842-843 | MATCH |
| 144 | 10.2 vocabularies: 27 cycle + 17 skip + 9 entry + 1 note + 4 warning + 1 operator = 59; 13 STOP codes; 8 worktree + 4 launch warning codes; ClickUp result words; `Read.kind` adds `incomplete`, `budget_exhausted`, `truncated`, `discovery_duplicate` | 10.2 | audit.py counted; SKILL.md :32-173 (13 distinct E- codes); orca_worktree.py :230-239, 802-817; clickup_claim.py :51-56, 166-242; github.py :482, 588, 619, 824, 830 | MATCH |
| 145 | 10.3 recovery: write-ahead save and restore at cut-off (:1091-1098); sweep (record.py:627-651); reset keeps day-cap count via `consumed_log` (:706-720); kill switches; budget `gh_timeout`; guard fail-open/closed cites | 10.3 | cycle.py; record.py; guard :147-163, 168-173, 208-238, 386-392 | MATCH |
| 146 | 11.1 numeric constants and cites: CALL_CAP 35, RESERVED 3, PAGE 100/5, MAX_CANDIDATES 10, DAY_CAP 6, DISCOVERY 100/80, GH 20, PROBE 10, GIT 10, LAUNCH 120, DEADLINE 240, FLOOR 5, CUTOFF 120, SKEW_WARN 60, SKEW_TOLERANCE 300, HEALTH 900, STALE 86400, RATE_LIMIT_MAX 3600 (github.py:376, cycle.py:488), MAX_ATTEMPTS 3, BACKOFF 10 min, LEASE 60 min, ROTATE 5 MiB, STDERR 500, approvers 1 MiB | 11.1 | cycle.py :34-47, 488; github.py :40-49, 376, 486; record.py :434-443; audit.py :106-107; runner.py :15; predicates.py :17 | MATCH |
| 147 | 11.1 hook/size limits: LL-BIG > 65536 (:419), G2 rule 2 8192 bytes / 64 args (:507, :511), identity input <= 1 MiB (:433-434) and command <= 32768 bytes (:197), L2 identity lookup `timeout 10` (pre-push :65), L2 self-test 30 s (constant orca_worktree.py :1078; used :1284, :1311), ClickUp one 429 retry (:119-123) | 11.1 | cited lines | MATCH (see M-4 for the `:1178` cite) |
| 148 | 12.1 closed vocabularies: 18 `LL-*` = 16 classes + `LL-NOBIND` + default `LL-BROKEN`; claim STOP codes 13, warning codes 12; L2 words 3 | 12.1 | guard :41-114; SKILL.md; pre-push :193-207 | MATCH |
| 149 | 13.1 symbols: `_cond` :587-588, `_stopped` :590-592, `_call` :557, `_issue_arg` :111, `_page_arg` :118, `_cursor_args` :141, `_trigger_arg` :150, `_login_arg` :168, `render_prompt` OW:746-761, `BLOCK_MARKER` OW:743, `ll_deny` :135-139, `_FRESHNESS_SCRIPTS` :42-97 (scripts at :90, 93, 96), tier keys in `ccsession-models.json` lines 85, 93, 104, 113 | 13.1 | files read at those lines | MATCH |
| 150 | 14.x code-evidence rows (D-01 dead constant, D-09 `disabled_present` test-only, D-10 `LaunchOutcome.detail`, D-11 write-only fields, D-12/X-14 `retry_argv`, D-13 tmp cleanup `atomic.py:33-38`, D-25 `probes.py:43` default `orca-ide`, X-13 `_ORCA_CLIS` line 36, X-18 `fail` from `failed` :511, X-19 id pattern, X-20 `_find_orca` :247, Q-07 `_retry_orca` :1262-1267, Q-09 `cli.py:309-313`, Q-21 session-start.sh `python3 -c` :20-21) | 14 | grep and reads on snap | MATCH |
| 151 | 14.1.1: `reset` refuses `claimed` (`record.py:448`); Linux check `cli.py:88` and `:314`; `status` unchecked `:169`; identity returns 0 for non-Bash `:442-444` | 14.1.1 | record.py :448; cli.py :84-91, 169, 314; identity :442-444 | MATCH |
| 152 | Appendix A.1 per-file lines/tests (conftest 1155/0; cycle 4982/237; github 2161/141; record 2377/147; cli 1672/60; security 1013/16; no_text 971/22; launch 952/66; audit 849/46; predicates 732/44; e2e 443/4; slo 421/14; boundaries 413/13; crash 373/6; find_orca 288/10; concurrency 275/6; no_shell 266/9; runner 226/16; origin_parity 179/7; marker 53/3; fixtures 19 files 12,059 bytes) | A.1 | `wc -l`, `grep -c 'def test_'`, `cat | wc -c` on snap tests | MATCH |
| 153 | Appendix A.2/A.3/A.4 per-file lines/tests (guard 4631/162 (163 plain, extra string literal at :4615); l2_tokens 160/7; registration 127/7; with_identity 212/5; worker 300/11; identity 1530/56; pre_push 1194/34; records 230/8; observations 84/6 (12 parametrised cases skip); governed 56/1; freshness policy 115/5; protocol 1055/62; orca_worktree 2501/109; l2_install 716/26; repo_resolution 291/18; worker_agents 559/24; t1 fallback 69/8; worker_contract 3220/59; clickup 569/29; model_alias 249/11; command 212/15; body_templates 97/5; install_hooks 1246/37; install_ccsession 417/22; ccsession_tag 7101/277; tiers 3821/149; launch guidance 62/3) | A.2-A.4 | same commands | MATCH |
| 154 | Appendix A "48 rows (A.1 21, A.2 11, A.3 9, A.4 7)" | A end | rows counted in the document | MATCH |
| 155 | test-name line cites in 5.3/5.2 (grid tests :3394, :3401, :3457, :905, :927, :936, :1712, :4520, :3737, :3800, :3852; ids `GRID-<CLASS>-<case>-<level>` from `test_grid_policy`; worker tests :74, :187, :213, :226-230, :262, :287; `test_ir7_shipped_switch_is_off` :639; protocol :147, :251, :350, :560, :791; command :84, :191; orca_worktree :837, :1838, :2472; clickup :277, :311, :548; worker agents :77, :85, :102; alias policy :83, :104) | 5.2, 5.3, A | grep -n of each `def test_` | MATCH |
| 156 | design-doc line counts in the Section 3 tree: issue-watcher 942, setup 706, sc-issue-command 509, claim-pipeline-flag 470, launch-level-hook 627, guard-g2 51, g2-no-to 57, fu1 119 | 3 | `wc -l` on snap docs | MATCH |
| 157 | test_audit pins 59 names (`test_reasons_pin_59_names...` :214) and pairs (:223); `test_every_assumed_shape_fixture_parses_and_is_labelled` asserts 19 files | 5.1.6, 15.2 | test_audit.py :214, 223; test_github.py :575-583 | MATCH |
| 158 | CHANGELOG, WORKER-CONTRACT 339 lines, `grep -c` of `WC-17` / `Issue pipeline duties` = 0; COORD- no output; `orca-ide` count in guard = 0 (spot-check 7, 8, 9) | 15.2 | commands re-run on snap | MATCH |
| 159 | `_launch` ordering and `_revalidate` G7 reserved (`reread` uses `reserved=True`), G3'/G6' via `reserved=True` | 4.1, 5.1.2 | github.py :942; cycle.py :996, 1013 | MATCH |
| 160 | `ccsession-orca` carries no launch-level text; `wire_ccsession` timeouts 30/30/60 s; hooks installed mode 0755 (install_hooks.py:288) | 5.3, 8.1 | grep zero hits; install_ccsession.py :98, 119, 138 | MATCH |

### Part 6 - Findings (graded)

No BLOCKING finding. Six MINOR findings (notes; they do not fail the gate).

| ID | Severity | Document location | Documented claim | Source value (path:line) | Required fix |
|---|---|---|---|---|---|
| M-1 | MINOR | doc :737 (5.1.1) | "The cycle-line reason is a stop reason, else the first condition reason matching the exit code, else `cycle_complete`" | `src/superclaude/cli/issue_watch/cycle.py:1164-1174` (`_cycle_reason`): when the exit code is non-zero the first condition whose code equals the exit comes first, then `stop_reason`, then `cycle_complete`. The order of the first two is reversed in the document. No reachable cycle gives a different word: every non-zero condition except exit 7 is itself a stop reason, and exit 7 cannot coexist with a different stop code (S1 halt, `:833-834`). | Reword to the code order (condition matching a non-zero exit, else stop reason, else `cycle_complete`). Wording only. |
| M-2 | MINOR | doc :259 (2.1 diagram) | box "3 orca_worktree.py (only code that calls orca)" | `src/superclaude/cli/issue_watch/launch.py:95-116, 358-370` (the watcher also runs `orca agent launch`); the qualified form "only code that calls `orca` for the claim" is used at doc 2.2 and `SKILL.md:35` | Add "for the claim" in the diagram box. |
| M-3 | MINOR | doc :1101 (5.2 `prompt` row) | `kept` when "a launch entry exists and the file exists" | `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:770-777`: also requires `guarded_record_path(source, common)` (the recorded worktree still exists); `claim.md:83` states it | Add "and its worktree still exists". |
| M-4 | MINOR | doc :1681 (11.1 "Claim command timeouts") | L2 self-test 30 s at `orca_worktree.py:1078, 1178` | constant at `:1078`; use sites are `:1284` and `:1311`; `:1178` is `L2_PACKAGED_MAX` | Replace `:1178` with `:1284, 1311`. 30 s is correct. |
| M-5 | MINOR | doc :1003 and D-19 | IR-7 refusal "text `OW:829-831`" | the refusal text is `IR7_REFUSAL` at `orca_worktree.py:823-826`; `:829-831` is `remedy()` that selects it | Cite `:823-831`. |
| M-6 | MINOR | doc :210 (Section 1 statistics) | "20 files in `tests/issue_watch/` (19 test modules plus `conftest.py`), 19,801 lines" | the directory holds 21 `.py` files: the 19 test modules, `conftest.py` and an empty `__init__.py` (0 lines, so the 19,801-line total is unaffected) | Say "plus an empty `__init__.py`" or count 21. |

## Checks performed

- Items compared: 160 numbered rows (Parts 1 to 5); many rows cover several facts, so the facts checked exceed 400. MATCH 160, MISMATCH 0 at a BLOCKING level; the six MINOR notes above are wording, an omitted condition or a cite that points a few lines from the true site.
- Appendix B: every claim re-read from `git show 01e7a9e23^:<path>` for all ten removed files (line counts, 10 verbs with options and exit words, approval texts, plan-hash framing and 11 refusal words, adoption and approval row keys and states, release action flags and refusals, WC-17 six steps, six duty rows, the TAMPER case patterns, `git diff` for the guard and `main.py`, test counts per file, edits to `test_worker_contract.py` (3,181/61 to 3,135/59) and `test_launch_level_guard_worker.py` (330/13 to 300/11)). No wrong removed-code fact found.
- Level matrix: all 16 W/WA/F/FS cells for IMPL, COMMIT, PUSH, SUBMIT agree with `launch-level-guard.sh:785-803` (read in full); TURN, SKILL and the ten always-blocked classes agree.
- Hook events and matchers: `hooks.json` lines 63-71, 115-134 (event, matcher, command, `timeout: 5`) agree; plugin copy differences agree.
- Argv lists: G1-G7 (`github.py:175-262`), the 12-element launch argv (`launch.py:95-116`), the claim launch argv (`orca_worktree.py:1776-1779`), worktree create and list argv, ClickUp PUT body agree element by element.
- Constants, exit codes and reason words: cycle.py constants (14), exit precedence, `REASON_TABLE` (59, counted by group), cli.py exit constants, github.py caps, record.py MAX_ATTEMPTS/BACKOFF/LEASE/DAY_CAP_WINDOW, audit rotation, runner stderr cap, model pins (t1 tier1b, t2 tier2, t3 tier2b + `effort: low`) agree.
- Counts: every test-file line and test count in Sections 1, 5 and Appendix A, the 17-file guard total (24,388 lines; 921 plain, 920 strict), 867 watcher tests, 19 fixtures (12,059 bytes), 15 templates, source line counts agree.
- Not checked by reading source (outside the assigned set): contents of `docs/designs/*` and `docs/architecture/*` beyond line counts and the one line at `SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:268`; `skills/agent-work-report`; the design-doc line cites inside the contradiction tables.
- Tool use: Read 31, Grep 12, Bash 24 (git show, wc, grep -c, sed -n; read-only), no write under the snapshot.

Confidence: Verified 160 / 160 rows | Unverifiable 0 | Unchecked 0 | Confidence 100% for the rows listed; the checked facts cover the assigned set, not every sentence of the document.

Status: Complete

## Verdict: PASS
