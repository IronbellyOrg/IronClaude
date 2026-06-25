---
title: "sc:reflect UC-2 Runtime-Surface Reachability Escalation"
version: "1.0.0"
status: draft
feature_id: FR-RSR
parent_feature: sc-reflect-protocol
spec_type: new_feature
complexity_score: 0.85
complexity_class: HIGH
target_release: 4.4.0
authors: [user, claude]
created: 2026_06_19
quality_scores:
  clarity: 9.3
  completeness: 9.4
  testability: 9.5
  consistency: 9.4
  overall: 9.4
---

## 1. Problem Statement

`sc:reflect` UC-2 (post-execution audit) graded a release **PASS** where every leaf
mechanism existed and every unit test was green, but **nothing was wired into the
production entrypoint** — the user-facing feature was unreachable. A requirement
"user can reach `/ai` and invoke Spawn" (FR-S9-04) was marked PASS at Tier 1 citing
only the gate source plus its unit tests. The implementing symbols had referrers
**only** in test files and doc-comments; there was **no production caller**.

This is a structural blind spot, not a one-off misjudgement. The protocol's Tier-1
STOP rubric, its evidence chain, its coverage algorithm, and its deviation taxonomy
**all** independently fail to detect a complete-but-unintegrated feature, and they fail
in a mutually reinforcing way. Four load-bearing facts (adversarially confirmed at ~88%
confidence) explain why:

1. **The STOP rubric has no row for it.** SKILL.md §5.3 row 1 STOPs at a confident PASS
   when `C ≥ 0.90 AND S_scope ≤ 5 AND S_domains == 1 AND S_dev_density ≤ 0.05 AND
   coverage_pct ≥ floor` — *exactly* the signature of a small, clean, additive,
   well-tested but unwired leaf. The only structural escalation rows are 3 (Regression)
   and 3a (Reuse-Miss); there is **no row** for "claimed user surface with no production
   caller."
2. **The reachability signal is gathered but discarded.** §6.1 Wave-1A step 4 already
   runs `mcp__serena__find_referencing_symbols` (SKILL.md:463), but only for "downstream
   impact + signatures." It **never** partitions referrers into production-vs-test/comment
   to decide reachability.
3. **Coverage maps mapping, not reachability.** `refs/coverage-mapping.md` proves
   "requirement → task/diff mapping." An additive diff contradicts no mapping, so the
   matcher yields a clean STOP. Reachability is simply not in its value space.
4. **The taxonomy is the sink, and it has no class.** §10 is contradiction-anchored:
   §10.3 Drift needs an *unmapped hunk*; §10.4 Regression needs a *contradicted criterion*.
   Additive-only code triggers neither. So even if the signal were gathered, there is no
   class under which to file "complete-but-unintegrated."

**Framing correction (load-bearing for the whole design).** Production reachability is
**semi-decidable** — static analysis cannot *prove* reachability in the presence of
dynamic dispatch, plugin/registry wiring, reflection, and `console_scripts`-style
entrypoints. This feature therefore specifies a **zero-production-referrer ESCALATION**,
not a reachability *proof*. The single biggest risk is a fix bolted onto
`find_referencing_symbols` that **silently no-ops** on `backend: none` and on
dynamic/plugin/registry entrypoints (including this very repository's own
`[project.scripts]` console_scripts: `superclaude = superclaude.cli.main:main`,
`ic = superclaude.cli.ic:main`). The escalation MUST **fail loud** to a Grounding Gap
on every uncertainty, and MUST **never** silently downgrade a real finding nor silently
PASS an unwired one.

### 1.1 Evidence

| Evidence | Source | Impact |
|----------|--------|--------|
| FR-S9-04 ("user can reach `/ai` and invoke Spawn") graded PASS at Tier 1 with implementing symbols referenced only by tests + doc-comments | The motivating production incident (release audit) | User-facing feature shipped unreachable; audit declared 100% adherence |
| §5.3 row 1 STOP fires on `C≥0.90 ∧ S_scope≤5 ∧ S_domains==1 ∧ S_dev_density≤0.05 ∧ coverage_pct≥floor` | SKILL.md §5.3 (decision table, ~line 390) | Unwired-leaf signature is an exact STOP match — no escalation row exists |
| `find_referencing_symbols include_info:true` used "for downstream impact + signatures" only | SKILL.md §6.1 step 4 (~line 463) | The referrer set needed for reachability is fetched then thrown away |
| Coverage algorithm produces `coverage matrix`/`coverage_pct`/`unmapped_requirements` from requirement→task mapping only | `refs/coverage-mapping.md` (stages 1-5) | Additive diff contradicts no mapping → clean STOP; reachability not in value space |
| §10 taxonomy: Drift needs an unmapped hunk (§10.3), Regression needs a contradicted criterion (§10.4) | SKILL.md §10.3/§10.4; `refs/deviation-taxonomy.md` | Additive-only unwired code triggers neither class → no sink for the finding |
| This repo wires its CLI via `[project.scripts]` (`superclaude`, `ic`) — pure registry entrypoints with zero static callers | `pyproject.toml` lines 67-68 | A naive referrer-only sweep would false-flag idiomatic console_scripts wiring as UNREACHED |

### 1.2 Scope Boundary

**In scope**: A deterministic (LLM-free) user-reachable-surface **tagger** running in
§6.1 Wave-1A (UC-2 only); a production-caller **reachability sweep** extending the
existing `find_referencing_symbols` call; a concrete deterministic **degrade oracle** for
dynamic/registry/decorator/reflection wiring; an **entrypoint-rootwalk** to catch the
dead-production-caller false-negative; a **table-wide forbid-STOP pre-filter**
(`surface_unreached`) in §5.3; a **Reuse-Miss-style finding modifier** in §10 that maps
UNREACHED onto the existing 4 classes by evidence (no 5th class); additive §9.1 contract
fields and a `runtime-surface-ledger.yaml` artifact; a `contract_version` bump
1.5.0 → 1.6.0; reviewer-brief routing of the ledger as a grounding-hunk artifact-ref; and
new MAIN eval cases plus promotion of one falsifier-suite case to `status: active`.

**Out of scope**: UC-1 (pre-execution) reachability — the surface lives in UC-2 diff hunks,
not in a UC-1 tasklist. Whole-program call-graph construction or any reachability *proof*
(semi-decidable; explicitly rejected — see §7). Cross-language entrypoint resolution beyond
the deterministic degrade-oracle table (unknown languages DEGRADE, they are not analyzed).
Any change to UC-1 coverage semantics, the §10 4-class taxonomy count, or the exit-code-
sourced `verification_regressions_detected` field. Auto-remediation of UNREACHED findings
(reflect AUTHORS, never runs `/task` — the §"Will Not" invariant is preserved).

## 2. Solution Overview

Add a reachability-escalation capability to UC-2 that is **gathered, classified, and
gated** along the same three planes the blind spot spans — and that **fails loud** at every
seam where static analysis is undecidable.

1. **TAGGER (gather, deterministic).** A new Wave-1A (UC-2) step deterministically tags
   each diff-hunk-touching requirement as a *user-reachable surface* requirement, keyed off
   the hunk's symbol **kind** plus a surface-keyword/decorator allowlist. Emits
   `runtime_surface_requirements: [ids]`. LLM-free; zero cost on non-surface diffs.
2. **SWEEP (decide, evidence-producing).** A production-caller reachability sweep **extends
   the existing** `find_referencing_symbols` call (§6.1 step 4): it partitions referrers
   into production vs test/comment via a language→(test-marker, comment-syntax) table, then
   walks entrypoint roots. A tagged symbol with **zero surviving production referrers AND
   not an entrypoint** is UNREACHED. Writes `runtime-surface-ledger.yaml`.
