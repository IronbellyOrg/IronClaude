# IronClaude Quick Guide: Which Skill for Which Work

Last checked: 2026-10-01. Sources: IronClaude master (`IronClaude-tier-tools`), the IC-Harness project copies, and your last 45 days of work sessions. Evidence lives next to this file (`01`-`06`).

---

## 1. The one rule

**Use the lightest approach that still leaves something on disk and gets checked by someone other than the author.**
Climb the ladder below only when a trigger fires. If you name a skill, it runs end to end and nothing extra gets added.

**Words used here**
- **Task file (MDTM):** a checklist file that `/task` executes and checks off; survives disconnects.
- **BUILD-REQUEST:** a short file describing the work; run `/task-builder path/to/BUILD-REQUEST.md`.
- **Reflect:** `/sc:reflect`, an independent audit of a plan (pre) or of finished work (post).
- **Master:** the current IronClaude code, checked out at `/Users/cmerritt/GFxAI/IronClaude-tier-tools`. IC-Harness runs an older June copy.
- **Tier:** how deep a skill researches and checks (quick/standard/deep; section 7 lists skills that use other words).
- **6-agent check:** the QA gate `/task` runs: at least 6 separate reviewers (3 structural, 3 content), then a fix and a re-check, repeated up to 3 times before it stops and asks you.
- **Fidelity check:** a final pass confirming the output still matches its source documents.

## 2. Pick your depth (first match wins)

