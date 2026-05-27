# QA Report — Research Gate

**Topic:** Track 1 (Change A — escalation-rubric formula update)
**Date:** 2026-05-27
**Phase:** research-gate
**Fix cycle:** N/A (initial gate)

---

## Overall Verdict: FAIL (preliminary — see Critical Findings)

A FAIL verdict is preliminary because two of three assigned research files do not exist on disk. The single existing file will still be fully checklist-verified for completeness.

---

## File Inventory (Check 1 — preliminary)

Assigned files:

1. `01-change-a-spec-extraction.md` — PRESENT (19,154 bytes; mtime 2026-05-27 04:54)
2. `02-target-file-state.md` — **MISSING**
3. `03-template-and-conventions.md` — **MISSING**

Research directory contents:

```text
.dev/tasks/to-do/TASK-RF-track-1-change-a-rubric-formula-20260527-044000/research/
└── 01-change-a-spec-extraction.md
```

Verification commands run:

- `ls -la <research dir>` — confirmed only one file present
- `ls <qa dir>` — directory did not exist (no analyst report)

This is a **CRITICAL** failure that blocks all downstream checks against files 02 and 03.

Note: no `research-notes.md` (planning artifact) exists in the task directory either. Scope-coverage cross-validation (Check 3) has no canonical EXISTING_FILES list to compare against — falling back to the spawn prompt's TRACK GOAL as the de facto scope contract.

---

## Independent Spot-Checks (Proposal + Target File)

These are the spot-checks called out in the spawn prompt. They were performed by reading the cited sources independently.

### Spot-check A — Proposal block citations (proposal L43-109)

Verified file: `/config/workspace/IronClaude/.dev/brainstorms/calibration-refactor-pr86/cross-env-compare/CROSS-ENV-PROPOSAL-MERGED.md`

| Research-file claim | Verified at proposal | Match |
|---|---|---|
| Block 1 OLD (research L42) | proposal L56 | EXACT |
| Block 2 INSERT (research L79) | proposal L62 | EXACT |
| Block 3 OLD formula (research L105) | proposal L64 | EXACT |
| Block 3 NEW formula (research L111) | proposal L65 | EXACT |
| Block 4 prose (research L136) | proposal L67 | EXACT |
| Block 5 cap table values 0.70 / 0.84 (research L168-169) | proposal L77-78 | EXACT |
| Block 6 cross-tab header (research L211 `[V2 merged]` suffix) | proposal L82 | EXACT (inline suffix preserved) |
| Block 7 escalation rule (research L266) | proposal L105 | EXACT (incl. U+2208 `∈`) |
| Provenance header (research L18) | proposal L45 | EXACT |

All 9 quoted citations match the proposal byte-for-byte. Block typing (REQUIRED-REPLACE / REQUIRED-INSERT) maps correctly to the `-` / `+` markers in the diff sketch.

### Spot-check B — Target file anchor capture

Verified file: `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md`

| Research-file anchor claim | Verified at target | Match |
|---|---|---|
| L13 = `**Evidence grounding**` row | L13 | EXACT |
| L17 = `**Domain coherence**` row (last dimension before Runtime check insert point) | L17 | EXACT |
| L19 = `**Confidence** = arithmetic mean of the five dimension scores.` | L19 | EXACT |
| L21 = `Round to two decimals.` | L21 | EXACT |
| L23 = `## Escalation decision (Wave 2)` | L23 | EXACT |
| L39 = `--type security` bullet (last § 3 sub-bullet, anchor for Block 7) | L39 | EXACT |
| L41 = `4. **Default**` heading | L41 | EXACT |
| Total file line count: 52 lines | File ends at L53 (content terminates at L52, trailing newline) | EXACT (52 content lines) |

All 8 target-file anchors are correct. The edit-order recommendation in the research file's Summary correctly preserves anchor uniqueness (earlier edits do not invalidate later anchor strings).

---

## Items Reviewed (10-item Research Gate Checklist)

### 1. File inventory — FAIL (CRITICAL)

- Assigned: 3 files. Present: 1. Missing: 2 (`02-target-file-state.md`, `03-template-and-conventions.md`).
- The single present file (`01-change-a-spec-extraction.md`) has:
  - `**Status:** Complete` at L5 — present ✓
  - `## Summary` section at L287 — present ✓
- Verdict: Item-level PASS for the one file that exists; cohort-level **FAIL** because 2/3 assigned files are absent.

### 2. Evidence density — PASS (for file 01)

