# Troubleshoot Report — Issue 5: Files-that-MUST-NOT-change conflicting trigger rules

**Target**: auggie review #3290499069 on PR #73
**Tier reached**: 1
**Confidence**: 0.95
**Status**: success
**Severity**: LOW

## Root cause

The `## Files that MUST NOT change` subsection has THREE rule statements in `refs/report-template.md` that name different triggers:

1. **Line 70** (inline directive inside the literal template block): `**Files that MUST NOT change** (REQUIRED when 'Test is wrong: true' in the header; OMIT this subsection otherwise):` — narrow trigger, *omits* the behavior-documented case explicitly.
2. **Line 164** (prose under "When `test_is_wrong=true`:"): `An explicit '## Files that MUST NOT change' subsection MUST appear under Proposed Fix...` — narrow trigger.
3. **Line 185** (prose under "Behavior-is-documented" rendering rules): `A '## Files that MUST NOT change' subsection MUST appear listing every code file...` — independent trigger that directly contradicts line 70's "OMIT … otherwise" when `behavior_is_documented=true`.

Intent evidence (lines 167 and 186 both invoke identical asymmetric-cost rationale) confirms the rules are complementary, not designed to differ.

## Proposed Fix

**Edit 1 — `src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md:70`** (inline template directive)

Old:
> `**Files that MUST NOT change** (REQUIRED when \`Test is wrong: true\` in the header; OMIT this subsection otherwise):`

New:
> `**Files that MUST NOT change** (REQUIRED when \`Test is wrong: true\` OR \`Behavior is documented: true\` in the header; OMIT this subsection otherwise):`

**Edit 2 — `src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md:164`** (test_is_wrong=true rendering bullet)

Old:
> - An explicit **`## Files that MUST NOT change`** subsection MUST appear under Proposed Fix, listing every production-code file a careless remediation might touch.

New:
> - An explicit **`## Files that MUST NOT change`** subsection MUST appear under Proposed Fix, listing every production-code file a careless remediation might touch. (The same subsection is also required when `behavior_is_documented=true` — see the Behavior-is-documented rule below. Trigger union: `test_is_wrong=true OR behavior_is_documented=true`.)

**Edit 3 — `src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md:185`** (behavior_is_documented=true rendering bullet — symmetry tightening)

Old:
> - A `## Files that MUST NOT change` subsection MUST appear listing every code file a careless remediation might touch.

New:
> - A `## Files that MUST NOT change` subsection MUST appear listing every code file a careless remediation might touch. (Same subsection required when `test_is_wrong=true`; trigger union: `test_is_wrong=true OR behavior_is_documented=true`.)

## Files that MUST NOT change

None — single-file fix.

## Risk + Rollback

Very low — three prose edits to a template, no executable code touched. Rollback = `git revert`.
