# Troubleshoot Report — Issue 2: behavior_is_documented vs test_is_wrong priority mis-routes Case B

**Target**: auggie review #3290499063 on PR #73
**Tier reached**: 1
**Confidence**: 0.93
**Status**: success

## Root cause

The mutual-exclusion clause between `behavior_is_documented` and `test_is_wrong` was authored as a binary tiebreaker ("spec/docs change takes priority"), but it conflates two logically distinct cases:

- **Case A**: observed behavior matches docs, test passes, user expectation diverges → docs change (current rule handles correctly)
- **Case B**: test asserts an invariant the docs explicitly contradict while production code already matches the docs → test change required, but current binary rule mis-routes to docs change
- **Case C**: code violates docs → both flags false, normal code remediation

## Proposed Fix

**Edit 1 — `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:69`** (derivation rule mutual-exclusion clause)

Replace the final sentence "Mutually exclusive with `test_is_wrong=true`: if both would be set, the spec/docs change takes priority over the test change since the test is downstream of the documented contract." with:

> Mutually exclusive with `test_is_wrong=true` by construction (not by tiebreaker), via this 3-case decomposition:
>
> - **Case A** (user expectation diverges): observed behavior matches docs AND failing artifact is NOT a test → `behavior_is_documented=true`, `test_is_wrong=false`. Remediate via spec change or stakeholder discussion.
> - **Case B** (test contradicts docs+code consensus): `consistency_with_docs=aligned` AND failing artifact IS a test → `test_is_wrong=true`, `behavior_is_documented=false`. The docs are not the bug; remediate by updating the test to match the docs.
> - **Case C** (code violates docs): `consistency_with_docs=conflicts` → both flags false; normal code remediation.

**Edit 2 — `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:51`** (Output Contract `behavior_is_documented` row, append one clause)

After "Asymmetric-cost flag — downstream automation MUST NOT auto-apply a code fix when this is `true`; the remediation target is the spec/docs file(s), or a stakeholder-level discussion." append:

> When the failing artifact is a test (Case B in the derivation rule), `test_is_wrong=true` is the correct flag and this flag stays false — the docs are not the bug.

**Edit 3 — `src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md:179`** (rendering rule mutual-exclusion line)

Replace "Mutually exclusive with `Test is wrong: true`. If both would be set, the spec/docs change takes priority since the test is downstream of the documented contract." with:

> Mutually exclusive with `Test is wrong: true` **by construction, not by tiebreaker**. The 3-case decomposition (see SKILL.md `behavior_is_documented` derivation rule): Case A (user expectation diverges) → `behavior_is_documented=true`; Case B (test contradicts docs+code consensus) → `test_is_wrong=true`; Case C (code violates docs) → both false. Only one can be true.

**Edit 4 — `src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md:18`** (header field HTML comment)

Replace the existing inline HTML comment with one that adds "AND the recommended remediation is a SPEC/DOCS change" to the trigger:

> `**Behavior is documented**: <true|false|n/a> <!-- See "Behavior-is-documented rule" below. When true, the observed behavior matches the documented contract AND the recommended remediation is a SPEC/DOCS change (not a test change — that's the test_is_wrong=true case). Mutually exclusive with `Test is wrong: true` by construction. `n/a` when --no-doc-discovery suppressed Wave 1.5. -->`

## Files that MUST NOT change

None — docs/spec-only fix.

## Risk + Rollback

Low. Pure prose tightening, no behavioral change to executable agents. Rollback = `git revert`.
