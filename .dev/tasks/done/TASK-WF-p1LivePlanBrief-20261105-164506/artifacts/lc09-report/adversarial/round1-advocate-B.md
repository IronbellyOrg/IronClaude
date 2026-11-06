# Round 1 advocate statement: Variant B (command detects it runs as an Orca worker)

Advocate: Variant B. Opponent: Variant A (explicit `--unattended` flag). Depth: quick, round 1 of 1.

## Position
The defensible core of B is narrower than B's text. It is this: the live Orca preamble (Task ID plus Dispatch ID), not the environment variable, is the signal that a session is a worker, and a coordinator that forgets a flag must not be able to leave a worker stalled on a prompt that Orca reports as healthy.

B as written (every command detects the preamble itself) loses to A on testability, Orca coupling and migration cost. I say so below. B's real contribution is the stall hazard and the preamble as a signal.

Context the lead should have. The current spec (`orca-worker-contract-spec.md:401`, section 9) already records D1 as approved on 2026-11-02 as "Option (c): `--unattended` is the only switch; from P1 the worker session also applies the brief guard. Commands never detect Orca." `~/.claude/WORKER-CONTRACT.md` lines 16-20 spell out that guard. It is a hybrid: the flag stays the switch, and a worker session that holds a live preamble refuses to run a convertible command whose line lacks the flag. So B's preamble insight was adopted, but moved out of the commands and into the worker session. That outcome supports B on points C-003, X-001 and U-005, and supports A on C-001, C-004, C-005 and C-006.

## Steelman of Variant A
A's strongest argument has four parts, and each is correct.
1. A flag is a lexical, greppable token. A person never types it, and the parse rule (standalone token outside quotes) is live-checked by AC-2.8 (v4 `SPEC:269`). Preamble recognition is prose the model must notice, and nothing can grep for it.
2. A names the condition (no person at the keyboard), not a tool. `claude -p`, CI and a future orchestrator can use it with no Orca. Detection ties every command to Orca, which spec non-goal 1 and SA-2 forbid (`SPEC:314`, `SPEC:170`).
3. A is migration-safe. Detection can be added later as an extra trigger; removing detection from 35 commands later is not cheap.
4. A is honest about its one weakness (a forgotten flag stalls the worker) and names the after-the-fact catches (brief template, step-3 stall proof).

A also gets the safety asymmetry right: its failure direction (flag missing, so the command prompts) leaves a person's behaviour intact, whereas B's false-positive direction takes prompts away from a person.

## Key strengths claimed
- **Orca defines a worker by the preamble.** `orca-capabilities.md:148` quotes the guide: "No live preamble and no explicit supervision | Ordinary terminal agent"; only a session that received a preamble with Task and Dispatch IDs is a worker (`[G]` line 38). Preamble detection reuses Orca's own rule and a person's own session has none.
- **The stall is silent and Orca calls it healthy.** `CAPS:52` and `CAPS:129`: "A waiting worker is healthy, not failed." The spec itself calls the silent stall "the real failure mode for a command prompt" (v4 `SPEC:47`). A design where the coordinator's omission cannot produce that state is worth something, and the approved spec agreed by adding the brief guard (`WORKER-CONTRACT.md:17`, case 1).
- **The environment-variable observation does not condemn the preamble route.** The 2026-11-02 observation is about `ORCA_TERMINAL_HANDLE` only. `CAPS:149` shows Orca's own error text treats the variable as the identity of "a live Orca terminal", so it marks any Orca tab. Nothing observed says a person's tab carries a Task/Dispatch preamble. A's "detection would misfire" (A:9) is therefore proved for the environment route and merely asserted for the preamble route.

