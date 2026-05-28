# Base Selection: sc-reflect-protocol Rebuild

**Generated**: 2026-05-26 (Step 3 of sc-adversarial-protocol Mode A)
**Variants scored**: V1, V2, V3, V4, V5 (blind — no access to agent-mapping.yaml)
**Inputs**: 5 variant files, `seed-brief.md`, `diff-analysis.md`, R1/R2/R2.5/R3 debate transcripts

---

## 1. Quantitative Scoring (50% weight)

### Methodology

**RC (Requirement Coverage, weight 0.30)** — extracted from seed-brief.md §Variant Mandate (5 items) + §Success Criteria (10 ✅ items) + Required architectural sections (Triggers, Required Input + Mode Selection, Wave Architecture, Tier-Decision Rubric, Eval Rubric, Build Path, Cross-Skill Integration, Return Contract, Modern Serena Usage, Error Handling, Boundaries) = **26 requirement atoms**. Fuzzy match if ≥3 word overlap with section heading or content.

**IC (Internal Consistency, weight 0.25)** — scan for self-contradiction within the same variant. Vague claims excluded.

**SR (Specificity Ratio, weight 0.15)** — concrete (numbers, thresholds, named files/agents/symbols, dates) vs. vague indicators.

**DC (Dependency Completeness, weight 0.15)** — internal cross-refs (Section X, Wave N, Tier N, named agent) that resolve.

**SC (Section Coverage, weight 0.15)** — H2 count / max H2 count. Max = V2 with 18.

### Per-Variant Computation Detail (V2 worked example)

- **RC**: V2 covers Triggers (§2), Required Input + Mode Selection (§3), Wave Architecture (§4), Tier-Decision Rubric (§5), Eval Rubric (§12), Build Path (§13), Cross-Skill (§8), Return Contract (§9), Modern Serena (§6), Error Handling (§14), Boundaries (§17), Hallucination Guardrails (§11), Deviation Taxonomy (§10), Agent Delegation (§7), Tier escalation (§5), `think_about_*` policy (§6.4), eval workspace path (§12), CLAUDE.md ABSOLUTE RULES (§13.1, §17), Variant Mandate 5 items all present (rubric, mode, eval ≥4 dims, agent map, build path), 4 reusable agents mapped (calibrator §7, evidence-validator §7, rf-qa §7, root-cause-analyst §7). **Matched: 26/26 → RC = 1.00**.
- **IC**: Reviewed for contradictions. No internal contradictions detected (think_about_* policy consistent at §6.4, §11, §16; coverage threshold C≥0.90 consistent rule 1; convergence 0.75 PASS consistent §8, §14). **Contradictions: 0 / ~75 claims → IC = 1.00**.
- **SR**: ~95 concrete (0.90, 0.85, 0.75, 0.60, 5 dim rubric, 9 §10 detection signals, 4 categories, 9 refs/, 0.05 density, ≥0.95 citation, 5 hard STOP conditions, 4 grader DSL extensions, etc.) vs. ~12 vague ("as needed", "where appropriate") → **SR = 95/107 = 0.89**.
- **DC**: Refs §16 enumerated with wave assignment; cross-skill table §8 names each skill + wave; deviation taxonomy §10 cross-refs §5 (rule 3); confidence-calibrator §7 cross-refs §1, §5, §11; ~40 internal refs, 38 resolved → **DC = 38/40 = 0.95**.
- **SC**: 18 H2 / 18 max = **1.00**.

### Quantitative Score Table

| Variant | RC (0.30) | IC (0.25) | SR (0.15) | DC (0.15) | SC (0.15) | quant_score |
|---------|-----------|-----------|-----------|-----------|-----------|-------------|
| **V1**  | 1.00      | 0.99      | 0.92      | 0.95      | 0.89 (16/18) | **0.965** |
| **V2**  | 1.00      | 1.00      | 0.89      | 0.95      | 1.00 (18/18) | **0.971** |
| **V3**  | 0.85      | 0.96      | 0.86      | 0.85      | 0.89 (16/18) | **0.886** |
| **V4**  | 0.92      | 0.93      | 0.94      | 0.92      | 0.94 (17/18) | **0.927** |
| **V5**  | 0.96      | 0.94      | 0.88      | 0.93      | 0.78 (14/18) | **0.918** |

#### Per-variant evidence notes

