# Revise 2: orca-worker-contract-spec.md

- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (edited in place)
- Input report: `.dev/orca-command-refactor/review/round2.md` (`review: 2 of 3`, `verdict: FAIL`), Reviser brief at `review/round2.md:144-150`
- Blocking ids revised: R-2, N-1, N-2. Medium and minor ids (N-3 to N-6, R-6 to R-9, A-1 to A-9) were not edited.
- Prompt: REVISE prompt in `~/.claude/rules/prompts/document_review_loop_prompts.md` (sandbox home copy, read in full).

## Byte accounting

| State | Lines | Bytes | SHA-256 |
|---|---|---|---|
| Before (review-2 candidate) | 285 | 59446 | `0d68261e01a3ed1635c14612d194b7036278add2ee00b1558b4001bfcd42d22b` |
| After (revise-2 candidate) | 285 | 60136 | `2fadf1465791032cab449691f98fc1d6c0b5bd279da252336d54f84f58e6198f` |

Net change: +690 bytes (1406 added, 716 deleted). Line count unchanged, so the line numbers cited in round2.md still point at the same lines.

Per finding id (bytes measured per replaced string, old and new):

| Id | Edit (spec line) | Added | Deleted | Net |
|---|---|---|---|---|
| N-1 | WC-3 answer rule (`:61`) | 256 | 161 | +95 |
| N-2 | init-lite row, last cell (`:87`) | 181 | 123 | +58 |
| N-2 | P1 row, init-lite clause (`:159`) | 90 | 49 | +41 |
| N-2 | AC-1.2 command clause (`:196`) | 122 | 70 | +52 |
| R-2 | Step 3 pass clause (`:182`) | 121 | 79 | +42 |
| R-2 | Step 4 P0 clause (`:183`) | 184 | 78 | +106 |
| R-2 | AC-0.4 P0 outcome rule (`:194`) | 452 | 156 | +296 |
| **Total** | | **1406** | **716** | **+690** |

Check: 59446 + 690 = 60136.

## Findings

| Id | Disposition | Where applied | Basis |
|---|---|---|---|
| R-2 | Applied | `:182` step 3 now names the outcome rule for P0 and points to AC-0.4. `:183` step 4 says that in P0 the only check is `test -s <existing report file>`. `:194` AC-0.4 defines the P0 outcome rule: `succeeded` when the §3.1 report file exists and is non-empty, `failed` when it does not. | round2.md:78-85. WC-5 (`:63`) already sends `failed` for "no report", so the P0 rule is the WC-5 rule with the report file standing in for the contract. A P0 troubleshoot run has no contract (`inventory/commands-b.md:242`), so step 3 now has a value that can pass. WC-4 (`:62`) and WC-5 (`:63`) are unchanged, so P1+ behaviour is unchanged. |
| N-1 | Applied | `:61` WC-3 now says an answer supplies a flag value only when it quotes the user's own words for that value, the coordinator then writes that flag into the brief, a coordinator's own "yes" supplies no flag, and an answer never supplies an implement Ruling (D2(a)). | round2.md:87-94. WC-3 and D4(a) (`:245`) now state the same rule for a quoted answer. D4(a) (`:245`) was not edited because its text already matches the new WC-3. The "written into the brief" clause keeps WC-9 (`:67`, "the command's own explicit flag written in the brief") true. D2 (`:235`) and the Ruling clause are untouched; N-5 (`:61`, D2 conditional) is not in this brief and is left for a later round. |
| N-2 | Applied | `:87` init-lite row now adds `--output-dir <dir>` for the WC-4 contract, so the row matches WC-4 (`:62`) and init-lite writes `<output-dir>/return-contract.yaml` in unattended mode. `:159` P1 row names the init-lite output flag. `:196` AC-1.2 names `--output-dir` for init-lite. | round2.md:96-102. Current behaviour is `inventory/commands-a.md:55` (init-lite writes no contract; its report is `.dev/superclaude/context-audit.md`). `--output-dir` is the flag WC-4 (`:62`) already names as a possible `<output-dir>`, so no new WC-4 wording was needed. The existing `--output <file>` stays as the report flag. N-3 (`--output <file>` for tdd and init-lite, Medium) is not in this brief and is not resolved here. |

## Checks run on the edited spec

- `wc -c` and `wc -l` above; the hash changed from the review-2 candidate.
- Each `>`-side text from the revision was grepped in the spec before the report was written (the same self-check the RE-REVIEW prompt uses), so the edits are present as written.
- Cross-references checked against the inventory files under `.dev/orca-command-refactor/inventory/`:
  - `inventory/commands-a.md:55` (init-lite: no contract today).
  - `inventory/commands-b.md:242` (troubleshoot: contract only with `--caller task-unified`).
  - `inventory/commands-b.md:52` and `:272` (workflow contract at `.dev/tasks/to-do/<id>/return-contract.yaml`, fields `status`, `plan_path`, `reflect_report_path`; no `command` key listed).

## UNVERIFIED in this revision

- Whether the workflow return contract has a `command` key (AC-0.4 step 4, `:183`, asks for it in P1). The source `sk/sc-workflow-protocol/refs/return-contract.md` is outside this sandbox, so the claim stays as round2.md:82 recorded it: UNVERIFIED.
- Whether `adversarial`'s P0 run writes its return contract to a path the P0 rule (`:194`) can read; the path is not fixed until P1 (`inventory/commands-a.md:35`). The P0 rule says "the command's existing report file" and does not name adversarial's path. UNVERIFIED.
- Whether Orca reads the file named by `--report-path` (`CAPS:178`, spec UNVERIFIED item 3). Unchanged by this revision.

## Not changed

- No edit to WC-4, WC-5, WC-9, D2, D4(a) or the phase table beyond the P1 row clause at `:159`.
- No edit to any Medium or minor finding: N-3, N-4, N-5, N-6, R-6 to R-9, A-1 to A-9.
- No review was run, and no PASS is claimed.
