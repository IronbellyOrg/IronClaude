---
spec_id: AB-TEST-T2-BARE-REVIEWER
spec_version: 1.0.0-draft
date: 2026-05-28T05:55Z
status: ready-for-execution
spec_source: /config/workspace/IronClaude/.dev/brainstorms/20260528030000-t2-bare-reviewer-adjunct/merged-requirements.md (v1.3.0-draft)
empirical_seed: TUIBBS 7.8 review experiment (2026-05-28 00:30-00:50)
test_population_target: /sc:reflect (NOT /sc:auggie-review — per multi-caller evaluation redirect)
estimated_cost: ~$60
estimated_duration: ~1 day execution + ~1 day analysis
---

# A/B Test Harness — T2 Bare-Reviewer Adjunct

> **Why /sc:reflect (not /sc:auggie-review):** The `multi-caller-integration-evaluations.md` analysis identified reflect-T1 (UC-2 post-execution audit) as the highest-ROI test population: it's the empirical seed (the 7.8 experiment was reflect-shaped), it has the most favorable cost ratio (cheapest baseline + largest delta), and it has the clearest marginal-yield signal. Auggie-review can be re-tested as a secondary population if reflect-T1 confirms positive ROI.

---

## 1. Test Question

**Primary:** Does adding 3 parallel non-Anthropic bare reviewers to `/sc:reflect` produce findings that the structured reflect pass alone does not produce, at a quality level worth the cost?

**Secondary:** Does `--bare-c7` enrichment (context7 + auggie doc grounding) further increase the rate of high-quality novel findings?

**Tertiary:** What should the production default for `--bare-reviewers N` be? (Currently spec says 0; tests will inform if a non-zero default is justified.)

---

## 2. Test Design

### 2.1 Arms

| Arm | Configuration | Hypothesis |
|-----|--------------|------------|
| **A — Baseline** | `/sc:reflect --type task --analyze --validate` | Existing structured pass; no bare adjunct |
| **B — Bare, no c7** | `+ --bare-reviewers 3` | Bare diversity adds findings without c7 grounding |
| **C — Bare + c7** | `+ --bare-reviewers 3 --bare-c7` | c7 doc grounding catches library-specific issues that all-Anthropic miss |

Each fixture (per §3) is run through ALL THREE arms in independent invocations. The outputs are compared as a triplet, not pooled.

### 2.2 Reviewer rotation

Per T2Model env vars, the three bare reviewers per Arm B / Arm C are:
- T2Model01 = `deepseek-v4-pro`
- T2Model02 = `qwen3.6-plus`
- T2Model03 = `kimi-k2.6`

T2Model04 (`glm-5.1`) is HELD IN RESERVE — used only if one of the primary three fails (per `--reviewers 3` partial-OK semantics).

---

## 3. Test Population (20 fixtures)

### 3.1 Selection criteria

Sample from recently-completed stories/tasks/audits in the active project that match:
- Have a clear post-execution artifact (completed code + spec + tests)
- Have already passed a human review
- Cover a representative mix of trivial / medium / complex implementations

### 3.2 Fixture distribution

| Bucket | Count | Definition |
|--------|-------|------------|
| Trivial | 5 | <50 LOC change, single-file, low review-effort baseline |
| Medium | 10 | 50-300 LOC, 2-5 files, moderate review-effort baseline |
| Complex | 5 | >300 LOC, ≥5 files, multi-component or new-pattern introduction |

This distribution roughly matches the 7.8 case's "medium" complexity (200-500 LOC, single story, moderate review depth).

### 3.3 Concrete fixture suggestions

From TUIBBS (the empirical-seed project):
- Story 7.7 KeyHintBar (medium)
- Story 7.8 MCITemplate (medium — the empirical seed itself)
- Story 7.5 closure (medium)
- Story 7.6 NoColor (medium)
- (And ~16 more from across the project history)

Document the chosen 20 in `<test-output>/fixture-manifest.md` before running.

### 3.4 Exclusions

- Fixtures with no library imports (c7 gets `skipped_no_candidates`; biases against Arm C)
- Fixtures where a human reviewer rejected the work (we want passed-review baseline)
- Auto-generated code (bare reviewers flag intentional patterns as issues)

---

## 4. Measurements (per fixture × arm)

### 4.1 Quantitative

