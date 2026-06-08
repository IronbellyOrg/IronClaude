# QA Report — task-qualitative (FINAL qualitative gate)

**Topic:** Remediation TASK-RF-20260603-031100 — UC-2 audit findings F-1/F-2/G-1/G-2 in sc-reflect-protocol
**Date:** 2026-06-03
**Phase:** task-qualitative
**Fix cycle:** N/A (first qualitative pass)
**Stance:** Adversarial / zero-trust. Each semantic judgment re-derived from source with my own tool engagement; the inherited structural PASS was relied on ONLY for facts it machine-verified, never substituted for semantic reasoning.

---

## Overall Verdict: PASS

All four fixes are not merely syntactically valid — they are **logically correct, complete, and internally coherent**. The F-1 predicate is the genuinely-correct encoding of the spec's intent (verified by exhaustive boundary-case walk, not by reproducing the one worked example). The three F-1 sites and the F-2 three (effectively four) sites tell a single coherent story with zero residual contradiction. The F-2 `unknown` rename is semantically aligned with both the §9.2 STATUS enum and FR-6.4. G-1's bump and G-2's `regex_present` swap are the appropriate calls, and the false-positive risk the spawn flagged is bounded and acceptable for these scaffolded evals.

---

## Items Reviewed

| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | F-1 predicate logical correctness (boundary walk) | none | PASS | SKILL.md:432 predicate `slug_count > 20 AND (slug_count − readonly_count) ≤ 20`. Walked 7 boundary cases (below). Fires iff read-only-dominated/total-unreachable; never on the bounded case. Genuinely-correct, not example-fit. |
| 2 | F-1 prose unambiguity for a future implementer | none | PASS | SKILL.md:432 parenthetical spells out the intent ("total exceeds the 20-entry budget but the deletable entries alone are within it, so read-only entries are what make the ≤20-total target unreachable"). Maps 1:1 to spec FR-8.6 (04-spec:280) + the C1 invariant prose (04-spec:271). |
| 3 | F-1 single coherent story across 3 sites | none | PASS | SKILL.md:432, expected.yaml:21 comment, evals.json:803 `text` all describe `slug_count > 20 AND deletable ≤ 20`. grep for inverted `>20` fire-condition across src/ + eval-workspaces = ZERO. The grading field (evals.json:799-804 `memory_retention_unbounded == true`) is unchanged — relabel only. |
| 4 | F-2 internal consistency (SOURCE vs STATUS enum) | none | PASS | SOURCE enum SKILL.md:230 `activation_msg \| list_memories_proxy \| unknown`; STATUS enum SKILL.md:230 + :684 (§9.2) `{bootstrapped, not_bootstrapped, unknown}`. The renamed `unknown` SOURCE no-signal token now shares its lexeme with the STATUS `unknown` and with FR-6.4's "absence of signal is not negative signal" (no `S_dev_density` down-weight, SKILL.md:231). Semantically coherent. |
| 5 | F-2 no residual old tokens at any site | none | PASS | grep `activation_message` across src/ + eval-workspaces = 0. Enum-position `none` gone (replaced by `unknown`). Matches spec FR-6.1 (04-spec:239) exactly. |
| 6 | G-1 contract_version appropriateness | none | PASS | report-template.md:14 `contract_version: 1.1.0`. The header is rendered as fenced YAML so downstream parsers (sprint TurnLedger, CI) lift it (template:11). A stale `1.0.0` would mis-declare the contract the template implements. `1.1.0` matches the §9.1 5-site bump (per inherited structural PASS). Bumping (vs leaving / arbitrary value) is the right call — it is the version-of-record consistency fix. |
| 7 | G-2 regex_present appropriateness vs grader limitation | none | PASS | grader.py:172-187 `check_yaml_list_contains` requires `isinstance(node, list)`; an indexed-scalar path (`...0.abstract_name_path`) resolves to `str` → always-False. grader.py:152-159 `check_regex_present` reads target text + `re.findall`. The swap restores a genuinely-grading assertion with no grader.py change. Appropriate minimal fix. |
| 8 | G-2 false-positive risk (PaymentHandler / fastapi.Depends) | none | PASS | Risk bounded — see Analysis below. Targets are runtime-generated `with_skill/outputs/contract.yaml` (NOT the static fixture); both evals are explicitly "Scaffold: assertions target a future run's with_skill/outputs/" (evals.json:577,696). `fastapi\.Depends` correctly escapes the dot. Acceptable for scaffolded presence-assertions. |
| 9 | Completeness — all in-scope sites touched | none | PASS | F-1: 3 sites (SKILL.md, expected.yaml, evals.json:803). F-2: 3 named + 1 swept (diff.patch:11, caught by PG-3) = 4. G-1: 1 site. G-2: 2 sites. No in-scope site missed. The out-of-scope FR-1.4 degrade-token gap is correctly recorded as a separate follow-up (not re-litigated here). |
| 10 | No collateral edits beyond the 4 findings | none | PASS | `git diff --stat` for report-template = exactly `2 +-` (single-line bump). SKILL.md/evals.json larger diff is the uncommitted PARENT task body (per inherited structural PASS — HEAD predates §6.3/§0.7), not this remediation. |

---

## F-1 Predicate Boundary-Case Walk (my own derivation)

Predicate fires `memory_retention_unbounded: true` iff `slug_count > 20 AND (slug_count − readonly_count) ≤ 20`. Let d = deletable = slug_count − readonly_count.

