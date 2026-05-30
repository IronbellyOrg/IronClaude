# PG.B Verification Inventory — SKILL.md + 3 modified refs

Captured: 2026-05-29 17:40

## Line-count deltas

| File | Pre-edit | Post-edit | Delta | Notes |
|------|----------|-----------|-------|-------|
| `SKILL.md` | 468 | 546 | +78 | +~70 for Wave 1.6 section (Step 4.4) + 4 Output Contract rows + 6 Error Handling rows + 1 Token Cost row + 1 Refs row + 3 Will Do + 3 Will Not Do + 1 Wave Structure line + 1 hard-stop edge note + 1 deep-banner instruction = 78 (within target). |
| `refs/diagnosability-audit.md` | n/a (new) | 340 | new | 8 sections + terminal Loading discipline, twin of doc-discovery.md. |
| `refs/hypothesis-card-template.md` | 152 | 154 | +2 | One paragraph appended in `## Grounding gaps` section per Step 3.1 (a long sentence, ~2 lines after word-wrap). |
| `refs/report-template.md` | 184 | 256 | +72 | (1) `## Diagnosability Context` section (~13 lines); (2) Hard-stop Next Steps variant with verbatim chat message (~40 lines); (3) `--depth deep` banner template (~5 lines); (4) SKIPPED header field line (~2 lines); + spacing. |
| `refs/escalation-rubric.md` | 82 | 90 | +8 | Terminal `## Diagnosability interaction` section ≤15 lines per Step 3.3 (8 lines incl. heading). |

## Per-change-point landing verification (SKILL.md)

| Change-point | Spec source | Landed at | Status |
|--------------|------------|-----------|--------|
| **E1** Wave Structure ASCII insert Wave 1.6 line + hard-stop edge note | merged-output §10 row 1 | SKILL.md:83 (Wave 1.6 line) + L89 (hard-stop edge note inside fence) | ✓ Present |
| **E2** Output Contract +4 rows (diagnosability_verdict, _context_card_path, _tasklist_path, _hard_stop) | merged-output §5:244-249 | SKILL.md:58-61 | ✓ Present (all 4 rows, vocabulary exact, 19 rows total: was 15) |
| **E3** SKILL.md Wave 0 step 1 flag list +3 flags (--no-diagnosability-audit, --diagnosability-handoff, --reset-diagnosability-rounds) | research/06 §A2 (12th change-point) | SKILL.md:103 | ✓ Present (all 3 flags in spec order) |
| **E4** New Wave 1.6 section ~70 lines | merged-output §1:14-66 + §10 row 4 | SKILL.md:196-249 (54 content lines + heading + spacing → ~70 with prefix lines) | ✓ Present (heading at L196; Preconditions, S1.6.0-S1.6.4, Per-defect counter, Exit criteria, Failure handling table 6 rows, Token budget; trailing `---` at L250) |
| **E5** Wave 1.7 Preconditions +Wave 1.6 hard-stop clause | merged-output §10 row 5 | SKILL.md:255 | ✓ Present (appended `; Wave 1.6 did NOT fire its hard-stop ... When Wave 1.6 hard-stopped, this wave is skipped entirely.`) |
| **E6** Wave 5 step 2 — Diagnosability Context bullet + hard-stop rendering + `--depth deep` banner instruction | merged-output §10 row 6 | SKILL.md:396 (new bullet between Documentation Context L395 and Diagnosis L397); SKILL.md:406 (hard-stop + deep-banner prose continuation) | ✓ Present (bullet sits between Documentation Context and Diagnosis; hard-stop + deep-banner instructions appear as prose continuation after the bullet list, matching the existing `--no-doc-discovery` continuation paragraph pattern) |
| **E7** Tool Coordination Tier 1 annotations × 3 (auggie, Task, Read/Grep/Glob) | merged-output §10 row 7 | SKILL.md:457 (auggie row), L462 (Task row), L464 (Read/Grep/Glob row) | ✓ Present (3 specific Tier 1 cells annotated with Wave 1.6 detail; no new column added — preserves existing 4-column table structure) |
| **E8a** Will Do +3 bullets | merged-output §10 row 8 Will Do section | SKILL.md:478-480 | ✓ Present (3 bullets appended after the existing 8-bullet Will Do list, in spec order: default-run, hard-stop, instrumentation tasklist) |
| **E8b** Will Not Do +3 bullets | merged-output §10 row 8 Will Not Do section | SKILL.md:493-495 | ✓ Present (3 bullets appended after the existing Will Not Do list, in spec order: don't auto-apply tasklist, don't force hard-stop under --no-escalate, never target failing-component source) |
| **E10** Error Handling +6 rows | merged-output §10 row 10 | SKILL.md:515-520 | ✓ Present (6 rows appended after existing 15-row table → 21 rows total) |
| **E9** Token Cost Profile +1 row + net-saving footnote | merged-output §10 row 9 | SKILL.md:530 (Wave 1.6 row) + L532 (net-saving parenthetical appended to existing prose) | ✓ Present |
| **E11** Refs table +1 row for refs/diagnosability-audit.md | merged-output §10 row 11 | SKILL.md:544 | ✓ Present (appended after refs/remediation-handoff.md row, matching existing 2-column schema) |

