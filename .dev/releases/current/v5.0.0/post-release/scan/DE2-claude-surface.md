# DE2 — Claude Code surface scan (workstreams D + E), v5.0.0

- Scanner: read-only, slice = `~/.claude` surface (commands, skills, agents, hooks, core, ccsession, codegraph integration)
- Repo: `/home/coder/workspaces/worktrees/IronClaude/post-release-v5.0.0` (HEAD == tag v5.0.0)
- Sources of "new/changed": `CHANGELOG.md` `## [5.0.0]` (line 7 onward) and `docs/releases/v5.0.0.md`
- Citations are repo-relative `path:line`. Anything not read directly is marked UNVERIFIED.
- Surface size: 45 `/sc:` commands (`src/superclaude/commands/*.md` minus `README.md`), 37 skill folders, 46 agents (`src/superclaude/agents/*.md` minus `README.md`), 13 hook scripts + `hooks.json`, 12 core `.md` files.
- Status: COMPLETE

## Slash command inventory

Legend. **Skill** = the skill the command file says to load (`> Skill <name>`); "own file" = the command names no skill and runs from its own file (per `src/superclaude/core/CLAUDE.md` routing block). **Cost**: `cheap` = one prompt, minutes, no pipeline or PR; `medium` = several agents or a few minutes of tool work; `long` = multi-agent pipeline, external service (PR, reviewers, CI) or a multi-step plan/execute run. **5.0.0** = touched by the 5.0.0 changelog (NEW / CHANGED / -).

| /sc: command | One-line purpose (frontmatter `description`) | Skill loaded | Cost | 5.0.0 |
|---|---|---|---|---|
| adversarial | Structured adversarial debate, comparison and merge pipeline for 2-10 artifacts | sc:adversarial-protocol | long | - |
| agent | SC Agent session controller: investigation, implementation, review | own file | long | - |
| analyze | Code analysis across quality, security, performance, architecture | own file | cheap | - |
| auggie-review | Auggie-powered review of PRs, diffs or file snapshots, auto-posted PR review, optional remediation handoff | sc:auggie-review-protocol | long (needs auggie + a PR) | CHANGED (remediation via sc:workflow; offer-pr-review hook refs removed; codegraph) |
| brainstorm | Socratic dialogue + parallel proposals + adversarial merge | sc:brainstorm-protocol | long | CHANGED (codegraph floor) |
| build | Build, compile, package with error handling | own file | cheap | - |
| business-panel | Business panel analysis (file has NO `description:` line; `/sc:help` will print "(no description line)") | own file | medium | - |
| cleanup | Clean up code, dead code, structure | own file | cheap (mutates files) | - |
| cleanup-audit | Multi-pass read-only repo audit with evidence | sc:cleanup-audit-protocol | long | CHANGED (codegraph; default exclusions) |
| cli-eval | Author or run a cliEval suite | sc:cli-eval-protocol | long | CHANGED (cliEval remediation) |
| cli-portify | Port inference workflows into programmatic CLI pipelines | sc:cli-portify-protocol | long | CHANGED (convergence default 1; `--max-convergence` has no effect, known issue `docs/releases/v5.0.0.md:229`) |
| design | Architecture, API and interface design | own file | cheap | - |
| document | Focused docs for components, APIs | own file | cheap | - |
| explain | Explain code and concepts | own file | cheap | - |
| git | Git operations with commit messages | own file | cheap (mutates git) | - |
| graph | Code-graph index readiness; `init` builds the index (user-typed only) | sc:graph-protocol | cheap (status); init seconds-minutes | NEW |
| help | List installed commands/skills, print six-level table, point to routing guide | own file (reads `HOW-WE-WORK.md`) | cheap | CHANGED |
| impact | Definitions + production/test dependents from the code graph, advisory test list on `--tests`, Grep fallback | sc:impact-protocol | cheap | NEW |
| implement | Middleweight spec executor with per-task compliance QA and ledger | sc:implement-protocol | long | CHANGED (one A2 repair; calls /sc:impact) |
| improve | Systematic code improvements | own file | cheap (mutates files) | - |
| index | Project documentation / knowledge base | own file | medium | - |
| index-repo | Repository index (token reduction) | own file | medium | - |
| init-lite | Non-destructive audit of project-local SuperClaude context surfaces | sc:init-lite-protocol | cheap | - |
| load | Load project context from memory files | own file | cheap | CHANGED (`.superclaude/memory/`, `.serena` read-only fallback) |
| pm | Project Manager agent orchestration (PDCA) | sc:pm-protocol | long | CHANGED (memory files) |
| post-release | Post-release external-surface sync (docs, install scripts, e2e guides) | sc:post-release-protocol | long | - (UNVERIFIED whether new in 5.0.0; not named in the changelog headings) |
| pr-submit | Open PR on the fork + review auto-remediation monitor (Augment, Codex) | sc:pr-submit-protocol | long (real PR, reviewers, CI) | CHANGED (default `--monitor 3`, `--pr`, Codex, origin-first, `--yes` removed) |
| recommend | Paste-ready delegation prompt from the routing guide, or `--plugin` ecosystem search | sc-recommend | cheap (local); medium (`--plugin`, `--eval`) | CHANGED (reads `HOW-WE-WORK.md` first) |
| reflect | UC-1/UC-2 grounded reflection, heterogeneous reviewers, optional remediation | sc:reflect-protocol | long | CHANGED (`--onboard`/`--with-hierarchy` removed; remediation via sc:workflow; contract 1.8.0) |
| release-split | Two-phase release split analysis | sc:release-split-protocol | long | - |
| research | Deep web research | own file | medium-long (tavily) | - |
| review-translation | Localization review with adversarial validation | sc:review-translation-protocol | long | - |
| roadmap | Roadmap pipeline from 1-3 spec/TDD/PRD inputs | sc:roadmap-protocol | long | - |
| save | Persist session context as memory files | own file | cheap | CHANGED (`.superclaude/memory/`) |
| spawn | Meta task orchestration | own file | long | - |
| spec-panel | Multi-expert spec review | own file | medium | - |
| swarm-wizard | Plain-language guide to `superclaude swarm` | sc:swarm-wizard-protocol | long | - |
| task | Unified task execution with compliance tiers | sc:task-protocol | medium | CHANGED (codegraph floor) |
| tasklist | Roadmap → Sprint-compatible tasklist bundle | sc:tasklist-protocol | long | CHANGED (review cap 2; codegraph) |
| tdd | Create/populate a TDD | tdd | long | CHANGED (review cap 2) |
| test | Run tests with coverage reporting | own file | cheap-medium | - |
| troubleshoot | Tiered debugging, optional `--fix` remediation chain | sc:troubleshoot-protocol | medium (Tier 1) / long (Tier 2-3) | CHANGED (codegraph grounding; `--fix` via sc:workflow) |
| validate-roadmap | Roadmap-to-spec fidelity validation | sc-validate-roadmap-protocol | long | CHANGED (codegraph) |
| validate-tests | Validate `/sc:task` tier classification against YAML specs | sc:validate-tests-protocol | medium | - |
| workflow | PRD/spec/prompt → phased plan package | sc:workflow-protocol | medium-long | CHANGED (default remediation planner) |

