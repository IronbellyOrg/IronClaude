# Cross-Validation Analysis Report

**Analysis type:** completeness-verification (cross-validation lens)
**Topic:** QA/reflect hardening — task-builder single track vs PR #209 F1-F4 (FX1/FX2/FX3/FX5/FX7)
**Date:** 2026-07-03
**Files analyzed:** 7 research files (01-07)
**Lens:** Cross-file consistency — contradictions, conflicting counts, divergent symbol descriptions
**Stance:** Adversarial

---

## Scope

Cross-validate claims BETWEEN research files 01-07. Reconcile six specific tension points:
1. F1-F4 status (already-fixed vs live)
2. FX7 exemption conflict (verification_ran:false vs _VERIFICATION_SKIP_EXEMPTIONS; degrade routing)
3. FX2 home (04 augment group vs 07 doc-QA scope-expansion tension)
4. FX1 taxonomy (5th-category forbidden; advisory parallel artifact)
5. FX5 mechanism (05 pytest_generate_tests vs 02 registry-anchored collector; helper-set)
6. Verification commands / helper counts / symbol line numbers consistency

---

## Method

Read all 7 research files fully. Spot-checked every load-bearing cross-file
claim against the actual worktree code at HEAD `46a787da` (origin/master
`156f2829`) to adjudicate divergences. Code checks performed:
`questions.py` field/def line numbers, `contract.py` exemption + verdict
routing, `ensemble.py` builder hardcoded fields, `rf-qa-qualitative.md`
charter vs task-qualitative Code Compatibility group, `deviation-taxonomy.md`
4-category invariant, `reflect-reviewer.md` return-only/persona_lens.

---

## Tension 1 — F1–F4 status (already-fixed vs live)

**VERDICT: FULL AGREEMENT. No cross-file contradiction.**

| File | Claim | Consistent? |
|---|---|---|
| 01 (FX3) | "The `questions.py` in this worktree is the **already-FIXED** version of F3" (headline, L16). FX3 = "regression backstop." | ✓ |
| 02 (FX5) | "The current worktree ALREADY carries the F4 fix … FX5 is a REGRESSION LOCK, not a first-fix" (L6, §2.1 L129). | ✓ |
| 05 (tests) | FX3/FX5 "authored to PASS against the current (post-F1–F4-fix) tree and FAIL only on regression" (L184). | ✓ |
| 07 (doc-xval) | HL-2: "F1–F4 are ALREADY FIXED at worktree HEAD → FX2/FX3/FX5 are REGRESSION-GUARDS" (L35, L104, L217-220). | ✓ |

**No file implies F1–F4 are live.** All four converge: the fixes shipped via
`f6a32e9a`/`21d4b8e0` on this branch; the new artifacts are recurrence-guards.
Independently confirmed against code: `questions.py:136` carries the fix
`_evidence_attr("pr_number", answer_attr="probe_pr")`; `candidate.py:360`
`_path_resolves` carries the all-None-list collapse. Consistent.

**Cross-check with 07's HL-1 (branch fact):** 07 uniquely flags that the plan's
"contract_setup lives on master" premise is FALSE (`git ls-tree origin/master |
grep contract_setup` → 0; it lives on this branch). No other file asserts the
master-premise, so there is no contradiction — 07 corrects a *plan* claim, not a
sibling *research* claim. Confirmed: HEAD `46a787da`, origin/master `156f2829`
(matches session git status). This is a builder-critical fact (build on THIS
branch) that only 07 carries — flag for the builder, not a cross-file conflict.

---

## Tension 2 — FX7 exemption conflict (03 vs 07)

**VERDICT: CONSISTENT + COMPLEMENTARY. No contradiction; 03 supplies the
mechanism, 07 supplies the design-tension flag. Both correct against code.**

