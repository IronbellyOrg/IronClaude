# QA Report — Phase Gate A (Detection-Gate, content/domain-accuracy lens)

**Lens:** RESEARCH-DEPTH / DOMAIN-ACCURACY
**Phase:** Phase Gate A — Detection Contract Gate (spec §3 step 0 / DAG root)
**document_type:** Detection-gate build artifacts
**Date:** 2026-06-11
**fix_authorization:** false (report-only)
**Stance:** ADVERSARIAL — assume ≥5 spec/behavior divergences exist; prove they do or don't.

---

## Scope of judgment

Three intent-faithfulness questions, each cited against spec §7 (merged-spec.md
lines 473–507) AND the artifact:

1. Is the R1 probe a genuine HALT that NEVER auto-locks and NEVER hard-guesses
   `augment_bot_login` (memory `feedback_human_decision_items_must_halt`)?
2. Does `locked:false` ACTUALLY block arming (RAISE/HALT), not merely warn?
3. Is the classifier genuinely generic/data-driven, not hard-coded?

---

## Tool engagement

Read: 6 (manifest, spec §7, runbook, detection-contract.md, detection.py, classifier.py, test file)
Grep: 1 (literal-login / locked-default sweep across classifier.py + detection.py + contract.md)
Bash: 1 (`uv run pytest tests/pr_submit/test_detection_contract.py` → 6 passed)

---

## Judgment 1 — R1 probe is a genuine HALT; no auto-lock; no hard-guess (ref + runbook)

**Spec intent (§7 lines 483, 491; consequence 1 lines 496–498; consequence 3 lines 500–503):**
`augment_bot_login: "<PROBE-LOCKED>"` "NOT hard-guessed"; `locked: false` "R1 flips
this to true; build BLOCKS while false"; the login "lives in data". Memory
`feedback_human_decision_items_must_halt`: a `needs_human_decision` item must write
PENDING + halt the dependent mutation, never auto-apply a default that ships a change.

**Artifact evidence:**
- `detection-contract.md:16` ships `augment_bot_login: "<PROBE-LOCKED>"` (placeholder,
  not a guessed login). `detection-contract.md:24` ships `locked: false`. PASS.
- `r1-detection-probe-runbook.md:5` Status `PENDING — CANNOT run autonomously`; lines
  64–82 are an explicit HALT note (installation unconfirmed, ZERO captured Augment JSON
  in `.dev/`): "writes PENDING and HALTs the **lock path only**. It NEVER auto-locks the
  contract and NEVER hard-guesses `augment_bot_login`." PASS.
- The runbook correctly distinguishes the in-session `/sc:auggie-review` from the
  GitHub-App reviewer (lines 70–72) — it does not conflate them to manufacture a probe
  result. Research-depth: accurate. PASS.

**Verdict for the ref + runbook surface:** FAITHFUL. The shipped ref and the operator
runbook honor "NEVER auto-lock / NEVER hard-guess." BUT an adversarial cross-check of the
*production loader* surface uncovers a hard-guess + auto-lock that this prose disclaims —
see **Finding C1**.

---

## Judgment 2 — `locked:false` ACTUALLY blocks arming (RAISE, not warn)

**Spec intent (§7 consequence 3 lines 500–503):** "The pre-flight asserts
`contract.locked == true` and **refuses to arm** … turning R1 from a 'should' into a
**mechanically-enforced** sequencing dependency." Manifest AC: "`locked:false` HALT path
present (T-210)".

**Artifact evidence (`detection.py`):**
- `DetectionContractLocked(RuntimeError)` (line 33) is a real exception type.
- `load()` (lines 96–100): `if require_locked and not contract.locked:` → `raise
  DetectionContractLocked(...)`. This is a genuine **raise**, not a log/warn. PASS.
- `require_locked: bool = True` (line 76) — the gate is ON by default; a caller must
  explicitly opt OUT (`require_locked=False`) to inspect. PASS.
- Absent file (lines 84–87) and unparseable YAML (lines 91–94) ALSO raise — fail-closed.
  PASS.
