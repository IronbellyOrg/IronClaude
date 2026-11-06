# Merge Log

## Metadata

- Base: Variant 2 (sonnet:analyzer), `variant-2-sonnet-analyzer.md`
- Incorporated from: Variant 1 (opus:scribe), `variant-1-opus-scribe.md`
- Plan: `refactor-plan.md` (5 planned changes, 5 rejected changes)
- Executor: merge-executor agent
- Output: `../merged-output.md`
- Changes applied: 5 of 5 (plus 3 consequential consistency edits, listed under the change that caused them)
- Status: success
- Timestamp: 2026-11-05T20:03:38Z

Facts re-checked before use: `src/superclaude/commands/reflect.md:101` (`--output` default `.dev/reflect/<mode>-<slug>-<ts>/`), `src/superclaude/commands/brainstorm.md:62` (default `.dev/brainstorms/<ts>-<slug>/`), `.dev/README.md:47` (`TASK-WF-<subject>-<YYYYMMDD>-<HHMMSS>`, camelCase at most 16), `.dev/README.md:54` (`progress.md` inside the package), `.dev/README.md:63` (`.dev/workflow/<slug>/` and `.dev/implement/` preserved legacy), `~/.claude/WORKER-CONTRACT.md:159` (`--output .dev/tdd/auth-1/tdd.md --report-dir .dev/tdd/auth-1/`). All match the plan.

Nothing from "Changes NOT Being Made" was applied: no dedicated root or run stamp as the default (C-001, C-002), no camelCase subject (C-006), no V1 section order or flat list (S-001, S-003), no "never written again" wording (X-002).

## Changes Applied

### Change 1: FR-017, tool-owned folders

- Status: applied
- Before: no requirement; the base's pattern `.dev/<command>/<subject>-<n>/` did not mention folders other tools own.
- After (excerpt): "**FR-017. Report directories never sit directly in a folder another tool owns.** ... Option A (Variant 1). A dedicated root for every command: `.dev/orca/<runStamp>-<runSlug>/<command>-<subject>-<attempt>/` ... Option B (Variant 2). Keep `.dev/<command>/<subject>-<n>/` and give the reserved commands a parent folder that no tool owns. The folder name is to be decided by the person. Status: UNRESOLVED."
- Placement: in "Functional requirements", directly after FR-007, as the plan says.
- Provenance tag: `Variant 1 (opus:scribe), R4 and Recommended pattern (dedicated root), with the Variant 2 advocate's reserved-name concession, merged per Change #1`
- Consequential edits:
  - Preamble: one sentence added saying the merged document also cites `reflect.md`, `brainstorm.md` and `.dev/README.md`; without it the base's "three files" evidence statement would be false. Tag: `Base (original, modified)`.
  - "Recommended pattern": one sentence appended pointing to the UNRESOLVED date and root decisions; the base sentence "no date in the name" is kept. Tag: `Base (original, modified)`.
- Validation: both options shown, neither chosen; Option A's conflict with FR-009 is stated, not resolved; V1 R4's UNVERIFIED marker kept.

### Change 2: FR-011 replaced

- Status: applied
- Before: "**FR-011. The directory value is one isolated token.** ... the `Command:` line should contain the path exactly once, so the comparison strips one token."
- After (excerpt): "**FR-011. Only the attempt number changes between retries.** ... The path can appear more than once on the `Command:` line: the contract's own example passes `--output .dev/tdd/auth-1/tdd.md --report-dir .dev/tdd/auth-1/` (WORKER-CONTRACT.md line 159). Before it compares command lines for the three-failed-starts limit, the coordinator removes every path token that carries the attempt number (the directory and any file path inside it)."
- Provenance tag: `Variant 1 (opus:scribe), FR-005 "Attempts stay visible to the circuit breaker", merged per Change #2 (replaces base FR-011)`
- Consequential edit: FR-001 said the path goes into "the single `--report-dir` or `--output` token", which would contradict the new FR-011. Changed to "the `--report-dir` or `--output` token ..., and into any file path inside that directory that the line also passes (FR-011)". Tag: `Base (original, modified)`. This edit is not named in the plan; it was made so that validation item 6 (FR-011 agrees with the two-token example) holds across the document. Rollback with Change 2.
- Validation: no remaining "exactly once" or "single token" wording in the body.

### Change 3: FR-005, open risk 2, FR-008 edited; FR-018 added

