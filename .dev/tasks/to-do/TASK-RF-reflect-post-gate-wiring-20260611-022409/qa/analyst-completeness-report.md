# Research Completeness Verification — Reflect POST Gate-Wiring

**Topic:** Replace terminal/per-phase POST reflect-gate EMISSION (O1 task-builder, O2 sc-tasklist) with flat `superclaude reflect run` Bash shell-outs under the SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE skip guard
**Date:** 2026-06-10
**Lens:** BREADTH (completeness — does every area the builder needs have coverage?)
**Analysis type:** completeness-verification
**Decision of record:** Option A (conform to contract; do NOT revive Mode-2/§6.3 dial taxonomy)

**Assigned files:**
- 01-o1-taskbuilder-edit-surface.md
- 02-o2-sctasklist-edit-surface.md
- 03-acceptance-test-and-guard-shape.md

**Also read:** ../research-notes.md, reflect-wrapper-contract.md (authoritative)

---

## Coverage Audit (research-notes.md EXISTING_FILES + GAPS → research files)

| Scope item (from research-notes.md) | Covered by | Status |
|---|---|---|
| O1: task-builder/SKILL.md all POST surfaces (verbatim + line refs) | 01-o1 Surfaces 1-8 + summary table | COVERED |
| O2: sc-tasklist SKILL.md all POST surfaces | 02-o2 Surfaces 1,3,4,5,7 | COVERED |
| O2: phase-template.md mirror | 02-o2 Surface 2 (+ mirror note) | COVERED |
| O2: structural checks #18-20 / Self-Check #6 | 02-o2 Surface 4a/4b | COVERED |
| O2: --no-reflect toggle (KEEP, distinct from dial) | 02-o2 Surface 5 | COVERED |
| Acceptance test: verbatim current Layer A + rewrite target | 03 §1, §3 | COVERED |
| Acceptance test: Layer-B/thinness DO-NOT-MODIFY list | 03 §2 | COVERED |
| Skip-guard / shell-out / exit-code verbatim shapes | 03 §4 (+ contract cross-ref) | COVERED |
| Frontmatter: start_commit / per-phase SHA / executor_model_class / reflect_post room | 01-o1 Surface 7; 02-o2 Surface 6; contract §6 | COVERED |
| TCS-depth reconciliation (wrapper fixed deep; PRE keeps TCS) | 01-o1 Surface 6; 02-o2 FLAG (L1471-1507) | COVERED |
| GAP-Q1 (exact O1 verbatim/lines) | 01-o1 | CLOSED |
| GAP-Q2 (exact O2 verbatim/lines + checks) | 02-o2 | CLOSED |
| GAP-Q3 (test rewrite anchor + assertions + xfail) | 03 §3 | CLOSED |
| GAP-Q4 (abs path + per-phase start SHA at gen time) | 02-o2 Surface 6; 01-o1 Surface 7 | CLOSED (with FLAG, see below) |
| GAP-Q5 (TCS depth fixed deep; removed only from POST) | 01-o1 Surface 6; 02-o2 FLAG | CLOSED |

Every EXISTING_FILE and every numbered GAPS_AND_QUESTIONS item from research-notes.md is covered. No scope item is orphaned.

---

## Per-Criterion Lens Evaluation (BREADTH)

### Criterion 1 — Every O1 edit site identified with exact line range + verbatim block? **PASS**
01-o1 enumerates 8 surfaces, each with VERBATIM blocks and a summary table (lines 207-214). Spot-verified live:
- Surface 1 (L2193-2198) — `- [ ] **N.{X-1} -- Independent post-execution reflection gate (run via subagent)**` matches L2193 exactly.
- Surface 2 (Critical Rule 20, L2312) — verbatim block matches L2312 exactly (self-run subagent form, MALFORMED clause).
Surfaces 3 (A.9 L1073-1076), 4 (validation checklist L2253), 5 (banner L1722-1724), 6 (TCS/O4 L2318-2358), 7 (frontmatter L2137-2156), 8 (cross-ref grep sweep) all carry verbatim + line refs. The grep sweep (Surface 8) explicitly confirms `superclaude reflect run`, `executor_model_class`, `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` = ZERO occurrences (must be introduced) — this is the breadth-critical negative-space coverage.

