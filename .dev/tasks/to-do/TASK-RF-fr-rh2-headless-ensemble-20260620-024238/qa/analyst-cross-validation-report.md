# Cross-Validation Report — FR-RH2 Research (sc:reflect Tier-2 ensemble via swarm dispatch)

**Analysis type:** completeness-verification
**Lens:** cross-validation (between research files AND against driving spec/TDD)
**Date:** 2026-06-20
**Assigned files:** 01..06 (all six research files)
**Output:** this file

---

## Methodology

Read all six research files plus the driving spec.md (oracle) and tdd.md. Cross-validated
claims where two researchers touch overlapping surfaces. Verified each reported TDD drift
correction is internally consistent and anchored to a current file:line (not the stale TDD
anchor). Verdict appended at the end.

**Driving docs located and read (zero-trust against shipped):**
- spec.md → `.dev/reflect-hardening/issue-2-headless-ensemble/spec.md` (49,436 bytes)
- tdd.md → `.dev/reflect-hardening/issue-2-headless-ensemble/tdd.md` (203,387 bytes)

Both present at the paths research-notes.md cites. §15 test matrix, §22 Q1/Q6, §5.3 (M,N)
table, §4.6 order, §8.3 OI-1 table all confirmed present in the TDD/spec and cross-checked
against the six research files.

---

## Checklist Item 1 — Cross-file consistency on shared symbols

### 1a. LensEntry field count: R3 says 14 — R4 agrees
- **R3 §6d** pins `LensEntry` (DM-010) at **14 fields**, models.py:707-720, listed in order
  (name, description, system_prompt_fragment, user_template, output_template_path, recipe_name,
  normalizer_strategy, default_workers, default_target_line_cap, suspect, tier,
  recommended_next_command_template, acceptance_notes, stability).
- **R4 §1** documents the `bare_review.py` call-site, which passes all 14 kwargs verbatim
  (L40-75), and R4 explicitly defers the dataclass field/default authority to R3 (R4 NOTE at
  L124-127: "R3 owns the dataclass field/default verification"). R4's field-by-field crib
  table enumerates the same 14 kwargs.
- **CONSISTENT.** R3 (14 fields, dataclass) and R4 (14 kwargs, call-site) agree. R3 additionally
  flags the brief's "11 load-bearing fields" undercount as a drift (description,
  default_target_line_cap, acceptance_notes omitted from the brief) — this is a brief-vs-code
  correction, not an R3/R4 contradiction. No conflict. **PASS.**

### 1b. FR-6 PASS→BLOCKED location: R1 says run() L588-590 — R6 agrees
- **R1 §2 + DRIFT findings** place the PASS→BLOCKED demotion in `run()` at **runner.py:588-590**,
  NOT inside `write_reflect_post` (R1 flags this as a "NUANCE, not drift": write_reflect_post
  only RETURNS the non-"written" status; the demotion is in the caller).
- **R6 §4** (B3 row + B2 row) independently describes "FR-6 fail-closed write-back downgrades"
  and B2 pinning "FR-6 fail-closed write-back" — consistent with the demotion living in the
  runner's `run()` path that B2 exercises end-to-end. R6 does not contradict the L588-590 anchor.
- **CONSISTENT.** R1 owns the precise anchor (L588-590); R6 references the same behavior from the
  test side without disagreement. **PASS.**

