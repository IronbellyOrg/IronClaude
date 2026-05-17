# D-0043 — T04.03 Evidence: AX-3 + AX-4 Canonical-Axes Entries Landed

**Task:** T04.03 (Phase 4 — M4 Five Adversarial Axes Overlay)
**Roadmap items:** R-073 (AX-3 Omissions), R-074 (AX-4 Weakened criteria)
**Date:** 2026-05-17
**Status:** PASS
**Tier:** STANDARD
**Confidence:** [████████--] 88%

---

## 0. TL;DR

AX-3 (Omissions, missing-signature-update pattern) and AX-4
(Weakened criteria, trivially-passing-test pattern) canonical-axes
entries authored in `src/superclaude/agents/rf-qa-qualitative.md` at
lines 534–535 inside the FR-CONV.4 overlay region landed by T04.01
and refined by T04.02. All four acceptance criteria for T04.03 met.
15-item checklist body and severity-floor block byte-identical to
T04.01 / T04.02 baseline. PR-07 test suite 11/11 green; full
`test_task_builder_merge.py` suite 67/68 green (the single failure
is the pre-existing PR-01 Execution Context Header gap documented
in D-0042 §7.2, unrelated to T04.03).

| AC | Status | Section |
|---|---|---|
| `grep -c "AX-3\|AX-4"` returns ≥ 2 distinct matches in canonical-axes block | ✅ PASS | §1 |
| AX-3 cites missing-signature-update pattern; AX-4 cites trivially-passing-test pattern | ✅ PASS | §2 |
| Both finding examples present | ✅ PASS | §2 |
| Evidence at `D-0043/evidence.md` | ✅ PASS | this file |

Bonus invariant checks (T04.01 / T04.02 baselines preserved):

| Invariant | Status | Section |
|---|---|---|
| 15-item checklist body byte-stable (538–573) | ✅ PASS | §3 |
| Severity-floor block byte-stable (786–795) | ✅ PASS | §4 |
| src ↔ .claude parity | ✅ PASS | §5 |
| Ordering: axis header (528) before checklist (538) | ✅ PASS | §6 |
| PR-07 test suite green (11/11) | ✅ PASS | §7 |
| Anti-inflation rule #11 clause preserved (AX-4) | ✅ PASS | §7.1 |
| Inherited-Structural-Verdict FAIL clause preserved (AX-3) | ✅ PASS | §1 |
| make verify-sync PASS | ✅ PASS | §7.3 |

---

## 1. AC#1 — grep `AX-3\|AX-4` returns ≥ 2 distinct matches

**Command:**
```
grep -c "AX-3\|AX-4" src/superclaude/agents/rf-qa-qualitative.md
```

**Output:**
```
2
```