| # | Your situation | Use | What you get |
|---|---|---|---|
| 1 | You asked a question | **Just ask.** No skill. | An answer. Nothing changes. |
| 2 | One file, 5 edits or fewer, obvious fix | **Direct edit + one test.** Optional `/sc:task "<op>"` (adds a test run; words like security, auth, database, migration, refactor, token, or session auto-escalate to strict) | The fix |
| 3 | A written protocol already governs the work (component reviews, grading batches) | **Follow that protocol only.** Interactive, step by step, you approve each step | Work against an on-disk protocol |
| 4 | Design not agreed yet (new tier logic, new grader, new profile scheme) | **Spec first:** short spec in `.dev/research/<topic>/` with exact file changes. Optional `/sc:spec-panel @spec.md --mode critique` | A spec you approve before any build |
| 5 | Agreed scope, a few files, 1-2 sessions | **Simple task file.** Inside `IronClaude-tier-tools`: `/sc:workflow <spec> --depth quick --handoff implement`. In IC-Harness today: `/task-builder` with "quick, lite QA, final gate only" (see section 3), then `/task` | A plan with acceptance criteria, resumable |
| 6 | 5-20 files, or crosses several sessions | **Full task file:** `/task-builder <goal>` then `/task <path>` | Researched, QA-gated, checkbox-tracked task file |
| 7 | 20+ files or several subsystems | Same. Deep is picked on its own at this size; to force it, say "deep dive" or "thorough" | Deep tier, more researchers and QA |
| 8 | You don't know what to build or where the code is | **`/tech-research <question>`** (it defaults to deep and picks the tier itself from the question's size; there is no setting to force Quick. The word "quick" on its own only lowers QA. For a small run, ask a narrow question), then hand the report to `/task-builder` | Research report with an implementation plan |
| 9 | New product or component needing a formal doc | **`/prd`** then **`/tdd`**, review with `/sc:spec-panel` | Template-conformant PRD / TDD |
| 10 | Multi-phase release | **`/roadmap <prd/tdd>`** then `/task` per phase (stays in task files; defaults to deep and many agents and picks the tier itself from the input's size: Quick gives the document only, Standard adds build requests, Deep adds task files. There is no setting to force a tier; the word "quick" on its own only lowers QA), or `/sc:roadmap` then `/sc:validate-roadmap` then `/sc:tasklist` then `superclaude sprint run` | Phased plan plus executable phases |

Project rule: more than 5 edits or more than one file must go through a task file (row 5 or higher). Rows 3-4 still obey it: when protocol or spec work crosses that line, put the steps in a checklist file in the protocol or spec folder. **Open question for you:** does an approved spec or protocol checklist count as the task file, or must it be an MDTM task file?

## 3. Simple task file vs full task file

| | Simple plan (master only) | "Lite" MDTM task file | Full MDTM task file |
|---|---|---|---|
| How to ask | `/sc:workflow <spec or prompt> --depth quick` then `/sc:implement @.dev/workflow/<slug>/plan.md` (`--resume` to continue) | `/task-builder` with a BUILD-REQUEST containing `TEMPLATE: 01`, `QA_INTENSITY: lite`, `QA_GATE_REQUIREMENTS: FINAL_ONLY`; then `/task <path>` | `/task-builder <goal>` (Standard by default; Deep on its own for 20+ files or several subsystems, or say "deep dive" or "thorough"); then `/task <path>` |
| Planning cost | No subagents | 3 researchers + research gate + 5 validators | 4-8 researchers, full gates |
| Checking | One reviewer per task against its acceptance criteria, one fix pass, then halts for your ruling | One QA gate written into the file, but `/task` still adds a 6-agent check after each phase from phase 2 on, plus a 6-agent final validation and fidelity check. Reflect still runs before (if there is a spec) and after. Whether `/task` ever scales down for "lite" is unconfirmed | QA gate after every phase, plus reflect before and after |
| Best for | Known scope, a few files | Known scope that must survive disconnects with audited checkboxes | Discovery, multi-file features, long unattended runs |
| Available in IC-Harness now? | **No** (June copy). **Yes** when working inside `IronClaude-tier-tools` | Yes | Yes |

Keep a lite task file as short as possible (setup plus one work phase); each extra phase adds another 6-agent check.

## 4. Workflows for debugging, hard problems, review, and PRs

**Something is broken**
1. Look at the code and logs yourself first, and get a plain-English root cause.
2. If that fails, or the bug is intermittent or crosses files: `/sc:troubleshoot "<symptom>"`. It diagnoses only. A plain run takes 1-3 min but can grow to about 18 if it escalates; add `--depth quick` to cap it at 1-3 min, or `--depth deep` for several hypotheses plus a debate (describe the symptom in 10+ words or add `--scope <path>`, otherwise it stops and asks for detail).
3. Small fix: edit + test. Multi-file fix: `/sc:troubleshoot ... --fix` offers to build a task file once the diagnosis succeeds; accept, then run `/task <path>` yourself.

**Hard, ambiguous problem (needs several perspectives)**
- Fuzzy idea or requirements: `/sc:brainstorm "<topic>"` (add `--handoff task` to go straight to a task file).
- Two or more competing drafts or designs: `/sc:adversarial --compare a.md,b.md` (debate, score, merge).
- A spec that needs expert critique: `/sc:spec-panel @spec.md --mode critique`.
- Want other model families to look: `/sc:swarm-wizard` (guided interview; needs the newer CLI).
- Business or strategy question: `/sc:business-panel @doc.md`.

**Before you start building**
- Not sure which tool fits: `/sc:recommend "<goal>"`.
- Have a spec and a plan: `/sc:reflect --mode pre --spec <spec> --tasklist <plan>` (checks the plan covers the spec).
- Ask for a "confidence check" before implementing anything you are unsure of.

**After building, before commit**
1. Run the tests.
2. `/sc:reflect --mode post --diff <ref> --no-promote` (independent check of drift and regressions).
3. `/simplify`, then `/code-review`; `/security-review` if auth, secrets, input handling, or file paths changed.

**Before push and PR** (push only when you say so)
1. `/sc:auggie-review --diff origin/main...HEAD --no-post-pr` (use `origin/master` in IronClaude; local review, nothing posted).
2. You approve the push.
3. `/sc:pr-submit --monitor 0 --head <branch> --title "..." --body "..."` opens the PR only. Level 1 also proposes fixes for the review bot's findings; level 2 fixes locally and stops before push. Use levels 1 and 2 only from inside `IronClaude-tier-tools`, where they need no setup. In IC-Harness (June copy) they do not work: they stop with "probe first", and the code they need is not in your installed CLI (4.2.0). Always pass `--monitor`; the default is 2.

**Lost session or crash**
- Interrupted task file: just run `/task <path>` again; the checkboxes are the truth.
- Don't know where you were: say "the session crashed, where was I?" (crash recovery, read-only).

## 5. Your current work, mapped

| Work | Mode | Sequence |
|---|---|---|
| Component consolidation (modularization) | Interactive under the component protocol | Protocol, build candidate, side-by-side HTML, you approve. No task-builder. Cross-consumer fixes over 5 edits: checklist per the project rule. Optional post-reflect after such a fix. |
| ccsession / Coder tier spec work | Spec first | Discuss, spec with exact file changes, optional `/sc:adversarial` debate, build (simple or lite task file), test locally, `/code-review`, push and PR on your go. |
| Skill-eval harness | Spec first, task file for big research | Spec, reuse what the product domain already solved, build one grading piece at a time (over 5 edits: checklist per the project rule), `/skill-eval <domain> --candidate <gold>`. |
| Persona brain testing | Interactive | One question at a time, five-field report, surgical fix, rerun the same question. |
| Large batched research | Task file | `/tech-research` end to end, batches with independent QA, fix before the next batch. |
| Recruiting grading | Spec (protocol) then batches | One master grading protocol, run batches against it, cumulative report on disk. |
| Environment or tooling problems | Debug | Plain-English root cause from code and logs; `/sc:troubleshoot` only if you ask for it. |
| Short docs (summaries, onboarding, stories) | Direct | Write and present. Formal PRD/TDD/ops guide: the matching doc skill. |
| Git: push, prune, branches | Approval-gated | Show the plan and diff, wait for go. |
| Resume / status checks | Answer | Read the tracker or task file, report done / left / next. |

## 6. Don't use a skill when

- You asked a question or for a status check.
- The fix is narrow and known: do the surgical fix, test it, report. No new validators, timers, or extra QA rounds.
- A protocol already governs the work and doesn't call for that skill.
- The deliverable is a short doc or message.

## 7. Traps

| Trap | What to know |
|---|---|
| `/task` vs `/sc:task` | `/task` runs a task file with QA gates. `/sc:task` is a one-shot executor with no file. |
| `/roadmap` vs `/sc:roadmap` | `/roadmap` makes task files for `/task`. `/sc:roadmap` feeds `/sc:tasklist` and `superclaude sprint`. `/roadmap` defaults to deep (task files for every phase) and picks the tier from input size; Quick gives the document only, Standard adds build requests. |
| `/sc:reflect --mode post` | Moves the finished work folder by default. Add `--no-promote`. |
| `/sc:auggie-review <PR#>` | Posts to the PR without asking. Add `--no-post-pr`. |
| `/sc:pr-submit --monitor 3` | Pushes on its own. Use 0; use 1 or 2 only inside `IronClaude-tier-tools`. No `--monitor` means 2. |
| Tier words differ | task-builder, tech-research, roadmap: quick/standard/deep. prd, tdd, tech-reference: lightweight/standard/heavyweight. |
| Your install is behind master | IC-Harness `/sc:*` is a June copy (old `/sc:implement` and `/sc:workflow`, no `/sc:post-release`). The `superclaude` CLI on your PATH is 4.2.0 (no `reflect`, `prd`, `swarm`). A CLI reinstall from `IronClaude-tier-tools` (likely `pipx install --force <path>`, unverified) does NOT update IC-Harness's own `.claude` copies; those need a separate sync. Until then, use the newer commands from inside `IronClaude-tier-tools`. |
| `/sc:select-tool`, `/sc:estimate` | Still in IC-Harness's old copy, removed on master. Use `/sc:recommend`. |