Notes:

- Retired in 5.0.0, so a guide must check they are ABSENT: `/ccsession-tag` (CHANGELOG.md:70; skill kept with `user-invocable: false`), `/sc:README` on new installs (CHANGELOG.md:248), core files `ORCHESTRATOR.md`, `COMMANDS.md`, `PERSONAS.md`, `MODES.md`, `FLAGS.md`, `MCP.md` (CHANGELOG.md:252; old copies left in `~/.claude/`).
- Non-command skills a user can trigger directly: `sc-crash-recovery`, `task`, `task-builder`, `prd`, `tdd`, `tech-research`, `tech-reference`, `readme`, `operational-guide`, `roadmap`, `confidence-check`, `sc-bare-review` (delegate-only). Not inventoried further.
- Skill name vs folder: folders are `sc-<x>-protocol`, frontmatter names are `sc:<x>-protocol` (e.g. `src/superclaude/skills/sc-graph-protocol/SKILL.md:2`).

## New/changed 5.0.0 capabilities (detail)

### 1. `/sc:graph` (status + init) — NEW

- Invocation: `/sc:graph` (= `status`), `/sc:graph status --output-dir .dev/graph`, `/sc:graph init`, `/sc:graph init --worktree-local` (`src/superclaude/commands/graph.md:20-25`).
- Expected (status): an 8-line screen report in fixed order: version+pin, index state+relation, access, counts, pending, telemetry+opt-out, the `SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off` switch line, `next:` line (`src/superclaude/skills/sc-graph-protocol/SKILL.md:142-151`). `next_action` table: disabled → `enable_codegraph`; absent → `install_codegraph`; not_initialized → "type `/sc:graph init`"; foreign_index → `--worktree-local`; pin mismatch → `./update.sh`; stale → `wait_for_sync`; else "index ready" (`SKILL.md:50-62`). With `--output-dir`, writes `return-contract.yaml` (schema at `SKILL.md:85-110`).
- Expected (init): preflight refuses with `already_initialized` when an own fresh/stale index exists, `init_running` when `pgrep -f 'codegraph\.js (init|index)'` matches, `nested_worktree` for a foreign index without `--worktree-local` (`SKILL.md:68-82`). Command body runs `codegraph init --yes <worktree_root>` once with a 600 s timeout, then re-checks via `status --post-init <exit>` (`commands/graph.md:44-53`). Guard: only runs when the user's own message starts with `/sc:graph init` (`commands/graph.md:48`).
- Flag errors: unknown positional or two positionals → `status: blocked`; `--worktree-local` with `status` → blocked (`SKILL.md:25-26`).
- Hand-test recipe: (a) fresh clone with `SUPERCLAUDE_CODEGRAPH_AUTOINIT=0` exported → `/sc:graph` shows `not_initialized` + `run_graph_init`; (b) `/sc:graph init` → success, then `/sc:graph` shows `fresh`; (c) second `/sc:graph init` → `already_initialized`; (d) `/sc:graph bogus` → blocked; (e) `SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off` → `disabled`, `enable_codegraph`.
- Caveat for testers: the command's allowlist is `Bash(codegraph init --yes *)` (`commands/graph.md:9`), i.e. bare `codegraph` on PATH. The installer links into `~/.local/bin` and only warns when that is not on PATH (`src/superclaude/cli/install_codegraph.py:155-163`). If `~/.local/bin` is not on PATH, init will not resolve (UNVERIFIED in practice; note as a guide precondition).

