# Spec panel review: orca-worker-contract-spec.md

review: 1 of 3 (ledger phase `find`; the line is copied from the script's `status` output, `review_header`)

Task: task_5cd98936d719 (Task 5, independent review). Planning only.
Command: `/sc:spec-panel-ledger --ledger .dev/orca-command-refactor/specs/orca-worker-contract-spec.review-ledger --revert-unclaimed @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
Document reviewed: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (57763 bytes, sha256 `d3cdbe57...200d`, byte-identical to `snapshots/r1.md`).

## Verdict
**FAIL.** There are 13 blocking findings (all MAJOR with a concrete wrong outcome, three of them from FR-8 boundary-table gaps) and 4 minor notes. The architecture decision in section 1 holds up. The failures sit in the worker contract's report-file rule (WC-4) and its neighbours (WC-3, WC-6, WC-7, WC-10, WC-11), and in acceptance checks that cannot pass or that pass for the wrong reason (AC-0.4, 7.2 step 6, AC-C5). The `find --dry-run` preview agrees: `rows: 17, blocking: 13, deferred: 4`. The binding loop decision is the script's `close` verdict, which the coordinator's ledger step appends below.

## Panel and method
- Mode: critique, a single review (the ledger loop runs one review per session and writes no improved spec). Focus: requirements (Wiegers lead, Adzic, Cockburn) and architecture (Fowler lead, Newman, Hohpe, Nygard), plus Whittaker, who sits on every panel.
- Ledger: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.review-ledger/ledger.json` read on 2026-11-08 showed `phase: find`, `round: 1`, `rows: []`; `status` printed `review_header: "review: 1 of 3"` and `snapshots_intact: true`; `cmp` showed `snapshots/r1.md` is byte-identical to the spec. This session ran only `status` and `find --dry-run`; every ledger write belongs to the coordinator's ledger step.
- Repo root used: `/home/coder/workspaces/worktrees/IronClaude/exp346-v-ledger` (the brief's root). Every citation below was read in this checkout on 2026-11-08 with Read, `grep -n` or `sed -n`. Spec lines are cited as `spec:N`.
- Stance: adversarial. For each requirement the panel asked: can a coordinator or implementer follow this text exactly and still get a wrong result? Findings that change only wording or formatting are graded MINOR.

## === REQUIREMENTS ANALYSIS ===
**Wiegers (requirements quality).** The contract table (`spec:57-70`) has an owner and evidence for each rule, which is good. But its core rule, WC-4, is not satisfiable for several commands the spec itself marks "ready today":
- WC-4 says the report path is `<output-dir>/return-contract.yaml`, "where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)" (`spec:62`). `/sc:workflow` has retired `--output`: "Validate all input and flags first (`--output` is retired → `E-LEGACY`)" (`src/superclaude/skills/sc-workflow-protocol/SKILL.md:24`). Its package name is generated with a timestamp (`SKILL.md:44`, example `TASK-WF-authLogin-20261001-063000.md`). It also deliberately writes "No package, no plan file, no yaml on a pre-creation STOP" (`SKILL.md:26`). Yet the spec lists workflow as ready, needing only "Write the contract for pre-creation STOPs too" (`spec:92`), and names no location for that file. Finding 1.
- `/sc:tdd` and `/sc:init-lite` take `--output <file>` (`spec:87`, `spec:90`; `src/superclaude/commands/tdd.md:49`: "Output path for the final TDD document"). WC-4 defines `<output-dir>` only as a directory, so the contract path for `--output docs/TDD.md` is undefined. The spec's own gate test uses exactly this case: `/sc:tdd "auth" --unattended --output <file>` (`spec:200`). Finding 4.
- WC-4 fixes `status` to `succeeded | partial | failed | blocked` and says "Commands that already write a contract keep their fields and add the missing ones" (`spec:62`). The existing contracts use the same key with other values: workflow `status: success | partial | failed` (`src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md:7`), brainstorm `success | partial | failed | dry-run` (`src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:341`), troubleshoot TFEP `success|partial|blocked|failed` (`src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:560`). Keeping the field fails the 7.2 step 4 assertion (`spec:183`, `assert d['status'] in {'succeeded',...}`); renaming the value breaks the existing readers. Finding 2.

**Adzic (examples and testability).** Several acceptance checks fail or pass for the wrong reason when run exactly as written:
- AC-0.4 requires steps 1-3 to pass in P0 and exempts only step 4 "since the contract arrives in P1" (`spec:194`). Step 3's pass condition is "its report path is the WC-4 contract path" and "its `--outcome` matches the contract's `status`" (`spec:182`). No WC-4 contract exists in P0, so step 3 cannot pass, and "Later phases do not start until the earlier phase's checks in section 7 pass" (`spec:154`) blocks the whole rollout. Finding 6.
- 7.2 step 6 passes only when "only files under the brief's output directory (and the command's documented artifacts) appear" in `git status --short` (`spec:185`). Workers share the worktree by default (`CAPS:115`), WC-11 explicitly allows two workers in one worktree (`spec:69`), and AC-3.4 runs two (`spec:207`). Any other worker's or person's file makes step 6 fail. In this checkout `git status --short` already shows `?? .dev/orca-command-refactor/` before any worker runs. Finding 12.
- AC-C5 and AC-0.3 treat `grep -E '^-[^-]'` printing nothing as proof that edits are additive (`spec:176`, `spec:193`). A deleted Markdown bullet `- item` appears in the diff as `-- item`, which that pattern does not match: piping `-- removed bullet` through `grep -E "^-[^-]"` printed nothing (NO_MATCH, run 2026-11-08). Command files are mostly bullets, so deletions pass as "additive". Finding 13.

**Cockburn (actors and goals).** The primary actor is the coordinator and its goal is "dispatch, then read one known file". WC-3 lets the worker get an answer from the coordinator and then "re-invoke or resume the command with the answer as a flag" (`spec:61`). For many gates no such flag exists: recommend's "one clarifying question" (`spec:115`), tdd's topic clarification (`spec:90`), task's confidence below 0.70 (`spec:121`). The spec does not say how the answer gets back in. A re-invoked command that writes to a "fresh dir" (WC-6, `spec:64`) also changes the report path the coordinator recorded before dispatch (WC-4). Finding 8.

## === ARCHITECTURE ANALYSIS ===
**Fowler (interfaces).** The decision in section 1 (coordinator above, commands as units, no Orca calls in commands) is sound and well evidenced: `grep -rlni orca` over `src/superclaude/{commands,skills,core,agents,hooks}` lists only `src/superclaude/skills/ccsession-tag/*` (run 2026-11-08), and AC-C1 prints nothing today. The weak point is the one shared interface, the report file:
- Two different paths for one command: WC-4 says `<output-dir>/return-contract.yaml` (`spec:62`), and the adversarial fix says "Fix the contract filename to `<output>/adversarial/return-contract.yaml`" (`spec:83`). 7.2 step 3 checks against the WC-4 path (`spec:182`), so AC-1.2 fails for adversarial whichever one is built. Finding 5.
- One filename, two schemas: troubleshoot already writes `<output-dir>/return-contract.yaml` with the 7-field TFEP schema when `caller=task-unified` (`src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:560`). WC-4 would write a different schema to the same path under `--unattended`. The troubleshoot row (`spec:91`) and the task row (`spec:121`) do not resolve which one wins when `/sc:task --unattended` runs troubleshoot through TFEP. Finding 3.

**Newman (evolution and rollout).** P1 makes "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)" (`spec:159`), and AC-1.1 requires the `## Unattended mode` section on every 3.1 and 3.2 command in P1 (`spec:195`). Gates are only converted in P2 to P4 (`spec:160-162`). The spec does not say what `--unattended` does on a gated command between P1 and its gate phase. A coordinator following `WORKER-CONTRACT.md` (written in P0, `spec:158`) relies on WC-9. But `/sc:auggie-review` posts by default, "No confirmation prompt" (`src/superclaude/commands/auggie-review.md:51`), so `--unattended` in P1 still posts to the PR. Finding 9.

**Hohpe (message flow).** Retry breaks the "known before dispatch" guarantee. A retry is `worker-start --task <task_id> --retry-of <dispatch_id>` on the same Task (`CAPS:116`), so it gets the same brief and the same `--output`. WC-6 then requires "fresh output directory so a re-run starts clean" (`spec:64`). Either the retry writes into the first attempt's directory (the corruption WC-6 forbids), or the command picks a new directory the coordinator never saw. Finding 7.

**Nygard (failure modes).** Two liveness and safety gaps:
- WC-10 splits only Bash waits: "A command step that blocks a single tool call for longer than 5 minutes (a poll wait, a long eval)" (`spec:68`). WC-7 keeps every command's Agent-tool fan-out (`spec:65`), and tdd, adversarial and troubleshoot Tier 2 run subagents. The repo's own ledger command treats heartbeating through a subagent run of more than 5 minutes as unproven until "a recorded smoke check showed that a dispatched worker can spawn an Agent-tool subagent and keep sending its 5-minute heartbeat through a subagent run longer than 5 minutes" (`~/.claude/commands/sc/spec-panel-ledger.md:261`). No acceptance check covers it except AC-4.3, which is for pr-submit only (`spec:210`). Finding 11.
- WC-7 forbids an Agent-tool wrapper but does not require the Skill tool call. The repo rule is "you MUST invoke the corresponding skill via the Skill tool BEFORE generating any other output" (`CLAUDE.md:11`). 7.2 step 5 checks only for `AskUserQuestion` (`spec:184`), and AC-0.4 checks only for "no Agent-tool wrapper" (`spec:194`). A worker that reads the command file and improvises the protocol passes every check. Finding 10.
- Shared-worktree git state: `/sc:workflow` requires `git add .dev/tasks` (`src/superclaude/skills/sc-workflow-protocol/SKILL.md:28`). WC-11 covers output files only (`spec:69`), so two workers in one worktree can collide on the git index lock. This is folded into Finding 12 because it is the same root cause: the contract ignores state that workers share.

## === ADVERSARIAL ANALYSIS (Whittaker) ===
- **Sequence attack (retry).** I can break this spec by repeating a step. The invariant at WC-6 (`spec:64`) fails when the coordinator retries a failed Task. Concrete attack: Task T brief has `--output .dev/x/`; attempt 1 writes `.dev/x/REPORT.md` and fails. The retry (`CAPS:116`, same Task, same brief) runs again with `--output .dev/x/`. Before: `.dev/x/` holds attempt 1's files. After: attempt 2 overwrites or mixes them, or the command chooses `.dev/x-2/`, which the coordinator never recorded. (Finding 7)
- **Sequence attack (phase order).** The invariant "`--unattended` means no outward default" (WC-9, `spec:67`) fails between P1 and P2. Concrete attack: P1 done; the coordinator dispatches `/sc:auggie-review 412 --unattended --output-dir .dev/r/`. Before: PR 412 has 0 reviews. After: 1 review comment posted, because the gate conversion for auggie-review is P2 (`spec:160`) and its default posts (`src/superclaude/commands/auggie-review.md:51`). (Finding 9)
- **Zero/empty attack.** The invariant "contract written on every outcome, including stops before any other output exists" (WC-4, `spec:62`) fails for workflow's pre-creation STOP. Before: no package exists (`SKILL.md:26`). After: WC-4 requires a file at `<output-dir>/return-contract.yaml`, but workflow has no output dir and refuses `--output` (`SKILL.md:24`). (Finding 1)
- **Sentinel collision attack.** The filename `return-contract.yaml` is a sentinel that the coordinator reads as "the WC-4 report". It collides with troubleshoot's TFEP file at the same path (`src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:560`), and the `status` value `success` collides with WC-4's `succeeded`. (Findings 2 and 3)
- **Divergence attack.** In the AC-C5 regex `^-[^-]` (`spec:176`), the branch between "deletion" and "diff header" sits on the second character. A deleted line whose content starts with `-` (every bullet) falls on the header side and is silently ignored. (Finding 13)
- **Accumulation attack.** WC-10 (`spec:68`) bounds Bash waits at 4 minutes but places no bound on one Agent-tool call. A tdd heavyweight run with parallel research subagents can block the top-level session longer than the 5-minute heartbeat cadence; no check counts heartbeat gaps outside AC-4.3. (Finding 11)

## Guard Condition Boundary Table
Two guards in the spec decide a branch from a value: WC-5's report status to Orca outcome mapping (`spec:63`) and WC-10's wait-size rule (`spec:68`). Every GAP row maps to a numbered finding (FR-8: MAJOR at least).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| status→outcome | WC-5 `spec:63` | Zero/Empty | no contract file | failed | "`--outcome failed` when ... no report exists" | OK |
| status→outcome | WC-5 `spec:63` | One/Minimal | `status: blocked` | failed | `failed` for `blocked` | OK |
| status→outcome | WC-5 `spec:63` | Typical | `status: succeeded` | succeeded | `succeeded` | OK |
| status→outcome | WC-5 `spec:63` | Maximum/Overflow | two `return-contract.yaml` writers at one path (troubleshoot TFEP and WC-4) | undefined | unspecified | GAP (Finding 3) |
| status→outcome | WC-5 `spec:63` | Sentinel Value Match | `status: success` (existing workflow and brainstorm value) | undefined | WC-4 keeps old fields; 7.2 step 4 rejects the value | GAP (Finding 2) |
| status→outcome | WC-5 `spec:63` | Legitimate Edge Case | `status: partial` | succeeded | `succeeded` "including `partial`" | OK |
| wait split | WC-10 `spec:68` | Zero/Empty | 0 s tool call | no split | nothing required | OK |
| wait split | WC-10 `spec:68` | One/Minimal | 1 s poll | no split | nothing required | OK |
| wait split | WC-10 `spec:68` | Typical | 240 s poll-then-sleep iteration | no split | allowed (at most 4 minutes) | OK |
| wait split | WC-10 `spec:68` | Maximum/Overflow | 3600 s eval (`spec:68` cites eval timeouts up to 3600 s) | split | split into waits of at most 4 minutes | OK |
| wait split | WC-10 `spec:68` | Sentinel Value Match | exactly 300 s single call | no split ("longer than 5 minutes") | heartbeat gap can exceed 5 minutes; not addressed | GAP (Finding 11) |
| wait split | WC-10 `spec:68` | Legitimate Edge Case | one Agent-tool subagent call over 5 minutes | not covered (WC-10 names only poll and eval waits) | unspecified | GAP (Finding 11) |

## Numbered findings
Severity uses the panel scale. Blocking follows the ledger's `spec-panel` profile: CRITICAL, rule FR-8 or FR-9, or MAJOR with a concrete wrong outcome. MINOR findings are notes and never fail the review.

| # | Finding | Severity | Blocking | Spec section | Evidence (path:line) |
|---|---|---|---|---|---|
| 1 | `/sc:workflow` cannot meet WC-4: it refuses `--output` (`E-LEGACY`), names its package with a generated timestamp id, and deliberately writes no yaml on a pre-creation STOP. The spec still lists it as ready, with a P1 fix that names no location for the file. | MAJOR | yes | 3.1 (workflow row), 2.2 WC-4 | `spec:62`, `spec:92`; `src/superclaude/skills/sc-workflow-protocol/SKILL.md:24,26,44`; `src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md:3` |
| 2 | WC-4's fixed status set (`succeeded`) conflicts with "keep their fields": existing contracts use `status: success`. 7.2 step 4 then rejects every existing workflow and brainstorm contract, or renaming the value breaks their readers. | MAJOR | yes (FR-8 GAP) | 2.2 WC-4, 7.2 step 4 | `spec:62`, `spec:183`; `src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md:7`; `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:341` |
| 3 | Troubleshoot already writes `<output-dir>/return-contract.yaml` with the TFEP schema when `caller=task-unified`. WC-4 puts a second schema at the same path, and nothing says which one wins under `/sc:task --unattended`. | MAJOR | yes (FR-8 GAP) | 3.1 (troubleshoot row), 3.2 (task row), WC-4 | `spec:62`, `spec:91`, `spec:121`; `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:560` |
| 4 | WC-4 defines `<output-dir>` only as a directory, but tdd and init-lite take `--output <file>`, so their contract path is undefined. The spec's own gate test uses `/sc:tdd ... --output <file>`. | MAJOR | yes | 2.2 WC-4, 3.1 (tdd, init-lite), AC-2.2 | `spec:62`, `spec:87`, `spec:90`, `spec:200`; `src/superclaude/commands/tdd.md:49` |
| 5 | The adversarial fix path `<output>/adversarial/return-contract.yaml` contradicts WC-4's `<output-dir>/return-contract.yaml`, and 7.2 step 3 checks the WC-4 path, so AC-1.2 fails for adversarial whichever path is built. | MAJOR | yes | 3.1 (adversarial row), WC-4, 7.2 step 3 | `spec:62`, `spec:83`, `spec:182` |
| 6 | AC-0.4 cannot pass in P0. It exempts only step 4, but step 3 requires the WC-4 contract path and status, and the contract arrives in P1. Since later phases wait on earlier checks, the rollout cannot start. | MAJOR | yes | 7.3 AC-0.4, 7.2 step 3, 6 | `spec:154`, `spec:182`, `spec:194` |
| 7 | WC-6's "fresh output directory" conflicts with retry. `--retry-of` reuses the same Task and brief, hence the same `--output`, so a retry either overwrites attempt 1 or writes to a directory the coordinator never recorded. | MAJOR | yes | 2.2 WC-6, 2.3 | `spec:64`, `spec:73`; `.dev/orca-command-refactor/inventory/orca-capabilities.md:116` |
| 8 | WC-3's "re-invoke or resume the command with the answer as a flag" has no route for gates without a flag (recommend's clarifying question, tdd topic clarification, task's confidence below 0.70), and a fresh-dir re-run changes the report path recorded before dispatch. | MAJOR | yes | 2.2 WC-3, 3.1 and 3.2 rows | `spec:61`, `spec:64`, `spec:90`, `spec:115`, `spec:121` |
| 9 | P1 makes `--unattended` a no-op on commands whose gates are converted only in P2 to P4. Between phases, `/sc:auggie-review --unattended` still posts to the PR (its default, with no prompt), which breaks WC-9 for a coordinator that trusts the P0 contract file. | MAJOR | yes | 6 (P1), 7.3 AC-1.1, WC-9 | `spec:67`, `spec:158-160`, `spec:195`; `src/superclaude/commands/auggie-review.md:51` |
| 10 | WC-7 forbids an Agent-tool wrapper but does not require the Skill tool call the repo makes mandatory. 7.2 step 5 and AC-0.4 do not check for it, so a worker that improvises the protocol from the command file passes. | MAJOR | yes | 2.2 WC-7, 7.2 step 5, AC-0.4 | `spec:65`, `spec:184`, `spec:194`; `CLAUDE.md:11` |
| 11 | WC-10 splits only Bash waits. One Agent-tool subagent call (kept by WC-7) can block the session past the 5-minute heartbeat, which the repo itself treats as unproven. A single 300 s call is also allowed. Only AC-4.3 (pr-submit) checks heartbeat gaps. | MAJOR | yes (FR-8 GAP) | 2.2 WC-10, WC-7, 7.3 | `spec:65`, `spec:68`, `spec:210`; `~/.claude/commands/sc/spec-panel-ledger.md:261` |
| 12 | 7.2 step 6 fails whenever the shared worktree holds any other file, and WC-11 explicitly allows two workers in one worktree (AC-3.4 runs two). This checkout already shows `?? .dev/orca-command-refactor/`. WC-11 also ignores shared git state: workflow runs `git add .dev/tasks`. | MAJOR | yes | 7.2 step 6, 2.2 WC-11, AC-3.4 | `spec:69`, `spec:185`, `spec:207`; `.dev/orca-command-refactor/inventory/orca-capabilities.md:115`; `src/superclaude/skills/sc-workflow-protocol/SKILL.md:28` |
| 13 | The "edits are additive" regex `^-[^-]` misses deleted lines that start with `-` (every Markdown bullet shows as `-- item`), so AC-C5 and AC-0.3 pass deletions. Tested: `-- removed bullet` gives NO_MATCH. | MAJOR | yes | 7.1 AC-C5, 7.3 AC-0.3, SA-4 | `spec:149`, `spec:176`, `spec:193` |
| 14 | WC-5 says the body's first sentence gives the report's "status and verdict", but WC-4 has no `verdict` field, so an audit FAIL with outcome `succeeded` is visible only in prose. | MINOR | no | 2.2 WC-4, WC-5 | `spec:62`, `spec:63` |
| 15 | WC-1 is owned by "Launch setup, not commands", but no phase scope or acceptance check names it (only 7.2 step 1 covers it indirectly). | MINOR | no | 2.2 WC-1, 6, 7 | `spec:59`, `spec:158-162`, `spec:180` |
| 16 | The stated repo root `.../OrcaCLICommandRefactor-Specs` does not exist on this machine (`ls` failed, 2026-11-08). Repo-relative paths still resolve in this checkout, and README line 8 says the same. | MINOR | no | header | `spec:4`; `.dev/orca-command-refactor/README.md:8` |
| 17 | The table-escaped `\|` in AC-C1, AC-C4, AC-C5 and AC-0.3 is literal in raw text. Copied from the raw file, AC-C1's pattern matched nothing on `orca worktree create` (NO_MATCH, tested), so the check passes vacuously. Rendered Markdown is correct. | MINOR | no | 7.1, 7.3 | `spec:172`, `spec:175`, `spec:176`, `spec:193` |

## Ledger input
Review-1 `find` rows, one per numbered finding (labels F1-F17). Checked with `find --input <this report> --dry-run`; the result is recorded under Decisions.

```ledger-input
[
  {"label": "F1", "grade": "MAJOR", "rule": "WC-4", "wrong_outcome": "Coordinator passes --output to /sc:workflow and the run STOPs E-LEGACY; without it the contract path is unknown before dispatch and a pre-creation STOP writes no contract at all.", "anchor": "Write the contract for pre-creation STOPs too", "finding": "workflow is marked ready but cannot meet WC-4: --output retired (sc-workflow-protocol/SKILL.md:24), generated package id (SKILL.md:44), no yaml on pre-creation STOP (SKILL.md:26)."},
  {"label": "F2", "grade": "MAJOR", "rule": "FR-8", "wrong_outcome": "7.2 step 4 assertion rejects existing workflow/brainstorm contracts with status: success, or renaming the value breaks their current readers.", "anchor": "Commands that already write a contract keep their fields and add the missing ones.", "finding": "WC-4 fixed status set conflicts with keep-their-fields; refs/return-contract.md:7 and sc-brainstorm-protocol/SKILL.md:341 use success."},
  {"label": "F3", "grade": "MAJOR", "rule": "FR-8", "wrong_outcome": "Under /sc:task --unattended, troubleshoot writes two schemas to one path, so either the TFEP consumer or the coordinator reads the wrong contract.", "anchor": "`REPORT.md` (`report_path`)", "finding": "troubleshoot already writes <output-dir>/return-contract.yaml with the TFEP schema (sc-troubleshoot-protocol/SKILL.md:560); WC-4 reuses the path."},
  {"label": "F4", "grade": "MAJOR", "rule": "WC-4", "wrong_outcome": "For /sc:tdd --output <file> the contract path is undefined, so 7.2 step 3 and AC-2.2 cannot locate it.", "anchor": "where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)", "finding": "WC-4 output-dir undefined for file-valued --output (tdd.md:49; spec 3.1 tdd and init-lite rows; AC-2.2 example)."},
  {"label": "F5", "grade": "MAJOR", "rule": "WC-4", "wrong_outcome": "AC-1.2 step 3 fails for adversarial whichever of the two contract paths is implemented.", "anchor": "Fix the contract filename to `<output>/adversarial/return-contract.yaml`", "finding": "adversarial fix path contradicts WC-4 <output-dir>/return-contract.yaml checked by 7.2 step 3."},
  {"label": "F6", "grade": "MAJOR", "rule": "AC-0.4", "wrong_outcome": "P0 cannot pass because step 3 needs a WC-4 contract that arrives only in P1, and later phases wait on P0, so the rollout never starts.", "anchor": "step 4 uses the command's existing report file, since the contract arrives in P1", "finding": "AC-0.4 exempts only step 4 but step 3 requires the WC-4 contract path and status."},
  {"label": "F7", "grade": "MAJOR", "rule": "WC-6", "wrong_outcome": "A --retry-of worker gets the same brief and --output, so it overwrites attempt 1 or writes to a directory the coordinator never recorded.", "anchor": "writes each run into a fresh output directory so a re-run starts clean", "finding": "WC-6 fresh-dir rule conflicts with retry reusing the Task brief (orca-capabilities.md:116) and WC-4 known-before-dispatch."},
  {"label": "F8", "grade": "MAJOR", "rule": "WC-3", "wrong_outcome": "For gates with no answer flag (recommend, tdd topic, task confidence) the coordinator's answer cannot reach the command, and a fresh-dir re-run changes the report path.", "anchor": "then re-invoke or resume the command with the answer as a flag", "finding": "WC-3 answer-as-flag route undefined for flagless gates."},
  {"label": "F9", "grade": "MAJOR", "rule": "WC-9", "wrong_outcome": "Between P1 and P2, /sc:auggie-review --unattended still posts to the PR by default, an outward action the contract says is off.", "anchor": "(a no-op where a command has no gate)", "finding": "P1 accepts --unattended on every command but gated commands convert only in P2-P4; auggie-review.md:51 posts with no prompt."},
  {"label": "F10", "grade": "MAJOR", "rule": "WC-7", "wrong_outcome": "A worker that reads the command file and improvises the protocol without the Skill call passes 7.2 step 5 and AC-0.4.", "anchor": "it never wraps the command in an Agent-tool subagent", "finding": "WC-7 does not require the Skill tool invocation mandated by CLAUDE.md:11; no check tests it."},
  {"label": "F11", "grade": "MAJOR", "rule": "FR-8", "wrong_outcome": "An Agent-tool subagent call or a single 300 s call blocks the session past the 5-minute heartbeat and no check outside AC-4.3 detects it.", "anchor": "A command step that blocks a single tool call for longer than 5 minutes (a poll wait, a long eval)", "finding": "WC-10 ignores subagent waits kept by WC-7; spec-panel-ledger.md:261 treats heartbeat through a long subagent run as unproven."},
  {"label": "F12", "grade": "MAJOR", "rule": "WC-11", "wrong_outcome": "7.2 step 6 fails whenever the shared worktree has any other untracked file (this checkout already shows ?? .dev/orca-command-refactor/), and two workers can collide on git add .dev/tasks.", "anchor": "only files under the brief's output directory (and the command's documented artifacts) appear", "finding": "step 6 and WC-11 ignore shared worktree and git index state (orca-capabilities.md:115; sc-workflow-protocol/SKILL.md:28)."},
  {"label": "F13", "grade": "MAJOR", "rule": "SA-4", "wrong_outcome": "A deleted Markdown bullet shows as '-- item', which grep -E '^-[^-]' does not match, so AC-C5 and AC-0.3 pass a non-additive edit.", "anchor": "src/superclaude/commands/<name>.md", "finding": "additive-edit regex misses deleted lines starting with '-'; tested NO_MATCH."},
  {"label": "F14", "grade": "MINOR", "rule": null, "wrong_outcome": null, "anchor": "The first sentence of the body states the report's status and verdict.", "finding": "WC-5 cites a verdict that WC-4 has no field for."},
  {"label": "F15", "grade": "MINOR", "rule": null, "wrong_outcome": null, "anchor": "Launch setup, not commands", "finding": "WC-1 has no phase owner or acceptance check."},
  {"label": "F16", "grade": "MINOR", "rule": null, "wrong_outcome": null, "anchor": "Repo root: /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs.", "finding": "stated repo root does not exist on this machine; relative paths still resolve."},
  {"label": "F17", "grade": "MINOR", "rule": null, "wrong_outcome": null, "anchor": "prints nothing (SA-2, WC-8)", "finding": "table-escaped \\| makes raw-copied checks vacuous; rendered Markdown is correct."}
]
```

## Decisions
| Decision | Options considered | Rationale |
|---|---|---|
| Ledger writes | Run `find` myself; leave every write to the coordinator | The brief allows writing only this report, and the command says this session runs only `status`, `verdict` and `--dry-run`. `find --dry-run` returned `ok: true, rows: 17, blocking: 13, deferred: 4` with `would_write: inputs/r1-find.json`. |
| Repo root | The spec's `OrcaCLICommandRefactor-Specs`; the brief's `exp346-v-ledger` | The brief's root is used: the spec's root does not exist here, and the ledger snapshot matches the spec in this checkout byte for byte. |
| Grade of Finding 9 (outward PR post between phases) | CRITICAL; MAJOR | MAJOR: the spec is ambiguous about P1 behaviour on gated commands rather than provably wrong. It blocks either way under the profile. |
| Shared git index collision | Separate finding; fold into Finding 12 | Folded: same root cause (WC-11 ignores state that workers share), so one fix covers both. |
| Escaped `\|` in checks | MAJOR; MINOR | MINOR: it is table formatting, and rendered Markdown shows the correct command. |
| Severity of WC-10's 300 s boundary | Separate MINOR; part of Finding 11 | Part of Finding 11: both GAP rows come from the same guard. |

## UNVERIFIED items
1. Whether an Agent-tool subagent call in a dispatched Claude worker blocks the top-level session from heartbeating. Some harness builds run subagents in the background. Finding 11 rests on the spec not covering it, not on an observed stall.
2. Whether `orca orchestration worker-start --retry-of` passes the identical Task spec text to the retry worker. `CAPS:116` shows the same `--task <task_id>`; the preamble contents of a retry were not read. Finding 7 assumes the brief is reused.
3. Whether an executing agent would copy the AC commands from raw Markdown (literal `\|`) or from the rendered form (Finding 17).
4. Whether `/sc:task --unattended` would in practice call troubleshoot with `caller=task-unified` and `--unattended` together (Finding 3). The path collision itself is verified at `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:560`.

<!-- review-ledger tail: written by review_ledger.py close; do not edit -->
## Review ledger

review: 1 of 3

| id | grade | rule | blocking | status | scope | anchor |
|---|---|---|---|---|---|---|
| R1 | MAJOR | WC-4 | yes | open | in | Write the contract for pre-creation STOPs too |
| R2 | MAJOR | FR-8 | yes | open | in | Commands that already write a contract keep their fields and add the missing ones. |
| R3 | MAJOR | FR-8 | yes | open | in | `REPORT.md` (`report_path`) |
| R4 | MAJOR | WC-4 | yes | open | in | where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`) |
| R5 | MAJOR | WC-4 | yes | open | in | Fix the contract filename to `<output>/adversarial/return-contract.yaml` |
| R6 | MAJOR | AC-0.4 | yes | open | in | step 4 uses the command's existing report file, since the contract arrives in P1 |
| R7 | MAJOR | WC-6 | yes | open | in | writes each run into a fresh output directory so a re-run starts clean |
| R8 | MAJOR | WC-3 | yes | open | in | then re-invoke or resume the command with the answer as a flag |
| R9 | MAJOR | WC-9 | yes | open | in | (a no-op where a command has no gate) |
| R10 | MAJOR | WC-7 | yes | open | in | it never wraps the command in an Agent-tool subagent |
| R11 | MAJOR | FR-8 | yes | open | in | A command step that blocks a single tool call for longer than 5 minutes (a poll wait, a long eval) |
| R12 | MAJOR | WC-11 | yes | open | in | only files under the brief's output directory (and the command's documented artifacts) appear |
| R13 | MAJOR | SA-4 | yes | open | in | src/superclaude/commands/<name>.md |
| R14 | MINOR |  | no | deferred | in | The first sentence of the body states the report's status and verdict. |
| R15 | MINOR |  | no | deferred | in | Launch setup, not commands |
| R16 | MINOR |  | no | deferred | in | Repo root: /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs. |
| R17 | MINOR |  | no | deferred | in | prints nothing (SA-2, WC-8) |

### Reviser brief

Blocking rows to fix: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13
Revise only text a listed blocking row names; minor (deferred) rows are not answerable; add no rule, mechanism or section no blocking row calls for; each added paragraph or table cites its row id; report the byte size before and after.

loop_decision: CONTINUE (U=13, X=0, I=true)
verdict: FAIL
