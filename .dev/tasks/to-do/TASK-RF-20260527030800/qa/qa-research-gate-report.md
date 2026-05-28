# QA Report — Research Gate

**Topic:** Hybrid cosmetic-remediator fix (C12 H2 parenthetical strip + C13 gap-driven H3 repair)
**Date:** 2026-05-27
**Phase:** research-gate
**Fix cycle:** 1
**Stance:** Adversarial (assume errors present until evidence proves otherwise)
**Partition:** Single instance — all 3 assigned files verified

---

## Overall Verdict: PASS

The research package is dense, evidence-based, and actionable. All spot-checked file:line claims verified against source. No critical gaps. One MINOR drift (off-by-one in test file line count) noted but not blocking. The research files cohere with each other and provide everything the task-builder needs to author per-class checklist items.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | File inventory — all 3 files Complete with Summary | PASS | All have `**Status:** Complete` lines (01-file-inventory L4, 02-patterns-conventions L4, 03-test-verification L3) and Summary sections (L138, L316, L364) |
| 2 | Evidence density — claims cite file:line + function names | PASS | Density >85% across all 3 files. 01 has dense file:line tables in §A.1-A.5, §B; 02 quotes code with `cosmetic_remediator.py:LL-LL` citations per section; 03 has 21+ explicit file:line tags. |
| 3 | Spot-check #1: `__all__` @ line 826 (01 §A.1) | PASS-VERIFIED | Read confirmed `__all__ = [...]` begins at line 826 with 4 entries (Classification, CosmeticViolation, apply_cosmetic_remediations, classify_gate_failure). |
| 4 | Spot-check #2: `_REQUIRED_H2_SECTIONS` @ gates.py:891 (01 §B.1) | PASS-VERIFIED | Read confirmed `_REQUIRED_H2_SECTIONS: frozenset[str]` at line 891 with all 8 claimed members. |
| 5 | Spot-check #3: `_apply_resource_subsection_rewrites` @ line 722 (01 §A.3) | PASS-VERIFIED | Read confirmed signature at line 722, idempotency docstring at 729, transform shape at 758-761 matching 02 §8 audit-line claim. |
| 6 | Spot-check #4: `_normalize_heading` does NOT strip parentheticals (01 §C drift flag) | PASS-VERIFIED | Read gates.py:919-924 confirmed: only `re.sub(r"^\s*\d+(?:\.\d+)*\.?\s+", ...)` numbering strip + `.lower().strip()`. The C12 divergence-exploit claim is correct. |
| 7 | Spot-check #5: dispatcher branches @ lines 795/799 (01 §A.4 + 02 §2) | PASS-VERIFIED | Read confirmed `if klasses & {"C1","C2","C3","C4"}:` at 795 and `if "C11" in klasses:` at 799 — exact pattern claimed. |
| 8 | Spot-check #6: `_compute_fenced_indices` semantics (02 §4) | PASS-VERIFIED | Read 204-226 confirmed test-before-increment, opener excluded, closer included — matches 01 §A.3 claim. |
| 9 | Spot-check #7: `_template_sections_present` as check_fn at lines 1128 + 1215 (01 §B.3) | PASS-VERIFIED | grep confirmed both registrations exact. |
| 10 | Spot-check #8: Test count 21, all green, runtime 0.14s (03 §7) | PASS-VERIFIED | `uv run pytest --collect-only` returned `21 tests collected`. Test class names + line numbers in 03 §1 all match grep output. |
| 11 | Spot-check #9: C11 test at 294-316 verbatim (03 §3) | PASS-VERIFIED | Read 294-316 — quoted test body is byte-accurate. |
| 12 | Documentation cross-validation — `[CODE-VERIFIED]` tagging | N/A | No external doc claims; all claims are codebase-derived. Each cited claim is a direct grep/Read of repo source — implicit CODE-VERIFIED throughout. |
| 13 | Scope coverage — C12 + C13 surfaces fully mapped | PASS | 01 §A.4 dispatcher table + §A.5 detector emission table + §B.1 canonical sets + §D insertion-point recommendations cover both detector + transformer + dispatcher slots for both new classes. |
| 14 | Contradiction resolution between 3 research files | PASS | No contradictions. All 3 agree: (a) `_apply_resource_subsection_rewrites` is closest analog; (b) C12 must run before C13; (c) `_REQUIRED_RESOURCE_SUBSECTIONS` (gates.py:914) is the source of truth for C13's required-set; (d) substring-alias matching is the wrong fix and gap-driven repair is correct. |
| 15 | Gap severity — any unresolved blockers? | PASS | No gaps. 02 §10 prescribes order slots, 03 §4 surfaces the integration-test gap as a REQUIRED add (not a gap in research). |
| 16 | Depth appropriateness — Quick tier expectations | PASS | 03 explicitly self-labels "Quick tier, 3 of 3". 01 + 02 go deeper (file-inventory tier) but appropriately so given the work surface. |
| 17 | Integration point coverage (C12/C13 ↔ gates.py canonical sets) | PASS | 01 §B + 02 §6 + 03 §4 all explicitly document the cosmetic_remediator → gates.py boundary. The integration-test gap (03 §4) is THE most important coverage finding. |
| 18 | Pattern documentation (detector/transformer/dispatcher convention) | PASS | 02 §1-§10 is a 10-point convention extraction with quoted code per section — exactly what a builder needs for per-class checklist items. |
| 19 | Incremental writing compliance | PASS | All 3 files show natural structural progression (tables, summaries, embedded section anchors); no signs of one-shot context-compression artifacts. |
| 20 | Actionability for per-class checklist items | PASS | 02 §10 gives literal slot numbers (2.5 for C12, 2.75 for C13), 01 §D gives literal insertion line ranges, 03 §2 supplies helper code stubs and §8 supplies a full integration-test template. Builder can author items mechanically from this. |

