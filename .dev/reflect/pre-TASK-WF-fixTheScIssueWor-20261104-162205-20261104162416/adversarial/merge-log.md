# Merge Execution Log

## Metadata
- Base: Variant 3 (opus:refactorer), `variant-3-original.md`
- Executor: merge-executor agent
- Changes applied: 13 of 13
- Status: success
- Timestamp: 2026-11-04T17:10:00Z
- Output: `merged-verdict.yaml` (this directory)

## Changes Applied

### Change 1: M-01 early-section authority (base R3-F5, modified)
- **Status**: Applied
- **Source**: Base R3-F5, plus Variant 1 R1-F1 (early-section part) and Variant 2 R2-2
- **Target**: Base finding R3-F5 (replaced)
- **Before**: R3-F5, `plan:19`, "Coordinator message authorizing the expansion is not stored in the package."; recommendation: save the message under artifacts/.
- **After**: M-01, `plan:19,22-26 vs source.md:1`, grounding_gap/minor; claim adds that the early section exceeds source.md:1 and that early placement is the plan's own inference; recommendation adds stating that inference in the plan. source_variants variant-1, variant-2, variant-3.
- **Provenance tag**: `# Source: Base (original, modified) — R3-F5 widened with Variant 1 R1-F1 (early-section part) and Variant 2 R2-2 — merged per Change #1`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 2: M-02 SKILL.md line outside the spec's Files list
- **Status**: Applied
- **Source**: Variant 2 R2-1, plus Variant 1 R1-F1 (SKILL.md part)
- **Target**: New finding after M-01
- **Before**: Not in base
- **After**: M-02, `plan:20,68-77 vs source.md:1`, drift/minor; Task 3 edits SKILL.md outside the spec's Files list; record sign-off or descope Task 3.
- **Provenance tag**: `# Source: Variant 2 (haiku:qa), R2-1, with Variant 1 R1-F1 (SKILL.md part) — merged per Change #2`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 3: M-03 pointer-style Rules bullet
- **Status**: Applied
- **Source**: Variant 2 R2-3 and Variant 1 R1-F2
- **Target**: New finding after M-02
- **Before**: Not in base
- **After**: M-03, `plan:27-29 vs source.md:1`, drift/minor; Rules bullet omits E-WORKER-NO-OUTPUT, the failure wording, consumers and harness-note clause; make it stand alone. source_variants variant-1, variant-2.
- **Provenance tag**: `# Source: Variant 2 (haiku:qa) R2-3 and Variant 1 (sonnet:analyzer) R1-F2 — merged per Change #3`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 4: M-06 exact-text delimiters (base R3-F1, modified)
- **Status**: Applied
- **Source**: Base R3-F1, plus Variant 1 R1-F5 and Variant 2 R2-5
- **Target**: Base finding R3-F1 (replaced)
- **Before**: R3-F1, `plan:26`, backtick spans with two-space indent; consistent mis-copy would pass.
- **After**: M-06, `plan:24-32`, grounding_gap/minor; adds the trailing-period boundary ambiguity; recommendation adds "or state that the module constants are the canonical bytes".
- **Provenance tag**: `# Source: Base (original, modified) — R3-F1 widened with Variant 1 R1-F5 and Variant 2 R2-5 — merged per Change #4`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 5: M-07 verify-sync on unrelated drift
- **Status**: Applied
- **Source**: Variant 1 R1-F6
- **Target**: New finding
- **Before**: Not in base
- **After**: M-07, `plan:72,77; Makefile:188-200`, grounding_gap/minor; record unrelated verify-sync failures in t3-verify-sync.log and do not fix them here.
- **Provenance tag**: `# Source: Variant 1 (sonnet:analyzer), R1-F6 — merged per Change #5`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 6: M-09 report wording (base R3-F2, modified)
- **Status**: Applied
- **Source**: Base R3-F2, plus invariant-probe INV-008
- **Target**: Base finding R3-F2 (replaced)
- **Before**: R3-F2, `plan:26`, "the reports under analysis/" repeats harness trigger words.
- **After**: M-09, `plan:26; issue-worker-t2.md:17; issue-worker-t1.md:17`, drift/minor; adds the clash with the unchanged "save its report under <D>/analysis/" job text (INV-008).
- **Provenance tag**: `# Source: Base (original, modified) — R3-F2 with invariant-probe INV-008 folded in — merged per Change #6`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 7: Remove R3-F3 (M-10)
- **Status**: Applied (deletion)
- **Source**: Base R3-F3; debate C-005
- **Target**: Base finding R3-F3 (deleted from the findings list)
- **Before**: R3-F3, consumer parenthetical "(gh --body-file posts and /sc:recommend)" reads as the full consumer list; drift/minor.
- **After**: Absent from `merged-verdict.yaml`. Listed under the plan's "Changes NOT Being Made" as M-10.
- **Provenance tag**: none (no content written)
- **Dropped-anchor record**: anchor `R3-F3` ("Parenthetical '(gh --body-file posts and /sc:recommend)' reads as the full consumer list"); source variant: Variant 3 (base); change number: 7; decision basis: the parenthetical copies source.md:1 word for word, V3 conceded in Round 1, all three dropped it in Round 2; replacement target: none.
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 8: M-11 "names each exact path" (base R3-F4, modified)
- **Status**: Applied
- **Source**: Base R3-F4, plus INV-007 (subsumed)
- **Target**: Base finding R3-F4 (replaced)
- **Before**: R3-F4, `plan:32; refs/claim.md:24,54,58; refs/create.md:20`, covered both the analysis/ path problem and the refs' spawn lists naming no paths.
- **After**: M-11, `plan:32; refs/claim.md:58`, drift/minor; claim and recommendation narrowed to the analysis/ directory per the plan text.
- **Provenance tag**: `# Source: Base (original, modified) — R3-F4 narrowed to the analysis/ point (refs point moved to M-15), INV-007 subsumed — merged per Change #8`
- **Dropped-anchor record**: anchor "refs' spawn lists name no paths and stay unchanged" and recommendation "record that refs stay unchanged on purpose"; source variant: Variant 3 (base) R3-F4; change number: 8; decision basis: the plan's M-11 text omits it; replacement target: M-15 (Change 12), whose claim and recommendation carry both points. Also `refs/claim.md:24` and `refs/create.md:20` leave M-11's file_line; `refs/create.md:20` reappears in M-15.
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 9: M-12 helper position check (base R3-F6, kept)
- **Status**: Applied
- **Source**: Base R3-F6
- **Target**: Base finding R3-F6 (kept, restated)
- **Before**: R3-F6, `plan:45`, helper checks the bullet is in Rules but not that it follows the "Writing only under" bullet.
- **After**: M-12, `plan:27,45,65`, drift/minor; same substance, adds that plan:27 requires the position and the Task 2 criterion does not check it. Recommendation unchanged in substance.
- **Provenance tag**: `# Source: Base (original, modified) — R3-F6 kept; id, file_line and wording restated — merged per Change #9` (tagged "modified" rather than "original" because the id, file_line and wording changed)
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 10: M-13 untracked targets make the diff criteria vacuous (blocking)
- **Status**: Applied
- **Source**: invariant-probe INV-001 (HIGH); Round 2.6 unanimous grounding_gap, blocking
- **Target**: New finding
- **Before**: Not in base (base verdict was PASS)
- **After**: M-13, `plan:53,65,75`, grounding_gap/**blocking**; all five targets untracked so `git diff` criteria pass on empty output; snapshot to ./artifacts/pre/ and use `git diff --no-index`.
- **Provenance tag**: `# Source: invariant-probe INV-001 (HIGH), voted blocking in Round 2.6 — merged per Change #10`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 11: M-14 behavioural sufficiency
- **Status**: Applied
- **Source**: invariant-probe INV-002 (MEDIUM), with A-001 and A-003
- **Target**: New finding
- **Before**: Not in base
- **After**: M-14, `plan:12,15,72; SKILL.md:58-62`, grounding_gap/minor; tests pin text only; state it and record a live re-claim of #365 as follow-up.
- **Provenance tag**: `# Source: invariant-probe INV-002 (MEDIUM), with debate points A-001 and A-003 — merged per Change #11`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 12: M-15 the refs' spawn steps name no paths
- **Status**: Applied
- **Source**: invariant-probe INV-003 (MEDIUM); Round 2.6 2-of-3 majority (V2 voted drift)
- **Target**: New finding
- **Before**: Not in base as a separate finding (partly in R3-F4)
- **After**: M-15, `plan:20,32; refs/claim.md:53-54; refs/create.md:20`, grounding_gap/minor; SKILL.md line may not govern spawn prompts built from the refs; word it to cover the Wave spawns and record refs unchanged on purpose.
- **Provenance tag**: `# Source: invariant-probe INV-003 (MEDIUM), absorbs the refs half of base R3-F4 — merged per Change #12`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 13: Header, verdict and unresolved conflicts
- **Status**: Applied
- **Source**: Refactor plan Overview and Change 13
- **Target**: Top-level keys of the output
- **Before**: Base card keys `reviewer`, `persona`, `model_class`, `verdict: PASS`, `self_reported_confidence`, `findings`, `self_audit`.
- **After**: Provenance header (3 comment lines) and keys in order `merge_method: "adversarial"`, `base_variant: "opus:refactorer (variant-3)"`, `convergence_score: 0.94`, `verdict: "FAIL"`, `findings` (11, in the planned order), `unresolved_conflicts` (one entry, X-001).
- **Provenance tag**: `# Provenance: This document was produced by /sc:adversarial` / `# Base: Variant 3 (opus:refactorer)` / `# Merge date: 2026-11-04T17:10:00Z`; `# Source: Refactor plan — merged per Change #13` above `unresolved_conflicts`
- **Dropped-anchor record**: base keys `reviewer: 3`, `persona`, `model_class`, `self_reported_confidence: 0.80`, `self_audit` and `verdict: PASS`; source variant: Variant 3 (base); change number: 13; decision basis: the plan's Overview fixes the output schema to six top-level keys, and the verdict rule makes M-13 force FAIL; replacement target: the six fixed keys.
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

## Post-Merge Validation

Command run:
`uv run --no-project --with pyyaml python -I - <adversarial-dir>` (inline script: `yaml.safe_load` plus field checks and a field-by-field comparison against `refactor-plan.md`)

Result:
```
['merge_method', 'base_variant', 'convergence_score', 'verdict', 'findings', 'unresolved_conflicts'] 11 FAIL 1
order_ok True
dup_ids []
keys_ok True
class_ok True
sev_ok True
verdict_rule_ok True
plan_text_mismatches []
source_comment_above_each_finding True
dropped_ids_absent True
```

### Structural Integrity
- YAML parse: ✅ `yaml.safe_load` succeeded.
- Top-level key order: ✅ exactly `merge_method, base_variant, convergence_score, verdict, findings, unresolved_conflicts`.
- Finding order: ✅ M-01, M-02, M-03, M-06, M-07, M-09, M-11, M-12, M-13, M-14, M-15 (11 findings).
- Finding key order: ✅ every finding has exactly `id, file_line, claim, class, severity, recommendation, source_variants`.
- Domains: ✅ every class is in {authorized, necessary, drift, regression, grounding_gap}; every severity is in {blocking, minor}.
- Provenance: ✅ three-line header present; one `# Source:` comment directly above each of the 11 findings.
- Plan fidelity: ✅ file_line, claim, recommendation, class, severity and source_variants match the plan text exactly for all 11 findings (0 mismatches).

### Internal References
- Total references checked: 8
- Resolved: 8
  - `unresolved_conflicts[X-001].status` names M-01 (grounding_gap) and M-02 (drift): both present with those classes.
  - Plan "Changes NOT Being Made": M-04, M-05, M-08, M-10 are absent from the findings (correct); INV-007 is covered by M-11 (present); INV-005 is dropped and absent.
  - Plan Change 8 / Change 12 split: the refs half of R3-F4 resolves to M-15 (present).
  - Plan verdict rule "M-13 is blocking": M-13 present with severity blocking.
- Broken: 0

### Contradiction Re-Scan
- New contradictions introduced: 0
- Verdict vs blocking count: verdict FAIL, blocking count 1 (M-13); the rule "FAIL only if any finding is blocking" holds.
- Duplicate ids: none.
- Kept vs not-made: no finding id appears both in the findings and in "Changes NOT Being Made" (M-04, M-05, M-08, M-10, R3-F3 all absent).
- Overlap check: M-11 (analysis/ path naming) and M-15 (refs' spawn prompts) cover separate halves of base R3-F4; their recommendations do not conflict. M-01 (save coordinator message) and M-02 (record sign-off or descope Task 3) are compatible.
- Noted, not a contradiction: M-15 lists variant-2 in source_variants although V2 voted drift in Round 2.6; the plan specifies this list, and the 2-of-3 majority class is recorded.

### Threshold Preservation / Dropped Anchors
- Fixed values preserved: `convergence_score: 0.94` exact; all line numbers in file_line copied from the plan.
- Dropped anchors: R3-F3 (Change 7), the refs half of R3-F4 moved to M-15 (Change 8), and the base card's metadata keys (Change 13); each has a dropped-anchor record above. No unaccounted anchors.

## Summary
- Total changes planned: 13
- Successfully applied: 13
- Failed: 0
- Skipped: 0
- Post-merge validation: PASS (YAML parses; 11 findings; verdict FAIL; 1 blocking finding, M-13)
