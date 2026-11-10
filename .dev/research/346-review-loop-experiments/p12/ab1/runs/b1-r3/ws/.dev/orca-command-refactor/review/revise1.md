# Revise 1 (candidate: specs/orca-worker-contract-spec.md; S:n = line n of the revised spec; IDS = M1, M2, M3, M5)

Evidence: review/round1.md (Reviser brief), verify-1.md, and inventory/commands-a.md, commands-b.md (`INV-B:52` generated package id, `INV-B:272` workflow contract path, `INV-B:39` via ref: not written for pre-creation STOPs). The real `command.md:460-461` cited in round1.md is outside the workspace: UNVERIFIED, not relied on.

## Byte accounting
- Before: 57763 bytes. After: 58733 bytes. Net +970.
- Added 2071, deleted 1101 (bytes of the replaced and replacing text).

| Finding id | Bytes deleted | Bytes added |
|---|---|---|
| M1 and M5 (one shared edit set) | 397 | 685 |
| M2 only | 70 | 122 |
| M2 and M3 (shared edits) | 347 | 843 |
| M3 only | 287 | 421 |
| Total | 1101 | 2071 |

Shared rows are counted once; the edits answer both ids and are not split.

## Findings
| id | Disposition | Where applied | Narrowing / reason |
|---|---|---|---|
| M1 | applied | S:154 (new sentence: a command accepts `--unattended` and the `## Unattended mode` section only in the phase its row names, together with its gate resolution); S:159 P1 scope ("a no-op where a command has no gate" and "every command in 3.1 and 3.2" replaced by "the commands listed in this row only"); S:195 AC-1.1 | Narrowed, not added: auggie-review and cleanup (rows P2, S:100, S:103) no longer gain the flag in P1. |
| M2 | applied | S:62 WC-4 (contract path is the one the row names; default `<output-dir>/return-contract.yaml`; file-valued `--output` (tdd S:90, init-lite S:87, spec-panel S:120) gives `<output-file>.return-contract.yaml` beside the file); S:73 (brief states the output path); S:182 step 3; S:196 AC-1.2 (directory or file as the row says) | One sibling-path rule is the smallest addition that makes the path predictable without a new flag. |
| M3 | applied | S:62 WC-4 (workflow excepted: package id is generated, `INV-B:52`, so the worker reports the contract in the one new `.dev/tasks/to-do/<id>/`; workflow pre-creation STOPs write no contract, mapped to `failed` by WC-5); S:76 ("Contract" = file at the path the row names); S:92 workflow small-fix cell (pre-creation fix deleted); S:198 AC-1.4; adversarial's `<output>/adversarial/return-contract.yaml` (S:83) is now covered by "the path the row names" | Deleted the pre-creation-STOP fix instead of inventing a directory for it (`INV-B:39` says today's skill does not write it). |
| M5 | applied | Same edits as M1 (S:154, S:159, S:195): implement, post-release and pr-submit (P4, S:109, 113, 114) and every P2/P3 command are removed from the P1 flag scope and AC-1.1; AC-1.1 now says later phases add their own commands to the test | No D2-D4 dependence remains in P1. |
| M4 | not touched | none | Not in IDS; the verifier rejected it (verify-1.md, M4 row), a noted, unactioned finding. |

## Notes
- No existing P1 command row changed except workflow's small-fix cell. Minor and Medium findings left alone.
- Process slip: I briefly saved the before-copy of the spec at `/tmp/claude-0/spec-before.md` (outside the sandbox) and a helper script in the workspace root; both were moved into the run's own `tmp/` directory next to `ws/` and nothing else outside the sandbox was written or read.
- Not run: the spec-panel and any re-review. No PASS is claimed.
