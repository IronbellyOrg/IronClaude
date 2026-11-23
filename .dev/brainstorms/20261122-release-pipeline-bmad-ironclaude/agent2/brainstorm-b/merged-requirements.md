<!-- Provenance: This document was produced by /sc:adversarial (Mode B, quick, unattended) -->
<!-- Base: Variant 1 (opus:architect) -->
<!-- Incorporated: Variant 2 (sonnet:analyzer), plus orchestrator adjudication of 9 unresolved debate points -->
<!-- Merge date: 2026-11-22T21:20:00Z -->

# Requirements: who writes the spec at the BMAD to IronClaude hand-off of one story

<!-- Source: Base (original, modified): title kept; numbering added per Change #1 (Variant 2) -->

Status of the debate behind this document: convergence 65.4% (17 of 26 diff points) against a 75% threshold, so the run is flagged as not fully converged. Nine points were settled by the orchestrator from verified evidence (section 10). Every figure marked ESTIMATE or UNVERIFIED is to be measured in the trial of section 7.

## 1. Recommendation

<!-- Source: Base (original, modified) and Variant 2 section 1 reasons -->

**Default: the BMAD story is the spec (option 1), reviewed once by `/sc:spec-panel`. IronClaude writes its own code-grounded spec with `/sc:brainstorm` and merges it with the story by `/sc:adversarial --compare` (option 2) only when one of the seven triggers in section 4 fires.** This is option 3 (conditional). Always running both (option 2 on every story) is not recommended.

Why:
- A BMAD story is already an LLM-researched, code-aware artifact: `bmad-create-story` reads the PRD, architecture, epics, recent commits and the previous story's notes, and its stated purpose is to prevent developer mistakes (`.claude/skills/bmad-create-story/SKILL.md`, "Your Role"). A second full spec on every story mostly re-derives it.
- IronClaude already works this way: the installed issue chains plan a simple feature straight from its text with `/sc:workflow` and add a brainstorm only from medium upward (`~/.claude/skills/sc-issue-protocol/refs/chains.md`).
- The alternate arm costs about 3 to 4 times the default arm in model calls (section 5), and it adds a second merge, which is a new place for acceptance criteria to be lost.
- The code-grounded pass is worth its cost when the story's code facts may be stale or the work crosses subsystems.

Boundary: BMAD owns the what (acceptance criteria and architecture decisions). IronClaude owns the how and the facts about today's code. Terms: AC = acceptance criterion; a story id is `S<epic>.<story>-AC<n>`; a worker is a `--unattended` command run that cannot ask a person; the coordinator is the session that answers escalations and keeps the panel review count.

## 2. Hand-off flow

<!-- Source: Base (original, modified): flags per Change #13; depth per Change #17; source copy per Change #7 -->

`<D>` is the run folder `.dev/stories/<epic>-<story>/` (a proposal). Two scripts do not exist yet and must be built before the trial: `story-gate` and `ac-map-check` (modes: check, `--tasklist`, `--repair`). They cost 0 model calls and 1 step each time they run.

**Default arm (no trigger fires):**
1. `story-gate <story.md> --out <D>`. It applies the shape stop and triggers T1 to T5 and T7 (section 4), and writes `<D>/gate.json`, `<D>/source-story.md` (byte-exact copy) and `<D>/spec.md`: the story with each criterion tagged `[S<e>.<s>-AC<n>]`, each task's `(AC: n)` reference replaced by the full criterion text, and two empty tables, `## AC change log` and `## Dev Notes corrections`.
2. `/sc:spec-panel @<D>/spec.md --mode critique --focus requirements,testing --unattended --report-dir <D>/panel`. The coordinator keeps the review count; at most 2 fix cycles (3 reviews); a third review that ends `verdict: FAIL` halts and escalates and never switches arms (`~/.claude/commands/sc/spec-panel.md`, Review Loop, bullet 4). Read T6 from the report.
3. `ac-map-check <D>/spec.md <D>/source-story.md` (rules R1, R2, R3, R7).
4. `/sc:workflow <D>/spec.md --depth <quick if simple, standard if medium> --handoff none --unattended --report-dir <D>/wf`.
5. `ac-map-check --tasklist <plan path> <D>/spec.md` (rule R4); writes `<D>/ac-map.md`.
6. `/sc:implement <plan path>`.

