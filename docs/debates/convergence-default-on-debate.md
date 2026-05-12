---
debate_topic: "Should the roadmap pipeline convergence engine default to ON?"
date: 2026-04-03
rounds: 3
convergence_score: 0.72
rounds_completed: 3
verdict: "PROPONENT (default ON) -- with conditions"
---

# Adversarial Debate: Convergence Engine Default Behavior

**Question**: Should the roadmap pipeline's convergence engine default to ON (always active, no flag needed) rather than being opt-in via a `--convergence` flag?

**Proponent position**: Default ON, deprecate single-shot path.
**Opponent position**: Opt-in via `--convergence` flag, single-shot remains default.

---

## Evidence Base (Code Facts)

Before the debate begins, the following facts are established from the codebase:

1. **convergence.py** (384 lines) is fully implemented: TurnLedger budget model, DeviationRegistry with atomic persistence, 3-run convergence loop (catch/verify/backup), structural regression detection, semantic fluctuation logging, parallel regression validation with 3 agents, atexit cleanup.

2. **executor.py** already contains the wiring at line 688: `if step.id == "spec-fidelity" and hasattr(config, "convergence_enabled") and config.convergence_enabled` routes to `_run_convergence_spec_fidelity()`. The full integration function (`_run_convergence_spec_fidelity`, ~130 lines) exists and creates a TurnLedger, DeviationRegistry, and calls `execute_fidelity_with_convergence`.

3. **models.py** line 112: `convergence_enabled: bool = False` -- the field exists but defaults to False with no CLI flag to set it to True.

4. **commands.py**: Zero references to "convergence" -- no Click option exposes it.

5. **gates.py** line 1449: When `convergence_enabled=True`, the spec-fidelity step's gate is set to `None` (convergence engine manages pass/fail internally).

6. **Budget model**: MAX_CONVERGENCE_BUDGET = 61 turns covers 3 full cycles. CHECKER_COST=10, REMEDIATION_COST=8, REGRESSION_VALIDATION_COST=15. Budget credit on progress at 0.8 reimbursement rate.

7. **No test coverage** of the convergence integration path was found in the grep results -- the field is tested in model tests but the runtime path through `_run_convergence_spec_fidelity` has no integration test.

---

## Round 1: Opening Arguments

### PROPONENT (Default ON)

**P1. The current UX is objectively broken.** The single-shot spec-fidelity path fails, halts the pipeline, and forces users to manually `--resume` 3-4 times. This is not a "sometimes suboptimal" experience -- it is a workflow that routinely requires manual intervention to complete. The convergence engine was built specifically to solve this problem. Leaving it off by default means every user hits the broken path first.

**P2. The code is fully wired and ready.** `_run_convergence_spec_fidelity()` exists in executor.py with complete integration: TurnLedger creation, DeviationRegistry initialization, checker/remediation callbacks, regression handling. The only thing preventing activation is a boolean default. This is not a prototype -- it is shipped, reviewed code sitting behind a light switch nobody flipped.

**P3. Dead code is a liability.** 384 lines of convergence.py plus ~130 lines of integration code in executor.py represent ~500 lines of code that are never executed in production. Dead code rots: it drifts from the rest of the codebase, accumulates silent breakage, and confuses contributors who read it. The principle "ship it or delete it" applies directly.

**P4. Simplification through deletion.** If convergence is the default, the old single-shot LLM path for spec-fidelity becomes dead code. We can delete it, reducing the total code surface. Two code paths for the same step is an ongoing maintenance burden.

### OPPONENT (Opt-in Flag)

**O1. No integration tests exist for the convergence path.** The codebase shows zero integration test coverage of `_run_convergence_spec_fidelity()`. Making untested code the default for every user is reckless. The burden of proof for "safe to default ON" requires demonstrated test coverage of the full integration path, including edge cases (budget exhaustion, regression detection, semantic fluctuation).

