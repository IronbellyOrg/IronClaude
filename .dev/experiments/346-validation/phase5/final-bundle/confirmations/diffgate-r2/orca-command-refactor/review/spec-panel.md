# Spec panel review: orca-worker-contract-spec.md

review: 1 of 3
Task: task_04238322f65b (Task 5, independent review). Reviewer did not write the spec.
Command: `/sc:spec-panel-diffgate @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture --diffgate-dir .dev/orca-command-refactor/review/diffgate-loop --expect-round 1`
Reviewed copy: `.dev/orca-command-refactor/review/diffgate-loop/doc-r1.md` (byte-identical to the spec; `at=` line numbers refer to it).
Diffgate `status`: state `open`, review 1 (full document).

**Result: FAIL.** 8 blocking findings (R1.1-R1.8) and 4 minor notes (R1.9-R1.12), derived by `diffgate.py check --dry-run` on this report (exit 0, `blocking_ids` R1.1-R1.8). Per the command, the formal last line (`verdict: FAIL`) and the Reviser brief come from the coordinator's `check` step, which appends `close-r1.md`; this reviewer writes no `verdict:` line.

## Method
- Read the whole spec (`doc-r1.md:1-286`) and the binding run rules (`.dev/orca-command-refactor/README.md:31-41`).
- Re-read the sources behind the load-bearing claims instead of trusting the inventories: the existing return-contract schemas (`src/superclaude/skills/sc-adversarial-protocol/SKILL.md:432-456`, `src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md:1-41`, `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:253,280-292,341`, `src/superclaude/skills/sc-reflect-protocol/SKILL.md:250`), the workflow flag ban (`src/superclaude/commands/workflow.md:42`), the auggie-review flags (`src/superclaude/commands/auggie-review.md:45-55`), Orca liveness and report facts (`.dev/orca-command-refactor/inventory/orca-capabilities.md:79-80,125-131`), the PR #329 brief and contract (`.dev/codegraph-migration/orchestration/README.md:28-34`, `.dev/codegraph-migration/decisions/P3-command-set/adversarial/return-contract.yaml:1-15`).
- Ran E5 and AC-C1 in this worktree on 2026-11-09: `grep -rlni orca` over commands, skills, core and agents lists only `src/superclaude/skills/ccsession-tag/` files; the AC-C1 grep prints nothing. Both claims hold today.
- Counted `src/superclaude/commands/`: 45 entries, of which `README.md` and `__init__.py` are not commands, so 43 commands, matching the spec's 10 + 27 + 6 (`doc-r1.md:76`).
- Panel: requirements focus (Wiegers lead, Adzic, Cockburn) and architecture focus (Fowler lead, Nygard, Newman, Hohpe), plus Whittaker (always active) and Crispin for the acceptance checks.

## Panel result

=== REQUIREMENTS ANALYSIS ===

**Wiegers (requirements quality).** The WC table is the strongest part: each rule has an owner and evidence. Its weak point is WC-4, the rule every later phase checks. It fixes a status vocabulary (`succeeded / partial / failed / blocked`, `doc-r1.md:62`) and in the same paragraph tells commands that already write a contract to "keep their fields". The commands the spec itself names as the model (`doc-r1.md:261`) write `status: success`, not `succeeded` (`sc-adversarial-protocol/SKILL.md:436,454`; `sc-workflow-protocol/refs/return-contract.md:7`), and two write values outside any four-value set (`dry-run` at `sc-brainstorm-protocol/SKILL.md:253,341`; `stopped-precondition` at `sc-reflect-protocol/SKILL.md:250`). The rule cannot be met as written: keeping the field fails the 7.2 step 4 assertion (`doc-r1.md:183`), and renaming it breaks today's consumers, for example brainstorm reading the adversarial contract's `status` (`sc-brainstorm-protocol/SKILL.md:283`). Finding R1.1.

