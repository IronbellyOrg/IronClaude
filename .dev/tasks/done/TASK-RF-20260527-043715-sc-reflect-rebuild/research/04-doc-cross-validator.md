# Research: Doc Cross-Validator
**Topic type:** Doc Cross-Validator
**Scope:** Verify every CODE-referenced claim in merged-requirements.md against actual code state
**Status:** Complete
**Date:** 2026-05-27
---

## Methodology

For every CODE-referenced claim in `.dev/brainstorms/sc-reflect-rebuild/merged-requirements.md` (1707-line spec) — file paths, agent contracts, MCP tool surfaces, Makefile targets, env vars, hook behavior, directory existence — I independently verified against the worktree state via `ls`, `grep`, and targeted `Read`. Each claim is tagged:

- **[CODE-VERIFIED]** — confirmed at file:line
- **[CODE-CONTRADICTED]** — spec says X, code says Y (divergence described)
- **[UNVERIFIED]** — could not locate corresponding code; may be stale, planned, or external

Worktree root: `/config/workspace/IronClaude/.claude/worktrees/feat-reflect-v2`

---

## Verification Ledger

### Claim 1 — Legacy `src/superclaude/commands/reflect.md` shape

- **[CODE-VERIFIED]** — File EXISTS at `src/superclaude/commands/reflect.md`, 111 lines.
- Frontmatter (lines 1–7) confirms: `name: reflect`, `description: "Task reflection and validation using Serena MCP analysis capabilities"`, `category: special`, `complexity: standard`, `mcp-servers: [serena, context7]`, `personas: []`.
- This matches the spec's §1 description of the legacy `think_about_*` surface that the rebuild replaces.

### Claim 2 — `confidence-calibrator.md` contract (§11.3 5-dim rubric)

- **[CODE-VERIFIED]** — File EXISTS at `src/superclaude/agents/confidence-calibrator.md`, 118 lines.
- Frontmatter (lines 4–8): `name: confidence-calibrator`, `tools: Read`, `model: sonnet`, `maxTurns: 25`, `permissionMode: plan`.
- Inputs (lines 43–48): `card_path`, `rubric_path`, `card_tier`, `flags_context`, `output_path` — match §11.3 field names.
- Output Format (lines 62–93): 5-dimension table (Evidence grounding, Symptom coverage, Reproducibility fit, Fix directness, Domain coherence), Confidence section with Self-reported/Calibrated/Delta, Escalation recommendation with Verdict + Reason + Rubric rule fired.
- Model is hardcoded `sonnet`. Spec §11.3 may expect dynamic alias resolution — if so, this is a partial gap, but the agent itself is real and matches the rubric contract.

### Claim 3 — `evidence-validator.md` re-Read contract (§11.2)

- **[CODE-VERIFIED]** — File EXISTS at `src/superclaude/agents/evidence-validator.md`, 128 lines.
- Frontmatter (lines 4–8): `tools: Read, Grep, Glob`, `model: sonnet`, `maxTurns: 50`, `permissionMode: plan` — matches spec §11.2 exactly.
- `allow_command_reexec` input (line 44): "bool, whether you may re-run cited commands. Default and recommended: `false`."
- Per-citation verdicts (line 30): `verified` / `line-mismatch` / `file-missing` / `snippet-mismatch`.
- v1 always passes `false` (lines 44, 57) — confirmed.

### Claim 4 — `sc-adversarial-protocol` flag surface (§8)

- **[CODE-VERIFIED]** — File EXISTS at `src/superclaude/skills/sc-adversarial-protocol/SKILL.md`, 3002 lines.
- `--compare` (lines 26, 29, 58): Mode A invocation, comma-separated paths.
- `--depth` (line 334): default `standard`, accepts `quick/standard/deep`.
- `--focus` (line 338): comma-separated focus areas.
- `--output` (line 337): auto-derived default; subject to forbidden-prefix guard (line 41).
- All four flags reflect's Wave-3 debate references are present and behave as documented.

### Claim 5 — `task-builder` BUILD_REQUEST 15-field schema (§16)

