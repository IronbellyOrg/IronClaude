# Diff Analysis: D3 decision-option comparison (`/sc:pr-submit` as an Orca worker)

## Metadata
- Generated: 2026-11-02T00:00:00Z (date from session context; time not recorded)
- Pipeline: `/sc:adversarial` Mode A, Step 1 (diff analysis); analytical, non-advocating
- Decision: D3, `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:339-343`
- Variants compared: 3 (`variant-1-original.md` option a; `variant-2-original.md` option b; `variant-3-original.md` option c)
- Total differences found: 33 (S + C + X + U), plus 8 shared assumptions
- Categories: structural (6), content (13), contradictions (5), unique (9), shared assumptions (8)
- Taxonomy levels (AD-5, `sc-adversarial-protocol/SKILL.md:133-177`): L1 surface, L2 structural, L3 state-mechanics; priority L3 > L2 > L1; default L2

## Structural Differences

Variant 1 = option (a), coordinator or person only. Variant 2 = option (b), worker with pre-authorization. Variant 3 = option (c), unsupervised orca-cli handoff to a person-owned agent tab. Citation keys follow each variant's own key (`SPEC`, `PRS`, `PRC`, `HWW`, `CAPS`, `[CLI]`, `[G]`).

| # | Area | Variant 1 | Variant 2 | Variant 3 | Severity | Tag |
|---|------|-----------|-----------|-----------|----------|-----|
| S-001 | Section layout | Position, Safety, Reliability, Day to day, Cost | Adds a leading "Strongest case for it" section before Safety | Adds a leading "Why a third option" section framing (a) and (b) as the two poles | Low | L1 |
| S-002 | Citation key coverage | SPEC, PRS, PRC, HWW, CAPS (plus `CLAUDE.md:50` inline) | SPEC, PRS, PRC, CAPS; no HWW, no CLAUDE.md | SPEC, PRS, PRC, CAPS, plus Orca guides `[CLI]` / `[G]` pinned to version 1.4.237 | Low | L1 |
| S-003 | Execution topology (architecture) | One top-level session (coordinator or person) runs pr-submit inline, serially | Coordinator plus N supervised Orca workers, one Task/Dispatch per PR, each in its own worktree | Coordinator plus N unsupervised person-owned agent tabs launched by `agent launch`; no Run, Task or Dispatch | High | L2 |
| S-004 | Change surface on the pr-submit component | None | Full section 3.2 row (`SPEC:137`), markdown summary, reconciled "Will Not" line, AC-4.3 | None to pr-submit; one sentence in spec section 4 / D3 | Medium | L2 |
| S-005 | Relationship to the spec's option set (`SPEC:341-343`) | Is spec option (a), the current recommendation | Is spec option (b) | Not in the spec; a new option outside the a/b pair | Medium | L2 |
| S-006 | Where each variant places its own weaknesses | One named weakness (coordinator blocked during waits) | Safety and Reliability sections mostly argue against itself (boundary, unattended push, UNVERIFIED runtime, slower HALTs) | Two named weaknesses (no completion signal; UNVERIFIED slash-command-as-prompt) | Low | L1 |

## Content Differences

