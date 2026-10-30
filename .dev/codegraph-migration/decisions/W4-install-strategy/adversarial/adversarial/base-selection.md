# Base Selection

Variants: V1 = Option A, V2 = Option B, V3 = Option C.

## Quantitative Scoring (50% weight)

The "source requirements" for RC are the 10 explicit asks of the decision brief and the evidence file:

- R1 install via `superclaude install`
- R2 update via `./update.sh`
- R3 Coder bake or no bake
- R4 version pin v1.6.2
- R5 integrity verification
- R6 MCP registration
- R7 guidance that survives update
- R8 telemetry off
- R9 non-Coder platforms
- R10 removal/uninstall

| Metric | Weight | V1 (A) | V2 (B) | V3 (C) | Computation notes |
|---|---|---|---|---|---|
| Requirement Coverage (RC) | 0.30 | 1.00 | 0.80 | 0.90 | A covers all 10. B does not mention R9 or R10. C does not mention R10. |
| Internal Consistency (IC) | 0.25 | 0.95 | 0.93 | 1.00 | A: keeping the upstream layout so `codegraph upgrade` works conflicts with "no self-update" (1/20). B: "upstream keeps config correct" conflicts with "re-runs keep fighting" (1/15). C: 0/14. |
| Specificity Ratio (SR) | 0.15 | 0.96 | 0.88 | 0.92 | Concrete vs vague counts: A 22/1 ("roughly"); B 14/2 ("a few", "if wanted later"); C 12/1 ("if both are built"). |
| Dependency Completeness (DC) | 0.15 | 1.00 | 1.00 | 1.00 | All internal refs resolve. A's `main.py:253-262` is off by one (the phase is at 254-262) but resolves. External refs excluded. |
| Section Coverage (SC) | 0.15 | 1.00 | 1.00 | 1.00 | 3 H2 sections each. |
| **quant_score** | | **0.982** | **0.905** | **0.958** | |

## Qualitative Scoring (50% weight) — Additive Binary Rubric

Final verdicts after dual-pass reconciliation (see Position-Bias Mitigation). M = MET, N = NOT MET.

### Completeness (5 criteria)
| # | Criterion | V1 | V2 | V3 | Evidence |
|---|---|---|---|---|---|
| 1 | Covers all explicit requirements | M | N | N | A covers R1-R10. B has no integrity check and no non-Coder or uninstall coverage. C has no non-Coder path unless A is also built. |
| 2 | Edge cases / failure scenarios | N | N | M | C: "If missing (non-Coder machine), it fails with a clear message, or falls back". A and B define no failure behaviour. |
| 3 | Dependencies / prerequisites | M | M | M | A: `claude mcp add-json`, optional `gh`. B: curl/sh, pinned tag. C: "Two repos must agree". |
| 4 | Success / completion criteria | N | N | M | C: "checks `codegraph --version` equals the IronClaude-expected version". |
| 5 | Out of scope stated | M | M | M | A: "Never runs `codegraph install`", "Does not install the `UserPromptSubmit` prompt hook". B: "does not bake". C: title "IronClaude only verifies and registers". |

