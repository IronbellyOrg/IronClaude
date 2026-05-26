# Round 2 — Variant 1 Rebuttal (opus)

## Response to Criticisms

- **Criticism**: V1's lockout deferral to M3 leaves a 4-week brute-force window on a public endpoint, contradicting the TDD's explicit security consideration (X-002, C-003).
- **Response**: **CONCEDE.** Already conceded in Round 1 (Concession 1). R-102 gateway rate-limiting (10/min/IP) and bcrypt cost-12 latency (~300ms) are partial mitigations but not equivalents. The fix is small (V2-advocate is correct that a counter+threshold is ~20-30 lines) and the brute-force risk is PRD-rated "High probability." Move D-305 into M1.
- **Diff IDs**: C-003, X-002.

- **Criticism**: V1's rollback procedure step 2 ("traffic routes back to legacy auth") is architecturally infeasible on the PRD-declared greenfield (X-004, C-022).
- **Response**: **CONCEDE.** Already conceded in Round 1 (Concession 2). PRD Executive Summary explicitly says "the platform currently operates without any user identity system." V1's rollback section must be rewritten to match V2's maintenance-page or unauthenticated read-only mode.
- **Diff IDs**: C-022, X-004.

- **Criticism**: V1's single-row staffing ("2 backend + 1 frontend FTE + 0.5 SRE + 0.25 security review") is unactionable for hiring (U-022, S-012).
- **Response**: **CONCEDE.** Already conceded in Round 1 (Concession 3). V2's 10-row per-sprint table is materially better. Adopt V2's table format.
- **Diff IDs**: S-012, U-022.

- **Criticism**: V1 lacks a dedicated admin audit-log query deliverable for Jordan persona (C-018, U-027).
- **Response**: **CONCEDE.** Already conceded in Round 1 (Concession 4). V2's D-030 ("filter by date range, user, event type") is the correct concrete deliverable. V1's persona coverage check (Section 13) names Jordan but does not produce the deliverable.
- **Diff IDs**: C-018, U-027.

