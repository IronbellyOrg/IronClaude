---
schema_version: "1.0"
debate_id: "DEBATE-03"
proposal_id: "PROP-03"
title: "Adversarial Debate — Code Integration Gate: Static Analysis for Orphaned Implementations and No-Op Fallbacks"
status: "complete"
date: "2026-03-17"
scoring_framework: "proposals/scoring-framework.md"
incident_reference: "cli-portify-executor-noop-forensic-report.md"
composite_score: 6.65
tier: "Tier 2 — Implement in Phase 2"
---

# Debate 03: Code Integration Gate

**Proposal under review**: `proposal-03-code-integration-gate.md` (PROP-03)
**Format**: Three-round adversarial transcript + structured scoring
**Participants**: Proponent (FOR) | Devil's Advocate (AGAINST)

---

## Preamble

The cli-portify executor shipped three consecutive releases (v2.24, v2.24.1, v2.25) performing zero
real work. Every step returned `(exit_code=0, stdout="", timed_out=False)` because `step_runner` was
never passed to `PortifyExecutor`. The same structural fingerprint — a fully implemented component
that is syntactically correct, passes all linters, but is never invoked from its intended caller —
appears in at least two other locations in the codebase. PROP-03 proposes four static analysis checks
(CPC, IRE, NOPF, REGC) implemented via Python's `ast` module to detect this class of defect before
release.

---

## Round 1 — Opening Positions

### Proponent: The Case FOR PROP-03

This proposal targets a defect class that every existing gate is structurally blind to. The forensic
report is explicit: "Every gate follows the signature `(content: str) -> bool`... They validate that
generated documents have correct structure." Not one gate in the entire pipeline asks whether code
components are wired together.

The cli-portify bug is not subtle. It is not a race condition, a floating-point error, or an edge
case under unusual load. It is a named parameter, `step_runner`, that was never passed to its
constructor across three releases. PROP-03's NOPF check would have found `executor.py:397-399` on
its first run: the pattern `if self._step_runner is not None: <real work> else: (0, "", False)` is
unambiguous. An AST traversal needs no LLM, no heuristic threshold, and no configuration to
recognize this structure. It fires deterministically whenever an `else` branch assigns a zero exit
code to a variable named `exit_code`, `rc`, or `returncode` — the pattern is a 15-line AST visitor.

The CPC check adds independent confirmation: `PortifyExecutor.__init__` declares
`step_runner: Optional[Callable[[PortifyStep], tuple[int, str, bool]]] = None`. There is exactly one
non-test call site — `run_portify()` at `executor.py:1395` — and it never passes `step_runner`. CPC
cross-references all non-test `PortifyExecutor(...)` call nodes against the parameter list. Zero
keyword matches for `step_runner`. ERROR severity emitted. Pipeline blocked.

These two checks — NOPF and CPC — are Stage 1 of the proposal, estimated at 5 developer-days, and
they address the archetypal bug directly and deterministically. The full 4-check suite extends
coverage to the two other known instances of the same pattern: `DEVIATION_ANALYSIS_GATE` (unwired
from `_build_steps()`) and `SprintGatePolicy` / `TrailingGateRunner` (never instantiated in
`execute_sprint()`). The forensic report explicitly names these. IRE catches the 8 unreachable
`steps/` modules as a third independent signal on the same incident.

The proposal is not proposing to replace LLM-based fidelity gates. It is proposing to add a narrow,
deterministic layer that catches the specific failure mode where working code is permanently bypassed.
The value proposition is straightforward: 5 developer-days versus three releases shipping no-ops.

### Devil's Advocate: The Case AGAINST PROP-03

The proposal sounds compelling because it is written backwards from a known bug. Given any bug, you
can design a check that catches it. The question is whether that check generalizes, stays green in
normal development, and justifies its maintenance cost. On all three counts, PROP-03 has significant
problems.

**Problem 1 — Static analysis on Python has very high false positive rates for this check class.**

