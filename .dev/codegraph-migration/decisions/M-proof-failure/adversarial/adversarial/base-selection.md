# Base Selection (M-proof-failure)

Variants: V1 = option A (draft PR with a label), V2 = option B (issue only), V3 = option C (split by failure class).

Source requirements used for coverage (no formal IDs in the source, so topic matching): R1 handle class 1 integrity failures; R2 handle class 2 behaviour failures; R3 never put or merge unverified bytes; R4 give a person a next action; R5 idempotency across daily runs; R6 state the number of code paths to test; R7 class 3 infrastructure case (named in `context.md`).

## Quantitative Scoring (50% weight)

| Metric | Weight | V1 (A) | V2 (B) | V3 (C) | Computation notes |
|---|---|---|---|---|---|
| Requirement coverage (RC) | 0.30 | 4/7 = 0.571 | 5/7 = 0.714 | 6/7 = 0.857 | A: R1-R4. B: R1-R5. C: R1-R4, R6 ("three paths to test"), R7. Only B covers R5; only C covers R6 and R7. |
| Internal consistency (IC) | 0.25 | 1 - 1/6 = 0.833 | 1 - 0/6 = 1.000 | 1 - 1/9 = 0.889 | Reuses Step 1: X-001 counted against A, X-003 against C. |
| Specificity ratio (SR) | 0.15 | 6/7 = 0.857 | 7/7 = 1.000 | 10/10 = 1.000 | A's vague item: "looks like routine work" and the "..." title placeholder. |
| Dependency completeness (DC) | 0.15 | 1.000 | 1.000 | 1.000 | No internal cross-references in any card; external references (Coder, context classes) excluded. |
| Section coverage (SC) | 0.15 | 4/5 = 0.800 | 3/5 = 0.600 | 5/5 = 1.000 | Cards have no H2 sections; top-level bullets used as sections (A 4, B 3, C 5). |
| **Quant score** | | **0.778** | **0.854** | **0.929** | `RC*0.30 + IC*0.25 + SR*0.15 + DC*0.15 + SC*0.15` |

## Qualitative Scoring (50% weight): Additive Binary Rubric

Pass 1 (input order V1, V2, V3) was run by the orchestrator. Pass 2 (reverse order V3, V2, V1) was run by an independent evaluator agent (`rubric-pass2-reverse.md`, which holds the full CEV tables with quotes). The final verdicts below follow the disagreement resolution in the position-bias section.

### Completeness (5)

| Criterion | V1 | V2 | V3 | Evidence (final) |
|---|---|---|---|---|
| 1 all explicit requirements | 0 | 0 | 0 | A and C omit R5; B omits R6 and R7. |
| 2 edge cases and failure scenarios | 0 | 1 | 1 | B: "Open (or comment on, idempotently by title)". C: three classes including infra. A: none beyond the two classes. |
| 3 dependencies and prerequisites | 0 | 0 | 0 | No card says the label must be created or which token permissions are needed. |
| 4 success or completion criteria | 0 | 0 | 0 | None states when a failure artifact is resolved. |
| 5 out of scope stated | 0 | 0 | 0 | "No branch, no PR" (B) and "no issue" (C) are design choices, not scope statements. |

### Correctness (5)

| Criterion | V1 | V2 | V3 | Evidence (final) |
|---|---|---|---|---|
| 1 no factual errors | 1 | 1 | 1 | "proven in Coder", "issues notify the owner", "as Coder does" all match `context.md`. |
| 2 feasible | 1 | 1 | 1 | Every step uses `gh` actions the repo allows (`can_approve_pull_request_reviews: true`). |
| 3 terminology consistent | 1 | 1 | 1 | Class names used as in `context.md`. |
| 4 no internal contradictions | 1 | 1 | 1 | A states its trade-off honestly (X-001 is a tension, not a contradiction); C's X-003 is an ambiguity, scored under Clarity 1. |
| 5 claims supported by rationale | 1 | 1 | 1 | Each card has a rationale line. |

