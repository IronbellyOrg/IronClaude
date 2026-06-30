# QA Verification — Content Lens (Phase Gate A, post-fix)

**Generated:** 2026-06-11
**Phase:** Gate A content re-verification (`fix_authorization: false` — verify only)
**Scope:** Confirm the PGA.4 fix genuinely restores spec INTENT (not a cosmetic edit)
**File under verification:** `src/superclaude/pr_submit/detection.py`

---

## Overall Verdict: PASS

The PGA.4 fix genuinely restores spec intent for all three findings. The fabricated
`DetectionContract(augment_bot_login="augment-code[bot]", locked=True)` default is replaced by a
neutral, unlocked `DetectionContract()` whose semantics are provably fail-safe against the actual
classifier, the lock gate is honestly confined to `DetectionContract.load()`, and the
comments/docstrings now tell the truth. No new divergence introduced. All 6 tests pass.

---

## Judgments (each cites spec/memory AND artifact line)

### (a) C1 truly resolved — no hard-guess, no auto-lock; neutral default yields fail-safe "polling" — VERIFIED PASS

- **Spec intent (§7 line 483):** `augment_bot_login: "<PROBE-LOCKED>"  # e.g. "augment-code[bot]" — NOT hard-guessed`
  (verified via grep: line 483). The bot login must live in *data*, never guessed in code.
- **Memory intent (`feedback_human_decision_items_must_halt`):** human-decision items must HALT,
  never auto-default a change that ships. An in-code `locked=True` is exactly the forbidden auto-lock.
- **Artifact (detection.py:143-150):** the `if contract is None:` branch now assigns
  `contract = DetectionContract()` — all dataclass defaults (`augment_bot_login=None` at
  detection.py:50, `locked=False` at detection.py:58). No `"augment-code[bot]"` literal, no `locked=True`.
- **Grep confirmation:** `grep 'augment-code\[bot\]' src/superclaude/pr_submit/detection.py` → exit 1
  (no match). The hard-guessed literal is GONE from the core.
