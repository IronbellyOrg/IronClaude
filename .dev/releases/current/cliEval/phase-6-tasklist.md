# Phase 6 -- Docs ADRs Hardening Sync Platform

**Phase Goal:** Close decisions, complete documentation (ADRs D-5..D-8, PROVENANCE.md), enforce source-of-truth discipline (`make sync-dev` + `make verify-sync`), record macOS platform follow-up plan (MIG-003), and prove single-command runnability on a clean dev machine. RyanW signs off ADRs, `make verify-sync` exits 0, and SC1-SC5 are satisfied.

### T06.01 -- SC1 ADR sign-offs D-5..D-8 in decisions.md

| Field | Value |
|---|---|
| Roadmap Item IDs | R-104 |
| Why | SC1 requires RyanW signs off 4 original + 4 new ADRs in `decisions.md`; OQ-1 resolution recorded; ADRs cross-reference roadmap deliverables. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | EXEMPT |
| Confidence | [█████████-] 95% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0105 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0105/spec.md`
- `TASKLIST_ROOT/artifacts/D-0105/notes.md`
- `TASKLIST_ROOT/artifacts/D-0105/evidence.md`

**Deliverables:**
- 8 signed-off ADR entries (D-1..D-8) in `.dev/releases/current/cliEval/decisions.md` with cross-references to roadmap deliverables.

**Steps:**
1. **[PLANNING]** Confirm OPS-001 (T01.25) entries queued D-5..D-8 for sign-off.
2. **[PLANNING]** Confirm OQ-1 resolution status from T01.25 and T06.09.
3. **[EXECUTION]** Add `signed_off_by: RyanW` and `signed_off_date: <ISO>` to each of D-1..D-8.
4. **[EXECUTION]** Add cross-reference roadmap deliverable IDs to each ADR.
5. **[VERIFICATION]** Manual review by RyanW.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T06.01/`.

**Acceptance Criteria:**
- File `.dev/releases/current/cliEval/decisions.md` contains 8 ADR entries (D-1..D-8), each with `signed_off_by` and `signed_off_date` fields populated.
- OQ-1 entry shows `resolution: <resolved-text>` field populated.
- Each ADR cross-references at least one roadmap deliverable ID.
- `TASKLIST_ROOT/artifacts/D-0105/spec.md` records the sign-off summary.

**Validation:**
- Manual check: read decisions.md and confirm 8 signed-off entries.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T01.25
**Rollback:** TBD (if not specified in roadmap)
**Notes:** SC1 success criterion landed here.

### T06.02 -- DOC-OQ9 macOS support roadmap entry

| Field | Value |
|---|---|
| Roadmap Item IDs | R-105 |
| Why | DOC-OQ9 records macOS timeline in decisions.md with owner + target; AC1 reaffirmed for v1 (Linux-only). |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | EXEMPT |
| Confidence | [█████████-] 95% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0106 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0106/spec.md`
- `TASKLIST_ROOT/artifacts/D-0106/notes.md`
- `TASKLIST_ROOT/artifacts/D-0106/evidence.md`

**Deliverables:**
- `decisions.md` entry recording the macOS follow-up plan with owner and target date; AC1 (Linux-only) cross-referenced.

**Steps:**
1. **[PLANNING]** Identify OQ-9 resolution status (macOS timeline).
2. **[PLANNING]** Confirm AC1 (T06.07) Linux-only declaration exists.
3. **[EXECUTION]** Add macOS follow-up entry to decisions.md naming owner + target date.
4. **[EXECUTION]** Cross-reference AC1 declaration.
5. **[VERIFICATION]** Manual review.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T06.02/`.

**Acceptance Criteria:**
- File `.dev/releases/current/cliEval/decisions.md` contains a `DOC-OQ9` entry naming the macOS follow-up owner and target date.
- Entry cross-references AC1 Linux-only declaration.
- OQ-9 status changes from `open` to `resolved` in decisions.md.
- `TASKLIST_ROOT/artifacts/D-0106/spec.md` records the macOS follow-up summary.

