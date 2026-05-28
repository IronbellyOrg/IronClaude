# Multi-Caller Bare-Reviewer Integration Evaluations

```yaml
evaluation_metadata:
  date: 2026-05-28T05:50Z
  spec_context: merged-requirements.md (v1.3.0-draft)
  companion: auggie-review-integration-evaluation.md
  scope: /sc:troubleshoot, /sc:reflect, /sc:code-review, /sc:tech-research
  framing: honest cost/benefit, conditional on IMM-1/IMM-2 ship, not advocacy
  estimation_basis:
    - Caller-specific token + wall-clock baselines drawn from each caller's SKILL.md
    - Bare-adjunct delta drawn from §4.1 of auggie-review-integration-evaluation.md
      and the §15 cost profile of sc-reflect-protocol/SKILL.md
    - Marginal-yield estimates anchored to the 7.8 empirical baseline (36% additive
      findings at 1+1 reviewer count) and de-rated by existing reviewer count
```

---

## /sc:troubleshoot

### 1. What this caller already does

Per `sc-troubleshoot-protocol/SKILL.md` — a strictly tiered, escalation-gated debugger:

- **Tier 1**: real-code grounding (auggie + serena fan-out), documentation grounding (Wave 1.5, three parallel discovery branches), single `root-cause-analyst` hypothesis card, blind `confidence-calibrator` re-grade. ~3-6k Claude tokens, 1-3 min.
- **Tier 2** (escalated only by rubric or `--depth deep`): 2-4 parallel hypothesis agents (varied by `--type`: `root-cause-analyst`, `quality-engineer`, `performance-engineer`, `security-engineer`, `system-architect`, `devops-architect`, `refactoring-expert`), each blind-calibrated. ~15-30k Claude tokens.
- **Tier 2 + adversarial debate**: when ≥2 fixes compete, `/sc:adversarial` debates them; `self-review` sanity-checks the merge. ~30-60k Claude tokens, 8-15 min.
- **Tier 3**: hands off to `task-builder` for MDTM remediation.
- **Output shape**: `REPORT.md` (diagnosis + evidence + proposed fix + risk) + audit log + optional task file.

Effective reviewer count at Tier 1: **1**. At Tier 2 without adversarial: **2-4** (all Anthropic). At Tier 2 with adversarial debate: **2-4 + adversarial judge**, all Anthropic-trained.

### 2. What bare adds that isn't already there

| Dimension | Existing pipeline | What bare adds | Marginal value |
|-----------|-------------------|----------------|----------------|
| Tier 1 reviewer count | 1 | +2/3 → 3-4 | Bare gives Tier 1 the ensemble it doesn't have |
| Tier 2 reviewer count | 2-4 (all Anthropic) | +2/3 → 4-7 | Linear, but de-rated past 4 |
| Vendor diversity | Anthropic-only | DeepSeek/Qwen/Kimi/GLM | Genuine — different training corpora flag different bug classes |
| Library-doc grounding | context7 ON in Tier 2 only when symptom names a library | `--bare-c7` enriches docs on EVERY bare reviewer | Net new only for Tier 1 (Tier 2 already touches context7) |
| Stack-trace pattern recognition | Anthropic-trained reasoning | Non-Anthropic models often have wider exposure to OSS stack traces in training | Real, mostly bug-class diversity |
| Hypothesis space coverage | Bounded by 2-4 agent specialties | Bare reviewers can probe across specialties simultaneously | Modest — already covered by the existing agent matrix |

**The honest summary:** Bare on troubleshoot adds the most where Tier 1's single-hypothesis path is most exposed (intermittent / cross-domain bugs). Bare on Tier 2 with debate already-running is closer to noise.

### 3. Concrete value mechanisms (troubleshoot-adapted)

**3.1 "This used to work" / regression-hunting bugs.** Tier 1's `root-cause-analyst` is single-hypothesis; the rubric escalates to Tier 2 only on rubric-fail or `--depth deep`. A bare adjunct at Tier 1 catches a class of "I would have escalated if I'd seen this" cases earlier, by raising `S_dev_density` via independent reviewers noticing things the single analyst missed.

**3.2 Multi-domain symptoms (perf + correctness, security + build).** The rubric already escalates these to Tier 2. The marginal value of bare HERE is lower than at Tier 1, because Tier 2 already runs 3-4 specialists. The non-Anthropic distribution diversity is the only net-new signal — useful, but ~15-20% additive, not 36%.

**3.3 Stack-trace symptoms in third-party code.** Existing Tier 2 fires `mcp__context7__resolve-library-id` only when the symptom names a library by name. Bare with `--bare-c7` injects docs proactively per reviewer. This is the strongest single argument for `--bare-c7` on troubleshoot — catches a class of "library API drift caused this" bugs the existing pipeline only opportunistically covers.

**3.4 The `test_is_wrong` and `behavior_is_documented` asymmetric-cost flags.** Troubleshoot's downstream automation hinges on these flags. A bare reviewer reading the test and the docs without the structured `consistency_with_docs` rubric could flag patterns the rubric missed (e.g., test asserts behavior that's documented as deprecated). Net positive ONLY if the validator gates hallucinations on these flags strictly — a bare-induced false `test_is_wrong=true` is asymmetric-cost-WORSE than no bare adjunct.

### 4. Concrete cost mechanisms

