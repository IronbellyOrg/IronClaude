# Round 1, Variant 3 advocate: option (c), flag plus worker-session guard

Citation key as in the variants: `SPEC:N` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:N`; `CAPS:N` = `.dev/orca-command-refactor/inventory/orca-capabilities.md:N`; `[G] N` = line N of `orca-ide skills get orchestration` (re-read 2026-11-02); `DA` = `diff-analysis.md` in this folder. Every source cited below was re-read for this round.

## Position summary
Commands switch only on the standalone `--unattended` token, exactly as option (a). The worker session, which already owns Orca duties, adds one pre-run guard: if the Task's command has an `## Unattended mode` section but the command line lacks the flag, or the command is one of the six coordinator-only commands, it does not run it and sends `worker_done --outcome failed`. This corrects my original wording, which X-005 rightly showed would have refused the spec's own Phase 0 smoke runs.

## Steelman
### Variant 1 (option a)
The strongest case for (a) is that it has one mechanism, and that mechanism is already the spec's design (`SPEC:328-331`). It is caller-neutral (`SPEC:54`), cannot switch a person's run because only a standalone token counts (`SPEC:55`, AC-2.8 at `SPEC:269`), and is phase-gated so the flag never promises behaviour a command lacks (`SPEC:187-195`). Every extra rule is another place a model can misapply prose. X-005 shows my guard, as first written, would have broken AC-0.4. The forgotten-flag stall is still caught by 7.2 step 3 (`SPEC:238`). (a) asks the reviewer to trust nothing beyond the parse rule.

### Variant 2 (option b)
The strongest case for (b) is that it uses Orca's own definition of a worker. "The current prompt contains a live injected preamble with Task and Dispatch IDs" is a "Dispatched worker", and "No live preamble" is an "Ordinary terminal agent" (`[G]` 38, 41; `CAPS:148`). A person's session has no preamble, so the preamble route cannot fire for a person. A coordinator cannot forget a flag that does not exist, and the silent "healthy, not failed" stall (`CAPS:52`, `CAPS:129`) is the most expensive failure in the contract (`SPEC:47`).

## Strengths claimed
1. **Direct answer to X-005: the guard is keyed to the `## Unattended mode` section, not to "every brief".** The spec already makes that section the marker of a command that accepts the flag. AC-1.1 asserts that exactly the commands accepting `--unattended` in the current phase have it, "and that no other command has one yet" (`SPEC:257`). The corrected rule is: refuse when the Task's command file has an `## Unattended mode` section and the line lacks a standalone `--unattended`. Three consequences follow:
   - In P0 no command has the section (`SPEC:191`: "none (smoke runs use each command's existing flags)"), so the AC-0.4 smoke runs (`SPEC:254`) run unchanged. AC-0.4 then acts as the guard's regression check.
   - `/sc:load` "never gains the flag" (`SPEC:197`), so it is never refused.
   - The guard follows each phase with no list to maintain.

   The guard ships with P1, the first phase with flag-accepting commands (`SPEC:182`), not in P0.
2. **A forgotten flag fails fast and in the form Orca guarantees.** Orca's only reliable failure signal is the explicit outcome: "Never encode failure only in prose" (`[G]` 88-90; `CAPS:73`). Under (a) the coordinator learns of a stall only after `check --wait` times out (900000 ms in the 7.2 recipe) and a transcript read shows a final turn with no `worker_done` (`SPEC:238`; `CAPS:126`). Under (c) the same mistake returns a `worker_done --outcome failed` at once. The spec already accepts a pre-run refusal with no contract (AC-1.5, `SPEC:261`; WC-5 "no contract exists" gives `failed`, `SPEC:69`).
3. **It adds no new dependency on reading the preamble (answers X-001).** The worker session must already recognize its preamble to send `worker_done`, heartbeats and `check` (WC-3, WC-5, WC-7, WC-12, `SPEC:67-76`). [G] line 78 says "The injected preamble is authoritative". [G] line 38 is the identity rule; my original "`[G]` 78-82" range for identity was overstated (DA line 100). If the session misses the preamble, every option already fails the same way, with no `worker_done`. (c) reuses that recognition and does not add a second one.
4. **Safety for people is identical to (a).** Commands read neither the environment nor the conversation (SA-1, `SPEC:169`; SA-2, `SPEC:170`). The guard runs only in a session that has a Task. A false positive would be a visible refusal message, never a silent loss of prompts.
5. **It enforces section 4 mechanically.** The six coordinator-only commands "are never dispatched as workers" (`SPEC:151`), but today only prose says so. The guard refuses them by a fixed list of six names.
6. **Cost and testability.** The cost is one rule in the worker-session part of `WORKER-CONTRACT.md` (`SPEC:58`), with no command edits. Two checks cover it: a `test_worker_contract.py` assertion that the rule text is present (the AC-0.1 style, `SPEC:251`), and one P2 live run. In that run, `/sc:tdd "auth" --output <f> --report-dir <d>` without `--unattended` must end with `worker_done --outcome failed`, an empty step 6 and no `agentWait`. Without the guard, the same bare topic stalls on tdd's gate (`SPEC:113`, `SPEC:264`), so the run tells the two designs apart.