Shared, mutually-agreed facts (both files):
- The ensemble builder hardcodes `verification_ran: False` with
  `verification_skip_reason: "tool-unavailable"`, and `tool-unavailable` ∈
  `_VERIFICATION_SKIP_EXEMPTIONS` → the verification-skipped degrade (Trigger 12)
  is dodged → **vacuously-clean PASS**. (03 §3c; 07 "FX7 CONTRADICTS an existing
  deliberate exemption".)
- Line anchors agree within off-by-one: exemption set 03=`contract.py:36-38`,
  07=`contract.py:35-38` (**actual: opens at :36**, comment at :35 — both point
  to the right block). Trigger 12: 03=`:288`, 07=`:287-291` (**actual: skip_reason
  read :289, guard :290, return :291** — 07's range is exact, 03 off-by-one but
  correct block).

Where 03 goes further (NOT contradicted by 07 — 07 simply doesn't address the
routing mechanism):
- 03 §3.4 / §5: **"set status:degraded" would MISROUTE** — `status` string is only
  recognized as `success`/`failed`/`partial`; an unrecognized `"degraded"` falls
  through to `tier-mismatch` HALTED (exit-10), NOT degraded (exit-11). Degrade
  MUST route via `degraded_components` (an existing `_degraded_reason` trigger),
  not the `status` string.
- **Independently VERIFIED against code:** `contract.py:235`
  (`status == "success" … → PASS`), `:243` (`reason="tier-mismatch"` fallthrough),
  `_degraded_reason(…, degraded_components: list, …)` at `:249-252` with
  `degraded_components` membership routing at `:258-259`. 03's misroute claim and
  the `degraded_components` mechanism are **both confirmed**.
- 03's additive-safe path: change what the **ensemble BUILDER emits**
  (`ensemble.py:550-551`, `:560`) for the ensemble case; keep the **consumer**
  exemption set intact so genuine read-only-project skips still exempt.
- **Confirmed builder anchors:** `ensemble.py:492` builder, `:517`
  `reviewer_count = len(succeeded)`, `:538` `status "success"`, `:550`
  `verification_ran False`, `:551` `skip_reason "tool-unavailable"`, `:560`
  `degraded_components []`. All six exact.

07's framing: FX7 "is NOT purely additive … flag the design tension for a human
decision (why was `tool-unavailable` exempted; does making it degrade over-HALT
legitimate read-only/tool-unavailable runs?)."

**Reconciliation:** No inconsistency. 03 and 07 agree the naive FX7 spec text is
wrong; both agree `tool-unavailable` is currently exempt; both point to the same
`contract.py` locus. 03 additionally proves `status:"degraded"` misroutes and
prescribes the `degraded_components` route + builder-side (not consumer-side)
edit; 07 independently flags the same tension as human-decision. The two are the
same finding at two altitudes. **The recommended mechanism is consistent:
degrade via `degraded_components`, NOT `status:"degraded"`; edit the ensemble
builder, NOT the consumer exemption set.** This must be carried as a
needs_human_decision item (the "should the ensemble stop self-exempting" call is
a real design decision, per both files).

---

## Tension 3 — FX2 home (04 vs 07): REAL OPEN DESIGN QUESTION ⚠️

**VERDICT: NOT a factual contradiction — both files are correct at different
granularities — but their RECOMMENDATIONS genuinely diverge. This IS a real,
unresolved design question the task MUST surface and decide explicitly.**

### What both files AGREE on (verified)
- **No lens literally named `internal-consistency` exists.** 04 asserts it
  (§CRITICAL FRAMING); 07 says the lens "appears three times (lines 92, 307, 755)"
  but always as document-prose. **VERIFIED: `grep -n "internal-consistency"
  rf-qa-qualitative.md` → ZERO hits.** The three "Internal consistency" instances
  are Verification Principle #3 (`:92`), tdd-qualitative Internal Consistency group
  (`:307`), doc-qualitative item 4 (`:755`) — all document-prose. **04 and 07
  agree FX2 is NOT a clean rename of a named lens.** Consistent.
- Both agree the Five Adversarial Axes vocabulary is a **closed set**
  `{AX-1…AX-5, none}` and **no AX-6 may be added.** VERIFIED: `:639`, `:826/840`.
  04 states this explicitly; 07 does not contradict.

### Where they DIVERGE (the open question)
- **04's position:** FX2's natural home is the **task-qualitative "Code
  Compatibility" group** (`rf-qa-qualitative.md:670`, items 4–6 at `:672/:674/:676`),
  which **already reads actual functions in source files** (item 4 "read the actual
  function in the target source file … verify … the actual signature"). So adding a
  cross-symbol input-shape check there is a natural, in-scope augmentation
  (new item after 6, or augment item 5). **VERIFIED verbatim** — the Code
  Compatibility group and its code-reading items 4–6 exist exactly as 04 describes.
- **07's position:** the agent's **top-level charter** scopes it to documents:
  description line 3 = *"content-level quality assurance on assembled documents
  (PRDs, research reports, tech references) … whether the content actually makes
  sense as a product document."* **VERIFIED verbatim.** 07 therefore calls grafting
  a Python cross-symbol lens a **scope expansion**, not a rename, and recommends
  either (a) a different code-reviewing surface (`rf-qa` structural / a new code
  lens) OR (b) explicitly widening the charter.

### Adjudication
Both are factually right. The reconciliation the two files do NOT resolve between
themselves:
- The task-qualitative Code Compatibility checks today are scoped to verifying a
  **task file's described function-modifications** against real code (checking a
  task item's claims) — that is narrower than a **general cross-symbol code
  invariant lens** over sibling functions. So 07's scope-expansion caution is
  valid (the agent's *charter* is document-QA and its code-reading is currently
  in service of task-file review), AND 04's placement is valid (Code Compatibility
  is the ONE place the agent reads actual source — the least-surprising home).
- **This is a genuine open design question, not a research defect.** Both agents
  independently arrived at it; 07 explicitly flags it "for a human decision." The
  task-builder MUST NOT silently pick one. Recommended resolution to carry as a
  needs_human_decision item: adopt 04's placement (task-qualitative Code
  Compatibility group) **scoped to code claims made by task items**, while
  honoring 07's framing (note the charter is being widened from
  document-consistency to sibling-symbol code-invariant; do not over-broaden the
  agent's document mandate; annotate findings with existing **AX-2**, add no AX-6).
  If the builder/human prefers a code-native surface, 07's `rf-qa`-structural
  alternative is the fallback. **Either way, the task must state the decision.**

