# QA Report: Final Fix-Cycle QA, Part 1 (Sections 1, 2, Workflows 3.1-3.4)

**Topic:** IronClaude New User Guide, all lenses (accuracy, redundancy, workflow completeness)
**Date:** 2026-10-02
**Phase:** fix-cycle (adversarial; report-only, guide NOT edited)
**Fix cycle:** 2 (re-verifies in-scope findings from 14, 15, 16)
**Guide:** `/Users/cmerritt/GFxAI/IC-Harness/.dev/research/ironclaude-user-guide-20261001/IRONCLAUDE-NEW-USER-GUIDE.md` (242 lines; scope = L1-L131)
**Source truth:** `/Users/cmerritt/GFxAI/IronClaude-tier-tools/src/superclaude/` (abbreviated `SRC/`)
**Author decisions respected:** `--spec` only for a spec/PRD/TDD (never a research or troubleshoot report); ruling-line format referenced by file path; hard limit excludes a matching test file.

---

## Overall Verdict: FAIL

Every in-scope prior finding is resolved (22 of 22; 1 resolved by author decision). One new accuracy defect remains in 3.4 step 1 (`--depth deep` described as skipping the first pass). No redundancy defects found. Out-of-scope remnants (L202, L227, L236, 3.7, 3.10, section 5) are not judged here.

## Part 1: Prior findings in scope

