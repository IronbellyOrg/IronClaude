# Refactoring Plan: Merge into Base (Variant 2, CLAY)

## Overview
- Base: Variant 2 (CLAY, `variant-2-original.md`)
- Incorporating strengths from: Variant 1 (OURS, `variant-1-original.md`), plus debate outputs (`debate-transcript.md`, `invariant-probe.md`)
- Planned changes: 8
- Risk level: Low (all additive or wording fixes; no claim of the base is removed without a debate-backed reason)
- Output file: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D02/adversarial/merged-position-d02.md`
- The merged text is a neutral "settled facts and open items" paper for the scheduler question, not a third advocacy paper. It must not state a winner (the owner's weighting rule is applied later in VERDICT.md); it states what both sides agree on, what stays contested and what would settle it.

## Planned Changes

### Change 1: Run now bypass and a dropped `exit 1` (from Variant 1, Mechanism and facts 5, 6)
- **Source**: Variant 1, fact 5 and fact 6; Round 2 both advocates (conceded by Variant 2, concession 1 and 2)
- **Target**: Base, Cost section (append)
- **Rationale**: C-004 (V1 wins, 67%), U-001 High. Both advocates agree the harm is bounded (one idle session per click; a few at most for a dropped `exit 1`).
- **Integration point**: Replace Cost bullet 2 with the full statement, add the two mitigations offered in Round 2 as suggestions, not facts: a fixed always-exit-1 command, and a "do nothing and stop" prompt.
- **Risk**: Low, additive

### Change 2: What cron has actually been tested for (from Variant 1, fact 2, with Round 2 limits)
- **Source**: Variant 1, fact 2; Round 2 concession 1 (Variant 1)
- **Target**: Base, Cited facts (new fact) and Risk
- **Rationale**: C-006 draw. The tested mechanism (per-minute firing, `orca repo list` and `gh auth status` under an empty environment) is real; the install path is not (cron was `apt install`ed by hand on 2026-11-18 18:40:49, the daemon started by hand at 20:20:37, crontab empty, Coder issue 515 open).
- **Integration point**: new Cited fact after fact 8; one sentence in Risk
- **Risk**: Low

### Change 3: Fix the six-field cron line in the old runbook (from Variant 1, Cost bullet 2)
- **Source**: Variant 1, Cost
- **Target**: Base, Cost (new bullet)
- **Rationale**: C-010, U-004. The line `0 */5 * * * *` in `docs/designs/issue-watcher-setup.md` is six fields; cron 3.0pl1 takes five. Not run here: UNVERIFIED by a test.
- **Integration point**: new bullet; the base's design 4.8 drops cron entirely, so the fix applies only if cron stays
- **Risk**: Low

### Change 4: "Debated and rejected" is not backed (from Variant 1, Risk bullet 2)
- **Source**: Variant 1, Risk
- **Target**: Base, Risk (new bullet)
- **Rationale**: U-005; both advocates and the fault-finder (INV-028) agree. Only requirements line 18 mentions automations; the debate folder covers dispatcher against per-project entries and assumes cron.
- **Integration point**: new Risk bullet, with INV-028's consequence: the written reason must be restated if cron stays
- **Risk**: Low

### Change 5: Repair the base's overbroad sentence (base weakness K4, X-003)
- **Source**: Base fact 6 and Cost bullet 4; Round 2 Variant 2 concession 4
- **Target**: Base fact 6 (replace)
- **Rationale**: "Nothing outside this repo has to change" is false as written: creating the automation is an owner step in Orca (design O3, O4) and no boot script exists. Replacement: no image, package, daemon or per-boot crontab change; one creation step per Orca host, owner-run in the design (N5 binds the orchestrator, not a boot script; a boot script could do `list --json` then `create`, none exists)
- **Integration point**: rewrite of fact 6
- **Risk**: Medium (changes a base claim), supported by the base author's own Round 2 concession

### Change 6: Write the comparison per command (A-001, INV-023)
- **Source**: Diff A-001; invariant INV-023 (HIGH, UNADDRESSED); Round 2 both advocates
- **Target**: Base, new section "Which poll is scheduled"
- **Rationale**: Master and the PR 686 design have `once` with `repos.yaml`; `run-all` with per-repo configs exists only in the unpushed branch `claim-handoff-planb` (`cli.py:432`). The scheduler choice cannot be judged apart from which poll runs. `repos.yaml` does not auto-enrol a new project; `run-all` does (INV-015)
- **Integration point**: new section after Mechanism
- **Risk**: Low

### Change 7: What the scheduler does not decide (INV-024) and other open invariants
- **Source**: invariant-probe.md INV-024, INV-008, INV-011, INV-017, INV-020
- **Target**: Base, new section "What the scheduler choice does not settle"
- **Rationale**: Zero setup (R1, R17) is not decided by cron or automation: issue 515, per-host `superclaude install --force`, the owner-created `Approved` field and issue 516 (`Coordinator` worktree) remain; a sweep can last about 525 s against a 300 s tick; nobody reads a silent scheduler failure; the automation is coupled to the orchestrator checkout path
- **Integration point**: new section
- **Risk**: Low

### Change 8: Debate outcome and the decisive fact
- **Source**: debate-transcript.md Scoring Matrix and Convergence Assessment; Round 2 "What would change my mind"
- **Target**: Base, new closing section "Debate outcome (D02)"
- **Rationale**: record agreed points (15 of 18), unresolved points (C-008, X-003, A-002), the two blocking invariants, both advocates' lean (about 50% and 55%), and the one fact that would settle it: a scheduled `*/5` automation with a `; exit 1` precheck, created `--disabled` then enabled, firing headless on this host for 1 to 24 hours with only `skipped_precheck` rows, no session started and still present after a server restart
- **Integration point**: new final section
- **Risk**: Low

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|------------|-------------------|---------------------------|
| C-001, X-001 | Variant 1 Risk keeps the owner's sentence "an automation starts an agent on each run" as a factual premise | Variant 1 concedes it is true only when the precheck exits 0; the CLI help and installed code agree |
| (Round 1 strength) | "A scheduler that cannot start an agent" as a property of the system | Withdrawn by Variant 1 in Round 2: the poll itself starts agents under both schedulers; only the narrow scheduler-layer claim is kept (Change 1) |
| (Round 1 strength) | "Every tick leaves a plain record" as a cron advantage | Conceded wash in Round 2: cron drops the exit code; outcome lives in the poll's own log and `audit.jsonl` under both |
| (Round 1 strength) | "The scheduler is already tested on this host" | Narrowed in Round 2 to "the mechanism is tested, the install path is not" (Change 2) |
| C-002, X-002 | "An automation is bound to one repo, so cron fits one dispatcher" | Both advocates agree the binding only sets the precheck's working directory; the real question is which poll ships (Change 6) |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|----------|------|------------------|----------|
| 1 | Low | Cost section incomplete | Remove the appended bullet |
| 2 | Low | Cron evidence overstated | Restore base wording |
| 3 | Low | A doc defect goes unmentioned | Remove bullet |
| 4 | Low | Premise stays unquestioned | Remove bullet |
| 5 | Medium | A base claim is softened | Restore fact 6 |
| 6 | Low | Verdict mixes two different polls | Remove section |
| 7 | Low | Scope of the decision unclear | Remove section |
| 8 | Low | No record of the decisive fact | Remove section |

## Review Status
- [x] Auto-approved (default; `--unattended`, no `--interactive`)
- Approved by: auto
- Approval timestamp: 2026-11-20 (time not recorded)