3. **DEGRADE ORACLE (fail loud, deterministic table).** A concrete table mapping
   decorator-route / `[project.scripts]` / registry-DI-string-dispatch / reflection wiring
   to **degrade → Grounding Gap**, NEVER to a blocking Regression. Unknown language or
   comment-ambiguous referrers DEGRADE.
4. **ESCALATION (gate).** A **table-wide** forbid-STOP pre-filter `surface_unreached` added
   to §5.3 (alongside `coverage_degraded`), routing to Tier 2. Explicit pins
   (`--tier 1` / `--depth quick`) override loudly with `status: partial`.
5. **SINK (classify, no 5th class).** A Reuse-Miss-style finding **modifier** in §10 that
   maps UNREACHED onto the existing 4 classes **by evidence**, plus §10.6 Grounding Gap for
   the degraded/ambiguous case.
6. **CONTRACT (surface).** Six additive §9.1 fields + the ledger artifact;
   `contract_version` 1.5.0 → 1.6.0 (minor, additive-only).

Everything the existing protocol already does stays the same: the 4-class taxonomy count,
UC-1 coverage semantics, the verification triangle, the promotion gate's 9 conditions, and
the SRP boundary (Waves 0-6 read-only). The new sweep is read-only and lives entirely in
the Wave-1A grounding chain.

### 2.1 Key Design Decisions

| Decision | Choice | Alternatives Considered | Rationale |
|----------|--------|------------------------|-----------|
| Where the tagger runs | §6.1 **Wave-1A (UC-2)**, off diff-hunk symbol kind | "coverage-mapping Pass-1" | Coverage Pass-1 is UC-1 / Wave-1B; the reachable surface lives in **UC-2 diff hunks**, not a UC-1 spec. Putting it in coverage-mapping would mis-fire on the wrong mode and the wrong artifact. |
| Reachability vs escalation | **Zero-production-referrer ESCALATION** | Static reachability "proof" | Static reachability is **semi-decidable**; a "proof" would either over-claim (silent PASS on dynamic wiring) or over-block (false Regression on idiomatic registry wiring). Escalation + loud degrade is the only sound posture. |
| Sweep mechanism | **Extend** the existing `find_referencing_symbols` call (§6.1 step 4) | New standalone reachability agent | The referrer set is *already fetched* (SKILL.md:463) and discarded; partitioning it is a filter, not a new tool. Avoids agent-coordination cost and keeps fail-open inheritance. |
| Dead-production-caller false-negative | v1 **REQUIRES** an entrypoint-rootwalk | Referrer-partition only | A symbol called only by *other unreached production code* would falsely read REACHED on a referrer-only check. The rootwalk anchors REACHED to an actual entrypoint root. |
| Dynamic/registry wiring | **DEFAULT degrade → Grounding Gap**, never blocking Regression | Treat-as-production; treat-as-unreached | A false `UNREACHED → Regression` triggers unconditional T2+T3 + a TurnLedger rollback in the sprint consumer — net-negative if it false-fires on `@app.route` / `[project.scripts]` / registry wiring. Degrade is the asymmetric-cost-correct default. |
| Escalation shape | **Table-wide forbid-STOP pre-filter** | Plain inserted §5.3 row | §5.3 is first-match-wins; a plain row could be shadowed by row 1's earlier STOP. A pre-filter (the same shape as `coverage_degraded`) forbids ALL STOP rows when set. |
| Taxonomy sink | **Reuse-Miss-style finding modifier**, NO 5th class | New 5th deviation class | §17.7 Kill List item 6 rejected a 5th class for structural cleanliness; §10.8 Reuse-Miss is the established pattern for "maps onto the 4 by evidence." UNREACHED follows it exactly. |
| Regression counter hygiene | Increment ONLY `deviation_count_by_class.regression` | Also touch `verification_regressions_detected` | `verification_regressions_detected` is **exit-code-sourced** (§10.4 / step 5.5). An UNREACHED contradiction is evidence-sourced, not a verify exit — conflating them would corrupt the verified-regression count. |
| Contract bump | **1.5.0 → 1.6.0** (additive minor) | Major bump | All six new fields are purely additive; existing fields keep semantics; §9.4 minor rules + read-and-ignore forward-compat apply. |
| Eval placement | Companions in the **MAIN eval cases** (`evals/`); one falsifier promoted to `active` | All in falsifier-suite | Skeleton falsifier cases pass *vacuously* (structural-contract-only). The positive/negative companions must FAIL pre-change / PASS post-change against real fixtures — that is MAIN-case (`regex_absent` / `yaml_field`, D13 pattern) behaviour, not skeleton behaviour. |
| Downstream rollback coupling (Newman) | **Accept** that an UNREACHED-contradiction Regression triggers the sprint consumer's TurnLedger rollback | Add a separate non-rollback "unreached" signal; suppress rollback | Routing UNREACHED-contradiction to `deviation_count_by_class.regression` is the §10.9 by-evidence design; the sprint consumer (§9.3) already rolls back on `regression`. An unwired user-facing surface is exactly the kind of "should not have shipped" state rollback exists for. The coupling is intentional and stated (OQ-RSR.5 tracks revisiting it if false-fire data appears). |

### 2.2 Workflow / Data Flow

```
UC-2 post-execution audit
        │
Wave 1A (§6.1) ─── grounding chain (unchanged steps 1..7') ─────────────────────┐
        │                                                                        │
        ├── [NEW] TAGGER (step 4b'): for each diff hunk, kind + surface-keyword/  │
        │        decorator allowlist → runtime_surface_requirements:[ids]         │
        │        (LLM-free; emits nothing on non-surface diffs)                   │
        │                                                                         │
        └── step 4 find_referencing_symbols (already runs, SKILL.md:463) ─────────┤
                 │                                                                 │
                 ├── [NEW] SWEEP (step 4b): partition referrers                    │
                 │     production-vs-(test|comment) via lang→(marker,syntax) table │
                 │       │                                                         │
                 │       ├── ≥1 production referrer ........... REACHED            │
                 │       ├── 0 prod referrers ∧ entrypoint-rootwalk hit . REACHED  │
                 │       ├── 0 prod referrers ∧ no entrypoint ... UNREACHED        │
                 │       └── unknown lang | comment-ambiguous |                    │
                 │             dynamic/registry/decorator/reflection (oracle)      │
                 │                       .................... DEGRADE              │
                 │                                                                 │
                 └── writes runtime-surface-ledger.yaml ──────────────────────────┘
        │
        ▼
Wave 2 (§5.3 rubric): [NEW] table-wide forbid-STOP pre-filter `surface_unreached`
        │   UNREACHED≥1 → NO STOP row may fire → route Tier 2
        │   (pins --tier 1/--depth quick override → loud WARN + status:partial)
        ▼
Wave 5 synthesis: [NEW] §10 finding-modifier maps each UNREACHED by evidence
        │   contradiction → Regression (increment deviation_count_by_class.regression ONLY)
        │   unmapped     → Drift
        │   degraded/ambiguous → §10.6 Grounding Gap (needs_human_decision, status:partial)
        ▼
Contract: +runtime_surface_* (6 fields), contract_version 1.6.0
Reviewer brief (T2): runtime-surface-ledger.yaml routed as a grounding-hunk artifact-ref
```

### 2.3 Worked Scenario (the motivating FR-S9-04 case, before/after state trace)

> Given/When/Then trace proving the fix fires on the exact incident that motivated it.

