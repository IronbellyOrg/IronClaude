# Code Review — PR #62

| Field | Value |
|---|---|
| Repo | IronbellyOrg/IronClaude |
| PR # | 62 |
| Title | fix(prd): align gates.py research-notes schema with upstream prompt |
| State | MERGED (2026-05-20T06:25:20Z) |
| Base / Head | master ← fix/prd-gates-schema-divergence |
| Commit | f4d5df19cf34198f8f91af06425912e3315e2273 |
| Stats | +5427 / -32 across 21 files (production diff: 4 files, ~108 lines) |
| Review date | 2026-05-20 |
| Depth | Standard (focus on production code + tests; meta/task artifacts skimmed) |

## Scope

The PR fixes a schema-divergence bug where the PRD pipeline gate (`gates.py`) hard-coded a 7-name section list that did not match what the prompt (`prompts.py`) instructed the agent to emit, causing every `superclaude prd run` invocation to halt at the step-4 research-notes gate. The production-code surface is small (8 lines changed in `gates.py`) plus three test files (one new). The bulk of the +5,427 line count is meta-files in `.dev/tasks/to-do/TASK-RF-20260520-050937/`.

## Findings

### Critical
None.

### High
None.

### Medium

#### M1 — Stale error message and docstring after rename ("Suggested Phases" → "SUGGESTED_PHASES")
- File: `src/superclaude/cli/prd/gates.py:130`, `gates.py:140`, `gates.py:145`, `gates.py:335`
- After the schema rename from the old human-readable list (`"Suggested Phases"`) to the new `SUGGESTED_PHASES` convention, the function's docstring (`"""Check that the Suggested Phases section..."""`), the error strings (`"No 'Suggested Phases' section found"`, `"Suggested Phases section has no detail items"`), and the `_make_semantic_check` `failure_message` (`"Suggested Phases section lacks detail"`) all still reference the legacy name. Operators who see the error in pipeline output will grep for `"Suggested Phases"` in `prompts.py` / `SKILL.md` and find nothing.
- Why it matters: It is the same class of drift this PR is fixing. The fix landed in the regex but the surrounding human-facing text was not updated to match. Recommend tightening to `"No 'SUGGESTED_PHASES' section found"` etc., to keep the error message aligned with what the agent was actually instructed to emit.

#### M2 — Schema is duplicated in three places; round-trip test only covers two of them
- Files: `src/superclaude/cli/prd/gates.py:102-110` (the list), `src/superclaude/cli/prd/prompts.py:226-256` (prompt template), `src/superclaude/skills/prd/SKILL.md:280-304` (template / source of truth)
- The new `tests/cli/prd/test_research_notes_roundtrip.py:53-60` only verifies `prompts.py` ↔ `gates.py`. The PR body explicitly identifies `SKILL.md` as the upstream source of truth, but no test pins `SKILL.md` to either `prompts.py` or `gates.py`. If the skill is updated upstream and re-synced via `make sync-dev`, the two CLI artifacts can silently drift again.
- Why it matters: This is the exact failure mode this PR was patched to prevent — schema drift between an instruction surface and an enforcement surface. The structural blind spot is narrowed, not closed. Recommend adding a second round-trip assertion that extracts the H2 list from `src/superclaude/skills/prd/SKILL.md` (or `refs/agent-prompts.md`) and pins it to `_RESEARCH_REQUIRED_SECTIONS`.

### Low

#### L1 — Roundtrip test regex silently filters non-uppercase headings
- File: `tests/cli/prd/test_research_notes_roundtrip.py:50`
- `_extract_h2_sections_from_prompt` uses `r"^##\s+([A-Z_][A-Z0-9_]+)\s*$"`. This is restrictive in a good way for current schema but would silently filter out any future `## Mixed_Case` heading from the comparison. If somebody adds a lowercase section to `prompts.py`, the schema-match assertion still passes because the lowercase heading isn't in the extracted list. The test could falsely report "schemas match" while drift exists.
- Why it matters: The test framing is "the schema instructed equals the schema accepted," but the extractor's filter encodes an extra invariant ("schema is ALL_CAPS") that isn't asserted anywhere. Consider either (a) extracting all `^## (.+)$` then filtering, with an explicit `assert all(s.isupper() for s in instructed)` so the invariant is visible, or (b) documenting why uppercase-only is enforced.

#### L2 — `_check_research_notes_sections` is case-insensitive, allowing lowercase section headings to pass
- File: `src/superclaude/cli/prd/gates.py:118-121`
- Both `heading_pat` and `bold_pat` are compiled with `re.IGNORECASE`. So `## existing_files`, `## Existing_Files`, or even `**existing_files**` would all pass the gate even though the prompt and SKILL.md explicitly instruct uppercase (`## EXISTING_FILES`). The pre-existing flag (not introduced by this PR) is now more visible because all 7 sections are uppercase by convention.
- Why it matters: Permissive matching reduces gate value. Either the casing convention should be enforced (drop `re.IGNORECASE`) or its laxness should be explicitly documented as intentional. As-is, an agent that emits a lowercase variant passes the gate but downstream tooling (e.g., `prompts.py:290` which references `SUGGESTED_PHASES` literally) may break.