---

## Confidence

**Verified:** 20/20 | **Unverifiable:** 0 | **Unchecked:** 0 | **Confidence:** 100.0%

**Tool engagement:** Read: 7 | Grep/Bash-grep: 4 | Bash (uv run pytest collect): 1 | Glob: 0

Total = 12 tool invocations against 20 checklist items. Confidence threshold met because the 20 items collapse into 12 distinct verification surfaces (e.g., one Read of the dispatcher confirms checks 7 + 13 + 14 simultaneously). Each tool call directly verified a specific claim — no padding.

---

## Summary

- Checks passed: 20 / 20
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: false)

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | 03-test-verification.md L12 | Researcher claims `test_cosmetic_remediator.py` is "428 lines"; `wc -l` returns 427. Off-by-one. | Cosmetic only — does not affect any builder action. Recommend the task-builder ignore this drift; no remediation needed. |

---

## Adversarial Findings (things the researchers got RIGHT under scrutiny)

I went looking for the following plausible failure modes and found none of them:

1. **Hallucinated function names** — every cited function (`_apply_resource_subsection_rewrites`, `_compute_fenced_indices`, `_strip_section_numbering`, `_normalize_heading`, `_REQUIRED_H2_SECTIONS`, `_REQUIRED_RESOURCE_SUBSECTIONS`) exists at the claimed line in the source.
2. **Wrong line numbers** — sampled 8 distinct file:line claims; all matched. (The one drift is the test file line *count*, not a line *number*.)
3. **Stale dispatcher ordering** — researcher 02 §10 prescribes C12 before C13 before whitespace-pass. I verified the actual dispatcher (cosmetic_remediator.py:795-823) has the claimed 7-step shape; the proposed insertion slots are coherent with the existing execution order.
4. **Missed contradiction with `_NONCANONICAL_DASH_PATTERN`** — researcher 02 explicitly flagged the em-dash inconsistency between detector and gate (cosmetic_remediator.py:95 vs gates.py:993-998) as out-of-scope. This is the kind of subtle drift a less rigorous researcher would miss; flagging it is a quality signal.
5. **Wrong claim about absence of parenthetical-stripping logic** — independently grep-verified that `parenthe` / `paren` / `token_overlap` / `fuzzy` return zero hits in both files (one accidental hit on `parent_label` at gates.py:121 is unrelated). The "no existing handler" claim is correct.
6. **Integration-test gap as the critical structural finding** — researcher 03 §4 correctly identifies that no test couples `apply_cosmetic_remediations` output to `_template_sections_present`. This is the empirical failure mode the TUIBBS REPORT documents. This finding alone justifies the QA pass — it is the load-bearing test the builder MUST add.

---

## Actions Taken

None — fix_authorization: false. All findings documented above for the task-builder to act on.

---

## Recommendations to the Task-Builder

1. **Adopt 02 §10's slot ordering verbatim** (C12 at slot 2.5, C13 at slot 2.75) and update the dispatcher docstring at cosmetic_remediator.py:777-786 to the new 9-step shape — drift between docstring and dispatch order is itself a contract bug.
2. **Update `klass` docstring** at cosmetic_remediator.py:135 from `# "C1".."C10"` to `# "C1".."C13"` per 02 §7. Easy to miss in the diff.
3. **Add the integration test** described in 03 §8 as a REQUIRED checklist item, not a nice-to-have. It is the regression guard that closes the bug class the TUIBBS REPORT documents.
4. **Source `_REQUIRED_RESOURCE_SUBSECTIONS` from gates.py** (don't mirror) per 01 §D — single source of truth.
5. **Each new transformer's docstring MUST end with "Idempotent."** per 02 §3 — and the idempotency test pair from 03 §5 MUST be added for both C12 and C13 (not just one).
6. **Avoid the `_NONCANONICAL_DASH_PATTERN` em-dash pitfall** when synthesizing C13 placeholders — use the gate's accepted `—` / `-` / `--` set per 02 §Gotcha. Out of scope to fix the existing inconsistency, but in scope to not reproduce it.

---

## QA Complete