## Weaknesses identified
### Variant 1 (option a)
1. **It knowingly leaves the stall open.** V1:19 names the forgotten-flag stall as its known weakness, caught "only after the fact". Orca reports the stalled worker as healthy (`CAPS:52`, `CAPS:129`), so each miss costs a full wait timeout plus a transcript diagnosis (`SPEC:238`).
2. **It depends on template discipline that nothing enforces.** Nothing makes a coordinator write its brief from the template (DA A-009; `SPEC:58`, `SPEC:79` only describe it).
3. **"Add detection later cheaply" (V1:23) conflicts with the SA-2 that V1 itself relies on.** Adding Orca detection to commands is forbidden by `SPEC:170` and non-goal 1 (`SPEC:314`) (DA X-004). The cheap later extension is a worker-session rule, which is option (c).
4. **Coordinator-only commands have no guard.** Section 4 is prose only (`SPEC:151`).

### Variant 2 (option b)
1. **It contradicts itself.** "Removes that whole failure class" (V2:9) versus "a wrong guess by the model is invisible until a run stalls or a prompt disappears" (V2:17). A missed detection reproduces the stall (DA X-002).
2. **The environment route is unsafe for people, and V2 says so itself** (V2:13; `SPEC:330`; UNVERIFIED item 13, `SPEC:395`). V2 never picks between its two routes (DA S-003).
3. **It puts Orca-specific branching into every command.** That breaks SA-2's "only allowed mention of Orca" rule (`SPEC:170`) and non-goal 1 (`SPEC:314`). It does nothing for `claude -p` or CI callers (V2:18). I do not repeat V2's AC-C1 claim, which DA marked WRONG: the conflict is with SA-2's text, not with the AC-C1 grep.
4. **Briefs do not get shorter.** Every unattended brief still passes exactly one report directory (`SPEC:57`; WC-4 at `SPEC:68`), so `--unattended` is the only token (b) removes (DA X-006).

## Concessions
1. My original guard wording ("if the command line in its Task has no standalone `--unattended` ... it does not run it", V3:3) was wrong. It would have refused the P0 smoke runs and every pre-conversion section 3.1 brief (`SPEC:102`, `SPEC:191`). Strength 1 corrects it.
2. Because of that correction, the guard does not cover section 3.1 commands before their conversion phase. For example, tdd, troubleshoot, reflect and release-split before P2 still stall when an input hits a gate (`SPEC:102`). (a) and (c) behave the same there.
3. "Deterministic" (V3:16) was overstated (DA X-003). A text check of the brief is deterministic. The worker session applying the guard is a model reading prose, like every WC row and like (a)'s parse rule (V1:22).
4. V1 is better on simplicity, and it argued the WC-9 outward-default point (C-002) and phase gating (C-013) explicitly, where my variant did not. V2's `claude --print` precedent (C-012) is a contribution I lacked.
5. The guard adds a second rule a coordinator must understand. If the guard text is wrong, it misfires on every worker until it is fixed. Removing it is one sentence (V3:23), but the risk is real.

## Shared assumption responses
| A-NNN | Response | Reason |
|---|---|---|
| A-001 | QUALIFY | The `ORCA_TERMINAL_HANDLE` evidence is only partly verified. The variable is set in this advocate subagent too (`term_feb70160-...`, 2026-11-02). I did not re-run `worker-list` (out of bounds), and its 100-row page and remote filtering (`CAPS:127-128`) were not ruled out. (c) does not depend on A-001: it never reads the environment. The finding only weakens (b)'s environment route. |
| A-002 | ACCEPT | `CAPS:52` and `CAPS:129` quote `[H:worker-show]` line 16 directly. |
| A-003 | QUALIFY | `SPEC:329` states this as intent, not as an enforced rule. A person who types the flag gets the unattended mode by choice, which non-goal 5 (`SPEC:318`) permits because the mode is opt-in. Under (c) the guard never runs in a person's session, because a person's session has no Task. |
| A-004 | QUALIFY | Every option relies on a model applying text rules. (c) relies on two such rules: the parse rule, shared with (a), and preamble recognition, which WC-3, WC-5, WC-7 and WC-12 already require. It adds no third. |
| A-005 | REJECT | Not every legitimate brief carries the flag (P0, `/sc:load`, pre-conversion commands; `SPEC:191`, `SPEC:197`, `SPEC:187`). The corrected guard therefore assumes only that a brief carries the flag when its command has an `## Unattended mode` section. That is the spec's own rule (`SPEC:79`, `SPEC:187`). |
| A-006 | ACCEPT | `SPEC:170` and `SPEC:314`. (c) keeps all Orca awareness in the worker session, which SA-2 does not govern. |
| A-007 | QUALIFY | `SPEC:54` makes the mode caller-neutral, but no non-Orca caller is planned. The point is a tie between (a) and (c), and counts against (b). |
| A-008 | ACCEPT | `check --wait` returns on `worker_done` (`[G]` 108, quoted at `CAPS:63`; `SPEC:238`), while proving a stall needs a timed-out wait plus a transcript read (`CAPS:126`). |
| A-009 | QUALIFY | True as a precondition for (a). (c) is the check that catches a brief written without the template. |

