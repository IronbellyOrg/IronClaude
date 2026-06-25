# Research: Citation Cross-Validation + --spec §22

**Status:** Complete
**Date:** 2026-06-19
**Researcher:** R07 (Doc Cross-Validator)
**Scope:** Citation verification + `--spec §22` input-contract settlement + stale-token absence confirmation

> **Source-of-truth note:** All verification done against `src/superclaude/` (the canonical source per CLAUDE.md SoT discipline; `.claude/` is sync-dev output). Line numbers below are CURRENT `src/superclaude/...` line numbers as of 2026-06-19. The driving spec/TDD cite line numbers that (per task framing) reflect intended/historical state — where the spec/TDD anchor differs from current source it is flagged DRIFT.

---

## 1. Citation Cross-Validation Table

Tag legend: **[CODE-VERIFIED]** = contract/text confirmed at the cited anchor in current source. **[CODE-VERIFIED+DRIFT]** = content present and correct, but the exact line numbers moved vs. the doc anchor (builder must use current anchors). **[CODE-CONTRADICTED]** = current code shows something materially different. **[UNVERIFIED]** = could not locate.

### 1a. task-builder/SKILL.md

| Citation (doc anchor) | Doc source claim | Current-source state | Tag |
|---|---|---|---|
| `task-builder/SKILL.md:873-911` (synthetic-dnsp / DM-003 contract) | DNSP Synthetic Finding Protocol + emitter contract present | **PRESENT at 873-911.** `873` = heading "**DNSP Synthetic Finding Protocol (PR-03 ...)**"; emitter contract fields (`severity: HIGH`, `source: "synthetic-dnsp"`, `affected_range`, `evidence`, `recommendation`, `dedup_key`, `found_n_times`) at 877-883; fixed-field rejection R-113/R-114 at 885; dynamic-field R-115/R-116 at 887; R-117/R-118/R-119 at 889; API-003-M6 wire-shape R-120/R-121 at 891; A.8 merge step R-127 at 911. | **[CODE-VERIFIED]** |
| `task-builder/SKILL.md:1066` (Execution Context section) | `EXECUTION_CONTEXT_INSTRUCTION` block | **PRESENT at 1066-1071.** `1066` = "EXECUTION_CONTEXT_INSTRUCTION: The builder MUST populate the `## Execution Context` section...". | **[CODE-VERIFIED]** |
| `task-builder/SKILL.md:1231` (TB-Add-7 / Execution Context populate step) | STEP 5a populates `## Execution Context` | **PRESENT at 1231.** `1231` = "5a. Populate the `## Execution Context` section from the template with References / Source areas / Key constraints...". | **[CODE-VERIFIED]** |
| `task-builder/SKILL.md:1290-1305` (PR-02 regression/monotonicity) | F-set / 4-step ordering rule + regression non-emission | **PRESENT at 1285-1305.** `1285` = "**F-set definition (item identity = dedup-key...)**"; synthetic-dnsp dedup-key at 1290; `\|F_n\|` cardinality at 1292; 4-step ordering rule heading at 1294; regression check (step 1) at 1298; monotonicity check (step 2) at 1299 (`[HALT-MONOTONICITY] \|F\|=<n>`); hard-cap at 1300; strict-ordering invariant at 1303; regression non-emission invariant at 1305. | **[CODE-VERIFIED]** |

### 1b. sc-tasklist-protocol/SKILL.md

