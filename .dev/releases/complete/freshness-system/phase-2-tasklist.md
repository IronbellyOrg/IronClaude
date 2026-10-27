# Phase 2 -- Hook script implementation

Phase goal: replace each stub from Phase 1 with its real handler per `InfraDocs:phase5.1-context-refresh-design.md` §3. Six STRICT tasks; one per handler (subagent start/stop paired). Each task closes by mirroring src → plugins (per T01.03 pattern).

**Standing pattern for every task in this phase:**
- All work is in `src/superclaude/hooks/scripts/freshness-X.sh`.
- After body lands, `cp` to `plugins/superclaude/hooks/scripts/`.
- Each hook reads stdin JSON via `jq` (already a build dependency).
- Each hook's state paths reference `~/.claude/state/...` even though the source file lives in IronClaude. This is intentional — scripts run *after* install, where the state dir is at the user's home.
- Each hook self-mkdir's its state subdir if missing (fail-open on permission errors).

---

### T02.01 -- Implement SessionStart hook

| Field | Value |
|---|---|
| Roadmap Item IDs | R-004 |
| Why | The only event that re-fires on `--resume`. Critical for the 2-day-suspension scenario. Implements both startup and resume branches per design §3.1. |
| Effort | M | Risk | Medium | Risk Drivers | stdin JSON parsing, fail-open semantics, 10K char cap |
| Tier | STRICT | Confidence | `[█████████-] 90%` | Requires Confirmation | No | Critical Path Override | No |
| Verification Method | Sub-agent quality-engineer review + 2 dry-runs |
| MCP Requirements | Required: Sequential, Serena | Fallback Allowed | No | Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0004 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0004/spec.md` (link to design §3.1)
- `TASKLIST_ROOT/artifacts/D-0004/dry-run-startup.txt`
- `TASKLIST_ROOT/artifacts/D-0004/dry-run-resume.txt`
- `TASKLIST_ROOT/artifacts/D-0004/evidence.md`

**Deliverables:**
- `src/superclaude/hooks/scripts/freshness-session-start.sh` body per design §3.1
- Plugins mirror in sync

**Steps:**
1. **[PLANNING]** Read design §3.1 pseudocode.
2. **[EXECUTION]** Implement startup branch + resume branch per design.
3. **[EXECUTION]** Wrap output in `<session-context source="...">...</session-context>` (NFR-9).
4. **[EXECUTION]** Add fail-open: any subcommand failure (git, jq, docker) → omit field silently.
5. **[EXECUTION]** Mirror to plugins/.
6. **[VERIFICATION]** Dry-run startup: `echo '{"session_id":"t","source":"startup","cwd":"/tmp"}' | bash freshness-session-start.sh | jq -e .hookSpecificOutput.additionalContext`.
7. **[VERIFICATION]** Dry-run resume: `echo '{"session_id":"t","source":"resume","cwd":"'$PWD'"}' | bash freshness-session-start.sh | jq -e .hookSpecificOutput.additionalContext` — confirm `resumed_after=` field present.
8. **[VERIFICATION]** Sub-agent quality-engineer review for fail-open semantics on each subcommand.

**Acceptance Criteria:**
- File `src/superclaude/hooks/scripts/freshness-session-start.sh` exists, mode 0755, `bash -n` passes.
- Dry-run-startup.txt contains valid JSON with `<session-context source="startup">` envelope.
- Dry-run-resume.txt contains valid JSON with `resumed_after=` field.
- Plugins mirror `diff -q` returns clean.

**Validation:** Manual check per step 6/7 commands. **Evidence:** dry-run files + sub-agent report.

**Dependencies:** T01.02 (stub exists)
**Rollback:** Restore stub body.
**Notes:** Memory-index field reads first line of each file in `~/.claude/projects/<project>/memory/[a-z]*.md`. Max 8 lines, trim 80 chars.

---

### T02.02 -- Implement UserPromptSubmit hook

| Field | Value |
|---|---|
| Roadmap Item IDs | R-005 |
| Why | Per-turn envelope. Conditional rendering (NFR-8). 10K cap defense per `InfraDocs:phase5.1-token-budget-check.md` (truncation at 9000 chars). |
| Effort | L | Risk | Medium | Risk Drivers | Multi-source aggregation; truncation logic; turn-counter atomicity |
| Tier | STRICT | Confidence | `[████████--] 85%` | Requires Confirmation | No | Critical Path Override | No |
| Verification Method | Sub-agent review + 4 dry-runs (clean, dirty, resume, truncation) |
| MCP Requirements | Required: Sequential, Serena | Fallback Allowed | No | Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0005 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0005/spec.md`, `dry-run-clean.txt`, `dry-run-dirty.txt`, `dry-run-resume.txt`, `dry-run-truncation.txt`, `evidence.md`

