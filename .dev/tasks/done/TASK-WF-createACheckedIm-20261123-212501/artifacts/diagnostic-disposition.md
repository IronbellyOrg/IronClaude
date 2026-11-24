# Historical Diagnostic Disposition

## Fresh observations

Fresh pre-edit captures are ./public-before.txt (2026-11-24T15:18:58Z), bound to the current checkout, imported commands.py and commit 720cbaf96653c1c983497ba480f76ca6e60e5369. Public validate-lenses/scaffold help each exits 0 and advertises the unsupported option; run with that option exits 2 before any job. Expected observed status sequence is 0/0/2. ./scaffold-help-red.txt separately shows two collected root-command help regressions fail on their stale-option assertions; ./parser-before.txt shows the parser regression passes and its temporary directory stays empty.

These are new implementation observations, not retroactive validation of the copied diagnosis. Historical report and tasklist remain unchanged under .dev/troubleshoot/bug-swarm-custom-prompt-help-20261123191427/.

## Historical row applicability

| Historical row | New evidence / applicability | Historical state |
|---|---|---|
| P1-exact | New validate-lenses public capture exposes stale spelling, exit 0. Source producer commands.py:432-439 matches this wording. | Pending record preserved; new local evidence only |
| P2-exact | New scaffold public capture exposes stale spelling, exit 0. Source lens-option help commands.py:3773-3786 matches. | Pending record preserved; new local evidence only |
| P1-ref | Historical tasklist:19-20 prescribes identical validate-lenses --help form and predictions for exact/reference. No different control input or discriminatory outcome exists for this pair. The fresh capture covers that same form, not an independent control. | Applicability disposition here; not retroactively passed |
| P2-ref | Historical tasklist:21-22 likewise uses identical scaffold --help form and predictions. Fresh scaffold capture covers that form but cannot establish an independent control. | Applicability disposition here; not retroactively passed |
| control | Historical tasklist:23 gives a no-op with unknown true/false outcomes and says either is inconclusive. A no-op has no causal discrimination for the emitted wording. It is not needed to distinguish two visible source/help descriptions from the rejecting parser; no environment-property claim is made. | Inapplicable to this bounded wording comparison; pending original untouched |

## Limits

This record addresses the two exact-help observations and supplies an evidence-backed applicability decision for the identical reference/no-op rows. It does not prove a fixed state, full custom-job success, environment comparison, or independent applied-fix review. Repaired public outputs and applied-fix review are still required later. No counter-update.py invocation, shared-store edit, historical status rewrite, model-backed job or GitHub action occurred. User-requested path relocation happened before this implementation and is separately documented in the original report; no further historical evidence was changed.
