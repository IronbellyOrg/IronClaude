# Reviewer Card 1 — Coverage Lens

## Coverage Table

| Requirement | Covered? | Section / UNMAPPED | Severity |
|---|---:|---|---|
| Original ask: create an evaluation release plan | COVERED | merged §3 state machine; §14 phased timeline | LOW |
| Original ask: incorporate `sem`, `inspect`, `weave` | COVERED | merged §8.1–§8.3 per-tool plans; §9 integration map | LOW |
| Original ask: incorporate tools one at a time | PARTIAL | merged §3 says inspect blocked until sem S4+KEEP and weave blocked until inspect S4+KEEP; §14 repeats. But merged §8.2 says “inspect KILL does not block weave,” contradicting hard sequential gating. | HIGH |
| Original ask: detailed set of evals | PARTIAL | merged §4 scenario matrix, §5 metrics, §7 judging, §11 corpus. Missing executable per-scenario procedure, runner contract, fixtures, artifact schemas, and adjudication workflow details. | MED |
| Original ask: determine real-world value | COVERED | merged §5 review/structural/merge quality metrics; §8 per-tool hypotheses and KEEP gates | LOW |
| Original ask: determine real-world cost | COVERED | merged §6 all-in TCO; §5 cost/performance; §10 CP-2 | LOW |
| Original ask: value AND cost with go/no-go thresholds | COVERED | merged §5 metric catalog; §8.1 S2, §8.2 S2, §8.3 S2 gates | LOW |
| Original ask: broad variety of scenarios | PARTIAL | merged §4 scenario matrix and §11 native/curated/synthetic/generalization tiers. External multi-repo/multi-language breadth is deferred and not specified as an appendix. | HIGH |
| Constraint: one tool at a time, hard-gated; sem before inspect before weave | PARTIAL | merged §3/§14 enforce order, but §8.2 explicitly allows inspect KILL not to block weave. | HIGH |
| Constraint: framework-native scenarios first | COVERED | merged §11 native tier first; frontmatter `eval_scope`; §14 generalization optional after native path | LOW |
| Constraint: all-in cost accounting tokens, latency, integration/maintenance, collision | COVERED | merged §6 C1–C5; §5 CP metrics; §6 collision neutralization | LOW |
| Constraint: falsifiable, baseline-anchored evals | COVERED | merged §5 requires baselines; §7 ground-truth tiers; §13 token baseline resolution | LOW |
| Constraint: independent verification of vendor claims | COVERED | merged §1 rejects vendor benchmarks; §7 rejects weak/tool self-labels; §8 tests vendor hypotheses | LOW |
| Constraint: reversibility | COVERED | merged §3 rollback per state; §10 kill switch; §8 rollback requirements | LOW |
| Constraint: no production gating on day one | COVERED | merged §3 S1 zero production effect; §8.2 advisory-only; §8.3 preview-only | LOW |
| Success: release plan with Spike → Shadow eval → Gated decision → Skill integration → Re-eval and kill/keep between tools | PARTIAL | merged §3 provides state machine and gate; §3/§14 order contradicted by §8.2 inspect KILL exception. | HIGH |
| Success: detailed eval harness spec with scenario matrix | PARTIAL | merged §4 matrix is broad at row level, but lacks executable procedure per scenario and fixture definitions. | MED |
| Success: metrics with units and baselines | COVERED | merged §5 units/baselines; §6 cost units | LOW |
| Success: data sources with repo PRs/branches | PARTIAL | merged §11 names source tiers and §7 sample minimums, but no concrete PR/branch selection list or manifest schema beyond Phase 0 deliverable. | MED |
| Success: pass/fail thresholds | COVERED | merged §5 thresholds; §8 per-tool KEEP/KILL thresholds | LOW |
| Success: per-tool value/cost scorecards with explicit go/no-go thresholds | PARTIAL | thresholds exist in §8, but the scorecard template itself is only named in §4 harness components, not specified. | MED |
| Success: decision-record template with keep/kill verdict and evidence citations | PARTIAL | merged §4 lists “decision-record template” as harness component; §3 mentions `decisions/<tool>-KILL.md`; no actual template fields or citation requirements. | MED |
| Success: broad-scenario generalization appendix gated behind native-eval success | PARTIAL | merged §11 and §14 mention generalization as gated/optional; no appendix structure, scenario inventory, languages, repos, or thresholds. | HIGH |
| Success: Rust-toolchain-maintenance ownership | UNMAPPED | merged §6/§10 quantify maintenance burden, but no owner, role, cadence owner, escalation owner, or RACI. | HIGH |
| Success: stance on `sem` ↔ GNU-parallel collision | COVERED | merged §6 4-step neutralization; §2 Phase 0 deliverable; §12 risk register | LOW |
| Open question: `superclaude eval` CLI vs `.dev/` scripts | COVERED | merged §4 and §13 resolve `.dev/` scripts first | LOW |
| Open question: inspect false-positive budget / pre-filter vs replacement | COVERED | merged §8.2 and §13 resolve advisory/pre-filter only, with precision/FP budgets | LOW |
| Open question: weave global vs per-worktree setup | COVERED | merged §8.3, §9, §13 resolve per-worktree local; never global | LOW |
| Open question: inspect provider routing and token attribution | COVERED | merged §6 provider-weighted economics; §8.2 fixed provider in shadow; §13 routing resolution | LOW |
| Open question: token-cost baseline raw diff vs Auggie | COVERED | merged §5 and §13 require both measured, graduation beats Auggie | LOW |
| Open question: sample size / statistically meaningful native eval set | COVERED | merged §2 G0-1; §7 evidence minimums; §13 sample resolution | LOW |