---

## Tension 4 — FX1 taxonomy (04 and 07)

**VERDICT: FULL AGREEMENT. No contradiction.**

- Both cite `deviation-taxonomy.md:5` ("**4 categories** … not a 5th category").
  04 adds `:131` and `:154` (§17.7 Kill List); 07 relies on `:5`. **VERIFIED:
  `:5`, `:119` ("adds **no 5th category**"), `:131` ("4 categories, not 5"), `:154`
  ("The 5th deviation category was explicitly rejected in §17.7 Kill List").**
- Both conclude FX1 MUST be an **advisory parallel artifact / finding-modifier**
  mirroring the Grounding-gaps pattern (`:129-154`), NOT a 5th gating class.
- 04 additionally grounds the *justification* for FX1: Regression is
  **spec-relative** ("A documented invariant **in the spec** … is violated"), so a
  **no-spec** invariant break has no existing home. 04 cited `:75/:82`; **actual
  content is at `:81`** (minor line drift, content correct and verified). 07 does
  not contradict this.
- Both agree `reflect-reviewer` **never gates** — it RETURNs findings, orchestrator
  persists (04 cites `:36/:55/:65`; **VERIFIED `:36`, `:55`, `:65`**), and the
  advisory slot = new `persona_lens` value (`:54`, verified) + a separate
  advisory sub-section outside the 4-class Deviations table. Consistent.

---

## Tension 5 — FX5 mechanism (05 vs 02)

**VERDICT: MINOR DIVERGENCE, RECONCILABLE. Compatible on the parametrize
mechanism; differ on the SOURCE of the helper set. Task-builder must pick;
recommend 02's registry+drift-alarm with 05's per-helper parametrize.**

| Dimension | 05 (tests-conventions) | 02 (gate-helpers) |
|---|---|---|
| Collector mechanism | `pytest_generate_tests` (Opt A) OR parametrized test module (Opt B) — per-helper red test | (compatible — 02 assumes a per-helper collector) |
| Helper-set SOURCE | **Enumerate current symbols at test time; do NOT hardcode a stale helper list** (L186-187) | **Hand-maintained registry** `GATE_LOAD_BEARING_HELPERS` (≥21 dotted names) **+ pattern-assisted drift alarm** (§4.1) |
| Helper count | (none given) | ≥21 gate-load-bearing; total helpers lockgate 14 / candidate 18 / diagnosis 14 / validation 11 |

- The apparent tension: **dynamic enumeration (05) vs hand-maintained registry
  (02).** 02 argues (§4.3) a pure name-pattern scan MISSES load-bearing helpers —
  dataclass methods (`CandidateContract.required_unobserved`,
  `ValidationReport.passed`) and the `*_checks` builder family — whose names carry
  no `resolve`/`observed` token. That is a real blind spot for a naive dynamic
  scan and the core reason 02 wants an explicit registry.
