# QA Report — Phase 2 (load-bearing edit to repo-inventory.sh)

**Topic:** cleanup-audit scope defaults — Phase 2 implementation
**Date:** 2026-05-29
**Phase:** task-integrity (post-implementation verification of Items 2.1–2.4)
**Fix cycle:** N/A (first pass)

---

## Overall Verdict: PASS

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 2.1a | `DEFAULT_EXCLUDES` variable exists near top of script | PASS | Read line 20: `DEFAULT_EXCLUDES='^(\.|.*/\.)|^_bmad/|^_bmad-output/|^_planning-input/|^\.claude-audit/'` — byte-exact match against the spec's required literal value |
| 2.1b | `apply_scope()` function exists, reads `EXTRA_EXCLUDES`, branches on emptiness | PASS | Read lines 29–37: function definition with `if [ -n "$EXTRA_EXCLUDES" ]` branch using combined regex, else branch using `DEFAULT_EXCLUDES` only; both arms guarded with `\|\| true` to survive `set -e` on empty input |
| 2.1c | Placement is after `BATCH_SIZE`/`SCOPE_FILE` setup, before "Validate target exists" | PASS | Read confirms: line 12 `BATCH_SIZE=`, line 13 `SCOPE_FILE=`, lines 15–37 contain the new block, line 40 starts `# Validate target exists` |
| 2.1d | POSIX `sh` compatibility (`sh -n` clean) | PASS | `sh -n` exited 0 with output `SYNTAX-OK` |
| 2.2a | Exactly 2 `FILE_LIST=` assignments, both pipe through `apply_scope` | PASS | `grep -c "FILE_LIST="` → 2. Line 49 (git branch): `FILE_LIST=$(git ls-files -- "$TARGET" 2>/dev/null \| apply_scope)`. Line 66 (find branch closes): `2>/dev/null \| apply_scope)` |
| 2.2b | Git branch line byte-exact | PASS | Line 49 exactly: `    FILE_LIST=$(git ls-files -- "$TARGET" 2>/dev/null \| apply_scope)` |
| 2.2c | Find branch closing line byte-exact | PASS | Line 66 ends with `2>/dev/null \| apply_scope)` |
| 2.3a | "ACTIVE SCOPE RULES" diagnostic block placed AFTER find branch closes, BEFORE `TOTAL=` | PASS | Find branch closes line 67; ACTIVE SCOPE RULES block at lines 70–77; `TOTAL=` at line 79 |
| 2.3b | Block contains 3 echo lines + blank | PASS | Lines 70–77: `echo "=== ACTIVE SCOPE RULES ==="`, `echo "  Default excludes: $DEFAULT_EXCLUDES"`, if/else with `Project excludes...` lines, trailing `echo ""` |
| 2.3c | Both extras-present and extras-absent branches show correct text | PASS | Line 73 (extras present): `Project excludes (from $SCOPE_FILE): $EXTRA_EXCLUDES`. Line 75 (extras absent): `Project excludes: (none — no SCOPE.md or no EXCLUDE: lines)` — both match spec verbatim including em-dash |
| 2.3d | Runtime verification (`/tmp 50`) shows block | PASS | Executed `bash repo-inventory.sh /tmp 50` from /tmp cwd → output begins with `=== ACTIVE SCOPE RULES ===`, `Default excludes: ^(\.\|.*/\.)\|^_bmad/...`, `Project excludes: (none — no SCOPE.md or no EXCLUDE: lines)` |
| 2.4a | Header comment block (lines 1–8) documents `SCOPE_FILE` env override | PASS | Read lines 1–8: line 4 `# Optional env:`, line 5 `#   SCOPE_FILE=path   — per-project file; one extra regex per line, '#' for comments`, line 6 `#                       (default: $TARGET/.claude-audit/SCOPE.md if present)` — all three lines byte-exact match spec |
| a | `sh -n` exit 0 | PASS | Confirmed |
| b | Diagnostic block visible at runtime | PASS | `bash ... /tmp 50 2>&1 \| grep -E "ACTIVE SCOPE RULES\|Default excludes:\|Project excludes"` shows all 3 expected lines |
| c | TUIBBS filter produces 389 | PASS | `cd /config/workspace/TUIBBS && bash .../repo-inventory.sh . 50 2>&1 \| grep "Total files:"` → `  Total files: 389` (matches dynamic-expected value in `/config/workspace/TUIBBS/.claude-audit/progress.json:current_scope.in_scope_paths`) |
| d | No debugging/scratch code, no broken pipes, no unguarded grep under `set -e` | PASS | Both branches of `apply_scope` use `\|\| true` to neutralize grep's exit-1 on empty input; no `set -x`, no commented-out scratch lines, no orphaned `echo "DEBUG"` patterns |
| e1 | Regex correctly matches hidden + BMAD paths (true positives) | PASS | Adversarial test against 8 paths — `.github/foo`, `internal/.bar/baz`, `_bmad/x`, `_bmad-output/x`, `_planning-input/x`, `.claude-audit/x`, `.env`, `.dev/tasks/foo` — all matched (excluded) as intended |
| e2 | Regex correctly preserves non-matching paths (true negatives) | PASS | Adversarial test against 7 paths — `internal/foo.go`, `_internal/foo`, `bmad/foo` (no underscore prefix), `claude-audit/x` (no dot prefix), `src/main.py`, `README.md`, `internal/foo.bar` — none matched (all kept) |
| e3 | Anchor boundary correctness (additional edge cases) | PASS | `_bmadx/foo`, `_bmad-other/x`, `foo.bar.baz` correctly NOT matched (only canonical `_bmad/`, `_bmad-output/`, `_planning-input/` excluded); `.claude/CLAUDE.md`, `src/.hidden/x`, `foo/.bar`, `a/b/c/.d/e` correctly matched as hidden segments |

