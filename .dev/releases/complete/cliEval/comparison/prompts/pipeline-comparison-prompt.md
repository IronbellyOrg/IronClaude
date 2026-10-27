# Reusable Prompt: Adversarial Comparison of Tasklist Outputs Across Two Pipelines

**Version:** 1.0
**Purpose:** Standardized scoring + adversarial debate of tasklists produced by two competing pipelines (e.g., task-builder vs Sprint CLI) for the same design specification.
**Reusable for:** Any future task-builder-vs-tasklist pipeline comparison; not hard-coded to `cliEval`.
**Recommender:** `/sc:recommend` via `sc:recommend-protocol` (verified-interface output, Rule-1/2/3 compliant).
**Cost envelope:** ~465-725K tokens per full run (12 agents + 1 `/sc:adversarial` hand-off + 2 `/sc:analyze` invocations + verification).

---

## How to use this prompt

1. Substitute the four `{{TEMPLATE_VARIABLES}}` at the top of Section A below with concrete values for the comparison you are running.
2. Paste the entire prompt body (Sections A through E) into a fresh Claude Code chat OR pass it as the `prompt` argument to a top-level `Agent` tool invocation.
3. The receiving agent will self-discover artifact paths and execute the 6 phases declaratively.
4. Final delta verdict + confidence land at `{{OUTPUT_DIR}}/comparison-summary.md` plus a structured `comparison-summary.json`.

---

# Section A — Template Variables (substitute before running)

```
{{RELEASE_ID}}                  e.g., "cliEval"
{{PIPELINE_A_ARTIFACT_GLOB}}    e.g., ".dev/tasks/to-do/TASK-*-cliEval-*/TASK-*-cliEval-*.md"
{{PIPELINE_B_ARTIFACT_GLOB}}    e.g., ".dev/releases/current/cliEval/tasklist/**/*.md"
{{OUTPUT_DIR}}                  e.g., ".dev/releases/current/cliEval/comparison/run-<ISO>/"
```

If the maintainer has not provided values for these, the receiving agent MUST `AskUserQuestion` to obtain them before proceeding (do not invent defaults).

---

# Section B — Objective

You are executing a six-phase comparative analysis. The output is a **delta verdict**: which pipeline produces better tasklists for releases of this scope, by how much, with what confidence, and which dimensions drove the delta.

## Pipelines under comparison

- **Pipeline A** ("task-builder pipeline"): shared design spec → `/task-builder` skill → one or more MDTM task files at `{{PIPELINE_A_ARTIFACT_GLOB}}`. Executed manually via `/task`.
- **Pipeline B** ("Sprint CLI pipeline"): shared design spec → `/sc:spec-panel` → `/sc:design` → `superclaude roadmap` → `/sc:tasklist` → `superclaude sprint run`. Outputs at `{{PIPELINE_B_ARTIFACT_GLOB}}`. Executed via Sprint CLI.

## What this comparison does NOT do

- Does NOT execute either pipeline's tasklist (that is a separate workstream).
- Does NOT score the **design spec** itself (both pipelines consume the same spec; spec quality is constant).
- Does NOT make value judgments about pipeline ergonomics (single-shot vs CLI-orchestrated); only artifact quality.
- Does NOT modify either pipeline's source artifacts. Read-only end-to-end.

## What this comparison MUST produce

- A 12-dimension scoring matrix per pipeline (Section C rubric).
- An `/sc:adversarial`-driven debate over the two scoring outputs (Section D hand-off).
- A final delta verdict with confidence percentage (Section E synthesis).
- All artifacts under `{{OUTPUT_DIR}}` with deterministic, reproducible filenames.

---

# Section C — Scoring Framework (the rubric)

This rubric is the **single source of truth** for scoring. Every parallel agent uses these 12 dimensions, these weights, and these score thresholds. Do not invent variants.

## 12 dimensions, 3 groups, weighted

