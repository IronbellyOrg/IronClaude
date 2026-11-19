# Merge Log

## Metadata

- Base: Variant 1 (variant-1-original.md, opus-class alias, analyzer)
- Incorporated: Variant 2 (variant-2-original.md, haiku-class alias, qa); invariant-probe.md
- Executor: merge-executor
- Plan: /home/coder/workspaces/worktrees/IronClaude/issue-606/.dev/reflect/pre-makeInstallCoreS-20261119-tier2/adversarial/refactor-plan.md
- Output: /home/coder/workspaces/worktrees/IronClaude/issue-606/.dev/reflect/pre-makeInstallCoreS-20261119-tier2/merged-reflection-card.md
- Changes planned: 10; applied: 10; failed: 0; skipped: 0
- Status: success
- Timestamp: 2026-11-19

## Change Entries

### Change 1: F1 and F2 from minor to note
- Status: applied
- Before: F1 and F2 labelled "minor".
- After: both labelled "note", text kept, plus the statement that each is a wording point that cannot cause a wrong edit (symbol names next to each number; plan:36 measurable requirement).
- Provenance tag: Base (original, modified) on both bullets.
- Validation: both bullets keep their original Cites lines; no other bullet changed severity.

### Change 2: IndexError weakness as lead Finding
- Status: applied
- Before: IndexError mentioned only as an extension inside the F5 bullet and in Risks bullet 2.
- After: new first Finding, "minor", with plan:36, t2-checks.log:8-10, test:113 and test:134; stated as readability only. The F5 bullet lost the IndexError sentence (moved, not duplicated).
- Provenance tag: Base (original, modified); F5 also tagged Base (original, modified).
- Validation: the severity appears once (minor); the Risks bullet points back to the Finding.

### Change 3: Coverage verdict mapping and log citations
- Status: applied
- Before: five base bullets only.
- After: five base bullets kept, then four V2 mapping bullets with V2's absolute-path citations (source.md:1, task file :24-30 and :32-40, test :118-134, t2-checks.log:1-16).
- Provenance tag: Variant 2 (haiku-class alias, qa), Section Coverage verdict, Change #3.
- Validation: citations copied as V2 wrote them.

### Change 4: Provenance sentence for supplied evidence
- Status: applied
- Before: only the base's partial disclosure ("I could not run tests").
- After: one sentence stating the results are supplied evidence, corroborated by log agreement (351 then 352) and the predicted IndexError, and not independently repeated. Also V2's closing note kept in the footer.
- Provenance tag: Variant 2 (haiku-class alias, qa), Coverage verdict and closing note, Change #4.
- Validation: consistent with the base's "I could not run tests" line (see contradiction re-scan).

### Change 5: Risks counter-evidence from V2
- Status: applied
- Before: Risks held only the missed-risk items and base checks.
- After: appended "Checked and fine" with the three V2 cases and their citations.
- Provenance tag: Variant 2 (haiku-class alias, qa), Section Risks, Change #5.
- Validation: the three cases are framed as counter-evidence, not as proof of "no risk".

### Change 6: orca_worktree.py demoted to optional lead
- Status: applied
- Before: advisory note asserting the same flaw exists; Recommendation told the reader to open a backlog issue.
- After: note kept with [INFERRED], retitled "optional investigation lead", with the verified context (line 500 follows `shutil.copyfile` at line 499; no wrong-answer path found; double-call caller not checked). Backlog-issue action removed from the Recommendation. "exists" softened to "may exist" to match the lead status.
- Provenance tag: Base (original, modified); Recommendation also Base (original, modified).
- Validation: Risks and Open items refer to it as a lead only.

### Change 7: Non-empty PRINCIPLES.md qualifier
- Status: applied
- Before: "That works because PRINCIPLES.md is not empty."
- After: one appended sentence with the validity condition, line 1 text, no guard test, and the IndexError for an empty file.
- Provenance tag: Base (original, modified) on the F2 bullet.
- Validation: citation test:128 preserved.

### Change 8: Recommendation as one concrete action
- Status: applied
- Before: assert at line 134 only, plus a backlog issue.
- After: accept the plan; optional non-blocking assert before lines 134 and 113; one-site version named as minimum; verification command kept.
- Provenance tag: Base (original, modified).
- Validation: matches the Findings lead item and the Open items question.

### Change 9: Four MEDIUM probe findings
- Status: applied
- Before: none of INV-001, INV-002, INV-003, INV-008 present.
- After: labelled sub-block "Carried over from the invariant probe (not from either reviewer)" with one entry each and the cited lines.
- Provenance tag: invariant probe INV-001, INV-002, INV-003, INV-008 (one tag per entry).
- Validation: each entry labelled "from the invariant probe"; severities MEDIUM as in the probe; the severity table in the probe and the card agree.

### Change 10: LOW probe items and INV-010 caveat in Open items
- Status: applied
- Before: no Open items section.
- After: new "Open items" section: the four plan questions, INV-006, INV-012 and the INV-010 caveat.
- Provenance tag: Base (original, modified) for the section; invariant probe INV-006, INV-012, INV-010 per item.
- Validation: INV-012 stated as "no defect found".

## Post-Merge Validation

### Structural integrity
- Headings: Findings (H2), Carried over from the invariant probe (H3 under Findings), Coverage verdict (H2), Risks the first run missed (H2), Recommendation (H2), Open items (H2). No skipped levels. Order follows the plan outline (Findings, Coverage verdict, Risks, Recommendation, Open items).
- Provenance header: three required HTML comments present at the top. Every Finding bullet, Coverage block, Risks block, Recommendation and Open items block carries a Source tag.

### Internal references
- References checked: 7 ("see the lead Finding", "see the advisory Finding", "Recommendation" in Open items, "the four MEDIUM items carried over above", "see Findings" lines, "Cites" lines inside the card, the F1 to F5 labels).
- Resolved: 7. Broken: 0. The F1 to F5 labels point at the first run's list, outside the card, but each bullet restates its substance (same position as in the base).

### Contradiction re-scan
- New contradictions introduced by the merge: none.
- Tensions checked and found compatible:
  - "I could not run tests, so I have not confirmed that they pass" (base) next to the V2 log citation: reconciled by the provenance sentence (supplied evidence, not repeated).
  - INV-001 (a full cache could hide the old bug) next to F5 (negative control works): the control ran only this test, which INV-001 states; both can be true.
  - "Accept the plan as they are" next to the minor lead Finding: the follow-up is marked optional and non-blocking.
  - Severity of the sibling-file lead: "note, optional lead" in Findings, "optional investigation lead, not a defect" in Risks, "lead" in Open items. One severity throughout.
  - F1 and F2 now "note"; no other section assigns them minor.

## Summary

| Planned | Applied | Failed | Skipped |
|---|---|---|---|
| 10 | 10 | 0 | 0 |

Escalations to the orchestrator: none. Small wording adjustment inside Change 6 ("may exist" for "exists") to match the lead status; no content added beyond the plan and source files.
