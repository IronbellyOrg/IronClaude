# Round 1 advocate statement: Variant 2 (proposal-B, new phase in the existing sweep task package)

Advocate persona: analyzer (evidence quality, logical consistency). Depth quick, Round 1 only. All files were read on 2026-11-14; nothing was edited except this file.

## Position summary

Variant 2 is the only answer that adds no new `.dev/tasks/` package to PR #539, keeps the plan, its ledger and the fix in one checkout, and has no dependency on Q26, and it is mechanically executable today because `/task` resumes from the first unchecked item. Its cost is real: it routes an ordinary fix through level-4 task-file machinery without a stated need, and it reopens a task whose Done status and review sign-offs were recorded for a different scope. On the evidence, Variant 2 is a valid fallback only when the owner wants zero new packages in #539; Variant 3 is the stronger default.

## Steelman of Variant 1

Strongest version: the safest reading of rule A-004 is that #539 should receive nothing from this alignment program except the fix and its tests, and Variant 1 delivers exactly that. It matches the spec's own written default word for word ("The package is written in the coordinator home (Q26) and referenced by absolute path; #539 commits stage named code and test paths only", `merged-requirements.md:554`, and criterion (5) at `:191`), so choosing it requires no owner exception at all. It also respects rule 3 ("no program artifact ... is created there", `merged-requirements.md:977`) and the #539 author's "never adds keys or files to #539" (`merged-requirements.md:965`) without argument. It keeps level-3 routing (`/sc:workflow` then `/sc:implement`, `~/.claude/CLAUDE.md:88`). What it genuinely gets right: it is the lowest-risk choice for the PR's reviewed surface, and it is honest that the archive location is UNVERIFIED (proposal-A "What it costs or risks").

## Steelman of Variant 3

