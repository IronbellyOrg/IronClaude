# Research: Prompt & Tasklist Changes

| Field | Value |
|-------|-------|
| Topic | File Inventory + Patterns |
| Status | Complete |
| Date | 2026-04-02 |
| Researcher | researcher-04 |
| Scope | `src/superclaude/cli/roadmap/prompts.py`, `src/superclaude/cli/tasklist/prompts.py`, `src/superclaude/cli/tasklist/commands.py` |

---

## 1. Roadmap Prompt Builder Changes

All prompt builder functions in `src/superclaude/cli/roadmap/prompts.py`:

| # | Function | Has `tdd_file`? | Has `prd_file`? | TDD Block Summary | PRD Block Summary | Changed Since Prior E2E? |
|---|----------|----------------|----------------|-------------------|-------------------|--------------------------|
| 1 | `build_extract_prompt` (L82) | Yes (L160) | Yes (L182) | 6 enrichment items from TDD sections 7,8,10,15,19,25 | 5 enrichment items from PRD S19,S7,S12,S17,S6 + **authority language** | **YES** -- PRD authority language changed |
| 2 | `build_extract_prompt_tdd` (L208) | Yes (L334) | Yes (L354) | Cross-reference/consistency validation (5 items) | 5 enrichment items from PRD S19,S7,S12,S17,S6 + **authority language** | **YES** -- PRD authority language changed |
| 3 | `build_generate_prompt` (L380) | Yes (L436) | Yes (L465) | 6 TDD-specific roadmap generation enrichments | 4 PRD-driven phasing/sequencing/compliance/scope items | No |
| 4 | `build_diff_prompt` (L486) | No | No | N/A | N/A | No |
| 5 | `build_debate_prompt` (L511) | No | No | N/A | N/A | No |
| 6 | `build_score_prompt` (L538) | Yes (L565) | Yes (L579) | 3 TDD scoring dimensions (completeness, testing, migration) | 3 PRD scoring dimensions (business value, persona, compliance) | No |
| 7 | `build_merge_prompt` (L596) | Yes (L629) | Yes (L643) | 3 merge guidelines (identifiers, API contracts, TDD tasks) | 4 merge guidelines (personas, metrics, compliance, tie-breaking) | No |
| 8 | `build_spec_fidelity_prompt` (L661) | Yes (L714) | Yes (L750) | Dimensions 7-11 (API, Components, Testing, Migration, Ops) | Dimensions 12-15 (Persona, Metrics, Compliance, Scope) | No |
| 9 | `build_wiring_verification_prompt` (L772) | No | No | N/A | N/A | No |
| 10 | `build_test_strategy_prompt` (L830) | Yes (L877) | Yes (L900) | 6 TDD enrichment items (pyramid, cases, contract, data, migration, ops) | 5 PRD enrichment items (persona, journey, KPI, compliance, edge) | No |

**Total builders**: 10 in roadmap prompts. 6 accept `tdd_file`, 6 accept `prd_file`. 4 have neither (diff, debate, wiring_verification, and one extra: diff and debate both lack them).

Plus 2 tasklist builders (see section 3 below) = **12 total prompt builders across both files**.

---

## 2. PRD Authority Language Change

### What Changed

**Commit**: `a74cb83` (feat: add tech-reference skill, auto-detection task, E2E fixes)

**Diff**: `git diff a9cf7ee..a74cb83 -- src/superclaude/cli/roadmap/prompts.py`

**Old language** (2 locations):
```
"The PRD is advisory context for enrichment -- do NOT treat PRD content "
"as hard requirements unless they are also stated in the specification."
```

**New language** (2 locations):
```
"The PRD defines business requirements (personas, compliance, success metrics, scope). "
"Treat these as authoritative for business context. When PRD business requirements "
"conflict with the specification's technical approach, the specification wins on "
"implementation details but the PRD wins on business intent and constraints."
```

### Which Builders Were Changed

1. **`build_extract_prompt`** -- Lines 199-202 (PRD block for spec-primary extraction)
2. **`build_extract_prompt_tdd`** -- Lines 371-374 (PRD block for TDD-primary extraction)

Only these 2 builders had the old "advisory" language. The other 4 PRD-accepting builders (`build_generate_prompt`, `build_score_prompt`, `build_merge_prompt`, `build_test_strategy_prompt`) already used different phrasing (e.g., "business 'why' context", "inform roadmap prioritization") and were **not changed**.

### E2E Impact

**Phase 4 items 4.3 and 4.9**: These grep for PRD content in extraction output (persona names, compliance terms). The authority language change means the LLM may surface PRD content more prominently in extraction output. However, the E2E items grep for presence of content terms (Alex, Jordan, Sam, GDPR, SOC2), not for the prompt language itself. **No grep pattern update needed** -- the items check for outcome effects, not prompt wording.

