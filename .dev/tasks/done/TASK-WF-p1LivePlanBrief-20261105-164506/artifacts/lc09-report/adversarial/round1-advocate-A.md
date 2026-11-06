# Round 1 advocate statement: Variant A (explicit `--unattended` flag)

## Position
Citation key: `V-A:N` / `V-B:N` = line N of `variant-1-original.md` / `variant-2-original.md`. `SPEC4:N` = line N of `.dev/orca-command-refactor/specs/history/spec-v4-after-round3.md`. `SPEC-LIVE:N` = line N of the current `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. `CAPS:N` = `.dev/orca-command-refactor/inventory/orca-capabilities.md:N`. `WC` = `/home/coder/.claude/WORKER-CONTRACT.md`.

**Baseline fact the lead must know first.** Both variants cite `SPEC:N` line numbers that match `spec-v4-after-round3.md` (the spec before the D1 decision), not the live spec. Example: `SPEC4:330` is the "Detect Orca ... prompts would vanish" text, but `SPEC-LIVE:330` is an AC-2.6 table row. In the live spec, D1 is already settled at `SPEC-LIVE:401`: "Option (c): `--unattended` is the only switch; from P1 the worker session also applies the brief guard. Commands never detect Orca." UNVERIFIED item 13 moved to `SPEC-LIVE:448` and now says "D1 no longer depends on it: no option the spec keeps reads the variable." This affects both variants equally, and the content of every cited line I checked is intact in v4. I checked against v4.

**My position.** The trigger for unattended mode should be a standalone `--unattended` token on the command line, not detection of Orca by the command. Five reasons, strongest first:

1. **The flag is scoped to one invocation; the preamble is scoped to a whole session.** A person who takes over a worker terminal (the live spec names "a taken-over terminal" among possible writers, `SPEC-LIVE:79`) still has the preamble in context. Under B every command the person then types would silently drop its prompts. Under A the person's typed command has no flag, so it prompts as today (SA-1, `SPEC4:169`).
2. **It can be tested.** `SPEC4:257` (AC-1.1) asserts per phase which commands carry an `## Unattended mode` section; `SPEC4:269` (AC-2.8) live-checks the quoted-token rule. B has no equivalent and says so (`V-B:17`).
3. **It keeps commands Orca-free.** Non-goal 1 forbids "Orca-specific branching" (`SPEC4:314`) and SA-2 keeps commands runnable in other projects (`SPEC4:170`). B's own text admits it ties commands to Orca (`V-B:18`).
4. **It serves any caller with no person** (`claude -p`, CI), because the flag "names the condition (no person), not a tool" (`SPEC4:361`, `SPEC4:54`).
5. **Its one real weakness (a forgotten flag causes a silent stall) is better fixed by a refuse-only guard in the worker session than by moving the trigger into every command.** That is what the live spec adopted (`WC` "Brief guard", case 1: every copy of the command has an `## Unattended mode` section and the line lacks the flag, so the worker refuses with `guard refused: brief lacks --unattended`). I treat that as Variant A plus a backstop, and I argue it below as the answer to B's best point.

## Steelman of Variant B
The strongest version of B, stated so B's advocate would sign it:

> The failure that actually hurts in production is the silent stall. A command that prompts inside a worker is reported by Orca as "healthy, not failed" (`CAPS:52`, `CAPS:129`; `SPEC4:47`: "the real failure mode ... is a silent stall with no `worker_done`"). Under A that failure is one forgotten token away, and the coordinator is a model writing prose briefs; A's own text admits the catch comes only "after the fact" (`V-A:19`). Orca already defines a worker precisely: a session whose current prompt carries a live preamble with Task and Dispatch IDs; no preamble means "Ordinary terminal agent" (`CAPS:148`, `SPEC4:53`). So drop the environment variable (unsafe, as both sides agree) and detect the preamble only. A person's own session has no preamble, so people are safe, and the coordinator cannot forget anything. The repo already has a precedent of commands reading their run context (reflect's `claude --print` headless rule, `remediation-handoff.md:239-242`, which I re-read and confirm). Briefs get shorter and 35 commands need no new flag token.

What B genuinely gets right:
- The forgotten-flag stall is real, silent, and not caught by Orca. A's mitigations (brief template, step-3 stall proof, `SPEC4:238`) are after the fact.
- A's "detection would misfire" headline (`V-A:9`) is supported only by an observation about the environment variable. It says nothing about the preamble route. B is right to separate the two (`V-B:13-14`).
- B correctly identifies Orca's own role table as the authoritative definition of a worker (`CAPS:148`).
- B correctly notes that the reflect headless signal would not fire for an Orca worker (`SPEC4:391` says "assumed not"; UNVERIFIED), so no existing command-side signal exists.

## Key strengths claimed
- **Invocation-scoped trigger (L3, state mechanics).** The flag lives in the one command line the coordinator wrote. It cannot leak into a later command typed in the same session. The flag parse rule (`SPEC4:55`) makes even quoted text inert: `/sc:troubleshoot "the worker ignores --unattended"` stays a person's run, and AC-2.8 (`SPEC4:269`) checks it live.
- **Deterministic and greppable.** AC-1.1 (`SPEC4:257`) asserts per phase which commands carry the section and that no other command has one yet. The live 7.2 checks (`SPEC4:234-238`) then show the flag's effect, including the step-3 stall proof.
- **Phase gating.** `SPEC4:187-195` lists which commands accept the flag after each phase, so the flag never promises behaviour a command lacks. Detection cannot be phase-gated this way: it would activate in a command the moment the worker runs it, converted or not.
- **Outward defaults stay a person's.** Under `--unattended`, outward defaults are off (WC-9, `SPEC4:73`). Only a flag the coordinator writes can turn that off, so a person working in Orca keeps, for example, auggie-review's posting default (`SPEC4:169`).
- **Commands stay Orca-free** (non-goal 1 `SPEC4:314`, SA-2 `SPEC4:170`) and the mode is caller-neutral (`SPEC4:54`, `SPEC4:361`).
- **Per-command cost is the same under both options except one token.** Gate resolutions, the report file and the `## Unattended mode` section are required whichever way the mode is switched (`SPEC4:58`); the brief still carries the report directory (`SPEC4:57`). B's saving is the flag token, not 35 sections.
- **The live spec adopted A as the only switch.** `SPEC-LIVE:401`: "`--unattended` is the only switch ... Commands never detect Orca." This is supporting weight, not proof: the debate should stand on the evidence above.

## Weaknesses identified in Variant B
1. **B's trigger is session-scoped, so it fires when a person is at the keyboard (L3).** The preamble stays in the context of any Orca terminal that received it. The live spec lists "the person" and "a taken-over terminal" among the writers that can share a worker's worktree (`SPEC-LIVE:79`). A person who takes over a worker terminal and types `/sc:cleanup --interactive` would, under B, lose the approval prompts and outward-default protection with no flag in sight. B's safety claim "a person's own session has no preamble" (`V-B:14`) is true for sessions the person starts, not for sessions the person takes over. The flag is per invocation and has no such leak.
2. **B is not testable and B says so.** `V-B:17`: "there is no token to grep, and a wrong guess by the model is invisible until a run stalls or a prompt disappears." A has AC-1.1 and AC-2.8; B has no check that could be written. B also admits the preamble and the task arrive together, so a test cannot tell them apart (`V-B:14`; the supporting fact is `CAPS:47`, task passed on argv, though that line does not itself say the preamble is in the same string, so this is an inference).
3. **B contradicts itself on the stall (X-002, L3).** `V-B:9` says detection "removes that whole failure class". `V-B:14` and `V-B:17` say detection "relies on the model noticing prose" and that a wrong guess is invisible until a run stalls. A missed detection produces the same silent stall as a forgotten flag, with no coordinator action to blame and nothing in the brief to catch it. B swaps a failure that has a visible cause (a missing token in the brief, now checkable by the guard) for one with none.
4. **B's AC-C1 objection is overstated.** `V-B:25` says AC-C1's grep "would need an exception". The grep in `SPEC4:205-212` matches `orca (orchestration|worktree|terminal|agent)` command phrases (v4 has no `-i`). Detection text such as `ORCA_TERMINAL_HANDLE` or "live preamble" does not match. The real objection to B is SA-2 and non-goal 1 as text (`SPEC4:170`, `SPEC4:314`), which `V-B:18` does cite correctly. The grep claim should be dropped.
5. **B does nothing for non-Orca callers.** `claude -p`, CI and any other orchestrator have no preamble. B concedes this (`V-B:18`). The flag serves them with no change (`SPEC4:54`).
6. **B's repo precedent argues for A.** Reflect's headless rule works because `--print` with no TTY is a mechanical, documented signal (`remediation-handoff.md:239-242`). Orca launches Claude interactively with the task on the command line (`CAPS:47`), so that signal is absent (`SPEC4:391`). The precedent shows detection is acceptable when a mechanical signal exists; here none does, and B substitutes model judgement over prose.
7. **B's "Orca's own rule" (U-005) cuts both ways.** Orca defines a worker by the preamble so that the session knows whether to send lifecycle messages (`CAPS:148`: "Do not emit lifecycle messages" when there is no preamble). That is a question about the worker session's duties, which is exactly where the live spec applies the preamble (the brief guard, `WC`). It is not a statement that commands should change behaviour on it.

## Concessions
- **A alone leaves the silent stall open (C-003).** `V-A:19` says so, and I concede B's point: the catches are after the fact. The only fix that removes it before the run is a pre-run check. The live spec supplies one in the worker session, not in commands (`WC` "Brief guard" case 1). So the recommended design is A plus that guard, and B was right that A needed something.
- **A's headline overreaches (C-002).** `V-A:9` is titled "Detection would misfire" but its evidence concerns only `ORCA_TERMINAL_HANDLE`. The preamble route is not shown to misfire by that observation. B's separation of the two routes (`V-B:13-14`) is more precise. My argument against the preamble route rests on points 1 to 3 in the weaknesses above, not on that observation.
- **The 2026-11-02 observation is not verifiable from the repo files.** I did not run any Orca command (my brief forbids it) and found the "11 workers" claim only in the variants themselves and in earlier merge logs. The files I can check say: `CAPS:149` (the error text names "a live Orca terminal with ORCA_TERMINAL_HANDLE set") and `CAPS:151` (the variable was set in a dispatched worker). Neither shows the variable absent from a non-worker terminal. The live spec still lists this as open (`SPEC-LIVE:448`).
- **A's migration path (`V-A:23`) conflicts with non-goal 1.** "Detection can be added later as an extra trigger" inside commands would breach `SPEC4:314` and `SPEC4:170`. If anything is added later, it belongs in the worker session (as the guard is), not in commands.
- **The quoted-token rule is applied by a model reading text** (`V-A:22`). Nobody has measured how often it errs. AC-2.8 checks one case.
- **Phase gating has a cost.** The coordinator must test each command copy to decide whether the line carries the flag (`WC` "Brief layout"), and a stale copy yields a refusal. That is added coordinator work B avoids.

## Citation spot-checks
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

## Shared assumption responses
**A-001: QUALIFY** (the single 2026-11-02 observation proves the variable is set in non-worker terminals in general).
It does not prove that, and I do not need it to. What the repo files show is `CAPS:149` (the sender-identity error says to run "inside a live Orca terminal with ORCA_TERMINAL_HANDLE set", which implies the variable marks any live Orca terminal) and `CAPS:151` (the variable is set in a dispatched worker). The live spec still lists the question as open (`SPEC-LIVE:448`: "this item stays open"). The observation is one session on one profile and version, and a local worker list omits remote workers unless `--include-remote` is passed (`CAPS:127-128`), so "handle not among 11 rows" has at least one other explanation I cannot rule out from the files. This matters for the A-versus-B comparison only for the environment route, which both sides already reject. A's case does not depend on it: points 1 to 3 in my weaknesses section stand if the variable is set only in workers. The sentence in `V-A:9` should be downgraded to "likely, not proven".

**A-002: QUALIFY** (a model reliably applies the trigger guard; neither side measures it).
Accept that neither failure rate is measured, and that A's quoted-token rule is applied by a model reading text (`V-A:22`). Reject that the two tasks are equally hard. Recognising a standalone token outside quotes is a lexical test on the line the model was just given. Recognising a live preamble is a judgement about the provenance of prose in a long context, and the preamble and task arrive together (`V-B:14`). A also has checks that exercise the rule (AC-2.8 `SPEC4:269`, AC-1.7 and AC-2.9 for the guard in the live spec `SPEC-LIVE:323`, `SPEC-LIVE:331`); B has none. The recommended remedy is to measure A's rate during P1 live checks, not to assume it. L3 note: the failure modes differ in cost. A's error on a person's line (treating quoted text as the flag) is caught by AC-2.8; B's error on a person's session (treating a taken-over terminal as unattended) has no check and no visible signal.

**A-003: ACCEPT** (the options are not mutually exclusive; neither considered a hybrid).
Accept: the diff analysis is right that neither variant discusses a hybrid, and the hybrid exists in the live contract (`WC` "Brief guard" case 1; `SPEC-LIVE:60`, `SPEC-LIVE:401`). The hybrid is "require the flag; when a live preamble is present and the flag is absent, refuse instead of prompting". It uses B's preamble recognition only in the worker session, where Orca already requires it (`CAPS:148`), and only to refuse, never to switch a command's behaviour. That answers B's best argument (the forgotten-flag stall) without making commands Orca-aware (non-goal 1) and without the taken-over-terminal hazard, because a refusal at the start of a brief cannot change a person's later commands. It is A with a backstop. A residual risk remains: the guard still depends on the model recognising the preamble and on reading every command copy (`WC` "Brief guard"), so it narrows the stall rather than eliminating it.

## Point table
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
