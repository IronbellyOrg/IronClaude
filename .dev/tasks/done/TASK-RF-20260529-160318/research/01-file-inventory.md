# Research 01 — File Inventory

**Topic:** File Inventory (Researcher 1 of 5)
**Task:** TASK-RF-20260529-160318
**Date:** 2026-05-29
**Status:** Complete

## Scope

Catalog the CURRENT state of every file the implementation will touch or read. For each file: full path, purpose, key sections/exports with line ranges, line count, dependencies.

---

## File 1: SKILL.md

**Path:** `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`
**Line count:** 468 (`wc -l` output)
**Purpose:** Main protocol document defining the tiered debugging skill. Frontmatter + waves + tool coordination + token-cost profile + refs table.

### Frontmatter (lines 1-5)

- `name`, `description`, `allowed-tools` — SKILL.md:1-5
- Extended metadata comment (category, complexity, mcp-servers, personas) — SKILL.md:7-12

### Top-level sections (line ranges verified)

| Section | Line range |
|---|---|
| `# Troubleshoot Protocol` (H1) | SKILL.md:14 |
| `## Purpose` | SKILL.md:16-24 |
| `## Required Input (STOP if missing)` | SKILL.md:26-35 |
| `## Output Contract` | SKILL.md:37-71 |
| `## Wave Structure` (overview list + fence) | SKILL.md:73-87 |
| `## Tool Coordination Summary` | SKILL.md:389-402 |
| `## Will Do` | SKILL.md:404-413 |
| `## Will Not Do` | SKILL.md:415-425 |
| `## Error Handling` | SKILL.md:427-444 |
| `## Token Cost Profile` | SKILL.md:446-455 |
| `## Refs` | SKILL.md:457-468 |

### Wave sections (heading line + body span verified via Read)

| Wave heading | Heading line | Body span |
|---|---|---|
| `### Wave 0: Parse + Validate Input` | SKILL.md:91 | 91-126 |
| `### Wave 1: Tier 1 — Real-Code Grounding` | SKILL.md:129 | 129-148 |
| `### Wave 1.5: Documentation Grounding` | SKILL.md:152 | 152-186 |
| `### Wave 1.7: Tier 1 — Hypothesis Formation` | SKILL.md:190 | 190-206 |
| `### Wave 2: Confidence Gate` | SKILL.md:210 | 210-227 |
| `### Wave 3: Tier 2 — Parallel Hypotheses` | SKILL.md:230 | 230-292 |
| `### Wave 4: Tier 2 — Adversarial Fix Debate` | SKILL.md:295 | 295-321 |
| `### Wave 5: Synthesis + Report` | SKILL.md:324 | 324-368 |
| `### Wave 6: Tier 3 — Remediation Chain` | SKILL.md:371 | 371-385 |

**Where Wave 1.6 would land (between Wave 1.5 exit ~line 186 and Wave 1.7 entry at line 190):** New wave would insert AFTER the Wave 1.5 horizontal-rule `---` at SKILL.md:188 and BEFORE the `### Wave 1.7` heading at SKILL.md:190. Insertion would require updating Wave 1.7's `**Preconditions**:` line (SKILL.md:194) to add the Wave 1.6 dependency edge, plus updating the Wave Structure list at SKILL.md:75-85, the Tool Coordination Summary at SKILL.md:391-402, and the Refs table at SKILL.md:459-466.

### Markdown tables (name → line range)

| Table | Lines |
|---|---|
| Output Contract field schema (`Field \| Type \| Description`) | SKILL.md:41-57 |
| Wave 1.5 failure-handling table | SKILL.md:178-184 |
| Wave 3 agent selection table (`Signal / type \| Agents to spawn`) | SKILL.md:238-245 |
| Wave 3 failure-handling table | SKILL.md:285-291 |
| Tool Coordination Summary (`Tool \| Tier 1 \| Tier 2 \| Tier 3`) | SKILL.md:391-402 |
| Error Handling table (`Scenario \| Behavior \| Fallback`) | SKILL.md:429-444 |
| Token Cost Profile (`Tier reached \| Auggie tokens \| Claude tokens \| Wall clock`) | SKILL.md:448-453 |
| Refs table (`File \| When loaded`) | SKILL.md:459-466 |

### refs/* files referenced from SKILL.md

All references verified via Read through SKILL.md:1-468:

