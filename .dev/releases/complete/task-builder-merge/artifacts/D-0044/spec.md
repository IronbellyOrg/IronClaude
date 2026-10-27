# D-0044 — T04.04 Spec: AX-5 Invented-content Canonical-Axes Entry

**Task:** T04.04 (Phase 4 — M4 Five Adversarial Axes Overlay)
**Roadmap item:** R-075 (AX-5 Invented-content axis definition)
**Date:** 2026-05-17
**Status:** PASS
**Tier:** STANDARD
**Confidence:** [█████████-] 90%

---

## 1. Scope

T04.04 lands the fifth and final stable-ID entry (AX-5 Invented
content) of the FR-CONV.4 canonical-axes block inside the
overlay-only Five Adversarial Axes subsection of
`src/superclaude/agents/rf-qa-qualitative.md`. It is the direct
follow-on to T04.03 / D-0043 (AX-3 + AX-4) and completes the same
authoring pattern established by T04.02 / D-0042 (AX-1 + AX-2) and
extended by T04.03 / D-0043 (AX-3 + AX-4). The entry consists of:

1. **Canonical ID** (`AX-5`) prefixed onto the existing axis bullet
   header alongside the kebab alias (`invented-content`) used in the
   `axis: ...` annotation vocabulary at line 530.
2. **Definition** preserved from the PR-07 wrapper text (T04.01) and
   extended with the roadmap R-075 phrasing: "does the artifact
   introduce a requirement, feature, or capability not present in
   its upstream source (BUILD_REQUEST, PRD, TDD, research evidence)?"
   alongside the existing PR-07 "files, modules, interfaces, or
   commands NOT present in `research/*.md`" framing.
3. **Finding example** appended to the bullet:
   - AX-5: **scope-inflation pattern** — the task introduces a
     Redis caching layer in front of `build_axis_overlay()` to
     memoise per-task results, but no upstream source mentions
     caching, memoisation, or Redis (mirrors TDD §8.5 row 941's
     canonical "TDD adds a caching layer the PRD never specified"
     example; reuses the `build_axis_overlay` callable already cited
     in AX-2 / AX-3 finding examples so the canonical-axes block
     runs on one coherent illustration).

T04.04 closes the canonical-axes block for M4; T04.05 lands the
`none` sentinel + `drift-axis-inactive` annotation rules that
consume the `{AX-1..AX-5, none}` vocabulary defined by
D-0042 / D-0043 / D-0044. T04.07 / T04.11 finalise the Axis column
header on the Items Reviewed table that carries those values per
row.

## 2. Insertion site & wrapper anatomy

**File:** `src/superclaude/agents/rf-qa-qualitative.md`
**Block:** the existing FR-CONV.4 overlay region (528–536) landed by
T04.01 / D-0041 at PR-07 commit, refined by T04.02 / D-0042 (lines
532–533) and T04.03 / D-0043 (lines 534–535). T04.04 edits only line
536 (the Invented-content bullet). Lines 528–531, 532–535
(AX-1..AX-4), and the 15-item checklist body at 538–573 are
untouched.

| Line | Pre-edit (post-T04.03) | Post-edit (post-T04.04) |
|---|---|---|
| 528 | `#### Five Adversarial Axes (PR-07 — applied as a sharpening overlay across all 15 checks below)` | (unchanged) |
| 530 | overlay paragraph + annotation vocabulary | (unchanged) |
| 532 | `- **AX-1 Drift** (kebab alias: \`drift\`) — …` | (unchanged — T04.02 contribution) |
| 533 | `- **AX-2 Contradictions** (kebab alias: \`contradictions\`) — …` | (unchanged — T04.02 contribution) |
| 534 | `- **AX-3 Omissions** (kebab alias: \`omissions\`) — …` | (unchanged — T04.03 contribution) |
| 535 | `- **AX-4 Weakened criteria** (kebab alias: \`weakened-criteria\`) — …` | (unchanged — T04.03 contribution) |
| 536 | `- **Invented content** — …` | `- **AX-5 Invented content** (kebab alias: \`invented-content\`) — … **Finding example (scope-inflation pattern):** …` |
| 538 | `#### Checklist (15 items)` | (unchanged) |
| 538–573 | 15-item checklist body | (unchanged — byte-identical, hash `28f8459a…6aaa`) |
| 786–795 | severity-floor / Critical Rules block | (unchanged — byte-identical, hash `97ebf75c…f10ae`) |

The canonical ID prefix format established by T04.02 and reused by
T04.03 is preserved verbatim: `**AX-N <Title>** (kebab alias:
\`<kebab>\`)`. This gives:

