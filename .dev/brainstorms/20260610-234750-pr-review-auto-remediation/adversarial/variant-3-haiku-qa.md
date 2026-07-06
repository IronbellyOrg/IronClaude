---
contract_version: "1.0"
artifact: adversarial-spec-variant
topic: "PR Review Auto-Remediation Monitor (V1.0)"
domain: qa
strategy: systematic
depth: standard
synthesis_mode: adversarial-qa
adversarial_status: qa-variant-pass
created: 2026-06-11T00:00:00Z
source_requirements: ./merged-requirements.md
---

# QA Variant Specification: PR Review Auto-Remediation Monitor (V1.0)

> **Perspective:** Quality Engineer — edge cases, boundary conditions, test coverage, failure
> scenarios, acceptance-criteria rigor, off-by-one and loop-termination correctness.
> This spec takes strong, opinionated positions on testability, detection-contract exhaustiveness,
> and loop-guard correctness. Every requirement is mapped to concrete test IDs (T-xxx).

---

## 1. Overview / Goals

### 1.1 What this is

A new skill `sc:submit-pr` with an in-session Monitor-driven loop that:
1. Opens a PR on `IronbellyOrg/IronClaude`.
2. Polls for the Augment Code GitHub App review.
3. Routes findings through severity re-grading to `/sc:troubleshoot`.
4. At autonomy levels 2-3, fixes, validates, pushes, replies, and resolves.
5. Terminates deterministically under a capped round counter.

### 1.2 Quality Goals

- **Deterministic termination** — no infinite remediation loops (loop-guard off-by-one = P0 defect).
- **Zero-regression** — `--monitor 0` behaves identically to today.
- **Autonomy-gate enforcement** — level boundaries are proven by behavioral tests, not assertions in prose.
- **Fail-safe by default** — unknown severity → Medium; unknown bot → "not detected".
- **Full test coverage** — every FR/NFR/AC has a concrete test; every edge case in §6 has a fixture.

### 1.3 Non-goals (V1.0)

- Headless / detached execution.
- GitHub Actions hosting.
- Non-Augment review handling.
- Merge-state mutation.

---

## 2. Functional Requirements (Elaborated with Testability Notes)

### FR-1 — PR submission skill with `--monitor` ordinal

| ID | Requirement | Testability note |
|---|---|---|
| FR-1.1 | Signature: `/sc:submit-pr [--monitor {0,1,2,3}] [--max-rounds N] [--base master] [--head <branch>] [--title …] [--body …]` | T-101: parse --help, verify flag set {0,1,2,3} with argparse `choices`; T-102: `--max-rounds` default=2, clamp max=5. |
| FR-1.2 | `--monitor` defaults to 0. | T-103: invoke skill with no `--monitor`; assert monitor not armed. |
| FR-1.3 | All `gh` calls pin `--repo IronbellyOrg/IronClaude`. | T-104: static grep over all Python/shell sources in `src/superclaude/skills/sc-submit-pr-protocol/` and `hooks/` for `gh ` without subsequent `--repo`. T-105: runtime mock captures every `gh` subprocess, asserts `--repo` present. |
| FR-1.4 | Pre-PR checks: confirm origin, rebase if behind, verify returned URL. | T-106: mock `git remote -v` returning wrong origin → skill HALTs with error. T-107: mock `git log master..origin/master` showing behind → auto-rebase before create. T-108: mock `gh pr create` returning URL with wrong owner → skill HALTs. |
| FR-1.5 | On `--monitor >= 1`, arm Monitor after PR creation. | T-109: `--monitor 1` → Monitor tool spawned exactly once; T-110: `--monitor 0` → Monitor tool never spawned. |

### FR-2 — In-session Augment review monitor

| ID | Requirement | Testability note |
|---|---|---|
| FR-2.1 | Poll PR for Augment Code GitHub App review via `gh pr view --json reviews,comments` + `gh api …/pulls/<N>/comments`. | T-201: mock `gh pr view` returning empty reviews → state = polling. T-202: mock returning Augment review with empty body → state = clean. T-203: mock returning Augment review with findings → state = findings. |
| FR-2.2 | Detection contract: three states (no review / clean / findings). Key on Augment App bot login (config constant, not hard-guessed). | T-210: config constant absent → skill HALTs with "probe first" error (R1). T-211: comment from different bot login → "review not detected" (NFR-4). T-212: two comments, one Augment one human → only Augment parsed. |
| FR-2.3 | Poll interval >= 30s; overall timeout default ~30 min, configurable. | T-220: mock poll fires at 29s interval → assertion fails (must be >= 30). T-221: mock never-arriving review → timeout fires at configurable deadline, state = "never arrived". T-222: `--timeout 60` → fires at 60s. |
| FR-2.4 | Monitor hosted by Monitor tool; session close = monitor lost (documented limitation). | T-230: integration test — close session mid-poll → monitor drops, run-log records `session_closed` event. No code assertion beyond logging (documented limitation). |

### FR-3 — Severity → troubleshoot-tier routing