**Wiegers (continued).** WC-4 also assumes every command takes an output directory (`doc-r1.md:62`). Rows in the spec's own tables break that: `/sc:workflow` bans `--output` as `E-LEGACY` and always writes to a generated `.dev/tasks/to-do/<id>/` (`src/superclaude/commands/workflow.md:42`; `doc-r1.md:92`), so the path is not "known before dispatch" and a brief that passes `--output` stops the run; `/sc:init-lite` and `/sc:tdd` take `--output <file>`, a file, not a directory (`doc-r1.md:87,90`). Finding R1.2.

**Adzic (examples).** The spec gives command-line examples but no worked example of a full contract file; one example per status value would have exposed R1.1. AC-2.2 (`doc-r1.md:200`) is the one example-driven check for gates, and it is not deterministic: WC-3 lets the worker ask the coordinator instead of resolving as blocked (`doc-r1.md:61`), and then the run can end `succeeded`. Finding R1.8.

**Cockburn (actors and goals).** Coordinator, worker session and command are clear actors; the person is the fourth actor for D2 and D4 and is handled well. The weak boundary is worker session versus command: WC-7 says the worker "runs the command directly" (`doc-r1.md:65`) but never says how. A slash command written inside a pasted TASK block is not a message that starts with `/sc:`, so the worker must make a `Skill` call. The owner ruled on 2026-11-07 that a worker which only reads the command file does not satisfy WC-7, after 11 P1 live rows passed 7.2 step 5 that way (`/home/coder/.claude/projects/-home-coder-workspaces-IronClaude/memory/p1-c5-wc7-decided-no.md:11-15`). Neither WC-7, 7.2 step 5 (`doc-r1.md:184`) nor AC-0.4 (`doc-r1.md:194`) checks for the call. Finding R1.6.

=== ARCHITECTURE ANALYSIS ===

**Fowler (interfaces).** The section 1 decision is sound and well argued: one stable interface (the `--unattended` flag plus one report file) between coordinator and command, no Orca coupling in commands. The interface leaks in two places. First, the report location is not one rule: WC-4 says `<output-dir>/return-contract.yaml` (`doc-r1.md:62`), the adversarial fix says `<output>/adversarial/return-contract.yaml` (`doc-r1.md:83`), and workflow says `.dev/tasks/to-do/<id>/return-contract.yaml` (`doc-r1.md:92`). A coordinator written to WC-4 opens the wrong path for adversarial. Finding R1.3. Second, the flag's meaning shifts across phases: P1 makes every command in 3.1-3.2 accept `--unattended` (`doc-r1.md:159`) and AC-1.1 requires each to carry an `## Unattended mode` section in P1 (`doc-r1.md:195`), but the gate behaviour behind the flag lands in P2-P4. Between P1 and P2, `/sc:auggie-review <PR> --unattended` is accepted and still posts to GitHub, because posting is on by default with no prompt (`src/superclaude/commands/auggie-review.md:51`) and the `--no-post-pr` implication is a P2 change (`doc-r1.md:100,160`). Finding R1.4.

**Nygard (failure modes).** The spec reasons well about the silent stall (`doc-r1.md:44`) and correctly notes a waiting worker reads as healthy (`orca-capabilities.md:129`). WC-10 then fails on its own terms: it asks for a heartbeat every 5 minutes and requires any single tool call over 5 minutes to be split (`doc-r1.md:68`), while E4 and WC-7 keep each command's Agent-tool fan-out unchanged (`doc-r1.md:24,65`). An Agent-tool wave in `/sc:adversarial`, `/sc:tasklist` (reflect fan-out) or `/sc:tdd` is one blocking tool call that can run well past 5 minutes, so the implementer must break one rule or the other. The preamble's own remedy, a background heartbeat loop ("If a background loop sends them, restart it if it expires mid-task"), is absent from the spec. Finding R1.5. Orca's guide says absence of a signal never authorizes stop or retry (`orca-capabilities.md:125`) and that a heartbeat is liveness only (`orca-capabilities.md:130`), so the harm is a contradictory requirement and false check failures, not lost work.

