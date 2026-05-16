# Web Research: Monotonicity Guards + Dedup-Key Strategies in Retry/Fix-Loop Control

**Status:** Complete
**Date:** 2026-05-14
**Topic:** External prior art for `|F_{n+1}| >= |F_n|` HALT-on-non-shrink and PASS@N → FAIL@N+1 regression detection in adversarial QA fix-cycles
**Codebase context:** FR-CONV.5 of task-builder convergence v3.9; composes with FR-CONV.6 (synthetic-dnsp) via INV-012 dedup-key `(assigned_files_range, escalation_ladder_exhaust_point)`.

---

## 1. Sources surveyed

| # | URL | Date accessed | Domain | Relevance |
|---|---|---|---|---|
| S1 | https://arxiv.org/abs/1309.7766 — "Termination criteria for inexact fixed point methods" | 2026-05-14 | Numerical methods | MEDIUM — formalizes termination criteria for outer-loop iteration with inexact inner solves; analogous to fix-cycle with synthetic-dnsp inner findings |
| S2 | https://fncbook.com/fixed-point/ — "Fixed-point iteration — Fundamentals of Numerical Computation" | 2026-05-14 | Numerical methods | MEDIUM — Lipschitz/contraction conditions for convergence |
| S3 | https://reference.wolfram.com/language/ref/FixedPoint.html.en — Wolfram FixedPoint documentation | 2026-05-14 | Practical engineering | LOW — establishes industry convention of max-iteration safeguard alongside convergence test |
| S4 | https://en.wikiversity.org/wiki/Gradient_descent — Gradient descent termination | 2026-05-14 | Optimization | MEDIUM — termination conditions: small step length, small improvement in objective, vanishing gradient — the "small improvement" criterion is structurally identical to `\|F_{n+1}\| >= \|F_n\|` |
| S5 | https://metricgate.com/docs/fixed-point-iteration-convergence/ | 2026-05-14 | Numerical methods | LOW — EM/MM-style monotone-ascent/descent algorithms |
| S6 | https://www.microsoft.com/en-us/research/publication/on-the-fly-progress-detection-in-iterative-stream-queries/ — "Flying Fixed-Point" | 2026-05-14 | Stream-processing | MEDIUM — directly addresses "progress detection in iterative queries" — most analogous of the engineering literature |
| S7 | https://docs.kernel.org/RCU/stallwarn.html — Linux RCU CPU stall detector | 2026-05-14 | Systems | LOW — stall = "no progress for too long"; useful framing only |
| S8 | https://www.sciencedirect.com/science/article/pii/S2215098618315908 — Oscillation detection in process control loops | 2026-05-14 | Control theory | LOW — oscillation in continuous control; not directly applicable to discrete fix-cycle |
| S9 | https://costops.dev/guides/reduce-ci-flakiness — "Flaky Tests Cost Real Money" | 2026-05-14 | CI/CD | HIGH — fail-then-pass / pass-then-fail patterns; the inverse problem this TDD must distinguish |
| S10 | https://deviera.dev/blog/how-to-detect-flaky-tests-automatically — CI pattern analysis | 2026-05-14 | CI/CD | HIGH — CI history pattern analysis with alternating pass/fail signal |
| S11 | https://gaffer.sh/solutions/flaky-test-detection/ — "flip rate" | 2026-05-14 | CI/CD | HIGH — names the exact metric: frequency of pass/fail transitions across consecutive runs |
| S12 | https://arxiv.org/abs/2302.10594 — "Discerning Flaky from Fault-triggering Test Failures: Chromium CI" | 2026-05-14 | CI/CD research | HIGH — academic treatment of distinguishing flake from regression — same problem class as INV-012 dedup vs regression precedence |
| S13 | https://sentry.zendesk.com/hc/en-us/articles/26184711712155 — Sentry event fingerprinting | 2026-05-14 | Error tracking | HIGH — fingerprint = (stack trace, exception, message) tuple; directly comparable to INV-012 dedup-key `(assigned_files_range, escalation_ladder_exhaust_point)` |
| S14 | https://docs.bugsnag.com/product/error-grouping/ — BugSnag error grouping | 2026-05-14 | Error tracking | HIGH — custom-grouping-hash mechanism for stable failure identity |
| S15 | https://docs.rollbar.com/docs/grouping-algorithm — Rollbar default grouping algorithm | 2026-05-14 | Error tracking | HIGH — fingerprint computed as SHA1 of (normalized stack frames, exception class), explicitly excludes line numbers because "they can change due to unrelated edits" — same stability concern that motivates INV-012's choice of `escalation_ladder_exhaust_point` over more volatile keys |
| S16 | https://docs.rollbar.com/docs/error-grouping-best-practices | 2026-05-14 | Error tracking | HIGH — explicitly discusses over-grouping vs under-grouping tradeoffs |
| S17 | https://www.bugsink.com/sentry-fingerprint/ — Custom Sentry fingerprinting | 2026-05-14 | Error tracking | MEDIUM — when many different stack traces share one root cause, custom fingerprint normalizes them |
| S18 | https://www.kroening.com/papers/sas2012.pdf — "Satisfiability Solvers are Static Analysers" | 2026-05-14 | Formal methods | HIGH — explicit connection: SAT = "greatest fixed point computation over a lattice"; CDCL-style clause learning is a fixed-point method |
| S19 | https://en.wikipedia.org/wiki/Conflict-driven_clause_learning — CDCL | 2026-05-14 | Formal methods | MEDIUM — learned clauses preserved across restarts; analogous to dedup-key persistence across fix-cycles |
| S20 | https://link.springer.com/article/10.1007/s10817-018-9455-7 — Verified SAT solver framework | 2026-05-14 | Formal methods | MEDIUM — formal termination proofs for CDCL with learn/forget/restart |
| S21 | https://arxiv.org/abs/2303.17651 — "Self-Refine: Iterative Refinement with Self-Feedback" (Madaan et al., 2023) | 2026-05-14 | LLM agents | HIGH — single LLM generates/critiques/refines until stopping condition; directly analogous to QA fix-cycle |
| S22 | https://openreview.net/pdf?id=vAElhFcKW6 — Reflexion (Shinn et al.) | 2026-05-14 | LLM agents | HIGH — verbal RL with trial limits, reflection memory, "lack of improvement" stop |
| S23 | https://aiwiki.ai/wiki/reflexion — Reflexion wiki | 2026-05-14 | LLM agents | MEDIUM — notes Reflexion limitations: local minima, "lack of improvement across trials" — names the failure mode that motivates `\|F_{n+1}\| >= \|F_n\|` HALT |
| S24 | https://sureprompts.com/blog/self-refine-prompting-guide | 2026-05-14 | LLM agents | HIGH — explicit treatment of termination conditions: fixed iterations, PASS verdicts, no-improvement detectors, external validators |
| S25 | https://arxiv.org/abs/2401.02009 — "Self-Contrast: Better Reflection Through Inconsistent Solving Perspectives" | 2026-05-14 | LLM agents | MEDIUM — intrinsic reflection without external feedback is unstable (i.e., can oscillate) |
| S26 | https://openreview.net/forum?id=xrLhmzw5p2 — "Spectral Guarantees for Policy Drift in Self-Refining LLM Agents" | 2026-05-14 | LLM agents | MEDIUM — convergence analysis, spectral radius, stability guarantees |
| S27 | https://homes.cs.washington.edu/~mernst/teaching/6.893/readings/zeller-tse.pdf — Zeller & Hildebrandt, "Simplifying and Isolating Failure-Inducing Input" (IEEE TSE 2002) | 2026-05-14 | Debugging | HIGH — defines `ddmin`, the 1-minimal termination condition for delta debugging |
| S28 | https://en.wikipedia.org/wiki/Delta_debugging | 2026-05-14 | Debugging | MEDIUM — connects ddmin to regression isolation and `git bisect` |
| S29 | https://www.sciencedirect.com/science/article/pii/S0167642315004165 — "Efficiently intertwining widening and narrowing" | 2026-05-14 | Static analysis | HIGH — worklist iteration variants guaranteed to terminate via widening/narrowing on monotonic systems |
| S30 | https://www.sciencedirect.com/science/article/pii/S1477842410000254 — "Widening and narrowing operators for abstract interpretation" | 2026-05-14 | Static analysis | HIGH — widening as the canonical mechanism for forcing convergence of fixpoint computations |
| S31 | https://arxiv.org/abs/0902.3722 — "A minimalistic look at widening operators" | 2026-05-14 | Static analysis | MEDIUM — formalizes widening for termination of widening sequences |