| ID | Requirement | Testability note |
|---|---|---|
| FR-3.1 | Re-grade via severity rubric; Augment's self-reported severity is a hint, not authoritative. | T-301: fixture with Augment `severity_hint=low` but category=security → remap to Critical. T-302: fixture with `severity_hint=critical` but `confidence=low` → downgrade to High. |
| FR-3.2 | Route: Medium → `troubleshoot --fix`; High/Critical → `troubleshoot --depth deep --fix`; Low/Nit → report only. | T-310: Medium finding → mock troubleshoot called with `--fix` only. T-311: High finding → `--depth deep --fix`. T-312: Low finding → troubleshoot NOT called; finding recorded in report-only list. |
| FR-3.3 | Seed troubleshoot with finding body + file:line + evidence. | T-320: mock troubleshoot receives seeded context; assert `scope` param contains file:line from finding. |
| FR-3.4 | Batch findings by file/area; never exceed round budget. | T-330: 3 findings in same file → single troubleshoot batch. T-331: findings exceed round budget → truncate and HALT with summary. |

### FR-4 — Autonomy gates

| ID | Requirement | Testability note |
|---|---|---|
| FR-4.1 | Level 1: diagnose + propose only. **No edits.** | T-401: level 1 run → assert zero file writes (Monitor Write/Edit count = 0). T-402: emit exact offer prompt "fix these? y/n". |
| FR-4.2 | Level 2: implement fixes + validate locally. HALT before any commit/push/reply. Changes left in working tree. | T-410: level 2 → files modified on disk; T-411: `git push` never called; T-412: `git commit` never called; T-413: reply never posted. |
| FR-4.3 | Level 3: implement + validate + commit + push + reply + resolve, unattended, loop-guard governed. | T-420: level 3 → full end-to-end fixture (see AC-2). |
| FR-4.4 | `needs_human_decision` findings HALT even at level 3. | T-430: level 3 + fixture with `needs_human_decision` finding → skill HALTs, no push, no reply. |

### FR-5 — Local validation before push

| ID | Requirement | Testability note |
|---|---|---|
| FR-5.1 | Validation = relevant test command passes. Targeted tests for changed files; escalate to `make test` when cross-cutting. | T-501: single-file change → targeted `uv run pytest tests/path/` executed. T-502: cross-cutting (5+ files, multiple dirs) → `make test` executed. |
| FR-5.2 | `make lint` AND `uv run ruff format --check src/ tests/` must pass before push. | T-510: mock lint failure → push blocked, failure reported. T-511: mock format failure (lint green) → push blocked, failure reported (the known repo gotcha). |
| FR-5.3 | Validation fail → no push; report failure; level 3 retry or HALT. | T-520: test failure → no push, round counter NOT incremented (retry within same round). T-521: 3 consecutive validation failures → HALT. |

### FR-6 — Reply, resolve, and loop termination

| ID | Requirement | Testability note |
|---|---|---|
| FR-6.1 | Fix posts reply on specific Augment comment thread, summarizing fix + commit SHA, then resolves thread. | T-601: mock `gh api …/comments/<id>/replies` → assert reply posted to correct thread ID. T-602: resolve thread via appropriate API call. |
| FR-6.2 | Loop-stop: zero Medium+ findings OR `--max-rounds` reached. | T-610: re-review returns clean → loop terminates. T-611: re-review returns findings but round == max-rounds → loop terminates with summary. |
| FR-6.3 | Loop-guard: monitor-triggered re-review = next round, not new trigger. Round counter monotonic, capped. Default 2, max 5. | T-620 through T-629 (see §7 for full matrix). |
| FR-6.4 | Max-rounds with residual findings → post summary listing unresolved findings. | T-630: fixture with residual findings after max rounds → summary comment posted with exact list. |

### FR-7 — Hook integration

| ID | Requirement | Testability note |
|---|---|---|
| FR-7.1 | `offer-pr-review.sh` additionally mentions `sc:submit-pr --monitor`. Hook stays fail-open. | T-701: hook output contains both `/sc:auggie-review` and `/sc:submit-pr --monitor`. T-702: hook exits 0 on non-matching input. T-703: hook exits 0 on failed `gh pr create`. |

---

## 3. Non-Functional Requirements (Elaborated)

| ID | Requirement | Testability note |
|---|---|---|
| NFR-1 | Idempotent replies: never double-post same fix reply. Track replied comment IDs. | T-N01: replay same findings twice → assert reply posted exactly once per comment ID. T-N02: reply-tracking state persisted across polls within a round. |
| NFR-2 | Rate-limit safety: poll >= 30s; back off on 403/secondary-limit. | T-N10: mock 403 from `gh` → backoff to 60s next poll. T-N11: mock 403 x 3 → exponential backoff, still bounded by timeout. |
| NFR-3 | Observability: per-run log `.dev/.../monitor-run-<PR>.jsonl`. | T-N20: after level-3 fixture run, log file exists. T-N21: each event (poll, finding, route, fix, push, reply) has timestamp, round number, state. T-N22: log is valid JSONL (every line parses). |
| NFR-4 | Fail-safe defaults: unknown severity → Medium; unknown bot → "review not detected". | T-N30: finding with unrecognized severity string → routed as Medium. T-N31: comment from `github-actions[bot]` → ignored, state stays "polling". |
| NFR-5 | All paths absolute in user-facing prompts; paste-ready commands single-line. | T-N40: scan all `print`/`yield`/stdout in skill for relative paths → none. T-N41: no multi-line paste-ready commands in any user-facing string. |

