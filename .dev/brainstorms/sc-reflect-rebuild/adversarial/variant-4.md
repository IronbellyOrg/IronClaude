---
name: sc:reflect-protocol
description: "Tiered reflection protocol for /sc:reflect — pre-execution plan validation and post-execution completion review with Serena-grounded evidence, calibrated tier escalation, adversarial merge delegation, and eval-harness acceptance gates."
version: 2.0.0
mcp-servers: [auggie, serena, context7, tavily, sequential]
complexity: advanced
allowed-tools: Read, Grep, Glob, Bash, TodoWrite, Task, Write, Edit, Skill, mcp__auggie__codebase-retrieval, mcp__serena__activate_project, mcp__serena__get_current_config, mcp__serena__get_symbols_overview, mcp__serena__find_symbol, mcp__serena__find_referencing_symbols, mcp__serena__get_diagnostics_for_file, mcp__serena__list_memories, mcp__serena__read_memory, mcp__serena__write_memory, mcp__serena__think_about_collected_information, mcp__serena__think_about_task_adherence, mcp__serena__think_about_whether_you_are_done, mcp__context7__resolve-library-id, mcp__context7__query-docs, mcp__tavily__tavily-search, mcp__sequential-thinking__sequentialthinking
argument-hint: "--mode pre|post|auto --source <tasklist-or-spec> [--work <diff|commit|dir>] [--depth quick|standard|deep] [--fix] [--output dir]"
spec: .dev/eval-workspaces/sc-reflect/SPEC.md
---
<!-- markdownlint-disable MD013 MD040 -->
# /sc:reflect — Tiered Reflection and Validation Protocol
## Triggers
`sc:reflect-protocol` is invoked by the `/sc:reflect` command. It may also be invoked by other protocol skills as a validation gate after they produce a tasklist, task file, implementation report, or release artifact.
Activation conditions:
- User runs `/sc:reflect` with a spec, tasklist, implementation diff, task log, or completion artifact.
- A parent protocol needs pre-execution validation of a proposed plan before executing tools.
- A parent protocol needs post-execution verification that completed work matches its tasklist/spec.
- A task report contains executable recommendations that must pass recommendation re-scrutiny before delivery.
- A high-stakes change needs an independent model-class review rather than self-review by the executor.
Non-activation conditions:
- User asks for debugging of a broken command, failing test, or runtime error as the primary task. Use `sc:troubleshoot-protocol` first, then reflect on its report if needed.
- User asks for open-ended idea generation. Use `sc:brainstorm-protocol`; reflect only on the produced plan or requirements.
- User asks for adversarial comparison of 2-10 artifacts without a task/spec adherence question. Use `sc:adversarial-protocol` directly.
## 1. Purpose and Identity
`/sc:reflect` answers two questions with evidence:
1. **UC-1 pre-execution validation**: Is the proposed plan aligned to the source spec/tasklist before execution begins?
2. **UC-2 post-execution review**: Did completed work fully satisfy the source tasklist/spec without unauthorized drift?
The protocol is deliberately tiered. Tier 1 is a fast, single-pass, Serena-grounded review. Tier 2 adds independent parallel reviewers, calibrated findings, and `sc-adversarial-protocol` merge when findings conflict. Tier 3 is opt-in remediation through `task-builder`, not automatic editing.
**Hallucination contract:** Every final finding that cites a file, line, command, task item, checklist item, or config value must be re-grounded. Findings without evidence are dropped or explicitly marked `unverified`; they are never silently promoted to verdict facts.
**No duplicate debate implementation:** This skill orchestrates reflection. It does not implement debate, scoring, base selection, or merge logic. When multiple candidate verdicts need comparison, it delegates to `sc-adversarial-protocol` in Mode A.
## 2. Required Input (UC-1 / UC-2 selection)
Required: one source-of-truth artifact and, for post-execution mode, one completed-work artifact.
### UC-1: Pre-execution validation
Minimum input:
- `--mode pre` or auto-detected pre mode.
- `--source <spec|prd|tasklist|roadmap|requirements|issue>`.
- A proposed plan, tasklist, strategy, or intended tool/action sequence.
UC-1 output: coverage matrix, best-practice compliance verdict, missing requirements, risk register, and `pass | revise | block` recommendation.
### UC-2: Post-execution review
Minimum input:
- `--mode post` or auto-detected post mode.
- `--source <tasklist|spec|prd|roadmap|issue>`.
- `--work <git diff|commit range|task log|artifact dir|report>`.
UC-2 output: completion matrix, deviation taxonomy, evidence-validated findings, best-practice grade, and `complete | partial | fail | needs-human-decision` verdict.
### Auto-detection rules
| Signal | Mode |
|--------|------|
| Input includes `git diff`, commit hash/range, completed task log, `status: complete`, or changed files | `post` |
| Input includes only proposed checklist, strategy, planned commands, or task file not yet executed | `pre` |
| Both plan and diff are present | `post`, with plan used as source-of-truth |
| Neither source nor work is present | STOP |
STOP messages:
- Missing source: `Reflect requires --source <spec|tasklist|artifact>. For post mode also provide --work <diff|task-log|artifact-dir>.`
- Ambiguous mode: `Reflect could not infer pre vs post. Re-run with --mode pre or --mode post.`
- Empty source file: `Reflect source is empty or unreadable; cannot validate adherence.`
## 3. Wave/Tier Architecture
```
Wave 0: Parse, validate, source-of-truth guard, output-dir guard
Wave 1: Evidence inventory + Serena project activation
Wave 1.5: Scripted Serena reflection checkpoints
Wave 2: Tier decision rubric + confidence calibration
Wave 3: Tier 1 verdict synthesis (always runs)
Wave 4: Tier 2 parallel review (conditional)
Wave 5: Adversarial merge via sc-adversarial-protocol (conditional)
Wave 6: Final evidence validation + recommendation re-scrutiny
Wave 7: Tier 3 remediation handoff (opt-in only)
Wave 8: Return contract + memory write
```
### Execution vocabulary
| Verb | Tool | Scope |
|------|------|-------|
| Ground | `Read`, `mcp__auggie__codebase-retrieval`, Serena symbols | Source/work evidence |
| Checkpoint | Serena `think_about_*` tools | Scripted reflection gates |
| Dispatch | `Task` | Parallel review/calibration agents |
| Invoke | `Skill` | Cross-skill calls (`sc-adversarial-protocol`, `task-builder`) |
| Validate | `Read`, `Grep`, `Bash`, `evidence-validator` | Citation and command verification |
| Compose | inline | Matrices, verdict, return contract |
| Persist | `mcp__serena__write_memory` | Project-scoped reflection patterns |
## 4. Wave Details
### Wave 0 — Parse + validate inputs
Steps:
1. Parse flags: `--mode`, `--source`, `--work`, `--depth`, `--fix`, `--no-escalate`, `--models`, `--output`, `--blind`, `--no-mcp`, `--no-memory`.
2. Validate output path. Refuse any output under `.claude/skills/`, `.claude/commands/`, `.claude/agents/`, `.claude/hooks/`, or `.claude/templates/`.
3. Normalize output dir to `.dev/reflect/<timestamp>-<slug>/` unless `--output` is supplied.
4. Resolve source and work paths to repo-root-relative path strings for artifacts, but use absolute paths in user-facing final responses.
5. Verify downstream skills exist before promising them: `sc-adversarial-protocol` for Tier 2 merge and `task-builder` for Tier 3 remediation.
6. Create `reflection-brief.md`, `audit.log`, and `return-contract.yaml` stubs in the output dir.
Exit criteria: mode selected, source/work readable, output dir safe, prerequisites known.
### Wave 1 — Evidence inventory + modern Serena grounding
Steps:
1. Activate Serena on the current project. If activation fails, continue in degraded mode and record `serena_available: false`.
2. Run a broad Auggie query: `Find the code, tests, task files, and docs relevant to validating <source> against <work>. Include likely requirement touch-points and changed-file context.`
3. For each touched source file, use Serena in this preference order:
   - `get_symbols_overview` for file-level structural inventory.
   - `find_symbol` for named functions/classes/modules referenced by the tasklist.
   - `find_referencing_symbols` for downstream-impact checks.
   - `get_diagnostics_for_file` for changed code files when available.
