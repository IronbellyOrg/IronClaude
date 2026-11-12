# Handoff step 2 (bmad-prd): orca-observer PRD

PRD: `.dev/issues/409/bmad/prd-orca-observer/prd.md` (copy of Coder `_bmad-output/planning-artifacts/orca-observer/prd.md`, status final). Companion: `addendum.md` (CAP to FR to test matrix, counts).

## What the PRD locks
- Staged releases: R0 offline fixtures; DIRECTION-SELECTED gate (NOT passed, so only R0 work is allowed today); R1 = Signal Bridge worker ledger on verified `worker-list`, with Attention Ledger's "question source UNVERIFIED" notice; R2 = Attention Ledger after QUESTION-OBSERVATION; R3 = Decision Desk after QUESTION-LINK; R4 remote; Later; Future write-back.
- Stack: Python + Rich, `superclaude observe`-style subcommand in IronClaude; R1 writes a versioned additive-only JSON snapshot (`export(view)`, schema PROPOSED) with a schema test; key-reader spike first, Textual only if it fails, never both.
- R1 read-only. Write-back is a separate future section needing a boundary change on issue 409 and an amendment of TUIBBS FR-X-13.
- TUIBBS background only (no dependency, no copied code). Evidence labels kept; no invented Orca fields.
- Users: one human, 5-10 orchestrators, 50-100 sessions. NFRs: 160/116/80 columns, NO_COLOR, ASCII, keyboard, sanitizing, bounded polling, no LLM loop.

## Counts
- 18 FR (R0 2, R1 14, R2 1, R3 1); 14 NFR; success criteria reuse issue ACs and spec tests T1-T51 (all cited).
- 15 open questions carried word for word from SPEC.md:99-113, none resolved; 13 open items (OI-1 to OI-13).

## Validation and review
- VALIDATE (review 1): grade Excellent; 4 blocking fixed in fix cycle 1; 11 minor deferred as notes (`validation-report.md/.html`).
- Adversarial fresh-context review (review 2): FAIL, 2 blocking, 13 minor (`adversarial-review.json`).
  - B1: FR-8 falsely said no mismatch string is pinned (an error introduced by fix cycle 1). Fixed: FR-8 now states `collected n / reported T (mismatch)` (rendering-rules.md:55, T47).
  - B2: glossary PARTIAL was wrong. Fixed: PARTIAL = call cap hit with `page.hasMore` true, or empty page with T above 0; new Mismatch row.
- Both fixes applied in fix cycle 2 after the review and NOT re-verified by a further review (brief allows one adversarial pass). Step 5 should recheck FR-8 and the glossary.

## UNVERIFIED, dropped, open
- 13 adversarial minors (M1-M13) and 11 validation minors not acted on. Watch M12 (JTBD-4 "exactly the view on screen" vs CAP-9/T48 lossless export) and M6 (R2-only strings inside R1 FR-8).
- 4 prose fixes skipped: (c) proof list split (could change the gate), "summary decision" renumbering x2 (collision kept as OI-11), V1/V3 definitions (meaning unknown).
- `reason unknown` (FR-17/FR-18, A7/A8) is a PRD-added display string, not in the spec.
- NFR-13 Windows behaviour UNVERIFIED until T27 runs on Windows; NFR-1 numeric height blocked on OQ-14.
- No commit, push, PR or issue edit was made.