**O2. Token cost is non-trivial and not all users can afford it.** MAX_CONVERGENCE_BUDGET = 61 TurnLedger units. A single convergence run can execute up to 3 checker cycles (cost 30) + 2 remediation cycles (cost 16) + potential regression validation (cost 15) = 61 units. In LLM API terms, this could mean 3x the token spend of the current single-shot approach. Users on tight API budgets or free tiers should not have this imposed by default.

**O3. Never been activated in production -- zero burn-in.** This code was built in v3.05 but has never run against real user workloads. We have no data on: false positive rates, remediation success rates, budget exhaustion frequency, or regression detection accuracy. Defaulting ON without burn-in data is a violation of progressive rollout principles.

**O4. v5.xx may supersede this entirely.** The backlog release v5.xx-ValidateRoadmapCLIIntegration lists convergence fate as an "open design decision." If we default ON now and v5.xx redesigns the validation pipeline, we create a harder migration: users who built workflows around always-on convergence must now adapt to whatever v5.xx delivers. Keeping it opt-in preserves design flexibility.

---

### Round 1 Scoring Matrix

| Dimension | Proponent | Opponent | Assessment |
|-----------|-----------|----------|------------|
| User Experience | P1: Strong (broken UX is factual) | -- | Proponent leads |
| Code Readiness | P2: Strong (code exists, wired) | O1: Strong (no integration tests) | Split -- code exists but untested |
| Maintenance | P3-P4: Moderate (dead code argument) | -- | Proponent leads |
| Cost | -- | O2: Strong (3x token cost) | Opponent leads |
| Risk | -- | O3: Strong (zero burn-in) | Opponent leads |
| Future Compat | -- | O4: Moderate (v5.xx uncertain) | Opponent leads slightly |

**Round 1 Convergence**: 35% -- significant disagreement on core dimensions.

---

## Round 2: Rebuttals and Refinement

### PROPONENT Rebuttal

**P5. Rebuttal to O1 (no integration tests).** The lack of integration tests is a valid concern but it is an argument for "write tests before shipping," not an argument for "never ship." The test gap can be closed in a single sprint. Furthermore, the convergence engine's internal functions (reimburse_for_progress, compute_stable_id, DeviationRegistry, etc.) are tested. The gap is in the end-to-end path, which is addressable.

**P6. Rebuttal to O2 (token cost).** The convergence engine has built-in cost control: TurnLedger budget accounting with can_launch() and can_remediate() guards. If budget is exhausted, it halts gracefully with a diagnostic report. The user is never "surprised" by unbounded cost. Moreover, the alternative -- manual `--resume` 3-4 times -- also costs tokens (each resume reruns the spec-fidelity LLM call). The convergence engine may actually be more token-efficient because remediation is targeted, not a full rerun.

**P7. Rebuttal to O4 (v5.xx).** The v5.xx design decision is explicitly listed as "open." Deferring a known UX fix because a future release *might* do something different is indefinite postponement. If v5.xx ships a better solution, we migrate then. In the meantime, users suffer the broken UX today.

**P8. Proposed compromise.** Default ON with `--no-convergence` escape hatch. This gives users who hit issues a way out, while fixing the broken default for everyone else.

### OPPONENT Rebuttal

**O5. Rebuttal to P1 (broken UX).** The UX is suboptimal, but "broken" overstates it. The pipeline does halt and provide clear error messages. Users can `--resume`. The current path is inconvenient but functional. Replacing it with an untested auto-remediation engine that silently modifies roadmap artifacts is a different kind of "broken" -- one where the user cannot easily verify what changed.

**O6. Rebuttal to P3 (dead code).** The code is not dead -- it is staged for activation. Many codebases have feature-flagged code awaiting enablement. The correct sequence is: (1) add integration tests, (2) opt-in flag for early adopters, (3) gather telemetry, (4) default ON. Skipping steps 1-3 is premature.

**O7. Rebuttal to P6 (cost control).** TurnLedger guards prevent unbounded cost, but the minimum cost (MIN_CONVERGENCE_BUDGET = 28 units) is still higher than a single-shot check. Users who always pass on first check (which does happen for well-written specs) pay a tax for convergence infrastructure that they did not need. An opt-in flag lets these users avoid the overhead.

