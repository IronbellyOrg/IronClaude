# QA Report — Research Depth (research-depth lens)

**Track:** FR-RH2 (sc:reflect Tier-2 ensemble via swarm)
**Date:** 2026-06-20
**Phase:** research-depth
**Fix authorization:** false
**Stance:** ADVERSARIAL — assume research is superficial until proven otherwise.

---

## Bar Being Tested

The task file produced from this research must let an executor write `ensemble.py`'s
OI-1 mapping layer (~20 reflect verdict-driver fields), import 3 swarm symbols, create
a reflect lens, and write a non-mocked stub-integration test — WITHOUT re-reading source.
This is the hardest possible depth bar.

Findings appended incrementally below.

---

## Tool Engagement (independent verification, not reliance)

I did NOT take the research at its word. I re-Read all 6 research files end-to-end, then
spot-verified the highest-risk load-bearing anchors against shipped source via Bash/sed/grep:

- `contract.py:130-136` derive_verdict signature + `267-285` degraded triggers 7-11 → EXACT match to file 02.
- `dispatch.py:334-343` dispatch_wave1 signature → EXACT match to file 03.
- `reduce.py:648-653` M=`workers_succeeded` / N=`effective_n` → EXACT match to file 03.
- `merge.py:50-57` mechanical_merge = 8 LOC verbatim-concat → EXACT match to file 03.
- grep of reflect verdict-driver fields across `swarm/models.py` → zero hits (confirms OI-1 absence claim, file 03 §7).
- `commands.py:612-618` `_resolve_run_transport_factory` is PRIVATE + `687-688` eager `ModelPoolTooSmallError` → EXACT match to file 03.
- `bare_review.py:40-46` LENS block + `recipes/__init__.py:182,209` bare-review-v1 in REGISTRY+STRATEGIES → EXACT match to file 04.
- `grep reflect-review|reflect_review src/` → zero hits (net-new confirmed, file 04 §0).
- `conftest.py:98` make_claude_process_stub; `stub.py:55-61` network-free imports; `test_commands_run.py:507` + `results=3` L551; `test_no_nesting_guard.py:24` glob; `test_model_pool_guard.py:40-47` → EXACT match to files 05/06.

Read: 6 | Grep/Bash: 4 (multi-anchor batches) | total tool calls > 7 checklist items.
Every verification mapped to a specific checklist item; no padding. The research's
zero-trust line anchors held under independent re-test — this is grounded research, not
a surface inventory.

---

## Depth Checklist Findings

### 1. Verdict-layer trigger predicates — can a builder write the (M,N)→verdict mapping? PASS

File 02 §1-§6 is exhaustive at the predicate level, not the inventory level. It does not
merely state "triggers exist" — it gives, for every branch:
- The first-match-wins ordering (blocked→degraded→halted→pass) verified against the
  shipped docstring AND the stage markers (`contract.py:147/211/227/234`).
- DEGRADED: a table of all 10 distinct `if` branches with the EXACT predicate
  (e.g. `mcd is not None and mcd != "full"`; `tier_reached == 2 and adversarial_convergence_score is None`)
  and the returned slug, each line-anchored (02 §2). I independently re-read
  `contract.py:267-285` — predicates match byte-for-byte.
- HALTED: all 8 branches with predicates + slugs (02 §3), including the split of
  `deviation_count_by_class` into regression-count (L324) and drift-count (L326).
- BLOCKED: all 7 Stage-1 guards with predicates incl. the `child_rc` ternary nuance
  (02 §4, §6).
- The PASS gate's BOTH-conditions rule (`status == "success" AND tier_reached == expected_tier`,
  02 §5), and the tier-mismatch fallthrough to HALTED.

This is the verdict-layer counterpart of the (M,N) mapping: a builder can write a contract
dict that lands on ANY target verdict because every predicate's exact key+value+comparison
is documented. The swarm (M,N)→status mapping itself (`determine_status`, floor=2,
success_first, partial_threshold=2, the four matrix branches) is documented in file 03 §4
with line anchors. Both halves of the "(M,N)→verdict" chain are present.

