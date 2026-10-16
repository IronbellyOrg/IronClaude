# QA Report: Fix Cycle 2 for IronClaude Quick Guide (adversarial, report-only)

**Target:** `IRONCLAUDE-QUICK-GUIDE.md` (116 lines, read in full; not edited)
**Prior report:** `08-qa-fix-cycle.md` (open: R-F1, R-F6, R-F8, R-F10, N1)
**Source truth checked:** `IronClaude-tier-tools/src/superclaude/` (`git rev-list --left-right --count origin/master...HEAD` = `0 0`), `IC-Harness/.claude/commands/sc/`, `IC-Harness/.claude/skills/`, installed pipx `superclaude` package
**Date:** 2026-10-01
**Phase:** fix-cycle
**Fix cycle:** 2

---

## Overall Verdict: FAIL

Four of the five open items are resolved (R-F6, R-F8, R-F10, N1). R-F1 is only partly resolved. The new text also brought in 2 new errors (N2, N4), and the row 7 "ask for deep" check found 1 more (N3). Remaining issues: 4 (cycle 1: 5). The count went down, so the monotonicity halt does not fire. No regressions: everything that passed in `08` still passes. Fix cycles used: 2 of 3.

## Prior Findings Status

| ID | Status | New guide text (quoted) | Verification |
|---|---|---|---|
| R-F1 | PARTLY RESOLVED (see R-F1b) | Line 77: "Inside `IronClaude-tier-tools`, levels 1 and 2 need no setup. In IC-Harness (June copy) they stop with "probe first" until a one-time setup: follow `IronClaude-tier-tools/.dev/tasks/to-do/TASK-RF-submit-pr-20260611-030241/phase-outputs/plans/r1-detection-probe-runbook.md` on a bot-reviewed PR, then write `.dev/pr-monitor/detection-contract.locked.md` with `locked: true` yourself." Line 113: "Use 0, or 1 or 2 (in IC-Harness, only after the probe setup in section 4)." | Master claim is correct: `src/superclaude/commands/pr-submit.md:66` "a missing or unlocked override is not a halt. No R1 probe is required." The runbook path exists (`ls`: 4815 bytes) and is git-tracked on master (`git ls-tree origin/master`). The IC-Harness "probe first" STOP is real (`IC-Harness/.claude/commands/sc/pr-submit.md:29`). But the IC-Harness setup path the guide describes does not lead to working levels 1 and 2. See R-F1b. |
| R-F6 | RESOLVED | Line 54: "A plain run takes 1-3 min but can grow to about 18 if it escalates; add `--depth quick` to cap it at 1-3 min, or `--depth deep` for several hypotheses plus a debate (describe the symptom in 10+ words or add `--scope <path>`, otherwise it stops and asks for detail)." | `troubleshoot.md:33` (10-word STOP), `:51` (quick = Tier 1 only, 1-3 min), `:75` (Tier 1, 1-3 min), `:76` (Tier 2 +4-15 min, 2-4 specialists, adversarial debate). Lines match in IC-Harness and on master. |
| R-F8 | RESOLVED (but see N2) | Lines 17-19: "**Tier:** how deep a skill researches and checks (quick/standard/deep; section 7 lists skills that use other words)." / "**6-agent check:** the QA gate `/task` runs: at least 6 separate reviewers (3 structural, 3 content), then one fix pass." / "**Fidelity check:** a final pass confirming the output still matches its source documents." | All three terms are now defined. Tier and Fidelity match `task/SKILL.md:119,369` and guide line 114. "then one fix pass" is wrong (N2). |
| R-F10 | RESOLVED | Line 110: "`/roadmap` defaults to deep, which builds task files for every phase; the Quick tier gives the document only, and Standard adds build requests." | `roadmap/SKILL.md:102` ("Default to Deep"), `:106-108` (Quick = document only; Standard = document plus BUILD_REQUESTs; Deep = full pipeline incl. task files). Same on master (`:111`). |
| N1 | RESOLVED (but see N4) | Line 32: "(it defaults to deep; ask explicitly for the "Quick tier" otherwise, because the word "quick" on its own only lowers QA)". Line 34: "ask explicitly for the "Quick tier" for the document only, or the "Standard tier" for document plus build requests; the word "quick" on its own only lowers QA". | "quick" maps to lite QA: `roadmap/SKILL.md:124`, `tech-research/SKILL.md:119` (master `roadmap:124`, `tech-research:119`). The statement that the word alone only lowers QA is now correct. |

## Remaining and New Issues

### R-F1b (IMPORTANT). Levels 1 and 2 cannot run from IC-Harness, and the runbook does not fit IC-Harness