| total / readonly / deletable | `>20`? | `d ≤ 20`? | Fires? | Correct? (spec: fire iff read-only makes ≤20-total unreachable) |
|---|---|---|---|---|
| 25 / 24 / 1 | T | T (1) | **YES** | ✓ worked example — read-only dominates, total 25 unreachable w/o deleting read-only |
| 25 / 0 / 25 | T | F (25) | no | ✓ bounded — delete 5 deletables → 20; sweep resolves it |
| 21 / 1 / 20 | T | T (20) | **YES** | ✓ 20 deletables at budget; the 1 read-only pushes total to 21, genuinely unreachable |
| 21 / 0 / 21 | T | F (21) | no | ✓ delete 1 → 20, bounded |
| 20 / 19 / 1 | F | — | no | ✓ total already at target (20), nothing to flag |
| 41 / 21 / 20 | T | T (20) | **YES** | ✓ deletables at budget, 21 read-only make 41 unreachable |
| 41 / 0 / 41 | T | F (41) | no | ✓ delete 21 → 20, bounded |

The predicate fires **exactly** on the read-only-dominated/total-unreachable class and never on the bounded class. It is the genuinely-correct encoding of FR-8.6 + the C1 invariant (04-spec:271,280), not a predicate that merely happens to pass 25/24/1. The boundary `d = 20` (inclusive `≤`) is correct: 20 deletables is already the maximum kept by the "keep last 20 deletable" rule, so any read-only on top makes total > 20 with no further deletion possible.

---

## G-2 False-Positive Risk Analysis (spawn item 4 — answered)

**Could `PaymentHandler` / `fastapi\.Depends` match spuriously in a real contract.yaml?**

- The target is `with_skill/outputs/contract.yaml` — the **runtime-generated** contract the skill-under-test emits, NOT the static stub `expected.yaml` (grader does not read expected.yaml; it is a human doc per its own line 1-2). The contract.yaml does not exist statically; both evals are flagged "Scaffold: assertions target a future run's with_skill/outputs/" (evals.json:577 id-22, :696 id-24), so neither grades today.
- `regex_present` is a **presence** assertion (`re.findall` over MULTILINE|DOTALL). For id-24, `fastapi\.Depends` correctly escapes the literal dot (doubled backslash in JSON → single backslash in the compiled pattern → matches literal `fastapi.Depends`, not `fastapiXDepends`). For id-22, `PaymentHandler` is an unanchored substring.
- **Residual risk (acceptable, not a defect):** because both patterns are unanchored substrings against the *whole* contract.yaml, they assert "this symbol appears somewhere in the generated contract," not "it appears in the specific `missing_implementations[].abstract_name_path` / `third_party_api_grounding[].api_name` field." A contract.yaml that mentioned `PaymentHandler` in an unrelated section would still pass. This is a **strict-improvement over the always-False original** (which could never pass even on correct output) and is the documented minimal fix; the assertion `text` itself records the grader limitation and names the two heavier alternatives (top-level-scalar-list field_path; new scalar-capable grader type). For scaffolded presence-evals this is the appropriate altitude — it does not create a *false-PASS-on-broken-output* hazard for any realistic contract.yaml, because the symbol names (`PaymentHandler`, `fastapi.Depends`) are exactly the fixture's subject-under-test and would only appear if the find_implementations / search_deps grounding actually ran. Verdict: appropriate, with the limitation honestly disclosed in-band.

---

## Summary

- Checks passed: 10 / 10
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (none required)
- Axis lens status: `drift-axis-inactive` — no BUILD_REQUEST.GOAL verbatim was provided in the spawn prompt or reproduced in the task file's GOAL form, so AX-1 Drift was lens-disabled for this review. AX-2..AX-5 applied normally and surfaced nothing (all rows `none`).

## Issues Found

None.

## Actions Taken

No fixes applied — the remediation is qualitatively sound. fix_authorization was true; nothing required correction.

## Self-Audit

**(a) Reliance list — inherited structural-PASS facts I relied on (did NOT re-verify):**
- Relied on rf-qa final-structural PASS for: all 4 findings closed at every site, guards `check_onboarding_performed`/`find_referencing_code_snippets` = 0, 7 allowed-tools present, no project-mutating Serena tool, 5-site §9.1 contract bump intact, verify-sync PASS, evals.json valid JSON, no `.claude/` staged, C2/C3/C4/C5 markers present, and that the large SKILL.md/evals.json `git diff` is the uncommitted parent-task body (HEAD predates §6.3/§0.7).

**(b) Independent semantic checks where structural PASS was insufficient and my own tool work was required (INV-019):**
- F-1 predicate *logical correctness* — structural PASS confirms the `≤ 20` string exists; it does NOT prove the predicate fires on the right class. I derived a 7-row boundary truth-table myself (Read SKILL.md:432 + spec 04-spec:271,280) and confirmed fire-iff-read-only-dominated.
- F-2 *semantic alignment* of the renamed `unknown` SOURCE token with the §9.2 STATUS enum + FR-6.4 — structural PASS confirms the token string; I Read SKILL.md:230,231,684 to confirm the no-signal SOURCE `unknown` is semantically coherent with the STATUS `unknown` and the "no down-weight" rule.
- G-2 *false-positive appropriateness* — structural PASS confirms `regex_present` is well-formed; I Read grader.py:152-159 + :172-187 and the two scaffold expected.yaml files myself to reason that unanchored substring matching is an acceptable strict-improvement for runtime-generated scaffolded contract.yaml, with the limitation disclosed in-band.

**Confidence Gate:**
- **Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 11 | Grep: ~10 (via Bash) | Glob: 0 | Bash: 3
- **UNCHECKED:** none.
- **UNVERIFIABLE:** none. (Tavily/web research: none required — review was fully local-file-bound.)

## Recommendations

- Proceed to Step 6.4 task closure. The two existing follow-ups (FR-1.4 degrade-token gap; whole-case-dir grep for enum renames) are correctly tracked and out-of-scope for this remediation — no new follow-up is warranted.

## QA Complete
