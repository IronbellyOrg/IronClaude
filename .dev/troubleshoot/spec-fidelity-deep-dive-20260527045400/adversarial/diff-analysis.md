# Diff Analysis: Spec-Fidelity Convergence Fix Proposals Comparison

## Metadata
- Generated: 2026-05-27T05:55:00Z
- Variants compared: 5 (fix-1 minimal, fix-2 fixability-classifier, fix-3 upstream-canon, fix-4 advisory-tier, fix-5 code+tests)
- Total differences found: 5 structural + 5 content + 3 contradictions + 4 unique contributions + 4 shared assumptions
- Categories: structural (5), content (5), contradictions (3), unique (4), shared assumptions (4)

## Structural Differences

| # | Area | fix-1 | fix-2 | fix-3 | fix-4 | fix-5 | Severity |
|---|---|---|---|---|---|---|---|
| S-001 | Files touched | 1 (`structural_checkers.py`) | 1 (`structural_checkers.py`) | 1 (`spec_parser.py`) | 3 (`structural_checkers.py` + `commands.py` + `Finding.severity`) | 1 production + 4 test files | Medium |
| S-002 | Production LOC | ~15 | ~48 | ~12 | ~57 | ~15 | Low |
| S-003 | Test LOC | ~30 (3 example tests) | ~50 (5 tests) | ~30 (3 tests) | ~40 (4 tests) | ~150 (property-based + flatline + integration) | Medium |
| S-004 | API surface added | none | optional `fixability` arg on `_make_finding` | none | new CLI flags + new severity enum value | none | Medium |
| S-005 | New abstractions introduced | 1 helper | 2 helpers + 1 enum + 1 template dict | 1 helper | 1 helper + 1 severity tier + 1 CLI lane | 1 helper | Medium |

## Content Differences

| # | Topic | fix-1 approach | fix-2 approach | fix-3 approach | fix-4 approach | fix-5 approach | Severity |
|---|---|---|---|---|---|---|---|
| C-001 | WHERE to canonicalize | comparator (in `check_signatures`) | comparator + emission-time classifier | extractor (`extract_requirement_ids`) | comparator + severity tier | comparator (mirrors fix-1) | **High** |
| C-002 | Generalization scope | this rule_id only | all rule_ids via fixability classifier | this rule_id (but seam eliminated) | this rule_id + CLI lane extends to future | this rule_id + property tests generalize family | **High** |
| C-003 | Drift severity | MEDIUM (`id_schema_drift`) | MEDIUM (auto-demoted via classifier) | drift not emitted (zero findings) | new `ADVISORY` tier | MEDIUM (`id_schema_drift`) | **High** |
| C-004 | Recurrence foreclosure | none claimed | fixability invariant addresses next shape proactively | seam-elimination forecloses extractor/comparator asymmetry recurrence | CLI lane pattern extends to next rule_id (1-line additions) | property-based tests catch next-family drift at construction | **High** |
| C-005 | Test depth | example fixtures only | example fixtures only | example + family-cross-coverage | example fixtures only | property-based + flatline-halt integration + cross-cutting | Medium |

## Contradictions

