# Disposition: spec panel review 1 of orca-worker-contract-spec.md

Task: task_4917ae1dbd7e (Task 6, revise the spec). Planning only.
Inputs: `.dev/orca-command-refactor/review/spec-panel.md` (17 numbered findings, ledger rows R1-R17) and `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`.
Repo root used: `/home/coder/workspaces/worktrees/IronClaude/exp346-v-ledger` (the brief's root). Spec lines are cited as `spec:N` (new text) or `r1:N` (the review-1 snapshot, `specs/orca-worker-contract-spec.review-ledger/snapshots/r1.md`).

## Summary
- 17 findings verified against the cited sources. All 13 blocking findings (R1-R13) are confirmed and applied to the spec. The 4 minor findings (R14-R17) are confirmed true but rejected for this cycle: the ledger stores them `deferred`, and the reviser contract says "minor (deferred) rows are not answerable" (`~/.claude/commands/sc/spec-panel-ledger.md:264`; `review/spec-panel.md:163`).
- One factual correction to a finding's example: Finding 8 lists `/sc:task`'s confidence-below-0.70 gate as flagless, but `cmd/task.md:93` reads "If confidence <0.70, prompt user: Override with `--compliance [tier]`", so that gate has a flag. The finding still holds for `/sc:recommend` (`cmd/recommend.md:44`) and `/sc:tdd` (`sk/tdd/SKILL.md:52-61`), and the fix names both routes.
- Spec size: 57763 bytes before (sha256 `d3cdbe57...200d`, identical to `snapshots/r1.md`), 66484 bytes after. 12 provisional hunks, each claimed below; no unclaimed hunk. No placeholder is left in the spec: `grep -nE 'TODO|TBD|FIXME|RF_PLACEHOLDER|\{\{|XXX|<!--'` on it printed nothing (rc=1, 2026-11-09).

## Edit placement rule
The review run line carries `--revert-unclaimed` (`review/spec-panel.md:6`), so the ledger's next `begin` restores every hunk no row claims. A claim must change text inside the row's anchor line and may not reach past that line's table row or paragraph (`E-FIXED-NO-EDIT`, `E-CLAIM-WIDE`, `~/.claude/skills/sc-review-ledger/scripts/review_ledger.py:1040-1068`; a zero-width insertion at the line's start or end counts, `review_ledger.py:174-182`). Three anchor pairs sit on adjacent lines (R8 and R2+R4 at `r1:61-62`, R7 and R10 at `r1:64-65`, R3 and R1 at `r1:91-92`); changing both lines of a pair would merge into one hunk that neither row could claim. So in each pair one line is rewritten in place and the other fix is a new table row inserted on the far side of its anchor line:
- WC-3 rewritten in place (R8); WC-4 left as is and followed by the new row WC-4a (R2, R4).
- WC-6 rewritten in place (R7); WC-7 left as is and followed by the new row WC-7a (R10).
- workflow row rewritten in place (R1); a new row "troubleshoot as run by `/sc:task` (TFEP)" inserted just above the troubleshoot row (R3).

The WC-4a insertion sits at the start of WC-5's line, which is minor row R14's span, so the ledger's `minor_touched` metric will count one touch; WC-5's text is unchanged.

## Disposition table
"Verified" means this session re-read the finding's evidence on 2026-11-09. Hunk numbers are the provisional hunks `status` printed after the edits.

