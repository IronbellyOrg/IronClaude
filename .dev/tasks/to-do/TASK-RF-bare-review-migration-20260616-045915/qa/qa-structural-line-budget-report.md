# QA Report — Structural Line-Budget & Script-Free Lens (sc-bare-review SKILL.md)

**Topic:** sc-bare-review M8/M9 migration — `<=80-line` / script-free SKILL.md invariant
**Date:** 2026-06-16
**Phase:** task-integrity (structural, line-budget-and-script-free lens)
**Fix cycle:** N/A
**Fix authorization:** false (REPORT ONLY)
**Stance:** ADVERSARIAL — assumed >=5 violations; verified independently, did not trust the disk-verdict file.

---

## Overall Verdict: PASS (on the spawn-mandated checks) — with one IMPORTANT out-of-lens finding

The three mandated checks (line count, `t2_*` grep, stale-orchestration grep) **all PASS** against
the SKILL.md *text*. The independently-measured line count is **79** (`<= 80` ✓).

However, an adversarial sweep of the surrounding skill directory surfaced a real contradiction that
the disk-verdict missed: the legacy `scripts/` directory **still exists on disk** with all three
retired scripts, while SKILL.md line 10 asserts "legacy bundled scripts retired." This is an
IMPORTANT documentation-vs-reality contradiction, not a line-budget failure. See Issues Found #1.

---

## Independently-Measured Line Count

```
$ wc -l src/superclaude/skills/sc-bare-review/SKILL.md
79 src/superclaude/skills/sc-bare-review/SKILL.md
```

**Measured: 79 lines. Required: <= 80. Result: PASS.** Mirror `.claude/skills/sc-bare-review/SKILL.md`
also measures 79 (src↔mirror parity holds for the SKILL.md file).

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | `wc -l SKILL.md` <= 80 | PASS | Measured 79 directly from file (command above). Matches disk-verdict's claim of 79. |
| 2 | `grep -nE 't2_preflight\|t2_dispatch\|t2_normalize\|scripts/t2_' SKILL.md` == 0 matches | PASS | Ran the exact pattern; grep EXIT=1 (zero matches). No `t2_*` script-invocation tokens in SKILL.md text. |
| 3 | No stale `SKILL_DIR` / `Wave A` / `Wave C` / `t2_` orchestration tokens | PASS | `grep -nE 'SKILL_DIR\|Wave A\|Wave C\|single-message\|t2_'` returned only line 43 (`single-message`). |
| 4 | Line-43 `single-message` hit is not a surviving orchestration directive | PASS | Context: "fans out the N reviewers internally (no manual **single-message** dispatch)". This is a *negation* describing the new CLI-owned behavior, not a residual manual-dispatch instruction. Correct. |
| 5 | Broad orchestration-remnant sweep (`scripts/`, `.sh`, `preflight`, `dispatch`, `normalize`, `Wave`, `legacy`) inside SKILL.md text | PASS | Remaining hits are all in the "thin caller over swarm" / "legacy bundled scripts retired" framing or env-contract prose — none re-introduce script orchestration into the skill body. |
| 6 | `--lens bare-review` swarm target actually exists (skill isn't pointing at a phantom CLI) | PASS | `src/superclaude/cli/swarm/recipes/bare_review_v1.py`, `recipes/__init__.py` ("bare-review-v1 ports t2_normalize.py"), and `commands.py` `--lens` shortcut all present. The thin-caller claim is backed by a real CLI surface. |
| 7 | SKILL.md meta-claim "legacy bundled scripts retired" (line 10) is true on disk | **FAIL** | Out of pure line-budget lens, but checked adversarially: `scripts/t2_preflight.sh` (219 L), `t2_dispatch.sh` (112 L), `t2_normalize.py` (316 L) **still present and git-tracked** under `src/superclaude/skills/sc-bare-review/scripts/`, plus a `.pyc`. Mirror has them too. "Retired" is contradicted by disk reality. |

---

## Summary
- Checks passed: 6 / 7
- Checks failed: 1 (out-of-lens but material)
- Mandated checks (line count, `t2_*` grep, stale-token grep): 3 / 3 PASS
- Critical issues: 0
- Important issues: 1
- Issues fixed in-place: 0 (REPORT ONLY)
- Tool engagement: Read: 2 | Grep: 0 | Glob: 0 | Bash: 6

## Confidence
Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100% for the structural lens.
(The line-budget + script-free invariant on the SKILL.md text is fully verified. The PASS verdict is
issued on the spawn-mandated scope; the IMPORTANT finding is flagged for the orchestrator.)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | `src/superclaude/skills/sc-bare-review/scripts/` + SKILL.md:10 | SKILL.md states "legacy bundled scripts retired" but `t2_preflight.sh`, `t2_dispatch.sh`, `t2_normalize.py` (+ `__pycache__/*.pyc`) are still present and git-tracked. The skill body is a clean thin caller, but the skill *package* still bundles the 647-line legacy script set the migration claimed to remove. | DECISION REQUIRED — not a blind delete. The scripts are **intentionally referenced as the frozen parity golden** by `tests/swarm/test_bare_review_parity.py` and `test_recipe_bare_review.py` (they `importlib`-load `t2_normalize.py` to assert byte-identity vs `BareReviewV1`). Options: (a) keep the scripts but **correct line 10** to say "legacy scripts retained only as the test-parity golden, no longer invoked by the skill"; or (b) relocate the golden under `tests/` fixtures and delete from the skill package, updating the test import paths. Do NOT simply delete — that breaks `test_bare_review_parity.py`. |
| 2 | MINOR (note) | `scripts/__pycache__/t2_normalize.cpython-313.pyc` | A compiled `.pyc` is shipped inside the skill package directory. Even if the `.py` golden stays, the `__pycache__` artifact should not be tracked/shipped. | Add to `.gitignore` / remove from the package if currently tracked. |

## Actions Taken
None — `fix_authorization: false`. All findings are report-only and handed to the orchestrator.

## Recommendations
- The spawn-mandated line-budget/script-free invariant on **SKILL.md** is satisfied (PASS, 79 lines, zero `t2_*` references). The disk-verdict's narrow claim is accurate **as far as it goes**.
- The disk-verdict over-claims by implying the rewrite fully "landed": it verified only the SKILL.md text, never the skill *package*. The "legacy bundled scripts retired" assertion in SKILL.md line 10 is **false on disk** — the scripts remain. Resolve via Issue #1 option (a) or (b) before treating the migration as complete.
- `refs/prompts.md`, `refs/output-template.md`, and `refs/templates/bare-review-output.md` still describe the `t2_preflight.sh`/`t2_normalize.py` harness as the live mechanism; if the skill is now a thin swarm caller, those refs are stale and should be reconciled too (out of this lens; flag for the content-lens QA pass).

## QA Complete
