# Diff Analysis: Tier-2 reviewer-card (UC-2 deviation audit) Comparison

## Metadata
- Generated: 2026-10-25T00:00:00Z
- Pipeline: Skill sc:sc-adversarial-protocol, Mode A, --depth standard, --convergence 0.80, --focus correctness,coverage,deviation-classification, non-interactive
- Step 1 author: sc:debate-orchestrator (opus) — native analysis (no /sc:sc-analyze delegation)
- Variants compared: 2
  - Variant 1 = `variant-1-original.md` — reviewer-1, persona analyzer, sonnet slot; calibrated C = 0.90 (self-reported 0.85 ignored)
  - Variant 2 = `variant-2-original.md` — reviewer-2, persona qa, haiku slot (env alias grok-4.7[1m]); calibrated C = 0.92 (self-reported 0.8 ignored)
- Evidence grounding: frozen snapshot S = `runs/post-tier2-attempt-1/artifacts/reviewer-snapshot/root` (spec.md, completed.md, changes.patch, src/greeting.py, tests/test_greeting.py, execution.log, `__run_evidence__/artifacts/{task-diff-map.yaml,git-inventory.txt}`) and `<plugin>/skills/sc-reflect-protocol/refs/deviation-taxonomy.md`. Orchestrator re-read every one of those files before writing this analysis.
- Total differences found: 17 debate points (S 3, C 9, X 3, A 2) plus 6 unique contributions (U, not in the convergence denominator)
- Categories: structural (3), content (9), contradictions (3), unique (6), shared assumptions (2 promoted UNSTATED; 4 STATED documented, not promoted)
- Variant metadata: V1 104 lines, 4 top-level YAML sections with list content (grounding_gaps 3, agreements 5, disagreements 2, risks 5, recommendations 3) + leading 9-line comment rationale block; V2 68 lines, same keys (grounding_gaps 3, agreements 7, disagreements 1, risks 6, recommendations 5), no rationale comment block.

## Agreement baseline (not diff points)
Both variants: `findings: []` (no 4-class deviation); 3 grounding gaps with identical hunk_refs (G1 T-103 test file not in diff; G2 `from src.greeting import greet` importability [INFERRED]; G3 `if not name` falsy/whitespace semantics, R-002); G1/G2 `decision_needed_by_user: true`, G3 `false`; `regression_present: false`; `status_recommendation: partial` forced by non-empty grounding gaps (deviation-taxonomy.md:149-153); R-001 and R-002 statically satisfied; no unmapped hunks (task-diff-map.yaml:29). Orchestrator verified each of these against S.

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Severity | Taxonomy |
|---|------|-----------|-----------|----------|----------|
| S-001 | Rationale placement | 9-line `#` comment block (lines 6-14) carrying basis/evidence for `findings: []` before `grounding_gaps` | No comment block; the same basis is expressed as structured `agreements_with_t1` entries with line citations | Low | L1 |
| S-002 | Scalar style | Folded block scalars (`>`) for multi-sentence fields | Double-quoted single-line strings | Low | L1 |
| S-003 | List granularity | agreements 5 / disagreements 2 / risks 5 / recommendations 3 | agreements 7 / disagreements 1 / risks 6 / recommendations 5 | Medium | L2 |

## Content Differences

