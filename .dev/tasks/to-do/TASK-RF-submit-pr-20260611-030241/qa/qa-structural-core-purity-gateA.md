# QA Report — Phase Gate A (Structural Lens: CORE-PURITY / INTERNAL-CONSISTENCY)

**Topic:** sc:pr-submit deterministic core — detection-contract gate (Phase 2)
**Date:** 2026-06-11
**Phase:** task-integrity / core-purity structural lens
**Lens:** CORE-PURITY / INTERNAL-CONSISTENCY
**Fix authorization:** false (report-only)
**Adversarial stance:** Assumed >= 5 purity/consistency violations; hunted for stray gh/git/anthropic tokens, literal bot logins, state mismatches.

---

## Files in scope

| File | Lines | Read | Greps run |
|------|------:|:----:|:---------:|
| `src/superclaude/pr_submit/detection.py` | 140 | yes | 4 |
| `src/superclaude/pr_submit/classifier.py` | 86 | yes | 4 |
| `src/superclaude/pr_submit/models.py` | 202 | yes | 3 |
| `tests/pr_submit/test_detection_contract.py` | 124 | yes | 1 |
| `qa-input-manifest-gateA.md` | 28 | yes | — |

---

## CHECK 1 — Command-token purity (NFR-6 / AC-9 / FR-G1)

Grep patterns run against `{detection,classifier,models}.py`: `\bgh \b`, `\bgit\b`, `subprocess`, `import anthropic`, `\banthropic\b`, plus a broader sweep for `os.system|Popen|run(|check_output|from anthropic`.

**Raw hits and adjudication:**

| File:Line | Hit | Verdict | Reason |
|-----------|-----|---------|--------|
| `classifier.py:25` | `` `gh pr view --json reviews` yields ... `` | BENIGN (docstring) | Prose in `_login_of` docstring describing the *payload shape* that the upstream bash poller produces. Documents data provenance, not a command invocation. No executable `gh` call. |
| `models.py:9-10` | `imports NO anthropic SDK and contains ZERO gh/git tokens` | BENIGN (docstring) | The module's own purity *assertion*. Quoted/negated prose, not an import or command. |

**Subprocess / SDK import sweep:** `subprocess`, `os.system`, `Popen`, `run(`, `check_output`, `import anthropic`, `from anthropic` — **0 hits** across all three files (exit=1, no match).

**Actual command-token violations: 0.** The two hits are docstring prose (one documenting the payload origin, one the purity claim itself). Neither is a `gh`/`git`/`subprocess`/`anthropic` command invocation or import. The core consumes an already-fetched payload; the real fetch is delegated to `scripts/poll-augment-review.sh` (detection.py:8-10).

**CHECK 1 result: PASS.**

---

## CHECK 2 — Internal consistency (loader/test/classifier)

### 2a. T-210 lock-gate HALT matches test expectation

- `detection.py:96-100`: `load()` with `require_locked=True` (default) raises `DetectionContractLocked` when `not contract.locked`.
- `detection.py:84-87`: absent ref also raises `DetectionContractLocked`.
- `detection.py:91-94`: unparseable YAML also raises `DetectionContractLocked`.
- `detection.py:101` / `:96`: `require_locked=False` returns the contract without HALT.

Test `test_t210_locked_false_halts` (test:71-92) asserts ALL FOUR arms:
- `DetectionContract.load()` (shipped `locked:false`) → `pytest.raises(DetectionContractLocked)` (test:74-75).
- explicit unlocked file → raises (test:78-84).
- absent file → raises (test:87-88).
- `require_locked=False` → returns, `inspected.locked is False` (test:91-92).

Loader behavior and test expectation are **consistent**. No mismatch.

### 2b. Classifier returns EXACTLY three states

Every `return` in `classify()` (classifier.py:60-86) resolves to one of `STATE_POLLING` (:77), `STATE_FINDINGS` (:83, :85), `STATE_CLEAN` (:86) — bound to `"polling"`/`"clean"`/`"findings"` at :17-19. No fourth state string is emitted. Helper returns (`_login_of`, `_augment_entries`, `_entry_has_findings`) return logins/lists/bools, not state strings. **Consistent** — exactly three documented states.

### 2c. No literal bot-login string in classifier.py

