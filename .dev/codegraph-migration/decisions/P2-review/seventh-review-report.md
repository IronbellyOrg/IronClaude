# P2 seventh review: verification of the sixth-review fixes (issue #323)

Reviewer: independent adversarial verification, read-only, 2026-10-29. Deliverables (under `.dev/codegraph-migration/`):
- A = `specs/phase-2-codegraph-install-spec.md` (737 lines)
- DF = `decisions/P2-serena-entry-removal/adversarial/P2-serena-entry-removal-merged.md` (49 lines)
- P1 = `specs/phase-1-removal-spec.md` (read only, as the target of T0b's checks)

Input: `decisions/P2-review/sixth-review-report.md` §1 rows 1 and 4 (PARTLY) and §2 new finding 1.

## Verdict: PASS

- 3 items: 3 FIXED, 0 PARTLY, 0 NOT.
- New findings: 0.
- What this round did not break: the T0b acceptance block (A:437-441) passes `bash -n`. Every row of the Decisions table (A:712-737) has 6 unescaped pipes, the same as the header. A full scan of every table in A finds no row whose pipe count differs from its header. D24 (A:718) has balanced parentheses (4/4), quotes (4) and backticks (30). DF:5 has balanced parentheses (5/5), backticks (20) and bold markers (4).

## 1. Status of the 3 items

| # | Item | Status | Evidence |
|---|---|---|---|
| 1 | Sixth 1: T0b acceptance not tied to the Tier R and Tier K lines | FIXED | The single file-wide check is replaced by two anchored checks. A:439: ``rg -q 'Tier R \(removed\).*absent or `\{\}`' …phase-1-removal-spec.md   # Tier R line amended``. A:440: ``rg -q 'Tier K \(kept.*absent or `\{\}`' …phase-1-removal-spec.md      # Tier K line amended``. The anchors match the real P1 line prefixes: P1:315 starts `**serena, Tier R (removed):**` and P1:325 starts `**serena, Tier K (kept, one printed line per run):**`. These are the only two P1 lines with either prefix. Temp-file matrix, built from the real P1:315 and P1:325 text (exit 0 = match): only Tier R amended gives R=0, K=1; only Tier K amended gives R=1, K=0; both amended gives R=0, K=0; neither amended gives R=1, K=1. `absent or {}` without backticks gives R=1, K=1. On P1 today both checks exit 1, so neither passes vacuously. Each check now fails when only the other line is amended, which was the sixth review's defect. A:433 ("Tier R and Tier K match `env`/`headers` absent or `{}`") and D24 (A:718, "plus the `absent or {}` wording on the Tier R and Tier K lines") describe what A:439-440 check. |
| 2 | Sixth 4: D24 row incomplete; DF:5 credited only D23-D24 | FIXED | D24's Decision cell (A:718) now records "the §2.12 acceptance is split into a user-scope and a local-scope `jq` check (local-scope hits mean "run the printed command")". This matches A:205 (user scope, by name and by launcher shape) and A:206 (local scope, where a failure "means the user must run the printed `claude mcp remove <name> --scope local` command"). D24 also records "the Serena decision record carries an "Amended by D22-D24" note". DF:5 now reads "Amended by Phase 2 spec D22-D24 (§2.12)", which is the second remedy the sixth review offered. DF:5's "never left with neither" narrowing is recorded in D22 (A:717: "gating on codegraph readiness never removes the current-pin Serena entry while codegraph is missing"), so every change DF:5 lists is now recorded in D22, D23 or D24. A `rg` for `D22-D24`, `D23-D24` and `D23 and D24` across A, DF and `handoff/` finds only A:718 and DF:5. No stale "D23-D24" or "D23 and D24" text is left. |
| 3 | Sixth new 1: unescaped `\|` in D21's `pgrep` pattern | FIXED | A:720 now reads `` `pgrep -f 'codegraph\.js (init\|index)'` ``. With `\|` removed first, the row has 6 pipes, like the header (A:712) and every other row (A:714-737). If the row is split on unescaped pipes, it gives the 5 expected cells. Cell 2 (Decision) ends with the whole code span, `` `pgrep -f 'codegraph\.js (init\|index)'` ``. Cell 3 holds the options ("D15's PID-file and `status` design; …"), cell 4 the method ("self, forced by probe rows 6-9 …") and cell 5 the rationale ("`status` during an `init` empties the index (row 6) …"). In GFM, `\|` inside a table cell is unescaped before inline parsing, including inside code spans, so the rendered pattern is `codegraph\.js (init|index)`. This is the same pattern as B:27 and C:53, which are prose, not tables. Backticks on A:720: 32 (even). |

## 2. New findings

None.

## 3. Checks run and results

- **T0b block (A:437-441).** Extracted to a temp file; `bash -n` passes. The single-quoted `rg` patterns contain backticks and braces, and the shell does not interpret them.
- **Pattern matrix.** Built from `sed -n 315p` and `sed -n 325p` of P1. To amend Tier R, "no `env`/`headers`" was replaced with "`env`/`headers` absent or `{}`". To amend Tier K, "`env`/`headers` absent or `{}`;" was inserted after the bold prefix. `cmp` confirmed that both amended copies differ from the originals. The results are in item 1.
- **P1 today.** Both new patterns exit 1. `rg -n 'Tier R \(removed\)|Tier K \(kept'` finds only P1:315 and P1:325.
- **Decisions table pipe scan (A:712-737).** After removing `\|`, all 26 lines (header, separator and 24 rows) have 6 pipes.
- **Whole-file table scan of A.** Rows are compared with the first row of each table after removing `\|`. There are no mismatches. A:205 has an unescaped `|` inside `test("serena-agent|start-mcp-server")`, but it is a list item, not a table row, so the `|` is correct there.
- **D21 cell split.** Shown in item 3.
- **D24 and DF:5.** Parentheses, quotes, backticks and bold markers are counted above. The D24 text was compared with A:205-206 and A:437-440, and the DF:5 credits with D22-D24.
- **Cross-references.** `rg` for the `D22-D24` and `D23-D24` forms, and for `pgrep -f` in A and `handoff/`.

## 4. Self-audit

- **Read in full:** the sixth review report and DF.
- **Read in part:**
  - A:428-447 (T0b), A:203-209 (§2.12 acceptance) and A:708-737 (Decisions);
  - P1:310-329;
  - targeted `rg` lines in A, B and C.
- **Ran:** the commands below, in one private `mktemp -d /tmp/p2-seventh-review.*` directory, which a trap removed (`CLEANUP_OK`):
  - `bash -n` on the T0b block;
  - the 4-file `rg` matrix and the no-backtick variant;
  - the two patterns against P1;
  - pipe counts per row and per table;
  - backtick, parenthesis and quote counts;
  - the D21 cell split;
  - `rg` cross-reference searches.
- **Not done:**
  - no edits except this report;
  - no installs, MCP changes, test suite, commit or push;
  - no history diff, because `.dev/codegraph-migration/` is untracked, so what changed this round is judged from the author's edit list and the sixth review's quotes;
  - the layer-2 script and the `jq` expressions were not re-run, because this round did not edit them.
- **Limits:**
  - When the T0b block is run as one script without `set -e`, it exits 0 on today's P1 (the last line passes because the facts file is absent). The spec's acceptance blocks are checked line by line, and earlier rounds accepted that. This round did not change it, so it is not reported as a finding, under the "do not reopen earlier rounds" instruction.
  - Similarly, A:437 prints "integer expression expected" when `rg -c` finds nothing. It still exits nonzero, as the sixth review recorded.
  - The temp-file amendments are my own wording. A real amendment that puts `{}` without backticks, or on a separate line, would fail the checks. That is the intended strictness.
  - Severity and the GFM reading are my judgment, based on the GFM spec's table-cell escape rule. The table was not rendered on GitHub.
