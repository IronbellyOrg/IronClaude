# Spec panel review: orca-worker-contract-spec.md

review: 1 of 3
Task: task_dfb49b3c1503 (Task 5, independent review). Reviewer did not write the spec.
Command: `/sc:spec-panel-diffgate @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture --diffgate-dir .dev/orca-command-refactor/review/diffgate-loop --expect-round 1`
Spec under review: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (byte copy `review/diffgate-loop/doc-r1.md`; line numbers below refer to it).
Diffgate status before review: `state: open`, `review: 1` (matches `--expect-round 1`).

## 1. Method
- Mode: critique; focus: requirements (Wiegers lead, Adzic, Cockburn) and architecture (Fowler lead, Newman, Hohpe, Nygard); Whittaker's adversarial pass is always on. Under `--diffgate-dir` the run is one review, the Improve step is skipped and no revised spec is written (command file, Review Loop bullet 4). The spec was not edited.
- Read the whole spec (`doc-r1.md:1-286`) and the shared rules (`.dev/orca-command-refactor/README.md:29-38`).
- Re-read the sources the findings depend on (2026-11-09, this worktree): `src/superclaude/commands/` (43 command files plus `README.md` and `__init__.py`, so the count at `doc-r1.md:76` holds); `grep -rlni orca` over commands, skills, core and agents (only `sk/ccsession-tag/` files, so E5 at `doc-r1.md:25` holds); the AC-C1 grep at `doc-r1.md:172` (prints nothing today); `sk/sc-workflow-protocol/SKILL.md:24,66,72`; `cmd/workflow.md:12,42`; `sk/sc-adversarial-protocol/SKILL.md:425-429`; `sk/sc-tasklist-protocol/SKILL.md` Stage 10.5 block (about lines 1612-1630); `sk/sc-reflect-protocol/refs/remediation-handoff.md` "Headless auto-accept" section (about lines 235-250); `sk/sc-troubleshoot-protocol/refs/remediation-handoff.md:3,14,58`; `sk/sc-brainstorm-protocol/SKILL.md:134,335`; `cmd/auggie-review.md:51-55`; `CLAUDE.md:9-11,16,50,72-83`; `.dev/orca-command-refactor/inventory/orca-capabilities.md:52,64,76,97-103,129-130,159-162`; `.dev/orca-command-refactor/inventory/commands-a.md:60-62`.
- `git check-ignore -v .dev/reviews/x .dev/troubleshoot/x .claude-audit/x` printed nothing, so these output locations are not ignored and appear in `git status --short` (the current status already shows `?? .dev/orca-command-refactor/`).
- Grading follows the command's Review Loop bullet 2: CRITICAL is blocking; MAJOR is blocking only when it names a concrete wrong outcome (`outcome=` in the findings block); MINOR is a note.

## 2. Requirements analysis
=== REQUIREMENTS ANALYSIS ===

**Wiegers (testability, traceability).** The decision (section 1) and the standalone rules (section 5) are well evidenced, and most WC rules trace to a source line. The breaks are between the requirement tables and the acceptance checks:
- AC-1.1 (`doc-r1.md:195`) makes every command in sections 3.1-3.2 carry an `## Unattended mode` section naming `return-contract.yaml` at the end of P1. The `/sc:load` row gives it no report (`doc-r1.md:112`), and the Decisions table rejects a load report as "an unrequested addition" (`doc-r1.md:265`). AC-1.1 passes only if P1 adds what the Decisions table forbids. (R1.1)
- The same AC-1.1 reaches every P2-P4 command at P1, including `/sc:implement`, `/sc:post-release` and `/sc:pr-submit`, which section 6 holds until the user answers D2-D4 (`doc-r1.md:154,162`). The P1 scope defines `--unattended` only as "a no-op where a command has no gate" (`doc-r1.md:159`) and is silent on gated commands, so between P1 and P2 `/sc:auggie-review --unattended` is accepted while its default still posts with "No confirmation prompt" (`cmd/auggie-review.md:51`), breaking WC-9 (`doc-r1.md:67`). (R1.2)
- WC-1 (`doc-r1.md:59`) is owned by "Launch setup" but no phase scope and no AC exercises it. (R1.11, minor)
- Section 2.1 calls `--unattended` "the only command-side change ... besides report files and resume" (`doc-r1.md:51`), while WC-9, WC-10 and WC-11 are also command-owned (`doc-r1.md:67-69`). (R1.12, minor)

