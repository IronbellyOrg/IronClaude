# Research Notes: Change F — Tier 2 Audit-Layer Gate

**Date:** 2026-05-27
**Scenario:** A (Explicit — target file known, spec content in proposal)
**Depth Tier:** Standard-Deep
**Track Count:** 3 of 4 (parallel tracks A, C, F, E)
**Template selection:** Template 02 (Complex) — structural skill change with phase-flow integration

---

## EXISTING_FILES

- `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` — 456 lines — the target skill body. Change F adds a new "Tier 2 calibration completeness gate (hard precondition for report publishing)" subsection INSIDE the Wave 3 (Tier 2 — Parallel Hypotheses) section at L230-282, specifically after the calibrator dispatch step.
- `src/superclaude/agents/confidence-calibrator.md` — 118 lines — referenced by the gate's "must parse as a Calibration Report (per the agent's Output Format)" verification check. Read-only for this task.
- `/config/workspace/IronClaude/.dev/brainstorms/calibration-refactor-pr86/cross-env-compare/CROSS-ENV-PROPOSAL-MERGED.md` (in MAIN checkout) — Change F spec at L374-401.

## PATTERNS_AND_CONVENTIONS

- Skill bodies are markdown with `##` heading per Wave + subsections inside. The Wave 3 section uses Bash steps, agent dispatch instructions, and verification clauses.
- Make sync-dev mirrors `src/superclaude/skills/` to `.claude/skills/`. Same source-of-truth rule.
- The proposal's Diff sketch uses verbatim insertion content with `+` prefix — researchers must strip the `+` to produce paste-ready text.
- Audit-log convention: existing skill body already references `audit.log` (need to confirm where it lives and how entries are appended).

## GAPS_AND_QUESTIONS

- **Exact insertion anchor inside Wave 3:** Wave 3 spans L230-282. The proposal says "after the calibrator dispatch step" — researcher must identify the precise line where the calibrator-dispatch instruction ends and the new gate subsection should begin. Likely after a verifiable Bash command or instruction block; before the next Wave 3 subsection or before Wave 4.
- **Audit log path/conventions:** the new gate emits `calibration: missing` log lines. Where does `audit.log` live in the output directory layout? The skill's existing log handling needs to be inventoried.
- **Retry timeout semantics:** the gate spec says "re-dispatch the calibrator subagent for the missing card with the same inputs and a 2-minute extended timeout (one retry only)". Need to confirm how the Agent tool handles timeout overrides — is there a per-spawn timeout flag, or does this map to maxTurns?
- **Force-degrade output format:** the spec says force-degrade confidence to `min(self_reported, 0.65)` with `calibration_status: failed_to_calibrate` annotation in REPORT.md. Need to inventory the REPORT.md schema/template and find where calibration_status fits.
- **Sibling-artifact naming:** the spec uses `tier2-h<N>-*.md` ↔ `tier2-h<N>-*-calibration.md` pairing. Need to confirm this is the actual naming convention used by the skill's Wave 3 output directory layout (or whether the actual convention differs and the spec wording is illustrative).

## RECOMMENDED_OUTPUTS

| # | Researcher | Topic Type | Output File |
|---|------------|-----------|-------------|
| 1 | spec-extraction | Source Spec Extraction | research/01-change-f-spec-extraction.md |
| 2 | target-file-state | File Inventory + Anchor Capture | research/02-target-file-state.md |
| 3 | template-conventions | Template & Examples | research/03-template-and-conventions.md |
| 4 | wave3-integration | Integration Points | research/04-wave3-integration-and-conventions.md |
| 5 | audit-log-and-report | Data Flow Tracer | research/05-audit-log-and-report-conventions.md |

## SUGGESTED_PHASES

- **Researcher 1 — Source Spec Extraction:**
  - Scope: Read proposal L374-401 (Change F spec block).
  - Focus: Extract the full Diff sketch with `+` stripped; extract the MUST/MUST NOT statements ("orchestrator MUST verify on disk"; "MUST NOT publish REPORT.md with the un-calibrated card's confidence"; "Self-reported confidence is NEVER passed through unmodified"); extract the 3-step retry-then-force-degrade ladder; extract the verification command pattern; capture the [V2 MERGED] provenance tag and the "closes Cause #1" rationale.
  - Output: research/01-change-f-spec-extraction.md
  - Other researchers covering: target-file-state covers SKILL.md byte-state; wave3-integration covers exact insertion anchor; audit-log-and-report covers log/report conventions.