- `refs/triage-checklist.md` — SKILL.md:77, 462
- `refs/doc-discovery.md` — SKILL.md:78, 160, 163, 463
- `refs/escalation-rubric.md` — SKILL.md:20, 47, 199, 214, 407, 461
- `refs/hypothesis-card-template.md` — SKILL.md:198, 260, 464
- `refs/report-template.md` — SKILL.md:83, 330, 465
- `refs/remediation-handoff.md` — SKILL.md:377, 466

Note: `refs/calibrator-eval-cases.md` is NOT referenced from SKILL.md by name. It is a sibling-test corpus loaded by tests, not by waves.

---

## File 2: refs/triage-checklist.md

**Path:** `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/refs/triage-checklist.md`
**Line count:** 65 (matches spec)
**Purpose:** Wave 1 brief content passed to `root-cause-analyst` agent.

### Section list

| Section | Line range |
|---|---|
| `# Triage Checklist (Wave 1)` (H1) | triage-checklist.md:1 |
| `## Pre-investigation grounding` | triage-checklist.md:5-14 |
| `## Cause-class scan` (incl. table of 13 cause classes) | triage-checklist.md:16-34 |
| `## Evidence-or-drop check` | triage-checklist.md:36-44 |
| `## Fix sketch` | triage-checklist.md:46-54 |
| `## When to refuse Tier 1` | triage-checklist.md:56-65 |

Tables: one — the Cause-class scan table at triage-checklist.md:20-34.

---

## File 3: refs/escalation-rubric.md

**Path:** `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md`
**Line count:** 82 (matches spec)
**Purpose:** Confidence calibration rubric + Wave 2 escalation decision logic. Used by Wave 1.7 (calibration) and Wave 2 (escalation).

### Section list

| Section | Line range |
|---|---|
| `# Escalation Rubric` (H1) | escalation-rubric.md:1 |
| `## Confidence calibration (Wave 1.7)` | escalation-rubric.md:5-25 |
| `### Verdict-direction modifier (M3a)` | escalation-rubric.md:27-35 |
| `### Claim-class × evidence-class cross-tab [V2 merged]` | escalation-rubric.md:37-50 |
| `## Escalation decision (Wave 2)` | escalation-rubric.md:52-72 |
| `## Why 0.85?` | escalation-rubric.md:74-78 |
| `## What escalation does NOT mean` | escalation-rubric.md:80-82 |

### Where the new `## Diagnosability interaction` section would land

Inserting between existing sections, the natural seam is AFTER `## What escalation does NOT mean` (escalation-rubric.md:80-82) at the END of the file (line 83+). This keeps the rubric's primary structure — calibration → modifiers → cross-tab → escalation decision → rationale (`## Why 0.85?`) → caveat (`## What escalation does NOT mean`) → diagnosability interaction — intact. An alternative seam is between line 72 (end of `## Escalation decision`) and line 74 (`## Why 0.85?`), but that breaks the rationale-grouping flow. **Recommended seam: line 83 (append at EOF).**

Tables: three — Confidence-calibration dimensions (escalation-rubric.md:11-18), Verdict-direction modifier (escalation-rubric.md:30-33), Claim-class × evidence-class cross-tab (escalation-rubric.md:41-48).

---

## File 4: refs/doc-discovery.md

**Path:** `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/refs/doc-discovery.md`
**Line count:** 182 (matches spec)
**Purpose:** Wave 1.5 documentation-grounding rules — three discovery branches (release-doc, architectural-doc with currency, semantic-restriction), per-branch schemas, Documentation Context Card template.

### Section list (light inventory only; Researcher 2 does deep extraction)

| Section | Line range |
|---|---|
| `# Documentation Grounding Rules` (H1) | doc-discovery.md:1 |
| Intro paragraphs | doc-discovery.md:1-7 |
| `## Section 1: Auggie query templates per branch` | doc-discovery.md:9-35 |
| `### Branch A — Release-doc lookup` | doc-discovery.md:13-19 |
| `### Branch B — Architectural-doc lookup (with currency validation)` | doc-discovery.md:21-27 |
| `### Branch C — Semantic-restriction extraction` | doc-discovery.md:29-35 |
| `## Section 2: Branch B currency-check procedure` | doc-discovery.md:39-68 |
| `### Step 1 — Filesystem mtime` | doc-discovery.md:43-49 |
| `### Step 2 — Explicit doc-header status markers` | doc-discovery.md:51-57 |
| `### Verdict combination rule` | doc-discovery.md:59-68 |
| `## Section 3: Structured-output schema per branch` | doc-discovery.md:72-127 |
| `### Branch A schema` | doc-discovery.md:76-93 |
| `### Branch B schema` | doc-discovery.md:95-110 |
| `### Branch C schema` | doc-discovery.md:112-127 |
| `## Section 4: Documentation Context Card template` | doc-discovery.md:131-176 |
| `## Loading discipline` | doc-discovery.md:180-182 |

