# QA Fix Log, Gate 3 (report validation), fix cycle 2 (last cycle)

**Status:** Complete
**Date:** 2026-11-08

---

Target: `RESEARCH-REPORT-bmad-first-use.md`. Input: `qa/qa-consolidated-findings-phase6-cycle2.md` (BLOCKING_COUNT 5). Notes (MINOR) not acted on. Line numbers are those before the edits.

## Row 5 (B-4): "template push only" for B3 and D3 (done first because rows 1 and 4 depend on it)

- Evidence read: `main.tf:74` (`catalogue_sha256` hashes every file under `image/catalogue/**`; `main.tf:104-107` folds it into `image_inputs_sha256`, which names the image tag at `main.tf:111`); `Dockerfile.coder:593` (`COPY --chown=0:0 catalogue /catalogue`, an existing COPY, so 0 new layers); report steps 4B.6 (L1499) and 4D.7 (L1521) edit `image/catalogue/bmad/manifest.yaml` unconditionally; step 2.5 (L1403) and step 7.2 (L1610) already say an edit under `image/catalogue/` retags the image and needs `coder update`.
- Decision: the true statement is that B3 and D3 as planned need a template push for `modules.tf` AND a catalogue-hash retag (two delivery layers). By the rubric (L1004) two delivery layers is L. The plan was left as written (the manifest sentence stays); the report now says `modules.tf` alone would be a template push (S on the researched minimum).
- Changed: delivery-variants table B3 row (L1083); Option B Effort (L1087, M to L), Risk (L1088, "no rebuild" removed) and Pros (L1091); Option D D3 Effort (L1137, M to L) and Pros (L1141); Table 1 Effort cells for B3 and D3 (L1227, M to L); Table 1 "Image rebuild or only a template push" cells for B3 and D3 (L1234); Rationale 4 (L1311); steps 4B.1 (L1494), 4D.1 (L1515) and 7.7 (L1615); Section 9 row 1 (L1691); constraint K-05 (L625). L204 is the general rule about root `.tf` files, still true, not edited.

## Row 1 (F-1): D2 left at "S (4 files)"

- Evidence read: report L1355, L1476, step 4D.6 (L1520: D2 is built for the (no, session) case), steps 5.3 and 5.4 (L1534-1535: a new test file and driver-table row in `coder-ci-aidev02-contract.yml`, and a second-file check in `test-73`), step 4D.7 (manifest.yaml and README.md words).
- Count by the rubric (L1004): 8 files as planned (new `20-*.json`, `Dockerfile.coder`, `main.tf`, `test-73`, `manifest.yaml`, `README.md`, the new first-use test, `coder-ci-aidev02-contract.yml`); 2 new or amended tests; one delivery layer (image). 8 or more files is L, so D2 is rated L as planned, not the M the finding proposed (M would contradict the 8-file rule). S stays as the researched minimum (4 files).
- Changed: Option D D2 Effort (L1137); Table 1 D2 Effort cell (L1227); Section 7 Stage 1 "Why" (L1299), which now names D2 and says Effort does not favour B3 or D3 over B1 and D1.

## Row 4 (B-3): "cheapest" while the Effort row is disclaimed

- Evidence read: rubric L1004-1005, L1087 and L1227 (B1 S, B3 now L), L1299, L1311.
- Changed: Option B Pros (L1091) "Cheapest" became "Lowest risk of the three (no certain break, 0 layers)"; Rationale 4 (L1311) now rests on the Risk, Image layers and HOME persistence rows, names Effort (L, against S for B1) and Image rebuild as the price; Phase 4 Goal (L1465) "cheapest evidence-ranked" became "evidence-ranked". Grep afterwards for `cheapest`, `template push only` and `S (4 files)`: only L204 (the general root-`.tf` rule) remains.

## Row 2 (B-1): Phase 4 gate order stated four ways

- Evidence read: report L1463, L1477-1488 (gate heading, procedure, Fact 1 needs the stub or hook plus the Phase 3 block, so a candidate build of the chosen branch), L1300 (Stage 2), L1517 (step 4D.3 inside 4D), L1669, L1694.
- Decision: one order everywhere. The gate is run on the candidate build of the chosen branch (steps 4B.1 and 4B.2; 4D.1 to 4D.3 for D3; 4D.6 for D2), drafted and not shipped, before the branch is relied on; a failed Fact 1 discards that draft.
- Changed: Phase 4 heading parenthetical (L1463); gate heading (L1478, was "Gate before any branch"); gate Rule row (L1488); Section 7 Stage 2 (L1300); checklist item (L1669); Section 9 row 4 resolution (L1694). The Phase 4 table of owner answers (L1470-1476) is unchanged: it is about the owner gate, not this gate. Grep afterwards: no "Gate before any branch" and no "observed before B or D is relied on" remain.

## Row 3 (B-2): open owner defaults recorded as `(constraint)` memlog bullets

- Evidence read: `.claude/skills/bmad-spec/SKILL.md:54` (memlog is the append-only decision of record), `SKILL.md:61` (valid types: decision, constraint, capability, assumption, question, direction, note, event), `_bmad/scripts/memlog.py:164-177` (`cmd_append` only appends; the only other mutating command is `cmd_set` on front-matter fields, no entry edit or delete), report step 3.4 (L1459: owner has not decided), Section 9 rows 5, 6, 10, step 7.1 (L1609: reversal by superseding).
- Changed: Phase 3 header (L1452) now records each open default (steps 3.2, 3.3, 3.4) as `--type assumption` ("plan default pending owner, Section 9 rows 5, 6, 10"), owner inputs as `--type question`, only the step 3.6 prohibitions as `--type constraint`, and the owner's later answer as a superseding `--type decision`; the CAP-8 success text says the command and predicate are defaults until rows 5, 6 and 10 are answered; step 1.1 (L1383) and Stage 0 (c) (L1298) and the Phase 1 checklist item (L1656) say the same. L409 only describes the existing memlog and was not edited. Grep afterwards: every remaining `(constraint)` or `--type constraint` is either L409 or limited to the step 3.6 prohibitions.

## Observation outside the five rows (not acted on)

- Option C Effort is rated M as planned for a new command; by the same count used for D2 (Dockerfile.coder, helper, `main.tf`, `manifest.yaml`, `README.md`, new test, driver row, pass-through case) it may also reach 8 files. No finding named it, so it was not re-counted; it is for the reviewer or the owner of the next cycle.

## Result

- Findings in scope: 5. Fixes applied: 5 (rows 1, 2, 3, 4, 5). Findings not fixed: 0. 5 + 0 = 5.
- Deviation from a proposed fix: row 1 proposed M for D2; the rubric count (8 files) gives L, so L was written with the count shown.
- No MINOR note (N-1 to N-5) was acted on. Q1 and Q2 stay unanswered, every `[synthesis inference: ...]` label was kept, no evidence was invented, only the report and this log were edited, nothing was staged or committed.
