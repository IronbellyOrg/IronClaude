# D-0014: Per-Phase Loading Declarations at Stage A.7

## Task
T03.02 — Add per-phase loading declarations at Stage A.7

## What Was Done
Added a loading declaration block to the `### A.7: Build the Task File` section in `src/superclaude/skills/prd/SKILL.md`, distinguishing orchestrator loading from builder subagent loading.

### Loading Declarations Added (lines 346-353)

**Orchestrator loads:**
- `refs/build-request-template.md` — BUILD_REQUEST format and variable reference block

**Builder subagent loads** (referenced within BUILD_REQUEST):
- `refs/agent-prompts.md` — agent prompt templates for Phase 2 items
- `refs/synthesis-mapping.md` — template section mapping for Phase 5 items
- `refs/validation-checklists.md` — validation criteria for Phase 3, 5, 6 items

**Context budget note:** Orchestrator loads at most 2 refs simultaneously (SKILL.md + `refs/build-request-template.md`), satisfying NFR-PRD-R.2.

## Verification

### Acceptance Criteria Check

1. **Stage A.7 contains loading declaration block** — PASS
   - Two `**Refs Loaded**` blocks at lines 346 and 348, clearly separating orchestrator vs builder loading

2. **No other phases contain refs/ loading declarations** — PASS
   - `grep 'Refs Loaded' src/superclaude/skills/prd/SKILL.md` returns only lines 346 and 348 (both in A.7)
   - `grep 'Read.*refs/\|Load.*refs/' src/superclaude/skills/prd/SKILL.md` returns only A.7 lines

3. **Orchestrator context loads at most 2 refs simultaneously** — PASS
   - Explicitly stated: "SKILL.md + `refs/build-request-template.md`"

### Pattern Conformance
Loading declaration format follows the `**Refs Loaded**:` pattern established by `sc-roadmap-protocol/SKILL.md` (FR-PRD-R.6).

## Notes
- `.claude/skills/prd/SKILL.md` write was blocked by permissions; edit applied to `src/superclaude/skills/prd/SKILL.md` (source of truth). Run `make sync-dev` to propagate.
- `refs/build-request-template.md` does not yet exist in refs/ — it is expected to be created by a prior Phase 2 task (T02.01, extracting block B11).