### 1c. Retry/backoff location: R5 says dispatch.py not transport — R3 is the owning lane
- **R5 §5** states the retry-once-on-5xx + 2s-backoff matrix is **NOT** in the transport: the
  transport records a single-attempt outcome (`attempts=1`, openai_compat.py:399,134) and the
  retry policy "wraps send externally (dispatch — R3's lane)". R5 cites the openai_compat
  docstring (L50-53) attributing retry to `retry_policy` wrapping the send call. R5 explicitly
  hands the retry/backoff arithmetic to R3 ("the retry/backoff arithmetic itself is in
  dispatch.py (R3)").
- **R3** documents `dispatch_wave1` (dispatch.py:334-343) as the fan-out owner but does NOT itself
  enumerate the retry-once/backoff arithmetic line anchors in its body. This is a **COVERAGE
  SEAM, not a contradiction**: R5 correctly points retry to dispatch.py/R3's lane, and R3 owns
  dispatch.py — but neither file pins the exact retry_policy line anchor. See Gap G2 below.
- **CONSISTENT (no contradiction), but a shared-surface coverage gap exists** (G2). **PASS with
  a noted gap.**

---

## Checklist Item 2 — OI-1 field list reconciliation (R2 left-column vs R3 absence proof)

- **R2 §7** ("OI-1 LEFT COLUMN") enumerates the **20 consolidated unique fields** that
  `derive_verdict` (+ its helpers `_degraded_reason`, `_halted_reason`, `_make_result`,
  `_extract_deviations`) read: contract_version, status, tier_reached, degraded_components,
  deviation_count_by_class, report_path, remediation_task_path, regression_present,
  unauthorized_deviation_present, needs_human_decision, user_decision_required,
  adversarial_unavailable, input_drift_detected, verification_ran, verification_skip_reason,
  t2_model_class_diversity, t2_vendor_diversity, merge_method, adversarial_convergence_score,
  citations_dropped. Each with a contract.py:LINE anchor.
- **R3 §7 + grep** confirms that of the swarm-side verdict drivers (`tier_reached`,
  `merge_method`, `t2_model_class_diversity`, `t2_vendor_diversity`, `reviewer_count`,
  `adversarial_convergence_score`), **ALL are ABSENT** from the swarm `ResultContract` (DM-012,
  19 fields models.py:997-1015) — grep exit 1, zero hits across all 5 swarm files. The ONLY
  shared key name is `status` (different semantics: IMM-5 worker verdict vs reflect tier check).
- **RECONCILIATION — CONSISTENT and TOGETHER SIZE THE MAPPING LAYER.** R2 says "these 20 fields
  must be produced for `derive_verdict`"; R3 says "the swarm contract supplies NONE of them
  except `status`". This matches the TDD §8.3 "sizing conclusion" (tdd.md:794): of ~22 reflect
  verdict-driver fields, exactly one (`status`) has a same-named swarm key (needs re-mapping),
  `reviewer_count` maps from `workers_succeeded` (M), `merge_method`/`t2_model_class_diversity`/
  `t2_vendor_diversity` are derived/computed, and **every remaining field is synthesized or
  defaulted in `ensemble.py`**. R2's left column (20 fields) ∩ R3's absence proof = the full
  `ensemble.py` mapping layer. **No contradiction. The two halves of OI-1 are internally
  consistent and consistent with TDD §8.3. PASS.**
- Minor note: R2 lists 20 consolidated fields; TDD §8.3 says "~22 reflect verdict-driver fields".
  The delta is accounting (R2 collapsed the 7 load-bearing booleans into the unique-field list and
  did not separately count `expected_tier`/`allow_single_vendor` kwargs which are caller-supplied,
  not contract-sourced). Not a contradiction — R2 is counting contract-dict keys, TDD is counting
  verdict drivers inclusive of kwargs. Both agree the swarm side supplies ~1.

---

## Checklist Item 3 — Q6 grep gives unambiguous Option A vs Option B basis

- **R2 §0** ("Q6 GREP RESULT — read this first"): `grep -rn "ensemble-empty" src/superclaude/cli/
  reflect/` → **ZERO matches**; `grep -rn "ensemble" .../contract.py` → ZERO. Confirmed: the slug
  `ensemble-empty` does NOT exist; the substring `ensemble` is entirely absent from contract.py.
- **R2 §6** enumerates the **complete** existing BLOCKED slug set (the Option B landing targets):
  `{timeout, child-crash, contract-missing, contract-version-missing, unknown-major-version,
  malformed-degraded-components, malformed-contract-boolean}` — all structural (child process /
  contract file integrity), each with a contract.py:LINE. `ensemble-empty` is confirmed not among
  them.
- **Option A vs Option B basis — UNAMBIGUOUS:**
  - **Option A** = add a NEW `ensemble-empty` BLOCKED branch in `derive_verdict`/`_make_result`.
    R2 §0 correctly states this is a net-new edit to the verdict-derivation path.
  - **Option B** = have `ensemble.py` synthesize an empty/None contract so an EXISTING Stage-1
    structural guard fires (e.g. `contract-missing` / `malformed-*`), leaving `derive_verdict`
    byte-for-byte unchanged.
- **FR-RH2.7 impact of each option is clearly derivable.** FR-RH2.7 = "verdict map + exit codes
  unchanged; downstream return-contract consumers unaffected" (spec L295, L137; TDD U6/B1 rows).
  - Option B PRESERVES FR-RH2.7 literally (derive_verdict untouched; cost = a less-specific slug).
  - Option A is a DELIBERATE AMENDMENT to FR-RH2.7's "derive_verdict unchanged" claim (exit-code
    map + 4-state vocabulary stay intact, but the derivation path is modified) — must be called
    out as such, NOT a no-cost rename. This is exactly how TDD §22 Q6 (tdd.md:1533) frames it.