### Criterion 2 — Every O2 edit site identified with exact line range + verbatim block? **PASS**
02-o2 enumerates 7 surfaces + a 10-row summary table (L350-361). Spot-verified live:
- SKILL.md L1041 heading `### T<PP>.<final> -- Post-Execution Reflection: sc:reflect --mode post` matches exactly.
- SKILL.md L1063 spawn directive `/sc:reflect --mode post --remediate --tasklist ... --diff <phase-commit-range> --depth <DET..> --tier <DET..> --executor-model <EXECUTOR_CLASS> --output ...` matches exactly.
- struct check #18 (L1169) verbatim matches.
phase-template.md mirror (Surface 2, L117-174) covered with its own verbatim. A complete grep sweep (Surface 7) tabulates EVERY token line with KEEP/CHANGE disposition for both files, plus a confirmed ZERO-hits list (`superclaude reflect run`, `start_commit`, `executor_model_class`, `--base`, `--no-promote`, `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE`, the `<phase-N-start-sha>` exact token).

### Criterion 3 — Acceptance-test rewrite target verbatim (49-84) + flat anchor + assertions + Layer-B DO-NOT-MODIFY list? **PASS**
03 §1 quotes the rewrite target verbatim: module constants 18-46 (1a), `_extract_wrapper_branch` 49-60 (1b), xfail decorator + body 63-84 (1c). §2 is an 8-row DO-NOT-MODIFY table covering Layer B (87-94), thinness (97-134), shared constants (18-46) — explicitly "only lines 49-84 in scope". §3 proposes a flat heading anchor `#### POST reflect gate (O1` (no Mode taxonomy) with two delimiting strategies, a concrete rewritten helper, and the full positive/negative assertion set (`superclaude reflect run`, `--depth deep`, `--fix`, `--promote`, `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE`; negative reuse of `_NESTING_TOKENS`). §4 quotes the §3.2 guard + §2 exit-table verbatim. §6 confirms every asserted flag is a REAL Click option in commands.py.
Live md5 of the test file = `124549e67dd25258c7739371b4a89cb2` — matches R3's stated md5 exactly. (Minor: R3 says "135 lines total"; live `wc -l` = 134 — a 1-line discrepancy with no load-bearing impact since the scope is line-range 49-84, which R3 also re-cites by symbol, not just by absolute count.)

### Criterion 4 — Frontmatter persistence located with insertion points, including the FLAGGED phase-files-have-no-frontmatter collision? **PASS (with correctly-surfaced blockers)**
- O1: 01-o1 Surface 7 (L2137-2156) gives the exact generated-MDTM frontmatter template and specifies ADDING `start_commit`, `executor_model_class`, and leaving ROOM for wrapper-written `reflect_post` — with a concrete capture mechanism (`git rev-parse HEAD` at build). It also flags the reversal: the existing L2195 prose "`start_commit` ... never as the diff base" is REVERSED under the wrapper path and must be rewritten.
- O2: 02-o2 Surface 6 is a KEY STRUCTURAL FINDING — phase files have NO YAML frontmatter today (live-verified: phase-template.md starts with `# Phase File Template` then `# Phase N -- <Name>`; no frontmatter block). It presents two contract-compatible options (prepend frontmatter vs inject `--base <sha>` on the gate line) and correctly flags that option 1 COLLIDES with structural check #5 ("Every phase file starts with `# Phase N -- <Name>`" — live-verified verbatim at SKILL.md L1128 area) and Sprint CLI TUI display-name extraction. It also flags that `executor_model_class` still needs a persistence slot even if `--base` sidesteps frontmatter for the SHA. This is the single most important breadth finding and it is surfaced, not buried.

### Criterion 5 — Contract conformance (O1 flags / O2 flags / skip-guard / exit-code) captured verbatim? **PASS**
- O1 `--depth deep --fix --promote`: contract §2 (L37-39) + 01-o1 §contract-anchors + research-notes GOAL. Verbatim.
- O2 `--depth deep --fix --no-promote --base <sha>`: contract §2 (L49-51) + 02-o2 header + 03 §4b. Verbatim, with the `--no-promote` REQUIRED rationale (no per-phase adapter, contract §5) captured.
- Skip-guard: contract §3.2 (L99-104) quoted verbatim in 03 §4a AND research-notes; marker name `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` confirmed against CLI `commands.py:44`/`:69`.
- Exit codes 0/10/11/2: contract §2 table (L65-73) quoted verbatim in 03 §4c, with CLI confirmation (`commands.py:36`/`:235`). "Only exit 0 completes the gate" captured in all three files.

