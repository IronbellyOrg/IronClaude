# Refactor Plan — Merging V1 and V2 into V3 Base

## Overview
- Base variant: V3 (QA, --persona-qa) — combined score 0.977
- Variants incorporated from: V1 (Architect, 5 changes), V2 (Analyzer, 5 changes)
- Total changes planned: 10
- Changes rejected (with rationale): 5
- Overall risk: Low (all changes are additive or token-swap replacements)
- Review status: auto-approved (depth=quick, no `--interactive` set)

## Planned Changes

### Change #1 — Add `conflict-register.md` as file-mediated precedence ledger
- **Source**: V1 §Phase 1 Step 1.0; V1 §3.3, 5.3, 7.3
- **Target location in base**: V3's Phase 1 setup (currently V3 only declares state/ dir, no register)
- **Integration approach**: insert (new file declaration in pre-phase setup; cross-references added in Phases 3, 5, 7)
- **Rationale**: V3's four-case rule benefits from a single file-mediated audit trail; the register makes case decisions visible across phases without re-derivation. Debate evidence: U-001 confidence 92%.
- **Risk level**: Low — additive artifact, no behavioral changes to existing phases.

### Change #2 — Add explicit Phase 3 `proposals/INDEX.md` manifest
- **Source**: V1 §Step 3.4
- **Target location in base**: V3 Phase 3 (currently writes proposals as `NN-<slug>.md` but does not enumerate)
- **Integration approach**: append (new Step at end of Phase 3 that writes INDEX.md as a comma-separated path manifest)
- **Rationale**: Removes ambiguity at Phase 4 `--compare` invocation. Debate evidence: S-001 confidence 88%.
- **Risk level**: Low — new write step with deterministic content.

### Change #3 — Remove `--downstream roadmap` from Phase 7
- **Source**: V1 §Phase 7 Step 7.1
- **Target location in base**: V3 Phase 7 currently has `--downstream roadmap`
- **Integration approach**: replace (remove the flag from the /sc:spec-panel invocation; add a rationale comment)
- **Rationale**: spec-panel.md Step 6b activates roadmap-oriented frontmatter that the prd skill (the actual downstream consumer) ignores. The flag is dead at best, misleading at worst. Debate evidence: C-005 confidence 95%.
- **Risk level**: Low — flag removal documented per V1 §S-005; not invented behavior.

