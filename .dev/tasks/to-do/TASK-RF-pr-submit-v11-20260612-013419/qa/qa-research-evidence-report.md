# QA Report — Research Gate (Evidence-Quality Lens)

**Topic:** Implement pr_submit V1.1 (FR-8/9/10) honoring NFR-6 core purity + INV-001 verbatim
**Date:** 2026-06-12
**Phase:** research-gate
**Lens:** evidence-quality
**Fix cycle:** N/A
**Fix authorization:** false (report-only)

---

## Method

Adversarial stance. Every cited anchor treated as suspect until independently Read.
Spot-checking >20% of high-stakes anchors against actual source.

(Findings appended incrementally below.)

---

## High-Stakes Anchor Spot-Checks (independently Read against source)

All anchors below were independently verified this session by Reading the actual
source files — NOT trusted from the research claims.

| Anchor (claimed by) | Claim | Source-verified result | Verdict |
|---|---|---|---|
| `fsm.py:793` (01/02/07) | `result.round_counter += 1` optimistic increment | EXACT match at :793; comment at :792 = `# Re-review attributed to our push: tick the monotonic round counter (INV-001).` | CONFIRMED |
| `fsm.py` transition INV-001 edge (02) | edge #14 `(S5_AWAITING_REREVIEW, "rereview_attributed") → S2_CLASSIFY` with INV-001 comment | EXACT at :613-614, comment `# loop-guard increments at this edge (INV-001)` present | CONFIRMED |
| `fsm.py` needs_human override (02) | pre-gate `if ctx.get("needs_human_decision"): return HALT_HUMAN` evaluated FIRST | EXACT at :574-575 | CONFIRMED |
| `fsm.py` RESOLVING edge (02) | edge #13 `(RESOLVING,"resolved")→S5_AWAITING_REREVIEW` ([MOD] target) | EXACT at :611-612 | CONFIRMED |
| `fsm.py` defensive fallback (02) | `return state` at chain end | EXACT at :619 | CONFIRMED |
| `run_log.py:27` IDEMPOTENCY_SETS (01/03/07 say 5; 05 says 4) | 5 members | EXACT 5 members at :27-33; comment :26 = `# The 5 idempotency sets (§11.4).` Members: processed_review_ids, processed_finding_ids, replied_comment_ids, resolved_thread_ids, pushed_commit_shas | CONFIRMED **5** — file 05 is WRONG |
| `models.py` EventType count (01/03/05/07) | EXACTLY 33 members | awk count = 33; class docstring :20 = "EXACTLY 33 members"; module docstring :3 = "exactly 33 members" | CONFIRMED |
| `run_log.py` ValueError "33" (03 says hardcodes "33") | error string hardcodes 33 | :109 = `(not one of the 33 §11.3 events)`; docstring :103 = "not one of the 33 closed" | CONFIRMED (line drift: 03 cited :108-110/:104, actual :109/:103 — within drift tolerance; 03 explicitly says re-grep) |
| `detection.py` DetectionContract (07) | has from_yaml + augment_bot_login, NO decline fields | augment_bot_login :64, from_yaml :75; grep for decline_phrase_regex/decline_retrigger_regex/accepted_trigger_phrases = ABSENT | CONFIRMED |
| `commands/auggie-review.md` §2 flags (07: 49/52/55/50) | depth=quick:49, post-pr:50, remediation-offer:52, auggie-model claude-sonnet-4-6:55 | ALL EXACT (depth/quick :49, post-pr default-true-for-PR :50, remediation-offer true :52, auggie-model claude-sonnet-4-6 :55) | CONFIRMED |
| `fsm.py` RunConfig _noop seam (01/02/05) | RunConfig :653-677; do_push/do_reply/do_resolve=_noop; run_validation=staticmethod(lambda) | EXACT :653-676; run_validation uses `staticmethod(lambda **_: "validated")` :673; three do_* = _noop :674-676 | CONFIRMED |
| `loop_guard.py:23` should_halt (01/02/05/07) | `should_halt(round_counter, max_rounds) -> bool` returns `>=` | EXACT :23, returns `round_counter >= max_rounds` :30 | CONFIRMED |
| `fsm.py` _noop/_default_verify/_default_apply_edits (02) | defined as seam defaults | _noop :627, _default_verify :631, _default_apply_edits :642 | CONFIRMED |
| `models.py` TERMINAL_STATES (01/03/07) | frozenset of 6 terminals | EXACT 6 members :117-126 (TERMINAL_CLEAN, HALT_MAX_ROUNDS, HALT_HUMAN, VALIDATION_FAIL, TERMINAL_TIMEOUT, TERMINAL_FAILED) | CONFIRMED |
| `models.py` MonitorState count (01) | 19 members | awk count = 19 | CONFIRMED |
| `models.py` SkillResult fields (01/03) | 10 fields | awk count = 10 | CONFIRMED |
| `classifier.py` 3-state (01/07) | STATE_POLLING/CLEAN/FINDINGS only, classify returns those 3, no is_decline | 3 STATE_* :17-19; classify returns only those :77/:83/:85/:86; no is_decline | CONFIRMED |

