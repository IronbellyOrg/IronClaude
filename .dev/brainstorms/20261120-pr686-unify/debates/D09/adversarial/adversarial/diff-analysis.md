# Diff Analysis: position paper comparison (D09 watcher writes to GitHub)

## Metadata

- Generated: 2026-11-20
- Variants compared: 2 (variant-1 = OURS, variant-2 = CLAY)
- Total differences found: 20
- Categories: structural (1), content (7), contradictions (3), unique (4), shared assumptions (4 promoted, 1 stated)
- Taxonomy: L1 surface, L2 structural, L3 state-mechanics (each point carries one level tag)
- Analyst note: the analyst checked three claims against the repository (see X-002, A-004). Those checks are cited in the rows.

## Structural Differences

| # | Area | Variant 1 (OURS) | Variant 2 (CLAY) | Severity | Level |
|---|------|------------------|------------------|----------|-------|
| S-001 | Section skeleton | Claim, Mechanism, Cited facts, Costs, Risks, Gets right, "Honest concession" | Same skeleton, closing section is "Weak point conceded" | Low | L1 |

## Content Differences

| # | Topic | Variant 1 (OURS) approach | Variant 2 (CLAY) approach | Severity | Level |
|---|-------|---------------------------|---------------------------|----------|-------|
| C-001 | Value of a mechanical plan check | Useful, but separable: `plan_check(body)` is read-only and can be taken alone | Core of the design: the check is what keeps an empty issue from launching a worker | Medium | L2 |
| C-002 | Who may write the `hold:plan` label | Nobody on the poll side; if ever written, the coordinator under a grant row | The poll, two writes only (add, remove), under the grant `issue.hold` | High | L2 |
| C-003 | Where a hold is shown | `issue-watch status` and the audit log (local) | A GitHub label on the issue, visible to every person | Medium | L2 |
| C-004 | Plan request after one hour | Not accepted as a poll-side timer | Kept: the poll writes one `plan_requests[]` item into the wake file; the coordinator then runs `/sc:issue --plan` | High | L3 |
| C-005 | Lease comment (DQ3) | Not discussed | Written by the orchestrator, not the poll; exists to arbitrate two claimers; conceded to depend on topology (D07) | Medium | L2 |
| C-006 | Staleness and retry of the write path | Search index can be one cycle late; the write path adds a consistency problem | Bounded: failed write is `hold_write_failed`, skipped, retried next cycle; live read confirms a missing label | Medium | L3 |
| C-007 | Is a human approval gate in force | Yes: the `Approved` issue field plus trigger label is the gate, so "ready" is a person's call | No: approval code was deleted by PR 682 and assignment is the only trigger, so the plan check is the only gate | High | L3 |

## Contradictions

| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Impact |
|---|-------------------|--------------------|--------------------|--------|
| X-001 | Whether a human approval gate exists to lean on | Mechanism 1: the owner's gate is a person (requirement R35). Source is the local, unpushed worktree requirements file | Fact 9: "The human approval that OURS leans on is not on master"; PR 682 deleted it | High: both are true for different trees (OURS is local and unpushed, CLAY is master). The spec must say which tree it describes |
| X-002 | Whether the owner's own watcher is read-only on GitHub | Claim: "The poll stays read-only on GitHub ... NG-2 stays as written" | Not claimed by CLAY. Analyst check: the owner's local branch writes a label. `repo_init.py:72` builds `gh label create`, `repo_init.py:116` runs it, `first_run.py:192` calls it, and requirement R11 and R30 say "only the per-repo first run creates labels" (`/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/src/superclaude/cli/issue_watch/`) | High: OURS' absolute framing is wrong against OURS' own unpushed code; the owner already accepts a narrow, once-per-repo label write from an unattended path |
| X-003 | What a repeated write costs | Fact 7: a wrong write "repeats every cycle until noticed" | Risk 1: bounded by retry-next-cycle and the call budget. Analyst note: adding an existing label is idempotent, and the design drops the entry once the check passes (`orchestrator.md:453-454`) | Medium: OURS overstates for an idempotent add; CLAY understates the wrong-issue case |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | OURS | Least-privilege chain: workers never write (WC-9), only the orchestrator writes in `sc-issue-protocol`, completion writes need the issue's grant row (R24); the poll is the only unattended writer if CLAY wins | High |
| U-002 | CLAY | `--dry-run` runs the whole hold step and writes nothing, so a 24-hour shadow run shows holds before any write (`orchestrator.md:461`) | Medium |
| U-003 | CLAY | Switch-on baseline: issues already assigned are never touched, so no label lands on the 17 already-assigned issues (`orchestrator.md:492`) | Medium |
| U-004 | CLAY | `hold:backlog`: a person-set stop label the poll only reads; a hand-removed `hold:plan` is never put back (`orchestrator.md:445-446`) | High |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|-----------|------------------|--------|--------|
| A-001 | "Has a plan" means the three headings Priority, Fix approach and Test plan are filled in (issue 651 format) | Both treat `plan_check` as the readiness test | A thin plan passes the check; the check guards against empty issues only (CLAY design limit (b), `orchestrator.md:494`, not in either paper) | UNSTATED, promoted, L2 |
| A-002 | An issue assigned to the user with no plan is a mistake to hold, and not a deliberate request for a plan to be written | Both discuss holding it; neither asks why a person assigned it | If the person assigned it to get a plan made, a hold delays what they asked for; the one-hour plan request is CLAY's answer | UNSTATED, promoted, L2 |
| A-003 | One writer per repo: two pollers (two workspaces, each with its own cron) never race on one label | Both assume a single poll per repo | Label add and remove are idempotent, but two pollers disagreeing on `hold_removed_by_hand` state could undo each other; the poll store is per workspace | UNSTATED, promoted, L3 |
| A-004 | The cron-run poll's GitHub login can write labels with no extra scope | Both assume a login that can write | Requirement R21 says "`gh` login under cron is not yet tested" (`requirements.md:49`); a read-only poll needs only read scope | UNSTATED, promoted, L2 |
| A-005 | The login `ironbelly` is shared by the owner and the sessions on this host, so a label write does not show who acted | OURS fact 9, CLAY risk 3 | Same for the claim comments already written today | STATED, not promoted |

## Summary

- Total structural differences: 1
- Total content differences: 7
- Total contradictions: 3
- Total unique contributions: 4
- Total shared assumptions surfaced: 5 (UNSTATED: 4, STATED: 1, CONTRADICTED: 0)
- Highest-severity items: C-002, C-004, C-007, X-001, X-002
- Analyst observation (not a diff point): the three GitHub writes the topic names are not all by the poll. The plan request is a wake-file item (no GitHub write). The lease comment is the orchestrator's. The plan body write is the coordinator's, through `/sc:issue --plan` under grant `issue.body.append_plan_sections` (`orchestrator.md:116`, `:480`). The only write the poll itself makes is the label.
