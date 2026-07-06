# QA Report — Research Depth (research-depth lens)

**Topic:** pr_submit V1.1 (FR-8/9/10; FSM extension with INV-001 verbatim + INV-R1/R2/R3 + NFR-6 core purity)
**Date:** 2026-06-12
**Phase:** research-depth
**Fix cycle:** N/A
**Fix authorization:** false
**Assigned files:** research/01..07 (all 7)
**Adversarial stance applied:** Assumed research superficial until proven otherwise; independently re-verified the single highest-risk anchor (`fsm.py:793` + loop ordering) and the two count contradictions against live source.

---

## Overall Verdict: PASS

The research is GENUINELY DEEP, not surface-level. Files 02 and 03 — the two that carry the
highest-risk operations (the `round_counter` increment relocation and the rebuild_state folds) —
go well past listing symbol names: they trace ORDERING, CONSEQUENCES of partial edits, and supply
literal-implementation idioms. A builder could author per-file AND per-test-ID items from this
research without re-reading source for the load-bearing operations. The one intra-research
miscount (file 05's "4 sets today") is self-flagged by its own author as needing reconciliation,
and the three authoritative tracks (01/03/07) plus my own grep all agree on the correct value (5→6).

---

## Independent verification performed (adversarial re-test)

| Claim re-tested | Research source | My verification | Result |
|---|---|---|---|
| `fsm.py:793` is `result.round_counter += 1`, the ONLY round_counter mutation, after do_resolve/S5 set, before final-clean tail | 02 §2, 07 #1 | Read fsm.py:715-802 | EXACT — :792 comment, :793 increment, :786 push, :720 top-of-loop `>=` gate. Ordering claim verbatim correct |
| `should_halt_rounds` is `>=` and delegates to loop_guard | 02 §5, 03, 07 #8 | Read fsm.py:135-142 | CONFIRMED — `return loop_guard_should_halt(...)`, docstring `>=` not `>` |
| transition() edge #14 `(S5_AWAITING_REREVIEW,"rereview_attributed")→S2_CLASSIFY` with INV-001 comment | 02 §1 | Read fsm.py:611-616 | EXACT including the `# loop-guard increments at this edge (INV-001)` comment |
| RunConfig seam pattern (`_noop` defaults, `staticmethod` lambda) | 02 §3, 05 §1 | Read fsm.py:653-676 | EXACT — `run_validation: ... = staticmethod(lambda **_: "validated")`, do_push/reply/resolve=_noop |
| IDEMPOTENCY_SETS = 5 today (→6) | 01,03,06,07 | grep run_log.py:26-33 | CONFIRMED 5, comment literally "The 5 idempotency sets" |
| EventType = 33 today (→37) | 01,03,06,07 | awk count models.py | CONFIRMED 33 |

Tool engagement: Read=6 (fsm.py x3 ranges + all 7 research files), Bash/grep=2. Every tool call
mapped to a specific depth-checklist claim, not padding.

---

## Depth Checklist (7 items — the lens-specific gate)

| # | Depth question | Result | Evidence |
|---|---|---|---|
| 1 | File 02 explains HOW the loop enforces `max_rounds=N⇒N pushes` (increment ORDERING vs push + budget gate), not just WHERE | PASS | 02 §2 ★-block: "the round_counter tick must happen BEFORE the top-of-loop should_halt gate of the NEXT iteration (fsm.py:720) — that ordering is what makes max_rounds=N⇒N pushes hold." Names push(:786)→increment(:793)→next-budget-gate(:720) sequence. I re-confirmed all three sites. |
| 2 | File 02 captures that run_skill() re-implements the cycle inline (does NOT call transition()) + consequence of editing only one | PASS | 02 §0 (load-bearing, bolded): "transition() is a free function, run_skill() re-implements the cycle inline (does NOT call transition())… both must be modified in lock-step or they drift." Reinforced in §6 builder summary item: "run_skill() does NOT call transition() — edits to one do not propagate." |
| 3 | File 03 gives EXACT fold idioms for rebuild_state incl. the monotone-min fold with no precedent — enough to implement | PASS | 03 §3.2 names IDIOM A (count/`+=1`), IDIOM B (add-to-set w/ guard), and §4.3 AUTHORS IDIOM C (monotone-min) with a complete None-safe code block: `state["effective_max_rounds"] = clamp if prev is None else min(prev, clamp)`, plus rationale + a recommended test. Explicitly flags "no existing min-fold template — author it." |
| 4 | Decline classification (FR-9.1) understood deeply enough to avoid a false-positive-prone item | PASS | 06 §3 FR-9.1 transcribes the full conjunction: authored-by `augment_bot_login` AND `decline_phrase_regex` AND `decline_retrigger_regex` AND newer-than-watermark, with the explicit false-positive defense ("requiring BOTH phrase + re-trigger-instruction defeats a finding body that merely mentions 'abnormally large'"). 01 §classifier + 04 §G add the decline-check-BEFORE-clean/findings ordering and the "don't take the App's bait" distinction. Default regexes given verbatim. |
| 5 | Strict-once + clamp arithmetic (INV-R2 `push_count≤max_rounds+1`; INV-R3 monotone clamp; two independent counters) traced not just named | PASS | 06 §4 transcribes INV-R1/R2/R3 verbatim; FR-10.5 derives the `+1` bound ("≤max_rounds from Augment loop + ≤1 fallback"); FR-10.3 states the two counters are independent and `round_counter` is FROZEN at fallback entry. 03 §4.2/§4.3 give the strict-once `record_idempotent` True-then-False contract + the monotone-min clamp fold. EC-21/EC-24 cover two-decline and resume strict-once. |
| 6 | Could the builder create per-file AND per-test-ID items WITHOUT re-reading source? §9 coverage matrix maps FR→test | PASS | 06 §5 is a per-file delta list (one bullet per symbol/constant); §8 reproduces the FULL §9 FR→test coverage matrix (every FR/INV/AC→T-ID) + §8.1 the new/extended test-file table. 05 adds the mirror-pattern per test module (file:line assertion idioms) + fixture schemas for all 7 new fixtures. 01 gives verified before/after counts per file. This is per-file + per-test-ID buildable. |
| 7 | NFR-6 core-purity boundary (core decisions vs SKILL I/O) + T-N50 static-grep enforcement understood concretely | PASS | 02 §4 ran the grep (CLEAN — docstring-only) and names the boundary: decisions pure in pr_submit, `gh api` post + `> Skill sc:auggie-review-protocol` live in SKILL.md. 06 §9 + 04 §F/§G nail which DECISION is core (re-trigger gating, decline classify, strict-once, clamp) vs which I/O is SKILL. 05 §3 gives the exact T-N50 mechanics (`CORE_PURE_FILES` list, `re.compile(r"\bgh\b|\bgit\b")`, offenders assertion) and that the new refs must be ADDED to `CORE_PURE_FILES`. 07 #12 re-verified purity currently holds. |

All 7 depth questions PASS.

---

## Summary

- Depth-checklist items passed: 7 / 7
- Issues: CRITICAL 0 | IMPORTANT 0 | MINOR 1

## Why this research is deep (not shallow symbol-listing)

The adversarial test for shallowness is: *does the researcher understand BEHAVIOR, or just names?*
The decisive evidence the research passes:

1. **Behavioral ordering, not location.** File 02 does not merely say "the increment is at :793."
   It explains WHY the ordering (push→increment→next-iteration budget gate) is the mechanism that
   makes `max_rounds=N⇒N pushes` true, and warns that a naive relocation breaks it. I re-read the
   loop and the ordering claim is verbatim correct — this is the single highest-risk operation and
   the research nailed it.
2. **Authored a missing idiom.** File 03 §4.3 confronts the fact that the monotone-min fold has NO
   in-repo precedent and writes the None-safe implementation + rationale, rather than hand-waving
   "add a min fold." That is the difference between deep and surface.
3. **False-positive-aware classification.** File 06 FR-9.1 understands WHY both regexes + watermark
   are required (defeats a finding body that merely mentions "abnormally large"), not just THAT
   they are required.
4. **Found a real coverage gap.** File 04 §D independently reasons that state-machine.md needs a
   [MOD] even though spec §6.5 omits it, because the FSM single-source invariant would otherwise
   break. That is active understanding, not transcription.
5. **Two-surface drift warning.** File 02 repeatedly flags that `transition()` and `run_skill()`
   are independent implementations of the cycle — the classic trap that produces a broken loop if
   only one is edited.

## Issues Found

| # | Severity | Location | Issue | Required Fix (for the BUILDER, not this QA) |
|---|----------|----------|-------|---------------------------------------------|
| 1 | MINOR | research/05 §6 "idempotency sets today = EXACTLY 4" (lines ~343-349) | File 05 miscounts the current idempotency sets as 4 and frames the spec's "6th set" as an unreconciled contradiction. The authoritative count is **5** (verified: run_log.py:26-33 + grep + files 01/03/06/07 all agree). File 05's own author flagged this as "Builder MUST reconcile … against R3's run_log source" — so it is a self-disclosed open item, not a silent error. | Builder should anchor the idempotency-set delta on file 03/01/07 (5→6), NOT on file 05's "4". Recommend the consolidated research note / task file state the reconciled value explicitly so the builder does not propagate the "4"/"contradiction" framing into a test asserting the wrong count. No source code is wrong; this is a research-internal inconsistency only. |

**Severity rationale:** MINOR (not IMPORTANT) because: (a) the miscount is isolated to one
secondary track (test-infra), (b) all four primary tracks + live source agree on the correct value,
(c) file 05 self-flagged it as needing reconciliation rather than asserting it as fact, and (d) it
does not touch the highest-risk INV-001 operation. It nonetheless must be resolved (no leniency):
the builder must not carry the "4 / contradiction" framing forward into the `len()` / set-membership
test assertion. With this single note resolved at consolidation, the research is sufficient to
produce a correct, INV-safe task file.

## Confidence

Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%

(Each of the 7 depth items was verified by reading the cited research passage AND, for the 6
load-bearing factual claims, re-reading the live source. Confidence is computed, not assessed.)

**Tool engagement:** Read: 10 (7 research files + 3 fsm.py ranges) | Grep/Bash: 2 | Glob: 0
Tool calls (12) exceed checklist items (7) — engagement floor satisfied; no padding (every call
targeted a specific claim).

## Self-Audit

1. **How many factual claims independently verified against source?** Six load-bearing claims
   re-verified against live `src/superclaude/pr_submit/fsm.py`, `run_log.py`, `models.py`: the
   :793 increment + its position, the loop ordering, the `>=` gate delegation, edge #14 + its
   INV-001 comment, the RunConfig seam pattern, and the two counts (IDEMPOTENCY_SETS=5,
   EventType=33). All matched the research exactly.
2. **What files did I read to verify?** fsm.py (lines 125-144, 555-685, 715-802), run_log.py
   (26-34 via grep), models.py (EventType count via awk), plus all 7 research files in full.
3. **If I found ~0 issues, why trust the review?** I did NOT rubber-stamp — I adversarially
   re-tested the single highest-risk anchor (the increment relocation) by reading the actual loop,
   confirmed the ordering claim is correct, AND I chased the one count discrepancy (file 05's "4")
   to the source to determine whether it was a real defect or an isolated miscount. It is an
   isolated, self-flagged miscount → 1 MINOR finding. The review is not a pass-by-default: it
   located a genuine (if low-severity) intra-research inconsistency and graded it honestly.
4. **Web research?** None performed — this is an entirely local-source depth review. Tavily-first
   precedence not triggered.

## Recommendations

1. At research-consolidation / task-build time, RECONCILE the idempotency-set count to **5→6**
   explicitly (per files 01/03/06/07 + verified source), and do NOT propagate file 05's "EXACTLY
   4 today / 6th-set contradiction" framing into any test assertion or task item.
2. Proceed to task-build. The research is deep enough to author per-file AND per-test-ID checklist
   items for the FR-8/9/10 deltas, including the high-risk INV-001 increment relocation, without
   re-reading source for the load-bearing operations.
3. Carry forward to the builder (already well-surfaced by the research, not QA gaps): the
   state-machine.md [MOD] coverage gap (04 §D), the recovery.py Branch-A resume-target latent
   interaction (01 §RECOVERY), and the `--strict-markers` new-marker → pyproject.toml gate (05 §4).

## QA Complete