**Phase 5 items 5.3 and 5.6**: Same pattern -- checking for PRD content presence, not prompt language. **No update needed**.

**Indirect impact**: The stronger authority language may cause the LLM to include MORE PRD-derived content in extraction output, making Phase 4/5 PRD enrichment checks more likely to pass (more persona/compliance content visible). This is a behavioral improvement, not a test breakage.

---

## 3. Tasklist Fidelity Changes

Source: `src/superclaude/cli/tasklist/prompts.py`, function `build_tasklist_fidelity_prompt` (L17-148)

### New TDD Fidelity Checks (Lines 123-126)

Added in commit `a74cb83`:

```python
"4. Data model entities from the TDD's Data Models section (§7) should have "
"corresponding schema implementation tasks in the tasklist.\n"
"5. API endpoints from the TDD's API Specifications section (§8) should have "
"corresponding endpoint implementation tasks in the tasklist.\n"
```

**Before**: TDD supplementary validation had 3 checks (test cases from §15, rollback from §19, components from §10).
**After**: TDD supplementary validation has 5 checks (+ data models from §7, API endpoints from §8).

### New PRD Fidelity Check (Lines 142-144)

Added in commit `a74cb83`:

```python
"4. Priority ordering from the PRD's Business Context (S5) -- task priority "
"should reflect business value hierarchy, not just technical dependency order. "
"Flag tasks where priority contradicts PRD stakeholder priorities as LOW severity.\n"
```

**Before**: PRD supplementary validation had 3 checks (persona coverage S7, success metrics S19, acceptance scenarios S12/S22).
**After**: PRD supplementary validation has 4 checks (+ priority ordering from S5, flagged as LOW severity unlike others which are MEDIUM).

### E2E Impact -- Phase 7

**Item 7.3** is the critical item. The E2E task currently says:
> Check for: (a) "Supplementary TDD Validation" section with **3 checks** (test cases from TDD S15, rollback from TDD S19, components from TDD S10), (b) "Supplementary PRD Validation" section with **3 checks** (persona coverage S7, success metrics S19, acceptance scenarios S12/S22)

**This is now STALE.** The correct expected counts are:
- TDD supplementary validation: **5 checks** (S15 test cases, S19 rollback, S10 components, **S7 data models**, **S8 API endpoints**)
- PRD supplementary validation: **4 checks** (S7 persona, S19 metrics, S12/S22 scenarios, **S5 priority ordering**)

**Item 6.2** has the same issue -- references "3 PRD validation checks" but should now be **4**.

### Items Requiring Update

| E2E Item | Current Text | Required Update |
|----------|-------------|-----------------|
| **6.2** | "3 PRD validation checks: persona coverage (S7), success metrics (S19), acceptance scenarios (S12/S22)" | Change to "4 PRD validation checks: persona coverage (S7), success metrics (S19), acceptance scenarios (S12/S22), **priority ordering (S5)**" |
| **7.3(a)** | "3 checks (test cases from TDD S15, rollback from TDD S19, components from TDD S10)" | Change to "5 checks (test cases from TDD S15, rollback from TDD S19, components from TDD S10, **data models from TDD S7, API endpoints from TDD S8**)" |
| **7.3(b)** | "3 checks (persona coverage S7, success metrics S19, acceptance scenarios S12/S22)" | Change to "4 checks (persona coverage S7, success metrics S19, acceptance scenarios S12/S22, **priority ordering S5**)" |

---

## 4. Tasklist Generate Prompt

### Function Exists: Yes

`build_tasklist_generate_prompt` at `src/superclaude/cli/tasklist/prompts.py` lines 151-237.

**Signature**: `build_tasklist_generate_prompt(roadmap_file: Path, tdd_file: Path | None = None, prd_file: Path | None = None) -> str`

**Enrichment scenarios supported**:
1. **No supplements** (L171-184): Baseline generation prompt from roadmap alone
2. **TDD-only** (L187-202): 5 enrichment items (S15 test cases, S8 API schemas, S10 components, S19 migration rollback, S7 data model fields)
3. **PRD-only** (L204-224): 5 enrichment items (S7 personas, S12/S22 acceptance, S19 metrics, S5 priorities, S12 scope boundaries) + note that PRD informs but doesn't generate standalone tasks
4. **Both TDD+PRD** (L227-235): Additional "TDD + PRD Interaction" block stating TDD provides engineering detail, PRD provides product context

### E2E Item 7.5

