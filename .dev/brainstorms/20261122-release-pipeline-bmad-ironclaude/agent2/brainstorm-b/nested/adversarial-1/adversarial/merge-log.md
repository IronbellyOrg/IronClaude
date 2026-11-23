# Merge Log

## Metadata

- Base: Variant 1 (opus:architect)
- Executor: the orchestrating session, inline. The protocol names a dedicated `merge-executor` agent; it was not dispatched in this run (deviation, recorded here and in the return contract as `fallback_mode: true`)
- Changes applied: 17 of 17 planned
- Status: complete with warnings (see Post-Merge Validation)
- Timestamp: 2026-11-22T21:25:00Z
- Output: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261122-release-pipeline-bmad-ironclaude/agent2/brainstorm-b/nested/adversarial-1/merged-output.md`

## Changes Applied

| Change | Status | Before (base) | After (merged) | Provenance tag in merged output | Validation |
|--------|--------|---------------|----------------|----------------------------------|------------|
| CH-1 numbered headings | applied | Unnumbered `##` headings | `## 1.` to `## 10.` | Source comment on the title | Headings contiguous 1 to 10 |
| CH-2 new-path skip in T1 and T2 | applied | T1 fires on any missing named path | Named paths exclude `(new)` and new-file lists | Source comment on section 4 | T1 and T2 both refer to "named paths" as defined |
| CH-3 T5 thresholds | applied | More than 6 criteria or tasks | More than 8 criteria or more than 12 tasks | Section 4 | Cost section uses the same T5 for the complex class |
| CH-4 T4 regex | applied | Broad regex incl. database, permission, encrypt | Whole-word list incl. storage and protocol | Section 4 | List appears once |
| CH-5 shape stop | applied | No malformed-story gate (T7 only) | New section 3; step 1 of the default arm applies it | Source comment on section 3 | Referenced from section 2 step 1 and risk 12 |
| CH-6 cost rebuild | applied | One table, no formulas, 31 vs 30 | Counting rule, formulas, arm-split table, arithmetic rechecked | Source comment on section 5 | Recomputed: see below |
| CH-7 source copy | applied | None | `<D>/source-story.md` in step 1 and R7 | Sections 2 and 6 | Named in R1 and R7 |
| CH-8 ac-map as data | applied | Text match only | R4 writes `ac-map.md` with predicted ids | Section 6 R4 | Referenced by R9 |
| CH-9 completion closure | applied | None | R9 | Section 6 R9 | R9 refers to R4 and the ledger |
| CH-10 re-check | applied | Checks at steps 3 and 5 | R8 after every reviser pass and the repair | Section 6 R8 | Step 5 of the alternate arm runs `ac-map-check` |
| CH-11 provenance tag | applied | None | R10, `[IC]` plus source file | Section 6 R10 | Used by R6 and step 4 of the alternate arm |
| CH-12 trial plan | applied | Prose plus decision rules | M1 to M4, 12 stories, merged non-overlapping rules | Source comment on section 7 | Decision rules checked for overlap |
| CH-13 flags | applied | `--report-dir` on brainstorm and adversarial | `--output` there; `--report-dir` on panel and workflow | Section 2 closing paragraph | Read against each command's Unattended mode section |
| CH-14 acronyms, guard, likelihood | applied | Missing | Terms line in section 1; zero-criteria guard in section 3; likelihood column in section 8 | Sections 1, 3, 8 | |
| CH-15 accuracy-check candidate | applied | None | Candidate, not in the frozen list (end of section 4, section 7) | Section 4 | Not counted as a trigger |
| CH-16 coordinator dependency | applied | Implicit | Defined in section 1; R2, R5; risk 11 | Sections 1, 6, 8 | |
| CH-17 workflow depth by size | applied | quick default | quick if simple, standard if medium | Section 2 step 4 | Matches `chains.md` rows |

## Post-Merge Validation

- **Structural integrity:** pass. One H1, ten contiguous H2 sections, no skipped heading levels, no orphan subsections.
- **Internal references:** every section, rule and trigger reference was checked by reading (not counted by a script); none is broken. Examples checked: "section 10" (exists), "rule R5" in step 6 (R5 is the conflict rule), "T1 to T5 and T7" at the gate (T6 read from the panel report), "R1, R2, R3, R7" at step 3 (all defined).
- **Contradiction re-scan:** 0 new contradictions. One earlier inconsistency was fixed in the merge: the base's option 3 complex cell (31) and option 2 complex cell (30) are replaced by a rebuilt table whose cells were recomputed (calls: panel 2R - 1, workflow 3, brainstorm 2P + 4 (+ P + 1 at standard depth), compare 4: simple 16, medium 18, complex 14 + 4 + 5 + 3 = 26; default arm 4, 6, 8; ratios 4.0, 3.0, 3.25).
- **Style check:** no em dashes or en dashes in any file written by this run (searched).
- **Warnings:** (1) the merge ran inline, not through a merge agent; (2) the cost table is an ESTIMATE built from protocol text, with one measured data point (this run); (3) convergence 65.4% is below the 75% threshold, so nine points were adjudicated by the orchestrator, not agreed by both advocates; (4) the claim that `bmad-create-story` reads recent commits and the previous story's notes comes from the topic file, not from a line read in the skill (only the skill's role and purpose lines were read); (5) the sub-agent calls of this adversarial run reported about 671K tokens against the brainstorm's Wave 2B estimate of about 208K, which is above the protocol's 1.25 times hard-kill threshold (about 260K); the threshold was not enforced during the run and the run was not aborted, so the token budget guard did not work as written.

## Summary

| Planned | Applied | Failed | Skipped |
|---------|---------|--------|---------|
| 17 | 17 | 0 | 0 |
