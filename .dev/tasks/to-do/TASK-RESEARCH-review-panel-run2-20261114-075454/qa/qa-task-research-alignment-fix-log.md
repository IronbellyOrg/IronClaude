# Fix Log - A.10.25 research-alignment findings (F1, F2, F3, F4, M2)

**Date:** 2026-11-14
**Task file:** `.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/TASK-RESEARCH-review-panel-run2-20261114-075454.md`
**Source findings:** `qa/qa-task-validation-consolidated.md` (Addendum: A.10.25), `qa/qa-task-research-alignment-report.md`
**Method:** Read the target line with Read offset/limit, Edit with a once-occurring old_string, re-read after each edit. No sed -i, no rewriters.

Entries are appended below, per finding.

---

## F1 - item 2.13 (task file line 195)

- Edited: item 2.13 only (line 195), inside the "Slices to read first ... Code to read in the consumers" sentence of the agent prompt.
- Change: "44 `subagent_type: rf-*` lines in the tech-research SKILL.md" became "44 `subagent_type: rf-*` lines over the SKILL.md files of eight skills (per-skill split in scope slice 12 line 286; tech-research alone 1)". The 185 U2 figure and the "both [UNVERIFIED] until recounted" tag and recount instruction are unchanged.
- Proof: Grep for the new phrase returns exactly one hit (line 195); the only "44 `subagent_type: rf-*` lines" occurrence in the task file is that line. Slice 12 line 286 in `research/scope/12-e3-loop-variants-consumers.md` contains "task-builder 23, roadmap 12" (Grep hit), so the citation is valid.

## F2 - VL/DR duplicate-defect rule (items 5.08, 5.14, 5.17, 5.20, 5.23, 5.26, 6.57)

All seven edits are text additions inside existing items; line numbers unchanged (file stays 724 lines).

| Item | Line | What was added |
|---|---|---|
| 5.08 (synth-08) | 326 | RULES (3): where a `VL-NN-nnn` row and a `DR-nnn` row describe the same defect (D-1..D-31, X-1..X-22, D1-D13, B-1..B-7 appear in both the defect register and ledgers 23/24), keep ONE inventory row with a single destination (DR destination wins when the defect register re-verified it) and mark the other `DROP: duplicate of <ID>`. Second edit: the reconciliation line now also states the number of VL/DR duplicate pairs. |
| 5.14 (Gate 2, partition C, synthesis-accuracy) | 342 | GATE FOCUS: same check (one row, one destination, other row `DROP: duplicate of <ID>`, pair count in the synth-08 reconciliation line). |
| 5.17 (Gate 2, partition C, source-tracing) | 348 | GATE FOCUS: same check. |
| 5.20 (Gate 2, partition C, structure) | 354 | GATE FOCUS: same check. |
| 5.23 (Gate 2, partition C, content-quality) | 360 | GATE FOCUS: same check. |
| 5.26 (Gate 2, partition C, synthesis-coherence) | 366 | GATE FOCUS: same check. |
| 6.57 (Gate 5, anti-omission agent 4) | 576 | CHECKLIST step 3: a defect in both a ledger row (23/24) and a DR row must appear in Section 8.1 once with one destination, the other row `DROP: duplicate of <ID>` counts as COVERED-BY-DEDUP, the reconciliation line must state the pair count, and one defect in 8.1 twice with two destinations is an IMPORTANT finding. |

Proof: `grep -n 'DROP: duplicate of <ID>'` hits exactly lines 326, 342, 348, 354, 360, 366, 576 (7 items); `grep -n 'one defect appearing in Section 8.1 twice'` hits line 576 only; the partition C lens items were confirmed by header (5.14, 5.17, 5.20, 5.23, 5.26 are all "Gate 2, partition C"). Each Edit used a once-occurring old_string (the first 6.57 attempt matched 4 gate-5 agents, so it was extended with agent-4-only context before applying). `wc -l` still 724.

## F3 - slice gaps restored in Gate 1 focus and item 3.26

All edits are text additions inside existing items; line numbers unchanged (file stays 724 lines).

New wording used for gate focus (b): "every open item of research-notes.md for the file AND every gap or question in the `## Gaps and Questions` section of the scope slice(s) it reads is resolved, logged under Gaps and Questions, or carried as a ledger row".

