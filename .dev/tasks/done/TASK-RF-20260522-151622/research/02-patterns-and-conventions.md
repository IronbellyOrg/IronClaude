# Research: Patterns & Conventions

**Topic type:** Patterns & Conventions
**Scope:** SKILL.md wave templates, command-file conventions
**Status:** Complete
**Date:** 2026-05-22
---

## Pattern 1: Canonical Wave block template

**Verbatim quote of Wave 3** (SKILL.md:167-217):

````markdown
### Wave 3: Tier 2 — Parallel Hypotheses

**Goal**: Cast a wider net with multiple independent perspectives, then surface the strongest candidate fixes.

**Preconditions**: Wave 2 decided to escalate.

**Agent selection** — pick 2-4 agents based on `--type` and signal mix. Each agent runs in its own context, in parallel, via `Task`:

| Signal / type | Agents to spawn |
|---------------|------------------|
| `bug` (default) | `root-cause-analyst`, `quality-engineer` (edge cases), + 1 of {`refactoring-expert` if recent refactor signals, `system-architect` if multi-component} |
| `performance` | `performance-engineer`, `root-cause-analyst`, `system-architect` (if cross-component) |
| `security` | `security-engineer`, `root-cause-analyst`, `quality-engineer` |
| `build` | `root-cause-analyst`, `devops-architect`, `refactoring-expert` |
| `deployment` | `devops-architect`, `root-cause-analyst`, `system-architect` |
| `test` | `quality-engineer`, `root-cause-analyst`, `refactoring-expert` (if test is brittle by structure) |

Cap at 4 agents. If `--type` is unset and signals point in multiple directions, spawn 3 from the union of relevant rows.

**Steps**:

1. **MCP enrichment in parallel with agent spawn** — issue any of the following that match the signals (parallel calls, all kicked off in the same turn):
   - `mcp__context7__resolve-library-id` + `mcp__context7__query-docs` when the issue mentions a framework / library by name or the stack trace is in third-party code
   - `mcp__tavily__tavily-search` for the exact error message string + "github issue", or for `<library> <version> <symptom>` (rate-limited — at most 2 queries in this wave)
   - `mcp__auggie__codebase-retrieval` with a more targeted query than Tier 1 (e.g. "find every call site of `<symbol>` and how they handle the error case")
2. **Spawn hypothesis agents** in parallel via `Task` (single message with multiple Task calls). Each agent receives:
   - The original issue + Tier 1 hypothesis card (so they can agree, disagree, or extend)
   - The MCP enrichment results
   - The output path for their own hypothesis card: `<output-dir>/tier2-<agent-name>-hypothesis.md`
   - An instruction to produce **at most one proposed fix** with: claim, evidence (cited file:line or command output), proposed fix, confidence, risks, and a one-line "if I'm wrong it's probably because...".
   - Use the agent's default model. If `--models` overrides per-tier, apply (e.g. `hypothesis:opus` forces all hypothesis agents to opus).