Python's dynamic dispatch, decorators, and dependency injection frameworks make static call-site
analysis unreliable. Consider a factory: `executor = ExecutorFactory.create(config)`. The factory
internally passes `step_runner=RealRunner()`. AST analysis of the `create()` call site sees no
`PortifyExecutor(...)` call at all. CPC searches non-test call sites and finds zero — then
incorrectly concludes the parameter is never provided. The proposal acknowledges this in Risk 3
("Dynamic Construction and Factories") and mitigates it by checking `audit/dynamic_imports.py`. But
`audit/dynamic_imports.py` itself has false negatives for patterns it does not recognize. You are
stacking one imperfect heuristic on another.

The NOPF check has its own false positive class: dry-run modes. Every pipeline tool in this
codebase has dry-run functionality. A dry-run runner returns `(0, "", False)` by design — that is
the correct production behavior when `--dry-run` is passed. The proposal's heuristic for
distinguishing intentional dry-run no-ops from pathological ones (conditional call sites vs. always
omitted) is plausible but not reliable. The exact same AST pattern appears in both cases.

**Problem 2 — The 15 developer-day estimate is high for a single bug class.**

The proposal itemizes 9 days of implementation + 4 days of testing + 2 days of review. That is
nearly three engineer-weeks for a static analysis module that catches one structural pattern. The
forensic report identifies three instances of this pattern in the current codebase. Three instances
do not justify three weeks of infrastructure investment. The suppression annotation system alone
(0.5 days in the estimate) creates an ongoing maintenance obligation: every legitimate optional
callable now requires a `# integration-gate: ignore(CPC-001) reason=...` annotation or it generates
a false positive. This annotation debt grows with every new contributor who does not know the rule.

**Problem 3 — "Defined but not wired" has many legitimate uses.**

Optional plugins, feature flags, extensibility hooks, dependency injection for testability, staged
rollouts, A/B test boundaries — all of these use the exact pattern that CPC and NOPF target. The
`step_runner` pattern is not pathological because it is `Optional[Callable]`. It is pathological
because the comment says "Used for testing" and no production caller ever passes a real
implementation. AST analysis cannot read intent. It can read structure. The structural pattern is
shared by the bug and by dozens of correct implementations.

**Problem 4 — AST-based no-op detection requires constant maintenance as code patterns evolve.**

The NOPF success indicator heuristics are a fixed list: variable names `exit_code`, `rc`,
`returncode`, `code`; string literals `"SUCCESS"`, `"PASS"`, `"OK"`, `""`; tuple `(0, ...)`. If a
developer returns a `PortifyStatus.SUCCESS` enum member instead of the integer `0`, NOPF misses it.
If they rename `exit_code` to `status_code`, NOPF misses it. The proposal's check is brittle to
code style evolution. Every codebase refactor that touches these naming conventions requires a
corresponding update to the heuristic list. This is not a one-time cost; it is a maintenance tax
on normal development velocity.

---

## Round 2 — Cross-Examination

### Proponent Defends Against False Positive Risk

The Devil's Advocate raises four attack vectors. They deserve direct answers.

**On factory construction and dynamic dispatch:** The proposal already requires the suppression
annotation as the escape hatch for cases AST analysis cannot resolve. But the more important point
is that the factory pattern is not present in this codebase for the classes CPC targets. CPC is
configured with explicit class targets. The check is not a generic scanner over all Python classes —
it runs against specifically configured classes and entry points defined in `integration_gate.toml`.
If `PortifyExecutor` is constructed exclusively through a factory in the future, that change is
accompanied by a configuration update or a suppression annotation. The maintenance cost is
proportional to the rate of architectural change, not to the size of the codebase.

**On dry-run false positives:** The proposal's distinguishing heuristic for NOPF is not just the
presence of a no-op `else` branch. It requires conjunction: the `else` branch returns a success
value AND CPC confirms no non-test call site provides the guarded parameter. A dry-run runner
that genuinely passes `runner=None` at some call sites and `runner=RealRunner()` at others produces
zero CPC findings — CPC only fires when every non-test call site omits the parameter entirely or
always passes `None` unconditionally. The dry-run false positive requires both checks to misfire
simultaneously, which is structurally unlikely for a correctly designed dry-run mode.

