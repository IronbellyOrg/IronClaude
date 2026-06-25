# QA Report — Phase 6 (P5) Fix-Cycle Content Verification

**Topic:** P5 Tier Calibration Advisory — fix-cycle re-verification (Step 6.G9)
**Date:** 2026-06-19
**Phase:** fix-cycle (re-verification of cycle 1 fixes)
**Fix cycle:** 1 (re-verification)
**Agent:** rf-qa-qualitative — fix_authorization: **false** (REPORT-ONLY, modified nothing)
**Consolidated findings under review:** qa/qa-consolidated-findings-phase-6.md
**Fix report under review:** qa/qa-fix-phase-6.md

---

## Overall Verdict: PASS

The cycle-1 fixes are SOUND. The prior CRITICAL (C6-01) is genuinely resolved — the
advisory match logic now references only columns that exist in the actual Feedback
Collection Template schema. Determinism is genuinely secured (deterministic per-pair
row + ordering + count + malformed handling + first-run omission). The non-mutation /
advisory-only property and the §5.3 pure-function fence are intact. Domain-accuracy vs
FR-RFMERGE.5 + NFR-RFMERGE.1 + the recorded `retain-advisory-only` decision is preserved.

---

## CONFIRM-1: DETERMINISM genuinely secured (prior CRITICAL C6-01 RESOLVED)

**Result: PASS.**

The prior CRITICAL was that the match logic referenced feedback-log fields that do not
exist in the generator's actual `## Feedback Collection Template` schema. I re-read both
the schema (SKILL.md:855) and the reconciled match logic (SKILL.md:873) independently.

- **Actual schema columns** (SKILL.md:855):
  `Task ID | Original Tier | Override Tier | Override Reason | Completion Status | Quality Signal | Time Variance`.
- **Reconciled match logic** (SKILL.md:873) now matches on **`Task ID`** (col 1, EXISTS)
  and treats a "matching override" as a matched row whose **`Override Tier`** (col 3,
  EXISTS) is non-blank AND differs from the deterministically-scored tier. The advisory's
  `Feedback-suggested tier` ← `Override Tier`; `Scored tier` ← the task's current scored tier.
- **Phantom names eliminated from the operative logic.** Independent grep
  (`roadmap_item_id|task_signature|suggested_tier`) returns hits ONLY at SKILL.md:873, and
  ONLY inside the explicit spec→concrete mapping note ("the spec's abstract `roadmap_item_id`
  / `task_signature` maps to the concrete `Task ID`… `suggested_tier` maps to `Override
  Tier`"). They no longer drive any match — they document the reconciliation. So "matching
  overrides" is now COMPUTABLE → the ≥2 threshold (render vs omit) is deterministic.

Determinism sub-invariants verified present in source (independent grep, byte-exact):

| Invariant | Source string (verified) | Loc | Status |
|-----------|--------------------------|-----|--------|
| Per-pair row (tie-break) C6-02 | one advisory row per distinct `(Task ID, Override Tier)` pair | SKILL.md:875 | PASS |
| Ordering C6-02 | ordered ascending by `T<PP>.<TT>` (i.e. `Task ID`) then `Override Tier` ascending | SKILL.md:875 | PASS |
| Observed count C6-03 | `Observed count` = number of feedback-log rows for that pair | SKILL.md:875 | PASS |
| Malformed/empty/partial C6-04 | rows missing `Task ID`/`Override Tier` ignored; <2 ⇒ omit, no error | SKILL.md:877 | PASS |
| First-run absence C6-04 | "when absent, the whole section is omitted, no error" (best-effort READ-ONLY) | SKILL.md:870-871 | PASS |
| Same-inputs determinism | "same inputs → byte-identical section" | SKILL.md:889 | PASS |

Tie-break note: a single `Task ID` with two distinct non-blank `Override Tier` values now
yields TWO rows in `Override Tier`-ascending order — the previously-undefined multi-row
ordering is now total and deterministic. No remaining source of non-determinism in the
rendered advisory was found.

---

## CONFIRM-2: NON-MUTATION / advisory-only soundness PRESERVED

**Result: PASS.**

- **Still read-only.** SKILL.md:870-871 — "reads the PRIOR-run `feedback-log.md`
  **best-effort and READ-ONLY**"; "the render is read-only — it never writes the scored
  tiers, it only displays them next to the feedback's suggestion."
- **Never mutates scored Tier/Confidence.** SKILL.md:871 — "**NEVER auto-applies** and
  **MUST NOT mutate** any task's scored `Tier`/`Confidence` field." (`MUST NOT mutate`
  count = 1; `NEVER auto-applies` present — both retained, non-regressed.)