### 2. `/sc:impact` — NEW

- Invocation: `/sc:impact parse_config`, `/sc:impact a b --depth 3`, `/sc:impact --diff`, `/sc:impact --diff origin/master --tests`, `--caller <skill> --output-dir <dir>` (`src/superclaude/commands/impact.md:20-25`). Flags: 1-30 bare symbols XOR `--diff [<base>]`; `--depth` 1-3 (default 2); `--limit` 1-100 (default 20); `--tests`; `--test-depth` 1-5 (`impact.md:29-38`).
- Expected: writes `<output-dir>/impact.md` (12 fixed sections) and `return-contract.yaml` (max 40 rows, 6 KB) (`impact.md:47-50`); default dir `<worktree_root>/.dev/impact/<slug>-<YYYYMMDDTHHMMSSZ>/` (`skills/sc-impact-protocol/SKILL.md:29`). Every row labelled `def-line`, `call-site-verified` or `unresolved`; `shown/total` counts (`impact.md:56-57`). Never stops its caller: codegraph missing/disabled/stale → Grep fallback and `status: partial` (`impact.md:13`, `SKILL.md:15`). With `--caller`, chat output shrinks to 3 lines (`impact.md:38`).
- Hand-test recipe: named symbol in an indexed checkout (expect `success`); same with `SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off` (expect `partial` + `graph:disabled`); `--diff` after a small local edit; `--tests`; both a symbol and `--diff` together (expect blocked). Check it never claims "no dependents" from an empty graph (`impact.md:63`).
- Consumers: `/sc:implement`, `/sc:pr-submit`, `/sc:troubleshoot --fix`, `/sc:auggie-review` call it (CHANGELOG.md:84).

### 3. Codegraph SessionStart auto-index hook + `SUPERCLAUDE_CODEGRAPH_AUTOINIT=0`

- Registration: `SessionStart` matcher `startup` → `~/.claude/hooks/codegraph-session-start.sh`, timeout 5 (`src/superclaude/hooks/hooks.json:23-31`).
- Behaviour (`src/superclaude/hooks/scripts/codegraph-session-start.sh`): exits 0 at once when `SUPERCLAUDE_CODEGRAPH_AUTOINIT=0` (line 11); binary from `~/.codegraph/.superclaude-bin`, else PATH (15-19); git top-level of `CLAUDE_PROJECT_DIR`/PWD, skipped for `$HOME` and `/` (21-22); skips when `<top>/.codegraph/codegraph.db` exists in any state (25); otherwise one detached `nohup codegraph init --yes <top>` logging to `${XDG_STATE_HOME:-~/.local/state}/superclaude/codegraph-init.log` (27-31). Prints nothing on stdout, never runs status/index/sync (6-8).
- Observable: new clone → after first `claude` start, `.codegraph/codegraph.db` appears and the log file grows; resume (not startup) does not trigger; `SUPERCLAUDE_CODEGRAPH_AUTOINIT=0 claude` → no `.codegraph/`. Cost: ~70 KB per file, up to ~1 GB memory at first init (CHANGELOG.md:93).

### 4. `SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off`

- Read by every primitive's readiness check: `printenv SUPERCLAUDE_CODEGRAPH_PRIMITIVES` = `off` → `index_state: disabled`, token `graph:disabled`, Grep/Glob/Read floor (`src/superclaude/core/CODEGRAPH.md:11`, `:26`, `:32`). Does not affect the hook (`CODEGRAPH.md:26`). `/sc:graph` reports `enable_codegraph` (`sc-graph-protocol/SKILL.md:54`).
- Test: export before `claude`, run `/sc:graph` and `/sc:impact <sym>`; both must continue (no stop) and name the switch.

### 5. Codegraph install / MCP registration (context for groups)

