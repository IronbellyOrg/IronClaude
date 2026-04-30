# Consolidated Structural Findings — Phase 5 Gate 2 (Cycle 1 of max 2)

**Date:** 2026-04-30
**Cycle:** 1 of 2
**Source lens reports:** qa-structural-lens-{1..6}-*.md

## Overall Verdict: FAIL

5 of 6 lens reports FAIL; only Lens 5 (Domain-Accuracy) PASSES. Cycle 1 must run fix agent.

| Lens | Verdict | Critical | Important | Minor |
|---|---|---|---|---|
| 1 Template-Conformance | FAIL | 0 | 3 | 1 |
| 2 Internal-Consistency | FAIL | 2 | 4 | 0 |
| 3 Evidence-Quality | FAIL | 1 | 2 | 1 |
| 4 Actionability | FAIL | 0 | 2 | 2 |
| 5 Domain-Accuracy | PASS | 0 | 0 | 0 |
| 6 Section-Classification | FAIL | 3 | 4 | 2 |
| **Total** | — | **6** | **15** | **6** |

## Deduplicated Unique Findings (priority-ordered)

### CRITICAL (fix-priority TOP — block Phase 6 if unresolved)

| ID | Issue | Affected Section | Source Lens | Suggested Fix |
|---|---|---|---|---|
| C1 | **Section numbering inconsistency** — S1-S20 use unnumbered headers; S21-S29 use numbered (`## 21.` ... `## 29.`). Skill's own SECTION_COUNT_29 self-check (S25.3 line 1661) requires 29 numbered headers; only 9 present. | Lines 6-1413 (S1-S20), S25.3 line 1651 | L1, L2, L6 | Add canonical `## N. SectionName` numbered headers to S1-S20 OR update S25.3 SECTION_COUNT_29 check to count headers without numeric prefix. Recommend numbering S1-S20 to match canonical 29-section schema. |
| C2 | **Missing S18 (A.8 Receive & Verify Task File)** classified COPY but absent. Tech-research has A.8 at L450-461. Persona-research jumps from A.7 (line 513) to Stage B (line 515). | Between line 513 and 515 | L2 | Insert A.8 block from tech-research/SKILL.md L450-461 verbatim, with persona-research-specific verification points (Phase 1 ethics-attestation item, §5.2 worker JSON contract embedded in Phase 4). |
| C3 | **Citation to non-existent research file** — `09-spec-part3-ethics-archetype-schema.md` does not exist; actual filename is `09-spec-part3-ethics-acceptance-archetype-schema.md`. Spec FR Coverage QA prompt directs an agent to read this file → agent will fail. | SKILL.md:1352 | L3 | Rename citation to match actual filename. |
| C4 | **Archetype folder name conflict** — three different names used: `archetypes/` (S4 line 46, S9 line 176, S2 folder-creation line 335), `archetype-proposals/` (S20 Discovery Worker line 865, S28 line 1820), and `archetype_store.local_path` (Aggregator line 982). Runtime task folder will use one name; the other set of references will dangle. | Lines 46, 176, 335 vs 606, 865, 964, 982, 1805, 1820 | L3, L6 | Standardize on one canonical name (recommend `archetype-proposals/` since used in worker output paths). Update all references uniformly across S4, S9, S20, S28. |
| C5 | **Aggregator folder name conflict** — S4 declares `synthesis/`; S20 Aggregator (lines 956-957) writes to `aggregation/`. Folder not declared in S4 Variable Reference. | S4 line 41, S9 line 171, S20 lines 956-957 | L6 | Pick one folder name and use uniformly across S4, S9, S20. |
| C6 | **Agent roster mismatch S14↔S20** — S14 lists "Approval Gate" as agent type; S20 has "Archetype Matcher" prompt instead. Approval Gate is a halt phase, not a spawned agent. | S14 line 312-319, S20 lines 620, 693, 736, 858, 950, 1018 | L6 | Add Archetype Matcher to S14 agent table; remove Approval Gate from agent roster (clarify it's a phase). |

### IMPORTANT (fix-priority HIGH — should resolve)

| ID | Issue | Affected Section | Source Lens | Suggested Fix |
|---|---|---|---|---|
| I1 | S19 header has suffix `(Delegation Protocol)` not in tech-research line 465; line 517 inserts preamble paragraph not in tech-research. Violates COPY contract. | Line 515, 517 | L2 | Remove `(Delegation Protocol)` suffix; remove or relocate preamble at line 517. |
| I2 | S16 (A.5) classified COPY but content is persona-research-specific (SUBJECT_ROSTER, ETHICS_ATTESTATION, Guard G1/G4) — SUBSTITUTE-grade mislabeled COPY. | Lines 390-412 | L2, L6 | Reclassify S16 as SUBSTITUTE in 12-section-classification.md (matches reality). |
| I3 | "(per skill-creator architecture):" — bare reference-skill noun in body prose of §10 (GENERATE). | Line 218 | L2 | Replace with citation form: "(per RF 3-gate QA architecture)". |
| I4 | No `allowed-tools` field in frontmatter. Critical Rule 14 calls for tightly-scoped allowed-tools. | Frontmatter lines 1-4 | L1, L2 | Add `allowed-tools: [Read, Write, Edit, Glob, Grep, Bash, Task, WebFetch, WebSearch]`. |
| I5 | S25.3 SECTION_COUNT_29 self-check unsatisfiable given current structure. | S25.3 line 1651 | L1 | Resolved by C1 (numbering S1-S20). |
| I6 | S21.1 schema block lists `## 1.` through `## 29.` but document doesn't have those literal headers. | Lines 1419-1457 | L1 | Revise schema to match actual section names OR clarify schema is logical mapping. |
| I7 | Citation to non-existent `02-tech-research-analysis.md`; actual file is `02-reference-tech-research.md`. | SKILL.md:1498-1499 | L3 | Replace with `02-reference-tech-research.md`. |
| I8 | Documentation-staleness tagging defined (S23 #12, S26 Rule 5) but not applied. Hundreds of FR citations as bare "(FR-8)". | Body throughout | L3 | Add explicit S26 exception that "(FR-N)" parenthetical citation subsumes [SPEC-FR-N] tag (less invasive than retagging hundreds of citations). |
| I9 | NO_FIRST_PERSON_ATTRIBUTION uses `<Name>` meta-placeholder, not runnable regex. | S25.3 line 1655, S25.2 FR-7 line 1628, S27 Rule 25 line 1788 | L4 | Replace with concrete regex: `grep -nE '\b[A-Z][a-z]+ (said\|stated\|wrote\|tweeted)\s+["“]'`. |
| I10 | ARCHETYPE_GENERIC_PURITY described in S25 but linter not encoded as runnable rule list. Discovery Worker prompt (L916-921) has it. | S25.3 line 1656 | L4 | Add sub-checklist of grep rules under §25.3 mirroring L916-921 OR cross-reference Discovery Worker prompt. |
| I11 | L-level mapping disagreement: document encodes L0/L1/L1/L4/L2/L0/L4; checklist expected L0/L1/L4/L2/L4/L6/L0. | S10 lines 209-216, A.7 lines 451-460 | L6 | Document's L-levels are internally consistent (S10↔A.7) — accept as-is OR resolve with orchestrator. Recommend update document to match expected L-level mapping (Phase 4 already at L4; ensure Phase 5 = L4, Phase 6 = L6). |
| I12 | Critical Rule 3 (line 1740) references "Phase 7 agent-creator nests" — leftover skill-creator boilerplate. Phase 7 in this skill is "Optional Validator". | Line 1740 | L6 | Remove agent-creator reference from Rule 3; replace with Validator-specific guidance. |
| I13 | S20 Identity Verifier output schema includes `ethics_screen` field; §5.2 worker contract `identity_verification` block omits it. | S20 line 691 vs S20 lines 808-847 | L6 | Add `ethics_screen` to §5.2 `identity_verification` block. |
| I14 | S26 row 6 ("Don't fabricate") borderline boilerplate-vs-domain. Strict count of unambiguous domain rows is exactly 4 — meets floor with no margin. | S26 row 6 | L4 | Add 11th row covering FR-25 Tavily routing or FR-8 no-auto-write for margin. |
| I15 | S25.3 ETHICS_DISCLAIMER_VERBATIM count = exactly 3 — tight; future deletion would break check. | S25.3 line 1654 | L6 | Make locations explicit (cite line numbers in check) or relax threshold to "≥2". |

### MINOR (fix-priority LOW)

| ID | Issue | Affected Section | Suggested Fix |
|---|---|---|---|
| M1 | "spec §3, lines 80-156" — actual schema content L80-114. | SKILL.md:56 | Tighten to "lines 80-114". |
| M2 | S6 "Don't fabricate" rule could reference FR-11 INSUFFICIENT_PUBLIC_DATA sentinel. | S26 row 6 | Optional reframe. |
| M3 | S21.1 schema block self-contradiction (lists `## 1.` through `## 29.` not matching doc). | Lines 1419-1457 | Resolved by C1 + I6. |
| M4 | Frontmatter `allowed-tools` (also tracked as I4). | Frontmatter | Resolved by I4. |
| M5 | Some persona-research customizations within COPY-classified S19 body. | S19 lines 545, 550 | Consider classifying these passages as substitution-allowed. |

## Fix-Priority List (CRITICAL → IMPORTANT → MINOR)

1. **C1** Renumber S1-S20 sections (or update SECTION_COUNT_29 check) — UNBLOCKS L1/L2/L6 findings
2. **C2** Insert S18 (A.8) section
3. **C3** Fix `09-spec-part3-ethics-archetype-schema.md` citation
4. **C4** Standardize archetype folder name → `archetype-proposals/`
5. **C5** Standardize aggregator folder name → `synthesis/` or `aggregation/`
6. **C6** Reconcile S14↔S20 agent rosters
7. **I1-I15** as listed above
8. **M1-M5** as time permits

## Cycle Counter

**Cycle 1 of max 2** (Gate 2 — Structural+Qualitative QA).

## Verdict

**FAIL — proceed to Step 5.3 (fix agent) — Cycle 1.**
