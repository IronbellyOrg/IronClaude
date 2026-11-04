# Round 1 — Variant 3 advocate (refactorer, opus)

## Position summary
Variant 3 alone treats Task 1's tokenizer as a lexer problem: heredocs, comments, line continuation and `$(` inside double quotes are four places where plan line 37's split rule diverges from shell lexing; two violate the Done-when (line 19). V3 missed C-002, where V1 and V2 are right.

## Steelman
- V1: most balanced; finds both checkable blockers (R1-F1, R1-F2) plus unique hygiene defects (R1-F10 tautological live-home assertion at line 92, R1-F7 missing Depends on, R1-F8 template line 965). Grading tokenizer gaps minor is consistent with an advisory fail-open hook. Critique: "minor ceiling" requires documentation; only the heredoc ceiling (line 40) is documented. R1-F5 inverts the Done-when: `x="$(python3 -c ...)"` runs python.
- V2: lean, test-oriented; only card asking for the jq-missing branch to be exercised (R2-F3); C-001 fix pins the new state exactly. Critique: no tokenizer findings; the "only Bash registration is block-bare-python.sh" pin re-breaks on the next Bash hook (test name `..._without_bash_counter`, line 91, shows intent); R2-F5 unverifiable.

## Strengths claimed
1. Coupling: fixing R3-F5 alone makes the heredoc body inside `git commit -m "$(cat <<'EOF' ... EOF)"` scanned line-by-line (line 40), blocking commit/PR bodies with python3 lines; R3-F2 must ship with R3-F5 or F5 is documented and pinned.
2. R3-F5 targets the issue's core misuse (inline JSON parsing via quoted assignment); line 56 blocks only the unquoted form.
3. R3-F4: `uv run --no-project \<nl> python x.py` yields command word `python`; line 19 requires `uv run python` allowed.
4. R3-F3 grounded: read-parse.md lines 6-9 carry trailing `#` comments containing `;` (line 7); `# don't` opens an unclosed quote hiding later lines (undocumented false negative).
5. R3-F6: line 40 rationale vs line 58 `bash -c` allowance contradict.
6. R3-F7: exit 2 only on a positive jq block result makes never-exit-1 hold by construction.
7. Unique: R3-F11 (Task 6/7 mislabel, line 20), R3-F9 (bypassPermissions broader than needed, line 124).
8. R3-F1 fix keeps intent; whole-directory runs catch other hooks.json readers (tests/hooks/test_auggie_flag_clear_mcp_prefix.py:22, tests/unit/test_ccsession_tag.py:3145).

## Weaknesses identified in others
1. V1 R1-F5 misreads the Done-when for `$(` in quotes.
2. V1 and V2 accept line 40 without checking apostrophe desync (false negatives).
3. V2 R2-F1 fix brittle.
4. V2 has no lexical-rule coverage.
5. R1-F11 / R3-F8 flakiness weak: repo asserts elapsed < 1 at test_freshness_subagent_start_policy.py:86.
6. R2-F5 unverifiable.

## Concessions
1. Missed C-002 (line 58 allowed list has only && and |; line 64 unmeetable).
2. Missed C-009, C-013, C-014, C-018.
3. R3-F3 vs R3-F10 inconsistency: the `(` false positive is minor; F3 stays blocking only for the apostrophe-in-comment desync.
4. R3-F1 fix should also run tests/unit.
5. R3-F5 alone regresses; pair with R3-F2 or document-and-pin.
6. R3-F8 flakiness overstated; keep the jq guard.
7. Citation grounding was V3's weakest dimension.

## Per-point positions
| Point | Superior | Reason |
|---|---|---|
| C-001 | V3 (+tests/unit) | intent-preserving narrowing; directory runs |
| C-002 | V1 | multiple allowed ; cases |
| C-003 | V3 | apostrophe desync + coupling |
| C-004 | V3 | unique, grounded in read-parse.md 6-9 |
| C-005 | V3 | breaks required allowed form |
| C-006 | V3 | core misuse; handle or pin |
| C-007 | V3 (slight) | line 40 vs 58 contradiction |
| C-008 | V3 + V2 | construction + test |
| C-009 | V1 | template 965 evidence |
| C-010 | Equivalent | precedent weakens |
| C-011 | V3 | unique |
| C-012 | V1 | scope expansion |
| C-013 | V1 | tautological assertion |
| C-014 | V1 | missing Depends on |
| C-015 | V3 | mislabel |
| C-016 | V3 | unique, minor |
| C-017 | V2 | unverifiable, low |
| C-018 | V1 | refinement classification |
| X-001 | V3 | blocking spec gap |
| X-002 | V3 | "runs bare python" governs |
| X-003 | V3 (qualified) | text FP documented; apostrophe FN not |

## Shared assumptions
- A-001: QUALIFY — in scope (Task 3 necessarily breaks it; test name shows intent); record as Necessary deviation in the PR body.
- A-002: REJECT — plan will not be edited; fixes are implement-time obligations under /sc:implement.
- A-003: QUALIFY — comment strip, continuation join, quoted-delimiter heredoc detection fit as pre-passes; `$(` nesting in double quotes needs a stateful scanner (awk allowed by line 41; unmeasured); else document-and-pin.
