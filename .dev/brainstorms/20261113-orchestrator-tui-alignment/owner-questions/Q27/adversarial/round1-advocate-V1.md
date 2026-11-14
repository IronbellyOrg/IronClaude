# Round 1 advocate statement: Variant 1 (plan in the coordinator home)

Advocate: Variant 1. Persona: architect (structure, dependencies, long-term impact). Depth: quick, Round 1.

## Position summary

Variant 1 has the right instinct, which is to keep PR #539's reviewed surface to code and tests, but as written it cannot run: `/sc:implement` refuses a managed `/sc:workflow` plan that lives in a different checkout from the one it runs in (`~/.claude/skills/sc-implement-protocol/refs/managed-workspace.md:11`). I therefore defend Variant 1's goal (a narrow #539) and concede its mechanism, and I judge Variant 3 the better answer, provided it carries Variant 1's narrowness guard.

## Steelman of Variant 2

Variant 2's strongest form: the project already has a package for Phase 1 inside #539, and the routing rule says "When an adequate approved plan already exists, use its existing executor directly; do not rebuild it" (`~/.claude/CLAUDE.md:88`). Appending SW-02 as a phase keeps the whole Phase 1 history (build, then the INV-008 fix) in one package in the PR that shipped it, adds no new `.dev/tasks/` package to #539 (so rule A-004's "no new artifact" is kept in letter, `merged-requirements.md:978` rule 5), and gives a security-sensitive fix the MDTM per-phase reviewer panels. It also has no dependency on Q26 and no cross-checkout coupling, because the package is already tracked in the #539 checkout. What it genuinely gets right: one checkout, one executor run, and no new top-level package.

## Steelman of Variant 3

Variant 3's strongest form: the spec already names this exact exception. Rule 15 says "the only `.dev/tasks/` package allowed there is SW-02's own, under Q27" (`merged-requirements.md:988`), and rule 5 says SW-02's plan package "is a separate question" from A-004's ban (`merged-requirements.md:978`). A `/sc:workflow` package is a plan, not a program, collector, JSON key, sidecar or report file. Writing and executing it in the #539 checkout satisfies every mechanical constraint at once: `/sc:workflow` writes into the checkout it runs in (`sc-workflow-protocol/SKILL.md:47`), `/sc:implement` requires the plan to sit under the current git top-level (`managed-workspace.md:11`), the archive helper takes `--root <checkout>` (`managed-workspace.md:54`), and the always-staged rule (project `CLAUDE.md`, ".dev/tasks/ Is Always Staged") stops fighting the named-paths commit rule. It has no Q26 dependency and a measured precedent of 921 `.dev/tasks/to-do/` files already in #539 (question.md fact 5). What it genuinely gets right: it is the only variant whose level-3 route actually executes.

## Key strengths claimed (Variant 1)

1. **Tightest #539 surface.** Variant 1 adds zero files to #539 from SW-02's plan (diff-analysis C-004). Rule A-004 bans "every program artifact of this alignment work" inside #539 (`merged-requirements.md:978` rule 5); placing the plan elsewhere honours that rule's spirit with no interpretation needed.
2. **Level-3 routing.** Variant 1 uses `/sc:workflow` then `/sc:implement`, the ordinary route for multi-file work (`~/.claude/CLAUDE.md`, workflow table level 3 and "Hard limit": "normally level 3, not automatic level 4").
3. **It matches the spec's own default.** The "Default if unanswered" for Q27 is Variant 1 word for word (`merged-requirements.md:554`; question.md "Default if unanswered"), so it is the conservative choice the spec already accepted as a fallback.
4. **Program records stay together.** The plan sits beside the ledger on the program branch named under Q26 (diff-analysis U-001), and the coordinator never needs to create a program artifact in the #539 checkout (`merged-requirements.md` 6.4 rule 3).

## Weaknesses identified in Variant 2

1. **Level 4 with no stated need.** The project table sends level 4 only to an explicit MDTM choice or "exceptionally complex, long-running phased program with a stated need for its research, checklist and phase-reviewer machinery" (`~/.claude/CLAUDE.md`, level 4 row). SW-02 is a bounded fix plus tests; Variant 2 names no such need beyond "per-phase reviewer panels" (variant-2 "What it unlocks"). The hard limit says written plans are "normally level 3, not automatic level 4".
2. **The "adequate existing plan" rule does not apply.** `~/.claude/CLAUDE.md:88` covers an adequate approved plan that already exists. The sweep task is Done and "does not plan SW-02" (question.md fact 6; variant-2 itself admits this under "What it costs or risks"). Appending a phase is writing a new plan inside an old file, not reusing an approved one.
3. **Reopening a Done record rewrites history.** Flipping `status: "🟢 Done"` back to Doing invalidates the frontmatter's pre-execution review for the original scope (variant-2 "What it costs or risks"), and whether the existing gates accept a phase added after Done is open (variant-2 "What stays unresolved"). Architecturally this couples a security fix's lifecycle to a finished build record.
4. **It keeps A-004 in letter only.** The package already has 764 files in #539 (question.md fact 5); a new phase plus its `/task` outputs grows #539 more than Variant 3's one small package would, while claiming "no new artifact".

## Weaknesses identified in Variant 3

