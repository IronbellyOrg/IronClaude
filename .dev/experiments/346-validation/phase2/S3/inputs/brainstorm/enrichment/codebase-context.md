# Codebase context: launch-level hook (issue #394)

quality_tier: fallback_1 (the auggie MCP server is not available in this session; native Read, Grep, Bash and Glob were used)
gathered: 2026-11-05, worktree `hook-launch-level-394`, branch `ironbelly/hook-launch-level-394`

## 1. Where hook code lives and how it ships

| Fact | Evidence (read this session) |
|---|---|
| Hook scripts are in `src/superclaude/hooks/scripts/*.sh` and `*.js`; `make sync-dev` copies them to `.claude/hooks/` | `Makefile` lines 137-146; `make verify-sync` diffs both sides (lines 255-275) |
| Hook registrations for installed users are in `src/superclaude/hooks/hooks.json`; `superclaude install` merges them into `~/.claude/settings.json` (additive, atomic, backup first, ownership by command path) | `src/superclaude/cli/install_hooks.py` `_merge_settings` |
| Every script in `scripts/` must also be listed in `_FRESHNESS_SCRIPTS` or `make verify-sync` fails | `Makefile` lines 308-325; `install_hooks.py` line 42 |
| Project-only registrations (used by `reject-workspace-writes.sh`, `sc-recommend-phase0.sh`) live in the tracked `.claude/settings.json` and use `$CLAUDE_PROJECT_DIR/.claude/hooks/<name>` | `.claude/settings.json` |
| `hooks.json` today registers PreToolUse for `Edit|Write` (freshness) and `Bash` (`block-bare-python.sh`, timeout 3). It has no `UserPromptExpansion` entry and no `Skill`/`Agent` PreToolUse entry | `src/superclaude/hooks/hooks.json` |
| `src/superclaude/hooks/README.md` is stale (talks about `plugins/superclaude/hooks/`); do not rely on it | read this session |

## 2. The closest existing example: `block-bare-python.sh` (issue #357)

- Contract: JSON on stdin, `jq` to read it, block = one message on stderr plus `exit 2`, never `exit 1`, fail open when `jq`/`awk` is missing or the input is not understood.
- It parses shell with a 300-line stateful `awk` scanner. Its header lists nine "known ceilings" it does not catch (for example `bash -c "python3 x"`, `xargs python3`, `${CMD:-python3}`), and its test file `tests/hooks/test_block_bare_python.py` holds over 100 named cases added across three PR review rounds (comments "PR #359 review round 1/2/3"). Lesson for #394: real shell parsing is a large, slow-to-finish edge-case sink.
- Test pattern: run the real script with `subprocess.run([bash, HOOK], input=json_bytes, env={HOME: tmp_path})`, assert exit code and stderr text, and assert `elapsed < 1` second. Reusable for #394.

## 3. State conventions already in use

- `~/.claude/state/` holds per-session files keyed by `session_id` (turn counters, background agent counters, flags), written with `flock` and sanitised ids (`case "$SESSION_ID" in *[!A-Za-z0-9._-]*) ...`). `freshness-subagent-start.sh` reads `.session_id` from the payload. A launch-level store can follow the same convention.
- `reject-workspace-writes.sh` shows the plain-words deny pattern: a "what was blocked, what to do instead, why" message on stderr, `exit 2`.

## 4. Skill tool payload shape used in this repo

`sc-recommend-phase0.sh` reads `tool_name == "Skill"` and `tool_input.skill // tool_input.name`. It is advisory and has never been shown to fire, so the field names are UNVERIFIED against the official docs (see `research-light.md`).

## 5. The claim feature is not in this worktree yet

`src/superclaude/skills/sc-issue-protocol/` has `SKILL.md`, `refs/{chains,claim,create,labels,tiers}.md`, `scripts/` and `templates/`. `scripts/orca_worktree.py`, `templates/launch-prompt.md` and `pipeline.json` do not exist. Everything the hook needs from the claim side is therefore an interface request, listed in `seed-brief.md` under "Interface requests to the claim feature".

## 6. Facts from the launch evidence (`.dev/evals/ccsession-orca-e2e-20261026/EVIDENCE.md`, main checkout)

- The launched `claude` process is started by the ccsession shim with `--dangerously-skip-permissions --allowedTools=Grep --settings <json> --model ...`, then Orca's own arguments unchanged; the prompt is the last argument, byte for byte.
- The process environment holds `CLAUDE_TOPIC`, `CCSESSION_PROFILE`, `ANTHROPIC_BASE_URL`, `ANTHROPIC_AUTH_TOKEN` (set), `ANTHROPIC_API_KEY` (unset). An environment channel from the shim to the hook therefore exists in principle, but the shim is out of scope for #394.
- `--resume <id>` keeps the same transcript id; `--resume <id> --fork-session` creates a new one.

## 7. Related worker rules the hook must not contradict (`~/.claude/WORKER-CONTRACT.md`)

- WC-9: a worker run has every outward action off (push, merge, PR, GitHub post). `--submit` is the one case where a launched agent is allowed outward actions, so it only fits if the launched session is not a "worker run" (UNVERIFIED: whether Orca adds a worker preamble to `orca agent launch` sessions).
- WC-13: a worker never calls `orca agent launch` or `worktree create --agent`. The hook's escape rules (block `orca`, `claude`, `ccsession` as command words) agree with this.
- Never-as-worker list contains `/sc:issue`, `/sc:pr-submit`, `/sc:git`, `/sc:spawn`, `/sc:pm`, `/sc:agent`, `/sc:swarm-wizard`.