- `grep '\[bot\]' classifier.py` → **0 hits** (exit=1).
- `grep 'augment-code\[bot\]'` across all three src files → single hit at **`detection.py:139`** only.
- `classifier.py:70`: `bot_login = getattr(contract, "augment_bot_login", None)` — the classifier keys on the *contract field*, never a literal.

The one `augment-code[bot]` literal at `detection.py:139` is the `poll_augment_review` synthetic-contract default for the empty-reviews ("polling") path — explicitly the polling-seam default contract (per its inline comment :137-139), NOT a classifier match constant. Spec §7 consequence 1 (the CLASSIFIER must not key on a literal) is **satisfied**: the classifier dispatches solely on `contract.augment_bot_login`. The detection.py default is acceptable per the manifest adjudication note and spec §7 consequence 1.

**CHECK 2 result: PASS.**

---

## CHECK 3 — `MonitorState.S4_HALT_BEFORE_PUSH` prime-drop consistency

- `models.py:101`: `S4_HALT_BEFORE_PUSH = "S4_HALT_BEFORE_PUSH"  # spec S4'_HALT_BEFORE_PUSH` — unprimed Python identifier (apostrophe is illegal in identifiers), value string also unprimed, with an inline comment back-referencing the primed spec name.
- `models.py:5-6` and `:87-90`: module/class docstrings both state Python identifiers drop the spec's prime, and that "the ref/prose retain the primed spec name." This matches the Key Constraint (refs retain the prime; models/fsm drop it).

The unprimed identifier is **consistent and intentional**, documented in two places, and matches the Key Constraint. No violation.

**CHECK 3 result: PASS.**

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Command-token purity (gh/git/subprocess/anthropic) | PASS | 2 docstring-prose hits adjudicated benign (classifier.py:25, models.py:9-10); 0 subprocess/import hits across 3 files |
| 2a | T-210 lock-gate HALT ↔ test expectation | PASS | detection.py:84-100 raises on locked:false/absent/unparseable; test:74-92 asserts all 4 arms |
| 2b | Classifier emits EXACTLY 3 states | PASS | All returns → STATE_POLLING/CLEAN/FINDINGS (classifier.py:17-19,77,83,85,86); no 4th string |
| 2c | No literal bot-login in classifier.py | PASS | grep [bot] classifier.py = 0 hits; keys on getattr(contract, "augment_bot_login") at :70; sole literal is detection.py:139 poll-seam default |
| 3 | S4_HALT_BEFORE_PUSH prime-drop consistency | PASS | models.py:101 unprimed id + comment; docstrings :5-6,:87-90 document the constraint |

## Summary

- Checks passed: 5 / 5
- Checks failed: 0
- Critical issues: 0
- Important issues: 0
- Minor issues: 0
- Issues fixed in-place: 0 (fix_authorization: false)

## Issues Found

None. The adversarial hypothesis (>= 5 violations) was tested and not confirmed:

- **Stray gh/git/anthropic command token:** searched — only docstring prose found (payload-shape documentation + the purity assertion itself). No invocation/import.
- **Literal bot login in the classifier:** searched — `classifier.py` has zero `[bot]` literals; the sole `augment-code[bot]` literal lives at `detection.py:139` as the polling-seam default contract, which spec §7 consequence 1 permits (it forbids the *classifier* keying on a literal, not the poll-seam default).
- **State mismatch (extra/missing classifier state, loader↔test divergence, prime inconsistency):** searched — classifier emits exactly 3 states; loader HALT matches all 4 test arms; S4 prime-drop is documented and matches the Key Constraint.

## Confidence Gate

- Item 1 (command-token purity): [x] VERIFIED — Grep across 3 files, 2 hits read in context and adjudicated.
- Item 2a (T-210 loader↔test): [x] VERIFIED — Read detection.py:84-101 + test:71-92.
- Item 2b (3-state set): [x] VERIFIED — Grep all returns + Read classifier.py:60-86.
- Item 2c (no classifier literal): [x] VERIFIED — Grep [bot]/augment-code[bot] across 3 files + Read classifier.py:70.
- Item 3 (prime-drop): [x] VERIFIED — Read models.py:5-6,87-90,101 + Grep S4.

**Confidence:** Verified: 5/5 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 6 | Grep: 12 | Glob: 0 | Bash: 4
(Tool calls >= checklist items — not suspect.)

## QA Complete

## VERDICT: PASS