**On annotation debt:** The suppression annotation is not free, but it is deliberate. The proposal
explicitly states that requiring the annotation is "itself a code quality improvement." A developer
who writes `# integration-gate: ignore(CPC-001) reason=dry-run-design` has documented that the
`None` path is intentional. That documentation did not exist for `step_runner`. The annotation
obligation is a forcing function for intent documentation, not a maintenance burden — unless the
team is writing many undocumented optional callables, in which case the annotation is surfacing a
real problem.

**On the 15-day estimate:** The Devil's Advocate correctly identifies that 15 days is substantial.
But Stage 1 (NOPF + CPC) is estimated at 5 days and independently catches the archetypal bug. The
question is whether 5 days of engineering is justified to prevent the pattern that cost three
releases of invisible no-ops. The forensic report notes the bug class recurs across at least three
locations already. The question is not whether the 15-day full suite is justified; it is whether the
5-day MVP is. That is a much easier case to make.

### Devil's Advocate Attacks the 5-Day MVP Claim

The Proponent's strongest retreat position is the Stage 1 MVP: NOPF + CPC in 5 days. Let me examine
whether that retreat holds.

**The 5-day estimate is optimistic on technical grounds.** NOPF requires not just pattern matching
but also severity classification: is this `else` branch in a production code path or only in a test
helper? The proposal assigns `"ERROR"` when in production path and `"WARNING"` when in test helpers.
Determining whether a function is in a production path requires either a reachability graph (which
is the IRE check — Stage 2, another 4 days) or a path heuristic based on file location. File
location heuristics are fragile: `executor.py` is in the production path but contains both
production functions and test-injection helpers. You cannot determine severity from file path alone
without the reachability graph. Either NOPF severity classification is unreliable at Stage 1, or
you need IRE sooner than planned.

**NOPF alone without CPC has a high false positive rate.** The proposal's Stage 1 bundles both NOPF
and CPC. But CPC requires the call-site traversal logic — scanning all non-test constructor calls
and checking for parameter presence. That traversal is not trivial. You need to resolve class names
across imports, handle aliased imports (`from executor import PortifyExecutor as PE`), and handle
calls in list comprehensions and conditional expressions. A robust CPC check is closer to 3 days
than the 2 days estimated. The 5-day Stage 1 requires both NOPF and CPC to be reliable, but CPC
has underestimated complexity.

**The most important challenge: NOPF + CPC alone addresses the archetypal bug but misses the two
other known instances.** The `DEVIATION_ANALYSIS_GATE` case is a registry-completeness problem
(REGC). The `SprintGatePolicy` / `TrailingGateRunner` case is a reachability problem (IRE variant).
If the MVP's value claim is "catches the three known instances of the pattern," then NOPF + CPC
delivers only one of three. The remaining two require Stage 2 (IRE) and Stage 3 (REGC). The 5-day
MVP is a partial solution to a problem the proposal frames as systematic. The full value requires
the full 15 days.

**This does not mean the MVP is worthless.** It means the proposal's framing should be honest: Stage
1 prevents recurrence of the archetypal `step_runner` bug specifically. Stages 2-4 are needed for
the full "defined but not wired" detection capability the proposal promises. The Tier 1 / Tier 2
adoption profile should reflect this staged delivery.

---

## Round 3 — Synthesis

### Where Static Analysis Genuinely Adds Value

The debate converges on a distinction that is not explicit in the proposal but is critical for its
correct adoption: **static analysis on structure is reliable; static analysis on intent is not.**

NOPF detects a structural pattern: an `if x is not None: <work> else: <zero-return>` AST shape.
This structure is objectively present or absent. The question of whether it represents a bug or
intentional dry-run behavior is a matter of intent — which AST cannot determine. The proposal's
attempt to resolve intent through CPC conjunction (both checks firing) is sound but imperfect.

The highest-confidence value zone for PROP-03 is the overlap of structural certainty and intent
evidence:

1. **NOPF fires** (structural: no-op else branch returning success)
2. **CPC fires** (evidential: zero non-test call sites provide the parameter)
3. **The parameter's docstring or name contains "test" or "mock"** (intent: designed for injection)

