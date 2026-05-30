---
topic: "Add Wave 1.6 'Diagnosability Audit' to sc:troubleshoot — audit existing logging around the symptom before deep debugging; emit instrumentation tasklist when verdict is 'insufficient' AND the issue is non-trivial."
domain: code
strategy: systematic
depth: standard
proposals_target: 3
handoff_target: none
created: 2026-05-29T14:19:00Z
---

# Seed Brief: troubleshoot Wave 1.6 Diagnosability Audit

## Problem Statement

The current `sc:troubleshoot` protocol (skill at `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`) has a documented gap: it consumes whatever runtime evidence already exists (`evidence_class: runtime_repro | runtime_trace | log_evidence | source_static | doc_static | none` per `refs/hypothesis-card-template.md:23-26`), and when evidence is thin, the only escalation lever is "more agents in parallel" (Tier 2) or `--depth deep`. It never asks the inverse question: *is the system itself under-instrumented for the symptom?* For intermittent bugs, race conditions, performance regressions, and production-only failures — exactly the cases that *should* escalate — hypothesizing harder against blind code is structurally weaker than emitting an instrumentation tasklist and re-running once signal exists.

We want to add a new wave (working name: **Wave 1.6 Diagnosability Audit**) between Wave 1.5 (documentation grounding) and Wave 1.7 (hypothesis formation) that:

1. **Audits logging coverage** around the symptom site — logger calls, print statements, exception-handler richness, log-config files (`logging.yaml`, `pyproject [tool.logging]`, `log4j2.xml`, Sentry init, structured-log filters, log-level config).
2. **Scores instrumentation sufficiency** against the symptom: would the existing logging, if it had fired, have answered "when/where/why"? Verdict: `sufficient | partial | insufficient`.
3. **Branches on (verdict × issue complexity)**:
   - `insufficient` AND issue is non-trivial → **hard-stop**: emit a `diagnosability-tasklist.md` of concrete instrumentation tasks (file:line, log level, fields, scope) + off-ramp message; skip Waves 1.7-5 entirely.
   - `insufficient` AND issue is trivial → **soft-warn**: surface in a Diagnosability Context section of REPORT.md, continue to hypothesis formation.
   - `sufficient` / `partial` → continue normally; surface findings in REPORT.md.

## Known Context

### Settled design forks (from Wave 1 Socratic dialogue + variant-4 field-study integration)

| Fork | Decision | Notes |
|------|----------|-------|
| **Audit scope** | Logging only (narrow) | Loggers, prints, log config, structured-log schemas, exception context. Excludes metrics/traces/full-observability triad for v1. Phase 0 field study (variant-4) advocated for broader scope (CLI flags + OS introspection + doctor commands); user maintained narrow scope (Option A, 2026-05-29). |
| **Default behavior** | Default-on, opt-out via `--no-diagnosability-audit` | Mirrors how Wave 1.5 documentation grounding works today. **The bypass MUST be logged in the troubleshoot output** so post-mortems can see "this run skipped diagnosability validation" (adopted from variant-4 §6 R5). |
| **Response when insufficient** | Hard-stop + tasklist (when non-trivial) / soft-warn (when trivial) | **Load-bearing temporal-discipline rule: no hypothesis work happens in the same turn as an instrumentation patch** (variant-4 §3.5). The hard-stop halts Waves 1.7-5; the user re-runs after instrumenting; that re-run starts fresh with new evidence. Soft-warn path emits the tasklist but continues to Wave 1.7 for the trivial case. |

### Additives confirmed from variant-4 (Phase 0 field study, accepted into the spec without further debate)

1. **Byte-count metric for log-surface sufficiency** — every captured stream in the audit gets a byte-count column. `0 bytes` is a gap signal sharper than static-call-density alone. (variant-4 §3.3 S0.2)
2. **Invocation-site-only instrumentation rule (hard)** — the diagnosability tasklist MUST patch invocation sites (test scripts, CI workflow YAML, dev harnesses), NEVER the failing component's own source. Prevents diagnostic code leaking into release artifacts. (variant-4 §5 R2)
3. **3-round patch-loop cap** — after 3 instrumentation rounds for the same defect, escalate to "structural change needed; this isn't observable through cheap additions." Closes Open Question #6. (variant-4 §3.7)
4. **Heisenbug fallback** — if instrumentation alters timing and the bug stops reproducing, record as Heisenbug finding; fall back to lighter-weight instrumentation (env-vars only, no flag changes). (variant-4 §5 R3)
5. **Component-identification step (S0.1)** — explicit first substep in Wave 1.6: identify the smallest component whose output the failure is asserting against, before any auggie query runs. Sharper than relying on `--scope` alone.
6. **T4 worked example** — variant-4 §4 (zellij contract-test case study) adopted verbatim into `refs/diagnosability-audit.md` as canonical "what the audit saves" illustration.
7. **`--no-diagnosability-audit` bypass is logged** — see settled-fork "Default behavior" above.

