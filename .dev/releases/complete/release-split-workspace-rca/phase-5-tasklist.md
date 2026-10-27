# Phase 5 -- Acceptance Validation

**Phase Goal:** End-to-end exercise of the layered defense against the 5 acceptance criteria (AC1-AC5). M5 ENTRY GATE: no CP-M3-END CRITICAL severity findings open (test-strategy thresholds binding). Discovery risk -- if M5 surfaces gaps, loop back to M2/M3 with a revised fix; no production impact (validation-only milestone).

### T05.01 -- AC1 test: skill-creator + M1-M3 yields correct destination or hook redirect

| Field | Value |
|---|---|
| Roadmap Item IDs | R-012 |
| Why | Simulate a good-faith author invoking `skill-creator` against an IronClaude skill in a clone with all M1-M3 changes installed. Verify Claude reads project CLAUDE.md addendum and writes to `.dev/eval-workspaces/<name>/`. If addendum is ignored, verify the PreToolUse hook blocks the write with the redirect-pointing error. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0012 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0012/spec.md`
- `TASKLIST_ROOT/artifacts/D-0012/notes.md`
- `TASKLIST_ROOT/artifacts/D-0012/evidence.md`

**Deliverables:**
- A scripted simulation (or recorded session) of `skill-creator` invocation in a clean clone with M1-M3 landed, showing one of the two acceptable outcomes:
  - **Outcome A**: Claude reads the CLAUDE.md addendum and writes the workspace to `.dev/eval-workspaces/<name>/` directly.
  - **Outcome B**: Claude attempts to write the workspace to `.claude/skills/<name>-workspace/`; the PreToolUse hook rejects with the redirect message; Claude retries with the correct path.

**Steps:**
1. **[PLANNING]** Set up (or scope) a clean clone of the repo with M1 (T01.01-T01.03), M2 (T02.01-T02.03), M3 (T03.01-T03.03) all landed.
2. **[PLANNING]** Identify a target skill name (e.g., `__ac1_probe__`) and an invocation form for `skill-creator` against an IronClaude skill.
3. **[EXECUTION]** Run the simulation: invoke `skill-creator` and observe whether Claude follows the addendum (Outcome A) or hits the hook (Outcome B).
4. **[EXECUTION]** Capture the full sequence of file writes, hook decisions, and Claude responses.
5. **[VERIFICATION]** Confirm the resulting workspace lives under `.dev/eval-workspaces/<name>/`, NOT under `.claude/skills/<name>-workspace/`.
6. **[VERIFICATION]** Confirm that if Outcome B occurred, the hook error message contained the verbatim substring `.dev/eval-workspaces/`.
7. **[COMPLETION]** Capture session transcript + final directory listing in `TASKLIST_ROOT/artifacts/D-0012/evidence.md`.

**Acceptance Criteria:**
- Final workspace directory exists at `.dev/eval-workspaces/__ac1_probe__/` (or chosen probe name) AND does NOT exist at `.claude/skills/__ac1_probe__-workspace/`.
- Session transcript shows either Outcome A (no hook fire) or Outcome B (hook fired with redirect message); both are acceptable.
- If Outcome B, the recorded hook message contains the substring `.dev/eval-workspaces/`.
- Transcript captured in `TASKLIST_ROOT/artifacts/D-0012/evidence.md`.

**Validation:**
- Manual check: reviewer scans the transcript and confirms one of the two acceptable outcomes.
- Evidence: linkable artifact produced (`evidence.md` with transcript and final directory state).

**Dependencies:** T01.01, T01.02, T01.03, T02.01, T02.02, T02.03, T03.01, T03.02, T03.03 (M1-M3 must be landed).
**Rollback:** N/A (validation-only).
**Notes:** This is the canonical AC1 acceptance test. Discovery risk per roadmap: gaps surfaced loop back to M2/M3 with a revised fix.

---

### T05.02 -- AC2 test: fresh clone without hooks; verify-sync flags; CI blocks

| Field | Value |
|---|---|
| Roadmap Item IDs | R-013 |
| Why | Simulate a fresh clone without hooks installed (i.e., L1 bypassed). Create a `.claude/skills/<X>-workspace/` directory without SKILL.md. Verify `make verify-sync` flags it with the correct M2 error message, and CI blocks the PR. |
| Effort | M |
| Risk | Low |
| Risk Drivers | ci (matched keyword) |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0013 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0013/spec.md`
- `TASKLIST_ROOT/artifacts/D-0013/notes.md`
- `TASKLIST_ROOT/artifacts/D-0013/evidence.md`

