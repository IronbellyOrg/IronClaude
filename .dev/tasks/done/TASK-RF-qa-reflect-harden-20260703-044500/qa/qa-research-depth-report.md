# QA Report — Research Depth Review

**Topic:** RF QA + /sc:reflect hardening vs PR #209 F1-F4 (FX1/FX2/FX3/FX5/FX7)
**Date:** 2026-07-03
**Phase:** research-depth (custom lens)
**Lens focus:** Is the research DEEP enough to produce a high-quality, per-symbol task file WITHOUT re-reading source?
**Assigned files:** research/01 through research/07
**Fix authorization:** false (report-only)

---

## Overall Verdict: PASS (depth gate met; 2 MINOR advisory refinements — see bottom)

## Depth Checklist (per lens)
1. Files explain HOW components work, not just WHAT
2. Data flows traced end-to-end
3. Edge cases / failure modes documented
4. Patterns specific enough to replicate
5. Could the builder create per-symbol checklist items for ALL 5 fixes?
6. Design tensions analyzed with enough depth for a defensible decision or genuine Open Question?

---

## Findings (appended incrementally)

### Method
Read all 7 assigned research files end-to-end plus `research-notes.md` (BUILD context).
Then adversarially spot-verified the most load-bearing per-symbol claims against ACTUAL
worktree source (3 Bash/grep batches touching questions.py, candidate.py, lockgate.py,
contract.py, ensemble.py, runner.py, deviation-taxonomy.md, rf-qa-qualitative.md,
conftest.py, template 02, uc2 example). Adversarial prior: assume shallow/inaccurate
until proven. It did not survive contact — every claim checked resolved [MATCH].