- Pin `1.6.2` (`src/superclaude/cli/install_codegraph.py:26`, `core/CODEGRAPH.md:34`); registration env `CODEGRAPH_TELEMETRY=0`, `CODEGRAPH_MCP_TOOLS=<seven tools>` (`src/superclaude/cli/install_mcp.py:855-872`). `superclaude install --list` codegraph block, `superclaude doctor` registration check, Serena / codebase-memory retire step (CHANGELOG.md:94-115). This is CLI surface; detail belongs to the CLI scanner, but group G1 needs it as a precondition.
- Core `CLAUDE.md` codegraph block between markers at `src/superclaude/core/CLAUDE.md:28-30`.

### 6. `/sc:save` + `/sc:load` file-based memory — CHANGED (breaking)

- Store: `<project>/.superclaude/memory/<key>.md`, `<project>` = `git rev-parse --show-toplevel` or cwd, one store per worktree (`src/superclaude/commands/save.md:42`, `load.md:42`).
- `/sc:save` first write creates `<project>/.superclaude/.gitignore` containing `*` (`save.md:43`); single-owner keys `pm_context`, `last_session`, `next_actions` overwritten; parallel keys (`checkpoint`, `decision`, handoffs) written as `<key>-<session-or-timestamp>.md` (`save.md:44-45`). Flags: `--type session|learnings|context|all`, `--summarize`, `--checkpoint` (`save.md:22`).
- `/sc:load`: reads `.superclaude/memory/`; legacy fallback reads `.serena/memories/<key>.md` only when the matching new file is absent, never writes there, and tells the user it is read-only history (`load.md:43`); ends its summary with a line pointing to `/sc:graph status` and never runs it (`load.md:53`). Fallback ends next release (`docs/releases/v5.0.0.md:198`).
- `/sc:pm` and the PM agent use the same store (`src/superclaude/commands/pm.md:16`, `:47`).
- Hand-test recipe: in a scratch repo `/sc:save` → check `.superclaude/memory/*.md` and `.superclaude/.gitignore` = `*`, `git status` shows nothing under `.superclaude/`; new session `/sc:load` → summary cites the saved content + `/sc:graph status` line; place `.serena/memories/last_session.md` with no new-store twin → `/sc:load` reads it and says read-only; then confirm `.serena/` unchanged. Second worktree → separate store (expected empty). Behaviour is LLM-driven (no script), so expected output wording is UNVERIFIED; check files, not phrasing.

### 7. `/sc:help` + `/sc:recommend` reading `HOW-WE-WORK.md` — CHANGED

- `/sc:help` runs four `find` listings (commands, skills, project-local, plugin), then prints verbatim the text between `<!-- level-table:v1 -->` and `<!-- /level-table -->` (`src/superclaude/commands/help.md:21-73`); markers exist at `src/superclaude/core/HOW-WE-WORK.md:11` and `:28`. Guide lookup order `~/.claude/HOW-WE-WORK.md` → plugin copy → `src/` copy, with the `src/` copy first inside an IronClaude checkout (`help.md:67-71`). Exact fallback messages for missing markers / missing guide (`help.md:75-81`), built-ins line naming `/code-review` and `/security-review` (`help.md:85`), and `-protocol` skills listed last (`help.md:59`). Writes nothing (`help.md:132`).
- `/sc:recommend` loads skill `sc-recommend` (`commands/recommend.md:56`); reads the guide first, matches a routing row and returns its steps with required flags; asks one question when ambiguous; otherwise enumerates surface + one auggie query (`recommend.md:44-48`). Flags: `--plugin`, `--eval none|quick|normal|deep`, `--minstar N` (default 500, ignored with a warning in local mode) (`recommend.md:32-38`). Advisory PreToolUse hook `sc-recommend-phase0.sh` only where registered in project `.claude/settings.json` (`recommend.md:60`); it is NOT in `hooks.json`.
- Hand-test recipe: `/sc:help` with the guide installed (table appears verbatim, compare to the guide); temporarily move `~/.claude/HOW-WE-WORK.md` outside an IronClaude checkout → exact "Routing guide not found" line; `/sc:recommend "Rename tz_offest to tz_offset in one file"` → level 2 native edit; `/sc:recommend "build feature X across 6 files"` → `/sc:workflow ... --depth standard --handoff none` then `/sc:implement`; `/sc:recommend "..." --minstar 10` → warning, ignored.

### 8. `/sc:pr-submit` — CHANGED