### Change #4 — Add `SUPPORTING_INPUTS` to Phase 8 prd skill invocation
- **Source**: V1 §Phase 8 Step 8.2
- **Target location in base**: V3 Phase 8 currently passes WHAT/WHY/WHERE/OUTPUT (with V3's INPUT_SPEC routing fix)
- **Integration approach**: append (add SUPPORTING_INPUTS line listing conflict-register, merge-log, reflect output)
- **Rationale**: Routes additional context the PRD can trace decisions through. Combines with V3's INPUT_SPEC fix (Change #5 carried through from base).
- **Risk level**: Low — additive; prd skill may ignore SUPPORTING_INPUTS, but base's WHAT/WHERE routing fix already binds the spec.

### Change #5 — Add Phase 1 Step 1.0 explicit subdirectory pre-creation
- **Source**: V1 §Phase 1 Step 1.0
- **Target location in base**: V3 currently mentions state/ but doesn't pre-create all subdirs
- **Integration approach**: insert (new Step 1.0 that creates context-digests/, analysis/, proposals/, adversarial/, reflection/, state/ via touch; touches conflict-register.md and pipeline-log.md)
- **Rationale**: Hook-compliant first writes need parent directories. Debate evidence: S-004 confidence 90%.
- **Risk level**: Low — pure setup.

### Change #6 — Outcome-bound Sequential thought count
- **Source**: V2 §Phase 2 "stop when each row has source-grounded justification"
- **Target location in base**: V3 Phase 3 currently says "15-25 thoughts minimum"
- **Integration approach**: replace (drop the numeric floor, replace with outcome-bound phrasing)
- **Rationale**: V2 §A-001 — FINAL-REPORT §5 carries 5 proposals; 15-thought floor is unanchored. Debate evidence: C-002 confidence 95%.
- **Risk level**: Low — language tightening.

### Change #7 — Change `/sc:adversarial --depth deep` to `--depth standard` with conditional escalation
- **Source**: V2 §Phase 3 flag-discipline notes
- **Target location in base**: V3 Phase 4 currently `--depth deep`
- **Integration approach**: replace (use standard as default; escalate to deep only when a proposal's cited risk is HIGH per FINAL-REPORT §9)
- **Rationale**: FINAL-REPORT §6.1 ran prior study at depth=quick, converged at 0.81 mean. Source's `deep` is unjustified. Debate evidence: X-001 confidence 70%.
- **Risk level**: Low — conditional escalation preserves the ability to deepen.

### Change #8 — Drop `/sc:adversarial --interactive`
- **Source**: V2 §A-011
- **Target location in base**: V3 Phase 4 currently `--interactive`
- **Integration approach**: replace (remove the flag)
- **Rationale**: Batch-replayable orchestration contract is cleaner; Phases 5-8 don't expect human-in-loop. Debate evidence: X-003 confidence 82%.
- **Risk level**: Low — verified-flag set respected.

### Change #9 — Add required proposal-header fields `final_report_citation` + `direction_inversion_basis`
- **Source**: V2 §Phase 2 proposal header schema
- **Target location in base**: V3 Phase 3 proposal file requirements (currently CASE-A/B/C/D classification + complexity + quality gain)
- **Integration approach**: append (extend the required header schema; missing fields halt the proposal in Phase 4 gate)
- **Rationale**: Closes the inversion-symmetry evidence gap (V2 §G-A1). The user's reversal of FINAL-REPORT direction needs per-mechanism justification. Debate evidence: U-003 confidence 90%.
- **Risk level**: Low — additive header fields.

### Change #10 — Add Glob-and-report-absent rule for Bucket D and Bucket F
- **Source**: V2 §Phase 1 buckets
- **Target location in base**: V3 Phase 1 bucket list (currently lists rf-* agents and sample release specs without absence check)
- **Integration approach**: append (Bucket D Globs rf-*.md and reports "absent" for any missing; Bucket F Globs `.dev/releases/current/**/release-spec.md` and reports "no samples available")
- **Rationale**: Verified in V2 §A-007 that Bucket F is currently empty in this repo. Prevents sub-agent fabrication. Debate evidence: U-004 confidence 88%.
- **Risk level**: Low — pure validation.

## Changes NOT Being Made (transparency)

### Rejected: V2's Phase 2+3 folding
- **What V2 proposed**: collapse Phase 2 matrices and Phase 3 brainstorm into a single `analysis.md`
- **Why rejected**: collapses the audit trail. V1's critique §W4 and V3's preserved structure both prefer separation. Keeping the two-phase shape lets a reviewer inspect the matrix in isolation from the brainstorm.

### Rejected: V2's outright replacement of `/sc:reflect` with Citation Gate
- **What V2 proposed**: drop /sc:reflect entirely; replace with `gate-report.md` G1-G5
- **Why rejected**: the user explicitly asked for `/sc:reflect` engagement throughout. Replacement overshoots the brief. **Compromise (Change-IN-MERGE-#11)**: incorporate V2's G1-G5 gate as an additional artifact INSIDE Phase 5; reflect runs first, then the gate validates its output. This preserves user intent while gaining V2's binary-halt rigor.

### Rejected: V2's drop of `--convergence 0.80`
- **What V2 proposed**: omit the convergence flag entirely, defer to protocol default
- **Why rejected**: V3's explicit 0.80 + sub-threshold branch (Phase 4) is the stronger failure-mode contract. Protocol default value is not verified in this repo; omitting risks a weaker bar than the source set.

### Rejected: V3's retention of `--downstream roadmap`
- **What V3 retained**: source's `--downstream roadmap` flag in Phase 7
- **Why rejected**: addressed by Change #3 above; V1's evidence-backed argument prevails.

### Rejected: V3's sequential single-value `--focus` passes
- **What V3 changed**: split source's `--focus structure,completeness` into two sequential `--focus completeness` then `--focus correctness` calls
- **Why rejected**: adversarial.md:97 (example block) shows `--focus structure,completeness` as the documented invocation pattern with comma-list semantics. Restoring the source's comma-list usage. Documented as V3-deviation rollback in merge-log.

## Compromise / Hybrid Change

### Change #11 — Hybrid /sc:reflect + Citation Gate (Phase 5)
- **Source**: V2 §Phase 4 G1-G5 gate + user's explicit /sc:reflect engagement requirement
- **Target location in base**: V3 Phase 5
- **Integration approach**: sequence — (a) run /sc:reflect first per V3 (with retry → `--type completion` → DEGRADED), (b) then produce `gate-report.md` with G1-G5 PASS/FAIL rows per V2, (c) gate is the binding decision artifact; reflect output is the advisory layer
- **Rationale**: Preserves user intent (sc:reflect engaged) while incorporating V2's binary-halt rigor. Both V2 (§A-005) and V3 (§Q-004) flagged the source's reflect-as-decision conflation; merged solution separates the two.
- **Risk level**: Low — additive; both tools' outputs are persisted.

## Risk Summary

| Change | Risk | Impact | Rollback |
|--------|------|--------|----------|
| 1-5 | Low | Additive structural artifacts | Delete added artifacts; phases function without them |
| 6 | Low | Sequential length is content-bounded, may extend wall-clock | Reinstate "15-25 minimum" |
| 7 | Low | adversarial run depth changes | Use --depth deep as override |
| 8 | Low | No --interactive prompts | Add back --interactive if review needed |
| 9 | Medium-Low | Halt on missing header fields | Demote required fields to advisory |
| 10 | Low | Bucket D/F may now report absent | Treat absent as DEGRADED, continue |
| 11 | Low | Both reflect and gate run | Drop one if redundancy proves wasteful |

## Approval
- **Status**: Auto-approved
- **Timestamp**: 2026-05-14T06:55:00Z
- **Mode**: Non-interactive (depth=quick; --interactive not set on this debate)
