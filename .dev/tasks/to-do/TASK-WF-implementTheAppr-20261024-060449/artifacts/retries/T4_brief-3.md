pick: advice-3.md; runner-up: none; reason: single adviser
## Task 4: Make cache consumption request-specific and align condensed prompts

Acceptance criteria:
T4.AC1: - Matched routing still bypasses cache lookup/write-back. An unmatched hit is only a candidate/template hint: recheck current objective/authority, actual source/dependencies/lifecycle, bind current inputs and reconstruct the handoff. No verbatim cached answer or another request's paths is emitted.
T4.AC2: - Reject incompatible, retired, unavailable or contradictory cached candidates through existing live discovery. Preserve hash, budget and miss protections, guide invalidation and missing-guide/non-checkout/helper-CLI safeguards.
T4.AC3: - Existing classifier keys remain unchanged. Task-file-generation means explicit/justified MDTM rather than generic spec/tasklist planning; raw spec generation, populated-document derivation and roadmap artifact intent remain distinct. Correct misleading spec-panel fixtures without weakening cache mechanics.
T4.AC4: - Cold-worker policy, source/flag verification, net-value scope and current-request binding agree with the main skill. Contract cases T52-T58 and related classification/retirement fixtures cover actual negative behavior of the consumer contract, not a new runtime router.

Steps:
1. Keep every non-test hunk from `attempt-2.diff` byte-for-byte: lines 1-366, 367-431 and 433-478, plus the routing-contract tests at 726-848. If the work is reverted to Q0 first, reapply them unchanged. Do not change the dispatch code, the cache code or the schema.
2. Reapply the `test_dispatch.py` hunk (`attempt-2.diff:479-725`) unchanged.
3. Directly after the `T53-PRD-authoring-is-not-TDD` param, add one `pytest.param` with:
   - request: "Critique the existing spec docs/specs/current-spec.md without rewriting it"
   - key: `"spec-generation"`
   - candidate: `"/prd"`
   - envelope: `"Run: /prd docs/raw.md"`
   - scope: `"verification"`
   - guards: `("objective", "artifact", "authority ceiling")`
   - id: `"T53-PRD-authoring-is-not-existing-spec-critique"`

   All three guard terms appear in the verification section (`attempt-2.diff:389`). The request text must not contain "changed backing references", because the test branches on that phrase (`attempt-2.diff:689`).
4. Leave the T55 path-binding fixture unchanged, and do not count it as T53 coverage.
5. Keep the static-only docstring (`attempt-2.diff:671-675`). Do not claim the fixtures run model behavior.
6. Run `uv run pytest tests/recommend tests/skills/test_sc_recommend_routing_contract.py`, then `ruff check` and `ruff format --check` on the four touched files. Record the real output in `extras-3.log`. Expect 80 tests collected, one more than `extras-2.log:8`.
7. In `approach-3.md`, map T53 to both fixture IDs and T55 to the path-binding fixture.

differs-by: Treat T53 as two separate required test cases that seed the same `spec-generation` + `/prd` row, one for the TDD request and one for the existing-spec critique.
