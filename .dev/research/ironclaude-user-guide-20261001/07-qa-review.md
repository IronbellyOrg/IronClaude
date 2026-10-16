# QA Report: IronClaude Quick Guide (adversarial, report-only)

**Target:** `IRONCLAUDE-QUICK-GUIDE.md` (107 lines)
**Evidence base:** `01`-`06` in this folder
**Source truth checked:** `IronClaude-tier-tools/src/superclaude/` (master), `IronClaude-tier-tools/.claude/commands/sc/`, `IC-Harness/.claude/commands/sc/`, `IC-Harness/.claude/skills/`, installed `superclaude` CLI
**Date:** 2026-10-01
**Phase:** report-validation (report-only, no fixes applied)
**Fix cycle:** N/A

---

## Overall Verdict: FAIL

11 findings: 1 CRITICAL, 4 IMPORTANT, 6 MINOR. Each one has to be fixed before the guide can pass.

## Items Reviewed

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Commands and flags exist as written | FAIL (F1, F2, F6, F7) | Most flags verified. Failures: pr-submit preconditions, `origin/master` ref, troubleshoot timing, sc:task trigger words |
| 2 | Availability in IC-Harness | PASS with caveat gaps (F5, F9, F11) | pr-submit, recommend, swarm-wizard, reflect, auggie-review, troubleshoot, brainstorm, adversarial, spec-panel, business-panel, crash-recovery, confidence-check and skill-eval all exist in IC-Harness. Gaps are in the wording, not in missing commands |
| 3 | Internal contradictions | FAIL (F3, F4) | The lite column contradicts `/task` source. The task-file rule (line 27) contradicts rows 2-3 and section 5 |
| 4 | Readability (plain English, no em or en dashes) | FAIL (F8) | No U+2014 or U+2013 found (grep returned exit 1). Some jargon is never explained |
| 5 | Missing items from 01-06 that would mislead | FAIL (F3, F4, F5, F10) | Open questions from 02 and 05/06 are presented as settled; `/roadmap` defaults to Deep |

### What was verified and is correct (no finding)

| Guide claim | Verified at |
|---|---|
| `/sc:workflow ... --depth quick --handoff implement` (master) | `IronClaude-tier-tools/src/superclaude/commands/workflow.md:7,40,42` |
| `/sc:implement @.dev/workflow/<slug>/plan.md`, `--resume` (master) | `commands/implement.md:6,44,57`; `@path ok` at `commands/workflow.md:20`; output dir `skills/sc-workflow-protocol/refs/input-parse.md:11` |
| Simple plan: no subagents, one reviewer per task, one fix pass, then a halt | `skills/sc-implement-protocol/SKILL.md:31,118`; `sc-workflow-protocol/SKILL.md:62` |
| IC-Harness `/sc:workflow` and `/sc:implement` are old copies | `IC-Harness/.claude/commands/sc/workflow.md:22` (`--depth shallow|normal|deep`, no `--handoff`); `implement.md:3` (old persona-based) |
| BUILD-REQUEST `TEMPLATE`, `QA_INTENSITY: lite`, `QA_GATE_REQUIREMENTS: FINAL_ONLY` | `IC-Harness/.claude/skills/task-builder/SKILL.md:996,1000,1001` |
| task-builder tiers: Quick 3 researchers, Standard 4-5 (default), Deep 6-8 | `task-builder/SKILL.md:132-138` |
| `/sc:reflect --mode pre/post --spec --tasklist --diff --no-promote`; promotion moves the folder by default | `IC-Harness/.claude/commands/sc/reflect.md:10,41,57,91` |
| `/sc:auggie-review --diff ... --no-post-pr`; PR target posts with no confirmation | `IC-Harness/.claude/commands/sc/auggie-review.md:8,50,51,107` |
| `/sc:pr-submit --monitor` 0/1/2/3 meanings; 3 pushes | `IC-Harness/.claude/commands/sc/pr-submit.md:26,34-37,80` |
| `/sc:troubleshoot --fix`, `--depth deep`; diagnose-first; user runs `/task` | `IC-Harness/.claude/commands/sc/troubleshoot.md:8,54,187-192` |
| `/sc:brainstorm --handoff task` invokes task-builder | `brainstorm.md:39,60,175` |
| `/sc:adversarial --compare a,b` | `adversarial.md:15,23,58` |
| `/sc:spec-panel @file --mode critique` | `spec-panel.md:22,398` |
| `/sc:recommend "<goal>"` | `recommend.md:8` |
| `/sc:business-panel` | `business-panel.md:57` |
| Tier words: task-builder, tech-research and roadmap use Quick/Standard/Deep; prd, tdd and tech-reference use Lightweight/Standard/Heavyweight | `**Tier**` grep of each `SKILL.md` qa_intensity table |
| tech-research defaults to Deep | `tech-research/SKILL.md:97` |
| `/roadmap` builds task files per phase only at Deep | `02-planning-depth-ladder.md:162`; `roadmap/SKILL.md:5-9` |
| CLI 4.2.0 has no reflect, prd or swarm; has sprint, roadmap, tasklist | `superclaude version` = 4.2.0; `superclaude --help` |
| No `/sc:post-release` in IC-Harness; present on master | `ls` of both command dirs |
| `/sc:select-tool`, `/sc:estimate` are absent on master | `ls src/superclaude/commands` |
| `/skill-eval <domain> --candidate <path>` | `IC-Harness/.claude/skills/skill-eval/SKILL.md:31,133` |
| "last 45 days" | `04-work-patterns.md:2` |

