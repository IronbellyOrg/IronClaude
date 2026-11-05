# Command nuance: /sc:research

**Generated**: 2026-10-27 by the sc-research nuance agent (read-only; only this file written). Brief: `_brief.md` (same folder).
**Path shorthand** (all under `/home/coder/.claude/` unless noted): CMD = `commands/sc/research.md`; CFG = `RESEARCH_CONFIG.md`; AGT = `agents/deep-research-agent.md`; HWW = `HOW-WE-WORK.md`; TR = `skills/tech-research/SKILL.md`; BS = `skills/sc-brainstorm-protocol/SKILL.md`; HR = `skills/sc-brainstorm-protocol/refs/handoff-routing.md`.
**Marking**: `(J)` = my judgment, no file states it. UNVERIFIED = not confirmed from a file.

## 1. Status and role

- **Does**: "Deep web research with adaptive planning and intelligent search" (CMD:3); writes a report only, no implementation (CMD:124-142). Standalone-invokable, NOT retired; CMD never mentions `/sc:task` or `/sc:tasklist` (grep: none). Serves the Spec phase as a side input for OUTSIDE knowledge (library, standard, best practice): routing row `external-research` (HWW:312), HWW 3.5 (HWW:143). It is also called automatically by `/sc:brainstorm` as "research light" (BS:185).
- **Backing protocol skill `~/.claude/skills/sc-research-protocol/` DOES NOT EXIST** (`ls` failed; `find` under `~/.claude` finds no `*research-protocol*`). CMD names no skill; it runs from its own file plus the `deep-research-agent` persona (CMD:7), AGT and CFG (CMD:93,97). HWW:232 allows a command with no skill, but BS:185 and HR:49,76 tell brainstorm to call `Skill sc-research-protocol` / `Skill sc:research-protocol`, which cannot load; HR:55 supplies a WebSearch fallback.
- **Overlaps**: `/tech-research` (our code, has its own web phase), `bmad-technical-research` (BMad lane; requires web search, `.claude/skills/bmad-technical-research/SKILL.md:8,21`), `bmad-domain-research` / `bmad-market-research` (content UNVERIFIED), and the `feasibility-probe` swarm lens that points at this command (`skills/sc-swarm-wizard-protocol/refs/cli-contract.md:47`).

## 2. Flags

CMD has exactly two flags plus one positional argument (CMD:25; grep of `--` in CMD finds only `--depth` and `--strategy`). AGT and CFG define no further user-facing flags.

| Flag / arg | Values | Default | What it changes (cited) | Worth using when | Avoid when |
|---|---|---|---|---|---|
| `"[query]"` (positional) | free text | none; behaviour when missing is UNVERIFIED | Becomes the research question (CMD:25). Step 1 scores "query complexity and ambiguity" (CMD:32), and step 3 scales the task list "to query complexity (3-15 tasks)" (CMD:46) | Always. Put question, why, and constraints in it (HWW:30-35, four-part request rule) | The question is about our own code: use `/tech-research` (HWW:247) |
| `--depth` | `quick`, `standard`, `deep`, `exhaustive` (CMD:25) | **Not stated in CMD or CFG.** CFG has no depth default (CFG:5-13); `max_hops: 5` (CFG:8) equals exhaustive's hop count but is not labelled a depth. UNVERIFIED | Hops: quick 1, standard 2-3, deep 3-4, exhaustive 5 (CMD:86-91). Profiles (CFG:66-71): quick = 10 sources, 1 hop, 2 min, confidence 0.6, `basic` search, search only; standard = 20, 3 hops, 5 min, 0.7, basic, search+extract; deep = 40, 4 hops, 8 min, 0.8, **advanced** search+extract, adds `tavily-map`; exhaustive = 50+, 5 hops, 10 min, 0.9, advanced, adds `tavily-crawl`. Caps: maps=2, crawls=1, crawl result max 50 URLs (CFG:77-78). Global ceiling 10 min / 10 iterations / 5 hops (CFG:35) | `deep`: the guide sets `--depth deep` as the mandatory flag on `external-research` (HWW:312, example HWW:143); `/sc:recommend` emits it too (`skills/sc-recommend/SKILL.md:255`). `quick`: one-fact lookup; brainstorm uses it (BS:185) | `exhaustive` for a fact one official page answers (spends the full 10 min, CFG:71). Omitting the flag in routine use: the bare default is undocumented |
| `--strategy` | `planning`, `intent`, `unified` (CMD:25) | `unified` (CFG:6). Mapping of flag names to config keys `planning_only` / `intent_planning` / `unified` (CFG:18-20) is by inference: UNVERIFIED | `planning`: no clarification, executes immediately. `intent`: asks up to 3 clarifying questions, then executes. `unified`: optional clarification, **presents the plan and executes only after user confirmation** (CFG:17-20; AGT:38-56). Selection indicators (CFG:39-43): clear, well-scoped query -> planning; ambiguous or broad -> intent; complex multi-faceted or high-stakes -> unified | `planning` for a clear narrow question, and in any unattended run. `unified` for high-stakes or multi-faceted topics (CMD:114 example) | `unified` when no human is watching: it waits for confirmation (CFG:20). `intent` when the question is already precise |