### Criterion 6 — TCS-depth reconciliation (wrapper fixed deep; PRE keeps TCS) addressed? **PASS**
01-o1 Surface 6 decouples POST from TCS: O4 floor (L2356) and the L2320 intro must stop coupling POST to TCS; `{DEPTH}` plumbing removed from the POST item ONLY; the entire TCS apparatus (S1-S6, formula L2338, threshold table, O1/O2/O3 overrides) STAYS for PRE (A.10.7). 02-o2 mirrors this: COMPLEXITY_SCORE machinery (L1471-1507) + PRE invocation (L1455-1460) KEEP INTACT (PRE out of scope); POST no longer consumes `<DETERMINISTIC_DEPTH>`/`<DETERMINISTIC_TIER>`/`--tier`. Both correctly scope the removal to POST-only.

### Criterion 7 — Structural-check interactions (#18-20, Self-Check #6, checkpoint-is-last) flagged where the rewrite could trip them? **PASS**
02-o2 Surface 4 is dedicated to this. Self-Check #6 = structural check #6 (L1129) — KEEP (no invocation token). Checks #18/#19/#20 (L1169-1171) — #18 FLAGGED: it asserts the heading PREFIX `### T<PP>.<NN> -- Post-Execution Reflection:`; recommendation is to keep that prefix (drop only the `: sc:reflect --mode post` suffix) so #18 needs no edit — else #18 must be updated. #19/#20 KEEP. Checkpoint-is-last invariant (Surface 3, SKILL.md L1018-1034 + template L117-125) — KEEP (no token). Plus the additional structural check #5 collision surfaced under Criterion 4. This is thorough breadth coverage of the check battery.

