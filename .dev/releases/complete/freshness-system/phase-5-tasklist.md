# Phase 5 -- Local install + validation + baseline

Phase goal: run the install pipeline against the local user environment, validate via the regression suite, and capture a baseline of real telemetry data. This is the only phase that actually modifies `~/.claude/` and the only phase where Test 1 from the regression suite executes against a real Claude Code session. Four tasks; gated mid-phase by Test 1 result.

---

### T05.01 -- Run make sync-dev && superclaude install -f locally

| Field | Value |
|---|---|
| Roadmap Item IDs | R-017 |
| Why | Phase 4 produced the install pipeline; this task fires it against the real user environment. After this, `~/.claude/CLAUDE.md` has the freshness section, `~/.claude/hooks/` contains the 7 freshness scripts (+ session-init.sh), and `~/.claude/settings.json` has 7 new hook registrations merged additively. |
| Effort | XS | Risk | Medium | Risk Drivers | merges into the user's real settings.json; one bad merge breaks every hook on this machine |
| Tier | STANDARD | Confidence | `[████████--] 85%` | Requires Confirmation | No | Critical Path Override | Yes |
| Verification Method | jq + filesystem + side-by-side diff against backup |
| MCP Requirements | Preferred: Sequential | Fallback Allowed | No | Sub-Agent Delegation | None |
| Deliverable IDs | D-0018, D-0019 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0018/{install-output.txt, post-install-ls.txt, post-install-jq.txt}`
- `TASKLIST_ROOT/artifacts/D-0019/settings-pair/{before.json, after.json, diff.md, audit.md}`

**Deliverables:**
- `~/.claude/settings.json` with 7 freshness hook registrations merged additively (existing hooks preserved)
- `~/.claude/hooks/freshness-*.sh` (7 scripts, mode 0755) plus `session-init.sh` if not already present
- `~/.claude/CLAUDE.md` with the freshness section appended (via `install_core_files`)
- Backup pair captured for audit

**Steps:**
1. **[PLANNING]** Pre-install snapshot:
   ```bash
   cp ~/.claude/settings.json TASKLIST_ROOT/artifacts/D-0019/settings-pair/before.json 2>/dev/null || \
     echo "no pre-existing settings.json" > .../before.json
   ls -la ~/.claude/hooks/ 2>/dev/null > TASKLIST_ROOT/artifacts/D-0018/pre-install-ls.txt
   ```
2. **[EXECUTION]** Run sync: `cd /config/workspace/IronClaude && make sync-dev 2>&1 | tee TASKLIST_ROOT/artifacts/D-0018/install-output.txt`
3. **[EXECUTION]** Run install: `uv run superclaude install -f 2>&1 | tee -a TASKLIST_ROOT/artifacts/D-0018/install-output.txt`
4. **[VERIFICATION]** Post-install state capture:
   ```bash
   cp ~/.claude/settings.json TASKLIST_ROOT/artifacts/D-0019/settings-pair/after.json
   ls -la ~/.claude/hooks/ > TASKLIST_ROOT/artifacts/D-0018/post-install-ls.txt
   jq -r '.hooks | keys[]' ~/.claude/settings.json > TASKLIST_ROOT/artifacts/D-0018/post-install-jq.txt
   ```
5. **[VERIFICATION]** `jq . ~/.claude/settings.json` exits 0.
6. **[VERIFICATION]** `post-install-jq.txt` lists at minimum: SessionStart, UserPromptSubmit, PreToolUse, PostToolUse, FileChanged, SubagentStart, SubagentStop.
7. **[VERIFICATION]** `ls ~/.claude/hooks/freshness-*.sh | wc -l` returns 7.
8. **[VERIFICATION]** `bash -n ~/.claude/hooks/freshness-*.sh` (each) exits 0.
9. **[VERIFICATION]** `grep -F "## Context freshness discipline" ~/.claude/CLAUDE.md` returns the heading.
10. **[VERIFICATION]** Diff before.json against after.json. Manually audit to confirm: (a) existing hooks preserved; (b) only the 7 freshness registrations added; (c) no other key changes. Record audit in `audit.md`.
11. **[VERIFICATION]** Confirm install_hooks's own backup exists: `ls ~/.claude/settings.json.bak.*` should show at least one timestamped backup.
12. **[COMPLETION]** Open a fresh Claude Code session in `/tmp/freshness-smoke` (mkdir if needed). On session start, the `freshness-session-start.sh` hook should fire and create `~/.claude/state/turns/<session>.txt` with "0". Verify.

**Acceptance Criteria:**
- `jq -r '.hooks | keys[]' ~/.claude/settings.json` includes all 7 freshness events.
- `~/.claude/hooks/` contains 7 mode-0755 freshness-*.sh files.
- `~/.claude/CLAUDE.md` contains `## Context freshness discipline`.
- `audit.md` confirms additive merge: no existing user hooks or unrelated keys were modified.
- A fresh `/tmp/freshness-smoke` session triggers SessionStart hook (verified by `~/.claude/state/turns/` gaining a file).

