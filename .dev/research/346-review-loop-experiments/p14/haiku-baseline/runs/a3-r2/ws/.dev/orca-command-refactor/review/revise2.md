# Revise 2: orca-worker-contract-spec.md (blocking ids: F-08)

- Prompt: REVISE prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md` (sandbox home copy; the file's REVISE section is at lines 49-51).
- Input report: `.dev/orca-command-refactor/review/round2.md` (`review: 2 of 3`, `verdict: FAIL`). Its Reviser brief (`review/round2.md:168-172`) lists blocking id F-08 only (`review/round2.md:170`).
- Candidate revised: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`.
- Spec-panel not run. No other file edited.

## Byte accounting

| Measure | Before | After | Net |
|---|---|---|---|
| sha256 | `a6bb2fd31d271c13717322860b98be5dce7608e4f442926d61851162c5d899b7` (matches `review/round2.md:6`) | `284cc6b74e9164675f12bdb0a33d7d0c5edf49544b271cb956ec89ae5853237e` | |
| bytes | 60391 | 60530 | +139 |
| lines | 288 | 288 | 0 |

Per finding id:

| Finding id | Bytes added | Bytes deleted | Net |
|---|---|---|---|
| F-08 | 176 (57 for the `In unattended mode, a command with no resume flag refuses` lead-in, 119 for the appended `Without ... (SA-1, F-08).` sentence) | 37 (`A command with no resume flag refuses`) | +139 |

Check: 60391 + 139 = 60530.

## Finding rows

| Id | Status | Where applied | Note |
|---|---|---|---|
| F-08 | applied | `specs/orca-worker-contract-spec.md:73` (section 2.3) | The refusal of a non-empty `--output` directory is now scoped to unattended mode. The F-05 protection is kept for worker runs. A standalone run without `--unattended` is stated to keep today's output behaviour, citing SA-1 (`specs/orca-worker-contract-spec.md:146`). |

Only line 73 changed. `diff -w` of the spec before and after shows no other changed line.

## Rows not in scope for this revision

The brief names only F-08. The following are left alone, as the REVISE prompt and the round2 Reviser brief require (`review/round2.md:172`):

- M-09 (Medium, refused retry passes the live check), `review/round2.md:115-119`: not revised.
- M-10 (Medium, routing-guide Orca text), `review/round2.md:121-127`: not revised.
- M-11 (Medium, AC-1.7 names no path), `review/round2.md:129-132`: not revised.
- F-01 to F-07: resolved per `review/round2.md:91-99`; not touched.

## Checks

- Round2's Reviser brief asks for the reviser to cite the finding id on each addition. The two added phrases in line 73 both cite F-08.
- The unchanged WC-4 text at `specs/orca-worker-contract-spec.md:62` already excepts "the non-empty-directory refusal in section 2.3 (F-05)". With the new scope, that exception still holds for unattended runs only, so WC-4 needs no edit.
- The Phase-0 and AC-1.5 text (`specs/orca-worker-contract-spec.md:199`) tests the refusal under `--unattended` by its own wording ("run twice ... with the same `<dir>` and no resume flag"). It inherits the unattended scope but names no flag. It is not edited here. Whether AC-1.5 should name `--unattended` explicitly is a Medium question, not part of F-08.
- UNVERIFIED: the behaviour of commands in the inventory as to what they do today with a non-empty `--output` directory. The round2 review states that the ready rows for brainstorm and adversarial do not refuse a second run today (`review/round2.md:111`); that is the review's own claim and was not re-checked against `inventory/` in this pass.

## Verdict

Not awarded. Under the REVISE prompt the reviser does not award a PASS (`document_review_loop_prompts.md`, REVISE brief). The next step is a re-review by the coordinator.
