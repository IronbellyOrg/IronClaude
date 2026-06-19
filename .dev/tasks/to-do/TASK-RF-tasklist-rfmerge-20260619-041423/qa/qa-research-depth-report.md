# QA Report — Research Depth (research-depth lens)

**Track Goal:** Implement RFMerger P1-P5 into sc:tasklist generator.
**Date:** 2026-06-19
**Phase:** research-depth (Partition A)
**Lens focus:** Is the research DEEP ENOUGH to produce precise per-proposal implementation items WITHOUT re-reading source?
**Fix authorization:** false (report-only)
**Assigned files (Partition A):**
- 01-skill-stage-map.md
- 02-skill-conventions.md
- 03-integration-contracts.md
- 04-proposal-attachment-trace.md

**Adversarial stance:** Assume the research is superficial until proven otherwise.

---

## Tool-engagement summary

- Read: 9 (4 research files + 5 targeted source verifications)
- Grep/Bash: 3 (line counts, anchor greps, contract greps)
- Glob: 0
- Web (Tavily): 0 — all verification was local-file-bound; no external lookup required for the research-depth lens.

Source files independently re-verified (not relied on from research prose):
- `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` — lines 700-714, 820-844, 1180-1199, 1244-1312, 1429-1462, 1557-1619 (anchors + stale-17 + Stage 7/10/10.5).
- `src/superclaude/skills/task-builder/SKILL.md` — lines 878-911 (DM-003 8-field), 1066/1231/1389 (Execution Context + TB-Add-7), 1261-1305 (PR-02), `wc -l` = 2527.

---

## Lens findings (research-depth, Partition A)

### LF-1 — Q1 "HOW each stage works, not just WHERE": PASS
R01 §A gives per-stage What/Inputs/Outputs for all 11 stages, not just line anchors. Stage 4 enrichment (§5.2–§5.7), Stage 6 three-sub-gate decomposition, Stage 7 `split = ceil(task_count/2)` → 2N fan-out, merge, retry — all explained behaviorally. R02 §1 adds the *form* (numbered behavioral SECTION vs pipeline STAGE conventions). Independently confirmed Stage 7 body at SKILL.md:1244-1295 matches R01's description (split algorithm at :1253, 2N at :1263, 4-step merge at :1290-1295, retry clause at :1310). Depth is behavioral, not inventory.

### LF-2 — Q2 "data flow traced end-to-end for P2/P3/P4": PASS
R04 traces each:
- **P2 (loop state k/F_k):** in=`F_{k-1}` patched files → out=`F_k` full re-validation set; explicitly flags that Stage 10 today is a *cheap targeted re-read* (SKILL.md:1433-1439) and the loop must invoke the Stage-7 2N fan-out to compute F_k — a real behavioral gap, not hand-waved. Loop state (k, |F_{k-1}|, regression set) sink proposed (Verification Results table). Verified SKILL.md:1456 no-loop sentence and :1429 Stage 10 heading exist verbatim.
- **P3 (merge branch):** in=per-agent {findings | "No issues" | failure}; out=some-fail→synth HIGH + proceed / zero-success→escalate no-synth. Insertion = new step 1a between merge steps 1 (:1292) and 2 (:1293) + replace gate :1310. Confirmed the current retry clause is binary (success vs error) at :1310.
- **P4 (emit→inject):** in=checks 1-20 booleans at the pre-write gate (:1187); out=`validation/gate-results.txt`; inject site = inside the agent instruction block after :1268 before Drift check at :1271, OR as a 4th spawn-payload bullet at :1255-1261. Flags that `validation/` dir is first created at Stage 8 (:1407) and must move earlier. Verified all these anchors.
This is genuine end-to-end tracing with named producer/consumer sites, not entry-point listing.

