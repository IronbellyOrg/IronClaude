# SKILL.md Downstream Consumer Cross-Check Verdict

**Target:** `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` (sole downstream consumer of confidence-calibrator)
**Edited calibrator file:** `src/superclaude/agents/confidence-calibrator.md` (141 lines post-Change-C)
**Calibrator Inputs (post-edit, unchanged from pre-edit):** `card_path`, `rubric_path`, `card_tier`, `flags_context`, `output_path`
**Calibrator Output Format named fields (post-edit):** `Card under calibration`, `Rubric`, `Card tier`, `Timestamp`, `## Per-dimension scores`, `## Stage-2 trace (REQUIRED)` (NEW), `## Confidence` (Self-reported, Calibrated, Formula applied (NEW), Delta), `## Escalation recommendation` (Verdict, Reason, Rubric rule fired), `## Notes`

---

## L199 — Wave 1.7 dispatch invocation

**Verbatim quote (SKILL.md L198–L199):**

> 2. **Calibrate confidence (independently)** — spawn the `confidence-calibrator` agent via `Task` with `card_path=<output-dir>/tier1-hypothesis.md`, `rubric_path=<skill-dir>/refs/escalation-rubric.md`, `card_tier=1`, `flags_context=<wave 0 parsed flags>`, `output_path=<output-dir>/tier1-calibration.md`. The agent re-grades the hypothesis card against the 5-dimension rubric without the formation context (anchoring is reduced, not eliminated).

**Matching fields in edited calibrator:** All five parameters (`card_path`, `rubric_path`, `card_tier`, `flags_context`, `output_path`) are present verbatim in the `## Inputs` section (file L47–L51). The dispatch invocation resolves cleanly.

**Staleness note (NOT a dispatch failure):** the SKILL.md prose says "5-dimension rubric" — this is now stale (rubric is 6-dimension after Change A; calibrator Responsibilities #1 now says "6 dimensions"). This is a documentation phrase, not a parameter contract, so it does NOT break dispatch. Already tracked as a follow-up item in the task frontmatter (Risks section); bundled with Change F.

**Status:** PASS

---

## L202 — Wave 1.7 exit criteria

**Verbatim quote (SKILL.md L202):**

> **Exit criteria**: One hypothesis card at `<output-dir>/tier1-hypothesis.md`, a calibration report at `<output-dir>/tier1-calibration.md` (or `calibration: inline-fallback` in audit), and the calibrated confidence in the audit log. Emit "Wave 1.7 complete: confidence=<x>".

**Matching contract:** The calibrator writes a calibration report to its `output_path` parameter. The "calibrated confidence" the orchestrator pulls is the `**Calibrated (this report)**: <Y.YY>` field in the `## Confidence` section (file L101) — unchanged across Change C. Exit criteria fully resolves.

**Status:** PASS

---

## L263 — Wave 3 dispatch invocation (per-card Tier 2 calibration)

**Verbatim quote (SKILL.md L263):**

> 3.5. **Calibrate each card independently** — spawn N `confidence-calibrator` instances in parallel (one per Tier 2 card), each with `card_tier=2` and `output_path=<output-dir>/tier2-<agent-name>-calibration.md`. Use the calibrated scores (not the agents' self-reports) when weighting consensus/competing/outlier in step 4. Fallback rule from Wave 1.7 applies per-card.

**Matching fields in edited calibrator:** `card_tier` and `output_path` remain present in `## Inputs`. The orchestrator's "calibrated scores" consumption pulls the `**Calibrated (this report)**: <Y.YY>` field (unchanged). The new Stage-2 trace is purely additive — does not displace existing fields.

**Status:** PASS

---

## L340 — Audit-log `escalation_reason` enumeration

**Verbatim quote (SKILL.md L340):**

> escalation_reason: <none|low_confidence|multi_domain|forced_by_depth_deep|intermittent>

**Enumeration listed:** 5 values — `none`, `low_confidence`, `multi_domain`, `forced_by_depth_deep`, `intermittent`.

**Rubric's full enumeration (`escalation-rubric.md` § Escalation Decision):** 8 values — the above 5 PLUS `not_reproducible` (rule 3, L67), `security_caution` (rule 3, L68), and `source_only_dynamic_claim` (Change A, rubric L69).

**Gap (pre-existing tech debt, surfaced not fixed by Change C):** SKILL.md L340 currently lists 5 of the 8 rubric-defined values. Pre-existing missing values: `not_reproducible`, `security_caution`. NEW missing value introduced by Change A and now consumed by Change C: `source_only_dynamic_claim`.

**Status:** PASS (with documented gap) — the dispatch invocation works (the calibrator can return `source_only_dynamic_claim`; the audit log enumeration is what would record it, and the missing values are a documentation gap, not a functional break). Tracked as a Change F follow-up (separate entry below in `change-f-follow-up.md`).

---

## L386 — Tool table reference

**Verbatim quote (SKILL.md L386):**

> | `Task` (agent spawn) | ✓ (root-cause-analyst + confidence-calibrator) | ✓ (2-4 hypothesis agents in parallel + per-card confidence-calibrator + evidence-validator at Wave 5) | ✓ (self-review for post-exec) |

**Matching:** References the `confidence-calibrator` agent by literal name. The agent's `name: confidence-calibrator` frontmatter (file L2) is unchanged across Change C. Reference resolves.

**Status:** PASS

---

## L410 — Will Not Do reference

**Verbatim quote (SKILL.md L410):**

> - Trust agent-reported confidence without independent re-grading (the `confidence-calibrator` agent or the inline fallback applies the rubric in a fresh context)

**Matching:** References the calibrator by name + behavior. The independence behavior was strengthened in Change C (new "read but NOT used as input to your score (independence instruction)" clause in the Self-reported bullet at file L100). Stronger alignment with this Will-Not statement, not weaker. Reference resolves.

**Status:** PASS

---

## L432 — Error handling fallback

**Verbatim quote (SKILL.md L432):**

> | `confidence-calibrator` agent fails for any card | Fall back to inline orchestrator calibration for that card; mark the card with `calibration: inline-fallback` in the audit log; do NOT block escalation on a missing calibration | None |

**Matching:** References the `confidence-calibrator` agent by name. The Failure Modes section of the calibrator (file L136–L141) documents the same fallback contract ("orchestrator falls back to inline calibration for that card; logs `calibration: inline-fallback` in audit"). Reference resolves; the fallback contract on both sides agrees.

**Status:** PASS

---

## OVERALL_VERDICT: PASS

All six SKILL.md dispatch invocations (L199 dispatch, L202 exit criteria, L263 Wave 3 dispatch, L386 tool table, L410 Will-Not declaration, L432 error handling) still resolve cleanly against the post-Change-C calibrator agent. The calibrator's Inputs and named output-field contracts are unchanged; new content (Stage-2 trace, Formula applied bullet) is purely additive.

The one DOCUMENTED gap at L340 (audit-log `escalation_reason` enumeration listing 5 of 8 rubric values, missing `not_reproducible`, `security_caution`, and the Change-A-added `source_only_dynamic_claim`) is pre-existing tech debt that Change C surfaces but does NOT fix. This is tracked as a Change F follow-up — see `phase-outputs/plans/change-f-follow-up.md`.

The named-field parsing model is preserved: the SKILL.md orchestrator parses the calibration report by named fields (`**Calibrated (this report)**`, `## Escalation recommendation`'s `Reason`), not by positional row order. Therefore the new `## Stage-2 trace (REQUIRED)` subsection inserted between the per-dimension table and `## Confidence` does NOT break the parser — it is invisible to the orchestrator's positional concerns.
