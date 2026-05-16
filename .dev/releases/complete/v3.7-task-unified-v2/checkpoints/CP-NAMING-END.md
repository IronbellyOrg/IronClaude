# Checkpoint: End of Naming Consolidation

**Checkpoint ID:** CP-NAMING-END
**Release:** v3.7-task-unified-v2
**Phase:** Naming Consolidation (Spec §3.3 + §4.3)
**Status:** PASS
**Timestamp (UTC):** 2026-04-22

## Scope

Three-layer naming collision resolved. Per spec §3.3:

| Component | Before | After |
|---|---|---|
| User-facing command | `/sc:task` OR `/sc:task-unified` (ambiguous) | `/sc:task` (canonical) |
| Command file | `task-unified.md` (frontmatter `name: task`) | `task.md` |
| Legacy command file | `task.md` (frontmatter `name: task-legacy`, deprecated) | **deleted** |
| Skill directory | `sc-task-unified-protocol/` | `sc-task-protocol/` |
| Skill frontmatter | `sc:task-unified-protocol` | `sc:task-protocol` |
| Sprint CLI prompt | `/sc:task-unified` (hardcoded) | `/sc:task` |

All live-source references (src/ + .claude/) to the old names have
been eliminated. The `.claude/settings.local.json` keeps an old sed
command pattern inside a permission rule — left untouched because it
is gitignored user state.

Dependency order followed per spec §4.3: **N1 → N2 → N3 → N4 → (N5 ‖
N6) → (N7 ‖ N8 ‖ N9 ‖ N10) → N11**.

## Files Changed

### Deleted

| Path | Reason |
|---|---|
| `src/superclaude/commands/task.md` | Deprecated `task-legacy` command, superseded by the renamed `task-unified.md` |
| `.claude/commands/sc/task.md` | Stale dev copy of the legacy command |
| `.claude/commands/sc/task-unified.md` | Stale dev copy — the renamed file lives at `.claude/commands/sc/task.md` now |
| `.claude/skills/sc-task-unified-protocol/SKILL.md` | Stale dev copy — the renamed skill lives at `.claude/skills/sc-task-protocol/` |

### Renamed

| From | To | Notes |
|---|---|---|
| `src/superclaude/commands/task-unified.md` | `src/superclaude/commands/task.md` | Frontmatter `name: task` unchanged |
| `src/superclaude/skills/sc-task-unified-protocol/` | `src/superclaude/skills/sc-task-protocol/` | Directory rename via `git mv` |

### Modified (reference updates)

| File | Changes |
|---|---|
| `src/superclaude/skills/sc-task-protocol/SKILL.md` | Frontmatter `name:` + 1 heading updated |
| `src/superclaude/skills/sc-task-protocol/__init__.py` | 1 comment line |
| `src/superclaude/cli/sprint/process.py` | `build_prompt()` docstring + the actual prompt at line 170 (`/sc:task-unified` → `/sc:task`) |
| `src/superclaude/cli/cleanup_audit/prompts.py` | 5 prompt builder strings (N6) |
| `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` | 12 references across Stages 1-9 + descriptions (N7) |
| `src/superclaude/commands/validate-tests.md` | 3 references (path hints + skill path) |
| `src/superclaude/commands/task-mcp.md` | 1 migration notice reference |
| `src/superclaude/commands/task.md` | 1 internal skill invocation example (`Skill sc:task-protocol`) |
| `src/superclaude/skills/sc-validate-tests-protocol/SKILL.md` | 7 test-path and description references |
| `src/superclaude/skills/sc-roadmap-protocol/SKILL.md` | 1 pipeline-position reference |
| `src/superclaude/skills/sc-cli-portify-protocol/refs/code-templates.md` | 1 code-template comment |
| `tests/sprint/test_process.py` | `test_build_prompt_contains_task_unified` → `test_build_prompt_contains_task_command`; asserts `/sc:task ` prefix and absence of `/sc:task-unified` |

### Dev copies propagated

Ran `make sync-dev` to regenerate `.claude/skills/sc-task-protocol/`,
`.claude/commands/sc/task.md`, and the other touched dev copies from
their src counterparts.

## Verification

### Spec §4.3 acceptance criteria

