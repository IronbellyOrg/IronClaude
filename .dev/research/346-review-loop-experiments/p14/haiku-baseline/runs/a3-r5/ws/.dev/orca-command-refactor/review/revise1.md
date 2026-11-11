# Revise 1: Orca worker-contract spec

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (edited in place)
- brief: repair only the blocking findings F-01, F-02, F-03, F-04 from `.dev/orca-command-refactor/review/round1.md` (its `Reviser brief`, line 254)
- candidate before: 57763 bytes, 285 lines, sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` (matches the hash in `review/round1.md:5`)
- candidate after: 59142 bytes, 291 lines, sha256 `013a84aaca6a86058868c7f7b79fe52a951e5bbb08547665cff18e7d59d845ed`
- net change: +1379 bytes (+6 lines)
- Medium and minor findings were not edited. The spec was not re-reviewed and no PASS is claimed.

## Read for this revision
`.dev/orca-command-refactor/README.md` (shared context), `review/round1.md` (all findings), the candidate (all lines), `inventory/commands-a.md` and `inventory/commands-b.md` (for the rows named by F-03 and F-04). `inventory/orca-capabilities.md` was not read; no edit depends on it. Citations below are checked against files inside the workspace. Anything outside it is UNVERIFIED.

## Byte accounting

Computed with `python3 -I` over the exact old and new strings of each edit (UTF-8 bytes). The sum of the edits equals the file-size change, which was checked against `wc -c`.

| Finding | Bytes added | Bytes deleted | Net | Edits |
|---|---|---|---|---|
| F-01 | 375 | 147 | +228 | spec line 188 (7.2 step 3); line 200 (AC-0.4) |
| F-02 | 682 | 310 | +372 | line 172 (AC-C1 cell); lines 178-182 (new code block) |
| F-03 | 1227 | 622 | +605 | line 62 (WC-4 exemption); lines 87, 89, 90, 91 (3.1 rows); line 125 (validate-tests, 3.2); line 159 (P1 commands cell) |
| F-04 | 279 | 105 | +174 | line 85 (cleanup-audit row, one shared edit; its contract sentence is the F-03 part and is not split out) |
| total | 2563 | 1184 | +1379 | matches 59142 - 57763 |

## Dispositions

| Finding | Disposition | Where (revised spec) | Reason |
|---|---|---|---|
| F-01 | Applied | line 188 (7.2 step 3); line 200 (AC-0.4) | Step 3 required the WC-4 contract path, but the spec says that contract arrives in P1 (line 200 before the edit; `review/round1.md:24-27`). P0 now checks the command's existing report file. Existing files cited: troubleshoot `REPORT.md` (`inventory/commands-b.md:242`); workflow `.dev/tasks/to-do/<id>/return-contract.yaml` (`inventory/commands-b.md:272`); adversarial, where the filename is not fixed and real runs differ (`inventory/commands-a.md:35`, `inventory/commands-a.md:60`). Steps 3 and 4 both use that existing file in P0. |
| F-02 | Applied | line 172 (AC-C1 cell now points to the block); lines 178-182 (the command as a fenced block) | Checked in the sandbox with `printf` samples (no file written): the `\|` form in `grep -E` printed nothing and exited 1, while `|` matched all three samples and exited 0. The command moved out of the table because `|` splits table cells. Line 178 requires the three samples to match before first use. The fixture itself is a P0 deliverable in `tests/skills/test_worker_contract.py`, as the spec already states (line 158, unchanged). |
| F-03 | Applied | line 62 (`load` exempt from WC-4, citing `inventory/commands-b.md:65`); lines 87 (init-lite), 89 (release-split), 90 (tdd), 91 (troubleshoot), 86 (index-repo), 85 (cleanup-audit) gain a contract; line 125 (validate-tests, P3); line 159 (P1 commands cell lists the four commands that had no row) | WC-4 requires a contract on every outcome (line 62). These rows had none: init-lite writes no contract (`inventory/commands-a.md:55`); troubleshoot writes one only with `--caller task-unified` (`inventory/commands-b.md:242`); workflow writes one, but not for pre-creation STOPs (`inventory/commands-b.md:272`); release-split writes `release-split-report.md` with no contract (`inventory/commands-b.md:37`). The tdd, index-repo, cleanup-audit and validate-tests rows are the same case. `load` is exempt because it writes no file and is used as a brief step (`inventory/commands-b.md:65`, matching the spec's Decisions table row "`/sc:load` handling"). The review said the P1 command list named 13 commands; the cell now adds the four that had no row. Whether the P1 scope sentence and AC-1.1 agree is F-14, which was not edited. |
| F-04 | Applied | line 85 (cleanup-audit row) | The fixed output paths are `.claude-audit/pass<N>-summary.md` and `progress.json` (`inventory/commands-a.md:42`), so two workers in one worktree would share `progress.json` and lose the resume checkpoint. WC-11 (line 69) requires a timestamp or a coordinator slug. The row now applies that rule under `--unattended` and cites WC-11 for it, instead of the non-existent "one audit at a time" rule. UNVERIFIED: whether cleanup-audit accepts a per-run path today. The inventory names no flag for a per-run path (`inventory/commands-a.md:42`), so the row says only that the output path "carries a per-run slug the coordinator passes". |

## Scope check
- Added text cites its finding id (F-01 to F-04) as the brief requires.
- No rule, mechanism or section was added beyond what a listed finding calls for. The `load` exemption and the new contract rows follow from F-03's recommendation.
- The spec's WC rules, decisions D1-D5, phase order and section 1 are unchanged.