4. Load project-scoped memories with `list_memories`, then read only relevant keys such as `reflection/deviation-patterns/<project-slug>` and `reflection/false-positives/<project-slug>`.
5. Build `evidence-inventory.yaml` with: source items, work artifacts, touched files, changed symbols, diagnostics count, memory keys used, and grounding gaps.
Exit criteria: `evidence-inventory.yaml` exists and includes every supplied source/work artifact.
### Wave 1.5 — Scripted Serena reflection checkpoints
The `think_about_*` Serena tools are current meta-cognition checkpoints, not deprecated. They do not replace symbolic evidence gathering; they verify that the evidence loop is not drifting.
Mandatory checkpoints:
1. After evidence inventory: `think_about_collected_information`.
   - If it identifies missing source/work evidence, return to Wave 1 once.
   - If still missing after one retry, continue with `status: partial`.
2. Before Tier decision: `think_about_task_adherence`.
   - If it identifies mode/source mismatch, STOP with a corrective usage message.
   - If it identifies unexamined high-stakes requirements, mark `force_tier2`.
3. Before final return: `think_about_whether_you_are_done`.
   - If it identifies unvalidated claims, rerun Wave 6 evidence validation.
   - If unresolved after validation, downgrade verdict to `partial`.
These checkpoints are scripted gates with observable routing outcomes in `audit.log`; they are not free-form self-nudges.
### Wave 2 — Tier decision rubric + confidence calibration
Compute a numeric `complexity_score` from signals below. Scores are additive and capped at 1.00.
| Signal | Points |
|--------|--------|
| Source has > 10 checklist/spec items | +0.15 |
| Work touches > 5 files or > 300 changed lines | +0.15 |
| Work spans > 2 top-level domains (src/tests/docs/cli/skills) | +0.15 |
| Any security, auth, data-loss, migration, deploy, or destructive command risk | +0.20 |
| UC-2 has unmapped tasklist items after initial coverage pass | +0.20 |
| UC-1 plan contains irreversible commands or unclear preconditions | +0.15 |
| Serena diagnostics include errors in touched files | +0.15 |
| Contradictory evidence ratio > 0.30 | +0.20 |
| Prior reflection memory records similar false-positive/false-negative pattern | +0.10 |
Tier thresholds:
| Condition | Tier |
|-----------|------|
| `--depth quick` or `--no-escalate` and no high-stakes risk | Tier 1 only |
| `complexity_score < 0.35` and calibrated confidence ≥ 0.85 | Tier 1 only |
| `0.35 ≤ complexity_score < 0.65` or calibrated confidence in `[0.70, 0.85)` | Tier 2 |
| `complexity_score ≥ 0.65`, high-stakes risk, contradictory evidence > 0.30, or `--depth deep` | Tier 2 with adversarial merge required |
| User sets `--fix` and final verdict is `revise`, `partial`, or `fail` | Offer Tier 3 remediation |
Calibrated confidence:
- Spawn `confidence-calibrator` against `evidence-inventory.yaml` and `reflection-brief.md`.
- Use a 5-dimension calibration: source clarity, evidence completeness, mapping confidence, risk severity, model-independence need.
- If the agent is unavailable, inline-calibrate and mark `calibration: inline-fallback`.
Exit criteria: `tier_decision.yaml` contains tier, score, calibrated confidence, and escalation reason.
### Wave 3 — Tier 1 verdict synthesis
Tier 1 always runs because Tier 2 needs its coverage matrix as input.
UC-1 Tier 1 outputs:
- `coverage-matrix.yaml`: every source requirement mapped to planned action(s).
- `best-practice-check.md`: framework/library practices checked via Context7 when named.
- `tier1-verdict.md`: `pass | revise | block` with evidence.
UC-2 Tier 1 outputs:
- `completion-matrix.yaml`: every source task item mapped to diff/log/artifact evidence.
- `deviation-ledger.yaml`: each mismatch classified as authorized expansion, necessary deviation, drift, regression, or unknown.
- `tier1-verdict.md`: `complete | partial | fail | needs-human-decision` with evidence.
Recommendation re-scrutiny begins here: every command, shell snippet, or action recommendation in the draft verdict gets a `(verb, object, precondition)` row in `recommendation-scrutiny.yaml`.
### Wave 4 — Tier 2 parallel review (conditional)
Tier 2 runs when Wave 2 escalates. Spawn independent reviewers in parallel; do not give them each other's findings.
Reviewer topology:
| Role | Agent | Purpose |
|------|-------|---------|
| Coverage reviewer | `rf-qa` | Structural source/tasklist vs work mapping |
| Qualitative reviewer | `rf-qa-qualitative` | Product/spec/document coherence |
| Root-cause reviewer | `root-cause-analyst` | Why deviations exist and whether they are justified |
| Code-system reviewer | `quality-engineer` or `auggie-reviewer` | Edge cases, tests, impacted symbols, code-quality risks |
| Calibrator | `confidence-calibrator` | Re-score every reviewer finding independently |
Agent instructions:
- Use explicit `ADVERSARIAL STANCE` for rf-qa / rf-qa-qualitative checks.
- Set `fix_authorization: true` only for correcting evaluation artifacts inside the reflect output dir, never for source code changes.
- Require each finding to include `claim`, `source_item`, `evidence`, `severity`, `deviation_class`, and `if_wrong_reason`.
- Require `evidence` to be a file path, file:line, command output excerpt, or explicit `unverified` marker.
Exit criteria: `tier2-findings/` contains one report per reviewer and one calibration file per report.
### Wave 5 — Adversarial merge via sc-adversarial-protocol (conditional)
Run only when Tier 2 produced conflicting verdicts, high-stakes findings, or `--depth deep`.
Steps:
1. Materialize each reviewer verdict as `candidate-verdicts/verdict-<N>.md`.
2. Invoke `Skill sc-adversarial-protocol` in Mode A:
   ```text
   --compare <candidate-verdicts/verdict-1.md>,<candidate-verdicts/verdict-2.md>[,...]
   --depth standard|deep
   --focus coverage,correctness,deviation-classification,citation-grounding,actionability
   --output <output-dir>/adversarial/
   --blind when requested
   ```