**Spot-check coverage:** 17 distinct high-stakes anchors independently Read against source
(>> 20% of cited anchors). Of these, 16 CONFIRMED exact; 1 (run_log ValueError) had a
~1-line drift that both research files explicitly anticipate with re-grep instructions.
**One cross-file contradiction surfaced (file 05 "4 idempotency sets") — detailed below.**

---

## Doc Cross-Validation Tag Audit (file 07)

File 07 uses `[CODE-VERIFIED]` / `[CODE-CONTRADICTED]` / `[UNVERIFIED]` tags as required.
- 11 of 12 verification-table rows tagged `[CODE-VERIFIED]`; I independently re-verified
  9 of those — all hold.
- 1 row (10b, `accepted_trigger_phrases` provenance) correctly tagged `[UNVERIFIED]` —
  the field genuinely does not exist yet (confirmed by my grep above). Properly flagged.
- ZERO `[CODE-CONTRADICTED]` claimed by file 07 — consistent with my own findings
  (no spec claim contradicts source).
- File 06 (spec index) correctly marks every code-state claim it restates with
  `*(spec claim — R7 verifies)*`, deferring HOW-verification to R7. Good discipline —
  no fabricated code-state assertions presented as verified facts.

**Verdict on tagging discipline: PASS.** All doc-sourced/spec-sourced claims are tagged or
deferred; no untagged doc claim found.

---

## Evidence Density Assessment (per file)

| File | Density | Notes |
|---|---|---|
| 01 core-modules | DENSE (>80%) | Every symbol cited file:line; explicit re-grep warning; verified counts table at end |
| 02 fsm anatomy | DENSE (>80%) | Every edge/seam line-cited; verbatim code blocks; INV-001 preservation map |
| 03 run_log/models | DENSE (>80%) | Every fold/idiom line-cited; exact mirror examples; honest "no min-fold precedent" note |
| 04 skill/refs/scripts | DENSE (>80%) | Every ref/script line-cited; flag surface cross-checked; state-machine.md MOD gap surfaced |
| 05 test-infra | ADEQUATE (60-80%) | Strong fixture/marker citations BUT contains the 4-vs-5 idempotency contradiction (below) |
| 06 spec-delta | DENSE (>80%) | Spec citations; correctly defers code-HOW to R7 with explicit tags |
| 07 doc-crossvalidate | DENSE (>80%) | Pure verification table, every row file:line + tag |

---

## CROSS-FILE CONTRADICTION (the load-bearing finding)

**Files 01, 03, 04, 07 all state IDEMPOTENCY_SETS currently has 5 members.**
**File 05 (lines 343-349) states "idempotency sets today = EXACTLY 4" and lists only 4**
(omitting `processed_review_ids`).

Source truth (verified this session, run_log.py:26-33): **5 members.** The comment at
:26 literally reads "The 5 idempotency sets (§11.4)."

File 05's own text even flags the discrepancy as a reconciliation point:
> "spec §9.1 says V1.1 adds a '6th set' — but the code has only 4 today, so either the
> spec counts differently ... **Builder MUST reconcile the '6th set' wording with R3's
> run_log source**"

This reasoning is built on a WRONG premise (4, not 5). With the correct base of 5, the
spec's "6th set" is trivially consistent (5 + auggie_review_invoked = 6). File 05's
"reconcile / maybe a 5th also lands" speculation is therefore a phantom problem that
could mislead the builder into authoring an unnecessary reconciliation item or a wrong
count assertion in the new test.

**Why this is IMPORTANT (not CRITICAL):** Files 01/03/07 (the core-source + cross-validate
tracks that OWN run_log.py) all have it right at 5, and file 03 gives the exact correct
tuple. A builder reading the run_log-owning tracks gets the right answer. But file 05 OWNS
the test-infra track — it is the file that will drive the `len(...)==6` / new-set test
assertion, so its miscount lands exactly where it can do harm (the test that enforces the
count). The contradiction is unresolved across the research set and must be corrected
before synthesis.

---

## Minor line-count / drift observations (MINOR)

- File 01 says fsm.py is 802 lines; file 02 says 803. Source = 802 (wc -l). Off-by-one,
  both files mandate re-grep, no builder impact.
- File 03 cites run_log ValueError at :108-110 + docstring :104; actual :109 + :103.
  Within stated drift tolerance.
- File 01 cites detection from_yaml at :74-89; actual def at :75. 1-line drift.
None of these affect correctness — all research files carry explicit "RE-GREP at edit
time" instructions, which is the correct mitigation.

---

## Unsupported-assertion scan

No assertion in any file was found stated as a verified code-fact without a citation,
EXCEPT file 05's "EXACTLY 4 idempotency sets" — which IS cited (`run_log.py:29-32`) but
the citation is wrong/incomplete (it points at 4 of the 5 tuple lines, skipping
:28 `processed_review_ids`). This is the worst failure mode: a confidently-cited but
inaccurate claim. All other count claims (33 events, 19 states, 6 terminals, 10
SkillResult fields, 9 DetectionContract fields, 3 classifier states) verified accurate.

