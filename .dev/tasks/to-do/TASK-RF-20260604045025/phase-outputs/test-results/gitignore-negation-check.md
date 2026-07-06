# .gitignore Negation Verification — Step 2.1

**Timestamp:** 2026-06-04 05:16
**Result:** PASS — all 6 target fixtures UN-IGNORED, negation appended after `*.log`, no unintended leak beyond the known broad-pattern side effect.

## Placement

- Blanket rule: `.gitignore:79` = `*.log`
- Negation appended AFTER `*.log` (lines 80-82):
  - `80` `# Canonical evidence-pack fixtures asserted by tests/audit/*CanonicalFixtureParity*.`
  - `81` `# The blanket *.log rule above otherwise leaves them untracked -> clean CI checkouts fail.`
  - `82` `!.dev/releases/**/artifacts/**/fixture-*.log`
- Confirmed via `git check-ignore -v`: the matching rule reported is `.gitignore:82:!.dev/releases/**/artifacts/**/fixture-*.log` (negation, not the blanket `*.log`) — proving it is placed after and takes precedence.

## Target fixtures (6) — `git check-ignore -q`, exit=1 = UN-IGNORED = PASS

| exit | path | status |
|------|------|--------|
| 1 | D-0056/fixture-F-5-5-5-halt-cycle-2.log | UN-IGNORED ✅ |
| 1 | D-0057/fixture-pass1-fail2-shrinking.log | UN-IGNORED ✅ |
| 1 | D-0057/fixture-pass1-fail2-non-shrinking.log | UN-IGNORED ✅ |
| 1 | D-0059/fixture-cross-cycle-dedup-shrinking.log | UN-IGNORED ✅ |
| 1 | D-0059/fixture-cross-cycle-dedup-non-shrink.log | UN-IGNORED ✅ |
| 1 | D-0060/fixture-slow-shrink-F-5-4.log | UN-IGNORED ✅ |

All paths under `.dev/releases/complete/task-builder-merge/artifacts/`.

## Non-fixture representative (no leak check)

- `results/phase-1-output.txt` → `git check-ignore -q` exit=1 (NOT ignored). The broad fixture negation did NOT newly un-ignore non-fixture artifacts; `results/phase-*-output.txt` is not separately ignored on this checkout. Acceptable.

## Scope-leak enumeration — ALL `fixture-*.log` under artifacts/ (12 total)

The broad `**/artifacts/**/fixture-*.log` pattern un-ignores ALL 12 fixtures on disk. This is the intentionally broad pattern's KNOWN, ACCEPTED side effect.

### 6 TARGETS (to be committed in Step 2.2 by explicit path):

- D-0056/fixture-F-5-5-5-halt-cycle-2.log
- D-0057/fixture-pass1-fail2-shrinking.log
- D-0057/fixture-pass1-fail2-non-shrinking.log
- D-0059/fixture-cross-cycle-dedup-shrinking.log
- D-0059/fixture-cross-cycle-dedup-non-shrink.log
- D-0060/fixture-slow-shrink-F-5-4.log

### 6 NON-TARGETS now UN-IGNORED (KNOWN side effect — MUST NOT be committed; will appear as untracked in `git status`, that is EXPECTED, not contamination):

- D-0030/fixture-2cycle.log
- D-0031/fixture-enum.log
- D-0032/fixture-missing-verdict.log
- D-0056/fixture-F-0-skip.log
- D-0056/fixture-regression-precedes-monotonicity.log
- D-0057/fixture-no-regression-loop-continues.log

## Decision

All acceptance conditions met: negation appended AFTER `*.log`, all 6 targets UN-IGNORED, non-targets recorded as known-untracked-not-to-commit. **Cleared to proceed to staging (Step 2.2), staging the 6 targets by explicit path only.**
