# Research: Observed Work Patterns and Skill Usage (work projects only)
**Scope:** `~/.claude/history.jsonl` (last 45 days, 2026-08-17 to 2026-10-01) and session logs under `~/.claude/projects/` for work project directories only (`/Users/cmerritt/GFxAI/*` excluding `Financials`, plus `/Users/cmerritt/orca/workspaces/IC-Harness*`). No personal projects read or reported.
**Status:** Complete
**Date:** 2026-10-01
---

## 0. Method and data volume

| Source | What was extracted | Volume (45 days) |
|---|---|---|
| `~/.claude/history.jsonl` | `display` text of every typed prompt where `project` is a work path | 2,232 work prompts: IC-Harness 1,597; Ironbelly-Recruiting 337 (+3 in TeamTailor subfolder); GFxAI-with-RigorFlow 241; llm-workflows 54 |
| Session logs `~/.claude/projects/<work-dir>/*.jsonl` and `*/subagents/*.jsonl` | Streamed line by line (python); only lines containing `"Skill"`, `<command-name>`, or `"subagent_type"` were parsed | 10,022 files, about 15.3 GB scanned without loading any file whole |
| Excluded | `GFxAI/Financials`, every `CMxAI/*` path, the `orca/workspaces/financials*` and `health*` workspaces, and `/private/var/.../ccsession-*` temp probe dirs | Not read |

Notes on coverage:
- The IronClaude worktrees (`/Users/cmerritt/GFxAI/IronClaude-ccsession`, `-ccsession-split`, `-ccsession-grok47`, `-ccsession-sol850`, `-tier-failover`, `-tier-tools`, `-model-data`, `-user-setup`) have NO session-log directory of their own. The ccsession and IronClaude work was driven from sessions whose cwd was `/Users/cmerritt/GFxAI/IC-Harness`, so it is counted under IC-Harness. [CODE-VERIFIED: branch names and last commits read via `git -C <worktree> log -1`; for example `IronClaude-tier-failover` is on `feat/ccsession-tier-failover`, last commit 2026-09-30.]
- `/Users/cmerritt/GFxAI/IC-Harness/CONTEXT-SUMMARY.md` does NOT exist on disk (ls returned "No such file"), even though `CLAUDE.md` names it as the "Start here" file. Program framing below therefore comes from prompts, memory index lines, and on-disk `.dev/research/` folder names, not from that file. **Unverified pointer, logged in Gaps.**
- The `orca/workspaces/IC-Harness-modularization` log directory had no files modified in the window.

## 1. Skill and command usage frequency (2026-08-17 to 2026-10-01, work projects only)

### 1a. Slash commands the user typed (from `<command-name>` tags in main-session user turns)

| Command | Count | Where | What it tells us |
|---|---|---|---|
| `/model` | 164 | IC-Harness 124, Recruiting 14, RigorFlow 14, llm-workflows 12 | Constant model switching across the gateway (Sol, Astra, Grok, Opus, GLM, Kimi). Strongest single habit. |
| `/compact` | 49 | mostly IC-Harness (42) | Long sessions routinely hit context limits. |
| `/task` | 34 | IC-Harness 31, llm-workflows 3 | MDTM task execution. |
| `/task-builder` | 34 | IC-Harness 32, llm-workflows 2 | Task file creation. |
| `/skill-eval` | 11 | IC-Harness | Running the eval harness, almost always `/skill-eval task-building --candidate .../reference_solution/candidate.md` or bare `/skill-eval task-building`. |
| `/exit` | 8 | mixed | Exit to relaunch with a different `ccsession --profile`. |
| `/effort` | 7 | mixed | Reasoning effort tuning. |
| `/ccsession-tag` | 5 | IC-Harness 3, llm-workflows 2 | Naming sessions for resume. |
| `/tech-research` | 4 | IC-Harness 3, RigorFlow 1 | Deep research runs (for example game-studio acquisition research). |
| `/tdd`, `/roadmap` | 1 each | IC-Harness | Rare. |

`history.jsonl` agrees on the top items (`/model` 200, `/compact` 27, `/context` 17, `/skill-eval` 6, `/effort` 6) but under-records commands typed with long arguments, which is why the log counts above are higher for `/task` and `/task-builder`.

### 1b. Skill tool invocations in MAIN sessions (the model or the user triggered a skill)