- **[CODE-VERIFIED + partial CODE-CONTRADICTED]** — task-builder SKILL.md exists at `src/superclaude/skills/task-builder/SKILL.md`, 2190 lines.
- BUILD_REQUEST format documented inline at lines 785–910+ with fields: GOAL, WHY, TASK_ID_PREFIX, TEMPLATE, QA_GATE_REQUIREMENTS, VALIDATION_REQUIREMENTS, TESTING_REQUIREMENTS, EXECUTION_CONTEXT_REQUIREMENTS, DOCUMENTATION STALENESS WARNINGS, RESEARCH DIR, QUALITY GATE RESULTS, OPEN QUESTIONS, REMAINING GAPS, GRANULARITY REQUIREMENT, ESCALATION OVERRIDE — and explicit "M1-frozen 15-field BUILD_REQUEST" reference at line 843.
- **CONTRADICTION:** spec §16 references `refs/remediation-handoff.md` — **this file does NOT exist**. `src/superclaude/skills/task-builder/` contains ONLY `SKILL.md` (no `refs/`, `templates/`, or `scripts/` subdirs). BUILD_REQUEST schema is documented inline in SKILL.md, not in a separate `refs/` file. If reflect's spec authors expected to read `refs/remediation-handoff.md`, they will need to either inline the schema (as task-builder does) or create that ref file as part of the reflect rebuild.

### Claim 6 — `sc-troubleshoot-protocol` Wave 6 reflect references (§2)

- **[CODE-VERIFIED]** — File EXISTS at `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`, 456 lines.
- Wave 6 Phase B (line 368): `invoke /sc:reflect --type task --analyze (if available) against the new task file. If reflect flags issues, surface them; ask the user whether to refactor the tasklist or proceed as-is.`
- Wave 6 Phase D (line 370): `invoke /sc:reflect --type task --validate (or self-review agent as fallback) before the user commits.`
- Cross-skill matrix (line 387): `Skill sc:adversarial-protocol`, `task-builder`, `/sc:reflect`.
- Auto-commit gate (line 413): `/sc:reflect --type task --validate` is the final gate.
- **Real integration today**, NOT aspirational — but current code invokes via `/sc:reflect` slash form, not `Skill sc-reflect`. If the rebuild replaces the slash command with skill invocation, these references must be updated in lockstep (parallel sc-troubleshoot update required).

### Claim 7 — `sc-task-protocol` end-of-task reflect hook (§2)

- **[CODE-CONTRADICTED]** — File EXISTS at `src/superclaude/skills/sc-task-protocol/SKILL.md`, 396 lines.
- Only one match for "reflect" across the entire file: line 303 — `3. think_about_task_adherence: Reflect on completeness` — this is a legacy serena `think_about_*` reference, NOT a `/sc:reflect` or `Skill sc-reflect` invocation.
- There is NO end-of-task hook invoking the reflect skill in sc-task-protocol today. The spec's §2 claim of an end-of-task reflect integration is aspirational: it will require a new edit to sc-task-protocol's task-completion logic as part of (or alongside) the reflect rebuild.

### Claim 8 — `02_mdtm_template_complex_task.md`

- **[CODE-VERIFIED]** — File EXISTS at `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md`, 1204 lines.
- Referenced indirectly via spec §16 for task-template selection — template is real.

### Claim 9 — Agent file inventory

All files EXIST with confirmed line counts:

- **[CODE-VERIFIED]** `root-cause-analyst.md` — 56 lines
- **[CODE-VERIFIED]** `self-review.md` — 37 lines
- **[CODE-VERIFIED]** `requirements-analyst.md` — 56 lines
- **[CODE-VERIFIED]** `audit-validator.md` — 145 lines
- **[CODE-VERIFIED]** `socratic-mentor.md` — 310 lines
- **[CODE-VERIFIED]** `rf-qa.md` — 552 lines
- **[CODE-VERIFIED]** `rf-qa-qualitative.md` — 1139 lines

### Claim 10 — `.dev/tasks/to-do/` + `.dev/tasks/done/` (promotion `task` adapter, §14.5.1)

- **[CODE-VERIFIED]** — Both directories EXIST in the worktree.

### Claim 11 — `.dev/releases/current/` + `.dev/releases/complete/` (promotion `sprint-release` adapter, §14.5.1)

- **[CODE-VERIFIED]** — Both directories EXIST in the worktree.

### Claim 12 — Eval workspace structure for sc-brainstorm + sc-troubleshoot (§13.1, §13.2)

