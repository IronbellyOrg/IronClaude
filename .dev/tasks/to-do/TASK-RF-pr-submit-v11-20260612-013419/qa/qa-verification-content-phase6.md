# Phase 6 — Content Verification (CONTENT agent, I-verify, fix_authorization: false)

Adversarial verify-only pass over the 3 ACTIONABLE Phase 6 fixes. Scope: claims (a), (b), (c).
Modified nothing. Test run: `test_t1115_auggie_fallback_flag_parity` = **1 passed**.

## (a) T-1115 is now non-vacuous — PASS

**Row-startswith matching traced against real option-table rows in `auggie-review.md`:**

- `--depth` row = line 49: `` | `--depth` | `standard` | `quick` (auggie single-pass...) | ``
  After `.strip()` it starts with exactly `` | `--depth` `` → the generator
  `next(ln for ln in cmd.splitlines() if ln.strip().startswith("| `--depth`"))`
  selects THIS row (not a document-wide scan). `"quick" in depth_row` is scoped to
  this one row.
- `--auggie-model` row = line 55: `` | `--auggie-model` | (auggie default) | Override the model auggie uses (e.g., `--auggie-model claude-sonnet-4-6`) | ``
  Starts with `` | `--auggie-model` `` → selected by the second generator.
  `"claude-sonnet-4-6" in model_row` is scoped to this row, where the model appears
  as the `e.g.` example INSIDE the option cell.

**Would FAIL if `--depth quick` were not an accepted pairing:** if `quick` were dropped
from the `--depth` table row, `depth_row` would no longer contain `quick` →
`assert "quick" in depth_row` raises. A stray `quick` elsewhere in the document does
NOT rescue it, because `depth_row` is the matched row string only. ✓ Non-vacuous.

**Would FAIL if `claude-sonnet-4-6` were removed from the `--auggie-model` ROW (not a
stray mention):** `model_row` is bound via `startswith("| `--auggie-model`")` to line 55
exclusively. Removing the model from a non-table "document mention" would NOT break the
test — but removing it from the `--auggie-model` row WOULD. This is exactly the
"row, not stray mention" property requested. ✓ Non-vacuous and correctly targeted.

**Flag-to-row binding:** `for flag in ("--depth","--remediation-offer","--auggie-model"):
assert f"| `{flag}`" in cmd` pins each flag to a real option-table cell prefix
`` | `--flag` ``. Deleting any of these flags from the Options table makes the cell
prefix vanish → FAIL. (All three prefixes present: lines 49, 52, 55.) ✓

**Default-empty does not reintroduce vacuity:** `next(gen, "")` returns `""` when no
row matches. `"quick" in ""` / `"claude-sonnet-4-6" in ""` both evaluate False →
a MISSING row makes the test FAIL, never silently pass. ✓

**Byte-exact invocation pin retained:** `flag_string = "--depth quick --remediation-offer
--auggie-model claude-sonnet-4-6"` is still asserted `in fallback`, and the
`--no-post-pr` guard scopes to the actual `> Skill ... sc:auggie-review-protocol`
invocation lines (not the whole doc). No regression. ✓

## (b) F3 clamp wording consistent with ref/core (`effective_max_rounds`) — PASS

SKILL.md Wave 6b (L94) now reads:
`clamp the effective budget effective_max_rounds := min(effective_max_rounds, 1) (the
clamp_max_rounds helper, recorded once via the max_rounds_clamped event — INV-R3 monotone)`.

Cross-checked against ref + core (all agree on the same three names):
- `refs/auggie-fallback.md:44-45` — `effective_max_rounds := min(effective_max_rounds, 1)`,
  recorded via `max_rounds_clamped`.
- `refs/loop-guard.md:49,58` — identical formula + `max_rounds_clamped` event.
- `refs/state-machine.md:108` — `effective_max_rounds=1`.
- `pr_submit/fsm.py:145` — `clamp_max_rounds(...)` helper exists.
- `pr_submit/models.py:79,212` — `MAX_ROUNDS_CLAMPED = "max_rounds_clamped"`,
  `effective_max_rounds: int | None`.
- `pr_submit/run_log.py:160-192` — reduces the `max_rounds_clamped` event over
  `effective_max_rounds`.

The earlier naming drift (the fix-applied note's F3) is resolved: SKILL prose, refs, and
core all use `effective_max_rounds` + `max_rounds_clamped` + `clamp_max_rounds`. ✓

## (c) No new content vacuity introduced — PASS

The strengthened assertions are each scoped to a specifically-matched table row
(`depth_row`, `model_row`) or to a specific cell-prefix (`` | `--flag` ``). No loose
document-wide substring is used for the row-binding checks. The default-empty branch
fails-closed (not open). The original byte-exact `flag_string` and `--no-post-pr`
invocation-line guards are intact. No assertion was weakened to something
trivially-satisfiable. ✓

## Out-of-scope notes (verify-only, not fixed)
- F2/F4/F5/F6/F7 not in this agent's remit; not re-audited beyond the fix-applied summary.
- Pre-existing `sc-recommend-protocol` verify-sync drift is orthogonal and unverified here.

## Tool engagement
Read: 3 | Bash(grep/sed/pytest): 4 | Glob: 0. Each call mapped to a specific claim
(test run for the verdict; grep/sed traces for the row + clamp claims).

VERDICT: PASS