---

## File 5: refs/hypothesis-card-template.md

**Path:** `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md`
**Line count:** 152 (matches spec)
**Purpose:** Hypothesis-card schema used by `root-cause-analyst` (Wave 1.7) and Tier 2 hypothesis agents (Wave 3). Defines frontmatter fields (Cause class, Claim class, Evidence class, Verdict direction, Consistency with docs), the body sections, and a worked example.

### Section list

| Section | Line range |
|---|---|
| `# Hypothesis Card Template` (H1) | hypothesis-card-template.md:1 |
| Intro paragraphs | hypothesis-card-template.md:1-6 |
| `## Template` (fenced markdown block) | hypothesis-card-template.md:7-114 |
| **Inside `## Template`** — the embedded `## Grounding gaps` sub-heading | hypothesis-card-template.md:111-113 |
| `## Filling the card` | hypothesis-card-template.md:116-121 |
| `## Worked example (illustrative — not a real card)` | hypothesis-card-template.md:123-152 |

### `## Grounding gaps` section line range

The literal `## Grounding gaps` heading appears INSIDE the template fence at hypothesis-card-template.md:111. Its body is at lines 112-113 (one-paragraph guidance: "What the agent could **not** verify..."). Note: this is a SUB-HEADING within the fenced template — not a top-level section. A new sibling sub-heading (e.g., `## Diagnosability check` or expanded `## Grounding gaps`) would insert AFTER line 113 and BEFORE the closing fence at line 114.

Tables inside the template: one — the optional v2.0 typed-evidence table at hypothesis-card-template.md:97-101.

---

## File 6: refs/remediation-handoff.md

**Path:** `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/refs/remediation-handoff.md`
**Line count:** 122 (matches spec)
**Purpose:** Wave 6 (Tier 3) remediation-offer prompt + task-builder handoff + reflect gating. Not modified per task spec; inventoried for completeness.

### Section list

| Section | Line range |
|---|---|
| `# Tier 3 Remediation Handoff (Wave 6)` (H1) | remediation-handoff.md:1 |
| `## The user offer` | remediation-handoff.md:5-28 |
| `## Decision matrix` | remediation-handoff.md:30-36 |
| `## Phase A — Build the task file` | remediation-handoff.md:38-66 |
| `## Phase B — Pre-execution review` | remediation-handoff.md:68-77 |
| `## Phase C — Execution gate (always user-initiated)` | remediation-handoff.md:79-92 |
| `## Phase D — Post-execution validation (optional, user-triggered)` | remediation-handoff.md:94-106 |
| `## Why this is the only safe handoff` | remediation-handoff.md:108-113 |
| `## Failure modes` | remediation-handoff.md:115-122 |

Tables: two — Decision matrix (remediation-handoff.md:32-36) and Failure modes (remediation-handoff.md:117-122).

---

## File 7: refs/report-template.md

**Path:** `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md`
**Line count:** 196 (per `wc -l`; matches spec)
**Purpose:** REPORT.md template (Wave 5 deliverable). Defines the header schema, all sections, test-is-wrong rule, behavior-is-documented rule.

### Section list