When all three conditions hold, the probability that this is an intentional design is near zero.
This is exactly the `step_runner` situation. The forensic report quotes the docstring: "Used for
testing; real runs use subprocess." CPC finds one call site, no parameter. NOPF finds the no-op.
Three independent signals, zero ambiguity.

The proposal should be scoped to fire ERROR severity only at this high-confidence intersection. NOPF
alone or CPC alone should produce WARNING. Only the conjunction produces ERROR and blocks the gate.
This reduces false positive rate substantially while preserving detection of the archetypal case.

Static analysis also adds unambiguous value for IRE in its specific configuration: a `steps/`
directory explicitly declared as "must be reachable" in `integration_gate.toml` is not reached from
the entry point. This is a structural fact. There is no intent ambiguity: either the entry point
imports from `steps/` transitively or it does not. The configuration makes intent explicit (the
developer declared `steps/` should be reachable) and the check is deterministic.

### Where Static Analysis Creates Maintenance Burden

The maintenance burden is concentrated in the NOPF success indicator heuristics and the REGC
registry detection heuristics. These are brittle to code style evolution. A team that adopts this
proposal needs to commit to keeping the heuristic lists current as naming conventions evolve. This
is a reasonable commitment for a focused team but a real cost.

The IRE check's dependency on explicit `integration_gate.toml` configuration is both a strength
and a weakness. It avoids false positives by requiring explicit opt-in. But it means the check only
covers what developers remember to configure. The `steps/` directory would have needed to be
configured. Whether that configuration would have existed when the bug was introduced depends on
team process discipline.

### Minimum Viable Version That Justifies the Effort

The minimum viable version is not purely Stage 1 (NOPF + CPC) as the proposal defines it. The
MVP that justifies 5 developer-days should be:

**MVP Definition**: NOPF + CPC in conjunction mode (ERROR only when both fire simultaneously for
the same guarded attribute), plus the suppression annotation parser, plus one integration test
against `cli_portify/executor.py` confirming the check fires on the actual bug.

This 5-day scope:
- Deterministically catches the archetypal `step_runner` bug
- Has low false positive rate (requires conjunction)
- Has an escape hatch (suppression annotation)
- Validates against the real incident as its acceptance test

Stages 2-4 (IRE, REGC, configuration framework) should be sequenced as Phase 2 work after the MVP
demonstrates value in CI. The full 15-day suite is justified, but only after Stage 1 proves the
check runs cleanly on the existing codebase without generating noise.

---

## Scoring

### Axis 1 — Catch Rate (weight 25%)

**Score: 9**

Evidence: Three of four checks (CPC, NOPF, IRE) would independently fire on the `step_runner` bug,
each producing ERROR severity. Any single one would have blocked the pipeline.

- NOPF: `executor.py:397-399` is a textbook match for the `if self._step_runner is not None: <work>
  else: (0, "", False)` pattern. Detection is deterministic — zero LLM dependency, zero threshold
  tuning required.
- CPC: `step_runner: Optional[Callable[...]] = None` in `__init__`, combined with `run_portify()`
  as the sole non-test call site never providing the parameter, is an unambiguous CPC finding.
- IRE: All 8 modules in `cli_portify/steps/` are unreachable from `commands.py` → this would have
  been confirmed within milliseconds by a graph traversal from the declared entry point.

Score is 9 rather than 10 because IRE requires explicit `integration_gate.toml` configuration to
know which directories "must be reachable." If that configuration was not present when the bug was
introduced, IRE would not have fired automatically. NOPF and CPC have no configuration dependency
for the archetypal case, but the 1-point deduction reflects the IRE configuration prerequisite.

**Strongest counter-argument on this axis**: The check would only have fired if it was already
running in CI at the time the bug was introduced. A gate that doesn't exist catches nothing. Stage 1
must be deployed before it prevents anything.

---

### Axis 2 — Generalizability (weight 25%)

**Score: 7**

Evidence: PROP-03 addresses three of the named "defined but not wired" instances from the forensic
report, with the caveat that coverage of the non-archetypal cases requires Stages 2-4.

