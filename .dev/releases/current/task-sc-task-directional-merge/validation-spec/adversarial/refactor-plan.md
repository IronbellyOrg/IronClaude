# Refactoring Plan — Merge Variant-2 (Base) with Variant-1 + Variant-3 Strengths

## Overview

- **Base variant:** variant-2 (adversarial-attack stance; combined score 0.947)
- **Incorporated variants:** variant-1 (steelman), variant-3 (security-probe)
- **Change count:** 14 planned changes; 3 rejected alternatives
- **Risk:** Medium overall — additive merges with one structural reframe (executive section converts from indictment to balanced verdict)
- **Approval:** auto-approved (non-interactive mode)

## Planned Changes

### Change 1 — Executive section reframe (V2 § 1 → balanced verdict)

- **Source variant and section:** V2 § 1 (indictment) + V1 § 1 (defense) + V3 § 11 (partial-affirm)
- **Target location in base:** § 1 of merged spec (replaces V2's pure-indictment opening)
- **Rationale (citing debate evidence):** Round 2 / Round 3 consensus that V3's partial-affirm framing is most operationally honest (S-006 winner: V3, 70% confidence; X-006 winner: V3, 75% confidence). The merged spec opens with the dual claim: (a) closures are correctly dispositioned at the level the plan defines them (V1 wins this); (b) closure predicates are under-specified against degenerate inputs (V2 wins this); (c) six timeline / tooling-layer hazards survive at a layer the plan does not reach (V3 wins this).
- **Integration approach:** restructure
- **Risk level:** Medium — changes the document's stance signal but is required for honest convergence

### Change 2 — Insert TU/ME positive-validation overlay (from V1 §§ 2–3)

- **Source variant and section:** V1 § 2 (per-TU steelman) + V1 § 3 (per-ME load-bearing)
- **Target location in base:** new § 2 in merged spec (positioned before the attack list)
- **Rationale:** V1's "invariants protected" + "alternative that would weaken INV" framework is the only generative defense in any variant (U-001, U-002 — value: High). Conceded by V2 in Round 2 ("V1 per-TU steelman is generative"). The defense overlay tells future reviewers what to keep before the attack list tells them what to harden.
- **Integration approach:** insert before V2's attack sections
- **Risk level:** Low — additive

### Change 3 — Adopt V3 96-file empirical evidence (V3 § 2)

- **Source variant and section:** V3 § 2 (in-flight MDTM enumeration)
- **Target location in base:** new § 3 in merged spec (empirical exposure section)
- **Rationale:** V3's live grep evidence is decisive (C-011 winner: V3, 95% confidence; C-013 winner: V3, 100% confidence). 96 task files, 149+ refs in named PRD subtree — empirically grounds the abstract attacks in V2.
- **Integration approach:** insert as new section
- **Risk level:** Low — purely empirical

### Change 4 — Replace V2 § 2 CR-FM-* attacks with consolidated INV-04 semantic-vs-parse frame

- **Source variant and section:** V3 § 7 (in-flight resumability) + V2 § 2.3 (CR-FM-03 shim sunset)
- **Target location in base:** § 4 of merged spec (replaces V2 § 2 with parse-vs-semantic split)
- **Rationale:** V3 § 7 demonstrates INV-04 resumability has parse-level guarantee and semantic-level exposure (X-005 winner: V3, 95% confidence). V2's shim-sunset attack stands as a sub-finding. Round 3 resolved by adopting CR-FM-03 content-level audit with warn-and-continue HALT disposition per ME-3.
- **Integration approach:** restructure V2 § 2 to organize around the parse-vs-semantic distinction
- **Risk level:** Medium — restructures a section

### Change 5 — Preserve V2 § 3 CR-TASK-* attacks but apply V1's input-invalid asymmetry distinction

- **Source variant and section:** V2 § 3 (CR-TASK-* attacks) + V1 R2 (F-03 asymmetry distinction)
- **Target location in base:** § 5 of merged spec
- **Rationale:** V2's CR-TASK-* attacks are largely correct and most are not refuted. V2 conceded the F-03 asymmetry distinction in Round 2 (X-002 winner: V1, 75% confidence). The AC-ATK-10 (unified pre-loop HALT policy table) text changes to distinguish "input-invalid" rows from "environment-non-ideal" rows.
- **Integration approach:** modify V2 § 3.2 (CR-TASK-02) and § 3.4 (CR-TASK-06) language to use the asymmetry; AC-ATK-10 amended
- **Risk level:** Low — language tightening

### Change 6 — Preserve V2 §§ 4–5 (CR-DEP, CR-DIST, CR-REF, CR-DOC attacks) verbatim

- **Source variant and section:** V2 §§ 4–5
- **Target location in base:** § 6 of merged spec
- **Rationale:** Bucket-condensation and row-count gaps (C-008, C-009 winners: V2 at 95%, 90%) and CR-DOC disambiguation (C-015) are unique to V2 and unrefuted. Adopt verbatim.
- **Integration approach:** append; no language changes
- **Risk level:** Low

### Change 7 — Adopt V3 §§ 3–5 sequencing-constraint probes

- **Source variant and section:** V3 § 3 (S-1 probe), § 4 (S-2 probe), § 5 (S-3 probe)
- **Target location in base:** new § 7 of merged spec (sequencing constraint probes)
- **Rationale:** V3 dominates sequencing-constraint analysis (C-005, C-006, C-007 winners: V3 at 85%, 90%, 80%). `--max-wait` + pinned-SHA (S-1), server-side pre-push hook (S-2), `flock` (S-3) are concrete operational mitigations V1 and V2 did not produce.
- **Integration approach:** insert as new section
- **Risk level:** Low — additive

### Change 8 — Adopt V3 § 6 post-CR-DEP-03 residual-reference probe

- **Source variant and section:** V3 § 6
- **Target location in base:** new § 8 of merged spec
- **Rationale:** Concurrent with V2 § 3.10 on CR-TASK-12 fragility. CR-DEP-06 proposal (V3 § 6) is the operational mitigation V2 left at the AC-level only.
- **Integration approach:** insert
- **Risk level:** Low

### Change 9 — Preserve V2 § 6 INV-01..INV-05 attack vector table + augment with V3 § 9 invariant corrections

- **Source variant and section:** V2 § 6 + V3 § 9
- **Target location in base:** § 9 of merged spec
- **Rationale:** V2's table is the broadest invariant-attack mapping; V3 § 9 adds INV-03 SKILL.md:191-198 anchor brittleness and INV-04 96-file exposure as concrete row qualifications.
- **Integration approach:** merge tables row-by-row; V3 entries augment V2 entries
- **Risk level:** Low

### Change 10 — Merge V2 § 7 (scenarios A..G) + V3 § 8 (scenarios H-1..H-4)

- **Source variant and section:** V2 § 7 + V3 § 8
- **Target location in base:** § 10 of merged spec
- **Rationale:** V2's 7 scenarios are predicate-level; V3's 4 scenarios are timeline-level. Together they cover both layers.
- **Integration approach:** append V3 scenarios after V2 scenarios; renumber as A..G then H-1..H-4
- **Risk level:** Low

### Change 11 — Adopt consolidated acceptance-criteria list (AC-ATK-01..18 + AC-SM-01..12)

- **Source variant and section:** V2 § 8 (AC-ATK-01..15) + V3 § 10 mitigations table + V1 § 7 (AC-SM-01..12)
- **Target location in base:** § 11 of merged spec
- **Rationale:** V2's gap-closure ACs are the primary list. AC-ATK-16 (flock), AC-ATK-17 (server-side pre-push hook), AC-ATK-18 (CR-FM-03 content audit) added from V3. AC-SM-01..12 from V1 added as positive validation tests in a separate subsection.
- **Integration approach:** combine into one numbered list with subsections
- **Risk level:** Low

### Change 12 — Preserve V2 §§ 9–11 (tradeoffs, failure modes, evidence audit) verbatim

- **Source variant and section:** V2 §§ 9–11
- **Target location in base:** §§ 12–14 of merged spec
- **Rationale:** All three sections are unique to V2 (U-010, U-011, U-012 — value: High). Adopt verbatim.
- **Integration approach:** append; no changes
- **Risk level:** Low

### Change 13 — Add V1 § 6 "Honest concessions" as a residual-risk section

- **Source variant and section:** V1 § 6
- **Target location in base:** new § 15 of merged spec
- **Rationale:** V1's 5 concessions identify entry points the attack list does not flag as "concession from the steelman side." Useful for downstream reviewers who want to understand which attacks the steelman acknowledges as legitimate.
- **Integration approach:** insert as new section
- **Risk level:** Low

### Change 14 — Verdict synthesis (replaces V2 § 12 with three-way verdict)

- **Source variant and section:** V1 § 7 verdict claim + V2 § 12 verdict + V3 § 11 verdict
- **Target location in base:** § 16 of merged spec
- **Rationale:** S-006 + X-006 both go to V3 (partial-affirm). The merged verdict states: (a) closures resolve Phase-7-named findings (V1 holds); (b) closure predicates are under-specified against 18 falsifiable gaps (V2 holds); (c) 6 timeline-layer hazards survive (V3 holds). Phase 7.5 patch list is the unified remediation.
- **Integration approach:** restructure V2 § 12 into a three-clause verdict
- **Risk level:** Medium — verdict reframing

## Changes NOT Being Made

### Rejected: V1's ratification-only framing of "ZERO OPEN FINDINGS"

- **Diff point:** X-006
- **V1 approach:** Treat the source plan's "ZERO OPEN FINDINGS" claim as ratified by the steelman.
- **Rationale for rejection:** V2 + V3 consensus (X-006 winner: V3 partial-affirm at 75% confidence) is that the claim survives only at the predicate-precision layer the plan defines, not at the operational layer. Ratifying it would erase 18 falsifiable gaps + 6 timeline-layer hazards.

### Rejected: V2's pure-indictment framing in § 1

- **Diff point:** S-006 / X-006
- **V2 approach:** Open with "The 'ZERO OPEN FINDINGS' claim does not survive."
- **Rationale for rejection:** V1's R2 conceded several attacks but also surfaced load-bearing defenses (per-TU invariant protection, asymmetry distinction) that V2 did not refute. The merged spec opens with a balanced verdict rather than a one-sided indictment.

### Rejected: V2's md5sum collision attack as a HIGH-priority finding

- **Diff point:** C-014
- **V2 approach:** Include CR-TASK-11 md5 → sha256 mitigation as AC-ATK-09.
- **Rationale for rejection:** Adversarial-only concern with negligible accidental-collision probability. Demote to LOW-severity informational note; keep the sha256 recommendation but not as a blocking AC.

## Risk Summary

| Change | Risk | Impact | Rollback |
|---|---|---|---|
| 1 (executive reframe) | Medium | Document opening stance | Revert to V2 § 1 verbatim |
| 2 (TU/ME overlay insert) | Low | Adds defense framework | Remove new section |
| 3 (V3 evidence section) | Low | Adds empirical section | Remove new section |
| 4 (INV-04 restructure) | Medium | Reorganizes one section | Revert V2 § 2 verbatim |
| 5 (V1 asymmetry edits) | Low | Tightens language | Revert AC-ATK-10 |
| 6–10 (verbatim adopts) | Low | Adds content | Trim sections |
| 11 (consolidated ACs) | Low | Merges three lists | Split back into V1/V2/V3 lists |
| 12–13 (verbatim adopts) | Low | Adds content | Trim sections |
| 14 (verdict synthesis) | Medium | Final verdict reframed | Revert to V2 § 12 |

## Review Status

- **Mode:** non-interactive (auto-approved per default)
- **Approval:** auto-approved at 2026-05-15
- **Override path:** any reviewer may re-run with `--interactive` and modify the plan before merge execution.