| Skill | Count | Notes |
|---|---|---|
| task-builder | 35 | Includes several the user did NOT want (see Section 3). |
| sc-reflect-protocol (+ `sc:reflect` 8, `sc:reflect-protocol` 3) | 40 total | Pre and post reflection gates inside task files. |
| task | 21 | Task file execution. |
| tech-research | 10 | |
| persona-agent | 10 | Persona brain sample questions. |
| claude-api | 8 | Auto-triggered by model and gateway questions. |
| artifact-design | 8 | HTML comparison files and reports. |
| sc-adversarial-protocol | 7 | Debates (for example "debate this with a couple agents"). |
| confidence-check | 6 | |
| code-review | 5 | PR review of IronClaude ccsession PRs. |
| orca-cli | 5 | Orca terminal and worktree control. |
| sc-troubleshoot-protocol | 4 | User twice said "do not use sc troubleshoot, find out yourself". |
| sc-crash-recovery | 3 | After reboots and dropped connections. |
| computer-use | 2 | |
| prd 2; tdd, operational-guide, tech-reference, repo-cleanup, skill-eval, sc-bare-review, ccsession-tag, loop, update-config, workflow-authoring, goal | 1 each | Document skills are rarely invoked directly in this window. |

### 1c. Skill tool invocations inside SUBAGENTS

| Skill | Count | Likely origin (inference, not verified per run) |
|---|---|---|
| claude-api | 81 | Agents auto-loading it when they touch model names or gateway config. |
| artifact-design | 74 | Agents producing HTML side-by-side comparison files. |
| code-review | 47 | Review lenses in eval and component QA runs. |
| sc-adversarial-protocol | 32 | Reflection Tier 2 merges and debates. |
| sc-reflect-protocol | 13 | |
| confidence-check | 8 | |

### 1d. Subagent types spawned (all work sessions)

| Agent type | Spawns | Agent type | Spawns |
|---|---|---|---|
| rf-task-researcher | 3,748 | eval-substantiation-judge | 793 |
| rf-qa | 3,731 | fork | 753 |
| general-purpose | 2,387 | persona-organ-lead | 278 |
| rf-qa-qualitative | 2,037 | rf-assembler | 148 |
| persona-neuron | 1,303 | rf-task-builder | 97 |
| rf-analyst | 1,105 | Explore | 86 |
| claude (catch-all) | 834 | persona-executive / persona-classifier | 85 / 75 |

Reading: the work is dominated by research fan-out plus QA (rf-task-researcher and rf-qa together about 7,500 spawns), then the persona brain (about 1,800 persona-* spawns), then eval judges. `general-purpose` still has 2,387 spawns despite the project rule that bans it for edits and web research.

## 2. Work-type taxonomy (observed)

Share of prompts is a rough keyword-and-reading estimate over the 2,232 work prompts, not an exact classification.

### W1. IronFlow component consolidation (skills modularization)
The largest single stream in IC-Harness (keyword "component" alone hits 188 prompts). The user walks through shared components one at a time (frontmatter, skill introduction, input, tier selection, execution overview, scope discovery and research readiness, output locations), using PRD as the reference consumer, and approves each one.
- Example asks (paraphrased): "Show me the proposed component line for line next to the PRD original, and mark which lines are shared versus per-consumer." / "Fix this across all consumers, check the others for the same issue, then rebuild every comparison file and send me the links." / "Approved as a plan only; do not install anything into live skills."
- Skills used: mostly none (direct work under an on-disk workflow protocol); `artifact-design` for the HTML side-by-side comparison files; `sc-adversarial-protocol` occasionally. The user repeatedly said NOT to run `task-builder` for this stream.

### W2. Skill-eval harness build-out (product, task-building, task-execution, document domains)
- Example asks: "Run `/skill-eval task-building` against the reference candidate and give me the final report as a link I can open." / "The golden task file fails on a literal wording issue; how did we solve this in the product domain?" (led to the alias, numeric, and concept tier rule) / "Next we need a task-execution eval using the exact same method and infrastructure as product and task building."
- Skills used: `/skill-eval` (11 typed), `eval-substantiation-judge` agents (793 spawns), `task-builder` and `task` for the task-execution eval research, `tech-research` once (the user later said it was more research than needed).