| # | Topic | Variant 1 Approach | Variant 2 Approach | Variant 3 Approach | Severity | Tag |
|---|-------|-------------------|-------------------|-------------------|----------|-----|
| C-001 | The command's own "**Will Not:** run headless / imply a daemon" boundary (`PRC:85`; `PRS:43-45`) | Decisive reason against: a worker under `--unattended` has no person at the keyboard (`SPEC:54`), so running it as one contradicts the stated design | Acknowledged as a cost: either rewrite the boundary or treat an unwatched worker session as "attended" | Boundary kept intact: each run is a normal top-level session in a visible tab | High | L3 |
| C-002 | Outward actions at `--monitor 3` (commit, push, retrigger, reply, resolve; `PRC:83`, `HWW:221`, `HWW:307`) | Kept one hop from a person, in a session a person can watch; repo makes it the mandatory PR path (`CLAUDE.md:50`) | Worker pushes and resolves threads with no person watching; safety rests on D4 authorization plus pr-submit's own guards (no force-push, one fix commit, `PRC:85`) | Run unchanged in a person-owned tab; the coordinator launches it only when the person's instruction names it (cites D4) | High | L3 |
| C-003 | HALT handling (state transition at `pr_head_mismatch` and other operator HALTs, `PRC:28`) | Operator reads and follows the HALT message in place | HALT becomes a `blocked` contract, then a new Task (WC-6); admitted slower than reading it in place; spec row allows `ask` or `escalation` (`SPEC:137`) | HALT waits in a visible tab; claims no time limit applies (`CAPS:52`); person steps in | High | L3 |
| C-004 | Parallel PR monitoring | Serial; asserts "a run usually opens one PR at the end, so parallel PR monitoring is rarely needed" (no citation) | The strongest case: several PRs monitored at once, one worker per worktree | Parallel via one tab per PR | High | L2 |
| C-005 | Coordinator availability (concurrency of the coordinator's own loop) | Coordinator is held during each wait (up to 600 s default, `PRC:49`) over up to `--max-rounds` cycles (`PRC:47`) and cannot service other workers' questions in that turn | Coordinator stays free | Coordinator stays free | Medium | L3 |
| C-006 | Completion signal to the coordinator (state of the PR run) | Implicit: the run happens in the coordinator's own session | `worker_done` plus contract in `--output-dir` pointing at a markdown summary and `monitor-run-<PR>.jsonl` (`SPEC:137`, WC-4, WC-5) | None; the person reads each tab, or the coordinator reads the run-log file later (stated weakness) | High | L3 |
| C-007 | Heartbeat feasibility (WC-10 liveness) | Avoids the need; notes poll runtime is UNVERIFIED (`SPEC:394`) and WC-10 depends on it (`SPEC:74`) | Claims heartbeats fit between poll-then-sleep iterations (`PRS:56-80`, `SPEC:137`); AC-4.3 must prove no Bash call exceeds 240 s (`SPEC:276`) | Not applicable: no heartbeat, no contract, no `worker_done` | Medium | L3 |
| C-008 | Dependence on D4 (outward-action authorization) | None stated; the coordinator or person runs it directly | "Depends on D4 (a) or (c) for any push" | Treats the launch itself as an outward step needing a person's instruction under D4 | High | L2 |
| C-009 | Implementation cost | Zero: no pr-submit edits, no AC-4.3, 35 not 36 commands accept `--unattended` (`SPEC:195`) | Full P4 row (`SPEC:137`, `SPEC:185`), AC-4.3 on a scratch fork PR (`SPEC:276`), reconciled "Will Not" line | One spec sentence; no pr-submit edits; no AC-4.3 | Medium | L2 |
| C-010 | Durability and resume state (`PRS:43-45`, `PRC:55-56`) | Not discussed | Write-ahead run-log plus `--resume`, matched to WC-6's resume cell | Run-log and `--resume` work as today | Low | L3 |
| C-011 | Top-level activation requirement (`PRS:47-49`) | Satisfied: the coordinator is top-level (`CAPS:161`) | Satisfied: an Orca worker is a top-level session (`CAPS:161`) | Satisfied: the tab is a top-level session | Low | L2 |
| C-012 | What the person sees day to day | The review loop in the coordinator's session | Worker reports and contracts; acts on a HALT via a contract and a re-dispatch | One live tab per PR | Low | L2 |
| C-013 | Reversibility | Reversible later by choosing (b) | Not discussed | Cost to switch to (b) later unchanged | Low | L2 |

## Contradictions

| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Variant 3 Position | Impact | Tag |
|---|-------------------|-------------------|-------------------|-------------------|--------|-----|
| X-001 | Does an unattended Orca worker fit pr-submit's attended, not-headless boundary? | "Running it as a worker contradicts the command's stated design" (V1 Safety, citing `PRC:85`, `SPEC:54`) | "**It already fits a worker technically.**" (V2 Strongest case), while its own Safety section concedes it "either rewrites that boundary or treats the worker's session as 'attended' when no person watches it" | "(b) ... makes an attended, top-level, 'Will Not: run headless' command ... into an unattended worker" (V3 Why a third option) | High | L3 |
| X-002 | Is parallel PR monitoring a real need? | "A run usually opens one PR at the end, so parallel PR monitoring is rarely needed" (unsourced) | "**Parallel PR monitoring.**" is the strongest case for (b) | Parallelism is the reason (c) exists ("(a) is safe but serial") | Medium | L2 |
| X-003 | Can an operator HALT be resolved without a person in place? | HALTs "are written for an operator to act on" (`PRC:28`) | Yes, as a `blocked` contract and a new Task (WC-6), only slower | A HALT "waits in a visible tab"; a person steps in | Medium | L3 |
| X-004 | Does the coordinator need the PR run's completion state? | Gets it in-session by construction | Yes: `worker_done` plus contract | Coordinator "gets no completion signal" and creates no Task, yet may "read the run-log file later"; the guide line it cites says "do not monitor completion" (`[G]` 39), and the handoff route does not apply when the user asks to "monitor, wait for results, track completion" (`[CLI]` 27) | High | L3 |
| X-005 | Which decision governs who may start the outward loop? | No D4 dependency; the coordinator or person runs it | D4 governs every push by a worker ("Depends on D4 (a) or (c)") | D4 governs the coordinator's launch of a person-owned tab, although D4 is framed as "May a coordinator's brief authorize a worker's outward actions?" (`SPEC:345`) | Medium | L2 |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | Variant 3 | A third option outside the spec's a/b pair: parallel monitoring through orca-cli full handoffs, with pr-submit unchanged | High |
| U-002 | Variant 3 | Grounds the route in Orca's own role table: "Handoff owner ... create no Run, Task, or Dispatch" (`[G]` 39) | Medium |
| U-003 | Variant 3 | Names the UNVERIFIED point that a slash command passed as `--prompt` runs as a slash command, and ties it to the same argv mechanism the spec's workers rely on (`CAPS:47`) | Medium |
| U-004 | Variant 2 | Shows the 600 s default is a cumulative budget over poll-then-sleep iterations (`PRS:56-80`), so heartbeating does not require changing the wait budget | Medium |
| U-005 | Variant 2 | Lists pr-submit's own residual guards under an unwatched push (no force-push, only the cycle's one fix commit, `PRC:85`) | Medium |
| U-006 | Variant 2 | Ties durability (write-ahead run-log plus `--resume`) to WC-6's resume cell | Low |
| U-007 | Variant 1 | Quantifies its own weakness: coordinator held up to 600 s per wait over up to `--max-rounds` cycles (`PRC:47`, `PRC:49`) | Medium |
| U-008 | Variant 1 | Cites routing-guide policy that monitor 3 is the full mutating/publishing loop (`HWW:221`, `HWW:307`) and the repo's mandatory-PR-path rule (`CLAUDE.md:50`) | Low |
| U-009 | Variant 1 | Records the command-count consequence (35 vs 36, `SPEC:195`) and that (a) is reversible to (b) later | Low |