## Ranked Gap List

1. **Sequential gating contradiction: inspect KILL may not block weave** — HIGH
   - Evidence: seed constraint requires “sem must clear before inspect; inspect before weave” and “One tool at a time, hard-gated” in seed §Constraints. merged §3/§14 state weave is blocked until inspect S4 live+KEEP, but merged §8.2 says “inspect KILL does not block weave.”
   - Why it matters before execution: the plan is internally inconsistent on the central sequencing invariant. An executor could legitimately skip the inspect keep/kill barrier and start weave, violating the original ask.

2. **Generalization appendix is named, not specified** — HIGH
   - Evidence: seed §Success Criteria requires a “broad-scenario generalization appendix (multi-repo / multi-language) gated behind native-eval success.” merged §11 says generalization is external repos/multi-language gated behind native success, and §14 makes it optional, but no appendix structure, candidate repos/languages, thresholds, or entry/exit criteria are defined.
   - Why it matters before execution: “broad variety” risks collapsing into native-only evaluation indefinitely, with external breadth deferred without a concrete deliverable.

3. **Rust-toolchain maintenance ownership is missing** — HIGH
   - Evidence: seed §Success Criteria requires “Clear ownership of the new Rust toolchain maintenance cost.” merged §6 quantifies maintenance and §10 freezes admissions if budget crosses threshold, but no owner is assigned.
   - Why it matters before execution: cost without ownership is not operational. Cargo updates, MCP binary drift, CI failures, and collision guard upkeep can become nobody’s responsibility.

4. **Eval harness is not executable enough** — MED
   - Evidence: seed §Success Criteria calls for a detailed eval harness spec with scenario matrix, metrics, data sources, and thresholds. merged §4 lists components and §5/§7 define metrics/judging, but there are no per-scenario run steps, fixture manifests, runner CLI contracts, output schemas, adjudicator instructions, or data-selection procedure.
   - Why it matters before execution: teams may implement incompatible one-off scripts and produce non-comparable results, undermining falsifiability.

5. **Decision-record and scorecard templates are underspecified** — MED
   - Evidence: seed §Success Criteria requires per-tool scorecards and a decision-record template with evidence citations. merged §4 names a scorecard generator and decision-record template; §8 embeds gate thresholds; §3 mentions `decisions/<tool>-KILL.md`, but no template fields are defined.
   - Why it matters before execution: keep/kill decisions can become narrative-only and omit evidence citations, cost rollups, rollback proof, or confidence labels.

## Coverage Estimate

- Total mapped requirements counted: 31
- Covered: 19
- Partial: 10
- Unmapped: 1
- Coverage estimate: 19 + 0.5×10 = 24 / 31 ≈ **77%**
