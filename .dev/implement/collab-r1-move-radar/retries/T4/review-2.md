start=397b62f0e95b6dad3c9c888d7928c60899f86a87 tree=c31b01bb03266679fc53cbefa497c6d358392f68
## Earlier blocking findings

F1.1 resolved
F2.1 resolved

Evidence:
- F1.1: `DROPPED=$(jq '.dropped_lines' ...)` (tools/run-reviewer.sh:117) now reads `dropped_lines` from h2.json, which counts block lines, not errors (tools/h2_normalize.py:49-61). With the heading and a block, it counts the non-blank body lines of the last block that carry an error. Block-level notices sit on the fence line, which is outside the body, so they count 0. Without the heading, or with no block after it, every non-blank line of the last findings-v1 fence counts. Probes: an unclosed block with one bad line gives `dropped_lines` 1, not 2 (/tmp/collab-r1/probe-T4-2-2/unclosed.json). Tests: tests/test_h2.py:87 (one bad line of two gives 1; wrong heading gives 2; two blocks give 0) and tests/test_h2.py:101 (runner, wrong heading: `meta.dropped_lines` = 2). All pass.
- F2.1: the code now splits with `text.splitlines(keepends=True)` (tools/h2_normalize.py:25), the same splitter `_blocks_after` uses (src/superclaude/cli/review/findings.py:49), and keeps each line's terminator (tools/h2_normalize.py:42-45). I re-ran the original probe with U+2028, \x85 and \x1c in the prose before the block (/tmp/collab-r1/probe-T4-2-2/u2028.md). Result: `ok:true`, `truncated:1`, `dropped_lines:0`, and only output line 10, the over-long finding, differs from the input. tests/test_h2.py:115 covers \x0c and passes.

## Acceptance criteria

- T4.AC1: unmet [F3.2].
  - Met: section 2.7 command, model and block check, retry, hang guard, H2 re-ask and outputs (T4.AC1@.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/run-reviewer.sh:31-33, :59-67, :79-82, :57, :89-118, :127-134).
  - Met: section 2.6 formulas and Spike 4 (tools/values.py:32, :37, :47, :66, :89, :129), and the section 4 planning guard and refusal (tools/values.py:195, :198).
  - Met: the R-05 allowed set in `--print-cmd` (tools/run-reviewer.sh:35-38).
  - Unmet: for a report with CRLF or CR line endings, the H2 normaliser rewrites every line, not only the block (tools/h2_normalize.py:67). See F3.2.
- T4.AC2: met.
  - `uv run pytest .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests -q` gives 97 passed in 25.17 s.
  - Each test checks what DESIGN.md 6.1 or 6.2 lists for it:
    - T-10 cmd part: tests/test_settings_and_cmd.py:50 and :61.
    - T-11: tests/test_h2.py:31-81.
    - T-12: tests/test_values.py:38, :48, :52, :76.
    - T-13: tests/test_runner_retry.py:6 and :21.
    - F-8 runner part: tests/test_faults.py:39.
    - F-9: tests/test_faults.py:55.
    - F-10 runner part: tests/test_faults.py:64.
    - F-13: test_f13 in tests/test_faults.py.
  - F-13 note: the test breaks the hook's index so the hook logs `hook_error` and exits 0. It does not make the hook `exit 1`. The pass condition (review completes, `hook_error` logged) is still checked. I do not raise this as a finding.

F3.2 sev=blocking trigger=B2 ac=T4.AC1 at=.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/h2_normalize.py:4 anchor=.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/h2_normalize.py:67 chk=n,y,n,n family=h2-line-endings fix=read and write with newline="" (open(src, encoding="utf-8", newline="") and open(out, "w", encoding="utf-8", newline="")) so \r\n and \r terminators survive; add a T-11 case with CRLF input that asserts only the block line changes first=A1 origin=late covers="writes the report with only the block rewritten": The docstring says "Writes out.md (only the block lines rewritten)" (h2_normalize.py:4), and the comment at :23-24 says the code keeps "each line's own terminator". But the report is read in universal-newline text mode (`open(src, encoding="utf-8").read()`, :67), which turns every \r\n and \r into \n before normalise runs, and it is written back with \n. Probe: /tmp/collab-r1/probe-T4-2-2/crlf.md and cr.md each have 12 lines and one over-long claim. In both outputs all 12 lines differ from the input; with LF input, 1 line differs. The parse result is the same (ok:true, kept 2, dropped 0), so the merge sees the same findings. The defect is the false claim and the literal 1.2 behaviour, not merge content.
F4.2 sev=note trigger=none ac=scope at=.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_h2.py:116 anchor=.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_h2.py:117 chk=n,y,n,n family=h2-line-index first=A2 origin=fix-induced fix=either insert a U+2028 into the replaced prose as well as the \x0c, or reword the comment to name only the form feed: The test comment says "U+2028 and a form feed in the prose", but the input at :117 inserts only `\x0c`. The U+2028 case is not exercised by the suite. My probe (/tmp/collab-r1/probe-T4-2-2/u2028.json) shows the code handles it, so only the comment is wrong.
