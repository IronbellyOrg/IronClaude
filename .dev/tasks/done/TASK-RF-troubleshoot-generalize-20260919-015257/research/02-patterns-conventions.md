# Research 02 — Patterns & Conventions

**Task:** TASK-RF-troubleshoot-generalize-20260919-015257
**Topic:** Patterns & Conventions a builder must follow for §(d) R-01..R-19
**Status:** Complete
**Researcher:** patterns-conventions agent (read-only on repo)
**Date:** 2026-09-19

## Scope

- `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` (Wave 1, Wave 1.6, Wave 5 blocks)
- `src/superclaude/skills/sc-troubleshoot-protocol/refs/diagnosability-audit.md`, `refs/hypothesis-card-template.md`
- `src/superclaude/agents/confidence-calibrator.md`, `src/superclaude/agents/evidence-validator.md`
- `tests/troubleshoot/test_hardening_h0.py`, `tests/troubleshoot/test_hardening_output_contract.py`, `tests/conftest.py`
- `CLAUDE.md` (git workflow + component sync), `Makefile` (sync-dev/verify-sync/lint/test), `pyproject.toml` (ruff)

All claims cite `file:line` and quote verbatim.

## 1. SKILL.md — inserting a wave step / sub-step

File: `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`

### 1.1 Wave heading style

- Level-3 heading, `### Wave N: <Title>`; optional em-dash tier prefix. Verbatim:
  - `:156` `### Wave 1: Tier 1 — Real-Code Grounding`
  - `:217` `### Wave 1.6: Diagnosability Audit`
  - `:426` `### Wave 5: Synthesis + Report`
  - `:406` `### Wave 4.5: Pipeline Hardening Closure`
- Every wave block is bracketed by `---` on its own line with a blank line either side (`:154`, `:177`, `:215`, `:270`, `:424`, `:483`). Wave 0 is preceded by `---` at `:112` right after the "Refs are loaded per-wave, never pre-loaded." line (`:110`).
- Sub-section headings inside a wave use level-4 (`####`): `:348` `#### Tier 2 calibration completeness gate (hard precondition for report publishing)`.

### 1.2 Bold-label paragraph order inside a wave

Observed fixed order (Wave 1.6 `:217-268` is the most complete example):

1. `**Goal**: ...` (`:219`)
2. `**Preconditions**: ...` — either inline (`:160` `**Preconditions**: Wave 0 complete.`) or `**Preconditions**:` + blank + bullet list (`:221-226`)
3. `**Steps**:` + blank line + numbered list (`:228`)
4. optional free paragraph with bold lead (`:248` `**Per-defect patch-round counter**: ...`)
5. `**Exit criteria**: ...` inline (`:173`) or `**Exit criteria**:` + bullets (`:250-255`)
6. `**Failure handling**:` + table with `| Scenario | Behavior | Fallback |` header (`:257-266`, `:203-211`, `:365-373`)
7. `**Token budget...**` line (`:175`, `:213`, `:268`, `:288`)
8. Wave-specific alternates: `**STOP conditions**:` (`:152`), `**Skip conditions**:` (`:402`), `**Trigger**:` (`:410`), `**On STOP**:` / `**On escalate**:` (`:306`, `:308`).

Wave 5 (`:426-481`) omits Preconditions/Failure handling/Token budget and has only Goal, Steps, Exit criteria.

### 1.3 Step bullet style

- Numbered `1.` list; each item starts with a bold verb phrase followed by ` — ` (em-dash) then prose. Verbatim `:164`:
  `1. **Ground the symptom in real code** — issue two parallel MCP calls (or fall back to native tools):`
- Sub-bullets are 3-space-indented `-` under the numbered item (`:165-167`).
- Wave 1.6 uses **explicit sub-step IDs** `S1.6.N` inside the bold: `:230` `1. **S1.6.0 — Component identification**. ...`, `:232` `2. **S1.6.1 — Load \`refs/diagnosability-audit.md\`** (lazy load, mirroring Wave 1.5's discipline). ...`. Steps are separated by blank lines in Wave 1.6 (`:230-246`) but not in Wave 1/1.5/5.
- Wave 4.5 uses gate IDs `H0`–`H5` in the bold: `:414` `1. **H0 — Applicability + mechanism** (\`refs/pipeline-hardening-closure.md\`): ...`.
- Fractional step numbers are used for inserts between existing steps: `:345` `3.5. **Calibrate each card independently** — ...` and `:471` `4.5. **Emit TFEP return-contract (conditional, when \`caller=task-unified\`)** — ...`. **This is the established idiom for inserting a new sub-step without renumbering.**
- Fallback for an agent spawn is a nested bullet `- **Fallback**: if ... fails (...), fall back to ... and mark \`...: inline-fallback\` in the audit log.` (`:282`, `:452`).
- Lazy-load of a ref is an explicit first step: `:432` `1. Load \`refs/report-template.md\` (not before now — lazy load).` and `:187` `1. **Load \`refs/doc-discovery.md\`** — read the Section 1 ..., the Section 2 ..., ...`.