```gherkin
Scenario: Unwired user surface is escalated instead of clean-passed
  GIVEN a UC-2 audit of a diff implementing FR-S9-04 ("user can reach /ai and invoke Spawn")
    AND the Spawn handler symbol is touched by a diff hunk whose kind/decorator matches
        the surface allowlist
    AND every referrer of the Spawn handler resolves to a test file or a doc-comment
    AND no [project.scripts]/route/registry entrypoint root reaches the Spawn handler

  # --- BEFORE (pre-change skill) ---
  WHEN reflect runs Wave 1A
   THEN no reachability signal is produced (find_referencing_symbols result discarded)
    AND C >= 0.90, S_scope <= 5, S_domains == 1, S_dev_density <= 0.05, coverage_pct >= floor
    AND §5.3 row 1 fires  -> STOP at Tier 1
    AND status: success, deviation_count_by_class.regression == 0     # the defect: clean PASS

  # --- AFTER (post-change skill) ---
  WHEN reflect runs Wave 1A with the tagger + sweep
   THEN runtime_surface_requirements == ["FR-S9-04"]                  # TAGGER
    AND the Spawn handler reduces to UNREACHED (test/comment-only referrers, no root) # SWEEP+ROOTWALK
    AND runtime_surface_unreached == 1  AND len(unreached_surfaces) == 1
    AND §5.3 forbid-STOP pre-filter `surface_unreached` blocks row 1  -> route Tier 2  # FR-RSR.5
    AND because FR-S9-04 is a contradicted acceptance criterion,
        §10.9 maps it to Regression: deviation_count_by_class.regression == 1          # FR-RSR.6
    AND verification_regressions_detected is UNCHANGED (evidence-sourced, not exit-sourced)
    AND status != success (no clean PASS); the finding ships in the deviation register
```

```gherkin
Scenario: Idiomatic dynamic wiring degrades loud, never false-Regression (degenerate variant)
  GIVEN a UC-2 audit of a diff adding a CLI command wired via [project.scripts]
        (e.g. `ic = superclaude.cli.ic:main`) with zero static callers
  WHEN reflect runs the tagger + sweep
   THEN the command symbol is tagged (surface allowlist match)
    AND the degrade oracle (FR-RSR.3) matches the [project.scripts] row -> status: DEGRADE
    AND runtime_surface_degraded == true  AND runtime_surface_unreached == 0
    AND a §10.6 Grounding Gap row is filed (needs_human_decision: true, status: partial)
    AND deviation_count_by_class.regression is UNCHANGED (NO false Regression)        # NFR-RSR.3
    AND the forbid-STOP pre-filter does NOT force Tier 2 (degrade-only; FR-RSR.5)
```

## 3. Functional Requirements

### FR-RSR.1: Deterministic runtime-surface requirement tagger (Wave-1A, UC-2)

**Description**: In UC-2 only, a new §6.1 Wave-1A step deterministically (LLM-free) tags
each requirement whose diff hunks touch a *user-reachable surface* symbol. The tag is keyed
off the hunk's symbol **kind** (from `get_symbols_overview` / `find_symbol`) plus a
**surface-keyword/decorator allowlist** (e.g. route/command/handler/endpoint decorators,
CLI command symbols, HTTP handler kinds). Emits `runtime_surface_requirements: [ids]`. The
tagger is **NOT** "coverage-mapping Pass-1" (that is UC-1 / Wave-1B); the reachable surface
lives in UC-2 diff hunks.

**Acceptance Criteria**:

- [ ] In UC-2, a diff hunk whose symbol kind/decorator matches the allowlist contributes its
      mapped requirement id(s) to `runtime_surface_requirements`.
- [ ] Tagging is deterministic: identical (diff + allowlist) inputs produce identical
      `runtime_surface_requirements` across runs (no LLM in the tagging path).
- [ ] A diff with **no** surface-matching hunks emits `runtime_surface_requirements: []`,
      `runtime_surface_sweep_ran: false`, and incurs **zero** additional MCP/tool cost
      beyond the existing chain (NFR-RSR.1).
- [ ] In UC-1 (`mode == pre`) the tagger never runs and emits no `runtime_surface_*` fields
      beyond their additive defaults.

**Symbol-anchored, not requirement-anchored (resolves the Wave-1A/1B sequencing hazard).**
The tagger is keyed off the **diff hunk's symbol** (resolved in Wave 1A), NOT off a
requirement id that may not yet be mapped. The requirement id is an *attribute* attached
when the UC-2 tasklist-vs-diff map (inline Wave 1B) is available; when a surface hunk has no
mapped requirement, the tagger still tags the **symbol** with `requirement_id: null` and the
sweep runs regardless. This is load-bearing: reachability must not depend on a requirement
mapping that is built later in the wave order, or an ordering quirk would emit `[]` by
sequencing and resurrect the original clean-pass bug. A `requirement_id: null` UNREACHED
finding maps to §10.3 Drift (unmapped) by FR-RSR.6, never silently dropped.

**Kind-resolution failure (fail loud).** If `get_symbols_overview`/`find_symbol` cannot
resolve a hunk's symbol kind (parse failure / `backend: none`), the hunk is **not** silently
skipped — it routes to `DEGRADE` (FR-RSR.3/8 → Grounding Gap), preserving the fail-loud
doctrine.

**Acceptance Criteria (additions):**

- [ ] A surface hunk with no mapped requirement is still tagged (`requirement_id: null`); the
      sweep runs and an UNREACHED verdict maps to Drift, never dropped by missing-id.
- [ ] A hunk whose symbol kind cannot be resolved routes to DEGRADE, not silent-skip.

**Dependencies**: §6.1 Wave-1A `get_symbols_overview` / `find_symbol` (symbol + kind, the
load-bearing input); the UC-2 inline Wave-1B tasklist-vs-diff map (supplies the *optional*
requirement-id attribute, never gates whether the sweep runs).

### FR-RSR.2: Production-caller reachability sweep (extends `find_referencing_symbols`)

**Description**: A reachability sweep **extends the existing** §6.1 step 4
`find_referencing_symbols` call. For each symbol implementing a `runtime_surface_requirements`
id, partition its referrers into **production** vs **test/comment** using a deterministic
language → (test-marker, comment-syntax) table. The table MUST catch inline test modules
(e.g. Rust `#[cfg(test)]`) and in-file `Test*` constructs, not only path-based test
detection. A symbol with **zero surviving production referrers AND not an entrypoint** is
`UNREACHED`. v1 **REQUIRES** the FR-RSR.4 entrypoint-rootwalk to be consulted before any
`UNREACHED` verdict (catches the dead-production-caller false-negative). The sweep writes
`runtime-surface-ledger.yaml` with one row per evaluated edge:
`{requirement_id, symbol, edge, status, production_referrers[], evidence_ref}`.

**Count semantics (resolves the edge-vs-symbol divergence).** The ledger is **per-edge**
(one row per `symbol → referrer-or-root` evaluation), but every *count* the contract and
gate consume is **per-symbol**, computed by reducing a symbol's edges to a single verdict
under the precedence `DEGRADE-on-any-incompleteness > UNREACHED > REACHED` (a symbol is
REACHED if **any** edge is REACHED; UNREACHED only if **all** edges are non-REACHED and
none degraded; DEGRADE if **any** edge degraded — see FR-RSR.3/FR-RSR.4). Therefore
`runtime_surface_unreached` is the count of **symbols** whose reduced verdict is UNREACHED
(never an edge count), and `len(unreached_surfaces) == runtime_surface_unreached` is an
invariant. A single symbol with N test-only referrers contributes N ledger rows but
exactly 1 to `runtime_surface_unreached`.

**Acceptance Criteria**:

- [ ] A tagged symbol whose only referrers are in test files / doc-comments / inline test
      modules (`#[cfg(test)]`, in-file `Test*`) is classified `UNREACHED`.
