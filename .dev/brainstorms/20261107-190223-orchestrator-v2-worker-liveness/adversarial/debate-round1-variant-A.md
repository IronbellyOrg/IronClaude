# Debate Round 1: Advocate for Variant A (variant-1-opus-architect)

Scope: Round 1 of the adversarial debate (depth deep). Inputs read: `variant-1-opus-architect.md` (A), `variant-2-opus-analyzer.md` (B), `variant-3-haiku-backend.md` (C), `diff-analysis.md`, `../seed-brief.md`, `src/superclaude/core/WORKER-CONTRACT.md`, `.dev/issues/431/issue-body.md`. No Orca runtime was observed; runtime claims are documented, not tested.

## Steelman of Opposing Variants

### Variant B

B's strongest form is an evidence-first diagnosis. "§1.1 The root cause behind all eight cases" names one root cause for all eight cases: a past event was read as current state. Every rule then follows from it. FR-004 makes an observation older than 10 minutes count as unknown, not healthy. "§3.2 The arrival vs change matrix" separates a heartbeat arriving from progress changing. This is exactly what failed in case 1 (`issue-body.md:16`), and B notes that the design holds whether a timer or the model sent those heartbeats (UNVERIFIED).

B is the only variant that splits each case's cause into an occurrence cause and a detection cause, with a confidence for each ("§5 Mapping", "§5.1"). This tells a reader which fix removes the failure and which only bounds it. "§6.1 Mechanism (verified)" rests on a `check --help` read dated 2026-11-07. B then:

- wakes on all nine types (FR-011), the literal reading of the success criterion "a coordinator wait never filters out a worker message type" (`seed-brief.md:43`);
- processes the whole batch before `check --ack` (FR-012), closing the secondary case-4 hypothesis it names (whole batch acked after reading only the matching types).

B models freshness and reachability more precisely than A:

- S7 `unreachable` and S8 `exited` are separate states ("§2.2 States"). They need different responses, and only `exited` is stall proof (`WORKER-CONTRACT.md:72`).
- Idle needs two sources: a transcript entry at least 5 minutes old, plus an empty-prompt classification ("§4.2 Per-state rules").
- In v1 the sweep stats the contract path of each worker (FR-009). This directly catches finished-unreported (S9) and avoids case 3's single-file mtime trap, because the stat targets the closing artifact, not any file.

The worker-side rules hold up in failure cases:

- The handoff file is written even when a step fails (FR-025) and is listed in the artifacts (WR-3).
- WR-7's `expect_silence_min` lets a worker declare a quiet period.
- "§9.2 Why not the preamble or the commands" argues placement from WC-8 and `:7`.

Adaptive W (FR-010) keeps heartbeat wakes affordable on a large fleet. "§11.3" refuses L4 on any harness whose adapter cannot produce a stall proof, which keeps the portable core honest. Replay-fixture acceptance ("§13.1") makes every bound testable without a live run.

### Variant C

C's strongest form is a backend engineer's reading: the coordinator is a distributed controller that can crash, run twice or see clocks jump, so the design must hold under those faults as well as when every message arrives.

The design is built around that reading:

- FR-005's `attempt_epoch` fences stale observations and stale acks out of a replacement attempt.
- NFR-006 is a transactional action ledger.
- NFR-005 persists a message before it is acked.
- NFR-010 fails closed.
- NFR-008 sets limits for untrusted input.
- NFR-009 adds a watchdog outside the coordinator's own turn.
- A controller lock prevents two coordinators acting on one worker (risk table, "Risks, False Positives and Edge Cases").

Together these cover the shared assumptions A leaves unstated: C-044 transcript freshness, C-045 clocks, C-046 resume input and C-047 one coordinator. "Worker State Model" separates five facts (reachability, attention, last_progress, delivery, outcome) and gives only a partial precedence. That avoids a single total order that can be wrong at the edges.

C is the most cautious about typing into a worker:

- A nudge goes only to a positively identified prompt.
- A terminal copy of an answer is never typed while `ask` still owns terminal input (FR-017: "If ask still owns terminal input, a permission prompt is present, input semantics are ambiguous, or no terminal exists, do not type").
- Interrupt is never used.