**Whittaker (adversarial).**
- I can break this specification by **Sentinel Collision Attack**. The invariant at **WC-4 / WC-5 (`doc-r1.md:62-63`)** fails when **an existing contract writes `status: success`, `dry-run` or `stopped-precondition`**. Concrete attack: P1 adds `--unattended` to `/sc:adversarial` and keeps its fields as WC-4 says; the run writes `status: "success"`; WC-5 has no mapping for `success`; 7.2 step 4 asserts `status in {succeeded, partial, failed, blocked}` and fails a correct run. State: `status=success` → mapping undefined → AC fails. (R1.1)
- I can break this specification by **Zero/Empty Attack**. The invariant at **WC-4 (`doc-r1.md:62`)** fails when **the command has no output-directory flag**. Concrete attack: the coordinator follows 2.3 and writes `/sc:workflow "<change>" --unattended --handoff none --output .dev/x/`; workflow stops with `E-LEGACY` before any package exists, and its contract rule says that STOP writes no yaml (`sc-workflow-protocol/refs/return-contract.md:39`). State: brief path `.dev/x/return-contract.yaml` → never written → `worker_done --outcome failed` with no report. (R1.2)
- I can break this specification by **Sequence Attack**. The invariant at **SA-1 / WC-9 across phases (`doc-r1.md:159-160`)** fails when **a coordinator dispatches a gated command after P1 and before that command's phase**. Concrete attack: after P1, `/sc:auggie-review 123 --unattended --output-dir d/`; the flag is accepted and the review is posted to PR 123. State: GitHub review count n → n+1, the outcome AC-2.4 later forbids. (R1.4)
- I can break this specification by **Divergence Attack**. The invariant at **AC-2.2 (`doc-r1.md:200`)** fails when **the worker takes the permitted WC-3 `ask` branch**. Concrete attack: `/sc:tdd "auth" --unattended`; the worker asks the coordinator, gets a component name, re-invokes, writes `status: succeeded`; AC-2.2 expects `failed`/`blocked` and fails a correct implementation. (R1.8)
- I can break this specification by **Accumulation Attack**. The invariant at **WC-10 (`doc-r1.md:68`)** fails when **a command's Agent-tool wave accumulates past 5 minutes inside one tool call**. Concrete attack: `/sc:adversarial` at standard depth spawns its variant agents in one message; the top-level session cannot heartbeat until all return; heartbeat gap grows past 5 minutes with no rule broken by the command. (R1.5)

**Newman (evolution).** `~/.claude/WORKER-CONTRACT.md` carries no version, while the workflow return-contract already has `contract_version: "1.1"` (`sc-workflow-protocol/refs/return-contract.md:6`). A coordinator reading reports from mixed installs cannot tell which rules a report follows. Minor note R1.12.

**Hohpe (message exchange).** Brief → optional `ask`/reply → one `worker_done` carrying a pointer is a clean claim-check pattern; Orca does not read the pointed-to file (`orca-capabilities.md:79`), and the spec correctly makes the coordinator open it (`doc-r1.md:62`). One exchange gap: SA-2 allows an Orca mention "as an example of a caller's question channel inside the contract file" (`doc-r1.md:147`), but the contract file sits in `src/superclaude/core`, which AC-C1 greps (`doc-r1.md:172`); the natural example (`orca orchestration ask`) makes AC-C1 fail in P0. Finding R1.7.

=== ACCEPTANCE CHECKS (Crispin) ===
Checks are concrete and runnable, and AC-C3's baseline approach is right. Beyond R1.6 and R1.8: 7.2 step 6 (`doc-r1.md:185`) passes only if `git status --short` shows nothing outside the output directory, but WC-11 and 7.2 step 1 put workers in the shared current worktree (`doc-r1.md:69,180`), so a parallel worker's files make a correct run fail (R1.10, minor).

=== CONSENSUS ===
- The architecture decision (Orca on top, commands stay the units, no Orca calls in commands) is supported by the evidence, and the rejected alternative is fairly argued. No expert disputes section 1.
- The report-file interface (WC-4) is the one thing every phase depends on, and it is not implementable as written (R1.1, R1.2, R1.3). Fix it before P1 starts.
- The phase plan needs one rule for what `--unattended` does on a command whose gate work lands in a later phase (R1.4).

