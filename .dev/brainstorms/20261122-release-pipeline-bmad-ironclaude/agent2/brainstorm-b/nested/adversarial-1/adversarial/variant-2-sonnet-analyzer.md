# Spec: Who writes the spec at the BMAD to IronClaude hand-off of one story

## 1. Recommendation

Default is option 3 with option 1 as the default arm. IronClaude accepts the BMAD story file as the spec and runs `/sc:spec-panel` on it. The code-grounded IronClaude spec plus `/sc:adversarial --compare` (option 2) runs only when a trigger in section 3 fires.

Reasons:
- The story is already an LLM-researched, code-aware artifact (verified in `bmad-create-story` SKILL.md), so a second spec pass on every story mostly repeats work.
- The installed issue chains already run no brainstorm for simple work (taken from the enrichment notes, not re-read in this pass).
- Option 2 adds a second adversarial merge, which is a new place for acceptance criteria (AC) to be lost.

## 2. Hand-off flow

Inputs: story file `S` (status `ready-for-dev`), repo at HEAD.

**Default arm (option 1):**
1. `check-story S` (script, 0 model calls) evaluates T1 to T4. If none fires, continue.
2. `/sc:spec-panel @S --mode critique --focus requirements,testing,architecture --unattended`. Re-review up to the verified cap of 2 fix cycles (3 reviews). Review 3 with FAIL halts and escalates to the coordinator; it never switches arms.
3. Evaluate T5 on review 1. If it fires, go to the alternate arm step 2.
4. `/sc:workflow S --depth standard --handoff none`. The tasklist package keeps a byte-exact copy of `S` (per the topic file).
5. Write `ac-map.md` (R3), then `/sc:implement <package>`.

**Alternate arm (option 2, when T1, T2, T3 or T4 fires, or T5 after step 3):**
1. Script fires T1-T4, so no panel has run yet. If T5 fired, a panel review already exists and the panel in step 4 is a re-review.
2. `/sc:brainstorm "<story title> @S" --unattended --blind --codebase --depth quick --proposals 2 --handoff none --output <dir>/brainstorm` (3 proposals when T3 fired). Output: `merged-requirements.md`.
3. `/sc:adversarial --compare S,<dir>/brainstorm/merged-requirements.md --depth quick --focus requirements --unattended --output <dir>/merge`. Output: `merged-spec.md`, which must satisfy R1 to R9.
4. `/sc:spec-panel @<dir>/merge/merged-spec.md --mode critique --unattended`, same cap.
5. `/sc:workflow merged-spec.md --depth standard --handoff none`, then `ac-map.md`, then `/sc:implement`.

## 3. Triggers

The list is closed: T1 to T5 are the only switches, and a coordinator may not add or waive one mid-release. T1 to T4 are computed by `check-story`. Existing-path checks skip any path the story marks `(new)`.

1. **T1, missing path:** at least 1 repo path in the story's Dev Notes (backticked token with `/` and a file extension) does not exist at HEAD.
2. **T2, code churn:** at least 3 commits on master since the story file's creation commit touch the existing paths listed in Dev Notes (`git log <story-commit>..HEAD -- <paths>`).
3. **T3, size or blast radius:** any one of:
   - more than 8 numbered AC;
   - more than 12 tasks;
   - listed paths span at least 3 distinct top-level directories (first 2 path segments);
   - story text matches `migration|schema|DDL|Postgres|credential|secret|auth|wire format|protocol version`.

   This is the observable form of the complex rubric (more than one subsystem, security, data migration). The ">16 hours" test is replaced by these counts because hours are not observable by a script.
4. **T4, not executable as written:** any of:
   - 0 AC;
   - any task without an `AC: #` reference;
   - any AC with none of the words Given, When, Then;
   - Dev Notes with 0 file paths.
5. **T5, panel finding:** spec-panel review 1 returns `verdict: FAIL` with at least 2 blocking findings tagged requirements or architecture.

## 4. Cost comparison

**Counting rule:** one model call is one subagent or one single-session protocol pass; one step is one command or script run in the hand-off. `/sc:implement` cost is identical across options and excluded. Scripts cost 0 calls.

| Item | Count |
|---|---|
| spec-panel review | 1 call, 1 step per review |
| `/sc:workflow` | 2 calls (plan plus pre-review), 1 step |
| brainstorm unattended quick | P proposals + 1 analyze + 4 inside the adversarial merge = P+5 calls, 1 step |
| `/sc:adversarial --compare` quick | 4 calls, 1 step |

P is 2, or 3 for complex. R is the number of panel reviews: 1 simple, 2 medium, 3 complex.

| Option | Simple (R=1) | Medium (R=2) | Complex (R=3, P=3) |
|---|---|---|---|
| 1, BMAD only | 3 calls, 2 steps | 4 calls, 3 steps | 5 calls, 4 steps |
| 2, always both | 14 calls, 4 steps | 15 calls, 5 steps | 18 calls, 6 steps |
| 3, default arm | 3 calls, 3 steps | 4 calls, 4 steps | 5 calls, 5 steps |
| 3, alternate arm | 14 calls, 5 steps | 15 calls, 6 steps | 18 calls, 7 steps |

The alternate arm is option 2 plus 1 script step. If it is reached by T5, it also carries the earlier panel review (+1 call, +1 step).