| Source | # | Status | New text (quoted, guide line) | Evidence |
|---|---|---|---|---|
| 14 | N1 | RESOLVED (author decision) | L36: "`/task-builder \"Add per-tenant rate limits as recommended in .dev/tasks/to-do/TASK-RESEARCH-rate-limits-<timestamp>/RESEARCH-REPORT-rate-limits.md. ...\"`"; L17 same shape, no `--spec` | Author ruled `--spec` is for a driving spec only, matching `SRC/skills/task-builder/SKILL.md:41` "driving spec/PRD/TDD". Consequence (`reflect_pre: skipped`, `:1666`) is handled in 3.10, out of scope |
| 14 | N2 | OUT OF SCOPE (3.10) | n/a | n/a |
| 14 | N3 | RESOLVED | L128: "If you did not pass `--fix`, do not diagnose again; build the task file from the report you already have: `/task-builder \"Fix the root cause described in .../REPORT.md ...\"`" | No re-diagnosis; no `--spec` on a report, per author decision |
| 14 | O1 | RESOLVED | L72: "At its full setting it also checks the phase task files against the roadmap and your PRD and TDD; those check reports are in the roadmap folder's `qa/` subfolder." L73 adds `--spec docs/billing/TDD_BILLING.md` | `SRC/skills/roadmap/SKILL.md:106-108` (only Deep makes task files), `:665` (input-to-task fidelity to `qa/`) |
| 14 | O2 | RESOLVED | L115: "**Ship.** Run the tests yourself only if nothing ran them ... Then follow workflow 3.11. Its `/code-review` step looks for bugs" | `/code-review` now runs once, in 3.11 |
| 15 | Error 6 | RESOLVED in scope | L16: "after each phase except the first (setup) one"; L77: "reviewer panels after each group of items inside it (except the first, setup group)" | `SRC/skills/task/SKILL.md:188`, `:282`. L227 is out of scope |
| 15 | N1 | RESOLVED in scope | L79: "The task folder stays in `.dev/tasks/to-do/` when `/task` finishes; moving it to `.dev/tasks/done/` is a separate step your lead will tell you about." | POST item is penultimate, before status-to-Done (`SRC/skills/task-builder/SKILL.md:2233`). L202/L236 out of scope |
| 15 | N2 | RESOLVED | L98: "If the check fails (less than 90% of requirements covered), the missed requirements are added to the task file's Open Questions." | `SRC/skills/task-builder/SKILL.md` A.10.7 routing: floor 0.90, fail appends `unmapped_requirements` |
| 15 | N3 | RESOLVED | L15: "a progress file under `.dev/implement/plan-<code>/progress.md` (the tool prints the exact path)" | `SRC/skills/sc-implement-protocol/SKILL.md:54` (basename + hash8), `:148` (prints ledger path) |
| 15 | N4 | RESOLVED | L113: "Copy its exact form ... from the \"Ruling line\" section of `src/superclaude/skills/sc-implement-protocol/refs/ledger.md`" | Section exists at `refs/ledger.md:61`; regex `:70`; executor never writes it `refs/qa.md:65` |
| 15 | N5 | RESOLVED | L26: "If the first one is missing or vague, the skill stops and asks you for it. The other three are optional" | `SRC/skills/tech-research/SKILL.md:82`, `SRC/skills/task-builder/SKILL.md:102` |
| 15 | N6 | OUT OF SCOPE (3.7) | n/a | n/a |
| 15 | N7 | RESOLVED | L122: "If the diagnosis succeeds, it then offers to build a task file for the fix" | `SRC/commands/troubleshoot.md:170`; protocol `:550` |
| 15 | N8 | RESOLVED for L72 (3.10 part out of scope) | L72 quoted above | As 14 O1 |
| 16 | N1 | RESOLVED | L113 quoted above | As 15 N4 |
| 16 | N2 | RESOLVED | L20: "touches more than one source file (its matching test file does not count) ... The one exception is `/sc:cleanup` and `/sc:improve` run on a folder (3.7)" | L14 and L127 now fit the limit |
| 16 | N3 | RESOLVED in scope | L72, L73 quoted above | As 14 O1 |
| 16 | N4 | RESOLVED | L16: "If you have a spec, PRD, or TDD, add `--spec <path to it>`" | `SRC/skills/task-builder/SKILL.md:41` (optional) |
| 16 | N5 | RESOLVED | L128 (no re-diagnosis, stop-note link "see the note at the end of 3.1"); L129: "**If the report says the cause is not confirmed:** do not fix anything yet." | `SRC/commands/troubleshoot.md:170` |
| 16 | N6 | RESOLVED | L115 quoted above | As 14 O2 |
| 16 | N7 | RESOLVED | L16: "The items are grouped into phases"; L77: "after each group of items inside it"; L73: "(A build request is the short input file `/task-builder` turns into a task file.)" | Inline definitions present |
| 16 | N8 | OUT OF SCOPE (section 5) | n/a | n/a |
| 16 | N9 | RESOLVED | As 15 N3 | As 15 N3 |
| 16 | N10 | RESOLVED | L79: "Decide each one with your lead ... fix the code, correct the spec, or accept it in writing. Only if you changed anything ..., re-confirm with `/sc:reflect --mode post --tasklist ... --spec ... --diff <first commit of this phase>..HEAD --no-promote`" | Flags valid: `SRC/commands/reflect.md:10`, `:28` |

## Part 2: New issues

### F1 [MINOR, accuracy] 3.4 step 1 says `--depth deep` skips the first pass (guide L121)

- **Quoted (L121):** "`--depth deep` goes straight to several agents testing competing explanations."
- **Evidence:** `SRC/commands/troubleshoot.md:51`: "`deep` (force Tier 2 with adversarial debate)". `SRC/commands/troubleshoot.md:177` (Will Not): "Skip Tier 1 and jump straight to Tier 2 (even with `--depth deep`, Tier 1 still runs first and its output feeds Tier 2)". Same at `SRC/skills/sc-troubleshoot-protocol/SKILL.md:598`. The guide says the opposite of the source's explicit prohibition, and it implies a shorter run than the user will get.
- **Replacement (L121):** "`--depth quick` stops it after the first pass; `--depth deep` always brings in several agents to test competing explanations after the first pass."

No redundancy defects found: no in-scope step repeats a check a skill already runs (Part 3 rows R1-R6).

## Part 3: Claim-by-claim re-verification (in scope)

