# D1 Round 2: rebuttal by the Variant 2 advocate (option b, the command detects it is an Orca worker)

Citation key: `SPEC:N` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:N`; `CAPS:N` = `.dev/orca-command-refactor/inventory/orca-capabilities.md:N`; `TL:N` = `src/superclaude/skills/sc-tasklist-protocol/SKILL.md:N`; `[G] N` = line N of `orca-ide skills get orchestration`; `V1:N`/`V2:N`/`V3:N` = variant files; `R1-V1:N`, `R1-V2:N`, `R1-V3:N`, `R2-V1:N` = earlier round statements in `rounds/`; `DA:N` = `diff-analysis.md`. Every citation newly relied on was re-read on 2026-11-02.

## Responses to criticisms
| # | Criticism | Source | Response | Concede / hold |
|---|---|---|---|---|
| 1 | V2 never picks between the environment route and the preamble route. | R1-V1:25; R1-V3:37; DA:19-20 (S-002, S-003) | True of the original (V2:3). Round 1 committed to preamble-only and dropped the environment route (R1-V2:6, R1-V2:35). The defect is fixed for the debate, but it stays a defect of the variant as written. | Concede (original); fixed in R1 |
| 2 | The environment route is unsafe for people. | V2:13 (self); R1-V3:37; DA:30 (C-001) | Agreed, and the case no longer rests on the `worker-list` observation. Orca sets `ORCA_TERMINAL_HANDLE` in any "live Orca terminal" (`CAPS:149`), and it was also observed in a dispatched worker (`CAPS:151`). By design it marks Orca terminals, not workers. | Concede |
| 3 | (b) does not remove the forgotten-switch failure class (X-002). | R1-V1:26; R1-V3:36; DA:49 | Already conceded (R1-V2:36). A missed preamble reproduces the stall. | Concede |
| 4 | (b) breaks SA-2 and non-goal 1, and no grep enforces SA-2, so a violation would pass CI. | R1-V1:27; R1-V3:38; R2-V1:21 | My Round 1 fallback was to write the detection rule only in `WORKER-CONTRACT.md` (R1-V2:21). That does not save it. SA-2 allows Orca in the contract file only "as an example of a caller's question channel" (`SPEC:170`), and non-goal 1 bans "Orca-specific branching" (`SPEC:314`) whichever file holds the text. Both need amending, and nothing mechanical would catch drift. | Concede |
| 5 | V2:25 claimed AC-C1's grep needs an exception. | DA:97; R1-V1:27 | Wrong; withdrawn in R1-V2:38. The AC-C1 pattern does not match detection text. | Concede |
| 6 | V2:14 overstated `CAPS:47` (preamble and task share one command line). | DA:96; R1-V1:29 | `CAPS:47` speaks only of the task (`promptInjectionMode: 'argv'`). Withdrawn (R1-V2:37). | Concede |
| 7 | No token to audit: a missing flag is visible in the brief afterwards, a missed recognition leaves nothing to find. | R1-V1:29; R2-V1:9; DA:32 (C-003) | Partly. The input is visible under both: the brief under (a), the preamble in the `worker-read` transcript under (b). Whether the model acted on it is invisible under both (AC-2.8 is manual, `SPEC:269`). What (b) truly loses is a static check before dispatch: a coordinator can grep its brief for `--unattended`; nothing equivalent checks "the worker will recognise its preamble". | Partly concede |
| 8 | Recognising context is a broader model judgment than recognising a literal token. | R1-V1:20 | Hold for the worker session: it must already recognise its preamble for WC-3, WC-5, WC-7 and WC-12 (`SPEC:67-76`), so (b) adds no new recognition there. Concede for commands: under (b) the command's behaviour branches on that recognition, so a miss changes what the command does (it prompts). Under (a) and (c) a miss loses only lifecycle messages. | Partly concede |
| 9 | Briefs do not get shorter (X-006). | R1-V1:28; R1-V3:39; DA:53 | Conceded (R1-V2:39). One token goes; the report directory stays (`SPEC:57`). | Concede |
| 10 | (b) does nothing for callers with no preamble (`claude -p`, CI). | V2:18; R1-V3:38; DA:34 (C-005) | True, low weight while no outside caller is planned (A-007). But one such caller sits inside the design: see 11. | Concede |
| 11 | The preamble does not reach Agent-tool subagents, so tasklist's reflect fan-out needs an explicit marker, a flag by another name. | R2-V1:23, R2-V1:33 | Verified and decisive (New evidence 1). Stage 10.5 dispatches reflect through the Agent primitive with a literal command line (`TL:1618`, `TL:1623`), and the spec requires that line to carry `--unattended` (`SPEC:145`). So (b) still needs a flag-like token wherever a command fans out to another command. It would then carry two switches, strictly more than (a). | Concede |
| 12 | (b) degrades worse: a missed preamble stalls with nothing written, while under (c) the flagged command still writes its contract. | R2-V1:22; R1-V2:41 (self) | Agreed. | Concede |
| 13 | A pasted flag under (a) fails safe and is visible in what the person typed. | R2-V1:15 | A pasted preamble under (b) triggers the same unattended behaviour, which fails safe through WC-2 and WC-9 (`SPEC:66`, `SPEC:73`), and is equally visible in the person's prompt. Neither is enforced against. | Hold (equal) |
| 14 | The `[G]` citation key can be re-read only by running Orca. | DA:22 (S-005); R1-V1:64 | `skills get` reads bundled content without the runtime (`CAPS:147`), and `CAPS:148` quotes `[G]` 38 and 41. It needs an installed tool, not a running Orca. | Hold (equal) |

## Updated assessment of other variants
**Variant 3 (corrected in R1-V3:16-21).** Steelman: commands keep (a)'s single token switch, and the only Orca-aware check runs in the worker session. That session is already Orca-aware, and SA-2 does not govern it. The check is keyed to the `## Unattended mode` section, which AC-1.1 already ties to exactly the commands that accept the flag in each phase (`SPEC:257`). So it is inert in P0 (`SPEC:191`), never refuses `/sc:load` (`SPEC:197`), and turns a forgotten flag into the `worker_done --outcome failed` that Orca guarantees (`CAPS:73`). It also carries V2's best idea to the right place. The guard's own trigger, "this session received a preamble with Task and Dispatch IDs", is Orca's role-table rule (`[G]` 38, 41; `SPEC:53`), which V2 brought in (U-004).

