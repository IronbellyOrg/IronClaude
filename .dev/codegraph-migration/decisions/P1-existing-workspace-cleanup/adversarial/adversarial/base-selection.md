# Base Selection Report

Variants scored as written (the original option files, `variant-{1,2,3}-original.md`), not as amended in debate. Debate amendments enter through the refactor plan.

## Quantitative Scoring (50% weight)

Requirement set (no formal IDs in the source, so section-level topics from `context.md:3-5`, 12 items): R1 `./update.sh` path cleans existing workspaces; R2 fresh `superclaude install` leaves nothing; R3 binary registration; R4 MCP entry; R5 permission; R6 companion skill/agent/hook; R7 `CLAUDE.md` mention; R8 docs reference; R9 Coder/upstream-uninstaller leftovers handed off; R10 exact user scope only; R11 never touch unrelated/same-named project/local entries; R12 decide indexes/memories kept or deleted.

| Metric | Weight | Variant 1 (A) | Variant 2 (B) | Variant 3 (C) |
|--------|--------|---------------|---------------|---------------|
| requirement_coverage | 0.30 | 0.83 (10/12; misses R5, R8) | 0.58 (7/12; R1,R3,R4,R6,R9,R10,R12) | 0.67 (8/12; R1,R2,R3,R4,R8,R9,R10,R11) |
| internal_consistency | 0.25 | 0.95 (1/20: "identified by exact shape" vs basename/substring matcher) | 0.93 (1/15: "IronClaude-provable" vs no-proof uv tool) | 1.00 (0/12) |
| specificity_ratio | 0.15 | 0.90 | 0.85 ("Optionally", "may exceed") | 0.75 ("shape-matched" undefined, "Docs tell") |
| dependency_completeness | 0.15 | 1.00 | 0.80 (defined as "Everything in Option A", unresolved within the document) | 1.00 |
| section_coverage | 0.15 | 1.00 (3 H2) | 1.00 (3 H2) | 1.00 (3 H2) |
| **quant_score** | | **0.92** | **0.80** | **0.86** |

## Qualitative Scoring (50% weight) — Additive Binary Rubric

CEV evidence is abbreviated to the decisive quote/section. "NOT MET" means no qualifying evidence found in the variant text.

### Completeness (5 criteria)

| Criterion | V1 (A) | Evidence | V2 (B) | Evidence | V3 (C) | Evidence |
|-----------|--------|----------|--------|----------|--------|----------|
| All explicit requirements | NOT MET | permission, docs absent | NOT MET | R2, R5, R7, R8 absent | NOT MET | R5-R7 absent |
| Edge cases/failures | MET | step 6 non-fatal, missing CLI, different-shape entry | MET | step 4 "Non-fatal ... bounded timeouts" | NOT MET | no failure handling stated |
| Dependencies/prerequisites | MET | reuses `read_user_mcp_entry`, Claude CLI | MET | receipt + sha256, `uv tool list` | MET | step 4 depends on Coder handoff |
| Success criteria | MET | "re-reads to verify absence"; "Meets the goal on both paths" | NOT MET | only "fully clean" | NOT MET | none |
| Out of scope | MET | step 4 never-touch list | MET | "External binaries ... never touched"; data kept | MET | "prints the manual commands for binaries, uv tools and data" |
| **Subtotal** | **4/5** | | **3/5** | | **2/5** | |

### Correctness (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|-----------|----|----------|----|----------|----|----------|
| No factual errors | NOT MET | "only removes entries IronClaude or Coder wrote" false for basename/substring matches; misses older IronClaude shape (git 0e7bc31f) | NOT MET | "upstream uninstall 60 s" vs `INSTALL_TIMEOUT = 300` (`install_codebase_memory.py:28`) | NOT MET | "existing consent rule for every removal" contradicted by `install_mcp.py:874-883` |
| Feasible with constraints | MET | 2 reads, <= 2 short CLI calls within 60 s | NOT MET | 60 s + 30 s exceeds Coder's 60 s | MET | adds nothing to install |
| Consistent terminology | MET | | MET | | MET | |
| No internal contradictions | NOT MET | "exact shape" vs basename matcher | NOT MET | "IronClaude-provable" vs uv tool with no proof | MET | none found |
| Claims supported | MET | cites helpers, `install_plugins` pattern | MET | cites `install_mcp.py:981-986` | NOT MET | no citations |
| **Subtotal** | **3/5** | | **2/5** | | **3/5** | |

### Structure (5 criteria)

All three: logical ordering MET, consistent hierarchy MET, separation of concerns MET, navigation aid ("Read `context.md` first") MET, option-document convention (What/For/Against) MET. **Subtotal 5/5 each.**

### Clarity (5 criteria)

| Criterion | V1 | V2 | V3 |
|-----------|----|----|----|
| Unambiguous language | MET | NOT MET ("Optionally `uv cache clean`", "may exceed") | NOT MET ("shape-matched" undefined) |
| Concrete | MET | MET | MET |
| Section purpose clear | MET | MET | MET |
| Terms defined (kind A/B via context.md) | MET | MET | MET |
| Actionable next steps | MET (printed commands, sunset task) | MET (prints how to delete data) | MET ("run the command once after `./update.sh`") |
| **Subtotal** | **5/5** | **4/5** | **4/5** |

### Risk Coverage (5 criteria)

