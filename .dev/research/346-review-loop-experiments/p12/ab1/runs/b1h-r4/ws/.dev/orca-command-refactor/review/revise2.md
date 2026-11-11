# Revise 2 of the Orca worker-contract spec

REVISE prompt (`~/.claude/rules/prompts/document_review_loop_prompts.md:60-62`), run on the review 2 report `review/round2.md` (`review: 2 of 3`, verdict FAIL) and its verification block `review/verify-2.md`.

- Candidate revised in place: `specs/orca-worker-contract-spec.md`
- IDS: `N2` only. The VERIFY reply (`review/verify-2.md:13`, `confirmed: N2`) confirmed one blocking id. M2 and N1 were rejected, so they are noted, not revised (`review/round2.md:2`).
- Candidate sha256 before: `6f240e27e8d58d66b8256a439936eb55132bda0b917254aa463c5abc36931750` (matches `review/round2.md:8` and `review/verify-2.md:3`)
- Candidate sha256 after: `005c14750dde7985fd4ffcf42529a7b23cc2ca06ed4169b3ad679316a9e00f9a`
- Change count: one cell edited, in one line (`specs/orca-worker-contract-spec.md:86`). No other line changed.

## Byte accounting

| Measure | Bytes |
|---|---|
| Candidate before (`wc -c`) | 60372 |
| Candidate after (`wc -c`) | 60539 |
| Net change | +167 |
| Total bytes deleted | 66 |
| Total bytes added | 233 |

Per finding id:

| Finding id | Bytes deleted | Bytes added | Net |
|---|---|---|---|
| N2 | 66 | 233 | +167 |
| M2 | 0 | 0 | 0 (the cell keeps its `[M2]` tags and its "Fresh dir per run" and "Per-run output directory (P1)" text) |
| N1 | 0 | 0 | 0 |
| F1-F5, M1, M3, M5 | 0 | 0 | 0 |

The deleted text is `` `--output <dir>` after P1 (the flag becomes directory-valued) [M2] `` (66 bytes, the "Brief must pass" cell of the init-lite row). The added text is `` `--unattended --output <dir>/context-audit.md` after P1, with a fresh `<dir>` per run (`<dir>` is the WC-4 output directory, so the contract is `<dir>/return-contract.yaml`); standalone `--output <file>` is unchanged (SA-1) [N2] [M2] `` (233 bytes).

## Rows per finding id

| Id | Disposition | Where | Reason with citation |
|---|---|---|---|
| N2 | Applied | `specs/orca-worker-contract-spec.md:86` (3.1 init-lite row, "Brief must pass" cell) | The defect was that the row made `--output` directory-valued for every run. Its stated text at `specs/orca-worker-contract-spec.md:86` had no `--unattended` qualifier, while SA-1 (`specs/orca-worker-contract-spec.md:147`) and the section 5 hard requirement (`specs/orca-worker-contract-spec.md:143`) keep every output path unchanged without `--unattended`. The repair follows the round-2 recommendation (`review/round2.md:120`): standalone `--output <file>` stays a file, and the unattended brief passes a fresh per-run file under a fresh `<dir>`. The edit also names the WC-4 contract path (`specs/orca-worker-contract-spec.md:62`), so the brief's `<dir>` is the output directory WC-4 uses. The baseline `--output <file>` is confirmed at `specs/history/spec-v1.md:87` (the line is present in the workspace; `verify-2.md:5` says the file is absent, and that statement is incorrect for this workspace). |
| M2 | Not revised (rejected by VERIFY) | Not edited beyond the N2 cell; its `[M2]` tags and the "Fresh dir per run (WC-6)" and "Per-run output directory (P1)" text at `specs/orca-worker-contract-spec.md:86` are unchanged | Rejected by the verifier (`review/verify-2.md:9`): the row tags the fix P1, and the P1 scope at `specs/orca-worker-contract-spec.md:160` covers "the small fixes to ready commands". Not in IDS, so not repaired. Rejected findings are never revised. |
| N1 | Not revised (rejected by VERIFY) | Not edited; the phrase "after P1" in the N2 cell is kept as it was | Rejected by the verifier (`review/verify-2.md:11`): the overwrite outcome does not follow, because `specs/orca-worker-contract-spec.md:160` includes "the small fixes to ready commands", and the dispatch outcome rests on `spec-v1.md:87`, which the verifier said was absent. The file is present (see N2 row), so the verifier's stated premise is wrong for that point; the readiness wording of `specs/orca-worker-contract-spec.md:79` and `:159` remains inconsistent with the row, as the verifier noted. Not in IDS, so left alone. |
| F1 | Left alone (Medium, not in IDS) | `specs/orca-worker-contract-spec.md:56,140` | Medium follow-up (`review/round2.md:125`). Not in IDS. |
| F2 | Left alone (Medium, not in IDS) | `specs/orca-worker-contract-spec.md:87`, P0 row at `:85` | Medium follow-up (`review/round2.md:126`). Not in IDS. |
| F3 | Left alone (Medium, not in IDS) | `specs/orca-worker-contract-spec.md:111` | Medium follow-up (`review/round2.md:127`). Not in IDS. |
| F4 | Left alone (Medium, not in IDS) | `specs/orca-worker-contract-spec.md:186` | Medium follow-up (`review/round2.md:128`). Not in IDS. |
| F5 | Left alone (note, not in IDS) | `specs/orca-worker-contract-spec.md:85` | Note (`review/round2.md:129`). Not in IDS. |
| M1, M3, M5 | Left alone (notes carried from round 1) | `review/round2.md:133-135` | Carried notes, not blocking. Not in IDS. |

## Checks run

- `wc -c` before the edit: 60372 bytes. After: 60539 bytes. The arithmetic (233 - 66 = 167) matches the net change.
- Only one `Edit` call was made, on `specs/orca-worker-contract-spec.md`. No other file in the workspace was written.
- `grep -c 'directory-valued'` on the candidate after the edit returns 0, so no line still says the flag is directory-valued.
- `grep -n 'N2\]'` finds one line, `specs/orca-worker-contract-spec.md:86`.
- The cited lines were re-read after the edit: `specs/orca-worker-contract-spec.md:62` (WC-4), `:64` (WC-6), `:79` (3.1 header), `:143` and `:147` (section 5, SA-1) are unchanged.
- Spec-panel was not run, and no finding was regraded.

## Coverage and limits

- Read: the REVISE prompt (`~/.claude/rules/prompts/document_review_loop_prompts.md:60-62`), `.dev/orca-command-refactor/README.md`, `review/round2.md`, `review/verify-2.md`, the full candidate, and `specs/history/spec-v1.md:85-89`.
- Not read: the inventories under `inventory/` were not needed for this single-cell repair. Citations to `cmd/init-lite.md:32`, `sk/sc-init-lite-protocol/SKILL.md:66,70` and the CAPS lines are carried from the spec and are UNVERIFIED here, because those files are outside the workspace.
- UNVERIFIED: `cmd/init-lite.md:32` (whether the command's `--output` accepts a directory in the unattended path), since the command file is not in the workspace. The N2 repair does not depend on that answer, because it keeps the flag file-valued.