**Validation:**
- Manual check: read DOC-OQ9 entry in decisions.md.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** None
**Rollback:** TBD (if not specified in roadmap)
**Notes:** OQ-9 resolution gate for M6 exit.

### T06.03 -- DOC-OQ8 time-offset mechanism contract decision

| Field | Value |
|---|---|
| Roadmap Item IDs | R-106 |
| Why | DOC-OQ8 documents how Claude Code consumes `CLAUDE_FAKE_TIME_OFFSET` (or removes it): either confirmation that the claude binary honors the env var OR removal of the time-offset layer from FR-ISO1. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | EXEMPT |
| Confidence | [█████████-] 95% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0107 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0107/spec.md`
- `TASKLIST_ROOT/artifacts/D-0107/notes.md`
- `TASKLIST_ROOT/artifacts/D-0107/evidence.md`

**Deliverables:**
- `decisions.md` entry recording either (a) confirmation that claude honors `CLAUDE_FAKE_TIME_OFFSET` OR (b) removal of the time-offset layer from FR-ISO1 (T02.07).

**Steps:**
1. **[PLANNING]** Read OQ-8 status and prior investigation notes from T01.25.
2. **[PLANNING]** Confirm FR-ISO1 (T02.07) currently includes optional time-offset.
3. **[EXECUTION]** Document the decision (honor or remove) in decisions.md.
4. **[EXECUTION]** If removed, file follow-up task to strip time_offset_sec from HomeIsolation.
5. **[VERIFICATION]** Manual review.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T06.03/`.

**Acceptance Criteria:**
- File `decisions.md` contains a `DOC-OQ8` entry recording the chosen path (honor or remove).
- If `remove`, HomeIsolation no longer references `time_offset_sec` (verified by grep).
- OQ-8 status changes from `open` to `resolved`.
- `TASKLIST_ROOT/artifacts/D-0107/spec.md` records the decision.

**Validation:**
- Manual check: read DOC-OQ8 entry; grep HomeIsolation for time_offset reference if chosen path is `remove`.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T01.25, T02.07
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Carried from M1 OPS-001; final decision lands here.

### T06.04 -- DOC-OQ6 suite naming convention README

| Field | Value |
|---|---|
| Roadmap Item IDs | R-107 |
| Why | DOC-OQ6 documents the suite filename rules and records the `quick.yaml` follow-up plan in `cli/eval/suites/README.md`. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | EXEMPT |
| Confidence | [█████████-] 95% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0108 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0108/spec.md`
- `TASKLIST_ROOT/artifacts/D-0108/notes.md`
- `TASKLIST_ROOT/artifacts/D-0108/evidence.md`

**Deliverables:**
- `src/superclaude/cli/eval/suites/README.md` documenting suite naming convention beyond `real.yaml` and recording the `quick.yaml` follow-up.

**Steps:**
1. **[PLANNING]** Confirm SuiteLoader (T01.07) suite enumeration semantics.
2. **[PLANNING]** Decide naming convention rules (alphanumeric, snake_case, `.yaml`).
3. **[EXECUTION]** Author `suites/README.md` documenting naming + `quick.yaml` follow-up.
4. **[EXECUTION]** Add a note pointing back to DOC-OQ6 in decisions.md.
5. **[VERIFICATION]** Manual review.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T06.04/`.

**Acceptance Criteria:**
- File `src/superclaude/cli/eval/suites/README.md` documents the suite filename rules (alphanumeric, snake_case, `.yaml`).
- README records the `quick.yaml` follow-up plan as a planned follow-up.
- decisions.md DOC-OQ6 entry status changes to `resolved`.
- `TASKLIST_ROOT/artifacts/D-0108/spec.md` records the naming convention summary.

**Validation:**
- Manual check: read README and confirm fields present.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T01.07
**Rollback:** TBD (if not specified in roadmap)
**Notes:** P2 priority; not blocking SC5.

### T06.05 -- AC2 CI integration deferral note

