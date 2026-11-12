# Research Notes: bounded sweep chat-output exception revision

**Date:** 2026-11-09
**Status:** Complete
**Scenario:** A
**Depth Tier:** Standard (narrow change, with ledger/history and style/test integration)
**Track Count:** 1

## EXISTING_FILES

- Existing task package: TASK-RF-sweep-phase1-20261108-072653. Current item 7.10 (implement T138) stopped after the owner chose output-style option (b); 137 prior tasks complete. Baseline copies and manifest record exact task labels, ledger bytes and hashes under this revision's baseline/ folder.
- Task lines 1201-1213 define the original no-exception-only completion gate and revision stop. Lines 1971-1989 define future sweep skill creation, primitive tests and phase validation. Their current wording has no planned style-source change or exception regression test.
- DESIGN section 7.6 defines the skill's counts-and-path reply; section 7.5 defines the Python report. The latter must remain unaffected.
- Canonical style source: src/superclaude/output-styles/pragmatic.md. Installed style: ~/.claude/output-styles/pragmatic.md. Neither may be edited in this plan-only request. Existing style tests include tests/skills/test_review_severity_rule.py and test_implement_severity_static.py, plus installer/user-setup tests; researchers must determine the smallest suitable test surface.
- Existing BUILD-REQUEST.md and research-notes.md are historical source artifacts; preserve them. The existing executor's progress.md and item-map.tsv reside in .dev/implement/task-rf-sweep-phase1-202-c7ea3265/. Do not reset, stage or rewrite that ledger.

## PATTERNS_AND_CONVENTIONS

- Use task-builder's Updating an Existing Task File path: changed-area research, research QA, builder revision, validation. Historical gates are not reset or automatically accepted as reviews of the new revision.
- Use existing Template 02. Reports are stubbed then populated; source claims have citations and code/doc-verification tags. Read at most 150 lines per file call.
- Planning only: no source-style/test/skill edits, sync, implementation, commit, push, PR, merge or permission/config changes. Future implementation must be explicit in the revised plan, not executed now.
- Preserve all 355 task labels and enumeration order plus 137 completed item bodies and ledger bindings. No new earlier checkbox can shift later T numbers. Changes must be bounded to unfinished item bodies, additive revision metadata/notes and an explicitly scoped design addendum. Investigate a safe shape rather than assuming regeneration is safe.
- Helpers must run on a live Tier1b slot. Environment at revision start maps sonnet alias to claude-gw-tier1b[1m], with slots claude-sonnet-5-5, gpt-6.1-sol and muse-wonder-full-1.0. Agent recorded assistant metadata must confirm an actual match after completion; aliases/inheritance alone are not proof. No new Orca session/worktree. Auggie codebase-retrieval is unavailable in this session; use dedicated source reads/searches and record that limitation.

## GAPS_AND_QUESTIONS

- Find every style paragraph that restates the mandatory summary table and the smallest precise exception limited to `/sc:sweep`'s coordinator reply, not all coordinator conversations or Python report contents.
- Determine an unambiguous trigger that does not rely on a user-provided report claiming authority and preserves ordinary replies, error visibility and all other style rules.
- Find future tests and sync surfaces that pin this exception without editing installed mirrors now.
- Determine how to include future style edit/test work and resolve current item 7.10 without adding/removing/reordering any enumerable item or altering completed bodies.
- Identify all remaining plan/design references that assume option (a), including decision-gate QA and final diff/validation scope; propose only needed edits and preserve old evidence.

## RECOMMENDED_OUTPUTS

All new revision artifacts live under revisions/chat-output-exception-20261109-133150/ in the existing task package, without overwriting original research/QA/reflect artifacts. Targeted research: research/01-style-and-tests.md, research/02-executor-preservation.md, research/03-template-and-plan-integration.md. Then new research-gate reports, a revision BUILD-REQUEST.md, builder revision and delta/fidelity checks, structural/research-alignment/qualitative reports, and required PRE reflection artifacts. Present actual revised plan/check paths and disposition; execution remains separately authorized.

## SUGGESTED_PHASES

1. Style/patterns/tests researcher: canonical/installed style paragraphs, existing style tests, installer/sync destinations and planned sweep reply. Own report research/01-style-and-tests.md. Does not audit ledger/mapping or revise task.
2. Executor-preservation researcher: existing ledger, item-map/helper assumptions, baseline manifest and current-start snapshot. Identify safe revision/resume procedure preserving identities and completion evidence. Own report research/02-executor-preservation.md. Does not design style wording or template QA.
3. Template/integration researcher: Template 02 building instructions, current unfinished item7.10 and later plan consumers/QA/final diff scope. Map minimal future checklist edits and required checks without item insertion. Own report research/03-template-and-plan-integration.md. Does not audit executor internals or style tests.

All three run in parallel, report only; then the prescribed research quality gate precedes the builder. No researcher may alter the existing task/design/product sources.

## TEMPLATE_NOTES

Template 02 remains authoritative for the existing phased task. This is a revision, not a fresh build or executor switch. Preserve full-intensity existing gates; apply task-builder research and validation gates to the changed area. Standard research tier because the actual changed surface is narrow but ledger/history and style integration are consequential. Source requirements resolve to the existing design plus the direct owner's bounded revision authorization; PRE reflection must not be represented by the old PRE sign-off.

### Research sufficiency check (A.5)

Scope bounded, changed source areas identified, style/skill/test and executor integration mapped, three non-overlapping targeted assignments specified, Template 02 retained, existing templates/research inventoried, and intent ambiguity explicitly constrained. All seven sufficiency criteria are satisfied for changed-area research. This is not a claim that research findings or the revised plan have passed QA.

## AMBIGUITIES_FOR_USER

None preventing research: the owner directly selected "Add an exception" for the sweep skill chat reply and then "Authorize bounded revision" for plan revision/checking only. Keep the exception no broader than that choice. If exact future wording changes duties or extends to other coordinator messages, surface that as a separate decision rather than assume approval.
