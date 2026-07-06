# QA Verification — Structural (Phase 3 fix-cycle re-verification)

**Topic:** pr_submit V1.1 — Phase 3 QA fix verification
**Date:** 2026-06-12
**Phase:** fix-cycle (structural lens)
**Fix authorization:** false (verify-only)
**Stance:** adversarial — confirm fixes landed AND introduced no new structural defect.

---

## Overall Verdict: PASS

All 4 ACTIONABLE fixes (F1–F4) are present and correct. F1 regex round-trips byte-equal
across all three sources and `locked: false` is preserved. No new structural defect:
exactly 3 V1.1 fields, all 3 wired in `from_yaml`, exactly 4 classifier states with
decline-first ordering, zero `gh`/`git` executable tokens added. F5–F8 each carry an
explicit DEFER/NO-FIX disposition in the consolidated findings (none silently dropped).
Test suite: 16 passed.

---

## (a) Each of the 4 ACTIONABLE fixes is present

| Fix | Claim | Evidence | Result |
|---|---|---|---|
| **F1** backtick regex — detection.py site 1 (field default) | char class widened to `["'\`]?` | `detection.py:84-86` field default `comment\s+["'\`]?(augment\|auggie\|augmentcode)\s+review["'\`]?`; necessary-deviation note `detection.py:78-82` | PASS |
| **F1** backtick regex — detection.py site 2 (`from_yaml` default) | same char class as `from_yaml` fallback | `detection.py:113-116` | PASS |
| **F1** backtick regex — ref YAML | ref default carries backtick | `detection-contract.md:27` `decline_retrigger_regex: 'comment\s+["''\`]?(augment\|auggie\|augmentcode)\s+review["''\`]?'` | PASS |
| **F1** fixture | backtick-wrapped decline fixture exists | `fixtures/decline-backtick.json:7` body contains `` Comment `augment review` `` | PASS |
| **F1** test | backtick test asserts `"declined"` | `test_detection_contract.py:209-220` `test_t1110_decline_backtick_wrapped_trigger`; asserts `` "`augment review`" in body `` (L218), `is_decline(...) is True` (L219), `classify(...) == "declined"` (L220) | PASS |
| **F2** co-occurrence test | findings-review + decline-comment → "declined" | `test_detection_contract.py:223-250` `test_t1110c_decline_wins_over_cooccurring_findings`; sanity `findings_only → "findings"` (L248), then co-occurring `→ "declined"` (L250) | PASS |
| **F3** 4-state docstring | poll docstring updated to 4-state incl. "declined" | module docstring `detection.py:1-2` lists `"polling"/"clean"/"findings"/"declined"`; `poll_augment_review` docstring `detection.py:201-204` lists all 4 incl. `"declined" (FR-9.1)` | PASS |
| **F4** T-1118 token | watermark test traceable to T-1118 | `test_detection_contract.py:313` test renamed `test_ec23_t1118_stale_pre_watermark_decline_ignored`; docstring L313-314 `EC-23 / T-1118` | PASS |

## (b) F1 round-trip byte-equality + `locked: false` preserved

Verified by executing a Python round-trip (`uv run python`) parsing all three sources to native strings:

- `DetectionContract().decline_retrigger_regex` (field default)
- `DetectionContract.from_yaml({}).decline_retrigger_regex` (from_yaml default)
- `yaml.safe_load(...)['decline_retrigger_regex']` (ref YAML block)

Result: all three equal the identical string
`comment\s+["'\`]?(augment|auggie|augmentcode)\s+review["'\`]?`
(`field == from_yaml: True`, `field == ref YAML: True`). The differing source-level
quoting (Python `"..."` with `\\"`, YAML single-quote with `''` doubling) collapses to
byte-identical parsed values. Match check confirms the regex hits BOTH a backtick-wrapped
trigger and a dquote-wrapped trigger (`matches backtick: True`, `matches dquote: True`).

`locked: false` preserved: `detection-contract.md:29` `locked: false`. Surrounding prose
(`:10`, `:15`, `:43-44`) still documents the build-BLOCKS-while-false / T-210 gate. PASS.

## (c) No new structural issue introduced