## Shared Assumptions

Agreement points found across all three variants, with the preconditions under them. UNSTATED preconditions are promoted to synthetic diff points marked [SHARED-ASSUMPTION].

| # | Shared assumption | Classification | Evidence / note | Tag |
|---|-------------------|----------------|-----------------|-----|
| A-001 | "Run unattended as an Orca worker" equals "run headless" in the sense of the "**Will Not:** run headless" boundary (`PRC:85`). All three read it so (V1 via `SPEC:54`; V2 "either rewrites that boundary"; V3 "into an unattended worker"). | CONTRADICTED | `PRC:85` does not define "headless". The spec's own UNVERIFIED item 9 (`SPEC:391`) says the repo's headless signal is `claude --print` with no TTY, while Orca launches Claude interactively with the prompt on the command line (`CAPS:47`). By that definition an Orca worker is not headless; what it lacks is an attending person (`PRS:43` "attended, in-session"). The debate should argue "attended", not "headless". | L3 |
| A-002 | pr-submit must run in a top-level session, never an Agent-tool subagent (`PRS:47-49`), and every option satisfies this activation guard. | STATED | All three cite it (C-011). | L3 |
| A-003 | pr-submit's FSM, ordinal gates and guards (`PRC:85`: no upstream push, no force-push, one fix commit per cycle) stay unchanged in every option. | STATED | V2 and V3 explicit; V1 by "no Phase 4 changes". | L3 |
| A-004 | [SHARED-ASSUMPTION] "Attended" in `PRS:43` is satisfied when a person *can* see the session, not when a person actively watches it. V1: "a session where a person can watch"; V3: "a visible tab"; V2 treats an unwatched worker as the failing case. None states whether a person is actually watching the coordinator during a long Orca run, or N tabs at once. | UNSTATED | Decides whether (a) and (c) really keep outward steps "one hop from a person" and whether a HALT is noticed. Boundary/state term: attended state. | L3 |
| A-005 | [SHARED-ASSUMPTION] Losing the session loses the monitor (`PRS:43-45`), and resume via `--resume` is the recovery path in every option; none considers what happens to a coordinator session, a worker, or a launched tab when the Orca app or terminal restarts mid-wait. | UNSTATED | V2 and V3 rely on the run-log; V1 is silent. Spec UNVERIFIED item 11 (`SPEC:393`) leaves Orca's total Dispatch runtime unknown. | L3 |
| A-006 | [SHARED-ASSUMPTION] The session that runs pr-submit (coordinator, worker worktree, or handoff tab) has authenticated `gh`, the review App, a checkout at the PR head commit, and the CI-wait prerequisites (`HWW:216`, `HWW:223`; `PRC:28-30`). | UNSTATED | Matters most for V2 and V3, where each PR runs in a different worktree; a head-checkout mismatch is a `pr_head_mismatch` HALT (`PRC:28`). Dependency precondition. | L2 |
| A-007 | The repo rule that every PR goes through `/sc:pr-submit --monitor 3` (`CLAUDE.md:50`) stays in force in Orca runs, so D3 decides where it runs, not whether. | STATED | V1 cites `CLAUDE.md:50`; V2 and V3 assume `--monitor 3` (V3's launch prompt passes it). | L2 |
| A-008 | Parallelism, if needed, comes from several independent changes, each in its own worktree and branch with its own PR. | STATED | V2 "each worker in its own worktree"; V3 "in that change's worktree"; V1 implies one PR per run. | L2 |

## Citation spot-check

Six decision-critical citations re-read on 2026-11-02 (files via Read; Orca guides via `orca-ide skills get orca-cli | cat -n` and `orca-ide skills get orchestration | cat -n`).

| # | Citation (used by) | Short quote from the source | Verdict | Note |
|---|--------------------|-----------------------------|---------|------|
| 1 | `src/superclaude/commands/pr-submit.md:85` (V1, V2, V3) | "**Will Not:** run headless / imply a daemon; push to an upstream parent remote ... force-push; push any commit besides the cycle's one fix commit" | CONFIRMED | Text matches all three uses. It does not define "headless" (see A-001). |
| 2 | orca-cli guide lines 25-52 (V3 cites 27-31 and 49-52) | L29: "Do not wait for the receiving agent to finish." L31: "Do not use `orca orchestration task-create` ... for full handoffs." L49: "For a fresh agent in a worktree that already exists, use `agent launch`" with `--prompt` (L52) | CONFIRMED | The mechanism V3 describes exists as cited. Caveats the variant does not carry: L27 says the original agent "then ... stops" and excludes requests to "monitor, wait for results, track completion"; the L52 example uses `--agent codex`, not `claude`. |
| 3 | orchestration guide line 39 (V3) | "The user asks to hand off ownership or start another agent/worktree without supervision \| Handoff owner \| Use `orca-cli`; create no Run, Task, or Dispatch and do not monitor completion" | CONFIRMED | Quoted accurately, but V3 omits the final clause "do not monitor completion", which bears on its "coordinator reads the run-log file later" (X-004). |
| 4 | `.dev/orca-command-refactor/inventory/orca-capabilities.md:52` (V3) | "The 60 s applies only to startup ... A person's own launch tab has no limit: ... 'No time limit was observed for a person's launch tab.'" | OVERSTATED | V3 uses it to say a HALT can wait in the tab with no limit. The cited limit is the startup readiness limit only; the same line says any started worker waiting on a prompt "is healthy, not failed". So the no-limit point does not distinguish (c) from (b) for HALT waits, and a tab started by `agent launch` from the coordinator is not shown to be "a person's own launch tab". |
| 5 | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:54` (V1) | "It names no Orca command, so the same mode serves any caller that has no person at the keyboard." | CONFIRMED | Supports "a worker under `--unattended` is a run with no person at the keyboard". |
| 6 | V2 "Depends on D4 (a) or (c) for any push", against `.dev/orca-command-refactor/decisions/D4/option-c.md:3` | "a brief may authorize a worker to make **local commits** on its own feature branch, and nothing else outward ... (push, merge, PR ...) is never done by a worker" | WRONG | Under D4 (c) a worker never pushes, so (b) at `--monitor 3` is possible only under D4 (a). Under D4 (b) or (c), option (b) caps out at `--monitor 2` (fix locally, HALT before push, `PRC:37`). The spec itself lists only D4 (a) and (b) (`SPEC:346-347`). |

Incidental findings from the same reads (not counted above):
- V1 and V2 cite `CAPS:161` for "top-level session". The line is about Orca workers ("Such a command can still be an Orca worker, because an Orca worker is a top-level Claude session"); it supports V2 directly and V1 only by analogy (OVERSTATED for V1's coordinator claim, low impact).
- The spec cites `sk/sc-pr-submit-protocol/SKILL.md:37-39` for the top-level rule (WC-7 at `SPEC:71`, pr-submit row at `SPEC:137`). Those lines hold the FSM-ordinal paragraph; the top-level rule is at `SKILL.md:47-49`, which all three variants cite correctly. Spec citation drift, WRONG.

## Summary
- Total structural differences: 6
- Total content differences: 13
- Total contradictions: 5
- Total unique contributions: 9 (Variant 1: 3, Variant 2: 3, Variant 3: 3)
- Total shared assumptions: 8 (STATED 4, UNSTATED 3 promoted as [SHARED-ASSUMPTION]: A-004, A-005, A-006; CONTRADICTED 1: A-001)
- Taxonomy coverage over S/C/X/A (32 points): L1 = 3, L2 = 14, L3 = 15. Every level is covered.
- Citation spot-check: 6 checked; CONFIRMED 4, OVERSTATED 1 (V3 on `CAPS:52`), WRONG 1 (V2's "D4 (a) or (c)"). Two incidental findings: V1's `CAPS:161` use is overstated; the spec's own `SKILL.md:37-39` top-level citation is wrong (should be 47-49).
- Highest-severity items: S-003 (topology), C-001 (headless boundary), C-002 (outward actions at monitor 3), C-003 (HALT handling), C-004 (parallel PR need), C-006 (completion signal), C-008 (D4 dependency), X-001 (does a worker fit the boundary), X-004 (unsupervised handoff vs completion tracking), and A-001 (CONTRADICTED: "worker" is treated as "headless", but by the repo's own headless signal an Orca worker is not headless; the real issue is "attended").
- Similarity check: of 19 comparable items (S + C), the three variants take the same position on 1 (C-011, top-level activation), i.e. 5% agreement and 95% difference. Differences are well above the 10% threshold, so the variants are not near-duplicates and no similarity warning applies.
