# Diff Analysis: requirements spec Comparison

## Metadata
- Generated: 2026-11-05T03:12:00+00:00
- Variants compared: 3 (A = variant-1-opus-architect, B = variant-2-sonnet-refactorer, C = variant-3-haiku-qa)
- Total differences found: 29 debate points plus 14 unique contributions
- Categories: structural (4), content (16), contradictions (4), unique (14), shared assumptions (5)
- Verification done by the orchestrator while writing this file (read-only): `cp -r` re-copy behavior, `git rev-parse --git-common-dir` from a linked worktree, `version:` frontmatter census of `src/superclaude/commands/`, `orca worktree list` for this repo.

## Structural Differences

| # | Area | A (opus architect) | B (sonnet refactorer) | C (haiku qa) | Severity |
|---|------|--------------------|-----------------------|--------------|----------|
| S-001 | Where the logic lives [L2] | New `refs/worktree.md` plus a standard-library script `scripts/orca_worktree.py`; the skill never builds an `orca` command itself (A FR-5) | Wave 7 inside `refs/claim.md`; no new file; the orchestrator runs the commands (B s1, s8) | Wave 7 inside `refs/claim.md`; the orchestrator runs the commands and `cp -r` inline (C s5) | High |
| S-002 | How Wave 6 step 4 ("print path and STOP") is changed [L2] | Rewritten: without the flag print and STOP, with it run Wave 7 then print both and STOP (A s5) | Rewritten the same way (B s5) | Declared "byte-identical" and Wave 7 placed "after Wave 6 step 4" (C s5) | Medium |
| S-003 | Shape of section 4 [L1] | Prose, one code block, YAML contract block | Table of codes, one code block | Prose, one code block | Low |
| S-004 | Edge-case table [L1] | 11 rows, behavior only | 7 rows, behavior only | 15 rows, each mapped to a test ID | Low |

## Content Differences

| # | Topic | A | B | C | Severity |
|---|-------|---|---|---|----------|
| C-001 | Name and branch [L2] | `--name issue-<N>-<slug>`, no `--branch` so Orca adds its prefix (A 2.3) | `--name issue-<N> --branch issue-<N>` (B 2.3) | same as B (C Q3) | Medium |
| C-002 | Which repo Orca is told [L2] | `--repo path:<main>`, main checkout from `git --git-common-dir`, so a claim run in a linked worktree still works (A s4) | `--repo path:<T>`, `<T>` = `--show-toplevel`; from a linked worktree resolution is UNVERIFIED (B s4, s6) | `--repo` omitted; Orca infers from the current managed worktree (C s4) | Medium |
| C-003 | `--setup` policy [L2] | omitted (repo policy decides); FR-6 forbids `--setup` | omitted | `--setup run` | Medium |
| C-004 | Duplicate lookup key on re-claim [L3] | `--comment "sc:issue <R>#<N>"` marker, else path basename `^issue-<N>(-\|$)` (A 2.5) | branch matches `(^\|/)issue-<N>(-[0-9]+)?$` (B 2.5) | `<D>/worktree.json` record, then `git rev-parse` of the recorded path, then list match on exact branch `issue-<N>` (C Q5) | High |
| C-005 | Several rows match [L3] | reuse first marker match, else first path match; warn listing all (A s6) | warn, create nothing (B s5 step 3) | not addressed | Medium |
| C-006 | Stale, archived or deleted worktree [L3] | matched path gone from disk: `failed` + `W-WORKTREE-STALE`, no create (A s6) | archived rows ignored, a new one is created (B s6) | deleted worktree fails the rev-parse check and is re-created (C E8) | Medium |
| C-007 | Copy semantics into the worktree [L3] | copy `<D>` recursively; same-named files overwritten on re-claim (A 2.4) | copy files; never overwrite an existing file (B 2.4, FR-7) | `mkdir -p` then `cp -r <D> <wt>/.dev/issues/<N>/`; re-copy on reuse (C s5, E5) | High |
| C-008 | Where the worktree path comes from after create [L3] | create JSON `path`/`branch`, else re-list by marker (A s5) | always the follow-up list; create JSON never trusted (B s5 step 4) | parse create JSON, accept top-level or nested `result`; no re-list (C s5 step 4) | Medium |
| C-009 | Return-contract additions [L1] | 4 fields: status, path, branch, warning | 2 fields: path, status | 1 field: path | Low |
| C-010 | Warning vocabulary [L1] | 6 codes | 4 codes | 1 code (`W-WORKTREE-FAILED`) | Low |
| C-011 | Version marker [L2] | `version: "1.1.0"` in `commands/issue.md`; recorded as decision B16 in the design doc | `version: "1.1.0"` in `commands/issue.md` only | none; dated addendum in the design doc | Medium |
| C-012 | Test strategy [L2] | new `tests/skills/test_issue_orca_worktree.py` runs the script against a fake `orca` on PATH (behavior), plus static pins, plus one manual run | static text pins only, plus one manual run | static pins T1-T3 plus three observed runs T4-T6 | High |
| C-013 | Timeouts on Orca calls [L3] | 120 s per call inside the script; a create that timed out but finished is found next run | none stated | none stated | Medium |
| C-014 | When Wave 7 starts [L3] | after Wave 6 step 3 succeeded | after both comments posted | after Wave 6 steps 1-2 | Low |
| C-015 | How the design doc records the change [L2] | new decision B16 plus edits to sections 4, 7, 14, 16 | one new decision row "B2 unchanged" | dated addendum; R5 says the B2 reading must be confirmed in the debate | Medium |
| C-016 | Taken name / Orca numeric suffix [L3] | `W-WORKTREE-CREATE-FAILED` if create fails (UNVERIFIED) | regex tolerates `-<digits>` suffix | accepts suffix, prints `created (renamed)`, records the returned branch | Medium |

