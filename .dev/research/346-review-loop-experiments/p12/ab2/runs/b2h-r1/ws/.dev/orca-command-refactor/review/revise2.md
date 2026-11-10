# Revise 2: spec revision for blocking finding N2-01

- Prompt: REVISE prompt in `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full before this revision).
- Candidate edited in place: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`.
- Input (review 2 candidate): sha256 `00cb7b63ea6019f358ead17f8b721ad6058432fb1bebc97218c1af92404e5038`, 58776 bytes, 285 lines (matches `review/round2.md:7` and `review/verify-2.md:3`).
- Output: sha256 `2d14bcd06b4ba445afa8a700e4b20d34af0ab4a0f9ac87d402e2488534d77270`, 58906 bytes, 285 lines.
- IDS: N2-01 only (`review/verify-2.md:` last line `confirmed: N2-01`; `review/round2.md:2`). The Reviser brief at `review/round2.md:101-103` is narrowed to N2-01.
- Scope: two text edits, both on the lines N2-01 names: spec:182 (step 3 pass clause) and spec:194 (AC-0.4, P0 row). No line was added or removed, so every other line number is unchanged. No Medium or minor finding was touched (M2-01 to M2-04, N2-02 stay as they were).
- Verifier check: `verify-2.md` reads the inventory citation `commands-b.md:242` as absent from the workspace. The file is present in `inventory/` (323 lines), and line 242 reads "`report_path` (REPORT.md)", so that citation is verified here, not UNVERIFIED.
- No verdict is given in this file. The re-review decides PASS or FAIL.

## What changed

### N2-01: the P0 gate AC-0.4 cannot pass as written (spec:182, spec:194)

The defect: step 3's pass clause requires "its report path is the WC-4 contract path" (spec:182). WC-4 writes `<output-dir>/return-contract.yaml` only "In unattended mode" (spec:62). The P0 smoke runs are ready commands run "if the brief uses the stated flags" (spec:79), and the troubleshoot row lists only "no `--fix`" as its brief flag (spec:91). P0 also adds no command edits (spec:158). So in P0 no WC-4 contract exists, the `worker_done --report-path` is `REPORT.md` (spec:91; `inventory/commands-b.md:242`), and the clause fails. AC-0.4 (spec:194) overrides step 4 and the step 3 outcome source, but not this path clause.

Edit 1, spec:182 (step 3 pass clause). The path clause now names the contract path from P1 and the command's own report file in P0:
- before: `its report path is the WC-4 contract path.`
- after: `its report path is the WC-4 contract path from P1; in P0 it is the command's own report file (N2-01, see AC-0.4).`

Edit 2, spec:194 (AC-0.4 P0 row). The P0 report file that step 4 tests is the same file step 3 checks. The clause is inserted after `with no YAML parse,`:
- before: `step 4 is `test -s <report>` on the file the command already writes, with no YAML parse (for`
- after: `step 4 is `test -s <report>` on the file the command already writes, with no YAML parse, and that file is the P0 report path step 3 checks (N2-01) (for`

The change follows the recommendation in `review/round2.md:57` (state the P0 report path in spec:194, so the clause reads "the command's own report path" in P0 and "the WC-4 contract path" from P1). The P1 checks (spec:183 and the P1 rows) are not changed.

## Byte accounting

Bytes are counted on the replaced text: "deleted" is the old string's bytes, "added" the new string's bytes. Counts from `printf '%s' ... | wc -c`.

| Finding id | Edit | Bytes deleted | Bytes added | Net |
|---|---|---|---|---|
| N2-01 | spec:182 pass clause | 42 | 113 | +71 |
| N2-01 | spec:194 AC-0.4 P0 clause | 92 | 151 | +59 |
| Total | | 134 | 264 | +130 |

Check: 58776 (before) + 264 (added) - 134 (deleted) = 58906, and `wc -c` on the output file gives 58906. No bytes were changed outside these two edits. Line count stays 285.

## Rows, one per finding id

| Finding id | Result | Where applied (spec line, after edit) | Cited evidence |
|---|---|---|---|
| N2-01 | applied | spec:182 (step 3 pass clause) and spec:194 (AC-0.4 P0 row) | `review/verify-2.md` (confirmed; its `confirmed: N2-01` line); `spec:62` (WC-4 "In unattended mode"); `spec:79` and `spec:91` (P0 flags, REPORT.md); `spec:158` (P0 "no command edits"); `inventory/commands-b.md:242` (`report_path` REPORT.md, verified present) |
| F-02 | not actioned: resolved in review 1, not in IDS | none (spec:181 and spec:182 loop text from revise 1 unchanged, except the N2-01 clause above) | `review/round2.md:43` (resolved) |
| F-03 | not actioned: resolved in review 1, not in IDS | none (spec:194 P0 text from revise 1 unchanged, except the N2-01 clause above) | `review/round2.md:44` (resolved) |
| F-01 | not actioned: rejected by VERIFY, kept as a note | none | `review/round1.md:2`; `review/round2.md:39` |
| F-04 | not actioned: rejected by VERIFY, kept as a note | none | `review/round1.md:2`; `review/round2.md:39` |
| M2-01 | not actioned: Medium, not in IDS (escalation loop has no deadline) | none; spec:182 still says only `worker_done` ends the loop | `review/round2.md:62` |
| M2-02 | not actioned: Medium, not in IDS (answer delivery for pending `question`) | none | `review/round2.md:63` |
| M2-03 | not actioned: Medium, not in IDS (P0 outcome from an unmapped status line) | none; spec:194 still says "recorded as found" | `review/round2.md:64` |
| M2-04 | not actioned: Medium, not in IDS (adversarial report path not fixed) | none | `review/round2.md:65`; `spec:83` |
| N2-02 | not actioned: minor note, not in IDS (spec:183 general step 4 still reads as YAML) | none; spec:183 unchanged | `review/round2.md:69`; `spec:183` |

## Self-check

- Each string added by this revision was located in the output file with `grep -nF`: the spec:182 clause ("its report path is the WC-4 contract path from P1; in P0 it is the command's own report file (N2-01, see AC-0.4).") and the spec:194 clause ("and that file is the P0 report path step 3 checks (N2-01)"). Both were found once.
- Line count is 285 before and after, so no other cited spec line moved.
- The removed text was located in the input file before editing (the spec:182 clause at `review/round2.md:51-57` quotes it, and the spec:194 clause at `review/round2.md:31`). The byte counts above are from the strings removed.

## Not checked, marked UNVERIFIED

- Whether `check --wait` returns with no rows after a 240 s timeout (inherited from revise 1; `inventory/orca-capabilities.md:63` does not state it). UNVERIFIED, not relied on by this revision.
- The format of the troubleshoot report's first status line (AC-0.4, inherited). UNVERIFIED; not relied on by this revision.
- Repository files cited by the spec (outside the workspace) were not read. Nothing in this revision depends on them.
- The side observation in `review/verify-2.md` (spec:73 requires `--unattended` in every brief, which P0 cannot accept) is not in IDS and is left unchanged. It is a candidate for the next review, not a fix in this revision.
- No `--unattended` P0 run or any Orca command was run (no Orca and no repository in this sandbox).