- **Fail-safe semantics independently verified against classifier.py (NOT taken on the fix log's word):**
  - `classifier._augment_entries` (classifier.py:39-43) returns `[]` when `bot_login` is falsy:
    `if not isinstance(entries, list) or not bot_login: return []`. With `augment_bot_login=None`,
    `not bot_login` is True → `[]` for ANY payload.
  - `classify` (classifier.py:74-77): `augment_reviews = _augment_entries(...)`; `if not augment_reviews: return STATE_POLLING`. So a `None` login → no Augment entries → `"polling"`.
  - `STATE_POLLING = "polling"` (classifier.py:17). This is the spec's fail-safe state:
    NFR-4 (spec line 804) "unknown/absent bot → 'review not detected'" and FR-2.2 (spec line 179)
    map exactly to "polling" (T-211, spec line 179, asserts `classify(...) == "polling"`).
  - **The only remaining `locked=True` in the file (detection.py:45) is inside a DOCSTRING** describing
    how *tests* construct synthetic contracts — not a production assignment (grep-confirmed; the sole
    code-path default is `DetectionContract()` at line 150).
- **Verdict:** C1 resolved. No login is guessed; nothing is auto-locked; the neutral default is
  provably the spec-correct fail-safe, not a workaround that hides the gate.

### (b) C2 — the §7-consequence-3 lock gate is NOT bypassable via the convenience seam — VERIFIED PASS

- **Spec intent (§7 consequence 3, spec lines 500-503 / contract ref lines 34-39):** the pre-flight
  asserts `contract.locked == true` and refuses to arm an unlocked contract — a mechanically-enforced
  sequencing dependency (T-210).
- **Artifact (detection.py:75-101):** the lock gate lives in `DetectionContract.load()`:
  `if require_locked and not contract.locked: raise DetectionContractLocked(...)` (lines 96-100).
  `require_locked` defaults to `True` (line 76). This is the genuine arm gate.
- **`poll_augment_review` never calls `load()` and never fabricates a `locked=True` contract**
  (detection.py:121-151): when `contract is None` it builds `DetectionContract()` with
  `locked=False`. Because the seam no longer manufactures a locked contract in-process, the default
  path cannot bypass the gate by inventing `locked=True` — the C1 neutral-placeholder edit *is* the
  C2 fix. The seam is honestly a *classification convenience*, not an arm path.
- **Docstring honesty (detection.py:134-139):** "This is a classification CONVENIENCE over an injected
  payload/contract — it is NOT the arm gate. Arming proper is gated by `DetectionContract.load`
  (T-210), which HALTs on `locked:false`." Accurate and unambiguous.
- **Test evidence:** T-210 (`test_t210_locked_false_halts`, test lines 71-92) confirms `load()` raises
  `DetectionContractLocked` for locked:false / absent / shipped contract, AND that `require_locked=False`
  inspection does not HALT. The shipped `detection-contract.md` ships `locked: false` (ref line 24),
  so live arming HALTs until the R1 probe flips it. Gate is intact.
- **Verdict:** C2 resolved. The arm gate remains exclusively in `load()` and is not bypassable; the
  seam's role is documented honestly.

### (c) C3 — comments/docstrings now tell the truth — VERIFIED PASS

- **Original defect (consolidated findings C3, lines 46-50):** the old comment "A default synthetic
  contract suffices for the empty-reviews ('polling') path; real arming loads the locked contract
  upstream (T-210)" papered over the hard-guess + auto-lock.
- **Artifact (detection.py:144-149):** the replacement comment states the neutral fail-safe behavior
  explicitly: "use a neutral UNLOCKED placeholder (no bot login) so classification is the fail-safe
  'polling' / 'review not detected' state (NFR-4) — augment_bot_login=None makes the classifier match
  no entries for ANY payload. No login is guessed and nothing is auto-locked. Arming proper is gated by
  DetectionContract.load() (T-210), which HALTs on locked:false." The comment now matches the code's
  actual behavior — no euphemism, names the NFR-4 fail-safe, names the real T-210 gate.
- **Verdict:** C3 resolved. Comment + docstring are truthful and consistent with code behavior.

### (d) No NEW divergence from spec intent introduced — VERIFIED PASS

- **Scope:** only `detection.py` was modified (fix log line 84; the change touches solely the
  `if contract is None:` branch + the `poll_augment_review` docstring). `classifier.py`,
  `DetectionContract.load()`, and `test_detection_contract.py` are untouched (grep + read confirm
  `load()` at lines 75-101 is the original gate; classifier read in full shows no edits).
- **No regression:** `uv run pytest tests/pr_submit/test_detection_contract.py -v` → **6 passed in 0.03s**
  (independently re-run, not taken on the fix log's word). T-201 polling, T-202 clean, T-203 findings,
  T-210 HALT, T-211 not-detected, T-212 interleaved all PASS.
- **No new literal / auto-lock:** grep for `augment-code[bot]` → exit 1 (gone); grep for `locked=True`
  → single hit at detection.py:45 (docstring only, not a code path).
- **The neutral default does not weaken any state transition:** the `clean`/`findings` paths require a
  matching Augment login (classifier.py:74-86); with `augment_bot_login=None` those paths are
  unreachable by construction, so the default can ONLY ever classify as `"polling"` — strictly
  fail-safe, never a false "clean" or false "findings".
- **Verdict:** no new divergence. The fix narrows behavior to the spec-correct fail-safe and adds no
  speculative surface.

---

## Self-Audit

**(a) Reliance list — items I did NOT re-verify structurally (delegated to prior lenses):**
- Relied on the 4 prior PASS lenses (completeness, source-tracing, evidence-quality, core-purity) for
  structural correctness of the QA artifacts themselves.

**(b) Independent semantic checks (≥1 required — verified with my own tool engagement):**
- C1 fail-safe semantics: verified by READING `classifier.py:39-43` (`not bot_login → []`) and
  `classifier.py:74-77` (`not augment_reviews → STATE_POLLING`), then confirming `STATE_POLLING="polling"`
  (classifier.py:17) — did NOT take the fix log's classifier claim on faith.
- No-regression: re-ran `uv run pytest tests/pr_submit/test_detection_contract.py -v` myself → 6 passed.
- Literal removal: re-ran `grep 'augment-code\[bot\]' detection.py` myself → exit 1.
- Auto-lock absence: re-ran `grep 'locked=True' detection.py` myself → only the docstring hit at line 45.
- Spec line 483 + NFR-4 line 804 + FR-2.2 line 179: read directly from `merged-spec.md`, not paraphrased.

**Confidence:** Verified: 4/4 judgments | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
**Tool engagement:** Read: 6 | Grep/Bash: 5 | Glob: 0

---

## VERDICT: PASS