---

## 4. Test Strategy & Coverage Matrix

### 4.1 Test Categories

| Category | Tool | Scope | Count |
|---|---|---|---|
| Unit | pytest | Individual functions (parse, route, guard, validate) | 38 |
| Integration | pytest + subprocess | Hook scripts, skill end-to-end with mocks | 14 |
| Behavioral | pytest | Autonomy gates, detection states, loop-guard | 18 |
| Edge-case | pytest | Boundary conditions, malformed input, race | 16 |
| Static analysis | grep + pytest | `--repo` pin, no relative paths, single-line commands | 4 |

**Total: 90 tests.**

### 4.2 Coverage Matrix: Requirement → Test

```
FR-1.1  → T-101, T-102
FR-1.2  → T-103
FR-1.3  → T-104, T-105
FR-1.4  → T-106, T-107, T-108
FR-1.5  → T-109, T-110
FR-2.1  → T-201, T-202, T-203
FR-2.2  → T-210, T-211, T-212
FR-2.3  → T-220, T-221, T-222
FR-2.4  → T-230
FR-3.1  → T-301, T-302
FR-3.2  → T-310, T-311, T-312
FR-3.3  → T-320
FR-3.4  → T-330, T-331
FR-4.1  → T-401, T-402
FR-4.2  → T-410, T-411, T-412, T-413
FR-4.3  → T-420
FR-4.4  → T-430
FR-5.1  → T-501, T-502
FR-5.2  → T-510, T-511
FR-5.3  → T-520, T-521
FR-6.1  → T-601, T-602
FR-6.2  → T-610, T-611
FR-6.3  → T-620 through T-629 (§7)
FR-6.4  → T-630
FR-7.1  → T-701, T-702, T-703
NFR-1   → T-N01, T-N02
NFR-2   → T-N10, T-N11
NFR-3   → T-N20, T-N21, T-N22
NFR-4   → T-N30, T-N31
NFR-5   → T-N40, T-N41
AC-1    → T-103, T-110
AC-2    → T-310, T-311, T-420, T-601, T-602, T-610
AC-3    → T-401, T-402
AC-4    → T-410, T-411, T-412, T-413
AC-5    → T-430
AC-6    → T-620 through T-629
AC-7    → T-104, T-105
```

### 4.3 Test File Layout

```
tests/submit_pr/
├── __init__.py
├── conftest.py                          # fixtures: mock_gh, mock_monitor, fixture_findings, tmp_skill_dir
├── test_skill_parse.py                  # T-101..T-103: flag parsing, defaults, choices
├── test_pre_pr_checks.py               # T-106..T-108: origin check, rebase, URL verification
├── test_monitor_arm.py                  # T-109, T-110, T-230: monitor arming logic
├── test_detection_contract.py           # T-201..T-203, T-210..T-212: poll states, bot detection
├── test_timeout.py                      # T-220..T-222: poll interval, timeout firing
├── test_severity_router.py              # T-301..T-302, T-310..T-312, T-N30: remap + routing
├── test_troubleshoot_seed.py            # T-320, T-330, T-331: seeding + batching
├── test_autonomy_gates.py               # T-401..T-402, T-410..T-413, T-420, T-430: level behavioral
├── test_validation_gate.py              # T-501..T-502, T-510..T-511, T-520..T-521: lint/format/test
├── test_loop_guard.py                   # T-620..T-629: fence-post matrix (§7)
├── test_reply_resolve.py                # T-601, T-602, T-610, T-611, T-630: reply + termination
├── test_idempotency.py                  # T-N01, T-N02: no double-post
├── test_rate_limit.py                   # T-N10, T-N11: 403 backoff
├── test_run_log.py                      # T-N20..T-N22: JSONL observability
├── test_edge_cases.py                   # T-E01..T-E16: edge-case catalog (§6)
├── test_hook_update.py                  # T-701..T-703: offer-pr-review.sh update
├── test_static_grep.py                  # T-104, T-N40, T-N41: static analysis checks
└── fixtures/
    ├── finding-medium.json              # single Medium finding
    ├── finding-high.json                # single High finding
    ├── finding-medium-high.json         # AC-2 fixture: 1 Medium + 1 High
    ├── finding-empty.json               # empty findings list
    ├── finding-max.json                 # 50 findings (stress test)
    ├── finding-duplicate.json           # same finding twice
    ├── finding-needs-human.json         # needs_human_decision finding
    ├── finding-malformed.json           # missing file:line, bad severity string
    ├── review-clean.json                # Augment review, zero findings
    ├── review-with-findings.json        # Augment review, 3 findings
    ├── review-non-augment.json          # review from different bot
    ├── review-interleaved.json          # Augment review + human comment interleaved
    └── round-sequence-2.json            # AC-6: round 1 findings → fix → round 2 clean
```

