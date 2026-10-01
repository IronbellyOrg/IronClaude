# QA Report — Research Gate (Gap-Detection Lens)

**Topic:** Sprint 429 detector hardening + Shape-2 fixtures + contract-table + parity
**Date:** 2026-07-02
**Phase:** research-gate
**Fix cycle:** N/A
**Fix authorization:** false (report-only)

---

## Scope

- Research dir: `.dev/tasks/to-do/TASK-RF-sprint-429-detector-20260702-174028/research/`
- Assigned files: `01-detector-change-surface.md`, `02-test-and-fixture-conventions.md`, `03-template-examples.md`, `shape2-verbatim-transcript.jsonl`
- BUILD-REQUEST: 9 deliverables
- Lens: GAPS the builder would hit

## Verification actions performed (evidence log)

Every research claim below was re-verified against CURRENT source this turn:

- `monitor.py:319-345` — Read. C1 predicate at `:323` (`if is_error and api_error_status == 429:`) CONFIRMED verbatim. Timeout branch `:335-343`, terminal NONE `:345`, neither-body default `:332-333` all CONFIRMED. Locals `is_error`/`api_error_status`/`body` at `:319-321` CONFIRMED.
- `monitor.py:41-44` — Read. `_RE_ALL_ACCOUNT` at `:41-43` requires `via provider` (C8 target) CONFIRMED; `_RE_SINGLE_ACCOUNT` at `:44` CONFIRMED.
- `monitor.py:272-275` — Read. Enum members NONE/SINGLE_ACCOUNT_LIMIT/ALL_ACCOUNT_COOLDOWN/OPERATION_TIMEOUT CONFIRMED (research/02 cited `:272-275`).
- `rerun_tasks.py:552` — Read. `def _classify_transcript(text: str) -> TaskStatus` CONFIRMED (text arg, not path). Delegates to inner at `:592`; returns `FAIL_PROVIDER_EXHAUSTED` at `:605`, `PASS_RECOVERED` at `:604`. CONFIRMED.
- `rerun_tasks.py:607-618` — Read. Post-exhaustion ladder: `not is_error and output_tokens>0 → PASS`; else transient→FAIL_RECOVERABLE; `is_error`→FAIL_TERMINAL; else INCOMPLETE. (Used for FP-parity trace below.)
- `test_rerun_tasks.py:42-57` — Read. `_classify_transcript` imported at `:43`; `_FIXTURES` at `:57`. CONFIRMED.
- `test_rerun_tasks.py:794-828` — Read. `TestClassifyTranscriptProviderExhaustion` at `:794`; `test_completed_then_trailing_429_recovers_not_exhausted` at `:815-828`; class methods NOT `@pytest.mark.unit`-decorated. CONFIRMED (research/02 §4 called this out).
- `test_monitor.py:243-343` — Read. `TestDetectProviderFailure` at `:243`; `test_text_core_matches_path_wrapper` at `:336-343`; inline `tmp_path.write_text` convention at `:307-332`; `resolved_model == "claude-opus-4-8"` (== + str) / `kind is` (identity) convention CONFIRMED.
- `test_recovery_policy.py` — Read entire (27 lines). 7-row `decide()` truth table CONFIRMED byte-for-byte with research/02 §6.
- `shape2-verbatim-transcript.jsonl` — Read (3 lines). Result line (line 3) carries `is_error:true`, NO `api_error_status` key, `rate_limit_error` substring, `All credentials for model gpt-5.5 are cooling down` (NO "via provider"). All 4 R1/R2 invariants CONFIRMED present in the byte-source. `model:"gpt-5.5"` in init line.

Cross-file result: every file:line the research asserts is accurate against current source. No stale citations. `start_commit` 156f2829 matches HEAD in git status.

---

## Findings — targeted gap analysis (the builder's-eye lens)

### G-A [MINOR] FP fixture (deliverable 4): PASS-vs-INCOMPLETE authoring precision under `_classify_transcript`