## Findings

### F1 (CRITICAL). Section 4 "Before push and PR" step 3 and Section 7 trap row: `/sc:pr-submit --monitor 1` as written will halt or stop

- **Quoted text (line 68):** "`/sc:pr-submit --monitor 1` (opens the PR and proposes fixes for the review bot's findings). Use `--monitor 2` to let it fix locally; it stops before pushing."
- **Quoted text (line 104):** "`/sc:pr-submit --monitor 3` | Pushes on its own. Use 1 or 2."
- **Problem:** There are two blockers the guide does not mention.
  - (a) Any `--monitor` of 1 or higher STOPs unless a detection contract is locked. The shipped contract is `locked: false`, and the operator override `<repo-root>/.dev/pr-monitor/detection-contract.locked.md` does not exist in either IC-Harness or IronClaude-tier-tools. So the recommended `--monitor 1` and `--monitor 2` both halt with "probe first".
  - (b) PR context (`--head`/`--base`/`--title`/`--body`, or an existing PR number) is a required input. The bare invocation leaves it out.
  - Also, when `--monitor` is omitted the default is 2, not 0.
- **Evidence:** `IC-Harness/.claude/commands/sc/pr-submit.md:26` (default 2), `:27` (PR context Required: Yes), `:29` (STOP if `--monitor >= 1` and contract `locked: false`), `:61` (shipped `locked: false`, write the override after an R1 probe); `IC-Harness/.claude/skills/sc-pr-submit-protocol/refs/detection-contract.md:10`. `ls` of `IC-Harness/.dev/pr-monitor/` and `IronClaude-tier-tools/.dev/pr-monitor/` both fail with "No such file or directory". Evidence file `03-quality-debug-review.md:67,176` also omits the lock precondition.
- **Suggested replacement (line 68):** "`/sc:pr-submit --monitor 0 --head <branch> --title "..." --body "..."` opens the PR only. To have it watch the review bot (`--monitor 1` proposes fixes, `--monitor 2` fixes locally and stops before pushing), a one-time setup is needed first: run the detection probe on a PR the Augment bot has reviewed and save `.dev/pr-monitor/detection-contract.locked.md`. Until then, level 1 and above stop with "probe first". Always pass `--monitor` explicitly, because the default is 2."
- **Suggested replacement (line 104):** "`/sc:pr-submit --monitor 3` | Pushes on its own. Use 0 (open only), or 1 or 2 once the detection probe is set up. The default with no `--monitor` is 2."

### F2 (IMPORTANT). Section 4 step 1: `origin/master` does not exist in IC-Harness

