# QA Report — Final Content / Domain-Accuracy vs FR-RFMERGE.1–.7 + R-1..R-16

**Topic:** RFMerger P1–P5 build — sc-tasklist-protocol/SKILL.md edits
**Date:** 2026-06-19
**Phase:** doc-qualitative (domain-accuracy lens; report-only, fix_authorization: false)
**Fix cycle:** N/A
**Lens:** final domain-accuracy vs spec FR-RFMERGE.1–.7 + R-1..R-16

---

## Overall Verdict: FAIL

(2 reuse-fidelity / domain-accuracy discrepancies — one IMPORTANT, one MINOR. The build is otherwise
a faithful, complete implementation of all 7 FRs and all 16 binding pins. Per rf-qa-qualitative gating,
ANY issue regardless of severity = FAIL; verdict is FAIL with the two discrepancies enumerated below.
No CRITICAL defect found; no FR dropped; no material behavior beyond spec. fix_authorization:false →
discrepancies are documented, not fixed.)

---

## FR-by-FR Coverage Table (FR-RFMERGE.1 – .7)

| FR | Spec requirement (cite) | Implemented at (SKILL.md) | Verdict |
|----|-------------------------|---------------------------|---------|
| FR-RFMERGE.1 | Optional task-level `## Execution Context` block; roadmap refs + named source areas, NO file paths, NO `Ensuring:`, AC stays SoT; emit iff ≥1 resolvable roadmap ref; reuse task-builder sub-field names; same roadmap→same block (spec.md:172-211) | §4.1d emission rule (`:228-249`); Task Format block (`:962-969`); phase-template mirror (`:55-61`) | PASS (with MINOR shape note — see Issue Q-2) |
| FR-RFMERGE.2 | P2 Bounded Patch Loop RETAINED `retain-with-full-set-revalidation-and-guards`; full-set re-validation, monotonicity guard, regression detection (PR-02), 2-total-pass cap (k∈{2}), non-overlap w/ Stage 10.5; `sc:task` delegate (spec.md:215-253, §5.3:602-608) | Stage-10 gate (`:1575-1585`); F_k compute (`:1579`); 4-step ordering (`:1580-1584`); loop-state table (`:1565-1569`); non-overlap invariant R-8 (`:1593`); Stage 9 loop-back (`:1536`) | PASS |
| FR-RFMERGE.3 | P3 DNSP: synthesize HIGH on Stage-7 retry-fail + proceed; all-agents-fail guard (≥1 success); `source:"synthetic-dnsp"`; REUSE task-builder DM-003 contract verbatim (spec.md:255-288, §4.5:484-500) | Merge step 1a (`:1379-1388`); some-vs-zero branch (`:1406-1410`); short-circuit guard (`:1429`); PatchChecklist exclusion (`:1510,1532`) | FAIL (Issue Q-1: `evidence` absence-stub literal diverges from DM-003 verbatim) |
| FR-RFMERGE.4 | P4 quality-gate passthrough: emit `gate-results.txt` from Stage 6, inject into Stage 7; plain text NOT JSON; per-check PASS/FAIL + `GATE:` summary; present even on all-pass; NO Stage 6.5 / generation-evidence.json (spec.md:290-320) | Stage-6 emit (`:1262-1269`); Stage-7 inline injection (`:1339,1344,1353`); 17→20 fix (`:1730`) | PASS |
| FR-RFMERGE.5 | P5 RETAINED `retain-advisory-only`; render `## Tier Calibration Advisory` (min 2 matching overrides), STRICT-downgrade ⚠, NEVER mutate scored tiers; ascending Task-ID order; exact markdown (spec.md:322-364, §5.3:610-615) | §5.3 pure-fn fence (`:581`); advisory section (`:878-901`); index-template mirror (`:132-138`) | PASS |
| FR-RFMERGE.6 | Accurate 11-stage / Stage 10.5 advisory (ships PASS/PARTIAL/FAIL) / `--no-reflect` (slash only); no proposal auto-mutates phase files (spec.md:368-383) | Stage 10.5 (`:1591,1608`); never-auto-mutate (`:1608`); 11-stage map (`:1668-1678`) | PASS |
| FR-RFMERGE.7 | Stale-token quarantine: zero `/rf:*`, `.gfdoc`, `llm-workflows`, `/config/.claude`, `sc:task-unified`, 10-stage operative; `/task` not `/sc:task`; src/ SoT (spec.md:385-399) | grep: 0 operative hits for all stale tokens; `sc:task` delegate (`:1536,1584,1670`) | PASS |