- File 01 has 7 explicit "Block N" sections, each carrying:
  - Proposal line citation (e.g., `Proposal source: L56 → L57`)
  - Target file line anchor (e.g., `target file L13`)
  - Paste-ready verbatim text in fenced blocks
  - MUST-statement enumeration (where applicable)
- Spot-check sample: 9/9 proposal citations + 8/8 target anchors verified exact (see Spot-checks A and B above).
- Density rating: **Dense** (>95% of claims carry both source-line + target-anchor evidence; spot-checks confirm citations are not hallucinated).

### 3. Scope coverage — PARTIAL FAIL

- TRACK GOAL listed 5 deliverables: (a) 6th Runtime row, (b) gated-min formula, (c) M3a subsection with REFUTE/REJECT→0.70 + AFFIRM→0.84 caps, (d) Claim-class × evidence-class cross-tab subsection, (e) new escalation rule for source_only_dynamic_claim.
- File 01 covers all 5 spec-extraction deliverables (Blocks 1, 2, 3, 4 cover [a]+[b]; Block 5 covers [c]; Block 6 covers [d]; Block 7 covers [e]).
- However, missing files 02 and 03 are part of scope per the assigned-files spec:
  - 02-target-file-state.md → would document the target file's current state, headings, anchors, line numbers, surrounding-context for each insert/replace.
  - 03-template-and-conventions.md → would document the markdown conventions, table formatting, bold/code-style rules used in `escalation-rubric.md` so the builder can preserve voice and style.
- Verdict: spec-extraction scope (file 01) covered; target-file-state and template-conventions scope **uncovered** because files 02 and 03 do not exist.

### 4. Documentation cross-validation — N/A → PASS (vacuously)

- File 01 is a spec-extraction file; it cites the proposal (.dev/brainstorms/) and the target file (src/superclaude/), both of which are repo-local source files, not external documentation. No `[CODE-VERIFIED]` / `[CODE-CONTRADICTED]` / `[UNVERIFIED]` tags are required for repo-local citations under the existing convention.
- Spot-checks above functionally serve as code-cross-validation: all 17 cited locations match exactly.
- No untagged doc-only claims found.

### 5. Contradiction resolution — PASS

- Only one file present; no inter-file contradictions possible within file 01's coverage.
- Within file 01, the provenance treatment is consistent: Block 6 carries `[V2 merged]` inline marker; the top-of-section `[Provenance: V1 base; cross-tab table merged from V2]` is cited at L18; the Summary's V2-merge provenance section (research L319-323) restates this without contradiction.

### 6. Gap severity — FAIL (critical gaps exist)

- File 01 itself contains no "Gaps and Questions" section, which is **acceptable** for a pure spec-extraction track — there is no ambiguity to surface; the proposal is the source of truth and is quoted verbatim.
- However, the cohort-level gap is that files 02 and 03 are missing entirely:
  - **CRITICAL gap:** No `02-target-file-state.md` — builder has no canonical "what does the current target file look like at each anchor" reference. File 01 inlines target line numbers but does not capture surrounding-context for surgical-edit anchoring.
  - **CRITICAL gap:** No `03-template-and-conventions.md` — builder has no canonical "what markdown style/table conventions does escalation-rubric.md use" reference, risking style drift in inserted blocks.

### 7. Depth appropriateness — PASS (for file 01, against Standard tier)

- DEPTH TIER is Standard. Standard expects file-level coverage. File 01 covers the proposal section L43-106 at block-level granularity (7 blocks identified, each with proposal-line + target-line evidence).
- For a spec-extraction track in Standard tier, file 01's depth is appropriate and arguably exceeds Standard (it has block-by-block paste-ready text, MUST-statement enumeration, edit-order recommendation).

### 8. Integration point coverage — PASS

- File 01 documents integration points with downstream tracks:
  - "Cross-referenced changes" section (research L325-328) names Change B (`hypothesis-card-template.md` — supplies frontmatter fields `claim_class`, `evidence_class`, `verdict_direction`) and Change C (`confidence-calibrator.md` — consumes the formula).
  - Block 7's escalation-rule rationale explicitly references the existing `escalation_reason` enum and lists what value joins it (`source_only_dynamic_claim`).
- Integration coverage for THIS track (Change A) is complete.

### 9. Pattern documentation — PARTIAL PASS