---

## 2. Key external findings

| Source | Key info | Relevance | Rating |
|---|---|---|---|
| S13 Sentry | Default fingerprint = (stack trace > exception > message) priority cascade; supports SDK fingerprinting + rules | Direct analog: INV-012 dedup-key is a (assigned_files_range, escalation_ladder_exhaust_point) tuple with priority semantics | HIGH |
| S15 Rollbar | Fingerprint = SHA1 of (normalized frames, exception class); excludes line numbers because they change for unrelated reasons | Validates INV-012's choice to use coarse-grained `assigned_files_range` rather than line-level identity — stability over precision | HIGH |
| S16 Rollbar best-practices | Over-grouping is riskier than under-grouping because distinct bugs hide in one group | Counter-argument for `(files_range, exhaust_point)` granularity — TDD should justify chosen granularity against over-grouping risk | HIGH |
| S11 Gaffer "flip rate" | Frequency of pass/fail transitions across consecutive runs is the canonical flake metric | INV-012 dedup rule prevents flips from registering as regression when dedup-key identical | HIGH |
| S12 Chromium CI study | Distinguishing flake from real regression is a quantitatively hard problem; the canonical approach is repeated execution with identity | INV-012 sidesteps this by *defining* identity via dedup-key composition rather than statistical inference | HIGH |
| S21 Self-Refine (Madaan 2023) | Single LLM iterates generate/critique/refine until stop condition met | The QA fix-cycle is a Self-Refine instance; v3.9 adds the missing principled stop condition | HIGH |
| S22 Reflexion | Verbal RL with trial limits; "lack of improvement" is acknowledged stop condition | "Lack of improvement" = `|F_{n+1}| >= |F_n|` directly | HIGH |
| S24 sureprompts.com termination | Enumerates 4 stop conditions: (1) fixed iterations, (2) PASS verdict, (3) no-improvement detector, (4) external validator | v3.9 implements (3) via monotonicity guard; existing cap implements (1); convergence-clean = (2); regression detection = bridge between (3) and (4) | HIGH |
| S25 Self-Contrast | Intrinsic reflection without external feedback is unstable | Empirically validates v3.8 F2 oscillation (21 retry files across 18 batches) as the predicted failure mode | MEDIUM |
| S29/S30 Widening | Worklist algorithms terminate on monotonic systems by widening; without widening, infinite ascending chains can occur | Structural parallel: fix-cycle without monotonicity guard is the unwidened worklist; `|F_{n+1}| >= |F_n|` HALT is the widening operator (forces termination at potential cost of precision) | HIGH |
| S18 SAT/static analysis | SAT solving is greatest-fixed-point computation; CDCL clause learning preserves clauses across restarts | Dedup-key persistence across cycles is structurally identical to learned-clause persistence across CDCL restarts | HIGH |
| S27 Zeller ddmin | 1-minimal = no single element can be removed without losing the failure; algorithm halts at 1-minimal | The "must strictly shrink" requirement is dual to ddmin's "must strictly progress toward minimality" | HIGH |