---

## 5. Edge-Case & Boundary Catalog

Each edge case has a concrete test. No edge case is "covered by other tests" — each has a
dedicated fixture and assertion.

### EC-1: Empty findings list (T-E01)
**Scenario:** Augment review arrives but contains zero findings (edge of the "clean" state).
**Expected:** State transitions to "clean", loop terminates, zero troubleshoot calls.
**Fixture:** `fixtures/review-clean.json`.
**Assertion:** `assert troubleshoot_mock.call_count == 0`, `assert state == "clean"`.

### EC-2: Single finding (T-E02)
**Scenario:** Exactly one Medium finding.
**Expected:** One troubleshoot call, one reply, one resolve.
**Fixture:** `fixtures/finding-medium.json`.
**Assertion:** `troubleshoot_mock.call_count == 1`, `reply_mock.call_count == 1`.

### EC-3: Max findings stress (T-E03)
**Scenario:** 50 findings in one review (exceeds batch capacity).
**Expected:** Batched into N troubleshoot calls without exceeding round budget; if batching
would overflow, truncate and HALT with summary (T-331).
**Fixture:** `fixtures/finding-max.json`.
**Assertion:** `troubleshoot_mock.call_count <= max_batch_size`, `HALT_triggered == True` if overflow.

### EC-4: Duplicate findings across rounds (T-E04)
**Scenario:** Same finding appears in round 1 and round 2 re-review (Augment re-reports unfixed item).
**Expected:** Deduplicated by `file:line` + finding body hash; not double-troubleshooted. Reply-ID
tracking (NFR-1) prevents double-reply.
**Fixture:** `fixtures/finding-duplicate.json` replayed across two poll cycles.
**Assertion:** `reply_mock.call_count == 1` for that comment_id.

### EC-5: Review arrives during a fix (T-E05)
**Scenario:** Poll detects review → troubleshoot starts → second poll fires while troubleshoot
running → new Augment re-review arrives.
**Expected:** In-flight troubleshoot completes; new review queued for next round (not processed
mid-fix). Monitor does NOT spawn a second troubleshoot for the same round.
**Assertion:** `round_counter == 1` after both polls; `troubleshoot_mock.call_count == 1` for round 1.

### EC-6: Timeout fires mid-remediation (T-E06)
**Scenario:** Timeout fires while troubleshoot is running (level 3).
**Expected:** Current troubleshoot allowed to finish (no orphaned work); loop terminates; summary
posted with partial-fix state. Run-log records `timeout_during_remediation`.
**Assertion:** `run_log` contains `timeout_during_remediation` event; no further polls after timeout.

### EC-7: `needs_human_decision` at every level (T-E07, T-430)
**Scenario:** Only finding is `needs_human_decision`.
- Level 1: propose + offer prompt (expected).
- Level 2: fix locally, then HALT (no commit/push).
- Level 3: HALT immediately — no fix, no push, no reply.
**Fixture:** `fixtures/finding-needs-human.json`.
**Assertion per level:** L1: `edits == 0`; L2: `pushes == 0, edits > 0`; L3: `edits == 0, pushes == 0, halted == True`.

### EC-8: `--max-rounds=0` (T-E08)
**Scenario:** User sets `--max-rounds 0`.
**Expected:** Skill treats as "monitor but never remediate" — equivalent to level 1 behavior
regardless of `--monitor` value. Poll fires, findings reported, zero rounds executed.
**Assertion:** `round_counter` never increments past 0; `troubleshoot_mock.call_count == 0`.

### EC-9: Malformed Augment payload (T-E09)
**Scenario:** Augment comment contains valid bot login but malformed JSON/missing `file:line`.
**Expected:** Finding fails grounding (T-N30 applies — unknown severity → Medium), but missing
`file:line` → finding dropped per hallucination contract, reported as "ungroundable" in run-log.
**Fixture:** `fixtures/finding-malformed.json`.
**Assertion:** `dropped_count >= 1`, no troubleshoot called for ungroundable finding.

### EC-10: Non-Augment comment interleaved (T-E10)
**Scenario:** PR has human review comment + Augment review. Human comment arrives first.
**Expected:** Human comment ignored entirely (NFR-4 — unknown bot → "review not detected").
Only Augment bot login triggers detection.
**Fixture:** `fixtures/review-interleaved.json`.
**Assertion:** `human_comment_parsed == False`, `augment_review_detected == True`.

### EC-11: Augment bot login not configured (T-E11 = T-210)
**Scenario:** Config constant for Augment bot login is absent (first run, R1 probe not done).
**Expected:** Skill HALTs with error message directing user to run empirical probe first.
**Assertion:** `skill_exited_with_error == True`, error message contains "probe".

