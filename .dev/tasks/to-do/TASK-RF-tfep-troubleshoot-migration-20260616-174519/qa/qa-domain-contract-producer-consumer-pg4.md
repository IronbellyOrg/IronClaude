# QA Report — Contract Producer-Consumer Integrity (Phase 4)

**Topic:** TFEP return-contract adapter for /sc:troubleshoot — producer/consumer token integrity
**Date:** 2026-06-16
**Phase:** task-integrity (domain lens: contract-producer-consumer-integrity)
**Fix cycle:** N/A
**Fix authorization:** false (REPORT ONLY)

---

## Overall Verdict: PASS

The R-003 §5 adapter-contract gate is satisfied: **every consumer-side token that
task-protocol §4.5 reads from `return-contract.yaml` has a producer** on the troubleshoot
adapter side (Output Contract row + Wave 5 step 4.5 emitter + report-template `## TFEP Consumer`
echo block). No consumer token is left without a producer.

Two non-blocking integration observations (IMPORTANT + MINOR) are documented below. Neither is a
producer-absence for a token the consumer reads from the return contract, so neither overturns the
PASS for THIS lens's scoped gate. They are flagged for the Phase 5 §4.5 rewrite owner.

---

## Token Cross-Check Table (the core deliverable)

The consumer (`sc-task-protocol` §4.5) reads exactly these fields from `return-contract.yaml`
(Step 4 lines 218-224, Step 5 line 227). Each is cross-checked against the producer side.

| # | Consumer token | Where consumer reads it | Producer location(s) | Producer present? |
|---|----------------|-------------------------|----------------------|-------------------|
| 1 | `test_is_wrong` | §4.5 Step 4, line 221 (`if test_is_wrong == true`) | troubleshoot SKILL.md Output Contract row L49 (pre-existing donor); emitter L471; report-template TFEP Consumer block L162 | YES |
| 2 | `status` | §4.5 Step 4, lines 222/223/224 (`== success` / `== partial` / `== failed`) | troubleshoot SKILL.md Output Contract row L43 (pre-existing donor; enum `success`/`partial`/`failed`); emitter L471; report-template TFEP Consumer block L161 (`<success\|partial\|failed>`) | YES |
| 3 | `recommended_escalation` | §4.5 Step 4, line 223 (`!= "none"`) | troubleshoot SKILL.md Output Contract row L73 (NEW Phase 4 row; enum `none\|retry\|escalate_depth\|halt`); emitter L471; report-template TFEP Consumer block L163 | YES |
| 4 | `tasklist_insertion_path` | §4.5 Step 5, line 227 (`Read tasklist_insertion_path`) | troubleshoot SKILL.md Output Contract row L74 (NEW Phase 4 row); emitter L471; report-template TFEP Consumer block L164 | YES |

**Value-level (enum) alignment** — verified, not assumed:

| Token | Consumer compares against | Producer-declared domain | Aligned? |
|-------|---------------------------|--------------------------|----------|
| `status` | `success`, `partial`, `failed` (3 of 3 used) | `success`, `partial`, `failed` (L43; report-template L161) | YES — exact |
| `recommended_escalation` | `none` (negated: `!= "none"`) | `none\|retry\|escalate_depth\|halt` (L73) — `none` is a member | YES — `none` present |
| `test_is_wrong` | `true` | bool (L49) | YES |

**Producer-only fields** (emitted but NOT read by §4.5 today): `remediation_target`,
`root_cause_summary`, `solution_summary`. These are over-supply, not under-supply — over-supply
does not break the §5 gate (consumer simply ignores unread fields). They are present in all three
producer surfaces (emitter L471; report-template L165-167). Per R-003, §4.5 is rewritten in Phase 5;
these may become consumed then. No producer gap.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Enumerate EVERY consumer token read from return contract | PASS | `grep` of §4.5 lines 215-238; reads = {test_is_wrong, status, recommended_escalation, tasklist_insertion_path}. No other contract-field read exists in §4.5 (verified line-by-line; `rca-verdict.md`/`solution-verdict.md` at L249-250 are incident-report template artifacts, NOT return-contract reads). |
| 2 | Each token has an Output Contract producer row | PASS | L43 (status), L49 (test_is_wrong), L73 (recommended_escalation), L74 (tasklist_insertion_path) all present in troubleshoot SKILL.md. |
| 3 | Each token is in the Wave 5 step-4.5 emitter | PASS | troubleshoot SKILL.md L471 emitter lists status, test_is_wrong, recommended_escalation, tasklist_insertion_path (+ 3 over-supply fields). |
| 4 | Each token echoed in report-template `## TFEP Consumer` block | PASS | report-template.md L161-167; all 4 consumed tokens present (L161-164). |
| 5 | Enum/value-level alignment (not just key presence) | PASS | status 3/3 values match; recommended_escalation `none` is a declared member; see value table above. |
| 6 | New Phase-4 rows vs pre-existing donors classified | PASS | Donors: status (L43), test_is_wrong (L49). New Phase-4 adapter rows: recommended_escalation (L73), tasklist_insertion_path (L74), remediation_target (L75), root_cause_summary (L76), solution_summary (L77); all stamped "TFEP adapter field (contract v1.1.0+)". |
| 7 | Emission gating-caller matches consumer's passed caller | FAIL (IMPORTANT) | Producer gates emission on `caller=task-unified` (L148, L471). Consumer §4.5 line 214 passes `--caller task-unified`. Caller NAME aligns. BUT the invocation BINARY does not — see Issue 1. |
| 8 | Contract file path agreement | PASS | Producer writes `<output-dir>/return-contract.yaml` (L471); consumer reads `{output_dir}/return-contract.yaml` (L218). Same filename. |
| 9 | Over-supply fields do not break §5 gate | PASS | remediation_target/root_cause_summary/solution_summary emitted but unread by §4.5; consumer ignores unread keys — no gate violation. |

