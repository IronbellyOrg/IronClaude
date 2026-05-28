---
name: sc:troubleshoot-protocol
description: "Tiered debugging protocol — fast Tier 1 triage with auggie + serena grounding, auto-escalation to parallel hypothesis agents + adversarial fix debate in Tier 2, and an opt-in task-builder remediation chain in Tier 3. Use this skill whenever the user reports a broken build, runtime error, performance regression, deployment problem, or failing test, even when they don't explicitly say 'troubleshoot' — phrases like 'why is X broken', 'this used to work', 'something's off with...', a pasted stack trace, or a failing-command transcript should all activate it."
allowed-tools: Read, Grep, Glob, Bash, TodoWrite, Task, Write, Edit, Skill, mcp__auggie__codebase-retrieval, mcp__serena__find_symbol, mcp__serena__find_referencing_symbols, mcp__serena__get_symbols_overview, mcp__context7__resolve-library-id, mcp__context7__query-docs, mcp__tavily__tavily-search, mcp__sequential-thinking__sequentialthinking
---

<!-- Extended metadata (for documentation, not parsed):
category: utility
complexity: advanced
mcp-servers: [auggie, serena, context7, tavily, sequential]
personas: [analyzer, performance, security, qa, refactorer, devops]
-->

# Troubleshoot Protocol

## Purpose

Diagnose a reported issue with the smallest amount of work that produces a high-confidence answer. The protocol is deliberately tiered so that small bugs stay cheap and only complex ones unlock the parallel + adversarial machinery.

**Core contract — quick first, deep when needed.** Tier 1 is intended to feel close to "just look at it" — a single grounded hypothesis returned in roughly 1-2 minutes. Tier 2 is the escape valve for cases where the symptom is ambiguous, spans multiple domains, or where one hypothesis is not enough. Tier 3 closes the loop by turning the chosen fix into an executable task. The user never has to know upfront which tier is needed; the rubric in `refs/escalation-rubric.md` decides.

**Why this works.** Most reported bugs cluster around a small set of common causes: missing imports, off-by-one, stale state, type mismatches, N+1 queries, environment drift. A single experienced agent grounded in real code finds these quickly. The hard cases — flaky tests, regressions after refactors, multi-system performance issues, security findings — benefit from multiple independent hypotheses generated in parallel and then *debated*, because the "obvious" cause is often a red herring and the cost of being wrong is much higher than the cost of fanning out.

**Hallucination contract.** Every claim in the final report must cite a real `file:line` or a real diagnostic command and its output. Findings that cannot be grounded are dropped, not downgraded. A diagnosis built on invented line numbers is worse than no diagnosis at all.

## Required Input (STOP if missing)

The skill receives at least one of:

- An **issue description** (free text, error message, stack trace, log excerpt)
- A **`--scope`** (file, directory, or symbol) paired with at least a brief description

**STOP** if neither is present — without a symptom and a scope the skill has nothing to triage.

**STOP** if `--depth deep` is requested but the issue description is under 10 words and no scope was given — too vague for a deep pass to add value; ask the user to add detail first.

## Output Contract

The skill returns a structured dictionary on completion:

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | `success`, `partial` (some findings dropped for grounding), `failed` |
| `tier_reached` | int | 1, 2, or 3 |
| `report_path` | string | Absolute path to `REPORT.md` |
| `audit_log_path` | string | Absolute path to `audit.log` |
| `confidence` | float | 0.0-1.0, calibrated via `refs/escalation-rubric.md` |
| `escalation_reason` | string | If Tier 2 ran: which rubric condition triggered it (or `forced_by_depth_deep`) |
| `test_is_wrong` | bool | `true` when the diagnosis concludes the failing test is the bug (test asserts wrong behavior, stale invariant, or inverted policy claim) rather than the code under test. Set independent of tier. Asymmetric-cost flag — downstream automation MUST NOT auto-apply a fix to the code when this is `true`; the remediation target is the test file. |
| `test_file_path` | string \| null | When `test_is_wrong=true`, the **repo-relative** path of the test file that must be updated (e.g., `tests/api/test_foo.py`), resolved against the repo root containing `.git/`. `null` otherwise. The format is intentionally fixed to repo-relative so downstream automation can compare/join paths without ambiguity; if the report is consumed outside the repo, the consumer is responsible for joining against the repo root recorded in the audit log. |
| `behavior_is_documented` | bool | `true` when the diagnosis concludes the reported behavior is the documented behavior (i.e., a code change would regress the documented contract). Set independent of tier; mutually exclusive with `test_is_wrong=true`. Asymmetric-cost flag — downstream automation MUST NOT auto-apply a code fix when this is `true`; the remediation target is the spec/docs file(s), or a stakeholder-level discussion. Derived from the chosen hypothesis card's `consistency_with_docs=aligned` AND the Diagnosis section concluding the observed symptom IS the documented behavior. When the failing artifact is a test (Case B in the derivation rule), `test_is_wrong=true` is the correct flag and this flag stays false — the docs are not the bug. |
| `doc_context_card_path` | string \| null | When Wave 1.5 ran, the **repo-relative** path of the Documentation Context Card (e.g., `.dev/troubleshoot/bug-foo-20260522/doc-context.md`). `null` ONLY when `--no-doc-discovery` was set (the wave is skipped entirely). When the wave runs but produces no relevant docs across all three branches, the field still points to an empty card whose sections all read "None found" — distinguished downstream from the skip case via the hypothesis card's `consistency_with_docs=no_docs_found` value. Format is repo-relative, same convention as `test_file_path`. |
| `hypothesis_cards` | list[path] | Paths to per-agent hypothesis cards (Tier 2) |
| `adversarial_artifacts_dir` | string | `sc:adversarial` artifacts dir (Tier 2 only, when 2+ fix proposals were debated) |
| `task_file_path` | string | MDTM task file path (Tier 3 only) |
| `remediation_offered` | bool | Whether Tier 3 was offered |
| `remediation_accepted` | bool | If offered, user's response |

