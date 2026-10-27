# D-0043 — T04.03 Spec: AX-3 Omissions + AX-4 Weakened-criteria Canonical-Axes Entries

**Task:** T04.03 (Phase 4 — M4 Five Adversarial Axes Overlay)
**Roadmap items:** R-073 (AX-3 Omissions axis definition), R-074 (AX-4 Weakened-criteria axis definition)
**Date:** 2026-05-17
**Status:** PASS
**Tier:** STANDARD
**Confidence:** [████████--] 88%

---

## 1. Scope

T04.03 lands the third and fourth stable-ID entries (AX-3 Omissions,
AX-4 Weakened criteria) of the FR-CONV.4 canonical-axes block inside
the overlay-only Five Adversarial Axes subsection of
`src/superclaude/agents/rf-qa-qualitative.md`. It is the direct
follow-on to T04.02 / D-0042 (AX-1 + AX-2) and continues the same
authoring pattern. Each entry consists of:

1. **Canonical ID** (`AX-3`, `AX-4`) prefixed onto the existing axis
   bullet header alongside the kebab alias (`omissions`,
   `weakened-criteria`) used in the `axis: ...` annotation vocabulary
   at line 530.
2. **Definition** preserved from the PR-07 wrapper text (T04.01) and
   extended with the roadmap R-073 / R-074 phrasing:
   - AX-3 adds the broader-scope sentence "is a required touchpoint,
     consumer, dependency, or step absent from the plan?" alongside
     the existing BUILD_REQUEST QA/Validation/Testing-requirements
     framing.
   - AX-4 adds the "softened to something unobservable or trivially
     satisfiable" framing alongside the existing "or"-split / "may"
     verb / optional-clause framing.
3. **Finding example** appended to each bullet:
   - AX-3: **missing-signature-update pattern** — an item passes a new
     `axis` kwarg to `build_axis_overlay()`, but no earlier item
     updates the function's signature to accept it (mirrors the
     T04.02 / D-0042 fixture callable name; same imagined function
     used in AX-2's return-type mismatch example).
   - AX-4: **trivially-passing-test pattern** — a verification step
     writes the 6-character placeholder `# Test` into a fixture file
     and asserts the file is non-empty / contains the substring
     `Test`; the assertion passes for the placeholder itself and
     exercises none of the feature under review (mirrors the TDD
     §8.5 row 940 canonical example).

T04.04 (AX-5) extends the same enumeration with the final entry;
T04.07 / T04.11 finalise the Axis column header so the per-row
vocabulary `{AX-1..AX-5, none}` ties back to this canonical-axes
block.

## 2. Insertion site & wrapper anatomy

**File:** `src/superclaude/agents/rf-qa-qualitative.md`
**Block:** the existing FR-CONV.4 overlay region (528–536) landed by
T04.01 / D-0041 at PR-07 commit `0abf897` and refined by T04.02 /
D-0042 at lines 532–533. T04.03 edits only lines 534–535 (the
Omissions + Weakened-criteria bullets). Lines 528–531, 532–533 (AX-1
/ AX-2), 536 (Invented content), and the 15-item checklist body at
538–573 are untouched.

| Line | Pre-edit (post-T04.02) | Post-edit (post-T04.03) |
|---|---|---|
| 528 | `#### Five Adversarial Axes (PR-07 — applied as a sharpening overlay across all 15 checks below)` | (unchanged) |
| 530 | overlay paragraph + annotation vocabulary | (unchanged) |
| 532 | `- **AX-1 Drift** (kebab alias: \`drift\`) — …` | (unchanged — T04.02 contribution) |
| 533 | `- **AX-2 Contradictions** (kebab alias: \`contradictions\`) — …` | (unchanged — T04.02 contribution) |
| 534 | `- **Omissions** — …` | `- **AX-3 Omissions** (kebab alias: \`omissions\`) — … **Finding example (missing-signature-update pattern):** …` |
| 535 | `- **Weakened criteria** — …` | `- **AX-4 Weakened criteria** (kebab alias: \`weakened-criteria\`) — … **Finding example (trivially-passing-test pattern):** …` |
| 536 | `- **Invented content** — …` | (unchanged — touched by T04.04) |
| 538 | `#### Checklist (15 items)` | (unchanged) |
| 538–573 | 15-item checklist body | (unchanged — byte-identical, hash `28f8459a…6aaa`) |
| 786–795 | severity-floor / Critical Rules block | (unchanged — byte-identical, hash `97ebf75c…f10ae`) |

