# 09 — Reflect Config + CLI Surface & Swarm Recipe Registry (FR-RH2 Mutation Points)

- **Topic:** FR-RH2 new-input mutation surface — how `--transport` / `--reviewers` / `--depth` flow from Click → config resolver → runner, plus the swarm recipe registry binding the new `reflect-review` lens needs.
- **Type:** Code Tracer
- **Scope:** `src/superclaude/cli/reflect/{commands,config,models,runner,contract}.py`; `src/superclaude/cli/swarm/recipes/`; `src/superclaude/cli/swarm/lenses/_validate.py`; `bare_review.py`.
- **Status:** Complete
- **Date:** 2026-06-20

---

## Orientation: where each FR-RH2 field lives

Critical structural fact verified up front: **`ReflectConfig` is NOT defined in `config.py`.** It is a dataclass in `models.py` and is imported by `config.py` (`from .models import ReflectConfig`, `config.py:24`). FR-RH2 must therefore touch BOTH files for every new resolved field:

1. `models.py` — add the dataclass FIELD (with type + default).
2. `config.py` `resolve_config()` — add the PARAMETER + resolution logic + pass it into the `ReflectConfig(...)` constructor call.
3. `commands.py` — add the `@click.option`, the `run()` signature param, and thread it into the `resolve_config(...)` call.

This three-file chain is the whole "Click → config → runner" mutation surface. The runner consumes `config.<field>` directly.

[CODE-VERIFIED] `config.py:24` — `from .models import ReflectConfig`.
[CODE-VERIFIED] `models.py:57-86` — `@dataclass class ReflectConfig` definition.

---

## Section 1 — `ReflectConfig` dataclass (`models.py:57-91`)

The dataclass has **no field defaults** for the core block — fields are positional/keyword and ALL are supplied by `resolve_config`. The "auto-fix evolution" block at the tail (`base_override`, `fix`, `max_fix_iterations`) is documented as "appended AFTER all existing non-default fields to respect the dataclass field-ordering rule" (`models.py:82-83`). This is the load-bearing precedent for FR-RH2: **new fields append at the tail of the dataclass** (after `max_fix_iterations`), never mid-block.

### Every field, in declaration order (`models.py:66-86`)

| # | Field | Type | Default (in dataclass) | Resolved from |
|---|-------|------|------------------------|---------------|
| 1 | `tasklist_path` | `Path` | (none) | `Path(tasklist_path).resolve()` `config.py:165` |
| 2 | `base` | `str` | (none) | FR-6 precedence `_resolve_base()` `config.py:183` |
| 3 | `head` | `str` | (none) | `git rev-parse HEAD` `config.py:185` |
| 4 | `spec_path` | `Path \| None` | (none) | `--spec` arg → frontmatter, file-exists gated `config.py:193-198` |
| 5 | `depth` | `str` | (none) | `"standard" if depth=="quick" else depth` `config.py:190` |
| 6 | `executor_model` | `str \| None` | (none) | env `EXECUTOR_MODEL_CLASS` → frontmatter `config.py:201-205` |
| 7 | `output_dir` | `Path` | (none) | `--output` or `<task-dir>/reflect/post/<head[:12]>/` `config.py:207-218` |
| 8 | `model` | `str` | (none) | non-empty required `config.py:170-172` |
| 9 | `timeout_seconds` | `int` | (none) | `timeout or 3600` `config.py:229` |
| 10 | `max_turns` | `int` | (none) | `max_turns or 250` `config.py:230` |
| 11 | `promote` | `bool` | (none) | passthrough `config.py:231` |
| 12 | `allow_single_vendor` | `bool` | (none) | passthrough `config.py:232` |
| 13 | `tmux` | `bool` | (none) | passthrough `config.py:233` |
| 14 | `dry_run` | `bool` | (none) | passthrough `config.py:234` |
| 15 | `print_command` | `bool` | (none) | passthrough `config.py:235` |
| 16 | `resume` | `bool` | (none) | passthrough `config.py:236` |
| 17 | `base_override` | `str \| None` | (none) | `--base` passthrough `config.py:237` |
| 18 | `fix` | `bool` | (none) | passthrough `config.py:238` |
| 19 | `max_fix_iterations` | `int` | (none) | passthrough `config.py:239` |

