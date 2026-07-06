# Reviewer Card 2 — Best-Practice Compliance + Risk Surface Audit

**Reviewer:** Independent pre-execution reflection (sc:reflect UC-1, Tier 2)
**Lens:** BEST-PRACTICE COMPLIANCE + RISK SURFACE
**Tasklist:** `TASK-RF-pr-submit-v11-20260612-013419.md`
**Spec:** `merged-spec-v1.1-addendum.md`
**Date:** 2026-06-12

---

## 1. Dependency Ordering / DAG Correctness

**Grade: 4/5**

The phase ordering is correctly layered:

- **Phase 2** (models.py) → **Phase 3** (classifier/detection) → **Phase 4** (run_log) → **Phase 5** (fsm) → **Phase 6** (skill/refs/script) → **Phase 7** (validation) → **Phase 8** (reflect/Done).

This respects the import-DAG: `models.py` defines `MonitorState.S5A_RETRIGGER_REVIEW` / `S5B_AUGGIE_FALLBACK` and the 4 new `EventType` members that Phase 3's `STATE_DECLINED`, Phase 4's `rebuild_state` folds, and Phase 5's `transition()` edges all reference. The tasklist explicitly marks models.py as a "HARD prerequisite" (line 88).

**Spot-check on the 6th-idempotency-set vs strict-once-gate ordering:** Step 4.1 adds `"auggie_review_invoked"` to `IDEMPOTENCY_SETS` (Phase 4), and Step 5.5 uses `record_idempotent("auggie_review_invoked", ...)` (Phase 5). I verified `run_log.py:207` that `record_idempotent` raises `ValueError(f"unknown idempotency set: {set_name!r}")` on an unknown set name — so Phase 4 MUST precede Phase 5, and it does. Correct.

**Minor concern (deducted 1 point):** Step 3.4 edits `refs/detection-contract.md` (under `src/superclaude/skills/`) but defers `make sync-dev` + `make verify-sync` to Phase 6. This is intentional (note at line 259: "do NOT run it here"), but it means the `detection.py` tests run in Phase 3.7 will be validating against a `from_yaml` default on a ref whose `locked: false` YAML has not been sync'd to `.claude/`. In a single-worktree sequential execution this is benign (the tests load from `src/` directly), but if the executors happen to test against `.claude/skills/` (e.g., via an installed-skill path), the new keys won't be present yet. The tasklist should explicitly note the test fixture loads from `src/` (or use the detection-contract YAML file path directly), not from `.claude/skills/`.

---

## 2. NFR-6 Core Purity

**Grade: 4/5**

The tasklist maintains a strong boundary: `gh`/`git` tokens are confined to SKILL.md I/O, the `scripts/retrigger-review.sh`, and the new `refs/review-retrigger.md`. The deterministic core gets `_noop`-defaulted `RunConfig` seams for `do_retrigger` and `invoke_auggie_review`.

The T-N50 static-grep test is correctly extended (Step 6.8):

- `refs/auggie-fallback.md` (gh-free) → added to `CORE_PURE_FILES`.
- `refs/review-retrigger.md` (gh-bearing, has `gh api … repos/IronbellyOrg/IronClaude/...`) → covered by the T-104 fork-pin path, NOT `CORE_PURE_FILES`.
- `retrigger-review.sh` (gh-bearing) → likewise covered by T-104 via the existing `SKILL_DIR.rglob("*")` glob.

I spot-checked `test_static_grep.py` (lines 27-34) — `CORE_PURE_FILES` currently lists 6 entries (3 skill refs + 3 core .py files). Step 6.8 correctly instructs adding only `auggie-fallback.md` (after a pre-grep for gh) and explicitly forbids adding `review-retrigger.md` or `retrigger-review.sh`.

**Minor concern (deducted 1 point):** The tasklist says T-N50's `CORE_PURE_FILES` extension goes in Step 6.8, which is Phase 6 (skill surface). But the tasklist's Phase 3.7 already runs `pytest tests/pr_submit/test_detection_contract.py` and Phase 4.6 runs its own tests — if the tasklist's test items add new `.py` files to `CORE_PURE_FILES` as part of those phases (e.g., `classifier.py`/`detection.py` are already in there), there is no explicit instruction to keep `CORE_PURE_FILES` stable until Phase 6.8. This is not a defect — `classifier.py` and `detection.py` are already in `CORE_PURE_FILES` (no, wait, they are NOT — they are under `pr_submit/` not in `CORE_PURE_FILES` which lives in the test file). The real risk is subtler: if Phase 3 or 4 accidentally adds a `gh`/`git` token to a file already in `CORE_PURE_FILES` (fsm.py, loop_guard.py, etc.), T-N50 will catch it, but the tasklist has no explicit NFR-6 re-grep instruction at Phase 3/4 level — only at Phase 5 (Step 5.6) and Phase 6. This is a gap, but a narrow one since the Phase 3/4 edits are pure-classification and run-log folds (no shell I/O by spec).

