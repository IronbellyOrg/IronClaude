# Change C — 8-Edit Anchor Inventory

**Target file:** `src/superclaude/agents/confidence-calibrator.md` (118 lines)
**Ordering source:** research/02-target-file-state.md Section 6 (conservative 8-Edit sequence)
**Replacement text source:** research/01-change-c-spec-extraction.md (verbatim diff sketches)
**Status:** Inventory complete, ready for Steps 2.2–2.9

---

## Edit 1 — (a) INSERT `## Claim-class handling` between L27 and L29

**Old anchor (verbatim L27–L29, 3 lines including blank L28):**

```
**Spot-check evidence citations.** Do NOT trust the card's quoted snippets without Reading the cited files. "Evidence grounding" can only be scored honestly if you've actually verified what's there.

## Safety Constraint
```

**Replacement source:** research/01 L177–L181 (verbatim subsection body).
**Expected uniqueness:** EXACTLY 1 match. The `## Safety Constraint` heading is unique in the file; the L27 sentence "Spot-check evidence citations" is also unique.

---

## Edit 2 — (b) REPLACE Responsibilities item #1 (5 → 6 dimensions)

**Old anchor (verbatim L49–L50, 2 lines for uniqueness):**

```
1. **Read the rubric** at `rubric_path`. Note the 5 dimensions: Evidence grounding, Symptom coverage, Reproducibility fit, Fix directness, Domain coherence.
2. **Read the card** at `card_path`.
```