Note: none of these carry a `= default` in the dataclass body — `resolve_config` supplies every value, so the dataclass relies on positional/keyword completeness. The defaults (3600, 250, etc.) live in `resolve_config` constants, not the dataclass. The `field(default_factory=...)` pattern is only used in the sibling `ReflectResult` (`models.py:109`), not `ReflectConfig`.

There is **one property**: `contract_path` (`models.py:88-91`) → `self.output_dir / "return-contract.yaml"`.

[CODE-VERIFIED] All field rows above traced to `models.py:66-86` and `config.py` resolution lines cited.

### FR-RH2 insertion point in the dataclass

Append the three new resolved fields **after `max_fix_iterations` (`models.py:86`)**, following the documented "append at tail" rule:

```python
    # FR-RH2 hardening inputs (appended at tail per field-ordering rule).
    transport: str            # "openai_compat" | "stub"
    reviewers: int            # clamped [2,4]; 1 => negative-witness mode
    # depth already exists (field #5) — see Section 1a, do NOT re-add.
```

`expected_tier` is **NOT a ReflectConfig field** — it is derived at runtime in `runner.py` (Section 1b). FR-RH2 may either keep deriving it in the runner or promote it to a resolved config field; the current code derives it.

---

## Section 1a — `--depth` ALREADY EXISTS (do NOT re-add)

`--depth` is fully wired today. FR-RH2 must **not** introduce it as new — it only needs to lean on the existing field.

- **Click option** `commands.py:101-106`:
  ```python
  @click.option(
      "--depth",
      type=click.Choice(["standard", "deep"], case_sensitive=False),
      default="standard",
      help="Reflect depth passthrough (POST never runs quick).",
  )
  ```
  Choices are exactly `{standard, deep}` (case-insensitive), default `standard`. This already matches the FR-RH2 spec `--depth {standard|deep}`.
- **`run()` signature** receives `depth: str` (`commands.py:154`) and passes `depth=depth` into `resolve_config` (`commands.py:177`).
- **`resolve_config` parameter** `depth: str` is keyword-only (`config.py:126`).
- **Resolution / floor**: `resolved_depth = "standard" if depth == "quick" else depth` (`config.py:190`). A `quick` value is floored to `standard` (O4/FR-3: POST never runs quick). Stored into `ReflectConfig.depth` (`config.py:225`).

[CODE-VERIFIED] `--depth` Click option `commands.py:101-106`; resolution `config.py:190`; field `models.py:71`.

---

## Section 1b — How `expected_tier` is derived from `depth`

Derived in the runner, NOT config:

`runner.py:403`:
```python
expected_tier = 2 if config.depth in {"standard", "deep"} else 1
```

So for BOTH `standard` and `deep`, `expected_tier == 2` (a T2 post gate). Only a non-`{standard,deep}` depth would yield tier 1 — and since `resolve_config` floors `quick`→`standard` and Click constrains choices to `{standard,deep}`, the practical result is always `2`. It is then passed into `derive_verdict(expected_tier=...)` (`runner.py:421-426`), where:
- `contract.py:235` — pass requires `status == "success" and tier_reached == expected_tier`.
- `contract.py:263` — `if expected_tier >= 2 and tier_reached == 1:` flags a degrade/halt path.

**FR-RH2 implication:** if `deep` must map to a DIFFERENT expected tier than `standard`, the `runner.py:403` ternary is the exact mutation point (it currently collapses both to 2). The `expected_tier` signature already threads through `contract.derive_verdict` (`contract.py:133, 216, 235, 254, 263`), so no plumbing change is needed there — only the derivation rule.

[CODE-VERIFIED] `runner.py:403` derivation; `contract.py:133/216/235/254/263` consumption.

---

## Section 1c — `--transport` and `--reviewers` are NET-NEW (zero occurrences today)

