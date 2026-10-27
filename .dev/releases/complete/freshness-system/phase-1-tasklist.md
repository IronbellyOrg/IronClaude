# Phase 1 -- Pre-cleanup and source layout

Phase goal: prepare the IronClaude source tree to receive the freshness work. Two pre-cleanups (existing hooks.json relative-path fix, creating scripts/ subdirs) before any new hook code lands. After this phase, `src/superclaude/hooks/scripts/` exists with 7 stub scripts and the existing `session-init.sh` command path is no longer fragile.

---

### T01.01 -- Rewrite hooks.json `session-init.sh` path; relocate script

| Field | Value |
|---|---|
| Roadmap Item IDs | R-001 |
| Why | The existing `./scripts/session-init.sh` relative path in `src/superclaude/hooks/hooks.json:8` and the mirror copy is fragile — it resolves against unpredictable cwd at hook fire time and likely fails silently in most installs. Fixing it now means freshness work merges into a clean base (see `IronClaude:docs/analysis/hooks-json-relative-path-issue.md`). |
| Effort | XS |
| Risk | Low |
| Risk Drivers | none material; defect already exists |
| Tier | STANDARD |
| Confidence | `[█████████-] 90%` |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | jq parse + grep |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0001 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0001/diff.md`
- `TASKLIST_ROOT/artifacts/D-0001/notes.md`

**Deliverables:**
- `src/superclaude/hooks/hooks.json` line 8 command rewritten to `~/.claude/hooks/session-init.sh`
- Mirror change applied to `plugins/superclaude/hooks/hooks.json`
- `session-init.sh` script (current location TBD — search and document) staged for inclusion in install_hooks.py copy list

**Steps:**
1. **[PLANNING]** Read `IronClaude:docs/analysis/hooks-json-relative-path-issue.md` for context.
2. **[PLANNING]** Locate the actual `session-init.sh` file. Try `find /config/workspace/IronClaude -name "session-init.sh"`. Note its current path for inclusion in install_hooks copy list (Phase 4).
3. **[EXECUTION]** Edit `src/superclaude/hooks/hooks.json`: change `"command": "./scripts/session-init.sh"` to `"command": "~/.claude/hooks/session-init.sh"`.
4. **[EXECUTION]** Same edit on `plugins/superclaude/hooks/hooks.json`.
5. **[VERIFICATION]** `jq . src/superclaude/hooks/hooks.json` and `jq . plugins/superclaude/hooks/hooks.json` both exit 0.
6. **[VERIFICATION]** `diff src/superclaude/hooks/hooks.json plugins/superclaude/hooks/hooks.json` shows no differences.
7. **[VERIFICATION]** `grep -c '\./scripts' src/superclaude/hooks/hooks.json plugins/superclaude/hooks/hooks.json` returns 0 for both.
8. **[COMPLETION]** Diff captured to `TASKLIST_ROOT/artifacts/D-0001/diff.md`; notes record where session-init.sh currently lives.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/artifacts/D-0001/diff.md` shows exactly one-line changes in each of the two hooks.json files.
- `jq . hooks.json` returns exit 0 for both files.
- `grep -F './scripts/' hooks.json` finds no remaining occurrences in either file.
- notes.md documents the current location of `session-init.sh` for use in T04.01.

**Validation:**
- Manual check: `cat src/superclaude/hooks/hooks.json | jq .hooks.SessionStart[0].hooks[0].command` returns `"~/.claude/hooks/session-init.sh"`
- Evidence: diff.md + notes.md

**Dependencies:** None
**Rollback:** Revert both hooks.json files (single-line revert in each).
**Notes:** session-init.sh content not modified in this task; only its registered path. Inclusion in install pipeline happens in Phase 4.

---

### T01.02 -- Create src/superclaude/hooks/scripts/ with 7 stubs

| Field | Value |
|---|---|
| Roadmap Item IDs | R-002 |
| Why | Phase 2 implements 7 hook handlers; they must live in a stable source location that the install pipeline (Phase 4) can copy from. Stubs first, real bodies later, keeps Phase 2 task scopes small. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | none |
| Tier | LIGHT |
| Confidence | `[█████████-] 95%` |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | ls + bash -n |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0002 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0002/stubs.txt`

**Deliverables:**
- `src/superclaude/hooks/scripts/` directory
- 7 executable stub files:
  - `freshness-session-start.sh`
  - `freshness-user-prompt.sh`
  - `freshness-pre-edit.sh`
  - `freshness-post-read.sh`
  - `freshness-file-changed.sh`
  - `freshness-subagent-start.sh`
  - `freshness-subagent-stop.sh`
- Each stub: shebang + `# STUB - implemented in Phase 2 T02.0X` + `exit 0`. Mode 0755.

