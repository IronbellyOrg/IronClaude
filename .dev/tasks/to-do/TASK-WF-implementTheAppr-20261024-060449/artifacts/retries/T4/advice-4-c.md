# Adviser ladder entry: opus

outcome: ready
| AC | why earlier attempts missed it (path:line) | change |
|---|---|---|
| T4.AC1 | Not missed. The reviewer marked it met (review-3.md:5-11). The hint-only bullets are at attempt-3.diff:388-390 and the matched-row bypass is at attempt-3.diff:396. | Keep the text at attempt-3.diff:375-396. Only add indented sub-lines under the verification bullet (attempt-3.diff:389) and the binding bullet (attempt-3.diff:390). Every substring pinned at attempt-3.diff:761-772 stays. |
| T4.AC2 | Not missed. The reviewer marked it met (review-3.md:14-20), based on attempt-3.diff:391, 393, 405. | Keep the bullets at attempt-3.diff:391 and 393 word for word. Add the reject sub-lines under 391, before the native bullet (attempt-3.diff:392). The rejection pins at attempt-3.diff:775-787 stay as they are. No edits to dispatch, cache or schema code (SPEC-sc-recommend-refresh.md:344). |
| T4.AC3 | Not missed. The reviewer marked it met (review-3.md:23-29). | Keep attempt-3.diff:5-366, 433-478 and 816-840 byte-for-byte. |
| T4.AC4 | 1. The production text named no case. Its consumer bullets cover only general categories (attempt-3.diff:389-391), so there was no case-specific sentence a test could pin. 2. All eight fixtures check generic words (attempt-3.diff:596, 605, 614, 623, 632, 642-643, 653-654, 665) taken from those shared bullets, so any two cases can swap without a failure. 3. current_request is used only in failure messages and one phrase branch (attempt-3.diff:698, 727, 734). 4. The "changed reference" is a temp file that the hashed source never names (attempt-3.diff:686-688, 698-699). 5. The data checks end at what dispatch returns (attempt-3.diff:707-709). The reviewer states this at review-3.md:37 and 50. | 1. Add one negative sub-line per case, under the bullet that owns its required action (reject, rebind or reread). 2. Give each fixture a real hazard in its own data that dispatch cannot see. 3. Add one cross-case matrix test, so swapping, merging or deleting any case line fails. |

differs-by: Case-specific coverage is checked across all eight cases at once, not one case at a time. An 8x8 matrix compares each fixture's pair of phrases (what the cache holds, what the current request asks) against every case sub-line, and it must be exactly the identity (each fixture matches one line, and only that line). Each action word must also appear only under the bullet that owns it: reject under rejection, rebind under binding, reread under verification. This is not generic word presence, not a list of fixtures checked separately, and not one extra fixture.

steps:
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