**Deliverables:**
- A fresh-clone scenario (or scripted equivalent) demonstrating L1 (hook) is unavailable.
- A synthetic PR (or local `act` simulation) introducing `.claude/skills/__ac2_probe__-workspace/` (no SKILL.md), with a captured CI workflow failure showing the verbatim M2 message and a non-zero exit.

**Steps:**
1. **[PLANNING]** Set up a fresh clone (or simulate via stripping `.claude/settings.json` hooks section) so L1 is bypassed.
2. **[PLANNING]** Identify the target probe directory `.claude/skills/__ac2_probe__-workspace/` (no SKILL.md).
3. **[EXECUTION]** Create the probe directory locally.
4. **[EXECUTION]** Run `make verify-sync` and `make lint-architecture`; confirm both fail with M2 messages (T02.01 message OR T02.02 message).
5. **[EXECUTION]** Open a synthetic PR (or run local `act .github/workflows/quick-check.yml`) and confirm the workflow fails with the same messages.
6. **[VERIFICATION]** Confirm the captured CI failure output contains the verbatim substring `Move to .dev/eval-workspaces/` (from T02.01) OR `Workspace directories belong under .dev/eval-workspaces/` (from T02.02).
7. **[COMPLETION]** Remove the probe directory and capture local + CI failure logs in `TASKLIST_ROOT/artifacts/D-0013/evidence.md`.

**Acceptance Criteria:**
- Local `make verify-sync` against the `.claude/skills/__ac2_probe__-workspace/` probe (no SKILL.md) fails with verbatim T02.01 or T02.02 message.
- Synthetic PR (or `act` run) shows the CI workflow failing on the same probe with the same verbatim message; workflow status is FAIL.
- Probe directory removed before commit (validates no contamination).
- Local + CI logs captured in `TASKLIST_ROOT/artifacts/D-0013/evidence.md`.

**Validation:**
- Manual check: reviewer reviews local + CI failure logs and confirms verbatim message match.
- Evidence: linkable artifact produced (`evidence.md` with both logs).

**Dependencies:** T02.01, T02.02, T02.03 (M2 must be landed).
**Rollback:** N/A (validation-only). Probe directory is removed by step 7.
**Notes:** This is the canonical AC2 acceptance test. Effort M because both local and CI verification are required.

---

### T05.03 -- AC3 test: --output guard refuses .claude/ prefixes

