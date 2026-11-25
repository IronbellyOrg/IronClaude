# Spec: who writes the spec at the BMAD to IronClaude hand-off of one story

## Recommendation

Use option 3, with option 1 as the default. The BMAD story becomes the spec: IronClaude tags its criteria, reviews it once with `/sc:spec-panel` and plans from it. Option 2 (an IronClaude brainstorm merged with the story) runs only when one of the seven triggers below fires.

Why: `bmad-create-story` already writes an LLM-researched, code-aware story, and IronClaude's own issue chains (`~/.claude/skills/sc-issue-protocol/refs/chains.md`) already skip the brainstorm for simple work. Running a second spec on every story costs about 4x the hand-off calls, mostly to re-derive what BMAD wrote. The code-grounded pass is worth its cost only when the story's code facts are stale or the work crosses subsystems.

Where the boundary sits: BMAD owns the what (the acceptance criteria and the architecture decisions). IronClaude owns the how, and the facts about today's code.

## Hand-off flow

Two scripts in this flow are proposals and do not exist yet: `story-gate` and `ac-map-check`. `<D>` is a proposed run folder, `.dev/stories/<epic>-<story>/`.

**Default path (no trigger fires):**

1. `story-gate <story.md> --out <D>` (a script, no model call). It checks T1-T5 and T7 and writes `<D>/gate.json`. It also writes `<D>/spec.md`: a copy of the story where each criterion is tagged `[S<e>.<s>-AC<n>]`, each task's `(AC: #)` reference is replaced by the full criterion text, and two empty tables are added, `## AC change log` and `## Dev Notes corrections`.
2. `/sc:spec-panel @<D>/spec.md --mode critique --focus requirements,testing --unattended --report-dir <D>/panel`. Check T6 against its report.
3. `ac-map-check <D>/spec.md <story.md>`, which enforces R1, R2 and R7.
4. `/sc:workflow <D>/spec.md --depth quick --handoff none --unattended --report-dir <D>/wf`.
5. `ac-map-check --tasklist <plan path> <D>/spec.md`, which enforces R4.
6. `/sc:implement <plan path>`.

**Alternate path (any trigger fires at step 1, or T6 fires at step 2):**

1. Run `story-gate` as above.
2. `/sc:brainstorm "code-grounded spec for story <e>.<s> @<D>/spec.md" --codebase --depth quick --blind --unattended --report-dir <D>/bs`. Use `--depth standard` when T3 or T4 fired.
3. `/sc:adversarial --compare <D>/spec.md,<brainstorm merged-requirements.md> --depth quick --focus correctness,architecture --unattended --report-dir <D>/adv`.
4. `ac-map-check --repair <D>/adv/<merged output> <D>/spec.md`. It rebuilds the spec under R7 and writes a second version of `<D>/spec.md`.
5. Run `/sc:spec-panel` (same flags) on the new spec, then `ac-map-check`.
6. If any `## AC change log` row says `proposed`, stop and escalate to the coordinator. Otherwise run `/sc:workflow --depth standard` (`deep` when T3 and T4 both fired), then `ac-map-check --tasklist`, then `/sc:implement`.

`/sc:design` is not run on either path, because BMAD's architecture document already is the design.

## Triggers

This list is closed: nothing outside it switches the path.

- "Named paths" are the backticked repository paths in the story's Dev Notes, Project Structure Notes and References.
- "Story commit" is the output of `git log -1 --format=%H -- <story.md>`.

1. **T1, missing path:** at least one named path does not exist at HEAD.
2. **T2, drift:** since the story commit, the named paths have 3 or more commits, or 150 or more changed lines (`git diff --shortstat <story commit>..HEAD -- <paths>`).
3. **T3, cross-subsystem:** the named paths have 2 or more distinct 3-segment path prefixes.
4. **T4, risk class:** the story text or criteria match this case-insensitive regex: `migrat|schema|postgres|database|storage|protocol|wire format|auth|secret|permission|encrypt`. This covers the complex rubric's security and data-migration classes, plus storage and protocol work.
5. **T5, size:** more than 6 criteria, or more than 6 top-level tasks.
6. **T6, panel code gap:** the spec-panel report has a blocking finding located in Dev Notes, Project Structure Notes or Tasks. A blocking finding on criterion text is not a trigger: it becomes an R2 row instead.
7. **T7, ungrounded story:** the story has zero named paths.

