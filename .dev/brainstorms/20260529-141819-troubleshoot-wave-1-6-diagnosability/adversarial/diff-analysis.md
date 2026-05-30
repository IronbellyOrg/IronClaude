# Diff Analysis: Wave 1.6 Diagnosability Audit (3 variants)

## Metadata

- Generated: 2026-05-29T15:20:00Z
- Variants compared: 3 (variant-1-opus-architect, variant-3-haiku-devops, variant-4-fieldstudy-phase0)
- Total differences found: 14 (5 structural + 4 content + 0 contradictions + 3 unique contributions + 2 shared assumptions)
- Settled-fork lock applied: scope=narrow, placement=between-1.5-and-1.7, default=on — variant-4 positions on these forks are tagged DISQUALIFIED from base selection but additives still mergeable.

## Structural Differences

| # | Area | V1 (architect) | V3 (devops) | V4 (field study) | Severity |
|---|------|----------------|-------------|------------------|----------|
| S-001 | Branch count | 3 branches (D=logger-call, E=log-config, F=symptom-coverage) | 2 branches (A=log-call+exception piggyback, B=log-config) | 0 branches — shell + `--help` based; DISQUALIFIED by scope lock | Medium |
| S-002 | Audit card filename | `diagnosability-audit.md` | `diagnosability-context.md` | n/a (uses 4 separate `phase0-*.md` files) | Low |
| S-003 | Output contract field count | 3 new fields + 1 enum extension on `status` | 4 new fields, no enum change | n/a (no Output Contract concept in field study) | Low |
| S-004 | Wave placement | Between 1.5 and 1.7 ✓ | Between 1.5 and 1.7 ✓ | Pre-Wave-1 ("Phase 0") — DISQUALIFIED by placement lock | High (resolved by lock) |
| S-005 | Discovery mechanism | auggie + serena (per branch) | auggie + Grep/Glob fallback (per branch) | Shell commands + `--help` introspection — DISQUALIFIED by mechanism lock derived from scope lock | High (resolved by lock) |

## Content Differences

| # | Topic | V1 approach | V3 approach | V4 approach | Severity |
|---|-------|-------------|-------------|-------------|----------|
| C-001 | Tasklist handoff | Standalone artifact only; no `--diagnosability-handoff` flag (v1.1 follow-up) | Standalone artifact + `--diagnosability-handoff` flag for task-builder packaging | Patch + commit + push + halt (DISQUALIFIED — no halt-in-same-turn from VCS layer in our scope) | Medium |
| C-002 | `--depth deep` interaction | Does NOT force hard-stop — `--depth deep` is orthogonal to evidence availability | DOES force hard-stop on `insufficient` — `--depth deep` signals user wants thoroughness | n/a (no `--depth` concept) | Medium |
| C-003 | Tasklist specificity bar | Medium-high: file + line + framework + level + suggested fields; fallback to generic field set | High per-line: file:line + current code + framework + literal add-this snippet + fields rationale + verification + rollback (full 5-task worked example) | Patch diff (literal `+`/`-` lines for a complete invocation site) | Low |
| C-004 | Re-run loop UX | `--skip-diagnosability-audit` (per-issue) + tasklist file:line validated at re-run entry | `--skip-diagnosability-audit` (per-issue) + tasklist Verification section instructs user to include fresh log excerpt | 3-round cap; after 3 rounds escalate to "structural change needed" — V4 UNIQUE | High (V4 unique mechanism — adopt) |

## Contradictions

None detected. All 3 variants agree on the core design moves (place between 1.5 and 1.7 — once V4's pre-Wave-1 position is dropped per lock; default-on with `--no-*` opt-out; quaternary verdict — once V4's binary is reframed; hard-stop+tasklist; reuse escalation rubric for complexity; stack-trace-self-documents short-circuit). The remaining differences are choices in dimension, not opposites.

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---------|--------------|-------|
| U-001 | V3 (devops) | Complete 5-task worked tasklist with framework detection, fields rationale, Verification section, Rollback section | **High** — sets the actionability bar |
| U-002 | V1 (architect) | Branch F (symptom-coverage audit) — pure synthesis, no MCP call, addresses the 3 W's (when/where/why) directly | **High** — semantically distinct from log-call and log-config audits |
| U-003 | V4 (field study) | 7 additives: byte-count metric, invocation-site-only rule, 3-round cap, Heisenbug fallback, component-id step (S0.1), T4 worked example, bypass-is-logged | **High** — already absorbed into seed brief; merge spec must surface them |

## Shared Assumptions (UNSTATED preconditions all variants depend on)

| # | Assumption | Source agreement | Impact | Status |
|---|------------|------------------|--------|--------|
| A-001 | The user's failing-component code is **inspectable** — i.e., not closed-source, not compiled-only, not behind an opaque RPC boundary | All 3 variants assume auggie/shell can reach the relevant source/config files | If the failing component is e.g. a managed cloud service or proprietary binary, all 3 audit strategies degrade to `unknown` | UNSTATED — promote to a Risk Register entry in the merge ("R6: opaque-component degradation") |
| A-002 | The user has **write access to the invocation site** (test scripts, CI YAML, dev harnesses) to act on the tasklist | All 3 variants assume the tasklist is implementable by the same user running troubleshoot | If the user is on a read-only branch, or instrumentation requires infra-team approval, hard-stop becomes a dead end | UNSTATED — surface in chat-message off-ramp as "if you can't instrument, re-run with `--no-diagnosability-audit`" |

## Summary

- Convergences (free merge): placement, opt-out behavior, hard-stop+tasklist branching, quaternary verdict, reuse-escalation-rubric for complexity, stack-trace short-circuit, `--no-escalate` suppresses hard-stop.
- Real disagreements requiring base-selection + debate: branch count (3 vs 2), audit-card filename, contract field count, `--depth deep` interaction, tasklist handoff (standalone vs +flag).
- V4 unique mechanism worth promoting regardless of base: 3-round cap, byte-count, invocation-site-only, Heisenbug, component-id, bypass-logged, T4 example.
- Settled-fork lock disqualifies V4's scope/placement/mechanism positions from base selection but does NOT disqualify its 7 additives.