- **[CODE-VERIFIED with one gap]** Both workspaces EXIST under `.dev/eval-workspaces/`.
- `.dev/eval-workspaces/sc-brainstorm/` contains: `SPEC.md`, `evals/evals.json`, `iterations/`, `grader.py`, `aggregate_iteration.py`, `skill-snapshot/brainstorm-v1.md`.
- `.dev/eval-workspaces/sc-troubleshoot/` contains: `agent-design.md`, `evals/`, `forensic-analysis/`, `iteration-1/`, `iteration-2/`, `iteration-3/`, `skill-snapshot/`, `meta-eval-test-is-wrong/`, `phase4-5-errors-20260521202240/`.
- **GAP** — spec mentions `eval-viewer/generate_review.py`; this file does NOT exist in either workspace (`find ... -name generate_review.py` returns empty). If the reflect spec relies on an eval-viewer harness, it must be authored fresh or the reference dropped.
- **GAP** — sc-troubleshoot workspace has NO `SPEC.md`, `grader.py`, or `aggregate_iteration.py` at top level (different layout from sc-brainstorm). The spec §13.2 should not assume parity with §13.1's layout.

### Claim 13 — Makefile targets referenced in §17.5

- **[CODE-CONTRADICTED]** — `make dev` does NOT exist as a Makefile target.
  - Actual targets present: `install`, `test`, `test-plugin`, `doctor`, `verify`, `lint`, `format`, `clean`, `build-plugin`, `sync-plugin-repo`, `translate`, `sync-dev`, `verify-sync`, `verify-deps`, `lint-architecture`, `eval-skill`, `help`, `uninstall-legacy`.
  - The project's CLAUDE.md and global SuperClaude CLAUDE.md both reference `make dev` (Install editable + dev deps); the actual Makefile uses `make install` for that role. Reflect spec authors should refer to `make install` (or `make verify` for the post-install check), not `make dev`.
- **[CODE-VERIFIED]** — `test`, `lint`, `format`, `sync-dev`, `verify-sync`, `verify`, `doctor`, `build-plugin` all EXIST.

### Claim 14 — `.claude/settings.json` PreToolUse hook for `*-workspace`

- **[CODE-VERIFIED]** — Hook is present in `.claude/settings.json` at line 6.
- Verbatim description: "Reject-with-redirect: writes to `.claude/skills/*-workspace/**` are denied with a message naming the correct destination `.dev/eval-workspaces/<skill>/<remainder>`. Semantics are deny + explanatory message (Claude Code hooks do not transparently rewrite paths) — Claude is expected to retry against the redirected path. Source: phase-3-tasklist.md T03.01, FR-L1.1, R-007. Pattern precision (R-01): only `<...>/.claude/skills/<X>-workspace/<remainder>` matches; `.claude/skills/<X>/workspace.md` and `.claude/skills/<X>/file.md` are NOT affected."
- Hook script: `$CLAUDE_PROJECT_DIR/.claude/hooks/reject-workspace-writes.sh`, timeout 3s.

### Claim 15 — `.gitignore` matches `.claude/skills/*-workspace/`

- **[CODE-VERIFIED]** — `.gitignore` line 206: `.claude/skills/*-workspace/`.
- Also line 117 (`.claude/`) and line 118 (`!.claude/settings.json`) corroborate the CLAUDE.md "only settings.json is tracked" rule.

### Claim 16 — `pyproject.toml` skill-creator hook reference

