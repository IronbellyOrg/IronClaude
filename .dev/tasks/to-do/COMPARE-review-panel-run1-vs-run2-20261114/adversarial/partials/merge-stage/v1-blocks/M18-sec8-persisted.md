<!-- Source: Variant 1, Section 8 (lines 3830, 3861, 3880, 3898) — merged per Change #M-18; ids prefixed R1- -->
### 8.6 Run 1 persisted-format compatibility and rollback rules

Run 1's persisted-format and rollback rules from its four track introductions (V1:3830 for R1-M1, V1:3861 for R1-M2, V1:3880 for R1-M3, V1:3898 for R1-M4); they are carried only here, not in 8.4. <!-- Source: new (lead per Change #M-18) -->

**Persisted formats and rollback (applies to every R1-M1 step; [proposed] rule, not in code).** Each persisted format keeps its schema string until a deliberate bump (`review-ledger/1`, `review-panel-manifest/1`, `review-telemetry/1`): new keys are optional; files written before the step are read without migration; `validate` and `load` accept both the old and the new form; and the step's tests re-validate recorded artifacts (the step rows name them). Rollback: each step is one change that can be reverted alone; a revert leaves files that hold the new optional keys, so every step that adds a persisted key also adds a test that the previous reader tolerates unknown keys (whether it does today is [UNVERIFIED] for `ledger.load` and `manifest.load` until that test exists). The track-level rollback line is: revert in reverse dependency order, run R1-G1 to R1-G11 and R1-G-exit, and confirm the 13 recorded shadow manifests still validate.

**Rollback (R1-M2; [proposed] rule).** Contract 1.8.0 stays byte-identical in every R1-M2 step except the R1-M2-10 bump gate, so reverting a step leaves recorded shadow runs and their contracts valid; after a revert run R1-G8 and R1-G-exit (the recorded shadow runs must still count 13 of 20 with the same failures); an edit to `SKILL.md` outside the R1-C6 allowed sections is reverted together with its R1-C6 allowed-list change.

**Rollback (R1-M3; [proposed] rule).** R1-M3-03 to R1-M3-06 change the post-gate engine only and keep its CLI line, exit codes, output files and the `reflect_post:` block, so a revert restores today's behaviour (the blocking gate cannot HALT, R1-ENS-1) and R1-G9 must stay green; R1-M3-01, R1-M3-02, R1-M3-08 and R1-M3-09 are text and test edits whose pins are in R1-G10, R1-G11 and R1-G-skills and whose plugin copies are reverted with them.

**Rollback (R1-M4; [proposed] rule).** Adding a lens entry or a thin module is additive, so a revert removes the entry and its tests; the router change of R1-M4-03 is reverted together with its R1-G-pr test changes; the rf-qa pins moved by R1-M4-06 are restored with the files they cover (R1-G10).

**Correction (R25-INV-003).** "Keep the schema string and add optional keys" is safe only for additive changes. V2's adopted ledger design changes clearing and verdict semantics, which run 1's own debate (R1-C13-22 R1-INV-014, V1:2657) closed with a `min_writer` field and a `review-ledger/2` bump; an old installed binary would clear rows by silence on a new ledger and raise `KeyError` on `last["verdict"]` (`ledger.py:363-372`). This is an open decision with both versions: <!-- Source: new (correction per Change #M-18, R25-INV-003) -->

- V2 (A-9): keep `review-ledger/1`. <!-- Source: new (M-18) -->
- Run 1 (R1-C13-22 R1-INV-014, V1:2657): a `min_writer` field plus the `review-ledger/2` bump. <!-- Source: new (M-18) -->
