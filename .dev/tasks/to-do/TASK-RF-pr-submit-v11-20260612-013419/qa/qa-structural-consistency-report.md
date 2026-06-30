# QA Report — Internal-Consistency Lens (Phase 3, pr_submit V1.1)

**Topic:** pr_submit V1.1 detection-contract / classifier / fixtures structural consistency
**Date:** 2026-06-12
**Phase:** task-integrity (structural cross-file consistency lens)
**Fix cycle:** N/A
**Fix authorization:** false (report-only — nothing modified)

---

## Overall Verdict: FAIL

The five **mechanical** consistency claims I was asked to verify (STATE_DECLINED literal, regex byte-for-byte, accepted_trigger_phrases agreement, expected-block agreement, fixture-login ↔ AUGMENT-constant agreement) all hold **within the synthetic test surface** — the suite is internally self-consistent and all 14 tests pass.

BUT the adversarial sweep surfaced a load-bearing contradiction the in-suite checks cannot see: **the synthetic bot login baked into every fixture and the `AUGMENT` test constant (`augment-code[bot]`, hyphenated) does NOT match the real, probe-confirmed production login (`augmentcode[bot]`, no hyphen)** that the armed contract and project memory use. The suite passes only because the synthetic `contract` fixture is wrong in the *same* direction. This is a genuine internal inconsistency across the Phase-3 artifact set plus its production override, and it is mirrored in `augment_app_slug`. There is additionally an intra-file contradiction inside `test_detection_contract.py` itself.

Reporting FAIL is the honest call: a false PASS here would let a test suite that does not model the real bot login ship as "verified."

---

## Items Reviewed

| # | Check (from spawn prompt) | Result | Evidence |
|---|---|---|---|
| 1 | `STATE_DECLINED` == `"declined"` matches classifier ↔ test assertions | PASS | `classifier.py:24` `STATE_DECLINED = "declined"`, returned at `classifier.py:129`; asserted at `test_detection_contract.py:197,206,277,280`. Exact match. |
| 2 | `decline_phrase_regex` / `decline_retrigger_regex` defaults match BYTE-FOR-BYTE across detection.py field default, from_yaml default, and ref YAML, and are consistent with fixtures | PASS | Runtime-resolved values are identical across all three sources (verified by executing the loader): phrase `'abnormally\\s+large'`; retrigger `'comment\\s+["\']?(augment\|auggie\|augmentcode)\\s+review["\']?'`. Field `detection.py:78-81`; from_yaml `detection.py:105-111`; ref `detection-contract.md:26-27`. `field==ref==from_yaml` all `True`. Fixtures exercise both quote forms and match. |
| 3 | `accepted_trigger_phrases` agrees across field default, from_yaml default, ref YAML | PASS | All resolve to `['auggie review', 'augment review', 'augmentcode review']`. Field `detection.py:82-88`; from_yaml `detection.py:112-115`; ref `detection-contract.md:28`. Runtime equality `True`. |
| 4 | Each fixture's `expected` block agrees with the `classify`/`is_decline` return the tests assert | PASS | `decline-comment.json:11` `{"state":"declined"}` ↔ `test:196-197`; `decline-initial-poll.json:11` `{"state":"declined"}` ↔ `test:206`; `stale-decline-pre-watermark.json:12` `{"is_decline_with_watermark":false,"state_without_watermark":"declined"}` ↔ `test:276-280`. All consistent; tests pass. |
| 5 | Fixture bot login (`augment-code[bot]`) matches the test `AUGMENT` constant | PASS (literal match) **but the shared value is WRONG vs production** — see Issues #1, #4 | `AUGMENT` = `augment-code[bot]` (`test:28`); fixtures all `augment-code[bot]` (`decline-comment.json:5`, `decline-initial-poll.json:5`, `stale-decline-pre-watermark.json:5`). They match each other, satisfying the literal check — but both contradict the production login `augmentcode[bot]` (`.dev/pr-monitor/detection-contract.locked.md:17`). |

---

## Summary

- Checks passed (literal, as scoped): 5 / 5
- Checks failed (literal): 0
- **Cross-cutting inconsistencies found (adversarial): 5**
- Critical issues: 1 (HIGH); Important: 1; Minor: 3
- Issues fixed in-place: 0 (fix_authorization: false)
- Tests: 14/14 PASS (`uv run pytest tests/pr_submit/test_detection_contract.py`) — passing does NOT clear Issue #1 because the synthetic contract is wrong in the same direction as the fixtures.