| Group | Dimension | Weight | What it measures |
|---|---|---|---|
| **Structural** | D1. Coverage / Completeness | 1.5× | % of design-spec ACs that map to at least one tasklist item with a verifying step |
| **Structural** | D2. Granularity / Atomic items | 1.0× | Per-item self-containment, single-paragraph items vs multi-step blobs |
| **Structural** | D3. Dependency clarity | 1.0× | Explicit prereq gates; merge-to-master dependency declarations; blocked-by relationships |
| **Structural** | D4. Quality gates | 1.5× | Phase-gate QA presence, fix-cycle caps, retry monotonicity, acceptance criteria → item mapping |
| **Operational** | D5. Executability | 1.5× | Cold-start friction: can the artifact be handed to its target executor today with zero prep? |
| **Operational** | D6. Fidelity to source spec | 1.5× | No phantom requirements; no missing ACs; all "ensuring..." clauses traceable to the spec |
| **Operational** | D7. Adaptability / Resilience | 1.0× | Failure-mode handling, retry mechanism quality, escape hatches on cycle exhaust |
| **Operational** | D8. Reviewability | 1.0× | Can a human reviewer evaluate in <30 min? Diff readability? Section organization? |
| **Meta** | D9. Reproducibility | 0.75× | Running the same pipeline against the same spec → same tasklist? Deterministic ordering, naming, sequencing? |
| **Meta** | D10. Token efficiency | 0.75× | Total artifact LOC; bytes per AC; cost-to-produce-and-execute |
| **Meta** | D11. Risk surface | 0.75× | Failure modes that could damage the codebase (destructive ops, missing safety guards, weak rollback) |
| **Meta** | D12. Auditability | 1.0× | Post-execution traceability: which artifact came from which item; provenance fidelity |

## Per-dimension score thresholds

| Score | Label | Meaning |
|---|---|---|
| 9-10 | EXCELLENT | Dimension is exemplary; would be a positive reference for future releases |
| 7-8 | PASS | Dimension is well-handled; no actionable improvement needed |
| 5-6 | MARGINAL | Dimension works but has identifiable weaknesses worth fixing |
| 3-4 | WEAK | Dimension has serious problems that would degrade execution |
| 0-2 | FAIL | Dimension is broken / absent; would block successful execution |

## Per-dimension scoring requirements (mandatory for every agent)

For every dimension scored, the agent MUST emit:

```yaml
dimension: D{1-12}
dimension_name: "<the dimension name>"
pipeline: "A" | "B"
score: <0-10 integer>
label: "EXCELLENT|PASS|MARGINAL|WEAK|FAIL"
weight: <1.5|1.0|0.75>
evidence:
  - file: "<path>"
    line: <line number or range>
    quote: "<verbatim excerpt, ≤120 chars>"
    rationale: "<why this evidence supports the score, ≤200 chars>"
  # MINIMUM 2 evidence entries per dimension
counter_evidence:                  # weaknesses found even if score is high
  - file: "<path>"
    line: <line number or range>
    issue: "<what's wrong or missing, ≤200 chars>"
  # 0 or more entries
recommendation:                    # what would push this dimension to 10
  text: "<concrete improvement, ≤300 chars>"
```

Fabricated scores, evidence-less assertions, or rationale shorter than the required minimum disqualify the agent's output and trigger a re-score.

## Weighted aggregation

For each pipeline:

```
raw_score        = Σ (dimension_score × dimension_weight)
max_possible     = Σ (10 × dimension_weight)              = 130.0
percent_score    = raw_score / max_possible × 100
critical_score   = Σ_{D1,D4,D5,D6} dimension_score        # the four 1.5× weighted ones; 0-40 raw
critical_percent = critical_score / 40 × 100
```

Final pipeline grade:

| Grade | Condition |
|---|---|
| A | percent_score ≥ 85% AND no dimension below 5 |
| B | percent_score ≥ 75% AND critical_percent ≥ 80% AND no critical dimension below 6 |
| C | percent_score ≥ 65% AND no critical dimension below 5 |
| D | percent_score ≥ 50% |
| F | any of: percent_score < 50%; OR ANY critical dimension below 5; OR ANY dimension at FAIL (0-2) |

## Delta verdict definitions

| Delta term | Meaning |
|---|---|
| **A-WINS** | Pipeline A percent_score > Pipeline B by ≥10 points AND A's critical_percent ≥ B's |
| **B-WINS** | Symmetric for B |
| **HYBRID-BEATS-BOTH** | Per-dimension max-of-A-or-B aggregated would exceed both A and B individual scores by ≥5 points (suggests a synthesis would beat either alone) |
| **TIE** | abs(A.percent_score − B.percent_score) < 10 AND neither has critical-dimension-FAIL |
| **BOTH-FAIL** | Both pipelines score F |

---

