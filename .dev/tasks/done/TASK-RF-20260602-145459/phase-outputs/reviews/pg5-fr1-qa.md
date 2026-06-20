# QA Report — Phase Gate PG-5 (task-integrity / FR-RV3-MED.1 `type_hierarchy`)

**Topic:** FR-RV3-MED.1 — `type_hierarchy` transitive family coverage (ships LAST)
**Task:** TASK-RF-20260602-145459
**Date:** 2026-06-03
**Phase:** task-integrity (Phase Gate PG-5)
**Fix cycle:** N/A (first pass; 1 fix applied in-place under fix_authorization:true)
**Driving spec:** `.dev/releases/current/Reflect-V3.5-Serena_Mediums/05-spec-medium-complexity.md` (FR-RV3-MED.1, FR-1.1–FR-1.6, Backend gating §FR-1)

---

## Overall Verdict: PASS (with 1 pre-existing consistency defect found and FIXED in-place)

Adversarial stance held: I assumed FR-1 was wrong and hunted. FR-1's own wiring is correct and
complete against all six acceptance criteria. I did, however, find one stale-version defect the
phase5-verify.md report explicitly (and inaccurately) claimed was absent — see Issue #1. It was
pre-existing (committed at `fc044837`, the low-spec work), not introduced by FR-1, but it is a live
internal-consistency defect in an in-scope skill ref file, so I fixed it.

---

## Items Reviewed

| # | Check (prompt item) | Result | Evidence |
|---|---------------------|--------|----------|
| 1 | OQ-M3 probe records backend=`lsp`, no generic type_hierarchy → `--with-hierarchy` default-OFF on lsp | PASS | Read `phase-outputs/plans/oqm3-probe-result.md`: "Backend: `lsp`", "Generic `type_hierarchy` tool: NOT exposed", gating decision "`--with-hierarchy` defaults OFF on `lsp` … unavailable on `none`". Merge-precondition SATISFIED. |
| 2 | Frontmatter `allowed-tools` (line 5) has ALL FOUR medium tools, single-line, no token lost | PASS | Read SKILL.md:5. Single line contains `mcp__serena__execute_shell_command, mcp__serena__onboarding, mcp__serena__prepare_for_new_conversation, mcp__serena__type_hierarchy` plus the full prior tool set. No truncation; 38-tool list intact. Mirror also has them (grep -c type_hierarchy .claude mirror = 8). |
| 3 | §3 declares `--with-hierarchy` (opt-in default OFF; OFF on lsp; unavailable on none; backend-gated) | PASS | SKILL.md:81 — "opt-in (default OFF) … **default OFF on `lsp` backends** … **unavailable on `none`**; only a hierarchy-capable (`jetbrains`) backend runs it." |
| 4 | §6.1 chain: step 4.5 between step 4 and 5; step 5.5 (FR-4) STILL present; order 4,4.5,5,5.5,6; gating prose (FR-1.1/1.4/1.5; skip-no-degrade vs error-degrade explicit) | PASS | SKILL.md:454-458 — `4. find_referencing_symbols` → `4.5. type_hierarchy(hierarchy_type=both\|subtypes, depth=0)` → `5. get_diagnostics_for_file` → `5.5. execute_shell_command` → `6. Re-Read`. Step 5.5 (FR-4) intact. Prose SKILL.md:471: runs only when backend-capable AND --with-hierarchy AND symbol-is-type (FR-1.1); `none`/`lsp-disabled` → skip, `type_hierarchy_invoked:false`, **NO degrade** (FR-1.4); explicit backend error → `degraded:["type_hierarchy:backend_error"]` + find_implementations/find_referencing_symbols fallback (FR-1.5). Skip-no-degrade vs error-degrade distinction is explicit. |
| 5 | §4.1 Wave 1B.3 sub-step 3a (`type_hierarchy(subtypes)` lineage-confirm; HIGH only after genuine lineage, FR-1.6; same gate; no broken renumber) | PASS | SKILL.md:311 sub-step `3a.` inserted between numbered steps 3 and 4 as a decimal sub-step — existing items (1,1a,2,3,4,5) NOT renumbered, no broken refs. "HIGH-severity interaction edge is raised … ONLY after this lineage confirmation" (not name collision = FR-1.6). Same backend + --with-hierarchy gate; skip-no-degrade fallback to step-3 find_referencing_symbols. |
| 6 | §9.1 UC-1 carries `hierarchy_slice_path` + `hierarchy_coverage_pct` (=registered/total, null-safe); §9.2 has 4 telemetry fields; no contract bump (still 1.2.0); no field crosses §9.1/§9.2; medium fields distinct from low-spec FR-1 `implementation_coverage_pct`/`missing_implementations` | PASS | SKILL.md:660-661 under `# UC-1 specific`: `hierarchy_slice_path` + `hierarchy_coverage_pct` (= registered_subtypes / total_subtypes_in_hierarchy; null when empty/unavailable). §9.2 SKILL.md:807-810: `type_hierarchy_invoked`, `hierarchy_backend: jetbrains\|lsp\|none\|lsp-disabled`, `hierarchy_nodes_examined`, `hierarchy_gaps_found`. Contract `1.2.0` at heading 637/yaml 640/self-check 1715 — no bump. Low-spec FR-1 fields at 655-659 are tagged `# FR-1` (find_implementations) and clearly DISTINCT from the FR-RV3-MED.1 hierarchy fields; no crossover. |
| 7 | rubric + coverage-mapping: FR-1 hierarchy-gap sub-term in S_dev_density (parallel up-weight, null-safe, lockstep, NOT disturbing FR-4 sub-term) | PASS | reflection-rubric.md:120 — "FR-RV3-MED.1 hierarchy-gap weight … up-weights S_dev_density … additive weighting input, not a threshold change; null-safe". coverage-mapping.md:127-135 — "parallel up-weight … NOT a numerator addend … null-safe … mirrors the reflection-rubric.md hierarchy-gap sub-term". FR-4 sub-term (rubric:119 / coverage:117-125, lint/type channel) is separate and undisturbed. In lockstep. |
| 8 | reviewer-spec.md: FR-1 hierarchy-slice grounding-hunk under `## Grounding hunks` (analyzer/architect persona, carries hierarchy-slice.yaml ref); three-section invariant intact; FR-4 entry not disturbed | PASS | reviewer-spec.md:45 — FR-RV3-MED.1 hierarchy-slice hunk under `## Grounding hunks`, "**`analyzer`/`architect`-persona** reviewer", carries `<output>/artifacts/hierarchy-slice.yaml` ref, "NOT a fourth brief section; the 'exactly three sections' invariant is unchanged." FR-4 verification-results hunk (line 43) intact and undisturbed. |
| 9 | `make verify-sync` passes | PASS | Ran independently (zero-trust): "✅ All components in sync." Re-ran after my fix: still clean. |
| 10 | phase5-verify.md accuracy | PARTIAL → corrected | phase5-verify.md is accurate on items 1-8 EXCEPT its claim "no stale `1.1.0`" (line 14 of that report). A stale `contract_version: 1.1.0` existed at `report-template.md:14`. See Issue #1. After my fix the claim is now true. |
| 11 | Staging discipline — no `.claude/` staged; edits in `src/` only; fail-open posture preserved | PASS | `git diff --cached` empty. My only edit is `src/superclaude/skills/sc-reflect-protocol/refs/report-template.md` (1 line) then `make sync-dev`. type_hierarchy wiring is fail-open throughout (SKILL.md:471 "MUST never abort"). |