### 1.4 "Emit:" exit line

Exit criteria always end with an `Emit "Wave N complete: ..."` sentence carrying key=value pairs:

- `:150` `**Exit criteria**: input validated, output dir created, audit log opened. Emit "Wave 0 complete: type=<type> depth=<depth>".`
- `:173` `... Emit "Wave 1 complete: grounding done; handing off to Wave 1.5".`
- `:201` `- Emit "Wave 1.5 complete: doc_context_card_path=<output-dir>/doc-context.md".`
- `:255` `` - Emit `Wave 1.6 complete: verdict=<v> complexity=<c> hard_stop=<bool> round=<N>/3`. `` (backticks instead of quotes — both forms exist)
- `:284` `... Emit "Wave 1.7 complete: confidence=<x>".`

Wave 5 has no Emit line; its exit is `:481` `**Exit criteria**: \`REPORT.md\` written, audit log finalized, user notified. If \`--fix\` is not set, return the output contract and STOP. ...`.

### 1.5 Token-target line

Two phrasings, both used:

- `:175` `**Token budget for Wave 1**: target ≤ ~3k Claude tokens (MCP retrieval offloads the bulk of the work). ...`
- `:213` `**Token budget**: Wave 1.5 should consume ≤ 2k Claude tokens (the auggie calls offload heavy retrieval). If it goes over 3k Claude tokens, audit-log the overrun — ...`
- `:268` `**Token budget**: ≤ 2-3k Claude tokens (auggie offloads retrieval bulk). Hard-stop case yields a net token saving over the full Tier 2 pipeline.`

Adding a wave also requires a row in the `## Token Cost Profile` table `:574-580` (e.g. `:580` `| Wave 1.6 added | +1-2k auggie | +1-2.5k Claude | +30-60s wall clock |`).

### 1.6 Wave Structure diagram + Tool Coordination + Will Do/Will Not + Error Handling

A new wave/sub-step must be reflected in five other places (this is what Wave 1.6 did):

- `## Wave Structure` text block `:95-108`, one line per wave with `← always; loads refs/<file>.md on demand; skipped only by --<flag>` annotation (`:99`).
- `## Tool Coordination Summary` table `:505-516` — parenthetical additions inside existing cells, e.g. `:507` `... Wave 1.6 audit fan-out: 2 parallel branch queries (A log-call, B log-config))`.
- `## Will Do` bullets `:520-530` — plain `-` bullets, sentence case, no trailing period except the last three (`:528-530` end with `.`).
- `## Will Not Do` bullets `:534-545`.
- `## Error Handling` table `:549-570` with header `| Scenario | Behavior | Fallback |`; Wave-scoped rows are labelled in the Scenario cell, e.g. `:566` `| Auggie unavailable (Wave 1.6) | ... |`. Wave 1.6 rows are DUPLICATED verbatim between the in-wave Failure handling table (`:261-266`) and the global Error Handling table (`:565-570`).

### 1.7 Refs table and lazy-load footers

`## Refs` table `:584-602`, header `| File | When loaded |`. Row format: backticked repo-relative path from the skill dir + wave + parenthetical contents summary. Verbatim:

- `:594` `` | `refs/diagnosability-audit.md` | Wave 1.6 (audit query templates, fallback paths, sufficiency rubric, complexity gate, context card template, tasklist rules + hard constraints, T4 worked example) | ``
- `:591` `` | `refs/hypothesis-card-template.md` | Wave 1.7 and Wave 3 (passed to agents) | ``

Closing line `:602` `Each ref is loaded only by the wave that needs it. Do not pre-load.` Also `:110` `Each wave has explicit entry/exit criteria. Refs are loaded per-wave, never pre-loaded.`

### 1.8 Output Contract additions

New contract fields go in the `## Output Contract` table `:41-77` (`| Field | Type | Description |`). Field names are backticked snake_case; `string \| null` types escape the pipe (`:50`, `:52`). Additive fields cite the version: `:62` `| \`contract_version\` | semver string | Output-contract semver, default \`1.1.0\`. Additive version stamp ...`. Derivation rules for flags are bold-titled paragraphs directly after the table: `:79` `**\`test_is_wrong\` derivation rule** (applied during Wave 5 synthesis): ...`.