**Does not exist** (grep of CMD, AGT, CFG): `--output`, `--format`, `--sources`, `--hops`, `--handoff`, `--fix`, any QA-intensity flag. Output formats `summary` / `report` / `academic` are a CFG concept (CFG:125-129) with no flag in CMD. The report path is fixed: `claudedocs/research_[topic]_[timestamp].md` (CMD:104,135). `--research light|deep` belongs to `/sc:brainstorm`, not here (BS:185-186). The depth tiers and QA-intensity override at TR:99-121 belong to `/tech-research`, a different command.

## 3. Scope x complexity matrix

**Complexity here means how hard the OUTSIDE question is, not how big the code change is.** The command does vary by complexity: through `--depth` and `--strategy`. No file gives a numeric threshold (TCS at `skills/task-builder/SKILL.md:2410-2441` scores task files, not research queries), so the bands below are JUDGMENT, built from the signals CFG already uses for strategy (CFG:39-43) and the profile table (CFG:66-71).

| Band | Definition (signals) | Flags (J) |
|---|---|---|
| LOW | One factual question, one authoritative source likely; "clear query, technical docs, well-defined scope" (CFG:41) | `--depth quick --strategy planning` |
| MEDIUM | One topic, several facets or two or three options to compare; answer needs cross-checking sources | `--depth standard`, or `deep` to follow the guide (HWW:312); `--strategy planning` |
| HIGH | Multi-faceted, ambiguous, or high-stakes decision resting on outside facts (CFG:43); the answer could change the design | `--depth deep --strategy unified` (`exhaustive` only for a whole-domain survey) |

Scope here is the size of the work the research serves. No file rates `/sc:research` REQUIRED anywhere: the guide's `external-research` row is an intent route (`changes_files: no`, HWW:312), not a mandatory step.

| Scope | LOW | MEDIUM | HIGH |
|---|---|---|---|
| T one-off | SKIP (J) | SKIP (J) | OPTIONAL (J) `--depth standard`; a one-off rarely needs more than a doc lookup |
| B bug fix | SKIP (J) | SKIP (J) | OPTIONAL (J) `--depth standard`, only after `/sc:troubleshoot` points at third-party behaviour |
| S single story | SKIP (J) | OPTIONAL (J) `--depth standard` | OPTIONAL (J) `--depth deep` |
| F multi-story feature | SKIP (J) | OPTIONAL (J) `--depth standard` | WORTH IT (J) `--depth deep --strategy unified` |
| R multi-feature release (new definition) | SKIP (J) | OPTIONAL (J) `--depth standard` | WORTH IT (J) `--depth deep`; e.g. a dependency or standard that several features share |
| N new product | OPTIONAL (J) `--depth quick` | WORTH IT (J) `--depth standard` or `deep` | WORTH IT (J) `--depth deep --strategy unified` |

Every cell is `(J)`: no file ties this command to a scope or a complexity band. N MEDIUM/HIGH keep the existing WORTH IT rating in `command-value-by-phase.md` (Section 2.1, `/sc:research` row).

## 4. Choose this or the neighbour

