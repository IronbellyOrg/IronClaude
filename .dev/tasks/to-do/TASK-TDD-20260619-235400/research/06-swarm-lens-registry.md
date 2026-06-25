# Research 06 — Swarm Lens Registry + `bare_review` Precedent

- **Type:** Integration Mapper
- **Scope:** Swarm lens registry (`cli/swarm/lenses/`), `bare_review` LensEntry precedent, lens registration + validation, output-template frontmatter convention, `LensEntry` dataclass, `CANONICAL_INJECTION_GUARD_SENTENCE`. Target: define exact shape for new `reflect-review` lens + `reflect-review-output.md` template per FR-RH2.2.
- **Status:** Complete
- **Date:** 2026-06-19

---

## 1. The `LensEntry` dataclass field set (DM-010) `[CODE-VERIFIED]`

Source: `src/superclaude/cli/swarm/models.py`, class `LensEntry` defined L636-728; **field declarations L707-720**; `__post_init__` stability guard L722-728.

Full field set (14 fields, in declaration order):

| # | Field | Type | Default | Notes |
|---|-------|------|---------|-------|
| 1 | `name` | `str` | `""` | Hyphenated registry name (e.g. `"bare-review"`). |
| 2 | `description` | `str` | `""` | Human-facing registry metadata; NOT propagated to `ResolvedLensEntry`. |
| 3 | `system_prompt_fragment` | `str` | `""` | Must contain `CANONICAL_INJECTION_GUARD_SENTENCE` (validator assertion 5). |
| 4 | `user_template` | `str` | `""` | Verbatim user prompt with `{target_content}` placeholder. |
| 5 | `output_template_path` | `str` | `""` | Abs path to the per-lens output template; validator assertion 1 checks it resolves. |
| 6 | `recipe_name` | `str` | `""` | Must resolve in recipe registry (validator assertion 2). |
| 7 | `normalizer_strategy` | `str` | `""` | FR-LENSREG.NS / T02.21 sixth field; validator assertion 6. |
| 8 | `default_workers` | `int` | `3` | Worker fan-out count. |
| 9 | `default_target_line_cap` | `int` | `4000` | Mirrors `Truncation.line_cap` default. |
| 10 | `suspect` | `bool` | `False` | Opt-in; couples to `{suspect_files}` placeholder (validator assertion 3). |
| 11 | `tier` | `str` | `""` | Free-form tier string (e.g. `"T2"`, `"T2-feas"`). |
| 12 | `recommended_next_command_template` | `str` | `""` | Next-command template; must carry `{suspect_files}` when `suspect=True`. |
| 13 | `acceptance_notes` | `str` | `""` | Validator advisory text; not consumed at runtime. |
| 14 | `stability` | `Stability` (`Literal["stable","experimental"]`) | `"stable"` | `__post_init__` raises `ValueError` if out of enum. |

`Stability` Literal defined `models.py` L67: `Literal["stable", "experimental"]`. The dataclass is a plain mutable `@dataclass` (L636) — no `frozen=`.

**Note on the prompt's `~L` anchors vs. the dataclass:** the task prompt's anchors (`suspect=True` ~L63, `tier="T2"` ~L64, etc.) refer to the **`bare_review.py` LensEntry literal**, NOT the dataclass field declarations. Both verified below.

`ResolvedLensEntry` (DM-011, the immutable manifest snapshot) carries a **narrower 9-field subset** (`models.py` L791-799): `name`, `system_prompt_fragment`, `user_template`, `recipe_name`, `default_workers`, `suspect`, `tier`, `recommended_next_command_template`, `stability`. It drops `description`, `output_template_path`, `default_target_line_cap`, `acceptance_notes`, and (notably) does **not** carry `normalizer_strategy`. `from_lens()` classmethod at L809-839 copies exactly those 9. Implication for `reflect-review`: the `tier`, `suspect`, and `recommended_next_command_template` values survive into the manifest; `default_target_line_cap` and `normalizer_strategy` do not.

---

## 2. The `bare_review` LensEntry literal — every field `[CODE-VERIFIED]`

Source: `src/superclaude/cli/swarm/lenses/bare_review.py`. The `LENS: LensEntry = LensEntry(` literal is at **L40-75** (prompt said ~L40 — confirmed). Template path computed L35-37; injection-guard import L29.