### Criterion 8 — Sibling-worktree do-not-touch boundary documented? **PASS**
03 §5 is an explicit table of all three on-disk copies: THIS worktree (rewrite target, md5 `124549e6…`), `reflectWrapper` (BYTE-IDENTICAL, same md5 — live-confirmed THIS file's md5 = `124549e67dd25258c7739371b4a89cb2`), and `wrapper-onto-master` (stale/un-xfailed, md5 `9017231d…`). Hard "MUST NOT TOUCH OTHER WORKTREES" directive citing memory `feedback_worktree_discipline`.

### Criterion 9 — Ambiguity (xfail decorator disposition) surfaced rather than silently assumed? **PASS**
03 §3d surfaces the xfail disposition as an explicit OPEN QUESTION with options (a) keep `strict=False`→XPASS vs (b) remove→plain PASS, a reasoned recommendation (b), and a fallback condition. research-notes.md §AMBIGUITIES_FOR_USER independently records the same residual sub-decision (default: keep strict=False→XPASS per the stated acceptance phrasing). NOTE a soft TENSION between the two: 03 §3d recommends (b) remove→PASS; research-notes default is (a) keep→XPASS. Both are surfaced and non-blocking, but the builder should treat this as a single decision point and not silently pick one — see Minor gap M1.

---

## Contradictions Found

- **C1 (soft, non-blocking) — xfail disposition default differs between sources.** 03 §3d *recommends* removing the decorator (plain PASS); research-notes.md §AMBIGUITIES_FOR_USER *defaults* to keeping `strict=False` (XPASS). Not a factual contradiction (both flag it as an OPEN QUESTION for the user), but the builder must reconcile to ONE disposition. Surfaced, not silently resolved.

No hard contradictions about file content, line numbers, or contract shapes were found across the three files — they are mutually consistent and consistent with the contract.

---

## Compiled Gaps

### Critical Gaps (block synthesis)
None. Every builder-required area has verbatim coverage, line anchors (spot-verified accurate), and the two hard structural blockers (phase-file frontmatter absence, check-#5 collision) are explicitly surfaced with options.

### Important Gaps (affect quality — builder must resolve during build, but research located them)
- **I1 — `executor_model_class` persistence for O2 is located but NOT resolved.** 02-o2 Surface 6 correctly identifies that `--base <sha>` on the gate line sidesteps frontmatter for the SHA, but `executor_model_class` (contract §6) still needs a persistence slot, and the only frontmatter option collides with structural check #5. The research surfaces this as a decision the builder must make (prepend frontmatter + amend check #5, OR another mechanism). This is a genuine design-decision gap, correctly delegated — not a research omission. The builder should treat it as a task Open Question / human-decision point.

### Minor Gaps (must still be fixed)
- **M1 — Reconcile the xfail disposition to one value** (see C1). Builder should surface as a single Open Question, defaulting per the user's stated acceptance phrasing (research-notes default = keep `strict=False`→XPASS) unless the user picks remove→PASS.
- **M2 — R3 line-count off-by-one.** 03 §1 says the test file is "135 lines total"; live `wc -l` = 134. No load-bearing impact (scope is the symbol range 49-84, re-cited by symbol). Builder should re-confirm exact line numbers at edit time anyway (research-notes already instructs "researchers MUST re-verify" line anchors).
- **M3 — Heading-anchor coordination point.** 03 §3 proposes the flat anchor `#### POST reflect gate (O1` but notes the exact heading text is an R1/R3 coordination point. 01-o1 (R1) does NOT commit to emitting that exact heading. The builder must ensure the O1 emission in task-builder/SKILL.md carries the literal heading prefix the rewritten `_extract_wrapper_branch` greps for, or the acceptance test will not locate the block. This cross-file coupling is surfaced in 03 but needs the builder to close it concretely.

---

## Depth Assessment
**Expected depth:** Standard (per research-notes — focused, small edit surface, deep prior investigation).
**Actual depth achieved:** Meets/exceeds Standard. All three files carry verbatim current blocks, exact line anchors, full grep sweeps with KEEP/CHANGE dispositions, contract cross-references, and live CLI-surface confirmation (commands.py flag/line citations). Negative-space coverage (ZERO-occurrence token lists) is present in both O1 and O2 — this is the breadth signal that nothing was assumed present.
**Missing depth elements:** None for the stated tier. The two unresolved items (I1 executor_model_class mechanism, M3 heading coordination) are correctly framed as build-time decisions, not research omissions.

---

## Recommendations
1. Builder: treat **I1** (O2 `executor_model_class` persistence vs check-#5 collision) as an explicit Open Question / human-decision in the generated task — do not silently prepend frontmatter without amending check #5, and do not silently drop `executor_model_class`.
2. Builder: pin the O1 heading prefix (**M3**) so the rewritten `_extract_wrapper_branch` anchor and the task-builder/SKILL.md O1 emission agree on the exact literal (recommend `#### POST reflect gate (O1`).
3. Builder: reconcile the **xfail disposition (C1/M1)** to one value, defaulting to the user's stated acceptance phrasing.
4. Builder: re-verify all absolute line numbers at edit time (research-notes already mandates this) — spot-checks here confirmed L2193, L2312, L1041, L1063, L1169, and check #5 are accurate as of this read, but surgical Edits should re-anchor.
5. Builder: keep the PRE gate, TCS apparatus, `--no-reflect` toggle, Layer-B/thinness tests, and sibling worktrees strictly untouched per the scope fences all three files document.

---

## VERDICT: PASS

All 9 breadth criteria PASS. Coverage is complete: every EXISTING_FILE and every GAPS_AND_QUESTIONS item from research-notes.md is closed, every edit surface carries a verbatim current block with a spot-verified line anchor, the contract shapes (O1/O2 flags, skip-guard, exit codes, frontmatter) are captured verbatim, the TCS-depth reconciliation is correctly scoped POST-only, the structural-check battery (#5, #6, #18-20, checkpoint-is-last) is mapped with #5 and #18 collisions FLAGGED, the sibling-worktree boundary is documented, and the xfail ambiguity is surfaced as an Open Question.

No CRITICAL gaps. Findings carried forward are 1 Important (I1, a delegated design decision) and 3 Minor (M1 xfail reconciliation, M2 off-by-one line count, M3 heading-anchor coordination) — none block proceeding to synthesis/task-build; all are correctly framed as build-time decisions the research located rather than omitted.

**The research is COMPLETE and the builder has everything needed to write surgical Edits.**