| Citation (doc anchor) | Doc source claim | Current-source state | Tag |
|---|---|---|---|
| `:1132-1194` (20-check pre-write gate) | pre-write self-check gate | **PRESENT at 1132-1187.** `1132` = "## Sprint Compatibility Self-Check (Pre-Write, Mandatory)"; checks 1-8 at 1138-1145; Semantic gate (checks 9-12) at 1147-1156; Structural gate (checks 13-20) table at 1174-1185; gate close "If any check 1-20 fails..." at 1187. The gate **ends at 1187**, not 1194 — 1189-1198 are "Final Output Constraint" + write-atomicity prose. Builder anchor for gate body = **1132-1187**. | **[CODE-VERIFIED+DRIFT]** (end anchor 1194→1187) |
| `:1187` (check 1-20) | "all 17/20 checks" wording | **CONFIRMED 20 at 1187:** "If any check **1-20** fails, fix it before writing any output file." The gate genuinely defines 20 numbered checks (1-8, 9-12, 13-20). | **[CODE-VERIFIED]** |
| `:1597` ("all 17 checks passed" — stray 17-vs-20) | stale "17" should be "20" | **CONFIRMED STALE at 1597:** Stage-6 completion message literally reads `- Stage 6: "Self-Check: all **17** checks passed"`. This **contradicts** the gate's own "check 1-20" at 1187. Confirmed by grep: only two count tokens exist — `1187: check 1-20` and `1597: all 17 checks`. This is a real internal inconsistency the builder should fix (17→20) as a P-class hygiene item. | **[CODE-CONTRADICTED]** (1597 says 17; authoritative gate says 20) |
| `:1460-1481` (Stage 10.5 Pre-Reflect Sign-off) | Stage 10.5 fan-out | **PRESENT at 1460-1481.** `1460` = "### Stage 10.5: Pre-Reflect Sign-off"; reuse-Stage-7-primitive (N not 2N) at 1464; spec-resolution + invoke block at 1466-1475; per-phase verdict handling at 1477; skip-when-disabled at 1479; stage gate at 1481. | **[CODE-VERIFIED]** |
| `:1409-1427` (Stage 9 sc:task) | Stage 9 delegates patch exec to sc:task | **PRESENT at 1409-1427.** `1409` = "### Stage 9: Patch Execution (Delegate to `sc:task`)"; Skill-tool invoke + `--compliance strict` at 1413-1416; "orchestrator does NOT apply patches itself" at 1425; stage gate at 1427. | **[CODE-VERIFIED]** |
| `:1525-1558` (stage reporting) | Stage Completion Reporting Contract | **PRESENT at 1525-1558.** `1525` = "## Stage Completion Reporting Contract"; "executes in 11 stages" at 1527; stage table 1-10.5 at 1529-1541; Gate Behavior at 1543; dependency chain at 1551-1557. | **[CODE-VERIFIED]** |
| `:130-132` (sc:task) | doc tags this as "sc:task" | **CONTRADICTED — content is NOT sc:task.** `130` = "### 3.x Source Document Enrichment"; `132` = the **Scope note** distinguishing skill-protocol enrichment (`build_tasklist_generate_prompt`) from the CLI `validate` subcommand (`build_tasklist_fidelity_prompt`). The actual `/sc:task` integration anchors are: frontmatter `description` (line 3), overview line 16, tier algorithm ref at 546, Stage 9 at 1409-1418. **Builder: do not treat 130-132 as an sc:task anchor.** | **[CODE-CONTRADICTED]** (130-132 = Source Document Enrichment scope note, not sc:task) |
| `:546-646` (tier scoring) | Compliance Tier Classification | **PRESENT at 544-648.** `544` = "### 5.3 Compliance Tier Classification (mandatory, deterministic)"; priority order at 548; compound overrides 5.3.1 at 550-566; keyword matching 5.3.2 at 568-594; context boosters 5.3.3 at 596-614; confidence scoring 5.4 at 616-629; MCP tool reqs 5.5 at 631-640; sub-agent delegation 5.6 at 642-648. Heading starts at **544**, one line above the doc's `546`. | **[CODE-VERIFIED+DRIFT]** (start 546→544; body fully present) |

### 1c. sc-tasklist-protocol/SKILL.md — `--spec` enrichment sites

| Citation (doc anchor) | Doc source claim | Current-source state | Tag |
|---|---|---|---|
| `:169-182` (4.1a Supplementary TDD Context) | conditional on `--spec` flag | **PRESENT at 169-183.** `169` = "### 4.1a Supplementary TDD Context (conditional on --spec flag)"; "If `--spec <spec-path>` was provided:" at 171; TDD-format detection at 174; `supplementary_context` keys (component_inventory, migration_phases, testing_strategy, observability, release_criteria, api_surface) at 175-181; non-TDD warning at 182; missing-file abort at 183. | **[CODE-VERIFIED]** |
| `:246-271` (4.4a Supplementary Task Gen) | conditional on `--spec` flag | **PRESENT at 246-267** (4.4a). `246` = "### 4.4a Supplementary Task Generation (conditional on --spec flag)"; task-pattern table at 250-259; generation-time enrichment at 261-267. NOTE: **4.4b PRD** begins at 269 — the doc anchor `271` lands in the *4.4b PRD* block, not 4.4a. 4.4a body = **246-267**. | **[CODE-VERIFIED+DRIFT]** (end anchor 271→267; 269+ is 4.4b PRD) |
| `:1297-1308` (Stage-7 Supplementary TDD Validation) | conditional on `--spec` flag | **PRESENT at 1297-1308.** `1297` = "**Supplementary TDD Validation (conditional on --spec flag):**"; "When `--spec` was provided and supplementary_context was loaded in Step 4.1a..." at 1299; check table at 1301-1306; "merged into the same consolidated findings list...unchanged for invocations without `--spec`" at 1308. | **[CODE-VERIFIED]** |
| `:1466-1471` (Stage 10.5 PRE reflect spec threading) | `--spec` threaded into pre-reflect | **PRESENT at 1466-1471.** `1466` = "**Resolve depth/tier deterministically + spec.**" with resolution order "explicit `--spec` → auto-wired TDD/PRD from `.roadmap-state.json` → the roadmap itself, always present"; `--spec <RESOLVED_SPEC_PATH>` in the invoke block at 1471. | **[CODE-VERIFIED]** |
| `:49-57` ("exactly one input: roadmap text...only source of truth") | input contract | **PRESENT at 47-57.** `47` = "## Input Contract"; `49` = "You receive exactly one input: **the roadmap text**."; `57` = "Treat the roadmap as the **only source of truth**." | **[CODE-VERIFIED]** — but see §2: this CONTRADICTS the four `--spec` sites above. |

