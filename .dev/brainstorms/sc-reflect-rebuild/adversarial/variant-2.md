---
name: sc:reflect-protocol
description: "Tiered reflection protocol grounded in real code and real citations. UC-1 (pre-execution) validates a proposed strategy/tasklist against its driving spec/PRD for coverage and best-practice compliance. UC-2 (post-execution) audits completed work for 100% adherence and classifies every divergence under a 4-category deviation taxonomy (Authorized expansion / Necessary deviation / Drift / Regression). Tier 1 is a fast single-agent grounded pass; Tier 2 fans out 2-3 heterogeneous reviewer agents on different model classes and merges via sc-adversarial-protocol Mode A; Tier 3 hands off to task-builder for a corrective MDTM remediation. Structural mechanisms — heterogeneous reviewers, blind calibration, mandatory evidence-validator gate — exist specifically to neutralise the representational bias that makes single-agent self-review unreliable."
version: 1.0.0
allowed-tools: Read, Grep, Glob, Bash, TodoWrite, Task, Write, Edit, Skill, mcp__auggie__codebase-retrieval, mcp__serena__find_symbol, mcp__serena__find_referencing_symbols, mcp__serena__get_symbols_overview, mcp__serena__get_diagnostics_for_file, mcp__serena__read_memory, mcp__serena__write_memory, mcp__serena__list_memories, mcp__serena__search_for_pattern, mcp__serena__activate_project, mcp__context7__resolve-library-id, mcp__context7__query-docs, mcp__tavily__tavily-search, mcp__sequential-thinking__sequentialthinking
---

<!-- Extended metadata (for documentation, not parsed):
category: validation
complexity: advanced
mcp-servers: [serena, auggie, context7, tavily, sequential]
personas: [analyzer, qa, refactorer, architect]
spec: .dev/eval-workspaces/sc-reflect/SPEC.md
supersedes: src/superclaude/commands/reflect.md (legacy think_about_* surface)
-->

# Reflect Protocol

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

- `--mode pre | post` — explicit mode (RECOMMENDED for non-interactive callers; eliminates auto-detect ambiguity)
- `--spec <path>` — driving spec/PRD/objectives doc (required for UC-1; recommended for UC-2)
- `--tasklist <path>` — tasklist file (required for UC-2; recommended for UC-1 if a tasklist already exists)
- `--diff <ref-or-path>` — git ref (e.g., `HEAD~1..HEAD`, branch name) or path to a diff file (required for UC-2)
- `--task-log <path>` — task execution log (optional, UC-2 only)
- `--depth quick | standard | deep` — Tier-1-only / Tier-1-then-rubric / force-Tier-2 (see §5)
- `--tier 1 | 2 | auto` — explicit tier pin (overrides rubric); `auto` is default
- `--reviewers N` — number of Tier 2 reviewers (2-3; default 3, clamped by `--depth`)
- `--output <dir>` — output directory (default `.dev/reflect/<mode>-<slug>-<YYYYMMDDHHMMSS>/`)
- `--no-mcp`, `--no-evidence-validator` (debug only; auto-warns), `--remediate` (offer Tier 3)

### 3.2 Mode selection (priority order)

1. **Explicit `--mode pre|post`** wins unconditionally.
2. **Auto-detect from input shape** (only when `--mode` is unset):
   - If `--diff` is present OR `--task-log` is present OR the current git working tree has uncommitted-but-non-empty diff against `--tasklist`'s referenced base → **UC-2 (post)**.
   - Else if `--spec` is present AND `--tasklist` is present AND no diff/log artifact exists → **UC-1 (pre)**.
   - Else if only `--spec` is present → **UC-1 (pre)** with a coverage-only pass (no tasklist-spec map).
   - Else → **STOP** with: `"Reflect requires --mode pre|post OR a resolvable input combination. See refs/input-resolution.md."`

### 3.3 Hard STOP conditions

- Neither `--spec`, `--tasklist`, nor `--diff` provided.
- `--mode pre` with no `--spec` (pre-execution reflection has nothing to reflect against).
- `--mode post` with no `--diff` AND no `--task-log` (post-execution reflection has no completed work to audit).
- `--depth deep` with under-specified input (e.g., 1-line spec, empty tasklist).
- `--output` resolves under `.claude/skills/`, `.claude/agents/`, or `.claude/commands/` (CLAUDE.md ABSOLUTE RULE — distributable paths are not output sinks).

