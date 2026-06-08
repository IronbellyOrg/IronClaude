# `troubleshoot-hypothesis-output` — Per-Worker Hypothesis-Table Template

> Canonical Wave-2 worker output for the `troubleshoot-hypothesis`
> bundled lens (COMP-029 / R-054,
> `src/superclaude/cli/swarm/lenses/troubleshoot_hypothesis.py`). The
> lens binds to the `hypothesis_table_v1` recipe
> (`src/superclaude/cli/swarm/recipes/hypothesis_table_v1.py`); this
> template documents the canonical shape that recipe emits so the
> COMP-023 U-008 validator
> (`src/superclaude/cli/swarm/lenses/_validate.py::_check_file_refs`) can
> assert this path resolves, and so `tests/swarm/test_per_lens_templates.py`
> can pin `recipe_name == "hypothesis_table_v1"` for this lens.

---

## Lens prompt → recipe column mapping

The worker is asked for a ranked hypothesis table; models in practice
emit 4-, 5-, or 6-column variants. The recipe tail-anchors confidence
and next-step and joins middle cells into evidence so over-wide
emissions are preserved (AC-011):

| Worker emission                                                | Canonical column |
|----------------------------------------------------------------|------------------|
| cell 1 (Cause / Hypothesis)                                    | `Cause`          |
| cell 2 (Supporting evidence)                                   | `Evidence`       |
| cell 3 (Falsifying evidence) — width ≥ 5, joined with `" | "`  | `Evidence`       |
| penultimate cell (Confidence)                                  | `Confidence`     |
| final cell (Next probe / Next step)                            | `Next Step`      |

The `ID` column is auto-assigned by the recipe as `H-NN` (zero-padded,
sequential, body order — model-emitted likelihood ranking preserved,
never re-sorted). `troubleshoot-hypothesis` ships with
`default_workers=4` (the only built-in besides `edge-case-hunt` to
override the default of 3 per COMP-029) so the fan-out raises
hypothesis diversity; the recipe shape is identical regardless of
worker count.

## Canonical shape (what `hypothesis_table_v1.render_markdown` emits)

```markdown
---
schema_version: "1.0"
tier: "T2-tshoot"
suspect: false
lens: "troubleshoot-hypothesis"
reviewer_model_id: "{reviewer_model_id}"
reviewer_model_label: "{reviewer_model_label}"
target: "{target}"
target_checksum: "{target_checksum}"
target_truncated: {target_truncated}
generated: "{generated}"
caller_label: "{caller_label}"
elapsed_ms: {elapsed_ms}
hypothesis_count: {hypothesis_count}
---

# T2-Hypothesis Table (troubleshoot-hypothesis) — {slug}

## Hypotheses

| ID | Cause | Evidence | Confidence | Next Step |
|----|-------|----------|------------|-----------|
| H-01 | {cause} | {evidence} | {confidence} | {next_step} |
| ... | ... | ... | ... | ... |

## Notes
{notes}
```

When the worker yields no rows AND no `## Notes`, the recipe degrades
to a freeform-fallback Notes section (first
`hypothesis_table_v1.FALLBACK_NOTES_CAP` chars of the body, whitespace
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
| `{hypothesis_count}` | normalizer | bare int | `len(parse_hypothesis_table(body))` |
| `{slug}` | normalizer | bare string | `splitext(basename(target))[0]` |

`schema_version`, `tier`, `suspect`, and `lens` are pinned by the
lens entry (`LensEntry.tier="T2-tshoot"`, `suspect=False`,
`name="troubleshoot-hypothesis"`) and emitted verbatim.

## Row cell placeholders (one row per parsed hypothesis)

| Placeholder    | Cap (chars)        | Normalization |
|----------------|--------------------|---------------|
| `{cause}`      | `CAUSE_CAP` (240)  | whitespace-collapsed, hard-capped |
| `{evidence}`   | `EVIDENCE_CAP` (320) | for width ≥ 5: middle cells joined with `" | "`; whitespace-collapsed; hard-capped |
| `{confidence}` | (digit-run clamped to `[0, 100]`) | `parse_confidence`: first digit-run is clamped; qualitative labels (`high`/`medium`/`low`) pass through whitespace-collapsed — the recipe does NOT score them (AC-011) |
| `{next_step}`  | `NEXT_STEP_CAP` (240) | whitespace-collapsed, hard-capped |

## §7.4 salvage semantics

- `status == "parse_error"` and the body yields ≥1 row or non-empty
  notes → `NormalizedResult(salvaged=True)`; dispatcher promotes to
  `success` per FR-028.
- `status == "parse_error"` and the body yields neither → empty text +
  `error="no hypotheses or notes"`; status stays `parse_error`.
- Empty raw body → empty text + `error="empty raw body"`.

## AC-011 boundary

The recipe MUST NOT score, dedupe, or reorder hypotheses. Row order is
the worker body's row order (so model-emitted likelihood ranking is
preserved verbatim); duplicate rows are emitted verbatim. Confidence
cells are reformatted (digit-run extracted + clamped), never compared.
This template documents the shape, not a judging contract — the
boundary itself is enforced by `tests/swarm/test_recipe_no_judging.py`
(T04.14).

## Provenance

- Recipe: `src/superclaude/cli/swarm/recipes/hypothesis_table_v1.py`
  (`HypothesisTableV1.normalize` + `render_markdown`).
- Lens:   `src/superclaude/cli/swarm/lenses/troubleshoot_hypothesis.py`
  (`recipe_name="hypothesis_table_v1"`, `tier="T2-tshoot"`,
  `default_workers=4`, `suspect=False`).
- Fixture: `tests/swarm/fixtures/hypothesis_table_v1/troubleshoot_hypothesis.raw.txt`.
- Spec anchors: merged-requirements §3.3 (lens registry,
  `default_workers=4` override), §4.1 (template), §7.4 (parse-error
  salvage), §12 (template path pin), AC-011 (no-judging boundary).