**Validation:**
- Manual: `jq . ~/.claude/settings.json` + open fresh session + check state dir
- Evidence: install-output.txt + pre/post-install-ls.txt + before/after JSON pair + audit.md

**Dependencies:** T04.05 (full Phase 4 complete)
**Rollback:** Restore `~/.claude/settings.json` from `~/.claude/settings.json.bak.<latest>`. Remove `~/.claude/hooks/freshness-*.sh`. Restore previous `~/.claude/CLAUDE.md` (note: `install_core_files` doesn't backup, so this rollback requires `git checkout` of the CLAUDE.md source + re-install OR manual section removal).
**Notes:** This is the highest-risk step in Phase 5. The audit.md step (10) is non-negotiable — automation can't catch every subtle merge issue.

---

### Checkpoint: Phase 5 / Install gate (after T05.01)

**Purpose:** Confirm install landed cleanly before running regression suite. Halt phase if any verification fails.

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P05-T05.01.md`

**Verification:**
- `audit.md` confirms additive merge (no unrelated changes).
- 7 freshness hook scripts present, mode 0755, syntax-valid.
- CLAUDE.md contains the freshness section.

**Exit Criteria:**
- No `jq .` errors on `~/.claude/settings.json`.
- Fresh-session smoke test from step 12 produced state files.
- No errors in stderr from `superclaude install -f`.

---

### T05.02 -- Run regression test 1 (originating-bug smoke)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-018 |
| Why | Test 1 replays the §5.1 docker-compose.yml line-cite drift bug. If freshness can't prevent this specific scenario, the build was wasted. Gating test before tests 2-5. |
| Effort | S | Risk | Medium | Risk Drivers | first real exercise of the gate against a live session |
| Tier | STANDARD | Confidence | `[████████--] 85%` | Requires Confirmation | No | Critical Path Override | Yes |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential | Fallback Allowed | No | Sub-Agent Delegation | None |
| Deliverable IDs | D-0020, D-0021 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0020/{test-1-transcript.md, test-1-result.md}`
- `TASKLIST_ROOT/artifacts/D-0021/log-sample.jsonl` (telemetry rows produced)

**Deliverables:**
- Recorded PASS/FAIL outcome for Test 1
- Telemetry sample showing a block decision with `reason=read_too_old` or `reason=external_change`

**Steps:**
1. **[PLANNING]** Source the regression test spec. Note: in the IronClaude-distribution model, the regression test spec lives at `~/.claude/CLAUDE.md`'s linked location OR in `IronClaude:docs/user-guide/freshness-hooks.md` (created in T04.05). If it doesn't exist yet, copy from `InfraDocs:/config/.claude/tests/freshness-regression.md` into IronClaude as part of this task.
2. **[PLANNING]** Snapshot baseline: `wc -l ~/.claude/logs/freshness-hook.jsonl` → N_pre.
3. **[EXECUTION]** Set up `/tmp/freshness-test-1` fixture per Test 1 spec: 30-line `compose.yml` with `volumes:` at line 25.
4. **[EXECUTION]** Open fresh Claude Code session in the fixture. Have Claude Read compose.yml at turn 1.
5. **[EXECUTION]** Issue 8-10 unrelated tool calls (Bash, Grep, etc.).
6. **[EXECUTION]** Externally modify the file (insert 3 lines at top so `volumes:` is now at line 28).
7. **[EXECUTION]** Ask Claude: "What line is `volumes:` on in compose.yml?"
8. **[VERIFICATION]** Observe:
   - PASS: Claude Reads the file before answering AND cites line 28.
   - FAIL: Claude cites line 25 from memory without re-reading.
9. **[VERIFICATION]** Count post-test telemetry rows: `wc -l ~/.claude/logs/freshness-hook.jsonl` ≥ N_pre + 1 with at least one row having `reason=external_change` or `reason=read_too_old`. Sample saved to log-sample.jsonl.
10. **[COMPLETION]** Record PASS/FAIL in test-1-result.md with explicit evidence references.

**Acceptance Criteria:**
- test-1-result.md has explicit PASS or FAIL verdict referencing the transcript.
- If PASS: log-sample.jsonl shows at least one block decision row.
- If FAIL: result.md documents which expected behavior was missing AND proposes remediation (which hook or CLAUDE.md element is responsible).
- Fixture under `/tmp/freshness-test-1` captured (tar'd or contents copied) for reproducibility.

**Validation:** Manual replay using captured fixture should produce same outcome. **Evidence:** transcript + result + telemetry excerpt.

**Dependencies:** T05.01 PASS
**Rollback:** N/A (read-only verification)
**Notes:** GATING test. FAIL halts the phase. Remediation tasks are inserted before T05.03.

---

### T05.03 -- Run regression tests 2-5

| Field | Value |
|---|---|
| Roadmap Item IDs | R-019 |
| Why | Tests 2-5 cover chat-only citations, cross-file claims, 2-day suspension, and the negative control (system doesn't over-fire). Together with Test 1 they validate full FR-1 signal taxonomy. |
| Effort | M | Risk | Medium | Risk Drivers | Test 4 needs real elapsed time or transcript-timestamp simulation |
| Tier | STANDARD | Confidence | `[████████--] 80%` | Requires Confirmation | No | Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential | Fallback Allowed | Yes (Test 4 simulation fallback) | Sub-Agent Delegation | None |
| Deliverable IDs | D-0022 |

**Artifacts:** `TASKLIST_ROOT/artifacts/D-0022/{test-2-result.md, test-3-result.md, test-4-result.md, test-5-result.md, summary.md}`

**Deliverables:**
- Recorded outcomes for Tests 2-5
- Aggregated summary table

**Steps:**
1. **[EXECUTION]** Run Test 2 (chat-only citation): setup → trigger → record PASS/FAIL → annotate.
2. **[EXECUTION]** Run Test 3 (cross-file claim): setup → trigger → record → annotate.
3. **[EXECUTION]** Run Test 4 (suspension): real wall-clock if 2 days available; else timestamp-simulation fallback documented in test spec. Record → annotate.
4. **[EXECUTION]** Run Test 5 (negative control): 5 conversational turns; confirm 0 ceremonial Reads.
5. **[VERIFICATION]** Each test gets its own result.md with PASS/FAIL + evidence.
6. **[VERIFICATION]** Summary table in summary.md: test ID, PASS/FAIL, key evidence path, notes.

**Acceptance Criteria:**
- 4 result files exist with explicit PASS/FAIL.
- summary.md aggregates all 4.
- Test 5: zero unsolicited Reads (verified by grep over transcript).
- Any FAIL has linked remediation note.

**Validation:** Per step. **Evidence:** 4 result files + summary.md.

**Dependencies:** T05.02 PASS
**Rollback:** N/A
**Notes:** Test 4 simulation fallback acceptable if real-wall-clock impractical; flag in result file.

---

### T05.04 -- Capture telemetry baseline + write memory entries

| Field | Value |
|---|---|
| Roadmap Item IDs | R-020 |
| Why | FR-6 telemetry's purpose is to inform future tuning. One week of real-session data answers "should we adjust N?". Closing the build means writing the cumulative baseline to Serena memory (for future tuning), an auto-memory entry (so future sessions know the system exists), and a MEMORY.md index entry (so it loads automatically). |
| Effort | XS | Risk | Low | Risk Drivers | none |
| Tier | EXEMPT | Confidence | `[█████████-] 95%` | Requires Confirmation | No | Critical Path Override | No |
| Verification Method | Read logs + Serena memory + filesystem |
| MCP Requirements | Required: Serena | Fallback Allowed | No | Sub-Agent Delegation | None |
| Deliverable IDs | D-0023, D-0024, D-0025, D-0026 |

**Artifacts:**
- `TASKLIST_ROOT/artifacts/D-0023/baseline.md`
- `TASKLIST_ROOT/artifacts/D-0024/memory-content.md` (Serena memory)
- `TASKLIST_ROOT/artifacts/D-0025/memory-content.md` (auto-memory file body)
- `TASKLIST_ROOT/artifacts/D-0026/diff.md` (MEMORY.md index entry)

**Deliverables:**
- Telemetry baseline summary written to baseline.md
- Serena memory `freshness/tuning/window-size.md` (project: IronClaude) updated with one-week findings + recommend-keep-or-adjust verdict
- Auto-memory `feedback_freshness_system_live.md` under `/config/.claude/projects/-config-workspace-IronClaude/memory/` documenting that the system is live and how to interact with `<session-context>` envelope and block-with-reason stderr
- MEMORY.md (project: IronClaude) gains one-line index entry

**Steps:**
1. **[PLANNING]** Wait ≥7 days after T05.01. Daily Claude Code usage generates the data.
2. **[EXECUTION]** Aggregate `~/.claude/logs/freshness-hook.jsonl`: total rows, distribution by `decision` and `reason`, distribution of `recent_read_age_sec` for allow decisions.
3. **[EXECUTION]** Identify false positives (blocks where the file truly hadn't changed; user manually flags).
4. **[EXECUTION]** Decide N=30min keep/adjust. Write rationale (1-2 paragraphs).
5. **[EXECUTION]** `mcp__serena__write_memory(memory_name="freshness/tuning/window-size.md", content=<rationale>)`.
6. **[EXECUTION]** Write new auto-memory file at `/config/.claude/projects/-config-workspace-IronClaude/memory/feedback_freshness_system_live.md` with frontmatter (type: feedback) and body explaining: `<session-context>` envelope per turn, block-with-reason stderr from freshness gate, treat envelope as ground truth for current turn, re-Read when stderr asks.
7. **[EXECUTION]** Append index line to `/config/.claude/projects/-config-workspace-IronClaude/memory/MEMORY.md` (create the file if missing — that's where the auto-memory lives for the IronClaude project).
8. **[VERIFICATION]** `wc -l ~/.claude/logs/freshness-hook.jsonl` confirms ≥1 week of population (or ≥50 events).
9. **[VERIFICATION]** `mcp__serena__read_memory(memory_name="freshness/tuning/window-size.md")` returns the new body; copy to D-0024 artifact.
10. **[VERIFICATION]** `grep -F "feedback_freshness_system_live" .../MEMORY.md` returns the new entry.

**Acceptance Criteria:**
- baseline.md contains table with row count, decision distribution, reason distribution, and any false positives identified by date+path.
- D-0024 memory-content.md matches the body returned by `read_memory`.
- D-0025 memory-content.md matches the body in the filesystem auto-memory file.
- D-0026 diff.md shows the new MEMORY.md entry line.
- All 4 deliverables exist; none modify existing entries (pure additions).

**Validation:** Per step. **Evidence:** baseline.md + 2 memory-content files + diff.md.

**Dependencies:** T05.03 complete + ≥7 days of real session activity post-T05.01
**Rollback:** Delete the 4 added entries (Serena memory + filesystem file + MEMORY.md line). Telemetry log unchanged.
**Notes:** If telemetry shows <50 events in the week, extend baseline window to 14 days before tuning.

---

### Checkpoint: End of Phase 5 (FINAL)

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P05-END.md`

**Verification:**
- All 5 regression tests have recorded results; aggregate is PASS unless documented otherwise.
- Telemetry baseline + Serena memory + auto-memory + MEMORY.md entry all in place.
- `~/.claude/settings.json` audit confirms no regression from T05.01 install.

**Exit Criteria:**
- Zero open regression failures.
- Telemetry confirms hooks fire as designed (allow/block counts plausible; no silent crashes).
- All 20 tasks across phases 1-5 have completed status with their deliverables in `TASKLIST_ROOT/artifacts/`.

---

### Final acceptance for the entire freshness-system tasklist

Once Phase 5 closes:

1. Mark `InfraDocs:phase5.1-context-refresh-requirements.md` status as `IMPLEMENTED <date>`.
2. Add a one-line entry to `IronClaude:CHANGELOG.md` under the next release.
3. The system is live across all Claude Code projects on this machine.
4. Future tuning is driven by `freshness-hook.jsonl` telemetry; no further `/sc:design` / `/sc:implement` cycle expected until the v2 deferred-items list is revisited (4-week trigger per design §9).