### W3. Persona-agent brain testing
- Example asks: "Write real questions from evidence in the repo for reflex, intuition, and full council; no multiple-choice answers." / "After each sample question stop and report: the question, the answer, which thinking type ran, whether it was right, and how long it took." / "Two neurons failing must never make the whole decision fail; make a simple fix to the executive."
- Skills used: `persona-agent` (10), persona-* agent family (about 1,800 spawns), `sc-reflect-protocol` on the persona-core-gap task file.

### W4. ccsession, shim, and IronClaude packaging (including Coder and tier work)
Confirmed in-flight. Keywords: "ccsession" 46, "coder" 49, "tier" 48. Worktrees on disk: `IronClaude-ccsession-split` (`feat/ccsession-local-profiles`), `IronClaude-tier-failover` (`feat/ccsession-tier-failover`), `IronClaude-model-data`, `IronClaude-tier-tools`, `IronClaude-user-setup`. Research folders: `.dev/research/ccsession-tier-failover-20260930`, `ccsession-model-refresh-debate-20260930`, `coder-ccsession-live-20260925`, `ccsession-personal-routing-20260924`.
- Example asks: "Rename the gpt profiles, add a new 6.1 Sol profile with the same context settings, and drop the old 1mm, 500k, and 372k profile names." / "Keep my personal ChatGPT routing local only; push the company version to IronClaude as its own PR." / "Write a small spec for the tier design: tier 0 to tier 3 model groups in the Coder env, failover on rate limit and server errors, an allow list instead of a picker removal list, and exact file-level changes."
- Skills used: `code-review` (PR comments, Augment review), `sc-adversarial-protocol` ("debate this with a couple of agents"), `claude-api` (auto), `orca-cli`. Work is spec-first (Section 4).

### W5. Environment and tooling troubleshooting
- Example asks: "Why does switching from a 500k profile to Kimi drop the context to 200k?" / "The shim returns a 400 about `context_management` on Claude models only; is this local or a LiteLLM problem?" / "New Coder workspaces keep connecting to another workspace's Orca server; why?" / "Bypass permissions is on but I still have to approve Bash in other sessions."
- Skills used: `sc-troubleshoot-protocol` (4, and the user twice told the agent not to use it), `claude-api`, `computer-use` (2). Most answers were expected in plain English, directly, with a root cause.

### W6. Large batched research runs (GFxAI-with-RigorFlow)
Game-studio acquisition research (778 studios, batches of 40 with independent QA and fix-then-proceed), RAG infrastructure research, a plugin "research bridge" spec.
- Example asks: "Use the tech-research skill for this research, follow it end to end, do not stop." / "Start the next 40-studio batch after studio X; fix anything QA finds before moving on." / "Only 60 of 778 done; this is too slow and too costly. What work are you doing per studio, and how do we speed it up?"
- Skills used: `/tech-research`, `task`, `task-builder`, `workflow-authoring` (1).

### W7. Recruiting candidate filtering and grading (Ironbelly-Recruiting, 340 prompts)
Filtering a large applicant pool by location and fit, objective resume and GitHub scoring to a 0-100 scale, batch grading under a written grading protocol, a cumulative ranked report, and pushing results into the applicant tracking system over its API.
- Example asks: "Write one master grading-workflow spec with the exact steps and scripts, not spread across files." / "Run the next batch of 20 following the protocol, then show me the file and the QA you did." / "Build a new filter for a QA-tester role, put the plan in a workflow protocol file, not plan mode."
- Skills used: almost none (`code-review` 4, `claude-api` 3). Driven by on-disk protocol files.

### W8. Documents and communication deliverables
Onboarding document for two new contributors, CEO summaries, ClickUp stories and subtasks, handoff messages, Orca setup package, this user guide, and a patent-style filing with figures in `llm-workflows`.
- Example asks: "Write an onboarding doc for two people joining IronFlow and IronClaude work: table of contents, executive summary, our workflow protocols." / "Turn the first few tasks into ClickUp stories with subtasks and assign both people." / "Give me a brief overview of this work for my CEO."
- Skills used: rarely the document skills. The user said "do not run a skill for this" and "do not use tech-research" for a comparison write-up.

### W9. Repo operations and side builds
Push everything to main, prune large eval runs and add them to gitignore, fix an accidental chore branch, open and update PRs, clone the company marketing site into a local repo for a partner to review.
- Example asks: "Push everything in IronFlow to main." / "Delete eval runs older than last week and gitignore that folder." / "Recreate the company website locally so my partner can run it on localhost, then push to the new repo."
- Skills used: none in particular; `sc:git` was never invoked.