File 04's state-machine.md [MOD] gap (§D) is appropriately framed as a recommendation/
risk-flag, not asserted as spec fact — it explicitly says "§6.5 omits state-machine.md
but the new edges require it — escalate as a coverage gap." Correct epistemic framing.

---

## Confidence Gate

Checklist items for evidence-quality lens (per spawn prompt):
1. [x] VERIFIED — claims are evidence-based (file:line/symbol): 6/7 files DENSE, file 05 ADEQUATE
2. [x] VERIFIED — 20%+ anchor spot-check: 17 anchors independently Read (>>20%)
3. [x] VERIFIED — unsupported-assertion scan: 1 mis-cited claim found (file 05)
4. [x] VERIFIED — [CODE-CONTRADICTED]/[UNVERIFIED] flagging in file 07: correct
5. [x] VERIFIED — cross-file contradiction detection: 1 found (4-vs-5 sets)

- **Confidence:** Verified: 5/5 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 11 | Grep: 0 (folded into Bash) | Glob: 0 | Bash: 3
  (Bash calls each ran multiple targeted greps/awks mapping to specific anchor checks;
  total verification tool calls = 14 ≥ checklist items. No web research performed —
  all claims were local-source-verifiable, so Tavily/WebSearch not engaged.)

No UNCHECKED items. No UNVERIFIABLE items.

---

## Summary

- Checks passed: 4 / 5 (evidence-density, spot-check accuracy, tag discipline, no-fabrication)
- Checks failed: 1 / 5 (cross-file contradiction unresolved: 4-vs-5 idempotency sets)
- Critical issues: 0
- Important issues: 1
- Minor issues: 3 (line drift — mitigated by re-grep instructions)
- Issues fixed in-place: 0 (fix_authorization: false)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | IMPORTANT | file 05 lines 343-349 | States "idempotency sets today = EXACTLY 4" and lists 4, omitting `processed_review_ids`. Source has 5 (run_log.py:26-33). Contradicts files 01/03/04/07. File 05 owns the test-infra track → drives the new count assertion, so the miscount lands where it can produce a wrong `len(...)` test. Its "reconcile 6th set" speculation is a phantom problem built on the wrong base. | Correct file 05 to "5 idempotency sets" with the full tuple (incl. `processed_review_ids`); delete the "code has only 4 today / maybe a 5th also lands" reconciliation speculation; restate the new count as 5 → 6. Synthesis must use 5 as the base and `len==6` post-V1.1. |
| 2 | MINOR | file 01:22 vs file 02:14 | fsm.py line count disagreement (802 vs 803). Source = 802. | Harmonize to 802 OR (preferred) both already mandate re-grep; no fix strictly required. |
| 3 | MINOR | file 03 (ValueError :108-110/:104) | ~1-line drift vs actual :109/:103. | Covered by explicit re-grep instruction; no action needed. |
| 4 | MINOR | file 01 (from_yaml :74-89) | def actually at :75. 1-line drift. | Covered by re-grep instruction; no action needed. |

## Recommendations

1. **Before synthesis:** correct file 05's idempotency-set count (4 → 5) and remove the
   phantom "6th set reconciliation" speculation. This is the one gap that can corrupt a
   downstream test assertion. Per research-gate rules, ANY gap regardless of severity =
   FAIL — this IMPORTANT contradiction must be resolved.
2. Synthesis should adopt the run_log-owning tracks (01/03/07) as authoritative for the
   idempotency-set count: **5 today → 6 after V1.1** (+`auggie_review_invoked`).
3. The MINOR line drifts need no correction — every research file already instructs the
   executor to re-grep anchors at edit time, which is the correct and sufficient mitigation.
4. Note for synthesis: file 04's state-machine.md [MOD] coverage-gap flag (§6.5 omits it
   but S5a/S5b edges require it) is a legitimate, well-reasoned finding and should be
   surfaced into Open Questions / Gap Analysis — it is NOT an evidence defect, it is a
   genuine spec-vs-design gap worth carrying forward.

---

## Overall Verdict: FAIL

**Rationale:** Evidence quality is HIGH overall — every high-stakes anchor I independently
spot-checked (17 of them, including all 8 the spawn prompt named) is accurate to the
source, tag discipline is clean, and no fabrication was found. The fsm.py:793 increment,
the INV-001 S5→S2 edge, the RunConfig _noop seam pattern, the auggie-review.md flag lines,
and the run_log "33" hardcodes are all EXACT.

**However**, research-gate rules are zero-tolerance: ANY unresolved gap or contradiction =
FAIL. File 05 carries a confidently-cited but WRONG idempotency-set count (4 vs the actual
5), it contradicts the three run_log-owning tracks, and it sits in the exact track that
will author the count test — so it is not cosmetic. It must be corrected before synthesis
proceeds. This is a single, surgically-fixable IMPORTANT issue; once file 05 is corrected
to 5 sets and the phantom reconciliation removed, the research set is green for synthesis.

## QA Complete
