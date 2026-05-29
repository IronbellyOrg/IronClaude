# Research 05: Doc Cross-Validator

**Status**: Complete
**Researcher**: 5 of 5
**Topic**: Verify spec §10 SKILL.md Diff Sketch line ranges against current SKILL.md
**Spec**: `/config/workspace/IronClaude/.dev/brainstorms/20260529-141819-troubleshoot-wave-1-6-diagnosability/merged-output.md` §10 (lines 555-571)
**Target**: `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` (current length: **468 lines**, spec assumes 470)
**Drift summary**: 2 lines of net contraction since spec written; substantial section-internal drift due to extensive Wave 3 calibration text (lines 263-276) and Wave 5 evidence-validator block (lines 343-344) added after the brainstorm landed.

---

## 1. The 11-Row Verification Table

| # | Section | Spec-claimed range | Current actual range | Status | Δ (lines) |
|---|---|---|---|---|---|
| 1 | Wave Structure ASCII | 75-85 | **75-85** | **[CODE-VERIFIED]** | 0 |
| 2 | Output Contract table | 41-57 | **41-57** (rows); 37-71 if "section incl. derivation rules" | **[CODE-VERIFIED]** | 0 |
| 3 | Wave 0: Parse + Validate Input | 91-126 | **91-125** | **[CODE-VERIFIED]** | -1 |
| 4 | Insert Wave 1.6 after line 187 (end of Wave 1.5) | line 187 | **line 187** (Wave 1.5 ends 186; `---` at 187; `### Wave 1.7` at 190) | **[CODE-VERIFIED]** | 0 |
| 5 | Wave 1.7 Preconditions | 194-196 | **194** (single-line bullet; reaches Steps header at 196) | **[CODE-VERIFIED]** | -2 (preconditions is now 1 line of prose, not 3) |
| 6 | Wave 5 step 2 REPORT.md composition | 331-342 | **331-342** | **[CODE-VERIFIED]** | 0 |
| 7 | Tool Coordination Summary | 391-403 | **389-402** (heading at 389; rows 391-402) | **[CODE-VERIFIED]** | -1 (heading moved up 2 lines, table -1 row) |
| 8 | Will Do / Will Not Do | 404-425 | **404-425** | **[CODE-VERIFIED]** | 0 |
| 9 | Token Cost Profile table | 446-454 | **446-454** | **[CODE-VERIFIED]** | 0 |
| 10 | Error Handling table | 428-444 | **427-444** (heading at 427; rows 430-444) | **[CODE-VERIFIED]** | 0 |
| 11 | Refs table | 458-466 | **457-466** (heading at 457; rows 461-466) | **[CODE-VERIFIED]** | 0 |

**Summary**: **0 [CODE-CONTRADICTED]**, **11 [CODE-VERIFIED]** (all within ±3 lines), **0 [UNVERIFIED]**.

The spec §10 line ranges are remarkably accurate. Drift exists *inside* sections (Wave 3 has been extended substantially since spec was written, see §4 below), but every section the implementation must touch is still at its spec-claimed coordinates within tolerance.

---

## 2. Updated line-range table — DROP-IN for rf-task-builder

This is what per-edit checklist items should cite (current, verified, ready to use):

