# D-0042 — T04.02 Evidence: AX-1 + AX-2 Canonical-Axes Entries Landed

**Task:** T04.02 (Phase 4 — M4 Five Adversarial Axes Overlay)
**Roadmap items:** R-071 (AX-1 Drift), R-072 (AX-2 Contradictions)
**Date:** 2026-05-17
**Status:** PASS
**Tier:** STANDARD
**Confidence:** [████████--] 88%

---

## 0. TL;DR

AX-1 (Drift, stale citation pattern) and AX-2 (Contradictions,
return-type mismatch pattern) canonical-axes entries authored in
`src/superclaude/agents/rf-qa-qualitative.md` at lines 532–533 inside
the FR-CONV.4 overlay region landed by T04.01. All four acceptance
criteria for T04.02 met. 15-item checklist body and severity-floor
block byte-identical to T04.01 baseline. PR-07 test suite green.

| AC | Status | Section |
|---|---|---|
| `grep -c "AX-1\|AX-2"` returns ≥ 2 distinct matches in canonical-axes block | ✅ PASS | §1 |
| AX-1 cites stale citation pattern; AX-2 cites return-type mismatch pattern | ✅ PASS | §2 |
| Both finding examples present | ✅ PASS | §2 |
| Evidence at `D-0042/evidence.md` | ✅ PASS | this file |

Bonus invariant checks (T04.01 baselines preserved):

| Invariant | Status | Section |
|---|---|---|
| 15-item checklist body byte-stable (538–573) | ✅ PASS | §3 |
| Severity-floor block byte-stable (786–795) | ✅ PASS | §4 |
| src ↔ .claude parity | ✅ PASS | §5 |
| Ordering: axis header (528) before checklist (538) | ✅ PASS | §6 |
| PR-07 test suite green | ✅ PASS | §7 |
| make verify-sync PASS | ✅ PASS | §7 |

---

## 1. AC#1 — grep `AX-1\|AX-2` returns ≥ 2 distinct matches

**Command:**
```
grep -c "AX-1\|AX-2" src/superclaude/agents/rf-qa-qualitative.md
```

**Output:**
```
2
```

**Distinct-match listing:**
```
$ grep -n "AX-1\|AX-2" src/superclaude/agents/rf-qa-qualitative.md
532:- **AX-1 Drift** (kebab alias: `drift`) — Has the task content drifted from BUILD_REQUEST.GOAL through paraphrasing, OR has a cited fact (file path, line number, signature, count, config value) drifted out of sync with current source? Look for paraphrases that substitute weaker verbs ("review" instead of "validate", "consider" instead of "implement") or quietly narrowed scope. **Drift-baseline requirement:** before applying the drift axis, you MUST capture the BUILD_REQUEST.GOAL verbatim somewhere in your review notes — typically as part of your initial Read of the task file or the spawn prompt. If no GOAL verbatim is available (e.g., the spawn prompt elided it and the task file does not reproduce it), drift axis is INACTIVE for this review; annotate `drift-axis-inactive` in the report and proceed with the other four axes. **Finding example (stale citation pattern):** task item cites `rf-qa-qualitative.md:528 — "Five Adversarial Axes" header`, but an upstream insertion shifted the header to line 530; the cited line number no longer matches current source. Annotate `axis: AX-1`.
533:- **AX-2 Contradictions** (kebab alias: `contradictions`) — Do two items in the task (or two artifacts, or two sections of one artifact) assert mutually incompatible facts about the same subject? One says "use A", another implies "must not use A"? Do frontmatter fields contradict body content? Do Acceptance Criteria contradict Open Questions? Severity floor: IMPORTANT (cf. Critical Rule #6). **Finding example (return-type mismatch pattern):** Section A states `build_axis_overlay()` returns `dict[str, Axis]`, while Section B's call site unpacks the same function's return value as `list[Axis]` (`for ax in build_axis_overlay(): ...`). Two artifacts assert incompatible return types for the same callable. Annotate `axis: AX-2` with severity ≥ IMPORTANT.
```

**Interpretation:** Two distinct lines in the canonical-axes block
(the FR-CONV.4 overlay region at 528–536 landed by T04.01) carry the
AX-1 / AX-2 IDs as bullet-header prefixes. Each bullet is a complete
canonical entry (ID + kebab alias + definition + drift-baseline (AX-1
only) + severity-floor reference (AX-2 only) + finding example). AC #1
satisfied.

---

## 2. AC#2 / AC#3 — Finding examples present and pattern-matched to roadmap

**Command:**
```
grep -n "stale citation\|return-type mismatch" src/superclaude/agents/rf-qa-qualitative.md
```

