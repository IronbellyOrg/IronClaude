3fcda2559111a21ecba12be20c060f1cc805f6c8
Review one task for spec compliance.

Task brief: ## Task 4: Write the recipes file, the RL block, the search-form line and the recipes README

Depends on: Task 3

Follow `RL/IMPLEMENTATION.md` step 2 and `RL/DESIGN.md` sections 4.1 to 4.6, 6.3 and 11.3. Create `RL/recipes/recipes.json` (schema `rl-recipes/1`, version 1, the eight recipes of `RL/DESIGN.md` 4.2 byte for byte from the quoted text of `MR` 3.2(a), each ending with exactly one sentence `Write at most N rows.`, C2 with 6 and the others with 4), `RL/recipes/rl-block.txt` (the `MR` 3.2(a) ledger rule with `{{LENS_ROW_CAP}}` in place of 14, `RL/DESIGN.md` 6.3), `RL/recipes/search-form.txt` (`RL/DESIGN.md` 4.5), `RL/rl/recipes.py` (load, `row_budget(id)`, validation: key set equals the card ids of `RL/cards/` (DR-1), at most 120 words, one budget sentence with N from 1 to 14, no `src/superclaude/` path, no expected-outcome words `expected`, `should find`, `will find`, `you will see`), `RL/recipes/README.md` (the re-derive table of `RL/DESIGN.md` 11.3 with a row per target type for plan, specification and documentation covering each of: meaning of edits, meaning of tests and gate, meaning of source, command dialect, test and root-document paths, severity guidance, snapshot, lens assignment; its first lines say the sibling's extractor sentences do not apply; REQ-38) and `RL/recipes/REVIEWS.md` (eight rows C1 to C8 with status OPEN, reviewer and date empty; REQ-08). A one-time helper `RL/rl/extract_mr.py` may extract the quoted blocks from `MR` 3.2(a) and prints a diff against the `recipes.json` text.

Write tests with the invented synthetic ground truth `RL/fixtures/gt/lint-gt.json` (F-LINT-GT): `RL/tests/test_recipes.py` (key sets equal card ids, at most 120 words with the counts 71, 89, 56, 99, 86, 93, 50, 67, budget sentence once and parsed, text equals the `MR` quote while no `override` entry exists, no `src/superclaude/` path, recipe text only in one file; REQ-06, REQ-09, REQ-25), `RL/tests/test_recipes_readme.py` (REQ-38), `RL/tests/test_recipes_reviews.py` (the completeness test carries marker `freeze` and is not run by this build), `RL/tests/test_lint_rl.py` (seeded phrase in a recipe fails, seeded name in `lenses.json` fails, clean files pass on the synthetic ground truth; REQ-07). Register the markers `slow` and `freeze` in a `RL/tests/conftest.py` addition only if the copied `conftest.py` does not already define them; otherwise use a new `RL/pytest.ini`.

Acceptance criteria (ids added by the orchestrator, in source order):
T4.AC1: `$T $RL/tests/test_recipes.py $RL/tests/test_recipes_readme.py $RL/tests/test_recipes_reviews.py $RL/tests/test_lint_rl.py -q -m "not freeze"` exits 0.
T4.AC2: `RL/recipes/recipes.json` has exactly the key set C1 to C8, equal to the ids in `RL/cards/`, and the word counts are all at most 120.
T4.AC3: The RL block rendered with 14 in place of `{{LENS_ROW_CAP}}` equals the `MR` 3.2(a) quote byte for byte (checked later by Task 6, the placeholder is present now).
T4.AC4: `RL/recipes/REVIEWS.md` has 8 rows with status OPEN: the second-author review (REQ-08) is a manual record left open for a person who has not seen the ground truth, and is listed in Task 20.
T4.AC5: No file under `RL/recipes/` contains a package name, task number, file name of a study package or a 4-word sequence from a ground-truth file (the real lint is not run by this build).

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


Start sha: 3fcda2559111a21ecba12be20c060f1cc805f6c8
Diff against the start snapshot: diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/fixtures/gt/lint-gt.json b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/fixtures/gt/lint-gt.json
new file mode 100644
index 000000000..23f1faf8d
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/fixtures/gt/lint-gt.json
@@ -0,0 +1,20 @@
+{
+  "doc_id": "quillfern-dock-4",
+  "title": "Saltmarsh Pontoon Retrofit",
+  "items": [
+    {
+      "id": "L1",
+      "class": "C3",
+      "blocking_in_implement": true,
+      "description": "Gasket sleeves must be requalified before every dockside inspection cycle",
+      "plan_quote": "Run `tidepool/valves/flow_gate.py` once the pontoon sleeves are sealed"
+    },
+    {
+      "id": "L2",
+      "class": "C5",
+      "blocking_in_implement": false,
+      "description": "The mooring table still lists nine bollards after the retrofit",
+      "plan_quote": "Replace the bollard count in the harbour notes"
+    }
+  ]
+}
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/recipes/README.md b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/recipes/README.md
new file mode 100644
index 000000000..b5f765ef2
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/recipes/README.md
@@ -0,0 +1,39 @@
+# Recipes
+
+The sibling build's extractor sentences do not apply here: Recipe Ledger has no extractor, no pre-pass and no script that finds the places to check. Where the class cards README says to register an extractor pair or to fill a "block patterns" row, do neither. Each recipe is a written procedure that the reviewer runs, and a target type needs only the notes below.
+
+## Files
+
+- `recipes.json`: the eight recipes, one entry per card id, schema `rl-recipes/1`. The text is written once. The row budget is the closing sentence of the text ("Write at most N rows."); no other file stores it.
+- `rl-block.txt`: the ledger rule of the RL brief. `{{LENS_ROW_CAP}}` stands where the lens row cap goes.
+- `search-form.txt`: the line of generic search forms that the renderer adds to the brief of every search reviewer.
+- `REVIEWS.md`: the swap test and second-author review of each recipe.
+
+## Add a class
+
+1. Write `cards/C<n>.json` with every field of the card schema.
+2. Add `"C<n>": {"version": 1, "text": "..."}` to `recipes.json`. The text is at most 120 words, states no expected outcome and ends with one sentence "Write at most N rows." with N from 1 to 14.
+3. Place the class in at least one lens of `config/lenses.json`.
+
+No code changes. The class list, the budgets and the lens contents come from these three files.
+
+## Add a target type (REQ-38)
+
+The recipes speak of "the plan", "the driving document", "criterion", "task", "constraint" and "dictated text", so their wording needs no change. Fill one column of this table. Each cell says what to write down for that target; it is not a restatement of the row name.
+
+| Re-derive | Plan (done) | Specification (drafted) | Documentation (drafted) |
+|---|---|---|---|
+| Meaning of edits | the paths that a task orders to be edited or created | the items listed under an "Affects" or "Affected" heading | the sections that the change rewrites |
+| Meaning of tests and gate | files under `tests/`, `scripts/` and `docs/`, root-level files, and the commands of the last task | the checks that the verification rows of the specification name | the commands in the fenced blocks of the document, and the code they run |
+| Meaning of source | the document named on the plan's `Source:` line | the parent requirement document | the code the text describes, or the change log; recipe C2 does not apply until a file path names the source |
+| Command dialect | grep, git grep, pytest, test | the dialect that the verification rows use | shell commands inside fenced blocks |
+| Test and root-document paths | `tests`, `scripts`, `docs`, root-level files, change logs anywhere | the same, plus the folder of the parent document | the repository paths of the documents and of the code they describe |
+| Severity guidance | the card's `severity_guidance`: blocking when a builder cannot satisfy the text | blocking when a shall line cannot be met or checked | blocking when a reader who follows the text gets a wrong result |
+| Snapshot | the base commit of the plan | the base commit, or a recorded working tree | the commit before the fix |
+| Lens assignment | `config/lenses.json` as it stands | the same table; run the compliance spike on a specification first | the same table; recipes C2 and C8 will often answer NONE FOUND |
+
+A recipe that finds nothing to check writes one row with `NONE FOUND`; the share of such rows is reported per class.
+
+## Change a recipe
+
+A recipe is data in one file plus its card. Editing one before the freeze is a normal commit. After the freeze it is a re-freeze: a new tag and a new `config/freeze.json`, recorded in the report.
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/recipes/REVIEWS.md b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/recipes/REVIEWS.md
new file mode 100644
index 000000000..adc5ce554
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/recipes/REVIEWS.md
@@ -0,0 +1,16 @@
+# Recipe reviews (REQ-08, AO-2)
+
+One row per recipe. A person who has not seen the ground truth replaces the domain nouns of the recipe by placeholders, reads it again, and signs with the statement below. A row is complete when reviewer and date are filled and the date is before the freeze.
+
+Statement: "domain nouns replaced by placeholders, still reads correctly, no issue-specific word".
+
+| Recipe | Status | Reviewer | Date |
+|---|---|---|---|
+| C1 | OPEN | | |
+| C2 | OPEN | | |
+| C3 | OPEN | | |
+| C4 | OPEN | | |
+| C5 | OPEN | | |
+| C6 | OPEN | | |
+| C7 | OPEN | | |
+| C8 | OPEN | | |
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/recipes/recipes.json b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/recipes/recipes.json
new file mode 100644
index 000000000..a8b6d4c2d
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/recipes/recipes.json
@@ -0,0 +1,38 @@
+{
+  "schema": "rl-recipes/1",
+  "version": 1,
+  "recipes": {
+    "C1": {
+      "version": 1,
+      "text": "For each acceptance criterion or requirement that says every, all, each, complete, exhaustive, found, covers or no remaining: (1) write the finite check that would let a reviewer say yes, with its stopping rule; (2) copy the instruction sentence the criterion checks and write what set each of the two covers; (3) if you cannot write a finite check, or the two sets differ, mark PROBLEM. Write at most 4 rows."
+    },
+    "C2": {
+      "version": 1,
+      "text": "Split the driving document into rules: one per sentence that contains must, shall, never, only, halts, reports or returns, or per table row. Take up to 10 rules, preferring those that govern a failure, an exit or a special case. For each, quote the candidate sentence that carries it. For the three with the most conditions, trace each failure path through the candidate's tasks to the output the rule governs. No carrying sentence, or a path that ends in a different output, is PROBLEM. Write at most 6 rows."
+    },
+    "C3": {
+      "version": 1,
+      "text": "List every value, field or state that a task reads, maps or requires as the input to a decision (lookup tables, status mappings, conditions). For each, find the row, task or step that writes it, for every case the reader handles. A value with no writer in some case is PROBLEM. Write at most 4 rows."
+    },
+    "C4": {
+      "version": 1,
+      "text": "For each criterion that embeds a command, pattern, selector or test name: write the exact text the same task tells the implementer to write or create. Apply the literal pattern to that text, case included (you may run it on a scratch string with Bash). Then ask what the command selects or matches on the current tree. A pattern that cannot match the ordered text, or a selector that picks fewer or other checks than the criterion needs, is PROBLEM. Do not use the current file as proof; it may already contain finished work. Write at most 4 rows."
+    },
+    "C5": {
+      "version": 1,
+      "text": "For each change that alters a number, name, count, behavior or default that the repository may also state elsewhere: (1) write the old literal; (2) run one search of the whole tree for it, including root-level documents (changelogs, readmes, guides), mirrored copies and comments, not only the files the plan names; (3) list every hit the plan neither edits nor checks. A hit that would be false after the change is PROBLEM. Grade it with the grading check; never drop it. Write at most 4 rows."
+    },
+    "C6": {
+      "version": 1,
+      "text": "For each sentence the plan states or dictates that says all, only, never, every, no other, or outside X nothing: (1) name the set it covers; (2) run one count or listing command for that set over the tree; (3) compare with the plan's other tasks and with the scope of the test or check said to enforce it (what does that test skip or not read?). A member outside the claim, a task that does the opposite, or a test scope narrower than the claim is PROBLEM. Write at most 4 rows."
+    },
+    "C7": {
+      "version": 1,
+      "text": "List every constraint, one clause per line (split at semicolons and 'and'). List every piece of text the plan dictates word for word. For each text and each constraint on its topic, tick each clause. A text that omits or contradicts a clause is PROBLEM. Write at most 4 rows."
+    },
+    "C8": {
+      "version": 1,
+      "text": "For each file the plan edits or creates, search the tests, scripts and docs for its path and distinctive strings: `git grep -l -F '<string>' -- tests scripts docs`. For each referencing file the plan never names, open it and decide whether it pins the text or behavior being changed. If it does and no task updates or runs it, mark PROBLEM. Write at most 4 rows."
+    }
+  }
+}
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/recipes/rl-block.txt b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/recipes/rl-block.txt
new file mode 100644
index 000000000..bb73178dc
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/recipes/rl-block.txt
@@ -0,0 +1 @@
+RECIPES AND LEDGER. Before you review freely, run the recipes below that are assigned to you, in order. For each recipe step, write one row in the `ledger-v1` block. The row id is the recipe id and a row number, for example `C4.1`, then `C4.2`. Set `item` to the row id, `verdict` to OK, PROBLEM or UNSURE, and copy each quote exactly. In `ran`, say in at most 15 words what you ran or read. If a recipe finds nothing to check in this document, write one row for it with verdict OK, an empty `quote_plan`, and the words NONE FOUND and what you searched in `ran`. Each recipe has a row limit, and you never write more than {{LENS_ROW_CAP}} rows. A recipe row is a question about the text, not a finding. When you write a findings line for a PROBLEM or UNSURE row, set the findings key `probe` to the row id. Keep at least half of your time for your own review of the plan. The recipes do not replace it. Put the ledger under the heading `## Ledger`, directly above the findings block, in your final message.
\ No newline at end of file
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/recipes/search-form.txt b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/recipes/search-form.txt
new file mode 100644
index 000000000..889e94d90
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/recipes/search-form.txt
@@ -0,0 +1 @@
+Search forms you may adapt: `grep -rlF '<path>' <test dirs>`; `grep -rlF '<name without extension>' .`; `grep -rnF '<old value>' . --include='*.md'` (include root files); `printf '%s' '<ordered text>' | grep -c '<pattern>'`.
\ No newline at end of file
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/rl/extract_mr.py b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/rl/extract_mr.py
new file mode 100644
index 000000000..81f429790
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/rl/extract_mr.py
@@ -0,0 +1,83 @@
+"""One-time helper: cut the quoted recipe wording out of MR 3.2(a) and diff it against recipes/.
+
+`quotes(mr_text)` returns {"C1".."C8": text, "rl_block": text with {{LENS_ROW_CAP}}, "search_form": text}.
+Run it as `uv run --frozen --project REPO python RL/rl/extract_mr.py [MR]`: it prints a unified diff of
+recipes/recipes.json, rl-block.txt and search-form.txt against the quotes and exits 1 when any differs.
+It reads MR only, never a ground-truth file.
+"""
+
+from __future__ import annotations
+
+import difflib
+import json
+import re
+import sys
+from pathlib import Path
+
+RL = Path(__file__).resolve().parents[1]
+REPO = RL.parents[3]
+MR = (
+    REPO
+    / ".dev/brainstorms/20261113-223124-panel-process-redesign/merged-requirements.md"
+)
+CAP_PLACEHOLDER = "{{LENS_ROW_CAP}}"
+_RECIPE = re.compile(r'^> \*\*R-(C[1-8])\.\*\* "(.*)"$')
+_BLOCK = re.compile(r'^> "((?:RECIPES AND LEDGER\.|Search forms you may adapt:).*)"$')
+
+
+def quotes(mr_text: str) -> dict[str, str]:
+    """The ten quoted blocks of 3.2(a): eight recipes, the RL block (cap placeholder) and the search-form line."""
+    out: dict[str, str] = {}
+    for line in mr_text.splitlines():
+        m = _RECIPE.match(line)
+        if m:
+            out[m.group(1)] = m.group(2)
+            continue
+        m = _BLOCK.match(line)
+        if m:
+            key = "rl_block" if m.group(1).startswith("RECIPES") else "search_form"
+            out[key] = m.group(1)
+    block = out["rl_block"]
+    assert block.count("more than 14 rows") == 1
+    out["rl_block"] = block.replace(
+        "more than 14 rows", f"more than {CAP_PLACEHOLDER} rows"
+    )
+    return out
+
+
+def stored(rl: Path = RL) -> dict[str, str]:
+    """The same ten texts as they are stored under rl/recipes/."""
+    data = json.loads((rl / "recipes" / "recipes.json").read_text(encoding="utf-8"))
+    out = {k: v["text"] for k, v in data["recipes"].items()}
+    out["rl_block"] = (rl / "recipes" / "rl-block.txt").read_text(encoding="utf-8")
+    out["search_form"] = (rl / "recipes" / "search-form.txt").read_text(
+        encoding="utf-8"
+    )
+    return out
+
+
+def diff(mr_text: str, rl: Path = RL) -> list[str]:
+    """Unified diff lines of the stored texts against the quotes (empty when they are byte for byte equal)."""
+    want, have = quotes(mr_text), stored(rl)
+    lines: list[str] = []
+    for key in sorted(set(want) | set(have)):
+        a, b = want.get(key, ""), have.get(key, "")
+        if a != b:
+            lines.extend(
+                difflib.unified_diff(
+                    [a], [b], f"MR {key}", f"recipes {key}", lineterm=""
+                )
+            )
+    return lines
+
+
+def main(argv=None) -> int:
+    args = list(sys.argv[1:] if argv is None else argv)
+    mr = Path(args[0]) if args else MR
+    lines = diff(mr.read_text(encoding="utf-8"))
+    print("\n".join(lines) if lines else "recipes equal the MR 3.2(a) quotes")
+    return 1 if lines else 0
+
+
+if __name__ == "__main__":
+    sys.exit(main())
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/rl/recipes.py b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/rl/recipes.py
new file mode 100644
index 000000000..91fec4a71
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/rl/recipes.py
@@ -0,0 +1,78 @@
+"""Recipes as data (DESIGN 4.1, REQ-25, DR-1): recipes/recipes.json is the only file that holds recipe text.
+
+The row budget is never stored: `row_budget` reads N out of the last sentence of the text, "Write at most N rows.".
+`validate` returns the list of rule breaks (empty when the file is sound); `load` raises ValueError on any.
+"""
+
+from __future__ import annotations
+
+import json
+import re
+from pathlib import Path
+
+from scaffold import cards
+
+RECIPES_DIR = Path(__file__).resolve().parents[1] / "recipes"
+RECIPES_JSON = RECIPES_DIR / "recipes.json"
+SCHEMA = "rl-recipes/1"
+MAX_WORDS = 120
+BUDGET_MIN, BUDGET_MAX = 1, 14
+_BUDGET = re.compile(r"Write at most (\d+) rows\.")
+FORBIDDEN_PHRASES = ("expected", "should find", "will find", "you will see")
+FORBIDDEN_PATH = "src/superclaude/"
+
+
+def budget_of(text: str) -> int | None:
+    """N of the single closing sentence "Write at most N rows.", or None when it is missing, repeated or not last."""
+    found = _BUDGET.findall(text)
+    if len(found) != 1 or not text.rstrip().endswith(f"Write at most {found[0]} rows."):
+        return None
+    return int(found[0])
+
+
+def validate(data: dict, card_ids=None) -> list[str]:
+    """Every rule of DESIGN 4.1 that `data` (a parsed recipes.json) breaks; card_ids defaults to the ids in cards/."""
+    ids = set(cards.load() if card_ids is None else card_ids)
+    errors: list[str] = []
+    if data.get("schema") != SCHEMA:
+        errors.append(f"schema is not {SCHEMA}")
+    recipes = data.get("recipes", {})
+    if set(recipes) != ids:
+        errors.append(
+            f"recipe ids {sorted(recipes)} differ from card ids {sorted(ids)}"
+        )
+    for rid, entry in sorted(recipes.items()):
+        text = entry.get("text", "") if isinstance(entry, dict) else ""
+        low = text.lower()
+        if not text:
+            errors.append(f"{rid}: no text")
+            continue
+        if len(text.split()) > MAX_WORDS:
+            errors.append(f"{rid}: more than {MAX_WORDS} words")
+        n = budget_of(text)
+        if n is None:
+            errors.append(f"{rid}: no single closing sentence 'Write at most N rows.'")
+        elif not BUDGET_MIN <= n <= BUDGET_MAX:
+            errors.append(f"{rid}: budget {n} outside {BUDGET_MIN} to {BUDGET_MAX}")
+        if FORBIDDEN_PATH in text:
+            errors.append(f"{rid}: holds a {FORBIDDEN_PATH} path")
+        errors.extend(
+            f"{rid}: states an expected outcome ({p!r})"
+            for p in FORBIDDEN_PHRASES
+            if p in low
+        )
+    return errors
+
+
+def load(path: Path | str | None = None, card_ids=None) -> dict[str, dict]:
+    """{recipe id: {"version", "text"}} from recipes.json; ValueError when validate finds anything."""
+    data = json.loads(Path(path or RECIPES_JSON).read_text(encoding="utf-8"))
+    errors = validate(data, card_ids)
+    if errors:
+        raise ValueError("; ".join(errors))
+    return data["recipes"]
+
+
+def row_budget(recipe_id: str, recipes: dict[str, dict] | None = None) -> int:
+    """The row budget N of one recipe, parsed from its text."""
+    return budget_of((recipes or load())[recipe_id]["text"])
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/tests/test_lint_rl.py b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/tests/test_lint_rl.py
new file mode 100644
index 000000000..444c3d7aa
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/tests/test_lint_rl.py
@@ -0,0 +1,69 @@
+"""REQ-07: the copied AO-1 lint (scaffold/lint.py) over the RL files, against the invented F-LINT-GT ground truth."""
+
+import json
+import os
+import shutil
+
+import pytest
+from helpers import SW
+
+from scaffold import lint
+
+GT = SW / "fixtures" / "gt" / "lint-gt.json"
+PHRASE = (
+    "requalified before every dockside"  # four words of the invented L1 description
+)
+NAME = "quillfern-dock-4"  # the invented doc_id
+FOLDERS = ("recipes", "config", "briefs", "cards", "fixtures")
+
+
+def run(*paths):
+    return lint.main(["--gt-glob", str(GT), *map(str, paths)])
+
+
+def test_seeded_phrase_in_recipe_fails(tmp_path, capsys):
+    folder = tmp_path / "recipes"
+    shutil.copytree(SW / "recipes", folder)
+    assert run(folder) == 0
+    path = folder / "recipes.json"
+    data = json.loads(path.read_text(encoding="utf-8"))
+    entry = data["recipes"]["C3"]
+    entry["text"] = entry["text"].replace(" Write at most", f" {PHRASE}. Write at most")
+    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
+    capsys.readouterr()
+    assert run(folder) == 1
+    out = capsys.readouterr().out
+    assert "recipes.json" in out and "phrase" in out and "dockside" not in out
+
+
+def test_seeded_name_in_lenses_fails(tmp_path, capsys):
+    real = SW / "config" / "lenses.json"
+    lenses = tmp_path / "config" / "lenses.json"
+    lenses.parent.mkdir()
+    if real.is_file():
+        shutil.copy(real, lenses)
+    else:  # config/lenses.json is written by a later task; the lint only reads text
+        lenses.write_text('{"panels": {}}\n', encoding="utf-8")
+    assert run(lenses.parent) == 0
+    data = json.loads(lenses.read_text(encoding="utf-8"))
+    data["note"] = f"see {NAME} for the lens"
+    lenses.write_text(json.dumps(data), encoding="utf-8")
+    capsys.readouterr()
+    assert run(lenses.parent) == 1
+    out = capsys.readouterr().out
+    assert "lenses.json" in out and "name" in out and "quillfern" not in out
+
+
+def test_rl_files_clean_on_synthetic_gt(capsys):
+    folders = [SW / f for f in FOLDERS if (SW / f).is_dir()]
+    assert SW / "recipes" in folders and SW / "cards" in folders
+    assert run(*folders) == 0, capsys.readouterr().out
+
+
+@pytest.mark.freeze
+def test_real_recipes_against_real_gt():
+    """Written, not run by the build. A maintainer gives the real ground-truth glob in LINT_REAL_GT_GLOB (never hard-coded)."""
+    pattern = os.environ.get("LINT_REAL_GT_GLOB")
+    assert pattern, "LINT_REAL_GT_GLOB is not set: a maintainer must pass the real glob"
+    folders = [str(SW / f) for f in FOLDERS if (SW / f).is_dir()]
+    assert lint.main(["--gt-glob", pattern, *folders]) == 0
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/tests/test_recipes.py b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/tests/test_recipes.py
new file mode 100644
index 000000000..62955fc68
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/tests/test_recipes.py
@@ -0,0 +1,128 @@
+"""REQ-06, REQ-09, REQ-25, DR-1: the eight recipes in recipes/recipes.json (DESIGN 4.1, 4.2)."""
+
+import json
+
+import pytest
+from helpers import SW
+
+from rl import extract_mr, recipes
+from scaffold import cards
+
+RECIPES_DIR = SW / "recipes"
+DATA = json.loads((RECIPES_DIR / "recipes.json").read_text(encoding="utf-8"))
+WORDS = {"C1": 71, "C2": 89, "C3": 56, "C4": 99, "C5": 86, "C6": 93, "C7": 50, "C8": 67}
+BUDGETS = {"C2": 6, "C1": 4, "C3": 4, "C4": 4, "C5": 4, "C6": 4, "C7": 4, "C8": 4}
+# the design documents and the session logs of the planning and build runs quote the wording on purpose
+QUOTING = {"DESIGN.md", "TESTING.md", "IMPLEMENTATION.md", "recipes/recipes.json"}
+QUOTING_DIRS = {"design-report", "workflow-report", "implement-report"}
+
+
+def test_file_shape():
+    assert DATA["schema"] == "rl-recipes/1" and DATA["version"] == 1
+    assert all(set(r) == {"version", "text"} for r in DATA["recipes"].values())
+
+
+def test_recipe_keys_equal_card_ids():
+    assert set(DATA["recipes"]) == set(cards.load()) == set(WORDS)
+    assert recipes.validate(DATA) == []
+    assert set(recipes.load()) == set(WORDS)
+
+
+def test_each_recipe_at_most_120_words():
+    counts = {k: len(v["text"].split()) for k, v in DATA["recipes"].items()}
+    assert counts == WORDS
+    assert all(n <= 120 for n in counts.values())
+
+
+def test_budget_sentence_once_and_parsed():
+    for rid, entry in DATA["recipes"].items():
+        text = entry["text"]
+        assert text.count("Write at most") == 1
+        assert text.endswith(f"Write at most {BUDGETS[rid]} rows.")
+        n = recipes.row_budget(rid)
+        assert n == BUDGETS[rid] and 1 <= n <= 14
+
+
+@pytest.mark.parametrize(
+    "text",
+    [
+        "Do it.",
+        "Do it. Write at most 4 rows. Write at most 4 rows.",
+        "Write at most 4 rows. Then stop.",
+        "Do it. Write at most 0 rows.",
+        "Do it. Write at most 15 rows.",
+        "Do it. Write at most 4 rows.".replace("Do it.", " ".join(["w"] * 120)),
+        "You will see it. Write at most 4 rows.",
+        "It should find it. Write at most 4 rows.",
+        "The expected result. Write at most 4 rows.",
+        "Read src/superclaude/x. Write at most 4 rows.",
+    ],
+)
+def test_validate_refuses_a_broken_recipe(text):
+    data = {"schema": "rl-recipes/1", "recipes": {"C1": {"version": 1, "text": text}}}
+    assert recipes.validate(data, ["C1"]) != []
+
+
+def test_validate_refuses_key_set_mismatch():
+    ok = {"version": 1, "text": "Do it. Write at most 4 rows."}
+    assert (
+        recipes.validate({"schema": "rl-recipes/1", "recipes": {"C1": ok}}, ["C1"])
+        == []
+    )
+    assert recipes.validate(
+        {"schema": "rl-recipes/1", "recipes": {"C1": ok}}, ["C1", "C2"]
+    )
+    assert recipes.validate(
+        {"schema": "rl-recipes/1", "recipes": {"C1": ok, "C9": ok}}, ["C1"]
+    )
+    assert recipes.validate({"schema": "other", "recipes": {"C1": ok}}, ["C1"])
+
+
+def test_recipes_equal_mr_quotes():
+    if "override" in DATA:
+        pytest.skip(
+            "an override entry is recorded: a wording change after the freeze (DESIGN 4.1)"
+        )
+    quotes = extract_mr.quotes(extract_mr.MR.read_text(encoding="utf-8"))
+    assert {k: v["text"] for k, v in DATA["recipes"].items()} == {
+        k: quotes[k] for k in WORDS
+    }
+    block = (RECIPES_DIR / "rl-block.txt").read_text(encoding="utf-8")
+    assert block.count("{{LENS_ROW_CAP}}") == 1 and block == quotes["rl_block"]
+    assert block.replace("{{LENS_ROW_CAP}}", "14").count("14 rows") == 1
+    assert (RECIPES_DIR / "search-form.txt").read_text(encoding="utf-8") == quotes[
+        "search_form"
+    ]
+    assert extract_mr.diff(extract_mr.MR.read_text(encoding="utf-8")) == []
+
+
+def test_no_src_path_in_recipe_files():
+    files = [p for p in RECIPES_DIR.rglob("*") if p.is_file()]
+    assert {p.name for p in files} >= {
+        "recipes.json",
+        "rl-block.txt",
+        "search-form.txt",
+    }
+    assert not [
+        p.name for p in files if "src/superclaude/" in p.read_text(encoding="utf-8")
+    ]
+
+
+def test_recipe_text_only_in_one_file():
+    heads = {
+        rid: " ".join(e["text"].split()[:10]) for rid, e in DATA["recipes"].items()
+    }
+    assert all(len(h.split()) == 10 for h in heads.values())
+    holders = []
+    for p in sorted(SW.rglob("*")):
+        rel = p.relative_to(SW)
+        if (
+            not p.is_file()
+            or "__pycache__" in p.parts
+            or rel.parts[0] in QUOTING_DIRS
+            or rel.as_posix() in QUOTING
+        ):
+            continue
+        text = p.read_text(encoding="utf-8", errors="ignore")
+        holders.extend((str(rel), rid) for rid, h in heads.items() if h in text)
+    assert holders == []
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/tests/test_recipes_readme.py b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/tests/test_recipes_readme.py
new file mode 100644
index 000000000..9400cfa16
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/tests/test_recipes_readme.py
@@ -0,0 +1,45 @@
+"""REQ-38: recipes/README.md lists, per target type, what a maintainer must re-derive (DESIGN 11.3)."""
+
+from helpers import SW
+
+README = SW / "recipes" / "README.md"
+ROWS = (
+    "meaning of edits",
+    "meaning of tests and gate",
+    "meaning of source",
+    "command dialect",
+    "test and root-document paths",
+    "severity guidance",
+    "snapshot",
+    "lens assignment",
+)
+TARGETS = ("plan", "specification", "documentation")
+
+
+def table():
+    """{row name (lower-case): [cell per target type]} for the re-derive table; its header names the target types."""
+    lines = [
+        ln
+        for ln in README.read_text(encoding="utf-8").splitlines()
+        if ln.startswith("|")
+    ]
+    rows = [[c.strip() for c in ln.strip().strip("|").split("|")] for ln in lines]
+    header = next(r for r in rows if r[0].lower() == "re-derive")
+    assert [h.lower().split(" (")[0] for h in header[1:]] == list(TARGETS)
+    return {r[0].lower(): r[1:] for r in rows if r is not header and len(r) == 4}
+
+
+def test_readme_lists_rederive_rows():
+    t = table()
+    for row in ROWS:
+        matches = [k for k in t if k.startswith(row)]
+        assert len(matches) == 1, row
+        cells = t[matches[0]]
+        assert len(cells) == len(TARGETS)
+        for target, cell in zip(TARGETS, cells):
+            assert len(cell) >= 20, (row, target)
+
+
+def test_readme_says_the_extractor_sentences_do_not_apply():
+    first = " ".join(README.read_text(encoding="utf-8").splitlines()[:4])
+    assert "extractor sentences do not apply" in first
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/tests/test_recipes_reviews.py b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/tests/test_recipes_reviews.py
new file mode 100644
index 000000000..4880ac3d7
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/tests/test_recipes_reviews.py
@@ -0,0 +1,33 @@
+"""REQ-08: recipes/REVIEWS.md holds one row per recipe; the completeness test needs a person and is not run by the build."""
+
+import pytest
+from helpers import SW
+
+REVIEWS = SW / "recipes" / "REVIEWS.md"
+
+
+def rows():
+    """[(recipe, status, reviewer, date)] of the table rows of REVIEWS.md."""
+    cells = [
+        [c.strip() for c in ln.strip().strip("|").split("|")]
+        for ln in REVIEWS.read_text(encoding="utf-8").splitlines()
+        if ln.startswith("| C")
+    ]
+    assert all(len(c) == 4 for c in cells)
+    return [tuple(c) for c in cells]
+
+
+def test_review_record_has_one_row_per_recipe():
+    got = rows()
+    assert [r[0] for r in got] == [f"C{n}" for n in range(1, 9)]
+    assert {r[1] for r in got} <= {"OPEN", "DONE"}
+
+
+@pytest.mark.freeze
+def test_review_record_complete():
+    """Written, not run by the build: 8 rows, none with an empty reviewer or date."""
+    got = rows()
+    assert len(got) == 8
+    assert all(
+        status == "DONE" and reviewer and date for _, status, reviewer, date in got
+    )

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
