# PRD Validation Report: Orca Read-Only Terminal Observer

- PRD: `_bmad-output/planning-artifacts/orca-observer/prd.md` (with `addendum.md`)
- Rubric: `.claude/skills/bmad-prd/assets/prd-validation-checklist.md`
- Run at: 2026-11-08T18:32Z (rubric walker); fixes applied 2026-11-08T18:40Z
- Grade: **Excellent** (all dimensions strong or adequate; no high or critical findings)

## Overall verdict

A usable, honest PRD for a gated, R0-only internal tool. Decisions, gates and their status, dissents, evidence labels and FR-to-test traceability are solid. The open questions are genuinely open and carried word for word (checked against SPEC.md:99-113). The risk was concentrated in four requirements that could not be tested as written (FR-8 mismatch form, NFR-1 height threshold, NFR-13 Windows claim, FR-17/FR-18 "why it matters"), and in success metrics that measure delivery rather than the thesis. All four BLOCKING items were fixed in the single permitted fix cycle (see "Fix status" under each). The 11 MINOR findings are recorded as notes and not acted on.

## Dimension verdicts

| Dimension | Verdict |
|---|---|
| Decision-readiness | strong |
| Substance over theater | strong |
| Strategic coherence | adequate |
| Done-ness clarity | adequate |
| Scope honesty | strong |
| Downstream usability | adequate |
| Shape fit | strong |

## Findings by severity

### Critical

None.

### High

None.

### Medium

- **[Done-ness clarity]** FR-8 contradicts itself on the mismatch form (§5.4 FR-8) — BLOCKING
  The bullet listed mismatch as "exactly as pinned" while saying no mismatch string is pinned; T47 inherits the gap.
  Fix: remove mismatch from the pinned list, let UX set it, mark T47's mismatch part pending. **Fix status: applied.** Also added `reported unknown` (T18, T32).
  **Correction (fix cycle 2, after the adversarial review):** this fix was wrong. rendering-rules.md:55 does pin the mismatch string, `collected n / reported T (mismatch)`, and T47 cites it. FR-8 now states that string; "UX sets it" and "T47 pending" were removed.
- **[Done-ness clarity]** NFR-1's too-small-height diagnostic has no threshold (§6 NFR-1) — BLOCKING
  Height depends on C's 44-row contract, which OQ-14 says is undefined, so T49 could not be written.
  Fix: state the threshold or mark it blocked on OQ-14. **Fix status: applied** (threshold stated as a content rule; numeric row count blocked on OQ-14).
- **[Done-ness clarity]** NFR-13's Windows claim verified by a test that does not test Windows (§6 NFR-13) — BLOCKING
  T27 is a headless export assertion with no platform dimension.
  Fix: mark Windows UNVERIFIED or require a Windows runner. **Fix status: applied** (Windows behaviour UNVERIFIED until T27 runs on a Windows runner).
- **[Done-ness clarity]** "Why it matters" has no defined source (§5.10 FR-17; §5.11 FR-18) — BLOCKING for R2/R3 stories only
  The reason text had no source; message fields are UNVERIFIED (U1).
  Fix: sourced field shown verbatim or `reason unknown`, tied to OQ-7. **Fix status: applied** (assumptions A7, A8 added to §13.3).
- **[Strategic coherence]** Success metrics measure delivery, not the thesis (§9.2) — MINOR
  SM-1 to SM-3 would pass on a product no supervisor can use; R2 has no success metric of its own.
  Fix: add one thesis metric per release. Not applied (minor).
- **[Downstream usability]** Citations to chain-internal artifacts a downstream reader cannot resolve (§5.5, §5.6, §5.9, §9.1, §10.1, §12.2, §13.2) — MINOR
  "step-1 minor n", "gap Gn", "I:91", "M:463", "V1/V3" have no key.
  Fix: add a one-line key or restate in place. Not applied (minor).

### Low

- **[Decision-readiness]** Open questions not tagged with the release they block (§12.1). Fix: add a "blocks" marker. MINOR.
- **[Decision-readiness]** Owner-decision numbering collides within one source file (§5.1, §11, §12.2, §12.3 item 10). Fix: one numbering scheme. MINOR.
- **[Substance over theater]** Pipeline commentary in the product body (§12.2 step-1 minor 7 note; OI-13 pointer). Fix: move to a review log. MINOR.
- **[Done-ness clarity]** FR-9 four-state rule has no test; FR-6 view choice trivially true in R1 (§5.4, §5.2). Fix: map to T13/T15/T40/T42; note FR-6 becomes meaningful at R2. MINOR.
- **[Done-ness clarity]** FR-8 omitted `reported unknown` (§5.4). Fix: add it. MINOR. **Applied** with the FR-8 blocking fix.
- **[Downstream usability]** Glossary misses normative nouns (COUNTS strip, freshness strip, source window, `scope=bound`, historical row); "stage" overloaded (§3). MINOR.
- **[Downstream usability]** Addendum matrix lists T9 under CAP-2 but FR-3 does not cite it (§5.2 FR-3). MINOR.
- **[Shape fit]** Jobs encoded three times (JTBD, user story, UJ list). MINOR.
- **[Mechanical]** Assumptions Index roundtrip: FR-17/FR-18 tags had no §13.3 entry (**applied**: A7, A8); A1 and A6 lack inline tags (not applied). MINOR.

## Mechanical notes

- ID continuity: FR, NFR, UJ, JTBD, SM, SM-C, OQ, OI and A ids are contiguous and unique.
- Coverage verified by the reviewer: every T1-T51 cited in prd.md; addendum §C counts correct (18 FR, 14 NFR, 15 OQ, 13 OI).
- Verbatim claim verified: OQ-1 to OQ-15 match SPEC.md:99-113.
- Stack/spike rule consistent with the owner-confirmed stack.
- Required sections present for the stakes.

## Reviewer files

- `review-rubric.md` (rubric walker; single VALIDATE pass, also serving as the Finalize Reviewer Gate per the memlog override)
- Input reconciliation (not review rounds): `reconcile-originals.md`, `reconcile-spec-companions.md`, `reconcile-spec-core.md`
