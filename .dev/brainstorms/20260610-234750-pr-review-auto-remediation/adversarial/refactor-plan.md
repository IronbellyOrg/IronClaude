---
contract_version: "1.0"
artifact: adversarial-refactor-plan
step: 4-merge-plan
topic: "PR Review Auto-Remediation Monitor (V1.0)"
base: variant-3-haiku-qa.md
incorporates: [variant-1-opus-architect.md, variant-2-sonnet-backend.md]
invariant_resolutions: [INV-001, INV-007, INV-009, INV-015, INV-016]
created: 2026-06-11
review_status: auto-approved-non-interactive
---

# Refactor Plan — PR Review Auto-Remediation Monitor (V1.0)

## Overview

- **Base = Variant C** (`variant-3-haiku-qa.md`) — selected per `base-selection.md`: quant
  leader (0.961), maxes the two dimensions the feature exists to get right (Invariant & Edge
  5/5, Risk 5/5). C's native spine — the fence-post loop-guard matrix (T-620..T-629, T-626
  canonical off-by-one), the EC-1..EC-16 edge catalog, the INV-1..INV-7 round-counter
  invariants, the per-requirement FR/NFR/AC→T-id coverage matrix, and the three-state
  detection classifier with independently-tested severity rubric — is **preserved verbatim**.
- **Incorporating A (architect) + B (backend)** as additive imports onto C's two genuine
  weaknesses (Structure 2/5, durability) — never as spine replacements.
- **Change count:** 14 planned changes. 5 are MANDATORY normative invariant-resolution grafts
  (highest priority, adopted verbatim from R3); 3 from A; 3 from B; 3 supporting integration
  changes (FSM-state renumber alignment, validation-gate reconciliation, AC superset merge).
- **Overall risk: MEDIUM.** No change is High-risk in isolation. The aggregate risk concentrates
  in two seams: (a) re-deriving C's INV-1..INV-7 numeric fence-posts against the new INV-001
  single-edge counter definition (CH-1), and (b) reconciling C's autonomy-level prose against
  A's capability-ceiling FSM without losing any of C's behavioral test assertions (CH-6). Both
  are de-risked because R3 + base-selection already did the contradiction analysis; this plan
  only transcribes their verdicts into C's structure.

---

## Planned Changes

> Entries CH-1..CH-5 are the MANDATORY Round-3 invariant resolutions. Their normative sentences
> are adopted **verbatim** and are the highest-priority, non-negotiable content of the merged
> spec. CH-6..CH-14 graft A/B strengths around them.

### CH-1 — INV-001 single-edge round-counter definition (MANDATORY)

- **Source:** R3 `r3-architect.md` §INV-001 (owns); accepted by `r3-backend.md`, verified by
  `r3-qa.md` (T-626-OFF-BY-ONE, T-VANISHED-MONO).
- **Target in C:** §6.1 "Round Counter Invariants" (INV-1..INV-7) + §6.2 fence-post matrix
  (T-620..T-629) + §6.4 (T-630).
- **Integration approach:** **restructure** — replace C's INV-2 ("increments exactly once per
  remediation cycle (fix → push → re-review)") and the ambiguous INV-1 "starts at 0" framing
  with the verbatim normative sentence, then re-derive every fence-post row from the single edge.
- **Verbatim normative rule:** "`round_counter` = the count of **completed monitor-triggered
  remediation cycles**; increments by exactly 1 at the single FSM transition
  `S5_AWAITING_REREVIEW --[review_observed ∧ sha_attributed_to_our_push]--> S2_CLASSIFY`;
  increments **nowhere else** (not on inbound-review detection, diagnosis start, push emission,
  or validation retry); monotonic — a counted re-review that later vanishes does NOT decrement;
  gate `round_counter >= max_rounds ⇒ HALT_MAX_ROUNDS` evaluated before opening each fix cycle;
  user-facing label = `round_counter + 1`; `max_rounds=N` → exactly N pushes."
