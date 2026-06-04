# QA Report — Research Gate (Re-check, gap-fill 07)

**Topic:** sc:reflect V3 Serena low-complexity adoptions — Issue #1 re-check (contract_version literal)
**Date:** 2026-06-02
**Phase:** research-gate (focused re-check of single gap-fill file)
**Fix cycle:** N/A (fix_authorization: false)
**Scope:** ONLY `research/07-gap-fill-contract-version.md` vs source. The other 6 files already PASSed and were NOT re-validated.

---

## Overall Verdict: FAIL

The gap-fill correctly resolves the **value** ambiguity (adopt `"1.1.0"`, 3-segment) and correctly identifies edit #4 (the §9.4 L640 format-declaration string). Every line-number claim it makes is byte-accurate against source. **However, the 4-edit set is INCOMPLETE.** There is a FIFTH load-bearing `contract_version` site — the grader/falsifier assertion at `SKILL.md:1503` which hard-codes `return-contract.yaml contract_version == "1.0"`. Bumping §9.1 to `"1.1.0"` without updating L1503 makes the eval-gate assertion fail (it would assert `== "1.0"` against an emitted `"1.1.0"`). The gap-fill claims the 4-edit set is "the correct, complete site list" — it is NOT. Issue #1 is therefore NOT fully resolved.

---

## Claim-by-claim verification (all anchors independently re-Read from source)

