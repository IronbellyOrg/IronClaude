# /sc:reflect UC-1 Pre-Execution Coverage Audit — Requirements Coverage Lens

Reviewer: independent coverage audit agent  
Spec: `/config/workspace/IronClaude/.dev/brainstorms/20260610-234750-pr-review-auto-remediation/merged-spec.md`  
Tasklist: `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-submit-pr-20260611-030241/TASK-RF-submit-pr-20260611-030241.md`

## 1. Requirement Inventory Count

I counted the driving spec as the following auditable requirement inventory:

| Requirement family | Count | Source evidence |
|---|---:|---|
| FR subrequirements | 31 | FR-1.1..1.7, FR-2.1..2.5, FR-3.1..3.5, FR-4.1..4.4, FR-5.1..5.4, FR-6.1..6.5, FR-7.1 at spec lines 160-245 |
| NFR | 8 | NFR-1..NFR-8 at spec lines 796-808 |
| AC | 15 | AC-1..AC-15 at spec lines 972-995 |
| Normative invariants | 5 | INV-001/007/009/015/016 in frontmatter/spec matrix plus bodies at spec lines 316-331, 600-606, 754-776, 813-822, 1076-1082 |
| Component inventory | 11 | C1, C2, DET, C3, C3a, C3b, C4, LG, VAL, C5, C6 at spec lines 109-121 |
| §6.3 test layout files/modules | 21 | task prompt calls out 21; spec layout is `__init__.py`, `conftest.py`, 20 `test_*.py` modules, fixtures at spec lines 424-469 |
| Canonical tests named by prompt | 7 | T-626-OFF-BY-ONE, T-VANISHED-MONO, T-CRASH-WINDOW-NO-DOUBLE-PUSH, T-ZERO-EDIT-NO-PUSH, T-VALIDATED-NOT-VERIFIED, T-N50, T-210 at spec lines 401-406, 641-659, 775-776, 878-887, 813-822 |
| §11 run-log event types + idempotency sets | 38 | 33 event types: 32 listed at spec lines 723-731 plus correction `push_aborted_or_not_landed` from spec lines 765-772; 5 sets at spec lines 735-745 |
| §12 failure modes | 12 | FM-1..FM-12 at spec lines 778-792 |
| §10 validation gates | 6 | VG-1..VG-6 at spec lines 669-676 |
| **Total audited units** | **154** | Includes C3b because it is an explicit §2 component even though the prompt shorthand omitted it. |

Scoring: COVERED = 1.0, PARTIAL = 0.5, UNMAPPED = 0.0.

## 2. Coverage Matrix

### 2.1 Functional Requirements

