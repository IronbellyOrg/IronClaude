# D1 Round 1: advocate for Variant 1 (option a, explicit `--unattended` flag)

Citation key: `SPEC:N` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:N`; `CAPS:N` = `.dev/orca-command-refactor/inventory/orca-capabilities.md:N`; `[G] N` = line N of `orca-ide skills get orchestration` (re-run 2026-11-02 by this advocate); `V1:N`, `V2:N`, `V3:N` = line N of the variant files; `DA` = `diff-analysis.md`.

## Position summary
A command should switch to unattended behaviour only when its own command line carries the standalone token `--unattended`, because that is the one switch that cannot change a person's run, keeps commands free of Orca (SA-2, `SPEC:170`), and fits the spec's phase plan as written (`SPEC:187-197`). V3's guard is a good idea that V1 should adopt later in a narrowed form, but as written it refuses the spec's own legitimate flagless worker briefs (X-005), so V1 is the right base.

## Steelman
### Variant 2 (option b, detect Orca)
Strongest version: drop the environment route entirely (V2 itself argues against it, V2:13) and keep only preamble detection. Then the worker's identity comes from Orca's own rule, not a guess: "The current prompt contains a live injected preamble with Task and Dispatch IDs | Dispatched worker" and "No live preamble ... | Ordinary terminal agent" (`[G]` 38, 41, re-read 2026-11-02). A person's own session has no preamble, so the preamble route is safe for people (V2:14). And no coordinator can forget a switch that does not exist, so the silent stall that Orca reports as "healthy, not failed" (`CAPS:52`) has no flag-shaped cause (V2:9). What it gets right: the forgotten-flag stall is V1's real weakness (V1:19), and Orca's role table is the authoritative definition of a worker (U-004).

### Variant 3 (option c, flag plus worker-session guard)
Strongest version: keep every command-side property of V1 (V3:3, V3:11), and add one check in the only place that is already allowed to be Orca-aware, the worker session, which the spec already gives Orca duties (WC-3, WC-5, WC-7, WC-12 at `SPEC:67-76`). Orca's guide makes the preamble authoritative for that session ("The injected preamble is authoritative. A dispatched worker must:", `[G]` 78), so the guard adds no new recognition dependency: if the session cannot recognise its preamble, `worker_done` fails anyway. A forgotten flag then ends in `worker_done --outcome failed` with a reason, the only failure signal Orca guarantees (`CAPS:73`), instead of a stall the coordinator must prove with `worker-read` (`SPEC:238`). It also blocks a worker from running a section 4 coordinator-only command (V3:13, `SPEC:151`). What it gets right: it closes V1's known hole without breaking SA-2, and it names a concrete live test (V3:16).

## Strengths claimed
1. **A person's run cannot switch.** No command reads the environment or the conversation; only a standalone token outside quoted arguments counts (`SPEC:55`), checked by AC-2.8 (`SPEC:269`). This holds whether or not `ORCA_TERMINAL_HANDLE` is set in a person's tab, so V1's safety does not depend on A-001. Independent of the worker-list observation, Orca's own error text treats the variable as a property of any "live Orca terminal" (`CAPS:149`, quoting `terminal-identity.js:213-215`), and it is set in this advocate's environment (`term_feb70160-...`, checked 2026-11-02).
2. **Outward defaults stay with people.** WC-9 turns outward defaults off only under the flag (`SPEC:73`), so auggie-review's posting default (`SA-1`, `SPEC:169`) survives for a person working inside Orca (U-002).
3. **Commands stay Orca-free.** The flag names the condition, not the tool (Decisions row, `SPEC:361`), so it satisfies SA-2's "only allowed mention of Orca ... inside the contract file" (`SPEC:170`) and non-goal 1 (`SPEC:314`) with no exception.
4. **Fits the phase plan without special cases.** A command accepts the flag only once its gates are converted (`SPEC:187-195`, U-003). Under V1, a flagless brief simply gets today's behaviour, which is exactly what P0's smoke runs (`SPEC:191`), the section 3.1 ready commands before P2 (`SPEC:102`) and `/sc:load` (`SPEC:197`) need.
5. **Narrowest model judgment.** The parse is still a model applying a rule (V1:22, U-001), but recognising a literal token in its own command line is a smaller task than classifying its context (V2), and equal to V3's command side.
6. **Lowest cost.** One parse rule and one refusal list in `WORKER-CONTRACT.md`, plus a short `## Unattended mode` section per command (`SPEC:58`); no extra worker-session rule or phase-aware exemption list.

