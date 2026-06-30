# QA Fix Applied — Phase Gate B M3 (serialized fix, I20 / PGB.5)

**Generated:** 2026-06-11
**Fix agent:** single serialized fixer (only agent permitted to modify these files)
**Source findings:** `qa/qa-consolidated-findings-gateB.md` (FAIL — 1 IMPORTANT domain-accuracy + 7 IMPORTANT + 2 MINOR crossref)
**Scope:** `src/superclaude/pr_submit/fsm.py` + named `tests/pr_submit/*.py` only.

---

## Result summary

- **pytest:** `135 passed` (was 131 → +4 new tests).
- **ruff check** (`src/superclaude/pr_submit/ tests/pr_submit/`): **All checks passed!** — yes.
- **ruff format --check**: **31 files already formatted** (clean) — yes (3 test files auto-reformatted for line-length collapse during `ruff format`, all cosmetic; re-run confirms clean).
- **fsm.py core purity:** `grep -nE '\bgh\b|\bgit\b' fsm.py` → no output (grep exit 1). fsm.py is still gh/git-free — yes.

---

## B-1 (IMPORTANT) — fsm.py parse_args: allow `--max-rounds 0` (EC-8)

**File:** `src/superclaude/pr_submit/fsm.py` (`parse_args`)

**Edit:** Changed the lower-bound guard so 0 is accepted (only negative rejected):

```python
# before
if ns.max_rounds < 1:
    raise ValueError("--max-rounds must be >= 1")
# after
if ns.max_rounds < 0:
    raise ValueError("--max-rounds must be >= 0")
```

The `> HARD_CAP_MAX_ROUNDS` (5) cap is unchanged. Only a numeric guard changed — no
shell/VC tokens introduced; fsm.py remains core-pure.

**Test added:** `tests/pr_submit/test_skill_parse.py::test_t_max_rounds_zero_allowed`
asserts `parse_args(["--max-rounds","0"]).max_rounds == 0` and that `-1` still raises
`ValueError`. EC-8 "monitor but never remediate" is now reachable via the CLI surface
(the core already honored it via `RunConfig(max_rounds=0)`; see
`test_ec8_max_rounds_zero_never_remediates`).

---

## B-2 (IMPORTANT) — T-105 missing (runtime `--repo` pin)

**File:** `tests/pr_submit/test_static_grep.py`

**Test added:** `test_t105_runtime_repo_pin` — the RUNTIME complement to T-104's static
grep. Reads the actual poll script
(`scripts/poll-augment-review.sh`) via the existing `_command_lines` helper and asserts:
every `gh pr` runtime line contains `--repo IronbellyOrg/IronClaude`; every `gh api`
runtime line targets `repos/IronbellyOrg/IronClaude/...` or `graphql` (gh api takes no
`--repo`). Also asserts at least one `gh pr` and one `gh api` call exist. T-105 +
FR-1.3/AC-7 mapped in the docstring.

Verified the script's actual commands: line 37 `gh pr view ... --repo IronbellyOrg/IronClaude`,
line 47 `gh api "repos/IronbellyOrg/IronClaude/pulls/..."` — both pinned.

---

## B-3 (IMPORTANT) — T-N31 missing (known non-Augment bot stays polling)

**File:** `tests/pr_submit/test_detection_contract.py`

**Test added:** `test_tn31_known_non_augment_bot_polling` — asserts `classify` on a
`github-actions[bot]` review (with `has_findings: True`) returns `"polling"` under a
`DetectionContract(augment_bot_login="augment-code[bot]", locked=True)`. This is the
NFR-4 fail-safe (review not detected → keep polling). T-N31 + NFR-4 mapped in the
docstring. Placed in test_detection_contract.py per the instruction.

---

## B-4 (IMPORTANT) — 5 orphan fixtures wired into test_edge_cases.py

**File:** `tests/pr_submit/test_edge_cases.py`

Added module helpers `_FINDING_KEYS` + `_finding_from_fixture(fd)` (filters a fixture
dict to the known Finding constructor keys). Existing inline assertions KEPT; fixture
references ADDED:

- `test_ec1_empty_findings_clean` — `load_fixture("finding-empty.json")`,
  asserts `fixture["findings"] == []`.
- `test_ec9_malformed_missing_fileline_structural_drop` —
  `load_fixture("finding-malformed.json")`, builds a Finding from `findings[0]` and
  asserts `is_groundable(it) is False`.
- `test_ec3_max_findings_stress_truncates` — `load_fixture("finding-max.json")`,
  asserts `len(findings)==50`, builds Findings (verified) and runs `plan_dispatch`
  asserting `truncated is True` and `len(batches) <= 2`.
- `test_ec7_needs_human_at_every_level` — `load_fixture("finding-needs-human.json")`,
  asserts `findings[0]["needs_human_decision"] is True` (parametrized inline run kept).
- **NEW** `test_round_sequence_2_fixture` — `load_fixture("round-sequence-2.json")`,
  builds findings from `cycles[0]` + `cycles[1]`, drives `run_skill` (max_rounds from
  fixture), asserts `round_counter==2`, `push_count==2`, `TERMINAL_CLEAN` matching the
  fixture's `expected` block.

All updated/new tests accept the `load_fixture` fixture param.

---

## B-5 (MINOR) — 3 comment-only fixtures get parity assertions

- `tests/pr_submit/test_loop_guard.py::test_t626_off_by_one_canonical` (added
  `load_fixture` param) — loads `round-sequence-residual-x3.json` and asserts its
  `expected` `{round_counter:2, push_count:2}` matches the computed result.
- `tests/pr_submit/test_crash_recovery.py::test_crash_window_no_double_push` (added
  `load_fixture` param) — loads `crash-after-push-before-completed.json`, computes the
  dangling `push_initiated` (key with no matching `push_completed`) and asserts exactly
  one, plus `expected.push_count==2` and `expected.recovered is True`.
- `tests/pr_submit/test_validated_not_verified.py::test_validated_not_verified_flags_behavioral_drift`
  (added `load_fixture` param) — loads `behavioral-drift.json`, asserts
  `behavioral_test_failures` non-empty, and that it drives the same
  `audit_validated_not_verified` verdict (`validated_not_verified is True`).

---

## Re-run evidence

```
$ uv run pytest tests/pr_submit/ -q | tail -3
============================= 135 passed in 0.21s ==============================

$ uv run ruff check src/superclaude/pr_submit/ tests/pr_submit/ | tail -1
All checks passed!

$ uv run ruff format --check src/superclaude/pr_submit/ tests/pr_submit/ | tail -1
31 files already formatted

$ grep -nE '\bgh\b|\bgit\b' src/superclaude/pr_submit/fsm.py ; echo exit:$?
exit:1        # no output → fsm.py is gh/git-free
```

## Verdict: all findings B-1..B-5 fixed; suite green; lint+format clean; fsm.py core-pure.