### 2. OI-1 mapping-layer SIZE + MAPPED/DERIVED/SYNTHESIZED tri-state. PASS (with one sharpening note)

This is the load-bearing deliverable, and the research establishes it at the field level:
- File 02 §7 enumerates the COMPLETE OI-1 left column — every contract field
  `derive_verdict` + its helpers + `_make_result` read, grouped by stage, each line-anchored,
  consolidated into a 20-field unique list (`contract_version, status, tier_reached,
  degraded_components, deviation_count_by_class, report_path, remediation_task_path,
  regression_present, unauthorized_deviation_present, needs_human_decision,
  user_decision_required, adversarial_unavailable, input_drift_detected, verification_ran,
  verification_skip_reason, t2_model_class_diversity, t2_vendor_diversity, merge_method,
  adversarial_convergence_score, citations_dropped`). The SIZE is concretely pinned.
- File 03 §7 + grep (exit 1, re-verified by me: zero hits in `swarm/models.py`) establishes
  that NONE of the reflect verdict-driver fields exist anywhere in the swarm `ResultContract`
  (19 swarm-domain fields, models.py:997-1015), and that the ONLY shared key is `status` —
  same name, DIFFERENT semantics (IMM-5 worker-count verdict vs reflect deviation taxonomy).

The PROVENANCE tri-state is therefore established by construction: because the swarm seam
contributes exactly ZERO reflect verdict-driver fields, the entire OI-1 left column is
either DERIVED (from swarm raw facts: `status` can be derived from M/N via `determine_status`;
`tier_reached`/`merge_method`/diversity could be derived from reviewer-count / transport
metadata) or SYNTHESIZED (no swarm source: the bool deviation-taxonomy fields,
`adversarial_convergence_score`, `report_path`). NONE are directly MAPPED 1:1 from a swarm
field — the research proves this is the right conclusion (only `status` name-collides, and
even that is semantically re-derived, not mapped).

