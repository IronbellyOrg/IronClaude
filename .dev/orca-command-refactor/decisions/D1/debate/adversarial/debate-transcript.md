# Adversarial Debate Transcript

## Metadata
- Decision: D1, how an IronClaude `/sc:` command knows it runs without a person (Orca worker) (`.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:328-331`)
- Mode: /sc:adversarial Mode A (compare existing files)
- Assembled: 2026-11-02T16:23Z by the debate orchestrator (not an advocate)
- Depth: standard
- Rounds completed: 2 (Round 1 statements, Round 2 rebuttals), plus Round 2.5 invariant probe
- Round 3: skipped (depth is standard; Round 3 runs only at depth deep)
- Convergence achieved: 100% on diff points (31 of 31 agreed). Final status: **BLOCKED_BY_INVARIANTS** (5 HIGH-severity UNADDRESSED invariants; see Convergence Assessment)
- Convergence threshold: 80%
- Focus areas: All
- Advocate count: 3 (Variant 1 = option a, explicit flag; Variant 2 = option b, detect Orca; Variant 3 = option c, flag plus worker-session guard)
- Inputs: `variant-{1,2,3}-original.md`, `diff-analysis.md`, `rounds/r1-variant-{1,2,3}.md`, `rounds/r2-variant-{1,2,3}.md`, `invariant-probe.md`
- The Round 1 and Round 2 subsections below are the round files copied verbatim. Each copied file keeps its own `#` title line, so a level-1 heading appears inside each round subsection.

## Round 1: Advocate Statements

### Variant 1 Advocate (option a, explicit `--unattended` flag)
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

### Variant 2 Advocate (option b, detect Orca)
# D1 Round 1: advocate for Variant 2 (option b, the command detects it is an Orca worker)

Citation key: `SPEC:N` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:N`; `CAPS:N` = `.dev/orca-command-refactor/inventory/orca-capabilities.md:N`; `[G] N` = line N of `orca-ide skills get orchestration` (re-read 2026-11-02; it reads bundled content without the Orca runtime, `CAPS:147`); `V1:N`/`V2:N`/`V3:N` = line N of the variant files. Every source cited below was re-read for this round.

## Position summary
I argue the strongest form of option (b): **preamble-only detection**. The environment route is dropped. A command is in unattended mode when its session is a "worker run" as the spec already defines it (a live Orca preamble with Task and Dispatch IDs, `SPEC:53`), with that rule written once in `WORKER-CONTRACT.md`. It removes the one switch a coordinator can forget and leaves a person's own session untouched. I also say plainly where it loses, mainly to Variant 3.

## Steelman
### Variant 1 (option a, `--unattended` flag)
The best case for (a): the trigger is a literal token that anyone can see in the brief and that a static check can grep. A person cannot trip it, because quoted text never counts (`SPEC:55`, AC-2.8 at `SPEC:269`). It names the condition rather than the tool, so any caller with no person present can use it (`SPEC:54`, `SPEC:361`). It fits SA-2 and non-goal 1 without amendment (`SPEC:170`, `SPEC:314`). The whole spec is already written around it (`SPEC:54`), so it costs least to adopt. Phase gating is explicit (`SPEC:187-195`). Its only stated failure, a forgotten flag, is caught by the 7.2 step-3 stall proof (`SPEC:238`).

### Variant 3 (option c, flag plus worker-session guard)
The best case for (c): it keeps everything (a) gets right and also turns (a)'s silent stall into an immediate, named `worker_done --outcome failed`. That is Orca's only guaranteed failure signal ("Never encode failure only in prose", `[G]` lines 88-90, `CAPS:73`). The check sits in the worker session, which already carries the Orca duties (WC-3, WC-5, WC-7, WC-12, `SPEC:67-76`), so commands stay Orca-free. The same guard stops a worker from running the coordinator-only commands (`SPEC:151`). It costs one rule in one file.

## Strengths claimed
1. **It uses Orca's own definition of a worker, which the spec already depends on.** Orca's role table: a prompt with "a live injected preamble with Task and Dispatch IDs" is a "Dispatched worker", and "No live preamble" means an "Ordinary terminal agent" (`[G]` lines 38, 41; `CAPS:148`). The spec takes that rule as its "Worker run" term (`SPEC:53`). Every worker-session duty depends on the model recognizing that preamble: asking (WC-3), `worker_done` (WC-5), the top-level rule (WC-7) and `check` (WC-12) (`SPEC:67-76`). So preamble-only (b) asks the model to make no recognition the contract does not already require.
2. **A person's own session is safe on this route.** A session a person started has no live preamble (`[G]` line 41), so prompts and outward defaults stay as they are (SA-1, `SPEC:169`). A false positive needs a person to paste a live preamble into their own session. That is the same kind of unenforced risk as a person pasting a brief's command line under (a) (A-003).
3. **No coordinator omission causes a silent stall.** Under (b) there is no switch to forget. The brief can still miss other content, such as the report directory, but that fails fast: WC-4 refuses and gives `failed` (`SPEC:68`; AC-1.5 at `SPEC:261`). Under (a), a missing flag leaves the worker parked on a prompt, and Orca reports that as "healthy, not failed" (`CAPS:52`, `CAPS:129`; `SPEC:47`).
4. **Phase gating works with no special case.** The detection text arrives with each command's `## Unattended mode` section in the phase that converts it (`SPEC:182`, `SPEC:187-195`). Flagless P0 smoke runs and `/sc:load` briefs (`SPEC:181`, `SPEC:191`, `SPEC:197`) therefore behave as they do today, so X-005 does not arise.
5. **The repo already infers "no person" without a flag.** `/sc:reflect` treats `claude --print` with no TTY as "the headless signal" (`src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md:239-242`), and SA-6 protects that rule (`SPEC:174`). Option (b) applies the same pattern to the signal an Orca worker actually has, because the print signal does not fire for one (`SPEC:391`).
6. **Per-command cost is the same as (a).** The detection rule is written once in `WORKER-CONTRACT.md`, which AC-C1 already excludes (`SPEC:205-211`). Each command's section refers to "unattended mode" as that file defines it, so commands stay free of Orca text. This corrects `V2:25`; see Concessions.

