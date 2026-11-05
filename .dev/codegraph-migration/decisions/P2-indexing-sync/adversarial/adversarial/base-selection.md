# Base Selection

Variants: V1 = option-a (guidance only), V2 = option-b (SessionStart hook), V3 = option-c (global git template hooks).

## Quantitative Scoring (50% weight)

Source requirements (no formal IDs; taken from the decision statement): R1 new clones get an index automatically, R2 new worktrees do too, R3 existing/opened projects do too, R4 the index stays fresh, R5 smallest correct code, R6 states concretely what IronClaude ships (mechanism, opt-out, guidance).

| Metric | Weight | V1 | V2 | V3 | Computation |
|---|---|---|---|---|---|
| Requirement Coverage (RC) | 0.30 | 0.50 | 0.83 | 0.67 | V1: R4 R5 R6 = 3/6. V2: R1 R2 R3 R4 R6 = 5/6. V3: R1 R2 R4 R6 = 4/6 (R3 no: existing clones; R5 no). |
| Internal Consistency (IC) | 0.25 | 1.00 | 1.00 | 0.90 | V3: 1 contradiction (X-001) of ~10 claims. |
| Specificity Ratio (SR) | 0.15 | 0.88 | 0.93 | 0.82 | V1 7/8 ("docs page" unlocated). V2 14/15 ("seconds to minutes"). V3 9/11 ("unless backgrounded", "seconds to minutes"). |
| Dependency Completeness (DC) | 0.15 | 1.00 | 1.00 | 1.00 | All references (context.md, "rule from Option A") resolve inside the input set. |
| Section Coverage (SC) | 0.15 | 0.86 | 1.00 | 0.71 | No H2 headings in any variant; counted top-level blocks: 6 / 7 / 5. |
| **Quant score** | | **0.811** | **0.939** | **0.806** | |

## Qualitative Scoring (50% weight) — Additive Binary Rubric

CEV summary per criterion (MET = 1). Evidence quotes refer to the variant files.

### Completeness
| # | Criterion | V1 | V2 | V3 | Evidence |
|---|---|---|---|---|---|
| 1 | All explicit requirements | 0 | 1 | 0 | V1 "every new clone or worktree starts unindexed"; V3 "does nothing for existing clones"; V2 covers each checkout on first session |
| 2 | Edge/failure cases | 1 | 1 | 1 | V1 "forgets and falls back to grep"; V2 non-git, `$HOME`, two sessions; V3 `core.hooksPath`, lock |
| 3 | Dependencies | 1 | 1 | 1 | V1 watcher + Coder; V2 `command -v codegraph`, git; V3 template applies at clone/init |
| 4 | Success criteria | 0 | 1 | 1 | V2 "Each worktree gets its own index on the first session"; V3 "indexes on clone and worktree creation" |
| 5 | Out of scope stated | 1 | 0 | 0 | V1 "ownership goes entirely to the user and to Coder" |

### Correctness
| # | Criterion | V1 | V2 | V3 | Evidence |
|---|---|---|---|---|---|
| 1 | No factual errors | 1 | 1 | 0 | V2 DB path verified (`.codegraph/codegraph.db` in sandbox). V3 "Existing checkouts get nothing until re-cloned" is overstated: re-running `git init` applies templates (V3 advocate, git-init manual) |
| 2 | Feasible | 1 | 1 | 1 | V3 feasible if backgrounded, as it states |
| 3 | Terminology consistent | 1 | 1 | 1 | |
| 4 | No internal contradictions | 1 | 1 | 0 | X-001 |
| 5 | Claims supported | 1 | 1 | 1 | All defer to context.md |

### Structure
All three meet all 5 criteria: short options in the same shape (mechanism bullets, then strengths and weaknesses) that open with "Read `context.md` first" as the cross-reference. V1 5, V2 5, V3 5.

### Clarity
| # | Criterion | V1 | V2 | V3 | Evidence |
|---|---|---|---|---|---|
| 1 | Unambiguous | 1 | 0 | 0 | V2 log sentence garbled ("`nohup … >"$top/.codegraph-init.log" 2>&1 &` is avoided; log goes to …"); V3 "unless backgrounded" leaves the choice open |
| 2 | Concrete | 1 | 1 | 1 | |
| 3 | Clear purpose | 1 | 1 | 1 | |
| 4 | Terms defined | 1 | 1 | 1 | via context.md |
| 5 | Actionable | 1 | 1 | 1 | |