All counts are estimates from the protocol texts. The 4 calls per adversarial run and the 1 analyze call are not measured. The verified facts are: the quick-depth brainstorm estimate of about 80K tokens per proposal, the 6 artifacts per adversarial run, and the 2-fix-cycle cap. Option 2 costs about 3 to 5 times option 1 in calls.

## 5. Merge rules

Rules R1 to R9 apply to the default arm too, where "merged spec" reads as "story after panel revision". Each is checkable by a script.

- **R1** Every BMAD AC id `n` in `S` appears in the spec as `AC-n`. Failure: any id is missing.
- **R2** BMAD ids are never renumbered or reused. IronClaude-added criteria use `AC-IC-k` and carry a `[IC]` tag. Failure: any `AC-n` text differs in meaning from `S` without an R6 entry.
- **R3** `/sc:workflow` output carries `ac-map.md` with rows `AC-n -> T<i>.AC<k>`. Every BMAD id has at least 1 row, and every task `AC:` block cites its BMAD ids. Failure: row count for an id is 0.
- **R4** Conflict between story and code:
  - Code wins on facts: paths, symbols, signatures, current behaviour.
  - The story wins on intent: the acceptance outcome and architecture constraints taken from the architecture doc.
  - If the code makes an AC outcome impossible, the worker marks that task `BLOCKED-AC-n` and records the conflict in `deviations.md`. It sends a coordinator message and continues the other tasks. It never edits the AC itself.
- **R5** Every merged line is tagged `[BMAD]`, `[IC]` or `[BOTH]`. Failure: untagged lines.
- **R6** An AC may be reworded, split or dropped only through a `deviations.md` row with the fields: AC id, story text, new text, evidence (`file:line`), who decided (R4 rule or coordinator). Check: a diff of normalized AC text against `S` shows every change listed.
- **R7** `S` is stored byte-exact as `source-story.md` in the package. IronClaude edits only the story's Dev Agent Record section, never AC or tasks. The spec-panel reviser edits only text a blocking finding names, and any AC change it makes needs R6.
- **R8** After the panel and after the merge, a script re-runs R1 and R6. Any failure blocks `/sc:workflow`.
- **R9** A story is complete only if each `AC-n` has a passing executor row or an R6 or R4 row.

## 6. Trial plan

Run one release of at least 12 stories on the default (option 3). If there are fewer than 12, extend into the next release. Record per story:
- M1: which triggers fired, plus calls and wall-clock minutes per step.
- M2: "missed conflict" count. This is a story that fired no trigger but still produced an R4 `deviations.md` row about a fact, or a task that failed first-pass QA and was traced to stale Dev Notes.
- M3: AC loss, meaning any R1 or R6 failure after R8.
- M4: coordinator escalations.

Decision thresholds:
- **Keep the default** if both hold: missed conflicts are at most 10% of non-triggered stories, and triggers fire on at most 40% of all stories.
- **Make option 2 the default** if missed conflicts are 25% or more of non-triggered stories, or the fire rate of T1 or T2 is 50% or more. Open the staleness item in section 8.
- **Tighten triggers and re-run** if missed conflicts are between 10% and 25%. Lower T2 to 2 commits first.
- **Stop using option 2** if M3 is greater than 0 on 2 or more alternate-arm stories after R8 is in place.

## 7. Risks and failure modes

1. **Stale Dev Notes that pass T1 and T2** (the path exists but the behaviour changed). Guard: M2 is measured. R4 halts the task, not the release.
2. **The merge rewords or drops an AC.** Guard: R1, R6 and R8 scripts block `/sc:workflow`.
3. **The panel reviser rewrites ACs.** Guard: R7 limits it to blocking-finding text, and R8 re-checks after the revision.
4. **Executor ids drift from the BMAD ids.** Guard: R3 `ac-map.md` check before `/sc:implement`.
5. **Trigger thresholds are too loose or too tight.** Guard: M1 fire rate and the section 6 rules.
6. **The story and code conflict mid-run and a worker cannot ask.** Guard: R4 marks the task `BLOCKED-AC-n` and escalates to the coordinator.
7. **The brainstorm re-derives something BMAD already decided.** Guard: R4 gives the story the win on architecture constraints, and `--blind` limits anchoring on the story.
8. **The cost estimates are wrong.** Guard: M1 is compared with section 4, and the table is revised after the trial.

## 8. Out of scope and open items

Out of scope: epics, sprint status, the PR and the release gate, money estimates, and feeding corrections back to the BMAD story or the `sprint-status.yaml` file.

Open items:
- The staleness rate of BMAD Dev Notes is UNVERIFIED.
- The model-call count per adversarial run is UNVERIFIED.
- The `current` or `out_of_date` check of `/sc:issue --claim` could not be confirmed in the installed `chains.md` (grep found nothing). T1 and T2 are therefore scripts and do not reuse it.
- I did not re-read `refs/retry.md`, so `T<i>.AC<k>` rests on the enrichment notes. Only the `AC:` block requirement in `/sc:implement` SKILL.md line 98 was re-read.
- Whether `/sc:workflow` preserves `AC-n` ids from a merged spec is UNVERIFIED and is checked by R3.
- Verified in this pass: the spec-panel cap of 2 fix cycles and 3 reviews, and the `--unattended` mode of spec-panel.