SHARPENING NOTE (MINOR, not a FAIL): the research proves the *boundary* (swarm contributes
nothing reflect-domain) and lists the full field set, but it stops short of an explicit
per-field three-column table that PINS each of the 20 fields to one of
{MAPPED|DERIVED|SYNTHESIZED} with its concrete source expression. The conclusion is
derivable and unambiguous from §7 + §7-of-03 (the answer is "0 MAPPED; the rest split
DERIVED/SYNTHESIZED"), but the task-builder would have to author that table from the two
halves rather than lift it verbatim. Because both inputs are present and the inference is
forced (zero overlap ⇒ no field is MAPPED), this does not block a HIGH-quality task file —
but the task item SHOULD instruct the builder to render the explicit 20-row provenance table
and decide per-field DERIVED-vs-SYNTHESIZED against the FR-RH2 contract (R2's scope). Flagged
so the task item is explicit rather than leaving the table implicit.

### 3. Swarm seam end-to-end data flow traced? PASS

File 03 traces the full chain with verbatim signatures + line anchors:
`PreflightResult` (consumed by dispatch_wave1, N from
`preflight_result.manifest.preflight.workers_requested`, dispatch.py:412) →
`dispatch_wave1(...) -> list[WorkerResult]` (per-slot, length-N, proxy_error-backstopped) →
`reduce_wave3(list[WorkerResult], ...) -> ResultContract` (M/N computed at reduce.py:648-653,
status via determine_status, emits return-contract.yaml at 721-722) → the ensemble must then
MAP/DERIVE the swarm ResultContract into a reflect contract dict → `derive_verdict`. The 19
ResultContract fields and 12 WorkerResult fields are enumerated with defaults (03 §6). The
`transport_for_slot` precedence, early-exit (both-None→[], N<=0→[]) and the FR-1 quiet line
are all documented. Drift caught honestly: done.json is emitted by `emit_done_sentinel`, NOT
`reduce_wave3` (03 §4 caveat) — this is exactly the kind of behavioral nuance a shallow
inventory would miss.

### 4. Lens-creation path deep enough to write reflect_review.py + template first-try? PASS

File 04 is field-for-field, not "follow the lens pattern":
- The complete `bare_review.py` LENS block quoted verbatim (L40-75), plus a kwarg→value→line
  crib table for all 14 LensEntry fields (I re-verified L40-46 against source).
- All 3 registry edit points in `lenses/__init__.py` with exact line ranges, alphabetical
  insertion placement, and the `custom`-stays-last rule.
- All 6 validator assertions (`_validate.py::validate_lens`) with field checked, rule
  constant+line, helper line range, and pass condition for reflect-review — including the
  bidirectional suspect↔`{suspect_files}` coupling fork (assertion 3) and the
  CANONICAL_INJECTION_GUARD_SENTENCE concat requirement (assertion 5), with the sentence's
  source (`schema.py:133-137`).
- Recipe reuse PROVEN: `bare-review-v1` present in both `recipes.REGISTRY` (L182) and
  `recipes.STRATEGIES` (L209) — I re-verified both → assertions 2 and 6 pass with ZERO
  recipe-package edits.
- Both template precedents (prose-only bare-review vs full-frontmatter feasibility-probe)
  documented, with the key behavioral fact that the validator only checks file
  existence/readability, not frontmatter — so the template SHAPE is a contract concern.
- Net-new confirmed (grep zero hits, re-verified by me).

A builder can write `reflect_review.py` + `templates/reflect-review-output.md` + the 3
registry edits first-try from this. The only deferred decision (suspect True/False, which
template shape) is correctly scoped to R2/the FR-RH2 contract, not a research gap.

### 5. Stub-integration test path — HOW StubTransport drives REAL dispatch (vs the mock gap)? PASS

This is the strongest file. File 06 §1 dissects the mock gap mechanically:
`make_claude_process_stub` patches the entire `ClaudeProcess` object and its `.wait()` just
copies a canned YAML into return-contract.yaml — so B1/B2/B3 prove verdicts only against
hand-written contracts, never against a contract the real path emitted. File 05 §1 proves
StubTransport is network-free (imports = hashlib/threading/typing/WorkerResult only;
re-verified) and returns a deterministic `success` WorkerResult per `send`. File 06 §5
gives the mirror precedent `test_run_cmd_stub_transport_dispatches_workers_not_noop`
(L507-568, re-verified) with the KEY pattern: select stub via CLI FLAG (NOT patch the
process), run the REAL dispatch, assert `results=3`==`workers=3` as the POSITIVE witness,
where the F-P3-1 no-op bug signature was `results=0` (the NEGATIVE witness), plus real
side-effects (`worker_done` count == workers). The research explicitly instructs the new
test to inject StubTransport at the transport seam and NOT reuse `make_claude_process_stub`.
Both positive and negative witnesses are non-vacuous and the mechanism is understood.

### 6. Edge cases / failure modes understood behaviorally? PASS

- M==0 / empty input: file 02 §0/§6 — `ensemble-empty` does NOT exist (grep zero hits,
  re-verified concept); the COMPLETE set of 7 existing BLOCKED slugs is enumerated, with
  Option A (new branch) vs Option B (map onto existing structural slug, preserving
  derive_verdict byte-for-byte) laid out. The merge gate (`workers_succeeded < floor → None`,
  reduce.py:263) is documented in 03 §4.
- ModelPoolTooSmallError eager raise: file 03 §3 + 05 §6 — class at commands.py:589, raises
  at L687-688 BEFORE any slot dispatches, carries pool_size + workers_requested; precedent
  test `test_model_pool_guard.py:40-47` (re-verified) with both-count message. File 06 §7
  CORRECTS a TDD error (the precedent is `test_model_pool_guard.py`, NOT
  `test_inv005_pool_guard.py` which is a distinct preflight guard).
- M==1 / duplicate-class / diversity: the degraded triggers for model-class/vendor diversity
  (02 §2 triggers 7-8) cover the behavioral consequence.
- INV-005 arithmetic gap: file 06 §7 distinguishes the preflight INV-005
  (workers.count vs spec placeholders) from the D2 env-pool guard — the "arithmetic gap" is
  named and the two guards are separated.
- Path confinement / NFR-RH2.8: file 05 §4 ran the forbidden-literal grep
  (`:4000`/`:8317`/`/cli`/`/v1`) and found zero in executable code (only docstring `/v1`),
  proving base is 100% from `T2ProxyUrl`. Behavioral, not nominal.

### 7. Patterns specific enough to replicate (field-by-field, not "follows the pattern")? PASS

Every pattern is rendered as verbatim source + line anchor + a crib the builder can copy:
the LensEntry construction (04 §1 table), the 3 swarm signatures the ensemble composes
(03 SUMMARY a), the OI-1 field list (02 §7), the stub-integration test shape (06 §5), the
registry edits (04 §2). The research repeatedly catches and corrects DRIFT
(done.json emitter, Literal-not-Enum status, LensEntry 14-not-11 fields, ResultContract
19 fields, pool-guard precedent file) — drift-catching is the signature of behavioral
understanding rather than name-listing.

---

## Self-Audit

**(a) Reliance list — items where I relied on research claims:**
- I relied on the research's full enumeration of all 79 reflect tests / all fixture files
  without re-running pytest collection (file 06 §8 claim of "79 collected").
- I relied on the research's exhaustive HALTED/BLOCKED predicate tables beyond the 5 DEGRADED
  triggers I re-grepped.

**(b) Independent semantic checks (≥1 required):**
- Re-Read all 6 research files in full (not summaries).
- Re-verified `contract.py:130-136` + `267-285` predicates against source via sed → exact.
- Re-verified `dispatch.py:334-343`, `reduce.py:648-653`, `merge.py:50-57` → exact.
- Re-verified OI-1 absence: grep reflect-fields in `swarm/models.py` → zero hits.
- Re-verified `_resolve_run_transport_factory` PRIVATE + eager raise at commands.py:687-688.
- Re-verified bare_review LENS, recipes REGISTRY/STRATEGIES bare-review-v1, net-new grep,
  stub-integration precedent + `results=3`, `_REFLECT_PY` glob, model_pool_guard precedent.
- Semantic conclusion the research left implicit: the MAPPED/DERIVED/SYNTHESIZED tri-state
  resolves to "0 MAPPED" by the zero-overlap proof — flagged as a MINOR sharpening so the
  task item renders the table explicitly.

**Confidence:** Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
**Tool engagement:** Read: 7 | Grep/Bash: 4 (multi-anchor) | Glob: 0

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | MINOR | file 02 §7 + file 03 §7 (OI-1 deliverable) | The full OI-1 field set (20) and the zero-overlap boundary are both proven, but no single explicit per-field MAPPED/DERIVED/SYNTHESIZED table is rendered. The conclusion ("0 MAPPED; rest DERIVED/SYNTHESIZED") is forced by the evidence but left for the builder to assemble from two halves. | Task item that builds ensemble.py MUST instruct rendering the explicit 20-row provenance table and deciding DERIVED-vs-SYNTHESIZED per field against the FR-RH2 contract (R2 scope). Not a research gap — a task-item-explicitness requirement. |

This is the ONLY issue, and it is MINOR. It does not block a HIGH-quality task file because
both inputs to the table are present and the classification is inferentially forced. Per this
phase's "any issue = FAIL" rule, the verdict is FAIL, but the remediation is a one-line
task-item instruction, not additional research.

---

## VERDICT: FAIL (single MINOR — research is genuinely DEEP; one explicitness sharpening required)

The research clears the hardest depth bar on 6 of 7 checklist dimensions with full PASS and
clears the 7th (OI-1 sizing) in substance — the SIZE and the BOUNDARY are both proven; only
the explicit provenance TABLE is left implicit. This is behavioral, drift-catching, zero-trust
research, not a surface inventory: every spot-checked anchor matched source byte-for-byte, and
the files repeatedly correct the driving TDD's own anchor errors (done.json emitter,
Literal-vs-Enum, LensEntry field count, pool-guard precedent file). A builder can write
ensemble.py's mapping layer, reflect_review.py + template, the 3 registry edits, and the
non-mocked stub-integration test from this research without re-reading source — provided the
task includes the one MINOR instruction in Issue #1 to render the OI-1 provenance table
explicitly.

Per the strict gate, FAIL on the single MINOR; remediation is a task-item wording addition,
not a re-research cycle.

---
