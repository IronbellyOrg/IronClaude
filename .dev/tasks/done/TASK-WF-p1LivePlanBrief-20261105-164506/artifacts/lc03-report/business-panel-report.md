# Business Panel Report: D1 option (a), an explicit `--unattended` flag

- **Input**: `.dev/orca-command-refactor/decisions/D1/option-a.md` (24 lines, read in full this run)
- **Mode**: discussion (collaborative), forced by `--mode discussion`
- **Panel**: Michael Porter, Peter Drucker (selected with `--experts "porter,drucker"`; the other seven experts did not take part)
- **Run**: unattended worker run, task `task_a8ae733797de`
- **Nature of the voices**: simulated analysis through each expert's published frameworks. These are not quotations and not the experts' actual views.
- **Evidence limits**: the document's own `SPEC:N` and `CAPS:N` citations were NOT opened or checked in this run (UNVERIFIED). One cross-check was made against `~/.claude/WORKER-CONTRACT.md`, which was read in full this run (see section 2).

## 1. The decision under analysis

The document argues that a command should switch to unattended behaviour only when its command line carries the standalone token `--unattended`. Nothing in the environment, the conversation or Orca turns it on.

Its case rests on three claims:

1. **Safety.** A person never types the flag, so a person's run cannot be switched by accident. The document says detection already misfired in one observed session (2026-11-02): `ORCA_TERMINAL_HANDLE` was set in an Orca terminal that was not a dispatched worker.
2. **Reliability.** The flag is plain text, so a check can read it. It does not name a tool, so any caller (`claude -p`, CI, a future orchestrator) can use it. A command accepts it only after its gates are converted.
3. **Cost.** One shared parse rule plus a short section per command. It can be changed later.

The document names one weakness itself: if a coordinator forgets the flag, the command prompts, the worker stalls with no completion message, and Orca reports it as healthy.

## 2. Expert discussion

### Opening: Porter (competitive strategy, trade-offs, fit)

**Strategy is a choice of what not to do, and this document makes one.** It gives up automatic switching (no coordinator effort) to buy a guarantee that a person's run is never switched. That is a real trade-off with a clear winner: the two ways of being wrong are not equal. If the flag is forgotten, the system fails toward doing nothing (a stall that can be seen and retried). If detection misfires, the system fails toward acting without asking (a person's prompts vanish, and outward defaults go off). A design should fail in the cheap direction. Option (a) does.

**The activities reinforce each other, which is what makes it hard to copy and hard to break.** The parse rule, the per-command section, the phase gate ("a command accepts the flag only once its gates are converted") and the brief template all point at the same token. A reader or a checker can verify each by text.

**Caller neutrality is positioning.** Because the switch names a condition ("no person") and not a tool, the same flag serves Orca, `claude -p` and CI. That widens who can use the mechanism without adding any code.

**Where I push back: "changing later is cheap" is only half true.** Adding a second trigger is cheap to write. But if detection is added as an extra trigger that also switches the mode, it is an OR, and an OR inherits detection's false positives, which is the exact misfire the document rejects. Detection can only be added safely as a warning (for example "environment says worker, flag missing"), never as a switch. Once 16 commands, the brief template and the guard all name the flag, taking it out is expensive. The flag is closer to a one-way door than the document admits.

**The evidence for the strongest claim is thin.** The misfire is "observed" in one session on one day. That is enough to disprove "detection is always safe", but not enough to size how often it happens.

### Response: Drucker (effectiveness, delegation, management by objectives)

**I agree with the ordering of the criteria.** Safety for the person comes first, then reliability, then cost. The first question for any system is who it serves and what must never be harmed. Here the person at the keyboard is the one whose work must not change, and the document protects that person first. That is doing the right thing before doing the thing right.

**An explicit flag is an explicit objective.** Delegation fails when the delegate has to guess. The brief states the command, the report directory, the blocked-gate policy and the commit grant in plain text. A worker that has to infer "am I unattended?" from its surroundings is a worker being managed by hope.

