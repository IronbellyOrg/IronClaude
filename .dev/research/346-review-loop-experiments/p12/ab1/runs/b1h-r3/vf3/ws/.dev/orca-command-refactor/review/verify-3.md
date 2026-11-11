# Verification 3: blocking findings R2-1 and M6

Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
sha256: `530bb94dc36fffb71a0dd0f59ecf0aa60e32ab1c485bde6cfedea040d97adda7`

Checks run with `grep -nF` and line reads inside the workspace. `INV-A` and `commands-b.md` are cited by the candidate but are not in the workspace, so any claim about their content is UNVERIFIED.

| id | found text | exists | outcome follows | confirm or reject | reason |
|---|---|---|---|---|---|
| R2-1 | Quote at `:201`: "steps 1-3 and 5-7 pass; step 3's report path is the one the command writes today" | no | no | reject | The phrase "the one the command writes today" does not occur. `:201` reads "steps 1-3 and 5-7 pass, with step 3 replaced for P0 (R2-1)". Step 3 at `:189` does exist verbatim ("Pass: exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path."), but `:189` and `:201` both route P0 to a replacement rule, so the unreplaced step 3 is not what P0 runs. |
| R2-1 | Sentence: troubleshoot's P0 report is `REPORT.md` (`:91`; `commands-b.md:49`) | yes (`:91`); `commands-b.md:49` UNVERIFIED | yes | (part of R2-1 sentence, not a separate test) | `:91` shows `REPORT.md` (`report_path`) for troubleshoot. `commands-b.md` is not in the workspace. |
| R2-1 | Sentence: "the contract does not exist before P1 (`:201`)" | yes | yes | (part of R2-1 sentence) | `:201` says "the contract arrives in P1". |
| R2-1 | Sentence: "Step 3 cannot pass, and P0 cannot pass" | yes (as a claim) | no | reject | `:201` gives the P0 rule for step 3: `troubleshoot` and `adversarial` have no `status`, so each passes when `--outcome succeeded` is sent exactly when the step-4 file is non-empty, `--outcome failed` otherwise, and its report path is that file. `:201` also replaces step 4 for P0 with a per-command check. The stated failure needs step 3 to run unreplaced, which the candidate text does not require. |
| M6 | Quote at `:201`: adversarial step 4, "`test -s` on its existing contract file (the inventory names no field list, `INV-A:35`)" | yes | no | reject | The quote exists verbatim. The stated outcome ("tests either the wrong file or no file, so step 4 ... cannot pass as written") needs an assumption that the implementer picks a wrong or absent file. The candidate does not force that. `:201` names no path, which leaves the check underdetermined, not contradictory. |
| M6 | "its report path is that file" (step 3 at `:201`, adversarial) | yes | (part of M6 sentence) | (part of M6 sentence) | Exists in `:201`. The step-3 text at `:189` says "the WC-4 contract path", not "that file", so the finding's claim that `:189` uses the same file is only true for `:201`. |
| M6 | "`spec:83`: filename not fixed" | yes | (part of M6 sentence) | (part of M6 sentence) | `:83` contains "contract, but filename not fixed" for adversarial. |
| M6 | "The inventory records two layouts (`INV-A:35`)" | UNVERIFIED (`INV-A` not in workspace) | (part of M6 sentence) | (part of M6 sentence) | Cannot be checked here. |
| M6 | Note: `:83` gives the P1 fix as `<output>/return-contract.yaml`, and P0 runs before P1 | yes | yes | (part of M6 note) | `:83` says "Fix the contract filename to `<output>/return-contract.yaml` ... (P1)". The P0 ordering is also in the phase table. |

confirmed: none
