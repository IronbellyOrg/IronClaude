pick: advice-3.md; runner-up: none; reason: single adviser
## Task 6: Encode every specified contract and specialist regression case

Acceptance criteria:
T6.AC1: - Map each of the approved T01-T76 checks to a real focused assertion or a clearly identified behavioral-evaluation requirement. Every S01-S29 fixture has a concrete request, environment, expected target/mode/input retention, negative competitor and side-effect boundary.
T6.AC2: - Specialist fixtures include unavailable-plugin and seeded-wrong-cache variants. In particular cleanup-audit, cliEval create/run, release split/no-split/proposal continuation, swarm settings and tier-validation missing-suite cases have direct selection expectations, not unrelated IDs.
T6.AC3: - Fixtures never execute recommended commands, authenticate or make external changes. Static text/schema/cache tests are labeled static and do not pretend to demonstrate model generation.
T6.AC4: - The 47-command coverage/dispositions remain traceable; four retirements and formatting-only histories are preserved. No prior research check is silently rewritten as runtime success, and original research evidence is retained.
T6.AC5: - All affected static regression tests run, with outcomes recorded under ./artifacts/. Failures are repaired within approved scope rather than weakened, skipped or hidden.

Steps:
1. In the fixture, rewrite only the five seeded_wrong_cache.expected strings for S23-S27 (attempt-2.diff:580, 602, 624, 646, 666) to the "consulted then rejected" outcome above. Keep cache_row, key and candidate as they are; they already pass the key, primitive and non-target checks (attempt-2.diff:1126-1131). Optionally add a shared environment note so "rejected" names the live-discovery fallback. Do not add classifier keys or schema (plan:22; SKILL.md:90).
2. In test_variants_name_real_primitives_and_wrong_cache_rows (attempt-2.diff:1113-1134), replace the comment and the assertion at :1132-1133 with a branch on case["guide_route"]["block"]. For "routing", require "cache not consulted". For "other", require "consulted", "rejected" and "no hit telemetry", and require that "cache not consulted" is absent. Keep the shared "never emitted" assertion at :1134 for both branches.
3. Split test_matched_routes_bypass_cache_so_seeded_rows_cannot_win (attempt-2.diff:1137-1141) into two static checks. Keep the Step 0 skip phrase (SKILL.md:62). Add a check that the Other-commands bullet limits itself to no_match (SKILL.md:54), and that the hot-path section holds both the hint-only and the reject-to-live-discovery wording (SKILL.md:67, 90). Assert short stable phrases, not whole sentences.
4. Add a guard test: every case whose guide_route.block is "other" has an expectation that does not claim the cache was bypassed, and every "routing" case does. This stops the uniform wording from coming back.
5. Replace the substring check at attempt-2.diff:1056 with the anchored conditional-guard regex described in the T6.AC1 row. Keep absent_from_route semantics (attempt-2.diff:1047) and the repeat-clash logic (:1041-1045) unchanged.
6. Make no product, guide, SKILL or mirror edits. Rerun the Task 6 test files and the parity tests with uv, record the log under artifacts/, and report the Task 7 parity failures honestly (extras-2.log:30-31).

differs-by: the seeded-wrong-cache expectation and its assertion now depend on which guide block the case routes through (matched routing row = cache bypassed; Other-commands no_match = hint consulted then rejected), and each branch is checked against its own SKILL.md clause instead of one uniform "cache not consulted" claim.