Grep across `src/superclaude/cli/reflect/` finds **no** `transport`, `reviewers`, `openai_compat`, `stub`, `negative-witness`, or `negative_witness` tokens in any reflect module. The only `transport` hit is the word "reviewers" inside a config.py code-comment about Tier-2 reviewers (`config.py:34`), unrelated to a flag. So FR-RH2 adds these from scratch.

[CODE-CONTRADICTED] (against any assumption they exist) — `grep -rn "transport|reviewers|openai_compat|negative-witness"` over `src/superclaude/cli/reflect/` returns only the prose comment at `config.py:34`. No flag, field, or resolver exists.

### `--transport {openai_compat|stub}` (default openai_compat) — insertion points

1. **Dataclass** (`models.py`, append after line 86): `transport: str`.
2. **`resolve_config` param** (`config.py:123-142` signature, keyword-only block): add `transport: str = "openai_compat"`.
3. **Constructor call** (`config.py:220-240` `ReflectConfig(...)`): add `transport=transport` (optionally validated against `{"openai_compat","stub"}` — mirror the `model` non-empty `raise ValueError` pattern at `config.py:170-172`; a bad transport → `ValueError` → command-body `blocked`/exit 2 at `commands.py:191-227`).
4. **Click option** (`commands.py`, after the `--depth` block at line 106): use `type=click.Choice(["openai_compat","stub"], case_sensitive=False), default="openai_compat"` — exactly mirroring the `--depth` Choice idiom.
5. **`run()` signature + call** (`commands.py:148-162` params; `commands.py:175-190` call): add `transport: str` param and `transport=transport` kwarg.

### `--reviewers <N>` (clamp [2,4], default 3, 1=negative-witness) — insertion points

1. **Dataclass** (`models.py`, append after `transport`): `reviewers: int`.
2. **`resolve_config` param** (`config.py` signature): `reviewers: int = 3`.
3. **Clamp logic** — the spec wants clamp `[2,4]` BUT `1` is a meaningful sentinel (negative-witness). The cleanest place is `resolve_config` body (alongside the depth floor at `config.py:190`). Two valid readings the TDD must disambiguate (flagged in Gaps):
   - (a) Clamp to `[2,4]` and treat `1` as a special pre-clamp branch: `if reviewers == 1: <negative-witness mode>` else `reviewers = max(2, min(4, reviewers))`.
   - (b) Validate-and-reject out-of-range with a `ValueError` (mirrors `model` empty check) rather than silently clamping.
   The phrase "clamp [2,4]" strongly implies (a)-style silent clamp; `1` must be checked BEFORE the clamp or the clamp would rewrite it to `2` and erase negative-witness mode.
4. **Click option** (`commands.py`, after `--transport`): `type=int, default=3, help="Reviewer count; clamped to [2,4]; 1 selects negative-witness mode."`. Do the clamp in `resolve_config`, not the Click callback, to keep validation in one place (the house pattern — all resolution lives in `config.py`).
5. **`run()` signature + call**: add `reviewers: int` and `reviewers=reviewers`.

[CODE-VERIFIED] `config.py:170-172` ValueError pattern; `config.py:190` floor pattern; `commands.py:101-106` Choice idiom — all are the templates the above insertions copy.

---

## Section 2 — `reflect run` Click command block (`commands.py:76-162`)

The command is `@reflect_group.command()` named `run` (decorator stack `commands.py:76-147`, body `commands.py:148-249`). It takes one positional `TASKLIST` argument and 12 options. The options ARE the full Section-9 in-scope set today.

### The positional argument (`commands.py:77-80`)

```python
@click.argument(
    "tasklist",
    type=click.Path(exists=True, dir_okay=False, resolve_path=True),
)
```

`exists=True` validation happens at Click parse time — relevant because the FR-2 recursion breaker in the GROUP callback (`commands.py:69-73`) must fire BEFORE this validation, which is why it lives in the group callback, not `run()`'s body.

### Every existing `@click.option` (quoted verbatim, `commands.py:81-147`)