Strongest version: a plan for a change belongs with that change. Variant 3 keeps one checkout, one session and one PR, so every later state change of the package (ledger lines, the `done/` move, `~/.claude/skills/sc-implement-protocol/SKILL.md:188-196`) happens where the code is, which removes A-002 as a risk. It stays on level-3 routing, which the project table makes the default for ordinary implementation and which explicitly says "File count, multiple sessions ... risk, auditability ... alone never select level 4" (`~/.claude/CLAUDE.md:86`). It has no Q26 dependency. It resolves the always-staged versus named-paths tension by committing the package (project `CLAUDE.md` always-staged rule; `merged-requirements.md:988` rule 15, which already reserves "the only `.dev/tasks/` package allowed there" for SW-02's own). And it is the spec's own recommended answer (`merged-requirements.md:554`, "Yes: it is not a program, collector, key or sidecar"), backed by a measured precedent of 921 `.dev/tasks/to-do/` files already in #539 (question.md fact 5). What it genuinely gets right: it is the only variant that answers the literal question (a `/sc:workflow` package) with a direct yes or no and no extra machinery, and it already includes the "first check whether an existing plan covers SW-02" step that Variant 2 builds on.

## Key strengths claimed

1. No new package enters #539. Variant 2 extends `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/`, which is already in #539 (764 files, question.md fact 5). Rule 15 allows only one `.dev/tasks/` package in that checkout, SW-02's own (`merged-requirements.md:988`); under Variant 2 that slot stays unused.
2. It takes the spec's "existing plan first" branch seriously. Criterion (5) says "first check whether an adequate existing plan covers SW-02" (`merged-requirements.md:191`), and the project rule says "When an adequate approved plan already exists, use its existing executor directly; do not rebuild it ... existing MDTM execution uses `/task`" (`~/.claude/CLAUDE.md:88`). Variant 2 is the only proposal that turns that branch into an action rather than a check.
3. It is mechanically executable without new tooling. `/task` "finds the first unchecked `- [ ]` item, and picks up exactly where it left off" (`~/.claude/skills/task/SKILL.md:21`, `:92`, `:535`), so an appended phase of unchecked items would be picked up by the existing executor.
4. No dependency on Q26 and no cross-checkout writes. Plan, ledger lines and code all live in the #539 checkout, so A-001 and A-002 hold trivially (contrast Variant 1, where "one worktree never holds two live agents", `merged-requirements.md:951`, forces someone other than the #539 author, or a second checkout session, to write the plan).
5. History stays in one place. The package already records Phase 1 from design fixes to POST reflect (task file phases 1 to 14, `TASK-RF-sweep-phase1-20261108-072653.md:209-2440`); SW-02 is a correction to that same deliverable.

## Weaknesses identified in Variant 1

1. Hard dependency on Q26. If Q26 is unanswered "no program file is written on any branch" (`merged-requirements.md:553`), so the plan has nowhere to live and SW-02, which the hard limit requires to have a written plan (question.md fact 1), stalls. Variant 1 admits this (proposal-A "What it costs or risks").
2. A-001 is unresolved. `/sc:workflow` writes into the checkout it runs in (`~/.claude/skills/sc-workflow-protocol/SKILL.md:47`), and a worktree never holds two live agents (`merged-requirements.md:951`). Variant 1's step 1 says "a session in the coordinator home runs `/sc:workflow`" without naming who; if it is the coordinator, the coordinator plans an item the #539 author owns, a role split the spec does not grant (`merged-requirements.md:962-965`). UNVERIFIED whether that is forbidden; it is at least unassigned.
3. A-002 is unresolved. The executor runs in #539 but writes its ledger and archive in another checkout; where the managed archive lands is UNVERIFIED (question.md fact 8; proposal-A says so itself).
4. The plan is not discoverable from the merged PR (proposal-A "What it costs or risks").

## Weaknesses identified in Variant 3

1. It needs an owner exception to A-004's spirit. The #539 author "never ... adds keys or files to #539 (A-004)" (`merged-requirements.md:965`); Variant 3 depends on the owner accepting that a plan is not a program artifact. The spec already pre-authorises this path through Q27 (`:978`, `:988`), so this is a decision cost, not a rule breach.
2. The package grows beyond the plan. `/sc:workflow` ends with an advisory `/sc:reflect --mode pre` (`~/.claude/skills/sc-workflow-protocol/SKILL.md:105`), and `/sc:implement` runs a FINAL review and an archive move (`sc-implement-protocol/SKILL.md:188-196`). Each writes into the package, so the "few files" estimate (proposal-C) is UNVERIFIED and the archive move to `done/` becomes a rename inside #539. Proposal-C concedes the first part.
3. The "921 files" precedent is weaker than it looks. Those packages are the build and research packages of issue #339 itself (question.md fact 5), not artifacts added during a later review fix, so they show that `.dev/tasks/` content is normal in #539, not that alignment-program plans are.
4. "Nothing material unresolved" (proposal-C) overstates: the commit point relative to the archive move is not stated.

## Concessions

1. Routing. Variant 2 uses level-4 task-file machinery for an ordinary multi-file fix with no stated need for it, and the project table says level 4 is for an explicit MDTM choice, an existing MDTM task for execution, or "an exceptionally complex, long-running phased program with a stated need" (`~/.claude/CLAUDE.md:80`), and that risk or auditability "alone never select level 4" (`:86`). The existing task does not plan SW-02 (question.md fact 6), so "an existing MDTM task for execution" does not apply until someone writes the new phase, which is new planning, not reuse. Variant 2 itself flags this (proposal-B "What it costs or risks").
2. It does not answer the literal question. Q27 asks about SW-02's own `/sc:workflow` plan package (`merged-requirements.md:554`). Variant 2 replaces that package with a task-file phase, so it sidesteps rather than answers; the owner would have to accept a format change as well as a location.
3. Reopening a Done task damages its record. The task's last phase is "Final validation ... POST reflect, Done" (`TASK-RF-sweep-phase1-20261108-072653.md:2440`), and its frontmatter carries `status: "🟢 Done"`, a `reflect_pre` sign-off for the original scope (coverage 0.960) and a `reflect_post` verdict "PASS-with-deviations". A phase appended after the Done phase sits outside both reviews, and flipping status back to Doing makes the shipped Phase 1 look unfinished.
4. The no-new-artifact claim is letter only. The new phase's outputs are new files under `.dev/tasks/` in #539, which the #539 author's "never adds ... files to #539" (`merged-requirements.md:965`) reads against just as much as a new package does.
5. Cost. The task file is 3106 lines and `/task` runs per-phase reviewer panels; for a fix of a few files this is the highest per-step cost of the three.
6. Whether the task file's gates accept a phase after Done is unverified (proposal-B "What stays unresolved"). `/task` completion requires every `- [ ]` checked (`~/.claude/skills/task/SKILL.md:298`), which a new phase satisfies mechanically, but no rule in the skill covers reopening.

## Shared assumption responses

| ID | Response | Reason |
|---|---|---|
| A-001 | ACCEPT | Verified: `/sc:workflow` creates its package in the checkout it runs in (`sc-workflow-protocol/SKILL.md:47`) and one worktree never holds two live agents (`merged-requirements.md:951`). It holds trivially for V2 and V3 (the #539 author works in its own checkout) and is the real open gap in V1, which must name who runs `/sc:workflow` in the coordinator home. |
| A-002 | QUALIFY | True for V2 and V3, where package and code share a checkout. For V1 it is the unverified risk the variant already names (question.md fact 8). For V3 it adds one detail: the managed archive moves the package to `done/` (`sc-implement-protocol/SKILL.md:196`), so the commit to #539 must come after that move or include it as a rename. |
| A-003 | ACCEPT | SW-02 touches `probes.py`, at least three test files and the allow-list under F1/F2, or at least 16 text locations under F3 (`merged-requirements.md:191`), which crosses the hard limit (more than one source file or more than 5 edits, `~/.claude/CLAUDE.md`). A written plan is required; "Direct command selection does not waive the written-plan requirement". |

## Per-point verdicts

| Point | Superior variant | One-line reason |
|---|---|---|
| S-001 | Tie (V1 = V2 = V3) | All three use the same five sections and four steps; no structural advantage. |
| C-001 | V3 | Plan beside the fix in one checkout and one PR, using the single package slot rule 15 already reserves for it (`merged-requirements.md:988`). |
| C-002 | V3 | `/sc:implement` in the same checkout is the level-3 executor (`~/.claude/CLAUDE.md:88`); V1 splits checkouts and V2 uses `/task` on a reopened file. |
| C-003 | V2 and V3 (tie) | Neither depends on Q26; V1 stalls if Q26 stays at its default (`merged-requirements.md:553`). |
| C-004 | V1 | It adds nothing from SW-02's plan to #539; V3 adds one package and V2 grows a 764-file package. |
| X-001 | V3 | A plan is none of A-004's named things, and the spec routes it explicitly to Q27 (`merged-requirements.md:978`); V2 keeps only the letter and still adds files. |
| X-002 | V3 | It removes the tension by committing the package; V1 avoids it by moving the plan away at the cost of Q26 and A-002, and V2 avoids it only by reopening a Done package. |
| X-003 | V1 and V3 (tie) | Both stay at level 3; V2 selects level 4 without the stated need `~/.claude/CLAUDE.md:80` and `:86` require. |
| A-001 | V2 and V3 (tie) | The planner writes into its own checkout; V1 leaves the planner unnamed under the one-agent-per-worktree rule (`merged-requirements.md:951`). |
| A-002 | V2 and V3 (tie) | Ledger and archive stay in the code's checkout; V1's archive location is UNVERIFIED. |

## Overall pick

Variant 3, with Variant 2's one useful element kept as its first step (check, and record, that the Done sweep task does not cover SW-02 before writing a new plan); Variant 2 only if the owner refuses any new `.dev/tasks/` package in #539.
