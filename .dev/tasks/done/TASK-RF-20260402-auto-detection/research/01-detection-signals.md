# Detection Signal Analysis: PRD vs TDD vs Spec Three-Way Classification

**Researcher**: researcher-1
**Date**: 2026-04-01
**Track Goal**: Add PRD detection to `detect_input_type()` for auto-classification
**Status**: COMPLETE

---

## 1. Source Materials Analyzed

| Artifact | Path | Lines | Type |
|----------|------|-------|------|
| PRD fixture | `.dev/test-fixtures/test-prd-user-auth.md` | 406 | Real PRD |
| TDD fixture | `.dev/test-fixtures/test-tdd-user-auth.md` | 876 | Real TDD |
| Spec fixture | `.dev/test-fixtures/test-spec-user-auth.md` | 312 | Real spec |
| TDD template | `src/superclaude/examples/tdd_template.md` | ~1273 | Template |
| Spec template | `src/superclaude/examples/release-spec-template.md` | 265 | Template |
| Current detection | `src/superclaude/cli/roadmap/executor.py` lines 63-133 | 71 | Code |

---

## 2. Frontmatter Field Comparison Matrix

| Field | PRD | TDD | Spec | Exclusive To |
|-------|-----|-----|------|-------------|
| `id` | `AUTH-PRD-001` | `AUTH-001-TDD` | -- | PRD+TDD |
| `title` | "...Product Requirements Document (PRD)" | "...Technical Design Document" | "User Authentication Service" | -- |
| `type` | `"Product Requirements"` | `"Technical Design Document"` | -- (absent) | **PRD** (`"Product Requirements"`) / **TDD** |
| `coordinator` | `"product-manager"` | `"test-lead"` | -- | PRD+TDD (shared) |
| `parent_doc` | -- (absent) | `"AUTH-PRD-001"` | -- | **TDD exclusive** |
| `parent_task` | `""` (present, empty) | -- (absent) | -- | **PRD exclusive** |
| `assigned_to` | `"product-team"` | `"auth-team"` | -- | PRD+TDD |
| `feature_id` | -- (absent) | `"AUTH-001"` | `AUTH-001` | TDD+Spec |
| `spec_type` | -- (absent) | `"new_feature"` | `new_feature` | TDD+Spec |
| `complexity_score` | -- | present | `0.6` | TDD+Spec |
| `authors` | -- (absent) | present | present | TDD+Spec |
| `quality_scores` | -- (absent) | present | present | TDD+Spec |
| `tags` | `[prd, requirements, ...]` | `[technical-design-document, ...]` | -- (absent) | PRD+TDD |
| `related_docs` | present | present | -- | PRD+TDD |
| `autogen` | present | present | -- | PRD+TDD |
| `approvers` (nested) | -- | present | -- | **TDD exclusive** |
| `review_info` (nested) | -- | present | -- | **TDD exclusive** |

**Key finding**: The `type` frontmatter field is the strongest single discriminator. PRDs have `"Product Requirements"`, TDDs have `"Technical Design Document"`, and specs lack this field entirely.

---

## 3. Section Heading Comparison

### 3.1 Numbered Headings (## N. pattern)

| Document | Count | Score (current algo) |
|----------|-------|---------------------|
| PRD | **0** | +0 |
| TDD | **28** | +3 |
| Spec | **12** | +1 |

PRDs use **unnumbered** section headings. This is a strong negative signal for TDD and a neutral signal for PRD vs spec.

### 3.2 PRD-Exclusive Section Headings (## level)

These headings appear ONLY in the PRD fixture and NOT in TDD or spec:

| Heading | PRD | TDD | Spec |
|---------|-----|-----|------|
| `User Personas` | 1 | 0 | 0 |
| `Jobs To Be Done` | 1 | 0 | 0 |
| `Product Vision` | 1 | 0 | 0 |
| `Customer Journey Map` | 1 | 0 | 0 |
| `Value Proposition Canvas` | 1 | 0 | 0 |
| `Competitive Analysis` | 1 | 0 | 0 |
| `User Stories` | 1 | 0 | 0 |
| `User Experience Requirements` | 1 | 0 | 0 |
| `Legal and Compliance` | 1 | 0 | 0 |
| `Success Metrics and Measurement` | 1 | 0 | 0 |
| `Maintenance and Ownership` | 1 | 0 | 0 |
| `Background and Strategic Fit` | 1 | 0 | 0 |