## Per-point positions
| ID | Superior approach | One-line reason |
|---|---|---|
| S-001 | equal | How a variant opens does not change the decision. |
| S-002 | V1 | V1 names its own weakness. V3 offered no self-critique (now added in Concessions). V2 argues against itself without choosing. |
| S-003 | V3 | One switch in commands plus one check that sits outside SA-2. V2 never picks a route. |
| S-004 | V3 | The switch is in command files as in V1. The Orca-aware check is in the one file that already holds worker-session duties (`SPEC:58`). V2 spreads it across every command. |
| S-005 | V1 | `SPEC`/`CAPS` keys can be re-read without Orca. `[G]` needs `orca-ide skills get`, which is read-only but still extra. |
| S-006 | V1 | Standing alone is clearer. V3's "same as (a)" framing still holds because the command side is identical. |
| S-007 | equal | V1 and V3 both cover the person and the coordinator. |
| C-001 | equal (V1/V3) | Commands read no environment or conversation under either. V2's environment route fails SA-1 (`SPEC:330`). |
| C-002 | V1 | V1 argued WC-9 explicitly. V3 inherits the same behaviour but did not argue it. |
| C-003 | V3 | Same text checks as V1, plus one discriminating live run (Strength 6). Neither is runtime-deterministic (X-003). |
| C-004 | V3 | An immediate `worker_done --outcome failed` instead of a timed-out wait plus a transcript read (`SPEC:238`). |
| C-005 | equal (V1/V3) | Identical command side. Both satisfy SA-2 and non-goal 1. V2 does not. |
| C-006 | V3 | The coordinator still writes the flag, but a miss is named at once instead of being diagnosed later. |
| C-007 | V1 | V1 has the lowest cost. V3 adds one rule and two checks, which is small but more than zero. |
| C-008 | equal (V1/V3) | Both are cheap to undo. V3's guard is one sentence. V1's "add detection later" is not cheap (X-004). |
| C-009 | equal | All three cite the same partly verified observation (A-001). |
| C-010 | V3 | It uses Orca's identity rule (`[G]` 38) where SA-2 allows it: in the worker session, not in commands. |
| C-011 | V3 | Only V3 makes section 4 (`SPEC:151`) more than prose. |
| C-012 | V2 | Only V2 shows the `claude --print` precedent does not fire for an Orca worker (`SPEC:391`). |
| C-013 | V1 (V3 corrected to match) | V1 stated phase gating. The corrected guard is keyed to the same `## Unattended mode` marker (`SPEC:257`). |
| X-001 | V3 | Preamble recognition is already required by WC-3, WC-5, WC-7 and WC-12. (c) reuses it inside the worker session, while (b) makes every command depend on it. |
| X-002 | V3 | V2 cannot remove the stall class (V2:17 against V2:9). V3 converts the stall into a named failure for every flag-accepting command. |
| X-003 | V1 | V1 admitted the runtime parse is model-applied (V1:22). V3 overstated "deterministic" (conceded). |
| X-004 | V3 | Adding detection later belongs in the worker session. V1's in-command route conflicts with `SPEC:170` and `SPEC:314`. |
| X-005 | V3 (corrected) | Keyed to the `## Unattended mode` section, the guard is inert in P0 (`SPEC:191`), never refuses `/sc:load` (`SPEC:197`), and ships in P1. |
| X-006 | V1 | (b) removes only `--unattended`. The report directory stays (`SPEC:57`). |
| X-007 | V3 | V3 adds the fail-fast mechanism V1 lacks. The live run in Strength 6 tests it. |
| A-001 | equal (V1/V3) | Neither depends on the environment observation. It matters only to V2. |
| A-003 | equal (V1/V3) | Same command-side exposure. The guard never runs in a person's session. |
| A-005 | V3 (corrected) | The corrected guard drops this assumption. V1 relies on it only through the template. |
| A-009 | V3 | The guard catches a brief written without the template. V1 relies on the coordinator using it. |