**Distinct-match listing:**
```
$ grep -n "AX-3\|AX-4" src/superclaude/agents/rf-qa-qualitative.md
534:- **AX-3 Omissions** (kebab alias: `omissions`) — Are any BUILD_REQUEST `QA_GATE_REQUIREMENTS`, `VALIDATION_REQUIREMENTS`, or `TESTING_REQUIREMENTS` (SKILL.md rules #16/#17/#18) missing from the task as checklist items? Are any rf-qa FAIL items from the Inherited Structural Verdict left unaddressed? More broadly: is a required touchpoint, consumer, dependency, or step absent from the plan? **Finding example (missing-signature-update pattern):** an item passes a new `axis` kwarg to `build_axis_overlay()`, but no earlier item updates the function's signature to accept it; the kwarg is supplied to a callable that never declared it, so the new argument is silently dropped or raises `TypeError` at runtime. Annotate `axis: AX-3`.
535:- **AX-4 Weakened criteria** (kebab alias: `weakened-criteria`) — Are acceptance criteria phrased more permissively than BUILD_REQUEST or the research findings warrant? Look for "or" splits, "may" verbs, optional clauses, conditional language ("if applicable") where the source materials are unconditional. Has an acceptance/verification condition been softened to something unobservable or trivially satisfiable? An item is "weakened" only when BUILD_REQUEST or research evidence demands stronger phrasing — speculation about absent stronger phrasing does NOT count (anti-inflation alignment with rule #11). **Finding example (trivially-passing-test pattern):** a verification step writes the 6-character placeholder `# Test` into a fixture file and then asserts that the file is non-empty (or contains the substring `Test`); the assertion passes for the placeholder itself and exercises none of the feature under review. Annotate `axis: AX-4`.
```

**Interpretation:** Two distinct lines in the canonical-axes block
(the FR-CONV.4 overlay region at 528–536 landed by T04.01 and
refined by T04.02) carry the AX-3 / AX-4 IDs as bullet-header
prefixes. Each bullet is a complete canonical entry (ID + kebab
alias + definition + roadmap broader-scope clause + finding example
+ axis annotation directive). AC #1 satisfied. The AX-3 bullet also
preserves the Inherited-Structural-Verdict FAIL-carryover clause
("Are any rf-qa FAIL items from the Inherited Structural Verdict
left unaddressed?") landed by T03.16 / D-0039.

---

## 2. AC#2 / AC#3 — Finding examples present and pattern-matched to roadmap

**Command:**
```
grep -n "missing-signature-update\|trivially-passing-test" src/superclaude/agents/rf-qa-qualitative.md
```

**Output:**
```
534:- **AX-3 Omissions** (kebab alias: `omissions`) — … **Finding example (missing-signature-update pattern):** an item passes a new `axis` kwarg to `build_axis_overlay()`, but no earlier item updates the function's signature to accept it; the kwarg is supplied to a callable that never declared it, so the new argument is silently dropped or raises `TypeError` at runtime. Annotate `axis: AX-3`.
535:- **AX-4 Weakened criteria** (kebab alias: `weakened-criteria`) — … **Finding example (trivially-passing-test pattern):** a verification step writes the 6-character placeholder `# Test` into a fixture file and then asserts that the file is non-empty (or contains the substring `Test`); the assertion passes for the placeholder itself and exercises none of the feature under review. Annotate `axis: AX-4`.
```

**Interpretation:**

- AX-3's `**Finding example (missing-signature-update pattern):**`
  sub-phrase realises roadmap R-073's "A required touchpoint,
  consumer, dependency, or step absent from plan" (per
  `roadmap-opus-architect.md:222`, AC column: "finding example shows
  missing signature-update pattern"). The concrete example uses the
  same `build_axis_overlay` callable already cited in AX-2's
  return-type-mismatch finding example (D-0042 §3.2), so the
  canonical-axes block runs on one coherent illustration rather than
  scattering fictitious symbols across axes. It aligns with TDD §8.5
  row 939 ("Item adds a new kwarg but no item updates the function
  signature to accept it.").

- AX-4's `**Finding example (trivially-passing-test pattern):**`
  sub-phrase realises roadmap R-074's "Acceptance/verification
  condition softened to unobservable or trivially satisfiable" (per
  `roadmap-opus-architect.md:223`, AC column: "finding example shows
  trivially-passing test pattern"). The concrete example reuses the
  `# Test` placeholder already cited by checklist item #7 (`Test
  validity`) at line 558 — so the AX-4 lens explicitly sharpens the
  item it annotates, reinforcing INV-013 (axes annotate; do not
  substitute). It aligns with TDD §8.5 row 940 ("Verification reads
  `# Test` into a file and asserts on the 6-char placeholder.").

AC #2 and AC #3 both satisfied. AC #4 (both finding examples
present) follows from the same two grep matches.

---

## 3. 15-item checklist body byte-stability (lines 538–573)

T04.01 / D-0041 §6 recorded the pre-edit body hash; T04.02 / D-0042
§3 re-verified it. T04.03 re-verifies the body slice once more:

**Command:**
```
sed -n '538,573p' src/superclaude/agents/rf-qa-qualitative.md | sha256sum
```

**Output (post-T04.03):**
```
28f8459a7bc9d2863bf3e3cf626a5cdfb623992d8db5bb8770505993a9086aaa  -
```

**Pre-T04.03 baseline (captured before the edit, identical to
T04.02 post-edit baseline):**
```
28f8459a7bc9d2863bf3e3cf626a5cdfb623992d8db5bb8770505993a9086aaa  -
```

**Result:** Byte-identical. The 15-item checklist body is unchanged.
T04.08 / D-0048 will perform the formal end-of-phase byte-diff sweep,
but T04.03's contribution to that diff is verified zero here.

---

## 4. Severity-floor / Critical Rules block byte-stability (lines 786–795)

T04.10 / D-0049 will perform the formal end-of-phase byte-diff sweep
on the severity-floor block. T04.03 verifies its contribution is
zero:

**Command:**
```
sed -n '786,795p' src/superclaude/agents/rf-qa-qualitative.md | sha256sum
```

**Output (post-T04.03):**
```
97ebf75cf2bafc04f72eda8f3c95bdc1dcc252ba852aa4387346522ea81f10ae  -
```

**Pre-T04.03 baseline (identical to T04.02 post-edit baseline):**
```
97ebf75cf2bafc04f72eda8f3c95bdc1dcc252ba852aa4387346522ea81f10ae  -
```

**Result:** Byte-identical. T04.03 does not modify the severity
floor; the AX-4 bullet preserves the anti-inflation rule #11 clause
by reference and adds no severity statement of its own.

---

## 5. src ↔ .claude parity

Per project rule: edit `src/superclaude/`, then `make sync-dev` to
mirror into `.claude/`. After `make sync-dev`:

**Command:**
```
sha256sum src/superclaude/agents/rf-qa-qualitative.md .claude/agents/rf-qa-qualitative.md
```

**Output:**
```
b5c808e1115af0a16c8bdabfa5e5ddc105d0ae0b657bb6c197a75295b5740de4  src/superclaude/agents/rf-qa-qualitative.md
b5c808e1115af0a16c8bdabfa5e5ddc105d0ae0b657bb6c197a75295b5740de4  .claude/agents/rf-qa-qualitative.md
```

**Result:** Byte-identical mirror. `make verify-sync` PASS (§7.3
below).

Pre-T04.03 file hash was
`e20183f61e09d703dc044651029305d3f4462ba4d023ca2c6e695c4f8548bcf9`
(per T04.02 / D-0042 §5); post-T04.03 hash is
`b5c808e1115af0a16c8bdabfa5e5ddc105d0ae0b657bb6c197a75295b5740de4` —
the only change is the AX-3 / AX-4 edit at lines 534–535.

---

## 6. Ordering preservation (axes header before checklist)

**Command:**
```
grep -n "Five Adversarial Axes\|Checklist (15 items)" \
  src/superclaude/agents/rf-qa-qualitative.md | sort -t: -k2n
```

**Output (canonical lines only — AX-N bullets are listed by their
header text, omitted here for brevity):**
```
528:#### Five Adversarial Axes (PR-07 — applied as a sharpening overlay across all 15 checks below)
538:#### Checklist (15 items)
```

**Result:** Line 528 (axes header) precedes line 538 (checklist
header). T04.01's wrapper-ordering invariant remains intact across
the T04.02 → T04.03 chain.

---

## 7. Regression checks

### 7.1 PR-07 test suite

**Command:**
```
uv run pytest tests/skills/test_task_builder_merge.py::TestPR07AdversarialCategoryNaming -q
```

**Output:**
```
...........                                                              [100%]
11 passed in 0.02s
```

All 11 PR-07 fixtures green:

- `test_rf_qa_qualitative_contains_axis[Drift|Contradictions|Omissions|Weakened criteria|Invented content]` — the title words `Omissions` and `Weakened criteria` survive the `**AX-3 Omissions**` / `**AX-4 Weakened criteria**` prefix transformations.
- `test_axes_are_overlay_not_replacement` — wrapper header + "overlay" / "sharpening overlay" preserved.
- `test_drift_baseline_requirement` — `drift-axis-inactive` and `BUILD_REQUEST.GOAL` preserved (T04.02 contribution).
- `test_axis_annotation_required_in_items_reviewed` — `Axis (PR-07)` column header (line ~701) untouched.
- `test_skill_references_5_axis_lens` — SKILL.md axis lens reference untouched (T04.03 did not edit SKILL.md).
- `test_invented_content_axis_is_evidence_bound` — Invented-content bullet (line 536) untouched; T04.04 / D-0044 will prefix it with AX-5.
- `test_weakened_axis_anti_inflation` — the "speculation about absent stronger phrasing does NOT count (anti-inflation alignment with rule #11)" clause is preserved verbatim in the post-edit AX-4 bullet.

### 7.2 Whole `test_task_builder_merge.py` suite

```
67 passed, 1 failed in 0.05s
```

The single failure is
`TestPR01ExecutionContextHeader::test_execution_context_uses_source_areas_not_paths`
asserting `"NEVER write specific" in skill_text`. This is the same
pre-existing failure documented in D-0042 §7.2 — caused by missing
PR-01 Execution Context Header content in `task-builder/SKILL.md`,
unrelated to PR-07 / FR-CONV.4 / T04.03. Tracked under PR-01 / M2
follow-up work. T04.03 introduces no new failures.

