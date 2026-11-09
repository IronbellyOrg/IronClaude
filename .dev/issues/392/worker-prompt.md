# Worker brief: issue #392, ccsession tier failover

You are working in the Orca worktree `/home/coder/workspaces/worktrees/IronClaude/ccsession-failover-392`, branch `clayphi/ccsession-failover-392`, based on `origin/master` (it already contains PR #391). Stay in this folder for all work. Do not `cd` to the main checkout, and do not create another worktree.

## Goal

Implement GitHub issue #392 exactly as corrected and confirmed by the owner on 2026-11-09. The issue body is the spec. Successful HTTP replies stream immediately and unchanged; do not buffer or inspect events before forwarding. Read it first:

```bash
gh issue view 392 --repo IronbellyOrg/IronClaude
```

In short:
- **A.** Every server error (408, 429, 500, 502, 503, 504 not on the existing switch list, or a cut-off error reply) counts against its model. Below 3 failures in a row, the error goes back to Claude Code so it retries. The 3rd failure parks the model and sends the same request to the next model. Parks last 5 minutes, then double to 10, 20 and 40 minutes, capped at 1 hour; a success resets both the count and the park length. Out-of-usage errors (the existing `SWITCH_RULES`) still switch at once and park for `Retry-After` or the cooldown. Errors that are the request's own fault are never switched.
- **C.** In tier mode, a request that names one model falls back within the tier where that model is listed highest (ties go to the higher tier), and only within tiers the person's role may use.
- **D.** The shim keeps its log by default at `${XDG_CACHE_HOME:-$HOME/.cache}/ccsession/proxy.log`, capped at 5 MB with one older copy, and never logs a key, token, authorization header or request body.

If anything in the spec looks wrong or cannot work as written, stop and ask the user in plain English in the chat. Never change a decision on your own.

## Files

- `src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py`: the shim. The relevant parts are `SWITCH_RULES`, `cool_down`, `_post`, `_forward_tier`, `_proxy`, `_stream` and `audit`.
- `src/superclaude/skills/ccsession-tag/models.py`: tier data and access (`tier_access`, `resolve_tiers`). Change it only if C needs it.
- `tests/unit/test_ccsession_tiers.py`: it contains a scripted fake gateway (around lines 585-750, the `shim` fixture, `_ask`, `_ask_raw`) and the existing failover tests (`test_out_of_usage_switches_and_cools_down` onward). Build on it.
- `src/superclaude/skills/ccsession-tag/README.md` (the failover table around line 420) and `CHANGELOG.md`.
- Read `CLAUDE.md` in this worktree and follow it.

## Workflow, in order

1. **Read** the issue, the shim, the test harness and the README failover section. Trace how a tier request and a single-model request flow today before changing anything.
2. **Tests first.** Add a test for every item in the issue's "Tests" list. Run them and confirm each one fails on the unchanged shim for the right reason. Save the output to `.dev/issues/392/red.log`.
3. **Implement** A, C and D in the shim. Keep every other behaviour unchanged. Add the new settings `CCSESSION_FAILS_BEFORE_SWITCH`, `CCSESSION_PARK_SECONDS` and `CCSESSION_PARK_MAX_SECONDS` with the spec's defaults.
4. **Update the two existing tests the spec names** (`test_named_model_has_no_failover`, `test_errors_outside_the_rules_pass_back_unchanged`) to the new rules. Every other existing test must pass unchanged.
5. **Docs.** Update the README failover table, the cooldown row and the admin options paragraph, the `ccsession --help` lines that say "no failover" for `--model`, and `CHANGELOG.md`.
6. **Validate**, saving each output under `.dev/issues/392/`:
   - `uv run --extra dev pytest tests/unit/test_ccsession_tiers.py tests/unit/test_ccsession_tag.py tests/unit/test_cli_doctor.py tests/unit/test_cli_install.py tests/unit/test_install_ccsession.py tests/hooks tests/core tests/commands tests/recommend tests/skills -q`
   - then the whole suite once: `uv run --extra dev pytest -q`
   - `uv run --extra dev ruff check .` and `uv run --extra dev ruff format --check src/ tests/`
   - `make verify-sync` (if `make` is missing, run its recipe from the Makefile by hand).
   - Known: `tests/unit/test_ccsession_tiers.py::test_shim_outlives_the_terminal_that_started_it` fails in this Coder workspace on unchanged master too (issue #352). If it or any other test fails, run it against `origin/master`'s shim before deciding whether your change caused it, and record the result.
7. **End-to-end test on this machine** (scripts and logs under `.dev/issues/392/e2e/`):
   - Start the new shim from this worktree on a free port of its own (`GW_PROXY_PORT`), with its upstream pointed at a scripted fake gateway that returns valid Anthropic-format streamed replies. Run the real `claude` command against it (`ANTHROPIC_BASE_URL=http://127.0.0.1:<port>`, `claude -p "Reply with the word OK" --model <name>`). Show at least: a tier request whose first model fails three times with 500 and that is then answered by the next model, with Claude Code's own retries driving the count; a single-model request for `claude-opus-5-5` that hits an out-of-usage error and is answered by Claude Sonnet 5.5; a streamed reply (including pings and error events) passed straight through without waiting for a later event; and the log file showing each failure, park and switch.
   - Then a live smoke test: the new shim on its own port against the real gateway upstream (the `upstream` value in the running shim's health page, `curl -s http://127.0.0.1:4078/__ccsession_shim`). Check that one tier request (`--model claude-gw-tier2`) and one single-model request (`--model claude-opus-5-5`) answer normally, and that the log records the model that answered.
   - **Never stop, restart or replace the shared shim the user's sessions run on** (the process serving `$ANTHROPIC_BASE_URL`, port 4078). Use only new ports, and stop your own test shims when you are done.
   - Read credentials only from the environment (for example `ANTHROPIC_AUTH_TOKEN`). Never print, log or write a key or token to any file.
8. **Commit** the source, tests, docs and `.dev/issues/392/` files with a conventional message (`fix(ccsession): ...`), ending with `Co-Authored-By: Claude Code <noreply@anthropic.com>`. Never stage anything under `.claude/` (see CLAUDE.md).
9. **Open the PR** with `/sc:pr-submit --monitor 3 --max-rounds 3 --head clayphi/ccsession-failover-392 --title "fix(ccsession): tier failover retries then switches on every server error, and covers single models (#392)" --body "<summary, test evidence, Closes #392>"`. Follow that skill to the end: review findings, fixes, replies, CI.
10. **Report** to the user: a DONE / NEXT table, the PR link, the test counts, and what the end-to-end and live runs showed.

## Rules for this session

- Do not launch any subagent, fork or background agent. Where a skill says to spawn an agent (for example the evidence check in `/sc:pr-submit`), do that step yourself, inline.
- Ask the user questions in plain English in the chat. Never use the AskUserQuestion pop-up tool.
- Use `uv` for every Python command.
- Never write an API key, token or other secret into a file, a log or the chat.
- Plain English in every message to the user, and no internal codes without saying what they mean.
