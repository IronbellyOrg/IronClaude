---
variant: 2
lens: analyzer/eval-methodology
title: "Baseline-Anchored Evaluation Harness for Ataraxy-Labs Tool Incorporation"
release_area: "AtaraxyLabs eval + incorporation"
incorporation_order:
  - sem
  - inspect
  - weave
integration_mechanism: "hybrid: MCP registration plus framework-native skill wiring"
eval_scope: "framework-native first, then optional multi-repo generalization"
cost_lens: "all-in: tokens + latency + integration + maintenance"
stance: "vendor claims are hypotheses until re-measured on IronClaude data"
created: 2026-06-04
status: proposal_variant
---

# Variant 2: Analyzer Proposal — A Falsifiable Eval Harness Before Incorporation

## 0. Executive Thesis

The Ataraxy-Labs tools should not be incorporated because their upstream demos are impressive.

They should be incorporated only if they beat concrete IronClaude baselines on real IronClaude workflows.

The harness must therefore treat every vendor benchmark as a hypothesis:

- `sem` might reduce review-context tokens, but no public speed or token-reduction numbers exist.
- `inspect` claims high recall, but its precision is low and its judge is weak.
- `weave` claims dramatic conflict reduction, but our worktree patterns may not match its 31-scenario suite.

The release plan should be an evidence pipeline:

1. Measure the status quo.
2. Run the candidate tool in shadow mode.
3. Compare value and cost with identical inputs.
4. Require predeclared graduation thresholds.
5. Kill, defer, or incorporate based on observed deltas.

This proposal is intentionally conservative.

It does not optimize for fastest integration.

It optimizes for avoiding a false positive adoption decision.

## 1. Eval Philosophy

### 1.1 Vendor numbers are priors, not facts

The upstream claims become hypotheses to test.

They do not become acceptance criteria by themselves.

A tool graduates only when IronClaude-native measurements show it improves outcomes.

### 1.2 No metric without a baseline

Every metric must name its baseline.

A metric such as "tokens used" is incomplete.

A valid metric is "prompt input tokens vs current sc:auggie-review Auggie pass, measured on the same PR corpus."

### 1.3 No value metric without a cost metric

A tool that improves recall but doubles review latency may still fail.

A merge driver that avoids conflicts but requires fragile global setup may still fail.

A context extractor that saves tokens but hides the changed entity may still fail.

### 1.4 Shadow mode before replacement

The tools run beside current behavior first.

They do not gate reviews, block merges, or replace existing workflows during eval.

### 1.5 Framework-native first

The first corpus is this repository.

The first scenarios are actual IronClaude activities:

- PR review.
- Worktree merge.
- Entity diff.
- Cross-file impact analysis.
- LLM-context extraction.
- Roadmap and cleanup-audit diffs.

General multi-repo validation is a second phase, not the first proof point.

### 1.6 Independent judging only

The tools' own labels and judges are not trusted as ground truth.

Especially for `inspect`, keyword-matching benchmark judging is not sufficient.

The harness uses curated expected findings, human review, replayed historical outcomes, and independent LLM adjudication with blind inputs.

### 1.7 Reproducibility over anecdotes

A single impressive demo is not evidence.

Each score must be reproducible from stored inputs, commands, versions, and outputs.

### 1.8 Kill gates are first-class

The eval is allowed to reject tools.

The plan should not assume all three reach incorporation.

If `sem` fails, `inspect` and `weave` are paused because sem-core is the foundation.

## 2. Release Gating Model

### 2.1 Common phase shape per tool

Each tool follows the same release lifecycle:

1. Spike.
2. Harness integration.
3. Shadow eval.
4. Gated decision.
5. Skill wiring if passed.
6. Re-eval after wiring.
7. Keep, kill, or defer.

### 2.2 Dependency order

The order is fixed:

1. `sem`.
2. `inspect`.
3. `weave`.

This order is not merely operational.

It is methodological.

`sem` establishes whether entity extraction and token-budgeted context are valuable enough to justify the new Rust/toolchain surface.

`inspect` depends on the same entity worldview and must be evaluated after `sem` establishes extraction reliability.

`weave` has a different value surface, but its semantic merge credibility still depends on entity-level parsing and language support.

### 2.3 Graduation states

Each tool receives one of four verdicts:

- `kill`: do not integrate; document evidence and rollback.
- `defer`: promising but blocked by data volume, install risk, or unsupported workflow.
- `shadow_only`: register or script as advisory only; no user-facing replacement.
- `graduate`: wire into targeted skills with guarded defaults.

### 2.4 Minimum evidence before any graduation

No tool graduates with fewer than:

- 20 native PR/review cases or all available native cases if fewer exist plus synthetic backfill.
- 10 native or constructed merge cases for merge-specific evaluation.
- 5 manually curated high-risk diffs with ground-truth expected findings.
- One repeated-run stability pass across at least 3 executions on the same inputs.
- A documented rollback path.

If the repository lacks enough historical cases, the verdict cannot be stronger than `shadow_only` until synthetic and curated cases are clearly separated from real cases.

## 3. Scenario Matrix

The matrix is the core harness object.

Rows are scenarios.

Columns are tools and baselines.

Each cell declares whether the tool is a candidate, a comparator, or not applicable.

### 3.1 Matrix overview

| Scenario | Baseline A | Baseline B | sem | inspect | weave | Primary question |
|---|---|---|---|---|---|---|
| PR review triage | raw `git diff` | current `sc:auggie-review` Auggie pass | context supplier | risk comparator | n/a | Does entity awareness improve review finding quality per token? |
| Worktree merge | native `git merge` | manual conflict resolution | conflict explanation only | n/a | merge candidate | Does semantic merge reduce false conflicts without hiding true conflicts? |
| Entity diff | raw `git diff --stat` + file diff | current reviewer inspection | primary candidate | risk overlay | n/a | Does entity-level diff expose changed units more accurately? |
| Cross-file impact | grep/import/manual reasoning | Auggie retrieval | primary candidate | risk scoring consumer | n/a | Does impact graph identify affected dependents with useful precision? |
| LLM-context extraction | full diff + selected files | Auggie retrieval context | primary candidate | downstream reviewer | n/a | Does token-budgeted context preserve findings while reducing tokens? |
| Cleanup-audit diff | line diff + scanner output | current cleanup-audit flow | structural signal | risk prioritizer | n/a | Does entity granularity improve cleanup prioritization? |
| Roadmap scanner diff | line diff | current scanner detector output | structural signal | n/a | n/a | Does entity diff reduce false positives in roadmap change interpretation? |
| Large PR risk ranking | file count/LOC heuristics | Auggie review output | feature source | primary candidate | n/a | Does inspect rank the truly risky entities in top-N? |
| Unsupported language/file fallback | raw git behavior | current reviewer behavior | fallback candidate | fallback candidate | fallback candidate | Does fallback degrade safely? |
| MCP integration stability | no MCP server | Auggie MCP precedent | server candidate | server candidate | server candidate | Do stdio servers behave reliably under Claude Code usage? |