C also refuses outright to let IronClaude invent a stall-proof class: "A context error alone is NOT an additional Orca stall-proof class" ("Response Ladder"). This is the strictest reading of the brief's constraint that WC-6 acts only on Orca's proofs (`seed-brief.md:25`, `:35`).

The restart budget is tighter: one per 60 minutes and two per lineage, with no second replacement after a same-checkpoint thrash (FR-020). That bounds a case-8 loop harder than A or B.

C keeps the core free of Orca and screen strings (FR-025, FR-026). Its acceptance tests cover crash boundaries, a harness fixture with no terminal, no transcript and no ack, and a stress test with a message flood (FR-027 tests 1-12). That makes C the most portable and most testable design under faults. Its WC-7 amendment also says the top-level session must invoke the real command through the Skill tool. This is the P1-C5/WC-7 lesson that the other two variants omit.

## Strengths of Variant A

1. **Every observation records its proof class.** "§3 Observation record" (FR-001/002) labels each observation with how strong its evidence is. An unknown or stale observation is never read as healthy; it starts an L1 probe. This rules out the single error that the eight cases share: a weak signal counted as alive (`seed-brief.md:17`, `issue-body.md:14`). The same field draws the line that WC-10 needs between absence and stall proof (`WORKER-CONTRACT.md:44`).
2. **The coordinator never interrupts and never manufactures proof.**
   - "§8 Rungs" L2 runs "never with `--interrupt`".
   - FR-025 bans `--interrupt`, `/clear`, `/compact` and Escape.
   - L4 needs Orca's positive stall proof after L2 has failed twice ("§8 Rungs").

   These rules meet the brief's demand that "a nudge into a working session must be harmless" (`seed-brief.md:37`). They also leave WC-6's proof set Orca-owned (`WORKER-CONTRACT.md:69-74`, `seed-brief.md:71`).
3. **The coordinator never answers a person-only prompt.**
   - "§2 Named states" ranks the person prompt above context-exhausted.
   - FR-024 bans typing an answer into a permission or decision prompt.
   - The person-prompt row of "§8 State-to-ladder map" goes to L5 at once.

   Case 6's prompt ("This shell script runs rm", `issue-body.md:45`) is exactly the input that a coordinator keystroke must never answer. Orca says "A waiting worker is healthy, not failed" (`seed-brief.md:69`).
4. **The ack rides on a carrier that already exists in v1.** "§7 Protocol (`ironclaude.ack/1`)" sends the ack as a `status` message, because heartbeats follow the preamble cadence and are not sent while blocked in `ask` (`WORKER-CONTRACT.md:7`, `:61`). `status` is a lifecycle message from the top-level session (WC-7, `:58`), so no command gains an Orca call (WC-8, `:38`). The design satisfies the success criterion "confirmed read by an explicit worker acknowledgement" (`seed-brief.md:44`) without asking Orca or the preamble to change. "§7 Idempotency" adds `duplicate` and `supersedes` rules, so a mailbox copy and a terminal copy of one reply are applied once.
5. **The v1/v2 line is drawn by one test that anyone can apply.** "§10 Contract Changes: v1 Now vs v2 (#423)" puts in v1 anything two sessions can do by following text with existing verbs, and in v2 anything that needs a running component, persisted state or a hook. The "§10 Delivery table" lists every capability against that test. "§10 WC rules amended (proposed wording)" gives the exact text for WC-10, WC-12, WC-3, WC-5 and the Heartbeats bullet, plus the new WC-14. It also states that WC-7 and WC-8 are not amended, which meets success criterion 5 (`seed-brief.md:46`). FR-030 makes each v1 amendment adoptable on its own.
6. **Bounds are stated as data, and sweep cost stays fixed.**
   - "§4 Timing parameters" puts W, S, Q, G, A, D and F in one table, so tuning means changing data, not rules.
   - "§4 The sweep" runs at most once per S. It makes two fleet-wide calls whatever the fleet size (NFR-004, AC-14). Probes reach only suspicious workers.
   - The bounds (idle 15 min, person prompt 10, `ask` 5 + A, context-exhausted 15, exited 5) all meet the 15-minute target (`seed-brief.md:42`) with the 5-minute wait timeout already in v1, without a 1-minute timer.