EVERY field of the `bare_review` `LENS` literal, with exact values:

| Field | Value (verbatim from L41-74) | Line |
|-------|------------------------------|------|
| `name` | `"bare-review"` | L41 |
| `description` | `"Unscaffolded native-instinct review with suspect-source framing. Ports the sc-bare-review v1.3.0-draft skill into the bundled swarm-lens registry (COMP-024)."` | L42-46 |
| `system_prompt_fragment` | `"You are conducting a bare review of the target. Surface concrete findings with file:line citations and label any high-confidence suspect-source files. "` **`+ CANONICAL_INJECTION_GUARD_SENTENCE`** | L47-52 |
| `user_template` | `"Review the following target and produce a findings table with severity, file:line, title, evidence, and suspect-source flag.\n\n<<<TARGET>>>\n{target_content}\n<<<END TARGET>>>"` | L53-57 |
| `output_template_path` | `_TEMPLATE_PATH` (= `str((Path(__file__).parent / "templates" / "bare-review-output.md").resolve())`, L35-37) | L58 |
| `recipe_name` | `"bare-review-v1"` | L59 |
| `normalizer_strategy` | `"bare-review-v1"` | L60 |
| `default_workers` | `3` | L61 |
| `default_target_line_cap` | `4000` | L62 |
| `suspect` | `True` | **L63** (prompt said ~L63 — confirmed) |
| `tier` | `"T2"` | **L64** (prompt said ~L64 — confirmed) |
| `recommended_next_command_template` | `"/sc:adversarial --compare {compare_files} --suspect-source {suspect_files}"` | **L65-68** (prompt said ~L65→~L66 — confirmed) |
| `acceptance_notes` | `"Stable lens. PR-review discipline (NFR-012) applies: extra scrutiny on suspect:true; ensure {suspect_files} substitution remains in the next-command template (COMP-023 assertion 3)."` | L69-73 |
| `stability` | `"stable"` | L74 |

Key observations for the mirror:
- `bare_review.py` keeps `recipe_name == normalizer_strategy == "bare-review-v1"` (a 1:1 binding). The validator's assertions 2 and 6 both resolve against the recipe registry surfaces, so both must name a registered recipe.
- The injection-guard sentence is **appended verbatim** via Python string concatenation (`+ CANONICAL_INJECTION_GUARD_SENTENCE`, L51), imported at L29 from `schema`. This is how assertion 5 is satisfied byte-for-byte.
- `recommended_next_command_template` carries BOTH `{compare_files}` and `{suspect_files}`. Only `{suspect_files}` is checked by the validator (assertion 3). `{compare_files}` is a free additional placeholder for the `/sc:adversarial` driver.
- `__all__ = ["LENS"]` (L32) — each lens module exports exactly one `LENS` constant.
- NO hard-coded model ID anywhere in `bare_review.py`. Models flow from the `T2Model0N` env pool via `WorkerSpec.models` at preflight (FR-020 expansion), NOT from the lens. **Confirmed by grep:** zero `claude`/`anthropic`/`gpt`/`model_id`/`models=` literals in ANY of the seven lens files — every lens imports only `LensEntry` + `CANONICAL_INJECTION_GUARD_SENTENCE`. Model expansion happens in `preflight.py` from `job_spec.workers.models` (the configured T2 pool; `preflight.py` L1663, L1808), with INV-007 raising env-missing on an empty pool (`preflight.py` L121, L930-951).

---

## 3. Registration: how lenses register; where `reflect-review` goes `[CODE-VERIFIED]`

Source: `src/superclaude/cli/swarm/lenses/__init__.py` (the aggregator/registry).

Registration is a 3-point wiring, all in `__init__.py`:

1. **Import** the module's `LENS` constant under a private alias. `bare-review` example at L49: `from superclaude.cli.swarm.lenses.bare_review import LENS as _BARE_REVIEW_LENS`. (Imports are kept alphabetical by module; L49-67.)
2. **Add the hyphenated name to `LENS_NAMES`** — the canonical ordered tuple at L73-82. Current 8 entries: `bare-review`, `refactor-find`, `edge-case-hunt`, `spec-completeness`, `feasibility-probe`, `troubleshoot-hypothesis`, `doc-completeness`, `custom`. This tuple pins registry order for docs + tests.
3. **Add the dict entry to `LENSES`** — L105-114, mapping hyphenated name → the imported `LENS` constant. `"bare-review": _BARE_REVIEW_LENS` at L106.