**But a system that depends on someone remembering will eventually fail.** The document's own answer to the forgotten flag is "the brief template and the stall proof catch it, but only after the fact". That is weak management: the first signal is damage. I would ask for two things: a check *before* the work starts, and a measure that tells you how often the weakness bites.

**Cross-check against the contract file (read this run).** `~/.claude/WORKER-CONTRACT.md:16-19` already defines a brief guard. In a worker session, before anything runs, the worker reads the command file copies and refuses with `guard refused: brief lacks --unattended` when the command has an `## Unattended mode` section and the line has no flag. For converted commands this turns the silent stall into a stated refusal before work begins. So the document's "only after the fact" is out of date for converted commands, or it was written before the guard. Two limits remain: the guard is prose that the model applies, not code that runs, and it does not help for a command that has gates but is not yet converted.

### Porter replies

That guard strengthens the case: it adds a second activity that supports the first, and it is the right shape (it checks the flag, it does not replace it). My reservation stands on the reversibility claim and on the thin evidence. I would add that the guard itself reads the worker's preamble, which is a limited form of environment awareness. That is acceptable only because it can refuse, never switch. The line between "detect to warn or refuse" and "detect to switch" is the design principle, and the document should say it.

### Drucker closes

Agreed, and I would make it measurable. The cost of option (a) is carried by the coordinator, so count what the coordinator experiences: guard refusals for a missing flag and stalls caused by one. Without a count there is no way to know whether the weakness is a rounding error or the main failure. A decision with no review point is a decision nobody will revisit.

## 3. Consensus and disagreements

### Consensus

1. **Adopt option (a).** Both experts support it. The asymmetry of failure (stall versus silent behaviour change) is the deciding argument.
2. **The "Known weakness" paragraph should be updated.** `~/.claude/WORKER-CONTRACT.md:16-19` adds a before-the-run refusal for converted commands that the document does not mention.
3. **Detection must never be a switch.** It may warn or refuse, never turn the mode on.

### Disagreements

| Point | Porter | Drucker |
|---|---|---|
| How worrying is lock-in? | The flag is close to a one-way door once 16 commands, the template and the guard name it; "changing later is cheap" overstates. | Less concerned. Reversibility matters less than whether the objective is clear and reviewed. |
| What closes the remaining weakness? | Strengthen the fit: keep the guard, and say in writing that detection may only warn or refuse. | Measure it: count refusals and stalls, and set a review point. No new mechanism until the count justifies one. |
| How strong is the evidence? | One session is enough to disprove "always safe", not to size the problem. | Accepts it for the decision; wants the count to supply the size later. |

These are differences of emphasis. Neither expert argues against the choice.

## 4. Priority-ranked recommendations

1. **Adopt option (a).** The two failure modes are unequal, and (a) fails in the cheap direction.
2. **Rewrite the "Known weakness" bullet in `option-a.md` (line 19).** State that for converted commands the brief guard (`~/.claude/WORKER-CONTRACT.md:16-19`) refuses a missing flag before any work, and state the two limits: the guard is prose the model applies, and it does not cover an unconverted command that still has gates.
3. **Replace "changing later is cheap" (line 23) with a precise sentence.** Detection can be added later only as a warning or a refusal, never as a second switch, because an OR of the two triggers brings back the misfire the document rejects.
4. **Add a review measure.** Have the coordinator's run notes record each guard refusal and each stall traced to a missing flag, and name who looks at the count and when. The decision owner sets any threshold; this report does not invent one.
5. **Strengthen the misfire evidence when convenient.** Repeat the check (variable set versus the dispatched-worker list) in a second session, so the claim does not rest on one observation. Lowest priority: the decision does not depend on it.

## 5. What this analysis did not do

- It did not open `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` or `.dev/orca-command-refactor/inventory/orca-capabilities.md`, so every `SPEC:N` and `CAPS:N` claim in the input is taken as written (UNVERIFIED).
- It did not re-run the live check behind the `ORCA_TERMINAL_HANDLE` observation.
- It did not compare options (b) or (c); the input document argues only for (a).
- Only two of the nine experts took part, as requested. Other lenses (for example Taleb on failure modes, Meadows on feedback loops) were not applied.
- It implemented nothing and changed no file other than this report and its contract.
