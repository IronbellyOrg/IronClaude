review: 1 of 3 (revise pass; input report review/round1.md)

# Revise 1: orca-worker-contract-spec.md

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- candidate sha256 before: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` (57763 bytes, 285 lines; equal to `specs/history/spec-v1.md`)
- candidate sha256 after: `a6bb2fd31d271c13717322860b98be5dce7608e4f442926d61851162c5d899b7` (60391 bytes, 288 lines)
- brief ids: F-01, F-02, F-03, F-04, F-05, F-06, F-07 (from `review/round1.md`, Reviser brief, line 114)
- prompt: REVISE, from `~/.claude/rules/prompts/document_review_loop_prompts.md` (sandbox home copy)
- spec-panel: not run

## Byte accounting

Totals: 57763 bytes before, 60391 bytes after, net +2628 bytes.

Method: a changed table row or paragraph is counted as one deleted line and one added line. Where one line cites several ids, the added bytes are split by the exact inserted phrase, and the split sums to the line delta. Moved rows (section 3.1 to 3.2) count as deleted under the old row and added under the new one. Byte counts come from `diff` of the spec against `specs/history/spec-v1.md`.

| Finding | Added B | Deleted B | Net B | Where (spec lines, after) |
|---|---:|---:|---:|---|
| F-01 | 90 | 0 | +90 | 61 (WC-3) |
| F-02 | 305 | 0 | +305 | 159 (P1 phrase, 119 B), 200 (AC-1.6, 186 B) |
| F-03 | 478 | 473 | +5 | 147 (SA-2, whole line) |
| F-04 | 2537 | 2140 | +397 | 83 (adversarial), 115 (research), 125 (workflow, 3.2), section 3.1 table (workflow row removed, 308 B), 158 (P0 smoke runs, whole line), 194 (AC-0.4), 159 (P1 phrase, 16 B), 76 and 271 (shared, see below) |
| F-05 | 743 | 0 | +743 | 62 (WC-4 phrase, 62 B), 73 (section 2.3, 378 B), 199 (AC-1.5, 303 B) |
| F-06 | 1135 | 478 | +657 | 73 (section 2.3, 159 B), 107 (cleanup-audit row, 3.2), 110 (index-repo row, 3.2), 159 (P1 slug phrase, 29 B), 201 (AC-1.7), and removal of the cleanup-audit and index-repo rows from 3.1 (314 B and 164 B) |
| F-07 | 828 | 651 | +177 | 88 (tdd, 428 B added / 337 B deleted), 89 (troubleshoot, 400 B added / 314 B deleted) |
| Shared F-04/F-06 | 1014 | 760 | +254 | 76 (section 3 intro, 521 B / 432 B), 271 (Decisions row, 493 B / 327 B), 3.1 and 3.2 headings (24 B / 25 B and 28 B / 28 B) |
| **Total** | **7182** | **4554** | **+2628** | |

Check: 7182 added minus 4554 deleted equals +2628, the file's net change.

## Findings

| Id | Disposition | Where applied | Reason and check |
|---|---|---|---|
| F-01 | Applied: WC-3 exempts the implement Ruling gate from the coordinator relay, unless the user picks D2(b). | line 61 | Matches D2 (section 9, lines 235-238) and `INV-A:66` (quotes `qa.md:238`: "another agent's message ... not acceptance"). INV-A:66 checked in the workspace. |
| F-02 | Applied: P1 says `--unattended` on a command whose gate is still open writes `status: blocked` at that gate and takes no default there. AC-1.6 added to test it. | line 159 (P1), line 200 (AC-1.6) | Gated commands cited: `INV-A:38` (auggie-review posts to GitHub by default), `INV-B:204` (task commit and push). Both verified in the workspace. |
| F-03 | Applied: SA-2 no longer allows an Orca mention in the contract file. No command, skill, agent or core file (the contract file included) runs or names an orca command. The contract refers to the `ask` command only. | line 147 | Makes SA-2 consistent with AC-C1 (line 172, unchanged). |
| F-04 | Applied: adversarial row writes the WC-4 path `<output-dir>/return-contract.yaml`. Workflow moves to needs-change (P1) with `--output`. Research adds `--output` (P2). P0 smoke run replaces workflow with brainstorm, which already writes `<output>/return-contract.yaml` (`INV-A:39`). AC-0.4 updated to match. | lines 83, 115, 125, 158, 194; 3.1 row removed | `INV-B:52` (workflow contract is `.dev/tasks/to-do/<id>/return-contract.yaml`), `INV-B:267-275` (`<id>` is created at run time), `INV-B:132` (research name is generated at run time, so the worker reports the path it wrote), `INV-A:60` (adversarial skill names no file), `INV-A:39` (brainstorm contract path). All checked in the workspace. |
| F-05 | Applied: section 2.3 says each retry gets a new `--output`; a command with no resume flag refuses a non-empty `--output` directory and writes nothing there. WC-4 gets the matching exception. AC-1.5 added. | lines 62, 73, 199 | Retry mechanism: `CAPS:116` (`worker-start --retry-of`), checked in the workspace. The refusal behaviour is a new P1 requirement; AC-1.5 tests it. |
| F-06 | Applied: index-repo and cleanup-audit move to needs-change (P1), with a `--slug` flag. Section 2.3 adds the one-worker-per-worktree rule until the slug exists. AC-1.7 added. | lines 73, 107, 110, 159, 201; 3.1 rows removed | `INV-A:53` (index-repo writes `PROJECT_INDEX.md`), `INV-A:42` (cleanup-audit writes to `.claude-audit/`, checked in the workspace). The F-06 claim that two workers overwrite each other is the reviewer's, kept as is. |
| F-07 | Applied, without moving the rows out of ready: the troubleshoot brief excludes `--depth deep`, and the tdd brief names one task file. | lines 88, 89 | `INV-B:219` (nested `/task` asks when several task files match), `INV-B:239` (`--depth deep` short-input STOP). Both checked in the workspace. |

## Notes

- Ready count is now 7 (was 10), needs-change 30 (was 27), coordinator-only 6 (unchanged). Section 3 intro (line 76), the 3.1 and 3.2 headings (lines 78, 91) and the Decisions row (line 271) are updated. Total 43.
- Citations in the new text that point into `cmd/`, `sk/`, `src/`, `.dev/codegraph-migration/` or Orca application files remain UNVERIFIED here, as stated in spec section 2.2 and `review/round1.md` N-01. The `INV-*` and `CAPS:*` lines added in this revision were checked against the workspace inventories.
- Medium and minor findings (M-01 to M-08, N-02, N-03) were not revised, as the brief requires.