### EC-12: Review arrives then disappears (T-E12)
**Scenario:** Augment review detected, then on next poll the review is no longer returned by
the GitHub API (edge case: review withdrawn or API inconsistency).
**Expected:** Treated as transient; poll continues until timeout. Run-log records
`review_disappeared` event.
**Assertion:** `state` transitions from `findings` back to `polling`; no troubleshoot called.

### EC-13: `--monitor 3` with `--max-rounds 5` (upper bound) (T-E13)
**Scenario:** Max autonomy + max rounds.
**Expected:** Loop runs at most 5 rounds; after round 5 with residual findings, summary posted.
**Assertion:** `round_counter <= 5`, `summary_posted == True` if residual.

### EC-14: Multiple PRs in same session (T-E14)
**Scenario:** User runs `/sc:submit-pr --monitor 3` twice in one session.
**Expected:** Second run creates separate monitor state, separate run-log, separate round counter.
No state leakage.
**Assertion:** Two distinct `.jsonl` log files; counters independent.

### EC-15: `gh` CLI not installed (T-E15)
**Scenario:** `gh` not on PATH.
**Expected:** Skill HALTs at Wave 0 with clear error. No partial execution.
**Assertion:** `skill_exited_with_error == True`, error mentions `gh` prerequisite.

### EC-16: `--base` branch does not exist (T-E16)
**Scenario:** `--base develop` but `develop` does not exist on `IronbellyOrg/IronClaude`.
**Expected:** Skill HALTs with error listing available branches.
**Assertion:** `skill_exited_with_error == True`, `git ls-remote` called to enumerate.

---

## 6. Loop-Guard Correctness Tests (§7 from requirements, expanded)

The loop-guard is the single most critical correctness invariant. An off-by-one here causes
infinite remediation loops. This section provides an exhaustive fence-post test matrix.

### 6.1 Round Counter Invariants

**INV-1:** `round_counter` starts at 0.
**INV-2:** `round_counter` increments exactly once per remediation cycle (fix → push → re-review).
**INV-3:** A re-review triggered by the monitor's own push counts as the *next* round, not a
new independent trigger.
**INV-4:** `round_counter` is monotonic (never decrements).
**INV-5:** `round_counter` never exceeds `--max-rounds`.
**INV-6:** Validation failure (T-520) does NOT increment `round_counter` (retry within same round).
**INV-7:** The "no review yet" poll state does NOT increment `round_counter`.

### 6.2 Fence-Post Test Matrix

| Test ID | Setup | `--max-rounds` | Rounds executed | Expected outcome |
|---|---|---|---|---|
| T-620 | Round 0: findings → fix → re-review clean | 2 | 1 | Terminates: clean |
| T-621 | Round 0: findings → fix → re-review findings → fix → re-review clean | 2 | 2 | Terminates: clean |
| T-622 | Round 0: findings → fix → re-review findings → fix → re-review findings | 2 | 2 | Terminates: max-rounds, summary posted |
| T-623 | Round 0: findings → fix → re-review findings → fix → re-review findings → fix → re-review clean | 5 | 3 | Terminates: clean |
| T-624 | Round 0: findings → fix → re-review findings × 5 times | 5 | 5 | Terminates: max-rounds, summary |
| T-625 | Round 0: clean immediately | 2 | 0 | Terminates: clean, zero rounds |
| T-626 | Round 0: findings → fix → re-review findings → fix → re-review findings → fix → re-review findings | 2 | 2 | **Critical:** assert `round_counter == 2` NOT 3, no round 3 fix pushed |
| T-627 | `--max-rounds 1`, findings → fix → re-review findings | 1 | 1 | Terminates: max-rounds, summary |
| T-628 | `--max-rounds 0` (see EC-8) | 0 | 0 | Terminates: no rounds, findings reported only |
| T-629 | Round 0: findings → fix → validation fails → retry → fix → re-review clean | 2 | 1 | Terminates: clean; validation retry did NOT consume a round |

### 6.3 Off-By-One Specific Assertions

For T-626 (the most critical test):

```python
def test_loop_guard_off_by_one_at_max_2(mock_skill_env):
    """The canonical off-by-one test.
    
    Simulates: initial findings → fix → re-review with residual findings →
    fix → re-review with residual findings. With --max-rounds=2, the third
    fix MUST NOT be pushed. round_counter must equal exactly 2.
    """
    fixture = load_fixture("round-sequence-residual-x3.json")
    result = run_skill("--monitor 3 --max-rounds 2", fixture)
    
    # Fence-post: exactly 2 remediation rounds executed
    assert result.round_counter == 2, f"Expected 2, got {result.round_counter}"
    
    # Exactly 2 pushes, not 3
    assert result.push_count == 2, f"Expected 2 pushes, got {result.push_count}"
    
    # Exactly 2 reply threads, not 3
    assert result.reply_count == 2
    
    # Summary comment posted (residual findings after max rounds)
    assert result.summary_posted == True
    
    # NO third fix was written to disk
    assert third_fix_not_applied(result)
```

