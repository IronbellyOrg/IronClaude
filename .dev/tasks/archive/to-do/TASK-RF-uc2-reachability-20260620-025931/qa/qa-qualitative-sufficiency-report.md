# QA Report — Task Qualitative Review (QA-Gate Sufficiency + Fail-Loud Doctrine)

**Topic:** TASK-RF-uc2-reachability-20260620-025931 (FR-RSR additive UC-2 reachability escalation)
**Date:** 2026-06-20
**Phase:** task-qualitative
**Lens:** qa-gate-sufficiency-and-doctrine
**Fix authorization:** false (REPORT ONLY)
**Fix cycle:** N/A

---

## Overall Verdict: PASS

This is a task-qualitative review under a focused lens (QA-gate sufficiency + fail-loud
doctrine + scope discipline), not the full 15-item checklist. Both lens halves were checked
against the live spec/TDD/SKILL.md/eval-workspace source. No CRITICAL, IMPORTANT, or MINOR
issue rose to the bar of a FAIL on either lens half. Three sub-threshold observations are
recorded below as advisory NOTES (not findings, not gating) — they document residual nuance,
not defects in the plan.

I held an adversarial stance throughout (assumed the tasklist contained errors and tried to
break each doctrine claim against source). The plan survived. Evidence trail is in
"Verification performed" and the Self-Audit.

---

## Adversarial Axes annotation

Axis vocabulary applied per row: `{AX-1 drift, AX-2 contradictions, AX-3 omissions,
AX-4 weakened-criteria, AX-5 invented-content, none}`. The driving GOAL verbatim WAS
available (task References block line 118: "Build the additive UC-2 reachability escalation
for sc-reflect-protocol ... exactly the scope of the authoritative TDD") AND the BUILD-REQUEST
GOAL was readable — so AX-1 Drift is ACTIVE for this review (NOT `drift-axis-inactive`).

---

## Items Reviewed (lens-scoped)

| # | Lens check | axis | Result | Evidence |
|---|-----------|------|--------|----------|
| A1 | FINAL M3 gate has >=6 distinct lens agents (3 rf-qa + 3 rf-qa-qualitative) | none | PASS | PG.2-PG.7 = 3 rf-qa (skill-conformance, blocker-counter, evidence-citation) + 3 rf-qa-qualitative (fail-loud, eval-falsifiability, no-scope-expansion); all distinct embedded lenses |
| A2 | Serialized fix authorization (I20) | none | PASS | PG.2-PG.7 ALL `fix_authorization: false`; PG.9 spawns EXACTLY ONE `rf-qa` `fix_authorization: true` ("NO other fix agent concurrently"); PG.10 verification round |
| A3 | Adversarial framing in embedded gate prompts | none | PASS | Each of PG.2-PG.7 carries "Assume this change has at least 5 errors ... A 0-issue verdict requires proof of exhaustive checking" |
| A4 | Per-phase verify embeds spec §3 boxes + §6 NFR + TDD §24.1 DoD + sync | none | PASS | Steps 2.2/3.4/4.2/5.3/6.3 each cite spec §3 acceptance line ranges + spec §6 NFR + TDD §24.1 DoD line + `make sync-dev`+`verify-sync`; matches BUILD-REQUEST per-task DoD (a)(b)(c)(d) at BR:88-91 |
| B5 | Degrade-default doctrine (all uncertainty -> DEGRADE -> §10.6, never blocking Regression, never silent PASS) | none | PASS | Encoded in Steps 2.1/2.2/3.2/6.2; matches spec FR-RSR.3 AC (spec:332-342) + FR-RSR.4 partial-rootwalk=DEGRADE (spec:355-370); asymmetric-cost default explicit |
| B6 | Symbol-anchored tagger (requirement_id nullable; sweep runs regardless; kind-fail -> DEGRADE) | none | PASS | Step 3.1: keyed off resolved symbol KIND, `requirement_id` OPTIONAL/null, "sweep still runs", kind-resolution failure -> DEGRADE not silent-skip; ledger schema `requirement_id: str \| None` (Step 2.1) |
| B7 | Counter hygiene (increment ONLY deviation_count_by_class.regression, never verification_regressions_detected) | none | PASS | Step 5.1/5.3: "increments ONLY deviation_count_by_class.regression (NEVER verification_regressions_detected, exit-code-sourced)"; matches spec FR-RSR.6 (spec:415-416, 432-433) |
| B8 | No scope expansion past TDD (no 5th class, no new counter, no new CLI flag, no whole-program proof) | AX-5 | PASS | PG.7 lens enforces TDD §18.2-only; §17.7 kill-list item 6 (SKILL:1799) confirms no-5th-class is a live invariant; no new counter/flag/call-graph in any item. Inverse-AX5 check: no invented artifact found |
| B9 | Headline eval `status: active`, REAL fixtures, FAIL-pre/PASS-post; skeletons green+unmodified | none | PASS | Step 7.2 (active headline, real git diff, FR-S9-04 re-enactment), 7.8/7.9 dual-snapshot FAIL-pre/PASS-post; ids 19/20 (T2-converges-on-wrong, T2-judge-class-collision) "stay green and unmodified" (verified present in evals.json) |
| B10 | §5.3 pre-filter gates on SUCCESSFUL sweep; degrade-only does NOT force T2 but Grounding Gap forces status:partial | none | PASS | Step 4.1/4.2: trigger `runtime_surface_unreached >= 1` from SUCCESSFUL sweep; degrade-only (==0) does NOT force T2; matches spec FR-RSR.5 AC (spec:394-403) verbatim |

---

## Lens A — QA-gate sufficiency (detailed)

**A1 — >=6 distinct lens agents: PASS.** The single FINAL gate (Phase Gate PG.1-PG.10) is
correctly the ONLY agent-gate (per QA_GATE_REQUIREMENTS FINAL_ONLY). It fields exactly 6
review agents, each with a genuinely distinct embedded lens:
- PG.2 rf-qa: SKILL.md-edit-conformance + contract-additivity
- PG.3 rf-qa: blocker-ordering + counter-hygiene
- PG.4 rf-qa: evidence-citation-accuracy
- PG.5 rf-qa-qualitative: fail-loud-doctrine-correctness
- PG.6 rf-qa-qualitative: eval-falsifiability
- PG.7 rf-qa-qualitative: no-scope-expansion-past-TDD

No lens is a duplicate; the 3+3 structural/content split is correct. >=6 satisfied. Not <6, so
no CRITICAL rejection.

**A2 — Serialized fix authorization (I20): PASS.** All six review agents are spawned
`fix_authorization: false` ("REPORT ONLY"). PG.8 consolidates. PG.9 spawns EXACTLY ONE
`rf-qa` `fix_authorization: true` with the explicit guard "and NO other fix agent
concurrently (serialized per I20)". PG.10 runs a 2-agent verification round (both
`fix_authorization: false`) and applies the Retry Monotonicity Protocol (regression ->
monotonicity -> hard-cap -> proceed, max 3 cycles, byte-exact HALT strings). No two
simultaneous fixers anywhere. Correct.