- [ ] A tagged symbol with ≥1 production (non-test, non-comment) referrer is `REACHED`.
- [ ] A tagged symbol with 0 production referrers but reachable from an entrypoint root
      (FR-RSR.4) is `REACHED`, not `UNREACHED`.
- [ ] UNKNOWN-language referrers OR comment-ambiguous referrers route to `DEGRADE`
      (per FR-RSR.3) — they are **never** treated as production.
- [ ] `runtime_surface_unreached` counts **symbols** (reduced per-symbol verdict), not edges;
      `len(unreached_surfaces) == runtime_surface_unreached` holds for every run.
- [ ] `runtime-surface-ledger.yaml` is written with the exact row schema above and its path
      emitted as `runtime_surface_ledger_path`.
- [ ] The sweep is **read-only** (Wave-1A; no repository mutation outside `<output>/`).

**Dependencies**: FR-RSR.1 (tags), §6.1 step 4 `find_referencing_symbols`, FR-RSR.3
(oracle), FR-RSR.4 (rootwalk).

### FR-RSR.3: Degrade oracle (concrete deterministic table; the highest-risk element)

**Description**: A concrete, deterministic table that maps wiring idioms that static
referrer analysis cannot resolve to **DEGRADE → §10.6 Grounding Gap**, NEVER to a blocking
Regression. The table MUST cover at minimum: (a) decorator routes (`@app.route`,
`@click.*` / Typer command decorators); (b) packaging entrypoints
(`pyproject [project.scripts]` / `[project.entry-points.*]` and equivalents); (c)
registry / dependency-injection / string-dispatch wiring; (d) reflection / dynamic import.
When a tagged symbol's reachability turns on any table row, the verdict is `DEGRADE` and the
finding is routed to §10.6, never to a blocking class.

**Acceptance Criteria**:

- [ ] Each of the four categories (a)-(d) is an explicit table row with a deterministic
      match predicate; matching any row yields `status: DEGRADE`.
- [ ] A symbol wired via `[project.scripts]` (e.g. this repo's
      `superclaude = superclaude.cli.main:main`) is `DEGRADE`, **never** `UNREACHED` and
      **never** Regression.
- [ ] A DEGRADE verdict produces a §10.6 Grounding Gap row and **never** increments
      `deviation_count_by_class.regression`.
- [ ] The oracle default for any reachability uncertainty is DEGRADE (fail loud), not a
      silent PASS and not a silent Regression.

**Dependencies**: FR-RSR.2 (sweep), §10.6 Grounding Gaps.

### FR-RSR.4: Entrypoint-rootwalk (dead-production-caller false-negative guard)

**Description**: Before emitting any `UNREACHED` verdict, the sweep MUST consult an
entrypoint-rootwalk: enumerate the project's entrypoint roots (CLI `[project.scripts]`,
declared web/app mount points, registered command surfaces, etc., per the FR-RSR.3 oracle's
entrypoint categories) and determine whether the tagged symbol is reachable from any root.
A symbol reachable from a root is `REACHED` even with zero direct production referrers
(its production callers are themselves reachable). When the rootwalk cannot be performed
(no enumerable roots / unknown wiring), the verdict DEGRADEs, it does not silently become
`UNREACHED`. **Partial enumeration is incompleteness:** if the rootwalk enumerates some
roots but any root throws, is skipped, or exceeds the OQ-RSR.3 depth bound before the symbol
is resolved, the verdict is `DEGRADE` (asymmetric-cost default — an UNREACHED verdict may
only be emitted when the rootwalk completed over the **full** enumerable root set without
finding the symbol).

**Acceptance Criteria**:

- [ ] A symbol with zero direct production referrers but reachable from an enumerated
      entrypoint root is `REACHED`.
- [ ] When entrypoint roots cannot be enumerated, the affected verdict is `DEGRADE`
      (Grounding Gap), not `UNREACHED`.
- [ ] **Partial** rootwalk enumeration (any root errors/skips, or the depth bound is hit
      before resolution) yields `DEGRADE`, never `UNREACHED`.
- [ ] The rootwalk is invoked on **every** candidate-`UNREACHED` verdict in v1 (mandatory,
      not opt-in).

**Dependencies**: FR-RSR.2, FR-RSR.3.

### FR-RSR.5: Table-wide forbid-STOP escalation pre-filter (`surface_unreached`)

**Description**: A new table-wide pre-filter `surface_unreached` is added to §5.3 alongside
`coverage_degraded`. When `runtime_surface_unreached ≥ 1`, **no** §5.3 STOP row (1, 2, or the
row-8 default) may fire; the run routes to Tier 2. This is **NOT** a plain inserted row —
§5.3 is first-match-wins and a plain row would be shadowed by row 1's earlier STOP. Explicit
user pins (`--tier 1`, `--depth quick`) override the pre-filter and proceed at the pinned
tier, but MUST emit a **loud WARN** naming the overridden flag AND set `status: partial`.

**Degrade-only runs do NOT escalate via this pre-filter (intentional).** The pre-filter
trigger is `runtime_surface_unreached ≥ 1` (decided UNREACHED symbols), NOT
`runtime_surface_degraded`. A diff whose tagged surfaces are **all** DEGRADE (the
`[project.scripts]` / dynamic-wiring case) yields `runtime_surface_unreached == 0` and does
**not** force Tier 2. This is sound, not a gap: every DEGRADE already files a §10.6 Grounding
Gap, which independently forces `status: partial` + `needs_human_decision: true` — so a
degrade-only run cannot clean-PASS, but it also does not pay the asymmetric T2 cost for a
finding that is, by construction, "could not decide" rather than "decided unreachable."

**Acceptance Criteria**:

- [ ] With `runtime_surface_unreached ≥ 1` and no pin, the run routes to Tier 2 regardless
      of which STOP row would otherwise have matched (including a confident row-1 PASS).
- [ ] A **degrade-only** run (`runtime_surface_unreached == 0 ∧ runtime_surface_degraded ==
      true`) does NOT force Tier 2 via this pre-filter, but its Grounding Gap still forces
      `status: partial` (no clean PASS).
- [ ] `tier_decision.yaml` records the forced-T2 with `surface_unreached` as the reason.
- [ ] `--tier 1` / `--depth quick` override the pre-filter, emit a WARN naming the flag, and
      force `status: partial`.
- [ ] The pre-filter never alters the coverage matrix and never blocks the run on its own
      (it routes tier; it does not STOP).

**Dependencies**: FR-RSR.2, §5.3 decision table.

### FR-RSR.6: §10 UNREACHED finding-modifier (maps by evidence; NO 5th class)

**Description**: A Reuse-Miss-style finding **modifier** (§10.8 pattern) maps each
`UNREACHED` finding onto the existing 4-class taxonomy **by evidence**. There is **NO** 5th
deviation class and **NO** `deviation_count_by_class.<new>` counter (consistent with §17.7
Kill List item 6). Mapping:

- UNREACHED that **contradicts** an acceptance criterion ("user can reach X") →
  **§10.4 Regression**, incrementing **ONLY** `deviation_count_by_class.regression` (NEVER
  `verification_regressions_detected`, which is exit-code-sourced).
- UNREACHED that is merely **unmapped** to any tasklist item → **§10.3 Drift**.
- UNREACHED that is **degraded / comment-ambiguous / oracle-routed** → **§10.6 Grounding
  Gap** (`needs_human_decision: true`, `status: partial`).

