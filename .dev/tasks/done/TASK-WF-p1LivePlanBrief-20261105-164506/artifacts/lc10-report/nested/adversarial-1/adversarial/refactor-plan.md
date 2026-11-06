# Refactoring Plan

## Overview

- Base variant: Variant 2 (sonnet:analyzer), `variant-2-sonnet-analyzer.md`
- Incorporated from: Variant 1 (opus:scribe), `variant-1-opus-scribe.md`
- Planned changes: 5 (4 edits to base requirements, 1 new section)
- Rejected changes: 5 (listed below)
- Overall risk: Medium (change 1 records an open decision and does not settle it)
- Unresolved debate points carried into the merged output: S-001, C-001, C-002, C-006, X-001, A-002

## Planned Changes

### Change 1: Add a tool-owned-folders requirement (from Variant 1, with Variant 2's reserved-name idea)

- Source: V1 R4 and its separate-root design (diff points C-001, X-001, A-002); V2 advocate concession "a reserved-name rule is needed".
- Target: new requirement FR-017 in the base, after FR-007.
- Integration: insert.
- Rationale: both advocates agreed the clash is real (debate-transcript.md, X-001 and A-002 rows). Verified facts to state: `src/superclaude/commands/reflect.md:101` makes `.dev/reflect/<mode>-<slug>-<ts>/` the default output of `reflect`; `.dev/README.md:63` lists `.dev/workflow/<slug>/` and `.dev/implement/` as preserved legacy locations; `src/superclaude/commands/brainstorm.md:62` makes `.dev/brainstorms/<ts>-<slug>/` the brainstorm default. A coordinator report folder must not sit directly in those folders.
- Content: the requirement states the rule and the facts, then records two candidate fixes without choosing: Option A, V1's dedicated root `.dev/orca/<runStamp>-<runSlug>/<command>-<subject>-<attempt>/` for every command; Option B, keep `.dev/<command>/<subject>-<n>/` and give the reserved commands a parent no tool owns (folder name to be decided by the person). Status line: UNRESOLVED, because the debate did not converge on it and unattended mode cannot ask.
- Risk: Medium (the merged spec ships with an open decision).

### Change 2: Replace FR-011 (from Variant 1 FR-005, diff point C-005)

- Source: V1 FR-005 plus the contract's two-token example (`--output .dev/tdd/auth-1/tdd.md --report-dir .dev/tdd/auth-1/`, WORKER-CONTRACT.md line 159).
- Target: FR-011 in the base.
- Integration: replace.
- Rationale: both advocates chose MERGE; V2's "path exactly once" is false for the contract's own example. New wording: between retries only the attempt number changes, and the coordinator removes every path token that carries the attempt number (the directory and any file path inside it) before it compares command lines for the three-failed-starts limit.
- Risk: Low.

### Change 3: Fix counter recovery and add the audit line (from Variant 1 R1 and FR-009, diff points A-001, A-003)

- Source: V1 R1 (a guard-refused attempt leaves no contract and no directory) and V1 FR-009 (one run-notes line per name, with the Task ID and `replaces`).
- Target: FR-005, open risk 2 and FR-008 in the base; one new requirement FR-018.
- Integration: restructure.
- Rationale: A-003 was rejected by both advocates (75% and 70%). Recovery of the highest attempt number must come from the written run notes and the Task specs, with the directory listing used only as a cross-check. FR-018 adds the audit line format from V1.
- Risk: Low.

### Change 4: Make the `-1` suffix a requirement (from Variant 1 FR-011, diff point C-007)

- Source: V1 FR-011; V2 open risk 1.
- Target: open risk 1 in the base, moved into a new requirement FR-019.
- Integration: restructure.
- Rationale: both advocates picked V1 (65% and 60%). A fixed per-check name such as `.dev/p1-live/impact/` has no free name for a re-run.
- Risk: Low.

### Change 5: Add a decisions table (from Variant 1, diff point S-002)

- Source: V1 "Decisions on the open questions".
- Target: new section after "Recommended pattern" in the base.
- Integration: insert.
- Rationale: both advocates picked V1 (70% and 65%). The table lists the four open questions of the seed brief with the base's answer and reason; for the date and for the subject style the row says "UNRESOLVED" and names V1's alternative.
- Risk: Low.

## Changes NOT Being Made (with rationale)

| Diff point | Non-base approach | Why the base approach stays |
|---|---|---|
| C-001 | V1 dedicated root and run folder as the default shape | Unresolved in the debate (MERGE against V2); kept as Option A inside Change 1 |
| C-002 | V1 run-level UTC stamp | Unresolved; the base has no date (git history and the contract carry time); V1's stamp stays as Option A and in the decisions table |
| C-006 | V1 camelCase, at most 16 characters | Unresolved (55% against 60%); the base's kebab slug stays, and its trailing-digit warning is kept |
| S-001, S-003 | V1 section order and flat requirement list | S-003 went to V2 (topic sections); S-001 is cosmetic and unresolved |
| X-002 | V1 FR-004 "never written again" | V2's FR-013 is correct (WC-3 re-run inside one Task); V1's wording is not carried over |

## Risk Summary

| Change | Risk | Impact if wrong | Rollback |
|---|---|---|---|
| 1 | Medium | The spec states an open decision; a reader may pick the wrong option | Remove FR-017 and the Unresolved section |
| 2 | Low | Retry comparison wording | Restore the base FR-011 |
| 3 | Low | Recovery wording | Restore base FR-005 and risk 2 |
| 4 | Low | Extra suffix on fixed names | Move back to risk 1 |
| 5 | Low | Table only | Delete the section |

## Review Status

Auto-approved (non-interactive, `--unattended`), 2026-11-05T20:02:00Z.
