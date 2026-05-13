# Phase 3 -- hooks.json registration + CLAUDE.md

Phase goal: register the 7 freshness handlers in `src/superclaude/hooks/hooks.json` (auto-distributed by Phase 4's `install_hooks.py`) and append the behavioral discipline section to `src/superclaude/core/CLAUDE.md` (auto-distributed by existing `install_core_files`). Two tasks; the system is now "specified" in source but not yet "installed."

---

### T03.01 -- Merge 7 freshness registrations into hooks.json

| Field | Value |
|---|---|
| Roadmap Item IDs | R-010 |
| Why | `install_hooks.py` (Phase 4) will read this file and merge it into the user's `~/.claude/settings.json`. The 7 freshness hooks must be registered here for distribution. Plugins mirror must stay in sync. |
| Effort | S | Risk | High | Risk Drivers | malformed JSON breaks all hooks; wrong matcher misroutes events; one wrong path → ENOENT silently |
| Tier | STRICT | Confidence | `[█████████-] 90%` | Requires Confirmation | No | Critical Path Override | Yes |
| Verification Method | Sub-agent quality-engineer review + jq schema validation |
| MCP Requirements | Required: Sequential, Serena | Fallback Allowed | No | Sub-Agent Delegation | Required |
| Deliverable IDs | D-0010 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0010/{spec.md, before.json, after.json, diff.md, jq-validation.txt, evidence.md}`

**Deliverables:**
- `src/superclaude/hooks/hooks.json` with 7 new event registrations merged into existing `hooks` key (existing SessionStart entry preserved)
- `plugins/superclaude/hooks/hooks.json` mirror in sync

**Steps:**
1. **[PLANNING]** Read `InfraDocs:phase5.1-context-refresh-design.md` §5 for canonical JSON shape.
2. **[PLANNING]** Backup current hooks.json to `before.json`.
3. **[EXECUTION]** Merge new registrations into the `hooks` object. The existing SessionStart entry stays; new entry appended to SessionStart's array (NOT replacing). Add new event keys (UserPromptSubmit, PreToolUse, PostToolUse, FileChanged, SubagentStart, SubagentStop) with their respective matcher/handler shapes per design §5.
4. **[EXECUTION]** Use `~/.claude/hooks/freshness-X.sh` for all command paths (per NFR-6; never `$HOME` or relative).
5. **[EXECUTION]** Set `async: true` on PostToolUse(Read), FileChanged, SubagentStart, SubagentStop.
6. **[EXECUTION]** Apply same edit to `plugins/superclaude/hooks/hooks.json`.
7. **[VERIFICATION]** `jq . src/superclaude/hooks/hooks.json` exits 0.
8. **[VERIFICATION]** `jq -r '.hooks | keys[]' src/superclaude/hooks/hooks.json` lists: SessionStart, UserPromptSubmit, PreToolUse, PostToolUse, FileChanged, SubagentStart, SubagentStop.
9. **[VERIFICATION]** `diff src/superclaude/hooks/hooks.json plugins/superclaude/hooks/hooks.json` returns clean.
10. **[VERIFICATION]** `grep -F '$HOME' src/superclaude/hooks/hooks.json plugins/superclaude/hooks/hooks.json` returns nothing.
11. **[VERIFICATION]** Sub-agent review of diff: NFR-6/7/9/10/12 compliance, async flag placement, matcher form (exact-pipe for Edit-class list).

**Acceptance Criteria:**
- `after.json` is valid JSON (`jq . after.json` exit 0; output captured to jq-validation.txt).
- `diff.md` shows 7 added event registrations, no unrelated modifications.
- No `$HOME` reference anywhere in either hooks.json.
- All hook command paths use `~/.claude/hooks/...` form.
- Sub-agent report confirms NFR compliance.

**Validation:** Manual jq queries per step 8. **Evidence:** before/after/diff/jq-validation + sub-agent report.

**Dependencies:** T01.01 (existing session-init path already cleaned)
**Rollback:** Restore both hooks.json files from `before.json`.
**Notes:** This is a SOURCE edit, not a live install. The user's `~/.claude/settings.json` is untouched until Phase 5.

---

### T03.02 -- Append Context Freshness Discipline section to core/CLAUDE.md

| Field | Value |
|---|---|
| Roadmap Item IDs | R-011 |
| Why | Self-discipline layer for chat-only citations where no tool call fires (Q3 resolution). Auto-distributes via existing `install_core_files` — no new install code needed. |
| Effort | S | Risk | Low | Risk Drivers | markdown only; no system impact beyond Claude behavior |
| Tier | STANDARD | Confidence | `[█████████-] 95%` | Requires Confirmation | No | Critical Path Override | No |
| Verification Method | Manual diff + wc -w check |
| MCP Requirements | Preferred: Sequential | Fallback Allowed | Yes | Sub-Agent Delegation | None |
| Deliverable IDs | D-0011 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0011/{spec.md, before.md, after.md, diff.md}`

**Deliverables:**
- `src/superclaude/core/CLAUDE.md` with new section `## Context freshness discipline` appended, body verbatim from `InfraDocs:phase5.1-context-refresh-design.md` §4

**Steps:**
1. **[PLANNING]** Read design §4 wording.
2. **[PLANNING]** Backup `src/superclaude/core/CLAUDE.md` to `before.md`.
3. **[PLANNING]** Confirm no existing `## Context freshness discipline` heading present.
4. **[EXECUTION]** Append the section from design §4 verbatim at end of file.
5. **[VERIFICATION]** Diff is a pure append.
6. **[VERIFICATION]** Section uses factual phrasing for the self-check (per Q3: "Did I Read..." not "Always re-read...").
7. **[VERIFICATION]** Section word count ≤350 words.

**Acceptance Criteria:**
- `after.md` contains literal heading `## Context freshness discipline`.
- `diff.md` is a pure append (no existing content modified).
- Self-check phrased as question, not imperative (manual review note in diff annotation).
- `wc -w` of added lines ≤350.

**Validation:** Read the appended section; confirm it matches design §4 verbatim. **Evidence:** before/after/diff artifacts.

**Dependencies:** None (independent of T03.01)
**Rollback:** Restore CLAUDE.md from `before.md`.
**Notes:** Existing `install_core_files` (in `src/superclaude/cli/install_core.py`) copies all `core/*.md` to `~/.claude/`, so this source change auto-distributes via `superclaude install` without requiring new install logic.

---

### Checkpoint: End of Phase 3

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P03-END.md`

**Verification:**
- `jq . src/superclaude/hooks/hooks.json` exits 0 and lists 7 event keys.
- `grep -F "## Context freshness discipline" src/superclaude/core/CLAUDE.md` returns the heading.
- Plugins mirror clean.

**Exit Criteria:**
- Zero malformed-JSON or schema issues.
- Source side is "spec complete" — all 7 hooks registered, behavioral rules in CLAUDE.md.
- `~/.claude/` is unchanged (live install happens in Phase 5).