### Skill-graph context (Wave 1 grounding)

- Current wave graph: `Wave 0 → 1 → 1.5 → 1.7 → 2 → 3 → 4 → 5 → 6`. New wave inserts at `1.6` between `1.5` (doc-grounding) and `1.7` (hypothesis formation).
- Wave 1.5 has an established 3-branch parallel pattern (release-doc, architectural-doc with currency check, semantic-restriction extraction) via `Task` fan-out and per-branch structured outputs. Wave 1.6 should consider whether to mirror this fan-out shape (e.g., branches for logger-call audit, log-config audit, exception-richness audit) or use a single agent.
- Output Contract today has 13 fields including `doc_context_card_path`, `test_is_wrong`, `behavior_is_documented`, `hypothesis_cards`. New wave likely adds at least `diagnosability_verdict` and `diagnosability_tasklist_path`; maybe `audit_card_path` parallel to `doc_context_card_path`.
- The Escalation Rubric (`refs/escalation-rubric.md`) decides Tier 1 vs Tier 2 in Wave 2. It currently has 5 dimensions and a complexity heuristic (multi-domain, intermittent, security_caution). The new "issue complexity" decision in Wave 1.6 could reuse this rubric's signals OR define its own narrower complexity score — design choice.
- Hypothesis cards currently classify evidence as `runtime_repro | runtime_trace | log_evidence | source_static | doc_static | none`. The new wave's output should influence how the `Runtime check` dimension is scored (rubric line 18) — currently source-only cards mandatorily score 0.0 for `claim_class: runtime_behavior`; that signal partly motivates this work.

## Constraints

- **No new MCP server dependency.** Use existing `mcp__auggie__codebase-retrieval` for log-call discovery + `mcp__serena__find_symbol`/`find_referencing_symbols` for cross-call inspection + `Read`/`Grep`/`Glob` for log-config files. No new context7/tavily reach.
- **Token budget discipline.** Wave 1.5 targets ≤2k Claude tokens (offloads to auggie); Wave 1.6 must hit a similar bar (≤2-3k Claude). Bulk retrieval offloaded to auggie, not Claude reasoning.
- **No silent downgrades.** When the audit cannot run (auggie unavailable, log-config absent, symptom site not localizable), the protocol must record `diagnosability_verdict: unknown` and proceed — never quietly skip without a Grounding Gaps entry.
- **Wave-graph stability.** Existing Waves 0, 1, 1.5, 1.7, 2-6 must not be re-numbered (already a tax — Wave 1.5 + 1.7 split is recent). Insert as `1.6`. Wave 5's REPORT.md template gains a `## Diagnosability Context` section but no other waves change their entry/exit criteria.
- **No auto-execution of the tasklist.** Like Tier 3 (Wave 6), the tasklist is an artifact the user (or a separate `/task` invocation) runs — never auto-applied. Diagnosability changes touch production code paths and must not surprise the user.
- **Backwards-compatible Output Contract.** New fields are additive; downstream consumers (Tier 3 task-builder, fleet auto-apply wrappers) that don't read the new fields keep working.
- **Complexity gate must be cheap.** The trivial-vs-non-trivial classification can't itself require a hypothesis pass — that would be circular. It must be derivable from Wave 0 (parsed type/scope/keywords) + Wave 1 (grounding observations) signals alone.
- **The audit must NOT modify code.** Read-only inspection. The tasklist proposes changes; it does not apply them.

## Success Criteria

A merged design proposal that defines:

1. **Wave 1.6 placement + entry/exit criteria** consistent with Wave 1.5's pattern (parallel `Task` branches with structured per-branch outputs, lazy ref load, audit-log emissions).
2. **Audit mechanics**: what auggie/serena queries run, what files are inspected (logger calls, log config, exception handlers), what schema each branch emits.
3. **Sufficiency rubric**: how the audit synthesizes a `sufficient | partial | insufficient | unknown` verdict from per-branch findings. Be concrete: which signals tip which way, with a worked example for at least one case (e.g., NameError with no nearby logger.exception → sufficient because the stack trace IS the signal; intermittent race condition with only `print` at function entry → insufficient).
4. **Complexity gate**: how Wave 1.6 decides "trivial" vs "non-trivial." Concrete signals from Wave 0 + Wave 1 only. Examples of trivial: deterministic exception with single-file scope, missing-import class, off-by-one with clear stack trace. Examples of non-trivial: intermittent, multi-domain, performance regression, deployment-only.
5. **Output Contract additions**: which new fields, types, default values. Backwards-compatible.
6. **Tasklist artifact format**: what `diagnosability-tasklist.md` looks like — concrete file:line targets, log level, fields, scope. Should be actionable enough that a user (or `task-builder`) can implement it without further design.
7. **Off-ramp UX**: what the chat-surface message says when hard-stop fires; what `Next Steps` line is rendered in REPORT.md.
8. **Risk register**: 3-5 named risks (e.g., audit false-negatives on log-call patterns the auggie query misses; complexity-gate misfires that block a trivial issue; tasklist staleness if user re-runs troubleshoot months after instrumenting; coupling Wave 1.6 too tightly to specific log frameworks).
9. **Ref-file changes**: list each `refs/*.md` file under `sc-troubleshoot-protocol` that needs a new section or new file (e.g., new `refs/diagnosability-audit.md` for queries + sufficiency rubric).
10. **SKILL.md diff sketch**: which sections of `SKILL.md` change (Output Contract table, Wave Structure ASCII, Tool Coordination Summary, Token Cost Profile, Will Do/Will Not Do, Error Handling, Refs table).

## Open Questions (debate-worthy)

1. **Complexity gate signal source.** Options to debate:
   - (a) Reuse the existing escalation-rubric dimensions (multi-domain, intermittent keywords, security_caution) — cheap, consistent with downstream gates, but the rubric was designed for *post-hypothesis* triage, not *pre-hypothesis* gating.
   - (b) Define a new narrower "issue complexity" score from Wave 0 + Wave 1 signals only (type, scope file count, stack-trace clarity, deterministic-vs-intermittent keywords) — purpose-built, but adds a second classification surface to maintain.
   - (c) Use the Tier 1 calibrated confidence from Wave 1.7 — but this fires *after* Wave 1.6, so would require deferring the hard-stop decision until Wave 1.7, breaking the "skip 1.7-5" cleanliness.
2. **Audit branch shape.** Mirror Wave 1.5's 3-branch fan-out vs single-agent vs hybrid (one branch for log-call inspection, one for log-config inspection, synthesize without a 3rd)? Token-budget vs coverage tradeoff.
3. **Where the tasklist lives.** `<output-dir>/diagnosability-tasklist.md` (parallel to other Wave artifacts) vs hand off to `task-builder` for MDTM packaging (consistent with Tier 3 Wave 6 pattern) vs both with the latter gated by a new `--diagnosability-handoff` flag.
4. **Interaction with `--depth deep`.** Today `--depth deep` forces Tier 2 escalation. Does it also force the hard-stop variant of Wave 1.6, even when issue would normally be trivial? Argument for: deep mode signals user wants thoroughness; argument against: forcing instrumentation on a clear NameError just because the user typed `--depth deep` is wasteful.
5. **Interaction with `--no-escalate`.** If user explicitly says "don't escalate," does that suppress the hard-stop (which is itself a kind of escalation to "go instrument first")? Strong case for yes — `--no-escalate` is a user-asserted "give me a Tier 1 best-effort answer."
6. **Re-run loop UX.** When user instruments and re-runs, how does Wave 1.6 know the instrumentation landed? Options: re-audit (might emit the same tasklist if the user instrumented the wrong place), accept a `--skip-diagnosability-audit` per-issue flag, or rely on the user passing fresh log excerpts in the issue description (which Wave 1.6 then weighs).
7. **Cause-class coupling.** Some triage-checklist cause classes (Stale state/cache, Race/concurrency, Performance/resource) almost always benefit from instrumentation; others (Missing import, Type mismatch) almost never do. Should the sufficiency rubric short-circuit on cause class? Risk: cause class is the analyst's *hypothesis* about the bug, not ground truth; rubric should not treat it as authoritative.
8. **Tasklist actionability bar.** How specific must each task be? `Add structured logger.info at foo.py:142 with fields {request_id, attempt, latency_ms}` (high specificity, may require Wave 1.6 to understand the local data model) vs `Add entry/exit logging around the suspect function` (lower specificity, easier to generate, more burden on the user).

## Enrichment Context

Codebase enrichment skipped — prior conversation turn already produced a detailed grounded analysis of the gap (citing `SKILL.md:24, 131-148, 152-187, 198-202`; `refs/hypothesis-card-template.md:23-26`; `refs/escalation-rubric.md:18, 68`; `refs/triage-checklist.md:5-65`; `refs/report-template.md:107`). Parallel-proposal agents should re-read those same files; no additional auggie pull required for v1 brainstorm.