| Neighbour | Decision rule (by signal) | Cited |
|---|---|---|
| `/tech-research` | **Where the answer lives.** Question names our code, or "how does our system work / what would need to change / is it feasible" -> `/tech-research`. Question is a library, standard, or best practice outside our code -> `/sc:research`. Never use `/tech-research` for a pure web question (`sc-recommend/SKILL.md:255` says so) | HWW:247, HWW:143, HWW:308 |
| `/tech-research` (mixed question) | If the work needs both (our code plus an outside library), `/tech-research` already runs a web phase: 0-1 web agents at Quick, 1-2 at Standard, 2-4 at Deep (TR:99-103; web phase TR:388). Run `/sc:research` first only when the outside answer decides whether the code investigation is worth doing | TR:99-103, TR:388 |
| `/tech-research` (cost) | `/tech-research` runs at its deepest setting by default with many agents (HWW:255) and at least 11 agents at the final gate (TR:27). `/sc:research` stops at one report with a 10 min ceiling (CFG:35). For a question that only needs outside facts, `/sc:research` is the cheap path | HWW:255, TR:27, CFG:35 |
| `/tech-research` (what follows) | `/tech-research` feeds `/task-builder` (HWW:19, HWW:308). `/sc:research` has no routed next step in the guide. Its own file says "use `/sc:design` ... or `/sc:implement`" (CMD:142), which skips the tasklist step and disagrees with HWW:308 (report -> `/task-builder`). Treat the CMD line as stale (J) | CMD:142, HWW:308 |
| `bmad-technical-research` | **Lane.** In the BMad lane use `bmad-technical-research`; it also requires web search (SKILL.md:21) and writes `{planning_artifacts}/research/technical-<slug>-research-<date>.md` (SKILL.md:91). This resolves `command-value-by-phase.md` U8 for the web/code question: web. Inside one lane, run one of the two, not both | `.claude/skills/bmad-technical-research/SKILL.md:8,21,91` |
| `/sc:brainstorm --research light` | Not an engineer decision. Brainstorm calls `/sc:research --depth quick` itself for framework/library topics not in the project (BS:185); `--research deep` routes to `/tech-research`, with `sc-research-protocol --depth deep` only as fallback (BS:186, HR:70-76). Do not run `/sc:research` again for the same topic | BS:185-186, HR:49,70-76 |
| Plain library lookup (context7 / `WebSearch`) | For one API signature or flag, CFG routes tech docs to context7 (CFG:116) and "native" for simple explanations (CFG:117). `/sc:research --depth quick` is a heavier way to get the same answer (J) | CFG:112-117 |
| `/sc:swarm-wizard` | Different job (review by other model families). `feasibility-probe` lens names `/sc:research` as the human-run precursor (cli-contract.md:47), not a replacement | `skills/sc-swarm-wizard-protocol/refs/cli-contract.md:47` |

Retired commands: none of the above route through `/sc:task` or `/sc:tasklist`.

## 5. What a scheduled checker can see

| Footprint | Path / key | Source | Status |
|---|---|---|---|
| Report | `claudedocs/research_[topic]_[timestamp].md` in the repo working tree | CMD:104,135 | File exists only if the engineer commits it. `claudedocs/` is tracked and not gitignored here (`git ls-files claudedocs` lists files; `git check-ignore` prints nothing). One matching file exists: `claudedocs/research_orca_headless_v1.4.162_20260801.md` (date-only suffix, no time; it is a hypothesis validation, added by commit `f70b38d3`). Whether `/sc:research` produced it is UNVERIFIED |
| Report content | executive summary, confidence levels, source list | CMD:105-107 | Does NOT record the `--depth` or `--strategy` used (no such field in CMD:102-107). So depth cannot be checked from disk |
| Session persistence | Serena memory ("research session persistence") | CMD:100, CFG:25 | Location and name UNVERIFIED |
| Via brainstorm | `enrichment/research-light.md` in the brainstorm run folder | BS:185 | Parent path UNVERIFIED. If the protocol skill fails to load the tier falls to WebSearch (HR:55) and the file may hold a condensed result instead |
| BMad twin | `_bmad-output/planning-artifacts/research/technical-*-research-*.md` | `bmad-technical-research/SKILL.md:91` | `{planning_artifacts}` resolution not checked: UNVERIFIED |

Otherwise "none, transcript only". The work leaves no frontmatter keys and no ledger lines. An engineer who runs it and does not commit `claudedocs/` leaves no trace in the repo.

## 6. Expected-step rule

