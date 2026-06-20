# QA Report — Structural Gate (No-Dangling-Reference Lens)

**Topic:** sc-bare-review M8/M9 migration — Phase Gate 5, no-dangling-reference lens
**Date:** 2026-06-16
**Phase:** report-validation (structural / reference-scan)
**Fix authorization:** FALSE (report-only)
**Input verdict under review:** `.dev/tasks/to-do/TASK-RF-bare-review-migration-20260616-045915/phase-outputs/plans/ws-c-reference-verdict.md`

---

## Overall Verdict: PASS

Zero class-(iii) live invocations of any deleted script exist. The legacy
script deletion (`t2_preflight.sh`, `t2_dispatch.sh`, `t2_normalize.py`) and
the deleted ref paths (`refs/prompts.md`, `refs/output-template.md`) strand no
live consumer in `src/`, `tests/`, `scripts/`, `Makefile`,
`.pre-commit-config.yaml`, `.github/`, or the post-WS-A SKILL.md. The input
verdict's PASS is independently confirmed AND extended (the input verdict did
not separately classify the two deleted-ref-path matches; both are class (i)).

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | All three scripts absent on disk | PASS | `ls scripts/` → empty dir; per-file existence check → all 3 ABSENT |
| 2 | Both deleted refs absent on disk | PASS | `refs/prompts.md` ABSENT, `refs/output-template.md` ABSENT; survivor `refs/templates/bare-review-output.md` EXISTS |
| 3 | git deletion is real (staged D) | PASS | `git status --porcelain` shows `D` for all 5 files (3 scripts + 2 refs) |
| 4 | `t2_*` grep across all scope dirs | PASS (all benign) | 33 matches, every one class (i) docstring/comment or class (ii) env-gated regen helper; quoted below |
| 5 | Deleted ref-path grep | PASS (all benign) | 2 matches: `bare-review-output.md:128` (provenance prose) + `test_bare_review_parity.py:493` (test docstring) — both class (i) |
| 6 | post-WS-A SKILL.md scan | PASS | `grep t2_*` and `grep refs/{prompts,output-template}.md` on `src/superclaude/skills/sc-bare-review/SKILL.md` → 0 matches |
| 7 | `.github/` CI | PASS | No `t2_`/bare-review script ref anywhere in `.github/`; CI runs bare `pytest` (test.yml:56,61,107) |
| 8 | CI does not trigger regen helper | PASS | `test_bare_review_golden_regen.py:122-123` module-level `skipif(SWARM_REGEN_GOLDEN != "1")`; no workflow sets that env var |
| 9 | Makefile | PASS | No `t2_`/bare-review reference in Makefile |
| 10 | `.pre-commit-config.yaml` | PASS | One bare-review hook (L119-124) but it invokes `scripts/precommit_verify_bare_review_sync.sh`, a sync-parity check — NOT a deleted script |
| 11 | pre-commit hook script body | PASS | `grep t2_* scripts/precommit_verify_bare_review_sync.sh` → no t2 invocation |
| 12 | `scripts/` dir | PASS | No `t2_` reference in any `scripts/` file |
| 13 | No CODE loads deleted ref paths | PASS | `grep --include=*.py --include=*.sh` for `output-template.md`/`prompts.md` → only a test docstring (prose); the `prd/prompts.py` hits are a different file (`agent-prompts.md`) |
| 14 | Recipe has no deleted-template dep | PASS | `bare_review_v1.py` builds body via in-Python `render_markdown` (L175,308); no external template-file load |

## Summary

- Checks passed: 14 / 14
- Checks failed: 0
- Class-(iii) live invocations found: 0
- Critical issues: 0

## Classification of every match

### Class (iii) — LIVE invocation (would force FAIL)
**NONE.** No CI workflow, Makefile target, pre-commit hook, `scripts/` file,
or non-env-gated executable code path runs any deleted script.

### Class (ii) — env-gated frozen-golden regen helper (legitimate)
- `tests/swarm/test_bare_review_golden_regen.py:4,12,18,64,152,154,264,278` —
  module-level `pytestmark = skipif(os.environ.get("SWARM_REGEN_GOLDEN") != "1")`
  (verified L122-123). The `LEGACY_SCRIPT` path executes ONLY under an explicit
  `SWARM_REGEN_GOLDEN=1` invocation and then `assert LEGACY_SCRIPT.exists()`
  fails with an actionable message (L264). CI never sets the env var → never runs.

### Class (i) — docstring / comment / historical-note / prose (acceptable)
- `src/superclaude/cli/swarm/recipes/bare_review_v1.py:4,89,105,217` — port-provenance docstrings/comments.
- `src/superclaude/cli/swarm/recipes/__init__.py:9` — comment.
- `src/superclaude/cli/swarm/commands.py:1392,1405,1417,1429,1628,1652,1665,1674,1847` — CLI help-text + comments citing legacy semantics as historical context; no invocation.
- `src/superclaude/skills/sc-bare-review/refs/templates/bare-review-output.md:121` — doc prose (kept survivor template).
- `src/superclaude/skills/sc-bare-review/refs/templates/bare-review-output.md:128` — **Provenance prose line referencing the now-deleted `refs/output-template.md`.** Pure prose in a doc's Provenance section; no executable consumer (verified: no `.py`/`.sh` loads this path). Stale-but-harmless documentation pointer, NOT a dangling live reference. (Not separately classified by the input verdict — flagged here as MINOR doc-hygiene, non-blocking.)
- `tests/swarm/test_recipe_bare_review.py:4,18,52` — provenance docstring/comment.
- `tests/swarm/test_e2e_user_guide.py:155,163,293` — parity comments.
- `tests/swarm/test_bare_review_parity.py:13,15,19,46` — docstring.
- `tests/swarm/test_bare_review_parity.py:493` — docstring referencing deleted `refs/prompts.md` (explains intentional non-byte-parity); prose only.
- `tests/swarm/fixtures/bare_review_v1/golden/README.md:5,8,28,75` — doc prose.

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | MINOR | `refs/templates/bare-review-output.md:128-129` | Provenance prose still points at deleted `refs/output-template.md` ("kept in place for the legacy bash/Python pipeline under `scripts/`") — both that ref and `scripts/` are now deleted, so the note is stale | Doc-hygiene only: update/remove the stale Provenance pointer. NON-BLOCKING for the no-dangling-reference gate (prose, no executable consumer). Not fixed here per fix_authorization: FALSE. |

## Actions Taken

None — report-only (fix_authorization: FALSE).

## Confidence

- **Confidence:** Verified: 14/14 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 3 | Grep: 0 (via Bash) | Glob: 0 | Bash: 5
  (All grep/ls/git executed via Bash; each call mapped to a specific check. No web research performed — all claims are local/source-truth, so Tavily was not engaged.)

## Adversarial self-audit

The adversarial premise ("assume a live invocation still exists somewhere")
was tested by: (a) grepping the deleted-script names across all scope dirs AND
CI/Make/config/shell file-type globs repo-wide; (b) reading the one bare-review
pre-commit hook to confirm it calls a sync-parity script, not a deleted one;
(c) confirming CI's `pytest` invocations cannot reach the regen helper because
it is module-`skipif`-gated and no workflow exports `SWARM_REGEN_GOLDEN`; (d)
grepping for any `.py`/`.sh` that loads the deleted ref PATHS (none — the only
hits are a different file `agent-prompts.md` and a test docstring). The single
residual is a stale doc-prose pointer (MINOR), which by definition cannot RUN a
deleted script. I can cite specific tool output for every PASS row.

## QA Complete