### 3.2 Scenario: PR review triage

Purpose:

Measure whether entity-aware tools improve PR review value.

Inputs:

- Historical IronClaude PR diffs.
- Current working-tree diffs from roadmap, cleanup-audit, and skill edits.
- Curated diffs with known defects.

Baselines:

- Raw `git diff` supplied to review prompt.
- Current `sc:auggie-review` Auggie pass.
- Existing `code-review` skill behavior where available.

Tools:

- `sem diff` and `sem context` as context suppliers.
- `inspect triage` and `inspect review` as risk filters or secondary reviewer.

Judgment:

- Finding recall against curated expected findings.
- Actionable precision from human or blind adjudicator.
- Token delta vs baseline.
- Latency delta vs baseline.
- Missed-critical count.

### 3.3 Scenario: Worktree merge

Purpose:

Measure whether `weave` reduces false conflicts in the worktree-heavy development model.

Inputs:

- Historical branch merges if available.
- Synthetic paired branches that edit independent functions in the same file.
- Synthetic paired branches that edit the same function incompatibly.
- Real unresolved conflict examples from recent release work if recoverable.

Baselines:

- Native `git merge`.
- Manual conflict resolution time.
- `git merge-file` behavior for controlled 3-way cases.

Tools:

- `weave preview`.
- Local-scoped `weave setup` only after preview success.

Judgment:

- False conflict reduction.
- True conflict preservation.
- Clean merge correctness.
- Regression rate.
- Setup and rollback reliability.

### 3.4 Scenario: Entity diff

Purpose:

Measure whether `sem diff` creates a better unit of review than line diff.

Inputs:

- Small single-function diffs.
- Multi-function same-file diffs.
- Cross-file class/function movement diffs.
- Formatting-only diffs.
- Generated or markdown-heavy diffs where tree-sitter support may be weak.

Baselines:

- `git diff --stat`.
- Raw unified diff.
- Human-labeled changed entities.

Tools:

- `sem diff`.
- `inspect diff` as a risk-weighted derivative where applicable.

Judgment:

- Entity detection recall.
- Entity boundary precision.
- Rename/move handling.
- Cosmetic-change suppression.
- Unsupported-file fallback safety.

### 3.5 Scenario: Cross-file impact

Purpose:

Measure whether impact graph output identifies useful downstream files/entities.

Inputs:

- Changes to CLI entry points.
- Changes to skill files.
- Changes to test fixtures.
- Changes to scanner logic.
- Changes to package metadata.

Baselines:

- Import graph/manual grep.
- Current Auggie retrieval.
- Test failure or affected-test mapping where available.

Tools:

- `sem impact`.
- `inspect risk_map` if it consumes dependents.

Judgment:

- Impact recall.
- Impact precision.
- Number of irrelevant dependents surfaced.
- Whether surfaced impact would change review/test selection.

### 3.6 Scenario: LLM-context extraction

Purpose:

Measure whether `sem context` reduces LLM prompt tokens without dropping necessary evidence.

Inputs:

- Diffs with changed entities smaller than budget.
- Diffs with changed entities larger than budget.
- Diffs requiring cross-file context.
- Diffs where bug evidence is outside the changed file.

Baselines:

- Full raw diff.
- Current `sc:auggie-review` Auggie output.
- Manual file-selection prompt.

Tools:

- `sem context` at multiple token budgets.

Judgment:

- Prompt input tokens.
- Finding recall at equal reviewer prompt.
- Critical evidence retention.
- Target-entity omission rate.
- Context construction latency.

### 3.7 Scenario: Cleanup-audit and roadmap diffs

Purpose:

Measure whether entity diff improves framework-native scanners and audit workflows.

Inputs:

- Roadmap scanner changes.
- Cleanup-audit detector changes.
- Markdown-heavy specs and generated artifacts.
- Diffs that move logic without changing semantics.

Baselines:

- Current scanner output.
- Current cleanup-audit output.
- Raw diff interpretation.

Tools:

- `sem entities`.
- `sem diff`.
- `sem impact`.
- `inspect triage` as prioritization only.

Judgment:

- Reduced false-positive review attention.
- Better mapping from changed code to changed detector behavior.
- Improved test selection.
- Latency and setup overhead.

### 3.8 Scenario: MCP integration stability

Purpose:

Measure whether stdio MCP servers are reliable enough for hybrid integration.

Inputs:

- Repeated server startup.
- Normal command calls.
- Missing binary conditions.
- Unsupported workspace conditions.
- Large diff inputs.

Baselines:

- Existing Auggie MCP registration precedent.
- No-server CLI-only invocation.

Tools:

- `sem-mcp`.
- inspect MCP binary.
- weave MCP binary after tool-name discovery.

Judgment:

- Startup success rate.
- Tool schema stability.
- Error clarity.
- Latency overhead vs CLI.
- Deregistration reliability.

## 4. Metric Catalog

### 4.1 Metric groups

The harness reports five metric groups:

1. Review quality.
2. Structural accuracy.
3. Merge correctness.
4. Cost and performance.
5. Operational maintainability.

Each group contains measurements with units, baselines, and thresholds.

### 4.2 Review-quality metrics

#### RQ-1 Finding recall

Definition:

Percentage of ground-truth findings identified by the workflow.

Unit:

Percent.

Baseline:

Current `sc:auggie-review` Auggie pass on the same diff.

Secondary baseline:

Raw `git diff` review prompt on the same diff.

Measurement:

`true_positive_findings / ground_truth_findings * 100`.

Graduation threshold:

- `sem context`: recall must be at least baseline minus 5 percentage points while reducing tokens by at least 30%.
- `inspect`: recall must exceed baseline by at least 10 percentage points for high-risk findings, or match baseline with at least 25% token reduction when used as pre-filter.
- `weave`: not applicable.