**12 PRD-exclusive section headings** identified. A typical PRD will match at least 5-8 of these.

### 3.3 TDD-Exclusive Section Headings (existing in detection code)

| Heading | PRD | TDD | Spec |
|---------|-----|-----|------|
| `Data Models` | 0 | 1 | 0 |
| `API Specifications` | 0 | 1 | 0 |
| `Component Inventory` | 0 | 1 | 0 |
| `Testing Strategy` | 0 | 1 | 0 |
| `Operational Readiness` | 0 | 1 | 0 |
| `State Management` | 0 | 1 | 0 |
| `Performance Budgets` | 0 | 1 | 0 |
| `Accessibility Requirements` | 0 | 1 | 0 |

Zero overlap between PRD sections and TDD sections -- no false-positive risk.

### 3.4 Shared Sections (appear in multiple types)

| Heading | PRD | TDD | Spec |
|---------|-----|-----|------|
| `Executive Summary` | 1 | 1 | 0 |
| `Problem Statement` | 1 | 1 | 1 |
| `Dependencies` | 1 | 1 | 0 |
| `Error Handling` (partial) | 1 | 1 | 0 |
| `Risk` (various forms) | 1 | 1 | 1 |

These shared sections provide NO discriminative value.

---

## 4. Unique Keyword/Phrase Signals

### 4.1 PRD-Exclusive Keywords

| Signal | PRD Count | TDD Count | Spec Count | Notes |
|--------|-----------|-----------|------------|-------|
| `"Product Requirements"` (in frontmatter type or body) | 3 | 0 | 0 | Strongest single signal |
| `"As .* I want"` (user story pattern) | 8 | 0 | 0 | Very strong -- unique to PRDs |
| `"When I .* I want to"` (JTBD pattern) | 5 | 0 | 0 | Strong -- JTBD is PRD-only |
| `Product Owner` | 1 | 0 | 0 | |
| `Product Type` | 1 | 0 | 0 | |
| `Stakeholders` (as heading/field) | 1 | 0 | 0 | |
| Tag: `prd` | 1 | 0 | 0 | Present in `tags:` array |
| Tag: `requirements` | 1 | 0 | 0 | Present in `tags:` array |
| Tag: `user-stories` | 1 | 0 | 0 | Present in `tags:` array |
| Tag: `acceptance-criteria` | 1 | 0 | 0 | Present in `tags:` array |

### 4.2 Ambiguous Signals (present in PRD + TDD but not spec)

| Signal | PRD | TDD | Spec | Verdict |
|--------|-----|-----|------|---------|
| `Business Context` | 1 | 1 | 0 | Do NOT use for PRD detection |
| `Epics` | 1 | 1 | 0 | Do NOT use for PRD detection |
| `coordinator:` | 1 | 1 | 0 | Already used for TDD; shared |

---

## 5. Tag Analysis

| Tag | PRD | TDD | Spec |
|-----|-----|-----|------|
| `prd` | YES | no | -- |
| `requirements` | YES | no | -- |
| `user-stories` | YES | no | -- |
| `acceptance-criteria` | YES | no | -- |
| `technical-design-document` | no | YES | -- |
| `architecture` | no | YES | -- |
| `specifications` | no | YES | -- |

Spec fixture has **no tags field at all**. Tags are a strong discriminator between PRD and TDD but not useful for spec detection.

---

## 6. Proposed PRD Detection Signals with Weights

Modeled after the existing TDD detection pattern in `executor.py` lines 63-133.

### Signal 1: Frontmatter `type` field contains "Product Requirements" (weight: +3)

```python
if "Product Requirements" in content[:1000]:
    prd_score += 3
```

**Rationale**: The `type:` frontmatter field is the single strongest discriminator. Present in PRD fixture line 7: `type: "Product Requirements"`. Absent from TDD (`"Technical Design Document"`) and spec (no `type` field). Checking first 1000 chars limits to frontmatter.

