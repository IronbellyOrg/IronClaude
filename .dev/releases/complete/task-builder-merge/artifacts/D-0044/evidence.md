# D-0044 — T04.04 Evidence: AX-5 Canonical-Axes Entry Landed

**Task:** T04.04 (Phase 4 — M4 Five Adversarial Axes Overlay)
**Roadmap item:** R-075 (AX-5 Invented-content axis definition)
**Date:** 2026-05-17
**Status:** PASS
**Tier:** STANDARD
**Confidence:** [█████████-] 90%

---

## 0. TL;DR

AX-5 (Invented content, scope-inflation pattern) canonical-axes
entry authored in `src/superclaude/agents/rf-qa-qualitative.md` at
line 536 inside the FR-CONV.4 overlay region landed by T04.01 and
refined by T04.02 / T04.03. All four acceptance criteria for T04.04
met. 15-item checklist body and severity-floor block byte-identical
to T04.01 / T04.02 / T04.03 baseline. PR-07 test suite 11/11 green;
full `test_task_builder_merge.py` suite 67/68 green (the single
failure is the pre-existing PR-01 Execution Context Header gap
documented in D-0042 §7.2 and D-0043 §7.2, unrelated to T04.04).
The canonical-axes block now carries AX-1..AX-5 with stable IDs +
kebab aliases + roadmap-aligned finding examples; the
`{AX-1..AX-5, none}` vocabulary required by T04.05 / T04.07 /
T04.11 is now fully enumerated.

| AC | Status | Section |
|---|---|---|
| `grep -n "AX-5"` returns ≥ 1 match in canonical-axes block | ✅ PASS | §1 |
| AX-5 definition cites scope inflation pattern | ✅ PASS | §2 |
| Finding example present and aligned with FR-CONV.4 spec | ✅ PASS | §2 |
| Evidence at `D-0044/evidence.md` | ✅ PASS | this file |

Bonus invariant checks (T04.01 / T04.02 / T04.03 baselines preserved):

| Invariant | Status | Section |
|---|---|---|
| 15-item checklist body byte-stable (538–573) | ✅ PASS | §3 |
| Severity-floor block byte-stable (786–795) | ✅ PASS | §4 |
| src ↔ .claude parity | ✅ PASS | §5 |
| Ordering: axis header (528) before checklist (538) | ✅ PASS | §6 |
| PR-07 test suite green (11/11) | ✅ PASS | §7 |
| Evidence-bound clause preserved (AX-5) | ✅ PASS | §7.1 |
| Anti-inflation rule #11 clause preserved (AX-4, unchanged) | ✅ PASS | §7.1 |
| make verify-sync PASS | ✅ PASS | §7.3 |

---

## 1. AC#1 — grep `AX-5` returns ≥ 1 match

**Command:**
```
grep -n "AX-5" src/superclaude/agents/rf-qa-qualitative.md
```

