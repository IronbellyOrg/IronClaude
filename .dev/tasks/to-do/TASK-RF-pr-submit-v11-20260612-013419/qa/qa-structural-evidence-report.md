# QA Report — Phase 3 Structural Evidence / Anchor-Freshness Lens

**Task:** TASK-RF-pr-submit-v11-20260612-013419 (sc:pr-submit V1.1)
**Lens:** evidence-quality / anchor-freshness (classifier + detection + detection-contract tests)
**Date:** 2026-06-12
**Stance:** ADVERSARIAL — assume ≥5 stale-anchor / unsupported-claim defects exist.
**Fix authorization:** false (report only; nothing modified).

---

## Scope

Files read in full and verified:

- `src/superclaude/pr_submit/classifier.py`
- `src/superclaude/pr_submit/detection.py`
- `tests/pr_submit/test_detection_contract.py`
- `.dev/tasks/.../phase-outputs/discovery/anchor-map.md`

Supporting reads: `src/superclaude/pr_submit/__init__.py`, `tests/pr_submit/conftest.py`,
the 3 decline fixtures, and spot-checks of `fsm.py` / `models.py` against the anchor map.

---

## Verification Results (the three required checks)

### Check 1 — Phase 3 edits landed at CURRENT symbol locations (not frozen line numbers)

**PASS.** The classifier/detection symbols referenced by the Phase 3 edits all exist at
their current locations, verified by grep, not by trusting spec line numbers:

- `is_decline` defined at module scope (column 0) — `classifier.py:65`.
- `classify` — `classifier.py:100`; it calls `is_decline(entry, contract, watermark=watermark)`
  at `classifier.py:128`.
- `STATE_DECLINED = "declined"` — `classifier.py:24`; consumed at `classifier.py:129`
  (`return STATE_DECLINED`).
- New `DetectionContract` decline fields exist and are wired through the loader:
  `decline_phrase_regex` (`detection.py:78`), `decline_retrigger_regex` (`detection.py:79`),
  `accepted_trigger_phrases` (`detection.py:82`); `from_yaml` round-trips all three at
  `detection.py:105-115`.
- Public re-exports present: `classify`, `is_decline`, `STATE_DECLINED` at
  `__init__.py:21` / `:42` and in `__all__` (`__init__.py:39-44`).

### Check 2 — No edit references a non-existent symbol

**PASS.** Every symbol named in an edit resolves to a real definition:

- `classify` → `is_decline` (defined module-scope, `classifier.py:65`) — not a method, not
  a nested fn; the adversarial "is_decline must be defined at module scope" concern is
  satisfied (`grep -n '^def is_decline'` → line 65).
- `classify` → `STATE_DECLINED` / `STATE_POLLING` / `STATE_CLEAN` / `STATE_FINDINGS`
  (`classifier.py:21-24`).
- `detection.py` imports `classify` from `.classifier` (`detection.py:21`) — resolves.
- Tests import `DetectionContract`, `DetectionContractLocked`, `classify`, `is_decline`,
  `poll_augment_review` from `superclaude.pr_submit` — all in `__all__`. Collection +
  import succeed (suite runs, see Check 3).

### Check 3 — Every test expectation traces to actual code behavior (no fabricated expectations)

**PASS.** Each new test's asserted result was reproduced from the actual `is_decline` /
`classify` source and fixtures, then confirmed by running the suite
(`14 passed in 0.04s`, 0 skips/xfails — no fabricated expectation hidden behind a skip).

Per-test trace (regexes executed against the real bodies):

| Test | Body (source) | phrase re | retrigger re | `is_decline` | classify | Asserted | Match |
|---|---|---|---|---|---|---|---|
| `test_t1110` | `decline-comment.json` | ✓ | ✓ | True | declined | declined / True | ✓ |
| `test_t1110b` | `decline-initial-poll.json` (`'auggie review'`) | ✓ | ✓ | — | declined | declined | ✓ |
| `test_t1111` (phrase-only) | inline `"…abnormally large."` | ✓ | **✗** | **False** | **polling** | False / polling | ✓ |
| `test_t1112` (retrigger-only) | inline `'…comment "augment review"…'` | **✗** | ✓ | False | polling | False / polling | ✓ |
| `test_t1112b` (non-Augment author) | inline, login `octocat` | ✓ | ✓ | False (login gate, `classifier.py:82`) | polling | False / polling | ✓ |
| `test_ec23` (stale pre-watermark) | `stale-decline-pre-watermark.json` | ✓ | ✓ | False *with* watermark / True *without* | declined w/o wm | see below | ✓ |