---

## 3. Closed-Enum Integrity

**Grade: 3/5** — **THIS IS THE HIGHEST-RISK DIMENSION**

I spot-checked the current source against the tasklist's claims:

**EventType:** Currently has **33 members** (verified via live Python enumeration). The class docstring at `models.py:20` says "EXACTLY 33 members" and the module docstring at `models.py:3` says "exactly 33 members". The tasklist (Step 2.2) correctly identifies BOTH count-bearing docstrings and instructs bumping them to 37.

**However, the tasklist misses TWO additional count-bump sites that Step 4.3 only partially covers:**

1. **`models.py` class docstring** (line 20): `"EXACTLY 33 members"` — covered by Step 2.2. OK.
2. **`models.py` module docstring** (line 3): `"exactly 33 members"` — covered by Step 2.2. OK.
3. **`run_log.py:103`**: `"not one of the 33 closed enum values"` (append docstring) — covered by Step 4.3. OK.
4. **`run_log.py:109`**: `"not one of the 33 §11.3 events"` (ValueError message) — covered by Step 4.3. OK.

**But I found a latent risk the tasklist does not explicitly address:**

- **`run_log.py:148`**: The `rebuild_state` docstring says `"the 5 idempotency sets"`. Step 4.1 correctly identifies this (line 316 mentions the rebuild_state docstring at ":148" "the 5 idempotency sets"→"the 6 idempotency sets"). This is covered.

**The gap is in the `len(EventType) == 37` test:** Step 4.5 (line 332) says to add `assert len(EventType) == 37` to `test_run_log.py`, noting "no numeric count test exists today — this establishes it." I verified this is correct: there is currently no `len(EventType)` assertion in the existing test suite. This is good — the tasklist correctly identifies the gap and plugs it.

**The IDEMPOTENCY_SETS count is also correct:** Currently 5 sets at `run_log.py:27-33`. Step 4.1 adds the 6th and updates the `# The 5 idempotency sets` comment (line 26). Step 4.1 also explicitly re-greps for stale "5" prose. This is thorough.

**Deduction rationale (3/5):** While the count sites are all identified, the tasklist puts the EventType count bump in Phase 2 Step 2.2 and the run_log count bump in Phase 4 Step 4.3. Between those phases, the codebase is in a transient state where `models.py` says "37" but `run_log.py` still says "33". The `len(EventType) == 37` test (Phase 4.5) will fail if run between Phase 2 and Phase 4.3. This is not a DAG error per se (the tasklist never asks you to run the full suite mid-build), but it creates a window where the Phase 2.4 validation (`pytest tests/pr_submit/test_run_log.py`) could break if a later edit had already added the `len(EventType)` test. The tasklist avoids this by deferring the count test to Phase 4.5, but the instruction to bump `models.py` docstrings to 37 in Phase 2.2 is a documentation-only change that is easy to over-eagerly verify. A cleaner approach would bump all count docstrings in a single Phase 4 pass after all enum members exist. This is a style risk, not a correctness risk.

---

## 4. Test Coverage Adequacy

**Grade: 4/5**

The §9 coverage matrix maps every FR sub-ID to a T-ID:

| FR | Test IDs |
|---|---|
| FR-8.1-8.6 | T-1101..T-1106, T-PUSH-WITHOUT-REREVIEW-NO-TICK |
| FR-9.1-9.5 | T-1110..T-1118 |
| FR-10.1-10.5 | T-1120..T-1125, T-AUGGIE-AT-MOST-ONCE |

Two NEW test modules (`test_review_retrigger.py`, `test_auggie_fallback.py`) plus 5 extended modules cover all T-IDs. The 7 fixtures (`decline-comment.json`, `rereview-attributed.json`, `rereview-then-decline.json`, `decline-initial-poll.json`, `decline-twice.json`, `stale-decline-pre-watermark.json`, `auggie-fallback-findings.json`) are named and described with their schemas.

**Strict-markers compliance:** The tasklist explicitly warns (Steps 3.6, 4.4, 4.5, 5.8, 5.9) that `--strict-markers` is ON and any new marker MUST be registered in `pyproject.toml` first. I verified the registered markers (pyproject.toml lines 114-140): `unit`, `integration`, `hallucination`, `performance`, `slow`, `confidence_check`, `self_check`, `reflexion`, `complexity`, `diagnostic*`, `e2e_trailing`, `backward_compat`, `property_based`, `nfr_benchmark`, `gate_performance`, `context_injection_test`, `thread_safety`, `agent_regression`, `imm`, `inv`, `loop_guard`, `autonomy`, `recovery`, `p0`. The tasklist instructs reusing `inv`, `loop_guard`, or `recovery` (all registered) or no marker. This is correct.

