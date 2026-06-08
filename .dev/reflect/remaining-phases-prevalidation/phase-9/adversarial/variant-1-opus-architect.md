# Variant 1 — opus:architect — Phase 9 Unchecked-Item Review

**Stance:** Systems/structural correctness, sequencing, step-count budget, contract-mechanism coherence with what 9.1–9.10 actually built.

**Scope (ground-truth checkbox audit):** The driving prompt named 9.7–9.12 + PG9.1 + PG9.2 as "unchecked." The real task file shows **9.7, 9.8, 9.9, 9.10 are already `[x]`** with logged findings (score, merge, spec_fidelity DONE; wiring marked N/A user-approved). The genuinely unchecked items are **9.11, 9.12, PG9.1, PG9.2**. I review those four and sanity-check 9.7–9.10 only for coherence.

---

## Step 9.11 — test_strategy + certify + validate-reflect + remediation (4 secondary migrations)

**Necessity (spec):** BUILD-REQUEST §3 ("tool-write at every LLM step") says *every* `build_*_prompt` becomes a tool definition. test_strategy, certify, reflect are genuine LLM-output steps → in scope. §3 also explicitly names **`remediate`** in the phantom-ID-schema group ("schema for `merge`, `generate-*`, and `remediate` includes a `roadmap_ids` array"). So §3 mandates a `remediate` tool-write with the subset constraint. **This item is spec-required.**