# Section D — The 6-Phase Execution Plan

## Phase 0 — Self-discovery & gate

**Action items (sequential):**

1. Use `Glob` on `{{PIPELINE_A_ARTIFACT_GLOB}}` to enumerate Pipeline A files. Store the list as `PIPELINE_A_FILES`.
2. Use `Glob` on `{{PIPELINE_B_ARTIFACT_GLOB}}` to enumerate Pipeline B files. Store the list as `PIPELINE_B_FILES`.
3. If either list is empty: HALT and emit `**Verdict:** BLOCKED — <pipeline> has no artifacts at <glob>. Resolve before retrying.` Exit phase 0.
4. Read the design spec source. Default location: `.dev/releases/current/{{RELEASE_ID}}/design-spec.md`. If absent, `AskUserQuestion` for the design-spec path. Store as `DESIGN_SPEC_PATH`.
5. Read the design spec. Extract every line matching `^- [Aa][Cc]-` or `\*\*AC-` (acceptance criteria markers). Store the count as `TOTAL_ACS_IN_SPEC`. This is the denominator for D1 (Coverage).
6. Create `{{OUTPUT_DIR}}` and these subdirectories: `baselines/`, `scores/`, `adversarial-output/`, `qa/`, `final/`.
7. Write `{{OUTPUT_DIR}}/run-context.yaml` with: `release_id`, `pipeline_a_files`, `pipeline_b_files`, `design_spec_path`, `total_acs`, `started_at`.

**Gate:** Both pipelines have ≥1 file AND `TOTAL_ACS_IN_SPEC > 0` → proceed to Phase 1.

## Phase 1 — Structural baseline per pipeline (2 parallel `/sc:analyze` invocations)

Hand off to `/sc:analyze` for each pipeline. The receiving agent MUST invoke the actual `/sc:analyze` command (Rule 3: invoke, do not reimplement).

**Pipeline A invocation:**
```
/sc:analyze {{PIPELINE_A_DIR}} --focus architecture,quality --depth deep --format report
```
Output captured to `{{OUTPUT_DIR}}/baselines/baseline-A.md`.

**Pipeline B invocation:**
```
/sc:analyze {{PIPELINE_B_DIR}} --focus architecture,quality --depth deep --format report
```
Output captured to `{{OUTPUT_DIR}}/baselines/baseline-B.md`.

These baselines provide architecture/quality findings the parallel scorers may reference as evidence but are NOT scored themselves. They serve as input context for Phase 2.

**Parallelism:** Phase 1 invocations are independent. Run both in parallel via two simultaneous `Agent` (or `Skill`) tool calls in one message.

## Phase 2 — Parallel rubric scoring (6 agents, 3 per pipeline)

Six `Agent` (`general-purpose`) tool calls in a single message. Each agent receives:

- The full rubric from Section C
- The list of files for ITS pipeline only
- The baseline report for ITS pipeline (from Phase 1)
- The 4 dimensions ITS group covers
- The design spec path (for fidelity / coverage)
- The output destination for ITS score fragment

### Agent fan-out specification

| Agent ID | Pipeline | Dimensions | Output file |
|---|---|---|---|
| A-1 | Pipeline A | D1, D2, D3, D4 (Structural) | `{{OUTPUT_DIR}}/scores/A-structural.yaml` |
| A-2 | Pipeline A | D5, D6, D7, D8 (Operational) | `{{OUTPUT_DIR}}/scores/A-operational.yaml` |
| A-3 | Pipeline A | D9, D10, D11, D12 (Meta) | `{{OUTPUT_DIR}}/scores/A-meta.yaml` |
| B-1 | Pipeline B | D1, D2, D3, D4 (Structural) | `{{OUTPUT_DIR}}/scores/B-structural.yaml` |
| B-2 | Pipeline B | D5, D6, D7, D8 (Operational) | `{{OUTPUT_DIR}}/scores/B-operational.yaml` |
| B-3 | Pipeline B | D9, D10, D11, D12 (Meta) | `{{OUTPUT_DIR}}/scores/B-meta.yaml` |

### Boilerplate agent prompt (paste into each `Agent` call, varying the bracketed fields)