**Output:**
```
532:- **AX-1 Drift** (kebab alias: `drift`) — … **Finding example (stale citation pattern):** task item cites `rf-qa-qualitative.md:528 — "Five Adversarial Axes" header`, but an upstream insertion shifted the header to line 530; the cited line number no longer matches current source. Annotate `axis: AX-1`.
533:- **AX-2 Contradictions** (kebab alias: `contradictions`) — … **Finding example (return-type mismatch pattern):** Section A states `build_axis_overlay()` returns `dict[str, Axis]`, while Section B's call site unpacks the same function's return value as `list[Axis]` (`for ax in build_axis_overlay(): ...`). Two artifacts assert incompatible return types for the same callable. Annotate `axis: AX-2` with severity ≥ IMPORTANT.
```

**Interpretation:**
- AX-1's `**Finding example (stale citation pattern):**` sub-phrase
  realises roadmap R-071's "A cited fact (file path, line number,
  signature, count, config value) no longer matches current source."
  The concrete example uses a `file:line` citation that drifted after
  an upstream insertion — a faithful realisation of the pattern.
- AX-2's `**Finding example (return-type mismatch pattern):**`
  sub-phrase realises roadmap R-072's "Two artifacts (or two sections)
  assert mutually incompatible facts about same subject." The concrete
  example uses `dict[str, Axis]` vs. `list[Axis]` for the same callable
  — an unambiguous return-type contradiction. Severity ≥ IMPORTANT
  annotation honours Critical Rule #6.

AC #2 and AC #3 both satisfied.

---

## 3. 15-item checklist body byte-stability (lines 538–573)

T04.01 / D-0041 §6 recorded the pre-edit body hash via section-level
hash and via full-file hash. T04.02 re-verifies the body slice
specifically:

**Command:**
```
sed -n '538,573p' src/superclaude/agents/rf-qa-qualitative.md | sha256sum
```

**Output (post-T04.02):**
```
28f8459a7bc9d2863bf3e3cf626a5cdfb623992d8db5bb8770505993a9086aaa  -
```

**Pre-T04.02 baseline (captured before the edit):**
```
28f8459a7bc9d2863bf3e3cf626a5cdfb623992d8db5bb8770505993a9086aaa  -
```

**Result:** Byte-identical. The 15-item checklist body is unchanged.
T04.08 / D-0048 will perform the formal end-of-phase byte-diff sweep,
but T04.02's contribution to that diff is verified zero here.

---

## 4. Severity-floor / Critical Rules block byte-stability (lines 786–795)

T04.10 / D-0049 will perform the formal end-of-phase byte-diff sweep
on the severity-floor block. T04.02 verifies its contribution is zero:

**Command:**
```
sed -n '786,795p' src/superclaude/agents/rf-qa-qualitative.md | sha256sum
```

**Output (post-T04.02):**
```
97ebf75cf2bafc04f72eda8f3c95bdc1dcc252ba852aa4387346522ea81f10ae  -
```

**Pre-T04.02 baseline (captured before the edit):**
```
97ebf75cf2bafc04f72eda8f3c95bdc1dcc252ba852aa4387346522ea81f10ae  -
```