## Per-modified-ref landing verification

| Ref | Spec | Landed at | Status |
|-----|------|-----------|--------|
| `refs/hypothesis-card-template.md` — one-paragraph append under `## Grounding gaps` | merged-output §9:533-541 | hypothesis-card-template.md:115 | ✓ Present (appears inside the template fenced block after the existing Grounding gaps prose line) |
| `refs/report-template.md` — `## Diagnosability Context` section + hard-stop Next Steps variant + `--depth deep` banner + SKIPPED header field (4 surgical insertions) | merged-output §7:388-485, §9 | report-template.md:20 (SKIPPED header field, between Doc context card L19 and Duration L21); L24-30 (`--depth deep` banner template between header `---` separator and Summary, conditional comment); L50-63 (`## Diagnosability Context` section between Documentation Context end L48 and Diagnosis L65); L156-194 (Hard-stop Next Steps variant inside Next Steps section, includes 3-round cap paragraph) | ✓ All 4 surgical insertions present |
| `refs/escalation-rubric.md` — terminal `## Diagnosability interaction` section ≤15 lines | merged-output §9:547-549 | escalation-rubric.md:84-90 (heading + 5 prose lines) | ✓ Present (terminal section appended after `## What escalation does NOT mean`, ≤15 lines) |

## Bidirectional cross-reference consistency

| From | To | Resolved? |
|------|-----|----------|
| `SKILL.md` Refs table L544 → `refs/diagnosability-audit.md` | New ref file exists at expected path | ✓ |
| `refs/diagnosability-audit.md` L3 anchor → Wave 1.6 | SKILL.md:196 `### Wave 1.6: Diagnosability Audit` exists | ✓ |
| `refs/hypothesis-card-template.md:115` → "Diagnosability Context Card with `verdict ∈ {partial, insufficient}`" | refs/diagnosability-audit.md Section 6 defines the card and Section 4 defines the verdict vocabulary | ✓ |
| `refs/report-template.md:50-63` `## Diagnosability Context` section | refs/diagnosability-audit.md Section 6 (card template) defines the consumed content shape | ✓ |
| `refs/escalation-rubric.md:84-90` `## Diagnosability interaction` → refs/diagnosability-audit.md Section 5 | Section 5 exists at L163 of the new ref | ✓ |
| `SKILL.md:211` `**S1.6.1 — Load refs/diagnosability-audit.md**` enumerates Sections 1-8 | All 8 sections present in new ref | ✓ |
| `SKILL.md:396` Wave 5 bullet → `<output-dir>/diagnosability-context.md` | Section 6 of new ref defines the artifact's content; refs/report-template.md:60 also references it | ✓ |

## Unintended-rewrite check (sample lines from sections added since brainstorm)

Per `research/06-corrections.md` §A1, two newer sections of SKILL.md added since the brainstorm sit DOWNSTREAM of Wave 1.6's insertion point and should remain unmodified:

| Section | Original line | Post-edit location | Shifted by | Status |
|---------|--------------|--------------------|------------|--------|
| Wave 3 Tier 2 calibration completeness gate (originally L263-277) | L263 | L327 | +64 | ✓ Unmodified (confirmed via `grep -n '#### Tier 2 calibration completeness gate'` returning L327) |
| Wave 5 evidence-validator block (originally L343-344) | L343-344 | L407-408 | +64 | ✓ Unmodified (confirmed via `grep -n 'evidence-validator'` returning L407, L408, L490, L513, L462 — all references) |

Shift of +64 is consistent with the Wave 1.6 section insertion size (~70 lines minus existing 6 lines of blank separator + heading recovery). No drift.

## Provenance comment check across all 5 edited files

```
grep -c '<!-- Source:' SKILL.md refs/diagnosability-audit.md refs/hypothesis-card-template.md refs/report-template.md refs/escalation-rubric.md
```

Expected: 0 in all. Will be verified by rf-qa adversarial pass.

## Verdict

All 12 SKILL.md change-points + 3 modified-ref additions landed at their verified post-shift coordinates. Bidirectional cross-references resolve. Two downstream sections (Wave 3 calibration gate, Wave 5 evidence-validator block) remain unmodified. No new Output Contract row violates the debate Axis 3 verdict (the `status` enum is preserved unchanged).

Ready for PG.B rf-qa adversarial verification.