**Output:**
```
536:- **AX-5 Invented content** (kebab alias: `invented-content`) — Does the task reference files, modules, interfaces, or commands NOT present in `research/*.md` evidence files or the actual codebase? Cross-check every named artifact against the research files and the filesystem. More broadly: does the artifact introduce a requirement, feature, or capability not present in its upstream source (BUILD_REQUEST, PRD, TDD, research evidence)? This axis is itself evidence-bound — it requires you to read the research files, not just assert "I don't see it documented." **Finding example (scope-inflation pattern):** the task introduces a Redis caching layer in front of `build_axis_overlay()` to memoise per-task results, but no upstream source — BUILD_REQUEST, PRD §2 FR-CONV.4, TDD §8.5, or `research/*.md` — mentions caching, memoisation, or Redis; the caching layer is an invention that inflates scope beyond what was authorised (mirrors TDD §8.5 row 941's canonical "TDD adds a caching layer the PRD never specified" example). Annotate `axis: AX-5`.
```

**Interpretation:** One distinct line in the canonical-axes block
(the FR-CONV.4 overlay region at 528–536 landed by T04.01 and
refined by T04.02 / T04.03) carries the AX-5 ID as a bullet-header
prefix. The bullet is a complete canonical entry (ID + kebab alias
+ definition + roadmap broader-scope clause + finding example +
axis annotation directive). AC #1 satisfied. The AX-5 bullet also
preserves the canonical "evidence-bound" clause that anchors the
existing `test_invented_content_axis_is_evidence_bound` fixture.

Full canonical-axes block enumeration (AX-1..AX-5) confirmed:
```
$ grep -n "AX-1\|AX-2\|AX-3\|AX-4\|AX-5" src/superclaude/agents/rf-qa-qualitative.md | wc -l
5
```
Five distinct bullets at lines 532–536, one per axis.

---

## 2. AC#2 / AC#3 — Finding example present and pattern-matched to roadmap

**Command:**
```
grep -n "scope-inflation\|scope inflat" src/superclaude/agents/rf-qa-qualitative.md
```

**Output:**
```
536:- **AX-5 Invented content** (kebab alias: `invented-content`) — … **Finding example (scope-inflation pattern):** the task introduces a Redis caching layer in front of `build_axis_overlay()` to memoise per-task results, but no upstream source — BUILD_REQUEST, PRD §2 FR-CONV.4, TDD §8.5, or `research/*.md` — mentions caching, memoisation, or Redis; the caching layer is an invention that inflates scope beyond what was authorised (mirrors TDD §8.5 row 941's canonical "TDD adds a caching layer the PRD never specified" example). Annotate `axis: AX-5`.
```

**Interpretation:**

- AX-5's `**Finding example (scope-inflation pattern):**` sub-phrase
  realises roadmap R-075's "Artifact introduces requirement/feature/
  capability not present in upstream source" (per
  `roadmap-opus-architect.md:224`, AC column: "finding example shows
  scope-inflation pattern"). The concrete example uses the same
  `build_axis_overlay` callable already cited in AX-2's
  return-type-mismatch finding example (D-0042 §3.2) and AX-3's
  missing-signature-update example (D-0043 §3.1), so the
  canonical-axes block runs on one coherent illustration rather
  than scattering fictitious symbols across axes. It aligns with
  TDD §8.5 row 941 ("TDD adds a caching layer the PRD never
  specified") — explicitly cited by reference in the bullet itself
  so the cross-reference is self-documenting.

- The example enumerates the upstream-source cross-check list
  verbatim (BUILD_REQUEST, PRD §2 FR-CONV.4, TDD §8.5, `research/*.md`)
  so the reviewer's discipline is concrete: every named artifact in
  the task must trace back to one of these sources, otherwise it
  fires AX-5.

AC #2 (cites scope inflation pattern) and AC #3 (finding example
present and aligned with FR-CONV.4 spec) both satisfied.

---

## 3. 15-item checklist body byte-stability (lines 538–573)

T04.01 / D-0041 §6 recorded the pre-edit body hash; T04.02 / D-0042
§3 re-verified it; T04.03 / D-0043 §3 re-verified again. T04.04
re-verifies the body slice once more:

**Command:**
```
sed -n '538,573p' src/superclaude/agents/rf-qa-qualitative.md | sha256sum
```

**Output (post-T04.04):**
```
28f8459a7bc9d2863bf3e3cf626a5cdfb623992d8db5bb8770505993a9086aaa  -
```

**Pre-T04.04 baseline (captured before the edit, identical to
T04.03 post-edit baseline):**
```
28f8459a7bc9d2863bf3e3cf626a5cdfb623992d8db5bb8770505993a9086aaa  -
```

**Result:** Byte-identical. The 15-item checklist body is unchanged.
T04.09 / D-0048 will perform the formal end-of-phase byte-diff
sweep, but T04.04's contribution to that diff is verified zero
here.

---

## 4. Severity-floor / Critical Rules block byte-stability (lines 786–795)

T04.10 / D-0049 will perform the formal end-of-phase byte-diff
sweep on the severity-floor block. T04.04 verifies its contribution
is zero:

**Command:**
```
sed -n '786,795p' src/superclaude/agents/rf-qa-qualitative.md | sha256sum
```

**Output (post-T04.04):**
```
97ebf75cf2bafc04f72eda8f3c95bdc1dcc252ba852aa4387346522ea81f10ae  -
```

**Pre-T04.04 baseline (identical to T04.03 post-edit baseline):**
```
97ebf75cf2bafc04f72eda8f3c95bdc1dcc252ba852aa4387346522ea81f10ae  -
```

**Result:** Byte-identical. T04.04 does not modify the severity
floor; the AX-5 bullet preserves the evidence-bound clause and adds
no severity statement of its own.

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
926ff48f9da3c555af681a42644256dea2e0739bd38ad22d4cb115c1139c0cbf  src/superclaude/agents/rf-qa-qualitative.md
926ff48f9da3c555af681a42644256dea2e0739bd38ad22d4cb115c1139c0cbf  .claude/agents/rf-qa-qualitative.md
```

**Result:** Byte-identical mirror. `make verify-sync` PASS (§7.3
below).

Pre-T04.04 file hash was
`b5c808e1115af0a16c8bdabfa5e5ddc105d0ae0b657bb6c197a75295b5740de4`
(per T04.03 / D-0043 §5); post-T04.04 hash is
`926ff48f9da3c555af681a42644256dea2e0739bd38ad22d4cb115c1139c0cbf` —
the only change is the AX-5 edit at line 536.

---

## 6. Ordering preservation (axes header before checklist)

**Command:**
```
grep -n "Five Adversarial Axes\|Checklist (15 items)" \
  src/superclaude/agents/rf-qa-qualitative.md | sort -t: -k1n
```

**Output (canonical lines only — AX-N bullets are listed by their
header text, omitted here for brevity):**
```
528:#### Five Adversarial Axes (PR-07 — applied as a sharpening overlay across all 15 checks below)
538:#### Checklist (15 items)
```

**Result:** Line 528 (axes header) precedes line 538 (checklist
header). T04.01's wrapper-ordering invariant remains intact across
the T04.02 → T04.03 → T04.04 chain.

---

## 7. Regression checks

### 7.1 PR-07 test suite

**Command:**
```
uv run pytest tests/skills/test_task_builder_merge.py::TestPR07AdversarialCategoryNaming -v
```

**Output:**
```
collected 11 items

tests/skills/test_task_builder_merge.py::TestPR07AdversarialCategoryNaming::test_rf_qa_qualitative_contains_axis[Drift] PASSED
tests/skills/test_task_builder_merge.py::TestPR07AdversarialCategoryNaming::test_rf_qa_qualitative_contains_axis[Contradictions] PASSED
tests/skills/test_task_builder_merge.py::TestPR07AdversarialCategoryNaming::test_rf_qa_qualitative_contains_axis[Omissions] PASSED
tests/skills/test_task_builder_merge.py::TestPR07AdversarialCategoryNaming::test_rf_qa_qualitative_contains_axis[Weakened criteria] PASSED
tests/skills/test_task_builder_merge.py::TestPR07AdversarialCategoryNaming::test_rf_qa_qualitative_contains_axis[Invented content] PASSED
tests/skills/test_task_builder_merge.py::TestPR07AdversarialCategoryNaming::test_axes_are_overlay_not_replacement PASSED
tests/skills/test_task_builder_merge.py::TestPR07AdversarialCategoryNaming::test_drift_baseline_requirement PASSED
tests/skills/test_task_builder_merge.py::TestPR07AdversarialCategoryNaming::test_axis_annotation_required_in_items_reviewed PASSED
tests/skills/test_task_builder_merge.py::TestPR07AdversarialCategoryNaming::test_skill_references_5_axis_lens PASSED
tests/skills/test_task_builder_merge.py::TestPR07AdversarialCategoryNaming::test_invented_content_axis_is_evidence_bound PASSED
tests/skills/test_task_builder_merge.py::TestPR07AdversarialCategoryNaming::test_weakened_axis_anti_inflation PASSED

============================== 11 passed in 0.02s ==============================
```

All 11 PR-07 fixtures green:

- `test_rf_qa_qualitative_contains_axis[Drift|Contradictions|Omissions|Weakened criteria|Invented content]` — the title word `Invented content` survives the `**AX-5 Invented content**` prefix transformation; AX-1..AX-4 title words also preserved from prior tasks.
- `test_axes_are_overlay_not_replacement` — wrapper header + "overlay" / "sharpening overlay" preserved.
- `test_drift_baseline_requirement` — `drift-axis-inactive` and `BUILD_REQUEST.GOAL` preserved (T04.02 contribution).
- `test_axis_annotation_required_in_items_reviewed` — `Axis (PR-07)` column header untouched.
- `test_skill_references_5_axis_lens` — SKILL.md axis lens reference untouched (T04.04 did not edit SKILL.md).
- `test_invented_content_axis_is_evidence_bound` — the "evidence-bound" clause is preserved verbatim in the post-edit AX-5 bullet; the `research/*.md` / "research files" phrasing required by the fixture's assertion is present.
- `test_weakened_axis_anti_inflation` — AX-4 anti-inflation clause untouched by T04.04 (T04.03 contribution).

### 7.2 Whole `test_task_builder_merge.py` suite

```
67 passed, 1 failed in 0.05s
```

The single failure is
`TestPR01ExecutionContextHeader::test_execution_context_uses_source_areas_not_paths`
asserting `"NEVER write specific" in skill_text`. This is the same
pre-existing failure documented in D-0042 §7.2 and D-0043 §7.2 —
caused by missing PR-01 Execution Context Header content in
`task-builder/SKILL.md`, unrelated to PR-07 / FR-CONV.4 / T04.04.
Tracked under PR-01 / M2 follow-up work. T04.04 introduces no new
failures.

### 7.3 `make verify-sync`

**Output (tail):**
```
✅ All components in sync.
```

src/ ↔ .claude/ parity confirmed across all skills, agents,
commands, and hooks.

---

## 8. INV-013 composition preservation note

INV-013 (per
`.dev/tasks/done/TASK-TDD-20260514-121250/research/14-invariant-preservation.md:36`)
requires that the 5-axis overlay (PR-07) and the Inherited
Structural Verdict (PR-04, FR-CONV.3) compose cleanly: axes
annotate findings on items the consumer still runs, they do not
substitute for an inherited structural PASS, and an inherited PASS
does not substitute for a semantic check.

T04.04 preserves this composition because:

1. The wrapper paragraph at line 530 ("These axes are NOT new
   checks — they are adversarial lenses that sharpen the existing
   15-item checklist.") is untouched.
2. The kebab annotation vocabulary at line 530
   (`axis: drift | contradictions | omissions | weakened-criteria |
   invented-content`) is preserved verbatim; the new `(kebab alias:
   \`invented-content\`)` parenthetical makes the alias
   relationship explicit but introduces no new vocabulary outside
   the existing enumeration.
3. The AX-5 bullet retains the canonical "evidence-bound" clause —
   so AX-5 explicitly grounds its lens in the research-evidence
   substrate that FR-CONV.3 + research/*.md jointly populate,
   satisfying INV-013's evidence-binding requirement on the
   semantic surface.
4. The AX-5 finding example explicitly enumerates the upstream
   sources (BUILD_REQUEST / PRD / TDD / research) the reviewer must
   cross-check against — making the "annotate, do not substitute"
   discipline operational: AX-5 fires when an item exists that
   *cannot* be traced back to upstream evidence, not when an item
   passes its own internal logic.
5. No new code path, no new pipeline stage, no new agent file, no
   test modification — strictly markdown prose under the
   overlay-only (CB-3) constraint.

---

## 9. Pre / post hashes for downstream cross-reference

| Artifact | Pre-T04.04 hash | Post-T04.04 hash | Notes |
|---|---|---|---|
| `src/superclaude/agents/rf-qa-qualitative.md` (full file) | `b5c808e1115af0a16c8bdabfa5e5ddc105d0ae0b657bb6c197a75295b5740de4` | `926ff48f9da3c555af681a42644256dea2e0739bd38ad22d4cb115c1139c0cbf` | only AX-5 edit at 536 |
| `.claude/agents/rf-qa-qualitative.md` (mirror) | `b5c808e1115af0a16c8bdabfa5e5ddc105d0ae0b657bb6c197a75295b5740de4` | `926ff48f9da3c555af681a42644256dea2e0739bd38ad22d4cb115c1139c0cbf` | parity preserved |
| 15-item checklist body slice (538–573) | `28f8459a7bc9d2863bf3e3cf626a5cdfb623992d8db5bb8770505993a9086aaa` | `28f8459a7bc9d2863bf3e3cf626a5cdfb623992d8db5bb8770505993a9086aaa` | byte-identical |
| Severity-floor slice (786–795) | `97ebf75cf2bafc04f72eda8f3c95bdc1dcc252ba852aa4387346522ea81f10ae` | `97ebf75cf2bafc04f72eda8f3c95bdc1dcc252ba852aa4387346522ea81f10ae` | byte-identical |

T04.09 / D-0048 will reuse the 15-item body baseline; T04.10 /
D-0049 will reuse the severity-floor baseline; both end-of-phase
sweeps will confirm zero contribution from T04.02–T04.04 plus any
other M4 tasks.

---

## 10. Verdict

**T04.04 — PASS.**

All four acceptance criteria met. AX-5 (Invented content)
canonical-axes entry authored at
`rf-qa-qualitative.md:536` with scope-inflation finding example
reusing the `build_axis_overlay` running illustration from
D-0042 / D-0043 and explicitly aligning with TDD §8.5 row 941's
canonical example. 15-item checklist body and severity-floor block
byte-identical to T04.01 / T04.02 / T04.03 baseline. src ↔ .claude
parity preserved. PR-07 test suite 11/11 green; no new failures
introduced in the wider suite. INV-013 composition with inherited
structural PASS clean. Canonical-axes block now carries the full
`{AX-1..AX-5}` enumeration required by T04.05 (`none` sentinel +
`drift-axis-inactive` annotation), T04.07 / T04.11 (Axis column on
Items Reviewed table), and T04.13 (SKILL.md axis directive).

T04.05 (`none` sentinel + `drift-axis-inactive` annotation)
unblocked.