**Gap (deducted 1 point):** There is no explicit test item for **FR-8.5** (T-1105 — "the re-trigger token is one of the contract's accepted trigger phrases, sourced from the DetectionContract, never a hard-coded literal in the deterministic core"). The tasklist mentions T-1105 in Step 5.8 ("T-1105 (static: the script emits the trigger token, the core holds no hard-coded literal)") AND in Step 6.8(c) ("Add the static-parity tests ... T-1105 ... T-1115"). But Step 6.8(c) says "Add the static-parity tests" and includes T-1105 in `test_static_grep.py` — this is a static grep test, not a functional test. FR-8.5's requirement is that the re-trigger token comes from `DetectionContract.accepted_trigger_phrases`, not a hard-coded string. The tasklist does not specify a test that verifies the `retrigger-review.sh` script or the SKILL.md Wave 6 actually reads from the contract rather than hard-coding `auggie review`. T-1105 is partially covered by the static-grep assertion in Step 6.8(c), but the "sourced from DetectionContract" semantic is not functionally tested — only the absence of a hard-coded literal is asserted. This is a minor gap.

**Additionally:** The tasklist does not specify a test for **EC-21** ("Two declines in one run — 2nd decline → idempotency_skip"). The fixture `decline-twice.json` is created in Step 4.4, but the actual test asserting the 2nd-decline→skip behavior is only implicitly covered by "T-AUGGIE-AT-MOST-ONCE" in Step 5.9. It should be a dedicated test with a clear name like `test_second_decline_is_idempotency_skip`.

---

## 5. Verification Rigor

**Grade: 4/5**

The tasklist includes explicit per-phase validation gates:

- **Phase 2.4:** `make lint` + `uv run ruff format --check src/superclaude/pr_submit/models.py` + targeted pytest. This correctly applies the two-gate CI pattern (green make lint ≠ green format).
- **Phase 3.7 / 4.6 / 5.11 / 6.9:** Per-phase pytest runs with captured output.
- **Phase 7.2:** `make lint` + `uv run ruff format --check src/ tests/` — the full two-gate CI check across the whole tree. Correctly cites the project's CI gotcha.
- **Phase 7.1:** `make test` cross-cut check (to catch regressions outside `pr_submit/`).
- **Phase 6.9:** `make sync-dev` + `make verify-sync` for src→.claude mirror.
- **Step 8.2:** Final re-run of all four gates (`pytest` + `lint` + `format` + `verify-sync`) before marking Done.

**Gap (deducted 1 point):** Phase 3 and Phase 4 validation runs do NOT explicitly include `uv run ruff format --check` on their respective files. Phase 2.4 does (but only for `models.py`). The tasklist's Phase 7.2 covers the whole-tree format check, but if a formatter violation is introduced in Phase 3 or 4, it won't be caught until Phase 7 — potentially after the Phase 3/4 gates have passed. This is not critical (Phase 7.2 catches it before the PR ships), but it violates the "fail fast" discipline the tasklist claims. A lightweight fix would be adding `uv run ruff format --check` to Steps 3.7, 4.6, and 5.11 (the tasklist already knows this pattern from Phase 2.4).

---

## 6. Human-Decision Handling

**Grade: 5/5**

OQ-1 (recovery.py Branch-A resume target) is handled correctly:

- The tasklist explicitly marks it as **HUMAN-DECISION** (line 156).
- Step 5.7 (line 403-405) instructs: "write a PENDING decision record ... `DECISION: PENDING — requires human sign-off` ... leaving `recovery.py` SOURCE UNCHANGED, ensuring no default resume-target change is shipped."
- This follows memory `feedback_human_decision_items_must_halt`: write PENDING + halt the dependent spec/gate mutation; never auto-apply a default.

This is the correct posture. The tasklist does not silently change `recovery.py:111` to resume at `S5A_RETRIGGER_REVIEW` — it documents the trade-off and leaves the decision to the human.

---

## Additional Risks Identified

### RISK-1: `transition()` edge ordering and the needs_human_decision short-circuit

Step 5.3 adds 6 new edges to `transition()`. The tasklist correctly notes "the `needs_human_decision` short-circuit at the top of `transition()` stays FIRST" (line 389). However, the tasklist does not specify WHERE in the `if edge ==` chain the new edges should be inserted relative to the existing edges. If an executor inserts them in the wrong position (e.g., after the final `return state` fallback), the new edges will never be matched. The tasklist should specify an insertion anchor (e.g., "insert the new edges immediately after the existing `rereview_attributed` edge block").

### RISK-2: `fallback_skip` terminal selector is ambiguous

