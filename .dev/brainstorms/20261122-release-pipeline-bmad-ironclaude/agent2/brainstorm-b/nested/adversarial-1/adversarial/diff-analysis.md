# Diff Analysis: spec Comparison

## Metadata

- Generated: 2026-11-22T20:40:00Z
- Variants compared: 2 (Variant 1 = opus:architect, Variant 2 = sonnet:analyzer)
- Total differences found: 29 (structural 4, content 10, contradictions 5, unique 10), plus 7 shared assumptions
- Categories: structural (4), content (10), contradictions (5), unique (10), shared assumptions (7)
- Taxonomy level tags: L1 = surface, L2 = structural, L3 = state mechanics (auto-tagged by signal terms)

Both variants choose the same option (option 3, with BMAD-only plus spec-panel as the default arm and the brainstorm plus adversarial merge as the alternate arm). The diff is therefore about the triggers, the merge rules, the cost counts and the conflict policy, not about the headline option.

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Severity | Level |
|---|------|-----------|-----------|----------|-------|
| S-001 | Heading and list formatting | Unnumbered `##` headings; sub-lists with bold lead-ins | Numbered `## 1.` to `## 8.` headings | Low | L1 |
| S-002 | Cost section layout | One 3-row table (option x size) with `calls / steps` pairs, then a prose breakdown | A counting-rule table, then a per-option table that splits option 3 into default arm and alternate arm rows | Medium | L2 |
| S-003 | Merge-rule layout | R1 to R8 as numbered items; a field-by-field change-log schema (R2); a separate `### IronClaude criteria` list | R1 to R9 as bullets; per-rule "Failure:" lines; every merged line tagged | Medium | L2 |
| S-004 | Trial plan layout | Scope, per-story record, shadow runs, decision rules | Metrics M1 to M4, then four threshold rules | Low | L2 |

## Content Differences

| # | Topic | Variant 1 approach | Variant 2 approach | Severity | Level |
|---|-------|--------------------|--------------------|----------|-------|
| C-001 | Trigger set and thresholds | 7 triggers: missing path, drift (3 commits or 150 lines), cross-subsystem (2 prefixes of 3 segments), risk regex (adds storage, protocol, permission, encrypt), size (more than 6 AC or tasks), panel code gap, ungrounded story | 5 triggers: missing path, churn (3 commits), size or blast radius (more than 8 AC, more than 12 tasks, 3 top directories, narrower regex), not executable as written, panel finding (FAIL with at least 2 blocking) | Medium | L2 |
| C-002 | When the panel runs relative to triggers | Script gate first (T1 to T5, T7), panel second, T6 read from the panel report | Script gate first (T1 to T4), panel second, T5 read from panel review 1; if T5 fires the alternate arm follows | Medium | L2 |
| C-003 | Cost counting rule and numbers | Command session = 1 call, each subagent = 1; spec-panel 1 call per review plus 1 reviser call per fix cycle; workflow 3 calls; steps include scripts | One call per subagent or single-session pass; spec-panel 1 call per review, no reviser call; workflow 2 calls; brainstorm P+5, adversarial 4 | Medium | L2 |
| C-004 | Acceptance-criterion id syntax | `[S<e>.<s>-AC<n>]` for BMAD ids (epic and story included), `[IC-<n>]` for added ones | `AC-n` for BMAD ids, `AC-IC-k` for added ones | Low | L1 |
| C-005 | Handling of the adversarial merged output | Never the spec: its criteria section is discarded and rebuilt from the story (R7); a reworded criterion becomes a `proposed` change-log row | The merged spec must satisfy R1 to R9; a script re-runs R1 and R6 after the merge and blocks `/sc:workflow` on failure | High | L3 |
| C-006 | Mapping BMAD ids to executor ids | Every line of every task criteria block starts with exactly one id token (R4); checked after `/sc:workflow`, before `/sc:implement` | `ac-map.md` with rows `AC-n -> T<i>.AC<k>`; every BMAD id has at least 1 row (R3); R9 requires a passing executor row per id | Medium | L3 |
| C-007 | Story edits and source preservation | IronClaude edits only `## Dev Agent Record` (R8); no stored copy of the original beyond the story file | Same edit limit, plus the story is stored byte-exact as `source-story.md` in the package (R7) | Low | L2 |
| C-008 | Trial metrics and thresholds | Spec-caused failures (keep at 10% or less, switch at over 25%), shadow runs with material deltas (20% / 40%), trigger removal and 60% fire-rate rules | Missed conflicts (keep at 10% or less of non-triggered stories, switch at 25% or more), trigger fire rate (40% / 50%), AC-loss stop rule; at least 12 stories | Medium | L2 |
| C-009 | Command flags in the flow | `/sc:workflow --depth quick` on the default arm, `standard` or `deep` on the alternate; panel and brainstorm carry `--unattended --report-dir <D>/...`; brainstorm `--depth standard` when T3 or T4 fired | `/sc:workflow --depth standard` on both arms; panel carries `--unattended` with no report directory; brainstorm and adversarial use `--output` | Medium | L2 |
| C-010 | Design step | States `/sc:design` is not run on either arm (BMAD architecture is the design) | Silent about `/sc:design` | Low | L2 |