3. **Wait for all agents** to complete. Read each card.
3.5. **Calibrate each card independently** — spawn N `confidence-calibrator` instances in parallel (one per Tier 2 card), each with `card_tier=2` and `output_path=<output-dir>/tier2-<agent-name>-calibration.md`. Use the calibrated scores (not the agents' self-reports) when weighting consensus/competing/outlier in step 4. Fallback rule from Wave 1 applies per-card.
4. **Distill candidate fixes**: cluster the hypothesis cards by proposed fix. If 2 or more agents propose substantively different fixes, mark them as **competing**. If they all converge on one fix, mark as **consensus**.

**Exit criteria**:

- ≥ 1 hypothesis card written to disk
- A `candidate-fixes.md` index file written listing each unique fix proposal, the supporting agent(s), and a quick verdict (`consensus` / `competing` / `outlier`)

**Failure handling**:

| Scenario | Behavior | Fallback |
|----------|----------|----------|
| Agent subprocess fails | Continue with remaining agents; record failure in audit | If < 2 agents complete, downgrade to "Tier 1 only" and add a warning to the report |
| MCP call fails (auggie/serena) | Fall back to `Grep`/`Glob`; note in audit | None — proceed without that enrichment |
| MCP call fails (context7/tavily) | Continue without external docs; note in audit | None |
| All agents converge with high confidence | Skip Wave 4 (adversarial); jump to Wave 5 | None |
| All agents diverge with low confidence | Proceed to Wave 4; warn in audit that no fix is strongly supported | None |

---
````

**Abstracted template** (the structural skeleton Wave 1.5 must replicate):

- **Section header format**: `### Wave N: <Tier-tag if applicable> — <Short title>` — three-hash, em-dash separator between tier tag and title, no trailing punctuation.
- **Goal line**: `**Goal**: <one-sentence purpose>.` — bold key, colon, then sentence ending with a period.
- **Preconditions paragraph format**: `**Preconditions**: <prior-wave reference or condition>.` — single line, bold key, refers to prior wave's exit state.
- **Steps numbering style**: Top-level numeric (`1.`, `2.`, `3.`) with bold lead-in phrase + em-dash + description. Sub-steps use indented dash bullets (`- ...`). Half-step interleaves use decimal numbering (e.g., `3.5.`) when injected later — precedent: Wave 3 step 3.5 at SKILL.md:199.
- **Task spawning description**: Spelled `via \`Task\`` (backticked, single capital T). Brief construction uses imperative voice — "spawn the `<agent-name>` agent via `Task` with <key>=<value>, <key>=<value>..." — see Wave 1 step 3 (SKILL.md:137) and Wave 5 step 3 (SKILL.md:264). No `subagent_type:` / `mode:` keys are exposed; agents are named directly.
- **Output collection**: File paths are templated with `<output-dir>/<wave-prefix>-<agent-name>-<artifact>.md` (e.g., `<output-dir>/tier2-<agent-name>-hypothesis.md` at SKILL.md:195). Outputs are written by the agent, then orchestrator reads them back ("Wait for all agents to complete. Read each card." at SKILL.md:198).
- **Exit criteria format**: `**Exit criteria**: <inline list>` OR (when multi-line) `**Exit criteria**:` followed by `-` bullets. Often closes with `Emit "Wave N complete: <key>=<value>".` — precedent: Wave 0 (SKILL.md:115), Wave 1 (SKILL.md:141).
- **Wave separator**: A bare `---` horizontal rule between waves, with one blank line above and below.

---

## Pattern 2: Wave 3 parallel-fan-out specifics

**Per-agent brief construction** (SKILL.md:192-197):

```markdown
2. **Spawn hypothesis agents** in parallel via `Task` (single message with multiple Task calls). Each agent receives:
   - The original issue + Tier 1 hypothesis card (so they can agree, disagree, or extend)
   - The MCP enrichment results
   - The output path for their own hypothesis card: `<output-dir>/tier2-<agent-name>-hypothesis.md`
   - An instruction to produce **at most one proposed fix** with: claim, evidence (cited file:line or command output), proposed fix, confidence, risks, and a one-line "if I'm wrong it's probably because...".
   - Use the agent's default model. If `--models` overrides per-tier, apply (e.g. `hypothesis:opus` forces all hypothesis agents to opus).
```

Variables interpolated into the brief: original issue text, prior-wave card content, MCP enrichment, per-agent output path templated with `<agent-name>`. Refs are NOT loaded as separate variables here — the agent's instruction set IS the brief; refs are loaded by the orchestrator per-wave (see the Refs table) and passed in by reference or contents.

**Parallel-spawn-in-single-message phrasing** (SKILL.md:192):

> "Spawn hypothesis agents in parallel via `Task` (single message with multiple Task calls)."

This is the canonical phrasing the executor must reuse for any parallel fan-out. The parenthetical `(single message with multiple Task calls)` is load-bearing — it tells the orchestrator how to actually batch.

**Per-agent output directory pattern** (SKILL.md:195):

> "The output path for their own hypothesis card: `<output-dir>/tier2-<agent-name>-hypothesis.md`"

Outputs go to predictable paths inside `<output-dir>/`, named by tier-prefix + agent-name + artifact-type. Wave 1.5 should follow `<output-dir>/wave1_5-<branch-letter>-<artifact>.md` or an analogous template; a consistent prefix lets Wave 5 synthesis collect them deterministically.

**Wait-then-read collection step** (SKILL.md:198):

> "3. **Wait for all agents** to complete. Read each card."

Single-line bold-numbered step. Orchestrator blocks until all parallel agents return, then reads each output file.

**Post-fan-out synthesis precedent** (SKILL.md:199-200, the 3.5 + 4 pair):

```markdown
3.5. **Calibrate each card independently** — spawn N `confidence-calibrator` instances in parallel (one per Tier 2 card), each with `card_tier=2` and `output_path=<output-dir>/tier2-<agent-name>-calibration.md`. Use the calibrated scores (not the agents' self-reports) when weighting consensus/competing/outlier in step 4. Fallback rule from Wave 1 applies per-card.
4. **Distill candidate fixes**: cluster the hypothesis cards by proposed fix. If 2 or more agents propose substantively different fixes, mark them as **competing**. If they all converge on one fix, mark as **consensus**.
```

Two distinct post-fan-out moves: (3.5) a per-card calibration sub-fan-out, then (4) a synthesis/clustering step. Wave 1.5's synthesis can mirror step 4 — one step, bolded lead-in, an imperative verb (`cluster`, `distill`, `synthesize`), and a description of the deterministic output (cards classified into named verdicts).

---

## Pattern 3: Refs loader table format

**Verbatim quote of Refs table** (SKILL.md:377-383):

```markdown
| File | When loaded |
|------|-------------|
| `refs/escalation-rubric.md` | Wave 2 (confidence gate) and Wave 1 (calibration) |
| `refs/triage-checklist.md` | Wave 1 (passed to root-cause-analyst as part of the brief) |
| `refs/hypothesis-card-template.md` | Wave 1 and Wave 3 (passed to agents) |
| `refs/report-template.md` | Wave 5 |
| `refs/remediation-handoff.md` | Wave 6 |
```

Surrounding context (SKILL.md:375-385):

```markdown
## Refs

| File | When loaded |
|------|-------------|
| `refs/escalation-rubric.md` | Wave 2 (confidence gate) and Wave 1 (calibration) |
| `refs/triage-checklist.md` | Wave 1 (passed to root-cause-analyst as part of the brief) |
| `refs/hypothesis-card-template.md` | Wave 1 and Wave 3 (passed to agents) |
| `refs/report-template.md` | Wave 5 |
| `refs/remediation-handoff.md` | Wave 6 |

Each ref is loaded only by the wave that needs it. Do not pre-load.
```

**Format observations**:

- **Sort order**: Sorted by **wave number of first load** (escalation-rubric → Wave 1+2, triage-checklist → Wave 1, hypothesis-card-template → Wave 1+3, report-template → Wave 5, remediation-handoff → Wave 6). Not alphabetical. The first row breaks the strict ordering because it's used in Wave 2 as the primary purpose ("confidence gate") even though Wave 1 also uses it for calibration — the row reads "Wave 2 (...) and Wave 1 (...)" reflecting that.
- **Cell content style for "When loaded"**: Pattern is `Wave N (<short purpose>)` for single-wave loaders, e.g., `Wave 5` (bare when no qualifier needed) or `Wave 2 (confidence gate)`.
- **Multi-wave loaders**: Use the connective `and` (English word), not commas or `+` — e.g., `Wave 2 (confidence gate) and Wave 1 (calibration)` and `Wave 1 and Wave 3 (passed to agents)`. The second example shows a single parenthetical applies to both waves when the purpose is the same.
- **Filename style**: Backticked path-style `refs/<name>.md`, no leading slash, no escaping.
- **Closing line**: A free-standing sentence below the table: `Each ref is loaded only by the wave that needs it. Do not pre-load.` — Wave 1.5 must not violate this; if it introduces a new ref, the ref's row must say `Wave 1.5 (<purpose>)`.

---

## Pattern 4: Graceful Degradation table format

The SKILL.md does NOT have a section literally titled "Graceful Degradation". The functional equivalent is the **Error Handling** table at SKILL.md:348-362, plus the per-wave **Failure handling** table inside Wave 3 (SKILL.md:209-215). Both follow the same `Scenario | Behavior | Fallback` schema.

**Verbatim quote of Error Handling table** (SKILL.md:348-362):

```markdown
## Error Handling

| Scenario | Behavior | Fallback |
|----------|----------|----------|
| All MCPs unavailable | Run in `--no-mcp` mode; warn user that triage quality is degraded; native tools only | None |
| auggie unavailable (others OK) | Fall back to `Grep` + `Glob` for grounding; mark in audit | None |
| root-cause-analyst agent fails in Tier 1 | Skill produces a degraded Tier 1 (Claude inline) and recommends `--depth deep` | None |
| All Tier 2 agents fail | Downgrade to Tier 1 result; report `partial`; recommend rerun | None |
| `sc:adversarial-protocol` fails in Wave 4 | Pick the highest-confidence Tier 2 fix proposal as the chosen fix; note in audit and report header | None |
| `self-review` flags blocker on adversarial merge | STOP at Wave 5 with `partial` status; report includes the blocker; recommend rerun with `--depth deep` or different focus | None |
| `task-builder` unavailable in Wave 6 | Surface the fix proposal path; recommend manual task creation; don't fail the whole skill | None |
| User declines remediation offer | Return success; report stands | None |
| `--depth deep` requested on under-specified input | STOP at Wave 0; ask user to add detail | None |
| `evidence-validator` agent fails (subprocess crash, timeout, or malformed report) | Inline-validate citations in the orchestrator context (the original Wave 5 step 3 behavior); mark `status: partial` and add a Grounding Gap entry noting the validator was unavailable | None — the inline path is the fallback |
| `confidence-calibrator` agent fails for any card | Fall back to inline orchestrator calibration for that card; mark the card with `calibration: inline-fallback` in the audit log; do NOT block escalation on a missing calibration | None |
```

**Verbatim quote of Wave 3 Failure handling sub-table** (SKILL.md:209-215):

```markdown
**Failure handling**:

| Scenario | Behavior | Fallback |
|----------|----------|----------|
| Agent subprocess fails | Continue with remaining agents; record failure in audit | If < 2 agents complete, downgrade to "Tier 1 only" and add a warning to the report |
| MCP call fails (auggie/serena) | Fall back to `Grep`/`Glob`; note in audit | None — proceed without that enrichment |
| MCP call fails (context7/tavily) | Continue without external docs; note in audit | None |
| All agents converge with high confidence | Skip Wave 4 (adversarial); jump to Wave 5 | None |
| All agents diverge with low confidence | Proceed to Wave 4; warn in audit that no fix is strongly supported | None |
```

**Format observations**:

- **Column structure**: Exactly three columns — `Scenario | Behavior | Fallback`. Same schema in both the global Error Handling table and the per-wave Failure handling sub-table.
- **Per-MCP rows**: The global Error Handling table distinguishes `All MCPs unavailable` (line 352) vs `auggie unavailable (others OK)` (line 353) — both `<MCP-name> unavailable [(qualifier)]`. Per-server fine-grained rows exist only for auggie; the rest are grouped under "All MCPs unavailable" or in per-wave sub-tables (e.g., Wave 3 has `MCP call fails (auggie/serena)` and `MCP call fails (context7/tavily)`).
- **"Note in audit" boilerplate phrasing**: Recurring phrases include `mark in audit`, `note in audit`, `record failure in audit`, and the longer form `mark the card with \`<key>: <value>\` in the audit log`. Verbatim examples from the tables:`mark in audit` (line 353), `note in audit and report header` (line 356), `note in audit` (lines 212, 213). The skill does NOT use a single canonical phrase — variants are acceptable as long as the audit-log channel is named.
- **Tiers mentioned per-row**: Rows are tier-tagged inline when relevant — e.g., `root-cause-analyst agent fails in Tier 1`, `All Tier 2 agents fail`, `sc:adversarial-protocol fails in Wave 4`, `task-builder unavailable in Wave 6`. The tier/wave is named in the **Scenario** column, not in a separate column.
- **Fallback column conventions**: `None` is the most common entry; longer fallback chains use a full sentence (e.g., `If < 2 agents complete, downgrade to "Tier 1 only" and add a warning to the report`). The phrase `None — the inline path is the fallback` (line 361) appears when the Behavior column already describes a fallback path and the Fallback column is functionally redundant.

---

## Pattern 5: MCP Integration block

SKILL.md does not have a section literally titled "MCP Integration" — the closest semantic equivalent is the **Tool Coordination Summary** matrix at SKILL.md:310-324 (covering all tools, not just MCPs). The narrative MCP-by-MCP "block" the deliverable describes actually lives in the **command file** at `commands/troubleshoot.md:83-89`.

**Verbatim quote of the MCP Integration block** (commands/troubleshoot.md:83-89):

```markdown
## MCP Integration

- **Auggie** (primary, free retrieval): Tier 1 + Tier 2 codebase grounding via `mcp__auggie__codebase-retrieval`. Offloads heavy retrieval to a free / low-cost tier, keeping the Claude token budget tight.
- **Serena**: Tier 1 + Tier 2 symbol-level navigation via `find_symbol`, `find_referencing_symbols`, `get_symbols_overview`. Critical when the issue names a specific function or class.
- **Context7**: Tier 2 only, when the symptom mentions a framework or library by name or the stack trace ends in third-party code.
- **Tavily**: Tier 2 only, rate-limited to ≤ 2 queries per invocation. Used for `<exact error string> github issue` and `<library> <version> <symptom>` lookups.
- **Sequential**: Tier 2 synthesis when reconciling competing hypotheses.
```

**Verbatim quote of the SKILL.md Tool Coordination Summary** (SKILL.md:310-324):

```markdown
## Tool Coordination Summary

| Tool | Tier 1 | Tier 2 | Tier 3 |
|------|--------|--------|--------|
| `mcp__auggie__codebase-retrieval` | ✓ (one focused query) | ✓ (per-hypothesis queries) | — |
| `mcp__serena__find_symbol` / `find_referencing_symbols` / `get_symbols_overview` | ✓ | ✓ | — |
| `mcp__context7__query-docs` | — | ✓ when framework/library named | — |
| `mcp__tavily__tavily-search` | — | ✓ rate-limited (≤2 queries) | — |
| `mcp__sequential-thinking__sequentialthinking` | — | ✓ for synthesis | — |
| `Task` (agent spawn) | ✓ (root-cause-analyst + confidence-calibrator) | ✓ (2-4 hypothesis agents in parallel + per-card confidence-calibrator + evidence-validator at Wave 5) | ✓ (self-review for post-exec) |
| `Skill` | — | ✓ (`sc:adversarial-protocol`) | ✓ (`task-builder`, `/sc:reflect`) |
| `Read` / `Grep` / `Glob` | ✓ | ✓ | — |
| `Bash` | ✓ (repro when cheap) | ✓ (diagnostic commands) | — |
| `Write` | ✓ (hypothesis + report) | ✓ (hypothesis cards, fix proposals) | — |
```

**Per-MCP bullet structure** (from commands/troubleshoot.md):

- Opening pattern: `- **<MCP-name>** [(brief role)]: <tier scope> via <tool function names>. <Purpose sentence.>`
- Tier scope phrasing: `Tier 1 + Tier 2` (with literal `+`), `Tier 2 only`, or `Tier 2 synthesis when ...`.
- Tool function names: Comma-separated when multiple under one MCP (e.g., serena's `find_symbol`, `find_referencing_symbols`, `get_symbols_overview`) — listed bare, not backticked individually only when they're under the same MCP family.
- Purpose sentence: Always ends with a period. Frequently includes a `Critical when ...` qualifier or a token-budget rationale.

**Where Wave 1.5's load-bearing Auggie usage would slot in**:

- In `commands/troubleshoot.md:85` (the `**Auggie**` bullet): the tier scope `Tier 1 + Tier 2 codebase grounding via mcp__auggie__codebase-retrieval` needs to broaden to include Wave 1.5 — candidate amended phrasing: `Tier 1, Wave 1.5 (documentation grounding), and Tier 2 ...`.
- In `SKILL.md:314` (the `mcp__auggie__codebase-retrieval` row of the Tool Coordination Summary): the matrix is keyed by Tier (1/2/3), not Wave. If Wave 1.5 needs its own column or is collapsed under Tier 1, the executor will need to either (a) annotate the Tier 1 cell with `(one focused query + Wave 1.5 doc-grounding queries)` or (b) add a separate Wave 1.5 column — researcher 3 will document the integration choice; this researcher only flags the insertion point.

---

## Pattern 6: Options table cell format (command file)

**Verbatim quote of full Options table** (commands/troubleshoot.md:46-57):

```markdown
## Options

| Flag | Default | Description |
|------|---------|-------------|
| `--type` | auto-detect | One of `bug`, `build`, `performance`, `deployment`, `security`, `test`. Auto-detected from keywords + structural cues in the issue description. |
| `--depth` | `standard` | `quick` (Tier 1 only, ~1-3 min, ~3-6k Claude tokens), `standard` (auto-escalate by rubric), `deep` (force Tier 2 with adversarial debate). |
| `--scope` | (none) | File, directory, or symbol to narrow auggie/serena queries against. |
| `--no-escalate` | `false` | Cap at Tier 1 regardless of confidence. Useful for quick second-opinion passes. |
| `--fix` | `false` | After diagnosis, offer the Tier 3 remediation chain (`task-builder` → `/sc:reflect --type task --analyze` → user runs `/task` → `/sc:reflect --type task --validate`). Code changes never auto-apply; the user runs `/task`. |
| `--models` | (agent defaults) | Per-tier model override, e.g. `tier1:sonnet,hypothesis:opus`. |
| `--output-dir` | `.dev/troubleshoot/<slug>-<timestamp>/` | Where REPORT.md, hypothesis cards, fix proposals, adversarial artifacts, and audit log are written. |
| `--no-mcp` | `false` | Run in native-tools-only mode (skip auggie/serena/context7/tavily). Tier 1 quality degrades; surfaced in the report. |
```

**Format observations** (specific to the `--no-escalate` and `--fix` rows the deliverable called out):

- **Flag column**: Backticks around the literal flag, including the leading `--`. Examples: `` `--no-escalate` ``, `` `--fix` ``. Never bare. Never single-quoted.
- **Default column**:
  - Booleans: backticked literal — `` `false` ``, `` `standard` ``.
  - Sentinels: parenthesized prose without backticks — `(none)`, `(agent defaults)`, `auto-detect` (also unbacked — `auto-detect` is bare because it's a phrase, not a value).
  - Paths: backticked, with template placeholders inside backticks — `` `.dev/troubleshoot/<slug>-<timestamp>/` ``.
- **Description column style**:
  - **Sentence case**, starts with a capital letter or backticked literal that begins with `--`.
  - Two-sentence form is common: first sentence states the behavior (imperative-ish but past/present declarative — `Cap at Tier 1 regardless of confidence.`); second sentence adds a usage rationale or downstream consequence (`Useful for quick second-opinion passes.`).
  - Mentions other phases/tiers explicitly: `--fix` row references the Tier 3 chain with literal subcommand sequence (`` `task-builder` → `/sc:reflect --type task --analyze` → user runs `/task` → `/sc:reflect --type task --validate` ``) using `→` arrows.
  - Closes with a hard rule sentence when relevant: `Code changes never auto-apply; the user runs /task.` (semicolon-joined hard rule).
- **The pattern Wave 1.5's `--no-doc-discovery` row should follow**: backticked flag, backticked `` `false` `` default, two-sentence description — first sentence says what suppressing the flag does, second sentence gives the use case (e.g., "Useful when the codebase has no formal docs or the user has already grounded the symptom externally.").

---

## Pattern 7: Boundaries Will / Will Not bullet style

**Verbatim quote of full Will / Will Not sections** (commands/troubleshoot.md:155-178):

```markdown
## Boundaries

**Will:**

- Always run Tier 1 first (respect the "quick first option" contract)
- Auto-escalate to Tier 2 only when the rubric in `refs/escalation-rubric.md` says so, or when `--depth deep` is set
- Fan out 2-4 specialist agents in parallel in Tier 2 (capped at 4 by signal mix)
- Use auggie + serena every tier for in-repo grounding; use context7 + tavily only in Tier 2 and only when the symptom suggests external knowledge
- Invoke `sc:adversarial-protocol` only when Tier 2 produces 2-3 competing strong fixes (skip on consensus — that wastes the debate)
- Run `evidence-validator` in Wave 5 to drop any unfounded `file:line` citations before REPORT.md ships
- Run `confidence-calibrator` after every hypothesis card to defeat self-grading anchoring bias
- Offer the Tier 3 remediation chain only when `--fix` is set AND REPORT.md status is `success`

**Will Not:**

- Apply code changes without `--fix` AND explicit user confirmation
- Skip Tier 1 and jump straight to Tier 2 (even with `--depth deep`, Tier 1 still runs first and its output feeds Tier 2)
- Spawn Tier 2 hypothesis agents on consensus single-domain Tier 1 results
- Spawn more than 4 hypothesis agents in Tier 2 (token waste; signal already saturated)
- Trust agent-reported confidence without independent re-grading via `confidence-calibrator`
- Ship a REPORT.md whose `file:line` citations have not passed through `evidence-validator` (or its inline fallback)
- Auto-execute the Tier 3 task file — that is always a separate user-initiated `/task` invocation
- Auto-commit after Tier 3 — `/sc:reflect --type task --validate` is the final gate the user runs before committing
```

**Three Will bullets quoted verbatim**:

1. `Always run Tier 1 first (respect the "quick first option" contract)`
2. `Auto-escalate to Tier 2 only when the rubric in \`refs/escalation-rubric.md\` says so, or when \`--depth deep\` is set`
3. `Use auggie + serena every tier for in-repo grounding; use context7 + tavily only in Tier 2 and only when the symptom suggests external knowledge`

**Three Will Not bullets quoted verbatim**:

1. `Apply code changes without \`--fix\` AND explicit user confirmation`
2. `Skip Tier 1 and jump straight to Tier 2 (even with \`--depth deep\`, Tier 1 still runs first and its output feeds Tier 2)`
3. `Auto-execute the Tier 3 task file — that is always a separate user-initiated \`/task\` invocation`

**Style abstraction**:

- **Verb tense**: Imperative / present-tense, third-person elided. Will bullets start with an imperative verb (`Always run`, `Auto-escalate`, `Fan out`, `Use`, `Invoke`, `Run`, `Offer`). Will Not bullets start with the verb of the prohibited action (`Apply`, `Skip`, `Spawn`, `Trust`, `Ship`, `Auto-execute`, `Auto-commit`).
- **Em-dash vs hyphen**: Em-dash (`—`) is used for parenthetical qualifications and consequence/rationale clauses (e.g., `that wastes the debate`, `that is always a separate user-initiated /task invocation`). Hyphen is used in compound modifiers only (`user-initiated`, `self-grading`, `single-domain`). Parenthetical qualifiers commonly use round brackets instead of em-dashes (e.g., `(capped at 4 by signal mix)`).
- **Length budget**: Each bullet is a single line, generally ≤ 25 words including the trailing parenthetical. The longest line in the section (commands/troubleshoot.md:163) is `Invoke sc:adversarial-protocol only when Tier 2 produces 2-3 competing strong fixes (skip on consensus — that wastes the debate)` at ~24 words.
- **Conditional qualifiers** ("unless X" / "when Y" patterns): The existing Boundaries section already uses several conditional patterns the Wave 1.5 bullet can mirror:
  - `only when <condition>` — e.g., `Auto-escalate to Tier 2 only when the rubric...says so, or when --depth deep is set`, `Invoke sc:adversarial-protocol only when Tier 2 produces 2-3 competing strong fixes`, `Offer the Tier 3 remediation chain only when --fix is set AND REPORT.md status is success`.
  - `every tier ... only in Tier 2 and only when ...` — multi-condition layering on one bullet (commands/troubleshoot.md:162).
  - `without <condition>` (Will Not form) — e.g., `Apply code changes without --fix AND explicit user confirmation`, `Trust agent-reported confidence without independent re-grading via confidence-calibrator`, `Ship a REPORT.md whose file:line citations have not passed through evidence-validator (or its inline fallback)`.
  - The pattern `Always run documentation grounding ... unless --no-doc-discovery is set` for Wave 1.5 fits the existing `Always run Tier 1 first` precedent extended with the `unless <flag>` qualifier. There is no exact `unless --flag is set` precedent in the current Boundaries — the closest is the `or when --depth deep is set` clause (which is the inverse: condition that triggers, not condition that suppresses). The executor should consider adopting `unless <flag> is set` as the canonical suppression qualifier and may want to harmonize with the existing `only when` style by phrasing as `Always run documentation grounding in Wave 1.5 unless --no-doc-discovery is set` — single bullet, < 20 words, ends without parenthetical.

---

## Pattern 8: Output Contract field-row format

**Verbatim quote of full Output Contract table** (SKILL.md:41-55):

```markdown
| Field | Type | Description |
|-------|------|-------------|
| `status` | string | `success`, `partial` (some findings dropped for grounding), `failed` |
| `tier_reached` | int | 1, 2, or 3 |
| `report_path` | string | Absolute path to `REPORT.md` |
| `audit_log_path` | string | Absolute path to `audit.log` |
| `confidence` | float | 0.0-1.0, calibrated via `refs/escalation-rubric.md` |
| `escalation_reason` | string | If Tier 2 ran: which rubric condition triggered it (or `forced_by_depth_deep`) |
| `test_is_wrong` | bool | `true` when the diagnosis concludes the failing test is the bug (test asserts wrong behavior, stale invariant, or inverted policy claim) rather than the code under test. Set independent of tier. Asymmetric-cost flag — downstream automation MUST NOT auto-apply a fix to the code when this is `true`; the remediation target is the test file. |
| `test_file_path` | string \| null | When `test_is_wrong=true`, the **repo-relative** path of the test file that must be updated (e.g., `tests/api/test_foo.py`), resolved against the repo root containing `.git/`. `null` otherwise. The format is intentionally fixed to repo-relative so downstream automation can compare/join paths without ambiguity; if the report is consumed outside the repo, the consumer is responsible for joining against the repo root recorded in the audit log. |
| `hypothesis_cards` | list[path] | Paths to per-agent hypothesis cards (Tier 2) |
| `adversarial_artifacts_dir` | string | `sc:adversarial` artifacts dir (Tier 2 only, when 2+ fix proposals were debated) |
| `task_file_path` | string | MDTM task file path (Tier 3 only) |
| `remediation_offered` | bool | Whether Tier 3 was offered |
| `remediation_accepted` | bool | If offered, user's response |
```

**Two pre-existing-fields quoted verbatim for the format-template pair** (SKILL.md:49-50):

```markdown
| `test_is_wrong` | bool | `true` when the diagnosis concludes the failing test is the bug (test asserts wrong behavior, stale invariant, or inverted policy claim) rather than the code under test. Set independent of tier. Asymmetric-cost flag — downstream automation MUST NOT auto-apply a fix to the code when this is `true`; the remediation target is the test file. |
| `test_file_path` | string \| null | When `test_is_wrong=true`, the **repo-relative** path of the test file that must be updated (e.g., `tests/api/test_foo.py`), resolved against the repo root containing `.git/`. `null` otherwise. The format is intentionally fixed to repo-relative so downstream automation can compare/join paths without ambiguity; if the report is consumed outside the repo, the consumer is responsible for joining against the repo root recorded in the audit log. |
```

A simpler field-row for the minimal pattern (SKILL.md:52):

```markdown
| `adversarial_artifacts_dir` | string | `sc:adversarial` artifacts dir (Tier 2 only, when 2+ fix proposals were debated) |
```

**Format observations**:

- **Cell structure**: Exactly three columns — `Field | Type | Description`. Field is backticked snake_case. Type is unbacked, prose-typed (e.g., `string`, `int`, `float`, `bool`, `list[path]`).
- **Nullable typing**: Nullable fields are spelled `string \| null` (pipe-escaped because of table syntax). The `\|` is required because raw `|` would break the markdown table column.
- **Conditional-presence rules in-row**: Two distinct patterns:
  - Short form, parenthetical: `(Tier 2 only)`, `(Tier 3 only)`, `(Tier 2 only, when 2+ fix proposals were debated)` — appended to the description.
  - Long form, narrative: `When <condition>, <description>. <Fallback or default> otherwise.` — the pattern `test_file_path` uses: `When test_is_wrong=true, the repo-relative path ... null otherwise.`
- **Description style**: Sentence case, ends with a period when multi-sentence; first sentence is bare without trailing period when single-sentence. Backticks around literal values (`success`, `partial`, `true`, `null`, `forced_by_depth_deep`). Embedded examples use parenthesized `e.g.,` form: `(e.g., tests/api/test_foo.py)`.
- **Asymmetric-cost / safety flags**: Use the `MUST NOT` (all-caps RFC2119-style) phrasing — `downstream automation MUST NOT auto-apply a fix to the code when this is true` (SKILL.md:49). Wave 1.5's `behavior_is_documented` should consider whether it carries any asymmetric-cost semantics; if so, use the same `MUST NOT` phrasing.
- **The pattern Wave 1.5's `behavior_is_documented` and `doc_context_card_path` should follow**:
  - `behavior_is_documented` — type `bool`, no conditional presence (always set). Description should be a single declarative sentence: e.g., `` `true` when Wave 1.5 surfaced authoritative documentation (in-repo doc, ADR, or upstream library doc) for the symptom's domain. Used by Tier 2 to weight 'spec-says' evidence over 'code-says' evidence. ``
  - `doc_context_card_path` — type `string \| null`, conditional-presence via the long-form narrative pattern: `` When `behavior_is_documented=true`, the absolute path to the consolidated doc-context card synthesized by Wave 1.5 (e.g., `<output-dir>/wave1_5-doc-context.md`). `null` otherwise. ``
  - Both rows should be placed adjacent to each other in the table (mirroring the `test_is_wrong` + `test_file_path` adjacency at SKILL.md:49-50), with the boolean row first so the path row's `When <flag>=true` clause has its referent already in scope.

---

## Summary

- **Pattern 1 (Wave block template)**: Wave 1.5 mirrors Wave 3's structure exactly — `### Wave N: <tier-tag> — <title>` header, bold `**Goal**:` / `**Preconditions**:` / `**Steps**:` / `**Exit criteria**:` keys, numbered top-level steps with bold lead-ins + em-dash, `---` separator.
- **Pattern 2 (parallel fan-out)**: Wave 1.5 mirrors Wave 3's `Spawn ... in parallel via Task (single message with multiple Task calls)` phrasing, the templated `<output-dir>/<prefix>-<agent-name>-<artifact>.md` output convention, and the `Wait for all agents to complete. Read each card.` collection step. Synthesis mirrors Wave 3's step 4 "Distill ..." clustering style.
- **Pattern 3 (Refs loader)**: Wave 1.5 extends the existing Refs table at SKILL.md:377-383 with new rows in wave-number order, using `Wave 1.5 (<purpose>)` cell phrasing and `and` connectives for any multi-wave loaders.
- **Pattern 4 (Graceful Degradation / Error Handling)**: Wave 1.5 extends the existing Error Handling table at SKILL.md:348-362 with new `Scenario | Behavior | Fallback` rows (e.g., `auggie unavailable in Wave 1.5`, `docs not found in Wave 1.5`) using the same in-row tier/wave-tagged Scenario column and the recurring `note in audit` boilerplate.
- **Pattern 5 (MCP Integration)**: Wave 1.5 extends the **Auggie** bullet at commands/troubleshoot.md:85 to broaden the tier scope from `Tier 1 + Tier 2` to `Tier 1, Wave 1.5 (documentation grounding), and Tier 2`; the SKILL.md Tool Coordination Summary matrix's auggie row at SKILL.md:314 needs an annotation for the Wave 1.5 query class.
- **Pattern 6 (Options table)**: Wave 1.5's `--no-doc-discovery` row mirrors the `--no-escalate` / `--fix` row format exactly — backticked flag, backticked `` `false` `` default, two-sentence description with behavior + use-case rationale.
- **Pattern 7 (Boundaries Will / Will Not)**: Wave 1.5 extends the Will list with a single bullet using the existing `Always run X` precedent (commands/troubleshoot.md:159) + an `unless --no-doc-discovery is set` suppression qualifier that introduces a new — but harmonized — conditional pattern (the existing analogue is `or when --depth deep is set` which triggers; this triggers-by-default and suppresses on flag).
- **Pattern 8 (Output Contract field-row)**: Wave 1.5's `behavior_is_documented` (bool, always-set) and `doc_context_card_path` (string \| null, conditional-presence) mirror the `test_is_wrong` + `test_file_path` adjacent-pair pattern at SKILL.md:49-50, using the long-form `When <flag>=true, <path>. null otherwise.` narrative pattern for the path row.