- **CONSISTENT and ACTIONABLE. PASS.** The research-notes.md AMBIGUITIES_FOR_USER section (L96)
  and R2 §0 both correctly treat Q6 as a **human-decision HALT** (do not auto-pick Option B),
  matching project policy (`feedback_human_decision_items_must_halt`). The grep gives an
  unambiguous, evidence-backed basis for the human to choose. See CONTRADICTION C1 below for the
  one place the TDD pre-commits to a slug while Q6 is still open.

---

## Checklist Item 4 — Drift reconciliation (each reported TDD drift, corrected fact + anchor)

Each drift below is verified internally consistent across the research files AND anchored to a
**current shipped file:line** (so the task cites the corrected anchor, not the stale TDD one).

| # | Reported drift | Corrected fact + CURRENT anchor | Owning file | Consistent? |
|---|---|---|---|---|
| D1 | FR-6 PASS→BLOCKED location | Demotion is in `run()` at **runner.py:588-590**, NOT inside `write_reflect_post` (which only returns the non-"written" status, runner.py:148/182). | R1 §2/DRIFT; R6 B2/B3 | YES — see Item 1b |
| D2 | max_turns default location | `_DEFAULT_MAX_TURNS = 250` at **config.py:39** (resolved config.py:230); runner.py is default-free, passes `config.max_turns` through (runner.py:411). Any TDD anchor placing 250 in runner.py is DRIFT. | R1 §2 | YES |
| D3 | done.json emitter | `reduce_wave3` does NOT emit done.json — it emits only `merged.md` + `return-contract.yaml` (reduce.py:686-689, 721-722). done.json is written by the SEPARATE `emit_done_sentinel(terminal_status, contract_path)` at **reduce.py:402** (DONE_SENTINEL_FILENAME, target `contract.parent / "done.json"` reduce.py:456). | R3 §4/§(c) | YES — R3 self-consistent; matches TDD I9 which asserts done.json *shape* (DM-017) without attributing emission to reduce_wave3 |
| D4 | mechanical_merge size | **8 LOC** (signature + 7-line body), merge.py:50-57, under the ≤30 ceiling. | R3 §5; R6 §6 (test_merge_loc_ceiling LOC_CEILING=30) | YES — R3 (source) + R6 (test) agree |
| D5 | recipes anchors L181/L209 | `REGISTRY` HEADER at L181, `bare-review-v1` KEY at **L182**; `STRATEGIES` header L208, key at **L209**. R4 corrects the TDD's L181/L208 (header lines) to the actual key lines L182/L209. | R4 §4 | YES — R4 internally consistent; reuse with zero recipe edits confirmed |
| D6 | no-nesting guard L80-143 + agent-check runner-only | Full guard is 6 tests spanning **L80-143** (TDD "L95-102" is only Layer-B test #2). The `anthropic`/`subagent`/`Task(` agent-surface check is **runner.py-only** today (test #2, via `_RUNNER_SRC` L22); package-wide loops (#3 L108, #4 L122) iterate `_REFLECT_PY` glob (L24) and AUTO-cover ensemble.py for sprint/roadmap + async/await. Explicit agent-surface guard for ensemble.py is the edit FR-RH2 (U7) wants. | R6 §3 | YES — matches TDD U7 (tdd.md:1168) which says "looped over [runner.py, ensemble.py]" |
| D7 | U4 precedent file | U4's `ModelPoolTooSmallError` precedent is **`tests/swarm/test_model_pool_guard.py:40-47`** (eager raise naming both counts: `err.pool_size==2`, `err.workers_requested==3`), NOT `test_inv005_pool_guard.py` (which is the preflight `PreflightError`/`workers-exceed-pool` guard — a DISTINCT guard with no `ModelPoolTooSmallError`). | R6 §7 | YES — R6 grep-verified the class is in commands.py:589, tested by test_model_pool_guard.py |

- **ALL SEVEN DRIFTS are internally consistent across files and anchored to current shipped
  file:line.** Where two files touch the same drift (D1: R1+R6; D4: R3+R6) they agree. **PASS.**
- One additional consistency check: R3's D3 (done.json) does NOT contradict TDD I9 (tdd.md:1194),
  which asserts the done.json *shape* exists at terminal status (DM-017) — it never claims
  `reduce_wave3` is the emitter. So correcting the emitter to `emit_done_sentinel` is compatible
  with the I9 test as written. No conflict.

---

## Checklist Item 5 — Spec-vs-TDD authority conflicts (does spec or TDD win on any point?)

Build rule (research-notes L15): **spec wins on wording; TDD governs file paths / signatures /
§15 test matrix.** Checked for any place a research file applies the wrong authority:

- **No research file inverts the build rule.** R1-R6 consistently treat the TDD as the authority
  for file paths, signatures, line anchors, and the §15 matrix, and defer wording/verdict-policy
  to the spec. The research-notes explicitly encodes this (L15-16).
- **The one substantive spec↔TDD tension is the `ensemble-empty` slug** (see C1 below). Here the
  spec §5.3 (M,N) table (spec.md:448) and the TDD (M,N) tables (tdd.md:311/379/910/952/1109) BOTH
  name `ensemble-empty` as the M==0 slug — so spec and TDD AGREE on the *vocabulary*. The conflict
  is NOT spec-vs-TDD; it is **(spec+TDD vocabulary) vs (shipped contract.py reality + FR-RH2.7's
  "derive_verdict unchanged")**, which is precisely what Q6 exists to reconcile. The TDD itself
  flags this (tdd.md:1124, 952: "slug reconciliation — see §22 Q6"). So the research correctly
  routes it to a human-decision, not a spec-vs-TDD precedence call.
- **`status` semantics** — both R3 and TDD §8.3 agree the shared `status` key has different
  semantics on each side; no authority conflict, just a mapping requirement. Consistent.
- **PASS.** No research file mis-assigns spec/TDD authority. The build rule is honored throughout.

---

## Checklist Item 6 — §15 test-matrix items (U1-U9, I1-I9, B1-B3) research grounding

Verified each matrix row (tdd.md:1162-1212) has a research-backed grounding (precedent file /
target file / assertion). Spot-checked all 21 rows against the six research files:

| Row | TDD assertion | Research grounding | Grounded? |
|---|---|---|---|
| U1 | reflect-review lens registers + passes validator | R4 §1-§3 (lens crib + 6 validator assertions + 3 registry edit points) | YES |
| U2 | default_workers ∈ [2,4]; no hard-coded Claude model | R4 §1 (bare-review default_workers=3 precedent); R3 §6d (LensEntry.default_workers field) | YES |
| U3 | slot i → distinct T2Model0N (pool[i%len]) | R3 §2 (commands.py:692 binding); R5 §6 (per-slot factory) | YES |
| U4 | ModelPoolTooSmallError eager at build | **R6 §7** (corrected precedent test_model_pool_guard.py:40-47); R3 §3 (raise at commands.py:688) | YES (corrected) |
| U5 | diversity from distinct proxy model_ids, NOT alias count | R3 §6a (WorkerResult.model_id field); R2 (t2_model_class_diversity read at contract.py:267) | YES |
| U6 | derive_verdict map unchanged (0/10/11/2) | **R2 §1/§5** (ordering + PASS gate); R6 B1 (test_verdict_mapping.py direct calls) | YES |
| U7 | no-nesting guard extended to ensemble.py | **R6 §3** (glob auto-cover + explicit agent-surface edit) | YES |
| U8 | swarm merge stays ≤30 LOC scoring-free | **R3 §5** (8 LOC); R6 §6 (test_merge_loc_ceiling + test_merge_mechanical_only) | YES |
| U9 | no forbidden :4000/:8317/v1/cli literal | **R5 §4** (grep result, all /v1 in docstrings only) | YES |
| I1 | positive witness ≥2 reviewers, stub, no ClaudeProcess patch | **R6 §5** (test_run_cmd_stub precedent L507-568); R5 §1 (StubTransport) | YES |
| I2 | negative witness 1 reviewer → DEGRADED | R6 §5 (falsifiable-witness pattern); R2 §2 (single-reviewer-fallback trigger 10) | YES |
| I3 | 2-of-3, 2 distinct classes → PASS-eligible | R3 §4 (M=workers_succeeded); R2 (diversity full) | YES |
| I4 | 2-of-3 duplicate classes → degraded-model-diversity | R2 §2 (trigger 7, contract.py:267-269) | YES |
| I5 | M==1 from N>1 → single-reviewer-fallback | R2 §2 (trigger 10) | YES |
| I6 | M==0 → BLOCKED exit 2, reason ensemble-empty | R2 §0/§6 (slug absent; Option A/B); **see C1** | PARTIAL (slug unresolved — C1) |
| I7 | return-contract shape preserved | R2 §5/§7; R1 §2 (write_reflect_post/sidecar) | YES |
| I8 | path-confinement (only <output_dir>/return-contract.yaml) | R2 §5 (parse_contract); spec §5.3 path_confinement (spec.md:441) | YES |
| I9 | done.json shape (DM-017) | **R3 §4/§6c** (emit_done_sentinel + DoneSentinel DM-017) | YES |
| B1 | test_verdict_mapping.py (276 L) green unmodified | R6 §4 (B1 row, no ClaudeProcess patch) | YES |
| B2 | test_runner_e2e.py (220 L) green unmodified | R6 §4 (B2 row, patches ClaudeProcess — the canary) | YES |
| B3 | test_writeback.py (172 L) green unmodified | R6 §4 (B3 row) | YES |

- **20 of 21 rows are fully grounded.** I6 is grounded on the *mechanism* (M==0 → blocked → exit 2,
  fully backed by R2 + spec/TDD (M,N) tables) but its *slug assertion* (`ensemble-empty`) is
  unresolved pending Q6 (C1). **PASS with one conditional row (I6) flagged.**

---

## Contradictions Found

### C1 (IMPORTANT — must be surfaced, do NOT resolve silently): TDD I6 pre-commits to `ensemble-empty` while §22 Q6 is still OPEN
- **TDD §15 row I6** (tdd.md:1191) asserts the expected verdict: "reason `ensemble-empty` (per
  §22 Q6)". The spec §5.3 (M,N) table (spec.md:448) and TDD (M,N) tables likewise name the slug.
