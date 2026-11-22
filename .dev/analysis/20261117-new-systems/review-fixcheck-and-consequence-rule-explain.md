# Explanation (advanced): consequence-based review rule and `superclaude review fixcheck`

Source: origin/master (PR #582, commit 64e8eacf2, merged 2026-11-17T03:32:58Z). The local checkout does not hold this code; every line below was read with `git show origin/master:<path>`. Codegraph was not used (index does not cover origin/master).

## 1. The idea

Old rule: a review finding blocks when it is "a real defect" (wrong behaviour, false claim, missing deliverable, security risk). Reviewers then graded by label (CRITICAL, IMPORTANT) and too many cosmetic or harmless findings failed reviews and started fix passes.

New rule (src/superclaude/output-styles/pragmatic.md lines 229-235): grade a finding by what changes if the flawed text is corrected. Only three conditions block:

- Decision: the correction would change a named decision, recommendation, destination, required behaviour, outcome, acceptance check or quoted number that the deliverable (or a named later step) rests on, or the stated reason for it is false. A wrong number in an acceptance check blocks even if the recommendation is unchanged.
- Missing: a required deliverable, section, behaviour or step named by the task, template or acceptance criteria is absent in substance.
- Safety: following the text or running its code would lose or expose data or a secret, break a safety boundary, or act outside scope. Never downgraded by label, score, intent or fix cost. An unverified safety claim stays open.

Everything else: a real defect nothing named rests on is Medium (never fails, never starts a fix pass, listed under `follow-up candidates`, user asked once per run and again at an escalation halt); a defect of form only is a Note. The reviewer's own label (CRITICAL, IMPORTANT, MAJOR, High) is information, not the grade. Exception: if no consumer can be established, the reviewer keeps its own label and tags the row `consumer-unknown` ("Unknown is not no"). If several definitions of blocking are in context, the one in the running agent/skill/command wins over the session-wide output style.

## 2. Carriers

The same text is copied into ten carrier files (rf-qa, rf-qa-qualitative, two document templates, two workflow templates, four rule prompts); rf-analyst got a one-line change to its merge rule. rf-qa and rf-qa-qualitative were rewritten so checks no longer say "any X = FAIL": for example an untagged doc claim is now "Missing and blocks" only because a required tag is absent. Merge of partition reports changed from "take the more severe rating" to "consolidator grades each item by the rule and keeps every reviewer's own grade visible"; a blocking grade with no named consumer is sent back once (`reasked`), then the reviewer's label stands with `consumer-unknown`, listed first.

Cap behaviour: after 2 fix cycles (3 reviews) HALT; user picks fix by hand, accept and file each open blocker as an `accepted-blocker` follow-up, or stop.

## 3. fixcheck

`superclaude review fixcheck --file F (--base COPY | --lines S-E)`, repeatable per file. Read-only. After a fix, the fix agent runs it over the lines it edited and records every result (passes too) in the fix log. Lines come from either `--base` (difflib SequenceMatcher: lines new or changed vs the pre-fix copy, fixcheck.py:46-53) or `--lines` (parse_range, fixcheck.py:37-43). One output line per check, `check file line PASS|FAIL detail`, then `fixcheck: N checks, P passed, F failed`. Always exit 0 on results (the verifier decides); exit 2 for unusable input (fixcheck_cmd.py:17-35, 44-61).

Checks (fixcheck.py:86-169):
- range: requested line outside the file is a FAIL, not skipped.
- pipe: for a markdown table row, unescaped pipe count (outer pipes normalized, `_pipes` 67-75) must equal the header row; if the edited row is the header, compare with the separator row (fixes the self-compare bug found by Codex in review). Catches the "run 2" bug: an unescaped `|` inside a backticked command adds a cell.
- quote: `"text" path:line` cite; the quote must be byte-present on that line (cited file tried as given, then relative to the edited file).
- count: a line saying `N rows` directly above a table must match the table's data row count.
- link: relative `[text](path)` must exist; URLs, anchors, mailto skipped; percent-decoded and anchors stripped.

## 4. Pitfalls and limits

- fixcheck is advisory, mechanical, and only sees the shapes above; it cannot say the fix is right.
- The rule is prompt text. Nothing in code computes grade; behaviour depends on reviewers following it. Tests pin text, not behaviour.
- Not live on any machine until `superclaude install --force` (make sync-dev does not copy output styles).
- docs/developer-guide/review-severity-rule.md line 24 still holds the old sentence (outside the scan roots), per the owner note.
- Pre-handback fixcheck step is wired only into rf-qa and rf-qa-qualitative; no other file under src/superclaude mentions fixcheck (git grep).

## 5. Tests

tests/review/test_review_fixcheck.py (17 tests: run-2 pipe, escaped pipe, header vs separator, outer pipes, out-of-range, percent-decoding, quote, count, link, base diff, exit codes, read-only). tests/skills/test_review_old_rule_scan.py walks `*.md` under src/superclaude and plugins/superclaude and fails if the old sentence returns. tests/audit re-pins (Rule 6 text and block hash in test_severity_floor_unweakened.py; PASS/FAIL bullets in test_nfr_conv_9_zero_trust.py).