**O8. Concession with counter-proposal.** The UX problem is real. Counter-proposal: add `--convergence` flag now (low risk), announce it in release notes, gather usage data for one release cycle, then evaluate defaulting ON with data. This is progressive rollout, not indefinite postponement.

---

### Round 2 Scoring Matrix

| Dimension | Proponent | Opponent | Delta from R1 |
|-----------|-----------|----------|---------------|
| User Experience | P1+P7: Strong | O5: Moderate (functional but bad) | Proponent extends lead |
| Code Readiness | P5: Moderate (tests are writable) | O6: Strong (process argument) | Opponent holds |
| Cost | P6: Strong (budget guards exist) | O7: Moderate (minimum overhead) | Narrows -- proponent gains |
| Risk | P8: Strong (escape hatch) | O3+O6: Strong (progressive rollout) | Even |
| Future Compat | P7: Strong (don't defer for maybe) | O4: Weakened | Proponent gains |
| Process | -- | O8: Strong (data-driven approach) | Opponent introduces new dimension |

**Round 2 Convergence**: 55% -- positions narrowing, both sides making concessions.

---

## Round 3: Final Arguments and Synthesis

### PROPONENT Final

**P9. The escape hatch resolves the risk concern.** With `--no-convergence`, any user who encounters issues can immediately fall back to the old behavior. This is standard practice for defaults: the default serves the majority case, the flag serves the exception. The majority case here is clear -- users hitting spec-fidelity failures 3-4 times.

**P10. The opponent's counter-proposal still leaves the broken default.** Under O8, every new user hits the broken single-shot path first, then must discover the `--convergence` flag exists, then opt in. The users who need convergence most (those with complex specs that fail spec-fidelity) are the least likely to know about an opt-in flag. Defaults should serve the common case.

**P11. Accepting the test requirement.** The proponent concedes that integration tests should be written before flipping the default. The complete proposal is: (1) write integration tests for `_run_convergence_spec_fidelity`, (2) flip default to True, (3) add `--no-convergence` escape hatch, (4) deprecation notice for the single-shot path.

### OPPONENT Final

**O9. Accepting the UX problem, disputing the timeline.** The opponent concedes P1 -- the UX is broken, not merely suboptimal. However, the correct fix is not to flip a default on untested code. The complete counter-proposal: (1) add `--convergence` flag in the next patch release (days, not weeks), (2) write integration tests, (3) announce opt-in in release notes, (4) after one release cycle with telemetry, flip default to ON with `--no-convergence`.

**O10. The real disagreement is about one release cycle.** Both sides agree convergence should eventually be the default. The disagreement is whether to skip the opt-in burn-in period. The opponent argues one release cycle of opt-in data is worth the delay. The proponent argues the broken UX is not worth one more release cycle of suffering.

**O11. Risk asymmetry.** If convergence-by-default works: users save 3-4 manual reruns. If it fails (silent corruption, budget exhaustion on edge cases, remediation introducing new errors): users have corrupted roadmap artifacts they may not notice. The downside risk (silent corruption) is worse than the upside gain (saved reruns), which argues for opt-in first.

---

### Round 3 Scoring Matrix

| Dimension | Proponent | Opponent | Final Assessment |
|-----------|-----------|----------|------------------|
| User Experience | P9-P10: Very Strong | O9: Concedes problem | Proponent wins dimension |
| Code Readiness | P11: Concedes test need | O9: Same position | Converged -- tests required first |
| Cost | P6: Resolved (guards + escape) | O7: Minor concern remaining | Mostly resolved |
| Risk | P9: Escape hatch | O11: Risk asymmetry (strong) | Opponent has edge |
| Process | P11: Compressed timeline | O9-O10: One cycle burn-in | Core remaining disagreement |
| Timeline | P10: Ship now + escape hatch | O10: One release cycle delay | Genuine tradeoff |

**Round 3 Convergence**: 72% -- agreement on destination, disagreement on timeline.

---

## Convergence Summary

| Point | Agreed? | Details |
|-------|---------|---------|
| UX is broken | YES | Both sides acknowledge 3-4 manual reruns is unacceptable |
| Convergence should eventually be default | YES | Opponent concedes in O9-O10 |
| Integration tests must come first | YES | Proponent concedes in P11 |
| `--no-convergence` escape hatch needed | YES | Both sides support |
| Single-shot path should eventually be deprecated | YES | Timeline differs |
| Skip opt-in burn-in period | NO | Core remaining disagreement |
| Risk asymmetry (silent corruption vs. saved reruns) | PARTIAL | Proponent argues escape hatch mitigates; opponent argues insufficient |

**Unresolved**: Whether one release cycle of opt-in data is worth the UX cost of leaving the broken default in place for that period.

---

## Judge's Verdict

**Winner: PROPONENT (default ON) -- with conditions.**

### Reasoning

**1. The UX harm is concrete and ongoing; the risk is theoretical and mitigable.**

The single-shot spec-fidelity path fails routinely, forcing 3-4 manual `--resume` cycles. This is not an edge case -- it is the common path for any non-trivial spec. Every day the broken default remains, users suffer a known, documented problem. The opponent's risk concern (silent corruption from convergence) is valid but theoretical: no evidence of corruption exists because the code has never run. The `--no-convergence` escape hatch provides an immediate fallback if problems emerge.

**2. The convergence engine has built-in safety mechanisms.**

The code is not a naive retry loop. It has: (a) budget guards that halt gracefully on exhaustion, (b) structural regression detection that aborts on quality decrease, (c) atomic snapshot/rollback per file during remediation, (d) semantic fluctuation logging that separates noise from signal. These are production-grade safety features, not prototype code.

**3. The test gap is a prerequisite, not a blocker to the decision.**

Both sides agree integration tests must be written. The question is what happens after the tests pass. The proponent's position (default ON after tests) is more aligned with the evidence: fully wired code, safety mechanisms, clear UX benefit.

**4. The opponent's progressive rollout is sound engineering but disproportionate here.**

Progressive rollout is the right default strategy for *new features*. Convergence is not a new feature -- it is a *fix for a broken workflow*. The appropriate analogy is not "feature flag rollout" but "bug fix deployment." You do not progressively roll out a bug fix behind a flag for one release cycle.

**5. The v5.xx argument is not actionable.**

Deferring because a future release might supersede is indefinite postponement. The v5.xx release has convergence fate listed as "open design decision," which means no decision has been made. Waiting for a non-decision is not a strategy.

### Conditions for Default ON

The verdict is conditional on the following being completed before the default is flipped:

1. **Integration tests**: Write tests for `_run_convergence_spec_fidelity()` covering: (a) happy path (convergence passes on run 1), (b) convergence after remediation (passes on run 2-3), (c) budget exhaustion halt, (d) structural regression abort, (e) semantic fluctuation logging.

2. **CLI flag**: Add `--no-convergence` flag to `commands.py` that sets `convergence_enabled=False`, overriding the new default.

3. **Logging**: Ensure convergence run count, budget consumption, and remediation actions are logged at INFO level so users can audit what happened.

4. **Release notes**: Document the default change, the `--no-convergence` escape hatch, and the rationale.

### Implementation Recommendation

```
# models.py change:
convergence_enabled: bool = True   # v3.xx: default ON (was False)

# commands.py addition:
@click.option("--no-convergence", is_flag=True, default=False,
              help="Disable convergence engine; use single-shot spec-fidelity check")

# Wire the flag:
config.convergence_enabled = not no_convergence
```

### What NOT to Do

- Do not delete the single-shot path yet. Keep it as the `--no-convergence` fallback for one release cycle, then evaluate deletion.
- Do not skip the integration tests. The verdict is conditional on them.
- Do not add `--convergence` as an opt-in flag. This perpetuates the broken default and guarantees the UX problem persists for users who do not read release notes.

---

*Debate conducted 2026-04-03. 3 rounds. Final convergence: 72%.*