#### L3 — Heading regex allows arbitrary leading text on the heading line
- File: `src/superclaude/cli/prd/gates.py:119`
- The pattern `rf"^\s*#{{1,4}}\s+.*{re.escape(section)}"` includes `.*` between the heading marker and the section name. This permits headings like `## Random Prefix EXISTING_FILES` to satisfy the check. Pre-existing behavior; not introduced by the PR but now interacts with shorter `ALL_CAPS_TOKEN` section names that are more likely to appear coincidentally inside other heading text.
- Why it matters: Marginal robustness; if an agent emits a heading like `## Discussion of EXISTING_FILES patterns` instead of the dedicated section, the gate still passes. A tighter anchor (`rf"^\s*#{{1,4}}\s+{re.escape(section)}\b"`) would be safer.

#### L4 — Repository hygiene: 17 task-tracker files (~5,200 lines) committed to `to-do/` despite "Done" status
- Directory: `.dev/tasks/to-do/TASK-RF-20260520-050937/`
- The task's own frontmatter states `status: "🟢 Done"` (per the diff at `TASK-RF-20260520-050937.md`) and the PR body says all phases are PASS. Convention in this repo (verified by `.dev/tasks/done/` containing previously-completed `TASK-*` folders) is to move completed tasks to `done/`. The new task folder is committed to `to-do/`.
- Why it matters: Inconsistent with existing convention, will require a follow-up commit/PR to relocate. Also bloats the merge diff (94 % of the +5,427 line count is meta-files, not code).

### Nits

#### N1 — `pytest.fixture()` called with empty parens
- File: `tests/cli/prd/test_research_notes_roundtrip.py:26`
- Stylistic: `@pytest.fixture()` works identically to `@pytest.fixture` (no parens). Project-wide consistency check would be useful.

#### N2 — Comment in test slightly misleading
- File: `tests/cli/prd/test_research_notes_roundtrip.py:70-72`
- The comment says "Ensure SUGGESTED_PHASES has a numbered list item so `_check_suggested_phases_detail` finds detail under the heading (the loop appends a `- detail` bullet which already satisfies the list-pattern regex...)". Since the bullet already satisfies the regex, appending `"1. Phase one detail\n"` at the END of the document (after all sections) is gratuitous and slightly misleading — the gate scans `content[phases_match.end():]` which includes everything after the heading, so the bullet inside the loop is what actually carries the assertion. The appended numbered list at the file-end is harmless but doesn't add the asserted behavior. Either rely on the in-section bullet (and drop the trailing line) or move the numbered item inside the SUGGESTED_PHASES section to make the test express the documented intent.

#### N3 — Schema referenced as "EXISTING_FILES schema" in PR body but section names span 7 distinct tokens
- The naming convention "EXISTING_FILES schema" (used in the PR body and commit message) is potentially confusing since `EXISTING_FILES` is one of seven section names. Consider "ALL_CAPS section schema" or "v2 research-notes schema" in future changelog/release entries.

## Positive observations

- The round-trip integration test (`test_research_notes_roundtrip.py`) is a structural improvement that closes the exact blind spot the bug exploited. The two-assertion design (schema-equality + conforming-output-passes) is well-targeted.
- The regex widening `\s+` → `[\s_]+` at `gates.py:135` is minimal and correct. With `SUGGESTED_PHASES` (single underscore between words), it matches; the legacy `## Suggested Phases` (space) also still matches; and the prefix `Suggested[\s_]+` remains optional so bare `## Phases` still works.
- Test coverage was expanded in lockstep: `test_gates.py`, `test_e2e.py` (5 e2e scenarios), and the new round-trip test. All 20 PRD gate-related tests pass locally on master after the merge (verified by re-running `uv run pytest tests/cli/prd/test_gates.py tests/cli/prd/test_research_notes_roundtrip.py tests/cli/prd/test_e2e.py -v`).
- The PR is well-scoped: it does not touch `prompts.py` or `SKILL.md`, only the gate (the divergent surface). Out-of-scope sections in the PR description are explicit and correct.
- Frontmatter `Date / Scenario / Tier` required by the `research-notes` gate (verified at `gates.py:323`) is matched by the prompt template at `prompts.py:218-222` — no drift there.

## Summary

| Severity | Count |
|---|---|
| Critical | 0 |
| High | 0 |
| Medium | 2 |
| Low | 4 |
| Nit | 3 |
| Total | 9 |

**Verdict (advisory, PR already merged):** The fix is correct and well-tested. The two medium-priority items (stale "Suggested Phases" string artifacts and incomplete schema-drift coverage that does not pin `SKILL.md`) are worth addressing in a follow-up. The repository-hygiene issue (L4 — task folder placed in `to-do/` despite Done status) appears to be a follow-up bookkeeping omission rather than a code defect.
