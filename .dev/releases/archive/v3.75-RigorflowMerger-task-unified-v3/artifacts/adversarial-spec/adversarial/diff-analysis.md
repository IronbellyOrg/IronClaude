# Diff Analysis: release-spec Comparison (3 variants)

## Metadata
- Generated: 2026-05-14
- Variants compared: 3 (Variant A, B, C — blind anonymization in effect)
- Total differences found: 38 (S: 6, C: 14, X: 7, U: 6, A: 5)
- Categories: structural (6), content (14), contradictions (7), unique (6), shared assumptions (5)
- Focus areas applied: surface, protocol, naming, deprecation, test-strategy, backward-compat
- Source: FINAL-REPORT.md (11 sections, 929 lines)

Anonymization: variant identities stripped per --blind. A/B/C labels are derived from input order only.

---

## Structural Differences

| # | Area | Variant A | Variant B | Variant C | Severity |
|---|------|-----------|-----------|-----------|----------|
| S-001 | Top-level section count | 10 sections (1 Identity → 10 Coverage) | 10 sections (same shape) | 10 sections (same shape) | Low |
| S-002 | Scope organization | §1 with 4 sub-bullets (in-scope, out-of-scope, split-rec, name/ver) | §1 with 4 sub-bullets (mirrors A) | §1 leads with explicit per-candidate decision-tree TABLE (§1.2) before scope lists | Medium |
| S-003 | Surface contract section (§2) | "Stays / Changes / Additions" three-way split + sprint additions §2.4 | "Stays / Changes / Additions / Breaks" four-way split (Breaks subsection is variant-specific) | "Stays / Changes / Additions" + surface diff block §2.4 (visual diff format) | Medium |
| S-004 | Protocol section depth (§3) | 5 subsections, all edits in single SKILL.md | 8 subsections, restructured skill into refs/rules/templates/config/scripts sub-tree | 6 subsections, single SKILL.md + sibling audit.py | Medium |
| S-005 | Naming & deprecation section (§4) | 4 subsections; "Nothing is deprecated" stance | 5 subsections; formal deprecation table for v3.75→v3.8 runway | 3 subsections; per-candidate per-deprecation runway table | Low |
| S-006 | Open questions table column count (§8) | 3 columns (Q, Recommendation, Status) | 3 columns (mirrors A) | 4 columns (Q, Recommendation, Status this release, Status this variant) | Low |

Severity rationale: All variants follow the same outer shape (10 numbered sections in roughly the same order). Differences are sub-section organization and granularity, not document-level restructuring.

---

## Content Differences

| # | Topic | Variant A approach | Variant B approach | Variant C approach | Severity |
|---|-------|--------------------|--------------------|--------------------|----------|
| C-001 | Scope of best-of-breed adoption | Subset: TU-001/003/004/007 + SE-001/004/005, SE-002/003 paired conditional, defer TU-002/005/006/SE-006 | Full slate: all TU-001..007 + SE-001..006 + Q1/Q2 renames with shim | Per-candidate decision tree; ADOPT=8, ADOPT-WITH-DEPRECATION=4, ADOPT-WITH-INVESTIGATION=1, ADOPT-WITH-MITIGATION=1, DEFER=6 | High |
| C-002 | TU-002 (output-type axis) decision | DEFER to follow-on release; rationale: invasive routing change, Q3 unresolved | ADOPT with full per-output-type gate tables in TU-005 SoT YAML; adds 9th CLI flag --output-type | DEFER-GATED on Q3 confirmation; explicit gating condition documented | High |
| C-003 | TU-005 (SoT YAML) decision | DEFER | ADOPT — full YAML schema published in §3.3 (~50 lines of YAML) | DEFER-COUPLED — bundles with TU-006 to R3 future release with explicit Q3/Q7/Q12 prerequisites | High |
| C-004 | TU-006 (skill sub-files) decision | DEFER | ADOPT — full directory tree published in §3.1 (refs/rules/templates/config/scripts/) | DEFER-COUPLED with TU-005 | High |
| C-005 | Q1 (sentinel rename) decision | DEFER verbatim; preserve `<!-- SC:TASK-UNIFIED:CLASSIFICATION -->` and add preservation tests in §5.3 | RENAME with shim runway (v3.75 emits new + accepts both, v3.8 removes old); gated on A-005 pre-merge | DEFER-GATED on A-005 investigation; future R3 with shim; preservation in this release | High |
| C-006 | Q2 (forensic-caller rename) decision | DEFER verbatim with preservation test | RENAME with shim runway | DEFER-GATED on A-005; same shape as C-005 | High |
| C-007 | Release-split shape (Q8 commitment) | 2-release: R1 (task-surface) + R2 (sprint+TUI); R3 punted to "future" without explicit commitment | 3-release: R1 (rigor) + R2 (sprint+TUI) + R3 (structural consolidation: TU-002/005/006/Q1/Q2) | 2-release immediate (R1+R2) + R3 (deferred bundle) + R4 (SE-006); R3/R4 explicitly planned with named investigations | Medium |
| C-008 | SE-006 (auto-diagnostic threshold) | DEFER | ADOPT in this release | DEFER-GATED on RK-OOS-3 diagnostic-chain hardening | High |
| C-009 | Audit log infrastructure (Q11) | Lightweight: single append-only line per STRICT task | New `audit.py` module; daily-rotated JSONL; comprehensive schema | Same `audit.py`/JSONL schema as B; explicitly justified as future Q1/Q2 telemetry de-risker | Medium |
| C-010 | TU-007 six-condition list | Known-gap noted; six-condition placeholder list published with "must verify before merge" implementation note | Same placeholder; additionally adds script-side check `validate_classification.py` to assert LW-source citation | Treated as ADOPT-WITH-INVESTIGATION; pre-merge investigation produces canonical list; tests parameterize over investigation output | Medium |
| C-011 | Keyword reconciliation (Q12) | DEFER (TU-005 deferred) | ADOPT — STRICT widens to include `password, credential, secret, jwt, transaction, query`; LIGHT and STANDARD compounds widen | DEFER-GATED on Q12 confirmation (gates with TU-005) | High |
| C-012 | New CLI flags added this release | Zero new flags | One new flag `--output-type` | Zero new flags | Medium |
| C-013 | Version bump | 2.0.0 → 2.1.0 (minor; behavioral changes gated) | 2.0.0 → 3.0.0 (major; signals breaking changes) | 2.0.0 → 2.2.0 (minor; behavioral break gated by runway/migration guide) | Medium |
| C-014 | Migration guide requirement | Release notes "Behavior changes that may surprise users" subsection + "Known telemetry-compat carry-overs" subsection | Formal `MIGRATION-v3.75-to-v3.8.md` document | Formal `docs/migration/v3.75.md` with one entry per ADOPT-WITH-DEPRECATION candidate | Low |