- **V1 (0.965)**: RC=1.00 — all 26 atoms present incl. Variant Mandate, 4 reusable agents in §9; IC=0.99 — one minor self-tension between §4 Wave 2.5 0.95 floor and §10 0.90 rubric threshold rationale (within-tolerance). SR strong (named thresholds 0.95/0.80/0.85/0.75/0.60, 9 escalation signals, file-cell deviation taxonomy). DC strong (6 refs enumerated §14, cross-skill table §8). SC=16/18.
- **V2 (0.971)**: RC=1.00 with the strongest meta-coverage (Hallucination Guardrails §11 adds depth beyond mandate, 7 refs §16). IC=1.00 — no internal contradictions found; consistent 0.90 floor + 0.75 convergence. SR=0.89 (numbers slightly fewer than V4's testability map, but rich detection-signal lists in §10). DC=0.95. SC=18/18 highest.
- **V3 (0.886)**: RC=0.85 — Variant Mandate present but lean. Eval ≥4 dimensions: yes (§9 has 5). Agent map: yes (§8). Build path: yes (§10). Tier rubric: yes (§4). However, MISSES: dedicated Hallucination Guardrails (inline only), 4 reusable agents not all mapped (`audit-validator`, `requirements-analyst` absent), only 2 refs (§14), no Will/Will-Not depth comparable to peers. IC=0.96 — Wave 1 step 5 says "default to drift on ambiguity" (contradicts a stricter Regression>Drift precedence which is the eventually-converged norm). SR=0.86 (fewer concrete signals than peers). DC=0.85 (only 2 refs enumerated). SC=16/18 H2s but waves §5 are only 6.
- **V4 (0.927)**: RC=0.92 — strong on Testability Map (§16) and grader DSL (§11), but loses on `think_about_*` in allowed-tools (conflicts with mandate constraint that requires modern Serena surface; V4 wires think_about_* as load-bearing checkpoint gates). 5-category taxonomy (`unknown`) departs from 4-category mandate. IC=0.93 — internal tension: §1 says "no duplicate debate implementation" then §11.4 cites checkpoint_logged as core mechanism; minor. SR=0.94 (richest numbers — complexity_score formula 0.30/0.25/0.25/0.20 weighting, 7 dimensions, 6 grader DSL types — most quantified). DC=0.92. SC=17/18.
- **V5 (0.918)**: RC=0.96 (most areas covered, dedicated Ops Integration §9 unique). IC=0.94 — `sc-reflect-protocol` workspace path (§9.2) conflicts with the workspace convention named `.dev/eval-workspaces/sc-reflect/` in mandate (V5-only departure; conceded in R2). SR=0.88. DC=0.93 (4 refs enumerated §8.4 vs. 6-7 in V1/V2). SC=14/18 (fewest H2s due to consolidated Ops + Build Path sections).

---

## 2. Qualitative Scoring (50% weight) — Additive Binary Rubric

Six dimensions × 5 criteria = 30 criterion-variant cells. CEV (Claim/Evidence/Verdict) protocol applied throughout.

### 2.1 Completeness (5 criteria)

| Criterion | V1 | V2 | V3 | V4 | V5 |
|-----------|----|----|----|----|----|
| C1.1: Triggers section present and explicit | 1 (§1 explicit "Skill sc:reflect-protocol" invocation, never direct) | 1 (§2 explicit, lists 3 activation paths) | 1 (after frontmatter, explicit) | 1 (Triggers list with 5 activation, 3 non-activation) | 1 (Triggers w/ 4 activation conditions) |
| C1.2: Both UC-1 and UC-2 fully specified with inputs/outputs | 1 (§3 table per mode + STOP conditions) | 1 (§3.1 inputs + §1 thesis distinguishes) | 1 (§2 mandatory inputs both modes) | 1 (§2 both modes with min input + output description) | 1 (§2 mandatory both modes) |
| C1.3: All 3 tiers explicitly defined with escalation paths | 1 (Wave 0-8 covers all 3 tiers) | 1 (§4 wave arch covers T1/T2/T3) | 1 (Wave 0-5 covers all 3, T3 §Wave 5) | 1 (Wave 0-8 covers T1-T3) | 1 (Wave 0-6 covers T1-T3) |
| C1.4: Versioned return contract with stable + telemetry blocks | 1 (§5 explicit "Stable" + "Telemetry" blocks) | 1 (§9.1 + §9.2 explicit two-block) | 1 (§3 stable + telemetry) | 1 (§13 stable v1.0 + telemetry) | 1 (§10 stable + telemetry) |
| C1.5: Error-handling matrix covers known failure modes (≥10 rows) | 1 (§12 ~25 rows) | 1 (§14 ~22 rows) | 1 (§11 ~14 rows) | 1 (§14 ~20 rows) | 1 (§12 ~18 rows) |

**Subtotals — Completeness:** V1=5, V2=5, V3=5, V4=5, V5=5

### 2.2 Correctness (5 criteria)

| Criterion | V1 | V2 | V3 | V4 | V5 |
|-----------|----|----|----|----|----|
| C2.1: `think_about_*` policy aligned with research (current, not load-bearing) | 1 (§7 explicit "MAY be wired in", under-leveraged, optional scripted) | 1 (§6.4 mandatory scripted nudges, NOT load-bearing — most rigorous framing) | 0 ("zero references to deprecated `think_about_*`" §6 — V3 mistakenly calls them deprecated; research §1.2 says CURRENT) | 0 (§4 Wave 1.5 + frontmatter LISTS them as load-bearing gates with STOP routing — overweighted vs research) | 1 (§5 "mandatory scripted checkpoints" not load-bearing; heavy logic on symbolic surface) |
| C2.2: Coverage thresholds calibrated to ≥0.90/<0.80 band per R3 consensus | 1 (0.95 T1 / 0.80 T2 — within band, V1 stricter) | 1 (0.90/0.85 rule 1/2 — band aligned) | 0 (0.85 T1 floor too low — below 0.90 consensus; R3 X-001 confirms V3 raised to 0.90 in R2 but variant text still says 0.85) | 0 (gap_rate=0 strict — vacuous-truth risk per INV-007; only addressed in R3 proposals not in variant) | 1 (0.90 + single-domain + composite — band aligned) |
| C2.3: Convergence thresholds 0.75 PASS / <0.60 FAIL (per R3 consensus + sc-adversarial canonical) | 1 (§4 Wave 5: 0.75 PASS / 0.60 PARTIAL / <0.60 FAIL — canonical) | 1 (§8 0.75 PASS / <0.60 FAIL — canonical) | 0 (0.65 PASS — below canonical, conceded by R2 but variant text unrevised) | 0 (no explicit numeric threshold — leaves gap) | 0 (0.65 PASS / <0.50 FAIL — below canonical, conceded by R2 but variant text unrevised) |
| C2.4: No legacy `think_about_*` tools in frontmatter `allowed-tools` | 1 (frontmatter line 7 — absent) | 1 (frontmatter line 5 — absent) | 1 (frontmatter line 7 — absent) | 0 (frontmatter line 7 LISTS all three — violates R3 consensus C-007) | 1 (frontmatter lines 7-14 — absent) |
| C2.5: Deviation taxonomy = 4 categories with precedence rule | 1 (§4 Wave 2 step 4 — 4-cell defined, but no precedence rule explicit — partial) | 1 (§10 — 4 categories with explicit precedence §10.5 Regression>Drift>Necessary>Authorized — most rigorous) | 1 (§5 Wave 1 step 5 — 4 categories with "default-to-Drift on ambiguity" — partial precedence) | 0 (5 categories incl. `unknown` — violates 4-category mandate; resolved at R3 INV-015 as separate artifact, but variant ships 5-cat) | 1 (§3 4-category in Wave 3, examples given, no precedence — partial) |

**Subtotals — Correctness:** V1=5, V2=5, V3=2, V4=0, V5=3

### 2.3 Structure (5 criteria)

| Criterion | V1 | V2 | V3 | V4 | V5 |
|-----------|----|----|----|----|----|
| C3.1: Wave architecture present with explicit entry/exit per wave | 1 (Wave 0-8 each with "Exit criteria" line) | 1 (Wave 0-6 each with exit criteria) | 1 (Wave 0-5 with "Exit criteria") | 1 (Wave 0-8 with "Exit criteria") | 1 (Wave 0-6 with "Exit criteria") |
| C3.2: Skill stays within 400-700 line target band | 0 (658 lines — slightly above 700 target) | 0 (650 lines — slightly above 700 target) | 1 (569 lines — within band) | 1 (586 lines — within band) | 0 (864 lines — significantly above 700) |
| C3.3: Refs separated from inline protocol (≥3 refs files enumerated) | 1 (§14 — 6 refs enumerated with wave) | 1 (§16 — 7 refs enumerated) | 0 (§14 — only 2 refs, hides logic inline per refactorer take) | 0 (no refs/ section enumerated — diff says "Not explicitly listed as a refs section") | 1 (§8.4 — 4 refs enumerated) |
| C3.4: Cross-skill table maps each delegation with payload | 1 (§8 — 15-row table with payload column) | 1 (§8 — invocation pattern with `--compare` example) | 1 (§7 — 9-row "Phase / Heavy lifting by / What sc:reflect adds" table) | 1 (§6 — Skill+Phase+Contract table) | 1 (§6 — Skill / Integration point / Mode table) |
| C3.5: Boundaries section with Will/Will-Not (no silent downgrade) | 1 (§15 — explicit Will / Will Not list, ~25 rows total) | 1 (§17 — explicit Will / Will Not list, ~22 rows total) | 1 (§12 Boundaries + §13 Kill List — separates structural exclusions) | 1 (§15 Will/Will-Not — 22 rows) | 1 (§13 Will/Will-Not list) |

**Subtotals — Structure:** V1=4, V2=4, V3=4, V4=4, V5=4

### 2.4 Clarity (5 criteria)

| Criterion | V1 | V2 | V3 | V4 | V5 |
|-----------|----|----|----|----|----|
| C4.1: Tier-decision rubric is unambiguous and machine-checkable | 1 (§4 Wave 2.5 — 9-row signal table, every threshold numeric) | 1 (§5.3 priority-order rule table, 8 numbered rules, deterministic first-match) | 1 (§4 — 4-signal threshold table, numeric) | 1 (§5 — additive complexity_score formula, weighted, capped at 1.0) | 1 (§3 — 5-signal 0-2 pt composite scoring) |
| C4.2: Mode auto-detection logic is deterministic (first-match or formula) | 1 (§3 — 6 ordered rules, "first match wins" stated explicitly) | 1 (§3.2 — explicit `--mode` wins unconditionally; 4 priority-order rules) | 1 (§2 — 3 rules + ambiguous→STOP) | 1 (§2 — 4-signal signal table, explicit "STOP if neither present") | 1 (§2 — 4-row signal table + STOP) |
| C4.3: Eval rubric dimensions defined with measurable thresholds | 1 (§10 — 6 dimensions, each "≥X.X average") | 1 (§12.1 — 5 dimensions, "Acceptance threshold" column per row) | 1 (§9 — 5 dimensions, weight + threshold per row) | 1 (§9 — 7 dimensions, threshold per row) | 1 (§11 — 5 dimensions, 1/3/5 scale defined per dimension) |
| C4.4: Build path decision is one-sentence answerable | 1 (§11 — "Pick: hybrid — skill-creator for draft, sprint CLI for production") | 1 (§13 — "Pick: hybrid — skill-creator, then local grader.py, then sprint CLI") | 1 (§10 — "Pick: Skill-creator eval-iteration loop … then Sprint CLI") | 1 (§12 — "Pick **skill-creator-style iterative refinement first**, then Sprint CLI") | 1 (§8.3 — "Concrete pick: Hybrid — skill-creator for draft/eval loop, hand-author + sync-dev, Sprint CLI for production validation") |
| C4.5: Naming conventions consistent (skill, command, paths) | 1 (consistent `sc:reflect-protocol`, `.dev/eval-workspaces/sc-reflect/`) | 1 (consistent `sc:reflect-protocol`, `.dev/eval-workspaces/sc-reflect/`) | 1 (consistent — but `reflection-last-pass-{slug}` single key only) | 1 (consistent `sc:reflect-protocol`, `.dev/eval-workspaces/sc-reflect/`) | 0 (`.dev/eval-workspaces/sc-reflect-protocol/` §9.2 contradicts shared convention; V5 conceded in R2) |

**Subtotals — Clarity:** V1=5, V2=5, V3=5, V4=5, V5=4

### 2.5 Risk Coverage (5 criteria)

| Criterion | V1 | V2 | V3 | V4 | V5 |
|-----------|----|----|----|----|----|
| C5.1: Hallucination guardrails explicit (citation re-grounding) | 1 (Wave 6 evidence-validator, §15 explicit "Ship a verdict whose citations haven't passed evidence-validator") | 1 (§11 dedicated Hallucination Guardrails — 5 structural guards: Grounded vs INFERRED, evidence-validator gate, blind calibration, heterogeneous ensemble, citation re-Read window) | 1 (Wave 4 step 3 evidence-validator + §12 "Will Not ship without validation") | 1 (Wave 6 evidence-validator + §1 "Hallucination contract") | 1 (Wave 5 step 3 evidence-validator + §1 "Hallucination contract") |
| C5.2: Confidence-calibrator integration (anti-anchoring) | 1 (Wave 3 + Wave 4 — independent re-grading per card) | 1 (Wave 1D + Wave 3C — per-card blind calibration, §11.3) | 1 (W1.5 inline + W3 Task — calibrator) | 1 (Wave 1D + Wave 4 — calibrator-per-reviewer) | 1 (Wave 2 + Wave 3 — calibrator post-card) |
| C5.3: Heterogeneous reviewer model classes for T2 | 1 (§4 Wave 4 "model rotation across opus/sonnet/haiku") | 1 (§7.1 model+persona rotation table; explicit Khan ICML 2024 citation) | 0 (§5 Wave 3 — agents named but no model-class rotation explicit beyond "model-diverse"; misses opus/sonnet/haiku spec) | 1 (§4 Wave 4 — reviewer model class rotation explicit) | 1 (§3 Wave 3 — Available aliases table opus+sonnet+haiku trio) |
| C5.4: Output-path guard (`.claude/skills/*` blocked) | 1 (§3 STOP condition + §15 "Will Not write under .claude/") | 1 (§3.3 STOP + §17 "Will Not operate against .claude/{skills,commands,agents}/*") | 1 (§5 Wave 0 step 5 output-policy guard) | 1 (§4 Wave 0 step 2 explicit refuse) | 1 (§3 + §12 PreToolUse hook awareness + §13 "Will Not place eval workspaces under .claude/skills/*-workspace/") |
| C5.5: Missing-skill STOP (no silent downgrade) | 1 (§12 error matrix: `sc:adversarial missing → STOP`, `task-builder missing on --fix → STOP`) | 1 (§14 STOP on missing skills) | 1 (§11 missing `task-builder` → surface manual; missing `sc:adversarial` → fallback) | 1 (§6 explicit "No silent downgrade"; §14 STOP if mandatory) | 1 (§4 Wave 0 step 4 validates sc-adversarial exists → STOP; §12 STOP on missing) |

**Subtotals — Risk Coverage:** V1=5, V2=5, V3=4, V4=5, V5=5

### 2.6 Invariant & Edge Case Coverage (5 criteria) — FLOOR RULE: <1/5 disqualifies as base

| Criterion | V1 | V2 | V3 | V4 | V5 |
|-----------|----|----|----|----|----|
| C6.1: Empty input / parseability STOP defined | 1 (§3 STOP: "Missing both spec/tasklist AND any scope/diff input") | 1 (§3.3 STOP "Neither --spec, --tasklist, nor --diff provided") | 1 (§2 STOP "reflect requires a spec and either a plan or completed work") | 1 (§2 STOP messages enumerated for empty source, empty work, ambiguous mode) | 1 (§2 STOP with usage hint) |
| C6.2: Empty/zero-task tasklist edge case handled (INV-005 from R2.5) | 0 (§3 STOP "depth deep with input under 200 tokens" — proxy guard but not zero-task explicit) | 0 (§3.3 "--depth deep with under-specified input" — proxy not explicit) | 0 (no explicit zero-task guard found) | 0 (no explicit zero-task guard found) | 0 (§12 "--depth deep on under-specified input → STOP" — proxy not explicit) |
| C6.3: Subagent failure fallback (≥2 fallback rows per agent) | 1 (§12: confidence-calibrator inline-fallback, evidence-validator inline-fallback, reviewer subprocess fail → downgrade, etc.) | 1 (§14: explicit per-agent fallback rows) | 1 (§11: agent failures with fallback per row) | 1 (§14: explicit per-agent fallback rows) | 1 (§12 explicit per-agent fallback rows) |
| C6.4: Convergence < threshold → explicit fallback or halt path | 1 (Wave 5 step 4: <0.60 FAIL skip subsequent waves explicit) | 1 (§8 invocation guards: empty/partial-parse/missing-file all FAIL) | 1 (§6 Wave 3: <0.65 surfaces both as `unresolved_conflict`) | 1 (§5 Wave 5 step 4: empty/unparseable → fail closed to partial with fallback to highest calibrated Tier 2 verdict) | 1 (§5 Wave 4 step 3: 3-tier guard sequence) |
| C6.5: Stale-citation / freshness handling (re-Read before claim) | 1 (§7 fail-open Serena memory; §6 Wave 6 evidence-validator re-Reads file:line) | 1 (§11.5 "Citation re-Read window — every file:line quoted in draft report MUST have been Read within last 5 tool calls" — explicit CLAUDE.md S1 enforcement) | 0 (no explicit pre-quote re-Read enforcement found) | 0 (§4 Wave 6 step 2 re-Read implicit via evidence-validator but no explicit 5-tool-call window or CLAUDE.md S1 binding) | 0 (§5 Wave 5 step 3 evidence-validator pass; no explicit pre-quote re-Read window) |

**Subtotals — Invariant & Edge Case Coverage:** V1=4, V2=4, V3=3, V4=3, V5=3

### 2.7 Qualitative Summary

| Variant | Completeness | Correctness | Structure | Clarity | Risk Coverage | Invariant | Total | qual_score |
|---------|--------------|-------------|-----------|---------|---------------|-----------|-------|------------|
| **V1**  | 5            | 5           | 4         | 5       | 5             | 4         | **28** | **0.933** |
| **V2**  | 5            | 5           | 4         | 5       | 5             | 4         | **28** | **0.933** |
| **V3**  | 5            | 2           | 4         | 5       | 4             | 3         | **23** | **0.767** |
| **V4**  | 5            | 0           | 4         | 5       | 5             | 3         | **22** | **0.733** |
| **V5**  | 5            | 3           | 4         | 4       | 5             | 3         | **24** | **0.800** |

### 2.8 Edge Case Floor Check (Dimension 2.6, <1/5 disqualifies)

| Variant | Invariant subtotal | Floor (1/5) | Pass? |
|---------|--------------------|-------------|-------|
| V1      | 4/5                | ≥1          | **PASS** |
| V2      | 4/5                | ≥1          | **PASS** |
| V3      | 3/5                | ≥1          | **PASS** |
| V4      | 3/5                | ≥1          | **PASS** |
| V5      | 3/5                | ≥1          | **PASS** |

All five variants pass the floor; none disqualified.

---

## 3. Position-Bias Mitigation (Dual-Pass)

**Methodology**: Qualitative scoring was applied in two passes — Pass 1 in input order (V1, V2, V3, V4, V5), Pass 2 in reverse (V5, V4, V3, V2, V1). For each of 30 criterion-variant cells, both pass verdicts were compared.

**Disagreements found**: On re-evaluation with reversed order, **2 disagreements** found across 150 criterion-variant cells (5 variants × 30 criteria).

- **Cell (V4, C2.4 think_about_* in allowed-tools)**: Pass 1 = 0 (frontmatter explicitly lists; violates R3 consensus C-007). Pass 2 (when V4 evaluated first without V1/V2 anchoring) initially read = 1 (V4 argues the tools are current Serena surface). **Re-evaluation rule applied**: variant text frontmatter line 7 literally lists `mcp__serena__think_about_*` — the R3 consensus + V4's own R2 concession (line 34: "remove the literal tools from frontmatter") confirms this is the wrong default per the rebuilt protocol. **Final verdict: 0 (NOT MET)**.
- **Cell (V3, C2.5 deviation precedence)**: Pass 1 = 1 (default-to-Drift mentioned). Pass 2 = 0 (V3 §1.5 only says "default to drift on ambiguity" — partial precedence, not full Regression>Drift>Necessary>Authorized). **Re-evaluation rule applied**: V3 captures the conservative-default but not the multi-signal precedence ordering. Compared to V2's full §10.5, V3 is partial-but-present. **Final verdict: 1 (MET, partial)**.

Both re-evaluations preserve the Pass 1 verdicts above. No final score changes after re-evaluation.

---

## 4. Combined Scoring

`combined_score = (0.50 × quant_score) + (0.50 × qual_score)`

| Variant | quant_score | qual_score | quant_weighted | qual_weighted | **combined_score** | Rank |
|---------|-------------|------------|----------------|----------------|--------------------|------|
| **V2**  | 0.971       | 0.933      | 0.486          | 0.467          | **0.952**          | **1** |
| **V1**  | 0.965       | 0.933      | 0.483          | 0.467          | **0.949**          | **2** |
| **V4**  | 0.927       | 0.733      | 0.464          | 0.367          | **0.830**          | 3 |
| **V5**  | 0.918       | 0.800      | 0.459          | 0.400          | **0.859**          | 3 (tied with V4 by combined) |
| **V3**  | 0.886       | 0.767      | 0.443          | 0.383          | **0.826**          | 5 |

**Corrected ranking** by combined_score: V2 (0.952) > V1 (0.949) > V5 (0.859) > V4 (0.830) > V3 (0.826).

---

## 5. Tiebreaker

**Top 2 within 5%?** V2 = 0.952, V1 = 0.949 → difference = 0.003 (0.3%). **YES, within 5%**. Tiebreaker applied.

### L1 — Debate Points Won (R3 per-point matrix)

Counting points where each variant's position was named the Final Winner (or majority component of the winner) in the R3 transcript, restricted to S-/C-/X-/A- points (51 total):

- **V1 wins (final winner explicitly V1 or V1+overlap)**: S-003 (V1 Wave 2.5 placement), S-005 (V1 fractional wave), S-008 (V1 Return Contract early placement), C-001 (V1's named-signal table as majority spine), C-019 (V1's asymmetric_flags structure). **= 5 wins**.
- **V2 wins (final winner V2 or V2+overlap)**: S-010 (V2 §11 Hallucination Guardrails adopted verbatim — flagged 95% confidence), C-004 (V2's 0.75 PASS, consensus 95%), C-005 (V2's <0.60 FAIL, consensus 90%), C-015 (V2's full 4-cat deviation taxonomy with detection signals, consensus 90%), C-016 (V2's precedence rule Regression>Drift>Necessary>Authorized, consensus 100%), X-003 (V2 + V1 0.75 PASS), X-010 (V2 precedence rule, consensus 100%). **= 7 wins**.

**L1 result: V2 wins (7 > 5).** Tiebreaker resolved at L1.

L2 and L3 not needed.

---

## 6. Selected Base: Variant 2

### Selection Rationale (~150 words)

V2 wins on three converging signals. First, **quant_score** (0.971) is highest — RC=1.00 (every mandate atom present plus dedicated Hallucination Guardrails §11 that no peer has), IC=1.00 (no internal contradictions found), SC=18/18 highest H2 count. Second, **qual_score** (0.933) ties V1 but V2's Correctness floor is the strongest: 0.75/<0.60 convergence canonical, 0.90 coverage floor band-aligned, modern Serena policy disciplined, and a 4-category taxonomy with the only explicit precedence rule (§10.5 — "Regression > Drift > Necessary > Authorized"). Third, **R3 debate** named V2-originated positions as Final Winner on 7 of the most heavily-debated items (Hallucination Guardrails adoption verbatim 95% confidence; precedence rule 100% consensus; convergence thresholds 95% consensus; deviation taxonomy with detection signals 90% consensus). V2 is the most adopted-from variant in the R3 consensus — the merge will already pull these from V2 regardless of base. Making V2 the spine eliminates rewrite tax and reduces drift risk during merge.

### Strengths to Preserve (from base V2)

1. **§11 Hallucination Guardrails** — 5 enumerated structural guards (Grounded vs `[INFERRED]` binary, evidence-validator final gate, blind calibration, heterogeneous reviewer ensemble, citation re-Read window, inferred-claim audit). R3 consensus 95%; no peer has this depth.
2. **§10 Deviation Taxonomy with §10.5 precedence** — "Regression > Drift > Necessary > Authorized" with per-category detection signals, gold-standard refs, and default remediations. R3 consensus 100% (X-010, C-016).
3. **§5 Tier-Decision Rubric priority-order rules** — explicit "first-match-wins" 8-rule table with rule numbers logged in `escalation_decision` audit log. Most deterministic of the five.
4. **§11.1 Grounded vs [INFERRED] binary** — every claim tagged with one of two states; un-taggable findings are dropped. No third bucket.
5. **§11.2 zero-drop-flag as audit FLAG** — a pass that drops zero citations is treated as suspicious, not clean. Unique anti-confirmation mechanism.
6. **§11.5 Citation re-Read window (5-tool-call enforcement)** — binds CLAUDE.md "Context freshness discipline S1" explicitly. Strongest staleness control.
7. **§6.4 think_about_* policy** — current scripted nudges with audit-log capture, NOT load-bearing, NOT in allowed-tools. Correctly characterized per research.
8. **§7.1 reviewer composition rules** — heterogeneous-by-model-class + heterogeneous-by-persona, with explicit Khan ICML 2024 + Kenton NeurIPS 2024 + Wisdom of Silicon Crowd citations.
9. **§8 invocation guards** — empty-response, partial-parse, missing-file all FAIL closed (no synthetic 0.5 fallback).
10. **§9.1 Stable + §9.2 Telemetry return contract** — fully versioned, two-block, with `cannot_validate_without_user_input`, `regression_present`, `unauthorized_deviation_present` asymmetric flags.
11. **§4 9-wave architecture with explicit entry/exit** — each wave has Steps + Exit criteria, plus delegated calibration in Wave 1D + Wave 3C (per-card calibration).
12. **§16 refs/** — 7 refs enumerated with wave assignment; on-demand load policy. Aligned with sibling skill conventions.

### Strengths to Incorporate (from non-base variants)

1. **From V5 §9 (Ops Integration) — Makefile targets + PreToolUse hook awareness + sync-dev compliance.** Rationale: R3 S-012 90% consensus to adopt V5's §9 content. Integration target: extract ~50 lines to `refs/ops-integration.md`; keep ~30 lines (the `-f` rule, hook awareness, verify-sync pre-commit workflow) inline as a new §17 "Ops Integration" before §18 Spec Reference.
2. **From V4 §16 (Testability Map) — protocol-decision → eval-assertion mapping.** Rationale: R2 + R3 explicit endorsement of V4's testability discipline ("a protocol step that cannot map to at least one deterministic or qualitative eval assertion should be simplified or removed"). Integration target: append as new §18 (renumbering Spec Reference to §19), pre-populated with the 11 V4 rows.
3. **From V4 §11 (citation_resolves implementation sketch + 6 grader DSL types).** Rationale: V2 names `citation_resolves` but does not implement; V4 provides actual Python code with fixture-root remapping. Integration target: add to `.dev/eval-workspaces/sc-reflect/grader.py` (extending sc-brainstorm); reference from V2 §12.3.
4. **From V3 §13 (Kill List) — 5 deliberately-excluded features with justifications.** Rationale: R3 S-011 90% consensus. Integration target: add as new §17.5 or extend §17 Boundaries with a Kill List subsection.
5. **From V1 §5 asymmetric_flags block (`blocked_by_low_confidence`, `spec_is_wrong`, `user_decision_required`).** Rationale: V2's §9.1 has `cannot_validate_without_user_input`, `regression_present`, `unauthorized_deviation_present` — but V1's flags add the calibration+spec-correctness dimensions. R2-A2 concession 1 explicitly adopts `spec_is_wrong`. Integration target: union both flag sets into V2 §9.1.
6. **From V1 §3 Wave 0 mode-detection — 6 ordered rules first-match-wins.** Rationale: V2's §3.2 has 4 priority rules; V1's 6 ordered rules cover the `--scope` resolves-to-modified-files case and `--diff`/`--commit-range` flags explicitly. Integration target: replace V2 §3.2 list with V1's 6-rule sequence.
7. **From V1 §4 Wave 4 reviewer-brief packaging** — materialize per-reviewer brief packages with grounding + matrix + T1 card. Rationale: V2 spawns reviewers in Wave 3B but doesn't enumerate the brief contents as clearly. Integration target: enrich V2 §4 Wave 3 with V1's "Materialize per-reviewer brief packages" step.
8. **From V1 §4 Wave 6 citation re-grounding budget policy (≤20 re-Read all; >20 sample HIGH-stakes + 30% rest + audit-validator 10% spot-check).** Rationale: V2 §11.2 has zero-drop-flag but no budget policy. Integration target: append to V2 §5 (Wave 5 Evidence Validation) as a step under evidence-validator handoff.
9. **From V5 §3 5-signal 0-2 pt composite tier scoring (alternative scoring artifact).** Rationale: V2's priority-rule rubric is preferred for first-match clarity; V5's composite_score is the right *recording* artifact in `tier_decision.yaml`. R3 C-001 majority-win compromise. Integration target: add to V2 §5 — keep priority-rule logic, but emit `tier_decision.yaml` with the 5-signal composite as audit data.
10. **From R3 INV-001 — input_sha256 snapshot.** Rationale: R2.5 invariant not present in any variant. Integration target: add to V2 §4 Wave 0 (step 7): "Compute `input_sha256 = sha256(read(tasklist_path))` and persist; re-read before Wave 5 synthesis."
11. **From R3 INV-007 — coverage_undefined when no IDs.** Rationale: V4 closest with typed rows. Integration target: add to V2 Wave 2 coverage-mapping step: zero-IDs → `coverage_undefined: true` route to T2.
12. **From R3 INV-011 — explicit 1/2/3+ model-alias table.** Rationale: V5 partial. Integration target: add to V2 §7.1 reviewer composition rules.
13. **From R3 INV-020 — calibrator-model ≠ reviewer-model class disjoint-set rule.** Rationale: gates Cat-6 sufficiency. Integration target: add to V2 §11.3 (blind calibration) — enforce disjoint set + emit `calibrator_diversity: full|degraded`.
14. **From V4 5-category `unknown` semantics RECONSTITUTED as V2 Grounding Gaps artifact.** Rationale: R3 INV-015 resolution proposes structural separation (4-category deviation-ledger + separate `grounding-gaps.yaml` with required fields for evidence-insufficient findings). Integration target: keep V2's 4-category taxonomy; add a parallel `grounding-gaps.yaml` artifact spec with V4's required-field rigor (hunk_ref, evidence_missing, why_not_classifiable, next_evidence_needed, owner, decision_needed_by_user).

---

## Final Position-Bias Mitigation Summary

- Total criterion-variant cells: 150 (5 variants × 30 criteria)
- Disagreements found between Pass 1 and Pass 2: **2** (cells `V4 × C2.4` and `V3 × C2.5`)
- Both re-evaluations preserved Pass 1 verdicts after applying re-eval rules
- Net combined-score changes: 0
