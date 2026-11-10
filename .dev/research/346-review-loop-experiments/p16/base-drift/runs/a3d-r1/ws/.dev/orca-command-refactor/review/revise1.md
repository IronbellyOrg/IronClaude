# Revise 1: orca-worker-contract-spec.md

Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, edited in place. Blocking ids from `.dev/orca-command-refactor/review/round1.md:146-153` (Reviser brief): B-1, B-2. Medium and minor findings left alone. No PASS is claimed.

## Byte accounting (file size, `wc -c`)

| | Bytes |
|---|---|
| Before | 57763 |
| After | 58693 |
| Net | +930 |

Per finding id, counted as the bytes of the replaced text (deleted) and of its replacement (added), summed over the replacements; each replacement is a whole-phrase swap, so the gross figures include unchanged words inside the phrase.

| Id | Deleted | Added | Net |
|---|---|---|---|
| B-1 | 842 | 1396 | +554 |
| B-2 | 372 | 748 | +376 |

Net total 930 equals the file difference.

## Findings

| Id | Disposition | Where applied (line numbers in the revised spec) |
|---|---|---|
| B-1 | Applied | WC-4 (`spec` row WC-4): contract path is `<dir>/return-contract.yaml` for a directory value and `<file>.return-contract.yaml` beside the file for a file-valued `--output` (also keeps two workers from sharing one file, WC-11, as `round1.md:67` required). Adversarial named as a WC-4 exception (`<output>/adversarial/return-contract.yaml`, matching the observed runs, `inventory/commands-a.md:35`; `inventory/commands-b.md` adversarial location bullet). Workflow named as an exception: `<id>` is created by the command (`inventory/commands-b.md:272`, row at `:52`), so the path is found after creation, and a pre-creation stop writes no contract, which WC-5 already maps to `--outcome failed`. That deletes the P1 "pre-creation STOP" fix instead of inventing an id-less path. Consequent edits: WC-4 "every outcome" sentence, section 3 intro "Contract" definition, section 2.3 wording, section 3.1 adversarial and workflow rows, the P1 command list (workflow removed from the fixes), AC-1.4, and SA-4 (workflow contract gap removed from the defect-fix list). |
| B-2 | Applied | Section 3 intro: each changed command gains the `## Unattended mode` section in its own phase, `load` and `pr-submit` excepted (`load`: `inventory/commands-b.md:57-65`, writes no file; pr-submit only if D3 (b), `spec` D3 and section 4); the coordinator does not pass `--unattended` until the command's phase passes. This is a brief-side rule, not a new command mechanism, so no refusal logic is added to unchanged commands. Section 3.1 intro: contract arrives in the command's own phase; `brainstorm` and `init-lite` have no change and no section. P1 row: flag limited to the commands listed in that row, `load` excluded. P4 row: pr-submit "only if D3 (b)". AC-1.1: test covers the P1 commands, not `load`, and still requires no section-4 command to have one. |

## Residual notes (not edited, outside the named ids)

- AC-1.2 still says "each P1 command" and so includes `load`, which has no contract; AC-1.2 and AC-1.3 were not in the Reviser brief's text, left for the reviewer.
- AC-0.4 says "the contract arrives in P1"; for P2-phase ready commands (for example troubleshoot) it now arrives in P2. Left alone.
- Citations: all `inventory/` line numbers above were read in this sandbox; `spec:` line numbers cited from `round1.md` refer to the pre-revision file. Source-file citations (`sk/`, `cmd/`) inside the spec were not re-checked and stay as written (UNVERIFIED here: no source tree in the sandbox).
