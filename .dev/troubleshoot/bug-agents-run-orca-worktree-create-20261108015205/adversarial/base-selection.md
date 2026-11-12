# Base Selection

Evaluator: the orchestrating session (no separate scoring agent was spawned). Position-bias mitigation was run as two passes by the same evaluator (forward V1→V3, reverse V3→V1); that is weaker than independent judges and is recorded as a limitation.

## Quantitative Scoring (50% weight)

Source requirements (no formal IDs; topic-level from the troubleshoot context: doc-context.md restrictions + candidate-fixes.md facts):
r1 reaches all repos where creates happen (N12); r2 reaches running agents now (installed copy stale, N12); r3 close step cannot remove more than the seeded tab; r4 respects /sc:issue D2/FO-18 (no `--agent` on its create); r5 respects WC-13 (workers); r6 keeps the 12 pinned phrases; r7 keeps the Orca-only rule; r8 has a test that proves the text.

| Metric | Weight | V1 | V2 | V3 | Computation notes |
|---|---|---|---|---|---|
| Requirement coverage (RC) | 0.30 | 0.63 (5/8: r1,r2,r6,r7,r8) | 0.75 (6/8: r1,r3,r4,r6,r7,r8) | 0.75 (6/8: r2,r4,r5,r6,r7,r8) | V1 sends hand-offs to `--agent` without the /sc:issue/worker exemption (r4, r5 not met); V2 lacks reinstall (r2) and workers (r5); V3 lacks reach (r1) and safe close (r3) |
| Internal consistency (IC) | 0.25 | 1.00 (0/12) | 0.92 (1/12: X-003) | 0.90 (1/10: "CLAUDE.md only" vs a new test file) | |
| Specificity ratio (SR) | 0.15 | 0.92 | 0.90 | 0.92 | all name exact files, lines, commands; V2 has "if the agent misjudges" |
| Dependency completeness (DC) | 0.15 | 1.00 | 1.00 | 1.00 | all internal refs (N-rows, V-CLOSE, fix sections) resolve |
| Section coverage (SC) | 0.15 | 1.00 (6/6) | 1.00 | 1.00 | |
| **quant_score** | | **0.876** | **0.890** | **0.888** | (RC×0.30)+(IC×0.25)+(SR×0.15)+(DC×0.15)+(SC×0.15) |

## Qualitative Scoring (50% weight) — Additive Binary Rubric

CEV per criterion, abbreviated: verdict then evidence. MET = 1, NOT MET = 0.

### Completeness (5)
| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| 1 Covers explicit requirements (doc constraints) | NOT MET — hand-off `--agent` without /sc:issue/worker exemption | MET — no constraint violated; orca_worktree.py deferred | MET — exempts /sc:issue and workers |
| 2 Edge cases / failure scenarios | MET — Risks: setup/default tabs, `--all` reuse | MET — Risks: late seed, setup terminal | MET — Risks: `--all` after launch |
| 3 Dependencies / prerequisites | MET — sync-dev + `superclaude update` | MET — sync-dev, verify-sync | MET — "only on a branch with the fix" |
| 4 Success criteria | MET — pinned phrase test + V-CLOSE | MET — tests + V-JSON/V-CLOSE | MET — project test + V-CLOSE |
| 5 Out of scope stated | MET — "No project CLAUDE.md change" | MET — orca_worktree.py separate issue | MET — "CLAUDE.md only. No pinned-phrase changes" |

### Correctness (5)
| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| 1 No factual errors | MET | MET | MET |
| 2 Feasible | MET | MET | MET |
| 3 Consistent terminology | MET | MET | MET |
| 4 No internal contradictions | MET | NOT MET — X-003 | NOT MET — "CLAUDE.md only" vs new test file |
| 5 Claims supported | MET — N-rows, install_core.py | MET — startup.ts:187-214 | MET — provisioning.ts:189/:203 |

### Structure (5): all MET for all three (identical template, logical order, cross-references to N-rows). V1 5, V2 5, V3 5.