- **Reconciliation:** compatible, not contradictory. 02's design already answers
  05's staleness concern via its **drift alarm** (AST-walk the 4 modules; FAIL if a
  gate-shaped `def` is not in the registry) — that prevents the registry from
  silently rotting, which is exactly what 05's "don't hardcode a stale list"
  guards against. And 05's `pytest_generate_tests`/parametrize is a *mechanism*
  that can enumerate EITHER a registry OR a dynamic set. **The two compose:
  registry (02) as the source of truth + drift-alarm (02) to catch new helpers +
  per-helper parametrize (05) as the reporting mechanism.**
- **Recommendation to carry:** prefer 02's registry+drift-alarm over 05's
  pure-dynamic enumeration, because a pure AST-name scan demonstrably misses the
  dataclass methods and `*_checks` family that ARE gate-load-bearing (02 §4.3).
  Use 05's `pytest_generate_tests` as the parametrize vehicle. No helper-count
  conflict (05 gives none; 02's ≥21 stands). This is a design choice, not a
  blocking contradiction.

Cross-check: 02 and 05 AGREE on the anti-gaming core — a negative test is not
enough; a **differential (mutation) test** must exist per gate helper (02 §5; 05
L174-180). 05 confirms the F4 pair already exists
(`test_severity_path_all_none_does_not_resolve` + differential) so FX5 PASSes for
that helper and catches others. Consistent.

---

## Tension 6 — Line numbers / counts / commands consistency

**VERDICT: CONSISTENT on all load-bearing anchors. Three MINOR line-cite nits
(non-blocking; none changes a conclusion).**

**Consistent (verified):**
- `questions.py`: `_evidence_attr` def L64 (01 & 07 ✓, actual :64); probe_pr
  deriver L133-139 (01 & 07 ✓); `augment_app_slug` L28 (01 & 07 ✓, actual :28);
  SetupAnswers 17 fields (01) — class at :15.
- `candidate.py`: `_path_resolves` :360 (02 & 07 ✓); `MUST_OBSERVE_FIELDS` :18-25
  (02 & 07 ✓); `_findings_locus` :253, `_review_completeness_signal` :290,
  `required_unobserved` :47, `_selected_app_slug` :161 (02); list-branch region
  02=`:369-376` vs 07=`:365-376` (overlapping, same block — non-conflicting).
- `lockgate.py`: `_paths_resolve` :119 gate #6 (02 & 07 ✓); `LockGate.evaluate`
  :42, 12 checks (02); wired as check-id (07).
- `diagnosis.py`: `diagnose()` :63, `_evidence_sha256` :294 (02 & 07 ✓);
  `_stale_blockers` :334, `_resolve_optional_path` :285 (02).
- `evidence.py`: `EvidenceBundle` :18-37 / 13 attrs (01); `load_evidence` :56 with
  dir-guard :59-60 (07). Non-overlapping, consistent.
- `contract.py`: exemption block & Trigger 12 (see Tension 2 — both correct block).
- HEAD `46a787da` / origin/master `156f2829` (07) — VERIFIED, matches session.
- Verification commands: `uv run pytest tests/pr_submit/ -v` + scoped
  `ruff check` AND `ruff format --check` (05 §4); `uv run pytest tests/...` L3
  test items (06 §I18). 05 and 06 agree `make sync-dev`/`verify-sync` are NOT
  triggered by test-only additions but verify-sync is a CI gate. Consistent.
- deviation-taxonomy 4-category / Grounding-gaps (04 & 07 — see Tension 4). ✓

**Minor nits (non-blocking, flagged for evidence hygiene):**
1. **07 probe_pr field line = `questions.py:22`; ACTUAL = `:19`** (01 correct at
   L19). Off by 3. Does not affect any conclusion (both agree field EXISTS and
   `pr_number` does not).
2. **03 Trigger-12 cite `:288`; ACTUAL `:289-291`** (07's `:287-291` is exact).
   Off-by-one; correct block.
3. **04 Regression spec-relative cite `:75/:82`; ACTUAL content at `:81`.**
   Content correct; line drift only.

None of these three alters a load-bearing finding; they are citation-precision
nits, not contradictions.

---

## Contradiction ledger (adversarial summary)

| # | Candidate contradiction | Real? | Resolution |
|---|---|---|---|
| C1 | F1–F4 live vs fixed | **NO** | All 4 files agree: fixed at HEAD; artifacts are regression-guards. |
| C2 | FX7 degrade routing (03 vs 07) | **NO** | Same finding, two altitudes. Mechanism consistent: `degraded_components`, not `status:"degraded"`; edit builder, not exemption set. |
| C3 | FX2 home (04 in-scope vs 07 scope-expansion) | **NO (factual) / YES (recommendation)** | Both correct at different granularities. **Genuine open design question** — must be a needs_human_decision item. |
| C4 | FX1 5th category | **NO** | Both agree: no 5th class; advisory parallel artifact. |
| C5 | FX5 registry (02) vs dynamic (05) | **NO (reconcilable)** | Compose: registry+drift-alarm (02) + per-helper parametrize (05). Design choice. |
| C6 | Line-number cites | **NO** | 3 minor off-by-N nits; no conclusion changes. |

**Zero blocking cross-file factual contradictions.** Every load-bearing fact
asserted by one file is corroborated (not contradicted) by the others and by the
code. The two recommendation-level divergences (C3, C5) are correctly surfaced by
the researchers themselves.

---

## Open questions the task MUST carry (needs_human_decision)

These are NOT cross-file conflicts to resolve here — they are design decisions the
research correctly leaves open and the builder MUST NOT auto-default (per project
rule: human-decision items HALT, never ship a silent default):

1. **FX2 surface + charter scope (C3).** Augment task-qualitative Code
   Compatibility group in `rf-qa-qualitative.md` (04) — accepting an explicit
   charter-widening note (07) — OR target `rf-qa` structural / a new code lens
   (07 alt). Decision required before FX2 items are authored. No AX-6; annotate
   AX-2. Update the "15 items"→16 count (`:660`) + Adaptation Guidance table
   (`:699-715`) + partition note (`:738`) if the Code-Compatibility augmentation
   is chosen.
2. **FX7 additive mechanism (C2).** Confirm the additive-safe route: emit degrade
   via `degraded_components` from the ensemble **builder** (`ensemble.py:550-551`,
   `:560`); do NOT set `status:"degraded"` (misroutes to HALTED/exit-10); do NOT
   remove `tool-unavailable` from `_VERIFICATION_SKIP_EXEMPTIONS` (consumer
   behavior change). Human call: should the ensemble path stop self-exempting at
   all (over-HALT risk for legitimate read-only runs)?
3. **FX5 collector source (C5).** Registry+drift-alarm (02, recommended) vs
   pure-dynamic enumeration (05). Registry preferred because a naive AST-name scan
   misses `required_unobserved`/`ValidationReport.passed`/`*_checks`.

## Builder-critical facts (carry forward; only one file each)
- **Branch (07 HL-1):** build FX3/FX5 on THIS branch
  (`harden/qa-reflect-blindspot-pr209`) / its `DetectionContractBranch` base —
  NOT off `origin/master` (zero `contract_setup` there). VERIFIED.
- **Wording (07 HL-2):** word FX2/FX3/FX5 items as "prevent recurrence / guard the
  fix," NOT "fix the live bug." All F1–F4 fixed at HEAD.
- **SoT (04 §5):** edit only `src/superclaude/…`; `make sync-dev` →
  `make verify-sync`; never edit/stage `.claude/` mirrors.
- **Gate wiring (04 §2, 06 §3):** the "any gap = FAIL" Phase-2/Phase-4 wiring lives
  in `task-builder/SKILL.md` §A.8/§A.10 (out of the agent-file scope) — the builder
  must wire FX3 (Phase-2 prerequisite) / FX5 (Phase-4 FAIL) there, mirroring the
  per-phase Verdict FAIL-rule shape (`rf-qa-qualitative.md:732-735`).

---

## VERDICT: PASS

**Cross-file consistency holds.** Zero blocking factual contradictions among the 7
research files; every load-bearing claim is mutually corroborated and
code-verified at HEAD `46a787da`. The set is internally coherent and safe to build
on.

PASS is qualified, NOT unconditional: it means "no contradictory facts," NOT "no
decisions remain." **Three design decisions (FX2 surface, FX7 mechanism, FX5
collector source) MUST be carried into the task as explicit needs_human_decision
items** — they are correctly-surfaced open questions, not research defects. The
task-builder must not silently auto-default any of them. Three minor citation nits
(07 probe_pr `:22`→`:19`; 03 Trigger-12 `:288`→`:289-291`; 04 Regression
`:75/:82`→`:81`) are non-blocking evidence-hygiene notes.

**Gap list (if treated as FAIL by a stricter gate):** none are cross-file
contradictions; the only items a downstream gate might treat as blocking are the
three needs_human_decision design questions above — which are correctly the
task's to resolve, not the research's.

*Analyst: rf-analyst (cross-validation lens). Read-only on research files; no
research/synthesis file modified.*