- **Criticism**: V1 has no post-GA section, leaving v1.1/v2.0 sequencing undefined (S-013, U-023, Weakness 3 in V2's R1).
- **Response**: **PARTIAL CONCESSION.** V1's Out of Scope (Section 10) names v1.1/v1.2 items but supplies no quarters. V2's Section 13 (v1.1 = Q3 2026, v2.0 = Q4 2026) is operationally tighter. However, V2's quarter assignments are themselves not source-grounded — the PRD Non-Goals say "planned for v1.1" and "planned for v2.0" without dates, so V2 is inventing Q3/Q4 commitments. The right move: adopt V2's structure (named v1.1 features, named v2.0 features, ongoing maintenance subsection) but mark quarters as "target, not committed" until PM confirms.
- **Diff IDs**: S-013, U-023.

- **Criticism**: V1's audit retention reconciliation is internally inconsistent — D-102 specifies "90-day retention job spec" while CC1 SEC-3 says "bump to 12 months," so the deliverable text and workstream item contradict (V2 R1 Weakness 6, C-005, X-008).
- **Response**: **PARTIAL REBUTTAL with concession on wording.** The two-step structure is deliberate: D-102 ships the table with the TDD's 90-day default, then OQ-R1 forces a security+compliance decision before D-102 is sealed, and SEC-3 bumps to 12 months once that decision lands. This is sequencing, not contradiction. **However**, V2 advocate is correct that the deliverable text as written is ambiguous — D-102 should be re-worded to "retention parameterized, default 90d per TDD, set to 12 months pending OQ-R1 resolution before M1 commit." On storage cost: V2 is right that 12-month retention at ~12M rows × ~500 bytes ≈ 6 GB is unmodeled in V1's Section 14 cost table; this should be added (~$0.69/month at S3 pricing, negligible operationally but should be line-itemed for honesty).
- **Diff IDs**: C-005, X-008.

- **Criticism**: V1 has no measurable schedule buffer; any 2-3 day slip in M1 cascades through the entire chain (V2 R1 Weakness 2).
- **Response**: **PARTIAL CONCESSION.** V1's "2-week stabilization tail" is post-GA, not pre-GA, so V2 is correct that no pre-GA float exists. V2's "hidden 1-week beta-to-GA buffer" (U-028, C-029) is standard PM practice and V1 should adopt it. **However**, V2's argument that bcrypt re-benchmarking would blow M1 is weak: the M1 entry criteria include the bcrypt benchmark in Week 1, leaving Week 2 for remediation if needed; the mitigation ("drop to cost 11 with documented rationale") is a 1-line config change, not a multi-day re-architecture. The buffer concession is real; the bcrypt-cascade argument is overstated.
- **Diff IDs**: C-029, U-028.

- **Criticism**: V1's three-phase decomposition rationale is absent — V2 explicitly argues "Why Three Phases, Not Two" (U-021).
- **Response**: **PARTIAL CONCESSION.** V1 adopts the TDD's five-milestone structure without reconciling it against the PRD's two-phase prescription. V2's explicit rationale is a nice touch and prevents reader confusion. But this is a documentation-completeness issue, not a structural defect — V1's M1-M5 cadence is identical to the TDD §23.1 cadence, which itself is the PRD's two-phase split rendered at higher resolution. The fix is a one-paragraph "phase-to-milestone mapping" note in V1 Section 2.2, not a structural overhaul.
- **Diff IDs**: U-021.

## Updated Assessment of Variant 2

### Arguments I now find MORE persuasive

1. **Lockout-in-M1 (C-003).** I conceded this in R1 but V2's specific framing — "a `LoginAttemptTracker` is approximately 20-30 lines of code" — undercuts the scope objection more effectively than I gave it credit for. The TDD §13 lockout spec is simple enough that adding it to M1 is genuinely cheap. V2 wins outright.

2. **Greenfield rollback (X-004).** V2's framing that following V1's procedure during an actual incident would fail at step 2 is sharper than my R1 concession acknowledged. This is not just a documentation defect; it's a P1-incident-time failure mode. V2 wins outright.

3. **Beta-to-GA buffer (C-029, U-028).** I gave this a "V2" tally in R1 but didn't engage with the rationale. V2's argument — beta phases regularly surface issues requiring remediation, and zero-buffer GA forces a ship-known-issues-or-publicly-slip choice — is standard PM practice and V1 should adopt it.

4. **Post-GA Section 13 structure (S-013).** V2's three-subsection layout (v1.1 features, v2.0 features, ongoing maintenance) provides a template V1 should adopt verbatim. My R1 concession was correct but I should have flagged the ongoing-maintenance subsection (key rotation, bcrypt review, retention verification, dependency updates, capacity review) as particularly valuable — it captures the SOC2-relevant recurring activities that auditors will ask about.

### Arguments I still find UNPERSUASIVE

1. **"22-week timeline is realistic with full SDLC overhead" (if V2 argued this).** V2's R1 actually *concedes* the 22-week label is wrong (Concession 1). I expected a defense and got an admission — V2 advocate honorably conceded that "22 weeks" + Sprint 1-11 labeling is internally inconsistent with the 2026-06-09 GA date. V1 wins X-001 outright and there is no remaining V2 position to rebut.

2. **"State machines and token families belong in the TDD, not the roadmap" (V2 R1 position summary).** This is V2's strongest framing argument and I reject it. The TDD does not contain these state machines — that's the gap. A roadmap whose deliverables reference token-rotation behavior without specifying the reuse-detection consequence forces each implementer to invent it. V1's Section 9 is roadmap-appropriate because it converts ambiguous TDD prose into deliverable-level acceptance criteria. If the right home were the TDD, the right fix would be a TDD revision — but the roadmap is being built right now, and V1's Section 9 is the artifact that unblocks M2/M3 implementation. V2's position would be defensible only if the TDD already had these state machines, which it does not.

3. **"V2's structured logging in M2 partially mitigates the SOC2 audit gap" (V2 R1 Concession 2 caveat).** Application logs and audit logs are categorically different: app logs have no enforced retention, no immutable append-only semantics, no schema discipline, and are not designed for retrospective auditor queries. Calling app logs a "partial mitigation" for a SOC2 audit-trail constraint understates the gap. V1 wins X-003 / C-004 outright.

4. **"V2's 30-minute auto-unlock is more secure" (implicit in OQ-C, C-008/X-005).** V2's recommendation lacks source grounding. The TDD §13 explicitly references a 15-minute sliding window (consistent with V1). Doubling the window to 30 minutes punishes legitimate users (5 mistyped passwords → locked out for 30 minutes is a help-desk-ticket generator) without measurable security gain — an attacker pacing attempts to stay under the threshold is equally constrained at 15 or 30 minutes. UX cost is real, security benefit is marginal. V1 wins X-005.

### New criticisms not raised in Round 1

1. **V2's Bull/BullMQ recommendation creates an undisclosed infrastructure dependency.** Bull/BullMQ requires its own monitoring (queue depth, retry rate, dead-letter handling), its own runbook (drain procedure during deploys, stuck-job recovery), and its own failure modes (queue-poisoning attacks via crafted job payloads). V2's Section 10.3 cost table shows Redis at $100/month with no upgrade for queue workload, and V2 has no deliverable for queue monitoring/runbook. V1's SendGrid in-process retry approach is genuinely simpler and avoids this entire surface. This is V1's strongest unsurfaced counter to V2's "operational honesty" claim — V2 introduces operational complexity it does not budget for.

2. **V2's "soft M3→M4 dependency" claim (S-017) overstates parallelization gains.** V2 R1 Strength 10 argues frontend can start in Sprint 5-6 because only the password-reset page depends on M3. But M2's `/auth/me` endpoint, error-shape conventions, CSRF cookie format, and refresh-token cookie semantics are all dependencies for LoginPage/RegisterPage. M2 must close before M4 can start frontend integration — "M4 soft-blocked by M3" is technically true but operationally insignificant because M2 is the binding constraint. V1's "M4 blocked by M2, M3" is conservatively correct; V2's parallelization gain is mostly illusory.

## New Evidence

1. **PRD sprint count is explicit, not inferred.** PRD Phasing section says "Phase 1 (Sprint 1-3)" + "Phase 2 (Sprint 4-6)" = 6 sprints. At the project's own 2-week sprint convention (which V2 never disputes), that is 12 calendar weeks. V1's 11-week active + 2-week tail = 13 weeks total matches the source intent within rounding. V2's "22 weeks, Sprint 1-11" would require either (a) 1-week sprints (never claimed) or (b) doubling the PRD's prescribed sprint count without justification. This is decisive for X-001 / C-001 / C-002.

2. **TDD §13 lockout window is 15 minutes, not 30.** TDD Section 13 explicitly states "Account lockout after 5 failed login attempts within 15 minutes mitigates brute-force attacks." This is the window; the auto-unlock at the same interval is the natural sliding-window consequence. V2's OQ-C recommendation of 30 minutes contradicts the TDD without justification. V1 wins X-005 on source-grounding alone.

3. **TDD §25.3 Redis sizing is auth-only.** TDD Section 25.3 sizes Redis at ~50 MB for ~100K refresh tokens. This is the design budget. Adding Bull/BullMQ on the same instance — without re-sizing — violates the design. V2's OQ-A async-email recommendation is incomplete: it should specify "separate Redis namespace/instance" or "+200 MB queue allowance." V1's in-process SendGrid retry keeps the TDD sizing valid.

4. **PRD R-002 brute-force rating is "High probability, Medium impact" — both axes matter.** I cited this in R1 to justify the lockout concession. New angle: PRD R-002 mitigation column reads "Account lockout (5 attempts, 15 min window) + rate limiting at gateway." The PRD lists *both* as mitigations, implying both are required. V1's M3 placement of lockout makes one of the two PRD-named mitigations absent for the M1-M2 window. This strengthens the lockout-in-M1 concession from "good practice" to "PRD compliance."

## Per-Diff-Point Position Update

| Diff ID | R1 Position | R2 Position | Changed? | Why |
|---|---|---|---|---|
| C-001 | V1 | V1 | No | V2 advocate conceded the 22-week label; V1 wins outright. |
| C-002 | V1 | V1 | No | TDD §23.1 fortnightly cadence is explicit; V2 advocate conceded. |
| C-003 | V2 (concede) | V2 (concede, stronger) | Sharpened | V2's "20-30 lines of code" framing makes the scope objection untenable. |
| C-004 | V1 | V1 | No | V2's "structured logging mitigates" caveat understates the SOC2 gap. |
| C-005 | V1 | V1 with wording fix | Refined | D-102 deliverable text should be reworded to acknowledge the OQ-R1 dependency; storage cost line-item missing. |
| C-006 | Tie | Tie | No | Both architecturally valid. |
| C-007 | V2 | V2 | No | V2's 10-token cap is a concrete v1.0 policy. |
| C-008 | V1 | V1 | No | TDD §13 grounds 15-min window; V2's 30-min is unjustified. |
| C-009 | V1 | V1 | No | V2 advocate conceded (Concession 3). |
| C-010 | V1 | V1 | No | V2 has no equivalent. |
| C-011 | V1 | V1 | No | Specificity wins. |
| C-012 | V1 | V1 | No | Explicit `beforeunload` handler. |
| C-013 | V1 | V1 | No | Measurable Lighthouse gate. |
| C-014 | V1 | V1 | No | V2 advocate conceded (Concession 5). |
| C-015 | V1 | V1 | No | V2 advocate conceded (Concession 4). |
| C-016 | Tie | Tie | No | SET-NX and MULTI/EXEC both valid. |
| C-017 | V1 | V1 | No | V1 raises the OQ; V2 silently picks one path. |
| C-018 | V2 (concede) | V2 (concede) | No | D-030 is the right pattern. |
| C-019 | V1 | V1 | No | Legal urgency framing is correct. |
| C-020 | Tie (V2 specific, V1 cleaner) | V1 (newly persuaded) | Changed | New criticism above: V2's Bull/BullMQ creates undisclosed operational complexity (monitoring, runbook, queue-poisoning surface) not in V2's budget. V1's in-process retry is genuinely simpler. |
| C-021 | V2 (concede) | V2 (concede) | No | Appendix B is operationally tighter. |
| C-022 | V2 (concede) | V2 (concede, stronger) | Sharpened | V2's "would fail at step 2 during incident" framing elevates this to P1-time failure mode. |
| C-023 | V2 | V2 | No | Budget enables procurement. |
| C-027 | V1 | V1 | No | V2 silent on migration locking. |
| C-028 | V1 | V1 | No | V2 silent on coordinated release risk. |
| C-029 | V2 | V2 (stronger concession) | Sharpened | Standard PM practice; V1 should adopt verbatim. |
| S-007 | V1 | V1 | No | V2 advocate conceded; "belongs in TDD" rebuttal does not apply since TDD lacks them. |
| S-008 | V1 | V1 | No | V2 has no personas coverage check. |
| S-009 | V1 | V1 | No | V2 has no governance section. |
| S-012 | V2 (concede) | V2 (concede) | No | Adopt V2 staffing table. |
| S-013 | V2 | V2 (with quarter caveat) | Refined | Adopt V2 structure but mark Q3/Q4 as "target, not committed." |
| S-017 | (not tallied in R1) | V1 | New | V2's "soft M3→M4 dependency" parallelization gain is mostly illusory because M2 is the binding constraint. |
| X-001 | V1 | V1 | No | V2 conceded. |
| X-002 | V2 | V2 | No | Concede. |
| X-003 | V1 | V1 | No | SOC2 day-1 required. |
| X-004 | V2 | V2 (sharpened) | Sharpened | P1-incident failure mode. |
| X-005 | V1 | V1 | No | TDD §13 grounds 15-min. |
| X-006 | V2 | V2 | No | 10-token cap concrete. |
| X-007 | Tie | Tie | No | Both valid. |
| X-008 | V1 | V1 with wording fix | Refined | OQ-R1 discipline correct; D-102 text needs clarifying. |

**Net updated tally:**

- **V1 outright wins:** C-001, C-002, C-004, C-005, C-008, C-009, C-010, C-011, C-012, C-013, C-014, C-015, C-017, C-019, C-020 (newly), C-027, C-028, S-007, S-008, S-009, S-017 (newly), X-001, X-003, X-005, X-008 = **25 points**
- **V2 outright wins:** C-003, C-007, C-018, C-021, C-022, C-023, C-029, S-012, S-013, X-002, X-004, X-006 = **12 points**
- **Ties:** C-006, C-016, X-007 = **3 points**

V1 leads on the engineering-discipline and security-formalization axes; V2 leads on the operational-detail and procurement axes. The merged artifact dominates both — that remains the synthesis position.

## Final Concessions in This Round

1. **C-003 / X-002 (lockout in M1):** V2 wins decisively. Already conceded in R1; reaffirmed with sharper rationale.

2. **C-022 / X-004 (greenfield rollback):** V2 wins decisively. Already conceded in R1; sharpened to P1-incident failure mode.

3. **S-012 (staffing table):** V2 wins. Already conceded in R1.

4. **C-018 (admin audit query):** V2 wins. Already conceded in R1.

5. **S-013 (post-GA section):** V2 wins on structure (adopt verbatim), but quarter commitments should be softened to "target."

6. **C-029 (beta-to-GA buffer):** V2 wins. V1 should add the 1-week hidden buffer.

7. **C-005 wording (audit retention):** V2 advocate correctly identifies that V1's D-102 text + SEC-3 sequencing reads as a contradiction even though the intent is sequencing. V1's D-102 deliverable text should be reworded.

8. **U-021 (three-phase rationale):** V2 wins on documentation completeness — V1 should add a one-paragraph "PRD-two-phase to TDD-five-milestone" mapping note.

**Net:** V1 retains the security-discipline and engineering-formalization majority. V2 wins the operational-detail majority. The honest synthesis is the merge described in R1's closing — neither variant standalone dominates, but V1 contributes more load-bearing security and engineering content while V2 contributes more operational polish.
