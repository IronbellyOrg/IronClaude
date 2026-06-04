# QA Report — Task Integrity (Phase 4: F1 Remediation)

**Topic:** F1 — `.gitignore` `.claude/` dir-prune defeats file-level negations for the R3 lookup-cache exception
**Date:** 2026-06-03
**Phase:** task-integrity (Phase 4 remediation verification)
**Fix cycle:** N/A (first pass)
**Fix authorization:** true

---

## Overall Verdict: PASS

The F1 fix is correct and functionally effective. The `.claude/` directory-prune was replaced
with `.claude/*` (glob over direct children, no prune) in BOTH `.gitignore` and the defective
spec block, and the `.claude/cache/*` re-ignore chain is correctly ordered. I ran `git check-ignore`
myself (not `-v`, per instruction) for every required path; all exit codes match the contract.
The critical regression guard holds: the sync-dev mirrors remain ignored.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | `.gitignore` line 117 is `.claude/*` (not `.claude/`) | PASS | Read `.gitignore:117` = `.claude/*` |
| 2 | `.claude/cache/*` inserted AFTER `!.claude/cache/`, BEFORE per-file negations | PASS | `.gitignore`: L120 `!.claude/cache/` → L121 `.claude/cache/*` → L122 `!...lookup.yaml`. Correct order. |
| 3 | `!.claude/settings.json` preserved | PASS | `.gitignore:118` |
| 4 | Trailing `.claude/cache/sc-recommend-events.jsonl` re-ignore preserved | PASS | `.gitignore:127` |
| 5 | `git check-ignore` lookup.yaml → exit 1 (tracked) | PASS | Ran it: `lookup.yaml exit=1` |
| 6 | `git check-ignore` plugin.yaml → exit 1 (tracked) | PASS | Ran it: `plugin.yaml exit=1` |
| 7 | `git check-ignore` events.jsonl → exit 0 (still ignored) | PASS | Ran it: `events.jsonl exit=0` (printed path) |
| 8 | REGRESSION GUARD: `.claude/skills/sc-recommend/SKILL.md` → exit 0 (still ignored) | PASS | Ran it: `SKILL.md exit=0` (printed path) |
| 9 | REGRESSION GUARD: `.claude/commands/sc/recommend.md` → exit 0 (still ignored) | PASS | Ran it: `recommend.md exit=0` (printed path) |
| 10 | `.claude/settings.json` → exit 1 (still trackable) | PASS | Ran it: `settings.json exit=1` |
| 11 | Spec block (merged-requirements.md:87-104) uses corrected `.claude/*` + `.claude/cache/*` chain | PASS | Read L87-106: L93 `.claude/*`, L97 `!.claude/cache/`, L98 `.claude/cache/*`, L99-100 per-file negations, L105 events.jsonl re-ignore. Matches .gitignore. |
| 12 | Adversarial cross-check: real git sees cache yaml as un-ignored, not suppressed | PASS | `git check-ignore -v lookup.yaml` → matched rule `.gitignore:122:!.claude/cache/sc-recommend-lookup.yaml`; `git status` → `?? .claude/cache/`. The negation actually fires now. |

## Summary

- Checks passed: 12 / 12
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (no fixes required)

## Issues Found

None.

## Actions Taken

No fixes were required — the remediation was already correct and complete in both files.

## Adversarial Notes

Per the adversarial stance, I did not trust the change summary. Beyond the required plain
`git check-ignore` calls I added two independent cross-checks:

1. **`git check-ignore -v` on lookup.yaml** confirmed the matching rule is the *negation*
   `.gitignore:122:!.claude/cache/sc-recommend-lookup.yaml`. This proves the file is un-ignored
   by an explicit negation that *now actually takes effect* — the exact behavior the old
   `.claude/` dir-prune made impossible. (Git cannot re-include a file whose parent dir is pruned;
   the `.claude/*` glob keeps the dir traversable so negations apply.)
2. **`git status --porcelain --ignored .claude/cache/`** shows `?? .claude/cache/` (untracked,
   addable) rather than the cache being suppressed — the desired end state.

The regression guard (items 8–9) was the highest-risk surface: broadening `.claude/` → `.claude/*`
could have un-ignored the entire sync-dev mirror tree (`skills/`, `commands/`, `agents/`), which
CLAUDE.md forbids committing. It did NOT — the mirrors stay ignored because `.claude/*` matches the
`skills`/`commands`/`agents` directory entries directly and no negation re-includes them. Verified
by running check-ignore on two representative mirror files; both exit 0.

## Confidence Gate

- **Confidence:** Verified: 12/12 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 2 | Grep: 0 | Glob: 0 | Bash: 2
  (Bash calls were batched: one ran all 8 required check-ignore assertions, one ran the 2 adversarial
  cross-checks. Each check-ignore invocation maps 1:1 to a checklist item; the batching does not
  reduce per-item evidence — every required path was independently invoked.)
- No web research performed (no external claims in scope).

## Recommendations

Phase 4 (F1) remediation is verified correct. Green light to proceed. The lookup-cache and
plugin-cache YAML artifacts are now genuinely trackable, the telemetry JSONL stays ignored, the
sync-dev mirrors stay ignored, and `settings.json` stays trackable. The spec block in
`merged-requirements.md` now transcribes a working chain, so downstream implementers will not
re-introduce the dir-prune defect.

## QA Complete