The T2 and T5 thresholds are estimates that the trial calibrates.

## Cost comparison

**Counting rule:**

- One model call is one agent context that produces output. The command session counts as 1, and each spawned subagent counts as 1.
- A script counts as 0 calls but 1 step. A step is one command or script run.
- `/sc:implement` is left out because it runs the same tasklist size under every option.

**Story sizes:** simple means 3 or fewer criteria in one area; medium means 4 to 6 criteria; complex means more than 6 criteria, or T3 or T4 fired.

**Every call count below is an ESTIMATE from the protocol text.** The one sourced figure is about 80K tokens per quick brainstorm proposal, which is `/sc:brainstorm`'s own estimate.

| Option | Simple (calls / steps) | Medium (calls / steps) | Complex (calls / steps) |
|---|---|---|---|
| 1: story plus spec-panel | 4 / 5 | 6 / 5 | 8 / 5 |
| 2: both specs on every story | 18 / 8 | 23 / 8 | 30 / 8 |
| 3: option 1 by default, option 2 on a trigger | 4 / 5 | 6 or 24 / 5 or 8 | 31 / 8 |

How the estimates break down:

- **Option 1.** Spec-panel takes 1 call per review plus 1 reviser call per fix cycle: 1, 3 and 5 calls for simple, medium and complex. `/sc:workflow` takes 3 calls (planner, the `/sc:reflect` pre-review, writer).
- **Option 2.** The brainstorm takes 9, 11 or 14 calls (session, analyze, 2 to 4 proposals, the inner adversarial run). The compare takes 5, 6 or 8 calls. Spec-panel takes 1, 3 or 5, and the workflow takes 3.
- **Option 3.** When T6 is what fires, it adds the 1 panel call already spent. In practice T3 or T4 nearly always fires on complex stories.
- **Expected cost.** If 30% of medium stories trigger (an UNVERIFIED rate), option 3 averages about 0.7 x 6 + 0.3 x 24 = about 11 calls per medium story, against 23 for option 2.

## Merge rules

1. **R1:** Every story criterion n appears in the spec's `## Acceptance Criteria` as `[S<e>.<s>-AC<n>] <text>`, byte-identical to the story after trailing whitespace is trimmed. `ac-map-check` tests this with a diff.
2. **R2:** A BMAD criterion is removed or reworded only through an `## AC change log` row with these fields:
   - id;
   - old text;
   - new text, or `removed`;
   - reason: `contradicts-code`, `ambiguous` or `duplicate`;
   - evidence as `path:line@<sha>`;
   - status: `proposed` or `approved`;
   - approver: the coordinator session name.

   A worker may write only `proposed`. Any `proposed` row stops the hand-off before `/sc:workflow`.
3. **R3:** Criteria that IronClaude adds get ids `[IC-<n>]` in a separate `### IronClaude criteria` list. Each one names the BMAD id it supports (or `none`) and its source file. BMAD ids are never renumbered.
4. **R4:** In the tasklist, every line of every task's criteria block starts with exactly one `[S..-AC<n>]` or `[IC-<n>]` token. Each executor id `T<i>.AC<k>` then maps to a story id by text match. Every BMAD id must appear in at least 1 task, and no block may hold only id references. This is checked after `/sc:workflow` and before `/sc:implement`.
5. **R5:** A factual conflict, where the Dev Notes state a path, function or signature that the code contradicts, is settled in favor of the code, with no person involved. It is recorded as a `## Dev Notes corrections` row: the story's claim, the code fact, and `path:line@<sha>`.
6. **R6:** A normative conflict, where a criterion or BMAD architecture constraint cannot hold against the code or the brainstorm argues it should change, is settled in favor of the story. The worker writes an R2 `proposed` row and escalates. The coordinator then approves it, rejects it, or sends the story back to BMAD (`bmad-correct-course`). Nothing runs against a contested criterion.
7. **R7:** The adversarial merged output is an input, never the spec:
   - its criteria section is thrown away and rebuilt under R1;
   - a reworded criterion becomes an R2 `proposed` row, and a new one becomes an R3 row;
   - spec-panel fixes may edit only the sections that are not criteria, and a blocking finding on criterion text becomes an R2 row.