1. **Scope creep risk.** Once one `.dev/tasks/` package is admitted to #539, the next item can argue by precedent. Variant 3 names the guard ("it covers SW-02's own plan only", variant-3 "What it costs or risks") but the guard is prose, not mechanical.
2. **Executor side files.** `/sc:workflow` runs `/sc:reflect --mode pre` as its final step and may write `artifacts/` such as `codegraph-grounding.md` into the package (`sc-workflow-protocol/SKILL.md` "Will / Will Not" and "Artifact" bullet); `/sc:implement` writes `progress.md` and, on completion, moves the package from `to-do/` to `done/` (`sc-implement-protocol/SKILL.md` "Done"; question.md fact 8). The named-paths commit in #539 must therefore stage a rename and extra files. Variant 3 admits the extra artifacts but not the `to-do/` to `done/` move.
3. **Reviewer burden.** #539 already has 1003 files (question.md fact 5); a reviewer must recognise the new package as a plan. Small, but real.
4. **Untracked neighbours in the same checkout.** The #539 checkout holds untracked program files (this debate folder, review files) that rule 15 says must be neither deleted nor moved (`merged-requirements.md:988`). None of them is under `.dev/tasks/` in the session-start git status, so `git add .dev/tasks` would pick up only the new package, but the author must still commit by named paths, as rule 15 already requires.

## Concessions

1. **Variant 1's mechanism fails.** Its step 2 runs `/sc:implement` from the #539 checkout on a plan in the coordinator home. `/sc:workflow` writes `schema: workflow-plan/1.2` (`sc-workflow-protocol/refs/quality-gates.md:6`), which makes the plan "managed", and a managed plan must resolve to `<checkout>/.dev/tasks/to-do/<slug>/<slug>.md` "where `<checkout>` is the current git top-level. A copied plan or a plan from another checkout fails here" with `E-MANAGED-INVALID` (`managed-workspace.md:7`, `:11`). Variant 1 listed this as UNVERIFIED; it is now verified against Variant 1. The only way round it, running `/sc:implement` in the coordinator home, would put the code edits in the wrong checkout (the archive helper records delivery files as repo-relative paths under `--root <checkout>`, `managed-workspace.md:54`).
2. **The spec's default inherits the same defect.** Q27's default ("written in the coordinator home ... referenced by absolute path", `merged-requirements.md:554`) is not executable by `/sc:implement` either. The owner should know that leaving Q27 unanswered does not give a working fallback.
3. **Q26 dependency is a real stall.** If Q26 is left at its default, "no program file is written on any branch" (`merged-requirements.md:553`), so Variant 1 has nowhere to put the plan and SW-02 stops (diff-analysis C-003).
4. **Session ownership is awkward.** Under Variant 1 someone must run `/sc:workflow` in the coordinator home. Either the coordinator plans another role's item, or the #539 author opens a second session there, while "one worktree never holds two live agents" (`merged-requirements.md:951`, 6.2).
5. **Traceability loss.** A reader of merged #539 cannot find the plan from the PR (variant-1 "What it costs or risks").

## Shared assumption responses

| ID | Response | Reason |
|---|---|---|
| A-001 | QUALIFY | True for Variants 2 and 3 (the #539 author plans and executes in the #539 checkout). False for Variant 1 as written: `/sc:workflow` writes only into the checkout it runs in (`sc-workflow-protocol/SKILL.md:47`), so the #539 author cannot write into the coordinator home without a second live session there, which 6.2 forbids for one worktree (`merged-requirements.md:951`); the coordinator would have to author the plan. |
| A-002 | ACCEPT, and upgrade to a verified requirement | Not just an assumption: `/sc:implement` refuses a managed plan outside the current git top-level (`managed-workspace.md:11`) and the archive helper runs against `--root <checkout>` (`managed-workspace.md:54`). Ledger, archive and code must share one checkout. This settles Variant 1's UNVERIFIED archive question against Variant 1. |
| A-003 | ACCEPT | SW-02 under F1/F2 changes `probes.py` plus at least three test files and the allow-list; under F3 it edits at least 16 locations (question.md fact 1; `merged-requirements.md:191`). Either exceeds the hard limit (`~/.claude/CLAUDE.md`, "Hard limit"), so a written plan is required. |

## Per-point verdicts

| Point | Superior variant | One-line reason |
|---|---|---|
| S-001 | Tie | All three have the same five sections and four steps. |
| C-001 | Variant 3 | The plan must live in the checkout where `/sc:implement` runs (`managed-workspace.md:11`), which is the #539 checkout. |
| C-002 | Variant 3 | Same-checkout `/sc:implement` runs; Variant 1's cross-checkout run stops with `E-MANAGED-INVALID`; Variant 2 uses level-4 `/task` without a stated need. |
| C-003 | Variant 3 | No Q26 dependency, shared with Variant 2, but on the level-3 route. |
| C-004 | Variant 1 | Zero SW-02 files enter #539, the smallest possible change to the PR's file set. |
| X-001 | Variant 3 | Rules 5 and 15 explicitly carve SW-02's plan out of A-004 for Q27 (`merged-requirements.md:978`, `:988`); Variant 1 over-reads the ban. |
| X-002 | Variant 3 | Committing the plan removes the conflict; Variant 1 only moves it to a place the executor cannot reach. |
| X-003 | Variant 3 | Level 3 like Variant 1, but the only level-3 route that executes. |
| A-001 | Variant 3 | One author, one session, one checkout satisfies it without a second live agent. |
| A-002 | Variant 3 | The only variant in which the package's state changes happen in the checkout `/sc:implement` requires. |

## Overall pick

Variant 3, with Variant 1's guard written into the answer: only SW-02's own package, staged by named paths including its `artifacts/`, `progress.md` and the `to-do/` to `done/` move, and nothing else from the program enters #539.
