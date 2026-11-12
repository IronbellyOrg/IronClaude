model: claude-opus-5-5 family: claude rung: top family-fallback: no GPT spawn path verified (refs/retry.md Model ladder); strongest reachable Claude model used
outcome: ready

| AC | why earlier attempts missed it (path:line) | change |
|---|---|---|
| T1.AC1 | The module docstring said "Every valid v1 finding line is a valid v2 line with the same fields" (attempt-2.diff:10). That is false. The v1 checker does not reject keys it does not know (src/superclaude/cli/review/findings.py:90-121), so a line can pass v1 and still fail v2 because it carries `calibrated_confidence`, a bad `lens`, a bad `channel` or bad `citations` (attempt-2.diff:73-74, 104-105, 119-121, 148-149). review-2.md:4 is the blocking finding for this. The compatibility test also used four lines the implementer wrote, not lines taken from the existing tests (attempt-2.diff:277-282; review-1.md:5). It never included the existing F2 line (`MINOR`, non-blocking, category contradiction) at tests/review/test_review_findings.py:51. | State compatibility only under its real condition: the line passes v1 and has none of the v2-only keys and no `calibrated_confidence`. Prove it on lines collected from the real v1 tests. Add a test showing that a v1-valid line with a bad v2 key is rejected by v2. Say that `prior` lines are rejected and that the empty-block rule is block-level, so a v1 empty block is not automatically a valid v2 block. |
| T1.AC2 | Table rules were found missing one review at a time: `coverage_rows` and citation `path` (review-1.md:3-4). Then a crash on an unhashable value was patched for one field only (probe-2-1.md:2-3, 20-21; attempt-2.diff:129). The repo-relative check still accepts `C:\x`, `C:/x` and `\\host\x`, because it only looks for a leading `/` (attempt-2.diff:58). A `quote` of `null` is treated as missing (attempt-2.diff:66). A deeply nested JSON line raises `RecursionError`, which `except json.JSONDecodeError` (attempt-2.diff:201) does not catch. | Build a table of rule to check to test from merged-requirements.md:298-311 and 313, and write exactly one check and one test per row. Put a string type check before every lookup in an allowed-value set. Add a type-fuzz test that feeds each field every JSON type and checks that nothing raises. |
| T1.AC3 | Every earlier run passed (extras-2.log:2-6). Both attempts failed in review, not in tests. The risk now is that new tests reach into private parts of the v1 module or break the v1 tests. | Collect the v1 lines without editing the v1 test files. Run `uv run ruff check` and `uv run pytest tests/review -q`. |

differs-by: Every sentence in a docstring or comment must be backed by a named test, and the v1-compatibility claim is written as a condition and proven on v1 lines collected from the existing v1 tests, not on hand-picked lines.

