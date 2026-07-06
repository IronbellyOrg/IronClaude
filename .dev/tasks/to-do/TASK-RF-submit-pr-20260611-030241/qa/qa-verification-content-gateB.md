# QA Verification — CONTENT (Phase Gate B M3, post-fix)

**Generated:** 2026-06-11
**Phase:** content-verification (Gate B fix verification)
**Mode:** `fix_authorization: false` (verify only)
**document_type:** "sc:pr-submit build (post-fix)"
**Scope:** Confirm B-1..B-5 fixes restore spec INTENT (not cosmetic), no regression.

---

## Overall Verdict: PASS

Spec intent is **genuinely restored** for all five findings. Every fix was verified
against actual source (fsm.py, the poll script, the test files, and the fixture JSON),
not just against the fix report's prose. Suite is green: **135 passed**.

---

## (a) B-1 — EC-8 genuinely reachable (parser AND core agree)

**VERIFIED — genuine.** Both surfaces honor the EC-8 "monitor but never remediate" contract.

- **Parser** (`fsm.py:101-104`): guard is now `if ns.max_rounds > HARD_CAP_MAX_ROUNDS: raise`
  THEN `if ns.max_rounds < 0: raise`. So `0` is accepted; only negatives rejected.
  - `test_skill_parse.py::test_t_max_rounds_zero_allowed` (lines 50-53): asserts
    `parse_args(["--max-rounds","0"]).max_rounds == 0` AND `-1` raises `ValueError`.
    Non-trivial — would fail under the old `< 1` guard.
- **Core** (`run_skill`): `should_halt_rounds(0,0)` → loop-guard `0 >= 0` True → HALT before any cycle.
  - `test_edge_cases.py::test_ec8_max_rounds_zero_never_remediates` (lines 160-165):
    `run_skill(RunConfig(monitor_ordinal=3, max_rounds=0, findings=[_vf()]))` →
    `state == HALT_MAX_ROUNDS`, `round_counter == 0`, `push_count == 0`. This is the exact
    EC-8 contract (spec lines 550-554): "Poll fires, findings reported, zero rounds;
    round_counter never increments past 0." Verified at L3 (ordinal=3) where the ceiling
    would otherwise push — proving the round-budget gate, not the ceiling, blocks.

Parser AND core agree: the CLI surface now admits the value the core already honored.

## (b) B-2 (T-105) and B-3 (T-N31) — genuine spec assertions, not trivially-true

**VERIFIED — genuine.**

- **T-105 (B-2)** `test_static_grep.py::test_t105_runtime_repo_pin` (lines 148-186): the
  RUNTIME complement to T-104. It reads the ACTUAL poll script
  (`src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh` — note:
  the fix report abbreviated the path to `scripts/poll-augment-review.sh`; the test uses
  the full canonical path, which exists), extracts real `gh pr` / `gh api` command lines via
  the `_command_lines` helper, and asserts (i) ≥1 `gh pr` AND ≥1 `gh api` exist, (ii) every
  `gh pr` line contains `--repo IronbellyOrg/IronClaude`, (iii) every `gh api` line targets
  `repos/IronbellyOrg/IronClaude/...` or `graphql`. Cross-checked the script: line 37
  `gh pr view "$PR" --repo IronbellyOrg/IronClaude`, line 47
  `gh api "repos/IronbellyOrg/IronClaude/pulls/${PR}/comments"`. Both pinned. This is FR-1.3/
  AC-7's runtime arm (spec line 167) — the assertion fails if the script ever drops the pin.
  NOT trivially-true (would catch a real misroute).

