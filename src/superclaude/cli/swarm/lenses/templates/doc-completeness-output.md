# `doc-completeness-output` — Per-Worker Findings-Table Template

> Canonical Wave-2 worker output for the `doc-completeness` bundled lens
> (COMP-030 / R-055,
> `src/superclaude/cli/swarm/lenses/doc_completeness.py`). The lens
> binds to the shared `findings_table_v1` recipe
> (`src/superclaude/cli/swarm/recipes/findings_table_v1.py`); this
> template documents the canonical shape that recipe emits so the
> COMP-023 U-008 validator
> (`src/superclaude/cli/swarm/lenses/_validate.py::_check_file_refs`) can
> assert this path resolves, and so `tests/swarm/test_per_lens_templates.py`
> can pin `recipe_name == "findings_table_v1"` for this lens.

---

## Lens prompt → recipe column mapping

The worker is asked for a four-column markdown gap table:
`| Section | Gap kind | Issue | Suggested fix |`. The recipe collapses
that emission into the canonical 5-column shape below by positional
mapping (extra trailing cells join into `Action` rather than drop —
AC-011 preservation):

| Worker column   | Canonical column |
|-----------------|------------------|
| Section         | `Locator`        |
| Gap kind        | `Finding`        |
| Issue           | `Detail`         |
| Suggested fix   | `Action`         |

The `ID` column is auto-assigned by the recipe as `F-NN` (zero-padded,
sequential, body order — never reordered). Bundled emissions typically
classify `Gap kind` as one of `missing`, `unclear`, `stale`, or
`broken link`; the recipe does not normalise the label vocabulary
(AC-011 forbids silent coercion) — it passes the cell through
whitespace-collapsed.

## Canonical shape (what `findings_table_v1.render_markdown` emits)

```markdown
---
schema_version: "1.0"
tier: "T2-doc"
suspect: false
lens: "doc-completeness"
reviewer_model_id: "{reviewer_model_id}"
reviewer_model_label: "{reviewer_model_label}"
target: "{target}"
target_checksum: "{target_checksum}"
target_truncated: {target_truncated}
generated: "{generated}"
caller_label: "{caller_label}"
elapsed_ms: {elapsed_ms}
finding_count: {finding_count}
---

# T2-Findings Table (doc-completeness) — {slug}

## Findings

| ID | Locator | Finding | Detail | Action |
|----|---------|---------|--------|--------|
| F-01 | {locator} | {finding} | {detail} | {action} |
| ... | ... | ... | ... | ... |

## Notes
{notes}
```

When the worker yields no rows AND no `## Notes`, the recipe degrades
to a freeform-fallback Notes section (first
`findings_table_v1.FALLBACK_NOTES_CAP` chars of the body, whitespace
collapsed) and renders a single placeholder row of dashes so the
markdown table stays well-formed.

## Frontmatter placeholders (recipe-supplied)

| Placeholder | Owner | Type | Recipe source |
|-------------|-------|------|---------------|
| `{reviewer_model_id}` | dispatcher | YAML-quoted string | `args["model_id"]` |
| `{reviewer_model_label}` | dispatcher | YAML-quoted string | `args["model_label"]` |
| `{target}` | preflight | YAML-quoted abs path | `args["target"]` |
| `{target_checksum}` | preflight | YAML-quoted 12-hex sha256 | `args["target_checksum"]` |
| `{target_truncated}` | preflight | bare bool (`true`/`false`) | `args["target_truncated"]` |
| `{generated}` | normalizer | YAML-quoted ISO-8601 UTC | `args["generated"]` (else `iso_now()`) |
| `{caller_label}` | preflight | YAML-quoted string (may be empty) | `args["caller_label"]` |
| `{elapsed_ms}` | dispatch meta | bare int | `args["elapsed_ms"]` |
| `{finding_count}` | normalizer | bare int | `len(parse_findings_table(body))` |
| `{slug}` | normalizer | bare string | `splitext(basename(target))[0]` |

`schema_version`, `tier`, `suspect`, and `lens` are pinned by the
lens entry (`LensEntry.tier="T2-doc"`, `suspect=False`,
`name="doc-completeness"`) and emitted verbatim — the recipe does not
parameterise them on this lens.

## Row cell placeholders (one row per parsed finding)

| Placeholder | Cap (chars) | Normalization |
|-------------|-------------|---------------|
| `{locator}` | `CLAIM_CAP` (200) | whitespace-collapsed, hard-capped |
| `{finding}` | `CLAIM_CAP` (200) | whitespace-collapsed, hard-capped |
| `{detail}`  | `DETAIL_CAP` (200) | whitespace-collapsed, hard-capped |
| `{action}`  | `DETAIL_CAP` (200) | extra trailing cells joined with `" / "`; whitespace-collapsed; hard-capped |

## §7.4 salvage semantics

- `status == "parse_error"` and the body yields ≥1 row or non-empty
  notes → `NormalizedResult(salvaged=True)`; dispatcher promotes to
  `success` per FR-028.
- `status == "parse_error"` and the body yields neither → empty text +
  `error="no findings or notes"`; status stays `parse_error`.
- Empty raw body → empty text + `error="empty raw body"`.

## AC-011 boundary

The recipe MUST NOT score, dedupe, or reorder findings. Row order is
the worker body's row order; duplicate rows are emitted verbatim. This
template documents the shape, not a judging contract — the boundary
itself is enforced by `tests/swarm/test_recipe_no_judging.py` (T04.14).

## Provenance

- Recipe: `src/superclaude/cli/swarm/recipes/findings_table_v1.py`
  (`FindingsTableV1.normalize` + `render_markdown`).
- Lens:   `src/superclaude/cli/swarm/lenses/doc_completeness.py`
  (`recipe_name="findings_table_v1"`, `tier="T2-doc"`,
  `default_workers=3`, `suspect=False`).
- Fixture: `tests/swarm/fixtures/findings_table_v1/doc_completeness.raw.txt`.
- Spec anchors: merged-requirements §3.3 (lens registry), §4.1
  (template), §7.4 (parse-error salvage), §12 (template path pin),
  AC-011 (no-judging boundary).
