# QA Report: Fix Cycle for IronClaude Quick Guide (adversarial, report-only)

**Target:** `IRONCLAUDE-QUICK-GUIDE.md` (113 lines, read in full)
**Prior report:** `07-qa-review.md` (F1-F11)
**Source truth checked:** `IronClaude-tier-tools/src/superclaude/` (HEAD = `origin/master`, 0/0 ahead/behind), `IronClaude-tier-tools/.claude/commands/sc/`, `IC-Harness/.claude/commands/sc/`, `IC-Harness/.claude/skills/`, installed `superclaude` CLI
**Date:** 2026-10-01
**Phase:** fix-cycle (report-only; the guide was not edited)
**Fix cycle:** 1

---

## Overall Verdict: FAIL

7 of 11 prior findings are fully resolved (F2, F3, F4, F5, F7, F9, F11). 4 are only partly resolved (F1, F6, F8, F10), and the fixes introduced 1 new error (N1). Remaining issues: 5 (was 11), so the count shrank and the monotonicity guard does not fire. No regressions: every item that passed in `07` still passes.

## Prior Findings Status

| ID | Status | New guide text (quoted) | Verification |
|---|---|---|---|
| F1 | PARTLY RESOLVED (see R-F1) | Line 74: "`/sc:pr-submit --monitor 0 --head <branch> --title "..." --body "..."` opens the PR only. Levels 1 (propose fixes for the review bot's findings) and 2 (fix locally, stop before push) need a one-time setup first: a detection probe on a bot-reviewed PR that saves `.dev/pr-monitor/detection-contract.locked.md`; until then they stop with "probe first". Always pass `--monitor`; the default is 2." Line 110: "Pushes on its own. Use 0, or 1 or 2 once the probe is set up. No `--monitor` means 2." | `--monitor 0 --head --title --body` matches `IC-Harness/.claude/commands/sc/pr-submit.md:34`; default 2 at `:26,:45` (unchanged on master). PR context requirement is met. Probe path matches `:61` and master `pr_submit/detection.py:39`. But the probe requirement is stated for both repos, and it is false on master; the probe does not save the file. See R-F1. |
| F2 | RESOLVED | Line 72: "`/sc:auggie-review --diff origin/main...HEAD --no-post-pr` (use `origin/master` in IronClaude; local review, nothing posted)." | `git symbolic-ref refs/remotes/origin/HEAD`: IC-Harness = `origin/main`; IronClaude-tier-tools = `origin/master`. |
| F3 | RESOLVED | Line 41 lite cell: "One QA gate written into the file, but `/task` still adds a 6-agent check after each phase from phase 2 on, plus a 6-agent final validation and fidelity check. Reflect still runs before (if there is a spec) and after. Whether `/task` ever scales down for "lite" is unconfirmed". Line 45: "Keep a lite task file as short as possible (setup plus one work phase); each extra phase adds another 6-agent check." | `task/SKILL.md:117` (6-agent phase gate, Phase 2+), `:118` (6 floor also at post-completion), `:119` (Steps 1-4 incl. fidelity gate), `:190` (Phase 1 exempt). `02-planning-depth-ladder.md:257` (PRE reflect when a spec resolves, POST reflect always). |
| F4 | RESOLVED | Row 2 (line 23): "One file, 5 edits or fewer, obvious fix". Line 33: "Rows 3-4 still obey it: when protocol or spec work crosses that line, put the steps in a checklist file in the protocol or spec folder. **Open question for you:** does an approved spec or protocol checklist count as the task file, or must it be an MDTM task file?" Line 84: "Cross-consumer fixes over 5 edits: checklist per the project rule." Line 86: "(over 5 edits: checklist per the project rule)". | Matches `IC-Harness/CLAUDE.md` Custom Project Rule 6 and the open question in `05-debate-A-lean.md`. Short-docs row left unchanged; acceptable because short docs are single-file. |
| F5 | RESOLVED | Line 112: "A CLI reinstall from `IronClaude-tier-tools` (likely `pipx install --force <path>`, unverified) does NOT update IC-Harness's own `.claude` copies; those need a separate sync. Until then, use the newer commands from inside `IronClaude-tier-tools`." | `which superclaude` is a symlink into `~/.local/pipx/venvs/superclaude`; `pipx list` shows `superclaude 4.2.0`, so pipx is the real install method. `IronClaude-tier-tools/.claude/commands/sc/{workflow,implement,pr-submit,troubleshoot,task,swarm-wizard}.md` are byte-identical to `src/superclaude/commands/`, so "use the newer commands from inside `IronClaude-tier-tools`" holds. |
| F6 | PARTLY RESOLVED (see R-F6) | Line 51: "It diagnoses only. A plain run takes 1-3 min but can grow to about 15 if it escalates; add `--depth quick` to keep it short, or `--depth deep` for several hypotheses plus a debate." Line 52: "`/sc:troubleshoot ... --fix` offers to build a task file once the diagnosis succeeds; accept, then run `/task <path>` yourself." | Line 52 matches `troubleshoot.md:170,192`. `--depth quick` = Tier 1 only, 1-3 min at `:51` (same on master). The 10-word STOP for `--depth deep` (`:33`, same on master) is still missing, and "about 15" understates the total. |
| F7 | RESOLVED | Line 23: "words like security, auth, database, migration, refactor, token, or session auto-escalate to strict" | `IC-Harness/.claude/commands/sc/task.md:74` and master `commands/task.md:74` list security, authentication, authorization, database, migration, refactor, token, session. "auth" is covered by `:77` ("minor auth change" -> still STRICT). |
| F8 | PARTLY RESOLVED (see R-F8) | Lines 12-16: "**Words used here**" box defines Task file (MDTM), BUILD-REQUEST, Reflect, Master. | Four of the five suggested terms were added. "Tier" was left out, and "6-agent check" and the new "fidelity check" are still undefined. |
| F9 | RESOLVED | Line 43: "**No** (June copy). **Yes** when working inside `IronClaude-tier-tools`" | `IronClaude-tier-tools/.claude/commands/sc/workflow.md:7` has `--handoff none|design|implement|tasklist`. |
| F10 | PARTLY RESOLVED (see R-F10) | Row 10 (line 31): "defaults to deep and many agents, say "quick" for the document only or "standard" for document plus build requests". The trap row (line 107) is unchanged: "`/roadmap` only builds task files at deep tier." | `roadmap/SKILL.md:102` ("Default to Deep"), `:106-108` (Quick = document only, Standard = document plus BUILD_REQUESTs, Deep = full pipeline). The trap row in F10's quoted text was not changed. The new "say quick" wording is wrong (N1). |
| F11 | RESOLVED | Line 113 (trap row): "Still in IC-Harness's old copy, removed on master. Use `/sc:recommend`." | `ls IC-Harness/.claude/commands/sc` lists `estimate.md` and `select-tool.md`. |