| Finding (row) | Verified | Disposition | Where (new spec line; hunk) | What changed |
|---|---|---|---|---|
| 1 (R1) workflow cannot meet WC-4 | Confirmed: `--output` retired (`sk/sc-workflow-protocol/SKILL.md:24`), no yaml on a pre-creation STOP (`SKILL.md:26`), generated package id (`SKILL.md:44`), `refs/return-contract.md:39` ("chat only — no package directory, no yaml") | **Applied** | workflow row, `spec:95`; hunk 8 | Adds a `--report-dir <dir>` flag (P1); under `--unattended` the WC-4 report is `<report-dir>/worker-contract.yaml`, known before dispatch and written on every outcome, pre-creation STOPs included, with `status: failed` and the STOP code; the package and its own contract stay as today. |
| 2 (R2) fixed status set vs "keep their fields" | Confirmed: `status: success` in `sk/sc-workflow-protocol/refs/return-contract.md:7`, `sk/sc-brainstorm-protocol/SKILL.md:341`, `sk/sc-adversarial-protocol/SKILL.md:436`, `sk/sc-reflect-protocol/SKILL.md:665`; readers that need `success`: `sk/sc-implement-protocol/refs/managed-workspace.md:10`, `sk/sc-reflect-protocol/refs/remediation-handoff.md:75`, `sk/sc-auggie-review-protocol/refs/remediation-handoff.md:77` | **Applied** | new row WC-4a, `spec:63`; hunk 2 | A command that already writes `return-contract.yaml` keeps it byte-for-byte; its WC-4 report is a separate `worker-contract.yaml`, so 7.2 step 4's four-value assertion holds and no existing reader breaks. WC-4a states that it replaces WC-4's "keep their fields" sentence. |
| 3 (R3) troubleshoot TFEP file at the WC-4 path | Confirmed: `sk/sc-troubleshoot-protocol/SKILL.md:560` writes `<output-dir>/return-contract.yaml` (7-field TFEP schema) when `caller=task-unified`; `sk/sc-task-protocol/SKILL.md:216,220` invokes troubleshoot with `--output-dir {output_dir}` and reads that file | **Applied** | new row "troubleshoot as run by `/sc:task` (TFEP)", `spec:93`; hunk 7 (with WC-4a) | The TFEP file stays as today for `/sc:task`; troubleshoot's WC-4 report is `<output-dir>/worker-contract.yaml`; `/sc:task` gives TFEP a directory other than its own WC-4 directory; only the task worker reports to Orca. |
| 4 (R4) `<output-dir>` undefined for `--output <file>` | Confirmed: `cmd/tdd.md:49` ("Output path for the final TDD document"), `cmd/init-lite.md:32` ("Report output path"); spec AC-2.2 example `r1:200` | **Applied** | new row WC-4a, `spec:63`; hunk 2 | A file output flag gives `<file>.return-contract.yaml` beside the file; a directory flag gives `<dir>/return-contract.yaml`; a command with no output flag uses the report flag its section 3 row names. |
| 5 (R5) adversarial path vs WC-4 path | Confirmed: `r1:83` vs `r1:62`; the skill names no contract file (`INV-A:60`, `sk/sc-adversarial-protocol/SKILL.md:427-445`) | **Applied** | adversarial row, `spec:85`; hunk 6 | The existing contract is fixed at `<output>/adversarial/return-contract.yaml` for its readers; the WC-4 report is the separate `<output>/worker-contract.yaml`, the path 7.2 step 3 checks. |
| 6 (R6) AC-0.4 cannot pass in P0 | Confirmed: step 3 (`r1:182`) needs the WC-4 path and status; AC-0.4 (`r1:194`) exempts only step 4; phases wait on earlier checks (`r1:154`) | **Applied** | AC-0.4, `spec:197`; hunk 12 | In P0 every 7.2 reference to the WC-4 report uses the command's existing report file; step 3's pass condition is restated for that file; step 4 is not run in P0. Also carries the R10 Skill-call check and the R11 heartbeat-gap record. |
| 7 (R7) WC-6 fresh dir vs retry | Confirmed: retry is `worker-start --task <task_id> --retry-of <dispatch_id>` on the same Task (`inventory/orca-capabilities.md:116`); brief reuse is UNVERIFIED (see below) | **Applied** | WC-6, `spec:65`; hunk 3 | A re-run stays at the same path; at start it overwrites any earlier WC-4 report with `status: failed` ("attempt started, not finished"); the final report lists only this attempt's files; "fresh dir" in section 3 now means this; the coordinator moves an earlier attempt aside if it wants it kept. |
| 8 (R8) WC-3 answer-as-flag route | Confirmed for recommend (`cmd/recommend.md:44`) and tdd (`sk/tdd/SKILL.md:52-61`); not for task, whose gate names `--compliance [tier]` (`cmd/task.md:93`) | **Applied** | WC-3, `spec:61`; hunk 1 | The answer goes in through the gate's flag when one exists, otherwise folded into the command's main input; person-only gates are not asked and end blocked; the re-run keeps the brief's output flag, so the report path does not change. |
| 9 (R9) `--unattended` no-op on gated commands in P1 | Confirmed: `cmd/auggie-review.md:51` (`--post-pr` default true on a PR, "No confirmation prompt"); P1 scope `r1:159`; auggie-review converts in P2 (`r1:160`) | **Applied** | P1 row, `spec:162`; hunk 9 | Until its own phase, a command whose gates or outward defaults convert in P2-P4 does nothing under `--unattended` except write a `status: blocked` report naming that phase. |
| 10 (R10) Skill call not required | Confirmed: `CLAUDE.md:11`; `r1:65`, `r1:184` and `r1:194` check only for no wrapper and no `AskUserQuestion` | **Applied** | new row WC-7a, `spec:67`; hunk 4; check added in AC-0.4, `spec:197` (hunk 12) | The worker's first command step is the Skill tool call for the command's skill; improvising from the file does not meet WC-7; AC-0.4 checks the transcript for it. |
| 11 (R11) subagent calls and the 300 s boundary | Confirmed: `r1:68` names only poll and eval waits and allows a 300 s call; `~/.claude/commands/sc/spec-panel-ledger.md:261` treats heartbeating through a long subagent run as unproven | **Applied** | WC-10, `spec:70`; hunk 5; record added in AC-0.4, `spec:197` (hunk 12) | No single tool call of 4 minutes or more; subagent heartbeating marked UNVERIFIED and recorded in AC-0.4; until proven, the coordinator judges liveness by `worker-list` `projection.liveness` and `worker-show` (`inventory/orca-capabilities.md:123`), not by heartbeat age alone. |
| 12 (R12) 7.2 step 6 and shared worktree state | Confirmed: workers share the worktree by default (`inventory/orca-capabilities.md:115`); this checkout shows `?? .dev/orca-command-refactor/` before any worker ran (`git status --short`, 2026-11-09); workflow stages files (`sk/sc-workflow-protocol/SKILL.md:28`) | **Applied** | 7.2 step 6, `spec:188`; hunk 11 | Step 6 compares `git status --short --untracked-files=all` before and after and passes paths under the output directory or named in this or a concurrent worker's report; two workers that stage files never share a worktree at the same time. |
| 13 (R13) `^-[^-]` misses deleted bullets | Confirmed by test in a scratch repo (2026-11-09): deleting `- item two` gave no output from `git diff -U0 ... \| grep -E '^-[^-]'` (rc=1) while `git diff --numstat` printed `1 1 f.md` | **Applied** | AC-C5, `spec:179`; hunk 10 | The test is now "`git diff --numstat` deleted count is 0"; AC-C5 states AC-0.3 uses the same test in place of its grep (see Gaps). |
| 14 (R14) WC-5 "verdict" with no WC-4 field | Confirmed: `r1:63` names a verdict; WC-4 `r1:62` has no verdict field | **Rejected** | none | Minor row stored `deferred`; not answerable this cycle (`~/.claude/commands/sc/spec-panel-ledger.md:264`; ledger tail `review/spec-panel.md:155,163`). |
| 15 (R15) WC-1 has no phase or check | Confirmed: owner "Launch setup, not commands" (`r1:59`); no phase scope names it (`r1:158-162`) | **Rejected** | none | Minor row stored `deferred`; not answerable (same citations as R14; tail `review/spec-panel.md:156`). |
| 16 (R16) stated repo root does not exist | Confirmed: `ls -d /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs` failed (2026-11-09); repo-relative paths resolve here | **Rejected** | none | Minor row stored `deferred`; not answerable (tail `review/spec-panel.md:157`). The header line `spec:4` is unchanged. |
| 17 (R17) table-escaped `\|` in checks | Not re-tested this session; taken from the review's own test (`review/spec-panel.md:92`) | **Rejected** | none | Minor row stored `deferred`; not answerable (tail `review/spec-panel.md:158`). Note: the new AC-C5 text uses no pipe in its command. |