steps:
1. Create `src/superclaude/cli/review/findings_v2.py`. Import `_HEAD_FINDINGS`, `_ID`, `CATEGORIES`, `SEVERITIES`, `_blocks_after` and `_check_flat` from `superclaude.cli.review.findings` and leave that file unchanged. Define these tuples: `ROLES`, `LENSES`, `CHANNELS`, `DEVIATION_CLASSES`, `COMPLETION_STATES`, plus `REFLECT_CATEGORIES` (the mapping from merged-requirements.md:313, with risk allowed to be safety or other) and `V2_KEYS = ("reflect_category","citations","deviation_class","coverage_rows","self_confidence","lens","channel")`.
2. Add `_one_of(v, choices)`, which returns `isinstance(v, str) and v in choices`. Use it for every lookup in an allowed-value set (severity, category, role, lens, deviation_class, reflect_category, channel). No `in` test may run on an untrusted value without it.
3. Write `check_finding(obj, seen, lens=None)` in this order:
   - Reject the line if it has the key `calibrated_confidence`.
   - Run the v1 checks: `id` (string first, then regex), duplicate id, severity, `blocking` is a bool, MINOR cannot block, category, `claim` <=300, `refs` <=8 strings.
   - Anchor and citations: if the key `citations` is missing, `anchor` is required (12-200). If `citations` is present, `anchor` is optional but checked when present. `anchor2` follows the v1 rule: when not null, 12-200.
   - A v2-only key that is present must hold a valid value. `null` counts as invalid.
   - `citations`: a list of 1-8 objects. `role` is in `ROLES`. `path` is a non-empty string. Reject the path if `PurePosixPath(p).is_absolute()` or `PureWindowsPath(p).is_absolute()` is true, if `PureWindowsPath(p).drive` is set, if it starts with `\`, or if any part split on `/` or `\` is `..`. `line_start` and `line_end` are ints, not bools, >=1, and end >= start. If the `quote` key is present it must be a string of 12-200 characters after whitespace flattening, so `null` is rejected.
   - `self_confidence` is an int or float, not a bool, within 0..1. `coverage_rows` is a list of strings.
   - The effective lens is the line's own `lens`, otherwise the `lens` argument. If both are given and differ, reject the line. When the effective lens is `reflect-post`, `deviation_class` is required.
   - When `reflect_category` is set, `category` must be one of its mapped values, and `deviation` also requires `deviation_class`.
4. Add `channel_of(f)`, which returns `f.get("channel", "defect")`.
5. Write `parse_block(text, *, lens=None, assigned_rows=None, observed_rows=())`. Follow the v1 container flow (findings.py:124-196) with info string `findings-v2`, and add a `state` field:
   - `truncated` when the block is not closed. This wins over other errors.
   - `invalid` for any other error.
   - Otherwise `complete`.
   - Catch `(ValueError, RecursionError)` around `json.loads`.
   - Reject `prior` lines.
   - If `assigned_rows` is given, reject a finding whose `coverage_rows` names an id that is not assigned.
   - An empty valid block is `complete` only when `assigned_rows` is non-empty and every assigned id is in `observed_rows`. Otherwise it is `invalid`.
   - The parser never returns `failed` or `timed_out`.
6. Write the module docstring last, and say only what the code does:
   - (a) A line that passes the v1 checker and contains none of `V2_KEYS` or `calibrated_confidence` passes the v2 checker and comes back with the same fields.
   - (b) A v1-valid line that carries a v2 key must also meet the v2 rule for that key.
   - (c) `prior` lines are rejected, because reflect does not use the ledger loop.
   - (d) An empty v1 block is not automatically a valid v2 block.
   - (e) The parser checks that a quote is present and its length, not that it matches the cited lines.
   - (f) `coverage_rows` is checked against the slice only when `assigned_rows` is passed.
   - (g) Coverage observations come from the caller's `observed_rows`. The parser does not read them from the card.
   - (h) `failed` and `timed_out` are listed for callers and never returned.
   - Write no claims about a dispatcher, converter or verifier. Use one-line comments only.
7. Create `tests/review/test_review_findings_v2.py`:
   - (a) Collecting v1 lines: load `test_review_findings.py` by file path with `importlib.util.spec_from_file_location` from `Path(__file__).with_name(...)`. Monkeypatch `superclaude.cli.review.findings._check_finding` with a wrapper that calls the original and saves a deep copy of each object that passes. Run that module's test functions that take no arguments. Assert at least 5 lines were saved. For each saved line, assert that `v2.check_finding` returns None and that `v2.parse_block(...)["findings"]` equals `v1.parse_block(...)["findings"]` for the same line under the matching info string.
   - (b) A v1-valid line with `lens="post"` or `calibrated_confidence` passes v1 and fails v2.
   - (c) A `prior` line is rejected.
   - (d) One test for each AC2 item: neither anchor nor citations is invalid, MINOR cannot block, duplicate ids, `calibrated_confidence`, reflect-post needs `deviation_class` (also when it comes from the `lens=` argument), the empty block with and without full coverage, and `quote` absent / 11 / 12 / 200 / 201 / null.
   - (e) Citation paths `/a`, `C:\a`, `C:/a`, `\\h\a`, `../a` and `a/../../b` are rejected.
   - (f) `coverage_rows` outside the slice is rejected.
   - (g) Each mapping row, including risk to safety and risk to other.
   - (h) A null v2-only key is rejected.
   - (i) Type fuzz: for every field name plus each citation sub-field, try `None, True, 0, 1.5, "x", [], [1], {}, {"a": 1}` and assert `check_finding` returns None or a string and never raises.
   - (j) A line made of `"["*100000 + "]"*100000` gives `ok` False and does not raise.
   - (k) An unclosed block is `truncated`, and `COMPLETION_STATES` contains `failed` and `timed_out`.
8. Run `uv run ruff check src/superclaude/cli/review/findings_v2.py tests/review/test_review_findings_v2.py` and `uv run pytest tests/review -q`. Do not change any v1 file. Re-read the docstring against step 6 and delete any sentence that no test backs.
