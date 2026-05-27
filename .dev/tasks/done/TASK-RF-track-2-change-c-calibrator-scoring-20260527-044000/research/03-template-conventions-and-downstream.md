# Research: Template & Conventions + Downstream Consumer Audit (Track 2 / Change C)

**Date:** 2026-05-27
**Researcher:** template-conventions + downstream-consumers (folded)
**Task:** TASK-RF-track-2-change-c-calibrator-scoring-20260527-044000
**Scope:** MDTM Template 02 selection, sync-dev/verify-sync workflow, markdownlint + block-claude-generated-mirrors hooks, agent-prompt conventions (5 agent files inspected), and full downstream-consumer audit of the Calibration Report contract.

**Status:** Complete

---

## Section 1 — Template Selection: Template 02 (Complex)

**Decision:** Template 02 (Complex Task Template) at `.claude/templates/workflow/02_mdtm_template_complex_task.md` (1205 lines total).

**Rationale — Change C fits Template 02's discovery-and-handoff model:**

Change C is NOT a single-file additive edit. It is a **5-phase workflow** that needs the L1-L6 handoff patterns Template 02 provides:

| Phase | Work | Template 02 pattern that fits |
|-------|------|------------------------------|
| 1. Prerequisite verification | Verify Change A landed (escalation-rubric.md has 6-dim table + `source_only_dynamic_claim` enumerated) | L4 Review/QA pattern (verify upstream artifact state) |
| 2. Target file state capture | Read confidence-calibrator.md byte-exact, capture anchors for 4 distinct edit sites | L1 Discovery pattern (produce inventory file) |
| 3. Multi-section agent prompt edit | 4 distinct sections touched: Independence Instruction (insert), Responsibilities (replace #1, #4, #5 + insert #2a, #3a, #5a), Output Format (insert Stage-2 trace + replace Confidence subsection), new Claim-class handling subsection | L2 Build-from-discovery (each Edit uses the captured anchor) |
| 4. Sync + verify | `make sync-dev` then `make verify-sync` exit 0 then markdownlint hook PASS | L3 Test/Execute pattern (capture raw output + structured summary) |
| 5. Downstream consumer verification | Re-grep SKILL.md for calibrator references; confirm no parser breakage; document any enumerated-list gaps (e.g., SKILL.md L340 audit-log reason enumeration) | L4 Review/QA + L5 Conditional-action (PASS = proceed; FAIL = add follow-up task entry) |

**Why Template 01 does NOT fit:**

Template 01 assumes independent additive items with no cross-item handoff. Change C has explicit handoffs:

- Phase 2's anchor-capture file IS the input for Phase 3's Edit calls (L2 build-from-discovery)
- Phase 4's verify-sync output (PASS/FAIL) gates Phase 5 (L5 conditional)
- Phase 5's grep results may produce a follow-up task entry — that artifact-driven branch is L5

**Compare to Change B (TASK-RF-20260527-022700-change-b-hypothesis-card-schema):** Change B added 3 frontmatter fields to ONE file (hypothesis-card-template.md). Change C edits 4 distinct sections of confidence-calibrator.md AND has a cross-file consumer audit phase. Change B used a lighter footprint; Change C MUST use Template 02.

**Template 02 mandatory sections to honor (cross-referenced to research-notes.md plan):**

- Section A (Core Principles) — workflow-dependent sections are OFF (this is not a workflow-dependent task)
- Section B (Self-Contained Checklist Items) — every item embeds context + action + verification + blocker-logging clause
- Section D2 (Cross-Stage Integration) — REQUIRED here: Change C consumes Change A's rubric additions
- Section F (5-step execution pattern READ then IDENTIFY then EXECUTE then UPDATE then REPEAT) — applies as for any Template 02 task
- Section I15-I17 (Phase-gate QA + Post-completion validation) — research-notes.md says `QA_GATE_REQUIREMENTS: FINAL_ONLY`, so the orchestrator inserts ONE rf-qa gate at the end (per I15) plus the I17 post-completion validation triad (all items checked, all output files exist, blocker entries have resolution notes)
- Section J (Error handling) — embedded blocker-logging clause in every item

---

## Section 2 — Sync-Dev + Verify-Sync Workflow

Source: `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/Makefile`

### `make sync-dev` target (L108-163)

Header comment (L108): "Sync src/superclaude/{skills,agents} -> .claude/{skills,agents} for local dev"

Behavior (verbatim observation):

- L111: `mkdir -p .claude/skills .claude/agents` — idempotent
- L112-125: skills loop — for each `src/superclaude/skills/*/` containing `SKILL.md` or `skill.md`, mirror the entire directory tree into `.claude/skills/<name>/` (excluding `__init__.py` and `__pycache__`). Underscore-prefixed dirs (`__*`) are skipped.
- L126-130: **agents loop** — for each `src/superclaude/agents/*.md` (excluding `README.md`), `cp` it to `.claude/agents/<name>`. **Direct file copy** — no transformation, no diff suppression.
- L131-136: commands loop — `src/superclaude/commands/*.md` to `.claude/commands/sc/<name>`
- L137-143: hooks loop — `src/superclaude/hooks/scripts/*.sh` to `.claude/hooks/<name>` with `chmod +x`
- L144-147: `session-init.sh` shim copy
- L148-157: templates tree copy (excludes `agent-memory/`, `__pycache__`)
- L158-163: success summary printing counts

**Implication for Change C:** the edit is to `src/superclaude/agents/confidence-calibrator.md`. After Edit, `make sync-dev` triggers the L126-130 loop and overwrites `.claude/agents/confidence-calibrator.md` with the new content. No special handling needed for the new Stage-2 trace subsection — it is just additional bytes inside the same file.

### `make verify-sync` target (L165-end)

Header comment (L165): "Verify src/superclaude/ and .claude/ are in sync (CI-friendly, exits 1 on drift)"

Behavior (L166-184+ observed):

- L168: `drift=0` accumulator
- L170-185 (skills branch): for each skills dir, `diff -rq` against `.claude/skills/<name>/`; sets `drift=1` on any difference; emits MISSING or DIFFERS labels
- The same `diff -rq` pattern continues for agents/commands/hooks/templates
- Exit code: 1 on any drift, 0 on clean

**Implication for Change C:** the executor MUST run `make sync-dev` BEFORE `make verify-sync`. Reverse order = verify-sync sees drift and exits 1.

**Recovery path on verify-sync failure:** re-run `make sync-dev`; if it still fails, the `.claude/` copy was edited directly (violating the source-of-truth rule from CLAUDE.md L11) — copy `.claude/` changes back to `src/superclaude/`, then re-sync.

---

## Section 3 — Markdownlint Hook (.pre-commit-config.yaml L70-82)

Source: `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/.pre-commit-config.yaml`

Verbatim hook block (L70-82):

```yaml
  # Markdown linting
  - repo: https://github.com/igorshubovych/markdownlint-cli
    rev: v0.38.0
    hooks:
      - id: markdownlint
        args: ['--fix']
        exclude: |
          (?x)^(
            CHANGELOG\.md|
            .*node_modules.*|
            .*\.min\.md$|
            \.dev/.*
          )$
```

Key facts:

- **Repo:** `https://github.com/igorshubovych/markdownlint-cli`
- **Rev:** `v0.38.0`
- **Hook id:** `markdownlint`
- **Args:** `['--fix']` — auto-fixes violations IN PLACE. Executor must re-Read after the hook runs.
- **Excludes:** `CHANGELOG.md`, anything under `node_modules`, `*.min.md`, `.dev/*` (entire `.dev/` tree). Note: `.dev/tasks/*` task files are excluded, so the task file itself is NOT linted. The target file `src/superclaude/agents/confidence-calibrator.md` IS linted (not in any exclude).

**Implication for Change C:** the edit lands inside a fenced code block at L58-93 of confidence-calibrator.md. Markdownlint may have rules about list spacing (MD032), heading levels (MD025/MD041), or trailing punctuation. The new Stage-2 trace table is a standard markdown table — should not trigger violations. The new `## Claim-class handling` heading uses H2 same as siblings — consistent. The new Confidence subsection bullets use the same `- **Self-reported (in card)**: <X.XX>` pattern as existing bullets — consistent.

**If markdownlint --fix modifies the file:** the executor MUST Re-Read confidence-calibrator.md before any follow-up Edit (freshness-pre-edit hook will enforce this anyway).

---

## Section 4 — block-claude-generated-mirrors Hook + Source-of-Truth Rule

Source: `.pre-commit-config.yaml` L98-109.

Verbatim:

```yaml
  # AC11 / R-017 / T01.20 — source-of-truth discipline gate
  # Rejects generated `.claude/` mirrors on the commit path. Full mirror drift
  # remains available via `make verify-sync`, but pre-commit must not require
  # staging generated mirrors when this repository edits its own src/ sources.
  - repo: local
    hooks:
      - id: block-claude-generated-mirrors
        name: Block generated .claude mirror commits (AC11)
        entry: scripts/precommit_block_claude_mirrors.sh
        language: script
        pass_filenames: false
        files: '^\.claude/(skills|agents|commands|hooks|templates)/'
```

Key facts:

- **Local repo hook** (not a remote pre-commit upstream)
- **Script:** `scripts/precommit_block_claude_mirrors.sh`
- **Trigger pattern:** any path matching `^\.claude/(skills|agents|commands|hooks|templates)/` — this means staging `.claude/agents/confidence-calibrator.md` directly would BLOCK the commit.
- **Why:** AC11 / R-017 / T01.20 — `src/superclaude/` is the source of truth; `.claude/` is a generated mirror. Pre-commit must not require staging generated mirrors.

Cross-reference: user memory `feedback_claude_dir_gitignored.md` reinforces this — `.claude/skills,commands,agents,hooks` are gitignored except `.claude/settings.json`. If `git add` ever needs `-f` for `.claude/*`, STOP.

**Implication for Change C:** the executor MUST `git add src/superclaude/agents/confidence-calibrator.md`, NEVER `.claude/agents/confidence-calibrator.md`. The latter is a sync-dev artifact and the hook will reject it.

---

## Section 5 — Agent-Prompt Edit Conventions

Source files inspected:

- `src/superclaude/agents/confidence-calibrator.md` (118 lines — the target)
- `src/superclaude/agents/evidence-validator.md` (first 60 lines — sibling agent dispatched in same SKILL.md)
- (Cross-reference) other agents in `src/superclaude/agents/` follow the same template

### Frontmatter format (immutable shape, common to all 3 inspected)

```yaml
---
name: <slug>
description: <one-paragraph what + when + by-whom>
category: <analysis|quality|architecture|...>
tools: <comma-separated allowed tool list — e.g., Read or Read, Grep, Glob>
model: <sonnet|opus|haiku>
maxTurns: <int>
permissionMode: <plan|default|edit>
---
```

Calibrator current frontmatter (L1-9): `name: confidence-calibrator`, `category: analysis`, `tools: Read` (Read-only), `model: sonnet`, `maxTurns: 25`, `permissionMode: plan`.

**Change C does NOT modify frontmatter.** The `tools: Read` declaration stays — the new WebFetch-detection step in Responsibility #3a is a MARK-only ("mark spot_check_unverifiable in Notes"), NOT an actual WebFetch invocation, so the tools list does not need to grow (per research-notes.md L24).

### Standard section ordering (observed in both files)

1. `# <Agent Name> — <Subtitle>` (H1, one-line)
2. `## Triggers` (H2 — who delegates, when)
3. `## Role` (H2 — the agent's stance / self-conception)
4. `## Independence Instruction` (H2 — what the agent must NOT inherit from the upstream context)
5. `## Safety Constraint` (H2 — "DO NOT modify..." style boundaries)
6. `## Behavioral Mindset` (H2 — judgment / anti-pattern guidance)
7. `## Inputs` (H2 — bulleted list of named parameters with type/purpose)
8. `## Responsibilities` (H2 — numbered list `1.`, `2.`, ...)
9. `## Output Format` (H2 — fenced ` ```markdown ` block with the report template)
10. `## Boundaries` (H2 — "Will:" / "Will Not:" bulleted lists)
11. `## Failure Modes (what the orchestrator should plan for)` (H2 — bulleted list of failure scenarios)

**Change C inserts a NEW H2 subsection `## Claim-class handling` between Independence Instruction (current L23-27) and Inputs (current L39-45) — i.e., after Behavioral Mindset.** This breaks the standard ordering by one slot, but the new section is conceptually a sub-rule of Independence Instruction so the insertion point is defensible.

### Fenced-code-block convention (Output Format)

The Output Format section uses a fenced ` ```markdown ` block (calibrator L58-93). EVERYTHING inside that fence — including subsection headings like `## Per-dimension scores`, `## Confidence`, `## Escalation recommendation`, `## Notes` — is part of the report template the agent emits, NOT part of the agent prompt's own structure.

**Change C inserts a new `## Stage-2 trace (REQUIRED)` subsection INSIDE this fenced block**, between the per-dimension table (currently ending L74) and the `## Confidence` subsection (currently starting L76). This is an additive insertion to the template the agent emits — it does not alter the existing field semantics.

### Edit-anchoring rule for fenced-block insertions

Because the fenced block contains H2 headings (e.g., `## Confidence`), a naive `old_string = "## Confidence"` will be ambiguous if any other `## Confidence` exists elsewhere. Verified by Read: there is exactly ONE `## Confidence` in confidence-calibrator.md (L76, inside the fenced block). Safe to anchor on the multi-line context `## Confidence\n\n- **Self-reported (in card)**` to be doubly unique.

---

## Section 6 — Downstream Consumer Audit (Calibration Report contract)

This is the critical section. Source files inspected:

- `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` (456 lines) — primary consumer
- `src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md` (52 lines) — defines the rubric the calibrator reads
- `src/superclaude/agents/confidence-calibrator.md` — the producer
- `src/superclaude/agents/evidence-validator.md` — sibling agent (sanity check on contract patterns)
- (Negative result) cross-skill grep for "calibration-report" / "tier1-calibration" / "tier2-*-calibration" — NO other skill references the calibration report files.

### 6a. SKILL.md dispatch sites (where the calibrator is invoked)

**Wave 1.7 dispatch — SKILL.md L199-200:**

```
2. **Calibrate confidence (independently)** — spawn the `confidence-calibrator` agent via `Task` with
   `card_path=<output-dir>/tier1-hypothesis.md`,
   `rubric_path=<skill-dir>/refs/escalation-rubric.md`,
   `card_tier=1`,
   `flags_context=<wave 0 parsed flags>`,
   `output_path=<output-dir>/tier1-calibration.md`.
   ...Its calibrated confidence and verdict feed Wave 2 directly.
   - **Fallback** (L200): if `confidence-calibrator` fails ... fall back to inline orchestrator calibration
     against the rubric and mark `calibration: inline-fallback` in the audit log.
```

**Wave 1.7 exit criteria — SKILL.md L202:** "One hypothesis card at `<output-dir>/tier1-hypothesis.md`, a calibration report at `<output-dir>/tier1-calibration.md` (or `calibration: inline-fallback` in audit), and the calibrated confidence in the audit log. Emit `Wave 1.7 complete: confidence=<x>`."

**Wave 3 dispatch — SKILL.md L263:**

```
3.5. **Calibrate each card independently** — spawn N `confidence-calibrator` instances in parallel
     (one per Tier 2 card), each with `card_tier=2` and
     `output_path=<output-dir>/tier2-<agent-name>-calibration.md`.
     Use the calibrated scores (not the agents' self-reports) when weighting consensus/competing/outlier
     in step 4. Fallback rule from Wave 1.7 applies per-card.
```

**Tool coordination summary — SKILL.md L386:** lists `Task` (agent spawn) and confirms `confidence-calibrator` is called in Tier 1 AND in Tier 2 (per-card).

**Will-Not declaration — SKILL.md L410:** "Trust agent-reported confidence without independent re-grading (the `confidence-calibrator` agent or the inline fallback applies the rubric in a fresh context)."

**Error handling — SKILL.md L432:** "`confidence-calibrator` agent fails for any card | Fall back to inline orchestrator calibration for that card; mark the card with `calibration: inline-fallback` in the audit log; do NOT block escalation on a missing calibration."

### 6b. What fields of the Calibration Report does SKILL.md parse?

Based on SKILL.md dispatch and Wave 2 consumption logic, the orchestrator reads from the calibration report:

| Field in Calibration Report (output template L58-93 of calibrator.md) | Where SKILL.md consumes it |
|---|---|
| `## Per-dimension scores` table | Wave 2 confidence gate (SKILL.md L219-222) uses individual dimension scores: "Multi-domain symptom (e.g. perf + correctness, security + build) -> escalate even if confidence is high"; "Reproducibility unclear or 'intermittent' mentioned -> escalate" — these map to per-dimension scores |
| `## Confidence` -> `Calibrated (this report): <Y.YY>` | Wave 2 confidence gate (L219): "confidence >= 0.85 AND symptom is single-domain -> STOP"; "confidence < 0.85 -> escalate" |
| `## Escalation recommendation` -> `Verdict: STOP / ESCALATE` | Wave 2 outcome (L224-226): STOP jumps to Wave 5; ESCALATE proceeds to Wave 3 and records `escalation_reason` in audit log |
| `## Escalation recommendation` -> `Reason:` (enumerated value) | Audit log writes `escalation_reason: <value>` at SKILL.md L340; also surfaced in Output Contract (L48) and final audit footer (L336-346) |
| `## Notes` | Not directly parsed by SKILL.md, but consumed by evidence-validator at Wave 5 (cross-reference: calibrator.md L90 says "this also feeds the Wave 5 evidence-validator's work") |

**The `## Per-dimension scores` table is the most critical contract:** changing it from 5 rows to 6 rows (Change A's responsibility) is what enables Change C's Responsibility #1 ("6 dimensions"). The orchestrator does NOT enumerate the rows by index — it reads by dimension name — so adding a row is backward-compatible for SKILL.md's prose parsing.

### 6c. Does the new `## Stage-2 trace (REQUIRED)` subsection break any parser?

**Verdict: NO.** Reasoning:

1. The Stage-2 trace is INSIDE the fenced ` ```markdown ` block at calibrator.md L58-93 — i.e., it is part of the report template the agent emits.
2. It is inserted AFTER `## Per-dimension scores` and BEFORE `## Confidence`.
3. The SKILL.md orchestrator does NOT parse the calibration report by section ORDER — it reads named fields (`Calibrated`, `Verdict`, `Reason`).
4. evidence-validator agent at Wave 5 reads the calibration report's `## Notes` section (per calibrator.md L90), not the trace — adding a new section above Notes does not affect Notes parsing.
5. Sibling-agent pattern confirmed: evidence-validator.md also uses a fenced output template with H2 subsections; the orchestrator treats both as named-field reports, not positional structures.

**Recommendation in task file:** add a Phase 5 checklist item that re-greps SKILL.md for any positional/index-based parsing of the calibration report (`Read` the calibration report then `sed -n '<line>'` or `awk` patterns). Current evidence: NO such positional parsing exists. Phase 5 just confirms it.

### 6d. CRITICAL FINDING — Enumerated `escalation_reason` set is INCONSISTENT

Cross-file grep results for `escalation_reason` enumerations:

| File | Line | Enumeration content |
|---|---|---|
| `src/superclaude/agents/confidence-calibrator.md` | L85 | `none / low_confidence / multi_domain / intermittent / not_reproducible / forced_by_depth_deep / security_caution` (**7 values**) |
| `src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md` | L32-39 | `forced_by_depth_deep` (L32), `low_confidence` (L35), `multi_domain` (L36), `intermittent` (L37), `not_reproducible` (L38), `security_caution` (L39) — **6 ESCALATE values + implicit `none`** = 7 |
| `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` | L340 (audit log footer template) | `<none / low_confidence / multi_domain / forced_by_depth_deep / intermittent>` — **5 values** |

**SKILL.md L340 is already missing `not_reproducible` and `security_caution`** — this is a pre-existing inconsistency, NOT caused by Change C, but Change C makes it worse:

> Change C introduces a NEW value `source_only_dynamic_claim` (per proposal L190-255) that is added to the calibrator's enumeration and the rubric's Escalation Decision rules.

After Change C lands, the gap will be:

- Calibrator + rubric: 8 values (current 7 + new `source_only_dynamic_claim`)
- SKILL.md audit-log footer (L340): still 5 values

**Required follow-up (NOT in scope of Change C, but MUST be documented):**

The task file should include a Phase 5 checklist item that VERIFIES this gap exists and emits a Notes entry recommending a follow-up task to align SKILL.md L340 with the rubric. The follow-up may be folded into Change A's task (which already touches the rubric) OR into Change F (final integration). DO NOT silently fix SKILL.md L340 inside Change C — Change C's scope is the calibrator agent only.

### 6e. Cross-file consumer search — full inventory

Grep `escalation_reason` across entire src/superclaude/ tree:

- **Producers/declarators:** confidence-calibrator.md L54, L85; escalation-rubric.md L32-39
- **Audit-log writers:** SKILL.md L226, L340
- **Output contract declaration:** SKILL.md L48
- **UNRELATED CLI namespace (NOT the troubleshoot calibrator):** `src/superclaude/cli/cli_portify/convergence.py` L114, L172, L223, L238, L243, L253 and `src/superclaude/cli/cli_portify/steps/panel_review.py` L164, L189, L191, L207, L209 — these use a Python `EscalationReason` enum (values `MAX_ITERATIONS`, `BUDGET_EXHAUSTED`, `USER_REJECTED`) that is a SEPARATE concept (sc:cli-portify convergence loop). **These are NOT downstream consumers of the calibrator's `escalation_reason`** and do NOT need updating for Change C.

Grep `Calibration Report` / `calibration-report` / `tier1-calibration` / `tier2-*-calibration`:

- **Consumed only by sc-troubleshoot-protocol/SKILL.md** (Wave 1.7 step 2, Wave 3 step 3.5, Wave 2 confidence gate, Wave 5 evidence-validator dispatch which references Notes)
- **No other skill or agent reads the calibration report files.** Confirmed via grep.

Grep `source_only_dynamic_claim` (new value Change C introduces):

- **Zero hits across src/superclaude/** — confirms this is a new enum value and Change A's responsibility to add to the rubric. Change C's responsibility is to update the calibrator's enumeration in its Output Format (L85) and Escalation Decision rule invocation (L54 area).

Grep `spot_check_unverifiable` (new value Change C introduces in Responsibility #3a):

- **Zero hits across src/superclaude/** — confirms this is a new Notes-section marker introduced by Change C. No downstream consumer reads it programmatically; it surfaces in the human-readable Notes section only.

### 6f. evidence-validator's dependency on calibrator's Notes section

Calibrator.md L90 says: "Any evidence the card cited that did not verify on spot-check (this also feeds the Wave 5 evidence-validator's work, but is worth surfacing early)."

evidence-validator.md L59 confirms: validator reads `report_draft_path` (REPORT.md.draft), NOT the calibration report directly. The flow is:

1. Calibrator notes a spot-check failure in its `## Notes` section
2. Wave 5 synthesis reads the calibration report's Notes when composing REPORT.md (per SKILL.md L320-330 prose)
3. evidence-validator re-checks citations in the final REPORT.md draft, not the calibration report

**Implication:** Change C's new `spot_check_unverifiable` marker in Notes is consumed by Wave 5 prose-synthesis, not by evidence-validator directly. No agent contract update needed.

---

## Section 7 — Change B Precedent (Similar Additive Task)

Source: `.dev/tasks/done/TASK-RF-20260527-022700-change-b-hypothesis-card-schema/` (executed Change B task in the same worktree).

**Similarities to Change C:**

- Both are additive edits to a single source-of-truth file under `src/superclaude/`
- Both trigger `make sync-dev` then `make verify-sync` then markdownlint
- Both must respect the source-of-truth rule and the `block-claude-generated-mirrors` hook

**Differences (Change C is more complex):**

| Dimension | Change B | Change C |
|---|---|---|
| Template used | Template 01 (simple additive) | Template 02 (multi-section + handoff) |
| Target file | `src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md` | `src/superclaude/agents/confidence-calibrator.md` |
| Number of distinct edit sites | ~3 (frontmatter additions) | 4 (Independence Instruction insert, Responsibilities replace+insert, Output Format insert+replace, new Claim-class handling section) |
| Downstream consumer audit needed? | No (template is consumed by agents, not by SKILL.md parsers) | YES (SKILL.md L48, L226, L340 + audit log enumeration) |
| Cross-task dependency | Standalone | Hard dependency on Change A landing first (rubric 6-dim + new `source_only_dynamic_claim` enum) |
| Testing requirements | NONE in scope | NONE in scope (Track 4 / Change E builds the harness) |

**Lesson from Change B for Change C:** the additive-frontmatter-fields pattern in Change B used clean YAML-block anchoring. Change C's anchors are PROSE inside fenced markdown — the `old_string` MUST include surrounding context to be unique (calibrator.md has numbered list items that re-number after insertions, and H2 headings inside the fenced block that look identical to non-fenced H2s on grep).

---

## Section 8 — Known Gotchas

1. **Sync-dev BEFORE verify-sync** — `make verify-sync` exits 1 if `.claude/` differs from `src/`. The executor MUST run `make sync-dev` first. Reverse order fails the validation gate.

2. **Markdownlint `--fix` modifies the file in place** — the hook at `.pre-commit-config.yaml` L75 uses `args: ['--fix']`. If the hook auto-fixes anything, the file content on disk no longer matches what the executor wrote. Executor MUST Re-Read confidence-calibrator.md before any subsequent Edit (the `freshness-pre-edit.sh` hook will enforce this anyway, but plan for the re-read in checklist items).

3. **block-claude-generated-mirrors rejects `.claude/agents/*` staging** — `.pre-commit-config.yaml` L102-109 blocks `git add .claude/agents/confidence-calibrator.md`. Executor MUST `git add src/superclaude/agents/confidence-calibrator.md`. If pre-commit fails with this hook, the executor pivoted incorrectly — never stage the mirror.

4. **pre-commit install via uv pip** — if pre-commit hooks are not yet installed in the worktree, run `uv pip install pre-commit && pre-commit install`. NOT `pip install` (CLAUDE.md L8 — "UV only").

5. **Fenced code block H2 ambiguity** — the calibrator's Output Format block at L58-93 contains H2 headings (`## Per-dimension scores`, `## Confidence`, `## Escalation recommendation`, `## Notes`). Grep for `^## Confidence` returns ONE hit currently, but if Change C is partially applied (e.g., the new `## Claim-class handling` section is inserted but the Output Format edit fails), subsequent edits MUST re-Read to confirm anchor uniqueness.

6. **Numbered-list re-numbering hazard** — the Responsibilities section uses `1.`, `2.`, `3.`, ... When Change C inserts `2a.`, `3a.`, `5a.`, the existing items keep their numbers (sub-letter convention), but if any item is replaced (e.g., #1, #4, #5 per the proposal), the `old_string` for each REPLACE MUST anchor on the full numbered line plus the following line to disambiguate from numerically-similar lines elsewhere.

7. **Independence Instruction vs. Behavioral Mindset placement** — the new `## Claim-class handling` H2 subsection inserts between Independence Instruction (L23-27) and Inputs (L39-45). The current file ALSO has `## Safety Constraint` (L29-31) and `## Behavioral Mindset` (L33-37) between those two endpoints. The insertion point per proposal L190-255 is AFTER Independence Instruction but BEFORE Safety Constraint (verify against proposal — researcher 1's spec-extraction output has the exact placement). If proposal says "between Independence Instruction and Inputs," the precise slot is ambiguous; the orchestrator MUST land it specifically AFTER Behavioral Mindset (just before Inputs) to keep the Safety Constraint adjacent to Independence Instruction.

8. **Hard prerequisite on Change A** — Change C's Responsibility #1 ("6 dimensions") and §5 (gated-minimum formula) ONLY make sense after Change A lands. Phase 1 checklist item MUST verify by re-Reading `src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md` that:
   - The 6-dimension table is present (currently 5 dimensions, per L31 confidence-calibrator description "5-dimension rubric")
   - The new `source_only_dynamic_claim` value is enumerated in the rubric's Escalation Decision rules
   - The gated-minimum formula and verdict-direction modifier are documented
   If any verification fails, the task MUST HALT — Change C is invalid without Change A.

9. **SKILL.md L340 audit-log enumeration is pre-existing tech debt** — currently 5 values, missing `not_reproducible` and `security_caution` from the rubric. Change C adds an 8th value (`source_only_dynamic_claim`) to the rubric. Task file MUST surface this gap in a Findings entry; the fix is a SEPARATE follow-up task (likely Change F integration), NOT inside Change C's scope.

10. **frontmatter immutability** — the calibrator's frontmatter `tools: Read` is NOT modified by Change C. Researcher 1 (spec-extraction) MUST confirm proposal does not require WebFetch/Bash; current evidence (research-notes.md L24) says spot_check_unverifiable is MARK-only, no new tools needed.

---

## Status: Complete

## Summary

**Track 2 / Change C is a Template 02 (Complex) task** with a 5-phase workflow:

1. Prerequisite verification (Change A landed)
2. Anchor capture (covered by researcher 2)
3. Multi-section agent prompt edit (4 distinct sites)
4. Sync + verify (sync-dev then verify-sync then markdownlint)
5. Downstream consumer audit (per this report)

**Key facts captured:**

- **Sync workflow:** Makefile L108-163 (sync-dev) and L165+ (verify-sync). Mirror direction: `src/superclaude/agents/*.md` to `.claude/agents/<name>` via L126-130 loop. verify-sync uses `diff -rq` and exits 1 on drift.
- **Pre-commit hooks:** `.pre-commit-config.yaml` L70-82 (markdownlint v0.38.0 with `--fix`, excludes `.dev/*`) and L98-109 (`block-claude-generated-mirrors` — rejects `.claude/{skills,agents,commands,hooks,templates}/` staging).
- **Agent-prompt conventions:** 11-section template (Triggers / Role / Independence Instruction / Safety Constraint / Behavioral Mindset / Inputs / Responsibilities / Output Format / Boundaries / Failure Modes). Output Format is a fenced ` ```markdown ` block with H2 subsections. Confirmed across confidence-calibrator.md and evidence-validator.md.
- **Downstream consumer audit findings:**
  - Calibrator is dispatched ONLY by sc-troubleshoot-protocol/SKILL.md (Wave 1.7 L199-200, Wave 3 L263, tool table L386, Will-Not L410, error-handling L432, exit criteria L202)
  - Orchestrator parses calibration report by NAMED FIELDS, not positional order — the new Stage-2 trace insertion is SAFE (no parser breakage)
  - **CRITICAL: SKILL.md L340 audit-log `escalation_reason` enumeration is INCONSISTENT with the rubric** — currently lists 5 values, rubric defines 7, and Change C adds an 8th (`source_only_dynamic_claim`). This is pre-existing tech debt PLUS a new gap. Task file MUST flag for a follow-up (likely Change F integration), NOT fix inside Change C.
  - `escalation_reason` references in `src/superclaude/cli/cli_portify/*.py` are an UNRELATED namespace (convergence loop) — NOT downstream consumers of the troubleshoot calibrator.
  - No other skill/agent reads the calibration report files. evidence-validator reads REPORT.md, not the calibration report directly.
  - New values `source_only_dynamic_claim` and `spot_check_unverifiable` have zero current hits — confirming they are new in Change C.

**Outputs ready for task-builder Phase 4 (task file emission):**

- Template 02 confirmed
- 5-phase structure mapped to L1-L6 handoff patterns
- VALIDATION_REQUIREMENTS per research-notes.md L73: sync-dev pass + verify-sync exit 0 + markdownlint PASS + downstream consumer cross-check (Phase 5)
- TESTING_REQUIREMENTS: NONE (Track 4 / Change E has the harness — document this in Risks section)
- 10 gotchas captured for Phase-3 / Phase-4 / Phase-5 checklist guidance
