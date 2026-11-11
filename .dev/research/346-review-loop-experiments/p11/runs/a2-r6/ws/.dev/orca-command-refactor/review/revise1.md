revise: 1 of 3

# Revise report: orca-worker-contract-spec.md

- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, edited in place. Input review: `.dev/orca-command-refactor/review/round1.md` (verdict FAIL, one blocking finding, F-01; `round1.md:211`, Reviser brief at `round1.md:213-220`).
- Brief followed: repair only F-01; prefer deleting or narrowing; add nothing a listed finding does not call for; cite the finding id on every addition; Medium and minor findings left alone; no PASS awarded; spec-panel not run.
- Evidence: only the spec, `round1.md`, the README and the inventories were opened. Citations of source files behind the spec's section 3 are UNVERIFIED here.

## Byte accounting

| Measure | Bytes |
|---|---|
| Spec size before | 57763 |
| Spec size after | 57880 |
| Net change | +117 |
| sha256 before | `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` |
| sha256 after | `5214f80e3dc9557f5cf50e915b26edd24f7757a9ce7975ec766b78482cde7fd6` |

| Finding id | Bytes added | Bytes deleted |
|---|---|---|
| F-01 | 117 (59 in AC-1.1, 58 in AC-1.2) | 0 |
| All other ids | 0 | 0 |

## Disposition, one row per finding id

| Finding id | Disposition | Where | Reason |
|---|---|---|---|
| F-01 | Applied | spec:195 (AC-1.1) and spec:196 (AC-1.2) | The grading sentence (`round1.md:89`) says AC-1.1 and AC-1.2 demand a `## Unattended mode` section and a contract file for `load`, while the `/sc:load` row (spec:112) and the Decisions row (spec:265) give it neither. Fix: both checks now state load's exemption, in place (AC-1.1 "except `load`"; AC-1.2 "except `load` ... step 4 cannot apply", step 4 being the contract check at spec:183). The `/sc:load` row (spec:112) and the Decisions row were left unchanged, so the stated load handling is kept and the checks now agree with it. Narrowing, not a new rule: no new section, mechanism or flag. |
| F-01 supporting note | Not applied (rejected) | spec:159 / spec:195 command-set mismatch (13 vs 37) | `round1.md:90` marks it "Supporting, not needed for the grade" and says the P1 scope sentence covers it for most commands. Re-pointing AC-1.1 at the P1 Commands column would drop the section checks for the P2-P4 commands that have none before their own phase (no P3 or P4 check asserts the section), which is a new gap. The other half of that note, pr-submit and decision D3, depends on an open decision and no blocking sentence names it. |
| F-02 to F-13 | Left alone | none | Graded Medium (`round1.md:94-175`); the brief and the Reviser brief (`round1.md:215-218`) say not to fix them this cycle. |
| N-01 to N-11 | Left alone | none | Minor notes; the brief says leave them alone. |

## Not done

- No self-awarded verdict. The revised candidate is returned once for the next review round.