### 1.9 Flags

New flags are registered in Wave 0 step 1 `:120` (`Optional: \`--type\`, \`--depth\`, ..., \`--no-diagnosability-audit\`, \`--diagnosability-handoff\`, \`--reset-diagnosability-rounds\`, \`--context\`, \`--caller\`.`) and in the audit TARGET header block `:134-145` if they affect the header.

## 2. Adding a new ref file (`refs/<name>.md`)

Two header styles coexist; the **wave-owned** style (diagnosability-audit / doc-discovery) is the one to copy for a wave-loaded ref.

### 2.1 Header (wave-owned style)

`refs/diagnosability-audit.md:1-7` verbatim:

```markdown
# Diagnosability Audit Rules

Wave 1.6 of the sc:troubleshoot protocol. Loaded on demand by Wave 1.6 only.

This ref defines the two parallel audit branches (A: ...), the per-branch structured-output schemas, ... and the T4 worked example. Wave 1.7 (hypothesis formation) and Wave 5 (synthesis + report) consume the synthesised Diagnosability Context Card.

---
```

Same shape at `refs/doc-discovery.md:1-7` (`Wave 1.5 of the sc:troubleshoot protocol. Loaded on demand by Wave 1.5 only.`). Pattern: H1 title → one-line "Wave N ... Loaded on demand by Wave N only." → one paragraph "This ref defines ... <consumers> consume ..." → `---`.

Alternate (gate-owned, Wave 4.5 refs): `refs/effective-input-proof.md:1` `# Effective-Input Proof (H4)` followed by a prose paragraph linking sibling refs with relative markdown links `[`hardening-output-contract.md`](hardening-output-contract.md)` (`:3`). `refs/pipeline-hardening-closure.md:7` uses the same relative-link idiom. No "Loaded by" line in these; SKILL.md's Refs table carries the wave binding instead.

### 2.2 Section numbering

Wave-owned refs use `## Section N: <Title>` numbered H2s and `### <Branch/Topic>` H3s. Verbatim from diagnosability-audit.md:

- `:9` `## Section 1: Auggie query templates per branch`
- `:13` `### Branch A — Log-Call Inspection`
- `:47` `## Section 2: Fallback paths (auggie unavailable)`
- `:78` `## Section 3: Structured-output schemas per branch`
- `:120` `## Section 4: Sufficiency rubric + 3-W's synthesis`
- `:163` `## Section 5: Complexity gate`
- `:192` `## Section 6: Diagnosability Context Card template`
- `:238` `## Section 7: Tasklist generation rules + hard constraints`
- `:288` `## Section 8: T4 worked example — what the audit saves`

Every H2 section is separated by `---` (`:7`, `:45`, `:76`, `:118`, `:161`, `:190`, `:236`, `:286`, `:336`). SKILL.md refers to these by number (`:232` `Read Section 1 (query templates), Section 2 (fallback paths), ...`), so section numbers are load-bearing cross-references — **do not renumber existing sections; append**.

Gate-owned refs (pipeline-hardening-closure.md) instead use un-numbered gate-labelled H2s: `:15` `## H0 — Applicability gate (FR-1)`, `:22` `## H0 — Boundary scan row schema`, `:46` `## H5 — Off-path reviewer rule + waiver standard (FR-11)` — FR ids in parentheses.

### 2.3 Rubric/table idioms inside a ref

- Rubric rows are bold-IDed in the first cell: `:138` `| **S1**: Symptom is a deterministic exception ... | \`sufficient\` (stack trace IS the signal) |`, header `| Signal combination | Verdict |` (`:136`), preceded by `### Sufficiency rubric (applied in order; first match wins)` (`:134`).
- Enumerations are stated as set notation in backticks: `:116` `` `config_type` ∈ `{file, env_var, pipeline_config}`. ``
- Hard constraints are a numbered list with bold lead + colon: `:244` `1. **Invocation-site-only**: Every task MUST target ...` under `### Hard constraints (non-negotiable)` (`:242`).
- Templates for emitted artifacts are fenced ```` ```markdown ```` blocks with `<placeholder>` angle-bracket slots (`:196-234`, hypothesis-card-template.md `:9-116`).
- Schemas are fenced ```` ```json ```` blocks (`:84-95`, `:101-114`).
- Fallback commands are fenced ```` ```bash ```` blocks (`:53-61`).

### 2.4 Ref-local footer ("Loaded by Wave N")

`refs/diagnosability-audit.md:336-340` verbatim:

```markdown
---