---

## 4. Wave / Tier Architecture

```
Wave 0:   Parse + Validate Input + Activate Project + Memory Hydrate
Wave 1:   Tier 1 — Grounded Single-Agent Reflection
            1A. Real-code grounding (auggie + serena symbolic chain)
            1B. Mode-specific evidence gathering (UC-1: coverage map; UC-2: tasklist-vs-diff map)
            1C. Single-agent reflection (root-cause-analyst OR self-review)
            1D. Blind calibration (confidence-calibrator) on the Tier 1 card
Wave 2:   Tier-Decision Gate (rubric — §5)
Wave 3:   Tier 2 — Parallel Heterogeneous Reviewers (conditional)
            3A. Compose reviewer agent-spec (model + persona rotation)
            3B. Spawn N reviewers in parallel via Task
            3C. Per-card blind calibration (confidence-calibrator × N)
            3D. Distill candidate verdicts
Wave 4:   Tier 2 — Adversarial Merge via sc-adversarial-protocol (conditional)
Wave 5:   Synthesis + Evidence-Validator Gate + Report
Wave 6:   Tier 3 — Remediation Handoff (conditional, opt-in)
```

Each wave has explicit entry/exit. Refs are loaded on-demand per wave, never pre-loaded.

---

## 5. Tier-Decision Rubric (Wave 2)

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
| 1 | `C ≥ 0.90` AND `S_scope ≤ 5 files` AND `S_domains == 1` AND `S_dev_density ≤ 0.05` | **STOP at T1** — high confidence, narrow scope, single domain, near-zero ambiguity |
| 2 | `C ≥ 0.85` AND `S_scope ≤ 10 files` AND `S_domains ≤ 2` AND `S_dev_density ≤ 0.10` | STOP at T1 with WARN if `S_dev_density > 0.05` |
| 3 | UC-2 AND any single hunk classified as `Regression` candidate by Wave 1 | **ESCALATE** (regression must be debated by ≥2 reviewers; structural mechanism, not a confidence question) |
| 4 | `S_domains ≥ 3` | ESCALATE (multi-domain reflection cannot be reliably done by a single reviewer card) |
| 5 | `S_dev_density > 0.20` | ESCALATE (too many unmapped artifacts for a single-pass verdict) |
| 6 | `C < 0.85` | ESCALATE |
| 7 | `--strategy enterprise` set on caller | ESCALATE (enterprise default per sc-brainstorm convention) |
| 8 | Default | STOP at T1 |

### 5.4 Why these thresholds

- `0.90` for the strict T1 ceiling matches CLAUDE.md global rule 3 (≥90% confidence to proceed without alternatives). Reflection findings that the reviewer is willing to call ≥0.90 *and* narrowly-scoped *and* single-domain are the cases where ensemble verification is not cost-justified.
- `0.85` is the medium-confidence floor inherited from sc-troubleshoot's Wave 2 gate.
- `S_dev_density > 0.20` is the "structural ambiguity" trigger — at one in five unmapped artifacts, a single reviewer cannot adjudicate without ensemble pressure.
- Regression candidacy at rule 3 is non-negotiable because asymmetric cost: shipping a missed regression is far worse than spending T2 tokens debating one.

### 5.5 Escalation reason logging

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

These are scripted, not optional. Their output is captured to `<output>/serena-checkpoints.log` for audit. They are not the reflection — they are a free 200-token nudge layered on top.

### 6.5 Fail-open policy

Every Serena call is fail-open per `sc-validate-roadmap-protocol` convention. Missing Serena → fall back to `Grep`/`Glob` with `degraded: true` in the audit. The protocol must never abort because Serena is unavailable.

---

## 7. Agent Delegation Map

Every reusable agent is mapped to a wave; no agent is duplicated inline.