Failure threshold:

Any missed critical ground-truth finding in a curated high-risk case requires root-cause review and blocks graduation until fixed or bounded.

#### RQ-2 Actionable precision

Definition:

Percentage of reported findings judged actionable.

Unit:

Percent.

Baseline:

Current `sc:auggie-review` actionable precision.

Secondary baseline:

Inspect vendor-reported 33.3% precision treated as a prior, not an acceptance point.

Measurement:

`actionable_findings / total_reported_findings * 100`.

Graduation threshold:

- `inspect` advisory mode: at least 45% actionable precision on IronClaude corpus.
- `inspect` pre-filter mode: at least 55% precision among top-20 entities.
- Any replacement-like mode: at least baseline precision and no critical recall regression.

Failure threshold:

Precision below 33.3% on native corpus means the vendor prior was optimistic for us.

#### RQ-3 False-positive burden

Definition:

Number of non-actionable findings a human must inspect per PR.

Unit:

Count per PR.

Baseline:

Current review flow false-positive count per PR.

Measurement:

Non-actionable findings after deduplication.

Graduation threshold:

No more than baseline plus 2 false positives per medium PR.

For `inspect`, no more than 8 false positives per large PR when used as advisory.

Failure threshold:

Any mode that consistently creates more review work than it removes fails even if recall is high.

#### RQ-4 Critical miss count

Definition:

Number of severe known defects omitted by the tool or tool-assisted workflow.

Unit:

Count.

Baseline:

Current review miss count on curated replay cases.

Measurement:

Blind adjudication against ground-truth defect list.

Graduation threshold:

Zero critical misses that baseline catches.

Failure threshold:

One unbounded critical miss blocks replacement and limits the tool to advisory only.

#### RQ-5 Risk-ranking quality

Definition:

Quality of entity ordering by actual defect relevance.

Unit:

NDCG@K and recall@K.

Baseline:

File-size/LOC heuristic ranking.

Secondary baseline:

Current reviewer/Auggie-prioritized focus list where available.

Measurement:

Compare ranked entities to human-labeled risky entities.

Graduation threshold:

`inspect` must beat LOC heuristic by at least 20% NDCG@20 and must place all critical changed entities in top 60 on large PR cases.

Failure threshold:

If critical entities routinely fall outside top 60, top-60 review routing is unsafe for large PRs.

### 4.3 Structural-accuracy metrics

#### SA-1 Entity detection recall

Definition:

Percentage of human-labeled changed entities detected by entity tooling.

Unit:

Percent.

Baseline:

Human-labeled changed-entity list derived from raw diff.

Measurement:

`detected_changed_entities / labeled_changed_entities * 100`.

Graduation threshold:

`sem diff` must reach at least 90% recall on supported languages in native corpus.

Failure threshold:

Below 80% recall on Python or Markdown-adjacent framework workflows blocks skill wiring.

#### SA-2 Entity boundary precision

Definition:

Percentage of detected entities whose boundaries match human labels well enough for review context.

Unit:

Percent.

Baseline:

Human-labeled boundaries.

Measurement:

Boundary is correct if it includes the changed semantic unit without swallowing unrelated large regions.

Graduation threshold:

At least 85% boundary precision for supported-language code files.

Failure threshold:

Boundary precision below 75% means context extraction risks token waste and evidence distortion.

#### SA-3 Cosmetic-change suppression accuracy

Definition:

Ability to classify formatting-only or cosmetic changes as low risk.

Unit:

Percent accuracy.

Baseline:

Human-labeled cosmetic diff set.

Tool-specific note:

`inspect` danger formula applies cosmetic multiplier `*0.3`.

Graduation threshold:

Cosmetic cases should not exceed Medium tier unless public API or behavior changed.

Failure threshold:

More than 10% cosmetic cases ranked High or Critical blocks `inspect` review prioritization.

#### SA-4 Impact recall

Definition:

Percentage of actually affected downstream entities/files surfaced by impact tooling.

Unit:

Percent.

Baseline:

Manual import/test-impact map.

Secondary baseline:

Current Auggie retrieval references.

Graduation threshold:

`sem impact` must identify at least 70% of manually labeled high-value dependents.

Failure threshold:

Below 50% impact recall limits `sem impact` to exploratory use.

#### SA-5 Impact precision

Definition:

Percentage of surfaced impacted entities that are actually useful to review or test selection.

Unit:

Percent.

Baseline:

Manual impact map.

Graduation threshold:

At least 50% precision for high-value dependents.

Failure threshold:

If impact output is mostly noise, do not wire it into prompts.

### 4.4 Merge-correctness metrics

#### MC-1 False conflict reduction

Definition:

Reduction in conflicts where both branches can be merged without semantic conflict.

Unit:

Percent reduction vs native git.

Baseline:

Native `git merge` conflict count on same scenarios.

Vendor hypothesis:

`weave` claims approximately 95% conflict reduction.

Graduation threshold:

At least 60% false conflict reduction on IronClaude worktree corpus.

Stretch threshold:

At least 90% reduction on synthetic independent-function same-file cases.

Failure threshold:

Below 30% reduction on native or curated cases does not justify setup risk.

#### MC-2 True conflict preservation

Definition:

Percentage of real semantic conflicts still surfaced as conflicts.

Unit:

Percent.

Baseline:

Human-labeled true conflict set.

Graduation threshold:

100% preservation in curated true-conflict cases.

Failure threshold:

Any silent auto-merge of a true semantic conflict blocks `weave setup` adoption.

#### MC-3 Clean merge correctness

Definition:

Percentage of tool-produced clean merges that pass expected tests and human semantic inspection.

Unit:

Percent.

Baseline:

Native git clean merge correctness.

Vendor hypothesis:

`weave` claims 100% clean on 31 scenarios vs git 48%.

Graduation threshold:

At least 95% correctness on native/synthetic merged corpus.

Failure threshold:

Any incorrectly clean merge in high-risk code blocks default use.

#### MC-4 Manual resolution time saved

Definition:

Human time avoided by reducing false conflicts.

Unit:

Minutes per merge.

Baseline:

Manual conflict resolution time measured during replay or estimated from controlled tasks.

Graduation threshold:

Median at least 5 minutes saved per conflicting worktree merge, or at least 30% reduction in resolution time.

Failure threshold:

If setup/debug time exceeds resolution time saved over the eval period, do not graduate.

### 4.5 Cost and performance metrics

#### CP-1 Prompt input token delta

Definition:

Difference in prompt input tokens sent to review model.

Unit:

Tokens and percent delta.

Baselines:

- Raw git diff prompt.
- Current `sc:auggie-review` Auggie pass.

Graduation threshold:

`sem context` must reduce prompt input tokens at least 30% vs the current Auggie-based baseline at equal or near-equal finding recall.

Failure threshold:

No token reduction vs current Auggie baseline means no review-context graduation.

#### CP-2 Output token delta

Definition:

Difference in generated review output tokens.

Unit:

Tokens and percent delta.

Baseline:

Current review output for same prompt class.

Graduation threshold:

No hard threshold, but output-token increase must be justified by improved actionable findings.

Failure threshold:

Verbose low-precision output that increases total token cost without actionable gain fails.

#### CP-3 Wall-clock latency

Definition:

Elapsed time from invocation to usable output.

Unit:

Seconds.

Baselines:

- Raw `git diff` generation.
- Current Auggie pass.
- Native git merge for merge cases.

Graduation threshold:

- `sem diff`: median added latency under 2 seconds for medium diffs.
- `sem context`: median added latency under 8 seconds for medium PRs.
- `inspect triage`: median added latency under 10 seconds before LLM review.
- `weave preview`: median added latency under 5 seconds for controlled merge cases.

Failure threshold:

P95 latency above 60 seconds in routine workflows blocks interactive skill wiring.

#### CP-4 Setup latency

Definition:

Time to install, configure, and verify the tool in a clean environment.

Unit:

Minutes.

Baseline:

No new toolchain setup.

Graduation threshold:

Clean setup under 15 minutes with documented install route and rollback.

Failure threshold:

Setup requiring unclear Rust/cargo troubleshooting blocks user-facing recommendation.

#### CP-5 Binary and dependency burden

Definition:

Operational burden from new binaries, Rust/cargo dependency, version drift, and name collisions.

Unit:

Ordinal score 0-5, where 0 is no burden and 5 is unacceptable burden.

Baseline:

Current UV-only Python framework.

Graduation threshold:

Burden score at or below 3 with named owner and mitigation.

Failure threshold:

Unresolved `sem` collision with GNU parallel blocks any global setup recommendation.

#### CP-6 Maintenance touchpoints

Definition:

Number of files, docs, hooks, settings, and commands that must be maintained after incorporation.

Unit:

Count plus qualitative risk.

Baseline:

Current MCP registry and skill flow.

Graduation threshold:

Each tool incorporation must have fewer than 10 maintained touchpoints or an explicit simplification rationale.

Failure threshold:

If integration sprawls across skills without a central adapter, defer.

### 4.6 MCP reliability metrics

#### MCP-1 Startup success rate

Definition:

Percentage of server startup attempts that succeed.

Unit:

Percent across repeated runs.

Baseline:

Auggie MCP startup behavior.

Graduation threshold:

At least 95% startup success in local eval.

Failure threshold:

Any flaky server startup requires CLI-only mode until fixed.

#### MCP-2 Schema stability

Definition:

Whether tool names, schemas, and required arguments remain stable across version checks.

Unit:

Pass/fail plus diff count.

Baseline:

Documented server schemas.

Special note:

`weave` MCP tool names are undocumented and must be enumerated during spike.

Graduation threshold:

All tool names and schemas documented in the decision record before skill wiring.

Failure threshold:

Undocumented or unstable schemas block MCP integration.

#### MCP-3 Error clarity

Definition:

Whether failures produce actionable messages.

Unit:

Ordinal score 1-5.

Baseline:

Current CLI/MCP error clarity.

Graduation threshold:

Average score at least 4 for missing binary, unsupported file, large file fallback, and malformed input.

Failure threshold:

Opaque errors in common failure modes block user-facing usage.

## 5. Tool-Specific Graduation Gates

### 5.1 sem gates

`sem` is the foundation and must clear the highest bar.

#### sem spike gate

Pass only if:

- Install route is reproducible.
- Binary collision with GNU parallel is resolved or avoided.
- `sem diff`, `sem entities`, `sem impact`, and `sem context` can run on this repo.
- Unsupported file behavior is documented.
- Target-entity omission under token budget is reproduced and bounded.

Fail if:

- The binary collision remains ambiguous.
- Core commands fail on normal IronClaude files.
- Setup requires global state that cannot be rolled back.

#### sem shadow-eval gate

Pass only if:

- `sem diff` reaches at least 90% changed-entity recall on supported native files.
- `sem context` reduces prompt input tokens at least 30% vs current Auggie baseline.
- Finding recall stays within 5 percentage points of baseline or improves.
- Median context latency is under 8 seconds on medium PR cases.
- Impact output has at least 50% useful precision on high-value dependents.

Fail if:

- Token savings exist only vs raw git diff but not vs current Auggie pass.
- `sem context` frequently omits the changed entity in realistic budgets.
- Entity boundaries are too broad to save tokens.

#### sem incorporation gate

Graduate only to guarded skill wiring:

- Add as optional context source for `code-review` and `simplify`.
- Add as advisory structural signal for roadmap/cleanup-audit diffs.
- Do not replace Auggie retrieval until re-eval shows equal or better recall.

### 5.2 inspect gates

`inspect` must overcome its known precision and benchmark weaknesses.

#### inspect spike gate

Pass only if:

- Danger formula is reproduced exactly.
- Tier thresholds are verified: Critical >= 0.7, High >= 0.5, Medium >= 0.3, Low < 0.3.
- Top-60 entity routing behavior is verified.
- Provider routing and token attribution are measurable.
- MCP and CLI surfaces can run without forcing replacement of current review flow.

Fail if:

- Score calculation cannot be reproduced.
- Top-60 truncation cannot be detected in outputs.
- Review provider costs cannot be separated from framework model costs.

#### inspect shadow-eval gate

Pass only if:

- Actionable precision improves above 45% on native corpus in advisory mode.
- Risk ranking beats LOC heuristic by at least 20% NDCG@20.
- All critical human-labeled risky entities appear in top 60 for large PR cases.
- False-positive burden stays within budget.
- It improves review token efficiency when used as pre-filter without losing critical recall.

Fail if:

- Precision remains near or below 33.3% on native corpus.
- Critical changed entities fall outside top 60.
- Keyword-like findings dominate actionable review output.

#### inspect incorporation gate

Graduate only as:

- Pre-filter for risky entities.
- Advisory second reviewer.
- Risk map attached to `sc:auggie-review` output.

Do not graduate as:

- Replacement for Auggie review.
- Sole gate for PR safety.
- Sole determinant of review scope on large PRs.

### 5.3 weave gates

`weave` is evaluated last and locally first.

#### weave spike gate

Pass only if:

- CLI install route is reproducible.
- `weave preview` works on controlled merges.
- `weave setup` and `weave unsetup` rollback are verified in a disposable repo.
- MCP tool names are discovered and documented.
- Unsupported file fallback behavior is observed.

Fail if:

- MCP tool names remain unknowable.
- Setup affects global git behavior without safe scoping.
- Rollback is unreliable.

#### weave shadow-eval gate

Pass only if:

- False conflict reduction is at least 60% on IronClaude-relevant worktree cases.
- True conflict preservation is 100% on curated true-conflict cases.
- Clean merge correctness is at least 95%.
- Median resolution time saved is at least 5 minutes per conflicting merge or at least 30%.
- Local-scoped setup works before any global setup is considered.

Fail if:

- Any true semantic conflict is silently merged.
- False conflict reduction is materially below native workflow benefit.
- Setup/rollback burden exceeds conflict-resolution savings.

#### weave incorporation gate

Graduate only as:

- `weave preview` recommendation inside `sc:git` for conflicting worktree merges.
- Optional local merge driver for selected worktrees.

Do not graduate as:

- Global merge driver default.
- Automatic conflict resolver without human inspection.

## 6. Vendor-Claim Verification Plan

### 6.1 sem hypotheses

Known claim state:

`sem` publishes language support and capabilities, but no public speed or token-reduction numbers.

Hypotheses to test:

- H-sem-1: Entity diff identifies changed review units more accurately than line diff.
- H-sem-2: Token-budgeted context reduces prompt tokens at least 30% vs current Auggie baseline.
- H-sem-3: Impact graph output improves affected-test or review-context selection.
- H-sem-4: 27-language support does not imply equal quality on IronClaude's actual file mix.
- H-sem-5: Chunk fallback for unrecognized files is safe and not misleading.

Independent verification:

- Measure token deltas with the same tokenizer/model configuration used by the review workflow.
- Label changed entities manually for a stratified sample.
- Compare impact output to imports, tests, and human-labeled dependents.
- Record unsupported and fallback cases separately.

Refutation examples:

- Token savings occur only against raw diff, not against Auggie.
- Context omits the target entity in common budget settings.
- Entity boundaries swallow whole files and do not reduce review scope.
- Impact output has low precision and pollutes prompts.

### 6.2 inspect hypotheses

Known claim state:

`inspect` reports high recall on a benchmark, but precision is 33.3% and the judge is keyword-matching.

Known formula:

`danger = classification_weight + blast_ratio*0.3 + ln(1+dependents)*0.1 + public_api_boost 0.15 + change_type_weight`.

Cosmetic changes receive multiplier `*0.3`.

Tiers:

- Critical >= 0.7.
- High >= 0.5.
- Medium >= 0.3.
- Low < 0.3.

Hypotheses to test:

- H-inspect-1: The danger formula ranks IronClaude risky entities better than LOC/file heuristics.
- H-inspect-2: Low upstream precision improves on this repo when used as triage rather than final reviewer.
- H-inspect-3: Top-60 entity routing does not miss critical entities in large IronClaude PRs.
- H-inspect-4: Cosmetic multiplier prevents noise from format-only diffs.
- H-inspect-5: Inspect review output adds unique actionable findings beyond Auggie.

Independent verification:

- Recompute danger scores from raw fields where possible.
- Blind-label top-N entities by actual review risk.
- Compare to LOC ranking, changed-file count, and Auggie-discovered issue locations.
- Deduplicate findings before scoring precision.
- Use human or blind adjudicator, not keyword matching.

Refutation examples:

- Ranking mostly mirrors LOC and does not add predictive value.
- Critical entities fall outside top 60 in large diffs.
- False positives exceed human attention budget.
- Findings are generic and not actionable.

### 6.3 weave hypotheses

Known claim state:

`weave` claims about 95% conflict reduction and 100% clean on 31 scenarios vs git 48%.

Hypotheses to test:

- H-weave-1: Worktree branches in IronClaude create false conflicts similar to weave's target class.
- H-weave-2: Semantic merge reduces false conflicts by at least 60% in native/curated cases.
- H-weave-3: True conflicts are never silently auto-merged.
- H-weave-4: Clean merges pass tests and human semantic inspection.
- H-weave-5: Local setup is safe enough for optional `sc:git` recommendations.

Independent verification:

- Replay native merge cases where possible.
- Construct controlled same-file independent-function conflicts.
- Construct controlled same-function true conflicts.
- Run tests after clean merges when applicable.
- Inspect merged output manually for curated cases.

Refutation examples:

- Native IronClaude conflicts are mostly not false conflicts.
- Weave reduces conflict markers but produces semantically wrong merges.
- Setup is too global or hard to reverse.
- MCP surface is not stable enough to integrate.

## 7. Data-Source Plan

### 7.1 Native corpus first

The harness should mine this repository before external repos.

Candidate sources:

- Recent merged PRs in the fork.
- Recent feature branches.
- Current backlog release diffs.
- Roadmap scanner changes.
- Cleanup-audit changes.
- Skill and command edits under `src/superclaude/`.
- Worktree branches if available.

### 7.2 Historical PR selection

Select PRs with stratification:

- Small PRs: 1-3 files changed.
- Medium PRs: 4-15 files changed.
- Large PRs: more than 15 files changed or many entities.
- Python-heavy PRs.
- Markdown/skill-heavy PRs.
- Mixed code/docs PRs.
- Refactor-like PRs.
- Bug-fix PRs.
- Formatting/noise-heavy PRs.

Minimum target:

- 20 PR/review cases if available.
- If fewer exist locally, use all available native cases and mark confidence lower.

### 7.3 Native merge selection

Select merge cases with stratification:

- Independent same-file edits.
- Same-function edits.
- Same markdown section edits.
- Generated artifact or sync-dev adjacent edits.
- Branches touching skill source and dev-copy outputs.
- Worktree branches that should merge cleanly.
- Worktree branches that should conflict.