| Spec ID | Status | Tasklist coverage | Notes |
|---|---|---|---|
| FR-1.1 | COVERED | Step 4.5; Step 9.1 | Full signature, choices, command options. |
| FR-1.2 | COVERED | Step 4.5 | Default monitor=0 / not armed. |
| FR-1.3 | COVERED | Step 7.1; Step 7.2; Step 7.3; Step 9.5 | `--repo` pin and static grep covered. |
| FR-1.4 | PARTIAL | Step 9.6 | Spec requires origin, `gh auth status`, `git fetch origin`, rebase-if-behind, URL owner verification (spec line 168). Task tests wrong origin, behind/rebase, wrong-owner URL (task line 382) but does not explicitly require/test `gh auth status` or `git fetch origin` execution. |
| FR-1.5 | COVERED | Step 4.6 | Monitor arm exactly once for `--monitor 1`, never for 0. |
| FR-1.6 | COVERED | Step 4.5; Step 6.5 | Poll interval min/default timeout honored. |
| FR-1.7 | COVERED | Step 4.5; Step 8.4 | Resume from JSONL and recovery path. |
| FR-2.1 | COVERED | Step 2.3; Step 2.4; Step 6.1; Step 7.1 | Poll surfaces and three states covered. |
| FR-2.2 | COVERED | Step 2.0; Step 2.1; Step 2.3; Step 2.4; Step PGA.2 | Locked detection contract and bot filtering covered. |
| FR-2.3 | COVERED | Step 6.1; Step 6.5 | Interval/timeout wall-clock coverage. |
| FR-2.4 | COVERED | Step 4.6; Step 8.4 | Session-close limitation and resume reconstruction covered. Note: the task asks for `session_closed` logging, but the closed 33-event enum does not list `session_closed`; this is an implementation consistency risk, not a coverage miss. |
| FR-2.5 | COVERED | Step 6.1; Step 6.5; Step 6.6 | Backoff and reset covered. |
| FR-3.1 | COVERED | Step 5.1; Step 5.4 | Rubric reuse and remap tests. |
| FR-3.2 | COVERED | Step 5.1; Step 5.3; Step 5.4 | Medium/high/low routing covered; authorized correction excludes `--depth quick --fix`. |
| FR-3.3 | COVERED | Step 5.3; Step 5.6 | Scope seed from file:line. |
| FR-3.4 | COVERED | Step 5.3; Step 5.6 | Batching, route decision before dispatch, round budget. |
| FR-3.5 | COVERED | Step 5.2; Step 5.5; Step PGB.7 fidelity-agent-3 | Verify-before-remediate including unverified report-only/no-round. |
| FR-4.1 | COVERED | Step 4.1; Step 4.2; Step 4.4; Step 4.7 | L1 zero edits and offer prompt. |
| FR-4.2 | COVERED | Step 6.2; Step 6.3; Step 4.7 | L2 fixes locally, no commit/push/reply. |
| FR-4.3 | COVERED | Step 4.1; Step 4.2; Step 7.4; Step 4.7 | L3 full flow and G-push conjunction. |
| FR-4.4 | COVERED | Step 4.1; Step 4.2; Step 4.7 | Human-decision HALT override. |
| FR-5.1 | COVERED | Step 6.2; Step 6.4 | Targeted vs cross-cutting validation. |
| FR-5.2 | COVERED | Step 6.2; Step 6.4; Steps 11.4-11.5 | Lint and format split. |
| FR-5.3 | COVERED | Step 6.2; Step 6.4 | No push/reply/resolve on fail; retry no counter increment. |
| FR-5.4 | COVERED | Step 6.2; Step 6.4 | Single `validated` status definition. |
| FR-6.1 | COVERED | Step 7.2; Step 7.3; Step 7.5 | Specific thread reply, resolve, applied-edits text. |
| FR-6.2 | COVERED | Step 7.5; Step 8.2; Step 8.5 | Zero findings and max-round stop. |
| FR-6.3 | COVERED | Steps 8.1, 8.2, 8.5; Step PGB.7 fidelity-agent-2 | INV-001 single increment edge, `>=`, monotonicity. |
| FR-6.4 | COVERED | Step 7.5; Step 8.5 | Residual summary after cap. |
| FR-6.5 | COVERED | Step 7.2; Step 7.5; Step PGB.7 fidelity-agent-3 | Suggestion block, summary thread, idempotency. |
| FR-7.1 | COVERED | Step 9.2; Step 9.4 | Hook offer includes both commands and stays fail-open. |

### 2.2 Non-Functional Requirements

| Spec ID | Status | Tasklist coverage | Notes |
|---|---|---|---|
| NFR-1 | COVERED | Step 8.3; Step 8.7; Step 7.5 | Idempotent replies/resolves/fix-key. |
| NFR-2 | COVERED | Step 6.1; Step 6.5; Step 6.6 | Backoff and interval safety. |
| NFR-3 | COVERED | Step 8.3; Step 8.6; Step 11.3 | JSONL observability/resumability. |
| NFR-4 | COVERED | Step 2.3; Step 2.4; Step 5.4; Step 8.8 | Unknown severity/bot/shape behavior. |
| NFR-5 | COVERED | Step 9.5 | T-N40/T-N41 static checks for absolute paths/single-line commands. |
| NFR-6 | COVERED | Step 4.1; Step 4.2; Step 5.1; Step 8.1; Step 8.2; Step 9.5; Step PGB.2 core-purity | Deterministic core purity heavily covered. |
| NFR-7 | UNMAPPED | None found | Spec requires authenticated `gh` + local git only, no tokens in run-log, redact credential-bearing env/stderr (spec line 807). Tasklist has no T-N51 test, no redaction implementation item, and no explicit token-pattern scrubber in run-log/recovery/validation steps. |
| NFR-8 | UNMAPPED | None found | Spec requires deterministic replay for same fixtures+state (spec line 808). Tasklist has no T-N52 test and no item asserting identical decisions/run-log on replay. |