- **TDD §22 Q6** (tdd.md:1533) is marked **🔴 Open** — the slug choice (Option A add-new-branch
  vs Option B map-onto-existing) is an explicit, unresolved human-decision; R2 §0 + the shipped
  grep confirm `ensemble-empty` does NOT exist in contract.py today.
- **The contradiction:** the test matrix (I6) hard-asserts a slug that the open decision item
  (Q6) says may not exist (under Option B, the slug would be an existing structural one like
  `contract-missing`/`malformed-*`). If Option B is chosen, the I6 assertion `reason ==
  "ensemble-empty"` would be **wrong as written** and must be relaxed to the chosen slug.
- **This is NOT an error in the research** — the research correctly identifies and surfaces it
  (R2 §0; research-notes L65, L96). It IS a tension the task file must encode: the I6 test
  assertion's slug is **downstream of the Q6 human-decision** and must be written to the chosen
  slug (or assert only the verdict/exit-code `blocked`/2 until Q6 resolves). Per project policy
  the task must HALT on Q6, write PENDING, and NOT auto-pick. Surfaced, not resolved.

### C2 (MINOR — non-blocking, documentation-vs-code): stub.py docstring lists `time` import
- **R5 §1/§(a)** flags that `stub.py:36-38` docstring claims it imports `time`, but `time` is NOT
  actually imported (body uses a fixed `elapsed_ms`). No functional impact; network/clock-free
  property holds either way. R5 correctly tags it a docstring-vs-code discrepancy. Surfaced for
  completeness; does not affect any FR-RH2 deliverable.