| # | Topic | Variant 1 Approach | Variant 2 Approach | Severity | Taxonomy |
|---|-------|-------------------|-------------------|----------|----------|
| C-001 | Routing of G3 (`if not name` guard, src/greeting.py:2-3) | Keeps G3 in `grounding_gaps` but argues (disagreements_with_t1 #1) it belongs in advisory `correctness-gaps.yaml` and must not count toward forcing partial; concedes the sibling-symbol example (deviation-taxonomy.md:161/167) "does not fit exactly" | Keeps G3 as a grounding gap with `decision_needed_by_user: false`, no routing objection | Medium | L3 (guard) |
| C-002 | G1 rationale (why T-103 is unverified) | "git-inventory.txt says the repo has no commits, so it carries no tracked-state signal"; only delivery claim is execution.log:4 | Same class, but corrects T1 wording: whole tree is untracked incl. src/greeting.py (git-inventory.txt:7-9), so "absence from the supplied diff is the gap, not untracked status" | Low | L2 |
| C-003 | Strength of G2 (import resolution) | Explicit disagreement: G2 "weakly grounded", legitimate only because nothing ran; "would not call it a likely failure" | Retains G2 as risk; recommends adding `src/__init__.py` or pythonpath config if plain pytest fails to collect | Medium | L2 (module/dependency) |
| C-004 | Evidence provenance of citations | Risk #5 (line 82) states it did NOT read git-inventory.txt, reuse-audit.yaml or execution.log in the snapshot and relies on brief excerpts, yet cites execution.log:4/5 and git-inventory.txt in G1 and agreements | Cites git-inventory.txt:5/7/8/9, execution.log:2-5, task-diff-map.yaml:23-28/29/34/37/38 directly; all verified correct against S | High | L2 |
| C-005 | Requirement coverage enumeration | R-001/R-002 in comment block (src/greeting.py:4, :2-3); R-003 only via G1 | Per-requirement agreements for R-001/R-002/R-003 with changes.patch line refs, explicit statement that every MUST span (spec.md:6/9/12) is in the matrix, and executed coverage 0/3 | Medium | L2 |
| C-006 | Completion-status correction | Names false-completion risk (completed.md:2) only; no recommendation to change it | High-priority recommendation: set completed.md frontmatter `status: partial` until test hunk + real run exist | Medium | L3 (state transition) |
| C-007 | Spec clarification for R-002 falsy/whitespace inputs | Priority low; route to correctness-gaps.yaml; optional spec clarification | Priority medium; state None/non-str/whitespace behavior in spec, align src/greeting.py:2, add assertions | Low | L3 (validation rule) |
| C-008 | Test-oracle weakness | Manual try/except (tests/test_greeting.py:9-13) "adequate for R-003 but weak as a regression guard" | tests/test_greeting.py:11 accepts any ValueError, does not check message; spec.md:9 requires no message | Low | L3 (validation) |
| C-009 | Recommendation target for diff regeneration | Rec #1 `file:` is the absolute frozen-snapshot path `.../reviewer-snapshot/root/changes.patch`; the audited diff source is the audit-root changes.patch (task-diff-map.yaml:3) | Rec #1 `file: "changes.patch"` (bare; header line 2 resolves bare paths under the snapshot, so equally ambiguous as an action target, but not explicitly the frozen copy) | Medium | L2 |

## Contradictions

| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Impact | Taxonomy |
|---|-------------------|-------------------|-------------------|--------|----------|
| X-001 | `verdict.tasklist_completion_pct` unit | `66.7` (percent) | `0.667` (fraction). Contract schema: `tasklist_completion_pct: <float 0.0-1.0>` (sc-reflect-protocol SKILL.md:1136); task-diff-map.yaml:34 = 0.667 | High (machine-consumed field; 66.7 is out of range) | L2 (interface) |
| X-002 | Is G3 a Grounding Gap? | Cross + intra-variant: lists G3 under `grounding_gaps` while stating "This is not a Grounding Gap in the strict taxonomy sense" and that it should be advisory correctness-gap | G3 is a grounding gap (agrees with T1 card) | Medium | L3 (guard) |
| X-003 | Citation basis (intra-V1) | Cites execution.log:4/5 and git-inventory.txt (lines 13, 21, 59, 78) while line 82 says those files were not read | n/a (V2 has no such conflict) | Medium | L2 |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | V2 | `proposed.md` is listed untracked (git-inventory.txt:5) but absent from the snapshot; may carry extra task/MUST text — recommendation to bring it into the snapshot or have user scope it out | Medium |
| U-002 | V2 | Recommendation to set completed.md:2 `status: partial` (matches T1 rec #4) | Medium |
| U-003 | V2 | Concrete collection remedy (add `src/__init__.py` or pythonpath config) plus verifier "both exit 0 with 2 passed" | Low |
| U-004 | V1 | Proposal to route G3 to advisory `correctness-gaps.yaml` (non-gating) | Medium (contested — see C-001/X-002) |
| U-005 | V1 | Honest self-disclosure of evidence gaps (files not independently read) | Low |
| U-006 | V2 | Explicit "Executed coverage is 0/3" statement | Low |

## Shared Assumptions

Promoted ([SHARED-ASSUMPTION], UNSTATED in both variants; included in convergence denominator):

| A-NNN | Assumption | Source Agreement | Impact | Status | Taxonomy |
|-------|-----------|------------------|--------|--------|----------|
| A-001 | The frozen snapshot is a complete mirror of the audit root for absence claims: both variants infer "no src/__init__.py, tests/__init__.py, conftest.py, pyproject.toml or pytest config" from a snapshot Glob (V1 G2; V2 G2), yet V2 itself shows the snapshot omits `proposed.md` (git-inventory.txt:5) — so absence-in-snapshot may not equal absence-in-repo | Agreement on G2 evidence_missing | Medium (G2 grounding and the "add __init__.py" remedy depend on it) | UNSTATED | L3 (boundary) |
| A-002 | The absence of a tests/ hunk reflects non-delivery evidence rather than an audit-scope boundary: task-diff-map.yaml:27 records the test file as "outside --scope src/"; neither variant states that the scope configuration, not the work, may be why the diff lacks the hunk (both just recommend regenerating the diff) | Agreement on G1 + "regenerate changes.patch" | Medium (affects whether G1 is owner=user vs owner=reviewer/orchestrator re-scope) | UNSTATED | L3 (boundary) |

STATED (documented, not promoted): (a) a mapped task with no hunk is a Grounding Gap, not Drift — V1 G1 why_not_classifiable cites deviation-taxonomy.md:62/109; (b) R-001/R-002 satisfaction is static-only — both; (c) partial is forced independently of G3 — V1 disagreements #1; (d) `''` is the only spec-defined empty input — both G3. CONTRADICTED: none.

## Summary
- Total structural differences: 3
- Total content differences: 9
- Total contradictions: 3
- Total unique contributions: 6
- Total shared assumptions surfaced: 6 (UNSTATED: 2 promoted, STATED: 4, CONTRADICTED: 0)
- Convergence denominator: S 3 + C 9 + X 3 + A 2 = 17
- Highest-severity items: C-004, X-001 (High); C-001, C-003, C-005, C-006, C-009, X-002, X-003, S-003, A-001, A-002 (Medium)
- Taxonomy pre-tag: L1 = {S-001, S-002}; L2 = {S-003, C-002, C-003, C-004, C-005, C-009, X-001, X-003}; L3 = {C-001, C-006, C-007, C-008, X-002, A-001, A-002} — all three levels populated
- Similarity check: 17 debate points vs ~30 comparable items (>50% differ) — NOT "substantially identical"; debate proceeds