- **§5.3 fence intact.** SKILL.md:569 — "scored tiers are a **pure function of the roadmap
  text**… the §5.3/§5.4 scored-tier compute path takes **NO calibration/feedback input** (it
  **MUST NOT read `feedback-log.md`** or the P5 `## Tier Calibration Advisory`). The advisory
  is read-only and never feeds back into `tier_scores`." All four byte-strings verified
  present via independent grep.
- **Render-at-index-assembly clarification does NOT create a feedback loop.** The C6-05
  edit ("rendered at index assembly (Stage 4/5), **after** scored tiers are computed") is a
  one-way dependency: scored-tier COMPUTE → advisory RENDER. The render consumes the
  already-computed tiers + the feedback-log, and writes nothing back. SKILL.md:871 states
  this explicitly ("The §5.3 fence holds precisely because the scored-tier COMPUTE never
  reads the feedback-log; only this advisory RENDER reads it"). No path was found by which
  the advisory feeds back into `tier_scores`. The clarification fixed a stage-attribution
  contradiction without weakening the fence.

The non-mutation lens PASSed in cycle 1; these edits did not regress it.

---

## CONFIRM-3: DOMAIN-ACCURACY vs FR-RFMERGE.5 + NFR-RFMERGE.1 + recorded decision PRESERVED

**Result: PASS.**

- **Spec table unchanged.** spec.md:344-350 untouched. The SKILL.md exact-output block
  (882-886) is byte-identical to the spec table content (verified by normalized diff that
  strips only the spec's 2-space code-fence indent — column headers, separator row, the
  `T<PP>.<TT> | STRICT | STANDARD | <n> | ⚠ STRICT-downgrade…` data row, and the
  blockquote all match exactly). Table-conformance lens PASS preserved.
- **Schema reconciliation is a faithful mapping, not a spec violation.** FR-RFMERGE.5
  (spec.md:334-339) defines the advisory input in ABSTRACT terms (`roadmap_item_id |
  task_signature`, `suggested_tier`, `observed_count`). This generator's concrete
  `feedback-log.md` schema (SKILL.md:855) carries `Task ID` and `Override Tier`. The fix
  maps abstract→concrete (`roadmap_item_id`/`task_signature` → `Task ID`;
  `suggested_tier` → `Override Tier`; `observed_count` → derived `Observed count` per pair),
  documented explicitly at SKILL.md:873. This satisfies the spec's intent (match a feedback
  row to a scored task; a matching override = differing suggested tier; ≥2 threshold) using
  the columns that actually exist — it does not drop, add, or contradict any spec field.
- **No requirement dropped.** Min-2 threshold (spec.md:340 → SKILL.md:873), STRICT-downgrade
  warning semantics (spec.md:352-353 → SKILL.md:879, 886), deterministic ordering / omission
  (spec.md:354-357 → SKILL.md:875, 889), and "never feeds back into scored tiers"
  (spec.md:356-357 → SKILL.md:871, 889) all present.
- **NFR-RFMERGE.1 honored.** spec.md:627 requires "same roadmap → same scored tiers (always)"
  AND "same roadmap + same feedback-log → same advisory." Both are asserted in source
  (SKILL.md:569 fence for scored tiers; SKILL.md:889 "same inputs → byte-identical section"
  for the advisory). The byte-identical-bundle ⇔ `(roadmap, --spec, feedback-log.md)` tuple
  semantics is consistent with the reconciled per-pair-deterministic render.
- **Recorded `retain-advisory-only` decision honored.** spec.md:610-615 / 325 — the
  generator renders the section + STRICT-downgrade warnings and never mutates scored tiers.
  The fix preserves exactly this disposition; no shift toward `defer` or toward
  tier-mutation.

The domain-accuracy lens recorded 0 defects in cycle 1; these edits did not introduce any.

---

## Index-template mirror (non-regression)

Mirror at `templates/index-template.md:132-138` carries the reconciled semantics
(abbreviated, consistent): `## Tier Calibration Advisory` placeholder present; match on
`Task ID` == `T<PP>.<TT>`; suggested tier ← `Override Tier`; one row per `(Task ID,
Override Tier)` pair; `Observed count` per pair; ordered ascending by `T<PP>.<TT>` then
`Override Tier`; ≥2-override render threshold; STRICT-downgrade ⚠. No mirror drift vs the
SKILL.md authority.

---

## Test hardening re-verification (C6-06..C6-08)

All asserts in the three new tests were independently confirmed byte-present in the
post-fix source (not merely trusted from the fix report):