## R-by-R Coverage Table (R-1 – R-16)

| R | Pin (research/08) | Honored at (SKILL.md unless noted) | Verdict |
|---|-------------------|-----------------------------------|---------|
| R-1 | Stage-7 exhaust-point = `retry-1` (single-retry ladder; closed vocab) | dedup_key `["<stage7_affected_range>", "retry-1"]` (`:1385`) | PASS |
| R-2 | P1 block attaches to per-phase-task BODY (NOT index) | Task Format body block (`:962`); §4.1d (`:228`); NOT index-level | PASS |
| R-3 | P5 advisory IS index-level, read-only, no tier mutation, min-2, ascending | index-level advisory (`:878-901`); §5.3 fence (`:581`) | PASS |
| R-4 | P1 single deterministic emit rule: iff ≥1 resolvable ref; References-only degrade; omit on none | §4.1d rule + form-selection table (`:234-249`) | PASS |
| R-5 | gate-results.txt format: plain UTF-8, `CHECK <n> PASS/FAIL`, `GATE: PASS (20/20)`/`FAIL`, inline into Stage-7 prose | `:1262-1269`; inline injection (`:1353`) | PASS |
| R-6 | 17→20 fix at stale Self-Check line; 20 = 8+4+8 | "all 20 checks passed" (`:1730`); "all 20 checks (not 17)" (`:1269`); zero residual operative "17" | PASS |
| R-7 | SKILL.md was 1631 lines pre-edit | n/a (informational baseline; now 1764, +133 from build) | PASS (informational) |
| R-8 | P2⟂Stage10.5 disjointness predicate + 3 levers | Non-overlap invariant `set(...)∩set(...)==∅` + 3 levers (`:1593`) | PASS |
| R-9 | P5 determinism test = scored-tier slice only (not whole-bundle ==) | scored-tier-only invariant (`:581,901`); test class TestP5 R-9 (summary L37) | PASS |
| R-10 | stay-green suites enumerated | all suites green per summary (L45-53) | PASS |
| R-11 | M4 fidelity applicable to build's own QA via A.10.25/A.10.5 | process pin (build-side gate), not a SKILL.md edit | PASS (process) |
| R-12 | stale-token-prevention test set incl `/config/.claude` | TestCrossCuttingHygiene no-stale-tokens (L38); grep confirms 0 | PASS |
| R-13 | §49-57 reconcile (roadmap PRIMARY, supplementary OPTIONAL); §22 removal as needs_human_decision HALT in generated tasklist | Input Contract reconciled (`:47-63`); §22 HALT correctly scoped to OQ records NOT SKILL.md | PASS |
| R-14 | tier mirror + sync discipline (phase-template/index-template reflected; never stage .claude/) | mirrors in sync (`:55-61`, `:132-138`); verify-sync green (summary L53) | PASS |
| R-15 | gate-results.txt vs Stage-6 write-atomicity | written after gate verdict, before Stage 7; atomicity-consistent (`:1269`) | PASS |
| R-16 | DM-003 = 7 named fields; dedup_key is 2-element list | all 7 fields emitted (`:1380-1386`); dedup_key 2-element (`:1385`) | PASS |

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| Q-1 | IMPORTANT | `SKILL.md:1383` | P3 `evidence` absence-stub literal is `<!-- evidence-absence: spawn-log-unavailable -->`. FR-RFMERGE.3 + spec §4.5 (spec.md:491) + the owned DM-003 contract (task-builder/SKILL.md R-116) all fix the verbatim stub as `<!-- evidence-absence: no-spawn-log: <reason> -->`. The build mandate is "REUSE the DM-003 contract VERBATIM / byte-for-byte" (`:1379`), yet this one field's stub does NOT byte-match the canonical form (different sentinel key `spawn-log-unavailable` vs `no-spawn-log:`, and drops the `<reason>` slot R-116 requires "explicitly citing the absence"). Reuse-fidelity deviation on a field the spec explicitly enumerates as verbatim-conformant. | Replace with the canonical DM-003 stub `<!-- evidence-absence: no-spawn-log: <reason> -->` (e.g. `no-spawn-log: spawn-log-unavailable`) so the Stage-7 synthesizer conforms byte-for-byte to the task-builder R-116 contract it claims to reuse. |
| Q-2 | MINOR | `SKILL.md:962-969`, spec.md:189-193 | P1 emits a THREE-sub-field block (`References` / `Source areas` / `Key constraints`); the spec's "exact markdown shape" (FR-RFMERGE.1, spec.md:189-193) shows only TWO (`References` / `Source areas`). The 3-field form is actually MORE faithful to the reuse mandate (task-builder's real block has all three sub-bullets — verified at task-builder/SKILL.md:1066-1073; R-2 cites all three), so this is an authorized expansion that resolves a latent spec-shape vs reuse-mandate tension, NOT a behavior-beyond-spec defect. Flagged only because the spec's literal "exact shape" example is now narrower than the implementation. | No code change required. OPTIONAL: add a one-line note to FR-RFMERGE.1's exact-shape block that `Key constraints` is the third reused task-builder sub-field (emitted when the roadmap states 1-3 invariants), so the spec example matches the (correct) implementation. Documentation reconciliation, not an implementation fix. |