## Loading discipline

This ref is loaded by Wave 1.6 only. Other waves do not import it. Wave 1.6 reads Section 1 (query templates), Section 2 (fallback paths), ... and Section 8 (T4 worked example) on entry; the file is not re-read during the wave.
```

`refs/doc-discovery.md:180-182`: `## Loading discipline` / `This ref is loaded only by Wave 1.5. Do not pre-load. ...`. The footer enumerates every section by number, so a new section must be added to the footer list too.

### 2.5 Where an existing ref gets cross-wave notes

`refs/hypothesis-card-template.md:115` shows the idiom for an existing ref acknowledging a newer wave: a trailing paragraph inside the template's `## Grounding gaps` section: `If Wave 1.6 emitted a Diagnosability Context Card with \`verdict ∈ {partial, insufficient}\`, reference it here (e.g., "Diagnosability verdict: partial — see <card-path>; ...").` Header line `:3` names its consumers: `Used by every agent that produces a hypothesis — \`root-cause-analyst\` in Wave 1.7, and every Tier 2 agent in Wave 3.`

Template field additions in hypothesis-card-template.md are bold-label lines in the frontmatter block with indented em-dash sub-definitions: `:16-22` `**Claim class**: \`static_defect\` | \`runtime_behavior\` | ...` then `  — \`static_defect\`: source-reading alone is sufficient evidence ...`. Versioned additions carry a bracket tag in the heading: `:84` `## Evidence classification [V2 merged]`, `:93` `## Recommended evidence shape (v2.0 preview)`.

`refs/escalation-rubric.md` tail (last 5 lines) is the model for a "forward reference" note when a new wave *consumes* an existing ref without changing it: `This is a forward reference: Wave 1.6's complexity gate is the consumer; this rubric is unchanged.`

## 3. Extending an agent (`src/superclaude/agents/<name>.md`)

Files: `confidence-calibrator.md` (142 lines), `evidence-validator.md` (129 lines). Both share one section skeleton (verified by reading both):

```text
--- frontmatter: name, description, category, tools, model, maxTurns, permissionMode ---
# <Title> — <Role Noun> Agent
## Triggers            (bullets; first bullet names the delegating skill + wave)
## Role
## Independence Instruction
## [Claim-class handling]   (calibrator only)
## Safety Constraint
## Behavioral Mindset
## Inputs
## Responsibilities
## Output Format       (single fenced ```markdown block)
## [Status Decision]   (validator only)
## Boundaries          (**Will:** bullets / **Will Not:** bullets)
## Failure Modes (what the orchestrator should plan for)
```

### 3.1 Frontmatter

`confidence-calibrator.md:1-9`:

```yaml
---
name: confidence-calibrator
description: Independently re-grades a hypothesis card ... Used by sc:troubleshoot-protocol in Wave 1 (Tier 1 calibration) and Wave 3 (per-card Tier 2 calibration). ...
category: analysis
tools: Read
model: sonnet
maxTurns: 25
permissionMode: plan
---
```

`evidence-validator.md:4-8`: `category: quality`, `tools: Read, Grep, Glob`, `maxTurns: 50`. The `description` field names the caller skill and wave(s) — if a wave is renumbered/generalized, update the description AND the Triggers bullet (`confidence-calibrator.md:15` `- Delegated by \`sc:troubleshoot-protocol\` in Wave 1 (after the Tier 1 hypothesis card is written) and in Wave 3 (...)`). NOTE: calibrator still says "Wave 1" although SKILL.md moved calibration to Wave 1.7 (`SKILL.md:281`) — an existing drift the builder may need to reconcile.

### 3.2 Inputs section — bullet style

`confidence-calibrator.md:45-51`:

```markdown
## Inputs

- `card_path`: absolute path to the hypothesis card to score
- `rubric_path`: absolute path to `refs/escalation-rubric.md`
- `card_tier`: 1 or 2 (affects the escalation recommendation)
- `flags_context`: dict with `--depth`, `--no-escalate`, `--type` (...)
- `output_path`: where to write your calibration report
```

`evidence-validator.md:37-44` prefixes with a sentence `The orchestrator passes you:` then the same `- \`name\`: description` bullets; defaults are stated inline (`:44` `` `allow_command_reexec`: bool, ... Default and recommended: `false`. ``). Input names match the `Task` call kwargs in SKILL.md (`SKILL.md:281`, `:451`) exactly — keep both sides in sync.