### Risk Coverage
| # | Criterion | V1 | V2 | V3 | Evidence |
|---|---|---|---|---|---|
| 1 | 3+ risks with probability and impact | 0 | 0 | 0 | none rate probability |
| 2 | Mitigation per risk | 0 | 0 | 0 | V2 mitigates 2 of 3 weaknesses (opt-out, fallback rule), not maintenance |
| 3 | Failure modes and recovery | 1 | 1 | 1 | the fallback rule in all three |
| 4 | External dependency failure | 1 | 1 | 1 | Coder; missing binary; husky/pre-commit |
| 5 | Monitoring | 0 | 1 | 0 | V2 log file |

### Invariant & Edge Case Coverage
| # | Criterion | V1 | V2 | V3 | Evidence |
|---|---|---|---|---|---|
| 1 | Boundary inputs | 0 | 1 | 0 | V2 non-git / `$HOME` / `/` |
| 2 | Cross-component state | 1 | 1 | 1 | V1 daemon owns the index; V2 nested vs parent index; V3 sync vs daemon lock |
| 3 | Guard gaps | 0 | 1 | 1 | V2 guards; V3 "only when unset" |
| 4 | Count divergence | 0 | 0 | 0 | not applicable |
| 5 | Interaction effects | 0 | 1 | 1 | V2 two sessions; V3 `core.hooksPath` collision |

### Qualitative Summary
| Dimension | V1 | V2 | V3 |
|---|---|---|---|
| Completeness | 3 | 4 | 3 |
| Correctness | 5 | 5 | 3 |
| Structure | 5 | 5 | 5 |
| Clarity | 5 | 4 | 4 |
| Risk | 2 | 3 | 2 |
| Invariant/Edge | 1 | 4 | 3 |
| **Total / 30** | **21 (0.700)** | **25 (0.833)** | **20 (0.667)** |

### Edge Case Floor Check
V1 1/5, V2 4/5, V3 3/5: all eligible (floor 1/5).

## Position-Bias Mitigation
Pass 1 order V1, V2, V3; Pass 2 order V3, V2, V1 (both by the orchestrator). One disagreement: V3 Correctness-2 (Pass 2 said NOT MET because the init cost lands in the foreground). Re-evaluated with both pieces of evidence. V3 states "unless backgrounded", so it is feasible within its stated constraint: final MET. Verdicts changed: 0.

## Combined Scoring
| Variant | Quant ×0.5 | Qual ×0.5 | Final |
|---|---|---|---|
| V1 | 0.406 | 0.350 | 0.756 |
| V2 | 0.470 | 0.417 | **0.886** |
| V3 | 0.403 | 0.333 | 0.736 |

Margin V2 over V1: 0.130 (above 5%). Tiebreaker: not applied. Debate points won: V2 7, V1 4, V3 0.

## Selected Base: Variant 2 (option-b, SessionStart hook)

### Selection Rationale
V2 has the highest score on both layers. It is the only variant that meets every coverage requirement without writing global state. All three advocates, including V1's and V3's, named it the better default to ship (debate C-001, C-003, C-007).

### Strengths to Preserve from Base
Fail-open hook with no stdout; the `command -v` gate; the env opt-out; the `git rev-parse --show-toplevel` guard with the `$HOME` and `/` skips; a fast path when the index exists; detached init; a log outside the checkout; registration in hooks.json, `_FRESHNESS_SCRIPTS` and the plugin mirror; per-worktree indexes.

### Strengths to Incorporate from Non-Base Variants
- V1 U-008: the never-sync rule (X-001), as exact guidance text.
- V1 U-007: the docs page, with the disk and memory cost and the `codegraph.json` excludes (A-005).
- V1 A-003 point: a failed init must not leave a DB that the fast path then trusts.
- V1 C-009: smallest code. Drop the `mkdir` lock (it goes stale) unless the probe shows concurrent inits corrupt the index.
- V2/V3 A-006 point: the fallback rule covers any codegraph tool error, not one phrase.
- V3 U-006: a documented opt-in `post-checkout` recipe (init only, backgrounded, `|| true`, never `sync`). The installer never writes global git config.