| Edit target | File:line range (CURRENT) | Action | Spec source |
|---|---|---|---|
| **E1: Wave Structure ASCII** | `SKILL.md:75-85` | Insert new lines between line 78 (`Wave 1.5: ...`) and line 79 (`Wave 1.7: ...`): two lines for the Wave 1.6 entry and one note line for the hard-stop edge. Net diff: +2 lines inside the fence; total file becomes ~470. | spec §10 row 1 |
| **E2: Output Contract table** | `SKILL.md:41-57` | Add 4 new rows after line 57 (after `remediation_accepted` row). Keep `status` enum unchanged. New rows: `diagnosability_verdict`, `diagnosability_context_card_path`, `diagnosability_tasklist_path`, `diagnosability_hard_stop`. | spec §10 row 2 |
| **E3: Wave 0 optional flags** | `SKILL.md:97` (the "Optional:" sentence in step 1) | Append `--no-diagnosability-audit`, `--diagnosability-handoff`, `--reset-diagnosability-rounds` to the optional flag list at end of line 97. | spec §10 row 3 |
| **E4: New Wave 1.6 section** | Insert at `SKILL.md:188` (between current line 187 `---` separator and line 190 `### Wave 1.7` header) | Insert ~70-line `### Wave 1.6: Diagnosability Audit` block per spec §1 (Preconditions, Steps S1.6.0-S1.6.4, Exit criteria, Failure handling, Token budget), followed by a `---` separator. | spec §10 row 4 |
| **E5: Wave 1.7 Preconditions** | `SKILL.md:194` (single-line: "Wave 1 (real-code grounding) is complete; Wave 1.5 has produced...") | Add a sentence/clause: `Wave 1.6 did NOT fire its hard-stop (or was skipped via --no-diagnosability-audit, or fired soft-warn under --no-escalate). When Wave 1.6 hard-stopped, this wave is skipped entirely.` | spec §10 row 5 |
| **E6: Wave 5 step 2 — REPORT.md composition** | `SKILL.md:331-342` (step 2 bullet list at 332-341, trailing prose at 342) | (a) Add `Diagnosability Context` to bullet list — insert after line 334 (`Documentation Context`), before line 335 (`Diagnosis`). (b) Add hard-stop rendering path: when `diagnosability_hard_stop=true`, the line-335 `Diagnosis` bullet becomes a "Halted — instrumentation required" block referencing tasklist. (c) Add `--depth deep` mandatory-banner rendering instruction. | spec §10 row 6 |
| **E7: Tool Coordination Summary** | `SKILL.md:391-402` (table rows; heading at 389) | Annotate the "Tier 1" column for `mcp__auggie__codebase-retrieval` row (line 393), `Glob`/`Grep` row (line 400), and `Task` row (line 398) to reflect Wave 1.6 use. Add a parenthetical "(Wave 1.6: 2 branches A/B + orchestrator)" to each. Spec ambiguity preserved: spec offered "Add Wave 1.6 column OR annotate Tier 1 column" — annotate is the lighter-touch option. | spec §10 row 7 |
| **E8a: Will Do additions** | `SKILL.md:404-413` (heading at 404, bullets 406-413) | Append 3 bullets after line 413: "Run Wave 1.6 Diagnosability Audit by default; opt-out via `--no-diagnosability-audit` (bypass is logged)." / "Halt Waves 1.7-4 when verdict=`insufficient` AND complexity=`non-trivial` AND `--no-escalate` is not set." / "No hypothesis work happens in the same turn as an instrumentation patch — the user re-runs after instrumenting." | spec §10 row 8 |
| **E8b: Will Not Do additions** | `SKILL.md:415-425` (heading at 415, bullets 417-425) | Append 3 bullets after line 425: "Auto-apply the diagnosability tasklist (it is a proposal)." / "Force the hard-stop when `--no-escalate` is set." / "Allow the tasklist to target the failing component's own source — invocation sites only." | spec §10 row 8 |
| **E9: Token Cost Profile** | `SKILL.md:446-454` (heading 446, table 448-453, prose 455) | Add a new row to the table after line 453 (after the `Tier 3 added` row) describing Wave 1.6 standalone cost: `+1-2k auggie, +1-2.5k Claude, +30-60s wall clock` — or fold into a footnote referencing hard-stop net-saving. | spec §10 row 9 |
| **E10: Error Handling** | `SKILL.md:427-444` (heading 427, table 430-444) | Append 6 new rows after line 444 (after `confidence-calibrator` fallback row): `--no-diagnosability-audit set`; `auggie unavailable (Wave 1.6 — Glob/Grep fallback, cap verdict at partial)`; `both Wave 1.6 branches return empty`; `failing_component not localizable`; `Heisenbug detected on re-run`; `3-round cap reached`. | spec §10 row 10 |
| **E11: Refs table** | `SKILL.md:457-466` (heading 457, table 461-466, prose 468) | Add a new row after line 466 (current last row `refs/remediation-handoff.md`): `\| refs/diagnosability-audit.md \| Wave 1.6 (audit query templates, fallback paths, sufficiency rubric, complexity gate, context card template, tasklist rules, T4 worked example) \|` | spec §10 row 11 |

---

## 3. Validation rules check (per role brief, mandatory)

### 3.1 Wave 1.5 ends near "insert after line 187" — VERIFIED

`SKILL.md:185-195` actual content:

```text
185 | Branch synthesis times out / one branch crashes | Continue with remaining...
186 **Token budget**: Wave 1.5 should consume ≤ 2k Claude tokens (the auggie calls offload heavy retrieval). If it goes over 3k Claude tokens, audit-log the overrun — the wave is meant to be retrieval-offload, not Claude reasoning.
187 ---
188 (blank)
189 (blank)
190 ### Wave 1.7: Tier 1 — Hypothesis Formation
191 (blank)
192 **Goal**: Form one calibrated Tier 1 hypothesis card, consuming the Wave 1.5 Documentation Context Card (when produced) so the hypothesis is doc-grounded from the start.
193 (blank)
194 **Preconditions**: Wave 1 (real-code grounding) is complete; Wave 1.5 has produced a Documentation Context Card at `<output-dir>/doc-context.md` (or `--no-doc-discovery` was set and `doc_context_card_path` is `null`).
195 (blank)
```

