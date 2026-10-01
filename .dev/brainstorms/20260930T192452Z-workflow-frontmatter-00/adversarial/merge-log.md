# Merge Log

## Metadata
- Base: Variant 1 `variant-1-opus-architect.md` (opus:architect)
- Incorporated from: Variant 2 `variant-2-sonnet-refactorer.md` (sonnet:refactorer)
- Plan: `refactor-plan.md`
- Executor: merge-executor
- Changes planned: 8
- Changes applied: 8
- Status: success
- Timestamp: 2026-09-30T19:42:00Z
- Output: `merged-output.md`

## Changes Applied

### Change #1: `version` is a constant `"1"`
- Status: applied
- Target: `## Decision` item 2; `## File edits` edit 2 `## Fill rules` block (`version` bullet); `## Fill rules` table row `version`; `## Risks` (old Risk 4); `## Out of scope`
- Before → after:
  - Decision 2: "`"1"`, or the previous integer + 1 when overwriting" → "`"1"` (same-slug runs overwrite in place, no resume — `input-parse.md:13`)". Rationale "only means something as a rewrite counter" → "the plan is always revision 1" (V2:18 wording).
  - Edit 2 fill bullet: "`"1"`. If `<run>/plan.md` already exists ... value + 1." → "`version`: `"1"`."
  - Table: Source "previous ... + 1" → "constant (same-slug runs overwrite in place, no resume)"; default `"1"`.
  - Risk 4 (version increment) deleted; old Risk 5 renumbered to Risk 4.
  - Out of scope: added "A `version` counter across runs." (V2:216).
  - Gate regex `^[1-9]\d*$` kept (C-002).
- Provenance tag: `Base (original, modified) — Change #1` on Decision, File edits, Fill rules, Risks, Out of scope

### Change #2: plugin mirror byte-equality in the guard test
- Status: applied
- Target: `## File edits` edit 4 (test body), edit 3 (plugin mirror), `## Risks` (old Risk 5, now Risk 4)
- Before → after:
  - Edit 4: appended the 3-line `plugin` / `read_bytes()` equality loop (V2:135-137) to the test body.
  - Edit 3: "Apply edits 1 and 2 verbatim, then confirm with `diff -r ...`" → "Apply edits 1 and 2 by copying the two edited `src/` files byte-for-byte; the guard test (edit 4) asserts equality (no make target syncs `plugins/superclaude/`, `Makefile:109,166`)."
  - Risk 4 mitigation: "a `diff -r` check is listed, and the new test pins the `src/` side" → cites the `read_bytes()` equality assert.
- Provenance tag: `Base (original, modified) — Change #2` on File edits and Risks

### Change #3: Checkpoint → last Task's acceptance criteria
- Status: applied
- Target: `## File edits` edit 1, Wave 2 "New" block, last bullet
- Before → after: "Phase Outputs and Checkpoint → that phase's task `Acceptance criteria:` bullets (never a separate verify task)" → "Phase Outputs → the task bodies that produce them; Phase Checkpoint → the `Acceptance criteria:` of that phase's last Task (never a separate verify task)". Inputs mapping and deps mapping kept unchanged.
- Provenance tag: `Base (original, modified) — Change #3` on File edits

### Change #4: priority never inferred
- Status: applied
- Target: edit 2 `## Fill rules` `priority` bullet; `## Fill rules` table `priority` row
- Before → after: appended "Never inferred from tone or urgency (template 00: DO NOT invent, `00:14`)." to the bullet; appended the same clause to the table Source cell.
- Provenance tag: `Base (original, modified) — Change #4` on File edits and Fill rules

### Change #5: placeholder check without the bare `[`-line clause
- Status: applied
- Target: edit 2 Schema-min "with" block, bullet 2
- Before → after: "or `[`-bracketed placeholder line" → "or any `[...]` placeholder text copied verbatim from template 00 (literal-match only; markdown links and reference definitions are not flagged)"
- Provenance tag: `Base (original, modified) — Change #5` on File edits

### Change #6: numbered/checkbox ban covers fenced code
- Status: applied
- Target: edit 2 Schema-min bullet 4; `## Gate changes` Schema-min bullet; `## /sc:implement compatibility` "No dialect leaks" bullet
- Before → after: appended "including inside fenced code blocks (`/sc:implement` has no fence exemption, `sc-implement-protocol/SKILL.md:63-64`)" at all three locations.
- Provenance tag: `Base (original, modified) — Change #6` on File edits, Gate changes, /sc:implement compatibility

