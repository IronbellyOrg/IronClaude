# Candidate Fixes — Tier 2 Distillation

All three cards converge on the same diagnosis (the `output_dir=output_dir` self-reference at `commands.py:1476`) but two distinct *fix mechanisms* emerge:

| ID | Description | Supporting agents | Confidence (avg) | Verdict |
|----|-------------|-------------------|------------------|---------|
| **FIX-A** | Remove the `output_dir=output_dir` kwarg from the line-1473 call. Mirror doctor's call shape. | security-engineer (primary), root-cause-analyst (primary), quality-engineer (primary) | 0.93 | **consensus** on the mechanism, but FIX-B is in tension on the API hygiene question |
| **FIX-B** | Remove the `output_dir` kwarg from `resolve_scratch_root` entirely; rely on the existing `runtime_config` pattern at commands.py:1490-1499 for legitimate "extend allowlist for sub-paths" cases. | root-cause-analyst (deferred), quality-engineer (sympathetic, not primary) | 0.75 (lower because no agent picked it as primary) | **competing** in API-design sense, but no agent recommended it as the immediate fix |

**Quick verdict**: All three primary fixes are FIX-A. FIX-B is named as a follow-up refactor (root-cause-analyst's "alternate worth considering") rather than a competing primary. The rubric calls for adversarial debate when 2-3 *competing strong* fixes are proposed; here we have one strong consensus fix + one weaker refactor proposal.

**Decision (per Wave 3 exit criteria)**: Both fixes share the same diagnosis but differ in mechanism. Per the protocol's Wave 4 entry rule ("when Wave 3 produced 2-3 competing strong fix proposals"), the prudent call is **to run the adversarial debate in `--depth quick` mode**: same diagnosis, different mechanism — exactly the case the skill's Wave 4 step 2 names as "Use `--depth quick` if all proposals share the same diagnosis and only differ in the fix mechanism." This is consistent with the `--type security` raised bar; let the debate confirm we're not papering over a refactor that should be done now.

Both fix proposals are written to `fix-proposals/` as standalone files.