| Check | Evidence | Result |
|---|---|---|
| DetectionContract has exactly 3 new V1.1 fields | `detection.py:83` `decline_phrase_regex`, `:84-86` `decline_retrigger_regex`, `:87-93` `accepted_trigger_phrases` — 3 fields, no 4th | PASS |
| `from_yaml` wires all 3 | `detection.py:110-112` phrase, `:113-116` retrigger, `:117-120` accepted_trigger_phrases | PASS |
| `classify` returns exactly 4 states | `classifier.py:21-24` constants `STATE_POLLING/CLEAN/FINDINGS/DECLINED`; returns at `:129` DECLINED, `:133` POLLING, `:139/:141` FINDINGS, `:142` CLEAN — no 5th | PASS |
| Decline-first ordering | `classifier.py:127-129` decline loop runs BEFORE the `not augment_reviews`/findings/clean branches (`:131-142`); F2 test L250 independently proves precedence | PASS |
| No `gh`/`git` executable token added | grep `\b(gh\|git)\b` over both files: only `classifier.py:30` (`gh pr view` in payload-shape docstring) and `:76` (`no gh/git tokens` purity assertion) — both prose, no executable invocation; no `subprocess`/`os.system`/`Popen`/`check_output` | PASS |

## (d) F5–F8 correctly DEFERRED/NO-FIX (not silently dropped)

Each disposition is explicitly documented in `qa-consolidated-findings-phase3.md` and
echoed in `qa-fix-applied-phase3.md`:

| Item | Disposition | Consolidated-findings citation |
|---|---|---|
| F5 (`augment-code[bot]` hyphen vs real `augmentcode[bot]`) | **DEFER (no-fix, documented)** — Step 3.6 instructed matching fixtures; no runtime bug (classify keys on `contract.augment_bot_login`, not a literal); logged as Follow-Up | findings L19; fix-applied L15 |
| F6 (17/21 §9-matrix T-IDs untested) | **DEFER — out of Phase-3 scope** (Phase 4/5 tests; Steps 4.4/4.5/5.8/5.9) | findings L20; fix-applied L16 |
| F7 (phrase regex narrow) | **NO-FIX (documented)** — keep spec-literal `abnormally\s+large` | findings L21; fix-applied L17 |
| F8 (tautological fixture self-assert) | **NO-FIX** — harmless; real assertion follows | findings L22; fix-applied L18 |

All four are present with rationale. None dropped. PASS.

Adversarial note: I independently confirmed the F5 "no runtime bug" claim — `classify`
(`classifier.py:117`) and `is_decline` (`classifier.py:81`) both read
`contract.augment_bot_login` via `getattr`/attribute, never a hard-coded login literal —
so the hyphenated synthetic test login is a self-consistent test artifact, not a runtime
defect. Disposition is sound.

---

## Items Reviewed
| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | F1 detection.py site 1 (field) | PASS | detection.py:84-86 |
| 2 | F1 detection.py site 2 (from_yaml) | PASS | detection.py:113-116 |
| 3 | F1 ref YAML | PASS | detection-contract.md:27 |
| 4 | F1 fixture | PASS | decline-backtick.json:7 |
| 5 | F1 test | PASS | test_detection_contract.py:209-220 |
| 6 | F2 co-occurrence test | PASS | test_detection_contract.py:223-250 |
| 7 | F3 4-state docstring | PASS | detection.py:1-2, 201-204 |
| 8 | F4 T-1118 token | PASS | test_detection_contract.py:313-314 |
| 9 | F1 round-trip byte-equality | PASS | uv run python round-trip: field==from_yaml==ref YAML True |
| 10 | locked: false preserved | PASS | detection-contract.md:29 |
| 11 | exactly 3 V1.1 fields | PASS | detection.py:83,84-86,87-93 |
| 12 | from_yaml wires all 3 | PASS | detection.py:110-120 |
| 13 | classify exactly 4 states | PASS | classifier.py:21-24,129,133,139,141,142 |
| 14 | decline-first ordering | PASS | classifier.py:127-129 before 131-142 |
| 15 | no gh/git executable token | PASS | grep: only docstring prose; no subprocess |
| 16 | F5-F8 dispositions documented | PASS | findings L19-22 |
| 17 | test suite green | PASS | pytest test_detection_contract.py = 16 passed |

## Summary
- Checks passed: 17 / 17
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (verify-only)

## Confidence
- **Confidence:** Verified: 17/17 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 5 | Grep: 0 (via Bash) | Glob: 0 | Bash: 3

## QA Complete

VERDICT: PASS