3. Require the standard adversarial artifacts: `diff-analysis.md`, `debate-transcript.md`, `base-selection.md`, `refactor-plan.md`, `merge-log.md`, `merged-output.md`.
4. If the adversarial response is empty, unparseable, or missing `merged-output.md`, fail closed to `status: partial` and use the highest calibrated Tier 2 verdict as fallback with a visible warning.
5. Do not reinterpret or rescore debate results inline. Consume the merged output and move to evidence validation.
Exit criteria: `merged-reflection-verdict.md` exists or fallback is explicitly recorded.
### Wave 6 — Final evidence validation + recommendation re-scrutiny
Steps:
1. Draft `reflection-report.md` from Tier 1 or merged Tier 2 output.
2. Spawn `evidence-validator` with the draft report. It must re-Read every file:line citation and drop mismatches.
3. For command/action recommendations:
   - Check session/source facts first.
   - Use Context7 for library/CLI preconditions when the tool is covered by official docs.
   - Use Tavily or WebSearch fallback only for current external CLI behavior not in Context7.
   - HIGH-stakes unknown preconditions block; LOW/MEDIUM unknowns are surfaced as hedged checks.
4. Apply validator changes to final report.
5. Run `think_about_whether_you_are_done`; if it reports unresolved validation gaps, add them to `Grounding Gaps` and set `status: partial`.
Exit criteria: `reflection-report.md` has verified citations or explicit grounding gaps; `return-contract.yaml` status is updated.
### Wave 7 — Tier 3 remediation handoff (opt-in)
Tier 3 never edits implementation code directly.
Entry conditions:
- User supplied `--fix` or accepts the remediation offer.
- Final report verdict is `revise`, `partial`, `fail`, or `needs-human-decision` with actionable remediation.
- Evidence validation completed; no HIGH-stakes unverified recommendation remains.
Steps:
1. Ask one yes/no remediation question unless `--fix --yes` is explicitly supported by the parent command.
2. Invoke `Skill task-builder` with a build request that cites `reflection-report.md`, `completion-matrix.yaml`, and `deviation-ledger.yaml`.
3. Run UC-1 reflect on the newly generated task file before presenting it as executable.
4. Return task path and a user-run command suggestion. Do not auto-run `/task`.
Exit criteria: task file path recorded or user declined remediation.
### Wave 8 — Return contract + memory write
Steps:
1. Write final `return-contract.yaml`.
2. Persist compact memory unless `--no-memory`:
   - `reflection/last-pass/<project-slug>`
   - `reflection/deviation-patterns/<project-slug>`
   - `reflection/false-positives/<project-slug>` when a finding was downgraded.