**Alternate arm (any of T1 to T5 or T7 fires at step 1, or T6 fires at step 2):**
1. `story-gate`, as above.
2. `/sc:brainstorm "code-grounded spec for story <e>.<s> @<D>/spec.md" --codebase --blind --unattended --output <D>/bs`, with `--depth quick --proposals 2` by default and `--depth standard --proposals 3` when T3 or T4 fired.
3. `/sc:adversarial --compare <D>/spec.md,<D>/bs/merged-requirements.md --depth quick --focus correctness,architecture --unattended --output <D>/adv`.
4. `ac-map-check --repair <D>/adv/<merged file> <D>/spec.md`. It writes `<D>/spec.v2.md`: the criteria section copied from `<D>/source-story.md`, and from the merged file only the non-criteria content, tagged `[IC]` (rule R6). A reworded or new criterion in the merged file becomes a change-log row or an `[IC-n]` entry, never an edit.
5. `/sc:spec-panel` on `<D>/spec.v2.md` with the same flags, then `ac-map-check`.
6. If any `## AC change log` row has status `proposed`, stop and escalate to the coordinator (rule R5). Otherwise `/sc:workflow --depth standard` (`deep` only when T3 and T4 both fired), then `ac-map-check --tasklist`, then `/sc:implement`.

`/sc:design` is not run on either arm: BMAD's architecture document already is the design. The flags above were read in each command's Unattended mode section: spec-panel and workflow need `--report-dir` (refused without it); brainstorm and adversarial take their own directory flag `--output` (`~/.claude/WORKER-CONTRACT.md`, brief table).

## 3. Shape stop