Minimum target:

- 10 merge cases if available.
- At least 5 false-conflict candidates.
- At least 5 true-conflict candidates.

### 7.4 Curated defect corpus

Create curated diffs with known expected findings.

Defect classes:

- Wrong branch/remote PR target.
- `.claude/` source-of-truth violation.
- UV-only violation.
- Missing sync-dev after source edit.
- Incorrect danger threshold handling.
- Token budget omission.
- Broken rollback command.
- Large-file fallback mishandling.
- Silent merge semantic conflict.
- False-positive cosmetic risk.

Each curated case stores:

- Input diff.
- Expected findings.
- Severity.
- Evidence location.
- Whether baseline catches it.
- Whether tool-assisted workflow catches it.

### 7.5 Synthetic corpus

Synthetic cases are allowed only as labeled supplements.

They must not be mixed with native results without a separate breakdown.

Synthetic cases should target known edge cases:

- Same-file independent function edits.
- Same-function incompatible edits.
- Function rename plus call-site update.
- Public API change with dependents.
- Cosmetic-only change.
- Large entity exceeding token budget.
- Unsupported file type.
- Binary file.
- File larger than weave fallback threshold.
- Multi-language sample across sem-supported languages.

### 7.6 Generalization corpus

Generalization comes after native success.

Use small external repositories only after the framework-native gate passes.

Purpose:

- Validate 27-language claim breadth for `sem`.
- Stress `weave` across language families.
- Compare `inspect` beyond IronClaude patterns.

Do not use generalization success to override native failure.

If a tool helps other repos but not IronClaude, it does not graduate for IronClaude workflows.

## 8. Ground Truth and Judging Plan

### 8.1 Ground truth levels

The harness uses three levels of ground truth:

1. Strong ground truth.
2. Medium ground truth.
3. Weak ground truth.

Strong ground truth:

- Curated defects with known expected findings.
- Controlled merge cases with known correct output.
- Human-labeled changed entities.

Medium ground truth:

- Historical PR findings accepted by maintainers.
- Test failures after merge or review.
- Existing tasklists that documented defects.

Weak ground truth:

- LLM adjudication only.
- Tool self-reported labels.
- Keyword matching.

Graduation cannot rely on weak ground truth alone.

### 8.2 Blind adjudication

For review findings:

- Hide the tool source from the judge.
- Deduplicate findings across tools.
- Ask whether each finding is actionable, correct, severe, and novel.
- Require evidence citation from the diff or context.

For risk ranking:

- Label entities independently before viewing inspect score where possible.
- Compare rankings afterward.

For merge correctness:

- Human-inspect merged output for curated true-conflict and false-conflict cases.
- Run available tests when code compiles and test selection is known.

### 8.3 No trust in keyword matching

Keyword matching is allowed only as a rough triage helper.

It is not used for final precision or recall.

The `inspect bench` judge is therefore not accepted as a validation method.

### 8.4 Deduplication policy

Findings are deduplicated before precision/recall scoring.

Two findings are duplicates if they identify the same defect, same affected entity, and same remediation.

A generic warning and a specific bug are not duplicates.

The specific bug receives higher adjudication value.

### 8.5 Severity labels

Use four severities:

- Critical: would cause wrong behavior, security exposure, data loss, or severe workflow break.
- High: likely user-visible failure or serious quality regression.
- Medium: maintainability, correctness, or UX issue worth fixing.
- Low: minor cleanup, style, or optional improvement.

Review-quality thresholds weight Critical and High more heavily.

A tool cannot compensate for missed Critical findings with many Low findings.

## 9. Harness Architecture

### 9.1 Preferred implementation stance

Start as a framework-native `.dev/` eval harness, not a full `superclaude eval` product.

Reason:

The first release needs evidence, not a reusable evaluation platform.

If the harness proves valuable and repeatable, promote it later into a CLI subcommand.

### 9.2 Harness components

The harness needs these components:

- Corpus manifest.
- Baseline runners.
- Tool runners.
- Token measurement.
- Latency measurement.
- Output normalizer.
- Finding deduplicator.
- Human/adjudicator scoring sheet.
- Scorecard generator.
- Decision-record template.

### 9.3 Corpus manifest fields

Each scenario case should record:

- Case ID.
- Scenario type.
- Source kind: native, curated, synthetic, generalization.
- Repository path.
- Base ref.
- Head ref.
- Merge base if applicable.
- Changed files.
- Language mix.
- Expected entities if labeled.
- Expected findings if curated.
- Expected merge outcome if merge case.
- Baselines to run.
- Tools to run.
- Notes and known caveats.

### 9.4 Runner outputs

Each runner should emit normalized JSON.

Common fields:

- Tool name.
- Tool version.
- Command or MCP call.
- Start timestamp.
- End timestamp.
- Exit code.
- Stdout/stderr paths or captured payload.
- Parsed entities.
- Parsed findings.
- Token counts.
- Latency seconds.
- Error classification.

### 9.5 Token accounting

Token accounting must include:

- Context-generation prompt input tokens.
- Review prompt input tokens.
- Review output tokens.
- Inspect provider tokens if `inspect review` calls an LLM.
- Any second-pass adjudication tokens reported separately.

Do not count adjudication tokens as tool runtime cost.

Do count them as eval-harness cost.

### 9.6 Latency accounting

Measure:

- CLI command time.
- MCP startup time.
- MCP tool call time.
- LLM review time.
- End-to-end workflow time.

Report median, P90, and P95.

### 9.7 Cost attribution

Separate costs:

- User workflow cost.
- Eval-only measurement cost.
- One-time integration cost.
- Ongoing maintenance cost.

A tool can have high eval cost and still low user workflow cost.

A tool cannot hide ongoing maintenance cost behind one-time setup.

## 10. Per-Tool Scorecard Template

### 10.1 Scorecard header

Tool:

Version:

Install route:

Evaluation date:

Evaluator:

Corpus size:

Native cases:

Curated cases:

Synthetic cases:

Generalization cases:

Verdict:

Verdict options:

- kill.
- defer.
- shadow_only.
- graduate.

### 10.2 Value scorecard

