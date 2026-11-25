# Position CLAY (D12): /sc:issue plan sections and planning at create

Paths are from the master snapshot `/home/coder/.cache/ic-snap-20261120/master` (origin/master 61ac2c2e6) or the pr-p snapshot `/home/coder/.cache/ic-snap-20261120/pr-p` (branch issue-655-pr-p, PR 690) as marked.

## Claim

Planning belongs at filing time, once, on a strong model, so that whoever picks the issue up (a person, a worker or the polling orchestrator) runs a light check and then executes. Clay's four pieces implement one idea in steps: PR 661 (merged) puts a light plan in every template; PR 690 (open) adds `--plan` so any existing issue can get the same sections, and `--remaining` so a left-open issue is re-planned; issue 689 (open, not built) moves the heavy part (brainstorm, design, command choice) from claim into create and makes claim read the plan.

## Mechanism

- Create fills `## Priority`, `## Fix approach` and `## Test plan` at every depth (`src/superclaude/skills/sc-issue-protocol/refs/create.md:59-81`, master). `--plan <N>` runs the same drafting on an existing issue and makes one body edit built by a script (`src/superclaude/skills/sc-issue-protocol/scripts/plan_body.py` with `check`, `splice`, `verify`, pr-p snapshot), so the model never retypes the body.
- The orchestrator design (`docs/designs/orchestrator.md`, section 4.11 and 8.3, master) holds an issue with no plan (`hold:plan`) and fills the plan through `/sc:issue --plan`; claim then runs only the execution steps.
- Issue 689 moves the chain rows of `refs/chains.md` into `refs/create.md`, adds a `## Design` section before `## Priority`, makes claim write `next-steps.md` from `## Approach`, refuses a claim whose issue lacks the sections (pointing to `--plan`), and adds `--mode other`.

## Cited facts

1. Issue 651 (Clay, PR 661 closes it): "front-load planning into the issue at filing time, so a polling orchestrator or a worker only executes. That lets cheaper models do the execution and stronger models do the planning" (`gh issue view 651 --repo IronbellyOrg/IronClaude`, Problem Statement).
2. PR 661 merged 2026-11-19T01:29:57Z (merged by the `ironbelly` login). It touched 12 files, added 26 test cases, and its gate shows 921 targeted tests passed and the full suite with 2 failures that pass alone (PR 661 body). Its own text says "Not changed: the claim flow".
3. After PR 661 the two ends disagree. Create now writes a Fix approach whose commands are `/sc:workflow`, `/sc:implement`, `/sc:pr-submit --monitor 3` (`refs/create.md:66`), while claim, in Wave 5, still builds a chain that starts with `/sc:brainstorm` and `/sc:design` for medium and complex features (`refs/chains.md` rows 2 and 3) and never reads the plan sections (no `Fix approach` text in `refs/claim.md`, `templates/next-steps.md`, `templates/issue-summary.md`). The same plan is therefore made twice.
4. A capability the owner's line lacks: nothing fills the plan sections of an issue that already exists. Hand-filed issues (GitHub forms with no plan field: `.github/ISSUE_TEMPLATE/bug_report.yml`, `feature_request.yml`, `other.yml`; `grep` finds 0 matches for the three headings) and every issue filed before 2026-11-19 reach claim with no plan. PR 690's `--plan` is that capability.
5. PR 690 is built and tested: 2,811 additions, three review rounds (Augment and Codex), full suite 23,043 passed on its first head (PR 690 body), and a hand run in the private sandbox `IronbellyOrg/orchestrator-sandbox` issue 1 with before and after bodies shown. Its write boundary matches the owner's: one body edit, nothing else (`commands/issue.md` Will Not, plan line, pr-p snapshot).
6. The design's hold depends on it. `plan_check` (design 4.11 point 1) tests the same three headings; ruling 31 says "all plan creation flows through `/sc:issue`" and PR P is "built before PR B" (design 8.3, line 1085). Without `--plan` an unattended poll can hold an issue but nothing can fill it.
7. Issue 689 states the asymmetries as findings read on master: create drafts on T3 at quick and T2 at standard and only deep uses T1 (`refs/tiers.md` tier map), while claim plans on T1 (`refs/chains.md` tier lines); `refs/labels.md:26` says "Task is never chosen", so docs, chores and research are filed as features; the GitHub forms carry no plan field.
8. Issue 689 is honest about its state: "Decision for Clay" is marked on items 2, 5, 6, 7, 8 and 9, "Assumption, for Clay to confirm" on others, and step 1 reads "Nothing is built before this." It calls for the orchestrator's `plan_check` to accept both `Fix approach` and `Approach` during migration.

## What it costs

- A heavy create: a brainstorm and a design on tier 1a or 1b per medium or complex filing, at filing time. Issue 689 itself says create "gets longer and more expensive per issue" and its success metric has "Not measured yet: no baseline".
- Changes the claim chain the owner built and tested: `refs/chains.md`, `refs/claim.md`, four templates, two new templates, three worker agents, three GitHub forms, and the tests that pin chains (`tests/skills/test_issue_protocol.py` has checks on `refs/chains.md` rows, around lines 723 to 770).
- Renames a heading (`Fix approach` to `Approach`) already pinned by PR 661's tests and by the design's `plan_check` token `fix_approach`.

## What it risks

- A design in the body can be stale at claim time. The owner's accuracy check exists because "issue bodies are assumed out of date" (issue 302, line 10).
- Who runs the brainstorm at create is not stated: the create workers have tools `Read, Grep, Glob, Write, Bash` and no Skill tool (`agents/issue-worker-t1.md:5`), and `/sc:issue` is on the never-as-worker list (`WORKER-CONTRACT.md:23`). The calling session would have to run `/sc:brainstorm` and `/sc:design`, which breaks the B2 rule that `/sc:issue` never runs chain commands.
- Refusing plan-less claims blocks every older issue until `--plan` is run on it.
- PR 690's `--remaining` serves the orchestrator's hand-back loop (design ruling 36, `handback` verb), which is unbuilt and contested elsewhere.
- Known limit stated in PR 690: the session follows `refs/plan.md` as prose and only the body building and checks are code; issue text reaches a drafting worker with the claim-mode tool set (follow-up issue 665).

## What it gets right

- It found a real double-planning gap (point 3) and a real missing capability (point 4).
- `plan_body.py` makes the write deterministic and testable, and the one-write boundary is the owner's own rule.
- It states its assumptions and open decisions in writing instead of building them.
- A plan that exists before claim is what lets an unattended poll hold and release work without a person at each step.