### Structure (5)

| Criterion | V1 | V2 | V3 | Evidence (final) |
|---|---|---|---|---|
| 1 logical ordering | 1 | 1 | 1 | Rule, rationale, cost. |
| 2 consistent hierarchy | 1 | 1 | 1 | One H1, flat bullets. |
| 3 separation of concerns | 1 | 1 | 1 | Rule bullets separate from rationale and cost. |
| 4 navigation aids or cross-references | 0 | 0 | 0 | References point outside the card only. |
| 5 artifact conventions | 1 | 1 | 1 | Standard option card. |

### Clarity (5)

| Criterion | V1 | V2 | V3 | Evidence (final) |
|---|---|---|---|---|
| 1 unambiguous | 0 | 1 | 0 | A: title "... [proof failed]" is a placeholder. C: one event (truncated download, attestation during outage) fits both the integrity and the infra rule; draft PR title missing. |
| 2 concrete actions | 1 | 1 | 1 | All name the artifact, title and contents. |
| 3 clear purpose | 1 | 1 | 1 | |
| 4 terms as in context | 1 | 1 | 1 | |
| 5 actionable next step | 0 | 1 | 1 | B: "the commands to reproduce locally". C: "so a person can push a fix (for example an `MCP_TOOLS` or entry change)". A names no next step for the reader. |

### Risk Coverage (5)

| Criterion | V1 | V2 | V3 | Evidence (final) |
|---|---|---|---|---|
| 1 at least 3 risks with probability and impact | 0 | 0 | 0 | No card rates probability or impact. |
| 2 mitigation per risk | 0 | 0 | 0 | |
| 3 failure modes and recovery | 0 | 1 | 1 | B: reproduce locally. C: retries next schedule; push a fix onto the draft. |
| 4 external dependency failure | 0 | 0 | 1 | C: "GitHub API or download unavailable" handled. |
| 5 monitoring or detection | 0 | 1 | 0 | B: "issues notify the owner". C's infra signal is a step summary, and "Nobody watches IronClaude Actions run summaries" (`context.md`). |

### Invariant and Edge Case Coverage (5)

| Criterion | V1 | V2 | V3 | Evidence (final) |
|---|---|---|---|---|
| 1 collection boundaries | 0 | 1 | 0 | B: zero versus one existing issue ("open (or comment on) one issue"). |
| 2 state across runs | 0 | 1 | 0 | B: "idempotently by title". |
| 3 guard condition gaps | 1 | 1 | 1 | All three name the unverified-bytes guard: A as its own gap ("pin points at unverified bytes"), B ("nothing mergeable ... from failed or unverified bytes"), C ("never put unverified hashes on a branch"). |
| 4 count divergence | 0 | 0 | 0 | |
| 5 interaction effects | 0 | 0 | 0 | |

### Qualitative Summary

| Dimension | V1 (A) | V2 (B) | V3 (C) |
|---|---|---|---|
| Completeness | 0 | 1 | 1 |
| Correctness | 5 | 5 | 5 |
| Structure | 4 | 4 | 4 |
| Clarity | 3 | 5 | 4 |
| Risk coverage | 0 | 2 | 2 |
| Invariant and edge cases | 1 | 3 | 1 |
| **Total** | **13/30 = 0.433** | **20/30 = 0.667** | **17/30 = 0.567** |

### Edge Case Floor Check

Threshold 1/5 on Invariant and Edge Case Coverage. V1 = 1, V2 = 3, V3 = 1. All three are eligible as base.