| # | Point of Conflict | fix-X claim | fix-Y claim | Impact |
|---|---|---|---|---|
| X-001 | Module ownership of canonicalization | fix-1, fix-2, fix-4, fix-5: "structural_checkers.py owns comparator semantics (FR-1/FR-3) → fix lives here" | fix-3: "spec_parser.py owns extraction (FR-2/FR-5); canonicalization-as-extraction is within parser's mandate → fix lives there" | **High** — these are mutually exclusive locus choices; both cite Restriction 1 of doc-context.md but interpret it differently. Resolution requires choosing one reading. |
| X-002 | Root-cause framing | fix-1, fix-3, fix-5: "the comparator (or its surrounding seam) IS the root cause" | fix-2: "the comparator is a SYMPTOM; missing fixability invariant at emission boundary IS the root cause" | **High** — drives whether to ship surgical patch (fix-1/3/5) or scaffolded fix (fix-2). |
| X-003 | Severity-tier extension | fix-1, fix-2, fix-3, fix-5: "demote drift to existing MEDIUM tier (consistent with S5 precedent at `_classify_nfr_severity:309-327`)" | fix-4: "introduce new ADVISORY tier beneath MEDIUM to semantically distinguish 'informational but found' from 'deferred by design as structurally unfixable'" | Medium — both are defensible; ADVISORY tier introduces ongoing audit burden on `Finding.severity` consumers but provides cleaner semantics. |

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---|---|---|
| U-001 | fix-5 | Property-based comparator test via `hypothesis` library (gated by `pytest.importorskip` to respect "not a declared dependency" posture). Catches family-agnostic drift at construction time, would have prevented bug 18 months ago. | **High** — family-agnostic coverage is unique; no other proposal provides this. |
| U-002 | fix-3 | "Remove the seam entirely" framing — moves canonicalization to the source so all 5 checkers (current and future) consume canonical IDs by construction. Refactoring-quality signal: bug disappears at call site without modifying call site. | **High** — structurally elegant; eliminates the entire class of extractor/comparator asymmetry recurrence. |
| U-003 | fix-4 | CLI lane pattern (`--allow-advisory-drift` / `--strict-no-advisory`) modeled on `--allow-cosmetic-remediation`. Operator runtime control over advisory behavior; preserves backward-compat for high-stakes pipelines. | Medium — useful for production rollout safety; not required for TUIBBS unblock. |
| U-004 | fix-2 | `_classify_fixability(dim, mismatch_type, count, canonical) → FixabilityClass` — generalizable invariant at finding-emission boundary. Captures the missing precondition that the convergence loop and 30% guard tacitly assume. | **High** — addresses the structural recurrence vector identified in historical-context.md Pattern 2 directly. |

## Shared Assumptions

(Surfaced by AD-2 — UNSTATED preconditions promoted to debate-attention diff points)

| A-NNN | Assumption | Source Agreement | Impact | Status |
|---|---|---|---|---|
| A-001 | The spec must be treated as immutable input (Restriction 5). The agent cannot edit the spec. | All 5 proposals enforce this | **High** — if the canonicalization decision is "the spec should adopt zero-pad form" (a legitimate alternative), no proposal accommodates it. The right outcome may sometimes be a human-driven spec edit, not a code change. | UNSTATED — none of the 5 proposals consider spec-side normalization as a valid outcome path. |
| A-002 | Zero-pad → unpad is the canonical direction. `D01` canonicalizes to `D1`, not the reverse. | All 5 (implicit in canonicalizer design — strip leading zeros) | Medium — if a project intentionally uses zero-pad for sortability or alignment, the canonicalizer DESTROYS that intent at the comparator boundary. | UNSTATED — direction choice is justified by none of the proposals. |
| A-003 | The 30% per-patch diff guard at `remediate_executor.py:309-362` is correctly calibrated. None of the proposals challenge it. | All 5 work around it; none modify it | Medium — S3 from the deferred backlog (tiered diff-relax) targeted this exact guard. By accepting the guard, all 5 proposals trade off agent autonomy for safety. | UNSTATED — alternative S3 framing was deferred without debate evidence in this round. |
| A-004 | `convergence.py:539` (the binary `active_highs == 0` pass condition) must not be modified. | fix-1, fix-2, fix-3, fix-5 explicitly avoid it; fix-4 implicitly avoids by introducing ADVISORY tier "beneath" the predicate's filter | **High** — if the deeper architectural defect IS the binary pass condition itself (fix-4's strong claim), then NOT modifying it just relocates the problem to severity-tier vocabulary. The system-architect framing is partially blocked by this shared restriction. | STATED in fix-1, fix-2, fix-5; UNSTATED-but-honored in fix-3, fix-4. |

## Summary

- Total structural differences: 5
- Total content differences: 5
- Total contradictions: 3 (2 High, 1 Medium)
- Total unique contributions: 4 (3 High, 1 Medium)
- Total shared assumptions surfaced: 4 (UNSTATED: 3, STATED+UNSTATED-mixed: 1, CONTRADICTED: 0)
- Highest-severity items: C-001, C-002, C-003, C-004, X-001, X-002, U-001, U-002, U-004, A-001, A-004

**Convergence denominator** (`total_diff_points`): S(5) + C(5) + X(3) + A(4) = **17**.

**Similarity check**: 17 differences across 5 proposals = high diversity, NOT substantially identical. Proceed to debate (Step 2).