Resolution helpers:
- `get_lens(name)` (L125-137) → `LENSES[name]` or raises `KeyError(name)` (preflight wraps into `RULE_UNKNOWN_LENS`).
- `iter_lenses()` (L140-149) yields entries in `LENS_NAMES` order — the canonical sequence the validator iterates.

**Naming convention (critical, `__init__.py` L36-42 + L85-89):**
- **Hyphenated** form (`reflect-review`) = `LensEntry.name`, the `LENS_NAMES` tuple member, and the `LENSES` dict key.
- **Underscored** form (`reflect_review`) = the Python **module filename** `cli/swarm/lenses/reflect_review.py` and the import alias `_REFLECT_REVIEW_LENS`.

`custom` is special: built by `_custom_placeholder()` (L92-102) = `LensEntry(name="custom")` with all-default fields; the validator skips it (escape hatch, contents flow from `--custom-prompt-dir`).

**Where `reflect-review` registers** — three edits to `__init__.py`:
1. `from superclaude.cli.swarm.lenses.reflect_review import LENS as _REFLECT_REVIEW_LENS` (alphabetical insertion among L49-67).
2. Append `"reflect-review"` to `LENS_NAMES` (L73-82) — pick a deterministic slot; appending after the existing experimental built-ins keeps `custom` last (the registry contract puts `custom` last).
3. Add `"reflect-review": _REFLECT_REVIEW_LENS,` to the `LENSES` dict (L105-114), inserted to match the `LENS_NAMES` order.

---

## 4. Validation: the gate `reflect-review` must pass `[CODE-VERIFIED]`

Source: `src/superclaude/cli/swarm/lenses/_validate.py`. Public entry `validate_lens()` L540-615 (fail-fast, returns first failure); registry-wide `validate_all()` L623-702. The `custom` lens is exempt (short-circuits to `None`, L594-595).

Six assertions, in order (`validate_lens` loop L604-611), each with a stable `RULE_*` identifier:

| # | Assertion | Check | Rule id | Helper |
|---|-----------|-------|---------|--------|
| 1 | File refs resolve | `output_template_path` non-empty AND resolves to a readable file (`Path.is_file`) | `lens.file_ref_unresolved` (L122) | `_check_file_refs` L320-354 |
| 2 | Recipe registered | `recipe_name` non-empty AND resolves in recipe registry | `lens.recipe_unregistered` (L125) | `_check_recipe_registered` L357-391 |
| 3 | Suspect ↔ suspect_files | `suspect=True` ⇒ template contains `{suspect_files}`; `suspect=False` ⇒ it must NOT | `lens.suspect_files_coupling` (L128) | `_check_suspect_coupling` L394-431 |
| 4 | Name uniqueness | `name` not in `other_names` (registry context only) | `lens.name_duplicate` (L131) | `_check_name_unique` L434-456 |
| 5 | §11.5 substring | `system_prompt_fragment` contains `CANONICAL_INJECTION_GUARD_SENTENCE` (via `contains_required_substring`) | `lens.injection_substring_missing` (L134) | `_check_injection_substring` L459-490 |
| 6 | Normalizer-strategy | `normalizer_strategy` non-empty AND resolves against a registered recipe | `lens.normalizer_strategy_unmatched` (L137) | `_check_normalizer_strategy` L493-532 |

`SUSPECT_FILES_PLACEHOLDER = "{suspect_files}"` (L111). `CUSTOM_LENS_NAME = "custom"` (L99). Default substring is `CANONICAL_INJECTION_GUARD_SENTENCE` (L547, imported L70-73).

**Implications for `reflect-review` (which is `suspect=True`):**
- Assertion 3 is the load-bearing one: because `suspect=True`, `recommended_next_command_template` **MUST** contain the literal `{suspect_files}` token, or validation fails with `lens.suspect_files_coupling`. The FR-RH2.2 template `/sc:adversarial ... {suspect_files}` satisfies this exactly.
- Assertion 1: the template file `reflect-review-output.md` must exist on disk at the resolved path (so the file must be created, not just referenced).
- Assertions 2 & 6: `recipe_name` and `normalizer_strategy` must each resolve in the recipe registry. The bare-review precedent sets both to the same value (`"bare-review-v1"`); `reflect-review` must bind to a recipe that is actually registered, or both assertions fail. **This is a dependency** — the lens cannot be authored in isolation if it names a new recipe that isn't registered (see Gaps).
- Assertion 5: `system_prompt_fragment` must append `CANONICAL_INJECTION_GUARD_SENTENCE` verbatim (same `+ CANONICAL_INJECTION_GUARD_SENTENCE` pattern as `bare_review.py` L51).