- **Researcher 2 — Target File State:**
  - Scope: Read `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` end-to-end with focus on Wave 3 section (L230-282).
  - Focus: byte-level current Wave 3 state; identify the line where the calibrator-dispatch instructions end and the next subsection begins (this is the INSERT anchor); capture surrounding context for a unique-match `old_string`; confirm Wave 3's overall structure (subsections, headings, code fences); confirm whether Wave 3 already has any precondition / gate / verification subsection and if so how the new one should compose with it.
  - Output: research/02-target-file-state.md
  - Other researchers covering: spec-extraction; wave3-integration; audit-log-and-report.

- **Researcher 3 — Template & Conventions:**
  - Scope: Read MDTM Template 02; read Makefile sync targets; read 2-3 other SKILL.md files to confirm consistent wave/subsection conventions.
  - Focus: confirm Template 02 fits a structural-skill-change flow; document any conventions for adding new gates/precondition subsections to skill bodies.
  - Output: research/03-template-and-conventions.md
  - Other researchers covering: spec-extraction; target-file-state.

- **Researcher 4 — Wave 3 Integration Points:**
  - Scope: Trace Wave 3 in detail — calibrator dispatch invocation, output-directory layout, sibling-artifact naming, how Wave 3 hands off to Wave 4 (Adversarial Fix Debate) and Wave 5 (Synthesis + Report).
  - Focus: confirm the actual `tier2-h<N>-*.md` ↔ `tier2-h<N>-*-calibration.md` naming convention vs the spec's wording; identify Wave 3's exit conditions and how the new gate composes with them; identify whether the gate runs BEFORE Wave 4 (recommended per "hard precondition for report publishing") or BETWEEN Wave 4 and Wave 5 ("for report publishing"); confirm the orchestrator's filesystem-verification pattern (Glob? Bash ls?).
  - Output: research/04-wave3-integration-and-conventions.md
  - Other researchers covering: target-file-state; audit-log-and-report.

- **Researcher 5 — Audit Log & REPORT.md Conventions (Data Flow Tracer):**
  - Scope: Locate the skill's `audit.log` writer pattern; locate the REPORT.md template/assembly logic; trace how confidence values flow from calibrator output → REPORT.md entry.
  - Focus: confirm audit.log path and append format; document REPORT.md's card-entry schema and find the slot for `calibration_status: failed_to_calibrate` annotation; verify the spec's `min(self_reported, 0.65)` force-degrade formula maps cleanly to existing confidence-field handling.
  - Output: research/05-audit-log-and-report-conventions.md
  - Other researchers covering: target-file-state; wave3-integration.

## TEMPLATE_NOTES

- Template 02 (Complex) — structural addition to a load-bearing skill body; multi-aspect verification (insert location, audit log, retry semantics, force-degrade math, REPORT.md integration) warrants discovery and verification phases.
- Tier Standard-Deep (5 researchers).
- QA_GATE_REQUIREMENTS: FINAL_ONLY (executor-performed structural check at end + executor-performed integration check of audit log path + REPORT.md schema).
- VALIDATION_REQUIREMENTS: "make sync-dev pass + make verify-sync exit 0 + markdownlint hook PASS on edited file + structural review confirms gate is inside Wave 3 + audit-log/REPORT.md references resolve"
- TESTING_REQUIREMENTS: NONE for THIS task — no automated test harness exists for the skill body. The Track 4 / Change E corpus is for the calibrator; Change F's gate is enforced at orchestrator runtime, not by the corpus. Document this in Risks.

## AMBIGUITIES_FOR_USER

- **Open Question:** the spec uses both `Glob` semantics ("for every `tier2-h<N>-*.md` card") and a Bash verification command ("Verification command (run before publishing)"). The actual implementation may pick one — researcher should recommend the most consistent approach with existing skill conventions, and the task file should document the choice. If the existing skill uses Bash for filesystem checks, prefer Bash; if it uses Glob, prefer Glob.
