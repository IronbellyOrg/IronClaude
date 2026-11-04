# Scan A2 — feature user docs

Scope: docs/user-guide/{mcp-servers,freshness-hooks,brainstorm,eval-pipeline}.md, docs/swarm/{user-guide,wizard-guide,README,command-reference}.md, docs/guides/*.md.
Code baseline: tag v5.0.0 (commit d953b983), working tree clean.

## docs/user-guide/mcp-servers.md

**Describes:** the MCP servers SuperClaude knows about (context7, playwright, morphllm-fast-apply, tavily, auggie, litellm), auto-activation triggers, an AIRIS gateway alternative, a sample `~/.claude.json`, usage flags, troubleshooting. Undated; litellm section is 5.0.0-era, but the core list predates codegraph.

**Verdict:** present-but-stale

| Doc line | Claim | Code evidence | Correct statement |
|---|---|---|---|
| 14-20 | "Core Servers" are context7, playwright, morphllm-fast-apply, tavily, auggie | `src/superclaude/cli/install_mcp.py:96-103` registry has `codegraph`; `superclaude install --help` says it installs "the pinned, checksum-verified codegraph binary registered as a user-scope MCP server" as a required phase; `superclaude mcp --list` prints `codegraph ... (pinned, installed by superclaude install)` | codegraph is the default, always-installed code-intelligence server in 5.0.0 (seven tools: node, search, callers, callees, impact, files, status). It needs a section and a row in the auto-activation table (symbols, callers, impact questions) with a link to mcp-installation.md#default-setup-codegraph. |
| 26-34 | Auto-activation table has no code-structure row | `src/superclaude/core/CLAUDE.md` MCP table and `src/superclaude/core/CODEGRAPH.md` route symbol/caller/impact questions to codegraph | Add "Symbol, caller, impact questions → codegraph (Grep/Read fallback)". |
| 106, 244, 256 | Auggie requires Node.js 18+ | `install_mcp.py:79-86` `requires_global_binary` pins `@augmentcode/auggie@0.36.0`, `"min_node_version": 20` | Auggie needs Node.js 20+; installer pins `@augmentcode/auggie@0.36.0`. |
| 107 | Auggie tools are `codebase-retrieval`, `ask_question`, `implement` | `install_mcp.py:78` description lists only `codebase-retrieval, ask_question`; no `implement` anywhere in install_mcp.py | UNVERIFIED for `implement` (depends on the auggie binary); the shipped description names two tools. |
| 139-144 | "Research Depth Control" (`--depth quick/standard/deep/exhaustive`) and "Capabilities" list sit under the litellm heading | `src/superclaude/commands/research.md:25` defines these depths for `/sc:research`; litellm is a gateway with no depth control | Structural defect: move the Capabilities and Research Depth blocks back under tavily / `/sc:research`. |
| 148-171 | AIRIS gateway: "50 tools from default servers (airis-agent, context7, fetch, memory, tavily)", set up by manual `git clone` + `docker compose up` | `install_mcp.py:28` "60+ tools"; `install_mcp.py:346` `servers_to_disable = ["airis-agent", "mindbase"]`; `superclaude mcp --list` shows `Install: superclaude mcp --servers airis-mcp-gateway` | The installer can install the gateway (`superclaude mcp --servers airis-mcp-gateway`), advertises 60+ tools (UNVERIFIED figure), and disables airis-agent and mindbase on a fresh template download. |
| 189-213 | Sample `~/.claude.json` with `@upstash/context7-mcp@latest`, `@playwright/mcp@latest` (no -y) | `install_mcp.py:47` `npx -y @upstash/context7-mcp`; `:54` `npx -y @playwright/mcp@latest`; tavily `0.2.22` matches `:38` | Minor: example differs from what the installer registers; no codegraph entry shown. Prefer `superclaude mcp --servers <name>` over hand-editing. |
| 65 | `/sc:validate "accessibility compliance" --play` | `ls src/superclaude/commands/` has no `validate.md` (only `validate-roadmap.md`, `validate-tests.md`) | No `/sc:validate` command exists. Use e.g. `/sc:test --type e2e` (`commands/test.md:22`). |
| 225, 228, 259 | `--no-mcp`, `--all-mcp` flags on `/sc:` commands | `grep -- '--no-mcp\|--all-mcp' src/superclaude/{core,commands}` → no hits; `FLAGS.md` removed in 5.0.0 (CHANGELOG Removed; `ls src/superclaude/core/` has no FLAGS.md) | These are not defined anywhere in 5.0.0. Only `--c7`, `--tavily`, `--play` survive as advisory hints in core `CLAUDE.md:22-24`. Remove or mark as advisory hints with no effect. |
| 323 | `--concurrency N` (1-15) | no `--concurrency` in `src/superclaude/commands` or `core` | Not a defined flag in 5.0.0; remove. |
| 313-318, 335 | "Behavioral Modes", "Orchestration Mode", "Deep Research Mode" link to modes.md | `MODES.md`/`ORCHESTRATOR.md` core files removed in 5.0.0 (release notes Change 3); `docs/user-guide/modes.md:5` says mode files are not installed and flags are hints | Reword as advisory; owned by A1 for modes.md itself. |

Not stale: no Serena / codebase-memory-mcp mentions remain (grep clean); line 316 already says `.superclaude/memory/`; litellm section (117-128) matches `install_mcp.py:107-116` (`http://ibcore:4000/mcp/`, `x-litellm-api-key: Bearer ${LITELLM_API_KEY}`, `opt_in_only`).

## docs/user-guide/freshness-hooks.md

**Describes:** the context-freshness hook set (session-start, user-prompt, pre-edit gate, post-read tracker, subagent start/stop), the Bash inspection batching policy, state/telemetry files, known v1 limitations, opt-out.

**Verdict:** present-but-stale (one wrong command; otherwise current)

| Doc line | Claim | Code evidence | Correct statement |
|---|---|---|---|
| 117 | "To re-enable later: `superclaude install -f`." | `uv run superclaude install -f --list` → `Error: No such option '-f'.`; `superclaude install --help` lists only `--force` | `superclaude install --force`. |
| 13-23 | Table of what gets installed omits other SessionStart/PostToolUse/SubagentStart hooks shipped in the same `hooks.json` | `src/superclaude/hooks/hooks.json`: `codegraph-session-start.sh` (SessionStart, matcher `startup`, new in 5.0.0), `auggie-flag-clear.sh` (PostToolUse), `pragmatic-subagent.js` (SubagentStart) | Optional: add a note that the 5.0.0 codegraph SessionStart hook is installed alongside (opt out with `SUPERCLAUDE_CODEGRAPH_AUTOINIT=0`), so users opting out of freshness entries do not delete it by accident. |
| 123-124 | "jq (already a SuperClaude build dependency)" | `jq` appears in `Makefile:329` only; not in `pyproject.toml` | UNVERIFIED as a declared dependency; say "requires jq on PATH". |

Verified current: PreToolUse matcher is `Edit|Write` (`hooks.json` PreToolUse) — Serena matchers removed in 5.0.0, doc never names them; `FRESH_HORIZON=1800` at `freshness-pre-edit.sh:15`; subagent-start injects `$HOME/.claude/BASH_INSPECTION_POLICY.md` (`freshness-subagent-start.sh:7`); core `CLAUDE.md:3` imports `@BASH_INSPECTION_POLICY.md`.

## docs/user-guide/brainstorm.md

**Describes:** `/sc:brainstorm` v2 — syntax, flags, 5-wave flow, artifacts, convergence routing, handoff targets.

**Verdict:** present-but-stale (minor, codegraph omission only)

| Doc line | Claim | Code evidence | Correct statement |
|---|---|---|---|
| 17 | v2 MCP servers: `auggie-mcp, tavily` | `src/superclaude/commands/brainstorm.md:6` and `skills/sc-brainstorm-protocol/SKILL.md:15` `mcp-servers: [auggie-mcp, codegraph, tavily]`; SKILL.md:4 allowed-tools include `mcp__codegraph__codegraph_status/files/search` | `auggie-mcp, codegraph, tavily`. |
| 14, 107 | Codebase context = "/sc:analyze or Auggie quick scan" | SKILL.md:57, 193, 386: Auggie → codegraph → native Glob/Grep fallback (`quality_tier=fallback_1`) | Mention the codegraph fallback tier before Glob/Grep. |
| 233 | "Brainstorming mode (`--brainstorm` flag)" | `docs/user-guide/modes.md:5` says mode flags are hints, mode files are not installed; MODES.md removed in 5.0.0 | Reword as an advisory hint (owned with modes.md by A1). |

Verified current: flag table, defaults (`--convergence 0.75`, `--proposals 3`, `--models opus,sonnet,haiku`), flag interactions, convergence routing ≥0.65/≥0.50 (SKILL.md:289-291), handoff STOP behaviour (SKILL.md:106-107) all match `commands/brainstorm.md`.

## docs/user-guide/eval-pipeline.md

**Describes:** `superclaude eval` (doctor, list, describe, run), exit codes, output layout, scratch-root allowlist, FR-G5 coverage gate. "Last verified 2026-05-22".

**Verdict:** present-and-current (for 5.0.0 behaviour; two dead links)

| Doc line | Claim | Code evidence | Correct statement |
|---|---|---|---|
| 7, 391 | Link to `.dev/releases/current/cliEval/design-spec.md` | `ls` → No such file or directory | Dead link; remove or repoint. |
| 388 | Link to `docs/eval/release-checklist.md` | `ls docs/eval/` → retention, retry, runtime, scratch-roots, validation-commands only | Dead link; remove. |
| 77, 86 | `--check-coverage` "also run the FR-G5 matcher coverage gate" | `eval doctor --help`: "Wire the FR-G5 coverage gate marker into the payload (full gate lands in M4 T04.14)" | Minor wording gap: help text says doctor only wires a marker. UNVERIFIED whether the full gate runs in doctor. |

Verified current: all 12 `eval run` flags and defaults (`--parallel 8`, `--timeout-mult 1.0`, `--max-disk-mb 1024`), doctor/list/describe options match `uv run superclaude eval <cmd> --help`; `_NullLifecycleExecutor` WARNING still emitted (`cli/eval/commands.py:1881`); coverage scope is the auggie/airis prefixes (`cli/eval/coverage.py:101-102`). Not covered: the 18 shipped suites under `cli/eval/suites/` and the `/sc:cli-eval` command (see Uncovered).

## docs/swarm/README.md

**Describes:** index for `superclaude swarm` (MultiModelSwarm): implementation status, 8 subcommands, lens/recipe catalog, transports, "what a run emits today", smoke test. Last changed 2026-06-19 (6c04cca1); `cli/swarm/commands.py` last changed 2026-07-07 (87c180fb). Swarm is not mentioned in the 5.0.0 CHANGELOG section, but the docs are stale against the 5.0.0 tree.

**Verdict:** present-but-stale

Evidence base: a stub run at tag v5.0.0 (`uv run superclaude swarm run --lens bare-review --target <file> --output <tmp>/out --transport stub`, exit 0) left `.swarm-state.json`, `execution-log.{jsonl,md}`, `manifest.json`, `merged.md`, `return-contract.yaml` and three `bare-review-0N-*.final.md` + `.meta.json` pairs (no `done.json`); `swarm status` printed `phase=terminal ... terminal_status=success`. Code: `src/superclaude/cli/swarm/commands.py:2083-2159` (fresh path now runs `normalize_wave2` + `reduce_wave3`, "replace the T03.01 dispatch-only stub with the full post-dispatch pipeline"). `swarm validate-lenses` prints `registry OK (9 entries inspected, 8 validated)`.

| Doc line | Claim | Code evidence | Correct statement |
|---|---|---|---|
| 8-15 | "Implementation status": `swarm run` is preflight + dispatch only; Wave 2/3 writer (merged.md, return-contract.yaml, done.json) "is not yet wired into the run path" | `commands.py:2083-2159`; live stub run output above | A fresh run with a recipe now runs Wave 2 normalize + Wave 3 reduce and writes `merged.md` (normalize+merge mode), `return-contract.yaml` and per-worker `*.final.md`/`*.meta.json`. `done.json` is still not written on a fresh run (only `swarm kill --output`). Remove the M5-pending banner. |
| 27, 77-79, 132, 157 | "7 lenses", "registry has 8 entries; validate-lenses validates 7", expect "registry OK (8 ... 7 validated)" | `swarm validate-lenses` → `registry OK (9 entries inspected, 8 validated)`; `cli/swarm/lenses/reflect_review.py:33-72` | 8 bundled lenses + `custom` = 9 entries, 8 validated. |
| 66-75 | Lens table lacks `reflect-review` | `reflect_review.py:34,57,59,61,64,71`: 3 workers, recipe `passthrough`, suspect yes, stable, hands off to `/sc:adversarial` | Add row: `reflect-review` · 3 · `passthrough` · stable · yes · `/sc:adversarial`. |
| 43 | `run` = "Wave 0 preflight → Wave 1 dispatch" | as above | Run = preflight → dispatch → normalize → reduce/contract. |
| 75 | custom lens prompts come from `--custom-prompt-dir` | `swarm run --lens custom --custom-prompt-dir ...` → `Error: No such option '--custom-prompt-dir'.`; command-reference.md:53-58 itself says it is the JobSpec `custom_prompt_dir` field | Refer to the JobSpec field `custom_prompt_dir`, not a flag. |
| 95-123 | "What a run emits today": exactly four files; merged.md/return-contract.yaml/per-worker outputs not emitted | live stub run lists 12 entries | Rewrite the artifact table. |
| 69 | `refactor-find` hands off to `/sc:code-review` | `refactor_find.py:53` template is `/sc:code-review --apply {compare_files}`; `src/superclaude/commands/` has no `code-review.md` | Doc matches code, but the target is not a shipped SuperClaude command (Claude Code's built-in `/code-review` is meant). Code-level issue; flag to maintainers. |

## docs/swarm/command-reference.md

**Describes:** per-flag reference and exit codes for the 8 `superclaude swarm` subcommands plus run artifacts. Last changed 2026-06-17.

**Verdict:** present-but-stale

| Doc line | Claim | Code evidence | Correct statement |
|---|---|---|---|
| 22-24 | run = Wave 0 + Wave 1; Wave 2/3 pending M5 | `commands.py:2083-2159` | Fresh run includes Wave 2/3 when the spec has a normalization recipe. |
| 35-51 | Options table | `uv run superclaude swarm run --help` also lists `--tui` ("render a live Rich progress dashboard while Wave 1 dispatch runs ... Fresh-run only ... requires a TTY ... Mutually exclusive with --detached") | Add `--tui`. |
| 44 | `--transport` "`stub` (default for `--lens`)" | `run --help`: `openai_compat (default, FR-022)` for transport.kind; `--lens` help: "the default is stub for safe quick-dispatch" | Current; keep, but state that spec-file/stdin runs default to `openai_compat`. |
| 60-66 | Exit codes 0/1/2 | `commands.py:2070-2072` SIGINT during a `--tui` run raises `Exit(130)` | Add exit `130` (interrupted). |
| 147-148 | validate-lenses prints "registry OK (8 entries inspected, 7 validated)" | live: `registry OK (9 entries inspected, 8 validated)` | 9 / 8. |
| 170-173 | status exit 1 (terminal+partial/failed) "requires the M5 contract; not reachable on today's dispatch-only path" | fresh run now writes `return-contract.yaml`; `swarm status` printed `terminal_status=success` | Exit 1 is reachable when the contract records partial/failed. |
| 175-177 | status line format `status: phase=... job_id=... updated=...` | live: `... updated=2026-11-02T23:11:58Z terminal_status=success` | Add the `terminal_status=` field. |
| 241-263 | Run artifacts: "exactly four files"; merged.md, return-contract.yaml, per-worker `*.md`/`*.meta.json` not emitted on fresh runs | live stub run: those files present (`*.final.md`, `*.meta.json`, `merged.md`, `return-contract.yaml`); `done.json` absent | Rewrite: fresh run emits the four observability files plus per-worker outputs, `merged.md` (normalize+merge) and `return-contract.yaml`; `done.json` only on `kill --output` (and resume per `reduce.py:139`, UNVERIFIED for fresh path). |

Verified current: `scaffold`, `validate` (`--strict` no-op), `status`/`logs` flags and defaults (`--watch-interval` 2.0 / 0.5, `x>=0.01`), `attach` (no options), `kill --output` match live `--help`.

## docs/swarm/user-guide.md

**Describes:** task walkthrough for `superclaude swarm` with stub-transport examples: quickstart, validate-lenses, scaffold/validate/run, lens choice, status/logs/manifest, real proxy, monitoring, resume, injection guard, custom recipes, troubleshooting. Last changed 2026-06-09.

**Verdict:** present-but-stale

| Doc line | Claim | Code evidence | Correct statement |
|---|---|---|---|
| 9-11, 63-73 | Quickstart writes only four files (`ls -A` shows `.swarm-state.json execution-log.jsonl execution-log.md manifest.json`); merged output is pending M5 | live stub run (see README section) | `ls -A` also shows `merged.md`, `return-contract.yaml` and `bare-review-0{0,1,2}-lens-default-model-0.{final.md,meta.json}`. |
| 85, 95-100 | "7 bundled lenses"; expected `registry OK (8 entries inspected, 7 validated)` | live `registry OK (9 entries inspected, 8 validated)` | 8 lenses / 9 entries. |
| 191-199 | Lens chooser table has 7 lenses | `lenses/reflect_review.py` | Add `reflect-review` (reflection-review ensemble; used headlessly by `superclaude reflect` Tier 2). |
| 248-253 | status line and "Once the M5 contract writer lands, terminal+partial/failed will exit 1" | live status prints `terminal_status=success`; contract now written | Contract writer has landed; exit 1 applies now. |
| 387-391 | "Today's caveat": `done.json` and partial/failed exit codes depend on M5; dispatch-only path | `commands.py:2161-2169` flips terminal after reduce; `done.json` still absent on fresh run (live check) | Keep the `done.json` caveat; drop the "dispatch-only" and exit-code parts. |
| 434-439 | `swarm run --lens custom --custom-prompt-dir /path/to/prompts ... --auto-inject-guard` | live: `Error: No such option '--custom-prompt-dir'.`; `--lens custom` is rejected ("custom and unknown lens names are rejected with EXIT_USAGE", run --help) | Example is broken twice. Custom prompts go in a spec file (`custom_prompt_dir` field, `"lens": "custom"`) run via `swarm run job.json --output ... --auto-inject-guard`. |
| 477 | "for `custom`, supply `--custom-prompt-dir`" | same | Same correction. |
| 481 | "No merged.md / return-contract.yaml / done.json after a normal run — Expected (M5 pending)" | live stub run | Only `done.json` is absent; remove merged.md/return-contract.yaml from this row. |
| — | No mention of `--tui` | `run --help` `--tui` | Add to §7 monitoring. |

## docs/swarm/wizard-guide.md

**Describes:** plain-language guide to `/sc:swarm-wizard` (interview, practice run, real run, monitoring, results, flags). Last changed 2026-10-14.

**Verdict:** present-but-stale (minor)

| Doc line | Claim | Code evidence | Correct statement |
|---|---|---|---|
| 60-68 | Lens menu lists 7 lenses | `lenses/reflect_review.py:34` `reflect-review` (stable) | Matches the wizard skill (`grep reflect-review src/superclaude/skills/sc-swarm-wizard-protocol` → no hits), so not wrong; optionally note that reflect-review exists and is reserved for `superclaude reflect` Tier 2. |
| 73-74 | "`bare-review` is the mature, stable lens. The others are experimental" | `reflect_review.py:71` `stability="stable"` | Two stable lenses. |
| 98-105 | Run produces `merged.md`, one file per reviewer, `return-contract.yaml` | live stub run | Current (and now contradicts README/user-guide, which still say M5 pending). |

Verified current: flag list and defaults (`--goal --target --output --real --detached --advanced --yes`, output `.dev/swarm-runs/<lens>-<ts>/`) match `src/superclaude/commands/swarm-wizard.md` Options table; `--tui` exists in `swarm run --help`; T2 env names match user-guide §6a.

## docs/guides/sprint-cli-tools-release-guide.md

**Describes:** `superclaude sprint` (run, attach, status, logs, kill, rerun-tasks), auto-resume (v4.3.5), spec→roadmap→tasklist→sprint workflow, runtime internals. Last changed 2026-06-18. Covers auto-resume, `--fresh`, `--yes`, `CI=1` correctly; misses the per-task handoff/resume/parallelism surface that 5.0.0 ships.

**Verdict:** present-but-stale

| Doc line | Claim | Code evidence | Correct statement |
|---|---|---|---|
| 17-23 | "provides 5 subcommands: run, attach, status, logs, kill" | `uv run superclaude sprint --help`: attach, kill, logs, rerun-tasks, run, status, verify-checkpoints | 7 subcommands. |
| 64-79 | Key options list | `sprint run --help` also has `--handoff/--no-handoff` (default enabled), `--resume TEXT` ("Resume from a task id, skipping validated-successful tasks (composes with --start/--end)"), `--task-parallelism INTEGER` (default 1), `--release-dir`, `--state-dir`, `--shadow-gates`, `--force-fidelity`, `--startup-stall-timeout`, `--stall-timeout`, `--stall-action`, `--debug` | Add the three 5.0.0 flags (`--resume <task_id>`, `--task-parallelism K`, `--handoff/--no-handoff`) with the `handoff/phase-{N}-task-{id}.json` records and `task_complete` event (CHANGELOG "Sprint CLI — wire the per-task execution path"). |
| 77-78 | `--force-fidelity-fail` bullet carries the `--permission-flag` supported-values sub-bullet | `sprint run --help` | Formatting defect: sub-bullet belongs under `--permission-flag` (line 76). |
| 96-97, 461-467 | "Foreground execution for CI" / "Use case 4: CI" = `sprint run <index> --no-tmux` | release notes migration step 7 and CHANGELOG: auto-resume asks for confirmation; "A non-interactive session without assent stops with guidance"; CI needs `--yes` or `CI=1` | CI example should add `--yes` (or rely on `CI=1`), else a resumable state stops the run. |
| 56, 303, 320 | Phase prompt is `/sc:task-unified Execute all tasks in @<phase-file> ...` | `src/superclaude/cli/sprint/process.py:174,220` builds `/sc:task Execute all tasks in @{phase_file} --compliance strict --strategy systematic` | `/sc:task`, not `/sc:task-unified`. |
| 295-305 | Child argv: `claude --print <perm> --no-session-persistence --max-turns N --output-format text -p "<prompt>"` | `cli/pipeline/process.py:134-165` builds `claude --print --verbose <perm> --no-session-persistence --tools default --max-turns N --output-format <fmt>`; prompt "delivered via stdin ... not as a -p argv value" (`:137`); sprint passes `output_format="stream-json"` (`sprint/process.py:166`) | Update the argv shape: `--verbose`, `--tools default`, `--output-format stream-json`, prompt on stdin. |
| 368-371 | tmux inner command forwards `--start/--max-turns/--permission-flag/--end/--model/--tmux-session-name` | `cli/sprint/tmux.py:178-217` also forwards `--state-dir`, `--debug`, `--stall-*`, `--ignore-run-lock`; it does NOT forward `--resume`, `--task-parallelism`, `--handoff/--no-handoff` or `--yes` | Doc list is incomplete. Code observation (not a doc fix): under tmux the inner worker is rebuilt from argv only (comment `tmux.py:210-214`), so `--task-parallelism`, `--resume <task_id>` and `--no-handoff` appear to be dropped in tmux mode — UNVERIFIED at runtime; raise to maintainers. |

Verified current: auto-resume semantics, `--fresh/--restart`, `-y/--yes`, `SUPERCLAUDE_SPRINT_ASSUME_YES=1`/`CI=1`, `--max-session-resets` default 8, `--ignore-run-lock`, rerun-tasks options table (`--fresh` disables auto-detection) all match `sprint run --help` / `sprint rerun-tasks --help`.

## docs/guides/reflect-cli-tools-guide.md

**Describes:** `superclaude reflect run` as a bounded auto-fix engine (PR #159): state machine, flags/defaults, auto-fixable vs human-required carve-out, O1/O2 gates, recursion breaker. Last changed 2026-07-07.

**Verdict:** present-but-stale (remediation route)

| Doc line | Claim | Code evidence | Correct statement |
|---|---|---|---|
| 28-31, 59-60, 262-273 | Auto-fix always runs `/task <remediation_task_path>`; if `remediation_task_path` is absent the wrapper HALTs (exit 10) | `cli/reflect/runner.py:474-477` "Route keyed on `--depth`: deep -> MDTM (`remediation_task_path`, run via /task); otherwise -> sc:workflow plan (`remediation_plan_path`, run via /sc:implement)"; `runner.py:769-775` uses the plan path when no task path; `runner.py:597` `verb = "/sc:implement" if plan else "/task"` | With `--depth standard` (the default) the corrective artifact is a `/sc:workflow` plan run via `/sc:implement`; `/task` is used only with `--depth deep`. HALT only when neither path is present. Matches 5.0.0 CHANGELOG "Remediation routing". |
| 41 | Wrapper consumes "the new `remediation_task_path` contract field" | same | Also consumes `remediation_plan_path`. |
| — | No mention of the `reflect contract-status` subcommand | `uv run superclaude reflect --help` lists `contract-status` ("Report detection-contract readiness without launching..."; options `--validate`, `--repo`, `--pr`) | Add a short section, or list it as undocumented. |

Verified current: `--fix/--no-fix` default `--no-fix`; `--max-fix-iterations` default 2; `--promote` default (5.0.0 flip); `--reachability` default on; `--depth standard|deep`; `--transport` default `openai_compat`; `--reviewers` default 3; `--timeout` 3600; `--base`; `--isolate-reviewers`, `--tier2-fallback` — all in `uv run superclaude reflect run --help`. No `--onboard`/`--with-hierarchy` references.

## docs/guides/cli-portify-and-pipeline-runner-guide.md

**Describes:** `/sc:cli-portify` 3-layer architecture, shared `pipeline/` foundation, how to build a runner, existing runners (roadmap, tasklist, sprint, cli-portify), CLI usage. Last changed 2026-05-22.

**Verdict:** present-but-stale

| Doc line | Claim | Code evidence | Correct statement |
|---|---|---|---|
| 80 | Phase 4 "convergence loop until score >= 7.0" | `skills/sc-cli-portify-protocol/SKILL.md:367` "Hard cap: `max_iterations = 1` ... within the 2-fix-cycle cap"; `:369` converges on zero unaddressed CRITICALs; `:374` ESCALATED → escalate to user; `:380` 7.0 is the `downstream_ready` gate | One convergence iteration (2 review passes); converges when no CRITICAL is unaddressed, else escalates; score ≥ 7.0 only sets `downstream_ready`. (5.0.0 Breaking Change 4.) |
| 495-506 | Options reference (WORKFLOW, --name, --output, --max-turns, --model, --dry-run, --resume, --debug) | `uv run superclaude cli-portify run --help` also: `--cli-name` (alias of `--name`), `--commands-dir`, `--skills-dir`, `--agents-dir`, `--include-agent`, `--save-manifest`, `--start` (alias of `--resume`), `--max-convergence` ("default: 1 ... nothing reads it yet"), `--gate-mode [shadow|soft|full]` | Add missing flags; document `--max-convergence` default 1 and that it currently has no effect (release-notes Known Issues). |
| 199-202 | ClaudeProcess builds `claude --print --verbose --dangerously-skip-permissions --no-session-persistence --tools default --max-turns N --output-format text -p "prompt"` | `cli/pipeline/process.py:137` prompt delivered via stdin, not `-p`; `:95` default `output_format="stream-json"`; `:144-153` reviewer profile drops the permission flag and `--tools default` | Prompt on stdin; output format per caller (default stream-json); restricted reviewer profile exists. |
| 400-425 | Roadmap runner "9-step", `superclaude roadmap run spec.md` | roadmap guide says 11 steps; `roadmap run --help` takes `INPUT_FILES...` (1-3: spec, TDD, PRD) | Align with roadmap guide (see below). |

## docs/guides/roadmap-cli-tools-release-guide.md

**Describes:** `superclaude roadmap` (run, validate, accept-spec-change), 11-step adversarial pipeline, gates, convergence/remediation/certification, workflow fit. Last changed 2026-10-14 (routing note added).

**Verdict:** present-but-stale (flag surface; not 5.0.0-changelog items)

| Doc line | Claim | Code evidence | Correct statement |
|---|---|---|---|
| 104, 117-125 | `superclaude roadmap run <SPEC_FILE>`; single positional `SPEC_FILE` | `roadmap run --help`: `Usage: superclaude roadmap run [OPTIONS] INPUT_FILES...` "accepts 1-3 markdown files (spec, TDD, PRD) in any order. Content type is auto-detected" | `INPUT_FILES...` (1-3 files). |
| 127-141 | Key options table | `roadmap run --help` also: `--no-convergence`, `--input-type [auto|tdd|spec]`, `--tdd-file`, `--prd-file`, `--no-compress`, `--allow-cosmetic-remediation/--no-allow-cosmetic-remediation`, `--strict-no-remediation`, 11 `--tool-write-*` flags; `grep -c` of each in the guide = 0 | Add the missing options (at least `--input-type`, `--tdd-file`, `--prd-file`, `--no-convergence`, remediation flags). |
| 899, 1420 | `convergence_enabled: bool  # Default: False`; convergence engine is an advanced opt-in feature | `cli/roadmap/models.py:111-113` `convergence_enabled: bool = True  # ... (default ON)`; `commands.py:362` `"convergence_enabled": not no_convergence` | Default ON; disable with `--no-convergence`. |
| — | Convergence budget not stated | `cli/roadmap/convergence.py:440,446` `max_runs: int = 3` "up to max_runs (default 3) checker/remediation cycles" | Code observation: roadmap convergence allows 3 runs, above the 5.0.0 "2 fix cycles" cap (changelog scope names prd CLI and cli-portify, not roadmap). UNVERIFIED whether intended; raise to maintainers. |

Verified current: `--agents` default `opus:architect,sonnet:architect`, `--depth` quick=1/standard=2/deep=3, `--max-turns` 100, `--output` default parent dir, `--retrospective` — match `roadmap run --help`. No Serena/codebase-memory references.

## docs/guides/prd-skill-release-guide.md

**Describes:** `/prd` skill v2 (7-phase multi-agent pipeline, QA gates, artifacts, PR submission). Frontmatter `last_updated: 2026-04-03`; file last changed 2026-10-31 (pr-submit wording).

**Verdict:** present-but-stale (5.0.0 review-loop rules)

| Doc line | Claim | Code evidence | Correct statement |
|---|---|---|---|
| 261, 455, 620 | Research gate FAIL "triggers targeted gap-filling agents (max 3 fix cycles)"; troubleshooting row "3+ fix cycles" | `skills/prd/refs/build-request-template.md:130` "Maximum 2 fix cycles — after 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings"; CHANGELOG "Every review-loop cap above 2 is lowered to 2 fix cycles. The prd CLI's research fix cycles default to 2" | Max 2 fix cycles for the research gate (and synthesis), then HALT and escalate. |
| 332 | "Zero leniency: All severity levels (CRITICAL, IMPORTANT, MINOR) must be resolved before proceeding." | `skills/prd/refs/agent-prompts.md:273,283` "Minor gaps are recorded as notes and do not fail it"; "Minor findings are notes: they never fail the gate and are not rechecked"; `:332-333` | Only blocking (CRITICAL/IMPORTANT) findings must be resolved; MINOR are notes. |
| 726, 736 | "3 independent QA gates" | consistent | Current. |
| — | No mention of the `superclaude prd run/resume` CLI | `uv run superclaude prd --help` (run, resume; `--tier`, `--spec`, `--where`, `--product`); only `docs/designs/prd-spec-flag.md` mentions it | Add a pointer or list as uncovered. |

PR-submission section (535-538) already uses `/sc:pr-submit --monitor 3` — current.

## docs/guides/tdd-skill-release-guide.md

**Describes:** `/tdd` skill v2 (7-phase pipeline, QA gates, PRD→TDD, artifacts, PR submission). Frontmatter `last_updated: 2026-04-03`; file last changed 2026-10-31.

**Verdict:** present-but-stale (5.0.0 review-loop rules)

| Doc line | Claim | Code evidence | Correct statement |
|---|---|---|---|
| 271, 477, 652 | Research gate "max 3 fix cycles. After 3 failed cycles, execution halts"; troubleshooting "3+ fix cycles for research" | `skills/tdd/refs/build-request-template.md:125` "Maximum 2 fix cycles — after 2 fix cycles (3 reviews), HALT and escalate" | Max 2 fix cycles. |
| 265 | "Minor still must be fixed" | `skills/tdd/refs/agent-prompts.md:282` "Minor gaps are recorded as notes and do not fail it" | Minor gaps are notes and do not fail the gate. |
| 345 | "Zero leniency: All severity levels (CRITICAL, IMPORTANT, MINOR) must be resolved" | `skills/tdd/refs/agent-prompts.md:291,340-341` | Only blocking findings must be resolved. |

PR-submission section (557-560) uses `/sc:pr-submit --monitor 3` — current. No `superclaude tdd` CLI exists (`uv run superclaude tdd --help` → usage error), and the guide does not claim one.

## docs/guides/suites-guide.md

**Describes:** cliEval suite catalogue (17 suites), per-suite run recipes, cross-cutting workflows, troubleshooting. Last changed 2026-10-17.

**Verdict:** present-but-stale

| Doc line | Claim | Code evidence | Correct statement |
|---|---|---|---|
| 44-51, 64-77, 214, 243, 271, 293, 323, 354, 385, 409 | Suites #4-#11 are "stash@{0}" (not on disk) and must be restored with `git stash apply stash@{0} -- src/superclaude/cli/eval/suites/...` | `ls src/superclaude/cli/eval/suites/` lists all eight YAMLs; `uv run superclaude eval list` loads all 17 | All suites are on disk; delete the stash column/section and every `git stash apply` line. These lines are also unsafe: the git stash stack is shared across worktrees, so `stash@{0}` is someone else's entry. |
| 59-61 | "88 expanded evals across 17 suites, including `real` (18)" | `uv run superclaude eval list`: `real (version 1.0, 17 evals)`; JSON total 87 | 87 evals; `real` has 17. |
| 81-418 | Suite-by-suite reference jumps from #11 to #15; #12-#14 (`eval_cli_doc_parity`, `cli_eval_skill_contract`, `suite_schema_guard`), `real` and `post_release_command_contract` have no section | `grep -c post_release_command_contract` = 1 (inventory note only) | Add sections or say they are covered elsewhere. |

Verified current: quick-start commands and flags (`--no-pty`, `--no-mcp`, `--json`, `--eval`, `--parallel`) exist in `eval run --help`.

## docs/guides/RELEASE-GUIDE-INSTRUCTIONS.md and docs/guides/RELEASE-GUIDE-TEMPLATE.md

**Describes:** authoring instructions and a fill-in template for component release guides (placeholders such as `component_version: "[e.g., 4.2.0 or skill-v2]"`). Last changed 2026-05-22.

**Verdict:** template — not a user doc; not scanned for staleness. No 5.0.0 behaviour claims beyond placeholders.

(Grep of both templates for serena / codebase-memory / `gh pr create` / FLAGS.md / MODES.md: no hits; only generic "fix cycle limits" placeholders at INSTRUCTIONS:124 and TEMPLATE:148. Optional: add "max 2 fix cycles, minor findings are notes" as the default authors should state.)

## Uncovered 5.0.0 capabilities

Capabilities in this slice's area that ship in 5.0.0 with no user doc (grep over `docs/` and `README.md`):

| Capability | Code / changelog evidence | Doc coverage |
|---|---|---|
| codegraph as an MCP server in the server guide | `install_mcp.py:96-103`; `superclaude install --help` | Only `docs/user-guide/mcp-installation.md` (owned by the install scanner); absent from `mcp-servers.md`. |
| `superclaude sprint run --task-parallelism K` | `sprint run --help` (default 1); CHANGELOG Sprint CLI | Only `docs/releases/v5.0.0.md`; no user guide. |
| `superclaude sprint run --resume <task_id>` | `sprint run --help`; CHANGELOG | Only release notes. |
| `--handoff/--no-handoff`, per-task `handoff/phase-{N}-task-{id}.json` records, `task_complete` log event | `sprint run --help`; CHANGELOG; `cli/sprint/handoff.py` | No doc (`grep -rl no-handoff docs/` → none). |
| `superclaude reflect run --fix` plan route (`remediation_plan_path` → `/sc:implement`) | `cli/reflect/runner.py:474-477,769-775,597` | No doc (`grep remediation_plan_path docs/` → none); reflect guide describes only the `/task` route. |
| `superclaude reflect contract-status` | `uv run superclaude reflect --help` | No doc. |
| `superclaude prd run` / `prd resume` CLI (research fix cycles default 2 in 5.0.0) | `uv run superclaude prd --help` | Only `docs/designs/prd-spec-flag.md` (design doc, not a user guide). |
| Swarm fresh-run Wave 2/3 output (merged.md, return-contract.yaml, per-worker outputs) | `cli/swarm/commands.py:2083-2159`; live stub run | Only wizard-guide hints at it; README/user-guide/command-reference say it is pending. |
| Swarm `reflect-review` lens | `cli/swarm/lenses/reflect_review.py` | No doc (`grep -rl reflect-review docs/` → none). |
| Swarm `run --tui` | `swarm run --help` | Mentioned in wizard-guide.md and runbook.md only; not in command-reference.md or user-guide.md. |
| `/sc:cli-eval` command | `src/superclaude/commands/cli-eval.md` | Mentioned in suites-guide inventory only; not in eval-pipeline.md. |
| `post_release_command_contract` and `real` eval suites | `cli/eval/suites/` | Inventory note only in suites-guide.md. |

Not uncovered here (owned by other scanners or covered): `/sc:impact`, `/sc:graph`, `SUPERCLAUDE_CODEGRAPH_*` env vars (mcp-installation.md, release notes), memory move to `.superclaude/memory/` (session-management/memory-system docs), `/sc:pr-submit` changes, removed `superclaude mcp` flags (mcp-installation.md).

## Self-audit

- Every "Code evidence" cell cites a file:line read this session, a live `--help` output from `uv run superclaude ...` at the v5.0.0 tree, or a live stub run. The swarm artifact claims rest on one real stub run (`swarm run --lens bare-review --transport stub` into a `mktemp` dir under `/tmp`, removed afterwards); no repo file other than this output was written (`git status --porcelain` showed only `.dev/releases/current/v5.0.0/post-release/`).
- UNVERIFIED items, marked inline: auggie `implement` tool; AIRIS "60+ tools" figure; `jq` as a declared dependency; whether `eval doctor --check-coverage` runs the full gate; whether `done.json` is ever written on a fresh swarm run beyond `kill --output`; whether sprint tmux mode really drops `--task-parallelism/--resume/--no-handoff` at runtime (code reading of `tmux.py:178-217` only); whether roadmap convergence `max_runs=3` is intended under the 2-fix-cycle rule.
- Two items are code observations, not doc fixes: sprint tmux argv forwarding and roadmap `max_runs=3`; also the `refactor-find` lens hands off to `/sc:code-review`, which is not a shipped SuperClaude command (`refactor_find.py:53`).
- Scope kept to the assigned slice: did not scan mcp-installation.md, modes.md, flags.md, commands.md, or other docs/swarm files (runbook, lens-catalog, monitoring-patterns, release-notes-v1 also say 7 lenses / M5 pending — not verified, out of slice).
- Line numbers were taken from Read/grep of each doc in this session; docs were not modified during the scan.
- Not checked: every example in the 1,420-line roadmap guide and 700-line PRD/TDD guides line by line; scan targeted 5.0.0 change areas (fix-cycle caps, severity, removed flags, Serena/codebase-memory, CLI flag surfaces) plus `--help` diffs.