| Acceptance criterion | Result |
|---|---|
| N1 — `task-legacy` file deleted (src + .claude) | PASS |
| N2 — `task-unified.md` → `task.md` with frontmatter `name: task` unchanged | PASS |
| N3 — `sc-task-unified-protocol/` → `sc-task-protocol/` | PASS |
| N4 — skill frontmatter `name: sc:task-protocol` | PASS |
| N5 — `process.py` emits `/sc:task` (2 refs updated, 0 remaining) | PASS |
| N6 — `cleanup_audit/prompts.py` all 5 builders emit `/sc:task` | PASS |
| N7 — `sc-tasklist-protocol/SKILL.md` 0 remaining `sc:task-unified` refs | PASS (12 → 0) |
| N8 — `tasklist.md`/`help.md`/other command refs | PASS (handled via the same sweep; no refs were present in tasklist.md/help.md) |
| N9 — cross-protocol refs in `sc-roadmap-protocol`, `sc-cli-portify-protocol`, `sc-validate-tests-protocol` | PASS |
| N10 — core docs (`COMMANDS.md`, `ORCHESTRATOR.md`) | PASS (no refs were present) |
| N11 — `make sync-dev` passes and dev copies updated | PASS |
| N12 — `task-mcp.md` deprecation status confirmed | PASS (kept; migration notice now points to `/sc:task`) |
| Grep `sc:task-unified\|sc-task-unified\|/sc:task-unified` returns 0 hits in `src/superclaude/` and `.claude/` | PASS |
| `/sc:task` smoke path: `ClaudeProcess.build_prompt()` starts with `/sc:task ` | PASS (`test_build_prompt_contains_task_command`) |

### Regression Status

| Suite | Before Naming | After Naming |
|---|---|---|
| Full `tests/sprint/` | 921 passed, 57 failed | 921 passed, 57 failed |
| Regressions | — | 0 |

The one test that broke during the rename
(`test_build_prompt_contains_task_unified`) was a characterization
test of the old prompt string; it was renamed to
`test_build_prompt_contains_task_command` and now asserts the new
`/sc:task` contract.

## Cross-wave concerns

- **Checkpoint Wave 1** (Prompt-level Enforcement) — already
  modified `build_prompt()` to add the `## Checkpoints` section; the
  N5 rename changes a different line (the leading command invocation)
  so there is no conflict. Both changes coexist cleanly.
- **TUI v2 Waves 1-4** — none of those waves depend on the command
  surface; the rename is invisible to the display layer. No test
  adjustments needed.
- **Checkpoint Wave 4 / Tasklist Protocol** — the spec flagged a
  potential SKILL.md conflict between "Naming N7" and Checkpoint
  Wave 4 (§5.5). Checkpoint Wave 4 already landed (`8eba113`) before
  this rename; the merge here simply replaces `sc:task-unified`
  everywhere it still appeared in `sc-tasklist-protocol/SKILL.md`
  without touching the checkpoint-generation rules.

## Open items

- `.claude/settings.local.json` still references `sc-task-unified`
  inside a permission rule (a sed command pattern). Left alone — this
  file is user-local and gitignored; new users will never see it.
- `.venv/lib/python3.12/site-packages/superclaude/_src/...` retains
  old directory names because it is the installed editable copy. A
  `make dev` (or `uv pip install -e .`) re-install will repopulate
  with the canonical names.
- Historical artifacts under `.dev/releases/complete/` retain the
  old names intentionally — archival.

## Next steps

With this commit the v3.7-task-unified-v2 release hits every item on
the §6.2 Recommended Implementation Order:

1. ✅ Naming Consolidation (this checkpoint)
2. ✅ Checkpoint W1 (`183f8f8`)
3. ✅ TUI v2 Core — Waves 1+2 (`430a1c9`, `3e293c4`)
4. ✅ Checkpoint W2 (`2a60667`)
5. ✅ TUI v2 Summary — Waves 3+4 (`5115dfa`, `08addac`)
6. ✅ Checkpoint W3 (`965213b`)
7. ✅ Checkpoint W4 (`8eba113`; originally flagged as "deferred to
   next cycle" but shipped on this branch — release-manager decision
   outstanding)

**Source**: `v3.7-UNIFIED-RELEASE-SPEC-merged.md` §3.3, §4.3, §5.5,
§6.2; `clickup-tasks.md` Phase 1 task list N1-N12.
