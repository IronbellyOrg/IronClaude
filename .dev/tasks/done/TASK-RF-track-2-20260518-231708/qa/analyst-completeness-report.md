# Phase 11 QA — Analyst Completeness Track 2

**Topic:** FU-002 reflexion writer test pollution — `REFLEXION_OUTPUT_DIR` override + pytest fixture upgrade + autouse safety net
**Date:** 2026-05-18
**Files analyzed:** 3 (01-file-inventory.md, 02-test-fixtures.md, 03-template-examples.md)
**Depth tier:** Standard
**Pre-existing pollution baseline:** 84 files + 292 lines

---

## Verdict: FAIL — 1 CRITICAL ambiguity (env-var name disagreement) + 2 IMPORTANT gaps

The three research files are individually thorough and evidence-rich, but they contain a load-bearing **internal contradiction on the env-var name** (`REFLEXION_OUTPUT_DIR` in 01-file-inventory vs `SUPERCLAUDE_REFLEXION_MEMORY_DIR` in 02-test-fixtures), and Track 2 has no inventory of the baseline-cleanup procedure for the 84 polluted files + 292 JSONL lines that the regression test depends on. Synthesis cannot proceed until the env-var name is canonicalized and the baseline-cleanup step is specified.

---

## 1. Source Files Identified (checklist item 1)

| Required source | Covered? | Evidence |
|---|---|---|
| `reflexion.py` L56-74 (`__init__`) | YES | 01-file-inventory §1 table L18-24; §2 verbatim L64-70 quote; §6 patch shown for L56-74. 02-test-fixtures §1 also cites L56-74. |
| `reflexion.py` L123-124 (JSONL append) | YES | 01-file-inventory §3 row 3+4 (`self.solutions_file.open("a")` / `f.write(json.dumps(error_info) + "\n")`) |
| `reflexion.py` L308 (mistake .md write) | YES | 01-file-inventory §3 row 5 (`filepath.write_text(content)` at L308) |
| `pytest_plugin.py` L71-81 (`reflexion_pattern` fixture) | YES | 02-test-fixtures §1 cites L71-81 with verbatim quote; 01-file-inventory §4 notes "pytest_plugin.py:81 return ReflexionPattern() ... no args" |
| `pytest_plugin.py` L160-184 (`pytest_runtest_makereport` hook) | YES | 02-test-fixtures §1 quotes L160-184; 01-file-inventory §4 cites "pytest_plugin.py:173" with `reflexion = ReflexionPattern()` |
| `tests/unit/test_reflexion.py` 9 tests | YES | 02-test-fixtures §2 enumerates all 9 tests with line numbers + pollution classification; 01-file-inventory §4 enumerates instantiation sites at L17, 25, 39, 52, 73, 100, 118, 165. Minor cross-file line offset on test_initialization (15 vs 17) and test_record_error_basic (23 vs 25), likely def-line vs first-statement counting — not load-bearing |
| `tests/integration/test_pytest_plugin.py` | YES | 02-test-fixtures §3 cites L25-29 and L45-90 (neither writes); 01-file-inventory §4 cites lines 25,27,28,29,46 |

**Verdict for item 1: PASS.** Source files covered with line-level evidence.

---

## 2. Output Paths Clear (checklist item 2)

| Required output spec | Covered? | Evidence |
|---|---|---|
| Env var name | **CONTRADICTION** | 01-file-inventory §6 says `REFLEXION_OUTPUT_DIR` (4 occurrences). 02-test-fixtures §4 says `SUPERCLAUDE_REFLEXION_MEMORY_DIR` (4 occurrences in patch + autouse fixture + comments). Spawn prompt names `REFLEXION_OUTPUT_DIR`. Synthesis cannot pick one without an explicit decision. |
| conftest.py monkeypatch design | YES | 02-test-fixtures §4 provides the full autouse fixture in `tests/conftest.py` using `monkeypatch.setenv(...)` to `str(tmp_path / "reflexion_memory")` |
| Autouse safety net design | YES | 02-test-fixtures §4 names it `_redirect_reflexion_writes`, scope autouse, redirects all bare `ReflexionPattern()` constructions including the hook path |
| Existing adjacent fixture patterns to mirror | YES | 02-test-fixtures §1 cites `temp_memory_dir(tmp_path)` at `tests/conftest.py:101-121` and `pm_context(tmp_path)` at `pytest_plugin.py:105-133` as templates |