| # | Guide line | Claim / command / flag / path | Result | Source |
|---|---|---|---|---|
| V1 | L13 | `/sc:explain <file>` | PASS | `SRC/commands/explain.md:22` |
| V2 | L14 | `/sc:task` runs tests for normal/risky, skips for trivial (typo, comment) | PASS | `SRC/skills/sc-task-protocol/SKILL.md:126-129`; `SRC/commands/task.md:85` |
| V3 | L15 | `/sc:workflow ... --depth quick`; plan at `.dev/workflow/<name>/plan.md`; acceptance criteria per step | PASS | `SRC/commands/workflow.md:7`, `:41`, `:67`; `SRC/skills/sc-workflow-protocol/SKILL.md:44` |
| V4 | L15 | `/sc:implement @plan.md`; reviewer checks each step; `--resume` | PASS | `SRC/commands/workflow.md:82`; `SRC/skills/sc-implement-protocol/SKILL.md` Q3 REVIEW; `SRC/commands/implement.md:6`, `:57` |
| V5 | L16 | Task file under `.dev/tasks/to-do/`; `--spec` optional; panels skip Phase 1; tests at end; resumes | PASS | `SRC/skills/task-builder/SKILL.md:41`; `SRC/skills/task/SKILL.md:10`, `:188`, Step 0 check 4 (tests) |
| V6 | L17 | Report path `TASK-RESEARCH-<topic>-<timestamp>/RESEARCH-REPORT-<topic>.md` | PASS | `SRC/skills/tech-research/SKILL.md:38`, `:136` |
| V7 | L18, L20 | Level 6 chain; hard limit with test-file and cleanup exception | PASS | Internally consistent with L14, L106, L127 |
| V8 | L26 | Missing/vague "what" stops the skill | PASS | `SRC/skills/tech-research/SKILL.md:82`; `SRC/skills/task-builder/SKILL.md:102` |
| V9 | L48-49 | `/sc:brainstorm --depth standard`; output `.dev/brainstorms/<ts>-<slug>/merged-requirements.md`; stops (handoff default none) | PASS | `SRC/commands/brainstorm.md:49`, `:60`, `:61`, `:191` |
| V10 | L56, L63 | `/sc:spec-panel @file --mode critique --focus requirements` / `architecture,testing` | PASS | `SRC/commands/spec-panel.md:22`, `:25` |
| V11 | L67-68 | `/sc:release-split <spec>`; output `<spec-dir>/release-split/` | PASS | `SRC/commands/release-split.md:19`, `:53` |
| V12 | L71-73 | `/roadmap` dry run waits for yes; "full roadmap" forces Deep; `build-requests/BUILD_REQUEST-phase-NN-<name>.md`; folder `TASK-ROADMAP-<subject>-<ts>`; summary lists task files in execution order; `qa/` reports | PASS | `SRC/skills/roadmap/SKILL.md:112`, `:141`, `:247`, `:284`, `:665`, `:671`, `:2614-2640` |
| V13 | L77, L79 | POST audit is last step before Done; records `reflect_post`; unfixed deviations to Open Questions; folder not moved | PASS | `SRC/skills/task-builder/SKILL.md:2231-2233` |
| V14 | L85 | Stop writes to Task Log; status Blocked; resume from first unchecked item | PASS | `SRC/skills/task/SKILL.md:21`, `:170`, `:177`, `:180` |
| V15 | L94 | `/sc:design <name> --type api --format spec` | PASS | `SRC/commands/design.md:22` |
| V16 | L97-98 | `--spec` drives PRE check; `reflect_pre` in frontmatter; 90% floor; skipped without spec | PASS | `SRC/skills/task-builder/SKILL.md` A.10.7 (sign-off block, verdict routing) |
| V17 | L113 | `E-HALT-QA` after failed fix pass; prints ledger path; ruling-line file path; never auto-written | PASS | `SRC/skills/sc-implement-protocol/refs/qa.md:61`, `:65`; `refs/ledger.md:61-70` |
| V18 | L120-121 | `--type bug|test|build|performance|deployment`; timings 1-3 min, +4-15 min; `--depth quick` | PASS | `SRC/commands/troubleshoot.md:50-51`, `:75-76` |
| V19 | L121 | `--depth deep` "goes straight to" Tier 2 | FAIL (F1) | `SRC/commands/troubleshoot.md:177` |
| V20 | L122 | `--fix` offer only on success; changes nothing unless accepted | PASS | `SRC/commands/troubleshoot.md:54`, `:170`; protocol `:550` |
| V21 | L124 | `.dev/troubleshoot/<name>-<timestamp>/REPORT.md`; fix target code/test/docs | PASS | `SRC/commands/troubleshoot.md:57`; `SRC/skills/sc-troubleshoot-protocol/SKILL.md:75` (`remediation_target`) |
| V22 | L127 | `/sc:test <file> --coverage` | PASS | `SRC/commands/test.md:22` |
| V23 | L1-131 | Em dashes / en dashes | PASS (0 / 0) | Python count over lines 1-131 |