- `test_t210_locked_false_halts` (test lines 71–92) proves all three raise paths
  (shipped-ref, explicit-unlocked, absent) via `pytest.raises(DetectionContractLocked)`,
  and that `require_locked=False` returns `locked is False` without raising. Ran live:
  **6/6 passed** — matches the gate verdict (no hallucinated counts). PASS.

**Verdict:** FAITHFUL on the `load()` path — it RAISES, fail-closed, gated-on by default.
**However**, the manifest claims `load()` is the *only* arming entry; the second in-process
entry `poll_augment_review` BYPASSES `load()` entirely — see **Finding C1**.

---

## Judgment 3 — classifier is generic/data-driven, not hard-coded

**Spec intent (§7 consequence 1 lines 496–498):** "It contains
`if login == contract.augment_bot_login`, never a literal string. The login lives in data."

**Artifact evidence (`classifier.py`):**
- `bot_login = getattr(contract, "augment_bot_login", None)` (line 70) — the login is read
  from the contract, never embedded. PASS.
- `_augment_entries(entries, bot_login)` (lines 39–43) filters on `_login_of(e) ==
  bot_login` — the spec's exact `login == contract.augment_bot_login` shape. PASS.
- Grep sweep of `classifier.py` for `augment-code` / `<PROBE-LOCKED>`: ZERO literal logins
  in branch logic (only doc-comment references at lines 5 and the field name at line 70).
  PASS.
- T-211 (different bot → polling) and T-212 (interleaved → only Augment parsed) pass live,
  confirming the keying is genuinely data-driven. PASS.

**Verdict:** FAITHFUL. `classifier.py` is purely generic and data-keyed.

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| C1 | CRITICAL | `detection.py:137-139` | `poll_augment_review` fabricates a default `DetectionContract(augment_bot_login="augment-code[bot]", locked=True)` when `contract is None`. This simultaneously (a) **hard-guesses** the bot login `augment-code[bot]` — the exact string §7 line 483 forbids ("NOT hard-guessed") and the runbook swears is never guessed — and (b) **auto-locks** (`locked=True`), the precise auto-lock that `feedback_human_decision_items_must_halt` and the runbook (lines 73–75) say "NEVER" happens. It is in PRODUCTION code, not a test fixture. | Remove the auto-lock default. `poll_augment_review` with `contract is None` must call `DetectionContract.load()` (which RAISES on `locked:false`), or accept no implicit default and require an explicit locked contract. The literal `"augment-code[bot]"` must not appear in `detection.py`. |
| C2 | IMPORTANT | `detection.py:121-140` vs manifest line 25 / Judgment-2 intent | The `locked==true` gate lives ONLY in `load()`. `poll_augment_review` — the in-process poll/arm seam — never consults `load()` and never checks `locked`, so the "mechanically-enforced" gate (§7 consequence 3) has a bypass path: any caller invoking `poll_augment_review(pr_num)` with no contract arms against a synthetic locked contract without ever running the probe. The gate is not enforced at the seam the spec calls "arming". | Route `poll_augment_review`'s contract acquisition through the lock gate (call `load()` when no contract is supplied) so the HALT is enforced on every arming path, not just direct `load()` callers. |
| C3 | MINOR | `detection.py:139` comment | The inline comment claims "real arming loads the locked contract upstream (T-210)" — but nothing in this module or the shipped artifacts demonstrates that upstream `load()` call exists; it is an unproven assertion that papers over C1/C2. At Gate A there is no caller wiring to verify the claim. | Either land the upstream `load()` caller (and cite it) or soften the comment to not assert a guarantee the code does not provide. |

### Finding detail — C1 (the headline divergence)

Spec §7 line 483: `augment_bot_login: "<PROBE-LOCKED>"  # … — NOT hard-guessed`.
Runbook lines 73–75: "this item writes PENDING and HALTs the lock path only. It NEVER
auto-locks the contract and NEVER hard-guesses `augment_bot_login`."

`detection.py:139`:
`contract = DetectionContract(augment_bot_login="augment-code[bot]", locked=True)`