**Verdict for item 2: FAIL** — the env-var name is the single most load-bearing identifier in this task and the two research files disagree. This must be resolved before synthesis.

---

## 3. Phases (checklist item 3)

Expected phase shape: Inventory → Add env-var resolver → Upgrade pytest fixture → Add autouse → Update direct-construction tests → Regression test → Validation.

| Phase | Covered in research? | Evidence |
|---|---|---|
| Inventory | YES | 01-file-inventory §4 (every `ReflexionPattern` caller); 02-test-fixtures §2 (every test, with pollution flag) |
| Add env-var resolver in `reflexion.py` `__init__` | YES | 01-file-inventory §6 (concrete patch with `os.environ.get`); 02-test-fixtures §4 "Track-1 prerequisite" code block |
| Upgrade pytest fixture | YES | 02-test-fixtures §4 "Track-2 fixture upgrade" patch for `pytest_plugin.py:71-81` |
| Add autouse safety net | YES | 02-test-fixtures §4 `_redirect_reflexion_writes` autouse fixture |
| Update direct-construction tests | PARTIAL | 02-test-fixtures §4 argues the autouse safety net makes individual updates unnecessary because env-var redirects all bare `ReflexionPattern()` constructions. This is a design decision (Option C makes the per-test update redundant) and should be documented as such in synthesis. The 6 bare-construction tests (2,3,4,5,7,9 from §2) are enumerated, so the alternative path exists if needed. |
| Regression test | YES | 02-test-fixtures §5 provides 3 designs (5a per-test guard, 5b git-status guard, 5c file-name fingerprint) with recommendation to combine 5a+5c (and 5b for local dev) |
| Validation (test execution) | YES | 03-template-examples §4 Track 2 recommendation: `uv run pytest tests/unit/test_reflexion.py -v` + regression sweep `uv run pytest -v --ignore=tests/unit/test_reflexion.py` |

**Verdict for item 3: PASS** — all phases covered. The "update direct-construction tests" phase is intentionally optional under Option C; synthesis should mark this as a decision point but not a gap.

---

## 4. Patterns Documented (checklist item 4)