| Field | Value |
|---|---|
| Roadmap Item IDs | R-108 |
| Why | AC2 records the CI deferral and follow-up trigger: local-only for v1; trigger for CI revisit recorded in decisions.md. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | EXEMPT |
| Confidence | [█████████-] 95% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0109 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0109/spec.md`
- `TASKLIST_ROOT/artifacts/D-0109/notes.md`
- `TASKLIST_ROOT/artifacts/D-0109/evidence.md`

**Deliverables:**
- `decisions.md` entry recording AC2 deferral: local-only for v1; CI revisit trigger documented.

**Steps:**
1. **[PLANNING]** Confirm v1 scope is Linux-only local-only per AC1.
2. **[PLANNING]** Identify a concrete CI revisit trigger (e.g., 3+ harness regressions in a month).
3. **[EXECUTION]** Add AC2 entry to decisions.md naming the deferral and revisit trigger.
4. **[EXECUTION]** Cross-reference AC1 declaration.
5. **[VERIFICATION]** Manual review.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T06.05/`.

**Acceptance Criteria:**
- File `decisions.md` contains an `AC2` entry stating "CI: deferred (local-only v1)" with a named revisit trigger.
- Cross-reference to AC1 Linux-only declaration is recorded.
- AC2 entry status is `resolved`.
- `TASKLIST_ROOT/artifacts/D-0109/spec.md` records the deferral summary.

**Validation:**
- Manual check: read AC2 entry in decisions.md.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** None
**Rollback:** TBD (if not specified in roadmap)
**Notes:** P2 priority; complements MIG-003 (T06.15).

### T06.06 -- Checkpoint: Phase 6 / Tasks T06.01-T06.05

| Field | Value |
|---|---|
| Roadmap Item IDs | R-104,R-105,R-106,R-107,R-108 |
| Why | Gate: verify SC1 ADR sign-offs, DOC-OQ9 macOS roadmap, DOC-OQ8 time-offset, DOC-OQ6 naming README, AC2 CI deferral before SC5 OQ list closure. |
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
| Deliverable IDs | D-CP06-MID-T01-T05 |

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P06-T01-T05.md`

**Purpose:** Confirm SC1 ADRs + DOC-OQ9/8/6 + AC2 entries before AC1/SC4/SC5/SC3/OPS-004 close M6.

**Verification:**
- `decisions.md` contains 8 signed-off ADRs (D-1..D-8) with cross-references.
- DOC-OQ9, DOC-OQ8, DOC-OQ6 entries recorded with resolutions.
- AC2 deferral entry recorded with revisit trigger.

**Exit Criteria:**
- 5 decisions.md entries (SC1, DOC-OQ9, DOC-OQ8, DOC-OQ6, AC2) present and resolved.
- `src/superclaude/cli/eval/suites/README.md` exists.
- Checkpoint report `CP-P06-T01-T05.md` records pass/fail per upstream task.

**Steps:**
1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
2. **[VERIFICATION]** Re-run the tier-proportional checks for the covered tasks.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/checkpoints/CP-P06-T01-T05.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report includes the task IDs it covers (T06.01-T06.05).

**Validation:**
- Manual check: reviewer confirms the report at the Checkpoint Report Path.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T06.01..T06.05
**Rollback:** N/A (checkpoints are read-only verifications)

### T06.07 -- AC1 Linux-only declaration in README + decisions

| Field | Value |
|---|---|
| Roadmap Item IDs | R-109 |
| Why | AC1 documents Linux-only v1 in README; `eval doctor` refuses non-Linux with a friendly error message. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | EXEMPT |
| Confidence | [█████████-] 95% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0110 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0110/spec.md`
- `TASKLIST_ROOT/artifacts/D-0110/notes.md`
- `TASKLIST_ROOT/artifacts/D-0110/evidence.md`

**Deliverables:**
- README update documenting Linux-only v1 scope; `eval doctor` non-Linux refusal message.