| Agent | Wave | Mode | Role | Fallback |
|-------|------|------|------|----------|
| `root-cause-analyst` | 1C | UC-2 | Investigate any deviation candidate found in Wave 1B; produce hypothesis card with `deviation_class` field | Inline orchestrator card |
| `self-review` | 1C | UC-2 (low-stakes) | Cheap 4-question completion pass (tests / edge cases / requirements / rollback) when `S_scope ≤ 3 files` AND `--depth quick` | Inline 4-question template |
| `requirements-analyst` | 1B | UC-1 | Build the spec-to-tasklist coverage map; surface unmapped requirements | Inline orchestrator analysis |
| `confidence-calibrator` | 1D, 3C | both | Blind re-grade per the 5-dim reflection rubric; the dominant anti-anchoring mechanism | Inline orchestrator calibration with `calibration: inline-fallback` marker |
| `rf-qa` | 3B | UC-2 (structural) | Adversarial-stance structural QA on diff hunks; runs with `fix_authorization: false` (reflection never auto-fixes) | Inline orchestrator pass on `S_scope ≤ 3` |
| `rf-qa-qualitative` | 3B | UC-2 (documents) | Adversarial-stance content-level QA when the artifact under review is a document (PRD, TDD, tech-ref) | Skip; UC-2 still runs with `rf-qa` only |
| `audit-validator` | 5 | UC-2 (large) | When Wave 5 produces ≥20 findings, 10% random spot-check before report ships (lighter alternative to full evidence-validator pass) | Evidence-validator alone (more expensive but stricter) |
| `evidence-validator` | 5 | both | **Non-negotiable final gate**; re-Reads every cited file:line; drops unfounded items | Inline validation with `status: partial` and "validator unavailable" Grounding Gap |
| `task-builder` (skill, not agent) | 6 | UC-2 (post-execution remediation) | Generate corrective MDTM task file from reflection findings | None; surface findings without remediation |
| `socratic-mentor` | 1C | UC-1 (deep) | Optional probing pass for `--depth deep` UC-1 when spec is ambiguous | Skip |

### 7.1 Reviewer composition rules (Wave 3A)

Reviewers are heterogeneous by model class AND by persona, to maximise representational diversity (per Topic 2 research, Wisdom of Silicon Crowd, LLM-TOPLA):

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

Rationale: keeping the SKILL.md within the sc-troubleshoot/sc-brainstorm 421-456 line band requires keeping inline logic *only* where the inline logic is templated. Where the work is open-ended hypothesis or judgement, agents stay. Where the work is mechanical mapping, inline stays.

---

## 8. Cross-Skill Integration

| Skill | When | Why |
|-------|------|-----|
| `sc-adversarial-protocol` (Mode A `--compare`) | Wave 4 (T2 only) | Merge 2-3 reviewer cards into one verdict via the established debate + scoring + merge pipeline. Reflect does NOT re-implement debate. |
| `task-builder` | Wave 6 (T3 only) | Generate corrective MDTM task file from reflection findings; gated on user opt-in. |
| `confidence-check` (skill) | Before any actionable recommendation in Wave 5 chat surface | CLAUDE.md global rule 3 — confidence ≥0.90 to proceed, 70-89% present alternatives, <70% ask. |
| `tech-research` | Wave 1B (optional, `--depth deep` only) | When the spec references frameworks/libraries by name, fetch current best-practice docs (UC-1) or current best-practice patterns to score the implementation against (UC-2). |
| `sc-troubleshoot-protocol` | (Reverse direction — sc-troubleshoot invokes us in its Wave 6 Phase B/D) | Pre-exec + post-exec validation of `/task` runs. |

Invocation pattern (all via `Skill <name>`, never `/sc:<command>`):

```
Skill sc-adversarial-protocol with \
  --compare <output>/reviewer-cards/card-1.md,card-2.md,card-3.md \
  --depth standard \
  --focus correctness,coverage,deviation-classification \
  --output <output>/adversarial/
```

Empty-response / partial-parse / missing-file guards apply per `sc-brainstorm-protocol/SKILL.md:280-285` — no synthetic 0.5 fallback; FAIL if response is unparseable or merged_output_path file does not exist on disk.

---

## 9. Output Contract (Versioned)

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

# Hallucination guard
citations_total: <int>
citations_dropped: <int>      # >0 forces status: partial
citations_inferred: <int>     # [INFERRED]-tagged; does not force partial
evidence_validator_ran: bool