```python
@click.option(
    "--tmux", is_flag=True, help="Run inside a detached tmux window to watch live."
)
@click.option(
    "--print-command",
    is_flag=True,
    help="Print the composed claude argv + prompt and exit without launching.",
)
@click.option(
    "--promote/--no-promote",
    "promote",
    default=True,
    help="Allow reflect's gated Wave-7 promotion (default: --promote). O2 callers pass --no-promote.",
)
@click.option(
    "--timeout",
    type=int,
    default=None,
    help="Subprocess timeout seconds (default 3600).",
)
@click.option(
    "--depth",
    type=click.Choice(["standard", "deep"], case_sensitive=False),
    default="standard",
    help="Reflect depth passthrough (POST never runs quick).",
)
@click.option(
    "--output",
    default=None,
    help="Pinned output dir (default <task-dir>/reflect/post/<short-sha>/).",
)
@click.option(
    "--allow-single-vendor",
    is_flag=True,
    help="Do not flag DEGRADED (exit 11) on single-vendor Tier-2 diversity.",
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Derive + preflight + construct command, but do not launch or edit the task file.",
)
@click.option(
    "--resume",
    is_flag=True,
    help="Skip the launch when the prior reflect_post is a pass on the current HEAD.",
)
@click.option(
    "--fix/--no-fix",
    "fix",
    default=False,
    help="Run the bounded audit->apply->re-verify auto-fix loop (Click default --no-fix; the O1/O2 gates pass --fix).",
)
@click.option(
    "--max-fix-iterations",
    type=int,
    default=2,
    help="Max apply->verify cycles before terminal HALT (D3, default 2).",
)
@click.option(
    "--base",
    "base_override",
    default=None,
    help=(
        "Explicit audit base ref (single ref vs working tree). Highest precedence "
        "over frontmatter start_commit + merge-base."
    ),
)
```

[CODE-VERIFIED] All twelve options quoted verbatim from `commands.py:81-147`.

### How options map into `ReflectConfig` construction (`commands.py:148-190`)

`run()` signature (`commands.py:148-162`) takes each option as a positional param, then constructs the model env-default and calls `resolve_config`:

- `commands.py:172` — `model = os.environ.get("ANTHROPIC_MODEL", "").strip() or _DEFAULT_MODEL` (`_DEFAULT_MODEL="claude-opus-4-8"`, `commands.py:31`). There is deliberately **no `--model` flag** (Section-9 option set is exact; `commands.py:27-30`).
- `commands.py:174-190` — the `resolve_config(...)` call inside a `try/except ValueError`. Each option threads as a kwarg:
  ```python
  config = resolve_config(
      tasklist,
      depth=depth,
      output_dir=output,
      model=model,
      timeout=timeout,
      promote=promote,
      allow_single_vendor=allow_single_vendor,
      tmux=tmux,
      dry_run=dry_run,
      print_command=print_command,
      resume=resume,
      fix=fix,
      max_fix_iterations=max_fix_iterations,
      base_override=base_override,
  )
  ```
- The `except ValueError` (`commands.py:191-227`) routes any resolution/preflight STOP to `blocked` → `sys.exit(2)`, after best-effort writing a `BLOCKED` sidecar when `--output` was explicit.

[CODE-VERIFIED] `resolve_config` call `commands.py:174-190`; ValueError→blocked path `commands.py:191-227`.

### Where the new `--transport` / `--reviewers` options + clamp wire in

1. **Add two `@click.option` decorators** in the stack. Natural placement: right after `--depth` (`commands.py:106`) since they are the same "reviewer-shape" family. Use the `--depth` `click.Choice` idiom for `--transport`; plain `type=int, default=3` for `--reviewers`.
2. **Add two params** to the `run(...)` signature (`commands.py:148-162`) — e.g. `transport: str, reviewers: int`.
3. **Add two kwargs** to the `resolve_config(...)` call (`commands.py:174-190`) — `transport=transport, reviewers=reviewers`.
4. **The `[2,4]` clamp + the `1`→negative-witness branch belong in `resolve_config`** (`config.py` body, next to the `config.py:190` depth floor), NOT in a Click callback. Rationale: the house convention keeps ALL input resolution in `config.py` (the module docstring `config.py:1-14` states it "Turns CLI args + tasklist frontmatter + git state into a validated `ReflectConfig`"). An out-of-range `--reviewers` that should HARD-fail uses the `raise ValueError(...)` idiom (`config.py:170-172`), which the command body already catches and maps to exit-2 blocked. A silent clamp simply rewrites the value before the constructor call.

