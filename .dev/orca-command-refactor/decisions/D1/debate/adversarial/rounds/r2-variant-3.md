# D1 Round 2: rebuttal by the Variant 3 advocate (option c, flag plus worker-session guard)

Citation key: `SPEC:N` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:N`; `CAPS:N` = `.dev/orca-command-refactor/inventory/orca-capabilities.md:N`; `[G] N` = line N of `orca-ide skills get orchestration`; `V1:N`/`V2:N`/`V3:N` = variant files; `R1-V1:N`, `R1-V2:N`, `R1-V3:N`, `R2-V1:N`, `R2-V2:N` = earlier round statements in `rounds/`; `DA:N` = `diff-analysis.md`. Every citation newly relied on was re-read on 2026-11-02.

## Responses to criticisms
| # | Criticism | Source | Response | Concede / hold |
|---|---|---|---|---|
| 1 | As written, the guard refuses legitimate flagless worker briefs: P0 smoke runs, `/sc:load`, pre-conversion commands (X-005, A-005). | R1-V1:32; R1-V2:30; DA:52 | V3:3 was wrong. R1-V3:16-21 keys the guard to the command's `## Unattended mode` section: no command has one in P0 (`SPEC:191`), `/sc:load` never gains the flag (`SPEC:197`), and the guard ships in P1 (`SPEC:182`). Both other advocates accept the fix (R2-V1:14, R2-V2:24). | Concede (original); fixed |
| 2 | Fixing X-005 needs a per-phase list, so it is no longer "one sentence". | R1-V1:32 | The key is the section that AC-1.1 already maintains phase by phase, "and that no other command has one yet" (`SPEC:257`). The guard needs no list of its own. | Hold |
| 3 | The guard reaches only a worker whose brief carries the contract rule, so R1-V3:59 ("catches a brief written without the template") is unsupported. | R1-V1:33; R2-V1:12; R2-V2:28; A-009 | Correct, and R1-V3:59 overclaimed. Nothing loads `WORKER-CONTRACT.md` automatically (`SPEC:58`). The guard sentence must therefore travel in the brief template, which already fixes what every brief states (`SPEC:79`). It catches "template used, flag wrong". A brief written with no template gets exactly (a)'s behaviour, so it is never worse than (a). | Concede |
| 4 | "Deterministic" is overstated (X-003). | R1-V1:34; DA:50 | Already conceded (R1-V3:44). The brief text can be checked deterministically; the worker applying the rule is a model, as under (a) (V1:22). | Concede |
| 5 | The `[G]` 78-82 range is wrong for the identity rule. | R1-V1:35; R1-V2:32; DA:100 | Conceded. The trigger is Orca's role table, `[G]` 38 and 41, quoted at `CAPS:148` and adopted as "Worker run" at `SPEC:53`. | Concede |
| 6 | The guard relies on the same preamble recognition V3 calls "authoritative", which weakens `SPEC:330`'s objection to (b) (X-001). | R1-V2:31; DA:48 | Partly right. "Authoritative" describes Orca's rule, not how reliably a model applies it. The consequence differs, though. WC-5 already needs that recognition (`SPEC:69`). Under (c), a miss falls back to plain (a): the flagged command still writes its contract (R1-V2:41). Under (b), a miss changes what the command does (R2-V2:15). | Partly concede |
| 7 | The worker must open the command file before running it: one more model step, plus a path that must satisfy the dual-surface rule. | R2-V1:14; R2-V2:27 | Refinement: the check fires when the worker loads the command to run it. The worker runs the command itself at top level (WC-7, `SPEC:71`), so at that point the command text, with any `## Unattended mode` section (`SPEC:58`), is already in its context, before the command's first step. That removes the separate file read and the path. It is still a model step, which the live runs in New evidence 1 test. | Partly concede |
| 8 | A wrong guard text would misfire on every worker until fixed. | R1-V3:46 (self) | The risk is bounded and tested in both directions in P1 (New evidence 1). Removing the guard is one sentence (V3:23). | Hold |
| 9 | Commands not yet converted still stall on a gate. | R1-V3:43; R2-V2:31 | True, and the same under every option, because no option reaches a command before its phase. | Concede |
| 10 | V3 did not argue WC-9 outward defaults (C-002) or phase gating (C-013), and offered no self-critique (S-002). | DA:19, DA:31, DA:42 | True of the variant text. Behaviour is identical: WC-9 is command-side (`SPEC:73`), and V3's command side is (a)'s. V1 deserves the credit for the argument. | Concede |
| 11 | A one-way guard misses the reverse mismatch: the flag on a command that has not been converted, which `SPEC:79` invites. | R2-V1:35 | Adopted. The guard refuses when the flag and the section disagree in either direction. `SPEC:79` should read "where the command accepts it at this phase". | Concede |
| 12 | (c) costs more than (a). | R1-V1:21; R2-V1:56 | Yes. It adds one sentence in the template and the contract file, one static assertion and two live runs. It needs no command edits. | Concede |
| 13 | V3 is defined by reference to (a) (S-006). | DA:23 | Intentional. (c) is (a) plus a guard, so every fix to (a) applies to (c) unchanged, and dropping the guard returns exactly (a). | Hold |

