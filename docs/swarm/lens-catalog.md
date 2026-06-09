# MultiModelSwarm — Lens & Recipe Catalog

A **lens** is a named review intent. It bundles a system/user prompt, a default worker
count, a normalization **recipe**, an output template, and a downstream hand-off command.
The `--lens NAME` shortcut expands these defaults into a full JobSpec so you don't author
one by hand.

A **recipe** takes one worker's raw Markdown and normalizes it into a canonical shape.
**Recipes never judge, score, dedupe, or reorder** (AC-011) — they reshape, salvage on
parse error, and preserve content. Cross-worker comparison is the downstream skill's job
(that's what the hand-off command is for).

Source of truth: `cli/swarm/lenses/` and `cli/swarm/recipes/`. Validate the registry any
time with `uv run superclaude swarm validate-lenses`.

---

## The 7 bundled lenses

All default to a 4000-line target cap. Worker counts and recipes differ by intent.

| Lens | Workers | Recipe | Stability | Tier | Suspect | Hands off to |
|---|---:|---|---|---|:---:|---|
| [`bare-review`](#bare-review) | 3 | `bare-review-v1` | **stable** | T2 | ✅ | `/sc:adversarial --compare {compare_files} --suspect-source {suspect_files}` |
| [`refactor-find`](#refactor-find) | 3 | `findings_table_v1` | experimental | T2-code | — | `/sc:code-review --apply {compare_files}` |
| [`edge-case-hunt`](#edge-case-hunt) | 4 | `findings_table_v1` | experimental | T2-edge | — | `/sc:adversarial --compare {compare_files}` |
| [`spec-completeness`](#spec-completeness) | 3 | `verdict_only_v1` | experimental | T2-spec | — | `/sc:reflect --merge {compare_files}` |
| [`feasibility-probe`](#feasibility-probe) | 3 | `verdict_only_v1` | experimental | T2-feas | — | `/sc:research --extend {compare_files}` |
| [`troubleshoot-hypothesis`](#troubleshoot-hypothesis) | 4 | `hypothesis_table_v1` | experimental | T2-tshoot | — | `/sc:troubleshoot --merge-hypotheses {compare_files}` |
| [`doc-completeness`](#doc-completeness) | 3 | `findings_table_v1` | experimental | T2-doc | — | `/sc:document --apply {compare_files}` |

> Only `bare-review` is `stable`; the rest are `experimental` (interfaces may shift).
> Only `bare-review` is `suspect=true` — see [What "suspect" means](#what-suspect-means).

### bare-review

Unscaffolded native-instinct code review (ports the `sc-bare-review` skill). Workers
surface concrete findings with `file:line` citations and flag high-confidence
**suspect-source** files. Recipe `bare-review-v1` → findings table
`| ID | Sev | Claim | Cite | SelfConf |` + Verdict + Notes. Hands off to `/sc:adversarial`
with both `{compare_files}` and `{suspect_files}`.

### refactor-find

The smallest cleanups that improve correctness, readability, or efficiency. Recipe
`findings_table_v1` → `| ID | Locator | Finding | Detail | Action |`. Hands off to
`/sc:code-review`.

### edge-case-hunt

Inputs/states that break the target (boundary, off-by-one, concurrency, error paths).
**4 workers** for broader search. Recipe `findings_table_v1`. Hands off to
`/sc:adversarial`.

### spec-completeness

Gaps and under-specified sections in a specification. Recipe `verdict_only_v1` →
`## Verdict` (`yes`/`no`/`uncertain`) + `## Rationale` + `## Notes`. Hands off to
`/sc:reflect`.

### feasibility-probe

Whether a proposed approach would actually work; risks, unknowns, verdict. Recipe
`verdict_only_v1`. Hands off to `/sc:research`.

### troubleshoot-hypothesis

Given a failure/symptom, ranked root-cause hypotheses with supporting + falsifying
evidence. **4 workers.** Recipe `hypothesis_table_v1` →
`| ID | Cause | Evidence | Confidence | Next Step |`. Hands off to `/sc:troubleshoot`.

### doc-completeness

Missing, unclear, or out-of-date documentation content. Recipe `findings_table_v1`.
Hands off to `/sc:document`.

### custom (the 8th entry)

The escape hatch — **not** validated by `validate-lenses` and has no registry defaults.
Its prompt body flows in from `--custom-prompt-dir` at preflight (FR-021). Use it with
`--auto-inject-guard` when migrating legacy prompts — see
[User Guide §9](user-guide.md#9-prompt-injection-guard--custom-prompts).

---

## The 6 recipes

All implement `normalize(raw_output, args) -> NormalizedResult` and are **normalize-only**.
The `NormalizedResult` carries `text`, a `salvaged` flag (drives the parse-error →
success promotion), and an optional `error`.

| Recipe | Canonical output | Bound to lens(es) |
|---|---|---|
| `bare-review-v1` | Findings table `\| ID \| Sev \| Claim \| Cite \| SelfConf \|` + Verdict + Notes; auto `F-NN` IDs; severity/confidence reformatted (never compared). | `bare-review` |
| `findings_table_v1` | `\| ID \| Locator \| Finding \| Detail \| Action \|` + Notes; positional cell mapping. | `refactor-find`, `edge-case-hunt`, `doc-completeness` |
| `hypothesis_table_v1` | `\| ID \| Cause \| Evidence \| Confidence \| Next Step \|` + Notes; `H-NN` IDs. | `troubleshoot-hypothesis` |
| `verdict_only_v1` | `## Verdict` (`yes`/`no`/`uncertain` via alias map; unknown labels pass through) + `## Rationale` + `## Notes`. | `spec-completeness`, `feasibility-probe` |
| `passthrough` | Worker body byte-for-byte unchanged (raw amalgamation mode). `salvaged` always false. | — (raw mode) |
| `custom` | Dynamic loader dispatcher; resolves a real recipe from a `custom-py:` spec. | — (escape hatch) |

> "Reformatted, never compared" is the AC-011 line: a recipe may *restate* a worker's
> severity or confidence in canonical form, but must not rank workers against each
> other. That comparison happens downstream in the hand-off skill.

### The `custom-py` loader

Author your own normalization without modifying the registry:

```text
normalization.recipe = "custom-py:<module>:<callable>"
```

- Grammar: prefix `custom-py:`, then `<module>:<callable>`. Parsed with `rpartition(":")`
  so the **last** colon separates the callable — the module path may contain colons.
- The callable resolves to either a **zero-arg class** (instantiated `cls()`) or a
  **pre-built Recipe object**; the loader asserts `isinstance(instance, Recipe)` and
  raises `TypeError` otherwise.
- Valid: `custom-py:my_pkg.recipes.priority:PriorityRecipe`,
  `custom-py:my_pkg.recipes:singleton_recipe`.
- Rejected: empty, missing `custom-py:` prefix, no second colon, empty module, empty
  callable.
- The bundled `custom` registry slot is a dispatcher sentinel; calling its `normalize`
  directly raises `RuntimeError` — you must resolve through a `custom-py:` spec.

> **Trust boundary.** `custom-py` imports an arbitrary Python module with full host
> privileges — no sandbox, no allow-list. Treat the spec string as trusted, PR-reviewed
> input, exactly like code.

---

## The lens validator (6 assertions)

`validate-lenses` runs the COMP-023 validator over every non-`custom` entry. Each entry
must pass **all six** assertions (fail-fast, first failure reported):

| # | Assertion | Checks |
|---|---|---|
| 1 | File ref resolves | `output_template_path` is non-empty and points at a readable file. |
| 2 | Recipe registered | `recipe_name` resolves against the recipe registry. |
| 3 | Suspect coupling | `suspect=true` ⟺ `{suspect_files}` present in the hand-off template (bidirectional). |
| 4 | Name unique | The lens `name` doesn't collide with another entry. |
| 5 | Injection substring | `system_prompt_fragment` contains the canonical §11.5 guard sentence. |
| 6 | Normalizer strategy | `normalizer_strategy` resolves to a registered recipe (added by T02.21). |

> **Doc-vs-code note:** the `validate-lenses --help` text and some module docstrings
> still say "five-assertion" / "COMP-023 five assertions." The **implemented** validator
> runs **six** — assertion 6 (`normalizer_strategy`) was added in T02.21. The live
> summary line (`8 entries inspected, 7 validated`) and the assertion loop in
> `lenses/_validate.py` are ground truth.

External dependencies (recipe registry, strategy registry, filesystem) are injected as
callables, so the validator is unit-testable with stubs.

---

## What "suspect" means

`suspect` marks a lens whose review needs extra scrutiny on **suspect-source** files —
the files a worker flags as the likely origin of a problem. When `suspect=true`, the
`recommended_next_command_template` **must** contain `{suspect_files}` so the downstream
driver can substitute the flagged-file list at hand-off (assertion 3). When `false`, the
placeholder is **forbidden** (it would dangle with no value). Only `bare-review` is
`suspect=true` — it carries the PR-review discipline that produces a suspect-file list;
its hand-off is `/sc:adversarial … --suspect-source {suspect_files}`.

---

## Authoring a new lens (orientation)

A `LensEntry` (DM-010, `cli/swarm/lenses/`) carries: `name`, `description`,
`system_prompt_fragment` (**must** end with the canonical injection-guard sentence),
`user_template`, `recipe_name`, `normalizer_strategy`, `default_workers`,
`default_target_line_cap`, `stability`, `tier`, `suspect`,
`recommended_next_command_template`, `output_template_path`, and `acceptance_notes`.

Checklist to pass `validate-lenses`:

1. Point `output_template_path` at a real file under `lenses/templates/`.
2. Set `recipe_name` and `normalizer_strategy` to registered recipes.
3. Append the canonical §11.5 guard sentence to `system_prompt_fragment`.
4. If `suspect=true`, include `{suspect_files}` in the hand-off template (and omit it if
   `false`).
5. Keep `name` unique.

The per-worker output **template** (in `lenses/templates/`) is the shape contract workers
are asked to follow and that the recipe normalizes toward. Mirror an existing template
for your recipe family (findings-table / verdict / hypothesis).

See also: [Command Reference](command-reference.md) · [User Guide](user-guide.md) ·
[Open-Question Resolutions](oq-resolutions.md) for the `validate-lenses` failure-semantics
rationale (OQ-010) and the `caller_metadata.suspect` propagation design (OQ-009).