---

## 3. Prior-art for monotonicity guards (`|F_{n+1}| >= |F_n|` HALT)

The exact pattern — "halt when the failure-set cardinality fails to strictly decrease" — has strong precedent across four domains:

**3.1 Optimization (gradient descent and related).** Standard termination criteria for descent methods include "small improvement in objective value" (S4). The strict-decrease requirement on `|F_n|` is the discrete analog: in a discrete setting where the objective is integer cardinality, "small improvement" collapses to "any improvement," and `|F_{n+1}| >= |F_n|` is the negation. This is the canonical monotone-descent stopping criterion.

**3.2 Abstract interpretation (widening operators).** Widening operators are introduced precisely because Kleene iteration on monotonic systems may not terminate in finite steps over infinite-height lattices (S29, S30, S31). The widening operator forces termination by ensuring eventual stabilization. The v3.9 monotonicity guard is structurally a widening operator: it forces termination when the underlying fix-cycle would otherwise iterate without progress. The terminology fit is strong enough that the TDD could legitimately cite widening as the formal foundation.

**3.3 Fixed-point iteration termination.** Inexact fixed-point methods (S1) and standard fixed-point iteration (S2, S3, S5) all combine a convergence test with a max-iteration safeguard. v3.9 inherits the max-iteration safeguard from existing retry-cap logic; the monotonicity guard adds the convergence test. This matches industry-standard practice (Wolfram FixedPoint, SciPy fixed_point).

