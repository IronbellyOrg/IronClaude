| Card | E1 | E2 | E3 | E4 | E5 | E6 | E7 | E8 | TOTAL |
|---|---|---|---|---|---|---|---|---|---|
| card-E-01 | B-own | B-own | B-own | B-own | B-own | B-own | B-own | absent | 7 |
| card-E-02 | B-own | B-own | B-own | B-own | B-own | B-own | B-own | absent | 7 |
| card-E-03 | B-own | B-own | B-own | B-folded | absent | B-folded | N | B-own | 5 |
| card-E-04 | B-own | B-own | M | B-own | B-own | B-own | absent | absent | 5 |
| card-E-05 | B-own | B-own | B-own | M | M | B-folded | M | absent | 3 |
| card-E-06 | B-own | B-own | B-own | M | M | B-folded | M | B-own | 4 |
| card-E-07 | B-own | B-own | B-own | B-own | B-own | B-folded | absent | B-own | 5 |
| card-E-08 | B-own | B-own | B-own | M | M | B-folded | N | B-own | 4 |
| card-E-09 | B-own | M | B-own | M | M | B-folded | M | B-own | 3 |
| card-E-10 | B-own | B-own | B-own | B-folded | N | B-folded | B-folded | absent | 4 |
| card-E-11 | B-own | B-own | B-own | M | absent | M | N | M | 3 |
| card-E-12 | B-own | B-own | B-own | M | M | M | M | absent | 3 |

Evidence:
- E-01 E1 row 3: "the error line prefix and the success exit code are missing from the plan"
- E-01 E2 row 5: "\"no output written\" for an unreadable input is dropped"
- E-01 E3 row 1: "no task writes the JSON output"
- E-01 E4 row 6: "\"blank lines between rows are skipped\" has no check"
- E-01 E5 row 7: "the spec does not say how `<n>` is counted"
- E-01 E6 row 4: "weak check on \"rows already written stay written\""
- E-01 E7 row 2: "weak check on key order. SPEC:9 says keys are in file order"
- E-02 E1 row 3: "the plan never mentions the `csv2jsonl: ` stderr prefix"
- E-02 E2 row 7: "\"no output written\" for the unreadable-input case is not checked"
- E-02 E3 row 1: "no task builds the output writer"
- E-02 E4 row 6: "no plan check covers blank lines between rows"
- E-02 E5 row 4: "the wrong-field-count message `row <n> has <k> fields, expected <m>` leaves `n` undefined"
- E-02 E6 row 5: "no check asserts that rows already written stay written"
- E-02 E7 row 2: "key order is not stated in the plan and no check pins it"
- E-03 E1 row 3: "never states the `csv2jsonl: ` prefix"
- E-03 E2 row 4: "the \"no output written\" rule for an unreadable input is absent"
- E-03 E3 row 1: "no task owns the JSON-lines writer"
- E-03 E4 row 5: "Missing tests: blank-line skipping (T2 claims it at PLAN:15)"
- E-03 E6 row 5: "Missing tests: ... rows already written stay written, exit 0 on success"
- E-03 E8 row 2: "the hand-off between T2 (`convert.py`) and T3 (`csv2jsonl.py`) is undefined"
- E-04 E1 row 1: "weak check on the error prefix"
- E-04 E2 row 2: "no check for \"no output written\" on an unreadable input"
- E-04 E4 row 4: "no check at all on blank lines"
- E-04 E5 row 5: "the row number `<n>` in `row <n> has <k> fields, expected <m>` is undefined"
- E-04 E6 row 3: "weak check on \"rows already written stay written\""
- E-05 E1 row 2: "the required error format `csv2jsonl: <message>` is not carried into the plan"
- E-05 E2 row 3: "the \"no output written\" rule for an unreadable or missing input is absent"
- E-05 E3 row 1: "no task serializes rows to output"
- E-05 E6 row 1: "written incrementally so earlier rows survive a later error ... \"rows already written stay written\""
- E-06 E1 row 2: "never states the required `csv2jsonl: ` prefix"
- E-06 E2 row 3: "the \"no output written\" rule for unreadable input is absent from the plan"
- E-06 E3 row 1: "no task builds the JSON Lines writer"
- E-06 E6 row 4: "If `convert.py` returns a list ... a bad row 3 writes nothing"
- E-06 E8 row 4: "the T2/T3 interface is undefined"
- E-07 E1 row 3: "the plan never states the `csv2jsonl: ` prefix (SPEC:14)"
- E-07 E2 row 4: "SPEC:22 requires \"no output written\" for unreadable input. The check only tests"
- E-07 E3 row 1: "no task owns turning a row dict into the output line"
- E-07 E4 row 5: "(a) Blank lines between rows are skipped (SPEC:19) ... no blank-line test"
- E-07 E5 row 5: "(b) The `row <n>` in the field-count message (SPEC:25) does not say"
- E-07 E6 row 2: "Rows \"already written stay written\" (SPEC:25) needs row-by-row streaming"
- E-07 E8 row 2: "the error-handling hand-off between T2 (`convert.py`) and T3 (`csv2jsonl.py`) is not defined"
- E-08 E1 row 2: "the `csv2jsonl: ` prefix is not stated"
- E-08 E2 row 3: "the \"no output written\" rule for unreadable input is absent"
- E-08 E3 row 1: "no task builds the JSON line writer"
- E-08 E6 row 4: "no acceptance check in T3 or T4 exercises \"earlier rows persist\""
- E-08 E8 row 4: "T2 and T3 are in different modules ... interface between them is not defined"
- E-09 E1 row 3: "never states the required `csv2jsonl: ` prefix"
- E-09 E3 row 1: "no task owns turning rows into output lines"
- E-09 E6 row 2: "the \"rows already written stay written\" behaviour depends on it"
- E-09 E8 row 2: "the T2/T3 interface is undefined"
- E-10 E1 row 2: "the `csv2jsonl: ` stderr prefix and the success exit code 0 are not stated"
- E-10 E2 row 3: "\"no output written\" for a missing or unreadable input is dropped"
- E-10 E3 row 1: "no task writes the output"
- E-10 E4 row 4: "T4 ... has no check for several stated behaviours: blank lines skipped (SPEC:19)"
- E-10 E6 row 1: "the \"rows already written stay written\" behaviour also depends on rows being written one at a time"
- E-10 E7 row 4: "no check for several stated behaviours: ... header-order keys (SPEC:9)"
- E-11 E1 row 2: "the error format `csv2jsonl: <message>` is not stated"
- E-11 E2 row 3: "the \"no output written\" rule for an unreadable input is absent"
- E-11 E3 row 1: "no task serializes rows to output"
- E-12 E1 row 2: "the plan never requires the `csv2jsonl: ` prefix on error messages"
- E-12 E2 row 3: "the \"no output written\" rule for an unreadable input is not in the plan"
- E-12 E3 row 1: "no task builds the JSON writer"

