# Refactoring Plan — merge to unified findings card (shadow15)

## Overview

- Base variant: V2 (qa/haiku) — combined score 0.816
- Incorporated variants: V1 (analyzer/sonnet, 2 findings + family framing), V3 (refactorer/opus, 1 finding + 1 reduced-scope finding)
- Changes planned: 7 (4 incorporations, 2 re-scopes of base claims, 1 structural reorganization into family grouping)
- Changes rejected: 4 (the refuted findings/clauses)
- Overall risk: Low (additive merge of verified findings; no claim rewritten beyond debate-adjudicated re-scopes)

## Planned Changes

| # | Change | Source | Target in base | Integration | Rationale (debate evidence) | Risk |
|---|--------|--------|----------------|-------------|------------------------------|------|
| 1 | Add V1-F1 (R7 symbolsOnly file-mode ban has no AC) as the lead instance of a "constraint without matching AC" family | V1 F1 | New finding (family head) after base F4 | insert | C-001 winner 85%; corroborated independently by V2-F2's clause from a different model class (Round 1, V2 steelman of V1); t1-card H1 names the recurrence family | Low |
| 2 | Add V1-F3 (R2 `access: mcp` half-gate absent from every AC) as third family instance | V1 F3 | Family grouping | insert | C-005 winner 85%; verified — R2 source.md:12 carries the gate, Task 1/2 ACs name only `index_state: fresh`, execution commit 7764bb623 had the in-file wording (git) | Low |
| 3 | Re-scope base F1: drop "no visible matrix row" clause (refuted by t1-card INF-012), keep AC-level gap for §2.4 items 3/6 as a family sub-clause | V2 F1 (modified) | Family grouping | restructure | X-002: full matrix maps source.md:38-46→Task 1; brief showed only the excerpt (vantage artifact). Conceded by V2 advocate Round 1 | Low |
| 4 | Unbundle base F2: drop return-contract clause (X-004, transitively gated by Task 2 AC2 byte-identity over `## Unattended mode`), merge symbolsOnly/wildcard clause into family head (Change 1), keep 25-line cap residue as family sub-clause | V2 F2 (modified) | Family grouping | restructure | X-004 80%; INV-002 guard check confirmed the transitive gating before dropping | Low |
| 5 | Keep base F3 and F4 (unpassable-check pair) verbatim as base-authored findings | V2 F3, F4 | Unchanged base body | keep | C-004 winner 90%; unanimous adoption (Round 2 all advocates) | Low |
| 6 | Add V3-F1 (guide §7 "only section that names these" vs analyze.md:68 verb restatement — two-site rule) as the sole shipped-artifact finding | V3 F1 | New section after family findings | insert | C-006 winner 75%; verified at both HEAD and 7764bb623 (clause predates PR #513) | Low |
| 7 | Add V3-F3 at reduced scope (Leads bullet ~4→6 rules, dense, duplicates guide §3/§5; density attributable to this package, the `graph:empty`/`graph:unresolved` tail is PR #513's) as MINOR, confidence 0.55 | V3 F3 (modified) | New section, last finding | insert | Round 2 V2 rebuttal + V3 concession; verified against 7764bb623 text | Low |

Structural note: the merged card presents the family findings (Changes 1-4) as one grouped finding set with per-clause citations plus the two standalone findings, rather than six independent rows — per Round 2 V1 rebuttal (family framing) adopted by all advocates.

## Changes NOT Being Made

| Diff point | Rejected approach | Rationale (debate evidence) |
|------------|-------------------|------------------------------|
| C-003 / X-001 | V1-F2's "mild unplanned elaboration" finding (Discover `path` param, symbolsOnly on main files, search-only-when-symbol) | Refuted by git: 7764bb623 Discover matched the tasklist verbatim; all three elaborations landed in 930c5ebc8 (PR #513, separate package). Recorded in merged card as post-execution evolution, out of audit scope. V1 advocate conceded Round 1 |
| X-003 | V3-F2's 60s-wait unconditional restatement finding | Same git evidence: clause did not exist at 7764bb623; and at HEAD the text carries "(guide step 3)" pointing at the conditioning section. V3 advocate conceded Round 1 |
| X-002 (full rejection of V2-F1) | Rejecting the whole finding rather than re-scoping | The AC-level half survives: no tasklist AC greps for "leads, never citations" or the subagent state hand-off even though Task 1 body carries both. Re-scope, not drop |
| S-002 | Treating findings count as a quality signal | Debate consensus: count is noise; one card's 4 findings included a bundle (V2-F2) that split 3 ways |

## Risk Summary

All changes are Low risk: additive inserts of debate-verified findings plus two adjudicated re-scopes already conceded by their own advocates. No base finding is rewritten beyond the two re-scopes (Changes 3, 4). Rollback = revert to variant-2-original.md (preserved in this directory).

## Review Status

Auto-approved (non-interactive invocation). Timestamp: 2026-11-13T03:0x Z (session time).