### 3.3 Responsibilities/Process — numbering style

Numbered list with bold lead; **sub-steps inserted with letter suffixes, not renumbering**: `confidence-calibrator.md:56-63`:

```markdown
2. **Read the card** at `card_path`.
2a. **Resolve `claim_class`, `evidence_class`, and `verdict_direction` from frontmatter.** ...
3. **Spot-check the evidence**: ...
3a. **WebFetch URL detection** [V2 merged]: ...
...
5a. **Apply the verdict-direction modifier** per the rubric: ...
```

Provenance tags in square brackets after the bold (`[V2 merged]`). `evidence-validator.md:48-59` uses `1.`–`4.` with indented `-` sub-bullets for per-case rules (`:52-55`) and backticked verdict vocab (`:55` `Verdict per citation: \`verified\` / \`line-mismatch\` / \`file-missing\` / \`snippet-mismatch\`.`).

### 3.4 Output Format — table style

Single fenced ```` ```markdown ```` block containing an H1 report title, bold `**Key**: <placeholder>` header lines, then `##` sections with pipe tables. `confidence-calibrator.md:67-116` (header `# Calibration Report`, `**Card under calibration**: <abs path>`, tables `| Dimension | Score | Justification (cite card content) |` `:77`, `| Step | Value | Notes |` `:88`), section marked `## Stage-2 trace (REQUIRED)` `:86`. `evidence-validator.md:63-97` (`# Evidence Validation Report`, `| # | Type | Location | Verdict |` `:76`, `| # | Type | Location | Reason | Recommended action |` `:82`). The SKILL.md Wave 3 gate `:358` greps these literal markers (`# Calibration Report`, `## Per-dimension scores`, `**Verdict**: STOP|ESCALATE`, `**Calibrated (this report)**:`) — output-format headings are contract, don't rename.

### 3.5 Boundaries — Will / Will-Not list

`confidence-calibrator.md:118-134`:

```markdown
## Boundaries

**Will:**

- Score each dimension independently using the rubric's anchors
...

**Will Not:**

- Trust the card's self-reported confidence as a starting point
- Re-write the card
...
```

Identical shape in `evidence-validator.md:105-122`. Bullets are imperative verb phrases, no trailing period. (Contrast: SKILL.md uses `## Will Do` / `## Will Not Do` H2s at `:518`, `:532`.)

### 3.6 Failure Modes

`## Failure Modes (what the orchestrator should plan for)` with `- **<Mode>**: <orchestrator action>; logs \`calibration: inline-fallback\` in audit.` (`confidence-calibrator.md:136-141`, `evidence-validator.md:124-128`). The audit-log token (`calibration: inline-fallback`) must match SKILL.md `:282`/`:564`.

### 3.7 Safety constraint boilerplate

Both agents: `## Safety Constraint` / `**DO NOT modify, edit, delete, move, or rename ANY file.** You may only write your <report>.` (`confidence-calibrator.md:35-37`, `evidence-validator.md:27-29`). Keep verbatim for any read-only agent.

## 4. Content-assertion pytest over markdown

Directory: `/config/workspace/IronClaude/tests/troubleshoot/` (package; `__init__.py` present). Existing files: `test_hardening_h0.py`, `_h1..._h4.py`, `test_hardening_output_contract.py`, `test_hardening_verdict.py`, `e2e-backtest-scenarios.md`, `backtest/`.

### 4.1 Package marker

`tests/troubleshoot/__init__.py:1-4` verbatim:

```python
# Test package for the sc-troubleshoot-protocol Pipeline Hardening Closure mode.
# Content-assertion tests over the source-of-truth markdown under
# src/superclaude/skills/sc-troubleshoot-protocol/ (REPO_ROOT = Path(__file__).resolve().parents[2]),
# following the tests/skills/ convention.
```

### 4.2 File naming

`test_<feature>_<unit>.py`: `test_hardening_h0.py` (feature=hardening, unit=gate H0), `test_hardening_output_contract.py`, `test_hardening_verdict.py`. Function names: `test_<gate>_<behaviour>` e.g. `test_h0_applicability_skip_requires_boundary_scan` (`test_hardening_h0.py:19`), `test_output_contract_backward_compat` (`test_hardening_output_contract.py:59`). pytest discovery config (`pyproject.toml` `[tool.pytest.ini_options]`): `python_files = ["test_*.py"]`, `python_functions = ["test_*"]`, `addopts = ["-v", "--strict-markers", "--tb=short"]` — `--strict-markers` means any `@pytest.mark.<x>` must be in the registered `markers` list; the existing content tests use **no markers**.