<!-- Source: Variant 2 T4, adapted (Change #5) -->

Before any trigger, `story-gate` stops the hand-off, records the reason, and the coordinator returns the story to BMAD (`bmad-create-story` again, or `bmad-correct-course`) when: the story has zero criteria; the criteria are not a numbered list; or a task has no `(AC: n)` reference. A story with zero criteria cannot be repaired by IronClaude (`/sc:implement` would stop with `E-NO-AC`), so it never reaches a trigger. A Given/When/Then test is not used: the BMAD template makes criteria free-form numbered text (`.claude/skills/bmad-create-story/template.md`, line 15).

## 4. Triggers

<!-- Source: Base (original, modified): T1 and T2 skip new paths (V2); T4 list and T5 thresholds (V2, V1); T6 and T7 (V1) -->

The list is closed and frozen for a release: no one adds or waives a trigger mid-release. "Named paths" are the backticked repository paths in the story's Dev Notes, Project Structure Notes and References, leaving out any path the story marks `(new)` or lists as a new file (BMAD separates UPDATE from NEW files). "Story commit" is `git log -1 --format=%H -- <story.md>`. Every threshold is an ESTIMATE that the trial calibrates.

1. **T1, missing path:** at least 1 named path does not exist at HEAD.
2. **T2, drift:** since the story commit, the named paths have 3 or more commits or 150 or more changed lines (`git log`, `git diff --shortstat`). A story with no commit counts as drifted.
3. **T3, cross-subsystem:** the named paths fall under 2 or more distinct 3-segment path prefixes (the observable form of "more than one subsystem").
4. **T4, risk class:** the story text or criteria match, case-insensitive and whole-word, one of: migration, schema, ddl, postgres, storage, credential, secret, auth, authn, authz, wire format, protocol (the observable form of the complex rubric's security and data-migration classes, plus storage and protocol work).
5. **T5, size:** more than 8 criteria or more than 12 top-level tasks.
6. **T6, panel code gap:** the spec-panel report has a blocking finding located in Dev Notes, Project Structure Notes or Tasks. A blocking finding on criterion text is not a trigger: it becomes an R2 change-log row.
7. **T7, ungrounded story:** the story has zero named paths.

The rubric's ">16 hours" test is not used because a script cannot observe hours. Candidate for the next release, not in the list: the one-call code accuracy check that `/sc:issue --claim` already runs (verdict `current` or `out_of_date`, `~/.claude/skills/sc-issue-protocol/refs/claim.md` line 58); it is a coordinator-only command, so a worker equivalent would have to be built.

## 5. Cost comparison

<!-- Source: Variant 2 section 4 (counting rule, formulas, arm rows), Variant 1 (reviser call); arithmetic corrected (Changes #6, #14) -->

**Counting rule.** A model call is one agent context that produces output; the command session counts 1 and each spawned agent counts 1. A step is one command or script run. A script costs 0 calls and 1 step. `/sc:implement` is left out because it runs the same tasklist size under every option.

**Component formulas (ESTIMATE).**

| Component | Calls | Basis |
|---|---|---|
| `/sc:spec-panel`, R reviews | 2R - 1 | R reviews plus R - 1 reviser passes (cap R = 3) |
| `/sc:workflow` | 3 | planner, reflect pre-review (`workflow.md` line 94), writer (the planner and writer split is UNVERIFIED) |
| `/sc:brainstorm`, quick, P proposals | 2P + 4 | session, codebase scan, P generators, P advocates, 1 position-bias scorer, 1 merge agent. Standard depth adds P + 1 (rebuttals and invariant probe) |
| `/sc:adversarial --compare`, 2 inputs, quick | 4 | 2 advocates, 1 scorer, 1 merge agent |

One measured data point: this brainstorm run (quick, P = 2, no research) used 5 sub-agent calls (2 generators, 2 advocates, 1 scorer) plus the command session; the merge was run inline, and a separate merge agent would be the 6th. Those 5 calls reported about 671K tokens in total (138.7K, 123.2K, 130.2K, 132.9K and 146.1K; how the harness counts them is UNVERIFIED), about 3 times the brainstorm's own pre-flight estimate of about 208K for 2 proposals. So the token cost of the alternate arm is larger than its call count suggests, which is why the trial logs tokens.

**Sizes.** Simple: R = 1, P = 2. Medium: R = 2, P = 2. Complex (T3, T4 or T5 fired): R = 3, P = 3, standard depth. R is an assumption the trial measures.

| Option | Simple (calls / steps) | Medium | Complex |
|---|---|---|---|
| 1: story plus spec-panel on every story | 4 / 5 | 6 / 6 | 8 / 7 |
| 2: both specs on every story | 16 / 8 | 18 / 9 | 26 / 10 |
| 3, no trigger fires (default arm) | 4 / 5 | 6 / 6 | not reachable |
| 3, trigger fires (alternate arm) | 16 / 8 | 18 / 9 | 26 / 10 |

When T6 is the trigger, add the first panel review already spent: +1 call, +1 step (17 / 9, 19 / 10, 27 / 11). Steps: default arm = 4 + R; alternate arm = 7 + R.

Reading the table: the alternate arm costs 4.0 times (simple), 3.0 times (medium) and 3.25 times (complex, compared with option 1) the default arm in calls. A complex story always takes the alternate arm, so option 3 equals option 2 for it; the saving comes only from simple and medium stories with no trigger. With a trigger fire rate f, a medium story costs 6 + 12f calls on average: 9.6 at f = 0.3 (the rate is UNVERIFIED) against 18 for option 2.

**Not in the per-story table.** The scripts are built once, by a named owner of the release pipeline, before the trial starts. The tables count calls, but the brainstorm's own estimate is about 80K tokens per quick proposal, and no figure exists for a panel pass or a workflow pass, so the trial also logs tokens and wall-clock minutes per step where the command reports them (UNVERIFIED which commands do).

## 6. Merge rules (BMAD ids survive)

<!-- Source: Base R1 to R8, with R4 and R9 incorporated from Variant 2 (Changes #7 to #11) -->

Each rule is checked by a script (`ac-map-check`), not by reading.

1. **R1, ids:** every story criterion n appears in the spec's `## Acceptance Criteria` as `[S<e>.<s>-AC<n>] <text>`, byte-identical to `<D>/source-story.md` after trailing whitespace is trimmed. The short form `AC-n` is allowed only in prose inside one story folder, never as a key.
2. **R2, change log:** a criterion is removed or reworded only through a `## AC change log` row with: id, old text, new text or `removed`, reason (`contradicts-code`, `ambiguous` or `duplicate`), evidence as `path:line@<sha>`, status (`proposed` or `approved`), approver (coordinator session name). A worker writes only `proposed`. Any `proposed` row stops the hand-off before `/sc:workflow`.
3. **R3, added criteria:** criteria IronClaude adds get ids `[IC-<n>]` in a separate `### IronClaude criteria` list, each naming the BMAD id it supports (or `none`) and its source file. BMAD ids are never renumbered or reused.
4. **R4, tasklist tokens:** every line of every task's criteria block in the tasklist starts with exactly one `[S..-AC<n>]` or `[IC-<n>]` token, and no block holds only references. `ac-map-check --tasklist` writes `<D>/ac-map.md` with rows `S<e>.<s>-AC<n> -> T<i>.AC<k>`, predicting the executor ids by source order (executor ids are assigned by `/sc:implement`; see R9). Every BMAD id must appear in at least 1 task. Checked after `/sc:workflow` and before `/sc:implement`.
5. **R5, conflicts:** a factual conflict (a path, function or signature in the Dev Notes that the code contradicts) is settled for the code with no person involved and recorded as a `## Dev Notes corrections` row (the story's claim, the code fact, `path:line@<sha>`). A normative conflict (a criterion or BMAD architecture constraint that cannot hold against the code, or that the brainstorm argues should change) is settled for the story: the worker writes a `proposed` R2 row and escalates; the coordinator approves, rejects, or sends the story back to BMAD (`bmad-correct-course`). Nothing runs against a contested criterion. The executor cannot skip an incomplete task (`/sc:implement` Q8 stops, `SKILL.md` line 150), so a conflict is resolved before it starts, and the unaffected tasks of a stopped story wait.
6. **R6, adversarial output is an input, never the spec:** its criteria section is discarded and rebuilt from the story under R1; a reworded criterion becomes an R2 `proposed` row and a new one an R3 entry; spec-panel fixes may edit only non-criteria sections, and a blocking finding on criterion text becomes an R2 row.
7. **R7, edit surface:** IronClaude edits only the story's `## Dev Agent Record`, where it appends the paths of `spec.md`, `ac-map.md` and the corrections table so the next `bmad-create-story` run can learn from them. `<D>/source-story.md` is byte-exact. Test: a diff of the story outside that section is empty.
8. **R8, re-check:** `ac-map-check` re-runs R1, R2, R3 and R6 after every spec-panel reviser pass and after the repair. Any failure blocks `/sc:workflow`.
9. **R9, completion:** a story is complete only when each id has a passing row in the `/sc:implement` ledger or an `approved` R2 row, and the predicted `T<i>.AC<k>` map of R4 matches the ledger.
10. **R10, provenance:** every list item or section IronClaude adds is tagged `[IC]` with its source file.

## 7. Trial plan

<!-- Source: Base (original, modified): metrics M1 to M4, scope and stop rule from Variant 2; shadow runs from Base (Change #12) -->

**Scope.** One release with every story going through the flow, at least 12 stories (extend into the next release if fewer). Triggers and thresholds are frozen during it. The trial starts only when the scripts exist.

**Record per story in `<D>/gate.json`:**
- M1: the path taken, the triggers fired, calls and wall-clock minutes per step (and tokens where available);
- M2: a missed conflict is a story where no trigger fired, yet a factual conflict row appeared or a task failed its first QA pass and was traced to stale Dev Notes;
- M3: AC loss, meaning any R1, R2, R3 or R6 failure after R8;
- M4: coordinator escalations, plus `E-HALT-QA` and `E-NO-AC` halts and QA retries, and for each failure whether it was spec-caused (the fix needed a code fact the spec lacked or got wrong).

**Shadow runs.** On every third default-path story (at least 3), also run alternate steps 2 to 4 without executing the result, and count material deltas: corrections or R2 rows that would change a task. Fire rates of T1 and T2 also measure how stale the Dev Notes are, which is the largest unknown (UNVERIFIED).

**Decision rules** (the three outcomes do not overlap):
- Keep the default when all hold: spec-caused failures on default-path stories 10% or less; missed conflicts 10% or less of untriggered stories; shadow material deltas 20% or less; triggers fire on 40% or less of all stories.
- Make option 2 the default when any holds: spec-caused failures over 25%; missed conflicts 25% or more of untriggered stories; shadow deltas over 40%; the fire rate of T1 or T2 is 50% or more.
- Otherwise keep the default and tighten the triggers, lowering T2 to 2 commits first.
- Remove a trigger whose firings (at least 3) produced no correction and no R2 row in 80% or more of cases.
- If triggers fire on more than 60% of stories, treat option 3 as option 2 and redo the cost decision.
- Stop using the alternate arm when M3 is above 0 on 2 or more alternate-arm stories after R8 is in place.
- Replace the section 5 tables with the measured calls. Evaluate the accuracy-check candidate of section 4 against the missed conflicts.

## 8. Risks and failure modes

<!-- Source: Base risks 1 to 8, plus Variant 2 and debate additions. Likelihood is an ESTIMATE, not measured -->

| # | Risk | Likelihood | Impact | Guard |
|---|------|------------|--------|-------|
| 1 | Stale behavior behind paths that still exist (T1 and T2 miss it) | Medium | High | Shadow runs; M2; classify every executor halt |
| 2 | The adversarial merge rewords or drops a criterion | Medium | High | R6 rebuild; R1 to R3 re-check after the merge (R8) |
| 3 | `/sc:workflow` drops or merges id tokens (UNVERIFIED whether it keeps them) | Medium | Medium | R4 check; one rerun with the token rule quoted; then escalate |
| 4 | `/sc:implement` reads a task reference `(AC: 2)` as the criterion itself (AC QUALIFY rule 1 matches an `AC:` token, `SKILL.md` line 98; the exact misread is untested) | Medium | High | `story-gate` inlines the full text; R4 rejects reference-only blocks |
| 5 | A normative conflict stalls a story | Medium | Medium | R5: one escalation; other stories carry on |
| 6 | Triggers over-fire and erase the savings (T4 list, T5, new files) | Medium | Medium | New-path skip; per-trigger precision; 60% rule |
| 7 | Brainstorm convergence falls below 0.50 and the brainstorm fails | Low | Medium | Fall back to the default arm, record it in `gate.json`, review it under M2 |
| 8 | Spec-panel reaches review 3 with a FAIL | Low | Medium | Escalate under its own cap; no fourth review |
| 9 | The scripts are not built or are late | High | High | Named owner; the trial does not start without them |
| 10 | Call counts understate the real cost | Medium | Medium | Log tokens and wall time (section 5) |
| 11 | No coordinator is available to answer an R2 or R5 escalation | Low | Medium | Escalations are counted in M4; stories wait, none proceeds |
| 12 | A hand-edited story is malformed | Low | Medium | Shape stop (section 3) |

## 9. Out of scope and open items

Out of scope: creating epics and stories, sprint-status updates, the pull request and the release gate, `bmad-dev-story` (IronClaude does the executing), `/sc:design`, and money estimates.

Open items:
- Build `story-gate` and `ac-map-check`; assign an owner (UNVERIFIED who). `--repair` is the largest piece.
- Every call count, threshold and likelihood is an ESTIMATE; the trial measures them.
- UNVERIFIED: whether `/sc:workflow` keeps the id tokens; whether `/sc:spec-panel` spawns agents; how often Dev Notes are stale; the exact tokens per step.
- This is a recommendation. The owner decides whether to adopt it; nothing here was approved.

## 10. Debate status and adjudicated points

<!-- Source: Orchestrator, from debate-transcript.md and base-selection.md -->

Convergence 65.4% (17 of 26) against a threshold of 75%, depth quick (1 round; the invariant probe is skipped at this depth). Combined scores: Variant 1 0.960, Variant 2 0.867. Both variants chose option 3 with the BMAD story as the default; the debate was about triggers, merge rules, cost counts and conflict handling. The nine unresolved points were settled from the evidence read after the debate: S-001 (numbered headings, V2), S-004 and C-008 (trial: merged), C-002 (location-based panel trigger, V1), C-003 and X-002 (cost: formulas merged, arithmetic corrected), C-004 (full id canonical), A-002 (keep both post-workflow checks), A-006 (coordinator dependency stated).
