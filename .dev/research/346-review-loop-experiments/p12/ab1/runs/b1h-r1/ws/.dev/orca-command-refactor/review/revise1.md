review: revise 1 of 3 (REVISE prompt, document_review_loop_prompts.md)

Input: `.dev/orca-command-refactor/review/round1.md` (merged first review, verdict FAIL; Reviser brief lists M1 to M10). Verifier reply `.dev/orca-command-refactor/review/verify-1.md`, last line `confirmed: M1 M2 M3 M4 M5 M6 M7 M8 M9 M10`.
Candidate (edited in place): `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
sha256 before: d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d (matches `round1.md:5`)
sha256 after: 260c7c0ee1cfff6f147fa7f24960981dd4f6f1f953afdeef2b24a0b090d875da

Citations: `spec:N` is line N of the candidate after revision. `INV-A:N` and `INV-B:N` were checked against `.dev/orca-command-refactor/inventory/commands-a.md` and `commands-b.md`. Citations to `sk/`, `cmd/`, `CAPS:` and `src/` paths outside this workspace are UNVERIFIED and were not relied on for any edit.

## Byte accounting

Before: 57763 bytes, 285 lines. After: 59812 bytes, 293 lines. Net +2049 bytes.

Method: line-level. Each changed line counts its full old bytes as deleted and its full new bytes as added. A changed line tagged with several ids splits its bytes evenly among them. Lines of the new AC-C1 code block (spec:180-184) count under M4.

| id | bytes deleted | bytes added | net |
|---|---|---|---|
| M1 | 1450.0 | 1686.0 | +236.0 |
| M2 | 513.5 | 742.5 | +229.0 |
| M3 | 96.5 | 195.5 | +99.0 |
| M4 | 644.5 | 972.0 | +327.5 |
| M5 | 471.0 | 639.5 | +168.5 |
| M6 | 557.0 | 675.0 | +118.0 |
| M7 | 506.5 | 741.5 | +235.0 |
| M8 | 130.0 | 328.0 | +198.0 |
| M9 | 983.0 | 1224.5 | +241.5 |
| M10 | 393.0 | 589.5 | +196.5 |
| total | 5745.0 | 7794.0 | +2049.0 |

## Disposition per finding id

No Medium or minor finding was touched. No prior blocking finding was rejected by the verifier, so none is listed as noted, unactioned.

| id | disposition | where (spec line) | change and evidence |
|---|---|---|---|
| M1 | applied | WC-4 at `spec:62`; cleanup-audit row `spec:85`; index-repo row `spec:86` | WC-4 now says that when the output flag names a file (`--output <file>`, tdd and init-lite at `spec:90`, `spec:87`), `<output-dir>` is the file's parent directory. cleanup-audit and index-repo gain an `--output-dir` flag for the contract in unattended mode, which removes the fixed-path gap. INV-A:42 (`.claude-audit/` fixed, no output flag) and INV-A:53 (`PROJECT_INDEX.md`, location implied) were checked. |
| M2 | applied | 7.2 step 4 at `spec:191`; AC-0.4 at `spec:202` | Step 4 is now marked "From P1". In P0, step 4 applies to workflow only, whose contract exists today (INV-B:272). For troubleshoot and adversarial, P0 uses `test -s` on the command's own report, with no YAML assertion. The adversarial report filename is not named in this workspace, so it is UNVERIFIED. The "`--caller task-unified`" claim in verify-1 is not in the candidate and was not used. |
| M3 | applied | 3.1 intro at `spec:79` | The sentence "The only command changes are the small fixes" is replaced. From P1, every 3.1 command gains `--unattended` and the `## Unattended mode` section, which AC-1.1 (`spec:195`) checks. |
| M4 | applied | P0 row `spec:158`; AC-C1 row `spec:172`; scan block `spec:178-185` | The AC-C1 pattern moved out of the table into a code block, unescaped (`\|` removed), with the contract file exempt by path (`^src/superclaude/core/WORKER-CONTRACT\.md:`). P0 requires the HOW-WE-WORK Orca section to name no Orca subcommand, so AC-C1 passes it. Rejected sub-claim, M4.c "the routing guide has no permitted form at all": SA-2 (`spec:147`) governs command, skill and agent files only, so it does not bar HOW-WE-WORK; the fix is to the scan, not to SA-2. The second outcome in M4.a rests on a P0 text the candidate does not require; it was not used. |
| M5 | applied | WC-4 `spec:62`; adversarial row `spec:83`; workflow row `spec:92` | Adversarial in unattended mode writes `<output-dir>/return-contract.yaml`, not the `adversarial/` subfolder, so it matches WC-4. Workflow gains `--output-dir`, so the contract path is known before dispatch. The package stays at `.dev/tasks/to-do/<id>/`. INV-B:272 was checked: the contract is `.dev/tasks/to-do/<id>/return-contract.yaml`, written on post-creation outcomes and not for pre-creation STOPs (INV-B:272, citing its `:39`). |
| M6 | applied | WC-3 `spec:61` | Added: the exception is the `/sc:implement` Ruling; a relayed answer is never accepted as a Ruling until D2 is decided. The candidate defines no Ruling flag, so this sentence is what keeps WC-3 from reaching the implement row (`spec:109`). |
| M7 | applied | 7.2 step 3 `spec:190`; AC-0.4 `spec:202` | Step 3's contract-path clause is marked "from P1; in P0, AC-0.4 applies". AC-0.4 now drops the contract-path clause for P0 and checks the outcome against the command's own report status under WC-5. |
| M8 | applied | 7.2 step 6 `spec:193` | Split by command class. Report-only commands show files under the output directory. Edit-in-place commands (cleanup and improve, P2) also show the files their contract lists under `artifacts` (WC-4), and the contract must list every applied edit. |
| M9 | applied | 3.1 intro `spec:79`; section 2.3 `spec:73`; P0 row `spec:158` | Option 2 of M9's recommendation: P0 smoke runs use the ready commands without `--unattended`, because the flag arrives in P1. Section 2.3 now says the flag is from P1 on. The 3.1 intro says the flag applies from P1. Rejected sub-claim: the claim that brainstorm and init-lite "cannot pass" AC-1.1 because their small-fix cell says "None" is overstated (verify-1), since the P1 blanket at `spec:159` covers them. Those cells were left unchanged. |
| M10 | applied | adversarial `spec:83`; cleanup-audit `spec:85`; index-repo `spec:86`; workflow `spec:92`; WC-4 `spec:62` | Workflow gets an explicit `--output-dir`. Cleanup-audit and index-repo get one for the contract. Adversarial follows WC-4 (M5). init-lite is covered by the file-parent rule in WC-4 (M1). Rejected sub-claims: "no phase gives workflow an output directory" is contradicted by the P1 bullet at `spec:159`, so no separate change was made beyond naming the flag in its row. "Adds neither a contract nor an output flag" for cleanup-audit and index-repo is contradicted by the P1 blanket at `spec:159`; their rows now name the flag explicitly. |

## Residual notes
- The `--output-dir` flags for cleanup-audit, index-repo and workflow are new interface additions. Each is cited to M1, M5 or M10 in the spec.
- `spec:190` and `spec:202` keep their P0 checks narrow on purpose. They depend on the command's own report file, whose name for adversarial is UNVERIFIED.
- The follow-up candidates in round1.md were not merged or edited.
