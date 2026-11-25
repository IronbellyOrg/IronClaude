# Merge Log

## Metadata

- Base: Variant 3 (staged), `/home/coder/workspaces/IronClaude/.dev/troubleshoot/performance-ccsession-launch-takes-20-seconds-20261117185300/adversarial/adversarial/variant-3-original.md`
- Plan: `/home/coder/workspaces/IronClaude/.dev/troubleshoot/performance-ccsession-launch-takes-20-seconds-20261117185300/adversarial/adversarial/refactor-plan.md`
- Output: `/home/coder/workspaces/IronClaude/.dev/troubleshoot/performance-ccsession-launch-takes-20-seconds-20261117185300/adversarial/merged-output.md`
- Executor: merge-executor
- Changes applied: 9 of 9 (Changes #1 to #9, in order)
- Status: complete (Change #4 included as an optional item, as the plan says)
- Timestamp: 2026-11-17 (non-interactive run)

Structural edits to the base that the plan implies but does not list: Stage 1, Stage 2 and Stage 3 became `###` headings under "Proposed change" (the base had them inline); the last sentence of the base "Test plan" paragraph became its own "Success measure" section (the task names that section); the base "Risks" paragraph became a table (Change #7b).

## Change entries

### Change #1: name the helper and its place
- Status: applied
- Before: "Stage 2: a python3 helper called once per list (inside the `first` block ...)"
- After: "Add `scan_sessions.py` beside `retention.py` in `src/superclaude/skills/ccsession-tag/` (precedent: I:1674-1675 ...; install route: `install.sh:40` and `src/superclaude/cli/install_skill.py:52` copy the whole skill folder, so no manifest edit). It is called once per list (inside the `first` block ...)"
- Provenance: `<!-- Source: Base (original, modified) - helper named and placed per Change #1 -->`
- Validation: base wording of the record format, scan rules and fallback kept; the list of what the helper does was split into bullets with the same content.

### Change #2: one-record-per-line pairing as a stated risk and test
- Status: applied
- Before: Risks had no pairing risk; Test plan had no such fixture.
- After: risk-table row "One-record-per-input-uuid pairing breaks ... `validate_label` at `ccsession:315`"; Test plan line "topic names with spaces and with `%2F` escapes, and one topic file whose uuid has no transcript".
- Provenance: `<!-- Source: Variant 1, Section "Risks" (U-004) - merged per Change #2 -->`
- Validation: wording follows the plan; the `ccsession:315` citation is used as given by the plan and was not re-read from the file in this step.

### Change #3: invalid-UTF-8 output nuance of the locale fix
- Status: applied
- Before: no locale-output risk.
- After: risk-table row "Locale output change: the C locale restores the intended byte-wise match ... (worker knowledge of GNU grep, unverified)"; Test plan line "a cwd that holds invalid UTF-8 bytes".
- Provenance: `<!-- Source: Variant 2, C-005 - merged per Change #3 -->`
- Validation: the "unverified" label kept.

### Change #4: optional skip of work for rows that are later discarded
- Status: applied
- Before: Stage 1 ended with the bash 3.2 item.
- After: Stage 1 last item "Optional, measure first: rows classified `other` ... (about 0.9 s on assumptions ..., not derived exactly); keep only if the trace shows it and the output stays byte-identical".
- Provenance: `<!-- Source: Variant 2, Section "Proposed change" and Test plan (U-003) - merged per Change #4 -->`
- Validation: line citations written as I:1610-1627, I:1636 (plan used `ccsession:`; same file). I added one risk-table row for this item (Medium, reordering could change output) because the plan's Risk Summary rates it Medium; this is a small addition beyond the plan text.

### Change #5: state the file count of each stage
- Status: applied
- Before: only "more than 3 files at stage 2" in Risks.
- After: "File count: Stage 1 touches 2 files ... can ship as its own change" and "Stage 2 touches 3 to 4 files ..." placed at the end of each stage.
- Provenance: `<!-- Source: Variant 2, Section "Proposed change" (C-011) - merged per Change #5 -->`
- Validation: consistent with the risk row "More than 3 files at Stage 2".

### Change #6: add the open assumptions with measurement gates
- Status: applied
- Before: no such section.
- After: new `## Open assumptions and measurement gates` after Risks, four rows A-001, A-002, A-004, A-006 with the plan's gates.
- Provenance: `<!-- Source: Base (original, modified) - new section per Change #6; ... -->`
- Validation: the gate text uses only the numbers named in the plan (1.53 ms, 1.2 ms, 200 iterations, 2.8 s, 0.75 s, 1.95 s). The gate A-002 refers to "the 0.75 s prototype", which the base did not describe, so I added one Evidence line for it (0.75 s, 439 sessions, 554 MB, from tier1-observation.md and Variant 1) so the reference resolves. This line is outside the plan text.

### Change #7: repair the base's scored weaknesses
- Status: applied
- Before: `I:<n>` used with no definition; "Task 1 trace" and "A-core/A-full" not defined (A-core/A-full were not in the base text; they come from the plan); Risks a paragraph; no Out of scope.
- After: (a) `I:<n>` defined in the first sentence of the Problem statement; A-core/A-full defined in Evidence; Task 1 trace defined in Success measure. (b) Risks table with columns risk, probability, impact, mitigation covering helper drift, locale output change, python3 missing, `date --version` probe on BSD, timing window on larger stores (plus the base's unmeasured proxy and file-count risks). (c) new `## Out of scope` with five items.
- Provenance: Problem statement, Risks, Out of scope blocks tagged `Base (original, modified)`.
- Validation: probability and impact cells are qualitative labels, not numbers, and the document says so; no number was invented.

### Change #8: bring in the measured locale probe and relabel the derived estimates
- Status: applied
- Before: Evidence led with the system-architect card's derived figures; Success measure had no Stage 1 target.
- After: Evidence leads with the measured table (23.586, 24.663, 22.471 s vs 16.657, 16.244, 16.597 s; median gap 6.99 s; load 9.76 to 4.19, alternated) plus the source caveat; the remaining-time estimates (about 13.6 s, 11.6-14.1 s, about 14.6 s) are labelled "Derived, not executed, split unresolved in the debate (C-010)"; Success measure states "at or below the derived 14.6 s on the same store, to be confirmed by the same trace".
- Provenance: `<!-- Source: Base (original, modified) - measured locale probe leads ... per Change #8 ... -->`
- Validation: every figure matches tier1-observation.md (table rows 1-3, medians) or the variants; load given at source precision (plan rounded to 9.8 and 4.2).

### Change #9: resolve the printf/date contradiction explicitly
- Status: applied
- Before: Stage 1 said only "no ... `printf '%(...)T'`" inside the bash 3.2 item.
- After: separate item "Why `printf '%(...)T'` is not used for dates: bash 3.2 (macOS) lacks it (I:1690, 1823 ...); the `date --version` probe ... keep format_epoch's text and both platforms (I:1533-1537)".
- Provenance: `<!-- Source: Variant 3 (base), Stage 1 date item - modified per Change #9 -->`
- Validation: no text in the merged file recommends `printf '%(...)T'`; Variant 2's guarded printf was not incorporated.

## Post-Merge Validation

### Structural integrity
- Heading levels: `#` title, then `##` sections, then `###` for Stage 1, 2, 3 only. No gaps. Result: pass.
- Base section order kept: Problem statement, Proposed change, Evidence, Risks, then (new) Open assumptions and measurement gates, Out of scope, then Test plan, Success measure (split out of the base Test plan paragraph), Documented constraints to honor. The base order of its own sections is unchanged. Result: pass.
- "Documented constraints to honor": 10 bullets plus the lead-in line, copied verbatim from the base (diff by eye; no edits).

### Internal references
- Total: 27 lines carrying references to a stage, a gate (A-001/A-002/A-004/A-006), the Test plan or the open-assumptions section (counted with a search; a line with several references counts once).
- Resolved: 27
- Broken: 0
- Not counted: references to external files (`ccsession:315`, `install.sh:40`, `install_skill.py:52`, I:<n> lines) and to debate ids (C-010); they were taken from the plan and not re-read from the source files in this step.

### Contradiction re-scan
- New contradictions introduced: 0.
- Printf ban against added text: Stage 1 bans `printf '%(...)T'`; the Change #9 item, the Test plan (static test for bash 4 constructs) and the risk table agree. Variant 2's printf route is absent.
- Stage 1 optional item (Change #4) against "output stays byte-identical" constraint: consistent; it is gated on identical output.
- Stage 3 (optional in Proposed change) against Out of scope (Stage 3 unless trace shows more than about 2 s): consistent with the base condition.
- Out of scope "printing rows as built" against gate A-006: consistent (follow-up).
- Observation, not a contradiction: "parity A/B/C" (base wording, three views) and "A-core/A-full" use similar letters for different things; left as written.

## Summary

| Measure | Count |
|---|---|
| Planned | 9 |
| Applied | 9 |
| Failed | 0 |
| Skipped | 0 |

Additions outside the plan text, both small: one Evidence line for the 0.75 s prototype (so gate A-002 resolves) and one risk-table row for the optional Change #4 item.
