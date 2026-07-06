---
artifact: adversarial-merge-log
step: 5-merge-execution
topic: "PR Review Auto-Remediation Monitor (V1.0)"
executor: merge-executor
base: variant-3-haiku-qa.md
output: ../merged-spec.md
created: 2026-06-11
---

# Merge Log — PR Review Auto-Remediation Monitor (V1.0)

## Metadata

| Field | Value |
|---|---|
| Base variant | Variant C (`variant-3-haiku-qa.md`) — test-centric spine preserved |
| Executor | merge-executor (sc:adversarial Step 5) |
| Plan | `refactor-plan.md` (14 changes CH-1..CH-14) |
| Changes applied | 14 / 14 |
| Changes failed | 0 |
| Changes skipped | 0 |
| Output | `/config/workspace/IronClaude/.dev/brainstorms/20260610-234750-pr-review-auto-remediation/merged-spec.md` |
| Status | success |
| Timestamp | 2026-06-11 |

Graft sources: Variant A (`variant-1-opus-architect.md`), Variant B (`variant-2-sonnet-backend.md`),
and the three Round-3 normative resolutions (`r3-architect.md`, `r3-backend.md`, `r3-qa.md`) for the
five verbatim invariant rules.

---

## Changes Applied

### CH-1 — INV-001 single-edge round-counter definition (MANDATORY)
- **Status:** applied.
- **Before:** C §6.1 had INV-1 "starts at 0" + INV-2 "increments exactly once per remediation cycle
  (fix → push → re-review)" — ambiguous edge, two readings.
- **After:** merged §9.1 carries the verbatim INV-001 normative sentence (single edge
  `S5_AWAITING_REREVIEW --[review_observed ∧ sha_attributed_to_our_push]--> S2_CLASSIFY`, increments
  nowhere else, monotonic/irrevocable, `>=` gate, label `+1`, `max_rounds=N` → N pushes). INV-1..INV-7
  re-derived as corollaries of the single edge; fence-post matrix (§9.2) re-anchored; T-626-OFF-BY-ONE
  + T-VANISHED-MONO added verbatim (§9.3).
- **Provenance:** `<!-- Source: r3-architect.md §INV-001 ... Change CH-1 -->` (merged §9).
- **Validation:** single-counter check — exactly one verbatim INV-001 definition; rejected B
  "reviews observed since arm" counter absent (grep NONE). FR-6.3 carries the same sentence.

### CH-2 — INV-016 G-push 5-predicate runtime conjunction (MANDATORY)
- **Status:** applied.
- **Before:** C FR-4.3 level-3 = "implement + validate + commit + push + reply + resolve" (bare
  ordinal, no runtime gate).
- **After:** new §5.3 carries the verbatim INV-016 5-predicate conjunction + `push_decision`
  write-ahead audit + first-push confirm; FR-4.3 routes through it; §10.2 commit/push gate references
  it; §17 R4 updated. T-ZERO-EDIT-NO-PUSH bound.
- **Provenance:** `<!-- Source: r3-architect.md §INV-016 ... Change CH-2 -->` (merged §5.3).
- **Validation:** predicate (5) `applied_edits > 0` present; FR-4.3 + §10.2 reference §5.3 (resolved).

### CH-3 — INV-007 write-ahead push idempotency ordering (MANDATORY)
- **Status:** applied.
- **Before:** C had no push-event ordering / crash-window rule.
- **After:** §12.1 carries the verbatim ordered sequence (`push_decision` → `push_initiated`
  {target_sha, pre_push_sha, fsync} → `git push` → `push_completed`) + 3-case `--resume` rule + pre-push
  SHA idempotency key. T-CRASH-WINDOW-NO-DOUBLE-PUSH bound.
- **Provenance:** `<!-- Source: r3-backend.md §INV-007 ... Change CH-3 -->` (merged §12.1).
- **Validation:** event triad present in §11.3 type list and §12.1; ties to CH-1 SHA-attributed
  increment (cross-ref resolved).