- Default `--monitor 3` (`src/superclaude/pr_submit/fsm.py:31`, `:77`; `commands/pr-submit.md:25`, `:46`). Ordinals: 0 open PR only; 1 arm+poll+propose; 2 fix locally, halt before push; 3 fix→push→reply→resolve (`pr-submit.md:35-38`). `--max-rounds` default 2, hard cap 5 (`pr-submit.md:47`; `fsm.py:33`, `:115`). `--poll-interval` ≥30, `--timeout` 600, `--silence-timeout` 300 (`pr-submit.md:48-50`). `--pr <N>` attach (`pr-submit.md:53`); `--resume <jsonl>` (`:56`); default output `.dev/pr-monitor/pr-<N>-<ts>/` (`:55`).
- Target repo from `origin` remote; STOP when the PR cannot be confirmed on it or when the checkout is not the PR head (`pr_head_mismatch`) (`pr-submit.md:28`). CI-wait preflight needs `gh pr checks --json` (`pr-submit.md:30`).
- Codex: bot `chatgpt-codex-connector[bot]`, re-trigger `@codex review`; local override `<repo-root>/.dev/pr-monitor/detection-contract.locked.md` (`pr-submit.md:66`). P0-P3 → Critical..Low; absent reviewer → `reviewer_absent`; dedup by path+line; per-reviewer re-trigger after a fixing push (CHANGELOG.md:49-54). Codex re-review marker update UNVERIFIED (CHANGELOG.md:54). Known issue: clean Augment "0 suggestions" may be recorded incomplete (`docs/releases/v5.0.0.md:234`).
- Removed: `--yes` (CHANGELOG.md:217). Test that it is rejected or ignored (behaviour on an unknown flag UNVERIFIED).
- Hand-test recipe (needs a sandbox branch on the fork, real reviewers, CI): `--monitor 0` opens PR only; `--monitor 1 --pr <N>` proposes only; `--monitor 2` edits locally and halts before push; bare `/sc:pr-submit --pr <N>` = level 3 and pushes; run from a different branch than the PR head → `pr_head_mismatch` HALT; `--max-rounds 6` rejected. Verify PR URL owner is `IronbellyOrg`.

### 9. Review loop cap (2 fix cycles; minor never fails)

- Rule text: `src/superclaude/output-styles/pragmatic.md:225-229` (blocking vs minor; at most 2 fix cycles / 3 reviews, then escalate). Injected into every subagent by the SubagentStart hook `pragmatic-subagent.js` (`src/superclaude/hooks/hooks.json:120-127`; script reads `~/.claude/output-styles/pragmatic.md` and exits 1 if missing, `hooks/scripts/pragmatic-subagent.js:7-21`). Applied to rf-qa agents, prd/tdd/task/task-builder skills, `/sc:tasklist` patch loop, `/sc:implement` A2 (CHANGELOG.md:30-33). CI guard `tests/skills/test_review_severity_rule.py` (CHANGELOG.md:37).
- Hand-testability: only observable inside long runs (`/tdd`, `/task-builder`, `/sc:tasklist`). Cheap proxy: inspect a subagent's injected context starts with `PRAGMATIC MODE ACTIVE`; full check needs a seeded spec with a persistent blocking defect and observing an escalation after review 3 (long).

### 10. ccsession features

Sources: `src/superclaude/skills/ccsession-tag/ccsession` (1617 lines), `ccsession-orca`, `models.py`, `local-gateway-alias-proxy.py`, hooks `session-start.sh` / `session-name.sh`, wired by `src/superclaude/cli/install_ccsession.py`.

- Install wiring: symlinks `~/.local/bin/ccsession` and `~/.local/bin/ccsession-orca`; seeds `~/.claude/ccsession.env` (mode 0600) from the example; runs `seed-env.py` (Coder gateway address); runs `ccsession --migrate-names` once (`install_ccsession.py:33-115`). Unmanaged existing links are left and warned (`:122-125`).
- Naming: `ccsession <name>` passes `--name` to Claude Code (`ccsession:1606-1608`); names may contain spaces (`ccsession "my work"`); `--name <n>` accepts a name starting with `-` (`ccsession:11-12`); `/rename` inside Claude Code syncs via `session-name.sh` on UserPromptSubmit and SessionEnd (`hooks.json:54-73`; CHANGELOG.md:61). Names belong to the repo, shared across worktrees (`ccsession --key`, `name_key()` at `ccsession:127`; CHANGELOG.md:174-180).
- Lists: `--list` all workspaces; `--here` this worktree + removed-worktree section + counts of other worktrees; `--here --all` every worktree of the repo (`ccsession:27-31`, `:1441-1448`); `--rm <topic>` deletes the label only (`:1454-1467`).
- `--ask [<hint>]`: prints list + question on the terminal, only the chosen name on stdout; `*` lists every worktree; exit 1 when not asked / timeout (`CCSESSION_ASK_TIMEOUT`) / EOF, 130 on Ctrl+C (`ccsession:47-53`; `ask_session_name()` at `:1324`).
- `ccsession-orca`: set as Orca Settings > Agents > Claude > Command; asks only when stdin+stdout are TTYs, not resuming (`--resume`, `-r`, `--continue`, `-c`), and `CCSESSION_AUTOSTART` ≠ 0; default ask timeout 30 s then untagged; always `--shim --claude-args "$@"` (`ccsession-orca:19-81`).
- Orca tab title `<label> · Claude Code` with `CLAUDE_CODE_DISABLE_TERMINAL_TITLE=1` when `ORCA_PANE_KEY` is set (`ccsession:1512-1528`).
- Tiers: tier mode when a `T<N>_WINDOW` exists in the workspace env file (`models.py:469-479`); `--tier 1a`/`tier1a`, `--model <name>` (`ccsession:57-66`); letter tiers regex `models.py:63-65`. `CCSESSION_TIER_RULES` grammar `<who>=<start>[:<tiers>][+models]`, precedence username > first matching `role:` > `*` (`models.py:72-79`, `:522-620`). `CCSESSION_ACCESS` is the older form read only without a rules line (`models.py:81-85`). Broken/duplicate entries stop the launch (`models.py:557-581`). Shim re-reads rules per request and limits the picker to allowed tiers (`local-gateway-alias-proxy.py:172-203`).
- Shim: shared per settings key on 127.0.0.1:4010 or nearby; survives its launching terminal; stop with `pkill -f local-gateway-alias-proxy.py` (`ccsession:798`; CHANGELOG.md:22). Running shims keep old behaviour until restarted (`docs/releases/v5.0.0.md:235`).
- Default launch flags `--dangerously-skip-permissions --allowedTools=Grep`, override with `CC_CLAUDE_FLAGS` (`ccsession:78-93`).
- Inspection commands: `ccsession --models-status`, `ccsession --refresh-models`, `ccsession --help` (`ccsession:1423-1435`).