## Weaknesses identified
**Variant 1**
1. **A forgotten flag fails silently and late.** The worker parks on a prompt that Orca reports as healthy (`CAPS:52`, `CAPS:129`). The 7.2 proof needs a 900 s wait plus a transcript read (`SPEC:238`), and V1 admits it catches the problem "only after the fact" (`V1:19`).
2. **"Deterministic" covers the text only, not the run.** The coordinator that writes the flag is a model, and the command's parse is "applied by the model reading the rule, not by code" (`V1:22`). The runtime check AC-2.8 is manual (`SPEC:269`). Remembering a token is the same kind of model-applied step that V1 holds against (b) (X-003).
3. **No caller in scope needs caller-neutrality yet.** The spec says the mode "serves any caller" (`SPEC:54`), but `claude -p` appears only in AC-1.3's file-creation check (`SPEC:259`); A-007 records that no other caller is shown in scope.

**Variant 3**
1. **As written, the guard refuses legitimate briefs (X-005).** P0 smoke runs carry no flag (`SPEC:181`, `SPEC:191`), `/sc:load` never gains it (`SPEC:197`), and the guard is proposed for "P0 or P1" (`V3:23`).
2. **It relies on the same recognition it calls authoritative.** The guard runs only if the worker session recognizes its preamble (`V3:3`, `V3:8`). If that recognition is reliable enough to base a guard on, then `SPEC:330`'s main objection to preamble-only (b) is weaker than V1 and V3 imply (X-001).
3. **One citation range is overstated.** `[G]` line 78 says "The injected preamble is authoritative" about a worker's obligations; the identity rule is at lines 38 and 41, not 78-82 (`V3:8`).