### 1d. cli/sprint/config.py (Sprint conventions)

| Citation (doc anchor) | Doc source claim | Current-source state | Tag |
|---|---|---|---|
| `config.py:15-32` | Canonical phase filename conventions | **PRESENT at 15-32.** `15-19` = convention comments (`phase-1-tasklist.md`, `p1-tasklist.md`, `phase_1_tasklist.md`, `tasklist-p1.md`); `PHASE_FILE_PATTERN` regex 20-32 — NOTE current pattern ALSO matches v4.3.0 rerun bundle `phase-Nr-tasklist.md` (27, comment 22-26), an addition beyond the 4 documented names. | **[CODE-VERIFIED]** (+1 undocumented rerun-bundle variant at 27) |
| `config.py:34-55` | task-id heading regex + count_tasks_in_file | **PRESENT at 34-55.** `_TASK_ID_HEADING_RE = ^###\s+T\d{2}\.\d{2}\b` at 37-40; `count_tasks_in_file()` at 43-55 (returns 0 on missing/unreadable). | **[CODE-VERIFIED]** |
| `config.py:73-124` | execution-mode column / index parsing | **PRESENT at 73-124** inside `discover_phases()`. Exec-mode-by-file map at 76; pipe-table row regex at 77-80; header detection ("file" col) at 84-93; allowed modes `{claude, python, skip}` at 116; unknown-mode ClickException at 118-121; default "claude" at 124. | **[CODE-VERIFIED]** |
| `config.py:134-146` | directory-scan fallback (Strategy 2) | **PRESENT at 134-146.** `134` = "# Strategy 2: scan directory if nothing found"; iterates `index_dir.iterdir()` 136-144; dedup by phase number; returns sorted list at 146. | **[CODE-VERIFIED]** |

---

## 2. SETTLEMENT — `--spec §22` input-contract risk (TDD §22 / spec §5.1 §11 "Autowire-vs-roadmap-only")

### 2a. The contradiction, characterized precisely (verbatim)

There is a **genuine internal contradiction** in `sc-tasklist-protocol/SKILL.md` between the Input Contract and the four `--spec`/source-document enrichment sites.

**Side A — "roadmap is the ONLY input" (Input Contract, lines 47-57, verbatim):**

> Line 47: `## Input Contract`
> Line 49: `You receive exactly one input: **the roadmap text**.`
> Line 57: `Treat the roadmap as the **only source of truth**.`

**Side B — `--spec` / source-document enrichment is a first-class supported input (verbatim):**

> Line 9 (frontmatter `argument-hint`): `argument-hint: "<roadmap-path> [--spec <spec-path>] [--output <output-dir>] [--no-reflect]"`
> Line 134 (§3.x): `When the tasklist generator has access to TDD and/or PRD source documents (via auto-wired paths from `.roadmap-state.json` or explicit `--tdd-file`/`--prd-file` flags), it MUST read them and use their structured content...`
> Line 169: `### 4.1a Supplementary TDD Context (conditional on --spec flag)`
> Line 171: `If `--spec <spec-path>` was provided:`
> Line 246: `### 4.4a Supplementary Task Generation (conditional on --spec flag)`
> Line 1297: `**Supplementary TDD Validation (conditional on --spec flag):**`
> Line 1466: `Resolve `<RESOLVED_SPEC_PATH>` per the spec resolution order (explicit `--spec` → auto-wired TDD/PRD from `.roadmap-state.json` → the roadmap itself, always present).`

