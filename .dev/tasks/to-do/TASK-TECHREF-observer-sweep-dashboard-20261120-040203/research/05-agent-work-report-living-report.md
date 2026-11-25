# Research: agent-work-report skill (pipeline and living report)
**Investigation type:** Code Tracer + Doc Analyst
**Scope:** src/superclaude/skills/agent-work-report/ (SKILL.md, config.json, scripts/*.py, templates/*), tests/skills/test_agent_work_report.py, tests/skills/test_worker_contract.py, docs/designs/orchestrator.md, docs/designs/sc-closeout.md, src/superclaude/skills/sc-closeout-protocol/ (settle.sh), src/superclaude/cli/issue_watch/
**Status:** Complete
**Date:** 2026-11-20

---

Path convention: every code path below is relative to the repo root of the read-only export of origin/master 61ac2c2e6 (/home/coder/.cache/ic-snap-20261120/master) unless it says "checkout".

## 0. File inventory (Glob and `ls` of the snapshot)

- Skill folder `src/superclaude/skills/agent-work-report/`: `SKILL.md`, `config.json`, `scripts/` (activity.py, check.py, classify.py, clickup.py, collect.py, common.py, compare.py, exclude.py, match.py, orca_term.py, page.py, prefs.py, render.py, run.py, sessions.py, waker.py: 16 files), `templates/` (item-template.md, needs-you-template.md, overview-template.md, summary-template.md, qa-report-template.md, report-template.html, report.js: 7 files).
- Closeout: `src/superclaude/skills/sc-closeout-protocol/scripts/settle.sh` (one `settle.sh` under `src/superclaude`), `src/superclaude/commands/closeout.md`.
- `ls src/superclaude/commands | grep -i -E 'orchestr|closeout|sweep|observe'` gives `closeout.md`, `sweep.md`; `ls src/superclaude/skills | grep -i -E 'orchestr|closeout|sweep|agent-work'` gives `agent-work-report`, `sc-closeout-protocol`, `sc-sweep-protocol`. There is no `orchestrator.md` command and no `sc-orchestrator-protocol` skill.
- `ls src/superclaude/cli` has: audit, doctor.py, eval, ic.py, init_lite.py, install_*.py, issue_watch, main.py, observe, pipeline, prompt_policy.py, recommend, reflect, review, swarm, sweep, user_settings_defaults.json, vocabulary.py. There is no `orchestrator` package; `Grep orchestrat` in `cli/main.py` has no match; the only `orchestrator*` file under `src/` is `cli/eval/orchestrator.py` (the eval runner).
- `src/superclaude/cli/issue_pipeline/` has no files (PR D landed).

## 1. SKILL.md (194 lines): what the skill says about itself

File: src/superclaude/skills/agent-work-report/SKILL.md. Size (wc -l): SKILL.md 194; scripts: run.py 887, clickup.py 642, render.py 626, common.py 507, sessions.py 444, waker.py 405, page.py 387, check.py 350, collect.py 317, match.py 283, activity.py 279, compare.py 197, classify.py 147, orca_term.py 133, exclude.py 109, prefs.py 64 (scripts total 6,321); templates: item-template.md 73, needs-you-template.md 23, overview-template.md 42, qa-report-template.md 33, report-template.html 172, report.js 122, summary-template.md 14. Tests: tests/skills/test_agent_work_report.py 4,005 lines; tests/skills/test_worker_contract.py 3,220 lines.

Frontmatter (SKILL.md:1-4): name `agent-work-report`; description "The daily helper" for Clay: all open work across both Ironbelly GitHub orgs, Projects boards, ClickUp and Orca agent sessions in one report. Triggers: coordinator session woken for the daily report, `/agent-work-report`, "what's on my plate" (SKILL.md:3).

Doc claims (code verification follows in later sections):
- SKILL.md:10 "The model reads the run files and never calls GitHub, ClickUp or Orca itself." Target "about 5 minutes and well under 1M new tokens a run".
- SKILL.md:12 names the spec `.dev/specs/SPEC-AGENT-WORK-COORDINATOR-20261027.md` "in the orchestrator repo (milestone 1)": that repo is not in the snapshot or checkout; **[UNVERIFIED]**. States "The orchestrator (`/sc:orchestrator`) does every check-in itself; there is no session manager."
- SKILL.md:14 state lives in `.dev/coordinator/` of the orchestrator repo, path = `$AWR_ROOT` else `orchestrator_repo` in `~/.config/superclaude/issue-watch.json` (repo must hold `repos.yaml`). Reader side **[CODE-VERIFIED]** at common.py:28-51. Who sets the key: section 12.
- SKILL.md:16 "The orchestrator keeps one entry file per issue it holds in `.dev/coordinator/orchestrated/` (added at claim, updated at milestones, moved to `orchestrated/closed/` at close; information items go to `orchestrated/info/`)". The writer is the orchestrator, not this skill. See sections 9 and 10.
- SKILL.md:30-35 two Orca automations: `coordinator-morning-wake` runs `waker.py morning` (07:00 local) and `coordinator-missed-check` runs `waker.py check-missed` (09:00 local), Mon-Fri; Orca cron triggers `0 12,13 * * 1-5` and `0 14,15 * * 1-5` (UTC, to cover the clock change). They live in Orca, outside the repo: **[UNVERIFIED]** as to whether they exist now. The script side is verified in section 8.
- SKILL.md:37 ClickUp API with `CLICKUP_API_TOKEN` (required) and `CLICKUP_WORKSPACE_ID` (optional); never the ClickUp connector (decision cited "IronClaude #302").
- SKILL.md:38 Orca terminal list and "agent hook file" say which transcript belongs to which terminal; "What Orca says about a session's state is never used."
- SKILL.md:44-54 output locations; SKILL.md:56-72 artifact-to-writer table (checked in section 2); SKILL.md:76-95 the 15 steps (section 4); SKILL.md:97 time budget 120 minutes (NFR-4); SKILL.md:140 the six session statuses; SKILL.md:152 the gate; SKILL.md:155 `page.py --open`; SKILL.md:157 ClickUp DM; SKILL.md:161 commit, "Never push."
- SKILL.md:192-194 Boundaries: "never routes work, starts or messages agents, approves prompts, or posts on GitHub or ClickUp except the DM to Clay." Section 8 shows `waker.py` does start a coordinator session and types into its terminal (only the coordinator's own); see Gaps.

Key Takeaways
- SKILL.md is the single behavioural spec. The model's part is Steps 3 (record DM answers), 10, 11 (fix), 13 (post and DM), 15.
- The doc names the orchestrator as the writer of `orchestrated/` entry files; that writer is checked in sections 9-11.

## 2. common.py (507 lines): shared helpers, state paths, the entry-file contract

- Config: `SKILL_DIR`, `CONFIG = json.loads(config.json)` at common.py:18-19.
- `repo_root()` common.py:28-51 **[CODE-VERIFIED]**: `$AWR_ROOT` if set (35-37), else the `orchestrator_repo` key of `~/.config/superclaude/issue-watch.json` (`POLL_CONFIG`, 25; read at 38-41), which must be an absolute path with a `repos.yaml` file in it (46-50); otherwise `SystemExit` with a message (42-45). No YAML is read (comment 32-34).
- `workspace_path()` 54-56 returns `repo_root()` as a string: the coordinator's Orca workspace is the orchestrator repo's own worktree (comment cites DQ12).
- `state_dir()` 59-62 = `<repo>/.dev/coordinator` (created); `runs_dir()` 65-68 = `.../runs`.
- `run_cmd(args, timeout=120)` 103-113: `subprocess.run(args, capture_output, text, timeout)` with a list (no shell); raises `CommandError` on non-zero exit or timeout. `gh_json(*args)` 116-117 runs `gh <args>` and parses JSON.
- `answered_since(since)` 120-130 reads `action-log.jsonl` rows with `action == "answer"`.
- `safe_title` 74-82 strips control/format characters, folds whitespace, caps 200 characters (TITLE_MAX 71).
- `safe_url` 176-180 accepts only `http(s)://` and `orca://` (URL_OK 173); `inside_repo` 164-170 rejects paths that resolve outside the orchestrator repo.
- Entry-file reading: `ORCHESTRATED = "orchestrated"` (152); `orchestrated_dir()` 160-161; `entry_files(folder=None)` 183-209 reads `*.json` directly inside the folder, refuses a symlinked folder or file and prints a note to stderr, skips unparseable or non-object JSON; `entry_issue_url(entry, path)` 212-220 uses `entry["url"]` else the file stem `<owner>__<repo>__<number>`; `entry_session_ids(entry)` 223-233 unions `session_status` keys, `worker.session_ids`, `orchestrator.session_id`, and ids parsed from `worker.link` / `orchestrator.link` (prefix `orca://session/`, SESSION_URL 317).
- Constants that fix the report's vocabulary: `SESSION_STATUSES` 240-247 (working, progressed, waiting on you, stuck, stalled, done); `ITEM_SECTIONS` 345-357 (11 parts: What it is, Current state, Done with evidence, Still to do, What happened since the previous report, Recommendation, Needs you, ClickUp tasks, Agent sessions, Why this priority, How I know); `BULLET_SLOTS` 359; `NEEDS_PARTS` 361-371 (9 bullets); `WRITTEN` 373; `STATES` 375-385 (9 states); `WRITE_GROUPS` 386 = assigned, owned, opened, inprogress; `LEVELS` 388 = Urgent, High, Medium, Low; `STATE_ORDER` 389-399; `REPORT_PORT = 8765`, `REPORT_URL = http://127.0.0.1:8765/report.html` 404-405; `NOTICES` 407-411; `ESCALATION_LINES` 153-157.
- `to_write(run)` 420-434: items in a write group that are new, changed or absent from the previous run's `notes.json`. `previous_notes(run)` 414-417 resolves the previous run through `run.json["previous_completed_run"]`.
- `order_key` 481-489 sorts by level then state; `needs_in_order` 492-507.
- The comment block common.py:133-151 is the entry-file contract (fields listed in section 9). It states at 136 "`superclaude orchestrator report-entry` writes them; this skill reads them (exclude.py, run.py refresh, render.py entry) and moves a closed one (run.py refresh)." The writer verb is checked in section 10.

Key Takeaways
- All subprocess calls in this skill go through `run_cmd` (list args, no shell) with two exceptions (the `subprocess.Popen` of the page server, page.py:318, and the `subprocess.run` of `git remote get-url`, sessions.py:119).
- State location is resolved only by common.py:28-51; nothing else in the skill knows the orchestrator repo path.

## 3. run.py (887 lines): run lock, run folder, gate, close, abandon, log, refresh

CLI dispatch run.py:868-887: `open <kind>`, `gate <run>`, `summary <run>`, `close <run>`, `abandon <run> <reason>`, `log <run> <action> <item|-> <reason>`, `refresh [--run <run>]`, `status`. Kinds: daily, hourly, on-demand (docstring 4-7).

Run lock (run.py:75-76, 90-157) **[CODE-VERIFIED]**:
- File `<state>/run.lock` = JSON `{run, kind, started}` (122).
- `open_run(kind)`: if a lock exists and `now - started < budget` (budget from `config.json` `time_budget_minutes`: daily 120, hourly 10; 95-100), it writes `<state>/wakes/<time>-skipped.json` `{mode, time, outcome: "SKIPPED: run <id> is still active"}` (101-111), prints to stderr and `sys.exit(3)`. If older than the budget the old lock is kept as `stuck` and replaced (114), and `run.json.stuck_run_replaced` carries it (131).
- Run id = UTC `%Y%m%dT%H%M%SZ-<kind>` with a `-n` suffix on collision (115-120).
- Writes into the new folder: `run.json` `{run, kind, started, previous_completed_run, stuck_run_replaced}` (124-133); `incomplete-runs.json` (list of earlier run folders with no `complete.json` since the previous run started, 135-143); `wake-records.json` (the `wakes/*.json` records since then, 144-153); `automation-runs.json` (154); `run-log.md` (155).
- `latest_completed` 79-87 ignores `hourly` runs.

Commands this script runs (run_cmd, list args):
- `orca automations list --json` and `orca automations runs --id <id> --json` (`automation_runs` 160-186, `orca_result` 197-201). Read-only. Only automations whose name starts with `automation_prefix` ("coordinator-", config.json) are used. On failure or none found it writes `{"read": false, "reason": ..., "runs": []}`.
- `gh issue view <number> --repo <owner/repo> --json state,stateReason,assignees` (`reconcile_entries`, 502-510). Read-only.

Delivery gate (run.py:204-368) **[CODE-VERIFIED]**:
- `REQUIRED_CHECKS` (204-212): placeholders, template, sessions, carry-forward, needs-you, candidates, links.
- `passed(folder)` 219-242: `script-checks.md` must have a row `| <name> | PASS |` for all 7 (227-236) and must contain the line `overview sha256: <sha256 of overview.md now>` (237-241).
- `page_ok` 254-265: `report.html` must contain `<meta name="overview-sha256" content="<sha256 of overview.md>">`.
- `summary_ok` 348-358: `summary.md` must equal `build_summary(folder)` byte for byte.
- `deliverable` 245-251 chains the three; `gate` 361-368 prints `PASS: the report may be delivered` (exit 0) or `BLOCKED: <why>; fix it, do not deliver` (exit 1).
- `close_run` 371-387: a non-hourly run needs `passed()`; writes `complete.json` `{run, kind, finished}` and removes the lock if it is this run's. NOTE: `close` checks `passed` only, not `page_ok` or `summary_ok`, although SKILL.md:183 says the gate is "enforced again by `clickup.py dm` and `run.py close`"; for `close` the code enforces the checks-and-sha part only (compare section 7 for `clickup.py dm`).
- `abandon_run` 390-402: writes `abandoned.json` `{run, reason, time}`, releases the lock, writes no `complete.json`.
- `log_action` 405-418: appends to `<state>/action-log.jsonl` `{time, run, action, item, reason, overview}` and a line to `<run>/run-log.md`.
- `build_summary` 268-340: summary is generated from `overview.md` and `templates/summary-template.md` only (counts table, `**Since the previous report:**` line, each "Needs you" heading via `needs_in_order`, "Not checked" lines, `REPORT_URL`); en and em dashes are replaced by `-` (340).

`refresh` (the living report builder) run.py:433-865 is described in section 11.

Key Takeaways
- The sha256 chain is: `check.py` writes `overview sha256` into `script-checks.md`; `page.py` writes `overview-sha256` into `report.html`; `build_summary` regenerates `summary.md` from the same `overview.md`; `gate` re-computes all three.
- `run.py` itself writes nothing outside `.dev/coordinator/` and runs only `orca automations ...` and `gh issue view`.

## 4. exclude.py (109 lines): Step 4b, leave out what the orchestrator holds

Docstring exclude.py:1-24; `main(run)` 59-103 **[CODE-VERIFIED]**.
- Reads: `entry_files()` (the active `orchestrated/*.json` only), `github-items.json`, `sessions.json`, `coverage.json`. Keeps unreduced copies as `github-items-before-exclude.json` and `sessions-before-exclude.json` on first run (`original`, 51-56) so a rerun gives the same result.
- A GitHub item is a candidate only if `kind == "issue"`, the person (`CONFIG["person"]` = `clayphi`) is among its `assignees`, and its repo was read without error (`readable_repos` 40-48: no `errors`, not `archived`, `issues_enabled`) (65-71).
- For each entry file whose issue url is in that set (73-76) it adds to the removal set: the issue url, the entry's `pr_url`, and `orca://session/<id>` for every id in `entry_session_ids` (78-79). Comparison is lower-case.
- Writes `github-items.json` and `sessions.json` without those urls, and `excluded.json` = sorted list of removed urls (97-99). Prints `N orchestrated issues left out of this run: ...` (100-103).
- An entry whose issue is not shown open and assigned, or whose repo failed to read, excludes nothing (comment 16-20). Entries in `closed/` and `info/` exclude nothing (they are not read: `entry_files()` reads only the folder itself).
- Runs no external command (no `gh`, no `orca`). It writes only inside the run folder.

Key Takeaways
- Whether anything is ever excluded depends entirely on `.dev/coordinator/orchestrated/*.json` files existing. See section 9 for who writes them.

## 5. orca_term.py (133 lines): Orca terminal verbs

Module docstring orca_term.py:1-4 says it is shared by the waker and "FR-26: reused, never copied" **[CODE-VERIFIED]** that waker.py imports it (waker.py:25). Verbs actually run (all via `run_cmd(["orca", *args, "--json"])`, orca_term.py:17-21, default timeout 60s):

| Function | Orca command line | Reads or writes |
|---|---|---|
| `terminals(worktree_path)` 24-31 | `orca terminal list --worktree path:<path> --json` | read; a truncated list raises `CommandError` |
| `screen(handle)` 87-91 | `orca terminal read --terminal <handle> --screen --json` | read |
| `is_idle(handle, wait_ms)` 94-110 | `orca terminal wait --terminal <handle> --for tui-idle --timeout-ms <ms> --json` | read (blocks up to `wait_ms`) |
| `send(handle, text, enter, wait_submit_s)` 124-133 | `orca terminal send --terminal <handle> --text <text> [--enter --wait-submit <s>] --json` | WRITES: types text into a live terminal; returns `{stages, accepted, raw}` |
| `claude_processes()` 34-58 | no Orca call: reads `/proc/<pid>/environ` and `/proc/<pid>/cmdline` for processes whose command ends in `claude`; maps env `ORCA_TERMINAL_HANDLE` to env `CLAUDE_TOPIC` | read (local proc files) |
| `find_session(worktree_path, tag)` 61-70 | uses `terminals` and `claude_processes` | read; returns (live terminals running Claude with `CLAUDE_TOPIC == tag`, newest `lastOutputAt` first; spare connected terminals with no Claude) |
| `typing_or_fresh(term)` 113-121 | uses `screen` | read; unsafe if `draft` has text or last output under `FRESH_OUTPUT_SECONDS` = 60 (14) |

Other verbs used elsewhere in the skill (not in this file): `orca terminal create --worktree path:<ws>` and `orca worktree set --worktree path:<ws> --unread --comment <text>` in waker.py (section 8); `orca automations list|runs` in run.py (section 3); the Orca browser verbs in page.py (section 10). No `orca` command in orca_term.py reads a session's state from Orca (consistent with SKILL.md:38).

Key Takeaways
- The only terminal-writing function is `send`; it is called from waker.py only (to be confirmed by grep in section 8).
- A live coordinator session is identified by the process environment, not by Orca's title (docstring 37-39).

## 6. waker.py (405 lines): find or start the coordinator session, wake line, retries, DM

Usage waker.py:4: `waker.py morning | hourly | check-missed` **[CODE-VERIFIED]** (dispatch 398-405: `morning` and `hourly` call `wake`, `check-missed` calls `check_missed`).

- Wake line (36-38): only `morning`: `Wake (daily report): run /agent-work-report for today's report.`
- `hourly` (216-220): writes a wake record `SKIPPED: there is no hourly check ...`; no session contact.
- `local_gate(mode)` 45-63: uses `CONFIG["timezone"]` (America/Chicago). Skips on a non-report day (`report_days`), skips `morning` before `daily_run_local` hour (07), skips `morning` if a daily run folder already started today (`daily_run_started` 66-78), skips `check-missed` unless the local hour is `missed_run_dm_local` (09).
- `wake(mode)` 214-260: record = `{mode, workspace}`; retries `HOLD_RETRIES` = 15 times with `HOLD_WAIT_S` = 120 s between (39-42), i.e. 30 minutes, only for `morning` (232); a stuck run lock (older than the budget, `stuck_run` 116-124) adds a `DM_NEEDED` note but the wake still goes out (225-231). After the retries a `HOLD` becomes `DM_NEEDED: today's report did not start after ...` (250-256).
- `try_wake` 263-338, one attempt:
  1. On a retry, if a daily run opened meanwhile, outcome `SENT` (265-272).
  2. `orca_term.find_session(workspace_path(), "coordinator")` (273). None live: `start_session` (275), which reuses a spare terminal whose last screen line contains "Session name" and nobody is typing (171-184), else `orca terminal create --worktree path:<workspace>` (186-189), waits up to `SHELL_WAIT_S` = 30 s for the name question or a shell prompt (194-199), then types the tag (name question) or `ccsession coordinator` (a shell) with Enter (201-202) and waits up to `START_WAIT_S` = 120 s until Claude runs there (203-210). If the new session is not idle in 90 s: `HOLD` (278-279).
  3. One live: use the newest (`live[0]`), list the others as `other_live_sessions` (282-286); `HOLD` if someone is typing or output is fresh (287-289) or the session is busy (290-291).
  4. `morning` only: sends `/clear` (297), `HOLD` if not idle in 30 s (299-300).
  5. Sends the wake line (302) and stores the receipt. A non-morning mode needs `turn_started` in the stages (305-313) (not reachable today: only `morning` is in `WAKE_LINES`, and `hourly` returns earlier).
  6. For `morning`, `SENT` only when a run folder opened since the send (`run_opened_since`, 127-137, `RUN_WAIT_S` = 120 s); otherwise reads the screen for an error (`ERROR_LINE` 146: API Error, 429, usage limit, out of usage, rate limit) and returns `HOLD` (turn started) or `DM_NEEDED` (no turn) (322-338).
- `check_missed()` 371-395: if no non-hourly run has a `complete.json` finished today (local) it records `DM_NEEDED: no daily report has finished today (<date>) by 09:00; <why_missed>`; else `OK: today's report finished (<run>)`. `why_missed` 341-368 reads `wakes/*-morning.json` for today, the run folder state and the coordinator screen error.
- `record(rec, final)` 102-113: writes `<state>/wakes/<time>-<mode>.json`; on the final write, an outcome starting `DM_NEEDED` is sent by `notify` and the result put in `rec["notified"]` (109-110). The last printed line is the outcome (113).
- `notify(text)` 81-99: first `clickup.send_dm("Coordinator: <text>")`; if that fails, `orca worktree set --worktree path:<repo> --unread --comment "Coordinator: <text>"[:500]` (Orca unread mark with a note); if that fails too it says so in the record.

What waker.py WRITES (summary): wake records under `.dev/coordinator/wakes/`; text typed into the coordinator's Orca terminal (`/clear`, the wake line, `ccsession coordinator`, the session name); a new Orca terminal; a ClickUp DM; an Orca workspace unread mark and comment. **[CODE-VERIFIED]**. Boundary tension with SKILL.md:194 ("never ... starts or messages agents"): the waker starts and messages the coordinator session only, not workers; recorded in Gaps.

Triggers: nothing in the skill schedules `waker.py`. The Orca automations that call it (SKILL.md:30-35) live outside the repo: **[UNVERIFIED]**. `hourly` mode exists in code but is stated to be unused (waker.py:8-9).

Key Takeaways
- The waker is a session-management script for ONE session (the `coordinator` ccsession tag in the orchestrator repo's worktree), not a worker dispatcher.
- Success of the morning wake is defined by a run folder appearing, not by Orca's delivery receipt.

## 7. clickup.py (642 lines): ClickUp reads and the only ClickUp write (the DM)

Usage clickup.py:4-6: `clickup.py <run>` (read) and `clickup.py dm <run> <message_file>` (send); dispatch 635-642 **[CODE-VERIFIED]**.

HTTP layer (`call`, 58-105): `urllib.request` against `API = https://api.clickup.com/api` (39); header `Authorization: <CLICKUP_API_TOKEN>`; no token raises `ClickUpError` (60-64). GET retries up to 3 times on 5xx or connection errors with backoff; POST is never retried (66-68); a 429 waits for `X-RateLimit-Reset` up to 65 s and retries (82-85, 108-113); at most 6 attempts. Limits: `MAX_TASK_PAGES` 200, `MAX_COMMENT_CALLS` 400, `ACTIVE_DAYS` 30, `FIRST_RUN_DAYS` 1, `OVERLAP_MS` 10 minutes (40-44).

Calls it makes (READ, GET): `/v2/user` (131); `/v2/team` (133, 139); `/v2/team/{team}/task?include_closed=false&subtasks=true&page=n` and `...include_closed=true&subtasks=true&date_updated_gt=<ms>` (153, 418, 426); `/v2/team/{team}/space?archived=false` (431); `/v2/task/{id}/comment` (170); `/v2/comment/{id}/reply` (211); `/v3/workspaces/{team}/chat/channels?limit=100&with_message_since=<ms>` (230); `.../chat/channels/{id}/messages?limit=100` (246); `.../chat/messages/{id}/replies?limit=100` (266); the DM channel's messages (579).

WRITES to ClickUp (POST), only in `send_dm` (596-613): `/v3/workspaces/{team}/chat/channels/direct_message` with body `{}` (creates or returns the token owner's self DM, 601) then `/v3/workspaces/{team}/chat/channels/{cid}/messages` with `{type: "message", content: <text>, content_format: "text/md"}` (603-607). These are the only ClickUp writes in the skill. Callers: `dm()` (629) and `waker.notify` (waker.py:84).

Local writes: run folder `clickup-items.json`, `clickup-events.json` (`{comments: {url: [...]}, chat: [...]}`), `clickup-gone.json` (url to reason), `clickup-status.json`, `clickup-replies.json` (550-557, 574, 589-592), and `clickup-dm.json` from `dm()` (625-630); state folder `settings.json` keys `clickup_user_id`, `clickup_workspaces` (558-563) and `clickup_dm_channel` (610-612).

Selection rule (main 394-567): open tasks (not `date_closed`, status type not done/closed; `finished` 116-120). `mine` = assigned to the token owner, or created by them with nobody assigned (436-443, 452). `watched` = watcher and neither of those, kept only when updated or mentioned (444-449, 465). Tasks of `mine` with `date_updated` older than 30 days are "quiet" and only counted (468-482, `status.parts.quiet`). `keep = (mine - quiet) | watched | (mentioned and open)` (474-476). Replies in the helper's self DM since the previous report are read, minus text starting with `NOTICE_PREFIXES` ("# Today's work report", "Coordinator:", "Coordinator test:", 47, 583-588).

`dm()` 616-632 **[CODE-VERIFIED]**: imports `run` as `runmod` and calls `runmod.deliverable(run)` (the full gate: checks and sha, page built from the sheet, summary equal to the script's); refuses any file other than `<run>/summary.md` (620-621); on refusal writes `clickup-dm.json {sent: false, detail: "blocked: ..."}` and exits (625-628). So for the DM, SKILL.md:183 is accurate; for `run.py close` only the checks-and-sha part is enforced (section 3).

Key Takeaways
- ClickUp is read-only except the self-DM; no task, comment or status is ever written.
- The token owner's own DM channel is the notice channel; the ClickUp DM is also how `waker.py` reaches Clay.

## 8. collect.py (317 lines): GitHub collection (two orgs, Projects, "involves" search)

Docstring collect.py:1-13; `main(run)` 223-311 **[CODE-VERIFIED]**. All commands are read-only `gh` calls through `gh_json` (list args, no shell). Orgs come from `config.json` (`IronbellyOrg`, `IronbellyGroup`); none of these calls names `--repo IronbellyOrg/IronClaude` because they sweep every repo of both orgs. No SuperClaude-Org target appears.

| Command (collect.py line) | Purpose |
|---|---|
| `gh repo list <org> --limit 1000 --json name,isArchived,hasIssuesEnabled` (236-244) | repo inventory per org; archived repos recorded and skipped (256-266); `excluded_repos` (empty in config.json) skipped (252) |
| `gh issue list --repo <org>/<repo> --state open --limit 1000 --json number,title,author,assignees,labels,createdAt,updatedAt,url,comments,body` (127-138, fields 22-24) | open issues, only if `hasIssuesEnabled` (123-124) |
| `gh pr list --repo <org>/<repo> --state open --limit 1000 --json <issue fields>,isDraft,reviewRequests,closingIssuesReferences,headRefName,isCrossRepository` (fields 25-28) | open pull requests |
| `gh project list --owner <org> --limit 100 --format json` (156-158) | Projects boards (closed ones skipped, 162) |
| `gh project item-list <n> --owner <org> --limit 1000 --format json` (165-175) | board status and priority per item url |
| `gh search issues --owner <org> --involves <person> --state open --limit 1000 --json url` and the same with `--include-prs` (203-218) | the "involves Clay" set |

Repos are read by a `ThreadPoolExecutor(max_workers=8)` (267-270). Each failure becomes an `errors` entry in `coverage.json` or `source_errors`, never fatal (140-141, 245-247, 277-278).

Record shape per item (`record` 85-116): `org, repo, kind (issue|pr), number, title, url, author, assignees, labels, created, updated, comments (count), priority_mentions, draft, review_requests, closes, branch, cross_repo, clickup_refs`; main adds `boards` and `involves_person` (279-281). `priority_mentions` (49-72) keeps, per matching line of the body or a comment, `{by, date, where, level, line[:200]}` using `PRIORITY_LINE` (39-42). `clickup_refs` (75-82) finds `CU-<id>`, `app.clickup.com/t/...` and `#<id>` forms. NOTE: the docstring says the body "is not kept" (12); the code keeps only priority lines (200 characters) and ClickUp ids from it.

Writes (run folder only): `github-items.json` (sorted by url), `coverage.json` `{repos, boards, source_errors}`, and appended lines under `## Sources read` in `run-log.md` (284-307).

Key Takeaways
- `coverage.json` is what `exclude.py` uses to decide a repo was read without error.
- Collection is org-wide and not limited to IronClaude; it needs no `--repo` flag.

## 9. sessions.py (444 lines): Orca terminals, hook file and transcripts

Docstring sessions.py:1-20; `main(run)` 278-438 **[CODE-VERIFIED]**.

Inputs and commands:
- Orca's agent hook file `~/.config/orca/agent-hooks/last-status.json` (override `AWR_HOOK_FILE`; `HOOK_FILE` 42-46), must be `version == 2` (282); entries keyed `"<tabId>:<leafId>"` give `providerSession.id` (Claude session id) and `providerSession.transcriptPath` (327-329). If missing, `sessions.json` is `[]` and `sessions-status.json` `{read: false, reason}` (283-289).
- `orca terminal list --json` (291, via `orca_term.orca`); a truncated list means "not read" (300-306).
- `orca worktree list --json` (309-312) for each worktree's `linkedIssue` and `linkedPR` (368-369); failure only loses those links (313-317).
- `claude_processes()` (99, = `orca_term.claude_processes`, reads /proc) gives `CLAUDE_TOPIC`; fallback session id from the tag file `~/.claude/projects/*/topics/<tag>.txt` (`tag_session` 109-114; `PROJECTS` 47, override `AWR_PROJECTS`).
- `git -C <worktree path> remote get-url origin` (`git_repo` 117-128, timeout 10 s).
- Transcripts: `~/.claude/projects/*/<session id>.jsonl` (`find_transcript` 102-106) read from the previous report's `read_offset` (first report: the last 24 hours, at most the last 30 MB: `FIRST_WINDOW_HOURS` and `FIRST_READ_BYTES`, sessions.py:48-49). A partial last line is left for the next read (175-176). Sidechain events are skipped (185).
- Terminals whose `worktreePath` equals `workspace_path()` (the coordinator's own) are skipped (325-326).

It reads, and never writes, Orca and the transcripts. It writes `sessions.json` and `sessions-status.json` in the run folder only (424-434).

Facts extracted per session into `since_previous_report` (`extract` 141-275): `events, first_event, last_event, prompts[-10:] (800 chars each), replies[-5:] (last 600 chars each), tools (top 15), files_written (Write, Edit, NotebookEdit, MultiEdit; first 50), commands[-20:] (git commit/push/merge/checkout -b/switch -c/branch and gh pr/issue/release, regex 51-53), errors[-5:], error_count, repeated_steps (same tool and input 3 or more times, up to 10), ends_on_question (last role assistant and a "?" in the last 400 characters), last_turn (reply|tool|prompt), pending_tool_call (last tool call with no result when the last role is tool), prompt_urls, item_urls, title`.

Session record fields: `session_id, handle, terminal_title, tag, title (tag, else Claude title, else first prompt 80 chars), worktree, branch, repo, linked_issue, linked_pr, terminal_open, claude_running, transcript, read_offset, events_total, since_previous_report, last_event, prompt_urls_all` (348-376, 401-407). A session from the previous report whose terminal is gone is kept (read on) until a report called it `done` (378-400). A session with no new events keeps its earlier `ends_on_question`, `pending_tool_call`, `last_turn` and gets `state_from_earlier: true` (408-422).

Key Takeaways
- The script produces facts only. The six statuses are written by the model from these facts (section 14).
- Orca's own state vocabulary for a session is not read (consistent with SKILL.md:38).

## 10. page.py (387 lines): report.html, notes.json, local server, Orca browser tab

`main(run)` 226-305 builds the page; `--open` calls `open_tab` 345-378 **[CODE-VERIFIED]** (dispatch 381-387).

Build: reads `overview.md`, `run.json`, `classified.json`, `compare.json`, `items.json`, `snapshot.json`, `to-write.json`; writes `<run>/notes.json` (each listed item's written parts with `as_of`, 246-256), `<run>/report.html` (template `templates/report-template.html` with `__OVERVIEW_SHA256__`, `__DATA__` JSON blob and `__SCRIPT__` = `templates/report.js` substituted, 292-300) and copies it to `.dev/coordinator/report.html` (301). The sha256 of `overview.md` goes into the `<meta name="overview-sha256">` tag that `run.py page_ok` checks. Links other than `http(s)://` and `orca://` are rendered as plain text (`md` 61-77, `SAFE_URL` 57).

Server `ensure_server()` 308-342: if `http://127.0.0.1:8765/report.html` does not answer, starts a detached `sys.executable -m http.server 8765 --bind 127.0.0.1 --directory <.dev/coordinator>` (318-333), waits up to about 10 s. WRITES nothing, but it serves the WHOLE `.dev/coordinator/` folder (run folders, `settings.json`, `action-log.jsonl`, `priorities.json`, entry files) to any local process on the machine, not only `report.html`: observation from the `--directory` argument, not a stated design choice. It invokes `python -m http.server` in a skill script (the repo's own UV-only rule governs repo work; this script runs under the system `python3`, per common.py:32-34).

Orca browser verbs in `open_tab` (all `orca <verb> ... --json` via `orca_term.orca`): `orca tab list --worktree path:<repo>` (354); `orca tab close --page <browserPageId>` for stale and extra copies (361, 364); `orca tab switch --page <id>` (366); `orca eval --page <id> --expression location.reload()` (369-375); `orca tab create --url http://127.0.0.1:8765/report.html --worktree path:<repo>` (377). The tab is recognised by its url (`REPORT_URL`, or the `file://` url of the old location); there is no tab title in the code, the name "Your Work Report" is only in the print and docs.

Key Takeaways
- This is the only place the skill writes to Orca's browser, and the only long-lived process it starts (the http.server).
- Page content is the model's written text plus run-file facts; nothing on the page is fetched live (the data is embedded JSON).

## 11. check.py (350 lines): the seven script checks

`main(run, links=False)` check.py:168-343 **[CODE-VERIFIED]**; exit 1 if any check fails; writes `<run>/script-checks.md` as a table `| Check | Result | Detail |` plus `overview sha256: <sha>` (338-341).

| Check | What it verifies (check.py lines) |
|---|---|
| placeholders | no `{{...}}` slot, no `<!-- judge each` comment, no `RF_UPDATE` marker (175-183) |
| template | every item in groups assigned, owned, opened, inprogress (`MINE` 52) follows `template_problems` (72-135): linked identifier heading, a State in `STATES`, a Next line, priority set or `Suggested <level>` with a reason, the 11 sections in order and non-empty, capital-letter lines, bullet-only done/todo/happened |
| sessions | every `](orca://session/...)` line that starts with 2-space-dash ends with `status: <one of 6>: <reason>` (`STATUS_OK` 53, 196-209) |
| carry-forward | every group-MINE item in the previous `snapshot.json` is listed, closed, counted as quiet, or in `excluded.json` (211-237) |
| needs-you | exactly the sessions with status "waiting on you" have an entry, both ways (240-270); each entry follows `needs_problems` (138-165) |
| candidates | every `candidate` item has a "likely yours/not yours, because" line ending `Priority: <level> (set)` or `(suggested)` (272-308) |
| links | only with `--links`: `gh pr view <url> --json number` or `gh issue view <url> --json number` for every GitHub link not marked "(dead link)" (310-336) |

Commands run: only `gh pr|issue view <url> --json number` (317-326), read-only, timeout 30 s.

`template_problems(url, block, orchestrated=False)` 72-135: with `orchestrated=True` a "Needs you" part that is not "N/A" must also contain the three `ESCALATION_LINES` (127-134). The docstring (77-80) says the orchestrator's `report-entry` verb checks with it. Whether any caller passes `orchestrated=True` is checked in section 13.

Key Takeaways
- The delivery gate depends on `link` being PASS (run.py `REQUIRED_CHECKS`); a run without `--links` cannot pass the gate.
- No model or network judgement is used; only the `gh ... view` reachability test touches the network.

## 12. activity.py (279 lines) and render.py (626 lines): evidence file and writing sheet

### activity.py (Step 8) **[CODE-VERIFIED]**
- Commands (read-only `gh`, via `gh_json`): `gh api --paginate --slurp repos/<org>/<repo>/issues/<n>/timeline?per_page=100` (activity.py:71-76) and, for pull requests, `gh pr view <url> --json mergeable,isDraft,reviewDecision,statusCheckRollup` (122-128). Six worker threads (225).
- Targets: items in `to-write.json` plus candidates that are new or changed (191-199). At most `MAX_EVENTS` = 8 events per item, `BODY` = 600 characters; noisy events skipped (`SKIP` 24-34: subscribed, mentioned, labeled, project moves ...).
- Everything other people or sessions wrote is emitted only as a `> ` quoted line with control characters removed (`clean`, `quote` 40-54): data, never instruction.
- Session lines (157-175) carry: Claude running or not, event count since the previous report, last activity, title and branch, the last 3 prompts, the last reply, the last 2 errors, and a "stopped on a <tool> call with no result since <time>" line from `pending_tool_call`. They do NOT print `ends_on_question`, `repeated_steps` or `error_count`; the model sees the quoted last reply and errors instead.
- Writes `activity.md` (head, per-item sections, "Priority lines in the text or comments of items with no priority set", "ClickUp messages to you").

### render.py (Step 9) **[CODE-VERIFIED]**
- `main(run)` 392-620 stubs `overview.md` from `templates/overview-template.md`; it exits if `overview.md` already exists (395-396). It builds the count table, items by priority (`by_priority` 465-489), carried "Needs you" entries (`still_waiting` 331-351: only entries led by an `orca://session/` link, not answered since the previous run's start, not excluded, not closed), closed lines, "Not checked" lines (`not_checked_lines` 354-389; always ends with `NOT_ASKED`), header notices (`missed` 306-328: stuck run replaced, missed report days; plus "Two coordinator sessions are running" from `wake-records.json` `other_live_sessions`, 552-563).
- Session statuses in the stub (`entry` 242-252): a session with `carried` set keeps its last status plus the note ` (kept as it was: sessions not read this run)`; an item that is new or changed gets the slot `{{RF_PLACEHOLDER:status:<session id>}}` for the model; an unchanged item's session gets `carried_status` (172-176): the previous status if it started with `waiting on you` or `done`, else `stalled: no activity after <time>, and its work is not reported done`. So for an unchanged item the status is set by script, not by the model.
- `entry(url, it, c, cmp_, ctx, filed=None)` 194-303 is also the renderer for an orchestrator entry file when `filed` is given (called from `run.py _refresh`, run.py:775): every written part in `WRITTEN` comes from the entry file or "N/A" (219-220); each session's status comes from the file's `session_status` map, else `stalled: the entry file has no status for this session` (221-227); the worker's `pr_url` becomes a line "the worker's pull request" (229-231); the header gets `**Orchestrator:** [<tag or id>](<link>) (<tier>)` or `none recorded` (`filed_orchestrator` 179-191); a suggested priority and its reason come from `suggested` and `priority_why` (256-258); no update marker and no placeholder is left (298: marker only when `filed is None`).

Key Takeaways
- `render.entry(..., filed=)` is the only code that turns an entry-file JSON into card text; the JSON field names it reads are exactly the `WRITTEN` slot names plus `session_status`, `pr_url`, `orchestrator`, `priority_why`, `suggested`.
- Statuses of unchanged sessions are a script rule; statuses of changed sessions are the model's judgement.

## 13. classify.py (147 lines), compare.py (197 lines), prefs.py (64 lines)

### classify.py (Step 6) **[CODE-VERIFIED]**
- Groups in fixed order `GROUP_ORDER` = assigned, owned, opened, inprogress, candidate, other (classify.py:28). `rule()` 67-83: assigned (person in `assignees`, or in `review_requests`); owned (the person wrote a pull request with no assignees, or an open PR by the person closes the issue); opened (the person is author and nobody assigned); candidate (`involves_person` or `mentions_you`); else other. A session on no item is `inprogress` (94-99); an item with a session on it is at least `owned` (106-107); a ClickUp task under an item counts toward the item's group (101-105); the best (lowest index) option wins (108).
- Priority (31-64): `priorities.json` override, then board priority of the item or its ClickUp tasks, then labels from `config.json` `priority_labels`, then the person's own level in the item text or a comment (`priority_mentions` by the person, latest wins), else `Unset`. Order: priority, `created`, url (121-128).
- Reads `items.json` and `.dev/coordinator/priorities.json`; writes `classified.json` `{order, items{url: {group, why, priority, priority_source}}, counts}`. No external command.

### compare.py (Step 7) **[CODE-VERIFIED]**
- `TRACKED` (27-39): title, updated, comments, assignees, labels, draft, board_status, group, priority, clickup_tasks, agent_sessions. Writes `snapshot.json` (the tracked fields plus `kind`, `source`, `last_activity`, `carried`) and `compare.json` `{previous_run, new, changed{url: {field: {was, now}}}, closed{url: {reason, title, group}}, unchanged, carried}`.
- Drops the urls in `excluded.json` from the previous snapshot first (128-131), so an excluded item is neither new, changed, carried nor closed.
- An item missing now is closed only by evidence: `gh issue|pr view <url> --json state,closedAt[,mergedAt]` (`lookup_closed` 84-105; read-only); "HTTP 404", "HTTP 410" or "Could not resolve to" give "no longer visible"; any other error carries the item (FR-19). Items in a repo or org that failed to read are carried without a lookup (166-169, `unread_prefixes` 108-118). A ClickUp task closes with `clickup-gone.json`'s reason; an agent session missing from a good read is "its agent session's work was reported done" (175-176).
- It imports `latest_completed` from `run.py` (25); `compare.py` therefore pulls in `run.py`'s module (and, through run.py's imports, `common.py`).

### prefs.py **[CODE-VERIFIED]**
- `prefs.py priority <run> <item url> <Urgent|High|Medium|Low|clear>` reads the person's words from stdin, writes `.dev/coordinator/priorities.json` and logs `priority-change` (35-47). `prefs.py answer <run> <url|-> <session|clickup-dm>` logs `answer` only (50-54); `render.still_waiting` and `common.answered_since` read those log rows to stop carrying a "Needs you" entry. `check_url` accepts only `https://github.com/...` or `https://app.clickup.com/...` (20), so an `orca://session/...` url is NOT accepted by `prefs.py answer`, although SKILL.md:172 says to use "`prefs.py answer <run> <session url> session`" with an Orca session url as the argument. **[CODE-CONTRADICTED]** (see Gaps).

Key Takeaways
- Nothing in these three scripts calls Orca or ClickUp; compare.py and check.py are the two extra `gh` readers besides collect.py and activity.py.

## 14. match.py (283 lines): Step 5, join items

**[CODE-VERIFIED]** Reads `github-items.json`, `clickup-items.json`, `sessions.json`; writes `items.json` and `merged-into.json`. No external command.
- ClickUp task to GitHub item (match.py:119-148): a GitHub url in the task's `github_links`, or the task id named by an item's `clickup_refs`. A task matching several items is listed under the first by url; the others are named.
- Session to item (191-247), in this order: the Orca workspace's `linked_pr` / `linked_issue` (195-204); a pull request open on the session's branch (not a fork's, not main/master/develop/dev: `prs_by_branch` 183-190, `SHARED_BRANCHES` 36); an issue or PR number at the start of a branch part (`BRANCH_NUMBER` 32, 210-220); a ClickUp id in the branch (`BRANCH_CU` 34, 221-230); else the single item named in the prompts it was given (231-240). No match: the session becomes its own item `orca://session/<id>` in group `inprogress` (`session_item` 80-106, 245-247).
- A source not read keeps the previous report's tasks or sessions marked `carried` (159-176, 249-268); urls in `excluded.json` are not restored (158, 263).
- Sessions excluded by `exclude.py` are already absent from `sessions.json`, so the held issue's worker and orchestrator sessions never get a card from the daily run.

## 15. Who writes the living-report entry files (R5 capability check)

Declaring lines (DOC):
- SKILL.md:16 "The orchestrator keeps one entry file per issue it holds in `.dev/coordinator/orchestrated/` (added at claim, updated at milestones, moved to `orchestrated/closed/` at close ...)".
- common.py:133-137 "`superclaude orchestrator report-entry` writes them; this skill reads them (exclude.py, run.py refresh, render.py entry) and moves a closed one (run.py refresh)."
- check.py:77-80 `template_problems(..., orchestrated=True)` "its `report-entry` verb checks with it".
- run.py:688-689 "`report-entry --closed` moved it".
- tests/skills/test_agent_work_report.py:2856 "PR B's `report-entry` writes the same shape."

Code evidence in the snapshot (origin/master 61ac2c2e6):
- `Grep orchestrated|coordinator/|\.dev/coordinator` over `src/` finds only the 11 files of the agent-work-report skill (check.py, classify.py, common.py, exclude.py, page.py, prefs.py, render.py, run.py, waker.py, SKILL.md, item-template.md). No file outside the skill writes into `.dev/coordinator/orchestrated/`.
- `Grep report-entry|report_entry` over the snapshot (excluding docs/designs) finds only: the skill's comments above; `src/superclaude/skills/sc-closeout-protocol/SKILL.md:21`; `src/superclaude/skills/sc-closeout-protocol/refs/settle.md:99`; `src/superclaude/skills/sc-closeout-protocol/scripts/settle.sh:1037,1042`; tests (a fake `report-entry` in tests/skills/test_closeout_protocol.py:397-399, 2675; the entry fixture in test_agent_work_report.py:2856-2870). No Python or shell implementation of the verb.
- `src/superclaude/cli/main.py` has no match for `orchestrat`; the only file named `orchestrator*` under `src/` is `src/superclaude/cli/eval/orchestrator.py` (the eval runner, unrelated). The `superclaude orchestrator` command group is absent. **[CODE-CONTRADICTED]** for the common.py:136 claim as a statement of current state; it is design-only.
- sc-closeout's own text says so: refs/settle.md:99 "The command does not exist in this repository, so the entry item is `escalated why=surface_absent` until it does" and settle.sh:1037-1040 probes `superclaude orchestrator report-entry --help` and prints `ENTRY escalated key=<k> why=surface_absent` (exit 1) when it fails.
- `/sc:orchestrator` itself: no command or skill of that name was found by the greps above under `src/` (the only `orchestrat*` skill-side hits are listed; none define it). Marked **[UNVERIFIED]** beyond that grep.

On-record scope decision: docs/designs/orchestrator.md (read in section 17) states the entry writer is PR B (`report-entry` in the orchestrator package) and the skill is PR C. That is a design-document statement of sequencing; the cited decision list for it is in section 17. Consequence for the capability: `exclude.py`, `run.py refresh` (the `held_entries` path), `render.entry(filed=...)` and `check.template_problems(orchestrated=True)` are reachable only if something creates files in `orchestrated/`; today only the tests do. Run on a real checkout, `exclude.py` excludes nothing and `refresh` renders no "Held by the orchestrator" block, but `refresh` still builds the shared page from the last daily report.

DEFECT-CANDIDATE (R5): capability "living report: the orchestrator's entry files appear on the shared page and are left out of the daily run" is declared as shipped by SKILL.md:14-16 and Step 4b (SKILL.md:115-116) and wired at the reader side (run.py:629-840, exclude.py:59-103), but the writer (`superclaude orchestrator report-entry`) has no code in the snapshot. Remediation task not created (read-only brief); flagged for the owner. The sequencing statement in the design (section 17) is the closest on-record decision; whether it counts as a cited scope decision that the capability is deliberately out of this PR is for the owner.

Orchestrator PRs after 61ac2c2e6: section 18.

## 16. Where `orchestrator_repo` is read and who sets it (SKILL.md:14 claim)

- Reader: common.py:38-51 (the only code that reads the key; also tests/skills/test_agent_work_report.py:2979-3000). **[CODE-VERIFIED]**
- `Grep orchestrator_repo` over the whole snapshot: matches only CHANGELOG.md:9, docs/designs/orchestrator.md (269, 308, 338, 372, 374), docs/designs/sc-closeout.md:361, SKILL.md:14, common.py (22, 30, 40, 43, 48) and the test file. Nothing in `src/superclaude/cli/issue_watch/` reads or sets it. **[CODE-VERIFIED]**
- The poll's configuration loader REJECTS it today: `_TOP_KEYS` in src/superclaude/cli/issue_watch/cycle.py:58-69 is {schema_version, enabled, labels, project_id, owner_account_id, worktree, approvers_file, state_dir}; cycle.py:216-220 raises `_invalid("unknown configuration key: ...")` for any other top-level key. So adding `orchestrator_repo` to `~/.config/superclaude/issue-watch.json` (as common.py:25 and SKILL.md:14 direct) would make the poll refuse its configuration file. `_DEFAULT_CONFIG` is `~/.config/superclaude/issue-watch.json` (cli.py:31). **[CODE-CONTRADICTED]** between SKILL.md:14 and cycle.py:216. (Whether the same file is meant to carry the key is the design's plan: docs/designs/orchestrator.md:269 and :372 list `orchestrator_repo` as a key the poll's reshape adds; see section 17.)
- Who sets it: **[UNVERIFIED]**. The design says an installer or the owner sets it (to be confirmed in section 17); no code in the snapshot writes the file. Alternative path that works today: `$AWR_ROOT` (common.py:35-37).

Key Takeaways
- Today the coordinator state folder is reachable only with `AWR_ROOT` set; the documented `orchestrator_repo` route is blocked by the poll's own strict key check.
- The reader side of the living report is built and tested; the writer is not in the snapshot.

## 17. Relationship to the orchestrator design (docs/designs/orchestrator.md, snapshot copy)

Paths are `docs/designs/orchestrator.md` in the snapshot (also on master: PR #681, merge c2a1395522239429dd21f19cadd206fd643fec03, merged 2026-11-20T00:02:33Z). The design says it is "approved by the owner (ruling 37, 2026-11-19)" (section 8.2 table row "This design"). It is a design, not code: it holds no implementation of the skill; the skill is PR C.

What the design says about this skill, checked against code:
- **DQ12** (orchestrator.md line 122): the report session (tag `coordinator`) runs `/agent-work-report`; orchestrators (tag `orchestrator-<short>-<n>`) run `/sc:orchestrator`; the orchestrator writes `.dev/coordinator/orchestrated/<owner>__<repo>__<N>.json` "using the slot names of `item_written`"; PR C moves the folder, changes `repo_root()` to `$AWR_ROOT` or the orchestrator repo path and drops the `workspace` key; adds `exclude.py` between Steps 4 and 5; `compare.py` and `check.py` skip `excluded.json`; `run.py refresh` with reconcile and prune; Step 12 ends with `run.py refresh --run <run>`.
  - `repo_root()` change **[CODE-VERIFIED]** common.py:28-51; no `workspace` key **[CODE-VERIFIED]** config.json (no such key) and test_agent_work_report.py:3005 `test_the_config_has_no_workspace_key_and_no_script_reads_one`.
  - `exclude.py` between Steps 4 and 5 **[CODE-VERIFIED]** SKILL.md:115-116 and exclude.py; `compare.py` skips excluded **[CODE-VERIFIED]** compare.py:128-131; `check.py` carry-forward skips excluded **[CODE-VERIFIED]** check.py:222-228.
  - `run.py refresh` reconcile (`gh issue view <N> --repo <R> --json state,stateReason,assignees`), prune by `info_ttl_days` 14, build the shared page with `page.main`, never write `<run>/report.html`, do nothing while a daily run holds the lock when called without `--run` **[CODE-VERIFIED]** run.py:491-527, 530-539, 443-452, 649-653, 807-832. The `refresh.lock` (exclusive `flock`, run.py:637-641) is an addition beyond the DQ12 text.
  - Step 12 ends with `run.py refresh --run <run>` **[CODE-VERIFIED]** SKILL.md:152.
  - Design U-items marked it UNVERIFIED before PR C existed ("the `refresh` verb, `exclude.py` and the ClickUp re-homing are UNVERIFIED, section 12"); the code now exists and is tested (section 19).
- **Section 6.4** table of readers: matches the code above (`exclude.py`, `compare.py`, `check.py`, `render.entry(filed=)`, `run.py refresh`) **[CODE-VERIFIED]** with shifted line numbers (the design read the IronFlow copy; for example `render.entry` is at render.py:194-303 here, 126-174 there).
- **Section 5.4** (orchestrator.md:648) `templates/report-entry-update.md` "follows `item-template.md` part for part" and adds a header block (`Follow-up state`, `Human assignee`, `Orchestrator`, `Agent session`, `PR and CI state`, `Last update`, `Kind`). The JSON entry file field names in common.py:139-149 are different from that header block (JSON keys `state, next, what, ...`, `orchestrator{...}`, `worker{...}`, `pr_url`, `last_update`, `closed_at`, `close_reason`; no `Follow-up state`, `Kind` or `Human assignee` header as text). `human_assignee` and `kind` appear in the JSON contract (common.py:141-142), `Follow-up state` does not. Whether the writer will write the markdown template or the JSON file is the design's PR B; no code exists. **[UNVERIFIED]** how they reconcile.
- **Section 8.1** row PR C: files, `config.json`, 15 scripts, 7 templates; test file moved and repointed (U13). Code: scripts are 16 files (the list in the brief names 16: run, common, collect, clickup, sessions, orca_term, exclude, match, classify, compare, activity, render, check, page, prefs, waker); the design counts 15 before `exclude.py` was added **[CODE-VERIFIED]** by the Glob in section 0. Templates are 7 files **[CODE-VERIFIED]**.
- **Section 8.1** row PR B: "orchestrator skill, one PR": `src/superclaude/commands/orchestrator.md`, `src/superclaude/skills/sc-orchestrator-protocol/`, `src/superclaude/cli/orchestrator/` registered in `main.py`, and the `superclaude orchestrator` verbs listed in ADD6 (`wake-check`, `wake-ack`, `state`, `merge-gate`, `lease`, `repos`, `escalate`, `answer-check`, `audit`, `handback`). ADD6 (orchestrator.md:140) lists the verbs `wake-check`, `wake-ack`, `state`, `merge-gate`, `lease`, `repos`, `escalate`, `answer-check`, `audit`, `handback` and does NOT list `report-entry` or `plan-check`; the package row of section 5.1 (orchestrator.md:510) lists `wake-check, wake-ack, state, lease, merge-gate, plan-check, repos, report-entry, escalate, answer-check, audit, handback`. So `report-entry` is named in the design's 5.1 package row and in the report skill and sc-closeout code (common.py:136, check.py:77, run.py:688, settle.sh:1037), but not in ADD6's list. This is an internal inconsistency of the design text (ADD6 versus 5.1), not a code contradiction; the verb itself exists in neither. The design also names the closeout contract: sc-closeout.md:66 (D10) "The work report entry is settled only through `superclaude orchestrator report-entry --key <key> --closed`. Where that command is absent the entry item is `escalated`", and sc-closeout.md:368 "(today, and until the orchestrator's pull requests land)".
- **Section 8.2**: order D, A, P, then B (opens after A merges), C waits for O1 (create the orchestrator repo), live test, PR E, shadow run, switch-on. PR C has merged (#684) before A and B.
- **Section 1.1** the system diagram says "Orca automation (every 5 min, precheck only, no agent)" and "orchestrator session ... `/sc:orchestrator`". `/sc:orchestrator` **[UNVERIFIED]**: not in the snapshot (no `src/superclaude/commands/orchestrator.md` found by the greps; the Glob in section 15 found only the eval orchestrator).

Key Takeaways
- The design assigns the living report's reader side to PR C (built, merged) and its writer to PR B (not in the snapshot, no PR open).
- The design itself says DQ12's refresh, exclude and ClickUp re-homing were UNVERIFIED by a run; code and tests now exist, but no live run is recorded in this research.

## 18. Orchestrator pull requests (read-only `gh`, `--repo IronbellyOrg/IronClaude`, run 2026-11-20)

Snapshot commit 61ac2c2e6effc24baa5ccef2a71a0a08d85bd5cd is "feat(reflect): grade a spec behaviour the plan lets slip as Blocking (issue 552, stage 3c) (#688)", committed 2026-11-19T21:26:01-05:00 (= 2026-11-20T02:26:01Z). `gh pr list ... --search "orchestrator"` and `--search "issue 655"` and `--search "report-entry"` give these 655-family PRs:

| PR | Title (short) | State | Merged (UTC) | Merge commit | In the snapshot |
|---|---|---|---|---|---|
| #681 | docs(design): approved orchestrator design (docs only) | MERGED | 2026-11-20T00:02:33Z | c2a1395522239429dd21f19cadd206fd643fec03 | yes (docs/designs/orchestrator.md exists) |
| #682 | PR D: retire the old plan-approval gate | MERGED | 2026-11-20T00:02:36Z | 01e7a9e23519fd54bc438bb1a1a0e03dcdae5baf | yes: `src/superclaude/cli/issue_pipeline/` has no files in the snapshot (Glob `src/superclaude/cli/issue_pipeline/**`: none) |
| #683 | /sc:closeout and sc-closeout-protocol (issue 668) | MERGED | 2026-11-20T01:16:58Z | 8b2ce556c691ed53490c1c7f3ab7f56275491c02 | yes (settle.sh exists) |
| #684 | PR C: agent-work-report moved in with the living report | MERGED | 2026-11-20T02:01:07Z | d7d645dddd42e49a72a734f9c8b6952bcbcb4527 | yes (the skill exists) |
| #686 | PR A: the poll wakes the repo's orchestrator | OPEN, not draft, MERGEABLE, updated 2026-11-20T03:00:40Z | not merged | none | no |
| #690 | PR P: /sc:issue --plan and --remaining | OPEN | not merged | none | no |
| (none) | PR B: orchestrator skill and `superclaude orchestrator` package | no PR found by the three searches | n/a | n/a | no |

NOTE: `_TOP_KEYS` in the snapshot still lists `approvers_file` and `project_id` (cycle.py:58-69); design section 8.1 says PR A removes them (PR A's acceptance: "`grep -rn "issue-watch:trigger\|approvers_file\|project_id" src/superclaude/cli` finds nothing"). That is consistent with PR A (#686) being unmerged.

PR #686 (PR A), 59 files per `gh pr view 686 --json files`: touches `src/superclaude/cli/issue_watch/` (audit.py, cli.py, cycle.py, github.py, hold.py, launch.py, predicates.py, record.py, repos.py, route.py, wake.py), `CHANGELOG.md` and `tests/issue_watch/`. It adds `wake.py`, `repos.py`, `route.py`, `hold.py` per the design 4.10 plan. It touches no file under `src/superclaude/skills/agent-work-report/` and no `src/superclaude/cli/orchestrator/`. Whether it adds `orchestrator_repo` to `_TOP_KEYS` is checked in section 20.

Key Takeaways
- Built on master (as of the snapshot): the design (#681), PR D (#682), the closeout skill (#683), PR C (#684).
- Not built: PR A (open, #686), PR P (open, #690), PR B (no PR).

## 19. The key `orchestrator_repo` on PR A's unmerged branch (read-only `gh api`, 2026-11-20)

- `gh api repos/IronbellyOrg/IronClaude/pulls/686/files` returns no patch text for `cycle.py` (1,478 additions, 652 deletions; patch withheld by GitHub for size), so the diff was not usable. The branch file was read instead: `gh api "repos/IronbellyOrg/IronClaude/contents/src/superclaude/cli/issue_watch/cycle.py?ref=clayphi/issue-655-pr-a"`.
- On branch `clayphi/issue-655-pr-a` (PR #686, OPEN, unmerged): `_TOP_KEYS` contains `orchestrator_repo` (cycle.py line 80 of that file) and `session_tag_prefix` (82); `Config` has `orchestrator_repo: Path` (117) and `session_tag_prefix: str` (119); `orchestrator_repo` must be an absolute path (236-238); `orchestrator_repo_invalid` is a closed reason when the directory is missing (286-288); `repos.load_repos(config.orchestrator_repo, ...)` reads `<orchestrator_repo>/repos.yaml` (repos.py line 380-386 of that branch). So the reader of the key in the poll exists only on the unmerged PR A branch; on master (the snapshot) the poll rejects the key (section 16).
- Who writes `~/.config/superclaude/issue-watch.json`: no code found on master or on the PR A branch files read that creates the file with the key; **[UNVERIFIED]** (the design, orchestrator.md:269, says "The poll's own configuration file ... keeps only ..." and 6.2:893 "Nothing in IronClaude names it: the poll's configuration file holds its absolute path on each host", i.e. set by hand per host).

## 20. Tests (tests/skills/test_agent_work_report.py, 4,005 lines; tests/skills/test_worker_contract.py, 3,220 lines)

- test_agent_work_report.py: the `def test_` listing is in the Grep output of this session. Count and groups are in section 21 (written after counting). Test names that pin the living-report reader side (all in this file): `test_repo_root_is_awr_root_else_the_orchestrator_repo_of_the_poll_config` (2979), `test_the_config_has_no_workspace_key_and_no_script_reads_one` (3005), `test_a_daily_run_leaves_out_an_issue_the_orchestrator_holds` (3014), `test_without_excluded_json_the_carry_forward_check_reports_the_held_item_lost` (3052), `test_an_entry_the_run_does_not_show_open_and_assigned_excludes_nothing` (3073), `test_exclude_gives_the_same_result_run_twice` (3100), `test_a_clickup_task_linked_to_a_held_issue_is_an_item_of_its_own` (3111), `test_the_two_templates_carry_the_three_escalation_lines` (3148), `test_an_escalation_in_an_entry_file_needs_the_three_lines_in_its_own_part` (3168), `test_refresh_builds_the_shared_page_after_a_daily_run_closes` (3203), `test_a_refreshed_entry_shows_its_own_text_and_its_session_statuses` (3236), `test_refresh_moves_a_closed_or_unassigned_issue_and_keeps_an_open_one` (3291), `test_a_failed_github_read_closes_no_entry` (3334), `test_refresh_deletes_closed_and_info_files_older_than_info_ttl_days` (3344), `test_refresh_without_run_does_nothing_while_a_daily_run_holds_the_lock` (3391), `test_two_refreshes_never_run_at_once` (3614), `test_a_closed_entry_is_never_written_through_a_symlink` (3879), `test_a_symlinked_entry_folder_is_not_read_pruned_or_closed_into` (3929), `test_an_entry_url_that_is_not_web_or_orca_is_never_a_card_link` (3983).
- The entry fixture the tests use: test_agent_work_report.py:2856 comment "ones documented in common.py. PR B's `report-entry` writes the same shape." and 2870 `"""The entry file of one issue the orchestrator holds, as `report-entry` writes it."""`. The tests build entry files by hand; no test calls a real `report-entry`.

## 21. Test inventory (counts verified with `grep -c`)

- tests/skills/test_agent_work_report.py: 142 top-level `def test_` (`grep -c '^def test_'` = 142; matches the brief's 142). Groups by line range (from the Grep listing): run lock, close, abandon, action log (326-442, 2543-2560); compare and carry-forward (460-536, 641-669); render and check (558-803, 2361-2393); candidates and priority (669-780); waker (1427-1670, 2585-2658); ClickUp reads, DM, rate limit (1045-1220, 2050-2144, 2304); sessions and transcripts (1284-1426, 1809-1870, 2204-2321); match (1948-2200); gate, summary, page (2456-2840); PR C living report: repo root, exclude, refresh, symlink and url safety (2979-3983, about 60 tests). The brief's expectation "read the test names" is done; the names in section 20 are the ones that pin the entry-file reader side.
- No test runs a real `orca`, `gh` or ClickUp call: the fixtures patch `gh_json`, `run_cmd` and the ClickUp `call` (for example `fake_gh` at test_agent_work_report.py:2941-2959 asserts only `issue view` is run and makes any other command fail the test).
- tests/skills/test_worker_contract.py: 59 top-level `def test_` plus parametrized cases. It tests `src/superclaude/core/WORKER-CONTRACT.md` (the rules WC-n, brief template, never-as-worker list, unattended sections, write-verb audit at 3144-3216). A search for `agent-work-report`, `awr` and `report-entry` in that file finds none; its "coordinator" hits are the contract's own coordinator role (for example line 188 "the coordinator never uses `worker-start --retry-of`"). So the contract tests do not cover the report skill. The design's ADD1 "Orchestrated issue flow" section (brief line `Flow: orchestrated-issue`): a search of the whole snapshot for `Orchestrated issue flow|orchestrated-issue|Flow: orchestrated` finds only docs/designs/orchestrator.md. **[CODE-VERIFIED]** not built; part of PR B, which is not built.

## 22. Templates (templates/, 7 files)

| File (lines) | Role | Evidence |
|---|---|---|
| item-template.md (73) | one item card: heading `#### {{identifier_link}}: {{title}}`, status line `{{state}} · {{priority}} · {{change}}`, `Opened by / Assigned to / Owner / Board{{orchestrator_part}}`, `Next`, then 11 parts (What it is, Current state, Done with evidence, Still to do, What happened since the previous report, Recommendation, Needs you, ClickUp tasks, Agent sessions, Why this priority, How I know); carries the priority protocol (Urgent, High, Medium, Low rules) in its comments | item-template.md:1-73; read by `render.item_template` (render.py:132-139) |
| needs-you-template.md (23) | one "Needs you" entry for one session waiting on Clay (9 bullets) | needs-you-template.md:13-23; `NEEDS_PARTS` common.py:361-371 |
| overview-template.md (42) | the writing sheet `overview.md`: header, count table, since-previous line, Needs you, Your work by priority, Other work in progress, Likely yours, Closed, Not checked, How this was made | overview-template.md:1-42; filled by render.py:568-616 |
| summary-template.md (14) | the session summary and ClickUp DM text | run.py:321-340 |
| report-template.html (172) and report.js (122) | the page; data embedded as one JSON blob (`__DATA__`), sha in a `<meta name="overview-sha256">` | page.py:292-300. Network: report-template.html:8-10 load Google Fonts from `fonts.googleapis.com` and `fonts.gstatic.com`; a search for `fetch(`, `XMLHttpRequest`, `WebSocket`, `sendBeacon` in the two files finds none, so the only outside request the page makes is the font stylesheet |
| qa-report-template.md (33) | a "QA report" with a verdict that "`run.py gate` reads" (`**PASS.**` or `**FAIL.**`), a fresh-context reviewer and repeated review passes | **unreferenced**: `Grep qa-report-template` over the whole snapshot finds no match, and `Grep "qa-report|QA report"` in the skill folder finds only the file's own heading (qa-report-template.md:1). **[STALE DOC]**: SKILL.md:24 says "there is no review loop (Clay, 2026-11-03)" and `run.passed` (run.py:219-242) reads only `script-checks.md`; nothing reads a QA verdict. |

The item and needs-you templates both carry the orchestrator additions: item-template.md:10-12 and 59-65 (an issue the orchestrator holds is rendered by `run.py refresh` from its entry file; its escalation is written inside the item's own "Needs you" part with the three lines `Why this reaches you:`, `Low-stakes options:`, `If you do not answer:`); needs-you-template.md:10-12. The three lines are checked by `check.template_problems(..., orchestrated=True)` (check.py:127-134); tests 3148-3197.

## 23. Run-folder artifacts, `.dev/coordinator/runs/<run id>/` (fields from the writing code)

Run id format `%Y%m%dT%H%M%SZ-<kind>` (run.py:115). Written-by column follows SKILL.md:56-72; each row was checked against the code named.

| Artifact | Writer (code) | Fields or content |
|---|---|---|
| `run.json` | run.py:124-133 | `run, kind, started, previous_completed_run, stuck_run_replaced` |
| `run-log.md` | run.py:155; collect.py:306; run.py:417 | `# Run log <id>`, a `## Sources read` list, and one line per logged action |
| `wake-records.json` | run.py:153 | list of the `wakes/*.json` records since the previous run started |
| `automation-runs.json` | run.py:154, 160-186 | `{read, reason?, runs[]}` from `orca automations runs` for automations named `coordinator-*` |
| `incomplete-runs.json` | run.py:143 | list of earlier run folders with no `complete.json`; only when any |
| `github-items.json` | collect.py:284; rewritten by exclude.py:97 | per item: `org, repo, kind, number, title, url, author, assignees, labels, created, updated, comments, priority_mentions, draft, review_requests, closes, branch, cross_repo, clickup_refs, boards, involves_person` |
| `coverage.json` | collect.py:285-292 | `{repos[{org, repo, issues_enabled, items, errors | archived}], boards[], source_errors[]}` |
| `clickup-items.json` | clickup.py:550 | per task: `source, org, repo, kind, number, title, url, author, assignees, labels, created, updated, boards[{board, status, priority}], location, hierarchy, waiting_on, blocking, github_links, mentions_you, involves_person ...` (normalize 307-376) |
| `clickup-events.json` | clickup.py:551 | `{comments{task url: [comment records]}, chat[message records]}` |
| `clickup-gone.json` | clickup.py:552 | `{task url: reason}` |
| `clickup-status.json` | clickup.py:557 | `{read, reason?, parts{quiet, tasks, chat, replies}, workspaces, calls, since}` |
| `clickup-replies.json` | clickup.py:574, 589-592 | `[{time, text}]` (the person's own messages in the helper's DM) |
| `clickup-dm.json` | clickup.py:625-630 | `{sent, detail}` |
| `sessions.json` | sessions.py:424; rewritten by exclude.py:98 | session records (section 9) |
| `sessions-status.json` | sessions.py:425-434 | `{read, sessions, missing, started_no_prompt, worktree_links}` or `{read: false, reason}` |
| `excluded.json` | exclude.py:99 | sorted list of urls |
| `github-items-before-exclude.json`, `sessions-before-exclude.json` | exclude.py:51-56 | unreduced copies |
| `items.json`, `merged-into.json` | match.py:271-272 | joined items; `{task or session url: item url}` |
| `classified.json` | classify.py:129-136 | `{order[], items{url: {group, why, priority, priority_source}}, counts}` |
| `snapshot.json`, `compare.json` | compare.py:186-187 | section 13 |
| `activity.md` | activity.py:268 | section 12 |
| `overview.md` | render.py:616, then the model | the writing sheet |
| `to-write.json` | render.py:419 (`common.to_write`) | list of urls the model writes |
| `script-checks.md` | check.py:341 | results table plus `overview sha256: <hex>` |
| `report.html`, `notes.json` | page.py:256, 300 | page (copied to `.dev/coordinator/report.html`, page.py:301); per-url written parts plus `as_of` |
| `summary.md` | run.py:344 | script-made summary |
| `complete.json` | run.py:380 | `{run, kind, finished}` |
| `abandoned.json` | run.py:395 | `{run, reason, time}` (not listed in SKILL.md's table: **[STALE DOC]**, minor) |

State-folder files outside a run (`.dev/coordinator/`): `run.lock` (run.py:122), `refresh.lock` (run.py:639, not in SKILL.md), `action-log.jsonl` (run.py:415), `priorities.json` (prefs.py:40-46), `settings.json` (clickup.py:558-563, 610-612), `wakes/<time>-<mode>.json` (waker.py:111, run.py:104-111), `report.html` (page.py:301), `orchestrated/`, `orchestrated/closed/`, `orchestrated/info/` (only `closed/` is written by this skill: run.py:487), `waker.log` (redirected by the automation precheck command in SKILL.md:32, not by any script), and a temporary `.refresh-build-*` folder removed after each refresh (run.py:807-832). Step 14 commits `.dev/coordinator` to the orchestrator repo with `git add .dev/coordinator && git commit -m "chore(coordinator): report <run id>"`, never pushes (SKILL.md:161); the commit is run by the model, not by a script: no script under scripts/ runs `git commit` **[CODE-VERIFIED]** by reading all 16 scripts (the only `git` call is `git -C <path> remote get-url origin`, sessions.py:119).

## 24. The six statuses, grouping and priority

Statuses (SKILL.md:140; common.py:240-247 `SESSION_STATUSES`; check.py:53 `STATUS_OK`). Orca's own state is never read (SKILL.md:38).

| Status | SKILL.md definition | Script-produced inputs the model sees |
|---|---|---|
| working | "running, active in the last 15 minutes" | activity.md session line: `Claude running` or `not running`, `N events since the previous report`, `last activity <time>` (activity.py:159-163); `claude_running` is the `claude` process with the terminal's `ORCA_TERMINAL_HANDLE` (orca_term.py:34-58) |
| progressed | "did work since the previous report, now at rest" | events count; last prompts (3) and last reply (activity.py:165-168) |
| waiting on you | "its last turn asks Clay something, or a tool call has waited over 15 minutes" | quoted last reply (400 characters), `stopped on a <tool> call with no result since <time>` (activity.py:171-174); facts `ends_on_question` ("?" in the last 400 characters of the last reply when the last role is assistant) and `pending_tool_call` are in `sessions.json` (sessions.py:262-270) |
| stuck | "the same error or step repeating" | last 2 errors (activity.py:169-170); `repeated_steps` (same tool and input 3 or more times) and `error_count` are in `sessions.json` only; activity.md does not print them |
| stalled | "nothing since the previous report, or its Claude is gone, work not done" | event count 0; `claude running` / `not running`; script rule for unchanged items (`render.carried_status`, render.py:172-176) |
| done | "it reports the work finished" | quoted last reply; script behaviour: a session is kept in `sessions.json` until a report called it `done` (sessions.py:378-400), and compare.py:175-176 closes it after that |

Who writes the status: the model, for a session on a new or changed item (slot `{{RF_PLACEHOLDER:status:<sid>}}`, render.py:248-249); the script, for an unchanged item (`carried_status`, render.py:251); the orchestrator through the entry file's `session_status`, for a held issue (render.py:221-227), where "nobody writes it today" (section 15). The 15-minute thresholds appear only in SKILL.md:140: a search for `15 min|minutes=15|900` in the skill folder finds no code that computes them. **[CODE-VERIFIED]** that no script enforces the thresholds; they are the model's instruction. `check.py` enforces only that each session line ends `status: <one of six>: <reason>` (check.py:53, 196-209) and that sessions with status `waiting on you` and the "Needs you" entries match both ways (240-270).

Grouping and priority, summary of section 13: groups assigned, owned, opened, inprogress, candidate, other; priority from `priorities.json`, then board priority, then labels, then the person's own text, else Unset (suggested by the model). Report order: level (Urgent, High, Medium, Low), then state (`STATE_ORDER` common.py:389-399).

Key Takeaways
- Statuses are judgements over script-gathered transcript facts; the script enforces form, not the threshold values.
- Two inputs the model might want (`repeated_steps`, `error_count`) never reach activity.md.

## 25. The 15-step pipeline mapped to scripts (SKILL.md:76-95, steps 101-174)

| # | Step | Command (SKILL.md) | Reads | Writes (run folder unless noted) | External commands |
|---|---|---|---|---|---|
| 1 | Open the run | `python3 run.py open daily|on-demand` | lock, `wakes/`, previous run | `run.json`, `run-log.md`, `wake-records.json`, `automation-runs.json`, `incomplete-runs.json`, `run.lock`; skip record `wakes/*-skipped.json` | `orca automations list`, `orca automations runs --id` |
| 2 | Collect GitHub | `collect.py <run>` | config orgs | `github-items.json`, `coverage.json`, `run-log.md` | `gh repo list`, `gh issue list`, `gh pr list`, `gh project list`, `gh project item-list`, `gh search issues` |
| 3 | ClickUp and DM replies | `clickup.py <run>` (then model records answers with `prefs.py answer`) | `$CLICKUP_API_TOKEN`, previous run | `clickup-*.json`, `settings.json` | ClickUp REST GET calls |
| 4 | Agent sessions | `sessions.py <run>` | Orca hook file, transcripts, `/proc` | `sessions.json`, `sessions-status.json` | `orca terminal list`, `orca worktree list`, `git -C <path> remote get-url origin` |
| 4b | Leave out what the orchestrator holds | `exclude.py <run>` | `orchestrated/*.json`, `coverage.json` | `excluded.json`, rewritten `github-items.json`, `sessions.json`, the two `-before-exclude` copies | none |
| 5 | Join | `match.py <run>` | items, tasks, sessions | `items.json`, `merged-into.json` | none |
| 6 | Sort and prioritize | `classify.py <run>` | `items.json`, `priorities.json` | `classified.json` | none |
| 7 | Compare | `compare.py <run>` | previous `snapshot.json`, `excluded.json` | `snapshot.json`, `compare.json` | `gh issue|pr view <url> --json state,closedAt[,mergedAt]` per missing item |
| 8 | Read what happened | `activity.py <run>` | classified, compare, items, sessions, ClickUp events | `activity.md` | `gh api --paginate --slurp repos/<o>/<r>/issues/<n>/timeline`, `gh pr view <url> --json ...` |
| 9 | Stub the report | `render.py <run>` | all of the above | `overview.md`, `to-write.json` | none |
| 10 | Write the report | model edits `overview.md` | `activity.md`, templates | `overview.md` | none (the model is told never to call GitHub, ClickUp or Orca, SKILL.md:10) |
| 11 | Script checks | `check.py <run> --links` | `overview.md`, run files | `script-checks.md` | `gh pr|issue view <url> --json number` per GitHub link |
| 12 | Page, summary, gate, refresh | `page.py <run>`; `run.py summary <run>`; `run.py gate <run>`; `run.py refresh --run <run>` | `overview.md`, run files, entry files | `report.html`, `notes.json`, `.dev/coordinator/report.html`, `summary.md`; refresh rewrites only the shared `.dev/coordinator/report.html` and moves/deletes entry files | refresh: `gh issue view <n> --repo <r> --json state,stateReason,assignees` |
| 13 | Deliver | `page.py --open`; model posts `summary.md`; `clickup.py dm <run> <run>/summary.md`; `run.py log <run> delivered ...` | gate-checked files | `clickup-dm.json`, `action-log.jsonl`; Orca browser tab; ClickUp DM | Orca tab verbs, ClickUp POST |
| 14 | Close and commit | `run.py close <run>`; model runs `git add .dev/coordinator && git commit` in the orchestrator repo | gate (checks and sha) | `complete.json`; a git commit | `git` (by the model, not a script) |
| 15 | Help Clay | model with `prefs.py priority|answer` | stdin | `priorities.json`, `action-log.jsonl` | none |

Order of SKILL.md versus code: **[CODE-VERIFIED]** the step numbers and commands in SKILL.md:101-174 match the script usage lines. Exit code 3 from `run.py open` means another run is active (run.py:113).

## 26. Entry-file JSON contract: field, readers, and who writes it today

Contract text: common.py:133-151. Path: `.dev/coordinator/orchestrated/<owner>__<repo>__<number>.json` (active), `orchestrated/closed/` (closed), `orchestrated/info/<kind>__<key>.json` (information). Readers listed are code that reads the field (Grep of `e.get(`, `filed.get(`, `entry.get(` in run.py, render.py, exclude.py, common.py, page.py).

| Field | In common.py contract | Read by (file:line) | Written today by |
|---|---|---|---|
| `url` | yes (143) | `entry_issue_url` common.py:214; `safe_url(e.get("url"))` run.py:751 (info) | nobody in the snapshot (designed writer `report-entry`, PR B) |
| `title` | yes | run.py:576 (card), 798 (closed line) | nobody |
| `kind` | yes (`orchestrated` or `info:<stream>` in the design) | **not read by any code**; for info entries only the file name carries it | nobody |
| `group` | yes | **not read by any code**: `entry_record` sets `assigned` or `inprogress` itself (run.py:593) | nobody |
| `priority` | yes | run.py:596 | nobody |
| `assignees` | yes | run.py:570 | nobody |
| `human_assignee` | yes | run.py:570-571 (only when `assignees` is empty) | nobody |
| `author` | yes | run.py:578 | nobody |
| `orchestrator` `{id, tag, session_id, link, tier}` | yes (146) | common.py:226-232; run.py:545-566; render.py:181-191 | nobody |
| `worker` `{session_ids, link, title, branch, tier}` | yes (147) | common.py:226-232; run.py:545-566 | nobody |
| `pr_url` | yes | exclude.py:78; run.py:684, 698; render.py:229-231 | nobody |
| `last_update` | yes | run.py:457-463 (`entry_time`), 567, 582, 602 | nobody |
| `session_status` `{session id: "<status>: <reason>"}` | yes (142) | common.py:225; run.py:544; render.py:221-227 | nobody |
| written parts `state, next, what, state_text, done, todo, happened, recommend, needs, how` (`WRITTEN`) | yes (139-141) | render.py:219-220 | nobody |
| `suggested`, `priority_why` | yes (when priority is Unset) | render.py:257-258, 264-265 | nobody |
| `closed_at`, `close_reason` | yes (149) | run.py:457-463, 798 | THIS SKILL: `move_to_closed` (run.py:483) when `reconcile_entries` finds the issue closed or no longer assigned; the only entry-file writer in the snapshot |
| `follow_up_state` | NO (not in common.py) | read by no code | present in the test fixture (test_agent_work_report.py:2896) and, as the header `Follow-up state`, in the design (orchestrator.md:648) |

Result: **[CODE-VERIFIED]** nobody in the snapshot writes an active `orchestrated/` entry or an `info/` entry. Only `run.py move_to_closed` writes into the folder tree (to `closed/`), and the tests write entries by hand (`put_entry`, test_agent_work_report.py:2920-2925). Who is meant to write (design): the orchestrator, by `superclaude orchestrator report-entry` (orchestrator.md:558, 510); the model fills the written parts from `templates/report-entry-update.md`; the fixed fields are set by the verb. Who is meant to update: waves 3 to 8 of the orchestrator at milestones (orchestrator.md:558-607). The verb, the templates and the orchestrator skill do not exist in the snapshot (section 29).

Defensive reading of entries (the reader side is hardened): symlinked folder or file refused (common.py:188-199, run.py:466-481), non-object or unparseable JSON skipped with a stderr note (200-208), `javascript:`/`data:` urls dropped (`safe_url`), a missing field gives a plain fallback and never an exception (common.py:150-151, render.py:219-231).

## 27. Data sources, exactly what runs, and what the skill WRITES outside the run folder

All subprocess calls use list arguments through `common.run_cmd` (common.py:103-113), including every `orca` call (`orca_term.orca`, `run.orca_result`), with two exceptions: the `subprocess.Popen` of the page server (page.py:318) and the `subprocess.run` for git (sessions.py:119); bare `orca` and `gh` from PATH, no `--repo IronbellyOrg/IronClaude` is passed because the skill reads both orgs. Network: GitHub through `gh`; ClickUp through `urllib` (HTTPS to api.clickup.com); no other network except the page's Google Fonts stylesheet when it is opened in a browser (section 22).

| Source | Commands (script) | Read or write |
|---|---|---|
| GitHub (both orgs, `IronbellyOrg`, `IronbellyGroup`) | `gh repo list`, `gh issue list`, `gh pr list`, `gh search issues --involves` (collect.py); `gh api --paginate --slurp .../timeline`, `gh pr view` (activity.py); `gh issue|pr view` (compare.py, check.py); `gh issue view --repo` (run.py) | read only. No `gh` command in the 16 scripts creates, edits, comments or merges. |
| GitHub Projects | `gh project list`, `gh project item-list` (collect.py:156-175) | read only |
| ClickUp | GET endpoints of section 7 | read; POST only the self-DM |
| Orca terminals | `orca terminal list`, `read --screen`, `wait --for tui-idle`, `send`, `create` (orca_term.py, waker.py, sessions.py) | read, plus `send` and `create` by waker.py only |
| Orca worktrees | `orca worktree list` (sessions.py:311); `orca worktree set --worktree path:<repo> --unread --comment` (waker.py:88-96) | read; one write (unread mark) |
| Orca automations | `orca automations list`, `orca automations runs --id` (run.py:166-177) | read only |
| Orca browser | `orca tab list|close|switch|create`, `orca eval --page --expression location.reload()` (page.py:354-377) | write (tab) |
| Transcripts and hook file | `~/.config/orca/agent-hooks/last-status.json`, `~/.claude/projects/*/*.jsonl`, `/proc/*/environ` | read only |
| git | `git -C <path> remote get-url origin` (sessions.py:119) | read only. The Step 14 `git add` and `git commit` is a model action named in SKILL.md:161. |

What the skill WRITES outside the run folder and the state folder (each **[CODE-VERIFIED]** at the line cited):
1. A ClickUp DM to the token owner's own DM channel: `clickup.send_dm` (clickup.py:596-613), from `clickup.py dm` after the gate (clickup.py:616-632) and from `waker.notify` (waker.py:81-99).
2. An Orca unread mark and comment on the orchestrator repo's workspace: `waker.notify` fallback (waker.py:88-96).
3. Text typed into the coordinator's Orca terminal (`/clear`, the wake line, `ccsession coordinator`, the session name) and a new Orca terminal: waker.py:171-211, 297-302.
4. An Orca browser tab, always the same url `http://127.0.0.1:8765/report.html`: page.py:345-378.
5. A detached `python -m http.server 8765 --bind 127.0.0.1 --directory <.dev/coordinator>` process: page.py:308-342.
6. A git commit in the orchestrator repo at Step 14 (SKILL.md:161): by the model, not by a script.
7. Files under `.dev/coordinator/` of the orchestrator repo (section 23); `.dev/coordinator/report.html` is the shared page.

Triggers: (a) the Orca automations `coordinator-morning-wake` (`waker.py morning`) and `coordinator-missed-check` (`waker.py check-missed`), described in SKILL.md:30-35; they live in Orca, outside the repo: **[UNVERIFIED]** that they exist and are enabled. The design records that `orca automations list` showed only those two on 2026-11-19 and that O3 and O4 (re-pointing them at the installed script path, owner-run) were pending (orchestrator.md:120, 1025). (b) The user typing `/agent-work-report` or asking in the session. (c) `run.py refresh` without `--run`, which the design intends the orchestrator to call at each milestone (orchestrator.md:122): no code in the snapshot calls it; only SKILL.md Step 12 does. The brief's mention of "Orca automations ... triggers": the poll automation `orchestrator-poll` is designed (orchestrator.md:348) and not part of this skill.

## 28. sc-closeout and the report entry (settle.sh:1010-1063)

- `src/superclaude/skills/sc-closeout-protocol/scripts/settle.sh` `cmd_entry` (1010-1063) **[CODE-VERIFIED]**: requires `--key` made of letters, digits, `_ . -` (1026-1028); `--match differs` gives `ENTRY escalated key=<k> why=merge_differs` (1029-1032); `--issue-open` gives `ENTRY already_final key=<k> how=issue_open` (1033-1035); then probes `superclaude orchestrator report-entry --help` (1037) and, if it fails, prints `ENTRY escalated key=<k> why=surface_absent`, exit 1 (1038-1039); else runs `superclaude orchestrator report-entry --key <k> --closed` (1042) and maps the first stdout word `moved` (settled), `already_closed` (already_final), `no_entry` (none_found), anything else `ENTRY escalated key=<k> why=entry_command_failed` (1044-1062).
- On the snapshot the probe always fails (no `superclaude orchestrator` group), so every closeout of an orchestrated issue ends `ENTRY escalated ... why=surface_absent`. Stated by the skill itself: refs/settle.md:99 "The command does not exist in this repository, so the entry item is `escalated why=surface_absent` until it does." `settle.sh` calls `orca` nowhere in `cmd_entry`; it never edits a report file (design D10, sc-closeout.md:66).
- Design cross-check: docs/designs/sc-closeout.md:361-374. The paragraph at :361 says the `agent-work-report` skill "is in the IronFlow repo" and "`report-entry` and `orchestrator_repo` appear nowhere under `src/`". **[STALE DOC]** since PR #684: the skill is in `src/superclaude/skills/agent-work-report/` and `orchestrator_repo` appears in common.py (the poll config reader). `report-entry` still appears only in comments and in sc-closeout. sc-closeout.md:374 records an open question: the orchestrator's wave 8 also runs `report-entry --closed` ("one writer per status") and "the difference needs a ruling (section 12.2, row 2)". **[UNVERIFIED]** whether that ruling was made (section 12.2 of sc-closeout.md not read in this pass).
- Tests: tests/skills/test_closeout_protocol.py:397-399 (a fake `report-entry` that prints `FAKE_ENTRY_WORD`), 2675 (`orchestrator report-entry --key k1 --closed` in a log).

## 29. Built versus designed

"Built" means code in origin/master 61ac2c2e6 that I read; "PR open" means present only on an unmerged PR branch; "designed" means only in design text.

| Capability | Status | Evidence |
|---|---|---|
| `agent-work-report` skill in IronClaude (16 scripts, 7 templates, config.json) | built (PR #684, merge d7d645ddd) | section 0 file list; gh pr list |
| 15-step daily pipeline, run lock, sha256 gate, carry-forward invariants | built, unit-tested with fakes | sections 3, 11, 21 |
| `exclude.py` (Step 4b) and `excluded.json` readers (`compare.py`, `check.py`, `render.py`) | built | sections 4, 13 |
| `run.py refresh` (7 stages: lock check, reconcile, prune, read base overview, drop held blocks, add entry blocks, build page) | built, tested with fakes; no live run recorded here | run.py:629-840; tests 3203-3983 |
| `render.entry(filed=)` card from an entry file | built | render.py:194-303 |
| Entry-file reader contract (`common.py`) | built | section 26 |
| Entry-file writer, verb `superclaude orchestrator report-entry` | designed (PR B); no PR open | sections 15, 18 |
| `superclaude orchestrator` package (`src/superclaude/cli/orchestrator/`) | designed; absent | `ls src/superclaude/cli` in section 0 list; no `orchestrator` in cli/main.py |
| `/sc:orchestrator` command and `sc-orchestrator-protocol` skill | designed; absent | `ls src/superclaude/commands` and `ls src/superclaude/skills` show only closeout, sweep, agent-work-report, sc-closeout-protocol, sc-sweep-protocol |
| Poll that wakes the orchestrator (`issue-watch once` reshaped: wake.py, repos.py, route.py, hold.py) | PR open (#686, not merged) | gh pr view 686 |
| `orchestrator_repo` and `session_tag_prefix` keys in `issue-watch.json` | PR open; master rejects the key | cycle.py:58-69, 216-220; PR branch cycle.py lines 75-82 |
| `/sc:issue --plan` and `--remaining` | PR open (#690) | gh pr list |
| Retire plan-approval gate (PR D) | built (#682) | `src/superclaude/cli/issue_pipeline/` absent |
| `/sc:closeout` skill (issue 668) | built (#683); its entry step ends `surface_absent` | settle.sh:1037-1039 |
| WORKER-CONTRACT "Orchestrated issue flow" (ADD1) | designed (PR B) | only in docs/designs/orchestrator.md |
| Daily report phased out in favour of the living report | designed (owner ruling 1, orchestrator.md:49) | code still runs the full daily pipeline; hourly mode is a recorded skip (waker.py:216-220) |
| Orca automations `coordinator-morning-wake`, `coordinator-missed-check`, `orchestrator-poll` | outside the repo | **[UNVERIFIED]** |
| Orchestrator repo `IronbellyOrg/IronOrchestrator` with `repos.yaml` | outside the repo; design says it exists (orchestrator.md:866-868) | **[UNVERIFIED]** by this research |
| Spec `.dev/specs/SPEC-AGENT-WORK-COORDINATOR-20261027.md` | outside this repo | **[UNVERIFIED]** |

## Gaps and Questions

DEFECT-CANDIDATES (R5, in-scope capability declared but not wired; remediation task not created (read-only brief); flagged for the owner):
1. **Living-report writer.** Capability: "the orchestrator keeps one entry file per issue it holds" (SKILL.md:16; common.py:133-137; `exclude.py` and `run.py refresh` exist for it). Code evidence: no code outside tests writes `orchestrated/*.json` or `orchestrated/info/*.json`; `superclaude orchestrator report-entry` and `/sc:orchestrator` do not exist (section 15, 29). On-record scope decision: docs/designs/orchestrator.md assigns the writer to PR B and the reader to PR C (8.1 rows PR B and PR C; 8.2 order), approved by the owner (orchestrator.md:3, 8.2 "approved by the owner (ruling 37, 2026-11-19)"). That is a design-level sequencing decision for the writer, not a cited decision that the writer is out of scope; whether it counts is for the owner. Until the writer exists `exclude.py` excludes nothing and `refresh` renders no "Held by the orchestrator" block.
2. **Answering a "Needs you" session entry.** Declared: SKILL.md:172 (`prefs.py answer <run> <session url> session`) and SKILL.md:22 ("An unanswered 'Needs you' entry stays until Clay answers it"). Code: `prefs.check_url` accepts only `https://github.com/...` or `https://app.clickup.com/...` (prefs.py:20, 30-32), so an `orca://session/<id>` url exits "not an item URL"; `render.still_waiting` drops a carried entry only when its session url is in `answered_since` (render.py:339, 347), and the only recorded answers can name a GitHub or ClickUp url (test_agent_work_report.py:1277 uses a GitHub issue url). No cited scope decision found. **[CODE-CONTRADICTED]** SKILL.md:172 versus prefs.py:20.
3. **`orchestrator_repo` route to the state folder.** SKILL.md:14 and common.py:25 name `orchestrator_repo` in `~/.config/superclaude/issue-watch.json`; the master poll rejects that key (cycle.py:216-220, unknown key) so the documented route fails on master; only `$AWR_ROOT` works. PR A (unmerged) accepts the key. **[CODE-CONTRADICTED]** until PR A merges.

Other items:
4. Who sets `orchestrator_repo` and who writes `issue-watch.json`: **[UNVERIFIED]** (no code sets it; design 6.2:893 says it is per host).
5. Orca automations `coordinator-morning-wake`, `coordinator-missed-check` (SKILL.md:30-35) and their VERIFIED dates (2026-11-03, 2026-11-05, 2026-10-30): **[UNVERIFIED]** by this research (outside the repo; not run).
6. SKILL.md:12 spec path in the orchestrator repo: **[UNVERIFIED]**.
7. SKILL.md:183 says the gate is "enforced again by `clickup.py dm` and `run.py close`": for `clickup.py dm` the whole gate (`deliverable`) is enforced (clickup.py:619); for `run.py close` only `passed()` is (run.py:376-379), so a page or summary check is not repeated at close. **[CODE-CONTRADICTED]** in part.
8. SKILL.md:194 "never ... starts or messages agents": `waker.py` starts the coordinator session and types into its terminal (waker.py:171-211, 297-302). Likely meant as limited to workers and the skill's steps; the sentence is broader than the code.
9. Design DQ13 puts information entries "under the report section 'Watching'" (orchestrator.md:123); the code puts them under "Other work in progress" (run.py:788-793) and no "Watching" string exists in the skill. **[CODE-CONTRADICTED]** design versus code (the writer that would set the section is absent anyway).
10. The fields `kind`, `group` and `follow_up_state` of an entry file are never read (section 26).
11. Design 5.4 `report-entry-update.md` is a markdown template with header lines, while the skill reads a JSON file; how the verb converts is not specified in code. **[UNVERIFIED]**.
12. `page.py` serves the whole `.dev/coordinator/` folder on 127.0.0.1:8765 (page.py:326-327), not only `report.html`: the folder holds `settings.json` (ClickUp user id, DM channel id), `action-log.jsonl`, run folders. Fact only.
13. `report-template.html` loads Google Fonts (report-template.html:8-10): the page makes an external request when opened.
14. `qa-report-template.md` unreferenced and stale (section 22).
15. Design unknowns that the code now partly answers: U17 (can `page.py` and `render.py` rebuild with no model call): yes by reading `_refresh` (run.py:644-840), not run here. U27 (a ClickUp task linked to a held issue becomes its own item): test at test_agent_work_report.py:3111 exists; not run. U38 (can `notify` send several held notices as one DM): `waker.notify` (waker.py:81-99) sends exactly one text per call; no batching or daily cap exists in the skill (the design's `reach_daily_max` belongs to `escalate` of PR B).
16. Two writers of the closed entry (orchestrator wave 8 and sc-closeout) need a ruling per sc-closeout.md:374; ruling status **[UNVERIFIED]**.
17. Tests were not executed (read-only brief); "142 tests" is a count of definitions.
18. `waker.py` `hourly` mode and `local_gate` mode `hourly` remain in code though no hourly automation exists (waker.py:8-9, 216-220).
19. Section 12.2 and the owner-decision rows of orchestrator.md (1146-1216) and the UNVERIFIED rows (1253-1320) were read only for U13, U17, U27, U38, OD6; the rest of those tables was not read.

## Stale Documentation Found

- **[STALE DOC]** `templates/qa-report-template.md`: describes a QA verdict "`run.py gate` reads"; no code reads it; unreferenced (section 22).
- **[STALE DOC]** docs/designs/sc-closeout.md:361: says the report skill is in IronFlow and `orchestrator_repo` appears nowhere under `src/`; both changed with PR #684.
- **[STALE DOC]** SKILL.md:56-72 artifact table omits `abandoned.json` (written by `run.py abandon`) and the state-folder `refresh.lock`; every other row was found in code (section 23).
- **[STALE DOC]** SKILL.md:172 `prefs.py answer ... <session url>` (section Gaps item 2).
- Design line numbers (orchestrator.md DQ12, 6.4) refer to the IronFlow copy of the scripts (for example `render.py entry` 126-174, `compare.py` 73-122, `check.py` 127-133, `common.py` 211-217); in the snapshot these are render.py:194-303, compare.py:121-186, check.py:211-237, common.py:420-434. The design says it read the IronFlow copy (6.4 intro), so this is an expected shift, not an error.
- orchestrator.md DQ12 says "SKILL.md 183 lines ... 15 scripts"; the snapshot has SKILL.md 194 lines and 16 scripts (`exclude.py` added).

## Summary

The `agent-work-report` skill is built and merged in IronClaude (PR #684, d7d645ddd): a 15-step daily pipeline of 16 scripts that reads two GitHub orgs with read-only `gh`, ClickUp through its REST API, and Orca terminals plus Claude transcripts; the model writes only the judgement parts, `check.py` and a sha256 chain gate delivery, and the skill writes a ClickUp DM, an Orca unread mark, an Orca browser tab, a localhost page server and (through the model) a git commit. The living-report reader side (`exclude.py`, `run.py refresh`, `render.entry(filed=)`, `waker.py`, the entry-file contract in `common.py`) is built and tested with fakes, but nothing in the snapshot writes an active `orchestrated/` entry: the writer `superclaude orchestrator report-entry`, the `superclaude orchestrator` package and `/sc:orchestrator` are designed (PR B, no PR open), the poll that wakes orchestrators is PR A (#686, open) and `/sc:issue --plan` is PR P (#690, open). Three defect candidates are flagged for the owner: the missing writer, the unusable `prefs.py answer <session url>` instruction, and the `orchestrator_repo` key that the master poll rejects. The six statuses are model judgements over script-gathered facts; no script enforces the 15-minute thresholds.



- see gapfill-c1-GF1-c8-reconciliation.md for the resolution of GF-1 (living-report writer determination).

- see gapfill-c1-GF3-orchestrator-design-overlap.md for GF-3 (orchestrator design overlap).
