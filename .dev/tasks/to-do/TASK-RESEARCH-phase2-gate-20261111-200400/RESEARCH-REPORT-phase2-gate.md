# Technical Research Report: Phase 2 gate (QUESTION-OBSERVATION) for the Orca terminal observer, issue #409

**Date:** 2026-11-11
**Depth:** Standard, scaled down (see Process note)
**Research files:** 1 codebase/live-probe file (`research/01-live-probe-log.md`) + 27 sanitized evidence files (`research/evidence/`), 0 web research
**Scope:** `.dev/issues/409/bmad/spec-orca-observer/{release-gates,owner-decisions-and-risks,unverified-register,adapter-contract}.md`, `.dev/issues/409/bmad/prd-orca-observer/prd.md`, live behaviour of `orca-ide orchestration check/send/run-*` on two throwaway Runs, two `.dev/tasks` folders.

**Process note (read first).** The `/tech-research` skill was invoked. Its full pipeline (task-builder, a /task executor and 20+ QA agents) was not run: this is a narrow, evidence-by-command question, so I did scope discovery, live probing, synthesis and assembly directly and left the independent review to one fresh-context reviewer (see Section 10). That is a reduced process and is declared as such. "Phase 2" in the brief is release R2 (question ledger) in the spec; the PRD names it R2 (`prd.md:106`).

## Table of Contents
1. Problem Statement
2. Current State Analysis (answers 1, 2 and 5)
3. Target State
4. Gap Analysis
5. External Research Findings
6. Options Analysis (decisions 8 and 6)
7. Recommendation
8. Implementation Plan (answer 4)
9. Open Questions
10. Evidence Trail
11. Owner decisions (plain English)

---

## 1. Problem Statement

- **The question:** What does the phase 2 gate (`QUESTION-OBSERVATION`) require, and does the candidate read `orca orchestration check --all --run <runId> --json` pass it? (`release-gates.md:36-48`)
- **Why it matters:** R2 (open human questions list with the 100-row disclosure and observer-side retention) is blocked by this gate, not by effort. The spec says the candidate verb is "a candidate, never an available source, until all are recorded" (`release-gates.md:38`).
- **Trigger:** R1 merged as PR #503. The coordinator asked for the gate evidence.

---

## 2. Current State Analysis

### 2.1 Answer 1: the three unproven facts, quoted, with proof or failed proof

Executable: `orca-ide` (ORCA_CLI_COMMAND unset; Linux). Probe Runs: **Run A `run_c1badaa6576b`**, **Run B `run_14cfcbd8edf2`**, both created by me on 2026-11-11 (first call 20:00:47Z). All results below come from those two Runs only.

#### Fact (a)

Gate text (`release-gates.md:40`): "**Proof (a), UNVERIFIED:** `--run` narrows `--all`, shown with samples from at least 2 Runs."

**Result: FAILED as worded. `--run` does not narrow anything; it is a check that the caller is already bound to that Run.**

| Step | Command | Observed (sanitized) | File |
|---|---|---|---|
| 1 | caller bound to B: `orca-ide orchestration check --all --run run_c1badaa6576b --json` | `{"ok":false,"error":{"code":"consumer_fenced","message":"This caller is bound to Run run_14cfcbd8edf2, not Run run_c1badaa6576b. Nothing changed."}}` | evidence/01, 02 |
| 2 | bound to B: `check --all --run run_14cfcbd8edf2 --json` | `ok`, 2 messages, `runId` B | evidence/03 |
| 3 | bound to B: `check --all --json` (no `--run`) | same rows as step 2 | evidence/04 |
| 4 | after `run-use --id run_c1badaa6576b`: `check --all --run run_c1badaa6576b --json` | `ok`, 2 messages (`probe A status`, `probe A question`), `runId` A | evidence/23 |
| 5 | bound to A: `check --all --run run_14cfcbd8edf2 --json` | `consumer_fenced` | transcript (L-10) |

Samples from 2 Runs exist (A: 2 rows, B: 2 rows), and no row from the other Run ever appears. So the scope of the read is "the Run the caller is bound to". That is the fact the observer needs, but it is a different fact from the one the gate states. Date of test: 2026-11-11.

#### Fact (b)

Gate text (`release-gates.md:41`): "**Proof (b), UNVERIFIED:** which handle receives human-addressed messages, and whether the read works from an unbound observer terminal."