---

## Summary

- Checks passed: 8 / 9
- Checks failed: 1 (IMPORTANT, integration-adjacent; does NOT overturn the scoped §5 PASS)
- Critical issues: 0
- Producer-absence for a consumer-read token: 0 (the adversarial hypothesis of "3+ consumer fields with no producer" was tested and DISPROVEN — all 4 consumed tokens have producers across all 3 surfaces)

---

## Issues Found

| # | Severity | Location | Issue | Required Fix (for Phase 5 owner — NOT applied) |
|---|----------|----------|-------|------------------------------------------------|
| 1 | IMPORTANT | task-protocol §4.5 L214 vs L137 | Invocation-binary mismatch. §4.5 Step 3 L214 invokes `/sc:forensic --tier {tier} --intent triage --caller task-unified ...`, but the declared diagnostic backend (L137) is `/sc:troubleshoot`. The producer that emits `return-contract.yaml` is `sc:troubleshoot-protocol` (Wave 5 step 4.5). `/sc:forensic` is a different (likely non-existent / legacy) command. If §4.5 actually invokes `/sc:forensic`, the troubleshoot producer never runs and NONE of the 4 tokens are produced — the entire contract is dead at runtime. The token-schema mapping is sound; the wiring of WHICH backend gets invoked is stale. Per the brief, §4.5 has NOT yet been rewritten (that is Phase 5) — this is the exact stale-wiring Phase 5 must correct. Phase-5 rewrite must replace the `/sc:forensic ...` invocation string (L214) AND the `--tier/--intent` flags (which troubleshoot does not accept — it uses `--depth`/`--caller`/`--context`/`--output`) with a valid `/sc:troubleshoot` invocation. Flagging now so Phase 5 does not inherit it silently. |
| 2 | MINOR | task-protocol §4.5 L249-250 | Incident-report template references `{summary from rca-verdict.md}` and `{summary from solution-verdict.md}`. The troubleshoot producer emits NO `rca-verdict.md` / `solution-verdict.md` artifacts — its summaries live in `root_cause_summary` / `solution_summary` return-contract fields (producer L76-77, over-supplied today). These template placeholders point at non-existent producer artifacts. Not a return-contract-field gap (these are not read from the contract), hence MINOR, but the Phase-5 rewrite should re-point them at `root_cause_summary`/`solution_summary` so the incident report has a real source. |

---

## Actions Taken

None — `fix_authorization: false`. Report-only lens. Issues 1 and 2 are documented for the Phase 5
§4.5 rewrite owner; do NOT resolve them in Phase 4.

---

## Recommendations

- **PASS the R-003 §5 adapter-contract gate for Phase 4.** Every consumer token has a producer.
  The Phase-4 work (adding `recommended_escalation`, `tasklist_insertion_path`, `remediation_target`,
  `root_cause_summary`, `solution_summary` to the Output Contract + emitter + report-template) is
  complete and consistent across all three producer surfaces.
- **Carry Issue 1 (IMPORTANT) into Phase 5 as a mandatory rewrite item.** The §4.5 invocation still
  names `/sc:forensic` with `--tier/--intent` flags that the troubleshoot backend does not accept.
  This is the known stale-consumer state per R-003; surfacing it ensures Phase 5 does not ship a
  contract whose producer is never invoked. (Note: this lens verifies token-level producer presence,
  which holds; the invocation-wiring defect is orthogonal to the §5 token gate and is Phase 5 scope.)
- **Carry Issue 2 (MINOR) into Phase 5.** Re-point the incident-report template's
  `rca-verdict.md`/`solution-verdict.md` references at the `root_cause_summary`/`solution_summary`
  contract fields.

---

## Confidence

**Confidence:** Verified: 9/9 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
(All 9 checklist items closed with tool evidence. The 1 FAIL is a verified finding, not an unchecked item.)

**Tool engagement:** Read: 3 | Grep: 0 (unavailable this session) | Glob: 0 | Bash: 4 (grep via Bash — 3 multi-file content searches + 1 enum/caller alignment search)

No web research was required — this is a fully local source-truth verification (Principle 6); no
external/URL/standards-bound claim was in scope, so Tavily was not engaged.

Tool-engagement note: total content-search invocations (4 Bash greps, each covering multiple files
and patterns) + 3 Reads = 7 evidence-gathering calls against 9 checklist items. Each grep targeted
specific tokens being verified (not padding); the multi-pattern/multi-file form means call count is
below item count but every item maps to cited tool output above.

## QA Complete
