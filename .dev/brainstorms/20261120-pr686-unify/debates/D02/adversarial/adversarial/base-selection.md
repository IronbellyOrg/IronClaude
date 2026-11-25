# Base Selection Report

Variant 1 = OURS (cron with one dispatcher). Variant 2 = CLAY (Orca automation with a no-agent precheck). Scope: this scores the two position papers as documents and as debate performers. It does not replace the owner's weighting rule, which VERDICT.md applies.

## Quantitative Scoring (50% weight)

Requirements used for requirement_coverage (the asks of the topic): (a) test the precheck claim against `waker.py` and the Orca CLI help or docs; (b) owner's R6 and R16; (c) Coder issue 515; (d) Clay's R4 and design 4.8; (e) the owner's "debated and rejected" statement; (f) cited sources; (g) unverified items marked. Counted by reading both papers.

| Metric | Weight | Variant 1 (OURS) | Variant 2 (CLAY) |
|--------|--------|------------------|------------------|
| requirement_coverage | 0.30 | 0.857 (6 of 7; no test against `waker.py`'s precheck claim, only its time-zone note) | 0.714 (5 of 7; no R6/R16 by name or one-dispatcher shape, no check of "debated and rejected") |
| internal_consistency | 0.25 | 1.000 (0 contradictions in about 20 claims) | 0.950 (1 in about 20: "nothing outside this repo changes" against "creating the automation is an owner step") |
| specificity_ratio | 0.15 | 0.950 (about 40 concrete statements, 2 vague) | 0.950 (about 38 concrete, 2 vague) |
| dependency_completeness | 0.15 | 1.000 (all internal references, such as OURS facts and R-numbers, resolve) | 1.000 |
| section_coverage | 0.15 | 1.000 (6 H2 sections) | 1.000 (6 H2 sections) |
| **quant_score** | | **0.950** | **0.894** |

Computation: V1 = 0.857x0.30 + 1.0x0.25 + 0.95x0.15 + 1.0x0.15 + 1.0x0.15 = 0.9496. V2 = 0.714x0.30 + 0.95x0.25 + 0.95x0.15 + 0.15 + 0.15 = 0.8943. The specificity counts are hand estimates, not a script count.

## Qualitative Scoring (50% weight) — Additive Binary Rubric

Two passes: Pass 1 (orchestrator, input order V1 then V2) and Pass 2 (independent evaluator agent, reverse order, full CEV rows in `rounds/qual-pass2.md`). Final verdicts below after reconciling disagreements. Evidence is a short quote or section reference; a MET without evidence would be NOT MET.

### Completeness (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence |
|-----------|----|----------|----|----------|
| C1 covers all explicit requirements | NOT MET | No test of the precheck claim against `waker.py`; names no R4 | NOT MET | No R6/R16 by name; no check of "debated and rejected" |
| C2 edge cases and failures | MET | Fact 6 (Run now click), fact 7 (crash looks like ok) | MET | Cost: Run now bypass; fact 5 exit 75 hidden |
| C3 dependencies and prerequisites | MET | Mechanism: Coder 515 package, daemon, entry | MET | Mechanism: `~/.aienv`; Cost: `--prompt` and `--provider` required |
| C4 success or completion criteria | NOT MET | No test for "cron works" beyond history | MET | Fact 7: 24-hour scheduled `--dry-run` shadow run before switch-on |
| C5 out of scope | NOT MET | none stated | NOT MET | none stated |
| **Subtotal** | **2/5** | | **3/5** | |

### Correctness (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence |
|-----------|----|----------|----|----------|
| K1 no factual errors | MET | R6/R16/R21, handoff doc, CLI help quotes match sources | MET | `SKILL.md:30`, `waker.py:1-2`, design 4.8 quotes match sources |
| K2 feasible | MET | Cron fires on time (R21); dependency stated | MET | Pattern already on master |
| K3 terminology consistent | MET | "dispatcher", "poll" used the same way | MET | "precheck", "poll", "waker" used the same way |
| K4 no internal contradictions | MET | Fact 1 and Risk are scoped apart | NOT MET | "Nothing outside this repo has to change" (fact 6) against Cost "Creating the automation is an owner step"; creating an automation changes Orca state outside the repo |
| K5 claims supported | MET | Each fact carries file:line | MET | Each fact carries file:line; inference marked UNVERIFIED |
| **Subtotal** | **5/5** | | **4/5** | |

### Structure (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence |
|-----------|----|----------|----|----------|
| T1 to T5 (order, depth, separation, navigation, conventions) | MET x5 | Claim, Mechanism, Cited facts, Cost, Risk, What OURS gets right; numbered facts with cross references | MET x5 | Same six sections; numbered facts with cross references |
| **Subtotal** | **5/5** | | **5/5** | |

### Clarity (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence |
|-----------|----|----------|----|----------|
| L1 unambiguous | MET | "the template" is named in the same sentence as Coder issue 515 (pass 2 said NOT MET; re-evaluated MET) | MET | Claim names the command and outcome exactly |
| L2 concrete | MET | Full cron line, dated firings | MET | Full precheck command shape, dated firings |
| L3 section purpose | MET | headings state their purpose | MET | same |
| L4 terms defined | MET | R21, R6/R16 glossed | MET | U6, N5, R4 glossed |
| L5 actionable steps | MET | "The runbook line must be fixed"; boot step per 515 | MET | Create `--disabled`, read next run, shadow run |
| **Subtotal** | **5/5** | | **5/5** | |

### Risk Coverage (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence |
|-----------|----|----------|----|----------|
| R1 three risks with probability and impact | NOT MET | two risks, no probability or impact | NOT MET | three unverified points, no probability or impact |
| R2 mitigation for each risk | NOT MET | only "must not lean on that sentence" | NOT MET | mitigation for U6 and U7 only; none for the documentation gap or the app-running question (pass 1 said MET; re-evaluated NOT MET because "each" is not met) |
| R3 failure modes and recovery | MET | boot step recreates the crontab; locked tick exits and next tick retries | NOT MET | failure modes named; no recovery step stated |
| R4 external dependencies | MET | Coder image change still open | MET | Orca app or server running is stated unknown |
| R5 monitoring or validation | MET | log file plus exit code | MET | `orca automations list`, `audit.jsonl`, shadow run |
| **Subtotal** | **3/5** | | **2/5** | |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence |
|-----------|----|----------|----|----------|
| I1 collections (zero, one, many) | MET | "discovers repos on every tick ... bound to one repo" (one against many) | NOT MET | only one automation and one poll discussed |
| I2 state interactions | MET | dispatcher lock and per-repo lock | MET | precheck exit versus poll's own `flock`, exit 75 hidden |
| I3 guard condition gaps | MET | Run now bypass; wrong exit code | MET | Run now bypass |
| I4 count divergence | NOT MET | the six-field cron line is a syntax point, not tick count, timeout or history cap (pass 2 said MET; re-evaluated NOT MET) | MET | 60-second precheck limit against the poll; `*/5` accepted |
| I5 interaction effects | MET | `flock -n` plus two locks; cron plus Orca at boot | MET | detached poll plus precheck plus lock |
| **Subtotal** | **4/5** | | **4/5** | |

### Qualitative Summary

| Dimension | V1 | V2 |
|-----------|----|----|
| Completeness | 2/5 | 3/5 |
| Correctness | 5/5 | 4/5 |
| Structure | 5/5 | 5/5 |
| Clarity | 5/5 | 5/5 |
| Risk Coverage | 3/5 | 2/5 |
| Invariant & Edge Case | 4/5 | 4/5 |
| **qual_score** | **24/30 = 0.800** | **23/30 = 0.767** |

### Edge Case Floor Check
Both variants score at least 1/5 on Invariant & Edge Case Coverage (4/5 each). Both eligible as base.

## Position-Bias Mitigation

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|-----------|---------|--------|--------|-----------|-------|
| K4 | V2 | NOT MET | MET | DISAGREE | NOT MET |
| L1 | V1 | MET | NOT MET | DISAGREE | MET |
| R2 | V2 | MET | NOT MET | DISAGREE | NOT MET |
| I4 | V1 | NOT MET | MET | DISAGREE | NOT MET |

All other 56 variant-criterion pairs agreed. Disagreements re-evaluated: 4. Final verdicts that changed one of the two passes: 4. Pass totals: Pass 1 V1 24, V2 23; Pass 2 V1 24, V2 24. Note that the orchestrator wrote Pass 1 after reading Pass 2's totals, which weakens independence; the four re-evaluations rely on the quoted text of each paper.

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate Tiebreaker |
|---------|---------------|--------------|-----------------|-------------------|
| 1 (OURS, cron) | 0.4748 | 0.4000 | **0.8748** | 3 points won |
| 2 (CLAY, automation) | 0.4472 | 0.3833 | **0.8305** | 5 points won |

**Margin**: 0.0443 absolute (4.4 percentage points), below the 0.05 threshold
**Tiebreaker applied**: Yes, level 1 (debate performance). Points won in the Step 2 scoring matrix: Variant 2 won C-001, C-002, C-003, X-001, X-002 (5); Variant 1 won C-004, C-007, C-010 (3); draws and unresolved points not counted. The 2-point gap of 18 diff points is 11 percentage points, outside the 5% band, so level 2 and 3 are not needed.

## Selected Base: Variant 2 (CLAY, Orca automation with a no-agent precheck)

### Selection Rationale
Variant 1 scores higher on the raw combined score (0.875 against 0.831), but the margin is under the 5-point threshold, so the protocol's tiebreaker decides, and Variant 2 won more diff points in the debate (5 against 3). The five points are the ones that correct the owner's written premise (C-001, X-001, X-002) and the dependency question (C-002, C-003). This selects the better-supported document base. It is not the decision: the owner's weighting rule (OURS wins unless CLAY shows a clear evidenced benefit) is applied in VERDICT.md, and the unresolved items (C-008, X-003, A-002) and the two blocking invariants (INV-023, INV-024) are carried into it.

### Strengths to Preserve from Base
1. Evidence that the precheck pattern is already on master and documented as VERIFIED (`SKILL.md:30`), with the exact command shape.
2. The plan to test unknowns (U6, U7, scheduled shadow run) before switch-on.
3. The point that the scheduler is part of a runtime the poll needs anyway.

### Strengths to Incorporate from Non-Base Variants
1. From Variant 1, Mechanism and fact 6: the Run now and `orca automations run` bypass starts a Claude session; cron has no such path (U-001, C-004, High).
2. From Variant 1, fact 2: tested cron facts on this host (R21 and the handoff doc), stated with the limit that the install path is untested (Round 2 concession).
3. From Variant 1, Cost bullet 2: the six-field FU-2 line is wrong for cron 3.0pl1 (U-004).
4. From Variant 1, Risk bullet 2: "debated and rejected" is not backed by the debate folder (U-005).
5. From the debate: write the verdict per command (A-001, INV-023) and state that zero setup is not decided by the scheduler (INV-024).
