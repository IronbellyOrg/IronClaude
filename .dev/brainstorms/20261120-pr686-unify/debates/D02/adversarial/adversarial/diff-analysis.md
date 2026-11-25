# Diff Analysis: Position-paper Comparison (D02 scheduler: cron or Orca automation)

## Metadata
- Generated: 2026-11-20 (ISO date of this run; time not recorded)
- Variants compared: 2 (Variant 1 = OURS, cron with one dispatcher; Variant 2 = CLAY, Orca automation with a no-agent precheck)
- Variant files: `variant-1-original.md` (886 words), `variant-2-original.md` (824 words)
- Total differences found: 25
- Categories: structural (2), content (10), contradictions (3), unique (10), shared assumptions (3 promoted, 1 stated)

## Structural Differences

| # | Area | Variant 1 (OURS) | Variant 2 (CLAY) | Severity |
|---|------|------------------|------------------|----------|
| S-001 | Section order | Claim, Mechanism, Cited facts (9), Cost, Risk, What OURS gets right | Same six sections in the same order, 9 cited facts | Low |
| S-002 | What the Risk section holds | Risk lists weaknesses of OURS's own written reason and of its own "debated and rejected" statement | Risk lists gaps in documentation and in the host evidence for CLAY's pattern | Low |

## Content Differences

