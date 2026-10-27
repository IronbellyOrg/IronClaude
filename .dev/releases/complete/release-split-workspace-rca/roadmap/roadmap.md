---
artifact_type: roadmap
spec_source: .dev/releases/current/release-split-workspace-rca/merged-thesis.md
generated: 2026-05-13
generator: sc-roadmap-protocol v2.0.0
template: inline (quality-derived; remediation flavor)
template_compatibility:
  quality: 0.85
  security: 0.55
  migration: 0.40
  feature: 0.20
complexity_class: MEDIUM
complexity_score: 0.60
primary_persona: devops
consulting_personas: [security, architect, refactorer, scribe]
domain_distribution:
  devops: 0.55
  security: 0.20
  architect: 0.15
  scribe: 0.10
milestone_count: 5
total_deliverables: 16
total_tasks: 16
deliverables_breakdown:
  M1: 3
  M2: 3
  M3: 3
  M4: 2  # D4.2 is optional (defer-pending-capacity)
  M5: 5
risks_count: 5
acceptance_criteria_count: 5
compliance_tier: STANDARD
adversarial_predecessor: true
validation_score: 0.875
validation_status: PASS
validation_agents:
  quality_engineer: 0.87
  self_review: 0.88
validation_weights:
  quality_engineer: 0.55
  self_review: 0.45
---

# Roadmap — Release-Split Workspace Misplacement Remediation

## Overview

This release implements the 11-action **layered fix** synthesized in `merged-thesis.md` after an adversarial debate over a workspace-misplacement incident: ~100 eval artifacts for `sc-release-split-protocol` landed under `.claude/skills/sc-release-split-protocol-workspace/` (inside the distributable skill tree) because Anthropic's vendored `skill-creator` plugin has a hardcoded "sibling to skill directory" convention (SKILL.md L167) with no override flag.

The workspace itself has already been physically relocated to `.dev/eval-workspaces/sc-release-split-protocol/` (commit `86d2749`). This roadmap covers the **preventive remediation** so the same path is not re-tread by a future good-faith author:

- **Layer 1** (occurrence prevention): hook + project rule + convenience target
- **Layer 2** (persistence prevention): correct error message → blocklist → CI enforcement
- **Layer 3** (defense in depth): skill-level output-path guard
- **Validation**: end-to-end exercise of all 5 acceptance criteria

Sequencing is driven by INV-002 (HIGH, unaddressed in the thesis), which mandates that the CI gate land before the rest of Layer 2 is meaningful.

## Milestone Summary

| ID | Name | Priority | Effort | Dependencies | Deliverables |
|---|---|---|---|---|---|
| M1 | Pre-flight & discoverability | P1 | S | — | D1.1, D1.2, D1.3 |
| M2 | Detection gate (closes INV-002) | **P0** | M | M1 | D2.1, D2.2, D2.3 |
| M3 | Occurrence prevention | P1 | M-L | M2 | D3.1, D3.2, D3.3 |
| M4 | Defense in depth | P2 | S | (parallel-eligible with M3) | D4.1, D4.2* |
| M5 | Acceptance validation | P1 | M | M1, M2, M3, M4 | D5.1–D5.5 |

*D4.2 is the optional sibling-skill consistency pass per merged-thesis §L3.2.

## Dependency Graph

```
M1 ──► M2 ──► M3 ──┐
                   ├──► M5
       ┌─► M4 ─────┘
       (M4 may start as early as M1 completion; only joins at M5)
```

DEP-001: M2 depends on M1 — error message in D2.1 must cite the convention published in D1.1 (`.dev/README.md`).
DEP-002: M3 depends on M2 — hook + CLAUDE.md override carry less risk if CI gate is already detecting bypass cases.
DEP-003: M5 depends on M1+M2+M3+M4 — exercises full layered defense. **M5 ENTRY GATE**: no CP-M3-END CRITICAL severity findings may be open (test-strategy thresholds binding).
DEP-004: M4 may start as early as M1 completion (skill content edits need the convention published), but joins M5 alongside M3.
DEP-005: M4 has a SOFT dependency on M2 — M4's own validation runs `make verify-sync` which only emits the correct error messages after D2.1 + D2.2 land. M4 can begin authoring edits before M2 completes but should not be marked done until M2 verify-sync output is correct.

