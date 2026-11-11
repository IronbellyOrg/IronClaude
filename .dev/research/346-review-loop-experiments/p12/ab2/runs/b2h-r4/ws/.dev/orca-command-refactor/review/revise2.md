# Revise 2: repair of blocking finding N-1

- Candidate (edited in place): `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- Input report: `.dev/orca-command-refactor/review/round2.md` (review 2 of 3, verdict FAIL)
- Verification: `.dev/orca-command-refactor/review/verify-2.md:22` reads `confirmed: N-1`
- Blocking ids given to this revision (IDS): N-1
- Prompt: REVISE prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md` (sandbox home copy), "Revise brief"
- Note on ids: round1 also used `N-1` (round1 minor: `spec:215` cites `CAPS:12-13`, carried at `round2.md:132`). In this file, `N-1` means the round2 finding at `round2.md:96`. The round1 item is written `round1 N-1`.

## Byte accounting

| Measure | Before | After | Change |
|---|---|---|---|
| Spec file bytes | 58887 (sha256 `97f56a6e69838dc9f80dfae9d1e8e0aa95413656b2559e687870566b2996ca6a`) | 59060 (sha256 `87c84d9ca9169f943376688b64d421baec2513be9fe5034504496a4473d86140`) | +173 |
| Spec line count | 285 | 285 | 0 (both edits replace text within a line) |

Per finding id (exact byte count of each replaced string, measured with Python from the old and new strings):

| id | Edit | Bytes deleted | Bytes added | Net |
|---|---|---|---|---|
| N-1 | `spec:63` (WC-5) | 0 (the removed text is ", or when the contract is missing" and is re-added in the P1 clause; net shown) | 67 | +67 |
| N-1 | `spec:182` (7.2 step 3) | 0 (same convention; net shown) | 106 | +106 |
| all other ids | none | 0 | 0 | 0 |

Total net: +173 bytes, equal to the file size change. Gross deleted and added bytes are not reported separately: a character-level diff and a token-level diff give different gross figures for the same change, and only the net is exact.

Old and new text, for the record:

- `spec:63`, before: "`--outcome failed` when the report says `failed` or `blocked`, or when the contract is missing, zero bytes, truncated, unparseable, lacks `status`, or has a `status` outside the four values (B-5: the default is `failed`);"
- `spec:63`, after: "`--outcome failed` when the report says `failed` or `blocked`; in P0, when the named report is missing or zero bytes (N-1); from P1, when the contract is missing, zero bytes, truncated, unparseable, lacks `status`, or has a `status` outside the four values (B-5: the default is `failed`);"
- `spec:182`, before: "**Pass:** exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path."
- `spec:182`, after: "**Pass:** exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5 (from P1) or the named report under WC-5 (P0, N-1); its report path is the WC-4 contract path (from P1) or the command's named report file (P0, N-1)."

## Row per finding id

