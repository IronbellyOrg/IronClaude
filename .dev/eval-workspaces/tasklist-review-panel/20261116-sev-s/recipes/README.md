# Recipes

The sibling build's extractor sentences do not apply here: Recipe Ledger has no extractor, no pre-pass and no script that finds the places to check. Where the class cards README says to register an extractor pair or to fill a "block patterns" row, do neither. Each recipe is a written procedure that the reviewer runs, and a target type needs only the notes below.

## Files

- `recipes.json`: the eight recipes, one entry per card id, schema `rl-recipes/1`. The text is written once. The row budget is the closing sentence of the text ("Write at most N rows."); no other file stores it.
- `rl-block.txt`: the ledger rule of the RL brief. `{{LENS_ROW_CAP}}` stands where the lens row cap goes.
- `search-form.txt`: the line of generic search forms that the renderer adds to the brief of every search reviewer.
- `REVIEWS.md`: the swap test and second-author review of each recipe.

## Add a class

1. Write `cards/C<n>.json` with every field of the card schema.
2. Add `"C<n>": {"version": 1, "text": "..."}` to `recipes.json`. The text is at most 120 words, states no expected outcome and ends with one sentence "Write at most N rows." with N from 1 to 14.
3. Place the class in at least one lens of `config/lenses.json`.

No code changes. The class list, the budgets and the lens contents come from these three files.

## Add a target type (REQ-38)

The recipes speak of "the plan", "the driving document", "criterion", "task", "constraint" and "dictated text", so their wording needs no change. Fill one column of this table. Each cell says what to write down for that target; it is not a restatement of the row name.

| Re-derive | Plan (done) | Specification (drafted) | Documentation (drafted) |
|---|---|---|---|
| Meaning of edits | the paths that a task orders to be edited or created | the items listed under an "Affects" or "Affected" heading | the sections that the change rewrites |
| Meaning of tests and gate | files under `tests/`, `scripts/` and `docs/`, root-level files, and the commands of the last task | the checks that the verification rows of the specification name | the commands in the fenced blocks of the document, and the code they run |
| Meaning of source | the document named on the plan's `Source:` line | the parent requirement document | the code the text describes, or the change log; recipe C2 does not apply until a file path names the source |
| Command dialect | grep, git grep, pytest, test | the dialect that the verification rows use | shell commands inside fenced blocks |
| Test and root-document paths | `tests`, `scripts`, `docs`, root-level files, change logs anywhere | the same, plus the folder of the parent document | the repository paths of the documents and of the code they describe |
| Severity guidance | the card's `severity_guidance`: blocking when a builder cannot satisfy the text | blocking when a shall line cannot be met or checked | blocking when a reader who follows the text gets a wrong result |
| Snapshot | the base commit of the plan | the base commit, or a recorded working tree | the commit before the fix |
| Lens assignment | `config/lenses.json` as it stands | the same table; run the compliance spike on a specification first | the same table; recipes C2 and C8 will often answer NONE FOUND |

A recipe that finds nothing to check writes one row with `NONE FOUND`; the share of such rows is reported per class.

## Change a recipe

A recipe is data in one file plus its card. Editing one before the freeze is a normal commit. After the freeze it is a re-freeze: a new tag and a new `config/freeze.json`, recorded in the report.