### 2.3 Acceptance Criteria

| Spec ID | Status | Tasklist coverage | Notes |
|---|---|---|---|
| AC-1 | COVERED | Step 4.5; Step 4.6 | `--monitor 0` zero monitor activity. |
| AC-2 | COVERED | Step 4.7 | Full L3 1 Medium + 1 High flow. |
| AC-3 | COVERED | Step 4.7 | L1 zero edit + prompt. |
| AC-4 | COVERED | Step 4.7; Step 6.3 | L2 leaves changes, no pushes. |
| AC-5 | COVERED | Step 4.7 | Human-decision HALT. |
| AC-6 | COVERED | Step 8.5 | Max-round and off-by-one matrix. |
| AC-7 | COVERED | Step 9.5; Step 7.1-7.3 | Repo pin. |
| AC-8 | COVERED | Step 2.0-2.6; Step PGA.2 | Detection lock gate. |
| AC-9 | COVERED | Step 9.5; Step PGB.2 core-purity | No `gh`/`git` in pure core. |
| AC-10 | COVERED | Step 6.5; Step 6.6 | 403 backoff. |
| AC-11 | COVERED | Step 4.5; Step 8.4 | Resume rebuild. |
| AC-12 | COVERED | Step 8.4; Step 8.8 | Crash-window no duplicate push/resume idempotency. |
| AC-13 | PARTIAL | Step 8.9 | Spec says a validated fix that drifts untested behavior still pushes and records `validated_not_verified` + behavioral failures (spec lines 813-822, 993). Task Step 8.9 reframes it as a finding whose validation passed but was never grounded/verified and says it is flagged/not auto-resolved (task line 357). That conflates INV-015 with FR-3.5 input verification and misses the explicit “push occurs, record audit” behavior. |
| AC-14 | COVERED | Step 5.5 | False-positive finding → unverified/report-only/no round. |
| AC-15 | COVERED | Step 7.2; Step 7.5 | Suggestion-block and single summary thread. |

### 2.4 Normative Invariants

| Spec ID | Status | Tasklist coverage | Notes |
|---|---|---|---|
| INV-001 | COVERED | Step 8.1; Step 8.2; Step 8.5; Step PGB.7 fidelity-agent-2 | Single increment edge and fence-post tests. |
| INV-007 | COVERED | Step 7.4; Step 8.4; Step 8.8; Step PGB.7 fidelity-agent-2 | Push triad and crash-window 3-way. |
| INV-009 | COVERED | Step 8.3; Step 8.7; Step 10.2; Step 7.5 | `fix_key` comment_id-independent; thread-scoped reply key. |
| INV-015 | PARTIAL | Step 8.9 | Same gap as AC-13: task covers a validated-vs-verified audit superficially but changes the semantics from “validated fix may push, record residual risk” to “not grounded/not auto-resolved.” |
| INV-016 | COVERED | Step 4.1; Step 4.2; Step 7.4; Step 4.7; Step PGB.7 fidelity-agent-1 | 5-predicate G-push conjunction including applied_edits>0. |

### 2.5 Component Inventory (§2)

| Component | Status | Tasklist coverage | Notes |
|---|---|---|---|
| C1 | COVERED | Step 4.1; Step 4.4; Step 9.1 | Orchestrator/FSM/command. |
| C2 | COVERED | Step 6.1; Step 7.1 | Poller ref + script. |
| DET | COVERED | Step 2.0; Step 2.1 | Detection contract. |
| C3 | COVERED | Step 5.1; Step 5.4 | Severity router/rubric reuse. |
| C3a | COVERED | Step 5.2; Step 5.5 | Verification wave. |
| C3b | COVERED | Step 5.3; Step 5.6 | Troubleshoot dispatcher. |
| C4 | COVERED | Step 7.2; Step 7.3; Step 7.5 | Reply/resolve. |
| LG | COVERED | Steps 8.1-8.8 | Loop guard/run-log/recovery. |
| VAL | COVERED | Step 4.4; Step 6.2; Steps 11.1-11.6 | Validator gate list and validation execution. |
| C5 | COVERED | Step 9.2; Step 9.4 | Hook edit/test. |
| C6 | COVERED | Steps 4.5-4.7, 5.4-5.6, 6.4-6.6, 7.5, 8.5-8.10, 9.4-9.6, 10.1-10.3 | Test suite + fixtures. |