This is the literal hard-guess (`augment-code[bot]`) AND the auto-lock (`locked=True`) the
spec and the human-decision-HALT memory both prohibit, sitting in shippable production
code. The contract ref and runbook honor the intent on paper; the loader contradicts it.
Even though `poll_augment_review`'s current `_fetch_payload` default yields empty reviews
(so the guessed login is presently inert for the "polling" path), the guessed constant and
the `locked=True` default are latent: the moment a real payload is injected without an
explicit contract, classification runs against a GUESSED login that was never probe-locked,
and arming proceeds under a contract that never passed T-210. This is precisely the
"auto-default that ships a change" the memory exists to prevent.

### Why test-suite GREEN does not clear C1/C2

The 6 passing tests all pass an EXPLICIT locked synthetic `contract` fixture (test lines
33–40) into `classify` / `poll_augment_review`, so the `contract is None` default branch at
`detection.py:137-139` is **never exercised**. T-210 only tests the `load()` path. There is
NO test asserting that `poll_augment_review(pr_num)` with no contract refuses to arm —
the bypass is untested and therefore invisible to the gate. (Research-depth note: a faithful
gate would include a T-210-sibling proving the in-process seam also HALTs.)

---

## Adversarial-stance accounting (≥5 divergence probes)

The stance required hunting ≥5 places where behavior could diverge from intent. Probed:

1. Auto-lock of the shipped contract → NOT found in the ref (`locked:false` at line 24). Clear.
2. Hard-guessed login in the ref → NOT found (`<PROBE-LOCKED>` at line 16). Clear.
3. Hard-guessed login in PRODUCTION loader → **FOUND** (C1, `detection.py:139`).
4. Auto-lock in production loader → **FOUND** (C1, `locked=True` default).
5. `locked:false` merely warns instead of raising in `load()` → NOT found (genuine raise, lines 96–100). Clear.
6. Arming seam that bypasses the lock gate → **FOUND** (C2, `poll_augment_review` never calls `load()`).
7. Literal login in classifier branch logic → NOT found (keys on `contract.augment_bot_login`, line 70). Clear.
8. Hallucinated/inflated pass counts in the gate verdict → NOT found (live run: 6 passed, matches). Clear.

3 genuine divergences surfaced (C1, C2, C3); 5 probes cleared with evidence. The "0 findings
would be suspect" bar is satisfied with concrete file:line evidence on both sides.

---

## Self-Audit

1. **Factual claims independently verified against source:** All three judgments + all three
   findings cite specific file:line. Verified the contract `locked:false`/`<PROBE-LOCKED>`
   (grep + Read), the `load()` raise path (Read lines 96–100), the classifier keying (Read
   line 70 + grep for literals), the `poll_augment_review` auto-lock default (Read lines
   137–139 + grep `augment-code` in detection.py), and the live test outcome (Bash, 6/6).
2. **Files read:** detection-contract.md, detection.py, classifier.py,
   test_detection_contract.py, r1-detection-probe-runbook.md, the manifest, spec §7.
3. **Why trust the check:** This is NOT a 0-finding rubber-stamp. The grep that confirmed
   "no literal in classifier.py" is the SAME grep that surfaced the literal
   `augment-code[bot]` in detection.py:139 — the headline CRITICAL. The ref/runbook pass on
   intent; the loader fails it. That asymmetry is the evidence the surfaces were read
   independently rather than assumed consistent.
4. **Web research:** none performed (all verification was local-file + local-test bound);
   no Tavily/fallback engagement to record.

**Confidence:** Verified: 8/8 probes | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%

---

## Recommendations (report-only; fix_authorization:false)

1. **Blocking for arm-readiness:** Fix C1 — delete the hard-guessed `"augment-code[bot]"` +
   `locked=True` default from `detection.py:139`; route `poll_augment_review`'s no-contract
   path through `DetectionContract.load()` so it inherits the T-210 raise.
2. Fix C2 in the same change — the lock gate must hold at the `poll_augment_review` seam,
   not only at direct `load()` callers.
3. Add a regression test: `poll_augment_review(pr_num)` with no explicit contract must raise
   `DetectionContractLocked` while the shipped ref is `locked:false` (the missing
   in-process-seam sibling of T-210).
4. C3: reconcile or soften the "real arming loads the locked contract upstream" comment once
   the wiring exists.

---

## VERDICT: FAIL
