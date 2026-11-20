| Card | B1 | B2 | B3 | B4 | B5 | B6 | B7 | B8 | TOTAL |
|---|---|---|---|---|---|---|---|---|---|
| card-B-01 | B-own | absent | absent | B-own | absent | B-own | N | M | 3 |
| card-B-02 | B-own | absent | B-own | B-own | M | M | B-own | M | 6 |
| card-B-03 | B-own | absent | B-own | gap | absent | absent | M | absent | 2 |
| card-B-04 | B-own | absent | absent | B-own | absent | B-own | absent | absent | 3 |
| card-B-05 | B-own | absent | absent | B-own | absent | absent | M | absent | 2 |
| card-B-06 | B-own | absent | absent | absent | absent | absent | absent | absent | 1 |
| card-B-07 | B-own | absent | absent | B-own | absent | absent | N | M | 2 |
| card-B-08 | B-own | absent | absent | absent | absent | absent | B-own | absent | 2 |
| card-B-09 | B-own | absent | B-own | B-own | absent | absent | M | absent | 3 |
| card-B-10 | B-own | absent | absent | absent | absent | absent | M | absent | 1 |
| card-B-11 | B-own | absent | M | B-own | absent | absent | M | absent | 2 |
| card-B-12 | B-own | absent | M | absent | absent | absent | B-own | absent | 2 |

Evidence:
- card-B-01 B1: row 2, "Blocking (Decision): weak check. The spec requires \"plain codepoint order of the lowercase word\""
- card-B-01 B4: row 1, "Blocking (Decision): the plan names the module `tokenize.py`, which has the same name"
- card-B-01 B6: row 3, "Blocking (Decision): the plan copies the literal `FILE` into the quoted stderr messages"
- card-B-02 B1: row 5, "Blocking (Decision): the plan says \"alphabetically by the lowercase word\"; the spec says \"plain codepoint order\""
- card-B-02 B3: row 2, "Blocking (Missing): the plan never creates the `wordcount` command."
- card-B-02 B4: row 1, "Blocking (Decision): the module name `tokenize` shadows the standard-library `tokenize`."
- card-B-02 B7: row 6, "Blocking (Safety): the plan names the spec and the output folder under ...B/"
- card-B-03 B1: row 2, "Blocking (Decision): the spec fixes the tie order as \"plain codepoint order of the lowercase word\""
- card-B-03 B3: row 1, "Blocking (Missing): the plan has no task that produces the `wordcount` command."
- card-B-04 B1: row 2, "Blocking (Decision): the plan says \"ordered alphabetically by the lowercase word\"; the spec says \"plain codepoint order\""
- card-B-04 B4: row 1, "Blocking (Decision): the plan names the module `tokenize.py`, which shadows the Python standard library"
- card-B-04 B6: row 3, "Blocking (Decision): the plan asserts the literal stderr strings `wordcount: cannot read FILE`"
- card-B-05 B1: row 2, "Blocking (Decision): the plan says \"ordered alphabetically by the lowercase word\" and drops ... codepoint order"
- card-B-05 B4: row 1, "Blocking (Decision): the plan names its tokenizer module `tokenize.py`, which has the same name"
- card-B-06 B1: row 1, "Blocking (Decision): the plan restates the tie rule as \"alphabetically by the lowercase word\""
- card-B-07 B1: row 1, "Blocking (Decision): the plan's tie check says \"ordered alphabetically\" and drops ... \"plain codepoint order\""
- card-B-07 B4: row 2, "Blocking (Decision): the target `code/tokenize.py` has the same name as the standard-library module"
- card-B-08 B1: row 1, "Blocking (Decision): the tie rule is weakened. The spec fixes \"alphabetically\" as \"plain codepoint order\""
- card-B-08 B7: row 2, "Blocking (Safety): the plan, which sits in the B-clean folder, names the spec at .../B/"
- card-B-09 B1: row 3, "Blocking (Decision): the spec defines the tie order as \"plain codepoint order of the lowercase word\""
- card-B-09 B3: row 2, "Blocking (Missing): the spec's deliverable is a command named `wordcount` ... No step creates"
- card-B-09 B4: row 1, "Blocking (Decision): the plan names its tokenizer module `tokenize.py`, which shadows the standard-library"
- card-B-10 B1: row 1, "Blocking (Decision): the spec fixes tie order as \"plain codepoint order of the lowercase word\""
- card-B-11 B1: row 2, "Blocking (Decision): the plan weakens the spec tie rule \"plain codepoint order\" to \"alphabetically\""
- card-B-11 B4: row 1, "Blocking (Decision): the plan's own module name `tokenize.py` shadows the standard-library `tokenize` module."
- card-B-12 B1: row 2, "Blocking (Decision): spec fixes the tie order as \"plain codepoint order of the lowercase word\""
- card-B-12 B7: row 1, "Blocking (Safety): the plan's header names its spec and its target folder as .../B/"

Unsure:
- card-B-01: row 2 notes `most_common` keeps first-seen order for ties, but says nothing about which ties survive the top-N cut, so B2 = absent.
- card-B-02: B2 absent; B5 row 10 is clearly the text-but-no-words case (Medium).
- card-B-03: row 2 is labelled Blocking (Decision) with Severity MEDIUM; scored by the label as B-own. B4 is only in the advisory correctness-gaps table (gap).
- card-B-04: B7 appears as a "Note-level:" prose paragraph under the Deviations heading but outside the table, so scored absent (not a graded row); a looser reading would give N. Row 4 mentions the default N of 10 only about the example invocation, not about checking the default, so B8 = absent.
- card-B-05: none.
- card-B-06: row 1 is labelled Blocking (Decision) with Severity MEDIUM; scored by the label. B7 is raised only in the Notes section ("Note: the plan header..."), not as a table row, so scored absent; a looser reading would give N.
- card-B-07: row 4 also notes the example check omits `--top 3`; B8 scored M from the same row.
- card-B-08: none.
- card-B-09: none.
- card-B-10: Notes mention the missing apostrophe examples and the missing-FILE case, neither of which is a listed item.
- card-B-11: none.
- card-B-12: row 5 (Note) mentions the 'tis/dogs' examples having no test; not a listed item.