### 7.3 `make verify-sync`

**Output (tail):**
```
✅ All components in sync.
```

src/ ↔ .claude/ parity confirmed across all skills, agents, commands,
and hooks.

---

## 8. INV-013 composition preservation note

INV-013 (per
`.dev/tasks/done/TASK-TDD-20260514-121250/research/14-invariant-preservation.md:36`)
requires that the 5-axis overlay (PR-07) and the Inherited
Structural Verdict (PR-04, FR-CONV.3) compose cleanly: axes
annotate findings on items the consumer still runs, they do not
substitute for an inherited structural PASS, and an inherited PASS
does not substitute for a semantic check.

T04.03 preserves this composition because:

1. The wrapper paragraph at line 530 ("These axes are NOT new
   checks — they are adversarial lenses that sharpen the existing
   15-item checklist.") is untouched.
2. The kebab annotation vocabulary at line 530
   (`axis: drift | contradictions | omissions | weakened-criteria |
   invented-content`) is preserved verbatim; the new `(kebab alias:
   \`omissions\`)` and `(kebab alias: \`weakened-criteria\`)`
   parentheticals make the alias relationship explicit but introduce
   no new vocabulary outside the existing enumeration.
3. The AX-3 bullet retains the Inherited-Structural-Verdict FAIL
   carry-over clause ("Are any rf-qa FAIL items from the Inherited
   Structural Verdict left unaddressed?") landed by T03.16 / D-0039
   — so AX-3 explicitly bridges FR-CONV.3 inherited verdicts into
   the FR-CONV.4 axis overlay, satisfying INV-013's composition
   requirement.
4. The AX-4 finding example explicitly cites the `# Test`
   placeholder already used by checklist item #7 (`Test validity`)
   at line 558, reinforcing that AX-4 sharpens an existing checklist
   item rather than introducing a new check.
5. No new code path, no new pipeline stage, no new agent file, no
   test modification — strictly markdown prose under the overlay-only
   (CB-3) constraint.

---

## 9. Pre / post hashes for downstream cross-reference

| Artifact | Pre-T04.03 hash | Post-T04.03 hash | Notes |
|---|---|---|---|
| `src/superclaude/agents/rf-qa-qualitative.md` (full file) | `e20183f61e09d703dc044651029305d3f4462ba4d023ca2c6e695c4f8548bcf9` | `b5c808e1115af0a16c8bdabfa5e5ddc105d0ae0b657bb6c197a75295b5740de4` | only AX-3 / AX-4 edit at 534–535 |
| `.claude/agents/rf-qa-qualitative.md` (mirror) | `e20183f61e09d703dc044651029305d3f4462ba4d023ca2c6e695c4f8548bcf9` | `b5c808e1115af0a16c8bdabfa5e5ddc105d0ae0b657bb6c197a75295b5740de4` | parity preserved |
| 15-item checklist body slice (538–573) | `28f8459a7bc9d2863bf3e3cf626a5cdfb623992d8db5bb8770505993a9086aaa` | `28f8459a7bc9d2863bf3e3cf626a5cdfb623992d8db5bb8770505993a9086aaa` | byte-identical |
| Severity-floor slice (786–795) | `97ebf75cf2bafc04f72eda8f3c95bdc1dcc252ba852aa4387346522ea81f10ae` | `97ebf75cf2bafc04f72eda8f3c95bdc1dcc252ba852aa4387346522ea81f10ae` | byte-identical |

T04.08 / D-0048 will reuse the 15-item body baseline; T04.10 /
D-0049 will reuse the severity-floor baseline; both end-of-phase
sweeps will confirm zero contribution from T04.02–T04.04 plus any
other M4 tasks.

---

## 10. Verdict

**T04.03 — PASS.**

All four acceptance criteria met. AX-3 (Omissions) and AX-4
(Weakened criteria) canonical-axes entries authored at
`rf-qa-qualitative.md:534–535` with missing-signature-update and
trivially-passing-test finding examples respectively. 15-item
checklist body and severity-floor block byte-identical to T04.01 /
T04.02 baseline. src ↔ .claude parity preserved. PR-07 test suite
11/11 green; no new failures introduced in the wider suite.
INV-013 composition with inherited structural PASS clean.

T04.04 (AX-5) unblocked.