| Section | Line range |
|---|---|
| `# REPORT.md Template` (H1) | report-template.md:1 |
| Intro | report-template.md:1-4 |
| `## Template` (fenced markdown block opens) | report-template.md:5 |
| Fence opens with template body at line 7 | report-template.md:7-141 |
| **Inside `## Template`** — header block | report-template.md:8-22 |
| **Inside `## Template`** — `## Summary` | report-template.md:25-30 |
| **Inside `## Template`** — `## Documentation Context` | report-template.md:32-41 |
| **Inside `## Template`** — `## Diagnosis` | report-template.md:43-51 |
| **Inside `## Template`** — `## Evidence` | report-template.md:53-61 |
| **Inside `## Template`** — `## Proposed Fix` | report-template.md:63-77 |
| **Inside `## Template`** — `## Alternative Fixes Considered` | report-template.md:79-88 |
| **Inside `## Template`** — `## Risk + Rollback` | report-template.md:90-98 |
| **Inside `## Template`** — `## Follow-up tasks` | report-template.md:100-110 |
| **Inside `## Template`** — `## Grounding Gaps` | report-template.md:112-122 |
| **Inside `## Template`** — `## Next Steps` | report-template.md:124-132 |
| **Inside `## Template`** — `## Audit` | report-template.md:134-140 |
| Template fence closes | report-template.md:141 |
| `## Rendering rules` | report-template.md:143-148 |
| `## Test-is-wrong rule` | report-template.md:150-169 |
| `## Behavior-is-documented rule` | report-template.md:171-196 |
| `### Rendering rules when Behavior is documented: true` | report-template.md:181-186 |
| `### Rendering rules when Behavior is documented: false (docs side with the user)` | report-template.md:188-191 |
| `### Rendering rules when Behavior is documented: n/a (--no-doc-discovery)` | report-template.md:193-196 |

### Where the new `## Diagnosability Context` section should land (per spec: between Documentation Context and Diagnosis)

The `## Documentation Context` section inside the template ends at report-template.md:41 ("Documentation grounding skipped by `--no-doc-discovery`."). The `## Diagnosis` section starts at report-template.md:43. The new `## Diagnosability Context` section would insert at report-template.md:42 (currently a blank line between sections) — between these two top-level sections, inside the template fence. The insertion preserves the user-facing reading order: Header → Summary → Documentation Context → **Diagnosability Context** → Diagnosis → Evidence → Proposed Fix → ...

Tables: zero inside the template body (the header is a series of bold-field bullets, not a table); zero outside the template.

---

## File 8: refs/calibrator-eval-cases.md

**Path:** `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md`
**Line count:** 81 (matches spec)
**Purpose:** Golden fixtures + property tests for calibration. Run before any change to escalation-rubric / hypothesis-card-template / SKILL.md. Inventoried for completeness; not modified per task spec.

### Section list

| Section | Line range |
|---|---|
| `# Calibrator Eval Cases` (H1) | calibrator-eval-cases.md:1 |
| `## Synthetic fixtures (V1 base)` | calibrator-eval-cases.md:5-39 |
| `### Fixture 1 — fixture-h3-style.md (source-only runtime REFUTE)` | calibrator-eval-cases.md:7-11 |
| `### Fixture 2 — fixture-pr86-rca-style.md (AFFIRM with structural truncation)` | calibrator-eval-cases.md:13-17 |
| `### Fixture 3 — fixture-static-defect-clean.md (eval_run.py Path import case)` | calibrator-eval-cases.md:19-22 |
| `### Fixture 4 — fixture-sha-pinned.md (structurally unverifiable predicate)` | calibrator-eval-cases.md:24-27 |
| `### Fixture 5 — fixture-v1-legacy-card.md (missing claim_class — migration)` | calibrator-eval-cases.md:29-33 |
| `### Fixture 6 — fixture-refute-runtime-verified.md (legitimate REFUTE with strong runtime check)` | calibrator-eval-cases.md:35-39 |
| `## Real-card replay fixtures (V2 merged)` | calibrator-eval-cases.md:41-55 |
| `### Fixture 7 — fixture-t4-h3-replay.md [V2 merged]` | calibrator-eval-cases.md:43-45 |
| `### Fixture 8 — fixture-t4-h2-replay.md [V2 merged]` | calibrator-eval-cases.md:47-50 |
| `### Fixture 9 — fixture-t4-h1-no-overcorrect.md [V2 merged]` | calibrator-eval-cases.md:52-55 |
| `## Property tests` (P1-P5 table) | calibrator-eval-cases.md:57-65 |
| `## Suite integrity` | calibrator-eval-cases.md:67-77 |
| `## Implementation hook (deferred to follow-up commit)` | calibrator-eval-cases.md:79-81 |

Tables: one — Property tests (calibrator-eval-cases.md:59-65).

**Note:** This ref is NOT referenced from SKILL.md (verified — no occurrence of `calibrator-eval-cases` in SKILL.md:1-468). Mentioned only in `## Suite integrity` (calibrator-eval-cases.md:67-77) as a CI gate.

---

## File 9: Makefile — target bodies

**Path:** `/config/workspace/IronClaude/Makefile`
**Line count:** 552 (`wc -l` output)

### `lint` target — Makefile:48-50

```
lint:
	@echo "Running linter..."
	uv run ruff check .
```

