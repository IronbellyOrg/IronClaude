# Revise 2: blocking findings F-03 and R2-01

Prompt: REVISE prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md` (sandbox home copy, "REVISE prompt" section).
Input report: `.dev/orca-command-refactor/review/round2.md` (`review/round2.md:73-79`, Reviser brief: "Blocking finding ids: F-03, R2-01").
Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`.

## Byte accounting

| | Bytes | sha256 |
|---|---|---|
| Before (round 2 candidate) | 59746 | `e1f78b891d8bb255eebfc49ad5aa8456501e35c3ff87d61c58e99699e8350b62` (matches `review/round2.md:7`) |
| After (this revision) | 59962 | `2a0ba05dc4158ae8fc6c4b9c265ce2ded840533c29031835d61d7c548122ac84` |
| Net | +216 | |

| Finding id | Bytes added | Bytes deleted |
|---|---|---|
| F-03 | 63 | 0 |
| R2-01 | 98 + 55 = 153 | 0 |
| Total | 216 | 0 |

Check: 59746 + 216 - 0 = 59962. Measured after the edits with `wc -c`. Line count is unchanged at 285 lines, so `diff -w` line numbers in the round 2 report still map.

## Rows

| Id | Disposition | Where (spec path:line, after edit) | Reason |
|---|---|---|---|
| F-03 | Applied | `specs/orca-worker-contract-spec.md:146` (SA-1). Added ", except the two standalone file changes that SA-3 names (F-03)". | SA-1 now names the same two exceptions as SA-3 (`:148`). The adversarial row (`:83`) and SA-3 (`:148`) are unchanged, so SA-1, SA-3 and `:83` now list the same set. The reviewer's first option (name the exception in SA-1) was used, not the second (gate the name behind `--unattended`), because the adversarial contract path is already a P1 change in the §3.1 table and the reviewer's recommendation allowed either. |
| R2-01 | Applied | `specs/orca-worker-contract-spec.md:182` (§7.2 step 3). Added "(R2-01: waived for troubleshoot in P0, because its `REPORT.md` has no `status` field, `INV-B:49`)" after the WC-5 clause. | The reviewer's second option (waive the outcome clause for troubleshoot in P0 by name). `inventory/commands-b.md:49` lists `report_path` REPORT.md with no contract. The round 2 review also cites `REPORT.md` as Markdown (`:194`). The outcome clause is kept for workflow (`inventory/commands-b.md:52`, `return-contract.yaml`) and adversarial (`inventory/commands-a.md:35`). |
| R2-01 (cross-ref) | Applied | `specs/orca-worker-contract-spec.md:194` (AC-0.4). Added "and the step 3 outcome waiver for troubleshoot (R2-01)" to the list of P0 substitutes. | Keeps AC-0.4 consistent with the waiver at `:182`, so a P0 checker does not treat the waived clause as a failing step. |

## Not touched

Per the brief, Medium and minor findings were not edited: R2-02, R2-03, R2-04, R2-05 (Medium) and m-04 (minor). Round 1 follow-ups F-07 to F-15 and m-01 to m-03 were not re-graded and were not edited.

## Notes

- Checked: `inventory/commands-a.md:35` and `inventory/commands-b.md:49,52` exist and say what the rows above rely on. The reviewer's claim that real runs wrote `.../adversarial/adversarial/return-contract.yaml` (`review/round2.md:41`, citing `inventory/commands-a.md:35`) is not in the visible text of that line. UNVERIFIED here; the F-03 fix does not depend on it.
- Citations to `src/superclaude/core/HOW-WE-WORK.md:171,249,254` (SA-1) are outside this workspace. UNVERIFIED here; the edit to SA-1 cites SA-3 only, not those lines.
- No `.claude/` file, no `src/` file and no other spec file was changed. The only edited file is `specs/orca-worker-contract-spec.md`.
- Review verdict is not awarded. Per the REVISE prompt, a re-review (review 3 of 3) follows; this file does not state a PASS.
