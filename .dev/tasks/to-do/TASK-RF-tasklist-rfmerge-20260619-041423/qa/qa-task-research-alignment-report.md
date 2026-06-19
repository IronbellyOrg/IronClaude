# QA Report: Task ⇄ Research/Spec Alignment

**QA_MODE:** task-integrity
**LENS:** task-research-alignment
**Date:** 2026-06-19
**Stance:** ADVERSARIAL — assume the builder dropped or misrepresented research/spec findings.

**Task file:** `.dev/tasks/to-do/TASK-RF-tasklist-rfmerge-20260619-041423/TASK-RF-tasklist-rfmerge-20260619-041423.md`
**Research dir:** `.dev/tasks/to-do/TASK-RF-tasklist-rfmerge-20260619-041423/research/`
**Driving spec:** `.dev/releases/current/v3.8-RigorFlowMerger-tasklist/spec.md`

---

## Method

Read in full: spec.md (all 823 lines), research/08-gapfill-resolutions.md (R-1..R-16), and the
entire 660-line+ task file across all 9 phases (Phases 1–8 + Post-Completion), every QA gate, the
test plan, and the Task Log / Open-Questions scaffold. Cross-checked every FR acceptance criterion
and every binding pin against a concrete task item, then ran adversarial fabrication checks (file
existence, verbatim reuse-string existence in task-builder source, stale-token operativeness).

Disk-grounded verifications performed (not assumed):
- All 8 research files, all 5 source edit-targets, all 11 referenced test files EXIST.
- `tests/cli/reflect/` exists; `tests/reflect/` (stale path) absent — OQ-1 honored on disk.
- The 4 byte-exact reuse strings the task tells the executor to copy VERBATIM all exist in
  `src/superclaude/skills/task-builder/SKILL.md`: recommendation literal (em-dash, :881),
  regression halt string (em-dash, :1268), `[HALT-MONOTONICITY] |F|=<n>` (:1267), closed exhaust
  vocab (:882). The "PR-02 / Retry Monotonicity Protocol" label is real (:1263).

---

## §1. FR-RFMERGE.1–.7 Coverage

| FR | Requirement | Implementing task item(s) | Acceptance criteria reflected? | Status |
|----|-------------|---------------------------|-------------------------------|--------|
| FR-RFMERGE.1 | P1 `## Execution Context` block | Ph3 Steps 3.1 (block), 3.2 (emit-iff-≥1-ref + References-only degrade), 3.3 (phase-template mirror), 3.6/3.7 (tests) | Yes — no file paths, no `Ensuring:`, AC stays authoritative, reuse TB sub-fields, deterministic emission, phase-template assertion all present | COVERED |
| FR-RFMERGE.2 | P2 bounded patch loop (retained) | Ph5 Steps 5.1 (loop + PR-02 guards + 2-total cap), 5.2 (iteration state + sc:task delegate), 5.3 (Stage-10.5 non-overlap), 5.6/5.7 (tests) | Yes — full-set re-validation, monotonicity+regression precedence, 2-total cap (NOT 3), disjointness predicate all present | COVERED |
| FR-RFMERGE.3 | P3 DNSP + guards | Ph4 Steps 4.1 (synthetic emit), 4.2 (some-vs-zero branch / Path A), 4.3 (Stage-8 short-circuit guard), 4.6/4.7/4.8 (tests) | Yes — ≥1-success activation, zero-success→Path A no-emit, `source: synthetic-dnsp`, HIGH non-overridable, reuse-not-fork, never-block-Stage-8 all present | COVERED |
| FR-RFMERGE.4 | P4 gate-results passthrough | Ph2 Steps 2.1 (emit), 2.2 (Stage-7 inject), 2.3 (17→20), 2.6/2.7 (tests) | Yes — Stage-6 emit, plain text not JSON, PASS/FAIL+`GATE:` summary, all-pass still emits, no Stage 6.5 / no generation-evidence.json, Stage-7 injection all present | COVERED |
| FR-RFMERGE.5 | P5 advisory-only | Ph6 Steps 6.1 (advisory section), 6.2 (fence out of scored-tier path), 6.3 (mirror), 6.6/6.7 (tests) | Yes — index-level, min-2 overrides else omit, ascending T-id order, STRICT-downgrade ⚠, never mutate scored tiers, R-9 scored-tier-slice determinism all present | COVERED |
| FR-RFMERGE.6 | Accurate Stage 10.5 / `--no-reflect` representation | Ph7 Steps 7.7 (no-reflect skips 10.5), 7.8 (advisory ships all verdicts) | Partial-by-ID, full-by-content — see GAP-1 | COVERED (content), see GAP-1 |
| FR-RFMERGE.7 | Stale-token quarantine + SoT discipline | Ph7 Steps 7.5 (sc:task naming), 7.6 (stale-token-prevention test); SoT discipline in every sync/verify step + Key Constraints | Partial-by-ID, full-by-content — see GAP-1 | COVERED (content), see GAP-1 |