## Position-Bias Mitigation

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final | Reason |
|---|---|---|---|---|---|---|
| Corr4 | V1 | NOT MET | MET | No | MET | The cost line states the trade-off; nothing in A asserts the opposite. |
| Corr4 | V3 | NOT MET | MET | No | MET | X-003 is an undefined boundary, not two opposite claims; penalised under Clar1 instead. |
| Str4 | V1 | MET | NOT MET | No | NOT MET | "class 1" and "Coder" are external references, which the rubric excludes. |
| Str4 | V3 | MET | NOT MET | No | NOT MET | Same reason. |
| Comp5 | V2 | MET | NOT MET | No | NOT MET | "No branch, no PR" is a design choice, not an out-of-scope statement. |
| Comp5 | V3 | MET | NOT MET | No | NOT MET | Same reason. |
| Risk1 | V3 | MET | NOT MET | No | NOT MET | C names risks but rates none for probability or impact. |
| Risk5 | V3 | MET | NOT MET | No | NOT MET | Its only detection signal is a step summary nobody watches (`context.md`). |
| Inv3 | V1 | MET | NOT MET | No | MET | A's cost names the missing guard explicitly. |
| Inv3 | V2 | MET | NOT MET | No | MET | B's rationale states the guard. |
| Inv3 | V3 | MET | NOT MET | No | MET | C states the guard and its reason (possible tampering). |

- Disagreements found: 11 criterion-variant pairs
- Final verdicts that differ from pass 2: 3 (Inv3 for all three variants); final verdicts that differ from pass 1: 8 (Corr4 x2, Str4 x2, Comp5 x2, Risk1, Risk5)
- Pass totals before resolution: pass 1 V1 13, V2 21, V3 20; pass 2 V1 12, V2 19, V3 16. Final: V1 13, V2 20, V3 17.

Note: the quantitative IC metric keeps the Step 1 contradiction counts (X-001 against A, X-003 against C) because that layer is deterministic and reuses Step 1. The qualitative Corr4 re-evaluation judged them a tension and an ambiguity. The difference is recorded here, not reconciled.

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | Combined | Debate points won |
|---|---|---|---|---|
| V2 (B) | 0.854 -> 0.427 | 0.667 -> 0.333 | **0.760** | 5 |
| V3 (C) | 0.929 -> 0.465 | 0.567 -> 0.283 | **0.748** | 9 |
| V1 (A) | 0.778 -> 0.389 | 0.433 -> 0.217 | **0.606** | 2 |

- Margin between V2 and V3: 0.012, inside the 0.05 tie band.
- Tiebreaker applied: Yes, level 1 (debate performance). V3 won 9 diff points, V2 won 5 (`debate-transcript.md`, scoring matrix). Level 2 (correctness count) would tie at 5 versus 5.

## Selected Base: Variant 3 (option C, split by failure class; advocate default:qa)

### Selection rationale

All three advocates, including the A and B advocates, chose C's split as the shape of the rule (S-001 unanimous, 95%). It is the only variant that satisfies both "no unverified bytes on a branch" and "a diff a person can push a fix onto". The fact behind this is `install_codegraph.py:328-330`: the installer trusts the pinned table and nothing else, and a merged pin reaches every Coder workspace. B scored higher on the rubric because its card is more complete about re-runs and notification. Those are additions to C, not reasons to drop a draft PR for behaviour failures, which B's own advocate conceded.

### Strengths to preserve from the base (V3)

- Integrity failure: issue only, no branch, no PR.
- Behaviour failure: bump branch plus draft PR labelled `needs-codegraph-proof`, so a person can push a fix.
- An explicit infrastructure path.
- Distinct integrity issue title.

### Strengths to incorporate from non-base variants

- From V2: idempotency (C-004, U-002); run URL and reproduce commands in every artifact (C-005, U-001); the issue as the notification channel a person actually reads (A-006 reasoning).
- From V1: the "[proof failed]" marker in the draft PR title (S-002, U-005); branch-name key for PRs (V1 advocate).
- From the debate: fail-closed classifier (X-003, A-001); infra escalation (X-002, C-003); never push to an existing branch (A-002, N-001); supersede and later-pass rules (A-003, A-004, N-002, N-003, N-007, N-008); label created idempotently and applied non-fatally, explicit permissions (A-005); owner assigned (A-006, N-004).