**Nature of the contradiction:** Line 49's "**exactly one input**" and line 57's "**only source of truth**" are literally false against the *current implemented behavior* of the skill, which (a) advertises `--spec` in its own `argument-hint` (line 9), (b) auto-wires TDD/PRD from `.roadmap-state.json` (lines 134, 1466), and (c) has four behavioral sections that read and act on those supplementary inputs. The §3.x scope note (line 132) already acknowledges enrichment is a real skill-protocol behavior. So the Input Contract prose is **stale** relative to the rest of the file — it was not updated when `--spec`/source-enrichment was added. **The behavior already supports `--spec`; only the contract prose lags.**

### 2b. Recommended SMALLEST behavior-preserving reconciliation (doc-consistency edit, NOT a behavior change)

Reconcile by **amending lines 49-57 to acknowledge `--spec`/source documents as OPTIONAL SUPPLEMENTARY inputs while preserving the roadmap's primacy as the sole task-*generation* source of truth.** This is a documentation-consistency edit — it changes no algorithm step, no flag, no emitter, no gate. It makes the already-true behavior self-consistent.

**Exact verbatim current text to change (lines 49-57):**

```
You receive exactly one input: **the roadmap text**.

The roadmap may contain:

- Phases, milestones, versions, epics, bullets, paragraphs
- Requirements, features, risks, success metrics, constraints
- Vague items ("improve performance", "harden security")

Treat the roadmap as the **only source of truth**.
```

**Exact verbatim proposed replacement (behavior-preserving):**

```
You receive one **required** input — **the roadmap text** — and may receive
**optional supplementary inputs** (`--spec <spec-path>`, or auto-wired
TDD/PRD paths from `.roadmap-state.json`; see §3.x Source Document
Enrichment and §4.1a/§4.4a).

The roadmap may contain:

- Phases, milestones, versions, epics, bullets, paragraphs
- Requirements, features, risks, success metrics, constraints
- Vague items ("improve performance", "harden security")

Treat the roadmap as the **primary source of truth** for task generation:
every task MUST trace to a roadmap item (R-### traceability). Supplementary
TDD/PRD inputs, when present, only **enrich** roadmap-derived tasks
(specificity, acceptance criteria, validation, deployment phases) and the
pre-reflect spec resolution (§10.5) — they never originate tasks that lack
a roadmap anchor. Without supplementary inputs, the generator works from
the roadmap alone (the baseline behavior described in §3.x).
```

**Surrounding context for the builder** (so the Edit is unambiguous): the block sits between `## Input Contract` (line 47) and the `---` separator at line 59, immediately preceding `## Artifact Paths (Deterministic, Explicit)` at line 61. The replacement keeps the bullet list verbatim and only rewrites the opening sentence (49) and the closing "only source of truth" sentence (57). It is consistent with the already-present §4.4b guarantee (line 271: "engineering tasks come from the roadmap; PRD enriches them") and §3.x line 136 ("Without source documents: The generator works from the roadmap alone (current baseline behavior)").

### 2c. Residual genuine ambiguity → MUST remain an Open Question (do NOT auto-apply)

The reconciliation in §2b assumes the maintainer's intent is **"keep `--spec` enrichment; fix the stale contract prose."** There is a second, materially different possibility the builder cannot resolve from the source alone:

> **OPEN QUESTION (human decision required):** Does the maintainer instead want to **REMOVE `--spec`/source-document enrichment** to make the generator *truly* roadmap-only (honoring lines 49/57 as the intended contract)? That is a **behavior change** — it would delete §3.x (130-147), §4.1a (169-183), §4.1b (185+), §4.4a (246-267), §4.4b (269+), the Stage-7 Supplementary TDD Validation (1297-1308), the `--spec` thread in Stage 10.5 (1466-1471), and the `--spec`/`--tdd-file`/`--prd-file` flags from `argument-hint` (line 9) and the CLI. This is **out of P1-P5 scope** and **MUST NOT be auto-applied.**

Per `feedback_human_decision_items_must_halt`: the builder should encode §2b as a bounded P-class doc-consistency item (low risk, behavior-preserving) AND encode §2c as a `needs_human_decision` Open Question that HALTs rather than auto-defaulting to either direction. The recommended default *for the bounded item* is §2b (acknowledge `--spec` as optional supplementary) because it makes the file self-consistent with zero behavior change; the removal path stays an explicit human gate.

---

## 3. Stale-Token Absence Confirmation (operative targets)

Grep over `src/superclaude/` (and the two SKILL.md files specifically). "Operative target" = does the token appear as a live target the tasklist generator acts on?

