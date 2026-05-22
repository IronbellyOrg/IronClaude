# Research: Template & Examples

**Topic type:** Template & Examples
**Scope:** MDTM Template 02 (Complex Task) structure, recent task folder examples in `.dev/tasks/done/`
**Status:** Complete
**Date:** 2026-05-20

---

## MDTM Template 02 — Path & Status

- **Path**: `.claude/templates/workflow/02_mdtm_template_complex_task.md`
- **Confirmed present** via directory listing at the start of this skill's execution.
- **PART 1**: Task Building Instructions — defines rules A-K (granularity, self-contained items, evidence-based, etc.) + L (template-02-specific patterns).
- **PART 2**: Task File Structure — the actual frontmatter + sections shape the builder writes.

## Key Template 02 rules relevant to this task

- **Rule A3 (Complete Granular Breakdown)**: every file / component gets its own item. For this task: each of the 4 edits (A/B/C/D) gets its own checklist item — do NOT batch as "apply all gates.py edits".
- **Rule A4 (Iterative Process Structure)**: phases reflect natural dependency ordering, with explicit gates between phases.
- **Rule B2 (Self-contained items)**: each item must include Context + Action + Output + Verification + Completion gate. Do NOT use "see above" or "as described in previous phase".
- **Frontmatter fields** (required): `id`, `title`, `status`, `created_date`. Recommended: `type`, `priority`, `complexity`, `tags`, `description`, `template_schema_doc`, `related_docs`.
- **Acceptance Criteria format**: `- [ ]` or `- ✅` style; `Verify: ...` prefix encouraged for verification clauses.

## Recent task folder examples (referenced)

Listed under `.dev/tasks/done/`:

- `TASK-RF-20260325-001/` — example with full research/qa/synthesis tree
- `TASK-RF-20260325-cli-tdd/` — CLI test-driven task; similar shape to this task (small-scope Python edits + pytest verification)
- `TASK-RF-20260326-e2e-modified/` — e2e modifications

The current task's closest shape match is the CLI-TDD style: small set of Python source edits + pytest verification + final lint check.

## Effective phase pattern for "small edit + new test + verify" jobs

Mapped to the 4 phases proposed in SUGGESTED_PHASES of research-notes.md:

1. **Phase 1 — Preparation**:
   - Item 1.1: Read all three source files to bind exact current strings (gates.py, test_gates.py, prompts.py for cross-check). Required by Edit tool semantics — file must be Read before Edit.
   - Single item.
2. **Phase 2 — Source edits to gates.py**:
   - Item 2.1: Apply Edit A — rewrite `_RESEARCH_REQUIRED_SECTIONS` list literal.
   - Item 2.2: Apply Edit B — widen the regex in `_check_suggested_phases_detail`.
   - Two items, sequential (both touch gates.py; order doesn't strictly matter but consistent ordering aids review).
3. **Phase 3 — Test edits & creation**:
   - Item 3.1: Apply Edit C — rewrite `TestCheckResearchNotesSections` fixture in `test_gates.py`.
   - Item 3.2: Apply Edit D — Write the new file `tests/cli/prd/test_research_notes_roundtrip.py`.
   - Two items, sequential.
4. **Phase 4 — Verification & completion**:
   - Item 4.1: Run `uv run pytest tests/cli/prd/test_gates.py tests/cli/prd/test_research_notes_roundtrip.py -v` — must pass.
   - Item 4.2: Run `uv run pytest tests/cli/prd/ -v` — full PRD test suite, no regressions.
   - Item 4.3: Run `make lint` — must pass.
   - Item 4.4: Update frontmatter status to "🟢 Done", set updated_date. (Completion item INSIDE Phase 4 — anti-orphaning rule.)
   - Four items.

Total: ~9 checklist items across 4 phases. Comfortably within Quick-tier bounds (≥3, ≤40).

## Self-containment evidence anchors

For each item that applies an edit, the Action field embeds:

- The exact `old_string` to find (with enough surrounding context to disambiguate).
- The exact `new_string` to replace it with.
- The file path.

This way the `/task` executor can apply each edit without referring back to the research files. Per template Rule B2, items are self-contained.

## What NOT to do (avoiding common task-file failure modes)

- **Do NOT** create batch items like "edit gates.py" — each edit is its own item.
- **Do NOT** reference `research/01-file-inventory.md:NN` from inside the task file's Action fields — embed the verbatim strings instead (B2 self-containment).
- **Do NOT** spawn QA agents inside this task file's phases — at Quick tier with FINAL_ONLY QA, the verification phase is sufficient (pytest + lint). PER_PHASE QA would be over-engineering for 4 edits.
- **Do NOT** add a git-commit item — the user hasn't asked for one, and CLAUDE.md says "NEVER commit changes unless the user explicitly asks you to."
- **Do NOT** modify `prompts.py` or `SKILL.md` — out of scope per the debate verdict.

## Summary

Template 02 + 4-phase structure + ~9 items, with per-edit granularity and verbatim `old_string`/`new_string` embedded in each Action field. Verification phase uses `uv run pytest` and `make lint` per CLAUDE.md project conventions. Anti-orphaning compliance: status-update item lives in Phase 4 (the final phase), not in a separate Post-Completion section.