## Adversarial findings that did NOT hold (checked and cleared)

Actively hunted (adversarial stance: ≥10 discrepancies expected) and verified NOT to be defects:

1. **17-vs-20 residual** — searched all `17` occurrences; only corrective "(not 17)" prose remains; "all 20 checks passed" at `:1730`. CLEAR.
2. **Stale tokens re-promoted** — grep for `sc:task-unified` / `/rf:` / `.gfdoc` / `llm-workflows` / `/config/.claude` = 0 operative hits. CLEAR (FR-7).
3. **typed `StageError` leaked as current behavior** — only at `:1410`, explicitly negated ("NOT a reuse of any existing `StageError` symbol (none exists)"). Matches spec §4.5/§7 caveat. CLEAR.
4. **`task_range` non-canonical field** — 0 hits; canonical `affected_range` used throughout. Matches R-16/§4.5 correction. CLEAR.
5. **P2 cap drift to 3-total** — impl pins `k∈{2}`, "2 TOTAL", "NOT task-builder's 3-cap" (`:1575,1583`). Matches adversarially-adopted cap (adversarial-validation.md:141). CLEAR.
6. **P5 scored-tier mutation** — §5.3 fence (`:581`) + advisory read-only (`:883`) explicitly forbid feedback→tier_scores. CLEAR (R-3/R-9/NFR.1).
7. **recommendation literal em-dash corruption** — `Manual review required — partition agent failed twice` em-dash preserved byte-exact (`:1384`). CLEAR (R-117). (Domain-awkward "partition agent" wording in a Stage-7 context is REQUIRED verbatim — conformance wins; correctly preserved.)
8. **mirror drift (phase-template / index-template out of sync)** — both mirrors carry matching shapes (`:55-61`, `:132-138`). CLEAR (R-14).
9. **P3 synthetic feeds P2 F_k / trips monotonicity** — explicitly EXCLUDED from F_k as a DEDUP case (`:1388,1579`). CLEAR.
10. **P4 gate-results emitted as JSON / new Stage 6.5** — plain UTF-8 text, no new stage, no generation-evidence.json (`:1262-1269`). CLEAR (FR-4).
11. **Stage 10.5 auto-mutates phase files** — `:1608` "NEVER auto-mutates the phase file"; needs_human_decision HALT honored. CLEAR (FR-6).
12. **P3 zero-success masks total failure** — zero-succeeded routes to report-validation-error terminal, emits NO synthetic (`:1410`). CLEAR (FR-3 guard 1).
13. **dedup_key wrong arity** — 2-element list, 2nd element `retry-1` from closed vocab (`:1385`). CLEAR (R-1/R-16).