### 6.4 "Monitor-triggered re-review counts as same round" Invariant (T-630)

This tests INV-3 explicitly: a re-review caused by the monitor's own push increments to the
*next* round, not a fresh trigger.

```python
def test_re_review_is_next_round_not_new_trigger(mock_skill_env):
    """Proves that the monitor does NOT treat its own push-triggered re-review
    as an independent trigger that would restart the round counter."""
    fixture = load_fixture("round-sequence-2.json")
    # Round 1: findings detected, fix pushed
    # Re-review arrives (triggered by the push)
    # This must be round 2, NOT round 1 again
    result = run_skill("--monitor 3 --max-rounds 2", fixture)
    assert result.round_sequence == [0, 1]  # starts at 0, increments to 1
    assert result.round_counter == 2  # 2 rounds total (0-indexed: 0 and 1 means 2 executed)
```

---

## 7. Autonomy-Gate Behavioral Tests

These tests prove the autonomy boundaries hold under adversarial conditions.

### 7.1 Level 1: Zero Edits Guarantee (T-401, T-402)

```python
def test_level1_zero_edits(mock_skill_env):
    """Level 1 must make ZERO file edits regardless of findings severity."""
    fixture = load_fixture("finding-medium-high.json")
    result = run_skill("--monitor 1", fixture)
    
    # No Write, Edit, or NotebookEdit tool calls
    assert result.tool_calls_by_name("Write") == 0
    assert result.tool_calls_by_name("Edit") == 0
    assert result.tool_calls_by_name("NotebookEdit") == 0
    
    # No Bash calls to git commit/push
    assert not any("git commit" in c for c in result.bash_commands)
    assert not any("git push" in c for c in result.bash_commands)
    
    # Offer prompt emitted verbatim
    assert "fix these? y/n" in result.stdout
```

### 7.2 Level 2: Zero Pushes Without Approval (T-410..T-413)

```python
def test_level2_fixes_but_no_push(mock_skill_env):
    """Level 2 implements fixes and validates, but HALTs before any push."""
    fixture = load_fixture("finding-medium-high.json")
    result = run_skill("--monitor 2", fixture)
    
    # Files modified on disk
    assert result.files_modified_count > 0
    
    # Validation ran
    assert result.validation_ran == True
    
    # But no push, no commit
    assert result.push_count == 0
    assert result.commit_count == 0
    
    # No reply posted
    assert result.reply_count == 0
    
    # User prompt emitted
    assert "ready to push" in result.stdout.lower() or "approve" in result.stdout.lower()
```

### 7.3 Level 3: HALT on needs_human_decision (T-430)

```python
def test_level3_halts_on_human_decision(mock_skill_env):
    """Even at maximum autonomy, needs_human_decision findings HALT."""
    fixture = load_fixture("finding-needs-human.json")
    result = run_skill("--monitor 3", fixture)
    
    # No edits
    assert result.tool_calls_by_name("Edit") == 0
    
    # No push
    assert result.push_count == 0
    
    # No reply
    assert result.reply_count == 0
    
    # HALT state recorded
    assert result.halted == True
    assert result.halt_reason == "needs_human_decision"
    
    # Human prompt emitted
    assert "human sign-off" in result.stdout.lower() or "sign-off" in result.stdout.lower()
```

### 7.4 Level 3: Full End-to-End (T-420 = AC-2)

```python
def test_level3_full_remediation_flow(mock_skill_env):
    """AC-2: Medium + High findings → 2 troubleshoot sessions → 2 fixes → 2 replies."""
    fixture = load_fixture("finding-medium-high.json")
    result = run_skill("--monitor 3 --max-rounds 2", fixture)
    
    # Two troubleshoot sessions
    assert result.troubleshoot_count == 2
    # One standard (Medium), one deep (High)
    assert "--depth deep" in result.troubleshoot_calls[0] or "--depth deep" in result.troubleshoot_calls[1]
    
    # Two validated fixes
    assert result.validation_ran == True
    
    # Two thread replies
    assert result.reply_count == 2
    
    # Two resolved threads
    assert result.resolve_count == 2
    
    # At most --max-rounds rounds
    assert result.round_counter <= 2
    
    # Deterministic termination
    assert result.terminated == True
```

---

## 8. Detection-Contract State Tests

### 8.1 State: No Review Yet (T-201)

```python
def test_detection_no_review(mock_gh):
    """gh pr view returns no Augment review → keep polling."""
    mock_gh.pr_view_returns({"reviews": [], "comments": []})
    state = poll_augment_review(pr_num=42)
    assert state == "polling"
    assert state.findings == []
```

### 8.2 State: Clean Review (T-202, T-E01)

```python
def test_detection_clean_review(mock_gh):
    """Augment review present but zero Medium+ findings → terminate clean."""
    mock_gh.pr_view_returns(review_from_augment_bot(findings=[]))
    state = poll_augment_review(pr_num=42)
    assert state == "clean"
    assert state.findings == []
    assert state.terminated == True
```