### W10. Session supervision and recovery
About 157 prompts are "resume this work", "pick up where the last agent left off", or "brief check: progress in under 10 lines". The user also built an Orca session-brief and investigator skill pair to supervise many panes.
- Skills used: `sc-crash-recovery` (3), `orca-cli` (5), `orchestration` (discussed for hourly scheduled checks).

## 3. Observed pain points (redirects, re-runs, complaints)

Counts are regex hits over the 2,232 work prompts (a prompt can match more than one row). Language is paraphrased; the originals were often profane.

| # | Pain point | Prompt hits | Typical paraphrased redirect | What would have fit better |
|---|---|---|---|---|
| P1 | Overengineering a narrow fix (building validators, proof machinery, extra QA cycles, timers, parsers) | 80 "overengineer" + 23 "surgical" + 32 "too long / hurry" | "This was a 25-line component; stop making mountains out of molehills." / "Do the surgical fix, test it, report. No new verification cycle." / "Take out every kill timer you added." | No skill; direct Edit plus one targeted test. If uncertain, `confidence-check` before starting, not after. |
| P2 | Not answering the question; starting work instead | 31 | "I asked you a question and you went and did a bunch of work. Answer it first." / "Just answer, do not change anything." | Answer-only turn. No skill. |
| P3 | Not in plain English; walls of text; wrong presentation format | 65 "plain English" | "Plain English: what did you do, how did it go, what went wrong, how do we fix it." / "For each sample: question, answer, thinking type, right or wrong, time." | The Pragmatic output style plus the five-field sample report rule already in memory. |
| P4 | Running `task-builder` (or another heavy skill) when not asked | 16 direct + several "do not use a skill / do not use tech-research / do not use sc troubleshoot" | "Why are you running task-builder? That is not in our workflow." / "Do not run a skill for this; you and a few agents can do it." | Direct work under the existing on-disk protocol. Note the user also said "when in doubt the regimented skill approach is right" once (2026-09-27), so the rule is: follow the named protocol, do not add a skill the protocol does not call for. |
| P5 | Drifting from the agreed workflow protocol | 104 mention "protocol" | "We have an established protocol; follow it and only it." / "You rewrote a component into a new abstract version; components are lossless best-of-best, not re-creations." / "You touched sections of skills we have not reached yet." | The component workflow protocol file plus `sc-reflect-protocol` UC-2 as a post-check. |
| P6 | Losing work to disconnects, reboots, credit exhaustion, stalls | 157 resume prompts + 66 progress pings | "I lost connection; figure out where you left off and continue." / "One researcher has run for 3 hours; no single agent should run that long." | `sc-crash-recovery` for the "where was I" step; agent watchdogs; Orca supervision skill. |
| P7 | Agents using a different model than the session | 19 | "Use the inherited model only; do not use Sonnet or any named model." / "Grades done by the weaker model must be re-verified." | Already a memory rule: omit Agent model overrides. |
| P8 | Re-solving problems already solved in another domain | several, notably 2026-08-19 | "Why does the task-building grader check exact words? Product domain already solved this with alias, numeric, and concept tiers." | Reuse-first: read the product-domain implementation before building. `reuse-auditor` agent fits. |
| P9 | Agent stopping mid-skill or asking unnecessary questions | many in RigorFlow research | "Do not stop until the skill run is 100% complete. Do not ask me anything again." | `/task` F1 loop run end to end (CLAUDE.md rule 16). |
| P10 | Unauthorized changes to config, branches, or live files | a handful, high severity | "You modified the Pragmatic style without approval; remove it." / "Why did the push go to a chore branch? We should be on main." / "Do not install into live skills; we are only building components." | Propose-then-wait for config; confirm branch before push. |
| P11 | Test infrastructure producing false failures | several (eval and recruiting) | "If the golden candidate cannot pass, nothing will ever pass; the threshold is too strict." / "Your normalized resume parser loses data; use the actual resumes." | Calibrate against the gold first; keep source data raw. |

## 4. Classification of each work type

Classes: **Interactive judgment** (user decides each step live, agent presents and waits), **Task-file** (MDTM via `/task-builder` then `/task`), **Spec-first** (agent writes a short spec or protocol file, user approves, then direct implementation and test), **Debug/review** (find root cause or review existing work, report in plain English).

