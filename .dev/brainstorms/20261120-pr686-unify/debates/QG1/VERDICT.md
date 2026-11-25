# Verdict QG1: Planning and hand-back (OD-1, OD-2, OD-13)

Reading notes: "D:nnn" means line nnn of Clay's design `docs/designs/orchestrator.md` (merged by PR 681, Clay's design pull request). "PR 686" is Clay's rewrite of the issue watcher. "PR 690" adds `/sc:issue --plan` and `--remaining`. "PR 682" is Clay's deletion of the plan-approval code. "D15" is the earlier verdict that listed these open questions; its answers are its own recommendations, not owner records.

## Question

QG1 Planning and hand-back: OD-1 (default plan_depth for the plan call), OD-2 (how hand-back round 2 starts: re-plan and re-approve vs carry the remaining list), OD-13 (a hand-back waiting for re-approval versus the in-flight count)

(Topic block verbatim from `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/TOPICS.md`, line 71.)

## Winner

HYBRID: OURS wins all three contested rules (default `quick`, re-plan then re-approve, a waiting step is not counted), and one separable Clay benefit set is adopted (the hand-back loop bounds and the per-repo depth option).

## Winning recommendation

Each answer below is a recommendation. The owner gives the answer in chat and the agent records it (D15 section 7).

1. **OD-1, default depth of the plan call: `quick`.**
   - Answer: the setting is one plain key `plan_depth`, passed straight to `/sc:issue --plan --depth`. Unset means `quick` (the `--plan` default, run by the cheapest worker `issue-worker-t3`). A repo may set `standard` or `deep` for itself. There is no `plan_tier` and no tier-to-depth table.
   - Reason: nobody has measured plan quality or cost per depth (D12 item 6 records "no cost baseline", about the create-time floor), the table that would map `plan_tier` to a depth is not on master (UNVERIFIED), and the person's approval is the quality gate because the plan check proves only that three headings are filled in. Both advocates, Clay's included, sided with `quick`.
   - Source: D15 section 7 OD-1 row; merged D15 position G-2; design D:60 and D:722-726 (Clay's `plan_tier`); `debates/QG1/adversarial/adversarial/debate-transcript.md` (C-001 66%, C-002 72%).
   - Testable: `repos` validation accepts `plan_depth` of quick, standard or deep and refuses anything else; an unset key gives `--depth quick`; a repo's own value beats the default for that repo.
2. **OD-2, how hand-back round 2 starts: option (a), re-plan the body and the person re-applies the approval.**
   - Answer: round 2 and later run the re-plan (`/sc:issue --plan <N> --remaining <file> --depth <d>`), then wait for the person to re-apply the approval, then pass the start gate again. No separate chat go per round. The check at the moment of start repeats the approval, not only `hold:backlog` and `plan_check`. Option (b) (leave the body alone and carry the remaining list in the handoff round block, D:619) is the owner's cheaper alternative, not the default.
   - Reason: a body edit after approval voids the approval (`predicates.py:249-259` in master, function `unchanged_since`), so a re-plan without re-approval starts a worker on a body nobody approved. Clay's text has no round-2 gate (wave 1 is not re-run, D:615; the wave-1 re-check covers only `hold:backlog` and `plan_check`, D:488), and Clay's advocate conceded this.
   - Source: D01 VERDICT item 5 and item 3 (MR-1); D15 R-6; design D:610-620; debate points C-003 (78%), X-003 (79%).
   - Testable: removing the approval between the wake and the start refuses the start; a re-plan voids an earlier approval; no worker starts for a waiting issue before the start gate passes, including after a coordinator restart.
   - Dependency (UNVERIFIED): whether the restored plan-approval flow (WC-17, deleted by PR 682) can serve as this gate; it exists only if the owner decides both gates stay (D14).
3. **OD-13, a hand-back waiting for re-approval versus the in-flight count: do not count it.**
   - Answer: the waiting step does not count toward `max_in_flight`, shows a visible waiting reason, and gets an expiry only if waiting issues pile up. Carrier (recommended, side effects UNVERIFIED): the state file takes status `escalated` with step `handback_awaiting_approval(body_sha)`, which `route.in_flight` already skips (`route.py:399`); on re-approval a wake path repeats the full start check and sets the file back to `in_progress` at wave 4.
   - Reason: a waiting issue has no worker; counting it means three waiting issues make the repo answer `coordinator_full` to new work while nobody works (C-INV-1). Clay's own design already frees the place for an issue that waits on a person (D:605, state file `escalated` "so the issue leaves the places in flight").
   - Source: `route.py:379-426` (snapshot pr-a); D:605, D:608, D:616; D15 C-INV-1 and C-INV-2; debate points C-004 (76%), X-002 (55%, the one split point).
   - Testable: with three issues waiting for re-approval, a new issue of the same repo is not refused with `coordinator_full`; a waiting issue returns to counting only when set back to `in_progress`.
   - Open points (UNVERIFIED): D:616 says "Nothing is escalated for a hand-back", so using `escalated` extends the design and its row-9, `stalled` and `--take` effects (D:608, D:617) need checking; the set-back can overshoot `max_in_flight` if new work took the place (allow one slot of overshoot or require a free place); which component runs the wake path is not decided (the poll never wakes an acknowledged entry, `cycle.py:993-994`).
   - If the owner picks option (b) at OD-2, this question does not arise (nothing waits).

## Strongest points

**OURS**
1. A re-plan voids the approval and Clay's text has no gate that replaces it; Clay's advocate conceded it (`predicates.py:249-259` in master; D:488, D:615; debate transcript, V2 concessions).
2. Counting only live work is the code's own rule: `route.in_flight` skips `done`, `skipped`, `failed` and `escalated` files (`route.py:393-399`), and the design itself frees the place on `escalated` (D:605).
3. `quick` is the documented `--plan` default and the `deep` alternative rests on a table that is not on master and on no cost baseline (merged D15 G-2; design D:726).

**CLAY**
1. The hand-back loop is fully specified and restart-safe: verb `handback` with stop reasons `no_remaining`, `cap`, `no_progress`; the old worker must be final first; read-then-write steps (D:612-614, D:620). The owner's line has nothing equivalent.
2. The re-plan is idempotent and narrow: marker `<!-- sc:issue:replan round=<n> -->`, only `## Fix approach` and `## Test plan` are replaced, done items are kept (D:1078-1080).
3. Goal G6 (stronger models plan, cheaper models build) is a real quality lever and a weak plan costs in every later wave (D:60, D:722); a per-repo `plan_depth` keeps it without the unverified table.

## Clay strengths to adopt

- **Hand-back loop bounds, old-worker-final rule, idempotent re-plan marker and `--remaining` replacement (D:612-614, D:620, D:1078-1080).** Why: clear gap in the owner's line (no loop mechanics; rubric score, `base-selection.md`), and they hold under any start rule (both advocates, C-006 86%). How to merge: put them in the spec's hand-back section unchanged, and add the waiting step for re-approval between "re-plan written" and "start gate" (OD-2 a). The `--remaining` option is built in PR 690, which D12 already marks keep-and-adapt; this makes the hand-back its first caller.
- **G6 as an option, not a default.** Why: a real lever (D:60) that the plain `plan_depth` key can serve per repo. How to merge: `plan_depth` per repo; document that `deep` runs the planner up to four times per issue because the re-plan passes the same depth (D:618).
- **The start re-check must repeat the approval.** Why: Clay's own fact (D01 MR-1: the wave-1 re-check covers only `hold:backlog` and `plan_check`, D:488) is a verified gap in the design. How to merge: the spec's re-check lists approval, `unchanged_since`, Status allow-list, `plan_check`, `hold:backlog`.

## Our strengths that must be kept

- A human approval between a plan edit and a new worker (owner rules R19 and R22; D01).
- No second approval mechanism: no per-round chat go, no `answer-check` per round, no `handback_awaiting_go` (D15 R-6).
- The two invariants from the invariant probe: C-INV-1 (a waiting issue must not hold a place) and C-INV-2 (something wakes the coordinator after re-approval).
- `quick` as the cheap default with the approval as the quality gate.
- Counting rule based on code, not on a new mechanism (`route.in_flight`).

## Actions

| Action | Type (LOCAL CHANGE / PR KEEP / PR REVERT / PR KEEP-ADAPT / PR CLOSE / DOC / DECISION) | Target (file, PR or issue number) | Order or dependency |
|--------|------|--------|-------|
| Owner answers OD-1, OD-2, OD-13 in chat; the agent records each answer | DECISION | Owner; D15 section 7 | First; nothing below is final before it |
| Replace `plan_tier` with `plan_depth` (default quick, per-repo override, validated to quick, standard, deep) in the spec and the per-repo config | DOC | Orchestrator spec; D15 C3/R-3 per-repo JSON | After the OD-1 answer |
| Rewrite the hand-back wave (D:610-620): round above 1 re-plans, then waits for the start gate; add the re-check list; rewrite test T12 | DOC | `docs/designs/orchestrator.md` text (PR 681) or its successor spec | After the OD-2 answer; needs the D14 outcome on restoring WC-17 |
| Add the waiting-step rule and the three open-point checks (row 9, `stalled`, `--take`; overshoot; wake component) | DOC | Spec section 5.5 and 5.7 | After OD-13 answer; before any build |
| Check the side effects of status `escalated` for a waiting hand-back against D:608, D:616, D:617 and `route.py:399` with a test on a fake state file | LOCAL CHANGE | `issue_watch/route.py` tests (planb or adapted PR 686) | Before building the waiting step |
| Keep the loop bounds, old-worker-final and the idempotent marker in the spec as written | DOC | Spec hand-back section | With the OD-2 rewrite |
| Merge `--remaining` with the four adaptations D12 lists; the hand-back becomes its first caller | PR KEEP-ADAPT | PR 690 | Lane 1, per D15/D14 order |
| Correct D15's OD-1 supporting row: D12 item 6 is a related create-time deferral, the direct source is merged D15 G-2 | DOC | `debates/D15/VERDICT.md` section 7 | Low priority; when D15 is next edited |

## Implications

- **OD-1.** Watcher and claim pipeline: the plan call (`/sc:issue --plan`) runs the cheapest planner unless a repo opts in; no `plan_tier` code is needed in PR 686's `repos.py`, which D14 says does not land. Dashboard: none. Owner must know: `quick` plans pass the check on presence alone, so the person's approval is the only quality gate.
- **OD-2.** Coordinator or orchestrator: a hand-back issue stops after the re-plan and waits for the person; after approval something must wake it (the poll never wakes an acknowledged entry, `cycle.py:993-994`) and repeat the whole start check. Claim pipeline: PR 690's `--remaining` gets its first caller. What breaks: Clay's text at D:610-620 and tests T1, T3, T4, T8, T10, T11, T12 as D15 lists them. Owner must know: if D14 does not restore the plan-approval flow (WC-17), round 2's gate is the start approval alone.
- **OD-13.** Watcher: `max_in_flight` is untouched; the count rule needs no new code if the carrier is a status the counter already skips. Dashboard: a new visible reason "waiting for approval" must reach the sweep and the observer (D15 dashboard note). Coordinator: the wave-0 restart rule resumes `in_progress` files, so an `escalated` waiting file is not resumed by a restart; its entry is `stalled` if its orchestrator is down and `--take` refuses it. What breaks: nothing built yet; PR B does not exist. Owner must know: using `escalated` is not stated in the design, so it is a recommendation with checks, not a given.

## Confidence

About 75% overall. OD-2 about 78% (the loss of approval on re-plan is shown by code and conceded by Clay's advocate). OD-1 about 66% (a tie resolved by the weighting rule, no measurement on either side). OD-13 about 70% on the answer and about 50% on the carrier (side effects unchecked).
What would change it: a measured quality or cost difference between `quick` and `deep` plans; an owner choice of option (b) at OD-2; a check showing `escalated` triggers row-9 notices or blocks the wake path; the `refs/intake.md` table showing `tier1b` maps to `quick`.

## Unverified

- The `plan_tier` to `--depth` table in `refs/intake.md` of PR P (not on master); whether `tier1b` implies `deep`.
- Whether the restored plan-approval flow (WC-17) can serve as the round-2 gate; whether the owner decides both gates stay (D14).
- Side effects of status `escalated` for a waiting hand-back (D:616 says nothing is escalated for a hand-back; row-9, `stalled`, `--take`), the `max_in_flight` overshoot, and the component that runs the wake path.
- Fidelity of `--remaining` in keeping done items (U60, D:1081); `HANDBACK_MAX` = 3 is "not measured" (D:612).
- Whether the counting code of PR 686 survives its adaptation (D14); `route.py` was read in snapshot pr-a only.
- Scoring limits: both advocates were given the owner's weighting rule and one conceded early, so the high convergence (15 of 16) partly reflects the rule; the six-case re-evaluation of the rubric was done by the orchestrator, who also wrote the diff analysis; the quantitative layer uses crude counts and barely separates the variants. D15's OD answers are its own tie-breaks (D15 Unverified), so this debate tested them but did not replace the owner's decision.

## Debate artifacts

All under `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/QG1/`:
- `position-OURS.md`, `position-CLAY.md` (position papers)
- `adversarial/adversarial/diff-analysis.md`
- `adversarial/adversarial/debate-transcript.md`
- `adversarial/adversarial/base-selection.md`
- `adversarial/adversarial/refactor-plan.md`
- `adversarial/adversarial/merge-log.md`
- `adversarial/adversarial/return-contract.yaml` (the skill's own contract)
- `adversarial/merged-qg1-position.md` (merged output)
- `adversarial/return-contract.yaml` (worker contract)
- `adversarial/adversarial/variant-1-original.md`, `variant-2-original.md` (normalized copies)