### Signal 2: PRD-exclusive section headings (weight: +1 each, 12 candidates)

```python
prd_sections = [
    "User Personas", "Jobs To Be Done", "Product Vision",
    "Customer Journey", "Value Proposition", "Competitive Analysis",
    "User Stories", "User Experience Requirements",
    "Legal and Compliance", "Success Metrics and Measurement",
    "Maintenance and Ownership", "Background and Strategic Fit",
]
for section in prd_sections:
    if section in content:
        prd_score += 1
```

**Rationale**: 12 PRD-exclusive headings. A real PRD matches 5-12 of these. TDD matches 0. Spec matches 0. The PRD fixture matches all 12.

### Signal 3: User story pattern "As .*, I want" (weight: +2)

```python
if re.search(r"As .+, I want", content):
    prd_score += 2
```

**Rationale**: User stories are definitional to PRDs. The PRD fixture has 8 matches. TDD has 0. Spec has 0. Using presence (not count) keeps it simple.

### Signal 4: JTBD pattern "When I .* I want to" (weight: +2)

```python
if re.search(r"When I .+ I want to", content):
    prd_score += 2
```

**Rationale**: Jobs-To-Be-Done is exclusively a PRD artifact. 5 matches in PRD fixture, 0 in TDD, 0 in spec.

### Signal 5: PRD tag in frontmatter (weight: +2)

```python
if re.search(r"tags:.*\bprd\b", content[:2000]):
    prd_score += 2
```

**Rationale**: The `prd` tag in the tags array is explicit type declaration. Present in PRD fixture line 17. Absent from TDD and spec.

---

## 7. Proposed PRD Detection Threshold

**Threshold: prd_score >= 5 means "prd"**

This matches the existing TDD threshold symmetry.

**Maximum possible PRD score**: 3 (type field) + 12 (section headings) + 2 (user stories) + 2 (JTBD) + 2 (prd tag) = **21**

---

## 8. Verification: Would proposed detection correctly classify all 3 fixtures?

### 8.1 PRD fixture (`test-prd-user-auth.md`)

| Signal | Match? | Score |
|--------|--------|-------|
| `"Product Requirements"` in first 1000 chars | YES (line 7) | +3 |
| PRD section headings | 12/12 match | +12 |
| `"As .*, I want"` pattern | YES (8 instances) | +2 |
| `"When I .* I want to"` pattern | YES (5 instances) | +2 |
| `prd` tag | YES (line 17) | +2 |
| **PRD TOTAL** | | **21** |
| **TDD score (existing algo)** | coordinator=+2, rest=0 | **2** |

**Result**: PRD score 21 >= 5 -> classified as **"prd"** (CORRECT)
TDD score 2 < 5 -> would not be classified as TDD. No conflict.

### 8.2 TDD fixture (`test-tdd-user-auth.md`)

| Signal | Match? | Score |
|--------|--------|-------|
| `"Product Requirements"` in first 1000 chars | NO | +0 |
| PRD section headings | 0/12 match | +0 |
| `"As .*, I want"` pattern | NO | +0 |
| `"When I .* I want to"` pattern | NO | +0 |
| `prd` tag | NO | +0 |
| **PRD TOTAL** | | **0** |
| **TDD score (existing algo)** | 28 headings(+3) + coordinator(+2) + parent_doc(+2) + 8 sections(+8) + type(+2) | **17** |

**Result**: PRD score 0 < 5 -> NOT classified as PRD. TDD score 17 >= 5 -> classified as **"tdd"** (CORRECT)

### 8.3 Spec fixture (`test-spec-user-auth.md`)

| Signal | Match? | Score |
|--------|--------|-------|
| `"Product Requirements"` in first 1000 chars | NO | +0 |
| PRD section headings | 0/12 match | +0 |
| `"As .*, I want"` pattern | NO | +0 |
| `"When I .* I want to"` pattern | NO | +0 |
| `prd` tag | NO (no tags field) | +0 |
| **PRD TOTAL** | | **0** |
| **TDD score (existing algo)** | 12 headings(+1) + no exclusive fields(+0) + 0 sections(+0) + no type(+0) | **1** |