- **Quoted text (line 77):** "In IC-Harness (June copy) they stop with "probe first" until a one-time setup: follow `IronClaude-tier-tools/.dev/tasks/to-do/TASK-RF-submit-pr-20260611-030241/phase-outputs/plans/r1-detection-probe-runbook.md` on a bot-reviewed PR, then write `.dev/pr-monitor/detection-contract.locked.md` with `locked: true` yourself."
- **Quoted text (line 113):** "Use 0, or 1 or 2 (in IC-Harness, only after the probe setup in section 4)."
- **Problem:** Both lines say levels 1 and 2 will work in IC-Harness once you do the setup. That is not true, for three reasons:
  - (a) **The code is missing.** The IC-Harness skill arms by calling `superclaude.pr_submit.DetectionContract.for_arming()` and refuses to arm if no locked contract loads (`IC-Harness/.claude/skills/sc-pr-submit-protocol/SKILL.md:90`). It also calls `remap_severity` from the same module (`:91`). The installed CLI 4.2.0 has no `pr_submit` package: `ls .../site-packages/superclaude/pr_submit` gives "No such file or directory", and `~/.local/pipx/venvs/superclaude/bin/python -c "import superclaude.pr_submit"` gives `ModuleNotFoundError`. IC-Harness has no copy of that Python code either. A probe and an override file do not fix this.
  - (b) **The runbook is written for the IronClaude repo, not IC-Harness.** Every capture command is pinned to `--repo IronbellyOrg/IronClaude`. IC-Harness's origin is `IronbellyOrg/IronFlow`. Capture 5 writes to `/config/workspace/IronClaude/.dev/pr-monitor/probe/`, and that path does not exist on this Mac.
  - (c) **The runbook's lock step contradicts the guide.** The runbook says to edit the shipped `src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md`, flip it to `locked: true`, and run `make sync-dev`. The guide says to write the local override instead. The override also needs the captured values (bot login, emission shape, findings locus, and so on), not only `locked: true`: "populated by the R1 probe with this fork's real Augment values" (`SKILL.md:90`), and the fields are listed in `refs/detection-contract.md` (YAML block, lines 14-30; `locked:` at 29).
- **Evidence:** runbook "The 5 captures" and "After capture" sections; `IC-Harness/.claude/skills/sc-pr-submit-protocol/SKILL.md:90-91`; `git -C IC-Harness remote get-url origin` = `https://github.com/IronbellyOrg/IronFlow.git`; pipx package listing (no `pr_submit`).
- **Replacement (line 77):** "3. `/sc:pr-submit --monitor 0 --head <branch> --title "..." --body "..."` opens the PR only. Level 1 also proposes fixes for the review bot's findings; level 2 fixes locally and stops before push. Use levels 1 and 2 only from inside `IronClaude-tier-tools`, where they need no setup. In IC-Harness (June copy) they do not work: they stop with "probe first", and the code they need is not in your installed CLI (4.2.0). Always pass `--monitor`; the default is 2."
- **Replacement (line 113):** "Pushes on its own. Use 0; use 1 or 2 only inside `IronClaude-tier-tools`. No `--monitor` means 2."

### N2 (MINOR, introduced by the R-F8 fix). "then one fix pass" is wrong

- **Quoted text (line 18):** "**6-agent check:** the QA gate `/task` runs: at least 6 separate reviewers (3 structural, 3 content), then one fix pass."
- **Problem:** The gate does not stop after a single fix pass. It runs a fix agent and then a verification round, and it repeats both until the gate passes, up to 3 cycles. After that it halts and asks the user. The wording came from the `08` replacement, so `08` was wrong here too.
- **Evidence:** `IC-Harness/.claude/skills/task/SKILL.md:117` (minimum 6 agents, then the Serialized Fix Protocol), `:256` ("Maximum 3 fix cycles total ... After 3 failed cycles: HALT"), `:329` ("spawn a single fix agent, then a verification round. Maximum 3 fix cycles."), `:359` ("repeat from step 2 ... Maximum 3 fix cycles total per gate").
- **Replacement (line 18):** "- **6-agent check:** the QA gate `/task` runs: at least 6 separate reviewers (3 structural, 3 content), then a fix and a re-check, repeated up to 3 times before it stops and asks you."

### N3 (MINOR, asked-for check). Saying "deep" does not select task-builder's Deep tier

- **Quoted text (line 31, row 7):** "Same, ask for **deep**" with result "Deep tier, more researchers and QA".
- **Quoted text (line 42):** "`/task-builder <goal>` (Standard by default; say "deep" for big work)".
- **Problem:** task-builder's trigger words are "thorough", "comprehensive", and "deep dive". "deep" is not on the list. Row 7's own situation (20+ files or several subsystems) already selects Deep based on scope, so asking for it is unnecessary. The guide makes the word "deep" sound like the switch, which is the same flaw N1 fixed for "quick".
- **Evidence:** `IC-Harness/.claude/skills/task-builder/SKILL.md:132` ("Default to Standard unless ... clearly large (20+ files, multiple subsystems)"), `:138` (Deep = 20+ files, multiple subsystems), `:143` ("If the user says "thorough", "comprehensive", or "deep dive" -- always Deep"), `:145` (multiple subsystems: always Deep). Master `task-builder/SKILL.md:132,143` is identical.
- **Replacement (line 31, Use cell):** "Same. Deep is picked on its own at this size; to force it, say "deep dive" or "thorough""
- **Replacement (line 42, parenthetical):** "(Standard by default; Deep on its own for 20+ files or several subsystems, or say "deep dive" or "thorough")"

