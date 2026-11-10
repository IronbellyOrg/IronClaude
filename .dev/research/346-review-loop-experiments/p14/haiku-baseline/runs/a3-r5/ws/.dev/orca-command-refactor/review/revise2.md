# Revise 2: Orca worker-contract spec

- Prompt: REVISE prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:49-51` (sandbox copy at `home/.claude/rules/prompts/document_review_loop_prompts.md:49-51`).
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, edited in place.
- Input review: `.dev/orca-command-refactor/review/round2.md` (`review: 2 of 3`, verdict FAIL; its Reviser brief is at `round2.md:188-190`).
- Candidate before: 291 lines, 59142 bytes, sha256 `013a84aaca6a86058868c7f7b79fe52a951e5bbb08547665cff18e7d59d845ed` (matches `round2.md:5`).
- Candidate after: 291 lines, 59413 bytes, sha256 `5dc5c21ad2cf82fb9524020aa4cd5b0bc6a285be451e62fe6377194b27c70222`.
- Net change: +271 bytes. Line numbers did not move; the edited lines are `spec:85`, `spec:189` and `spec:200`.

## IDS used

Blocking ids are F-01 and F-03. The round 2 Reviser brief names exactly these two (`round2.md:190`), and the REVISE prompt defines IDS as the ids in that brief, and only those (`document_review_loop_prompts.md:21`).

The coordinator brief also listed F-02 and F-04. Both are resolved in round 2 (`round2.md:88` for F-02, `round2.md:90` for F-04), and `round2.md:190` says they are not part of the brief. Naming them would widen the revision, so they were not edited. Their rows below record that.

No Medium or minor finding was edited (N-1, N-2, N-3, N-5, F-05 to F-20, and the step 3 sentence note; `round2.md:124-186`).

## Byte accounting

| Finding | Spec location after edit | Bytes deleted | Bytes added | Net |
|---|---|---|---|---|
| F-01 | `spec:189` (7.2 step 4) | 27 | 102 | +75 |
| F-01 | `spec:200` (AC-0.4) | 269 | 393 | +124 |
| F-03 | `spec:85` (cleanup-audit row) | 108 | 180 | +72 |
| **Total** | | **404** | **675** | **+271** |

Check: 59142 + 271 = 59413 bytes.

## Per-finding rows

| Id | Status | Where | Reason |
|---|---|---|---|
| F-01 (blocking) | applied | `spec:189` and `spec:200` | `round2.md:94-98`: AC-0.4 applied the YAML assertion of step 4 to `REPORT.md` for `/sc:troubleshoot`. `REPORT.md` is markdown (`spec:91`), so the check fails on a correct run. Step 4 is now limited to YAML contracts (`spec:189`). AC-0.4 gives troubleshoot its own check, that `REPORT.md` exists and is non-empty (`spec:200`). Workflow and adversarial keep the YAML check (`spec:200`). Step 3 (`spec:188`) and its status-source note (`round2.md:148-152`, Medium follow-up) are not edited. |
| F-02 (resolved) | not revised | none | Not in the Reviser brief (`round2.md:190`). Resolved in round 2 (`round2.md:88`; the AC-C1 block is at `spec:178-183`, unchanged here). |
| F-03 (blocking) | applied | `spec:85` | `round2.md:104-111`: a `--pass <N>` run wrote no `return-contract.yaml`. `spec:85` now says a single-pass run writes the contract beside `pass<N>-summary.md`, and `--pass all` writes it beside the final report. This is the fix `round2.md:112` recommends. Other rows that carry F-03 (`spec:86-91`, `spec:125`, `spec:159`) are not edited. |
| F-04 (resolved) | not revised | none | Not in the Reviser brief (`round2.md:190`). Resolved in round 2 (`round2.md:90`, `round2.md:116-120`). The per-run slug text at `spec:85` is unchanged. The missing slug flag is N-5 (Medium), which is not in this brief. |

## Notes

- The spec now has a troubleshoot P0 check that does not depend on YAML. A reader of AC-0.4 can tell which check applies to which command.
- Open follow-ups, not edited under this brief: N-1 (`spec:62` directory versus file-valued `--output`), N-2 (`spec:62` section citation for `load`), N-3 (`spec:91` troubleshoot contract path), N-5 (`spec:85` slug flag), and the step 3 status-source note (`spec:188`).
- Citations in this file are to `spec` lines inside `.dev/orca-command-refactor/` and to `round2.md` lines. All were read in this run. Nothing cited here lies outside the workspace, so no citation is UNVERIFIED.
- No PASS verdict is given. The revision is returned for the next re-review.