**Result**: PRD score 0 < 5 -> NOT classified as PRD. TDD score 1 < 5 -> NOT classified as TDD. Falls through to **"spec"** (CORRECT)

---

## 9. Verification: No false positives from PRD signals on existing TDD detection

The PRD detection signals are **completely disjoint** from TDD detection signals:

| PRD Signal | Overlap with TDD signals? |
|------------|--------------------------|
| `"Product Requirements"` | No -- TDD checks `"Technical Design Document"` |
| PRD section headings (12) | No -- zero overlap with TDD's 8 section keywords |
| User story pattern | No -- not checked in TDD detection |
| JTBD pattern | No -- not checked in TDD detection |
| `prd` tag | No -- TDD checks `parent_doc` and `coordinator` |

**The PRD `coordinator` field** is worth noting: it exists in the PRD fixture (`coordinator: "product-manager"`) and contributes +2 to the TDD score. However, the PRD's total TDD score is only 2 (well below threshold 5), so this does not cause a false positive. No change to the existing TDD detection is needed.

---

## 10. Proposed Classification Algorithm

The detection should run PRD scoring first, then TDD scoring, with spec as the fallback:

```python
def detect_input_type(spec_file: Path) -> str:
    content = spec_file.read_text(...)

    # --- PRD scoring ---
    prd_score = 0
    if "Product Requirements" in content[:1000]:
        prd_score += 3
    prd_sections = [
        "User Personas", "Jobs To Be Done", "Product Vision",
        "Customer Journey", "Value Proposition", "Competitive Analysis",
        "User Stories", "User Experience Requirements",
        "Legal and Compliance", "Success Metrics and Measurement",
        "Maintenance and Ownership", "Background and Strategic Fit",
    ]
    for section in prd_sections:
        if section in content:
            prd_score += 1
    if re.search(r"As .+, I want", content):
        prd_score += 2
    if re.search(r"When I .+ I want to", content):
        prd_score += 2
    if re.search(r"tags:.*\bprd\b", content[:2000]):
        prd_score += 2

    if prd_score >= 5:
        return "prd"

    # --- TDD scoring (existing, unchanged) ---
    tdd_score = 0
    # ... (existing code) ...
    if tdd_score >= 5:
        return "tdd"

    return "spec"
```

**Order matters**: PRD check runs first because a PRD with a `coordinator:` field could get +2 on the TDD score, but its TDD score will never reach 5. Running PRD first is cleaner and avoids any edge-case accumulation.

---

## 11. Edge Cases and Robustness Notes

1. **PRD without `type` field**: If a PRD omits the `type:` frontmatter field, it would lose 3 points. But 5+ PRD section headings (+5) plus user stories (+2) still reach threshold 7 >= 5.

2. **Minimal PRD** (only 3-4 section headings, no user stories): Would score ~3-4 and fall to "spec". This is acceptable -- minimal PRDs that lack standard PRD structure should be manually classified with `--input-type prd`.

3. **PRD with numbered headings**: If a PRD author numbers their sections, the TDD score could rise. But without TDD-exclusive fields (`parent_doc`) or TDD section names, the TDD score would still be well below 5.

4. **`coordinator:` in PRD**: Already analyzed. Contributes +2 to TDD score but TDD total stays at 2. Not a problem.

---

## 12. Summary

| Document Type | Key Discriminators | Score Range | Threshold |
|---------------|-------------------|-------------|-----------|
| **PRD** | `type: "Product Requirements"`, PRD section headings (12), user story patterns, JTBD patterns, `prd` tag | 0-21 | >= 5 |
| **TDD** | Numbered headings (28), `parent_doc`/`coordinator`, TDD section names (8), `type: "Technical Design Document"` | 0-17 | >= 5 |
| **Spec** | Fallback when neither PRD nor TDD threshold met | N/A | default |

All 3 test fixtures are correctly classified by the proposed algorithm. No false positives between PRD and TDD detection. The spec correctly falls through as default.