Item 7.5 tests this function directly via `uv run python -c ...` with all 4 scenarios. The test checks:
- `no_supplements`: 'Supplementary' not in result -- **correct** (baseline has no supplementary blocks)
- `tdd_only`: 'TDD' in result and 'PRD' not in result -- **correct**
- `prd_only`: 'PRD' in result and 'PRD context informs' in result -- **STALE**. The current code uses `"PRD context informs task descriptions"` (L223), so the substring `'PRD context informs'` **does match**. No update needed.
- `both`: 'TDD' in result and 'PRD' in result and 'When both TDD and PRD' in result -- **correct** (L228: "When both TDD and PRD are available")

**Item 7.5 does NOT need updating** -- all 4 checks still match the current code.

---

## 5. E2E Impact Assessment

### Phase 4 Items (Extraction Content)

| Item | Check | Impact | Update Needed? |
|------|-------|--------|----------------|
| 4.3 | Grep for persona names, GDPR/SOC2 in extraction | Authority language change may increase PRD content presence. Grep patterns still valid. | **No** |
| 4.5c | Grep for business value/persona/compliance in base-selection.md | Patterns unaffected by prompt changes | **No** |
| 4.6 | Grep for PRD business value in merged roadmap | Patterns unaffected | **No** |
| 4.9 | Grep for "source-document fidelity analyst" and dimensions 12-15 | Language still present at L677. Dimensions 12-15 unchanged. | **No** |

### Phase 5 Items (Spec-Fidelity Language)

| Item | Check | Impact | Update Needed? |
|------|-------|--------|----------------|
| 5.6 | "source-document fidelity analyst" language | Still present at `src/superclaude/cli/roadmap/prompts.py` L677 | **No** |
| 5.6 | Dimensions 12-15 for PRD | Unchanged in `build_spec_fidelity_prompt` (L755-767) | **No** |

### Phase 6 Items (Auto-Wire)

| Item | Check | Impact | Update Needed? |
|------|-------|--------|----------------|
| 6.2 | "3 PRD validation checks" | Now 4 checks (added S5 priority ordering) | **YES -- change to 4** |

### Phase 7 Items (Validation Enrichment)

| Item | Check | Impact | Update Needed? |
|------|-------|--------|----------------|
| 7.3(a) | "3 checks" for TDD supplementary | Now 5 checks (added S7 data models, S8 API endpoints) | **YES -- change to 5** |
| 7.3(b) | "3 checks" for PRD supplementary | Now 4 checks (added S5 priority ordering) | **YES -- change to 4** |
| 7.5 | Generate prompt function test | All 4 substring checks still valid | **No** |

### Pipeline Code Line Reference (L74-77 of E2E task)

The E2E task's "Pipeline Code" section at line 77 states:
> `build_tasklist_fidelity_prompt()` with PRD validation block (3 checks: S7, S19, S12/S22)

This should be updated to:
> `build_tasklist_fidelity_prompt()` with PRD validation block (**4 checks: S7, S19, S12/S22, S5**) and TDD validation block (**5 checks: S15, S19, S10, S7, S8**)

### Tasklist Commands File

`src/superclaude/cli/tasklist/commands.py` has `--tdd-file` and `--prd-file` flags (L61-72) with auto-wire logic from `.roadmap-state.json` (L113-159). These are unchanged in the recent commit -- the auto-wire logic and flag definitions were established in the prior PRD implementation commit (`a9cf7ee`). **No E2E impact from commands.py changes.**

---

## 6. Summary of Required E2E Task Updates

### Definite Updates (evidence-based, code changed)

1. **Item 6.2**: Change "3 PRD validation checks" to "4 PRD validation checks" and add "priority ordering (S5)" to the list.
2. **Item 7.3(a)**: Change "3 checks (test cases from TDD S15, rollback from TDD S19, components from TDD S10)" to "5 checks (test cases from TDD S15, rollback from TDD S19, components from TDD S10, data models from TDD S7, API endpoints from TDD S8)".
3. **Item 7.3(b)**: Change "3 checks (persona coverage S7, success metrics S19, acceptance scenarios S12/S22)" to "4 checks (persona coverage S7, success metrics S19, acceptance scenarios S12/S22, priority ordering S5)".
4. **Pipeline Code reference (L77)**: Update check counts from 3 to 4 (PRD) and mention 5 TDD checks.

### No Update Needed (verified stable)

- Phase 4 grep patterns (content-based, not prompt-wording-based)
- Phase 5 "source-document fidelity analyst" language (unchanged at L677)
- Phase 5 dimensions 12-15 (unchanged)
- Item 7.5 generate prompt function test (all substring checks still valid)
- `tasklist/commands.py` flags and auto-wire logic (unchanged since prior commit)
- All `_OUTPUT_FORMAT_BLOCK` references (unchanged)