Uncertain:
- card-E-01: none material; row 1 also mentions T1 "the writer" but not the T2/T3 hand-off, so E8 scored absent.
- card-E-02: none material.
- card-E-03: E5 appears only in Notes ("not graded"), scored absent; E6 named both in row 2 (hand-off) and row 5 (missing tests), scored B-folded.
- card-E-04: E7 not raised; row 7 wrongly claims the example check pins key order, scored absent.
- card-E-05: E6 B-folded rests on row 1 naming "rows already written stay written" as an affected action of the missing writer, not as a missing check; could be read as absent.
- card-E-06: E7 scored M from row 8 ("Header file order ... is not stated either"), which is about statement rather than a check.
- card-E-07: row 5 has two co-equal subjects (blank lines and row number); both E4 and E5 scored B-own.
- card-E-08: E7 scored N from row 9 ("in file order ... not stated"), framed as valid reading, not a missing check.
- card-E-09: E2 scored M because "no output written" appears only inside the Medium T4 test-gap row 5.
- card-E-10: E6 B-folded rests on row 1 framing (writer must stream), similar to card-E-05; E5 scored N from row 6.
- card-E-11: E5 only in Notes ("not graded"), scored absent; E8 scored M from row 4 ("splits reading (convert.py) from writing/errors (csv2jsonl.py)").
- card-E-12: E8 scored absent; row 4 says "T2 describes conversion with no streaming contract" but does not name the T2/T3 hand-off.