- `DEVIATION_ANALYSIS_GATE` (unwired from `_build_steps()`): REGC variant catches this — the gate
  constant exists in `ALL_GATES` but no step with `id="deviation-analysis"` exists in
  `_build_steps()`. This requires a REGC extension (gate-ID vs. step-ID cross-reference), which the
  proposal notes but does not fully specify. Partial credit.
- `SprintGatePolicy` / `TrailingGateRunner` (never instantiated in `execute_sprint()`): The proposal
  acknowledges IRE does not directly catch this case — it is "imported but never instantiated in
  production path," which requires a REGC variant scanning for Protocol implementations. The check
  produces WARNING, not ERROR, without the extension. Partial credit.
- The NOPF check generalizes to any codebase that uses `Optional[Callable]` for dependency
  injection, which is a common Python pattern. This is genuine category coverage.

Score is 7 rather than 8+ because the two non-archetypal instances require REGC extensions that are
specified but not fully designed in the proposal. Full generalizability to all three named instances
requires the complete 15-day suite, not the 5-day MVP.

**Strongest counter-argument on this axis**: The Devil's Advocate correctly identifies that NOPF +
CPC (Stage 1) addresses only one of three known instances. Claiming generalizability requires
delivering Stage 2 and Stage 3.

---

### Axis 3 — Implementation Complexity (weight 20%, inverted — higher = simpler)

**Score: 3**

Evidence: The proposal estimates ~15 developer-days across 3 new files, 4 modified files, 4 new
dataclasses, a configuration schema, a suppression annotation parser, and a new pipeline step.

Per the scoring rubric:
- 3 new files: `audit/integration_gate.py`, `audit/ast_utils.py`, `tests/audit/test_integration_gate.py`
- 4 modified files: `pipeline/gates.py`, `pipeline/models.py`, `audit/__init__.py`, `roadmap/executor.py`
- New subsystem: 4 detection algorithms, `IntegrationReport` dataclass, `run_integration_checks()` entry point
- Significant test coverage required: 7 formal acceptance tests including fixture source trees

This falls in the "2-3" band: "Cross-cutting infrastructure change; new subsystem; significant test
coverage." The Stage 1 MVP (NOPF + CPC) narrows to approximately 4 files, 2 new abstractions, and
~250 lines of new code — which would score 5-6. But the proposal as a whole scores 3 given its full
scope.

**Note**: The Devil's Advocate's Cross-Examination revealed that Stage 1 alone may require IRE
infrastructure (reachability graph) for reliable NOPF severity classification — which would push
Stage 1 scope upward toward 7-8 developer-days. This does not change the score but is a planning
risk.

**Strongest counter-argument on this axis**: The complexity is the most legitimate objection to the
proposal. A 15-day implementation for a static analysis subsystem is a significant investment that
must be justified by recurring catch rate across multiple incidents, not a single historical bug.

---

### Axis 4 — False Positive Risk (weight 15%, inverted — higher = lower FP risk)

**Score: 6**

Evidence: The proposal has a credible suppression mechanism and conjunction heuristics that reduce
false positive rate, but real FP scenarios exist and require active management.

True false positive scenarios identified in debate:
1. **Factory construction** (Risk 3): ExecutorFactory pattern bypasses call-site analysis. Mitigated
   by suppression annotation but requires developer awareness. Estimated FP rate: low (factory
   patterns are concentrated; developers using them know to annotate).
2. **Dry-run no-ops** (Risk 1): NOPF fires on intentional `(0, "", False)` returns in dry-run
   branches. Mitigated by conjunction with CPC (requires both to fire), but a dry-run mode that
   always passes `runner=None` at the call site would still trigger CPC. Estimated FP rate: moderate
   for codebases with extensive dry-run infrastructure.
3. **NOPF heuristic brittleness**: Code that uses `PortifyStatus.SUCCESS` enum or renames `exit_code`
   to `status_code` would evade NOPF (false negative, not false positive). But code that introduces
   a new success indicator not in the heuristic list would initially be missed, then cause noise
   when the heuristic is updated to include it.