## Remaining and New Issues

### R-F1 (IMPORTANT). The pr-submit probe setup is stated for both repos, but master needs no probe, and the probe does not save the file

- **Quoted text (line 74):** "Levels 1 (propose fixes for the review bot's findings) and 2 (fix locally, stop before push) need a one-time setup first: a detection probe on a bot-reviewed PR that saves `.dev/pr-monitor/detection-contract.locked.md`; until then they stop with "probe first"."
- **Quoted text (line 110):** "Use 0, or 1 or 2 once the probe is set up."
- **Problem:**
  - (a) The guide tells users to work inside `IronClaude-tier-tools` for newer commands (lines 26, 43, 112). On master, and in `IronClaude-tier-tools/.claude/commands/sc/pr-submit.md` (byte-identical to master), there is no probe requirement: "a missing or unlocked override is not a halt. No R1 probe is required." The master STOP line no longer mentions the contract. The probe requirement applies only to the IC-Harness June copy.
  - (b) In IC-Harness, the probe does not save the file. The operator writes it: "write the gitignored operator-local override ... with `locked: true`" (`IC-Harness/.claude/commands/sc/pr-submit.md:61`), and the Boundaries say "Will Not: ... auto-lock the detection contract" (`:80`). The guide also gives no way to run "a detection probe". The only runbook is `IronClaude-tier-tools/.dev/tasks/to-do/TASK-RF-submit-pr-20260611-030241/phase-outputs/plans/r1-detection-probe-runbook.md`. No probe script exists in either `scripts/` folder; both contain only `poll-augment-review.sh`, `reply-resolve-thread.sh` and `retrigger-review.sh`, and master adds `poll-ci-checks.sh`.