---

## Issues Found

| # | Severity | Location (BOTH sides) | Issue | Required Fix |
|---|---|---|---|---|
| 1 | **HIGH** | Synthetic side: `tests/pr_submit/test_detection_contract.py:28` `AUGMENT = "augment-code[bot]"` + fixtures `decline-comment.json:5`, `decline-initial-poll.json:5`, `stale-decline-pre-watermark.json:5` (all `"augment-code[bot]"`). Production/ground-truth side: `.dev/pr-monitor/detection-contract.locked.md:17` `augment_bot_login: "augmentcode[bot]"  # confirmed: user.type == "Bot"` AND override test `test_detection_contract.py:107,119` `"augmentcode[bot]"` AND project memory `reference_augment_review_triggers.md:10` (`augmentcode[bot]`). | The entire decline/detection fixture set + `AUGMENT` constant model a bot login (`augment-code[bot]`, hyphen) that does NOT exist; the probe-confirmed real login is `augmentcode[bot]` (no hyphen). The synthetic `contract` fixture (`test:34-41`) sets `augment_bot_login=AUGMENT`, so classifier matching is self-consistent and tests pass — but the suite verifies behavior against a login the armed system will never see. Detection keys on the contract field (`classifier.py:48,82` — no production literal, good), so this is NOT a runtime bug in shipped code; it IS a test-fidelity inconsistency: green tests assert nothing about the real login. | Decide the single canonical login = `augmentcode[bot]` (probe-confirmed). Update `AUGMENT` (3 test files: `test_detection_contract.py:28`, `test_edge_cases.py:27`, `test_crash_recovery.py:30`) and all fixtures' `login` values to `augmentcode[bot]`. Re-run the suite. |
| 2 | IMPORTANT | `tests/pr_submit/test_detection_contract.py:28` (`AUGMENT = "augment-code[bot]"`) vs SAME FILE `:107` (`augment_bot_login: "augmentcode[bot]"`) and `:119` (`assert armed.augment_bot_login == "augmentcode[bot]"`) | Intra-file contradiction: one file asserts the Augment login is BOTH `augment-code[bot]` (synthetic classifier tests) AND `augmentcode[bot]` (override/arm test). A reader cannot tell which is the real login; the override test (correct value) silently disagrees with the file's own top-level constant. | Reconcile to `augmentcode[bot]` per Issue #1; the override test at `:107/:119` is already correct and should become the file-wide value. |
| 3 | MINOR | `augment_app_slug` — ref `detection-contract.md:18` `"augment-code"` + test contract fixture `test_detection_contract.py:37` `augment_app_slug="augment-code"` vs production `.dev/pr-monitor/detection-contract.locked.md:19` `augment_app_slug: "augmentcode"  # derived from the bot login` | Same hyphen contradiction as Issue #1, in a second field. Ref + synthetic test use `augment-code`; the probe-derived production slug is `augmentcode`. Not asserted by any decline test, so low blast radius, but it propagates the wrong-login error into a second field and the shipped ref. | Align ref `:18` and test fixture `:37` to `augmentcode` (or leave ref as `<PROBE-LOCKED>`-style placeholder; the ref's bot-login line `:16` correctly stays a placeholder while the slug line bakes a concrete wrong value). |
| 4 | MINOR | Spawn-prompt claim #5 vs reality — claim asserts "fixture bot login (`augment-code[bot]`) matches the test AUGMENT constant" as the success condition | The verification criterion itself encodes the wrong login as canonical. The literal match holds, but treating `augment-code[bot]` as correct masks Issue #1. Flagging per Principle 9 (self-audit): a PASS on claim #5 as written would be a false PASS. | When fixing Issue #1, also correct the canonical value referenced in any task/spec text that cites `augment-code[bot]` as the expected login. |
| 5 | MINOR | `tests/pr_submit/test_detection_contract.py:8-14` (docstring: Phase-10 `fixtures/*.json` "SUPERSEDES these inline dicts — when Phase 10 lands, swap the inline dicts for `load_fixture(...)`") vs current file state (`:47,55-60,67-72,131-136,150-153,160-182` still use inline dicts AND `:193-280` already use `load_fixture`) | The docstring's stated migration ("swap … rather than keeping both") is now violated: Phase-10 fixtures have landed (`fixtures/review-clean.json`, `review-with-findings.json`, `review-non-augment.json`, `review-interleaved.json` all exist) yet the inline dicts were NOT swapped — both coexist, exactly the state the docstring says to avoid. Separately, the docstring's "Phase 10 set" list does NOT mention the decline fixtures (`decline-comment.json`, `decline-initial-poll.json`, `stale-decline-pre-watermark.json`), so the V1.1 decline fixtures are undocumented in the file's own migration note. | Either complete the swap (replace inline T-201/202/203/211/212 dicts with `load_fixture`) or update the docstring to reflect the intentional dual state and add the V1.1 decline fixtures to the enumerated set. |