### 4.3 Module header idiom (imports + REPO_ROOT + module-level read)

`test_hardening_h0.py:1-16` verbatim:

```python
"""H0 (Applicability Gate + Boundary Scan) content-assertion tests.

Asserts the documented FR-1 / §5.6 H0 markers in the source-of-truth ref
src/superclaude/skills/sc-troubleshoot-protocol/refs/pipeline-hardening-closure.md.
Content gate over the markdown Claude Code consumes at runtime (see tests/skills/).
"""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
REFS = (
    REPO_ROOT / "src" / "superclaude" / "skills" / "sc-troubleshoot-protocol" / "refs"
)
CLOSURE = (REFS / "pipeline-hardening-closure.md").read_text(encoding="utf-8")
```

`test_hardening_output_contract.py:13-18` adds `SKILL_DIR = REPO_ROOT / "src" / "superclaude" / "skills" / "sc-troubleshoot-protocol"`, `SKILL = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")`, and short UPPER constants per ref (`OC`, `RT`). Same `parents[2]` idiom in `tests/skills/test_task_builder_merge.py:20`. Only stdlib imports (`pathlib`); no `pytest` import needed when no fixtures/markers are used. Agents would be `REPO_ROOT / "src" / "superclaude" / "agents" / "<name>.md"` (no existing test reads agents — new idiom, same shape).

### 4.4 Docstring cites

Module docstring: first line = `<Unit> content-assertion tests.`; body names the FR/§ and the source-of-truth path. Function docstring = `"""<FR-id> <AC-id>[ + <NFR>]: <one-sentence assertion in plain English>."""` — `test_hardening_h0.py:20-21` `"""FR-1 AC2: an applicable=false skip requires a recorded one-sentence reason AND the boundary scan — a bare reason is insufficient."""`; `test_hardening_output_contract.py:60-62` `"""FR-13 AC1 + NFR-6: the SKILL.md Output Contract still contains ALL pre-existing result fields ..."""`. For this track, cite `R-NN` from merged-report-v2.md §(d) in the same slot.

### 4.5 Assertion idioms

- Case-insensitive prose check: `low = CLOSURE.lower()` then `assert "one-sentence reason" in low, "skip must record a one-sentence reason"` (`test_hardening_h0.py:22-30`).
- Accept both spellings with `or`: `:24-27` `assert ("pipeline_hardening_applicable = false" in low or "pipeline_hardening_applicable=false" in low), "..."`; `test_hardening_output_contract.py:92-95` same for `pass|blocked|advisory|not_applicable`.
- Field-tuple loop with f-string message: `test_hardening_output_contract.py:21-41` `LEGACY_FIELDS = (...)` then `:63-66` `for field in LEGACY_FIELDS: assert f"\`{field}\`" in SKILL, (f"legacy Output Contract field removed/renamed: {field}")` — backticked field names assert the table cell, not incidental prose.
- Literal heading check: `:89` `assert "## Pipeline Hardening Closure" in RT`.
- Verbatim token: `:98` `assert "NOT PROVEN" in RT`.
- Inline `# ...` comment above each assert explaining the AC clause (`test_hardening_h0.py:23`, `:28`, `:31`).
- Every `assert` carries a message; multi-line messages use parenthesized string on the next line (`:32-34`).

### 4.6 conftest.py — nothing to add

`tests/conftest.py` provides only reflexion/PM-agent fixtures (`_pollution_snapshot` session autouse `:28`, `_redirect_reflexion_writes` autouse `:82`, `sample_context`, `low_confidence_context`, `sample_implementation`, `failing_implementation`, `temp_memory_dir`) and `collect_ignore` (`:13-15`). Content-assertion tests use none of them; `tests/troubleshoot/` has no local conftest. No new fixture is required for the pattern (tests researcher covers any deliberate fixture design).

### 4.7 Verified green baseline

Ran: `uv run ruff check tests/troubleshoot/` → `All checks passed!`; `uv run pytest tests/troubleshoot/test_hardening_h0.py tests/troubleshoot/test_hardening_output_contract.py -q` → `5 passed in 0.05s` (2026-09-19).

## 5. Git / sync workflow for skill edits

### 5.1 Source of truth and sync