| Metric | Unit | Baseline | Observed | Threshold | Pass? | Evidence |
|---|---:|---:|---:|---:|---|---|
| Finding recall | % | | | | | |
| Actionable precision | % | | | | | |
| Critical miss count | count | | | 0 missed baseline-caught criticals | | |
| Entity detection recall | % | | | | | |
| Entity boundary precision | % | | | | | |
| Impact precision | % | | | | | |
| Impact recall | % | | | | | |
| False conflict reduction | % | | | | | |
| True conflict preservation | % | | | 100% | | |
| Clean merge correctness | % | | | | | |
| Review novelty | count | | | | | |

### 10.3 Cost scorecard

| Metric | Unit | Baseline | Observed | Threshold | Pass? | Evidence |
|---|---:|---:|---:|---:|---|---|
| Prompt input token delta | tokens/% | | | | | |
| Output token delta | tokens/% | | | | | |
| Total model token delta | tokens/% | | | | | |
| Median latency | seconds | | | | | |
| P95 latency | seconds | | | | | |
| Setup time | minutes | | | | | |
| Maintenance touchpoints | count | | | | | |
| Dependency burden | 0-5 | | | <=3 | | |
| MCP startup success | % | | | >=95% | | |
| Rollback success | pass/fail | | | pass | | |

### 10.4 Risk scorecard

| Risk | Severity | Likelihood | Mitigation | Residual risk | Blocks graduation? |
|---|---|---|---|---|---|
| Rust/cargo new dependency | | | | | |
| `sem` binary collision | | | | | |
| Inspect low precision | | | | | |
| Inspect top-60 recall ceiling | | | | | |
| Inspect provider token attribution | | | | | |
| Weave silent bad merge | | | | | |
| Weave global setup blast radius | | | | | |
| Undocumented weave MCP tools | | | | | |
| Unsupported language fallback | | | | | |
| Skill integration sprawl | | | | | |

### 10.5 Decision summary template

Decision:

Rationale:

Top evidence for:

Top evidence against:

Thresholds passed:

Thresholds failed:

Allowed integration surface:

Disallowed integration surface:

Rollback steps:

Next re-eval trigger:

Owner:

## 11. Statistical Validity Notes

### 11.1 Sample size reality

This repo may not have enough historical cases for high-powered statistical claims.

The harness must be honest about that.

If there are only 8 relevant historical PRs, do not claim broad proof.

Instead:

- Report native results as directional.
- Supplement with curated cases.
- Supplement with synthetic cases.
- Mark confidence level explicitly.

### 11.2 Minimum useful samples

Recommended minimums:

- PR review: 20 cases.
- Entity diff: 30 changed-file or changed-entity cases.
- Context extraction: 15 review cases across size bands.
- Impact analysis: 10 changes with known dependents.
- Merge: 10 cases, split between false and true conflicts.
- MCP stability: 20 startup/call attempts per server.

### 11.3 Stratification requirements

Do not average across unlike cases without stratification.

Report separately by:

- PR size.
- File type.
- Language.
- Code vs docs.
- Supported vs fallback parser behavior.
- Native vs curated vs synthetic.
- Small vs large entity.
- Conflict type for merge.

### 11.4 Repeated-run stability

Run each candidate workflow at least 3 times on a subset.

Measure:

- Output stability.
- Latency variance.
- MCP startup variance.
- LLM review nondeterminism if applicable.

If outputs vary materially, use median and record instability.

### 11.5 Confidence labels

Assign confidence labels to verdicts:

- High: native sample meets minimums and curated edge cases pass.
- Medium: native sample is small but curated/synthetic cases are strong.
- Low: mostly synthetic or incomplete data.

Graduation should require High or strong Medium confidence.

Replacement of existing workflows requires High confidence.

### 11.6 Avoiding Simpson's paradox

A tool may look good overall while failing the most important stratum.

Examples:

- `sem` saves tokens on small diffs but omits target entities on large diffs.
- `inspect` ranks well on small PRs but misses top-60 criticals on large PRs.
- `weave` succeeds on synthetic same-file independent edits but fails markdown/skill cases.

Therefore the final scorecard must show stratum-level pass/fail.

### 11.7 Effect-size framing

Use effect sizes, not just pass/fail.

Report:

- Absolute percentage-point recall change.
- Percent token reduction.
- Minutes saved.
- False positives added per PR.
- Conflicts avoided per merge.

A small statistically visible improvement may still not justify maintenance burden.

## 12. Incorporation Implications from the Eval Lens

### 12.1 sem incorporation if passed

Allowed:

- Optional entity diff summary in review workflows.
- Optional token-budgeted context source.
- Advisory impact graph for test/review selection.
- Framework-native eval fixture for later tools.

Not allowed initially:

- Replacement of Auggie retrieval.
- Global `sem setup` without binary-collision resolution.
- Mandatory MCP dependency for core workflows.

### 12.2 inspect incorporation if passed

Allowed:

- Advisory risk map in `sc:auggie-review`.
- Pre-filter for entities sent to a reviewer.
- Comparison channel beside Auggie findings.
- Risk explanation attached to findings.

Not allowed initially:

- Sole reviewer.
- Sole gate for PR safety.
- Blind trust in danger score.
- Automatic exclusion of entities outside top 60.

### 12.3 weave incorporation if passed

Allowed:

- `weave preview` in `sc:git` conflict guidance.
- Local worktree merge-driver setup for selected cases.
- Documented rollback via `weave unsetup`.

Not allowed initially:

- Global default merge driver.
- Auto-resolution without human inspection.
- Use on unsupported files without explicit fallback visibility.

## 13. Risk Register

### 13.1 Risk: current baselines are not fully measured

Severity:

High.

Why it matters:

Without current Auggie and git baselines, we cannot prove improvement.

Mitigation:

Start by measuring baselines before running vendor tools.

Graduation impact:

Blocks all graduation.

### 13.2 Risk: native corpus too small

Severity:

Medium.

Why it matters:

Small samples can produce misleading conclusions.

Mitigation:

Use all available native cases, then add curated and synthetic cases with separate reporting.

Graduation impact:

Limits verdict to `shadow_only` or Medium confidence unless supplemented strongly.

### 13.3 Risk: sem binary collision

Severity:

High.

Why it matters:

A command named `sem` may collide with GNU parallel's `sem`.

Mitigation:

Use explicit binary path or alias strategy; never recommend global setup until resolved.

Graduation impact:

Blocks `sem` global integration.

### 13.4 Risk: Rust/cargo maintenance burden

Severity:

High.

Why it matters:

