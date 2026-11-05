# Next-step chains

Loaded in claim Wave 5.

Spawn workers with `subagent_type: issue-worker-t<N>` and never pass the `model` parameter. (No worker is spawned in Wave 5; the rule is repeated here so every ref carries it. Workers are `~/.claude/agents/issue-worker-t3.md`, `~/.claude/agents/issue-worker-t2.md` and `~/.claude/agents/issue-worker-t1.md`, project `.claude/agents/` copy first; they run `/sc:analyze` by following `~/.claude/commands/sc/analyze.md`.)

These are the default rows passed to `/sc:recommend` as the suggested route. `/sc:recommend` makes the final pick (B4). `<S>` = `.dev/issues/<N>/summary.md`; `<symptom>` is the bug's one-line symptom from the summary (at least 10 words); `<scope>` is the main path from the summary. `/sc:issue` never runs these commands (B2); it writes them into `next-steps.md` from `templates/next-steps.md`.

| Type / complexity | Tier line | Chain |
|---|---|---|
| Feature, simple | `/model claude-gw-tier2` | 1. `/sc:brainstorm "<topic> @<S>" --depth quick --models opus,sonnet` (no `--handoff`)<br>2. `/sc:workflow <brainstorm dir>/merged-requirements.md --depth quick --handoff none`<br>3. `/sc:implement <plan path printed by step 2>` |
| Feature, medium | `/model claude-gw-tier1a` | 1. `/sc:brainstorm "<topic> @<S>" --blind --models opus,sonnet`<br>2. `/sc:design <brainstorm dir>/merged-requirements.md --type <architecture\|api\|component\|database> --format spec`<br>3. `/sc:workflow <design doc> --depth standard --handoff none`<br>4. `/sc:implement <plan path>` |
| Feature, complex | `/model claude-gw-tier1a` | 1. `/sc:brainstorm "<topic> @<S>" --depth deep --research deep --codebase --blind --models opus,sonnet`<br>2. `/sc:design <merged-requirements.md> --type <...> --format spec`<br>3. `/sc:workflow <design doc> --depth deep --handoff none`<br>4. `/sc:implement <plan path>` |
| Bug, simple | `/model claude-gw-tier2` | 1. `/sc:troubleshoot "<symptom>" --depth quick --context <S> --scope <scope>`<br>2. `/sc:implement <REPORT.md path printed by step 1>` |
| Bug, medium | `/model claude-gw-tier1a` | 1. `/sc:troubleshoot "<symptom>" --fix --context <S> --scope <scope>` (plan route: after the report it offers to build the `/sc:workflow` package; the user accepts, and it then prints the `/sc:implement` command)<br>2. `/sc:implement <plan path printed by step 1>` |
| Bug, complex | `/model claude-gw-tier1a` | 1. `/sc:troubleshoot "<symptom>" --depth deep --fix --context <S> --scope <scope>` (MDTM route: after the report it offers to build the task file with `task-builder`; the user accepts, and it then prints the `/task` command)<br>2. `/task <task file path printed by step 1>` |

Notes:
- `--depth quick` with `--fix` is a STOP in `/sc:troubleshoot`, so the simple bug row has no `--fix` and hands the report to `/sc:implement` (issue body: "Hand the output directly off ... /sc:implement").
- `/sc:troubleshoot --depth deep` STOPs on a description under 10 words without `--scope`; the rows always pass `--scope`.
- `/sc:brainstorm --models` defaults to `opus,sonnet,haiku`, rotated across proposals, and takes aliases only. Every brainstorm row passes `--models opus,sonnet` so no proposal runs on the `haiku` alias, which on this workspace resolves to `glm-5.3` (`refs/tiers.md`), below T2 (B14). Aliases cannot name a picker ID, so this is the closest the chain can get to B14 inside a brainstorm; the session tier itself is pinned by the `/model` line (default D25).
- `/sc:design --type` is chosen per issue by `/sc:recommend` from the four values the command accepts.

No brainstorm step carries a handoff flag: the tasklist handoff feeds `/sc:tasklist`, not `/sc:workflow`, and the design handoff only prints a suggestion (B11), so `/sc:workflow` and `/sc:design` run as their own steps.

## Goal sent to `/sc:recommend` (claim Wave 5 step 1)

Invoke `Skill sc-recommend` with this goal, filled from `summary.md`:

```text
Pick the next-step chain for GitHub issue <issue url>.
Type: <feature|bug>. Complexity: <simple|medium|complex>.
Summary: .dev/issues/<N>/summary.md
Suggested route (default row "<Type>, <complexity>" of the /sc:issue chains):
<tier line>
<the numbered chain of that row, one step per line>
```

Save the skill's output verbatim to `.dev/issues/<N>/recommend.md` from `templates/recommend-record.md`. When `/sc:recommend` asks a question or finds no route, record that in `recommend.md` and write `next-steps.md` from the default row, saying so. When it chooses a different route, `next-steps.md` follows `/sc:recommend` and names the unused default row in one line (default D23).