| Field | Value |
|---|---|
| Roadmap Item IDs | R-014 |
| Why | Invoke `sc-release-split-protocol --output .claude/skills/foo/` (and equivalents under `.claude/agents/`, `.claude/commands/`). Verify the skill refuses (L3.1) BEFORE writing any artifacts. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0014 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0014/spec.md`
- `TASKLIST_ROOT/artifacts/D-0014/notes.md`
- `TASKLIST_ROOT/artifacts/D-0014/evidence.md`

**Deliverables:**
- Three captured invocations of `sc-release-split-protocol`, each with `--output` under one of the three forbidden prefixes (`.claude/skills/`, `.claude/agents/`, `.claude/commands/`), all aborting pre-write with the L3.1 refusal message.
- One captured invocation with a legitimate `--output` (e.g., `.dev/releases/current/test-output/`), confirming normal behavior.

**Steps:**
1. **[PLANNING]** Confirm T04.01 (and ideally T04.02) is landed; otherwise the guard does not exist and AC3 cannot be exercised.
2. **[PLANNING]** Identify three forbidden invocation forms (one per `.claude/<subdir>/`) and one legitimate form.
3. **[EXECUTION]** Run `sc-release-split-protocol --output .claude/skills/foo/`; confirm refusal pre-write; capture output.
4. **[EXECUTION]** Run `sc-release-split-protocol --output .claude/agents/foo/`; confirm refusal pre-write; capture output.
5. **[EXECUTION]** Run `sc-release-split-protocol --output .claude/commands/foo/`; confirm refusal pre-write; capture output.
6. **[EXECUTION]** Run `sc-release-split-protocol --output .dev/releases/current/test-output/`; confirm normal behavior; capture output.
7. **[VERIFICATION]** Confirm no files were written under `.claude/skills/foo/`, `.claude/agents/foo/`, or `.claude/commands/foo/` after the three forbidden runs.
8. **[COMPLETION]** Capture all four invocations and the post-run directory checks in `TASKLIST_ROOT/artifacts/D-0014/evidence.md`.

**Acceptance Criteria:**
- All three forbidden invocations abort pre-write and emit an error mentioning `.dev/` as the correct destination.
- Legitimate invocation proceeds normally and writes its outputs under `.dev/`.
- Post-run directory listing of the three forbidden prefixes shows the probe `foo/` directory was NOT created in any of them.
- All four invocations + post-run directory checks captured in `TASKLIST_ROOT/artifacts/D-0014/evidence.md`.

**Validation:**
- Manual check: reviewer runs the four invocations and confirms refusal pre-write for the three forbidden cases.
- Evidence: linkable artifact produced (`evidence.md` with four invocations and post-run directory state).

**Dependencies:** T04.01 (must be landed; T04.02 optional).
**Rollback:** N/A (validation-only).
**Notes:** This is the canonical AC3 acceptance test. The guard runs pre-write so no rollback of artifacts is needed.

---

### T05.04 -- AC4 test: grep CLAUDE.md pointers resolve to existing files

| Field | Value |
|---|---|
| Roadmap Item IDs | R-015 |
| Why | Assert all CLAUDE.md doc pointers resolve. `grep -E 'PLANNING\.md|TASK\.md|KNOWLEDGE\.md' CLAUDE.md` returns lines whose referenced files exist (post-D1.2 decision). |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | LIGHT |
| Confidence | [█████████-] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Quick sanity check |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0015 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0015/spec.md`
- `TASKLIST_ROOT/artifacts/D-0015/notes.md`
- `TASKLIST_ROOT/artifacts/D-0015/evidence.md`

**Deliverables:**
- Captured output of `grep -E 'PLANNING\.md|TASK\.md|KNOWLEDGE\.md' /config/workspace/IronClaude/CLAUDE.md` showing only `KNOWLEDGE.md` matches (post-T01.02 state).
- File existence checks for each matched filename: `KNOWLEDGE.md` exists; `PLANNING.md` and `TASK.md` do NOT match anymore.

**Steps:**
1. **[PLANNING]** Confirm T01.02 has landed (CLAUDE.md no longer references `PLANNING.md` or `TASK.md`).
2. **[EXECUTION]** Run `grep -E 'PLANNING\.md|TASK\.md|KNOWLEDGE\.md' /config/workspace/IronClaude/CLAUDE.md` and capture output.
3. **[EXECUTION]** For every filename in the grep output (only `KNOWLEDGE.md` should appear), run `test -f <filename>` and capture exit status.
4. **[VERIFICATION]** Confirm grep output shows `KNOWLEDGE.md` matches and zero `PLANNING.md` / `TASK.md` matches.
5. **[VERIFICATION]** Confirm `test -f KNOWLEDGE.md` exits 0.
6. **[COMPLETION]** Capture grep output + `test -f` outputs in `TASKLIST_ROOT/artifacts/D-0015/evidence.md`.