**Steps:**
1. **[PLANNING]** Confirm eval doctor (T01.13) entry point.
2. **[PLANNING]** Choose README section for AC1 declaration.
3. **[EXECUTION]** Add Linux-only declaration to README and decisions.md (`AC1` entry).
4. **[EXECUTION]** Wire `eval doctor` to refuse non-Linux platforms with a friendly error.
5. **[VERIFICATION]** Manual test on macOS or Windows stub (or pytest skip).
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T06.07/`.

**Acceptance Criteria:**
- File `README.md` documents Linux-only v1 scope at the eval CLI section.
- `eval doctor` on non-Linux platform (or stubbed `platform.system()=="Darwin"`) exits with a friendly error.
- decisions.md `AC1` entry status is `resolved`.
- `TASKLIST_ROOT/artifacts/D-0110/spec.md` records the platform policy.

**Validation:**
- Manual check: read README + run doctor with platform stub.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T01.13
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Pairs with MIG-003 macOS follow-up (T06.15).

### T06.08 -- SC4 effort estimate acknowledgment

| Field | Value |
|---|---|
| Roadmap Item IDs | R-110 |
| Why | SC4 records RyanW sign-off on LOC estimate ~1,340 harness + ~3,000-4,500 eval bodies; ledger updated post-implementation with actual LOC. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | EXEMPT |
| Confidence | [█████████-] 95% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0111 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0111/spec.md`
- `TASKLIST_ROOT/artifacts/D-0111/notes.md`
- `TASKLIST_ROOT/artifacts/D-0111/evidence.md`

**Deliverables:**
- `decisions.md` entry recording signed-off LOC estimate + actual LOC delta post-implementation.

**Steps:**
1. **[PLANNING]** Confirm SC1 ADR ledger (T06.01) infrastructure.
2. **[PLANNING]** Capture actual LOC for harness + eval bodies via `cloc` or `tokei`.
3. **[EXECUTION]** Record signed-off estimate + actual LOC in decisions.md SC4 entry.
4. **[EXECUTION]** Document any delta beyond +/-15% with justification.
5. **[VERIFICATION]** Manual review by RyanW.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T06.08/`.

**Acceptance Criteria:**
- File `decisions.md` contains an `SC4` entry with signed-off LOC estimate and actual LOC measurement.
- Delta is recorded and within +/-15% of estimate (or justified explicitly).
- SC4 entry status is `resolved`.
- `TASKLIST_ROOT/artifacts/D-0111/spec.md` records the estimate vs actual.

**Validation:**
- Manual check: read SC4 entry; confirm signed_off_by populated.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T06.01
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Post-implementation ledger; runs after eval suite lands.

### T06.09 -- SC5 OQ-1..OQ-10 resolution ledger

| Field | Value |
|---|---|
| Roadmap Item IDs | R-111 |
| Why | SC5 requires all 10 OQ-xxx items recorded as resolved in decisions.md; every OQ entry has a `resolution:` field signed-off by RyanW. |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | EXEMPT |
| Confidence | [█████████-] 95% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0112 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0112/spec.md`
- `TASKLIST_ROOT/artifacts/D-0112/notes.md`
- `TASKLIST_ROOT/artifacts/D-0112/evidence.md`

**Deliverables:**
- `decisions.md` ledger showing all 10 OQ-xxx entries (OQ-1..OQ-10) resolved and signed-off.

**Steps:**
1. **[PLANNING]** Enumerate the 10 OQ-xxx items: OQ-1..OQ-10.
2. **[PLANNING]** Confirm individual resolution tasks (T01.25, T02.02, T04.15, T04.16, T05.01, T06.02, T06.03, T06.04).
3. **[EXECUTION]** Add `resolution:` field to each OQ-xxx entry in decisions.md.
4. **[EXECUTION]** Add `signed_off_by: RyanW` to each.
5. **[VERIFICATION]** Manual review.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T06.09/`.

**Acceptance Criteria:**
- File `decisions.md` lists all 10 OQ-xxx entries (OQ-1..OQ-10), each with `resolution` and `signed_off_by` fields populated.
- All entries show status `resolved`.
- `grep -c "status: resolved" decisions.md` returns >= 10.
- `TASKLIST_ROOT/artifacts/D-0112/spec.md` records the ledger summary.

**Validation:**
- Manual check: read decisions.md and confirm all 10 entries resolved.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T01.25, T02.02, T04.15, T04.16, T05.01, T06.02, T06.03, T06.04
**Rollback:** TBD (if not specified in roadmap)
**Notes:** SC5 success criterion lands here.

### T06.10 -- SC3 zero-new-deps verification

| Field | Value |
|---|---|
| Roadmap Item IDs | R-112 |
| Why | SC3 verifies `pyproject.toml` has no new external deps beyond pexpect (vendored) + jsonschema (transitive); `uv pip list` diff post-implementation shows only ptytest-vendored sources changed; CI assertion enforces. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | EXEMPT |
| Confidence | [█████████-] 95% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0113 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0113/spec.md`
- `TASKLIST_ROOT/artifacts/D-0113/notes.md`
- `TASKLIST_ROOT/artifacts/D-0113/evidence.md`