CLAUDE.md "Component Sync": `Source of truth is src/superclaude/. Always edit there first, then make sync-dev.` Makefile `sync-dev` (`Makefile:109`) copies `src/superclaude/skills/*/` → `.claude/skills/<name>/` (all files except `__init__.py`/`__pycache__`), `src/superclaude/agents/*.md` → `.claude/agents/`, `src/superclaude/commands/*.md` → `.claude/commands/sc/`, hooks, templates. `verify-sync` (`Makefile:166`) runs `diff -rq` per skill dir and `diff -q` per agent/command and exits 1 on drift: `❌ Drift detected! Run 'make sync-dev' to fix, or copy .claude/ changes to src/.` (`Makefile:351`).

Order for this track: edit `src/superclaude/skills/sc-troubleshoot-protocol/**` + `src/superclaude/agents/*.md` (+ `src/superclaude/commands/troubleshoot.md` if the command advertise line changes — #173 touched it) → `make sync-dev` → `make verify-sync` → `make lint` → `make test`.

### 5.2 Never stage `.claude/`

CLAUDE.md "ABSOLUTE RULE: Never Stage or Commit `.claude/` Contents": only `.claude/settings.json` is tracked. `.gitignore:120-121` `.claude/*` / `!.claude/settings.json`. Pre-commit local hook `block-claude-generated-mirrors` (`.pre-commit-config.yaml`, `files: '^\.claude/(skills|agents|commands|hooks|templates)/'`, entry `scripts/precommit_block_claude_mirrors.sh`) rejects them. `git add -f` on `.claude/` is the violation siren. Stage by explicit path: `git add src/superclaude/skills/sc-troubleshoot-protocol/ src/superclaude/agents/<x>.md tests/troubleshoot/<new>.py`.

### 5.3 Branch naming + commits

CLAUDE.md "Git Workflow": `master (production) ← integration (testing) ← feature/*, fix/*, docs/*`; conventional commits enforced by `conventional-pre-commit` hook (commit-msg stage). Prior troubleshoot work landed as:

- `013ba2cc feat(sc-troubleshoot-protocol): add Wave 1.6 Diagnosability Audit (#107)`
- `71f16e13 feat(troubleshoot): Pipeline Hardening Closure mode (H0-H5 + waiver latch) (#173)`
- `a7a23896 feat(troubleshoot): insert Tier 2 calibration completeness gate into Wave 3 (Change F) (#96)`
- `300c06a6 feat(tfep): migrate Test Failure Escalation Protocol off /sc:forensic onto /sc:troubleshoot (#180)`

Scope token `troubleshoot` (or `sc-troubleshoot-protocol`); type `feat` for new waves/refs, `refactor` is the natural type for a generalization refactor. Existing local branches use `fix/<kebab>`; suggested `feature/troubleshoot-generalize` (CLAUDE.md example: `git checkout -b feature/your-feature`). Core rule: never commit directly to master.

Worktrees, if used, go under `.dev/worktrees/<name>` (CLAUDE.md: `git worktree add .dev/worktrees/<name> <branch>`; never `EnterWorktree`).

### 5.4 PR target

CLAUDE.md "ABSOLUTE RULE: PR Target = Fork": mandatory shape `gh pr create --repo IronbellyOrg/IronClaude --base master --head <branch> --title "..." --body "..."`. Pre-PR: `git remote -v` (origin = `IronbellyOrg/IronClaude.git`), `git fetch origin && git log master..origin/master` (rebase if fork master is ahead), verify returned URL is `https://github.com/IronbellyOrg/IronClaude/pull/N`. Never `upstream` / `SuperClaude-Org`.

### 5.5 Markdown lint (pre-commit)

`.pre-commit-config.yaml` runs `markdownlint --fix` on all `.md` except `CHANGELOG.md`, `.dev/*`, node_modules, `tests/swarm/fixtures/bare_review_v1/golden/*`. `.markdownlint.json`: `default: true`, `MD024 siblings_only`, `MD013` (line length) **off**, `MD029` (ol prefix) off, `MD036` (emphasis-as-heading) off, `MD033` (inline HTML) off. So: long lines OK, `**Bold**:` pseudo-headings OK, `<!-- -->` HTML comments OK, fractional `3.5.` list items OK (MD029 off), but duplicate sibling headings (same level, same parent) will fail, and `trailing-whitespace` hook excludes `.md` while `end-of-file-fixer` / `mixed-line-ending --fix=lf` apply. #173 recorded `markdownlint clean` as a validation step in its commit body.

## 6. Ruff rules new test files must pass

`pyproject.toml:191-220`:

```toml
[tool.ruff]
line-length = 88
target-version = "py310"
exclude = ["docs/"]
extend-exclude = [".dev/", "tests/audit/fixtures/syntax_error.py"]

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "TID"]
ignore = ["E501", "N818"]
```

Implications for `tests/troubleshoot/test_*.py`:

- `E501` ignored → long assert strings are fine, but `make format` (`uv run ruff format .`, `Makefile:53`) still wraps at 88 (hence the parenthesized `REFS = (...)` at `test_hardening_h0.py:13-15`).
- `I` (isort) → `from __future__ import annotations` first, blank line, then `from pathlib import Path`; stdlib before third-party.
- `F` → no unused imports (don't import `pytest` unless used).
- `N` → snake_case functions, UPPER_CASE module constants (`REPO_ROOT`, `CLOSURE`, `LEGACY_FIELDS`).
- `TID` banned-api → never `import anthropic`.
- `make lint` = `lint-architecture` + `uv run ruff check .` (`Makefile:48-50`); `make test` = `uv run pytest` (`Makefile:13-15`).

## 7. Builder checklist (condensed)

1. **New wave sub-step in SKILL.md** — `N.5.`-style fractional number or `S<wave>.<n>` bold ID; bold verb + ` — ` + prose; `- **Fallback**:` nested bullet for agent spawns; Exit criteria ends with `Emit "Wave N complete: k=<v> ..."`; `**Token budget**:` line; mirror any Failure-handling rows into `## Error Handling`; add to Wave Structure block, Tool Coordination, Will Do / Will Not Do, Token Cost Profile; register flags in Wave 0 step 1 and TARGET header.
2. **New ref** — H1 + `Wave N of the sc:troubleshoot protocol. Loaded on demand by Wave N only.` + "This ref defines ..." + `---`; `## Section N:` H2s separated by `---`; templates in ```` ```markdown ````, schemas in ```` ```json ````; end with `## Loading discipline` enumerating sections; add `| \`refs/<name>.md\` | Wave N (<contents>) |` row to SKILL.md Refs table; never renumber existing sections.
3. **Agent extension** — keep the 12-section skeleton; Inputs are `- \`kwarg\`: desc` and must match SKILL.md `Task` kwargs; insert Responsibilities as `2a.`/`3a.` letter-suffixed steps with `[tag]` provenance; Output Format is one fenced markdown block whose headings are grep-contracts; Boundaries = `**Will:**` / `**Will Not:**`; update frontmatter `description` + Triggers wave references.
4. **Test** — `tests/troubleshoot/test_<feature>_<unit>.py`; stdlib-only; `REPO_ROOT = Path(__file__).resolve().parents[2]`; module-level `read_text(encoding="utf-8")` into UPPER constants; function docstring `"""R-NN ACn: <claim>."""`; every assert has a message; `.lower()` for prose, backticked names for table cells, `or` for accepted spellings; no markers.
5. **Workflow** — branch `feature/…` off master; edit `src/` only → `make sync-dev` → `make verify-sync` → `make lint` → `make test`; stage explicit `src/` + `tests/` paths, never `.claude/`; conventional commit `feat|refactor(troubleshoot): ...`; `gh pr create --repo IronbellyOrg/IronClaude --base master --head <branch>`.
6. **Lint** — ruff `E,F,I,N,W,TID`, E501 ignored, format at 88; markdownlint with MD013/MD029/MD033/MD036 off, MD024 siblings-only.

## Summary

- SKILL.md waves follow a fixed Goal → Preconditions → Steps → Exit criteria (`Emit "Wave N complete: ..."`) → Failure handling table → Token budget order, `---`-separated; fractional step numbers (`3.5.`, `4.5.`) and `S1.6.n` IDs are the insert idioms; a wave change fans out to 5 other SKILL.md sections plus the Refs table.
- Wave-owned refs use the `Wave N ... Loaded on demand by Wave N only.` header, `## Section N:` numbering with `---` separators, and a `## Loading discipline` footer; section numbers are cross-referenced from SKILL.md so are append-only.
- Agents share a 12-section skeleton; Inputs bullets mirror `Task` kwargs, Responsibilities extend via `2a.`/`3a.`, Output Format headings are grep-contracts (SKILL.md:358), Boundaries are `**Will:**`/`**Will Not:**`; calibrator still cites "Wave 1" where SKILL.md now says Wave 1.7.
- Content tests are stdlib-only, `REPO_ROOT = Path(__file__).resolve().parents[2]`, module-level `read_text`, FR/AC-cited docstrings, messaged asserts; existing suite is ruff-clean, format-clean, and green.
- Workflow: edit `src/` → `make sync-dev` → `make verify-sync` → `make lint`/`make test`; never stage `.claude/`; conventional commits with `troubleshoot` scope; PR only via `--repo IronbellyOrg/IronClaude`.