- **T-N31 (B-3)** `test_detection_contract.py::test_tn31_known_non_augment_bot_polling`
  (lines 111-125): builds a `locked=True` contract and a payload with a
  `github-actions[bot]` review carrying `has_findings: True`, then asserts
  `classify(...) == "polling"`. This is the NFR-4 fail-safe (spec line 804: "`github-actions
  [bot]` → ignored, stays 'polling'"). The `has_findings: True` is the load-bearing detail —
  the test would FAIL if the classifier matched any-bot-with-findings instead of only the
  Augment login. NOT trivially-true. (T-211 covers a similar shape; T-N31 pins the named ID
  to the explicit canonical bot — a valid, if thin, distinction that resolves the
  previously-unresolvable §6.2 ID.)

## (c) B-4 / B-5 — fixtures genuinely referenced; parity assertions live

**VERIFIED — genuine.** All 8 previously-orphan fixtures are now `load_fixture`-ed exactly
once each (grep-confirmed), and each assertion compares fixture DATA to actual BEHAVIOR
(not a dead `assert True`):

- B-4 (`test_edge_cases.py`):
  - EC-1 → `finding-empty.json`: asserts `fixture["findings"] == []` (verified file: empty).
  - EC-9 → `finding-malformed.json`: builds a `Finding` from the fixture, asserts
    `is_groundable(it) is False` (real behavior).
  - EC-3 → `finding-max.json`: asserts `len == 50` (verified: 50), then runs `plan_dispatch`
    on the fixture findings asserting `truncated is True` and `len(batches) <= 2`.
  - EC-7 → `finding-needs-human.json`: asserts `findings[0]["needs_human_decision"] is True`
    (verified: True).
  - `test_round_sequence_2_fixture` → `round-sequence-2.json`: drives `run_skill` with the
    fixture's cycles + `max_rounds`, asserts `round_counter==2`, `push_count==2`,
    `TERMINAL_CLEAN` — matching the fixture `expected` block (verified: `{round_counter:2,
    push_count:2, terminal:TERMINAL_CLEAN}`).
- B-5 (parity assertions compare fixture `expected` to computed result):
  - `test_loop_guard.py::test_t626_off_by_one_canonical` → `round-sequence-residual-x3.json`:
    asserts `fixture["expected"]["round_counter"] == result.round_counter == 2` and push_count
    (verified fixture `expected`: `{round_counter:2, push_count:2, terminal:HALT_MAX_ROUNDS}`).
  - `test_crash_recovery.py::test_crash_window_no_double_push` →
    `crash-after-push-before-completed.json`: derives the dangling `push_initiated` (key with
    no matching `push_completed`), asserts exactly 1, plus `expected.push_count==2` and
    `expected.recovered is True` (verified fixture: 2 events, `expected.recovered:True`).
  - `test_validated_not_verified.py::test_validated_not_verified_flags_behavioral_drift` →
    `behavioral-drift.json`: feeds the fixture's `validation_status` + `behavioral_test_failures`
    through `audit_validated_not_verified(...)`, asserts `validated_not_verified is True`
    (verified fixture: `validation_status==validated`, btf non-empty).

No fixture remains orphaned among the 8; each assertion is data→behavior, not a dead stub.

## (d) No spec intent REGRESSED by allowing `--max-rounds 0`

**VERIFIED — no regression.**

- Hard cap 5 still holds: `fsm.py:101` `if ns.max_rounds > HARD_CAP_MAX_ROUNDS: raise`
  (unchanged). `test_t102_max_rounds_default_and_cap` (lines 34-39): `5` accepted, `6` raises.
- Negative still rejected: `fsm.py:103-104` `if ns.max_rounds < 0: raise`. `-1` raises
  (`test_t_max_rounds_zero_allowed` line 52-53).
- `fsm.py` core purity preserved: only a numeric guard changed; no `gh`/`git` token introduced
  (`test_tn50_core_pure_no_gh_git_tokens` still green; fsm.py in the core-pure set).
- Full suite green (135 passed) — no other behavior shifted.

---

## Self-Audit

**(a) Reliance list — structural items NOT re-checked (covered by prior Gate B lens passes):**
- Relied on prior PASS for template-conformance, internal-consistency, core-purity/evidence,
  actionability/spec-correction lenses (qa-consolidated-findings-gateB.md lines 6-11).

**(b) Independent semantic checks (≥1 required, INV-019):**
- B-1 parser/core agreement — verified by reading `fsm.py:101-104` + running the suite
  (`test_ec8...` lines 160-165, `test_t_max_rounds_zero_allowed` lines 50-53).
- T-105 runtime pin — verified by Reading the ACTUAL poll script
  (`poll-augment-review.sh:37,47`) and confirming the test extracts + asserts those exact
  command shapes (`test_static_grep.py:148-186`), not just the report's claim.
- Fixture-reference genuineness — verified by Reading each fixture JSON
  (`finding-empty/max/needs-human/round-sequence-2/-residual-x3/behavioral-drift/crash-*`)
  and grep-confirming each is `load_fixture`-ed exactly once with a live data→behavior assertion.

**Tool engagement:** Read: 9 | Grep/Bash-grep: 7 | Bash (pytest + python json): 4
**Confidence:** Verified: 5/5 findings (B-1..B-5) + regression check | Unverifiable: 0 |
Unchecked: 0 | Confidence: 100%

---

## VERDICT: PASS