## Gaps (text a fix needed but the ledger would revert)
These lines sit outside every blocking row's span, so an edit there would be unclaimed and restored by `begin --revert-unclaimed`. Each is left unchanged and overridden by claimed text; they are also passed to the ledger as `gaps` below so review 2 sees them.
1. `spec:78` (section 3 lead-in) still glosses "Contract" as "`<output-dir>/return-contract.yaml`". WC-4a (`spec:63`) now says that wherever the spec says "the contract", it means the WC-4a path. (R2, R4)
2. `spec:264` (Decisions row "Report shape") still says the report reuses `return-contract.yaml`. True for commands without an existing contract; WC-4a adds `worker-contract.yaml` for the five that have one. (R2)
3. `spec:196` (AC-0.3) still shows the `grep -E '^-[^-]'` test. AC-C5 (`spec:179`) states AC-0.3 uses the `--numstat` deleted-count test instead. (R13)
4. `spec:187` (7.2 step 5) still checks only for `AskUserQuestion`. The Skill-call check lives in WC-7a (`spec:67`) and AC-0.4 (`spec:197`), so P0 checks it; P1-P4 live checks reach it only through WC-7a. (R10)
5. Section 7.3 has no heartbeat-gap check outside AC-0.4 and AC-4.3. WC-10 (`spec:70`) now gives the coordinator a liveness rule that does not depend on the gap being proven. (R11)
6. WC-11 (`spec:71`) still covers output files only; the shared git-staging rule sits in 7.2 step 6 (`spec:188`). (R12)
7. AC-1.4 (`spec:201`) checks that the workflow return-contract ref "states the contract is written for pre-creation STOPs". Under the R1 fix that is the WC-4 report `worker-contract.yaml` in `--report-dir`, not the package contract, which still writes no yaml on such a STOP. (R1)