- **Evidence:** `diff IC-Harness/.claude/commands/sc/pr-submit.md IronClaude-tier-tools/src/superclaude/commands/pr-submit.md` (lines 29, 61 vs master 66); `IronClaude-tier-tools/src/superclaude/pr_submit/detection.py:35-39` ("Optional operator-local contract (gitignored). Preferred at arm time when present; NEVER required."); `IC-Harness/.claude/skills/sc-pr-submit-protocol/refs/detection-contract.md:7-8,29`.
- **Replacement (line 74):** "3. `/sc:pr-submit --monitor 0 --head <branch> --title "..." --body "..."` opens the PR only. Level 1 also proposes fixes for the review bot's findings, and level 2 fixes locally and stops before push. Inside `IronClaude-tier-tools` (master), levels 1 and 2 need no setup. In IC-Harness (June copy), they stop with "probe first" until you do a one-time setup: follow the R1 probe runbook (`IronClaude-tier-tools/.dev/tasks/to-do/TASK-RF-submit-pr-20260611-030241/phase-outputs/plans/r1-detection-probe-runbook.md`) on a PR the Augment bot has reviewed. Then write `.dev/pr-monitor/detection-contract.locked.md` with `locked: true` yourself, because the command never writes it. Always pass `--monitor`; the default is 2."
- **Replacement (line 110):** "Pushes on its own. Use 0, or 1 or 2 (in IC-Harness, only after the probe setup in section 4). No `--monitor` means 2."

### R-F6 (MINOR). Troubleshoot: the 10-word rule for deep is still missing, and "about 15" understates the time

- **Quoted text (line 51):** "A plain run takes 1-3 min but can grow to about 15 if it escalates; add `--depth quick` to keep it short, or `--depth deep` for several hypotheses plus a debate."
- **Problem:**
  - Tier 2 adds "+4-15 min" on top of Tier 1's "1-3 min", so an escalated run takes about 5-18 min, not "about 15".
  - `--depth deep` STOPs when the description is under 10 words and there is no `--scope`. F6 flagged this, and the guide still leaves it out.
- **Evidence:** `IC-Harness/.claude/commands/sc/troubleshoot.md:33,75-76`; master `commands/troubleshoot.md:33,75-76` are identical.
- **Replacement (line 51):** "It diagnoses only. A plain run takes 1-3 min but can grow to about 18 min (1-3 plus 4-15) if it escalates; add `--depth quick` to cap it at 1-3 min, or `--depth deep` for several hypotheses plus a debate (describe the symptom in 10 or more words or add `--scope <path>`, otherwise it stops and asks for detail)."

### R-F8 (MINOR). The "Words used here" box still leaves three terms undefined

- **Quoted text:** line 28 "Deep tier"; line 107 "at deep tier"; line 41 "a 6-agent check", "fidelity check" (the fidelity check is new text from the F3 fix).
- **Problem:** "Tier" was in F8's suggested list and was not added. "6-agent check" was named in F8 and is still not explained. "Fidelity check" is new jargon added by the F3 fix.
- **Evidence:** guide lines 12-16 (four bullets only); `task/SKILL.md:117` (6+ agents = 3 structural plus 3 content reviewers, then a serialized fix), `:119` (Step 4 "source-document fidelity gate").
- **Replacement (append to the box after line 16):**
  - "- **Tier:** how deep a skill researches and checks (quick/standard/deep; section 7 lists skills that use other words)."
  - "- **6-agent check:** the QA gate `/task` runs: at least 6 separate reviewer agents (3 structural, 3 content), then one fix pass."
  - "- **Fidelity check:** a final pass that confirms the output still matches its source documents."

### R-F10 (MINOR). The roadmap trap row is unchanged

- **Quoted text (line 107):** "`/roadmap` only builds task files at deep tier."
- **Problem:** F10 quoted this exact line and gave a replacement. Row 10 was fixed, but this row still reads as if deep must be requested. A reader who scans only the Traps table gets the misleading version.
- **Evidence:** `roadmap/SKILL.md:102,106-108`.
- **Replacement (line 107, last sentence):** "`/roadmap` defaults to deep, which builds task files for every phase; the Quick tier gives the document only, and Standard adds build requests."