### 2.6 §6.3 Test File Layout and Canonical Tests

| Requirement | Status | Tasklist coverage | Notes |
|---|---|---|---|
| `tests/submit_pr/__init__.py` | COVERED | Step 10.1 | Present. |
| `conftest.py` | COVERED | Step 10.1 | Fixtures covered. |
| 20 named `test_*.py` modules in spec layout | COVERED | Steps 2.4, 4.5, 4.6, 4.7, 5.4, 5.5, 5.6, 6.4, 6.5, 6.6, 7.5, 8.5, 8.6, 8.7, 8.8, 8.9, 8.10, 9.4, 9.5, 9.6 | Every spec-listed module from lines 430-449 has a task item. |
| “21 test files” count | PARTIAL | Objective line 79; Step 10.1 + 20 modules | The task objective says “21 test modules” (task line 79), but the detailed checklist creates 20 `test_*.py` modules plus `conftest.py` and `__init__.py`. The spec layout itself appears to list 20 test modules. The task should normalize the count to avoid executor confusion. |
| 18 fixtures | COVERED | Step 10.2; Step 10.3 | All fixture names covered. |
| T-626-OFF-BY-ONE | COVERED | Step 8.5 | Marked p0/loop_guard. |
| T-VANISHED-MONO | COVERED | Step 8.5 | Monotonicity covered. |
| T-CRASH-WINDOW-NO-DOUBLE-PUSH | COVERED | Step 8.8 | Crash-window test covered, though wording should be kept consistent around total push count vs no duplicate push. |
| T-ZERO-EDIT-NO-PUSH | COVERED | Step 4.7 | Predicate 5 covered. |
| T-VALIDATED-NOT-VERIFIED | PARTIAL | Step 8.9 | Semantic mismatch with INV-015/AC-13 as above. |
| T-N50 | COVERED | Step 9.5 | Core purity static grep. |
| T-210 | COVERED | Step 2.4; Step 2.5 | Locked:false HALT. |

### 2.7 Run-Log (§11), Failure Modes (§12), Validation Gates (§10)

| Requirement | Status | Tasklist coverage | Notes |
|---|---|---|---|
| 33 event types | COVERED | Step 2.2; Step 8.1; Step 8.3; Step PGB.7 fidelity-agent-2 | Authorized correction from 32+1 is encoded. |
| 5 idempotency sets | COVERED | Step 8.1; Step 8.3; Step 8.7; Step PGB.7 fidelity-agent-2 | Includes `fix_key=sha256(path+line+finding_body)`. |
| FM-1..FM-12 | COVERED | Step 8.8 | One test per FM. |
| VG-1 | COVERED | Step 6.2; Step 6.4 | Targeted tests. |
| VG-2 | COVERED | Step 6.2; Step 6.4 | Cross-cutting `make test` escalation. |
| VG-3 | COVERED | Step 6.2; Step 6.4; Step 11.4 | `make lint`. |
| VG-4 | COVERED | Step 6.2; Step 6.4; Step 11.5 | Ruff format check. |
| VG-5 | COVERED | Step 11.2; Step 11.6 | `make verify-sync`. |
| VG-6 | COVERED | Step 9.6; Step 6.2 | Fork URL / PR target blocks arm. |

## 3. Explicit Gaps

### UNMAPPED

1. **NFR-7 — Security/token redaction.**  
   - Spec: no tokens in run-log; redact credential-bearing env/stderr (spec line 807).  
   - Gap: no task item adds a scrubber, no run-log redaction test, no T-N51 mapping.  
   - Required fix: add implementation to `run_log.py`/validation artifact capture for token-pattern redaction and add `tests/submit_pr/test_run_log.py::T_N51` or equivalent.