[CODE-VERIFIED] insertion targets `commands.py:106` (after --depth), `commands.py:148-162` (signature), `commands.py:174-190` (call); clamp home `config.py:190` region.

---

## Section 3 — Swarm recipe registry (`src/superclaude/cli/swarm/recipes/`)

### Registry files

```
recipes/
├── __init__.py            # Recipe Protocol + NormalizedResult + REGISTRY + STRATEGIES + custom loader re-export
├── bare_review_v1.py      # BareReviewV1  -> "bare-review-v1"
├── findings_table_v1.py   # FindingsTableV1 -> "findings_table_v1"
├── hypothesis_table_v1.py # HypothesisTableV1 -> "hypothesis_table_v1"
├── verdict_only_v1.py     # VerdictOnlyV1 -> "verdict_only_v1"
├── passthrough.py         # Passthrough -> "passthrough"
└── custom.py              # CustomPyDispatcher -> "custom" (custom-py:module:func loader)
```

[CODE-VERIFIED] directory listing via `ls`; class→key mapping from `__init__.py:169-188`.

### How recipes register — `REGISTRY` and `STRATEGIES`

Two module-level dicts in `recipes/__init__.py` are the registration surface:

- **`REGISTRY`** (`__init__.py:181-188`) — maps `recipe_name` → a Recipe-conforming object:
  ```python
  REGISTRY: dict[str, Optional[Recipe]] = {
      "bare-review-v1": BareReviewV1(),
      "findings_table_v1": FindingsTableV1(),
      "hypothesis_table_v1": HypothesisTableV1(),
      "verdict_only_v1": VerdictOnlyV1(),
      "passthrough": Passthrough(),
      "custom": CustomPyDispatcher(),
  }
  ```
- **`STRATEGIES`** (`__init__.py:208-215`) — maps `normalizer_strategy` → recipe identifier. Today it is **N-to-1, strategy name == recipe name** (`__init__.py:208-215, 216-225`):
  ```python
  STRATEGIES: dict[str, str] = {
      "bare-review-v1": "bare-review-v1",
      "findings_table_v1": "findings_table_v1",
      "hypothesis_table_v1": "hypothesis_table_v1",
      "verdict_only_v1": "verdict_only_v1",
      "passthrough": "passthrough",
      "custom": "custom",
  }
  ```

"Open-class": the docstring (`__init__.py:202-205`) states contributors register by assigning `REGISTRY[<name>] = MyRecipe()` at import time. A new recipe module exports a class, `__init__.py` imports it (`# noqa: E402` deferred-import block at `__init__.py:165-178`) and adds the `REGISTRY` + `STRATEGIES` entries.

[CODE-VERIFIED] `REGISTRY` `__init__.py:181-188`; `STRATEGIES` `__init__.py:208-215`.

### How a lens binds to a recipe/strategy (the `bare-review` exemplar)

A `LensEntry` carries TWO string fields the validator checks:
- `recipe_name` (`models.py:712`, default `""`)
- `normalizer_strategy` (`models.py:713`, default `""`)

`bare-review` sets both to `"bare-review-v1"` (`lenses/bare_review.py:59-60`):
```python
    recipe_name="bare-review-v1",
    normalizer_strategy="bare-review-v1",
```

[CODE-VERIFIED] `lenses/bare_review.py:59-60`; `LensEntry` fields `models.py:712-713`.

### Validator assertions 2 & 6 (what FR-RH2's `reflect-review` lens must satisfy)

`lenses/_validate.py` runs six fail-fast assertions. The two recipe/strategy ones:

