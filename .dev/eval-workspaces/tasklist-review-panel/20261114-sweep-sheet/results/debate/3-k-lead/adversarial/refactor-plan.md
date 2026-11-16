# Refactoring Plan

## Overview
- Base: V3 (sonnet:architect). Verdict: PASS, so no file is changed. This plan lists what was weighed and rejected, and what the owner may choose to record by hand.
- Review status: auto-approved (non-interactive).

## Planned Changes
None to any file. A PASS changes no file.

## Changes NOT Being Made (rejected alternatives, with the reason)
| # | Candidate edit to `briefs/k-lead.txt` line 2 | Why it was not made |
|---|---|---|
| R-1 | Add "Apply each one to the plan." (V3's design) | Untested wording; moves K toward SS-lite (a structural unit of coverage, MR 36); the direction of the current gap is not established; it would split the byte-identical RL copy (RL DR-16) that this task may not edit |
| R-2 | Drop "in your own review of" | No evidence says either wording is better; CB-5 stays verbatim (REQ-05); same RL split |
| R-3 | Replace "kinds of defect" with "checks" | A reading gain only; no outcome effect shown |
| R-4 | Add "skip any kind that names a document you were not given" | A conditional the owner did not ask for (MR 1035: plain words); not needed for fairness because D2 and D7 read found fraction only; the real gap is in the analysis, which this task may not edit |
| R-5 | Drop "A plan may have none of them, one of them or several" | The sentence is symmetric; base.txt and CB-2 already carry the no-quota and no-suppression rules |

## Optional by-hand records for the owner (advice only; not applied here)
1. In `results/owner-decisions.md`, when row 4 is confirmed: the sha256 `6712596b3c8d3e60ad8edb86755613ca9b12550f2198d04d303e1e68019afb57` (269 bytes) of `briefs/k-lead.txt`, the words "line 2 only; the eight definitions stay open until step 14.5", and the date.
2. Before step 14.5: `cmp` the SW and RL copies of `briefs/k-lead.txt` and of the eight `cards/C*.json` definitions; check the hold-out packages for `source: null`.
3. Reading rule for the report: K minus Z0 is the effect of this one paragraph as frozen, not the most a plain checklist could add; SS minus K is the effect of everything SS adds over the definitions alone, not of automation alone.

## Risk Summary
Not applicable (no change).