---

## What I Verified Positively (so PASS items are evidence-backed, not assumed)

- **Regex runtime-equality** was checked by executing the actual loader (`DetectionContract()`, `.from_yaml({})`, and `yaml.safe_load(_extract_yaml_block(ref))`) and comparing `repr()` — not by eyeballing the differently-escaped source forms (Python `r"..."` / `"\\s"` vs YAML single-quoted `'\s'` / `''` escaping). All three collapse to the identical runtime string. This is the only sound way to verify "byte-for-byte" across two escaping regimes.
- **No production bot-login literal** exists in `src/superclaude/pr_submit/*.py` (grep empty) — the classifier correctly keys on `contract.augment_bot_login` (`classifier.py:48,82`). This is why Issue #1 is a test-fidelity defect, not a shipped runtime bug.
- **Watermark comparison** (`classifier.py:95` `created > watermark`) is a lexicographic string compare; the EC-23 fixture's `createdAt` (`08:00:00Z`) and `watermark` (`09:30:00Z`) are same-format ISO-8601, so string ordering is correct here, and the test asserts both branches (`test:276,279`).
- **`createdAt` key plumbing**: `is_decline` reads `createdAt` OR `created_at` (`classifier.py:94`); all three fixtures supply `createdAt` (`:6` each). Consistent.

---

## Confidence

**Confidence:** Verified: 5/5 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 7 | Grep: 0 (folded into Bash greps) | Glob: 0 | Bash: 7 (incl. 1 live pytest run + 1 live python loader-equality check)

- Tool-call count (14 Read+Bash) ≥ checklist items (5 scoped claims) — not suspect.
- Every PASS cites specific file:line on both sides and, for claims 2/3, live runtime-equality output.
- Every Issue cites BOTH sides with file:line per the spawn instruction.

No UNCHECKED or UNVERIFIABLE items. The five scoped claims are literally PASS; the FAIL verdict is driven by the cross-cutting login/slug inconsistencies (Issues #1–#5) that the scoped literal checks structurally cannot catch — which is precisely the internal-consistency lens's job.

---

## Recommendations (before Phase 3 is considered consistent)

1. **Resolve Issue #1 first** — choose `augmentcode[bot]` (probe-confirmed) as the single canonical login; propagate to the 3 `AUGMENT` constants and all fixture `login` values; re-run `uv run pytest tests/pr_submit/`.
2. Reconcile the intra-file contradiction (Issue #2) as a direct consequence of #1.
3. Align `augment_app_slug` (Issue #3) to `augmentcode`.
4. Correct any task/spec text that cites `augment-code[bot]` as expected (Issue #4).
5. Resolve the docstring migration drift (Issue #5) or document the intentional dual state and enumerate the V1.1 decline fixtures.

## QA Complete

VERDICT: FAIL
- HIGH — Issue #1: fixtures + `AUGMENT` constant use `augment-code[bot]` (`test_detection_contract.py:28`; `decline-comment.json:5`; `decline-initial-poll.json:5`; `stale-decline-pre-watermark.json:5`) vs probe-confirmed production `augmentcode[bot]` (`.dev/pr-monitor/detection-contract.locked.md:17`; memory `reference_augment_review_triggers.md:10`).
- IMPORTANT — Issue #2: intra-file login contradiction `test_detection_contract.py:28` vs `:107`/`:119`.
- MINOR — Issue #3: `augment_app_slug` hyphen mismatch `detection-contract.md:18` + `test_detection_contract.py:37` (`augment-code`) vs `.dev/pr-monitor/detection-contract.locked.md:19` (`augmentcode`).
- MINOR — Issue #4: spawn-prompt claim #5 encodes the wrong login as canonical.
- MINOR — Issue #5: docstring SUPERSEDES migration violated / decline fixtures undocumented `test_detection_contract.py:8-14`.
