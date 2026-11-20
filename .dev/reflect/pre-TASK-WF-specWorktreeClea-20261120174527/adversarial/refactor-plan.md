# Refactoring Plan (merge of two review cards into one verdict)

## Overview

- Base: variant 2 (`variant-2-original.md`, qa lens, haiku class)
- Incorporated: variant 1 (`variant-1-original.md`), the debate files, the invariant probe
- Output: `merged-verdict.yaml` (a YAML document that holds the merged review verdict and findings)
- Changes planned: 9. Risk: Low (additive and regrading; no finding of either card is deleted)
- Grade rule used for every finding: BLOCKING only if correcting it would change a named decision, required behaviour, outcome or acceptance check the plan rests on, or a required deliverable is absent, or following the plan would lose or expose data, break a safety boundary or act outside declared scope; MEDIUM if a real weakness nothing named rests on; NOTE if wording only.

## Planned Changes

| # | Change | Source | Target | Rationale | Risk |
|---|---|---|---|---|---|
| 1 | Replace V2 F1 with the merged ordering finding M-1: hard cases PLAN lines 62, 73, 108, 161, 174 (BLOCKING); declared deferrals at 49, 63, 76, 85 are noted as not blocking; add V1's missing collector tests (U-003) and V2's Task 7 self-reference | V1 F1, V2 F1 | M-1 | C-001 verdict, 92%; both advocates agree | Low |
| 2 | Keep V2 F4 as M-2 (pull-request step has no owning task; BLOCKING, Missing) and add the INV-006 caveat: make it a final handoff note, not an executing task | V2 F4, INV-006 | M-2 | C-004; both advocates accept | Low |
| 3 | Add V1 F2 as M-3 (15 rows, not 14; BLOCKING, wrong number in an acceptance check; labels outside the three words) | V1 F2 | M-3 | C-005, 99% | Low |
| 4 | Add V1 F3 as M-4 (Task 1 gives item 2's fallback to item 1; BLOCKING, Decision) and add INV-002 (no verb for "deregister from Orca") | V1 F3, INV-002 | M-4 | C-006, 95% | Low |
| 5 | Add the new open-pull-request proof point as M-5 (spec section 11 item 3 asks OPEN, plan uses NONE; BLOCKING by the acceptance-check clause, small practical effect) | debate Round 2 | M-5 | both advocates accept | Low |
| 6 | Regrade V2 F2 to MEDIUM as M-7 (helper's `git fetch` and the recorder blind spot), keep V2's evidence lines | V2 F2, debate | M-7 | C-002 and X-001: the spec requires the helper call | Low |
| 7 | Regrade V2 F3 to MEDIUM as M-6 by orchestrator tie-break and list it as UNRESOLVED (V2 holds BLOCKING); keep it as a follow-up candidate for the owner | V2 F3, debate | M-6 | C-003: source.md:214 is permissive ("can still") and source.md:83 does not include it; plan discloses the drop | Medium (grade is disputed) |
| 8 | Add INV-001 (Task 20 asks for a command list in the JSON that no task writes; BLOCKING) and INV-003 (Task 2 is a denylist, the spec says allowlist; BLOCKING) | invariant probe | M-8, M-9 | HIGH, verified against the plan text | Low |
| 9 | Add the MEDIUM and NOTE invariant items as notes: INV-004, INV-005, INV-007, INV-008, INV-009 | invariant probe | notes | real weaknesses nothing named rests on, or form only | Low |

## Changes NOT Being Made

| Diff point | Non-base approach | Rationale |
|---|---|---|
| V1 F1 wording that Task 2 cannot pass | V1 | Overstated: most of Task 2's checks pass when it ends (V1 conceded); only the refusal assertion looks ahead |
| V1 PLAN:99 attribution to Task 8 | V1 | Wrong: that line belongs to Task 6 (calibrator and V1 concession) |
| V2 F2 as BLOCKING | V2 | The spec requires the call (source.md:299) and defines "changes nothing" as no removal (source.md:256) |
| V2 self-reported confidence 0.95 | V2 | Two of four BLOCKING grades did not hold |

## Risk Summary

Every change is additive or a regrade documented from the debate; the merged verdict keeps FAIL, which both cards and every debate position support.

## Review Status

Auto-approved (non-interactive).