8. **R8:** IronClaude edits only the story's `## Dev Agent Record` section. There it appends the paths of `spec.md`, the T-to-AC map and the corrections table, so the next `bmad-create-story` run learns from them. Test: a diff of the story outside that section is empty.

## Trial plan

**Scope:** run one release with every story going through this flow. If the release has fewer than 10 stories, carry the trial into the next release before deciding.

**Record per story in `<D>/gate.json`:**

- the path taken and the triggers that fired;
- hand-off calls and wall time;
- the number of Dev Notes corrections and R2 rows;
- `E-HALT-QA` and `E-NO-AC` halts, and QA retries;
- for each failure, whether it was spec-caused: the fix needed a code fact the spec lacked or got wrong.

The T1 and T2 fire rate measures how often Dev Notes are stale, which is the brief's biggest unknown.

**Shadow runs:** on every third default-path story (at least 3), also run alternate steps 2-4 without executing the result. Count material deltas: corrections or R2 rows that would change a task.

**Decision rules:**

- Keep the default if spec-caused failures on default-path stories are 10% or less and shadow material deltas are 20% or less.
- Make option 2 the default if spec-caused failures are over 25% or shadow material deltas are over 40%.
- Anywhere in between, keep the default and add or tighten triggers based on the failed stories.
- Remove a trigger whose firings produced no corrections and no R2 rows in 80% or more of cases (at least 3 firings).
- If triggers fire on more than 60% of stories, treat option 3 as option 2 and redo the cost decision.

## Risks and failure modes

1. **Stale behavior behind paths that still exist (T1 and T2 miss it).** Guard: the shadow runs, plus classifying every executor halt; a spec-caused halt feeds a trigger review.
2. **The adversarial merge rewords criteria.** Guard: R1 and R7 repair the spec, and `ac-map-check` fails the hand-off on any missing BMAD id.
3. **`/sc:workflow` drops or merges id tokens (UNVERIFIED whether it keeps them).** Guard: the R4 check, then one rerun with the token rule quoted in the prompt, then escalation.
4. **`/sc:implement` reads a task title like `(AC: 2)` as the criterion itself.** AC QUALIFY rule 1 matches an `AC:` block, so the executor's first criterion for that task (T1.AC1) could become "2". Guard: `story-gate` replaces references with full text, and R4 rejects blocks that hold only references.
5. **A normative conflict stalls an unattended worker.** Guard: R6 stops with a single escalation, and other stories carry on.
6. **The T4 regex over-fires and wipes out the savings.** Guard: per-trigger precision in the trial, plus the 60% rule.
7. **Brainstorm convergence falls below 0.50 and the brainstorm fails.** Guard: fall back to the default path and note it in `gate.json`.
8. **Spec-panel reaches review 3 of 3 with a FAIL.** Guard: escalate under spec-panel's own cap; there is no fourth review.

## Out of scope and open items

**Out of scope:** creating epics and stories, sprint-status updates, the PR, the release gate, `bmad-dev-story` (IronClaude does the executing), and `/sc:design`.

**Open items:**

- `story-gate` and `ac-map-check` have to be built. Both are small, deterministic scripts. The `<D>` path and the scripts' flags are proposals.
- Every call count and the T2 and T5 thresholds are estimates for the trial to measure.
- UNVERIFIED:
  - whether `/sc:workflow` keeps the id tokens;
  - whether `/sc:spec-panel` spawns subagents;
  - the exact path of `merged-requirements.md` under `--unattended`;
  - how often Dev Notes are stale.
