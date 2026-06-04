# Refactor Plan — Merged QA Architecture (V3 base + V1/V2 transfers + INV-006 resolution)

## Overview

- **Base variant**: V3 (/sc:task tier-classified executor) — score 0.845
- **Incorporated variants**: V1 (high-value coverage transfers) + V2 (high-value protocol transfers)
- **Change count**: 8 incorporations + 3 architectural additions
- **Risk**: Medium overall — composition pattern, not a from-scratch design
- **Convergence-block resolution**: 1 architectural addition (sc:reflect-post integration) addresses INV-006

---

## Planned Changes

### Change #1 — Adopt V1's cross-phase post-completion validation (HIGH)

- **Source variant and section**: V1 §2 Layer 2 (Post-Completion 2-Step Validation)
- **Target location in base**: V3 §4 Verification Phase — new "Post-Task Cross-Cutting Validation" subsection
- **Rationale (citing debate evidence)**: Debate scoring matrix C-004 (cross-phase consistency): V1 won 85% on this unique capability. V3's per-task isolation cannot see orphaned-output / missing-output issues that only emerge at multi-task or multi-phase compositions. V1's contribution U-001 fills V3's documented blind spot.
- **Integration approach**: After STRICT-tier sub-agent verification completes for the final task in a coupled sequence (where "coupled" = tasks share a deliverable file), run rf-qa structural validation across the sequence's outputs.
- **Risk level**: Low — additive; does not modify V3's existing verification path

### Change #2 — Adopt V1's 15-item operational checklist as STRICT-tier depth (HIGH)

- **Source variant and section**: V1 §2 Layer 2 Step 2b (15-item rf-qa-qualitative checklist)
- **Target location in base**: V3 §4 STRICT tier definition — extend quality-engineer sub-agent prompt to apply the 15-item checklist
- **Rationale**: Debate scoring matrix U-002. V3's STRICT-tier 3-5K token budget is currently spent on a generic quality-engineer verification; spending it on V1's 15-item checklist (gate dry-run, runtime failure path trace, completion scope honesty, ambient dep completeness, etc.) is strictly more behavioral and grounded.
- **Integration approach**: Replace quality-engineer's open-ended prompt with the 15-item checklist; preserve adversarial-stance framing.
- **Risk level**: Low — refines existing STRICT-tier behavior; no new gates added

### Change #3 — Adopt V2's DNSP synthetic-finding protocol for STRICT-tier partition failures (HIGH)

- **Source variant and section**: V2 §2 Layer 1 (A.8 DNSP Synthetic Finding Protocol)
- **Target location in base**: V3 §4 STRICT-tier verification — handle the case where quality-engineer sub-agent partition (when partitioned across >6 output files) fails to complete
- **Rationale**: Debate scoring matrix C-005 (partition failure): V2 won 92%. V3 currently has no formal handling for QA-agent crashes; V2's DNSP is the only formal contract.
- **Integration approach**: Adopt the byte-exact emission contract (severity=HIGH non-overridable, source="synthetic-dnsp", dedup_key 2-tuple with closed-vocabulary second element, found_n_times counter). Apply at STRICT-tier partition spawns.
- **Risk level**: Low — defensive addition; only fires on partition failure

### Change #4 — Adopt V2's 5 Adversarial Axes including AX-5 invented-content as STRICT-tier hallucination defense (HIGH)

- **Source variant and section**: V2 §2 Layer 3 (5 Adversarial Axes PR-07)
- **Target location in base**: V3 §4 STRICT-tier sub-agent prompt — extend with the 5 Adversarial Axes
- **Rationale**: Debate scoring matrix X-004 (hallucination protection): V2 won 88% with the only explicit defense. INV-002 (HIGH partially-addressed by V2 only) reinforces the need.
- **Integration approach**: STRICT-tier sub-agent must emit findings with one of `{AX-1 drift, AX-2 contradictions, AX-3 omissions, AX-4 weakened-criteria, AX-5 invented-content, none}` per finding; FORBIDDEN to use N/A in the Axis column.
- **Risk level**: Low — additive structure; no behavioral change unless invented-content is detected

### Change #5 — Adopt V2's anti-inflation rule for forensic remediation reports (MEDIUM)