### Correctness (5 criteria)
| # | Criterion | V1 | V2 | V3 | Evidence |
|---|---|---|---|---|---|
| 1 | No factual errors | M | M | M | Claims match eval §1-§5 and the repo files re-read this run. |
| 2 | Feasible | M | M | M | All mechanisms were demonstrated hands-on in eval §5. |
| 3 | Consistent terminology | M | M | M | — |
| 4 | No internal contradictions | N | N | M | A: upgrade-compatible layout vs no self-update (raised by the V2 advocate; A's advocate conceded). B: X-001 self-contradiction (conceded). |
| 5 | Claims supported | M | M | M | All cite eval sections or file:line. |

### Structure (5 criteria)
All three variants are MET on all 5: logical order, consistent hierarchy, separation into What/Strengths/Weaknesses, an evidence cross-reference line, and option-doc convention. V1 5, V2 5, V3 5.

### Clarity (5 criteria)
| # | Criterion | V1 | V2 | V3 | Evidence |
|---|---|---|---|---|---|
| 1 | Unambiguous language | N | N | N | A: "Optional extra check", "roughly". B: "a version check". C: "or falls back … (if both are built)". |
| 2 | Concrete | M | M | M | Exact commands and paths in all three. |
| 3 | Clear section purpose | M | M | M | — |
| 4 | Acronyms defined | N | N | N | "MCP" is never expanded. |
| 5 | Actionable next steps | M | M | M | A: exact `add-json` JSON. B: exact commands. C: Dockerfile steps. |

### Risk Coverage (5 criteria)
| # | Criterion | V1 | V2 | V3 | Evidence |
|---|---|---|---|---|---|
| 1 | ≥3 risks with probability/impact | N | N | N | Weaknesses are listed without probability. |
| 2 | Mitigation per risk | N | N | N | Mitigations are only partial in all three. |
| 3 | Failure modes and recovery | N | N | M | C defines missing-binary failure and fallback. |
| 4 | External dependency failure | N | M | M | B: "depends on upstream installer changes between pins". C: "existing workspaces only get a new codegraph after an image rebuild". |
| 5 | Monitoring/validation mechanism | M | N | M | A: SHA-256 plus unit tests. C: build-time hash plus version check. |

### Invariant & Edge Case Coverage (5 criteria)
| # | Criterion | V1 | V2 | V3 | Evidence |
|---|---|---|---|---|---|
| 1 | Collection boundaries | N | N | N | None handles an unsupported platform or an empty hash table. |
| 2 | State interactions across boundaries | M | M | M | A: guidance survives `--force`. B: block wiped by `install_core.py`. C: workspace version vs `./update.sh` expectation. |
| 3 | Guard condition gaps | M | M | M | A: hash guard. B: names the missing checksum guard. C: version equality guard. |
| 4 | Count divergence (exact vs range) | N | N | M | C: "equals". A and B do not say whether the version must match exactly or fall in a range. |
| 5 | Interaction effects | M | M | M | A: upstream installer editing config. B: ordering fight. C: `codegraph upgrade` vs a root-owned install. |

### Qualitative Summary
| Dimension | V1 | V2 | V3 |
|---|---|---|---|
| Completeness | 3 | 2 | 4 |
| Correctness | 4 | 4 | 5 |
| Structure | 5 | 5 | 5 |
| Clarity | 3 | 3 | 3 |
| Risk Coverage | 1 | 1 | 3 |
| Invariant & Edge Case | 3 | 3 | 4 |
| **Total / 30** | **19** | **18** | **24** |
| **qual_score** | **0.633** | **0.600** | **0.800** |

### Edge Case Floor Check
V1 3/5, V2 3/5, V3 4/5. All are ≥1/5, so all are eligible.

## Position-Bias Mitigation

Pass 1 ran in input order (V1, V2, V3). Pass 2 ran in reverse order (V3, V2, V1).

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|---|---|---|---|---|---|
| Clarity-1 | V1 | M | N | Disagree | N (re-evaluated: "roughly" and "Optional extra check … when" are hedges) |
| Completeness-5 | V3 | N | M | Disagree | M (re-evaluated: title states the scope limit) |
| IED-1 | V3 | M | N | Disagree | N (re-evaluated: a missing binary is a guard condition, already credited under IED-3, not a collection boundary) |
| IED-4 | V3 | M | M | Agree | M |
| Completeness-2 | V3 | M | N | Disagree | M (re-evaluated: fail-or-fallback is an explicit failure scenario) |
| Risk-3 | V3 | M | M | Agree | M |

- Disagreements found: 4
- Verdicts changed from Pass 1: 3 (V1 Clarity-1 M→N, V3 Completeness-5 N→M, V3 IED-1 M→N)
- All other criterion-variant pairs agreed in both passes.

Note: totals after re-evaluation are V1 19/30 (Pass 1: 20), V2 18/30 (unchanged), V3 24/30 (Pass 1: 24, because its two changes cancel out).

## Combined Scoring
| Variant | quant × 0.50 | qual × 0.50 | Final | Rank |
|---|---|---|---|---|
| V1 (A) | 0.491 | 0.317 | **0.808** | 2 |
| V2 (B) | 0.452 | 0.300 | **0.752** | 3 |
| V3 (C) | 0.479 | 0.400 | **0.879** | 1 |

- Margin V3 over V1: 0.071 (7.1%). That is outside the 5% band, so no tiebreaker applies.
- Debate-points context: V1 won 13 points and V3 won 5. The debate favoured A's mechanisms, while the rubric favoured C's decision shape (detect, verify version, register, defined failure path). The merge resolves this by putting A's mechanisms into C's shape.

## Selected Base: Variant 3 (Option C, original)

**Selection rationale.** C is the only variant with an explicit gate (`codegraph --version` must equal the IronClaude pin), a defined failure and fallback path, and a named external-dependency risk (two repos, stale workspaces). All three advocates independently converged on exactly that shape: detect, else verified download, then register. C scores highest on Correctness (no internal contradiction), Risk Coverage and Invariant coverage.

**Strengths to preserve (from C).**
- The exact version-equality gate (C-012, U-010).
- The Coder image bakes a root-owned `/usr/local/bin/codegraph` with a build-time SHA-256 check (C-007, C-009).
- Guidance in `src/superclaude/core/CLAUDE.md`, and IronClaude-owned `claude mcp add-json` registration (C-003, C-004).
- Offline new workspaces with no per-home copy (U-008), and a binary swap only at restart for baked installs (A-004 argument).

**Strengths to incorporate.**
- From V1 (A):
  - The verified download becomes the required fallback, not an "if both are built" option (C-001, C-010).
  - IronClaude source holds the single pin and the 4-platform hash table, and the image consumes the same values (C-002, C-008, X-002).
  - MCP `env` gets `CODEGRAPH_TELEMETRY=0` and `CODEGRAPH_NO_UPDATE_CHECK=1` (C-006, U-002).
  - No prompt hook, and never run `codegraph install` or `install.sh` (C-005, X-001, U-005).
  - Receipt and removal for the user-installed copy (C-011).
  - Upstream-compatible `~/.codegraph/versions/<tag>` layout (U-003).
  - Unit-tested single bump point (U-004).
- From V2 (B):
  - The `codegraph install --print-config claude` drift check, a no-write command, used as a test-time comparison.
  - The daemon-before-prune hazard of `install.sh` (A-004).
- From the debate (shared assumptions):
  - Register the absolute path of the binary that passed the gate (A-003).
  - Reuse the existing Claude-readiness guard (A-002).
  - Handle running daemons on a user-copy swap (A-004).
  - Name per-worktree `codegraph init` as a separate follow-up decision (A-001).