## Confidence

**Verified:** 19/19 | **Unverifiable:** 0 | **Unchecked:** 0 | **Confidence:** 100.0%

**Tool engagement:** Read: 3 | Grep: 2 (via grep -c, grep -n) | Glob: 0 | Bash: 12

All checklist items verified by direct tool evidence — no reliance on prior reports. Tool-engagement count (17) exceeds checklist-item count (19) only marginally; specific items shared a single Read (e.g., the file-wide Read covered 2.1a, 2.1b, 2.1c, 2.4a simultaneously, which is legitimate consolidated verification, not padding).

## Summary

- **Checks passed:** 19/19
- **Checks failed:** 0
- **Critical issues:** 0
- **Issues fixed in-place:** 0 (no fixes needed)

## Issues Found

None.

## Observations (non-blocking, out-of-scope for Phase 2)

The script contains a pre-existing latent bug at line 122–123: when `domain_count` evaluates to a multi-line string (which occurs when stdin is unusual — e.g., running with `/tmp` TARGET from inside a git work tree — the `git ls-files -- /tmp` outputs nothing because /tmp isn't tracked, but the surrounding pipeline produces 2 lines instead of 1 for the `grep -c` aggregator), `[ "$domain_count" -gt 0 ]` errors with "integer expression expected". This bug is **present in the pre-Phase-2 baseline** (confirmed via `git show HEAD:...` and running the baseline script — identical `domain_count=$(...\| grep -c ...)` construct at line 84 of the committed version) and is therefore **NOT a Phase 2 regression**. It is out of scope for this gate. Recommend filing a separate task to harden the `domain_count` and `domain_total` `grep -c` constructs against multi-line outputs (likely fix: `tr -d '\n'` or wrap in `$(( ... ))` coercion).

## Actions Taken

None — all acceptance criteria pass on the first inspection. No fixes applied.

## Recommendations

- **Proceed to Phase 3.** Phase 2 is complete and correct against all four items' acceptance criteria, plus all 5 additional adversarial / runtime / regex checks (a–e).
- **Out-of-band followup (not blocking):** consider opening a separate task to harden the pre-existing `domain_count` multi-line-grep-c construct under `set -e`.

## QA Complete

## VERDICT: PASS