### 11. ISSUE-HANDOFF / ISSUE-BACKLOG core files

- Shipped as core files (`src/superclaude/cli/install_core.py:21-22`); plain install skips existing copies (CHANGELOG.md:43). Sections: Handoff = What was tried / Relevant files and links / Done when / Who it is for (`core/ISSUE-HANDOFF.md:1,4,7,10`); Backlog = same first three + Pick-up note (`core/ISSUE-BACKLOG.md:1,4,7,10`).
- Rule: `src/superclaude/core/CLAUDE.md:43` (Core Rule 10: copy to temp, fill, `gh issue create --title ... --body-file <copy>`, never edit the template). An existing `~/.claude/CLAUDE.md` is not replaced without `--force` (CHANGELOG.md:44).
- Hand-test: after install, files exist at `~/.claude/ISSUE-*.md`; ask Claude to "file a backlog issue for X" in a sandbox repo and check it copies to a temp file, the installed template is unchanged (checksum), and the issue body has all four headings. Filing a real issue is an external side effect: use a throwaway repo.

### 12. Freshness hooks

- Registrations (`src/superclaude/hooks/hooks.json`): SessionStart `freshness-session-start.sh` (13-21), UserPromptSubmit `freshness-user-prompt.sh` (44-53, injects `<session-context>`), PreToolUse `Edit|Write` → `freshness-pre-edit.sh` (75-86), PostToolUse `Read` → `freshness-post-read.sh` async (87-98), SubagentStart/Stop freshness scripts (110-141). `freshness-file-changed.sh` is shipped but unregistered (CHANGELOG.md:423).
- Gate (`hooks/scripts/freshness-pre-edit.sh`): 30-minute horizon `FRESH_HORIZON=1800` (15); `Write` to a nonexistent path allowed as `create_allowed` (84); `no_prior_read` block (87, message 127); stale-read block (130); `external_change` mtime block (97-103, 133). Telemetry `~/.claude/logs/freshness-hook.jsonl`, reads in `~/.claude/state/reads.jsonl` (CHANGELOG.md:405-408).
- Observed live during this scan: a `Write` over an existing file created earlier in the same session (not Read) was blocked with `no_prior_read`, confirming that a `Write` to an existing unread file is gated even when this session created it.
- Hand-test: in a session, Edit an unread file → FRESHNESS BLOCK `no_prior_read`; Read then Edit → allowed; Write a new path → allowed; modify the file from a shell after Read, then Edit → mtime block. Cheap.
- Also hooks shipped: `auggie-flag-clear.sh` (PostToolUse auggie), `reject-workspace-writes.sh` and `sc-recommend-phase0.sh` (project `.claude/settings.json` only, not in `hooks.json`).

## Proposed guide groups