**Adzic (examples).** The WC-4 path does not hold for two commands the spec itself schedules:
- `/sc:workflow` has no output flag: `--output` is retired and raises `E-LEGACY` (`cmd/workflow.md:42`; `sk/sc-workflow-protocol/SKILL.md:24`), and its contract lands in a new package named with the run's own timestamp (`cmd/workflow.md:12`; `sk/sc-workflow-protocol/SKILL.md:66,72`). WC-4 requires a path "known before dispatch" inside "the directory the coordinator passed" (`doc-r1.md:62`); the workflow row only adds the pre-creation STOP fix (`doc-r1.md:92`). (R1.3)
- The adversarial row fixes the contract at `<output>/adversarial/return-contract.yaml` (`doc-r1.md:83`), not the WC-4 path `<output-dir>/return-contract.yaml` (`doc-r1.md:62`). (R1.4)

**Cockburn (actors and goals).** The actors are clear (coordinator, worker session, command, person). One goal path is undefined: after WC-3's `ask`, the worker "re-invoke[s] or resume[s] the command with the answer as a flag" (`doc-r1.md:61`), but WC-6 makes commands without a resume flag write "each run into a fresh output directory" (`doc-r1.md:64`), and WC-4 fixes the report inside the brief's directory (`doc-r1.md:62`). The spec does not say which directory the second run uses or which contract the worker reports. (R1.6)

## 3. Architecture analysis
=== ARCHITECTURE ANALYSIS ===

**Fowler (boundaries, interfaces).** The central boundary is sound: Orca above, commands as units, no Orca calls inside commands (`doc-r1.md:16`; R1-R5 at `doc-r1.md:33-37`). Two places blur it:
- P0 adds "an Orca section to `HOW-WE-WORK.md`" (`doc-r1.md:158`) and a core `WORKER-CONTRACT.md` that holds the worker-session rules (WC-3, WC-5, WC-10, WC-12 name `ask`, `worker_done`, `heartbeat`, `check`; `doc-r1.md:61-70`). Both files live in `src/superclaude/core`, which AC-C1 scans for `orca orchestration|worktree|terminal|agent` (`doc-r1.md:172`). SA-2 allows Orca only "as an example of a caller's question channel inside the contract file" (`doc-r1.md:147`). The spec never says how the routing section names dispatch without the Orca command words, so the natural text fails AC-C1 in every phase. (R1.8)
- WC-7 says the worker "runs the command directly" (`doc-r1.md:65`) but does not name the mechanism. In a dispatched session the `/sc:` text sits inside the preamble's TASK block, not at the start of the message, and the repo rule is that the command's skill is invoked with the Skill tool, and answering from memory "is a VIOLATION" (`CLAUDE.md:9-11`). AC-0.4 only checks for the absence of an Agent-tool wrapper (`doc-r1.md:194`). (R1.9)

**Nygard (failure modes).** WC-10 asks for a heartbeat every 5 minutes and splits only "a poll wait, a long eval" (`doc-r1.md:68`). Fan-out commands block the session in one Agent-tool call (parallel calls in one message return together) and WC-7 forbids subagents from heartbeating. Whether such calls exceed 5 minutes was not measured (UNVERIFIED), and Orca does not treat heartbeat absence as a stop reason (`orca-capabilities.md:125,130`), so this is a note. (R1.10, minor)