```
You are scoring **{{PIPELINE_LABEL}}** of a two-pipeline comparison.
Your group: **{{GROUP_NAME}}** — dimensions {{DIMENSION_IDS}}.

INPUTS:
- Pipeline files: {{PIPELINE_FILES_LIST}}
- Pipeline baseline report: {{BASELINE_REPORT_PATH}}
- Design spec (source of truth for ACs): {{DESIGN_SPEC_PATH}}
- Total ACs in design spec: {{TOTAL_ACS_IN_SPEC}}

REQUIREMENTS (mandatory):
1. Read every pipeline file end-to-end. No skimming.
2. For each of your 4 dimensions:
   a. Score 0-10 per the rubric labels (Section C of the parent prompt).
   b. Provide MINIMUM 2 evidence entries with verbatim quotes and file:line citations.
   c. Provide counter-evidence (weaknesses) even if your score is 9-10.
   d. Provide a concrete recommendation to push the score to 10.
3. Output YAML exactly matching the per-dimension schema in Section C.
4. NO fabricated evidence. NO unscored dimensions. NO scores without quotes.
5. Write your output as a single YAML document to: {{OUTPUT_FILE}}

ADVERSARIAL STANCE:
Assume the pipeline has weaknesses. Your default is skepticism. Look for the
strongest counter-example to the surface impression. A 10/10 score requires
you to have actively searched for failure modes and not found them.

ANTI-CHEATING:
You cannot read the OTHER pipeline's files. Your scoring is independent.
The aggregator (Phase 3) handles cross-pipeline awareness; you do not.
```

**Parallelism:** All 6 agents fan out simultaneously in a single message (6 `Agent` tool calls in one block). No sequential dependencies among them. Wait for all 6 to return before Phase 3.

## Phase 3 — Aggregation (2 sequential aggregators, one per pipeline)

Two `Agent` (`general-purpose`) tool calls, possibly in parallel since they are independent.

Each aggregator:
1. Reads its pipeline's 3 score-fragment YAML files (`{{PIPELINE}}-structural.yaml`, `-operational.yaml`, `-meta.yaml`).
2. Validates: all 12 dimensions present; no missing evidence; no score outside 0-10 range; weights match Section C.
3. If validation fails, **re-issue the failing score fragment** by re-spawning the appropriate Phase-2 agent for that specific group. Cap: 1 re-issue per group. After cap, mark as INCOMPLETE-SCORE in the aggregate.
4. Compute `raw_score`, `max_possible`, `percent_score`, `critical_score`, `critical_percent`, `grade` per Section C formulas.
5. Write a structured markdown report to `{{OUTPUT_DIR}}/scores/score-{{PIPELINE}}.md` with:
   - YAML frontmatter containing the computed metrics
   - A 12-row dimension table
   - Per-dimension evidence quotes inlined
   - A "Top 5 strengths" and "Top 5 weaknesses" section derived from the evidence + counter-evidence
6. Write a parallel JSON to `{{OUTPUT_DIR}}/scores/score-{{PIPELINE}}.json` for machine consumption by Phase 4.

**Output filenames are mandatory** (Phase 4 reads them by exact path):
- `{{OUTPUT_DIR}}/scores/score-A.md`
- `{{OUTPUT_DIR}}/scores/score-B.md`
- `{{OUTPUT_DIR}}/scores/score-A.json`
- `{{OUTPUT_DIR}}/scores/score-B.json`

## Phase 4 — Adversarial debate (hand-off to `/sc:adversarial`)

**Invoke `/sc:adversarial` Mode A** to debate the two score reports. **Do NOT reimplement the debate protocol.** The receiving agent invokes the actual command and trusts its 5-step protocol (diff-analysis → debate → scoring → refactor-plan → merge).

### Verified invocation (from the recommender's interface record)