| Item(s) | Line(s) | What changed |
|---|---|---|
| 3.01-3.12 | 232, 234, 236, 238, 240, 242, 244, 246, 248, 250, 252, 254 | GATE FOCUS (b) replaced: old "every open item listed for the file is resolved or logged under Gaps and Questions" became the new wording above. These 12 items carried the old sentence verbatim, so one Edit with `replace_all` through the Edit tool hit all 12 (a per-item old_string would have needed about 2 KB of shared text to be unique). |
| 3.13, 3.14 (research-depth lens, partitions A, B) | 256, 258 | These two items have no GATE FOCUS (b) clause (the research-depth lens uses a numbered checklist). The equivalent clause is checklist question 6 "Are open items honestly acknowledged rather than hand-waved?", which now carries the new wording in parentheses. One Edit with `replace_all` (that question occurred only in 256 and 258 before the edit). |
| 3.15 (research-depth lens, partition C) | 260 | Same adaptation on checklist question 6 "Are open items honestly acknowledged?" (single Edit, once-occurring string). |
| 3.26 (gaps log) | 288 | Added: also read the `## Gaps and Questions` sections of scope slices `research/scope/01-*.md` through `12-*.md`, give each unresolved slice gap or question a `GQ` row (or point to the `VL-NN-nnn` row that already carries it) so synth-10 can turn them into Section 9 questions. Single Edit. |

Deviations to flag: (1) 3.13-3.15 had no "(b)" gate-focus sentence, contrary to the dispatch note, so the new wording was put on their checklist question 6, which is the only open-items test those prompts contain. (2) 3.01-3.12 and 3.13-3.14 used `replace_all` instead of one Edit per item (each string was identical across the items; verified by scan below).

Scan proof (Bash read-only, per line 232..260): for each of the 15 items 3.01-3.15, count of the new wording = 1 and count of the old wording "every open item listed for the file is resolved or logged" = 0. Global: old wording occurrences 0; lines carrying the new "AND every gap or question in the `## Gaps and Questions` section of the scope slice" wording 15. All 12 scope slices contain a `## Gaps and Questions` heading (Grep count 12 files), so the 3.26 instruction is satisfiable. `wc -l` still 724; 187 `- [ ]` items, 0 checked.

## F4 - open items for the 8 unowned [CODE-CONTRADICTED] rows and the numeric disagreements (items 2.01, 2.04, 2.05, 2.08, 2.17; Builder Notes line 721)