Severity rationale: C-001 through C-008 + C-011 are the substantive divergence axes (what does this release ship?). C-009/C-010/C-012/C-013/C-014 are policy-implementation details.

---

## Contradictions

| # | Point of Conflict | Variant A position | Variant B position | Variant C position | Impact |
|---|-------------------|--------------------|--------------------|--------------------|--------|
| X-001 | Should TU-002 ship in v3.75? | NO — invasive, defer (V-A §1.2 "TU-002 ... DEFERRED to follow-on") | YES — full output-type axis with gate tables (V-B §2.3 + §3.6) | NO — DEFER-GATED on Q3 (V-C §1.2 table row TU-002) | High — fundamentally different release scope |
| X-002 | Should Q1+Q2 renames ship in v3.75? | NO — preserve carry-overs (V-A §4.2 "explicitly preserves") | YES — rename with shim runway (V-B §4.2/§4.3) | NO — DEFER-GATED on A-005 (V-C §1.2 + §8.2) | High — different deprecation policy |
| X-003 | Should TU-005 SoT YAML ship in v3.75? | NO — defer (V-A §1.2) | YES — full YAML schema in §3.3 | NO — DEFER-COUPLED with TU-006 (V-C §1.2) | High — different scope policy |
| X-004 | Should the release introduce ANY breaking changes? | NO — "Zero breaking changes" (V-A §10 variant signature) | YES — breaking changes accepted under runway discipline (V-B §10 variant signature + §2.4 Breaks subsection) | YES, but limited to ADOPT-WITH-DEPRECATION candidates only (V-C §6.2) | High — different philosophical stance on breakage |
| X-005 | Should the release add a new CLI flag? | NO — flag surface unchanged (V-A §2.1) | YES — `--output-type {code\|analysis\|documentation\|opinion\|auto}` (V-B §2.3) | NO — no new flags (V-C §6.1) | Medium — surface stability vs. completeness |
| X-006 | Should SE-006 (auto-diagnostic threshold) ship now? | NO — defer (V-A §1.2) | YES — adopted (V-B §1.2 + §2.3) | NO — DEFER-GATED on RK-OOS-3 (V-C §1.2 + §8.2) | Medium |
| X-007 | Should the release-split shape have 2 or 3 releases? | 2 releases this v3.75 (R1+R2); future cleanup punted without explicit timeline | 3 releases proposed (R1+R2+R3), with R3 effort 5-7 days estimated | 2 releases this v3.75 (R1+R2) + future R3 (deferred bundle) + future R4 (SE-006); R3/R4 explicitly planned with named investigations | Medium — different commitment to future work |

**Cross-checking note (intra-variant):** No intra-variant contradictions detected. All three variants are internally consistent.