- **Rationale:** `invariant-probe.md` INV-001 (HIGH, root fault): consensus #1 fused two
  non-equivalent counters (B's increment-before-diagnosis vs C's increment-after-cycle); they
  diverge on every non-happy boundary (INV-013/014). R3 picks the cycle-completion edge because
  the increment is then **attributable and irrevocable**, closing INV-014's vanished-review
  ambiguity determinately. Preserves C T-626's `assert round_counter == 2 NOT 3`.
- **Risk: Med** — touches C's load-bearing safety proof; mitigated because R3-QA already
  re-derived T-626 + added T-VANISHED-MONO under exactly this definition.

### CH-2 — INV-016 G-push 5-predicate runtime conjunction (MANDATORY)

- **Source:** R3 `r3-architect.md` §INV-016 (owns); verified `r3-qa.md` (T-ZERO-EDIT-NO-PUSH).
- **Target in C:** §2 FR-4 (autonomy gates) + §2 FR-5/FR-6 (push path) + §12 R4 row.
- **Integration approach:** **insert** a new normative gate definition; **restructure** C's
  level-3 prose to route through it.
- **Verbatim normative rule:** "A push is authorized at `S4_PUSHING` iff ALL hold as a
  conjunction immediately before `git push`: (1) `monitor_ordinal >= 3`; (2)
  `validation_status == "validated"`; (3) `needs_human_decision == false` for every finding in
  the cycle; (4) `round_counter < max_rounds`; (5) `applied_edits > 0`. Any false predicate
  routes to `HALT_*` and NO push occurs. Every push, authorized or blocked, writes a write-ahead
  `push_decision` audit record naming which predicates held (mandatory at L3; not a per-push
  prompt). The FIRST push of a run requires `--yes` OR interactive confirm unless the run is
  non-interactive, in which case the `push_decision` record + explicit `--monitor 3` arming
  stands as the recorded authorization."
- **Rationale:** `invariant-probe.md` INV-016 (HIGH): bare `ordinal >= 3` is the level the
  operator already selected, not a safety layer. Predicate (5) `applied_edits > 0` closes the
  "push/announce-resolved with nothing changed" hole that INV-009 could feed.
- **Risk: Med** — adds a real confirmation primitive C lacked; mitigated by T-ZERO-EDIT-NO-PUSH.

### CH-3 — INV-007 write-ahead push idempotency ordering (MANDATORY)

- **Source:** R3 `r3-backend.md` §INV-007 (owns); verified `r3-qa.md`
  (T-CRASH-WINDOW-NO-DOUBLE-PUSH).
- **Target in C:** new run-log/recovery section (created by CH-9) — push event sequence.
- **Integration approach:** **append** the ordered event sequence + crash-window resume rule.
- **Verbatim normative rule:** "Ordered sequence per push: `push_decision` (fsync) →
  `push_initiated{target_sha, pre_push_sha, fsync}` (fsync **before** `git push`) →
  `git push <remote> <target_sha>:<branch>` → `push_completed` (fsync). On `--resume`, a
  `push_initiated` without matching `push_completed` MUST query the remote for `target_sha`
  before any new commit/push: reachable ⇒ append `push_completed{recovered:true}`; not reachable
  ⇒ `push_aborted_or_not_landed{recovered:true}` and re-enter the pre-push path without
  recomputing the fix; ambiguous ⇒ HALT_HUMAN. Idempotency key = `push:<run_id>:<cycle_id>:
  <pre_push_sha>:<target_branch>` (PRE-push SHA, not post-hoc). Every `round_counter` increment
  must attribute to a recorded `push_initiated.target_sha`."
- **Rationale:** `invariant-probe.md` INV-007 (HIGH): B's FM-6 detected crash-after-push via
  post-hoc `push_completed`, leaving the `git push`→log-fsync window with no write-ahead token →
  double-push. The pre-push SHA write-ahead closes it and ties cleanly to CH-1's SHA-attributed
  increment.
- **Risk: Med** — recovery correctness is subtle; mitigated by the 3-case resume rule + test.

### CH-4 — INV-009 fix-dedup / reply-key separation (MANDATORY)

- **Source:** R3 `r3-backend.md` §INV-009 (owns); verified `r3-qa.md`
  (T-FRESH-COMMENT-NO-DOUBLE-FIX).