| Metric | Source | Type |
|--------|--------|------|
| `findings_count_total` | Output count of all surfaced findings | int |
| `findings_count_validated` | Verdict=Validated (per IMM-2 semantic-match) | int |
| `findings_count_corroborated` | Verdict=Corroborated (per IMM-1 ≥1 non-suspect rule) | int |
| `findings_count_demoted` | Verdict=Demoted | int |
| `findings_count_dropped` | Verdict=Dropped | int |
| `findings_count_contradicted` | Verdict=Contradicted | int |
| `novel_findings_vs_A` | (Arms B, C only) — findings present in this arm but not in Arm A | int |
| `wall_clock_seconds` | Total invocation latency | float |
| `cost_usd_estimate` | Token cost: Anthropic tokens × rate + proxy tokens × rate + c7 cost | float |
| `c7_synthesis_token_count` | (Arm C only) — size of SYNTHESIS.md body | int |

### 4.2 Qualitative (human-rated per finding)

Each unique finding (deduplicated across arms) rated on a 3-point scale by ONE human reviewer:

| Rating | Meaning |
|--------|---------|
| **Agree** | This is a valid issue worth surfacing |
| **Partial** | There's something here but the finding is imprecise or off-target |
| **Disagree** | This is wrong, irrelevant, or noise |

**Human-rater discipline:**
- Rate without knowing which arm produced the finding (blinding)
- One pass per fixture across all unique findings; cross-arm comparison computed after
- Budget: ~30 min per fixture × 20 fixtures = ~10 hours human time

### 4.3 Derived per-arm metrics

- `signal_rate_per_arm = Agree_count / findings_count_total`
- `noise_rate_per_arm = Disagree_count / findings_count_total`
- `novel_signal_rate_per_arm = Agree_AND_novel_count / findings_count_total` (Arms B, C only)
- `cost_per_novel_finding = total_cost / Agree_AND_novel_count` (Arms B, C only)

---

## 5. Decision Criteria

### 5.1 Primary decision: enable bare-reviewers default

| Outcome | Action |
|---------|--------|
| Arm B `novel_signal_rate ≥ 0.20` (≥1 in 5 novel findings is genuine) AND `noise_rate ≤ 0.30` | Default `--bare-reviewers 3` on reflect-T1 |
| Arm B `novel_signal_rate < 0.20` OR `noise_rate > 0.30` | Keep `--bare-reviewers 0` default; bare is opt-in only |

### 5.2 Secondary decision: enable c7 default

| Outcome | Action |
|---------|--------|
| Arm C `novel_signal_rate` is ≥0.10 higher than Arm B's | Default `--bare-c7` ON when `--bare-reviewers > 0` |
| Arm C `novel_signal_rate` ≤ Arm B's + 0.05 | c7 stays opt-in (`--bare-c7` default off) |
| Arm C `novel_signal_rate` between B+0.05 and B+0.10 | Inconclusive — repeat test with 20 more fixtures OR ship default-off |

### 5.3 Abort criteria

| Trigger | Action |
|---------|--------|
| Arm B or C produces `noise_rate > 0.50` (more disagree than agree on bare-novel findings) | ABORT bare adjunct integration entirely; revisit spec |
| Cost-per-novel-finding > $1.00 (USD) | ABORT — economics don't work even if signal is real |
| Validator IMM-2 (semantic-match) rejects >80% of suspect findings | ABORT — validator is over-rejecting; revisit IMM-2 threshold |

---

## 6. Execution Protocol

### 6.1 Sequence

1. **Pre-flight (Day 0)** — fixture selection committed to `fixture-manifest.md`; T2 proxy stood up; T2Model01..04 verified resolving.
2. **Run Arm A baseline** — 20 fixtures × Arm A = 20 invocations. Wall clock ~1 hour at avg 3 min/run.
3. **Run Arm B** — 20 invocations. Wall clock ~1.5 hours at avg 5 min/run.
4. **Run Arm C** — 20 invocations. Wall clock ~2 hours at avg 6 min/run.
5. **Deduplicate findings** — across all 60 outputs (20 fixtures × 3 arms), build a unique-finding index. Each unique finding tagged with which arms produced it.
6. **Human rating** — single reviewer rates each unique finding blind to arm. ~10 hours.
7. **Compute metrics** — derived per-arm metrics per §4.3.
8. **Decision** — apply §5 criteria; document outcome in `decision-record.md`.

