# Code Review — PR #62

| Field | Value |
| --- | --- |
| Repository | IronbellyOrg/IronClaude |
| PR Number | #62 |
| Title | fix(prd): align gates.py research-notes schema with upstream prompt |
| Author | @ironbelly |
| State | MERGED (merge commit `f333cdf`, 2026-05-20 06:25 UTC) |
| Base / Head | `master` ← `fix/prd-gates-schema-divergence` |
| Diff size | +5,427 / −32, 21 files (16 docs/artifacts under `.dev/tasks/...`, 4 code/test files, 1 new test file) |
| Review depth | Standard (security / architecture / quality / performance / anti-patterns / tests / docs) |
| Review date | 2026-05-20 |
| Posted to GitHub | No (review-only; PR is already merged) |

## Scope of the change

Net source change is tiny and surgical:

- `src/superclaude/cli/prd/gates.py` — rewrites the 7-element `_RESEARCH_REQUIRED_SECTIONS` list from English-phrase form (`Product Capabilities`, `Technical Architecture`, …) to the UPPER_SNAKE form the prompt actually emits (`EXISTING_FILES`, `PATTERNS_AND_CONVENTIONS`, …); widens one regex from `\s+` to `[\s_]+` inside `_check_suggested_phases_detail`.
- `tests/cli/prd/test_gates.py` — fixture rewritten in lockstep with the new schema.
- `tests/cli/prd/test_e2e.py` — the `_make_passing_output("research-notes", …)` branch now emits the new schema so the 5 e2e scenarios still pass.
- `tests/cli/prd/test_research_notes_roundtrip.py` (new, 76 LOC) — round-trip integration test asserting `build_research_notes_prompt()` H2 sections equal `_RESEARCH_REQUIRED_SECTIONS`.
- 16 files under `.dev/tasks/to-do/TASK-RF-20260520-050937/` — MDTM artifacts (research, QA reports, pytest output, lint output, etc.).

I re-ran the focused suite locally on the merged tree:

```
uv run pytest tests/cli/prd/test_research_notes_roundtrip.py tests/cli/prd/test_gates.py -v
# 15 passed in 0.14s
```

The fix is correct, minimal, and the new round-trip test would have caught the original drift. I have no critical, high, or medium-severity concerns about the source change itself. All findings below are low / nit.

---

## Findings

### Critical
*(none)*

### High
*(none)*

### Medium
*(none)*

### Low