| Criterion | V1 | V2 | V3 |
|-----------|----|----|----|
| >= 3 risks with probability and impact | NOT MET (3 risks, no probability/impact) | NOT MET | NOT MET |
| Mitigation per risk | MET (printed kind-B command; allowlist + later removal; Coder re-add "harmlessly") | NOT MET | NOT MET |
| Failure modes and recovery | MET (warning, unchanged exit, verify) | MET (non-fatal) | NOT MET |
| External dependency failures | MET (missing `claude`, Coder bundle) | MET (network-free uninstall UNVERIFIED, Coder health check) | MET (Coder schedule) |
| Monitoring/validation | MET (re-read verify) | NOT MET | MET (`--dry-run` preview) |
| **Subtotal** | **4/5** | **2/5** | **2/5** |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | V1 | V2 | V3 |
|-----------|----|----|----|
| Collection boundaries (empty) | MET ("no subprocess when the entry is absent; zero cost on fresh") | NOT MET | NOT MET |
| State interactions across components | MET (bundle re-adds `serena`) | MET (bundle reinstall churn, health check) | MET (registration vs image binary removal) |
| Guard gaps | MET (different-shape kept; env/headers excluded) | MET (receipt + sha256, private single-link files) | NOT MET (matcher undefined) |
| Count divergence | NOT MET | NOT MET | NOT MET |
| Interaction effects | MET (step undone by bundle; Phase 2 reuse of helper) | MET (uv tool removal vs bundle) | MET (Coder image vs registration) |
| **Subtotal** | **4/5** | **3/5** | **2/5** |

### Qualitative Summary

| Dimension | V1 (A) | V2 (B) | V3 (C) |
|-----------|--------|--------|--------|
| Completeness | 4/5 | 3/5 | 2/5 |
| Correctness | 3/5 | 2/5 | 3/5 |
| Structure | 5/5 | 5/5 | 5/5 |
| Clarity | 5/5 | 4/5 | 4/5 |
| Risk Coverage | 4/5 | 2/5 | 2/5 |
| Invariant & Edge Case | 4/5 | 3/5 | 2/5 |
| **qual_score** | **25/30 = 0.833** | **19/30 = 0.633** | **18/30 = 0.600** |

### Edge Case Floor Check

V1 4/5 eligible; V2 3/5 eligible; V3 2/5 eligible. Floor not triggered.

## Position-Bias Mitigation

Pass 1 order V1, V2, V3; pass 2 order V3, V2, V1 (orchestrator, independent re-read of each variant file).

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|-----------|---------|--------|--------|-----------|-------|
| Completeness: out of scope | V3 | NOT MET | MET | DISAGREE | MET (step 2 lists binaries, uv tools and data as manual-only) |
| Completeness: success criteria | V2 | MET | NOT MET | DISAGREE | NOT MET ("fully clean" is not a checkable criterion) |
| Risk: monitoring/validation | V3 | MET | MET | AGREE | MET |
| Invariant: guard gaps | V3 | NOT MET | NOT MET | AGREE | NOT MET |
| Correctness: no internal contradictions | V1 | MET | NOT MET | DISAGREE | NOT MET ("identified by exact shape" vs basename matcher) |

Disagreements re-evaluated: 3. Final verdicts changed relative to pass 1: 2 (V3 out-of-scope -> MET; V1 internal contradictions -> NOT MET). Tables above show final verdicts.

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate points credited |
|---------|---------------|--------------|-----------------|------------------------|
| V1 (A, architect) | 0.460 | 0.417 | **0.877** | 21 of 23 |
| V2 (B, devops/backend) | 0.400 | 0.317 | **0.717** | 3 of 23 |
| V3 (C, security) | 0.430 | 0.300 | **0.730** | 4 of 23 |

**Margin**: 14.7 points (V1 over V3), well above the 5% threshold.
**Tiebreaker applied**: No.

## Selected Base: Variant 1 (Option A, architect advocate)

### Selection Rationale
Highest on both layers and won or co-won 21 of 23 debate points. It is the only original variant that meets the goal on the `./update.sh` path (X-003, conceded by C), fits Coder's 60 s bound (C-007, B's real timeout is 300 s), already specifies non-fatal and missing-CLI behaviour (C-004, C-009), and has the keep-and-report rule for different-shape entries (U-002). Its real weaknesses — loose matchers (A-001, INV-001/002), no handling of IronClaude's receipt/marker (A-006), and removal of an ambiguous Coder-written serena entry (X-004) — are all repairable from the other variants and the probe.

### Strengths to Preserve from Base
1. Automatic, non-interactive retire step inside `superclaude install`, not gated on `--force` (A step 1; `main.py:189-275`).
2. Exact top-level user scope, mutation only through `claude mcp remove --scope user`, verify by re-read (A steps 1-3).
3. Never-touch list and keep-indexes policy (A step 4; `install_codebase_memory.py:74-78`).
4. Non-fatal semantics and missing-CLI skip (A step 6; `install_user_setup.py:251-258`).
5. `RETIRED_MCP_SERVERS` table with sunset; parameterised removal helper reused by Phase 2 (A Implementation).
6. Stale-primitive analysis (A final paragraph), corrected for non-`--force` paths.

### Strengths to Incorporate from Non-Base Variants
1. From V2 (B), R1 strength 1 / R2: IronClaude-owned receipt and `.pending` cleanup; provenance split for the pre-0e7bc31f serena argv.
2. From V3 (C), steps 3-4 and R2: hand off ambiguous/Coder-owned serena entries with a printed command; Coder handoff; read-only preview (moved into `install --list`).
3. From the Round 2.5 probe and resolution round: INV-001..INV-014 resolutions (provenance tiers, binary gate, fixed order, safe helper, direct exec + caps, shared classifier, doctor/update notices, residual record).
