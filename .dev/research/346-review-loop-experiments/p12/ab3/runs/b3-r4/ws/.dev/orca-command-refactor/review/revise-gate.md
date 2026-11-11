# Revise (gate loop): orca-worker-contract-spec.md

Prompt followed: REVISE prompt in `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full). Ids from `.dev/orca-command-refactor/review/gate.md:130` (Reviser brief): BLK-1, BLK-2 only. Candidate edited in place: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. The spec-panel was not run; no PASS is claimed. Medium and minor findings (MED-1 to MED-9, MIN-1 to MIN-4) were left alone.

## Byte accounting
- Before: 58573 bytes (sha256 `fd9020aeb88b0fd3aa673b34de70465e3d6d2d18a0ec0245de39c5d2383e536b`, matches gate.md:7).
- After: 58669 bytes (sha256 `79f7d923a8aec892c0aa73658332d8e091d8ce46bc45e64a342ab24dea176c15`). Net +96.
- Per finding id (bytes of the replaced phrase deleted, bytes of the new phrase added, as measured on the edited phrases):

| Finding | Bytes deleted | Bytes added | Net |
|---|---|---|---|
| BLK-1 | 171 | 233 | +62 |
| BLK-2 | 119 | 153 | +34 |
| Total | 290 | 386 | +96 |

(BLK-2 phrases: 77 -> 76 and 42 -> 77. BLK-1 phrases: 60 -> 66, 15 -> 29, 30 -> 36, 34 -> 46, 32 -> 56. Net checks: 34 + 62 = 96 = 58669 - 58573.)

## Findings

| Id | Disposition | Where (candidate line numbers after the edit) |
|---|---|---|
| BLK-1 | Applied, by narrowing: load is named an explicit exception, the recommendation of gate.md:35. No contract or section is added for load; SPEC:112 and the Decisions row for load (SPEC:265) are unchanged and now agree with the tests. | Line 76: "Every changed command except load (section 6) also gains" (same defect: load is a changed command). Line 154: "brainstorm, init-lite and load (usage-line fix only) gain neither". Line 195 (AC-1.1): the positive set is "except load" and the negative set now lists load. Line 196 (AC-1.2): "each P1 command except load". Trace: P1 gate no longer requires a section or contract for load, whose 3.2 row says "none (see note)" and "n/a" (line 112) and which writes no file (`INV-B:31,62-65`, as cited by gate.md:33). |
| BLK-2 | Applied, by narrowing one path to match WC-4 (gate.md:45 offers this choice): adversarial's contract path is `<output>/return-contract.yaml`, the same as `<output-dir>/return-contract.yaml` in WC-4 (line 62) and brainstorm's row (line 84). Chosen over changing WC-4 because one rule serves the other contract writers and the coordinator needs no per-command directory. Residue: the skill's artifacts stay under `<output>/adversarial/` (gate.md:42, citing `INV-A:35`); only the contract file moves up one level. The skill source (`sk/sc-adversarial-protocol/SKILL.md:427-429`) was not readable in this sandbox, so the exact edit location is UNVERIFIED and left to the P1 plan; `INV-A:85` names the same line as the fix site. | Line 83: "Fix the contract path to `<output>/return-contract.yaml`, the WC-4 path (P1)". Line 198 (AC-1.4): "adversarial names `<output>/return-contract.yaml` and no other path", which now reconciles the two texts, so AC-1.2 steps 3 and 4 (lines 182-183) check one path. |

## Not touched
- No Orca-specific, rule, mechanism or section additions; each added phrase serves BLK-1 or BLK-2 above.
- `.dev/orca-command-refactor/specs/` holds no other edited file. This report is the only other file written.