**Trace (verified `rerun_tasks.py:607-618`):** The FP fixture is `is_error:false` with incidental "429"/"rate limit" prose. Under the NEW widened gate, `is_error` short-circuits → `_provider_failure_from_text` returns NONE → the exhaustion branch (`:593-605`) is skipped. Good — deliverable-7c's parity assert `_classify_transcript(fp) is not FAIL_PROVIDER_EXHAUSTED` holds robustly. **BUT** whether it lands on `PASS` vs `INCOMPLETE` depends on `total_output_tokens`: `:607` returns PASS only if `not is_error AND total_output_tokens > 0`. If the builder authors the FP fixture as a bare result line with no assistant/usage event, `total_output_tokens == 0` → it falls through to `INCOMPLETE` (`:618`), NOT PASS.

- Research/02 §4 item 3 says the FP fixture "should be `PASS`/`NONE`-classified, never provider-exhausted" — the `is not FAIL_PROVIDER_EXHAUSTED` assert is safe either way, so this is NOT a blocker. But research does NOT instruct the builder to include an `output_tokens>0` assistant line if they want deterministic PASS. If a builder over-tightens 7c to `is PASS` (following the parenthetical), a bare-result FP fixture fails.
- **Remediation:** Research/02 should add one sentence: "FP fixture (row 9) — for `_classify_transcript` to land on PASS (not INCOMPLETE) it must carry an assistant event with `output_tokens>0`; regardless, spec the parity assert as `is not FAIL_PROVIDER_EXHAUSTED` (never `is PASS`)." Severity MINOR because the spec §6.3.3 already correctly specifies `is not FAIL_PROVIDER_EXHAUSTED`; the risk is only builder over-tightening.

### G-B [MINOR] Detector-level FP row-9 assertion is `NONE`, and that IS covered — no gap, recorded for completeness