**Deliverables:**
- `src/superclaude/hooks/scripts/freshness-user-prompt.sh` per design §3.2
- Truncation logic per `phase5.1-token-budget-check.md` recommendations
- Plugins mirror

**Steps:**
1. **[PLANNING]** Read design §3.2 + token-budget doc.
2. **[EXECUTION]** Implement turn-counter increment with `flock`.
3. **[EXECUTION]** Implement Δ computation (read last-prompt-ts, format ≥300s as duration).
4. **[EXECUTION]** Implement git-dirty probe (porcelain count).
5. **[EXECUTION]** Implement bg-agents read.
6. **[EXECUTION]** Implement changes.jsonl consume + truncate (with flock).
7. **[EXECUTION]** Conditional items list per design §3.2 step 7 table.
8. **[EXECUTION]** RESUMED flag when Δ ≥ 3600s.
9. **[EXECUTION]** Truncation: if envelope > 9000 chars, truncate `changed_since_last_turn=` to first 3 + `,...(<N> more)`; if still over, drop RESUMED flag. Log `truncated=true` to telemetry.
10. **[EXECUTION]** Emit JSON additionalContext.
11. **[EXECUTION]** Mirror to plugins/.
12. **[VERIFICATION]** 4 dry-runs covering each scenario.
13. **[VERIFICATION]** Sub-agent review.

**Acceptance Criteria:**
- File `src/superclaude/hooks/scripts/freshness-user-prompt.sh` exists mode 0755, `bash -n` passes.
- Clean-tree dry-run is minimal envelope (~120 chars total).
- Dirty-tree dry-run includes all 5 conditional items.
- Resume dry-run includes RESUMED flag.
- Truncation dry-run (force 100-path changes.jsonl) caps output ≤9100 chars and logs `truncated=true`.

**Validation:** Manual check per dry-run scenarios. **Evidence:** 4 dry-run files + sub-agent report.

**Dependencies:** T01.02
**Rollback:** Restore stub.
**Notes:** TaskList active-count is v2-deferred. Do not emit.

---

### T02.03 -- Implement PreToolUse freshness gate