| Required pattern | Covered? | Evidence |
|---|---|---|
| pytest fixture conventions (function scope, monkeypatch, tmp_path) | YES | 02-test-fixtures §1 cites `temp_memory_dir` and `pm_context` as in-repo precedents; §4 demonstrates `tmp_path` + `monkeypatch.setenv` patterns |
| env-var override precedence (explicit > env > cwd) | YES | 01-file-inventory §6 "Resolution chain (priority order)" explicitly lists: 1. constructor arg, 2. env var, 3. cwd default |
| Autouse fixture conventions | YES | 02-test-fixtures §4 explains why autouse is needed (catches tests that don't take the explicit fixture and the `pytest_runtest_makereport` hook) |
| Backward-compatibility for downstream consumers | YES | 01-file-inventory §5 notes "external downstream consumers ... `ReflexionPattern()` with no args must still resolve to `Path.cwd() / 'docs' / 'memory'` in absence of the env var" |

**Verdict for item 4: PASS** — all patterns documented with precedents.

---

## 5. Template Notes (checklist item 5)

03-template-examples is the shared track-template research. Required: Template 02 + analogous done/ example.

| Required template element | Covered? | Evidence |
|---|---|---|
| MDTM Template 02 PART 1 distillation (A-M rules) | YES | 03-template-examples §1 covers A1-A4, B1-B7, C1-C4, D3, E1-E4, F1-F2, I3, I11-I18, L1-L7, M1-M2 with file:line citations against `02_mdtm_template_complex_task.md` |
| Mandatory body sections + ordering | YES | 03-template-examples §2 lists frontmatter fields (template:1-44) and body sections in mandatory order (template:896-1099) |
| Analogous done/ example for Track 2 | YES | 03-template-examples §3 Example B (`TASK-RF-track-4-20260517-032112` — "Repair tests/audit/ fixtures + xfail genuinely-broken cases") explicitly identified as the exact-shape match for Track 2; §4 Track 2 confirms "Mirror: Example B (Track-4 PR4) — exact shape match for 'test isolation / fixture repair'" |
| Per-track phase skeleton | YES | 03-template-examples §4 Track 2 provides 8-phase skeleton (Prep, Discovery, Phase Gate, Execute, Verify, Phase Gate, Commit/PR, Post-Completion) with item counts and pattern references |
| Quick-reference builder checklist | YES | 03-template-examples §5 11-item pre-flight checklist for builders |

**Verdict for item 5: PASS** — template guidance is complete and Example B is correctly mapped.

---

## 6. Granularity (checklist item 6)

Expected per-file items: 6 tests bypassing fixture + 1 hook path + 1 source file + 1 fixture + 1 regression test.

| Granularity element | Covered? | Evidence |
|---|---|---|
| 6 tests that bypass the fixture | YES | 02-test-fixtures §2 enumerates tests 2,3,4,5,7,9 as "POLLUTES" with bare `ReflexionPattern()` (matches spawn-prompt count of 6) |
| 1 hook path (`pytest_runtest_makereport`) | YES | 02-test-fixtures §1 dedicated subsection cites L160-184; 01-file-inventory §4 row "pytest_plugin.py:173" |
| 1 source file (`reflexion.py`) | YES | 01-file-inventory §6 concrete patch with line counts ("~6 added lines, 0 removed") |
| 1 fixture (`reflexion_pattern`) | YES | 02-test-fixtures §1 verbatim quote of current fixture; §4 concrete upgraded version |
| 1 regression test | YES | 02-test-fixtures §5 three designs (5a, 5b, 5c) with recommendation to combine 5a+5c |
| 1 autouse safety net | YES | 02-test-fixtures §4 `_redirect_reflexion_writes` design with code block |

**Verdict for item 6: PASS** — granularity is per-item ready. Note that under Option C the autouse safety net makes per-test updates of the 6 bare-construction tests optional (a single env-var setenv covers them all). Synthesis should make this explicit so the builder doesn't generate 6 redundant items.

---

## 7. Doc Cross-Validation Tagged (checklist item 7)

This task's research is overwhelmingly **code-sourced**, not doc-sourced. There are no architectural claims sourced from `docs/` or `README` requiring `[CODE-VERIFIED]` / `[CODE-CONTRADICTED]` / `[UNVERIFIED]` tags. The sources cited are:

- `src/superclaude/pm_agent/reflexion.py` (code) — verified by direct line citations
- `src/superclaude/pytest_plugin.py` (code) — verified by direct line citations and verbatim quotes
- `tests/unit/test_reflexion.py` (code) — verified by enumeration
- `tests/integration/test_pytest_plugin.py` (code) — verified by enumeration
- `pyproject.toml` `pytest11` entry point (mentioned in 02 §1 as the auto-load mechanism — this is a factual claim about packaging and could benefit from a verify-tag, but the claim is benign)
- `.claude/templates/workflow/02_mdtm_template_complex_task.md` (template) — verified by extensive file:line citations in 03

The 02 §2 "Live pollution evidence" claim ("84 files ... 292 lines ... verified via Bash 2026-05-18") is a live filesystem state observation, not a doc claim, and is consistent with the spawn-prompt baseline (84 files + 292 lines).

**Verdict for item 7: PASS** — no doc-only claims requiring verification tags. The one packaging claim (pytest11 entry point) is corroborated by 01-file-inventory §4's enumeration of plugin entry points.

---

## 8. Solution Approaches Evaluated (checklist item 8)

| Required option | Covered? | Evidence |
|---|---|---|
| Option A (constructor only) | YES | 02-test-fixtures §4 "Rationale" — "Why not Option A alone: 6 of 8 tests in test_reflexion.py call ReflexionPattern() directly, not the fixture. Fixing only the fixture leaves the bulk of pollution untouched." |
| Option B (env var only) | YES | 02-test-fixtures §4 "Rationale" — "Why not Option B alone: Requires the prerequisite production change anyway; without the fixture upgrade, the *explicit* reflexion_pattern fixture still constructs ReflexionPattern() before any monkeypatch.setenv in the consuming test runs." |
| Option C (both) | YES | 02-test-fixtures §4 "Why Option C wins: The fixture upgrade makes the intent explicit and self-documenting; the autouse env-var monkeypatch is the safety net for everything else, including future tests. Cost is a single Path.cwd() resolution + one setenv per test — negligible." |
| Researcher recommendation | YES | 02-test-fixtures §4 explicit "Recommendation: Option C (Both) — defense-in-depth, scoped per-test". 01-file-inventory §6 also implicitly favors C ("conftest/fixture changes can simply monkeypatch.setenv ... and every call site ... will redirect"). |

**Verdict for item 8: PASS** — all three options evaluated with rationale; researchers converge on Option C.

---

## 9. Ambiguities Documented (checklist item 9)

| Required ambiguity | Documented? | Evidence |
|---|---|---|
| Env-var name choice | **DOCUMENTED BUT UNRESOLVED** | 01-file-inventory uses `REFLEXION_OUTPUT_DIR` throughout §6; 02-test-fixtures uses `SUPERCLAUDE_REFLEXION_MEMORY_DIR` throughout §4. Spawn prompt names `REFLEXION_OUTPUT_DIR`. Neither file flags this as an open question — they assume their own choice. This is the **critical** synthesis-blocking ambiguity. |
| Whether to retain cwd-default or change it | YES | 01-file-inventory §5 explicitly resolves: "External downstream consumers ... `ReflexionPattern()` with no args must still resolve to `Path.cwd() / 'docs' / 'memory'` in absence of the env var" — retain. §6 patch preserves the cwd fallback. 02-test-fixtures §4 patch also preserves cwd fallback. |
| `pyproject.toml` requires-pytest-plugin re-registration | NO (not raised) | Not flagged but not load-bearing; the plugin is already registered. |

**Verdict for item 9: FAIL** — the env-var name ambiguity exists in the corpus but is not surfaced as an "Open Question" in either file. Synthesis must either pick one OR raise it as an explicit Open Question for the user.

---

## Compiled Gaps

### Critical Gaps (block synthesis)

1. **Env-var name contradiction.** 01-file-inventory and 02-test-fixtures use different env-var names (`REFLEXION_OUTPUT_DIR` vs `SUPERCLAUDE_REFLEXION_MEMORY_DIR`). The spawn prompt and 01-file-inventory align on `REFLEXION_OUTPUT_DIR`; 02-test-fixtures' fixture and autouse patches use `SUPERCLAUDE_REFLEXION_MEMORY_DIR`. Source: research files 01 §6 and 02 §4. Why critical: this is the literal string in source code, fixture, and autouse fixture. Any divergence between production and test code = the redirect silently breaks and tests pollute the repo anyway. **Required action before synthesis: pick one and propagate to all three patches (reflexion.py, pytest_plugin.py fixture, conftest.py autouse).**

### Important Gaps (affect quality)

2. **Baseline cleanup procedure not specified.** The regression test design in 02-test-fixtures §5b assumes "the regression test should run *after* a `git restore docs/memory/solutions_learned.jsonl` and `git clean -fd docs/mistakes/` to clear the existing 84-file backlog + 292 polluted JSONL lines." But Track 2 has no checklist-level item describing how/when this cleanup is done, by whom, and whether it lands in the same PR as the fix. Without an explicit baseline-cleanup step, the regression test will fail on landing because the working tree is already dirty with the 84 files + 292 lines. **Required action: synthesis must add a "Baseline cleanup" step (likely in Phase 3 or Phase 4) that clears the 84 files + 292 lines and explains the commit ordering (cleanup commit → fix commit, or single squash).**

### Minor Gaps (must still be fixed)

3. **Test line-number minor mismatch.** 02-test-fixtures §2 lists test_initialization at L15 while 01-file-inventory §4 lists `tests/unit/test_reflexion.py:17`. Same drift for test_record_error_basic (23 vs 25). Almost certainly a def-line vs first-statement counting difference. Synthesis should pick one source for line citations (recommend the test-by-test table in 02-test-fixtures §2 since it includes purpose + pollution classification).

4. **`pytest_runtest_makereport` hook gating clarification.** 02-test-fixtures §1 mentions the hook fires only on `@pytest.mark.reflexion`-marked tests. No reflexion-marked tests in `tests/unit/test_reflexion.py` are flagged with this marker (the marker integration test at L139 takes the fixture but is not itself marked). Worth a sentence in synthesis to confirm the hook path is currently dormant in the test suite but must still be covered for forward-compatibility (any future `@pytest.mark.reflexion`-marked test that fails would pollute).

---

## Depth Assessment

**Expected depth:** Standard — file-level understanding with key function documentation.
**Actual depth achieved:** Standard+. The research goes deeper than required:

- 01-file-inventory gives a full method anatomy table with line ranges per method
- 02-test-fixtures gives per-test pollution classification with rationale for each tag
- 02-test-fixtures §4 provides 3 concrete code blocks (the Track-1 prerequisite patch, the Track-2 fixture upgrade, and the autouse safety net) ready to drop in
- 02-test-fixtures §5 gives 3 alternative regression-test designs with tradeoffs
- 03-template-examples gives a per-track recommended phase skeleton with item counts

**Missing depth elements:** None for the Standard tier. The depth would meet Deep-tier expectations if not for the env-var contradiction and the missing baseline-cleanup step.

---

## Recommendations (for synthesis stage)

1. **Resolve the env-var name FIRST.** Pick `REFLEXION_OUTPUT_DIR` (matches spawn prompt + 01-file-inventory) OR `SUPERCLAUDE_REFLEXION_MEMORY_DIR` (matches 02-test-fixtures). Recommendation: use `REFLEXION_OUTPUT_DIR` — it is the shorter form, matches the spawn prompt verbatim, and namespace-pollution risk inside pytest is negligible since `REFLEXION_` is unlikely to collide. If the team prefers the namespaced form, propagate `SUPERCLAUDE_REFLEXION_MEMORY_DIR` consistently. Either way, the synthesized task file MUST use exactly one literal string across reflexion.py, pytest_plugin.py fixture, and conftest.py autouse fixture.

2. **Add a baseline-cleanup phase or step.** Suggested location: Phase 3 (Execute), as the FIRST step before the env-var resolver patch: `git restore docs/memory/solutions_learned.jsonl && git clean -fd docs/mistakes/` (or equivalent surgical removal of only the 84 test-generated files, preserving any legitimate mistake docs that may have accumulated). Spell out whether this lands in the same commit as the fix or as a preceding "chore: clean reflexion test pollution baseline" commit.

3. **Add to Open Questions section of synthesis:** "Should `pytest_runtest_makereport` hook continue to instantiate `ReflexionPattern()` in production, or be gated behind an env flag too? Currently dormant (no `@pytest.mark.reflexion`-marked tests exist in `tests/unit/test_reflexion.py`), but a future failure-marked test would pollute without the autouse safety net."

4. **Unify test line citations.** Use 02-test-fixtures §2's line numbers for all test references in the task file.

5. **Confirm Option C is the chosen path in synthesis Section 6 (Options).** Document the rejected Options A and B with the rationale from 02-test-fixtures §4.

6. **Mirror Example B (Track-4 PR4 from done/) phase skeleton.** 03-template-examples §4 confirms it is the exact-shape match. Two phase gates (after Discovery, after Verify).

---

## Final Verdict: **FAIL**

- 1 CRITICAL gap (env-var name contradiction) — must be resolved before synthesis
- 1 IMPORTANT gap (no baseline-cleanup procedure) — must be added to the task file
- 2 MINOR gaps (line-number drift; hook gating clarification) — nice-to-have

All other 7 checklist items PASS. Re-spawn this analyst after gaps 1 and 2 are addressed by either the team lead picking a canonical env-var name and inserting a baseline-cleanup phase, or by a targeted rf-researcher follow-up that updates 01-file-inventory and 02-test-fixtures to agree.