## Weaknesses identified in Variant A
1. **A treats the stall as a footnote.** A:19 files it under "known weakness" and says the catches work "only after the fact". For an unattended worker, after the fact means a worker parked indefinitely with no `worker_done` and a healthy status (`CAPS:52`). A's own mitigation (the 7.2 step-3 stall proof, v4 `SPEC:238`) is a test-time check, not a runtime prevention. The approved spec found A alone insufficient and added a worker-side guard. A:3 ("Nothing in the environment, the conversation or Orca turns it on") is superseded by that outcome.
2. **A over-generalizes its observation (C-002, X-001).** A:9 uses an environment-variable observation to say detection in general "would misfire". Preamble detection is untouched by that evidence.
3. **A's "flag or detection" framing is a false choice.** The hybrid shows the flag can stay the switch and still let the worker session react to the preamble (A-003).
4. **A's quoted-argument rule is only as strong as the model applying it.** Commands are prompts, so A:22 itself admits the "parse" is applied by the model reading the rule. That is the same model-reliability assumption (A-002) A uses against B, and A has not measured it either.

## Concessions
1. **Testability (C-004): A wins.** B:17 is right about its own weakness. There is no token to grep, and AC-1.1 (v4 `SPEC:257`) cannot assert detection text the way it asserts a section.
2. **Orca coupling (C-005): A wins.** B:18 concedes it. Non-goal 1 (v4 `SPEC:314`, current `SPEC:385`) and SA-2 forbid "Orca-specific branching" in commands, and commands run in other projects. Detection inside commands conflicts with both. The approved spec confirms: "Commands never detect Orca."
3. **Trigger mechanism (C-001): A wins.** The approved D1 is the flag.
4. **X-002 (B contradicts itself): the criticism is fair.** B:9 says detection "removes that whole failure class" while B:14 and B:17 say a wrong guess is invisible until a run stalls. Correct statement: detection removes the coordinator-omission failure and replaces it with a model-miss failure. Which is rarer is unmeasured (A-002). B:9 overstates.
5. **Environment route is unsafe.** Both variants agree, and `CAPS:149` explains why. B should not claim it.
6. **Cost and reversibility (C-006): A wins.** B:25 says so.
7. **B:19 states as fact that the `--print` headless signal "would not fire".** The spec lists this as an assumption (v4 `SPEC:391`, item 9, "assumed not"). It is UNVERIFIED, so B:19 is an inference.
8. **B:14 says the preamble "arrives on the same command line as the task (CAPS:47)".** `CAPS:47` only says that for Claude the task is passed on the command line (`promptInjectionMode: 'argv'`). It does not say the preamble is in that argv. Plausible, not shown.
9. **B:10 ("no new flag on 35 commands", citing `SPEC:189-195`) is weak.** The cited table lists which commands accept the flag. It does not support shorter briefs, and B:25 admits each command still needs per-command detection text, so the saving is not real.

## Citation spot-checks
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

## Shared assumption responses
**A-001: QUALIFY.** The conclusion (environment variable is unsafe) is right, but not because of one observation. `CAPS:149` quotes Orca's own error text, "run the command inside a live Orca terminal with ORCA_TERMINAL_HANDLE set", which treats the variable as the identity of any live terminal. That is independent support. What stays open is the claim for other Orca profiles or versions: the current spec still lists it as UNVERIFIED item 13 (`SPEC:448`). Accept for the environment route; do not extend it to the preamble route.

**A-002: QUALIFY.** Neither side measured how reliably a model applies its trigger rule. A's rule is lexical (a standalone token outside quotes); B's is semantic (recognize a live preamble). A's is probably easier, and A's failure direction (missing flag, so the command prompts) is the safer one for people. B's false-positive direction breaks SA-1. But A's error silently produces the stall A admits it cannot prevent, so the failure rates must be measured, not assumed. The live checks AC-1.2, AC-1.7 and AC-2.9 are the right way to measure them.

**A-003: REJECT.** The two options are not mutually exclusive, and the approved spec shows it. `WORKER-CONTRACT.md` lines 16-20 ("Brief guard") keep `--unattended` as the only switch in commands and add a worker-session rule: with a live preamble and no flag on a convertible command, refuse and send `worker_done --outcome failed` with a body starting `guard refused:`. That keeps A's testability and caller-neutrality, and it keeps B's insight that the preamble is the right worker signal and that a forgotten flag must not stall. Honest scoring: this hybrid is closer to A, because the commands stay Orca-free; B-as-written (commands detect) is superseded.

## Point table
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