All edits are text additions inside existing items (lettered open items in the items' own style); no item renumbered, no agent count, gate or phase changed. Every figure, commit id and line anchor in the added text is tagged [UNVERIFIED] until the agent re-derives it. Each edit also bumped the item's closing "open items (a)-(x) are resolved" clause to include the new letter.

| Item | Line | New open item | Claims now owned |
|---|---|---|---|
| 2.01 | 171 | (d); closing clause (a)-(c) became (a)-(d) | #519 + #518 attribution of the `cli/review` changes (re-derive with `git log` / `git show --stat`, `-- ':!.dev/tasks'`; #518 commit id `167184c6b` tagged [UNVERIFIED]); E2 run-2 reflect contrast ("reflect has no panel/tier code") vs `sc-reflect-protocol/SKILL.md:87`, `:340-349` and `src/superclaude/cli/reflect/` |
| 2.04 | 177 | (e); closing clause (a)-(d) became (a)-(e) | `T2bModel01` "not referenced anywhere in src/ or tests/" (Grep over `src tests docs scripts` + `ccsession-models.json`; anchors `ccsession-models.json:107`, `README.md:445`, `tests/unit/test_ccsession_tiers.py:72-73,239` tagged [UNVERIFIED]) |
| 2.05 | 179 | (e); closing clause (a)-(d) became (a)-(e) | harness brief `unpassable-ac` vs `unpassable-check` in `CATEGORIES` (`findings.py:15-22`) and the rules file; E2 `theory.py` HARD set (B3/B7 in, B5/I1/B6 out; read via `git show` at the E2 tip) |
| 2.08 | 185 | (e); closing clause (a)-(d) became (a)-(e) | alias GT3 vs GT1 (`COMBO-REPORT.md:497`, legend `:401-417`); `combos/` size 106/96/97/107, `RESULT.md` 19 vs 29, quarantine 428 vs 417, Qwen 3 vs 4 (all [UNVERIFIED] until re-counted with `git ls-tree` / `git show`) |
| 2.17 | 203 | (e); closing clause (a)-(d) became (a)-(e) | "159 functions" vs 179 (re-sum the E2 per-file test table); memory lesson "fenced yaml calibration not parsed by cluster" vs `src/superclaude/cli/review/cluster_cmd.py:27-34` (path confirmed by Glob; installed-CLI version at run time flagged unverified) |
| Builder Notes | 721 | sentence corrected | Old: "Phase 2 items 2.04, 2.05, 2.08, 2.10, 2.11 and others name the contradicted claims". New: names items 2.01 (d), 2.04 (e), 2.05 (e), 2.08 (b, d and e), 2.10, 2.11 and 2.17 (e) and states that between them they own all 13 [CODE-CONTRADICTED] rows and the numeric [UNVERIFIED] disagreements. |

Ownership cross-check against research-notes.md AMBIGUITIES_FOR_USER (13 [CODE-CONTRADICTED] rows): #519+#518 -> 2.01(d); D14 tasklist-reaches-no-reflect-panel -> 2.11 (already); reflect contrast -> 2.01(d); alias GT3 -> 2.08(e); "discarded with no error" -> 2.08(b); "four verdict flips" -> 2.08(b); "16 empty terra reviews" -> 2.08(d); `unpassable-ac` -> 2.05(e); `T2bModel01` -> 2.04(e); "159 functions" -> 2.17(e); "no missing-task category / no severity levels" -> 2.10 (already); `theory.py` HARD set -> 2.05(e); memory lesson -> 2.17(e). All 13 owned. Scan: a loop over Phase 2 item lines 171-225 listed CODE-CONTRADICTED occurrences in the assignments of 2.01, 2.04, 2.05, 2.08, 2.10, 2.11, 2.17 and the value-ledger items 2.19-2.24 (the DROP reason vocabulary), matching the corrected Builder Notes sentence.

Choice note: the dispatch said "2.15 or 2.17"; 2.17 was used because its slices (02, 11), its anchors (`cluster_cmd.py:27-34`) and its defect-register role already cover both claims, and 2.15 (telemetry) has no such link.

## M2 - item 4.01 (line 297)

- Edited: item 4.01 only. "both efforts lack a blind judge for E1." became "E2 scored reviewers with blind judges against a 16-defect ground truth; E1's quality-measurement design (seeded defects) was never run."
- Proof: Grep `both efforts lack a blind judge` returns 0; the read-back of line 297 shows the new sentence followed by "AGENT PROMPT (pass verbatim)". M1, M3, M4 untouched as instructed.

## Final verification (read-only Bash scan after all edits)

- `wc -l` of the task file: 724 (unchanged from before the fixes; every edit stayed inside an existing line).
- `- [ ]` items: 187; checked items `- [x]`: 0.
- Byte-exact halt messages unchanged: `Regression detected on Item X.Y, previously PASS at cycle N, now FAIL. Halt overrides monotonicity check.` 3 lines; `[HALT-MONOTONICITY] |F|=<n>` 4 lines (neither string was within any edited span).
- Placeholder scan: raw `TODO|TBD|FIXME` = 0 lines; the pattern literal `T[O]DO|T[B]D|FIX[M]E` still present (5 lines).
- Independence: the forbidden run-1 folder name appears on 153 lines after the fixes (count not taken before them, so no before/after comparison is claimed); the added text contains no path into that folder or the QUEUED note, and neither was opened.
- No `sed -i`, no rewriter, no Write over the task file: all 20 task-file changes went through the Edit tool (F1 1, F2 8, F3 4, F4 6, M2 1). Two F3 edits (items 3.01-3.12, and items 3.13-3.14) used `replace_all` for strings identical across those items, as noted under F3.
- Not touched: M1, M3, M4; any item numbering, agent counts, gates or phases.