=== DISAGREEMENT ===
- Fowler would have P1 add `--unattended` only to commands with no gate; Nygard would have gated commands refuse `--unattended` (blocked contract, "not yet supported") until their phase. Either closes R1.4; the panel does not pick.

Quality scores (0-10): Clarity 8, Completeness 6, Testability 6, Consistency 5.

## Numbered findings
Severity uses the panel scale. "Blocking" follows the command's rule: a MAJOR is blocking only when it names a concrete wrong outcome an implementer would produce (the script derives this from the `outcome=` field below). Spec lines are lines of `doc-r1.md`, which is byte-identical to `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`.

| # | Finding | Severity | Spec section | Evidence (path:line) |
|---|---|---|---|---|
| 1 (R1.1) | WC-4 fixes `status` to `succeeded/partial/failed/blocked` but tells commands with a contract to keep their fields; their `status` is `success`, `dry-run` or `stopped-precondition`. Keeping the field fails 7.2 step 4 and leaves WC-5 with no mapping; renaming breaks existing readers. | MAJOR, blocking | 2.2 WC-4, WC-5; 7.2 step 4 | spec `doc-r1.md:62,63,183,261`; `src/superclaude/skills/sc-adversarial-protocol/SKILL.md:436,454`; `src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md:7`; `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:253,283,341`; `src/superclaude/skills/sc-reflect-protocol/SKILL.md:250` |
| 2 (R1.2) | WC-4 assumes every command takes an output directory the coordinator passes. `/sc:workflow` bans `--output` (`E-LEGACY`) and writes to a generated `<id>` folder, so its path is not known before dispatch and a WC-4 brief stops the run; `/sc:init-lite` and `/sc:tdd` take a file, not a directory. | MAJOR, blocking | 2.2 WC-4; 2.3; 3.1 workflow, init-lite, tdd rows | spec `doc-r1.md:62,73,87,90,92`; `src/superclaude/commands/workflow.md:42`; `src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md:3,39` |
| 3 (R1.3) | The adversarial fix names `<output>/adversarial/return-contract.yaml`, which differs from the WC-4 path `<output-dir>/return-contract.yaml`; a coordinator built to WC-4 opens a file that does not exist. | MAJOR, blocking | 3.1 adversarial row; 2.2 WC-4; AC-1.4 | spec `doc-r1.md:62,83,198`; `src/superclaude/skills/sc-adversarial-protocol/SKILL.md:434` (`artifacts_dir` is the `adversarial/` directory) |
| 4 (R1.4) | P1 makes every 3.1-3.2 command accept `--unattended` and AC-1.1 requires its `## Unattended mode` section in P1, but gate and outward-action behaviour lands in P2-P4. Between phases, `/sc:auggie-review <PR> --unattended` still posts to GitHub; nothing says what the flag does on a gated command before its phase. | MAJOR, blocking | 6 P1, P2; 7.3 AC-1.1, AC-2.4; 2.2 WC-9 | spec `doc-r1.md:100,159,160,195,202`; `src/superclaude/commands/auggie-review.md:51` |
| 5 (R1.5) | WC-10 requires splitting any single tool call over 5 minutes so the worker can heartbeat, while E4 and WC-7 keep Agent-tool fan-out unchanged; an Agent-tool wave is one tool call that can exceed 5 minutes. The two rules conflict; the preamble's background heartbeat loop, which would resolve it, is not in the spec. | MAJOR, blocking | 2.2 WC-10, WC-7; 1.2 E4 | spec `doc-r1.md:24,65,68`; `.dev/orca-command-refactor/inventory/orca-capabilities.md:130` (cadence from the preamble only) |
| 6 (R1.6) | WC-7 says the worker "runs the command directly" but not how; a command line inside a TASK block is not expanded, so a worker can read the command file and improvise. 7.2 step 5 and AC-0.4 check only for `AskUserQuestion` and the absence of an Agent wrapper, not for a `Skill`/command call. The owner already ruled this case fails WC-7 after 11 P1 rows passed that way. | MAJOR, blocking | 2.2 WC-7; 7.2 step 5; 7.3 AC-0.4 | spec `doc-r1.md:65,184,194`; `/home/coder/.claude/projects/-home-coder-workspaces-IronClaude/memory/p1-c5-wc7-decided-no.md:11-15` |
| 7 (R1.7) | SA-2 allows an Orca example inside the contract file, which lives in `src/superclaude/core`; AC-C1 greps that folder for `orca orchestration ...` and must print nothing, so the natural WC-3 example fails P0. | MAJOR, blocking | 5 SA-2; 7.1 AC-C1; 2.1 contract file | spec `doc-r1.md:52,61,147,172` |
| 8 (R1.8) | AC-2.2 expects every gate-trigger run to end `failed` with `status: blocked`, but WC-3 lets the worker ask the coordinator and re-invoke, after which the run can end `succeeded`; a correct implementation fails the check. | MAJOR, blocking | 7.3 AC-2.2; 2.2 WC-3 | spec `doc-r1.md:61,200` |
| 9 (R1.9) | The stated repo root `OrcaCLICommandRefactor-Specs` does not exist on this machine; the spec was reviewed in `exp346-v-diffgate-r2`. Paths are repo-relative, so no claim breaks. | MINOR | header | spec `doc-r1.md:4`; `.dev/orca-command-refactor/README.md:8`; `ls` of that path on 2026-11-09: "No such file or directory" |
| 10 (R1.10) | 7.2 step 6 fails a correct worker whenever another worker shares the current worktree, which WC-11 and step 1 make the default. | MINOR | 7.2 step 6; 2.2 WC-11 | spec `doc-r1.md:69,180,185` |
| 11 (R1.11) | "the only command-side change ... besides report files and resume" overstates: section 3 also adds tools, fixes defaults and reconciles skills. | MINOR | 2.1 | spec `doc-r1.md:51,108,124-125` |
| 12 (R1.12) | The shared contract has no `contract_version`, unlike workflow's existing contract, so mixed installs cannot be told apart. | MINOR | 2.2 WC-4 | spec `doc-r1.md:62`; `src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md:6` |