## Content Differences

{{RF_PLACEHOLDER:content}}

## Contradictions

| # | Point of Conflict | A position | B position | C position | Impact |
|---|-------------------|-----------|-----------|-----------|--------|
| X-001 | Does the flag change Wave 6? [L2] | Yes: step 4 becomes conditional | Yes: step 4 becomes conditional | No: "Wave 6 stays byte-identical", yet `refs/claim.md:90` step 4 reads "Print the `next-steps.md` path and STOP", which ends the run before a later Wave 7. C contradicts itself. | High |
| X-002 | Does any primitive carry a version marker? [L2] | "eight commands already carry `version:`" | names `brainstorm`, `reflect`, `pr-submit` | "no primitive in `src/superclaude/` carries a version marker". Verified today: 8 of 47 command files have `version:` in frontmatter (brainstorm 2.0.0, cli-portify, init-lite, pr-submit, reflect, swarm-wizard, task, tasklist). C is wrong. | Medium |
| X-003 | Is B2 untouched? [L3] | B2 is stretched: records the change as new decision B16 | "B2 stays literally true" | B2 intact, but R5 admits the reading needs confirming. Design doc `docs/designs/sc-issue-command.md:27` says "`--claim` stops after writing the next-step prompt ... and links it in the issue comment". Creating a worktree after that is an extra action, so "literally true" (B) is overstated. | Medium |
| X-004 | Re-copy into an existing worktree [L3] | overwrite same-named files | skip existing files | requires re-copy on reuse (E5, E6) but specifies `cp -r <D> <wt>/.dev/issues/<N>/`. Verified today: when the destination exists, `cp -r` nests the copy at `.dev/issues/<N>/<N>/`. C's own re-claim requirement produces a nested duplicate tree. | High |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | A | Single script seam; every Orca argument testable with a fake `orca` on PATH | High |
| U-002 | A | `--comment` marker survives title edits (stable lookup key); `--comment` is not an Orca link flag | Medium |
| U-003 | A | Main checkout resolved from `git --git-common-dir` (verified to work from a linked worktree today) | Medium |
| U-004 | A | Per-call 120 s timeout and "a timed-out create that finished is found next run" | Medium |
| U-005 | A | Final line tells the user to open the worktree and run `next-steps.md` there | Low |
| U-006 | B | No new file, so the existing "named-path inventory" and "five refs" tests stay unedited | Medium |
| U-007 | B | Never overwrites an existing file, protecting notes the user wrote in the worktree | Medium |
| U-008 | B | Names the risk that Orca maps this repo to the upstream project id. Verified today: all 11 rows of `orca worktree list --repo path:<this repo>` carry `projectId: github:superclaude-org/superclaude_framework` | High |
| U-009 | B | Re-lists after create instead of trusting the unverified create JSON shape | Medium |
| U-010 | B | Explicit "left out on purpose" list (agent launch, name value, dry-run, auto-removal, `--setup` choice) | Low |
| U-011 | C | Edge-case table mapped to tests, forbidden-flag regex, "unflagged output byte-identical" acceptance criterion | High |
| U-012 | C | Records `<D>/worktree.json` so a re-claim does one exact read before asking Orca | Medium |
| U-013 | C | Says plainly that the B2 reading must be confirmed and the flag dies if overruled (R5) | Medium |
| U-014 | C | Failure prints a remedy line repeating the create command | Low |

