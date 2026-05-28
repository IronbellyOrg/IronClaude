# Discovery 01 — Hypothesis Card Self-Reported Confidence Field

**Source:** `src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md`
**Date:** 2026-05-27

## Field name

**`Self-reported confidence`** (under the `## Confidence` section header).

## Verbatim definition from the template

- **Section header (L58 of template):** `## Confidence`
- **Placeholder line (L60):** `Self-reported confidence: <0.0–1.0>`
- **Annotative line (L62):** `The skill will re-grade this against the rubric. The agent's score is a signal, not the final number.`
- **Per-dimension self-assessment** (L64-70) follows separately — these are NOT the self-reported confidence; they are per-dimension scores feeding the rubric.

## Worked-example rendering (illustrative — L147-149 of template)

```
## Confidence

0.92
```

The worked example renders the field as `## Confidence` (section header) followed by a blank line and then a bare numeric on the next line, NOT the `Self-reported confidence: 0.92` literal. The placeholder form (L60) and the worked-example form (L147-149) BOTH coexist in the same template — the template's placeholder uses the explicit prose-prefixed format, but the worked example shows the bare-numeric rendering an agent may emit.

## Expected value type

- **Range:** `[0.0, 1.0]` (per the placeholder `<0.0–1.0>`)
- **Format:** parseable float (the worked example `0.92` confirms decimal numeric)
- **Cap rule (L91):** cards with `claim_class: runtime_behavior` AND `evidence_class ∈ {source_static, doc_static, none}` MUST self-cap their confidence at `0.65` in the per-dimension self-assessment and state the cap in the rationale. This is a separate constraint from Change F's force-degrade floor.

## Recommendation for the inserted gate subsection

The gate's force-degrade Step 3 must reference the field unambiguously. Recommended phrasing for the inserted Change F text:

> "...the card's self-reported confidence (the numeric immediately under the `## Confidence` section header — per the hypothesis-card template, the `Self-reported confidence: <0.0–1.0>` line; in the worked-example rendering, the bare numeric on the line following the section header)."

This phrasing covers BOTH the placeholder form and the worked-example form so the orchestrator's parser is unambiguous regardless of which rendering the agent emitted.

## Handling of missing / malformed values

Per research-02 §9 (Force-Degrade Math):

| `self_reported` state | Treatment |
|-----------------------|-----------|
| Missing / null | Default to `0.0` (most pessimistic safe value); annotate `self_reported: missing` in audit |
| Non-numeric (parse error) | Default to `0.0`; annotate `self_reported: non-numeric` in audit |
| `> 1.0` (malformed) | Clamp to `1.0` first, then apply `min(1.0, 0.65) = 0.65`; annotate clamp in audit |
| `< 0.0` (malformed) | Clamp to `0.0` first; result is `0.0`; annotate clamp in audit |
| In range `[0.0, 1.0]` | Apply `min(self_reported, 0.65)` directly |

The inserted gate subsection MUST encode all four edge cases in the Step 3 (force-degrade) clause.

## Confirmation

The template defines the self-reported confidence field. No fabrication — verbatim lines cited from the actual template at L58, L60, L62, L91, L147-149.
