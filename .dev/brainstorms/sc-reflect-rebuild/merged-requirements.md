---
name: sc:reflect-protocol
description: "Tiered reflection protocol grounded in real code and real citations. UC-1 (pre-execution) validates a proposed strategy/tasklist against its driving spec/PRD for coverage and best-practice compliance. UC-2 (post-execution) audits completed work for 100% adherence and classifies every divergence under a 4-category deviation taxonomy (Authorized expansion / Necessary deviation / Drift / Regression). Tier 1 is a fast single-agent grounded pass; Tier 2 fans out 2-3 heterogeneous reviewer agents on different model classes and merges via sc-adversarial-protocol Mode A; Tier 3 hands off to task-builder for a corrective MDTM remediation. Structural mechanisms — heterogeneous reviewers, blind calibration, mandatory evidence-validator gate — exist specifically to neutralise the representational bias that makes single-agent self-review unreliable."
version: 1.0.0
allowed-tools: Read, Grep, Glob, Bash, TodoWrite, Task, Write, Edit, Skill, mcp__auggie__codebase-retrieval, mcp__serena__find_symbol, mcp__serena__find_referencing_symbols, mcp__serena__get_symbols_overview, mcp__serena__get_diagnostics_for_file, mcp__serena__read_memory, mcp__serena__write_memory, mcp__serena__list_memories, mcp__serena__search_for_pattern, mcp__serena__activate_project, mcp__context7__resolve-library-id, mcp__context7__query-docs, mcp__tavily__tavily-search, mcp__sequential-thinking__sequentialthinking
---

<!-- Provenance: This document was produced by /sc:adversarial via /sc:brainstorm -->
<!-- Base: Variant 2 -->
<!-- Merge date: 2026-05-26T23:02:22Z -->
<!-- Non-base sources incorporated: V1, V3, V4, V5 -->
<!-- unresolved_conflicts: [INV-021_vendor_heterogeneity_v1.1_deferral, INV-023_sufficiency_v1.1_hardening] -->

<!-- Extended metadata (for documentation, not parsed):
category: validation
complexity: advanced
mcp-servers: [serena, auggie, context7, tavily, sequential]
personas: [analyzer, qa, refactorer, architect]
spec: .dev/eval-workspaces/sc-reflect/SPEC.md
supersedes: src/superclaude/commands/reflect.md (legacy think_about_* surface)
-->

# Reflect Protocol

<!-- Source: Base (V2, original) — §1 Purpose & Core Thesis preserved verbatim -->

## 1. Purpose & Core Thesis

Reflection that confirms its own conclusions is worse than no reflection. The legacy `/sc:reflect` surface, built on `think_about_task_adherence` / `think_about_collected_information` / `think_about_whether_you_are_done`, runs the *same* representational stack that produced the work as the auditor of the work. Per Mehta (Towards AI, Mar 2026): "the same representational biases that produced the error are present when it re-evaluates." Single-agent self-review is structurally biased, not merely under-prompted.

This protocol is built around three structural mechanisms that single-model self-reflection cannot supply:

1. **Heterogeneous reviewer ensemble at Tier 2** — reviewers run on different model classes (haiku / sonnet / optional qwen-or-kimi) so per-model representational bias does not stack. Empirical support: HDEE, LLM-TOPLA, Wisdom of Silicon Crowd. The merge judge is *deliberately a different class than every debater* (weak-judge-strong-debaters per Khan ICML 2024 Oral, Kenton NeurIPS 2024).
2. **Blind calibration of every reviewer card** — `confidence-calibrator` re-grades each reviewer's findings without the formation context, so the merged verdict weights *calibrated* scores rather than self-reported ones.
3. **Mandatory evidence-validator gate on the final report** — every `file:line` citation in the merged reflection report is independently re-Read; unfounded citations are *dropped, not downgraded*. A report that ships with no dropped citations is treated as suspicious, not clean.

**Two modes, one protocol.**

- **UC-1 (pre-execution)**: input is a *proposed* tasklist/strategy plus its driving spec/PRD/objectives doc. Output is a coverage matrix, a best-practice compliance grade, and a gap registry — *before* token spend on execution. ROI band: 200-500 tokens to potentially save 5,000-50,000 (mirrors confidence-check economics).
- **UC-2 (post-execution)**: input is completed agent work (commit diff, artifact files, task log) plus the tasklist that drove it. Output is a 100%-completion audit, a per-item deviation classification under the 4-category taxonomy in §10, and a remediation recommendation. This is the durable, high-value mode.

**Hallucination contract.** Every claim in the final report is either (a) **Grounded** — backed by a real `file:line` citation, a real diagnostic output, or a real document section that survives evidence-validator re-Read; or (b) **Inferred** — explicitly tagged `[INFERRED]` with a citation chain that the report admits is non-load-bearing. There is no third bucket. Findings that cannot be tagged either way are *dropped*.

---

<!-- Source: Base (V2, original) — §2 Triggers preserved verbatim -->

## 2. Triggers

This skill is invoked ONLY by the `/sc:reflect` command via `Skill sc:reflect-protocol`. Never invoked directly by users.

Activation conditions on the command side:

- User runs `/sc:reflect <args>` in Claude Code.
- Auto-trigger from `sc:troubleshoot-protocol` Wave 6 Phase B (pre-execution review of task-builder output) and Phase D (post-execution validation of `/task` completion).
- Auto-trigger from `sc:task-protocol` end-of-task hook when configured.

Do NOT invoke this skill directly outside the above paths.

---

## 3. Required Input + Mode Selection

The skill MUST resolve a mode (UC-1 or UC-2) before any wave runs.

### 3.1 Inputs

<!-- Source: Base (V2, original) — input flag enumeration preserved verbatim -->

- `--mode pre | post` — explicit mode (RECOMMENDED for non-interactive callers; eliminates auto-detect ambiguity)
- `--spec <path>` — driving spec/PRD/objectives doc (required for UC-1; recommended for UC-2)
- `--tasklist <path>` — tasklist file (required for UC-2; recommended for UC-1 if a tasklist already exists)
- `--diff <ref-or-path>` — git ref (e.g., `HEAD~1..HEAD`, branch name) or path to a diff file (required for UC-2)
- `--commit-range <ref-range>` — alternative to `--diff` for resolving a post-execution diff via git
- `--scope <path>` — narrowing scope (when resolving to modified files → UC-2 auto-detect)
- `--task-log <path>` — task execution log (optional, UC-2 only)
- `--depth quick | standard | deep` — Tier-1-only / Tier-1-then-rubric / force-Tier-2 (see §5)
- `--tier 1 | 2 | auto` — explicit tier pin (overrides rubric); `auto` is default
- `--reviewers N` — number of Tier 2 reviewers (2-3; default 3, clamped by `--depth`)
- `--output <dir>` — output directory (default `.dev/reflect/<mode>-<slug>-<YYYYMMDDHHMMSS>/`)
- `--coverage-floor <float>` — optional override of the T1 coverage stop floor (default 0.90; high-safety profile may set to 0.95)
- `--no-mcp`, `--no-evidence-validator` (debug only; auto-warns), `--remediate` (offer Tier 3)
- `--budget-remaining <int>` *(P5)* — caller-side budget hint (typically `TurnLedger.available()` from a sprint context). When provided, reflect cross-checks against the §15 cost profile and may auto-degrade tier; emits `budget_forced_tier_downgrade: true` in the contract when this happens. See §4.0 step 0.9.
- **Promotion gate flags (UC-2 only — see §14.5):**
  - `--no-promote` — suppress Wave 7 promotion. Default is *default-on*: when the §14.5.2 strict gate passes, the validated work-unit folder moves to its `done` destination.
  - `--promote-anyway` — override `status: partial` gate condition (all other 7 conditions still apply). No effect on `status: failed`.
  - `--promote-dry-run` — print the `mv` command + gate evaluation; perform no mutation.
  - `--promote-mode auto|task|sprint-release|none` — force a specific promotion adapter or disable selection. Default `auto`.

### 3.2 Mode selection (6-rule first-match order)

<!-- Source: V1 §3 — merged per Change #6 (replaces V2's 4-priority table with V1's 6-ordered-rules first-match) -->

Applied in order, first match wins:

1. **`--mode pre | post`** present → use literal value. STOP if value is anything else.
2. **`--diff` OR `--commit-range`** flag present → **UC-2 (post)**.
3. **`--scope`** resolves to a directory whose tracked files overlap `git diff --name-only HEAD~1..HEAD` → **UC-2 (post)**.
4. Input arguments include both a `--tasklist` file AND a completed-work artifact directory (`.dev/tasks/done/`, `.dev/releases/current/results/`, etc.) → **UC-2 (post)**.
5. `--spec` AND `--tasklist` present with no diff / no done-marker artifacts → **UC-1 (pre)**. If only `--spec` is present → UC-1 with a coverage-only pass.
6. None of the above resolve → **STOP** with: `"Reflect requires --mode pre|post OR a resolvable input combination. See refs/input-resolution.md."`

### 3.3 Hard STOP conditions

<!-- Source: Base (V2, original) — preserved verbatim -->

- Neither `--spec`, `--tasklist`, nor `--diff` provided.
- `--mode pre` with no `--spec` (pre-execution reflection has nothing to reflect against).
- `--mode post` with no `--diff` AND no `--task-log` (post-execution reflection has no completed work to audit).
- `--depth deep` with under-specified input (e.g., 1-line spec, empty tasklist).
- `--output` resolves under `.claude/skills/`, `.claude/agents/`, or `.claude/commands/` (CLAUDE.md ABSOLUTE RULE — distributable paths are not output sinks).

### 3.4 Environment Prerequisites

<!-- Source: V1 R2-A1 + R3 A-002 consensus — merged per Change #14 (env-var fallback Required-Input subsection) -->

The skill resolves model aliases from environment at Wave 0:

- `ANTHROPIC_DEFAULT_OPUS_MODEL`, `ANTHROPIC_DEFAULT_SONNET_MODEL`, `ANTHROPIC_DEFAULT_HAIKU_MODEL`.

Aliases drive Tier 2 reviewer composition (see §7.1 and the alias-routing table in §4 Wave 0). Missing aliases **do not abort the skill**; they degrade reviewer topology per the §4 Wave 0 routing table (0/1/2/3+ alias rows). The skill emits `degraded_components: ["env-aliases"]` into the audit log and surfaces a WARN to the user when running with fewer than 3 distinct classes. The full degraded-mode envelope (env, MCPs, agents) is documented in §14.

---

## 4. Wave / Tier Architecture

<!-- Source: Base (V2, original) — 7-wave structure preserved per Change #21 (irreducible disagreement on wave count resolved at median = V2's 7) -->
<!-- Source: R3 §Top 3 — per-step audit emit added per Change #22 (compensates V1/V4 9-wave audit-budget concern) -->

**Per-step audit emit convention.** Every numbered step within every wave emits one row to `<output>/audit.log` with shape: `{wave: <N>, step: <M>, timestamp: <ISO-8601>, outcome: ok|warn|fail|skip, evidence_ref: <path-or-null>}`. This is the audit-granularity unit that resolves the 9-wave vs 7-wave structural disagreement: each step (not each wave) is the audit row.

```
Wave 0:   Parse + Validate Input + Activate Project + Memory Hydrate
            0.1 Parse flags + apply §3.2 mode-selection
            0.2 Validate input paths (Read existence)
            0.3 Probe sc-adversarial-protocol installation (see §14)
            0.4 Compute input_sha256 snapshot (see §4.0 — Change #10)
            0.5 Resolve env-var aliases + apply 0/1/2/3+ alias routing table (Change #13/#14)
            0.6 Inspect vendor heterogeneity (Change #18 — warn-only)
            0.7 Activate Serena project + memory hydrate
            0.8 Open audit log + machine-readable header
Wave 1:   Tier 1 — Grounded Single-Agent Reflection
            1A. Real-code grounding (auggie + serena symbolic chain)
            1B. Mode-specific evidence gathering (UC-1: coverage map; UC-2: tasklist-vs-diff map)
                — zero-task guard (Change #12); coverage_undefined route (Change #11)
            1C. Single-agent reflection (root-cause-analyst OR self-review)
            1D. Blind calibration (confidence-calibrator) on the Tier 1 card
Wave 2:   Tier-Decision Gate (rubric — §5; tier_decision.yaml audit artifact — §5.4)
Wave 3:   Tier 2 — Parallel Heterogeneous Reviewers (conditional)
            3A. Compose reviewer agent-spec (model + persona rotation)
            3B. Materialize per-reviewer brief packages (Change #7) + spawn N reviewers in parallel via Task
            3C. Per-card blind calibration (confidence-calibrator × N) — disjoint-set rule (Change #16 / §11.3)
            3D. Distill candidate verdicts
Wave 4:   Tier 2 — Adversarial Merge via sc-adversarial-protocol (conditional)
Wave 5:   Synthesis + Evidence-Validator Gate + Report
            5.0 Pre-invocation probe of sc-adversarial (F1/F2/F3 fallback — Change #15)
            5.x Re-read input + verify input_sha256 matches snapshot (Change #10 drift guard)
Wave 6:   Tier 3 — Remediation Handoff (conditional, opt-in)
Wave 7:   Promotion (UC-2 only — §14.5 strict gate; default-on, --no-promote to suppress)
            7.1 Resolve adapter (task | sprint-release | none)
            7.2 Re-verify all 8 gate conditions immediately before mutation
            7.3 Check destination collision rules (§14.5.5)
            7.4 Atomic mv (source → destination)
            7.5 SHA-verify moved tree vs pre-move snapshot
            7.6 Append promotion-log.yaml entry + audit row
            7.7 Update return-contract promotion_* fields
```

