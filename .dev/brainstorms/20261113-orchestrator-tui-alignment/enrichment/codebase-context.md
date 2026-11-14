# Codebase context (Wave 2A enrichment, quality_tier: primary)

Source: one `mcp__litellm__augment_code-augment_code_search` call on the observer adapter, commands and collector (pushed code only), cross-checked against the adjudicated document's facts E-01 to E-18 (`.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/alignment-findings-adjudicated.md`). Locations are those the adjudicated document cites; none is new. Anything not cited there is not asserted here.

## Observer (`src/superclaude/cli/observe/`, on master)

- Registered in the shipped CLI: `src/superclaude/cli/main.py:572-574`.
- Guard: `QUESTION_GATE_PASSED = False` at `observe/commands.py:63-67`; one boolean, `check_run_id` checks syntax only.
- Orca read shapes: three argv shapes only: `orchestration worker-list --json --limit 100 [--run] [--cursor]`, `skills list --json`, and one `orchestration check --all --types question --run <id> --json` behind the guard. Forbidden verb prefixes are enforced in the adapter.
- Caps: 15 s poll, up to 5 calls per read of 100 rows (`adapter.py:29,57`), 8 MiB and 10 s per call, backoff up to 60 s, STALE after 45 s (`collector.py:28-34`). With `--questions` on a cycle can make 6 calls.
- Output: snapshot v1 (`snapshot.schema.json`, additionalProperties false, 15 row keys), rewritten each live cycle under `$XDG_STATE_HOME/superclaude/observe/` mode 0600 (`export.py:26`; `XDG_STATE_HOME` accepted only when absolute, `export.py:241-242`); `observe --once` prints a text record with no file write unless `--snapshot` (`commands.py:215-237`).
- View: `HISTORICAL_STATES = ("released", "retained")` (`view.py:35`); prints `unavailable (no source)` for report status, acceptance, tests, approval, SETTLED, POLICY FROZEN (`view.py:96,412`).

## Sweep (`src/superclaude/cli/sweep/`, on PR #539 head `873599d59`, not on master)

- `probes.py`: `ALLOWED_GIT` exact one-entry list (`:64-67`); `git --no-optional-locks -C <wt> status --porcelain=v1 -z --branch --untracked-files=all` (`:305-327`, `:1203-1214`); `worker-show` cap 50 (`:115,1114,1171`); XDG state (`:1264-1266`); `paths` shared by git status, contract allow-list and transcript scans (`:1255-1263`, `:1301`).
- `classify.py`: settled from Orca `outcome` (`:98,114,781-786`); `policy_of` returns frozen only from a blocked or failed worker contract (`:377-392`); duplicate-dispatch note (`:893-896`); join basis `row_id` = `orca:<dispatch>` (`probes.py:435`, `classify.py:891`).
- `report.py`: version check compares text before the first hyphen (`:160`, `:23`); sanitizer (`:563-598`); wording to fix after merge (`:199,534`).
- Pins: `tests/sweep/test_readonly.py:85,156,300,400,453`; `tests/sweep/test_probes_allowlist.py:503`; `tests/sweep/test_cli_contract.py:1474`; `ROW_KEYS` golden set (`tests/sweep/test_report.py:1255`).
- Design: `docs/designs/orchestrator-mode.md` (exists only on the #539 branch).

## Watcher (`src/superclaude/cli/issue_watch/`, on master)

- `launch.PROMPT_PATTERN` (`launch.py:33`), `build_claim_prompt` (`:84-92`), `OPERATION_ID_PATHS` (`:39-45`, a guess pinned by `_assumed_shape` fixtures).
- Claim command: `src/superclaude/commands/issue.md:43,88` (default `worktree` level).
- Design: `docs/designs/issue-watcher.md` (decision D1 option A: no listener; `:28,43,47-49`).

## Routing and contract surfaces

- `HOW-WE-WORK.md` plus its plugin mirror and the sc-recommend table; machine-read tables `tests/core/test_how_we_work_routing_table.py:193-205,297-298,218,312`; `tests/recommend/test_routing_refresh.py:33`.
- `src/superclaude/core/WORKER-CONTRACT.md` (WC-12, WC-13, WC-16 at `:288`, never-as-worker list; slash commands at `:23`).
- Host: `ccsession:134-141` (permission flags; `CCSESSION_PERMISSIONS`, `CC_CLAUDE_FLAGS`).

## Installed orchestration entry points (checked this session)

- `~/.claude/skills/orchestration/SKILL.md` is a discovery stub; load the guide with `ORCA skills get orchestration` after resolving the CLI (`ORCA_CLI_COMMAND`, else `orca-dev`, else `orca-ide` on Linux outside Orca terminals, else `orca`). On this host `orca-ide` is at `/home/coder/.local/bin/orca-ide`.
- Task packages already on disk: `.dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115`, `.dev/tasks/to-do/TASK-TECHREF-orchestration-20261110-050239`, `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md` (listed, not read in full here).

quality_tier: primary (Augment answered; one gap: no live run of any Orca command was made in this brainstorm).