## Guard Condition Boundary Table
Built by Nygard, checked by Crispin, attacked by Whittaker. Every GAP maps to a numbered finding above (FR-8).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-5 status mapping | 2.2 WC-5 (`doc-r1.md:63`) | Zero/Empty | no report file; `status` missing or empty | maps to failed | "no report exists" → `failed`; missing field not stated | GAP (R1.1) |
| WC-5 status mapping | 2.2 WC-5 | One/Minimal | `blocked` | failed | `--outcome failed` | OK |
| WC-5 status mapping | 2.2 WC-5 | Typical | `succeeded`, `partial` | succeeded | `--outcome succeeded` | OK |
| WC-5 status mapping | 2.2 WC-5 | Maximum/Overflow | audit verdict FAIL with `succeeded` | succeeded | stated: audit itself succeeded | OK |
| WC-5 status mapping | 2.2 WC-5 / WC-4 | Sentinel Value Match | legacy `success`, `dry-run`, `stopped-precondition` | undefined | not specified; WC-4 keeps the field | GAP (R1.1) |
| WC-5 status mapping | 2.2 WC-5 | Legitimate Edge Case | `failed` | failed | `--outcome failed` | OK |
| WC-10 wait split | 2.2 WC-10 (`doc-r1.md:68`) | Zero/Empty | no long step | no split | heartbeat every 5 min | OK |
| WC-10 wait split | 2.2 WC-10 | One/Minimal | one 60 s poll | no split | allowed | OK |
| WC-10 wait split | 2.2 WC-10 | Typical | 4 min wait | no split | allowed (Decisions row, `doc-r1.md:266`) | OK |
| WC-10 wait split | 2.2 WC-10 | Maximum/Overflow | 3600 s eval | split | split into ≤4 min waits | OK |
| WC-10 wait split | 2.2 WC-10 vs WC-7 | Sentinel Value Match | Agent-tool wave > 5 min (one tool call) | split required | WC-7 says fan-out stays unchanged; conflict | GAP (R1.5) |
| WC-10 wait split | 2.2 WC-10 | Legitimate Edge Case | exactly 5 min | no split ("longer than") | inferrable; 1-minute margin lost | OK |
| `--unattended` present | 2.1, 6 P1 (`doc-r1.md:51,159`) | Zero/Empty | flag absent | standalone | today's behaviour (SA-1) | OK |
| `--unattended` present | 6 P1 | One/Minimal | flag on a no-gate command | accepted | no-op | OK |
| `--unattended` present | 3.2 rows | Typical | flag on a gated command in or after its phase | accepted | per-row resolution | OK |
| `--unattended` present | 6 P1 vs P2-P4 | Maximum/Overflow | flag on a gated command before its phase | accepted | not specified | GAP (R1.4) |
| `--unattended` present | 4 | Sentinel Value Match | flag on a section-4 command | n/a | never dispatched; no section (AC-1.1) | OK |
| `--unattended` present | 3.2 cleanup, roadmap | Legitimate Edge Case | with `--interactive` | refused | refused per row | OK |
| WC-4 output dir | 2.2 WC-4 (`doc-r1.md:62`) | Zero/Empty | command has no dir flag (workflow) or bans it | n/a | not specified | GAP (R1.2) |
| WC-4 output dir | 2.2 WC-4 | One/Minimal | `--output <file>` (init-lite, tdd) | n/a | not specified | GAP (R1.2) |
| WC-4 output dir | 2.2 WC-4 | Typical | `--output <dir>` | contract at `<dir>/return-contract.yaml` | stated | OK |
| WC-4 output dir | 3.1 adversarial | Maximum/Overflow | nested `<dir>/adversarial/` | two paths | conflicting rules | GAP (R1.3) |
| WC-4 output dir | 2.2 WC-6 | Sentinel Value Match | dir holds a prior attempt's contract | fresh dir or resume | stated | OK |
| WC-4 output dir | 2.2 WC-4 | Legitimate Edge Case | STOP before any output | contract still written | stated ("every outcome") | OK |

