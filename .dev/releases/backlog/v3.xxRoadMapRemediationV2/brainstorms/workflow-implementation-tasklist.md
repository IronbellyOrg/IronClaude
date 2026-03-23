---
title: "MCP Integration Implementation Tasklist for sc-validate-roadmap-protocol"
source: "all-proposals-merged.md (post-adversarial)"
target_skill: "src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md"
target_command: "src/superclaude/commands/validate-roadmap.md"
executor: "/sc:task-unified"
date: "2026-03-23"
---

# Implementation Tasklist: MCP Integration for sc-validate-roadmap-protocol

## Proposal Triage

After adversarial review, 12 proposals yielded 9 actionable implementation items across 3 tiers. Three proposals were rejected or had their MCP dependency eliminated entirely.

### Tier 1 — No New Dependencies (use existing allowed-tools)

These implementations use only tools already in the skill's `allowed-tools` list. They can be implemented immediately with no architectural decisions required.

| ID | Source | Title | Tools | Phase |
|----|--------|-------|-------|-------|
| T1.1 | Auggie P2 | File Path Verification Pass | Glob, Bash | Phase 3 (Step 3.1b) |
| T1.2 | Serena I | Spec File Reference Verification | Glob | Phase 0 (Step 0.1.5) |
| T1.3 | Serena G | Taxonomy Seed via --prior-taxonomy flag | Read, Write | Phase 0.4 |
| T1.4 | Serena C (partial) | Pattern-Based Adversarial Scanning | Grep | Phase 4 (Steps 4.3a, 4.6a) |
| T1.5 | Serena E | Grep-Based Symbol Spot-Check | Grep | Phase 3 (Step 3.7, deep only) |

### Tier 2 — Auggie MCP Integration (optional, fail-open)

These require adding `auggie-mcp` as an optional MCP server. Orchestrator-only calls; no agent-level access.

| ID | Source | Title | Tools | Phase |
|----|--------|-------|-------|-------|
| T2.1 | Auggie P1 | Codebase-Grounded Requirement Enrichment | codebase-retrieval | Phase 0 (Step 0.2b) |
| T2.2 | Auggie P3 | Codebase-Grounded Remediation Plans | codebase-retrieval | Phase 5 (Step 5.1b) |

### Tier 3 — Serena MCP Integration (optional, fail-open)

These require adding Serena tools to `allowed-tools` and MCP server dependency. All fail-open.

| ID | Source | Title | Tools | Phase |
|----|--------|-------|-------|-------|
| T3.1 | Serena D | Cross-Session Validation Ledger | write_memory, read_memory | Pre-Phase 0, Post-Phase 6 |
| T3.2 | Serena F | Terminology Persistence + Pattern Log | write_memory, read_memory | Pre-Phase 0, Post-Phase 6 |
| T3.3 | Serena C (partial) | Cross-Session Adversarial Pattern Learning | write_memory, read_memory | Post-Phase 6 |
| T3.4 | Serena H | Symbol Context Supplement (deep only) | find_symbol, get_symbols_overview | Phase 0 (Step 0.5) |

### Rejected / Deferred

| Source | Title | Reason |
|--------|-------|--------|
| Serena B | Symbol-Aware Requirement Tracing (Phase 2.5) | Violates Section 8 boundary; refactored to separate companion skill `sc-validate-roadmap-symbols` — not in scope for this tasklist |
| Serena A | Cross-Session Requirement Caching | File-based caching achieves same result without Serena; add `--no-cache` flag as a follow-up |

---

## Implementation Order

