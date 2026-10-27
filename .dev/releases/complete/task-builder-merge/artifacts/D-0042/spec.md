# D-0042 — T04.02 Spec: AX-1 Drift + AX-2 Contradictions Canonical-Axes Entries

**Task:** T04.02 (Phase 4 — M4 Five Adversarial Axes Overlay)
**Roadmap items:** R-071 (AX-1 Drift axis definition), R-072 (AX-2 Contradictions axis definition)
**Date:** 2026-05-17
**Status:** PASS
**Tier:** STANDARD
**Confidence:** [████████--] 88%

---

## 1. Scope

T04.02 lands the first two stable-ID entries (AX-1 Drift, AX-2
Contradictions) of the FR-CONV.4 canonical-axes block inside the
overlay-only Five Adversarial Axes subsection of
`src/superclaude/agents/rf-qa-qualitative.md`. Each entry consists of:

1. **Canonical ID** (`AX-1`, `AX-2`) prefixed onto the existing axis
   bullet header alongside the pre-existing kebab alias
   (`drift`, `contradictions`) used in the `axis: ...` annotation
   vocabulary at line 530.
2. **Definition** preserved from the PR-07 wrapper text (T04.01) and
   extended (AX-1 only) with the roadmap R-071 phrasing that the axis
   also fires when "a cited fact … no longer matches current source".
3. **Finding example** appended to each bullet:
   - AX-1: **stale citation pattern** — task item cites
     `rf-qa-qualitative.md:528` for the Five Adversarial Axes header,
     but an upstream insertion shifted the header to line 530.
   - AX-2: **return-type mismatch pattern** — Section A asserts
     `build_axis_overlay()` returns `dict[str, Axis]` while Section B's
     call site unpacks the return as `list[Axis]`.

T04.03 (AX-3 + AX-4) and T04.04 (AX-5) extend the same enumeration with
the remaining three entries; T04.07 / T04.11 finalise the Axis column
header (already present at line 701) so the per-row vocabulary
{AX-1..AX-5, none} ties back to this canonical-axes block.

## 2. Insertion site & wrapper anatomy

**File:** `src/superclaude/agents/rf-qa-qualitative.md`
**Block:** the existing FR-CONV.4 overlay region (528–536) landed by
T04.01 / D-0041 at PR-07 commit `0abf897`. T04.02 edits only lines
532–533 (the Drift + Contradictions bullets). Lines 528–531, 534–536
(other axes), and the 15-item checklist body at 538–573 are untouched.

| Line | Pre-edit (post-T04.01) | Post-edit (post-T04.02) |
|---|---|---|
| 528 | `#### Five Adversarial Axes (PR-07 — applied as a sharpening overlay across all 15 checks below)` | (unchanged) |
| 530 | overlay paragraph + annotation vocabulary | (unchanged) |
| 532 | `- **Drift** — …` | `- **AX-1 Drift** (kebab alias: `drift`) — … **Finding example (stale citation pattern):** …` |
| 533 | `- **Contradictions** — …` | `- **AX-2 Contradictions** (kebab alias: `contradictions`) — … **Finding example (return-type mismatch pattern):** …` |
| 534–536 | Omissions / Weakened criteria / Invented content bullets | (unchanged — touched by T04.03, T04.04) |
| 538 | `#### Checklist (15 items)` | (unchanged) |
| 538–573 | 15-item checklist body | (unchanged — byte-identical) |
| 786–795 | severity-floor / Critical Rules block | (unchanged — byte-identical) |

The new canonical ID prefix is structured as
`**AX-N <Title>** (kebab alias: \`<kebab>\`)` so that:

- `grep "AX-1\|AX-2" rf-qa-qualitative.md` returns one distinct match
  per axis (AC criterion).
- The kebab alias from the existing annotation vocabulary at line 530
  (`axis: drift | contradictions | …`) is preserved verbatim — no
  consumer who already annotates with `axis: drift` is broken.
- The existing test_rf_qa_qualitative_contains_axis fixture (which
  asserts capitalised axis names `Drift`, `Contradictions`, …) still
  passes because the title word is preserved inside the new
  `**AX-N <Title>**` form.