**Newman (evolution).** The phase order by risk (`doc-r1.md:267`) is right, but P1 changes the public flag surface of 37 commands at once while their meaning is only defined in P2-P4 (R1.2). A flag that is accepted but means nothing on a gated command is the backward-compatibility hazard here.

**Hohpe (message exchange).** The report channel is a file plus one `worker_done`, which is the right durable pattern (`orca-capabilities.md:76`). The exchange breaks where the file path is not fixed before dispatch (R1.3, R1.4) and where a question round trip (WC-3) changes which file is final (R1.6). The coordinator's duties in 2.3 (`doc-r1.md:73`) do not include serializing commands with a fixed output directory, which the cleanup-audit row requires ("one audit per worktree at a time", `doc-r1.md:85`). (R1.15, minor)

## 4. Adversarial analysis (Whittaker)
=== ADVERSARIAL ANALYSIS ===

- I can break this specification by **Sentinel Collision Attack**. The invariant at **WC-4 / 7.2 step 4** (`doc-r1.md:62,183`) fails when **a command that already writes a contract keeps its own `status` vocabulary, as WC-4 tells it to ("keep their fields and add the missing ones")**. Concrete attack: `/sc:workflow` writes `status: success | partial | failed` (`sk/sc-workflow-protocol/refs/return-contract.md:7`); `/sc:reflect` writes `success | partial | failed | dry-run` (`sk/sc-reflect-protocol/SKILL.md:665`); `/sc:adversarial` writes `"success"` (`sk/sc-adversarial-protocol/SKILL.md:436`). Before: workflow succeeds, contract `status: success`. After: 7.2 step 4 asserts `d['status'] in {'succeeded','partial','failed','blocked'}` and fails on a good run; WC-5 maps `success` and `dry-run` to `succeeded` only through its "otherwise" branch. Renaming the value instead breaks today's readers of those contracts, which SA-1 forbids (`doc-r1.md:146`). (R1.16)
- I can break this specification by **Divergence Attack**. The invariant at **AC-2.2** (`doc-r1.md:200`) fails when **the worker takes WC-3's optional branch ("the session may instead ask the coordinator", `doc-r1.md:61`)**. Concrete attack: `/sc:tdd "auth" --unattended` hits the topic gate; the worker asks; 7.2 step 3 waits on `question` too (`doc-r1.md:182`) and the coordinator answers; the worker re-runs and ends `succeeded`. Expected `--outcome failed` and `status: blocked` never appear, so AC-2.2 passes or fails by the worker's choice, not by the command's behaviour. (R1.5)
- I can break this specification by **Sequence Attack**. The invariant at **WC-3 + WC-6 + WC-4** (`doc-r1.md:61-64`) fails when **a blocked run is re-invoked after an answer**. Concrete attack: `/sc:analyze ... --unattended --output D` writes `D/return-contract.yaml` with `status: blocked`; after `ask`, the worker re-runs. Under WC-6 the re-run uses a fresh directory D2, so the final contract is `D2/return-contract.yaml`, and 7.2 step 3's pass rule "its report path is the WC-4 contract path" fails; if it reuses D, WC-6 is broken and a stale artifact list from the first run can remain. (R1.6)
- I can break this specification by **Accumulation Attack**. The invariant at **7.2 step 6** (`doc-r1.md:185`) fails when **a second live check runs in the same worktree**. Concrete attack: AC-1.2 runs 7.2 for nine P1 commands (`doc-r1.md:196`); after the first, its output directory stays untracked and not ignored (`git check-ignore` printed nothing), so command two's `git status --short` lists `?? <first output dir>/` and step 6 fails. Parallel workers share the worktree by default (`orca-capabilities.md:115`), which makes it worse. (R1.7)
- I can break this specification by **Zero/Empty Attack**. The invariant at **AC-C5** (`doc-r1.md:176`) fails when **an edit deletes a blank line or a line that starts with `-`**: `grep -E '^-[^-]'` matches neither `-` alone nor `--...`, so a non-additive edit prints nothing. (R1.13, minor)
- I can break this specification by **Divergence Attack**. The invariant at **the tasklist row** (`doc-r1.md:122`) fails when **Stage 10.5 always passes `--remediate`** (`sk/sc-tasklist-protocol/SKILL.md` Stage 10.5 command block) and the headless rule "MUST auto-accept and author the corrective artifact" (`sk/sc-reflect-protocol/refs/remediation-handoff.md`, headless section): an unattended tasklist run can author up to N remediation packages outside its output directory, which the row does not list as documented artifacts for 7.2 step 6. (R1.14, minor; how many packages appear depends on the registers found, UNVERIFIED)