DAG validated: acyclic. Soft dep DEP-005 does not introduce a cycle (M2→M4 only; M4 does not feed back into M2).

## M1 — Pre-flight & Discoverability

**Objective**: Land zero-risk docs/config so subsequent milestones can cite a published convention.

**Deliverables**:

- **D1.1** — Create `.dev/README.md` documenting all `.dev/` subdirectories (releases, eval-workspaces, etc.). Include the explicit rule: *"Workspaces, fixtures, harness code, and iteration outputs go under `.dev/`, never under `.claude/skills/`. Eval workspaces use `.dev/eval-workspaces/<skill-name>/`."* (Sourced from FR-L2.4.)
- **D1.2** — Repair broken `PLANNING.md`/`TASK.md` pointers in `/config/workspace/IronClaude/CLAUDE.md` (lines 51-53 and 225-227). `KNOWLEDGE.md` already exists at repo root and stays. **Pre-decision (resolves self-review TOP CONCERN):** *remove* the `PLANNING.md` and `TASK.md` lines rather than create empty stubs — these documents are referenced by global CLAUDE.md as project-specific files that don't currently apply to IronClaude. Replace the project-structure block's three-line listing with `KNOWLEDGE.md` only, and remove the corresponding two lines from the "Key Documentation Files" section. If a future contributor needs PLANNING/TASK, they can re-add at that time. (Sourced from FR-L2.5.)
- **D1.3** — Append `.claude/skills/*-workspace/` to `.gitignore` so any future misplacement does not get committed even if every other layer fails. (Sourced from FR-L2.6.)

**Risk Assessment**: Negligible. Pure docs/config edits; no runtime behavior changed.

## M2 — Detection Gate (Priority-0)

**Objective**: Convert the existing-but-dormant detection logic into an enforcing CI gate. Closes INV-002 HIGH-severity unaddressed invariant.

**Deliverables**:

- **D2.1** — Replace `Makefile:179-187` misleading `"MISSING in src/superclaude/skills/: <name> (not distributable!)"` with a context-aware variant. When the missing entry has no SKILL.md, emit: *"<name> has no SKILL.md — not a skill, must not live in .claude/skills/. Move to .dev/eval-workspaces/<name>/."* (Sourced from FR-L2.1.)
- **D2.2** — Add `*-workspace` suffix blocklist to either `verify-sync` or `lint-architecture` target. Explicit message: *"Workspace directories belong under `.dev/eval-workspaces/`, not `.claude/skills/`."* (Sourced from FR-L2.3.)
- **D2.3** — Wire `make verify-sync` and `make lint-architecture` into `.github/workflows/quick-check.yml`. PRs fail on drift before merge. (Sourced from FR-L2.2 — **INV-002 HIGH**.)

**Sequencing within M2**: D2.1 → D2.2 → D2.3. The CI gate (D2.3) flips on last so that the first PR-blocking failure exhibits the correct message and blocklist.

**Risk Assessment**: R-02 (Low/Low — `verify-sync` runs in seconds).

## M3 — Occurrence Prevention

**Objective**: Stop the misplacement at write time without depending on Claude obedience.

**Deliverables**:

- **D3.1** — Add PreToolUse hook in `.claude/settings.json` rejecting `Write`/`Edit` to `.claude/skills/*-workspace/**`. **Semantics (resolves self-review Q3 ambiguity):** the hook is a *reject-with-redirect* — it blocks the write and emits a deny-decision error whose message names the correct destination `.dev/eval-workspaces/<skill-name>/<remainder>`. It does NOT transparently rewrite the path (Claude Code hooks don't transparently mutate tool arguments; they emit a deny+message and Claude retries with the corrected path). Thesis L1.1 wording "rewrites the path" should be interpreted as "names the correct path in the error message". **Pattern precision required (R-01)**: must match only `.claude/skills/*-workspace/**` (directory suffix `-workspace`), NOT `.claude/skills/<skill>/<file>.md` files nor `.claude/skills/<skill>/workspace.md` single-file paths. (Sourced from FR-L1.1.)
- **D3.2** — Append a CLAUDE.md addendum (project-level) explicitly overriding skill-creator's "sibling to skill directory" convention. Names the override and the destination. Cites *behavior* not file path (mitigates R-04). (Sourced from FR-L1.2.)
- **D3.3** — Add `make eval-skill SKILL=<name>` target that creates `.dev/eval-workspaces/<name>/` and prints the absolute path for use as workspace root. (Sourced from FR-L1.3.)

**Risk Assessment**: R-01 (Medium/High — hook precision). Mitigation per merged-thesis §Risk Register: positive (skill file edit) + negative (workspace write) test cases mandatory.

## M4 — Defense in Depth (parallel-eligible)

**Objective**: Skill-level guard for the unlikely case that a future workflow routes a `.claude/skills/...` value through `sc-release-split-protocol --output` directly, bypassing both L1 and L2.

**Deliverables**:

- **D4.1** — Add output-path policy guard in `src/superclaude/skills/sc-release-split-protocol/SKILL.md` Prerequisites step 2a. Refuse `--output` paths under `.claude/skills/`, `.claude/agents/`, `.claude/commands/`. Document policy in `src/superclaude/commands/release-split.md` Options table. Run `make sync-dev` after. (Sourced from FR-L3.1.)
- **D4.2** *(status: optional, deferred-pending-capacity)* — Apply the same guard to `sc-adversarial-protocol` and `sc-cleanup-audit-protocol` SKILL.md files for consistency. Defer until M1-M5 ship. Excluded from sprint critical path; if not done, release still ships. (Sourced from FR-L3.2.)

**Risk Assessment**: Negligible. Pure skill content; verified by `make verify-sync` (which is itself the M2 deliverable — modest dependency loop only if M4 starts before M2 lands).

## M5 — Acceptance Validation

**Objective**: End-to-end exercise of the layered defense against the 5 acceptance criteria.

**Deliverables**:

- **D5.1** — AC1 test: simulate a good-faith author invoking `skill-creator` against an IronClaude skill in a clone with all M1-M3 changes installed. Verify Claude reads project CLAUDE.md addendum and writes to `.dev/eval-workspaces/<name>/`. If addendum is ignored, verify the PreToolUse hook blocks the write with the redirect-pointing error.
- **D5.2** — AC2 test: simulate a fresh clone without hooks installed (i.e., L1 bypassed). Create a `.claude/skills/<X>-workspace/` directory without SKILL.md. Verify `make verify-sync` flags it with the correct M2 error message, and CI blocks the PR.
- **D5.3** — AC3 test: invoke `sc-release-split-protocol --output .claude/skills/foo/` (or equivalent `.claude/agents/`, `.claude/commands/`). Verify the skill refuses (L3.1) before writing any artifacts.
- **D5.4** — AC4 test: assert all CLAUDE.md doc pointers resolve. `grep -E 'PLANNING\.md|TASK\.md|KNOWLEDGE\.md' CLAUDE.md` returns lines whose referenced files exist (post-D1.2 decision).
- **D5.5** — AC5 test: run `aggregate_benchmark.py` and `generate_review.py` against `.dev/eval-workspaces/sc-release-split-protocol/`. Verify no regression (both scripts accept positional paths per merged-thesis §Acceptance).

**Risk Assessment**: Discovery risk — if M5 surfaces gaps, loop back to M2/M3 with a revised fix. No production impact (validation-only milestone).

## Risk Register

| ID | Risk | Layer | Likelihood | Impact | Mitigation |
|---|---|---|---|---|---|
| R-01 | PreToolUse hook breaks legitimate `.claude/skills/<skill>/` writes | M3 | Medium | High (dev friction) | Pattern must match `*-workspace/**` precisely. M3 includes positive + negative test cases. |
| R-02 | CI wiring lengthens PR time | M2 | Low | Low | `make verify-sync` runs in seconds; concurrent with existing checks |
| R-03 | `.dev/eval-workspaces/` convention diverges from `.dev/releases/complete/v2.15-cli-portify/` prior art | M1 | Resolved | Medium | D1.1 (`.dev/README.md`) explicitly documents new rule; forward-only; prior workspace stays put |
| R-04 | skill-creator plugin updates upstream → L167 reference goes stale | M3 | Low | Low | D3.2 cites behavior ("sibling-workspace convention") not file path |
| R-05 | Future skill *should* legitimately have a workspace inside `.claude/` | M3, M2 | Very Low | Low | Hook + Makefile checks emit override-able errors; future reviewer can suppress with documented intent |

## Decision Summary

| Decision | Source | Rationale |
|---|---|---|
| Adopt RCA #2 as proximate cause + RCA #3 as systemic cause | merged-thesis §"Per-RCA Final Weighted Scores" | Already adversarially merged; no re-litigation |
| Phase ordering driven by INV-002 priority (M2 before M3) | merged-thesis §"Required Next Action" | M2.D2.3 turns existing detection logic from opt-in to enforcing; biggest leverage per LOC |
| M4 marked parallel-eligible | DEP-004 | Skill content edits don't depend on hook/CI chain |
| L3.2 (sibling skills) marked optional | merged-thesis §L3.2 | Defense-in-depth generalization; ship only if capacity allows |
| Template = inline (quality-derived) | Wave 2 template scoring | No exact remediation template; quality (0.85) wins on metrics + governance fit |
| Output directory overridden to `roadmap/` subdir of release dir | Wave 0 collision-avoidance | Default would have placed roadmap as sibling of the spec, breaking the release-folder containment convention |
| `PLANNING.md`/`TASK.md` references will be REMOVED from CLAUDE.md (not restored) | D1.2 pre-decision | Files don't exist; restoring empty stubs is worse than removing dangling references. KNOWLEDGE.md stays. |
| D3.1 hook semantics = reject-with-redirect-message (not transparent path rewrite) | D3.1 pre-decision | Matches Claude Code hook contract: hooks emit deny + explanatory message, Claude re-attempts with corrected path. |
| M2 ordered behind M1 despite thesis "L2.2 ships first" guidance | Self-review Q2 trade-off | M1 is S-effort docs; pushing M2's INV-002 closure 1 day later is acceptable given M1's error-message dependency (DEP-001). M2 retains P0 marking. |

## Success Criteria

- **SC-001** — All 5 acceptance criteria (AC1–AC5 in extraction.md) pass via M5 deliverables.
- **SC-002** — CI demonstrably blocks a synthetic PR that introduces `.claude/skills/<X>-workspace/` with no SKILL.md (verified via M5.D5.2).
- **SC-003** — `superclaude install` from a fresh clone produces a clean install with zero `*-workspace/` directories inside `.claude/skills/`.
- **SC-004** — `grep -E 'PLANNING\.md|TASK\.md|KNOWLEDGE\.md' CLAUDE.md` returns only references to files that exist on disk.
- **SC-005** — `make verify-sync` exits clean immediately after `make sync-dev` on a freshly merged branch (no drift introduced by the remediation itself).

## Predecessors

- `.dev/releases/current/release-split-workspace-rca/merged-thesis.md` (authoritative spec, adversarially merged)
- `.dev/releases/current/release-split-workspace-rca/rca-1-skill-spec.md` (defensive guard derivation)
- `.dev/releases/current/release-split-workspace-rca/rca-2-eval-harness.md` (proximate cause derivation, base variant)
- `.dev/releases/current/release-split-workspace-rca/rca-3-naming-convention.md` (systemic cause derivation)
- `.dev/releases/current/release-split-workspace-rca/adversarial/refactor-plan.md` (L1/L2/L3 action enumeration)
- `.dev/releases/current/release-split-workspace-rca/adversarial/invariant-probe.md` (INV-002 driving M2 priority)

## Next Step

Run `/sc:tasklist` against this `roadmap.md` to produce a Sprint CLI-compatible tasklist bundle (`phase-N-tasklist.md` per milestone + `tasklist-index.md`). The bundle can then be executed by `superclaude sprint run <tasklist-index.md>`.
