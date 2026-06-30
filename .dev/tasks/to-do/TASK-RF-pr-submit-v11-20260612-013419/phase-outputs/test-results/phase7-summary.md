# Phase 7 — full-suite + cross-cut summary

## pr_submit V1.1 surface: PASS
- `uv run pytest tests/pr_submit/ -v` = **175 passed**, 0 failed (Phase 1 baseline was 138 → +37 V1.1 tests across Phases 3-6, zero regressions).
- All V1.1 T-IDs present and green: T-1101..T-1125, T-PUSH-WITHOUT-REREVIEW-NO-TICK, T-AUGGIE-AT-MOST-ONCE, T-1105/T-1115, T-N50, the 9 unchanged INV-001 fence-post tests.

## Cross-cut `make test`: 19 failed, 10530 passed, 146 skipped, 1 error (210s)

**ALL 19 failures + 1 error are PRE-EXISTING and UNRELATED to pr_submit V1.1.** Evidence:

| Failing area | Count | Root cause (pre-existing) |
|---|---|---|
| `tests/cli/test_verify_sync_hooks.py` | (subset) | `make verify-sync` fails on `sc-recommend-protocol MISSING in src/` — the SAME pre-existing drift as the Phase 2 `make lint` failure. `sc-pr-submit-protocol` shows ✅ in the same output. |
| `tests/cli/test_install_hooks.py` | (subset) | same verify-sync / hook-install mechanism (sc-recommend-protocol drift) |
| `tests/sprint/test_rerun_tasks_e2e.py` | 2 | sprint CLI rerun — does NOT import/reference pr_submit |
| `tests/v3.3/test_zero_files_analyzed.py` | 1 error | analyzer — does NOT import/reference pr_submit |

Verification that these are NOT V1.1 regressions:
- `grep -lE 'pr_submit|pr-submit'` over all 4 failing test files → **NONE reference pr_submit**.
- `git status` → **none of the failing test files are modified by this task** (my diff is entirely
  `src/superclaude/pr_submit/*`, `src/superclaude/skills/sc-pr-submit-protocol/*`, `tests/pr_submit/*`).
- The verify-sync failure output explicitly names `sc-recommend-protocol` as the offender and shows
  `sc-pr-submit-protocol` ✅ (my skill is clean-synced).
- pr_submit changes are logically confined to the pr_submit package + its skill; the cli/sprint/v3.3
  subsystems do not depend on pr_submit, so they cannot regress from this work.

**Disposition:** the 19 pre-existing failures are OUT OF SCOPE for V1.1 pr_submit (the largest cluster is
the `sc-recommend-protocol` drift, a separate repo-state issue). The V1.1 deliverable — the full
`tests/pr_submit/` suite — is 175/175 green.