## Updated assessment of other variants
**Variant 1 (option a).** Steelman: one switch, the lowest cost, commands free of Orca, explicit phase gating, and the only variant that tied D1 to WC-9's outward defaults (`SPEC:73`). Its Round 2 work also improved (c). The subagent-boundary point (`SPEC:71`, `SPEC:145`) shows the token is the one selector that reaches a command's own fan-out. The symmetric check closes the reverse mismatch that `SPEC:79` invites. I adopt both. Its advocate now recommends (c) (R2-V1:76), which leaves (a) alone with one open weakness, the silent stall (`SPEC:47`, `SPEC:238`). (a) remains the correct fallback: if the guard's live runs fail, removing one sentence returns exactly (a). I rank it second.

**Variant 2 (option b).** Steelman: it brought Orca's own definition of a worker into the debate (`[G]` 38, 41; `CAPS:148`), and that rule is now the guard's trigger. It also brought the reflect `--print` precedent (`SPEC:174`, `SPEC:391`), which shows a worker needs an explicit switch. Its advocate has withdrawn both routes (R2-V2:86). I agree the subagent finding is decisive: (b) would need a flag-like token for nested commands anyway (R2-V2:18). I rank it third. Its environment evidence (`CAPS:149`, and `CAPS:151`, where the variable is set in a dispatched worker that `status` does not report as a caller) should be recorded at `SPEC:330` and item 13 (`SPEC:395`), so the environment route is closed on Orca's design rather than on the unverified `worker-list` reading (A-001).

## New evidence
1. **A faulty guard is caught in both directions in P1, using checks the spec already has.**
   - **False refusal.** AC-1.2 runs a 7.2 live check on every P1 command with `--unattended` and its report directory (`SPEC:258`). A guard that refuses a correct brief fails AC-1.2 on its first run.
   - **Missed refusal.** One added P1 run with the flag omitted on a P1 command checks this direction. Its pass conditions are those AC-1.5 already uses for a refusal before any work: step 6 empty, and `worker_done --outcome failed` with no `--report-path` (`SPEC:261`; WC-5 "no contract exists" gives `failed`, `SPEC:69`).
   - **Telling (c) from (a).** The P2 run from R1-V3:26, a bare-topic `/sc:tdd` with the flag omitted, does this, because without the guard it stalls on tdd's gate (`SPEC:264`).
   - **P0 is untouched.** The guard ships after P0, so AC-0.4's smoke runs (`SPEC:254`) cannot be affected by it.
2. **What the guard covers.** It checks only the commands the worker session runs at top level. A nested command inside a command's own Agent-tool fan-out, such as tasklist's reflect agents (`SPEC:145`), runs below the worker session (`SPEC:71`) and is not guarded. That case relies on the static per-gate assertions of AC-2.1 (`SPEC:263`). A brief that runs `/sc:load` before a converted command (`SPEC:197`) passes the guard, because `/sc:load` has neither the flag nor the section.
3. **The guard needs no change when the spec's phase table changes.** It reads the section, and AC-1.1 (`SPEC:257`) checks that the section and the phase table agree. A phase-table edit therefore reaches the guard through an existing test, not through a second list.

## Updated shared assumption responses
| A-NNN | R1 response | R2 response | Reason for change |
|---|---|---|---|
| A-009 | QUALIFY ("(c) is the check that catches a brief written without the template") | QUALIFY | The answer is unchanged, but the reason is narrowed (response 3). The guard travels in the template, so it catches "template used, flag wrong" in either direction. No option catches a brief written without the template; such a brief falls back to (a). |

A-001 (QUALIFY), A-003 (QUALIFY) and A-005 (REJECT) are unchanged.