- **[UNVERIFIED]** — `grep -i "skill-creator\|skill_creator" pyproject.toml` returns no matches. The skill-creator plugin is referenced in the project-level CLAUDE.md "Plugin Override" section but pyproject.toml itself has no dependency on it. The plugin is **external** (installed separately, not part of this repo's package metadata). Spec §13.1 / §13.2 should treat skill-creator as an external tool, not a pyproject dep.

### Claim 17 — `ANTHROPIC_DEFAULT_*_MODEL` env var convention

- **[CODE-VERIFIED]** — Only ONE existing skill references these env vars: `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:109` — "Validate model aliases: check env vars `ANTHROPIC_DEFAULT_OPUS_MODEL`, `ANTHROPIC_DEFAULT_SONNET_MODEL`, `ANTHROPIC_DEFAULT_HAIKU_MODEL` are set. If `--models` provided, validate each alias resolves to one of the known aliases."
- **Convention is precedented but thin**. Spec §4 Wave 0 step 0.5 alias resolution can follow this exact pattern for consistency. No other skill validates these vars yet.

### Claim 18 — Serena memory tools in skill `allowed-tools`

- **[CODE-VERIFIED but minimal precedent]** — `mcp__serena__read_memory` / `write_memory` / `list_memories` appear in only ONE skill: `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md`.
- Reflect's frontmatter convention (declaring these in `allowed-tools`) will be consistent with sc-validate-roadmap-protocol's precedent — a thin but valid convention.

### Claim 19 — `mcp__sequential-thinking__sequentialthinking` in other skills

- **[CODE-VERIFIED but thin]** — Only ONE skill references this tool: `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`.
- Reflect using it would be consistent precedent.

### Claim 20 — `mcp__context7__resolve-library-id` / `query-docs`

- **[CODE-VERIFIED but thin]** — Only ONE skill references these: `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`.
- Reflect using context7 tools would be consistent precedent.

### Claim 21 — `refs/escalation-rubric.md` (sc-troubleshoot, spec line 467)

- **[CODE-VERIFIED]** — File EXISTS at `src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md`, 52 lines. Spec citation is accurate.

### Claim 22 — `sc-brainstorm-protocol/SKILL.md:280-285` empty-response handling (§8)

- **[CODE-VERIFIED]** — Lines 280–285 contain exactly the empty-response guard the spec quotes:
  - L280: `Invoke: Skill sc-adversarial-protocol with above arguments...`
  - L282: `Consume return contract...`
  - L284: `Empty-response guard: If response is empty or has no parseable structure → FAIL Wave 3 (no synthetic 0.5 fallback). Emit: "Adversarial returned empty response — invocation likely failed at transport. See sc:adversarial logs."`
- Spec citation is accurate and quotable.

### Claim 23 — `evidence-validator.md:21` ("find unfounded citations, not to confirm absence")

- **[CODE-VERIFIED]** — Line 21 contains: `You are the last gate between a draft report and the user. Your job is to find unfounded citations, not to confirm absence of them. A pass that drops zero items is suspect...`
- Spec citation is accurate.

---

## Summary

### [CODE-CONTRADICTED] — DO NOT build task items on these

1. **Claim 5 (partial):** `src/superclaude/skills/task-builder/refs/remediation-handoff.md` does NOT exist. task-builder has only a single `SKILL.md` (no `refs/` dir). If the reflect spec assumes a separate handoff ref, that file must be created or the schema inlined.
2. **Claim 7:** `sc-task-protocol` has NO `/sc:reflect` or `Skill sc-reflect` integration today — only a legacy serena `think_about_task_adherence` reference on line 303. The spec §2 "end-of-task reflect hook" is aspirational; building it requires a parallel edit to `src/superclaude/skills/sc-task-protocol/SKILL.md`.
3. **Claim 13:** `make dev` does NOT exist as a Makefile target. The CLAUDE.md docs are stale on this point — actual target is `make install` for editable+dev install. Any task item that runs `make dev` will fail.

### [UNVERIFIED] — Treat as external or planned

1. **Claim 12 partial:** `eval-viewer/generate_review.py` is not present in either eval workspace. If reflect's spec depends on it for review rendering, the harness needs to be authored from scratch.
2. **Claim 12 partial:** sc-troubleshoot eval workspace does NOT mirror sc-brainstorm's layout (no `SPEC.md`/`grader.py`/`aggregate_iteration.py` at top level). Cross-workspace parity is not a safe assumption.
3. **Claim 16:** `skill-creator` plugin is not declared in `pyproject.toml`. It is external tooling; the reflect rebuild cannot assume it's installable via the project's package metadata.

### [CODE-VERIFIED] — Safe to build on

Claims 1, 2, 3, 4, 5 (BUILD_REQUEST schema inline), 6 (sc-troubleshoot reflect refs), 8, 9 (all 7 agents), 10, 11, 14, 15, 17 (env var convention), 18 (serena memory tools), 19 (sequential-thinking), 20 (context7 tools), 21, 22, 23.

### Caveats for the builder

- **Sc-troubleshoot integration (claim 6) is real today, but uses slash form `/sc:reflect`, not `Skill sc-reflect`.** If the rebuild switches reflect to skill-only invocation, the sc-troubleshoot Wave 6 Phase B/D + matrix (line 387) + auto-commit gate (line 413) must be updated in lockstep, or both invocation forms must remain supported.
- **Confidence-calibrator model is hardcoded `sonnet` (claim 2).** If reflect spec §11.3 expects dynamic alias resolution, that's an enhancement, not a refactor.
- **MCP tool conventions (claims 18, 19, 20) are precedented but thin** — only 1 skill each. Reflect using them is consistent but introduces a stronger pattern.
- **Promotion adapter directories all exist (claims 10, 11).** Building on `.dev/tasks/{to-do,done}/` and `.dev/releases/{current,complete}/` is safe.
