# QA Report — Phase 4 Dispatch Prose (Qualitative / Operational Coherence)

**Topic:** TASK-RF-20260603-032936 — sc-recommend hot/cold-path dispatch under Option P
**Date:** 2026-06-03
**Phase:** doc-qualitative (Phase-4 dispatch-prose coherence; adapted)
**Fix cycle:** N/A (first pass)
**Boundary:** Option P (Python-heavy / thin Haiku) — `boundary-resolved.md`

---

## Overall Verdict: PASS

The Phase 4 dispatch prose in `SKILL.md` is coherent, faithful to the resolved Option-P
boundary, and free of contradictions with the Phase 0–3 body and the actual CLI code.
One MINOR clarity gap (telemetry behavior on the `native` outcome) was found and **fixed
in-place**. Two non-blocking observations are recorded (a plan-artifact miscount and a
sequencing forward-reference) — neither is a `SKILL.md` prose defect.

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Internal consistency: prose claims match `dispatch.py` + `cache put` | PASS | source_hash validation = Read+sha256 compare in `dispatch.py:114-122`; `cache put` discards Haiku hash + recomputes `dispatch`/`commands.py:117-136`; "exactly ONE Haiku classifier" matches `CLASSIFIER_PROMPT` returning only `{classification_key,native_likely,confidence_top2_delta}` (`prompts.py:98-104`). All claims verified true. |
| 2 | No contradiction with Phase 0–3 | PASS | Cold path "is Phase 0–3 inside a 2nd Haiku" matches `COLD_PATH_RUNBOOK` which contains Phase 0 gate + degradation + Phase 1 net-value + Phase 2 hand-off + Phase 3 plugin + R1–R4 (`prompts.py:109-171`). Hand-off (COLD_PATH_RUNBOOK, not full SKILL.md) is coherent and the ~91K rationale is sound. |
| 3 | Option-P faithfulness (no "CLI spawns Agents" lie) | PASS | `SKILL.md:42` explicitly states the CLI cannot spawn Agents and the skill owns all Agent spawns. Both classifier (`:44`) and cold-path (`:187`) spawns use the Agent tool in skill prose. CLI is shelled to for scan/validate/commit only. Round-trip honest. |
| 4 | Flow gaps (trace HIT / MISS→insert / NATIVE) | PASS | All three terminate correctly with exactly-once-or-zero telemetry (trace below). No dead-end, no double-telemetry. |
| 5 | `--eval` triple-coherence (cmd doc ↔ SKILL cold-path ↔ `eval run`) | PASS | Modes `none\|quick\|normal\|deep` agree across `recommend.md:34`, `commands.py:31/EVAL_MODES`, and `eval_run` choices (`commands.py:205`). Opt-in, cold-insert-triggered, skill emits Agent fan-out / CLI grades — consistent with boundary-resolved row. |

## Summary
- Checks passed: 5 / 5
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 1 (MINOR clarity on `native` telemetry)

## Flow Traces (Check 4)

- **Hot HIT:** classify (1 Haiku) → `recommend dispatch` → `outcome:"hit"` → emit
  `recommendation` verbatim + telemetry `--cache-result hit` → DONE. **One** telemetry. ✓
- **Cold MISS→insert:** classify → dispatch → `outcome:"miss"` (one of 4 enum reasons) →
  spawn 2nd Haiku w/ COLD_PATH_RUNBOOK → returns `recommendation + cache_update` →
  `recommend cache put` (CLI recomputes source_hash) → optional `--eval` → emit + telemetry
  `--cache-result cold_inserted`. The hot-path `miss` branch logs **nothing** itself
  (`SKILL.md:55` only "falls through"), so no double-log. **One** telemetry. ✓
- **NATIVE:** classify → dispatch → `outcome:"native"` (`native_likely` OR `native_fallback`
  row) → recommend native per Phase 1 → no cold path, no write, **zero** telemetry. This is
  correct-by-design: `native` has no `cache_result` enum member (`dispatch.py:47-48`,
  `telemetry.py:17-26`), so the appender has nothing valid to log. Terminates. ✓

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | `SKILL.md:54` (native branch) | Prose said "no cold path, no table write" but was silent on telemetry. A reader could not tell whether `native` should log a telemetry event. Code makes native un-loggable (no enum member), but the prose did not say so. | FIXED: appended "and no telemetry event (native is not a cache-table event — it has no `cache_result` enum member, so the appender has nothing valid to log)." |

