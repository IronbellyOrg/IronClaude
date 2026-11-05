# D1 Round 2: rebuttal by the Variant 1 advocate (option a, explicit `--unattended` flag)

Citation key: `SPEC:N` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:N`; `CAPS:N` = `.dev/orca-command-refactor/inventory/orca-capabilities.md:N`; `[G] N` = line N of `orca-ide skills get orchestration`; `V1:N`/`V2:N`/`V3:N` = variant files; `R1-V1:N`, `R1-V2:N`, `R1-V3:N` = Round 1 statements in `rounds/`; `DA:N` = `diff-analysis.md`. Every citation newly relied on was re-read for this round on 2026-11-02.

## Responses to criticisms
| # | Criticism | Source | Response | Concede / hold |
|---|---|---|---|---|
| 1 | A forgotten flag fails silently and late: the worker parks on a prompt Orca calls healthy, and proof needs a 900 s wait plus a transcript read. | R1-V2:25; R1-V3:30; DA:33 (C-004) | Correct. `SPEC:47` names the silent stall as the real failure mode, and `SPEC:238` is the only catch (a timed-out wait plus a transcript read). V1 has no answer of its own; the answer is to adopt V3's guard. | Concede |
| 2 | "Deterministic" covers the text only. The coordinator writing the flag and the command parsing it are both model steps, and AC-2.8 is manual. | R1-V2:26; DA:50 (X-003) | Already conceded (R1-V1:39). One difference remains: a missing flag is visible in the text the worker received on its command line (`SPEC:70`), so it can be found afterwards. A missed preamble recognition leaves no token to find. | Concede (wording); hold (auditability) |
| 3 | No caller in scope needs caller-neutrality. | R1-V2:27; A-007 | Conceded for outside callers (R1-V1:41). New: one caller is in scope. A command's own Agent-tool fan-out stays (WC-7, `SPEC:71`), and tasklist's Stage 10.5 must pass `--unattended` to each reflect it fans out (`SPEC:145`). The flag is the one selector that crosses that boundary (New evidence 1). | Partly hold |
| 4 | `V1:23` (add detection later cheaply) conflicts with SA-2. | R1-V3:32; DA:51 (X-004) | Already conceded (R1-V1:40). The only cheap later addition is a worker-session rule, and the worker session is V3's location. | Concede |
| 5 | V1 depends on template discipline that nothing enforces. | R1-V3:31; A-009 | True, but V3's guard has the same dependency. Its rule lives in `WORKER-CONTRACT.md` (V3:17), and a worker reaches that file only through the brief or a command's pointer to it (`SPEC:58`, `SPEC:79`). So `R1-V3:59` ("catches a brief written without the template") is unsupported. The guard does add one case V1 misses: the template was used but the flag was dropped. To catch that case reliably, the guard sentence must be written into the brief template itself. | Partly concede |
| 6 | Coordinator-only commands have no guard. | R1-V3:33; DA:40 (C-011) | Correct. Section 4 is prose only (`SPEC:151`), and a fixed refusal list of six names is cheap. | Concede |
| 7 | X-005 is solved by keying the guard to the command's `## Unattended mode` section. | R1-V3:16-21 | This removes my main Round 1 objection. AC-1.1 already ties that section to exactly the commands that accept the flag in the current phase (`SPEC:257`). P0 has no such commands (`SPEC:191`), and `/sc:load` never gets the section (`SPEC:197`). The key therefore follows the phase plan with no list to maintain. The remaining cost is that the worker must read the command file before it runs the command. That read is one more model step, and V3's discriminating live run tests it (R1-V3:26). | Concede |
| 8 | Under (a), a person could paste a brief's command line, the same risk as pasting a preamble under (b). | R1-V2:48 | Neither risk is enforced against. Under (a) the paste fails safe: gates resolve to a default or to blocked, and outward defaults are off (WC-2, WC-9, `SPEC:66`, `SPEC:73`; opt-in per `SPEC:318`). The trigger is also visible in what the person typed. | Hold (equal) |
| 9 | V1 does not address the repo's headless precedent. | DA:41 (C-012) | V2 found it, and it supports the flag. Reflect's `--print` signal would not fire for an Orca worker (`SPEC:391`), so an explicit switch is needed. | Concede (credit V2) |
| 10 | V1 also relies on A-005, through the template's "including `--unattended`". | R1-V3:93 | Partly right. `SPEC:79` contradicts the phase table (`SPEC:187-191`) under every option. A coordinator who follows `SPEC:79` literally adds the flag to a command that has not been converted yet, and that command has no defined behaviour for the token. Fix: amend `SPEC:79` to read "where the command accepts it at this phase", and make the guard also refuse the reverse mismatch (New evidence 3). | Partly concede |

## Updated assessment of other variants
**Variant 2.** I accept its Round 1 reframing. Detection based only on the preamble is coherent, safe for a person's own session (`SPEC:53`), and costs no more per command than (a) (R1-V2:21). It still loses on three counts:
1. It needs SA-2 and non-goal 1 amended (R1-V2:38; `SPEC:170`, `SPEC:314`).
2. It degrades worse: a missed preamble stalls the worker with nothing written, as its advocate concedes (R1-V2:41).
3. New: the preamble does not reach Agent-tool subagents. Under (b), tasklist's reflect fan-out (`SPEC:145`) would need an explicit marker from the parent, which is a flag in all but name.

I rank V2 third.

