# Consolidated Findings — Phase Gate A (serialized fix protocol, I20)

**Generated:** 2026-06-11 11:30
**Step:** PGA.3
**Lens reports consolidated (5):**
- `qa-analyst-completeness-gateA.md` → PASS (0 findings)
- `qa-analyst-source-tracing-gateA.md` → PASS (0 findings)
- `qa-structural-evidence-quality-gateA.md` → PASS (0 findings)
- `qa-structural-core-purity-gateA.md` → PASS (0 findings)
- `qa-content-domain-accuracy-gateA.md` → **FAIL (3 findings: 1 CRITICAL, 1 IMPORTANT, 1 MINOR)**

## CONSOLIDATED VERDICT: FAIL

Per the any-finding-is-FAIL rule: the domain-accuracy lens surfaced 3 findings, all
rooted in a single defect in `detection.py::poll_augment_review`. The other 4 lenses
passed. One serialized fix agent (PGA.4) must resolve ALL three.

## Findings (deduplicated)

### C1 — CRITICAL — `src/superclaude/pr_submit/detection.py` (`poll_augment_review`, ~lines 137-139)
- **Originating lens:** DOMAIN-ACCURACY (also surfaced incidentally by CORE-PURITY's grep of `detection.py:139`, judged benign there — domain-accuracy correctly escalates it).
- **Issue:** When `contract is None`, `poll_augment_review` fabricates a default
  `DetectionContract(augment_bot_login="augment-code[bot]", locked=True)`. This:
  (a) **hard-guesses** the bot login `augment-code[bot]` — forbidden by spec §7 line 483
  ("NOT hard-guessed"); and (b) sets **`locked=True` in code** — an auto-lock forbidden by
  `feedback_human_decision_items_must_halt` and contradicting the R1 PENDING/HALT runbook.
- **Fix:** Replace the fabricated locked+guessed default with a NEUTRAL, UNLOCKED placeholder
  contract — `DetectionContract()` (i.e. `augment_bot_login=None`, `locked=False`, all fields
  at their dataclass defaults). With `augment_bot_login=None`, the classifier's
  `_augment_entries` returns `[]` (no bot match) so any payload classifies as `"polling"`
  ("review not detected") — the correct fail-safe per NFR-4. No login is guessed; nothing is
  auto-locked. (The empty-reviews "polling" path that T-201 exercises continues to work because
  empty reviews → no Augment entries → polling, independent of the login value.)

### C2 — IMPORTANT — `src/superclaude/pr_submit/detection.py` (lock-gate bypass)
- **Originating lens:** DOMAIN-ACCURACY.
- **Issue:** The `locked == true` gate (T-210) lives ONLY in `DetectionContract.load()`. The
  in-process convenience seam `poll_augment_review(pr_num)` never calls `load()`, so a caller
  using the default path bypasses the mechanically-enforced gate (§7 consequence 3).
- **Fix:** Keep `poll_augment_review` a pure classification convenience that NEVER fabricates a
  locked/guessed contract (covered by C1's neutral placeholder). The actual ARM gate remains in
  `load()` (raises `DetectionContractLocked`) and is the entry the SKILL.md arm step calls —
  document this in the `poll_augment_review` docstring so the seam's role (classification of an
  injected payload/contract, NOT arming) is unambiguous. No literal/auto-lock remains.

### C3 — MINOR — `src/superclaude/pr_submit/detection.py` (misleading comment)
- **Originating lens:** DOMAIN-ACCURACY.
- **Issue:** The comment "A default synthetic contract suffices for the empty-reviews ('polling')
  path; real arming loads the locked contract upstream (T-210)" papers over C1/C2 — it implies a
  default-contract path is benign without stating the default is a hard-guess+auto-lock.
- **Fix:** Replace the comment to state the neutral fail-safe behavior: with no contract, an
  unlocked placeholder (no bot login) is used so classification is fail-safe "polling" / "review
  not detected" (NFR-4); arming proper is gated by `DetectionContract.load()` (T-210) which HALTs
  on `locked:false`.

## Fix scope (PGA.4)
ONLY `src/superclaude/pr_submit/detection.py` is modified. After the fix, the existing
`test_detection_contract.py` (T-201 polling, T-210 HALT, T-211 not-detected) must still pass —
re-run `uv run pytest tests/pr_submit/test_detection_contract.py -v` to confirm.