---

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | A | Telemetry-compat preservation tests (§5.3) that **assert** the carry-over strings remain present in the codebase — encoding the DEFER decision in CI. | Medium — interesting CI pattern; useful for ensuring carry-overs don't get incidentally removed. |
| U-002 | B | Full YAML schema for `config/tier-keywords.yaml` (~50 lines, §3.3) including consolidated STRICT keywords, output-type gate tables, confidence thresholds, priority order. | High — concrete artifact; if R3 ever runs, this is the starting point. |
| U-003 | B | Full skill sub-directory tree spec (§3.1) including `refs/`, `rules/`, `templates/`, `config/`, `scripts/` with file-by-file purpose. | Medium — concrete artifact; resolves SKILL.md:359-365 broken references. |
| U-004 | B | Explicit RK-U-1..6 new-risks table (§6.3) covering keyword widening telemetry spike, YAML-load brittleness, A-005 dependency, and ordering of TU-002/005/006 PRs. | Medium — surfaces risks the surgical and contingent variants don't enumerate. |
| U-005 | C | Per-candidate decision tree with three explicit dimensions (coupling, break, gate) producing five verdict categories (ADOPT, ADOPT-WITH-DEPRECATION, ADOPT-WITH-INVESTIGATION, ADOPT-WITH-MITIGATION, DEFER-GATED, DEFER-COUPLED). | High — methodological contribution; provides a re-runnable decision framework for future releases. |
| U-006 | C | Backlog-task creation requirement in §9 acceptance criteria (A-005, Q3 confirmation, RK-OOS-3) committing the project to the future R3+R4 releases. | High — addresses the "infinite defer" risk; turns soft deferrals into tracked backlog. |

---

## Shared Assumptions

A-001 through A-005 are UNSTATED preconditions all three variants share without surfacing.

| # | Assumption | Source Agreement | Impact | Status |
|---|------------|------------------|--------|--------|
| A-001 | All three variants assume the FINAL-REPORT's candidate set (TU-001..007, SE-001..006, TUI P-01..P-10) is closed — none propose novel candidates not surfaced by Wave-1 extracts. | C-001 + §6 candidate inventory | Medium — limits inventive scope of any single variant | UNSTATED |
| A-002 | All variants treat `/sc:task` canonical-only as a non-negotiable hard constraint; no variant entertains a hypothetical where a future release could resurrect `/sc:task-unified` as a sibling command. | §4.1 in all three | Low — this is a real v3.7 hard constraint, but the assumption that no future release will ever reverse it is unstated. | UNSTATED |
| A-003 | All variants assume FINAL-REPORT's effort labels (S/M/L) and value/tractability ratings are reliable proxies for actual engineering cost; none propose an independent re-estimation. | §6.3 ranking in all three | Medium — sizing risk inherited from FINAL-REPORT A-003 (same assumption surfaced there) | UNSTATED — inherited from FINAL-REPORT §10 A-003 |
| A-004 | All variants assume the audit log infrastructure is a uniform "append-only JSON, daily-rotated" pattern; none propose alternative telemetry backends (e.g., structured event bus). | §3.7-§3.8 audit log specs in B+C; §2.3 in A | Low — append-only JSONL is widely-applicable but unstated as a design choice. | UNSTATED |
| A-005 | All variants assume that the TU-007 six-condition completion checklist exists somewhere in the original LW source and can be verified pre-merge; none propose what to do if the LW source contains a different number of conditions (5, 7, 8). | §3.3-§3.6 TU-007 specs | Medium — the entire TU-007 candidate could shift if the LW source diverges materially. C makes this least-brittle (parameterized tests over investigation output). | UNSTATED |

**Action:** A-001..A-005 are documented but **do not block** the release. A-005 is partially mitigated by Variant C's parameterized-test approach (U-005). A-003 is inherited from FINAL-REPORT and acknowledged as a known limitation.

---

## Summary

- Total structural differences: 6 (all Low-Medium severity; variants share overall shape)
- Total content differences: 14 (8 High severity, 5 Medium, 1 Low)
- Total contradictions: 7 (5 High severity, 2 Medium)
- Total unique contributions: 6 (3 High value, 3 Medium value)
- Total shared assumptions: 5 (UNSTATED; promoted to A-NNN diff points)

**Highest-severity items:** C-001 through C-006, C-008, C-011 (content-level scope decisions); X-001 through X-004 (contradictions on TU-002/Q1Q2/TU-005/breaking-change-philosophy); U-002, U-005, U-006 (high-value unique contributions).

**Convergence pre-debate:** ~35% (rough estimate of pre-debate diff-point agreement, before round-1 advocates can argue for convergence). The three variants disagree on the **scope** of this release more than the **shape** of what they ship.

**Debate priorities (focus areas mapping):**
- surface: C-005, C-006, C-012 (Q1/Q2/new-flag)
- protocol: S-004, C-001..C-004 (skill restructure, TU candidate adoption)
- naming: C-005, C-006, X-002 (Q1/Q2 renames)
- deprecation: C-007, C-013, X-004 (release-split, version bump, breaking-change philosophy)
- test-strategy: C-010, C-014 (TU-007 LW verification, migration guide)
- backward-compat: X-002, X-004 (carry-over preservation vs. rename, zero-break vs. runway-break)

Total diff points (for convergence denominator): 6 (S) + 14 (C) + 7 (X) + 6 (U) + 5 (A) = **38**.