## 3. Definitions and roadmap mapping

### 3.1 AX-1 Drift (R-071)

**Roadmap R-071 definition** (verbatim):
> "A cited fact (file path, line number, signature, count, config
> value) no longer matches current source."

**Authored bullet text** (line 532, definition portion):
> "Has the task content drifted from BUILD_REQUEST.GOAL through
> paraphrasing, OR has a cited fact (file path, line number, signature,
> count, config value) drifted out of sync with current source? Look
> for paraphrases that substitute weaker verbs … or quietly narrowed
> scope."

The R-071 phrasing is folded in verbatim ("a cited fact (file path,
line number, signature, count, config value) … out of sync with current
source") alongside the pre-existing PR-07 GOAL-drift framing. The
**Drift-baseline requirement** (BUILD_REQUEST.GOAL verbatim capture +
`drift-axis-inactive` fallback) lands intact from T04.01.

**Finding example (stale citation pattern)** authored at line 532:
> "task item cites `rf-qa-qualitative.md:528 — \"Five Adversarial
> Axes\" header`, but an upstream insertion shifted the header to line
> 530; the cited line number no longer matches current source. Annotate
> `axis: AX-1`."

This is the canonical realisation of the R-071 stale-citation pattern.
It maps a real-world condition (line shift after an unrelated edit) to
the AX-1 lens without inventing additional content beyond what R-071
already describes (cited fact ↔ current source mismatch).

### 3.2 AX-2 Contradictions (R-072)

**Roadmap R-072 definition** (verbatim):
> "Two artifacts (or two sections) assert mutually incompatible facts
> about same subject."

