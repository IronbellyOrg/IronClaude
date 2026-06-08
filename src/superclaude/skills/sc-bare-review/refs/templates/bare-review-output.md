# `bare-review-output` — Compressed-Markdown Per-Reviewer Template

> Canonical Wave-2 output template for the `bare-review-v1` recipe
> (`src/superclaude/cli/swarm/recipes/bare_review_v1.py`) and the
> `bare-review` bundled lens (`src/superclaude/cli/swarm/lenses/bare_review.py`).
> Pinned by `merged-requirements.compressed.md` §12 ("The compressed-markdown
> template lives in `bare_review_v1.py` recipe + `refs/templates/bare-review-output.md`").
> Validator U-008 (T02.16) asserts this path resolves; `BareReviewV1.normalize`
> emits a byte-identical body when fed the placeholders documented below.

---

## Shape

```markdown
---
schema_version: "1.0"
tier: "T2"
suspect: true
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

# T2-Bare Review — {slug}

## Findings

| ID | Sev | Claim | Cite | SelfConf |
|----|-----|-------|------|----------|
| F-01 | {sev} | {claim} | {cite} | {conf} |
| ... | ... | ... | ... | ... |

## Verdict
{verdict}

## Notes
{notes}
```

---

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
| `{finding_count}` | normalizer | bare int | `len(parse_findings(body))` |
| `{slug}` | normalizer | bare string | `splitext(basename(target))[0]` |

`schema_version`, `tier`, and `suspect` are pinned constants (AC-1.9, AC-1.10) and
are emitted verbatim by `BareReviewV1.render_markdown`; the recipe does not
parameterise them.

## Findings-row placeholders (one row per parsed finding)

| Placeholder | Domain | Normalization |
|-------------|--------|---------------|
| `{sev}` | `crit` / `high` / `med` / `low` / `nit` | `normalize_sev` — case-insensitive alias map; unknown → `med`. |
| `{claim}` | ≤120 char string, no newlines | Truncated to 120 chars; newlines collapsed to spaces. |
| `{cite}` | `file:line` or literal `none` | `normalize_cite` — empty / `n/a` / `-` → `none`. |
| `{conf}` | integer 0-100 (or empty string) | `parse_conf` — first digit run, clamped to `[0, 100]`. |

Row IDs are emitted sequentially by the recipe as `F-01`, `F-02`, …, `F-NN`
(zero-padded to width 2). They are NOT preserved verbatim from raw output —
the recipe re-numbers in table order to keep `F-NN` references stable across
salvage promotions.

## Section placeholders

| Placeholder | Cap | Normalization | Fallback |
|-------------|-----|---------------|----------|
| `{verdict}` | 300 chars | `extract_section(body, "Verdict", 300)` (whitespace-flattened). | When the body yields neither findings nor a verdict on a `success` worker, falls back to `body[:300]` flattened, else the literal `(no structured findings returned)`. |
| `{notes}` | 200 chars | `extract_section(body, "Notes", 200)`; entire `## Notes` block omitted when empty. | (None — section is omitted, not stubbed.) |

When `args["status"] == "parse_error"` and the body yields a finding OR a
verdict, the recipe sets `salvaged=True` (§7.4 promotion). When the body yields
neither, the recipe returns an empty result with `salvaged=False` and the
dispatcher retains the raw file for triage.

---

## AC-011 boundary

The recipe MUST NOT score, dedupe, or reorder findings. Row order is preserved
from `parse_findings` (which reads top-to-bottom). Duplicate rows are emitted
verbatim. This template documents the shape, not a judging contract — the
boundary itself is enforced by `tests/swarm/test_recipe_no_judging.py`
(T04.14).

## Render-test contract

A render check against any fixture under `tests/swarm/fixtures/bare_review_v1/`
must:

1. Invoke `BareReviewV1().normalize(raw_output, args)` with a deterministic
   `args["generated"]`.
2. Assert every literal section header (`# T2-Bare Review —`, `## Findings`,
   `## Verdict`, plus `## Notes` iff the fixture supplies notes) appears in the
   rendered text in the documented order.
3. Assert the frontmatter contains each placeholder key from the table above
   (`schema_version:`, `tier:`, `suspect:`, …, `finding_count:`) — i.e. no
   key is unbound.
4. Assert the findings-table column header row matches verbatim:
   `| ID | Sev | Claim | Cite | SelfConf |`.

See `tests/swarm/test_recipe_bare_review.py` for the byte-identity parity
gate against the legacy `t2_normalize.py` script (TEST-003 / M8 gate); the
render test above is a lighter shape check kept in sync with this template.

---

## Provenance

- Parent skill template: `src/superclaude/skills/sc-bare-review/refs/output-template.md`
  (kept in place for the legacy bash/Python pipeline under `scripts/`).
- Wave-2 recipe: `src/superclaude/cli/swarm/recipes/bare_review_v1.py`
  (`BareReviewV1.render_markdown` emits this exact shape).
- Spec anchors: merged-requirements §4.1 (template), §4.2 (field semantics),
  §7.4 (parse-error salvage), §12 (template path pin).