## Decisions
| Decision | Options considered | Rationale |
|---|---|---|
| Minor findings R14-R17 | Fix them now; leave them | Left: the ledger stores them `deferred` and the reviser contract makes them not answerable; any edit on their lines would be unclaimed and reverted. |
| How to fix the status clash (R2) and the TFEP path clash (R3) | Rename existing `status: success` values; widen 7.2 step 4's value set; a separate WC-4 file for commands that already write `return-contract.yaml` | Separate file `worker-contract.yaml`: renaming breaks the readers at `managed-workspace.md:10`, `remediation-handoff.md:75,77` and the TFEP reader; step 4 is outside every row's span, so it cannot change this cycle. One rule then fixes R2, R3 and R5 together. |
| Contract path for a file-valued `--output` (R4) | The file's directory plus `return-contract.yaml`; `<file>.return-contract.yaml` | `<file>.return-contract.yaml`: two runs writing different files in one directory would otherwise share one report (the WC-11 clash). The name still contains `return-contract.yaml`, so AC-1.1 and AC-1.3 greps still match. |
| Where workflow's report goes (R1) | Accept the package path learned after the run; add a report-only flag | Add `--report-dir`: WC-4 requires the path before dispatch, and `--output` is retired. The flag sets only the WC-4 report's location; the package is unchanged. |
| Retry behaviour (R7) | A new directory per attempt; same path with a stale-report guard | Same path: the brief, and so the output flag, are shared by every attempt of a Task; the "attempt started" report stops a crashed retry from leaving an old success in place. |
| Gated commands between P1 and their phase (R9) | No-op; refuse with a `blocked` report | Refuse with a `blocked` report: a no-op lets outward defaults run (auggie-review posting), and a `blocked` report still meets AC-1.1's `## Unattended mode` section and WC-4. |
| Heartbeat through subagent calls (R11) | Ban long subagent fan-out in workers; require background subagents; measure it and give the coordinator a rule meanwhile | Measure and give a rule: whether a subagent call blocks heartbeats is UNVERIFIED, so a ban or a harness-specific requirement would rest on an unproven premise. |
| Placement of adjacent-row fixes | See "Edit placement rule" | Forced by the ledger's claim-width check; the chosen side keeps the two core rows (WC-4 is untouched and refined by WC-4a; workflow is rewritten in place). |

## UNVERIFIED items
1. Whether a `--retry-of` worker receives the identical Task brief text (R7 assumes it does; `inventory/orca-capabilities.md:116` shows only the same `--task <task_id>`).
2. Whether an Agent-tool subagent call in a dispatched Claude worker stops the top-level session from heartbeating (R11); now stated as UNVERIFIED in WC-10 and recorded by AC-0.4.
3. Where `/sc:task` defines the TFEP `{output_dir}`: `sk/sc-task-protocol/SKILL.md:206,216,220` use it, and its definition was not found near them. The new TFEP row requires it to differ from the task worker's own WC-4 directory.
4. Finding 17's raw-copy test was not re-run in this session.