## Self-audit
Checked and found sound, so no finding: section 1 evidence E1-E6 and R1-R5 against the cited CAPS lines; E5 and AC-C1 by running them; the 43-command count; auggie-review's `--post-pr`/`--no-post-pr` flags exist as the row assumes (`src/superclaude/commands/auggie-review.md:51-52`); the circuit-breaker claim (`orca-capabilities.md:80`); the WC-5 `partial`→`succeeded` rationale; D1-D5 each stand alone with a recommendation. E3 versus 1.4 (PR #329 ran through Agent-tool subagents, `.dev/codegraph-migration/orchestration/README.md:31`, while the contract records `invocation_method: "skill-direct"`, `return-contract.yaml:10`) is consistent: 1.4 already says the run proves only the nested route. Not checked: section-3 citations not named above (taken from the inventories), and any live Orca behaviour.

## Decisions
| Decision | Options | Rationale |
|---|---|---|
| Review the worktree copy, not the stated repo root | stated root; this worktree | The stated root does not exist (R1.9); the diffgate ledger points at this worktree's spec (`review/diffgate-loop/ledger.json`, `doc` field). |
| Grade R1.7 and R1.8 blocking | minor; blocking | Each names an acceptance check that fails a correct implementation, which is a concrete wrong outcome. |
| Use the owner's memory note as evidence for R1.6 | omit; cite | It is the only record of the owner's WC-7 ruling and of the 11 P1 rows; it is outside the repo, so the path is absolute. |
| No verdict line written by the reviewer | write one; leave to `check` | The command says the verdict comes from the coordinator's `check` step (`close-r1.md`). |