## Contradictions

| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Impact |
|---|-------------------|--------------------|--------------------|--------|
| X-001 | What happens to the run when a criterion or architecture constraint cannot hold against the code | R6: the story wins; the worker writes a `proposed` change-log row; any `proposed` row stops the hand-off before `/sc:workflow` and goes to the coordinator, who approves, rejects or sends the story back to BMAD | R4: the story wins on intent; the worker marks that one task `BLOCKED-AC-n`, records it in `deviations.md`, messages the coordinator and continues the other tasks. Evidence against V2: `/sc:implement` Q8 (`~/.claude/skills/sc-implement-protocol/SKILL.md` line 150) says NEXT only if the task is complete, else STOP, so the executor cannot continue past an incomplete task | High |
| X-002 | Cost of the same option for the same story size | Option 1 simple 4 calls / 5 steps; option 2 simple 18 calls / 8 steps; option 3 complex 31 calls | Option 1 simple 3 calls / 2 steps; option 2 simple 14 calls / 4 steps; option 3 alternate arm complex 18 calls (differences come from the counting rule, C-003) | Medium |
| X-003 | Whether corrections go back to the BMAD story | R8: append spec path, id map and corrections table to `## Dev Agent Record` so the next `bmad-create-story` learns from them | Out of scope: feeding corrections back to the BMAD story or `sprint-status.yaml` | Low |
| X-004 | Spec-panel invocation under `--unattended` | Passes `--report-dir <D>/panel` | Passes no report directory. Evidence: `~/.claude/commands/sc/spec-panel.md` line 458: without `--report-dir` the run is refused before any work | Medium |
| X-005 | Treatment of paths the story says will be created | T1 fires when any named path does not exist at HEAD, so every story that creates a file fires T1 (the story's Dev Notes list "files to touch" including new ones) | T1 and T2 skip any path the story marks `(new)` | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | 1 | Shadow runs: on every third default-path story, also run alternate steps 2 to 4 without executing the result, and count material deltas. This measures the trigger false-negative rate directly | High |
| U-002 | 1 | `story-gate` rewrites each task's `(AC: #)` reference into the full criterion text, because AC QUALIFY rule 1 (`~/.claude/skills/sc-implement-protocol/SKILL.md` line 98) matches an `AC:` token and could read "2" as the criterion | High |
| U-003 | 1 | AC change log with fields (old text, new text, reason class, evidence `path:line@sha`, status `proposed` or `approved`, approver) and a route back to BMAD through `bmad-correct-course` | High |
| U-004 | 1 | Trigger hygiene: remove a trigger that produced no corrections in 80% or more of at least 3 firings; if triggers fire on more than 60% of stories, treat option 3 as option 2 | Medium |
| U-005 | 1 | T6 (panel blocking finding on Dev Notes, Project Structure or Tasks) and T7 (ungrounded story with zero named paths); risk regex includes storage and protocol | Medium |
| U-006 | 2 | T4 "not executable as written": zero AC, a task with no `AC: #` reference, an AC with no Given, When or Then, Dev Notes with no file path | Medium |
| U-007 | 2 | Provenance tag on every merged line: `[BMAD]`, `[IC]` or `[BOTH]` | Medium |
| U-008 | 2 | R9 completion closure (a story is complete only if each `AC-n` has a passing executor row or an R6 or R4 row) and the byte-exact `source-story.md` copy | High |
| U-009 | 2 | M2 "missed conflict" metric (no trigger fired, yet a fact conflict or stale-note QA failure appeared); stop rule for option 2 when AC loss appears on 2 or more alternate-arm stories; trigger list frozen during a release | Medium |
| U-010 | 2 | Cost formulas per component (brainstorm = P+5, adversarial = 4, panel R reviews) so a reader can recompute the table | Medium |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Classification | Impact | Status |
|-------|------------|------------------|----------------|--------|--------|
| A-001 | Path-level checks (a named path exists; commit count or changed lines since the story commit) detect when Dev Notes are semantically stale. The brief itself says the staleness rate is UNVERIFIED | Both: option 3 default arm rests on T1 and T2 | UNSTATED | High | Promoted |
| A-002 | `/sc:workflow` keeps story id tokens or the `AC:` block text when given a story-shaped file | Both: R3 or R4 check after the workflow | STATED (both mark it UNVERIFIED) | Medium | Documented |
| A-003 | The gate and map-check scripts (`story-gate`, `check-story`, `ac-map-check`, the R1 and R6 re-check) get built, are deterministic and are owned by someone; the cost tables count them as 0 calls and give no build cost | Both: scripts are the enforcement for R1 to R9 | UNSTATED | Medium | Promoted |
| A-004 | Every incoming story has the BMAD template shape: a non-empty numbered AC list, `Task n (AC: #)` references, a Dev Notes section with file paths. Humans can edit a story between creation and hand-off | Both: R1 and R3 parse numbers and references | UNSTATED | High | Promoted |
| A-005 | A code-blind spec-panel review plus path scripts is an adequate check of code accuracy. Neither variant considers the existing one-call accuracy check (`current` or `out_of_date`, `~/.claude/skills/sc-issue-protocol/refs/claim.md` line 58) as a trigger source; that check is part of `/sc:issue --claim`, a coordinator-only command | Both: no code-reading step on the default arm | UNSTATED | High | Promoted |
| A-006 | A coordinator session exists, keeps the spec-panel review count and prior-findings file, and answers escalations (R2 or R6 rows) before the release moves on | Both: escalation to the coordinator; `spec-panel.md` line 261 says the coordinator keeps the count | STATED | Medium | Documented |
| A-007 | Model calls are a good enough cost proxy. The brainstorm's own estimate is about 80K tokens per quick proposal, and a panel review or a workflow pass has different token weight, so calls can hide the real cost ratio | Both: cost tables count calls and steps | UNSTATED | Medium | Promoted |

## Summary

- Total structural differences: 4
- Total content differences: 10
- Total contradictions: 5
- Total unique contributions: 10
- Total shared assumptions surfaced: 7 (UNSTATED: 5, STATED: 2, CONTRADICTED: 0)
- Highest-severity items: C-005, X-001, U-001, U-002, U-003, U-008, A-001, A-004, A-005
- Diff points in the convergence denominator (S + C + X + A): 26
- Taxonomy: L1 = S-001, C-004 (2); L3 = C-005, C-006, X-001, A-004, A-006 (5); L2 = all other points (19). All three levels are covered, so no forced round is needed.
- Similarity check: differences are well above 10% of comparable items, so the debate runs.
