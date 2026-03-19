# Adversarial Debate — Proposal 01: Link 3 Code Fidelity Gate

**Debate ID**: D01
**Proposal under review**: `proposal-01-link3-code-fidelity.md`
**Scoring framework**: `scoring-framework.md`
**Incident context**: `docs/generated/cli-portify-executor-noop-forensic-report.md`
**Date**: 2026-03-17
**Format**: 3-round adversarial debate + composite scoring

---

## Table of Contents

1. [Round 1 — Opening Positions](#round-1--opening-positions)
2. [Round 2 — Cross-Examination](#round-2--cross-examination)
3. [Round 3 — Synthesis](#round-3--synthesis)
4. [Scoring Table](#scoring-table)
5. [Composite Score](#composite-score)
6. [Final Verdict](#final-verdict)
7. [Top Failure Conditions](#top-failure-conditions)

---

## Round 1 — Opening Positions

### Proponent: The Case FOR Proposal 01

Proposal 01 is the most structurally sound of the five proposals because it attacks the root cause
of the cli-portify incident at the architectural level, not the symptom level.

**The incident is a structural gap, not a point defect.**

The forensic report (Section 5) is explicit: the fidelity chain reads
`Spec → Roadmap → Tasklist → Code`, and Links 1 and 2 have gate infrastructure. Link 3 does not
exist. This is not a matter of a wrong threshold or a missed test — it is an entire class of
verification that the pipeline never performs. Every release of cli-portify (v2.24, v2.24.1, v2.25)
shipped with `(exit_code=0, stdout="", timed_out=False)` as the production return value for every
step because no gate at any link asked: "Did the code do what the tasklist said it should?"

**The proposal would have caught the specific defect deterministically.**

The key programmatic check is the WIRING assertion type. The Appendix A of the proposal
demonstrates exactly what the v2.25 T03.04 phase file should have contained:

```yaml
- type: WIRING
  id: WIRE-002
  description: "run_portify() must pass step_runner= argument to PortifyExecutor constructor"
  consumer: "src/superclaude/cli/cli_portify/executor.py"
  provider_symbol: "step_runner"
  context: "PortifyExecutor constructor call in run_portify()"
  pattern: "keyword_argument"
```

The Phase A programmatic check for WIRE-002 scans the AST of `executor.py` for a call to
`PortifyExecutor(` with a `step_runner=` keyword argument. The v2.25 code at lines 1395-1401 has no
such call. The check would have returned `passed=False` with evidence `executor.py:1395`.

This is not a heuristic. It is an AST parse. The result is deterministic, replayable, and produces
exact file:line evidence. This satisfies the scoring framework's Axis 1 anchor condition: "produces
a deterministic FAIL output when this condition exists."

**The generalizability is broad across the codebase's actual failure pattern.**

The forensic report (Section 7) identifies three additional "defined but not wired" instances that
exist right now in the codebase:

1. `DEVIATION_ANALYSIS_GATE` — fully defined in `roadmap/gates.py:712-758`, never called from
   `_build_steps()`.
2. `SprintGatePolicy` — stub at `sprint/executor.py:47-90`, never invoked from `execute_sprint()`.
3. `TrailingGateRunner` — defined in `pipeline/trailing_gate.py`, never called from
   `execute_sprint()`.

The `noop_detector.py` module and the WIRING assertion type would flag all three. A scan for
`Optional[Callable]` parameters defaulting to `None` with a success-returning else branch will
catch every future instance of this pattern, not just the cli-portify variant. Proposal 01 does not
fix one bug — it builds a detection mechanism for an entire bug class that has already recurred
three times independently in this codebase.

**The architecture mirrors what already works.**

The proposal's design is not invented from scratch. It follows the exact same two-phase pattern as
`TASKLIST_FIDELITY_GATE` (`tasklist/gates.py:20-43`) and `GateCriteria`
(`pipeline/gates.py:20-69`): deterministic Python checks first, LLM semantic checks second, Python
enforcement of the final pass/fail via a structured frontmatter field. The `SprintGatePolicy` stub
at `sprint/executor.py:47-90` is already the designated integration hook — it just needs to be
completed. Link 3 is not a new architectural pattern; it is the completion of a partially built one.

**The Problem B acknowledgment is a strength, not a weakness.**

The proposal is honest that a gate is only as good as the assertions it validates. It addresses
this directly through the tasklist generator changes in Section 2.7, which codify assertion
derivation rules: any acceptance criterion describing a connection between two code components must
emit a WIRING assertion. This closes the loop. The forensic report found that T03.04's acceptance
criteria were "silent on dispatch wiring" — the proposal's changes to `sc-tasklist-protocol/SKILL.md`
would make that silence a policy violation for any Tier=STRICT task.

The proposal is the right architectural addition because it fills the one structural gap that
allows documentation-quality pipelines to ship code-quality failures silently.

---

### Devil's Advocate: The Case AGAINST Proposal 01

This proposal is an ambitious, well-written document that solves a problem the team does not yet
have the preconditions to solve. It should not be implemented as specified, and certainly not first.

**The proposal's own Problem B admission is fatal, not acceptable.**

The proponent calls the Problem B acknowledgment a strength. I call it a load-bearing confession.
The proposal states (Section 1.2, emphasis mine):

> "Even when a Link 3 gate is introduced, it can only be as good as the acceptance criteria it
> validates. The v2.25 tasklist acceptance criteria for T03.04 were silent on dispatch wiring.
> A purely mechanical gate would have passed them."

This means: if the proposal had existed during v2.25 development and the tasklist generator had
NOT yet been updated (Phase 3), the gate would have passed the cli-portify defect. The proposal
requires a co-dependent change to the tasklist generator, or it provides zero additional protection
for the exact bug class it was motivated by. Phase 3 is estimated at ~3 additional sprint sessions
and is labeled "Medium-Large" effort with "requires validation against real roadmaps." The proposal
cannot be evaluated as a self-contained unit — it is two proposals stapled together.

**The AST-based WIRING check is brittle against the codebase's actual patterns.**

The proposal's primary catch mechanism for the cli-portify defect is an AST scan for
`PortifyExecutor(` with a `step_runner=` keyword argument. This works for this specific bug. But
the proposal's own Section 6.1 identifies the primary false negative risk: dynamic dispatch. The
cli-portify architecture uses a `STEP_REGISTRY` dictionary pattern. A correct fix to the bug does
NOT require passing `step_runner=` as a keyword argument — it could be implemented as:

```python
def _real_step_runner(step):
    return STEP_DISPATCH[step.step_id](config)

executor = PortifyExecutor(steps=steps, ..., step_runner=_real_step_runner)
```

But equally valid production code could restructure `_execute_step()` to dispatch directly from
`STEP_REGISTRY` without using the `step_runner` injection point at all:

```python
def _execute_step(self, step):
    fn = STEP_DISPATCH.get(step.step_id)
    if fn is None:
        raise PortifyError(f"No implementation: {step.step_id}")
    return fn(step)
```

In this refactoring, the `step_runner` injection pattern is removed entirely. The WIRE-002
assertion (`"run_portify() must pass step_runner= to PortifyExecutor"`) would now be a false
positive: it would flag the correct implementation as a wiring failure because `step_runner=` is
absent, even though dispatch is fully wired. The AST check encodes a specific architectural
decision (callback injection) rather than the semantic requirement (dispatch works). Any refactoring
that changes the injection pattern fires the gate incorrectly.

**The scope is 11 sprint sessions across 4 phases. This is not a gate; it is a subsystem.**

The scoring framework's Axis 3 calibration explicitly states: "The full audit gating v1.2.1 phase
plan (4 phases, 9+ files) scores approximately 2." Proposal 01 is its own 4-phase, 9-file plan
requiring ~880 new lines + ~175 modified lines. By the framework's own calibration, this scores
near the floor on Implementation Complexity. The team is being asked to build a subsystem to fix
a bug that has a two-line hotfix (pass `step_runner=_real_step_runner` to `PortifyExecutor`).

The dependency chain (Section 7.3) is particularly concerning:
- `AuditWorkflowState` enum must exist first (spec Phase 1)
- `GateResult` dataclass must exist first (spec Phase 1)
- `SprintGatePolicy` wiring must complete first (spec Phase 2)
- `audit_gate_required` in tasklist bundle must exist first (delta NR-1)

This gate cannot be activated until after four other pieces of infrastructure are built. The
"critical path" ends at Phase 3, meaning full protective value is 3-4 phases away. During that
entire window, developers operate with false confidence that "Link 3 is coming."

**The false positive surface is underestimated.**

The proposal identifies three FP scenarios in Section 6. It does not identify the most common one:
TDD red-phase development. During a sprint session where a developer is legitimately building an
integration incrementally — writing the executor skeleton first, then wiring it to steps — every
commit before the final wiring is complete will fire WIRE-002 as a failure. Under `standard`
profile this is a warning, but warnings that fire on every intermediate commit train developers to
ignore them. Under `strict` profile it blocks task completion until all wiring is done in a single
atomic commit, which conflicts with incremental development practices.

The `min_lines: 50` threshold in DELIVERABLE checks is arbitrary and will generate developer
friction on legitimately small modules. A 30-line helper function that correctly implements a step
fails the gate not because it is broken, but because the proposal author guessed that 50 was
"substantial enough." This is tunable, but every tuning parameter is a future maintenance burden.

**The tasklist generator change creates a new category of generator errors.**

The proposal modifies `sc-tasklist-protocol/SKILL.md` to emit `code_fidelity_assertions` in
generated phase files. This means every future tasklist generation session is subject to assertion
classification errors. The classification rules in Section 2.7 use text pattern matching on
acceptance criteria: "routes", "wires", "calls", "dispatches" trigger WIRING assertions. But:

- Natural language acceptance criteria are often written without these specific verbs.
- The v2.25 tasklist T03.04 acceptance criteria that failed to catch the bug did not use any of
  these trigger words — it said "execute each step," which under Section 6.2 is explicitly flagged
  as a known false negative risk.
- The mitigation for this (passive-voice patterns + minimum WIRING density for Tier=STRICT) adds
  complexity to the classifier without eliminating the ambiguity.

The result is that the tasklist generator now produces structured assertions that may or may not
reflect what the human engineer intended. A misclassified assertion (BEHAVIORAL when WIRING was
needed) produces no Phase A check, and the gate provides false confidence.

The proposal is not wrong about what needs to exist eventually. It is wrong about treating this
as a single coherent proposal when it is actually two coupled proposals (Link 3 infrastructure +
tasklist generator overhaul) each of which individually fails to catch the incident without the
other.

---

## Round 2 — Cross-Examination

### Proponent Responds to the Devil's Advocate's Strongest Objection

The Devil's Advocate's strongest objection is the WIRING check brittleness argument: that
correctly refactored code that eliminates the `step_runner=` injection pattern would fire
WIRE-002 as a false positive.

This objection is valid on the specific WIRE-002 example from Appendix A. The response is that
Appendix A shows what assertions **should have existed in the v2.25 tasklist for T03.04**. The
proposal does not claim that WIRE-002 must persist forever as written — it claims that the
assertion must be generated by the tasklist generator to match whatever architectural pattern the
acceptance criteria describe.

The correct assertion for a refactored implementation that uses direct dictionary dispatch rather
than callback injection would be:

```yaml
- type: WIRING
  id: WIRE-001
  description: "Each STEP_REGISTRY key must have a corresponding callable in a dispatch map"
  consumer: "src/superclaude/cli/cli_portify/executor.py"
  provider_symbol: "run_validate_config"
  provider_module: "superclaude.cli.cli_portify.steps.validate_config"
  context: "STEP_DISPATCH dictionary or equivalent dispatch map"
```

WIRE-001 from Appendix A is exactly this assertion. The AST check for WIRE-001 scans the executor
for a dictionary literal containing string keys matching step IDs and values that are callable
references imported from the `steps/` modules. This check is architecture-agnostic: it does not
care whether dispatch uses callback injection or direct dictionary lookup. It only requires that
a dispatch connection exists somewhere in the consumer file.

The proposal addresses this explicitly in Section 6.1:
> "The WIRING check must include a secondary scan for dictionary literals with string keys
> matching the provider symbol name (e.g., `{"validate-config": run_validate_config}` dispatch
> maps)."

The brittleness the Devil's Advocate identifies is real for a naively implemented WIRING check.
The proposal's mitigated implementation is not naive — it specifically handles the
`STEP_REGISTRY`/`STEP_DISPATCH` dictionary pattern. WIRE-001, not WIRE-002, is the
architecture-agnostic assertion. WIRE-002 is a supplementary check for the specific bug in the
specific code as it existed. A correctly implemented refactor that replaces callback injection
with dictionary dispatch would still pass WIRE-001 (the dict contains the import) and would
correctly fail WIRE-002 only if `step_runner=` was part of the acceptance criteria. If the
acceptance criteria no longer describes a `step_runner=` requirement (because the architecture
changed), WIRE-002 should not be in the tasklist and would not be generated.

The brittleness argument reduces to: "if the assertions are wrong, the gate is wrong." This is
true of every gate in the system, including `TASKLIST_FIDELITY_GATE` — if the LLM misclassifies
a deviation as LOW severity, the gate passes a genuine fidelity failure. Proposal 01 does not
introduce a new failure mode; it adds a new layer that is subject to the same fundamental
constraint all gates share: quality of input determines quality of output.

---

### Devil's Advocate Attacks the Proponent's Weakest Claim

The proponent's weakest claim is this sentence from the opening:

> "Proposal 01 does not fix one bug — it builds a detection mechanism for an entire bug class
> that has already recurred three times independently in this codebase."

The three additional "defined but not wired" instances cited (DEVIATION_ANALYSIS_GATE,
SprintGatePolicy, TrailingGateRunner) are not caught by the proposal's primary catch mechanism.
They are caught by `noop_detector.py`, which scans for `Optional[Callable]` parameters that
default to `None` and return success constants in the `None` branch.

Let us examine whether these three instances actually match that pattern:

1. **DEVIATION_ANALYSIS_GATE** is "fully defined in `roadmap/gates.py:712-758` but not wired
   into `_build_steps()`." This is not a no-op fallback — it is a gate that is never called at
   all. `_execute_step()` does not have an `Optional[Callable]` parameter for this gate; the gate
   simply does not appear in the step list. `noop_detector.py` would not flag this because there
   is no fallback branch to detect. There is only absence.

2. **SprintGatePolicy** is described as a stub at `sprint/executor.py:47-90`. If it is a class
   stub with placeholder methods, those methods may return `None` or `pass` rather than a
   success constant. Whether `noop_detector.py` catches this depends on the exact stub form —
   the proposal provides no fixture or evidence that the stub matches the scanner's detection
   pattern.

3. **TrailingGateRunner** is "never called from `execute_sprint()`." Again, this is absence, not
   a fallback. No `Optional[Callable]` parameter exists in `execute_sprint()` for this; the
   function simply never calls the runner.

The honest generalizability claim for this proposal is narrower than the proponent states. The
`noop_detector.py` catches the specific pattern: "callable injected via optional parameter,
production code forgets to inject it, else branch returns success." It does not catch: "entire
subsystem never called," "gate defined but not registered," or "function exists but is not in
the call graph." Those are genuinely different detection problems requiring different mechanisms —
`audit/dead_code.py` already exists for reachability analysis and addresses them more directly.

The Axis 2 (Generalizability) claim of "entire category of integration bugs" needs to be honest
about what the proposal actually catches versus what requires the existing dead code detector or
a different proposal entirely.

---

## Round 3 — Synthesis

Both parties agree on the following honest assessment:

### Points of Agreement

**1. The structural gap is real and this proposal correctly identifies it.**

Link 3 does not exist. The pipeline has no gate between tasklist acceptance criteria and code
output. This is a genuine architectural gap, not a subjective quality preference. The proposal's
diagnosis is accurate and the two-phase (programmatic + LLM) architecture is the right pattern
for bridging it.

**2. The WIRING check, specifically WIRE-001 (dispatch map variant), would have caught the
cli-portify defect deterministically.**

An AST scan for a dictionary literal in `executor.py` mapping step IDs to callable imports from
`steps/` would have found no such dictionary in v2.25 code and returned `passed=False`. This is
the correct catch mechanism. WIRE-002 (callback injection variant) is brittle; WIRE-001
(dispatch map variant) is architecture-agnostic. The proposal includes both, which is correct.

**3. The generalizability is narrower than the proponent claims but still meaningful.**

`noop_detector.py` catches specifically: "optional callable defaulting to None, None branch
returns success constant." The three additional instances cited (DEVIATION_ANALYSIS_GATE,
SprintGatePolicy, TrailingGateRunner) are partially covered but are better characterized as
"defined but not wired" — an absence problem, not a fallback problem. The WIRING assertion type
generalizes broadly across any future task that requires two code components to connect. That is
genuinely broad (any integration task). The no-op scanner generalizes to the specific injection
pattern. Honest Axis 2 score: high but not maximum.

**4. Problem B (acceptance criteria quality) remains the binding constraint.**

If the tasklist generator does not emit WIRING assertions for integration tasks, the gate has
nothing to check programmatically and falls through to LLM evaluation, which was the regime that
failed in v2.25. The Phase 3 changes to `sc-tasklist-protocol/SKILL.md` are not optional
enhancements — they are the prerequisite for Phase A checks having any teeth. The proposal should
be explicit that Phase 1-2 (gate infrastructure) without Phase 3 (generator changes) is a gate
with no input assertions, not partial protection.

**5. Implementation complexity is high but the phased plan is well-structured.**

The ~11 sprint session total is substantial. However, Phase 1 (ProgrammaticChecker + noop_detector
+ unit tests) is independent of all sprint runtime dependencies and can be built in parallel with
other v1.2.1 work. The dependency chain (AuditWorkflowState → GateResult → SprintGatePolicy)
is real but affects Phase 2 integration only, not Phase 1 library code. The proposal is correctly
sequenced.

### Honest Composite Score

See the scoring table below. Both parties agree the composite score is in the **Tier 2 range
(6.0–7.4)**: high value, moderate-to-high complexity, schedule in Phase 2 with Phase 1 library
work beginning immediately in parallel.

---

## Scoring Table

| Axis | Weight | Score | Evidence |
|------|--------|-------|---------|
| **Catch Rate** | 25% | **8** | The WIRING check WIRE-001 (dispatch map variant) would deterministically flag absence of a step ID-to-callable mapping in `executor.py`. AST parse of v2.25 `executor.py` finds no dictionary literal with step ID keys and `steps/` imports. `noop_detector.py` finds the `if self._step_runner is not None: ... else: exit_code, stdout, timed_out = 0, "", False` pattern at `executor.py:393-415`. Both checks produce `passed=False` with `evidence="executor.py:393"` and `evidence="executor.py:1395"` respectively. Not scored 10 because the gate requires Phase 3 (tasklist generator changes) to have input assertions to run against. Without assertions in the phase file, Phase A has nothing to scan for. Under `standard` profile with no assertions, the gate warns but does not block — this was the regime that failed. Catch rate is 10 conditional on Phase 3 being complete; 4 without it; 8 as a realistic expected value weighting the two scenarios. |
| **Generalizability** | 25% | **7** | WIRING assertion type generalizes to any future integration task describing a connection between two code components — this covers a broad class of "defined but not wired" bugs. `noop_detector.py` specifically catches the optional-callable-defaulting-to-success pattern; this is the exact pattern at `executor.py:393` and would catch future instances of the same anti-pattern. The three additional instances cited (DEVIATION_ANALYSIS_GATE, SprintGatePolicy, TrailingGateRunner) are partially covered: SprintGatePolicy is a stub that likely matches the no-op pattern; DEVIATION_ANALYSIS_GATE and TrailingGateRunner are absence-of-call problems that `noop_detector` does not directly address (though WIRING assertions on the roadmap step list would). The existing `audit/dead_code.py` handles reachability for the pure-absence cases. Score 7 reflects genuine broad coverage with honest acknowledgment that "entire category" is an overstatement for the no-op detector specifically. |
| **Implementation Complexity (inverted)** | 20% | **3** | 9 files modified/created, ~880 new lines + ~175 modified lines, 4 new abstractions (`CodeFidelityGate`, `ProgrammaticChecker`, `LLMAssistantChecker`, `AssertionParser`), 4-phase rollout over ~11 sprint sessions, with a 5-item dependency chain that serializes phases 2 and 3 onto pre-existing infrastructure work. The scoring framework calibrates the full audit gating v1.2.1 phase plan at approximately 2. Proposal 01 is a 4-phase plan unto itself, slightly smaller than the full spec, scored at 3. Phase 1 library code is self-contained and scores closer to 6 in isolation, but the full proposal including runtime integration and generator changes scores 3 honestly. |
| **False Positive Risk (inverted)** | 15% | **6** | Three FP scenarios explicitly identified in Section 6. The dynamic dispatch FP is mitigated (secondary dictionary scan). The TDD red-phase FP (flagging incomplete intermediate commits) is not addressed in the proposal — this is a real friction source in incremental development workflows. `min_lines: 50` DELIVERABLE threshold is arbitrary and will fire on legitimate small modules. The `legacy_migration` profile provides backward compatibility. Under `standard` profile, Phase B failure only warns; Phase A failure blocks. FP rate in normal operation is estimated at 5-15% before tuning — developers writing integration steps incrementally will encounter false gates on in-progress work. Override path is available but increases developer friction. Score 6: occasional FP expected, override path exists. |
| **Integration Fit** | 15% | **7** | The proposal explicitly maps to `SprintGatePolicy` stub at `sprint/executor.py:47-90` as the integration hook. It follows the same two-phase pattern as `TASKLIST_FIDELITY_GATE` and `GateCriteria`. `CodeFidelityResult` parallels `GateResult`. The `audit_task_*` state machine integration is correctly identified at `execute_sprint()` lines 668-787. The existing `audit/dead_code.py` is cited as potential reuse for reachability checks. The primary integration gap is that `SprintGatePolicy` stub completion requires the `AuditWorkflowState` enum and `GateResult` base class (spec Phase 1) to exist first — these are not yet built, making Phase 2 integration conditional on other work completing. Score 7: excellent conceptual fit, good reuse of patterns, minor new wiring required, blocked on Phase 1 infrastructure that must be built in parallel. |

---

## Composite Score

```
Composite = (8 × 0.25) + (7 × 0.25) + (3 × 0.20) + (6 × 0.15) + (7 × 0.15)
          = 2.00 + 1.75 + 0.60 + 0.90 + 1.05
          = 6.30
```

**Band: Tier 2 — Implement in Phase 2** (range 6.0–7.4)

> Good value; moderate complexity; schedule in next phase.

---

## Final Verdict

### Which Profile of Project / Release Should Adopt This First

**Profile: New releases that include integration tasks in Tier=STRICT phases, where acceptance
criteria describe connections between code components (executor-to-steps, registry-to-callables,
plugin-to-runner).**

Concretely: any sprint that produces a new executor class, a new registry/dispatch pattern, or a
new injectable callable dependency is exactly the scenario Link 3 was designed for. The cli-portify
incident is not idiosyncratic — the forensic report identifies the same "defined but not wired"
pattern recurring in DEVIATION_ANALYSIS_GATE, SprintGatePolicy, and TrailingGateRunner. Any
project using the SuperClaude pipeline to generate integration-heavy code is the right adopter.

**Adoption sequence recommendation:**

1. **Immediately (Phase 1)**: Build `noop_detector.py` and `ProgrammaticChecker` as standalone
   library code with no sprint runtime dependencies. Run `noop_detector` in CI against the current
   codebase — it will flag `executor.py:393-415` and likely the SprintGatePolicy stub today, before
   any gate infrastructure exists. This provides value in weeks, not months.

2. **Phase 2 (after AuditWorkflowState + GateResult land)**: Complete `SprintGatePolicy` and wire
   `CodeFidelityGate.evaluate()` into `execute_sprint()`. Activate under `legacy_migration` profile
   (no blocking, artifact collection only) for all existing sprint runs.

3. **Phase 3 (prerequisite for real protection)**: Extend `sc-tasklist-protocol/SKILL.md` to emit
   `code_fidelity_assertions`. Only after this change do new tasklist bundles have WIRING assertions
   for the gate to check. Promote to `standard` profile for new bundles immediately; maintain
   `legacy_migration` for pre-Phase-3 bundles.

4. **Full enforcement**: `strict` profile for Tier=STRICT tasks; `standard` for all others;
   `legacy_migration` only by explicit project-level override.

**Projects that should NOT adopt first**: Mature projects with stable, non-integration-heavy
sprint tasks (documentation pipelines, config generation, content synthesis) will see the highest
FP rates and the lowest catch rate. For these projects, Proposal 04 (Smoke Test Gate) or
Proposal 05 (Silent Success Detection) likely provides better ROI at lower complexity cost.

---

## Top Failure Conditions

### Failure Condition 1: Phase 3 Is Deprioritized or Deferred

**Mechanism**: The proposal ships as Phases 1-2 only (gate infrastructure + sprint integration)
without the tasklist generator changes in Phase 3. Existing tasklist bundles have no
`code_fidelity_assertions` field. Under `standard` profile with no assertions, the gate emits a
warning but does not block — and every task clears `audit_task_passed` as if the gate ran
successfully. The gate infrastructure exists but has no input; the pipeline continues shipping
integration failures with the gate in place and passing.

**Why this is likely**: Phase 3 is explicitly "Medium-Large" effort requiring "validation against
real roadmaps." It is the most expensive phase and the hardest to estimate. Under schedule
pressure, Phases 1-2 get shipped as "Link 3 complete" and Phase 3 is moved to the next backlog
cycle. The team operates with false confidence: the gate is live, the dashboard shows it running,
but it has never checked a WIRING assertion in production.

**Signal that this is happening**: After Phase 2 ships, run a query on sprint audit artifacts.
If `CodeFidelityResult.checks` is empty (no assertions parsed) for 100% of tasks, Phase 3 has not
landed. The gate is a no-op at the task level — the same structural failure it was designed to
catch has been instantiated in the gate itself.

**Detection**: Add an assertion density metric to Phase 2: any sprint run where 100% of tasks
produce `checks=[]` should emit a `failure_class="policy"` artifact (not a blocking gate failure,
but a pipeline health alert). This makes the Phase 3 gap visible before it causes production harm.

---

### Failure Condition 2: The Acceptance Criteria Pattern-Matching Misclassifies Integration Tasks

**Mechanism**: The tasklist generator applies the assertion derivation rules from Section 2.7.
A task's acceptance criterion reads: "The executor should process each step in sequence and record
the outcome." The classifier does not match any WIRING trigger words ("routes", "wires", "calls",
"dispatches", "invokes"). It emits only a BEHAVIORAL assertion. The LLM evaluates the BEHAVIORAL
assertion against the no-op implementation: the executor does process steps sequentially (the
no-op loop runs in the correct order) and does record outcomes (the no-op returns `(0, "", False)`
which is recorded). The BEHAVIORAL check passes. Phase A ran zero checks. Phase B passed. The
gate records `passed=True`.

**Why this is the cli-portify failure mode in a new form**: The v2.25 T03.04 acceptance criteria
were exactly this — behavioral descriptions of sequential flow and outcome recording with no
mention of what "processing" means. The LLM's BEHAVIORAL evaluation of "the executor processes
steps" would naturally pass on a loop that executes the no-op default, because the loop does
execute. The no-op satisfies the behavioral description.

**Why the mitigation is insufficient**: Section 6.2 proposes a "minimum density requirement":
any Tier=STRICT task that produces code files must have at least one WIRING assertion even without
explicit connection language. This is a valid rule but depends on the tasklist generator correctly
identifying which tasks "produce code files" and correctly classifying their Tier. If the Tier
assignment is wrong (task is Tier=STANDARD instead of STRICT), the minimum density rule does not
apply and the BEHAVIORAL-only path executes. The same LLM that failed to classify the v2.25
roadmap deviation as HIGH severity is now responsible for classifying whether a task is Tier=STRICT.

**The honest conclusion**: Link 3's Phase A protection ceiling is bounded by the quality of
WIRING assertions generated. WIRING assertions are only as good as the acceptance criteria
language and the tier classification. Both of these remain LLM-generated inputs. The proposal
reduces but does not eliminate the LLM reliability ceiling for the exact failure mode it targets.

---

*Debate conducted against scoring framework `scoring-framework.md`. Scores use the exact composite
formula from that document. All evidence citations reference line numbers validated in the forensic
report and proposal as read during this session.*