**Finding:** All 7 FRs have implementing items with acceptance criteria reflected. FR-6 and FR-7 are
not referenced by their literal IDs anywhere in the task (0 hits each), but their acceptance
criteria are fully implemented behaviorally (carried-gap tests 7.7/7.8 = FR-6 AC; stale-token +
sc:task tests 7.5/7.6 + SoT discipline = FR-7 AC). Logged as GAP-1 (MINOR — traceability, not
coverage).

---

## §2. Binding Pins R-1..R-16

| Pin | Binding requirement | Honored where | Verdict |
|-----|---------------------|---------------|---------|
| R-1 | Stage-7 P3 exhaust-point = `retry-1` (single-retry ladder) | Ph1 1.6 (pin design note), Ph4 4.1 (`dedup_key`=`["<stage7_affected_range>","retry-1"]`), header L79 | HONORED |
| R-2 | P1 attaches to per-task BODY, NOT index | Ph3 header (L251: "task body, NOT index-level"), 3.1, gate lens 3.G6 (no-conflation-with-P5) | HONORED |
| R-3 | P5 advisory = index-level (Stage 4, after Feedback Collection Template) | Ph6 header (L459: "INDEX-LEVEL"), 6.1 | HONORED |
| R-4 | P1 emit-iff-≥1-resolvable-roadmap-ref + References-only degraded, reuse 4.1c gate | Ph3 3.2 (verbatim rule, reuse existing 4.1c resolve/None gate) | HONORED |
| R-5 | P4 gate-results.txt format (`CHECK <n> PASS/FAIL`, `GATE: PASS (20/20)`) | Ph2 2.1 (exact format), 2.6 test asserts `CHECK ` + `GATE: PASS (20/20)` | HONORED |
| R-6 | 17→20 hygiene at `:1597` | Ph2 2.3 (single-token surgical fix), 2.7 test forbids `all 17 checks` | HONORED |
| R-8 | P2 disjointness predicate + test | Ph5 5.3 (`set(P2_loop_findings) ∩ set(stage_10_5_reflect_pre_findings) == ∅` + 3 levers), 5.7 test | HONORED |
| R-9 | P5 determinism = scored-tier-slice (NOT whole-bundle `==`) | Ph6 6.7 (explicit: "assert `==` on the SCORED-TIER SLICE, not the whole bundle"; "must NOT assert whole-bundle byte-equality across differing feedback logs") | HONORED |
| R-10 | Stay-green audit suites | Ph8 8.4 (test_task_builder_merge), 8.5 (test_inherited_verdict_freshness_inv_002 + test_five_axes_overlay), 8.6 (test_verify_sync_hooks), 8.2 (PRD/autowire), 8.3 (reflect CLI) — all R-10 suites present | HONORED |
| R-11 | M4 source-fidelity satisfied at build's own gates (not per-phase) | Ph9 Step 9.5 (records R-11 satisfied by 8.G7 FR/R coverage table); per-phase gates use M3 | HONORED |
| R-12 | Stale-token-prevention test set incl. `/config/.claude` | Ph7 7.6 (asserts `sc:task-unified`, `/rf:`, `.gfdoc`, `llm-workflows`, `/config/.claude`, `StageError` absent) | HONORED |
| R-13 | `--spec` bounded edit + HALT OQ | Ph1 1.6 (capture verbatim), Ph7 7.1 (bounded behavior-preserving §49-57 edit), 7.2 (removal-path `needs_human_decision` MUST-HALT, recorded in task OQ NOT source) | HONORED |
| R-14 | Tier-classification mirror + sync discipline | Ph3 3.3 / Ph6 6.3 (mirror edits), every phase has sync-dev + verify-sync steps | HONORED |
| R-15 | gate-results.txt vs write-atomicity | Ph2 2.1 (explicit: "consistent with write-atomicity… serializes the gate that just ran") | HONORED |
| R-16 | DM-003 = 7 named fields (`dedup_key` 2-element) | Ph1 1.5 (7 named fields enumerated), Ph4 4.1 (all 7 fields verbatim) | HONORED |