- **Target in C:** §14 QD-5 (reply-ID tracking) + EC-4 (duplicate findings) + NFR-1.
- **Integration approach:** **replace** C's QD-5 "reply-ID tracking keyed on comment_id" with
  the two-key scheme; **restructure** EC-4 to test fresh-comment_id (not just same-id replay).
- **Verbatim normative rule:** "fix-dedup key = `sha256(path + line + finding_body)` —
  **comment_id-INDEPENDENT**; reply/resolve-dedup key = thread-scoped (includes
  comment_id/thread_id + fix_key + reply_purpose). A fresh `comment_id` for the same
  `body + file:line` defect reuses the same fix record (no second fix). A reply MAY be posted on
  the fresh thread but MUST cite the cycle's `applied_edits` status — `applied_edits == 0` /
  ungroundable MUST be phrased as no code change applied and MUST NOT say resolved. Old threads
  resolve only by their own resolve key."
- **Rationale:** `invariant-probe.md` INV-009 (HIGH) + INV-010 (MED): B's original
  `finding_id = "aug-<comment_id>-<stable_hash>"` embedded comment_id, defeating fix-dedup on a
  fresh-comment_id re-review (base-selection X-003). Comment_id-independence is required by CH-1
  (counts cycles not findings) + CH-2 predicate (5). INV-010 rewording-collision stays MED/open
  (secondary near-dup detector deferred, per `r3-backend.md`).
- **Risk: Med** — changes C's dedup contract; mitigated by T-FRESH-COMMENT-NO-DOUBLE-FIX.

### CH-5 — INV-015 KNOWN-LIMITATION validated-not-verified clause (MANDATORY)

- **Source:** R3 `r3-qa.md` §INV-015 (owns, ADDRESSED-via-accepted-risk; T-VALIDATED-NOT-VERIFIED).
- **Target in C:** §12 Risks (R4 row) + a new "Known Limitations" subsection.
- **Integration approach:** **append** the verbatim clause + the `validated_not_verified` audit
  field + the audit test.
- **Verbatim normative clause:** "Validation authorizes a push within this gated envelope; it is
  NOT a correctness guarantee. A fix that passes targeted tests may break untested behaviors.
  Such pushes are recorded as `validated_not_verified` in the run-log (with the list of detected
  behavioral-test failures). Operators should maintain a comprehensive behavioral test suite to
  minimize this residual risk."
- **Rationale:** `invariant-probe.md` INV-015 (HIGH): the sufficiency claim is false — proxy
  validation cannot guarantee correctness. R3-QA's honest disposition is audited acceptance with
  bounded count (CH-1 max_rounds caps it; CH-2 ensures each push made a real edit). Must be
  surfaced, not hidden.
- **Risk: Low** — additive honesty clause + one audit field; no behavioral change.

### CH-6 — Capability-ceiling FSM (one machine, 3 gates + 1 override)

- **Source:** A `variant-1-opus-architect.md` §3 (state machine) + §3.2 ordinal gate table.
- **Target in C:** §1.1 + FR-4 autonomy-level prose + §7 autonomy behavioral tests.
- **Integration approach:** **restructure** — replace C's per-level prose with A's single FSM;
  re-anchor C's T-401/T-410/T-420/T-430 behavioral assertions onto FSM transitions.
- **Rationale:** `base-selection.md` import #1 (A): one machine + ordinal as 3 gates
  (G-arm `ordinal>=1`, G-edit `ordinal>=2`, G-push `ordinal>=3`) + 1 `needs_human_decision`
  override, not 4 nested code paths. Collapses the L2/L3 combinatorial bug surface; gives C's
  tests a real architecture to assert against (AC-2..AC-6 become transition-table rows). G-push
  is the entry point for CH-2's 5-predicate conjunction.
- **Risk: Med** — largest structural change; mitigated because C's level semantics are preserved
  exactly (the FSM is a refactoring of the same behavior, every C autonomy test still asserts).

### CH-7 — detection-contract.md as build-gated locked-constant + purity seam

- **Source:** A §4.1 (DetectionContract YAML), §7 (pluggable constant), AC-8 (locked:false hard
  stop), AC-9 + R5 (purity CI test).