**Authored bullet text** (line 533, definition portion):
> "Do two items in the task (or two artifacts, or two sections of one
> artifact) assert mutually incompatible facts about the same subject?
> One says \"use A\", another implies \"must not use A\"? Do
> frontmatter fields contradict body content? Do Acceptance Criteria
> contradict Open Questions? Severity floor: IMPORTANT (cf. Critical
> Rule #6)."

The R-072 phrasing ("two artifacts … or two sections … assert mutually
incompatible facts about the same subject") is woven into the existing
PR-07 bullet that already cited the "use A / must not use A",
frontmatter/body, and AC/Open-Questions contradiction sub-patterns.
**Severity floor: IMPORTANT (cf. Critical Rule #6)** is preserved
verbatim — T04.10 / D-0049 will hash-verify the Critical Rules block
at 786–795 remains byte-identical post-M4.

**Finding example (return-type mismatch pattern)** authored at line
533:
> "Section A states `build_axis_overlay()` returns `dict[str, Axis]`,
> while Section B's call site unpacks the same function's return value
> as `list[Axis]` (`for ax in build_axis_overlay(): …`). Two artifacts
> assert incompatible return types for the same callable. Annotate
> `axis: AX-2` with severity ≥ IMPORTANT."

This is the canonical realisation of the R-072 return-type-mismatch
pattern. It mirrors the existing test fixture name `build_axis_overlay`
(plausibly the future function for the overlay; not a fabricated
artifact). The annotation closes the loop on the severity floor:
"severity ≥ IMPORTANT" matches Critical Rule #6 (Contradictions are
IMPORTANT or CRITICAL by default).

## 4. Invariants enforced / preserved

| Invariant | Site | Guarantee |
|---|---|---|
| 15-item checklist body byte-stability | rf-qa-qualitative.md 538–573 | T04.02 edits are confined to lines 532–533; the 15-item body (538–573) is byte-identical pre/post. SHA-256 `28f8459a7bc9d2863bf3e3cf626a5cdfb623992d8db5bb8770505993a9086aaa` matches the T04.01 baseline. |
| Severity floor / Critical Rules byte-stability | rf-qa-qualitative.md 786–795 | T04.02 does not touch this range. SHA-256 `97ebf75cf2bafc04f72eda8f3c95bdc1dcc252ba852aa4387346522ea81f10ae` matches the T04.01 baseline. |
| INV-013 composition (axes annotate; do not substitute) | rf-qa-qualitative.md 530 | The "These axes are NOT new checks — they are adversarial lenses …" framing at line 530 is untouched. AX-1 / AX-2 prefixes are stable IDs on existing lenses, not new checks. |
| Annotation vocabulary back-compat | rf-qa-qualitative.md 530 | The kebab vocabulary `axis: drift | contradictions | …` at line 530 is untouched; the new bullets explicitly include `(kebab alias: \`drift\`)` / `(kebab alias: \`contradictions\`)` so consumers using the existing vocabulary continue to work. |
| Drift-baseline + drift-axis-inactive fallback | rf-qa-qualitative.md 532 | Preserved verbatim from T04.01; T04.05 / D-0045 will finalise the annotation emitter and TEST-013 fixture. |
| src ↔ .claude parity | both copies | Post-`make sync-dev`, SHA-256 `e20183f61e09d703dc044651029305d3f4462ba4d023ca2c6e695c4f8548bcf9` matches across `src/superclaude/agents/rf-qa-qualitative.md` and `.claude/agents/rf-qa-qualitative.md`. |
| Overlay-only (CB-3) | the whole edit | Edits are prose-only inside the markdown agent definition; no conditional code path, no new pipeline stage, no new agent file, no test code modified. |

## 5. Acceptance criteria mapping

| AC | Met by | Evidence |
|---|---|---|
| `grep -c "AX-1\|AX-2" src/superclaude/agents/rf-qa-qualitative.md` returns ≥ 2 distinct matches in the canonical-axes block | Two distinct bullets (lines 532, 533) carry the IDs | `D-0042/evidence.md` §1 |
| AX-1 definition cites stale citation pattern | Line 532 bullet ends with `**Finding example (stale citation pattern):** …` | `D-0042/evidence.md` §2 |
| AX-2 definition cites return-type mismatch pattern | Line 533 bullet ends with `**Finding example (return-type mismatch pattern):** …` | `D-0042/evidence.md` §2 |
| Both finding examples present | Two `**Finding example` sub-phrases — one per bullet | `D-0042/evidence.md` §2 |
| Evidence at `D-0042/evidence.md` | This file's sibling | `D-0042/evidence.md` exists |

## 6. Rollback path

As stated in roadmap row R-071 / R-072 (revertable by removing axis
overlay; 15-item checklist untouched). Mechanically for T04.02 alone:

1. Revert the `**AX-1 Drift**` and `**AX-2 Contradictions**` prefixes
   back to `**Drift**` and `**Contradictions**` on lines 532–533.
2. Delete the two **Finding example** sub-phrases appended to those
   bullets.
3. Run `make sync-dev` to mirror to `.claude/`.

The 15-item checklist body and severity-floor block are not touched, so
no further rollback is needed for them.

`FF_FIVE_ADVERSARIAL_AXES` is the logical feature-flag governing the
whole overlay; cleanup is consolidated in M7 (release-spec §8.3, M7
row). T04.02 inherits that governance from T04.01 / D-0041.

## 7. Cross-references

- Phase 4 task spec:
  `.dev/releases/current/task-builder-merge/phase-4-tasklist.md` T04.02
- Roadmap rows: R-071 (AX-1), R-072 (AX-2) in roadmap.md M4 table
- Release spec: release-spec.md §4.6 (sequencing), §8.3 (governance,
  M7 FF_FIVE_ADVERSARIAL_AXES row)
- T04.01 / D-0041 (wrapper landing) — entry gate for T04.02
- T04.03 / D-0043 (AX-3 + AX-4), T04.04 / D-0044 (AX-5) — extend this
  canonical-axes block with the remaining three entries
- T04.07 / D-0046, T04.11 / D-0050 — finalise the Axis column on the
  Items Reviewed table that consumes the `{AX-1..AX-5, none}`
  vocabulary defined here
- T04.10 / D-0049 — hash-verifies severity-floor block (786–795)
  preservation; T04.02 invariant check confirms the baseline
- INV-013 source:
  `.dev/tasks/done/TASK-TDD-20260514-121250/research/14-invariant-preservation.md:36`