## 5. Guard Condition Boundary Table
Guards found: WC-5 outcome mapping on the contract `status` (`doc-r1.md:63`) and WC-10 wait size (`doc-r1.md:68`). Other conditions in the spec (phase gating, D1-D5) are process rules, not value guards.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| WC-5 status mapping | WC-5, `doc-r1.md:63` | Zero/Empty | contract absent, or `status` empty | failed | "or no report exists" → `--outcome failed` (empty `status` also fails 7.2 step 4) | OK |
| WC-5 status mapping | WC-5, `doc-r1.md:63` | One/Minimal | `blocked` | failed | `--outcome failed` | OK |
| WC-5 status mapping | WC-5, `doc-r1.md:63` | Typical | `succeeded` | succeeded | `--outcome succeeded` | OK |
| WC-5 status mapping | WC-5, `doc-r1.md:63` | Maximum/Overflow | `partial` | succeeded | `--outcome succeeded`, body states `partial` | OK |
| WC-5 status mapping | WC-5, `doc-r1.md:63` | Sentinel Value Match | `success` / `dry-run` (existing contracts keep these, WC-4) | succeeded via "otherwise" | WC-5 maps it, but 7.2 step 4 rejects it; the spec does not say whether the old value is renamed or kept | GAP (R1.16) |
| WC-5 status mapping | WC-5, `doc-r1.md:63` | Legitimate Edge Case | audit report with verdict FAIL, `status: succeeded` | succeeded | "including an audit whose verdict is FAIL" | OK |
| WC-10 wait size | WC-10, `doc-r1.md:68` | Zero/Empty | no long wait | n/a | heartbeat every 5 minutes only | OK |
| WC-10 wait size | WC-10, `doc-r1.md:68` | One/Minimal | one 60 s poll | under limit | no split | OK |
| WC-10 wait size | WC-10, `doc-r1.md:68` | Typical | 600 s pr-submit budget over iterations | per-iteration | each iteration under 4 min (iteration time UNVERIFIED, item 12) | OK |
| WC-10 wait size | WC-10, `doc-r1.md:68` | Maximum/Overflow | 3600 s eval | over limit | split into waits of at most 4 minutes | OK |
| WC-10 wait size | WC-10, `doc-r1.md:68` | Sentinel Value Match | exactly 5 min single call | over 4 min | split (4 min cap) | OK |
| WC-10 wait size | WC-10, `doc-r1.md:68` | Legitimate Edge Case | one parallel Agent-tool call of unknown length | not covered | WC-10 names only poll waits and evals; duration UNVERIFIED | OK (note R1.10) |

FR-8: the one GAP row is R1.16, graded MAJOR with a concrete outcome. FR-9: no blank Specified Behavior cell. FR-10: table complete.

## 6. Numbered findings list
Severity is the panel label; "Blocking" is what the diffgate script derives from the findings block (CRITICAL, FR-8/9, or MAJOR with an outcome). Expected result: 10 blocking findings, so the derived result should be FAIL; the verdict line itself is appended by the coordinator's `check` step, not written here.

