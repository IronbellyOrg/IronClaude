# Step 6.3 — Cross-Reference Resolution Check

Captured: 2026-05-29 17:53
Scope: Every Wave-1.6-related reference under `src/superclaude/skills/sc-troubleshoot-protocol/`. Verify each reference resolves to a real target (no ORPHANs).

Total references found via grep: **87** across SKILL.md + 4 refs.

## Methodology

Grouped references by referent class — each class is independently verified.

## Class 1 — `refs/diagnosability-audit.md` path references

| Citer | Referent | Resolution |
|-------|----------|-----------|
| SKILL.md:83 (Wave Structure ASCII) | `refs/diagnosability-audit.md` (file path) | ✓ RESOLVED — file exists at `src/superclaude/skills/sc-troubleshoot-protocol/refs/diagnosability-audit.md` (340 lines) |
| SKILL.md:211 (S1.6.1 step body, lists Sections 1-8) | Sections 1-8 of refs/diagnosability-audit.md | ✓ RESOLVED — all 8 sections present (PG.A inventory L9, L47, L78, L120, L163, L192, L238, L288) |
| SKILL.md:241 (Error Handling row) | `refs/diagnosability-audit.md` Section 2 | ✓ RESOLVED — Section 2 (Fallback paths) at L47 |
| SKILL.md:516 (Error Handling row again, duplicate of L241 context) | `refs/diagnosability-audit.md` Section 2 | ✓ RESOLVED — same as above |
| SKILL.md:544 (Refs table row) | `refs/diagnosability-audit.md` (file path + description) | ✓ RESOLVED |
| refs/escalation-rubric.md:86 (Diagnosability interaction section) | `refs/diagnosability-audit.md` Section 5 (complexity gate) | ✓ RESOLVED — Section 5 at L163 |

## Class 2 — Wave 1.6 anchor (heading) references

