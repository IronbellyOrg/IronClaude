# QA Report — Task Integrity (Phase 3 / F-2)

**Task:** TASK-RF-20260603-031100 — FR-6 `onboarding_status_source` enum rename
**Date:** 2026-06-03
**Phase:** task-integrity (F-2 gate)
**Fix cycle:** 1 (1 issue found and fixed in-place)
**Fix authorization:** true

---

## Overall Verdict: PASS (after in-place fix)

A zero-trust adversarial pass found **one stray `activation_message` token** that the rename
missed — in the `serena-wave0-config` case's own `input/diff.patch` (a site NOT in the named
3-site scope, but inside the same case directory and contradicting that case's own
`expected.yaml`). It was fixed in-place. After the fix, all criteria pass cleanly.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| a1 | SKILL.md (src) FR-6 step 3 reads `activation_msg \| list_memories_proxy \| unknown`, `list_memories_proxy` unchanged | PASS | Read src SKILL.md:230 — `recording \`onboarding_status_source\` (\`activation_msg\` \| \`list_memories_proxy\` \| \`unknown\`)`. `.claude/` mirror:230 matches (grep). |
| a2 | expected.yaml:20 asserted value AND inline enum comment | PASS | Read expected.yaml:20 — `onboarding_status_source: activation_msg` + comment `# {activation_msg, list_memories_proxy, unknown}`. |
| a3 | evals.json ~527 assertion `text` parenthetical | PASS | Read + `sed -n 527p` — `(activation_msg \| list_memories_proxy \| unknown)`. |
| b1 | No stray `activation_message` at the 3 named sites | PASS | grep `activation_message` returned NONE at all 3 sites. |
| b2 | No enum-position `none` token at the 3 sites | PASS | grep `onboarding_status_source.*\bnone\b` and `activation_msg.*\bnone\b` → NONE. |
| b3 | Spec gold standard alignment (04-spec:239) | PASS | `sed -n 239p` 04-spec-low-complexity.md = `activation_msg \| list_memories_proxy \| unknown` — all 3 sites match verbatim. |
| b4 | **Repo-wide sweep for residual `activation_message`** | **FIXED** | grep -rn found `serena-wave0-config/input/diff.patch:11` carrying stale `activation_message`. Fixed → `activation_msg`. Re-grep repo-wide = NONE clean. |
| c1 | verify-sync PASSED | PASS | `make verify-sync` exit 0, "✅ All components in sync." (matches verify-f2-summary.md). |
| c2 | markdownlint new-violation delta 0 | PASS (relied + summary) | verify-f2-summary.md: 136 current = 136 baseline, delta 0. Edit was to a non-markdown `.patch` fixture comment — cannot introduce MD violations in SKILL.md. |
| c3 | evals.json valid JSON | PASS | `python -c json.load(...)` → JSON_VALID. |
| d1 | corrected-form guards still 0 | PASS | `grep -c check_onboarding_performed` SKILL.md = 0; `grep -c find_referencing_code_snippets` SKILL.md = 0. |
| d2 | `onboarding_status ∈ {bootstrapped, not_bootstrapped, unknown}` preserved | PASS | SKILL.md:230 — `\`onboarding_status\` ∈ \`{bootstrapped, not_bootstrapped, unknown}\``. |
| d3 | fixture `onboarding_status: bootstrapped` + FR-6.4 comment preserved | PASS | expected.yaml:19 `onboarding_status: bootstrapped`; :21 FR-6.4 comment intact. |
| d4 | evals.json assertion type/target/pattern unchanged (only `text`) | PASS | onboarding_status_source assertion = type `regex_present`, target `with_skill/outputs/audit.log`, pattern `onboarding_status_source` — all structurally intact; git diff shows the whole eval block is net-new additions carrying the corrected enum form (no pre-existing assertion was mutated to a wrong form). |
| d5 | no `.claude/` staged | PASS | `git diff --cached --name-only \| grep ^.claude/` → empty, before and after fix. |
| d6 | no unrelated `none` occurrence changed in SKILL.md | PASS | enum-`none` grep NONE; SKILL.md src diff shows only FR-6/V3-Serena additions, no deletion of an existing `none` enum token. |

## Summary

- Checks passed: 17 / 17 (after fix)
- Checks failed: 0 (1 was FIXED in-place during this pass)
- Critical issues: 0
- Issues fixed in-place: 1

## Issues Found

| # | Severity | Location | Issue | Fix Applied |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | `.dev/eval-workspaces/sc-reflect/cases/serena-wave0-config/input/diff.patch:11` | Stale pre-rename token: comment read `onboarding_status_source = activation_message`, contradicting this same case's `expected.yaml:20` (`activation_msg`) and the spec gold standard. A stray `activation_message` the FR-6 rename missed. | Edited to `onboarding_status_source = activation_msg`. Re-grep repo-wide confirms ZERO `activation_message` remain. Fixture comment only (not a graded assertion); no sync-dev needed (not under `src/`); JSON/verify-sync unaffected. |

## Actions Taken

- Fixed stale `activation_message` → `activation_msg` in `serena-wave0-config/input/diff.patch:11`.
- Verified fix: `sed -n 11p` shows corrected token; repo-wide `grep -rn activation_message` over
  reflect skill dir + eval-workspaces + spec dir returns NONE.
- Confirmed `.claude/` not staged post-edit; confirmed edit target was an eval fixture (not `src/`),
  so `make sync-dev` was not required.

## Confidence Gate

- **Confidence:** Verified: 17/17 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 5 | Grep: ~14 (across Bash grep calls) | Glob: 0 | Bash: 5 | Edit: 1
- markdownlint delta (c2) — the numeric delta was relied on from verify-f2-summary.md rather than
  re-run; justification: my only edit was to a non-markdown `.patch` comment, which cannot affect
  SKILL.md MD-rule counts. All other items independently tool-verified.

## QA Complete

VERDICT: PASS