## Ledger input
`answer` claims for the coordinator's ledger step, one per blocking row, against the 12 provisional hunks. Checked with `answer --input review/disposition.md --dry-run`; the result is recorded below the block.

```ledger-input
{
  "claims": [
    {"row": "R1", "action": "fixed", "hunks": [8], "reason": "workflow row: --report-dir; WC-4 report <report-dir>/worker-contract.yaml on every outcome incl. pre-creation STOP"},
    {"row": "R2", "action": "fixed", "hunks": [2], "reason": "WC-4a: existing return-contract.yaml kept as is; WC-4 report is a separate worker-contract.yaml"},
    {"row": "R3", "action": "fixed", "hunks": [7], "reason": "TFEP row: TFEP file unchanged; troubleshoot WC-4 report is <output-dir>/worker-contract.yaml"},
    {"row": "R4", "action": "fixed", "hunks": [2], "reason": "WC-4a: file-valued --output gives <file>.return-contract.yaml"},
    {"row": "R5", "action": "fixed", "hunks": [6], "reason": "adversarial row: existing contract fixed path; WC-4 report <output>/worker-contract.yaml, the path 7.2 step 3 checks"},
    {"row": "R6", "action": "fixed", "hunks": [12], "reason": "AC-0.4: P0 uses the existing report wherever 7.2 names the WC-4 report; step 3 restated; step 4 not run"},
    {"row": "R7", "action": "fixed", "hunks": [3], "reason": "WC-6: same-path re-run with stale-report guard; fresh dir redefined"},
    {"row": "R8", "action": "fixed", "hunks": [1], "reason": "WC-3: flag or folded-into-input answer route; person-only gates end blocked; report path unchanged"},
    {"row": "R9", "action": "fixed", "hunks": [9], "reason": "P1: gated commands write a blocked report until their phase"},
    {"row": "R10", "action": "fixed", "hunks": [4], "reason": "WC-7a: Skill tool call required; checked in AC-0.4"},
    {"row": "R11", "action": "fixed", "hunks": [5], "reason": "WC-10: no call of 4 min or more; subagent heartbeat UNVERIFIED and recorded; coordinator liveness rule"},
    {"row": "R12", "action": "fixed", "hunks": [11], "reason": "7.2 step 6: before/after comparison; staging workers never share a worktree"},
    {"row": "R13", "action": "fixed", "hunks": [10], "reason": "AC-C5: git diff --numstat deleted count 0, also for AC-0.3"}
  ],
  "gaps": [
    {"text": "R2/R4: section 3 lead-in (spec:78) still glosses Contract as <output-dir>/return-contract.yaml; WC-4a overrides it."},
    {"text": "R2: Decisions row 'Report shape' (spec:264) still says reuse return-contract.yaml; WC-4a adds worker-contract.yaml for commands with an existing contract."},
    {"text": "R13: AC-0.3 (spec:196) still shows grep -E '^-[^-]'; AC-C5 says AC-0.3 uses the --numstat test instead."},
    {"text": "R10: 7.2 step 5 (spec:187) checks only AskUserQuestion; the Skill-call check is in WC-7a and AC-0.4."},
    {"text": "R11: no heartbeat-gap check outside AC-0.4 and AC-4.3; WC-10 gives a coordinator liveness rule meanwhile."},
    {"text": "R12: WC-11 (spec:71) still covers output files only; the git-staging rule is in 7.2 step 6."},
    {"text": "R1: AC-1.4 (spec:201) wording about the workflow contract on pre-creation STOPs now means the WC-4 worker-contract.yaml in --report-dir."}
  ]
}
```

Dry-run result (2026-11-09): `answer --input .dev/orca-command-refactor/review/disposition.md --dry-run` returned `ok: true`, 13 claims accepted (one per blocking row, hunks 1-12, R2 and R4 sharing hunk 2), 7 gap entries, `would_write: inputs/c1-answers-4.json`. Every ledger write (`answer`, then `begin --doc <spec> --revert-unclaimed`) belongs to the coordinator's ledger step; this session ran only `status` and `--dry-run`. The independent check of these fixes is review 2 of 3.