| id | Severity (round2) | Disposition | Where | Reason |
|---|---|---|---|---|
| N-1 | BLOCKING (`round2.md:96-106`) | **applied** | `spec:63` (WC-5), `spec:182` (7.2 step 3) | The finding says WC-5 keys the default on a contract that P0 does not write (`spec:79`, `spec:194`). `spec:63` now keys on the named report in P0 and on the contract from P1, as the finding's recommendation allows. Only the B-5 wording (missing, zero, truncated, unparseable, no `status`, value outside the four) is kept for the contract, from P1 (`spec:63`). The P0 rule is limited to "named report missing or zero bytes", not the contract checks, so a `REPORT.md` without YAML `status` is not sent `failed` by the new text. `spec:182` step 3 gets the same P0/P1 split, because the finding names it: without it AC-0.4 step 3 has no contract to compare with (`spec:194`). The `report_path` clause of the same step is split the same way, since in P0 the WC-4 contract path does not exist. |
| B-1 | prior blocking, resolved (`round2.md:88`) | no edit | `spec:79`, `spec:195`, `spec:159` | Resolved per `round2.md:88`; nothing to revise. |
| B-2 | prior, noted, not re-graded (`round2.md:92`; `round1.md:2`) | not actioned | `spec:194`, `spec:183` | Not in the IDS list. The verifier rejected it at VF1 and it is recorded as a note. The brief allows only IDS. |
| B-3 | prior blocking, resolved (`round2.md:89`) | no edit | `spec:62`, `spec:83`, `spec:87`, `spec:90`, `spec:92` | Resolved per `round2.md:89`. |
| B-4 | prior, noted, not re-graded (`round2.md:92`; `round1.md:2`) | not actioned | `spec:88`, `spec:122` | Not in the IDS list; rejected at VF1 and recorded as a note. |
| B-5 | prior blocking, resolved (`round2.md:90`) | no edit | `spec:63`, `spec:200` | Resolved per `round2.md:90`. The B-5 wording is kept in the P1 clause of `spec:63`. |
| N-2 (`round2.md:108-110`) | minor | not actioned | `spec:83` | Not a blocking id. The REVISE prompt says to leave minor and Medium findings alone. |
| N-3 (`round2.md:112-114`) | minor | not actioned | `spec:52`, `spec:76`, `spec:79` | Not a blocking id. Left alone per the REVISE prompt. |
| N-4 (`round2.md:116-120`) | Medium | not actioned | `spec:105`, `spec:114` | Not a blocking id. Medium findings are left alone per the REVISE prompt. Recorded for the next round. |
| N-5 (`round2.md:122-124`) | minor | not actioned | `spec:182` | Not a blocking id. The `spec:182` edit above adds the workflow contract path only where N-1 needed it, not the full workflow exception. The rest of N-5 stays open. |
| M-1 | Medium (carried) | not actioned | `spec:59` | Not a blocking id; Medium left alone. |
| M-2 | Medium (carried) | not actioned | `spec:63`, `spec:262`, `spec:263` | Not a blocking id. `spec:63` changed for N-1, but the partial-to-succeeded mapping (M-2) is unchanged and not in IDS. |
| M-3 | Medium (carried) | not actioned | `spec:62`, `spec:63` | Not a blocking id. |
| M-4 | Medium (carried) | not actioned | `spec:61` | Not a blocking id. |
| M-5 | Medium (carried) | not actioned | `spec:172` | Not a blocking id. |
| M-6 | Medium (carried) | not actioned | `spec:149` | Not a blocking id. |
| M-7 | Medium (carried) | not actioned | `spec:122` | Not a blocking id. |
| M-8 | Medium (carried) | not actioned | `spec:279` | Not a blocking id. |
| M-9 | Medium (carried) | not actioned | `spec:79`, `spec:194` | Not a blocking id. The N-1 edit touches the same text, but M-9 (P0 smoke runs do not test WC-2) is a separate gap and is unchanged. |
| M-10 | Medium (carried) | not actioned | `spec:68` | Not a blocking id. |
| M-11 | Medium (carried) | not actioned | `spec:195` | Not a blocking id. |
| M-12 | Medium (carried) | not actioned | `spec:70` | Not a blocking id. |
| M-13 | Medium (`round2.md:130`, `round2.md:147`) | not actioned | `spec:62` | Not a blocking id. The `--output`-absent case is still undefined; left for a later round. |
| M-14 | Medium (carried) | not actioned | `spec:85`, `spec:119` | Not a blocking id. |
| M-15 | Medium (carried) | not actioned | `spec:73`, `spec:158` | Not a blocking id. |
| round1 N-1 (`round2.md:132`) | minor | not actioned | `spec:215` | Not a blocking id. Cites `CAPS:12-13`; left alone. |
| round1 N-2 (`round2.md:132`) | minor | not actioned | `spec:80` | Not a blocking id. |
| round1 N-3 (`round2.md:132`) | minor | not actioned | `spec:23` | Not a blocking id. |

## Self-check after the edit

- `grep -nF` finds the new `spec:63` text ("in P0, when the named report is missing") and the new `spec:182` text ("the named report under WC-5 (P0, N-1)") once each, at those lines.
- Line count is 285 before and after, so no other line moved.
- Only `spec:63` and `spec:182` were edited. Both are on the N-1 path. No rule, mechanism or section was added beyond what N-1 calls for.
- The P0 rule does not reuse the P1 contract checks. For a `REPORT.md` the P0 rule reads only "missing or zero bytes", so the open B-2 issue (`spec:194`) is not made worse.

## Not checked

- The sandbox holds no `CAPS:` or `INV-B:` citations beyond the inventory files, and no baseline or git history. The N-1 claim that `spec:79` and `spec:194` put the contract in P1 was checked by reading those lines in the candidate (`spec:79`, `spec:194`), not against the original Orca guides.
- Whether the step-3 `report_path` change in P0 matches what `/sc:troubleshoot` writes is UNVERIFIED: the command's report path is `REPORT.md` (`spec:91`), which the spec states but the sandbox cannot confirm.

## Result

The blocking finding N-1 is repaired. This revision does not award a PASS: the next re-review decides, with the verdict of the re-review. The brief's "Medium and minor findings" are unchanged in the candidate.