**Variant 3.** The corrected guard (R1-V3:16-21) answers X-005 and ships in P1, the first phase in which commands gain the section (`SPEC:182`). It adds no new dependency on recognising the preamble, because WC-5 already needs that recognition to send `worker_done` (`SPEC:69`). I now rank it first, with three amendments:
1. Write the guard sentence into the brief template, not only into the body of the contract file (response 5).
2. Make the check symmetric: the flag must be present exactly when the command's `## Unattended mode` section is (New evidence 3).
3. Keep its live test (R1-V3:26).

## New evidence
1. **The flag crosses the subagent boundary; the preamble does not.** WC-7 keeps each command's own Agent-tool fan-out (`SPEC:71`). The tasklist row requires Stage 10.5 to "pass `--unattended` to each reflect so the headless rule applies", and that fan-out "runs one layer below the worker" (`SPEC:145`). A subagent starts from the prompt its parent writes, not from the parent's conversation, so it never sees the preamble. A token can be passed down to it; preamble recognition cannot.
2. **V3's key is already under test.** AC-1.1 asserts that exactly the commands accepting `--unattended` in a phase have the section, "and that no other command has one yet" (`SPEC:257`). The guard therefore inherits an existing static check and needs no list of its own.
3. **The spec already contains the reverse mismatch.** `SPEC:79` says each brief states "the exact command line including `--unattended`", while `SPEC:191` and `SPEC:197` say P0 briefs and `/sc:load` carry no flag. A one-way guard, which checks only for a missing flag, misses a coordinator who copies `SPEC:79` literally onto a command that has not been converted. A two-way check covers both directions in one sentence: refuse when the flag and the section disagree, or when the command is one of the six coordinator-only commands.

## Updated shared assumption responses
None changed. A-001 (QUALIFY), A-003 (QUALIFY), A-005 (REJECT) and A-009 (QUALIFY) keep their Round 1 answers. Responses 5 and 10 add reasons to A-009 and A-005 without changing the answers.

## Final per-point positions
| ID | Superior approach | Changed since R1? | One-line reason |
|---|---|---|---|
| S-001 | equal | no | Section order is cosmetic. |
| S-002 | V1 | no | Among the original variants, only V1 named its own weakness. |
| S-003 | equal (V1, V3) | yes | Both commit to one switch on the command side; V3's second check now sits cleanly outside SA-2. |
| S-004 | V3 | yes | Same command side as V1, plus a check in the one place already allowed to know about Orca; X-005 is fixed. |
| S-005 | V1 | no | `SPEC`/`CAPS` citations can be re-read without `orca-ide`. |
| S-006 | V3 | no | It frames itself explicitly against both alternatives. |
| S-007 | equal | yes | V1 and V3 both cover the person and the coordinator. |
| C-001 | equal (V1, V3) | no | Identical for people; V2's environment route fails SA-1. |
| C-002 | V1 | no | Only V1 argued WC-9 and the auggie-review default. |
| C-003 | V3 | no | Same text checks as V1, plus a live run that tells the designs apart. |
| C-004 | V3 | no | A named `worker_done --outcome failed` instead of a timed-out wait. |
| C-005 | equal (V1, V3) | no | Identical command sides, and both are free of Orca. |
| C-006 | V3 | no | A missed flag is reported by name at once. |
| C-007 | V1 | no | Lowest cost; V3 adds one sentence and one live check. |
| C-008 | V3 | no | The guard is removable in one place; V1:23 is not cheap (X-004). |
| C-009 | equal | no | All three cite the same observation. |
| C-010 | V3 | yes | It applies Orca's identity rule in the worker session, where SA-2 allows it; V2 put it in commands. |
| C-011 | V3 | no | Only V3 enforces section 4. |
| C-012 | V2 | no | V2 found the precedent, and it supports an explicit switch. |
| C-013 | equal (V1, V3) | yes | The corrected guard is keyed to the same phase marker V1 relies on (`SPEC:257`). |
| X-001 | equal (V1, V3) | yes | V3's guard reuses recognition that WC-5 already needs; only (b) makes commands depend on it. |
| X-002 | V3 | no | (b) renames the stall; (c) converts it into a named failure. |
| X-003 | equal | no | Both overclaimed "deterministic"; both are checkable by text and applied by a model at run time. |
| X-004 | V3 | no | Detection added later fits only in the worker session. |
| X-005 | V3 | yes | Keyed to the section, the guard does nothing in P0 or for `/sc:load`. |
| X-006 | V1 | no | (b) saves one token; the report directory stays. |
| X-007 | V3 | no | It adds the fail-fast mechanism V1 lacks. |
| A-001 | equal (V1, V3) | yes | Neither reads the environment; only V2 depends on the observation. |
| A-003 | equal | no | Neither risk is enforced against; under (a), a pasted flag fails safe. |
| A-005 | equal (V1, V3) | yes | The corrected guard drops the assumption; `SPEC:79` needs amending under both. |
| A-009 | V3 | yes | The guard catches "template used, flag dropped"; neither variant catches a brief written without the template. |

## Overall recommendation
I now recommend option (c) as corrected in Round 1, not (a) alone. Commands switch only on the standalone `--unattended` token, exactly as (a) specifies (`SPEC:55`). The worker session runs one check before the command, shipped in P1. It refuses with `worker_done --outcome failed` in two cases: the flag and the command's `## Unattended mode` section disagree, or the command is one of the six coordinator-only commands. The guard sentence travels in the brief template, so it reaches the worker before the command runs. `SPEC:79` is amended to read "where the command accepts it at this phase". Option (b) should be rejected even in its preamble-only form: it needs SA-2 amended, it degrades to a silent stall, and it cannot reach the Agent-tool subagents that commands keep (`SPEC:71`, `SPEC:145`).