The canonical ID prefix format established by T04.02 is preserved
verbatim: `**AX-N <Title>** (kebab alias: \`<kebab>\`)`. This gives:

- `grep "AX-3\|AX-4" rf-qa-qualitative.md` returns exactly one distinct
  match per axis (AC criterion #1).
- The kebab vocabulary from line 530 (`axis: drift | contradictions |
  omissions | weakened-criteria | invented-content`) is preserved
  verbatim — no consumer who already annotates with
  `axis: omissions` or `axis: weakened-criteria` is broken.
- The existing `test_rf_qa_qualitative_contains_axis` fixture (which
  asserts capitalised axis names `Omissions`, `Weakened criteria`,
  …) still passes because the title words are preserved inside the
  new `**AX-N <Title>**` form.
- The existing `test_weakened_axis_anti_inflation` fixture still
  passes because the "speculation about absent stronger phrasing
  does NOT count (anti-inflation alignment with rule #11)" clause is
  preserved verbatim.
- The existing `test_invented_content_axis_is_evidence_bound` fixture
  is unaffected because line 536 (Invented content bullet) is
  untouched; T04.04 / D-0044 lands the AX-5 prefix there.

## 3. Definitions and roadmap mapping

### 3.1 AX-3 Omissions (R-073)

**Roadmap R-073 definition** (verbatim from
`roadmap-opus-architect.md:222`):
> "A required touchpoint, consumer, dependency, or step absent from
> plan."

**Authored bullet text** (line 534, definition portion):
> "Are any BUILD_REQUEST `QA_GATE_REQUIREMENTS`,
> `VALIDATION_REQUIREMENTS`, or `TESTING_REQUIREMENTS` (SKILL.md
> rules #16/#17/#18) missing from the task as checklist items? Are
> any rf-qa FAIL items from the Inherited Structural Verdict left
> unaddressed? More broadly: is a required touchpoint, consumer,
> dependency, or step absent from the plan?"

The R-073 phrasing ("a required touchpoint, consumer, dependency, or
step absent from the plan") is folded in verbatim alongside the
pre-existing PR-07 BUILD_REQUEST-requirements framing and the
T03.16 / D-0039 Inherited-Structural-Verdict FAIL-item framing. The
PR-07 questioning style ("Are any…") is preserved so reviewers
internalise the lens, while the canonical R-073 statement is
explicitly threaded in for the broader semantic check.

**Finding example (missing-signature-update pattern)** authored at
line 534:
> "an item passes a new `axis` kwarg to `build_axis_overlay()`, but
> no earlier item updates the function's signature to accept it; the
> kwarg is supplied to a callable that never declared it, so the new
> argument is silently dropped or raises `TypeError` at runtime.
> Annotate `axis: AX-3`."

This realises R-073's "missing signature-update" pattern (per the
roadmap-opus-architect row) and aligns with TDD §8.5 row 939's
canonical example "Item adds a new kwarg but no item updates the
function signature to accept it." The callable `build_axis_overlay`
matches the symbol already used by AX-2's return-type-mismatch
example (D-0042 §3.2) — keeping the canonical-axes block coherent
under one running illustration rather than inventing new fictitious
callables for each axis.

### 3.2 AX-4 Weakened criteria (R-074)

**Roadmap R-074 definition** (verbatim from
`roadmap-opus-architect.md:223`):
> "Acceptance/verification condition softened to unobservable or
> trivially satisfiable."

**Authored bullet text** (line 535, definition portion):
> "Are acceptance criteria phrased more permissively than
> BUILD_REQUEST or the research findings warrant? Look for \"or\"
> splits, \"may\" verbs, optional clauses, conditional language (\"if
> applicable\") where the source materials are unconditional. Has an
> acceptance/verification condition been softened to something
> unobservable or trivially satisfiable? An item is \"weakened\" only
> when BUILD_REQUEST or research evidence demands stronger phrasing
> — speculation about absent stronger phrasing does NOT count
> (anti-inflation alignment with rule #11)."

The R-074 phrasing ("softened to something unobservable or trivially
satisfiable") is woven into the existing PR-07 bullet that already
cited the "or"-split / "may"-verb / optional-clause sub-patterns and
the anti-inflation rule #11 alignment. The anti-inflation clause is
preserved verbatim — `test_weakened_axis_anti_inflation` still
passes.

**Finding example (trivially-passing-test pattern)** authored at
line 535:
> "a verification step writes the 6-character placeholder `# Test`
> into a fixture file and then asserts that the file is non-empty
> (or contains the substring `Test`); the assertion passes for the
> placeholder itself and exercises none of the feature under
> review. Annotate `axis: AX-4`."

This realises R-074's "trivially-passing test" pattern (per the
roadmap-opus-architect row) and aligns with TDD §8.5 row 940's
canonical example "Verification reads `# Test` into a file and
asserts on the 6-char placeholder." The example is also referenced
in the existing 15-item checklist item #7 (`Test validity`) at line
558 ("A test that writes `# Test` to a file and asserts against
that 6-character placeholder…"), so the canonical AX-4 example
explicitly points reviewers at the checklist item it sharpens —
reinforcing INV-013 (axes annotate; do not substitute).

## 4. Invariants enforced / preserved

| Invariant | Site | Guarantee |
|---|---|---|
| 15-item checklist body byte-stability | rf-qa-qualitative.md 538–573 | T04.03 edits are confined to lines 534–535; the 15-item body (538–573) is byte-identical pre/post. SHA-256 `28f8459a7bc9d2863bf3e3cf626a5cdfb623992d8db5bb8770505993a9086aaa` matches the T04.01 / T04.02 baseline. |
| Severity floor / Critical Rules byte-stability | rf-qa-qualitative.md 786–795 | T04.03 does not touch this range. SHA-256 `97ebf75cf2bafc04f72eda8f3c95bdc1dcc252ba852aa4387346522ea81f10ae` matches the T04.01 / T04.02 baseline. |
| INV-013 composition (axes annotate; do not substitute) | rf-qa-qualitative.md 530 | The "These axes are NOT new checks — they are adversarial lenses …" framing at line 530 is untouched. AX-3 / AX-4 prefixes are stable IDs on existing lenses; AX-4's finding example explicitly references checklist item #7 (`Test validity`) at line 558 to reinforce the annotate-not-substitute relationship. |
| Annotation vocabulary back-compat | rf-qa-qualitative.md 530 | The kebab vocabulary `axis: drift | contradictions | omissions | weakened-criteria | invented-content` at line 530 is untouched; the new bullets explicitly include `(kebab alias: \`omissions\`)` / `(kebab alias: \`weakened-criteria\`)` so consumers using the existing vocabulary continue to work. |
| Anti-inflation rule #11 alignment (AX-4) | rf-qa-qualitative.md 535 | The "An item is \"weakened\" only when BUILD_REQUEST or research evidence demands stronger phrasing — speculation about absent stronger phrasing does NOT count (anti-inflation alignment with rule #11)" clause is preserved verbatim. `test_weakened_axis_anti_inflation` still passes. |
| Inherited-Structural-Verdict FAIL-item carry-over (AX-3) | rf-qa-qualitative.md 534 | The "Are any rf-qa FAIL items from the Inherited Structural Verdict left unaddressed?" clause (T03.16 / D-0039 contribution to AX-3's lens) is preserved verbatim. |
| src ↔ .claude parity | both copies | Post-`make sync-dev`, SHA-256 `b5c808e1115af0a16c8bdabfa5e5ddc105d0ae0b657bb6c197a75295b5740de4` matches across `src/superclaude/agents/rf-qa-qualitative.md` and `.claude/agents/rf-qa-qualitative.md`. |
| Overlay-only (CB-3) | the whole edit | Edits are prose-only inside the markdown agent definition; no conditional code path, no new pipeline stage, no new agent file, no test code modified. |

## 5. Acceptance criteria mapping

| AC | Met by | Evidence |
|---|---|---|
| `grep -c "AX-3\|AX-4" src/superclaude/agents/rf-qa-qualitative.md` returns ≥ 2 distinct matches in the canonical-axes block | Two distinct bullets (lines 534, 535) carry the IDs | `D-0043/evidence.md` §1 |
| AX-3 definition cites missing-signature-update pattern | Line 534 bullet ends with `**Finding example (missing-signature-update pattern):** …` | `D-0043/evidence.md` §2 |
| AX-4 definition cites trivially-passing-test pattern | Line 535 bullet ends with `**Finding example (trivially-passing-test pattern):** …` | `D-0043/evidence.md` §2 |
| Both finding examples present | Two `**Finding example` sub-phrases — one per bullet | `D-0043/evidence.md` §2 |
| Evidence at `D-0043/evidence.md` | This file's sibling | `D-0043/evidence.md` exists |

## 6. Rollback path

As stated in roadmap rows R-073 / R-074 (revertable by removing axis
overlay; 15-item checklist untouched). Mechanically for T04.03 alone:

1. Revert the `**AX-3 Omissions**` and `**AX-4 Weakened criteria**`
   prefixes back to `**Omissions**` and `**Weakened criteria**` on
   lines 534–535.
2. Delete the two **Finding example** sub-phrases appended to those
   bullets.
3. Remove the two clauses added from R-073 ("More broadly: is a
   required touchpoint…absent from the plan?") and R-074 ("Has an
   acceptance/verification condition been softened to something
   unobservable or trivially satisfiable?").
4. Run `make sync-dev` to mirror to `.claude/`.

The 15-item checklist body and severity-floor block are not touched,
so no further rollback is needed for them. T04.02's AX-1 / AX-2
edits are independent and remain in place.

`FF_FIVE_ADVERSARIAL_AXES` is the logical feature-flag governing the
whole overlay; cleanup is consolidated in M7 (release-spec §8.3, M7
row). T04.03 inherits that governance from T04.01 / D-0041.

## 7. Cross-references

- Phase 4 task spec:
  `.dev/releases/current/task-builder-merge/phase-4-tasklist.md` T04.03
- Roadmap rows: R-073 (AX-3), R-074 (AX-4) in
  `roadmap-opus-architect.md:222–223` and `roadmap.compressed.md:246–247`
- TDD canonical examples: §8.5 rows 939–940 in
  `TDD_TASK_BUILDER_CONVERGENCE.md`
- Release spec: release-spec.md §4.6 (sequencing), §8.3 (governance,
  M7 FF_FIVE_ADVERSARIAL_AXES row)
- T04.02 / D-0042 (AX-1 + AX-2) — sibling axis entry pattern reused
- T04.04 / D-0044 (AX-5) — extends this canonical-axes block with the
  final entry at line 536
- T04.07 / D-0046, T04.11 / D-0050 — finalise the Axis column on the
  Items Reviewed table that consumes the `{AX-1..AX-5, none}`
  vocabulary defined here
- T04.10 / D-0049 — hash-verifies severity-floor block (786–795)
  preservation; T04.03 invariant check confirms the baseline
- INV-013 source:
  `.dev/tasks/done/TASK-TDD-20260514-121250/research/14-invariant-preservation.md:36`
