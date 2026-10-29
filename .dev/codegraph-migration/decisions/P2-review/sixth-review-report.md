# P2 sixth review: verification of the fifth-review fixes (issue #323)

Reviewer: independent adversarial verification, read-only, 2026-10-29. Deliverables (under `.dev/codegraph-migration/`):
- A = `specs/phase-2-codegraph-install-spec.md` (736 lines)
- B = `handoff/coder-handoff-prompt.md` (79 lines)
- C = `handoff/coder-handoff-context.md` (139 lines)
- DF = `decisions/P2-serena-entry-removal/adversarial/P2-serena-entry-removal-merged.md` (50 lines)
- P1 = `specs/phase-1-removal-spec.md` (read only, as the target of T0b's checks)

Input: `decisions/P2-review/fifth-review-report.md` §1 row 2 (third-review finding 3, PARTLY) and §2 (new findings 1-4).

## Verdict: FAIL

- 5 items: 3 FIXED, 2 PARTLY, 0 NOT.
- New findings: 1 (MINOR). It was not introduced by this round's edits; it was found while checking the D24 row against its neighbours.
- What this round did not break: A:190 now has balanced parentheses (7 open, 7 close). The T0b acceptance block passes `bash -n`. The new `rg` pattern matches the literal text "absent or `{}`". A:442 describes T7's real last acceptance line. The D24 row has the same column count as D22 and D23. The layer-2 script (A:319-398, 80 lines) still passes `bash -n`.

## 1. Status of the 5 items

| # | Item | Status | Evidence | Remaining fix (PARTLY only) |
|---|---|---|---|---|
| 1 | Third-review 3: T0b acceptance did not check the Tier R "absent or `{}`" wording | PARTLY | A:439 adds `rg -q 'absent or `\{\}`' …phase-1-removal-spec.md   # Tier R/Tier K env/headers wording amended`. The check is not vacuous: P1 has no match today (exit 1), because P1:313 says "absent or empty" and P1:315 says "no `env`/`headers`". But the check searches the whole file, so one amended line anywhere satisfies it. A:433 requires both Tier R (P1:315) and Tier K (P1:325) to carry the wording, and the comment claims both are checked. I tested this on a temp file where only the Tier K line is amended and the Tier R line still says "no `env`/`headers`": the A:439 check exits 0. The fifth review's fix was anchored to the Tier R line. | Replace A:439 with two anchored checks: ``rg -q 'Tier R \(removed\).*absent or `\{\}`' …phase-1-removal-spec.md`` and ``rg -q 'Tier K .*absent or `\{\}`' …phase-1-removal-spec.md``. Tested on temp files: each fails when only the other line is amended, and the Tier R check fails on P1 today. |
| 2 | Fifth new 1: A:190 unbalanced parenthesis | FIXED | A:190 has 7 `(` and 7 `)`. The clause now reads "…whose `env` and `headers` are each **absent or `{}`** (Coder's bundle and `claude mcp add` write `"env":{}`, and the live entry on this workspace has it: third review finding 1); and (b) …". The match rule (not `serena-local`; `start-mcp-server` in args; stdio or absent type; `env`/`headers` absent or `{}`) agrees with the T3b tests at A:506 (`serena` and `foo` removed, `{}` removed, non-empty kept, no `start-mcp-server` kept, `serena-local` never removed), with B:14 and with C:65. | |
| 3 | Fifth new 2: A:441 described a different check from T7 | FIXED | A:442 now reads "(T7's last acceptance line: no `Legacy Serena registration kept` line, or that line also names codegraph)". T7's last acceptance line is A:564: `! rg -n 'Legacy Serena registration kept' CHANGELOG.md \|\| … \| rg -q 'codegraph'`. The pattern and the escape condition match. | |
| 4 | Fifth new 3: DF:5 credited D23 with changes D23 does not record | PARTLY | A D24 row exists (A:717), and DF:5 now says "Amended by Phase 2 spec D23 and D24 (§2.12)". DF:5 credits D23/D24 with six changes. Four are recorded there: `{}` (D23), shape match (D24), the predicate (D23, D24), and `startup.sh` (D24). Two are not. (a) "acceptance is the two `jq` checks in spec §2.12": neither D23 (A:718) nor D24 (A:717) mentions the split user-scope/local-scope acceptance. The fifth review's fix text listed "split two-scope acceptance" for D24. (b) The narrowed "never left with neither" wording is recorded only in D22's rationale (A:716, "never removes the current-pin Serena entry while codegraph is missing"), not in D23 or D24. | In D24's Decision cell add "§2.12 acceptance split into user-scope and local-scope `jq` checks". Then either add "the 'never left with neither' claim is narrowed (D22)" to D24, or change DF:5 to "Amended by Phase 2 spec D22-D24 (§2.12)". |
| 5 | Fifth new 4: match-rule wording drift (B:14 missing stdio; A:190 keyed the kept case by name) | FIXED | B:14 now reads "matched by `start-mcp-server` in its args under any name except `serena-local`, stdio, `env`/`headers` absent or `{}`", the same as C:65. A:190 now reads "A launcher entry (any name) with a non-empty `env` or `headers` is kept and reported", so the kept case is matched by shape. `serena-local` is never removed (next sentence), so "(any name)" does not contradict the rule. | |

## 2. New findings

1. **MINOR (not introduced this round). The D21 row in the Decisions table has an extra column.**
   - Location: A:719. The header (A:711) and every other row from A:711 to A:737, including D24 (A:717), have 6 pipes. A:719 has 7.
   - Evidence: the Decision cell contains the code span `pgrep -f 'codegraph\.js (init|index)'`. In GitHub-flavoured Markdown an unescaped `|` splits a table cell even inside backticks. The row therefore renders as 6 cells under a 5-column header: the code span breaks at `(init`, the Options column shows `index)'`…, and the Rationale text is dropped. No other table in A, B or C has a pipe-count mismatch (mechanical scan, `\|` removed first).
   - Fix: write `(init\|index)` in that cell. The same pattern in prose (B:27, A §3) does not need escaping.

## 3. Checks run and results

- **A:190 rule bullet.** Parentheses: 7 open, 7 close. Backticks: 32 (even). The sentence parses as: (a) [shape clause] (justification); and (b) [kind-B clause]. The match rule agrees with T3b (A:506), B:14, C:65 and DF:5.
- **B:14.** Parentheses: 2 open, 2 close. Contains "stdio".
- **T0b block (A:437-440).** Extracted and run with `bash -n`: passes.
  - `rg` pattern test on a temp file. "Tier R: env/headers absent or `{}`" matches (exit 0). "no `env`/`headers`", "absent or {}" without backticks, and "absent or `{ }`" do not match (exit 1).
  - On P1 today: `rg 'absent or `\{\}`'` exits 1. `rg -c codegraph_ready` prints nothing (exit 1), so the `-ge 7` test still fails correctly.
  - Weakness found: a temp file with only the Tier K line amended passes A:439 (item 1).
- **T0b commit line (A:442) against T7 (A:554-566).** T7's last acceptance line is A:564, and it matches A:442's description.
- **Decisions table (A:711-737).** D24 has 6 pipes, the same as D22, D23 and the header. Its backticks are balanced (28). D24 sits between D22 and D23. The table was already out of numeric order (D3, D22, D23, D21, D15 …), so this is not a defect. D21 has 7 pipes (new finding 1).
- **DF:5.** Parentheses 5/5, backticks 20. Each listed change checked against D22, D23 and D24 (item 4).
- **Layer-2 script.** Extracted A:319-398 (`#!/usr/bin/env bash` to `echo "LAYER2_OK"`): 80 lines, `bash -n` passes. This is the same length as the fifth review's extraction.
- **Cross-file consistency.** The acceptance `jq` expressions at A:205-206 and C:67 are byte-equal (`diff` empty). The "Ready for Serena retirement" line is at A:125 and A:137, which D24 references correctly.

## 4. Self-audit

- **Read in full:** the fifth review report, B and DF.
- **Read in part:** A:180-214, A:425-449, A:500-569 and A:708-737. P1 lines 269, 307-325, 354, 361, 368 and 811, via `rg`/`sed`. C:65, C:67 and C:92.
- **Ran** (two private `mktemp -d /tmp/p2-sixth-review.*` directories, each removed by a trap):
  - parenthesis and backtick counts;
  - `bash -n` on the T0b block and on the layer-2 extraction;
  - `rg` positive and negative tests of the A:439 pattern and of the proposed anchored patterns on temp files;
  - the `rg` checks against P1;
  - a pipe-count scan of every table in A, B and C;
  - a `diff` of the acceptance `jq` between A and C;
  - a `grep` for D24 references.
- **Not done:**
  - no edits except this report;
  - no installs, MCP registration changes, test suite, commit or push;
  - the layer-2 script was not executed (it needs T1-T5 code);
  - the `jq` expressions were not re-run, because they are byte-identical to the ones earlier reviews tested;
  - no history diff was possible, because `.dev/codegraph-migration/` is untracked. "Introduced this round" is judged from the author's list of edited locations and from the fifth review's quotes.
- **Limits:**
  - Severity is my judgment.
  - Under the "any issue fails" rule, the two PARTLY items alone make the verdict FAIL.
  - New finding 1 is pre-existing. It is reported because the D24 check covered the whole table, and it does not change the verdict.
