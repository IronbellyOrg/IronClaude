# Revise 1: orca-worker-contract-spec.md

Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. Blocking ids: F-1 (`review/round1.md:140-145`). Not run: spec-panel, PASS award. Medium and minor findings (M-1..M-11, notes) left alone.

## Byte accounting
- Before: 57763 bytes. After: 58186 bytes. Net added: 423 bytes; deleted: 0 net bytes (a few words were replaced inside the rows listed below; counted as additions).
- F-1 only; all additions cite F-1.

| Edit | Spec line | Bytes added | Deleted |
|---|---|---|---|
| WC-4 sibling-file rule | 62 | 203 | 0 |
| research row: `--output <file>`, contract beside it | 116 | 64 | 0 |
| spec-panel row: `--output <file>`, contract beside it | 120 | 29 | 0 |
| section 2.3 brief carries the file path for file-valued `--output` | 73 | 52 | 0 |
| AC-2.2/7.2 step 4: contract is the sibling path | 183 | 75 | 0 |

(Per-edit figures sum to 423, matching the total measured with `wc -c`.)

## Findings
| Id | Disposition |
|---|---|
| F-1 | Applied. Rule chosen: when `--output` names a file, the contract is `<file-stem>.return-contract.yaml` in that file's directory (WC-4, line 62). It is one sentence, adds no flag, and gives each worker a distinct path (the stem is unique per deliverable), so it does not recreate the shared-directory collision WC-11 forbids (`round1.md:44`). Rows 87 (init-lite), 90 (tdd) and 200 (AC-2.2) already pass `--output <file>` and are now defined by WC-4, so they are unchanged. Rows 116 (research, no `--output` today: `inventory/commands-b.md:132`) and 120 (spec-panel, no `--output` today: `inventory/commands-b.md:182`) now say to add `--output <file>`; this is within the existing needs-change at `inventory/commands-b.md:135,185`. Section 2.3 (line 73) and the step 4 check (line 183) name the file path. `INV-A:55` confirms init-lite's `--output` is a file. |

Note: the directory-versus-file test is "what the `--output` value names"; how a command tells them apart for an `--output` that does not yet exist is not stated and is left to follow-up (relates to M-2/M-3, not touched).