## Actions Taken
- Fixed issue #1 in `src/superclaude/skills/sc-recommend/SKILL.md` (native outcome branch)
  by making the zero-telemetry behavior explicit, matching `dispatch.py:47-48` +
  `telemetry.py:17-26` exactly.
- Verified the fix is consistent with the closed 6-value `CACHE_RESULTS` enum (no `native`
  member) and with `DispatchResult.cache_result=None` on native.
- Edit applied to the `src/` source-of-truth side only. `make sync-dev` is Phase 6's
  explicit job (task line 345-347); not run here (out of qualitative-QA scope).

## Non-Blocking Observations (NOT prose defects)

1. **`recommend` CLI group not yet registered in `main.py`.** Empirically confirmed:
   `uv run superclaude recommend dispatch ...` → `Error: No such command 'recommend'`.
   `recommend_group` is absent from `main.py:402-426`. **This is expected per the plan, not
   a defect:** task Phase 6 Step 6.1 (line 347-349, currently unchecked `[ ]`) registers the
   group, and the task explicitly states registration is required "regardless of which option
   ships the dispatch logic" (line 345). Phase 4 (prose) legitimately runs before Phase 6
   (wiring). The SKILL.md prose correctly forward-references the post-Phase-6 invocation form
   `superclaude recommend dispatch`, which matches the planned `name="recommend"` registration.
   All four shelled commands (`dispatch`, `cache put`, `telemetry append`, `eval run`) are
   flag-faithful to the Click definitions in `commands.py`. **No SKILL.md change warranted.**

2. **`boundary-resolved.md:44` says "All 5 miss reasons"; code + prose use 4.** The CLI emits
   **4** miss reasons (`miss_no_key`, `miss_low_confidence`, `miss_validation_stale`,
   `miss_budget_exceeded` — `dispatch.py` + `telemetry.py:17-26`) plus 2 `native` paths
   (`native_likely`, `native_fallback`). `SKILL.md:55` and `:185` correctly list **4**. The
   "5" in the plan artifact appears to fold the `native_likely` exit into a "miss-like"
   count. The **shipped prose is correct**; the discrepancy is in the planning artifact, not
   in `SKILL.md`. Flagged for the plan author; no prose fix.

## Self-Audit

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- No `## Inherited Structural Verdict` was provided in the spawn prompt — ran standalone.
  Did NOT rely on any structural PASS; verified prose-vs-code independently.

**(b) Independent semantic checks (≥1 required, INV-019):**
- Source_hash ownership claim — verified by Read of `dispatch.py:114-122` and
  `commands.py:117-136` (CLI does Read+sha256, discards Haiku hash) — not a structural check.
- Telemetry-once invariant across 3 flows — verified by Read of `telemetry.py:17-26`
  (closed 6-value enum, no `native`) + `dispatch.py:47-48` (cache_result=None on native) +
  flow trace through `SKILL.md:53-57,197`.
- Dead-command empirical check — ran `uv run superclaude recommend dispatch ...` and
  observed `No such command 'recommend'`, then cross-checked against task Phase 6 plan to
  confirm it is a sequencing artifact, not a defect.

**Confidence:** Verified: 5/5 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 6 | Grep: 4 | Glob: 0 | Bash: 5
(No web research performed — all checks were local-file/code-bound. Tavily not needed.)

## Recommendations
- Proceed to Phase 5/6. Before Phase 6 registration lands, the SKILL.md commands are
  intentionally inert (forward-referenced); Phase 6 Step 6.1 + the CLI-registration test
  (line 357) will make them live. Verify post-registration that `superclaude recommend
  dispatch --help` resolves.
- Optional cleanup (plan hygiene, not blocking): correct `boundary-resolved.md:44`
  "5 miss reasons" → "4 miss reasons (+2 native paths)" to match the shipped code/prose.

## QA Complete