| Field | Value |
|---|---|
| Roadmap Item IDs | R-006 |
| Why | The enforcement layer. Prevents the §5.1 originating bug. |
| Effort | L | Risk | High | Risk Drivers | wrong block halts legit work; wrong allow lets bug recur; exit-2 discipline (NFR-10) |
| Tier | STRICT | Confidence | `[█████████-] 90%` | Requires Confirmation | No | Critical Path Override | Yes |
| Verification Method | Sub-agent review + 4 dry-runs (each decision branch) |
| MCP Requirements | Required: Sequential, Serena | Fallback Allowed | No | Sub-Agent Delegation | Required |
| Deliverable IDs | D-0006 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0006/{spec.md, dry-run-allow.txt, dry-run-block-noread.txt, dry-run-block-toold.txt, dry-run-block-changed.txt, evidence.md}`

**Deliverables:**
- `src/superclaude/hooks/scripts/freshness-pre-edit.sh` per design §3.3
- Telemetry append to `~/.claude/logs/freshness-hook.jsonl`
- Plugins mirror

**Steps:**
1. **[PLANNING]** Read design §3.3, FR-6 telemetry schema, NFR-10 exit-code discipline.
2. **[EXECUTION]** Extract target_path from stdin (prefer `file_path`, fallback `relative_path` + cwd).
3. **[EXECUTION]** Increment tool-call-counter atomically.
4. **[EXECUTION]** Look up last Read in reads.jsonl by path + session_id.
5. **[EXECUTION]** Compute Δ in seconds.
6. **[EXECUTION]** Check changes.jsonl for entries with `path == target` AND `ts_unix > last_read.ts_unix`.
7. **[EXECUTION]** Decision logic (4-branch per design §3.3 step 8).
8. **[EXECUTION]** Telemetry append per FR-6 schema.
9. **[EXECUTION]** Block path: factual-phrasing stderr + exit 2. Allow path: exit 0. Never exit 1 (NFR-10).
10. **[EXECUTION]** Mirror to plugins/.
11. **[VERIFICATION]** 4 dry-runs.
12. **[VERIFICATION]** Sub-agent review explicitly addresses: (a) only exit 2 blocks; (b) fail-open semantics; (c) factual stderr phrasing.

**Acceptance Criteria:**
- File `src/superclaude/hooks/scripts/freshness-pre-edit.sh` mode 0755, `bash -n` passes.
- 4 dry-runs produce documented exit codes and stderr matching design §3.3.
- `~/.claude/logs/freshness-hook.jsonl` gains rows matching FR-6 schema (each row `jq .` parses).
- Sub-agent report addresses (a), (b), (c) explicitly.

**Validation:** Per dry-run. **Evidence:** 4 dry-run files + telemetry sample + sub-agent report.

**Dependencies:** T01.02
**Rollback:** Restore stub.
**Notes:** Highest-risk hook. Sub-agent review is mandatory, not just recommended.

---

### T02.04 -- Implement PostToolUse(Read) tracker

| Field | Value |
|---|---|
| Roadmap Item IDs | R-007 |
| Why | Records every successful Read into reads.jsonl. Prerequisite for the freshness gate. |
| Effort | S | Risk | Low | Risk Drivers | atomicity under concurrent fires |
| Tier | STRICT | Confidence | `[█████████-] 95%` | Requires Confirmation | No | Critical Path Override | No |
| Verification Method | Sub-agent review + concurrency simulation |
| MCP Requirements | Required: Sequential, Serena | Fallback Allowed | Yes (async:true) | Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0007 |

**Artifacts:** `TASKLIST_ROOT/artifacts/D-0007/{spec.md, dry-run.txt, concurrency-test.txt, evidence.md}`

**Deliverables:**
- `src/superclaude/hooks/scripts/freshness-post-read.sh` per design §3.4
- Plugins mirror

**Steps:**
1. **[EXECUTION]** Implement per design §3.4: skip on failed Read response; atomic counter increment; append to reads.jsonl.
2. **[EXECUTION]** Mirror to plugins/.
3. **[VERIFICATION]** Dry-run success (1 row appended); dry-run failure (0 rows).
4. **[VERIFICATION]** Concurrency: `xargs -P 10` of 100 invocations → reads.jsonl gains exactly 100 rows; tool-call-counter is monotonic.

**Acceptance Criteria:** File mode 0755, `bash -n` passes; success dry-run appends 1 row matching schema; failure dry-run appends 0; concurrency test produces no duplicate `tool_call_idx`.

**Validation:** Per step. **Evidence:** dry-run.txt + concurrency-test.txt + sub-agent report.

**Dependencies:** T01.02
**Rollback:** Restore stub.
**Notes:** `async: true` in hooks.json — non-blocking.

---

### T02.05 -- Implement FileChanged tracker

| Field | Value |
|---|---|
| Roadmap Item IDs | R-008 |
| Why | External-modification detection for the gate's `external_change` branch. |
| Effort | M | Risk | Medium | Risk Drivers | FileChanged stdin schema not primary-source verified; matcher static |
| Tier | STRICT | Confidence | `[███████---] 75%` | **Requires Confirmation** | **Yes (<0.80)** | Critical Path Override | No |
| Verification Method | Sub-agent + probe handler |
| MCP Requirements | Required: Sequential, Serena; Preferred: Auggie | Fallback Allowed | Yes | Sub-Agent Delegation | Required |
| Deliverable IDs | D-0008 |

**Artifacts:** `TASKLIST_ROOT/artifacts/D-0008/{spec.md, probe-output.txt, dry-run.txt, evidence.md}`

**Deliverables:**
- Probe handler artifact documenting actual FileChanged stdin field set
- `src/superclaude/hooks/scripts/freshness-file-changed.sh` per design §3.5 (after probe confirms shape)
- Plugins mirror

**Steps:**
1. **[PROBE]** Deploy temporary probe handler at `~/.claude/hooks/freshness-file-changed.sh`: `cat - > ~/.claude/logs/file-changed-probe-$(date +%s).json; exit 0`. Wire briefly in `~/.claude/settings.json` for testing only.
2. **[PROBE]** Trigger FileChanged by editing a watched file in a real Claude Code session. Capture probe JSON.
3. **[PROBE]** Record probe findings to `probe-output.txt`. Note field names (`path`, `change_type`, anything else).
4. **[EXECUTION]** Implement real handler per design §3.5, using probe-confirmed field names.
5. **[EXECUTION]** Remove probe handler from `~/.claude/settings.json`; replace with permanent registration in T03.01.
6. **[EXECUTION]** Mirror to plugins/.
7. **[VERIFICATION]** Dry-run with reads.jsonl populated → changes.jsonl appended.
8. **[VERIFICATION]** Dry-run with file not in reads.jsonl → no append.
9. **[VERIFICATION]** Sub-agent review for grep-cost (<50ms on 1000-entry reads.jsonl) and schema correctness.

**Acceptance Criteria:** probe-output.txt documents actual FileChanged stdin shape; final handler uses confirmed field names; dry-run appends to changes.jsonl with correct schema; sub-agent confirms latency target.

**Validation:** Per step. **Evidence:** probe-output.txt + dry-run.txt + sub-agent report.

**Dependencies:** T01.02
**Rollback:** Restore stub; remove probe handler from settings.json if still present.
**Notes:** Confidence <0.80 — requires user confirmation before committing real handler. Probe stage lifts confidence empirically.

---

### T02.06 -- Implement Subagent counter hooks

| Field | Value |
|---|---|
| Roadmap Item IDs | R-009 |
| Why | UserPromptSubmit's `bg=` conditional. Paired start/stop, floored at 0. |
| Effort | S | Risk | Low | Risk Drivers | concurrent ++/-- races |
| Tier | STRICT | Confidence | `[█████████-] 90%` | Requires Confirmation | No | Critical Path Override | No |
| Verification Method | Sub-agent + concurrency test |
| MCP Requirements | Required: Sequential, Serena | Fallback Allowed | Yes | Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0009 |

**Artifacts:** `TASKLIST_ROOT/artifacts/D-0009/{spec.md, dry-run.txt, evidence.md}`

**Deliverables:**
- `src/superclaude/hooks/scripts/freshness-subagent-start.sh` (increment)
- `src/superclaude/hooks/scripts/freshness-subagent-stop.sh` (decrement, floored at 0)
- Plugins mirror

**Steps:**
1. **[EXECUTION]** Implement start/stop per design §3.6 with flock.
2. **[EXECUTION]** Mirror to plugins/.
3. **[VERIFICATION]** Linear: 3 starts + 2 stops → counter=1; 3 stops → counter=0 (floored).
4. **[VERIFICATION]** Concurrency: `xargs -P 10` of 100 mixed → counter equals start_count - stop_count, never negative.

**Acceptance Criteria:** Both files mode 0755, `bash -n` passes; linear dry-run produces correct counter; floor test stays at 0; concurrency test correct.

**Validation:** Per step. **Evidence:** dry-run.txt + sub-agent report.

**Dependencies:** T01.02
**Rollback:** Restore stubs.

---

### Checkpoint: End of Phase 2

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P02-END.md`

**Verification:**
- All 6 task deliverables (D-0004 through D-0009) have spec/dry-run/evidence artifacts.
- Every hook passes `bash -n`.
- Plugins mirror `diff -r src/superclaude/hooks/scripts plugins/superclaude/hooks/scripts` clean.

**Exit Criteria:**
- Zero CRITICAL sub-agent flags.
- T02.05 probe-output.txt documents actual FileChanged stdin schema.
- `~/.claude/settings.json` was NOT modified during Phase 2 (live wiring belongs to Phase 5; src-side wiring to Phase 3).
