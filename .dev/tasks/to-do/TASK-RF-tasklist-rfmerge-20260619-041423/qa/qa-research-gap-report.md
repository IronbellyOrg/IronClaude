# QA Report — Research Gate (Partition A of 2)

**Topic:** RigorFlow Merger tasklist — SOURCE/CONTRACT side research
**Date:** 2026-06-19
**Phase:** research-gate
**Lens:** gap-detection (GAPS the researchers missed for the SOURCE/CONTRACT side)
**Fix cycle:** N/A
**Fix authorization:** false (report-only)

**Assigned files (partition A):**
- 01-skill-stage-map.md
- 02-skill-conventions.md
- 03-integration-contracts.md
- 04-proposal-attachment-trace.md

[PARTITION NOTE: Cross-file checks (contradictions, scope coverage, cross-references) limited to assigned subset. Full cross-file verification requires merging all partition reports. Files 05/06/07 are out of this partition's scope.]

---

## Overall Verdict: FAIL

FAIL is driven by **gaps the research left for the SOURCE/CONTRACT side**, not by inaccuracy. The
four assigned files are unusually well-evidenced and almost every cited anchor was independently
re-verified against current source (see Items Reviewed). However, the research-gate rule is
zero-tolerance: **any gap of any severity = FAIL**, and this partition found one CRITICAL and several
IMPORTANT/MINOR gaps the implementing tasklist could trip on. None are fatal to the research effort;
all are remediable with bounded follow-ups.

---

## Confidence

**Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
(All 10 research-gate checks were applied to the 4 assigned files with tool evidence. "Confidence
100%" refers to the QA *checks being performed*, NOT to the work passing — the work FAILs on gaps.)

**Tool engagement:** Read: 6 | Grep: 0 | Glob: 0 | Bash: 4 (each Bash batched multiple grep/sed
verifications against current source). No web research performed (all claims are intrinsically
local source-of-truth; Tavily not required). tavily_search: 0 | tavily_extract: 0 |
web_search_fallback: 0 | web_fetch_fallback: 0.

Tool-call count (16 discrete verifications across 10 batched calls) ≥ 10 checklist items — engagement
minimum satisfied.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | File inventory / completeness | PASS | All 4 assigned files carry `**Status:** Complete` + a Summary/closing section (01 §E + "Status: Complete" :237; 02 §7; 03 §7; 04 "Per-proposal anchor summary"). |
| 2 | Evidence density | PASS (Dense, >80%) | Spot-verified ~15 anchors against current source, all matched: sc-tasklist :1456 (no-loop), :1462 (Stage 10.5 fence), :1310 (retry), :1288-1295 (merge), :1187 (20-check), :1597 (17 stray), :49/:57 (input-contract), :1409-1427 (sc:task), :894-927 (P1 body), :86 (feedback-log), :212 (4.1c resolve/None), :1407 (validation mkdir), :1316 (short-circuit), :1487 (no-inference); task-builder :873-911 (DM-003), :1066/:1231/:1389 (Exec Ctx + TB-Add-7), :1261/:1290 (PR-02). |
| 3 | Scope coverage (assigned subset) | PASS | P1→Stage4, P5→Stage4/index, P4→Stage6+7, P3→Stage7, P2→Stage9/10, plus sc:task delegate, Stage-10.5 boundary, Sprint parser, PR-02, Exec-Context reuse all examined. [PARTITION NOTE: tests (05) + template (06) + citation-crossval (07) are out of this partition.] |
| 4 | Documentation cross-validation tags | PASS | No doc-only architecture claims; all are code-cited. 02 §6 correctly tags RULES.md sync/UV/lint as **Unverified** and defers to CLAUDE.md; 03 marks zero "Unverified" and every field carries a re-verified file:line. |
| 5 | Contradiction resolution | **FAIL** | **R01 vs R02 line-count contradiction**: 01:17 asserts SKILL.md is 1632 lines ("Cite 1632, not 1631"); 02:10 cites 1631. `wc -l` = **1631** (file ends with trailing newline). R01 is wrong; R02 is right. Unresolved within the research set. See I-1. |
| 6 | Gap severity (all gaps = FAIL) | **FAIL** | Gaps present (see Issues Found): G-A (CRITICAL), plus IMPORTANT/MINOR. Research-gate is zero-tolerance. |
| 7 | Depth appropriateness (Deep) | PASS | 04 traces the full 11-stage data flow end-to-end (Stage4 enrich → Stage6 self-check → Stage7 2N merge → Stage8/9/10 patch → Stage10.5) with per-proposal in/out shapes. Deep-tier end-to-end requirement met. |
| 8 | Integration point coverage | PASS | 03 is a dedicated integration-contract map (DM-003, PR-02, Exec-Context, Stage-10.5 reflect boundary, sc:task delegate, Sprint parser). Cross-subsystem connection points documented with reuse-vs-fork HALT conditions. |
| 9 | Pattern documentation | PASS | 02 documents heading conventions, determinism phrasing, emission shapes, the 20-check sub-gate structure, SoT/sync/UV/lint mechanics. |
| 10 | Incremental-writing compliance | PASS | Files show cross-researcher boundary notes (01 §F, 02 implementer notes, 03/04 "owned by Rnn" flags) and iterative anchor refinement — consistent with incremental authoring, not one-shot. |

**Summary**
- Checks passed: 8 / 10
- Checks failed: 2 (Contradiction resolution; Gap severity)
- Critical issues: 1
- Issues fixed in-place: 0 (fix_authorization: false — report-only)

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| I-1 | **IMPORTANT** | 01:17 vs 02:10 | Line-count contradiction: R01 says SKILL.md = **1632** and instructs "Cite 1632"; R02 says **1631**. Verified `wc -l` = **1631** (trailing newline present). R01 mis-counted the Read-tool "1632 total" display. A builder citing 1632 per R01's instruction will cite a non-existent last line. | Correct 01:17 to 1631; the authoritative count is `wc -l` = 1631. (R02 is already correct.) |
| I-2 (G-A) | **CRITICAL** | 03 §1.8 + 04 §P3 (P3 reuse boundary) | **P3 reuse boundary is under-specified for the lens question "what exactly maps from task-builder partition-cohort to the Stage-7 2N fan-out."** 03 §1.8 correctly says the per-agent wire/merge contract reuses verbatim while `affected_range`/cohort/R-122-path "MAP" to Stage-7's unit — but it does NOT pin (a) what the Stage-7 **`escalation_ladder_exhaust_point`** value is, given Stage-7's ladder is "retry once" (:1310), NOT the partition agent's `WebSearch→/rf:opinion→team-lead` ladder. The closed vocab `{retry-1, retry-2, gap-fill-round-1..3}` is partition-cohort-specific; Stage-7 has only a single retry. Reusing the vocab verbatim (a HALT-condition if forked) is impossible without a mapping rule, yet emitting an out-of-vocab value triggers `API-003-exhaust-point-vocabulary-violation`. This is an unresolved contract collision the builder will hit. | Add an explicit Stage-7→DM-003 dedup-key mapping: which closed-vocab token Stage-7's single-retry-exhaust maps to (likely `retry-1`), and what the Stage-7 cohort unit / `assigned_files_range` analogue is (phase-file task split range). Without it, P3 cannot conform to the no-fork DM-003 contract. |
| I-3 | **IMPORTANT** | 04 §P2 / 03 §3.4-3.6 (P2 NON-OVERLAP proof obligation actionability) | **The Stage-10.5 NON-OVERLAP proof is argued but not made into a writable disjointness test.** 03 §4.3 + 04 "fence" give a sound *argument* (different stages, different finding-source, different remediation ownership) but neither defines the **observable predicate** a disjointness test would assert (e.g., "for every finding f remediated in the P2 loop, f.stage ∈ {7,9} and f ∉ reflect-pre gap-registry"). The spec demands a "non-overlap argument/test" (FR-RFMERGE.2; NFR-RFMERGE.2 "zero double-remediation"); the research stops at the argument. | Specify the disjointness *predicate* + where each finding-set is observable (P2 F_n from ValidationReport.md verification table; reflect-pre gaps from `validation/reflect-pre/phase-<P>/`), so the builder can author a concrete assertion rather than re-derive it. |
| I-4 | **IMPORTANT** | 04 §P1 emit-iff rule | **P1 determinism emission rule ("emit iff ≥1 roadmap ref resolves; no invented paths") lacks a concrete, single emission rule.** 04 §P1 surfaces the real problem (the generator has NO roadmap-ref scanner today; the only resolvable ref is the TASKLIST_ROOT token + resolved tdd/prd) and offers options (a)/(b) but recommends (a) without the research *committing* to the deterministic rule. The spec's AC ("emitted iff ≥1 roadmap ref resolves") is therefore not yet backed by a single concrete rule — option (b) would need a regex that no file defines. | Commit to option (a): define "roadmap ref resolves" = the 4.1c non-None set {TASKLIST_ROOT token, resolved tdd_file, resolved prd_file, component_inventory.new}. State it as the one deterministic rule so the builder does not re-open the design. |
| I-5 | **MINOR** | 03 §1 header "8 fields"/04, vs source | **DM-003 field-count framing drift.** 03 §1.1 titles "The 8-field emission record" then §1.49 clarifies it is **7 named YAML fields** (dedup_key being a 2-tuple). The header "8" risks a builder asserting 8 top-level fields. Source (:877-883) is 7 named fields. | Lead with "7 named fields (dedup_key is a 2-tuple)"; demote the "8" to the parenthetical. (03 already half-corrects this at §1.49 — make the header match.) |
| I-6 | **MINOR** | Mirror-sync coverage (lens Q5) | **Mirror-sync implications partially covered, one gap.** 02 §6 covers `make sync-dev`/`verify-sync`/SoT well; 01 flags `phase-template.md` + `rules/tier-classification.md` + `rules/file-emission-rules.md` mirror-lag. But **no file states which `rules/*.md` must be re-synced when the P3/P4 Stage-6/7 SKILL.md prose changes** (file-emission-rules.md governs emission; P4 adds a `validation/gate-results.txt` emission — does the rule mirror need updating?). The interplay "P4 emits gate-results.txt at Stage 6" vs the write-atomicity rule at :1195 (all output validated before any Write) is noted by 04 (:1195 ref) but not resolved: gate-results.txt is written at Stage 6 *after* the gate passes — is that consistent with "no Write before all checks pass"? | Add a one-line note: gate-results.txt is emitted *after* checks 1-20 pass (so it does not violate :1195 write-atomicity), and state whether `rules/file-emission-rules.md` must gain a gate-results.txt row on sync. |
| I-7 | **MINOR** | Lens Q6 (Stage-6 emit affecting write-atomicity :1195) | **The specific integration risk "does emitting gate-results.txt at Stage 6 affect the write-atomicity rule at :1195?" is not directly answered.** 04 cites :1195 and :1134 ("Invalid output is never written") but does not close the loop on whether a *new* Stage-6 disk write is exempt from the atomicity rule (the rule targets the tasklist bundle; gate-results.txt is evidence, not bundle). | State explicitly that :1195 atomicity governs the *tasklist bundle*, and gate-results.txt (evidence artifact, post-gate) is outside that set — or flag it as a builder decision if ambiguous. |

---

## Lens Questions — Direct Answers

1. **Every FR-RFMERGE.1-.7 has an attachment point?** YES for .1 (Stage4 :894-927/index), .3 (Stage7 merge :1288/:1310), .4 (Stage6 :1187 + Stage7 :1267), .2 (Stage10 :1456→Stage9 :1413), .5 (index after :839). .6/.7 are doc-accuracy/quarantine reqs with no code attachment needed. **No FR lacks an attachment point.** PASS.
2. **P2 Stage-10.5 NON-OVERLAP actionable as a disjointness test?** PARTIAL → see I-3. Argument is sound; the *writable predicate* is missing.
3. **P3 reuse boundary clear (partition-cohort → 2N fan-out)?** PARTIAL → see I-2 (CRITICAL). The wire contract is clear; the dedup-key `escalation_ladder_exhaust_point` vocab mapping for Stage-7's single-retry ladder is NOT.
4. **P1 determinism emission rule backed by a concrete rule?** PARTIAL → see I-4. Options surfaced; not committed.
5. **Mirror-sync implications covered?** MOSTLY → see I-6. sync mechanics solid; one `rules/*.md` re-sync question open.
6. **Stage-6 gate-results.txt vs write-atomicity :1195?** PARTIAL → see I-7.

---

## Recommendations (before synthesis)

- Resolve I-2 (CRITICAL) first: pin the Stage-7 dedup-key vocab mapping so P3 can conform to the
  no-fork DM-003 contract. This is the only gap that could force a contract-fork HALT downstream.
- Resolve I-1, I-3, I-4 (IMPORTANT): correct the line count; make the P2 disjointness predicate
  writable; commit P1's deterministic emission rule to option (a).
- Resolve I-5, I-6, I-7 (MINOR) for internal consistency.
- These can be addressed by a bounded gap-fill on files 01/03/04; no re-research needed.

[PARTITION NOTE: This verdict covers partition A (files 01-04) only. Cross-file checks were limited
to the assigned subset. The orchestrator must merge with partition B (files 05-07) before the final
research-gate verdict; take the more severe rating on any shared item.]

---

## VERDICT: FAIL

Severity-rated issues: 1 CRITICAL (I-2 / G-A — P3 dedup-key vocab mapping for Stage-7), 3 IMPORTANT
(I-1 line count, I-3 P2 disjointness predicate, I-4 P1 emission rule), 3 MINOR (I-5 field-count
framing, I-6 rules/* re-sync, I-7 write-atomicity scoping). Research is high-quality and accurate;
FAIL is on zero-tolerance gap presence, all remediable via bounded gap-fill.

## QA Complete