# Tier 2 artifacts
reviewer_cards: [<list of paths>] | []
adversarial_artifacts_dir: <path> | null
adversarial_convergence_score: <float> | null

# Tier 3
remediation_offered: bool
remediation_accepted: bool | null
task_file_path: <path> | null

# Asymmetric-cost flags (downstream automation must respect)
cannot_validate_without_user_input: bool
regression_present: bool
unauthorized_deviation_present: bool
```

### 9.2 Telemetry (non-stable)

```yaml
wave_durations_ms: { wave_0: <ms>, wave_1: <ms>, wave_2: <ms>, ... }
token_usage: { wave_0: <est>, ... }
reviewer_models: [<list>]
reviewer_personas: [<list>]
serena_checkpoints_path: <path>
degraded_components: [<list>]   # e.g. ["auggie", "evidence-validator"]
```

---

## 10. Deviation Taxonomy

Reflection's defining contribution beyond a generic verification protocol is *classifying* every divergence between expected and actual work into a concrete, decision-driving category. The literature gap noted in `research-deep.md` Topic 4.4 is filled here with a 4-category taxonomy. The gold-standard reference source for "what was expected" is the **driving spec/tasklist** (the artifact the agent was instructed to fulfil) — not the executor's commit message, which is reviewer-side narrative.

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

### 10.6 Reporting

Every deviation in REPORT.md is rendered with: file:line, mapped tasklist item (or "unmapped"), spec section (or "n/a"), evidence (verified by evidence-validator), classification rationale (signals matched + gold-standard refs cited), default remediation, and any `[INFERRED]` notes flagged for the reader. Template in `refs/report-template.md`.

---

## 11. Hallucination Guardrails

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

### 11.3 Blind calibration (anti-anchoring)

`confidence-calibrator` per `src/superclaude/agents/confidence-calibrator.md` is deliberately stripped of formation context. The card itself is its only input; the upstream investigative trail is not provided. This reduces (does not eliminate) the anchoring bias where the reviewer's own self-reported confidence inflates the next stage's verdict. Calibrated scores, not self-reports, feed the rubric in §5.

For Tier 2, *every* reviewer card is calibrated by an independent calibrator instance in parallel (Wave 3C). Cards are passed to Wave 4 with calibrated scores attached; sc-adversarial-protocol's debate is weighted by calibrated confidence, not self-reported.

### 11.4 Heterogeneous reviewer ensemble (anti-representational-bias)

Single-model self-review reproduces its own representational bias. Per §7.1, Tier 2 reviewers are heterogeneous by model class. The merge judge is a different class than the debaters (Khan ICML 2024 Oral, Kenton NeurIPS 2024). When the haiku reviewer and the sonnet reviewer agree on a finding, the cross-class agreement is itself evidence that the finding survives at least one representational frame change.

### 11.5 Citation re-Read window (anti-staleness)

Per CLAUDE.md "Context freshness discipline": every `file:line` quoted in the draft report MUST have been Read within the last 5 tool calls before the quote enters context. The orchestrator enforces this explicitly by inserting a final re-Read pass immediately before evidence-validator hands off. Stale citations from earlier waves are re-validated against current file state, not against a possibly-modified mid-wave snapshot.

### 11.6 Inferred-claim audit

The report header surfaces `citations_inferred: N`. A reviewer that produces a report with `citations_total > 20` AND `citations_inferred > citations_total / 2` triggers an automatic WARN in chat: "Reflection is more inference than evidence. Consider re-running with --depth deep or providing more grounding artifacts." This is a soft signal; the report still ships.

---

## 12. Eval Rubric

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

### 12.2 Iteration harness

Three pilot evals for iteration-1, expanding to 9-12 for iteration-2 (mirrors sc-brainstorm's expansion pattern):

| ID | Mode | Scope | Notes |
|----|------|-------|-------|
| `pre-trivial-coverage-gap` | UC-1 | tasklist missing 2/8 spec requirements | T1 expected to STOP with `coverage_pct: 0.75` |
| `post-small-diff-clean` | UC-2 | 3-file diff, all tasklist items mapped, no deviations | T1 expected to STOP with `status: success` |
| `post-large-diff-mixed` | UC-2 | 15-file diff with 1 Regression + 2 Drift + 1 Necessary + 1 Authorized | T2 expected (rule 3 + rule 4 + rule 5); merged verdict must classify ≥4/5 correctly |

Convergence rule: ship iteration N when N+1 vs N shows <5% absolute improvement on held-out test set (60/40 split, Anthropic skill-creator default).

### 12.3 New assertion DSL types

`grader.py` from sc-brainstorm provides 8 syntactic types. Reflect adds two semantic types:

- `citation_resolves` — given a file:line citation in the report, re-Read the file and verify the cited snippet matches the actual content at that line (±5 lines).
- `deviation_class_matches` — given an annotated deviation in the eval fixture, verify the report's deviation register tags the same diff hunk with the same class.

Both new types live in `.dev/eval-workspaces/sc-reflect/grader.py` (copy from sc-brainstorm's `grader.py` and extend).

### 12.4 Grader model

Per Topic 5 research (Arize, Galileo, Evidently): the grader runs on a *different, more capable* model class than the skill-under-test. Default grader: `opus`. The grader is NOT one of the Tier 2 reviewer models, to avoid self-enhancement bias.

For final ship-acceptance, an optional 3-model LLM jury (opus + sonnet + qwen) aggregated by majority across the 5 dimensions. Activated by `--jury` on the eval runner.

---

## 13. Build Path Decision

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
| Deterministic assertion gate | Local `grader.py` (copy from sc-brainstorm; extend with `citation_resolves` + `deviation_class_matches`) | Per-iteration `grading.json` |
| Iteration 2 (9-12 evals) | Same harness, expanded matrix | Convergence check; ship at <5% improvement |
| Production execution | `superclaude sprint run` against tasklists that *use* sc-reflect | Only after skill ships and is stable |
| Real-process eval at scale | `superclaude eval ...` with PTY isolation | Optional, defer until pilot reflect runs are producing reliable artifact shapes |

`superclaude sprint` is *not* the build path; it is the *execution* path for skills already built. Conflating the two is the trap.

### 13.3 What is NOT used

- Sprint CLI for the build loop (wrong shape).
- `superclaude eval ...` for v1 (overkill until artifacts stabilise).
- Skill-creator's default sibling-workspace path (forbidden by project hook).

---

## 14. Error Handling Matrix

| Scenario | Behavior | Fallback |
|----------|----------|----------|
| No `--mode` AND no resolvable input combination | STOP at Wave 0 with usage hint | None |
| `--mode pre` with no `--spec` | STOP | None |
| `--mode post` with no `--diff` AND no `--task-log` | STOP | None |
| `--output` under `.claude/skills`/`.claude/agents`/`.claude/commands` | STOP (CLAUDE.md ABSOLUTE RULE violation) | None |
| `sc-adversarial-protocol` skill missing | STOP at Wave 3 entry with install instruction | None |
| `task-builder` skill missing in Tier 3 | Surface findings without remediation; do NOT silently downgrade | None |
| `confidence-calibrator` agent fails | Inline orchestrator calibration; mark `calibration: inline-fallback` in audit | Continue |
| `evidence-validator` agent fails | Inline citation re-Read; force `status: partial`; add Grounding Gap entry | Continue |
| `root-cause-analyst` agent fails in Wave 1C | Inline orchestrator hypothesis card; mark `hypothesis_source: inline-fallback` | Continue |
| `rf-qa` / `rf-qa-qualitative` fails in Wave 3 | Continue with remaining reviewers; if <2 reviewers complete, downgrade to T1 result with WARN | None |
| All Tier 2 reviewers fail | Downgrade to T1 result; `status: partial`; recommend re-run | None |
| sc-adversarial returns empty / unparseable | FAIL Wave 4 (per sc-brainstorm guard pattern; no synthetic 0.5 fallback) | None |
| sc-adversarial `convergence_score < 0.50` | Surface as `status: partial`; report includes "no merged verdict" warning; skip Wave 6 | None |
| `merged_output_path` from sc-adversarial does not exist on disk | FAIL Wave 4 (missing-file guard before status routing) | None |
| Auggie unavailable | Fall back to Grep/Glob in Wave 1A; mark `degraded: ["auggie"]` | Continue |
| Serena unavailable | Fall back to Grep/Glob; skip `get_diagnostics_for_file`; mark `degraded: ["serena"]` | Continue |
| Context7 unavailable in `--depth deep` UC-1 | Skip best-practice external lookup; mark `degraded: ["context7"]` | Continue |
| `--no-mcp` set | Run with native tools only; WARN that quality is degraded | None |
| Token budget exceeded mid-Wave-3 | Hard abort at 1.25× estimate; preserve partial state for `--resume-from` | None |
| User declines Tier 3 remediation offer | Return success; report stands | None |
| `--depth deep` on under-specified input (≤10 words spec/diff) | STOP at Wave 0; ask user to add detail | None |
| Topic / spec contains adversarial-flag-like chars | Sanitize before passing to sc-adversarial (per sc-brainstorm Wave 2B pattern) | Continue |
| Output dir collision | Append `-N` suffix, cap at 99 with STOP, WARN at N≥10 | None |

---

## 15. Token Cost Profile

| Path | Auggie (offloaded) | Claude (orchestration + agents) | Wall clock |
|------|-------------------|---------------------------------|------------|
| T1 only | ~2-5k | ~3-8k | 1-3 min |
| T2 (2-3 reviewers + adversarial debate) | ~10-25k | ~35-70k | 8-15 min |
| T3 added | +0 | +20-40k | +5-10 min |

Targets, not caps. Hard kill at 1.25× estimate per sc-brainstorm convention.

---

## 16. Refs (loaded on-demand per wave)

| File | Wave | Purpose |
|------|------|---------|
| `refs/input-resolution.md` | Wave 0 | Mode auto-detection rules, STOP conditions, slug generation |
| `refs/reflection-rubric.md` | Wave 1D, Wave 3C | 5-dimension calibration rubric (Citation grounding, Coverage completeness, Deviation-classification clarity, Risk surface coverage, Recommendation actionability) |
| `refs/deviation-taxonomy.md` | Wave 1B (UC-2), Wave 5 | The 4-category taxonomy with detection signals, gold-standard refs, default remediations |
| `refs/coverage-mapping.md` | Wave 1B (UC-1) | Spec-to-tasklist coverage map algorithm; bipartite matching heuristics; `S_dev_density` calculation |
| `refs/reviewer-spec.md` | Wave 3A | Model + persona rotation rules; reviewer card template |
| `refs/report-template.md` | Wave 5 | Final REPORT.md skeleton with Grounded vs [INFERRED] tagging conventions |
| `refs/remediation-handoff.md` | Wave 6 | Task-builder BUILD_REQUEST template; opt-in prompt |

Refs loaded by the wave that needs them; never pre-loaded. Session-start footprint: SKILL.md only (~50 tokens via Claude Code skill loader).

---

## 17. Boundaries

### Will

- Run T1 always; respect "quick first" contract.
- Auto-escalate to T2 only when the rubric in §5 says so, or when `--tier 2`/`--depth deep` is set.
- Fan out heterogeneous reviewers (different model classes) in Tier 2 to break representational-bias self-confirmation.
- Use modern Serena symbolic chain (`get_symbols_overview` → `find_symbol` → `find_referencing_symbols`) for evidence; wire `think_about_*` as scripted nudges captured to audit, never as the gating signal.
- Run `evidence-validator` as a non-negotiable final gate before any report ships; treat a zero-drop pass as a flag, not a clean signal.
- Classify every UC-2 deviation under the 4-category taxonomy in §10 with explicit detection signals and gold-standard references.
- Tag every claim as Grounded or `[INFERRED]`; drop claims that fit neither bucket.
- Respect CLAUDE.md ABSOLUTE RULES: source-of-truth is `src/superclaude/`, never commit `.claude/` mirrors, PR target is fork only.
- Fail-open on missing MCPs (auggie, serena, context7, tavily) — fall back to native tools and mark degraded.
- Persist deviation patterns to per-project Serena memory with 90-day expiry.
- Delegate debate / scoring / merge to `sc-adversarial-protocol`; never re-implement.

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

---

## 18. Spec Reference

Full spec at `.dev/eval-workspaces/sc-reflect/SPEC.md` (authored alongside SKILL.md per skill-creator iteration-1). This SKILL.md is the working protocol; SPEC.md is the design rationale + acceptance criteria + iteration history.