| Token | grep result | Operative in tasklist generator? | Notes |
|---|---|---|---|
| `sc:task-unified` | **0 hits** anywhere in `src/superclaude/` | **ABSENT** | Fully retired. The unified-task surface is now `sc:task` (e.g., sc-tasklist `:1409`, `:1413`, `:546`). Builder must reference `sc:task`, never `sc:task-unified`. |
| `/rf:` | **0 hits** in sc-tasklist-protocol/SKILL.md; **1 hit** in task-builder/SKILL.md:875 (`/rf:opinion` inside the DNSP escalation-ladder description) | **NOT an operative tasklist target** | The single hit is a reference to the rf-agent escalation ladder (`WebSearch -> /rf:opinion -> team-lead`) inside the DM-003 contract narrative — descriptive, not a command the tasklist generator invokes. No `/rf:` command surface exists in the generator. |
| `.gfdoc` | **0 hits** in either SKILL.md; **multiple hits** in `src/superclaude/agents/rf-*.md` and `src/superclaude/templates/workflow/*.md` (e.g., rf-team-lead.md:369, rf-task-executor.md:152/163, 01/02 mdtm templates :87/:91, changelog_template.md:41/45) | **NOT an operative tasklist target** | `.gfdoc` lives only in the legacy RF agent/template ecosystem (automated_qa_workflow.sh paths, workflow-doc discovery). It is NOT referenced by the tasklist generator or task-builder SKILL bodies. Builder: do not introduce `.gfdoc` paths into tasklist output; the generator writes under `TASKLIST_ROOT/`. |
| `llm-workflows` | **0 hits** anywhere in `src/superclaude/` | **ABSENT** | Fully absent. No stale reference. |
| typed `StageError` | **0 hits** anywhere in `src/superclaude/` | **ABSENT** | No typed `StageError` class/exception in current code. Stage gating in sc-tasklist-protocol is prose-level ("Stage gate:" lines) + (in CLI) `click.ClickException` (e.g., config.py:118). If the spec/TDD assumes a typed `StageError`, that is an **[UNVERIFIED]/non-existent** construct — the builder should not author tasks that import/raise a `StageError` symbol. |

**Summary of §3:** `sc:task-unified`, `llm-workflows`, and `StageError` are genuinely ABSENT (safe to treat as fully-retired / never-existed). `/rf:` and `.gfdoc` DO exist in current source but ONLY in the RF-agent/template legacy ecosystem — they are **not operative targets in the tasklist generator or task-builder SKILL bodies**, so the builder must not wire them into tasklist-generator changes.

---

## 4. DRIFT Summary for the Builder (use CURRENT anchors)

The following doc anchors **moved** vs. current `src/superclaude/` source. Builder must anchor edits to the current line numbers, not the doc's:

| Doc anchor | Current anchor | What |
|---|---|---|
| `sc-tasklist:1132-1194` (20-check gate) | **1132-1187** | Gate body ends at 1187 (`If any check 1-20 fails...`); 1189+ is Final Output Constraint. |
| `sc-tasklist:546-646` (tier scoring) | heading at **544** | §5.3 starts one line earlier (544); body 544-648. |
| `sc-tasklist:246-271` (4.4a) | 4.4a body **246-267** | 269+ is §4.4b PRD; doc end anchor 271 lands in 4.4b. |
| `sc-tasklist:130-132` mislabeled "sc:task" | **130-132 = §3.x Source Document Enrichment scope note** | NOT an sc:task anchor; real sc:task anchors are 3, 16, 546, 1409-1418. |

**Real internal inconsistency to fix (not just an anchor drift):**

- `sc-tasklist:1597` says `"Self-Check: all 17 checks passed"` but the authoritative gate at `:1187` defines **20** checks (1-20). **Fix 17→20** as a bounded hygiene item (low risk).

**Confirmed-stable (no drift) anchors:** task-builder DM-003 873-911; task-builder 1066, 1231, 1290-1305; sc-tasklist 1409-1427, 1460-1481, 1525-1558, 169-183, 1297-1308, 1466-1471, 49-57; all four config.py ranges.

---

## 5. Status

**Complete.** All requested citations verified against current `src/superclaude/` source. Key deliverables:
- Citation table (§1) tags every cited anchor [CODE-VERIFIED] / [CODE-VERIFIED+DRIFT] / [CODE-CONTRADICTED].
- `--spec §22` settlement (§2): contradiction characterized verbatim (lines 49/57 vs four `--spec` sites), smallest behavior-preserving reconciliation drafted as exact replacement text for lines 49-57, residual removal-path ambiguity isolated as a HALT Open Question.
- Stale-token absence confirmed (§3): `sc:task-unified`/`llm-workflows`/`StageError` ABSENT; `/rf:`/`.gfdoc` present only in legacy RF ecosystem (non-operative for the generator).
- DRIFT summary (§4) gives the builder current anchors + the real 17→20 inconsistency at :1597.
