# Class cards

One JSON file per defect class (`C1.json` to `C8.json`), checked against `schema.json` by `scaffold/cards.py`. A card is data: the printed question, the route, the replica count, the extractor name, the promotion category and the target-neutral definition all come from it. Nothing else in the build keeps a class list (MR 3.0.3, DESIGN 13.2).

Fields: `id`, `name`, `version`, `definition`, `question_template`, `extractor`, `route` (`search` or `read`), `replicas`, `applies_to` (`plan`, `spec`, `doc`), `instances` (at least two citations, paths relative to `.dev/`, from the register of recorded cases outside the study packages), `severity_guidance`, `known_weakness` (for maintainers, never shown to a reviewer), `promote_category` (one of `FND.CATEGORIES`, DD-11) and `swap_test` (reviewer and date, filled by a second author).

## Add a class

1. Write `cards/C<n>.json` with every field above. The file name must equal its `id`.
2. Run `uv run --frozen --project <repo> pytest -p no:cacheprovider <SW>/tests/test_cards.py`.
3. Only if a deterministic trigger exists: register one extractor pair in `sweep/extractors.py` and name it in the card's `extractor`. With no extractor the class still enters the arm K paragraph.

No change to `select.py`, `assign.py`, `render.py`, `scaffold/ledgerv1.py` or the launcher (REQ-10).

## Add a target type (REQ-38)

Add one dictionary to `sweep/formats.py` and fill one column of this table. Each cell says what to write down for that target; it is not a restatement of the row name.

| Re-derive | Plan (done) | Specification (drafted) | Documentation (drafted) |
|---|---|---|---|
| Block patterns | `formats.py: plan`: `## Task N:` sections, `Acceptance criteria:` bullets, `## Constraints` bullets, quoted spans after a dictation verb, path tokens after an edit verb, the last task's criteria as the gate | `formats.py: spec`: numbered sections, lines with shall, must or should, fenced blocks under Example or Message format, items under Affects, a Verification section | `formats.py: doc`: headings, sentences with a set word, fenced command blocks and fenced text blocks of a how-to; no constraint or edit-target blocks |
| Command dialect | grep, egrep, rg, git grep, pytest, test | the dialect the specification's verification rows name | shell commands inside fenced blocks |
| Test and root-document paths | `tests/`, `scripts/`, `docs/`, root-level files, change-log style files anywhere, the folders of plan-named paths (DD-5) | the same, plus the parent folder of the specification | the repository paths of the documents and of the code they describe |
| Severity guidance | each card's `severity_guidance`, where blocking means a builder cannot satisfy the text | each card's `severity_guidance`, where blocking means a shall line cannot be met or checked | each card's `severity_guidance`, where blocking means a reader who follows the text gets a wrong result |
| Location of truth | the source document named on the `Source:` line | the parent requirement document | the code the text describes, or the change log |
| Snapshot | the base commit of the plan | the base commit, or a recorded working tree | the commit before the fix |

## Open manual checks

- Second reader of this table (TESTING REQ-38, row M): reader: ______  date: ______  statement: "each row is specific, not a restatement of the heading". Status: OPEN.
- Swap test (AO-2, REQ-08): the `swap_test` record of C1 to C8 was signed on 2026-11-15 by a second-author session (claude-sonnet-5-5, a fresh session that had not seen the ground truth or the extractors), which judged each card's definition and question with the domain nouns replaced by placeholders; all eight passed. No card was left unsigned; the per-card reasons are in `fixtures/recall/SWAP-NOTES.md`. Status: SIGNED for C1 to C8 by a session, not a person.