2. **NFR-8 — Deterministic replay.**  
   - Spec: same fixtures + same initial state produce identical classifier/counter/routes/terminal outcome (spec line 808).  
   - Gap: no T-N52 mapping and no replay-equivalence test.  
   - Required fix: add a deterministic replay test over representative fixtures that compares decisions/run-log-normalized output across two runs.

### PARTIAL

1. **FR-1.4 — pre-PR checks are incomplete.**  
   - Spec includes origin, `gh auth status`, `git fetch origin`, rebase-if-behind, URL verification (spec line 168).  
   - Task Step 9.6 covers wrong origin, behind/rebase, wrong-owner URL (task line 382), but not `gh auth status` or an explicit `git fetch origin` precondition/assertion.

2. **INV-015 / AC-13 / T-VALIDATED-NOT-VERIFIED — semantic mismatch.**  
   - Spec says a validated fix can still drift untested behavior; push occurs and run-log records `validated_not_verified` + behavioral-test failures (spec lines 813-822 and AC-13 at line 993).  
   - Task Step 8.9 says a finding “validation passed but was never grounded” is flagged and “not auto-resolved” (task line 357), conflating this residual post-validation risk with FR-3.5 verify-before-remediate input grounding.  
   - Required fix: rewrite Step 8.9 to assert `push_count == 1`, `validation_status == "validated_not_verified"`, behavioral failures are recorded, and this is distinct from FR-3.5 unverified-input report-only behavior.

3. **§6.3 test-file count normalization.**  
   - Spec layout names 20 `test_*.py` modules plus `__init__.py`, `conftest.py`, and fixtures; the prompt calls it “21 test files.”  
   - Task objective says “21 test modules” (task line 79), but the checklist creates 20 test modules.  
   - Required fix: normalize wording to “20 test modules + conftest.py + __init__.py” or explicitly identify the 21st counted file.

## 4. Scope Creep / Out-of-Spec Items

Authorized corrections are **not** scope creep and are correctly encoded: underscored `superclaude.submit_pr`, corrected `--cov=superclaude.submit_pr`, exactly 4 markers, 33 events, and no `--depth quick --fix` (task lines 131-135, 552).

Potential minor out-of-spec additions:

1. **`anthropic` token ban in core-purity checks.**  
   - Spec NFR-6/AC-9 only names zero `gh`/`git` calls/tokens in the deterministic core (spec lines 504-506, 806, 989).  
   - Task adds `anthropic` to static/purity bans in multiple places (task lines 203, 248, 429). This is likely harmless repo hygiene, but it is not traceable to the spec requirement as written.

2. **Extensive M3/M4 QA machinery.**  
   - Task adds heavy QA process gates beyond the product spec. This appears to be task-builder/process policy rather than feature scope. I do not count it as product creep, but it is not a spec functional requirement.

## 5. Coverage Calculation

- Total audited requirement units: 154
- UNMAPPED: 2 (`NFR-7`, `NFR-8`)
- PARTIAL: 5 (`FR-1.4`, `AC-13`, `INV-015`, `T-VALIDATED-NOT-VERIFIED`, `§6.3 test-file count normalization`)
- Covered score: 147 covered + (5 × 0.5) = 149.5
- Coverage percentage: 149.5 / 154 = **97.08%**

## 6. Best-Practice Grade

**Grade: 4 / 5**

The tasklist is unusually comprehensive and self-contained, with strong SoT discipline, explicit DAG gates, test IDs, QA gates, and the five authorized spec corrections encoded. The grade is not 5 because two NFRs are unmapped and the INV-015/AC-13 canonical test is semantically wrong enough that an executor could build the wrong behavior while believing coverage is complete.

COVERAGE_PCT: 97.08
UNMAPPED: [NFR-7, NFR-8]
PARTIAL: [FR-1.4, AC-13, INV-015, T-VALIDATED-NOT-VERIFIED, §6.3-test-file-count-normalization]