### N1 (MINOR, introduced by the F10 fix; the same flaw already exists in row 8). Saying "quick" lowers QA intensity; it does not select the Quick tier

- **Quoted text (line 31, new):** "say "quick" for the document only or "standard" for document plus build requests".
- **Quoted text (line 29, pre-existing, missed by `07`):** "(say "quick" unless you want deep; it defaults to deep)".
- **Problem:** In both skills, the word "quick" maps to the QA-intensity dial, not the depth tier: "If the user says "quick", "fast", "light QA", or "basic" -> lite." Tier is picked from the input's complexity ("Only use Quick for genuinely simple requests", "If in doubt, pick Deep"). There is no user-word rule that selects the Quick tier. A user who just says "quick" can still get a Deep roadmap, which builds task files for every phase, with lite QA.
- **Evidence:** `IC-Harness/.claude/skills/roadmap/SKILL.md:102,110-114,124`; `tech-research/SKILL.md:97,119`.
- **Replacement (line 31):** "defaults to deep and many agents. Ask explicitly for the "Quick tier" for the document only, or the "Standard tier" for document plus build requests. The word "quick" on its own only lowers QA."
- **Replacement (line 29):** "(ask explicitly for the "Quick tier" unless you want deep, because it defaults to deep; the word "quick" on its own only lowers QA)".

## New-Claim Re-verification (no finding)

| Claim | Verified at |
|---|---|
| `--monitor` default 2 (both repos) | `IC-Harness/.claude/commands/sc/pr-submit.md:26,45`; master diff shows those lines unchanged |
| `--head/--title/--body` is a valid PR context | `pr-submit.md:27,34` |
| Probe override path `.dev/pr-monitor/detection-contract.locked.md` | `pr-submit.md:61`; master `pr_submit/detection.py:39` |
| `--depth quick` = Tier 1 only, 1-3 min | `troubleshoot.md:51,75` (both repos) |
| `--fix` offers the task file only after success; the user runs `/task` | `troubleshoot.md:170,192` |
| `/sc:task` STRICT keywords | `task.md:74,77` (both repos) |
| `/sc:task` runs tests at STANDARD | `sc-task-protocol/SKILL.md:105,127,314` |
| `/roadmap` defaults to Deep; Quick = document only; Standard = document plus BUILD_REQUESTs | `roadmap/SKILL.md:102,106-108` |
| `/task` 6-agent gate, post-completion and fidelity | `task/SKILL.md:117-119,190` |
| "Master" = `IronClaude-tier-tools` | Checkout is on branch `feat/tier-tools-update`, but `git rev-list --left-right --count origin/master...HEAD` = `0 0`, so its content equals master. Acceptable. |
| CLI is pipx-installed 4.2.0 | `pipx list`; `~/.local/bin/superclaude` symlink |
| `/sc:swarm-wizard` present in IC-Harness and needs the swarm CLI | `IC-Harness/.claude/commands/sc/swarm-wizard.md:16,60` |
| No em dashes (U+2014) or en dashes (U+2013) | `grep -n $'—'`, `grep -n $'–'` and a byte-level `grep -P '\xe2\x80[\x93\x94]'` on the guide all returned exit 1 (no matches) |

## Summary

| Status | Count | IDs |
|---|---|---|
| Resolved | 7 | F2, F3, F4, F5, F7, F9, F11 |
| Partly resolved | 4 | F1 (IMPORTANT), F6, F8, F10 (MINOR) |
| New | 1 | N1 (MINOR) |
| Regressions | 0 | none |

- Remaining issues: 5 (cycle 0: 11). Strictly fewer, so no `[HALT-MONOTONICITY]`. Fix cycles used: 1 of 3.
- Issues fixed in place: 0 (report-only by instruction).

## Confidence Gate

- **Confidence:** Verified: 11/11 prior findings plus 13 new-claim checks plus the dash grep | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (this measures the review's coverage, not the guide's quality)
- **Tool engagement:** Read: 2 | Grep: 0 | Glob: 0 | Bash: 11 (sed, grep, diff, git, pipx and ls against the specific source files cited above) | Write: 1 | Edit: 2. No web research was performed.
- Not checked: whether a pipx reinstall from the source tree actually succeeds (the guide marks it unverified, which is acceptable); the contents of the R1 runbook beyond the fact that it exists.

## QA Complete