Step 5.3 says the `fallback_skip → TERMINAL_CLEAN | HALT_MAX_ROUNDS` selector "inspects the post-fallback residual-findings count, read from the `context`/`ctx` arg whose name matches the actual `transition()` signature — re-grep `def transition(` to bind it." This is a good instruction to re-grep, but the tasklist does not specify what the `transition()` function's actual second argument is named (it could be `ctx`, `context`, `event_data`, or something else). If the grep returns a different name, the executor must adapt. The "re-grep" instruction handles this, but the predicate encoding (`ctx.get("fallback_residual_findings")`) assumes a dict-with-key pattern that may not match the actual `transition()` signature.

### RISK-3: The `rereview_outcome` list indexing

Step 5.4 (line 393) gates the relocated `round_counter += 1` on `config.rereview_outcome[cycle_index] == "attributed"` with a guard for index-out-of-range. The tasklist says "guarding for index-out-of-range when the outcome sequence is shorter than the cycle list, defaulting to no-tick/timeout." This is correct but the tasklist does not specify the exact guard expression (e.g., `config.rereview_outcome[cycle_index] if cycle_index < len(config.rereview_outcome else None`). An executor could implement this incorrectly, causing a `None` comparison error.

### RISK-4: No test for `rebuild_state` with empty `auggie_review_invoked` set

The tasklist adds `auggie_review_invoked` to `IDEMPOTENCY_SETS` and specifies fold tests for when it IS populated (T-1120). But there is no explicit test that `rebuild_state()` on a run-log with NO `AUGGIE_FALLBACK_INVOKED` events produces an empty `auggie_review_invoked` set (the common case). This is not critical (it follows from the fold idiom), but it is a gap in the coverage matrix.

### RISK-5: Phase 7.1 runs `make test` which could be expensive

Step 7.1 runs `make test` (the cross-cut full suite) AFTER the `pr_submit/` suite. The tasklist notes this is to "catch any regression outside pr_submit." Given the heavy M3/M4 lens gates already planned for Phase 7, running the full `make test` could add significant time. This is not a correctness risk but a practical one — if the executor hits token/time limits, `make test` is the first candidate to trim.

---

## Dimension Summary

| Dimension | Score (0-5) | Key Issue |
|---|---|---|
| 1. Dependency ordering / DAG correctness | **4** | Phase 3.4 ref edit not sync'd until Phase 6; benign but worth noting |
| 2. NFR-6 core purity | **4** | No per-phase NFR-6 re-grep before Phase 5 |
| 3. Closed-enum integrity | **3** | Count-bump sites all found; transient-state risk between Phase 2 and 4 |
| 4. Test coverage adequacy | **4** | FR-8.5 semantic gap; EC-21 needs dedicated test name |
| 5. Verification rigor | **4** | Format gate only at Phase 2 and 7, not per-phase |
| 6. Human-decision handling | **5** | OQ-1 correctly HALT + PENDING, no default shipped |

---

## best_practice_grade: 4

**Concrete gaps / risks (6 items, none material enough to block execution):**

1. **FR-8.5 semantic test gap:** T-1105 asserts the core has no hard-coded trigger literal and the script emits `auggie review`, but does not verify the SKILL.md Wave 6 actually reads from `DetectionContract.accepted_trigger_phrases` rather than hard-coding the token. A test that validates the contract-field sourcing would close this.
2. **EC-21 needs a dedicated test:** The `decline-twice.json` fixture is created (Step 4.4) but the test asserting "2nd decline → idempotency_skip, auggie-review NOT re-invoked" should be a named `test_second_decline_is_idempotency_skip` in `test_auggie_fallback.py`, not just implicitly part of T-AUGGIE-AT-MOST-ONCE.
3. **Per-phase format gate missing:** Steps 3.7, 4.6, and 5.11 should each run `uv run ruff format --check` on their changed files, not defer all format checking to Phase 7.2. This enables faster feedback on formatter violations.
4. **`transition()` edge insertion anchor unspecified:** Step 5.3 should specify an insertion point (e.g., "after the `rereview_attributed` edge block") to prevent edges being placed after the `return state` fallback.
5. **`rereview_outcome` guard expression not specified:** Step 5.4's index-out-of-range guard should provide the exact Python expression to prevent `None` comparison errors.
6. **Empty `auggie_review_invoked` set rebuild test:** No test verifies `rebuild_state()` on a log with no `AUGGIE_FALLBACK_INVOKED` events produces an empty `auggie_review_invoked` set. Minor but a clean fold test.

## VERDICT: PROCEED

The tasklist is well-structured, correctly respects the dependency DAG, maintains NFR-6 core purity boundaries, handles the OQ-1 human decision correctly, and has thorough test coverage for the V1.1 functional requirements. The six gaps identified are refinements, not blockers. The closed-enum integrity dimension (3/5) is the highest-risk but all count-bump sites are identified — the deduction reflects the transient-state window, not a missing site.