### `format` target — Makefile:52-55

```
format:
	@echo "Formatting code..."
	uv run ruff format .
```

### `sync-dev` target — Makefile:109-163

Full body summarised (lines 109-163):

- Creates `.claude/skills/` and `.claude/agents/` directories.
- For every `src/superclaude/skills/<name>/` containing `SKILL.md` or `skill.md`: copies tree to `.claude/skills/<name>/`, excluding `__init__.py` and `__pycache__`.
- For every `src/superclaude/agents/*.md` (excluding `README.md`): copies to `.claude/agents/`.
- For every `src/superclaude/commands/*.md` (excluding `README.md`, `__init__.py`): copies to `.claude/commands/sc/`.
- For every `src/superclaude/hooks/scripts/*.sh`: copies to `.claude/hooks/`, sets `chmod +x`.
- If `src/superclaude/scripts/session-init.sh` exists: copies to `.claude/hooks/session-init.sh`, sets `chmod +x`.
- If `src/superclaude/templates/` exists: copies tree to `.claude/templates/`, excluding `agent-memory/` and `__pycache__`.
- Reports counts of skills/agents/commands/hooks/templates synced.

Key invariant: skill subdirectory structure (refs/, templates/, scripts/, etc.) is preserved by the `find ... -exec sh -c ...` pattern at Makefile:117-123.

### `verify-sync` target — Makefile:166-353

Full body summarised (lines 166-353):

- Iterates `src/superclaude/skills/*/` (excluding `__*`); for each, asserts `.claude/skills/<name>/` exists and `diff -rq` finds no differences (excludes `__init__.py` and `__pycache__`).
- Reverse check: any `.claude/skills/<name>/` without a matching `src/superclaude/skills/<name>/` is an error. Skills without `SKILL.md` get an additional "must move to .dev/eval-workspaces/" error.
- Same paired check for `agents/` and `commands/sc/`.
- For `hooks/`: src `src/superclaude/hooks/scripts/*.sh` ↔ `.claude/hooks/*.sh`, with `session-init.sh` allowed to be absent from src.
- For `templates/`: src `src/superclaude/templates/` ↔ `.claude/templates/`, recursive.
- `=== Installer Registration ===` block (Makefile:307-326): asserts `src/superclaude/hooks/scripts/*.sh` set equals `superclaude.cli.install_hooks._FRESHNESS_SCRIPTS` set.
- `=== Hooks Cross-Consistency ===` block (Makefile:328-346): asserts `hooks.json` PostToolUse matcher prefixes (auggie-related) agree with `auggie-flag-clear.sh` case-body prefixes.
- Exits 1 on any drift.

---

## File 10: Audit-log emission pattern in SKILL.md

The audit log is opened in Wave 0 and written by every subsequent wave. The convention is:

### Wave 0 — opens the audit log

SKILL.md:108-121 — emits the machine-readable header block (HTML-comment delimited):

```
<!-- SC:TROUBLESHOOT:TARGET
issue: <first 80 chars>
type: <type|auto>
depth: <quick|standard|deep|auto>
scope: <path|symbol|none>
fix_authorized: <bool>
no_escalate: <bool>
mcps_available: <auggie|serena|context7|tavily|sequential|none>
output_dir: <abs-path>
-->
```

Exit-criteria emission convention (SKILL.md:123): plain-text line `"Wave 0 complete: type=<type> depth=<depth>"`.

### Wave 1 — emits exit message + audit notations

SKILL.md:146 — `"Wave 1 complete: grounding done; handing off to Wave 1.5"`.
SKILL.md:140 — "note the fallback in the audit log" (Grep/Glob fallback when MCPs unavailable).

### Wave 1.5 — emits multiple audit entries

SKILL.md:168 — `doc_context_card_path: <output-dir>/doc-context.md` written to the audit log.
SKILL.md:174 — exit message `"Wave 1.5 complete: doc_context_card_path=<output-dir>/doc-context.md"`.
SKILL.md:180 — failure case: `doc_context_card_path: null` recorded.
SKILL.md:181 — failure case: branch fallback recorded with `degraded: true`.
SKILL.md:184 — failure case: branch synthesis failure logged; "see audit".

### Wave 1.7 — emits calibration + confidence

SKILL.md:200 — fallback: mark `calibration: inline-fallback` in the audit log.
SKILL.md:202 — exit message `"Wave 1.7 complete: confidence=<x>"`.
SKILL.md:204 — fallback: mark `hypothesis_source: inline-fallback` in audit.