**Deliverables:**
- Verification artifact `TASKLIST_ROOT/evidence/T06.10/dep-diff.log` showing zero new top-level deps post-implementation.

**Steps:**
1. **[PLANNING]** Confirm AC3 CI check (T01.17) is enforced.
2. **[PLANNING]** Snapshot baseline `uv pip list` from pre-eval-CLI commit.
3. **[EXECUTION]** Capture post-implementation `uv pip list` and diff against baseline.
4. **[EXECUTION]** Save diff to `dep-diff.log` confirming only ptytest-vendored entries.
5. **[VERIFICATION]** Run `make verify-deps` and confirm exit 0.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T06.10/`.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/evidence/T06.10/dep-diff.log` shows zero new top-level deps post-implementation.
- `make verify-deps` exits 0 on the final tree.
- decisions.md SC3 entry status is `resolved`.
- `TASKLIST_ROOT/artifacts/D-0113/spec.md` records the verification outcome.

**Validation:**
- Manual check: read dep-diff.log and confirm empty additions.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T01.17
**Rollback:** TBD (if not specified in roadmap)
**Notes:** SC3 success criterion lands here.

### T06.11 -- Define OPS-004 validation command sequence

| Field | Value |
|---|---|
| Roadmap Item IDs | R-113 |
| Why | OPS-004 defines the validation command sequence using UV and make targets: targeted eval tests, `make verify-sync`, eval doctor, single eval run; results linked in artifacts. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0114 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0114/spec.md`
- `TASKLIST_ROOT/artifacts/D-0114/notes.md`
- `TASKLIST_ROOT/artifacts/D-0114/evidence.md`

**Deliverables:**
- `docs/eval/validation-commands.md` documenting the validation command sequence + linked evidence locations.

**Steps:**
1. **[PLANNING]** Confirm MIG-001 source sync gate (T06.14) is wired.
2. **[PLANNING]** Enumerate validation commands: targeted pytest, make verify-sync, eval doctor, eval run --suite real --eval E1.
3. **[EXECUTION]** Author `docs/eval/validation-commands.md` documenting each command + intended evidence path.
4. **[EXECUTION]** Run each command and link its output under `TASKLIST_ROOT/evidence/T06.11/`.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_validation_commands.py -v`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T06.11/`.

**Acceptance Criteria:**
- File `docs/eval/validation-commands.md` documents the 4 validation commands in order.
- Each command's evidence path is linked under `TASKLIST_ROOT/evidence/T06.11/`.
- All 4 commands exit 0 on the current tree.
- `TASKLIST_ROOT/artifacts/D-0114/spec.md` records the command sequence.

**Validation:**
- Manual check: run the 4 validation commands and inspect linked evidence.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T06.14
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Forms the basis of OPS-005 release checklist (T06.13).

### T06.12 -- Checkpoint: Phase 6 / Tasks T06.07-T06.11

| Field | Value |
|---|---|
| Roadmap Item IDs | R-109,R-110,R-111,R-112,R-113 |
| Why | Gate: verify AC1 Linux declaration, SC4 effort estimate, SC5 OQ ledger, SC3 zero-new-deps, OPS-004 validation commands before release checklist + sync migration + MIG-003 close M6. |
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
| Deliverable IDs | D-CP06-MID-T07-T11 |

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P06-T07-T11.md`