**Replacement source:** research/01 L51 (new item #1 verbatim) + L50 unchanged item #2.
**Expected uniqueness:** EXACTLY 1 match. The string "5 dimensions" + the listed names uniquely identifies L49.

---

## Edit 3 — (c)+(d) combined: INSERT #2a (claim_class defaults) and #3a (WebFetch URL detection)

**Old anchor (verbatim L50–L52, 3 lines):**

```
2. **Read the card** at `card_path`.
3. **Spot-check the evidence**: for each `file:line` cited in the card, Read the file at that range and verify the snippet matches. This is essential to scoring "Evidence grounding" honestly. If a citation does not match, mark it in the Notes section and let that drive the Evidence grounding score.
4. **Score each dimension** 0.0 / 0.5 / 1.0 per the rubric's anchor language. Cite the specific card content (or absence thereof) that drove the score.
```

**Replacement source:** research/01 L64 (item #2a verbatim) and L81 (item #3a verbatim). Preserve items #2, #3, #4 byte-exact.
**Expected uniqueness:** EXACTLY 1 match. The 3-line slice is unique because it contains both the "Spot-check the evidence" sentence and item #4's "Score each dimension" opening — only one place in the file has this combination.

---

## Edit 4 — (e)+(f)+(g) combined: REPLACE #4, REPLACE #5, INSERT #5a

**Old anchor (verbatim L52–L54, 3 lines — CRITICAL: U+00A7 `§` on L54 MUST be preserved byte-exact):**

```
4. **Score each dimension** 0.0 / 0.5 / 1.0 per the rubric's anchor language. Cite the specific card content (or absence thereof) that drove the score.
5. **Compute the arithmetic mean**, rounded to 2 decimals.
6. **Apply the escalation decision rules** (rubric § Escalation Decision, in order) using the score and the `flags_context`. Return the verdict (`STOP` or `ESCALATE`) and the matching `escalation_reason`.
```

**Replacement source:** research/01 L100 (new #4 verbatim), L120 (new #5 verbatim with gated-min formula), L137 (new #5a verbatim with verdict-direction caps). L54 (item #6) preserved BYTE-EXACT including the `§` character (Edit 5 will modify it separately).
**Expected uniqueness:** EXACTLY 1 match. "Compute the arithmetic mean" is unique in the file.

---

## Edit 5 — (h) REPLACE Responsibilities item #6 (extend escalation_reason allowed-value set)

**Old anchor (verbatim L54, single line — contains U+00A7 `§` character):**

```
6. **Apply the escalation decision rules** (rubric § Escalation Decision, in order) using the score and the `flags_context`. Return the verdict (`STOP` or `ESCALATE`) and the matching `escalation_reason`.
```

**Replacement source:** research/01 L157 (new item #6 verbatim — preserves prefix through "escalation_reason" + appends the `source_only_dynamic_claim` sentence). The `§` character is preserved byte-for-byte in the replacement.
**Expected uniqueness:** EXACTLY 1 match. "Apply the escalation decision rules" appears only once in the file (the `## Escalation recommendation` template section uses different wording).

---

## Edit 6 — (i) INSERT Runtime check row in per-dimension table

**Old anchor (verbatim L70–L71, 2 lines inside the fenced ` ```markdown ` block at L58):**

```
| Evidence grounding | 1.0 / 0.5 / 0.0 | <one-line citing what in the card supports this> |
| Symptom coverage | ... | ... |
```

**Replacement source:** research/01 L213 (new Runtime check row verbatim with `(claim_class, evidence_class) cross-tab` cell). Preserves L70 and L71 byte-exact, inserts the new row between them.
**Expected uniqueness:** EXACTLY 1 match. Both rows appear once inside the only fenced code block.

---

## Edit 7 — (j) INSERT `## Stage-2 trace (REQUIRED)` subsection (7-row table)

**Old anchor (verbatim L74–L76, 3 lines including blank L75, inside fenced block):**

```
| Domain coherence | ... | ... |

## Confidence
```

**Replacement source:** research/01 L233–L243 (full Stage-2 trace subsection verbatim — heading with literal `(REQUIRED)` suffix, 7-row pipe-table with header + separator + 7 data rows in order: arithmetic_mean(all_six) → gate_M1 → gate_M2 → gated_min → verdict_cap → **calibrated** → spot_check_unverifiable).
**Expected uniqueness:** EXACTLY 1 match. "Domain coherence" row + blank + `## Confidence` is unique inside the fence.
**Fence safety:** New content contains only pipe-tables and H2 headings — NO triple-backticks. Fence at L58/L93 remains intact.

---

## Edit 8 — (k)+(l) combined: REPLACE Self-reported bullet, INSERT Formula applied bullet

**Old anchor (verbatim L78–L80, 3 lines inside fenced block):**

```
- **Self-reported (in card)**: <X.XX>
- **Calibrated (this report)**: <Y.YY>
- **Delta**: <signed difference, and a one-line read on why it differs>
```

**Replacement source:** research/01 L276 (new Self-reported bullet with em-dash U+2014 clause "— read but NOT used as input to your score (independence instruction)") + L291 (new Formula applied bullet with literal `min(mean(all_six), evidence_grounding + 0.30, runtime_check + 0.30)` formula). Calibrated bullet (L79) and Delta bullet (L80) preserved byte-exact.
**Expected uniqueness:** EXACTLY 1 match. The 3-bullet slice is unique inside the fence.

---

## Summary

| Edit | Operations | Anchor line span | New material source |
|------|-----------|------------------|---------------------|
| 1 | (a) | L27–L29 | research/01 L177–L181 |
| 2 | (b) | L49–L50 | research/01 L51 |
| 3 | (c)+(d) | L50–L52 | research/01 L64, L81 |
| 4 | (e)+(f)+(g) | L52–L54 | research/01 L100, L120, L137 |
| 5 | (h) | L54 | research/01 L157 |
| 6 | (i) | L70–L71 | research/01 L213 |
| 7 | (j) | L74–L76 | research/01 L233–L243 |
| 8 | (k)+(l) | L78–L80 | research/01 L276, L291 |

**Total:** 8 Edit operations apply 12 surgical changes (5 REPLACE + 7 INSERT). Target file grows from 118 → ~140–150 lines.

**Critical unicode preservation:** Edit 4 and Edit 5 anchors include U+00A7 `§` on L54; Edit 8 replacement includes em-dash U+2014 in the new Self-reported clause.
