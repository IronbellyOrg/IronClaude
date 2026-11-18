# Merge Log (Step 5)

## Metadata
- Date: 2026-11-16
- Executor: merge-executor (plan executor only; no strategic decision, no grade changed)
- Plan: `adversarial/adversarial/refactor-plan.md` (14 merged findings G1 to G14, earlier-review table, dropped list; review status auto-approved)
- Base variant: V1 (`variant-1-original.md`, analyzer, sonnet class), selected in `base-selection.md`
- Other inputs read: `variant-2-original.md`, `variant-3-original.md`, `invariant-probe.md`, `debate-transcript.md`, `debate/round2-advocate-2.md`, `debate/round2-advocate-3.md`; the repo lines named below were re-read where no source held a quote
- Output: `adversarial/merged-review-card.md` (parent of this folder); this log
- Result: 14 of 14 planned findings applied, plus the earlier-review table, the disagreement section, the dropped list and the Checked section. 0 skipped, 0 failed.
- Entry counts: blocking 2 (G1, G2), MEDIUM 4 (G3 to G6), minor 8 (G7 to G14)

## Planned changes

| # | Change | Status | Provenance on the card | Notes |
|---|---|---|---|---|
| 1 | G1 Task 1 line P4:37 unpassable; ledger go row; where the window result is recorded | applied | V1 F1, V2 D2, V3 F1, INV-010, INV-018 | V1 F1 citations kept; INV-010 sentence added (README:15); S3:161 re-read to back "quote RT1 and RT2" |
| 2 | G2 `follow-up candidates` removal against the mapping test; condition and the one grep | applied | V1 F2, V1 F5, INV-019, round 2 evidence | blocking, conditional on stage 3 Task 8 as written; settling grep and the re-pin ask taken from round2-advocate-3 sections 3 and 4; FR-8 line PANEL:332 included |
| 3 | G3 pinning tests not run after the last edit; one final run in Task 6 | applied | V1 F6, V3 F4, INV-008, INV-016, INV-020 | MEDIUM (probe raised from minor); `test_worker_contract.py:893` quote re-read from the repo |
| 4 | G4 Task 5 cannot be applied to the plugin twin as worded | applied | V1 F7, INV-006, INV-007 | MEDIUM; re-checked live: `plugins/superclaude/commands/spec-panel.md` has no `Unattended mode` match, `src/superclaude/commands/spec-panel.md:455` has the heading |
| 5 | G5 Task 5 narrowing not checked | applied | INV-012 | MEDIUM; SPEC:739 quote taken from the live line (the probe's copy had single quotes and no `[E]`) |
| 6 | G6 gate checks run after the edits | applied | V1 F8, INV-017 | MEDIUM (probe raised from minor); the Fix sentence combines the plan's "fix the plan before the first task" with V1 F8's point that the gate sits in acceptance lines |
| 7 | G7 "allow-list of the stage 3 scan test" | applied | V1 F3, V3 F5 | minor |
| 8 | G8 lowercase "after 2 fix cycles" in the tdd file | applied | V1 F4 | minor; V1 wrote a hyphen where the live file has an em dash, so the quote is the shared part "after 2 fix cycles (3 reviews), HALT and escalate" |
| 9 | G9 acceptance lines not pinned by content | applied | V1 F9, V3 F4 (first half) | minor |
| 10 | G10 Task 2 cap-sentence line and Medium wording check | applied | V2 D3, INV-016 | minor; round2-advocate-2 section 2 added to say digest equality already ties the cap content |
| 11 | G11 strict T2 reads tracked files; reverse-scan half vacuous | applied | V3 F2 | minor |
| 12 | G12 registry row model; second `canonical` row against the `plugin` surface | applied | V3 F3, INV-005 | minor, conditional on the stage 1 test; S1:96 origin sentence added from round2-advocate-3 |
| 13 | G13 strict T2 on unregistered files holding the fence opener or old sentence | applied | Round 2 N-1, INV-014 | minor (conditional); S1:209 quote taken from the live line (round2-advocate-3 had added bold marks) |
| 14 | G14 four small gaps (OD16 check, scale-map repo paths, stage 3 done, Task 7 ending) | applied | INV-013, INV-015, INV-011, V2 note | minor; the four fixes are the executor's wording of what each source says is missing |
| 15 | Earlier-review table (F3/F9/F13, F4, F5/F12, F6) | applied | V2 notes, V3 Checked, INV-002, INV-009 | status and the resolving plan line per row |
| 16 | Changes NOT being made (dropped list) | applied | refactor-plan.md, debate-transcript.md matrix | section `## Dropped`; X-002 stated as folded into G3, not dropped |
| 17 | Reviewer disagreement section (C-002, C-010, probe-raised grades) | applied | transcript, round 2 statements, probe summary | not a numbered plan row; requested in the brief |
| 18 | Checked section | applied | V1, V2, V3 Checked and the probe's ADDRESSED rows | merged into 12 bullets |

## Points to report
- Two findings were appended in one edit (G7 and G8); every other finding was appended on its own.
- The `## Dropped` and `## Reviewer disagreement` sections quote `debate-transcript.md`, which is on the executor's read list but is not a variant, the probe or a Round 2 statement.
- V1 cited S1:211 for the `pointer-only` sentence; the live line is S1:209, so the card says S1:209 (G4).
- The Fix sentences of G6, G10 and G14 are the executor's wording of the gap each source names; no new requirement was added.

## Post-merge check

Method: a Python script run with `uv run --no-project python` from a private `mktemp` directory under `/tmp` (removed afterwards). It parsed every `key:line "quote"` citation in the card (163 in all), resolved each key to a file (P4, S1, S3, SPEC, README, S3REQ, SRC4, MAP, PANEL, PPANEL, RLP, a repo path, or `ADV/...`), collapsed whitespace and unescaped `\"` in both the quote and the file, and searched for the quote on the stated line or line range of that file. It then searched the same quote in each source file (V1, V2, V3, the probe, the three Round 2 statements and the transcript).

- Every G-id present once: yes. The line-start pattern `G<n> | blocking true or false | blocking, MEDIUM or minor |` matched G1 to G14 in order, once each. Each entry is followed directly by its `<!-- Source: ... -->` comment (18 provenance comments: 14 findings and 4 section comments).
- Every citation present in a source file: 163 of 163 sit on their stated line in the file named by the key (the first run found 4 wrong: S1:211, SPEC:739, tdd:125 and S1:209; all four were corrected and the run repeated clean). 131 of the 163 quotes also appear in a variant, the probe, a Round 2 statement or the transcript. The other 32 are not in any of those files and were re-read from the repository: P4:20 (2), P4:24, P4:25 (2), P4:33, P4:40, P4:50, P4:55, P4:64 (2), P4:70, P4:84, P4:88, P4:89 (2), P4:90, P4:99 (2), P4:102, P4:104, P4:111, PANEL:259, PANEL:372, README:17, RLP:32, S1:209, S3:161, SPEC:739, SRC4:16, `tests/skills/test_review_brief_placement.py:137` and `tests/skills/test_worker_contract.py:893`. Citations not found anywhere: 0.
- No contradiction between the Verdict and the entries: the Verdict says 2 blocking and 12 non-blocking; the entries show `blocking true` on G1 and G2 only, grades blocking 2, MEDIUM 4, minor 8, and the flag matches the grade on all 14. The earlier-review table, the dropped list and the Checked section do not restate a grade that differs from G1 to G14 (the Checked section says the blocking grades hold; the disagreement section gives the same grades as the plan).
- Structure: sections in order are Verdict, Findings, Earlier-review findings, Reviewer disagreement, Dropped, Checked; the append marker is gone.
- Limit: the script proves that each quote exists on its line; it does not prove that the quote supports the claim next to it.