### LF-3 — Q3 "reused contracts (DM-003, PR-02) explained at field-level for a conformance test": PASS
R03 §1.1 gives the full DM-003 8-field table (field / fixed-or-dynamic / exact value / line / reject-symbol). Independently verified against task-builder SKILL.md:878-911:
- `severity: HIGH`, `source: synthetic-dnsp` (fixed) — :877-878, R-113/R-114 reject symbol :885 ✓
- `recommendation` byte-exact `Manual review required — partition agent failed twice` — :881, :889 ✓ (em-dash confirmed)
- `dedup_key` 2-tuple + closed exhaust vocab `{retry-1,retry-2,gap-fill-round-1,gap-fill-round-2,gap-fill-round-3}` — :882, :889 ✓
- `found_n_times` default 1 / +1 within-cycle — :883, :889 ✓
- R-122 Path A/B/C, R-126 strictly-additive + HIGH-non-overridable — :897, :901 ✓
PR-02 §3: two guards, regression>monotonicity precedence (:1270), byte-exact halt strings `[HALT-MONOTONICITY] |F|=<n>` and the regression string (verified :1282, :1261), F-set=post-dedup cardinality (:1289-1292), 4-step ordering (:1294-1303). A builder CAN write a conformance test from this — every field, every reject-symbol, every byte-exact string is present with a current line cite. R03's §1.8 reuse-vs-map boundary (wire contract reused verbatim; cohort machinery MAPPED to Stage-7's 2N unit) is the most valuable piece of depth in the set — it tells the builder exactly what is forkable (nothing) vs re-bindable (`affected_range`/cohort unit).

### LF-4 — Q4 "could author SKILL.md prose + exact emission shapes from research alone": PASS with one MINOR gap
- **P1 block / P5 advisory shapes:** R02 §3 gives the house emission patterns (section-heading-as-literal `## Execution Context` / `## Tier Calibration Advisory`, `**Intended Path:**`, fixed-count bullets, `(per Section N.M)` back-refs, `[████████--] XX%` bars, `TASKLIST_ROOT/...` paths only). R03 §2.1 pins P1's exact 3 sub-fields (References / Source areas / Key constraints) + References-only degradation + no-file:line-in-header (TB-Add-7). Verified the Execution Context contract at task-builder SKILL.md:1066-1071, 1231, 1389.
- **P5 advisory table:** R04 confirms `feedback-log.md` columns (Task ID | Original Tier | Override Tier | Override Reason | Completion Status | Quality Signal | Time Variance) — verified verbatim at SKILL.md:830. The advisory reads these; the no-mutation proof (current-run file emitted empty, advisory necessarily reads a *prior* run) is substantive.
- **P4 gate-results line format:** R02 §5 derives the format from the house verdict grammar `<VERDICT> (key=val)` at SKILL.md:725 → recommends `<CHECK-ID>: PASS|FAIL` lines + `GATE: PASS (20/20)` aggregate. This is *derived convention*, explicitly flagged as "form only; R03/R05 own the contract."
- **MINOR gap (the one shape NOT pinned to a literal):** there is no single canonical literal `GATE: PASS` token in the existing skill (R02 §5 states this outright). So the P4 gate-results.txt line format is a *reasoned proposal*, not a copied existing shape. A builder can author it, but two builders could produce slightly different line formats. This is acknowledged honestly by the research (not a blind spot) — hence MINOR, not IMPORTANT.

