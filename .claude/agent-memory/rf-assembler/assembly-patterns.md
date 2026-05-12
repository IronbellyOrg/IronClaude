---
name: assembly-patterns
description: Patterns and lessons from completed assembly sessions in the IronClaude PRD/TDD/Spec pipeline investigation
type: feedback
---

## Edit Tool Matching Requirement

The Edit tool requires the `old_string` to match exactly as it appears in the file, including trailing characters and whitespace. When appending large sections to an existing file, use `Bash` with `cat >>` (heredoc with ENDSECTIONS delimiter) rather than Edit, to avoid match failures on the last line of the file.

**Why:** On a 524-line file, an Edit attempting to match the last table row failed because trailing whitespace or newline differences prevented the match. Bash append succeeded immediately.

**How to apply:** For sections being appended to the end of a file (not inserting in the middle), always prefer `cat >>` via Bash over Edit tool.

## Large File Reading (>10,000 tokens)

When a synthesis file exceeds 10,000 tokens, the Read tool rejects it. Use offset/limit parameters to read in chunks of ~120 lines. Plan reads as: offset 0 limit 120, then offset 120 limit 120, etc.

**How to apply:** Pre-split reading into chunks before starting. A 465-line file at ~22 tokens/line = ~10,000 tokens -- right at the limit. When unsure, start with limit 120.

## Incremental Write Protocol — Hybrid Approach

For this report type (10 sections from 4 synth files):
1. Write header with Write tool (creates file)
2. Read synth file in chunks
3. For early sections (not at end of file): use Edit tool to append content after a known anchor string
4. For later sections (appending to end of file): use Bash `cat >>` heredoc to avoid Edit matching failures

**Update (2026-04-02):** For large multi-domain release specs (1600+ lines, 9 source files, 14 sections), the Edit tool approach worked well throughout. The key is matching on the last distinct line before the insertion point (e.g., a source citation + separator). Each Edit appended 200-400 lines successfully when the old_string anchor was unique.

## Section-to-Synth File Mapping (IronClaude Research Reports)

Standard 10-section research report with variable synth file count:

**3-file layout** (observed 2026-04-03):
- Sections 1-2 (Problem Statement, Current State): synth-01
- Sections 3-7 (Target State, Gap Analysis, External Research, Options, Recommendation): synth-02
- Sections 8-10 (Implementation Plan, Open Questions, Evidence Trail): synth-03

**6-file layout** (earlier standard):
- Sections 1-2: synth-01
- Sections 3-4: synth-02
- Section 5: synth-03
- Sections 6-7: synth-04
- Section 8: synth-05
- Sections 9-10: synth-06

Section 5 is frequently N/A for codebase-scoped investigations (no web research files).

**How to apply:** Always read the spawn prompt's section assignments rather than assuming a fixed mapping.

## Multi-Domain Release Spec Pattern (v3.7-task-unified-v2)

For release specs consolidating 3+ domain analyses + source files into 14-section unified document:
- Read ALL input files upfront in parallel (9 files read in 2 waves of 6+3)
- Write header first, then use Edit tool to append each section after the previous section's closing anchor
- Anchor pattern: `**Source**: [citation]\n\n---\n`
- Assembly order: Overview -> Problem Statement -> Solution Architecture -> Implementation Plan (largest, contains all task details) -> Cross-Domain Dependencies -> Data Model -> File Inventory -> Rollout -> Risk -> Success Metrics -> Test Strategy -> Config -> Open Questions -> Appendices
- Cross-domain conflict map is critical (Section 5) -- files modified by multiple domains need resolution ordering
- Preserve all T-numbered tasks and F-numbered features in full detail per assembly rules

## Table of Contents Generation

Generate the ToC immediately after the header (before section content). Use actual section numbers that match the template. The ToC in the header area is written once at the start; no need to update it after adding sections since the section headings are predetermined by the output format.

## Cross-Consistency Check Commands

After assembly, run these bash checks:
```bash
# Verify all sections present
grep -n "^## [0-9]" report.md

# Check for placeholders
grep -n "TODO\|TBD\|PLACEHOLDER\|\[MISSING" report.md

# Count T-task section headers (for checkpoint enforcement spec)
grep -oP '##### T\d{2}\.\d{2}' report.md | sort -u

# Count feature references (for TUI spec)
grep -oP 'F\d{1,2}[:\s]' report.md | sort -u
```

## Assembly with QA Context Notes (2026-04-04)

When the assembly prompt includes a "NOTE FROM QA" about cross-section reading context (e.g., implementation plan should be read in context of a recommendation's phased approach), add a blockquote **Reading Context** note at the top of the affected section. This preserves QA's guidance without altering the synthesis content.

**How to apply:** Use `> **Reading Context (per Section N):**` format. Keep it factual -- map plan phases to option labels from the recommendation.

## Edit Tool for All Sections Works (2026-04-04 confirmation)

For an 846-line 10-section report assembled from 6 synth files, using Edit tool for ALL section appends worked without issues. No need for Bash `cat >>` fallback when the old_string anchor is the last unique line of content added. The pattern: match on the final table row or text line of the previous section, append new section content after it.