### 8.3 State: Findings Review (T-203)

```python
def test_detection_findings_review(mock_gh):
    """Augment review with findings → route."""
    mock_gh.pr_view_returns(review_from_augment_bot(
        findings=[{"severity": "Medium", "file": "src/foo.py", "line": 42}]
    ))
    state = poll_augment_review(pr_num=42)
    assert state == "findings"
    assert len(state.findings) == 1
    assert state.findings[0].remapped_severity == "Medium"
```

### 8.4 Fail-Safe: Non-Augment Bot (T-211, T-N31)

```python
def test_detection_non_augment_bot(mock_gh):
    """Comment from github-actions[bot] → ignored, state stays polling."""
    mock_gh.pr_view_returns(review_from_bot("github-actions[bot]", findings=[]))
    state = poll_augment_review(pr_num=42)
    assert state == "polling"
```

### 8.5 Fail-Safe: Unknown Severity (T-N30)

```python
def test_severity_unknown_defaults_to_medium():
    """Finding with unrecognized severity string → treated as Medium."""
    finding = {"severity": "super_urgent", "file": "src/foo.py", "line": 1}
    result = remap_severity(finding)
    assert result.remapped_severity == "Medium"
```

---

## 9. Acceptance Criteria (Testable, Expanded)

| ID | Criterion | Verification Method |
|---|---|---|
| AC-1 | `--monitor 0` → PR opens, zero monitor activity | T-103 + T-110: assert Monitor tool never spawned, no polls logged |
| AC-2 | Fixture PR with 1 Medium + 1 High → 2 troubleshoot sessions, 2 fixes, 2 replies, 2 resolves, <=max-rounds, deterministic termination | T-420: full end-to-end with mocked gh API |
| AC-3 | Level-1 run makes zero file edits, emits offer prompt verbatim | T-401 + T-402: assert Write/Edit/NotebookEdit count = 0, stdout contains exact offer string |
| AC-4 | Level-2 run leaves changes in working tree, zero pushes | T-410..T-413: assert files_modified > 0, push_count = 0, commit_count = 0 |
| AC-5 | `needs_human_decision` finding HALTs at level 3 | T-430: assert halted = True, edits = 0, pushes = 0 |
| AC-6 | Loop never exceeds `--max-rounds`; re-review increments same counter; verified with 2-round fixture | T-620..T-629: fence-post matrix, especially T-626 (off-by-one) |
| AC-7 | Every `gh` call carries `--repo IronbellyOrg/IronClaude` | T-104 (static grep) + T-105 (runtime mock capture) |

---

## 10. Validation-Gate Tests (FR-5)

### 10.1 Lint + Format Both Required (T-510, T-511)

```python
def test_validation_blocks_push_on_format_failure(mock_skill_env):
    """make lint passes but ruff format --check fails → push blocked."""
    mock_skill_env.lint_passes = True
    mock_skill_env.format_passes = False  # the known repo gotcha
    result = run_validation_gate()
    assert result.push_allowed == False
    assert "format" in result.failure_reason.lower()
```

### 10.2 No-Push-On-Fail (T-510)

```python
def test_validation_blocks_push_on_lint_failure(mock_skill_env):
    """make lint fails → push blocked regardless of format."""
    mock_skill_env.lint_passes = False
    mock_skill_env.format_passes = True
    result = run_validation_gate()
    assert result.push_allowed == False
```

### 10.3 Validation Failure Does Not Consume Round (T-520)

```python
def test_validation_failure_retries_within_same_round(mock_skill_env):
    """Test failure → retry fix → validation passes → push. Round counter unchanged."""
    fixture = load_fixture("finding-medium.json")
    fixture.validation_passes_on_attempt = 2  # fails first, passes second
    result = run_skill("--monitor 3", fixture)
    assert result.round_counter == 1  # one round, despite 2 validation attempts
    assert result.validation_attempts == 2
```

---

## 11. Regression Safety Tests (AC-1)

```python
def test_monitor_zero_regression(mock_skill_env):
    """--monitor 0 must produce zero monitor activity — regression-safe vs today."""
    result = run_skill("--monitor 0", pr_fixture="basic-pr.json")
    
    # PR was created
    assert result.pr_created == True
    assert result.pr_url.contains("IronbellyOrg/IronClaude/pull/")
    
    # Monitor was never armed
    assert result.monitor_armed == False
    assert result.poll_count == 0
    assert result.findings_processed == 0
    
    # Behaviorally identical to pre-feature state
    assert result.tool_calls_by_name("Monitor") == 0
```

---

## 12. Risks & Mitigations