| Work type | Class | Reasoning from evidence | Suggested skill sequence for the guide |
|---|---|---|---|
| W1 Component consolidation | Interactive judgment (under a written protocol) | Every component ends in a user approval of a presentation; the user adjudicates every shared versus per-consumer line and every removal. The user explicitly rejected task-builder here. | Read the workflow protocol, build the candidate, build the HTML side-by-side (`artifact-design`), present, wait for approval. Optional `sc-reflect-protocol` UC-2 after a revision. |
| W2 Skill-eval harness | Spec-first, then task-file for big research | User asked for "a short spec first, then build one piece at a time and test it" (2026-08-18) and said not to use task-builder for the build. The task-execution eval later went through a task file with a pre-reflection gate. | Spec file, then build and test one grading surface at a time, then `/skill-eval <domain> --candidate <gold>`; use `/task-builder` and `/task` only for the multi-hour research part. |
| W3 Persona brain testing | Interactive judgment | One sample question at a time with a five-field report and a user verdict before the next. | `persona-agent` per question, report, wait. Surgical fixes, then rerun the same question. |
| W4 ccsession / IronClaude / tiers | Spec-first | The user repeatedly asked "write a small spec of everything we agreed", "the spec must list exact file changes", "test locally first, then PR". Separate PRs per concern. | Discuss design, write spec in `.dev/research/<topic>/`, optional `sc-adversarial-protocol` debate, implement in the IronClaude worktree, test locally, `code-review` on PR comments, push only on request. |
| W5 Env and tooling troubleshooting | Debug/review | Questions want a root cause and a fix, in plain English, without changing anything first. | Answer directly from code and logs. Use `sc-troubleshoot-protocol` only if the user asks; they twice declined it. |
| W6 Batched research | Task-file | The user named `/tech-research` and demanded end-to-end skill runs with batch QA and fix-then-proceed. | `/tech-research` (Stage A builds the task file, Stage B runs `/task`), batches of 40, independent QA, fix failures before next batch. |
| W7 Recruiting grading | Spec-first, then repeated batch execution | User demanded "one master grading workflow spec with exact steps and scripts", then "run the next 20 following the protocol". Plan mode explicitly rejected in favor of a protocol file. | Protocol file, then batches against it, cumulative report updated each batch, spot-check QA. |
| W8 Documents and communication | Interactive judgment for short deliverables; task-file only for template-governed docs | Most were short (CEO summary, onboarding, ClickUp stories) and the user said not to run a skill. Formal PRD or TDD style docs would use the document skills. | Short doc: write directly, present. Formal doc: `/prd`, `/tdd`, `/tech-reference`, `/operational-guide`, `/readme`. |
| W9 Repo operations | Interactive judgment (approval-gated) | Pushes, deletions, and branch changes all required an explicit "go". | Show diff and plan, wait for approval, then git. |
| W10 Supervision and recovery | Debug/review | The task is reconstructing state, not producing new work. | `sc-crash-recovery` or read the task file and tracker, then report "done / left / next" before resuming. |

## Gaps and Questions

- `/Users/cmerritt/GFxAI/IC-Harness/CONTEXT-SUMMARY.md` is named as "Start here" in `CLAUDE.md` but does not exist. [CODE-CONTRADICTED by `ls`.] The guide should not point users to it until it exists or the pointer is fixed.
- Subagent skill counts (claude-api 81, artifact-design 74, code-review 47) are attributed by inference; no per-run tracing was done.
- Category shares are approximate (keyword plus manual reading of the prompt dump), not a strict classifier.
- The IronClaude worktrees have no separate session logs, so ccsession effort is folded into IC-Harness counts and cannot be separated precisely.
- One prompt in the history contained a plaintext credential; it was not copied here. The user may want to rotate it.

## Summary

The user's work in the last 45 days falls into ten types. Three are high-volume and interactive (component consolidation, persona sample questions, recruiting batches), two are spec-first infrastructure builds (ccsession and tiers, skill-eval), and one is long batched research run through `/tech-research` and `/task`. The dominant habits are `/model` switching, `/task-builder` plus `/task` for big research, and `/skill-eval task-building`. The dominant frustrations are overengineering narrow fixes, not answering the question asked, not using plain English, invoking heavy skills the protocol did not call for, and losing state to disconnects. A quick-reference guide should map each work type to the lightest sequence that matches its class, and state plainly when NOT to reach for a skill.