## Weaknesses identified
### Variant 2
1. **It does not pick a mechanism** (S-003, V2:3), and its own Safety section rejects the environment route (V2:13). A decision option that argues against half of itself cannot be implemented as written.
2. **It does not remove the failure class** (X-002). V2:9 says detection "removes that whole failure class"; V2:17 says a wrong model guess "is invisible until a run stalls". A missed detection reproduces the same stall, now with no token to check in the brief.
3. **It breaks SA-2 and non-goal 1** (`SPEC:170`, `SPEC:314`), which V2:18 concedes. Correction to V2:25: AC-C1's grep would not need an exception, because its lowercase `orca ... orchestration|worktree|terminal|agent` pattern (`SPEC:207`) would not match `ORCA_TERMINAL_HANDLE` or preamble prose (DA spot-check 6, WRONG). The conflict is with SA-2's text, which no grep enforces, so a violation would pass CI silently.
4. **Shorter briefs are overstated** (X-006). Every unattended brief still passes exactly one report directory (`SPEC:57`, WC-4 at `SPEC:68`); only the `--unattended` token disappears.
5. **Correction to V2:14:** `CAPS:47` says only that Claude's task is passed on the command line, not the preamble (DA spot-check 5, OVERSTATED). The testability gap stands anyway: no token for AC-1.1-style text checks.

### Variant 3
1. **The guard refuses legitimate flagless worker briefs** (X-005, A-005). P0 smoke runs use "each command's existing flags" with no `--unattended` (`SPEC:181`, `SPEC:191`); `/sc:load` "never gains the flag" (`SPEC:197`); troubleshoot, tdd, reflect and release-split run as workers from P0 under brief constraints (`SPEC:102`) but accept the flag only from P2 (`SPEC:193`). V3's rule ("no standalone `--unattended` ... it does not run it", V3:3) refuses all of these. Fixing it needs a per-phase list of which commands accept the flag, so it is no longer "one sentence" (V3:23) or a plain string check (V3:16).
2. **The guard only reaches a worker that already read the contract.** The rule lives in `WORKER-CONTRACT.md` (V3:17), which is reached through the brief template or a command's `## Unattended mode` section (`SPEC:58`, `SPEC:79`); nothing loads it automatically. A brief written without the template lacks both the flag and the pointer, so the guard catches only "template used, flag dropped" (A-009).
3. **"Deterministic" is overstated** (X-003): V3:17 itself says the rule is "prose read by a model". The same correction applies to V1:13 (see Concessions).
4. **Citation range.** Re-read `[G]` 78-82 (V3:8): line 78 supports the preamble's authority, lines 80-82 are the `ask` rule; the identity rule is `[G]` 38 and 41. Partly OVERSTATED, as DA flagged.

## Concessions
1. **V3 is better on the forgotten flag** (C-004, C-006, X-007). V1 catches it only after the fact (V1:19, `SPEC:238`); a named `worker_done --outcome failed` reaches the coordinator's `check --wait` loop sooner (A-008). V1 should adopt a narrowed guard: refuse a flagless brief only for commands the section 6 table lists as accepting the flag at the current phase (`SPEC:189-195`), and keep V3's coordinator-only refusal (C-011, `SPEC:150-160`), which V1 does not address.
2. **"Deterministic" in V1:13 is overstated** (X-003). Correct wording: the brief and the command files are checkable by text (AC-1.1, `SPEC:257`); the runtime switch is a model applying a rule and is checked only by live and manual runs (7.2, AC-2.8 at `SPEC:269`, which is manual).
3. **V1:23's "add detection later as an extra trigger" is wrong as stated** (X-004). Detection inside commands would break SA-2 (`SPEC:170`), which V1 itself relies on. It is cheap only if added in the worker session, which is V3's location.
4. **Caller-neutrality is a secondary benefit** (A-007). No non-Orca headless caller is planned; `claude -p` appears only in AC-1.3's file-creation check (`SPEC:259`). The primary reason for the flag is SA-1 and SA-2, not other callers.
5. **V2 contributes two facts V1 lacked**: Orca's role table as the definition of a worker (U-004), and that reflect's `claude --print` headless signal would not fire for an Orca worker (U-006, `SPEC:391`).