- **`test_t1111` (phrase-only → NOT decline)** — confirmed genuinely produced by the code:
  body `"Heads up: this diff is abnormally large."` matches `abnormally\s+large` but NOT
  `comment\s+["']?(augment|auggie|augmentcode)\s+review["']?`, so `is_decline` returns
  False at the second-regex gate (`classifier.py:91-92`); with `reviews: []` and no Augment
  review, `classify` falls through to `STATE_POLLING` (`classifier.py:131-133`). Asserted
  `is_decline == False` and `classify == "polling"` are both what the code produces.
- **`test_ec23` (stale pre-watermark ignored)** — confirmed. `createdAt`
  `2026-06-12T08:00:00Z` vs `watermark` `2026-06-12T09:30:00Z`: at `classifier.py:93-96`,
  `created > watermark` is lexicographically False (verified: `'…08:00:00Z' > '…09:30:00Z'`
  → False on fixed-width Zulu strings), so `not (created > watermark)` is True → returns
  False (stale, ignored). With `watermark=None` the watermark block is skipped and
  `is_decline` returns True; `classify` (default `watermark=None`) returns `"declined"`
  (`classifier.py:127-129`). Both asserted halves trace to real behavior.

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | MINOR (doc-drift, out-of-edit-scope) | `detection.py:3-4`, `:191`, `:197` | `poll_augment_review` docstring enumerates the return domain as only `"polling"` / `"clean"` / `"findings"` and never mentions `"declined"`. Post-V1.1 it delegates to `classify` with `watermark` defaulting to `None`, so a decline payload now legitimately returns `"declined"`. The docstring is a stale (now-incorrect) claim about the function's return surface. NOT a broken edit — runtime behavior is correct; the assertion in the prose is unsupported. | Update the three docstring sites to include `"declined"` in the enumerated return domain. |
| 2 | INFO (anchor map is a point-in-time snapshot; explicitly self-described as drifting) | `anchor-map.md:10` vs `models.py:20` | Anchor map's "Grep Match Text" for the EventType docstring still reads `… EXACTLY 33 members.`; current source reads `EXACTLY 37 members` (the 33→37 edit landed). The map's match-text column is stale. The map header (`anchor-map.md:1-5`) pre-declares that line numbers will drift and must be re-grepped, but the *match-text* column drifting is worth flagging for any later phase that diffs against it. Outside the classifier/detection lens; no edit in scope depends on it. | None required for Phase 3. Re-grep anchor map before any phase that consumes the EventType/INV-001 rows. |

No CRITICAL or IMPORTANT issues found in the classifier/detection/test surface. The
adversarial hunt for ≥5 stale-anchor / non-existent-symbol / fabricated-expectation defects
turned up **zero** in the in-scope edit surface: every symbol exists at its current
location, every test expectation reproduces from real code, and the only stale claims are a
docstring return-domain omission (Issue 1) and a snapshot match-text in the anchor map
(Issue 2) — neither is a broken Phase 3 edit.

---

## Adversarial probes that came back CLEAN (negative evidence)

- `is_decline` is module-scope, not a nested/instance method → `classify`'s call resolves.
- Contract fixture (`test_detection_contract.py:34-41`) does NOT set decline regexes; relies
  on dataclass baked defaults (`detection.py:78-88`) — verified those defaults are the ones
  the regex trace used, so the green tests are not masking a missing override.
- Fixture login `augment-code[bot]` == test `AUGMENT` constant → author gate
  (`classifier.py:82`) does not silently drop all fixtures to False.
- `from_yaml` wires all three new fields with the same baked defaults (`detection.py:105-115`)
  → a YAML-loaded contract behaves identically to the directly-constructed test fixture.
- 14 test fns / 14 passed / 0 skipped → no fabricated expectation hidden behind a skip/xfail.

---

## Confidence

**Confidence:** "Verified: 3/3 required checks | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%"
**Tool engagement:** "Read: 5 | Grep: 6 | Glob: 0 | Bash: 6"

Every required check is backed by cited tool output: full Read of all four target files,
grep of every symbol's definition/usage, regex execution against real fixture bodies, a
lexicographic-comparison check for the watermark, and a live test run (14 passed).

---

## QA Complete

VERDICT: PASS
