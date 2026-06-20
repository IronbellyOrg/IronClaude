# QA Report — Report Validation (COMBINED STRUCTURAL lens)

**Topic:** PRD pipeline — remove `--file` local-path misuse (session-token crash fix)
**Date:** 2026-06-09
**Phase:** report-validation
**Fix cycle:** N/A
**Fix authorization:** false (REPORT ONLY)
**Repo:** /config/workspace/IronClaude

---

## Overall Verdict: PASS

All five spawn-prompt structural checks verified independently via grep / uv / Read,
zero-trust. No issue of any severity found. Two consolidation claims were found to
contain stale line numbers (call sites at 267/939, not the asserted ~247/~919), but
the underlying structural requirement — call sites *unchanged* — is verified TRUE,
so these are documentation imprecisions in upstream inputs, not defects in the edited
code. Documented below as MINOR notes; neither affects correctness, so PASS stands.

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Both `--file` emissions gone | PASS | `grep -rn '"--file"' src/superclaude/cli/prd/` → exit 1, 0 matches |
| 2a | `_build_file_args` removed, no dangling refs | PASS | `grep -rn '_build_file_args' src/superclaude/cli/prd/` → exit 1, 0 matches |
| 2b | `extra_args` wiring removed | PASS | `grep -rn 'extra_args' src/superclaude/cli/prd/` → exit 1, 0 matches |
| 2c | All 3 constants removed | PASS | `grep -rn '_PHASE_ALLOWED_REFS\|_FILE_SIZE_THRESHOLD\|_SPEC_FILE_STEPS' src/superclaude/cli/prd/` → exit 1, 0 matches |
| 2d | process.py imports cleanly | PASS | `uv run python -c "import superclaude.cli.prd.process"` → `IMPORT OK` |
| 3a | `_authoritative_specs_block` signature unchanged | PASS | prompts.py:120 `def _authoritative_specs_block(spec_paths: list[str] \| None) -> str:` |
| 3b | empty-input `return ""` contract preserved | PASS | prompts.py:134-135 `if not spec_paths: return ""` |
| 3c | substring `AUTHORITATIVE SPECIFICATIONS` survives | PASS | prompts.py:151 |
| 3d | substring `MUST Read each one IN FULL` survives | PASS | prompts.py:152 (`You MUST Read each one IN FULL before`) |
| 3e | `Path(p).is_file()` guard present + applied to every path | PASS | prompts.py:140 inside `for p in spec_paths:` loop (137-148); inline only on true branch, path-only fallback (`"- " + p`) on else; `Path` imported at prompts.py:17 |
| 4a | test file parses | PASS | `ast.parse(test_spec_flag.py)` → `PARSE OK` |
| 4b | zero `_build_file_args` refs in test | PASS | `grep -n '_build_file_args' tests/cli/prd/test_spec_flag.py` → exit 1, 0 matches |
| 4c | `--file` in test only as absence-assertions/comments | PASS | test_spec_flag.py:505,517 `assert "--file" not in cmd`; 462-463,481-483 comments only |
| 4d | `uv run pytest tests/cli/prd/ -q` GREEN | PASS | 160 passed in 0.51s (== baseline 160 claimed in consolidation); test_spec_flag.py alone: 30 passed |
| 5 | Both call sites unchanged | PASS | prompts.py single diff hunk `@@ -125,16 +125,36 @@` covers ONLY the function body (lines 125-160); call sites at prompts.py:267 and prompts.py:939 fall outside the hunk → unchanged |

## Summary
- Checks passed: 15 / 15
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (report-only mode)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | final-consolidation.md (implicit, via spec §3) | Spec/consolidation cite call sites at `prompts.py:247` and `:919`; actual locations are `:267` and `:939`. Stale line numbers in upstream prose. | None required for code; correct line refs in spec §3 if it is updated. Does NOT affect the verified "call sites unchanged" requirement. |
| 2 | MINOR | src/superclaude/cli/prd/process.py:11,98 | Two literal `--file` tokens remain in process.py — but BOTH are in docstrings explaining the *absence* of the flag (`"no \`\`--file\`\` flag"`), not emissions. The check-1 grep for the emission string `"--file"` (double-quoted, the argv form) correctly returns 0. | None. Documenting only so the reviewer is not surprised that `grep -i 'file'` surfaces these; they are correct descriptive docstrings, not regressions. |

## Adversarial findings (beyond the 5 mandated checks)
Per the COMBINED STRUCTURAL lens (template-conformance + internal-consistency +
evidence-quality), I checked beyond the spawn-prompt list and found NO defects:
- `_read_file` (prompts.py:42) + `_TRUNCATION_MARKER` (prompts.py:34) exist and are
  genuinely reused by the inlining branch (prompts.py:141) — not reinvented.
- `Path` is imported (prompts.py:17), so the runtime `Path(p).is_file()` guard cannot NameError.
- Empty-path elements are skipped (`if not p: continue`, prompts.py:138-139), so a
  stray `""` in SPECS cannot produce a bogus `Path("").is_file()` line.
- No dangling reference to any removed symbol anywhere in process.py (import succeeds + greps clean).
- Internal consistency: consolidation claims "160 passed == baseline 160" — independently reproduced (160 passed).

## Actions Taken
None (fix_authorization: false — report-only).

## Recommendations
- The two MINOR notes are upstream-prose imprecisions, not code defects. Optionally
  correct the call-site line numbers (267/939) in spec §3 if that spec is revised.
- Green light to proceed. The `make verify-sync` DRIFT noted in the consolidation
  is out of scope for this structural lens (skills surface, pre-existing/unrelated)
  and was not re-evaluated here.

## Confidence
**Verified:** 15/15 | **Unverifiable:** 0 | **Unchecked:** 0 | **Confidence:** 100.0%
**Tool engagement:** Read: 5 | Grep: 8 | Glob: 0 | Bash: 8 (greps + ast.parse + import + 2 pytest runs)

No web research performed (all claims are local source-truth; no external/URL/standards-bound claim in scope).

## QA Complete

VERDICT: PASS
