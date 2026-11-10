# Revise 1

Candidate: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md (edited in place). Blocking ids repaired: M1, M2, M5, M6, M7, M8, M9. M3 and M4 untouched (verifier-rejected, `review/round1.md:83-90`). Minor and Medium findings left alone. No PASS is awarded; the candidate goes back to review.

## Byte accounting

Size before 57763 bytes, after 59678 bytes (net +1915). Added and deleted bytes are word-level diff totals per finding id (so a reworded clause counts its old words as deleted and its new words as added).

| id | bytes added | bytes deleted | net |
|---|---|---|---|
| M1 | 457 | 119 | +338 |
| M2 | 295 | 38 | +257 |
| M5 | 384 | 102 | +282 |
| M6 | 230 | 108 | +122 |
| M7 | 276 | 0 | +276 |
| M8 | 220 | 53 | +167 |
| M9 | 481 | 8 | +473 |
| total | 2343 | 428 | +1915 |

Each addition cites its id in the spec where it is a new sentence (M1, M2, M5, M6, M7 in WC-4, the section 3 intro and section 2.3). Narrowed table cells (AC-0.4, AC-1.1, AC-1.2, AC-1.4, AC-2.2, the P1 scope cell, the load and workflow rows, SA-4) carry no inline tag; their ids are given below.

## Findings

All line numbers are in the revised spec unless marked.

| id | disposition | where applied | what changed |
|---|---|---|---|
| M1 | applied | WC-4 (`:62`); section 3 intro "Contract" definition (`:76`); workflow row (`:92`); SA-4 (`:149`); P1 command list (`:159`) | WC-4 now gives one path rule with stated exceptions instead of the single `<output-dir>` path: adversarial, file-valued `--output`, fixed locations (see M6, M7), and workflow, the one path not known before dispatch because the run generates `<id>` (`INV-B:272`). A workflow stop before the package exists writes no contract and the worker sends `--outcome failed` under WC-5 (`:63`, existing "or no report exists"). This deletes the workflow row's "write the contract for pre-creation STOPs" fix, which could not be met without an id (`INV-B:272` states the contract is not written for pre-creation STOPs). "Contract" in section 3 now means the file at the path WC-4 gives. Workflow was removed from the P1 fix list and SA-4's "adversarial and workflow contract gaps" became "the adversarial contract filename". |
| M2 | applied | section 3 intro (`:76`); P1 scope (`:159`); AC-1.1 (`:195`) | Population narrowed to commands whose row names a change in the phase. `## Unattended mode` is gained only by commands whose row names an unattended-mode change in P1-P3. brainstorm and init-lite (rows say "None", `:84`, `:87`), load (`:112`) and the P4 commands implement, post-release, pr-submit (decisions D2-D4, `:240`) are excluded in P1-P3. AC-1.1 asserts the section only for that population. The P1 scope no longer says "every command in sections 3.1 and 3.2". |
| M5 | applied | section 2.3 (`:73`); AC-0.4 (`:194`) | The P0 brief no longer includes `--unattended` (2.3 now says "only for a command that already has the section (P0 runs without it)"). AC-0.4 now runs steps 1, 2 and 5-7; in step 3 the report path is the command's existing report file (3.1 "Report today" column) with `--outcome succeeded` when it exists; step 4 is `test -s` on that file only, since the contract and `status` arrive in P1. The wrapper check moved into the step-5 transcript search, which now also looks for an Agent-tool call wrapping the command. |
| M6 | applied | WC-4 (`:62`); AC-1.4 (`:198`) | Chose the second of the two repairs the finding offers: WC-4 gains the single exception "adversarial: `<output>/adversarial/return-contract.yaml`", matching row 83 and the artifact layout at `INV-A:35`. Row 83 is unchanged. AC-1.4 now asserts that exact path and drops the workflow clause (workflow clause removed under M1). |
| M7 | applied | WC-4 (`:62`) | tdd and init-lite (file-valued `--output`, rows `:87`, `:90`): contract is `<output-file>.return-contract.yaml`. cleanup-audit and index-repo (fixed output locations, rows `:85`, `:86`): `.claude-audit/return-contract.yaml` and `PROJECT_INDEX.return-contract.yaml` at the repository root. Workflow is handled under M1. AC-1.2 and AC-2.2 now resolve through these paths; the AC-2.2 example `/sc:tdd "auth" --unattended --output <file>` has a defined contract file. The index-repo repository-root location is `INV-A:53` "location implied, UNVERIFIED"; it is a path choice for the implementer, not a claim about today's behavior. |
| M8 | applied | load row (`:112`); P1 command list (`:159`); AC-1.2 (`:196`) | load's row states "no `## Unattended mode` section, no `--unattended`, no contract"; the P1 list repeats it; AC-1.2 excludes load. AC-1.1 exclusion of load is under M2. |
| M9 | applied | AC-2.2 (`:200`) | AC-2.2 gate-trigger run now applies to the nine commands whose rows resolve a gate as blocked: cli-eval, cli-portify, recommend, review-translation, release-split, tdd, troubleshoot, task, and spec-panel with a TDD input (rows `:104`, `:105`, `:115`, `:117`, `:89`, `:90`, `:91`, `:121`, `:120`). The other six get a one-line expected result: auggie-review by AC-2.4; cleanup and improve by a contract listing the "Approval Required" items unapplied (rows `:103`, `:110`); research, reflect and tasklist by AC-2.3 with no `agentWait` (rows `:116`, `:88`, `:122`). |

## Checks and limits

- The 15 P2 commands in `:160` split 9 + 6 across the two groups above, with none dropped.
- Section 3.1 rows 83-92 and every other section were not otherwise touched.
- The inventory lines cited here (`INV-A:35`, `INV-A:53`, `INV-B:272`) were read in `.dev/orca-command-refactor/inventory/`. Orca guide citations in the spec were not rechecked; they are inventory-derived and outside the blocking findings.
- Not verified here: whether `<output-file>.return-contract.yaml` and the fixed-location file names fit the real commands. They are new names the implementer must confirm in the phase plan.