**Result: PARTLY PROVEN. A caller with no terminal identity at all fails; a terminal that has a handle but is bound to no Run is UNTESTED; the "human" half has no Orca field.**

| Question | Evidence |
|---|---|
| Which handle receives messages? | A message sent `--to run:<id>` is stored with `to_handle` `run:<id>`. A message sent to a terminal handle while that terminal is bound is rewritten to `to_handle` `run:<bound Run>` (probe: sent to my own terminal handle, stored as `run:run_14cfcbd8edf2`, `run_id` B). So messages land in the **Run mailbox**, read through the Run's bound consumer. (transcript L-5; row shape evidence/03) |
| Any "human" recipient? | No. `send --help` lists the types `status, dispatch, worker_done, merge_ready, escalation, handoff, decision_gate, question, heartbeat` and recipients `run:`, `dispatch:`, a legacy terminal handle or a group. There is no human handle. A `question` row is addressed to the Run (its coordinator, an agent), so "human question" is not something Orca records. |
| Unbound observer (no terminal identity) | `env -u ORCA_TERMINAL_HANDLE ... check --all --run <A or B>` and with no `--run`: `{"ok":false,"error":{"code":"no_active_terminal"}}` (evidence/17, 18, 19). Fails, but this only shows that a caller with no terminal identity cannot read; it is not the "observer terminal with no bound Run" case. |
| Terminal that has a handle but is bound to no Run | **UNVERIFIED.** I could not make one: my terminal was bound to the coordinator-created dispatch state and then to my probe Runs. A fresh plain terminal is needed (Section 9, Q-1). |
| Reader bound to a different Run | `consumer_fenced`, "Nothing changed" (step 1 above). |
| Taking over a Run | `run-use` is the only way found to bind to a Run you do not already hold. It changed `consumer_generation` (A: 1 to 5, B: 1 to 3 over my rebinds) and `coordinator_handle` of A was `null` while I was bound elsewhere (transcript L-11). In my probes the same terminal was already the coordinator of both Runs, so this shows only that binding rewrites the Run's coordinator fields. Whether a `run-use` on the live Run would displace or block the real coordinator is **UNVERIFIED** (needs two terminals; not tested because it would touch a Run I did not create). |
| Cross-Run send from a worker | Blocked: `dispatch_run_mismatch` (my terminal is an active Dispatch of the coordinator's Run). |

#### Fact (c)

Gate text (`release-gates.md:42`): "**Proof (c), UNVERIFIED:** measured message rate, recorded. A measured rate does not prove completeness, so the label stays 'bounded best effort; coverage unknown; bursts over 100 rows between reads may be lost' after the gate."

**Result: the real message rate is UNVERIFIED and I did not measure it** (it needs a read of a real Run, which the brief forbids and decision 6 has not granted). What I measured on my own Run is the shape of the 100-row bound and the cost of a call:

| Measurement (Run B, 104 messages) | Result | File |
|---|---|---|
| `check --all` rows | exactly 100, **newest first**; the 4 oldest are silently missing; no `total`, `hasMore` or truncation field | evidence/14 |
| `check --peek` rows | exactly 100, **oldest first**; newer unread rows are silently missing | evidence/15 |
| Read latency | `--all` 0.197, 0.199, 0.200 s; `--peek` 0.189, 0.197, 0.195 s (3 runs each, 104-message Run) | evidence/16 |
| Send latency | 0.201 s | evidence/16 |

So the label "bursts over 100 rows between reads may be lost" is correct for `--all` (the oldest are lost) and the observer cannot detect the loss from the response, since `count` equals 100 whether there are 100 or 10,000 rows.

### 2.2 Answer 2: the non-consumption test

Question: does `check --all --run <runId> --json` leave messages unread and unacknowledged? **Yes, for every visible effect I tested, on Run B where I am the real owner.** Quiet scope: no other sender wrote to B during the sequence. Identity fields were established first: each row has `id` (`msg_...`), `run_id`, `from_handle`, `to_handle`, `subject`, `body`, `type`, `priority`, `thread_id`, `payload`, `created_at`, `delivered_at` (evidence/03). The `inbox` rows add `read`, `sequence` (evidence/20).

| Step | Command | Result | File |
|---|---|---|---|
| 1 | `check --all --run B` | 2 rows | evidence/03 |
| 2 | second read of the same Run (the no-`--run` form, which resolves to the bound Run) | same rows, same `delivered_at` null; differs only by envelope id | evidence/03 vs 04 |
| 3 | `check --peek --run B` | 2 rows (unread), no `deliveryId` | evidence/05 |
| 4 | `check --all --run B` again | 2 rows | evidence/06 |
| 5 | **consuming** `check --run B` (the real owner) | receives **both** messages, `deliveryId` `delivery_657cbe0e1ebb` | evidence/07 |
| 6 | `check --all` and `--peek` before ack | still 2 rows each (the help says a delivery is replayed until acked; the rows themselves were unchanged) | evidence/08, 09 |
| 7 | `check --run B --ack delivery_657cbe0e1ebb` | `acknowledged` set, `count` 0 | evidence/10 |
| 8 | `check --all` after ack | still 2 rows, `delivered_at` still `null`, no read flag | evidence/11 |
| 9 | `check --peek` after ack | `count` 0 | evidence/12 |

Conclusions, limited to what was seen: the `--all` and `--peek` reads did not consume (steps 1-5); the later consuming `check` by the owner still received everything. A pass covers only these visible effects (T51 wording, `acceptance-tests.md:57`). **Two things the test also revealed that matter for the observer:** (1) `--all` rows carry no read or acknowledged marker, so a question that the coordinator has already handled looks the same as a fresh one (steps 8 vs 9); (2) `--peek` hides rows once the coordinator has read and acked them (step 9), so it cannot be the stable source. **Limit:** this was tested as the Run's owner with a pre-bound terminal; consumption by an observer that is not the owner is UNVERIFIED (Q-1).

### 2.3 Answer 5: is `TASK-WF-buildRelease1OfT-20261110-045742` abandoned or live?

**Abandoned (superseded), not live.** Evidence:

| Check | Result |
|---|---|
| Contents of `.dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/` | only `return-contract.yaml` (640 bytes). Its `plan_path` names `./TASK-WF-buildRelease1OfT-20261110-045742.md`, which does not exist in the folder or in `HEAD`. No `progress.md`, no `source.md`. |
| Later attempt | `.dev/tasks/done/TASK-WF-buildRelease1OfT-20261111-164757/` has the plan (53 KB), `progress.md` ledger with T1-T11 `complete verdict=compliant` lines, `source.md`, `artifacts/`; it is the run that produced R1. Its `source.md` quotes the owner's "Proceed with building the first release" of 2026-11-11. |
| Git | both folders were committed by `9e2608b03` (PR #503, 2026-11-11). Nothing newer touches the old one. |
| Reflect report named by the old contract | `.dev/reflect/pre-buildRelease1OfT-20261110050109/REPORT.md` does not exist (the folder is untracked per the session's git status). |

I cannot prove the author's intent; it is an inferred reading from a missing plan, no ledger and a complete successor. Report only: I did not move or delete anything. (Do not move by hand: the repo rule says archive moves are done by the executor.)

---

## 3. Target State

- **Desired behaviour:** a gate record that says exactly which parts of the candidate read are proven, so R2 can build on them or the owner can re-confirm the direction (fallback rule, `release-gates.md:48`).
- **Success criteria:** each of (a), (b), (c), non-consumption, question identity, decisions 8 and 6, and the call budget has a recorded verdict.
- **Constraints:** no consuming read on a Run I did not create; owner keeps decisions 8 and 6; unproven items stay UNVERIFIED and drive no recommendation.

---

## 4. Gap Analysis

| Gap | Current State | Target State | Severity | Notes |
|---|---|---|---|---|
| G-1 Proof (a) as worded is false | `--run` is a fence, not a filter | gate wording matches real behaviour | Critical | Section 2.1; changes the adapter design |
| G-2 Observer cannot read an arbitrary Run (as tested) | no terminal identity: `no_active_terminal`; terminal bound to another Run: `consumer_fenced`; terminal with a handle and no Run: UNTESTED; `run-use` rewrites the Run's coordinator fields (effect on a real coordinator UNVERIFIED) | a read path that is proven not to displace a coordinator | Important | treat `run-use` as forbidden for the observer until Q-1 and Q-2 are answered and the owner decides |
| G-3 Real message rate | not measured | measured on a permitted sample | Important | UNVERIFIED; needs decision 6 |
| G-4 Closure evidence | `--all` rows have no read flag | explicit resolution marker | Important | `inbox` has `read` and `sequence` but its scope is unproven |
| G-5 100-row loss undetectable | no total/truncation field | disclosure only | Minor | already planned (`prd.md:250`) |
| G-6 Human-ness of a question | no Orca field | owner decision 8 | Important | Section 6.1 |
| G-7 Acquisition permission | not granted | owner decision 6 | Important | Section 6.2 |
| G-8 Question identity | `message.id` (`msg_...`) is unique in probes | verified on real traffic | Important | UNVERIFIED on real data; a worker `dispatchId` must still never be used |
| G-9 Unbound terminal that has a handle | not testable from my terminal | one test from a fresh plain terminal | Important | Q-1 |

---

## 5. External Research Findings

None. This is a behaviour probe of the local Orca CLI. Help text read: `orca-ide orchestration check|send|ask|run-create|inbox|reset|worker-list --help` (Orca 1.4.245-aidev02.9cfecdd30b2a). One help-text finding: `worker-list` accepts `--terminal-state <active|reclaimable|retained|release_pending|release_unknown|released>`, while `unverified-register.md:42` lists a state filter as UNVERIFIED. Not run against live data, so it stays UNVERIFIED as a behaviour.

---

## 6. Options Analysis

I do not settle these. They belong to the owner.

### 6.1 Decision 8: what identifies a human question

**What the spec says** (`owner-decisions-and-risks.md:24`): "**Question-type choices.** What makes a message a 'human question', which `type` values count, which handle or Run carries it. Needs the owner or Orca. Recommend an explicit message type, never text inference."

| Option | What the observer would do | Evidence for/against |
|---|---|---|
| 8-A. Explicit type: rows with `type` = `question` | Reads `check --all --types question`; lists each as "question to the coordinator". Label says "coordinator questions", not "human". | `--types question` filters server-side (evidence/24); `question` is a valid `send` type. Weak point: Orca never says the question is for a human; the coordinator agent may answer it itself. Whether `ask` writes this type is UNVERIFIED. |
| 8-B. Type plus a convention in `payload`/`priority` (a marker meaning "needs a human") | Lists only marked rows. | No such convention exists; it would need Orca or the coordinator skill to start writing it. UNVERIFIED. |
| 8-C. Infer from text | Guess from subject/body. | Rejected by the spec recommendation and invents a contract. |
| 8-D. Defer | No question list; keep the R1 notice. | Safe; leaves R2 blocked. |

**Recommendation: 8-A**, labelled "questions sent to the coordinator (not confirmed to need a human)". It matches the spec's own recommendation, and it is the only option backed by observed data.

### 6.2 Decision 6: permission to read that scope

**What the spec says** (`owner-decisions-and-risks.md:22`): "**Sample capture and acquisition permission.** Permission to capture one non-empty redacted sample from the candidate `check --all` read; acquisition permission must cover the actual read scope before any message call, separate from display and export. Recommend yes, owner sets redaction rules. Unblocks B's headline panel."

**What "the actual read scope" turned out to be:** the whole mailbox of one bound Run (every sender, every type, full bodies) unless narrowed by `--types`. Bodies of all matching rows enter the observer process. In every case I tested the read needed a terminal bound to that Run; an unbound terminal that has a handle is UNTESTED (Section 2.1(b), Q-1).

| Option | What the observer would do | Cost / risk |
|---|---|---|
| 6-A. Grant one sample, narrowed: `check --all --types question` on the Run the owner names, run from a terminal that already holds that Run (no `run-use`), one non-empty redacted sample, owner sets redaction rules | Proves real row shape, identity and a real rate sample for one Run. | Reads question bodies of that Run into the process. No seat takeover. |
| 6-B. Grant a broad read of the Run mailbox (`--all`, no `--types`) | Also shows status/worker_done rows; useful for closure evidence. | Acquires all bodies; bigger than R2 needs. |
| 6-C. Grant only probe Runs (what this report did) | Nothing further to prove. | Cannot prove (c) or identity on real traffic. |
| 6-D. Deny / defer | No live message read. | R2 stays blocked; owner re-confirms direction at the fallback date (`release-gates.md:48`). |

**Recommendation: 6-A.** It is the narrowest read that can clear the open proofs. It must also say plainly that the observer never runs `run-use` on a Run it does not own.

---

## 7. Recommendation

1. Record the gate result as **not passed**: (a) failed as worded, (b) partly proven (messages land in the Run mailbox; a caller with no terminal identity cannot read; an unbound terminal with a handle is untested), (c) unmeasured, non-consumption passed on a probe Run as the Run's owner, identity candidate `message.id` seen on probes only. Call budget: 1 message call per cycle is consistent with the measured 0.2 s per call on a probe Run (real traffic UNVERIFIED).
2. Do not build R2 against the candidate as written. First rewrite proof (a) and the read path (Section 8, items 1-3).
3. Put the two decisions (8 then 6) to the owner, one at a time (Section 11). Recommended answers: 8-A and 6-A.

---

## 8. Implementation Plan (answer 4: what changes in phase 2's design, and what the plan must contain)

**Does anything change?** Yes, three things.

1. **The read is per bound Run, not a fleet read.** Observed: a terminal bound to one Run is fenced from every other Run (`consumer_fenced`). The adapter-contract "Rotation set" (`adapter-contract.md:57`: permissioned scopes, rotation across Runs with `revisit ~Ns`) therefore has no proven way to work: the only route found to another Run is `run-use`, whose effect on a real coordinator is UNVERIFIED (Q-2), and the unbound-terminal route is untested (Q-1). Until those are answered, plan R2 as **one Run only**; the rotation set is not to be built. The header text `read k of N Runs since start` (`adapter-contract.md:64`) loses its meaning for messages.
2. **The observer needs a caller identity that already holds the Run.** Options for the plan to evaluate: run the observer from the terminal that holds the Run (inherits the binding); never `run-use`. UNVERIFIED which of these works for a separate pane.
3. **The argv template changes.** Add `check --all --types question --run <runId> --json` as the only message template (argv list, separate arguments). Add to the forbidden set (`adapter-contract.md:17`): `run-use`, `run-create`, `send`, `ask`, `reply`, `reset`. Keep `inbox` forbidden (scope unproven).

What does **not** change: the 100-row window disclosure and observer-side retention (confirmed needed: `--all` loses the oldest silently), the "seen is not resolved" rule (confirmed: no read flag in `--all`), 1 message call per cycle (a call is about 0.2 s, well inside the 5-call cap), the label "bounded best effort; coverage unknown".

**What the phase 2 plan (input for a later `/sc:workflow`, not run) must contain:**

| Step | Action | Files / commands | Details |
|---|---|---|---|
| 8.1 | Rewrite the gate text | `release-gates.md`, `unverified-register.md`, `prd.md:106` | Replace proof (a) with "the read returns only the bound Run's mailbox; another Run is fenced". Record (b), (c), non-consumption results from this report. |
| 8.2 | Owner decisions 8 and 6 recorded | `owner-decisions-20261108.md` (owner writes) | Plain-English choice, date, decider. |
| 8.3 | Fresh-terminal test Q-1 | from a plain Orca terminal: `orca-ide orchestration check --all --run <probe Run A>` | Proves or fails "terminal with a handle but no Run". Probe Runs only. |
| 8.4 | One permitted real sample | owner-named Run, `--types question`, redacted | Gives real rate and identity check. Needs 6-A. |
| 8.5 | Adapter | `src/superclaude/cli/observe/adapter.py` (allow-list), `parse.py` (message row parser) | New template, forbidden set additions, parse by field with `UNKNOWN` sentinel; identity = Run-scoped `message.id`. |
| 8.6 | Retention | `view.py` | 1,000-record bound; oldest lost from the 100-row window disclosed. |
| 8.7 | Tests | `tests/observe/` | Fake-runner tests for the new argv, `consumer_fenced` and `no_active_terminal` responses, 100-row cap fixture, T51 quiet-scope test using the probe shapes. Recorded redacted samples of success, missing, stale, contradictory (data-gate rule, `release-gates.md:5`). |
| 8.8 | Disclosure text | rendering | "one Run only", "coordinator questions", "bounded best effort; coverage unknown; bursts over 100 rows between reads may be lost". |

Integration checklist: gate text rewritten; both decisions recorded; Q-1 run; sample captured (or R2 deferred and the owner re-confirms A at the fallback date).

---

## 9. Open Questions

| # | Question | Impact | Suggested Resolution |
|---|---|---|---|
| Q-1 | Can a terminal that has a handle but no bound Run run `check --all --run <Run>`? Does `--all` ever consume when the reader is not the owner? | Decides whether an observer pane can work without `run-use` | One test from a fresh plain terminal against probe Run A (`run_c1badaa6576b`) |
| Q-2 | Does `run-use` on a live Run stop the real coordinator from reading? | Decides how dangerous binding is | Needs two terminals and a probe Run; do not test on the live Run |
| Q-3 | Does `ask` write `type: question`? | Decides whether 8-A sees `ask` questions | Test from a coordinator-held probe Run (my worker dispatch cannot) |
| Q-4 | Does `inbox` reach across Runs? Its rows add `read` and `sequence` | Could supply closure evidence | Test with a quiet probe setup; counts only |
| Q-5 | Real message rate | Disclosure budget | Needs decision 6 |
| Q-6 | Does `worker-list --terminal-state active` work as the help says? | Settles INV-007 | Separate read-only test |

---

## 10. Evidence Trail

### Research and evidence
| File | Topic |
|---|---|
| `research/01-live-probe-log.md` | Command log L-1 to L-13, non-consumption steps N1-N9, cap and timing, cleanup |
| `research/evidence/01..27` | Sanitized raw outputs (01-02 fenced read, 03-04 all reads, 05-12 non-consumption, 13-16 cap and timing, 17-19 unbound, 20 inbox rows, 21 ask, 22-25 rebinding and `--types`, 26-27 run-create) |

Note: "transcript (L-n)" means the command output was seen in the session and is recorded in the L-table of the log; it was not saved as its own file. The review (`reviews/review-1.md`) found the evidence sound and two wording overclaims, which are corrected above (the "takes the seat" and "unbound half FAILED" statements).

### Spec files read
`release-gates.md`, `owner-decisions-and-risks.md`, `unverified-register.md`, `adapter-contract.md`, `acceptance-tests.md` (T51), `prd.md` (lines 97-116, 243-250), `.dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/return-contract.yaml`, `.dev/tasks/done/TASK-WF-buildRelease1OfT-20261111-164757/{return-contract.yaml,progress.md,source.md}`.

### Throwaway Runs left behind (no delete verb exists; `reset` not run)
`run_c1badaa6576b` (Run A, 2 messages) and `run_14cfcbd8edf2` (Run B, about 105 messages). My terminal is still bound to Run A. Also, sends to `run_93bfa00cae2b` were only the required heartbeats.

### Safety record
No `check`, `check --all`, `--peek`, `--ack`, `run-use`, `reset` or `ask` was run against `run_93bfa00cae2b` or any Run I did not create. `inbox --limit 100` was run once; only per-Run row counts and shape were kept (all 100 rows were Run B), so nothing from another Run was recorded. No credentials were printed or stored.

### Review
Independent fresh-context review: see `reviews/` (written after this report; result summarized in the final message).

---

## 11. Owner decisions (plain English, one at a time)

You do not need to settle these to read the report. They are the two decisions the gate names. I recommend an answer for each; I have not recorded either as decided.

### Decision 8: what counts as a "human question"?

Orca has no "human" label. It has a message type called `question`, sent to a Run's mailbox, which is read by the coordinator (an agent). The observer can list those. It cannot tell whether a person needs to answer.

- **Option A (recommended):** show every `question` message and call the list "questions sent to the coordinator". Example: a worker sends `--type question "Which branch?"`, and it appears.
- **Option B:** wait until Orca or the coordinator marks messages that truly need a person. Nothing does today.
- **Option C:** guess from the message text. Not recommended; it invents a rule Orca does not have.
- **Option D:** show no question list yet.

Which do you choose?

### Decision 6: may the observer read that mailbox?

The read returns the full text of every message in one Run's mailbox. In every case I tested it only worked from a terminal that already holds that Run. The only route I found to a different Run is to bind to it, and I could not test whether that would displace the real coordinator, so I recommend the observer never do that.

- **Option A (recommended):** you name one Run; the observer reads only `question` messages from it, once, from a terminal that already holds it; you set what is redacted.
- **Option B:** allow the whole mailbox, all message types.
- **Option C:** probe Runs only (done; it cannot show real traffic).
- **Option D:** no live read; R2 stays blocked until the fallback date.

Which do you choose?