### Change #7: `created_date` source
- Status: applied
- Target: `## Decision` item 2; edit 2 `## Fill rules` `created_date` bullet; `## Fill rules` table `created_date` row; `## Files unchanged` `refs/input-parse.md` bullet
- Before → after:
  - Decision 2: "run date (UTC, `YYYY-MM-DD`)" → "today's UTC date (`YYYY-MM-DD`) from the session's date context — not via Bash (`refs/input-parse.md:30` ...); never invented".
  - Fill bullet: "run date in UTC" → full plan text (session date context, not via Bash, never invent, missing/malformed → Wave 3 date check → `E-GATE`).
  - Table: "wall-clock run date, UTC" → "today's UTC date from the session's date context — not via Bash ...; never invented"; Default cell notes missing/malformed → `E-GATE`.
  - Files unchanged: added "The tool rule (`:30`: 'Bash: mkdir of output dir only') is unchanged, so `created_date` comes from the session's date context, not from Bash."
- Provenance tag: `Base (original, modified) — Change #7` on Decision, File edits, Files unchanged, Fill rules

### Change #8: open issue flagged by orchestrator (not debated)
- Status: applied
- Target: new `## Open issues (not debated)` section inserted before `## Out of scope`; `## Files unchanged` `refs/phase-templates.md` bullet
- Before → after: new section with open issue 1 (plan text verbatim, under a short bold title); phase-templates bullet marked "(pending open issue 1)".
- Provenance tag: `Orchestrator observation — Change #8 (not debated)` on the new section; `Base (original, modified) — Change #8` on Files unchanged

### Non-plan structural fix (no content change)
- The two edit 2 blocks that nest a ```` ```yaml ```` fence inside a ```` ```markdown ```` fence ("Replace lines 3-13" current and "with") had outer fences that the inner ```` ``` ```` closed early. Their outer fences were changed to four backticks (```` ````markdown ````) so the blocks render intact. The text inside is unchanged. This was needed to meet the "code fences balanced" requirement.

## Post-Merge Validation

### Structural integrity
- Heading hierarchy: PASS. H1 → H2 → H3, and H3 appears only under `## File edits`. No level gaps. `##` lines inside code fences are quoted file content, not document headings.
- Fences balanced: PASS. 22 fence lines, and a fence-state scan ends with no open fence.
- Provenance: PASS. All 10 document H2 sections carry a `<!-- Source: ... -->` comment right after the heading. The header block and the `merged_from` frontmatter key are present.
- Risks renumbered: PASS. The list runs 1-4 with no gaps.

### Internal references
- `Change #1`-`#8` (provenance comments): PASS. All 8 map to plan changes.
- `Decision 4` (Files unchanged): PASS. It resolves to Decision item 4.
- `edit 1`, `edit 4`, `edits 1 and 2`: PASS. They resolve to `### 1.`-`### 4.` under File edits.
- `Risk N`: PASS. No in-text Risk-number references remain, and nothing pointed at the deleted Risk 4 or the old Risk 5.
- `open issue 1`: PASS. It resolves to item 1 in `## Open issues (not debated)`.

### Contradiction re-scan
- No text says `version` increments per run: PASS. There are no matches for `+ 1`, `increment`, `rewrite counter` or `previous integer`.
- No text says Inputs → `Depends on`: PASS. No match. Inputs still map to named files and source sections, and only Phase deps map to `Depends on`.
- No bare "`[`-bracketed placeholder line" clause: PASS. No match.
- The numbered/checkbox ban mentions fenced code: PASS. It appears 3 times (Schema-min bullet, Gate changes, /sc:implement compatibility).
- `created_date` names the session date context: PASS. It appears 4 times (Decision 2, the fill bullet, the Fill rules table, Files unchanged), and no "wall-clock" wording remains.

## Summary
| Planned | Applied | Failed | Skipped |
|---------|---------|--------|---------|
| 8 | 8 | 0 | 0 |

One non-content structural fix was made (outer fences in two edit 2 blocks); see above. Nothing was escalated.