**Purpose:** Confirm AC1 + SC4 + SC5 + SC3 + OPS-004 before MIG-001 + OPS-005 + MIG-003 close M6.

**Verification:**
- AC1 Linux-only declaration in README; doctor refuses non-Linux.
- SC4, SC5, SC3 entries resolved in decisions.md with signed-off fields.
- OPS-004 validation-commands.md exists and all 4 commands exit 0.

**Exit Criteria:**
- `make verify-deps` exits 0; `make verify-sync` exits 0.
- `grep -c "status: resolved" decisions.md` returns >= 10.
- Checkpoint report `CP-P06-T07-T11.md` records pass/fail per upstream task.

**Steps:**
1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
2. **[VERIFICATION]** Re-run the tier-proportional checks for the covered tasks.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/checkpoints/CP-P06-T07-T11.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report includes the task IDs it covers (T06.07-T06.11).

**Validation:**
- Manual check: reviewer confirms the report at the Checkpoint Report Path.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T06.07..T06.11
**Rollback:** N/A (checkpoints are read-only verifications)

### T06.13 -- Assemble OPS-005 release checklist

| Field | Value |
|---|---|
| Roadmap Item IDs | R-114 |
| Why | OPS-005 assembles release evidence: eval doctor green; `make verify-sync` exits 0; targeted tests pass; full-run artifacts linked; follow-ups listed. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0115 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0115/spec.md`
- `TASKLIST_ROOT/artifacts/D-0115/notes.md`
- `TASKLIST_ROOT/artifacts/D-0115/evidence.md`

**Deliverables:**
- `docs/eval/release-checklist.md` assembling release evidence + follow-up plan; cross-references all OPS-004 commands.

**Steps:**
1. **[PLANNING]** Confirm OPS-004 (T06.11) validation commands documented.
2. **[PLANNING]** Inventory follow-ups (MIG-003, quick.yaml, macOS).
3. **[EXECUTION]** Author `docs/eval/release-checklist.md` enumerating evidence + follow-ups.
4. **[EXECUTION]** Cross-link each item to its evidence path.
5. **[VERIFICATION]** Walk through the checklist on the current tree.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T06.13/`.

**Acceptance Criteria:**
- File `docs/eval/release-checklist.md` lists `eval doctor`, `make verify-sync`, targeted tests, full-run artifacts, follow-ups.
- Each checklist item links to evidence under `TASKLIST_ROOT/evidence/`.
- Follow-ups section names MIG-003 (T06.15) and `quick.yaml` deferral.
- `TASKLIST_ROOT/artifacts/D-0115/spec.md` records the checklist summary.

**Validation:**
- Manual check: walk through the checklist and confirm each item.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T06.11
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Last process artifact before MIG-001 sync close.

### T06.14 -- MIG-001 source sync migration

| Field | Value |
|---|---|
| Roadmap Item IDs | R-115 |
| Why | MIG-001 syncs eval CLI sources from `src/superclaude/` into `.claude/` dev copies after implementation; `make verify-sync` exits 0; no direct `.claude/` source edits; sync evidence captured. |
| Effort | S |
| Risk | Medium |
| Risk Drivers | data (migration keyword) |
| Tier | STRICT |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena | Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0116 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0116/spec.md`
- `TASKLIST_ROOT/artifacts/D-0116/notes.md`
- `TASKLIST_ROOT/artifacts/D-0116/evidence.md`

**Deliverables:**
- Sync evidence artifact `TASKLIST_ROOT/evidence/T06.14/sync.log` recording `make sync-dev && make verify-sync` exit 0.

**Steps:**
1. **[PLANNING]** Confirm AC11 source-of-truth gate (T01.20) is wired.
2. **[PLANNING]** Confirm OPS-003 retention policy (T04.21).
3. **[EXECUTION]** Run `make sync-dev` to copy eval CLI sources into `.claude/`.
4. **[EXECUTION]** Run `make verify-sync` and capture log to `sync.log`.
5. **[VERIFICATION]** Sub-agent quality-engineer review of sync log.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T06.14/`.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/evidence/T06.14/sync.log` records `make sync-dev` followed by `make verify-sync` both exiting 0.
- No direct edits to `.claude/cli/eval/` exist; `git status` shows only `src/superclaude/` deltas before sync.
- Pre-commit hook (T01.20) rejects any synthetic `.claude/` direct edit.
- `TASKLIST_ROOT/artifacts/D-0116/spec.md` records the sync outcome.

**Validation:**
- Manual check: run `make sync-dev && make verify-sync` and inspect exit codes.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T01.20, T04.21
**Rollback:** TBD (if not specified in roadmap)
**Notes:** STRICT tier per Section 5.3.2 (migration keyword + critical-path override).

### T06.15 -- MIG-003 platform follow-up plan

| Field | Value |
|---|---|
| Roadmap Item IDs | R-116 |
| Why | MIG-003 records macOS and future CI support as follow-up scope outside v1 Linux-local delivery; macOS non-goal preserved; CI non-goal preserved; follow-up roadmap item created. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | EXEMPT |
| Confidence | [█████████-] 95% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0117 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0117/spec.md`
- `TASKLIST_ROOT/artifacts/D-0117/notes.md`
- `TASKLIST_ROOT/artifacts/D-0117/evidence.md`