## UNVERIFIED items
1. That a pasted `/sc:` line inside a TASK block is not expanded by Claude Code. This session had to make an explicit Skill call to run its own command, which is consistent but is one observation.
2. How long a real Agent-tool wave in `/sc:adversarial` or `/sc:tasklist` runs; R1.5 rests on the rules conflicting, not on a measured duration.
3. Whether Orca uses heartbeat age in its liveness verdict (`orca-capabilities.md:130` marks it UNVERIFIED).

## Diffgate findings
FINDING R1.1 sev=major at=62 fr=8 anchor="Commands that already write a contract keep their fields and add the missing ones" outcome="P1 keeps status: success in adversarial and workflow contracts, so WC-5 has no mapping and 7.2 step 4 fails a correct run; renaming instead breaks brainstorm reading the adversarial status" :: WC-4 status vocabulary conflicts with existing contracts
FINDING R1.2 sev=major at=62 fr=8 anchor="where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)" outcome="a brief for /sc:workflow passes --output, workflow stops with E-LEGACY and writes no contract; init-lite and tdd get a file path where a directory is expected" :: WC-4 assumes every command takes an output directory
FINDING R1.3 sev=major at=83 anchor="Fix the contract filename to `<output>/adversarial/return-contract.yaml`" outcome="a coordinator built to WC-4 opens <output>/return-contract.yaml for adversarial and finds no file" :: adversarial contract path differs from WC-4
FINDING R1.4 sev=major at=159 fr=8 anchor="the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)" outcome="after P1, /sc:auggie-review <PR> --unattended is accepted and still posts the review to GitHub because the posting-off rule is a P2 change" :: --unattended behaviour on gated commands before their phase is unspecified
FINDING R1.5 sev=major at=68 fr=8 anchor="A command step that blocks a single tool call for longer than 5 minutes" outcome="the WORKER-CONTRACT.md author must either split Agent-tool fan-out that WC-7 keeps unchanged or ship a rule every adversarial or tasklist worker breaks" :: WC-10 conflicts with WC-7 for Agent-tool waves
FINDING R1.6 sev=major at=65 anchor="The worker runs the command directly in its own session" outcome="a worker reads the command file and improvises with no Skill call, and 7.2 step 5 and AC-0.4 record it as PASS, as happened in 11 P1 rows" :: WC-7 does not require or check the Skill or command call
FINDING R1.7 sev=major at=147 anchor="The only allowed mention of Orca in a changed command is as an example of a caller's question channel inside the contract file." outcome="P0 writes an orca orchestration ask example into src/superclaude/core/WORKER-CONTRACT.md and AC-C1 fails" :: SA-2 allowance contradicts AC-C1
FINDING R1.8 sev=major at=200 anchor="`worker_done --outcome failed`; contract `status: blocked` with a non-empty `blocked_question`" outcome="a correct P2 gate conversion fails AC-2.2 whenever the worker uses the WC-3 ask path and the run ends succeeded" :: AC-2.2 ignores the WC-3 ask branch
FINDING R1.9 sev=minor at=4 anchor="Repo root: /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs" :: stated repo root does not exist
FINDING R1.10 sev=minor at=185 anchor="only files under the brief's output directory" :: step 6 fails under the shared worktree default
FINDING R1.11 sev=minor at=51 anchor="It is the only command-side change the contract asks for besides report files and resume." :: overstates the scope of command changes
FINDING R1.12 sev=minor at=62 anchor="One report file, known before dispatch, written on every outcome." :: no contract_version field


Reviser brief: your task list is `.dev/orca-command-refactor/review/diffgate-loop/reviser-brief-r1.md` (blocking ids R1.1, R1.2, R1.3, R1.4, R1.5, R1.6, R1.7, R1.8). Revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; write the fix map only inside your own disposition file, as a `## Diffgate fixmap` block with a `doc_sha:` first line and one line per changed hunk naming its blocking ids, or `declined <id> <reason>`; run the script's read-only `fixcheck --dry-run --map <disposition file>` until it exits 0; report the byte size before and after, which `fixcheck` prints. The next review refuses to open while any hunk maps to no listed finding.

verdict: FAIL
