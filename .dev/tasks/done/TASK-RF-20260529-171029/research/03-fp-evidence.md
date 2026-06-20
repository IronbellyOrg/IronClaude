# Research: FP Evidence at Specific Lines
**Topic type:** FP Evidence
**Scope:** .dev/releases/Current/MultiModelSwarm/roadmap.md (BareReview worktree)
**Status:** Complete
**Date:** 2026-05-29
---

## 1. Macro-Structure: H2 Milestone Map

Total file length: 611 lines.

| H2 Line | Title |
|---|---|
| 13 | Executive Summary |
| 33 | Milestone Summary |
| 48 | Dependency Graph |
| 62 | M1: Foundation & Domain Models |
| 119 | M2: Transport & Recipe Layers |
| 164 | M3: Lens Registry & Validator |
| 214 | M4: Wave 0 — Preflight |
| 253 | M5: Wave 1 — Parallel Dispatch |
| 294 | M6: Wave 2/3 — Normalize, Reduce, Merge |
| 335 | M7: CLI Surface, Observability, Resilience |
| 407 | M8a: IMM Invariant Test Suite |
| 439 | M8b: INV + Boundary Test Suite |
| 476 | M9: sc-bare-review Migration & A/B Parity |
| 507 | Resource Requirements and Dependencies |
| 533 | Risk Register |
| 556 | Success Criteria and Validation Approach |
| 579 | Decision Summary |
| 596 | Timeline Estimates |

Milestone bodies (H2 = `M{n}: ...`) span lines 62-506. Layer 5 only fires inside these.

## 2. H3 Subsection Inventory (grouped by H2)

**Note on subsection naming:** The roadmap uses these H3 patterns inside milestones:
- `### Integration Points — M{n}`
- `### Milestone Dependencies — M{n}`
- `### Open Questions — M{n}` (only some milestones)
- `### Risk Assessment and Mitigation — M{n}` (NOT "Risk Assessment Matrix")

The 4 demote-target subsection names per user: Risk Assessment / Integration Points / Milestone Dependencies / Open Questions. The actual H3 text begins with `Risk Assessment and Mitigation —`, so Layer 5's matcher must use prefix/substring matching, not exact equality.

### M1 (62-118)
- 91: Integration Points — M1
- 100: Milestone Dependencies — M1
- 104: Open Questions — M1
- 111: Risk Assessment and Mitigation — M1

### M2 (119-163)
- 139: Integration Points — M2
- 147: Milestone Dependencies — M2
- 151: Open Questions — M2
- 157: Risk Assessment and Mitigation — M2

### M3 (164-213)
- 188: Integration Points — M3
- 196: Milestone Dependencies — M3
- 200: Open Questions — M3
- 206: Risk Assessment and Mitigation — M3

### M4 (214-252)
- 233: Integration Points — M4
- 241: Milestone Dependencies — M4
- 245: Risk Assessment and Mitigation — M4
- (No Open Questions)

### M5 (253-293)
- 272: Integration Points — M5
- 281: Milestone Dependencies — M5
- 285: Risk Assessment and Mitigation — M5
- (No Open Questions)

### M6 (294-334)
- 315: Integration Points — M6
- 323: Milestone Dependencies — M6
- 327: Risk Assessment and Mitigation — M6

### M7 (335-406)
- 376: Integration Points — M7
- 385: Milestone Dependencies — M7
- 389: Open Questions — M7
- 397: Risk Assessment and Mitigation — M7

### M8a (407-438)
- 421: Integration Points — M8a
- 428: Milestone Dependencies — M8a
- 432: Risk Assessment and Mitigation — M8a

### M8b (439-475)
- 457: Integration Points — M8b
- 464: Milestone Dependencies — M8b
- 468: Risk Assessment and Mitigation — M8b

### M9 (476-506)
- 488: Integration Points — M9
- 495: Milestone Dependencies — M9
- 499: Risk Assessment and Mitigation — M9

---

## 3. Scaffold-Term Vocabulary (Ground Truth)

From `src/superclaude/cli/vocabulary.py` (SCAFFOLD_TERMS), the 11 regex patterns the scanner matches (case-insensitive, word-bounded via `\b`):

`mock(ed|s)?`, `stub(bed|s)?`, `skeleton`, `placeholder`, `scaffold(ing|ed)?`, `temporary`, `hardcoded`, `hardwired`, `no-?op`, `dummy`, `fake`

The scanner compiles these into `_SCAFFOLD_RE` and uses `finditer()` (obligation_scanner.py:170), so each occurrence on a line is a separate finding. Thus a single line with two `stub` occurrences yields 2 findings.