| # | Guide | Covers | Cost | Preconditions |
|---|---|---|---|---|
| G1 | Codegraph: auto-index, `/sc:graph`, `/sc:impact` | §1-5; kill switches; nested worktree `--worktree-local`; telemetry line | cheap (15-25 min) | `superclaude install` done, codegraph 1.6.2 registered, `~/.local/bin` on PATH, a scratch git repo with some Python |
| G2 | Session memory: `/sc:save`, `/sc:load`, `/sc:pm` | §6; `.serena` fallback; per-worktree stores; `.superclaude/.gitignore` | cheap | scratch repo; optional fake `.serena/memories/` |
| G3 | Routing: `/sc:help`, `/sc:recommend`, `HOW-WE-WORK.md` | §7; retired core files and `/sc:README` absent; `business-panel` "(no description line)" | cheap | install done; ability to move the guide temporarily |
| G4 | Planning chain: `/sc:workflow` → `/sc:implement` (+ `/sc:impact` call, review cap) | level-3 route, `progress.md`, resume, archive to `.dev/tasks/done/` (Linux only), §9 escalation | long | scratch repo with a small feature |
| G5 | PR flow: `/sc:pr-submit` | §8 ordinals 0-3, `--pr`, head-mismatch HALT, Codex/Augment absent handling, max-rounds cap | long (real PR + reviewers + CI) | sandbox branch on `IronbellyOrg/IronClaude` or a throwaway fork; Augment and/or Codex apps installed (UNVERIFIED availability) |
| G6 | ccsession (user) | §10: names with spaces, `/rename` sync, `--here`/`--here --all`/`--list`/`--rm`, `--ask`, `ccsession-orca` in Orca, tab title, `--tier`/`--model`, `--models-status`, shim survives terminal close | medium | Coder workspace with tier env; Orca for the Orca steps |
| G7 | Hooks: freshness gate, session-context envelope, pragmatic SubagentStart, auggie flag | §12, §9 cheap proxy | cheap | install done; `jq`, `node` present |
| G8 | Issue templates | §11 | cheap | throwaway GitHub repo, `gh` authenticated |
| G9 (E) | ccsession tier administration | Sysop rows S1-S4 below: role/username/`*` rules, broken-line lockout, `CCSESSION_ACCESS` back-compat, advisory-limit bypass check | medium | Coder admin access to the template / `/etc/aidev02/aienv.d/defaults.sh`; test users with `member` and `auditor` roles |

## Sysop-only candidates

| ID | Capability | Gate / evidence | Classification |
|---|---|---|---|
| S1 | Per-user/per-role tier policy `CCSESSION_TIER_RULES` (and legacy `CCSESSION_ACCESS`, `CCSESSION_DEFAULT_TIER`, `CCSESSION_MODEL_ORDER`, `T<N>ModelNN`, `T<N>_WINDOW`) | Read from the workspace env file `/etc/aidev02/aienv.d/defaults.sh` (`models.py:104`, `:454-466`), pushed from the Coder template `templates/VSCode-AIDev02/aienv.d/defaults.sh` (`ccsession-tag/MODEL-TIERS.md:9`); "the central file is changed only through review" (`ccsession-tag/README.md:354`). A bad line "stops ccsession for every Coder user until it is fixed" (`README.md:332-336`) | **Sysop-only** (affects all workspace users) |
| S2 | Coder role assignment that feeds `role:` entries (`owner`, `user-admin`, `template-admin`, `auditor`, `member`) | `CODER_WORKSPACE_OWNER_ROLES` set by the Coder template (`models.py:509-518`; `README.md:318-328`) | **Sysop-only** (Coder admin) |
| S3 | Real enforcement of tier limits | ccsession limit is advisory; owner can undo it via `CODER_WORKSPACE_OWNER_NAME`, `CODER_WORKSPACE_OWNER_ROLES`, `AIDEV_AI_DEFAULTS_PATH`, `CCSESSION_TIERS=0`; "Only a gateway key limited to those models enforces it" (`README.md:348-352`; `models.py:320-328`, `:476`) | **Sysop-only** (LiteLLM key scoping; outside this repo, UNVERIFIED). Guide should document the bypass as expected, not a bug |
| S4 | Published model data `ccsession-models.json` (tier layout, picker rules) | Every launch fetches from `raw.githubusercontent.com/IronbellyOrg/IronClaude/master/...` (`models.py:54-57`, `:298`); a push to master changes every install's picker. User can override with `CCSESSION_MODELS_URL` / skip with `CCSESSION_MODELS_REFRESH=0` (`ccsession:73-76`) | **Sysop-only** to publish (repo maintainer); ordinary to override |
| S5 | LiteLLM MCP gateway entry `superclaude mcp --servers litellm` (`http://ibcore:4000/mcp/`, header `x-litellm-api-key: Bearer ${LITELLM_API_KEY}`) | `src/superclaude/cli/install_mcp.py:107-112`; opt-in, skipped by "all servers" (`install_mcp.py:1359`) | Ordinary user to register; **sysop dependency**: gateway host and key issuance (UNVERIFIED) |
| S6 | Coder image reinstalling Serena / codebase-memory registrations | Retire step keeps "a registration Coder's bundle also writes"; "Coder workspaces reinstall it at start" (CHANGELOG.md:111, :131) | **Sysop-only** (Coder template); user can only remove user-scope entries |
| S7 | `CCSESSION_SHOW_ALL_MODELS=1` | Labelled "Admin options" (`README.md:296-299`) but no gate: plain env var, own shim (`models.py:744`) | Ordinary user (documented as admin; not gated) |
| S8 | Shim lifecycle `pkill -f local-gateway-alias-proxy.py` | Shim shared by all of this user's sessions with the same settings key (`ccsession:798`; CHANGELOG.md:22). Owners with different roles never share a shim (CHANGELOG.md:162) | Ordinary user, but kills replies for every session of that user in the workspace; flag in guide |
| S9 | `ccsession` launches with `--dangerously-skip-permissions` by default | `ccsession:78-93` (`CC_CLAUDE_FLAGS`) | Ordinary user behaviour; **sysop security note** (policy decision for workspace images) |
| S10 | Codegraph kill switches `SUPERCLAUDE_CODEGRAPH_AUTOINIT=0`, `SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off` | `codegraph-session-start.sh:11`; `core/CODEGRAPH.md:11,26` | Ordinary user; operator-recommended for CI/headless (CHANGELOG.md:93) |
| S11 | `AUGGIE_FIRST_DISABLE=1` | `hooks/scripts/freshness-user-prompt.sh:134`, `auggie-flag-clear.sh:8` | Ordinary user kill switch |
| S12 | Freshness / pragmatic / codegraph hook opt-out | Hooks are user scope only, in `~/.claude/settings.json`; opt out by removing entries (CHANGELOG.md:433) | Ordinary user (no admin privilege) |
| S13 | `ccsession-orca` as Orca's Claude command; `CCSESSION_AUTOSTART=0`, `CCSESSION_ASK_TIMEOUT` | Per-user Orca setting (`ccsession-orca:7-28`) | Ordinary user |
| S14 | `/sc:pr-submit --monitor 3` pushes without asking; detection-contract override | `pr-submit.md:46`, `:66` | Ordinary user (needs repo write); not sysop |
| S15 | CLI env gates outside this slice: `SUPERCLAUDE_SPRINT_ASSUME_YES`, `SUPERCLAUDE_PROMPT_MAX_BYTES`, `SUPERCLAUDE_SPRINT_RENDER_DIAG`, `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` | `cli/sprint/commands.py:231`, `cli/pipeline/process.py:25`, `cli/sprint/tui.py:113`, `cli/reflect/runner.py:56` | Hand off to the CLI scanner; not classified here |

