# DE1 — Python CLI surface scan (`superclaude`, `ic`) for v5.0.0

- Run: `/sc:post-release v5.0.0`, workstreams D (human e2e test guides) and E (sysop-only capabilities)
- Slice: the Python CLI surface only (`src/superclaude/cli/main.py` and its registered groups, plus the `ic` console script)
- Repo: `/home/coder/workspaces/worktrees/IronClaude/post-release-v5.0.0`, HEAD == tag `v5.0.0` (`git describe --tags` printed `v5.0.0`; working tree clean except the untracked `post-release/` folder)
- Scanner mode: read-only. Evidence = `--help` output of every command and subcommand (run through `.venv/bin/superclaude`, which is the `uv` venv entry point), the source lines cited, and a small set of real read-only smoke runs (results quoted below).
- Entry points: `pyproject.toml:70-72` — `superclaude = "superclaude.cli.main:main"`, `ic = "superclaude.cli.ic:main"`.
- Change sources: `CHANGELOG.md` `## [5.0.0] - 2026-11-02` (lines 7-436) and `docs/releases/v5.0.0.md`.

Hand-test cost legend:

| Cost | Meaning |
|---|---|
| FREE | Read-only, no network beyond local `claude` CLI, finishes in seconds |
| SLOW | Read-only but calls `claude mcp list` once per server; took over 25 s here |
| LOCAL-WRITE | No Claude API call; writes files under `~/.claude/`, the project, or `/tmp` |
| API | Launches `claude` subprocesses (Claude API spend), minutes to hours |
| PROXY | Needs operator-provisioned OpenAI-compatible proxy credentials (`T2ProxyUrl`, `T2ProxyKey`, `T2Model0N`) |

<!-- sections appended below -->

## Install, upgrade, health (`install`, `update`, `install-skill`, `doctor`, `version`)

| Command | Purpose | Invocation (from `--help`) | Expected result + source | Hand-test cost | 5.0.0 change |
|---|---|---|---|---|---|
| `superclaude --version` / `superclaude version` | Print version | `superclaude --version`; `superclaude version` | `SuperClaude, version 5.0.0` / `SuperClaude version 5.0.0`; exit 0 (`main.py:18-19`, `main.py:513-516`). Smoke: both printed 5.0.0 | FREE | Version bump only |
| `install --list` | List core files, commands, agents, skills, templates, codegraph block, retired MCP names without installing | `superclaude install --list` | Prints per-component `installed`/`not installed`, then a codegraph block (`Executable`, `Owner`, `User registration`, `Ready for Serena retirement`) and one line per retired name; exits 0 via early `return` (`main.py:87-172`; codegraph block `install_mcp.py:1059-1060` is documented "no download, no `claude mcp` call"). Smoke: rc 0, `Templates: 53 available, 53 installed`, `User registration: matches`, `Ready for Serena retirement: yes`, `codebase-memory-mcp absent`, `serena absent` | FREE | New codegraph block and retired-name lines (CHANGELOG 94, 114) |
| `install` | Install framework into `~/.claude/` (core, commands, agents, skills, ccsession wiring, hooks, templates, rules/output styles/settings defaults/Orca skills), then required codegraph phase, then non-fatal retire step | `superclaude install [--target DIR] [--force] [--list]` | Steps 1-7 (`main.py:174-237`), codegraph phase (`main.py:239-253`, user scope only), retire step whose outcome never changes the exit code (`main.py:255-267`); exit 1 if any phase failed, including codegraph (`main.py:269-280`). Plain install skips files that already exist (`install_core.py:68-69`) | LOCAL-WRITE (writes `~/.claude/`, `~/.claude.json` user MCP scope, may download codegraph v1.6.2 over the network). Test in a throwaway `HOME` | Breaking/major: required codegraph phase (CHANGELOG 91-93); retire step removes provably-IronClaude Serena/codebase-memory registrations (CHANGELOG 108-115); codebase-memory install removed (CHANGELOG 102); copies `HOW-WE-WORK.md`, `ISSUE-HANDOFF.md`, `ISSUE-BACKLOG.md` (CHANGELOG 236, 43); release notes require `install --force` for this upgrade (`docs/releases/v5.0.0.md:144-153`) |
| `install --force` | Same, overwriting every shipped file | `superclaude install --force` | As above; `--force` is not forwarded to the codegraph phase (`main.py:239-241`). Overwrites edited `~/.claude/CLAUDE.md`/`RULES.md` and re-copies skill folders with no backup (CHANGELOG 242) | LOCAL-WRITE (destructive to local edits) | The documented 5.0.0 upgrade command (`docs/releases/v5.0.0.md:148`) |
| `update` | Re-install core, commands, agents, skills, ccsession, hooks, templates, user setup with force | `superclaude update [--target DIR]` | Same phases as install with `force=True` but NO codegraph phase and NO retire step; prints `legacy registration present: run superclaude install` notice when relevant; exit 1 if any phase failed (`main.py:334-429`, notice `main.py:407-415`) | LOCAL-WRITE (overwrites like `--force`) | Known limitation: `update` does not complete the 5.0.0 upgrade (`docs/releases/v5.0.0.md:232`) |
| `install-skill` | Install one packaged skill | `superclaude install-skill SKILL_NAME [--target DIR] [--force]` | `✅ Skill '<name>' installed successfully ...` exit 0, or `❌ Skill '<name>' not found` exit 1 (`main.py:432-468`, `install_skill.py:29-30`). Lookup is `src/superclaude/skills/<name>` or `<name>` with `-`→`_` (`install_skill.py:58-97`) | LOCAL-WRITE (use `--target /tmp/...`) | None listed. Doc drift: the help example `pm-agent` has no matching skill directory (only `sc-pm-protocol`, `confidence-check` exist), so the example exits 1 (code-derived; not executed) |
| `doctor` | Installation health checks | `superclaude doctor [--verbose]` | Seven checks: pytest plugin, agents, skills, configuration, ccsession, codegraph MCP registration, retired MCP registrations (`doctor.py:17-54`); `✅ SuperClaude is healthy` exit 0, else `⚠️ N/M checks failed` exit 1 (`main.py:471-510`). Retired-MCP check warns, never fails (CHANGELOG 114). Smoke: all 7 ✅, rc 0 | FREE | New codegraph registration check (CHANGELOG 94), retired-MCP warning (CHANGELOG 114), ccsession UserPromptSubmit/SessionEnd hook check (CHANGELOG 65) |