### 6.2 Total cost budget

| Cost type | Estimate |
|-----------|----------|
| Anthropic tokens (60 invocations, baseline + adjunct) | ~$15 |
| Proxy tokens (Arms B + C, 40 invocations × 3 reviewers × ~$0.10) | ~$12 |
| c7 calls (Arm C, 20 invocations × ~$0.05) | ~$1 |
| **Subtotal compute** | **~$28** |
| Human review time (10 hours × hourly rate) | $30-200 depending on rate |
| **Estimated total** | **~$60-230 depending on labor** |

§5 abort criteria gate against runaway cost.

---

## 7. Output Artifacts

```
<test-output>/
├── fixture-manifest.md              (the chosen 20 fixtures + rationale)
├── arm-A-baseline/
│   ├── fixture-NN/                  (one per fixture)
│   │   ├── invocation.log
│   │   ├── findings.md              (reflect output)
│   │   └── metrics.yaml
│   └── ...
├── arm-B-bare-no-c7/
│   └── ... (same structure)
├── arm-C-bare-with-c7/
│   └── ... (same structure)
├── unique-finding-index.md          (cross-arm deduplication)
├── human-ratings.csv                (per-finding agree/partial/disagree)
├── derived-metrics.yaml             (per-arm aggregated)
├── decision-record.md               (§5 criteria applied)
└── report.md                        (executive summary)
```

---

## 8. Threats to Validity

| Threat | Mitigation |
|--------|------------|
| Human rater bias (knows which arm) | Blind rating — strip arm identifiers from finding cards before review |
| Fixture selection bias (cherry-picked stories) | Random sample from passed-review work; document selection criteria; pre-commit to 20 before running |
| Model-specific anomalies in single run | Each fixture invoked ONCE per arm (not averaged); temperature 0.2 reduces variance but doesn't eliminate. Re-run any outlier (e.g., Arm B noise_rate > 0.50 on a single fixture) before deciding it's the model's fault |
| Validator IMM-1/IMM-2 implementation bugs | This A/B test is downstream of Phase 2 ship; validator is assumed correct. If validator is buggy, results are unreliable. Pre-flight check: validate IMM-1/IMM-2 against known-good and known-bad fixtures before running A/B |
| Cost overrun | §5.3 abort criteria + cost-per-fixture monitoring |
| Single human rater | One rater = consistent calibration but limited ground truth. For tighter results, recruit 2 raters and report inter-rater agreement. Cost: ~2× human time |

---

## 9. Follow-On Tests (if primary results justify)

If reflect-T1 A/B shows positive ROI:

| Follow-on | Population | Why |
|-----------|------------|-----|
| Secondary test on /sc:auggie-review | 20 PRs | Confirm/refute the original §9 auggie-review evaluation hypothesis |
| Secondary test on /sc:troubleshoot | 20 bug reports | Evaluate Tier 1 vs Tier 2 differential value |
| Long-horizon test (3-month rolling) | Production usage | Confirm short-test results hold over time |

If reflect-T1 A/B shows negative ROI:

| Follow-on | Action |
|-----------|--------|
| Diagnose: is it bare quality or validator quality? | Run validator-only test with controlled inputs |
| Cost-cap re-test | Reduce `--target-line-cap` and re-run to see if cost-per-novel-finding improves |
| Different model mix | Try alternative T2Model combos (e.g., Mistral instead of DeepSeek) |

---

## 10. Reporting

Final `report.md` MUST include:

- 5-line executive summary (decision + key metrics)
- Per-arm metrics table (signal rate, noise rate, novel rate, cost)
- Cost-per-novel-finding chart across the 3 arms
- 3-5 representative finding examples (one Agree-novel from each arm; one Disagree-novel from each arm)
- Threats-to-validity addressed in this run
- Decision (per §5) with link to `decision-record.md`
- Recommended spec amendments (e.g., if Arm B passes but Arm C doesn't, update production defaults accordingly)

---

*A/B test harness spec authored 2026-05-28T05:55Z. Primary test target: /sc:reflect (redirected from /sc:auggie-review per multi-caller evaluation finding). Execution gated on Phase 1 + 1.5 + 2 ship.*
