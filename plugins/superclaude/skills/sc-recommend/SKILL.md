---
name: sc-recommend
description: "Build a refined, paste-ready prompt that hands the user's request off to the right local skill, command, agent, or native-tool sequence — only when delegation adds net value. Use this skill whenever the user asks 'which command should I use', 'how do I best prompt for X', 'help me invoke the right skill for Y', 'recommend a workflow for Z', or describes a task without naming a command. Also use proactively whenever the user pastes a goal that could plausibly map onto multiple skills/agents/commands in this repo and you would otherwise have to choose blindly. With --plugin, switches to ecosystem search (Claude plugin marketplaces + community skill repos) instead of the local project surface."
allowed-tools: Read, Glob, Grep, Bash, mcp__auggie__augment_code_search, mcp__tavily__tavily_search, mcp__tavily__tavily_extract, WebFetch, WebSearch, Edit, Write, Agent, Task
argument-hint: "[goal description] [--plugin] [--minstar <N>] [--eval none|quick|normal|deep]"
category: utility
---

# /sc:recommend — Refined-Prompt Builder

## Triggers

`sc-recommend` is invoked by the `/sc:recommend` command via its `## Activation` section, and Claude may also load it on its own when the user asks which command or skill to use or describes a task without naming a command (see the description above).

Activation conditions:

- User runs `/sc:recommend <goal>` in Claude Code
- `--plugin` flag may be passed to switch to ecosystem-search mode

## Purpose

Generate the **single best refined, paste-ready prompt** (occasionally a small set of clearly-distinguished prompts) that delegates the user's goal to whichever existing local skill / command / agent / native-tool sequence will execute it with the lowest waste and highest fidelity. Surface the project's *actual* current capability surface — not a stale mapping. Default to the smallest delegation that wins; recommend native tooling when delegation does not earn its overhead.

This skill **builds prompts**, it does not execute them. Output is a fenced prompt block the user can copy verbatim.

## Output

Every successful invocation emits one of:

