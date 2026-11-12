# Editorial Review - Structure: prd.md

## Document Summary
- **Purpose:** PRD stating what the Orca read-only terminal observer must do per release and how each release is judged done
- **Audience:** the owner (gates, open questions), the UX and architecture steps, step-5 reviewers
- **Reader type:** humans (and downstream agents)
- **Structure model:** Strategic/Context (Pyramid)
- **Current length:** 8777 words across 14 top-level sections (§0-§13), 24 subsections

Section map (words): §0 180, §1 156, §2 579, §3 353, §4 785, §5 2059, §6 782, §7 175, §8 141, §9 765, §10 577, §11 451, §12 1043, §13 644.

## Recommendations

### 1. MOVE - Current status into §0
**Rationale:** The headline status (DIRECTION-SELECTED NOT passed; only offline R0 work allowed today) first appears in §4 and §8 line 295; a Pyramid document states it at the top.
**Impact:** ~+25 words (one sentence restated from §8, which stays)
**Comprehension note:** improves the first-screen answer for the owner.

### 2. CONDENSE - §7 production-code bullet
**Rationale:** The I:91 quote and the "offline R0 only" rule are stated in full in §4 (Production-integration boundary); §7 repeats both verbatim.
**Impact:** ~-25 words (replace with a pointer to §4)

### 3. PRESERVE - Issue user story in §2.1
**Rationale:** It overlaps JTBD-1 to JTBD-6 (rubric minor), but it is the issue's own wording and anchors traceability to I:15.
**Impact:** 0 words

### 4. PRESERVE - §8 Release 1 Scope alongside the §4 R1 row
**Rationale:** The brief requires an explicit R1 scope; §8 maps scope to FR ids, the §4 row maps it to gates. Different jobs.
**Impact:** 0 words

### 5. QUESTION - §12.1 open questions vs §12.3 open owner decisions
**Rationale:** Some owner decisions in §12.3 overlap OQs in §12.1, but §12.1 must stay verbatim from SPEC.md and §12.3 carries the spec's recommendations; merging would rewrite carried wording. Left for the owner.
**Impact:** 0 words now (possible ~-200 if the owner allows a cross-reference)

### 6. PRESERVE - §5 Features length (2059 words)
**Rationale:** Largest section, but each FR carries its pinned strings and test ids; moving them to the addendum would split the single place UX reads requirements. Technical detail already lives in the spec companions.
**Impact:** 0 words

## Summary
- **Total recommendations:** 6 (2 applied: #1, #2; 3 PRESERVE; 1 QUESTION left open)
- **Estimated reduction:** ~0 words net (0% of original)
- **Meets length target:** No target specified
- **Comprehension trade-offs:** none

addendum.md (53 lines): no substantive changes recommended; document structure is sound.
