# Spec panel review: orca-worker-contract-spec.md

review: 1 of 3

- Task: task_ad50c816d677 (Task 5, independent review). Reviewer did not write the spec.
- Command: `/sc:spec-panel-armb @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- Spec under review: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (286 lines, read in full 2026-11-09). Not edited.
- Repo root for this review: /home/coder/workspaces/worktrees/IronClaude/exp346-v-ponytail-r3
- Panel: Wiegers (lead, requirements), Adzic, Cockburn; Fowler (lead, architecture), Nygard, Newman, Hohpe; Whittaker (always active).

## 1. Evidence checks run by the reviewer
All checks were read-only and run on 2026-11-09 in this worktree. "Holds" means the spec's claim matched what was on disk.

| # | Check | Result |
|---|---|---|
| V1 | `ls src/superclaude/commands/*.md` | 44 files: 43 commands plus `README.md`. The spec's count of 43 (spec:76) holds. |
| V2 | `grep -rlni orca src/superclaude/{commands,skills,core,agents}` | Only files under `src/superclaude/skills/ccsession-tag/`. E5 (spec:25) holds. |
| V3 | AC-C1 grep (spec:172), run with plain `\|` alternation | Prints nothing today, so the check is green at baseline. |
| V4 | `CLAUDE.md` lines 16, 50, 74, 76, 83, 157, 334, 408 | All exist (file has 447 lines) and say what the spec cites. |
| V5 | `ls /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs` | No such directory. The spec's stated repo root (spec:4) does not exist on this machine; its repo-relative paths do resolve in this worktree. |
| V6 | `Makefile:109-165` (`sync-dev` target) | Copies skills, agents, commands, hooks and templates; no line mentions `core`. Core files reach `~/.claude/` only through `superclaude install` (`src/superclaude/cli/install_core.py:4,33`). |
| V7 | `src/superclaude/cli/install_core.py:13-24` | `KNOWN_CORE_FILES` exists and does not yet list `WORKER-CONTRACT.md`. Spec:52 holds. |
| V8 | Existing return-contract `status` values | `success \| partial \| failed` at `src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md:7`; `success \| partial \| failed \| dry-run` at `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:341` and `src/superclaude/skills/sc-reflect-protocol/SKILL.md:665`; `status: "success"` at `src/superclaude/skills/sc-adversarial-protocol/SKILL.md:436`. None uses `succeeded`. |
| V9 | `src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md:3,39` | Contract path is `.dev/tasks/to-do/<id>/return-contract.yaml`; STOPs before the package exists, including `E-LEGACY` "including retired `--output`", write "no package directory, no yaml". |
| V10 | `src/superclaude/skills/sc-adversarial-protocol/SKILL.md:425-429` | "MUST write this return contract on every invocation, including failures". Holds. |
| V11 | Diff filter used by AC-C5 and AC-0.3 (`grep -E '^-[^-]'`) fed a diff that deletes `- a deleted bullet`, an empty line and `--flag deleted` | `grep` printed nothing (exit 1): all three deletions pass as "additive". |
| V12 | `pyproject.toml:38` | `"pyyaml>=6.0",`. Holds. |
| V13 | `src/superclaude/core/CLAUDE.md:65`, `src/superclaude/core/HOW-WE-WORK.md:22` | Both state the hard limit. Holds. |
| V14 | `.dev/evals/ccsession-orca-e2e-20261026/EVIDENCE.md:39,56` | The failing probe used a 45-second limit; "Raising `CCSESSION_ASK_TIMEOUT` above about 45 seconds would make supervised workers fail again". |
| V15 | `.dev/orca-command-refactor/inventory/orca-capabilities.md` lines 40-189, read in full | `--retry-of` restarts the same Task (`CAPS:116`); heartbeat use in the liveness verdict is UNVERIFIED (`CAPS:130`); release never happens on a heartbeat signal (`CAPS:111`). |

## 2. Requirements analysis
=== REQUIREMENTS ANALYSIS === (Wiegers lead, Adzic, Cockburn). Finding numbers refer to section 7.

**Wiegers (requirements quality).** The decision (spec:13-45) is well argued and its evidence gaps are stated honestly (spec:41-45). The weak point is that several requirements contradict either the code they build on or the acceptance checks meant to verify them, so an implementer cannot satisfy both:
- WC-4 fixes a four-value status set `succeeded / partial / failed / blocked` (spec:62) and tells commands that already write a contract to "keep their fields" (spec:62). Every existing contract uses `success` (V8). 7.2 step 4 then asserts `status in {'succeeded',...}` (spec:183), so a command that obeys "keep their fields" fails the check. Finding 1.
- WC-4 says the contract path is `<output-dir>/return-contract.yaml`, "known before dispatch" (spec:62, 73). Section 3 then names different shapes: `<output>/adversarial/return-contract.yaml` (spec:83), a generated package path for workflow (spec:92), a `--output <file>` for tdd and init-lite (spec:87, 90), a fixed `.claude-audit/` for cleanup-audit (spec:85). Workflow refuses `--output` outright (V9). Finding 2.
- P1 adds `--unattended` to every section 3 command "a no-op where a command has no gate" (spec:159), and AC-1.1 requires each to carry a `## Unattended mode` section (spec:195), but gates are converted only in P2-P4 (spec:160-162). The spec never says what `--unattended` does in P1-P3 for a command whose gate is still live. Finding 4.
- WC-1 and WC-12 have no phase that implements them and no acceptance check (spec:59, 70, 158-162, 178-210). Finding 14.

**Adzic (specification by example).** The acceptance checks are concrete and runnable, which is the spec's strongest part. Three examples do not hold when executed:
- Given a command-file edit that deletes a markdown bullet, When AC-C5 runs `grep -E '^-[^-]'` (spec:176), Then it prints nothing and the edit passes as additive (V11). The same filter guards routing rows in AC-0.3 (spec:193). Finding 6.
- Given the AC-C1 command copied from the spec's markdown source (spec:172), When it runs, Then GNU grep 3.11 reads `\|` as a literal pipe and the pattern matches nothing, so the check can never fail (reviewer test: `grep -cE '...(orchestration\|worktree...)'` printed `0` on a line containing `orca worktree`; with plain `|` it printed `1`). AC-C4 and AC-0.3 carry the same table escape inside shell pipelines (spec:175, 193). Finding 7.
- Given a P2 gate-trigger run (AC-2.2, spec:200), When the worker takes the WC-3 route the spec allows ("may instead ask the coordinator", spec:61), Then a `question` arrives in 7.2 step 3 (spec:182) and the check gives the coordinator no rule for answering it; the expected `--outcome failed` / `status: blocked` result is not determined. Finding 9.

**Cockburn (actors and goals).** Actors are clear: coordinator (goal: plan and read reports), worker session (goal: run one command and report), command (goal: do the unit of work), person (goal: unchanged standalone use, section 5). The coordinator's obligations (spec:72-73) are good. Two actor goals are under-specified:
- The retry actor. `worker-start --retry-of` restarts the same Task (`CAPS:116`), so the retry worker receives the same brief and the same `--output <dir>`. WC-6 asks for "a fresh output directory so a re-run starts clean" (spec:64) while WC-4 requires the path to be known before dispatch (spec:62). No actor owns choosing the fresh directory. Finding 3.
- The installer actor. Live checks (spec:178-186) exercise commands as a worker loads them, but no step says who runs `make sync-dev` or `superclaude install` before a live check, and the new core file only reaches `~/.claude/` through `superclaude install` (V6). Finding 5.

## 3. Architecture analysis
=== ARCHITECTURE ANALYSIS === (Fowler lead, Nygard, Newman, Hohpe).

**Fowler (interfaces and boundaries).** The boundary is sound: commands stay Orca-free units of work, the worker session owns lifecycle messages, the coordinator owns fan-out (spec:16, 65-66). The rejected alternative is rejected for verified reasons (R1-R5, spec:33-37; depth 1 at `CAPS:97-98`). The weak interface is the one the whole design rests on, the return contract:
- Its status vocabulary conflicts with existing producers (Finding 1) and its location is not one rule (Finding 2), so the coordinator cannot read every worker "the same way", which is the stated reason for reusing the file (spec:261).
- It carries no version field, while the workflow contract already declares `contract_version: "1.1"` (`src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md:6`). With 37 producers changing over four phases, the coordinator has no way to tell an old contract from a new one. Finding 16.
- Single source of truth: shared rules live once in `~/.claude/WORKER-CONTRACT.md` with per-command sections that point to it (spec:52). Good, and it follows the installed-path rule (`CLAUDE.md:74-83`).

**Nygard (failure modes).** Readiness, stalls and outward actions are handled with care (spec:44, 59-60, 67). Gaps:
- Retry corrupts the first attempt (Finding 3): the circuit breaker allows up to three attempts per Task (`CAPS:80`, `CAPS:116`), each writing into the same `<output-dir>` if the command has no resume flag.
- The liveness rule (WC-10, spec:68) covers Bash waits only. A command's own foreground Agent-tool fan-out, which WC-7 keeps (spec:65), blocks the top-level session for one tool call of unbounded length, and subagents may not heartbeat. The spec says nothing about it. Whether Orca acts on heartbeat age is UNVERIFIED (`CAPS:130`), and release never happens on a heartbeat signal (`CAPS:111`), so the harm is a coordinator that cannot tell a long fan-out from a hang, not a killed worker. Finding 11.
- Malformed or empty contract (Finding 10): WC-5 maps only "no report exists" to `failed` (spec:63). A truncated YAML from a crash mid-write is a likely failure mode and has no mapping.

**Newman (evolution and compatibility).** Standalone compatibility (section 5, spec:141-151) is the best-specified part: opt-in flag, additive edits, SA-3 no new files without the flag. Two compatibility risks:
- Phased rollout exposes a half-converted interface: in P1-P3 every command accepts `--unattended`, but the changes for the 22 commands scheduled in P2-P4 (spec:160-162) have not landed, including every gate conversion (Finding 4). A coordinator that trusts the flag stalls a worker on a live prompt, which the spec itself says is invisible (spec:44, 60).
- Changing existing contract `status` values from `success` to `succeeded` would break current consumers such as `/sc:reflect`, which branches on `status: success` from workflow (`src/superclaude/skills/sc-reflect-protocol/SKILL.md:334`). Finding 1 must be fixed by mapping, not by renaming.

**Hohpe (message exchange).** The exchange is request (brief) then one completion message with a pointer to a file (spec:62-63, 73), plus pull-only follow-ups (spec:70). It is clean. Two exchange gaps:
- The ask/reply sub-exchange has no bound: WC-3 resumes the same message ID after each timeout (spec:61) with no limit on resumes, and no rule for what the coordinator does with a gate-trigger question during acceptance testing. Finding 9.
- The retry message carries the same payload as the first attempt (`CAPS:116`), so any per-run variation (fresh directory) must come from the worker or command, which the spec does not assign. Finding 3.

## 4. Adversarial analysis (Whittaker)
Severity uses the panel scale. Each attack names its section 7 finding.

1. **Sentinel Collision Attack (Finding 1).** I can break this specification by **Sentinel Collision**. The invariant at **WC-4 / 7.2 step 4 (spec:62, 183)** fails when **an existing producer keeps its field values as WC-4 instructs**. Concrete attack: P1 adds `command` and `report_path` to the workflow contract and keeps `status: success` (`refs/return-contract.md:7`). Before: contract valid for `/sc:reflect`. 7.2 step 4 runs `assert d['status'] in {'succeeded','partial','failed','blocked'}`: AssertionError. After: a successful workflow worker fails AC-1.2, or, if the implementer renames the value, `/sc:reflect`'s `status: success` branch (`sc-reflect-protocol/SKILL.md:334`) stops matching. CRITICAL.
2. **Divergence Attack (Finding 2).** I can break this specification by **Divergence**. The invariant at **WC-4 "known before dispatch" (spec:62)** fails when **the command is workflow**. Concrete attack: coordinator follows 2.3 and passes the output directory as `--output .dev/x/`; workflow STOPs with `E-LEGACY` and writes "no package directory, no yaml" (`refs/return-contract.md:39`). If the coordinator instead omits `--output` (spec:92 row), the contract lands in `.dev/tasks/to-do/<id>/` where `<id>` is generated at run time, so 7.2 step 3 ("its report path is the WC-4 contract path", spec:182) cannot be checked before the run. CRITICAL.
3. **Sequence Attack (Finding 3).** I can break this specification by **Sequence (repeat)**. The invariant at **WC-6 (spec:64)** fails when **attempt 1 of a Task fails and the coordinator retries with `--retry-of`**. Concrete attack: Task spec carries `/sc:analyze src/x --unattended --output .dev/a/`. Attempt 1 writes `.dev/a/report.md` and dies before the contract. Attempt 2 is the same Task (`CAPS:116`), so the same `--output .dev/a/`; it overwrites `.dev/a/report.md`. Before: attempt-1 evidence on disk. After: gone, and no "fresh output directory" was ever chosen because no actor owns that choice. MAJOR (names a concrete wrong outcome).
4. **Sequence Attack, skipped step (Finding 4).** I can break this specification by **Sequence (skip)**. The invariant at **WC-2 (spec:60)** fails when **a coordinator dispatches a P2 command after P1 but before P2**. Concrete attack: after P1, `cmd/tdd.md` has a `## Unattended mode` section (AC-1.1, spec:195) and accepts `--unattended` as a no-op. Coordinator dispatches `/sc:tdd "auth" --unattended --output f.md`; the topic-only clarification (spec:90) still fires; the worker parks on a prompt, "healthy, not failed" (`CAPS:129`). MAJOR.
5. **Zero/Empty Attack (Finding 10).** I can break this specification by **Zero/Empty**. The invariant at **WC-5 (spec:63)** fails when **the contract file exists but is empty or truncated**. Concrete attack: the command crashes mid-write; `return-contract.yaml` is 0 bytes. WC-5 covers "no report exists" only; the worker has no rule, may read the absent status as "otherwise" and send `--outcome succeeded`. MAJOR (FR-8 GAP).
6. **Accumulation Attack (Finding 9).** I can break this specification by **Accumulation**. The invariant at **WC-3 (spec:61)** fails when **the coordinator never answers**. Concrete attack: each `ask` times out after 600 s, the worker resumes the same ID, forever; no heartbeat is sent while in `ask` (spec:61), so the Dispatch neither completes nor fails. MAJOR (FR-8 GAP).
7. **Accumulation Attack (Finding 11).** I can break this specification by **Accumulation**. The invariant at **WC-10 (spec:68)** fails when **a command's own Agent-tool fan-out runs in the foreground for longer than 5 minutes**. Concrete attack: a P0 smoke-run command (spec:158) runs its own Agent-tool fan-out, which the spec keeps (spec:24, 65); the top-level session sits inside one foreground Agent tool call for, as an example, 12 minutes; WC-7 forbids the subagents from heartbeating (spec:65); heartbeats stop for 12 minutes. MAJOR (FR-8 GAP).
8. **Zero/Empty Attack on the checks (Findings 6, 7).** I can break this specification by **Zero/Empty**. The invariants at **AC-C5, AC-0.3 and AC-C1 (spec:172, 176, 193)** fail when **the filter matches nothing by construction**. Concrete attack: a P2 edit deletes any markdown bullet line `- <text>` from a command file; the diff line is `-- <text>`; `^-[^-]` does not match (V11); AC-C5 passes. Separately, AC-C1 copied from the raw spec keeps `\|` and returns `0` matches even on `orca worktree` (section 2, Adzic). MAJOR.
9. **Divergence Attack (Finding 8).** I can break this specification by **Divergence**. The invariant at **SA-2 vs AC-C1 (spec:147, 172)** fails when **the P0 implementer uses the one Orca mention SA-2 allows**. Concrete attack: `src/superclaude/core/WORKER-CONTRACT.md` shows `orca orchestration ask --question ...` as the caller's question channel (SA-2 permits it; WC-3 needs it). AC-C1 scans `src/superclaude/core` and matches that line: P0 fails its own common check. MAJOR.

Assumptions Whittaker flags for downstream use: (A1) every existing contract can absorb the WC-4 enum (false, V8); (A2) one `--output` flag spelling works for all commands (false for workflow, V9); (A3) the same brief can be retried safely (unassigned, `CAPS:116`); (A4) the worker loads the edited primitives (unstated, V6).

## 5. Guard Condition Boundary Table
Built by Nygard, checked for completeness by Crispin's rule (six input rows per guard), attacked by Whittaker. Every GAP row becomes a MAJOR finding under FR-8 and is listed in section 7.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G1 contract status to outcome | WC-5, spec:63 | Zero/Empty | contract file absent | failed | "or no report exists" → `--outcome failed` | OK |
| G1 contract status to outcome | WC-5, spec:63 | One/Minimal | file exists, 0 bytes or no `status` key | unknown | not specified | GAP (Finding 10) |
| G1 contract status to outcome | WC-5, spec:63 | Typical | `status: succeeded` | succeeded | `--outcome succeeded` | OK |
| G1 contract status to outcome | WC-5, spec:63 | Maximum/Overflow | `status: blocked` with `blocked_question` | failed | `--outcome failed` | OK |
| G1 contract status to outcome | WC-5, spec:63 | Sentinel Value Match | `status: success` (existing producers, V8) | unknown | WC-4 says keep existing fields; 7.2 step 4 rejects the value | GAP (Finding 1) |
| G1 contract status to outcome | WC-5, spec:63 | Legitimate Edge Case | `status: partial`; audit verdict FAIL | succeeded | `--outcome succeeded`, body states status and verdict | OK |
| G2 single blocking call length | WC-10, spec:68 | Zero/Empty | 0 s call | no split | nothing required | OK |
| G2 single blocking call length | WC-10, spec:68 | One/Minimal | 1 s Bash call | no split | nothing required | OK |
| G2 single blocking call length | WC-10, spec:68 | Typical | 3 min Bash poll | no split | allowed; heartbeat every 5 min | OK |
| G2 single blocking call length | WC-10, spec:68 | Maximum/Overflow | 60 min eval wait (`sk/sc-cli-eval-protocol/SKILL.md:151-152` via spec:68) | split | split into waits of at most 4 min | OK |
| G2 single blocking call length | WC-10, spec:68 | Sentinel Value Match | foreground Agent-tool call over 5 min | unknown | not specified; WC-7 keeps the fan-out and forbids subagent heartbeats | GAP (Finding 11) |
| G2 single blocking call length | WC-10, spec:68 | Legitimate Edge Case | call between 4 and 5 min | no split | allowed; with other work the 5 min heartbeat can slip, but the rule is explicit | OK |
| G3 launch prompt fallback | WC-1, spec:59 | Zero/Empty | no launch prompt | ready | nothing required | OK |
| G3 launch prompt fallback | WC-1, spec:59 | One/Minimal | fallback 1 s | ready | passes | OK |
| G3 launch prompt fallback | WC-1, spec:59 | Typical | fallback 30 s (`EVIDENCE.md:45`) | ready | passes | OK |
| G3 launch prompt fallback | WC-1, spec:59 | Maximum/Overflow | no fallback | fails `agent_readiness` | forbidden | OK |
| G3 launch prompt fallback | WC-1, spec:59 | Sentinel Value Match | fallback 50 s with the 60 s default | unknown | "well inside the readiness limit": no number; `EVIDENCE.md:56` says above about 45 s fails | GAP (Finding 12) |
| G3 launch prompt fallback | WC-1, spec:59 | Legitimate Edge Case | coordinator raises `--timeout-ms` (`CAPS:45`) | ready | limit scales; "well inside" still unquantified | OK (covered by the GAP row above) |
| G4 ask resume | WC-3, spec:61 | Zero/Empty | no gate hit | no ask | nothing required | OK |
| G4 ask resume | WC-3, spec:61 | One/Minimal | one ask, answered | resume with flag | re-invoke or resume the command with the answer | OK |
| G4 ask resume | WC-3, spec:61 | Typical | one timeout then answer | resume same ID | resume same message ID | OK |
| G4 ask resume | WC-3, spec:61 | Maximum/Overflow | coordinator never answers | unbounded | resume forever; no limit, no fallback to `blocked` | GAP (Finding 9) |
| G4 ask resume | WC-3, spec:61 | Sentinel Value Match | answer arrives after the command already wrote `status: blocked` into `<output-dir>` | re-invoke | re-invocation into the same directory is not reconciled with WC-6 fresh-directory rule | GAP (Finding 9) |
| G4 ask resume | WC-3, spec:61 | Legitimate Edge Case | AC-2.2 gate-trigger run | ask or block | worker may choose either; expected test result assumes block | GAP (Finding 9) |
| G5 retry safety | WC-6, spec:64 | Zero/Empty | first attempt, empty output dir | fresh | runs | OK |
| G5 retry safety | WC-6, spec:64 | One/Minimal | retry, command has a resume flag | resume | resume from on-disk state | OK |
| G5 retry safety | WC-6, spec:64 | Typical | retry, no resume flag, same Task brief (`CAPS:116`) | fresh dir required | no actor chooses the fresh dir; same `--output` reused | GAP (Finding 3) |
| G5 retry safety | WC-6, spec:64 | Maximum/Overflow | third failed attempt | circuit breaks | Orca fails the Task (`CAPS:116`) | OK |
| G5 retry safety | WC-6, spec:64 | Sentinel Value Match | retry finds attempt-1 `return-contract.yaml` | unknown | overwrite vs keep not specified | GAP (Finding 3) |
| G5 retry safety | WC-6, spec:64 | Legitimate Edge Case | person reruns standalone | unchanged | SA-1 keeps today's behaviour | OK |
| G6 outward default | WC-9, spec:67 | Zero/Empty | no authorization in brief | off | every outward default off | OK |
| G6 outward default | WC-9, spec:67 | One/Minimal | one explicit flag, e.g. `--post-pr` | on for that action | on only through that flag | OK |
| G6 outward default | WC-9, spec:67 | Typical | `/sc:auggie-review --unattended` | off | implies `--no-post-pr` (spec:100) | OK |
| G6 outward default | WC-9, spec:67 | Maximum/Overflow | brief authorizes everything | on | per D4 (spec:244-247) | OK |
| G6 outward default | WC-9, spec:67 | Sentinel Value Match | standalone run with no `--unattended` | today's default | SA-1 keeps posting default | OK |
| G6 outward default | WC-9, spec:67 | Legitimate Edge Case | `/sc:task` EXEMPT `commit` | refused unless authorized | spec:121 | OK |

Table complete: six guards, 36 rows, every cell filled. Synthesis may proceed.

## 6. Quality scores
| Dimension | Score (0-10) | Basis |
|---|---|---|
| Clarity | 8 | Plain requirement table with owners (spec:57-70); decisions and open questions are self-contained (spec:224-269). |
| Completeness | 6 | All 43 commands classified (V1); missing: contract versioning, retry directory owner, install step, malformed-contract mapping, Agent-tool liveness. |
| Testability | 5 | Checks are concrete, but three of them cannot fail as written (Findings 6, 7) and one contradicts a requirement (Finding 8). |
| Consistency | 5 | WC-4 conflicts with existing contracts (Finding 1), with section 3 paths (Finding 2) and with WC-6 under retry (Finding 3). |
| Overall | 6.0 | The decision is sound; the worker contract needs one revision pass before Phase 1 can be planned. |

Expert consensus: the architecture decision (Orca on top, commands Orca-free) is supported by verified evidence and should stand. Disagreement: Nygard would grade the Agent-tool liveness gap (Finding 11) as minor because Orca never releases a worker on heartbeat age (`CAPS:111`); it stays blocking only because the FR-8 rule makes every boundary-table GAP at least MAJOR and FR-8 findings blocking.

## 7. Numbered findings
Grading follows this command's review loop: CRITICAL and FR-8/FR-9 findings are blocking; a MAJOR is blocking only when it names a concrete wrong outcome; MINOR is a note. Spec line numbers are `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:N`, written `spec:N`.

| # | Finding | Severity | Blocking | Spec section | Evidence (path:line) |
|---|---|---|---|---|---|
| 1 | WC-4 fixes `status` to `succeeded/partial/failed/blocked` and tells existing producers to keep their fields, but every existing contract uses `success`, so 7.2 step 4 rejects a correct workflow, brainstorm, reflect or adversarial contract; renaming the value instead breaks `/sc:reflect`, which branches on `status: success`. Recommendation: define a mapping (`success` counts as `succeeded`) in WC-4 and in the step-4 assert, and keep producers unchanged. Priority High. | CRITICAL | yes | 2.2 WC-4; 7.2 step 4 | spec:62, spec:183; `src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md:7`; `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:341`; `src/superclaude/skills/sc-reflect-protocol/SKILL.md:334,665`; `src/superclaude/skills/sc-adversarial-protocol/SKILL.md:436` |
| 2 | The contract location is not one rule and is not always known before dispatch: WC-4 says `<output-dir>/return-contract.yaml`, but section 3 plans `<output>/adversarial/return-contract.yaml`, keeps workflow's generated `.dev/tasks/to-do/<id>/` path, and gives tdd/init-lite a `--output <file>`; workflow STOPs on `--output` with no yaml. 7.2 step 3 cannot check "the WC-4 contract path". Recommendation: state per command, in section 3, the exact flag and resulting contract path, and how the coordinator learns workflow's `<id>` before or after dispatch. Priority High. | CRITICAL | yes | 2.2 WC-4; 2.3; 3.1 (adversarial, workflow, tdd, init-lite, cleanup-audit rows); 7.2 step 3 | spec:62, spec:73, spec:83, spec:85, spec:87, spec:90, spec:92, spec:182; `src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md:3,39` |
| 3 | A retry (`worker-start --retry-of`) reruns the same Task, so the same brief and the same `--output` directory; WC-6's "fresh output directory" has no owner, and a retry without a resume flag overwrites attempt 1. Recommendation: assign the choice (for example, the command writes into a per-run subdirectory named in the contract, or the coordinator creates a new Task) and say whether attempt 1's contract is kept. Priority High. | MAJOR (FR-8 GAP) | yes | 2.2 WC-4, WC-6 | spec:62, spec:64; `.dev/orca-command-refactor/inventory/orca-capabilities.md:116` |
| 4 | P1 makes every section 3 command accept `--unattended` and carry an `## Unattended mode` section, but gate conversion lands in P2-P4; the spec says the flag is a no-op only "where a command has no gate" and is silent for commands whose gates are still live, so a coordinator dispatching `/sc:tdd ... --unattended` after P1 stalls the worker on a prompt. Recommendation: in P1, add the flag and section only to P1 commands and ready commands without gates, or have P1's section for later-phase commands say "not yet unattended-safe" and make the coordinator brief template refuse them. Priority High. | MAJOR | yes | 6 (P1); 7.3 AC-1.1; 2.2 WC-2 | spec:60, spec:159-162, spec:195; `.dev/orca-command-refactor/inventory/orca-capabilities.md:129` |
| 5 | Live checks (7.2, AC-0.4, AC-1.2, AC-2.2) never say to install or sync the edited primitives before the run. `make sync-dev` does not copy core files, so `~/.claude/WORKER-CONTRACT.md`, which every `## Unattended mode` section points to, exists only after `superclaude install`; a live check can therefore exercise stale copies and its PASS proves nothing. Recommendation: add a 7.2 step 0 that runs `make sync-dev` and `uv run superclaude install` (or names the exact install command) and checks the contract file is present. Priority High. | MAJOR | yes | 2.1 contract file; 7.2 | spec:52, spec:178-186, spec:194, spec:196; `Makefile:109-165`; `src/superclaude/cli/install_core.py:4,33`; `CLAUDE.md:408` |
| 6 | The "edits are additive" filter `grep -E '^-[^-]'` (AC-C5, AC-0.3) misses deleted lines that start with `-` (every markdown bullet), deleted `--flag` lines and deleted blank lines, so a phase that removes bullets passes. Recommendation: check the deletions column of `git diff --numstat master...HEAD -- <file>`, which must be 0 for an additive edit. Priority Medium. | MAJOR | yes | 7.1 AC-C5; 7.3 AC-0.3 | spec:176, spec:193; reviewer test V11 (section 1) |
| 7 | Shell commands inside markdown tables carry `\|` as a table escape. Copied from the spec source, AC-C1's `\|` becomes a literal pipe for GNU grep 3.11, so the check matches nothing and can never fail; AC-C4 and AC-0.3 pipelines break the same way. Recommendation: move these commands out of tables into fenced code blocks. Priority Medium. | MAJOR | yes | 7.1 AC-C1, AC-C4; 7.3 AC-0.3 | spec:172, spec:175, spec:193; reviewer test in section 2 (Adzic) |
| 8 | SA-2 allows the contract file to mention Orca as the caller's question channel, and WC-3 needs that `ask` example, but AC-C1 scans `src/superclaude/core`, where `WORKER-CONTRACT.md` lives, and fails on `orca orchestration ask`. Recommendation: exclude `src/superclaude/core/WORKER-CONTRACT.md` from AC-C1 or forbid the literal command in SA-2. Priority Medium. | MAJOR | yes | 5 SA-2; 7.1 AC-C1; 2.2 WC-3 | spec:61, spec:147, spec:172 |
| 9 | WC-3 lets the worker ask the coordinator instead of blocking, with no bound on resumes and no reconciliation with WC-6 when it re-invokes into the same directory; AC-2.2 expects `status: blocked`, but 7.2 gives the coordinator no rule for answering a `question`, so the gate-trigger result is undefined. Recommendation: cap resumes (for example one timeout, then `blocked`), and state that during AC-2.2 the coordinator replies with a fixed refusal or the worker must not ask. Priority Medium. | MAJOR (FR-8 GAP) | yes | 2.2 WC-3; 7.2 step 3; 7.3 AC-2.2 | spec:61, spec:64, spec:182, spec:200 |
| 10 | WC-5 maps only "no report exists" to `failed`; an empty, truncated or `status`-less contract has no mapping, so a crashed command can be reported `succeeded` under "otherwise". Recommendation: "missing, unreadable, or without a valid `status` → `--outcome failed`". Priority Medium. | MAJOR (FR-8 GAP) | yes | 2.2 WC-5 | spec:63 |
| 11 | WC-10 bounds Bash waits only; a command's own foreground Agent-tool fan-out (kept by WC-7) can hold the top-level session in one tool call for longer than 5 minutes, and subagents may not heartbeat, so the "heartbeat every 5 minutes" requirement cannot be met as written. Harm is limited: Orca's use of heartbeat age is UNVERIFIED and release never happens on heartbeat. Recommendation: state that heartbeats may lapse during a foreground Agent-tool call and that the coordinator then uses `worker-show`/`worker-list`, or require background Agent calls. Priority Low. | MAJOR (FR-8 GAP) | yes | 2.2 WC-10, WC-7 | spec:24, spec:65, spec:68; `.dev/orca-command-refactor/inventory/orca-capabilities.md:111,130` |
| 12 | WC-1 requires a launch prompt to fall back "well inside" the readiness limit without a number; evidence shows failure above about 45 s and a pass at 30 s. Recommendation: state the number (for example at most 30 s, as `EVIDENCE.md:45` proved). Priority Low. | MAJOR (FR-8 GAP) | yes | 2.2 WC-1 | spec:59; `.dev/evals/ccsession-orca-e2e-20261026/EVIDENCE.md:39,45,56` |
| 13 | The spec's stated repo root names a worktree that does not exist on this machine; paths resolve here, so readers are not misled about content, only about location. | MINOR | no | header | spec:4; reviewer check V5 |
| 14 | WC-1 and WC-12 are not traced to any phase or acceptance check (WC-1 is owned by "launch setup", which no phase covers). | MINOR | no | 2.2; 6; 7 | spec:59, spec:70, spec:158-162 |
| 15 | 7.2 step 6 passes only when `git status --short` shows the brief's own files; workers share the current worktree by default, so parallel live checks see each other's files and fail falsely. | MINOR | no | 7.2 step 6; WC-11 | spec:69, spec:185; `.dev/orca-command-refactor/inventory/orca-capabilities.md:115` |
| 16 | WC-4 defines no version field, while the workflow contract already carries `contract_version: "1.1"`; with 37 producers changing over four phases the coordinator cannot tell old from new contracts. | MINOR | no | 2.2 WC-4 | spec:62; `src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md:6` |

Totals: 16 findings; 12 blocking (2 CRITICAL, 10 MAJOR, of which 5 come from boundary-table GAPs under FR-8), 4 minor.

Self-audit of what was checked and found sound: the 43-command count (V1); the "no Orca calls today" baseline (V2, V3); the cited `CLAUDE.md` lines (V4); `KNOWN_CORE_FILES` and the install path (V7); the adversarial "every invocation" contract rule (V10); PyYAML dependency (V12); the hard-limit citations (V13); the phase/command partition (section 3.2 rows: P1 9 + P2 11 + P3 4 + P4 3 = 27, matching its 27 rows; P2 also carries the 4 ready commands with gate fixes, spec:99-125, 159-162); the CAPS facts on depth, retry, release and readiness (V15).

## Decisions
| Decision | Options considered | Rationale |
|---|---|---|
| Skip the command's Improve step (no revised spec written) | Write an improved spec; review only | The task brief says "Do NOT edit the spec", and the command's own Boundaries forbid modifying a spec without consent. Revision is Task 6 (`.dev/orca-command-refactor/README.md:27`). |
| Repo root | The spec's stated root (spec:4); this worktree | The stated root does not exist (V5); the task brief names this worktree as repo root. |
| Severity of boundary-table GAPs | Grade each on harm; apply FR-8 | FR-8 makes each GAP at least MAJOR and the review loop makes FR-8 findings blocking. Applied as written; the lower real harm of Findings 11 and 12 is stated in their rows and in the consensus note. |
| One finding per defect | Split each check failure; group by root cause | Grouped by root cause (for example, the three G4 GAP rows are one Finding 9) so the reviser fixes each cause once. |
| Live probes | Run a real Orca worker to test WC rules; reason from files | Not run: the brief allows writing only this file and starting workers would create Orca state; behaviour not seen is marked UNVERIFIED. |

## UNVERIFIED items
1. Whether Orca uses heartbeat age in its liveness verdict (`.dev/orca-command-refactor/inventory/orca-capabilities.md:130,182`); decides the real harm of Finding 11.
2. Whether Claude Code loads a skill from the project `.claude/skills/` or `~/.claude/skills/` first when both exist; `CLAUDE.md` states the agent lookup order for primitives, not Claude Code's loader. Finding 5 holds either way for the core file, which only `superclaude install` places.
3. Exactly how each command's coordinator brief would be pasted (rendered markdown or source); Finding 7 assumes an agent copies from the source file, which is how agents read files.
4. Whether `worker-start --retry-of` lets the coordinator change the Task's brief; the capability inventory shows the same Task ID is reused (`CAPS:116`), and no flag to change the spec appears there.

## Reviser brief
Blocking findings to fix: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12.

Rules for the reviser (restated from the command's review loop): revise only the text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding number; report the spec's byte size before and after. Minor findings 13-16 are notes and need no change.

verdict: FAIL