---

## 5. Output-template frontmatter convention `[CODE-VERIFIED]`

Two precedents read:

### 5a. `feasibility-probe-output.md` (the mirror source for `reflect-review-output.md`)

The canonical frontmatter block is at `feasibility-probe-output.md` L46-62 (inside a fenced ```markdown block documenting what `verdict_only_v1.render_markdown` emits):

```yaml
schema_version: "1.0"
tier: "T2-feas"
suspect: false
lens: "feasibility-probe"
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
```

**Convention (stated explicitly at L98-100):** `schema_version`, `tier`, `suspect`, and `lens` are **pinned by the lens entry** (`LensEntry.tier`, `suspect`, `name`) and emitted verbatim — they are NOT placeholders. Everything wrapped in `{...}` is a **recipe-supplied placeholder** substituted at normalize/dispatch time (placeholder ownership table at L82-96):
- `{reviewer_model_id}` / `{reviewer_model_label}` — dispatcher (`args["model_id"]` / `args["model_label"]`). **This is the substitution point where the T2-pool model identity lands** — the lens never names a model; the dispatcher injects the resolved pool model id here.
- `{target}` / `{target_checksum}` / `{target_truncated}` — preflight.
- `{generated}` / `{verdict}` / `{verdict_confidence}` — normalizer.
- `{caller_label}` — preflight; `{elapsed_ms}` — dispatch meta.

YAML-quoting rules from the same table: string placeholders are YAML-quoted (`"{...}"`); bools/ints are bare (`{target_truncated}`, `{elapsed_ms}`).

The doc also carries: a `## Lens prompt → recipe section mapping` table (L16-30), verdict-label normalization (L32-43), section-cell placeholder caps (L104-109), §7.4 salvage semantics (L111-120), AC-011 no-judging boundary (L122-129), and a `## Provenance` block (L131-141) pointing at recipe/lens/fixture/spec anchors.

### 5b. `bare-review-output.md` (the suspect-lens precedent)

`bare-review-output.md` is **much terser** (21 lines, no YAML frontmatter at all). It documents a findings table (L10-11: `| Severity | File:line | Title | Evidence | Suspect-source? |`), a `## Suspect files` section (L13-16) explicitly noting the list is "consumed by `{suspect_files}` substitution in the recommended next-command template", and a `## Raw observations` section (L18-20). It does NOT carry the `schema_version`/`tier`/`suspect`/`lens` frontmatter block — that richer convention is the `feasibility-probe` family's.

**Reconciliation for `reflect-review-output.md`:** the REUSE-AUDIT verdict pins the template to **mirror-shape of `feasibility-probe-output.md`** (the frontmatter-bearing form), not the terse `bare-review-output.md`. So `reflect-review-output.md` should carry the full YAML frontmatter block with `suspect: true`, `tier:` pinned to the lens's tier, `lens: "reflect-review"`, `schema_version: "1.0"`, and the `{reviewer_model_id}` substitution — AND, because the lens is `suspect=True`, it should ALSO carry a `## Suspect files` section in the `bare-review-output.md` style so the `{suspect_files}` next-command substitution has a source. This is the one place the mirror blends both precedents.

---

## 6. EXACT shape the new `reflect-review` lens must take (per FR-RH2.2) `[CODE-VERIFIED]` against precedents

### 6a. `cli/swarm/lenses/reflect_review.py` — mirror-shape of `bare_review.py`

Required structure (mirroring `bare_review.py` L24-75):

```python
from __future__ import annotations
from pathlib import Path
from superclaude.cli.swarm.models import LensEntry
from superclaude.cli.swarm.schema import CANONICAL_INJECTION_GUARD_SENTENCE

__all__ = ["LENS"]

_TEMPLATE_PATH = str(
    (Path(__file__).parent / "templates" / "reflect-review-output.md").resolve()
)

LENS: LensEntry = LensEntry(
    name="reflect-review",
    description="...",                       # str
    system_prompt_fragment=(
        "...reflect-review framing... "
        + CANONICAL_INJECTION_GUARD_SENTENCE  # MANDATORY for assertion 5
    ),
    user_template="...{target_content}...<<<TARGET>>>...<<<END TARGET>>>",
    output_template_path=_TEMPLATE_PATH,
    recipe_name="<registered-recipe>",        # assertion 2 — must resolve
    normalizer_strategy="<registered-recipe>",# assertion 6 — must resolve
    default_workers=<2..4>,                   # FR-RH2.2: default_workers ∈ [2,4]
    default_target_line_cap=4000,             # or domain-appropriate
    suspect=True,                             # FR-RH2.2
    tier="T2",                                # FR-RH2.2
    recommended_next_command_template=(
        "/sc:adversarial ... --suspect-source {suspect_files}"  # FR-RH2.2: {suspect_files} REQUIRED
    ),
    acceptance_notes="...",                   # str
    stability="stable" | "experimental",
)
```

FR-RH2.2 hard constraints mapped to fields:
- `suspect=True` → field 10. Forces `{suspect_files}` in field 12 (validator assertion 3).
- `tier="T2"` → field 11. Same literal `"T2"` as `bare_review.py` L64.
- `default_workers ∈ [2,4]` → field 8. `bare_review` uses 3 (in-range). `edge_case_hunt`/`troubleshoot_hypothesis` use 4. Any of {2,3,4} satisfies FR-RH2.2. Must be ≥ `StatusPolicy.floor` (=2) for a `partial`/`success` outcome to be reachable.
- **NO hard-coded Claude model** → no model field exists on `LensEntry` to hold one; models come from the `T2Model0N` env pool via `job.workers.models` at preflight (§2 above). The lens file must import only `LensEntry` + `CANONICAL_INJECTION_GUARD_SENTENCE`, exactly like every existing lens. Do **not** set `spec.workers.models` from the lens.
- `recommended_next_command_template` carrying `/sc:adversarial` + `{suspect_files}` → field 12. Mirror `bare_review.py` L65-68 (`/sc:adversarial --compare {compare_files} --suspect-source {suspect_files}`), keeping at minimum the `--suspect-source {suspect_files}` tail.

### 6b. `cli/swarm/lenses/templates/reflect-review-output.md` — mirror-shape of `feasibility-probe-output.md`

Required frontmatter (pinned values from the lens entry + recipe placeholders), per §5a convention:

```yaml
schema_version: "1.0"      # pinned
tier: "T2"                 # pinned to LensEntry.tier
suspect: true              # pinned to LensEntry.suspect  (NOTE: lowercase YAML bool)
lens: "reflect-review"     # pinned to LensEntry.name
reviewer_model_id: "{reviewer_model_id}"        # dispatcher substitution (the T2-pool model lands here)
reviewer_model_label: "{reviewer_model_label}"
target: "{target}"
target_checksum: "{target_checksum}"
target_truncated: {target_truncated}            # bare bool
generated: "{generated}"
caller_label: "{caller_label}"
elapsed_ms: {elapsed_ms}                         # bare int
```

Plus (because `suspect=True`): a `## Suspect files` body section in the `bare-review-output.md` style (L13-16) so the `{suspect_files}` next-command substitution has a documented source, and the findings/sections body appropriate to the reflect-review recipe. Carry a `## Provenance` block (feasibility precedent L131-141) pointing at the recipe, lens module, fixture, and spec anchors.

### 6c. Registration edits (per §3): three lines in `__init__.py`
1. import `_REFLECT_REVIEW_LENS`,
2. append `"reflect-review"` to `LENS_NAMES`,
3. add `"reflect-review": _REFLECT_REVIEW_LENS` to `LENSES`.

---

## Key Takeaways

1. **`LensEntry` has 14 fields** (`models.py` L707-720); `reflect-review` sets the same fields `bare_review` does. There is **no model field** — that is the structural guarantee that "no hard-coded Claude model" is satisfiable: models only ever arrive via `job.workers.models` (the T2 pool) at preflight.
2. **`bare_review.py` is a clean, copyable precedent** for a `suspect=True` / `tier="T2"` lens. The mirror is mechanical: change `name`, `description`, prompts, template path, recipe binding; keep `suspect=True`, `tier="T2"`, the `+ CANONICAL_INJECTION_GUARD_SENTENCE` append, and the `{suspect_files}` next-command tail.
3. **The validator's assertion 3 is the FR-RH2.2 enforcer**: `suspect=True` mechanically requires `{suspect_files}` in `recommended_next_command_template`. `/sc:adversarial ... --suspect-source {suspect_files}` passes.
4. **Registration is 3 edits to `__init__.py`** (import alias, `LENS_NAMES` tuple, `LENSES` dict) using the hyphen-name/underscore-module convention.
5. **Template frontmatter convention**: `schema_version`/`tier`/`suspect`/`lens` are **pinned verbatim from the lens entry**; `{reviewer_model_id}` is the recipe/dispatcher substitution where the T2-pool model identity appears. Mirror `feasibility-probe-output.md`'s frontmatter; blend in `bare-review-output.md`'s `## Suspect files` section because the lens is `suspect=True`.
6. **REUSE-AUDIT re-confirmed against shipped code**: `reflect_review.py` = mirror-shape of `bare_review.py` (`bare_review.py` L40-75 is the literal to mirror); `reflect-review-output.md` = mirror-shape of `feasibility-probe-output.md` (frontmatter block at `feasibility-probe-output.md` L46-62, convention at L98-100). Verdicts hold.

## Gaps and Questions

- **`[UNVERIFIED]` Recipe binding for `reflect-review`.** Validator assertions 2 (`recipe_name`) and 6 (`normalizer_strategy`) require the named recipe to **resolve in the recipe registry** (`recipes.REGISTRY` / `STRATEGIES` / `__all__`). `bare_review` binds to `bare-review-v1`; `feasibility-probe` binds to `verdict_only_v1`. It is NOT determined here whether `reflect-review` reuses an existing recipe (e.g. `bare-review-v1`, a findings-table shape) or requires a new one. If a new recipe is needed, that is a separate deliverable that must land + register before the lens passes `swarm validate-lenses`. **Recommend the TDD specify the recipe binding explicitly.** (Not in scope of the files this agent was asked to read — `recipes/` was not opened.)
- **`[UNVERIFIED]` Exact `tier` string casing/suffix.** `bare_review` uses `"T2"`; `feasibility-probe` uses `"T2-feas"`. FR-RH2.2 says `tier:"T2"`. Using plain `"T2"` matches `bare_review` and FR-RH2.2 literally; confirm the TDD doesn't want a `-reflect` suffix for output-filename disambiguation.
- **`[UNVERIFIED]` `stability` value for the new lens.** `bare_review` is the only `"stable"` built-in at M2; the other six ship `"experimental"`. FR-RH2.2 does not state which `reflect-review` should be. Default to `"experimental"` unless the TDD wires a production caller.
- **`[UNVERIFIED]` `default_workers` exact value within [2,4].** FR-RH2.2 allows the range; the precise integer is a TDD decision (3 mirrors `bare_review` exactly; 4 mirrors the hunt lenses). Must be ≥ `StatusPolicy.floor`=2.

## Summary

The swarm lens registry is a three-file contract: each lens module (`cli/swarm/lenses/<name>.py`) exports one `LENS: LensEntry` constant; `__init__.py` imports it, lists its hyphenated name in `LENS_NAMES`, and maps it in `LENSES`; `_validate.py` runs six fail-fast cross-field assertions (the `custom` lens exempt). `bare_review.py` (L40-75) is the canonical `suspect=True`/`tier="T2"` precedent and a directly mirror-able template for `reflect-review`: it sets every `LensEntry` field, appends `CANONICAL_INJECTION_GUARD_SENTENCE` (`schema.py` L133-137) verbatim to `system_prompt_fragment`, and carries `/sc:adversarial ... --suspect-source {suspect_files}` as its next-command template — exactly the FR-RH2.2 shape. No lens file holds a model ID; the T2Model0N pool flows through `job.workers.models` at preflight. The output template mirrors `feasibility-probe-output.md`'s frontmatter convention (`schema_version`/`tier`/`suspect`/`lens` pinned from the lens entry; `{reviewer_model_id}` is the dispatcher substitution), blended with a `## Suspect files` section since the lens is `suspect=True`. The single open dependency is the recipe binding (assertions 2 & 6), which was outside the read scope and should be pinned by the TDD.