- **Quoted text (line 66):** "`/sc:auggie-review --diff origin/master...HEAD --no-post-pr` (local review, nothing posted)."
- **Problem:** The guide says the user works in IC-Harness, and IC-Harness's default remote branch is `origin/main`, not `origin/master`. The command as written fails there. `origin/master` only applies to IronClaude-tier-tools.
- **Evidence:** `git symbolic-ref refs/remotes/origin/HEAD` in IC-Harness returns `refs/remotes/origin/main`. IronClaude-tier-tools shows `origin/HEAD -> origin/master`. The command doc allows `--diff <base-ref>...HEAD` (`IC-Harness/.claude/commands/sc/auggie-review.md:28`).
- **Suggested replacement:** "`/sc:auggie-review --diff origin/<default-branch>...HEAD --no-post-pr` (use `origin/main` in IC-Harness and `origin/master` in IronClaude; local review, nothing posted)."

### F3 (IMPORTANT). Section 3: the "Lite" column understates what `/task` runs and presents an open question as fact

- **Quoted text (line 35):** "Final QA gate only, but `/task` still runs a 6-agent check after each phase from phase 2 on" and (Full column) "QA gate after every phase, plus reflect before and after".
- **Quoted text (line 39):** "Keep a lite task file to one execution phase; each extra phase triggers another 6-agent gate."
- **Problem:** The lite column leaves out three things.
  - (a) `/task` always runs a Post-Completion Validation before marking a task Done. That validation is another lens-based structural and content pass at the same 6+ agent floor, plus a serialized fix and a source-document fidelity gate. It happens even with one execution phase.
  - (b) A lite task file still gets the PRE reflect (when a spec resolves) and the POST reflect item. Because the guide puts "reflect before and after" only in the Full column, it implies lite skips them.
  - (c) Whether `/task` honors `qa_intensity: lite` at all is an unresolved open question in the evidence. `/task` does not read it and enforces 6+ agents. The guide states the lite cost as settled.
  - Also, `FINAL_ONLY` adds "a final QA validation phase", which is itself a Phase 2+ phase that gets a gate. So "one execution phase" may not be achievable as worded.
- **Evidence:** `IC-Harness/.claude/skills/task/SKILL.md:117-119` (phase gate plus mandatory post-completion), `:190` (every phase except Phase 1), `:279-300` (post-completion Step 0 to Step 1 at the 6+ agent table). `02-planning-depth-ladder.md:41` (FINAL_ONLY adds a final QA phase), `:74`, `:257` (lite keeps PRE/POST reflect and the fidelity gate), `:283`, `:295` (Open Question 1, UNVERIFIED). `06-debate-B-rigor.md` Open points bullet 2.
- **Suggested replacement (line 35, lite cell):** "One QA gate written into the file, but `/task` still adds its own 6-agent check after every phase from phase 2 on, plus a 6-agent final validation and a fidelity check before Done. Reflect still runs before (if there is a spec) and after. Whether `/task` ever scales down for "lite" is not yet confirmed."
- **Suggested replacement (line 39):** "Keep a lite task file as short as possible (setup plus one work phase). Each extra phase adds another 6-agent check, and the final validation always runs."

### F4 (IMPORTANT). The task-file rule (line 27) contradicts rows 2 and 3 and Section 5, and the open question from the debates is hidden

- **Quoted text (line 27):** "Project rule: more than 5 edits or more than one file must go through a task file (row 5 or higher)."
- **Conflicting text:**
  - Row 2 (line 17): "One file, obvious fix | **Direct edit + one test.**" There is no cap of 5 edits, so a 12-edit single-file change would break the rule.
  - Row 3 (line 18): "**Follow that protocol only.**" Protocol work such as component consolidation often edits several files.
  - Section 5 (line 78): "Component consolidation ... No task-builder."
  - Section 5 (line 80): "Skill-eval harness ... build one grading piece at a time". This is multi-file with no task file.
  - Section 5 (line 85): "Short docs ... Write and present".
- **Problem:** "First match wins" (line 12) sends multi-file protocol work to row 3 before the rule can apply. The evidence explicitly flags this as an open, user-owned decision: does an approved spec or protocol file with a checklist satisfy Rule 6? Debate B proposes a resolution: for cross-consumer fixes over 5 edits, write a short checklist in the protocol folder. The guide includes neither.
- **Evidence:** `IC-Harness/CLAUDE.md` Custom Project Rule 6. `05-debate-A-lean.md` Section 4, first concession ("does not literally satisfy it when the build crosses files"), and the Bottom line ("Open question for the user"). `06-debate-B-rigor.md` Section 3, W1 row ("Cross-consumer fixes over 5 edits go into a short checklist in the protocol folder per Rule 6").
- **Suggested replacement:**
  - Row 2: "One file, 5 edits or fewer, obvious fix".
  - Replace line 27 with: "Project rule: more than 5 edits or more than one file must go through a task file (row 5 or higher). Rows 3-4 still obey it: when protocol or spec work crosses that line, put the steps in a short checklist file in the protocol or spec folder. Open question for you: does an approved spec or protocol checklist count as the task file, or must it be an MDTM task file?"
  - Section 5 rows: add "(over 5 edits: checklist file per the project rule)".