- **Target in C:** §2 FR-2.2 (detection contract) + §12 R1 row + a new build-gate AC.
- **Integration approach:** **replace** C's "config constant, not hard-guessed" prose with A's
  YAML-fronted locked constant; **append** the `locked:false` refuse-to-arm HARD STOP and the
  purity test (no `gh`/`git` token in the deterministic core).
- **Rationale:** `base-selection.md` import #2 (A): turns R1 from a "should" into a
  mechanically-enforced sequencing gate. C's T-210 ("config absent → HALT 'probe first'") is
  preserved and strengthened to `locked == true` assertion. Purity test (AC-9) protects the seam
  from future maintainers inlining a bot-login string (R5 seam-leakage).
- **Risk: Low** — strengthens an existing C HALT; additive CI test.

### CH-8 — SoT component decomposition + build-sequencing DAG

- **Source:** A §2.2 (exact `src/superclaude/` source-tree), §2.3 (C1..C6 single-responsibility
  table), §12 (dependency DAG, probe-first gate).
- **Target in C:** new §"Component Inventory" + new §"Build Sequencing" (C had only the
  `tests/submit_pr/` tree).
- **Integration approach:** **insert** the component inventory (skill pkg
  `src/superclaude/skills/sc-submit-pr-protocol/`, command `commands/submit-pr.md`, hook edit
  `hooks/scripts/offer-pr-review.sh`) + the dependency DAG with DET (`detection-contract.md`)
  gating all downstream steps.
- **Rationale:** `base-selection.md` import #3 (A) — fills C's Completeness 1.5 + Structure
  3.3/3.4/3.5 gaps directly (the NOT-MET dimensions). The probe-first gate sequences CH-7's
  `locked:false` hard stop as build step 0.
- **Risk: Low** — purely additive structure C lacked.

### CH-9 — Write-ahead run-log substrate (JSONL authoritative + snapshot cache)

- **Source:** B `variant-2-sonnet-backend.md` §"Idempotency & Run-log Schema" (~29-event
  envelope, `state.snapshot.json` cache, "JSONL is authoritative" rule).
- **Target in C:** NFR-3 (C had only "per-run JSONL log exists" + T-N20..T-N22).
- **Integration approach:** **replace** C's thin NFR-3 with B's full substrate; **insert** the
  ~29-event type list + the materialized-state schema + the snapshot/JSONL conflict rule
  (rebuild from JSONL).
- **Rationale:** `base-selection.md` import #4 (B) — the durability/observability spine C lacks;
  also the write-ahead substrate CH-3 (INV-007) and CH-1 (write-ahead `round_counter`) require.
- **Risk: Low** — additive schema; C's JSONL-validity test (T-N22) still applies.

### CH-10 — Failure modes FM-1..FM-12 + `--resume` first-class flag

- **Source:** B §"Failure Modes & Recovery" (FM-1..12), command contract `--resume`, AC-16
  (resume reconstruction).
- **Target in C:** §5 edge catalog (EC) + §1 command signature + AC table.
- **Integration approach:** **append** FM-1..12 as a recovery catalog alongside C's EC-1..EC-16
  (complementary, not overlapping); **insert** `--resume <run-log-path>` into the signature with
  its acceptance criterion (AC-16).
- **Rationale:** `base-selection.md` import #5 (B) — crash-after-push-before-reply (FM-6),
  crash-after-reply-before-resolve (FM-7), corrupt-log (FM-12). FM-6 is the concrete realization
  of CH-3's crash-window. C's EC catalog stays (edge cases); FM catalog adds recovery semantics.
- **Risk: Low** — additive; `--resume` acceptance criterion is precise (AC-16).

### CH-11 — Precise idempotency sets / dedup keys (5 durable sets)

- **Source:** B §"Idempotency keys" (`processed_review_ids`, `processed_finding_ids`,
  `replied_comment_ids`, `resolved_thread_ids`, `pushed_commit_shas`) + `idempotency_skip` event.
- **Target in C:** NFR-1 + QD-5 (reconciled with CH-4).
- **Integration approach:** **insert** the 5 named durable sets into the materialized state;
  ensure `processed_finding_ids` uses CH-4's comment_id-independent `fix_key` (not B's original
  comment_id-embedding `finding_id`).