7. **Worker rules sit where the needed fact lives.** "§9 Worker-Side Rules" places each rule by asking who knows the fact it depends on. The preamble owns syntax and cadence (`:7`). Commands do not know they are in a chain (`:5`, WC-8). So chain continuity (WR-1), chunked reads (WR-2) and handoff files (WR-3) belong to the worker session, that is, contract section 3. WR-1 fixes case 7 at the source (`issue-body.md:22`). WR-6 fixes case 4 at the source (`:19`), while FR-015 to FR-017 remain the safety net.
8. **A case-8 loop cannot repeat like-for-like.** "§8 Restart budget" carries the same-cause rule: a repeated cause forces a changed plan and the person's approval. "§8 Resume-note format" puts on-disk progress in the new brief, because a brief cannot change after creation (`WORKER-CONTRACT.md:69`). This meets "a restart must preserve on-disk progress" (`seed-brief.md:37`).
9. **The design is portable through registries.** "§11 Adapter interface" and "§11 Registries" make a new harness, signal or message type a matter of adding a row (NFR-005, FR-018), and "§11 Porting checklist" lists the steps. This meets success criterion 6 (`seed-brief.md:47`).

## Critiques of Variants B and C

Each critique below names the claim it attacks and the evidence that would refute the critique.

### Variant B

