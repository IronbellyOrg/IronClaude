model: claude-opus-5-5 family: claude rung: top
outcome: ready

| AC | why earlier attempts missed it (path:line) | change |
|---|---|---|
| T1.AC1 | The module docstring said every valid v1 finding line is a valid v2 line (attempt-2.diff:10-11). The v1 checker ignores keys it does not know (findings.py:90-121), so a line can be valid under v1 while carrying `calibrated_confidence`, `lens`, `citations` or `channel` values that v2 rejects (attempt-2.diff:73-74, 104-105, 120-121, 148-149). That is the blocking finding at review-2.md:4. The compatibility test also wrote its own 4 lines instead of using the existing tests' lines (attempt-2.diff:277-282, review-1.md:5). | Define one constant, `V1_FIELDS`. Every compatibility statement is limited to "a v1-valid line whose keys are all in `V1_FIELDS`". Test it on lines built by the existing v1 test helper and the rule-text example line. Also test the opposite case: a v1-valid line carrying `calibrated_confidence` passes v1 and fails v2. |
| T1.AC2 | The required tests existed, but some table rules were missing or not always enforced. The coverage slice was not checked at first (review-1.md:3), and after the fix it was still skipped when no slice was given (attempt-2.diff:211, 397). Citation paths were only checked for being non-empty (review-1.md:4), and the fix still accepts Windows drive and backslash-rooted paths (attempt-2.diff:58). A list or dict value crashed a membership test (probe-2-1.md:3). The table says the brief sets `lens` (merged-requirements.md:310), but `deviation_class` was only required when the line itself said `reflect-post` (attempt-2.diff:119-126). | Move every table rule into one line checker that takes the block context (`lens`, `assigned_rows`) as arguments. Add a test table with one passing and one failing case per table row, plus a test that feeds every JSON value type into every field. |
| T1.AC3 | Not the cause of failure. ruff and pytest passed (extras-2.log:2-6). Both attempts failed on scope findings. | Keep the existing v1 tests untouched. Run `uv run pytest tests/review -q` and `uv run ruff check` on both new files. |

differs-by: The block context (brief `lens`, assigned Coverage slice) goes into the line checker, so every table rule is enforced on every line with no "no slice given, skip" path. Each docstring sentence must be paired with a test that checks it, including a test that proves the stated limit of the v1-compatibility claim.

steps:
1. Create `src/superclaude/cli/review/findings_v2.py`. Import `_HEAD_FINDINGS`, `_ID`, `CATEGORIES`, `SEVERITIES`, `_blocks_after` and `_check_flat` from `superclaude.cli.review.findings`, and do not edit findings.py. Define these constants:
   - `V1_FIELDS = ("id","severity","blocking","category","anchor","anchor2","refs","claim")`
   - `ROLES`, `LENSES`, `CHANNELS`, `DEVIATION_CLASSES`, `COMPLETION_STATES` as tuples
   - `REFLECT_CATEGORIES` as a dict from each reflect label to a tuple of allowed v1 categories (risk maps to safety or other).
