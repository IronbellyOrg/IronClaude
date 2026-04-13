# D-0004: Pre-Migration Baseline Snapshot

**Task:** T01.04 -- Snapshot Pre-Migration Baseline State
**Date:** 2026-04-05
**Source File:** `src/superclaude/skills/tdd/SKILL.md`
**Dependency:** T01.02 (D-0002/notes.md confirmed present)

---

## 1. Line Count (`wc -l`)

```
438 /config/workspace/IronClaude/src/superclaude/skills/tdd/SKILL.md
```

**Result:** 438 lines -- matches roadmap expectation of 438.

---

## 2. Git Diff Stat Baseline

```
 .../backlog/prd-skill-refactor/.roadmap-state.json | 31 ++++++++++++-----
 .../prd-skill-refactor/prd-refactor-spec-v2.md     |  3 +-
 .../releases/backlog/prd-skill-refactor/roadmap.md | 40 +++++++++++-----------
 .../prd-skill-refactor/wiring-verification.md      |  2 +-
 .../.roadmap-state.json                            | 29 +++++++++++-----
 .../wiring-verification.md                         |  2 +-
 .vendor/anthropic-skills                           |  0
 docs/memory/solutions_learned.jsonl                |  8 +++++
 8 files changed, 74 insertions(+), 41 deletions(-)
```

**Result:** SKILL.md has NO staged or unstaged changes -- clean baseline confirmed.

---

## 3. Verbatim Migration Block Copies

### Block A: Effective Prompt Examples (Lines 48-63)

```markdown
### Effective Prompt Examples

**Strong — all four pieces present:**
> Create a TDD for the agent orchestration system. The PRD is at `docs/docs-product/tech/agents/PRD_AGENT_SYSTEM.md`. Focus on `backend/app/agents/`, `backend/app/services/agent_service.py`, and `backend/app/workers/`. Write to `docs/agents/TDD_AGENT_ORCHESTRATION.md`.

**Strong — clear scope + PRD + output type:**
> Turn the canvas roadmap PRD into a TDD. The PRD is at `docs/docs-product/tech/canvas/PRD_ROADMAP_CANVAS.md`. I need a Standard-tier design covering the React canvas system, dependency management, and node type architecture. Focus on `frontend/app/roadmap/`.

**Strong — design from scratch with clear scope:**
> Design the technical architecture for a shared GPU pool to replace per-session VMs. Scope: `ue_manager/`, `infrastructure/`, `backend/app/services/streaming_service.py`. This is a Heavyweight TDD — new system, cross-team impact.

**Weak — topic only (will work but produces broader, less focused results):**
> Create a TDD for the wizard.

**Weak — no context (agents won't know what to focus on):**
> Write a technical design document.
```

**Location confirmed:** Lines 48-63 (16 lines)

### Block B: Tier Selection Table (Lines 82-88)

```markdown
Match the tier to component scope. **Default to Standard** unless the component is clearly documentable with a quick scan of <5 files.

| Tier | When | Codebase Agents | Web Agents | Target Lines |
|------|------|-----------------|------------|-------------|
| **Lightweight** | Bug fixes, config changes, small features (<1 sprint), <5 relevant files | 2–3 | 0–1 | 300–600 |
| **Standard** | Most features and services (1-3 sprints), 5-20 files, moderate complexity | 4–6 | 1–2 | 800–1,400 |
| **Heavyweight** | New systems, platform changes, cross-team projects, 20+ files | 6–10+ | 2–4 | 1,400–2,200 |
```

**Location confirmed:** Lines 82-88 (7 lines)

---

## Summary

| Measurement | Expected | Actual | Status |
|---|---|---|---|
| SKILL.md line count | 438 | 438 | MATCH |
| Migration Block A location | Lines 48-63 | Lines 48-63 | MATCH |
| Migration Block B location | Lines 82-88 | Lines 82-88 | MATCH |
| SKILL.md in git diff | Not present | Not present | CLEAN |

All three baseline measurements captured. No deviations from roadmap expectations. This snapshot is ready for Phase 4 fidelity verification (T04.02-T04.06).
