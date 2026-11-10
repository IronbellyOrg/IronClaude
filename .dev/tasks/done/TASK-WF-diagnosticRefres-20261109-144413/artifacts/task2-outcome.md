# Task 2 outcome (selective install of sc-troubleshoot-protocol)

Date: 2026-11-10. Status: INSTALL DONE; T2.AC2 NOT MET (disclosed). The owner accepted the gap: Ruling recorded 2026-11-10 (owner reply "accept" at 2026-11-10T04:59Z, relayed by the coordinator). The verdict stays non-compliant (missing), not rounded up.

## What was done
- Selective install: `uv run superclaude install-skill sc-troubleshoot-protocol --target ~/.claude/skills --force`, exit 0 at 2026-11-10T00:18:27Z (artifacts/selective-install.json).
- Installed content equals the source; exactly SKILL.md, refs/diagnosability-audit.md and refs/doc-discovery.md changed in content (artifacts/compatibility-after.json).
- The 19 authorized mode tightenings only (owner decision A). At install time and at the review, `~/.claude/settings.json` (sha256 b39dd568...), setup-bmad and the 46 unrelated skills were unchanged (artifacts/compatibility-after.json:292,298).
- Later change, not caused by the install: `~/.claude/settings.json` was modified at 2026-11-10T03:27:13Z (about 3 hours after the install at 00:18:27Z). Its sha256 is now ae6823c3c6d67d5284f84d16c43af1aa336dfe04c50dda89cddb7b4b03298a30. Against `~/.claude/settings.json.bak`, the only differences are `model` (now claude-gw-gpt-6.1-sol[1m]), `effortLevel` (high to medium) and hook order. The `permissions` block and the set of hook commands are identical; nothing was loosened. The cause is outside this task (a model or effort switch in a Claude session); it was found by the archive-gate FINAL review and is disclosed here and in the worker report.
- Focused contract suite: 51 passed (artifacts/canonical-contract-after.log).
- Restricted worker smoke test: passed, self-reported tool use (artifacts/restricted-worker-smoke.json).
- Pre-install guard run: recorded after the fact (artifacts/guard-before-install.json). It was not saved at the time.

## What did NOT pass
- `make verify-sync` FAILED (exit non-zero): artifacts/verify-sync.log:22,223-224. The only drift is the uncommitted edit to src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py from the previous worker. Every troubleshoot component reported OK. The plan forbids `make sync-dev`, so it was not run.
- T2.AC2 (read-only sync verification passes) is therefore unmet. It is not described as passed anywhere.

## Template review
retries/T2/review-1.md: three blocking findings. F1.2 (guard record) and F1.3 (staging) fixed in the A2 pass. F1.1 is covered by the accepted Ruling.

## Owner decision on the verify-sync failure
After the plan archive and before the commit, run `make sync-dev` then `make verify-sync` and report the result. Never stage `.claude/` mirrors.
