# QA Report — Post-Completion Constraint-Compliance

**Topic:** sc-bare-review M8/M9 migration — standing-constraint compliance
**Date:** 2026-06-17
**Phase:** doc-qualitative (post-completion constraint-compliance lens; adversarial stance)
**Fix cycle:** N/A (fix_authorization: FALSE — report only)
**Working dir:** git worktree `/config/workspace/IronClaude/.claude/worktrees/mms-m8m9`

---

## Overall Verdict: PASS

The migration honored all five audited standing constraints. Adversarial assumption (≥10 violations) was NOT borne out — the SoT/sync/UV/transport discipline held. Note: the Axis column applies only to the task-qualitative phase; this is a constraint-compliance lens, so it is omitted.

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | No `.claude/` staged (diff --cached) | PASS | `git diff --cached --name-only \| grep '^\.claude/'` → empty (grep exit 1) |
| 1b | No `.claude/` in working status | PASS | `git status --short \| grep '\.claude/'` → empty (grep exit 1). Zero `.claude/` paths anywhere in status output |
| 2 | UV-only (script + tests) | PASS | `scripts/swarm_env_readiness.sh` prefers `uv run python -c` (L80); `python3/python` loop (L47) is portable *detection* of a missing interpreter, fallback (L85) only when UV absent — correct for a readiness preflight. `uv pip install` (L89) is advisory text. 3 new/modified test files: no `subprocess`/bare `python`/`pip install` |
| 3 | No Anthropic SDK in swarm transports | PASS | `grep -rniE 'anthropic\|ANTHROPIC' src/superclaude/cli/swarm/` → empty (exit 1). transports/ = `openai_compat.py` + `stub.py` only; both clean. OPS docs explicitly state NO Anthropic creds required (`env-readiness.md:7,97-100`) |
| 4 | verify-sync clean | PASS | `make verify-sync` exit 0 — all skills/agents/commands/hooks/templates ✅; "All components in sync" |
| 5 | Staging hygiene (D on src/ only) | PASS | `git diff --cached --name-status \| grep '^D'` → 5 deletions, ALL `src/superclaude/skills/sc-bare-review/...` (3 scripts + 2 refs). Zero `.claude/` deletions staged — mirror pruned via `make sync-dev`, not `git rm` |

## Summary
- Checks passed: 6 / 6
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (report-only)

## Issues Found
None.

## Adversarial probes that did NOT find violations
- `git add -f .claude/` smell: no `.claude/` path staged or modified anywhere in `git status --short`.
- Bare `python`/`pip` smell: the only `python3 python` occurrence is interpreter *detection*; the dep-check path is `uv run python -c` first.
- Anthropic-creds-as-swarm-requirement smell: `env-readiness.md` affirmatively documents the *absence* of `ANTHROPIC_API_KEY` and points at `openai_compat.py` as the sole transport env contract.
- `stub.py` confirmed present for the hermetic CI parity gate (`--transport stub`), matching Key Constraint "CI parity gate uses `--transport stub` … never `openai_compat`".

## Command Evidence (raw)
```
$ git diff --cached --name-only | grep '^\.claude/'        # (empty) exit 1
$ git status --short | grep '\.claude/'                      # (empty) exit 1
$ git diff --cached --name-status | grep '^D'
D  src/superclaude/skills/sc-bare-review/refs/output-template.md
D  src/superclaude/skills/sc-bare-review/refs/prompts.md
D  src/superclaude/skills/sc-bare-review/scripts/t2_dispatch.sh
D  src/superclaude/skills/sc-bare-review/scripts/t2_normalize.py
D  src/superclaude/skills/sc-bare-review/scripts/t2_preflight.sh
$ make verify-sync                                          # exit 0, "All components in sync."
$ grep -rniE 'anthropic|ANTHROPIC' src/superclaude/cli/swarm/   # (empty) exit 1
$ ls src/superclaude/cli/swarm/transports/                 # __init__.py openai_compat.py stub.py
```

## Self-Audit
1. **Factual claims verified against source/git:** 11 (3 git status/diff invocations, 1 make target, 3 greps over swarm src + docs + transports, 1 ls, 1 Read of the script L40-94, 2 test-file greps).
2. **Files read/inspected:** `scripts/swarm_env_readiness.sh` (L40-94), `docs/swarm/env-readiness.md` (grep), the 3 test files, swarm `transports/` dir listing, task file (Key Constraints L124-131); plus live git index/working-tree state.
3. **Why trust the PASS:** every constraint maps to a concrete command whose raw output is reproduced above. The two "near-miss" lines (script `python3 python` loop; doc Anthropic mentions) were read in context and confirmed to be *compliant by intent* (interpreter detection; explicit creds-NOT-required documentation), not violations.
4. **Web research:** none performed (all checks are local git/repo state). Tavily N/A.

## Confidence
Verified: 6/6 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
Tool engagement: Read: 2 (task file page, script) | Grep: 7 (within Bash) | Glob: 0 | Bash: 5

## Recommendations
- None blocking. The five standing constraints are satisfied; the worktree is safe to stage `src/`-side and proceed to commit/PR per CLAUDE.md (fork-target rule applies at PR time).

## QA Complete
