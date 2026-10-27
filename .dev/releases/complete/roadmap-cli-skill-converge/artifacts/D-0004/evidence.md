# D-0004 — Evidence: `sc-roadmap-protocol/refs/scoring.md` PRD-First Detection

| Field | Value |
|---|---|
| Task | T02.02 |
| Roadmap Item | R-004 |
| Drift Item | B-4 |
| Deliverable | D-0004 |
| Date | 2026-05-26 |
| Source File Edited | `src/superclaude/skills/sc-roadmap-protocol/refs/scoring.md` |
| CLI Reference | `detect_input_type()` (`src/superclaude/cli/roadmap/executor.py:73-210`) |
| Decision Posture | Option 1 (CLI-faithful re-derivation) — see `design-decision.md` row B-4 |
| Source Claim Status | PARTIAL (`verification.md:92-106`) — PRD-omission claim was REFUTED for "PRD section presence" but VERIFIED for "PRD scoring algorithm absence". This edit closes the verified gap. |

## Linkage

- **B-4 → D-0004.** `release-scope.md:25` lists B-4 as `"scoring.md stale CLI cross-reference"` with status PARTIAL. `verification.md:92-106` records the nuance: the file already contained a "PRD Supplementary Scoring" subsection (so a literal PRD-omission claim was REFUTED), but the **PRD scoring algorithm itself** — the 5-signal rule with threshold ≥5, evaluated before TDD detection — was not documented even though `executor.py:73-148` implements it (VERIFIED). `design-decision.md` row B-4 (`design-decision.md:34`) selected Option 1: re-derive scoring directly from `executor.py`, name the function, and document PRD-first detection.
- **D-0004** is the resulting source-file edit at `src/superclaude/skills/sc-roadmap-protocol/refs/scoring.md` plus this evidence record.

## Source-file parity check

CLI canonical detection from `src/superclaude/cli/roadmap/executor.py:73-210` (`detect_input_type`):

```
1. PRD scoring (lines 100-147)  ── checked FIRST
   - prd_score >= 5 → returns "prd"  (line 138)
   - Signals: type field +3, 12 PRD sections +1 each, user-story regex +2,
     JTBD regex +2, prd tag in frontmatter +2
   - Borderline warning: 3 <= prd_score <= 6

2. TDD scoring (lines 149-210)  ── checked SECOND, only when PRD fails
   - score >= 5 → returns "tdd"
   - Else → returns "spec"
```

Post-edit `scoring.md` structure (in file order):

| Section | Anchor | Status |
|---|---|---|
| Input-Type Detection Order | New header, before TDD section | ✅ Lists PRD-first → TDD-second → spec-fallback evaluation order, cites `executor.py:73-210` |
| PRD-First Detection Rule | New header, before TDD-Format Detection Rule | ✅ Names all 5 PRD signals with weights, threshold ≥5, borderline-warning band, cites `executor.py:100-147` |
| TDD-Format Detection Rule | Preserved (existing content + "Order note") | ✅ Body unchanged; new lead paragraph notes TDD scorer runs only when PRD fails; CLI cross-reference now cites `executor.py:149-210` (the TDD half of the function) |
| PRD Supplementary Scoring | Existing section, lightly amended | ✅ Lead sentence updated to reference auto-detection via `detect_input_type()` returning `"prd"` in addition to `--prd-file` |

## Acceptance criteria check (`phase-2-tasklist.md:99-104`)

- ✅ `refs/scoring.md` states that PRD detection is checked before TDD detection — see "Input-Type Detection Order" section (lists PRD first, TDD second) and the "Order note" lead paragraph of the TDD-Format Detection Rule subsection.
- ✅ `refs/scoring.md` names the PRD signal categories and threshold behavior listed in the source documents — all 5 PRD signals enumerated with weights (type field +3, 12 PRD sections +1 each, user-story regex +2, JTBD regex +2, prd tag +2), threshold ≥5, borderline-warning band `3 ≤ prd_score ≤ 6`, maximum attainable score, and override flag (`--input-type`).
- ✅ `refs/scoring.md` preserves the TDD detection reference after the PRD section and cites the CLI detection function — TDD-Format Detection Rule still appears in the file (4 signals unchanged), now with an "Order note" lead paragraph and a more specific CLI cross-reference (`executor.py:detect_input_type()` lines 149–210). The original CLI cross-reference at `refs/scoring.md:18` is updated rather than removed.
- ✅ Evidence at this path links B-4 → D-0004 and records the source claim's PARTIAL status (`verification.md:92-106`); see the "Source Claim Status" row of the header table and the "Linkage" section above.

## CLI behavior anchors cited in the edit

- `cli/roadmap/executor.py:73-210` — `detect_input_type` (full function — both PRD and TDD scoring).
- `cli/roadmap/executor.py:100-147` — PRD scoring block: signal list, threshold check, borderline warning band, return statement.
- `cli/roadmap/executor.py:149-210` — TDD scoring block (preserved cross-reference for the TDD rule).
- `cli/roadmap/executor.py:138` — `if prd_score >= 5: ... return "prd"` — the canonical PRD-first short-circuit.

## Reframed vs. preserved skill content

- **Preserved** (no semantic change):
  - The 4-signal TDD detection rule body (numbered headings, TDD-exclusive frontmatter fields, TDD section names, "Technical Design Document" type field).
  - The standard 5-factor complexity formula and worked example.
  - The 7-factor TDD complexity formula.
  - Template Compatibility Scoring and Persona Confidence Calculation sections.
  - Existing "PRD Supplementary Scoring" body — only the lead sentence is amended to cover auto-detection via `detect_input_type()` in addition to `--prd-file`.
- **Added** (new canonical content for B-4):
  - "Input-Type Detection Order" subsection establishing PRD → TDD → spec evaluation order.
  - "PRD-First Detection Rule" subsection enumerating the 5 PRD signals, threshold behavior, borderline-warning band, and CLI line-range citation.
  - "Order note" lead paragraph in the TDD-Format Detection Rule subsection noting it runs second.

## Sync follow-up (B-12)

This edit lives only at `src/superclaude/skills/sc-roadmap-protocol/refs/scoring.md`. A subsequent `make sync-dev` is required (and tracked under B-12 / Phase 5) before `.claude/skills/sc-roadmap-protocol/refs/scoring.md` and `/config/.claude/skills/sc-roadmap-protocol/refs/scoring.md` reflect the change. Per repo rules, `.claude/` mirrors are not staged or committed.