Score of 6 reflects "occasional FP expected (5-10% of runs in normal operation); override
available." The suppression annotation is the override. The conjunction requirement reduces FP rate
substantially from naive NOPF-only scanning.

**Strongest counter-argument on this axis**: An active codebase with dependency injection patterns
for testability will likely encounter CPC false positives on correctly-designed injectable
components. The mitigation (annotation) is sound in principle but creates a continuous annotation
obligation as new injectable components are added.

---

### Axis 5 — Integration Fit (weight 15%)

**Score: 7**

Evidence: The proposal reuses existing infrastructure and fits the `GateCriteria` / `ALL_GATES`
pattern, but introduces a new pipeline step type (code analysis rather than document generation)
that requires moderate new wiring.

Integration assets reused:
- `audit/dependency_graph.py` DependencyEdge, EdgeTier, DependencyGraph (IRE check)
- `audit/dead_code.py` `_is_entry_point()`, `_is_framework_hook()` (exclusion logic)
- `audit/tool_orchestrator.py` FileAnalysis (REGC implementation lookup)
- `pipeline/gates.py` GateCriteria, SemanticCheck (INTEGRATION_GATE definition)
- `roadmap/gates.py` ALL_GATES registry (INTEGRATION_GATE entry)

New infrastructure required:
- `audit/ast_utils.py` (new shared module)
- `INTEGRATION_GATE` in `pipeline/gates.py` (new GateCriteria instance — well-defined extension point)
- New step in `_build_steps()` (roadmap/executor.py) — requires understanding of pipeline step
  model, but conceptually a single function call addition

Score is 7 rather than 8+ because the new step type (code analysis rather than document content
validation) requires the pipeline executor to handle a different input/output model. All existing
gates validate `content: str` from a generated document. INTEGRATION_GATE validates `source_root:
Path` — a conceptually adjacent but mechanically distinct input. The pipeline executor was not
designed with this input type in mind.

**Strongest counter-argument on this axis**: The proposal's INTEGRATION_GATE definition in Section 5
workarounds this mismatch by having `run_integration_checks()` write an `integration-report.md`
file whose frontmatter is then validated by the existing gate pattern. This is slightly awkward —
the check writes a report, then the gate validates the report's frontmatter — but it fits the
existing infrastructure without requiring executor changes. It is an acceptable tradeoff.

---

## Scoring Summary Table

| Axis | Weight | Raw Score | Weighted |
|------|--------|-----------|---------|
| Catch Rate | 25% | 9 | 2.25 |
| Generalizability | 25% | 7 | 1.75 |
| Implementation Complexity (inverted) | 20% | 3 | 0.60 |
| False Positive Risk (inverted) | 15% | 6 | 0.90 |
| Integration Fit | 15% | 7 | 1.05 |
| **Composite** | **100%** | — | **6.55** |

**Composite Score: 6.55**

Per the scoring bands:

| Band | Range | This Proposal |
|------|-------|--------------|
| Tier 1 — Implement Immediately | 7.5–10 | |
| **Tier 2 — Implement in Phase 2** | **6.0–7.4** | **6.55** |
| Tier 3 — Consider After Phase 2 | 4.5–5.9 | |
| Tier 4 — Reconsider | < 4.5 | |

---

## Final Verdict and Adoption Profile

**Verdict: Implement in Phase 2, staged delivery, MVP-first.**

PROP-03 earns its Tier 2 placement on the strength of its catch rate and the uniqueness of its
detection class. No existing gate catches "defined but not wired." The proposal fills a genuine
structural gap. The composite score of 6.55 is pulled down by complexity (3/10) and reflects the
honest cost of building a new static analysis subsystem, not a flaw in the design.

**Recommended Adoption Profile:**

**Phase 2A (5-7 days)**: Deploy the NOPF + CPC conjunction MVP against the existing codebase.
Gate behavior: WARNING severity for either check alone; ERROR only for conjunction on the same
guarded attribute. Validate that the MVP fires on `executor.py:397-399` and `PortifyExecutor`
before CI deployment. Establish the suppression annotation syntax. Accept that this addresses only
the archetypal bug class.