## Final per-point positions
| ID | Superior approach | Changed since R1? | One-line reason |
|---|---|---|---|
| S-001 | equal | no | Section order is cosmetic. |
| S-002 | V1 | no | Only V1 named its own weakness in the original text. |
| S-003 | equal (V1, V3) | yes | Both commit to one switch on the command side; V3's extra check sits outside SA-2 and is not a second switch. |
| S-004 | V3 | no | Commands as in V1, plus a check in the one place already allowed to know about Orca. |
| S-005 | equal | yes | `[G]` needs only an installed `orca-ide`, not a running Orca (`CAPS:147`), and `CAPS:148` quotes the lines that matter. |
| S-006 | equal | yes | V3's framing makes the comparison explicit; V1's stand-alone framing is clearer. Neither changes the decision. |
| S-007 | equal | no | V1 and V3 both cover the person and the coordinator. |
| C-001 | equal (V1, V3) | no | Commands read no environment or conversation; V2's environment route fails SA-1. |
| C-002 | equal (V1, V3) | yes | Identical WC-9 behaviour (`SPEC:73`); V1 argued it, and V3 inherits it. |
| C-003 | V3 | no | Same text checks as V1, plus live runs that test the guard in both directions (New evidence 1). |
| C-004 | V3 | no | A named `worker_done --outcome failed` instead of a timed-out wait plus a transcript read (`SPEC:238`). |
| C-005 | equal (V1, V3) | no | Identical command sides; only the token reaches nested fan-out (`SPEC:145`). |
| C-006 | V3 | no | A missed or wrong flag is reported by name at once. |
| C-007 | V1 | no | Lowest cost; V3 adds one template sentence, one assertion and two live runs. |
| C-008 | equal (V1, V3) | no | Both are cheap to change; dropping V3's guard returns exactly V1. |
| C-009 | equal | no | Same observation; no surviving option reads the environment. |
| C-010 | V3 | no | Applies Orca's role table (V2's find) in the worker session, where SA-2 allows it. |
| C-011 | V3 | no | Only V3 enforces section 4 (`SPEC:151`). |
| C-012 | V2 | no | V2 found the precedent, though it supports an explicit switch. |
| C-013 | equal (V1, V3) | yes | The corrected guard keys on the same phase marker V1 relies on (`SPEC:257`). |
| X-001 | equal (V1, V3) | yes | Neither makes command behaviour depend on preamble recognition; a guard miss under V3 falls back to V1. |
| X-002 | V3 | no | (b) moves the stall; (c) converts it into a named failure. |
| X-003 | equal | yes | Both V1 and V3 overclaimed; both are text-checkable and applied by a model at run time. |
| X-004 | V3 | no | Detection added later fits only in the worker session. |
| X-005 | V3 | no | Keyed to the section, the guard is inert in P0 and for `/sc:load`, and the symmetric form also refuses the reverse mismatch `SPEC:79` invites. |
| X-006 | V1 | no | (b) saves one token; the report directory stays (`SPEC:57`). |
| X-007 | V3 | no | It adds the fail-fast mechanism V1 lacks. |
| A-001 | equal (V1, V3) | no | Neither reads the environment; `CAPS:149` and `CAPS:151` close that route by design. |
| A-003 | equal | no | Same command-side exposure; the guard never runs in a session without a Task. |
| A-005 | equal (V1, V3) | yes | The corrected guard drops the assumption; `SPEC:79` needs amending under both. |
| A-009 | V3 | no | It catches "template used, flag wrong"; no option catches a brief written without the template (narrowed). |

## Overall recommendation
Adopt option (c) as corrected in R1-V3:16-21, with the amendments from R2-V1:76 and this round. Commands switch only on the standalone `--unattended` token (`SPEC:55`), exactly as (a) specifies. The worker session runs one check from P1 onward, at the point it loads each top-level command and before the command's first step. It refuses with `worker_done --outcome failed`, and runs nothing, in three cases:
- the flag is missing although the command has an `## Unattended mode` section;
- the flag is present although the command has no such section;
- the command is one of the six coordinator-only commands (`SPEC:150-160`).

The guard sentence goes in the brief template and in `WORKER-CONTRACT.md`. `SPEC:79` is amended to read "where the command accepts it at this phase". `SPEC:330` and item 13 (`SPEC:395`) record that `ORCA_TERMINAL_HANDLE` marks any live Orca terminal (`CAPS:149`, `CAPS:151`).

Three checks cover the guard:
- a static assertion in `test_worker_contract.py` that the rule is present;
- AC-1.2 for false refusals, plus one P1 run with the flag omitted;
- the discriminating P2 tdd run.

If those runs show that the guard misfires, delete its sentence and the design is exactly (a). Reject (b).