Tasks are ordered by dependency chain and blast radius (following the skill's own R-phase model):

```
Wave 1: Tier 1 tasks (no new deps, immediate value)
  T1.2 → T1.1 → T1.3 → T1.4 → T1.5
  (Phase 0 additions first, then Phase 3, then Phase 4)

Wave 2: Tier 2 tasks (Auggie, after architectural decision on MCP servers)
  T2.1 → T2.2
  (Phase 0 enrichment before Phase 5 enrichment)

Wave 3: Tier 3 tasks (Serena, after allowed-tools decision)
  T3.1 → T3.2 → T3.3 → T3.4
  (Ledger infra first, then terminology, then pattern learning, then symbol supplement)
```

---

## Task Details

### T1.1 — File Path Verification Pass (Phase 3, Step 3.1b)

**Source**: Auggie Proposal 2 (adversarially refactored — Auggie dependency eliminated)

**What**: After collecting agent reports (Step 3.1), extract all file path references from agent reports and `00-requirement-universe.md`. Verify existence via `Glob`/`Bash`. Write an informational "File Path Verification Table" as an annotation block at the top of `02-unified-coverage-matrix.md`.

**Acceptance Criteria**:
- [ ] New Step 3.1b documented in SKILL.md Phase 3 section
- [ ] Path extraction regex covers `.py`, `.ts`, `.md`, `.yaml`, `.json`, `.toml`
- [ ] Status values: EXISTS, NOT_FOUND, POSSIBLY_MOVED
- [ ] Table is labeled "INFORMATIONAL ONLY — does not change coverage statuses"
- [ ] Depth-gated: skip at `quick`, exact-match at `standard`, relocation search at `deep`

**Effort**: SMALL

**Dependencies**: None

---

### T1.2 — Spec File Reference Verification (Phase 0, Step 0.1.5)

**Source**: Serena Proposal I (adversarially refactored — Serena dependency eliminated)

**What**: After reading all documents (Step 0.1), scan spec text for file path patterns in backtick/inline-code context. Use `Glob` to check existence. Write a "File Reference Status" section at the top of `00-requirement-universe.md`. Annotate requirements with `file_ref_stale: true` where applicable.

**Acceptance Criteria**:
- [ ] New Step 0.1.5 documented in SKILL.md Phase 0 section
- [ ] Scans for `.py`, `.ts`, `.md`, `.yaml`, `.json`, `.toml` in backtick/code context
- [ ] Tries exact path first, then basename-only Glob search
- [ ] Status values: FOUND (with resolved path), NOT FOUND (with source reference)
- [ ] Stale references annotated on affected requirements (informational only)
- [ ] No scoring changes, no adjudication rule modifications

**Effort**: SMALL

**Dependencies**: None

---

### T1.3 — Taxonomy Seed via --prior-taxonomy Flag (Phase 0.4)

**Source**: Serena Proposal G (adversarially refactored — Serena dependency eliminated)

**What**: Add `--prior-taxonomy <path>` flag. When provided, Phase 0.4 reads the prior `00-domain-taxonomy.md` as initial cluster centers. New requirements assigned by affinity. Dead domains pruned. Delta section appended.

**Acceptance Criteria**:
- [ ] New `--prior-taxonomy` flag added to SKILL.md Section 3 flags table
- [ ] New `--prior-taxonomy` flag added to command file flags table
- [ ] Phase 0.4 reads prior taxonomy when flag is set
- [ ] Cold-start algorithm runs unchanged when flag is absent
- [ ] Delta section appended to new taxonomy artifact showing what changed
- [ ] R3 compliance: seeded domains still require evidence-based requirement assignment

**Effort**: SMALL

**Dependencies**: None

---

### T1.4 — Pattern-Based Adversarial Scanning (Phase 4, Steps 4.3a, 4.6a)

**Source**: Serena Proposal C (adversarially refactored — core scanning uses Grep)

**What**: Add structured regex pattern scans to Phase 4 Steps 4.3 and 4.6 using Grep (already allowed).

**Enhancement 4.3a — Orphan Requirement Detection**:
```
Grep patterns against spec files:
1. Modal: (shall|must|required to|needs to) [^.]{10,80}
2. Negation: (must not|shall not|never|prohibited|forbidden) [^.]{10,80}
3. Quantitative NFRs: (at least|at most|within|maximum|minimum) \d+
4. Conditional: (if|when|unless) .{5,40} (must|shall|should)

For each match not in requirement universe → ADV finding (ORPHAN_REQUIREMENT)
Filter: skip first 20 lines of each file (preamble)
```

**Enhancement 4.6a — Assumption Detection**:
```
Grep patterns against roadmap:
1. Explicit: (assumes|assuming|given that|prerequisite|depends on)
2. Implicit: (existing|current|already|previously) .{5,40} (service|system|API|database|table|endpoint)

For each match where assumed capability not in spec → ADV finding (SILENT_ASSUMPTION)
```

**Acceptance Criteria**:
- [ ] Enhancement 4.3a added to SKILL.md Phase 4, Step 4.3
- [ ] Enhancement 4.6a added to SKILL.md Phase 4, Step 4.6
- [ ] Patterns documented with filtering rules
- [ ] Uses only Grep (no Serena dependency for core functionality)

**Effort**: SMALL

**Dependencies**: None

---

### T1.5 — Grep-Based Symbol Spot-Check (Phase 3, Step 3.7)

**Source**: Serena Proposal E (adversarially refactored — uses Grep instead of Serena)

**What**: At `--depth deep` only, enhance Phase 3 Step 3.7 Integration Wiring Audit. For each integration point with backtick-wrapped identifiers, Grep the codebase for symbol existence. Flag NOT_FOUND symbols; downgrade FULLY_WIRED to PARTIALLY_WIRED with LOW finding.

**Acceptance Criteria**:
- [ ] Symbol spot-check added to SKILL.md Phase 3, Step 3.7
- [ ] Gated behind `--depth deep` only
- [ ] Only checks backtick-wrapped identifiers with PascalCase/snake_case > 6 chars
- [ ] Uses Grep (no Serena dependency)
- [ ] NOT_FOUND produces LOW severity finding (informational)

**Effort**: SMALL

**Dependencies**: None

---

### T2.1 — Codebase-Grounded Requirement Enrichment (Phase 0, Step 0.2b)

**Source**: Auggie Proposal 1 (adversarially refactored)

**What**: Add optional Step 0.2b between Steps 0.2 and 0.3. Scan requirement universe for code references (backtick identifiers, file paths, code keywords). Query Auggie's `codebase-retrieval` for semantic context (callers, related tests). Annotate requirements with advisory `codebase_context` field.

**Acceptance Criteria**:
- [ ] New Step 0.2b documented in SKILL.md Phase 0 section
- [ ] Hard cap: maximum 15 Auggie calls
- [ ] `codebase_context` is advisory only — no new requirements generated
- [ ] No changes to coverage calculations or requirement universe count
- [ ] Graceful skip when Auggie unavailable or no code references found
- [ ] Prefer Grep/Glob for simple reference resolution; Auggie for semantic queries only
- [ ] `mcp-servers` in SKILL.md metadata updated to include `auggie` as optional
- [ ] Token cost acknowledged: 200-500 tokens per annotated requirement

**Effort**: MEDIUM

**Dependencies**: Architectural decision — add `auggie` to `mcp-servers` metadata

**Prerequisite Decision**: Should `mcp__auggie-mcp__codebase-retrieval` be added to `allowed-tools`? Adversarial review says NO — orchestrator already has MCP access; adding to `allowed-tools` would expose it to Phase 2 spawned agents.

---

### T2.2 — Codebase-Grounded Remediation Plans (Phase 5, Step 5.1b)

**Source**: Auggie Proposal 3 (adversarially refactored)

**What**: Add optional Step 5.1b between Step 5.1 (ordering) and Step 5.2 (patch checklist). For CRITICAL/HIGH gaps with concrete keywords, query Auggie for affected files/packages. Attach advisory `codebase_context` block to remediation entries.

**Acceptance Criteria**:
- [ ] New Step 5.1b documented in SKILL.md Phase 5 section
- [ ] Hard cap: maximum 10 Auggie queries
- [ ] Hard skip: NFR/CONSTRAINT-type gaps without file-level specificity excluded
- [ ] Bail-out: after 3 consecutive irrelevant results, abandon enrichment
- [ ] Prefer Grep/Glob for concrete keywords; Auggie for semantic queries
- [ ] Codebase context is advisory — existing heuristic effort levels unchanged
- [ ] No backward flow into Phase 3 metrics (R11 compliance)
- [ ] Graceful skip when Auggie unavailable

**Effort**: MEDIUM

**Dependencies**: T2.1 (same MCP server decision applies)

---

### T3.1 — Cross-Session Validation Ledger (Pre/Post-Phase hooks)

**Source**: Serena Proposal D (adversarially refactored)

**What**: Use Serena `write_memory`/`read_memory` to maintain a Validation Ledger across sessions. Pre-Phase 0 hook loads baseline. Post-Phase 6 hook writes ledger entry. Phase 3 Step 3.10 appends delta section (PERSISTENT/RESOLVED/NEW/REGRESSION).

**Acceptance Criteria**:
- [ ] Pre-Phase 0 hook documented: load baseline (fail-open)
- [ ] Post-Phase 6 hook documented: write ledger entry (fail-open)
- [ ] Delta section appended to consolidated report when baseline exists
- [ ] Gap status types: PERSISTENT, RESOLVED, NEW, REGRESSION
- [ ] REGRESSION findings auto-escalate severity by one level (display only, not adjudication)
- [ ] No adversarial calibration (cut by adversarial review)
- [ ] Ledger pruning: keep last 10 entries or 30 days
- [ ] Serena tools added to `allowed-tools` in frontmatter

**Effort**: MEDIUM

**Dependencies**: Architectural decision — add Serena to `allowed-tools`

---

### T3.2 — Terminology Persistence + Pattern Log (Pre/Post-Phase hooks)

**Source**: Serena Proposal F (adversarially refactored)

**What**: Pre-Phase 0 hook loads project terminology map from Serena memory (advisory context for extraction). Post-Phase 6 hook writes updated terminology + append-only pattern log (trend tracking for human review).

**Acceptance Criteria**:
- [ ] Pre-Phase 0 load: terminology map (fail-open, max 200 entries)
- [ ] Post-Phase 6 write: merge new glossary terms, persist (fail-open)
- [ ] Post-Phase 6 write: append pattern log entry (fail-open, last 20 entries)
- [ ] Terminology map is advisory — current spec always wins (R4)
- [ ] Pattern log is write-only — validator never reads it during execution
- [ ] Terms older than 90 days treated as lower-confidence hints
- [ ] Cross-project contamination prevention via project slug

**Effort**: SMALL

**Dependencies**: T3.1 (shares Serena infrastructure decision)

---

### T3.3 — Cross-Session Adversarial Pattern Learning (Post-Phase 6)

**Source**: Serena Proposal C (cross-session learning component)

**What**: After Phase 4, compute pattern effectiveness stats (hit count, false positive rate, severity distribution). Store via `write_memory`. On future runs, load ranked patterns and insert top performers before default patterns in Step 4.3a scan list.

**Acceptance Criteria**:
- [ ] Post-Phase 4 hook: compute and store pattern effectiveness stats
- [ ] Pre-Phase 4 hook: load historical patterns (fail-open)
- [ ] Top 20 patterns per project type retained
- [ ] Entries expire after 90 days
- [ ] Project-type segmentation for cross-project transfer
- [ ] `--serena` flag or auto-detection for opt-in

**Effort**: SMALL

**Dependencies**: T1.4 (patterns must exist first), T3.1 (Serena infrastructure)

---

### T3.4 — Symbol Context Supplement (Phase 0, Step 0.5, deep only)

**Source**: Serena Proposal H (adversarially refactored)

**What**: At `deep` depth only, after Phase 0.4, use `serena.find_symbol()` and `serena.get_symbols_overview()` to produce a supplemental artifact documenting structural context of code-referenced requirements. Informational only — not consumed by agents or scoring.

**Acceptance Criteria**:
- [ ] New Step 0.5 documented in SKILL.md (deep depth only)
- [ ] Output: `{OUTPUT_DIR}/00-symbol-context-supplement.md`
- [ ] Hard cap: 30 symbol lookups
- [ ] Does NOT modify requirement records or generate derived sub-requirements
- [ ] Referenced as background reading in Phase 4 (adversarial reviewer only)
- [ ] Failure is non-blocking: skip if Serena unavailable or no symbols found

**Effort**: MEDIUM

**Dependencies**: T3.1 (Serena infrastructure), Serena project activation

---

## Deferred Items (Not in Scope)

| Item | Rationale | Future Work |
|------|-----------|-------------|
| `sc-validate-roadmap-symbols` companion skill | Serena B was rejected as internal integration; create as separate skill | Separate tasklist when demand justifies |
| `--no-cache` flag + file-based caching | Serena A showed caching is useful but file-based suffices | Add to skill independently |
| Phase 1 decomposition caching | Depends on roadmap structure, not just specs — unsafe to cache | Research further |

---

## Summary

| Wave | Tasks | New Dependencies | Estimated Effort |
|------|-------|-----------------|-----------------|
| Wave 1 (Tier 1) | T1.1, T1.2, T1.3, T1.4, T1.5 | None | 5x SMALL |
| Wave 2 (Tier 2) | T2.1, T2.2 | Auggie MCP (optional) | 2x MEDIUM |
| Wave 3 (Tier 3) | T3.1, T3.2, T3.3, T3.4 | Serena MCP (optional) | 2x MEDIUM + 2x SMALL |

**Total**: 11 implementation tasks across 3 waves.
**Blocking decisions**: 2 (Auggie `allowed-tools` policy, Serena `allowed-tools` policy).
**No-dependency quick wins**: 5 tasks in Wave 1 can ship immediately.