Determination: only S1-S4 and S6 are sysop-only (require Coder template/admin rights, the central env file, gateway key policy, or the fork's master). Everything else is ordinary-user, gated by the user's own environment or `~/.claude/settings.json`. No capability in this surface requires sudo inside a workspace, and nothing in this surface acts on another user's sessions except through the shared central env file (S1) and published model data (S4).

## Self-audit

- Read directly: `commands/{graph,impact,save,load,help,recommend}.md` (whole), `pr-submit.md` (grep of flags/lines), `skills/sc-graph-protocol/SKILL.md` (1-159), `core/CODEGRAPH.md` (1-70), `hooks/hooks.json`, `hooks/scripts/codegraph-session-start.sh`, `ccsession-orca`, `cli/install_ccsession.py`, `ccsession` (1-100, 630-670, 1415-1474 + greps), `models.py` (1-110, 316-329, 454-498, 520-649), `local-gateway-alias-proxy.py` (170-209), `ccsession-tag/README.md` (270-379), `cli/install_codegraph.py` (150-239), CHANGELOG 5.0.0 section (lines truncated at 400 chars), release notes 192-235.
- Grep-only (not fully read): `sc-impact-protocol/SKILL.md`, `freshness-pre-edit.sh`, `freshness-user-prompt.sh`, `pragmatic.md`, `fsm.py`, `install_mcp.py`, `install_core.py`, ISSUE templates (headings only), `HOW-WE-WORK.md` (markers only), `session-start.sh`.
- Not read: the 30+ protocol skills behind long-running commands, the 46 agents, `sc-pr-submit-protocol/SKILL.md`, `session-name.sh`, `seed-env.py`. Cost labels for those are judgement from descriptions (UNVERIFIED).
- UNVERIFIED items: `/sc:graph init` when `~/.local/bin` is off PATH; `/sc:save`/`/sc:load` exact chat wording (LLM-driven, no script); `/sc:pr-submit --yes` rejection behaviour; Codex re-review marker; Augment/Codex app availability on the fork; LiteLLM gateway key scoping; whether `/sc:post-release` is new in 5.0.0.
- Changelog line numbers are from `CHANGELOG.md` directly (the `## [5.0.0]` heading is line 7). Line numbers are valid at HEAD == v5.0.0.
- No repo file other than this one was written. No install or state-writing command was run.