### LF-5 — Q5 "P2 vs Stage-10.5 disjointness argument substantive": PASS
R03 §4.3 + R04 "Stage-10.5 non-overlap boundary" give a real three-lever proof, not hand-waving:
1. **Different stages** — P2 lives inside Stages 7→9 patch loop; reflect-pre at Stage 10.5 AFTER Stage 10 (fence verified at SKILL.md:1462 "fenced after the Stage 8-10 patch chain").
2. **Different finding source** — P2 consumes QA-gate FAIL-verdict items (`F_n`, dedup-key); reflect-pre consumes spec-coverage gaps / unmapped requirements (UC-1 coverage matrix). Cited sc-reflect SKILL.md:39 + sc-tasklist :1462.
3. **Different remediation ownership** — P2 patches inline via fix-cycle; reflect-pre AUTHORS-but-never-runs a corrective MDTM (sc-reflect :339/:348).
The proof identifies the exact failure mode it precludes ("a finding cannot be in both unless P2 were to re-run a spec-coverage audit — it does not") and gives the builder a guard obligation ("P2 MUST NOT widen its loop to spec-coverage gaps; Stage 10.5 MUST stay fenced"). Substantive.

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | MINOR | 01 line 17 vs 02 line 10 vs actual | Line-count disagreement: R01 asserts SKILL.md is **1632** lines and instructs "Cite 1632"; R02 cites **1631**. Actual `wc -l` = **1631**. R01's 1632 is off-by-one (likely counted a trailing newline as a line). Anchors are unaffected (R01 cites by interior line number, all verified correct), but the builder should not propagate "1632". | Builder: treat SKILL.md as 1631 lines; ignore R01's "Cite 1632" instruction. No anchor re-derivation needed. |
| 2 | MINOR | P4 emission shape (02 §5; 04 §P4) | The P4 `gate-results.txt` per-line + aggregate format (`GATE: PASS (20/20)`) is a *derived* convention with no single literal existing token to copy — two builders could author slightly divergent line formats. Honestly disclosed by the research, but not yet pinned to one canonical string. | Builder: pick ONE line format and pin it as a literal in the SKILL.md edit (e.g. `CHECK <N> PASS|FAIL: <label>` + `GATE: PASS (k/20)`), so gate-results.txt is itself deterministic. R03/R05 own the binding contract — coordinate. |

No CRITICAL or IMPORTANT depth issues. The research is genuinely deep: every reused contract is field-level, every data flow is producer→consumer traced, every attachment point is a verbatim line anchor that I independently confirmed against current source, and the disjointness argument is a real proof. The adversarial prior (surface-level inventory) is rebutted by the evidence.

---

## Self-Audit

**(a) Reliance — structural items I did NOT re-check (rf-qa's domain):** section-number existence, cross-reference well-formedness, and template conformance of the research files themselves were not re-verified — those are structural QA's job, not the research-depth lens.

**(b) Independent semantic checks (≥1 required):**
- Re-read SKILL.md:700-714 and :820-844 → independently confirmed P1's anchor (after Feedback Log row :707, before Phase Files Table :709) and P5's anchor (after Feedback Collection Template :839, before Glossary :841) are real and correctly described. (tool: Read)
- Re-read task-builder SKILL.md:878-911 → independently confirmed all 8 DM-003 fields + reject symbols match R03's field table byte-for-byte, incl. the em-dash `recommendation` literal. (tool: Bash grep + Read)
- Re-read SKILL.md:1244-1310 → independently confirmed Stage 7 split/2N/merge/retry behavior matches R01+R04 descriptions; confirmed :1310 retry clause is binary (validating P3's "must split some-vs-zero" gap). (tool: Read)
- Ran `wc -l` → caught the 1632-vs-1631 discrepancy R01 introduced (Issue #1). (tool: Bash)

Confidence: Verified 5/5 lens questions with tool evidence | Unverifiable 0 | Unchecked 0 | Confidence 100%.

---

## VERDICT: FAIL

The research is DEEP ENOUGH on all five lens questions (LF-1..LF-5 all PASS) — a builder could author the per-proposal SKILL.md prose edits and exact emission shapes from this research without re-reading source, with the single exception of the P4 line format which needs a builder-pinned literal. However, per the rf-qa-qualitative verdict rule, **ANY issue of any severity = FAIL**. Two MINOR issues remain (line-count drift; unpinned P4 gate-results format). Both are MINOR and quickly resolved; neither indicates superficial research.

**Resolution to reach PASS:** (1) Builder ignores R01's "Cite 1632" and uses 1631. (2) Builder pins one canonical gate-results.txt line format as a literal in the P4 edit. After these, research-depth is PASS-eligible.