Cheapest smoke for the group: `superclaude --version && superclaude doctor --verbose && superclaude install --list | tail -12`.

## MCP server management (`mcp`)

| Command | Purpose | Invocation | Expected result + source | Hand-test cost | 5.0.0 change |
|---|---|---|---|---|---|
| `mcp --list` | Show gateway + individual servers and installed state | `superclaude mcp --list` (cannot combine with `--servers`, `--dry-run` or non-user `--scope`: `UsageError`, `main.py:316-322`) | Box for AIRIS gateway, then each registry server with `installed`/`not installed` (`install_mcp.py:1317-1351`). Each status calls `claude mcp list` with a 60 s timeout (`install_mcp.py:551-556`), once per server | SLOW (smoke hit the 25 s batch timeout after 5 of 8 servers; budget about 1-2 min) | Registry now: context7, playwright, morphllm-fast-apply, tavily, auggie, codegraph, litellm (`install_mcp.py:42-115`); serena and codebase-memory-mcp gone (CHANGELOG 103) |
| `mcp --dry-run` (no selection) | Print the action menu and choices without prompting | `superclaude mcp --dry-run` | Prints `1. Install MCP servers (default) / 2. Cancel`, the `g/1-7/0` choices, `[DRY RUN] Available choices only...`, exit 0 (`install_mcp.py:1377-1384`). Smoke: rc 0 | FREE | Menu reduced to Install/Cancel (CHANGELOG 103) |
| `mcp --dry-run --servers <name>` | Preview one install | `superclaude mcp --dry-run --servers litellm` | `Successfully previewed 1 MCP server(s).` exit 0; dry-run skips prerequisites and mutation (`install_mcp.py:1370`, `1430-1458`). Smoke: litellm `Already installed and up to date`, rc 0 | FREE | litellm opt-in HTTP entry (CHANGELOG 80) |
| `mcp --servers serena` (negative) | Prove a retired server is rejected | `superclaude mcp --dry-run --servers serena` | `Unknown MCP server selection: serena`, exit 1 (`install_mcp.py:1422-1428`, `main.py:330-331`). Smoke: rc 1 | FREE | Breaking removal (CHANGELOG 103) |
| `mcp --uninstall` (negative) | Prove removed flag is rejected | `superclaude mcp --uninstall` | Click `No such option '--uninstall'`, exit 2. Smoke: rc 2 | FREE | `--uninstall` and `--yes` removed (CHANGELOG 103) |
| `mcp` (no TTY, no selection) | Non-interactive guard | `superclaude mcp </dev/null` | `Explicit server selection is required; use --servers.` exit 1 (`install_mcp.py:1385-1389`). Smoke: rc 1 | FREE | Menu change |
| `mcp` (TTY) | Interactive install | `superclaude mcp` | Prompts Action 1/2, then `g`/`0`/numbers; `0` excludes `opt_in_only` servers (`install_mcp.py:1390-1421`) | LOCAL-WRITE (registers in `~/.claude.json`; tavily/morph prompt for API keys `install_mcp.py:1221-1238`) | As above |
| `mcp --servers <a> --servers <b> [--scope local|project|user]` | Install named servers | e.g. `superclaude mcp --servers context7` | Prerequisite check, then per-server install; `Partially completed: n/m` exit 1 on any failure (`install_mcp.py:1430-1458`). codegraph accepts user scope only (`install_mcp.py:922-927`) | LOCAL-WRITE (network: npm/uvx/docker depending on server) | codegraph entry managed here too (CHANGELOG 92) |

Cheapest smoke: `superclaude mcp --dry-run; superclaude mcp --dry-run --servers serena; echo $?` (expect menu, then `Unknown MCP server selection: serena`, `1`).

## Sprint (`sprint`)