### CH-4 — INV-009 fix-dedup / reply-key separation (MANDATORY)
- **Status:** applied.
- **Before:** C QD-5 "reply-ID tracking keyed on comment_id (not finding body hash)" — single key.
- **After:** QD-5 (§20) REPLACED with the two-key scheme (fix_key = `sha256(path+line+body)`,
  comment_id-independent; reply_key thread-scoped). EC-4 (§8) restructured to test fresh-comment_id;
  NFR-1 (§13) + §11.4 `processed_finding_ids` keyed on `fix_key`. Reply MUST cite `applied_edits`
  status, never false "resolved". T-FRESH-COMMENT-NO-DOUBLE-FIX bound.
- **Provenance:** `<!-- Source: r3-backend.md §INV-009 ... Change CH-4 -->` (merged §5.4, §8 EC-4,
  §11.4, §20 QD-5).
- **Validation:** C's old comment_id-only key explicitly noted as replaced; fresh-comment_id test path
  present.

### CH-5 — INV-015 KNOWN-LIMITATION validated-not-verified clause (MANDATORY)
- **Status:** applied.
- **Before:** C R4 implied validation gate sufficiency.
- **After:** new §13.1 Known Limitations carries the verbatim INV-015 clause ("Validation authorizes a
  push within this gated envelope; it is NOT a correctness guarantee...") + `validated_not_verified`
  audit field; §17 R4 row updated. T-VALIDATED-NOT-VERIFIED bound (AC-13).
- **Provenance:** `<!-- Source: r3-qa.md §INV-015 ... Change CH-5 -->` (merged §13.1).
- **Validation:** clause present verbatim; additive honesty, no behavioral change.

### CH-6 — Capability-ceiling FSM (one machine, 3 gates + 1 override)
- **Status:** applied.
- **Before:** C per-level prose (FR-4.1..4.4) with no architecture.
- **After:** new §5 single FSM + §5.2 ordinal gate table (G-arm/G-edit/G-push + needs_human_decision
  override). FR-4 prose re-anchored onto FSM transitions; §14 behavioral tests assert FSM states
  visited (S3_FIXING, S4'_HALT_BEFORE_PUSH). C's level semantics preserved exactly.
- **Provenance:** `<!-- Source: Variant A (opus:architect) §3 ... Change CH-6 -->` (merged §1.1, §5,
  §14).
- **Validation:** all 4 C autonomy tests (T-401/410/420/430) preserved + re-anchored; G-push routes
  through §5.3.

### CH-7 — detection-contract.md build-gated locked constant + purity seam
- **Status:** applied.
- **Before:** C FR-2.2 "config constant, not hard-guessed" prose.
- **After:** §7 YAML-fronted locked DetectionContract + `locked:false` HARD STOP (AC-8) + core-purity
  test (AC-9/NFR-6, T-N50). FR-2.2 references §7; T-210 strengthened to `locked == true`.
- **Provenance:** `<!-- Source: Variant A (opus:architect) §4.1 + §7 + AC-8/AC-9 ... Change CH-7 -->`
  (merged §7).
- **Validation:** AC-8 + AC-9 present in §16; NFR-6 present; R11 seam-leakage row added.

### CH-8 — SoT component decomposition + build-sequencing DAG
- **Status:** applied.
- **Before:** C had only the `tests/submit_pr/` tree.
- **After:** new §2 Component Inventory (source-tree + C1..C6/DET table) + new §3 Build Sequencing DAG
  (DET as step 0 gate) + §19 SoT/PR-target discipline.
- **Provenance:** `<!-- Source: Variant A (opus:architect) §2.2 + §2.3 ... Change CH-8 -->` (merged §2,
  §3, §19).
- **Validation:** prerequisites-before-dependents ordering (DET gates step 1); purely additive.

### CH-9 — Write-ahead run-log substrate (JSONL authoritative + snapshot cache)
- **Status:** applied.
- **Before:** C NFR-3 = thin "per-run JSONL log exists" + T-N20..T-N22.
- **After:** new §11 full substrate (authority rule, locations, ~30-event type list, envelope, 5
  idempotency sets); C's T-N20..T-N22 retained under §11.3 / §13 NFR-3.
- **Provenance:** `<!-- Source: Variant B (sonnet:backend) §Idempotency & Run-log Schema ... Change
  CH-9 -->` (merged §11).
- **Validation:** JSONL-authoritative rule present; C's JSONL-validity test still applies.

### CH-10 — Failure modes FM-1..FM-12 + `--resume` first-class flag
- **Status:** applied.
- **Before:** C had EC-1..EC-16 only (edge cases, no recovery semantics).
- **After:** new §12.2 FM-1..12 recovery catalog (complementary to §8 EC); `--resume` added to
  signature (FR-1.7) + AC-11. EC catalog retained intact.
- **Provenance:** `<!-- Source: Variant B (sonnet:backend) §Failure Modes ... Change CH-10 -->`
  (merged §12).
- **Validation:** FM-6 realizes CH-3 crash-window; AC-11 resume reconstruction bound (T-113).

### CH-11 — Precise idempotency sets / dedup keys (5 durable sets)
- **Status:** applied.
- **Before:** C NFR-1 + QD-5 single comment_id key.
- **After:** §11.4 names 5 durable sets; `processed_finding_ids` keyed on CH-4 `fix_key` (NOT B's
  original comment_id-embedding `finding_id`).
- **Provenance:** `<!-- Source: Variant B (sonnet:backend) §Idempotency keys ... Change CH-11;
  processed_finding_ids keyed on CH-4 fix_key -->` (merged §11.4).
- **Validation:** the one conflict (finding-id key) resolved by CH-4; B's comment_id-embedding key
  rejected (refactor-plan "Changes NOT Being Made").

### CH-12 — FSM state-name reconciliation (C INV-* ↔ A/B S-states)
- **Status:** applied.
- **Before:** C INV-* prose + A 7-state + B S0..S14 used three lexicons.
- **After:** R3 state names adopted canonical (cited verbatim by CH-1/2/3); §15.6 glossary maps A's 7
  states + B's S0..S14 onto them. All FSM-referencing sections (§5, §9, §11, §12) use one lexicon.
- **Provenance:** `<!-- Source: integration glue (Change CH-12) — R3 names canonical ... -->` (merged
  §15.6).
- **Validation:** no orphan state references; glossary table complete (14 canonical rows).

### CH-13 — Validation-gate reconciliation (VG-1..VG-6 ∪ B 5-step order)
- **Status:** applied.
- **Before:** C FR-5/§10 prose; A VG-1..VG-6 table; B 5-step order — three phrasings.
- **After:** §10 single ordered numbered gate list (VG-1 targeted → VG-2 make test escalation → VG-3
  lint → VG-4 format → VG-5 verify-sync → VG-6 PR-target) + §10.1 no-push-on-failure + §10.2 commit/push
  gate. `validation_status == "validated"` = §10 all-green, the single definition consumed by §5.3
  predicate (2).
- **Provenance:** `<!-- Source: Variant A §9 + Variant B §Validation Gates + Variant C FR-5/§10 ...
  Change CH-13 -->` (merged §10).
- **Validation:** lint+format both mandatory (T-511 gotcha preserved); FR-5.4 ties to §5.3.

### CH-14 — Acceptance-criteria superset merge
- **Status:** applied.
- **Before:** C AC-1..AC-7.
- **After:** §16 superset — C AC-1..AC-7 verbatim + A AC-8/AC-9 + B AC-10..AC-13 (backoff, resume,
  crash-idempotency, validated-not-verified); 6 R3 canonical tests bound in §6.2 coverage matrix. No
  AC dropped.
- **Provenance:** `<!-- Source: Variant C AC-1..AC-7 + Variant A AC-8/AC-9 + Variant B ... Change
  CH-14 -->` (merged §16).
- **Validation:** AC superset by construction; coverage matrix extended for every grafted invariant.

---

## Post-Merge Validation

### Structural integrity — PASS
- Document starts with exactly one H1 (`# Merged Specification: ...`). (The second `# ...` grep hit at
  line 439 is a YAML comment inside a fenced code block, not a markdown heading.)
- Heading hierarchy: H1 → H2 (20) → H3 (60). No heading-level gaps (H2→H4 jump scan: clean). No
  orphaned subsections.
- Logical ordering: prerequisites precede dependents — Component Inventory (§2) and Build Sequencing
  (§3, DET as step 0 gate) precede the FRs that consume them; §5 FSM precedes §9 loop-guard which cites
  its single increment edge; §11 run-log substrate precedes §12 crash-recovery which writes to it.
- One FSM lexicon: R3 canonical names used throughout; §15.6 glossary maps A/B states. No orphan-state
  references.
- FR IDs normalized: C's FR-1..FR-7 canonical and preserved; A's FR-A* and B's FR-* remap noted (§4
  header + §16 header). AC IDs: C AC-1..7 preserved, A/B/R3 appended AC-8..13. No ID collisions.

### Internal references — total 30 / resolved 30 / broken 0
- Top-level section refs (§N): 16 cited, 16 resolved, 0 broken.
- Subsection refs (§N.M): 14 cited in visible body, 10 resolved to `### N.M` headings. The 4 flagged
  (§2.2, §2.3, §3.2, §4.1) are **provenance citations to the SOURCE variants** inside `<!-- Source -->`
  HTML comments (e.g., "Variant A §3.2 gate table"), not internal references — confirmed absent from
  visible body text. They are correct by construction and invisible in render.
- All 5 invariant cross-refs (INV-001/007/009/015/016) and the 6 R3 canonical test IDs resolve to their
  defining sections + the §6.2 coverage matrix.

### Contradiction rescan (NEW contradictions introduced by the merge only)
- **None introduced.** The merge transcribes R3 verdicts already accepted by all three personas; it did
  not author new normative claims.
- **Single-counter-definition check — CONFIRMED (yes).** Exactly one `round_counter` definition
  survives: the verbatim INV-001 single-edge sentence (§9.1, restated at FR-6.3). The rejected B
  "increment-before-diagnosis / reviews-observed-since-arm" counter is absent (grep for "reviews
  observed since" and "round_index is the count" → NONE). INV-001's two-counter ambiguity does NOT
  reappear. The EC-12 (transient review disappearance, pre-count) vs INV-4/T-VANISHED-MONO (counted
  re-review vanishing, irrevocable) distinction is explicitly reconciled in §8 EC-12 note and §20 QD-3 —
  these are complementary cases, not a contradiction.
- **Dedup-key consistency — CONFIRMED.** C's old comment_id-only QD-5 fully replaced; `fix_key`
  (comment_id-independent) and `reply_key` (thread-scoped) used consistently in §5.4, §8 EC-4, §11.4,
  §13 NFR-1, §20 QD-5. B's rejected comment_id-embedding `finding_id` absent.
- **G-push consistency — CONFIRMED.** "bare ordinal>=3" never stated as sufficient; FR-4.3, §10.2, and
  §17 R4 all route through the §5.3 5-predicate conjunction.

---

## Summary

| Metric | Count |
|---|---|
| Planned | 14 |
| Applied | 14 |
| Failed | 0 |
| Skipped | 0 |

- Mandatory invariant grafts (CH-1..CH-5): 5/5 applied, verbatim normative sentences present.
- Strength grafts (CH-6..CH-14): 9/9 applied, each traceable to `base-selection.md` imports.
- Structural integrity: PASS. Internal references: 30/30 resolved (0 broken). New contradictions: 0.
- Single counter definition: CONFIRMED (yes) — INV-001 two-counter ambiguity not reintroduced.
- **Overall status: success.**

---

## Post-Merge Amendments (prior-art incorporation, 2026-06-11)

> Applied **after** the adversarial Step-5 merge, sourced from
> `../prior-art-evaluation.md` (reuse eval of cc-plugins + Anthropic official `code-review` /
> `pr-review-toolkit` plugins). These are additive grafts onto the converged `merged-spec.md`,
> each carrying an in-document `<!-- Source: prior-art-evaluation.md ... -->` provenance comment.
> They did **not** alter any Round-3 invariant resolution (CH-1..CH-5) or the capability-ceiling FSM
> core; the single-counter-definition and G-push 5-predicate invariants are unchanged.

### AM-1 — Verify-before-remediate (prior-art best practice #1: two-wave verify)
- **Status:** applied.
- **Rationale:** the official `code-review` plugin runs a secondary wave of independent validators
  that cross-check every finding before publishing. V1.0 applies the same false-positive filter to the
  *external* Augment review: a routed finding must independently ground in real code before a
  `/sc:troubleshoot --fix` session (or a push) is spent on it. Directly attacks R1 (detection-is-guesswork)
  and R4 (auto-push blast radius).
- **Sites touched (13):** §1.1 overview flow (verify step); §1.2 new goal *False-positive resistance*;
  §2 new component **C3a** `finding-verify.md` + decomposition rule; §3 build-seq step [2]; **§4 FR-3.5**
  (new normative requirement + provenance block); §5.1 FSM new state **`S2b_VERIFY`** + `REPORT_ONLY`
  branch; §5.2 *G-verify is a content gate* note (explicitly preserves the INV-001 increment edge); §6.1
  counts; §6.2 coverage (`FR-3.5`, `AC-14`); §6.3 new `test_finding_verify.py`; §11.3 events
  `finding_verified`/`finding_unverified`; §13.1 INV-015 input-side reduction note; §16 **AC-14**;
  §17 **R13** (P1) + R4 mitigation strengthened.
- **New tests (3):** T-340 (verified → dispatch), T-341 (false-positive → report-only, no round), T-342
  (parallel fan-out). Distinct from the structural ungroundable-drop (§8 EC-9): verification additionally
  rejects findings whose location *exists* but whose defect does not reproduce.
- **Validation:** verifier stays inside the deterministic-core purity boundary (read-only grounding, no
  `gh`/`git`, NFR-6); INV-001 increment edge unchanged (round counter still ticks only at
  `S5_AWAITING_REREVIEW → S2_CLASSIFY`); test total 109 → 112.

### AM-2 — Posting hygiene + suggestion blocks (prior-art best practice #3)
- **Status:** applied.
- **Rationale:** the official review plugins post inline on the relevant source line, embed a
  ready-to-apply GitHub suggestion block for trivial fixes, use a single summary thread when clean, and
  never duplicate annotations.
- **Sites touched (7):** §1.3 non-goal (suggest-**instead-of**-push deferred as a future R4-reduction);
  **§4 FR-6.5** (new posting-hygiene requirement); §6.1 counts; §6.2 coverage (`FR-6.5`, `AC-15`); §6.3
  `test_reply_resolve.py` (+T-640..642); §16 **AC-15**.
- **New tests (3):** T-640 (trivial fix → reply embeds a ` ```suggestion ` block of the applied hunk),
  T-641 (non-trivial / multi-file → prose + SHA only), T-642 (clean re-review → exactly one summary thread).
- **Design boundary (deliberate):** GitHub thread replies occur only at L3, where the fix is already
  pushed — so V1.0's suggestion block reproduces the **applied** hunk as precise, re-applyable *evidence*.
  Replacing an auto-push with a maintainer-applied suggestion for trivial fixes (a candidate R4
  blast-radius reduction) is recorded as a **future-version** design choice in §1.3 non-goals, NOT V1.0
  behavior — preserving the converged FSM's L3 push semantics.
- **Validation:** gated by `applied_edits > 0` (consistent with FR-6.1 / §5.3 predicate 5); idempotency
  via thread-scoped `reply_key` (NFR-1 / §11.4) unchanged; test total 112 → 115.

### Amendment summary
| Metric | Value |
|---|---|
| Amendments applied | 2 (AM-1, AM-2) |
| Spec sites touched | 20 (13 + 7) |
| New requirements | FR-3.5, FR-6.5 |
| New ACs | AC-14, AC-15 |
| New risks | R13 |
| New tests | 6 (T-340..342, T-640..642) |
| Test total | 109 → 115 |
| R3 invariant resolutions altered | 0 (CH-1..CH-5 untouched) |
| Source | `../prior-art-evaluation.md` best practices #1, #3 |

**Not yet incorporated:** prior-art best practice #2 (certainty-over-volume / severity×confidence —
partly covered by FR-3.1) and #4 (parallel fan-out — partly covered by FR-3.5's parallel verification),
and the `pr-review-toolkit/comment-analyzer` 5-section structured report template.