- **Rationale:** `base-selection.md` import #6 (B) — pins the dedup sets. The one correction:
  `processed_finding_ids` keys on CH-4's `fix_key`, resolving X-003/INV-010 embedding defect.
- **Risk: Low** — additive sets; the one conflict (finding-id key) already resolved by CH-4.

### CH-12 — FSM state-name reconciliation (C INV-* ↔ A/B S-states)

- **Source:** integration glue — A's 7-state FSM + B's S0..S14 + R3's `S2_CLASSIFY`/
  `S4_PUSHING`/`S5_AWAITING_REREVIEW`/`HALT_MAX_ROUNDS`/`HALT_HUMAN` names.
- **Target in C:** all FSM-referencing sections (§6, §7, new run-log section).
- **Integration approach:** **restructure** — adopt the R3 state names as canonical (since CH-1
  and CH-2 cite them verbatim); map A's 7 states and B's S0..S14 onto them in a single glossary
  table so no section references an orphan state.
- **Rationale:** CH-1/CH-2/CH-3 normative sentences name specific states; the merged spec must
  use one consistent state lexicon or re-introduce the term-drift base-selection Clarity 4.4
  flagged against C.
- **Risk: Med** — pure renaming across many sections; risk is a missed reference, mitigated by a
  single canonical glossary + grep check.

### CH-13 — Validation-gate reconciliation (VG-1..VG-6 ∪ B 5-step order)

- **Source:** A §9 (VG-1..VG-6 table) + B §"Validation Gates" (ordered 5-step) + C FR-5/§10.
- **Target in C:** FR-5 + §10 validation-gate tests.
- **Integration approach:** **restructure** into one ordered, numbered gate list: targeted tests
  → cross-cutting escalation to `make test` → `make lint` → `uv run ruff format --check
  src/ tests/` → (sync `make verify-sync` for skill self-edits) → PR-target URL gate.
- **Rationale:** All three variants agree on the lint+format-both gotcha (base-selection 2.4 MET
  all); merge their three phrasings into one ordered gate so `validation_status == "validated"`
  in CH-2 predicate (2) has a single precise definition.
- **Risk: Low** — three consistent sources; mechanical merge.

### CH-14 — Acceptance-criteria superset merge

- **Source:** C AC-1..AC-7 (base) + A AC-8/AC-9 + B AC-1..AC-16 + R3 canonical tests
  (T-626-OFF-BY-ONE, T-VANISHED-MONO, T-CRASH-WINDOW-NO-DOUBLE-PUSH,
  T-FRESH-COMMENT-NO-DOUBLE-FIX, T-ZERO-EDIT-NO-PUSH, T-VALIDATED-NOT-VERIFIED).
- **Target in C:** §9 Acceptance Criteria + §4.2 coverage matrix.
- **Integration approach:** **append** — keep C's AC-1..AC-7 + coverage matrix, add A's
  build-gate/purity ACs, B's resume/backoff/idempotency ACs, and bind the 6 R3 canonical tests
  to CH-1..CH-5 with new T-ids in the matrix.
- **Rationale:** Preserves C's per-requirement testability (its strongest native asset) while
  extending the matrix to cover every grafted invariant + structural import. No AC is dropped.
- **Risk: Low** — additive; superset by construction.

---

## Changes NOT Being Made (rejected alternatives)

- **B-as-base — REJECTED.** B is the raw combined-score leader (0.912 vs C 0.897) but loses the
  fired L1 tiebreaker to C on debate-point count (co-win-inclusive 7>5; 0.5-weighted 5.5>5.0),
  and B is only 3/5 on Invariant & Edge — the dimension the edge-case floor exists to protect.
  C's edge/risk dimensions (5/5 each) dominate the feature's reason-to-exist; B's durability is
  an additive import (CH-9/10/11), not a spine. (`base-selection.md` Selected Base.)