**3.4 LLM agent self-refinement.** Self-Refine (S21), Reflexion (S22), and the broader pattern (S24) explicitly list "no-improvement detector" as one of four canonical termination conditions for iterative LLM refinement. The known failure mode of self-refinement without such a detector is local-minimum oscillation (S23, S25) — this is exactly the v3.8 F2 empirical observation (21 retry files across 18 batches). The v3.9 design imports a pattern that is *already named and recommended* in the LLM agents literature.

**Verdict for TDD §6.4:** the monotonicity guard is not a novel invention; it is the convergence of four mature traditions (descent methods, widening, fixed-point iteration, agent self-refinement) onto the same control structure. Citing any one of these in the Key Design Decision is defensible; citing widening (S29/S30) gives the strongest formal grounding.

---

## 4. Prior-art for regression detection (PASS@N → FAIL@N+1 HALT)

The pattern "a previously-passing test failing again indicates a regression and must halt" has direct industry analogs but a critical adversarial wrinkle.

**4.1 CI/CD pass-to-fail transition.** Pass-to-fail transition (S9, S10) is the canonical signal for real regression. The complication, well-documented in industry (S11 Gaffer, S12 Chromium study), is that *flaky tests also produce pass-to-fail transitions*. The industry distinguishes them statistically: "flip rate" (alternation frequency), repeated execution with identity-preservation, and history-based classifiers (S12).

**4.2 Why v3.9's design differs.** v3.9 cannot use statistical disambiguation — the QA fix-cycle is a single linear trajectory, not a histogram across runs. Instead, INV-012 introduces a *semantic* disambiguation: dedup-key composition. If `(assigned_files_range, escalation_ladder_exhaust_point)` is identical across cycles, the failure is "stuck on the same defect class" (dedup, NOT regression). If a previously-PASSing item with a *different* dedup-key now FAILs, it is a true regression. This sidesteps the flake/regression statistical problem by defining identity instead of inferring it.

**4.3 Regression > monotonicity precedence.** v3.9 specifies regression detection runs BEFORE the monotonicity check. This precedence ordering matches the ddmin (S27) treatment of failure-preservation: any algorithm that reduces a test case must first verify the failure is still present (otherwise it has accidentally fixed the bug). In v3.9 terms, the regression check is the failure-preservation invariant; if violated, the fix-cycle has worsened the system in a directionally meaningful way that takes precedence over the cardinality stall.

**Verdict for TDD §6.4:** the PASS@N → FAIL@N+1 halt with regression > monotonicity precedence is well-grounded in CI/CD regression-detection literature (S9, S10, S11) and ddmin failure-preservation semantics (S27). The "dedup-key disambiguates regression from oscillation" design choice has no direct named precedent the search uncovered — this appears to be a v3.9 *composition contribution* on top of established primitives. The TDD should claim this composition explicitly.

---

## 5. Prior-art for dedup-key composition

The error-tracking industry has the most directly transferable patterns.

**5.1 Sentry fingerprinting (S13).** Default fingerprint priority: stack trace > exception type > message. Supports custom fingerprint rules. INV-012's dedup-key `(assigned_files_range, escalation_ladder_exhaust_point)` is structurally identical: a tuple of stable identity attributes with explicit semantic priority.

**5.2 Rollbar default algorithm (S15).** Fingerprint = SHA1 of (normalized stack frames, exception class), *explicitly excluding line numbers* because "they can change due to unrelated edits." This validates v3.9's design choice to use `assigned_files_range` (a coarse range) rather than a finer-grained location identity that would invalidate dedup on incidental file edits.

**5.3 BugSnag custom-grouping hash (S14).** Allows arbitrary user-supplied grouping hash. v3.9's `(assigned_files_range, escalation_ladder_exhaust_point)` is a domain-specific custom grouping hash; the *composition* (tuple of two semantically-distinct attributes) matches BugSnag best practice.