Each wave has explicit entry/exit. Refs are loaded on-demand per wave, never pre-loaded.

### 4.0 Wave 0 — Detailed step additions

<!-- Source: R3 INV-001 — merged per Change #10 (input_sha256 snapshot) -->

**Step 0.4 (input_sha256 snapshot).** Compute `input_sha256 = sha256(read(tasklist_path))` (and `sha256(read(spec_path))` when present) and persist both to `<output>/artifacts/input-snapshot.yaml`. Before Wave 5 synthesis, re-read the input and recompute SHA; if it differs, STOP with `input_drift` flag, emit the SHA pair into the return contract, and route to `status: partial`.

<!-- Source: V1 R2-A1 + R3 A-002 + R3 INV-011 — merged per Change #14 and Change #13 (env-var alias resolution + 0/1/2/3+ routing table) -->

**Step 0.5 (env-var alias resolution + 0/1/2/3+ alias routing).** Resolve the three `ANTHROPIC_DEFAULT_*_MODEL` env vars into an alias-set. Apply this routing table to decide Tier 2 reviewer count:

| Aliases resolved | Routing | Telemetry |
|------------------|---------|-----------|
| 0 | T1-only path; WARN "T2 requires ≥1 model class"; degraded | `degraded_components: ["env-aliases"]` |
| 1 | T1-only path; WARN "T2 requires ≥2 model classes" | `t2_diversity: degraded` |
| 2 | T2 with 2 reviewers (degraded) | `t2_diversity: degraded` |
| ≥3 | T2 with 3 reviewers (full diversity) | `t2_diversity: full` |

Grader assertion: `yaml_field` asserts `t2_diversity` is one of `{full, degraded}`.

<!-- Source: R3 INV-021 + Cat-6 Gate 2 — merged per Change #18 (vendor heterogeneity warn-only telemetry) -->

**Step 0.6 (vendor heterogeneity check).** For each resolved alias, extract the vendor (Anthropic / Qwen / Kimi / DeepSeek / OpenAI-compat / etc.) by alias-name heuristic. Emit one of:

- `t2_vendor_diversity: multi` (≥2 vendors among resolved aliases)
- `t2_vendor_diversity: single` (all aliases share one vendor)

When `single`, emit a WARN with the suggested env-var override (full message body lives in `refs/ops-integration.md`). This is **warn-only in v1**; behaviour does not block. See §11.0 (sufficiency-conditional preamble) and the v1.1 deferred-hardening notes in §19.

<!-- Source: P5 (budget-awareness handshake) — caller-side budget pre-flight against §15 cost profile -->

**Step 0.9 (budget pre-flight, P5).** When `--budget-remaining N` is provided, route per this table against the §15 Token Cost Profile (Claude-side band midpoints):

| Budget remaining (N) | Routing | Telemetry |
|---------------------|---------|-----------|
| N < 5 (below `TurnLedger.minimum_allocation`) | **STOP** with explicit message: `"budget too low for reflect — minimum 5 turns"` | `budget_forced_stop: true` |
| 5 ≤ N < T1-midpoint (~6) | Run T1 only with WARN; do NOT escalate to T2 even if rubric requests | `budget_forced_tier_downgrade: true`, `forced_tier: 1` |
| T1-midpoint ≤ N < T2-midpoint (~52) | Allow T1; if rubric escalates to T2 and `N < (T2-midpoint × 1.25)`, downgrade to T1 with WARN | `budget_forced_tier_downgrade: true` *(only if downgrade applied)* |
| N ≥ T2-midpoint × 1.25 | No constraint; run as rubric directs | `budget_forced_tier_downgrade: false` |
| `--budget-remaining` unset | Skip; emit `budget_check_skipped: true` | none |

The 1.25× multiplier on the T2 threshold mirrors the hard-kill rule in §15. This step runs AFTER step 0.5 (env-var alias resolution) — alias-degraded routing takes precedence over budget routing for tier selection, but budget routing can still STOP a degraded T1 path if N < 5.

### 4.1 Wave 1 — Detailed step additions

<!-- Source: R3 INV-005 — merged per Change #12 (zero-task guard) -->

**Step 1B.1 (zero-task guard, UC-1).** Before any coverage-pct computation: if the parsed tasklist contains `total_tasks == 0` and mode is UC-1, STOP with `empty_input` flag and `status: partial`, return `coverage_pct: null` with `coverage_undefined: true` in the contract. Do NOT proceed to T1/T2.

<!-- Source: R3 INV-007 — merged per Change #11 (coverage_undefined route for zero-ID specs) -->

**Step 1B.2 (coverage_undefined route).** If the spec/tasklist parse produces zero requirement IDs (no `T-NNN`, no checklist items, no headings to map), set `coverage_undefined: true`, route directly to T2 (no T1 stop possible), and surface in the report header. `coverage_pct` is not computed. The 0.90 T1 floor cannot pass vacuously (0/0 ≠ PASS).

<!-- Source: P3 (cross-task interaction-effects scan) — central value-add of end-of-tasklist reflect vs N per-task reflects -->

**Step 1B.3 (cross-task interaction-effects scan, UC-2 tasklist-scope only).** When mode is UC-2 AND the tasklist contains ≥3 completed tasks, run the symbol-overlap scan:

1. For each task in the tasklist, derive its touched symbols via `mcp__serena__find_symbol` against the task's diff hunks.
2. Build a symbol-overlap graph: nodes = symbols, edges = "touched by task X and task Y." Cap at top-30 most-touched symbols (heuristic; full enumeration is bounded at 30 to control cost).
3. For each overlap edge, query `mcp__serena__find_referencing_symbols` to determine whether the symbol is genuinely shared or just transiently named the same.
4. For each confirmed interaction, check whether either task description explicitly cites the other (textual match on task ID). If neither cites the other, **flag as a cross-task interaction risk**.
5. Each risk becomes a synthetic invariant probe entry tagged `category: cross_task` (in addition to the existing 6 categories — see §11.2 / R2.5 invariant probe). Severity scales with the symbol's call-site count: HIGH if >5 referencing call sites, MEDIUM if 2-5, LOW if 1.

Emit `interaction_effects_scanned: true` in the contract when this step runs; `interaction_effects_scanned: false` when skipped (tasklist < 3 tasks OR mode == UC-1). This is the differentiating value of end-of-tasklist reflect — per the §1 thesis, single-scope review misses interaction effects, and this is where reflect catches them. Scan-skip transparency matters: a `false` value is a legitimate outcome, not a failure.

### 4.3 Wave 3 — Detailed step addition

<!-- Source: V1 §4 Wave 4 — merged per Change #7 (reviewer-brief packaging) -->

**Step 3B.0 (materialize per-reviewer brief packages).** Before spawning N reviewers, materialize one brief per reviewer at `<output>/reviewer-briefs/reviewer-<N>.md` containing:

- (a) T1 reflection card slice (the section relevant to this reviewer's persona)
- (b) reviewer-scoped grounding hunks (file:line excerpts from Wave 1A)
- (c) coverage-matrix slice (only the rows the reviewer is responsible for)

Each brief is self-contained, so reviewers run truly in parallel without orchestrator round-trips. Brief file shape is testable via the `yaml_field` grader assertion.

### 4.5 Wave 5 — Detailed step addition

<!-- Source: V1 R2-A1 + R3 INV-016 — merged per Change #15 (sc-adversarial F1/F2/F3 fallback + pre-invocation probe) -->

**Step 5.0 (sc-adversarial pre-invocation probe and F1/F2/F3 fallback).** Before calling `Skill sc-adversarial-protocol`, probe its existence via `mcp__serena__list_memories` for the skill's existence indicator OR a no-op `Skill('sc-adversarial-protocol', args='--help')`. If the probe returns `skill not found`:

- **F1**: retry the probe once after a short backoff.
- **F2**: on second probe failure, use the highest-calibrated single Tier 2 reviewer verdict as the fallback merged result; mark `merge_method: single-reviewer-fallback`.
- **F3**: route to Tier 3 only if user explicitly opts in (`--remediate`); otherwise surface `adversarial_unavailable: true` and `status: partial`.

The fallback path is **loud, never silent**: every F-step writes to audit.log; the return contract carries `adversarial_unavailable: true`.

---

## 5. Tier-Decision Rubric (Wave 2)

<!-- Source: Base (V2, original) — V2's priority-rule logic preserved as deterministic spine -->

The rubric routes work to T1 or T2 by combining a calibrated confidence score with three structural signals. Numeric thresholds are concrete and documented; the rubric is the source of truth for escalation.

### 5.1 Hard overrides (no rubric evaluation)

| Override | Result |
|----------|--------|
| `--tier 1` | STOP at T1 (skip Wave 3+) |
| `--tier 2` | ALWAYS escalate to T2 |
| `--depth quick` | STOP at T1 |
| `--depth deep` | ALWAYS escalate to T2 |
| `--no-escalate` | STOP at T1 with warning if confidence < 0.85 |
| `confidence-calibrator` failed AND no inline fallback verdict | STOP at T1, mark `partial`, recommend re-run |

### 5.2 Rubric inputs

From Wave 1D calibration:

- `C` = calibrated confidence (0.00-1.00), arithmetic mean across 5 dimensions per `refs/reflection-rubric.md`
- Five dimensions: **Citation grounding**, **Coverage completeness**, **Deviation-classification clarity**, **Risk surface coverage**, **Recommendation actionability**

Structural signals from Wave 1B:

- `S_scope` — touched-file count from diff (UC-2) or tasklist-item count (UC-1)
- `S_domains` — distinct domains touched (code, infra, docs, tests, config — counted from file paths)
- `S_dev_density` — for UC-2 only: ratio of unmapped diff hunks to total hunks; for UC-1: ratio of unmapped spec requirements to total requirements

### 5.3 Decision logic (applied in order; first match wins)

| # | Condition | Decision |
|---|-----------|----------|
| 1 | `C ≥ 0.90` AND `S_scope ≤ 5 files` AND `S_domains == 1` AND `S_dev_density ≤ 0.05` AND `coverage_pct ≥ <coverage-floor>` AND NOT `coverage_undefined` | **STOP at T1** — high confidence, narrow scope, single domain, near-zero ambiguity |
| 2 | `C ≥ 0.85` AND `S_scope ≤ 10 files` AND `S_domains ≤ 2` AND `S_dev_density ≤ 0.10` | STOP at T1 with WARN if `S_dev_density > 0.05` |
| 3 | UC-2 AND any single hunk classified as `Regression` candidate by Wave 1 | **ESCALATE** (regression must be debated by ≥2 reviewers; structural mechanism, not a confidence question) |
| 4 | `S_domains ≥ 3` | ESCALATE (multi-domain reflection cannot be reliably done by a single reviewer card) |
| 5 | `S_dev_density > 0.20` | ESCALATE (too many unmapped artifacts for a single-pass verdict) |
| 6 | `C < 0.85` | ESCALATE |
| 7 | `--strategy enterprise` set on caller | ESCALATE (enterprise default per sc-brainstorm convention) |
| 8 | Default | STOP at T1 |

Default `<coverage-floor>` is **0.90** per R3 X-001 / C-002 consensus. `--coverage-floor 0.95` is an optional high-safety override.

### 5.4 tier_decision.yaml audit artifact (composite-score recording)

<!-- Source: V5 §3 + R3 C-001 majority-win compromise — merged per Change #9 (5-signal composite recorded as audit artifact) -->

V2's priority-rule logic (§5.3) is the deciding mechanism. V5's 5-signal composite_score is recorded in `<output>/artifacts/tier_decision.yaml` for audit visibility:

```yaml
selected_tier: 1 | 2
fired_rule_number: <int>           # which §5.3 rule fired (deterministic first-match)
composite_score: <float 0-10>      # V5 5-signal sum
per_signal_breakdown:
  scope_size: <0-2>
  task_count: <0-2>
  blast_radius: <0-2>
  spec_density: <0-2>
  ambiguity_signals: <0-2>
escalation_reason: <string>        # human-readable rationale
```

Grader `yaml_field` asserts both `fired_rule_number` and `composite_score` are present. The composite is *recording*, not deciding.

### 5.5 Why these thresholds

- `0.90` for the strict T1 ceiling matches CLAUDE.md global rule 3 (≥90% confidence to proceed without alternatives). Reflection findings that the reviewer is willing to call ≥0.90 *and* narrowly-scoped *and* single-domain are the cases where ensemble verification is not cost-justified.
- `0.85` is the medium-confidence floor inherited from sc-troubleshoot's Wave 2 gate.
- `S_dev_density > 0.20` is the "structural ambiguity" trigger — at one in five unmapped artifacts, a single reviewer cannot adjudicate without ensemble pressure.
- Regression candidacy at rule 3 is non-negotiable because asymmetric cost: shipping a missed regression is far worse than spending T2 tokens debating one.

### 5.6 Escalation reason logging

The matching rule number + numeric values are written to the audit log:

```
escalation_decision:
  tier_reached: 2
  rule_matched: 3
  confidence_calibrated: 0.91
  S_scope: 8
  S_domains: 2
  S_dev_density: 0.07
  regression_candidate_count: 1
  reason: "regression_candidate_requires_debate"
```

---

## 6. Modern Serena Tool Usage

<!-- Source: Base (V2, original) — §6 preserved verbatim; think_about_* policy = mandatory scripted nudges, NOT load-bearing -->

The protocol replaces every `think_about_*` invocation with a concrete symbol-anchored evidence chain. The `think_about_*` triad is *current* (not deprecated per Topic 1 research) but is positioned here as scripted mandatory checkpoints, not the load-bearing reflection mechanism.

### 6.1 Mandatory evidence-gathering chain (Wave 1A)

For every touched file in UC-2, or every spec-referenced module in UC-1:

```
1. mcp__serena__activate_project (once, idempotent at Wave 0)
2. mcp__serena__get_symbols_overview <file>            # structural map
3. mcp__serena__find_symbol <relevant-symbol>          # symbol body
4. mcp__serena__find_referencing_symbols <symbol>      # downstream impact
5. mcp__serena__get_diagnostics_for_file <file>        # LSP-level issues
6. Re-Read each cited file:line range before quoting    # citation-grounding
```

The chain replaces "think_about_collected_information" — instead of asking the model to self-assess whether it has enough info, the protocol *produces* the evidence and lets the rubric score whether grounding is sufficient.

### 6.2 Citation-grounding via re-Read (anti-staleness)

Per CLAUDE.md "Context freshness discipline" S1: before any `file:line` citation enters a draft report, the orchestrator MUST have Read the source file within the last 5 tool calls. The hook layer enforces this at edit time but not for chat citations — the protocol enforces it explicitly by inserting a re-Read step immediately before Wave 5 evidence-validator hands off.

### 6.3 Memory pattern (per-project, expiring)

```
mcp__serena__read_memory  key=reflect/last-pass-{project-slug}      # Wave 0 hydrate
mcp__serena__read_memory  key=reflect/deviation-patterns-{slug}     # Wave 1 (recurring deviation signals)
mcp__serena__write_memory key=reflect/last-pass-{slug} value=<summary>  # Wave 5 persist
mcp__serena__write_memory key=reflect/deviation-patterns-{slug} value=<merged>  # Wave 5 persist
mcp__serena__list_memories                                          # Wave 0 inventory
```

Retention rule: keep last 20 entries per key; expire >90 days. Project slug derived from `pwd` basename.

### 6.4 `think_about_*` as scripted checkpoints (not load-bearing)

Per Topic 1 research, the `think_about_*` tools are cheap meta-cognition prompts. They are wired in as *mandatory scripted nudges*, with their output recorded in the audit log but never used as the load-bearing signal:

| When | Tool | Purpose |
|------|------|---------|
| End of Wave 1A | `think_about_collected_information` | Cheap sanity nudge after evidence-gathering chain — if model surfaces a gap, log it and influence rubric `S_dev_density` upward |
| End of Wave 1C | `think_about_task_adherence` | UC-1 mode only — cheap nudge before calibration |
| End of Wave 5 (after evidence-validator) | `think_about_whether_you_are_done` | Final completion nudge; result logged but does NOT gate ship (evidence-validator gates ship) |

These are scripted, not optional. Their output is captured to `<output>/serena-checkpoints.log` for audit. They are not the reflection — they are a free 200-token nudge layered on top. **They are NOT listed in frontmatter `allowed-tools`** (per R3 C-007 consensus — declaring them as protocol surface would overweight their role).

### 6.5 Fail-open policy

Every Serena call is fail-open per `sc-validate-roadmap-protocol` convention. Missing Serena → fall back to `Grep`/`Glob` with `degraded: true` in the audit. The protocol must never abort because Serena is unavailable.

---

## 7. Agent Delegation Map

<!-- Source: Base (V2, original) — §7 preserved verbatim -->

Every reusable agent is mapped to a wave; no agent is duplicated inline.

| Agent | Wave | Mode | Role | Fallback |
|-------|------|------|------|----------|
| `root-cause-analyst` | 1C | UC-2 | Investigate any deviation candidate found in Wave 1B; produce hypothesis card with `deviation_class` field | Inline orchestrator card |
| `self-review` | 1C | UC-2 (low-stakes) | Cheap 4-question completion pass (tests / edge cases / requirements / rollback) when `S_scope ≤ 3 files` AND `--depth quick` | Inline 4-question template |
| `requirements-analyst` | 1B | UC-1 | Build the spec-to-tasklist coverage map; surface unmapped requirements | Inline orchestrator analysis |
| `confidence-calibrator` | 1D, 3C | both | Blind re-grade per the 5-dim reflection rubric; the dominant anti-anchoring mechanism (calibrator-model ≠ reviewer-model class — see §11.3 disjoint-set rule) | Inline orchestrator calibration with `calibration: inline-fallback` marker |
| `rf-qa` | 3B | UC-2 (structural) | Adversarial-stance structural QA on diff hunks; runs with `fix_authorization: false` (reflection never auto-fixes) | Inline orchestrator pass on `S_scope ≤ 3` |
| `rf-qa-qualitative` | 3B | UC-2 (documents) | Adversarial-stance content-level QA when the artifact under review is a document (PRD, TDD, tech-ref) | Skip; UC-2 still runs with `rf-qa` only |
| `audit-validator` | 5 | UC-2 (large) | When Wave 5 produces ≥20 findings, 10% random spot-check before report ships (lighter alternative to full evidence-validator pass) | Evidence-validator alone (more expensive but stricter) |
| `evidence-validator` | 5 | both | **Non-negotiable final gate**; re-Reads every cited file:line; drops unfounded items | Inline validation with `status: partial` and "validator unavailable" Grounding Gap |
| `task-builder` (skill, not agent) | 6 | UC-2 (post-execution remediation) | Generate corrective MDTM task file from reflection findings | None; surface findings without remediation |
| `socratic-mentor` | 1C | UC-1 (deep) | Optional probing pass for `--depth deep` UC-1 when spec is ambiguous | Skip |

### 7.1 Reviewer composition rules (Wave 3A)

Reviewers are heterogeneous by model class AND by persona, to maximise representational diversity (per Topic 2 research, Wisdom of Silicon Crowd, LLM-TOPLA). Reviewer counts are clamped by the §4 Wave 0 alias-routing table:

| Reviewer count | Model rotation | Persona rotation |
|----------------|----------------|------------------|
| 2 (`--reviewers 2`) | sonnet, haiku | analyzer, qa |
| 3 (default) | sonnet, haiku, (qwen \| kimi \| deepseek if alias available; else opus) | analyzer, qa, refactorer |
| 3 with `--strategy enterprise` | sonnet, haiku, opus | analyzer, qa, architect |

The merge judge in Wave 4 is `sc-adversarial-protocol`'s internal scoring; per Khan et al. ICML 2024 Oral, the judge being a *different* class than the debaters is the right default. The protocol does not pin a judge model — sc-adversarial owns that selection.

### 7.2 No new agents required

The four hypothetical new agents discussed in `enrichment/codebase-context.md` §3.9 (`coverage-mapper`, `deviation-classifier`, `tasklist-vs-diff-comparator`, `reflection-synthesizer`) are *deliberately not introduced* in this variant. Their work is absorbed:

- Coverage-mapping work → `requirements-analyst` agent (UC-1) + inline Wave 1B logic (UC-2).
- Deviation classification → driven by `refs/deviation-taxonomy.md` and applied by `root-cause-analyst` per-card; the taxonomy *is* the classifier.
- Tasklist-vs-diff comparison → inline Wave 1B (`git diff` parse + tasklist parse + bipartite match).
- Reflection synthesis → inline Wave 5 (mirrors sc-troubleshoot's inline Wave 5; new agent introduces bloat without value).

Rationale: keeping the SKILL.md within the sc-troubleshoot/sc-brainstorm band requires keeping inline logic *only* where the inline logic is templated. Where the work is open-ended hypothesis or judgement, agents stay. Where the work is mechanical mapping, inline stays.

---

## 8. Cross-Skill Integration

<!-- Source: Base (V2, original) — §8 preserved verbatim -->

| Skill | When | Why |
|-------|------|-----|
| `sc-adversarial-protocol` (Mode A `--compare`) | Wave 4 (T2 only) | Merge 2-3 reviewer cards into one verdict via the established debate + scoring + merge pipeline. Reflect does NOT re-implement debate. |
| `task-builder` | Wave 6 (T3 only) | Generate corrective MDTM task file from reflection findings; gated on user opt-in. |
| `confidence-check` (skill) | Before any actionable recommendation in Wave 5 chat surface | CLAUDE.md global rule 3 — confidence ≥0.90 to proceed, 70-89% present alternatives, <70% ask. |
| `tech-research` | Wave 1B (optional, `--depth deep` only) | When the spec references frameworks/libraries by name, fetch current best-practice docs (UC-1) or current best-practice patterns to score the implementation against (UC-2). |
| `evidence-validator` (agent, but skill-level dependency) | Wave 5 | Mandatory final gate (see §11.2). |
| `sc-troubleshoot-protocol` | (Reverse direction — sc-troubleshoot invokes us in its Wave 6 Phase B/D) | Pre-exec + post-exec validation of `/task` runs. |

Invocation pattern (all via `Skill <name>`, never `/sc:<command>`):

```
Skill sc-adversarial-protocol with \
  --compare <output>/reviewer-cards/card-1.md,card-2.md,card-3.md \
  --depth standard \
  --focus correctness,coverage,deviation-classification \
  --output <output>/adversarial/
```

Empty-response / partial-parse / missing-file guards apply per `sc-brainstorm-protocol/SKILL.md:280-285` — no synthetic 0.5 fallback; FAIL if response is unparseable or merged_output_path file does not exist on disk. Convergence routing: ≥0.75 PASS, ≥0.60 PARTIAL, <0.60 FAIL (V2 canonical, R3 X-003 consensus 100%).

---

## 9. Output Contract (Versioned)

<!-- Source: Base (V2, original) — §9 spine preserved -->
<!-- Source: V1 §5 — asymmetric_flags union merged per Change #5 -->

Two-block contract: stable + telemetry. Written to `<output>/return-contract.yaml` AND returned inline.

### 9.1 Stable contract (contract_version: 1.0)

```yaml
contract_version: "1.0"
status: success | partial | failed | dry-run
mode: pre | post
tier_reached: 1 | 2 | 3
report_path: <abs path to REPORT.md>
audit_log_path: <abs path>
confidence_calibrated: <float 0.00-1.00>
escalation_rule_matched: <int 1-8> | null

# UC-1 specific
coverage_pct: <float 0.0-1.0> | null
coverage_undefined: <bool>           # true when no parseable requirement IDs (Change #11)
unmapped_requirements: [<list>]
best_practice_grade: <int 0-5> | null

# UC-2 specific
tasklist_completion_pct: <float 0.0-1.0> | null
deviation_count_by_class:
  authorized: <int>
  necessary: <int>
  drift: <int>
  regression: <int>
deviation_register_path: <abs path> | null
grounding_gaps_path: <abs path> | null    # parallel artifact for evidence-insufficient findings (Change #19)

# Input integrity
input_sha256:                         # Change #10
  tasklist: <hex>
  spec: <hex> | null
input_drift_detected: <bool>

# Hallucination guard
citations_total: <int>
citations_dropped: <int>      # >0 forces status: partial
citations_inferred: <int>     # [INFERRED]-tagged; does not force partial
citation_budget_policy: full_reread | sampled    # (Change #8)
evidence_validator_ran: bool

# Tier 2 artifacts
reviewer_cards: [<list of paths>] | []
adversarial_artifacts_dir: <path> | null
adversarial_convergence_score: <float> | null
adversarial_unavailable: <bool>      # F3 path (Change #15)
merge_method: adversarial | single-reviewer-fallback   # F2 path
t2_diversity: full | degraded         # (Change #13)
t2_vendor_diversity: multi | single   # (Change #18, warn-only)
calibrator_diversity: full | degraded # (Change #16)

# Tier 3
remediation_offered: bool
remediation_accepted: bool | null
task_file_path: <path> | null

# Asymmetric-cost flags (V2 base + V1 union — Change #5)
# Downstream automation must respect these.
cannot_validate_without_user_input: bool   # V2 base
regression_present: bool                   # V2 base
unauthorized_deviation_present: bool       # V2 base
blocked_by_low_confidence: bool            # V1 union: every actionable rec gated to <0.70 by confidence-check
spec_is_wrong: bool                        # V1 union: UC-2 — code is correct, spec contradicts on-disk reality
user_decision_required: bool               # V1 union: convergence < threshold AND no auto-route applies
needs_human_decision: bool                 # Change #19: grounding-gaps.yaml non-empty

# Per-task verdict array (P1 + P2) — populated when UC-2 input is a multi-task tasklist
per_task_verdicts:                       # empty list for UC-1 or single-task UC-2
  - task_id: <string>
    status: success | partial | failed
    deviation_class: authorized | necessary | drift | regression | none
    citations_dropped: <int>
    per_task_validation_strength: <float 0.00-1.00>   # P2: calibrated, post-evidence-validator
    evidence_anchor: <abs path or task-log ref>

# Cross-task interaction-effects (P3) — UC-2 tasklist-scope only
interaction_effects_scanned: bool         # true when Wave 1B.3 ran; false when skipped
interaction_effects_findings: <int>       # count of cross_task invariant probe entries (sum of HIGH+MEDIUM+LOW)

# Budget pre-flight (P5)
budget_forced_tier_downgrade: bool        # true when --budget-remaining triggered tier downgrade per §4.0 step 0.9
budget_forced_stop: bool                  # true when --budget-remaining < 5 (below TurnLedger.minimum_allocation)
budget_check_skipped: bool                # true when --budget-remaining was not provided
forced_tier: 1 | 2 | null                 # populated when budget_forced_tier_downgrade == true

# Promotion (UC-2 only — §14.5)
promotion_action: moved | skipped | rejected | failed | already-promoted | dry-run | not-applicable
promotion_adapter: task | sprint-release | none | null
promotion_source: <abs path> | null
promotion_destination: <abs path> | null
promotion_log_path: <abs path> | null      # always set when Wave 7 ran
promotion_gate_passed: bool | null         # null when mode == pre or Wave 7 skipped pre-gate
promotion_skip_reason: user-flag | gate-failed | adapter-unresolved | dry-run | null
promotion_fail_reason: source_disappeared | destination_collision | mv_error | sha_mismatch | null
promotion_override_used: --promote-anyway | null
promotion_rollback_command: <string> | null   # only set on promotion_action: moved
```

Each flag has a one-line semantics description in `refs/return-contract.md`. Contract version is `v1.0`.

### 9.2 Telemetry (non-stable)

```yaml
wave_durations_ms: { wave_0: <ms>, wave_1: <ms>, wave_2: <ms>, ... }
token_usage: { wave_0: <est>, ... }
reviewer_models: [<list>]
reviewer_personas: [<list>]
reviewer_vendors: [<list>]
serena_checkpoints_path: <path>
degraded_components: [<list>]   # e.g. ["auggie", "evidence-validator", "env-aliases"]
fallback_path: null | F1 | F2 | F3
```

---

## 10. Deviation Taxonomy

<!-- Source: Base (V2, original) — §10.1-§10.5 preserved verbatim; §10.6 added per Change #19 -->

Reflection's defining contribution beyond a generic verification protocol is *classifying* every divergence between expected and actual work into a concrete, decision-driving category. The literature gap noted in `research-deep.md` Topic 4.4 is filled here with a **4-category taxonomy** (not 5 — per R3 X-009 / INV-015 resolution, evidence-insufficient findings route to `grounding-gaps.yaml`, see §10.6). The gold-standard reference source for "what was expected" is the **driving spec/tasklist** (the artifact the agent was instructed to fulfil) — not the executor's commit message, which is reviewer-side narrative.

Each category has detection signals, a gold-standard reference, and a default remediation posture.

### 10.1 Authorized expansion

**Definition.** A scope addition that was *explicitly* approved by an authoritative artifact (an updated tasklist, a referenced spec amendment, a PR description with explicit reviewer sign-off, or a directly-cited user instruction in the task log).

**Detection signals.**

- Diff hunk maps to a tasklist item AND that tasklist item was added (not original) AND the addition has a commit/timestamp predating the diff.
- Task log contains explicit "user approved scope expansion to include X" or equivalent.
- Spec doc has a revision-history entry adding the relevant requirement.

**Gold-standard reference.** Updated tasklist file + revision-history of spec + task log explicit-approval lines.

**Default remediation.** None. Document in the report. No tier-3 task.

### 10.2 Necessary deviation

**Definition.** A divergence forced by a technical constraint discovered during execution, documented inline (commit message body, code comment, or task log entry) with a clear rationale, but *not* pre-authorized.

**Detection signals.**

- Diff hunk includes a TODO / NOTE / FIXME explaining why the original plan could not be followed.
- Commit message body (not subject) contains the rationale.
- Task log contains "blocked by X, deviated to Y" entry.
- The deviation does NOT contradict any acceptance criterion in the spec.

**Gold-standard reference.** Inline documentation (comment, commit body, task log) + spec acceptance-criteria check (no contradictions).

**Default remediation.** Surface in report with `Documentation note` recommendation — propose updating the spec/tasklist so future runs match reality. No tier-3 task unless `--remediate-docs` is set.

### 10.3 Drift

**Definition.** A silent change not in the original spec/tasklist with no inline rationale. The work *happened* without explicit authorization and without recorded justification.

**Detection signals.**

- Diff hunk does NOT map to any tasklist item.
- No commit-body rationale, no inline comment, no task-log entry explaining the change.
- Does NOT contradict any acceptance criterion (this is what distinguishes drift from regression).

**Gold-standard reference.** Tasklist coverage map (item is unmapped) + commit-body grep (no rationale found) + inline-comment search (no NOTE/TODO/FIXME explaining).

**Default remediation.** Surface in report with `Authorize-or-revert decision required`. If `--remediate`, offer Tier 3 task to either (a) backfill spec to authorize, or (b) revert the drift.

### 10.4 Regression

**Definition.** A change that *contradicts* an acceptance criterion, an explicit constraint in the spec, or a previously-passing test. The work undoes or violates a documented commitment.

**Detection signals.**

- Diff hunk contradicts a spec acceptance criterion (textual contradiction or behavioral contradiction surfaced by `get_diagnostics_for_file`).
- A test that previously passed now fails after the diff (detect via task log or by re-running tests if `--rerun-tests` set).
- A documented invariant in the spec or in a `@invariant` comment is violated.

**Gold-standard reference.** Spec acceptance-criteria section + test-suite state pre/post (from task log or re-run) + invariant comments.

**Default remediation.** This is the only class that *unconditionally* triggers a Tier 3 remediation offer in Wave 6 when `--remediate` is set. Also unconditionally forces escalation to Tier 2 per §5.3 rule 3 (the regression is debated by ≥2 reviewers before the report ships).

### 10.5 Classification precedence

When multiple signals match, precedence is **Regression > Drift > Necessary > Authorized**. A diff hunk that contradicts a spec criterion but has an inline TODO rationale is still a **Regression** — rationale does not authorise contradiction. A diff hunk with no tasklist mapping AND no rationale AND no contradiction is **Drift**, not Necessary.

### 10.6 Grounding Gaps (parallel artifact for evidence-insufficient findings)

<!-- Source: R3 INV-015 / X-009 — merged per Change #19 (grounding-gaps.yaml parallel artifact) -->

The taxonomy is **4 categories**, not 5. There is no `unknown` deviation class. When a hunk cannot be classified due to **insufficient evidence** (distinct from multi-signal ambiguity), the orchestrator does NOT add it to `deviation-ledger.yaml`. Instead, it writes a row to `<output>/grounding-gaps.yaml` with these **required fields**:

```yaml
- hunk_ref: <file:line-range>
  evidence_missing: <what is missing — e.g., "no commit body, no inline comment, no task-log entry, spec section ambiguous">
  why_not_classifiable: <one-sentence reason>
  next_evidence_needed: <what would resolve — e.g., "ask user whether feature X was authorized">
  owner: user             # default; can be `reviewer` if a reviewer round can resolve
  decision_needed_by_user: true | false
```

When `grounding-gaps.yaml` is non-empty:

- `status: partial` is forced.
- `needs_human_decision: true` is emitted to the return contract.
- The REPORT.md Grounding Gaps section enumerates each row with the missing-evidence rationale.

This is **structurally separate** from the 4-category ledger (V4's `unknown` semantics absorbed as a separate artifact with V4's required-field rigor; V2's Grounding Gap mechanism preserved as the routing target). See §17.7 Kill List for why a 5th deviation category was rejected.

### 10.7 Reporting

Every deviation in REPORT.md is rendered with: file:line, mapped tasklist item (or "unmapped"), spec section (or "n/a"), evidence (verified by evidence-validator), classification rationale (signals matched + gold-standard refs cited), default remediation, and any `[INFERRED]` notes flagged for the reader. Template in `refs/report-template.md`.

---

## 11. Hallucination Guardrails

<!-- Source: R3 INV-023 — sufficiency-conditional preamble added per Change #20 -->

### 11.0 Sufficiency claim is conditional

The protocol's anti-confirmation guarantee — "tier escalation catches self-confirmation bias" — is **CONDITIONAL**, not unconditional. It holds when, and only when, all three of these gates are operative:

1. **calibrator-model ≠ reviewer-model class** (see §11.3 disjoint-set rule, Change #16).
2. **≥2 vendors among reviewer aliases when possible** (see §4 Wave 0 step 0.6 vendor heterogeneity check, Change #18; warn-only in v1).
3. **sycophantic-convergence eval cases pass** (see §12 dimension "tier-escalation-anti-confirmation" + the `T2-convergence-wrong-answer` falsifier case, Change #17).

When any gate degrades, the protocol surfaces `calibrator_diversity: degraded`, `t2_vendor_diversity: single`, or fails the falsifier eval; in those cases the anti-confirmation claim weakens to "ensemble pressure applied" rather than "self-confirmation neutralised." See §19 v1.1 deferred-hardening notes for the path to unconditional sufficiency.

<!-- Source: Base (V2, original) — §11.1-§11.6 preserved with §11.3, §11.5 extensions -->

The protocol exists specifically to *not* confirm its own conclusions. Five structural guards work in concert.

### 11.1 Grounded vs Inferred (the binary)

Every claim in the report carries one of two tags:

- **Grounded** — backed by a real `file:line` citation, a real diagnostic command + output, or a real spec/PRD section that survives evidence-validator re-Read. Default; un-tagged claims are treated as Grounded.
- **`[INFERRED]`** — a claim the reviewer reached without direct citation (e.g., "this pattern is unusual" without pointing at a specific contrary example). Must be tagged explicitly. evidence-validator does not re-Read inferred claims; it counts them and surfaces the count in the report header.

There is no third bucket. Findings the reviewer could not tag either way are *dropped* before Wave 5 synthesis.

### 11.2 Evidence-validator as final gate (non-negotiable)

`evidence-validator` runs in Wave 5 *after* synthesis, *before* the report is surfaced to the user. Its contract (`src/superclaude/agents/evidence-validator.md:21`): "find unfounded citations, not to confirm absence of them. A pass that drops zero items is suspect."

The orchestrator interprets validator output as:

- `0 dropped` → `status: success`, but **audit-log a `zero-drop-flag: true` marker** so meta-eval can spot-check.
- `≥1 dropped` → `status: partial`; the report's "Grounding Gaps" section enumerates dropped citations and the original claim text.
- Validator subprocess crash → fall back to inline citation re-Read, mark `evidence_validator_ran: false`, force `status: partial`.

The `--no-evidence-validator` flag exists for debugging only; using it forces `status: partial` and emits a loud WARN in chat.

### 11.3 Blind calibration (anti-anchoring) — disjoint-set rule

<!-- Source: R3 INV-020 + Cat-6 Gate 1 — merged per Change #16 (calibrator-model ≠ reviewer-model disjoint-set rule) -->

`confidence-calibrator` per `src/superclaude/agents/confidence-calibrator.md` is deliberately stripped of formation context. The card itself is its only input; the upstream investigative trail is not provided. This reduces (does not eliminate) the anchoring bias where the reviewer's own self-reported confidence inflates the next stage's verdict. Calibrated scores, not self-reports, feed the rubric in §5.

**Calibrator-model selection rule (disjoint-set, per ICLR 2025 MAD evidence):**

```
LET reviewer_model_classes = union(reviewer 1..N model class)
LET calibrator_model_class ∈ {opus, sonnet, haiku, qwen, kimi, deepseek} \ reviewer_model_classes
IF disjoint set is non-empty: pick the highest-capability calibrator class from the disjoint set
                              AND emit `calibrator_diversity: full`.
IF disjoint set is empty (all available classes are reviewers):
    use the class with the highest available capability tier NOT used by the most reviewers
    AND emit `calibrator_diversity: degraded`.
```

Telemetry field `calibrator_diversity: full | degraded` is emitted into `reflection-card.yaml`. The §12 eval rubric dimension "calibration discipline" includes the assertion: `calibrator_model_class NOT IN reviewer_model_classes`.

For Tier 2, *every* reviewer card is calibrated by an independent calibrator instance in parallel (Wave 3C). Cards are passed to Wave 4 with calibrated scores attached; sc-adversarial-protocol's debate is weighted by calibrated confidence, not self-reported.

### 11.4 Heterogeneous reviewer ensemble (anti-representational-bias)

Single-model self-review reproduces its own representational bias. Per §7.1, Tier 2 reviewers are heterogeneous by model class. The merge judge is a different class than the debaters (Khan ICML 2024 Oral, Kenton NeurIPS 2024). When the haiku reviewer and the sonnet reviewer agree on a finding, the cross-class agreement is itself evidence that the finding survives at least one representational frame change.

### 11.5 Citation re-Read window (anti-staleness) + budget policy

<!-- Source: V1 §4 Wave 6 citation re-grounding budget — merged per Change #8 -->

Per CLAUDE.md "Context freshness discipline": every `file:line` quoted in the draft report MUST have been Read within the last 5 tool calls before the quote enters context. The orchestrator enforces this explicitly by inserting a final re-Read pass immediately before evidence-validator hands off. Stale citations from earlier waves are re-validated against current file state, not against a possibly-modified mid-wave snapshot.

**Budget policy** (makes the 5-tool-call window practical for large diffs):

- If citations ≤20: re-Read **all** citations.
- If citations >20: sample 100% of HIGH-stakes citations (those tied to `regression`, `security`, or any asymmetric flag) + 30% of remaining citations + 10% audit-validator spot-check on the rest.
- Emit `citation_budget_policy: full_reread | sampled` in telemetry.

### 11.6 Inferred-claim audit

The report header surfaces `citations_inferred: N`. A reviewer that produces a report with `citations_total > 20` AND `citations_inferred > citations_total / 2` triggers an automatic WARN in chat: "Reflection is more inference than evidence. Consider re-running with --depth deep or providing more grounding artifacts." This is a soft signal; the report still ships.

---

## 12. Eval Rubric

<!-- Source: Base (V2, original) — 5-dimension rubric preserved (R3 X-011 majority-win) -->
<!-- Source: V4 §11 — citation_resolves implementation referenced via refs/grader-extensions.md per Change #3 -->
<!-- Source: R3 INV-022 — falsifier eval case T2-convergence-wrong-answer added per Change #17 -->
<!-- Source: R3 INV-021 — T2 vendor heterogeneity eval dimension added per Change #18 -->

Eval workspace: **`.dev/eval-workspaces/sc-reflect/`** (NEVER `.claude/skills/sc-reflect-protocol-workspace/`, per CLAUDE.md plugin override).

Modeled on `.dev/eval-workspaces/sc-brainstorm/`. Same layout: `SPEC.md`, `evals/evals.json`, `iterations/iteration-N/`, `grader.py`, `aggregate_iteration.py`, `skill-snapshot/reflect-v1.md` (frozen baseline = current `src/superclaude/commands/reflect.md`).

### 12.1 Five grading dimensions (0-5 scale per arxiv 2601.03444)

| # | Dimension | Definition | Acceptance threshold |
|---|-----------|------------|----------------------|
| 1 | **Citation accuracy** | % of `file:line` citations that survive an independent re-Read against the on-disk file at eval time | ≥0.95 (T1 + T2); regression below 0.90 fails the iteration |
| 2 | **Coverage completeness** | UC-1: % of spec requirements that appear in the coverage matrix. UC-2: % of tasklist items resolved in the report. | ≥0.90 |
| 3 | **Deviation-classification precision** | % of deviations whose class matches the gold-standard annotation in the eval fixture | T1 ≥0.75, T2 ≥0.85 |
| 4 | **Recommendation actionability** | Each recommendation passes the "file + change + verifier" check: names a file, names a concrete change, names how to verify | ≥0.80 (binary per recommendation, ratio across all) |
| 5 | **False-positive rate** | Findings flagged as Drift/Regression that the gold standard says are Authorized/Necessary | ≤0.10 (T1), ≤0.05 (T2) |

### 12.2 Additional rubric dimensions (sub-criteria, not weighted separately)

The five top-level dimensions absorb three sub-criteria as inline assertions (per R3 X-011 — keep top-level rubric scannable):

- **Tier-routing correctness** (under dim #4 — actionability): eval cases route to expected tier per the §5.3 priority table; `yaml_field` assertion on `tier_decision.yaml`.
- **Calibration discipline** (under dim #1 — citation accuracy, since miscalibration drives bad citations): `calibrator_model_class NOT IN reviewer_model_classes` assertion. Eval cases that fail this auto-fail the iteration (Change #16).
- **Tier-escalation-anti-confirmation** (under dim #5 — false-positive rate, since sycophantic convergence IS the high-cost false positive): includes the `T2-convergence-wrong-answer` case (see §12.5). AUTO-FAIL if `convergence_score ≥ 0.75 AND verdict != regression_present`.
- **T2 vendor heterogeneity** (under dim #4 — actionability, since recommendations from a single-vendor ensemble are at higher risk): graded with `≥2 vendors → +1.0; 1 vendor → 0.5; warn-only`, sourced from `t2_vendor_diversity` telemetry field (Change #18).

### 12.3 Iteration harness

Three pilot evals for iteration-1, expanding to 9-12 for iteration-2 (mirrors sc-brainstorm's expansion pattern):

| ID | Mode | Scope | Notes |
|----|------|-------|-------|
| `pre-trivial-coverage-gap` | UC-1 | tasklist missing 2/8 spec requirements | T1 expected to STOP with `coverage_pct: 0.75` |
| `post-small-diff-clean` | UC-2 | 3-file diff, all tasklist items mapped, no deviations | T1 expected to STOP with `status: success` |
| `post-large-diff-mixed` | UC-2 | 15-file diff with 1 Regression + 2 Drift + 1 Necessary + 1 Authorized | T2 expected (rule 3 + rule 4 + rule 5); merged verdict must classify ≥4/5 correctness |

Convergence rule: ship iteration N when N+1 vs N shows <5% absolute improvement on held-out test set (60/40 split, Anthropic skill-creator default).

### 12.4 Grader DSL extensions

<!-- Source: V4 §11 — extracted to refs/grader-extensions.md per Change #3 -->

`grader.py` from sc-brainstorm provides 8 syntactic types. Reflect adds these **semantic** types, fully implemented (including Python sketch with fixture-root remapping) in `refs/grader-extensions.md`:

- `citation_resolves` — given a file:line citation in the report, re-Read the file and verify the cited snippet matches the actual content at that line (±5 lines); supports fixture-root remapping for synthetic eval diffs.
- `regex_present` / `regex_absent` — pattern presence/absence checks for seeded requirement mentions and false clean-pass detection.
- `yaml_list_contains` — list-field membership check (e.g., `deviation-ledger.yaml deviation_class contains regression`).
- `matrix_covers_items` — verify coverage matrix covers ≥ threshold of source-fixture items.
- `checkpoint_logged` — verify `audit.log` includes a row for a named checkpoint (scripted Serena think-checkpoints, audit-emit per-step).
- `deviation_class_matches` — given an annotated deviation in the eval fixture, verify the report's deviation register tags the same diff hunk with the same class.

All semantic types live in `.dev/eval-workspaces/sc-reflect/grader.py` (copy from sc-brainstorm's `grader.py` and extend per `refs/grader-extensions.md`).

### 12.5 Iteration-3 hardening: falsifier eval case T2-convergence-wrong-answer

<!-- Source: R3 INV-022 — merged per Change #17 (sufficiency-falsifier eval fixture) -->

The iteration-3 hardening fixture lives in `.dev/eval-workspaces/sc-reflect/cases/iteration-3/T2-convergence-wrong-answer/`:

```yaml
id: T2-convergence-wrong-answer
type: held-out adversarial
fixture: fixtures/spec-with-deliberate-misclassification.md
setup: |
  Spec describes a feature requiring authentication.
  Diff implements feature WITHOUT auth (regression).
  Tasklist mentions auth requirement.
  All three reviewers are sonnet-class (seeded ensemble).
  Pre-seed reviewer context with "the implementation looks complete and matches the spec"
  (anchoring all reviewers toward a wrong verdict).
expected:
  tier: 2
  verdict: regression_present (TRUE GROUND TRUTH)
  convergence_score: < 0.75 (PARTIAL or FAIL — they should NOT converge on the wrong answer)
  asymmetric_flags.regression_present: true
assertion: convergence_score < 0.75 OR verdict == regression_present
severity: AUTO-FAIL if convergence ≥ 0.75 AND verdict != regression_present
  (this is the falsifier: high agreement on a wrong call = the sufficiency claim fails)
```

This case is the **sufficiency-claim test** for "tier escalation catches self-confirmation bias." Without it, the central claim is unfalsifiable. It is the operationalisation of §11.0's conditional language.

### 12.6 Grader model

Per Topic 5 research (Arize, Galileo, Evidently): the grader runs on a *different, more capable* model class than the skill-under-test. Default grader: `opus`. The grader is NOT one of the Tier 2 reviewer models, to avoid self-enhancement bias.

For final ship-acceptance, an optional 3-model LLM jury (opus + sonnet + qwen) aggregated by majority across the 5 dimensions. Activated by `--jury` on the eval runner.

---

## 13. Build Path Decision

<!-- Source: Base (V2, original) — §13 preserved verbatim (hybrid pick consensus 100%) -->

**Pick: hybrid — skill-creator plugin for the draft/iterate loop, then local `grader.py` for deterministic assertions, then sprint CLI only after the skill ships.**

### 13.1 Rationale

Three concrete forces shape the pick:

1. **Eval-driven nature of the skill.** Reflection quality is judged by graders running on representative inputs; this is precisely what skill-creator 2.0 ships out of the box (`run_loop.py`, `eval-viewer/generate_review.py`, comparator/grader/analyzer sub-agents). Building the iteration harness from scratch with `superclaude sprint` would duplicate machinery skill-creator already provides.
2. **Cross-model verification.** Tier 2 needs to call heterogeneous models in parallel. Sprint CLI's `executor.py` is built for single-Claude-subprocess sprint execution against a tasklist; it is not optimised for parallel multi-model fan-out within one wave. Skill-creator's parallel sub-agent pattern fits the actual workload better.
3. **CLAUDE.md plugin-override on workspace location.** The skill-creator plugin defaults to `.claude/skills/<name>-workspace/`; the project overrides this to `.dev/eval-workspaces/<name>/`. The override is hook-enforced and gitignored; the override means we can use skill-creator's workflow without inheriting its workspace-location footgun.

### 13.2 Sequenced build

| Phase | Tool | Output |
|-------|------|--------|
| Draft v1 SKILL.md + refs/ + agent map | Hand-authored under `src/superclaude/skills/sc-reflect-protocol/` | Initial protocol |
| Iteration 1 (3 pilot evals) | `skill-creator run_loop.py` against `.dev/eval-workspaces/sc-reflect/` | First eval gate; HTML review via `eval-viewer/generate_review.py` |
| Deterministic assertion gate | Local `grader.py` (copy from sc-brainstorm; extend per `refs/grader-extensions.md`) | Per-iteration `grading.json` |
| Iteration 2 (9-12 evals) | Same harness, expanded matrix | Convergence check; ship at <5% improvement |
| Iteration 3 (hardening) | Same harness + `T2-convergence-wrong-answer` falsifier (§12.5) | Final pre-ship gate |
| Production execution | `superclaude sprint run` against tasklists that *use* sc-reflect | Only after skill ships and is stable |
| Real-process eval at scale | `superclaude eval ...` with PTY isolation | Optional, defer until pilot reflect runs are producing reliable artifact shapes |

`superclaude sprint` is *not* the build path; it is the *execution* path for skills already built. Conflating the two is the trap.

### 13.3 What is NOT used

- Sprint CLI for the build loop (wrong shape).
- `superclaude eval ...` for v1 (overkill until artifacts stabilise).
- Skill-creator's default sibling-workspace path (forbidden by project hook).

---

## 14. Error Handling Matrix

<!-- Source: Base (V2, original) — §14 preserved + Change #15 (F1/F2/F3 rows) added -->

| Scenario | Behavior | Fallback |
|----------|----------|----------|
| No `--mode` AND no resolvable input combination | STOP at Wave 0 with usage hint | None |
| `--mode pre` with no `--spec` | STOP | None |
| `--mode post` with no `--diff` AND no `--task-log` | STOP | None |
| `--output` under `.claude/skills`/`.claude/agents`/`.claude/commands` | STOP (CLAUDE.md ABSOLUTE RULE violation) | None |
| `sc-adversarial-protocol` skill missing (probe fails) | F3: surface `adversarial_unavailable: true`, fall back to single-reviewer highest-confidence verdict, Tier 3 only if user opts in (Change #15) | F2/F3 paths |
| `sc-adversarial-protocol` returns empty | F1: retry once with reduced depth (Change #15) | F2 if retry fails |
| `sc-adversarial-protocol` partial-parse / missing-file | F2: single-reviewer highest-confidence verdict; `merge_method: single-reviewer-fallback` | F3 |
| `task-builder` skill missing in Tier 3 | Surface findings without remediation; do NOT silently downgrade | None |
| `confidence-calibrator` agent fails | Inline orchestrator calibration; mark `calibration: inline-fallback` in audit | Continue |
| `evidence-validator` agent fails | Inline citation re-Read; force `status: partial`; add Grounding Gap entry | Continue |
| `root-cause-analyst` agent fails in Wave 1C | Inline orchestrator hypothesis card; mark `hypothesis_source: inline-fallback` | Continue |
| `rf-qa` / `rf-qa-qualitative` fails in Wave 3 | Continue with remaining reviewers; if <2 reviewers complete, downgrade to T1 result with WARN | None |
| All Tier 2 reviewers fail | Downgrade to T1 result; `status: partial`; recommend re-run | None |
| `merged_output_path` from sc-adversarial does not exist on disk | FAIL Wave 4 (missing-file guard before status routing) | F2 |
| `input_drift` detected (Change #10) — input SHA changed mid-run | STOP at Wave 5 pre-synthesis; emit SHA pair; `status: partial` | None |
| `empty_input` — zero-task tasklist in UC-1 (Change #12) | STOP at Wave 1; `coverage_undefined: true`; `status: partial` | None |
| `coverage_undefined` — zero parseable IDs (Change #11) | Route directly to T2; no T1 stop possible; surface in report header | Continue |
| Zero env-var aliases resolved (Change #13/#14) | T1-only path; WARN; `degraded_components: ["env-aliases"]` | None |
| 1 env-var alias resolved (Change #13) | T1-only path; WARN "T2 requires ≥2 model classes" | None |
| 2 env-var aliases resolved (Change #13) | T2 with 2 reviewers; `t2_diversity: degraded` | Continue |
| Single-vendor T2 ensemble (Change #18) | Continue; WARN; `t2_vendor_diversity: single` (warn-only) | None |
| Calibrator class collides with all reviewer classes (Change #16) | Continue with highest-cap calibrator not used by most reviewers; `calibrator_diversity: degraded` | None |
| Auggie unavailable | Fall back to Grep/Glob in Wave 1A; mark `degraded: ["auggie"]` | Continue |
| Serena unavailable | Fall back to Grep/Glob; skip `get_diagnostics_for_file`; mark `degraded: ["serena"]` | Continue |
| Context7 unavailable in `--depth deep` UC-1 | Skip best-practice external lookup; mark `degraded: ["context7"]` | Continue |
| `--no-mcp` set | Run with native tools only; WARN that quality is degraded | None |
| `think_about_*` Serena tools unavailable | Skip the scripted checkpoint; emit `checkpoint_logged: skipped` row; not load-bearing so OK | Continue |
| Token budget exceeded mid-Wave-3 | Hard abort at 1.25× estimate; preserve partial state for `--resume-from` | None |
| User declines Tier 3 remediation offer | Return success; report stands | None |
| `--depth deep` on under-specified input (≤10 words spec/diff) | STOP at Wave 0; ask user to add detail | None |
| Topic / spec contains adversarial-flag-like chars | Sanitize before passing to sc-adversarial (per sc-brainstorm Wave 2B pattern) | Continue |
| Output dir collision | Append `-N` suffix, cap at 99 with STOP, WARN at N≥10 | None |
| PreToolUse hook blocks write to `.claude/skills/*-workspace/**` | Redirect to `.dev/eval-workspaces/sc-reflect/`; never bypass the hook | None |
| `--budget-remaining N` with N < 5 (P5) | STOP at Wave 0 step 0.9 with `"budget too low for reflect"`; emit `budget_forced_stop: true` | None |
| `--budget-remaining N` triggers tier downgrade (P5) | Run T1 only; emit `budget_forced_tier_downgrade: true`, `forced_tier: 1`; WARN | Continue with T1 only |
| Wave 1B.3 cross-task interaction scan exceeds top-30 symbol cap (P3) | Truncate scan at 30; emit `interaction_effects_truncated: true` in audit; symbols beyond cap not analyzed | Continue with truncated scan |
| Wave 1B.3 `find_referencing_symbols` fails for one or more symbols (P3) | Skip just that symbol; record per-symbol skip in audit; do NOT abort entire scan | Continue |
| Wave 7 source path no longer exists (external mutation) | `promotion_action: failed`, `promotion_fail_reason: source_disappeared`; verdict unaffected | None |
| Wave 7 destination collision, non-identical content (§14.5.5) | `promotion_action: rejected`; diff captured in promotion-log; source untouched | None |
| Wave 7 destination collision, identical content (idempotent re-run) | `promotion_action: already-promoted`; remove source after second SHA verification | None |
| Wave 7 SHA mismatch after move | `promotion_action: failed`, `promotion_fail_reason: sha_mismatch`; attempt inverse `mv` to restore source | None |
| Wave 7 adapter resolution ambiguous OR neither matches | `promotion_action: skipped`, `promotion_skip_reason: adapter-unresolved` | None |
| Wave 7 strict gate fails | `promotion_action: skipped`, `promotion_skip_reason: gate-failed`; gate_evaluation table shows which condition failed | None |
| Wave 7 `--no-promote` set | `promotion_action: skipped`, `promotion_skip_reason: user-flag` | None |
| Wave 7 `--promote-anyway` used on `status: failed` | Override has NO effect; promotion still skipped with gate-failed | None |
| Wave 7 cross-filesystem mv required | Allowed via copy + remove + fsync; emit `cross_fs_promotion: true`; SHA-verify after copy | None |

---

## 14.5 Post-Verdict Promotion (UC-2 only — Wave 7)

<!-- Source: User directive (2026-05-27) — connect /sc:reflect to /task pipeline (task-builder + task) as final QA gate and to sprint CLI release pipeline. -->

Reflect is the **final QA gate** between the executor and the archive. When UC-2 verification passes strictly, the validated work-unit folder moves from its in-progress location to its completed location, closing the loop with `/task-builder` → `/task` → `/sc:reflect` → archive and the analogous loop for `superclaude sprint run`.

### 14.5.1 Two registered promotion adapters (v1.0)

| Adapter | Source path glob | Destination path | Trigger signal |
|---------|------------------|------------------|----------------|
| `task` | `.dev/tasks/to-do/TASK-*` | `.dev/tasks/done/TASK-*` | `--tasklist` resolves under `.dev/tasks/to-do/<TASK-DIR>/` AND tasklist frontmatter has a `status` field |
| `sprint-release` | `.dev/releases/current/<release>/` | `.dev/releases/complete/<release>/` | `--scope` or `--tasklist` resolves under `.dev/releases/current/<release>/` |

Adapter selection is deterministic from the resolved input path; if both apply or neither applies, promotion is suppressed (`promotion_action: skipped`, reason logged). Full adapter table lives in `refs/promotion-adapters.md` (load-on-demand at Wave 7).

### 14.5.2 Default-on with strict 8-condition gate

Promotion fires only when ALL of the following hold:

1. **`mode == post`** — UC-1 has no completed work to promote.
2. **`status == success`** — `partial` or `failed` blocks promotion. (Conditional-CONVERGED per §11.0 is NOT eligible.)
3. **`tasklist_completion_pct == 1.0`** — every checklist item independently verified done by reflect (not just frontmatter-declared).
4. **Frontmatter agrees with reflect's verdict** — the tasklist file's own `status`/`completion` frontmatter MUST declare done. Disagreement is Drift (§10.3) AND a hard promotion blocker.
5. **`deviation_count_by_class.drift == 0` AND `deviation_count_by_class.regression == 0`** — Authorized expansion and Necessary deviation are non-blocking; Drift and Regression block.
6. **`citations_dropped == 0` AND `grounding_gaps_path == null/empty`** — evidence-validator gate clean.
7. **`input_drift_detected == false`** — input SHA stable across the run (§4.0 Step 0.4).
8. **`needs_human_decision == false` AND `user_decision_required == false`** — no flagged ambiguity.

When all 8 hold and `--no-promote` is unset, Wave 7 executes. When 1, 3-8 hold but `status == partial`, `--promote-anyway` can override (still subject to 1, 3-8).

### 14.5.3 Wave 7 — execution

```
Wave 7:   Promotion (UC-2 only, conditional on §14.5.2 gate)
            7.1 Resolve adapter (task | sprint-release | none) from source path
            7.2 Re-verify all 8 gate conditions immediately before mutation
            7.3 Re-verify destination collision rules (§14.5.5)
            7.4 Perform atomic move (§14.5.5 mechanics)
            7.5 Re-Read moved files and verify SHA invariance vs pre-move
            7.6 Append promotion-log entry + audit.log row
            7.7 Update return-contract.yaml promotion_* fields
```

The mutation step (7.4) is the only filesystem write reflect performs outside `<output>/`. Every other wave reads from the repo and writes only to the reflect output dir.

### 14.5.4 Override flags

| Flag | Default | Effect |
|------|---------|--------|
| `--no-promote` | unset | Suppress Wave 7 entirely; `promotion_action: skipped`, `promotion_skip_reason: user-flag`. |
| `--promote-anyway` | unset | Override gate condition 2 for `status: partial`. **Conditions 1, 3-8 still apply.** No effect on `status: failed`. |
| `--promote-dry-run` | unset | Print the exact `mv` command + gate evaluation; perform no mutation. |
| `--promote-mode <auto\|task\|sprint-release\|none>` | `auto` | Force a specific adapter or disable selection. |

### 14.5.5 Mutation mechanics + collision rules

**Atomic move.** Use `mv <source> <destination>` (POSIX rename when same filesystem; copy + remove + fsync if cross-fs). NOT `rsync` (non-atomic).

**Destination collision rules.**

| Condition | Behavior |
|-----------|----------|
| Destination does not exist | Proceed |
| Destination exists, empty dir | Remove empty destination, then move (audit-logged) |
| Destination exists, non-empty, differs from source | STOP: `promotion_action: rejected`, `destination_collision`; diff captured. Do NOT auto-suffix or overwrite. |
| Destination exists, non-empty, identical to source | Idempotent: `promotion_action: already-promoted`; remove source after second SHA verification |
| Source path no longer exists at Wave 7.4 | FAIL: `promotion_action: failed`, `source_disappeared` |
| Destination parent dir missing | Create parent; emit audit row |

**Rollback.** Every promotion-log entry includes the inverse `mv` command. Reflect itself never auto-rolls-back (deferred to v1.1 — see §19).

**Git status.** Reflect does NOT `git add` moved files. Operator stages and commits.

### 14.5.6 Output: `promotion-log.yaml`

Written every time Wave 7 runs (even on reject/skip/dry-run):

```yaml
promotion_log_version: "1.0"
adapter: task | sprint-release | none
mode: auto | forced-task | forced-sprint-release | forced-none
action: moved | skipped | rejected | failed | already-promoted | dry-run
source: <abs path>
destination: <abs path> | null
source_sha256_before: <hex>        # tree-hash via find + xargs sha256sum, sorted
source_sha256_after_move: <hex>    # only on action=moved
sha_match: true | false | null
gate_evaluation:
  mode_post: pass | fail
  status_success: pass | fail
  tasklist_completion_pct_1_0: pass | fail
  frontmatter_agrees: pass | fail
  no_drift_no_regression: pass | fail
  no_citations_dropped: pass | fail
  no_grounding_gaps: pass | fail
  no_input_drift: pass | fail
  no_user_decision_pending: pass | fail
gate_passed: bool
skip_reason: user-flag | gate-failed | adapter-unresolved | dry-run | null
fail_reason: source_disappeared | destination_collision | mv_error | sha_mismatch | null
override_used: --promote-anyway | null
rollback_command: "mv <destination> <source>"   # only on action=moved
timestamp: <ISO-8601>
```

### 14.5.7 Acceptance assertions (eval-workspace)

Wired into `.dev/eval-workspaces/sc-reflect/evals/`:

- **promotion-task-strict-pass**: complete `.dev/tasks/to-do/TASK-EVAL-001/`, all 8 gates pass → `action: moved`, destination exists, source removed.
- **promotion-blocked-by-drift**: 1 Drift entry → `action: rejected`, `no_drift_no_regression: fail`.
- **promotion-blocked-by-frontmatter-mismatch**: reflect verifies done but frontmatter says `in-progress` → `action: rejected`, `frontmatter_agrees: fail`, Drift entry logged.
- **promotion-sprint-release-pass**: `.dev/releases/current/release-X/results/` → destination is `.dev/releases/complete/release-X/`, parent created.
- **promotion-collision-non-identical**: differing destination → `action: rejected`, source untouched, diff captured.
- **promotion-collision-identical**: idempotent re-run → `action: already-promoted`, source removed.
- **promotion-no-promote-flag**: `--no-promote` → `action: skipped`, `skip_reason: user-flag`.
- **promotion-promote-anyway-on-partial**: `status: partial` + `--promote-anyway` → `action: moved`, `override_used: --promote-anyway`.
- **promotion-dry-run**: `--promote-dry-run` → `action: dry-run`, no mutation, mv command printed.

New grader assertion types required (in addition to the 8 inherited): `path_exists` and `path_does_not_exist`. Both are short Python additions to `grader.py` per §17.5.

### 14.5.8 Interaction with §10 Deviation Taxonomy

Frontmatter-vs-verdict mismatch (gate condition 4) is a first-class **Drift** signal in §10.3 — the gate just consumes it. Reflect's independent verification is canonical; tasklist frontmatter is a *claim* that must agree. Disagreement is executor-side Drift, recorded in the deviation register regardless of promotion outcome.

---

## 15. Token Cost Profile

<!-- Source: Base (V2, original) — §15 preserved verbatim -->

| Path | Auggie (offloaded) | Claude (orchestration + agents) | Wall clock |
|------|-------------------|---------------------------------|------------|
| T1 only | ~2-5k | ~3-8k | 1-3 min |
| T2 (2-3 reviewers + adversarial debate) | ~10-25k | ~35-70k | 8-15 min |
| T3 added | +0 | +20-40k | +5-10 min |

Targets, not caps. Hard kill at 1.25× estimate per sc-brainstorm convention.

---

## 16. Refs (loaded on-demand per wave)

<!-- Source: Base (V2, original) §16 — extended with 2 new refs per Change #1 (ops-integration.md) and Change #3 (grader-extensions.md) -->

| File | Wave | Purpose |
|------|------|---------|
| `refs/input-resolution.md` | Wave 0 | Mode auto-detection rules, STOP conditions, slug generation |
| `refs/reflection-rubric.md` | Wave 1D, Wave 3C | 5-dimension calibration rubric (Citation grounding, Coverage completeness, Deviation-classification clarity, Risk surface coverage, Recommendation actionability) |
| `refs/deviation-taxonomy.md` | Wave 1B (UC-2), Wave 5 | The 4-category taxonomy with detection signals, gold-standard refs, default remediations |
| `refs/coverage-mapping.md` | Wave 1B (UC-1) | Spec-to-tasklist coverage map algorithm; bipartite matching heuristics; `S_dev_density` calculation |
| `refs/reviewer-spec.md` | Wave 3A | Model + persona rotation rules; reviewer card template |
| `refs/report-template.md` | Wave 5 | Final REPORT.md skeleton with Grounded vs [INFERRED] tagging conventions. **(P4) MANDATORY**: when `per_task_verdicts` length ≥ 2, the template emits a `## Per-Task Verdicts` section with one subsection per task (verdict block + deviation attribution + evidence anchor). Lifted directly from the contract array; no separate computation. |
| `refs/remediation-handoff.md` | Wave 6 | Task-builder BUILD_REQUEST template; opt-in prompt |
| `refs/ops-integration.md` | (build-time) | Makefile targets (`make sync-dev`, `make verify-sync`, `make reflect-eval`), CI cadence, PreToolUse hook redirect message body, vendor-heterogeneity WARN body (per §4 Wave 0 step 0.6) |
| `refs/grader-extensions.md` | (eval-time) | Python implementation sketch for `citation_resolves` with fixture-root remapping + the 6 grader DSL semantic types + new `path_exists` / `path_does_not_exist` assertion types (per §14.5.7) |
| `refs/promotion-adapters.md` | Wave 7 | Full adapter table (`task`, `sprint-release`, operator-added); collision-rule mechanics body; `mv` invocation template; rollback command template (per §14.5) |
| `refs/cost-profile.yaml` | (pre-invocation) | **(P7)** Static, machine-readable mirror of the §15 Token Cost Profile table. Callers (sprint TurnLedger, CI) read this BEFORE invoking reflect to pre-flight budget. Reflect itself never reads this at runtime — the file is for caller-side discovery only. Updated in lockstep with §15 by a `make sync-cost-profile` target (see `refs/ops-integration.md`). |

Refs loaded by the wave that needs them; never pre-loaded. Session-start footprint: SKILL.md only (~50 tokens via Claude Code skill loader).

---

## 17. Boundaries

<!-- Source: Base (V2, original) — §17 Will / Will Not preserved verbatim -->

### Will

- Run T1 always; respect "quick first" contract.
- Auto-escalate to T2 only when the rubric in §5 says so, or when `--tier 2`/`--depth deep` is set.
- Fan out heterogeneous reviewers (different model classes) in Tier 2 to break representational-bias self-confirmation.
- Use modern Serena symbolic chain (`get_symbols_overview` → `find_symbol` → `find_referencing_symbols`) for evidence; wire `think_about_*` as scripted nudges captured to audit, never as the gating signal.
- Run `evidence-validator` as a non-negotiable final gate before any report ships; treat a zero-drop pass as a flag, not a clean signal.
- Classify every UC-2 deviation under the 4-category taxonomy in §10 with explicit detection signals and gold-standard references.
- Route evidence-insufficient findings to `grounding-gaps.yaml` (§10.6), NOT to a 5th deviation category.
- Tag every claim as Grounded or `[INFERRED]`; drop claims that fit neither bucket.
- Respect CLAUDE.md ABSOLUTE RULES: source-of-truth is `src/superclaude/`, never commit `.claude/` mirrors, PR target is fork only.
- Fail-open on missing MCPs (auggie, serena, context7, tavily) — fall back to native tools and mark degraded.
- Persist deviation patterns to per-project Serena memory with 90-day expiry.
- Delegate debate / scoring / merge to `sc-adversarial-protocol`; never re-implement.
- **Promote validated work-units** (UC-2 only, Wave 7) via the §14.5 strict 8-condition gate: move `.dev/tasks/to-do/TASK-*` → `.dev/tasks/done/TASK-*` and `.dev/releases/current/<release>/` → `.dev/releases/complete/<release>/` when the gate passes. Default-on, `--no-promote` to suppress. Atomic `mv`, SHA-verified, rollback command preserved in promotion-log.
- Write a `promotion-log.yaml` every time Wave 7 runs (even on skip/reject/fail/dry-run) for forensic transparency.
- Refuse promotion on destination-collision with non-identical content (no auto-suffix, no overwrite); record the diff for human resolution.
- **Emit per-task verdicts** (P1+P2) in the contract when UC-2 input is a multi-task tasklist, including `per_task_validation_strength` (calibrated 0.0-1.0) suitable for downstream credit-allocation logic.
- **Scan for cross-task interaction effects** (P3) in Wave 1B.3 when UC-2 tasklist has ≥3 tasks — the differentiating value of end-of-tasklist reflect vs N per-task reflects.
- **Honor caller-side budget hints** (P5) via `--budget-remaining` and auto-degrade tier per §4.0 step 0.9.
- **Publish a static cost-profile ref** (P7) at `refs/cost-profile.yaml` so callers can pre-flight check before invoking.

### Will Not

- Run reflection on its own intermediate output without explicit `--recursive` flag and a token-budget envelope (prevents unbounded sub-skill recursion).
- Trust agent-reported self-confidence; always re-grade via `confidence-calibrator` (or inline fallback).
- Ship a report whose `file:line` citations have not passed through `evidence-validator` (or the inline fallback with `status: partial` marker).
- Auto-execute a Tier 3 remediation task — task-builder produces a file, the user runs `/task <path>`.
- Auto-commit after Tier 3.
- Silently downgrade missing skills (sc-adversarial, task-builder) — STOP with explicit install instruction (per sc-brainstorm Wave 0 pattern).
- Treat the executor's commit message as the gold-standard reference for "what was expected" — that is reviewer-side narrative, not spec.
- Skip the heterogeneous-model requirement at Tier 2 — 3× the same model class defeats the purpose of escalation.
- Confirm its own conclusions: a zero-drop evidence-validator pass on a non-trivial report is an audit flag, not a green light.
- Use the `think_about_*` triad as load-bearing — they are nudges, not evidence.
- Operate against `.claude/{skills,commands,agents}/*` paths as output sinks (CLAUDE.md ABSOLUTE RULE).
- **Auto-promote a `status: partial` or `status: failed` run** without `--promote-anyway` (and `--promote-anyway` has no effect on `status: failed`). Drift, Regression, citation drops, or grounding gaps hard-block promotion.
- **Promote without verifying frontmatter agreement.** Tasklist frontmatter `status: done` is a claim that must agree with reflect's independent verification.
- **Auto-overwrite or auto-suffix on destination collision.** Identical content = idempotent re-promotion; differing content = hard reject with diff capture.
- **Auto-roll back a successful promotion.** Rollback is operator-driven via the inverse `mv` command preserved in promotion-log. Auto-rollback is v1.1 scope (§19).
- **`git add` after promotion.** Filesystem-level move only; the operator stages and commits.
- **Emit `tasklist_aggregate` enum** (rejected P1 sub-proposal — adversary correctly identified it as redundant with `status` + `deviation_count_by_class`). Downstream computes the gestalt from existing fields.
- **Emit a separate top-level `validation_strength` field** (rejected P2 split — folded into `per_task_verdicts[].per_task_validation_strength` to avoid duplication with `confidence_calibrated`).
- **Stream per-task verdicts as they're emitted** (deferred P6 — see §19.4). Batch-emit at end of run is sufficient for v1.0.
- **Maintain cross-tasklist deviation-pattern memory** (deferred P8 — see §19.5). Existing per-project memory namespace is sufficient for v1.0.
- **Apply caller-side credit policy** (P5/P7 scope boundary). Reflect publishes calibrated numbers (`per_task_validation_strength`) and cost estimates (`refs/cost-profile.yaml`); the caller's ledger owns the credit-allocation arithmetic. Reflect never returns a turn-credit amount.

---

## 17.5 Ops Integration

<!-- Source: V5 §9 — merged per Change #1 (heavy ops content extracted to refs/ops-integration.md; ~30 lines kept inline) -->

This section codifies the build/CI/hook discipline that surrounds the skill. Detailed Makefile target tables, full CI cadence, and the full vendor-heterogeneity WARN body live in `refs/ops-integration.md` (load on-demand at build time).

**The `-f` rule (CLAUDE.md ABSOLUTE).** If `git add` requires `-f` on any `.claude/` path (except `.claude/settings.json`), that `-f` is the violation siren. STOP. Move the change to `src/superclaude/`, run `make sync-dev`, stage only the `src/` side. See memory `feedback_claude_dir_gitignored.md`.

**PreToolUse hook awareness.** The `.claude/settings.json` PreToolUse hook rejects writes to `.claude/skills/*-workspace/**` with a redirect to `.dev/eval-workspaces/<skill-name>/`. This skill's eval workspace MUST land at `.dev/eval-workspaces/sc-reflect/` to pass the hook. The `.gitignore` also matches `.claude/skills/*-workspace/`, so any misplaced workspace cannot be committed.

**`make sync-dev` / `make verify-sync` pre-commit workflow.**

1. Edit `src/superclaude/skills/sc-reflect-protocol/SKILL.md` (and/or `src/superclaude/commands/reflect.md`).
2. Run `make sync-dev` to mirror to `.claude/`.
3. Run `make verify-sync` — must exit 0 (the pre-commit hook also runs this).
4. Run `make lint-architecture` to confirm bidirectional command↔skill link + frontmatter completeness.
5. Stage ONLY `src/` and `.dev/` paths. NEVER stage `.claude/` paths.

**CI cadence.** Run `make reflect-eval-quick` (3 pilot cases, <30s) on every PR touching `src/superclaude/skills/sc-reflect-protocol/` or `src/superclaude/commands/reflect.md`. Full `make reflect-eval` (~2 min) runs on release-candidate branches. See `refs/ops-integration.md` for the full Makefile target table (`make sync-dev`, `make verify-sync`, `make lint`, `make lint-architecture`, `make test`, `make reflect-eval`, `make reflect-eval-quick`, `make eval-skill SKILL=sc-reflect-protocol`).

---

## 17.6 Testability Map

<!-- Source: V4 §16 — merged per Change #2 (testability map as protocol-decision-to-eval-assertion manifest) -->

Every load-bearing protocol decision maps to at least one deterministic or qualitative eval assertion. Rows where no mapping is feasible should be simplified or removed.

| Protocol decision | Eval assertion type | Target artifact / field |
|-------------------|---------------------|-------------------------|
| Output-dir guard rejects `.claude/{skills,commands,agents}/` | `regex_absent` in audit + STOP fixture | `audit.log` |
| §3.2 mode auto-detection (6-rule first-match) | `yaml_field` | `return-contract.yaml mode` |
| §4 Wave 0 input_sha256 snapshot (Change #10) | `yaml_field` | `input-snapshot.yaml input_sha256.tasklist` |
| §4 Wave 0 input_drift guard (Change #10) | `yaml_field` | `return-contract.yaml input_drift_detected` |
| §4 Wave 0 alias-routing 0/1/2/3+ (Change #13/#14) | `yaml_field` | `tier_decision.yaml t2_diversity ∈ {full, degraded}` |
| §4 Wave 0 vendor heterogeneity (Change #18) | `yaml_field` | `return-contract.yaml t2_vendor_diversity ∈ {multi, single}` |
| §4 Wave 1 zero-task guard (Change #12) | `yaml_field` | `return-contract.yaml coverage_undefined == true` |
| §4 Wave 1 coverage_undefined route (Change #11) | `yaml_field` | `return-contract.yaml coverage_pct == null AND tier_reached == 2` |
| §4 Wave 3 reviewer-brief packaging (Change #7) | `dir_count` | `<output>/reviewer-briefs/ min_files=N` |
| §4 Wave 5 sc-adversarial pre-invocation probe (Change #15) | `yaml_field` | `return-contract.yaml adversarial_unavailable` |
| §4 per-step audit emit (Change #22) | `yaml_list_contains` | `audit.log step rows` |
| §5.3 tier rubric rule fired (V2 priority) | `yaml_field` | `tier_decision.yaml fired_rule_number` |
| §5.4 composite_score recording (Change #9) | `yaml_field` | `tier_decision.yaml composite_score AND per_signal_breakdown` |
| §6.4 Serena scripted checkpoints | `checkpoint_logged` | `audit.log checkpoint=<name>` |
| §10 deviation taxonomy = 4 categories | `yaml_list_contains` | `deviation-ledger.yaml deviation_class ∈ {authorized, necessary, drift, regression}` |
| §10.6 grounding-gaps parallel artifact (Change #19) | `file_exists` + `yaml_field` | `grounding-gaps.yaml hunk_ref AND needs_human_decision` |
| §11.0 sufficiency-conditional gates (Change #20) | (eval composition) | dimensions #1 / #4 / #5 sub-criteria |
| §11.3 calibrator disjoint-set (Change #16) | `yaml_field` | `reflection-card.yaml calibrator_model_class NOT IN reviewer_model_classes` |
| §11.5 citation-budget policy (Change #8) | `yaml_field` | `return-contract.yaml citation_budget_policy ∈ {full_reread, sampled}` |
| §12.5 falsifier T2-convergence-wrong-answer (Change #17) | `yaml_field` + composite | `return-contract.yaml regression_present AND convergence_score < 0.75` |
| §9.1 versioned return contract stability | `yaml_field` | `return-contract.yaml contract_version == "1.0"` |
| Adversarial delegation artifacts | `dir_count` | `<output>/adversarial/ min_files=6` |
| Citation grounding (final report) | `citation_resolves` | `REPORT.md` |
| Recommendation actionability | `yaml_list_contains` | `recommendation-scrutiny.yaml decision` |
| Memory write optionality | `yaml_substring` | `telemetry memory_status` |

A protocol step that cannot map to at least one row here should be simplified or removed. The Testability Map is the manifest the eval workspace consumes; the merge-executor verified every row references a real protocol decision in §3-§14 (no orphan rows, no orphan decisions).

---

## 17.7 Kill List — Features Deliberately Excluded

<!-- Source: V3 §13 — merged per Change #4 (5 entries verbatim + 1 row for `unknown` deviation category per INV-015) -->

Features considered and rejected, each with a why-rejected line and a what-replaces-it pointer.

1. **New `coverage-mapper` agent** — the coverage mapping logic is narrow enough to handle inline in Wave 1; a dedicated agent adds coordination overhead without sufficient complexity reduction. *Replaces with:* `requirements-analyst` (UC-1) + inline Wave 1B logic (UC-2). Extract only if eval shows Wave 1 inline logic is fragile.

2. **New `deviation-classifier` agent** — the 4-class taxonomy is a classification rule over commit messages and task logs, not a deep investigation. Inline is cheaper and more auditable. *Replaces with:* `refs/deviation-taxonomy.md` + `root-cause-analyst` per-card.

3. **Streaming / interactive reflection dialogue** — interactive Socratic probing is `sc:brainstorm`'s core value. sc:reflect is a batch review skill. Adding interactive dialogue would duplicate brainstorm's Wave 1 and dilute reflect's identity as a validation tool. *Replaces with:* `Skill sc-brainstorm-protocol` (upstream).

4. **Persistent deviation knowledge graph** — Serena memory stores the last-pass summary. A full deviation graph with deduplication, temporal trending, and cross-project aggregation is a separate product, not a skill feature. *Replaces with:* `mcp__serena__write_memory key=reflect/deviation-patterns-{slug}` with 90-day TTL (§6.3).

5. **Multi-model fan-out in T1** — T1 is intentionally single-agent and cheap. Heterogeneous multi-model review is a T2/T3 feature. Running parallel models at T1 would violate the "quick first" contract that makes sc:troubleshoot's T1 effective. *Replaces with:* §5 rubric escalation path to T2.

6. **5th `unknown` deviation category in deviation-ledger** *(INV-015 resolution)* — V4 proposed `unknown` as a 5th class for evidence-insufficient findings. Rejected because per R3 X-009 / INV-015, structural cleanliness requires the 4-category ledger to remain pure; insufficient-evidence findings route to a *separate* artifact (`grounding-gaps.yaml`) with V4's required-field rigor. *Replaces with:* §10.6 Grounding Gaps parallel artifact (Change #19).

---

## 18. Spec Reference

<!-- Source: Base (V2, original) — §18 (now §18 in this merge; spec ref preserved verbatim) -->

Full spec at `.dev/eval-workspaces/sc-reflect/SPEC.md` (authored alongside SKILL.md per skill-creator iteration-1). This SKILL.md is the working protocol; SPEC.md is the design rationale + acceptance criteria + iteration history.

---

## 19. v1.1 Deferred Hardening (INV-021 + INV-023)

<!-- Source: R3 INV-021 + INV-023 — PARTIALLY-ADDRESSED items carried as v1.1 deferred hardening per Change #18 + Change #20 -->

Two HIGH invariants are deliberately deferred to a future v1.1 release. They are surfaced here so downstream consumers and meta-eval can track the gap.

### 19.1 INV-021 — Vendor heterogeneity v1.1 hardening

**v1.0 posture:** WARN + telemetry (`t2_vendor_diversity: single | multi`) + eval rubric dimension (≥2 vendors → +1.0; 1 vendor → 0.5). Warn-only. See §4 Wave 0 step 0.6 + §12.2.

**v1.1 candidate hardening:** if iteration-2 eval evidence shows convergence-on-wrong-answer cases correlate with single-vendor T2 (i.e., the `T2-convergence-wrong-answer` case fails more often when all reviewers are one vendor), promote single-vendor to a **BLOCK** with WARN before T2 runs unless `--allow-single-vendor` is set.

**Why deferred:** actually requiring cross-vendor would block most users today (who have only Anthropic aliases). The realistic v1 posture is data-collect via telemetry, then harden once evidence justifies the additional friction.

### 19.2 INV-023 — Sufficiency claim v1.1 hardening

**v1.0 posture:** the §11.0 sufficiency claim is **CONDITIONAL** on three gates (calibrator disjoint-set §11.3, ≥2 vendors §4 Wave 0 step 0.6, falsifier eval §12.5). The falsifier eval case ships in iteration-3 hardening; the conditional language is in §11.0.

**v1.1 candidate hardening:** based on first-run results of the `T2-convergence-wrong-answer` case across real eval runs:

- If the case passes ≥80% of runs: tighten language in §11.0 from "conditional" to "demonstrated under these gates."
- If the case fails ≥20% of runs: tighten the §11.3 disjoint-set rule from "degrade to non-disjoint" to "BLOCK at Wave 4" when calibrator class cannot be disjoint from reviewer classes.

**Why deferred:** v1 ships the falsifier eval case (operationalises the claim); v1.1 hardens based on the empirical record. Shipping unconditional sufficiency language in v1 without empirical evidence would be exactly the kind of self-confirming claim this protocol exists to prevent.

### 19.3 Auto-rollback of successful promotion (carryover from §14.5)

**v1.0 posture:** promotion-log preserves the inverse `mv` command but reflect never auto-executes it. Operator-driven rollback only.

**v1.1 candidate hardening:** if iteration-2 eval data shows >0 cases where a promotion was followed by a corrective rollback within 1 hour, add an automatic-rollback path triggered by a post-promotion `/sc:reflect --rollback-last <promotion-log-path>` invocation. Still gated on `confidence-calibrator` confirming the rollback rationale.

**Why deferred:** auto-rollback is dangerous without a clear decision rule for when it fires. v1 keeps the operator in the loop; v1.1 adds rollback only after the data shows a pattern.

### 19.4 Streaming per-task verdict emission (deferred P6)

**v1.0 posture:** `per_task_verdicts` array is emitted in the contract at end-of-run. No streaming.

**v1.1 candidate hardening:** if a real downstream consumer materializes that needs early-halt-on-systemic-failure for large (≥30-task) tasklists, add `<output>/streaming-verdicts.jsonl` emitted as each task verifies. New eval assertion `jsonl_line_count_equals_tasks` verifies streaming completeness.

**Why deferred:** the consumer doesn't exist yet. P1's `per_task_verdicts` array gives end-of-run consumers everything they need. Per spec discipline, don't ship a producer without a known consumer.

### 19.5 Cross-tasklist deviation-pattern memory (deferred P8)

**v1.0 posture:** §17 commits to per-project Serena memory with 90-day expiry for deviation patterns. Scope is per-project, not per-template or per-agent.

**v1.1 candidate hardening:** extend the memory namespace to `reflect/cross-tasklist-patterns/<template-slug-or-agent-id>.md` so recurring patterns across tasklists generated from the same template (or executed by the same agent) surface in subsequent reflect runs.

**Why deferred:** speculative — the existing per-project bucket is sufficient until pattern-recurrence is demonstrated by real data. Adding cross-template/cross-agent scoping is a generalization for a problem that hasn't been demonstrated to exist.