User-provided obligation IDs (DM-###, API-###, INV-###) are NOT scaffold terms — they are spec-token IDs. They do not trigger scaffold-term findings. (Discharge logic and constraint blocks reference them separately.)

---

## 4. Per-Line FP Evidence

### Line 145

**Literal line:**
```
|`openai_compat.py` httpx transport|Strategy implementation|Registered in M2 (alongside M1 stub)|M2|M5 (production dispatch)|
```

- **H3 (nearest above):** Line 139 — `### Integration Points — M2`
- **H2 milestone (nearest above):** Line 119 — `## M2: Transport & Recipe Layers`
- **Scaffold term hits:** 1 occurrence of `stub` (in phrase "alongside M1 stub")
- **FP count contribution:** 1
- **Demote-target match:** YES — H3 is "Integration Points"

---

### Line 149

**Literal line:**
```
- M1 (domain models for `DM-009`; `DM-010` interface; `COMP-018` package + stub).
```

- **H3 (nearest above):** Line 147 — `### Milestone Dependencies — M2`
- **H2 milestone (nearest above):** Line 119 — `## M2: Transport & Recipe Layers`
- **Scaffold term hits:** 1 occurrence of `stub` (in phrase "package + stub")
- **FP count contribution:** 1
- **Demote-target match:** YES — H3 is "Milestone Dependencies"

Note: Line 149 also contains DM-009, DM-010, COMP-018, but these are spec-token IDs, not scaffold terms — they do not fire findings. Only `stub` does.

---

### Line 278

**Literal line:**
```
|Transport `dispatch()` binding|Strategy selection|Bound from M2 transport per `transport.kind`|M5|M8a (stub-transport tests)|
```

- **H3 (nearest above):** Line 272 — `### Integration Points — M5`
- **H2 milestone (nearest above):** Line 253 — `## M5: Wave 1 — Parallel Dispatch`
- **Scaffold term hits:** 1 occurrence of `stub` (in compound "stub-transport"; regex `\bstub\b` matches at the word boundary before `-`)
- **FP count contribution:** 1
- **Demote-target match:** YES — H3 is "Integration Points"

---

### Line 425

**Literal line:**
```
|Stub transport fixture|Test DI/strategy|Bound from M1 stub for IMM tests in M8a|M8a|CI, M9 (parity harness reuse)|
```

- **H3 (nearest above):** Line 421 — `### Integration Points — M8a`
- **H2 milestone (nearest above):** Line 407 — `## M8a: IMM Invariant Test Suite`
- **Scaffold term hits:** 2 occurrences of `stub` ("Stub transport fixture" + "from M1 stub"). Case-insensitive match captures both.
- **FP count contribution:** 2
- **Demote-target match:** YES — H3 is "Integration Points"

---

### Line 437

**Literal line:**
```
|2|Stub transport drifts from real T2 proxy semantics|Medium|Low|Tests pass but production differs|Pin stub to documented OpenAI-compat response shape; periodic contract check against real proxy in M9|backend|
```

- **H3 (nearest above):** Line 432 — `### Risk Assessment and Mitigation — M8a`
- **H2 milestone (nearest above):** Line 407 — `## M8a: IMM Invariant Test Suite`
- **Scaffold term hits:** 2 occurrences of `stub` ("Stub transport drifts" + "Pin stub to documented")
- **FP count contribution:** 2
- **Demote-target match:** YES — H3 is "Risk Assessment and Mitigation" (matches "Risk Assessment" demote-target via prefix/substring)

---

### Line 474

**Literal line:**
```
|3|Parallel M8a/M8b coordination drift|Low|Low|Test infra duplication / shared fixtures conflict|Stub-transport + fixture directory layout finalized in M5; both halves consume same fixtures|qa|
```

- **H3 (nearest above):** Line 468 — `### Risk Assessment and Mitigation — M8b`
- **H2 milestone (nearest above):** Line 439 — `## M8b: INV + Boundary Test Suite`
- **Scaffold term hits:** 1 occurrence of `stub` (in "Stub-transport"; `\bstub\b` matches at the word boundary before the hyphen)
- **FP count contribution:** 1
- **Demote-target match:** YES — H3 is "Risk Assessment and Mitigation"

Note: "fixtures" is NOT in SCAFFOLD_TERMS, so it does not fire.

---

## 5. FP Count Reconciliation

| Line | H3 Subsection | Scaffold-term hits |
|---|---|---|
| 145 | Integration Points — M2 | 1 (stub) |
| 149 | Milestone Dependencies — M2 | 1 (stub) |
| 278 | Integration Points — M5 | 1 (stub) |
| 425 | Integration Points — M8a | 2 (Stub, stub) |
| 437 | Risk Assessment and Mitigation — M8a | 2 (Stub, stub) |
| 474 | Risk Assessment and Mitigation — M8b | 1 (Stub) |
| **Total** | | **8** |

**Confirmed:** 6 lines carry exactly 8 scaffold-term hits. The "8 emergent FPs" claim reconciles cleanly. Distribution: 4 lines with 1 hit each (145, 149, 278, 474) + 2 lines with 2 hits each (425, 437).

All 8 FPs are on the SAME scaffold term: `stub`. None of the other 10 SCAFFOLD_TERMS (mock, skeleton, placeholder, scaffold, temporary, hardcoded, hardwired, no-op, dummy, fake) fire on the 6 target lines.

Both lines with 2 hits are in M8a test-infrastructure context (Integration Points and Risk Assessment for the stub transport fixture), which is consistent with M8a's role as the IMM invariant test suite that exercises the stub transport.

---

## 6. Subsection-Name Cross-Check

User's 4 demote-target subsection names vs. actual H3 strings in roadmap:

| User-supplied name | Actual roadmap H3 text | Match strategy |
|---|---|---|
| Risk Assessment Matrix / Risk Assessment | `Risk Assessment and Mitigation — M{n}` | substring/prefix on "Risk Assessment" |
| Integration Points | `Integration Points — M{n}` | exact prefix |
| Milestone Dependencies | `Milestone Dependencies — M{n}` | exact prefix |
| Open Questions | `Open Questions — M{n}` | exact prefix |

**Implication for Layer 5 matcher:** The detector cannot use exact equality. It must:
- Strip the trailing ` — M{n}` decoration (em-dash + milestone tag), AND
- Use prefix or substring matching against canonical set `{"Integration Points", "Milestone Dependencies", "Open Questions", "Risk Assessment"}` (note: "Risk Assessment and Mitigation" starts with "Risk Assessment", so prefix matching on "Risk Assessment" works for that variant).

All 6 target lines fall under one of the 4 demote-target subsections. None fall under "Acceptance Criteria", "Objective", or any other H3.

---

## 7. Layer 5 Selectivity Concerns

**Question:** Are there any lines under the 4 demote-target subsections that contain GENUINE obligations (i.e., scaffold-term findings that should NOT be demoted)?

**Per-line audit (6 target lines):**
- Line 145: "alongside M1 stub" — meta-reference to a stub built in a prior milestone (M1). Not a new obligation. SAFE TO DEMOTE.
- Line 149: "package + stub" — describes the M1 deliverable (which was a stub by design per the prior-milestone spec). SAFE TO DEMOTE.
- Line 278: "stub-transport tests" — names the test category in Integration Points. SAFE TO DEMOTE.
- Line 425: "Stub transport fixture" / "from M1 stub" — names the test fixture and references prior-milestone artifact. SAFE TO DEMOTE.
- Line 437: Risk row about "Stub transport drifts" — meta-discussion of a test-infra risk; the mitigation references pinning the stub, not implementing a real one in this milestone. SAFE TO DEMOTE.
- Line 474: "Stub-transport + fixture directory layout" — test-infra coordination note in Risk Assessment. SAFE TO DEMOTE.

**General pattern:** Within Integration Points / Milestone Dependencies / Open Questions / Risk Assessment subsections, scaffold-term mentions are virtually always:
1. References to prior-milestone stubs being consumed (Integration Points, Milestone Dependencies)
2. Test-fixture names (Integration Points for test milestones M8a/M8b)
3. Meta-risks about test-stub fidelity (Risk Assessment)
4. Open architectural questions about stub semantics (Open Questions)

These are diagnostically distinct from milestone-body prose that says "the M{n} deliverable is a stub of X" (which IS a genuine HIGH obligation and should NOT be demoted). That prose lives in the milestone's Objective / Deliverables / Acceptance Criteria sections — H3s OUTSIDE the demote-target set — so Layer 5's subsection-based selectivity is well-grounded.

**Risk:** If a future roadmap author writes a genuine obligation inside one of the 4 demote-target subsections (e.g., places a deliverable description under "Integration Points" by mistake), Layer 5 would incorrectly demote it. Mitigation: this is a documentation-convention risk, not a Layer 5 design flaw; the schema for these 4 subsections is meta/reference-only by convention. Acceptable.

**No selectivity concerns identified** for the 6 target lines. Layer 5 as scoped is safe.

---
