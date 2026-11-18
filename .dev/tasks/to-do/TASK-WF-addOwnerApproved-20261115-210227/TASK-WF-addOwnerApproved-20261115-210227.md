---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-addOwnerApproved-20261115-210227
version: "1"
priority: Medium
created_date: "2026-11-15"
---

# Owner-approved format forgiveness in the Sweep Sheet ledger parser, reported strict and lenient per arm

Source: ./source.md
Goal: The ledger parser forgives the seven owner-approved small deviations when the content is correct, records every forgiveness with the raw text and a rule name, never forgives the listed hard failures, and the analysis reports the compliance gate and the primary metric both strict and lenient per arm with counts of forgiven items.

## Constraints

- SW means `.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet`. Every path that starts with `SW/` is repo-relative. Run commands from the repository root with `uv run --frozen pytest -p no:cacheprovider -q <path>` (the `REPO`, `SW` and `T` variables of `SW/TESTING.md` section 1.2 give the same form). Python only through `uv`.
- Files that may change: `SW/scaffold/ledgerv1.py`, `SW/analysis/analyze.py`, tests under `SW/tests/` (new files, and edits to existing tests only where an existing assertion pins behaviour the owner order changes), new report fixtures under `SW/fixtures/reports/`, and additions to `SW/DESIGN.md` and `SW/TESTING.md`. One narrow exception to "additions only" (review finding B1, resolved 2026-11-15 by the plan owner): Task 8 may rewrite item 4 and the heading-regex sentence of item 1 of `SW/DESIGN.md` section 9.1, because they state the old strict acceptance that the owner order changes; no other existing line of either file is edited.
- Files that must not change: everything under `SW/cards/` and `SW/briefs/`, and `SW/sweep/extractors.py`, `SW/sweep/words.py`, `SW/sweep/formats.py`, `SW/sweep/rank.py` (frozen). Also unchanged: `src/superclaude/cli/review/findings.py` (the production merge parses every arm's findings block strictly and is not edited), `SW/sweep/cli.py`, `SW/bin/`, repo-root `src/`, repo-root `tests/`, `.claude/`, and every existing `.dev/tasks` package. Forgiveness lives only in the ledger parser.
- No model is started: tests use the fake `claude` of `SW/tests/fakes/claude`. No file named `ground-truth*.json` is opened or read. Every new fixture is invented text.
- The implementation runs no `git add`, commit or push for any SW file.
- Approved forgiveness list, named by rule: `verdict_case` (verdict word in lower or mixed case), `json_line_tidy` (trailing comma or extra whitespace on a JSON line), `fence_case` (capitalised code-fence language), `item_decoration` (item id wrapped in backticks or followed by a colon), `heading_variant` (ledger heading written as `### Ledger` or `Ledger:`), `loose_layout` (a heading between the ledger block and the findings block: flagged, not missing), `quote_whitespace` (quote matching across line wraps and doubled spaces).
- Never forgiven, in both modes: a missing ledger, an unknown item (also when the decorated id does not resolve to an assigned item), a verdict that is not OK, PROBLEM or UNSURE after case folding, a quote not found in the plan, rows over budget (`limits_violated` stays and the row cannot be promoted), a missing CB-3 sentence on a blocking finding. `carries_cb3` and the limits in `read_ledger` are not loosened.
- Two modes. Lenient (default) applies the seven rules. Strict applies none: it reads the exact ledger-v1 shape of `SW/DESIGN.md` section 8.2 (verdict exactly OK, PROBLEM or UNSURE; the JSON line has no surrounding whitespace or trailing comma; item exactly an assigned id; fence info string exactly `ledger-v1`; heading exactly `## Ledger`; no heading between the ledger block and the findings heading; quotes found verbatim without whitespace flattening). Some of these were already silently accepted by the old reader (verdict case and trim, any heading level, any heading case, whitespace flattening); in this work each becomes a named, counted rule that strict turns off. The mode comes from the `forgiveness` argument, else the environment variable `LEDGER_FORGIVENESS` (`strict` or `lenient`), else lenient, mirroring `scope_from` and `CHECK_SCOPE`.
- Record shape for one forgiveness: `{"rule": <rule name>, "line": <1-based report line>, "item": <item id or null>, "raw": <the text as written>}`.
- Primary metric means `found_fraction` (the per-run found fraction that gate D2 and the claim sentence of `SW/analysis/analyze.py` use). Compliance gate means the `ledger_missing` rate limit `COMPLIANCE_LIMIT` (0.10) of `compliance()`.

## Phase 1: Reader forgives the approved deviations

## Task 1: Add the forgiveness mode and the line-level rules to read_ledger

Edit `SW/scaffold/ledgerv1.py`. Add the constant `FORGIVENESS_RULES` (the seven rule names above, in that order), `FORGIVENESS_MODES = ("lenient", "strict")` and `forgiveness_from(mode=None)` (argument, else `LEDGER_FORGIVENESS`, else `lenient`; any other value raises `ValueError`, as `scope_from` does). Give `read_ledger(report, assigned, *, lenient=True)` a `lenient` flag and add the keys `forgiven` (list of the record shape in Constraints), `loose_layout` (False for now) and `mode` to its result. Implement three rules inside the per-line loop of `read_ledger`:

- `verdict_case`: in lenient mode a verdict that differs from its upper-cased, trimmed form is accepted, recorded, and counted in the existing `normalised_verdict`. In strict mode it is the format error "verdict must be OK, PROBLEM or UNSURE" and `normalised_verdict` stays 0. A verdict outside the three after case folding is a format error in both modes.
- `json_line_tidy`: in lenient mode strip surrounding whitespace and one trailing comma after the closing brace before `json.loads`, and record the raw line when anything was removed. In strict mode a line whose text differs from its stripped form, or that ends in a comma, is a format error. A line that is still not valid JSON after tidying (for example the missing closing brace of `SW/fixtures/reports/bad_json_line.md`) stays a format error in both modes.
- `item_decoration`: in lenient mode strip surrounding backticks and one trailing colon from the item id; the rule applies, and is recorded, only when the stripped id is an assigned item. A stripped id that is not assigned stays an `unknown_item` entry carrying the id as written. In strict mode a decorated id is an `unknown_item`.

Update the module docstring with the new gap entries (one short entry per rule, in the existing "Gaps resolved here" style) and update the `read_ledger` docstring for the new keys. Add fixtures `SW/fixtures/reports/forgive_json_line.md` (an S1 line with a trailing comma and an S2 line padded with spaces) and `SW/fixtures/reports/forgive_item_decor.md` (items written as a backticked id, an id followed by a colon, and a backticked id followed by a colon), each derived from the layout of `SW/fixtures/reports/good.md`. Create `SW/tests/test_ledger_forgiveness.py` (same loader pattern as `SW/tests/test_ledgerv1.py`) with tests for these three rules in both modes, using the existing `SW/fixtures/reports/verdict_lowercase.md` for `verdict_case`.

Before the first edit, record a baseline for the frozen and untouchable files: write `sha256sum` of every file under `SW/cards/`, `SW/briefs/`, `SW/sweep/` and `SW/bin/`, plus `src/superclaude/cli/review/findings.py`, to `./artifacts/frozen-before.sha256` (package-relative; read-only commands only). Task 8 compares against it.

Dependents that must keep working: `check_report` in the same file (calls `read_ledger` with the default), `SW/tests/test_ledgerv1.py::test_misplaced_duplicated_truncated_blocks` and `::test_reader_counts_format_errors_dup_unknown_and_verdicts` (both call it with the default and must pass unchanged).

Acceptance criteria:
- `read_ledger(load("verdict_lowercase"), ASSIGNED)` returns the same rows, `normalised_verdict == 3` and no format errors as today, plus three `verdict_case` records whose `raw` is the line as written; with `lenient=False` it returns three format errors, no rows and `normalised_verdict == 0`.
- The `forgive_json_line` and `forgive_item_decor` fixtures give all rows in lenient mode with one `json_line_tidy` or `item_decoration` record per touched line (raw kept), and format errors or `unknown_item` entries in strict mode.
- An item such as `` `S9` `` (not assigned) is `unknown_item` in both modes and produces no `item_decoration` record; a verdict `maybe` is a format error in both modes.
- `forgiveness_from("bogus")` raises `ValueError`; with `LEDGER_FORGIVENESS=strict` set through `monkeypatch`, `forgiveness_from()` returns `strict`.
- `uv run --frozen pytest -p no:cacheprovider -q SW/tests/test_ledger_forgiveness.py SW/tests/test_ledgerv1.py` passes.

## Task 2: Forgive fence case, heading variants and loose layout in read_ledger

Depends on: Task 1

Edit `SW/scaffold/ledgerv1.py` (`read_ledger`, `_fenced`, `_heading_between`, `HEAD_LEDGER`). Keep the `HEAD_LEDGER` name and value for any importer (Grep finds its only use inside the file) and add the exact heading pattern `^##[ \t]+Ledger[ \t]*$` (case-sensitive) plus a lenient-only pattern for a bare `Ledger:` line (case-insensitive, nothing else on the line). Implement:

- `heading_variant`: in lenient mode the ledger heading may be any `#` level, any case, or the line `Ledger:`; when the heading used is not exactly `## Ledger`, record the heading line as written. In strict mode only the exact heading counts, so any other form gives the reason `ledger_heading_missing` (or `ledger_after_findings` when an exact heading lies only below the findings heading, as today).
- `fence_case`: in lenient mode collect every fence in the report whose info string equals `ledger-v1` ignoring case, by calling `_fenced` once per distinct spelling found with `_FENCE_LINE`; record each fence line whose spelling is not exactly `ledger-v1`. `two_blocks` counts all spellings together in lenient mode. In strict mode only the exact spelling is a ledger block (a report with only `Ledger-V1` gives `no_block`).
- `loose_layout`: change `_heading_between` so it returns the 1-based line number of the first heading outside a code fence (or None). In lenient mode, when the single ledger block is closed, lies after the ledger heading and before the findings heading, and every foreign heading between the ledger heading and the findings heading lies after the block's closing fence, the ledger is read, `loose_layout` is True and one record is added with the first foreign heading line as `raw`. In every other case, including a foreign heading between the ledger heading and the opening fence, the reason stays `heading_between` and the ledger is missing. In strict mode any foreign heading in that span keeps the reason `heading_between`.

Update the existing assertion at `SW/tests/test_ledgerv1.py` lines 77-80 (the `between` case) so it pins the old reason `heading_between` with `lenient=False` and adds the lenient expectation (rows read, `loose_layout` True). Add fixtures `SW/fixtures/reports/forgive_fence_case.md`, `SW/fixtures/reports/forgive_heading_h3.md`, `SW/fixtures/reports/forgive_heading_colon.md` and `SW/fixtures/reports/forgive_loose_layout.md` (each derived from `SW/fixtures/reports/good.md`, one change each), and add tests for the three rules in both modes to `SW/tests/test_ledger_forgiveness.py`. Confirm by reading `_blocks_after` in `src/superclaude/cli/review/findings.py` (read only) that it compares the info string exactly and returns lines without line endings, and note that in the docstring.

Dependents that must keep working: `check_report` (uses the reader result and `ledger["reason"]`), and the existing tests of `ledger_missing`, `ledger_after_findings`, `ledger_twice`, `ledger_unclosed` in `SW/tests/test_ledgerv1.py::test_misplaced_duplicated_truncated_blocks`, which must still pass with the default mode.

Acceptance criteria:
- Each of the four new fixtures reads as a present ledger with the expected rows in lenient mode and carries one record of `fence_case`, `heading_variant` (two fixtures) or `loose_layout`; in strict mode the same four reports are `ledger_missing` with the reasons `no_block`, `ledger_heading_missing`, `ledger_heading_missing` and `heading_between`.
- A foreign heading placed between the `## Ledger` heading and the opening fence is `heading_between` in both modes; a report with a `Ledger-V1` block and an exact `ledger-v1` block is `two_blocks` in lenient mode.
- The unchanged reasons of the four existing fixtures still hold in the default mode.
- `uv run --frozen pytest -p no:cacheprovider -q SW/tests/test_ledger_forgiveness.py SW/tests/test_ledgerv1.py` passes.

## Task 3: Verify the quote matcher and add a strict reading with a quote_whitespace record

Depends on: Task 1

Edit `SW/scaffold/ledgerv1.py` (`Corpora`, `check_row`). Verify first, and state the result in the `Corpora` docstring: `fnd.flat` is `" ".join(s.split())` and `fnd.locate` flattens the text the same way, so the existing matcher already matches a quote across line wraps and doubled spaces in the candidate and the source, and `Corpora.find` compares flattened strings for the sheet and transcript corpora. Nothing is added to the lenient matching. Add what is missing: `Corpora(..., *, lenient=True)` keeps the raw strings next to the flattened ones; in strict mode `in_candidate` and `find` require the quote to occur verbatim (`quote in text`, no flattening) in the corpus text. In lenient mode `check_row` additionally tests the verbatim form and, when a quote (`quote_plan` or `quote_other`) was found only after flattening, adds a `quote_whitespace` record to a new `forgiven` list on the row (`raw` is the quote as written, `line` and `item` come from the row). The quote-not-found failure is unchanged and never forgiven.

Add the fixture `SW/fixtures/reports/forgive_quote_spaces.md` (a `quote_plan` with a doubled space and a `quote_plan` wrapped over two lines of `SW/fixtures/plans/p_basic.md`) and tests in `SW/tests/test_ledger_forgiveness.py`: doubled spaces and a line wrap match in lenient mode for the candidate, the source, a printed sheet line and a transcript result; the same rows are `quote_plan_ok` false (or `quote_other_ok` false) in strict mode; a quote absent from every corpus is not ok in both modes.

Dependents that must keep working: `check_report` (builds `Corpora` and calls `check_row`), and `SW/tests/test_ledgerv1.py` lines 327 (`Corpora(CAND, SRC, ITEMS, TRANSCRIPT)`) and 361-377 (`check_row`), plus `::test_quote_wrapping_a_plan_line_matches`, all with the default mode and unchanged expectations.

Acceptance criteria:
- `check_row` of a row whose `quote_plan` has a doubled space returns `quote_plan_ok` true and a `forgiven` list with one `quote_whitespace` record in lenient mode, and `quote_plan_ok` false with an empty `forgiven` list in strict mode.
- A verbatim quote yields no `quote_whitespace` record in either mode.
- The existing `test_quote_other_corpora` and `test_quote_wrapping_a_plan_line_matches` pass unchanged.
- `uv run --frozen pytest -p no:cacheprovider -q SW/tests/test_ledger_forgiveness.py SW/tests/test_ledgerv1.py` passes.

## Phase 2: Check and check.json carry both modes

## Task 4: Run check_report in both modes and attach the strict and lenient summaries

Depends on: Task 1, Task 2, Task 3

Edit `check_report` in `SW/scaffold/ledgerv1.py`. Add `forgiveness: str | None = None` to its keyword arguments (resolved with `forgiveness_from`). Move the existing body into a private `_check_mode(report, ..., lenient)` and have `check_report` run it twice, once per mode. The result of the chosen mode is returned exactly as today plus: `mode`, `forgiven` merged into `ledger["forgiven"]` (the reader records and the row-level `quote_whitespace` records, sorted by line), `strict` and `lenient` summaries and `mode_text_differs` (True when the two checked texts differ). A summary holds only JSON-safe counts: `ledger_missing` (bool), `reason`, `format_errors` (count), `rows` (count per verdict), `quote_rows`, `quote_plan_ok`, `demoted_findings`, `promoted` (count) and `forgiven` (count). The result must still be `json.dumps`-able once `text` is popped, because `SW/sweep/cli.py` `run_check` (line 141) pops `text` and writes the rest to `check/<rid>.ledger.json`; `SW/sweep/cli.py` itself is not edited and calls `check_report` without the new argument.

Create the fixture `SW/fixtures/reports/forgive_all.md` (derived from `SW/fixtures/reports/good.md`): lower-case verdicts, a trailing comma, a backticked item id, a `Ledger-V1` fence, a `### Ledger` heading, a `## Notes` heading between the block and the findings block and a doubled-space quote, so that all seven rules fire. Add tests to `SW/tests/test_ledger_forgiveness.py`: the lenient result of `forgive_all` records exactly the seven rule names and reads every row, its strict summary is `ledger_missing` true, and a promotion and a demotion that depend on a forgiven row differ between the two modes (`mode_text_differs` true). Add never-forgiven tests that use code-edited copies of `good.md` (and the existing fixtures `ledger_missing.md`, `unknown_item.md`, `blocking_no_cb3.md`): a missing ledger stays missing in both modes; an unknown item stays unknown; a verdict `MAYBE` stays a format error; a quote not in the plan gives `quote_plan_ok` false and the row unsupported in both modes; a row over budget keeps `limits_violated` and is not promoted; a blocking finding without the CB-3 sentence is still demoted with the cause `no_cb3` in both modes.

Dependents that must keep working: `SW/sweep/cli.py` `run_check` (reads `res["text"]` and the dict above it), `SW/tests/test_ledgerv1.py` helpers `run` (line 38) and `run_c` (line 495) and all tests that use them, and `SW/tests/test_check_flow.py` (runs `run_check` through the CLI).

Acceptance criteria:
- For every existing fixture in `SW/fixtures/reports/`, `check_report(...)["text"]` and every existing key of the result are identical to the values before this task whenever the fixture contains none of the seven deviations; `SW/tests/test_ledgerv1.py` and `SW/tests/test_check_flow.py` pass with only the Task 2 assertion edit.
- `json.dumps` of the result without `text` succeeds, and `check_report(..., forgiveness="strict")` returns the strict result as the primary and the same `strict` and `lenient` summaries.
- The six never-forgiven cases above behave identically in the two modes, and each is asserted by a named test.
- `uv run --frozen pytest -p no:cacheprovider -q SW/tests/test_ledger_forgiveness.py SW/tests/test_ledgerv1.py SW/tests/test_check_flow.py` passes.

## Task 5: Add forgiven counts, mode and per-mode totals to summarise

Depends on: Task 4

Edit `summarise` in `SW/scaffold/ledgerv1.py` and the module docstring. Add to the per-run `check.json` dict: `mode` (the mode of the reviewers' results; `lenient` when `results` is empty), `forgiven` (count per rule, every one of the seven names present, zero when unused), `forgiven_total`, `loose_layout` (reviewer ids whose ledger was read as loose layout), `mode_text_differs` (reviewer ids whose strict and lenient checked texts differ), and `strict` and `lenient` blocks each holding `ledger_missing` (reviewer ids), `reviewers` (number of reviewers with a report), `format_errors`, `rows` (count per verdict), `quote_rows`, `quote_plan_ok`, `demoted_findings`, `promoted`. Every existing key keeps its name and meaning and is computed from the chosen mode, as today. Add the new keys to the gap list as extras of check.json.

The only caller is `SW/sweep/cli.py` `run_check` (line 152), which passes `results`, a class map and `no_report` and writes the dict with `json.dumps(..., indent=1, sort_keys=True)`; that call is not edited.

Acceptance criteria:
- A test in `SW/tests/test_ledger_forgiveness.py` builds a run folder as `make_run` of `SW/tests/test_check_flow.py` does (reuse its helper by import or copy), runs `run_check` over `forgive_all`, `good` and `ledger_missing` reports, and asserts `forgiven_total`, per-rule counts, `loose_layout`, `mode_text_differs` and that the `strict` block lists the `forgive_all` reviewer under `ledger_missing` while the `lenient` block does not.
- `SW/tests/test_check_flow.py::test_check_json_counts_every_field` passes unchanged (`normalised_verdict == 3`, `format_errors == 1` for the `bad_json_line` reviewer).
- A run with no deviation has `forgiven_total == 0`, `strict` equal to `lenient` in every field, and `mode_text_differs == []`.
- `uv run --frozen pytest -p no:cacheprovider -q SW/tests/test_ledger_forgiveness.py SW/tests/test_check_flow.py SW/tests/test_ledgerv1.py` passes.

## Phase 3: Analysis reports strict and lenient per arm

## Task 6: Report the compliance gate strict and lenient, with forgiven counts

Depends on: Task 5

Edit `compliance(runs_dir)` and `cmd_compliance` in `SW/analysis/analyze.py`. Keep every existing key and its meaning (they describe the check as it ran, which is the recorded `mode`). Add: `mode` (the mode recorded in the run folders' `check/check.json`, `mixed` when they differ, `not_recorded` when absent), `strict` and `lenient` (each `ledger_missing`, `ledger_missing_rate`, `go` against `COMPLIANCE_LIMIT`, `quote_rows`, `quote_plan_ok_share`, `format_errors`; read from the `strict` and `lenient` blocks of each `check/check.json` and the `strict` and `lenient` summaries inside each `check/<rid>.ledger.json`), `go_strict`, `go_lenient`, `forgiven` (count per rule) and `forgiven_total`, and `per_arm` (the same strict and lenient figures per arm, the arm read from the run folder's `run.json`; a folder without `run.json` goes under `unknown`). A run folder whose `check.json` has no `strict` or `lenient` block (written before this change) contributes to the existing keys only and is counted in `not_recorded`; the strict and lenient figures are `null` for it rather than guessed. `cmd_compliance` prints both verdicts, for example `ledger_missing strict 2 of 15, lenient 1 of 15: strict no go, lenient go`; its exit code stays tied to the existing `go`, and the printed text says so.

Dependents that must keep working: `cmd_compliance` (same file, line 1317), `SW/tests/test_report.py::test_compliance_go_no_go` (its `make_compliance` fixture writes `check.json` and `ledger.json` without the new blocks, so it must pass unchanged), `SW/tests/test_run_schedule.py::test_spike_compliance_go_and_no_go` (runs `SW/bin/run-spike.sh compliance`, which calls this command).

Acceptance criteria:
- A new test file `SW/tests/test_forgiveness_report.py` builds run folders with `check/check.json` and `check/<rid>.ledger.json` files holding strict and lenient blocks where the strict `ledger_missing` rate is above 0.10 and the lenient rate is at or below it, and asserts `go_strict` false, `go_lenient` true, the per-rule `forgiven` counts, and the per-arm split over two arms.
- A folder written without the new blocks gives `null` strict and lenient figures and is counted in `not_recorded`, and `SW/tests/test_report.py::test_compliance_go_no_go` still passes.
- `uv run --frozen pytest -p no:cacheprovider -q SW/tests/test_forgiveness_report.py SW/tests/test_report.py SW/tests/test_run_schedule.py` passes.

## Task 7: Report the primary metric strict and lenient per arm in the analysis report

Depends on: Task 6

Edit `SW/analysis/analyze.py`: add `forgiveness_report(runs)` (a pure function over the `Run` objects of `load_runs`, using `Run.path`), extend `render_report` with an optional keyword `forgiveness=None` (the five positional calls in `SW/tests/test_report.py` must keep working), and make `cmd_all` compute the result, write `forgiveness.json` next to `metrics.json` and pass it to `render_report`. Do not define a second `found_fraction`; call the existing one (`SW/tests/test_analyze.py::test_one_definition_of_found_fraction` checks this by AST). For every arm of the runs, `forgiveness_report` returns: the run count, the runs that have a `check/check.json`, `forgiven` per rule and `forgiven_total`, the compliance gate strict and lenient (from the `check.json` blocks, with the 0.10 limit), and the primary metric strict and lenient as `{mean, runs, unscored}` over the per-run `found_fraction`. Scoring rule: a run was merged and judged under its recorded mode. It counts in that mode's mean. It counts in the other mode's mean only when its `mode_text_differs` list is empty, because then the other mode would have produced the same checked text and the same merge input. A run with a differing text is `unscored` in the other mode (re-judging it needs a model and is not done here). A run without `check/check.json` (arms Z0-raw, Z0 and K have no ledger check) counts in both modes. `render_report` prints a section `## Format forgiveness (owner order 2026-11-15)` with one block per arm: forgiven counts by rule, compliance gate strict and lenient, primary metric strict and lenient with the `unscored` counts, and one sentence saying that unscored runs need a re-judge.

Dependents that must keep working: `cmd_all` (same file, line 1257), the five `render_report` calls in `SW/tests/test_report.py` (lines 59, 72, 112, 132, 184), `SW/tests/test_analyze.py::test_metrics_match_expected_json` and `::test_one_definition_of_found_fraction`.

Acceptance criteria:
- In `SW/tests/test_forgiveness_report.py`, a synthetic world built from the run folders of `SW/fixtures/runs/make_runs.py` plus hand-written `check/check.json` files gives strict and lenient primary means equal to hand-computed values for one arm where a run's `mode_text_differs` is non-empty (that run is `unscored` in the other mode), and equal strict and lenient means for an arm with no check output.
- The rendered report contains the new section with the forgiven counts and the `unscored` counts for each arm; a report rendered without the new keyword is byte-equal to the output before this task.
- `analyze.py all` on the synthetic world writes `forgiveness.json` and exits 0.
- `uv run --frozen pytest -p no:cacheprovider -q SW/tests/test_forgiveness_report.py SW/tests/test_report.py SW/tests/test_analyze.py` passes.

## Phase 4: Documentation and the whole-suite guard

## Task 8: Document the forgiveness rules and the strict and lenient reports, then run the full suite

Depends on: Task 7

Edit `SW/DESIGN.md`: add section 9.6 "Format forgiveness (owner order 2026-11-15)" after section 9.5 with the rule table (rule name, what is forgiven, strict reading), the never-forgiven list, the record shape, the mode switch (`LEDGER_FORGIVENESS`, the `forgiveness` argument, default lenient), the `check.json` additions, the compliance and primary-metric reporting and its `unscored` rule, and the statement that the production merge `src/superclaude/cli/review/findings.py` still parses the findings block strictly and is not edited. Change item 4 of section 9.1 and the heading regex sentence of item 1 so they point to 9.6 instead of describing the old silent acceptance. State that `LEDGER_FORGIVENESS` reaches `sweep/cli.py check` the way `CHECK_SCOPE` does (`SW/bin/run-panel.sh` line 14 and `sw_py` in `SW/bin/common.sh` pass the environment through `uv run`), and that no `SW/bin/` file is edited for it. Edit `SW/TESTING.md`: add section 3.8 with requirement rows FG-1 to FG-11 (one per rule, one for never-forgiven, one for the strict and lenient `check.json`, one for the compliance report, one for the primary-metric report) each naming its test in `SW/tests/test_ledger_forgiveness.py` or `SW/tests/test_forgiveness_report.py`, and list the new fixtures in the F-REPORT row of section 2.

Acceptance criteria:
- Every `SW/tests/` function named in the new `SW/TESTING.md` rows exists (checked by grep on the test files), and each rule name of `FORGIVENESS_RULES` appears in the `SW/DESIGN.md` 9.6 table.
- `uv run --frozen pytest -p no:cacheprovider -q SW/tests -m "not slow and not freeze"` exits 0, and `uv run --frozen ruff check SW` and `uv run --frozen ruff format --check SW` exit 0.
- `uv run --frozen pytest -p no:cacheprovider -q tests/review` still exits 0 (the production merge is untouched).
- `sha256sum -c ./artifacts/frozen-before.sha256` (the baseline written in Task 1) reports every file OK, so nothing under `SW/cards/`, `SW/briefs/`, `SW/sweep/`, `SW/bin/` or `src/superclaude/cli/review/findings.py` changed; `git diff --stat -- src tests .claude` prints nothing; no file named `ground-truth*.json` was opened.