**A3 — Adversarial framing: PASS.** Every embedded gate prompt (PG.2-PG.7) opens with
"Assume this change has at least 5 errors ..." and closes with "A 0-issue verdict requires
proof of exhaustive checking." N=5 framing matches the documented <500-line change surface.

**A4 — Per-phase verification completeness: PASS.** The BUILD-REQUEST per-task DoD
(BR:86-91) mandates each verify checklist carry (a) spec §3 acceptance boxes, (b) spec §6 NFR
method, (c) sync/verify-sync, (d) TDD §24.1 DoD line. Verified in every per-phase verify item:
- Step 2.2: FR-RSR.3 AC (spec:332-342) + OQ resolutions + TDD §24.1 DoD line + sync.
- Step 3.4: FR-RSR.1/.2/.3/.4/.7 AC + NFR-RSR.1/.2/.4 (spec:682-685) + TDD §24.1 + sync.
- Step 4.2: FR-RSR.5 AC (spec:392-403) + TDD §24.1 DoD line + sync.
- Step 5.3: FR-RSR.6 AC (spec:430-439) + §17.7 invariant + counter-hygiene + TDD §24.1 + sync.
- Step 6.3: FR-RSR.8/.9 AC + NFR-RSR.6 + three-section count + TDD §24.1 + sync.
These are per-phase VERIFICATION items (not agent-gates), exactly as the FINAL_ONLY policy
requires. Correct.

---

## Lens B — Fail-loud doctrine + scope discipline (detailed)

