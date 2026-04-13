---
base_variant: "roadmap-opus-architect"
variant_scores: "A:82 B:68"
---

## Scoring Criteria

Derived from the debate's convergence assessment and the task's nature (mechanical decomposition with precision requirements):

1. **Accuracy of Effort Estimation** (15%) — Does the timeline match the mechanical nature of the work?
2. **Phase Sequencing Correctness** (15%) — Are tasks ordered to respect true dependencies?
3. **Actionability & Specificity** (20%) — Can an implementer execute without interpretation?
4. **Verification Rigor** (15%) — Are success criteria automatable and complete?
5. **Integration Point Documentation** (15%) — Are wiring mechanisms explicit and traceable?
6. **Frontmatter & Machine-Readability** (10%) — Does metadata support tooling?
7. **Risk Management** (10%) — Are mitigations concrete and phase-linked?

## Per-Criterion Scores

| Criterion | Wt | Variant A (Opus) | Variant B (Haiku) | Rationale |
|---|---|---|---|---|
| Effort Estimation | 15% | **9/10** | 5/10 | Debate resolved: hours-scale correct for copy-paste-verify work. Haiku's 3.5–4.5 days calibrated for multi-person team with formal gates — not inherent complexity. |
| Phase Sequencing | 15% | **9/10** | 7/10 | Opus correctly places B05/B30 merge in Phase 3 (SKILL.md-internal operation). Haiku places it in Phase 1, which the debate ruled incorrect — no refs/ file references that table. |
| Actionability | 20% | **9/10** | 6/10 | Opus provides exact line ranges (e.g., "B14–B21, lines 553–967"), specific file counts ("exactly 6 path changes"), grep commands, and parallelism guidance (2.1–2.3 parallel, 2.4 sequential). Haiku uses requirement IDs but lacks line-level precision and parallelism analysis. |
| Verification Rigor | 15% | **9/10** | 7/10 | Opus provides a 12-criterion validation table with exact check methods and pass conditions. Haiku has a requirement-level validation matrix but less automatable — more prose, fewer commands. |
| Integration Points | 15% | **8/10** | 8/10 | Both document integration points well. Opus adds the BUILD_REQUEST dispatch table (valuable). Haiku adds IP-3 (fidelity index as integration point) — recognized by debate as a genuine addition. |
| Frontmatter | 10% | **9/10** | 5/10 | Opus has complete machine-readable frontmatter (phases, total_tasks, estimated_effort, generator). Haiku has minimal frontmatter (3 fields). |
| Risk Management | 10% | 7/10 | **8/10** | Both have identical risk inventories. Haiku adds risk burn-down checkpoints (risks retired per phase) — debate endorsed this as genuine value-add. |

## Overall Scores

| Variant | Weighted Score | Justification |
|---|---|---|
| **A (Opus)** | **82/100** | Superior on 5 of 7 criteria. Provides implementer-ready precision: line ranges, parallelism analysis, automatable 12-criterion table, complete frontmatter. Timeline is realistic per debate consensus. |
| **B (Haiku)** | **68/100** | Solid structure but less actionable. Inflated timeline, incorrect B05/B30 phase placement, missing parallelism guidance, sparse frontmatter. Contributes risk burn-down checkpoints, IP-3, and evidence artifact naming. |

## Base Variant Selection Rationale

**Opus is the base.** The debate resolved 7 divergences: 6 in favor of Opus (timeline, B05/B30 phase, staffing, parallelism, open question resolution, frontmatter), 3 items adopted from Haiku (risk burn-down, evidence artifacts, IP-3). Opus is closer to the final desired output — fewer modifications needed to reach the merged roadmap.

## Specific Improvements to Incorporate from Haiku

1. **Risk burn-down checkpoints** — Add to each phase's exit criteria section:
   - Phase 2 exit: "Risks 1, 5, 6 largely retired"
   - Phase 3 exit: "Risks 2, 3 retired"
   - Phase 4 exit: "Risks 4, 7 retired"

2. **IP-3: Fidelity index as integration point** — Add to Phase 2's integration point registry:
   - Named Artifact: `.dev/releases/backlog/prd-skill-refactor/fidelity-index.md`
   - Purpose: Source line ranges ↔ destination files for every moved/retained block
   - Owning Phase: Phase 1 (verified), consumed by Phase 2/3/4

3. **Explicit evidence artifact names** — Add to Phase 4, task 4.1 or as a new sub-section:
   - Fidelity index with verified block mappings
   - Diff logs per moved block family
   - Grep outputs for stale refs and A.7 declarations
   - E2E execution transcript and output structure comparison

4. **OQ-1 flag** — While adopting Opus's inline recommendation (500-line hard ceiling, 2,000-token soft target), add a note: "This is an assumption — confirm with spec author if challenged during review."