- **Source variant and section**: V2 §2 Layer 3 (anti-inflation rule)
- **Target location in base**: V3 §3.5 TFEP Step 4 (Consume Forensic Results) — when forensic returns a remediation plan, require the executor's Self-Audit to list (a) which forensic verdicts it relied on AND (b) ≥1 semantic check where forensic verdict was insufficient and executor's own tool work was required.
- **Rationale**: Prevents Self-Audit gaming where the executor rubber-stamps the forensic remediation plan without semantic verification.
- **Integration approach**: Add Self-Audit section to TFEP incident report template.
- **Risk level**: Low — process addition; no execution-path change

### Change #6 — Adopt V2's DM-005 Phase Contract pattern for forensic-to-remediation handoff (MEDIUM)

- **Source variant and section**: V2 §2 Layer 3 (DM-005 Phase Contract)
- **Target location in base**: V3 §3.5 TFEP Step 4-5 (Consume Forensic Results → Tasklist Insertion)
- **Rationale**: V3's forensic-to-remediation handoff currently uses an unversioned wire (tasklist_insertion_path). Adopting DM-005's schema_version 1.0.0 frozen wire ABI with INV-002 freshness re-extract prevents stale-verdict carry-over across TFEP cycles.
- **Integration approach**: Wrap forensic return contract in a versioned schema; on TFEP cycle re-entry, re-extract the latest forensic verdict.
- **Risk level**: Low — wire-shape contract; no semantic change

### Change #7 — Tighten V3's tier-routed SKIP criteria (MEDIUM)

- **Source variant and section**: V1 §3 Architectural Invariants (mandatory phase-gate floor) + INV-005 (interaction effects)
- **Target location in base**: V3 §2 Tier Selection Algorithm
- **Rationale**: Debate scoring matrix X-002 (verification floor): V1 won 70%. V3's LIGHT/EXEMPT skip allows under-validation. New rule: ANY task that touches a tested module (presence of `tests/test_<module>.py` or equivalent) triggers minimum STANDARD-tier verification regardless of computed tier.
- **Integration approach**: Add Critical Path Override extension: detect test files for the modules being touched; if present, override LIGHT/EXEMPT → STANDARD.
- **Risk level**: Medium — modifies tier-routing behavior; could increase verification cost on previously-LIGHT tasks

### Change #8 — Document the V1+V3 composition pattern explicitly (MEDIUM)

- **Source variant and section**: INV-005 (interaction_effects UNADDRESSED)
- **Target location in base**: V3 new §8 Composition with Other QA Architectures
- **Rationale**: INV-005 (MEDIUM UNADDRESSED): V1's phase-gate + V3's TFEP interaction is undefined. When `/task` executes individual task items and one item is delegated to `/sc:task`, the interaction MUST be defined.
- **Integration approach**: Add §8 defining (a) V3's TFEP fires INSIDE V1's phase boundary on a per-item basis; (b) V1's phase-gate runs AFTER all V3 TFEP cycles complete for items in the phase; (c) cross-phase post-completion (V1 Layer 2) runs AFTER V3's final-task TFEP.
- **Risk level**: Low — documentation; no execution change

### Change #9 (ARCHITECTURAL ADDITION — resolves INV-006) — Integrate sc:reflect --mode post as out-of-context independent verifier (CRITICAL)