2. Write a helper `_one_of(value, allowed)` that returns False unless `isinstance(value, str)` and then checks membership. Use it for every enum check: severity, category, role, lens, deviation_class, channel, reflect_category. Never test membership in a dict or set directly on a raw JSON value.
3. Write `_check_citation(c)` with these rules:
   - `c` must be a dict.
   - `role` passes `_one_of(role, ROLES)`.
   - `path` is a non-empty str and repo-relative. Reject it when `PurePosixPath(path).is_absolute()`, when `PureWindowsPath(path).is_absolute()` or it has a `.drive`, when it starts with `\` or `/`, or when any segment (after turning `\` into `/`) is `..`.
   - `line_start` and `line_end` are ints, not bools, both at least 1, with end not before start.
   - `quote` is optional (absent or null). When present it must pass `_check_flat(quote, "citation quote", 12, 200)`.
4. Write `check_finding(obj, seen, *, lens=None, assigned_rows=None)`, the single v2 line checker, in this order:
   - Reject `calibrated_confidence`.
   - Apply the v1 rules for id, duplicate id, severity, blocking bool, MINOR not blocking, category, claim <=300 and refs (list, at most 8 strings), with the same messages as findings.py:90-121.
   - `citations`: absent or null means `anchor` is required (12-200 characters). Otherwise it must be a list of 1 to 8 entries, each passing `_check_citation`, and `anchor` is optional but still checked when non-null. `anchor2` is checked when non-null.
   - `lens`: if both the line value and the `lens` argument are given, they must be equal; a mismatch is an error. The effective lens is the line value or the argument, and it must be in `LENSES`.
   - `deviation_class` is required when the effective lens is `reflect-post`, and must be in `DEVIATION_CLASSES` whenever present.
   - `reflect_category` must be in `REFLECT_CATEGORIES`, `category` must be one of its mapped values, and `deviation` requires `deviation_class`.
   - `coverage_rows` must be a list of strings. If it is non-empty, every id must be in `assigned_rows`. When `assigned_rows` is None, a non-empty list is an error ("no Coverage slice to check against").
   - `self_confidence` is an int or float (not a bool) with `0 <= x <= 1`, which also rejects NaN and infinity.
   - `channel` must be in `CHANNELS` when present.
   - Unknown keys are ignored, as v1 ignores them. The checker never changes `obj`.
5. Write `channel_of(f)`, which returns `f.get("channel")` when it is a str in `CHANNELS`, else `"defect"`. Do not add `channel` to parsed findings, so the parser's output fields stay the same as v1's (only `refs` gets its default, as in v1).
6. Write `parse_block(text, *, lens=None, assigned_rows=None, observed_rows=())`:
   - Use the same container steps as findings.py:124-196 with info string `findings-v2`.
   - Reject a `prior` line with an error saying v2 does not accept prior lines.
   - Pass `lens` and `assigned_rows` (as a set of str) to `check_finding`.
   - Return `{ok, state, findings, errors}`. The state is `truncated` for an unclosed fence (it beats invalid) and `invalid` for any other error.
   - A closed, error-free empty block is `complete` only when `assigned_rows` is non-empty and every assigned row is in `observed_rows`; otherwise it is `invalid`.
   - `parse_block` never returns `failed` or `timed_out`.
7. Write the docstrings and comments so each sentence states one fact the code does:
   - The module docstring says: "A line that findings-v1 accepts and whose keys are all in V1_FIELDS passes check_finding unchanged." It also says that v1-valid lines with other keys may be rejected, names `calibrated_confidence` as the example, says prior lines are rejected, and says `observed_rows` is supplied by the caller.
   - The comment on `COMPLETION_STATES` says only that `parse_block` returns complete, truncated or invalid, and that the other two are for callers.
   - Do not write any sentence about other modules or later behavior.
8. Create `tests/review/test_review_findings_v2.py` with these tests:
   - (a) v1 compatibility: import `line` from `tests/review/test_review_findings.py`. If import is awkward, copy its base dict verbatim with a comment naming the source line. Feed every variant used in that file's passing cases (default, MINOR non-blocking, `anchor2` with spaces, the `refs` text at line 203) plus the rule-text example line from test_review_rules_text.py:68 with its placeholders filled. For each, assert that `findings.parse_block` is ok, `check_finding` returns None, and the v2 `parse_block` returns the same dict plus `refs`.
   - (b) the stated limit: a line with `calibrated_confidence` passes v1 and fails v2.
   - (c) prior lines are rejected.
   - (d) each listed rule: neither anchor nor citations, MINOR blocking, duplicate id, `calibrated_confidence`, `deviation_class` required for reflect-post set by the line and set by the `lens` argument, line/argument lens mismatch, empty block invalid without observations and invalid with partial or empty `assigned_rows`, complete with full coverage, quote absent / null / 11 / 12 / 200 / 201 characters.
   - (e) one passing and one failing case per table row, including citation paths `/a`, `C:/a`, `\\srv\a`, `\a`, `a/../../b`, `..`, plus coverage_rows outside the slice and coverage_rows with no slice.
   - (f) a crash test: for each field in `V1_FIELDS` plus every v2 field and every citation key, set the value to each of `None, True, 0, 1.5, float("nan"), "x", [], [1], {}, {"a":1}` and assert `check_finding` returns None or a str without raising.
   - (g) a test that `channel_of` defaults to `"defect"`.
9. Run `uv run ruff check src/superclaude/cli/review/findings_v2.py tests/review/test_review_findings_v2.py` and `uv run pytest tests/review -q`. Confirm that `git diff --stat` shows only the two new files.
10. Before handing back, list every docstring and comment sentence next to the test that checks it. Delete any sentence that has no test or is broader than its test.
