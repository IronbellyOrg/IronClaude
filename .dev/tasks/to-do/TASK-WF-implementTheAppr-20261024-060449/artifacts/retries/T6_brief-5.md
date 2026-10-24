pick: refactor of advice-4-a.md; runner-up: none; reason: escalation 3
## Task 6: Encode every specified contract and specialist regression case

Acceptance criteria:
T6.AC1: - Map each of the approved T01-T76 checks to a real focused assertion or a clearly identified behavioral-evaluation requirement. Every S01-S29 fixture has a concrete request, environment, expected target/mode/input retention, negative competitor and side-effect boundary.
T6.AC2: - Specialist fixtures include unavailable-plugin and seeded-wrong-cache variants. In particular cleanup-audit, cliEval create/run, release split/no-split/proposal continuation, swarm settings and tier-validation missing-suite cases have direct selection expectations, not unrelated IDs.
T6.AC3: - Fixtures never execute recommended commands, authenticate or make external changes. Static text/schema/cache tests are labeled static and do not pretend to demonstrate model generation.
T6.AC4: - The 47-command coverage/dispositions remain traceable; four retirements and formatting-only histories are preserved. No prior research check is silently rewritten as runtime success, and original research evidence is retained.
T6.AC5: - All affected static regression tests run, with outcomes recorded under ./artifacts/. Failures are repaired within approved scope rather than weakened, skipped or hidden.

Steps:
1. Start from the attempt-4 checkpoint tree (89f3281647abcb763b2ea80aa30ecbf43a2d6f18) after the registered revert. Keep the A4 steps the review shows worked: the two-outcome (hit on the seeded key / no_key miss) seeded-wrong-cache wording and its key-bound helper for S23-S27 (review-4.md:20, attempt-4.diff hunks for those cases), S28 `--level basic`, the enumerated flag-value check and its negative self-checks (review-4.md:56), and everything AC3-AC5 rely on (review-4.md:29, 38, 47).
2. From advice-4-a.md step 1-3, replace the whole-file flag search with a `_declared(source)` helper that reads only the `## Usage` block, the `argument-hint:` front matter and option-table rows, never Examples; flag names and any enumerated values must be declared there. Add a self-check that `("improve", "--preview")` fails (example-only) and `("explain", "--level basic")` passes.
3. Route consistency, the systematic fix for the S24 defect (review-4.md:11, 53): add a check that any primary case or repeat whose guide_route block is "other" names a command that no routing-table row names in its steps (SKILL.md:54 allows Other commands only on no_match). Then move the S24 coordinated-documentation repeat to `{"block": "routing", "row": "document-built"}` with its 1b phrase, so its matched-row cache rule applies, and fix any other case the new check flags. Do not edit the guide.
4. Release-split continuation (review-4.md:54): the S12 `--resume-from` repeat must retain the required `<spec-file-path>` positional (release-split.md:52). Put the release spec fixture path in its retained inputs and expect a clarification question when no spec path is given. Add a per-repeat check that the positional arguments a target's option table marks Required appear in that repeat's retained inputs or expected clarification.
5. Mandatory row flags (review-4.md:55): add a `mandatory_flags` list to routing cases whose row has a non-empty mandatory_flags cell and whose expected steps include those labels (S18, S19 and any other the check finds). Assert each listed entry equals the guide row's cell entry for that step label (HOW-WE-WORK.md:356 for full-spec: step 3 `--mode critique --focus requirements`, step 5 `--mode critique --focus architecture,testing`).
6. Keep the T01-T76 map, Appendix C rows, retirements and Task 8 markers unchanged unless a new test function name must be added to an existing check's static list.
7. Rerun the Task 6 test files, the parity and core tests, ruff check, ruff format --check and the fixture JSON load with uv; record the log under ./artifacts/. Only the 4 Task 7 parity failures may remain.

lessons from A4:
- review-4.md:11 and review-4.md:53: a repeat was recorded on the Other-commands block although a routing row names its command; route membership was never checked systematically.
- review-4.md:54: the S12 continuation repeat dropped a Required positional (the release spec path), and no test checked required positionals.
- review-4.md:55: S18/S19 omitted the full-spec row's mandatory spec-panel flags, and no test compared cases with the guide's mandatory_flags column.

differs-by: Fixture expectations are checked for consistency against three guide/command structures they previously ignored: routing-row membership (an Other-commands route is valid only when no row names the command), Required positional arguments, and the routing table's mandatory_flags column, using a Usage-only declared-source parser instead of whole-file search.