No other cross-file contradictions found. All other overlapping-surface claims (Items 1-6) are
mutually consistent.

---

## Documentation Staleness / Verification-Tag Check

- Doc-sourced (TDD/spec) architectural claims in the research are consistently tagged or
  ground-verified. R2 carries `[CODE-VERIFIED]` on the Q6 absence; TDD §22 (tdd.md:1539) carries
  the `[UNVERIFIED]`/`[CODE-CONTRADICTED]` carry-forward list (Q5 undocumented `--suspect-source`,
  Q6 slug absence `[CODE-VERIFIED]`, Q7 import-shape `[UNVERIFIED]`, enum domains `[UNVERIFIED]`).
- **No untagged doc-sourced architectural claim reported as current fact.** Every line anchor in
  R1-R6 is stamped "verified against shipped source 2026-06-20" with the zero-trust note. The TDD's
  own "Last Verified 2026-06-20" claim was independently re-verified by the researchers rather than
  trusted (research-notes L63). **PASS.**

---

## Completeness Note (research file status fields)

- **R1 header inconsistency (MINOR):** `01-...md` line 6 header says **Status: In Progress**, but
  line 183 says **Status: Complete** and the body is fully populated through §5 + a DRIFT-findings
  section. This is a stale header field, not incomplete work — the file IS complete. Flag for a
  one-character fix (header → Complete) but does NOT block. R2-R6 all correctly say Status:
  Complete in their headers.