**Deliverables:**
- Follow-up roadmap entry for v2 covering macOS + CI; recorded as deferred scope (not blocking v1 release).

**Steps:**
1. **[PLANNING]** Confirm DOC-OQ9 (T06.02) macOS entry and AC2 (T06.05) CI deferral.
2. **[PLANNING]** Define follow-up scope: macOS + CI integration.
3. **[EXECUTION]** Author follow-up roadmap entry (e.g., new section in decisions.md or a separate file).
4. **[EXECUTION]** Confirm no v1 blocking work added.
5. **[VERIFICATION]** Manual review.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T06.15/`.

**Acceptance Criteria:**
- A follow-up roadmap entry (in decisions.md or `docs/eval/v2-followups.md`) records macOS + CI as deferred scope.
- macOS non-goal and CI non-goal are preserved (referenced from AC1 + AC2).
- No new v1-blocking work is added (verified by reading the follow-up entry).
- `TASKLIST_ROOT/artifacts/D-0117/spec.md` records the follow-up summary.

**Validation:**
- Manual check: read follow-up entry and confirm scope deferred.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T06.02, T06.05
**Rollback:** TBD (if not specified in roadmap)
**Notes:** P2 priority; closes M6 with platform clarity.

### T06.16 -- Checkpoint: End of Phase 6

| Field | Value |
|---|---|
| Roadmap Item IDs | R-104..R-116 |
| Why | M6 exit gate: RyanW signs off ADRs, `make verify-sync` exits 0, SC1-SC5 satisfied, macOS roadmap entry recorded in decisions.md. |
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
| Deliverable IDs | D-CP06 |

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P06-END.md`

**Purpose:** M6 exit gate: SC1-SC5 satisfied, sync verified, macOS follow-up recorded, release checklist green.

**Verification:**
- SC1 ADRs D-1..D-8 signed off; SC2 manifest covers 15 evals; SC3 zero new deps; SC4 effort estimate ack'd; SC5 OQ-1..OQ-10 resolved.
- `make verify-sync` exits 0; `make verify-deps` exits 0.
- MIG-003 follow-up entry recorded; release checklist `docs/eval/release-checklist.md` walked through green.

**Exit Criteria:**
- All 5 success criteria (SC1-SC5) record `status: resolved` in decisions.md.
- `make sync-dev && make verify-sync` exits 0.
- Checkpoint report `CP-P06-END.md` records pass/fail per task in Phase 6.

**Steps:**
1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
2. **[VERIFICATION]** Re-run the tier-proportional checks for the covered tasks.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/checkpoints/CP-P06-END.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report includes the task IDs it covers (T06.01-T06.15).

**Validation:**
- Manual check: reviewer confirms the report at the Checkpoint Report Path.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T06.01..T06.15
**Rollback:** N/A (checkpoints are read-only verifications)