| Risk | Severity | QA Mitigation | Test Coverage |
|---|---|---|---|
| **R1: Augment bot login unknown** | P0 | Skill HALTs at Wave 0 if config constant absent; empirical probe required before parser | T-210, T-E11 |
| **R2: Loop-guard off-by-one** | P0 | Exhaustive fence-post matrix (T-620..T-629); T-626 as canonical off-by-one; INV-1..INV-7 formal invariants | T-620..T-629 |
| **R3: Session-close mid-remediation** | P1 | Run-log checkpoint state (NFR-3); documented limitation; T-E06 verifies graceful termination | T-E06, T-N20..T-N22 |
| **R4: Auto-push blast radius** | P1 | Validation gate (FR-5.2), human-decision HALT (FR-4.4), conservative --max-rounds=2 default, audit log | T-510, T-511, T-430, T-N20 |
| **R5: Duplicate findings cause double-reply** | P2 | Reply-ID tracking (NFR-1), tested with replay fixture | T-N01, T-N02, T-E04 |
| **R6: Review arrives during fix** | P2 | Monitor queues re-review for next round; does not spawn concurrent troubleshoot | T-E05 |
| **R7: Timeout mid-remediation** | P2 | Current fix completes; summary posted with partial state | T-E06 |
| **R8: `make lint` green but format fails** | P2 | Validation gate requires BOTH; explicit test for this gotcha | T-511 |
| **R9: Non-Augment comment triggers false detection** | P2 | Bot-login guard (NFR-4); tested with interleaved fixture | T-E10, T-N31 |
| **R10: Malformed Augment payload** | P3 | Grounding failure → finding dropped, not downgraded | T-E09 |

---

## 13. Test Execution Strategy

### 13.1 CI Integration

Tests run as part of the standard `make test` pipeline:

```bash
uv run pytest tests/submit_pr/ -v --cov=superclaude.skills.sc-submit-pr-protocol
```

### 13.2 Test Markers

| Marker | Tests | Purpose |
|---|---|---|
| `@pytest.mark.unit` | T-101..T-331, T-N01..T-N41 | Fast, no I/O |
| `@pytest.mark.integration` | T-401..T-630, T-E01..T-E16 | Mocked gh API, subprocess hooks |
| `@pytest.mark.loop_guard` | T-620..T-629 | Fence-post matrix (run on every PR) |
| `@pytest.mark.autonomy` | T-401..T-430 | Autonomy gate enforcement (run on every PR) |
| `@pytest.mark.p0` | T-626, T-430, T-210, T-511 | Critical-path tests (fail-fast in CI) |

### 13.3 Mock Strategy

All external dependencies are mocked at the boundary:
- `gh` CLI: captured via subprocess mock; returns pre-built JSON fixtures.
- Monitor tool: simulated via callback that fires poll events on a controlled timeline.
- `/sc:troubleshoot`: captured via function mock; asserts on flags and seeded context.
- File system: `tmp_path` for all writes; no real repo mutation.

### 13.4 Fixture Authenticity

Fixtures in `tests/submit_pr/fixtures/` are derived from the R1 empirical probe (once completed).
Until the probe runs, fixtures are synthetic but follow the expected GitHub API response schema.
After probe, fixtures are regenerated from real data and a schema-validation test asserts parity.

---

## 14. QA-Specific Design Decisions

These are the opinionated positions that distinguish this QA spec from architect/backend variants:

### QD-1: Validation failure does NOT increment round counter
When `make test` or `make lint` fails during a remediation round, the retry is within the *same*
round. The round counter only increments after a successful push triggers a re-review. This is
encoded as INV-6 and tested in T-520. An alternative design (count validation attempt as a round)
would waste round budget on self-inflicted failures.

### QD-2: `--max-rounds=0` is a valid, meaningful setting
It means "monitor and report but never remediate" — a diagnostic mode. Equivalent to level 1
regardless of `--monitor` value. Tested in T-E08 and T-628.

### QD-3: Review disappearance is a transient, not terminal, state
If Augment's review is detected and then vanishes on the next poll (API inconsistency or review
withdrawn), the monitor treats this as transient and continues polling until timeout. Tested in
T-E12. Alternative (treat as "review withdrawn, terminate") would silently skip unfixed findings.

### QD-4: The off-by-one test (T-626) is the single most important test
If this test passes, the loop-guard is correct. If it fails, the feature is dangerous. It runs
in CI on every PR (`@pytest.mark.p0`), and its assertion messages are designed to be diagnostic:
`Expected 2 pushes, got 3` tells you exactly how the guard failed.

### QD-5: Reply-ID tracking is keyed on `comment_id`, not finding body hash
Two different findings on the same Augment comment thread share a `comment_id`. The reply is
posted once per thread, not once per finding. This prevents thread spam when multiple findings
map to one comment. Tested in T-N01 and T-E04.

### QD-6: Severity rubric is tested independently from the skill
The severity remap algorithm (from the reused `sc-auggie-review-protocol` rubric) is tested in
isolation (`test_severity_router.py`) with all 14 category-to-severity mappings from the rubric
table, plus all three confidence adjustments and both diff-locality adjustments. This is a pure
unit test with no skill orchestration dependency — if the rubric is wrong, the skill will route
wrong regardless of how well the skill logic is tested.