### F5 (IMPORTANT). Section 7 "Your install is behind master": the reinstall advice is unverified and probably does not fix IC-Harness

- **Quoted text (line 106):** "Reinstall from `IronClaude-tier-tools` to get the newer behavior."
- **Problem:** The guide gives no command, and the evidence marks the reinstall path UNVERIFIED. More importantly, `superclaude install` copies commands to the user-level `~/.claude/commands/sc`. The stale June copies that the user actually runs are project files under `IC-Harness/.claude/commands/sc/`, and a CLI reinstall does not touch them. A user who follows this advice could still get the old `/sc:workflow` and `/sc:implement` in IC-Harness.
- **Evidence:** `02-planning-depth-ladder.md:288` ("availability depends on the project's own `.claude/`"), `:305` (reinstall path UNVERIFIED). `01-command-inventory.md:91,204` (install target `~/.claude/commands/sc`), `:332`.
- **Suggested replacement:** "To get the newer CLI: `pipx install --force /Users/cmerritt/GFxAI/IronClaude-tier-tools` (unverified; confirm before relying on it). That alone does not update IC-Harness's own `.claude/commands/sc` and `.claude/skills` copies, which need a separate sync. Until then, run the newer `/sc:workflow` and `/sc:implement` from inside the IronClaude-tier-tools worktree."

### F6 (MINOR). Section 4 "Something is broken": troubleshoot timing and preconditions

- **Quoted text (line 45):** "`/sc:troubleshoot "<symptom>"` (it diagnoses only; quick first pass 1-3 min; `--depth deep` for several hypotheses plus a debate)."
- **Quoted text (line 46):** "`/sc:troubleshoot ... --fix` builds a task file".
- **Problem:**
  - The default depth is `standard`, which auto-escalates to Tier 2 (+4-15 min) on low confidence, intermittent or multi-domain issues. Only `--depth quick` caps the run at 1-3 min.
  - `--depth deep` STOPs if the description is under 10 words and there is no `--scope`.
  - `--fix` only *offers* the task-builder chain. It needs the user to accept, and it runs only if the report status is `success`.
- **Evidence:** `IC-Harness/.claude/commands/sc/troubleshoot.md:33,51,75-77,170,192`.
- **Suggested replacement (line 45):** "`/sc:troubleshoot "<symptom>"` diagnoses only. A plain run can grow from 1-3 min to about 15 min if it escalates; add `--depth quick` to keep it short. `--depth deep` (describe the symptom in 10+ words or add `--scope <path>`) gives several hypotheses plus a debate."
- **Suggested replacement (line 46):** "`/sc:troubleshoot ... --fix` offers to build a task file once the diagnosis succeeds; accept it, then run `/task <path>` yourself."

### F7 (MINOR). Section 2 row 2: `/sc:task` escalation triggers are understated

- **Quoted text (line 17):** "security words auto-escalate to strict".
- **Problem:** STRICT also fires on "refactor", "database", "migration", "breaking change", "token", "session" and "oauth". More than 2 estimated files is a booster. A user saying "refactor this function" will get STRICT unexpectedly.
- **Evidence:** `IC-Harness/.claude/commands/sc/task.md:73-77`.
- **Suggested replacement:** "words like security, auth, database, migration, refactor, token or session auto-escalate to strict".

### F8 (MINOR). Readability: unexplained jargon