## Concessions
1. **I drop the environment route.** By design, Orca uses `ORCA_TERMINAL_HANDLE` to identify the caller in any "live Orca terminal" (`CAPS:149`, `terminal-identity.js:213-215`), including a coordinator's tab, which is not a dispatched worker. In this subagent the variable was set on 2026-11-02 (`term_feb70160-...`). It is unsafe for SA-1 (`V2:13`).
2. **X-002 holds.** `V2:9` says detection removes "that whole failure class", which overclaims. A missed preamble produces the same stall, with no contract written. The failure moves from the coordinator's memory to the worker's recognition; it does not disappear.
3. **I withdraw the `CAPS:47` claim (OVERSTATED).** That line says only that Claude's task is passed on the command line (`promptInjectionMode: 'argv'`); it says nothing about the preamble.
4. **I correct the AC-C1 claim (WRONG).** The AC-C1 pattern would not match detection text, so it needs no exception. The real conflict is SA-2's sentence ("The only allowed mention of Orca ... as an example of a caller's question channel", `SPEC:170`) and non-goal 1's ban on "Orca-specific branching" (`SPEC:314`). Option (b) needs both amended, even in its strongest form.
5. **Shorter briefs is a small gain (X-006).** Option (b) removes one token; every brief still needs a report directory and the section 3 flags (`SPEC:57`, `SPEC:79`).
6. **Option (b) gives nothing to callers with no preamble,** such as CI or `claude -p` (`V2:18`).
7. **Variant 3 is better overall if X-005 is fixed.** It gets (b)'s main benefit (a forgotten switch fails visibly) without amending SA-2, and it degrades more gently. If the worker session misses its preamble under (c), the flagged command still writes its contract; under (b), the command prompts and stalls with nothing written.

## Shared assumption responses
| ID | Response | Reason |
|---|---|---|
| A-001 | QUALIFY | The three preconditions are unverified: `worker-list` paging (`CAPS:127`), remote workers, and the handle format. The conclusion stands on other evidence: Orca resolves the caller of any lifecycle command from `ORCA_TERMINAL_HANDLE` in a live Orca terminal (`CAPS:149`), including a coordinator's, which is not a worker. Variant 2 drops the environment route either way. |
| A-002 | ACCEPT | `CAPS:52` and `CAPS:129` quote `worker-show` line 16 directly. |
| A-003 | QUALIFY | It is a design intent, not a guard (`SPEC:329`). Option (b) has the matching risk: a person pasting a live preamble. Both are unenforced, and the quoted-argument rule covers only the typed-prompt case (`SPEC:55`). |
| A-004 | QUALIFY | All three options rest on a model applying a text rule at runtime (`V1:22`, `V3:17`, `SPEC:53`). Only static text checks are deterministic. The differences are in how each option fails, not whether it can fail. |
| A-005 | ACCEPT | The spec's own plan contradicts it (`SPEC:181`, `SPEC:191`, `SPEC:197`). It is a precondition of Variant 3 only; options (a) and (b) do not depend on it. |
| A-006 | QUALIFY | They are fixed only until the user rules on D1. Option (b) needs SA-2 and non-goal 1 amended (`SPEC:170`, `SPEC:314`), and that cost counts against it. |
| A-007 | QUALIFY | It is stated (`SPEC:54`), but no in-scope caller other than Orca is shown, so it should carry little weight. |
| A-008 | ACCEPT | `check --wait` returns on `worker_done` (`SPEC:238`), whereas a stall proof needs a timed-out wait plus a transcript read. |
| A-009 | QUALIFY | Nothing enforces use of the template (`SPEC:58`, `SPEC:79`). Under (b) and (c), leaving template content out fails fast (WC-4 refusal, or the guard); under (a), leaving out the flag stalls. |