Row 9 (detector table, `detect_provider_failure`) asserts `NONE`. Trace under widened gate: `is_error:false` → conjunct short-circuits → falls past timeout branch (`api_error_status is None` but `body != "API Error: The operation timed out."`) → terminal `NONE` (`monitor.py:345`). CONFIRMED reachable and correct. No gap. (Distinct from G-A which is the OFFLINE classifier's PASS/INCOMPLETE ambiguity.)

### G-C [IMPORTANT] Timeout unreachability test (deliverable 8 / F5): the test's ASSERTION MECHANISM is under-specified

The BUILD-REQUEST deliverable 8 and spec §6.4 both mandate an F5 test asserting "a 429 body never reaches the timeout branch — every `is_error` 429 returns inside the 429 block before `:335`." **Neither research/01 nor research/02 gives the builder a concrete test design for HOW to assert unreachability.** This is a genuine authoring gap because "assert the code returns before line 335" is not directly observable from a black-box `detect_provider_failure` call — the function has no branch-trace hook.

- The only tractable black-box design is behavioral: construct a transcript that carries BOTH a 429 signal (`is_error:true` + `rate_limit_error` in body OR `api_error_status==429`) AND the exact timeout body string, then assert the result is a 429 kind (SINGLE/ALL_ACCOUNT), NOT `OPERATION_TIMEOUT` — proving the 429 branch intercepts first. **But this is impossible to construct faithfully:** the timeout branch requires `body == "API Error: The operation timed out."` (exact `==`, `monitor.py:338`), while the 429 branch's text disjunct requires `rate_limit_error` to be a substring of that SAME `body`. A body cannot simultaneously `== "API Error: The operation timed out."` AND contain `rate_limit_error`. So the two branch predicates are **mutually exclusive by construction** — which is precisely WHY the timeout is unreachable for 429s, but also means the naive "both-signals transcript" test cannot be authored.
- The correct F5 design is therefore an **ordering/structural argument**, not a both-signals fixture: e.g. (a) assert that for every 429-classifying fixture, `.kind is not OPERATION_TIMEOUT`; OR (b) a source-structural assert (the 429 `if` block at `:323` textually precedes the timeout `if` at `:335` and every 429 path `return`s). Research does not name which of these the builder should write, nor flag the mutual-exclusivity that makes the "obvious" both-signals test un-authorable.
- **Remediation (IMPORTANT):** Research/01 or /02 must add an F5 test-design paragraph: state the timeout body (`==`) and the 429 text-gate (`rate_limit_error` substring) are mutually exclusive, so F5 must be either (i) a parametrized `assert sig.kind is not ProviderFailure.OPERATION_TIMEOUT` across all 429 rows, or (ii) an explicit inline transcript with `api_error_status:429` + a non-timeout body asserting it returns a 429 kind while a sibling timeout fixture returns OPERATION_TIMEOUT — i.e. prove the branches don't collide. Without this, the builder is left to guess the assertion mechanism (a real risk of authoring a vacuous or impossible test).

### G-D [IMPORTANT] `pytest.mark.parametrize` matrix + xfail-empty-cell convention: the resolved_model=None handling is specified, but the xfail MECHANICS and per-row source-encoding are left "builder's choice" with no worked example

Deliverable 6 requires a ~12-row parametrize matrix asserting `(kind, resolved_model)` per row (incl. `None`), with empty/impossible cells as explicit `xfail`/skip (never silent). Research/02 §5 reproduces the 12-row table parametrize-ready and gives a `def test_detection_contract_table(source, expected_kind, expected_model, tmp_path)` skeleton. Coverage of the resolved_model=None requirement (OQ4) is GOOD — every row's expected model is enumerated including `None`.

**Gap:** the research explicitly punts the two hardest authoring decisions to "builder's choice" without a worked example:
1. **The `source` encoding for mixed fixture-vs-inline rows.** Research/02 §5 says "The builder must decide a uniform `source` encoding" and offers two options (single list with filename-or-tmp_path dispatch, or two parametrize lists) but shows neither fully wired. A parametrize that mixes a `_FIXTURES / name` path (rows 1-4,7,9-12) with an inline JSON string needing `tmp_path.write_text` (rows 5,6,8) requires branching inside the test body on the source type — a non-trivial pattern the builder must invent. The `tmp_path` fixture is function-scoped, which interacts with parametrize in a way worth a worked snippet.
2. **The xfail mechanics.** Research/02 §5 says empty cross-product cells get `pytest.param(..., marks=pytest.mark.xfail(reason=...))` but then states "No matrix cell is currently expected to be `xfail` after the fix lands." This is internally tense: the spec §6.2 mandates empty/impossible cells be explicit xfail/skip "so a THIRD drift maps to exactly one visible failing row," yet research concludes none of the 12 enumerated rows is actually xfail. **So what is the xfail convention actually FOR here?** The 12 rows are all expected-GREEN. The builder is told to use xfail for "genuinely impossible cross-product cells" but the 3×2×3=18 full cross-product minus the 12 named rows = 6 unnamed cells that research never enumerates. Research does not tell the builder whether to (a) add those 6 cells as explicit xfail rows, or (b) treat the 12-row table as complete and omit xfail entirely. This ambiguity directly undercuts the spec's "never silent omission" invariant.
- **Remediation (IMPORTANT):** Research/02 §5 should either (i) enumerate the full 18-cell cross-product and mark the 6 impossible cells explicitly as `xfail(reason=...)` rows so the builder copies them verbatim, OR (ii) explicitly state "the 12 named rows ARE the complete contract; no xfail rows are needed because the impossible cells are the ones we deliberately did not enumerate" and reconcile that against spec §6.2's never-silent-omission rule. As written, a builder cannot tell whether omitting the 6 cells satisfies or violates the spec. Additionally, provide ONE fully-wired parametrize snippet showing the fixture-vs-inline `source` dispatch (not just a skeleton with `<path>`).

### G-E [IMPORTANT] Research/02 §3's hand-reconstructed Shape-2 literal DIFFERS from the verbatim transcript — a re-fabrication trap the builder could copy

The BUILD-REQUEST (lines 44-50) is emphatic: the load-bearing fixture MUST reproduce `shape2-verbatim-transcript.jsonl`'s result line BYTE-FOR-BYTE; hand-fabrication is "precisely what caused the original incident." Research/02 §3 correctly repeats this warning AND correctly tells the builder to pull the byte-exact line from the verbatim file. **However**, research/02 §3 ALSO embeds a "faithful reconstruction" literal (line 150) that does NOT match the actual verbatim source:

- Verbatim (`shape2-verbatim-transcript.jsonl` line 3) result value contains: `...cooling down\\\"}}'\",\"type\":\"None\",\"param\":\"None\",\"code\":\"429\"}}` and the full result event also carries `duration_ms`, `duration_api_ms`, `num_turns`, `session_id`, `total_cost_usd`, `usage`, `modelUsage`, `permission_denials`, `uuid`.
- Research/02 §3 reconstruction OMITS `"type":"None","param":"None"` from the nested envelope and drops all the outer telemetry keys, keeping only `type/subtype/is_error/result`.

Because the detector keys ONLY on the LAST result event's `is_error` + `api_error_status` (absent) + `rate_limit_error`-in-`result` + the all-account regex, the reconstruction WOULD still classify correctly (the 4 invariants survive). So this is not a correctness gap in the detector logic. **The risk is procedural:** a builder skimming research/02 §3 could copy the convenient inline reconstruction instead of doing the `Read shape2-verbatim-transcript.jsonl → byte-copy line 3` step the BUILD-REQUEST mandates — re-introducing exactly the fabrication the task exists to prevent. The reconstruction's presence in the research directly competes with the anti-fabrication instruction 6 lines above it.

- **Remediation (IMPORTANT):** Research/02 §3 should DELETE the inline reconstructed literal (or replace it with an explicit non-authoring marker like "DO NOT COPY — illustrative field-shape only; the fixture MUST be a byte-copy of `research/shape2-verbatim-transcript.jsonl` line 3"). At minimum it must note that the reconstruction diverges from the verbatim source (missing `type/param/None` + outer telemetry) so no builder mistakes it for copy-ready. The task file's fixture item (deliverable 3) MUST instruct: `Read research/shape2-verbatim-transcript.jsonl, copy the line-3 result event verbatim` — never "use the literal in research/02."

### G-F [MINOR] Verification-command coverage is strong; one thin spot on the F5/regression test node paths

Research/02 §7 covers the verification commands well: scoped `uv run pytest tests/sprint/{test_monitor,test_rerun_tasks,test_recovery_policy}.py -v`, full `tests/sprint/ -v`, the `make lint` (ruff check only) vs CI `uv run ruff format --check src/ tests/` distinction (with the changed-files-scoping footgun from project memory), and `make verify-sync` (no-op here, don't stage `.claude/`). The BUILD-REQUEST VALIDATION block matches. This is adequately covered — no gap on the make-lint-vs-CI-ruff distinction (explicitly called out).

Minor thin spot: research does not give the exact pytest node id for the F5 unreachability test or the parity tests once authored (understandable — they don't exist yet), and the RED→GREEN discipline (§7 tail) names rows 4/6/7 as the ones that must FAIL pre-fix but does not name the F5 test or the offline parity tests (7b/7c/7d) in the RED set. A builder should also confirm 7b (`_classify_transcript(shape2) is FAIL_PROVIDER_EXHAUSTED`) is RED pre-fix. MINOR.

### G-G [no gap — integration-point sweep, recorded for completeness]

Lens asked: does widening the gate risk a false positive NOT covered by a test, at the live executor seam? Traced the consumer chain (research/01 §4, spot-confirmed `rerun_tasks.py:592-605`): the executor call sites (`executor.py:1085`, `:2283`) and policy `decide()` consume only the `ProviderFailure.kind` enum, which does not change. The only NEW positive the widened gate can produce is the INV-001 residual (row 8: `is_error:true` + `rate_limit_error` in body + neither all/single body → SINGLE_ACCOUNT_LIMIT → one bounded `RETRY_NEW_SESSION`). This is **documented (spec §4 R4 / §7) AND tested (contract row 8)**. No uncovered new-FP surface at the executor seam. The existing non-429 fixtures (`operation_timeout` body `== "API Error: The operation timed out."`, `task_failure_real` body `"Tool execution failed: pytest exited 1"`, `clean_pass` `is_error:false`) contain NO `rate_limit_error` substring, so the widened gate stays closed for all three — confirmed by inspecting the fixture bodies in research/02 §2. No gap.

---

## Items Reviewed (10-item research-gate checklist)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | File inventory (all 3 .md + .jsonl Status:Complete + Summary) | PASS | All 3 research .md carry `Status: Complete` + a `## Summary`. shape2 .jsonl is a data reference (3 valid JSON lines), not a report — correct form. |
| 2 | Evidence density (claims cite file:line, paths exist) | PASS (Dense >80%) | Every research/01 + /02 claim cites `file:line`; I re-verified 11 distinct citations against current source — all exact. `monitor.py`/`rerun_tasks.py`/both test files confirmed. |
| 3 | Scope coverage (all key files discussed) | PASS | Change surface (monitor.py), both consumer paths, all 3 test files, all 6 fixtures, template rules — every deliverable's target file is covered. |
| 4 | Documentation cross-validation (doc claims tagged) | PASS (N/A) | Research is CODE-research: 0 doc-sourced claims (grep for `[CODE-VERIFIED]`-style tags = 0; research uses "CONFIRMED at file:line" against code). No untagged doc-only claims exist. |
| 5 | Contradiction resolution | FAIL | Internal tension G-D (xfail: "impossible cells must be xfail" vs "no cell is xfail") + G-E (anti-fabrication instruction vs an inline reconstructed literal that diverges from the verbatim source). Both surfaced, not silently resolved. |
| 6 | Gap severity (all gaps = FAIL) | FAIL | 3 IMPORTANT (G-C timeout-test design, G-D xfail/parametrize, G-E reconstruction trap) + 3 MINOR (G-A FP PASS/INCOMPLETE, G-B recorded-no-gap, G-F node-paths). Any gap = gate FAIL. |
| 7 | Depth appropriateness | PASS | Standard/file-level depth is correct for this narrow change; research/01 traces the full live+offline data flow end-to-end (predicate→branch→consumer→status→resume). |
| 8 | Integration-point coverage | PASS | Live wrapper + offline classifier + policy + executor + resume + alias-suggester all mapped (research/01 §4). Widened-gate FP surface traced (G-G) — no uncovered seam. |
| 9 | Pattern documentation | PASS | Test conventions (`@pytest.mark.unit`, `is` vs `==`, inline `tmp_path`, fixture NDJSON shape), template B2/A3 granularity, POST-reflect wrapper form all documented (research/02, /03). |
| 10 | Incremental-writing compliance | PASS | Research files show sectioned, iterative structure with per-claim citations; not one-shot prose walls. No sign of compression data-loss. |

**Checklist verdict:** 8 PASS / 2 FAIL (items 5, 6). Items 5 and 6 FAIL because gaps of IMPORTANT and MINOR severity exist — under the research-gate zero-tolerance rule, ANY gap of ANY severity = overall FAIL.

---

## Confidence Gate

- [x] VERIFIED — items 1,2,3,4,7,8,9,10 (tool evidence: 11 source Reads + 1 Bash fixture-listing, all cited above)
- [x] VERIFIED — items 5,6 (the gaps themselves are evidenced by direct source trace: `rerun_tasks.py:607-618` for G-A, `monitor.py:338`+`:323` mutual-exclusivity for G-C, verbatim-vs-reconstruction byte-diff for G-E)
- [?] UNVERIFIABLE — none
- [ ] UNCHECKED — none

**Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 11 | Grep: 1 | Glob: 0 | Bash: 2 (fixture-list + tail) | tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0 — no external lookup required (all claims are local-source-bound; Principle 6 primary surface fully sufficient).
Tool calls (14) ≥ checklist items (10) — engagement minimum satisfied; each Read/Grep/Bash targeted a specific claim.

---

## Summary

- Checks passed: 8 / 10
- Checks failed: 2 (items 5 contradiction, 6 gap-severity — both driven by the 6 findings below)
- Critical issues: 0
- Issues found: 6 (IMPORTANT: 3 [G-C, G-D, G-E], MINOR: 2 [G-A, G-F]; G-B and G-G are recorded no-gaps)
- Issues fixed in-place: 0 (fix_authorization: false — report-only)

**The research is strong on the load-bearing surface:** every monitor.py/rerun_tasks.py/test file:line is verified-accurate, the Shape-2 verbatim transcript is present and carries all 4 R1/R2 invariants, the offline-parity import/call form (deliverable 7b/7c) is fully documented and confirmed against the real `test_rerun_tasks.py` seam, and the resolved_model=None matrix requirement (OQ4) is completely enumerated. The gaps are authoring-precision gaps in the VERIFICATION surface — exactly where this task's stated risk lives (§10 anti-under-engineering) — not correctness gaps in the 2-hunk production change.

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| G-A | MINOR | research/02 §4 item 3 | FP fixture PASS-vs-INCOMPLETE under `_classify_transcript` depends on undocumented `output_tokens>0`; builder could over-tighten 7c to `is PASS` and fail | Add: FP parity assert must be `is not FAIL_PROVIDER_EXHAUSTED` (never `is PASS`); note output_tokens>0 needed for deterministic PASS |
| G-C | IMPORTANT | research/01+/02 (F5) | Timeout-unreachability test (deliverable 8) has NO concrete assertion design; the "obvious" both-signals fixture is un-authorable (timeout `==` body ⟂ `rate_limit_error` substring) | Add F5 design: parametrized `assert kind is not OPERATION_TIMEOUT` across 429 rows, and state the mutual-exclusivity that makes a both-signals test impossible |
| G-D | IMPORTANT | research/02 §5 | parametrize `source` encoding + xfail-empty-cell convention left "builder's choice"; internal tension on whether the 6 unnamed cross-product cells need explicit xfail (spec §6.2 "never silent") | Provide ONE fully-wired parametrize snippet (fixture-vs-inline dispatch); resolve the xfail convention — either enumerate all 18 cells or explicitly declare the 12 rows complete |
| G-E | IMPORTANT | research/02 §3 (line 150) | Inline "faithful reconstruction" literal DIFFERS from verbatim transcript (missing `type/param/None` + telemetry) and competes with the anti-fabrication instruction 6 lines above — re-fabrication trap | DELETE the inline literal or mark it "DO NOT COPY"; task fixture item must instruct byte-copy from `research/shape2-verbatim-transcript.jsonl` line 3 |
| G-F | MINOR | research/02 §7 | RED→GREEN set names rows 4/6/7 but omits F5 + offline parity tests (7b/7c/7d) from the pre-fix RED expectation | Add 7b/7c/7d + F5 to the RED→GREEN pre-fix checklist |

## Recommendations

Before the builder proceeds, the research authors (or the task-builder, folding these into the deliverable items) must resolve all 6 findings. The three IMPORTANT items (G-C, G-D, G-E) are the ones most likely to cause a builder to author a vacuous/impossible test (G-C), silently violate the never-omit invariant (G-D), or re-fabricate the load-bearing fixture (G-E). The two MINOR items are precision hardening. None require re-doing research — all are additive clarifications to research/01 §(F5 design) and research/02 §3/§4/§5/§7. In particular, the task file's fixture item (deliverable 3) MUST carry the explicit `Read + byte-copy from research/shape2-verbatim-transcript.jsonl line 3` instruction, since that is the single most incident-relevant step.

---

## Overall Verdict: FAIL

Gaps of IMPORTANT and MINOR severity exist. Under the research-gate zero-tolerance rule (ALL gaps regardless of severity = FAIL), the gate does not pass. These are authoring-precision gaps in the verification surface, not correctness defects — they are cheaply remediable via additive clarifications to research/01 and research/02 without re-running research. Recommend the orchestrator route G-A/C/D/E/F to a gap-fill pass (or have task-builder absorb them directly into the deliverable items) before synthesis/task-file generation proceeds.

VERDICT: FAIL

## QA Complete