The project is UV-only Python today.

Mitigation:

Score dependency burden, document install routes, prefer prebuilt binaries if reliable, assign owner.

Graduation impact:

Can block all tools if cost outweighs value.

### 13.5 Risk: inspect false positives normalize noise

Severity:

High.

Why it matters:

Low precision can make reviewers ignore warnings.

Mitigation:

Strict false-positive budget and advisory-only initial mode.

Graduation impact:

Blocks replacement mode.

### 13.6 Risk: inspect top-60 ceiling misses large-PR criticals

Severity:

High.

Why it matters:

Large PRs are where triage matters most.

Mitigation:

Measure recall@60 explicitly and require all critical entities in top 60.

Graduation impact:

Blocks pre-filter mode for large PRs.

### 13.7 Risk: weave silently produces wrong clean merge

Severity:

Critical.

Why it matters:

A silent bad merge is worse than a conflict.

Mitigation:

True-conflict preservation gate must be 100% on curated cases.

Graduation impact:

Any occurrence blocks adoption beyond preview.

### 13.8 Risk: weave setup blast radius

Severity:

High.

Why it matters:

Global merge driver behavior can affect unrelated repos or branches.

Mitigation:

Evaluate local setup first; document unsetup; avoid global default.

Graduation impact:

Blocks global setup recommendation.

### 13.9 Risk: MCP surface instability

Severity:

Medium.

Why it matters:

Hybrid integration requires reliable schemas.

Mitigation:

CLI-first fallback; enumerate schemas during spike; require startup success metrics.

Graduation impact:

May allow CLI integration while blocking MCP registration.

### 13.10 Risk: eval harness becomes too big

Severity:

Medium.

Why it matters:

A full eval platform could delay learning.

Mitigation:

Start in `.dev/` with small normalized runners and scorecards.

Graduation impact:

Does not block tool eval, but blocks promotion to `superclaude eval`.

## 14. Open Questions

### 14.1 Baseline selection

Should token reduction be judged primarily against raw git diff or current Auggie pass?

Analyzer answer:

Use both, but graduation requires beating current Auggie pass.

Raw git diff is an informative lower baseline, not the real status quo.

### 14.2 Corpus size

How many historical PRs and branch merges are recoverable from this fork?

Required action:

Inventory PRs, branches, and reflog/worktree history before finalizing statistical confidence.

### 14.3 Human adjudication budget

Who labels findings and changed entities?

Required action:

Define a small adjudication panel or single owner plus blind LLM assistant, with human final say for critical cases.

### 14.4 Tokenizer and model routing

Which tokenizer and model costs should be used?

Required action:

Use the actual model/provider path invoked by the workflow, including multi-vendor routing where inspect calls an LLM.

### 14.5 Inspect provider routing

Does `inspect review` call Anthropic/OpenAI/Ollama directly or through framework routing?

Required action:

Measure provider-specific token and latency costs separately.

### 14.6 Weave MCP tool names

What are the MCP tool names for weave?

Required action:

Spike must enumerate tools before any MCP registry entry is considered complete.

### 14.7 Generalization threshold

When do we add external repos?

Analyzer answer:

Only after native eval passes enough to justify broader validation.

External success cannot rescue native failure.

### 14.8 Promotion to CLI

Should this become `superclaude eval`?

Analyzer answer:

Not initially.

Promote only after the `.dev/` harness runs at least one full tool decision cycle successfully.

## 15. Proposed Evaluation Timeline

### 15.1 Phase A: Baseline inventory

Duration:

1-2 days.

Outputs:

- Corpus manifest draft.
- Baseline measurements for raw git diff, current Auggie review, and native git merge.
- Initial sample-size confidence statement.

Exit criteria:

At least enough cases to run `sem` shadow eval or a documented reason synthetic backfill is needed.

### 15.2 Phase B: sem spike and shadow eval

Duration:

2-4 days.

Outputs:

- Install and collision decision.
- Entity diff measurements.
- Context token measurements.
- Impact precision/recall measurements.
- sem scorecard and decision record.

Exit criteria:

`sem` verdict.

If `sem` is killed, stop the chain.

### 15.3 Phase C: sem guarded wiring and re-eval

Duration:

1-3 days if sem passes.

Outputs:

- Optional skill wiring proposal.
- Re-eval against same corpus.
- Regression comparison.

Exit criteria:

Wired mode still meets thresholds.

### 15.4 Phase D: inspect spike and shadow eval

Duration:

2-4 days.

Outputs:

- Formula reproduction.
- Precision/recall scorecard.
- Risk-ranking evaluation.
- Top-60 ceiling analysis.
- Provider cost accounting.

Exit criteria:

`inspect` verdict.

### 15.5 Phase E: inspect guarded wiring and re-eval

Duration:

1-3 days if inspect passes.

Outputs:

- Advisory risk map integration proposal.
- Re-eval against PR review corpus.
- False-positive budget check.

Exit criteria:

Advisory or pre-filter mode still meets thresholds.

### 15.6 Phase F: weave spike and shadow eval

Duration:

2-5 days.

Outputs:

- CLI/MCP surface discovery.
- Local setup/rollback proof.
- Merge scenario results.
- True-conflict preservation report.
- weave scorecard and decision record.

Exit criteria:

`weave` verdict.

### 15.7 Phase G: weave guarded wiring and re-eval

Duration:

1-3 days if weave passes.

Outputs:

- `sc:git` preview recommendation proposal.
- Local worktree-only usage guidance.
- Re-eval on merge corpus.

Exit criteria:

Preview/local mode still meets thresholds.

## 16. Final Recommendation from the Analyzer Lens

The release plan should be built around the eval harness, not around integration tasks.

The first deliverable is not an MCP registry patch.

The first deliverable is a baseline report showing current review, context, and merge costs.

Only after that should `sem` be tested.

Only after `sem` passes should `inspect` be tested.

Only after `inspect` passes should `weave` be tested.

The most important adoption guardrails are:

- `sem` must beat current Auggie token/context behavior, not just raw git diff.
- `inspect` must prove useful despite low precision, weak benchmark judging, and top-60 truncation.
- `weave` must preserve every true conflict before its conflict-reduction claim matters.

If the harness cannot prove these claims on IronClaude data, the correct outcome is not partial enthusiasm.

The correct outcome is a documented no-go, a rollback path, and a preserved eval corpus for future re-testing.