| Command | Purpose | Invocation | Expected result + source | Hand-test cost | 5.0.0 change |
|---|---|---|---|---|---|
| `sprint run --dry-run` | Show discovered phases without executing | `superclaude sprint run <tasklist-index.md> --dry-run [--start N --end M]` | With no explicit window, auto-resume planning runs first (pure-read) and prints the resume decision (`sprint/commands.py:332-352`); with an explicit window prints `Dry run: N phases discovered` (`commands.py:430-432`, `982-993`). Fidelity block exits 1 unless `--force-fidelity[-fail]` (`commands.py:418-428`) | FREE (UNVERIFIED: whether `load_sprint_config` creates state dirs under `.dev/sprint-state/` on dry run). Fixtures exist, e.g. `.dev/e2e-reflect/tl-1/bundle/tasklist-index.md` | Auto-resume default (CHANGELOG 320-323) |
| `sprint run` | Execute phases as fresh Claude sessions, in tmux by default | `superclaude sprint run INDEX [--start --end --max-turns --model --no-tmux --permission-flag --debug --stall-timeout --startup-stall-timeout --stall-action --shadow-gates --force-fidelity-fail TEXT/--force-fidelity --release-dir --state-dir --handoff/--no-handoff --resume TASK --task-parallelism K --fresh/--restart -y/--yes --max-session-resets N --ignore-run-lock]` | Auto-resume exits: ambiguous state 2 (`commands.py:452-458`), integrity gate 2 (`470-481`), drift < 0.80 → 2 (`483-497`), non-interactive without assent 2 (`516-528`), operator declines 1 (`507-515`), nothing to resume 0 (`338-340`). Then tmux launch or foreground `execute_sprint` (`434-438`). Default `--permission-flag --dangerously-skip-permissions` (`109-119`) | API (long; one Claude session per phase/task) | New `--handoff`, `--resume <task_id>`, `--task-parallelism` (CHANGELOG 302-307); `--fresh/--restart/--yes` (CHANGELOG 332); CI must pass `--yes`/`CI=1` or `--start 1` (`docs/releases/v5.0.0.md:156`) |
| `sprint rerun-tasks` | Re-run named failed tasks in one phase and merge back | `superclaude sprint rerun-tasks INDEX [--phase N --tasks T..] [--from-reflect-report PATH] [--merge-back/--no-merge-back --dry-run --include-transitive --ignore-deps --force-merge --allow-loop --no-verify-checkpoints --bundle-dir --restore --fresh/--restart -y]` | `--from-reflect-report` with `--phase/--tasks` → ClickException exit 1 (`commands.py:877-880`); auto-detect when no selector: ambiguous 2 (`898-902`), no phases → UsageError 2 (`903-910`), all complete 0 (`911-912`), phase-level only → exit 1 (`913-918`); exit code from `run_rerun_tasks` (`929-945`). `--dry-run` previews | API (dry-run likely FREE; UNVERIFIED) | Auto-detect default (CHANGELOG 321) |
| `sprint verify-checkpoints` | Check declared checkpoint report files; optionally recover | `superclaude sprint verify-checkpoints OUTPUT_DIR [--recover --reevaluate-stale --json]` | No `tasklist-index.md` → ClickException exit 1 (`commands.py:727-729`); prints table `Checkpoints: N declared | ...` (`948-979`). Always writes `OUTPUT_DIR/manifest.json`, even without `--recover` (`commands.py:747-748`) | LOCAL-WRITE (not read-only despite the name; use a copy of a fixture) | None listed |
| `sprint status` | Show sprint status | `superclaude sprint status` | STUB: always prints `Status command not yet connected to active sprint.` exit 0 (`sprint/logging_.py:367-371`). Help text claims it reads the execution log. Smoke confirmed | FREE | None; known gap (help/behavior mismatch) |
| `sprint logs` | Tail execution log | `superclaude sprint logs [-n N] [-f]` | STUB: prints `Logs command not yet connected to active sprint.` exit 0 (`sprint/logging_.py:374-378`); `-n/-f` ignored. Smoke confirmed | FREE | None; known gap |
| `sprint attach` | Attach to `sc-sprint-*` tmux session | `superclaude sprint attach` | `No running sprint session found.` exit 1 when none (`sprint/tmux.py:262-268`) | FREE (negative path) | None |
| `sprint kill` | Stop running sprint (SIGTERM, 10 s grace, SIGKILL) | `superclaude sprint kill [--force]` | `No running sprint session found.` exit 1 when none (`sprint/tmux.py:271-276`) | FREE (negative path); destructive on a live run | None |

Cheapest smoke: `superclaude sprint run .dev/e2e-reflect/tl-1/bundle/tasklist-index.md --dry-run --start 1` (UNVERIFIED output; not executed by this scanner) plus `superclaude sprint attach; echo $?` (expect `No running sprint session found.`, `1`).

## Roadmap and tasklist (`roadmap`, `tasklist`)