- **Assertion 2 — recipe registered** (`_validate.py:357-391`, rule `lens.recipe_unregistered` `_validate.py:125`). `recipe_name` must be non-empty AND `default_recipe_checker(name)` true. The default checker (`_validate.py:204-237`) returns `name in recipes.REGISTRY` (`_validate.py:231-233`). So `reflect-review`'s `recipe_name` **must be a key in `REGISTRY`**.
- **Assertion 6 — normalizer-strategy** (`_validate.py:493-532`, rule `lens.normalizer_strategy_unmatched` `_validate.py:137`). `normalizer_strategy` must be non-empty AND `default_strategy_checker(strategy)` true. The default checker (`_validate.py:240-291`) returns true if the strategy is in `recipes.STRATEGIES` (`_validate.py:276-278`), OR a `REGISTRY` key, OR a recipe's `.strategy` attr, OR in `__all__`. So `reflect-review`'s `normalizer_strategy` **must resolve in `STRATEGIES` (or REGISTRY)**.

Both default to lookups against the recipes module; the validator fails fast on the first violation (`_validate.py:604-615`), so an unregistered recipe_name short-circuits before assertion 6 even runs.

[CODE-VERIFIED] assertion 2 `_validate.py:357-391` + checker `_validate.py:231-233`; assertion 6 `_validate.py:493-532` + checker `_validate.py:276-291`.

### What a `reflect-review` recipe binding needs — CAN it reuse `bare-review-v1`?

Two paths, both satisfy assertions 2 & 6:

**Path A — reuse `bare-review-v1` (no recipe code).** Set the new `reflect-review` lens's `recipe_name="bare-review-v1"` and `normalizer_strategy="bare-review-v1"`. Both already exist in `REGISTRY` (`__init__.py:182`) and `STRATEGIES` (`__init__.py:209`), so assertions 2 & 6 pass with **zero changes to the recipes package**. Valid IF the reflect-review prompt emits the same findings-table-with-suspect output shape `BareReviewV1` normalizes. `bare_review_v1.py` ports `t2_normalize.py` (the bare-review lens shape, `__init__.py:8-9`).

**Path B — register a new `reflect-review-v1` recipe.** Add `recipes/reflect_review_v1.py` exporting a `ReflectReviewV1` class with `normalize(self, raw_output, args) -> NormalizedResult` (the structural `Recipe` Protocol, `__init__.py:121-137`), then:
1. Add a deferred import in `__init__.py` (after `__init__.py:178`).
2. Add `"reflect-review-v1": ReflectReviewV1()` to `REGISTRY` (`__init__.py:181-188`).
3. Add `"reflect-review-v1": "reflect-review-v1"` to `STRATEGIES` (`__init__.py:208-215`).
4. (Optional) add the token to `__all__` (`__init__.py:70-89`) for the back-compat `__all__` membership fallback.
Required only if reflect-review needs a DIFFERENT output shape than bare-review.

**Recommendation surfaced for the TDD:** Path A (reuse `bare-review-v1`) is the lower-risk default — the reflect-review lens is conceptually the bare-review shape applied to reflect's audit target, and reusing avoids a new recipe + its AC-011 boundary test. The TDD should confirm the prompt output shape matches before committing to Path A; if reflect-review needs a verdict/deviation-table shape distinct from a findings table, Path B is required.

[CODE-VERIFIED] `bare-review-v1` present in both `REGISTRY` `__init__.py:182` and `STRATEGIES` `__init__.py:209` — reuse satisfies assertions 2 & 6 with no recipe-package edit.

---

## Key Takeaways

