# Discovery 03 — REPORT.md `calibration_status` Insertion Strategy

**Source:** `src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md`
**Date:** 2026-05-27

## Independently verified line ranges

Verified by reading the file in full (196 lines):

| Section | Line range | Confirmation |
|---------|-----------|--------------|
| Embedded fenced template block | L7-L141 | Opens with ` ```markdown ` at L7; closes with ` ``` ` at L141 |
| Header fields block | L8-L21 | `# Troubleshoot Report` at L8; `**Date**: <ISO 8601>` at L21 |
| Summary section | L25-L29 | `## Summary` at L25 |
| Documentation Context | L31-L41 | `## Documentation Context` at L31 |
| Diagnosis | L43-L51 | `## Diagnosis` at L43 |
| Evidence | L53-L61 | `## Evidence` at L53 |
| Proposed Fix | L63-L77 | `## Proposed Fix` at L63 |
| Alternative Fixes Considered | L79-L88 | `## Alternative Fixes Considered` at L79 |
| Risk + Rollback | L90-L98 | `## Risk + Rollback` at L90 |
| Follow-up tasks | L100-L110 | `## Follow-up tasks` at L100 |
| **Grounding Gaps** | **L112-L122** | `## Grounding Gaps` at L112; "If there are no gaps, write 'None.'" at L122 |
| Next Steps | L124-L132 | `## Next Steps` at L124 |
| **Audit** | **L134-L140** | `## Audit` at L134; closing list item at L140 |
| Trailing rules and enforcement blocks | L143-L196 | Rendering rules + Test-is-wrong rule + Behavior-is-documented rule, all OUTSIDE the fenced template block |

**Note on research-02 §7 line citation:** Research-02 references "141 lines" — this is the line where the fenced template block CLOSES, not the file's total length. The file is 196 lines total; the trailing 55 lines hold rendering rules and the Test-is-wrong / Behavior-is-documented enforcement blocks. Phase 1 discovery (this file) confirms by reading the full 196 lines.

## Three insertion-point candidates

| Option | Approach | Pro | Con |
|--------|----------|-----|-----|
| 1 | New top-level header field after `**Status**` (e.g., `**Calibration status**: <ok\|partial\|failed_to_calibrate>`) | Machine-readable, one line | Only one value for whole report; loses per-card granularity; schema change |
| 2 | Extend per-card listing in Audit section (L134-140) | Per-card fidelity; structured | Schema change to free-form section |
| 3 | Prose line appended to Grounding Gaps (L112-122) | **Zero schema change**; section already accepts prose entries | Less structured for downstream parsing |

## Chosen strategy: **Option 3 — Grounding Gaps prose line + optional Confidence header note**

**Rationale:**
- Zero schema change to `refs/report-template.md` — Change F is purely orchestrator behavior; the template stays intact.
- Grounding Gaps section is **already prose-accepting** — the existing entries at L114-121 are bullet-point prose, exact format match.
- The Grounding Gaps tone already covers force-degrade-like situations (e.g., "Hypothesis card from `quality-engineer` cited line 88 of test_foo.py but that file is only 60 lines long — citation dropped" — L118 — has the same "card-from-X had-degraded-treatment" structure).

The **optional Confidence header note** makes the degradation observable at the header level without changing the field's semantics:
- Existing header: `**Confidence**: <0.0–1.0>` (L13)
- Augmented when force-degraded: `**Confidence**: 0.65 (force-degraded — see Grounding Gaps)`

The parenthetical is human-readable, does NOT change the numeric extraction (a parser would still match `\*\*Confidence\*\*:\s+([\d.]+)`), and points the reader to Grounding Gaps for the details.

## Exact phrasing for the Grounding Gaps prose line

When any Tier 2 card is force-degraded:

> `Hypothesis card from <agent> could not be calibrated after one retry — confidence force-degraded to min(self_reported, 0.65); calibration_status: failed_to_calibrate.`

This matches:
- The existing Grounding Gaps tone (declarative single-sentence prose ending in a period).
- The spec's literal `min(self_reported, 0.65)` math.
- The spec's literal `calibration_status: failed_to_calibrate` annotation.
- The "card from `<agent>`" idiom already used at L118 of the template.

If multiple cards were force-degraded, one prose line per card is appended (consistent with the existing bullet-point style — each gap is its own bullet).

## Schema change for `refs/report-template.md`

**None required for Change F itself.**

A follow-up could optionally extend the Grounding Gaps examples block (L114-121) to add the new failure-mode example as a fifth bullet. This is a documentation polish, not a load-bearing requirement, and is OUT OF SCOPE for Change F.

## Confirmation

Independently verified line ranges by reading the full 196-line template (not just copied from research-02 §7). The chosen phrasing uses verbatim spec terminology (`min(self_reported, 0.65)`, `calibration_status: failed_to_calibrate`) and matches the existing Grounding Gaps tone (declarative prose, single sentence per gap).