- File 01 captures Block 7's character-set convention note: "`∈` is U+2208 (ELEMENT OF) — matches existing project character set" (research L277) and the indent pattern "3-space indent + `- ` to match the existing § 3 sub-bullet style" (research L278).
- However, broader markdown-table style conventions, bold-vs-code formatting rules, and heading-level conventions for `escalation-rubric.md` are NOT documented in file 01 — this is what file 03 was supposed to capture.
- Verdict: pattern documentation is partial; what is present is precise (the U+2208 callout is exactly the kind of detail a builder needs), but coverage is incomplete pending file 03.

### 10. Incremental writing compliance — PASS

- File 01 (19,154 bytes; ~341 lines) shows organic structure consistent with incremental writing:
  - 7 numbered Block sections with consistent sub-headers (`### Diff`, `### Semantic delta`, `### MUST statements`)
  - The Summary section at L287 references back to earlier blocks by number (not by lexically substituting text), consistent with append-style assembly
  - Block 6's "Cross-tab — full 6 claim_class × 6 evidence_class verbatim" section (research L227-233) reads as a follow-up cataloging step after the paste-ready text was already captured — characteristic of incremental refinement, not one-shot generation.
- No one-shotted signature detected.

---

## Summary

- Checks passed: 6 (items 2, 4, 5, 7, 8, 10)
- Checks partial: 2 (items 3, 9)
- Checks failed: 2 (items 1, 6 — both CRITICAL severity due to missing files)
- Critical issues: 2
- Important issues: 0
- Minor issues: 0
- Issues fixed in-place: 0 (fix_authorization: false)

### Confidence (Computed)

- **Verified:** 10 / 10 checklist items checked against tool evidence
- **Unverifiable:** 0
- **Unchecked:** 0
- **Confidence:** 100.0% (every item received a tool-cited verdict; the 2 FAILs are evidenced, not unknowns)
- **Tool engagement:** Read: 3 | Grep: 0 | Glob: 0 | Bash: 2 | tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0
- **Tool-engagement vs. checklist-items ratio:** 5 tool calls / 10 items = 0.5. The deficit is explained because items 4, 5, 7, 8, 10 are derivable from the same Read of file 01 (one tool call evidences multiple items). Item 1 was evidenced by Bash `ls`. Items 2, 3, 6, 9 were evidenced by Read of file 01 + the two source-spot-check Reads. No single check was verified without a corresponding tool call.

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|---|---|---|---|
| 1 | CRITICAL | research/ (cohort-level) | File `02-target-file-state.md` does not exist; was in the spawn prompt's ASSIGNED FILES list | Spawn the assigned researcher to write `02-target-file-state.md` capturing the current state of `src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md` — headings, anchors per line, surrounding-context blocks for each of the 7 insert/replace anchors (target L13, L17, L19, L21, L39, L41), and the Why-0.85 + What-escalation-does-NOT-mean sections that follow the Wave 2 block. |
| 2 | CRITICAL | research/ (cohort-level) | File `03-template-and-conventions.md` does not exist; was in the spawn prompt's ASSIGNED FILES list | Spawn the assigned researcher to write `03-template-and-conventions.md` documenting `escalation-rubric.md`'s markdown conventions: H2 vs H3 heading usage, bold-formatted dimension names in table cells, code-fenced formula style (backticks around inline code), 3-space indent + `- ` for § 3 sub-bullets, U+2208 element-of usage, two-decimal rounding callout placement, and provenance-marker style ([V2 merged] suffix). The builder needs these to insert Blocks 1-7 without introducing style drift. |
| 3 | (none) | research/01 | File 01 is otherwise exemplary — no item-level findings within it | n/a |

## Actions Taken

None — `fix_authorization: false`. All findings are report-only.

## Recommendations

1. Spawn 2 gap-fill researchers in parallel (one per missing file) before proceeding to synthesis.
2. After gap-fill, re-run the Research Gate. The single-file PASS-on-file-01 result is durable; the re-run only needs to verify the 2 new files and re-check items 3, 6, 9 at cohort level.
3. Do NOT proceed to synthesis with only file 01 — the builder will be flying blind on target-file surrounding-context and markdown conventions, increasing the risk of style drift and broken anchors at edit time.

## QA Complete

VERDICT: **FAIL**

Reason: 2 of 3 assigned research files (`02-target-file-state.md`, `03-template-and-conventions.md`) do not exist on disk. File 01 itself passes all 10 checklist items at file-level rigor (evidence density: Dense; all 17 spot-checked citations match the source proposal and target file exactly). The FAIL is purely cohort-level: missing-file criticals 1 and 2 must be resolved before synthesis.