1. **`ReflectConfig` lives in `models.py:57-91`, not `config.py`.** Every FR-RH2 field is a 3-file edit: dataclass field (`models.py`, append at tail after `max_fix_iterations` line 86), `resolve_config` param + resolution + constructor kwarg (`config.py`), and Click option + `run()` param + call kwarg (`commands.py`).
2. **`--depth {standard|deep}` already exists**, fully wired (`commands.py:101-106` → `config.py:190` floor → `models.py:71`). FR-RH2 must NOT re-add it. Default `standard`, choices exact, `quick`→`standard` floor.
3. **`expected_tier` is derived in the runner, not config:** `runner.py:403` `2 if config.depth in {"standard","deep"} else 1` — collapses BOTH depths to tier 2. If `deep` must map to a different expected tier, `runner.py:403` is the single mutation point; the `derive_verdict(expected_tier=...)` plumbing (`contract.py:133/216/235/263`) needs no change.
4. **`--transport` and `--reviewers` are 100% net-new** — zero occurrences in `src/superclaude/cli/reflect/`. Copy the `--depth` `click.Choice` idiom for `--transport`; plain `type=int, default=3` for `--reviewers`. Put the `[2,4]` clamp + `1`→negative-witness branch in `resolve_config` (next to `config.py:190`), NOT the Click callback — house convention keeps all resolution in `config.py`.
5. **Swarm recipe binding for `reflect-review`:** assertions 2 (`_validate.py:357-391`) and 6 (`_validate.py:493-532`) require `recipe_name` ∈ `REGISTRY` and `normalizer_strategy` ∈ `STRATEGIES`. **Reusing `bare-review-v1` (Path A) satisfies both with zero recipe-package edits** because that key exists in both dicts (`__init__.py:182, 209`). A new `reflect-review-v1` recipe (Path B) is needed only if the output shape differs.

## Gaps and Questions

- **[UNVERIFIED] `--reviewers` clamp-vs-reject semantics.** The spec says "clamp [2,4]" but also "1 = negative-witness". The codebase has NO existing `reviewers` logic to model against. Open question for the TDD: does an out-of-range value (e.g. 0, 5) silently clamp, or hard-fail with `ValueError`→exit-2 blocked? The `1` sentinel MUST be branched BEFORE any `max(2,min(4,n))` clamp or it gets rewritten to 2. Recommend explicit: `if reviewers == 1: negative_witness else clamp`.
- **[UNVERIFIED] `--transport stub` runtime wiring.** This research covers the input-resolution surface only. Whether/how `transport="stub"` selects a stub Claude process / proxy is downstream of `ReflectConfig` (in `runner.py`/`process.py`) and NOT traced here — confirm the runner consumes `config.transport` once added.
- **[UNVERIFIED] `reflect-review` lens registration file.** No `reflect-review` lens module exists in `lenses/` today (grep: zero `reflect-review`/`reflect_review` hits anywhere in `src/`). FR-RH2 must add `lenses/reflect_review.py` exporting `LENS: LensEntry`, import it in `lenses/__init__.py` (`__init__.py:49-67` import block, `__init__.py:105-114` `LENSES` dict, `__init__.py:73-82` `LENS_NAMES` tuple). That lens-registration surface is adjacent to, but distinct from, the recipe-registry surface this doc focuses on.
- **[UNVERIFIED] expected_tier promotion to config field.** Whether FR-RH2 wants `expected_tier` resolved in `config.py` (so it is testable in isolation) vs left in `runner.py:403` is a design choice the TDD should settle; current code derives it in the runner.

## Summary

The FR-RH2 input-mutation surface is a clean, well-precedented three-file chain in `src/superclaude/cli/reflect/`: append `transport: str` and `reviewers: int` to the `ReflectConfig` dataclass tail (`models.py`, after line 86), add keyword params + resolution (transport-validate / reviewers-clamp at `config.py:190` region) + constructor kwargs in `resolve_config` (`config.py:123-240`), and add two `@click.option` decorators after `--depth` plus matching `run()` params and `resolve_config(...)` kwargs in `commands.py` (after line 106, signature 148-162, call 174-190). `--depth` is already present and must not be re-added; `expected_tier` is derived from depth at `runner.py:403` (both depths → tier 2). On the swarm side, the new `reflect-review` lens's `recipe_name`/`normalizer_strategy` must resolve in `recipes/__init__.py`'s `REGISTRY` (line 181-188) and `STRATEGIES` (208-215) or lens-validator assertions 2 & 6 fail — and reusing the already-registered `bare-review-v1` binding satisfies both with no recipe-package change, making it the recommended low-risk default unless reflect-review needs a distinct output shape.

---
**Status: Complete**