**Correctness vs spec — the load-bearing defect:** The item tells the worker to "rewrite `build_remediation_prompt` (`remediate_prompts.py:17`) since it is a true LLM-output step." But `build_remediation_prompt` (verified, remediate_prompts.py L17–81) produces a prompt that instructs an agent to **edit a target file in place** ("You are a remediation specialist… apply specific, targeted fixes to a single file… you may ONLY edit the target file"). Its output is **file edits, not a structured roadmap-ID-bearing artifact**. There is no `roadmap_ids` payload to constrain here. The §3 `remediate` that needs a `roadmap_ids` subset constraint is the **roadmap-producing remediate step** (`executor.py:_run_remediate_step` L2044, which "reads deviation JSON, generates tasklist"), NOT the file-editing remediation prompt. The item conflates two different "remediate" surfaces. **REFACTOR required**: the `roadmap_ids` subset constraint (the master:§Top-3 #3 phantom-ID kill) must land on whichever remediate surface emits requirement IDs into a roadmap/tasklist artifact; a tool-write of the file-editing `build_remediation_prompt` is a parity-only migration with NO Contract #3 obligation and should be labeled as such, or deferred.

**H4 sub-action decomposition:** The H4 preamble (task L538) already mandates 9.11 be split into 9.11.a/b/c/d with per-sub-action completion criteria, individual schemas/templates/parity tests, and FAIL-isolation (a FAIL on (b) certify does not block (a)/(c)). The item body does NOT reflect this decomposition — it's written as one monolithic "repeat the pattern for the 3 secondary steps in sequence … also rewrite remediation." The body and the H4 hardening preamble are **internally inconsistent**, exactly the H3/H4-class bundling defect the preamble was added to fix. REFACTOR: rewrite the item body to enumerate 9.11.a test_strategy, 9.11.b certify, 9.11.c validate-reflect, 9.11.d remediate(roadmap-producing) + 9.11.e consolidated parity test, each individually completable, with the Contract #3 obligation pinned to (d) only.

**certify coherence with R1.3:** certify dual-write must coexist with the R1.3 CodeAssertion wiring. Step 8.3's finding shows certify is constructed+executed *dynamically* post-remediate inside `execute_roadmap` (NOT a `_build_steps` literal), guarded by `remediate_result.status == PASS`. A tool-write of `build_certification_prompt` must therefore wire through that same dynamic construction path, not `_build_steps` — the item must say so. Minor REFACTOR note.

**Step-count budget:** Adding tool-write schemas/templates/flags does NOT add pipeline *steps* — these are dual-write render paths on existing steps. So 9.11 has **zero step-count-budget impact** (Acceptance Gate #6 ≤14 is untouched). The wiring-verification N/A determination (9.10) and the verify-implementation consolidation are the only budget pressure points, both downstream in R1.5/R1.6. No budget risk here.

**Verdict: REFACTOR** — necessary, but (1) the remediate target is mis-identified (file-editing prompt has no roadmap_ids; the roadmap-producing remediate surface is the real Contract #3 target), and (2) the body must be rewritten to the H4 a/b/c/d/e decomposition the preamble already mandates.

---

## Step 9.12 — cutover criterion over ≥3 release cycles

**Necessity (spec):** §R1.4 / Vector A: "side-by-side against current markdown output for ≥3 releases each before deletion." A cutover decision document is the artifact that enforces "no premature deletion." Required.

**Correctness vs spec & coherence with H5:** H5 (task L539) already mandated `.dev/migrations/r1-4-cutover-counters.yaml` keyed by step, with `release_marker_count`, `cutover_eligible`, `cutover_at_count: 3`, premature-cutover HALT-blocked. That file **exists** (verified: 13 step entries incl. remediation, all `release_marker_count: 0`, `cutover_eligible: false`). Step 9.12's body says "release-cycle counter (starts at 0…)" inline but does NOT reference the H5 counters file as the source of truth — it re-describes a counter mechanism in prose. The item and the H5 product are **redundant/divergent**: 9.12 should *consume and assert against* `r1-4-cutover-counters.yaml`, not re-narrate the counter. REFACTOR: pin 9.12 to read `r1-4-cutover-counters.yaml`, assert every step's `cutover_eligible == false` at authoring time (0 cycles), and make the readiness verdict iterate that file — eliminating the divergent inline counter prose.

**Fragility — the "DYNAMIC item" design smell:** 9.12 is self-described as "the only DYNAMIC item in the task… updated by the worker agent as live releases accumulate." An MDTM checklist item that is meant to be re-edited across future release cycles is an anti-pattern: the task file will be archived to `done/` long before 3 release cycles elapse. The cutover decision is genuinely a *post-R1.4, multi-release* concern that cannot complete inside this task's lifetime. REFACTOR: scope 9.12 to produce the **initial** cutover-decision document (state: "0 cycles, all 13 steps dual-write, none cutover-eligible, R1.4 NOT ready for cutover — markdown remains production default") and explicitly **hand off** the per-release counter increments + eventual cutover to R1.6 / a release-cycle hook. Do not pretend a checklist item tracks live releases.

**Counter-coherence with 9.10/9.11:** The H5 yaml has a `wiring_verification` entry (count 0) even though 9.10 determined wiring is N/A (already deterministic, no dual-write, no markdown path to retire). 9.12's "all 12 steps ready for cutover" verdict logic must treat wiring_verification as **EXEMPT** (no markdown path exists to delete), matching the 9.10 finding and the PG9.1 exemption note. The item as written would mis-count wiring as a dual-write step pending 3 cycles. REFACTOR: 9.12 readiness verdict = (11 genuine dual-write steps cutover-eligible) AND (wiring_verification marked deterministic-exempt). Mirror the same in the yaml's interpretation.

**Verdict: REFACTOR** — necessary but must (1) consume the H5 yaml as SoT instead of re-narrating a counter, (2) be scoped to the *initial* decision + explicit multi-release handoff rather than a self-mutating "DYNAMIC" item, (3) treat wiring_verification as exempt to stay coherent with 9.10.

---

## Step PG9.1 — aggregate + spawn rf-qa-qualitative

**Necessity:** Phase gate; required by the task's gate cadence. The H3 hardening already inserted interim QA after 9.5 and 9.10; PG9.1 is the terminal R1.4 gate. Keep the gate.

**Correctness vs spec:** The adversarial-stance prompt embedded in PG9.1 checks (a)–(h) are well-aimed: (c) generate+merge roadmap_ids subset = Contract #3, (d) score → CONVERGENCE_THRESHOLDS = Contract #8, (e) no <3-cycle cutover = Vector A, (f) convergence/semantic_layer/structural_checkers/commands unchanged = PRESERVE, (h) markdown stays production default. These map cleanly to the spec.

**The one defect — check (a) counts "12 sub-steps":** PG9.1 check (a) asserts "12 sub-steps all have schema + template + dual-write + parity test." But the 9.10 finding established wiring_verification is legitimately EXEMPT (deterministic, no LLM, no markdown path), and the 9.11 remediate target is contested (file-editing prompt has no roadmap_ids). The literal "12 sub-steps all have schema+template+dual-write+parity" will produce a **false FAIL** on wiring (no schema/template by design) unless the exemption is encoded. The 9.10 finding pre-emptively wrote the exemption rationale to `r1-4-wiring-validation.txt` so the glob catches it — good — but PG9.1's check (a) text still says "12 … all." REFACTOR: amend check (a) to "11 genuine LLM tool-write migrations have schema+template+dual-write+parity; wiring_verification is deterministic-exempt (documented in r1-4-wiring-validation.txt); the §3 `remediate` roadmap_ids constraint lands on the roadmap-producing remediate surface, not the file-edit prompt."

**Coherence with established mechanism:** PG9.1 correctly targets rf-qa-qualitative (not plain rf-qa) — appropriate because the risk here is *semantic drift / over-constrained schemas blocking valid LLM output*, which is a qualitative judgment, not a structural pass/fail. Good fit.

**Verdict: REFACTOR (light)** — keep the gate and its adversarial stance; only fix check (a)'s "12 all" to encode the wiring exemption + the remediate-surface clarification so the gate doesn't false-FAIL on a by-design exemption.

---

## Step PG9.2 — act on R1.4 QA verdict

**Necessity:** Standard conditional act-on-verdict gate (IF PASS → proceed-decision + Phase 10; IF FAIL → fix, re-spawn, max 3 cycles, then HALT+escalate). Required.

**Correctness vs spec:** The branch logic is the established L5 conditional-action pattern used by every prior PG. The max-3-cycle-then-HALT for a *qualitative* gate matches I16. The proceed-decision content ("12 steps dual-write, cutover deferred to live release cycles") is coherent with the 9.12 deferral and Vector A.

**One coherence note — Phase 10 sequencing trap:** PG9.2 says "proceed to Phase 10 (R1.5)." Phase 10's own preamble (H2 fix, task L603) warns R1.5 `verify-implementation` MUST NOT ship before R1.6 Step 11.4 (fail-open default deletion) or a one-cycle fail-open window opens. PG9.2 proceeding to Phase 10 is fine *as a task-execution order* (building ≠ shipping), but the proceed-decision should carry the H2 sequencing constraint forward so it isn't lost. Minor REFACTOR: add to PG9.2's proceed-decision a one-line carry-forward of the H2 Phase10-before-11.4 shipping constraint.

**Verdict: KEEP** (with an optional one-line H2 carry-forward note; not blocking).

---

## Architect's phase-coherence summary

The four unchecked items are all **necessary** and faithfully serve §R1.4/§MVR §3. The defects are **specification-precision and bundling-consistency**, not missing/superseded work:
1. **Highest impact:** 9.11's `remediate` target is mis-identified — the file-editing `build_remediation_prompt` carries no `roadmap_ids`, so wiring the master:§Top-3 #3 phantom-ID kill there would be a no-op. The §3 constraint must land on the roadmap/tasklist-producing remediate surface.
2. 9.11 body doesn't reflect its own H4 a/b/c/d decomposition.
3. 9.12 re-narrates a counter instead of consuming the H5 yaml, and is mis-scoped as a self-mutating "DYNAMIC" item rather than an initial-decision + handoff.
4. PG9.1 check (a)'s "12 all" will false-FAIL the by-design wiring exemption.
No DISCARDs. No step-count-budget risk (dual-write adds render paths, not steps).