## Per-point positions
| ID | Superior approach | One-line reason |
|---|---|---|
| S-001 | V3 | It meets both alternatives before making its own case. |
| S-002 | V1 | V2 never said which route it recommends; this round fixes that (preamble only). |
| S-003 | V1 | It commits to one mechanism; V2's original offered two and picked neither. |
| S-004 | V3 | It keeps the Orca-aware check in the worker session and the command side Orca-free; V2's strongest form still needs SA-2 amended. |
| S-005 | equal | `[G]` needs only `orca-ide` installed, not running (`CAPS:147`); the other keys need only the repo. |
| S-006 | V3 | Framing itself against both alternatives makes the comparison explicit. |
| S-007 | V1 | It covers both the person and the coordinator concretely. |
| C-001 | V1 and V3 | Preamble-only (b) is safe for people, but it relies on model judgment of context rather than on a visible token. |
| C-002 | V1 and V3 | They state outright that outward defaults stay on for people; (b) is safe here only on the preamble route. |
| C-003 | V1 | The trigger is visible to static checks; the runtime parse is model-applied under every option (X-003). |
| C-004 | V3 | A named failure with no SA-2 change; (b) replaces the forgotten flag with a missed preamble (X-002). |
| C-005 | V1 and V3 | (b) ties commands to Orca and does nothing for callers that have no preamble. |
| C-006 | V2 | One fewer token for the coordinator to remember; a small gain (X-006). |
| C-007 | V1 | The lowest cost; (b) also needs SA-2, non-goal 1, section 2.1 and AC-2.8 rewritten. |
| C-008 | equal | When commands refer to the contract file's definition of "unattended mode", changing the trigger means editing one file under any option. |
| C-009 | equal | All three read it as killing the environment route; I agree (A-001). |
| C-010 | V2 | It brought in Orca's own worker definition (`[G]` lines 38 and 41), which V3 then reuses. |
| C-011 | V3 | Only V3 blocks coordinator-only commands from being run by a worker. |
| C-012 | V2 | Only V2 checked the repo's headless precedent and showed that it misses Orca workers. |
| C-013 | V1 | It is the only one to state phase gating explicitly; (b) can follow it, but V2 did not say so. |
| X-001 | V3 | Both rely on preamble recognition, but a miss under (c) still leaves a flagged command that writes its contract. |
| X-002 | V1 and V3 | I concede that `V2:9` overclaims. |
| X-003 | equal | Every runtime switch is applied by a model; only text checks are deterministic. |
| X-004 | V2 | Adding Orca detection to commands later would break SA-2, so `V1:23`'s "cheap" add-on is not cheap. |
| X-005 | V1 and V2 | Neither refuses flagless P0 or `/sc:load` briefs; V3 must exempt them or ship the guard after P0. |
| X-006 | V1 | I concede: (b) removes one token, and the report directory and section 3 flags remain. |
| X-007 | V3 | The guard makes a forgotten flag fail at once instead of after a 900 s wait. |
| A-001 | equal | Every variant rejects the environment route; Orca's design (`CAPS:149`) supports that whatever the `worker-list` gaps. |
| A-003 | equal | (a) and (b) each depend on a person not pasting worker text: a command line under (a), a preamble under (b). |
| A-005 | V1 and V2 | Only V3 depends on this contradicted precondition. |
| A-009 | V2 and V3 | A template omission fails fast rather than stalling. |

### Variant 3 Advocate (option c, flag plus worker-session guard)
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

## Round 2: Rebuttals

### Variant 1 Rebuttal
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

### Variant 2 Rebuttal
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

### Variant 3 Rebuttal
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

## Round 2.5: Invariant Probe

Full findings: `invariant-probe.md` (fault-finder, not an advocate). It is not copied here; the gate result is in the Convergence Assessment. Summary: 23 findings; 7 ADDRESSED, 16 UNADDRESSED (HIGH 5, MEDIUM 8, LOW 3). The probe found that all three advocates converged on option (c) as corrected in R1-V3:16-21 with the Round 2 amendments, and that the five HIGH UNADDRESSED items are amendments the merged (c) needs, not arguments for (b).

## Round 3: Final Arguments

Not run. Depth is standard, and Round 3 runs only at depth deep. The Round 2 "Final per-point positions" tables are therefore the final positions used in the Scoring Matrix.

## Scoring Matrix

Method:
- Points scored: every S-NNN (7), C-NNN (13) and X-NNN (7) in `diff-analysis.md`, plus the four promoted shared assumptions A-001, A-003, A-005 and A-009 (`diff-analysis.md` line 84). Total: 31. The unpromoted A-002, A-004 and A-006 to A-008 are not debate points (A-004 is carried by X-001 and X-003).
- Positions: each advocate's Round 2 "Final per-point positions" table. Every one of the 31 points appears in all three Round 2 tables, so no Round 1 fallback was needed.
- Agreement: a point is agreed when at least 2 of 3 advocates give the same answer. An answer is either one variant, or a form of "equal". Bare "equal" and "equal (V1, V3)" count as the same answer (no single winner); the Winner column records the form the majority stated.
- Confidence: unanimous 90-99, majority 60-89, split 50. Within the band, higher when the losing side explicitly conceded (+10 in the majority band) and when the evidence was re-read and confirmed in the diff analysis or rounds. No point is given 100%.
- "R2-Vn #k" = row k of advocate n's Round 2 "Responses to criticisms" table. "V3" as winner means V3 as corrected in R1-V3:16-21 and amended in Round 2 wherever the original V3 text lost the point.

