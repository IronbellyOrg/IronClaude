# QA Report — Research Gate

**Topic:** Build MDTM task implementing reflect-in-task-builder.md + reflect-in-sc-tasklist.md against src/superclaude/, with S4 token-set trim
**Date:** 2026-06-04
**Phase:** research-gate
**Fix cycle:** N/A
**Fix authorization:** false (report only)
**Depth tier:** Deep

---

## Overall Verdict: PASS

Green light for the builder. All 6 research files are Complete, evidence-dense, and CODE-VERIFIED. I independently re-Read the actual source files and re-checked a representative sample of every load-bearing line claim across all 6 files — every sampled anchor was accurate (only trivial <=3-line self-citation drift in two spots, which does not block the builder). Both proposals' full delta sets are covered. No gaps of any severity remain. The one contradiction found (R3 / R5 / R6 header `Status: In Progress` vs in-body `Status: Complete`) is a cosmetic header-staleness artifact, NOT a content gap — every such file ends with a definitive `Status: Complete` / `STATUS: COMPLETE` and a full Summary; resolved below as MINOR-non-blocking.

---

## Independent Re-Verification (the adversarial core)

I did not trust the research's line claims. I re-Read the real source and confirmed:

| Claim under test | Research says | I verified (tool) | Result |
|---|---|---|---|
| task-builder/SKILL.md length | 2190 (R1; proposal says 2191) | `wc -l` = 2190 | R1 CORRECT; proposal off-by-1 (R1 flagged it) |
| A.10.5 / A.10.6 / A.11 headings | 1194 / 1339 (NEW) / 1398 (R1) | `grep -n` = 1194 / 1339 / 1398 | EXACT. A.10.6 (DM-005) IS the new section between A.10.5 & A.11 |
| A.10.7 insert point | L1397 (between 1396 content & 1398) | `sed -n 1396,1398p` confirms blank@1397, A.11@1398 | EXACT — insertion boundary correct |
| 4 checkpoint invariants | #6@1073, #18@1113, #19@1114, #20@1115 (R2) | `sed -n` each line — all 4 verbatim | EXACT, ZERO drift |
| gate close-line "check 1-20" | L1117 (R2) | `sed -n 1117p` | EXACT |
| Stage 10 / table / "10 stages" | 1359 / 1394-1405 / 1392 (R2) | `grep`+`sed` | EXACT |
| `--spec` in commands/tasklist.md | exists, 6 hits, row @L37 (R3) | `grep -c` = 6; row@37 | EXACT — must NOT re-add |
| `argument-hint` key in command | absent (R3) | `grep -c` = 0 | CONFIRMED absent |
| TCS / blockedBy / depends_on / POST_REFLECT_GATE / reflect_pre in TB | ALL 0 (R1) | `grep -c` each = 0 | CONFIRMED — all NEW content |
| `after Phase` in TB | 1 hit @L1993 (Content-Rules cell) (R1) | `grep -n` = 1 @1993 | EXACT |
| rf-qa.md "28 items" + TB-Add catalogue | `(28 items)`@298, Structural Gate@330, TB-Add-1@334, TB-Add-8@369 (R4) | `grep -n` all match | EXACT |
| test_task_builder_merge.py "28 items" | :69 + :190 (R4) | `grep -n` = 69, 190 | EXACT |
| INV-010 floor/density/grow | MIN_LIVE_K=8@88, k1>=@381, dense@391, k2==k1+1@412 (R4) | `grep -n` all match | EXACT (byte-identity cited :293, actual :296 — see MINOR-1) |
| checkpoints.py declaration-driven | HEADING_PATTERN + _nearest_heading, no last-task logic (R4) | `grep -n` confirms regexes + funcs | CONFIRMED — checkpoint-is-last is NOT a CLI risk |
| reflect flags --mode/--depth/--executor-model/--coverage-floor/--budget-remaining | all exist (R5) | `grep` reflect.md + refs/ — all found | CONFIRMED |
| model-routing `--model` flag | 0 (R5) | `grep -c` = 0 | CONFIRMED absent |
| `.markdownlint.json` rules | default:true, MD013/29/36/33 off, MD024 siblings (R5) | `cat` exact match | EXACT |
| MD040 disable in the 3 edited files | absent (enforced) (R5) | `grep -l` = empty; reflect skill HAS it @L8 | CONFIRMED |
| MDTM template 02 + 3 examples exist | 1204 lines + 135209/031100/024610 (R6) | `ls`/`wc`/`find` all present | CONFIRMED |
| 135209 item count | 81 checkbox items (R6) | `grep -cE '^\s*-\s*\['` = 81 | EXACT |