Note: R-7 (line-count = 1631, cosmetic off-by-one) is not a behavioral pin; the task correctly
instructs anchor-by-verbatim-text rather than trusting absolute numbers (L160, L174), which
subsumes R-7. No gap.

**Finding:** All 16 binding pins are honored. The two highest-risk pins — R-1 (`retry-1`) and R-9
(scored-tier-slice, not whole-bundle) — are reproduced with explicit, correct framing. R-2 (body
vs index) is reproduced AND defended by a dedicated QA lens (3.G6) against P5 conflation.

---

## §3. Fabrication Check (adversarial)

Searched for task items referencing files/patterns/requirements NOT present in research/spec.

- **File targets:** All 5 source edit-targets and all 11 referenced test files exist on disk
  (verified). Zero fabricated paths.
- **Reuse strings:** All 4 byte-exact strings the task instructs the executor to copy verbatim
  (recommendation literal, regression halt string with em-dash, `[HALT-MONOTONICITY]` token, closed
  exhaust vocab) exist verbatim in `task-builder/SKILL.md`. The "PR-02 Retry Monotonicity Protocol"
  label the task reuses is the real source label (`:1263`). NOT fabricated.
- **Stale tokens:** `sc:task-unified` (4 hits), `StageError` (6), `generation-evidence.json` (3),
  `Stage 6.5` (3) all appear ONLY in prohibition/negative context (things to avoid, test against, or
  reject) — never as operative edit targets. Correct quarantine.
- **Disk-correct path discipline:** Step 7.6 explicitly NOTEs the staleness-model path is
  `tests/cli/prd/test_prompts.py` NOT `tests/tasklist/test_prd_prompts.py`; Steps 8.3/8.10 pin
  `tests/cli/reflect/` NOT `tests/reflect/`. These are precise, disk-verified — the opposite of
  fabrication.

**Finding:** No fabrication. Every action is grounded in research/spec/source. This is the
strongest dimension of the task.

---

## §4. Research-Identified Edge Cases in Verification Criteria

| Edge case | Required by | Reflected in task? | Where |
|-----------|-------------|--------------------|-------|
| P3 zero-success → all-agents-fail, NO synthetic emit | spec §4.5 Path A, R-1 | YES | Ph4 4.2 (explicit zero-success no-emit), 4.7 test `test_dnsp_all_agents_fail_escalates`, gate lens 4.G3 |
| P5 <2 overrides → omit whole section | spec FR-5, R-3 | YES | Ph6 6.1 ("renders ONLY when ≥2… else the WHOLE section is omitted"), 6.6 test asserts min-2 threshold |
| P4 all-pass gate still emits gate-results.txt | spec FR-4, R-5/R-15 | YES | Ph2 2.1 ("emitted EVEN ON an all-pass gate"), 2.6 test "all-pass-still-emitted directive", gate lens 2.G2 |
| P2 regression-over-monotonicity precedence | spec FR-2, PR-02 | YES | Ph5 5.1 (regression "with precedence over the monotonicity check"), 5.6 test |
| P3 synthetic IS a finding → Stage-8 short-circuit must not swallow it | research/03 §1.5, /04 | YES | Ph4 4.3 (guard short-circuit when synthetic present), gate lens 4.G5 (silent-pass prevention) |
| P5 feedback-log absent on first run | research/04 §P5 | YES | Ph6 6.1 ("best-effort, read-only — the file may be absent on first run"), gate lens 6.G6 (first-run robustness) |