### Wave 2 — records escalation reason

SKILL.md:226 — "record the `escalation_reason` in the audit log".

### Wave 5 — appends final footer

SKILL.md:347-358 — appends the machine-readable footer block:

```
<!-- SC:TROUBLESHOOT:SUMMARY
status: <success|partial>
tier_reached: <1|2|3>
confidence: <float>
escalation_reason: <none|low_confidence|multi_domain|forced_by_depth_deep|intermittent>
hypothesis_count: <N>
adversarial_invoked: <bool>
fix_authorized: <bool>
duration_sec: <N>
-->
```

### Pattern summary for new Wave 1.6

The new wave should follow the same pattern as Wave 1.5:

1. Inside the wave body, name specific audit-log entries that must be written (e.g., `diagnosability_card_path: <path>` or `diagnosability_verdict: <value>`).
2. Surface fallback markers in audit (e.g., `diagnosability: inline-fallback`, `degraded: true`).
3. Emit an exit-criteria plain-text line: `"Wave 1.6 complete: diagnosability=<verdict>"` (or equivalent).
4. Use HTML-comment delimited blocks ONLY for the Wave 0 TARGET header and Wave 5 SUMMARY footer; intermediate waves emit `key: value` lines, not delimited blocks.

---

## File 11: Markdownlint config

**Path:** `/config/workspace/IronClaude/.markdownlint.json`
**Line count:** 8

Full content:

```json
{
  "default": true,
  "MD013": false,
  "MD036": false,
  "MD029": false,
  "MD033": false
}
```

### Active ruleset

- `default: true` — all standard markdownlint rules enabled.
- Disabled rules:
  - `MD013` (line-length) — long lines allowed.
  - `MD029` (ordered-list-item-prefix) — numbered list numbering relaxed (matters for the numbered Wave step lists in SKILL.md).
  - `MD033` (no-inline-html) — inline HTML allowed (matters for the HTML-comment delimited audit-log blocks at SKILL.md:111 and 348, and the `<!--` blocks in report-template.md:16-18).
  - `MD036` (no-emphasis-as-heading) — bold-text-acting-as-heading allowed.

### Implications for the new Wave 1.6

- HTML comment blocks (`<!-- ... -->`) for audit-log emission are explicitly permitted (MD033 disabled).
- Long lines in tables and dense descriptive paragraphs are permitted (MD013 disabled).
- Ordered-list step numbering (the `1.`, `2.`, `3.` pattern in every Wave's Steps section) is permitted to be flat-numbered or reset (MD029 disabled).
- Bold-as-heading constructs like `**Goal**:`, `**Preconditions**:`, `**Steps**:`, `**Exit criteria**:` (used in every wave body) are permitted (MD036 disabled).

No `.markdownlint.yaml`, `.markdownlint-cli2.cjs`, or `[tool.markdownlint]` block in `pyproject.toml` was found. The `.markdownlint.json` above is the sole active config.

---

## Summary

Inventoried 11 files plus the audit-log pattern and markdownlint config. The main editable surface for the upcoming Wave 1.6 implementation:

- `SKILL.md` (468 lines): new wave inserts between line 188 (Wave 1.5 horizontal rule) and line 190 (Wave 1.7 heading); also touches Wave Structure list (75-85), Tool Coordination Summary (391-402), Refs table (459-466), and Wave 1.7 preconditions (194).
- `refs/escalation-rubric.md` (82 lines): `## Diagnosability interaction` section appends at EOF (line 83+).
- `refs/report-template.md` (196 lines): `## Diagnosability Context` section inserts between Documentation Context (32-41) and Diagnosis (43-51), at line 42, INSIDE the template fence.
- `refs/hypothesis-card-template.md` (152 lines): `## Grounding gaps` lives at line 111-113 inside the template fence; new fields would insert before the closing fence at line 114.

Audit-log convention: HTML-delimited blocks only at Wave 0 (header) and Wave 5 (footer); intermediate waves emit `key: value` lines and exit-criteria plain-text status messages. Markdownlint allows HTML comments, long lines, ordered-list renumbering, and emphasis-as-heading — no constraint friction for the planned additions. The sync-dev and verify-sync Make targets preserve and verify the `refs/*.md` subdirectory structure, so adding sections to existing refs and adding new audit-log emissions to SKILL.md require only the standard `make sync-dev` workflow.
