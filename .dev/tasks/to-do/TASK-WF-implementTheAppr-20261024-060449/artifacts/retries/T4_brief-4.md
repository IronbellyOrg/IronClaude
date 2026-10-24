pick: advice-4-c.md; runner-up: none; reason: critique adviser
## Task 4: Make cache consumption request-specific and align condensed prompts

Acceptance criteria:
T4.AC1: - Matched routing still bypasses cache lookup/write-back. An unmatched hit is only a candidate/template hint: recheck current objective/authority, actual source/dependencies/lifecycle, bind current inputs and reconstruct the handoff. No verbatim cached answer or another request's paths is emitted.
T4.AC2: - Reject incompatible, retired, unavailable or contradictory cached candidates through existing live discovery. Preserve hash, budget and miss protections, guide invalidation and missing-guide/non-checkout/helper-CLI safeguards.
T4.AC3: - Existing classifier keys remain unchanged. Task-file-generation means explicit/justified MDTM rather than generic spec/tasklist planning; raw spec generation, populated-document derivation and roadmap artifact intent remain distinct. Correct misleading spec-panel fixtures without weakening cache mechanics.
T4.AC4: - Cold-worker policy, source/flag verification, net-value scope and current-request binding agree with the main skill. Contract cases T52-T58 and related classification/retirement fixtures cover actual negative behavior of the consumer contract, not a new runtime router.

Steps:
1. In SKILL.md, under the rejection bullet (attempt-3.diff:391), add the indented sub-lines below. Each must start "  - Cached" and must never start with "- If". None may contain the native split marker, `/sc:`, `Run:` or any replacement target, because the section splits at attempt-3.diff:715-719 depend on those markers.
   - "  - Cached comparison hint, current plan-adherence audit: reject; a key match never turns comparison into adherence checking."
   - "  - Cached comparison hint, current local PR review with no posting: reject; never inherit compare inputs or posting authority."
   - "  - Cached PRD-authoring hint, current TDD request: reject; the requested artifact differs."
   - "  - Cached PRD-authoring hint, current existing-spec critique: reject; never rewrite the spec under review."
   - "  - Cached MDTM or roadmap hint, current Sprint artifacts request: reject; never substitute task files for Sprint output."
   - "  - Cached retired-target hint with a valid source hash: reject; lifecycle evidence outranks the hash."
   These sub-lines come from SPEC-sc-recommend-refresh.md:308, 338, 340, 348-352, 721 and 725-729.
2. Add two more sub-lines.
   - Under the binding bullet (attempt-3.diff:390): "  - Cached same-key envelope path, current different path: rebind to current paths only; the cached path never appears."
   - Under the verification bullet (attempt-3.diff:389): "  - Cached source hash, current changed delegated reference that the source names: reread that reference before emission; the hash never proves its freshness."
3. In test_dispatch.py, replace the guard_scope and guards parameters (attempt-3.diff:588, 595-596) with hazard, cached_phrase, current_phrase, verb and section. Keep all eight IDs, their request texts (the T55 request names docs/current.md) and the dispatch-return asserts.
4. Make each hazard real in the fixture's own data. After _seed (attempt-3.diff:493), write that case's source body and set row["source_hash"] to compute_source_hash of that body before upsert. Then check, by hazard:
   - objective: result.candidate equals the cached candidate, and the cached envelope's distinguishing token (--compare, /prd or /task-builder) is not in current_request.
   - path: "docs/previous.md" is in result.recommendation and not in current_request.
   - reference: the source body names backing-reference.md. Rewrite that file after seeding, then assert the hash still matches and the outcome is "hit".
   - retired: the source body contains "deprecated: true", and the outcome is still "hit".
5. For each fixture, in its section (using the split markers at attempt-3.diff:715-719):
   - Exactly one line contains both cached_phrase and current_phrase (case-insensitive).
   - That line contains the fixture's verb.
   - No case sub-line with that verb appears in any other section.
   - The T55 line does not contain "reject".
6. Add one non-parametrized test that uses the same case table. Collect every "  - Cached" sub-line in the hot-path section and build the 8x8 matrix of matches (fixture i's phrase pair against line j). Assert it equals the identity: no orphan lines and no shared lines.
7. Keep the static-only docstring (attempt-3.diff:680-683). Add that no model and no specialist command runs here; actual generation stays in Task 8 (TASK-WF-implementTheAppr-20261024-060449.md:25, 151).
8. Run `uv run pytest tests/recommend tests/skills/test_sc_recommend_routing_contract.py`, plus ruff check and ruff format --check on the touched files. Record the real output in extras-4.log. Expect 81 collected: the 80 at extras-3.log:8 plus the matrix test.

differs-by: Case-specific coverage is checked across all eight cases at once, not one case at a time. An 8x8 matrix compares each fixture's pair of phrases (what the cache holds, what the current request asks) against every case sub-line, and it must be exactly the identity (each fixture matches one line, and only that line). Each action word must also appear only under the bullet that owns it: reject under rejection, rebind under binding, reread under verification. This is not generic word presence, not a list of fixtures checked separately, and not one extra fixture.