- All six files have Summary/Key-Takeaway sections and (R1's DRIFT findings, R2-R6's SUMMARY/
  deliverables) gap/handoff sections. Coverage of the 6 assigned slices is complete.

---

## Compiled Gaps

### Critical Gaps (block synthesis/FR-RH2.3 code)
- **None that the research failed to surface.** The one BLOCKING item — Q1 (OI-1) validation
  against the shipped diff and Q6 (slug) human-decision — is correctly identified, evidence-backed,
  and routed to a HALT. These are *intended* blocking gates, not research defects.

### Important Gaps (affect quality / must be encoded in the task)
- **G1 (C1): I6 slug assertion is downstream of the open Q6 decision.** The task file must NOT
  let I6 hard-assert `ensemble-empty` until Q6 is resolved; encode it as PENDING/conditional and
  HALT on Q6 (do not auto-pick Option B). Source: TDD I6 (L1191) vs §22 Q6 (L1533); R2 §0.
- **G2: retry-once-on-5xx / 2s-backoff arithmetic has no pinned line anchor.** R5 §5 correctly
  routes it to dispatch.py (R3's lane), but R3 does not enumerate the `retry_policy` body anchor.
  If U-tier or I-tier tests need to assert retry behavior, the task must add a grounding pass on
  dispatch.py's retry_policy (neither R3 nor R5 pins it). Source: R5 §5; R3 §1.

### Minor Gaps (must still be fixed)
- **G3: R1 header Status field says "In Progress"** (line 6) while the file is Complete (line 183).
  One-line fix. Source: 01-...md L6.
- **G4: stub.py docstring lists a `time` import that does not exist** (C2). Cosmetic; outside
  FR-RH2 scope but worth a note in the task's "observed adjacent issues". Source: R5 §(a).

---

## VERDICT: PASS

**Rationale:** Across all six research files and the driving spec/TDD, the cross-validation found
**zero substantive contradictions between research files** and **zero mis-assignment of spec/TDD
authority**. Every shared-surface claim (LensEntry 14 fields, FR-6 PASS→BLOCKED at runner.py:588-590,
retry-in-dispatch-not-transport, the OI-1 left-column ∩ swarm-absence sizing, all 7 TDD drift
corrections, the §15 matrix grounding) is internally consistent and anchored to a current shipped
`file:line`. The Q6 grep gives an unambiguous, evidence-backed Option A vs Option B basis, and the
research correctly routes it to a human-decision HALT.

The two issues surfaced (C1: the TDD I6 row pre-commits to a slug the open Q6 decision may
override; C2: a cosmetic stub.py docstring discrepancy) are **correctly identified BY the research
itself** and are tensions for the task file to encode — not research defects. C1 must be carried
into the task as a conditional/PENDING assertion gated on the Q6 human-decision (consistent with
project policy that human-decision items HALT rather than auto-default).

PASS is conditional on the task-builder encoding G1 (C1) as a Q6-gated PENDING item (HALT, no
auto-pick) and noting G2-G4. These are task-construction obligations, not blockers to proceeding
from research → synthesis.

### Structured gap list (for the task-builder)
1. **G1 / C1 (Important):** I6's `reason == "ensemble-empty"` assertion is downstream of open Q6.
   Encode as PENDING + HALT on the Option A/B human-decision; until resolved, I6 asserts only
   `verdict == blocked` / `exit == 2`. Anchors: tdd.md:1191 (I6), tdd.md:1533 (Q6), R2 §0/§6.
2. **G2 (Important):** No pinned line anchor for the retry-once-on-5xx/2s-backoff policy. Add a
   dispatch.py grounding pass if any test asserts retry. Anchors: R5 §5, R3 §1.
3. **G3 (Minor):** Fix R1 file header Status "In Progress" → "Complete" (01-...md:6).
4. **G4 (Minor):** stub.py docstring lists a non-existent `time` import (R5 §(a)); note as an
   adjacent cosmetic issue, out of FR-RH2 scope.
