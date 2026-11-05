# Troubleshoot Report

**Target**: PR #359 review round 2: block-bare-python.sh misses python3 after an escaped `[[`, after a process-substitution redirect, and inside backticks in `$(( ))`
**Type**: bug
**Tier reached**: 1
**Confidence**: 0.92
**Status**: success
**Escalation reason**: none
**Test is wrong**: false
**Behavior is documented**: false
**Doc context card**: .dev/troubleshoot/bug-pr359-round2-hook-findings-20261104153447/doc-context.md
**Duration**: 610
**Date**: 2026-11-04T15:44:38Z

---

## Summary

The hook's awk scanner loses track of the command word in three places, so three commands that run bare `python3` are allowed. It opens its `[[ ]]` test context even for a quoted or escaped `[[`, it treats a process substitution like a subshell command (clearing the parent's command position and keeping the redirect skip), and it ignores backticks inside arithmetic. The fix is one change set in the scanner, its plugin mirror and tests.

## Documentation Context

- **Relevant refs**: src/superclaude/hooks/scripts/block-bare-python.sh (header), CHANGELOG.md (#357 entry), .dev/tasks/done/TASK-WF-implementIronbel-20261104-130647/TASK-WF-implementIronbel-20261104-130647.md
- **Documented behavior**: the scanner handles process substitution, `$(( ))` arithmetic and `[[ ]]` tests, and honours backslash escapes when tracking quotes.
- **Restrictions honored**: exit 0/2 contract and fail open; awk only; 100 KB under 1 s; byte-identical mirror.
- **Restrictions overridden**: None
- **Card path**: .dev/troubleshoot/bug-pr359-round2-hook-findings-20261104153447/doc-context.md

## Diagnosability Context

**Verdict**: partial
**Complexity classification**: trivial
**Captured-bytes (failing run)**: n/a

The hook reports only a matched word, so a wrong allow leaves no trace. A read-only copy of the scanner that prints every chosen command word closed that gap. The partial verdict is a cap from Grep-only discovery.

(Full card: /home/coder/workspaces/worktrees/IronClaude/bare-python-hook-357/.dev/troubleshoot/bug-pr359-round2-hook-findings-20261104153447/diagnosability-context.md)
(Tasklist (informational): /home/coder/workspaces/worktrees/IronClaude/bare-python-hook-357/.dev/troubleshoot/bug-pr359-round2-hook-findings-20261104153447/diagnosability-tasklist.md)

## Diagnosis

**Root cause**: the awk scanner breaks three bash parsing rules (reserved words count only unquoted, process substitution is a word, arithmetic runs backtick substitutions), so it never reports `python3`.

**Cause class**: Logic error (incomplete grammar model in the parser)

**Detailed explanation**: A backslash is dropped without marking the word escaped (Evidence 1), so `\[\[` matches the test-opener check (Evidence 2) and the rest of the line is treated as test text. For `< <(printf "") python3`, the `<(` opens a subshell-type context while the redirect skip stays set (Evidence 3), and its `)` sets the parent's command position to done (Evidence 4), so `python3` is skipped. The arithmetic scanner has no backtick case (Evidence 5). In each case the scanner prints nothing and the hook allows the command (Evidence 6, 7).

## Evidence

1. `src/superclaude/hooks/scripts/block-bare-python.sh:153` — `if (c == "\\") { if (i == n) { i = n + 1; return }; i++; addc(o, substr(s, i, 1)); return }`
2. `src/superclaude/hooks/scripts/block-bare-python.sh:120` — `if (w == "[[") { tst[o] = 1; need[o] = 0; cmd[o] = w; return }`
3. `src/superclaude/hooks/scripts/block-bare-python.sh:196` — `if (nx == "(") { endword(o); i++; pushc("par"); return }`
4. `src/superclaude/hooks/scripts/block-bare-python.sh:96` — `if (skn[o]) { skn[o] = 0; return }` runs only when a word is open, so the skip set by the preceding `<` survives the `<(`; `src/superclaude/hooks/scripts/block-bare-python.sh:219` — `if (t == "dol" || t == "par" || t == "arr") { d--; if (t == "par" && iscmd(ct[d])) need[d] = 0; return }`
5. `src/superclaude/hooks/scripts/block-bare-python.sh:267` — `function arithchar(s, n, c) {` (handles `(`, `)` and `$(` only)
6. `src/superclaude/hooks/scripts/block-bare-python.sh:326` — `*) exit 0 ;;`
7. Command: `bash trace-probe.sh src/superclaude/hooks/scripts/block-bare-python.sh` → no command word for the escaped `[[` input, `cmdword=printf`, `cmdword=echo`, and `hook_exit=0` for all three (trace-probe.out)
8. Command: bash with a fake python3 on PATH → `FAKE-PY ran` for all three inputs and for `"[[" a ]]; python3 x` (tier1-observation.md)

## Proposed Fix

**Files to change**:
- `src/superclaude/hooks/scripts/block-bare-python.sh` — a per-word quoted flag (set by backslash and quotes) so reserved words, including `[[`, are recognized only unquoted; a `psub` context for `<(`/`>(` that clears the redirect skip on open and leaves the parent's command position on close; a backtick case in `arithchar`; header text.
- `plugins/superclaude/hooks/scripts/block-bare-python.sh` — byte-identical copy.

**Test to verify**:
- add BLOCKED and ALLOWED cases to `tests/hooks/test_block_bare_python.py`; existing `[[ ]]`, process-substitution and 100 KB cases stay green.

**Apply with**: applied by the caller sc-pr-submit-protocol in its fixing state.

## Risk + Rollback

- **Likelihood of regression**: medium in reserved-word and process-substitution handling
- **Test coverage of the changed code**: good after the new cases
- **Rollback**: revert the fix commit

## Follow-up tasks

None.

## Grounding Gaps

- MCP auggie was unavailable; Wave 1.5 and 1.6 used Grep/Glob/Read (Wave 1.6 degraded), capping the diagnosability verdict at partial.
- The quoted `"[["` variant was observed in bash only, not through the scanner trace.

## Next Steps

- D1 (core): observed this run, consistent; no pending rows.
- Tier 1, high confidence: the caller applies the fix and re-runs the three inputs (each must give `hook_exit=2`) and the test suite.

## Audit

- **Hypothesis cards**: .dev/troubleshoot/bug-pr359-round2-hook-findings-20261104153447/tier1-hypothesis.md
- **Audit log**: .dev/troubleshoot/bug-pr359-round2-hook-findings-20261104153447/audit.log

## Pipeline Hardening Closure

Pipeline hardening not applicable: the defect is in the scanner's word recognition after intact delivery; decision mapping, mirror and tests sit on the real boundary (boundary scan: .dev/troubleshoot/bug-pr359-round2-hook-findings-20261104153447/hc0-boundary-scan.md).