1. **Refined-prompt block** — a fenced `text` block containing the paste-ready prompt to invoke a target skill/command/agent. Includes explicit parameters, deliverable shape, and file/agent handoffs. Single-line bash commands only (no heredocs, no `\` continuations); the prompt body itself may be multi-line because it is an argument string.
2. **Native-tooling recommendation** — when delegation adds no net value, a short paragraph naming the native tools (`Read`, `Grep`, `Glob`, `Edit`, `Write`, `Bash`) and the order to run them in. No skill is invoked.
3. **Plugin-search result** (`--plugin` only) — one or more plugin/skill candidates with capability summary, install command, repo URL, and citations.
4. **Ordered workflow** — when Step 0 matched a routing row in the guide: a numbered list of steps in the guide's order, each with the command or skill to run and every flag the guide makes mandatory for that step, plus the level, whether it changes files, and the guide section to read (Phase 2, ordered-workflow template).

If multiple distinct paths are reasonable (e.g., "either `/sc:workflow` + `/sc:implement` (level 3) or `/task-builder` + `/task` (level 4) fits"), emit each as its own clearly-labeled prompt block with a one-line disambiguator — never as a flat "alternatives" list.

The skill never restates the target's internal logic (see Rule R3).

## Step 0 — Read the routing guide (before anything else)

Local mode only; skip this step when `--plugin` is set. Read the IronClaude routing guide before the cache lookup and before Phase 0. Try these locations in order and stop at the first one that exists. Inside an IronClaude checkout (`src/superclaude/commands/` exists under `git rev-parse --show-toplevel`), try location 4 first and then the others in order: inside a checkout, trust `src/` (the same rule as Phase 0 Step A), because the installed copy may be older.

1. `~/.claude/HOW-WE-WORK.md` (installed by `superclaude install`). Resolve `~` first (`echo "$HOME"` in Bash) and Read the absolute path. Never put `~` in a Glob pattern.
2. `${CLAUDE_SKILL_DIR}/refs/HOW-WE-WORK.md` (Claude Code plugin installs). If this text still shows the literal `${CLAUDE_SKILL_DIR}`, skip this location.
3. `${CLAUDE_PLUGIN_ROOT}/skills/sc-recommend/refs/HOW-WE-WORK.md` (Claude Code plugin installs, for when `${CLAUDE_SKILL_DIR}` is not expanded). If this text still shows the literal `${CLAUDE_PLUGIN_ROOT}`, or the variable is empty, skip this location.
4. `src/superclaude/core/HOW-WE-WORK.md` under the repository root (`git rev-parse --show-toplevel`; only inside an IronClaude checkout).
5. Not found: print exactly this one line, then skip the Hot-Path Cache Lookup and run Phase 0 (live enumeration only), with `guide_status: absent`:
   `Routing guide not found. pipx/pip install: run superclaude update. Plugin install: update the SuperClaude plugin. Until then, recommendations do not use the routing guide.`

When the guide is found, add its path to `verified_sources` and extract three blocks by their markers, never by line number or heading text:

- **Level table:** the text between `<!-- level-table:v1 -->` and `<!-- /level-table -->` (the six levels and the hard limit).
- **Routing table:** the text between `<!-- routing-table:v1 -->` and `<!-- /routing-table -->`. Columns: `id | intent | level | steps | mandatory_flags | changes_files | section | notes`. `steps` holds ordered steps separated by `<br>`, each starting with its label (`1.`, `2.`, `3a.`). `mandatory_flags` holds `-` or `;`-separated `<step label>: <flags>` entries.
- **Other commands:** the text between `<!-- other-commands:v1 -->` and `<!-- /other-commands -->` (installed commands no workflow routes to, with when to use each). Use it only when no routing row matches (`no_match`): a command it names whose "when to use it" text fits the goal becomes a candidate for Phase 0 Step C. On a cache miss, pass this block to the cold-path subagent (Cold-Path Write-Back, step 1), which runs Phase 0 for you.

**Parse rule:** after the header and separator lines, each routing-table row must split on unescaped `|` into exactly 8 cells. A row that does not is skipped and named in `degradation_notes` (`routing row <n> skipped: <k> cells`). A block is absent only if either of its markers is missing or, for the routing table, no row parses; say so in `degradation_notes`.

**Match the goal to one routing row.** A row matches when the goal states the situation in at least one of its `intent` phrases (separated by `;`; same meaning, not necessarily the same words). If no phrase of any row fits, the result is `no_match`. If two or more rows match: prefer the row whose matching phrase is more specific (it names the artifact, for example "stack trace" or "PRD"). If they are still tied and all tied rows have numeric levels, take the row with the higher `level` (the guide's rule: when unsure between two rows, choose the heavier one). If any tied row has level `-`, ask exactly this and stop: `Is this mainly <intent of row A> or <intent of row B>?`. If the goal is too vague to compare with any intent phrase, ask one clarifying question (Graceful degradation, last row).

- **A row matches:** set `guide_status: matched` and record the row `id`. Skip the Hot-Path Cache Lookup and the Cold-Path Write-Back: a cache row holds one hand-off target and cannot carry an ordered workflow. In matched mode, skip Phase 0 Step B. In Step C, verify each step's command or skill from the matched row directly (Read the Step A path for that name), whether or not auggie would rank it. Then build the answer with the ordered-workflow template in Phase 2. Before using a matched row at level 1 or 2 (for example `small-change`), apply the guide's hard limit: a row's intent phrases describe one situation, and if the goal needs more than five edits or touches more than one source file (its test file does not count), use the `simple-plan` (level 3) or `task-file` (level 4) row instead.
- **No row matches:** set `guide_status: no_match` and continue with the Hot-Path Cache Lookup as written. The level table and the hard limit still apply in Phase 1.

## Hot-Path Cache Lookup (try the amortized cache before the cold path)

Before running the full Phase 0–3 **cold path** below, attempt the **hot path** — the lazily-populated YAML lookup cache that drops a repeat delegation request from ~91K to ~5–10K tokens. The cold path (Phase 0–3) only runs on a cache miss. Skip this whole section when Step 0 matched a routing row.

**Availability gate (run once, before step 1).** The hot path runs only inside an IronClaude checkout. Every install has the `superclaude recommend` CLI, but its cache fingerprint is computed over the checkout's `src/superclaude/` (plus the installed `~/.claude/` and project `.claude/` command, skill and agent folders) and the cache lives in that project's `.claude/cache/`, so outside a checkout there is nothing valid to fingerprint or cache, and the skill skips the hot path. Use the hot path only if both checks pass: `test -f src/superclaude/cli/recommend/prompts.py`, then `uv run superclaude recommend --help` exits 0. Run both checks from the repository root (`git rev-parse --show-toplevel`; if that fails, the gate fails). Run the gate once per invocation, before the first `uv run superclaude recommend` call of any kind (hot path, write-back, or the `--plugin --eval` decision gate), and reuse its result. Do not run `uv run` in any other project: in a user's own uv project it would create or sync that project's environment. If either check fails, or any `uv run superclaude recommend ...` call in this skill exits non-zero, skip the rest of the hot path, run Phase 0–2 yourself in this context, skip the Cold-Path Write-Back, `--eval`, and telemetry, and add `recommend CLI unavailable; cache skipped` to `degradation_notes`.

Under the resolved **Option P** layering, the `cli/recommend/` Python module owns the deterministic dispatch (scan / source_hash validation / budget gate); this skill owns only the Agent spawns (the `anthropic` SDK is banned, so the CLI cannot spawn Agents).

1. **Classify (ONE Haiku subagent).** Spawn exactly **one** `model: haiku` subagent via the Agent tool. Read `src/superclaude/cli/recommend/prompts.py` under the repository root (`git rev-parse --show-toplevel`) and use the text of the string assigned to `CLASSIFIER_PROMPT` (without the quote marks) as the subagent prompt. Pass the verbatim user request. It returns `{classification_key, native_likely, confidence_top2_delta}` — nothing else. Do not classify in the parent.

2. **Deterministic dispatch (shell to the CLI).** The CLI owns the scan/validate/budget under Option P:

   `uv run superclaude recommend dispatch --key <classification_key> --delta <confidence_top2_delta> [--native-likely]`

   Add `--native-likely` only when the classifier returned `native_likely: true`. The skill does not pass `--budget-used`, so the CLI budget gate does not trigger from this skill: you cannot count your own tokens, and `dispatch` does not print a running total to pass back.

   If this call exits non-zero, treat it as an unavailable CLI (Availability gate above): no hot path, no write-back.

   It prints a JSON `DispatchResult`. The source_hash validation is the CLI's deterministic Read + sha256 compare — **never** trust a Haiku-computed hash.

3. **Interpret the outcome (the 5 fall-throughs):**
   - `outcome: "hit"` → emit `recommendation` **verbatim** (it is the row's filled `prompt_envelope_template` plus any `best_model_hint`). Then append exactly one telemetry event: `uv run superclaude recommend telemetry append --mode delegate --cache-result hit --classification-key <key> --duration-ms <ms>` (if it fails, ignore the failure; the recommendation is already emitted). **DONE — do not run the cold path.**
   - `outcome: "native"` (classifier `native_likely`, or a `native_fallback` row) → recommend native tooling per Phase 1, but run Phase 1's hard-limit check first: if the work needs more than 5 edits or touches more than one source file, recommend the written plan Phase 1 names instead of a native answer; **no cold path, no table write, and no telemetry event** (native is not a cache-table event — it has no `cache_result` enum member, so the appender has nothing valid to log).
   - `outcome: "miss"` with `cache_result` ∈ {`miss_no_key`, `miss_low_confidence`, `miss_validation_stale`} → **fall through to the cold path** (Phase 0–3). Carry the miss reason into the cold-path write-back.

The skill spawns exactly **one** Haiku subagent here (the classifier); the cold-path Haiku subagent is spawned only on a miss (see the Cold-Path Write-Back section after Phase 3). The emitted hot-hit recommendation reuses the row's hand-off envelope unchanged — it restates no target protocol (R3). The hot and cold paths emit the **same Return Contract** shape for caller parity.

## Phase 0 — Mandatory Surface Enumeration + Auggie Sweep (GATE)

**Hard gate. Do not advance to Phase 1 until BOTH steps have landed or the documented degradation notice has been emitted, except in matched mode (Step 0 matched a routing row), where Step B is skipped and Step A and Step C still run.**

The old skill failed because its discovery layer was a hand-curated 10-row keyword table that went stale (it failed to surface `/sc:spec-panel` even though that command file was sitting in `src/superclaude/commands/`). The fix is to enumerate the actual surface every invocation and let auggie semantically rank it. There is no static mapping in this skill.

### Step A — Live surface enumeration (Glob)

Enumerate the project's *actual* current surface. Read every result lazily — Glob first, Read only what the candidate set later requires.

Search these locations. List the `$HOME` locations with one Bash call that uses `find`, not shell globs (zsh aborts the whole command on an unmatched glob, and `2>/dev/null` cannot stop that): `find -L "$HOME/.claude/commands/sc" "$HOME/.claude/agents" -maxdepth 1 -name '*.md' 2>/dev/null; find -L "$HOME/.claude/skills" -mindepth 2 -maxdepth 2 -name SKILL.md 2>/dev/null; find -L "$HOME/.claude/templates" -name '*.md' 2>/dev/null`. Or resolve `$HOME` once and give Glob the absolute folder as `path`. Never put `~` in a Glob pattern. Run the project and checkout globs in parallel. Record the path where each name was found; Step C reads that path.

| # | Surface | Location | When |
|---|---|---|---|
| 1 | Installed commands | `$HOME/.claude/commands/sc/*.md` | always |
| 2 | Installed skills | `$HOME/.claude/skills/*/SKILL.md` | always |
| 3 | Installed agents | `$HOME/.claude/agents/*.md` | always |
| 4 | Installed templates | `$HOME/.claude/templates/**/*.md` | always |
| 5 | Project commands, skills, agents | `.claude/commands/**/*.md`, `.claude/skills/*/SKILL.md`, `.claude/agents/*.md` (cwd) | always |
| 6 | Plugin install | `${CLAUDE_PLUGIN_ROOT}/commands/*.md`, `${CLAUDE_PLUGIN_ROOT}/skills/*/SKILL.md`, `${CLAUDE_PLUGIN_ROOT}/agents/*.md` | only when the variable is expanded (plugin skill) |
| 7 | IronClaude source checkout | `src/superclaude/commands/*.md`, `src/superclaude/skills/*/SKILL.md`, `src/superclaude/agents/*.md`, `src/superclaude/templates/**/*.md`, `src/superclaude/examples/*-template.md` (repository root) | only inside an IronClaude checkout (`src/superclaude/commands/` exists under `git rev-parse --show-toplevel`) |

If the same name is found in several places: inside an IronClaude checkout trust `src/` (`.claude/` there is the `make sync-dev` mirror); otherwise prefer the project `.claude/` copy, then `$HOME/.claude/`, then the plugin. Note duplicates in `degradation_notes`.

Commands are thin dispatchers that delegate to skills via `## Activation`. Treat the installed `$HOME/.claude/commands/sc/*.md` (or `src/superclaude/commands/*.md` inside an IronClaude checkout) as the fast-path discovery surface for `/sc:*` slash commands.

The checkout paths (row 7) resolve under the repository root (`git rev-parse --show-toplevel`); the project paths (row 5) are read from cwd. If the user's cwd is a worktree under `.dev/worktrees/<name>/`, that command returns the worktree's root, so both resolve against **that worktree**. The skill must remain worktree-aware.

See `refs/surface-enumeration.md` for the full algorithm, the verification record schema, and worked examples.

### Step B — MANDATORY auggie semantic ranking

Skip this step in matched mode (Step 0 matched a routing row) and set `auggie_status: skipped`. Otherwise, after enumeration, issue **one** `mcp__auggie__augment_code_search` query to semantically rank the enumerated surface against the user's request. Auggie is the speed lever: one semantic query ranks the whole surface; do not iterate file-by-file.

Query shape:

> Given the user request "<verbatim user request>", and the enumerated surface (commands: <names>; skills: <names>; agents: <names>; templates: <names>), rank the top 3-5 candidates by capability fit. For each, summarize: what it does, when it wins over native Read/Edit/Glob/Grep/Bash, what flags or required inputs it expects, and any known caveats or recent behavioral changes.

### Step C — Per-candidate verification (the prerequisite gate)

For each candidate auggie returns, **before** it is allowed into the recommendation (in matched mode, for each step's command or skill in the matched routing row, whether or not auggie ranked it):

1. **Direct read** — Read the candidate's source file at the path recorded in Step A (any location in the search list). Extract: flag table, required-input rules, activation handoff, return contract.
2. **Auggie record** (skip in matched mode) — record the usage notes, related skills, and caveats auggie surfaced in Step B for this candidate.

A candidate that fails Step 1 (source file does not resolve) is a ghost. Drop it silently. Exception: a step of a matched routing row is never dropped; keep it and mark it `not installed: <name>` (see the ordered-workflow template in Phase 2). Do not warn the user about candidates that did not survive verification; the user does not need that noise.

Verification is **exempt** for built-in tools (`Read`, `Grep`, `Glob`, `Edit`, `Write`, `Bash`, `TodoWrite`, `WebFetch`, `WebSearch`) and for MCP server names referenced abstractly, and for the Claude Code built-in slash commands the routing guide names (`/code-review`, `/security-review`). Those have stable interfaces and verifying them adds overhead with no fabrication-risk return.

### Graceful degradation

| Failure | Response |
|---|---|
| Auggie MCP unavailable | Proceed with Glob+Read only. Emit a one-line header notice on the output: `Auggie unavailable — ranking falls back to literal Glob+Read; usage nuance may be thin.` Do not silently skip the gate, except in matched mode (Step 0 matched a routing row), where Step B is skipped. |
| Auggie returns empty | Note the gap in the output (`no auggie matches; ranking from file content only`) and proceed. The candidate may be new or rarely exercised — flag it rather than fake confidence. |
| Candidate source missing | Drop the candidate. Do not surface it. Exception: a matched routing row's step is kept and marked `not installed: <name>`. |
| User request is too vague to enumerate against | Ask one clarifying question. Do not emit a recommendation built on a guess. |

## Phase 1 — Level Check, then Net-Value Evaluation

**Routing row matched (Step 0):** the row decides the route. Do not replace it with native tooling or with a lighter command. Phase 1 only checks that each step's command or skill survived Phase 0 Step C. If one did not resolve, do not drop the step silently: keep it in its place, mark it `not installed: <name>`, and give the install hint for the full set (`pipx install git+https://github.com/IronbellyOrg/IronClaude && superclaude install`; plugin installs ship only some commands and skills). Also add one line to `degradation_notes`: `step <label> not installed: <name>`.

**No row matched, guide found:** place the goal on the guide's level table first, then answer the net-value questions inside that level.

- Level 1 (a question, nothing changes) and level 2 (one source file plus its test, five edits or fewer, exact change known): native tooling is allowed and is often right.
- The guide's **hard limit overrides native first.** If the work needs more than 5 edits or touches more than one source file (its matching test file does not count), never recommend a native edit sequence. Recommend a written plan instead: level 3 (`/sc:workflow --depth quick` then `/sc:implement`) for a few files with clear scope, level 4 (`/task-builder` then `/task`) for anything larger, longer, or riskier. The one exception is the guide's own: `/sc:cleanup` or `/sc:improve` on a folder, after a commit, with `git diff` reviewed afterwards.

**No guide:** apply the guide's hard limit, then the net-value questions. The hard limit: if the work needs more than 5 edits or touches more than one source file (its matching test file does not count), it must go through a written plan: level 3 for a few files with clear scope, level 4 for anything larger, longer, or riskier. The one exception is `/sc:cleanup` and `/sc:improve` run on a folder (guide section 3.7): commit first and review `git diff` afterwards.

For **every** surviving candidate, answer explicitly before recommending:

1. Does invoking `<skill/agent/command>` add value beyond a 2-3 step Read/Grep/Glob/Edit/Write sequence?
2. Is the overhead (token cost of the skill body, subagent spawn time, protocol complexity, hook gates) justified by specialized capability the model lacks natively in this context?
3. Would a senior engineer reading the user's request choose this delegation, or roll the equivalent themselves in less time?

If the honest answer to any of these is "no" or "barely", and neither a matched routing row nor the hard limit says otherwise, **default to native tooling**. The skill is allowed — and expected — to emit:

> No skill/agent delegation adds net value here. Use Read on `<file>`, then Edit. Reason: <one-line why>.

as a complete, valid recommendation. Anti-bloat is **core**, not optional. A recommendation engine that recommends delegation reflexively trains users to over-invoke and burns tokens for no gain.

When delegation **does** win, the recommended prompt must invoke the smallest delegation that earns its cost. Prefer `/sc:<x>` → skill → agent over `/sc:<x>` → skill → agent → sub-skill chains unless the longer chain is the documented best path.

See `refs/delegation-vs-native-heuristics.md` for the full rubric (when commands beat skills, when skills beat agents, when parallel `Agent` calls beat sequential skills, when native is strictly best).

## Phase 2 — Refined Prompt Construction

Build the prompt as a **hand-off envelope**, not a specification. The prompt carries:

- the target invocation (`/sc:<command>`, a skill's own slash name such as `/task-builder` or `/task` (`/<skill>`), `Skill <skill-name>`, `Agent <agent-name>`, or a native tool sequence)
- the user's verified parameters / file paths / flags
- the expected deliverable shape (what the user wants back)
- worktree-aware paths (resolved under `git rev-parse --show-toplevel`, which is the worktree's root when cwd is inside `.dev/worktrees/<name>/`)

The prompt MUST NOT restate the target's protocol logic — phase breakdown, scoring rules, agent roster, debate format, return contract internals. That belongs to the target skill. Trust the hand-off.

### Output template

````text
Goal: <one-line restatement of the user's intent>

Recommended delegation: <target name + why this wins net-value>

Paste-ready prompt:

```text
<the actual prompt — a hand-off envelope, not a specification>
```

Sources verified:

- <path/to/command.md> (Read)
- auggie semantic rank: <one-line summary>
````

If the recommendation is "use native tooling", drop the prompt block and emit the native-tool sequence as a numbered list instead.

### Ordered-workflow template (Step 0 matched a routing row)

````text
Goal: <one-line restatement of the user's intent>

Level: <the row's level; when the level is `-`, write "not on the six-level scale (a supporting task)"> — guide section <the row's section>, row `<the row's id>`

Changes files: <the row's changes_files: no | yes>

Run these in order:

1. <step 1, with the user's values in place of <placeholders>, plus every flag mandatory_flags lists for step 1>
2. <step 2 ...>
3a. <...> or 3b. <...> — say which one fits this goal
<a step whose command or skill did not resolve keeps its number: N. <step> (not installed: <name>)>

<only when a step is not installed:> Not installed here: <step labels and names>. Install the full set: pipx install git+https://github.com/IronbellyOrg/IronClaude && superclaude install

Notes:
- <each notes clause whose condition matches the user's goal>

Sources verified:
- <guide path> (routing table, row `<id>`)
- <path of each step's command or skill file> (Read)
- auggie semantic rank: skipped (matched row)
````

Rules for this template:

1. Emit every step of the row, in the row's order, with the row's labels. Steps that are not commands (for example "commit locally", "read the plan") are written as plain-language steps.
2. **Mandatory flags.** Every flag listed in the row's `mandatory_flags` for a step MUST appear on that step. Rule R1 still applies: if a mandatory flag is not in the verified command file's flag table or `argument-hint`, leave it out and add the note `guide flag <flag> not found in <file>; the guide may be out of date`.
3. Replace `<placeholders>` with values from the user's goal. When the goal does not give a value, keep the placeholder visible (for example `<task file>`). Never invent a path.
4. Include a `notes` clause only when its condition matches the goal; drop the Notes section when none matches.
5. When `changes_files` is `yes`, the `Changes files:` line is mandatory.
6. Claude Code built-in slash commands the guide names (`/code-review`, `/security-review`) are printed as they are (Rule R4).
7. Rule R3 still applies: name each command with its arguments and flags; never restate its protocol.

## Phase 3 — `--plugin` Mode (ecosystem search)

When `--plugin` is set, **ignore the entire local surface enumeration** and search the plugin / community-skill ecosystem instead. Local skills and plugins must not bleed into each other's outputs.

In-scope sources (this configuration):

- Claude Code plugin marketplaces (`claude-plugins-official`, anthropic-managed listings)
- Community skill repos (`anthropic/skills`, `sammcj/agentic-tools`, etc.)

Out-of-scope (this configuration): raw MCP server marketplaces. Do not surface MCP servers under `--plugin` unless the user explicitly asks for one in their request.

Search via (in priority order): `/sc:research "<query>" --depth deep` (web research), the `deep-research` agent, or Tavily MCP directly. WebFetch / WebSearch are last-resort fallbacks. Never use `/tech-research` here: it investigates the local codebase, not the web.

For every candidate, return:

- plugin / skill name
- one-sentence capability summary
- install command (single-line bash)
- repo URL
- GitHub star count + source URL (or `Stars: n/a — <curated|non-github|nested>` for bonus candidates)
- integration notes (what the user needs to wire up themselves)
- version / compatibility caveats
- citation (the URL the claim came from)

See `refs/plugin-ecosystem-sources.md` for the full source list, query patterns, and result-format template.

### Minimum-star floor + two-tier output (`--minstar`)

`--minstar <N>` sets the minimum GitHub-star floor for `--plugin` candidates. Resolve the floor as `N = --minstar value if passed else 500` — the **500 floor applies even when the flag is omitted** (default-on). `--minstar 0` disables the floor. A negative or non-integer value is a STOP: `"--minstar requires a non-negative integer (e.g. --minstar 500). Use --minstar 0 to disable the floor."`

**Local-mode guard (warn-and-ignore)**: `--minstar` only has meaning in `--plugin` mode. If `--minstar` is passed WITHOUT `--plugin`, emit exactly one notice — `"--minstar has no effect without --plugin (the local surface has no stars); ignoring it."` — then run the normal local recommendation (Phase 0-2). Never a STOP.

**Delegated star capture**: because the ecosystem search is delegated (not run inline), the generated search prompt MUST instruct the delegate to capture each candidate's GitHub star count and its source URL. The skill then enforces the floor and the two-tier split on the returned set. A star count is a claim — Rule R1/citation discipline forbids inventing one; an undiscoverable count routes the candidate to the bonus section, never to a guessed number.

**Two-tier output**:

- **Primary** — candidates with a discoverable own-repo star count `>= N`, sorted by stars **descending**. Each shows a `Stars` field with its source URL. Keep the top-3 disambiguator discipline.
- **Bonus — not ranked by GitHub stars** — credible candidates with no own-repo star count, **never filtered by the floor**, each labeled with the reason: `curated` (Anthropic-curated marketplace entry), `non-github` (source is not a GitHub repo), or `nested` (skill/plugin lives inside a larger repo whose stars are not attributable to it). Same top-3 discipline.

If the floor removes every GitHub candidate but bonus candidates exist, surface the bonus section with a one-line note: `"No candidate met the >= N star floor; showing unranked credible matches below. Lower the floor with --minstar <smaller>."` If nothing credible survives at all, reuse the existing "found nothing credible" guidance.

### `--plugin --eval` adoption lifecycle (4 phases)

When `--plugin` is combined with `--eval <mode>` (mode ≠ `none`), the skill runs the plugin adoption gate. The CLI owns the deterministic half (precondition HARD-BLOCK, adoption verdict, plugin-row patch); the skill owns the Agent-spawned eval panels. The four phases:

1. **Discovery** — `--plugin <query>` with no eval mode surfaces the candidate plugin/MCP resource + metadata (install command, `setup_steps`, repo URL, citations). No row is committed (browse mode).
2. **Adoption proposal** — `--plugin <query> --eval <mode>` runs the eval pipeline twice per panel cell: with the resource INSTALLED vs UNINSTALLED, on synthetic cases generated from the plugin's stated capabilities (the cold-path `--eval` fan-out below produces the per-(model,run) deliverables for each configuration). Install steps that need OAuth / API keys / env vars are EMITTED for the user to run — the skill never auto-completes auth flows; the user confirms readiness before the with-resource runs.
3. **Decision gate** — after the panels finalize, the parent shells the CLI:

   `uv run superclaude recommend eval plugin --key <plugin-key> --preconditions-file <path> --with-resource-file <agg.json> --without-resource-file <agg.json>`

   Run it only when the Availability gate passed. If it cannot run (gate failed, or the command is missing), stop the adoption lifecycle after phase 2 and tell the user the decision gate needs an IronClaude checkout. A non-zero exit from a failed hard precondition keeps its existing meaning (HARD-BLOCK).

   `run_preconditions` runs FIRST and **HARD-BLOCKS** on any `failure_mode: hard` precondition (e.g. the MCP server is not installed) — the CLI exits non-zero, no degraded fallback. On pass, `evaluate_adoption` applies the threshold (`pass_rate +≥0.10` **OR** `token −≤−0.20`, with `pass_rate` must-not-regress) and `patch_plugin_row` writes `adoption_status` (`evaluated_positive` / `evaluated_negative`) + an `eval_history` entry to `.claude/cache/sc-recommend-plugin.yaml` via the atomic writer.
4. **Hot-path use** — a later `--plugin <query>` matching the row reads its `adoption_status`: `evaluated_positive` rows emit the install command (if not locally installed) + best-model hint; `evaluated_negative` rows are kept (30-day TTL) but never surfaced as a hot-path recommendation.

## Cold-Path Write-Back (populate the cache on a miss)

The cold path **is** Phase 0–3 above — run when the Hot-Path Cache Lookup returned `outcome: "miss"` (any of the three miss reasons this skill can get: `miss_no_key`, `miss_low_confidence`, `miss_validation_stale`). A `native` outcome does **not** reach the cold path. Phase 0–3 run inside a **second** `model: haiku` subagent so the expensive enumerate→auggie→verify work happens in an isolated context, not the parent.

1. **Spawn the cold-path Haiku subagent.** Use the Agent tool, `model: haiku`, handing it the condensed runbook as its system context (Read `src/superclaude/cli/recommend/prompts.py` under the repository root (`git rev-parse --show-toplevel`) and use the text of the string assigned to `COLD_PATH_RUNBOOK`, without the quote marks) — **not** the full SKILL.md body (inlining the full skill would recreate the exact ~91K cost the cache exists to remove). The subagent runs Phase 0–3 (Glob → auggie → Read-verify → net-value → prompt) and returns the recommendation **plus** a structured `cache_update` payload (the row to commit: `key`, `candidate`, `flags`, `prompt_envelope_template`, `rationale`, `source_path`, `native_fallback`). If the runbook file cannot be read, run Phase 0–2 inline in this context instead of spawning the subagent, and skip steps 2–4. Pass the guide's level-table block and its other-commands block (or the line `no guide`) and the Step 0 result (`no_match` or `absent`) in the subagent prompt.

2. **Parent commits the cache_update.** Haiku **cannot write files**, so the parent (this skill, the Claude session) commits the row by shelling to the CLI atomic writer:

   `uv run superclaude recommend cache put --row-json '<the cache_update row as a single-line JSON object>'`

   If this call exits non-zero, do not retry; emit the recommendation anyway and add "cache write skipped: <exit code>" to degradation_notes.

   This routes through `LookupCache.save()` (atomic tmp + `os.replace`). The CLI recomputes the current `surface_hash` and the full per-row `source_hash` on write — the parent never trusts a Haiku-computed hash.

3. **Optional `--eval` trigger (Agent fan-out + finalize).** If the invocation carried `--eval <mode>` (mode ≠ `none`), evaluate the just-inserted row's `best_model`. Opt-in only. Under Option P the CLI cannot spawn Agents (anthropic SDK banned), so the **skill (parent session) emits the fan-out** and the CLI does the deterministic finalize:

   a. **Resolve the panel** for `<mode>` from `MODE_MATRIX`: `quick` = `opus`×1 (**1** Agent call); `normal` = `opus`+`sonnet`×2 (**4** Agent calls); `deep` = `opus`+`sonnet`+`haiku`×3 (**9** Agent calls). `none` = no-op.

   b. **Fan out** — emit one parallel Agent-tool call per `(model, run)` cell, each with the corresponding `model:` (e.g. `deep` → opus run-1/2/3 + sonnet run-1/2/3 + haiku run-1/2/3). Each Agent produces the real deliverable for the row and writes **both** files at the EXACT path the finalizer reads:

      - `.claude/cache/eval-runs/iteration-<N>/<key>/<model>/run-<i>/outputs/recommendation.md`
      - `.claude/cache/eval-runs/iteration-<N>/<key>/<model>/run-<i>/timing.json`

      (the `<i>` is the 1-based run number; `<N>` is one more than the highest existing `iteration-*` folder under `.claude/cache/eval-runs/`, or 1 if none exists; tokens are NOT auto-captured, so each Agent MUST emit `timing.json` itself.)

   c. **Finalize (CLI, deterministic).** After all Agent calls complete, the parent shells: `uv run superclaude recommend eval run --key <key> --mode <mode> --iteration <N>` (the same `<N>` as in step b). This grades each deliverable, aggregates per model, selects `best_model` by tier, writes `row-<key>-results.json`, and patches the lookup row's `best_model` + `eval_history` via the atomic writer. The finalizer assumes the deliverables already exist on disk — the fan-out in (b) must have produced them at the exact layout above, or grading sees empty text. If this call exits non-zero, report the eval as not finalized and keep the recommendation.

4. **Emit + telemetry.** Surface the recommendation verbatim, then append exactly one telemetry event with `--cache-result cold_inserted` (or the original miss reason if no row was inserted): `uv run superclaude recommend telemetry append --mode delegate --cache-result cold_inserted --classification-key <key> --duration-ms <ms>`. If the telemetry call fails, ignore the failure.

The cold path emits the **same Return Contract** shape as the hot path (caller parity). No protocol of any recommended target is restated in the `cache_update` (R3) — the `prompt_envelope_template` is a hand-off envelope.

## Output Constraints — Anti-Fabrication Rules

These rules are non-negotiable. They survived from the old skill because they were the only parts that held up under scrutiny.

### Rule R1 — No unverified flags

A flag may appear in the recommended prompt **only if** it is present in the verified target's flag table (or `argument-hint`). Example: `/sc:adversarial` has a fixed flag set in `src/superclaude/commands/adversarial.md`; no flag may be attached to it that is not in that file. Fabricated flags (`--rounds`, `--measure-first`, `--verdict-per-claim`, etc., when they do not exist) are forbidden.

### Rule R2 — No unverified commands or skills

A command or skill may appear **only if** its source file was resolved in Phase 0 Step C. Auggie-mentioned but not file-resolved → drop. Memory-recalled but not file-resolved → drop. A matched routing row's step whose file does not resolve appears only marked `not installed: <name>`, never as a runnable step. Exception: the Claude Code built-in slash commands that the routing guide names (`/code-review`, `/security-review`) have no source file and may appear without one (Rule R4).

### Rule R3 — No protocol reimplementation (the load-bearing rule)

When a verified target has `activation_style: skill-indirected` (its command file delegates to a protocol skill via `## Activation > Skill <name>`), the generated prompt MUST be a **hand-off**, not a **specification**.

- **Allowed**: `Run: /sc:adversarial --compare fileA.md,fileB.md --focus structure --depth standard`
- **Forbidden**: any inline content that restates the target's protocol — debate rules, phase counts, scoring formulas, "steelman strategy", artifact lists. The protocol skill owns that behavior; the prompt invokes and trusts.

R3 enforces: **invoke, don't reimplement**. Duplicating a target's protocol inline causes drift, wastes tokens, and produces prompts that disagree with the actual command when the command is run.

### Rule R4 — Built-ins exempt

`Read`, `Grep`, `Glob`, `Edit`, `Write`, `Bash`, `TodoWrite`, `WebFetch`, `WebSearch` are harness primitives. Recommend them by name without verification. The same holds for the Claude Code built-in slash commands the routing guide names: `/code-review` and `/security-review`.

## Return Contract

| Field | Type | Description |
|---|---|---|
| `status` | string | `success`, `clarification_needed`, `degraded`, `plugin_search` |
| `mode` | string | `local` (default) or `plugin` |
| `recommendation_kind` | string | `delegation_prompt`, `native_tooling`, `multi_path`, `plugin_candidate`, `ordered_workflow` |
| `prompt_block` | string | The paste-ready prompt (empty for `native_tooling`) |
| `verified_sources` | list | Paths Read in Step 0 (the guide) and Phase 0 Step C |
| `auggie_status` | string | `ok`, `unavailable`, `empty`, `skipped` (matched mode: Step B is not run; the stored value is exactly `skipped`, and the ordered-workflow template only displays it as `skipped (matched row)`) |
| `degradation_notes` | string | One-line note when degraded |
| `guide_status` | string | `matched` (a routing row decided the answer), `no_match`, `absent` (guide not found), `not_applicable` (`--plugin` mode) |
| `routing_row_id` | string | The matched row's `id`; empty unless `guide_status` is `matched` |

## Boundaries

**Will:**

- Read the routing guide first (Step 0), then enumerate the live surface (commands, skills, agents, templates) on every invocation
- Use auggie to semantically rank candidates against the user's request
- Verify every candidate against its source file before emitting
- Emit refined paste-ready prompts that hand off to existing skills/commands/agents
- Recommend native tooling when delegation does not add net value
- Switch to ecosystem search when `--plugin` is set
- Apply the `--minstar` floor (default 500) + star-descending sort in `--plugin` mode, with a separate bonus section for credible candidates that have no own-repo star count; warn-and-ignore `--minstar` in local mode
- Cite every source it read

**Will Not:**

- Keep its own hand-written keyword → category table (root cause of the old skill's discovery failure). The guide's routing table, read in Step 0, is the only fixed routing source.
- Invent flags or commands not present in source files (R1, R2)
- Restate a target's protocol logic inline in the prompt (R3)
- Mix local-surface candidates with `--plugin` ecosystem results
- Execute the recommended prompt (the user pastes it manually)
- Estimate time, budget, or token cost (out of scope for prompt generation)
- Detect user language (English-only — Turkish detection from old skill is dropped)
- Detect project framework from file system heuristics (this skill ships in the SuperClaude repo; the relevant context is the source tree, not which JS framework is present)

## Related References

- `refs/surface-enumeration.md` — Phase 0 glob set, auggie sweep algorithm, verification record schema
- `refs/delegation-vs-native-heuristics.md` — the net-value rubric (Phase 1)
- `refs/plugin-ecosystem-sources.md` — `--plugin` search targets and result template