- `grep "AX-5" rf-qa-qualitative.md` returns exactly one distinct
  match in the canonical-axes block (AC criterion #1).
- The kebab vocabulary from line 530 (`axis: drift | contradictions |
  omissions | weakened-criteria | invented-content`) is preserved
  verbatim — no consumer who already annotates with
  `axis: invented-content` is broken.
- The existing `test_rf_qa_qualitative_contains_axis` fixture (which
  asserts capitalised axis name `Invented content`) still passes
  because the title words are preserved inside the new `**AX-5
  Invented content**` form.
- The existing `test_invented_content_axis_is_evidence_bound`
  fixture still passes because the "research/*.md" / "research
  files" phrasing is preserved verbatim, plus the new "evidence-bound
  — it requires you to read the research files" clause is retained
  in full.

## 3. Definition and roadmap mapping

### 3.1 AX-5 Invented content (R-075)

**Roadmap R-075 definition** (verbatim from
`roadmap-opus-architect.md:224`):
> "Artifact introduces requirement/feature/capability not present in
> upstream source."

**Authored bullet text** (line 536, definition portion):
> "Does the task reference files, modules, interfaces, or commands
> NOT present in `research/*.md` evidence files or the actual
> codebase? Cross-check every named artifact against the research
> files and the filesystem. More broadly: does the artifact
> introduce a requirement, feature, or capability not present in its
> upstream source (BUILD_REQUEST, PRD, TDD, research evidence)? This
> axis is itself evidence-bound — it requires you to read the
> research files, not just assert \"I don't see it documented.\""

The R-075 phrasing ("introduces a requirement, feature, or
capability not present in upstream source") is folded in verbatim as
the broader-scope clause, alongside the pre-existing PR-07
file/module/interface/command framing and the canonical "this axis
is itself evidence-bound" clause that protects the
`test_invented_content_axis_is_evidence_bound` fixture's assertion
on `research/*.md` / "research files". The PR-07 questioning style
("Does the task reference…") is preserved so reviewers internalise
the lens, while the canonical R-075 statement is explicitly threaded
in for the broader semantic check.

**Finding example (scope-inflation pattern)** authored at line 536:
> "the task introduces a Redis caching layer in front of
> `build_axis_overlay()` to memoise per-task results, but no
> upstream source — BUILD_REQUEST, PRD §2 FR-CONV.4, TDD §8.5, or
> `research/*.md` — mentions caching, memoisation, or Redis; the
> caching layer is an invention that inflates scope beyond what was
> authorised (mirrors TDD §8.5 row 941's canonical \"TDD adds a
> caching layer the PRD never specified\" example). Annotate `axis:
> AX-5`."

This realises R-075's "scope-inflation" pattern (per the
roadmap-opus-architect row 224 AC column: "finding example shows
scope-inflation pattern") and aligns with TDD §8.5 row 941's
canonical example "TDD adds a caching layer the PRD never
specified." The callable `build_axis_overlay` matches the symbol
already used by AX-2's return-type-mismatch example (D-0042 §3.2)
and AX-3's missing-signature-update example (D-0043 §3.1) — keeping
the canonical-axes block coherent under one running illustration
rather than inventing new fictitious callables for each axis. The
example explicitly enumerates the upstream-source list
(BUILD_REQUEST / PRD / TDD / research) to make the cross-check
discipline concrete.

## 4. Invariants enforced / preserved

| Invariant | Site | Guarantee |
|---|---|---|
| 15-item checklist body byte-stability | rf-qa-qualitative.md 538–573 | T04.04 edits are confined to line 536; the 15-item body (538–573) is byte-identical pre/post. SHA-256 `28f8459a7bc9d2863bf3e3cf626a5cdfb623992d8db5bb8770505993a9086aaa` matches the T04.01 / T04.02 / T04.03 baseline. |
| Severity floor / Critical Rules byte-stability | rf-qa-qualitative.md 786–795 | T04.04 does not touch this range. SHA-256 `97ebf75cf2bafc04f72eda8f3c95bdc1dcc252ba852aa4387346522ea81f10ae` matches the T04.01 / T04.02 / T04.03 baseline. |
| INV-013 composition (axes annotate; do not substitute) | rf-qa-qualitative.md 530 | The "These axes are NOT new checks — they are adversarial lenses …" framing at line 530 is untouched. AX-5 prefix is a stable ID on the existing lens. |
| Annotation vocabulary back-compat | rf-qa-qualitative.md 530 | The kebab vocabulary `axis: drift | contradictions | omissions | weakened-criteria | invented-content` at line 530 is untouched; the new bullet explicitly includes `(kebab alias: \`invented-content\`)` so consumers using the existing vocabulary continue to work. |
| Evidence-bound clause (AX-5) | rf-qa-qualitative.md 536 | The "This axis is itself evidence-bound — it requires you to read the research files, not just assert \"I don't see it documented.\"" clause is preserved verbatim. `test_invented_content_axis_is_evidence_bound` still passes. |
| Anti-inflation rule #11 alignment (AX-4) | rf-qa-qualitative.md 535 | The AX-4 anti-inflation clause is untouched (T04.03 contribution). `test_weakened_axis_anti_inflation` still passes. |
| src ↔ .claude parity | both copies | Post-`make sync-dev`, SHA-256 `926ff48f9da3c555af681a42644256dea2e0739bd38ad22d4cb115c1139c0cbf` matches across `src/superclaude/agents/rf-qa-qualitative.md` and `.claude/agents/rf-qa-qualitative.md`. |
| Overlay-only (CB-3) | the whole edit | Edits are prose-only inside the markdown agent definition; no conditional code path, no new pipeline stage, no new agent file, no test code modified. |

## 5. Acceptance criteria mapping

| AC | Met by | Evidence |
|---|---|---|
| `grep -n "AX-5" src/superclaude/agents/rf-qa-qualitative.md` returns ≥ 1 match in the canonical-axes block | Line 536 bullet carries the `AX-5` prefix | `D-0044/evidence.md` §1 |
| AX-5 definition cites scope inflation pattern | Line 536 bullet ends with `**Finding example (scope-inflation pattern):** …` | `D-0044/evidence.md` §2 |
| Finding example present and aligned with FR-CONV.4 spec | `**Finding example` sub-phrase on line 536 reuses `build_axis_overlay` from AX-2 / AX-3 and mirrors TDD §8.5 row 941 | `D-0044/evidence.md` §2 |
| Evidence at `D-0044/evidence.md` | This file's sibling | `D-0044/evidence.md` exists |

## 6. Rollback path

As stated in roadmap row R-075 (revertable by removing axis overlay;
15-item checklist untouched). Mechanically for T04.04 alone:

1. Revert the `**AX-5 Invented content** (kebab alias:
   \`invented-content\`)` prefix back to `**Invented content**` on
   line 536.
2. Delete the **Finding example (scope-inflation pattern)** sub-phrase
   and the `Annotate \`axis: AX-5\`.` trailing directive.
3. Remove the broader-scope sentence "More broadly: does the
   artifact introduce a requirement, feature, or capability not
   present in its upstream source (BUILD_REQUEST, PRD, TDD, research
   evidence)?" added from R-075.
4. Run `make sync-dev` to mirror to `.claude/`.

The 15-item checklist body and severity-floor block are not touched,
so no further rollback is needed for them. T04.02's AX-1 / AX-2 and
T04.03's AX-3 / AX-4 edits are independent and remain in place.

`FF_FIVE_ADVERSARIAL_AXES` is the logical feature-flag governing
the whole overlay; cleanup is consolidated in M7 (release-spec
§8.3, M7 row). T04.04 inherits that governance from T04.01 /
D-0041.

## 7. Cross-references

- Phase 4 task spec:
  `.dev/releases/current/task-builder-merge/phase-4-tasklist.md` T04.04
- Roadmap row: R-075 (AX-5) in
  `roadmap-opus-architect.md:224` and `roadmap.compressed.md:248`
- TDD canonical example: §8.5 row 941 in
  `TDD_TASK_BUILDER_CONVERGENCE.md` ("TDD adds a caching layer the
  PRD never specified")
- Release spec: release-spec.md §4.6 (sequencing), §8.3 (governance,
  M7 FF_FIVE_ADVERSARIAL_AXES row)
- T04.02 / D-0042 (AX-1 + AX-2) — sibling axis entry pattern reused
- T04.03 / D-0043 (AX-3 + AX-4) — sibling axis entry pattern reused
- T04.05 / D-0045 — wires `none` sentinel + `drift-axis-inactive`
  annotation rules that consume the `{AX-1..AX-5, none}` vocabulary
  closed by this task
- T04.07 / D-0046, T04.11 / D-0050 — finalise the Axis column on the
  Items Reviewed table that consumes the `{AX-1..AX-5, none}`
  vocabulary defined here
- T04.10 / D-0049 — hash-verifies severity-floor block (786–795)
  preservation; T04.04 invariant check confirms the baseline
- INV-013 source:
  `.dev/tasks/done/TASK-TDD-20260514-121250/research/14-invariant-preservation.md:36`
