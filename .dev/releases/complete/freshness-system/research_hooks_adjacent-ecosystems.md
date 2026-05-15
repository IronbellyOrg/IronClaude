# Adjacent-Ecosystem Patterns for Per-Turn / Per-Prompt Context Injection

**Scope.** What other systems inject as "always-on" state, the cadence, the budget, and the pitfalls — so we can port the lessons into Claude Code's hook design without re-deriving them. No design proposal here; just observations and synthesized lessons.

---

## 1. Other AI Coding Assistants

### Aider — repo-map + git posture, refreshed every turn
Aider builds a **PageRank-ranked repo map** of the whole git repo and sends it with every change request. Default budget is 1k tokens, configurable via `--map-tokens`; aider "adjusts the size of the repo map dynamically based on the state of the chat" ([repomap docs](https://aider.chat/docs/repomap.html)). Aider also auto-commits every AI edit, so "current state" advances by one commit per turn ([git integration](https://aider.chat/docs/git.html)). Aider deliberately does not dump the full repo: "Adding a bunch of files … will often distract or confuse the LLM" ([FAQ](https://aider.chat/docs/faq.html)). Recent git history is included via session-warmup `/run git diff HEAD~3`, not per-turn.

### Cursor — rules + workspace index, no per-turn telemetry
Cursor's per-turn assembly: active file + cursor position, `@`-mentioned items, workspace semantic index hits, applicable rules from `.cursor/rules/`, recent chat history, MCP tool descriptions ([Datalakehouse](https://datalakehousehub.com/blog/2026-03-context-management-cursor/)). Rules have an `alwaysApply: true` flag and live "at the start of the model context" ([Cursor docs](https://cursor.com/docs/rules)). Notably **no time, git branch, or env state is auto-injected per turn** unless a rule encodes it. Critique from a Cursor user: rules "may not automatically access mid-dialog" — the assembled context is sticky once set ([Kirill Markin](https://kirill-markin.com/articles/cursor-ide-rules-for-ai/)).

### Cline — explicit "System Information" block, every prompt
Cline assembles a system prompt with three pillars; the **System Information** section explicitly contains OS, current directory structure, preferred terminal, environmental details ([Cline Chapter 3](https://cline.bot/blog/system-prompt)). Plus Cline has **Focus Chain** (todo list reinjected every 6 messages) and **Auto Compact** by default ([Cline LinkedIn](https://www.linkedin.com/posts/clinebot_context-engineering-in-cline-how-do-i-activity-7363632944709554176-AtUu)). This is the strongest example of an AI coding tool injecting **environment facts per turn**.

### Continue.dev — opt-in `@providers` for state
Continue exposes built-in providers including `@Git Diff`, `@Terminal`, `@Operating System`, `@Problems` (LSP diagnostics), `@Debugger`, `@Repository Map`, `@Current File`, `@Open` ([context providers](https://docs.continue.dev/customize/deep-dives/custom-providers)). Critical design difference: **user opts in per turn via `@`**; the model isn't fed git/OS/terminal state unless requested. Continue treats per-turn injection as a UI affordance, not an automatic decoration.

### Codex CLI — AGENTS.md walked root-to-leaf, no live state
Codex CLI auto-enumerates `AGENTS.md` files and injects each as a separate user-role message labeled `# AGENTS.md instructions for <directory>`, root-to-leaf ([OpenAI cookbook](https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide)). The system prompt describes the sandbox env, but **no live git/time/host state** is decorated per turn — Codex relies on the agent calling shell tools to discover state ([Philschmid teardown](https://www.philschmid.de/openai-codex-cli)). ZenML analysis notes Codex emphasizes "strategic prompt caching optimization to achieve linear rather than quadratic performance," which **disincentivizes per-turn variable injection** because variability breaks the cache prefix ([ZenML](https://www.zenml.io/llmops-database/building-production-ready-ai-agents-openai-codex-cli-architecture-and-agent-loop-design)).

### Sourcegraph Cody — context engine, not state injection
Cody's per-request context is **retrieval-based** (BM25-ranked snippets from local + remote repos, plus open-file context) — no decoration with time, branch, or session metadata ([Sourcegraph blog](https://sourcegraph.com/blog/how-cody-understands-your-codebase)). Cody deliberately avoids agentic context-fetch loops because they "compound the latency and randomness of multiple serial inference requests, leading to poor and unreliable context quality" ([Cody GA post](https://sourcegraph.com/blog/cody-is-generally-available)).

### Windsurf — default context, Cascade Hooks for the rest
Default per-turn context: open files + retrieved snippets from the indexed local codebase ([Windsurf docs](https://docs.windsurf.com/context-awareness/overview)). Windsurf added **Cascade Hooks** (parallel to Claude Code's hooks) and `AGENTS.md` support. Best-practice critique: "Pinning too much may slow down or negatively impact model performance" — a direct warning against decoration bloat.

### OpenHands — event stream as the context
Architecturally distinct: every Action and Observation becomes an **Event** with `id`, `source ∈ {agent, user, environment}`, `timestamp`, appended to an EventLog ([OpenHands events](https://docs.openhands.dev/sdk/arch/events)). The LLM sees this log as the conversation. Synthetic framework messages (hooks) are injected with `source="environment"` but LLM `role="user"` so the agent "reads it as a user-facing instruction." Pitfall noted: don't infer event origin from LLM role — use explicit metadata. Also runs a `StuckDetector` over the event log every step to catch loops ([DEV deep-dive](https://dev.to/truongpx396/openhands-deep-dive-build-your-own-guide-1al0)).

**Cross-tool pattern.** AI coding tools split into three camps:
- **Per-turn env decoration** (Cline, partially Aider): inject OS, cwd, repo-map every turn.
- **Pull-on-demand** (Cursor, Cody, Codex): rely on retrieval + tool calls; minimize decoration to preserve KV cache.
- **Event-log native** (OpenHands): no decoration concept — the log *is* the state.

Cursor added hooks in v1.7 (6 events, command-only). Cline has file-based hooks (4 events). Aider, Continue.dev, Windsurf had no hooks at writing of [ksred's comparison](https://www.ksred.com/claude-code-hooks-a-complete-guide-to-automating-your-ai-coding-workflow/); Windsurf has since added Cascade Hooks. Claude Code's `UserPromptSubmit` + `SessionStart` model is the most expressive — additional context can be added via plain stdout or `additionalContext` JSON ([Claude Code hooks](https://code.claude.com/docs/en/hooks)).

---

## 2. Shell Prompt Customization

### What experienced users actually show
From [Starship docs](https://starship.rs/config/), [Codependent Codr's full module list](https://www.codependentcodr.com/using-starship-for-terminal-prompt-goodness.html), [Aman Mittal's setup](https://amanhimself.dev/blog/my-starship-prompt-setup/), [Chad Austin's minimal tmux/shell config](https://chadaustin.me/2024/02/tmux-config/), and Powerlevel10k's [Lean/Rainbow](https://github.com/romkatv/powerlevel10k) defaults — the **universal high-signal set** is:

| Signal | Cadence | Notes |
|---|---|---|
| Current directory (truncated) | Every prompt | Always shown; truncation is universal |
| Git branch | Every prompt (when in repo) | Universal — every guide leads with this |
| Git status (dirty/ahead/behind) | Every prompt (when dirty) | **Conditional**: hidden when clean ([starship issue #6075](https://github.com/starship/starship/issues/6075) — users complain when status shows on clean trees) |
| Last command exit code | Every prompt (when non-zero) | Shown by changing `prompt_char` color or `$status` segment |
| Command duration | Every prompt (when > threshold) | Starship default `min_time = 2000ms`; P10k default 3s |
| Language runtime version | Every prompt (when relevant file present) | Auto-detected (Python in `.py` dir, Node in `package.json` dir) |
| Kubernetes context | Every prompt (when kubeconfig set) | Powerline/p10k staple |
| AWS profile/region | Every prompt (when AWS_PROFILE set) | Same |
| Background jobs count | Every prompt (when > 0) | Conditional |
| Hostname / SSH indicator | Every prompt (when SSH) | Hidden locally |
| Time | Optional, right-aligned | Often disabled; not universally valued |
| Battery | Optional (laptops, low %) | Conditional on % threshold |

### Pitfalls reported
- **Slow modules tank prompt latency.** A user reported a custom module taking 482ms per prompt rendering ([starship #6804](https://github.com/starship/starship/issues/6804)). Starship has `command_timeout` to abort hung modules.
- **Glyph fonts missing → broken display** ([starship FAQ](https://starship.rs/faq/)).
- **Plugin sprawl.** Eric Ma's tmux-powerline experience: "the status bar exploded with information. IP addresses, weather, load averages, hostname. Way too much" ([Eric Ma](https://ericmjl.github.io/blog/2025/12/27/how-i-themed-my-tmux-with-opencode-and-claude/)).
- **Two-spaces-after-clean-branch** formatting bug ([starship #6075](https://github.com/starship/starship/issues/6075)) — proves that *conditional rendering itself introduces alignment pitfalls*.

### Signal selection lesson
**Conditionality is the universal pattern.** Nearly every signal a power user displays is suppressed when "nothing interesting." Git status hidden when clean. cmd_duration hidden when < 2s. Battery hidden when full. Background jobs hidden when zero. Language version hidden outside a relevant project. The actual prompt content is small most of the time and balloons only when state warrants attention.

---

## 3. Editor / IDE Status Injection

### VS Code statusbar conventions
Per [official UX guidelines](https://code.visualstudio.com/api/ux-guidelines/status-bar): "Primary (left) and Secondary (right). Items that relate to the entire workspace (status, problems/warnings, sync) go on the left and items that are secondary or contextual (language, spacing, feedback) go on the right." Explicit "Don'ts": custom colors, multiple icons, multiple items per concern. Error/warning colored variants are "last resort and only for special cases given their prominence."

VS Code default per-file signals: git branch + sync state, problems/warnings count, line/col, encoding, line endings, indentation, language mode, selection count ([branches doc](https://code.visualstudio.com/docs/sourcecontrol/branches-worktrees), [user interface doc](https://code.visualstudio.com/docs/getstarted/userinterface)).

**Convention takeaway:** the statusbar shows **counts and modes**, not raw data. "5 problems," not the problems themselves. "main," not the commit hash.

### JetBrains IDEs
Status bar Git Branch widget is the canonical action point — single-click branch switcher ([JetBrains blog](https://blog.jetbrains.com/idea/2012/03/simpler-and-more-powerful-ui-for-git-branches/)). The IDE's status bar conventions track VS Code's: workspace state on left, file-mode state on right. A 2025 community plugin adds dual colored git indicators ([Git Status Indicator](https://plugins.jetbrains.com/plugin/29752-git-status-indicator)) — suggesting the built-in "branch name only" wasn't enough signal for some users, who want a freshness/dirtiness cue at a glance.

### Emacs modeline (doom-modeline / spacemacs)
[Tecosaur's Doom config](https://tecosaur.github.io/emacs-config/config.html) documents an explicit decision to **conditionally hide the file encoding** when it's the expected `LF UTF-8` — "it really isn't worth noting in the modeline." This is the same conditional-rendering pattern from shell prompts: suppress the default-value case, show only deviations. Other modeline signals: buffer modified indicator (color-toned from red to orange because red felt alarmist), Git branch, major mode, line/col, project name.

### tmux status bars
Chad Austin's [minimalist tmux config](https://chadaustin.me/2024/02/tmux-config/) is instructive: "Keep the date, but I think I can remember what year it is" — he deletes the year. He also moves the session ID next to the hostname to free the prefix line. Common left-side: session/window/pane labels. Common right-side: hostname, time, battery, uptime fragment ([dev.to tweaks](https://dev.to/krishnam/tmux-13-cool-tweaks-to-make-it-personal-and-powerful-487p), [Jaime's guide](https://www.barbarianmeetscoding.com/blog/jaimes-guide-to-tmux-the-most-awesome-tool-you-didnt-know-you-needed)). Update interval is configurable (15s default, often reduced or extended); slow status commands measurably degrade tmux UX.

**Status-bar lesson:** every veteran's writeup is a story of **pruning** — they all start with a maximal plugin and trim. The end state is 4–7 signals, mostly counts/modes, with deviation-only rendering.

---

## 4. CI/CD and Observability Dashboards

### Golden Signals (Google SRE)
The canonical "always-on" status set for a service: **Latency, Traffic, Errors, Saturation** ([Grafana golden-signals dashboard](https://grafana.com/grafana/dashboards/21073-monitoring-golden-signals/), [OneUptime walkthrough](https://oneuptime.com/blog/post/2026-02-06-service-health-dashboard-opentelemetry-golden-signals/view)). RED is a sibling framing (Rate, Errors, Duration); USE is for resources (Utilization, Saturation, Errors). Latency uses **percentiles, not averages** — "averages lie. If 1% of users experience 5-second delays, the average may still look fine" ([Al-Fatah Medium](https://al-fatah.medium.com/grafana-the-4-golden-signals-sre-monitoring-slis-slos-error-budgets-explained-cd9de63261e9)).

### Dashboard best practices that port
From [Gart Solutions on SRE monitoring](https://gartsolutions.com/sre-monitoring/) and [AndiDog on Grafana dashboards](https://andidog.de/blog/2022-04-21-grafana-dashboards-best-practices-dashboards-as-code):
- **Link metrics to logs and traces** — every panel should be one-click from spike to underlying trace.
- **Role-appropriate views** — SRE needs raw signal, leadership needs SLO health, devs need per-service detail. Same data, different rendering.
- **Treat dashboards as living documents** — "prune panels that nobody uses, reassess thresholds quarterly, add deployment or incident annotations."
- "A good dashboard is not cluttered. It tells a story" ([Al-Fatah](https://al-fatah.medium.com/grafana-the-4-golden-signals-sre-monitoring-slis-slos-error-budgets-explained-cd9de63261e9)).

### GitHub Actions status badges, kubectl top
Per-commit badges ([GitHub docs](https://docs.github.com/actions/managing-workflow-runs/adding-a-workflow-status-badge), [Shields.io](https://shields.io/badges/git-hub-actions-workflow-status)) compress an entire workflow's state into **one of three values** (pass/fail/in-progress). `kubectl top` shows CPU + memory per pod — two numbers per row, deltas implied from re-running. Both are **extreme compression**: a single glyph or pair of numbers stands for a deep underlying state.

### Pitfall reported
"Dashboard sprawl without governance." Same observation as the tmux plugin user: maximal-decoration drifts toward noise. Pruning is continuous.

---

## Cross-Ecosystem Lessons That Port to LLM Per-Turn Injection

1. **Conditional rendering is universal.** Shell prompts hide clean git status, zero job count, default file encoding, full battery, sub-2s command duration. Emacs hides `LF UTF-8`. VS Code shows error counts only when non-zero. The corollary for hooks: **don't inject "no changes since last turn" or "branch unchanged" — silence is the signal**. Bytes spent telling the model nothing changed are bytes that train the model to ignore the injection block.

2. **Counts and modes, not raw payloads.** Statusbars say "5 problems," not the problems. Aider sends a 1k-token repo *map*, not the repo. Golden signals show p95 latency, not the request log. Per-turn injection should compress: "3 uncommitted files, 2 staged, branch=feature/x at HEAD+4," not the diff.

3. **Pull-on-demand beats push-by-default for variable data.** Cursor, Cody, Codex all minimize per-turn decoration to preserve **prompt cache hits** (Codex specifically calls this out as a perf win — variability breaks linear scaling). The lesson is sharper for Anthropic users: cache-friendly hooks should inject *stable* facts (project name, conventions, today's date once per session) and avoid per-turn churn unless the signal is high-value. Cline's per-message env block is the counter-example, and it works because Cline's audience accepts the cache cost.

4. **Freshness signals are universally valuable.** VS Code shows "changes since last save," statusbars show "ahead/behind origin," doom-modeline shows modified-buffer color. Aider commits after every edit so the model always has a clean baseline. The recurring per-turn fact worth injecting is **"what changed since the model last saw this."** Not the full state — just the delta and a timestamp.

5. **Power users prune; defaults are over-decorated.** Every shell-prompt blog post, every tmux config writeup, every Grafana dashboard guide tells the same story: started maximal, trimmed to 4–7 signals. The pitfall is not under-decoration — it's the slow accumulation of stale or low-signal segments that nobody removed. Hook configs should be **opinionatedly minimal at install** and require explicit opt-in to add signals.

6. **Latency/cost is a hard ceiling, not a soft preference.** A 482ms shell module is an upstream bug report ([starship #6804](https://github.com/starship/starship/issues/6804)). Cody rejects agentic context-fetch because of compounded latency. Starship has `command_timeout`. Per-turn hooks need a budget cap (tokens + wall-clock) and a fail-quiet contract — a slow hook should degrade silently, never block.

7. **Separate workspace-global from contextual signals.** VS Code's left/right statusbar split is intentional: workspace-wide (sync state, problem count) vs. file-local (encoding, language). Per-turn injection benefits from the same split — session-stable facts (project name, today's date, OS) belong in `SessionStart`; per-turn deltas (git status, recent file changes) belong in `UserPromptSubmit`. Mixing them defeats prompt caching.

8. **Decoration must be distinguishable from user text.** OpenHands explicitly tags synthetic messages with `source="environment"` while presenting them as `role="user"`; the framework warns: "Do not infer event origin from LLM role." Cursor wraps rules and Codex wraps `AGENTS.md` files in headered blocks (`# AGENTS.md instructions for <dir>`). The lesson: hook output should be **boxed and labeled** so the model can tell injected context from human prompts — and so prompt-injection attacks on injected content are at least visible.

9. **Stuck-loop / drift detection beats more decoration.** OpenHands runs a `StuckDetector` over the event log every step — five patterns flagged. Cline auto-injects the focus chain every 6 messages to prevent drift. This is structurally different from "tell the model more things"; it's "watch the trajectory and intervene." When choosing between adding a new signal vs. adding a drift check, the drift check often wins per token spent.

10. **Default-value suppression has alignment pitfalls.** Starship issue #6075 documents the real cost of conditional rendering: the layout shifts when the suppressed module reappears. For LLM injection, the analog is: a hook that *sometimes* injects a block can confuse the model when the block disappears ("Did the user remove this rule? Should I forget it?"). A stable scaffold with conditional *contents* (e.g., `[git] clean` vs. `[git] 3 modified`) is safer than a sometimes-present block.

---

**Sources cited inline.** All claims tied to a specific source URL; tools listed (Aider, Cursor, Cline, Continue, Codex, Cody, Windsurf, OpenHands, starship, p10k, tmux, doom-modeline, VS Code, JetBrains, Grafana, GitHub Actions) each have at least one primary or near-primary reference.
