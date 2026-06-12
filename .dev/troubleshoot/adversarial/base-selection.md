# Base Selection

## Quantitative Scoring (50% weight)

Requirements derived from `REPORT.md`: **R1** fix output capture (gate evaluates the real document), **R2** fix `.dev/specs` contamination, plus a hotfix risk axis (blast radius, time-to-fix).

| Metric (weight) | Solution 1 | Solution 2 | Solution 3 |
|-----------------|-----------|-----------|-----------|
| Requirement coverage RC (0.30) | 0.50 (R1 only; R2 explicitly punted) | 0.95 (R1+R2 at source) | 0.95 (R1+R2) |
| Internal consistency IC (0.25) | 0.95 (no errors, honest) | 0.80 (chroot mislabel of S3) | 0.78 (tool-interception mislabel of S2 + unverified core claim asserted as fact) |
| Specificity SR (0.15) | 0.90 | 0.88 | 0.92 |
| Dependency completeness DC (0.15) | 0.90 | 0.90 | 0.90 |
| Section coverage SC (0.15) | 0.70 (7/10) | 1.00 (10/10) | 1.00 (10/10) |
| **quant_score** | **0.663** | **0.902** | **0.903** |

## Qualitative Scoring (50% weight) — 30-criterion additive binary rubric

| Dimension (5 each) | Solution 1 | Solution 2 | Solution 3 |
|--------------------|-----------|-----------|-----------|
| Completeness | 4 (R2 out of scope) | 5 | 5 |
| Correctness | 5 | 4 (chroot mislabel) | 3 (tool-interception mislabel + unverified result-event core, per INV-008) |
| Structure | 5 | 5 | 5 |
| Clarity | 5 | 5 | 4 (B1/B2 hybrid ambiguity) |
| Risk Coverage | 4 | 4 | 5 (7 ranked + CRITICAL flag + feature flag) |
| Invariant & Edge Coverage | 5 (tiebreak, empty, traversal, mtime, multi-match) | 3 (compliance, drift, task_dir) | 5 (truncation, sentinel, cwd, resume, parallel) |
| **criteria met / 30** | **28** | **26** | **27** |
| **qual_score** | **0.933** | **0.867** | **0.900** |

Edge-case floor (≥1/5 on Invariant & Edge): S1=5 ✅, S2=3 ✅, S3=5 ✅ — all eligible.

## Position-Bias Mitigation (dual-pass)

Pass 1 (S1,S2,S3) and Pass 2 (S3,S2,S1) agreed on all dimension subtotals. The only criterion re-evaluated was S3 Correctness: Pass 1 scored 3, Pass 2 initially 4 (crediting honesty about the unverified mechanism). Re-evaluation with explicit comparison: the result-event mechanism is **stated as fact** in `solution-3:207` ("The task file content is in the result event — correct") while flagged unverified in Open Q1 — an internal contradiction confirmed by INV-008 → **final verdict 3**. No other disagreements.

## Combined Scoring

`variant_score = 0.50 × quant + 0.50 × qual`

| Variant | quant | qual | **combined** |
|---------|-------|------|--------------|
| Solution 1 | 0.663 | 0.933 | **0.798** |
| Solution 2 | 0.902 | 0.867 | **0.885** |
| Solution 3 | 0.903 | 0.900 | **0.901** |

Raw ranking: S3 (0.901) > S2 (0.885) > S1 (0.798). Top two (S3, S2) are within 0.016 < 0.05 → **tiebreaker triggered**.

## Tiebreaker Protocol (S3 vs S2)

- **Level 1 — debate performance**: S2 wins. After the invariant probe, S3's two unique contributions both proved hazardous: cwd-isolation (U-004) breaks codebase reads (INV-011 HIGH) and can *cause* the research-notes gate to fail; result-event capture (C-002) is grep-confirmed unimplemented + unverified (INV-008). S2's core mechanism (path pinning) survived the probe intact and is the cleanest at-source fix. S2 won/co-won the decision-critical diff points (C-001, C-002, C-003, C-005, C-006, X-003).
- **Level 2 — correctness count** (confirmation): S2 correctness = 4 > S3 correctness = 3. Also favors S2.

**Tiebreaker resolves to Solution 2.**

## Selected Base: Solution 2 (Prompt-side path pinning)

### Selection rationale

Solution 2 is the most defensible **base** for a production hotfix:

1. It satisfies both requirements (R1 capture + R2 contamination) at the source with low–medium blast radius, by writing to `task_dir` (outside the WHERE source dirs).
2. Its mechanism (inject canonical absolute output path into prompts) **survived the invariant probe intact** — unlike S3's cwd (INV-011) and result-event (INV-008) contributions.
3. Its one genuine weakness (agent compliance, X-003) is precisely covered by incorporating Solution 1's hardened recovery as a backstop — the REPORT's recommended 2+1 pairing.
4. It is the natural spine for the layered-defense merge and aligns with the established, already-working `Output path:` pinning idiom used by ~12 other builders that do **not** exhibit the bug.

### Strengths to preserve (from base)

- `_artifact_path_for_step` helper mirroring `_STEP_ARTIFACT_FILES`, guarded by a sync unit test (U-003) — single source of truth, no prompt/executor drift.
- Pin canonical absolute output path in the four un-pinned document builders: `build_scope_discovery_prompt`, `build_research_notes_prompt`, `build_sufficiency_review_prompt`, `build_preparation_prompt`.
- Contamination prevention by directing output to `task_dir` rather than the WHERE-derived `.dev/specs/`.

### Strengths to incorporate (from non-base variants)

- **From Solution 1**: hardened `_resolve_step_content` as defense-in-depth backstop — pattern map for non-canonical names + `_pick_best_candidate` deterministic tiebreak (replacing current "largest wins", INV-006) + bounded WHERE search roots with symlink containment (INV-005) + path-traversal guard (U-002).
- **From Solution 3**: truncation-detection semantic check (U-005, cheap/harmless); preserve the `output_text`(NDJSON)↔`gate_content`(disk) split for sentinel detection (INV-010).

### Deferred (explicitly out of hotfix scope)

- **Solution 3 cwd-isolation** (U-004): only after adding an explicit absolute repo-root injection for input reads (INV-011/INV-003). As a hotfix, item 1's absolute output-path pinning already prevents contamination without breaking reads.
- **Solution 3 result-event capture** (C-002) behind `capture_mode` flag (default legacy): only after verifying the CLI emits a usable `result` event (INV-008) and confirming sentinel preservation (INV-010).

### Dropped

- **Frontmatter prompt-mandate** (naive consensus item 5): redundant (prompt already emits `[Date,Scenario,Tier]` at `prompts.py:224-228`) and a dead constraint (PRD `_evaluate_gate` never reads `required_frontmatter_fields`) — INV-001.