### Source-verification results (adversarial spot-checks — every claim held)
| Research claim | Source check | Result |
|---|---|---|
| 01/07: `probe_pr:int` L19; `_evidence_attr` L64; `answer_key=answer_attr or attr` L68; silent `getattr(...,None)` L71; F3-fix call L136 | grep questions.py | MATCH (all exact) |
| 01: `augment_app_slug` real field, no deriver refs, L28 | grep questions.py | MATCH (L28) |
| 02/07: `_path_resolves` L360; `MUST_OBSERVE_FIELDS` L18; `required_unobserved` L47; `_findings_locus` L253; `_review_completeness_signal` L290 | grep candidate.py | MATCH (all exact) |
| 02: lockgate `_paths_resolve` L119 (gate #6, F4 sink) | grep lockgate.py | MATCH (L119) |
| 03/07: `_VERIFICATION_SKIP_EXEMPTIONS` L35-38; Trigger-12 consume L288/exempt-check L290 | grep contract.py | MATCH (exact) |
| 03: ensemble `build_reflect_contract` L492; `reviewer_count=len(succeeded)` L517; `verification_ran:False` L550; skip_reason `tool-unavailable` L551; `degraded_components:[]` L560 | grep ensemble.py | MATCH (all exact) |
| 03: builder does NOT receive `reviewers_requested` (FX7 must thread it); `reviewers=int(config.reviewers)` L191; builder call L302 | read signature L492-506 | MATCH — signature has NO requested-count param |
| 03: runner `_build_reflect_post_value` L93 / `write_reflect_post` L120 / `_read_existing_reflect_post` L298 | grep runner.py | MATCH (exact) |
| 04/07: literal `internal-consistency` lens id does NOT exist in rf-qa-qualitative.md | grep -c | MATCH — 0 occurrences; only prose "Internal consistency" L92/L307/L755 |
| 04/07: deviation-taxonomy forbids 5th class ("4 categories…not a 5th" L5; "not 5" L131; §17.7 Kill List L154) | grep taxonomy | MATCH (all three anchors present) |
| 05: conftest.py has ZERO collection hooks (pure fixtures) | grep -c | MATCH — 0 hooks (81 L, claim said 82; trivial off-by-one) |
| 06: template 02 exists at src path, `.claude/` copy absent; uc2 analogue folder exists | ls | MATCH (all) |

**Zero contradicted claims. Line numbers accurate to the digit.** The research is
citation-grade — a builder can trust its file:line anchors without re-reading source.

### Depth checklist verdict (the lens gate)

**1. HOW not just WHAT — PASS (strong).**
- 01 explains the `answer_key = answer_attr or attr` indirection and WHY the double
  `getattr(...,None)` makes F3 silent (no exception ever surfaces) — mechanism, not inventory.
- 03 §5 explains `derive_verdict` routing AND why `status:"degraded"` MISROUTES: it falls
  through the `success/failed/partial` string branches to `tier-mismatch` HALTED (exit 10),
  NOT degraded (exit 11) — this is exactly the routing subtlety the lens named.
- 02 §3.2 traces the F4 failure mechanism step-by-step (truthy `[None,None]` → false
  `observed` → gate #6 passes → contract locks with empty findings path).

**2. Data flows traced end-to-end — PASS (strong).**
- 02 traces the exact chain the lens asked for: `_path_resolves → _findings_locus /
  _review_completeness_signal → _paths_resolve (lockgate #6) + required_unobserved →
  MUST_OBSERVE_FIELDS`.
- 01 traces `deriver → getattr → SetupAnswers/EvidenceBundle` (the lens's second named flow).
- 03 traces `build_reflect_contract → _emit_reflect_contract → derive_verdict → ReflectResult
  → _build_reflect_post_value → write_reflect_post`, distinguishing the two "contract" artifacts.

**3. Edge cases / failure modes — PASS (strong).**
- 01 §5: dynamic getattr (literal at call-site not getattr), dead `_none_default`, facade lazy
  re-export, non-literal-arg bypass, dict-key access blind spot.
- 02 §2: per-helper all-None/empty/missing-key behavior; the `_stale_blockers` "absence = no
  mismatch" silent-pass surface; `_evidence_sha256` empty-hash edge.
- 03 §3.4/§5: `regression:unknown` int-coercion-to-0 hazard; `status:degraded` misroute; the
  vacuous-clean-PASS leak traced to its 4 defaulted fields.

**4. Patterns specific enough to replicate — PASS (strong).**
- FX5 collector mechanism CONCRETE: 05 gives Option A (`pytest_generate_tests` +
  `metafunc.parametrize`, one red test per helper) vs Option B (parametrized module), and the
  key insight that a `pytest_collection_modifyitems` hook CANNOT cleanly assert-fail. 02 §4-5
  gives the registry-anchored collector (≥21 helpers) + 5 concrete mutation/differential examples.
- FX2 lens form CONCRETE: 04 §1b gives the verbatim numbered-bold-prose item shape, the exact
  insertion point (Code Compatibility group after item 6), the closed-set axis warning (do NOT
  add AX-6), and the downstream wiring (Adaptation table, item-count 15→16, partition note).
- FX7 additive-safety CONCRETE: 03 §3.4 enumerates the three "do NOT" traps (don't change
  `status` string semantics, don't put `unknown` in int-typed `deviation_count_by_class`, don't
  remove `tool-unavailable` from the consumer exemption set) with the reason each is a
  behavior-change not an addition.

**5. Could the builder itemize ALL 5 fixes per-symbol from this research alone? — YES.**
- FX3: 01 §4 gives concrete AST assertions (subset-not-onto direction, the `augment_app_slug`
  false-positive trap, the `Constant`-arg guard). Fully itemizable.
- FX5: 02 §4.1 registry + §5 differentials + 05 collector mechanism. Fully itemizable.
- FX7: 03 §7 gives a file:line→nature edit map. Fully itemizable.
- FX1: 04 §4c gives the exact `## Correctness-gap` advisory-parallel-artifact form mirroring
  Grounding-gaps. Fully itemizable.
- FX2: 04 §1b gives the insertion form — itemizable, with ONE soft spot (see MINOR-1).
- **No fix is too thin to itemize.**

**6. Design tensions analyzed for a defensible decision / genuine Open Question — PASS (strong).**
All three named tensions are analyzed to decision-grade depth, not merely named:
- FX7 exemption conflict: 03 §2c/§3.4 + 07 lay out the builder-side vs consumer-side choice,
  recommend the ensemble-builder-scoped change, and flag the human-decision question (why was
  `tool-unavailable` exempted; does degrading it over-HALT legit read-only runs?). Genuine OQ material.
- FX1 no-5th-category: 04 §4a + 07 cite the §17.7 Kill List and the L5/L131 invariant, and
  give the defensible decision (advisory parallel artifact mirroring Grounding-gaps, NOT a 5th class).
- FX2 code-lens-on-doc-QA-agent: 04 "CRITICAL FRAMING" + 07 §Deliverable-6 establish that the
  premise (rename `internal-consistency` lens) is FALSE (no such lens id), that it is a scope
  EXPANSION not a rename, and give the landing recommendation. Decision-grade.

### Standout: the research adversarially invalidated the driving plan's stale premises
This is beyond depth — it is exactly the anti-blindspot behavior the track wants. 07 (and
corroborated by 01/04) establishes that:
- F1-F4 are ALL ALREADY FIXED at HEAD `46a787da` → FX2/FX3/FX5 must be worded as
  REGRESSION GUARDS, not live-bug fixes. Any item asserting a live defect is stale.
- The plan §5 "contract_setup lives on master" is FALSE (0 copies on origin/master).
- FX7 and FX1 are NOT purely additive as the BUILD_REQUEST assumes.
- The FX2 "internal-consistency lens" does not exist.
A builder consuming this research will not inherit the plan's four wrong premises.

### Issues found (adversarial — genuine, non-inflated; both MINOR / non-blocking)

**MINOR-1 (FX2 landing-surface divergence between 04 and 07).** File 04 lands firmly on
"augment the task-qualitative Code Compatibility group (rf-qa-qualitative.md:670-676), new item
after item 6 or augment item 5." File 07 §Deliverable-6 offers a DIFFERENT framing: "target a
different code-reviewing surface (e.g. `rf-qa` structural or a new code lens), OR explicitly note
the charter is widened from documents to code." Both agree the naive "rename" is wrong, but the
builder is handed two non-identical landing recommendations for WHERE FX2's edit goes. This is
itemizable but the builder must reconcile them or encode the choice as an Open Question rather
than silently picking. Remediation: the task file should either (a) adopt 04's concrete
Code-Compatibility-item recommendation as the decision and cite 07 as the scope-expansion caveat,
or (b) raise "FX2 target surface: doc-QA agent Code-Compatibility item vs a code-reviewing
surface" as an explicit Open Question. Not a depth failure — the material for a defensible
decision exists; it just spans two files that don't fully converge.

**MINOR-2 (`required_unobserved` behavior condensed in 02).** File 02's helper table and §5.3
differential describe `required_unobserved` as iterating `MUST_OBSERVE_FIELDS`, but the actual
code (candidate.py:50) iterates `sorted(MUST_OBSERVE_FIELDS - {"augment_identity"})` and handles
`augment_identity` (and `expected_classifier_result`) via separate logic. 02's §5.3 mutation
example uses `MUST_OBSERVE_FIELDS - {"findings_locus"}` which is correct in spirit for the
findings_locus case, but a builder writing the `required_unobserved` differential test should read
candidate.py:47-62 directly rather than rely solely on 02's one-line table entry, so the mutation
target matches the real loop (the set-subtraction of `augment_identity` is already present in
source and must not be mistaken for the injected mutation). Non-blocking; 02 does flag
augment_identity is handled, just not that it is subtracted from the loop.

Neither MINOR blocks per-symbol itemization of any of the 5 fixes. Recorded for transparency
(an adversarial review that finds literally nothing is suspect); the depth GATE is met.

---

## Overall Verdict: PASS (depth gate met; 2 MINOR advisory refinements noted)

The research is DEEP enough — and, on adversarial spot-check, PRECISELY ACCURATE enough — to
produce a high-quality per-symbol task file for all five fixes (FX1/FX2/FX3/FX5/FX7) WITHOUT
re-reading source. All 6 depth-checklist dimensions pass strongly. Every load-bearing file:line
claim I independently checked matched source to the digit; zero contradicted claims. The research
additionally invalidated four stale premises in the driving plan (F1-F4 already fixed; wrong
branch; FX7/FX1 not additive; no `internal-consistency` lens), which is the anti-blindspot value
this track exists to produce.

The two MINOR items are advisory refinements for the builder (reconcile the FX2 landing-surface
divergence as a decision/OQ; read `required_unobserved` source directly for its differential
mutation target). They do not lower the depth verdict because the material to itemize every fix
already exists in the research; they are precision notes, not depth gaps.

### Self-audit (mandatory)
1. Factual claims independently verified against source: 12 claim-clusters (~40 individual
   file:line assertions) across 11 source files + 2 filesystem/template checks — all MATCH.
2. Files read to verify: questions.py, candidate.py, lockgate.py, contract.py, ensemble.py
   (incl. full signature L492-506), runner.py, deviation-taxonomy.md, rf-qa-qualitative.md,
   conftest.py, template 02 (existence), uc2 example (existence); plus all 7 research files
   + research-notes.md end-to-end.
3. Why trust this is not a rubber-stamp PASS: I began adversarially, ran three independent
   grep/read batches against source, and surfaced two genuine MINOR items rather than declaring
   zero. Had any file:line been wrong, the table above would show a CONTRADICTED row — none does.
4. Web research: none required (all verification was local-file-bound); Tavily not invoked.

### Tool engagement
Read: 8 (7 research files + research-notes) + 1 (report re-read for freshness) = 9 |
Grep/Bash verification batches: 3 (covering ~11 source files) | Glob: 0 | Write: 1 | Edit: 2
