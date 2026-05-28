# Audit Test Pin Updates — Phase 4 Regression Resolution

**Task:** TASK-RF-20260523-234320-markdownlint-remediation
**Date:** 2026-05-24
**Resolution path authorized by user:** "Update the 5 audit-test pins"
**Scope:** Update content-pinned audit tests to reflect post-remediation
state of `src/superclaude/agents/rf-qa.md` and
`src/superclaude/agents/rf-qa-qualitative.md` after the authorized
markdownlint MD013 reflow.

## Summary

The markdownlint MD013 remediation reflowed long prose lines in the two
agent files (`rf-qa.md`, `rf-qa-qualitative.md`). The semantic content
is unchanged, but byte sequences shifted — line breaks now appear in
the middle of phrases the audit tests pinned verbatim, and the SHA-256
of the Critical Rules block changed. The five failures were:

1. `test_dnsp_twice_exhaust.py::TestWrapperContractTextGuards::test_twice_exhaust_trigger_named_at_every_agent_site` — phrase split across newline in `rf-qa.md` and `rf-qa-qualitative.md`.
2. `test_nfr_conv_6_self_contained.py::TestQDm1SchemaCrossCheck::test_rf_qa_schema_matches_expected` — TB-Add-1 rule body reflowed; regex no longer matches across the wrap.
3. `test_self_audit_inv_019.py::TestCrossReferenceWiring::test_critical_rule_11_wired` — "Your Self-Audit MUST list" split across newline in `rf-qa-qualitative.md`.
4. `test_severity_floor_unweakened.py::TestCriticalRulesBlockHash::test_block_hash_matches_baseline_source` — SHA-256 of the Critical Rules block changed.
5. `test_severity_floor_unweakened.py::TestCriticalRulesBlockHash::test_block_hash_matches_baseline_mirror` — Same SHA shift, mirror file (`.claude/agents/rf-qa-qualitative.md`).

The agent file edits remain AUTHORIZED — only the tests' literal
expected values changed. No agent file was modified by this work.

## Files Modified (4 test files)

| # | File | Change Type | Specific Change |
|---|------|-------------|-----------------|
| 1 | `tests/audit/test_dnsp_twice_exhaust.py` | Test logic — whitespace normalization | Normalize `txt` via `" ".join(txt.split())` before substring check (preserves content pin, drops line-wrap byte pin). |
| 2 | `tests/audit/test_nfr_conv_6_self_contained.py` | Test logic — whitespace normalization | In `_rf_qa_field_names`: normalize `text` via `" ".join(text.split())` before regex search. |
| 3 | `tests/audit/test_self_audit_inv_019.py` | Test logic — whitespace normalization | Normalize `src_text` via `" ".join(src_text.split())` before substring check. |
| 4 | `tests/audit/test_severity_floor_unweakened.py` | Constant value | `BASELINE_BLOCK_SHA` updated from `fd7f2e457bf63ce0045ec5d7014e9af67c1b46892f49b090334be17bbd2fff0f` → `cc57869c5580b32d9c38a9a64089820a9ea92e4103c8eb68d5b5ff041e5de06b`. Docstring SHA reference also updated. Inline comment cites the authorized remediation task. |

### Notes on the chosen pattern

For tests 1-3, the user's preferred fix was "normalize whitespace in the
test reader over changing the expected phrase". Each fix collapses all
whitespace runs to single spaces at the assertion site (`" ".join(txt.split())`),
so a phrase like `"fails after the single retry AND exhausts its escalation ladder"`
matches whether the source file contains it on one line or wrapped across
two. This preserves the test's intent (the phrase must exist in the agent
file) without re-pinning to a specific line-wrap.

For tests 4-5, only the byte-exact SHA could be updated — the test's
purpose IS to detect byte drift in the Critical Rules block. The new
SHA was computed using the same extraction logic (`_critical_rules_block`)
the test uses, run against the post-remediation source file. An inline
comment ties the change to the authorized task ID for future auditors.

### SHA-256 computation (test 4/5)

```
python3 -c "
import hashlib, re
from pathlib import Path
path = Path('src/superclaude/agents/rf-qa-qualitative.md')
lines = path.read_text(encoding='utf-8').splitlines(keepends=True)
header_line = -1; rule_11_line = -1
for idx, line in enumerate(lines, start=1):
    if header_line == -1 and line.strip() == '## Critical Rules':
        header_line = idx; continue
    if header_line != -1 and re.match(r'\s*11\.\s+\*\*', line):
        rule_11_line = idx
block_text = ''.join(lines[header_line - 1 : rule_11_line])
print(hashlib.sha256(block_text.encode('utf-8')).hexdigest())
"
# → cc57869c5580b32d9c38a9a64089820a9ea92e4103c8eb68d5b5ff041e5de06b
```

`src/` and `.claude/` mirror are byte-identical (`diff` confirms SYNC_OK),
so the same SHA applies to both `test_block_hash_matches_baseline_source`
and `test_block_hash_matches_baseline_mirror`.

## Verification

Final run of the 5 originally failing tests:

```
uv run pytest \
  tests/audit/test_dnsp_twice_exhaust.py::TestWrapperContractTextGuards::test_twice_exhaust_trigger_named_at_every_agent_site \
  tests/audit/test_nfr_conv_6_self_contained.py::TestQDm1SchemaCrossCheck::test_rf_qa_schema_matches_expected \
  tests/audit/test_self_audit_inv_019.py::TestCrossReferenceWiring::test_critical_rule_11_wired \
  tests/audit/test_severity_floor_unweakened.py::TestCriticalRulesBlockHash::test_block_hash_matches_baseline_source \
  tests/audit/test_severity_floor_unweakened.py::TestCriticalRulesBlockHash::test_block_hash_matches_baseline_mirror \
  -v

============================== 5 passed in 0.03s ===============================
```

**All 5 in-scope failures now pass.**

## Out-of-Scope Observations

Running the broader test files surfaced 4 pre-existing failures in
`test_dnsp_twice_exhaust.py::TestWrapperContractTextGuards` related to
`rf-analyst.md` (missing tokens: `DM-003`, `7-field DM-003 contract`,
the five DM-003 rejection symbols, and the `gap-fill-round-N`
vocabulary). These were NOT in the 5-test scope authorized by the user
and were NOT caused by this work — they reflect prior reductions to
`rf-analyst.md` content. Flagged here for visibility; remediation is
not part of this task.

## Constraints Honored

- Edit tool only — no sed/awk/Python helper used for file mutations
  (Python was used once inline for SHA-256 calculation, which is a
  read-only computation, not a file mutation).
- Single-line Bash commands only.
- Test logic preserved where possible (whitespace normalization rather
  than re-pinning to specific wrap); only the SHA constant was changed
  byte-for-byte, which is unavoidable given that test's purpose.
- No agent files modified.