Remaining critique, all small:
1. The guard needs the worker to open the command file before it runs the command. That is one more model step, and under the repo's dual-surface rule it must name both the installed copy and the project `.claude/` copy.
2. I agree with R2-V1:28 that the guard sentence must travel in the brief template, because nothing loads `WORKER-CONTRACT.md` automatically (`SPEC:58`, `SPEC:79`).
3. I agree with the symmetric check (R2-V1:35). The flag on a command that has not been converted is the mismatch `SPEC:79` invites today.

Its residual gap, pre-conversion commands that still stall on a gate (R1-V3:43), is the same under (b), because (b)'s detection text also arrives per phase (R1-V2:19). (b) keeps no edge over (c). I rank V3 first.

**Variant 1.** Steelman: one mechanism, the lowest cost, Orca-free commands, explicit phase gating, and it is the only variant to tie D1 to WC-9's outward defaults (`SPEC:73`). Its advocate now recommends (c) (R2-V1:76), so (a) alone has one open weakness: the silent stall (`SPEC:47`, `SPEC:238`). I rank it second. It is still strictly better than (b): it needs no SA-2 amendment, and its token crosses the subagent boundary (New evidence 1).

**Variant 2 (mine).** I rank it third, including the preamble-only form.

## New evidence
1. **The subagent boundary is real in the source, not only in the spec.** Tasklist's Stage 10.5 says to "Dispatch the agents via the same `Task` (Agent) primitive Stage 7 uses" (`TL:1618`). Each agent receives a literal command line, `/sc:reflect --mode pre --remediate ...` (`TL:1623`), and nothing in the parent's conversation. An Agent-tool subagent therefore never sees the worker's preamble. Under (b), tasklist would have to write an explicit marker into that line to make reflect unattended, and `SPEC:145` already names that marker `--unattended`. Option (b) cannot avoid a flag. It can only add detection on top of one, which leaves it with (a)'s mechanism plus an SA-2 amendment.
2. **The environment variable is not a worker signal by design.** `CAPS:149` ties `ORCA_TERMINAL_HANDLE` to any "live Orca terminal", and `CAPS:151` records it set in a dispatched worker. Together they settle the environment route without relying on A-001's unverified `worker-list` preconditions. Item 13 (`SPEC:395`) and the D1 (b) text (`SPEC:330`) can say so.
3. **V2's unique contributions survive only as inputs to (a) and (c).** Orca's role table (U-004) is the trigger of V3's guard. The reflect `--print` precedent (U-006; `SPEC:174`, `SPEC:391`) shows that an Orca worker needs an explicit switch, which supports (a) and (c), not (b).