- **Quoted text:** line 31 "MDTM task file"; line 33 "a BUILD-REQUEST containing `TEMPLATE: 01`, `QA_INTENSITY: lite`, `QA_GATE_REQUIREMENTS: FINAL_ONLY`"; line 35 "6-agent check"; line 78 "post-reflect"; line 106 "June copy", "master"; line 25 "`superclaude sprint run`".
- **Problem:** The guide's audience rule is plain English with no unexplained codes. MDTM, BUILD-REQUEST (that it is a file you write and pass as `/task-builder <path>`), "reflect", "master" and "tier" are never defined. Nothing says where the BUILD-REQUEST file goes or how to pass it.
- **Evidence:** user memory `feedback_plain_english_no_abbreviations_spec_before_work.md` (from MEMORY.md index); the guide text itself.
- **Suggested replacement:** Add a 5-line "Words used here" box after Section 1, for example:
  - "Task file (MDTM): a checklist file that `/task` executes and checks off."
  - "BUILD-REQUEST: a short file you write describing the task; run `/task-builder path/to/BUILD-REQUEST.md`."
  - "Reflect: `/sc:reflect`, an independent audit of a plan (pre) or finished work (post)."
  - "Master: the current IronClaude source in `IronClaude-tier-tools`."
  - "Tier: how deep a skill researches (quick/standard/deep)."

### F9 (MINOR). Section 3: "Available in IC-Harness now? No" leaves out where the simple plan is available

- **Quoted text (line 37):** "**No** (IC-Harness still has the June copy)".
- **Problem:** The new `/sc:workflow` and `/sc:implement` ARE available as project commands when working inside `IronClaude-tier-tools`, which is where the ccsession and tier work (Section 5, line 79, "build (simple or lite task file)") happens. As written, a reader would think the simple plan is unusable everywhere.
- **Evidence:** `IronClaude-tier-tools/.claude/commands/sc/workflow.md:7` (new argument hint with `--handoff`).
- **Suggested replacement:** "**No** in IC-Harness (June copy). **Yes** when working inside `IronClaude-tier-tools`."

### F10 (MINOR). Section 2 row 10 and the Section 7 roadmap trap leave out that `/roadmap` defaults to Deep

- **Quoted text (line 101):** "`/roadmap` only builds task files at deep tier."
- **Problem:** The guide does not say that `/roadmap` defaults to Deep with full QA. The evidence prices that at 44-48 evaluating agents for 6 phases. A user who reads "only at deep" may think they have to ask for deep, when deep is the expensive default.
- **Evidence:** `IC-Harness/.claude/skills/roadmap/SKILL.md:102` ("Default to Deep"), `:2533`. `05-debate-A-lean.md` Section 2, rule 10.
- **Suggested replacement:** "`/roadmap` defaults to deep (full QA, task files for every phase, many agents). Say "quick" for the roadmap document only, or "standard" for the document plus build requests."

### F11 (MINOR). Section 7 last row: removed commands still run in IC-Harness

- **Quoted text (line 107):** "`/sc:select-tool`, `/sc:estimate` | Removed on master. Use `/sc:recommend`."
- **Problem:** Both still exist in IC-Harness and will run there. The row does not say this, so it reads as if they are gone.
- **Evidence:** `ls IC-Harness/.claude/commands/sc` lists `select-tool.md` and `estimate.md`; `ls IronClaude-tier-tools/src/superclaude/commands` lists neither.
- **Suggested replacement:** "Still present in IC-Harness's old copy but removed on master. Use `/sc:recommend` instead."

## Summary

| Severity | Count | IDs |
|---|---|---|
| CRITICAL | 1 | F1 |
| IMPORTANT | 4 | F2, F3, F4, F5 |
| MINOR | 6 | F6, F7, F8, F9, F10, F11 |

- Checks passed: 1 / 5 (availability); 4 failed.
- Issues fixed in place: 0 (report-only by instruction).

## Confidence Gate

- **Confidence:** Verified: 5/5 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (this is confidence in the review's coverage, not in the guide)
- **Tool engagement:** Read: 0 | Grep: 0 | Glob: 0 | Bash: 26 (grep, sed, ls, diff, git and CLI calls run through Bash against source files; each call targeted a specific guide claim) | Write: 1 | Edit: 4. No web research was performed.
- Not checked (out of scope or low value): per-flag behavior of `/sc:business-panel @doc.md` beyond the existence of the command; whether `/simplify`, `/code-review` and `/security-review` behave as described (these are built-ins, listed in the session skill list).

## QA Complete