Use the `Skill` tool (per the protocol skill's documented invocation pattern in `src/superclaude/skills/sc-roadmap-protocol/refs/adversarial-integration.md`):

```
Skill sc:adversarial-protocol args: "--compare {{OUTPUT_DIR}}/scores/score-A.md,{{OUTPUT_DIR}}/scores/score-B.md --depth deep --focus structure,completeness,fidelity,executability --output {{OUTPUT_DIR}}/adversarial-output/ --convergence 0.85 --auto-stop-plateau"
```

Or directly via the command surface:

```
/sc:adversarial --compare {{OUTPUT_DIR}}/scores/score-A.md,{{OUTPUT_DIR}}/scores/score-B.md \
                --depth deep \
                --focus structure,completeness,fidelity,executability \
                --output {{OUTPUT_DIR}}/adversarial-output/ \
                --convergence 0.85 \
                --auto-stop-plateau
```

### Flag rationale (every flag verified against `src/superclaude/commands/adversarial.md`)

| Flag | Verified value | Why |
|---|---|---|
| `--compare` | `score-A.md,score-B.md` | Mode A is the direct fit; comparing two pre-scored artifacts |
| `--depth` | `deep` | Multi-round + convergence check + invariant probe; tasklist comparison merits the full protocol |
| `--focus` | `structure,completeness,fidelity,executability` | Aligns with the 4 critical-weight dimensions (D1, D4, D5, D6) |
| `--output` | `{{OUTPUT_DIR}}/adversarial-output/` | Routes the 6 protocol artifacts to a dedicated subdir |
| `--convergence` | `0.85` | Per spec, range 0.50-0.99, default 0.80. 0.85 gates Round 3 strictly. |
| `--auto-stop-plateau` | (set) | Avoids wasteful rounds if convergence plateaus per the protocol's plateau-detection logic |

### Forbidden flags (would be fabrication)

Do NOT add: `--rounds`, `--evidence-required`, `--steelman-strategy`, `--verdict-per-claim`, `--measure-first`, `--rubric`. None of these exist in the verified flag table. The protocol owns its rubric internally.

### What `/sc:adversarial` will produce (per its `Behavioral Summary`)

Six artifacts in `{{OUTPUT_DIR}}/adversarial-output/`:

1. `diff-analysis.md` — per-claim diff between score-A and score-B
2. `debate-transcript.md` — multi-round advocate debate
3. `base-selection.md` — quantitative-qualitative scoring + selected base
4. `refactor-plan.md` — how to merge strengths if HYBRID emerges
5. `merge-log.md` — provenance annotations
6. The merged output (likely `merged-scoring.md` or similar — let the protocol name it)

These outputs are consumed by Phase 6 (synthesis). Do not pre-judge the merge result; let the protocol drive.

## Phase 5 — Adversarial-output quality verification (`rf-qa-qualitative`)

Spawn `rf-qa-qualitative` (subagent type, NOT a `/sc:*` command) with `qa_phase: "report-validation"` to verify the adversarial output is sound:

```
Subagent type: rf-qa-qualitative
Task: Verify /sc:adversarial output for run {{RELEASE_ID}}.
Inputs:
  - {{OUTPUT_DIR}}/adversarial-output/*.md (all 6 produced artifacts)
  - {{OUTPUT_DIR}}/scores/score-A.md, score-B.md (inputs to the debate)
  - {{OUTPUT_DIR}}/baselines/baseline-A.md, baseline-B.md (Phase 1 context)
Checklist (apply task-qualitative rubric):
  1. Every claim in debate-transcript.md cites evidence from score-A or score-B (no hallucinated claims).
  2. The convergence_score reported is computable from the per-point scoring matrix.
  3. base-selection.md's verdict is consistent with the debate-transcript's per-point winners.
  4. refactor-plan.md proposes only synthesis steps that are LOC-bounded and concrete.
  5. The merge output (if produced) does not invent dimensions not in score-A or score-B.
ADVERSARIAL STANCE: assume the adversarial pipeline cut corners. Find what was missed.
Output: {{OUTPUT_DIR}}/qa/adversarial-qa-report.md with PASS/FAIL verdict.
```

If verdict is FAIL: re-run Phase 4 once with `--interactive` flag added (forces user-approval gates). Cap at 1 re-run. If still FAIL: proceed to Phase 6 but record the QA failure in the final verdict's confidence reduction.

## Phase 6 — Final synthesis & delta verdict

Spawn one `general-purpose` agent to produce the final report. It reads:

- `{{OUTPUT_DIR}}/scores/score-A.json` and `score-B.json` (raw metrics)
- `{{OUTPUT_DIR}}/adversarial-output/base-selection.md` (debate verdict)
- `{{OUTPUT_DIR}}/adversarial-output/refactor-plan.md` (hybrid feasibility)
- `{{OUTPUT_DIR}}/qa/adversarial-qa-report.md` (Phase 5 verification)

It produces TWO files:

### `{{OUTPUT_DIR}}/final/comparison-summary.md` (human-readable)

Required structure (the synthesizer MUST follow this template):

```markdown
# Pipeline Comparison: {{RELEASE_ID}} — Delta Verdict
**Date:** <ISO>
**Pipelines:** A (task-builder) vs B (Sprint CLI)
**Total ACs in spec:** {{TOTAL_ACS_IN_SPEC}}
**Confidence:** XX% (derive: see "Confidence calculation" below)

## Aggregate scores
| | Pipeline A | Pipeline B | Δ (A − B) |
|---|---|---|---|
| percent_score | XX.X% | XX.X% | ±X.X |
| critical_percent | XX.X% | XX.X% | ±X.X |
| grade | X | X | — |

## Per-dimension delta (12 rows)
| Dim | Name | Weight | A | B | Δ | Winner |
|---|---|---|---|---|---|---|
| D1 | Coverage | 1.5× | X | X | ±X | A/B/= |
| ... |

## Final verdict
**Delta:** A-WINS | B-WINS | HYBRID-BEATS-BOTH | TIE | BOTH-FAIL
**Verbatim:** <one-paragraph plain-English summary referencing the dominant dimensions>

## Top 5 dimensions driving the delta
1. <Dimension name>: A=X, B=Y, Δ=±Z. <One-sentence explanation citing evidence file:line>
2. ...
5. ...

## Hybrid feasibility (if applicable)
If HYBRID-BEATS-BOTH or close-to-it, list the 3-5 best combination opportunities
from refactor-plan.md, expressed as: "Take Pipeline A's <strength> and combine
with Pipeline B's <strength> to achieve <expected outcome>."

## Confidence calculation
- Base: 1.0
- Subtract 0.10 if Phase 5 QA verdict was FAIL
- Subtract 0.05 per dimension where score divergence > 4 points between Phase 2 agent and a hypothetical re-score (inter-agent agreement proxy; if not measurable, subtract 0.0)
- Subtract 0.10 if convergence_score from adversarial-output < 0.70
- Subtract 0.05 if total_acs_in_spec is < 5 (small-sample noise)
- Multiply by 100 for percentage
Final confidence: clamped to [50, 100]

## Open questions for the maintainer (≤ 5)
1. <question> — <why it matters for next-pipeline-comparison>
```

### `{{OUTPUT_DIR}}/final/comparison-summary.json` (machine-readable)

JSON mirror of the human-readable summary with the same fields. Used by downstream automation if comparison becomes a CI gate.

---

# Section E — Pass/Fail criteria for the comparison itself

The comparison **PASSES** (i.e., produced a trustworthy verdict) when ALL of these hold:

- [ ] Phase 0 gate cleared (both pipelines had artifacts; design spec found)
- [ ] All 6 Phase-2 agents produced valid score fragments (no INCOMPLETE-SCORE markers)
- [ ] Phase 4 `/sc:adversarial` invocation returned all 6 expected artifacts
- [ ] Phase 5 `rf-qa-qualitative` verdict is PASS, OR the FAIL was disclosed in the confidence calculation
- [ ] Phase 6 final summary cites every dimension's score with file:line evidence
- [ ] Final confidence ≥ 60%

The comparison **FAILS** (verdict NOT trustworthy) when ANY of these hold:

- Any Phase-2 agent emitted fabricated evidence (no file:line, or quote does not match)
- `/sc:adversarial` could not reach convergence after 3 rounds AND `--auto-stop-plateau` did not engage
- Phase 5 QA verdict was FAIL twice (after the 1 retry cap)
- Final confidence < 60%

On comparison-fails, the synthesizer MUST emit `**Verdict:** UNRELIABLE — see <reason>` instead of A/B/HYBRID/TIE. The maintainer can then decide whether to re-run with different parameters or accept the partial output.

---

# Section F — Anti-fabrication rules (mandatory at every phase)

1. **Every score has evidence.** A dimension scored 7 with no `file:line` citation is INVALID.
2. **Every quote is verbatim.** If the file says "must" and the quote says "should", the score is rejected.
3. **No "ghost dimensions."** The 12 dimensions in Section C are the only ones scored. Adding D13 or splitting D5 is forbidden.
4. **No "ghost flags" on `/sc:adversarial`.** The verified flag table in Section D is exhaustive. Adding `--rounds`, `--rubric`, `--steelman-strategy` etc. is a Rule-3 violation.
5. **Inter-agent isolation in Phase 2.** Scorers must not see each other's outputs until Phase 3 aggregation.
6. **Pipeline isolation in Phase 2.** A-scorers cannot read Pipeline B files, and vice versa.
7. **The rubric is constant.** Do not "improve" the rubric mid-run. If the rubric is broken, halt and report.

---

# Section G — Reproducibility checklist

Run the same comparison twice on the same artifacts; the following MUST be stable across runs (i.e., deterministic):

- Per-dimension scores within ±1 point
- Final percent_score within ±2.0
- Critical_percent within ±2.0
- Delta verdict label (A-WINS, B-WINS, TIE, HYBRID-BEATS-BOTH, BOTH-FAIL)
- Confidence within ±5 points

If variance exceeds these bounds across runs, the rubric or the scorers need calibration — escalate.

---

# Section H — Estimated cost & wall-clock (per full run)

| Phase | Activity | Tokens | Wall-clock |
|---|---|---|---|
| 0 | Self-discover & gate | ~5K | <1 min |
| 1 | 2 × `/sc:analyze --depth deep` (parallel) | 80-150K | 5-10 min |
| 2 | 6 × parallel scoring agents | 180-300K | 10-15 min |
| 3 | 2 × aggregators | 40K | 3-5 min |
| 4 | `/sc:adversarial --depth deep` | 80-150K | 10-20 min |
| 5 | `rf-qa-qualitative` verification | 50K | 5-8 min |
| 6 | Final synthesizer | 30K | 2-4 min |
| **Total** | — | **465-725K** | **35-60 min** |

Costs assume default Claude pricing; substitute model-specific pricing as needed.

---

# Section I — Reusability notes

This prompt is parameterized over `{{RELEASE_ID}}` and the four template variables. To reuse for a different pipeline comparison:

1. Substitute the template variables at the top of Section A.
2. If the rubric needs domain-specific adjustments (e.g., new dimensions for a database-migration tasklist), version the rubric (`v1.0` → `v1.1`) and document the diff in a `CHANGELOG` next to this file. Do NOT silently mutate the rubric.
3. If `/sc:adversarial`'s flag set evolves (new flags added upstream), re-verify against the latest `src/superclaude/commands/adversarial.md` before incorporating new flags into Section D.

This prompt explicitly **invokes** `/sc:adversarial` and `/sc:analyze` rather than **reimplementing** them. If either command's protocol changes in a future SuperClaude release, the comparison automatically inherits the upgrade.

---

# Appendix A — Quick-start invocation skeleton

For a maintainer who just wants to copy-paste-run, the bare invocation is:

```
RELEASE_ID=cliEval
PIPELINE_A_GLOB=".dev/tasks/to-do/TASK-*-${RELEASE_ID}-*/TASK-*-${RELEASE_ID}-*.md"
PIPELINE_B_GLOB=".dev/releases/current/${RELEASE_ID}/tasklist/**/*.md"
OUTPUT_DIR=".dev/releases/current/${RELEASE_ID}/comparison/run-$(date -u +%Y%m%dT%H%M%S)"
mkdir -p "$OUTPUT_DIR"

# Then paste this prompt into Claude Code with the variables substituted.
```

---

# Appendix B — Authoring provenance

- **Recommender:** `/sc:recommend` via `sc:recommend-protocol`
- **Verified commands:** `/sc:adversarial` (15 flags), `/sc:analyze` (3 flags), `/sc:spec-panel` (6 flags — considered but excluded as primary)
- **Verification mechanism:** Step 1 direct read of `src/superclaude/commands/<name>.md` + Step 2 Auggie enrichment (`mcp__auggie-mcp__codebase-retrieval`)
- **Rule compliance:**
  - Rule 1 (No unverified flags): ✅ every flag in Section D's `/sc:adversarial` invocation traces to the verified flag table
  - Rule 2 (No unverified commands): ✅ all three commands resolved via Step 1+2
  - Rule 3 (No protocol reimplementation): ✅ `/sc:adversarial` is invoked, not specified; `/sc:analyze` is invoked, not specified; the rubric is OURS (not a target's protocol)
  - Rule 4 (Built-ins exempt): ✅ `Glob`, `Read`, `Write`, `Agent`, `Skill` used without verification overhead
- **Date authored:** 2026-05-18
- **Reusable across future task-builder-vs-tasklist pipeline comparisons:** yes, with template-variable substitution.