**Phase 2B (4-5 days)**: Add IRE with explicit `integration_gate.toml` configuration for `steps/`
directories. This closes coverage on the 8 unreachable `cli_portify/steps/` modules and adds the
second independent signal on the archetypal incident. IRE provides value beyond the archetypal case
for any future package that introduces a `steps/` directory.

**Phase 2C (4-5 days)**: Add REGC and the configuration framework. This extends coverage to
`DEVIATION_ANALYSIS_GATE` and `SprintGatePolicy` via REGC extensions. Implement the dynamic factory
handling to reduce CPC false positives in executor-heavy code paths.

**Phase 2D (deferred)**: Sprint pre-flight integration (Option B in proposal). Valuable as a
development-time feedback mechanism but lower priority than release-tier enforcement.

**What this proposal does NOT replace:** Proposal 04 (Smoke Test Gate) and Proposal 05 (Silent
Success Detection) address runtime verification — actually running the pipeline and observing
behavior. PROP-03 is complementary. Static analysis finds "defined but not wired" at analysis time.
Smoke tests find "runs but does nothing" at execution time. Both layers are needed. PROP-03 alone
would not catch a bug where step dispatch is wired but implementations are incorrect. Smoke tests
would not catch a bug in a code path that the smoke test does not exercise. These proposals must be
evaluated as a suite, not as substitutes.

---

## Top 2 Failure Conditions

### Failure Condition 1 — CPC False Positives on Dependency Injection Patterns Block Developer Velocity

**Scenario**: The codebase adopts a broader dependency injection pattern for testability — multiple
classes gain `Optional[Callable]` constructor parameters that are provided in production via
`DIContainer.inject()` calls that AST analysis cannot resolve. CPC fires on each new class. Every
sprint that introduces an injectable component triggers CPC findings that require suppression
annotations before the pipeline will proceed. Developers begin reflexively adding suppression
annotations without reviewing findings. The gate loses its signal value.

**Trigger conditions**: CPC false positive rate exceeds ~2 findings per sprint cycle. This threshold
is where annotation overhead shifts from deliberate documentation to reflexive suppression.

**Mitigation levers**: (1) Raise ERROR threshold to require NOPF conjunction (already recommended).
(2) Add `DIContainer`-aware factory detection to the dynamic imports module. (3) Implement
allow-listing for classes with documented injection patterns. (4) Move to WARNING-only for CPC
without NOPF conjunction.

**Probability**: Moderate. The codebase currently has limited DI patterns. If architectural direction
moves toward broader DI, this risk materializes within 6-12 months of deployment.

---

### Failure Condition 2 — NOPF Heuristic Staleness Creates False Negatives After Codebase Refactor

**Scenario**: A refactor renames `exit_code` to `step_status_code` and replaces the integer `0`
return with a `StepResult.SUCCESS` enum value. NOPF's success indicator heuristics do not include
`step_status_code` or `StepResult.SUCCESS`. A new no-op fallback is introduced using the new naming
convention. NOPF does not fire. The same bug class that PROP-03 was built to prevent slips through
because the heuristic list was not updated.

**Trigger conditions**: Any renaming of exit-code variables or replacement of integer literals with
enum values. Code style evolution is routine over 12-24 month horizons.

**Mitigation levers**: (1) Enumerate recognized success indicators from an authoritative source
(e.g., parse the codebase's own success sentinel definitions at check initialization time rather
than maintaining a static list). (2) Add a test that runs NOPF against a fixture using each
recognized success sentinel to catch heuristic staleness in CI. (3) Include NOPF heuristic review
in the definition-of-done for any task that introduces a new return type or renames exit-code
variables. (4) Escalate the REGC check as a partial compensating control: even if NOPF misses a
new no-op form, IRE would still catch unreachable step modules if they exist.

**Probability**: High over a 24-month horizon. Code style and type conventions evolve continuously.
This failure condition represents the baseline maintenance cost of owning any heuristic-based static
analysis check.

---

*Debate produced: 2026-03-17. Scoring framework: `proposals/scoring-framework.md`. Proposal under
review: `proposal-03-code-integration-gate.md`. Status: complete — ready for phase planning.*