| # | Gap-fill claim | Source check | Result |
|---|----------------|--------------|--------|
| 1 | SKILL.md:640 declares format `contract_version: "<major>.<minor>"` (2-seg) | Read L640: ``The return contract is versioned via `contract_version: "<major>.<minor>"`.`` | VERIFIED — exact |
| 2 | SKILL.md:642-644 versioning bullets use 3-SEGMENT examples (1.0.x / 1.x.0 / X.0.0) | Read L644 `Patch (1.0.x)`, L645 `Minor (1.x.0)`, L646 `Major (X.0.0)` | VERIFIED — claim cites 642-644; the three rule bullets actually sit at L644/645/646 (the `**Versioning rule.**` label is L642, blank L643). Off-by-two on the bullet anchor, but the substance (3-segment bullets exist directly beneath L640) is correct. MINOR cite drift, non-blocking. |
| 3 | SKILL.md:491 heading + :494 value are 2-segment "1.0" | Read L491 `### 9.1 Stable contract (contract_version: 1.0)`; L494 `contract_version: "1.0"` | VERIFIED — exact, both lines |
| 4 | refs/report-template.md:14 uses 3-segment `contract_version: 1.0.0` | Read L14 `contract_version: 1.0.0` | VERIFIED — exact |
| 5a | Trailer site `~:599` references the version | Read L599: ``Each flag has a one-line semantics description in `refs/report-template.md`. Contract version is `v1.0`.`` | VERIFIED — L599 references the version as `v1.0` (NOT the literal `"1.0"` string). See note below: the trailer says `v1.0`, so the edit must change `v1.0` → `v1.1.0`, not `"1.0"` → `"1.1.0"`. The gap-fill table row #3 says "`1.0` reference (verify exact line in chain)" which is approximately right but does not capture that the literal at this site is `v1.0` (with a `v` prefix), not a quoted string. Minor imprecision, but a builder editing blindly for `"1.0"` at L599 would find no match. |
| 5b | The 4-edit set is the "correct, complete site list" | `grep -n 'contract_version\|v1.0\|"1.0"'` across full SKILL.md (1585 lines) | **FAIL — INCOMPLETE.** See Issue R1 below. |
| 6 | Resolution is deterministic/actionable | Directive states "adopt 1.1.0", names sites, mandates edit #4 | PARTIAL — the value decision is deterministic and well-argued; but because the site list is incomplete (misses L1503), a builder following it deterministically would ship a broken eval gate. |

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| R1 | **CRITICAL** | SKILL.md:1503 (eval/falsifier assertion table, §16/§12 grading registry) — MISSED by gap-fill's 4-edit set | The gap-fill asserts its 4-edit set (L491, L494, ~L599, L640) is "the correct, complete site list for adopting 1.1.0 consistently." It is NOT. Line 1503 contains a hard-coded grader assertion: `` `return-contract.yaml contract_version == "1.0"` `` (a `yaml_field` eval check for "§9.1 versioned return contract stability"). If §9.1's value is bumped to `"1.1.0"` (edits #1/#2/#3) without updating L1503, the emitted contract carries `"1.1.0"` but the grader asserts equality against the literal `"1.0"` — the eval gate FAILS on every run. This is the exact failure mode Issue #1 was about: one literal value that must be written consistently into ALL sites that bind it. The gap-fill found 4 of 5. | Add a FIFTH edit to the set: SKILL.md:1503 `return-contract.yaml contract_version == "1.0"` → `... == "1.1.0"`. State it as a mandatory coordinated edit (same tier as edit #4). Without it the bump is not internally consistent and the eval suite breaks. |
| R2 | MINOR | gap-fill L36 / SKILL.md:642-644 vs actual 644-646 | The rule bullets cited at "642-644" actually render at L644/645/646 (L642 is the `**Versioning rule.**` label, L643 blank). Substance is correct (3-segment bullets sit beneath L640); anchor is off by two. | Cite L644-646 for the three bullets, or L642-646 for the labeled block. Non-blocking. |
| R3 | MINOR | gap-fill L35 (table row #3) / SKILL.md:599 | The trailer literal at L599 is `v1.0` (with a `v` prefix in prose: "Contract version is `v1.0`"), NOT the quoted YAML string `"1.0"`. The gap-fill row #3 hand-waves "verify exact line in chain." A builder must change `v1.0` → `v1.1.0` here, which is a different match target than the §9.1 value edit. | Make row #3 explicit: site is `Contract version is `v1.0`.` at L599; edit changes `v1.0` → `v1.1.0`. |

### Sites I checked and CLEARED (not part of the bump — correctly excluded)

The full grep surfaced several other `1.0` / `v1.0` tokens. I verified each is NOT a contract_version binding and correctly NOT in scope:

- **L1289** `"skill_version": "<contract_version from §9.1>"` — a *symbolic reference* ("from §9.1"), not a hard-coded literal. Auto-tracks the §9.1 value once §9.1 is bumped. No edit needed. CLEARED.
- **L1372** `"skill_version": "1.0"` — sample/illustrative JSON-lines record (a worked example of an emitted line), not a binding declaration or assertion. Cosmetic; out of scope for the contract bump (could optionally be refreshed but does not break anything). CLEARED as non-blocking.
- **L1286** `"metrics_schema_version": "1.0"` — DIFFERENT version field (metrics schema, not contract). CLEARED.
- **L1158** `checkpoint_version: "1.0"`, **L1204** `promotion_log_version: "1.0"` — DIFFERENT version fields (checkpoint/promotion-log schemas). CLEARED.
- **L195, L546, L908+, L1081, L1451-1581** `v1.0` / "in v1.0" — these refer to the **skill release version** (frontmatter `version: 1.0.0`), the v1.0 *posture* of features, NOT the return-contract version. CLEARED.

The single genuine miss is **L1503**, which is unambiguously a `contract_version` value binding (it is literally `contract_version == "1.0"`).

---

## Answer to the KEY QUESTION

> Does adopting "1.1.0" + fixing the §9.4 L640 format-declaration to "<major>.<minor>.<patch>" resolve the conflict consistently, with no remaining contradiction? Is edit #4 correctly identified?

- **Edit #4 (L640 format-string fix): correctly identified.** VERIFIED. The format declaration at L640 is the 2-segment string, the bullets beneath it are 3-segment, the value adoption is 3-segment — edit #4 reconciles them. Good catch by the gap-fill.
- **Value decision (adopt "1.1.0"): correct and well-justified.** Spec mandates it 5×; matches `report-template.md` (1.0.0) and the §9.4 bullet form. VERIFIED.
- **"No remaining contradiction": FALSE.** A 5th site (L1503 grader assertion) binds the literal `"1.0"` and is NOT in the edit set. After the 4 edits, the emitted contract says `1.1.0` while the eval gate asserts `== "1.0"` — a fresh, runtime-breaking contradiction. The conflict is NOT fully resolved by the 4-edit set.

---

## Summary

- Re-check claims verified: 6 / 6 line-anchor claims accurate (with 2 minor anchor/literal imprecisions, R2/R3)
- Critical issues: 1 (R1 — missing 5th edit site at L1503)
- The gap-fill's value decision and edit #4 are CORRECT; its completeness claim is FALSE.

## Confidence Gate

- **Confidence:** Verified: 6/6 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 6 | Grep: 0 | Glob: 0 | Bash: 2 (grep sweeps for all contract_version / 1.0 tokens across the full 1585-line file + refs/)
- No web research performed (all claims repo-local; no external URL/standard/API lookup required).
- Tool-engagement note: Every Read targeted a specific claimed anchor (491/494/599/640/642-646/report-template:14/1503/1289). The two Bash greps were the completeness check that surfaced L1503 — directly mapped to verification item 5b ("is the site list complete?"). No padding.

## Recommendations

1. **BLOCKER (R1):** The builder's contract-bump edit set MUST be **5 edits, not 4**. Add SKILL.md:1503 `contract_version == "1.0"` → `contract_version == "1.1.0"`. Without it the falsifier/eval grader assertion (`§9.1 versioned return contract stability`) fails on every run after the bump. The gap-fill must be corrected to list 5 sites and retract its "complete site list" claim, OR the builder instruction must independently carry the 5th edit.
2. **Fix (R2):** Re-anchor the §9.4 rule bullets to L644-646 (or L642-646 for the labeled block).
3. **Fix (R3):** Make trailer row #3 explicit: L599 literal is `v1.0` (prose, `v`-prefixed), edit to `v1.1.0`.
4. Issue #2 carry-forward (FR-1/2/4/5 vs L318's 1/2/4/8) is correctly handled by the gap-fill (L40-42) — no new concern.

## QA Complete
