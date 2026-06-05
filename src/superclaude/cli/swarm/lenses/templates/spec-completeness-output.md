# `spec-completeness-output` — Per-Worker Verdict-Only Template

> Canonical Wave-2 worker output for the `spec-completeness` bundled
> lens (COMP-027 / R-052,
> `src/superclaude/cli/swarm/lenses/spec_completeness.py`). The lens
> binds to the `verdict_only_v1` recipe
> (`src/superclaude/cli/swarm/recipes/verdict_only_v1.py`); this
> template documents the canonical shape that recipe emits so the
> COMP-023 U-008 validator
> (`src/superclaude/cli/swarm/lenses/_validate.py::_check_file_refs`) can
> assert this path resolves, and so `tests/swarm/test_per_lens_templates.py`
> can pin `recipe_name == "verdict_only_v1"` for this lens.

---

## Lens prompt → recipe section mapping

The worker is asked for a gap table
(`| Section | Gap | Why it matters | Suggested addition |`) plus a
one-line completeness verdict. The recipe collapses that emission into
three canonical sections: `## Verdict` / `## Rationale` / `## Notes`.
The gap table is preserved verbatim inside the `## Notes` section
(folded from any of `## Notes` / `## Gaps` / `## Concerns` headings)
so the supporting body content is never lost — AC-011 preservation.

| Worker section            | Canonical section |
|---------------------------|-------------------|
| `## Verdict` (one-line)   | `## Verdict` + `## Rationale` (split on `—`, `--`, ` - `, or `:<space>`) |
| `## Gaps` table + commentary | folded into `## Notes` |
| `## Notes` (free-form)    | folded into `## Notes` |

### Verdict-label normalization

`VERDICT_ALIASES` maps worker emissions onto the canonical triple
`{"yes", "no", "uncertain"}`. For `spec-completeness` the common
synonyms are `complete` → `yes`, `incomplete` → `no`, and `partial`
→ `uncertain`. Unknown labels pass through whitespace-collapsed —
AC-011 forbids silent coercion onto the canonical set.

Confidence (a digit-run inside the verdict head zone) is clamped to
`[0, 100]` and appears on the rendered line as `<label> (<conf>)`.

## Canonical shape (what `verdict_only_v1.render_markdown` emits)

```markdown
---
schema_version: "1.0"
tier: "T2-spec"
suspect: false
lens: "spec-completeness"
reviewer_model_id: "{reviewer_model_id}"
reviewer_model_label: "{reviewer_model_label}"
target: "{target}"
target_checksum: "{target_checksum}"
target_truncated: {target_truncated}
generated: "{generated}"
caller_label: "{caller_label}"
elapsed_ms: {elapsed_ms}
verdict: "{verdict}"
verdict_confidence: "{verdict_confidence}"
---

# T2-Verdict (spec-completeness) — {slug}

## Verdict
{label} ({confidence})

## Rationale
{rationale}

## Notes
{notes}
```

When the worker yields no verdict AND no rationale AND no notes on a
`success` worker, the recipe degrades to a freeform-fallback: the
rationale becomes the first `RATIONALE_CAP` (300) chars of the body
whitespace-flattened, and the verdict label degrades to `uncertain`
so the rendered body stays well-formed.

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
| `{verdict}` | normalizer | YAML-quoted canonical label (`yes` / `no` / `uncertain` or alias-passthrough) | `parse_verdict(body)[0]` |
| `{verdict_confidence}` | normalizer | YAML-quoted digit-run (`0`–`100`) or qualitative passthrough | `parse_verdict(body)[1]` |
| `{slug}` | normalizer | bare string | `splitext(basename(target))[0]` |

`schema_version`, `tier`, `suspect`, and `lens` are pinned by the
lens entry (`LensEntry.tier="T2-spec"`, `suspect=False`,
`name="spec-completeness"`) and emitted verbatim.

## Section cell placeholders

| Placeholder    | Cap (chars)              | Normalization |
|----------------|--------------------------|---------------|
| `{label}`      | `VERDICT_LABEL_CAP` (32) | alias-mapped via `VERDICT_ALIASES` to `yes`/`no`/`uncertain`; unknown labels pass through whitespace-collapsed |
| `{confidence}` | digit-run clamped `[0,100]` | qualitative labels (`high`/`medium`/`low`) pass through; recipe does NOT classify (AC-011) |
| `{rationale}`  | `RATIONALE_CAP` (300)    | extracted from the Verdict-section tail after the separator; whitespace-collapsed |
| `{notes}`      | `NOTES_CAP` (600)        | folded from `## Notes` / `## Gaps` / `## Concerns` joined with `" | "`; whitespace-collapsed |

## §7.4 salvage semantics

- `status == "parse_error"` and the body yields ≥1 of:
  verdict label, rationale, or non-empty notes
  → `NormalizedResult(salvaged=True)`; dispatcher promotes to
  `success` per FR-028.
- `status == "parse_error"` and the body yields none of the above →
  empty text + `error="no verdict or notes"`; status stays
  `parse_error`.
- Empty raw body → empty text + `error="empty raw body"`.

## AC-011 boundary

The recipe MUST NOT score, dedupe, or reorder findings. The verdict
label is reformatted (alias-mapped), never compared; the rationale is
extracted verbatim; the supporting `## Gaps` table is preserved
verbatim inside `## Notes`. This template documents the shape, not a
judging contract — the boundary itself is enforced by
`tests/swarm/test_recipe_no_judging.py` (T04.14).

## Provenance

- Recipe: `src/superclaude/cli/swarm/recipes/verdict_only_v1.py`
  (`VerdictOnlyV1.normalize` + `render_markdown`).
- Lens:   `src/superclaude/cli/swarm/lenses/spec_completeness.py`
  (`recipe_name="verdict_only_v1"`, `tier="T2-spec"`,
  `default_workers=3`, `suspect=False`).
- Fixture: `tests/swarm/fixtures/verdict_only_v1/spec_completeness.raw.txt`.
- Spec anchors: merged-requirements §3.3 (lens registry), §4.1
  (template), §7.4 (parse-error salvage), §12 (template path pin),
  AC-011 (no-judging boundary).