**Mapping precedence (resolves multi-signal collision).** The mapping inherits §10.5
precedence **Regression > Drift > Necessary > Authorized** by evidence: an UNREACHED finding
that is **both** contradiction AND unmapped is a **Regression** (contradiction wins;
mirroring §10.5's "rationale does not override a contradiction"). The DEGRADE → Grounding Gap
route is evidentiary, not a taxonomy class — a finding the oracle/rootwalk could not soundly
decide never reaches the Regression/Drift mapping at all (it has no decided UNREACHED verdict
to map). Thus the three branches are mutually exclusive and totally ordered: evaluate DEGRADE
first (no decided verdict → Grounding Gap), else contradiction → Regression, else → Drift.

**Acceptance Criteria**:

- [ ] An UNREACHED finding that contradicts a reachability acceptance criterion increments
      `deviation_count_by_class.regression` and leaves `verification_regressions_detected`
      unchanged.
- [ ] An UNREACHED finding with no tasklist mapping and no contradiction is classified Drift.
- [ ] A DEGRADE/ambiguous finding routes to §10.6 Grounding Gaps and forces `status: partial`
      + `needs_human_decision: true`; it never enters `deviation-ledger.yaml`.
- [ ] No 5th deviation class and no `reuse_miss`-style new counter is introduced; the
      taxonomy remains 4 classes.

**Dependencies**: §10.3, §10.4, §10.6, §10.8 pattern.

### FR-RSR.7: Additive contract fields + ledger artifact (`contract_version` 1.6.0)

**Description**: Six additive §9.1 stable-contract fields plus the ledger artifact are added;
`contract_version` bumps 1.5.0 → 1.6.0 (minor, additive-only). New fields:
`runtime_surface_requirements`, `runtime_surface_sweep_ran`, `runtime_surface_ledger_path`,
`runtime_surface_unreached`, `runtime_surface_degraded`, `unreached_surfaces[]`. No existing
field is renamed, removed, retyped, or has its semantics changed.

**No existing consumer load-bearing field changes (resolves §9.3 field-deletion-guard
interaction).** The six new fields are **advisory-only** for every existing §9.3 consumer
(one new advisory UC-2 row in §9.3 documents them). The one existing load-bearing field whose
*value* can now move is `deviation_count_by_class.regression` (sprint consumer) — but its
**semantics are unchanged**: it still means "a regression occurred." FR-RSR.6 only adds a new
evidence *source* (an UNREACHED contradiction) that feeds the same field with the same
meaning; this is not a rename/removal/retype/semantic-change, so it remains a **minor**
(additive) bump under §9.4. `verification_regressions_detected` is explicitly NOT touched
(it stays exit-code-sourced).

**Acceptance Criteria**:

- [ ] `contract_version` is `"1.6.0"` and the six new fields appear in
      `return-contract.yaml` with the §4.5 types/defaults.
- [ ] All pre-existing 1.5.0 fields keep identical names, types, and semantics
      (verified by an unchanged-fields assertion); `deviation_count_by_class.regression`
      retains its "a regression occurred" meaning (new evidence source, same semantics).
- [ ] `verification_regressions_detected` is never incremented by a reachability finding.
- [ ] Consumers that do not read the new fields are unaffected (read-and-ignore forward-
      compat; §9.4 minor rules).
- [ ] On a non-surface UC-2 diff and on every UC-1 run, the new fields take their inert
      defaults (`runtime_surface_sweep_ran: false`, `runtime_surface_unreached: 0`,
      `runtime_surface_degraded: false`, `unreached_surfaces: []`,
      `runtime_surface_ledger_path: null`, `runtime_surface_requirements: []`).

**Dependencies**: §9.1 contract, §9.4 evolution policy.

### FR-RSR.8: Fail-open on backend/tool unavailability

**Description**: When the reachability backend is unavailable (`backend: none`, Serena
unavailable, `find_referencing_symbols` fails, or the Wave-0 §0.5d availability surface
reports the chain degraded), the sweep DEGRADEs to a §10.6 Grounding Gap. It MUST **never**
STOP the skill and **never** silently PASS an untested surface. This inherits the §6.5
fail-open policy and adds `degraded_components += "runtime-surface:backend_unavailable"`.

**Acceptance Criteria**:

- [ ] `backend: none` → `runtime_surface_degraded: true`, a §10.6 Grounding Gap row, and the
      skill continues (no STOP).
- [ ] A `find_referencing_symbols` failure mid-sweep degrades that edge to Grounding Gap and
      records `degraded_components`.
- [ ] The skill never emits a clean PASS for a tagged surface whose reachability could not be
      evaluated.

**Dependencies**: §6.5 fail-open, §0.5d availability surface.

### FR-RSR.9: Reviewer-brief ledger routing (preserve "exactly three sections")

**Description**: When Tier 2 runs, `runtime-surface-ledger.yaml` is routed into the reviewer
brief as a **grounding-hunk artifact-ref** (the FR-4 verify-log pattern), filtered to the
`qa`-persona reviewer (who owns the coverage/acceptance surface). The artifact ref is
preserved verbatim for Wave-5 evidence-validator re-Read. This is an entry under the existing
`## Grounding hunks` section — **NOT** a fourth brief section; `reviewer-spec.md`'s "exactly
three sections" invariant is unchanged.

**Acceptance Criteria**:

- [ ] On a Tier-2 UC-2 run with a non-empty ledger, the qa-persona brief contains a
      `## Grounding hunks` entry referencing `<output>/artifacts/runtime-surface-ledger.yaml`.
- [ ] No reviewer brief gains a fourth top-level section (the three-section invariant holds).
- [ ] The artifact ref is byte-preserved so the evidence-validator can re-Read it.

**Dependencies**: `refs/reviewer-spec.md` brief template, §6.1 step 4.

### FR-RSR.10: Eval coverage (fail-before / pass-after, real fixtures)

**Description**: Ship eval cases that make the fix falsifiable. The headline case
`UC2-unwired-surface-passes` ships `status: active` with **real fixtures** (skeletons pass
vacuously) and MUST **FAIL pre-change / PASS post-change**. Four companion cases —
positive-control (genuinely-wired → REACHED, no escalation), dynamic-dispatch-not-false-
unreached (registry/decorator/`[project.scripts]` → Grounding Gap, never Regression),
degraded-backend → Grounding Gap, and test-only-reference → UNREACHED — go in the **MAIN
eval cases** (`evals/`, `regex_absent` / `yaml_field` D13 pattern), NOT the falsifier-suite.
The pre-existing falsifier cases (`T2-converges-on-wrong`, `T2-judge-class-collision`) MUST
still pass.

**Acceptance Criteria**:

- [ ] `UC2-unwired-surface-passes` is `status: active`, has real fixtures, FAILs against the
      pre-change skill and PASSes against the post-change skill.
- [ ] Companion cases (positive-control, dynamic-dispatch, degraded-backend, test-only) live
      under `evals/` and assert via `regex_absent` (no clean PASS) / `yaml_field`
      (`runtime_surface_unreached`, `runtime_surface_degraded`).
- [ ] The dynamic-dispatch companion asserts `DEGRADE`/Grounding Gap and asserts NO
      `deviation_count_by_class.regression` increment.
- [ ] Existing eval cases (`T2-convergence-wrong-answer`, `T2-judge-class-collision`, and the
      iteration-1 trio) still pass.
- [ ] At least one companion asserts the count invariant
      `len(unreached_surfaces) == runtime_surface_unreached` via `yaml_field` (Pass-1 fix).

**Dependencies**: `.dev/eval-workspaces/sc-reflect/`, `grader.py` (`regex_absent`,
`yaml_field`, `falsifier_skeleton_present`).

## 4. Architecture

### 4.1 New Files

| File | Purpose | Dependencies |
|------|---------|-------------|
| `src/superclaude/skills/sc-reflect-protocol/refs/runtime-surface.md` | Authoritative spec for the tagger allowlist, the language→(test-marker, comment-syntax) table, the degrade-oracle table, the rootwalk algorithm, and the `runtime-surface-ledger.yaml` schema | SKILL.md §6.1, §10.8 pattern |
| `<output>/artifacts/runtime-surface-ledger.yaml` (runtime artifact, per-run) | Per-edge reachability ledger `{requirement_id, symbol, edge, status, production_referrers[], evidence_ref}` | FR-RSR.2 sweep |
| `.dev/eval-workspaces/sc-reflect/evals/uc2-unwired-surface-passes/` (+ fixtures) | Headline active eval: unwired surface FAILs pre-change / PASSes post-change | grader.py |
| `.dev/eval-workspaces/sc-reflect/evals/uc2-surface-positive-control/` (+ fixtures) | Genuinely-wired surface → REACHED, no escalation | grader.py |
| `.dev/eval-workspaces/sc-reflect/evals/uc2-surface-dynamic-dispatch/` (+ fixtures) | Registry/decorator/`[project.scripts]` → Grounding Gap, never Regression | grader.py |
| `.dev/eval-workspaces/sc-reflect/evals/uc2-surface-degraded-backend/` (+ fixtures) | `backend: none` → Grounding Gap, no STOP | grader.py |
| `.dev/eval-workspaces/sc-reflect/evals/uc2-surface-test-only-ref/` (+ fixtures) | Referrers only in tests/comments → UNREACHED | grader.py |

### 4.2 Modified Files

| File | Change | Rationale |
|------|--------|-----------|
| `src/superclaude/skills/sc-reflect-protocol/SKILL.md` §6.1 | Add Wave-1A steps **4b'** (tagger, FR-RSR.1) and **4b** (sweep, FR-RSR.2-4) extending step 4; both UC-2-only, fail-open, one `audit.log` row each | Gather the discarded reachability signal |
| `SKILL.md` §5.3 + pre-filter precedence paragraph | Add `surface_unreached` to the table-wide forbid-STOP pre-filter set (FR-RSR.5) | First-match-wins table cannot host a plain row; pre-filter is the only correct shape |
| `SKILL.md` §5.4 `tier_decision.yaml` | Record `surface_unreached` as a forced-T2 reason | Audit visibility of the forced escalation |
| `SKILL.md` §10 (new §10.9 modifier) | Add UNREACHED finding-modifier mapping onto the 4 classes by evidence (FR-RSR.6); no 5th class | The taxonomy is the sink; modifier mirrors §10.8 Reuse-Miss |
| `SKILL.md` §9.1 stable contract | Add 6 additive fields; bump `contract_version` 1.5.0 → 1.6.0 (FR-RSR.7) | Surface the new signal additively |
| `SKILL.md` §9.3 Consumer Field Map | Add an advisory UC-2 consumer row for the new fields (non-gating) | §9.3 requires consumer rows for load-bearing fields |
| `src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md` | Add FR-RSR.9 ledger grounding-hunk entry (qa persona); preserve "exactly three sections" | Route the ledger to T2 reviewers without a 4th section |
| `src/superclaude/skills/sc-reflect-protocol/refs/deviation-taxonomy.md` | Cross-reference the §10.9 UNREACHED-by-evidence mapping | Keep the ref and SKILL.md in lockstep |
| `.dev/eval-workspaces/sc-reflect/cases/falsifier-suite/...` | Promote/author the relevant active companion per FR-RSR.10 (main cases primary) | Make the fix falsifiable with real fixtures |
| `.dev/eval-workspaces/sc-reflect/grader.py` | Ensure `regex_absent` / `yaml_field` cover the new fields (extend if needed) | Encode acceptance criteria as graded assertions |

### 4.4 Module Dependency Graph

```
                 §1B coverage hunk→requirement map
                              │
                FR-RSR.1 TAGGER (Wave-1A, UC-2)
                              │ runtime_surface_requirements:[ids]
                              ▼
   §6.1 step 4 find_referencing_symbols ──► FR-RSR.2 SWEEP
                              │                    │
                              │            ┌───────┴────────┐
                              │     FR-RSR.3 ORACLE   FR-RSR.4 ROOTWALK
                              │       (degrade)        (entrypoint roots)
                              │            └───────┬────────┘
                              ▼                    ▼
                     runtime-surface-ledger.yaml (status per edge)
                              │
            ┌─────────────────┼──────────────────────────┐
            ▼                 ▼                           ▼
  FR-RSR.5 §5.3 pre-filter  FR-RSR.6 §10.9 modifier   FR-RSR.7 contract 1.6.0
  (forbid-STOP → T2)        (Regression|Drift|Gap)    (+6 fields, +ledger path)
                              │
                              ▼ (T2 only)
                     FR-RSR.9 reviewer-brief grounding-hunk ref
                              │
                              ▼
                  FR-RSR.8 fail-open on backend/tool loss (§6.5)
```

### 4.5 Data Models

> New contract fields (additive to §9.1; `contract_version` 1.6.0) and the ledger row shape.

```python
# --- Additive §9.1 stable-contract fields (UC-2; inert defaults on UC-1 / non-surface) ---
# contract_version: "1.6.0"   # 1.5.0 + ADDITIVE ONLY (no rename/remove/retype/semantic change)

runtime_surface_requirements: list[str]      # FR-RSR.1: requirement ids tagged as user-reachable surface; [] when none
runtime_surface_sweep_ran: bool              # FR-RSR.2: true only when ≥1 tagged surface triggered the sweep (UC-2)
runtime_surface_ledger_path: str | None      # FR-RSR.2: abs path to <output>/artifacts/runtime-surface-ledger.yaml; null when sweep did not run
runtime_surface_unreached: int               # FR-RSR.2/6: count of UNREACHED symbols (reduced per-symbol verdict, NOT edges — see FR-RSR.2 count semantics; drives the §5.3 forbid-STOP pre-filter)
runtime_surface_degraded: bool               # FR-RSR.3/8: true when ≥1 symbol reduced to DEGRADE (oracle/unknown-lang/backend) → Grounding Gap
unreached_surfaces: list[dict]               # FR-RSR.6: per-UNREACHED detail (see UnreachedSurface below); [] when none

class UnreachedSurface(TypedDict):
    requirement_id: str | None               # the reachability requirement (e.g. "FR-S9-04"); null when the surface hunk had no mapped requirement (symbol-anchored, FR-RSR.1) → maps to §10.3 Drift
    symbol: str                              # symbol name-path with zero surviving production referrers
    mapped_class: Literal["regression", "drift", "grounding_gap"]  # §10.9 by-evidence mapping
    evidence_ref: str                        # resolves to the runtime-surface-ledger.yaml row for
                                             # regression/drift; resolves to the grounding-gaps.yaml row
                                             # for grounding_gap (same value space as the ledger row's
                                             # evidence_ref, repointed by mapped_class) — re-Read by the
                                             # Wave-5 evidence-validator. WRITE-ORDERING: the ledger is
                                             # written at Wave 1A (sweep); grounding-gaps.yaml at Wave 5
                                             # (synthesis). A grounding_gap evidence_ref is forward-declared
                                             # at sweep time and RESOLVED at synthesis — the contract field
                                             # is finalized in Wave 5, after both artifacts exist.

# --- runtime-surface-ledger.yaml: one row per evaluated edge (FR-RSR.2) ---
class RuntimeSurfaceLedgerRow(TypedDict):
    requirement_id: str | None               # null when the tagged surface hunk had no mapped requirement (symbol-anchored, FR-RSR.1)
    symbol: str                              # tagged surface symbol name-path
    edge: str                                # "<symbol> -> <referrer-or-entrypoint-root>"
    status: Literal["REACHED", "UNREACHED", "DEGRADE"]
    production_referrers: list[str]          # surviving non-test/non-comment referrer file:line refs ([] for UNREACHED)
    evidence_ref: str                        # file:line / artifact ref backing the verdict (re-Read by evidence-validator)
```

### 4.6 Implementation Order

```
1. refs/runtime-surface.md                        -- author allowlist + lang table + oracle table + rootwalk + ledger schema (source of truth for code-free behaviour)
2. SKILL.md §6.1 steps 4b' + 4b (tagger + sweep)  -- depends on 1; the gather plane
   SKILL.md §9.1 +6 fields, contract_version 1.6.0 -- [parallel with step 2] additive, no dependency on sweep internals
3. SKILL.md §5.3 forbid-STOP pre-filter + §5.4     -- depends on 2 (reads runtime_surface_unreached)
4. SKILL.md §10.9 finding-modifier + deviation-taxonomy.md xref -- depends on 2 (consumes ledger status)
5. refs/reviewer-spec.md ledger grounding-hunk ref -- depends on 2 (ledger path); [parallel with 3,4]
6. §9.3 consumer-field-map advisory row            -- depends on 2 (field names)
7. eval cases (1 active headline + 4 main companions) + grader assertions -- depends on 2-6; the falsifiability plane
8. make sync-dev && make verify-sync               -- depends on all SKILL.md/refs edits
```

## 5. Interface Contracts

### 5.1 CLI Surface

> This feature adds **no new CLI flags**. It activates automatically inside UC-2 (`--mode post`)
> via the Wave-1A sweep and is governed by existing pins. The rows below document the
> existing flags whose behaviour now interacts with the reachability pre-filter (FR-RSR.5).

```
# Reachability escalation is automatic in UC-2; no new flags. Existing pins interact:
/sc:reflect --mode post --diff <ref> [--tier 1 | --depth quick]
            # default (no pin): runtime_surface_unreached ≥ 1 forces Tier 2 (forbid-STOP pre-filter)
            # --tier 1 / --depth quick: override the pre-filter, emit loud WARN, force status: partial
            # --no-mcp / backend:none: sweep DEGRADEs → Grounding Gap (fail-open), never STOP
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--mode post` | enum | (mode-selected) | UC-2; the only mode in which the tagger + sweep run (FR-RSR.1). |
| `--tier 1` | pin | unset | Overrides the `surface_unreached` forbid-STOP pre-filter; emits a loud WARN naming the flag and forces `status: partial` (FR-RSR.5). |
| `--depth quick` | pin | unset | Same override semantics as `--tier 1` against the pre-filter (FR-RSR.5). |
| `--no-mcp` | flag | unset | Degrades the Serena backend; the sweep fails open to a §10.6 Grounding Gap (FR-RSR.8), never STOP. |

## 6. Non-Functional Requirements

| ID | Requirement | Target | Measurement |
|----|-------------|--------|-------------|
| NFR-RSR.1 | Zero added cost on non-surface diffs | 0 extra MCP/tool calls beyond the existing Wave-1A chain when `runtime_surface_requirements == []` | Telemetry: `runtime_surface_sweep_ran == false` ⇒ no `runtime-surface:*` audit rows; `uc2-surface-positive-control` companion asserts no sweep on a non-surface fixture |
| NFR-RSR.2 | Determinism of tagging + matching | Identical (diff + allowlist) inputs → identical `runtime_surface_requirements` and ledger statuses | Re-run eval fixture twice; assert byte-identical `runtime-surface-ledger.yaml` (LLM-free path) |
| NFR-RSR.3 | No false `UNREACHED → Regression` on idiomatic wiring | 0 Regression increments from `[project.scripts]` / decorator / registry wiring across the companion suite | `uc2-surface-dynamic-dispatch` asserts `runtime_surface_degraded: true` AND `deviation_count_by_class.regression` unchanged |
| NFR-RSR.4 | Additive contract compatibility | All pre-1.6.0 fields keep name/type/semantics; consumers read-and-ignore new fields | `make verify-sync` + an unchanged-fields grader assertion against the 1.5.0 field set |
| NFR-RSR.5 | Source-of-truth + sync discipline | Edit only `src/superclaude/`; `make sync-dev` then `make verify-sync` clean; UV-only | CI: `make verify-sync` passes; no `.claude/` mirror staged |
| NFR-RSR.6 | Fail-open availability | Backend/tool loss never STOPs and never silent-PASSes a tagged surface | `uc2-surface-degraded-backend` asserts Grounding Gap + skill-continues + no clean PASS |

## 7. Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Sweep silently no-ops on `backend: none` / dynamic wiring → reproduces the original blind spot | High | High | FR-RSR.3 oracle defaults uncertainty to **DEGRADE → Grounding Gap** (fail loud); FR-RSR.8 fail-open asserts no silent PASS; `uc2-surface-dynamic-dispatch` + `uc2-surface-degraded-backend` companions encode it |
| False `UNREACHED → Regression` on idiomatic `[project.scripts]`/decorator wiring triggers unconditional T2+T3 + TurnLedger rollback in the sprint consumer | Medium | High | Degrade oracle never maps wiring to Regression (NFR-RSR.3); dead-caller false-negative covered by the mandatory FR-RSR.4 rootwalk; companion asserts zero Regression increment |
| Plain §5.3 row gets shadowed by first-match-wins row 1 → escalation never fires | Medium | High | FR-RSR.5 uses a **table-wide forbid-STOP pre-filter** (proven `coverage_degraded` shape), not a row |
| Conflating UNREACHED Regression with verified-regression count corrupts `verification_regressions_detected` | Medium | Medium | FR-RSR.6 increments **only** `deviation_count_by_class.regression`; explicit acceptance criterion + grader assertion that `verification_regressions_detected` is unchanged |
| Skeleton eval cases pass vacuously → fix looks tested but isn't | Medium | High | FR-RSR.10 ships the headline case `status: active` with real fixtures + fail-before/pass-after; companions in MAIN `evals/`, not skeleton falsifier-suite |
| Reviewer brief gains a 4th section → breaks `reviewer-spec.md` invariant | Low | Medium | FR-RSR.9 routes the ledger as a grounding-hunk **entry** under the existing `## Grounding hunks`, asserted by the three-section invariant test |
| Unknown-language test/comment detection misfires → real test referrer counted as production | Medium | Medium | Lang→(marker,syntax) table; unknown language / comment-ambiguous → DEGRADE, never "treat as production" (FR-RSR.2 criterion) |

## 8. Test Plan

### 8.1 Unit Tests

| Test | File | Validates |
|------|------|-----------|
| `test_tagger_deterministic` | `.dev/eval-workspaces/sc-reflect/evals/uc2-unwired-surface-passes/` (fixture-driven via grader) | FR-RSR.1 deterministic surface tagging |
| `test_sweep_test_only_unreached` | `evals/uc2-surface-test-only-ref/` | FR-RSR.2 test/comment/inline-test referrers → UNREACHED |
| `test_positive_control_reached` | `evals/uc2-surface-positive-control/` | FR-RSR.2/4 production referrer / rootwalk → REACHED, no escalation |
| `test_dynamic_dispatch_degrade` | `evals/uc2-surface-dynamic-dispatch/` | FR-RSR.3 `[project.scripts]`/decorator/registry → DEGRADE, no Regression |
| `test_degraded_backend_gap` | `evals/uc2-surface-degraded-backend/` | FR-RSR.8 `backend: none` → Grounding Gap, no STOP |
| `test_contract_fields_additive` | grader unchanged-fields assertion | FR-RSR.7 `contract_version 1.6.0` + 6 additive fields + pre-1.6.0 fields intact |

### 8.2 Integration Tests

| Test | Validates |
|------|-----------|
| `uc2-unwired-surface-passes` (active, real fixtures) | End-to-end fail-before / pass-after: unwired surface → `runtime_surface_unreached ≥ 1` AND no clean PASS (`regex_absent` on a clean-pass marker) |
| Forbid-STOP escalation routing | FR-RSR.5: `tier_decision.yaml` shows forced T2 with reason `surface_unreached`; with `--tier 1`, override WARN + `status: partial` |
| §10.9 by-evidence mapping | FR-RSR.6: contradiction → `deviation_count_by_class.regression += 1` (and `verification_regressions_detected` unchanged); unmapped → Drift; degraded → Grounding Gap |
| Reviewer-brief ledger routing | FR-RSR.9: qa-persona brief carries the ledger grounding-hunk ref; three-section invariant holds |
| Regression-guard: existing cases | `T2-convergence-wrong-answer`, `T2-judge-class-collision`, and the iteration-1 trio still pass |

## 10. Downstream Inputs

### For sc:roadmap

Themes: **(T1) Gather** — Wave-1A tagger + sweep + oracle + rootwalk (FR-RSR.1-4);
**(T2) Gate** — §5.3 forbid-STOP pre-filter (FR-RSR.5); **(T3) Classify** — §10.9 by-evidence
finding-modifier (FR-RSR.6); **(T4) Surface** — additive contract 1.6.0 + ledger + reviewer
brief (FR-RSR.7, FR-RSR.9); **(T5) Falsify** — active headline eval + main companions
(FR-RSR.10). Milestone order = §4.6 implementation order; the source-of-truth ref
(`runtime-surface.md`) is the critical-path predecessor for everything else.

### For sc:tasklist

Each FR maps to one task. FR-RSR.3 (degrade oracle) and FR-RSR.4 (rootwalk) are the
highest-risk tasks and MUST land before any UNREACHED verdict is emittable (gate them as
blockers of FR-RSR.2's UNREACHED path). The contract task (FR-RSR.7) is parallelizable with
the sweep task. The eval task (FR-RSR.10) is terminal and is the acceptance gate: the
headline case must FAIL on the pre-change skill snapshot and PASS on the post-change skill.
Every SKILL.md/refs edit is followed by `make sync-dev` + `make verify-sync` (NFR-RSR.5);
UV-only for any Python (grader) work.

## 11. Open Items

| Item | Question | Impact | Resolution Target |
|------|----------|--------|-------------------|
| OQ-RSR.1 | Final surface-keyword/decorator allowlist contents (per-language) | Medium — under-broad allowlist misses surfaces; over-broad adds cost | Enumerate in `refs/runtime-surface.md` during implementation; validate against the companion fixtures |
| OQ-RSR.2 | Exact language→(test-marker, comment-syntax) table rows beyond py/rust/ts | Medium — unknown languages DEGRADE (safe) but coverage matters | Author py/rust/ts/js/go rows in v1; others DEGRADE until added |
| OQ-RSR.3 | Rootwalk depth bound for entrypoint reachability | Low — too-shallow misses transitive REACHED → over-DEGRADE (safe, not unsafe) | Pick a bounded depth (mirror the §4.0 link-following depth=1 convention) in `runtime-surface.md` |
| OQ-RSR.4 | Whether `runtime_surface_*` should feed `S_dev_density` as a parallel up-weight | Low — additive enrichment, not gating | Defer to a future iteration; v1 routes via the forbid-STOP pre-filter only |
| OQ-RSR.5 | Is a TurnLedger rollback the right sprint-consumer action for an UNREACHED-contradiction Regression (vs an unwired-but-not-broken signal)? | Medium — rollback is heavy; but unwired user surface is "should not ship" | v1 accepts the §10.9 by-evidence routing into `deviation_count_by_class.regression` (Newman §2.1 decision); revisit if iteration-2 telemetry shows false-fire rollbacks on idiomatic wiring |

## 12. Brainstorm Gap Analysis

| Gap ID | Description | Severity | Affected Section | Persona |
|--------|-------------|----------|-----------------|---------|
| G-RSR.1 | Degrade oracle is the highest-risk element; an incomplete table silently mis-classifies wiring | High | §3 FR-RSR.3 / §4.1 runtime-surface.md | architect |
| G-RSR.2 | Eval skeletons pass vacuously; without real fixtures the fix is unverified | High | §3 FR-RSR.10 / §8 | qa |
| G-RSR.3 | Regression-counter conflation could corrupt the exit-code-sourced verified-regression metric | Medium | §3 FR-RSR.6 | analyzer |

The fix is grounded in four mutually-reinforcing structural facts (§1), and each fix element
maps to exactly one of them: the tagger+sweep fix fact 2 (signal discarded), the forbid-STOP
pre-filter fixes fact 1 (no STOP row), the §10.9 modifier fixes fact 4 (no taxonomy sink),
and the deterministic-degrade posture fixes the semi-decidability framing correction. The
two HIGH gaps (degrade-oracle completeness, eval falsifiability) are the acceptance-critical
risks and are pinned to FR-RSR.3 and FR-RSR.10 respectively.

---

## Appendix A: Glossary

| Term | Definition |
|------|-----------|
| User-reachable surface | A symbol that constitutes a user-facing entry to a feature (CLI command, HTTP route handler, registered command) — what a reachability requirement like "user can reach X" refers to. |
| Production referrer | A referrer of a symbol that is NOT in a test file, doc-comment, or inline test module (`#[cfg(test)]`, in-file `Test*`). |
| UNREACHED | A tagged surface symbol with zero surviving production referrers AND not reachable from any entrypoint root (FR-RSR.2/4). |
| DEGRADE | A reachability verdict the sweep could not soundly decide (dynamic/registry/decorator/reflection wiring, unknown language, backend loss) → routed to §10.6 Grounding Gap, never a blocking class. |
| Entrypoint-rootwalk | Enumeration of project entrypoint roots (`[project.scripts]`, app mounts, command registries) to confirm reachability when direct production referrers are absent (FR-RSR.4). |
| Forbid-STOP pre-filter | A table-wide §5.3 flag (`surface_unreached`, like `coverage_degraded`) that forbids ALL STOP rows when set, forcing Tier 2 — not a first-match-wins row. |
| Finding-modifier | A §10.8-style mechanism that maps a finding onto the existing 4-class taxonomy by evidence, introducing NO 5th class and NO new counter. |

## Appendix B: Reference Documents

| Document | Relevance |
|----------|-----------|
| `src/superclaude/skills/sc-reflect-protocol/SKILL.md` §5.3, §6.1, §9.1, §10, §17.7 | Primary modification target; the four structural facts the fix addresses |
| `src/superclaude/skills/sc-reflect-protocol/refs/coverage-mapping.md` | Establishes that coverage proves mapping, not reachability (fact 3) |
| `src/superclaude/skills/sc-reflect-protocol/refs/deviation-taxonomy.md` | The contradiction-anchored taxonomy that is the missing sink (fact 4) |
| `src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md` | "Exactly three sections" invariant the ledger-routing FR must preserve (FR-RSR.9) |
| `src/superclaude/skills/sc-reflect-protocol/refs/grader-extensions.md` | `regex_absent` / `yaml_field` / `falsifier_skeleton_present` assertion types for the eval FRs |
| `pyproject.toml` (`[project.scripts]`: `superclaude`, `ic`) | Concrete in-repo registry entrypoints the degrade oracle MUST not false-flag (FR-RSR.3) |
| `.dev/eval-workspaces/sc-reflect/cases/falsifier-suite/` | Falsifier discipline; the dual-state skeleton/active lifecycle the eval FR follows |
