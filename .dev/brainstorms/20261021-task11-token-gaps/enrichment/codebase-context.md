# Codebase enrichment: Task 11 token-only gaps (quality_tier: primary, direct Read + in-memory mutation probe)

Method: imported the real check functions (`check_at01`..`check_at24`) from `tests/skills/test_auggie_claim_gate_contract.py`, applied each mutation to an in-memory copy of the 7 protocol files, ran every check. No file under src/ or tests/ was touched (`git status` unchanged; 44 tests still pass). Script and raw results: `mutation-probe.py`, `mutation-probe-results.json` in this directory.

## A. The 10 named gaps (+ smaller ones), reproduced

| Mutation | Result |
|---|---|
| G1a "A `protocol_literal` claim that" -> "Any claim that" | SURVIVES |
| G1b swap "(the entrypoint)" / "(the producer)" | SURVIVES |
| G2a "keeps only supported consequences" -> "keeps every consequence" | SURVIVES |
| G2b drop ", and all consequences are listed in excluded_consequences[]" | SURVIVES |
| G2c drop " and every other table condition holds" | SURVIVES |
| G3a SKILL Wave 2 step 5 `failed` -> `partial` | SURVIVES |
| G3b gate "Invariant check" Preflight `failed` -> `partial` | SURVIVES |
| G3c move `invariant_check_unavailable` from failed bullet to partial bullet | SURVIVES |
| G3d/e delete "`allowed-tools` is not a prerequisite check." (SKILL, gate) | SURVIVES |
| G4 agent resp. 5 "Emit ... candidates" -> "Move ... to cross-cutting notes" | SURVIVES |
| G5a "In explicit --diff mode" -> "In every mode" | SURVIVES |
| G5b delete "Only implicit dirty-tree diff mode and snapshot mode use local_read" | SURVIVES |
| G6a "highest-rank" -> "lowest-rank" | SURVIVES |
| G6b "never count votes" -> "count votes" | SURVIVES |
| G6c delete non-defect-group sentence | SURVIVES |
| G7 rubric "not security or data-integrity" inverted | SURVIVES (rubric copy) |
| G7b same inversion in gate Qualification | CAUGHT (check_at24 asserts it) |
| G8a delete "evaluates this table top to bottom ... records matching row ids" | SURVIVES |
| G8b delete "Verified" definition at the table | SURVIVES (same definition also in the file intro, line 5) |
| G9 delete "any row that needs the head object is unproven with head_mismatch_context_unavailable" | SURVIVES |
| G10a SKILL "dropped ..., not downgraded" -> "downgraded to unproven" | SURVIVES |
| G10b delete "never converted to another disposition" (gate) | SURVIVES |
| S2 "The row is then A7" -> A3 | SURVIVES |
| S3 drop runtime_reproduced exception (REQ-016) | SURVIVES (fail-safe direction: stricter) |
| S4 "one entry per applicable row A1 to A5" -> "one entry" | SURVIVES |
| S5 drop "only when a distinct current ref is known" | SURVIVES |
| S6 drop "Snapshot mode records base: null" | SURVIVES |
| S7 "Equal rank gives unproven ..." -> "gives defect" | CAUGHT |

(S1 "For every behavioral claim" mutation text did not match the file wording; the quality-bar sentence is "trace a production entrypoint or prescribing instruction" and was not re-probed.)

## B. Unbounded-target evidence (jq fence excluded; 7 files)

- 467 modal/negation/quantifier flips (not, never, only, every->any, highest->lowest, strictly, must->may, first->last, failed->partial, ...): 378 survive (81%).
- 1,112 sentence/table-row deletions: 900 survive (81%). Survivors by file: SKILL 246, gate 163, handoff 163, rubric 105, prompts 94, command 80, agent 49.
- Caveat: many survivors are examples, handoff phrasing and non-rule prose, so 81% overstates rule-level exposure. It still shows the reviewer standard "mutate any AT-demanded sentence" has no natural stopping point for needle tests: the asserted set is small relative to the sentence set, and an adaptive reviewer always finds survivors.

## C. What else binds the prose (verified from plan/spec/tests)

- jq program (claim-gate.md fence, tested by test_auggie_claim_gate_jq.py, 63 fixture pairs incl. `invalid-j14-qualified-not-capped`, `invalid-j13-*`, `invalid-j06-member-in-dropped`, `valid-merged-nondefect-group`): runs on every real review. A prose edit that makes the orchestrator emit a non-conforming ledger turns into `jq_exit != 0` and status `failed` (fail-closed, loud). It checks structure, not sentence semantics.
- SKILL Wave 3 step 6b (asserted): "A non-zero or missing `jq_exit`, or a missing `candidates.json`, makes the status `failed`." So even if jq-absent were mislabelled `partial`, step 6b cannot reach `jq_exit == 0` without jq.
- Task 12 oracle (not built): `admit()`/`grade()` are test-only reimplementations that read no files (plan Task 12). AT-16 compares the oracle's table (rows, order, fallback dispositions, class rules) with the table extracted from claim-gate.md. AT-17..AT-19 test the oracle, not the prose. No merge/dedupe function is planned in the oracle.
- Task 13: regression run, line-22 byte identity, scope, line-ref grep. Reads no rule prose.
- Spec 0 / 11.3: no semantic effectiveness is claimed; live evaluation is a pre-merge gate needing separate authorization.
- Plan final independent review (sc:implement closes with one) is the only remaining prose-vs-spec read.

## D. Constraint collision found for a golden-snapshot approach

`#### C1. <Short title> (id: <id>)` is in SKILL.md:215 and claim-gate.md:224 (only case-id-like whole words in the protocol files). AT-20 bans case ids in corpus and fixture text under `tests/skills/fixtures/auggie_claim_gate/` (except frozen-tokens.json). A snapshot fixture stored there that includes those two sections would fail the anti-overfit scan; storing it elsewhere violates the AT-22 scope list (source section 2 lists only that fixtures directory). A snapshot must therefore exclude the report-template / tag-grammar sections.