- **Source**: INV-006 convergence-blocker resolution + memory `feedback_sc_reflect_vs_inline_rfqa.md` + SprintRunReflect brainstorm
- **Target location in base**: V3 new §9 Out-of-Context Verification Layer
- **Rationale**: INV-006 sufficiency_challenge (HIGH UNADDRESSED across ALL 3 variants) BLOCKS convergence. Empirically demonstrated by R0 PR #112: inline rf-qa's fix passed inline-rf-qa's surface signal but missed the underlying defect that `/sc:reflect --mode post` caught. None of the three variants has a structural mechanism for self-confirmation-bias defense.
- **Integration approach**: After every STRICT-tier sub-agent verification (and after every V1 phase-gate completion when V1 is composed), spawn `/sc:reflect --mode post --depth deep` against the QA-resolved outputs. The reflect agent operates in a DIFFERENT context window than the verifier — providing the calibrator-disjoint-set property the three variants individually lack. Reflect's verdict either confirms the QA-resolved state or surfaces a blindspot the inline verifier missed.
- **Risk level**: Medium — new dependency on sc:reflect availability; adds ~10-30K tokens per STRICT-tier task. Mitigated by tier routing (only fires on STRICT) and by the empirical evidence (R0 PR #112) that the blindspots caught are real and high-impact.

### Change #10 (ARCHITECTURAL ADDITION) — Define third QA-finding state: needs-human-adjudication (MEDIUM)

- **Source**: INV-001 (UNADDRESSED across all 3)
- **Target location in base**: V3 §4 Verification Phase output schema
- **Rationale**: All three variants assume fix-or-flag binary is exhaustive. Real QA findings are sometimes genuinely ambiguous (e.g., a finding flagged by AX-5 invented-content might be a hallucination OR a genuine correct citation the verifier didn't recognize).
- **Integration approach**: Add `verdict: NEEDS_HUMAN_ADJUDICATION` to the QA return-contract schema. Findings with this verdict are surfaced to the user without auto-fix and without HALT.
- **Risk level**: Low — additive return-state; no execution path change for PASS / FAIL findings

### Change #11 (ARCHITECTURAL ADDITION) — Composition-safety check for /task + /sc:task interaction (LOW)

- **Source**: INV-005 (UNADDRESSED, MEDIUM)
- **Target location**: Both V1 §4 and V3 §2 — add interaction-safety detection
- **Rationale**: When a V1 /task execution internally delegates an item to /sc:task, the QA architectures compose. The interaction must be detected and the right behavior chosen (run /sc:task's TFEP inside /task's phase, then run /task's phase-gate on the union of outputs).
- **Integration approach**: Detect at delegation time; assert composition order.
- **Risk level**: Low — defensive check

---

## Changes NOT Being Made (Rejected Alternatives)

### Rejected — Adopt V1's fix_authorization: true model

- **Diff point**: X-001 (fix authority)
- **V1 approach proposed**: Allow rf-qa to auto-fix any output file, including tests, under fix_authorization: true with prompt-level restraint
- **Rationale for rejection**: Debate scoring matrix X-001: V3 won 78% on the test-modification subset. The empirical literature on Goodhart's law in ML evaluation (sycophancy in RLHF, reward-hacking in agentic systems) supports V3's structural prohibition over V1's prompt-level restraint. The cost of "test-gaming gets through" is asymmetric — catastrophic to the project's invariants.

### Rejected — Adopt V2's plan-time-only QA scope

- **Diff point**: S-001 (placement)
- **V2 approach proposed**: Validate at research / structural / qualitative stages only; defer execution-time validation to a separate skill
- **Rationale for rejection**: The base merges plan-time, task-time, and execution-time validation. V2's plan-time gates remain valuable but are properly the scope of `/task-builder`, not of the per-task QA architecture being merged here. V2's contributions to the base are protocol-level transfers (DNSP, DM-005, AX-5) — not scope-defining.

### Rejected — Adopt V3's full tier-skip for LIGHT/EXEMPT

- **Diff point**: X-002 (verification floor)
- **V3 approach proposed**: LIGHT and EXEMPT tiers skip verification entirely
- **Rationale for rejection**: Change #7 modifies this — V3's tier-skip is preserved for tasks that genuinely produce no verifiable output, but Change #7 tightens criteria to require minimum STANDARD verification when a tested module is touched. Pure skip is reserved for `--mode plan` / `--mode explain` shapes.

---

## Risk Summary

| Change | Risk | Impact if Fails | Rollback |
|---|---|---|---|
| #1 cross-phase validation | Low | Cross-phase integration bugs missed (V3 baseline) | Remove §4 subsection |
| #2 15-item checklist | Low | STRICT-tier reverts to generic quality-engineer prompt | Restore prior prompt |
| #3 DNSP partition | Low | Partition failures revert to implicit fallback | Remove §4 partition handling |
| #4 5 Adversarial Axes | Low | STRICT-tier loses explicit hallucination defense | Remove Axis column requirement |
| #5 anti-inflation rule | Low | TFEP incident reports without Self-Audit constraint | Remove Self-Audit section |
| #6 DM-005 wire | Low | TFEP wire is unversioned; stale-verdict gaming possible | Remove schema_version field |
| #7 tighter tier floor | Medium | LIGHT/EXEMPT skip restored; tested-module tasks under-validated | Revert tier-routing change |
| #8 composition doc | Low | Doc-only; no runtime impact | Remove §8 |
| **#9 sc:reflect-post integration** | **Medium** | **INV-006 unresolved; self-confirmation-bias persists; +10-30K tokens per STRICT** | **Disable §9; document gap** |
| #10 NEEDS_HUMAN state | Low | Ambiguous findings forced into fix-or-flag | Remove new verdict |
| #11 composition safety | Low | /task + /sc:task interactions undefined | Remove check |

## Review Status

- Approval: auto-approved (non-interactive mode)
- Timestamp: 2026-06-01