| Diff Point | Tag | V1 advocate | V2 advocate | V3 advocate | Agreement | Winner | Confidence | Evidence Summary |
|---|---|---|---|---|---|---|---|---|
| S-001 | L1 | equal | equal | equal | unanimous | equal (all) | 92% | All three call the opening order cosmetic. It does not affect the decision. |
| S-002 | L2 | V1 | V1 | V1 | unanimous | V1 | 96% | Only V1 names its own weakness (V1:19). V2's advocate conceded the original never chose a route (R2-V2 #1), and V3's advocate conceded it offered no self-critique (R2-V3 #10). |
| S-003 | L2 | equal (V1, V3) | equal (V1, V3) | equal (V1, V3) | unanimous | equal (V1, V3) | 94% | Both commit to one command-side switch; V3's extra check sits outside SA-2 and is not a second switch. V2 offered two routes and picked neither (V2:3), conceded at R2-V2 #1. |
| S-004 | L3 | V3 | V3 | V3 | unanimous | V3 | 95% | Command side as in V1 plus one check in the worker session, the one place allowed to know about Orca (`SPEC:58`, `SPEC:170`). V1's Round 1 objection (X-005) was withdrawn once the guard was keyed to the section (R2-V1 #7). |
| S-005 | L1 | V1 | equal | equal | majority | equal | 72% | `[G]` lines need only an installed `orca-ide`, not a running Orca (`CAPS:147`), and `CAPS:148` quotes the lines that matter (R2-V2 #14). V1's advocate holds that `SPEC`/`CAPS` keys are easier to re-read. |
| S-006 | L2 | V3 | V3 | equal | majority | V3 | 66% | V1 and V2 advocates credit V3 for framing itself against both alternatives. V3's own advocate rates the framing equal to V1's stand-alone clarity. |
| S-007 | L1 | equal (V1, V3) | equal (V1, V3) | equal (V1, V3) | unanimous | equal (V1, V3) | 92% | V1 and V3 both cover the person and the coordinator. V2's day-to-day section is one bullet restating a risk (DA S-007). |
| C-001 | L3 | equal (V1, V3) | equal (V1, V3) | equal (V1, V3) | unanimous | equal (V1, V3) | 97% | Under (a) and (c) no command reads the environment or the conversation (V1:8, V3:11). V2's environment route fails SA-1, conceded at R2-V2 #2. |
| C-002 | L3 | V1 | equal (V1, V3) | equal (V1, V3) | majority | equal (V1, V3) | 75% | WC-9 is command-side (`SPEC:73`), so V3 inherits V1's behaviour unchanged (R2-V3 #10). V1's advocate holds that only V1 argued it; the argument is V1's, the behaviour is shared. |
| C-003 | L3 | V3 | V3 | V3 | unanimous | V3 | 93% | Same text checks as V1 plus live runs that test the guard in both directions (R2-V3 New evidence 1). V2's advocate moved from V1 to V3 in Round 2. |
| C-004 | L3 | V3 | V3 | V3 | unanimous | V3 | 98% | A named `worker_done --outcome failed` replaces a stall proven only by a timed-out wait plus a transcript read (`SPEC:238`, `CAPS:52`). V1 conceded (R2-V1 #1) and V2 conceded X-002 (R2-V2 #3). |
| C-005 | L2 | equal (V1, V3) | equal (V1, V3) | equal (V1, V3) | unanimous | equal (V1, V3) | 96% | Identical Orca-free command sides satisfy SA-2 and non-goal 1 (`SPEC:170`, `SPEC:314`). V2 conceded that (b) breaks both and cannot reach Agent-tool subagents (R2-V2 #4, #11). |
| C-006 | L2 | V3 | V3 | V3 | unanimous | V3 | 94% | A missed or wrong flag is reported by name at once. V2's advocate switched from V2 to V3 in Round 2 because one saved token is worth less than a named failure. |
| C-007 | L2 | V1 | V1 | V1 | unanimous | V1 | 96% | V1 has the lowest cost. V3 adds one template sentence, one assertion and two live runs, which its advocate concedes (R2-V3 #12). |
| C-008 | L2 | V3 | equal (V1, V3) | equal (V1, V3) | majority | equal (V1, V3) | 70% | Dropping V3's guard returns exactly (a), and both command sides are equally cheap to keep. V1's advocate rates V3 higher because V1:23's "add detection later" is not cheap (X-004). |
| C-009 | L3 | equal | equal | equal | unanimous | equal (all) | 93% | All three cite the same partly verified observation. No surviving option reads the environment (`CAPS:149`, `CAPS:151`). |
| C-010 | L3 | V3 | V3 | V3 | unanimous | V3 | 93% | V3 applies Orca's role-table identity rule (`[G]` 38, 41; `CAPS:148`) in the worker session, where SA-2 allows it. V2 supplied the rule (U-004) and agrees it belongs there. |
| C-011 | L3 | V3 | V3 | V3 | unanimous | V3 | 97% | Only V3 turns section 4's prose ban (`SPEC:151`) into a refusal. V1 conceded (R2-V1 #6). |
| C-012 | L2 | V2 | V2 | V2 | unanimous | V2 | 95% | Only V2 checked reflect's `claude --print` precedent and showed it does not fire for an Orca worker (`SPEC:391`). All three note the finding supports an explicit switch, not (b). |
| C-013 | L3 | equal (V1, V3) | equal (V1, V3) | equal (V1, V3) | unanimous | equal (V1, V3) | 92% | V1 stated phase gating (V1:15). The corrected guard keys on the same `## Unattended mode` marker that AC-1.1 maintains (`SPEC:257`). |
| X-001 | L3 | equal (V1, V3) | V3 | equal (V1, V3) | majority | equal (V1, V3) | 75% | Neither (a) nor (c) makes command behaviour depend on preamble recognition, and a guard miss under (c) falls back to (a) (R2-V3 #6). V2's advocate rates V3 higher because a flagged command still writes its contract. |
| X-002 | L3 | V3 | V3 | V3 | unanimous | V3 | 98% | V2:9 ("removes that whole failure class") is contradicted by V2:17, conceded at R1-V2:36. (c) converts the forgotten switch into a named failure. |
| X-003 | L3 | equal | equal | equal | unanimous | equal (all) | 95% | V1 and V3 both conceded "deterministic" (R1-V1:39, R1-V3:44). Text checks are deterministic; the runtime switch is model-applied under every option. |
| X-004 | L2 | V3 | V3 | V3 | unanimous | V3 | 95% | Orca detection added to commands later breaks SA-2 and non-goal 1 (`SPEC:170`, `SPEC:314`); V1 conceded V1:23 is wrong (R1-V1:40). The only cheap later location is the worker session. |
| X-005 | L3 | V3 | equal | V3 | majority | V3 (corrected) | 78% | Keyed to the `## Unattended mode` section, the guard is inert in P0 and for `/sc:load` (`SPEC:191`, `SPEC:197`), and the symmetric form refuses the reverse mismatch (R2-V3 #11). The original V3:3 wording lost this point in Round 1 and was conceded (R1-V3:42); V2's advocate rates the corrected form equal. |
| X-006 | L2 | V1 | V1 | V1 | unanimous | V1 | 96% | (b) removes only the `--unattended` token; the report directory stays in every brief (`SPEC:57`). V2 conceded (R1-V2:39). |
| X-007 | L2 | V3 | V3 | V3 | unanimous | V3 | 96% | V3 adds the fail-fast mechanism V1 lacks. V1 conceded (R1-V1:38). |
| A-001 | L3 | equal (V1, V3) | equal | equal (V1, V3) | unanimous | equal | 93% | No surviving option reads the environment. `CAPS:149` and `CAPS:151` close the environment route by Orca's design, so A-001's unverified `worker-list` preconditions no longer decide anything. |
| A-003 | L3 | equal | equal | equal | unanimous | equal (all) | 92% | A pasted flag under (a)/(c) and a pasted preamble under (b) are both unenforced, opt-in and fail safe through WC-2 and WC-9 (`SPEC:66`, `SPEC:73`; R2-V1 #8, R2-V2 #13). |
| A-005 | L3 | equal (V1, V3) | equal | equal (V1, V3) | unanimous | equal | 94% | The assumption is false (`SPEC:191`, `SPEC:197`), and the corrected guard no longer depends on it. `SPEC:79` needs amending to "where the command accepts it at this phase" under every option. |
| A-009 | L2 | V3 | V3 | V3 | unanimous | V3 | 93% | The guard catches "template used, flag wrong" in either direction. No option catches a brief written without the template, and such a brief falls back to (a) (R2-V3 #3). |

Debate tally (used by the Step 3 tiebreaker): V1 wins 3 (S-002, C-007, X-006); V2 wins 1 (C-012); V3 wins 12 (S-004, S-006, C-003, C-004, C-006, C-010, C-011, X-002, X-004, X-005, X-007, A-009); no single winner 15. Unanimous 25, majority 6, split 0.

## Convergence Assessment
- Points resolved: 31 of 31
- Alignment: 100% (31 / 31; unanimous 25, majority 6)
- Threshold: 80%
- Unresolved points: none
- Round history: Round 1 positions already split on several points (for example X-005: V1 says V1, V2 says V1 and V2, V3 says corrected V3). Round 2 resolved every point. No oscillation was found: no point flipped winner back and forth.

### Taxonomy coverage (from the diff-analysis tags)

| Level | Points in scope | Agreed | Covered |
|---|---|---|---|
| L1 (surface: framing, order, citation style) | 3 (S-001, S-005, S-007) | 3 | yes |
| L2 (structure and approach: scope, cost, caller-neutrality) | 12 (S-002, S-003, S-006, C-005, C-006, C-007, C-008, C-012, X-004, X-006, X-007, A-009) | 12 | yes |
| L3 (state mechanics: safety, stalls, guard behaviour, phase state) | 16 (S-004, C-001, C-002, C-003, C-004, C-009, C-010, C-011, C-013, X-001, X-002, X-003, X-005, A-001, A-003, A-005) | 16 | yes |

All three levels have coverage, so the taxonomy gate passes and no forced round is needed.

### Invariant gate (Round 2.5)

HIGH-severity UNADDRESSED invariants (from `invariant-probe.md`):
- **INV-001**: the guard's key (`## Unattended mode` section) is checked by AC-1.1 in `src/superclaude/commands`, but the worker loads the installed `~/.claude/commands/sc/` copy or the gitignored project `.claude/` copy. Version skew makes the symmetric guard refuse correct briefs.
- **INV-005**: under D3 (a), pr-submit is "Coordinator or person only" (`SPEC:341`) but is not in the six-name list and has no section, so a flagless worker brief passes all three guard cases and runs pr-submit attended with outward defaults on.
- **INV-015**: "the guard runs before the command's first step" competes with the installed blocking skill-first rule (`CORE-CLAUDE:74`). If the skill starts first, side effects of coordinator-only commands (for example `/sc:pm`, `/sc:agent`) can happen before the refusal.
- **INV-016**: in-session Skill nesting is not defined: workflow invokes reflect via Skill with no flag (`WF:58`). From P2 the guard either refuses flagged workflow workers or its scope is undefined, and no check catches it.
- **INV-020**: the flag does not propagate to nested in-session skills (brainstorm into research, `BS:185`), so a flagged, converted worker can still stall. The consensus alone does not deliver "a worker never stalls".

```text
CONVERGENCE BLOCKED: 5 HIGH-severity UNADDRESSED invariant(s) detected
Blocking items: INV-001, INV-005, INV-015, INV-016, INV-020
These invariant violations must be resolved before convergence can be declared.
Action: Address the flagged items in a subsequent debate round or acknowledge as accepted risk.
```

```text
WARNING: 8 MEDIUM-severity UNADDRESSED invariant(s) detected
Items: INV-002, INV-008, INV-009, INV-010, INV-017, INV-018, INV-022, INV-023
These items do not block convergence but should be reviewed.
```

LOW UNADDRESSED (no action required by the gate): INV-003, INV-012, INV-013.

- **Status: BLOCKED_BY_INVARIANTS** (agreement 100% ≥ 80% threshold, all taxonomy levels covered, but 5 HIGH-severity UNADDRESSED invariants exist).
- How this run proceeds: depth is standard, so no further debate round is available. Steps 3 and 4 continue, and `refactor-plan.md` carries one planned change or one explicit accepted-risk entry for each blocking item. The probe notes that none of the five items favours option (b); each applies to (a) as well, or arises only from the guard's added scope.

## Advocates' final recommendations
- **Variant 1 advocate (option a)**: "I now recommend option (c) as corrected in Round 1, not (a) alone." (R2-V1:76)
- **Variant 2 advocate (option b)**: "I withdraw option (b) in both forms and recommend option (c) as corrected in R1-V3:16-21, with the amendments in R2-V1:76." (R2-V2:86)
- **Variant 3 advocate (option c)**: "Adopt option (c) as corrected in R1-V3:16-21, with the amendments from R2-V1:76 and this round." (R2-V3:79)