**Finding:** All four explicitly-named edge cases (P3 zero-success, P5 <2 omit, P4 all-pass emit)
plus two additional research-identified ones are reflected in both the implementation prose AND the
test/QA-lens verification criteria. No edge case dropped.

---

## §5. Dependency Ordering (spec §4.6)

spec §4.6 order: (1) docs+decisions [done by parent] → (2) P4 + P1 [parallel] → (3) P3 → (4) P2 +
P5 [P2 depends on 3] → (5) tests.

Task phase order: Ph2=P4 → Ph3=P1 → Ph4=P3 → Ph5=P2 → Ph6=P5 → Ph7=cross-cutting → Ph8=tests.

The task linearizes §4.6's two parallel groups (P4‖P1, P2‖P5) into sequential phases but PRESERVES
every dependency edge:
- P4 before P1: matches §4.6 step-2 ordering (P4 listed first, lowest risk — task header L184 cites
  this rationale explicitly).
- P3 (Ph4) before P2 (Ph5): §4.6 step-4 says P2 "depends on 1, 3" → P2-after-P3 honored.
- P5 (Ph6) after its only dep (docs): satisfied.
- Tests last (Ph8) after all features: matches §4.6 step-5.

**Finding:** Phase ordering is dependency-correct. Linearization of parallel groups is a valid
serialization, not a reordering violation. No gap.

---

## §6. Reuse-Not-Fork Contracts (DM-003, Execution Context, PR-02) Reproduced vs Paraphrased

| Contract | Reproduced verbatim? | Evidence |
|----------|----------------------|----------|
| DM-003 synthetic-dnsp (P3) | YES | Ph1 1.5 enumerates all 7 named fields + fixed values + closed vocab; Ph4 4.1 copies them verbatim; the recommendation literal with em-dash and the `retry-1` exhaust-point are pinned byte-exact. Confirmed against task-builder/SKILL.md:873-911. |
| `## Execution Context` 3-subfield (P1) | YES | Ph1 1.5 + Ph3 3.1 pin References/Source areas/Key constraints + "no file:line in header" rule + TB-Add-7, reused not renamed. Gate lens 3.G2 = "contract-reuse fidelity". |
| PR-02 Retry Monotonicity (P2) | YES | Ph1 1.5 + Ph5 5.1 pin the byte-exact `[HALT-MONOTONICITY] |F|=<n>` + regression string with em-dash + 4-step ordering `regression → monotonicity → hard-cap → proceed` + F-set post-dedup cardinality. Confirmed against task-builder/SKILL.md:1261-1305. |

Each phase that reuses a contract carries a dedicated "no-fork" QA lens (3.G2, 4.G2 DM-003 fidelity,
4.G6 map-not-copy, 5.G2 PR-02 fidelity) and the task header (L71, L126) declares forking any of
these a HALT condition. The em-dash (`—` not `-`) is called out explicitly in 4 places.

**Important nuance correctly handled:** P2's cap is 2-total (1 re-patch), NOT task-builder's 3-cap.
The task reuses the PR-02 *guard semantics* verbatim while legitimately overriding only the *cap
value* (adversarially-adopted per adversarial-validation.md:141). Ph5 5.1/5.6 + gate lens 5.G3
("cap-arithmetic… NOT task-builder's 3-cap") pin this distinction. This is a correct
reuse-with-bounded-override, not a fork — and the task makes the boundary explicit.

**Finding:** All three contracts are reproduced byte-exact, not paraphrased. The one intentional
deviation (P2 2-cap vs 3-cap) is spec-authorized and explicitly fenced.

---

## §7. Gaps

### GAP-1 [MINOR] — FR-6 / FR-7 not traceable by literal ID
FR-RFMERGE.6 and FR-RFMERGE.7 are referenced 0 times by their literal IDs in the task file, whereas
FR-1..FR-5 are each cited by ID. Their acceptance criteria ARE fully implemented behaviorally
(no-reflect/Stage-10.5 carried-gap tests 7.7/7.8 satisfy FR-6 AC; sc:task-naming + stale-token tests
7.5/7.6 and pervasive SoT discipline satisfy FR-7 AC), so this is a **traceability** weakness, not a
coverage gap. A future reviewer auditing FR-by-FR cannot grep "FR-RFMERGE.6" to find its
implementation. Severity MINOR: the work is present; only the explicit backward link is absent. (The
Phase 8 domain-accuracy lens 8.G7 does claim an "FR-by-FR + R-by-R coverage table" per Step 9.5,
which would surface this at execution time — partial mitigation.)
**Recommendation:** add an FR-6/FR-7 ID citation to the Phase 7 carried-gap/hygiene step prose
(one phrase each), or rely on the 8.G7 coverage-table lens to enumerate them. Non-blocking.

