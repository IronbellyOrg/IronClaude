# QA Report — needs-human-decision-handling (OQ-2 nominator exclusion)

## Overall Verdict: PASS

**Topic:** TASK-RF-429-recovery — OQ-2 (nominator exclusion) human-decision-handling lens
**Date:** 2026-06-18
**Phase:** doc-qualitative (needs-human-decision-handling content lens, P6/PG7.3)
**Fix cycle:** N/A (fix_authorization: false — report only)
**Stance:** ADVERSARIAL. Began from the assumption that P6 silently shipped a human-decision alternative. Read the actual source files end-to-end to disprove or confirm. The assumption was NOT borne out — the work is clean.

> NOTE: this path previously held a stale P5/OQ-1 report (filename collides across gates, per task-file ### Phase Gate Findings). Overwritten with the current P6/OQ-2 lens verdict.

---

## Lens Question

Did P6 honor the operator's DECISION for OQ-2 (option a — filter on persisted `failure_class == "provider_exhaustion"` in `select_default_recoverable_tasks`), and did it AVOID silently shipping the rejected alternative (option b — plumbing a failure_class map into the `nominate()` context) OR any new unreviewed `rerun-tasks` behavior under cover of the "NECESSARY EXTENSION"?

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | OQ-2 implemented per operator DECISION (option a) — `select_default_recoverable_tasks` filters persisted `failure_class == "provider_exhaustion"` | PASS | `rerun_tasks.py:1188` — `if entry.get("failure_class") == "provider_exhaustion": continue` inside the `select_default_recoverable_tasks` loop (def at :1159). Reads the persisted per-task `failure_class` from the deserialized `phase-result.json`. Confirmed by direct Read. |
| 2 | Rejected alternative (option b — plumbing failure_class into `nominate()` context) NOT silently shipped | PASS | All 3 `nominate()` call sites pass a literal empty dict: `rerun_tasks.py:1452/1454/1475` (`.nominate({})`). `recovery.py` nominators contain ZERO `failure_class`/`provider_exhaustion`/`context[...]` references (grep returned none). `ManualNominator.nominate` (recovery.py:160-161) returns `list(self.tasks)` — ignores `context` entirely. The exclusion lives upstream at the caller, NOT in the nominator. Confirmed by Read + grep. |
| 3 | NECESSARY EXTENSION (fallback-caller filter in `run_rerun_tasks`) is a legitimate engineering completion of option (a)'s goal (UX-contract #4) — NOT a silently-shipped undecided alternative, and introduces NO new rerun-tasks behavior beyond excluding provider-exhausted tasks | PASS | `rerun_tasks.py:1468-1474` — the fallback `default_ids` is a pure SUBTRACTIVE list-comprehension over `discover_failed_tasks_from_transcripts(...)` that drops ONLY `_status is TaskStatus.FAIL_PROVIDER_EXHAUSTED`; every other non-PASS status is kept verbatim. `discover_failed_tasks_from_transcripts` (def :621, returns `list[tuple[str, TaskStatus]]`) is left PURE — its body/docstring carry no provider-exhaustion special-casing (the manifest's "leaving it pure for other consumers" claim verified). The extension stays strictly within the operator-decided exclusion intent: same UX-contract #4 goal, narrower candidate set, no new emission/renaming/nomination semantics. Test `test_transcript_fallback_classifies_exhaustion_distinctly` (test_rerun_tasks.py:403) asserts terminal kept + exhausted excluded (`nominated == ["T03.20"]`, line 451). Confirmed by Read of both functions + the test. |
| 4 | OQ-2 is operator-decided ⇒ NO human-decision PENDING note expected; only a genuine technical `[BLOCKER]` would appear — confirm none was needed / contingency not triggered | PASS | Phase 7 Findings (task file :762-766) contains exactly ONE entry: `[OQ-2 RESOLUTION + NECESSARY EXTENSION]`. No templated `**[BLOCKER]**` entry was logged (the only bold-templated occurrence is the section's placeholder legend at :764; the 2 raw `[BLOCKER]` word-matches are the legend + the prose "the contingency `[BLOCKER]` path was not needed"). No human-decision PENDING note exists for OQ-2 — every PENDING/needs_human_decision reference in the task file is an explicit *affirmation of "no PENDING"* for the operator-decided OQs (:707, :710, :766), never an actual deferral. Confirmed by scoped grep. |

---

## Summary

- Checks passed: 4 / 4
- Checks failed: 0
- Critical issues: 0
- Important issues: 0
- Minor issues: 0
- Issues fixed in-place: 0 (fix_authorization: false)

**Adversarial conclusion:** The hypothesis "P6 silently shipped a human-decision alternative" is DISPROVEN by the source. Option a is the shipped path; option b is documented-not-shipped (the `nominate()` context is a verifiably-empty `{}` and the nominators never read `failure_class`). The NECESSARY EXTENSION is a legitimate, in-scope engineering completion — a pure subtractive filter at the realistic leak point (`run_rerun_tasks` fallback) that excludes only `FAIL_PROVIDER_EXHAUSTED` and introduces no new rerun-tasks behavior. No human-decision PENDING note was written (correct — OQ-2 is operator-decided) and no technical `[BLOCKER]` was needed (correct — option a was trivial to add).

## Confidence

Verified: 4/4 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

Tool engagement: Read: 5 | Grep: 6 | Glob: 0 | Bash: 0

Every check was verified against actual source code, not against the manifest or Phase 7 Findings prose. Specifically:
- `rerun_tasks.py:1159-1196` (`select_default_recoverable_tasks` — the option-a filter at :1188).
- `rerun_tasks.py:1448-1483` (`run_rerun_tasks` nominate block — the fallback-caller extension at :1468-1474; all 3 `nominate({})` sites).
- `rerun_tasks.py:621-660` (`discover_failed_tasks_from_transcripts` — confirmed left pure).
- `recovery.py:143-193` (`Nominator` Protocol + `ManualNominator`/`ReflectReportNominator` — confirmed ignore `context`, no `failure_class`).
- `executor.py:1007/1026/1087/1142` + `models.py:192/222/251` (persistence chain — confirmed the filtered `failure_class` field is actually written to and read back from `phase-result.json`, so the filter is LIVE, not dead code).
- `tests/sprint/test_rerun_tasks.py:348-451` (`TestProviderExhaustionNominationExclusion` — 3 tests asserting the exclusion on both seams).
- Task file `:705-710` (Open Questions / operator DECISION) and `:762-766` (Phase 7 Findings).

## Self-Audit (mandatory)

1. **How many factual claims independently verified against source code?** All claims load-bearing to the 4 checks: the option-a filter line, the empty `nominate({})` contexts, the nominators' indifference to context, the fallback filter's subtractive-only nature, `discover_failed_tasks_from_transcripts` purity, the failure_class persistence chain, the test assertions, and the absence of any `**[BLOCKER]**`/PENDING entry. Each was read in the actual file, not inferred from the manifest.
2. **What specific files were read?** `src/superclaude/cli/sprint/rerun_tasks.py`, `src/superclaude/cli/sprint/recovery.py`, `src/superclaude/cli/sprint/executor.py` (grep), `src/superclaude/cli/sprint/models.py` (grep), `tests/sprint/test_rerun_tasks.py` (grep), the task file's Open Questions + Phase 7 Findings, and the p6-aggregate manifest.
3. **Why trust this review found a clean result?** Because the adversarial hypothesis had three concrete falsification targets (a non-empty `nominate()` context, a `failure_class` read inside a nominator, or a fallback filter that did more than exclude provider-exhausted tasks) and all three were directly inspected and found absent in source. The result is PASS not because nothing was found suspicious, but because the specific suspected violations were each checked at the byte level and ruled out. Additionally I verified the filter is not dead code (the persistence chain writes `failure_class`), which is the subtle way an "implemented" exclusion can be silently inert — it is not.
4. **Web research performed?** None. This lens is entirely local-file-bound; no external lookup was required, so no Tavily/fallback engagement applies.

## Recommendations

None. OQ-2 human-decision handling is correct on all four checks. The lens passes; the gate may proceed on this dimension.

## QA Complete
