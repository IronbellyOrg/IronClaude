# R5 Current-State Confirmation (current branch `refactor/roadmap-pipeline-r0-r1-rewrite`)

**Captured:** 2026-06-02 06:55

## Grep 1 — MD in `contracts.ID_PATTERNS`
Command: `grep -n "MD" src/superclaude/contracts/__init__.py | grep -i pattern`
Output: **`no MD in ID_PATTERNS`**
→ **ABSENT.** `ID_PATTERNS` has FR/NFR/SC/G/D only; no MD family. Research claim CONFIRMED.

## Grep 2 — MD handling in roadmap CLI
Command: `grep -rn "md_ids\|milestone\|M\d+-D" src/superclaude/cli/roadmap/`
Output: ~120 matches — **ALL are the English word "milestone"** in roadmap templates (`*.md.j2`), tool schemas (`*.schema.json`), `prompts.py`, `gates.py` (`_milestone_counts_positive`, `## M{N}:` section validation), `obligation_scanner.py`, `cosmetic_remediator.py`, `executor.py`. These are roadmap *content* conventions (milestone H2/H3 sections, `validation_milestones`/`work_milestones` frontmatter counts), **NOT** ID-family tokenizer support.
→ **`md_ids` token: ABSENT (0 matches).** **`M\d+-D` ID-pattern handling: ABSENT (0 matches).** The grep matched the noisy word "milestone" but no MD-family ID extraction/dedup/canonicalization code exists. Research claim CONFIRMED — the roadmap pipeline knows the *concept* of milestones (M{N}: section headings) but has no machinery to tokenize/canonicalize milestone-prefixed *deliverable IDs* like `M1-D01`.

## Grep 3 — Explicit non-references allowlist
Command: `grep -n "non_ref\|Explicit non-references" src/superclaude/cli/roadmap/structural_checkers.py`
Output: **`no allowlist subsystem`**
→ **ABSENT.** No `non_ref` allowlist. Research claim CONFIRMED.

## Conclusion
The current branch has **NO MD family** in the contracts SoT, **NO `md_ids`** anywhere, **NO MD-family ID tokenizer/canonicalizer**, and **NO Explicit-non-references allowlist subsystem**. All three premises from the research are confirmed against the live tree. This is the precondition for the Phase 2.3 reproduction (the bare-`D` pattern `D-?\d+` is the only thing that can match the `D01` tail of `M1-D01`).

## Tokenizer FP Probe (Step 2.2)

Command: `uv run python -c "from superclaude.cli.roadmap.spec_parser import extract_requirement_ids; print(extract_requirement_ids('Implements M1-D01, M1-D02, M2-D01 milestone deliverables.'))"`

Literal output:
```
{'D': ['D01', 'D02']}
```

**FP CONFIRMED at the tokenizer level.** Input contained THREE distinct milestone-scoped deliverable IDs (`M1-D01`, `M1-D02`, `M2-D01`). The tokenizer extracted only the bare-`D` tails and produced `{'D': ['D01', 'D02']}`:
- The `M{n}-` milestone prefix is entirely discarded — `M1-D01` and `M2-D01` (distinct deliverables in different milestones) both reduce to bare `D01` and **collide into a single token**.
- The result is filed under the `D` family, so any spec/roadmap using `M{n}-D{nn}` IDs has those IDs mis-read as bare-`D` requirement IDs — the precise mechanism behind the 51-HIGH `phantom_id` false-positive PR #111 set out to fix.
- No `MD` family key appears in the result (consistent with the contracts-SoT having no MD body). The word-boundary `\bD-?\d+\b` matches `D01` after the `-` in `M1-D01` exactly as the research predicted.