- **A-as-base — REJECTED.** A is at the 1/5 Invariant & Edge floor (single AC-6 assertion, no
  edge catalog, no fence-post matrix, max-rounds=0 undefined). A's architecture is the strongest
  *import* (CH-6/7/8) but the hardest part to retrofit (exhaustive loop-guard proof) is native to
  C, not A.
- **B's "round counts reviews-observed-since-arm" timing — REJECTED per INV-001.** R3 picks the
  cycle-completion edge (increment AFTER our-push-attributed re-review), NOT B's
  increment-before-diagnosis. B's timing ticks on a transient detection event that can vanish
  (INV-014 ambiguity); the adopted timing is attributable + irrevocable. (CH-1.)
- **B's `finding_id = "aug-<comment_id>-<stable_hash>"` fix-dedup key — REJECTED per INV-009.**
  Embedding comment_id defeats fix-dedup on a fresh-comment_id re-review. Replaced by CH-4's
  comment_id-independent `sha256(path+line+body)`.
- **C's QD-5 "reply-ID tracking keyed on comment_id (not finding body hash)" — REPLACED.** C's
  single-key scheme is correct for thread-reply scope but insufficient for fix-dedup; CH-4 splits
  into the two-key scheme (fix_key + thread-scoped reply_key).
- **"Opt-in default-off" framing of L3 push — REJECTED per INV-016.** Bare `ordinal>=3` is not a
  safety layer; replaced by CH-2's 5-predicate conjunction + first-push confirmation +
  `push_decision` audit record.
- **Claiming validation is sufficient for R4 blast radius — REJECTED per INV-015.** Replaced by
  CH-5's honest KNOWN-LIMITATION clause + `validated_not_verified` audit field.
- **INV-010 rewording-collision full closure — DEFERRED (not made).** Per `r3-backend.md`, stays
  MEDIUM/open; a secondary near-duplicate detector or human-review fallback is out of V1.0 HIGH
  closure scope. Noted, not built.

---

## Risk Summary

| Change | Type | Risk |
|--------|------|------|
| CH-1 INV-001 single-edge counter | restructure | **Med** |
| CH-2 INV-016 G-push 5-predicate | insert/restructure | **Med** |
| CH-3 INV-007 push write-ahead ordering | append | **Med** |
| CH-4 INV-009 fix/reply dedup keys | replace/restructure | **Med** |
| CH-5 INV-015 known-limitation clause | append | Low |
| CH-6 Capability-ceiling FSM | restructure | **Med** |
| CH-7 detection-contract locked constant + purity | replace/append | Low |
| CH-8 SoT decomposition + build DAG | insert | Low |
| CH-9 Write-ahead run-log substrate | replace/insert | Low |
| CH-10 FM-1..12 + `--resume` | append/insert | Low |
| CH-11 5 idempotency sets | insert | Low |
| CH-12 FSM state-name reconciliation | restructure | **Med** |
| CH-13 Validation-gate reconciliation | restructure | Low |
| CH-14 AC superset merge | append | Low |

**Overall risk: MEDIUM.** 6 Med + 8 Low; zero High. The Med changes (CH-1/2/3/4/6/12) all
involve restructuring C's spine or reconciling state lexicons, but each is de-risked by an
upstream artifact that already resolved the contradiction: CH-1/2/3/4/5 transcribe R3 normative
sentences that are accepted by all three personas and verified by R3-QA canonical tests; CH-6/12
are behavior-preserving refactors (the FSM expresses the same level semantics C already tests).
The residual irreducible risk is INV-015's validated-not-verified gap — surfaced honestly as a
known limitation (CH-5), bounded by max_rounds (CH-1) and the applied_edits>0 predicate (CH-2),
not eliminated.

---

## Review Status

**AUTO-APPROVED — non-interactive run.** This refactor plan was generated as Step 4 of the
sc:adversarial pipeline in non-interactive mode. No human review gate was requested for this
step. The 5 mandatory invariant-resolution changes (CH-1..CH-5) adopt the Round-3 normative
sentences verbatim and are non-negotiable; the 9 strength-graft changes (CH-6..CH-14) are
traceable 1:1 to `base-selection.md`'s "Strengths to INCORPORATE" list and the R3 constraints.
The merged single implementable SPEC is produced from this plan downstream.
