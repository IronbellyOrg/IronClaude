# Claude Code Hooks — Community / Open-Source Patterns

Research date: 2026-05-12
Scope: GitHub, dotfiles, dev blogs, Reddit/HN, LinkedIn, and Anthropic issue tracker. Focus on patterns from roughly the last 6 months (late 2025 through May 2026).
Coverage: ~25 distinct community patterns across the six requested buckets, plus the top three failure modes that recur across sources.

> Note: "Context budget" estimates are rough — most hook authors don't publish token counts, so values below are derived from the rough size of the stdout / `additionalContext` payload (≈ 4 characters per token).

---

## 1. Pattern catalog

### Telemetry / observability

| # | Purpose | Event | Command shape | Context budget | Pitfalls reported | Source |
|---|---|---|---|---|---|---|
| T1 | Append every Bash command to a flat log | PostToolUse(Bash) | `jq -r '.tool_input.command' >> ~/.claude/command-log.txt` | 0 (file only, no model context) | None — pattern is the canonical Anthropic example | [code.claude.com/hooks-guide](https://code.claude.com/docs/en/hooks-guide) |
| T2 | JSONL audit trail of every tool call with ok/error flag | PostToolUse(*) | `jq -c '{ts: now, session: .session_id, tool: .tool_name, input: .tool_input, ok: (.tool_response.is_error \| not)}' >> ~/.claude/audit.jsonl` (with `async: true`) | 0 | Must use `async: true` or the agent loop stalls — author reports "hundreds per session" | [thomas-wiegold.com](https://thomas-wiegold.com/blog/claude-code-hooks/) |
| T3 | Lifecycle telemetry to local dashboard ("ap" CLI) | SessionStart, PreToolUse, Stop | Emits events over local socket to `@agentic-patterns/cli` dashboard | 0 | "Telemetry hooks silently no-op when `ap` is absent" — fail-open by design | [github.com/pattern-stack/claudecode-patterns](https://github.com/pattern-stack/claudecode-patterns) |
| T4 | Full JSON log per event-type in `logs/*.json` (12 files) | All 12 events | Python UV single-file scripts that dump payload per event | 0 | Authors stress logs balloon fast; rotate manually | [github.com/disler/claude-code-hooks-mastery](https://github.com/disler/claude-code-hooks-mastery) |
| T5 | Session recorder ("proof-log") — daily summary of work | SessionEnd | `proof-log-session.sh` writes per-day markdown summary | 0 | Built specifically because manual daily-summary generation got skipped | [dev.to/yurukusa](https://dev.to/yurukusa/10-claude-code-hooks-i-collected-from-108-hours-of-autonomous-operation-now-open-source-5633) |
| T6 | Decision-warn — non-blocking alert when monitored paths edited | PreToolUse(Edit\|Write) | grep file_path against monitored list, log + warn, exit 0 | ~50 tokens (stderr message) | Non-blocking by design; "doesn't block, just notifies" | [dev.to/yurukusa](https://dev.to/yurukusa/10-claude-code-hooks-i-collected-from-108-hours-of-autonomous-operation-now-open-source-5633) |

### Safety / guardrails

| # | Purpose | Event | Command shape | Context budget | Pitfalls reported | Source |
|---|---|---|---|---|---|---|
| S1 | Bash firewall — block `rm -rf /`, fork bombs, `curl \| sh`, force-push to main, `git reset --hard`, `chmod 777` | PreToolUse(Bash) | bash/node script grep-E's command against pattern list, exit 2 on match | ~30–80 tokens (error message echoed to Claude) | "Exit code 1 means error and continues anyway. Use exit 2." Pattern lists need ongoing whack-a-mole maintenance | [karanbansal.in](https://karanbansal.in/blog/claude-code-hooks/), [steve-adams.me](https://steve-adams.me/claude-code-deny-list-is-leaky.html) |
| S2 | Glob-deny-list is leaky — replace with regex over full command string | PreToolUse(Bash) | regex matches `git\s+commit`, `git\s+push`, `git\s+reset\s+--hard` regardless of flags/env wrappers (`GIT_DIR=…`, `git -c …`, `pushd && cmd`) | ~50 tokens | "Glob patterns aren't a great security strategy. LLM is Dr. Strange of constructing 14M future commands you can't anticipate." | [steve-adams.me](https://steve-adams.me/claude-code-deny-list-is-leaky.html) |
| S3 | Secret-protection — block reads/writes of `.env`, `~/.ssh/id_*`, `~/.aws/credentials`, `~/.kube/config`; block `cat .env`, `printenv`, `curl -d @.env` | PreToolUse(Read\|Edit\|Write\|Bash) | node/python script with extensive path + bash-command regex list | ~40 tokens on block | Author notes secrets can leak via subtle channels (`echo $API_KEY`, exfil via `curl -F`) so list must cover bash too | [karanb192/claude-code-hooks](https://github.com/karanb192/claude-code-hooks) |
| S4 | Block edits on `main`/`master` branch | PreToolUse(Write\|Edit\|MultiEdit) | shell hook reads current branch, exits 2 if it matches `main\|master` | ~30 tokens | Pairs naturally with feature-branch-only workflow | [github.com/datasci-iopsy/.dotfiles](https://github.com/datasci-iopsy/.dotfiles) |
| S5 | Block destructive cloud / package commands (`bq rm`, `gcloud delete`, `uv cache clean`, `pip uninstall`) | PreToolUse(Bash) | regex list of platform-specific destructive commands | ~30 tokens | One author's CLAUDE.md says "use `mv <target> ~/.Trash/`" instead of `rm` | [reddit.com/r/ClaudeCode](https://www.reddit.com/r/ClaudeCode/comments/1rltiv7/inside_a_116configuration_claude_code_setup/) |
| S6 | Block em-dashes in writes (style enforcement) | PreToolUse(Write\|Edit\|MultiEdit\|NotebookEdit) | `block-em-dash.sh` greps tool_input.content | ~20 tokens | Niche but well-defined; demonstrates content-level hooks not just command-level | [github.com/datasci-iopsy/.dotfiles](https://github.com/datasci-iopsy/.dotfiles) |
| S7 | Error-gate — block `git push`, `npm publish`, `curl POST` when error log has unresolved entries | PreToolUse(Bash) | greps error-log file for unresolved entries before allowing publish-class commands | ~40 tokens | Built after a broken-npm publish; "the gate between 'run the code' and 'push to production' was missing" | [dev.to/yurukusa](https://dev.to/yurukusa/10-claude-code-hooks-i-collected-from-108-hours-of-autonomous-operation-now-open-source-5633) |
| S8 | Block secrets at commit time (plugin: commit-helper) | PreToolUse(Bash matching `git commit`) | scans staged diff for high-entropy strings / known secret patterns | ~50 tokens | Designed as a plugin so it's portable across repos | [github.com/MuhammadUsmanGM/claude-code-best-practices](https://github.com/MuhammadUsmanGM/claude-code-best-practices) |
| S9 | Block destructive git (`git push --force`, `git clean -f`, `git branch -D`, `git checkout .`, `git restore .`) | PreToolUse(Bash) | "safe by default" rather than "never allow"; user customizes during install | ~30 tokens | Author admits any user can override; presented as a friction nudge, not crypto | [aihero.dev](https://www.aihero.dev/this-hook-stops-claude-code-running-dangerous-git-commands) |

### Context enrichment

| # | Purpose | Event | Command shape | Context budget | Pitfalls reported | Source |
|---|---|---|---|---|---|---|
| C1 | Inject git status + recent TODOs at session start | SessionStart | `echo '## Git Status' && git status --short && echo '## TODOs' && grep -r 'TODO:' src/ \| head -5` | ~100–500 tokens depending on repo | "Once injected, text is saved in transcript. Resuming replays the saved text rather than re-running the hook" — timestamps go stale | [claudefa.st](https://claudefa.st/blog/tools/hooks/hooks-guide), [code.claude.com](https://code.claude.com/docs/en/hooks) |
| C2 | Inject current date/time, session ID, project structure, coverage stats | SessionStart (one of 17 stacked hooks reported) | bash scripts that write into `additionalContext` | ~5,000+ tokens for the 17-hook stack reported in issue #23875 | "Users have no way to see what was actually injected … debugging and transparency gap" — author has 17 hooks injecting ~5KB+ | [github.com/anthropics/claude-code issue #23875](https://github.com/anthropics/claude-code/issues/23875) |
| C3 | Behavioral-rules surfacing per prompt | UserPromptSubmit | `surface-behavioral-rules.sh` reads `~/.claude/rules/*.md` and appends relevant ones | varies (rules files) | Author warns to phrase as factual statements, not imperatives — imperative phrasing triggers Claude's prompt-injection defenses | [github.com/datasci-iopsy/.dotfiles](https://github.com/datasci-iopsy/.dotfiles), [code.claude.com](https://code.claude.com/docs/en/hooks) |
| C4 | Skill activation — match prompt keywords against rules file and append skill context | UserPromptSubmit | `node .claude/hooks/SkillActivationHook/skill-activation-prompt.mjs` against 21 skill categories | varies; ~200–800 tokens per matched skill | Stacked skills can blow context budget fast | [claudefa.st](https://claudefa.st/blog/tools/hooks/hooks-guide) |
| C5 | Load persistent project memory (claude-mem) | SessionStart + UserPromptSubmit + PreToolUse(Read) + PostToolUse + SessionEnd | external worker-service + `context-hook.js`; injects via `hookSpecificOutput.additionalContext` | ~1,000–4,000 tokens per session start (p95 120ms execution) | "As of Claude Code 2.1.0, SessionStart no longer displays user-visible messages — context is silently injected" — visibility gap | [docs.claude-mem.ai](https://docs.claude-mem.ai/hooks-architecture) |
| C6 | Maintenance-check + ensure-repo-hooks per prompt | UserPromptSubmit | scripts validate environment health before each turn | small (warnings only) | Stacking many UserPromptSubmit hooks adds latency to every turn | [github.com/datasci-iopsy/.dotfiles](https://github.com/datasci-iopsy/.dotfiles) |
| C7 | PDF-as-text rewrite via `updatedInput` | PreToolUse(Read) | hook extracts PDF text to a temp file, returns `hookSpecificOutput.updatedInput = {file_path: $TMPFILE}` | saves ~50,000 tokens vs. PDF-as-images on a 33-page doc — author's "favorite hook" | "Claude thinks it's reading the PDF. It's actually reading a text file. 95% smaller, no behavior change." Demonstrates `updatedInput` field | [reddit.com/r/ClaudeCode](https://www.reddit.com/r/ClaudeCode/comments/1rltiv7/inside_a_116configuration_claude_code_setup/) |

### Freshness / staleness detection

| # | Purpose | Event | Command shape | Context budget | Pitfalls reported | Source |
|---|---|---|---|---|---|---|
| F1 | Compact Python tracebacks before they enter context | UserPromptSubmit + PostToolUse(Bash) | `claude-tools` Python lib scores frames by relevance; replaces traceback with `<COMPACT_PY_TRACEBACK …>` summary (~40 tokens vs. multi-KB) | -90% vs. raw traceback | Unified script auto-detects which event fired; user must configure both hooks for full coverage | [github.com/tarekziade/claude-tools](https://github.com/tarekziade/claude-tools) |
| F2 | Compact-trace on PreCompact | PreCompact | `compact-trace.sh` snapshots transcript before compaction | ~0 (writes file) | Useful when compaction loses important context | [github.com/tarekziade/claude-tools](https://github.com/tarekziade/claude-tools) |
| F3 | Stop-hook git-check — surface uncommitted diffs at end of turn | Stop | `stop-hook-git-check.sh` runs `git status` and surfaces dirty state | ~50–200 tokens | Risks infinite loop if it issues a follow-up prompt (see common pitfalls below) | [github.com/datasci-iopsy/.dotfiles](https://github.com/datasci-iopsy/.dotfiles) |
| F4 | "additionalContext stales on resume" — author explicit advice | SessionStart (resume matcher) | re-run hook on `source: "resume"` rather than relying on saved transcript | varies | "Time-sensitive data goes in SessionStart (which re-runs with `source: "resume"`), not in PostToolUse (which replays the saved string)" | [thomas-wiegold.com](https://thomas-wiegold.com/blog/claude-code-hooks/) |
| F5 | Version-check at session setup (claude-mem) | Setup | `version-check.js` <100ms; flags stale installs via stderr, non-blocking | ~30 tokens stderr | Pattern designed to stay fast; p99 = 40ms for marker match | [docs.claude-mem.ai](https://docs.claude-mem.ai/hooks-architecture) |
| F6 | FileChanged event (v2.1.x) — re-read modified files | FileChanged | matcher e.g. `.envrc\|.env`; no decision control | small | Newer event; community examples still thin | [code.claude.com hooks ref](https://code.claude.com/docs/en/hooks), [claudelog.com release notes](https://www.claudelog.com/faqs/claude-code-release-notes/) |

### Workflow automation

| # | Purpose | Event | Command shape | Context budget | Pitfalls reported | Source |
|---|---|---|---|---|---|---|
| W1 | Auto-format on write | PostToolUse(Edit\|Write\|MultiEdit) | `npx prettier --write "$CLAUDE_TOOL_INPUT_FILE_PATH"` (often chained with `eslint --fix`) | 0 if silent; small if linter emits errors | "PostToolUse hooks modify files but changes are overwritten / don't persist" — open Anthropic issue #10011 reports Write tool's buffer flush undoes hook edits | [claudefa.st](https://claudefa.st/blog/tools/hooks/hooks-guide), [github.com/anthropics/claude-code #10011](https://github.com/anthropics/claude-code/issues/10011) |
| W2 | Auto-lint per-language (`.py`, `.sh`, `.sql`, `.R`, `.json`) | PostToolUse(Edit\|Write) | `post-edit-lint.sh` dispatches by file extension | small | Per-file checks only — author explicitly warns against whole-project lint in hot path | [github.com/datasci-iopsy/.dotfiles](https://github.com/datasci-iopsy/.dotfiles), [dev.to/yurukusa](https://dev.to/yurukusa/5-claude-code-hook-mistakes-that-silently-break-your-safety-net-58l3) |
| W3 | Auto-stage edits to git | PostToolUse(Edit\|Write) | `git add "$FILE_PATH"` after every edit | 0 | Author claims clean commits "without Claude needing to remember" | [karanbansal.in](https://karanbansal.in/blog/claude-code-hooks/) |
| W4 | Quality gate on Stop — fail if tests fail / types broken | Stop | runs `bun run typecheck:fast` (tsgo) or vitest; exit 2 with `tail -50` of failures; checks `stop_hook_active` first | ~500–2,000 tokens of test output | "Stop hook infinite loops — always check `stop_hook_active` and exit 0 when true. Every developer learns this once." Use `--reporter=basic` to avoid ANSI noise | [thomas-wiegold.com](https://thomas-wiegold.com/blog/claude-code-hooks/), [morphllm.com](https://www.morphllm.com/claude-code-hooks) |
| W5 | TDD enforcement via prompt-handler hook (delegates judgement to fast model) | PreToolUse | prompt-hook calls Haiku to decide if tests-first rule was followed | model-decision overhead (cents) | More flexible than regex; expensive per fire | [ksred.com](https://www.ksred.com/claude-code-hooks-a-complete-guide-to-automating-your-ai-coding-workflow/) |
| W6 | Desktop / sound notifications on Stop/Notification | Stop, Notification | `osascript -e 'display notification …'` (macOS), `notify-send` (Linux), `afplay` | 0 | "stops checking back every thirty seconds" — high-value, near-zero cost | [pixelmojo.io](https://www.pixelmojo.io/blogs/claude-code-hooks-production-quality-ci-cd-patterns), [dev.to/avinash431](https://dev.to/avinash431/building-a-complete-developer-terminal-setup-for-claude-code-part-6-dotfiles-and-wrap-up-54c0) |
| W7 | Slack alert on permission prompt / idle | Notification(permission_prompt\|idle_prompt) | curls Slack webhook | 0 | Avoids losing autonomous run while AFK | [github.com/karanb192/claude-code-hooks](https://github.com/karanb192/claude-code-hooks) |
| W8 | Auto-approve safe read-only commands | PreToolUse(Bash) | grep against `^(ls\|cat\|head\|tail\|wc\|grep\|rg\|git\\s+(status\|log\|diff\|show)\|pwd\|which)` then return `permissionDecision: "allow"` | small | Reduces interactive prompts during exploration | [heyuan110.com](https://www.heyuan110.com/posts/ai/2026-02-28-claude-code-hooks-guide/) |
| W9 | Package-manager enforcer based on lockfile | PreToolUse(Bash) | detect `pnpm-lock.yaml` vs `yarn.lock` vs `package-lock.json` and block wrong PM | ~30 tokens | Protects against lockfile churn | [lobehub.com/skills/claude-code-bash-patterns](https://lobehub.com/bg/skills/jackspace-claudeskillz-claude-code-bash-patterns) |
| W10 | No-ask-human autonomy enforcer | UserPromptSubmit / Stop | detects "Should I…" patterns in output; reminds Claude to decide and continue | ~30 tokens | "Essential for overnight runs" — author runs Claude 24/7 on WSL2 | [dev.to/yurukusa](https://dev.to/yurukusa/10-claude-code-hooks-i-collected-from-108-hours-of-autonomous-operation-now-open-source-5633) |
| W11 | `prefer-jq.sh` — nudge toward jq over manual JSON parsing | PreToolUse(Bash) | detects manual JSON sed/awk patterns and suggests jq | small | Style hook only | [github.com/datasci-iopsy/.dotfiles](https://github.com/datasci-iopsy/.dotfiles) |

### Cost / quota management

| # | Purpose | Event | Command shape | Context budget | Pitfalls reported | Source |
|---|---|---|---|---|---|---|
| Q1 | ccusage statusline — daily/session cost + context % in status bar | statusLine (not strictly a hook event, but the same mechanism) | `bun x ccusage statusline` | 0 (status bar only) | Anthropic issue #52089 confirms hooks themselves cannot see token counts yet — ccusage reads JSONL files on disk | [ccusage.com](https://ccusage.com/guide/), [anthropics/claude-code #52089](https://github.com/anthropics/claude-code/issues/52089) |
| Q2 | Custom statusline showing worktree + branch + cost + rate-limit bar | statusLine | bash script reads `cost.total_cost_usd`, `context_window.used_percentage`, `rate_limits.five_hour` from stdin JSON | 0 | "No daemon, no background process — Claude Code calls the script on each update" | [dandoescode.com](https://www.dandoescode.com/blog/claude-code-custom-statusline), [gordonbeeming.com](https://gordonbeeming.com/blog/2026-03-22/building-a-custom-claude-code-status-line) |
| Q3 | Cost-guard — rate-limit / throttle expensive tools | PreToolUse(Agent\|WebFetch) | `cost-guard.sh` blocks or warns if budget exceeded | ~30 tokens | Implementation specifics not standardized; mostly bespoke per-user | [github.com/datasci-iopsy/.dotfiles](https://github.com/datasci-iopsy/.dotfiles) |
| Q4 | Threshold-based backup at context percentage | statusLine / Stop | StatusLine is "the only mechanism that receives live context metrics"; trigger transcript backup at 70%+ usage | varies | Hooks proper still lack live token counts — request pending in #52089 | [claudefa.st](https://claudefa.st/blog/tools/hooks/hooks-guide), [anthropics/claude-code #52089](https://github.com/anthropics/claude-code/issues/52089) |
| Q5 | Pre-compact transcript backup | PreCompact | dump session transcript to disk before Claude Code summarizes | 0 | Useful as fallback when compaction drops important context | [claudefa.st](https://claudefa.st/blog/tools/hooks/hooks-guide), [thomas-wiegold.com](https://thomas-wiegold.com/blog/claude-code-hooks/) |

---

## 2. Top 3 most-cited pitfalls

### Pitfall #1 — Exit code 1 vs. exit code 2 (the "leaky guardrail")

Cited in: [dev.to/yurukusa "5 Claude Code Hook Mistakes"](https://dev.to/yurukusa/5-claude-code-hook-mistakes-that-silently-break-your-safety-net-58l3), [techsy.io](https://techsy.io/en/blog/claude-code-hooks-guide), [claudefa.st](https://claudefa.st/blog/tools/hooks/hooks-guide), [code.claude.com hooks ref](https://code.claude.com/docs/en/hooks).

Exit code `1` means "hook errored" — Claude Code logs the error and continues anyway. Only exit `2` actually blocks the tool call. The yurukusa author lost three hours of autonomous operation before noticing force-pushes weren't being blocked. The official docs confirm this is "the most common mistake," and every blog tutorial leads with it. Symptoms are dangerous because they're silent: the hook fires, prints "blocked!", and Claude proceeds anyway.

### Pitfall #2 — Stop-hook infinite loops

Cited in: [thomas-wiegold.com](https://thomas-wiegold.com/blog/claude-code-hooks/), [linkedin.com/felipefreitag](https://www.linkedin.com/posts/felipefreitag_til-that-passing-a-prompt-to-a-claude-code-activity-7419908295697707008-E0k_), [techsy.io](https://techsy.io/en/blog/claude-code-hooks-guide), [news.ycombinator.com #47895029](https://news.ycombinator.com/item?id=47895029), [github.com/disler/claude-code-hooks-mastery](https://github.com/disler/claude-code-hooks-mastery).

A Stop hook that exits 2 forces Claude to keep working. If the gate condition is still false on the next stop attempt, the hook fires again — and so on. Wiegold: "Every developer who tries Stop hooks has done this once. I've done it twice." Freitag (LinkedIn): "passing a prompt to a Claude Code stop hook creates an infinite loop." Fix: check the `stop_hook_active` flag at the top of the script and `exit 0` when it's true. Disler's `claude-code-hooks-mastery` README labels Notification hooks similarly: "Can cause infinite loops if not properly controlled."

There's also a related but distinct complaint on HN (#47895029) that Claude 4.7 has been ignoring Stop hooks entirely — community speculates it's a deterministic-source-code issue rather than model behavior, but no resolution yet.

### Pitfall #3 — Hooks fire too often / synchronous overhead

Cited in: [dev.to/yurukusa](https://dev.to/yurukusa/5-claude-code-hook-mistakes-that-silently-break-your-safety-net-58l3), [techsy.io](https://techsy.io/en/blog/claude-code-hooks-guide), [thomas-wiegold.com](https://thomas-wiegold.com/blog/claude-code-hooks/), [github.com/anthropics/claude-code #21836](https://github.com/anthropics/claude-code/issues/21836).

PreToolUse and PostToolUse run synchronously on every matching tool call. A 3-second hook with 50 edits in a session is 2.5 minutes of pure overhead. Mitigations cited across sources:

- Use `async: true` for PostToolUse logging hooks ([thomas-wiegold.com](https://thomas-wiegold.com/blog/claude-code-hooks/)).
- Keep PreToolUse hooks under 500ms; check only the changed file, not the whole project ([dev.to/yurukusa](https://dev.to/yurukusa/5-claude-code-hook-mistakes-that-silently-break-your-safety-net-58l3)).
- Cache invariants (e.g. "is this a protected branch?") in a temp file ([techsy.io](https://techsy.io/en/blog/claude-code-hooks-guide)).
- Keep SessionStart hooks under 1s each; claude-mem targets <100ms with p99 = 250ms ([docs.claude-mem.ai](https://docs.claude-mem.ai/hooks-architecture)).
- Use `if` filters (permission-rule syntax like `"Bash(git )"` or `"Edit(*.ts)"`) for narrower matching than `matcher` regex ([code.claude.com hooks ref](https://code.claude.com/docs/en/hooks)).

Related failure modes from the same bucket: orphaned plugin hooks that persist after plugin removal and cannot be deleted via `/hooks` UI ([anthropics/claude-code #21836](https://github.com/anthropics/claude-code/issues/21836)), and entire hook-system regressions between releases (v2.0.31 broke all hooks one day after v2.0.30 fixed them: [anthropics/claude-code #10814](https://github.com/anthropics/claude-code/issues/10814)).

---

## 3. Additional cross-cutting observations

- **`$HOME` does not expand in hook config JSON.** Use `~` (which Claude Code does expand) or an absolute path. Silent failure mode ([dev.to/yurukusa](https://dev.to/yurukusa/5-claude-code-hook-mistakes-that-silently-break-your-safety-net-58l3)).
- **`additionalContext` is capped at 10,000 characters and is saved into the transcript.** On `--continue` / `--resume` it replays the saved string rather than re-running the hook, so timestamps and SHAs go stale ([thomas-wiegold.com](https://thomas-wiegold.com/blog/claude-code-hooks/), [code.claude.com hooks ref](https://code.claude.com/docs/en/hooks)).
- **Last-write-wins on `updatedInput`.** Multiple PreToolUse hooks rewriting the same field have non-deterministic ordering ([thomas-wiegold.com](https://thomas-wiegold.com/blog/claude-code-hooks/)).
- **Hooks defined in repo-local `.claude/settings.json` don't fire for paths brought in via `--add-dir`.** Repo-local policy is silently bypassed when Claude Code is launched from elsewhere ([anthropics/claude-code #52934](https://github.com/anthropics/claude-code/issues/52934)).
- **PostToolUse cannot undo a tool call.** Use PreToolUse for prevention, PostToolUse for reaction ([thomas-wiegold.com](https://thomas-wiegold.com/blog/claude-code-hooks/)). A known bug (#10011) reports PostToolUse file modifications are sometimes overwritten by the Write tool's buffer flush.
- **Hooks see no live token-usage data.** Statusline scripts do; hooks do not — see open feature request #52089 ([anthropics/claude-code #52089](https://github.com/anthropics/claude-code/issues/52089)). This is why cost-management patterns concentrate in the statusline layer rather than the hooks layer.
- **Phrasing matters in `additionalContext`.** Imperative system-style phrasing ("You must…") triggers Claude's prompt-injection defenses; factual phrasing ("This repo uses bun test") doesn't ([code.claude.com hooks ref](https://code.claude.com/docs/en/hooks)).
- **Security risk: hooks themselves are an attack surface.** SecurityWeek reported a hook-based MCP-hijacking technique where a malicious hook proxies OAuth tokens via `~/.claude.json` edits, surviving rotation and edits ([securityweek.com](https://www.securityweek.com/claude-code-oauth-tokens-can-be-stolen-through-stealthy-mcp-hijacking/)).

---

## 4. Source URLs (consolidated)

Anthropic docs & issues:
- https://code.claude.com/docs/en/hooks
- https://code.claude.com/docs/en/hooks-guide
- https://github.com/anthropics/claude-code/issues/10814 (hooks regression v2.0.31)
- https://github.com/anthropics/claude-code/issues/10011 (PostToolUse edits overwritten)
- https://github.com/anthropics/claude-code/issues/23875 (visibility of injected context)
- https://github.com/anthropics/claude-code/issues/52089 (expose token usage to hooks)
- https://github.com/anthropics/claude-code/issues/52934 (load settings from --add-dir)
- https://github.com/anthropics/claude-code/issues/21836 (orphaned plugin hooks)

GitHub repos / dotfiles:
- https://github.com/disler/claude-code-hooks-mastery
- https://github.com/karanb192/claude-code-hooks
- https://github.com/datasci-iopsy/.dotfiles
- https://github.com/tarekziade/claude-tools
- https://github.com/pattern-stack/claudecode-patterns
- https://github.com/MuhammadUsmanGM/claude-code-best-practices
- https://github.com/zircote/.claude
- https://github.com/feiskyer/claude-code-settings
- https://github.com/elizabethfuentes12/claude-code-dotfiles
- https://github.com/vsbuffalo/dotfiles/blob/main/docs/claude-code.md
- https://github.com/shakacode/claude-code-commands-skills-agents/blob/main/docs/hooks-guide.md
- https://github.com/ryoppippi/ccusage
- https://gist.github.com/alexfazio/653c5164d726987569ee8229a19f451f

Blog posts / write-ups:
- https://thomas-wiegold.com/blog/claude-code-hooks/
- https://claudefa.st/blog/tools/hooks/hooks-guide
- https://blakecrosley.com/blog/claude-code-hooks-tutorial
- https://blakecrosley.com/guides/claude-code
- https://karanbansal.in/blog/claude-code-hooks/
- https://www.ksred.com/claude-code-hooks-a-complete-guide-to-automating-your-ai-coding-workflow/
- https://www.morphllm.com/claude-code-hooks
- https://www.aihero.dev/this-hook-stops-claude-code-running-dangerous-git-commands
- https://www.pixelmojo.io/blogs/claude-code-hooks-production-quality-ci-cd-patterns
- https://joseparreogarcia.substack.com/p/claude-code-hooks-explained-the-missing
- https://www.heyuan110.com/posts/ai/2026-02-28-claude-code-hooks-guide/
- https://techsy.io/en/blog/claude-code-hooks-guide
- https://steve-adams.me/claude-code-deny-list-is-leaky.html
- https://docs.claude-mem.ai/hooks-architecture
- https://ccusage.com/guide/
- https://ccusage.com/guide/getting-started
- https://www.dandoescode.com/blog/claude-code-custom-statusline
- https://gordonbeeming.com/blog/2026-03-22/building-a-custom-claude-code-status-line
- https://www.dolthub.com/blog/2025-06-30-claude-code-gotchas/
- https://www.eesel.ai/blog/hooks-in-claude-code
- https://www.claudelog.com/faqs/claude-code-release-notes/
- https://dev.to/yurukusa/10-claude-code-hooks-i-collected-from-108-hours-of-autonomous-operation-now-open-source-5633
- https://dev.to/yurukusa/5-claude-code-hook-mistakes-that-silently-break-your-safety-net-58l3
- https://dev.to/boucle2026/what-claude-code-hooks-can-and-cannot-enforce-148o
- https://dev.to/avinash431/building-a-complete-developer-terminal-setup-for-claude-code-part-6-dotfiles-and-wrap-up-54c0

Forum / social:
- https://www.reddit.com/r/ClaudeCode/comments/1rltiv7/inside_a_116configuration_claude_code_setup/
- https://news.ycombinator.com/item?id=47895029
- https://www.linkedin.com/posts/felipefreitag_til-that-passing-a-prompt-to-a-claude-code-activity-7419908295697707008-E0k_
- https://www.linkedin.com/posts/akshay-pachaar_claude-code-hooks-clearly-explained-how-activity-7443372644386914304-eBBM
- https://www.securityweek.com/claude-code-oauth-tokens-can-be-stolen-through-stealthy-mcp-hijacking/

---

Word count: ~1,950 (excluding source list).