| Test | Key asserts → source | Status |
|------|----------------------|--------|
| `test_p5_advisory_same_inputs_byte_identical` (C6-06) | "same inputs → byte-identical section" (889); `Task ID` match (873); `Override Tier` differs (873); per-pair row (875); Observed count (875) | PASS |
| `test_p5_advisory_first_run_omission` (C6-07) | "best-effort and READ-ONLY" (871); "when absent…omitted, no error" (871); "Rows missing `Task ID` or `Override Tier` are ignored" (877); "yields fewer matches" (877) | PASS |
| `test_p5_advisory_index_template_mirror` (C6-08) | reads `index_template_text`; advisory placeholder + match/order phrasing in index-template.md:132-138 | PASS |

Each assert string was grep-confirmed in the cited source line. Tests are not stubs — they
gate the exact reconciled semantics, so future mirror/match drift fails.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | C6-01 CRITICAL resolved (match on real columns) | PASS | grep: phantom names only in spec-mapping note (SKILL.md:873); match keys `Task ID`/`Override Tier` exist in schema (855) |
| 2 | C6-02 per-pair row + ordering | PASS | SKILL.md:875 byte-grep |
| 3 | C6-03 Observed count semantics | PASS | SKILL.md:875 byte-grep |
| 4 | C6-04 malformed/empty/partial + first-run | PASS | SKILL.md:871, 877 byte-grep |
| 5 | C6-05 render-timing fence-holds clarification | PASS | SKILL.md:870-871; no feedback-loop path found |
| 6 | Non-mutation / advisory-only | PASS | `MUST NOT mutate`×1, `NEVER auto-applies`, READ-ONLY (871) |
| 7 | §5.3 pure-function fence intact | PASS | SKILL.md:569 four byte-strings present |
| 8 | Spec table byte-identical | PASS | normalized diff spec:345-349 vs SKILL:883-887 |
| 9 | Schema reconciliation faithful | PASS | FR-RFMERGE.5 abstract→concrete mapping (873) |
| 10 | NFR-RFMERGE.1 determinism | PASS | scored-tier fence (569) + advisory same-inputs (889) |
| 11 | Recorded retain-advisory-only honored | PASS | spec.md:610-615 vs SKILL.md:866-889 |
| 12 | Index-template mirror non-regression | PASS | index-template.md:132-138 |
| 13 | C6-06..C6-08 tests real, asserts byte-match | PASS | grep each assert string; 5 P5 tests pass |
| 14 | Sync + suite green | PASS | `make verify-sync` clean; `pytest tests/tasklist/` 95 passed |

## Summary
- Checks passed: 14 / 14
- Checks failed: 0
- Critical issues: 0 (prior CRITICAL C6-01 resolved)
- Issues fixed in-place: 0 (REPORT-ONLY agent — modified nothing)
- Confidence: Verified 14/14 | Unverifiable 0 | Unchecked 0 | Confidence 100%
- Tool engagement: Read 7 | Grep 6 | Bash 5 (verify-sync, pytest×2, table-diff, string-greps) | Glob 0

## Issues Found
None. All 8 cycle-1 findings (C6-01..C6-08) confirmed resolved with no regression and no
new issues introduced.

## Inherited Structural Verdict — Reliance Audit (PR-04, INV-019)
No `## Inherited Structural Verdict` block was supplied in the spawn prompt; this was a
direct fix-cycle content re-verification. I performed independent structural + content
verification rather than relying on inherited PASS items:
- Relied on rf-qa cycle-1 PASS for table-conformance → independent semantic counterpart
  verified: normalized byte-diff of spec.md:345-349 vs SKILL.md:883-887 (my own Bash diff),
  confirming content identity rather than trusting the prior verdict.
- Relied on rf-qa cycle-1 PASS for non-mutation → independent semantic counterpart verified:
  grep-counted `MUST NOT mutate` (=1) + `NEVER auto-applies` + traced the render-at-index
  clarification for any feedback-loop path (none found).

## Self-Audit
1. **Independently verified claims:** 14 (every fix string grep-confirmed in source; spec
   table diffed; tests executed; verify-sync run). I did not trust the fix report's "ALL
   APPLIED" claim — I re-derived each from the actual files.
2. **Files read/inspected:** consolidated-findings-phase-6.md, qa-fix-phase-6.md,
   SKILL.md (845-889, 567-569), index-template.md (120-149), spec.md (322-361, 600-634),
   test_tasklist_cli.py (36-48, 575-649).
3. **Why trust this (>0 issues sought):** I began adversarially — specifically hunting for
   (a) phantom field names surviving in operative logic, (b) a feedback→scored-tier loop
   reintroduced by the render-timing edit, (c) spec-table drift, (d) stub asserts. Each was
   actively checked and cleared with tool evidence, not assumed.
4. **Web research:** none required (fully local-file-bound verification); Tavily not invoked.

## Recommendations
- Green light to proceed. Phase 6 (P5) fix cycle 1 is verified PASS. No further fix cycle needed.

## QA Complete