| Phase | Existing (no bare) | With `--bare-reviewers 3` | With `--bare-reviewers 3 --bare-c7` |
|-------|-------------------|---------------------------|--------------------------------------|
| Tier 1 only | ~3-6k Claude, 1-3 min | +45K external + ~10-15K orchestration, +30-60s | +53K external + ~13-18K orch, +60-120s |
| Tier 2 (no adversarial) | ~15-30k Claude, 4-7 min | +45K external + ~12-18K orch, +30-70s | +53K external + ~15-21K orch, +60-145s |
| Tier 2 + adversarial | ~30-60k Claude, 8-15 min | +45K external + ~15-20K orch, +40-80s | +53K external + ~18-23K orch, +70-160s |
| Tier 3 added | +20-40k Claude | unchanged (bare doesn't touch task-builder) | unchanged |

On Tier 1, bare is a ~3x token cost multiplier. On Tier 2-with-adversarial, it's a ~1.4x multiplier. **The economic case is INVERTED from auggie-review:** bare is most cost-justified on the cheap Tier 1 path (where it shifts a single-hypothesis pass into an ensemble), not on the already-expensive Tier 2 path.

### 5. When bare adds the MOST value (troubleshoot-specific)

1. **Intermittent / flaky test bugs (`--type test`).** Tier 1 single-hypothesis is unreliable for non-determinism; bare ensemble at Tier 1 catches race / ordering / timing patterns the single analyst misses.
2. **Library-version regression bugs (`--bare-c7`).** When the user reports "worked on 4.2, broke on 4.3," bare-with-c7 catches API changes the existing pipeline catches only opportunistically.
3. **Cross-language / cross-runtime bugs.** Anthropic-distribution models may have weaker coverage of niche runtimes (Erlang, OCaml, Zig); non-Anthropic models with different training corpora may flag patterns specific to those.
4. **`test_is_wrong` / `behavior_is_documented` candidate cases.** When Tier 1 surfaces a deviation between code, test, and docs, bare reviewers add a third independent vote — high value IF validator quality holds.
5. **Production-incident triage where escalation cost is acceptable.** When the user explicitly invokes `--depth deep` on a P0, bare adjunct's wall-clock cost is dominated by the incident's impact cost.

### 6. When bare adds the LEAST value (or negative)

1. **Trivial single-domain bugs** caught by Tier 1 with confidence ≥ 0.90. Bare adds noise that the rubric's `S_dev_density` may then mis-interpret as ambiguity, triggering needless Tier 2 escalation.
2. **`--depth quick` runs.** The whole point of quick is sub-minute triage; bare's 60-120s wall-clock breaks the user expectation.
3. **PR-post mode equivalents** (when troubleshoot output is auto-posted to a GitHub issue comment). Same IMM-1/IMM-2 sensitivity as auggie-review's PR-post mode.
4. **Build-failure triage where the error is a clear compiler diagnostic.** Bare reviewers will speculate about causes the compiler has already named.
5. **Tier 3 task-builder hand-off cases.** Bare adds nothing to remediation — its findings have already merged into REPORT.md.

### 7. Recommended defaults

```yaml
recommended_defaults:
  default_bare_reviewers: 0           # off by default — opt-in per call
  default_bare_c7: false              # off by default
  conditional_triggers:
    enable_when:
      - "--type test AND (--depth deep OR --depth standard)"
      - "--depth deep"
      - "Tier 2 escalated AND no convergence"
    avoid_when:
      - "--depth quick"
      - "tier_reached=1 AND confidence >= 0.90"
      - "build failure with compiler diagnostic in scope"
  recommended_count: 3
  rationale: |
    Troubleshoot's biggest reviewer-count gap is at Tier 1 (single hypothesis). Default
    3 lifts Tier 1 to a 4-reviewer ensemble when the user opts in. Going to 4 pushes
    cost without proportional yield given the Tier 2 specialist matrix already saturates
    perspective diversity past 4.
```

### 8. Caller-specific gotchas

- **The `test_is_wrong` and `behavior_is_documented` asymmetric-cost flags are derived in Wave 5 from the chosen hypothesis card.** A bare-reviewer-sourced finding incorporated into the chosen hypothesis MUST be Validated (not just Corroborated) for the flag derivation to be safe. Without that constraint, hallucinated test/docs assertions could flip the flag and break downstream automation.
- **Wave 1.5's Documentation Context Card is consumed by ALL Tier 2 hypothesis agents.** If bare reviewers operate without seeing that card, they may flag findings the docs already explain. Recommend: pass the Card path into the bare prompt (`--label` channel) so bare reviewers can reference it — though they won't follow the `consistency_with_docs` schema.
- **The rubric's `S_dev_density` signal is computed from unmapped artifacts.** Bare reviewers raising findings about previously-mapped artifacts could artificially raise density and trigger Tier 2 escalation that wouldn't have happened otherwise. Mitigation: count bare findings separately when computing `S_dev_density`.
- **Tier 3 remediation handoff requires a `success` (not `partial`) REPORT.md.** If the evidence-validator drops bare findings, REPORT.md ships `partial` and Tier 3 is blocked. Users expecting `--fix` workflows should be warned that `--bare-reviewers` raises the risk of partial outcomes.

---

## /sc:reflect

### 1. What this caller already does

Per `sc-reflect-protocol/SKILL.md` — the most structurally adversarial of the four callers, BY DESIGN:

- **Tier 1**: single agent (`root-cause-analyst` for UC-2, `requirements-analyst` for UC-1, or `self-review` for low-stakes) + blind `confidence-calibrator` re-grade. Heterogeneous-by-design: T1 agent and calibrator are different model classes (disjoint-set rule §11.3).
- **Tier 2**: 2-3 parallel reviewers explicitly on **heterogeneous model classes** (sonnet, haiku, optional qwen/kimi if alias resolved) + per-card blind calibration. Executor-class exclusion rule (§7.1) further enforces disjointness.
- **Tier 2 + merge**: `sc-adversarial-protocol` Mode A merges with a judge of yet another class (weak-judge-strong-debaters per Khan ICML 2024).
- **Mandatory evidence-validator gate** — every cited file:line re-Read, drops if unfounded, status flips to `partial` on any drop.
- **Output shape**: `REPORT.md` + return contract YAML + deviation register + grounding-gaps + per-task verdicts array + optional Wave 7 promotion.

Effective reviewer count: **1 at T1; 2-3 at T2 (genuinely heterogeneous classes)**. ~3-8k Claude at T1; ~35-70k Claude at T2.

**This is the empirical-seed caller.** The 7.8 case was Reflect (1 reviewer) + Bare (1 reviewer) → 36% additive findings. That number is the high-water mark for the bare-adjunct value distribution.

### 2. What bare adds that isn't already there

| Dimension | Existing pipeline | What bare adds | Marginal value |
|-----------|-------------------|----------------|----------------|
| T1 reviewer count | 1 | +2/3 → 3-4 | The 7.8 case — strongest value mechanism |
| T2 reviewer count | 2-3 (already heterogeneous) | +2/3 → 4-6 | Diminishing — T2 already has model-class diversity |
| Vendor diversity at T2 | Optional (qwen/kimi if alias resolved) | Mandatory non-Anthropic if `--bare-reviewers > 0` | Strengthens an existing weak guarantee |
| `t2_vendor_diversity` field today | `single` (Anthropic-only) common case | `multi` after bare integration | Real — flips a known degraded telemetry to `full` |
| Library-doc grounding | Not in protocol; tech-research integration is `--depth deep` optional | `--bare-c7` makes it default per bare reviewer | Net new in T1; partial overlap with optional tech-research path in T2 |
| Protocol-vs-unstructured | T2 reviewers ARE protocol-driven (reflection rubric) | Bare = no protocol | Catches edge cases the rubric doesn't probe (this IS the 7.8 lesson) |
| Anti-self-confirmation | Executor-class exclusion + disjoint calibrator | + Distribution-diversity (non-Anthropic) | Strongest argument — the bare adjunct's purpose IS distribution-diversity |

**The honest summary:** Reflect already has the structural mechanisms bare-reviewer-adjunct was designed to add. Bare's marginal value on T2-reflect is LOWER than on auggie-review or code-review, but bare's marginal value on T1-reflect is the highest of any caller — T1 is structurally single-agent.

### 3. Concrete value mechanisms

**3.1 The 7.8 case generalized.** UC-2 post-execution audit at T1 is single-agent. Bare ensemble at T1 gives the empirically-proven 36% additive findings for cases where T1 confidence stays above the 0.90 floor and the rubric STOPs at T1. This is the strongest single value mechanism across all 5 callers.

**3.2 Cross-task interaction-effects scan (UC-2 tasklist-scope, Wave 1B.3).** When ≥3 tasks in a tasklist touch overlapping symbols, the existing scan flags cross-task risks. A bare-reviewer ensemble adds independent voting on whether the interaction is real, raising signal-to-noise on the synthetic invariant probe entries.

**3.3 `t2_vendor_diversity` flips from `single` to `multi`.** This is a real telemetry win, not a marketing one. The §11.0 warn today fires loudly when all aliases share one vendor; bare adjunct guarantees ≥1 non-Anthropic source.

**3.4 Wave 5 `input_drift_detected` cross-check.** Bare reviewers compute their own SHA snapshot of the target via the `target_checksum` frontmatter field. Cross-validating that checksum against reflect's `input_tree_sha256` adds a free integrity check (mismatched checksums catch a class of "files changed during the review" bugs).

**3.5 The 4-category deviation taxonomy.** Reflect's `Authorized expansion / Necessary deviation / Drift / Regression` classification is rubric-driven. Bare reviewers, lacking the taxonomy, will classify deviations differently — that's signal, not noise. The validator (with IMM-2 semantic-match) can reconcile.

### 4. Concrete cost mechanisms

| Phase | Existing (no bare) | With `--bare-reviewers 3` | With `--bare-reviewers 3 --bare-c7` |
|-------|-------------------|---------------------------|--------------------------------------|
| T1 only | ~3-8k Claude, 1-3 min | +45K external + ~10-15K orch, +30-70s | +53K external + ~13-18K orch, +60-130s |
| T2 (3 reviewers, no merge) | ~25-40k Claude, 5-9 min | +45K external + ~12-18K orch, +40-80s | +53K external + ~15-21K orch, +70-150s |
| T2 + adversarial merge | ~35-70k Claude, 7-14 min | +45K external + ~18-25K orch, +50-100s | +53K external + ~22-28K orch, +80-180s |
| Wave 7 promotion (UC-2) | +0 | unchanged (bare doesn't touch promotion) | unchanged |

T1-only is the cheap, common path. Bare on T1 is a ~2-3x cost multiplier — high, but the path is so cheap it remains affordable.

**T2 with bare adds 15-30% cost over T2-baseline.** This is the smallest relative cost of any caller because T2-reflect was already paying for full ensemble adversarial debate.

### 5. When bare adds the MOST value (reflect-specific)

1. **UC-2 audit at T1 (the 7.8 case).** Post-execution audits where the rubric STOPs at T1 because confidence ≥ 0.90 and scope ≤ 5 files. This is the highest-ROI scenario across all 5 callers.
2. **UC-2 audit with `interaction_effects_scanned: true`.** Cross-task interactions are the differentiating value of reflect; bare adds independent voting on whether the synthetic invariant entries are real.
3. **UC-2 with `regression_present: true` candidate.** Asymmetric-cost: a missed regression is far worse than the cost of bare adjunct. Rule 3 already escalates to T2 — bare adds further coverage.
4. **UC-1 spec-review at T1 where coverage ≥ 0.90 stops the rubric.** Edge-case coverage on specs is exactly what bare excelled at in 7.8.
5. **Pre-promotion gate runs (Wave 7).** UC-2 with promotion=on means the audit is load-bearing for repository mutation. Bare adjunct here is asymmetric-cost-positive even at full cost.

### 6. When bare adds the LEAST value (or negative)

1. **T2 runs that already have full vendor diversity** (`t2_vendor_diversity: multi` already). Bare's primary value mechanism is already satisfied.
2. **UC-1 with `coverage_undefined: true`.** No baseline to corroborate against; bare findings can't be Corroborated and most will be Demoted.
3. **`--no-evidence-validator` runs (debug only).** Without the gate, hallucinations leak straight into REPORT.md. Conditional-on-IMM-1/2 framing inverts to net-negative here.
4. **Promotion-target runs with destination collision risk.** The promotion gate's 9 conditions interact with bare-induced `status: partial`. A bare-caused partial blocks promotion that would otherwise succeed.
5. **Tier 1 STOP cases with `S_scope == 1` and trivial diff.** The rubric STOPs because it's truly trivial; bare adds noise to an already-cheap signal.

### 7. Recommended defaults

```yaml
recommended_defaults:
  default_bare_reviewers: 0           # off by default
  default_bare_c7: false              # off by default
  conditional_triggers:
    enable_when_user_should_opt_in:
      - "UC-2 post-execution audit (the 7.8 case)"
      - "UC-2 with interaction_effects_scanned=true and ≥3 tasks"
      - "UC-2 audit with --promote (promotion is load-bearing for mutation)"
      - "UC-1 with coverage_pct >= 0.90 at T1 (rubric would STOP otherwise)"
    avoid_when:
      - "T2 escalated AND t2_vendor_diversity already 'multi'"
      - "UC-1 with coverage_undefined=true"
      - "--no-evidence-validator"
      - "trivial UC-2 with S_scope=1"
  recommended_count: 3
  rationale: |
    Reflect's T1 path is structurally single-agent — bare ensemble there is the
    highest-ROI scenario of any caller. T2 already has 2-3 heterogeneous reviewers;
    bare's marginal yield there is real but smaller. N=3 balances both modes.
    N=2 would underweight the T1-only case; N=4 would over-spend on T2 paths.
```

### 8. Caller-specific gotchas

- **The `t2_effective_diversity` contract field.** When bare adjunct is on, this should flip to `full` (combining model + vendor axes). The integration must update reflect's contract schema to recognize bare-sourced reviewers as contributing to both axes.
- **UC-1 vs UC-2 distinction.** Bare reviewers receive the target without a UC-1/UC-2 hint. Their findings should be treated as schema-agnostic; UC-1 specifically benefits from coverage-style findings, UC-2 from deviation-class findings — the adversarial merge must NOT force a deviation-class on a UC-1 bare finding.
- **Executor-class exclusion (§7.1).** Bare reviewers are non-Anthropic, so they can never collide with the executor class (which is always Anthropic in practice). Bare adjunct effectively strengthens the executor-exclusion guarantee by definition — net positive on the anti-self-confirmation axis.
- **Wave 7 promotion gate's 9 conditions.** Condition 9 already gates `tier_reached == 2 AND convergence_score == null`. A bare-induced T2 escalation that fails to converge could block promotion. Document this loudly.
- **The 4-category deviation taxonomy mismatch.** Bare reviewers, lacking the taxonomy, will produce findings that don't map cleanly to Authorized/Necessary/Drift/Regression. The validator must default-classify them as `none` until a non-suspect source corroborates with a specific class — preventing hallucinated `regression_present: true` flags.

---

## /sc:code-review

### 1. What this caller already does

Per `bmad-code-review/SKILL.md` — the most adversarial of the four callers, by explicit design:

- **Three parallel review layers**: Blind Hunter (no context-anchoring), Edge Case Hunter (boundary/path-coverage), Acceptance Auditor (requirement-conformance).
- **Structured triage** into actionable categories.
- **Step-file architecture**: each step is a self-contained micro-file, executed sequentially. (Per `steps/step-02-review.md` and `steps/step-04-present.md`, the protocol is BMAD-style — workflow-driven, not LLM-orchestrated.)
- **Greeting + context gathering + persistent facts pattern.** The caller's runtime cost is dominated by the three parallel review layers + triage.

Effective reviewer count: **3 (Blind Hunter, Edge Case Hunter, Acceptance Auditor)**, all Anthropic-trained, all running in parallel. ~30-50k Claude tokens, 5-10 min wall-clock.

**This is the only caller with an explicitly-named adversarial structure built-in.**

### 2. What bare adds that isn't already there

| Dimension | Existing pipeline | What bare adds | Marginal value |
|-----------|-------------------|----------------|----------------|
| Reviewer count | 3 (Blind, Edge, Acceptance) | +2/3 → 5-6 | Lowest marginal yield of any caller — already saturated |
| Reviewer-stance diversity | 3 explicit adversarial stances | Bare adds an UNSTRUCTURED stance | Real but narrow — only catches what the 3 stances don't probe |
| Training-distribution diversity | All Anthropic | DeepSeek/Qwen/Kimi/GLM | Genuine — different bug-class blindspots |
| Triage classification | Structured into named categories | Bare findings would need re-classification | Net NEGATIVE on triage workflow — bare findings don't align to category schema |
| Library-doc grounding | None in current pipeline | `--bare-c7` injects docs per reviewer | Net new — strongest single argument for bare on code-review |
| Edge-case coverage | Edge Case Hunter explicit | Bare overlaps heavily with Edge Case Hunter | Mostly redundant |
| Acceptance-criteria check | Acceptance Auditor explicit | Bare ignores AC schema | Net negative for AC compliance findings |

**The honest summary:** code-review is the WORST fit for bare adjunct among the 4 callers, because its existing structure already satisfies the diversity-of-stance goal that bare provides. The one genuine value-add is `--bare-c7` for library-docs (which the existing 3-layer pipeline does NOT do).

### 3. Concrete value mechanisms

**3.1 Cross-vendor agreement on a Blind Hunter / Edge Case Hunter finding.** When the existing 3 reviewers agree on a finding, the agreement is within-Anthropic-distribution. A non-Anthropic bare reviewer corroborating that finding raises confidence meaningfully. This is real but quantitatively small.

**3.2 `--bare-c7` library-doc grounding.** This is the strongest argument for bare on code-review. The existing 3-layer pipeline does NOT pull library docs. For diffs that upgrade dependencies or use new framework APIs, bare-with-c7 catches API drift / deprecations that all three existing reviewers miss.

**3.3 Catching the protocol-blindspot.** All 3 existing reviewers operate under the BMAD workflow protocol. They share protocol-induced blindspots. Bare without protocol catches the 7.8-style edge cases the structured 3 miss — but the Edge Case Hunter is specifically designed to do this. Marginal yield is lower than on callers without an explicit Edge Case Hunter (i.e., everywhere else).

**3.4 Distribution diversity in language-specific bug classes.** Anthropic models may underperform on niche language patterns (Rust trait bounds, Haskell type-class resolution, etc.). Non-Anthropic models with different training corpora may flag these — most relevant in language-niche diffs.

### 4. Concrete cost mechanisms

| Phase | Existing (no bare) | With `--bare-reviewers 3` | With `--bare-reviewers 3 --bare-c7` |
|-------|-------------------|---------------------------|--------------------------------------|
| 3-layer parallel review | ~30-50k Claude, 5-10 min | +45K external + ~10-15K orch, +30-70s | +53K external + ~13-18K orch, +60-130s |
| Triage step | ~5-10k Claude, 1-2 min | +5-8K orch to re-classify bare findings | +5-8K orch (same) |
| Present step | ~3-5k Claude, <1 min | +1-2K orch (more findings to surface) | +1-2K orch (same) |

Bare adds ~1.2-1.4x cost on a caller that already has the highest reviewer count among the 4. The marginal yield is the lowest of any caller per dollar spent.

### 5. When bare adds the MOST value (code-review-specific)

1. **Diffs that touch third-party library APIs** (dependency upgrades, new framework imports). `--bare-c7` is the only mechanism in code-review's stack that pulls library docs.
2. **Diffs in language-niche code** (Rust, Haskell, OCaml, etc.) where Anthropic-distribution blindspots are most pronounced.
3. **Diffs from new contributors** where structural-stance diversity from 3 layers may still miss conformance issues a distribution-diverse model catches.
4. **Security-sensitive diffs** (auth, crypto, input validation) — distribution-diverse models may flag different threat-model gaps than the security-focused subset of the existing 3.
5. **Cross-cutting refactors touching ≥5 files** where the Edge Case Hunter's per-hunk coverage may miss integration-level issues a fresh-eyes bare reviewer catches.

### 6. When bare adds the LEAST value (or negative)

1. **Diffs caught fully by the existing 3 layers.** Adding 3 more reviewers to a saturated coverage is pure cost.
2. **Trivial diffs** (typo fixes, single-line bugs). All 4 of code-review's bare-irrelevant criteria fire.
3. **Triage-heavy workflows.** The bmad-code-review triage step expects categorized findings; bare findings need re-categorization, adding workflow friction.
4. **Acceptance-criteria-driven reviews.** Bare ignores the AC schema; its findings could distract from AC-conformance focus.
5. **Step-file architecture's discipline.** code-review's micro-file steps assume specific reviewer output shapes; bare's compressed-markdown template may not align cleanly with the step-04 present format.

### 7. Recommended defaults

```yaml
recommended_defaults:
  default_bare_reviewers: 0           # off by default — strongest off-default of any caller
  default_bare_c7: false              # off by default
  conditional_triggers:
    enable_when_user_should_opt_in:
      - "Diff touches dependency upgrade or new library import (then enable --bare-c7 specifically)"
      - "Diff in language-niche code (Rust/Haskell/OCaml/Zig/etc.)"
      - "Security-sensitive surface (auth/crypto/input validation)"
    avoid_when:
      - "Diff caught with high confidence by all 3 existing layers"
      - "Trivial diff (typo/single-line)"
      - "Triage workflow downstream of code-review (re-categorization cost)"
  recommended_count: 2
  rationale: |
    Code-review is the most-saturated reviewer caller. N=2 instead of 3 acknowledges
    that the 3 existing layers + 2 bare = 5 total reviewers is already at the saturation
    knee of the marginal-yield curve. The primary value of bare on code-review is c7
    library-doc grounding (which is per-reviewer-independent), not reviewer count.
```

### 8. Caller-specific gotchas

- **The triage step expects categorized findings.** Bare findings come in the compressed-markdown template's `Sev` enum (crit/high/med/low/nit), not the bmad triage categories. The integration MUST add a triage-mapping step or the triage workflow breaks.
- **Step-file architecture's "execute one step at a time" rule** (§Critical Rules). Spawning bare reviewers inline during step-02 may violate the sequential-execution constraint. The integration must spawn bare as a parallel sub-step within step-02, NOT as a new step file.
- **Customize.toml override pattern.** code-review's BMAD customization (base → team → user) controls workflow blocks. The `--bare-reviewers` flag needs to be a customize.toml override candidate so teams can default it on/off per repo.
- **No native PR-post mode (unlike auggie-review).** code-review presents findings via step-04-present, not GitHub PR comments. The IMM-1/IMM-2 PR-post-strict-mode concern from auggie-review does NOT apply directly to code-review — bare's hallucinated findings would surface to the user interactively, where they can be dismissed. The PR-post risk is lower here.
- **The 3-layer structure was empirically chosen (Blind/Edge/Acceptance).** Adding more layers (bare) without reconsidering the 3-layer choice may dilute the workflow's design intent. Document that bare is an *adjunct to the 3 layers*, not a *replacement for one of them*.

---

## /sc:tech-research

### 1. What this caller already does

Per `tech-research/SKILL.md` — fundamentally different shape: this is a research producer, not a finding emitter:

- **Stage A: Scope discovery + MDTM task-file creation.** Parses the research question, performs codebase scope discovery, writes a research-notes.md file, builds a TASK-RESEARCH MDTM file via rf-task-builder.
- **Stage B: Multi-phase execution via MDTM checklist.**
  - Phase 2: 5-10+ parallel Codebase Research Agents (Code Tracer / Doc Analyst / Integration Mapper / Pattern Investigator / Architecture Analyst) — each writes findings to a research file.
  - Phase 3: `rf-analyst` + `rf-qa` parallel research-gate (completeness + evidence-quality).
  - Phase 4: 1-4 parallel Web Research Agents.
  - Phase 5: Synthesis agents (one per report section) + `rf-analyst` + `rf-qa` synthesis-gate.
  - Phase 6: `rf-assembler` (single agent) → `rf-qa` report-validation → `rf-qa-qualitative` qualitative review.
- **Output shape**: `RESEARCH-REPORT-{descriptor}.md` — a multi-section structured report with findings, gap analysis, options, implementation plan, evidence trail. Persistent artifacts in `.dev/tasks/to-do/TASK-RESEARCH-*/`.

Effective reviewer count: **0 reviewers in the bare-adjunct sense**. tech-research is a *research producer*, not a *reviewer*. It has QA agents (rf-analyst, rf-qa, rf-qa-qualitative) but these are *quality gates on the research output*, not *reviewers of code under inspection*.

This is the most-different caller of the 5.

### 2. What bare adds that isn't already there

| Dimension | Existing pipeline | What bare adds | Marginal value |
|-----------|-------------------|----------------|----------------|
| Codebase Research Agents | 5-10+ (Anthropic, specialized) | +2/3 bare codebase reviewers | Bare reviewers don't follow the Incremental File Writing Protocol — incompatible by default |
| Web Research Agents | 1-4 (Anthropic with WebSearch) | Bare has no web access via the proxy | Net negative — bare can't replicate the web research role |
| Synthesis Agents | Per-section, structured | Bare doesn't follow synthesis schema | Net negative for synthesis |
| QA Layers (rf-analyst, rf-qa, rf-qa-qualitative) | 3 quality gates with specific checklists | Bare doesn't fit QA-gate semantics | Mismatch — bare emits findings, QA validates findings |
| Library-doc grounding for new tech research | Implicit via Web Research Agents | `--bare-c7` injects docs proactively | Real but already covered by web research |
| Adversarial review of the assembled report | rf-qa-qualitative does this | Bare review of the report itself | Possible value — see §3 |

**The honest summary:** tech-research's main pipeline (research → synthesis → assembly → QA) does NOT have a natural slot for bare-reviewer-as-adjunct. The ONLY potentially-applicable insertion point is **adversarial review of the assembled RESEARCH-REPORT-{descriptor}.md before user delivery** — and that role is already filled by rf-qa-qualitative.

**Bare-on-tech-research is the weakest fit of the 5 callers.**

### 3. Concrete value mechanisms (limited)

**3.1 Bare review of the final RESEARCH-REPORT as a post-Phase-6 adjunct.** After rf-qa-qualitative passes, bare reviewers could read the final report and flag patterns the qualitative QA missed (the same 7.8 dynamic — qualitative review with structured checklist vs unstructured probing). This is the ONLY clean insertion point.

**3.2 `--bare-c7` injecting library-docs during Phase 4 web research.** Marginal because web research already covers external docs. The genuine net-new value is when the bare reviewer's c7-fetched docs surface deprecations the WebSearch-using web researcher missed.

**3.3 Cross-vendor distillation of recommendations.** When Phase 5 synthesis produces "Recommendation: do X," bare reviewers reading the recommendation may flag distributional concerns (e.g., "this pattern is being deprecated in the Rust ecosystem"). Possible — but the rf-qa-qualitative agent is supposed to catch this.

**3.4 Adversarial probe of the Evidence Trail (Section S10).** Bare reviewers could probe whether the cited evidence supports the claims, mirroring evidence-validator semantics applied to a research report. This is structurally meaningful but operationally redundant.

### 4. Concrete cost mechanisms

| Phase | Existing (no bare) | With `--bare-reviewers 3` (post-Phase 6) |
|-------|-------------------|------------------------------------------|
| Phases 1-6 (full pipeline) | ~80-200k Claude (deep tier), 30-60 min | unchanged |
| Bare review of final report | — | +45K external + ~15-20K orch, +60-90s |

Bare on tech-research adds ~5-15% relative cost on what's already an expensive pipeline. The cost ratio is the most favorable of any caller — but the value ratio is the worst. **Bare on tech-research is the most-likely caller to be net-zero in practice.**

### 5. When bare adds the MOST value (tech-research-specific)

1. **Deep-tier research reports where the recommendation drives a major architectural decision.** Asymmetric-cost: getting the recommendation wrong is expensive enough that any additional adversarial review is justified.
2. **Reports where SOLUTION_RESEARCH (research notes Section 3) evaluated multiple approaches** — bare reviewers reading the options analysis may flag distributional concerns about each option.
3. **Reports where the codebase under research uses bleeding-edge framework versions** — `--bare-c7` catches deprecations the web researcher's training-cutoff missed.
4. **Feasibility studies** where the report concludes "yes, this is feasible" — bare adversarial probe of the feasibility argument adds genuine devil's-advocate signal.
5. **Reports consumed downstream by other tech-research or tech-reference invocations** — quality compounds; bare adjunct's signal carries through.

### 6. When bare adds the LEAST value (or negative)

1. **Quick-tier research** (narrow questions, <5 files). The whole pipeline is sub-15-minute; bare adds 60-90s without proportional value.
2. **Research that produces understanding, not recommendation.** When the report is "how does X work," there's no decision under adversarial pressure.
3. **Pure-codebase research with no external dependencies.** `--bare-c7` adds nothing; bare's distribution-diversity adds little when the codebase is the source of truth.
4. **Reports already consumed by /tech-reference downstream.** tech-reference is itself a structured workflow with its own validation; bare on tech-research, then bare on tech-reference, is double-counting.
5. **Reports where the rf-qa-qualitative agent flagged ZERO issues.** When the qualitative QA passes cleanly, bare adjunct is mostly redundant.

### 7. Recommended defaults

```yaml
recommended_defaults:
  default_bare_reviewers: 0           # off by default — strongest case for off-by-default
  default_bare_c7: false              # off by default
  conditional_triggers:
    enable_when_user_should_opt_in:
      - "Deep-tier research driving architectural decision"
      - "Multi-option feasibility study"
      - "Research on bleeding-edge framework/library versions (then --bare-c7)"
    avoid_when:
      - "Quick-tier research"
      - "Understanding-only output type"
      - "Standard-tier research without external dependencies"
      - "rf-qa-qualitative passed with zero findings"
  recommended_count: 2
  rationale: |
    Tech-research is a research-producer, not a finding-emitter. Bare adjunct has no
    natural slot in the pipeline — it can only operate as a post-Phase-6 adjunct
    reading the final report. N=2 acknowledges the limited value: bare provides
    cross-vendor cross-validation of the recommendation, not parallel research
    capacity. Going to 3+ adds cost without proportional yield. The
    rf-qa-qualitative agent IS the natural reviewer; bare adds distribution-diversity
    on top of it, nothing more.
  integration_pattern: |
    Insert bare AFTER Phase 6 (rf-qa-qualitative passes), BEFORE Phase 7 (present
    to user). Bare reviews the assembled RESEARCH-REPORT-{descriptor}.md as its
    target. Findings feed sc-adversarial-protocol merge with the rf-qa-qualitative
    report as the non-suspect source. Validator-gated as per spec §5.4.
```

### 8. Caller-specific gotchas

- **MDTM task-file architecture.** tech-research is MDTM-driven; bare adjunct must be inserted as a checklist item in the MDTM file, not as a workflow-orchestrated step. The rf-task-builder must be aware of bare-adjunct semantics or the integration cannot be granular per A3 rule.
- **Resumability.** MDTM resumability assumes checked items don't re-run. Bare reviewers run via external proxy — if the session restarts mid-bare-dispatch, the unchecked items resume, but the proxy may bill again. Mitigation: bare-dispatch should write its output files before checking the item, ensuring idempotency.
- **rf-qa-qualitative overlap.** rf-qa-qualitative explicitly checks for "circular reasoning, evidence trail completeness, conclusion proportionate to evidence strength" — exactly the patterns bare reviewers probe. The integration must position bare as ADJUNCT (after qualitative), not REPLACEMENT.
- **No PR-post mode.** tech-research outputs a report file, not a PR comment. IMM-1/IMM-2 PR-post-strict concerns from auggie-review do NOT apply. Bare adjunct is artifact-only by construction here — the lowest-risk integration mode of any caller.
- **The 4 QA checklists (analyst, rf-qa research-gate, rf-qa synthesis-gate, rf-qa report-validation).** Bare findings don't map to any of these checklists. Treat bare as a 5th informal review layer whose findings get appended to qa/ as bare-review-*.md files, parallel to the existing QA reports.
- **Token cost dominance.** tech-research is the most-expensive caller (~80-200k Claude on deep tier). Bare's relative cost is smallest here, but in absolute terms a deep-tier tech-research run with bare adjunct may exceed $1 of external proxy cost per invocation.

---

## Cross-Caller Comparison

### Recommended defaults summary

| Caller | Default `--bare-reviewers` | Default `--bare-c7` | Conditional triggers | Notes |
|--------|----------------------------|---------------------|----------------------|-------|
| /sc:auggie-review | 0 | false | Library-heavy diffs, cross-cutting refactors, security-sensitive surfaces, new contributors | Strongest single argument: `--bare-c7` covers a real gap (library docs). PR-post mode blocked until IMM-1/IMM-2 ship. |
| /sc:troubleshoot | 0 | false | `--type test` flaky bugs, library-version regressions, `--depth deep`, P0 incidents | Highest-value insertion at T1 (single-hypothesis path); diminishing returns at T2. |
| /sc:reflect | 0 | false | UC-2 audit at T1 (the 7.8 case), interaction-effects scans, pre-promotion gates | The empirical-seed caller — T1 ROI is the HIGHEST of any caller per dollar. T2 marginal yield is lowest because structure already optimal. |
| /sc:code-review | 0 | false | Dependency upgrades, language-niche code, security surfaces | Worst overall fit — the 3-layer adversarial structure already saturates. Only `--bare-c7` is genuinely net-new. Use N=2 not N=3. |
| /sc:tech-research | 0 | false | Deep-tier architecture-driving research, multi-option feasibility, bleeding-edge libraries | Weakest fit — research-producer not finding-emitter. Only valid insertion point is post-Phase-6 adjunct. Use N=2 not N=3. |

**Note:** All defaults are `0` (off). This is consistent across all 5 callers and aligns with the spec's §6.4 "Disabled-by-default" rationale (external proxy cost is non-trivial, latency higher, many calls don't need diversity). Differentiation across callers happens via the recommended *opt-in count* (2 or 3) and the *conditional triggers* set.

### Pattern observations across callers

1. **Callers with existing adversarial structure need bare LESS than single-reviewer callers.** code-review (3 layers) and reflect-at-T2 (heterogeneous 2-3 reviewers) have the lowest marginal yield. troubleshoot-at-T1 and reflect-at-T1 (single reviewer) have the highest.

2. **The single highest-ROI scenario across all 5 callers is reflect-at-T1 on UC-2 post-execution audit.** This is the 7.8 case generalized; ~36% additive findings at the empirical baseline. No other caller has this combination of (cheap baseline) × (single reviewer) × (high-value output).

3. **`--bare-c7` is the consistent net-new value across all callers** because none of the existing pipelines pull library docs systematically (reflect's tech-research integration is `--depth deep` optional only; auggie-review, troubleshoot, code-review pull context7 only opportunistically; tech-research pulls via web research, which has training-cutoff exposure).

4. **IMM-1 and IMM-2 are blockers for the PR-post-like modes only.** Among the 5 callers: auggie-review (PR-post mode) is the one impacted directly. Troubleshoot's potential auto-post to issue comments is the second risk surface. The other 3 callers (reflect, code-review, tech-research) are artifact-only by default — bare adjunct's hallucination risk is consumed by a human under caveat, not auto-posted.

5. **Wall-clock cost delta is dominated by parallel-dispatch latency (~30-90s) regardless of N.** Token cost scales linearly with N. This means N=2 vs N=3 vs N=4 has minimal wall-clock difference but meaningful token-cost difference. Recommended counts of 2 vs 3 are the meaningful axis.

6. **Validator-gating reliability matters MORE for callers where bare findings flow into asymmetric-cost flags.** Troubleshoot's `test_is_wrong` / `behavior_is_documented` and reflect's `regression_present` / `unauthorized_deviation_present` are downstream-load-bearing. Bare's hallucinations on these flags are worse than no bare adjunct.

7. **Reflect's mandatory evidence-validator gate is the BEST safety match for bare adjunct.** The pipeline already drops unfounded citations; adding bare's gate-and-suspect-tag layer composes cleanly. Code-review's triage step has the worst safety match — bare findings don't align to triage categories.

8. **Cost-to-value ratio across callers** (best to worst):
   - **Best**: reflect-T1 UC-2 audit (high value, cheap baseline)
   - Good: troubleshoot-T1 `--type test` (moderate value, cheap baseline)
   - Moderate: auggie-review library-heavy PR with `--bare-c7` (moderate value, moderate baseline)
   - Lower: code-review on language-niche code (low marginal yield, expensive baseline)
   - **Worst**: tech-research without architectural-decision driver (negligible marginal value, expensive baseline)

9. **The A/B test proposed in auggie-review-integration-evaluation.md §9 should run on reflect-T1 first**, not auggie-review. The empirical seed is reflect-based; the cost/baseline ratio is most favorable there; the resulting numerical estimates will be the cleanest signal for default-tuning across all 5 callers.

10. **Default-on cases.** None of the 5 callers should default `--bare-reviewers > 0` today. Post-IMM-1/IMM-2 and post-A/B test on reflect-T1, the strongest candidate for default-on is reflect's UC-2 post-execution audit at T1 with N=3. That's a future change, not a v1.0 ship change.

---

*Evaluation produced 2026-05-28T05:50Z. Honest framing: bare-reviewer-adjunct's value is real but conditional on (a) validator quality (IMM-1, IMM-2), (b) caller's existing reviewer count, (c) cost-baseline ratio. The empirical seed scenario (reflect-T1 UC-2) is the strongest case for bare adjunct anywhere in the SuperClaude pipeline; tech-research is the weakest. The cross-caller pattern is clear: bare adds the MOST value where existing structure is single-reviewer and the cost-baseline is cheap, and the LEAST value where existing structure is multi-reviewer-adversarial and the cost-baseline is expensive.*