**Acceptance Criteria:**
- `grep -E 'PLANNING\.md|TASK\.md|KNOWLEDGE\.md' /config/workspace/IronClaude/CLAUDE.md` shows only `KNOWLEDGE.md` matches; zero `PLANNING.md` and zero `TASK.md` matches.
- Test FAILS if any unexpected `PLANNING.md` or `TASK.md` match appears in the grep output (post-T01.02 state must show only `KNOWLEDGE.md`).
- `test -f KNOWLEDGE.md` exits 0.
- Grep + `test -f` outputs captured in `TASKLIST_ROOT/artifacts/D-0015/evidence.md`.
- Result aligns with SC-004 success criterion in the source roadmap.

**Validation:**
- Manual check: reviewer runs the grep and the `test -f` and confirms expected exits.
- Evidence: linkable artifact produced (`evidence.md` with command outputs).

**Dependencies:** T01.02 (CLAUDE.md pointer repair must be landed).
**Rollback:** N/A (validation-only).
**Notes:** This is the canonical AC4 acceptance test and exercises SC-004 directly.

---

### T05.05 -- AC5 test: aggregate_benchmark + generate_review against relocated workspace

| Field | Value |
|---|---|
| Roadmap Item IDs | R-016 |
| Why | Run `aggregate_benchmark.py` and `generate_review.py` against `.dev/eval-workspaces/sc-release-split-protocol/`. Verify no regression (both scripts accept positional paths per merged-thesis §Acceptance). |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0016 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0016/spec.md`
- `TASKLIST_ROOT/artifacts/D-0016/notes.md`
- `TASKLIST_ROOT/artifacts/D-0016/evidence.md`

**Deliverables:**
- Captured outputs of `aggregate_benchmark.py .dev/eval-workspaces/sc-release-split-protocol/` and `generate_review.py .dev/eval-workspaces/sc-release-split-protocol/` (positional-path forms) showing exit 0 and result content equivalent (within tolerance) to a prior run against the legacy workspace location.
- Comparison notes recording any deltas observed between the prior run and the relocated run; non-regression confirmation.

**Steps:**
1. **[PLANNING]** Locate `aggregate_benchmark.py` and `generate_review.py` in the repo; confirm both accept positional path arguments per merged-thesis §Acceptance.
2. **[PLANNING]** Confirm `.dev/eval-workspaces/sc-release-split-protocol/` exists with the relocated artifacts (per commit `86d2749`).
3. **[EXECUTION]** Run `uv run python <path>/aggregate_benchmark.py .dev/eval-workspaces/sc-release-split-protocol/`; capture stdout, stderr, exit status.
4. **[EXECUTION]** Run `uv run python <path>/generate_review.py .dev/eval-workspaces/sc-release-split-protocol/`; capture stdout, stderr, exit status.
5. **[VERIFICATION]** Compare output (e.g., benchmark counts, generated review content) against the prior run from the legacy workspace; document any deltas in `notes.md`.
6. **[VERIFICATION]** Confirm no regression: both scripts exit 0 and results match prior outputs within expected tolerance.
7. **[COMPLETION]** Capture script outputs + comparison notes in `TASKLIST_ROOT/artifacts/D-0016/evidence.md`.

**Acceptance Criteria:**
- `aggregate_benchmark.py .dev/eval-workspaces/sc-release-split-protocol/` exits 0 and produces valid (non-empty, expected-schema) output. If a prior baseline is available, output is compared and any deltas documented in `notes.md`; if no prior baseline exists, comparison is marked N/A.
- `generate_review.py .dev/eval-workspaces/sc-release-split-protocol/` exits 0 and produces valid (expected-schema) output. If a prior baseline is available, output is compared and any deltas documented in `notes.md`; if no prior baseline exists, comparison is marked N/A.
- Any observed deltas are explained in `notes.md` and explicitly classified as "non-regression" or "regression"; the latter blocks the checkpoint.
- Script outputs + comparison notes captured in `TASKLIST_ROOT/artifacts/D-0016/evidence.md`.

**Validation:**
- Manual check: reviewer scans script outputs and comparison notes; confirms non-regression classification.
- Evidence: linkable artifact produced (`evidence.md` with all script outputs and the comparison).

**Dependencies:** None hard; presumes `.dev/eval-workspaces/sc-release-split-protocol/` is present (from commit `86d2749`).
**Rollback:** N/A (validation-only).
**Notes:** This is the canonical AC5 acceptance test. Per CLAUDE.md project rule, scripts must be invoked via `uv run`.

---

### T05.06 -- Checkpoint: End of Phase 5

| Field | Value |
|---|---|
| Roadmap Item IDs | R-012, R-013, R-014, R-015, R-016 |
| Why | Final exit gate: all 5 acceptance criteria (AC1-AC5) demonstrably pass via the layered defense. Aligns with SC-001 in the source roadmap. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None |
| Tier | LIGHT |
| Confidence | [██████████] 100% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Quick sanity check |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-CP05 |

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P05-END.md`