- Status: applied
- Before (FR-005): "It confirms in the target worktree that the directory does not exist, or exists empty. A refusal by the command ... is a backstop, not the check."
- After (FR-005, excerpt): "... A free directory does not prove that its attempt number is unused: a guard-refused attempt (FR-012) runs nothing, writes no contract and may leave no directory ... So the next `<n>` comes from the coordinator's written run notes (FR-018) and from the Task specs ...; the directory listing is only a cross-check."
- Before (risk 2): "recover the highest `<n>` by listing the directories (FR-005)"
- After (risk 2, excerpt): "recover the highest `<n>` from those run notes and from the Task specs ... Listing the directories (FR-005) is only a cross-check, because a guard-refused attempt can leave no directory (FR-012)." Base UNVERIFIED marker kept; the A-001 caveat that Orca listing of Task specs is UNVERIFIED (Variant 2 advocate) added as UNVERIFIED.
- Before (FR-008): "... in the coordinator's run notes next to the path, not put in the directory name."
- After (FR-008): "... in the coordinator's run notes next to the path, in the line format of FR-018, not put in the directory name." UNVERIFIED marker kept.
- New FR-018 (after FR-008): one run-notes line per report directory (directory, Task ID, command line, worktree, replaced Task ID), plus `replaces <old Task ID>` in the retry brief, with an example line. The example uses the base path shape and an ellipsis for the command text, so no command text was invented.
- Provenance tags: FR-005, FR-008, risks section: `Base (original, modified)`; FR-018: `Variant 1 (opus:scribe), FR-009 "Audit record per name" and its run-notes example, merged per Change #3`
- Validation: FR-005, risk 2 and FR-012 now agree (guard refusals consume attempts and are recovered from notes, not listings).

### Change 4: FR-019, `-1` suffix as a requirement

- Status: applied
- Before (risk 1): "... has no attempt suffix ... Recommendation: add `-1` from the start; renaming existing planned paths is a plan edit outside this spec."
- After: new "**FR-019. Fixed per-check names gain an attempt suffix.**" in "Retries", after FR-013. Risk 1 is kept in place (so risks 2 to 6 keep their numbers) and now reads "The `-1` suffix is now a requirement (FR-019). The remaining risk: ... keeps its fixed names until the plan is edited".
- Provenance tag: `Variant 1 (opus:scribe), FR-011 "Fixed per-check names gain an attempt suffix", merged per Change #4 (moved from base open risk 1)`
- Validation: worked-example row "P1 live check `impact`, first run" (`.dev/p1-live/impact-1/`) agrees with FR-019.

### Change 5: Decisions table

- Status: applied
- Before: no section; the answers were one sentence in "Recommended pattern".
- After: new H2 "Decisions on the open questions" after "Recommended pattern", with the four seed-brief questions (base answer, reason, status) and a fifth row for subject style, which the plan names as UNRESOLVED. Date row and subject-style row say UNRESOLVED and name Variant 1's alternative.
- Provenance tag: `Variant 1 (opus:scribe), Decisions on the open questions, merged per Change #5 (answers are the base's; the date and subject-style rows are UNRESOLVED)`
- Validation: answers match the base text (FR-008, FR-009, FR-019, pattern section); no new decision added.

### Added per instruction: "Unresolved conflicts" section

- New H2 at the end listing S-001, C-001, C-002, C-006, X-001, A-002, each with a one-line description and both advocates' Round 1 positions and confidences from `debate-transcript.md`.

## Post-Merge Validation

### Structural Integrity

- One H1, ten H2 sections, no H3 or deeper: no level gaps.
- Base H2 sections kept in order; new H2 sections: "Decisions on the open questions" (after "Recommended pattern") and "Unresolved conflicts" (last).
- FR-001 to FR-019 each defined exactly once. FR-017 and FR-018 sit inside "Functional requirements" after FR-007 and FR-008; FR-019 sits in "Retries" after FR-013. Numbers are not in reading order, as the plan's numbering requires.
- Result: PASS.

### Internal References

- Total: 43 (34 FR-n references, 5 risk-n references including 3 in provenance comments, 4 quoted section-name references)
- Resolved: 43
- Broken: 0
- Diff-point IDs (S-001, C-001, C-002, C-006, X-001, A-002): every occurrence matches a row in "Unresolved conflicts".
- Quoted contract section names ("Brief guard", "Reading a result", "Feature worktree and child worktrees") point to WORKER-CONTRACT.md, not to this document, and are unchanged from the sources.

### Contradiction Re-Scan

- FR-011 against the contract's two-token example (WORKER-CONTRACT.md line 159): agree. FR-001 adjusted to match (see Change 2).
- FR-005 and risk 2 against FR-012: agree; recovery uses run notes and Task specs, listings only as a cross-check.
- FR-009 (no date) against FR-017 Option A (run stamp): not a contradiction in the decided text; FR-017 states the conflict and leaves it UNRESOLVED (C-002).
- "Recommended pattern" (`.dev/<command>/`) against FR-017: the pattern section now points to FR-017 for the open root decision.
- FR-018 example and the worked-examples row `.dev/tdd/auth-2/`: agree.
- Pre-existing, unchanged by the merge: FR-002's heading writes `<command>-subject-attempt` while the pattern is `.dev/<command>/<subject>-<n>/`; a naming shorthand from the base, not introduced by this merge.
- UNVERIFIED markers: all 5 base markers kept; V1 R4's marker kept in FR-017 Option A.
- New contradictions found: 0.

## Summary

- Planned: 5
- Applied: 5
- Failed: 0
- Skipped: 0
- Consequential consistency edits outside the literal plan: 3 (preamble, "Recommended pattern" last sentence, FR-001); each is tagged `Base (original, modified)` and listed above.
