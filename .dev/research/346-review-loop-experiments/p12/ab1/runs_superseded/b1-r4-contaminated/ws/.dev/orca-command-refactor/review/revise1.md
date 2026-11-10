# Revise 1

candidate: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md (edited in place; blocking ids M2, M3, M5 from review/round1.md Reviser brief)

## Byte accounting
- Before: 57763 bytes. After: 58235 bytes. Net +472.
- Per finding id (net bytes; edits are in-place extensions, wording replaced is counted inside the net figure):

| id | bytes added (net) | bytes deleted (net) |
|---|---|---|
| M2 | 84 | 0 |
| M3 | 240 | 0 |
| M5 | 148 | 0 |
| total | 472 | 0 |

(The M2 edit also rewrites "step 4 uses" to "steps 3 and 4 use"; the few replaced bytes are netted in the 84.)

## Findings
| id | disposition | where | note |
|---|---|---|---|
| M2 | applied | spec AC-0.4 (line 194 in the original; "7.2 step 3" at line 182 left unchanged) | AC-0.4 now says steps 3 and 4 use the command's existing report file in P0, the same relaxation round1.md M2.b recommends. Basis: contract added in P1 (spec:159), troubleshoot report is REPORT.md (spec:91), troubleshoot writes a contract only with `--caller task-unified` (`INV-B:242`, as quoted in round1.md; not re-read, UNVERIFIED here). |
| M3 | applied | spec WC-4 (line 62) | One rule added: when `--output` is a file (tdd, init-lite, spec-panel), the contract goes in the file's parent directory, which the brief must dedicate to the run; adversarial is named as the exception at `<output>/adversarial/return-contract.yaml`, matching spec:83. No new section or mechanism. Spec rows spec:83, 87, 90, 120 and AC-2.2 are unchanged and now consistent with WC-4. The sandbox spec-panel `--report-dir` evidence (`CMD:460`) is UNVERIFIED here. |
| M5 | applied | spec P1 scope (line 159) and AC-1.1 (line 195) | P1 flag and AC-1.1 scoped to commands whose phase is P1; P2-P4 commands gain the flag in their own phase; AC-1.1 states pr-submit, implement and post-release (P4) have no section yet. This removes the conflict with D3(a) (spec:240), spec:154 and spec:225. Lines 154, 162, 225, 240 untouched. |

Rejected findings M1 and M4 were left alone (noted, unactioned per round1.md). No other file was changed. No self-awarded PASS.
