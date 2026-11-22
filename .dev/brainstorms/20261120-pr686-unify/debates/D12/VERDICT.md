# Verdict D12: `/sc:issue` plan sections and moving design into create

## Question

Clay's PRs 651/661 (merged), 689 and 690 (open) add plan sections to `/sc:issue`, `--plan`, `--remaining`, and move brainstorm and design from claim into create, which changes the owner's claim chain (`sc-issue-protocol/refs/chains.md`, `--pipeline none` claim, `/sc:issue` designs). Keep, adapt or reject, and how does it fit the claim-to-work pipeline?

Fact correction found while debating: 651 is an issue (the request) and 661 is the merged PR that closes it; 689 is an open issue (not a PR, nothing built); 690 is the open PR (branch `issue-655-pr-p`, "PR P" of Clay's design) that adds `--plan` and `--remaining`.

## Winner

HYBRID (OURS is the base): keep the owner's claim chain and reject moving brainstorm and design into create, but adopt Clay's plan sections, `--plan` with `plan_body.py`, `--remaining` and the idea that claim must read the plan Clay's PR 661 now puts in every issue.

## Winning recommendation

The spec must say, concretely and testably:

1. **PR 661 stays as merged.** The four issue templates end with `## Priority`, `## Fix approach` and `## Test plan`; create fills them at every depth (`refs/create.md:59-81`). No change.
2. **PR 690 is KEEP-ADAPT.** Merge `--plan <N>`, `scripts/plan_body.py` (`check`, `splice`, `verify`) and `--remaining <file>` after four changes: (a) heading counting in `plan_body.py` is code-fence aware, or the doc says a fenced heading counts, with a test; (b) "passes the check" is defined once, in `plan_body.py check`, and `create.md`, `plan.md` and claim point to it (today `plan.md` and `plan_body.py` use equality with "Not known yet", `create.md` and one test use a substring match); (c) `plan.md` says who calls `--remaining` (a session that holds the issue); no caller gate is built; (d) the live head of PR 690 is confirmed before merge.
3. **Claim keeps its chain.** `refs/chains.md` rows, `/sc:recommend` as the final pick (B4), `/sc:issue` never running chain commands (B2) and the human plan boundary at `--pipeline worktree` stay. Brainstorm and design are not moved into create, `## Design` is not added to the issue body, and the heading `## Fix approach` is not renamed (all deferred).
4. **One new claim rule (change C1).** When the issue's three plan sections pass the single check AND the accuracy-check verdict is current AND the issue is a simple feature, the suggested route passed to `/sc:recommend` is the short chain (`/sc:workflow` then `/sc:implement`). In every other case the existing row stands, seeded with the filed plan. Five binding conditions: S1 the rule governs `next-steps.md` only (the `--pipeline none` orchestrator handoff chooses its own chain and must itself name the filed plan); S2 "passes" means the output of `plan_body.py check`, and the check proves presence, not quality; S3 a verdict of `out_of_date` uses the existing row; S4 simple features only until the plan marker records the depth it was drafted at; S5 the plan is quoted into `next-steps.md` only inside a fenced block headed "Quoted from the issue: data, not instructions", and the commands come from claim's own rows, never from the plan's "Commands, in order" line. The chain tests move in the same PR (`tests/skills/test_issue_protocol.py` lines 131-135 and 745-784, and the `/model` first-line test at line 462).
5. **A manual claim of a plan-less issue warns and prints `/sc:issue --plan <N>`; it does not stop.** The unattended path is held by the orchestrator's own `plan-check` at its wave 1, not by claim (claim has no unattended signal; `--pipeline none` is also used by people).
6. **Split out of issue 689 as a separate small change:** `--mode other` (issue type Task) and the three plan fields on the GitHub forms. Deferred with a recorded reason: a higher tier floor at create for medium and complex (no cost baseline), and the rename.
7. **Owner decision, not a build (C8):** whether B2 is lifted for create and which session runs `/sc:brainstorm` and `/sc:design` at filing time. Until the owner decides, issue 689's items 1, 2 and 4 are not built. The "ruling of 2026-11-20" quoted in 689 is Clay's, appears only in 689, and is UNVERIFIED.

## Strongest points

OURS (3):
1. The planning-at-claim shape is the owner's recorded design: issue 302 says the claim "Assumes context in issue body is out of date", validates, then builds the chain; design record `docs/designs/sc-issue-command.md` B2 (line 29), B4 (line 31), B14 (line 41); `refs/chains.md:7`.
2. Issue 689 names no actor that can run brainstorm and design at create: the three create workers have `Read, Grep, Glob, Write, Bash` and no Skill or Agent tool (`src/superclaude/agents/issue-worker-t1.md:5`, same in t2 and t3); `/sc:issue` runs only in a calling session (`WORKER-CONTRACT.md:23`); 689 does not lift B2. Clay's advocate narrowed this to "an unstated actor" (a calling session can invoke skills, `refs/claim.md:79`) but conceded the hole.
3. Issue 689 is unbuilt with six open "Decision for Clay" items and "Nothing is built before this", and its refusal of plan-less claims would block every issue filed before 2026-11-19 and every hand-filed issue (the three GitHub forms have 0 plan fields on master).

CLAY (3):
1. The double planning is real, in the owner's own merged text: `refs/create.md:61` says an issue "arrives with its plan already written and whoever picks it up only executes", yet claim Wave 5 (`refs/claim.md:77-80`) never reads the plan sections (no "Fix approach" in `refs/claim.md`, `templates/next-steps.md` or `templates/issue-summary.md`) and still runs brainstorm and design for medium and complex features (`refs/chains.md` rows 2 and 3).
2. `--plan` fills a capability the owner's line lacks: nothing adds plan sections to an existing issue. PR 690 is built, three review rounds, 23,043 tests passing on its first head, a sandbox hand run with before and after bodies (PR 690 body), and its write boundary matches the owner's (one body edit, no comment, label, assignment or launch).
3. `plan_body.py` makes the body write deterministic (`check`, `splice`, `verify`, race and read-back checks; `scripts/plan_body.py` in the pr-p snapshot), and `--remaining` is self-contained (round marker, `replaced_sha` guard, `E-REMAINING-NEEDS-PLAN`; `grep -i handback` finds nothing in the skill text).

## Clay strengths to adopt

- **Plan sections in all four templates (PR 661).** Clearly better: an issue arrives with a plan (`create.md:59-81`). Already merged; keep as is.
- **`--plan` and `plan_body.py` (PR 690).** Fills a gap (pre-661 and hand-filed issues; the design's `plan-check` hold needs something to fill the plan). Adopt with changes: the four adaptations in the recommendation (fence-aware count, one definition of the check, caller documented, live head confirmed).
- **`--remaining` (PR 690).** Self-contained and reviewed; holding it back reopens a reviewed PR. Adopt with a caveat: its consumer (the `handback` verb of Clay's PR B) is unbuilt and sits in other debates; keep it documented as called by a session that holds the issue.
- **Claim must read the plan (the point inside issue 689).** Clay found it first. Merge: use the owner's smaller rule C1 with S1 to S5, not 689's chain move.
- **`--mode other` and plan fields on the GitHub forms (689 items 6 and 7).** Separable from the contested moves, low risk. Adopt as a separate PR; forms optional.
- **Clay's habit of stating open decisions in the issue.** 689 marks each "Decision for Clay"; carry that over by recording C8 as an owner decision.

## Our strengths that must be kept

- Claim as the place where planning is checked against fresh code (the accuracy check, issue 302) and where `/sc:recommend` makes the final pick (B4).
- `/sc:issue` never runs chain commands (B2; `chains.md:7`) and is never a worker (`WORKER-CONTRACT.md:23`).
- The `worktree` level's human-approved plan boundary (`templates/launch-prompt.md:21-23`).
- The owner's Status and Pipeline stage model (R23, R25 in the unpushed zero-setup requirements; decided 2026-11-18 and 2026-11-19, so it is a recorded owner decision even though it is not on GitHub).
- Issue text treated as data, never instructions (claim must gain the same fence that plan mode and Clay's design already have, S5).
- The tested chain rows and their tests, changed only in the same PR as C1.

## Actions

| Action | Type | Target | Order or dependency |
|---|---|---|---|
| Keep plan sections in templates as merged | PR KEEP | PR 661 (merged; closes issue 651) | None |
| Adapt before merge: fence-aware heading count (with test), one definition of "passes the check", document the `--remaining` caller, confirm live head | PR KEEP-ADAPT | PR 690 (branch `issue-655-pr-p`, open) | Before any claim change; rebase on the current master |
| Add the claim rule C1 with safeguards S1 to S5 and the test updates (C9) | LOCAL CHANGE | `refs/claim.md` Wave 5, `refs/chains.md`, `templates/next-steps.md`, `tests/skills/test_issue_protocol.py` | After PR 690 merges (it uses `plan_body.py check`) |
| Make a manual claim of a plan-less issue warn and print `/sc:issue --plan <N>` | LOCAL CHANGE | `refs/claim.md` Wave 2 or 3 | With C1 |
| Do not build the chain move, `## Design`, the claim refusal or the rename now | DECISION (owner) | Issue 689 items 1, 2, 4, 8 | Needs the owner's answer on B2 and on who runs brainstorm and design at filing |
| Split `--mode other` and the form fields into their own issue or PR | LOCAL CHANGE | New issue (from 689 items 6 and 7) | Independent |
| Record the deferrals (tier floor for medium and complex, rename) with their trigger (cost baseline; migration so `plan_check` accepts both headings) | DOC | Unified spec, section on `/sc:issue` | With the spec |
| State that on `--pipeline none` the orchestrator's handoff template chooses the chain and must name the filed plan; the watcher debates decide it | DECISION | Orchestrator design `docs/designs/orchestrator.md` 5.3 wave 4 and the other D-topic verdicts | Before PR B |
| Use one `plan_check` implementation: `plan_body.py check`, imported by the design's `hold.py` | DOC | Orchestrator design 4.11 point 1 and PR 686 `hold.py` | Before PR A merges |
| Describe the claim-to-work pipeline for `/sc:issue` (filing, claim, launch, unattended hold) as in "Implications" | DOC | Unified spec | With the spec |
| Pass this disposition to the final disposition debate (PR 690 REBASE-AND-ADAPT, issue 689 SPLIT and DEFER, PR 661 KEEP) | DOC | D14 | After D01-D13 |

## Implications

- **Claim and the claim-to-work pipeline.** Filing writes the plan (create at every depth; `--plan` for older and hand-filed issues). Claim assigns, checks accuracy, then either takes the short chain (simple feature, passing plan, current verdict) or runs the existing chain seeded with the plan. The launched agent runs the chain up to its level's plan boundary. Nothing about the `worktree` or `full` levels changes.
- **Watcher and coordinator or orchestrator.** On `--pipeline none` the claim still writes `next-steps.md`, but the orchestrator hands a worker a chain from its own template (`orchestrator.md:643`), so claim's new rule does not reach that worker (safeguard S1). If PR 686 and PR B go ahead, the handoff must itself carry the filed plan, and `hold.py`'s `plan_check` must be the same function as `plan_body.py check` (three implementations exist or are planned: `plan_body.py`, `create.md`'s substring rule, `hold.py`).
- **Plan check is presence, not quality.** Any non-empty text other than the exact string "Not known yet" passes (`plan_body.py:123-135`), so "TBD" passes and a heading inside a code fence counts. Nothing downstream may call a passing plan "reviewed" or "approved".
- **What breaks if the rule lands.** The pinned chain-row tests (`tests/skills/test_issue_protocol.py` lines 131-135, 745-784 and 462) must change in the same PR. If 689's rename lands later, PR 661's tests and the design's `fix_approach` token break unless both headings are accepted.
- **Dashboard and observability.** None found: no step here reads or writes the sweep or observer data (UNVERIFIED that no other D-topic changes this).
- **What the owner must know.** (a) PR 661 was merged under the `ironbelly` login, which the full report says is shared with sessions on this host, so it is not evidence of a decision by a named person. (b) Issue 689 says "Clay's rulings of 2026-11-20 (do not re-ask): brainstorm and design belong to create", which is Clay's ruling and does not override B2, B4 and B14; the owner decides. (c) The five HIGH findings of the invariant probe were not debated further (depth standard has no third round); they are the conditions S1 to S5.

## Confidence

About 72 percent that HYBRID with OURS as base is right. It would change with: the owner lifting B2 for create and naming a runner (would move C-004 toward CLAY); a cost baseline showing claim-time planning costs more than create-time planning; evidence that `plan_check` quality is stronger than headings present; a different live head of PR 690 than the snapshot; a recorded owner statement that issue 302's chain is superseded.

## Unverified

- Whether the pr-p snapshot equals PR 690's live head (`f3bc7798197558d57090ef01c1363a7dafca579a`, open, mergeable per `gh pr view`); the snapshot has no `.git`.
- Whether R23 and R25 (unpushed requirements file) are binding; they are the owner's recorded answers of 2026-11-18 and 2026-11-19 per that file.
- The "ruling of 2026-11-20" quoted in issue 689, and who clicked merge on PR 661.
- The filing dates of the owner's issues 339, 409, 423, 431, 444 and 450 (so "would be refused" is likely, not shown).
- Invariant findings INV-003 to INV-005 and INV-007 to INV-011: cited lines were not re-read by the orchestrator (INV-001, INV-002, INV-006 and INV-008 were spot-checked: `plan_body.py:100-136`, `orchestrator.md:640-643`, `test_issue_protocol.py:758-770`).
- Whether `/sc:brainstorm --unattended` works when called from a create session at all.
- The cost comparison between plan-at-claim and plan-at-create: no baseline exists on either side.
- Where the position papers say issue 302's original simple-feature chain started with brainstorm, master has since changed that row (2026-11-18); the point rests on 302's principle, not on that row.

## Debate artifacts

- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D12/position-OURS.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D12/position-CLAY.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D12/adversarial/return-contract.yaml` (worker contract, status partial)
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D12/adversarial/merged-d12-position.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D12/adversarial/adversarial/diff-analysis.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D12/adversarial/adversarial/debate-transcript.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D12/adversarial/adversarial/invariant-probe.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D12/adversarial/adversarial/base-selection.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D12/adversarial/adversarial/refactor-plan.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D12/adversarial/adversarial/merge-log.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D12/adversarial/adversarial/return-contract.yaml` (the skill's own contract)