### GAP-2 [MINOR] — R-7 (1631 line count) not explicitly cited
R-7's resolution (SKILL.md = 1631 lines, R01's "1632" is off-by-one) is not cited. This is fully
mitigated by the task's standing instruction (L160, L174) to locate anchors by verbatim line text
rather than absolute number, which makes the exact line count irrelevant to correctness. Severity
MINOR / arguably N/A. **Recommendation:** none required; the anchor-by-text discipline subsumes R-7.

### GAP-3 [MINOR] — P3 `affected_range` map-vs-fork boundary relies on a research §ref not re-pinned in-line
Ph4 4.G6 instructs the no-fork lens to read "research/03 §1.8 (reuse-vs-map boundary) + §1.9 (no
typed StageError)". The task correctly frames `affected_range` re-binding to the Stage-7 fan-out
unit as a "legitimate map, not a fork" (4.1) — this is sound — but the precise boundary of what may
be mapped vs what must be copied verbatim is delegated to a research section rather than restated
in the item. If research/03 §1.8/§1.9 are imprecise, the executor inherits that. Severity MINOR:
the framing in 4.1/4.2 is itself correct and self-contained; the §ref is belt-and-suspenders.
**Recommendation:** none blocking; optionally inline the one-sentence map-vs-copy rule into 4.1.

**No CRITICAL or IMPORTANT gaps found.** The three gaps are all MINOR and all traceability/polish,
not coverage or correctness. The adversarial mandate to find ≥3 alignment gaps is met (GAP-1/2/3),
but in candor none of them represents a dropped or misrepresented finding — they are
citation-completeness nits against an otherwise faithful task.

---

## Cross-Validation Summary

| Dimension | Result |
|-----------|--------|
| FR-RFMERGE.1–.7 coverage | 7/7 implemented w/ acceptance criteria (FR-6/7 by content, GAP-1) |
| Binding pins R-1..R-16 | 16/16 honored (R-7 subsumed by anchor-by-text) |
| Fabrication | None — all files, reuse strings, labels verified real |
| Edge cases | All 4 named + 2 extra reflected in verification criteria |
| Dependency ordering | §4.6 preserved (valid linearization) |
| Reuse-not-fork (DM-003 / Exec Context / PR-02) | Reproduced byte-exact; P2 2-cap override spec-authorized |
| Stale-token quarantine | Correct (all in negative context) |
| Disk-path discipline | Precise (tests/cli/reflect, tests/cli/prd/test_prompts) |

---

## VERDICT: PASS

All seven FR-RFMERGE acceptance criteria and all sixteen binding pins (R-1..R-16) have corresponding,
faithfully-framed task checklist items. No task item fabricates actions ungrounded in research/spec:
every referenced file exists, every byte-exact reuse string exists verbatim in the cited source, and
every stale token appears only in prohibition context. Research-identified edge cases (P3
zero-success no-emit, P5 <2-override omission, P4 all-pass emission) are reflected in both
implementation prose and test/QA-lens verification criteria. The §4.6 dependency order is preserved.
The DM-003 / Execution Context / PR-02 reuse contracts are reproduced byte-exact (em-dash included),
with the one intentional P2 2-cap-vs-3-cap deviation correctly spec-authorized and explicitly fenced.

Three MINOR gaps were identified under the adversarial mandate (GAP-1 FR-6/7 ID traceability; GAP-2
R-7 line-count not cited but subsumed; GAP-3 P3 map-vs-fork boundary delegated to a research §ref).
None is a dropped or misrepresented finding; all three are citation-completeness polish that do not
block execution. The task is research/spec-aligned.

**Severity-rated gaps:** GAP-1 MINOR, GAP-2 MINOR, GAP-3 MINOR. No CRITICAL/IMPORTANT. PASS stands.
