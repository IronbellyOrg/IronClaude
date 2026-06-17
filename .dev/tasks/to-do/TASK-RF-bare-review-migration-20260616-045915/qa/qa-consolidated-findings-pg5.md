# PG5 Consolidated Findings (WS-C legacy-retirement QA)

**Status: Complete**
**Initial verdict: FAIL (1 MINOR finding)** → **fix applied (1 cycle)** → **final: PASS**
**Date:** 2026-06-16

## Lens verdicts (6 agents, all `fix_authorization: false`, adversarial stance)

| # | lens | agent | verdict | report |
|---|------|-------|---------|--------|
| 1 | deletion-completeness | rf-qa | **PASS** | `qa/qa-structural-deletion-completeness-report.md` |
| 2 | no-dangling-reference | rf-qa | **PASS** (1 MINOR non-blocking obs) | `qa/qa-structural-no-dangling-reference-report.md` |
| 3 | reworked-test-integrity | rf-qa | **PASS** | `qa/qa-structural-reworked-test-integrity-report.md` |
| 4 | gate-authorization | rf-qa-qualitative | **PASS** | `qa/qa-content-gate-authorization-report.md` |
| 5 | post-deletion-coverage | rf-qa-qualitative | **PASS** | `qa/qa-content-post-deletion-coverage-report.md` |
| 6 | mirror-and-staging-hygiene | rf-qa-qualitative | **PASS** | `qa/qa-content-mirror-staging-hygiene-report.md` |

## Decisive evidence
- **Deletion-completeness (#1):** independent `find` over both trees for `t2_*`/`prompts.md`/`output-template.md` → zero matches; survivor `refs/templates/bare-review-output.md` sha256-identical in src + mirror; 5 legacy `src/` artifacts staged `D`.
- **No-dangling-reference (#2):** 33 `t2_*` + 2 deleted-ref-path matches all class (i) prose or class (ii) env-gated regen helper; the bare-review pre-commit hook calls `precommit_verify_bare_review_sync.sh` (sync check), NOT a deleted script; CI runs `pytest` but the regen helper `skipif`-skips (no workflow exports `SWARM_REGEN_GOLDEN`). **Zero class (iii).**
- **Reworked-test-integrity (#3):** 11 passed / 0 skipped with `t2_normalize.py` deleted; no `LEGACY_SCRIPT`/`importlib`/`spec_from_file` runtime refs (docstring-only); all 7 legacy-independent tests present.
- **Gate-authorization (#4):** strict mtime monotonicity proof — golden capture (20:21-21:56) → parity-green PG4 (22:04, 0 cycles) → AUTHORIZED (22:05) → deletion (22:21). Deletion-while-red refuted; re-ran parity with scripts absent (16 passed/0 skipped).
- **Post-deletion-coverage (#5):** re-ran post-deletion → gate 27 passed/0 skipped; full suite 2212 passed/27 skipped/0 failed; baseline delta fully accounted (−5 deleted legacy A/B tests uncollected; +1 env-gated regen skip).
- **Mirror-staging-hygiene (#6):** `make verify-sync` exit 0; zero `.claude/` staged; 5 clean `git rm` deletions on src side; mirror orphans pruned on disk (gitignored, no forced-add).

## MINOR finding (#2) — FIXED (1 fix cycle, serialized)
**Finding:** the *kept* survivor `src/superclaude/skills/sc-bare-review/refs/templates/bare-review-output.md` had stale provenance prose: (a) a parity-gate pointer (~L120-122) citing `test_recipe_bare_review.py` "byte-identity parity gate against the legacy `t2_normalize.py`" (that A/B gate was removed in Step 5.2), and (b) a Provenance bullet (~L128-129) calling `refs/output-template.md` the parent template "kept in place for the legacy ... pipeline under `scripts/`" (both deleted in WS-C). Prose-only, no executable consumer → could not trip the no-dangling gate, but is misleading doc-hygiene.

**Fix (applied by orchestrator — serialized single-writer, trivial 2-edit doc-prose change; spawning a dedicated fix agent for a 4-line doc edit was deemed wasteful):**
- Repointed the gate reference to `test_bare_review_parity.py` (permanent CLI-vs-frozen-golden gate) + `test_recipe_bare_review.py` (recipe registry/dispatcher/salvage coverage).
- Rewrote the Provenance bullet: canonical source is now `recipes/bare_review_v1.py`; the legacy `refs/output-template.md` + `scripts/` pipeline are noted as RETIRED in the M8/M9 migration (WS-C), with this swarm-aware template the surviving reference.

**Post-fix verification:** `make sync-dev && make verify-sync` → exit 0 ("All components in sync", sc-bare-review ✅); the only remaining `output-template.md` mention is the correct historical "were retired" note (not a stale "kept in place" claim). Skill-dir edit synced to mirror; no `.claude/` staged.

## Fix cycle
**1 fix cycle** (of max 3). Final consolidated verdict: **PASS**.