| Citer | Referent | Resolution |
|-------|----------|-----------|
| refs/diagnosability-audit.md:3 (top-of-file wave anchor) | Wave 1.6 heading in SKILL.md | ✓ RESOLVED — SKILL.md:196 `### Wave 1.6: Diagnosability Audit` |
| SKILL.md:83 (Wave Structure ASCII) | Wave 1.6 heading | ✓ RESOLVED (self-ref to SKILL.md:196) |
| refs/hypothesis-card-template.md:115 ("Wave 1.6 emitted ...") | Wave 1.6 (the artifact-emitting agent) | ✓ RESOLVED — Wave 1.6 in SKILL.md emits the card |
| refs/escalation-rubric.md:84-90 (Diagnosability interaction section, references Wave 1.6's complexity gate) | Wave 1.6 + Section 5 of new ref | ✓ RESOLVED |
| refs/report-template.md:52 ("Wave 1.6 diagnosability audit result") | Wave 1.6 (which produces the audit result) | ✓ RESOLVED |
| refs/report-template.md:158 ("Wave 1.6 hard-stop fired") | The hard-stop branch in S1.6.4 (SKILL.md:220) | ✓ RESOLVED |
| refs/report-template.md:161 ("Wave 1.6 Diagnosability Audit — HALT") | Hard-stop chat message rendered when Wave 1.6 hard-stopped | ✓ RESOLVED — matches the merged-output §7 spec |
| refs/report-template.md:192 ("Wave 1.6 has now hard-stopped 3 times") | 3-round cap branch in the per-defect counter (SKILL.md:227) | ✓ RESOLVED |

## Class 3 — Output Contract field references

| Citer | Referent | Resolution |
|-------|----------|-----------|
| SKILL.md:58 (`diagnosability_verdict` row) | Field itself (definition) | ✓ RESOLVED — self-definitional row |
| SKILL.md:59 (`diagnosability_context_card_path` row) | Field itself | ✓ RESOLVED |
| SKILL.md:60 (`diagnosability_tasklist_path` row) | Field itself | ✓ RESOLVED |
| SKILL.md:61 (`diagnosability_hard_stop` row) | Field itself | ✓ RESOLVED |
| SKILL.md:89, 204, 220, 240, 245, 396, 406, 478, 479, 480, 515, 517, 518 (downstream references in Wave Structure, Wave 1.6 preconditions, S1.6.4 branching, failure handling, Wave 5 step 2, Will Do, Error Handling) | Output Contract fields | ✓ ALL RESOLVED — each matches a field defined in the contract table |
| refs/report-template.md:30 ("`diagnosability_verdict ∈ {insufficient, partial}`") | The `diagnosability_verdict` field's vocabulary | ✓ RESOLVED — vocabulary matches SKILL.md:58 + refs/diagnosability-audit.md Section 4 |
| refs/report-template.md:63 ("`diagnosability_hard_stop=true`") | The `diagnosability_hard_stop` field | ✓ RESOLVED — matches SKILL.md:61 |
| refs/hypothesis-card-template.md:115 ("verdict ∈ {partial, insufficient}") | The `diagnosability_verdict` field's vocabulary | ✓ RESOLVED |
| SKILL.md:406 ("`diagnosability_verdict ∈ {insufficient, partial}`") | Same as above | ✓ RESOLVED |

## Class 4 — Flag references

| Citer | Referent | Resolution |
|-------|----------|-----------|
| SKILL.md:103 (Wave 0 step 1 flag list) | Defines `--no-diagnosability-audit`, `--diagnosability-handoff`, `--reset-diagnosability-rounds` | ✓ RESOLVED — self-definitional |
| SKILL.md:83, 204, 240, 396, 478, 515 (consumers of `--no-diagnosability-audit`) | The flag defined at L103 | ✓ ALL RESOLVED |
| SKILL.md:480 + 493 + refs/report-template.md:185 + 189 (consumers of `--diagnosability-handoff`) | Flag defined at L103 | ✓ ALL RESOLVED |
| SKILL.md:227 + 245 + 520 + refs/diagnosability-audit.md:284 + refs/report-template.md:192 (consumers of `--reset-diagnosability-rounds`) | Flag defined at L103 | ✓ ALL RESOLVED |
| SKILL.md:225, 406, refs/report-template.md:30 (consumers of `--depth deep` in Wave 1.6 context) | Pre-existing `--depth` flag in SKILL.md Wave 0 | ✓ RESOLVED — flag was pre-existing; Wave 1.6 layers behavior onto it |
| SKILL.md:494, 220, 221, refs/diagnosability-audit.md (multiple) (consumers of `--no-escalate` in Wave 1.6 context) | Pre-existing `--no-escalate` flag | ✓ RESOLVED — pre-existing |

## Class 5 — Runtime artifact path references

| Citer | Referent | Resolution |
|-------|----------|-----------|
| SKILL.md:217, 232, refs/diagnosability-audit.md:194, refs/report-template.md:60 (consumers of `<output-dir>/diagnosability-context.md`) | The runtime artifact written by S1.6.3 | ✓ RESOLVED — Wave 1.6 S1.6.3 in SKILL.md:217 specifies the write; Section 6 of new ref defines its content |
| SKILL.md:220, 233, refs/diagnosability-audit.md:233, 240, refs/report-template.md:61 (consumers of `<output-dir>/diagnosability-tasklist.md`) | Runtime artifact written when verdict ∈ {partial, insufficient} | ✓ RESOLVED — SKILL.md:233 specifies the write; Section 7 of new ref defines its content |
| SKILL.md:227, 245, refs/diagnosability-audit.md:284 (consumers of `<output-dir>/diagnosability-rounds.json`) | Per-defect counter file written by the orchestrator | ✓ RESOLVED — Self-documenting; the counter is a JSON file the orchestrator maintains |
| SKILL.md:231 (`<output-dir>/wave1_6-branch-<A|B>.md`) | Per-branch output files written by S1.6.2 | ✓ RESOLVED — self-documenting exit criterion |
| refs/report-template.md:172 ("Diagnosability Context Card: <abs path>" placeholder) | Placeholder for the runtime card path | ✓ RESOLVED — template placeholder, filled at render time |

## Class 6 — "Diagnosability Context" section references

| Citer | Referent | Resolution |
|-------|----------|-----------|
| SKILL.md:223, 224 (S1.6.4 branching → "surface in REPORT.md's Diagnosability Context section") | The `## Diagnosability Context` section in refs/report-template.md | ✓ RESOLVED — refs/report-template.md:50 has `## Diagnosability Context` heading |
| SKILL.md:396 (Wave 5 step 2 bullet — "(≤6-line summary of the Wave 1.6 Diagnosability Context Card ... )") | Section in REPORT.md AND the card itself | ✓ RESOLVED — section at refs/report-template.md:50; card defined in Section 6 of new ref |
| refs/report-template.md:50 (the `## Diagnosability Context` section itself) | Self-definitional — declares the section | ✓ RESOLVED |
| refs/report-template.md:63 ("this section is replaced by the hard-stop block ... in the **Next Steps** hard-stop variant below") | Hard-stop variant at L156-194 | ✓ RESOLVED — variant exists |

## Class 7 — "Diagnosability interaction" reference

| Citer | Referent | Resolution |
|-------|----------|-----------|
| refs/escalation-rubric.md:84 (terminal section heading) | Self-definitional — the section itself | ✓ RESOLVED |

## Verdict

**ZERO ORPHAN references.** All 87 grep-surfaced Wave-1.6-related references resolve to:

- a defined section in the same file (self-references), OR
- a section/heading in another file in the protocol directory (cross-file references), OR
- an Output Contract field defined in SKILL.md:58-61, OR
- a flag defined in SKILL.md:103, OR
- a runtime artifact path with a clearly-specified producer step, OR
- a pre-existing entity (Wave 1.5, `--depth deep`, `--no-escalate`, etc.) that the Wave 1.6 work correctly references without redefining.

No reference points at a non-existent section, non-existent file, non-existent field, or non-existent flag. Bidirectional integrity confirmed across SKILL.md, refs/diagnosability-audit.md, refs/hypothesis-card-template.md, refs/report-template.md, refs/escalation-rubric.md.

**Phase 6 Step 6.3: PASS.**
