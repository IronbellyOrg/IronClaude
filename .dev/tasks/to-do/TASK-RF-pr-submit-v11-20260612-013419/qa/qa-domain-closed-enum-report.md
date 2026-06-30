# QA Report — Closed-Enum / State-Set Domain Lens

**Topic:** pr_submit V1.1 — closed-enum / state-set integrity (classifier states + DetectionContract fields)
**Date:** 2026-06-12
**Phase:** report-validation (domain lens, Phase 3)
**Fix cycle:** N/A
**Fix authorization:** false (report only — nothing modified)

---

## Overall Verdict: PASS

Both required counts are exact. The 4-state closed enum holds (4 distinct
emitted values across 5 return statements — the duplication is `findings`
via two predicates, not a 5th state), the decline branch is ordered FIRST,
and the 3 new `DetectionContract` fields are present and fully wired through
`from_yaml`.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | `classify()` emits EXACTLY 4 distinct states `{polling, clean, findings, declined}` | PASS | State constants `classifier.py:21-24`. Return statements in `classify()`: `:129` (declined), `:133` (polling), `:139` (findings), `:141` (findings), `:142` (clean). 5 returns → **4 distinct values**; `STATE_FINDINGS` is returned at both `:139` and `:141` (two predicates, same state). No 5th state value exists. |
| 2 | Decline branch ordered FIRST | PASS | Decline loop `classifier.py:127-129` returns `STATE_DECLINED` at `:129` BEFORE polling (`:131-133`), findings (`:138-141`), clean (`:142`). Docstring `:124-126` and module docstring `:8-10` confirm intent. |
| 3 | No stray/extra return path that could be a 5th state | PASS | `is_decline` (`classifier.py:65-97`) returns `bool` (predicate, not a state) — correctly excluded. Helpers `_login_of` (`:27-41`), `_augment_entries` (`:44-48`), `_entry_has_findings` (`:51-62`) return non-state types. Only `classify()` emits states. |
| 4 | `DetectionContract` gained EXACTLY 3 new fields | PASS | `detection.py:78` `decline_phrase_regex: str`, `:79-81` `decline_retrigger_regex: str`, `:82-88` `accepted_trigger_phrases: list[str]`. Exactly 3 under the V1.1 banner `:73`. No additional new fields. Pre-existing fields `:64-72` unchanged in count. |
| 5 | `decline_phrase_regex` wired through `from_yaml` | PASS | `detection.py:105-107` `decline_phrase_regex=data.get("decline_phrase_regex", r"abnormally\s+large")` — default matches dataclass default `:78`. |
| 6 | `decline_retrigger_regex` wired through `from_yaml` | PASS | `detection.py:108-111` `decline_retrigger_regex=data.get("decline_retrigger_regex", ...)` — default matches dataclass default `:79-81`. |
| 7 | `accepted_trigger_phrases` wired through `from_yaml` | PASS | `detection.py:112-115` `accepted_trigger_phrases=list(data.get("accepted_trigger_phrases") or [...])` — fallback list matches dataclass default_factory `:82-88`. |
| 8 | All 3 fields consumed by the decline predicate (state-set is reachable, not dead) | PASS | `is_decline` reads `decline_phrase_regex` (`classifier.py:84`) and `decline_retrigger_regex` (`:85`), both required to match (`:86-92`). `accepted_trigger_phrases` is the operator re-trigger token set (NOT consumed by `is_decline` — by design, per `detection.py:76-77`); see Issues Found #1 (MINOR observation, not a defect). |

---

## Summary

- Checks passed: 8 / 8
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: N/A (fix_authorization: false)

**Exact counts (the two assigned questions):**

- **Q1 — `classify()` distinct states:** EXACTLY **4** (`polling`, `clean`,
  `findings`, `declined`). Return-statement count is 5, but `findings` is emitted
  by two distinct predicates (`classifier.py:139` and `:141`). No 5th distinct
  state. Decline branch ordered **FIRST** (`:127-129`, returns at `:129`). ✓
- **Q2 — new `DetectionContract` fields:** EXACTLY **3**
  (`decline_phrase_regex` `:78`, `decline_retrigger_regex` `:79-81`,
  `accepted_trigger_phrases` `:82-88`). All **3 wired** through `from_yaml`
  (`:105-107`, `:108-111`, `:112-115`). ✓

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | OBSERVATION (not a defect) | `classifier.py:65-97` / `detection.py:82-88` | `accepted_trigger_phrases` is a `DetectionContract` field wired through `from_yaml` but is NOT read by `is_decline` or any function in classifier.py/detection.py. This is intentional per the inline comment (`detection.py:76-77`: it is the "canonical operator re-trigger token set", consumed elsewhere — e.g. the SKILL arm/re-trigger step, not the pure classifier). Flagged for transparency only — it does NOT affect either assigned count and is not a closed-enum violation. | None. If a downstream consumer is expected, confirm a reference exists in the SKILL/poller layer (outside this lens's scope). |

No enum/state-set integrity errors found. The adversarial hypothesis (a 5th
state-return path, or a field not wired into `from_yaml`) was tested directly:
the 5th return statement at `classifier.py:141` was the prime suspect, and it
resolves to the SAME state value `STATE_FINDINGS` as `:139` — a two-predicate
path, not a distinct enum member. Both `from_yaml` wirings for all 3 fields are
present with matching defaults.

---

## Actions Taken

None — fix_authorization: false. Report only; no files modified.

---

## Recommendations

- None blocking. The closed enum and field set are exact and correctly wired.
- Optional (outside this lens): a downstream-reference check that
  `accepted_trigger_phrases` is actually consumed by the SKILL re-trigger
  step would close the loop on Observation #1, but it is not a defect in the
  two files under review.

---

## Confidence

- **Confidence:** Verified: 8/8 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 2 | Grep: 0 | Glob: 0 | Bash: 0

Both target files (`classifier.py` 143 lines, `detection.py` 221 lines) were
read in full. Every state-return and every field/wiring claim is cited to an
exact line read directly from source. Tool-call count (2 Reads) is below the
checklist-item count (8) because both files fit in single full reads — every
one of the 8 checks maps to specific lines within those two reads, so no item
is unverified. No external/web lookup was required (all claims are local source
truth).

## QA Complete

VERDICT: PASS