## Updated shared assumption responses
| A-NNN | R1 response | R2 response | Reason for change |
|---|---|---|---|
| A-005 | ACCEPT (meaning the diff analysis's flag of it is valid) | REJECT | Restated to match the other advocates: the assumption is false (`SPEC:191`, `SPEC:197`). V3's corrected guard no longer depends on it, because it keys on the `## Unattended mode` section (`SPEC:257`). |
| A-006 | QUALIFY (fixed only until the user rules) | ACCEPT | With the subagent finding (New evidence 1), (b) offers nothing that justifies amending SA-2 or non-goal 1 (`SPEC:170`, `SPEC:314`). D1 should treat them as fixed. |

A-001, A-003 and A-009 are unchanged (QUALIFY). New evidence 2 adds a reason under A-001 without changing the answer.

## Final per-point positions
| ID | Superior approach | Changed since R1? | One-line reason |
|---|---|---|---|
| S-001 | equal | yes | Section order is cosmetic. |
| S-002 | V1 | no | Only V1 named its own weakness; V2 argued against half of itself. |
| S-003 | equal (V1, V3) | yes | Both commit to one command-side switch; V3's second check sits outside SA-2. |
| S-004 | V3 | no | The Orca-aware check lives in the worker session; commands stay as in V1. |
| S-005 | equal | no | `[G]` needs only an installed `orca-ide` (`CAPS:147`). |
| S-006 | V3 | no | It frames itself against both alternatives. |
| S-007 | equal (V1, V3) | yes | Both cover the person and the coordinator. |
| C-001 | equal (V1, V3) | no | Commands read no environment or conversation; V2's environment route fails SA-1. |
| C-002 | equal (V1, V3) | no | Same WC-9 behaviour; V1 argued it explicitly. |
| C-003 | V3 | yes | Same text checks as V1, plus a live run that tells the designs apart (R1-V3:26). |
| C-004 | V3 | no | A named `worker_done --outcome failed` instead of a stall. |
| C-005 | equal (V1, V3) | no | Orca-free commands; (b) also fails the subagent caller (New evidence 1). |
| C-006 | V3 | yes | One saved token (V2) is worth less than a named failure for a missed flag. |
| C-007 | V1 | no | Lowest cost; V3 adds one sentence and one check; V2 adds SA-2 amendments. |
| C-008 | equal (V1, V3) | yes | Both are cheap to change; reversing (b) means re-amending SA-2. |
| C-009 | equal | no | Same observation, and all three now reject the environment route. |
| C-010 | V3 | yes | It applies Orca's role-table rule (from V2) in the worker session, where SA-2 allows it. |
| C-011 | V3 | no | Only V3 enforces section 4 (`SPEC:151`). |
| C-012 | V2 | no | V2 found the precedent, though it supports an explicit switch. |
| C-013 | equal (V1, V3) | yes | The corrected guard keys on the same phase marker (`SPEC:257`). |
| X-001 | V3 | no | It reuses recognition WC-5 already needs; (b) makes command behaviour depend on it. |
| X-002 | V3 | yes | (b) only moves the stall; (c) converts it into a named failure. |
| X-003 | equal | no | Text checks are deterministic; every runtime switch is applied by a model. |
| X-004 | V3 | yes | Detection added later fits only in the worker session. |
| X-005 | equal | yes | V1 and V2 never refused P0 or `/sc:load` briefs; corrected V3 is inert there too. |
| X-006 | V1 | no | (b) saves one token; the report directory stays. |
| X-007 | V3 | no | It adds the fail-fast mechanism V1 lacks. |
| A-001 | equal | no | No surviving option reads the environment; `CAPS:149` and `CAPS:151` close that route. |
| A-003 | equal | no | A pasted flag and a pasted preamble both fail safe and are both visible. |
| A-005 | equal | yes | No variant, corrected V3 included, depends on it any longer. |
| A-009 | V3 | yes | The guard catches "template used, flag dropped"; no variant catches a brief written without the template. |

## Overall recommendation
I withdraw option (b) in both forms and recommend option (c) as corrected in R1-V3:16-21, with the amendments in R2-V1:76. Commands switch only on the standalone `--unattended` token (`SPEC:55`). Shipped in P1, the worker session refuses with `worker_done --outcome failed` in two cases: the flag and the command's `## Unattended mode` section disagree, or the command is one of the six coordinator-only commands. The guard sentence travels in the brief template, and `SPEC:79` is amended to read "where the command accepts it at this phase". Two facts decide against (b). It cannot reach the Agent-tool subagents that commands keep (`TL:1618`, `TL:1623`; `SPEC:145`), so it would need a flag anyway. And it needs SA-2 and non-goal 1 amended only to move the stall from the coordinator's memory to the worker's recognition. Option (b) should leave two things in the record: the D1 text at `SPEC:330` and item 13 at `SPEC:395` should state that `ORCA_TERMINAL_HANDLE` marks any live Orca terminal (`CAPS:149`, `CAPS:151`), and V3's guard should cite Orca's role table (`[G]` 38, 41) as its trigger.