### Redundancy check (steps vs. what skills already do)

| # | Guide step | Possible repeat | Verdict |
|---|---|---|---|
| R1 | L77, L79 (3.1 steps 8-9) | Re-running panels, tests, or POST audit | KEEP: guide says "Do not run those checks again yourself"; re-confirm only "if you changed anything" |
| R2 | L98-100 (3.2) | Re-running PRE check after `--spec` | KEEP: reads `reflect_pre`, no re-run |
| R3 | L112, L115 (3.3) | Tests after `/sc:implement` | KEEP: tests only "if nothing ran them"; `/code-review` once via 3.11 |
| R4 | L128 (3.4) | Re-diagnosis on non-`--fix` path | KEEP: explicitly forbidden ("do not diagnose again") |
| R5 | L128 (3.4) | Troubleshoot Phase D `/sc:reflect --validate` | KEEP the omission: task file's own POST item runs it (`SRC/skills/task-builder/SKILL.md:2233`) |
| R6 | L57, L64 (spec-panel loop) | Repeating `/prd`/`/tdd` own QA | KEEP: external critique, report-only (`SRC/commands/spec-panel.md` Boundaries) |

## Items Reviewed

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Prior findings in scope (22 checked, 4 out of scope) | PASS | Part 1 |
| 2 | Section 1 claims (V1-V7) | PASS | Part 3 |
| 3 | Section 2 claims (V8) | PASS | Part 3 |
| 4 | 3.1 claims (V9-V14) | PASS | Part 3 |
| 5 | 3.2 claims (V15-V16) | PASS | Part 3 |
| 6 | 3.3 claims (V17) | PASS | Part 3 |
| 7 | 3.4 claims (V18-V22) | FAIL | F1 (V19) |
| 8 | Redundancy (R1-R6) | PASS | Part 3 |
| 9 | Style: no em/en dashes in scope | PASS | V23 |

## Summary

- Prior in-scope findings: 22 of 22 resolved (14 N1 by author decision). Out of scope: 14 N2, 15 N6, 16 N8, and the L202/L227/L236/3.10 parts of 15 Error 6, N1, N8.
- New issues: 1 (MINOR: F1). CRITICAL 0, IMPORTANT 0.
- Checks passed: 8 / 9. Issues fixed in place: 0 (report-only).
- Monotonicity: in-scope count fell from the prior cycle (14: 3, 15: 9, 16: 10, of which the in-scope share was well above 1) to 1. No previously PASS item regressed.
- Removals proposed: none.

## Confidence Gate

- **Confidence:** Verified: 9/9 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%. Verdict is FAIL because F1 exists, not for low confidence.
- **Tool engagement:** Read: 4 | Grep: 0 (content search via Bash grep/sed, 11 calls) | Glob: 0 | Bash: 14 | Write: 1 | Edit: 3. No web research (tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0).
- **Self-Audit:** not required (verdict FAIL). Once F1's replacement is applied, this part has no open issues.

## QA Complete
