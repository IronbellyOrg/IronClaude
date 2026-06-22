# Research-Gate Verdict — FR-DRS TDD (Fix Cycle 1)

**Date:** 2026-06-21
**Phase:** Research gate, post-fix re-verification (fix cycle 1)
**Fix authorization:** TRUE
**Source findings:** `qa/qa-research-gate-consolidated-findings.md`
**Scope:** Apply ONLY the four `research-fix`-class fixes (C-1..C-4) to the research files.

---

## Fixes Applied (C-1..C-4)

### C-1 — File 01 stale header (MINOR)
- **File:** `research/01-runtime-surface-algorithm.md:3`
- **Before:** `**Status: In Progress**`
- **After:** `**Status: Complete**`
- **Rationale:** Header contradicted the footer (L281 already said Complete). Header was stale.
- **Status:** APPLIED ✅

### C-2 — File 03 missing status marker (MINOR)
- **File:** `research/03-consumer-surfaces.md` (header block, lines 1-9)
- **Before:** No top-level `Status:` field anywhere in the header.
- **After:** Inserted `**Status:** Complete` immediately under the H1 title (between the title and `**Investigation type:** Integration Mapper`).
- **Rationale:** File was substantively complete but lacked the status marker. NOT confused with the body's `TaskStatus` enum text (~L189-190), which is unrelated source content.
- **Status:** APPLIED ✅

### C-3 — File 01 §6 FR-RSR.7 citation re-anchored (MINOR)
- **File:** `research/01-runtime-surface-algorithm.md` §6 (Contract field discipline)
- **Before:** FR-RSR.7 forbidden-keys / contract-field-discipline content anchored to `SKILL:L491`.
- **After:** Re-anchored to `SKILL §9.1 MANDATORY EMISSION comment, SKILL.md:L721–L730`.
- **Edits made (3 sites carrying the FR-RSR.7 contract-field discipline):**
  1. L230 emit-fields directive: `(SKILL:L491)` → `(SKILL §9.1 MANDATORY EMISSION comment, SKILL.md:L721–L730)`
  2. L235 §6 section header: `(FR-RSR.7, SKILL:L491)` → `(FR-RSR.7, SKILL §9.1 MANDATORY EMISSION comment, SKILL.md:L721–L730)`
  3. L245 forbidden-keys line: `(SKILL:L491)` → `(SKILL §9.1 MANDATORY EMISSION comment, SKILL.md:L721–L730)`
- **Verification performed (zero-trust, read source directly):**
  - SKILL.md L489 = step 4b read-only production-caller sweep (NOT a forbidden-keys block).
  - SKILL.md L491 = the FR-RSR.7 contract-emission prose paragraph (prose, not the canonical contract-spec comment).
  - SKILL.md L721–L730 = the §9.1 `MANDATORY EMISSION (FR-RSR.7)` comment block — the canonical source that enumerates the six-field discipline and the forbidden improvised keys (`runtime_surface_reachable`, `reachability_path`, `static_caller_absent_is_expected`). Confirmed by reading SKILL.md 718-732.
- **Left intentionally unchanged:** L255 gap-analysis note cites `SKILL:L489/L491` as the literal locations where the "ALL SIX fields" assertion appears. That is an accurate provenance pointer for a different claim (a gap note about `refs/runtime-surface.md` enumerating only five field names), not the contract-field-discipline citation in scope for C-3. Left as-is to preserve correct provenance.
- **Status:** APPLIED ✅

### C-4 — File 04 grader.py line count (MINOR)
- **File:** `research/04-eval-path-integration.md:12`
- **Before:** `grader.py` (519 lines)
- **After:** `grader.py` (518 lines)
- **Verification performed:** `wc -l` on `.dev/eval-workspaces/sc-reflect/grader.py` = **518**. Confirmed only one occurrence of "519" in file 04 via grep.
- **Status:** APPLIED ✅

---

## Carry-Forward Items — INTENTIONALLY NOT EDITED (C-5..C-7)

The following are TDD-synthesis carry-forwards, NOT research-file edits. They were
**intentionally NOT touched** in this fix cycle. No research file was modified for any of them.

- **C-5** (MINOR, advisory) — file 04's honest flag that the `evals.json` → `eval_metadata.json`
  materializer is unverified (Option B dependency). Carry to TDD §15 as a noted dependency. **No research edit.**
- **C-6** (MINOR, advisory) — `grader.py:448-449` `target`-prefix routing fragility (a future
  non-`target` FR-RSR assertion would be silently dropped). Carry to TDD §15: oracle assertions
  MUST carry a `target` key. **No research edit.**
- **C-7** (IMPORTANT, defer) — DG-1: OQ-DRS.2 invocation-site decision left as weighable options
  without a ratified recommendation. Already handled by synth-03/synth-09 item instructions to present
  the decision WITH a recommendation in §6.4/§21/§22. **No research edit.**

(C-8 was an operational artifact issue — rf-qa Partition-A report persistence — already resolved
upstream; no action required here.)

---

## Verification Summary

| ID | Class | Action | Result |
|----|-------|--------|--------|
| C-1 | research-fix | Header → Complete | APPLIED |
| C-2 | research-fix | Added Status: Complete | APPLIED |
| C-3 | research-fix | Re-anchored 3 FR-RSR.7 citations to SKILL.md §9.1 L721–L730 | APPLIED |
| C-4 | research-fix | 519 → 518 (verified wc -l = 518) | APPLIED |
| C-5 | tdd-note | (not a research edit) | DEFERRED to TDD §15 |
| C-6 | tdd-note | (not a research edit) | DEFERRED to TDD §15 |
| C-7 | tdd-decision | (not a research edit) | DEFERRED to synth §6.4/§21/§22 |

- Research-fix items resolved: 4 / 4
- Research files modified: 3 (`01-runtime-surface-algorithm.md`, `03-consumer-surfaces.md`, `04-eval-path-integration.md`)
- Carry-forward items left untouched: 3 (C-5, C-6, C-7)
- All edits surgical (Edit tool, no whole-file rewrites).

## Post-Fix Verification (Step 3.9, two independent verifiers)

Two verification subagents (fix_authorization: false) independently re-checked the fixes against source:

- **Structural (rf-qa)** → **PASS** (6/6 checks). C-1: header now `Status: Complete`, no "In Progress"
  remains. C-2: exactly one `Status:` marker, correctly placed. C-3: 3 citations re-anchored to §9.1
  L721-730; forbidden keys confirmed verbatim at SKILL.md:723-724; unrelated L465-491 algorithm-span
  citations correctly left intact. C-4: `wc -l grader.py` = 518 confirmed, no stray "519". No content
  corruption; all 4 files parse as well-formed markdown. (One out-of-scope advisory noted: file 04's
  `evals.json (1134 lines)` uses editor-line vs `wc -l`=1133 — pre-existing, not in scope, affects no
  line-range citation.)
- **Content (rf-qa-qualitative)** → **PASS** (7/7 checks). C-3 re-anchor is SEMANTICALLY correct (the
  FR-RSR.7 forbidden-keys/contract-emission discipline genuinely lives at §9.1 L721-730; L491 is forward-
  referencing prose). C-5/C-6/C-7 confirmed NOT prematurely resolved in the research files (honesty flags
  intact; OQ-DRS.2 still deferred to TDD). The four fixes changed no substantive technical claim.

Both verifiers PASS → research gate cleared. Proceeding to Phase 4.

RESEARCH GATE: CLEARED → **PASS** (fix cycle 1; verified by 2 independent agents)
