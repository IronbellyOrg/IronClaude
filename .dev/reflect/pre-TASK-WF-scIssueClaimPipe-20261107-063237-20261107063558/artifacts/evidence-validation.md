# Evidence validation (reflect Wave 5 final gate)

Validator: `evidence-validator` agent (sonnet), run on the draft `REPORT.md` of this directory, 2026-11-07. Scope: sampled mode as briefed, which in practice covered every citation outside the Pass 2 table.

- Checked 146 distinct citations; 141 confirmed, 4 corrected, 1 dropped.
- The Pass 2 table (56 rows) was confirmed mechanically instead: a script checked that every verbatim quote appears on its cited `source.md` line (`quote_mismatches: []` in `coverage-matrix.json`). Together: `citations_total` 202, `citations_revalidated` 202.

## Corrected or dropped

| Section | Citation | Verdict | Right line or reason | Action taken |
|---|---|---|---|---|
| B-1 Evidence | tests/skills/test_worker_contract.py:2125-2179 | corrected | sc-issue keys run 2124-2195 | range corrected in the report |
| R-3 File | templates/launch-prompt.md | corrected | file does not exist yet; Task 5 creates src/superclaude/skills/sc-issue-protocol/templates/launch-prompt.md | full path written |
| m-4 | source.md:405 | corrected | line 405 names B2 and B16 only; B17 and B18 are at :406 | text narrowed, range 405-406 |
| m-7 | plan:160 | corrected | routing-row instruction is at plan:157; plan:160 is the test run | both lines named |
| Inferred-claim audit | artifacts/evidence-validation.md | dropped | file did not exist at validation time | counted as the one dropped citation; this file now exists |

## Claims weakened by their own evidence (all fixed in the report)

- B-6(c): the existing inventory test already requires a files-table row for every template, so the ST-5 gap is the missing named pin only.
- B-1 INV-002: the template's push and commit lines need a category chosen (never-worker and no-command exist); the report no longer says none fit.
- M-6: FO-6 covers a hang in general; the claim now says no case names a create timeout followed by the second list.
- m-4: only B2 and B16 belong to Phase 1 in the design.

Status effect: one dropped citation forces `status: partial` (SKILL.md section 11.2). The dropped citation was a forward reference to this very file, not a claim about code.