#### L1 — Bloated `make-lint.txt` artifact committed to the repo
- File: `.dev/tasks/to-do/TASK-RF-20260520-050937/phase-outputs/test-results/make-lint.txt` (3,145 LOC, 60% of the PR's net additions)
- Why it matters: this is a one-shot log of an unrelated full-repo lint run, captured during MDTM execution. It is checked into `master` and will be carried forever in the git history. `.gitignore` already excludes `.dev/eval-runs/` and `.dev/sprint-state/`; consider extending the rule to `.dev/tasks/**/phase-outputs/test-results/*.txt` (or at minimum the multi-MB lint logs) so that future MDTM runs do not balloon `master` with throwaway tool output. The 22-line `pytest-focused-summary.md` and 28-line `pytest-focused.txt` artifacts are reasonable to keep; the 3,145-line lint dump is not.

#### L2 — `_check_research_notes_sections` accepts permissive heading wrappers; new uppercase tokens raise the false-positive surface
- File: `src/superclaude/cli/prd/gates.py:113-126` (heading pattern `re.compile(rf"^\s*#{{1,4}}\s+.*{re.escape(section)}", re.MULTILINE | re.IGNORECASE)`).
- Why it matters: the regex matches any heading line that *contains* the section name as a substring, not the heading whose body equals it. With the previous English names (`"Suggested Phases"`) the collision risk was low. With the new uppercase tokens the risk is non-trivial: a heading like `## EXISTING_FILES_LEGACY_NOTES` would satisfy the gate's "has EXISTING_FILES section" check while a downstream consumer scanning for `^## EXISTING_FILES$` would miss it, producing schema drift in the opposite direction the PR is trying to prevent. The PR does not change this regex shape — it inherits it — but the schema change increases its blast radius. Tightening to `rf"^\s*#{{1,4}}\s+{re.escape(section)}\s*$"` would close it; if the looseness is intentional for tolerating bold prefixes etc., a comment to that effect would help future maintainers. (Pre-existing in spirit, but newly relevant.)

#### L3 — `re.IGNORECASE` on UPPER_SNAKE schema constants is permissive vs. the prompt's spec
- File: `src/superclaude/cli/prd/gates.py:119, 121` (the `re.IGNORECASE` flag on both `heading_pat` and `bold_pat`).
- Why it matters: the prompt in `src/superclaude/cli/prd/prompts.py:226-254` instructs the agent to emit the H2 sections in upper case (`## EXISTING_FILES`). With `IGNORECASE` the gate accepts `## existing_files` or `## Existing_Files` too. Today this is just leniency, not a bug — but the entire point of the PR is to lock prompt-schema and gate-schema together as a contract. Either drop `re.IGNORECASE` so the gate fails closed when the model produces a mixed-case variant the prompt did not authorize, or document in the gate that case insensitivity is an intentional escape hatch. The new round-trip test does not cover this (it builds with the exact prompt casing).

#### L4 — Round-trip test asserts schema equality but not the failure direction
- File: `tests/cli/prd/test_research_notes_roundtrip.py:53-60`
- Why it matters: the PR description explicitly says "Reviewer to confirm round-trip test fails meaningfully if either Edit A or Edit B is reverted." Edit A would clearly cause `test_prompt_schema_matches_gate_schema` to fail (list inequality). Edit B (the `\s+` → `[\s_]+` widening for `_check_suggested_phases_detail`) is **not directly exercised** by the new tests — `test_prompt_conforming_output_passes_gate` builds a fake notes string with `## SUGGESTED_PHASES` plus a `1. Phase one detail` line, but the surrounding `_check_suggested_phases_detail` regex would also have matched **before** Edit B if there were any heading anywhere containing the word "Phases" (the `(?:Suggested[\s_]+)?` group is optional). I confirmed: reverting Edit B in isolation does not break `test_prompt_conforming_output_passes_gate` because the regex still matches the `## SUGGESTED_PHASES` heading via the unconditional `Phases` token at the tail (the optional `(?:Suggested...)?` group is, well, optional). The PR's claim that the round-trip test guards Edit B is overstated. Recommendation: add a focused test that asserts `_check_suggested_phases_detail("## SUGGESTED_PHASES\n- x")` is `True`, and ideally one for `## suggested phases` and `## suggested_phases` so the regex is pinned in all three casings the prompt and downstream agents may emit.

#### L5 — Unused `skill_refs_dir` setup in the round-trip fixture
- File: `tests/cli/prd/test_research_notes_roundtrip.py:35-44`
- Why it matters: the fixture creates `tmp_path / "refs"` and passes it as `skill_refs_dir`, but `build_research_notes_prompt()` (verified at `src/superclaude/cli/prd/prompts.py:188-260`) never reads from `skill_refs_dir`. The dir creation is dead setup that future readers will assume is required. Either delete the two lines or add a comment explaining it satisfies a `PrdConfig` invariant (the field has a default factory in `models.py:188`, so the empty path is in fact unnecessary for the test).

#### L6 — Schema constants live in two places without a one-line cross-reference
- Files: `src/superclaude/cli/prd/prompts.py:226-254` (prompt) and `src/superclaude/cli/prd/gates.py:102-110` (`_RESEARCH_REQUIRED_SECTIONS`).
- Why it matters: the PR is itself a fix for these two lists drifting apart. The round-trip test now guards the invariant at CI time, but a developer editing either side will only see the other side if they happen to know to look. A 2-line docstring comment on `_RESEARCH_REQUIRED_SECTIONS` ("MUST mirror the H2 sections instructed by `build_research_notes_prompt()` in prompts.py — guarded by tests/cli/prd/test_research_notes_roundtrip.py") and a symmetric note above the prompt's section list would prevent the next port-time fabrication.

### Nit

#### N1 — Inline comment in roundtrip test contradicts itself
- File: `tests/cli/prd/test_research_notes_roundtrip.py:70-72`
- Why it matters: the comment says "Ensure SUGGESTED_PHASES has a numbered list item so `_check_suggested_phases_detail` finds detail under the heading" — but then immediately admits "the loop appends a `- detail` bullet which already satisfies the list-pattern regex". The `1. Phase one detail` line on line 73 is therefore decorative. Either remove the extra line or drop the contradictory comment.

#### N2 — `_check_suggested_phases_detail` heading regex is anchored only by the word "Phases"
- File: `src/superclaude/cli/prd/gates.py:134-138`
- Why it matters: the new regex `r"(?:^|\n)\s*#{1,4}\s+.*(?:Suggested[\s_]+)?Phases"` makes "Suggested" optional but keeps "Phases" required, with leading `.*`. A document that contains a heading like `## Implementation Phases` (with no SUGGESTED prefix at all) would satisfy the "Suggested Phases section exists" check. Probably acceptable for the lenient-by-design gate, but worth a one-line comment that the gate intentionally accepts any phases-style heading.

#### N3 — `re.escape(section)` is applied to constants that contain no regex-active characters
- File: `src/superclaude/cli/prd/gates.py:119, 121`
- Why it matters: harmless and defensive; calling it out only because the previous English values also had no regex-active characters, so this is purely a robustness pattern carried over. Keep it.

---

## Summary

| Severity | Count |
| --- | --- |
| Critical | 0 |
| High | 0 |
| Medium | 0 |
| Low | 6 |
| Nit | 3 |
| **Total** | **9** |

### Bottom line
The fix is correct, minimal, well-tested in the structural direction (Edit A), and the new round-trip integration test is a real architectural improvement: it converts an implicit cross-file contract (prompt H2 schema ≡ gate `_RESEARCH_REQUIRED_SECTIONS`) into a CI-enforced invariant. The single substantive review-time concern is **L4** — the round-trip test does not actually catch a revert of Edit B, contrary to the PR description; a targeted unit test would close that. Other low-severity items are tightening opportunities (regex strictness, fixture cleanup, doc cross-references) and one repo-hygiene item (**L1**: a 3,145-line lint log committed to history). No security, performance, or architectural concerns.

### Verification re-run on merged tree
- `uv run pytest tests/cli/prd/test_research_notes_roundtrip.py tests/cli/prd/test_gates.py -v` → 15 passed in 0.14s (locally confirmed).
- Prompt sections at `src/superclaude/cli/prd/prompts.py:226,230,233,236,239,251,254` match `_RESEARCH_REQUIRED_SECTIONS` at `src/superclaude/cli/prd/gates.py:103-109` exactly (7 names, order-independent).
- Upstream skill at `src/superclaude/skills/prd/SKILL.md:280-303` corroborates the EXISTING_FILES schema as the source of truth.