**5.4 Over-grouping vs under-grouping (S16 Rollbar best practices).** Rollbar warns over-grouping is more dangerous: distinct bugs hide inside one group. The TDD must justify why `(assigned_files_range, escalation_ladder_exhaust_point)` is *narrow enough* — i.e., why two genuinely-distinct defects could not share both fields. The escalation ladder exhaust point gives a reasonable orthogonal axis to the file range, but the TDD should explicitly defend this granularity.

**5.5 CDCL learned-clause persistence (S18, S19).** Conflict-driven clause learning preserves learned clauses across restarts. Persistence of failure identity across fix-cycles (so that "this defect was already seen at cycle N" can be tested at cycle N+1) is structurally identical: the dedup-key is a learned-fact carrier across iteration boundaries.

**Verdict for TDD §6.4:** the dedup-key composition is a domain-specific application of the Sentry/Rollbar/BugSnag fingerprinting pattern. Cite S13 (Sentry priority cascade) for the tuple structure and S15 (Rollbar line-number exclusion rationale) for the stability-over-precision tradeoff. Explicitly defend the chosen granularity against the over-grouping warning (S16).

---

## 6. Recommendations for TDD §6.4 Key Design Decisions

**Decision: Monotonicity-with-regression-precedence as the fix-cycle stop semantics.**

Recommended TDD §6.4 entry structure:

> **§6.4.X Monotonicity guard with regression precedence (FR-CONV.5)**
>
> **Decision:** Halt the QA fix-cycle when `|F_{n+1}| >= |F_n|` (monotonicity guard). Detect and halt earlier on PASS@N → FAIL@N+1 with a dedup-key-distinct failure (regression detection). Regression detection runs before monotonicity check.
>
> **Rationale (intent-port from sc-tasklist Stages 9-10):** Imports the proven control pattern from `sc-tasklist-protocol/SKILL.md` lines 1083+, where the same composition was empirically validated for roadmap-validation convergence.
>
> **Prior-art validation:**
> 1. The monotonicity guard is the discrete-cardinality form of standard monotone-descent stopping criteria in optimization (S4 gradient descent termination) and the abstract-interpretation widening operator (S29, S30, S31) that forces fixpoint convergence on otherwise non-terminating iterations.
> 2. Self-Refine / Reflexion literature (S21, S22, S24) lists "no-improvement detector" as a canonical termination condition for iterative LLM refinement, and identifies local-minimum oscillation (S23, S25) as the failure mode for self-refining agents without such a detector — exactly the failure observed in FINAL-REPORT §6.2 F2 (21 retry files across 18 batches in v3.8).
> 3. Regression detection follows CI/CD pass-to-fail transition semantics (S9, S10, S11) with a semantic disambiguation (dedup-key) rather than the statistical flake/regression distinction (S12) — the latter is unavailable in a single linear fix-cycle trajectory.
> 4. Regression-before-monotonicity precedence mirrors ddmin failure-preservation semantics (S27): any algorithm reducing a defect set must first preserve the failure-direction invariant.
>
> **Why not pure monotonicity (no regression precedence)?** Without regression detection, a fix-cycle could trade an old defect for a new one of equal cardinality and pass the monotonicity guard while silently worsening the system. Regression precedence catches direction-of-progress violations that cardinality alone cannot.
>
> **Why not pure regression detection (no monotonicity)?** Without monotonicity, a fix-cycle stuck on the same dedup-key cluster would iterate without progress until exhausting the max-retry cap — wasting tokens on a known-stuck configuration that v3.8 F2 empirically demonstrated.

**Decision: INV-012 dedup-key as `(assigned_files_range, escalation_ladder_exhaust_point)`.**

Recommended TDD §6.4 entry:

> **§6.4.Y INV-012 dedup-key composition**
>
> **Decision:** Dedup-key is the tuple `(assigned_files_range, escalation_ladder_exhaust_point)`. Identical dedup-key across consecutive cycles is dedup, NOT regression.
>
> **Rationale (Sentry/Rollbar fingerprinting precedent):**
> 1. Tuple-of-stable-attributes structure matches Sentry's default fingerprint priority cascade (S13) and BugSnag's custom-grouping-hash pattern (S14).
> 2. Choice of `assigned_files_range` over finer-grained location identity (e.g., line numbers) follows Rollbar's explicit exclusion of line numbers from default fingerprints because "they can change due to unrelated edits" (S15) — stability-over-precision tradeoff.
> 3. `escalation_ladder_exhaust_point` as the second axis provides orthogonality to the file range, addressing the over-grouping risk Rollbar best practices warns about (S16): two defects could share a file range but differ in how far up the escalation ladder they propagate.
> 4. Persistence of dedup-key across fix-cycles is structurally analogous to CDCL learned-clause persistence across restarts (S18, S19): a carrier of identity across iteration boundaries.

---

## 7. Recommendations for TDD §21 Alternatives Considered

**Alternative 4 (REJECTED): Single-FR mega-merge for FR-CONV.5 and FR-CONV.6.**

> Merging monotonicity guard and synthetic-dnsp findings into a single FR was rejected. Rationale:
> 1. Sentry/Rollbar fingerprinting literature (S13, S15, S16) treats failure-grouping (dedup) and progress-detection (cardinality stall) as orthogonal concerns. Conflating them obscures which control invariant any given halt was triggered by.
> 2. INV-012's stated semantics ("synthetic findings count as failures for `|F_n|` cardinality, but identical dedup-key across consecutive cycles is dedup, NOT regression") *requires* the two FRs to be expressible independently to phrase the composition rule. Mega-merge erases the seam INV-012 needs.
> 3. ddmin (S27) and CDCL (S18) both keep their failure-identity machinery (dedup) separate from their progress-condition (cardinality / clause-set-strictly-grows) — the composition is in the algorithm, not in the data structure.

**Alternative 5 (REJECTED, if applicable): X-003 "halt on slow convergence" threshold.**

> A variant proposal would halt the fix-cycle when `|F_{n+1}| < |F_n|` but the decrease is "small" (e.g., shrinks by < K items). Rejected. Rationale:
> 1. The abstract-interpretation widening literature (S29, S30) supports binary "did the chain stabilize?" rather than rate-of-stabilization thresholds. Rate thresholds introduce a tunable parameter K with no principled value, contradicting the v3.9 goal of intent-porting a proven mechanism.
> 2. CI/CD flake-detection (S11 "flip rate") provides rate-based detection only where statistical aggregation across many runs is available. A single linear fix-cycle trajectory cannot estimate "rate of convergence" without strong assumptions about per-cycle work being i.i.d., which it is not (later cycles tackle harder residual defects).
> 3. The max-retry cap already provides a soft "give up on slow convergence" backstop; X-003 would shadow that cap with a less principled tunable.

**Alternative 6 (REJECTED, if applicable): Pure cardinality halt with no regression detection.**

> See §6.4 rationale "Why not pure monotonicity": without regression precedence, an old-for-new defect swap of equal cardinality passes the cardinality test but silently worsens the system. Prior-art: ddmin failure-preservation invariant (S27) and CI/CD pass-to-fail transition semantics (S9, S10).

---

## 8. Codebase remains source of truth

No external finding contradicts the verified codebase. Specifically:
- The dedup-key `(assigned_files_range, escalation_ladder_exhaust_point)` is project-specific and is not directly named in any surveyed source; it is a domain-specific instantiation of the Sentry/Rollbar fingerprint pattern.
- The "regression > monotonicity precedence" ordering is consistent with ddmin failure-preservation semantics but is not directly stated in any surveyed source; this is a v3.9 composition contribution.
- The empirical motivation (21 retry files across 18 batches, FINAL-REPORT §6.2 F2) is codebase-internal evidence; external literature provides only the general failure-mode framing (S23 Reflexion local-minima, S25 Self-Contrast intrinsic-reflection instability), not the specific numbers.

**Flag for TDD authors:** if external sources are cited verbatim in §6.4 or §21, prefer paraphrase-with-citation over direct quotation, because the surveyed sources do not use the specific vocabulary (`|F_n|`, dedup-key, escalation ladder) of the v3.9 design. Citations are validating prior art, not authoritative definitions.

---

**Status:** Complete