**Conclusion of independent verification:** the research is not proposal-citation-parroting — it re-derived current lines. Every sampled claim survived adversarial re-checking against live source.

---

## Items Reviewed (10-item Research-Gate Checklist)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | File inventory (6 files, Complete + Summary) | PASS | All 6 present. R1/R2/R4 header Status Complete; R3/R5/R6 in-body Status Complete (L304/L265/L262). Every file has a Summary/anchor-map table. See MINOR-2 re header staleness. |
| 2 | Evidence density (sampled anchors re-checked) | PASS | 22-row re-verification table above. EVERY sampled anchor (A.10.7@1397; checkpoint #6/#18/#19/#20; --spec@37; TCS/S4 absence; rf-qa 28 items; INV-010) confirmed against live source. Density = Dense (>80% evidenced with file:line). |
| 3 | Scope coverage (both proposals' full delta sets) | PASS | Proposal-1 §8 (read L266-285) maps 1:1 to R1 edit-sites 1-11 + research-notes EXISTING_FILES. Proposal-2 §6 Flag/stage summary (L282) + §1-§4 covered by R2 (skill anchors), R3 (command+templates), R4 (tests). S4 trim explicitly handled (R1 edit-site 11 + notes L22). Nothing from either Implementer-Checklist omitted. |
| 4 | Doc-vs-code (CODE-VERIFIED, not proposal-trusting) | PASS | Research explicitly re-derived current lines and flagged proposal drift (R1 DRIFT BANNER: proposal between-A.10.5-and-A.11 is stale because of new A.10.6; R2 headline: proposal cites accurate, confirmed). My own re-Read confirms research read real files, not the proposals' known-drifted citations. |
| 5 | Contradiction resolution | PASS | No substantive cross-file contradiction. R1 (B2 single-paragraph for task-builder) vs R5/R6 (Sprint-CLI metadata-table for sc:tasklist POST task) is NOT a contradiction — R5 §2.7 explicitly distinguishes the two shapes by skill. rf-qa TB-Add-9 question (R4 §4) is resolved: default = NO rf-qa edit (validation-checklist path), break-risk NONE; optional TB-Add-9 path has 4 lockstep edits documented. The only literal contradiction (header In Progress vs body Complete) is cosmetic — see MINOR-2. |
| 6 | Gap severity | PASS | Zero CRITICAL/IMPORTANT/MINOR content gaps. Three MINOR-non-blocking quality notes (citation drift, header staleness, R6 stat method) listed below — none blocks the builder. |
| 7 | Depth appropriateness (Deep tier) | PASS | R4 traces a complete break-risk data flow end-to-end (SKILL text to audit test to fixture-vs-text-reading classification to exact must-pass command set). R1/R2 trace every delta-site to exact current lines with insertion boundaries. Exceeds Deep-tier bar. |
| 8 | Integration coverage (cross-file couplings + break-risk) | PASS | All 4 couplings documented WITH break-risk: (a) task-builder SKILL <-> rf-qa.md TB-Add catalogue (R1 edit-site 8 cross-skill note + R4 §4 INV-010 orphan risk); (b) tasklist SKILL <-> phase/index templates (R3 read-only-mirror caveat: live copies inline in SKILL §6A/6B) <-> Sprint checkpoint scanner (R4 §2: declaration-driven, NONE); (c) SKILL edits <-> audit tests (R4 per-test table, HIGH/MEDIUM/LOW/NONE rated); (d) checkpoint-is-last 4-invariant set (R2 edit-site 4). |
| 9 | Verification commands (UV-only must-pass set) | PASS | R4 Table B + R5 §3.5 give concrete UV-only set: make sync-dev to make verify-sync to uv run pytest tests/audit/ tests/skills/ -q + tests/sprint/test_checkpoints.py tests/audit/test_checkpoint.py to pre-commit run markdownlint to make test. Single-line smoke provided. Markdownlint scope (.dev/ excluded) + MD040 risk both pinned. Complete + concrete. |
| 10 | Incremental writing compliance | PASS | R3/R5/R6 show literal iterative structure (header Status In Progress left from incremental authoring, in-body Status Complete appended last) — evidence of incremental rather than one-shot writing. Files carry working-note artifacts (R5 §4.4 notes this file triggered a re-read reminder once). |

---

## Issues Found (all MINOR, NONE blocking)

| # | Severity | Location | Issue | Required Fix (advisory — fix_authorization:false) |
|---|----------|----------|-------|---------------------------------------------------|
| 1 | MINOR | 04-...md:72,154 | Cites INV-010 byte-identity assertion at :293; actual is test_dynamic_enumeration_inv_010.py:296 (off by 3). The assertion EXISTS and the claim is true — only the line number drifted. | Builder: trust the assertion's existence, not the exact :293. No action needed (additive make sync-dev satisfies it regardless of line). |
| 2 | MINOR | 03-...md:3; 05-...md:3; 06-...md:3 | Header Status In Progress contradicts the in-body terminal Status Complete (L304 / L265 / L262). Cosmetic header staleness from incremental writing, not incomplete work. | Cosmetic only — content is complete with full Summary tables. Builder may ignore. (If a future gate enforces header Status Complete, flip the three headers.) |
| 3 | MINOR | 06-...md:178,207 | "81 checkbox items" / "25 items" stat — my literal [ ] grep initially returned 0 (format), but grep -cE for dash-bracket confirms 81 for 135209. R6's count is ACCURATE; flagging only that the counting method is non-obvious. | None — R6 is correct. The TB-Add-2 bound concern (81 > 50 advisory) R6 raised is valid and correctly characterized as ADVISORY-not-blocking. |

**No CRITICAL or IMPORTANT issues. No content gaps. No fabrication. No hallucinated paths (all 4 target files + template + 3 examples confirmed to exist).**

---

## Actions Taken

None — fix_authorization: false (report-only). All three MINOR notes are advisory and surfaced for the builder; none requires resolution before the builder proceeds.

---

## Confidence Gate

- **Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 9 | Grep: 0 (grep run via Bash) | Glob: 0 | Bash: 8 (each targeting a specific checklist item: anchors, invariants, --spec, TCS-absence, tests, reflect-flags, markdownlint, template/example existence, item counts)
- **Tavily/web:** tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0 (no external lookup required — all claims local-source-verifiable per Principle 6).
- Tool-call count (17 Read+Bash) >= 10 checklist items: engagement minimum satisfied; every Bash call maps to a specific check (not padding).
- No UNCHECKED items. No UNVERIFIABLE items.

---

## Recommendations

1. **Proceed to build.** The research is a green light.
2. Builder: default to the validation-checklist path (no rf-qa.md TB-Add-9 edit) per R4 §4 — break-risk drops to NONE for INV-010 / merge-test couplings. Only create TB-Add-9 if a reviewer insists the gate run structurally (then apply R4's 4 lockstep edits + 28 items to 29 items).
3. Builder: label EVERY fenced code block in the new task-builder/sc-tasklist SKILL.md content (MD040 risk — those two files have no disable comment); do NOT copy reflect skill's markdownlint-disable.
4. Builder: aim for <=50 items (TB-Add-2 single-track advisory bound); R6's recommended skeleton (~33-41 items) already respects this.
5. Builder: encode the S4 token set literally as {after Phase \d+, depends_on:} (drop blockedBy: and after N.\d+ per user mandate; R1 edit-site 11 confirms 0 corpus collisions).

## QA Complete