### N4 (MINOR, introduced by the N1 fix). Nothing confirms that asking for the "Quick tier" gets it

- **Quoted text (line 32):** "ask explicitly for the "Quick tier" otherwise".
- **Quoted text (line 34):** "ask explicitly for the "Quick tier" for the document only, or the "Standard tier" for document plus build requests".
- **Problem:** Neither skill lets the user override the tier. Only QA intensity has an "Override allowed" column and user words. The tier is chosen from the input: "Select a tier based on input complexity", "Only use Quick for genuinely simple requests", "If in doubt, pick Deep". The guide presents an explicit request as a sure way to get Quick, and the source does not support that. The wording came from the `08` replacement, so `08` overstated it too.
- **Evidence:** `roadmap/SKILL.md:102,110-114,118-126`; `tech-research/SKILL.md:97,105-109,113-121` (IC-Harness; master `roadmap:111-112`, `tech-research:106-107` match).
- **Replacement (line 32 parenthetical):** "(it defaults to deep and chooses the tier from the question's size; the word "quick" on its own only lowers QA. To get the Quick tier, say so explicitly and confirm the tier it reports before it fans out)"
- **Replacement (line 34, from "defaults to deep"):** "defaults to deep and many agents and chooses the tier from the input's size. For the document only (Quick tier) or document plus build requests (Standard tier), say so explicitly and confirm the tier it reports; the word "quick" on its own only lowers QA"

## Changed-Claim Re-verification (no finding)

| Claim | Verified at |
|---|---|
| Master pr-submit needs no probe | `IronClaude-tier-tools/src/superclaude/commands/pr-submit.md:66`; `pr_submit/detection.py` comment "Preferred at arm time when present; NEVER required." |
| IC-Harness pr-submit stops with "probe first" | `IC-Harness/.claude/commands/sc/pr-submit.md:29,61`; skill `SKILL.md:133` |
| Runbook path exists | `ls -la` (4815 bytes, 2026-09-30); `git ls-files --error-unmatch` exit 0; present in `git ls-tree origin/master` |
| Troubleshoot timings and 10-word STOP | `troubleshoot.md:33,51,75,76`, identical in both repos |
| Fidelity check definition | `task/SKILL.md:119,369` ("verifies that generated output faithfully represents its source inputs") |
| Roadmap trap row tiers | `roadmap/SKILL.md:102,106-108` |
| "quick" maps to lite QA only | `roadmap/SKILL.md:124`, `tech-research/SKILL.md:119` |
| No em dashes (U+2014) or en dashes (U+2013) in the guide | `grep -n $'\xe2\x80\x94'` exit 1 and `grep -n $'\xe2\x80\x93'` exit 1 (no matches) |

## Summary

| Status | Count | IDs |
|---|---|---|
| Resolved | 4 | R-F6, R-F8, R-F10, N1 |
| Partly resolved | 1 | R-F1 (now R-F1b, IMPORTANT) |
| New | 3 | N2, N4 (both MINOR and introduced by the cycle-1 fixes); N3 (MINOR, existed before but was missed until the requested check) |
| Regressions | 0 | none |

- Remaining issues: 4 (cycle 1: 5; cycle 0: 11). The count went down again, so no `[HALT-MONOTONICITY]`. Fix cycles used: 2 of 3. If anything is still open after cycle 3, halt and ask the user.
- Issues fixed in place: 0 (report-only by instruction).
- Two of the new errors (N2, N4) came from wording that `08` itself recommended. If you apply the replacements in this report, check them against the cited lines; do not trust them without checking.

## Confidence Gate

- **Confidence:** Verified: 5/5 prior items, 3 new findings with source lines, 8 changed-claim checks, and the dash grep | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (this measures how much of the review was covered, not how good the guide is)
- **Tool engagement:** Read: 2 | Grep: 0 | Glob: 0 | Bash: 13 (grep, sed, ls, git, the pipx python import test, against the cited files) | Write: 1 | Edit: 4. No web research was performed.
- **Not checked:** whether `uv run` inside `IronClaude-tier-tools` actually imports `superclaude.pr_submit` end to end (master `detection.py` exists, so the replacement's "only from inside `IronClaude-tier-tools`" depends on that checkout's own environment). Also not checked: whether the Augment bot is installed on `IronbellyOrg/IronFlow`.

## QA Complete