| # | Topic | Variant 1 (OURS) approach | Variant 2 (CLAY) approach | Severity |
|---|-------|---------------------------|---------------------------|----------|
| C-001 | Does an automation start an agent on every run (the owner's stated reason)? | True only when the precheck exits 0; with a non-zero exit the CLI help says the run is skipped; "our argument must not lean on that sentence" (Risk, bullet 1) | False for the precheck pattern; "the owner's objection fails exactly where the precheck exits non-zero" (Claim) | High |
| C-002 | Fit to one dispatcher over many repos (R16) | Cron runs one `run-all` dispatcher that lists repos each tick; "an Orca automation is bound to one `--repo` or `--workspace`" (Mechanism, bullet 3) | One automation, `--workspace` the orchestrator repo, runs `superclaude issue-watch once`; repo list comes from the design's `repos.yaml` (design 4.8) | High |
| C-003 | Dependencies outside this repository | Cron needs Coder issue 515 (install cron, start daemon, per-boot entry); issue is open, so cron runs nowhere today (Cost) | Nothing outside this repo changes: no image, no cron package, no daemon start (fact 6); but creating the automation is an owner step (Cost, bullet 4) | High |
| C-004 | Failure modes that start a model | "Run now" bypasses the precheck and starts a Claude session; an edit mistake or wrong exit code does the same (OURS facts 6, "What OURS gets right") | Acknowledged: "Run now" bypasses the precheck; mitigated by a scheduled shadow run (Cost, bullet 2) | High |
| C-005 | Observability of each tick | Plain process: exit code and log file `~/.aidev/logs/issue-watch.log`; Orca history shows only `skipped_precheck`, so ok and crash look the same (fact 7) | Poll outcome is in `audit.jsonl` and `issue-watch status`; Orca keeps run history and shows the next run (facts 5, 8) | Medium |
| C-006 | Evidence the scheduler works | Cron per-minute test on this host (2026-11-18), `orca repo list` and `gh auth status` under an empty cron environment (facts 2) | Master skill text "VERIFIED 2026-11-03" for the waker automations; waker comments record firings on 2026-11-04 and 2026-11-18 (facts 1, 2) | Medium |
| C-007 | Documentation support | Official docs describe automations as running a prompt through an agent; script-only mode not documented (fact 5) | Precheck gating is documented behaviour (CLI help and official page, fact 4) | Medium |
| C-008 | Survives an image update | Crontab sits outside the persisted home volume and resets; needs a boot step (fact 3) | Orca user data is under `/home/coder/.config/orca` on the persisted home volume, so an automation probably survives; marked UNVERIFIED (fact 6) | Medium |
| C-009 | Known-unverified items | `orca automations list` is empty on this host; U6 and U7 unverified (fact 8) | Same items listed as to-do with a 24-hour `--dry-run` shadow run (fact 7) | Medium |
| C-010 | Cron line syntax in older docs | The runbook FU-2 line is six-field and does not match cron 3.0pl1; the handoff doc already uses five fields (Cost, bullet 2) | Not addressed (design 4.8 drops cron entirely) | Low |

## Contradictions

| # | Point of Conflict | Variant 1 (OURS) Position | Variant 2 (CLAY) Position | Impact |
|---|-------------------|---------------------------|---------------------------|--------|
| X-001 | "An automation starts an agent session on each run" | Quoted as the owner's written reason (requirements line 18, Coder 515 body) and then qualified as true only for exit 0 (Risk, bullet 1) | "The owner's objection fails exactly where the precheck exits non-zero" (Claim); CLI help quote in Mechanism | High (decides whether the stated reason stands; the CLI help text settles the fact for the exit 1 case) |
| X-002 | What an automation is bound to | "Bound to one `--repo` or `--workspace`" (Mechanism, bullet 3) | The bound workspace is the orchestrator repo; the poll reads many repos from `repos.yaml`, so the binding does not limit the poll (design 4.8) | Medium |
| X-003 | Does the automation need manual set-up per host | "Creation is an owner-run step (O3, O4) and N5 forbids the orchestrator to create it" (fact 9) | "Nothing outside this repo has to change" (fact 6) while its own Cost says "Creating the automation is an owner step" | Medium (CLAY paper is partly inconsistent with itself) |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|-----------------|
| U-001 | OURS | "Run now" and `orca automations run` bypass the precheck and start a real Claude session with the unused prompt (CLI help quote) | High |
| U-002 | OURS | Per-tick plain exit code and log; two lock layers (dispatcher lock and per-repo lock) plus `flock -n` | Medium |
| U-003 | OURS | Tested on this host: cron fires, `orca repo list` and `gh auth status` work in cron's empty environment | Medium |
| U-004 | OURS | The old runbook's six-field cron line is wrong for cron 3.0pl1; fix the doc | Low |
| U-005 | OURS | Admission that "debated and rejected" is not backed by the owner's debate folder (only requirements line 18 mentions automations) | Medium |
| U-006 | CLAY | The precheck pattern already ships on master: `SKILL.md:30` (VERIFIED 2026-11-03) and `waker.py` ("the Orca automation's only job") | High |
| U-007 | CLAY | A scheduled `--dry-run` shadow run keeps the first runs off the "Run now" bypass | Medium |
| U-008 | CLAY | No cross-repo dependency on the Coder template (issue 515) for the scheduler itself | Medium |
| U-009 | CLAY | The scheduler is part of the Orca runtime the poll has to reach anyway to wake sessions | Medium |
| U-010 | CLAY | Timeline: Clay asked for an automation on #450 at 2026-11-18 17:00:32, before the owner's reason was written | Low |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|------------|------------------|--------|--------|
| A-001 | The scheduler choice does not change the poll command: the same command can run under cron or under an automation. UNSTATED, and not clearly true: master has only the per-repo `once` poll (PR 686 head is not merged); the dispatcher `run-all` exists only in the unpushed owner branch `claim-handoff-planb` | Both papers treat the scheduler as the only variable | High | UNSTATED, promoted |
| A-002 | Every workspace has its own Orca runtime and needs its own scheduler set-up (a crontab per workspace; an automation per Orca host) | Both papers talk about "every workspace" or "this host" | Medium | UNSTATED, promoted |
| A-003 | A 5-minute tick, 24 hours a day, is the right cadence | Both quote `*/5 * * * *` | Low | UNSTATED, promoted |
| A-004 | `superclaude`, `gh` and `orca` are found from the scheduler's shell | OURS tested cron (fact 2); CLAY lists U6 as partly verified | Medium | STATED in both, not promoted |

## Summary
- Total structural differences: 2
- Total content differences: 10
- Total contradictions: 3
- Total unique contributions: 10
- Total shared assumptions surfaced: 4 (UNSTATED: 3, STATED: 1, CONTRADICTED: 0)
- Highest-severity items: C-001, C-002, C-003, C-004, X-001, A-001
- Taxonomy tags used in the debate: L3 state mechanics: C-004 (guard on exit code), A-001 (command contract); L2 structural: C-002, C-003, X-002, A-002; L1 surface: S-001, S-002, C-010
- Total diff points for convergence: S 2 + C 10 + X 3 + A 3 = 18