**`test_is_wrong` derivation rule** (applied during Wave 5 synthesis): set `test_is_wrong=true` when the chosen diagnosis names a test file (not production code) as the file requiring change, AND one of these conditions holds:

1. The test asserts an invariant that the cited spec / requirements doc explicitly contradicts (e.g., test claims policy rejects X but the policy doc allows X)
2. The test was authored before a feature change that legitimately altered the asserted behavior, and was not updated alongside the feature
3. The test mis-models the requirement (typo'd assertion, wrong fixture, wrong expected value)

If the diagnosis says "the test is incorrect but the code is also missing a guard" — surface BOTH in `Files to change` but keep `test_is_wrong=false` since the code is the load-bearing fix.

The prose REPORT.md is still the human-readable source of truth; this flag exists so downstream automation (Tier 3 task-builder, fleet auto-apply wrappers, telemetry) can short-circuit on the asymmetric-cost case without parsing prose.

**`behavior_is_documented` derivation rule** (applied during Wave 5 synthesis): set `behavior_is_documented=true` when the chosen hypothesis card's `consistency_with_docs=aligned` AND the Diagnosis section concludes the observed symptom IS the documented behavior (not the user's expected behavior). If the docs say the system should do X and the user reports it does X but expected Y, the bug is in the user's expectation (or the docs) — set the flag and recommend a spec change or stakeholder discussion. If `consistency_with_docs=conflicts`, the docs side with the user — keep the flag false and proceed with normal code remediation. Mutually exclusive with `test_is_wrong=true` by construction (not by tiebreaker), via this 3-case decomposition: **Case A** (user expectation diverges) — observed behavior matches docs AND failing artifact is NOT a test → `behavior_is_documented=true`, `test_is_wrong=false`; remediate via spec change or stakeholder discussion. **Case B** (test contradicts docs+code consensus) — `consistency_with_docs=aligned` AND failing artifact IS a test → `test_is_wrong=true`, `behavior_is_documented=false`; the docs are not the bug, remediate by updating the test to match the docs. **Case C** (code violates docs) — `consistency_with_docs=conflicts` → both flags false, normal code remediation.

This flag exists so downstream automation knows to NOT auto-apply a code fix when the observed behavior is the contracted behavior — the remediation target is the spec, the docs, or a stakeholder discussion.

## Wave Structure

```text
Wave 0: Parse + Validate Input
Wave 1: Tier 1 — Real-Code Grounding  ← always; loads refs/triage-checklist.md on demand (grounding + reproduce only)
Wave 1.5: Documentation Grounding    ← always; loads refs/doc-discovery.md on demand; skipped only by --no-doc-discovery
Wave 1.7: Tier 1 — Hypothesis Formation ← always; consumes Wave 1.5 Documentation Context Card; produces single hypothesis card + calibration
Wave 2: Confidence Gate              ← decides escalation via refs/escalation-rubric.md
Wave 3: Tier 2 — Parallel Hypotheses (conditional)
Wave 4: Tier 2 — Adversarial Fix Debate (conditional, requires ≥2 viable fixes)
Wave 5: Synthesis + Report        ← always finalises; loads refs/report-template.md
Wave 6: Tier 3 — Remediation Chain (conditional, requires --fix + user accept)
```

Each wave has explicit entry/exit criteria. Refs are loaded per-wave, never pre-loaded.

---

### Wave 0: Parse + Validate Input

**Preconditions**: command invocation with at least an issue description or `--scope`.

**Steps**:

1. Parse flags. Required: issue description OR `--scope`. Optional: `--type`, `--depth`, `--fix`, `--no-escalate`, `--models`, `--output-dir`, `--no-mcp`.
2. Auto-detect `--type` if not provided. Use keyword + structural cues from the issue description:
   - Stack trace, exception name, `undefined`/`null`/`NameError` → `bug`
   - "tsc", "ts(", "compiled", "lint", "build", `make`, CI log fragments → `build`
   - "slow", "latency", "p99", "memory", "leak", profiler output → `performance`
   - "production", "deploy", "container", "env var", "service won't start" → `deployment`
   - "auth", "token", "leak", "exposed", "CVE", "vulnerab" → `security`
   - "pytest", "jest", "flake", "intermittent", "passing locally" → `test`
   - On ambiguity, leave `--type` unset and treat all agent specialties as candidates for Tier 2.
3. Resolve `--scope` to a concrete path/symbol. If given, narrow auggie/serena queries to that target.
4. Compute output slug: `<type-or-untyped>-<first-5-words-of-issue-or-scope>-<YYYYMMDDHHMMSS>` and create `<output-dir>/`.
5. Open audit log; emit machine-readable header:

```text
<!-- SC:TROUBLESHOOT:TARGET
issue: <first 80 chars>
type: <type|auto>
depth: <quick|standard|deep|auto>
scope: <path|symbol|none>
fix_authorized: <bool>
no_escalate: <bool>
mcps_available: <auggie|serena|context7|tavily|sequential|none>
output_dir: <abs-path>
-->
```

**Exit criteria**: input validated, output dir created, audit log opened. Emit "Wave 0 complete: type=<type> depth=<depth>".

**STOP conditions**: missing input, conflicting flags (`--depth quick` with `--fix`), `--depth deep` on under-specified input, `--output-dir` not writable.

---

### Wave 1: Tier 1 — Real-Code Grounding

**Goal**: Ground the symptom in real code and capture the reproducer/observation, BEFORE Wave 1.5 documentation grounding and BEFORE hypothesis formation (which moves to Wave 1.7). Splitting Wave 1 this way makes the Wave 1.5 dependency edge explicit: the Documentation Context Card produced by Wave 1.5 step 4 is guaranteed to exist when Wave 1.7's root-cause-analyst consumes it.

**Preconditions**: Wave 0 complete.

**Steps**:

1. **Ground the symptom in real code** — issue two parallel MCP calls (or fall back to native tools):
   - `mcp__auggie__codebase-retrieval` with query: "Find the code involved in: `<issue description, capped at ~300 chars>`. Include the function or module that produces this behaviour, recent changes near it, and any related test." Scope to `--scope` if set.
   - `mcp__serena__get_symbols_overview` on the target file or `mcp__serena__find_symbol` on a specific function if the issue names one.
   - If `--no-mcp` or both MCPs are unavailable: fall back to `Glob` + `Grep` on the issue keywords; note the fallback in the audit log.
2. **Reproduce or observe** (when feasible and cheap):
   - For runtime errors: ask the user for a repro command if not provided, or attempt the obvious one (`pytest <test>`, `npm test`, the command that produced the stack trace). If the issue is a pasted log, treat that as the observation and skip.
   - For build failures: re-run the build command and capture the first error.
   - For performance issues: take the user's reported metric as the observation; do not run benchmarks in Tier 1.

**Exit criteria**: Real-code grounding complete (auggie + serena results captured in audit log, or `Glob`/`Grep` fallback noted); observation captured at `<output-dir>/tier1-observation.md` (or "no repro available" recorded in audit). Emit "Wave 1 complete: grounding done; handing off to Wave 1.5".

**Token budget for Wave 1**: target ≤ ~3k Claude tokens (MCP retrieval offloads the bulk of the work). Hypothesis formation's separate token budget is in Wave 1.7.

---

### Wave 1.5: Documentation Grounding

**Goal**: Surface release-doc context, currency-validated architectural docs, and semantic restrictions that constrain the affected surface, BEFORE any hypothesis is formed.

**Preconditions**: Wave 1 (real-code grounding) is complete; `--no-doc-discovery` is NOT set. When `--no-doc-discovery` IS set, skip this entire wave, record `doc_context_card_path: null` in the output contract, and surface a Grounding Gaps line in Wave 5's REPORT.md.

**Steps**:

1. **Load `refs/doc-discovery.md`** — read the Section 1 Auggie query templates, the Section 2 Branch B currency-check procedure, the Section 3 per-branch output schemas, and the Section 4 Documentation Context Card template.
2. **Spawn three discovery branches** in parallel via `Task` (single message with three Task calls). Each branch receives:
   - The original `<issue_description>`, `<scope>`, and `<component_paths>` from Wave 0.
   - The branch-specific Auggie query template from `refs/doc-discovery.md` Section 1 (Branch A = release-doc, Branch B = architectural-doc with Section 2 currency check, Branch C = semantic-restriction).
   - The output path for the branch's structured-output file: `<output-dir>/wave1_5-branch-<A|B|C>.md` per the Section 3 schemas.
   - An instruction to issue ONE `mcp__auggie__codebase-retrieval` call against the branch's query target and emit the schema-conformant output (Branch A: single object or `{ "hit": false }`; Branch B: array of `{ doc_path, currency_verdict, reason }`; Branch C: array of `{ source_file, file_line, quoted_text, applies_to }`).
3. **Wait for all three branches** to complete. Read each output file.
4. **Synthesise the Documentation Context Card** at `<output-dir>/doc-context.md` using the Section 4 template — merging Branch A's release-doc context (Section: Release context), Branch B's architectural-doc list with currency verdicts (Section: Architectural docs consulted; surface CAUTION lines for `stale` / `unknown` verdicts), Branch C's semantic restrictions (Section: Restrictions / decisions that constrain the fix), and a 1-3 bullet Re-frame signals synthesis tying the three findings back to the bug-as-stated.
5. **Set output-contract pointer** — emit `doc_context_card_path: <output-dir>/doc-context.md` in the audit log so Wave 5 can wire it into the report.

**Exit criteria**:

- Three branch outputs written to disk at `<output-dir>/wave1_5-branch-<A|B|C>.md`.
- One synthesised Documentation Context Card written to `<output-dir>/doc-context.md` with all four named sections populated (Release context, Architectural docs consulted, Restrictions / decisions that constrain the fix, Re-frame signals).
- Emit "Wave 1.5 complete: doc_context_card_path=<output-dir>/doc-context.md".

**Failure handling**:

| Scenario | Behavior | Fallback |
|----------|----------|----------|
| `--no-doc-discovery` set | Skip the entire wave; emit `doc_context_card_path: null`; surface in Grounding Gaps | None |
| Auggie unavailable for any branch | Fall back to `Grep`/`Glob` against the branch's query target (release dirs, docs/ dirs, scope source files); mark `degraded: true` in the affected branch's output | None |
| All three branches return empty / no-hit | Write the Documentation Context Card with "None found" in every section; set `doc_context_card_path` to the (still-emitted) card path; record `behavior_is_documented` derivation as `no_docs_found` candidate downstream | None |
| Branch B Section 2 currency check fails (`stat` not available, mtime unobtainable) | Emit `currency_verdict: unknown` for every Branch B hit; surface CAUTION lines in the card | None |
| Branch synthesis times out / one branch crashes | Continue with remaining branch outputs; mark the missing branch's section as "Branch <X> failed — see audit"; do NOT block downstream waves | None |

**Token budget**: Wave 1.5 should consume ≤ 2k Claude tokens (the auggie calls offload heavy retrieval). If it goes over 3k Claude tokens, audit-log the overrun — the wave is meant to be retrieval-offload, not Claude reasoning.

---

### Wave 1.7: Tier 1 — Hypothesis Formation

**Goal**: Form one calibrated Tier 1 hypothesis card, consuming the Wave 1.5 Documentation Context Card (when produced) so the hypothesis is doc-grounded from the start.

**Preconditions**: Wave 1 (real-code grounding) is complete; Wave 1.5 has produced a Documentation Context Card at `<output-dir>/doc-context.md` (or `--no-doc-discovery` was set and `doc_context_card_path` is `null`).

**Steps**:

1. **Form one hypothesis** — spawn the `root-cause-analyst` agent via `Task` with a focused brief: the symptom, the grounding from Wave 1 step 1, the observation from Wave 1 step 2, the Documentation Context Card path (`<output-dir>/doc-context.md`, or `null` when Wave 1.5 was skipped via `--no-doc-discovery`), and `--scope` if any. The agent's job is to produce one hypothesis card (template in `refs/hypothesis-card-template.md`) — not three, not the full tree. The hypothesis card MUST set `consistency_with_docs` to one of `aligned | conflicts | not_applicable | no_docs_found` based on the Documentation Context Card (or `not_applicable` when the card path is `null`).
2. **Calibrate confidence (independently)** — spawn the `confidence-calibrator` agent via `Task` with `card_path=<output-dir>/tier1-hypothesis.md`, `rubric_path=<skill-dir>/refs/escalation-rubric.md`, `card_tier=1`, `flags_context=<wave 0 parsed flags>`, `output_path=<output-dir>/tier1-calibration.md`. The agent re-grades the hypothesis card against the 5-dimension rubric without the formation context (anchoring is reduced, not eliminated). Its calibrated confidence and verdict feed Wave 2 directly.
   - **Fallback**: if `confidence-calibrator` fails (subprocess crash, malformed output, agent unavailable), fall back to inline orchestrator calibration against the rubric and mark `calibration: inline-fallback` in the audit log.

**Exit criteria**: One hypothesis card at `<output-dir>/tier1-hypothesis.md`, a calibration report at `<output-dir>/tier1-calibration.md` (or `calibration: inline-fallback` in audit), and the calibrated confidence in the audit log. Emit "Wave 1.7 complete: confidence=<x>".

**Failure handling**: If the `root-cause-analyst` agent fails entirely (subprocess crash, no output card produced), fall back to inline orchestrator hypothesis formation against `refs/hypothesis-card-template.md` and mark `hypothesis_source: inline-fallback` in audit. Wave 2 confidence gate proceeds normally with whatever was produced.