**Purpose:** Confirm AC1-AC5 evidence is captured and the layered defense holds end-to-end; release exit gate.

**Verification:** (exactly 3 bullets)
- AC1, AC2, AC3 evidence files (D-0012, D-0013, D-0014) all show pass results (outputs of T05.01, T05.02, T05.03).
- AC4 grep output (D-0015) shows only `KNOWLEDGE.md` matches and `test -f KNOWLEDGE.md` exits 0 (output of T05.04).
- AC5 script outputs (D-0016) show non-regression against the prior runs (output of T05.05).

**Exit Criteria:** (exactly 3 bullets)
- D-0012 through D-0016 all have evidence files captured under `TASKLIST_ROOT/artifacts/`.
- All five SC-### success criteria from the source roadmap are demonstrably satisfied or have a documented blocker.
- Release exit gate: no AC fails. If any AC fails, the checkpoint reports `Overall: Fail` and loops back to M2 and/or M3 with a revised fix per the M5 Risk Assessment in the roadmap.

**Steps:**
1. **[VERIFICATION]** Confirm each artifact listed in Verification is present on disk.
2. **[VERIFICATION]** Re-run the five AC sanity checks (open each `evidence.md` and confirm the recorded result) AND enumerate SC-001..SC-005 in the checkpoint report with explicit pass status, mapping each to evidence: SC-001 -> AC1-AC5 aggregate (T05.01-T05.05); SC-002 -> T05.02 (CI block); SC-003 -> probe `superclaude install` in a clean clone showing no `*-workspace/` directories under `.claude/skills/`; SC-004 -> T05.04; SC-005 -> `make sync-dev && make verify-sync` on a freshly merged branch exits 0 with no drift.
3. **[VERIFICATION]** Write the checkpoint report to `TASKLIST_ROOT/checkpoints/CP-P05-END.md` and list AC-by-AC pass status + SC-### success-criteria mapping.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/checkpoints/CP-P05-END.md` exists and contains `Overall: Pass` (or `Fail` with loopback plan).
- All 3 Verification bullets confirmed.
- All 3 Exit Criteria bullets met.
- Checkpoint report enumerates task IDs T05.01, T05.02, T05.03, T05.04, T05.05 and lists AC1-AC5 + SC-001-SC-005 pass status.

**Validation:**
- Manual check: reviewer confirms the report at `TASKLIST_ROOT/checkpoints/CP-P05-END.md` and the AC pass matrix.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T05.01, T05.02, T05.03, T05.04, T05.05
**Rollback:** N/A (checkpoints are read-only verifications)