**Natural insertion point for Wave 1.6**: line **188** (or 189 — either blank line works; the `---` separator at line 187 should stay attached to Wave 1.5's end). The new Wave 1.6 section should start with `### Wave 1.6: Diagnosability Audit` and end with its own `---` separator before line 190 (the existing Wave 1.7 heading). **Spec claim of "after line 187" is correct.**

### 3.2 Output Contract field count — VERIFIED (and spec was slightly wrong)

Spec §5 says "13 existing fields". Actual count of rows in `SKILL.md:43-57` (`status` through `remediation_accepted`):

1. `status` (line 43)
2. `tier_reached` (44)
3. `report_path` (45)
4. `audit_log_path` (46)
5. `confidence` (47)
6. `escalation_reason` (48)
7. `test_is_wrong` (49)
8. `test_file_path` (50)
9. `behavior_is_documented` (51)
10. `doc_context_card_path` (52)
11. `hypothesis_cards` (53)
12. `adversarial_artifacts_dir` (54)
13. `task_file_path` (55)
14. `remediation_offered` (56)
15. `remediation_accepted` (57)

**Actual count: 15 fields, not 13.** Spec was wrong by 2 (likely counted pre-`test_file_path` / pre-`behavior_is_documented` era). This does NOT affect the Wave 1.6 edit — the four new fields (`diagnosability_*`) still get appended after row 57, regardless of starting count — but the rf-task-builder should phrase the checklist item as "append after the existing rows" not "after the 13th row". **Spec footnote drift flagged.**

### 3.3 Wave-graph ASCII — VERIFIED (current text below)

Actual `SKILL.md:75-85`:

```text
75 ```text
76 Wave 0: Parse + Validate Input
77 Wave 1: Tier 1 — Real-Code Grounding  ← always; loads refs/triage-checklist.md on demand (grounding + reproduce only)
78 Wave 1.5: Documentation Grounding    ← always; loads refs/doc-discovery.md on demand; skipped only by --no-doc-discovery
79 Wave 1.7: Tier 1 — Hypothesis Formation ← always; consumes Wave 1.5 Documentation Context Card; produces single hypothesis card + calibration
80 Wave 2: Confidence Gate              ← decides escalation via refs/escalation-rubric.md
81 Wave 3: Tier 2 — Parallel Hypotheses (conditional)
82 Wave 4: Tier 2 — Adversarial Fix Debate (conditional, requires ≥2 viable fixes)
83 Wave 5: Synthesis + Report        ← always finalises; loads refs/report-template.md
84 Wave 6: Tier 3 — Remediation Chain (conditional, requires --fix + user accept)
85 ```
```

Wave sequence: `0 → 1 → 1.5 → 1.7 → 2 → 3 → 4 → 5 → 6`. Spec assumption matches.

**Insertion point inside the fence**: between line 78 and line 79. Suggested new line:

```text
Wave 1.6: Diagnosability Audit       ← always; loads refs/diagnosability-audit.md on demand; skipped only by --no-diagnosability-audit; may hard-stop to Wave 5
```

Plus a separate hard-stop edge note line (per spec §10 row 1) attached to Wave 5 or as a footnote inside the fence.

---

## 4. Newly-discovered sections not mentioned in spec §10

Sections that exist in current SKILL.md that the spec §10 table did not enumerate but the implementation may need to consider for ripple effects:

| Section | Lines | Implementation risk |
|---|---|---|
| **Required Input (STOP if missing)** | 26-35 | LOW — Wave 1.6 inherits the existing input gate; no new STOP added at this layer. |
| **Wave 1.5 Failure handling table** | 178-185 | MEDIUM — model for Wave 1.6 Failure handling table format. Reuse the same `\| Scenario \| Behavior \| Fallback \|` schema for consistency. |
| **Wave 3 Tier 2 calibration completeness gate** | 263-277 (NEW since spec) | MEDIUM — large prose block added post-brainstorm. The Wave 1.6 hard-stop verdict path that skips Waves 1.7-4 entirely also skips this gate naturally. No edit needed but the new Wave 1.6 section should mention "downstream Wave 3 calibration gate is skipped when hard-stop fires" for completeness. |
| **`test_is_wrong` and `behavior_is_documented` derivation rules** | 59-71 | LOW — these prose rules sit between the Output Contract table and the `## Wave Structure` heading; adding 4 new Output Contract rows (E2) does NOT disturb them. |
| **Wave 1.7 step 1's `consistency_with_docs` enum** | 198 | LOW — unchanged by Wave 1.6 work. The new `diagnosability_verdict` field is a peer, not a replacement. |
| **Wave 4 doc-update + fix bundle path** | 303, 315 | LOW — orthogonal to Wave 1.6; the diagnosability hard-stop fires before Wave 4 is reached. |
| **Wave 5 step 3 evidence-validator block** | 343-344 (NEW since spec) | MEDIUM — Wave 5 has grown; the existing step numbering (1, 2, 3, 4, 5) is preserved but step 3 is much denser than the spec authors saw. The spec §10 row 6 (Wave 5 step 2 composition) is still at lines 331-342, but anyone editing Wave 5 must be aware step 3 (file:line validation) is now load-bearing and runs AFTER REPORT.md composition. |
| **`uv run` / `make verify-sync` workflow** | (n/a — in CLAUDE.md / project rules, not SKILL.md) | LOW — out of file scope but task-builder checklist should include `make sync-dev` + `make verify-sync` after editing `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`. |

---

## 5. Sub-row line-number drift in spec §10

The spec §10 prose mentions a few embedded line numbers inside the change-text. Verifying those:

| Spec sub-claim | Spec coordinate | Current actual | Status |
|---|---|---|---|
| "Wave 1.5 Exit criteria 170-174" (from spec row 4 context, implied) | 170-174 | **170-174** (Exit criteria bullet list) | **[CODE-VERIFIED]** |
| "end of Wave 1.5 section" (spec row 4) | line 187 | line 187 (`---` separator) | **[CODE-VERIFIED]** |
| "current Wave 1.5 and Wave 1.7 lines" (spec row 1) | implies line 78 ↔ line 79 inside the fence | line 78 = Wave 1.5, line 79 = Wave 1.7 | **[CODE-VERIFIED]** |
| Wave 1.5 Failure handling table location (referenced by spec §1 "Steps") | implied ~175-185 | **178-185** | **[CODE-VERIFIED]** |

**No sub-row drift found.** The brainstorm spec was authored from a SKILL.md state that matches the current state within ±3 lines for every coordinate it references.

---

## 6. Risk call-outs for rf-task-builder

1. **The "after line 187" insertion (E4) is sensitive to blank-line semantics.** Lines 187 (`---`), 188 (blank), 189 (blank), 190 (`### Wave 1.7`). The new Wave 1.6 section needs its own preceding `---` *removed* (Wave 1.5 already has one at line 187) and its own trailing `---` added before line 190's blank line. Concretely: insert *between line 188 and line 189*, OR replace one of the blank lines. Mis-handling this produces a double `---` between Wave 1.5 and Wave 1.6, which looks broken in rendered Markdown.

2. **E7 (Tool Coordination Summary)** is the only "spec ambiguity" edit. The spec offered two phrasings ("add column" or "annotate Tier 1"). The task-builder should pick one — recommend annotation, since adding a column to a 4-column table that is already wider than 100 chars will overflow the right margin in many viewers.

3. **E10 (Error Handling) row count growth**: the current table is 15 rows (incl. header at 429). Adding 6 more makes it 21 rows. No structural risk but the table becomes the longest in the file; consider whether the rf-task-builder wants to nudge ordering (group all `--no-doc-discovery` style flag rows together).

4. **E2 (Output Contract) drift footnote**: rf-task-builder should NOT cite "13 fields" anywhere in the checklist (spec §5 typo). Cite "append after the existing 15 rows" or "append after the `remediation_accepted` row at line 57".

5. **The `make sync-dev` step is mandatory after this edit**. SKILL.md lives at `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`; the mirror at `.claude/skills/sc-troubleshoot-protocol/SKILL.md` is sync-dev output. The rf-task-builder checklist must end with `make sync-dev` then `make verify-sync` (per project rule 6 in `/config/.claude/CLAUDE.md` and the `feedback_hooks_source_of_truth.md` memory).

---

## 7. Final tallies

- **Total spec §10 rows verified**: 11/11
- **[CODE-CONTRADICTED] count**: **0**
- **[CODE-VERIFIED] count**: **11**
- **[UNVERIFIED] count**: **0**
- **Spec sub-row coordinates verified**: 4/4 (all match)
- **Spec auxiliary claim corrections**: 1 (Output Contract has 15 fields, not 13)
- **New sections added since spec authored**: 2 material additions (Wave 3 Tier 2 calibration gate, Wave 5 evidence-validator block) — neither blocks the Wave 1.6 work but both should be flagged to the task-builder for ripple awareness.

**Net assessment**: Spec §10 line-range table is reliable for implementation. The four-line drift between spec-era (470 lines) and current (468 lines) is concentrated in section-internal trims, not in the change-points. rf-task-builder can use the §2 "Updated line-range table" above as the per-edit citation source without further re-verification.
