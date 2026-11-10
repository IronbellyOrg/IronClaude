# Verification 3: finding N6 against the candidate spec

Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
Candidate sha256: `5c1ab8696d3015841916a6b721ba37673ca41cc95d7518dd2f44d176aa42898f`
(The brief gave no expected hash, so this is recorded for the record and not compared.)

| id | found text (candidate line) | exists | outcome follows | verdict | reason |
|---|---|---|---|---|---|
| N6 | SPEC:62 (WC-4): "In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)". SPEC:83 (adversarial row, brief column `--output <dir>`): "Fix the contract filename to `<output>/adversarial/return-contract.yaml` (P1)". SPEC:206: "its direct-route check is AC-1.2, which runs after AC-1.4 fixes the filename". SPEC:210 (AC-1.4): "adversarial names one fixed path", no path given. SPEC:194 (7.2 step 3): report path must be "the WC-4 contract path in P1 and later". SPEC:208 (AC-1.2) runs 7.2 on each P1 command except `load`; SPEC:159 lists adversarial fixes in P1. | yes (both quotes verbatim; SPEC:206 and SPEC:210 verbatim) | yes | confirm | Both texts are in the candidate and name different files for the same command (`<dir>/return-contract.yaml` vs `<dir>/adversarial/return-contract.yaml`). Following the SPEC:83 row writes the contract where WC-4 forbids it. SPEC:62 says the worker passes the contract path as `--report-path`, and SPEC:194 requires that path to equal the WC-4 path, so the step-3 check fails for that build with no added assumption. The SPEC:206 dependency is also as stated: AC-1.4 (SPEC:210) names no path, so the filename fix is the SPEC:83 row. |

Notes on what could not be checked:
- BASE:62 and BASE:83 (the claimed baseline origin) are not in the workspace, so the "unchanged from baseline" claim is UNVERIFIED. It does not affect the outcome, which rests on the candidate text alone.
- INV-A:35 and INV-A:60 are cited as evidence but no inventory file is in the workspace. The candidate itself repeats the INV-A:35,60 citation at SPEC:206, so the claim that the skill names no filename is only UNVERIFIED here. The confirmation does not depend on it.
- The "review-2 diff scope" statement is not checkable from the workspace and is not used in the verdict.

confirmed: N6
