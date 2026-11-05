# T3 spec-compliance QA

Task: "## Task 3: Add the single-source claim test and the changelog entry" (plan lines 76-87). Spec: FR-ONB.4 (spec.md:239-249). Start snapshot: 6ce4a2e58d37052c6623058362b4a81dad0dcdd5.

Reviewer note: the implementer's report was not trusted. Every check below was re-run by the reviewer.

## Diff under review

- New untracked file `tests/docs/test_onboarding_deck.py` (114 lines; not in the snapshot tree).
- `CHANGELOG.md`: against the snapshot, the only change is +5 lines, the `#### Added (onboarding deck)` subsection (CHANGELOG.md:19-22). The Part A lines 7-17 are identical to the snapshot.
- No other file changed: the deck, `src/superclaude/core/HOW-WE-WORK.md` and `src/superclaude/commands/recommend.md` are byte-identical to the snapshot (checked with `cmp`).

## Independent runs (repo root, no files written)

- `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/docs/test_onboarding_deck.py -v -p no:cacheprovider`: 3 passed.
- `uv run ruff check --no-cache tests/docs/test_onboarding_deck.py`: All checks passed.
- `uv run ruff format --no-cache --check tests/docs/test_onboarding_deck.py`: 1 file already formatted.
- The log artifacts/t3-tests.log matches: 3 passed. It records an initial format failure, then a formatting-only fix, then a pass. It also lists 35 distinct tokens taken from the real deck, so the real-deck test does not pass on empty input.

## Acceptance criteria

- T3.AC1 met. `uv run pytest tests/docs/test_onboarding_deck.py -v` passes (3 tests: tests/docs/test_onboarding_deck.py:83, :90, :94), and the output is saved in artifacts/t3-tests.log:1-13. The reviewer's re-run gave the same result.
- T3.AC2 met. The in-memory check is at tests/docs/test_onboarding_deck.py:94-113:
  - An unknown slash command (`/sc:not-a-command`, `/svg-only-command`) and an unknown flag (`--no-such-flag`, `--title-flag`) are planted at :98 and :101, and :105-111 asserts they are reported.
  - The planted path `.dev/tasks/to-do/x/x.md` (:100) is not in the expected list, and the assertion checks the whole list for equality.
  - A missing footer fails the regex (:112), and a valid footer matches it (:113).
  - Because the assertion at :105 checks a non-empty list for equality, the test fails if extraction finds nothing. The reviewer confirmed this: `<p>/sc:fake --fake</p>` returns `[]`.
- T3.AC3 met.
  - The scanned elements are `_CLAIM_TAGS = {"code", "text", "title", "desc"}` at tests/docs/test_onboarding_deck.py:26. A `<title>` counts only inside an `<svg>` (:38-51), so the page `<title>` is skipped.
  - Whole-token lookup is at :64-66. `_has_token("/task", "/task-builder")` is False, so `/task` is not satisfied by `/task-builder`, and the planted `/task` at :99 is reported at :110.
  - Adversarial checks by the reviewer:
    - Page-level `<title>/page-cmd --page-flag</title>` returns `[]`.
    - SVG `<desc>`, a `<tspan>` inside `<text>`, and an upper-case `<TITLE>` inside an svg are all reported.
    - A `<title>` after `</svg>` is ignored.
    - `src/jobs/runner.py`, `.dev/tasks/to-do/x/x.md` and `&lt;id&gt;/&lt;id&gt;.md` are not flagged.
  - The token rule matches the task text. Commands are matched at :19-21 (start of text, or after whitespace, an opening bracket or a quote; then `[a-z][a-z0-9-]*`, with an optional `:name`). Flags are matched at :22.
  - `--plugin` is sent to `src/superclaude/commands/recommend.md` at :12, :15 and :76-77. That file contains `--plugin` 15 times and HOW-WE-WORK.md contains it 0 times, so the guide on its own would fail it.
  - The footer regex at :23 requires a 7-40 character lower-case hex sha. The reviewer checked: 6 hex fails, 8 and 40 hex match, 41 hex fails, upper case fails, a trailing letter fails. The maintenance comment at docs/onboarding/ironclaude-onboarding.html:4 has no sha, so it cannot satisfy the regex. The real footer is at docs/onboarding/ironclaude-onboarding.html:596.
- T3.AC4 met. Both ruff commands pass. This is the reviewer's own run with `--no-cache`, and it matches artifacts/t3-tests.log:21-24.
- T3.AC5 met. The Part B entry is at CHANGELOG.md:19-22. It names `docs/onboarding/ironclaude-onboarding.html` (:21) and `tests/docs/test_onboarding_deck.py` (:22). It sits under the line 7 routing heading (CHANGELOG.md:7) and above the next `###` heading (CHANGELOG.md:24). It is written in plain English.

## Spec cross-check (FR-ONB.4, spec.md:245-247)

- `<code>` commands and flags are checked against the guide, with the `--plugin` exception (spec.md:245): tests/docs/test_onboarding_deck.py:69-87.
- The footer check (spec.md:246): tests/docs/test_onboarding_deck.py:90-91.
- pytest passes (spec.md:247): see T3.AC1.

## Observations (not AC breaches)

- The whole-token lookahead `(?![\w-])` at tests/docs/test_onboarding_deck.py:66 allows `:`, `.` and `/` after a token. So `/sc` would be satisfied by `/sc:workflow`, and `/task` by `/task.md` in the guide (the reviewer confirmed both). The AC only requires `/task` not to be satisfied by `/task-builder`, which holds. Tightening the lookahead to `(?![\w:/.-])` would close the gap. Optional.
- The in-memory check does not plant a `--plugin` case. Its routing was confirmed by the reviewer's own run instead (`<code>--plugin</code>` returns `[]`). This is not required by the AC.

## extra_scope

none. Only the new test file and the CHANGELOG subsection changed. No routing surface, guide or deck file was touched.

## misunderstood

none

VERDICT: compliant
