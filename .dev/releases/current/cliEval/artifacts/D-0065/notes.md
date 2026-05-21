# D-0065 — Implementation notes

## Why this task was test-only

T04.01 (D-0064) shipped the full `Expect.file` body alongside the
package skeleton — the file existed, contains/regex/equals branches
worked, and one happy/one sad case was exercised in
`tests/cli/eval/test_expect_primitives.py`. T04.02's deliverable is the
**per-primitive acceptance harness** that touches every named argument
and the unified-diff failure contract. No body changes were required to
`src/superclaude/cli/eval/expect.py`.

## Decisions

1. **Unified diff lives in `details["diff"]`, not the message.** The
   M1 stubs put compact reasons in `result.message` for the console
   reporter; a multiline diff there would smear the one-line summary.
   Keeping the diff in `details` lets the Reporter (T03.13) render it in
   the verbose section without re-parsing.
2. **`exists=False` short-circuits content checks.** When a manifest
   asserts a side-effect file should *not* be present, the primitive must
   not then attempt to read the (absent) file and crash. The existing
   implementation already had this; the test
   (`test_exists_false_passes_when_missing`) pins the contract.
3. **`regex` uses `re.search`, not `re.match`.** Manifest authors expect
   "does the pattern appear anywhere in the file" semantics; the test
   `test_regex_matches_across_lines_via_search` documents this.
4. **Path resolution at call time.** The closure resolves
   `ctx.home_path / path` inside `_run`, not at primitive construction,
   so one manifest-built callable runs against many EvalContexts (one per
   eval invocation).

## Things explicitly not covered here

* `regex` invalid-pattern handling — `re.compile` raising on bad regex
  is intentional fail-fast at primitive construction; covered by the
  declarative loader tests in T01.14.
* Binary-file behaviour — the primitive decodes UTF-8 with
  `errors="replace"`, so binary fixtures degrade gracefully but should
  not be the test target. Manifest authors expecting binary content
  comparison must use a custom helper.
* `equals` whitespace normalisation — none performed; `equals` is strict
  byte-for-byte (after UTF-8 decode). This matches the FR-EXP1 spec.

## Follow-ups

None. Two adjacent tasks consume this primitive:

* T05.02 (E1) wires `Expect.file` into the sticky-lifecycle eval.
* T05.10 (E9) wires it into per-matcher artifact assertions for the
  coverage gate.

Both pass without any further changes to `Expect.file`.