3. Keep only the last 20 memory entries per key family and summarize older entries.
## 5. Modern Serena Tool Usage
Serena is used for symbolic grounding and scripted reflection checkpoints.
| Need | Preferred Serena tool | Fallback |
|------|-----------------------|----------|
| Activate correct repo | `activate_project` | Continue degraded, note in audit |
| Know available state | `get_current_config` | Skip |
| File symbol inventory | `get_symbols_overview` | `Read` + `Grep` headings/classes/functions |
| Named symbol lookup | `find_symbol` | `Grep` exact identifier |
| Downstream impact | `find_referencing_symbols` | `Grep` identifier references |
| Touched-file diagnostics | `get_diagnostics_for_file` | `Bash` test/lint only if cheap and allowed |
| Prior patterns | `list_memories` then `read_memory` | Skip memory |
| Learning persistence | `write_memory` | Write nothing; report memory unavailable |
| Evidence completeness checkpoint | `think_about_collected_information` | Inline checklist |
| Task adherence checkpoint | `think_about_task_adherence` | Inline checklist |
| Completion checkpoint | `think_about_whether_you_are_done` | Inline checklist |
`think_about_*` tools are mandatory checkpoint gates. They are current Serena meta-cognition tools, but they do not replace symbolic evidence. The measurable assertion is that each checkpoint must leave an audit-log row with `checkpoint`, `result`, and `routing_decision`.
## 6. Cross-skill Integration
| Skill | Phase | Contract |
|-------|-------|----------|
| `confidence-check` | Before actionable recommendations | Enforce ≥90% confidence or present alternatives/ask |
| `sc-adversarial-protocol` | Wave 5 | Mode A compare; owns debate/scoring/merge |
| `task-builder` | Wave 7 | Builds corrective MDTM task from validated report |
| `sc-troubleshoot-protocol` | Precursor or fallback | Use for primary bug diagnosis, then reflect on its report |
| `sc-brainstorm-protocol` | Upstream | Reflect can validate brainstorm-generated tasklists/specs |
| `tech-research` | UC-1 best practices | Use for external best-practice validation when Context7 insufficient |
| `sc-validate-tests-protocol` | UC-2 test-specific gaps | Delegate when test validation dominates reflection scope |
No silent downgrade: if a requested downstream skill is missing, STOP for mandatory flows or mark optional integration as skipped with rationale.
## 7. Agent Delegation
| Agent | Tier | Use |
|-------|------|-----|
| `confidence-calibrator` | T1/T2 | Re-grade tier decision and each finding without formation context |
| `evidence-validator` | T1/T2 final | Re-read every citation; drop unsupported claims |
| `rf-qa` | T2 | Structural tasklist/spec vs work verification |
| `rf-qa-qualitative` | T2 | Coherence and product/spec quality checks |
| `root-cause-analyst` | T2 | Explain deviations and classify cause |
| `quality-engineer` | T2 | Edge cases, acceptance assertions, testability |
| `auggie-reviewer` | T2 | Independent code-system review with Auggie + Serena grounding |
| `audit-validator` | T2/T3 | 10% spot-check when findings ≥20 or repo-scale |
| `self-review` | T1 fallback | Low-cost final sanity check; never sole reviewer for high-stakes UC-2 |
Reusable agents are preferred over new agents. If a future `coverage-mapper` or `deviation-classifier` is created, it must be justified by eval failures showing existing agents cannot meet thresholds.
## 8. Tier-decision Rubric with Numeric Thresholds
The protocol records four measurable scores in `tier_decision.yaml`:
| Score | Range | Definition |
|-------|-------|------------|
| `coverage_gap_rate` | 0.0-1.0 | Unmapped source items / total source items |
| `evidence_conflict_rate` | 0.0-1.0 | Contradictory evidence items / total evidence items |
| `blast_radius_score` | 0.0-1.0 | Normalized changed files, domains, and downstream references |
| `stakes_score` | 0.0-1.0 | Security/destructive/deploy/data-loss/compliance severity |
Decision formula:
```text
complexity_score = min(1.0,
  0.30 * coverage_gap_rate +
  0.25 * evidence_conflict_rate +
  0.25 * blast_radius_score +
  0.20 * stakes_score +
  explicit_signal_bonus)
```
Explicit signal bonus is capped at `0.20` and comes from `--depth deep`, failed diagnostics, ambiguous mode, or prior memory false-negative.
Thresholds:
- Tier 1: `complexity_score < 0.35`, `coverage_gap_rate = 0`, `stakes_score < 0.30`, calibrated confidence ≥ 0.85.
- Tier 2: `complexity_score ≥ 0.35`, `coverage_gap_rate > 0`, `evidence_conflict_rate > 0.20`, or confidence < 0.85.
- Tier 2 + adversarial merge required: `complexity_score ≥ 0.65`, `stakes_score ≥ 0.50`, `evidence_conflict_rate > 0.30`, or two reviewers disagree on final verdict.
- Tier 3 offered: final verdict is not clean-pass and remediation can be represented as an MDTM task.
## 9. Eval Rubric and Acceptance Thresholds
The eval harness grades both deterministic assertions and qualitative quality dimensions on a 0-5 scale. A score of 3 means minimally acceptable; 4 means shippable; 5 means exemplary. The ship gate intentionally targets rigorous 70-90% performance rather than a soft 100%.
### Grading dimensions
1. **Citation accuracy** — every `file:line` citation in `reflection-report.md` resolves to the actual file and line content after re-Read. Threshold: ≥5 for ship; any unresolved citation in a HIGH-severity finding is an auto-fail.
2. **Source coverage completeness** — every source spec/tasklist item appears in `coverage-matrix.yaml` or `completion-matrix.yaml` with status `mapped`, `gap`, `not_applicable`, or `human_decision`. Threshold: ≥4 and deterministic assertion pass rate ≥0.90 for source-item presence.
3. **Deviation-classification precision** — deviations are correctly tagged as `authorized_expansion`, `necessary_deviation`, `drift`, `regression`, or `unknown`, with authorization evidence. Threshold: ≥4; false `complete` on a seeded regression is auto-fail.
4. **Best-practice grounding** — external/library/domain claims are backed by Context7 or documented project conventions, not generic advice. Threshold: ≥3 for Tier 1, ≥4 for Tier 2/3.
5. **Recommendation actionability and scrutiny** — every recommendation has owner/action/evidence/next-check and executable artifacts pass recommendation re-scrutiny. Threshold: ≥4; any HIGH-stakes unverified command presented as safe is auto-fail.
6. **Tier-routing correctness** — eval cases route to expected tier given numeric rubric, with escalation reasons in `tier_decision.yaml`. Threshold: ≥4 and deterministic `yaml_field` assertions for tier pass.
7. **Artifact contract compliance** — required files, return contract fields, audit checkpoint rows, and adversarial artifacts appear exactly where specified. Threshold: ≥4 and deterministic assertion pass rate ≥0.90.
### Aggregate ship threshold
Ship acceptance for iteration N:
- Deterministic assertion pass rate: ≥0.85 overall and ≥0.90 on held-out test cases involving citation resolution and source coverage.
- Qualitative mean: ≥4.0/5 across all seven dimensions.
- No auto-fail condition in any held-out test.
- New skill beats frozen v1 baseline by ≥0.75 points mean qualitative score and ≥15 percentage points deterministic pass rate.
Rationale: 0.85 is inside the recommended 70-90% rigorous-eval band. Reflection is a gatekeeping skill, so the threshold is high enough to catch regressions but not so high that evaluators become superficial to reach 100%.
### Train/test split
Use the skill-creator default 60/40 split:
- Train set: 60% of eval cases used for iteration and prompt/protocol refinement.
- Held-out test set: 40% never inspected during iteration except aggregate scores.
- Stratify by `use_case`, `tier`, `risk`, and `artifact_kind` so both UC-1 and UC-2 appear in train and test.
### Judge model selection
The judge must be different from the skill-under-test execution model and typically more capable. If Tier 1 reflect runs on a mid-tier model, qualitative grading runs on a higher-capability judge. If Tier 2 uses heterogeneous reviewers, the judge is a separate higher-capability model not participating in the reviewer set. For final release, use one primary judge plus optional second-judge calibration on ≥20% of cases to detect positional or verbosity bias.
### Iteration-cycle definition
- **Iteration 1 — pilot contract**: 3 cases: UC-1 simple plan, UC-2 small diff with one seeded gap, UC-2 doc/task artifact with citation checks. Goal: artifact shape, return contract, grader compatibility.
- **Iteration 2 — matrix expansion**: 8-10 cases across quick/standard/deep, pre/post, low/high risk, clean-pass/fail/partial, and adversarial merge. Goal: tier routing and deviation precision.
- **Iteration 3 — held-out hardening**: 12-15 cases with seeded false citations, authorized deviation, regression, missing tests, and recommendation-scrutiny traps. Goal: citation and high-stakes command safety.
Between iterations, only protocol text, refs, agent instructions, and grader assertions may change. Do not edit held-out expected outputs to fit the skill.
### Convergence signal
Stop iterating when iteration N+1 improves held-out deterministic pass rate by <5 percentage points and qualitative mean by <0.20/5, while all auto-fail gates remain clear. If train improves but held-out regresses, revert the protocol change and add a false-positive memory.
### Representative evals JSON skeleton
```json
{
  "skill_name": "sc-reflect-protocol",
  "iteration": 1,
  "split": {"train": 0.6, "test": 0.4},
  "evals": [
    {
      "id": 1,
      "name": "uc1-plan-missing-security-step",
      "prompt": "/sc:reflect --mode pre --source fixtures/spec-auth.md --work fixtures/plan-auth.md --depth standard",
      "expected_use_case": "UC-1",
      "expected_tier": 2,
      "expected_verdict": "revise",
      "assertions": [
        {"text": "coverage matrix exists", "type": "file_exists", "target": "with_skill/outputs/coverage-matrix.yaml"},
        {"text": "tier decision escalates to 2", "type": "yaml_field", "target": "with_skill/outputs/tier_decision.yaml", "field": "tier", "expected": "2"},
        {"text": "report names missing authz check", "type": "regex_present", "target": "with_skill/outputs/reflection-report.md", "pattern": "authorization|authz"}
      ]
    },
    {
      "id": 2,
      "name": "uc2-small-diff-complete",
      "prompt": "/sc:reflect --mode post --source fixtures/tasklist-cache.md --work fixtures/diff-cache-complete.patch --depth quick",
      "expected_use_case": "UC-2",
      "expected_tier": 1,
      "expected_verdict": "complete",
      "assertions": [
        {"text": "completion matrix exists", "type": "file_exists", "target": "with_skill/outputs/completion-matrix.yaml"},
        {"text": "return contract verdict complete", "type": "yaml_field", "target": "with_skill/outputs/return-contract.yaml", "field": "verdict", "expected": "complete"},
        {"text": "all citations resolve", "type": "citation_resolves", "target": "with_skill/outputs/reflection-report.md"}
      ]
    },
    {
      "id": 3,
      "name": "uc2-seeded-regression",
      "prompt": "/sc:reflect --mode post --source fixtures/tasklist-api.md --work fixtures/diff-api-regression.patch --depth standard",
      "expected_use_case": "UC-2",
      "expected_tier": 2,
      "expected_verdict": "fail",
      "assertions": [
        {"text": "deviation ledger includes regression", "type": "yaml_list_contains", "target": "with_skill/outputs/deviation-ledger.yaml", "field": "deviation_class", "expected": "regression"},
        {"text": "adversarial artifacts emitted", "type": "dir_count", "target": "with_skill/outputs/adversarial/", "min_files": 6},
        {"text": "no complete verdict", "type": "regex_absent", "target": "with_skill/outputs/return-contract.yaml", "pattern": "verdict:\\s*complete"}
      ]
    },
    {
      "id": 4,
      "name": "uc2-false-citation-trap",
      "prompt": "/sc:reflect --mode post --source fixtures/tasklist-cli.md --work fixtures/report-with-bad-line.md --depth deep",
      "expected_use_case": "UC-2",
      "expected_tier": 2,
      "expected_verdict": "partial",
      "assertions": [
        {"text": "bad citation removed or marked", "type": "citation_resolves", "target": "with_skill/outputs/reflection-report.md"},
        {"text": "grounding gaps section present", "type": "section_present", "target": "with_skill/outputs/reflection-report.md", "section_pattern": "Grounding Gaps"}
      ]
    },
    {
      "id": 5,
      "name": "uc1-high-stakes-command-block",
      "prompt": "/sc:reflect --mode pre --source fixtures/proxmox-spec.md --work fixtures/plan-start-template.md --depth standard",
      "expected_use_case": "UC-1",
      "expected_tier": 2,
      "expected_verdict": "block",
      "assertions": [
        {"text": "recommendation scrutiny exists", "type": "file_exists", "target": "with_skill/outputs/recommendation-scrutiny.yaml"},
        {"text": "blocked high stakes command", "type": "yaml_list_contains", "target": "with_skill/outputs/recommendation-scrutiny.yaml", "field": "decision", "expected": "block"}
      ]
    }
  ]
}
```
## 10. Iteration-harness Location and Directory Tree
All eval workspaces live under `.dev/eval-workspaces/`, never under `.claude/skills/<name>-workspace/`.
Required tree:
```text
.dev/eval-workspaces/sc-reflect/
├── SPEC.md
├── grader.py
├── aggregate_iteration.py
├── evals/
│   ├── evals.json
│   └── fixtures/
│       ├── specs/
│       ├── tasklists/
│       ├── diffs/
│       └── reports/
├── iterations/
│   ├── iteration-1/
│   │   ├── benchmark.json
│   │   ├── benchmark.md
│   │   ├── quality-grading.json
│   │   ├── review.html
│   │   └── eval-<case-name>/
│   │       ├── eval_metadata.json
│   │       ├── with_skill/
│   │       │   ├── outputs/
│   │       │   ├── run-1/
│   │       │   └── grading.json
│   │       └── old_skill/
│   │           ├── outputs/
│   │           ├── run-1/
│   │           └── grading.json
│   ├── iteration-2/
│   └── iteration-3/
└── skill-snapshot/
    ├── reflect-v1.md
    └── reflect-protocol-v<N>.md
```
`reflect-v1.md` is a frozen copy of the legacy command. `skill-snapshot/reflect-protocol-v<N>.md` captures each iteration candidate so the comparator can A/B against previous iterations.
## 11. New Assertion Types for grader.py
The existing eight assertion types are sufficient for artifact presence and simple YAML/section checks. Reflection needs semantic assertions.
Proposed additions:
1. `citation_resolves`
   - Input: markdown target.
   - Extract `path:line` patterns.
   - Resolve repo-relative paths against eval fixture root or workspace root.
   - Read target line and optional expected substring.
   - Pass only if every citation resolves or is explicitly marked `unverified` in Grounding Gaps.