**B5 — Degrade-default (the #1 risk): PASS.** This is the load-bearing correctness property
(a silent no-op reproduces FR-S9-04). The tasklist encodes it in depth and in multiple
mutually-reinforcing places:
- Step 2.1 authors the degrade-oracle table with categories (a)-(d) + an explicit
  default-DEGRADE rule ("any reachability uncertainty maps to status: DEGRADE -> §10.6
  Grounding Gap, NEVER a blocking Regression"), with `[project.scripts]` called out as the
  concrete in-repo DEGRADE case.
- Step 3.2 forbids emitting ANY UNREACHED before the oracle + rootwalk consult.
- Partial-rootwalk -> DEGRADE (Step 2.1 part 4, matches spec:355-370).
- Backend/tool loss -> DEGRADE + degraded_components, NEVER STOP (Step 6.2).
This matches spec FR-RSR.3 AC verbatim (spec:332-342) and the asymmetric-cost default. The
PG.5 content lens independently re-hunts for a silent no-op. No silent-PASS or
silent-Regression path found. PASS.

**B6 — Symbol-anchored tagger: PASS.** Step 3.1 keys the tagger off the diff hunk's resolved
symbol KIND (from existing get_symbols_overview/find_symbol steps) + the allowlist, with
`requirement_id` OPTIONAL and null-when-unmapped, and "the sweep still runs" regardless.
Kind-resolution failure routes to DEGRADE (never silent-skip). The ledger schema (Step 2.1)
types `requirement_id: str | None`. This is the exact anti-pattern guard the spec demands
(symbol-anchored, never requirement-anchored, so it does not depend on a Wave-1B mapping built
later in wave order). PASS.

**B7 — Counter hygiene: PASS.** Steps 5.1 and 5.3 state the UNREACHED-contradiction increments
ONLY `deviation_count_by_class.regression` and NEVER `verification_regressions_detected`
(exit-code-sourced). The PG.3 structural lens re-verifies this and that NO new counter exists.
Matches spec FR-RSR.6 (spec:415-416, 432-433) and TDD D8. The live SKILL.md §17.7 item 6
(SKILL:1799) confirms the no-new-counter invariant is real. PASS.

**B8 — No scope expansion: PASS (AX-5 inverse-checked).** I cross-checked every artifact the
task introduces against the TDD §18.2 inventory and the live codebase:
- 6 SKILL.md edits, 1 new ref (runtime-surface.md), 2 ref edits (reviewer-spec.md,
  deviation-taxonomy.md), 5 eval cases + evals.json registration. Nothing else.
- NO 5th deviation class (§17.7 item 6 live at SKILL:1799 rejects it; §10.9 is a
  finding-MODIFIER mapping onto the existing 4, mirroring the live §10.8 Reuse-Miss pattern at
  SKILL:1014-1025 — confirmed a real precedent, not invented).
- NO new counter, NO new CLI flag, NO whole-program call-graph/reachability-proof.
- grader.py change is conditional and minimal (Step 7.1 PREFERS the no-grader precomputed-
  scalar `count_invariant_holds` approach; only extends grader if infeasible).
The PG.7 lens enforces TDD §18.2-only + NG1/NG2/NG4/NG5 non-goals. No invented module,
interface, or capability surfaced. PASS.

**B9 — Active headline eval, real fixtures, FAIL-pre/PASS-post: PASS.** Step 7.2 authors
`cases/uc2-unwired-surface-passes/` as the ACTIVE headline with a REAL git diff exposing a
test/comment-only-referenced surface symbol (re-enacting FR-S9-04), and Steps 7.8/7.9 run the
dual-snapshot mechanism (`old_skill/` -> EXPECT FAIL, `with_skill/` -> EXPECT PASS) with an
explicit guard "if the headline cannot be made to fail-pre/pass-post the fix is incomplete"
and "NEVER widen an assertion just to force a pass." Skeletons ids 19/20
(T2-converges-on-wrong, T2-judge-class-collision) are required to "stay green and unmodified"
(verified present in the live evals.json at those ids). Matches spec FR-RSR.10 (spec:517-539).
The vacuous-pass trap is explicitly closed. PG.6 re-hunts for it. PASS.

**B10 — §5.3 pre-filter on successful sweep: PASS.** Step 4.1/4.2 gate the `surface_unreached`
table-wide forbid-STOP pre-filter on `runtime_surface_unreached >= 1` from a SUCCESSFUL sweep;
a degraded sweep does NOT force-T2; a degrade-only run (`==0 AND degraded==true`) does NOT
escalate via this pre-filter but its Grounding Gap independently forces `status: partial`. This
matches spec FR-RSR.5 AC verbatim (spec:394-403) and correctly threads the
sweep-succeeded-vs-degraded distinction that prevents a degraded sweep from false-forcing T2.
The design mirrors the live D13 pre-filter precedence paragraph (SKILL:402) it is told to
amend. PASS.

---

## Advisory NOTES (sub-threshold; not findings, not gating)

- **NOTE-1 (cosmetic-site nuance, MINOR-adjacent, does NOT gate).** The task instructs
  refreshing "cosmetic site :1558" to read 1.6.0. The live SKILL:1558 is
  `"skill_version": "<contract_version from §9.1>"` — a TEMPLATE REFERENCE to §9.1, not a
  literal `1.5.0`. It therefore needs NO edit (it already resolves to whatever §9.1 holds). The
  task's framing ("refresh the two cosmetic sites so they read 1.6.0") is slightly imprecise
  for :1558, but the live literal stale value to fix is ONLY at :1641
  (`"skill_version": "1.5.0"`). This is self-correcting at execution (re-Reading :1558 shows
  nothing to change) and the PG.4 evidence-citation lens will catch it. Not a defect in the
  plan's outcome.
- **NOTE-2 (spec-vs-codebase eval path, already reconciled, informational).** spec §4.1 /
  TDD §18.2 reference `evals/uc2-*/`, but the live repo convention is `cases/<name>/` with
  `evals/` holding only `evals.json`. The task explicitly carries this as a verified
  codebase-over-doc reconciliation (Key Constraints (a); Phase 7 NOTE) and instructs
  `case_dir: "cases/uc2-*/"`. Confirmed correct against the live `cases/` listing. No action.
- **NOTE-3 (count-invariant grader mechanism, sound).** The `len(unreached_surfaces) ==
  runtime_surface_unreached` invariant is not expressible by baseline `yaml_field`/
  `yaml_field_min` (cannot read list length). Step 7.1 resolves this by PREFERRING a
  precomputed top-level scalar `count_invariant_holds: true` asserted via `yaml_field` —
  honoring the `parse_yaml_simple` flat-key constraint — and only extending grader.py if
  infeasible. This is the minimal, scope-respecting choice. Sound.

---

## Verification performed (tool-grounded)

Every doctrine/citation claim the tasklist relies on was checked against live source, not
against the tasklist's own prose:

- **Live SKILL.md is 1854 lines** (matches task's "~1854") — `wc -l`.
- **contract_version "1.5.0" at :663/:804/:1772** — confirmed all three lockstep gate sites
  exist verbatim (grep). The kill-list test at :1772 reads
  `contract_version == "1.5.0"`. Task's claim accurate.
- **Cosmetic sites :1558/:1641** — :1558 is a §9.1 template reference (no literal); :1641 is
  the literal `"skill_version": "1.5.0"`. (Drives NOTE-1.)
- **§17.7 kill-list item 6 at :1799** — "5th `unknown` deviation category ... Rejected"
  confirmed verbatim. The no-5th-class invariant is LIVE, so B8 has a real backstop.
- **§10.8 Reuse-Miss finding-modifier at :1014-1025** — confirmed a real, in-skill precedent
  for the §10.9 "maps onto 4 by evidence, NOT a 5th class" pattern (B8 / AX-5 inverse).
- **§6.1 Wave-1A chain header :453, step 4 find_referencing_symbols :463** — confirmed; the
  4b'/4b insertion gap is real.
- **§5.3 rows 1/2 :390/:391, D13 pre-filter precedence paragraph :402, §5.4 :404,
  coverage_degraded reason :411** — confirmed; B10's amend-target exists with the exact
  table-wide-pre-filter wording to mirror.
- **reviewer-spec.md "exactly three sections" :23, headings :25/:31/:49, FR-4 :43,
  FR-RV3-MED.1 :45, D13 :47** — confirmed; FR-RSR.9 insertion between :47 and :49 inside
  `## Grounding hunks` is correct and the verbatim three-section reassertion wording exists.
- **deviation-taxonomy.md "4 categories" :5 and :117, Grounding-gaps section :115** —
  confirmed; the xref-placement target is real.
- **evals.json: exactly 36 entries, max id 36** — so ids 37–41 are contiguous (Python json
  load). **ids 19/20 = T2-converges-on-wrong / T2-judge-class-collision** confirmed present
  (the skeletons that must stay unmodified). Entry-key shape matches the task's claimed
  template (`id/name/case_dir/mode/use_case/spec_ref/description/inputs/expected/assertions`).
- **cases/ listing** — `cases/` holds 21 case dirs + `falsifier-suite`; `evals/` holds the
  registry. Confirms codebase-over-doc reconciliation (a) / NOTE-2.
- **spec FR-RSR.3/.4/.5/.6 acceptance** — read spec:321-450; every doctrine claim
  (degrade-default, partial-rootwalk=DEGRADE, pre-filter trigger, counter hygiene, no-5th-class)
  matches the task's encoding verbatim.
- **BUILD-REQUEST per-task DoD (BR:86-91)** — the (a)(b)(c)(d) requirement that A4 verifies is
  the literal source authority for the per-phase verify items.

---

## Self-Audit (MANDATORY)

1. **How many factual claims independently verified against source?** ~18 distinct
   claims (3 contract sites + 2 cosmetic + §17.7 + §10.8 + §6.1×2 + §5.3×4 + reviewer-spec×6 +
   taxonomy×3 + evals.json count/ids/shape + cases listing + 4 spec FR acceptance blocks +
   BUILD-REQUEST DoD). None were taken from the tasklist's own prose; each was re-read at source.

2. **What specific files did I read/grep?**
   - Task file (all 455 lines across 3 reads).
   - `spec.md` (FR-RSR.3-.7 acceptance, eval requirements).
   - `BUILD-REQUEST.md` (QA config + per-task DoD).
   - `SKILL.md` (live, via grep at the contract/kill-list/§10.8/§6.1/§5.3 anchors).
   - `refs/reviewer-spec.md`, `refs/deviation-taxonomy.md` (anchor grep).
   - `evals/evals.json` (Python load: count, max id, ids 19/20, key shape).
   - `cases/` directory listing; eval-workspace listing.

3. **If 0 issues — why trust I checked?** I did not return a bare 0. I returned PASS WITH three
   advisory NOTES and an 18-claim verification trail with exact line numbers, plus an
   inverse-AX5 scope sweep. The adversarial probes that could have produced a FAIL (vacuous
   headline eval, silent-PASS degrade path, requirement-anchored tagger, wrong contract sites,
   counter contamination, scope expansion, degraded-sweep false-forcing T2) were each tested
   against source and each held. NOTE-1 is the one imprecision found (cosmetic :1558 framing) —
   it is self-correcting at execution and does not change the plan's outcome, so it does not
   gate. A reviewer who found literally nothing to remark on would be suspect; I found and
   recorded the one rough edge.

4. **Web research?** None performed — this review is entirely local-file-bound (spec, TDD,
   SKILL.md, refs, eval workspace). No Tavily/WebFetch needed; nothing to record in a
   Tool-engagement fallback summary.

**Inherited Structural Verdict — Reliance Audit (PR-04, INV-019):** Not applicable — no
`## Inherited Structural Verdict` section was present in the spawn prompt (this is a
pre-execution task-plan review, not a post-assembly document review fed by an rf-qa structural
pass). I performed independent structural+semantic verification with my own tool engagement
throughout (see Verification performed). No reliance on a machine-verified upstream verdict.

---

## Confidence Gate

- **Confidence:** Verified: 10/10 lens items | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 6 | Grep: 4 (within Bash) | Glob: 0 | Bash: 4
- All 10 lens checks (A1-A4, B5-B10) marked VERIFIED with cited tool output. Tool-call count
  (Read 6 + Bash/grep 4 = 10+) >= lens item count (10), so engagement floor satisfied.
- No UNCHECKED items. No UNVERIFIABLE items.

---

## Summary
- Lens checks passed: 10 / 10
- Lens checks failed: 0
- Critical issues: 0 | Important: 0 | Minor: 0
- Advisory NOTES (non-gating): 3
- Issues fixed in-place: 0 (fix_authorization: false — REPORT ONLY)

## Issues Found
None at any severity. (Three sub-threshold advisory NOTES recorded above; none gate.)

## Recommendations
- Proceed. The tasklist is sufficient on both lens halves: the FINAL M3 QA gate is correctly
  structured (>=6 distinct lens agents, serialized I20 fix, adversarial framing, complete
  per-phase DoD), and the FR-RSR fail-loud doctrine + no-scope-expansion correctness is
  faithfully and redundantly encoded (degrade-default, symbol-anchored tagger, counter hygiene,
  active falsifiable headline eval, successful-sweep pre-filter gating).
- Optional polish (does NOT gate): tighten Step 3.3's cosmetic-site instruction to note that
  live :1558 is a §9.1 template reference needing no literal edit, and only :1641 carries a
  stale `1.5.0` literal (NOTE-1). The PG.4 evidence-citation lens already backstops this.

## VERDICT: PASS

## QA Complete