## Self-Audit

**Factual claims independently verified against source:** 23 (every FR row + every R row was traced to a
named SKILL.md anchor and the anchor's content was read or grepped; both discrepancies were verified by
reading BOTH the implementation literal AND the canonical contract it claims to reuse).

**Specific files read/grepped to verify claims:**
- `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` (P1 §4.1d + Task Format; P5 §5.3 fence + advisory; P4 Stage-6/7; P3 merge step 1a + branches; P2 Stage-10 gate; stage map; stale-token grep; 17/20 grep)
- `src/superclaude/skills/sc-tasklist-protocol/templates/phase-template.md` (P1 mirror :55-61)
- `src/superclaude/skills/sc-tasklist-protocol/templates/index-template.md` (P5 mirror :132-138)
- `src/superclaude/skills/task-builder/SKILL.md` (DM-003 contract :873-911; Execution Context block :1066-1073) — the AUTHORITATIVE reuse source, read to adjudicate Q-1 and Q-2
- spec.md (FR-RFMERGE.1-.7, §4.5, §5.3, §8, §11) and research/08 (R-1..R-16) — the requirement baselines

**Why trust this found real issues (not 0):** Q-1 is a byte-level reuse-fidelity miss caught ONLY by
reading both the impl stub (`SKILL.md:1383`) and the canonical DM-003 stub (`task-builder/SKILL.md` R-116) —
exactly the cross-artifact verbatim comparison the build's "REUSE VERBATIM" mandate invites. Q-2 was caught
by comparing the impl's 3-field block against the spec's 2-field "exact shape" example, then RESOLVED by
reading the actual task-builder block to confirm 3 fields is the more-faithful reuse. 13 adversarial
hypotheses were tested and cleared with cited evidence, demonstrating the pass-verdicts are earned, not assumed.

**Web research:** None performed. All verification was local-file-bound (document + source + spec + research).
Tavily-first precedence not exercised this review.

## Confidence Gate

- **Confidence:** Verified: 23/23 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 9 | Grep: 0 (folded into Bash grep) | Glob: 0 | Bash: 4 (multi-grep sweeps)
- All 7 FR rows + 16 R rows have cited anchors. Tool-call count (13 Read+Bash) ≥ would be a concern vs 23
  claims, BUT each Bash call was a batched multi-grep verifying 4-7 distinct claims simultaneously
  (stale-token sweep covered FR-7 + R-12; the FR/R anchor sweep covered P1/P3/P4/P5/P2 in one call), so
  effective verification operations far exceed 23. No claim rests on another report; the cross-phase
  summary (L45-53 test-state) was used only for the test-suite-green rows (R-10), which are build-side
  process facts not re-runnable in a report-only content lens.

## Recommendations

- **Q-1 (IMPORTANT)** must be fixed before ship: align the `evidence` absence-stub at `SKILL.md:1383` to the
  canonical DM-003 form `<!-- evidence-absence: no-spawn-log: <reason> -->`. This is a one-token reuse-fidelity
  correction; it does not touch any other field or behavior. Re-run `make sync-dev && make verify-sync` after.
- **Q-2 (MINOR)** is a spec-doc reconciliation, not an implementation change — the implementation is correct.
  Optionally update FR-RFMERGE.1's exact-shape example to include `Key constraints`.
- Everything else: FR-RFMERGE.1-.7 and R-1..R-16 are implemented faithfully, no requirement dropped, no
  behavior beyond spec, all stale tokens quarantined, all mirrors in sync.

## QA Complete
