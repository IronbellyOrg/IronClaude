70fcf81c2a755c83ea5383567d714bd3eef7e11e
Review one task for spec compliance.

Task brief: ## Task 5: Write the lens table, the values file, the lens render and the cost-driven row cap

Depends on: Task 4

Follow `RL/IMPLEMENTATION.md` step 3 (lens part) and `RL/DESIGN.md` sections 5.1 to 5.4 and DR-3, DR-4, DR-7. Create `RL/config/lenses.json` exactly as `RL/DESIGN.md` 5.1 (three panels `primary`, `haiku`, `sonnet`, three roles each with `rid`, `model`, `lens`, `table_cap`, `search_form`, `reask`), `RL/config/values.json` (planning `b` per panel and document: primary 100, 120, 122; haiku 220, 238, 226; sonnet 259, 302, 269; `c` per model: ember 0.4, luna 2, haiku 4, sonnet 3; fixed 6 s, share 0.35, hard cap 14; overhead 28 s for the primary panel and 30 s for haiku and sonnet; re-ask constants 30 and 1.35; every value marked planning), `RL/rl/lens.py` (load, the six validation rules of 5.2 raising `E_LENS_INVALID`, `render(panel, has_source, b_min, c_by_model)` returning per role `rid`, `model`, `recipes`, `budgets`, `assigned_ids`, `row_cap`, `search_form`, `reask`, `no_budget`, `lens_row_cap(b, c, table_cap) = min(table_cap, floor((0.35 b - 6) / c))`, `assigned_ids`; C2 dropped from every lens when `has_source` is false) and `RL/fixtures/lens/make_lens.py` (F-LENS: a valid table plus one invalid variant per rule of 5.2, and a C9 variant with card, recipe and placement). Model names pass `sw_assert_model` (K2).

Write `RL/tests/test_lens.py`: `test_duplicated_classes_equal_req25` (primary {C2, C4}, haiku {C1}, sonnet {C1, C7}), `test_search_form_only_in_search_role`, `test_row_cap_per_panel` (14/14/14, 6/14/12, 8/12/12), `test_row_cap_formula_table` (b=100: c 2.00 gives 14, 2.07 gives 14, 2.41 gives 12, 2.50 gives 11, 3.00 gives 9; b=122: c 2.00 gives 14, c 3.00 gives 12; b=60, c 2.00 gives 7), `test_no_budget_refuses`, `test_every_lens_keeps_two_recipes_without_c2` (DR-7), `test_fixture_class_c9_needs_no_code_change` (REQ-10), one test per invalid-table variant, `test_render_under_one_second`, and `RL/tests/test_model_allowlist_rl.py` (K2: every `model` in `lenses.json` passes `sw_assert_model`; `claude-opus-5-5` appears under `RL/bin`, `RL/rl`, `RL/scaffold` only in `bin/judge-one.sh`, which Task 14 creates, so the Opus half of this test is written in Task 14).

Acceptance criteria (ids added by the orchestrator, in source order):
T5.AC1: `$T $RL/tests/test_lens.py -q` exits 0 and covers REQ-10, REQ-25 (lens part), REQ-26 (cap part), DR-4 and DR-7.
T5.AC2: `RL/config/lenses.json` validates by the six rules of `RL/DESIGN.md` 5.2, each class is in at least one lens of every panel, and every lens holds 2 to 4 recipes.
T5.AC3: `lens_row_cap` returns the table values of `RL/DESIGN.md` 5.4 for all eight rows, and a cap below the number of recipes in a lens sets `no_budget`.
T5.AC4: Rendering one panel plus one brief takes under 1 second on the fixture.

Global constraints: ## Constraints

Path names used by every task (all repo-relative to the checkout root `REPO`, which is `git rev-parse --show-toplevel`):

- `RL` is `.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger`. It holds `DESIGN.md`, `TESTING.md`, `IMPLEMENTATION.md` and `SHARED-MANIFEST-DESIGN-TIME.tsv`, which are the specification and are never edited by the build.
- `SW` is `.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet`, the sibling build (Redesign 1). It is read only: no task writes, edits, moves or deletes anything under it, and no task runs a script or a test from inside it.
- `MR` is `.dev/brainstorms/20261113-223124-panel-process-redesign/merged-requirements.md` (sections 3.0, 3.2, 5 and 6 are the requirements source; the design documents already map them). `EVAL` is `.dev/eval-workspaces/tasklist-review-panel/20261111-a1` (read only).
- Design ids: `K1` to `K9` (constraints), `DR-1` to `DR-16` (decisions) and `REQ-nn` (requirements) are those of `RL/DESIGN.md` sections 1.2 and 1.3 and of `RL/TESTING.md` section 3.

Scope rules that hold for every task:

- Create or edit files only under `RL`, plus scratch under `/tmp` (sandboxes under `/tmp/evalsb-recipe`, scratch under `/tmp/rl-*`). Nothing under `src/`, `tests/`, `.claude/`, any existing folder under `.dev/tasks/`, `SW`, `EVAL`, `.dev/eval-workspaces/tasklist-review-panel/20261113-collab` or any other folder is changed.
- No task runs `git commit` or `git push`, and no task runs `git add` for a path under `RL`. The freeze tag (K5) is only printed, never created.
- No task opens, reads, greps the content of or copies any `ground-truth*.json`, score file or judge output of a study package, and no recipe, card, brief, fixture, regex or example uses a study answer. Fixtures are invented. Tests that need ground truth use the synthetic `RL/fixtures/gt/` files only. The tests marked `freeze` (they read the real ground truth or need a second author's records) are never run by this build.
- Python runs only through uv. No `python -m`, no bare `pip`. No code folder is named `lib/` (K7).
- No reviewer or judge session is started and no network call is made. Tests use the fake `claude` at `RL/tests/fakes/claude`. If a task ever needed a model it would use `claude-sonnet-5-5` or `claude-haiku-5-5`; Opus is only the blind judge script's model; never Qwen or glm.
- Files under `RL/scaffold/`, `RL/cards/`, `RL/briefs/`, `RL/bin/common.sh`, `RL/bin/build-sandbox.sh` and the copied tests are copies of sibling files and are never edited after the copy (DESIGN 3.1). A copied test that fails is reported, not edited.
- Shell variables used in task commands:

```
REPO=$(git rev-parse --show-toplevel)
RL=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger
SW=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet
MR=$REPO/.dev/brainstorms/20261113-223124-panel-process-redesign/merged-requirements.md
T="uv run --frozen --project $REPO pytest -p no:cacheprovider"
PYRUN="uv run --frozen --project $REPO python"
export PYTHONDONTWRITEBYTECODE=1 NOFALLBACK=1 SUPERCLAUDE_CODEGRAPH_AUTOINIT=0
```


Start sha: 70fcf81c2a755c83ea5383567d714bd3eef7e11e
Diff against the start snapshot: diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/config/lenses.json b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/config/lenses.json
new file mode 100644
index 000000000..6eab7055c
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/config/lenses.json
@@ -0,0 +1,18 @@
+{
+  "schema": "rl-lenses/1",
+  "version": 1,
+  "panels": {
+    "primary": {"label": "ember + 2x luna", "roles": {
+      "S":  {"rid": "t2b-1", "model": "muse-ember-1.0", "lens": ["C4", "C5", "C6", "C8"], "table_cap": 14, "search_form": true,  "reask": true},
+      "L1": {"rid": "t4-1",  "model": "gpt-6-luna",     "lens": ["C1", "C2", "C3"],       "table_cap": 14, "search_form": false, "reask": false},
+      "L2": {"rid": "t3-1",  "model": "gpt-6-luna",     "lens": ["C2", "C4", "C7"],       "table_cap": 14, "search_form": false, "reask": false}}},
+    "haiku": {"label": "haiku + 2x luna", "roles": {
+      "S":  {"rid": "t2-1",  "model": "claude-haiku-5-5", "lens": ["C5", "C6", "C8"],     "table_cap": 6,  "search_form": true,  "reask": false},
+      "L1": {"rid": "t4-1",  "model": "gpt-6-luna",       "lens": ["C1", "C2", "C3"],     "table_cap": 14, "search_form": false, "reask": false},
+      "L2": {"rid": "t3-1",  "model": "gpt-6-luna",       "lens": ["C1", "C4", "C7"],     "table_cap": 12, "search_form": false, "reask": false}}},
+    "sonnet": {"label": "sonnet + 2x luna", "roles": {
+      "S":  {"rid": "t1b-1", "model": "claude-sonnet-5-5", "lens": ["C5", "C6", "C8", "C2"], "table_cap": 8, "search_form": true,  "reask": false},
+      "L1": {"rid": "t4-1",  "model": "gpt-6-luna",        "lens": ["C1", "C3", "C7"],       "table_cap": 12, "search_form": false, "reask": false},
+      "L2": {"rid": "t3-1",  "model": "gpt-6-luna",        "lens": ["C4", "C7", "C1"],       "table_cap": 12, "search_form": false, "reask": false}}}
+  }
+}
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/config/values.json b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/config/values.json
new file mode 100644
index 000000000..17a21bca3
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/config/values.json
@@ -0,0 +1,14 @@
+{
+ "schema": "rl-values/1",
+ "status": "planning",
+ "note": "Every value in this file is a planning value (UNVERIFIED), from DESIGN 5.4 and 10. A measured value is recorded next to its planning value, never over it.",
+ "b": {
+  "primary": {"TASK-WF-designSpec-20261107-075614": 100, "TASK-WF-makeTheAliasOnly-20261105-051649": 120, "TASK-WF-design-20261108-041415": 122},
+  "haiku": {"TASK-WF-designSpec-20261107-075614": 220, "TASK-WF-makeTheAliasOnly-20261105-051649": 238, "TASK-WF-design-20261108-041415": 226},
+  "sonnet": {"TASK-WF-designSpec-20261107-075614": 259, "TASK-WF-makeTheAliasOnly-20261105-051649": 302, "TASK-WF-design-20261108-041415": 269}
+ },
+ "c": {"muse-ember-1.0": 0.4, "gpt-6-luna": 2, "claude-haiku-5-5": 4, "claude-sonnet-5-5": 3},
+ "row_cap": {"fixed_s": 6, "share": 0.35, "hard_cap": 14},
+ "overhead_s": {"primary": 28, "haiku": 30, "sonnet": 30},
+ "reask": {"fixed_s": 30, "factor": 1.35}
+}
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/fixtures/lens/make_lens.py b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/fixtures/lens/make_lens.py
new file mode 100644
index 000000000..8b45b6cea
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/fixtures/lens/make_lens.py
@@ -0,0 +1,103 @@
+"""F-LENS (TESTING section 2): lens tables built in a temporary folder, by code.
+
+`valid_table()` is a copy of config/lenses.json. `invalid_tables()` gives one table per way to break a rule of
+DESIGN 5.2, with the rule number it must trip. `build_c9(root)` writes a copy of the cards and of the recipes with a
+ninth class (card, recipe, lens placement) and a lens table that places it; nothing in the code changes for it.
+"""
+
+import copy
+import json
+import shutil
+from pathlib import Path
+from types import SimpleNamespace
+
+RL = Path(__file__).resolve().parents[2]
+
+
+def valid_table() -> dict:
+    return json.loads((RL / "config" / "lenses.json").read_text(encoding="utf-8"))
+
+
+def _roles(table, panel="primary"):
+    return table["panels"][panel]["roles"]
+
+
+def invalid_tables() -> dict[str, tuple[int, dict]]:
+    """{variant name: (rule of DESIGN 5.2 that it breaks, table)}; each differs from the valid table by one edit."""
+    v: dict[str, tuple[int, dict]] = {}
+
+    def make(name, rule, edit):
+        t = copy.deepcopy(valid_table())
+        edit(t)
+        v[name] = (rule, t)
+
+    make(
+        "class_in_no_lens", 1, lambda t: _roles(t)["S"].update(lens=["C4", "C5", "C6"])
+    )
+    make(
+        "five_recipes",
+        2,
+        lambda t: _roles(t)["S"].update(lens=["C4", "C5", "C6", "C8", "C1"]),
+    )
+    make("one_recipe", 2, lambda t: _roles(t)["L1"].update(lens=["C1"]))
+    make(
+        "repeated_recipe", 2, lambda t: _roles(t)["L1"].update(lens=["C1", "C1", "C3"])
+    )
+    make(
+        "recipe_without_text",
+        2,
+        lambda t: _roles(t)["L1"].update(lens=["C1", "C3", "C9"]),
+    )
+    make("table_cap_15", 3, lambda t: _roles(t)["L1"].update(table_cap=15))
+    make("table_cap_below_count", 3, lambda t: _roles(t)["S"].update(table_cap=3))
+    make("unknown_model", 4, lambda t: _roles(t)["L1"].update(model="claude-opus-5-5"))
+    make("two_search_roles", 4, lambda t: _roles(t)["L1"].update(search_form=True))
+    make("no_search_role", 4, lambda t: _roles(t)["S"].update(search_form=False))
+    make("reask_on_haiku", 4, lambda t: _roles(t, "haiku")["S"].update(reask=True))
+    make("no_reask_on_primary", 4, lambda t: _roles(t)["S"].update(reask=False))
+    make("repeated_rid", 4, lambda t: _roles(t)["L2"].update(rid="t4-1"))
+    make(
+        "duplicated_set_differs",
+        5,
+        lambda t: _roles(t, "haiku")["L2"].update(lens=["C4", "C7", "C3"]),
+    )
+    make(
+        "lens_empties_without_c2",
+        6,
+        lambda t: _roles(t, "sonnet")["L1"].update(lens=["C2", "C3"]),
+    )
+    return v
+
+
+def write_table(path: Path, table: dict) -> Path:
+    path.parent.mkdir(parents=True, exist_ok=True)
+    path.write_text(
+        json.dumps(table, indent=1, sort_keys=True) + "\n", encoding="utf-8"
+    )
+    return path
+
+
+def build_c9(root: Path) -> SimpleNamespace:
+    """Cards, recipes and a lens table that hold a class C9, under root. C9 is appended to the L1 lens of every panel."""
+    cards = root / "cards"
+    shutil.copytree(RL / "cards", cards)
+    card = json.loads((cards / "C8.json").read_text(encoding="utf-8"))
+    card.update(id="C9", name="Invented ninth class")
+    (cards / "C9.json").write_text(json.dumps(card, indent=2) + "\n", encoding="utf-8")
+    data = json.loads((RL / "recipes" / "recipes.json").read_text(encoding="utf-8"))
+    data["recipes"]["C9"] = {
+        "version": 1,
+        "text": "Compare the two named lists item by item and name the first item that differs. Write at most 4 rows.",
+    }
+    without = copy.deepcopy(data)
+    del without["recipes"]["C9"]
+    table = valid_table()
+    for panel in table["panels"]:
+        _roles(table, panel)["L1"]["lens"].append("C9")
+    return SimpleNamespace(
+        cards_dir=cards,
+        recipes_path=write_table(root / "recipes.json", data),
+        recipes_missing_path=write_table(root / "recipes-no-c9.json", without),
+        lenses_path=write_table(root / "lenses.json", table),
+        table=table,
+    )
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/rl/lens.py b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/rl/lens.py
new file mode 100644
index 000000000..a5ec932c8
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/rl/lens.py
@@ -0,0 +1,227 @@
+"""Lens table and lens render (DESIGN 5, R1, DR-3, DR-4, DR-7).
+
+config/lenses.json says which recipes each reviewer of each panel gets. It is data: a new panel, model or class
+placement is an edit of that file, with no change here. `validate` returns the breaks of the six rules of 5.2 as
+"rule N: ..." strings; `load` raises LensInvalid (message starts with E_LENS_INVALID) when there is any.
+
+`render` returns {role: {...}} in table order. `recipes` is the list of recipe ids (C2 left out when there is no
+source); a recipe prints as `R-C<n>. <text>` (`printed`). `assigned_ids` are the row ids the row check accepts (DR-5).
+"""
+
+from __future__ import annotations
+
+import json
+import math
+import re
+from fractions import Fraction
+from functools import lru_cache
+from pathlib import Path
+
+from rl import recipes as recipes_mod
+from scaffold import cards as cards_mod
+
+RL = Path(__file__).resolve().parents[1]
+LENSES_JSON = RL / "config" / "lenses.json"
+VALUES_JSON = RL / "config" / "values.json"
+COMMON_SH = RL / "bin" / "common.sh"
+SCHEMA = "rl-lenses/1"
+E_LENS_INVALID = "E_LENS_INVALID"
+LENS_MIN, LENS_MAX = 2, 4
+ROLE_KEYS = {"rid", "model", "lens", "table_cap", "search_form", "reask"}
+# REQ-25: the classes that two reviewers of one panel both hold (MR 3.2(a))
+REQ25_DUPLICATES = {"primary": {"C2", "C4"}, "haiku": {"C1"}, "sonnet": {"C1", "C7"}}
+REASK_PANEL = "primary"
+NO_SOURCE_CLASS = "C2"
+
+
+class LensInvalid(ValueError):
+    """The lens table breaks a rule of DESIGN 5.2 (configuration error; the launcher falls back to Z0)."""
+
+
+@lru_cache(maxsize=None)
+def allowed_models() -> tuple[str, ...]:
+    """The reviewer allowlist K2, read from the one place that holds it: ALLOWED_MODELS in bin/common.sh."""
+    m = re.search(r'^ALLOWED_MODELS="([^"]*)"', COMMON_SH.read_text(), re.M)
+    return tuple(m.group(1).split()) if m else ()
+
+
+@lru_cache(maxsize=None)
+def _values(path: str) -> dict:
+    return json.loads(Path(path).read_text(encoding="utf-8"))
+
+
+def values(path: Path | str | None = None) -> dict:
+    """The planning values of config/values.json (b, c, row cap constants, overhead, re-ask constants)."""
+    return _values(str(path or VALUES_JSON))
+
+
+def lens_row_cap(
+    b: float, c: float, table_cap: int, share=None, fixed=None, hard_cap=None
+) -> int:
+    """DR-4: min(table_cap, floor((share * b - fixed) / c)), never below 0 and never above the hard cap.
+
+    b: smallest same-block Z0 median of the panel (s); c: seconds per ledger row of the reviewer's model. The
+    division is exact (Fractions of the decimal text), so 14.0 or 12.0 at a table value never becomes 13.999.
+    """
+    k = values()["row_cap"]
+    share = k["share"] if share is None else share
+    fixed = k["fixed_s"] if fixed is None else fixed
+    hard_cap = k["hard_cap"] if hard_cap is None else hard_cap
+    if c <= 0:
+        raise ValueError(f"cost per row must be positive, got {c}")
+    exact = (Fraction(str(share)) * Fraction(str(b)) - Fraction(str(fixed))) / Fraction(
+        str(c)
+    )
+    return max(0, min(table_cap, hard_cap, math.floor(exact)))
+
+
+def assigned_ids(recipe_ids, recipes: dict | None = None) -> list[str]:
+    """`C<n>.1 ... C<n>.<N>` for every recipe in order, N the recipe's row budget (DR-5)."""
+    recipes = recipes or recipes_mod.load()
+    return [
+        f"{rid}.{k}"
+        for rid in recipe_ids
+        for k in range(1, recipes_mod.row_budget(rid, recipes) + 1)
+    ]
+
+
+def printed(recipe_id: str, recipes: dict | None = None) -> str:
+    """How a recipe appears in a brief (DESIGN 4.1): `R-C<n>. <text>`."""
+    return f"R-{recipe_id}. {(recipes or recipes_mod.load())[recipe_id]['text']}"
+
+
+def validate(
+    table: dict, card_ids=None, recipes=None, models=None, duplicates=None
+) -> list[str]:
+    """Every break of the six rules of DESIGN 5.2, as "rule N: ..." strings; [] means the table is sound.
+
+    card_ids defaults to the ids in cards/, recipes to the ids in recipes.json, models to the K2 allowlist and
+    duplicates to REQ25_DUPLICATES.
+    """
+    ids = set(cards_mod.load() if card_ids is None else card_ids)
+    have = set(recipes_mod.load() if recipes is None else recipes)
+    models = allowed_models() if models is None else models
+    duplicates = REQ25_DUPLICATES if duplicates is None else duplicates
+    cap = values()["row_cap"]["hard_cap"]
+    errs: list[str] = []
+    panels = table.get("panels") if isinstance(table, dict) else None
+    if not isinstance(panels, dict) or not panels or table.get("schema") != SCHEMA:
+        return [f"rule 0: schema is not {SCHEMA} or there are no panels"]
+    for name, panel in panels.items():
+        roles = panel.get("roles") if isinstance(panel, dict) else None
+        if not isinstance(roles, dict) or not roles:
+            errs.append(f"rule 0: panel {name} has no roles")
+            continue
+        bad = [
+            r
+            for r, v in roles.items()
+            if not isinstance(v, dict) or set(v) != ROLE_KEYS
+        ]
+        if bad:
+            errs.append(
+                f"rule 0: panel {name} roles {bad} do not have exactly {sorted(ROLE_KEYS)}"
+            )
+            continue
+        lenses = {r: v["lens"] for r, v in roles.items()}
+        held = [c for lens in lenses.values() for c in lens]
+        for c in sorted(ids - set(held)):
+            errs.append(f"rule 1: panel {name}: class {c} is in no lens")
+        for r, lens in lenses.items():
+            where = f"panel {name} role {r}"
+            if not LENS_MIN <= len(lens) <= LENS_MAX or len(set(lens)) != len(lens):
+                errs.append(
+                    f"rule 2: {where}: lens {lens} needs {LENS_MIN} to {LENS_MAX} different recipes"
+                )
+            errs.extend(
+                f"rule 2: {where}: recipe {c} does not exist"
+                for c in lens
+                if c not in have
+            )
+            tc = roles[r]["table_cap"]
+            if (
+                not isinstance(tc, int)
+                or isinstance(tc, bool)
+                or not len(lens) <= tc <= cap
+            ):
+                errs.append(
+                    f"rule 3: {where}: table_cap {tc!r} outside {len(lens)} to {cap}"
+                )
+            if roles[r]["model"] not in models:
+                errs.append(
+                    f"rule 4: {where}: model {roles[r]['model']!r} is not an allowed reviewer model"
+                )
+            kept = [c for c in lens if c != NO_SOURCE_CLASS]
+            if len(kept) < LENS_MIN:
+                errs.append(
+                    f"rule 6: {where}: lens {lens} keeps {len(kept)} recipes without {NO_SOURCE_CLASS}"
+                )
+        rids = [v["rid"] for v in roles.values()]
+        if len(set(rids)) != len(rids):
+            errs.append(f"rule 4: panel {name}: rid repeats in {rids}")
+        if sum(v["search_form"] is True for v in roles.values()) != 1:
+            errs.append(
+                f"rule 4: panel {name}: exactly one role needs search_form true"
+            )
+        asks = sum(v["reask"] is True for v in roles.values())
+        if asks != (1 if name == REASK_PANEL else 0):
+            errs.append(f"rule 4: panel {name}: {asks} roles have reask true")
+        twice = {c for c in held if held.count(c) > 1}
+        if name in duplicates and twice != set(duplicates[name]):
+            errs.append(
+                f"rule 5: panel {name}: duplicated classes {sorted(twice)} differ from {sorted(duplicates[name])}"
+            )
+    errs.extend(
+        f"rule 5: panel {p} is not in the REQ-25 list"
+        for p in sorted(set(duplicates) - set(panels))
+    )
+    return errs
+
+
+def load(path: Path | str | None = None, **kw) -> dict:
+    """The parsed lens table; raises LensInvalid (E_LENS_INVALID) when `validate` finds anything."""
+    try:
+        table = json.loads(Path(path or LENSES_JSON).read_text(encoding="utf-8"))
+    except (OSError, ValueError) as e:
+        raise LensInvalid(f"{E_LENS_INVALID}: cannot read the lens table: {e}") from e
+    errs = validate(table, **kw)
+    if errs:
+        raise LensInvalid(f"{E_LENS_INVALID}: " + "; ".join(errs))
+    return table
+
+
+def render(
+    panel: str,
+    has_source: bool,
+    b_min: float,
+    c_by_model: dict,
+    table: dict | None = None,
+    recipes: dict | None = None,
+) -> dict[str, dict]:
+    """The lens of every role of one panel (DESIGN 5.3): {role: {rid, model, recipes, budgets, assigned_ids,
+    row_cap, search_form, reask, no_budget}}.
+
+    row_cap = min(lens_row_cap(b_min, c_model, table_cap), sum of the budgets); no_budget when it is below the
+    number of recipes (one row per recipe is the least that makes a ledger mean anything).
+    """
+    table = load() if table is None else table
+    recipes = recipes_mod.load() if recipes is None else recipes
+    out = {}
+    for role, spec in table["panels"][panel]["roles"].items():
+        ids = [c for c in spec["lens"] if has_source or c != NO_SOURCE_CLASS]
+        budgets = {c: recipes_mod.row_budget(c, recipes) for c in ids}
+        cap = min(
+            lens_row_cap(b_min, c_by_model[spec["model"]], spec["table_cap"]),
+            sum(budgets.values()),
+        )
+        out[role] = {
+            "rid": spec["rid"],
+            "model": spec["model"],
+            "recipes": ids,
+            "budgets": budgets,
+            "assigned_ids": assigned_ids(ids, recipes),
+            "row_cap": cap,
+            "search_form": spec["search_form"],
+            "reask": spec["reask"],
+            "no_budget": cap < len(ids),
+        }
+    return out
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/tests/test_lens.py b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/tests/test_lens.py
new file mode 100644
index 000000000..88b9a1369
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/tests/test_lens.py
@@ -0,0 +1,230 @@
+"""REQ-10, REQ-25 (lens part), REQ-26 (cap part), DR-4, DR-7: config/lenses.json, config/values.json and rl/lens.py."""
+
+import json
+import time
+
+import pytest
+from helpers import SW
+
+from fixtures.lens.make_lens import build_c9, invalid_tables, valid_table, write_table
+from rl import lens, recipes
+from scaffold import cards
+
+TABLE = json.loads((SW / "config" / "lenses.json").read_text(encoding="utf-8"))
+VALUES = json.loads((SW / "config" / "values.json").read_text(encoding="utf-8"))
+PANELS = ("primary", "haiku", "sonnet")
+B_MIN = {p: min(v.values()) for p, v in VALUES["b"].items()}
+# REQ-25, from MR 3.2(a); written out here on purpose so a change of the table or of lens.py cannot move it
+REQ25 = {"primary": {"C2", "C4"}, "haiku": {"C1"}, "sonnet": {"C1", "C7"}}
+ROLE_KEYS = {"rid", "model", "lens", "table_cap", "search_form", "reask"}
+FIELDS = {
+    "rid",
+    "model",
+    "recipes",
+    "budgets",
+    "assigned_ids",
+    "row_cap",
+    "search_form",
+    "reask",
+    "no_budget",
+}
+
+
+def render(panel, has_source=True, **kw):
+    return lens.render(panel, has_source, B_MIN[panel], VALUES["c"], **kw)
+
+
+def test_table_shape_and_rules():
+    assert TABLE["schema"] == "rl-lenses/1" and set(TABLE["panels"]) == set(PANELS)
+    assert lens.validate(TABLE) == [] and lens.load() == TABLE
+    for panel in TABLE["panels"].values():
+        assert set(panel["roles"]) == {"S", "L1", "L2"}
+        for role in panel["roles"].values():
+            assert set(role) == ROLE_KEYS and 2 <= len(role["lens"]) <= 4
+
+
+def test_every_class_in_every_panel():
+    ids = set(cards.load())
+    for panel in TABLE["panels"].values():
+        assert {c for r in panel["roles"].values() for c in r["lens"]} == ids
+
+
+def test_values_file_is_all_planning():
+    assert VALUES["status"] == "planning" and "planning" in VALUES["note"]
+    assert VALUES["c"] == {
+        "muse-ember-1.0": 0.4,
+        "gpt-6-luna": 2,
+        "claude-haiku-5-5": 4,
+        "claude-sonnet-5-5": 3,
+    }
+    assert [sorted(v.values()) for v in VALUES["b"].values()] == [
+        [100, 120, 122],
+        [220, 226, 238],
+        [259, 269, 302],
+    ]
+    assert VALUES["row_cap"] == {"fixed_s": 6, "share": 0.35, "hard_cap": 14}
+    assert VALUES["overhead_s"] == {"primary": 28, "haiku": 30, "sonnet": 30}
+    assert VALUES["reask"] == {"fixed_s": 30, "factor": 1.35}
+
+
+def test_duplicated_classes_equal_req25():
+    for panel, want in REQ25.items():
+        held = [c for r in render(panel).values() for c in r["recipes"]]
+        assert {c for c in held if held.count(c) > 1} == want, panel
+
+
+def test_search_form_only_in_search_role():
+    for panel in PANELS:
+        flags = {role: r["search_form"] for role, r in render(panel).items()}
+        assert flags == {"S": True, "L1": False, "L2": False}, panel
+    asks = {p: [r for r, v in render(p).items() if v["reask"]] for p in PANELS}
+    assert asks == {"primary": ["S"], "haiku": [], "sonnet": []}
+
+
+def test_row_cap_per_panel():
+    caps = {p: [r["row_cap"] for r in render(p).values()] for p in PANELS}
+    assert caps == {
+        "primary": [14, 14, 14],
+        "haiku": [6, 14, 12],
+        "sonnet": [8, 12, 12],
+    }
+    assert not any(r["no_budget"] for p in PANELS for r in render(p).values())
+
+
+@pytest.mark.parametrize(
+    ("b", "c", "want"),
+    [
+        (100, 2.00, 14),
+        (100, 2.07, 14),
+        (100, 2.41, 12),
+        (100, 2.50, 11),
+        (100, 3.00, 9),
+        (122, 2.00, 14),
+        (122, 3.00, 12),
+        (60, 2.00, 7),
+    ],
+)
+def test_row_cap_formula_table(b, c, want):
+    assert lens.lens_row_cap(b, c, 14) == want
+
+
+def test_row_cap_formula_edges():
+    # the break-even at b = 100 is 29 / 14 = 2.0714...: just below it 14 rows fit, just above only 13
+    assert lens.lens_row_cap(100, 2.0714, 14) == 14
+    assert lens.lens_row_cap(100, 2.0715, 14) == 13
+    assert (
+        lens.lens_row_cap(122, 2.0, 99) == 14
+    )  # the hard cap holds even for a large table_cap
+    assert lens.lens_row_cap(10, 2.0, 14) == 0  # 3.5 - 6 is negative: never below 0
+    with pytest.raises(ValueError):
+        lens.lens_row_cap(100, 0, 14)
+
+
+def test_no_budget_refuses():
+    slow = dict(
+        VALUES["c"], **{"gpt-6-luna": 12.0}
+    )  # 29 / 12 = 2 rows for a lens of 3 recipes
+    out = lens.render("primary", True, 100, slow)
+    assert out["L1"]["row_cap"] == 2 and out["L1"]["no_budget"] is True
+    assert out["L2"]["no_budget"] is True and out["S"]["no_budget"] is False
+    exactly = dict(
+        VALUES["c"], **{"gpt-6-luna": 9.6}
+    )  # 29 / 9.6 = 3.02: one row per recipe is enough
+    out = lens.render("primary", True, 100, exactly)
+    assert out["L1"]["row_cap"] == 3 and out["L1"]["no_budget"] is False
+
+
+def test_assigned_ids():
+    out = render("primary")
+    assert out["L1"]["assigned_ids"] == [
+        f"{c}.{k}"
+        for c, n in (("C1", 4), ("C2", 6), ("C3", 4))
+        for k in range(1, n + 1)
+    ]
+    assert out["L1"]["budgets"] == {"C1": 4, "C2": 6, "C3": 4}
+    assert lens.assigned_ids(["C7"]) == ["C7.1", "C7.2", "C7.3", "C7.4"]
+    r = recipes.load()
+    assert lens.printed("C7", r) == f"R-C7. {r['C7']['text']}"
+
+
+def test_render_fields_and_models():
+    for panel in PANELS:
+        out = render(panel)
+        for role, r in out.items():
+            spec = TABLE["panels"][panel]["roles"][role]
+            assert set(r) == FIELDS
+            assert (r["rid"], r["model"], r["recipes"]) == (
+                spec["rid"],
+                spec["model"],
+                spec["lens"],
+            )
+            assert r["row_cap"] <= sum(r["budgets"].values())
+
+
+def test_every_lens_keeps_two_recipes_without_c2():
+    for panel in PANELS:
+        for role, r in render(panel, has_source=False).items():
+            assert "C2" not in r["recipes"] and len(r["recipes"]) >= 2, (panel, role)
+            assert not any(i.startswith("C2.") for i in r["assigned_ids"])
+            assert "C2" not in r["budgets"]
+    assert render("primary")["L1"]["recipes"] == ["C1", "C2", "C3"]
+    assert render("primary", False)["L1"]["recipes"] == ["C1", "C3"]
+    assert render("sonnet", False)["S"]["recipes"] == ["C5", "C6", "C8"]
+
+
+def test_fixture_class_c9_needs_no_code_change(tmp_path):
+    f = build_c9(tmp_path)
+    ids = cards.load(f.cards_dir)
+    assert "C9" in ids
+    data = json.loads(f.recipes_path.read_text(encoding="utf-8"))["recipes"]
+    assert lens.validate(f.table, card_ids=ids, recipes=data) == []
+    out = lens.render("primary", True, 100, VALUES["c"], table=f.table, recipes=data)
+    assert out["L1"]["recipes"] == ["C1", "C2", "C3", "C9"]
+    assert "C9.1" in out["L1"]["assigned_ids"] and "C9.4" in out["L1"]["assigned_ids"]
+    assert lens.printed("C9", data).startswith("R-C9. Compare the two named lists")
+    assert out["L1"]["row_cap"] == 14
+    # the recipe entry removed: the table is invalid, and so is the recipes file (card without recipe)
+    gone = json.loads(f.recipes_missing_path.read_text(encoding="utf-8"))["recipes"]
+    assert any(
+        "rule 2" in e and "C9" in e
+        for e in lens.validate(f.table, card_ids=ids, recipes=gone)
+    )
+    assert recipes.validate({"schema": "rl-recipes/1", "recipes": gone}, ids)
+    # and the placement removed: the card exists but no lens holds it
+    plain = valid_table()
+    assert any(
+        "rule 1" in e and "C9" in e
+        for e in lens.validate(plain, card_ids=ids, recipes=data)
+    )
+
+
+def test_load_reads_a_table_file(tmp_path):
+    assert lens.load(write_table(tmp_path / "ok.json", valid_table())) == valid_table()
+    with pytest.raises(lens.LensInvalid, match="E_LENS_INVALID"):
+        lens.load(tmp_path / "missing.json")
+
+
+@pytest.mark.parametrize("name", sorted(invalid_tables()))
+def test_invalid_table_is_refused(name, tmp_path):
+    rule, table = invalid_tables()[name]
+    errs = lens.validate(table)
+    assert any(e.startswith(f"rule {rule}:") for e in errs), (name, errs)
+    with pytest.raises(lens.LensInvalid, match="E_LENS_INVALID"):
+        lens.load(write_table(tmp_path / f"{name}.json", table))
+
+
+def test_every_rule_has_a_variant():
+    assert {rule for rule, _ in invalid_tables().values()} == {1, 2, 3, 4, 5, 6}
+    assert lens.validate(valid_table()) == []
+
+
+def test_missing_schema_is_refused():
+    assert lens.validate({"panels": TABLE["panels"]}) and lens.validate({})
+
+
+def test_render_under_one_second():
+    t0 = time.perf_counter()
+    for panel in PANELS:
+        render(panel)
+        render(panel, has_source=False)
+    assert time.perf_counter() - t0 < 1.0
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/tests/test_model_allowlist_rl.py b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/tests/test_model_allowlist_rl.py
new file mode 100644
index 000000000..74573ce57
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/tests/test_model_allowlist_rl.py
@@ -0,0 +1,38 @@
+"""K2 for RL: every model of the lens table is an allowed reviewer model; the judge model is not in the code yet.
+
+Task 14 extends this file with the Opus half (`claude-opus-5-5` appears under bin/, rl/ and scaffold/ only in
+bin/judge-one.sh, which Task 14 creates). Until then it must appear nowhere.
+"""
+
+import json
+
+from helpers import REVIEWERS, SW, sh
+
+from rl import lens
+
+JUDGE = "claude-opus-5-5"
+
+
+def test_lens_models_are_allowed():
+    table = json.loads((SW / "config" / "lenses.json").read_text(encoding="utf-8"))
+    models = {r["model"] for p in table["panels"].values() for r in p["roles"].values()}
+    assert models == set(REVIEWERS)
+    for m in sorted(models):
+        assert sh(f"sw_assert_model {m}").returncode == 0, m
+
+
+def test_lens_module_allowlist_is_the_shell_allowlist():
+    assert set(lens.allowed_models()) == set(REVIEWERS)
+    assert sh(f"sw_assert_model {JUDGE}").returncode == 1
+
+
+def test_opus_nowhere_yet():
+    hits = [
+        str(p.relative_to(SW))
+        for sub in ("bin", "rl", "scaffold")
+        for p in sorted((SW / sub).rglob("*"))
+        if p.is_file()
+        and "__pycache__" not in p.parts
+        and JUDGE in p.read_text(encoding="utf-8", errors="replace")
+    ]
+    assert hits == []  # Task 14 allows exactly ["bin/judge-one.sh"]

Codegraph context: index_state: fresh; checked_at: 2026-11-14T23:20:38Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel; projectPath: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
call codegraph only when index_state: fresh, never to widen scope
Q2b: this task changes no existing symbol; the files it creates are new, so there are no dependents outside the diff.

Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
Saved-probe re-check hit locations (may be empty): 

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