---

## Summary

- Checks passed: 10 / 11 (item 10 was PARTIAL, corrected to PASS after fix)
- Checks failed: 0 (after fix)
- Critical issues: 0
- Issues fixed in-place: 1 (pre-existing stale contract_version in report-template.md)

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | IMPORTANT | `src/superclaude/skills/sc-reflect-protocol/refs/report-template.md:14` | Stale `contract_version: 1.1.0` in the REPORT.md header template. Line 28 of that file states this field "pins the return-contract version this artifact was generated against", but the authoritative contract in SKILL.md §9.1 (line 640) and the self-check assertion (SKILL.md:1715, `contract_version == "1.2.0"`) are `1.2.0`. Any REPORT.md rendered from this template would advertise a contract version (1.1.0) that disagrees with the actual contract (1.2.0). phase5-verify.md inaccurately claimed "no stale 1.1.0". **Provenance:** committed at `fc044837` (low-spec FR-RV3-LOW work) — PRE-EXISTING, not introduced by FR-1; the medium-complexity phases bumped SKILL.md §9.1 to 1.2.0 but no phase updated this template example. | FIXED: changed `1.1.0` → `1.2.0` to match SKILL.md §9.1, then `make sync-dev` + `make verify-sync`. |

Note on scope: FR-1 itself correctly introduced **no** contract bump (hierarchy contract fields live
in the existing UC-1 block; hierarchy telemetry lives in §9.2). The 1.2.0 baseline was established by
prior medium phases (FR-4/2/3). Issue #1 is a coherence defect in a sibling ref file, orthogonal to
FR-1's correctness, but in-scope for this gate's "verify ALL Phase 5 outputs" + internal-consistency check.

---

## Actions Taken

- Fixed Issue #1: edited `src/superclaude/skills/sc-reflect-protocol/refs/report-template.md` line 14
  `contract_version: 1.1.0` → `contract_version: 1.2.0`.
- Re-synced: `make sync-dev` (✅ Sync complete).
- Verified fix: `make verify-sync` → "✅ All components in sync."; `grep -rn "1\.1\.0" src/.../sc-reflect-protocol/`
  → no matches remain; mirror `.claude/.../report-template.md:14` confirmed `1.2.0`.
- Confirmed no `.claude/` path staged (`git diff --cached` empty); only the `src/` side changed.

---

## Confidence Gate

- **Confidence:** Verified: 11/11 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 6 | Grep: ~14 (via Bash grep -n/-c batches) | Glob: 0 | Bash: 7
- All eleven checklist items were verified with direct tool evidence (file:line citations above).
  No item was marked VERIFIED on the basis of reading phase5-verify.md — every claim was
  independently re-derived from the source files. Tool-engagement count exceeds checklist item count.
- No web research required (all claims are local source-truth; OQ-M3 backend probe is a recorded
  artifact, not a live external lookup).

---

## Recommendations

- None blocking. FR-1 is complete and correct against FR-1.1–FR-1.6 and the backend-gating rule.
- Minor follow-up (non-blocking, already resolved this gate): the low-spec contract bump left
  `report-template.md` stale; future contract bumps should grep ALL `refs/*.md` for `contract_version`
  occurrences (there are exactly 2 in report-template.md — the YAML example at :14 and the prose
  description at :28) so the rendered-artifact header never drifts from §9.1.

## QA Complete

VERDICT: PASS
