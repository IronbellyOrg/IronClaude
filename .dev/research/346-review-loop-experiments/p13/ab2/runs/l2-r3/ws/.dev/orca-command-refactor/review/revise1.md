# Revise 1: orca-worker-contract-spec.md

Inputs: `review/round1.md` (Reviser brief lines 122-129: F-1, F-2), the spec, `inventory/commands-a.md`, `inventory/commands-b.md`. Candidate edited in place: `specs/orca-worker-contract-spec.md`. I did not run the spec-panel and award no PASS.

## Byte accounting
- Before: 57763 bytes (sha256 d3cdbe57...5200d, equals the hash in round1.md line 5). After: 58423 bytes. Net +660.
- Deleted bytes: 0 substantive; the one rewritten table line (section 3 intro) replaced 14 words of its own text, net +40 counted below. Every other edit is a pure insertion.

| Finding | Bytes added | Bytes deleted |
|---|---|---|
| F-1 | 612 (WC-4 +243; section 3 intro +40; cleanup-audit +56; index-repo +66; init-lite +75; tdd +76; spec-panel +56) | 0 net (intro line reworded, counted in the +40) |
| F-2 | 48 (AC-1.1 +24; P1 scope +24) | 0 |

## Findings
| ID | Disposition | Where |
|---|---|---|
| F-1 | Applied. One sentence in WC-4 (spec line 62): where `--output` is a file, the contract is `<file stem>.return-contract.yaml` in that file's directory; where the location is fixed, it is in that fixed directory, as named in the section 3 row. The section 3 intro definition of "Contract" (line 76) no longer states `<output-dir>/return-contract.yaml` unconditionally, which contradicted the rows. Row cells added for tdd (line 90), init-lite (line 87), spec-panel (line 120, `--output <file>`), cleanup-audit (line 85, `.claude-audit/return-contract.yaml`), index-repo (line 86, `PROJECT_INDEX.return-contract.yaml`). Each addition cites F-1. Result: `/sc:tdd "auth" --unattended --output docs/x/TDD_FOO.md` writes `docs/x/TDD_FOO.return-contract.yaml`, so the AC-2.2 blocked-path check (line 200) and `test -s <contract>` (line 183) have a creatable path. | Rule chosen follows the reviewer's allowed option "beside the named file under a stated filename" (round1.md:42); no new flag. |
| F-2 | Applied by narrowing, as recommended (round1.md:51). AC-1.1 (line 195) now says "except `/sc:load`"; P1 scope (line 159) says the `--unattended` flag is accepted by every command in 3.1-3.2 "except `/sc:load`". This keeps the decision at spec lines 112 and 265 (no report file for load). | Cites F-2 in both edits. |

## Notes
- index-repo's output location is itself UNVERIFIED (`inventory/commands-a.md:53`, "location (repo root) implied, UNVERIFIED"); the contract name is stated relative to `PROJECT_INDEX.md`, whatever its location.
- The row 3.2 spec-panel "add `--output`" now reads `--output <file>` because its deliverable is a review document (`inventory/commands-b.md:182`). tdd and init-lite file-valued `--output`: `inventory/commands-b.md:222`, `inventory/commands-a.md:55`.
- Medium and minor findings were left alone.