| # | Finding | Severity | Blocking | Spec section | Evidence (path:line) |
|---|---|---|---|---|---|
| R1.1 | AC-1.1 requires a `return-contract.yaml` Unattended section on every 3.1-3.2 command, but `/sc:load` gets no report and the Decisions table forbids one. | MAJOR | yes | 7.3 AC-1.1; 3.2 load row; Decisions | `doc-r1.md:195`, `doc-r1.md:112`, `doc-r1.md:265` |
| R1.2 | P1 makes every command accept `--unattended` but defines it only for commands with no gate; AC-1.1 forces the section onto P2-P4 commands at P1, so `/sc:auggie-review --unattended` still posts to GitHub until P2, breaking WC-9. | MAJOR | yes | 6 (P1 row); 7.3 AC-1.1; WC-9 | `doc-r1.md:159`, `doc-r1.md:195`, `doc-r1.md:67`, `doc-r1.md:162`; `src/superclaude/commands/auggie-review.md:51` |
| R1.3 | `/sc:workflow` cannot meet WC-4: it has no output flag (`--output` raises `E-LEGACY`) and its contract lands in a run-timestamped package, so the path is not known before dispatch; the row adds no fix. | MAJOR | yes | 2.2 WC-4; 3.1 workflow row; 7.2 step 3 | `doc-r1.md:62`, `doc-r1.md:92`, `doc-r1.md:182`; `src/superclaude/commands/workflow.md:12,42`; `src/superclaude/skills/sc-workflow-protocol/SKILL.md:24,66` |
| R1.4 | The adversarial fix names `<output>/adversarial/return-contract.yaml`, not the WC-4 path `<output-dir>/return-contract.yaml`. | MAJOR | yes | 3.1 adversarial row; WC-4 | `doc-r1.md:83`, `doc-r1.md:62` |
| R1.5 | AC-2.2 expects `blocked` / `failed`, but WC-3 lets the worker ask and re-run instead, so the check's result depends on the worker's choice. | MAJOR | yes | 7.3 AC-2.2; WC-3; 7.2 step 3 | `doc-r1.md:200`, `doc-r1.md:61`, `doc-r1.md:182` |
| R1.6 | After a WC-3 answer the re-run's output directory is undefined: WC-6 says fresh directory, WC-4 says the brief's directory. | MAJOR | yes | 2.2 WC-3, WC-4, WC-6 | `doc-r1.md:61`, `doc-r1.md:62`, `doc-r1.md:64` |
| R1.7 | 7.2 step 6 (`git status --short` shows only this brief's output) fails on every live check after the first in the same worktree, because earlier output stays untracked and not ignored. | MAJOR | yes | 7.2 step 6; AC-1.2 | `doc-r1.md:185`, `doc-r1.md:196`; `.dev/orca-command-refactor/inventory/orca-capabilities.md:115`; `git check-ignore` run in section 1 |
| R1.8 | P0 adds an Orca section to `HOW-WE-WORK.md` and an Orca-facing `WORKER-CONTRACT.md` in `src/superclaude/core`, which AC-C1 scans for `orca orchestration ...`; the spec gives no rule for writing them without those words, so AC-C1 fails. | MAJOR | yes | 6 (P0 row); 7.1 AC-C1; SA-2 | `doc-r1.md:158`, `doc-r1.md:172`, `doc-r1.md:147`, `doc-r1.md:61-70` |
| R1.9 | WC-7 does not require invoking the command's skill with the Skill tool; AC-0.4 checks only for no Agent wrapper, so a worker that reads the command file and works from memory passes, although the repo calls that a violation. | MAJOR | yes | 2.2 WC-7; 7.3 AC-0.4 | `doc-r1.md:65`, `doc-r1.md:194`; `CLAUDE.md:9-11` |
| R1.10 | WC-10 splits only poll waits and evals; a long parallel Agent-tool call inside a fan-out command cannot heartbeat (length UNVERIFIED). | MINOR | no | 2.2 WC-10 | `doc-r1.md:68`; `.dev/orca-command-refactor/inventory/orca-capabilities.md:130` |
| R1.11 | WC-1 has no phase scope and no acceptance check. | MINOR | no | 2.2 WC-1; 6; 7 | `doc-r1.md:59`, `doc-r1.md:158-162` |
| R1.12 | Section 2.1 calls `--unattended` the only command-side change besides reports and resume, but WC-9, WC-10, WC-11 are also command-owned. | MINOR | no | 2.1 | `doc-r1.md:51`, `doc-r1.md:67-69` |
| R1.13 | AC-C5's `grep -E '^-[^-]'` misses a deleted blank line or a deleted line starting with `-`. | MINOR | no | 7.1 AC-C5 | `doc-r1.md:176` |
| R1.14 | Unattended tasklist always runs reflect with `--remediate`; the headless rule then authors remediation packages outside the output directory, not listed as documented artifacts. | MINOR | no | 3.2 tasklist row; 7.2 step 6 | `doc-r1.md:122`; `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` Stage 10.5; `src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md` headless section |
| R1.15 | Coordinator duties (2.3) omit serializing fixed-directory commands such as cleanup-audit. | MINOR | no | 2.3; 3.1 cleanup-audit row | `doc-r1.md:73`, `doc-r1.md:85` |
| R1.16 | Existing contracts use `status: success` (and `dry-run`); WC-4 keeps existing fields, 7.2 step 4 accepts only `succeeded/partial/failed/blocked`, so good runs fail the check, and renaming breaks today's readers (SA-1). Guard-table GAP (FR-8). | MAJOR | yes | 2.2 WC-4, WC-5; 7.2 step 4; Decisions (status vocabulary) | `doc-r1.md:62`, `doc-r1.md:183`, `doc-r1.md:262`; `src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md:7`; `src/superclaude/skills/sc-reflect-protocol/SKILL.md:665`; `src/superclaude/skills/sc-adversarial-protocol/SKILL.md:436` |

### Self-audit of what holds
Checked and found sound: the 43-command count and 10/27/6 split (`doc-r1.md:76`; 27 rows counted in 3.2); E5's Orca grep (only `sk/ccsession-tag/`); AC-C1 prints nothing today; troubleshoot's offer loads only with `--fix` (`sk/sc-troubleshoot-protocol/refs/remediation-handoff.md:3,14`), so the P0 smoke run without `--fix` has no stall; brainstorm auto-proceeds without `--interactive` (`sk/sc-brainstorm-protocol/SKILL.md:134`); the pr-submit top-level rule (`sk/sc-pr-submit-protocol/SKILL.md:37`); `CLAUDE.md:16,50,72-83` as cited; the depth-1 facts (`orca-capabilities.md:97-103`).

## 7. Decisions
| Decision | Options considered | Rationale |
|---|---|---|
| Grade the WC-10 fan-out gap minor | major; minor | The length of a single Agent-tool call was not measured and Orca does not stop a worker for missing heartbeats (`orca-capabilities.md:125,130`), so no verified wrong outcome. |
| Grade R1.8 blocking | minor (wording); major with outcome | A routing section about dispatching workers naturally names `orca orchestration worker-start`, and AC-C1 then fails every phase; the spec gives no rule that prevents it. |
| Keep R1.3 and R1.4 separate | merge as "WC-4 path drift"; keep separate | They need different fixes (workflow has no output flag at all; adversarial only names a different subfolder). |
| Use `R1.<j>` ids in prose and the numbered list | separate `F<n>` ids; diffgate ids | One id per finding, matching the findings block the script reads. |
| Record the R1.16 GAP as `fr=8` | major with outcome only; fr=8 | The command's FR-8 rule makes a GAP row a MAJOR finding at minimum; tagging it lets the script count it. |

## 8. UNVERIFIED items
1. Whether one parallel Agent-tool call in a fan-out command (tdd, adversarial, troubleshoot Tier 2) exceeds 5 minutes (R1.10).
2. How many remediation packages an unattended tasklist run authors; it depends on which reflect registers are found (R1.14).
3. Whether a `/sc:` line inside an Orca preamble is ever expanded as a slash command; in this worker's own session it was not, and the command loaded only through a Skill tool call (R1.9).
4. Whether every current reader of the workflow, reflect and adversarial contracts tests the literal `success` value; not traced (R1.16).

## Diffgate findings
FINDING R1.1 sev=major at=195 anchor="every command in sections 3.1-3.2 has a `## Unattended mode` section" outcome="P1 either fails AC-1.1 on /sc:load or adds the load report file the Decisions table rejects" :: AC-1.1 contradicts the load row and the Decisions table
FINDING R1.2 sev=major at=159 anchor="a no-op where a command has no gate" outcome="between P1 and P2 /sc:auggie-review --unattended is accepted and still posts a PR review with no prompt" :: P1 accepts --unattended on gated commands without defining it
FINDING R1.3 sev=major at=92 anchor="`.dev/tasks/to-do/<id>/return-contract.yaml`" outcome="the coordinator cannot name the workflow contract path in the brief, and passing --output to /sc:workflow stops it with E-LEGACY" :: workflow cannot meet the WC-4 known-before-dispatch path
FINDING R1.4 sev=major at=83 anchor="Fix the contract filename to `<output>/adversarial/return-contract.yaml`" outcome="a coordinator opening <output-dir>/return-contract.yaml per WC-4 finds no file and reports a successful adversarial run as failed" :: adversarial contract path differs from WC-4
FINDING R1.5 sev=major at=200 anchor="contract `status: blocked` with a non-empty `blocked_question`" outcome="AC-2.2 fails whenever the worker uses the WC-3 ask branch and the coordinator answers" :: AC-2.2 outcome depends on the optional WC-3 branch
FINDING R1.6 sev=major at=61 anchor="then re-invoke or resume the command with the answer as a flag" outcome="a re-run after ask writes its contract to a fresh directory, so 7.2 step 3 fails, or reuses the old directory and breaks WC-6" :: re-run directory after ask is undefined
FINDING R1.7 sev=major at=185 anchor="only files under the brief's output directory" outcome="every 7.2 live check after the first in one worktree fails step 6 on the earlier run's untracked output" :: git status step fails on prior runs' output
FINDING R1.8 sev=major at=158 anchor="add an Orca section to `HOW-WE-WORK.md`" outcome="an Orca routing section in src/superclaude/core naming orca orchestration worker-start makes AC-C1 print a line and fail every phase" :: P0 core Orca text conflicts with AC-C1
FINDING R1.9 sev=major at=65 anchor="The worker runs the command directly in its own session" outcome="a worker that reads the command file and works from memory without the Skill call passes AC-0.4" :: WC-7 omits the Skill-tool invocation
FINDING R1.10 sev=minor at=68 anchor="must be split into waits of at most 4 minutes" :: long single Agent-tool calls are not covered by WC-10
FINDING R1.11 sev=minor at=59 anchor="Launch setup, not commands" :: WC-1 has no phase or acceptance check
FINDING R1.12 sev=minor at=51 anchor="It is the only command-side change the contract asks for besides report files and resume" :: WC-9 to WC-11 are also command-side
FINDING R1.13 sev=minor at=176 anchor="prints nothing: edits are additive" :: AC-C5 grep misses deleted blank lines
FINDING R1.14 sev=minor at=122 anchor="Stage 10.5 passes `--unattended` to each reflect so the headless rule applies" :: unattended tasklist authors remediation packages outside its output
FINDING R1.15 sev=minor at=73 anchor="and the worktree placement" :: coordinator duties omit serializing fixed-directory commands
FINDING R1.16 sev=major at=62 anchor="Commands that already write a contract keep their fields and add the missing ones" outcome="a successful /sc:workflow run keeps status: success and fails the 7.2 step 4 status assertion" fr=8 :: existing status values collide with the WC-4 set