**Token budget for Wave 1.7**: target ≤ ~3k Claude tokens (excluding the agent subprocess; the agent's own budget is governed by `--models` if overridden).

---

### Wave 2: Confidence Gate

**Goal**: Decide whether to stop or escalate.

**Decision logic** (from `refs/escalation-rubric.md`, summarised here for traceability):

- `--depth quick` OR `--no-escalate` → STOP at Tier 1 regardless of confidence; emit warning in report if confidence < threshold.
- `--depth deep` → ALWAYS escalate to Tier 2.
- Otherwise (`--depth standard` or unset):
  - `confidence ≥ 0.85` AND symptom is single-domain → STOP at Tier 1.
  - `confidence < 0.85` → escalate.
  - Multi-domain symptom (e.g. perf + correctness, security + build) → escalate even if confidence is high (because one hypothesis cannot cover both domains adequately).
  - Reproducibility unclear or "intermittent" mentioned → escalate.

**On STOP**: jump to Wave 5 (synthesis + report) with `tier_reached=1`.

**On escalate**: record the `escalation_reason` in the audit log and proceed to Wave 3.

---

### Wave 3: Tier 2 — Parallel Hypotheses

**Goal**: Cast a wider net with multiple independent perspectives, then surface the strongest candidate fixes.

**Preconditions**: Wave 2 decided to escalate.

**Agent selection** — pick 2-4 agents based on `--type` and signal mix. Each agent runs in its own context, in parallel, via `Task`:

| Signal / type | Agents to spawn |
|---------------|------------------|
| `bug` (default) | `root-cause-analyst`, `quality-engineer` (edge cases), + 1 of {`refactoring-expert` if recent refactor signals, `system-architect` if multi-component} |
| `performance` | `performance-engineer`, `root-cause-analyst`, `system-architect` (if cross-component) |
| `security` | `security-engineer`, `root-cause-analyst`, `quality-engineer` |
| `build` | `root-cause-analyst`, `devops-architect`, `refactoring-expert` |
| `deployment` | `devops-architect`, `root-cause-analyst`, `system-architect` |
| `test` | `quality-engineer`, `root-cause-analyst`, `refactoring-expert` (if test is brittle by structure) |

Cap at 4 agents. If `--type` is unset and signals point in multiple directions, spawn 3 from the union of relevant rows.

**Steps**:

1. **MCP enrichment in parallel with agent spawn** — issue any of the following that match the signals (parallel calls, all kicked off in the same turn):
   - `mcp__context7__resolve-library-id` + `mcp__context7__query-docs` when the issue mentions a framework / library by name or the stack trace is in third-party code
   - `mcp__tavily__tavily-search` for the exact error message string + "github issue", or for `<library> <version> <symptom>` (rate-limited — at most 2 queries in this wave)
   - `mcp__auggie__codebase-retrieval` with a more targeted query than Tier 1 (e.g. "find every call site of `<symbol>` and how they handle the error case")
2. **Spawn hypothesis agents** in parallel via `Task` (single message with multiple Task calls). Each agent receives:
   - The original issue + Tier 1 hypothesis card (so they can agree, disagree, or extend)
   - The **Documentation Context Card** at `<output-dir>/doc-context.md` (the same single card produced by Wave 1.5 — agents do NOT re-run discovery). If `--no-doc-discovery` was set, this path is `null` and agents set `consistency_with_docs: not_applicable` in their hypothesis cards.
   - The MCP enrichment results
   - The output path for their own hypothesis card: `<output-dir>/tier2-<agent-name>-hypothesis.md`
   - An instruction to produce **at most one proposed fix** with: claim, evidence (cited file:line or command output), proposed fix, confidence, risks, `consistency_with_docs` (see `refs/hypothesis-card-template.md`), and a one-line "if I'm wrong it's probably because...".
   - Use the agent's default model. If `--models` overrides per-tier, apply (e.g. `hypothesis:opus` forces all hypothesis agents to opus).
3. **Wait for all agents** to complete. Read each card.
3.5. **Calibrate each card independently** — spawn N `confidence-calibrator` instances in parallel (one per Tier 2 card), each with `card_tier=2` and `output_path=<output-dir>/tier2-<agent-name>-calibration.md`. Use the calibrated scores (not the agents' self-reports) when weighting consensus/competing/outlier in step 4. Fallback rule from Wave 1.7 applies per-card.
4. **Distill candidate fixes**: cluster the hypothesis cards by proposed fix. If 2 or more agents propose substantively different fixes, mark them as **competing**. If they all converge on one fix, mark as **consensus**.

#### Tier 2 calibration completeness gate (hard precondition for report publishing)

After all Tier 2 hypothesis cards are written and the calibrator subagents have been dispatched, the orchestrator MUST verify on disk:

- For every `tier2-<agent-name>-hypothesis.md` card written in this run's output directory, a sibling `tier2-<agent-name>-calibration.md` artifact MUST exist and parse as a Calibration Report (per the agent's Output Format).
- If any sibling calibration artifact is missing or malformed, the orchestrator MUST NOT publish `REPORT.md` with the un-calibrated card's confidence. Instead:
  1. Log `calibration: missing` for each missing sibling in `audit.log` with the absolute card path.
  2. Re-dispatch the `confidence-calibrator` `Task` once for the missing card with the same inputs. Wait up to 2 minutes wall-clock for completion. If the retry does not produce a parseable Calibration Report within that window, proceed to the force-degrade step. Do not attempt a third retry.
  3. If retry still fails, write the card into `REPORT.md` with confidence force-degraded to `min(self_reported, 0.65)` (using the card's self-reported confidence — per the hypothesis-card template, the `## Confidence` section's `Self-reported confidence: <0.0–1.0>` line is the load-bearing input; in the worked-example rendering, this is the bare numeric on the line immediately under the `## Confidence` header). If `self_reported` is missing, null, non-numeric, or outside `[0.0, 1.0]`, default to `0.0` (the most pessimistic safe value); clamp out-of-range numeric values into `[0.0, 1.0]` first, then apply the floor. Annotate `audit.log` with `calibration: force_degraded card=<path> self_reported=<value|missing|non-numeric|out-of-range> floored=0.65 calibration_status=failed_to_calibrate`. Add a prose line to the Grounding Gaps section of `REPORT.md` reading `Hypothesis card from <agent> could not be calibrated after one retry — confidence force-degraded to min(self_reported, 0.65); calibration_status: failed_to_calibrate.` Self-reported confidence is NEVER passed through unmodified.

Verification command (run before publishing): for each `tier2-*-hypothesis.md` (excluding `*-calibration.md`), assert a matching `*-calibration.md` exists and contains the Calibration Report markers (`# Calibration Report`, `## Per-dimension scores`, `## Confidence`, `## Escalation recommendation`, `**Verdict**: STOP|ESCALATE`, `**Calibrated (this report)**:` with a parseable float) — failure triggers the three-step ladder above.

**Exit criteria**:

- ≥ 1 hypothesis card written to disk
- A `candidate-fixes.md` index file written listing each unique fix proposal, the supporting agent(s), and a quick verdict (`consensus` / `competing` / `outlier`)

**Failure handling**:

| Scenario | Behavior | Fallback |
|----------|----------|----------|
| Agent subprocess fails | Continue with remaining agents; record failure in audit | If < 2 agents complete, downgrade to "Tier 1 only" and add a warning to the report |
| MCP call fails (auggie/serena) | Fall back to `Grep`/`Glob`; note in audit | None — proceed without that enrichment |
| MCP call fails (context7/tavily) | Continue without external docs; note in audit | None |
| All agents converge with high confidence | Skip Wave 4 (adversarial); jump to Wave 5 | None |
| All agents diverge with low confidence | Proceed to Wave 4; warn in audit that no fix is strongly supported | None |

---

### Wave 4: Tier 2 — Adversarial Fix Debate

**Goal**: When Wave 3 produced 2-3 competing strong fix proposals, let `/sc:adversarial` debate them so the chosen fix has earned its position.

**Preconditions**: Wave 3 marked ≥ 2 fixes as `competing` (or `--depth deep` + ≥ 2 distinct proposals, even if consensus).

**Steps**:

1. **Materialise each candidate fix as a standalone file** — write `<output-dir>/fix-proposals/fix-<N>.md` for each, structured as a self-contained proposal (problem statement, proposed change, evidence, risks, test plan). **When a Documentation Context Card exists at `<output-dir>/doc-context.md` (i.e., `--no-doc-discovery` was NOT set)**, append a final `## Documented constraints to honor` section to every `fix-<N>.md` containing a verbatim copy of the Card's Restrictions and Re-frame signals sections. This embed makes the debate doc-context-aware via the `--compare` artifact channel without introducing any new flag on `/sc:adversarial`. The debate agents, instructed to read each fix proposal in full, will weight proposals against the embedded constraints naturally. A fix that violates an embedded constraint must be either rejected outright by the debate, or wrapped as a **doc-update + fix bundle** (see step 3 output mode).
2. **Invoke `/sc:adversarial` in compare mode** via `Skill`:

   ```text
   Skill sc:adversarial-protocol with --compare fix-1.md,fix-2.md[,fix-3.md] \
       --depth quick (when source signals are strong) | standard (default) \
       --focus correctness,risk,test-coverage \
       --output <output-dir>/adversarial/
   ```

   - Use `--depth quick` if all proposals share the same diagnosis and only differ in the fix mechanism (fast debate is sufficient).
   - Use `--depth standard` otherwise.
3. **Collect adversarial output** — `<output-dir>/adversarial/` will contain the standard 6 artifacts (`diff-analysis.md`, `debate-transcript.md`, `base-selection.md`, `refactor-plan.md`, `merge-log.md`, `merged-output.md`). The merged output is the **chosen fix proposal**. If the debate flagged that the winning proposal requires a doc update to remove or rewrite a documented constraint (surfaced via the embedded `## Documented constraints to honor` section in the source fix-<N>.md), the merged output is structured as a **doc-update + fix bundle**: the bundle lists the doc file(s) to update alongside the code change(s), and Wave 5's Proposed Fix section renders both atoms.
4. **Sanity-check the merge** — spawn `self-review` via `Task` against the merged fix proposal with the four standard self-check questions (tests? edge cases? requirements? follow-up?). Record the result in the audit log. If self-review flags a blocker, surface it and STOP — do not proceed to Wave 5 with a known-broken proposal.

**Exit criteria**: `adversarial/merged-output.md` exists, `self-review` produced an OK or a documented blocker.

**Skip conditions**: only one viable fix proposal (skip and proceed to Wave 5), or all proposals failed sanity in Wave 3.

---

### Wave 5: Synthesis + Report

**Goal**: Produce one diagnosis report at `<output-dir>/REPORT.md` regardless of which tier ran.

**Steps**:

1. Load `refs/report-template.md` (not before now — lazy load).
2. Compose `REPORT.md` filling in:
   - Header (target, tier reached, confidence, escalation reason)
   - Summary (2-4 sentence executive summary)
   - Documentation Context (≤6-line summary of the Wave 1.5 Documentation Context Card at `<output-dir>/doc-context.md`; omit this section entirely and add a line to Grounding Gaps when `--no-doc-discovery` was set)
   - Diagnosis (the chosen hypothesis — from Tier 1 alone, or from the adversarial merge)
   - Evidence (cited `file:line` and command outputs)
   - Proposed Fix (the recommended change; if a doc-update + fix bundle was produced in Wave 4, render BOTH the doc file(s) to update and the code change(s) in this section)
   - Alternative Fixes Considered (Tier 2 only — the losing proposals from the debate, with one-line reason each)
   - Risk + Rollback (what to watch after applying)
   - Next Steps (Tier 1: rerun with `--depth deep` if needed; Tier 2 without `--fix`: re-invoke with `--fix` to authorize remediation; Tier 2 with `--fix`: confirm to proceed to Wave 6)

   When `--no-doc-discovery` was set, omit the Documentation Context section entirely AND populate the Grounding Gaps section with: "Documentation grounding skipped by `--no-doc-discovery` — diagnosis is not weighted against documented behavior or restrictions."
3. **File:line validation pass (non-negotiable)** — spawn the `evidence-validator` agent via `Task` with `report_draft_path=<output-dir>/REPORT.md.draft`, `evidence_section_locator="## Evidence"`, `output_path=<output-dir>/evidence-validation.md`, `allow_command_reexec=false`. The agent Reads every cited `file:line`, drops mismatches, and returns the verified evidence set plus a `Suggested report status` (success/partial). Apply its verdict: remove dropped citations from the final `REPORT.md`; if any were dropped, set the report's frontmatter `status: partial` and add a "Grounding Gaps" entry referencing them.
   - **Fallback**: if `evidence-validator` fails (subprocess crash, malformed output, agent unavailable), inline-validate citations in the orchestrator context (the original Wave 5 step 3 behavior); mark `status: partial` and add a Grounding Gap entry noting the validator was unavailable. The inline path is the fallback — never ship without validation.
4. Append the machine-readable footer to the audit log:

```text
<!-- SC:TROUBLESHOOT:SUMMARY
status: <success|partial>
tier_reached: <1|2|3>
confidence: <float>
escalation_reason: <none|low_confidence|multi_domain|forced_by_depth_deep|intermittent>
hypothesis_count: <N>
adversarial_invoked: <bool>
fix_authorized: <bool>
duration_sec: <N>
-->
```

5. Surface to the user in chat:
   - One-paragraph summary
   - Path to `REPORT.md`
   - The chosen fix (concise)
   - Tier reached + confidence
   - Next-step recommendation

**Exit criteria**: `REPORT.md` written, audit log finalized, user notified. If `--fix` is not set, return the output contract and STOP.

---

### Wave 6: Tier 3 — Remediation Chain

**Preconditions**: `--fix` is set AND `REPORT.md` is `success` (not `partial`) AND user explicitly accepts the remediation offer.

**Steps**:

1. **Present the remediation offer** to the user — read the prompt template in `refs/remediation-handoff.md`. Ask one yes/no question. Wait.
2. On accept:
   - **Phase A — Build the task file**: invoke the `task-builder` skill via `Skill` with a `BUILD_REQUEST` whose GOAL is "Apply the fix described in `<REPORT.md path>`", WHY is the summary section, WHERE is the cited file(s), and TEMPLATE is generic (template 01) unless the fix involves > 3 files or > 2 hours of work (then template 02).
   - **Phase B — Pre-execution review**: after `task-builder` returns the task file path, invoke `/sc:reflect --type task --analyze` (if available) against the new task file. If reflect flags issues, surface them; ask the user whether to refactor the tasklist or proceed as-is.
   - **Phase C — Execution gate**: do NOT auto-execute. Surface the task file path and the literal command (`/task <path>`) the user can run. Stop here — the user runs it.
   - **Phase D — Post-execution validation** (only if the user reports back after `/task` completion): invoke `/sc:reflect --type task --validate` (or `self-review` agent as fallback) before the user commits.
3. On decline: return success; the report is the final deliverable.

**Exit criteria**: task file path returned (or decline recorded). Output contract finalized.

---

## Tool Coordination Summary

| Tool | Tier 1 | Tier 2 | Tier 3 |
|------|--------|--------|--------|
| `mcp__auggie__codebase-retrieval` | ✓ (one focused query + Wave 1.5 doc-grounding fan-out: 3 parallel branch queries) | ✓ (per-hypothesis queries) | — |
| `mcp__serena__find_symbol` / `find_referencing_symbols` / `get_symbols_overview` | ✓ | ✓ | — |
| `mcp__context7__query-docs` | — | ✓ when framework/library named | — |
| `mcp__tavily__tavily-search` | — | ✓ rate-limited (≤2 queries) | — |
| `mcp__sequential-thinking__sequentialthinking` | — | ✓ for synthesis | — |
| `Task` (agent spawn) | ✓ (root-cause-analyst + confidence-calibrator) | ✓ (2-4 hypothesis agents in parallel + per-card confidence-calibrator + evidence-validator at Wave 5) | ✓ (self-review for post-exec) |
| `Skill` | — | ✓ (`sc:adversarial-protocol`) | ✓ (`task-builder`, `/sc:reflect`) |
| `Read` / `Grep` / `Glob` | ✓ | ✓ | — |
| `Bash` | ✓ (repro when cheap) | ✓ (diagnostic commands) | — |
| `Write` | ✓ (hypothesis + report) | ✓ (hypothesis cards, fix proposals) | — |

## Will Do

- Always run Tier 1 first; respect the "quick first option" contract
- Auto-escalate only when the rubric in `refs/escalation-rubric.md` says so, or when `--depth deep` is set
- Fan out 2-4 specialist agents in parallel in Tier 2, chosen by signal mix
- Use auggie/serena every tier for in-repo grounding; use context7/tavily only in Tier 2 and only when the symptom suggests external knowledge
- Run `/sc:adversarial` only when Tier 2 produces 2-3 competing strong fixes (not when there is consensus — that wastes the debate)
- Run `self-review` after the adversarial merge to catch obvious regressions before reporting
- Validate every `file:line` citation in the report against the real file
- Stop at the natural off-ramp for each tier; never silently proceed to a deeper tier than the user authorized

## Will Not Do

- Apply code changes without `--fix` and explicit user confirmation
- Skip Tier 1 and jump straight to Tier 2 (even with `--depth deep`, Tier 1 still runs first — it's cheap and its output feeds Tier 2)
- Spawn Tier 2 hypothesis agents on consensus single-domain Tier 1 results
- Spawn more than 4 hypothesis agents in Tier 2 (token waste; signal already saturated)
- Call tavily without a focused query (the rate cap exists for a reason)
- Trust agent-reported confidence without independent re-grading (the `confidence-calibrator` agent or the inline fallback applies the rubric in a fresh context)
- Ship a `REPORT.md` whose `file:line` citations have not passed through `evidence-validator` (or the inline fallback)
- Auto-execute the Tier 3 task file — that is always a separate user-initiated `/task` invocation
- Auto-commit after Tier 3 — `/sc:reflect --type task --validate` is the final gate the user runs before committing

## Error Handling

| Scenario | Behavior | Fallback |
|----------|----------|----------|
| All MCPs unavailable | Run in `--no-mcp` mode; warn user that triage quality is degraded; native tools only | None |
| auggie unavailable (others OK) | Fall back to `Grep` + `Glob` for grounding; mark in audit | None |
| auggie unavailable in Wave 1.5 (others OK) | Fall back to `Grep`/`Glob` against the per-branch query targets (`.dev/releases/`, `docs/`, `<scope>`); mark `degraded: true` per branch; do NOT block the Tier 1 hypothesis | None |
| All three Wave 1.5 branches return empty / no-hit | Write Documentation Context Card with "None found" in every section; set `doc_context_card_path` to the (still-emitted) empty card; mark `behavior_is_documented` derivation as `no_docs_found` candidate | None |
| `--no-doc-discovery` set by user | Skip Wave 1.5 entirely; emit `doc_context_card_path: null`; record skip-line in Wave 5 Grounding Gaps | None |
| root-cause-analyst agent fails in Tier 1 | Skill produces a degraded Tier 1 (Claude inline) and recommends `--depth deep` | None |
| All Tier 2 agents fail | Downgrade to Tier 1 result; report `partial`; recommend rerun | None |
| `sc:adversarial-protocol` fails in Wave 4 | Pick the highest-confidence Tier 2 fix proposal as the chosen fix; note in audit and report header | None |
| `self-review` flags blocker on adversarial merge | STOP at Wave 5 with `partial` status; report includes the blocker; recommend rerun with `--depth deep` or different focus | None |
| `task-builder` unavailable in Wave 6 | Surface the fix proposal path; recommend manual task creation; don't fail the whole skill | None |
| User declines remediation offer | Return success; report stands | None |
| `--depth deep` requested on under-specified input | STOP at Wave 0; ask user to add detail | None |
| `evidence-validator` agent fails (subprocess crash, timeout, or malformed report) | Inline-validate citations in the orchestrator context (the original Wave 5 step 3 behavior); mark `status: partial` and add a Grounding Gap entry noting the validator was unavailable | None — the inline path is the fallback |
| `confidence-calibrator` agent fails for any card | Fall back to inline orchestrator calibration for that card; mark the card with `calibration: inline-fallback` in the audit log; do NOT block escalation on a missing calibration | None |

## Token Cost Profile

| Tier reached | Auggie tokens (offloaded) | Claude tokens (orchestration + agents) | Wall clock |
|--------------|---------------------------|----------------------------------------|------------|
| Tier 1 only | ~2-5k | ~3-6k | 1-3 min |
| Tier 2 (no adversarial) | ~5-15k | ~15-30k | 4-7 min |
| Tier 2 (with adversarial) | ~10-25k | ~30-60k | 8-15 min |
| Tier 3 added | +0 (auggie not used) | +20-40k (task-builder) | +5-10 min |

These are targets, not hard caps. Auggie tokens are offloaded to a free / low-cost retrieval tier; Claude tokens are the constrained resource. The escalation gate exists specifically to keep the Tier-1-only path inside the 3-9k Claude-token band for the common case.

## Refs

| File | When loaded |
|------|-------------|
| `refs/escalation-rubric.md` | Wave 2 (confidence gate) and Wave 1.7 (calibration) |
| `refs/triage-checklist.md` | Wave 1 (real-code grounding load) AND Wave 1.7 (passed to root-cause-analyst as part of the brief) |
| `refs/doc-discovery.md` | Wave 1.5 (documentation grounding — Auggie query templates, currency-check procedure, output schemas, Documentation Context Card template) |
| `refs/hypothesis-card-template.md` | Wave 1.7 and Wave 3 (passed to agents) |
| `refs/report-template.md` | Wave 5 |
| `refs/remediation-handoff.md` | Wave 6 |

Each ref is loaded only by the wave that needs it. Do not pre-load.