**Result:** Byte-identical. The AX-2 bullet at line 533 cites
`Critical Rule #6` and "Severity floor: IMPORTANT" by reference — it
does not modify the floor itself.

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
e20183f61e09d703dc044651029305d3f4462ba4d023ca2c6e695c4f8548bcf9  src/superclaude/agents/rf-qa-qualitative.md
e20183f61e09d703dc044651029305d3f4462ba4d023ca2c6e695c4f8548bcf9  .claude/agents/rf-qa-qualitative.md
```

**Result:** Byte-identical mirror. `make verify-sync` PASS (§7 below).

Pre-T04.02 file hash was
`7a2712cfde048378cb937460723a9872ad9603d8ee786418d9436e8e8ca27723`
(per T04.01 / D-0041 §6); post-T04.02 hash is
`e20183f61e09d703dc044651029305d3f4462ba4d023ca2c6e695c4f8548bcf9` —
the only change is the AX-1 / AX-2 edit at lines 532–533.

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
header). T04.01's wrapper-ordering invariant remains intact.

---

## 7. Regression checks

### 7.1 PR-07 test suite

**Command:**
```
uv run pytest tests/skills/test_task_builder_merge.py::TestPR07AdversarialCategoryNaming -q
```

**Output:**
```
............                                                             [100%]
11 passed in 0.02s
```

All 11 PR-07 fixtures green:
- `test_rf_qa_qualitative_contains_axis[Drift|Contradictions|Omissions|Weakened criteria|Invented content]` — the title words survive the `**AX-N <Title>**` prefix transformation.
- `test_axes_are_overlay_not_replacement` — wrapper header + "overlay" / "sharpening overlay" preserved.
- `test_drift_baseline_requirement` — `drift-axis-inactive` and `BUILD_REQUEST.GOAL` preserved.
- `test_axis_annotation_required_in_items_reviewed` — `Axis (PR-07)` column header (line 701) untouched.
- `test_skill_references_5_axis_lens` — SKILL.md axis lens reference untouched (T04.02 did not edit SKILL.md).
- `test_invented_content_axis_is_evidence_bound` — Invented-content bullet (line 536) untouched.
- `test_weakened_axis_anti_inflation` — Weakened-criteria bullet (line 535) untouched.

### 7.2 Whole `test_task_builder_merge.py` suite

```
67 passed, 1 failed in 0.05s
```

The single failure is
`TestPR01ExecutionContextHeader::test_execution_context_uses_source_areas_not_paths`
asserting `"NEVER write specific" in skill_text`. This is a
pre-existing failure caused by missing PR-01 Execution Context Header
content in `task-builder/SKILL.md` — verified by re-running the test
under `git stash` (clean tree, no T04.02 changes), which produces the
identical failure. It is unrelated to T04.02 / AX-1 / AX-2 / FR-CONV.4
and is tracked under PR-01 / M2 follow-up work.

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
requires that the 5-axis overlay (PR-07) and the Inherited Structural
Verdict (PR-04, FR-CONV.3) compose cleanly: axes annotate findings on
items the consumer still runs, they do not substitute for an inherited
structural PASS, and an inherited PASS does not substitute for a
semantic check.

T04.02 preserves this composition because:

1. The wrapper paragraph at line 530 ("These axes are NOT new checks
   — they are adversarial lenses that sharpen the existing 15-item
   checklist.") is untouched.
2. The kebab annotation vocabulary at line 530
   (`axis: drift | contradictions | …`) is preserved verbatim; the new
   `(kebab alias: \`drift\`)` and `(kebab alias: \`contradictions\`)`
   parentheticals make the alias relationship explicit but introduce no
   new vocabulary outside the existing enumeration.
3. The AX-1 bullet retains the `drift-axis-inactive` fallback so
   GOAL-baseline-absent fixtures (T04.05 / T04.14 TEST-013) still
   trigger the correct annotation.
4. The AX-2 bullet retains the "Severity floor: IMPORTANT (cf. Critical
   Rule #6)" reference; T04.10 / D-0049 will hash-verify the floor
   itself.
5. No new code path, no new pipeline stage, no new agent file, no test
   modification — strictly markdown prose under the overlay-only (CB-3)
   constraint.

---

## 9. Pre / post hashes for downstream cross-reference

| Artifact | Pre-T04.02 hash | Post-T04.02 hash | Notes |
|---|---|---|---|
| `src/superclaude/agents/rf-qa-qualitative.md` (full file) | `7a2712cfde048378cb937460723a9872ad9603d8ee786418d9436e8e8ca27723` | `e20183f61e09d703dc044651029305d3f4462ba4d023ca2c6e695c4f8548bcf9` | only AX-1 / AX-2 edit at 532–533 |
| `.claude/agents/rf-qa-qualitative.md` (mirror) | `7a2712cfde048378cb937460723a9872ad9603d8ee786418d9436e8e8ca27723` | `e20183f61e09d703dc044651029305d3f4462ba4d023ca2c6e695c4f8548bcf9` | parity preserved |
| 15-item checklist body slice (538–573) | `28f8459a7bc9d2863bf3e3cf626a5cdfb623992d8db5bb8770505993a9086aaa` | `28f8459a7bc9d2863bf3e3cf626a5cdfb623992d8db5bb8770505993a9086aaa` | byte-identical |
| Severity-floor slice (786–795) | `97ebf75cf2bafc04f72eda8f3c95bdc1dcc252ba852aa4387346522ea81f10ae` | `97ebf75cf2bafc04f72eda8f3c95bdc1dcc252ba852aa4387346522ea81f10ae` | byte-identical |

T04.08 / D-0048 will reuse the 15-item body baseline; T04.10 / D-0049
will reuse the severity-floor baseline; both end-of-phase sweeps will
confirm zero contribution from T04.02–T04.04 plus any other M4 tasks.

---

## 10. Verdict

**T04.02 — PASS.**

All four acceptance criteria met. AX-1 (Drift) and AX-2
(Contradictions) canonical-axes entries authored at
`rf-qa-qualitative.md:532–533` with stale-citation and
return-type-mismatch finding examples respectively. 15-item checklist
body and severity-floor block byte-identical to T04.01 baseline.
src ↔ .claude parity preserved. PR-07 test suite green. INV-013
composition with inherited structural PASS clean.

T04.03 (AX-3 + AX-4) unblocked.
