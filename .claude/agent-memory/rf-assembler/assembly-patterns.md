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

**How to apply:** Pre-split reading into chunks before starting. A 465-line file at ~22 tokens/line = ~10,000 tokens — right at the limit. When unsure, start with limit 120.

## Incremental Write Protocol — Hybrid Approach

For this report type (10 sections from 4 synth files):
1. Write header with Write tool (creates file)
2. Read synth file in chunks
3. For early sections (not at end of file): use Edit tool to append content after a known anchor string
4. For later sections (appending to end of file): use Bash `cat >>` heredoc to avoid Edit matching failures

## Section-to-Synth File Mapping (IronClaude Research Reports)

Standard 10-section research report with 6 synthesis files:
- Sections 1-2 (Problem Statement, Current State): synth-01
- Sections 3-4 (Target State, Gap Analysis): synth-02
- Section 5 (External Research Findings): synth-03
- Sections 6-7 (Options Analysis, Recommendation): synth-04
- Section 8 (Implementation Plan): synth-05
- Sections 9-10 (Open Questions, Evidence Trail): synth-06

Section 5 is frequently N/A for codebase-scoped investigations (no web research files).

Earlier assemblies used 4 synth files with sections 5-8 merged into synth-03. The 6-file layout is the current standard.

## Table of Contents Generation

Generate the ToC immediately after the header (before section content). Use actual section numbers that match the template. The ToC in the header area is written once at the start; no need to update it after adding sections since the section headings are predetermined by the output format.

## Cross-Consistency Check Commands

After assembly, run these bash checks:
```bash
# Verify all 10 sections present
grep -n "^## [0-9]\+" report.md

# Check for placeholders (TBD/TODO/PLACEHOLDER are OK if they are content references, not blanks)
grep -n "\[TODO\]\|\[TBD\]\|PLACEHOLDER" report.md

# Verify all synthesis files listed in Evidence Trail
grep -c "synth-0[1-4]" report.md
```
