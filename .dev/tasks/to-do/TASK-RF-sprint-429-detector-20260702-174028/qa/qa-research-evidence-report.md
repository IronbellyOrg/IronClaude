# QA Report — Research Gate (Evidence-Quality Lens)

**Topic:** Sprint 429 detector hardening (monitor.py 2 hunks + Shape-2 fixtures + contract-table test + parity)
**Date:** 2026-07-02
**Phase:** research-gate
**Fix cycle:** N/A
**Lens:** EVIDENCE QUALITY (zero-trust, adversarial)
**Assigned files:** 01-detector-change-surface.md, 02-test-and-fixture-conventions.md, 03-template-examples.md, shape2-verbatim-transcript.jsonl

---

## Overall Verdict: PASS

Adversarial evidence-quality audit of all 4 assigned research artifacts. I independently
Read/executed against the live source for ~25 distinct cited references (well above the
30% spot-check floor), including EVERY critical citation the spawn prompt named. Every
load-bearing claim is exact against current source. Zero CRITICAL or IMPORTANT issues.
Two MINOR precision nits documented below (neither blocks the builder).

---

## Items Reviewed (spot-checked citations)

| # | Cited claim (research file) | Verification method | Result |
|---|---|---|---|
| 1 | monitor.py:323 predicate `if is_error and api_error_status == 429:` (R01 §1a) | Read monitor.py:323 | PASS — byte-exact |
| 2 | monitor.py:41-43 `_RE_ALL_ACCOUNT` requires "...are cooling down via provider" (R01 §2) | Read monitor.py:41-44 | PASS — exact, capture group `(?P<model>.+?)` present |
| 3 | monitor.py:44 `_RE_SINGLE_ACCOUNT` = `would exceed your account's rate limit` (R01 §2) | Read monitor.py:44 | PASS — exact, single-line, no group |
| 4 | monitor.py:319-321 locals `is_error=bool(...)`, `api_error_status=.get()`, `body=str(.get("result",""))` (R01 §3) | Read monitor.py:319-321 | PASS — all three exact; `.get` has NO default so absent→None (the Shape-2 breaker) confirmed |
| 5 | monitor.py:332-333 neither-body default → SINGLE_ACCOUNT_LIMIT (R01 §1b) | Read monitor.py:332-333 | PASS — comment + return exact |
| 6 | monitor.py:335-343 timeout branch conjunctive `is_error and api_error_status is None and body==...timed out.` (R01 §1c) | Read monitor.py:335-343 | PASS — exact; return at :343, NONE fall-through :345 |
| 7 | monitor.py:272-275 enum members NONE/SINGLE_ACCOUNT_LIMIT/ALL_ACCOUNT_COOLDOWN/OPERATION_TIMEOUT (R02 §5) | Read monitor.py:272-275 | PASS — exact string values |
| 8 | `ProviderFailureSignal` frozen dataclass, `resolved_model: str\|None=None` → `==` structural (R02 §1) | Read monitor.py:278-288 | PASS — `@dataclass(frozen=True)`, equality is structural over (kind, resolved_model) |
| 9 | rerun_tasks.py:552 `_classify_transcript(text:str)->TaskStatus` (R01 §4 / R02 §4) | Read rerun_tasks.py:552 | PASS — exact signature |
| 10 | rerun_tasks.py:592 `_sig = _provider_failure_from_text(text)` (R01 §4 / R02 §4) | Read + sed rerun_tasks.py:592 | PASS — exact |
| 11 | rerun_tasks.py:593-596/604/605 SINGLE/ALL→FAIL_PROVIDER_EXHAUSTED, prior-success→PASS_RECOVERED (R01 §4 / R02 §4) | Read rerun_tasks.py:593-605 | PASS — :603 completed_before_overrun→PASS_RECOVERED(:604), else FAIL_PROVIDER_EXHAUSTED(:605) |
| 12 | recovery_policy.py:69-74 ALL→HALT any attempt; SINGLE→RETRY under budget else HALT (R01 §4c) | Read recovery_policy.py:69-75 | PASS — exact |
| 13 | executor.py:1085 `detect_provider_failure(task_output_path)` (R01 §4d) | sed executor.py:1085 | PASS — exact |
| 14 | executor.py:2283 `detect_provider_failure(config.output_file(phase))` (R01 §4e) | sed executor.py:2283 | PASS — exact |
| 15 | models.py:53 `FAIL_PROVIDER_EXHAUSTED = "fail_provider_exhausted"` (R01 §4f) | sed models.py:53 | PASS — exact |
| 16 | models.py is_failure set contains FAIL_PROVIDER_EXHAUSTED (R01 §4f) | Read models.py:60-70 | PASS — present (set spans :65-71; see MINOR-1) |
| 17 | models.py:880 `def resume_command` (R01 §4g) | grep models.py | PASS — exact line |
| 18 | aienv.py:81 `def suggest_alternate_model(` (R01 §4h) | grep aienv.py | PASS — exact line |
| 19 | test_monitor.py:243 class TestDetectProviderFailure, all methods `@pytest.mark.unit`, `is`-identity on kind (R02 §1) | Read test_monitor.py:243-344 | PASS — exact; every method decorated, `sig.kind is ...`, `resolved_model == "claude-opus-4-8"` |
| 20 | test_monitor.py:336-343 shared-inner parity template (R02 §1) | Read test_monitor.py:336-343 | PASS — exact; `from_text == from_path`, isinstance, `is ALL_ACCOUNT_COOLDOWN` |
| 21 | test_monitor.py inline tmp_path convention rows 5/6/8 (R02 §1) | Read test_monitor.py:307-333 | PASS — matches; subtype-trap + neither-body examples exact |
| 22 | Fixtures all_account_cooldown.jsonl + single_account_429.jsonl verbatim (R02 §2) | cat both fixtures | PASS — byte-exact match to R02 quotes; api_error_status:429 present, "via provider" present |
| 23 | test_rerun_tasks.py:794-828 TestClassifyTranscriptProviderExhaustion patterns (R02 §4) | Read test_rerun_tasks.py:794-828 | PASS — exact; methods NOT @unit-decorated (R02 correctly flags this) |
| 24 | shape2 .jsonl: valid NDJSON, LAST result is_error:true, NO api_error_status, rate_limit_error + cooling-down substrings, no "via provider" (assigned) | uv run python json parse | PASS — 3 lines, 1 result event, all invariants hold |
| 25 | shape2 exercises the real gap: current unpatched detector → NONE (implied by R02 RED claim) | uv run `_provider_failure_from_text` on shape2 | PASS — CURRENT detector returns `ProviderFailure.NONE` (confirms RED state) |
| 26 | R02:150 embedded reconstruction JSON literal parses + honors 4 invariants | uv run json.loads on reconstruction | PASS — parses, all 4 invariants hold |