- **Never count `/sc:research` as an expected step at any scope or complexity.** It is OPTIONAL or WORTH IT at most (Section 3), no pipeline lists it, and the guide's own routing row makes it an answer-only route (HWW:312, `changes_files: no`). Its absence is always fine, including for N.
- **Presence is also fine at any scope.** At most, a checker may treat "N or F HIGH, spec cites an outside standard or library, and no research artifact of any kind (`/sc:research` report, `/tech-research` report with a web phase, or `bmad-technical-research` file)" as an advisory note (J), never a skipped step. Do not flag a short path that omits it, and do not flag a different depth than `deep`: depth is a flag and leaves no footprint (Section 5).

## 7. Proposed changes to command-value-by-phase.md

Proposals only; that file is not edited.

| Where | Current text | Proposed text | Why |
|---|---|---|---|
| Section 2.1, `/sc:research` row, R cell | `SKIP` | `OPTIONAL` | Re-rated under the new R definition (multi-feature release plan). The old SKIP read R as "assembles already-built work". A multi-feature release plan can hinge on an outside standard or shared dependency. Only cell that changes under the new R definition. (J) |
| Same row, T/B/S/F/N cells | `SKIP / SKIP / OPTIONAL / OPTIONAL / WORTH IT` | unchanged | Matrix above agrees as a summary; F and R become WORTH IT only at HIGH complexity (J) |
| Same row, Notes | `Outside knowledge only (library, standard). /tech-research is for our code` | `Outside knowledge only (library, standard). /tech-research is for our code. Depth by question difficulty: quick (one fact), standard (several facets), deep (high-stakes or ambiguous; the guide's mandatory flag for external-research, HWW:312). Use --strategy planning when unattended; the default unified waits for confirmation. Never REQUIRED. Backing skill sc-research-protocol does not exist; the command runs from its own file` | Adds the complexity layer and the flags that matter |
| Section 3, O10 row, Why | `Guide section 5. The three BMad research skills are product/market framing; whether bmad-technical-research reads code or web is UNVERIFIED` | `Guide section 5. bmad-technical-research needs web search (SKILL.md:21), so it is the BMad twin of /sc:research, not of /tech-research. Pick by lane` | Resolves U8 |
| Section 4 "What a checker could observe" table | no `/sc:research` row | Add `/sc:research` -> `claudedocs/research_<topic>_<timestamp>.md` (only if committed; no depth recorded) -> CMD:104 | New footprint |
| Section 5, U8 | open | Mark resolved for the web/code question (web); `bmad-domain-research` and `bmad-market-research` still unread | See above |

## 8. Unverified items

| # | Item | Resolve by |
|---|---|---|
| 1 | Default `--depth` when the flag is omitted (not in CMD, AGT, or CFG) | Run once, or find the engine source in the SuperClaude install |
| 2 | Mapping of `--strategy planning` / `intent` to config keys `planning_only` / `intent_planning` (CFG:18-19) | Same |
| 3 | Behaviour with a missing query | Same |
| 4 | Whether `claudedocs/research_orca_headless_v1.4.162_20260801.md` came from `/sc:research` | Check commit `f70b38d3` message and session history |
| 5 | Serena memory name/location for research session persistence (CMD:100) | Read the engine or run once |
| 6 | Parent path of `enrichment/research-light.md` under a brainstorm run (BS:185) | Read `sc-brainstorm-protocol` state/layout refs |
| 7 | `{planning_artifacts}` path for `bmad-technical-research` output | Read `_bmad/` config |
| 8 | Whether `bmad-domain-research` / `bmad-market-research` use the web | Read their SKILL.md |
| 9 | Whether Tavily MCP is configured on every engineer's machine; without it the agent falls back to WebSearch/WebFetch and records `fallback_reason` (AGT:125-139). Not checked (no env values read) | Check for the tool, not any key |
| 10 | Whether `sc-research-protocol` is expected to ship in a later IronClaude release (three files call it: BS:185, HR:49, HR:76) | Ask the IronClaude maintainers / check the source repo |
| 11 | Whether a bare run really waits for plan confirmation (CFG:20 says `unified` does; the default is `unified` per CFG:6) | Run once |

Note: HWW:3 says `superclaude update` re-copies shipped files, so another engineer's `~/.claude` may differ from the one read here (same caveat as U17 in the main file).