## Shared assumption responses
| A-NNN | Response | Reason |
|---|---|---|
| A-001 | QUALIFY | The worker-list half was not re-run here and its three preconditions (paging, observer role, handle format) are unconfirmed, so it is suggestive, not proof. It is consistent with `CAPS:149`, where Orca's error text ties the variable to any "live Orca terminal". V1 does not depend on it: the flag is immune either way. |
| A-002 | ACCEPT | `CAPS:52` and `CAPS:129` quote `[H:worker-show]` line 16 directly; DA spot-check 2 CONFIRMED. |
| A-003 | QUALIFY | Not enforced (`SPEC:329` is design intent). Accidental use is blocked by the parse rule (`SPEC:55`); deliberate use by a person is allowed, since `--unattended` is opt-in (`SPEC:318`) and it fails safe: outward defaults off (WC-9), gates resolve to default or blocked (WC-2). |
| A-004 | QUALIFY | All three rely on a model applying text rules. The flag narrows the runtime judgment to a literal token; the worker session must recognise its preamble under every variant for WC-3/5/7/12, so that dependency is shared, not V2- or V3-specific. |
| A-005 | REJECT | False per the spec: P0 smoke runs, `/sc:load` and pre-P2 ready commands are flagless worker briefs (`SPEC:191`, `SPEC:197`, `SPEC:102`). V1 does not need it; V3's guard does. `SPEC:79` ("including `--unattended`") should be amended to "where the command accepts it at this phase". |
| A-006 | ACCEPT | `SPEC:170`, `SPEC:314`; stated constraints. |
| A-007 | QUALIFY | `SPEC:54` states it, but no such caller is planned; a minor benefit only (Concession 4). |
| A-008 | ACCEPT | `check --wait --types "worker_done,..."` returns on `worker_done` (`SPEC:238`); a stall needs a timed-out wait plus a transcript read. |
| A-009 | QUALIFY | Nothing enforces the template. All variants depend on it for the report directory; V3 depends on it twice (flag and the pointer to its guard rule, `SPEC:58`). |

## Per-point positions
| ID | Superior approach | Reason |
|---|---|---|
| S-001 | equal | Section ordering is cosmetic. |
| S-002 | V1 | Advocates one option and names its own weakness; V2 argues against half of itself. |
| S-003 | V1 | One mechanism, no unresolved choice; V3 adds a second check that X-005 shows is not ready. |
| S-004 | V1 | Command-side logic identical to V3; V3's worker-session rule needs a phase-aware list first. |
| S-005 | V1 | `SPEC`/`CAPS` citations can be re-read without running Orca. |
| S-006 | V3 | Positions itself explicitly against both other options. |
| S-007 | V1 | Covers both the person and the coordinator day to day. |
| C-001 | equal | V1 and V3 are identical for people; V2's environment route fails SA-1. |
| C-002 | V1 | Only V1 ties D1 to WC-9 and the auggie-review default. |
| C-003 | V3 | Same command-side checks as V1 plus one concrete guard test (V3:16). |
| C-004 | V3 | Fast named failure beats an after-the-fact stall proof (conceded). |
| C-005 | equal | V1 and V3 command sides are identical and Orca-free. |
| C-006 | V3 | Coordinator gets a named failure instead of a stall to diagnose. |
| C-007 | V1 | Lowest cost; V3 needs the guard plus exemptions to fix X-005. |
| C-008 | V3 | V1:23 conflicts with SA-2 (X-004); V3's guard is removable in one place. |
| C-009 | equal | Same observation used by all; only V1 and V3 are immune to it. |
| C-010 | V2 | Grounds worker identity in Orca's role table (`[G]` 38, 41). |
| C-011 | V3 | Only V3 stops a worker running a coordinator-only command. |
| C-012 | V2 | Only V2 shows reflect's `--print` signal would not fire for a worker. |
| C-013 | V1 | Only V1 accounts for phase gating, which X-005 shows V3 must handle. |
| X-001 | V1 | V1's switch needs no preamble recognition; V3's guard reuses a dependency all variants share; V2 adds one inside commands. |
| X-002 | V3 | (b) only renames the stall; V3 converts a missed flag into a visible failure. |
| X-003 | equal | V1 and V3 both overclaim; both are text-checkable at the brief and model-applied at runtime. |
| X-004 | V3 | Later detection fits only in the worker session, V3's location. |
| X-005 | V1 | No guard, so P0, `/sc:load` and pre-P2 ready-command briefs run as planned. |
| X-006 | V1 | `--report-dir` stays in every brief, so V2's saving is one token. |
| X-007 | V3 | V3 adds a mechanism V1 lacks (conceded). |
| A-001 | V1 | V1's safety holds whether or not the observation generalises. |
| A-003 | equal | V1 and V3 share the parse rule and the opt-in, fail-safe behaviour. |
| A-005 | V1 | Only V1 does not depend on the false assumption. |
| A-009 | V1 | V1 depends on the template once; V3's guard depends on it twice. |
