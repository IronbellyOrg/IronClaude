# Adversarial Debate Transcript

## Metadata
- Depth: quick
- Rounds completed: 1 (Round 2, Round 2.5 invariant probe and Round 3 skipped: depth=quick)
- Convergence achieved: 64.3% (9 of 14 diff points)
- Convergence threshold: 80%
- Focus areas: All
- Advocate count: 2 (one per variant, Mode A; no `--agents` spec, so each advocate ran as a general-purpose agent on the session model)
- Mode: `--unattended` (no interactive checkpoints; every decision auto-resolved with a recorded rationale)
- Taxonomy coverage after Round 1: L1 = 2 points, L2 = 6, L3 = 6; every level addressed, so no forced round was triggered
- Shared-assumption omissions: none (both advocates answered A-001, A-002 and A-003 with ACCEPT, REJECT or QUALIFY)
- Advocate statements below are the verbatim files `round1-advocate-A.md` and `round1-advocate-B.md` from this directory, with their headings shifted down two levels

## Round 1: Advocate Statements
### Round 1 advocate statement: Variant A (explicit `--unattended` flag)

#### Position
Citation key: `V-A:N` / `V-B:N` = line N of `variant-1-original.md` / `variant-2-original.md`. `SPEC4:N` = line N of `.dev/orca-command-refactor/specs/history/spec-v4-after-round3.md`. `SPEC-LIVE:N` = line N of the current `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. `CAPS:N` = `.dev/orca-command-refactor/inventory/orca-capabilities.md:N`. `WC` = `/home/coder/.claude/WORKER-CONTRACT.md`.

**Baseline fact the lead must know first.** Both variants cite `SPEC:N` line numbers that match `spec-v4-after-round3.md` (the spec before the D1 decision), not the live spec. Example: `SPEC4:330` is the "Detect Orca ... prompts would vanish" text, but `SPEC-LIVE:330` is an AC-2.6 table row. In the live spec, D1 is already settled at `SPEC-LIVE:401`: "Option (c): `--unattended` is the only switch; from P1 the worker session also applies the brief guard. Commands never detect Orca." UNVERIFIED item 13 moved to `SPEC-LIVE:448` and now says "D1 no longer depends on it: no option the spec keeps reads the variable." This affects both variants equally, and the content of every cited line I checked is intact in v4. I checked against v4.

**My position.** The trigger for unattended mode should be a standalone `--unattended` token on the command line, not detection of Orca by the command. Five reasons, strongest first:

1. **The flag is scoped to one invocation; the preamble is scoped to a whole session.** A person who takes over a worker terminal (the live spec names "a taken-over terminal" among possible writers, `SPEC-LIVE:79`) still has the preamble in context. Under B every command the person then types would silently drop its prompts. Under A the person's typed command has no flag, so it prompts as today (SA-1, `SPEC4:169`).
2. **It can be tested.** `SPEC4:257` (AC-1.1) asserts per phase which commands carry an `## Unattended mode` section; `SPEC4:269` (AC-2.8) live-checks the quoted-token rule. B has no equivalent and says so (`V-B:17`).
3. **It keeps commands Orca-free.** Non-goal 1 forbids "Orca-specific branching" (`SPEC4:314`) and SA-2 keeps commands runnable in other projects (`SPEC4:170`). B's own text admits it ties commands to Orca (`V-B:18`).
4. **It serves any caller with no person** (`claude -p`, CI), because the flag "names the condition (no person), not a tool" (`SPEC4:361`, `SPEC4:54`).
5. **Its one real weakness (a forgotten flag causes a silent stall) is better fixed by a refuse-only guard in the worker session than by moving the trigger into every command.** That is what the live spec adopted (`WC` "Brief guard", case 1: every copy of the command has an `## Unattended mode` section and the line lacks the flag, so the worker refuses with `guard refused: brief lacks --unattended`). I treat that as Variant A plus a backstop, and I argue it below as the answer to B's best point.

#### Steelman of Variant B
The strongest version of B, stated so B's advocate would sign it:

> The failure that actually hurts in production is the silent stall. A command that prompts inside a worker is reported by Orca as "healthy, not failed" (`CAPS:52`, `CAPS:129`; `SPEC4:47`: "the real failure mode ... is a silent stall with no `worker_done`"). Under A that failure is one forgotten token away, and the coordinator is a model writing prose briefs; A's own text admits the catch comes only "after the fact" (`V-A:19`). Orca already defines a worker precisely: a session whose current prompt carries a live preamble with Task and Dispatch IDs; no preamble means "Ordinary terminal agent" (`CAPS:148`, `SPEC4:53`). So drop the environment variable (unsafe, as both sides agree) and detect the preamble only. A person's own session has no preamble, so people are safe, and the coordinator cannot forget anything. The repo already has a precedent of commands reading their run context (reflect's `claude --print` headless rule, `remediation-handoff.md:239-242`, which I re-read and confirm). Briefs get shorter and 35 commands need no new flag token.

What B genuinely gets right:
- The forgotten-flag stall is real, silent, and not caught by Orca. A's mitigations (brief template, step-3 stall proof, `SPEC4:238`) are after the fact.
- A's "detection would misfire" headline (`V-A:9`) is supported only by an observation about the environment variable. It says nothing about the preamble route. B is right to separate the two (`V-B:13-14`).
- B correctly identifies Orca's own role table as the authoritative definition of a worker (`CAPS:148`).
- B correctly notes that the reflect headless signal would not fire for an Orca worker (`SPEC4:391` says "assumed not"; UNVERIFIED), so no existing command-side signal exists.

#### Key strengths claimed
- **Invocation-scoped trigger (L3, state mechanics).** The flag lives in the one command line the coordinator wrote. It cannot leak into a later command typed in the same session. The flag parse rule (`SPEC4:55`) makes even quoted text inert: `/sc:troubleshoot "the worker ignores --unattended"` stays a person's run, and AC-2.8 (`SPEC4:269`) checks it live.
- **Deterministic and greppable.** AC-1.1 (`SPEC4:257`) asserts per phase which commands carry the section and that no other command has one yet. The live 7.2 checks (`SPEC4:234-238`) then show the flag's effect, including the step-3 stall proof.
- **Phase gating.** `SPEC4:187-195` lists which commands accept the flag after each phase, so the flag never promises behaviour a command lacks. Detection cannot be phase-gated this way: it would activate in a command the moment the worker runs it, converted or not.
- **Outward defaults stay a person's.** Under `--unattended`, outward defaults are off (WC-9, `SPEC4:73`). Only a flag the coordinator writes can turn that off, so a person working in Orca keeps, for example, auggie-review's posting default (`SPEC4:169`).
- **Commands stay Orca-free** (non-goal 1 `SPEC4:314`, SA-2 `SPEC4:170`) and the mode is caller-neutral (`SPEC4:54`, `SPEC4:361`).
- **Per-command cost is the same under both options except one token.** Gate resolutions, the report file and the `## Unattended mode` section are required whichever way the mode is switched (`SPEC4:58`); the brief still carries the report directory (`SPEC4:57`). B's saving is the flag token, not 35 sections.
- **The live spec adopted A as the only switch.** `SPEC-LIVE:401`: "`--unattended` is the only switch ... Commands never detect Orca." This is supporting weight, not proof: the debate should stand on the evidence above.

#### Weaknesses identified in Variant B
1. **B's trigger is session-scoped, so it fires when a person is at the keyboard (L3).** The preamble stays in the context of any Orca terminal that received it. The live spec lists "the person" and "a taken-over terminal" among the writers that can share a worker's worktree (`SPEC-LIVE:79`). A person who takes over a worker terminal and types `/sc:cleanup --interactive` would, under B, lose the approval prompts and outward-default protection with no flag in sight. B's safety claim "a person's own session has no preamble" (`V-B:14`) is true for sessions the person starts, not for sessions the person takes over. The flag is per invocation and has no such leak.
2. **B is not testable and B says so.** `V-B:17`: "there is no token to grep, and a wrong guess by the model is invisible until a run stalls or a prompt disappears." A has AC-1.1 and AC-2.8; B has no check that could be written. B also admits the preamble and the task arrive together, so a test cannot tell them apart (`V-B:14`; the supporting fact is `CAPS:47`, task passed on argv, though that line does not itself say the preamble is in the same string, so this is an inference).
3. **B contradicts itself on the stall (X-002, L3).** `V-B:9` says detection "removes that whole failure class". `V-B:14` and `V-B:17` say detection "relies on the model noticing prose" and that a wrong guess is invisible until a run stalls. A missed detection produces the same silent stall as a forgotten flag, with no coordinator action to blame and nothing in the brief to catch it. B swaps a failure that has a visible cause (a missing token in the brief, now checkable by the guard) for one with none.
4. **B's AC-C1 objection is overstated.** `V-B:25` says AC-C1's grep "would need an exception". The grep in `SPEC4:205-212` matches `orca (orchestration|worktree|terminal|agent)` command phrases (v4 has no `-i`). Detection text such as `ORCA_TERMINAL_HANDLE` or "live preamble" does not match. The real objection to B is SA-2 and non-goal 1 as text (`SPEC4:170`, `SPEC4:314`), which `V-B:18` does cite correctly. The grep claim should be dropped.
5. **B does nothing for non-Orca callers.** `claude -p`, CI and any other orchestrator have no preamble. B concedes this (`V-B:18`). The flag serves them with no change (`SPEC4:54`).
6. **B's repo precedent argues for A.** Reflect's headless rule works because `--print` with no TTY is a mechanical, documented signal (`remediation-handoff.md:239-242`). Orca launches Claude interactively with the task on the command line (`CAPS:47`), so that signal is absent (`SPEC4:391`). The precedent shows detection is acceptable when a mechanical signal exists; here none does, and B substitutes model judgement over prose.
7. **B's "Orca's own rule" (U-005) cuts both ways.** Orca defines a worker by the preamble so that the session knows whether to send lifecycle messages (`CAPS:148`: "Do not emit lifecycle messages" when there is no preamble). That is a question about the worker session's duties, which is exactly where the live spec applies the preamble (the brief guard, `WC`). It is not a statement that commands should change behaviour on it.

#### Concessions
- **A alone leaves the silent stall open (C-003).** `V-A:19` says so, and I concede B's point: the catches are after the fact. The only fix that removes it before the run is a pre-run check. The live spec supplies one in the worker session, not in commands (`WC` "Brief guard" case 1). So the recommended design is A plus that guard, and B was right that A needed something.
- **A's headline overreaches (C-002).** `V-A:9` is titled "Detection would misfire" but its evidence concerns only `ORCA_TERMINAL_HANDLE`. The preamble route is not shown to misfire by that observation. B's separation of the two routes (`V-B:13-14`) is more precise. My argument against the preamble route rests on points 1 to 3 in the weaknesses above, not on that observation.
- **The 2026-11-02 observation is not verifiable from the repo files.** I did not run any Orca command (my brief forbids it) and found the "11 workers" claim only in the variants themselves and in earlier merge logs. The files I can check say: `CAPS:149` (the error text names "a live Orca terminal with ORCA_TERMINAL_HANDLE set") and `CAPS:151` (the variable was set in a dispatched worker). Neither shows the variable absent from a non-worker terminal. The live spec still lists this as open (`SPEC-LIVE:448`).
- **A's migration path (`V-A:23`) conflicts with non-goal 1.** "Detection can be added later as an extra trigger" inside commands would breach `SPEC4:314` and `SPEC4:170`. If anything is added later, it belongs in the worker session (as the guard is), not in commands.
- **The quoted-token rule is applied by a model reading text** (`V-A:22`). Nobody has measured how often it errs. AC-2.8 checks one case.
- **Phase gating has a cost.** The coordinator must test each command copy to decide whether the line carries the flag (`WC` "Brief layout"), and a stale copy yields a refusal. That is added coordinator work B avoids.

#### Citation spot-checks
Method: I read each cited line in `spec-v4-after-round3.md` (the version whose numbering both variants use), in `orca-capabilities.md`, and in `/home/coder/.claude/WORKER-CONTRACT.md`, and compared the text with the claim. I did not run any `orca` command, so `[G]` guide lines and the "11 workers" observation are checked only through what `CAPS:148` and `SPEC4:53` quote.

**Variant A (13 checked)**

| Citation | Claim in A | Result |
|---|---|---|
| `SPEC:329` | "A person never types the flag" | Confirmed (`SPEC4:329`: "a person never types it"). |
| `SPEC:330` | If set in a person's tab, "prompts would vanish ... breaking SA-1" | Confirmed (`SPEC4:330`, the (b) bullet). Not present at `SPEC-LIVE:330` (line shifted). |
| `SPEC:328-331` | Spec's current recommendation is the flag | Confirmed for v4 (`SPEC4:331` "Recommendation: (a)"). Superseded: `SPEC-LIVE:401` approves option (c), flag plus brief guard. |
| `SPEC:395` | UNVERIFIED item 13 left this open | Confirmed (`SPEC4:395`). Live spec: `SPEC-LIVE:448`, now says D1 does not depend on it. |
| `SPEC:169` | SA-1, including auggie-review posting default | Confirmed (`SPEC4:169`). |
| `SPEC:73` | WC-9: flag turns outward defaults off | Confirmed (`SPEC4:73`: under `--unattended` any default that pushes or posts is off; auggie-review "posts by default, no prompt"). |
| `SPEC:269`, `SPEC:55` | AC-2.8 live check of the quoted-token rule | Confirmed (`SPEC4:269`, `SPEC4:55`). |
| `SPEC:257` | AC-1.1 asserts per-phase section presence | Confirmed (`SPEC4:257`). |
| `SPEC:187-195` | Phase-gated acceptance of the flag | Confirmed (`SPEC4:187-195` table). |
| `SPEC:47`, `CAPS:52` | Stalled waiting worker reported healthy | Confirmed (`SPEC4:47`; `CAPS:52`: "A waiting worker is healthy, not failed"). |
| `SPEC:58`, `SPEC:79` | One shared rule file, section per command; brief carries the command line | Confirmed (`SPEC4:58`, `SPEC4:79`). |
| `SPEC:238` | Step-3 stall proof | Confirmed (`SPEC4:238`). |
| "env shows `ORCA_TERMINAL_HANDLE` set, handle absent from 11 `worker-list` rows" | Observation on 2026-11-02 | UNVERIFIED by me. Not in `SPEC4`, `CAPS` or `WC`. `CAPS:151` shows the variable set in a dispatched worker, which is a different fact. |

**Variant B (11 checked)**

| Citation | Claim in B | Result |
|---|---|---|
| `SPEC:330` | Detection by env var or preamble | Confirmed (`SPEC4:330`). |
| `SPEC:395` | Item 13 | Confirmed (`SPEC4:395`). |
| `SPEC:189-195` | "No new flag on 35 commands" | Confirmed in substance (`SPEC4:189-195`: running total 35, or 36 with pr-submit). The table says the commands each *accept* the flag; B's "no new flag" is the claim, not the table. |
| `CAPS:52`, `CAPS:129` | Waiting worker "healthy, not failed" | Confirmed (both lines contain the phrase). |
| `CAPS:148` | "No live preamble" is an "Ordinary terminal agent" | Confirmed (quotes `[G]` line 41; paraphrases line 38). |
| `[G]` 38 verbatim: "current prompt contains a live injected preamble with Task and Dispatch IDs" | Quoted as Orca's wording | Substance supported (`CAPS:148`, `SPEC4:53`). The verbatim quote appears only in the variants and earlier merge output, not in `CAPS` or the spec. UNVERIFIED verbatim. |
| `SPEC:314`, `SPEC:170` | Non-goal 1 and SA-2 forbid Orca-specific commands | Confirmed (`SPEC4:314`, `SPEC4:170`). |
| `SPEC:205-212` | AC-C1's grep "would need an exception" | Line exists (`SPEC4:205-212`) but the claim is overstated. The pattern matches `orca <verb>` command phrases; `ORCA_TERMINAL_HANDLE` and "preamble" do not match. Counts against B. |
| `SPEC:391` | Reflect headless signal would not fire for a worker | Line exists, but it says "assumed not" (UNVERIFIED item 9). B states it as fact. Overstated. |
| `CAPS:47` | Preamble arrives on the same command line as the task | `CAPS:47` shows task passed by argv (`promptInjectionMode: 'argv'`). That the preamble shares that string is an inference, not stated. |
| `remediation-handoff.md:239-242` | Repo precedent: `claude --print`, no TTY | Confirmed (read at the file). |

Net: no fabricated citation on either side. A has one unverifiable session observation; B has one unverifiable verbatim quote, one overstated grep claim, one overstated "would not fire", and one inference presented as a fact.

#### Shared assumption responses
**A-001: QUALIFY** (the single 2026-11-02 observation proves the variable is set in non-worker terminals in general).
It does not prove that, and I do not need it to. What the repo files show is `CAPS:149` (the sender-identity error says to run "inside a live Orca terminal with ORCA_TERMINAL_HANDLE set", which implies the variable marks any live Orca terminal) and `CAPS:151` (the variable is set in a dispatched worker). The live spec still lists the question as open (`SPEC-LIVE:448`: "this item stays open"). The observation is one session on one profile and version, and a local worker list omits remote workers unless `--include-remote` is passed (`CAPS:127-128`), so "handle not among 11 rows" has at least one other explanation I cannot rule out from the files. This matters for the A-versus-B comparison only for the environment route, which both sides already reject. A's case does not depend on it: points 1 to 3 in my weaknesses section stand if the variable is set only in workers. The sentence in `V-A:9` should be downgraded to "likely, not proven".

**A-002: QUALIFY** (a model reliably applies the trigger guard; neither side measures it).
Accept that neither failure rate is measured, and that A's quoted-token rule is applied by a model reading text (`V-A:22`). Reject that the two tasks are equally hard. Recognising a standalone token outside quotes is a lexical test on the line the model was just given. Recognising a live preamble is a judgement about the provenance of prose in a long context, and the preamble and task arrive together (`V-B:14`). A also has checks that exercise the rule (AC-2.8 `SPEC4:269`, AC-1.7 and AC-2.9 for the guard in the live spec `SPEC-LIVE:323`, `SPEC-LIVE:331`); B has none. The recommended remedy is to measure A's rate during P1 live checks, not to assume it. L3 note: the failure modes differ in cost. A's error on a person's line (treating quoted text as the flag) is caught by AC-2.8; B's error on a person's session (treating a taken-over terminal as unattended) has no check and no visible signal.

**A-003: ACCEPT** (the options are not mutually exclusive; neither considered a hybrid).
Accept: the diff analysis is right that neither variant discusses a hybrid, and the hybrid exists in the live contract (`WC` "Brief guard" case 1; `SPEC-LIVE:60`, `SPEC-LIVE:401`). The hybrid is "require the flag; when a live preamble is present and the flag is absent, refuse instead of prompting". It uses B's preamble recognition only in the worker session, where Orca already requires it (`CAPS:148`), and only to refuse, never to switch a command's behaviour. That answers B's best argument (the forgotten-flag stall) without making commands Orca-aware (non-goal 1) and without the taken-over-terminal hazard, because a refusal at the start of a brief cannot change a person's later commands. It is A with a backstop. A residual risk remains: the guard still depends on the model recognising the preamble and on reading every command copy (`WC` "Brief guard"), so it narrows the stall rather than eliminating it.

#### Point table
L3 (state-mechanics) points argued explicitly above: C-003 (forgotten trigger), X-002 (stall in B), A-001, A-002, and the session-scoped versus invocation-scoped trigger under X-001 and C-007.

| Point | Preferred variant (A, B, or UNRESOLVED) | Confidence 50-100% | One-sentence evidence |
|---|---|---|---|
| S-001 | UNRESOLVED | 50% | Section layout is presentation only; B's extra "Strongest case" heading helps a reader and changes no claim. |
| S-002 | UNRESOLVED | 50% | B's third key `[G]` names its source more exactly, but the lines it quotes are only reachable through `CAPS:148` and `SPEC4:53`, and its verbatim quote could not be confirmed. |
| C-001 | A | 80% | Invocation-scoped, greppable trigger that keeps commands Orca-free (`SPEC4:314`, `SPEC4:170`, `SPEC4:257`) beats session-scoped detection; the live spec also adopts the flag as the only switch (`SPEC-LIVE:401`). |
| C-002 | B | 65% | A's evidence is about the environment variable only; B correctly separates the preamble route (`V-A:9` versus `V-B:13-14`), though neither observation is verifiable from the repo files. |
| C-003 | B | 60% | The silent stall from a forgotten flag is real and A's catches are after the fact (`SPEC4:47`, `CAPS:52`), but the live guard (`WC` case 1) fixes it without B's mechanism. |
| C-004 | A | 85% | AC-1.1 (`SPEC4:257`) and AC-2.8 (`SPEC4:269`) test A; B admits "no token to grep" (`V-B:17`). |
| C-005 | A | 85% | Non-goal 1 and SA-2 (`SPEC4:314`, `SPEC4:170`) forbid Orca-aware commands, and B concedes it does nothing for `claude -p` or CI (`V-B:18`); B's AC-C1 grep claim is overstated. |
| C-006 | A | 60% | Gate resolutions, report files and sections are needed under both options (`SPEC4:58`, `SPEC4:57`), so B saves one token per command line, while A's "add detection later" path conflicts with non-goal 1. |
| C-007 | A | 65% | Only a coordinator-written flag can turn outward defaults off (`SPEC4:73`), so a person's auggie-review posting default (`SPEC4:169`) is safe; B's preamble route can misfire in a taken-over terminal (`SPEC-LIVE:79`). |
| X-001 | A | 65% | Preamble detection is safer than the env route and B is right on that, but the preamble persists in a taken-over terminal, so "a person's own session has no preamble" (`V-B:14`) holds only for sessions the person starts. |
| X-002 | A | 75% | B says detection "removes that whole failure class" (`V-B:9`) and also that a wrong guess "is invisible until a run stalls" (`V-B:17`); a missed detection is the same silent stall with no visible cause. |
| A-001 | UNRESOLVED | 60% | One observation cannot be checked from the repo files; `CAPS:149` supports the generalisation and `CAPS:151` plus `SPEC-LIVE:448` keep it open, and A's case does not depend on it. |
| A-002 | A | 60% | A's rule is a lexical test with live checks (AC-2.8, AC-1.7, AC-2.9), B's is a provenance judgement with none; neither failure rate is measured. |
| A-003 | A | 65% | The hybrid already in the live contract (`WC` "Brief guard" case 1, `SPEC-LIVE:60`, `SPEC-LIVE:401`) keeps A's flag as the only switch and adds B's preamble recognition only as a refuse-only backstop. |

### Round 1 advocate statement: Variant B (command detects it runs as an Orca worker)

Advocate: Variant B. Opponent: Variant A (explicit `--unattended` flag). Depth: quick, round 1 of 1.

#### Position
The defensible core of B is narrower than B's text. It is this: the live Orca preamble (Task ID plus Dispatch ID), not the environment variable, is the signal that a session is a worker, and a coordinator that forgets a flag must not be able to leave a worker stalled on a prompt that Orca reports as healthy.

B as written (every command detects the preamble itself) loses to A on testability, Orca coupling and migration cost. I say so below. B's real contribution is the stall hazard and the preamble as a signal.

Context the lead should have. The current spec (`orca-worker-contract-spec.md:401`, section 9) already records D1 as approved on 2026-11-02 as "Option (c): `--unattended` is the only switch; from P1 the worker session also applies the brief guard. Commands never detect Orca." `~/.claude/WORKER-CONTRACT.md` lines 16-20 spell out that guard. It is a hybrid: the flag stays the switch, and a worker session that holds a live preamble refuses to run a convertible command whose line lacks the flag. So B's preamble insight was adopted, but moved out of the commands and into the worker session. That outcome supports B on points C-003, X-001 and U-005, and supports A on C-001, C-004, C-005 and C-006.

#### Steelman of Variant A
A's strongest argument has four parts, and each is correct.
1. A flag is a lexical, greppable token. A person never types it, and the parse rule (standalone token outside quotes) is live-checked by AC-2.8 (v4 `SPEC:269`). Preamble recognition is prose the model must notice, and nothing can grep for it.
2. A names the condition (no person at the keyboard), not a tool. `claude -p`, CI and a future orchestrator can use it with no Orca. Detection ties every command to Orca, which spec non-goal 1 and SA-2 forbid (`SPEC:314`, `SPEC:170`).
3. A is migration-safe. Detection can be added later as an extra trigger; removing detection from 35 commands later is not cheap.
4. A is honest about its one weakness (a forgotten flag stalls the worker) and names the after-the-fact catches (brief template, step-3 stall proof).

A also gets the safety asymmetry right: its failure direction (flag missing, so the command prompts) leaves a person's behaviour intact, whereas B's false-positive direction takes prompts away from a person.

#### Key strengths claimed
- **Orca defines a worker by the preamble.** `orca-capabilities.md:148` quotes the guide: "No live preamble and no explicit supervision | Ordinary terminal agent"; only a session that received a preamble with Task and Dispatch IDs is a worker (`[G]` line 38). Preamble detection reuses Orca's own rule and a person's own session has none.
- **The stall is silent and Orca calls it healthy.** `CAPS:52` and `CAPS:129`: "A waiting worker is healthy, not failed." The spec itself calls the silent stall "the real failure mode for a command prompt" (v4 `SPEC:47`). A design where the coordinator's omission cannot produce that state is worth something, and the approved spec agreed by adding the brief guard (`WORKER-CONTRACT.md:17`, case 1).
- **The environment-variable observation does not condemn the preamble route.** The 2026-11-02 observation is about `ORCA_TERMINAL_HANDLE` only. `CAPS:149` shows Orca's own error text treats the variable as the identity of "a live Orca terminal", so it marks any Orca tab. Nothing observed says a person's tab carries a Task/Dispatch preamble. A's "detection would misfire" (A:9) is therefore proved for the environment route and merely asserted for the preamble route.

#### Weaknesses identified in Variant A
1. **A treats the stall as a footnote.** A:19 files it under "known weakness" and says the catches work "only after the fact". For an unattended worker, after the fact means a worker parked indefinitely with no `worker_done` and a healthy status (`CAPS:52`). A's own mitigation (the 7.2 step-3 stall proof, v4 `SPEC:238`) is a test-time check, not a runtime prevention. The approved spec found A alone insufficient and added a worker-side guard. A:3 ("Nothing in the environment, the conversation or Orca turns it on") is superseded by that outcome.
2. **A over-generalizes its observation (C-002, X-001).** A:9 uses an environment-variable observation to say detection in general "would misfire". Preamble detection is untouched by that evidence.
3. **A's "flag or detection" framing is a false choice.** The hybrid shows the flag can stay the switch and still let the worker session react to the preamble (A-003).
4. **A's quoted-argument rule is only as strong as the model applying it.** Commands are prompts, so A:22 itself admits the "parse" is applied by the model reading the rule. That is the same model-reliability assumption (A-002) A uses against B, and A has not measured it either.

#### Concessions
1. **Testability (C-004): A wins.** B:17 is right about its own weakness. There is no token to grep, and AC-1.1 (v4 `SPEC:257`) cannot assert detection text the way it asserts a section.
2. **Orca coupling (C-005): A wins.** B:18 concedes it. Non-goal 1 (v4 `SPEC:314`, current `SPEC:385`) and SA-2 forbid "Orca-specific branching" in commands, and commands run in other projects. Detection inside commands conflicts with both. The approved spec confirms: "Commands never detect Orca."
3. **Trigger mechanism (C-001): A wins.** The approved D1 is the flag.
4. **X-002 (B contradicts itself): the criticism is fair.** B:9 says detection "removes that whole failure class" while B:14 and B:17 say a wrong guess is invisible until a run stalls. Correct statement: detection removes the coordinator-omission failure and replaces it with a model-miss failure. Which is rarer is unmeasured (A-002). B:9 overstates.
5. **Environment route is unsafe.** Both variants agree, and `CAPS:149` explains why. B should not claim it.
6. **Cost and reversibility (C-006): A wins.** B:25 says so.
7. **B:19 states as fact that the `--print` headless signal "would not fire".** The spec lists this as an assumption (v4 `SPEC:391`, item 9, "assumed not"). It is UNVERIFIED, so B:19 is an inference.
8. **B:14 says the preamble "arrives on the same command line as the task (CAPS:47)".** `CAPS:47` only says that for Claude the task is passed on the command line (`promptInjectionMode: 'argv'`). It does not say the preamble is in that argv. Plausible, not shown.
9. **B:10 ("no new flag on 35 commands", citing `SPEC:189-195`) is weak.** The cited table lists which commands accept the flag. It does not support shorter briefs, and B:25 admits each command still needs per-command detection text, so the saving is not real.

#### Citation spot-checks
**Version finding (applies to both variants equally).** Every `SPEC:N` line number in both variants matches `.dev/orca-command-refactor/specs/history/spec-v4-after-round3.md`, not the current `orca-worker-contract-spec.md`. In the current file `SPEC:330` is an AC-2.6 table row and `SPEC:395` is a blank line. Neither variant names the version. Not a fabrication, but a reader who opens the current spec will not find the cited text. `CAPS:N` lines and `WORKER-CONTRACT.md` are current.

**Variant B citations (checked against v4 for SPEC, current for CAPS)**
| Cite | Claim | Result |
|---|---|---|
| `SPEC:330` | Detect option; variable set in Orca terminals; prompts would vanish for a person, breaking SA-1 | Verified (v4:330) |
| `SPEC:395` | UNVERIFIED item 13 on `ORCA_TERMINAL_HANDLE` in a person's tab | Verified (v4:395) |
| `CAPS:52` | Waiting worker is "healthy, not failed" | Verified |
| `CAPS:148` | "No live preamble ... Ordinary terminal agent"; only Task/Dispatch preamble makes a worker (`[G]` 38, 41) | Verified |
| `SPEC:314` | Non-goal 1: no Orca-specific branching in commands | Verified (v4:314; current is `SPEC:385`) |
| `SPEC:205-212` | AC-C1 grep | Verified (v4:205-212; current is 244-254) |
| `SPEC:391` | Item 9, headless signal is `claude --print`, Orca launches interactively | Verified, but the spec says "assumed not"; B:19 states it as fact (overstated) |
| `remediation-handoff.md:239-242` | `--print` mode with no TTY is the headless signal | Verified (current file lines 235-242) |
| `SPEC:189-195` | "no new flag on 35 commands" | Table exists (v4:189-195) but it lists which commands accept the flag; it does not support the shorter-brief claim. Weak fit |
| `CAPS:47` | Preamble on the same command line as the task | Partly: `CAPS:47` says the task goes on the command line for Claude; it does not mention the preamble |

**Variant A citations**
| Cite | Claim | Result |
|---|---|---|
| `SPEC:329`, `SPEC:328-331` | Flag recommended; person never types it | Verified (v4:329, 331) |
| `SPEC:55`, `SPEC:269` | Quoted-argument parse rule; AC-2.8 live check | Verified |
| `SPEC:73` | WC-9 outward defaults off under `--unattended` | Verified (v4:73) |
| `SPEC:257` | AC-1.1 asserts per-phase `## Unattended mode` sections | Verified |
| `SPEC:187-195` | Phase-gated acceptance of the flag | Verified (v4:187 heading, 189-195 table) |
| `SPEC:361` | Decisions row: name of the switch, caller-neutral | Verified |
| `SPEC:395`, `SPEC:330` | Item 13 and SA-1 quote | Verified |
| `SPEC:47`, `CAPS:52` | Silent stall reported healthy | Verified |
| `SPEC:238` | Step-3 stall proof | Verified (v4:238, positive proof of stall) |

Net: no fabricated citation on either side. Both carry the stale-version issue. A's citations are cleaner; B has two overstated fits (`SPEC:189-195`, `CAPS:47`) and one inference stated as fact (`SPEC:391`). I could not re-run the `worker-list` observation behind A:9 and B:13 (this task forbids Orca commands); both variants report it identically, and `CAPS:149` independently supports the conclusion that the variable marks any live Orca terminal.

#### Shared assumption responses
**A-001: QUALIFY.** The conclusion (environment variable is unsafe) is right, but not because of one observation. `CAPS:149` quotes Orca's own error text, "run the command inside a live Orca terminal with ORCA_TERMINAL_HANDLE set", which treats the variable as the identity of any live terminal. That is independent support. What stays open is the claim for other Orca profiles or versions: the current spec still lists it as UNVERIFIED item 13 (`SPEC:448`). Accept for the environment route; do not extend it to the preamble route.

**A-002: QUALIFY.** Neither side measured how reliably a model applies its trigger rule. A's rule is lexical (a standalone token outside quotes); B's is semantic (recognize a live preamble). A's is probably easier, and A's failure direction (missing flag, so the command prompts) is the safer one for people. B's false-positive direction breaks SA-1. But A's error silently produces the stall A admits it cannot prevent, so the failure rates must be measured, not assumed. The live checks AC-1.2, AC-1.7 and AC-2.9 are the right way to measure them.

**A-003: REJECT.** The two options are not mutually exclusive, and the approved spec shows it. `WORKER-CONTRACT.md` lines 16-20 ("Brief guard") keep `--unattended` as the only switch in commands and add a worker-session rule: with a live preamble and no flag on a convertible command, refuse and send `worker_done --outcome failed` with a body starting `guard refused:`. That keeps A's testability and caller-neutrality, and it keeps B's insight that the preamble is the right worker signal and that a forgotten flag must not stall. Honest scoring: this hybrid is closer to A, because the commands stay Orca-free; B-as-written (commands detect) is superseded.

#### Point table
| Point | Preferred variant (A, B, or UNRESOLVED) | Confidence | One-sentence evidence |
|---|---|---|---|
| S-001 | UNRESOLVED | 50% | Presentation only: B's leading "Strongest case" section helps a reader, A's Position paragraph does the same job. |
| S-002 | B | 60% | B's extra `[G]` key points at Orca's own role table, which `CAPS:148` confirms. |
| C-001 | A | 80% | Approved D1 is the flag: "Commands never detect Orca" (`SPEC:401`); `WORKER-CONTRACT.md:12`. |
| C-002 | B | 70% | The observation is about `ORCA_TERMINAL_HANDLE` only; A:9 extends it to all detection without evidence for the preamble route. |
| C-003 | B | 60% | The silent stall is real and invisible (`CAPS:52`, v4 `SPEC:47`); the approved spec added a guard for it, so A's "known weakness" framing was too light, though B overstates that detection removes it. |
| C-004 | A | 85% | A flag is greppable and AC-1.1 asserts it (v4 `SPEC:257`); B:17 concedes there is no token to grep. |
| C-005 | A | 85% | Non-goal 1 and SA-2 forbid Orca branching in commands (v4 `SPEC:314`, `SPEC:170`); B:18 concedes. |
| C-006 | A | 70% | B:25 admits per-command detection text and an AC-C1 exception; A can add detection later without removing the flag. |
| C-007 | A | 65% | The flag is immune to losing outward defaults by construction; B's exposure only arises on the environment route, which B abandons. |
| X-001 | B | 60% | A's claim that nothing in the conversation can safely trigger the mode is unsupported for the preamble; the approved spec itself uses the preamble in the guard. |
| X-002 | A | 75% | B:9 ("removes that whole failure class") contradicts B:14 and B:17; detection trades one failure for another. |
| A-001 | UNRESOLVED | 60% | `CAPS:149` supports generalizing for the environment route, but item 13 stays open (`SPEC:448`) and I could not re-run `worker-list`. |
| A-002 | A | 55% | A's lexical token is easier for a model than B's semantic recognition, but neither rate is measured. |
| A-003 | UNRESOLVED | 70% | The approved hybrid (flag as switch plus worker-session preamble guard, `WORKER-CONTRACT.md:16-20`) is neither pure variant; it leans A in command text and adopts B's signal in the worker session. |

## Round 2: Rebuttals
Round 2 skipped: depth=quick.

Round 2.5 (invariant probe) skipped: `--depth quick`.

## Round 3: Final Arguments
Round 3 skipped: depth=quick (Round 3 runs only with `--depth deep`).

## Scoring Matrix
Rule used: each advocate's table row is one position. Both name the same variant: agreed (confidence = mean of the two advocate confidences, +10 when the losing advocate explicitly conceded the point, never 100%). Different variants, or either side UNRESOLVED: unresolved at 50%.

| Diff Point | Level | Advocate A | Advocate B | Winner | Confidence | Evidence Summary |
|------------|-------|-----------|-----------|--------|------------|-----------------|
| S-001 | L1 | UNRESOLVED 50 | UNRESOLVED 50 | unresolved | 50% | Presentation only; neither advocate claims a winner. |
| S-002 | L1 | UNRESOLVED 50 | B 60 | unresolved | 50% | Split; B's `[G]` key points at Orca's role table but its verbatim quote could not be confirmed. |
| C-001 | L2 | A 80 | A 80 | Variant A | 90% | B's advocate concedes: the approved decision is the flag, "Commands never detect Orca" (live spec line 401, verified). |
| C-002 | L3 | B 65 | B 70 | Variant B | 78% | A's advocate concedes A:9 overreaches: the observation covers the environment variable only. |
| C-003 | L3 | B 60 | B 60 | Variant B | 70% | The silent stall is real (CAPS:52); A's advocate concedes the catches are after the fact. The fix lies in the worker session, not in commands. |
| C-004 | L2 | A 85 | A 85 | Variant A | 95% | B's advocate concedes B:17: no token to grep; AC-1.1 and AC-2.8 test A. |
| C-005 | L2 | A 85 | A 85 | Variant A | 95% | B's advocate concedes B:18: breaks non-goal 1 and SA-2 and does nothing for `claude -p` or CI. |
| C-006 | L2 | A 60 | A 70 | Variant A | 75% | B's advocate concedes B:25; B's AC-C1 grep claim is overstated per both advocates. |
| C-007 | L3 | A 65 | A 65 | Variant A | 65% | Only a coordinator-written flag turns outward defaults off; no explicit concession by B's advocate. |
| X-001 | L2 | A 65 | B 60 | unresolved | 50% | Split on whether preamble-based detection is safe; A's advocate adds that the preamble persists in a taken-over terminal. |
| X-002 | L3 | A 75 | A 75 | Variant A | 85% | B's advocate concedes B:9 ("removes that whole failure class") contradicts B:14 and B:17. |
| A-001 | L3 | UNRESOLVED 60 | UNRESOLVED 60 | unresolved | 50% | Both QUALIFY: one observation, not verifiable from repository files; spec item 13 stays open. |
| A-002 | L3 | A 60 | A 55 | Variant A | 58% | A's rule is a lexical test with live checks, B's a provenance judgement; neither failure rate is measured. |
| A-003 | L2 | A 65 | UNRESOLVED 70 | unresolved | 50% | Mechanical split. Substantively both reject "mutually exclusive" and point to the hybrid already adopted (live spec line 401; `WORKER-CONTRACT.md` Brief guard), which they place nearer A. |

## Convergence Assessment
- Points resolved: 9 of 14 (C-001..C-007, X-002, A-002)
- Alignment: 64.3%
- Threshold: 80%
- Status: NOT_CONVERGED (maximum rounds for depth=quick reached: 1)
- Unresolved points: S-001, S-002, X-001, A-001, A-003
- Taxonomy coverage gate: passed (L1, L2 and L3 each have addressed points)
- Invariant probe gate: not applied (Round 2.5 skipped at depth=quick)
- Handling: force-select by combined score (FR-006); non-convergence recorded; return status `partial`

Findings raised by the advocates beyond the 14 diff points (checked by the orchestrator where marked):
1. Both variants cite `SPEC:N` line numbers from `.dev/orca-command-refactor/specs/history/spec-v4-after-round3.md`, not the current spec. The current spec records the decision at line 401 as "Option (c): `--unattended` is the only switch; from P1 the worker session also applies the brief guard. Commands never detect Orca." (checked by the orchestrator).
2. Overstated claims in Variant B per both advocates: B:19 states "would not fire" as fact though the spec says "assumed not" (item 9); B:14 reads CAPS:47 as covering the preamble though it covers only the task on the command line; B:25's AC-C1 grep exception and B:10's "shorter briefs" are not supported by the cited lines.
3. Advocate A's new argument, that a preamble stays in the context of a terminal a person takes over, so session-scoped detection could switch off a person's prompts, was not rebutted: depth=quick has no rebuttal round.
4. The 2026-11-02 observation (11 workers listed, handle absent) is reported identically by both variants and could not be checked from repository files; CAPS:127-128 show `worker-list` omits remote workers unless `--include-remote` is passed, an alternative explanation.