**Steps:**
1. **[EXECUTION]** `mkdir -p src/superclaude/hooks/scripts`.
2. **[EXECUTION]** Create each of the 7 stub files (heredoc shebang + comment + exit 0).
3. **[EXECUTION]** `chmod +x src/superclaude/hooks/scripts/freshness-*.sh`.
4. **[VERIFICATION]** `ls -l src/superclaude/hooks/scripts/freshness-*.sh` → all 7 mode 0755.
5. **[VERIFICATION]** For each: `bash -n <file>` exits 0.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/artifacts/D-0002/stubs.txt` lists all 7 scripts with mode `-rwxr-xr-x`.
- Each script's `bash -n` returns exit 0.
- No file other than the 7 freshness-*.sh stubs was created under `src/superclaude/hooks/scripts/`.
- Each stub body is ≤4 lines.

**Validation:**
- Manual check: `find src/superclaude/hooks/scripts -type f -name "freshness-*.sh" | wc -l` → 7
- Evidence: stubs.txt

**Dependencies:** None
**Rollback:** `rm -rf src/superclaude/hooks/scripts`
**Notes:** No semantic content yet; bodies land in Phase 2.

---

### T01.03 -- Mirror scripts/ to plugins/superclaude/hooks/scripts/

| Field | Value |
|---|---|
| Roadmap Item IDs | R-003 |
| Why | Per `src/superclaude/hooks/README.md`, src/ and plugins/ hook content must stay in sync until v5.0 unifies them. Maintaining the mirror as part of Phase 1 sets the pattern for Phase 2 (every hook script change must propagate). |
| Effort | XS |
| Risk | Low |
| Risk Drivers | drift between src/ and plugins/ if mirror step is forgotten |
| Tier | STANDARD |
| Confidence | `[█████████-] 95%` |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | diff |
| MCP Requirements | None |
| Fallback Allowed | No |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0003 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0003/mirror-diff.txt`

**Deliverables:**
- `plugins/superclaude/hooks/scripts/` directory containing exact copies of the 7 stubs from T01.02
- Mirror diff verification (should be empty)

**Steps:**
1. **[EXECUTION]** `mkdir -p plugins/superclaude/hooks/scripts`.
2. **[EXECUTION]** `cp src/superclaude/hooks/scripts/*.sh plugins/superclaude/hooks/scripts/`.
3. **[EXECUTION]** Preserve mode 0755 (cp preserves on Linux).
4. **[VERIFICATION]** `diff -r src/superclaude/hooks/scripts plugins/superclaude/hooks/scripts` → no differences.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/artifacts/D-0003/mirror-diff.txt` exists and is empty (or contains only a "files identical" message).
- All 7 scripts present in both `src/` and `plugins/` paths with identical content and mode.
- No additional files in plugins/scripts/ that aren't in src/scripts/.

**Validation:**
- Manual check: `diff -r src/superclaude/hooks/scripts plugins/superclaude/hooks/scripts` returns exit 0 with no output
- Evidence: mirror-diff.txt

**Dependencies:** T01.02
**Rollback:** `rm -rf plugins/superclaude/hooks/scripts`
**Notes:** Phase 2 task closeout MUST re-mirror after each hook body lands. Consider whether to script the mirror (e.g., `make mirror-hooks`) — out of scope here but worth a Phase 4 task addition.

---

### Checkpoint: End of Phase 1

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P01-END.md`

**Verification:**
- Both hooks.json files have `~/.claude/hooks/session-init.sh` and pass `jq .` (T01.01).
- All 7 freshness-*.sh stubs exist in both `src/` and `plugins/` paths with matching content (T01.02 + T01.03).
- No other files under either `hooks/scripts/` directory.

**Exit Criteria:**
- `diff -r src/superclaude/hooks plugins/superclaude/hooks` returns clean (only the `__init__.py` and `README.md` differences expected from prior state, if any).
- `find . -path '*/hooks/scripts/*' -name '*.sh' -not -executable` returns no rows.
- Pre-existing IronClaude hook (session-init.sh) is preserved; its registered path is fixed.
