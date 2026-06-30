# Fix Application Log — Phase Gate A (serialized fix protocol, I20)

**Generated:** 2026-06-11
**Step:** PGA.4 (serialized fix agent)
**File modified:** `src/superclaude/pr_submit/detection.py` (ONLY)
**Fix authorization:** true
**Consolidated findings source:** `qa/qa-consolidated-findings-gateA.md`

## Overall result: ALL 3 FINDINGS FIXED

C1 (CRITICAL), C2 (IMPORTANT), and C3 (MINOR) all share a single root defect in
`poll_augment_review`'s `if contract is None:` branch. A single coordinated edit
resolves all three.

---

## Findings fixed

### C1 — CRITICAL — hard-guessed bot login + auto-lock in code

**Before** (lines 136-139):

```python
if contract is None:
    # A default synthetic contract suffices for the empty-reviews ("polling")
    # path; real arming loads the locked contract upstream (T-210).
    contract = DetectionContract(augment_bot_login="augment-code[bot]", locked=True)
```

**After:**

```python
if contract is None:
    # No contract supplied: use a neutral UNLOCKED placeholder (no bot login)
    # so classification is the fail-safe "polling" / "review not detected"
    # state (NFR-4) — augment_bot_login=None makes the classifier match no
    # entries for ANY payload. No login is guessed and nothing is auto-locked.
    # Arming proper is gated by DetectionContract.load() (T-210), which HALTs
    # on locked:false.
    contract = DetectionContract()
```

**Edit made:** Replaced the fabricated `DetectionContract(augment_bot_login="augment-code[bot]", locked=True)`
with the neutral, unlocked `DetectionContract()` (all dataclass defaults →
`augment_bot_login=None`, `locked=False`).

**Why this is correct (verified against `classifier.py`):**
`classifier._augment_entries` (classifier.py:39-43) returns `[]` when `bot_login`
is falsy (`None`). With `augment_bot_login=None`, ANY payload yields no Augment
entries, so `classify` returns `STATE_POLLING` (classifier.py:75-77) — the
fail-safe "review not detected" per NFR-4. No login is hard-guessed (spec §7 line
483 satisfied); nothing is auto-locked (`feedback_human_decision_items_must_halt`
satisfied).

### C2 — IMPORTANT — lock-gate bypass via the convenience seam

**Edit made:** Covered by the C1 edit (neutral placeholder) + the docstring update
below. `poll_augment_review` no longer fabricates a locked/guessed contract, so the
default path can no longer bypass the gate by manufacturing a `locked=True` contract
in-process. The actual ARM gate remains exclusively in `DetectionContract.load()`
(unchanged — raises `DetectionContractLocked` on `locked:false`). The docstring now
states the seam is a classification convenience, NOT the arm gate.

**Docstring added to `poll_augment_review`:**

> This is a classification CONVENIENCE over an injected payload/contract — it is
> NOT the arm gate. Arming proper is gated by `DetectionContract.load` (T-210),
> which HALTs on `locked:false`. When no `contract` is supplied here, a neutral
> UNLOCKED placeholder (no bot login) is used, so classification is the fail-safe
> `"polling"` / "review not detected" state (NFR-4) — no login is guessed and
> nothing is auto-locked.

### C3 — MINOR — misleading inline comment

**Edit made:** Replaced the old comment ("A default synthetic contract suffices for
the empty-reviews ('polling') path; real arming loads the locked contract upstream
(T-210).") with a comment that states the neutral fail-safe behavior explicitly
(see the "After" block under C1).

---

## Constraints honored

- Modified ONLY `src/superclaude/pr_submit/detection.py`. ✓
- `DetectionContract.load()` (the real T-210 gate) NOT changed. ✓
- `DetectionContract()` with no args is constructible — all fields carry dataclass
  defaults (detection.py:50-58: `augment_bot_login: str | None = None` …
  `locked: bool = False`). ✓
- `classifier.py` and `test_detection_contract.py` untouched. ✓

---

## Verification

### Pytest re-run

```
$ uv run pytest tests/pr_submit/test_detection_contract.py -v
tests/pr_submit/test_detection_contract.py::test_t201_empty_reviews_polling PASSED [ 16%]
tests/pr_submit/test_detection_contract.py::test_t202_augment_clean PASSED [ 33%]
tests/pr_submit/test_detection_contract.py::test_t203_augment_findings PASSED [ 50%]
tests/pr_submit/test_detection_contract.py::test_t210_locked_false_halts PASSED [ 66%]
tests/pr_submit/test_detection_contract.py::test_t211_different_bot_not_detected PASSED [ 83%]
tests/pr_submit/test_detection_contract.py::test_t212_interleaved_only_augment_parsed PASSED [100%]

============================== 6 passed in 0.03s ===============================
```

**Result: 6 passed** (all original tests still pass — no regression).

### Grep for the removed literal

```
$ grep -n 'augment-code\[bot\]' src/superclaude/pr_submit/detection.py
(no match — exit 1)
```

**Result: the hard-guessed `augment-code[bot]` literal is GONE from
`detection.py`** (acceptable nowhere in the core now; the only remaining occurrence
of that string in the test suite is the test fixture's `AUGMENT` constant, which is
out of scope and correct as a synthetic test contract).

---

## Adversarial self-check (post-fix)

- No new literal or auto-lock introduced.
- The neutral-placeholder path is exercised only when `contract is None`; all 6
  tests pass explicit contracts, so behavior under test is unchanged. The new
  default path is provably fail-safe via the classifier's falsy-`bot_login`
  short-circuit.
- Scope confined to a single file; no collateral edits.

## QA Fix Complete