### Clarity (5)
| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| 1 Unambiguous | MET | MET | MET |
| 2 Concrete | MET | MET | MET |
| 3 Section purpose clear | MET | MET | MET |
| 4 Terms defined on first use | NOT MET — N1/V-CLOSE undefined | NOT MET — same | NOT MET — same |
| 5 Actionable next steps | MET | MET | MET |

### Risk Coverage (5)
| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| 1 ≥3 risks with probability+impact | NOT MET — 3 risks, no probability | NOT MET — 3 risks, no probability | NOT MET — 2 risks |
| 2 Mitigation per risk | NOT MET — setup race unmitigated | MET — late seed harmless; setup via create result / `--setup skip` | NOT MET — reach unmitigated |
| 3 Failure modes + recovery | NOT MET | MET — late seed → harmless incomplete | NOT MET |
| 4 External dependency failure | MET — reinstall dependency | MET — Orca registration timing | MET — branch dependency |
| 5 Monitoring/validation | MET — V-CLOSE | MET — V-JSON, V-CLOSE | MET — V-CLOSE |

### Invariant & Edge Case Coverage (5)
| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| 1 Collection boundaries (empty/single) | NOT MET | MET — "exactly one", zero-list case | NOT MET |
| 2 State interaction across components | MET — installed vs source copies | MET — setup provisioning | MET — /sc:issue, workers launch steps |
| 3 Guard condition gaps | MET — setup risk named | MET | MET — "`--all` ... only guard" |
| 4 Count divergence | NOT MET | MET — exactly one terminal | NOT MET |
| 5 Interaction effects | MET — launch then `--all` kills agent | MET — before any `agent launch` | MET — same |

### Qualitative Summary
| Dimension | V1 | V2 | V3 |
|---|---|---|---|
| Completeness | 4 | 5 | 5 |
| Correctness | 5 | 4 | 4 |
| Structure | 5 | 5 | 5 |
| Clarity | 4 | 4 | 4 |
| Risk Coverage | 2 | 4 | 2 |
| Invariant & Edge Case | 3 | 5 | 3 |
| **Total / 30** | **23 (0.767)** | **27 (0.900)** | **23 (0.767)** |

### Edge Case Floor Check
V1 3/5 eligible; V2 5/5 eligible; V3 3/5 eligible.

## Position-Bias Mitigation

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|---|---|---|---|---|---|
| Completeness 3 | V3 | NOT MET (no explicit prerequisite step) | MET (Risks names the branch prerequisite) | disagree | MET (re-evaluated: the branch dependency is stated) |
| Risk 2 | V2 | MET | MET | agree | MET |
| all others | all | agree | agree | agree | as tabled |
Disagreements found: 1; verdicts changed: 0 relative to pass 2.

## Combined Scoring

| Variant | Quant (×0.5) | Qual (×0.5) | Final | Rank |
|---|---|---|---|---|
| V2 | 0.445 | 0.450 | **0.895** | 1 |
| V3 | 0.444 | 0.383 | 0.828 | 2 |
| V1 | 0.438 | 0.383 | 0.822 | 3 |

Margin V2 over V3: 0.067 (> 0.05) → no tiebreaker.

## Selected Base: Variant 2 (fix-2, quality-engineer card)

**Selection rationale**: V2 already has the location the debate converged on (installed core copies plus a project bullet, C-001 unanimous), the strongest guards (C-003 unanimous, X-004 unanimous), and the only explicit deferral of orca_worktree.py (C-007 unanimous). Its defects are local: X-003 (self-contradicting test) and the missing reinstall step.

**Strengths to preserve**: core + README + project placement; "only a worktree you just created", "no setup script", "before any `agent launch`" guards; deferral of orca_worktree.py; running the three test files.

**Strengths to incorporate**:
- V1: `superclaude update` delivery step (C-005); hand-off → `worktree create --agent` (C-004).
- V1/V3: closing command `orca terminal close --worktree path:<path> --all` inside the guards, replacing list-and-handle (C-002, X-001 majority; V2 dissent recorded).
- V3: put the project step next to the example block :318-324 and exempt `/sc:issue` and supervised workers (U-006, U-007); project-section test (C-006).
- A-001 resolution: document that opening the worktree in the Orca UI re-seeds a shell (user-driven).
- Fix X-003: no `"--all" not in section` assertion.