- **B1. B creates its own stall proof, which contradicts the Orca stall-proof fact.** "§8.2" row S6 reads: "`terminal send --interrupt` plus 'write your handoff file now (WR-3), then end your turn'. If the session then ends its turn without `worker_done`, that is stall proof, so L4". Orca's proof class "a transcript whose final agent turn sent no `worker_done`" (`seed-brief.md:71`) is evidence that the worker stopped on its own. B's coordinator orders the turn end and then cites it as that proof. This gives automatic restart in v1 for context exhaustion, the very thing B's own C-9 ("§10.1") says needs Orca's or the person's acceptance. It also breaks WC-6's "positive stall proof" (`WORKER-CONTRACT.md:69-74`). *Refuted if* Orca documents that a final turn ended on coordinator instruction still counts as stall proof.
- **B2. B's interrupt can land on a person-only prompt.** "§2.3 Precedence" ranks S6 context-exhausted above S4 person-prompt. A worker that thrashes and also shows a permission dialog is classed as S6, and the §8.2 S6 row sends it `--interrupt`. The brief requires that a nudge into a working session be harmless (`seed-brief.md:37`). Orca treats a worker waiting on a prompt as healthy (`:69`). *Refuted if* B shows that S4 and S6 cannot be true at the same time.
- **B3. B's own acceptance criterion breaks the 15-minute target.** In "§13.1", AC-1 states "case 1 detected by 20 min after onset at worst", while the success criterion is "15 minutes or less for ... thrashing" (`seed-brief.md:42`). "§4.2" says S6 is recorded at 15 minutes, but a restart decision needs a second read 5 minutes later. *Refuted if* AC-1 is restated as 15 minutes or less.
- **B4. NFR-004 contradicts FR-009.** NFR-004 says "a fixed number of fleet-wide Orca calls (three), whatever the fleet size". FR-009 adds "one `stat` per worker contract path" and a heartbeat-record update for each worker. The stat step grows with the fleet, so the claim of constant cost is false as written. The same claim backs R10's mitigation ("§12"). The stat itself is cheap; only the claim is wrong.
- **B5. B can type a copy into a worker that is blocked in `ask`.** In "§7.3", A3 types a copy at 5 minutes when the worker is in S3, S5 or S11. S5 is "blocked in ask", where the foreground process is the `ask` call. A shares this flaw (X-010, conceded below). B's version is wider because it also covers S11 unknown.
- **B6. Host loss goes unreported for 30 minutes.** The "§4.2" and "§8.2" S7 rows report an `unverifiable` worker only after 30 continuous minutes, against the 15-minute target for blocked states (`seed-brief.md:42`). A and C report it at 10 minutes.
- **B7. Every wake triggers a sweep.** FR-008 runs a sweep "after every wake or timeout". With heartbeats in the wake set, six workers can wake the coordinator every few minutes. "§6.1" says this is intended and that sweeps run "at most once every 5 minutes", but FR-008 itself carries no such limit. That limit belongs in the FR (A's "§4 The sweep" states it).

### Variant C

- **C1. C sends its ack on a heartbeat, which contradicts `:7` and WC-3.** FR-016 sends `read_ack` "through existing heartbeat `--payload`" and admits that "The negotiated dispatch preamble must permit this immediate control acknowledgement". The preamble owns the cadence and syntax of heartbeats (`WORKER-CONTRACT.md:7`), and the brief forbids copying or bending them (`seed-brief.md:35`). So the ack has no carrier in v1. FR-016's own fallback (`ack_unsupported`) admits this. *Refuted if* the current preamble documents an immediate out-of-cadence heartbeat.
- **C2. C's v1 ack bounds have no v1 mechanism.** FR-017 probes at 2 minutes, types a copy at 5 and reports to the person at 10. With no ack carrier in v1 (C1), a worker that read the answer correctly and is 20 minutes into a step is reported at minute 10 (X-009). Every answer would be reported as unread.
- **C3. C's heartbeat for `blocked_ask` runs into WC-3.** FR-008's `mode` enum includes `blocked_ask`, but WC-3 and the Heartbeats bullet forbid any heartbeat while blocked in `ask` (`WORKER-CONTRACT.md:53-56`, `:61`). The value is safe only if sent strictly before `ask` starts, and C does not say so (X-020).
- **C4. C lets context exhaustion end by itself.** The "Worker State Model" exit "Evidence of useful resumed work → progressing" means a thrashing worker can clear its own incident. Case 1 ran about four hours and case 8 about 46 minutes with heartbeats still arriving (`issue-body.md:16`, `:23`). Activity that looks useful is exactly the signal that misled the coordinator. C's own risk table says heartbeat volume cannot clear it. *Refuted if* C limits "useful resumed work" to a new checkpoint revision (`progress_rev`) written after the thrash.
- **C5. C's v1 case-4 bound relies on v2 machinery.** "Mapping of the 8 Observed Cases" and FR-027 test 4 promise case 4 "within 1 minute". That is the type-free drain that runs every minute (FR-010), which C itself calls v2. In v1 the bound is one 5-minute cycle (X-021). The mapping table should say so.
- **C6. C's 6-minute idle bound has no scheduler in v1.** Idle at 6 minutes needs "a second sample within 1 minute" ("Detection Rules and Time Bounds"), which needs a timer that is not part of the coordinator's 5-minute wait. A coordinator session that follows text in v1 cannot hold it (X-013). 15 minutes meets the brief.
- **C7. C's bounds cost more than the target needs.** C's stated bounds (6-minute idle, 1-minute delivery) need a drain every minute (about 240 drains in four hours, C-039), plus a whole-worktree inventory (NFR-003, availability UNVERIFIED) and 30-second probes. C marks its own fleet cost budget UNVERIFIED. If any of this runs in an LLM coordinator instead of a v2 process, each drain uses context (A-002).

No variant breaks WC-8: none adds an Orca call to a command. On WC-7, C's ack is a heartbeat from the top-level session, so it is compliant on sender but not on cadence (C1).

## Concessions

1. **X-001: heartbeats belong in the wake set.** "§6 Wake set versus read set" keeps heartbeats out of the wake set. By A's own read-set argument nothing is lost, but the success criterion says "a coordinator wait never filters out a worker message type" (`seed-brief.md:43`). A heartbeat-only batch whose payload shows `pending_ack` or `near_limit` would then wait a full W. B (FR-011) and C (FR-010) both wake on all nine. The fix keeps A's "at most once per S" sweep limit, so a heartbeat wake costs one batch read, not one sweep.
2. **X-004: context exhaustion should not become a stall proof that IronClaude writes.** A's v2 WC-6 amendment ("§10 WC rules amended", last bullet) redefines a proof that the brief assigns to Orca (`seed-brief.md:25`, `:71`). C's refusal ("Response Ladder") is the safer position. Under it, a confirmed exhaustion verdict leads to L5 with a ready restart plan, and L4 runs only on the person's go, in v2 as well, unless Orca itself adopts the proof class.
3. **X-010: no typed copy while `ask` owns the input.** "§7 Protocol" step 4 types a terminal copy at A = 5 minutes for a worker blocked in `ask`. C's FR-017 guard is right: a worker blocked in `ask` has the `ask` call in the foreground, and keystrokes may reach it, not the model. A should take C's guard and report instead.
4. **X-012 and C-019: C's restart budget is tighter and fits case 8 better.** A allows 2 restarts per 6 hours, which permits 4 restarts of one unit in 12 hours. C's limits (one per 60 minutes, two per lineage) plus A's same-cause rule are stricter.
5. **X-006: finished-unreported ranks above context-exhausted.** If the contract on disk shows the work is finished, nudging for `worker_done` is cheaper and less destructive than starting a restart plan. B's order (S9 above S6) is right on this pair. A's order is kept for the person prompt (X-005).
6. **S-010 and C-001: B's split of unreachable from exited is clearer.** A puts both under one state with a sub-state. They need opposite responses: `exited` is stall proof and `unverifiable` never is (`WORKER-CONTRACT.md:72`). B makes them separate states.
7. **S-006 and S-007: B's analysis method is stronger.**
   - Separating each case's occurrence cause from its detection cause ("§5").
   - The arrival-vs-change matrix ("§3.2").
   - The constraints-check column ("§10.3").
   - Replay fixtures ("§13.1").
   - Adaptive W (FR-010).

   All five improve on A's presentation.
8. **C-024: B's handoff rule is stronger.** B writes the handoff file even when a step fails (FR-025) and allows up to 40 lines. A's 20-line file written only on success misses the failed step, which is exactly the one a restart most needs.
9. **C-013 and C-010: B's v1 checks are better.** B's per-worker `stat` of the contract path is a cheap, specific check in v1, better than A's "not in v1". B's two-source idle confirmation is stronger than A's flat Q plus one probe.
10. **S-008, C-037 and C-016: C's durability is missing from A.** A has no dedicated section on the coordinator's own faults. A lacks C's `attempt_epoch`, transactional ledger, persist-before-ack, fail-closed, untrusted-input limits and controller lock, and v2 (#423) needs them.
11. **Shared assumptions that A leaves unstated** (C-042 to C-047): C or B states each one, and A should adopt those statements. This covers transcript freshness, clocks, resume input, one coordinator, payload integrity and the reliability of `agentWait`.
12. **WC-7 clarification:** C's amendment requires the top-level session to invoke the actual command through the Skill tool. That matches the WC-7 decision of 2026-11-07 recorded in project memory (P1-C5: a worker that only reads a command file does not satisfy WC-7; not re-read for this round). A does not reflect it.
13. **X-019 and C-030: hooks should be accelerators, as in B.** B reads Orca's own evidence first and uses hooks only as v2 accelerators. A's v2 Stop hook, which refuses a turn end, is more invasive than the problem requires.

## Shared Assumption Responses

| ID | ACCEPT/REJECT/QUALIFY | Reason |
|---|---|---|
| A-001 | QUALIFY | No variant guards the coordinator itself in v1. A v1 rule should name the person as the backstop if the coordinator stops looping. v2 needs C's watchdog outside the coordinator's turn (NFR-009). |
| A-002 | QUALIFY | A's two fleet calls, made at most once per S, bound the cost of each sweep. They do not bound the cumulative context of about 48 sweeps in 4 h. Sweep output must be summarised to changed workers only. The budget is UNVERIFIED. |
| A-003 | QUALIFY | Plausible, but no variant measured it. Record it as UNVERIFIED until the first v1 run. |
| A-004 | REJECT | A worker inside a long tool call or subagent fan-out cannot ack until its turn reaches a checkpoint (WC-10, `WORKER-CONTRACT.md:44`). Each ack timeout must re-derive state before L5. A's WR-7 `expect_until` and the 10-minute A reduce this but do not remove it. |
| A-005 | QUALIFY | Orca documents null as "looked, none" and absent as "never looked" (`seed-brief.md:69`). Its delay and reliability are UNVERIFIED. A screen read stays the confirming fallback for case 6. |
| A-006 | ACCEPT | Documented: only `terminal send --wait-submit` gives a turn-start receipt, and only for terminal-backed workers (`seed-brief.md:67`). |
| A-007 | QUALIFY | UNVERIFIED. The ack's body first line (`ack R-...`) must be authoritative, so a mangled payload never loses an ack. Check it in the first v1 run (B and C both state this). |
| A-008 | QUALIFY | A transcript read can catch a turn in progress. Read it twice, one sweep apart, before treating "final turn sent no `worker_done`" as proof (C states this as UNVERIFIED). |
| A-009 | ACCEPT | WC-10 and WC-6 forbid stop, retry and release on absence. Neither forbids a probe, nudge or ask (`seed-brief.md:71`, `:80`). |
| A-010 | QUALIFY | Cases 4 and 7 show workers break rules. Worker rules shrink the failure rate. Coordinator detection (A FR-015 to FR-017) stays the safety net. |
| A-011 | QUALIFY | Deadlines should use the coordinator's own receipt time, or a monotonic clock in v2 (C NFR-004). A cross-host timestamp only confirms. |
| A-012 | QUALIFY | Only `/sc:implement` has a verified resume input. For other commands the resume note is advisory, and restart re-runs the unfinished step. |
| A-013 | QUALIFY | Must be stated. v1 rule: one coordinator per run mailbox. v2 needs a controller lock (C) and detection of two listeners (B R9). |
| A-014 | QUALIFY | Freshness is UNVERIFIED. A marks an observation stale after two sweeps, so a stale projection is read as unknown and never as healthy. |
| A-015 | ACCEPT | A returned batch is the whole FIFO batch (`seed-brief.md:66`). Processing all of it before `check --ack` is the rule in A (FR-015) and B (FR-012). |
| A-016 | ACCEPT | In case 1, heartbeats continued through four hours of thrashing (`issue-body.md:16`). Arrival is not progress, whoever sent them (sender UNVERIFIED). |
| A-017 | QUALIFY | Documented for listed types. Whether `--types` can be omitted to wake on every type is UNVERIFIED (A "§6"). |
| A-018 | QUALIFY | UNVERIFIED for Claude Code (A "§8 Nudge text"). Until it is checked, nudges go only to a confirmed prompt (C's guard), which makes this assumption unnecessary for safety. |

## Per-Point Positions

| Point | Preferred variant (A/B/C/merge) | Confidence 0-1 | One-line reason |
|---|---|---|---|
| X-001 | B | 0.75 | Waking on all nine types meets `seed-brief.md:43` literally. Keep A's limit of one sweep per S, so a heartbeat wake costs only a batch read. |
| X-002 | A | 0.9 | Never `--interrupt`. B's S6 interrupt is destructive when a screen pattern gives a false positive (`seed-brief.md:37`). |
| X-003 | A | 0.85 | Telling a worker to end its turn and then citing that turn end as stall proof empties Orca's proof class (`seed-brief.md:71`). C agrees. |
| X-004 | C | 0.7 | Stall proof is Orca's to define. Withdraw A's v2 WC-6 amendment; exhaustion goes to L5 with the person's go. |
| X-005 | A | 0.85 | The person prompt must outrank context-exhausted, so no coordinator action lands on a permission dialog (case 6). |
| X-006 | B | 0.65 | Finished work on disk makes a nudge for `worker_done` cheaper and safer than a restart path. |
| X-007 | A | 0.75 | Cases 1 and 8 show that apparent activity during a thrash misleads. No self-exit without a person or a restart; B agrees. |
| X-008 | A | 0.8 | `status` is a lifecycle message from the top-level session with no preamble-cadence conflict. C's heartbeat ack needs a preamble change (`:7`). |
| X-009 | A | 0.8 | C's 2/5/10 bounds have no v1 ack carrier, so correct reads get reported as missed. |
| X-010 | C | 0.75 | Never type into a worker whose input `ask` owns. A and B both should take C's FR-017 guard. |
| X-011 | merge | 0.65 | A's harmless text with reply id, sent only at a positively identified prompt (C), until queueing of typed input is verified. |
| X-012 | C | 0.6 | Tighter limits per lineage and per 60 min, plus A's same-cause rule, stop a case-8 loop sooner. |
| X-013 | A | 0.7 | 15 min meets the brief using the v1 5-min wait. C's 6 min needs a 1-min confirmation scheduler that v1 lacks. |
| X-014 | A | 0.8 | B's AC-1 allows 20 min against the 15-min thrashing target. |
| X-015 | A | 0.85 | B's NFR-004 "three" contradicts FR-009's per-worker stat. A's two-call claim is internally consistent. |
| X-016 | A | 0.75 | Report unverifiable at 10 min (A and C). B's 30 min leaves host loss unreported too long. |
| X-017 | merge | 0.6 | Keep the ack protocol independent of cause (A and C). Use B's ranked H1 to H4 only to guide investigation. |
| X-018 | A | 0.7 | Commands do not know they are in a chain (`:5`, WC-8), so the chain-continuity rule belongs in contract section 3. B agrees. |
| X-019 | B | 0.55 | Hooks as v2 accelerators after Orca's own evidence. A's turn-refusing Stop hook is more invasive than needed. |
| X-020 | A | 0.75 | No heartbeat while blocked in `ask` (`WORKER-CONTRACT.md:61`). C's `blocked_ask` mode needs a "send before ask" clause. |
| X-021 | A | 0.8 | C's 1-min case-4 bound relies on the v2 drain. The honest v1 bound is one 5-min cycle. |
| C-001 | merge | 0.6 | A's three orthogonal axes, with B's separate unreachable and exited states. |
| C-002 | merge | 0.65 | A's order, but with finished-unreported above context-exhausted (B). The person prompt stays above both. |
| C-003 | A | 0.75 | Context-exhausted leaves only by restart or a person (A and B). C's self-exit repeats case 1. |
| C-004 | A | 0.6 | `ironclaude.progress/1` carries step, sequence, `expect_until` and pending acks in v1. C's all-required schema suits a v2 gate. |
| C-005 | A | 0.6 | The payload is a claim that needs a second, non-contradicting source. That is safer than B's token change as primary signal. |
| C-006 | B | 0.75 | Wake on all nine with a 5-min timeout. C's 1-min type-free drain is v2. |
| C-007 | A | 0.65 | Two fleet calls per sweep, with probes only on suspicion. Fixed cost with a claim that holds. |
| C-008 | A | 0.7 | One sweep at most per S, whatever the wakes. Required once heartbeats wake the coordinator. |
| C-009 | A | 0.65 | All bounds are at most 15 min with v1 means. C's tighter figures need v2 timers. |
| C-010 | B | 0.6 | Two independent sources (old transcript plus empty prompt) beat A's flat Q plus one probe. |
| C-011 | B | 0.6 | The transcript is primary for the stall boundary and the screen only confirms; screen alone reaches S6 only on a known pattern seen twice. |
| C-012 | A | 0.6 | Trigger from flat progress or the compaction rate, confirmed by a different source. Matches C's "count alone never restarts". |
| C-013 | B | 0.6 | A v1 `stat` of the contract path is cheap and specific. It catches finished-unreported without case 3's mtime trap. |
| C-014 | A | 0.7 | Reply id in the coordinator's first line, `status` ack with a body line plus `ironclaude.ack/1` payload. Works in v1. |
| C-015 | merge | 0.65 | A's 5/10 clocks and restart-on-copy, plus C's rule never to type while `ask` owns input. |
| C-016 | C | 0.55 | A dedup key that includes `attempt_epoch` survives replacement attempts. A's reply-id rules are the v1 subset. |
| C-017 | A | 0.8 | L0 to L5 with no interrupt and positive proof for L4. B's S6 rung breaks this. |
| C-018 | A | 0.55 | Caps per episode and per Task are simple to follow by hand in v1. C's per-incident caps are similar. |
| C-019 | C | 0.6 | One per 60 min and two per lineage bounds a recurring cause harder than 2 in 6 h. |
| C-020 | A | 0.65 | A same-cause repeat forces a changed plan and the person's approval, which is broader than C's same-checkpoint test. |
| C-021 | A | 0.6 | A text resume note in the new brief works in v1 because a brief is fixed at creation (`:69`). C's JSON note is a v2 upgrade. |
| C-022 | C | 0.7 | Same as X-004. A context error alone is not an Orca stall proof. |
| C-023 | A | 0.65 | Contract section 3 by the who-knows-the-fact test (B agrees). C puts chain logic in commands, which do not know the chain. |
| C-024 | B | 0.6 | A handoff file written even on failure and listed in the artifacts. Up to 40 lines leaves room for the failed step. |
| C-025 | C | 0.55 | An 80-line limit plus a byte limit catches files with very long physical lines. |
| C-026 | A | 0.55 | One new rule (WC-14) keeps the contract compact. B's split into WC-14 and WC-15 is also acceptable. |
| C-027 | merge | 0.6 | A's amendment set, plus C's WC-7 clarification on Skill invocation. |
| C-028 | A | 0.7 | One stated test (follow text with existing verbs) and a full delivery table. |
| C-029 | merge | 0.55 | A's adapter with cost and capabilities, plus C's rule that the core never builds an Orca command or matches screen strings. |
| C-030 | B | 0.6 | Hooks only accelerate. Read Orca's evidence first. |
| C-031 | merge | 0.6 | The cause stays UNVERIFIED. The ack measures the outcome (A and C). B's hypotheses guide investigation. |
| C-032 | B | 0.6 | B adds the acked-whole-batch hypothesis and guards it with FR-012. A's FR-015 covers it implicitly. |
| C-033 | A | 0.75 | Cases 1 and 8: confirm, report to the person with a restart plan, and block a like-for-like repeat. No interrupt. |
| C-034 | A | 0.6 | One plain-text template with reply id that is harmless mid-turn. C's JSON envelope is a v2 form. |
| C-035 | A | 0.6 | Surface unknown types verbatim, with one registry row per type. Add C's bounds on raw input. |
| C-036 | A | 0.65 | Report at 10 min and never auto-restart (C agrees). |
| C-037 | C | 0.8 | Single-owner transactional ledger, persist before ack, fail closed, controller lock. v2 needs these and A lacks them. |
| C-038 | C | 0.6 | Two harness fixtures, one with no terminal, transcript or ack, plus a core without Orca dependencies. This proves portability more than A's checklist does. |
| C-039 | A | 0.5 | A has the lowest cumulative cost (at most one sweep per S, two calls each). It still needs output summarised to changed workers. |
| C-040 | A | 0.5 | A has the fewest empty waits with a 5-min timeout. Cost still UNVERIFIED. |
| C-041 | A | 0.5 | A requires the ack before acting, plus WR-7 declarations. Every ack timeout must re-derive state first, which no variant states. |
| C-042 | C | 0.55 | C states the null and absent semantics. Reliability is UNVERIFIED in all three. |
| C-043 | C | 0.65 | C states payload integrity as an UNVERIFIED v2 gate. A relies on it without saying so. |
| C-044 | C | 0.6 | C states the final-turn boundary as UNVERIFIED and requires a complete turn. |
| C-045 | C | 0.7 | C uses monotonic receipt time and tests clock jumps. |
| C-046 | C | 0.6 | C names `/sc:implement` as the only verified resume interface. |
| C-047 | C | 0.65 | Controller lock. B's R9 detection of two listeners is a v1 complement. |
| S-005 | merge | 0.55 | A's named, versioned schemas with C's byte limits and enums at the trust boundary. |
| S-006 | B | 0.7 | Separating occurrence cause from detection cause, each with a confidence, tells which fix removes and which bounds. |
| S-007 | B | 0.6 | A change table with a constraints-check column makes WC-7 and WC-8 compliance auditable. |
| S-008 | C | 0.8 | A dedicated durability and safety section. A only has a risk list. |
| S-010 | B | 0.6 | Unreachable and exited need opposite responses, so separate states. |
