# Revise 2 of the orca-worker-contract spec

Input report: `.dev/orca-command-refactor/review/round2.md` (review: 2 of 3, verdict FAIL).
Verifier reply: `.dev/orca-command-refactor/review/verify-2.md:16` (`confirmed: M16, N1`).
Revised file: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (edited in place).
Pre-revision copy used for the byte accounting: `.dev/orca-command-refactor/specs/history/spec-v2.md` (sha256 54648b506bfdcd80743a1d2154ba8247546181fddf2026636e6e105d2c2bbbc5, identical to the candidate that round2 reviewed).

Scope: only the two confirmed blocking ids (M16, N1) were repaired. No Medium or minor finding was touched. The spec-panel was not run.

## Byte accounting

| Item | Bytes |
|---|---|
| Spec before (spec-v2.md) | 60613 |
| Spec after | 61127 |
| Net change | +514 |

| Finding id | Lines changed (after edit) | Bytes deleted | Bytes added | Net |
|---|---|---|---|---|
| N1 | :92 (workflow row), :198 (AC-1.4) | 713 | 933 | +220 |
| M16 | :209 (AC-4.2 pass condition) | 390 | 684 | +294 |
| Total | 3 lines | 1103 | 1617 | +514 |

Check: 1617 - 1103 = 514, which equals the net change above. No other line of the spec differs from spec-v2.md (`diff` shows exactly three changed lines).

## Findings

| id | Status | Where applied | Notes |
|---|---|---|---|
| M16 | applied | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:209` (AC-4.2) | The `ps -ef` before/after process snapshot was replaced by a before/after listing of the install targets the install step uses (throwaway venv, `pipx` home, container and VM lists). The `ps` snapshot could not see an installer that starts and exits between the two snapshots, so it was removed. The pass condition now states that it covers only those locations, and that the contract's `skipped` entries are the primary evidence. Source for the install steps: `.dev/orca-command-refactor/inventory/commands-b.md:84` (quoting `sk/sc-post-release-protocol/SKILL.md:129-131,187`); the skill file is not in this sandbox, so those skill citations are UNVERIFIED here. |
| N1 | applied | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:92` (workflow row) and `:198` (AC-1.4) | The two texts named different files for a successful workflow run. The row now makes `<output-dir>/return-contract.yaml` the worker's contract on every outcome, pre-creation and post-creation, as WC-4 requires (`:62`). After creation it lists the package contract `.dev/tasks/to-do/<id>/return-contract.yaml` under `artifacts`. This keeps WC-5 (`:63`) reading one file. The package path is still the P0 existing report (AC-0.4, `:194`), because P0 passes no `--output-dir`. AC-1.4 (`:198`) was changed to check the new wording, so the P1 test would not pass on the old text. The package-path citation is `.dev/orca-command-refactor/inventory/commands-b.md:272`. |
| M1 | not revised (verifier rejected) | none | Verifier rejected M1 because AC-0.4 at `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:194` states the P0 override for step 3 itself (verify-2.md:10). Carried as noted, unactioned. |
| M9 | not revised (verifier rejected) | none | Verifier rejected M9: the quoted phrase is not in the candidate, and the step 4 failure does not follow because `:194` defers step 4 to P1 (verify-2.md:11). Carried as noted, unactioned. |
| N2 | not revised (verifier rejected) | none | Verifier rejected N2 because AC-1.1 (`:195`) is scoped by "section 3 phase", and section 3.1 (`:78-84`) assigns no phase to brainstorm or init-lite (verify-2.md:14). The contradiction with the P1 row (`:159`) is real but was not repaired, because it is not a confirmed blocking finding. Carried as noted, unactioned. |

## Medium and minor findings left alone

F1 and F2 (round2.md follow-up candidates) were not touched.

## Checks run

- Each edit applied with an exact-match replacement. Changed lines confirmed with `diff` against `history/spec-v2.md`: three lines (`:92`, `:198`, `:209`).
- Spec size and hash after revision: 61127 bytes, sha256 24e411dcd5b98e3947b103fd3ff76a76e2a8ddec93e2c6e4f42c03d1f20513c9.
- No inventory file was edited. No spec-panel was run.