2. `regex_present`
   - Input: target file, regex pattern.
   - Pass if pattern matches file text.
   - Used for seeded requirement/finding mentions.
3. `regex_absent`
   - Input: target file, regex pattern.
   - Pass if pattern does not match.
   - Used for avoiding false clean-pass verdicts.
4. `yaml_list_contains`
   - Input: simple YAML target, field, expected.
   - Minimal implementation can scan lines below `field:` for `- expected`.
   - Later implementation can use PyYAML if dependency policy permits.
5. `matrix_covers_items`
   - Input: source fixture, matrix YAML, min coverage rate.
   - Count source items by checkbox/bullet IDs.
   - Count matrix rows with matching `source_item_id`.
   - Pass if coverage ≥ threshold.
6. `checkpoint_logged`
   - Input: `audit.log`, checkpoint name.
   - Pass if audit includes `checkpoint=<name>` and `routing_decision=`.
   - Verifies scripted Serena think checkpoints are actually wired.
Implementation sketch for `citation_resolves`:
```python
def check_citation_resolves(assertion, base_dir):
    content = read_text(base_dir / assertion["target"])
    if not content:
        return False, "File not readable"
    citations = re.findall(r"([A-Za-z0-9_./-]+\.(?:py|md|toml|yaml|yml|json|ts|tsx|js)):(\d+)", content)
    unresolved = []
    for rel, line_s in citations:
        p = (base_dir / rel) if (base_dir / rel).exists() else (WORKSPACE_ROOT / rel)
        lines = read_text(p).splitlines() if read_text(p) else []
        line_no = int(line_s)
        if line_no < 1 or line_no > len(lines):
            unresolved.append(f"{rel}:{line_s}")
    if unresolved:
        return False, "Unresolved citations: " + ", ".join(unresolved)
    return True, f"All {len(citations)} citations resolve"
```
The actual implementation should avoid double reads and should support fixture-root remapping for synthetic eval diffs.
## 12. Build Path Decision
Pick **skill-creator-style iterative refinement first**, then use Sprint CLI after the skill stabilizes.
Rationale:
- `/sc:reflect` is itself an evaluator/gatekeeper; building it without an eval-first loop risks encoding untested judgment prose.
- Skill-creator's create/eval/improve/benchmark cycle maps directly to the required 60/40 train/test split, JSON test cases, 0-5 rubric, and A/B comparison against the legacy command.
- The local `.dev/eval-workspaces/sc-brainstorm/` harness already mirrors that pattern and can be adapted quickly.
- Sprint CLI remains valuable after the draft is stable: run a full tasklist implementation through `superclaude sprint run` to verify component sync, hooks, UV-only tests, and repository pipeline compatibility.
- The eval CLI can be deferred until the simple grader cannot represent required cases or real-process isolation becomes necessary.
Build sequence:
1. Author `src/superclaude/skills/sc-reflect-protocol/SKILL.md` and refs.
2. Thin `src/superclaude/commands/reflect.md` to activate the skill.
3. Create `.dev/eval-workspaces/sc-reflect/` harness from the brainstorm pattern.
4. Run iteration-1 pilots; improve protocol; snapshot.
5. Expand to iteration-2 matrix; hold out 40%.
6. Run iteration-3 hardening; stop on convergence signal.
7. Run `make sync-dev`, `make verify-sync`, `uv run pytest` targeted tests, then Sprint CLI only for production-style task execution.
## 13. Versioned Return Contract
Write to `<output-dir>/return-contract.yaml` and return inline.
Stable contract v1.0:
```yaml
contract_version: "1.0"
status: success | partial | failed | blocked | dry-run
mode: pre | post
tier_reached: 1 | 2 | 3
verdict: pass | revise | block | complete | partial | fail | needs-human-decision
source_path: <absolute-path>
work_path: <absolute-path|null>
output_dir: <absolute-path>
reflection_report_path: <absolute-path>
coverage_matrix_path: <absolute-path|null>
completion_matrix_path: <absolute-path|null>
deviation_ledger_path: <absolute-path|null>
tier_decision_path: <absolute-path>
calibrated_confidence: <float 0.0-1.0>
complexity_score: <float 0.0-1.0>
escalation_reason: <string|null>
adversarial_artifacts_dir: <absolute-path|null>
remediation_offered: <bool>
remediation_task_path: <absolute-path|null>
grounding_gaps: [<strings>]
high_stakes_blockers: [<strings>]
```
Telemetry block, non-stable:
```yaml
telemetry:
  wave_durations_ms: {}
  token_estimates: {}
  serena_available: true|false
  auggie_available: true|false
  checkpoint_results:
    collected_information: pass|concern|skipped
    task_adherence: pass|concern|skipped
    whether_done: pass|concern|skipped
  agents_spawned: []
  judge_model_class: <alias|null>
  reviewer_model_classes: []
  eval_harness_version: <string|null>
```
Downstream consumers must read only stable fields unless they explicitly opt into telemetry.
## 14. Error Handling Matrix
| Scenario | Behavior | Fallback |
|----------|----------|----------|
| Missing source | STOP | Ask for `--source` |
| Missing work in post mode | STOP | Ask for `--work` or use `--mode pre` |
| Output path under `.claude/` generated mirrors | STOP | Redirect to `.dev/reflect/` |
| Serena unavailable | Continue degraded | `Read`/`Grep`/`Glob`, mark checkpoints skipped |
| Auggie unavailable | Continue degraded | Native search + Serena symbols |
| Context7 unavailable for best-practice check | Continue if LOW/MEDIUM | Tavily/WebSearch fallback; HIGH-stakes blocks if unresolved |
| `think_about_*` checkpoint unavailable | Continue degraded | Inline checklist; mark `checkpoint_logged: skipped` |
| confidence-calibrator fails | Continue partial | Inline calibration with audit marker |
| Tier 2 reviewer fails | Continue if ≥2 reviewers remain | Otherwise downgrade to Tier 1 partial |
| All Tier 2 reviewers fail | Return Tier 1 partial | Recommend rerun with narrower scope |
| sc-adversarial missing when required | STOP | No inline debate fallback |
| sc-adversarial returns empty/unparseable | Partial | Highest calibrated Tier 2 verdict + warning |
| evidence-validator fails | Inline citation validation | Status partial; never skip validation entirely |
| Citation mismatch | Drop or mark claim unverified | Add Grounding Gaps entry |
| HIGH-stakes command precondition unknown | Block recommendation | Ask user to verify precondition manually |
| User declines Tier 3 remediation | Return final report | No task-builder call |
| task-builder missing for accepted remediation | Partial | Surface manual remediation checklist |
| Memory write fails | Continue | Report memory persistence skipped |
## 15. Boundaries
### Will
- Validate pre-execution plans against specs/tasklists before tool execution.
- Validate post-execution work against source-of-truth artifacts and diffs/logs.
- Use Auggie and Serena for code-system grounding before findings are synthesized.
- Use Serena `think_about_*` as scripted checkpoints with logged routing decisions.
- Use reusable agents for coverage, calibration, evidence validation, and QA.
- Delegate debate/scoring/merge to `sc-adversarial-protocol` without duplicating it.
- Produce deterministic artifacts that the eval harness can assert against.
- Re-scrutinize executable recommendations before delivery.
- Persist compact reflection memories with project-scoped names.
- Respect `src/superclaude/` as source of truth and `.dev/eval-workspaces/sc-reflect/` as eval workspace.
### Will Not
- Edit `.claude/skills/`, `.claude/commands/`, `.claude/agents/`, or `.claude/hooks/` as source of truth.
- Stage or recommend staging `.claude/` generated mirrors.
- Implement its own debate, scoring, base selection, or merge algorithm.
- Auto-apply source-code fixes during reflection.
- Auto-run `/task` after creating a remediation task file.
- Treat same-model self-review as sufficient for high-stakes UC-2 validation.
- Ship findings with fake or unchecked `file:line` citations.
- Present HIGH-stakes commands as safe when preconditions are unknown.
- Modify held-out eval expected outputs to improve apparent scores.
## 16. Testability Map
| Protocol decision | Eval assertion |
|-------------------|----------------|
| Output dir guard | `regex_absent` in audit for forbidden path + STOP fixture |
| Mode auto-detection | `yaml_field return-contract.yaml mode` |
| Tier thresholds | `yaml_field tier_decision.yaml tier` and `yaml_field_min complexity_score` |
| Serena checkpoints | `checkpoint_logged audit.log <checkpoint>` |
| Coverage matrix | `matrix_covers_items` |
| Deviation taxonomy | `yaml_list_contains deviation-ledger.yaml deviation_class` |
| Adversarial delegation | `dir_count adversarial/ min_files=6` |
| Citation grounding | `citation_resolves reflection-report.md` |
| Recommendation scrutiny | `yaml_list_contains recommendation-scrutiny.yaml decision` |
| Return contract stability | `yaml_field contract_version=1.0` |
| Memory write optionality | `yaml_substring telemetry memory_status` |
A protocol step that cannot map to at least one deterministic or qualitative eval assertion should be simplified or removed.