| Command | Purpose | Invocation | Expected result + source | Hand-test cost | 5.0.0 change |
|---|---|---|---|---|---|
| `roadmap run --dry-run` | Print step plan and gate criteria | `superclaude roadmap run SPEC [TDD] [PRD] --dry-run [--output DIR]` | More than 3 inputs → UsageError exit 2 (`roadmap/commands.py:299-303`); prints `[roadmap] Input type: ...` to stderr (`388-393`); creates the output dir before the dry-run branch (`roadmap/executor.py:3670`) then prints the plan and returns (`executor.py:3735-3737`) | LOCAL-WRITE (mkdir only; output defaults to the spec's parent dir, so pass `--output /tmp/...`) | None listed |
| `roadmap run` | 8-step pipeline: extract, generate x2, diff, debate, score, merge, test-strategy (+ validate unless `--no-validate`) | `superclaude roadmap run INPUT_FILES... [--agents --output --depth quick|standard|deep --resume --model --max-turns --debug --no-validate --allow-regeneration --no-convergence --retrospective --input-type auto|tdd|spec --tdd-file --prd-file --no-compress --allow-cosmetic-remediation/--no-... --strict-no-remediation --tool-write-*]` | Failure paths `sys.exit(1)` (`executor.py:3826`, `4048`) | API (long) | None listed |
| `roadmap validate` | Validate `roadmap.md`, `test-strategy.md`, `extraction.md` in a run dir | `superclaude roadmap validate OUTPUT_DIR [--agents --model --max-turns --debug --tool-write-validate-reflect]` | Prints `[validate] Complete: B blocking, W warning, I info`; exits 0 even with blocking issues (NFR-006 comment, `roadmap/commands.py:495-513`) | API | None listed |
| `roadmap accept-spec-change` | Update stored `spec_hash` after accepted deviation records | `superclaude roadmap accept-spec-change OUTPUT_DIR` | Exit code from `prompt_accept_spec_change` (`roadmap/commands.py:404-427`); interactive prompt, non-TTY branch at `roadmap/spec_patch.py:246` | LOCAL-WRITE (edits `.roadmap-state.json`) | None listed |
| `tasklist validate` | Tasklist fidelity vs roadmap | `superclaude tasklist validate OUTPUT_DIR [--roadmap-file --tasklist-dir --model --max-turns --debug --tdd-file --prd-file]` | Writes `OUTPUT_DIR/tasklist-fidelity.md`; `FAIL: HIGH-severity deviations found` exit 1, else `PASS` exit 0 (`tasklist/commands.py:170-185`) | API | None listed |

Cheapest smoke: `superclaude roadmap run src/superclaude/examples/release-spec-template.md --dry-run --output /tmp/rm-dry` (UNVERIFIED output; not executed).

## Reflect (`reflect`)

| Command | Purpose | Invocation | Expected result + source | Hand-test cost | 5.0.0 change |
|---|---|---|---|---|---|
| `reflect contract-status` | Report pr-submit detection-contract readiness | `superclaude reflect contract-status [--validate --repo OWNER/NAME --pr N]` | Prints `state:`, `checked_paths:`, `blocker_count:`, `next_command:`, `validation_requested:` (`reflect/commands.py:145-186`); `--validate` writes a validation report (`commands.py:113-134`, `pr_submit/contract_setup/writer.py:38-72`). Smoke: `state: missing`, `blocker_count: 1`, rc 0 | FREE (without `--validate`) | Now suggests `/sc:pr-submit --monitor 3 --pr <N>` when READY (CHANGELOG 211, 230; `commands.py:199-200`) |
| `reflect run --print-command` / `--dry-run` | Show composed `claude` argv/prompt, or preflight without launch | `superclaude reflect run /abs/TASK.md --print-command` | Skips the exit sentinel on dry-run/print (`commands.py:466-469`); config error → exit 2 (`commands.py:383-422`) | FREE likely (UNVERIFIED: whether `resolve_config` creates `<task-dir>/reflect/post/<sha>/`) | — |
| `reflect run` | POST reflect gate as top-level `claude --print`, fail-closed verdict, writes `reflect_post:` frontmatter | `superclaude reflect run TASKLIST [--tmux --print-command --promote/--no-promote --reachability/--no-reachability --timeout --depth standard|deep --transport openai_compat|stub --reviewers N --output --allow-single-vendor --dry-run --resume --fix/--no-fix --max-fix-iterations N --base REF --isolate-reviewers/--no-... --tier2-fallback/--no-...]` | Exit = verdict: pass 0 / halted 10 / degraded 11 / blocked 2 (`commands.py:350-355`, `464-478`). Default model `claude-opus-4-8` unless `ANTHROPIC_MODEL` set (`commands.py:31`, `359`) | API + PROXY for Tier-2 `openai_compat`; `--transport stub` is the credit-free lane per help | `--fix/--max-fix-iterations/--base` added; `--promote` now default (CHANGELOG 281-292); `--fix` applies `/sc:implement <remediation_plan_path>` on plan route (CHANGELOG 262); contract 1.8.0 (CHANGELOG 261) |
| Recursion breaker (all reflect subcommands) | Internal | env `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE=1` | Group callback prints `reflect-wrapper recursion breaker: nested gate suppressed` and exits 0 before any subcommand (`commands.py:62-73`) | FREE | Added with the fix loop (CHANGELOG 284) |

Cheapest smoke: `superclaude reflect contract-status` (expect `state:` line, rc 0) and `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE=1 superclaude reflect contract-status; echo $?` (expect breaker line, `0`; code-derived).

## PRD (`prd`)

| Command | Purpose | Invocation | Expected result + source | Hand-test cost | 5.0.0 change |
|---|---|---|---|---|---|
| `prd run --dry-run` | Validate config only | `superclaude prd run "REQUEST" --dry-run [-p PRODUCT -w DIR -s FILE -o PATH --tier lightweight|standard|heavyweight]` | Config error → `Error: ...` exit 1; dry-run prints `Dry run: config validated successfully.` plus Request/Tier/Output/Turns, exit 0 (`prd/commands.py:115-138`) | FREE (UNVERIFIED: `resolve_config` side effects) | Research fix cycles default to 2 (CHANGELOG 32) |
| `prd run` | 15-step PRD pipeline | as above without `--dry-run` | Non-success outcome → exit 1 (`prd/commands.py:140-145`) | API (long) | Review-loop cap 2 (CHANGELOG 30-32) |
| `prd resume` | Resume from STEP_ID | `superclaude prd resume STEP_ID [-p -o --tier --max-turns --model --debug]` (must match original `--output/--product/--tier`) | exit 1 on failure (`prd/commands.py:227`, `234`) | API | — |

Cheapest smoke: `superclaude prd run "MVP spec" --dry-run` (UNVERIFIED output; not executed).

## Eval harness (`eval`)

| Command | Purpose | Invocation | Expected result + source | Hand-test cost | 5.0.0 change |
|---|---|---|---|---|---|
| `eval list` | Enumerate suite manifests | `superclaude eval list [--json --suites-dir DIR]` | One row per suite; loader error exit 2 (`eval/commands.py:924-966`). Smoke: 17 suites (e.g. `eval_smoke (version 1.0, 3 evals)`, `real (version 1.0, 17 evals)`), rc 0 | FREE | Part of cliEval Phase 5+6 remediation in the 5.0.0 block (CHANGELOG 371-400) |
| `eval describe` | Print validated, expanded manifest | `superclaude eval describe --suite NAME [--eval ID --json --suites-dir]` | Suite missing / eval missing / loader error → exit 2 (`eval/commands.py:1205-1281`). Smoke: `--suite eval_smoke --json` rc 0 | FREE | Same |
| `eval doctor` | Host preconditions | `superclaude eval doctor [--json --no-mcp --check-coverage --output-dir DIR --parallel N --suite]` | Non-Linux → refusal exit 2 (`eval/commands.py:844-849`); scratch-root violation exit 2 (`859`); hard capability fail exit 2 (`917`); coverage gate (`921`). Smoke: `--json --no-mcp` rc 0, `vendored.ptytest` soft-skip (not found) | FREE | `--output-dir` now `file_okay=False` (CHANGELOG 377) |
| `eval run` | Run a suite end-to-end | `superclaude eval run --suite NAME [--parallel N --eval ID --no-mcp --no-pty --output-dir DIR --keep-home --timeout-mult --max-disk-mb --json --verbose --junit]` | Exits 0/1/2/3 (`eval/commands.py:1990-2004`). At 5.0.0 the executor is always `_NullLifecycleExecutor` (`commands.py:1386-1405`) and a stderr WARNING says results "MUST NOT be treated as authoritative" (`1879-1885`). Artifacts under `<output-root>/.dev/eval-runs/<date>/<run-id>/` (`eval/artifact_layout.py:76`, `179`) | LOCAL-WRITE (no Claude call while the null executor is wired; pass an allowlisted `--output-dir` such as a sub-path of `/tmp/eval-runs/`) | `--output-dir` became the output root; exit code module; WARNING added (CHANGELOG 375-389) |

Cheapest smoke: `superclaude eval list && superclaude eval doctor --json --no-mcp >/dev/null; echo $?` (expect 17 suites, `0`).

## Swarm (`swarm`)

| Command | Purpose | Invocation | Expected result + source | Hand-test cost | 5.0.0 change |
|---|---|---|---|---|---|
| `swarm validate-lenses` | Validate bundled LENSES registry | `superclaude swarm validate-lenses [--warning-mode]` | OK line exit 0; failures exit 1 unless `--warning-mode` (`swarm/commands.py:420-432`). Smoke: `registry OK (9 entries inspected, 8 validated)`, rc 0 | FREE | None listed |
| `swarm scaffold` | Emit starter JobSpec for a lens | `superclaude swarm scaffold --lens NAME [-o FILE]` | JSON to stdout (transport `stub`, placeholder models, empty `target.path`/`output.dir`); unknown/`custom` lens exit 2 (`swarm/commands.py:3773-3802`). Smoke: bare-review rc 0 | FREE | None listed |
| `swarm validate` | Schema-check a JobSpec | `superclaude swarm validate JOBSPEC_PATH [--strict]` | OK exit 0; rule failures exit 1; unreadable/bad JSON exit 2 (`swarm/commands.py:242-261`, consts `192-194`). Smoke: `swarm scaffold --lens bare-review | swarm validate /dev/stdin` → `validate: /dev/stdin OK`, rc 0 | FREE | None listed |
| `swarm run` | Wave 0 preflight → Wave 1 dispatch → normalize → merge | `superclaude swarm run [SPEC_PATH | --stdin | --lens NAME | --resume JOB_ID] [--target --output --transport openai_compat|stub --reviewers 2-4 --target-line-cap --timeout-sec --label --force-relens --detached --tui --auto-inject-guard]` | Preflight failure exit 1 (EXIT_INVALID) (`swarm/commands.py:1368-1558`). `--lens` defaults transport to `stub`; spec default `openai_compat` needs the T2 proxy env (`swarm/config.py:36-39`) | LOCAL-WRITE with `--transport stub`; PROXY with `openai_compat` | None listed |
| `swarm status` | Report phase/status from `.swarm-state.json` | `superclaude swarm status --output DIR [--job ID --watch --watch-interval --watch-max-iterations]` | 0 non-terminal/success, 1 partial/failed, 2 usage (`swarm/commands.py:2757-2811`) | FREE | None listed |
| `swarm logs` | Dump/tail execution log | `superclaude swarm logs --output DIR [--job --jsonl/--md -f --tail --lines N ...]` | 0 ok; 2 missing dir/log/job mismatch (`swarm/commands.py:3193-3282`) | FREE | None listed |
| `swarm attach` / `swarm kill` | Re-attach / terminate `swarm-<JOB_ID>` tmux session | `superclaude swarm attach JOB_ID`; `superclaude swarm kill JOB_ID [--output DIR]` | No live session → graceful exit 0 for both; tmux missing / nested tmux / bad id → 2 (`swarm/commands.py:3405-3407`, `3597-3613`). `kill --output` writes `.swarm-state.json` + `done.json` | FREE (no session); kill is LOCAL-WRITE with `--output` | None listed |

Cheapest smoke: `superclaude swarm validate-lenses && superclaude swarm scaffold --lens bare-review | superclaude swarm validate /dev/stdin`.

## cli-portify (`cli-portify`)

| Command | Purpose | Invocation | Expected result + source | Hand-test cost | 5.0.0 change |
|---|---|---|---|---|---|
| `cli-portify run --dry-run` | Validate config, print derived CLI name | `superclaude cli-portify run TARGET --dry-run` | Validation errors exit 1 (`cli_portify/commands.py:189-194`); dry-run prints `cli-portify dry-run: <workflow>` and `Derived CLI name: ...` then returns (`commands.py:196-202`). Help says dry-run "Execute only PREREQUISITES/ANALYSIS/USER_REVIEW/SPECIFICATION steps"; the command returns before `run_portify` (`commands.py:204`), so the help text does not match the code path | FREE (UNVERIFIED: `load_portify_config` side effects) | `--max-convergence` default 1 (CHANGELOG 32); help states the value is stored but not read |
| `cli-portify run` | Port a skill/command into a CLI pipeline | `superclaude cli-portify run TARGET [--cli-name/--name --output --commands-dir --skills-dir --agents-dir --include-agent --save-manifest --max-turns --model --dry-run --resume/--start STEP --max-convergence --debug --gate-mode shadow|soft|full]` | OS/permission/unexpected errors exit 1; Ctrl-C prints `EXIT_RECOMMENDATION: INTERRUPTED` and exits 0 (`commands.py:206-227`) | API (long) | As above |

Cheapest smoke: `superclaude cli-portify run sc:roadmap --dry-run` (UNVERIFIED output; not executed).

## Cleanup audit (`cleanup-audit`)

| Command | Purpose | Invocation | Expected result + source | Hand-test cost | 5.0.0 change |
|---|---|---|---|---|---|
| `cleanup-audit run --dry-run` | Show execution plan | `superclaude cleanup-audit run [TARGET] --dry-run [--pass surface|structural|cross-cutting|all --batch-size --focus --output --max-turns --model --debug]` | Prints plan and returns (`cleanup_audit/commands.py:85-87`, `93`) | FREE (UNVERIFIED output) | Scope-exclusion defaults changed in the skill script `repo-inventory.sh` (CHANGELOG 350); whether the CLI pipeline uses that script is UNVERIFIED |
| `cleanup-audit run` | Multi-pass read-only audit | same without `--dry-run` | exit 0 on `success`, else 1 (`commands.py:89-90`) | API | As above |

## Recommend helpers and init-lite (`recommend`, `init-lite`)

| Command | Purpose | Invocation | Expected result + source | Hand-test cost | 5.0.0 change |
|---|---|---|---|---|---|
| `init-lite --context-optimized --dry-run` | Audit project context surfaces, print report | `superclaude init-lite --context-optimized --dry-run [--project-root DIR]` | Report to stdout + `[dry-run] No files written; .dev/superclaude/ not created.`, exit 0 (`init_lite.py:346-350`); `--context-optimized` is required (`init_lite.py:284-290`). Smoke: 3 surfaces, ~6508 tokens, rc 0 | FREE | None listed |
| `init-lite --context-optimized [--output --scaffold --force]` | Write report (and optional scaffold) | `superclaude init-lite --context-optimized --project-root /tmp/proj` | Writes `<root>/.dev/superclaude/context-audit.md`; refuses CLAUDE.md/.mcp.json/.claude/** targets (`init_lite.py:247-251`) and marker-less existing files (`253-262`) with exit 1 | LOCAL-WRITE | None listed |
| `recommend cache get KEY` | Print cached row JSON | `superclaude recommend cache get KEY [--cache-path]` | Row JSON exit 0, or `No row for key` exit 1 (`recommend/commands.py:57-75`). Smoke: `spec-generation` → rc 1 | FREE | Key `tasklist-generation` renamed `task-file-generation`; cache fingerprint covers installed dirs (CHANGELOG 244-246) |
| `recommend cache put` / `telemetry append` / `eval run` / `eval plugin` / `dispatch` | Deterministic helpers the `sc-recommend` skill shells to | see `--help` (`recommend/commands.py:78`, `151`, `202`, `311`, `403`) | Write `.claude/cache/sc-recommend-*.{yaml,jsonl}` by default; `dispatch` prints a JSON DispatchResult and writes no telemetry | LOCAL-WRITE (dispatch FREE) | Same |

Cheapest smoke: `superclaude init-lite --context-optimized --dry-run | tail -3`.

## `ic` launcher

| Command | Purpose | Invocation | Expected result + source | Hand-test cost | 5.0.0 change |
|---|---|---|---|---|---|
| `ic --help` | Usage | `ic --help` | `ic.py:12-15` `execvp`s bash on the packaged `superclaude/scripts/ic`; the script sources `$AIENV` (default `~/.aienv`) BEFORE parsing args, warning if absent (`scripts/ic:25-30`), then prints usage and exits 0 (`scripts/ic:80-82`). Smoke: usage printed, rc 0 | FREE (runs the user's `~/.aienv`) | None listed |
| `ic [ALIAS] [-p PRESET] [-H/-S/-O M] [--no-yolo] [-- claude-args]` | Launch `claude` with model-slot overrides | e.g. `ic --no-yolo -- --version` | Resolves aliases through `$IC_ALIASES`; unknown preset or slot exit 2 (`scripts/ic:50-53`, `64`); default `exec claude --dangerously-skip-permissions` (`scripts/ic:71`, `108`); `--no-yolo` drops it (`110`) | FREE for `-- --version`; otherwise starts an interactive Claude session | None listed |

Cheapest smoke: `ic --no-yolo -- --version` (expect the slot summary on stderr and the `claude` version; UNVERIFIED output).

## Proposed guide groups

Each guide should run in three tiers so a tester can stop early: Tier A = FREE smoke, Tier B = LOCAL-WRITE (throwaway `HOME`, `/tmp` output dirs or a copied fixture), Tier C = API or PROXY runs.

| # | Guide | Commands covered | Tier A smoke (FREE) | Tier B/C focus | Notes for the author |
|---|---|---|---|---|---|
| G1 | Install, upgrade and health | `--version`, `version`, `install --list`, `install`, `install --force`, `update`, `install-skill`, `doctor` | `superclaude --version`; `superclaude doctor --verbose`; `superclaude install --list \| tail -12` | Fresh `HOME=$(mktemp -d)`: `install`, then `install` again (skips existing files), `install --force`, `update` (no codegraph/retire), `install-skill confidence-check --target /tmp/x` | Must state that the 5.0.0 upgrade is `install --force`, not `update`; codegraph phase needs network + `claude` on PATH and exits 1 on failure; retire step never changes the exit code; `pm-agent` example in help fails |
| G2 | MCP server management | `mcp --list`, `mcp --dry-run`, `mcp --servers ...`, `--scope` | `mcp --dry-run`; `mcp --dry-run --servers serena` (exit 1); `mcp --uninstall` (exit 2); `mcp </dev/null` (exit 1) | `mcp --servers context7 --scope project` in a temp project; `mcp --list` (allow 1-2 min) | litellm only works on the operator network (see Sysop section) |
| G3 | Sprint | `sprint run` (dry-run, auto-resume, `--fresh`, `--yes`, `--resume`, `--task-parallelism`, `--handoff`), `rerun-tasks`, `verify-checkpoints`, `attach`, `kill`, `status`, `logs` | `sprint attach` / `sprint kill` with no session (exit 1); `sprint status`/`logs` stub lines | `sprint run <fixture> --dry-run --start 1`; `verify-checkpoints` on a COPY (it writes `manifest.json`); real `sprint run --no-tmux` on a 1-phase fixture (API) | Record the known gaps: `status` and `logs` are stubs; non-interactive auto-resume needs `--yes`/`CI=1` |
| G4 | Roadmap and tasklist | `roadmap run`, `roadmap validate`, `roadmap accept-spec-change`, `tasklist validate` | `roadmap run <spec> --dry-run --output /tmp/rm-dry` (mkdir only) | Full `roadmap run --depth quick` then `roadmap validate` then `tasklist validate` (API, long) | `roadmap validate` exits 0 even with blocking issues |
| G5 | Reflect | `reflect contract-status`, `reflect run` (`--print-command`, `--dry-run`, `--transport stub`, `--fix`) | `reflect contract-status`; breaker env check | `reflect run <abs task> --print-command`; `--transport stub` run; live `openai_compat` run (PROXY) | Exit codes 0/10/11/2; `--promote` is default in 5.0.0 |
| G6 | LLM document/port/audit pipelines | `prd run`/`resume`, `cli-portify run`, `cleanup-audit run` | `prd run "MVP spec" --dry-run`; `cli-portify run sc:roadmap --dry-run`; `cleanup-audit run --dry-run` | One lightweight real run each (API) | One guide is enough: all three share the dry-run then subprocess-pipeline shape. Flag the `cli-portify --dry-run` help/code mismatch and the Ctrl-C exit 0 |
| G7 | Swarm | `swarm validate-lenses`, `scaffold`, `validate`, `run`, `status`, `logs`, `attach`, `kill` | `validate-lenses`; `scaffold --lens bare-review \| validate /dev/stdin` | `swarm run --lens bare-review --transport stub --target README.md --output /tmp/sw1`, then `status`/`logs --output /tmp/sw1`; `--detached` + `attach`/`kill`; `openai_compat` (PROXY) | Default transport for a spec file is `openai_compat`; `--lens` defaults to `stub` |
| G8 | Eval harness (maintainer audience) | `eval list`, `describe`, `doctor`, `run` | `eval list`; `eval describe --suite eval_smoke`; `eval doctor --json --no-mcp` | `eval run --suite real --no-pty --no-mcp --output-dir /tmp/eval-runs/t1 --junit` (LOCAL-WRITE) | State that `eval run` results are not authoritative at 5.0.0 (null executor WARNING); Linux only |
| G9 | init-lite and recommend helpers | `init-lite`, `recommend cache/telemetry/eval/dispatch` | `init-lite --context-optimized --dry-run`; `recommend cache get spec-generation` (exit 1 on empty cache) | `init-lite --context-optimized --project-root /tmp/proj --scaffold`; protected-path refusal with `--output CLAUDE.md` | `recommend` subcommands are plumbing for the `sc-recommend` skill; cover them as an appendix, not as user features |
| G10 | `ic` launcher | `ic`, `ic --help`, presets, slot overrides, `--no-yolo` | `ic --help` | `ic --no-yolo -- --version`; preset with a test `AIENV=/tmp/aienv` | Sysop-flavored: depends on an operator-provisioned `~/.aienv`; default launch skips permissions |

## Sysop-only candidates

No role check, root/`sudo` check or admin-only command exists in the CLI. A search of `src/superclaude/cli/**/*.py` for `geteuid|getuid|sudo|is_admin|hidden=True|isatty|platform` found only file-ownership safety checks (`install_retired_mcp.py:214`, `231`, `351` compare `st_uid` to `os.getuid()`), one hidden option, TTY checks and platform checks. The candidates below are capabilities that only work with operator-provisioned infrastructure, override safety gates, or are internal plumbing.

| Capability | Gate / trigger | Evidence | Classification |
|---|---|---|---|
| `superclaude mcp --servers litellm` | `opt_in_only: True`; excluded from "install all" (`0`); hardcoded URL `http://ibcore:4000/mcp/` and header `Bearer ${LITELLM_API_KEY}` | `install_mcp.py:107-115`, `1406-1410`; CHANGELOG 80 | SYSOP-ONLY: works only on the operator's network with an operator-issued key. Ordinary users cannot use it |
| `ic` launcher | Requires `~/.aienv` (or `$AIENV`) with `IC_ALIASES`, `IC_PRESET_<name>` and model aliases; launches `claude --dangerously-skip-permissions` unless `--no-yolo` | `scripts/ic:16-30`, `50-53`, `71`, `108-110` | SYSOP / power-user: depends on an operator-provisioned environment file; permission bypass by default |
| Tier-2 proxy transport (`swarm run --transport openai_compat`, `reflect run --transport openai_compat`, `reflect run --tier2-fallback`) | Env `T2ProxyUrl`, `T2ProxyKey`, `T2Model01..0N`; fallback ladder `T1Model0N` | `swarm/config.py:36-39`; `reflect run --help` (`--tier2-fallback` names `T1Model01/T1Model02`) | Operator-provisioned credentials; the commands themselves are ordinary user commands, and `--transport stub` works without them |
| Sprint account rotation (`sprint run --max-session-resets N`) and model-switch suggestion | Reads the operator's exported `~/.aienv` aliases from the environment | `sprint/commands.py:233-241`; `sprint/aienv.py:1-30`; `sprint/executor.py:1056`, `1110` | Operator infrastructure (multi-account provider pool). Flag is visible to all users; meaningful only with that pool |
| `sprint run --ignore-run-lock` | Flag; help says "Unsafe — use only if a prior run crashed" | `sprint/commands.py:242-250` | Operator recovery override, not gated |
| `sprint run --force-fidelity-fail TEXT` / `--force-fidelity` | Flag; overrides the fidelity preflight block (otherwise exit 1) | `sprint/commands.py:159-175`, `418-428` | Maintainer/operator gate override, not gated |
| `sprint run --permission-flag` | Default `--dangerously-skip-permissions` | `sprint/commands.py:109-119` | Ordinary flag; security posture worth stating in G3 |
| `sprint run --tmux-session-name` | `hidden=True`, "Internal" | `sprint/commands.py:120-125` | Internal plumbing (set by `launch_in_tmux`), not a user or sysop capability |
| `SUPERCLAUDE_SPRINT_ASSUME_YES` / `CI` | `bool(os.environ.get(...))`, so ANY non-empty value, including `CI=0` or `CI=false`, auto-assents to auto-resume | `sprint/commands.py:323-327`, `891-895` | CI-operator gate available to every user. Quirk to document: `CI=0` still counts as yes |
| `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE=1` | Exact string `"1"`; the group callback exits 0 for EVERY `reflect` subcommand | `reflect/commands.py:44`, `62-73` | Internal recursion breaker. Risk to document: if a user's shell exports it, `reflect run` silently exits 0 (looks like pass) |
| `SUPERCLAUDE_PROMPT_MAX_BYTES` | Env override of the 16 MiB prompt guard | `pipeline/process.py:53-58` ("env-overridable for operators with exotic workflows") | Sysop tuning knob |
| `SUPERCLAUDE_SPRINT_RENDER_DIAG=1` | Disables Rich redirect for crash diagnosis | `sprint/tui.py:112-118` | Maintainer diagnostic |
| `eval` group | Linux-only refusal (exit 2); scratch-root allowlist for `--output-dir` | `eval/commands.py:844-849`, `859`, `1751` | Maintainer/QA audience, not sysop and not an end-user feature |
| `recommend` group | None; documented as helpers the skill shells to | `recommend --help` text; `recommend/commands.py:34-35` | Internal plumbing |
| `CLAUDE_MODEL`, `ANTHROPIC_MODEL`, `SPRINT_STATE_DIR`, `CLAUDE_CONFIG_DIR` | Env defaults | `sprint/commands.py:366-377`; `reflect/commands.py:359`; `install_mcp.py:721` | Ordinary user configuration |
| Out of slice (hand to the ccsession/hooks scanner) | `CCSESSION_ACCESS`, Coder-role tiers; `SUPERCLAUDE_CODEGRAPH_AUTOINIT`, `SUPERCLAUDE_CODEGRAPH_PRIMITIVES` | CHANGELOG 151-187, 87, 93 | Not Python CLI flags; listed so they are not lost |

## Self-audit

- Coverage: every command and subcommand registered in `main.py:519-561` plus the top-level commands (`main.py:29-516`) and `ic` has a row. `--help` was captured for all of them, including every `recommend` sub-subcommand.
- Executed smoke runs (all read-only by code inspection, stdin from `/dev/null`): `--version`, `version`, `doctor`, `install --list`, `mcp --list` (timed out at 25 s, partial output), `mcp --dry-run`, `mcp --dry-run --servers serena|litellm`, `mcp --uninstall`, `mcp` (no TTY), `eval list`, `eval describe --suite eval_smoke --json`, `eval doctor --json --no-mcp`, `swarm validate-lenses`, `swarm scaffold --lens bare-review`, `swarm scaffold | swarm validate /dev/stdin`, `init-lite --context-optimized --dry-run`, `recommend cache get spec-generation`, `sprint status`, `sprint logs`, `reflect contract-status`, `ic --help`. No install, sprint, roadmap, reflect run, eval run or swarm run was executed.
- Repo state: `git status --short` after the runs showed only the untracked `post-release/` folder. `.claude/cache/sc-recommend-lookup.yaml` exists in this worktree; its mtime equals `.claude/settings.json` and the `.claude/` directory (worktree creation time), and `LookupCache.load_or_create` does not write (`recommend/cache.py:118-140`), so it was not created by this scan.
- UNVERIFIED (code-derived or not executed): output of `sprint run --dry-run`, `rerun-tasks --dry-run`, `roadmap run --dry-run`, `prd run --dry-run`, `cli-portify run --dry-run`, `cleanup-audit run --dry-run`, `reflect run --print-command/--dry-run`, `install-skill pm-agent`, `ic --no-yolo -- --version`; whether those dry runs create directories beyond the ones cited; whether the `cleanup-audit` CLI uses the skill's `repo-inventory.sh` exclusions; exact `mcp --list` runtime.
- Findings a guide author must not miss: `sprint status`/`sprint logs` are stubs (`sprint/logging_.py:367-378`); `sprint verify-checkpoints` writes `manifest.json` (`sprint/commands.py:747-748`); `roadmap run --dry-run` creates the output dir (`roadmap/executor.py:3670`); `cli-portify --dry-run` help does not match code (`cli_portify/commands.py:196-204`); `eval run` uses the null executor (`eval/commands.py:1386-1405`); `install-skill` help example `pm-agent` does not exist; `CI` env truthiness accepts `CI=0`; `update` does not finish the 5.0.0 upgrade.
- 5.0.0 change attribution comes from `CHANGELOG.md` lines 23-38, 40-47, 78-150, 206-400 (read in this session) and greps of `docs/releases/v5.0.0.md`; "None listed" means no CLI-surface entry for that command was found in the 5.0.0 block, not that its code is unchanged.
- Line numbers were taken from files read in this session at HEAD `v5.0.0`; no source file was modified during the scan.