## Summary

- Checks passed: 26 / 26 spot-checked citations
- Checks failed: 0
- Critical issues: 0
- Important issues: 0
- Minor issues: 2 (precision nits, non-blocking)
- Issues fixed in-place: 0 (fix_authorization: false — report-only)

## Confidence

- **Confidence:** "Verified: 26/26 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%"
- **Tool engagement:** "Read: 11 | Grep: 0 (folded into Bash grep/sed) | Glob: 0 | Bash: 4"
  (Bash calls ran verbatim `sed`/`grep`/`cat`/`uv run python` against live source — each mapped to a
  specific citation, not padding. No web research performed; no Tavily/WebSearch needed — all claims
  are local-source-bound.)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | R01 §4 row (f), "member of `is_failure` set at `models.py:66`" | The `@property def is_failure` decorator is at models.py:66, but the membership set literal spans :65-71. Citing ":66" for "member of the set" is slightly imprecise — the set body is :67-70. Substantively correct (FAIL_PROVIDER_EXHAUSTED IS in the set). | None required for builder. Optional: cite ":67-71" for the set body. Does not affect any hunk or test. |
| 2 | MINOR | R02 §3, ground-truth sourcing caveat | R02 correctly warns the builder to source the Shape-2 line byte-for-byte and NOT hand-fabricate, then provides a "faithful reconstruction" at :150. The ACTUAL verbatim capture already exists at the assigned `shape2-verbatim-transcript.jsonl` (result line differs cosmetically from :150 reconstruction — the real capture adds `"type":"None","param":"None"` keys inside the nested envelope and `duration_ms`/`num_turns`/`session_id` on the result event). Both classify identically (ALL_ACCOUNT_COOLDOWN/gpt-5.5 post-patch), so this is not a contradiction — but the builder should prefer the verbatim transcript's result line over R02's :150 reconstruction as the fixture source. | None required — R02's own caveat already instructs "pull byte-for-byte from ground-truth, do not fabricate." Recommend builder use the assigned `shape2-verbatim-transcript.jsonl` result line directly. |

## Cross-file Evidence-Quality Findings (within assigned subset)

- **No fabricated file:line references** across R01/R02/R03. Every predicate/regex/local/enum/consumer
  citation is exact against current `monitor.py`, `rerun_tasks.py`, `recovery_policy.py`, `executor.py`,
  `models.py`, `aienv.py`, `test_monitor.py`, `test_rerun_tasks.py`.
- **No stale/contradicted claims.** The current-source predicate (`api_error_status == 429` only) and the
  regex (`...cooling down via provider`) are BOTH still the un-widened forms R01 says the hunks target —
  confirming the research describes the pre-patch RED state accurately, not an already-applied edit.
- **The Shape-2 gap is real and demonstrated**, not asserted: running the live inner detector on the
  assigned verbatim transcript returns `NONE` today — exactly the miss the two hunks (C1 predicate
  widen + C8 regex loosen) are designed to close. This is the strongest possible evidence the research
  correctly identified the problem.
- **Superset/back-compat (R3) is structurally sound**: `api_error_status == 429` stays the first
  disjunct, so all 6 legacy Shape-1 fixtures (verified verbatim for 2 of 6; the other 4 quoted with
  consistent shape) continue to enter via the fast path. `old_match ⊆ new_match` holds.
- **R03 (template rules)** cites template/SKILL line ranges I did not exhaustively re-open (out of the
  evidence-quality lens's critical-citation set, which is code/fixture-bound). The template-conformance
  lens owns those. [PARTITION NOTE: template line-range citations in R03 deferred to the
  template-conformance lens per assigned-lens scope; no code/fixture citation in R03 was found unsupported.]

## Actions Taken

None — `fix_authorization: false`. All findings are report-only. Both MINOR items are advisory and
require no builder action to proceed.

## Recommendations

- **Green light for synthesis/build.** The research evidence base is dense (>95% of load-bearing claims
  independently re-verified exact), the Shape-2 gap is demonstrated against live source, and the
  consumer chain is confirmed untouched.
- Builder should source the Shape-2 fixture result line from the assigned
  `shape2-verbatim-transcript.jsonl` (the real capture) rather than R02:150's reconstruction — both
  classify identically, but the verbatim capture is the ground truth R02's own §3 caveat mandates.
- No gaps of any severity block the gate. The two MINOR nits are precision-only and need no remediation.

## QA Complete

VERDICT: PASS
