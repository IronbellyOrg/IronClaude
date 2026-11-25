
## Round 2.5: Invariant Probe

Full table in `invariant-probe.md` (28 findings: 11 ADDRESSED, 17 UNADDRESSED; UNADDRESSED HIGH 2, MEDIUM 5, LOW 10). The orchestrator re-checked these facts read-only: `LOOP_CAP_S = 270.0` and `CHILD_TIMEOUT_S = 255.0` in `dispatch.py:52-53` (worktree `claim-handoff-planb`); `run-all` is at `cli.py:432` of that worktree only and appears nowhere under the master snapshot `src/`; the master design `orchestrator.md` has 0 matches for `run-all` or `issue-watch.d` and reads repos from `repos.yaml`; the cron daemon is pid 1169996 started Wed Nov 18 20:20:37 2026.

Blocking items (HIGH and UNADDRESSED):
- INV-023: `run-all` starts `once --config <file>` per repo with per-repo configs, while the PR 686 design reshapes `once` to one config with `orchestrator_repo` and `repos.yaml`. The two polls differ in contract. The verdict must say which poll the scheduler runs.
- INV-024: choosing cron alone does not give zero setup: Coder issue 515 open, a per-host `superclaude install --force`, the owner-created `Approved` org field, and Coder issue 516 (the `Coordinator` worktree) all remain. The scheduler does not decide zero setup.

MEDIUM warnings (do not block): INV-008 (nobody notices a silent scheduler failure under either route), INV-011 (a sweep can take up to about 525 s against a 300 s tick), INV-015 (`once` with `repos.yaml` does not auto-enrol a new project; `run-all` does), INV-017 (the automation is coupled to an orchestrator checkout path that can move), INV-020 (two workspaces for one user have separate locks).

## Scoring Matrix

Winner values: V1 = OURS (cron), V2 = CLAY (automation), Draw = no difference that matters. Confidence is the mean of the two advocates' Round 2 figures where both gave one.

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|-----------------|
| S-001 | Draw | 90% | Same six sections; no effect on the decision. |
| S-002 | Draw | 90% | Both Risk sections are self-critical; no effect. |
| C-001 | V2 | 91% | CLI help: any non-zero precheck exit skips the run; installed code treats crash, timeout and unresolvable workspace as a skip; V1's own Risk concedes. |
| C-002 | V2 (narrow) | 56% | A precheck is any shell command, so an automation can run a dispatcher; but the polls differ in contract (INV-023), so this is a per-command question. |
| C-003 | V2 | 60% | Image has no cron (hand `apt install` 2026-11-18 18:40:49, hand-started daemon, empty crontab, issue 515 open). Offsets: both routes need a new `superclaude` build; automation needs a creation step. |
| C-004 | V1 | 67% | "Run now" and a dropped `exit 1` start a Claude session; cron has neither. Harm bounded (one idle session; a few at most), so the margin is small. |
| C-005 | Draw | 70% | Both advocates concede neither gives a better record of the poll's outcome; Orca keeps only 100 finished rows (about 8 hours 20 minutes). |
| C-006 | Draw | 70% | Cron: mechanism tested here, install path untested. Automation: pattern verified for the waker twice a day on another host, never fired here. |
| C-007 | V1 (narrow) | 55% | Script-only use is undocumented officially; V2 conceded it; the code supports it. |
| C-008 | Unresolved | 50% | V2 65% (profile on the persisted volume, files predate program updates, inferred); V1 did not accept it. Untested either way. |
| C-009 | Draw | 80% | Both list their open unknowns. |
| C-010 | V1 (doc fix) | 85% | The six-field FU-2 line is wrong for cron 3.0pl1 (not run here); both agree it is a doc defect, not a decision factor. |
| X-001 | V2 | 91% | Same evidence as C-001. |
| X-002 | V2 | 67% | The binding gives the precheck its working directory only; it does not limit the shell command. |
| X-003 | Unresolved | 50% | V1 55% (creation is an owner step in design O3, O4), V2 50% (N5 binds the orchestrator, not a boot script; a boot script could do list-then-create; none exists). |
| A-001 | Both: write the verdict per command | 60% | `run-all` is unpushed; `once` is the PR 686 poll. |
| A-002 | Unresolved | 50% | V1 55% cron, V2 55% automation; each route's boot step is unwritten. |
| A-003 | Draw | 60% | Both accept a 5-minute tick; sweep time can exceed it (INV-011). |

## Convergence Assessment
- Points resolved: 15 of 18 (unresolved: C-008, X-003, A-002)
- Alignment: 83.3%
- Threshold: 80%
- Taxonomy coverage: L1 (S-001, S-002, C-010), L2 (C-002, C-003, X-002, A-002), L3 (C-004, A-001): all covered
- Invariant gate: 2 HIGH UNADDRESSED (INV-023, INV-024) block convergence; Round 3 is not available at depth standard
- Status: BLOCKED_BY_INVARIANTS (reported as not converged for the return contract; status partial)
- Overall lean of the two advocates after Round 2: V1 advocate about 50% that cron is the better scheduler; V2 advocate about 55% that the automation is. Both state it is a toss-up and that the owner's recorded decision (R6, R16) stands unless one decisive fact appears: a scheduled `*/5` automation with a `; exit 1` precheck firing headless for 1 to 24 hours with only `skipped_precheck` rows, no session started, and surviving a server restart. That fact cannot be obtained read-only.