## Shared Assumptions

All five are promoted (none is STATED-and-safe). Each needs a response of ACCEPT, REJECT or QUALIFY from every advocate.

| A-NNN | Assumption [level] | Source agreement | Classification | Impact |
|-------|--------------------|------------------|----------------|--------|
| A-001 | A worktree created after `next-steps.md` is written still satisfies B2 ("stops after writing the next-step prompt") [L3] | all three keep Wave 7 after the comments | CONTRADICTED by the literal text of B2 (see X-003) | A needs a design-doc amendment; the flag can be refused |
| A-002 | `orca` is installed, the Orca app runs, and the current repo is registered with Orca, wherever the installed `/sc:issue` runs (it is installed to other projects) [L3] | all three use `orca` from the current directory | UNSTATED (they handle "missing", not "repo not registered") | wrong-repo or failed create in non-Orca projects |
| A-003 | `origin/<B>` exists locally, is fresh after the Wave 1 worker's `git fetch origin`, and Orca accepts it as `--base-branch` [L3] | all three use `--base-branch origin/<B>` | UNSTATED (offline fetch failure is not covered) | stale or failing base |
| A-004 | No hand-made worktree for the same issue exists under another name [L3] | B and C use `issue-<N>`; A adds `-<slug>` | CONTRADICTED by evidence: this repo already has `issue-330-ponytail-plugin`, `issue-315-ccsession-name-prompt`, `issue-305-pr-submit-conflicts` (and `issue-404-claim`, `issue-364-ruff-requests-default` on another repo). B's regex and C's exact match miss them; A's path fallback `^issue-<N>(-\|$)` would reuse them | duplicate worktree for the same issue, or reuse of an unrelated one |
| A-005 | An untracked copy of `.dev/issues/<N>/` inside the new worktree is harmless and will not be committed by mistake [L2] | all three copy and say "never stage" | UNSTATED (the new worktree's `git status` will show it) | accidental commit of issue artifacts |

## Summary

- Total structural differences: 4
- Total content differences: 16
- Total contradictions: 4
- Total unique contributions: 14
- Total shared assumptions surfaced: 5 (UNSTATED: 3, STATED: 0, CONTRADICTED: 2)
- Taxonomy coverage of debate points (S+C+X+A = 29): L1 = 4 (S-003, S-004, C-009, C-010), L2 = 11, L3 = 14. All three levels are covered.
- Highest-severity items: S-001, C-004, C-007, C-012, X-001, X-004, U-008

Agreement already present (not debated): all three keep a boolean, claim-only `--worktree`; all three create no agent and pass no Orca link flag; all three use `--no-parent` and `--base-branch origin/<B>`; all three copy `<D>` into the worktree; all three fail open with `status: success`; all three STOP `--create --worktree` with `E-CLAIM-ONLY-FLAG`.
