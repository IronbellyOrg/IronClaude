# Requirements specification, variant 4 (devops lens): reviewers that collaborate during the run on the tasklist review panel

Path abbreviations used throughout:

- `EVAL` = `.dev/eval-workspaces/tasklist-review-panel/20261111-a1`
- `BS` = `.dev/brainstorms/20261113-163248-panel-collaboration`
- `CR` = `EVAL/COMBO-REPORT.md`
- `HO2` = `.dev/eval-workspaces/tasklist-review-panel/HANDOFF-review-panel-unification-run2.md`

Issue labels follow `CR:401-417`. The study's "found /14" metric covers only the two defect-rich packages: B1-B5 and I1-I5 (designSpec), plus B6-B8 and I6 (alias). I7 and I8 belong to the control package and are reported as "control /2". So in this specification, gains on I7 are always reported separately from gains out of 14.

Devops framing: each redesign is treated as a change shipped to a running service, and each gets the following:

- **Elapsed-time target.** Panel elapsed time per package must stay at or below 1.35 times its isolated baseline.
- **Kill switch.** One setting turns collaboration off and restores the isolated panel unchanged.
- **Audit trail.** Every message exchanged is logged, so the exchange can be checked afterwards.
- **Alarms.** Each design has named alarms.
- **Runbook entries.** Each failure mode has an entry saying how it is detected and what to do.

---

## 1. Theories

All three theories from the seed brief are accepted, and each is refined against the evidence. The refinements matter for design. T1 is about **what the reviewer searches for**, not how much it searches. T2 is about **which question is asked at the right place**, not how much the model thinks. T3 is a **harness confound**: collaboration cannot remove it, so every gain estimate below has to be separated from it.

### T1 (refined). Searches stay inside the files the plan names

Cheap models check the files and lines the plan names. They never search outward from those files: no reverse-dependency sweep ("which tests and docs reference the files this plan edits?") and no inventory sweep ("the plan says *all*/*only*: list what it covers and count the exceptions").

| Evidence | Number | Source |
|---|---|---|
| Unnamed files touched per run | sonnet 3.1, grok 1.2, haiku 0.9, ember 0.8, luna 0.3 | `BS/enrichment/investigation-patterns.md:41-49` |
| Runs that touched a test file the plan does not name | sonnet 35%, grok 33%, ember 8%, luna 1%, haiku 0% | same |
| `tests/skills/test_worker_contract.py` opened on the control package | 0 of 176 ember/luna/haiku runs; 7 of the 8 runs that opened it found I7, against 0 of the 225 that did not | `investigation-patterns.md:43-46, :132` |
| Search volume is not the variable | haiku searches `tests/` in 81% of runs (5.2 recursive searches per run), yet in 5 of 11 cheap control runs `test_worker_contract.py` showed up in its grep output and it never opened the file | `investigation-patterns.md:55`; `investigation-alias-control.md:66` |
| CHANGELOG never reached | `CHANGELOG.md` touched by 1 of 233 designSpec runs; I5 never found | `investigation-patterns.md:134` |
| Universal claim never counted | 44 of 98 cheap alias reviewers saw the already-narrowed `refs/tiers.md:42` and none compared it with Task 7's "all other primitives" (B8) | `investigation-alias-control.md:67` |

Explains I7, I5, B8 and B6 (primarily) and supports I6.

### T2 (refined). The reviewer anchors the right place but checks it along one axis only

Cheap reviewers anchor the right sentence, ask one local question about it, and stop. The refinement is that this is **not a thinking-budget ceiling**. Within ember and luna, hard-issue hits do not rise between the lower-thinking and higher-thinking halves of runs: ember goes from 0.25 to 0.22 per run and luna stays at 0.09. For haiku the same comparison does rise, from 0.29 to 0.70 (`investigation-patterns.md:149-151`). A second axis has to be asked for explicitly.

| Evidence | Number | Source |
|---|---|---|
| Right anchor, inverted question on I5 | 16 cheap findings anchor the I5 sentence; all 16 say the grep over-matches; none asks where else the claim lives | `investigation-designspec.md:103` |
| One branch traced on B5 | 3 cheap findings on the exact B5 mapping; all traced only the mode-off case, none the halt path | `investigation-designspec.md:105` |
| One question asked on I1 | 1 haiku finding on the exact I1 row, asking a different question | `investigation-designspec.md:106` |
| Stopping rule never tested (B1, B2) | ember anchors Task 1 of designSpec in 52% of runs, yet the unbounded-inventory issue is matched in about 3%; no finding in any panel anchors O3/AC3 | `investigation-patterns.md:111, :140`; `investigation-designspec.md:104` |
| AC grep never read literally (I4) | 0 cheap findings; only sonnet, in 4 of 26 runs | `investigation-designspec.md:107, :124` |
| Check stops after one task (I6) | cheap reviewers found the sibling defect B7 (Task 6 against the Constraint) and never repeated the check on Task 7 or Task 3 | `investigation-alias-control.md:69` |
| Wrong framing of the right observation (B6) | luna read the `chains.md` `/model` lines and graded them "unclear exemption"; credit depended on framing them as "goal against test scope" | `investigation-alias-control.md:102` |

Explains B1, B2, B5, I1, I4, I6 (primarily) and supports I5 and B6.

### T3 (refined). The evidence environment and the reporting filters hide or drop defects (a harness confound)

Two parts: the reviewer **cannot see** the defect, or it **sees it and the pipeline drops it**. This theory describes the harness, not the models, so a gain from fixing it must never be credited to collaboration.

| Part | Evidence | Number | Source |
|---|---|---|---|
| (a) Cannot see | The sandbox is a checkout taken after implementation, with the repairs already present: `refs/merge-guard.md:146` (B5), `merge_guard.py:256` (I1), `pr-submit.md:81` (I4), `refs/tiers.md:42` (B8) | 4 of the 9 target issues masked for plan-vs-code checks | `investigation-designspec.md:14-20`; `investigation-alias-control.md:9` |
| (a) | source.md is not named in the brief | 156 of 665 runs never referenced it; 14 of 39 ember designSpec reports never opened it | `CR:373`; `investigation-designspec.md:73` |
| (b) Seen and dropped | A missing requirement is graded Medium and the brief has no missing-task category | all 7 true I7 findings non-blocking; grok saw `CHANGELOG.md:166` and dropped it as "minor" | `investigation-patterns.md:132, :161`; `investigation-designspec.md:126` |
| (b) | luna reports almost only blocker-grade findings | 1.75 findings per run, 72% blocking | `investigation-patterns.md:64` |
| (b) | The merge drops long anchors and claims | 49 blocking findings lost (luna 30, ember 33 cases) | `CR:292`; `HO2:162` |
| Leak (inflates rather than hides) | The sandbox holds `.dev/reflect/pre-design-20261108041729/REPORT.md`, which names I7 | 2 of the 9 I7 credits came after reading it | `investigation-alias-control.md:125` |

Explains B5, I1, I4 and B8 (masking), I5 and I7 (filtering). It is a confound for every measured number.

### Mapping of the ten missed issues to the theories

| Issue | Primary theory | Secondary | Generic move that finds it (catalogue id, section 2.0) |
|---|---|---|---|
| B1 (designSpec Task 1 AC3, unbounded "every") | T2 | T3b (rubric steers toward wrong builds) | M3 stopping rule |
| B2 (designSpec Task 1 scope against AC) | T2 | T3a (source.md skipped) | M9 scope compare |
| B5 (designSpec exit-report mapping after halts) | T2 | T3a (repaired ref) | M5 branch trace |
| B6 (alias aliases-only goal against test scope) | T1 | T2 (framing) | M10 claim against enforcing test |
| B8 (alias "all other primitives use aliases") | T1 | T3a (repaired tiers.md) | M2 universal-claim count |
| I1 (designSpec fold rows against the status mapping) | T2 | T3a (repaired code) | M6 producer/consumer against source.md |
| I4 (designSpec heading against case-sensitive grep) | T2 | T3a (repaired heading passes) | M4 literal AC check |
| I5 (designSpec stale "43 members" in CHANGELOG) | T1 | T2, T3b (dropped as minor) | M7 other-direction sweep |
| I6 (alias user-guide text drops a constraint clause) | T2 | none | M8 constraint sweep across tasks |
| I7 (control: worker-contract test never updated) | T1 | T3b (missing task = Medium), leak | M1 reverse-dependency sweep |

---

## 2. Five redesigns

### 2.0 Shared building blocks (used by several designs)

**Move catalogue (frozen, generic).** These ten investigative moves come from the "needed move" columns of both missed-issue investigations, reworded so that none names a package, task number, file from ground truth, or ground-truth quote. They are the only instruction text a message may carry.

| Id | Move (text sent to a reviewer) | Style that runs it best |
|---|---|---|
| M1 | For each file the plan edits, search `tests/`, `docs/` and the repo root for its path or key strings; open every test file the plan never names. | search (ember, haiku, sonnet) |
| M2 | For each sentence that says all, only, every or none, list what it quantifies over and count the exceptions. | search |
| M3 | For each acceptance criterion that says every, all or complete, state the finite check that proves it; if none exists, say so. | reading (luna, haiku) |
| M4 | For each grep or command criterion, run it against the exact text the task tells the implementer to write, not the current file. | either |
| M5 | For each mapping or decision rule, trace every input value (each reason, each mode) through to its output. | reading |
| M6 | For each value a consumer reads, find the producer row that writes it, in the source document, not the checkout. | reading |
| M7 | When you checked a claim is not too broad, check the other direction: where else in the repository (root files included) is the same claim stated? | search |
| M8 | When a check fails for one task, apply the same check, clause by clause, to every other task. | reading |
| M9 | Compare each task body's scope with its acceptance criterion's scope and with the source document's scope. | reading |
| M10 | When the plan says a test enforces a rule, list what that test can actually fail on. | either |

**Message schema `panel-msg/1`.** One JSON object per line. Serialised size is at most 600 bytes, and the reader rejects longer lines.

```json
{"v":"panel-msg/1","id":"m-r2-03","run":"<row>/<pkg>","from":"t4-1","to":"t3-1|*","t":1731500000123,
 "kind":"move|fact|challenge|card|coverage","move":"M1",
 "anchor":"<optional: 12-200 chars copied exactly from candidate.md>",
 "items":["<optional: up to 8 repo paths or path:line>"],"n":0}
```

The fields `claim`, `severity`, `blocking`, `category` and free text are **forbidden**, and the validator drops any line that contains them. A message can therefore point (move, anchor, paths, count) but cannot conclude.

**Board substrate (the transport for designs 1, 2, 4 and 5).**

- **Location.** The harness creates `$BOARD/<row>/<pkg>/` outside the sandbox repo.
- **Writing.** Each reviewer writes only through two Bash helpers on `PATH`: `panel-post` (appends one validated line to `msgs/<rid>.jsonl`) and `panel-seal` (copies the reviewer's current draft findings lines to `sealed/<rid>.jsonl`).
- **Reading.** A `PostToolUse` hook prints new peer lines as `additionalContext`, capped at 1,500 characters per call. A `Stop` hook does a final check and can **hold**: it polls the board for up to H seconds, then returns `decision: block` with the new messages, or allows the stop.
- **Configuration.** Hooks are passed per reviewer with `--settings '<json>'`. The absolute board path and the reviewer id are written into the hook command string, so nothing depends on environment-variable inheritance, which is UNVERIFIED (`BS/enrichment/research-light.md:205-207`).
- **Why the board was chosen.** It delivers the same way for every model because delivery happens on the CLI side, not by the model calling a tool. It is durable, it is its own audit log, and it needs about 100 lines of bash (`research-light.md:157-207`).

**Transports rejected for every design.**

| Transport | Why rejected |
|---|---|
| Orca mail | No per-reviewer mailbox for bash-launched `claude -p`; would need a `worker-start` rewrite. |
| A2A | No way to inject into a running turn; needs a server per reviewer. |
| Claude Code cross-session messaging | No durable audit file. Whether gateway models call `SendMessage` correctly is unverified. Behaviour after a `-p` session's last turn is unverified. `ListAgents` shows every session on the host (`research-light.md:115-123`). |

Cross-session messaging stays a spike-gated fallback for design 4 only.

**Reviewers stay read-only.** `--disallowedTools Edit Write NotebookEdit` is unchanged. The two helpers write only under `$BOARD`, outside `/tmp/evalsb/repo` and outside the candidate.

**Kill switch.** With `PANEL_COLLAB=0`, the harness passes no hooks, no helpers and no phase 2, which reproduces today's `EVAL/tools/run-reviewer.sh` exactly.

**Timing constants.** Median wall time divided by median turns gives the time per turn:

| Model | Median wall | Median turns | Seconds per turn |
|---|---|---|---|
| ember | 41 s | 13 | 3.2 |
| luna | 102 s | 16 | 6.4 |
| haiku | 233 s | 10 | 23 |
| sonnet | 228 s | 16 | 14 |

Source: `investigation-patterns.md:19-23`. One move costs about 2 turns. A fresh or resumed `claude -p` start costs about 6 s (UNVERIFIED; measured in spike S0).

**Baseline elapsed time per package** (CR elapsed over 3 packages divided by 3):

| Baseline panel | Set | Elapsed per package | +35% cap | Output tokens per package |
|---|---|---|---|---|
| ember + 2x luna | S07 | 116 s | 157 s | 21.2k |
| ember + luna | S13 | 100 s | 135 s | 17.5k |
| ember + luna + sonnet | S14 | 225 s | 304 s | 46.2k |
| haiku + 2x luna | S24 | 238 s | 322 s | 63.7k |

Source: `CR:317, :319, :320, :331`.

**Harness-fix share (H), common to all designs.** Four fixes:

- (H1) name source.md in the brief;
- (H2) validate each report with the real parser at run time and re-ask once when lines would be dropped, which fixes the anchor limit without changing findings-v1;
- (H3) review each package in a checkout of the commit the plan was written against;
- (H4) remove `.dev/reflect/` from the sandbox.

Estimated H share, out of 14 per run:

| Panel | Estimated H share |
|---|---|
| ember + 2x luna | +0.2 to +0.6 |
| ember + luna | +0.2 to +0.5 |
| sonnet panels | +0.1 to +0.4 |

Basis for the estimate:

- AUDIT-CLEAN minus AS-SCORED: +0.09 for S07 and +0.3 for S24 (`CR:331, :355, :319, :347`).
- In ember + 2x luna, ember skipped source.md in 9 of 18 runs and luna in 9 of 36 (`CR:382`).
- H3 unmasks the plan-vs-code route to 4 of the 9 target issues.

H4 changes nothing for cheap panels, which never found I7. For sonnet panels it can lower measured I7 by up to 2 in 9 credits. Every collaboration estimate below **assumes H is applied in both arms**. Moves M4 and M6 only pay off once H1 and H3 hold.

---

### Redesign 1: Move Radar (coverage gaps from tool-call telemetry; reviewers author no messages)

**(a) Mechanism.** A `PostToolUse` hook in every reviewer logs each tool call (tool name plus command or path) to the board. A deterministic classifier (jq and regex) maps tool calls to catalogue moves:

- `grep -r…` over `tests/` with a plan-edited path counts as M1.
- A Read of source.md counts as "source opened".
- A Read of a test file that is not in the candidate's file list counts as "unnamed test opened".
- A repo-wide search that includes root files counts as M7.

At fixed checkpoints the hook injects into each reviewer **one move that no panel member has done yet**, chosen by that reviewer's style:

| Reviewer | Moves it receives | Reason |
|---|---|---|
| ember (sweeper) | search moves: M1, M2, M7, M4 | ember greps (3.7 recursive searches per run) |
| luna x2 (readers) | reading moves: M3, M5, M6, M9, M8, M10, plus "open source.md" if not yet opened | luna reads whole files and almost never searches |

No model writes anything. The "communication" is one reviewer's observed work changing what the others are asked to do. Baseline: ember + 2x luna (S07).

**(b) Schedule.**

| Item | Value |
|---|---|
| Triggers | ember after tool call 6 and 10; luna after tool call 8 and 12; Stop hook gives a final "source.md never opened" check, with no hold |
| Frequency | at most 2 injections per reviewer per package |
| Messages per reviewer | 2 received, 0 sent (telemetry is automatic) |
| Size cap | 300 characters per injection (one move text plus "no panel member has done this yet") |
| Schema | `panel-msg/1` with `kind:"move"`, `from:"radar"`, `move`, no anchor, no items |
| Deadline guard | no injection after t = 110 s (cap 157 s minus 45 s margin) |

**(c) Transport.** Board plus hooks. It is the only transport where the model takes no action at all, so it works the same for ember, luna and haiku.

**(d) Time budget (per package, baseline ember + 2x luna = 116 s, cap 157 s).**

| Reviewer | Baseline end | Added | New end |
|---|---|---|---|
| ember | 41 s | 2 moves x 2 turns x 3.2 s = 13 s | 54 s (inside luna's time, no effect on elapsed) |
| luna (slowest of two) | 116 s | 2 moves x 2 x 6.4 s = 26 s, plus hooks about 16 calls x 0.1 s = 2 s | 144 s |

Critical path 144 s: **+24%** (worst case equals expected, because injections are capped at 2). Idle time used: ember's 62-75 s idle hosts its 2 moves.

**(e) Contamination safeguards.**

- **Shared:** only move ids that nobody has done.
- **Withheld:** every finding, anchor, path and count.
- **Independent first pass:** no injection before tool call 6 (ember) or 8 (luna), so each reviewer has formed its own plan first.
- **Blind-spot spread:** impossible by construction, because no peer content is sent.
- **Convergence alarm:** the panel's mean pairwise Jaccard of anchored Tasks above the isolated baseline plus 0.15 (ember+luna 0.25 and luna+luna 0.33 per `investigation-patterns.md:81-82`, so alarm above 0.40 and 0.48) in 2 or more of 3 packages. Logged per package in `collab.json`.

**(f) Expected gain (collaboration share, out of 14 per run).** Assumption: an injected move is executed in 50-80% of cases, and executing it reaches the defect at a rate between the cheap near-miss rate and sonnet's rate.

| Issue | Low | High | Through |
|---|---|---|---|
| B1 / B2 | 0 / 0 | 0.05 / 0.05 | T2 (M3, M9 to luna; the rubric still pulls away) |
| B5 / I1 | 0.05 / 0.03 | 0.15 / 0.10 | T2 (M5, M6) |
| I4 | 0.05 | 0.20 | T2 (M4 is mechanical; ember runs it in seconds) |
| I5 | 0.02 | 0.10 | T1 (M7; may still be dropped as minor) |
| B8 / B6 / I6 | 0.03 / 0.02 / 0 | 0.10 / 0.08 / 0.05 | T1, T2 |
| **Total /14** | **0.20** | **0.88** | |
| I7 (control /2) | 0.10 | 0.40 | T1 (M1) |

Plus H share +0.2 to +0.6.

Caveat: a large part of this gain could come from a static catalogue in the brief. The experiment (section 4) isolates that with arm A1.

**(g) Effort.**

| Component | Lines |
|---|---|
| Board substrate (helpers, PostToolUse and Stop hooks, settings generator, `run-reviewer.sh` changes) | about 100 |
| `radar-classify.sh` (about 60), gap selector (about 40), catalogue JSON (about 30) | about 130 |
| **Total** | **about 230** |

Files: `EVAL/tools/run-reviewer.sh`, new `EVAL/tools/panel/`.

**(h) Failure modes and runbook.**

| Failure | Detection | Action |
|---|---|---|
| Classifier mislabels a move, so a done move is re-injected | `radar.jsonl` audit, spot-check | Fix the regex; the extra cost is at most 2 moves |
| The gaps are always the same moves | catalogue usage histogram | Expected; it measures panel blind spots, so report it |
| A reviewer ignores the injection | move executed: no (from telemetry) | Logged; the gain falls toward the static baseline |
| Hook not firing on gateway models | `hook_calls = 0` in metrics | Spike S0 gate; with the kill switch the run is isolated |
| Project hooks in the sandbox's tracked `.claude/settings.json` also fire | S0 lists active hooks | Confirm there is no conflicting `additionalContext` |

---

### Redesign 2: Idle-Shift Sweeper (ember's idle time becomes a search service for the luna reviewers)

**(a) Mechanism.** Ember finishes its normal review at about 41 s. Its report is sealed because the process exits. The harness then starts a **second ember session** with a sweeper brief: run moves M1, M2 and M7 against the candidate and the repo, and post **facts only**: path lists, counts, and `path:line` hits, with no judgement.

The two luna reviewers are read-driven followers: they open every file they are told about (`investigation-alias-control.md:60`). They receive the facts through the hook, open the listed files, and decide for themselves. This pairs the one cheap model that searches with the one that reads deeply. It attacks T1: luna runs 0.2 recursive searches per run, ember runs 3.7. Baseline: ember + 2x luna (S07).

**(b) Schedule.**

| Item | Value |
|---|---|
| Trigger 1 | ember review exits, then the sweeper starts (t ≈ 41 s) |
| Trigger 2 | the sweeper posts each fact as found; first at about t = 55 s, last by t ≤ 85 s |
| Trigger 3 (delivery) | luna's PostToolUse hook delivers only once (i) luna has made 6 or more tool calls **and** (ii) `sealed/<luna>.jsonl` exists. At call 6 the hook asks once: "run `panel-seal` with your current findings lines; peer facts become available after". If there is no seal by call 10, delivery is skipped and logged `seal_missing`. |
| Trigger 4 | luna's Stop hook holds at most 15 s for undelivered facts |
| Frequency | sweeper sends at most 4 facts; each luna acts on at most 3 |
| Size cap | 600 bytes per fact; at most 8 paths |
| Schema | `panel-msg/1` with `kind:"fact"`, `move` ∈ {M1, M2, M7}, `anchor` (the plan phrase swept), `items` (paths or path:line), `n` (count) |
| Deadline guard | no delivery after t = 125 s |

**(c) Transport.** Board plus hooks: facts must reach luna mid-run, the transport must work the same across models, and the facts form an audit log. A between-phase digest would add a full luna phase after 116 s.

**(d) Time budget (per package, baseline 116 s, cap 157 s).**

| Reviewer | Baseline end | Added | New end |
|---|---|---|---|
| ember review | 41 s | none | 41 s |
| ember sweeper | not run | starts at 41 s; 6 s start plus 10 turns x 3.2 s = 38 s | 79 s (runs in ember's idle time) |
| luna (slowest) | 116 s | seal 1 turn (6 s) plus up to 3 facts x 2 x 6.4 s = 38 s (worst), 2 facts typical = 26 s | worst 160 s, capped by the 125 s delivery deadline to at most 116 + 6 + 26 = 148 s; typical 142 s |

Critical path: typical **+22%**, worst **+28%**. Idle used: ember's whole idle window (41-79 s) hosts the sweep, so the sweep itself adds no elapsed time.

**(e) Contamination safeguards.**

- **Shared:** repo facts (paths, counts, line hits) from generic moves.
- **Withheld:** ember's findings, severities, claims and verdict. The sweeper is a fresh session that has never seen ember's report, so ember's conclusions cannot leak through it.
- **Independent first pass:** sealed draft before any delivery (`sealed/<rid>.jsonl`), and findings that come after a delivery are tagged `"origin":"peer"` (findings-v1 accepts unknown keys, `HO2:346`).
- **Blind-spot spread:** facts carry no framing, so ember's habit of asking whether a grep over-matches (the I5 inversion) cannot be passed on.
- **Convergence alarms:**
  - (i) echo rate: the share of luna's peer-tagged findings whose anchor equals a sweeper fact's anchor; alarm above 60%. Some echo is the intended effect; total echo means luna stopped its own review.
  - (ii) luna's own sealed findings per run falling below 1.0, against the S07 baseline of 1.75.

**(f) Expected gain (collaboration share).**

| Issue | Chain of assumptions | Low | High |
|---|---|---|---|
| I7 (control /2) | sweeper lists `test_worker_contract.py` 0.7-0.9 x luna opens a listed file 0.6-0.8 x finds and reports it (7 of 8 openers found it, but luna reports blocker-grade only) 0.4-0.7; two lunas | 0.25 | 0.60 |
| I5 | sweep lists the CHANGELOG line 0.3-0.6 x luna reports and keeps it 0.2-0.4 | 0.06 | 0.24 |
| B8 | M2 count computed 0.3-0.5 x linked to the Task sentence 0.2-0.4 | 0.06 | 0.20 |
| B6 | | 0.02 | 0.08 |
| B5, I1, I4 (not targeted) | | 0 | 0.05 each |
| B1, B2, I6 | | 0 | 0 |
| **Total /14** | | **0.14** | **0.67** |

Plus H share +0.2 to +0.6.

**(g) Effort.** Board substrate (about 100 lines), plus sweeper brief text (about 25), a launcher hook that starts the sweeper after ember's exit (about 15), a fact validator (about 25) and `panel-seal` (about 15). **Total about 180 lines.** Files: `run-reviewer.sh`, a row launcher, `EVAL/tools/panel/`.

**(h) Failure modes and runbook.**

| Failure | Detection | Action |
|---|---|---|
| luna never seals (gateway compliance) | `seal_missing` rate | Above 50% of luna runs: switch delivery to "tool call 8 or later, no seal needed", and record that the first pass is no longer separable |
| Sweeper floods trivial facts | facts per run equal to the cap, low luna uptake | Tighten the brief: only files outside the plan's named list |
| Facts arrive after luna finished | `first_delivery_t` later than luna's Stop | The Stop hold (15 s) covers it; otherwise logged `late` |
| Wrong blockers rise (luna grades every fact blocking) | wrong blockers more than baseline + 1.0 | Fail the arm (section 4 rule) |
| Sweeper's ember session misrouted | `model_ok` check on the sweeper's meta | The same identity audit as reviewers |

---

### Redesign 3: Axis-Flip Challenge (between phases: peers' anchors come back with an "other axis" move)

**(a) Mechanism.** Phase 1 is today's isolated review, unchanged; its sealed report is the first pass. When a reviewer finishes, the harness parses the findings-v1 blocks of the peers that have finished so far. It selects up to K peer findings whose category is `unpassable-check`, `contradiction` or `missing-requirement`. Surface findings are skipped: claims matching artifact path, hash or line-number patterns, which make up 21-23% of ember and luna findings (`investigation-patterns.md:73`).

For each selected finding it sends **only the anchor**, never the claim, paired with an axis-flip move. The move depends on the anchor's content:

| Anchor contains | Move sent |
|---|---|
| every, all, complete, only | M3 or M2 |
| a command or grep | M4 and M7 |
| a mapping or table | M5 and M6 |
| a constraint | M8 |

This is the "right place, wrong question" fix (T2): ember anchored the I5 sentence 15 times and the B5 mapping once, and in each case asked one question. A different model now asks a different question at the same place. Phase 2 resumes the reviewer's own session (`claude -p --resume <session_id> "<digest>"`) and returns an addendum. The harness then concatenates phase-1 and phase-2 findings lines into **one** findings-v1 block, with phase-2 ids renamed `P2-F1`… and tagged `"origin":"peer"`. The findings-v1 merge contract is unchanged.

Roles:

- **luna x2** receive reading flips on ember's anchors (ember produces 4.19 findings per run and anchors designSpec Task 1 in 52% of runs, Task 2 in 46%, Task 8 in 33%).
- **ember** receives search flips on luna's anchors and on the other reviewers' search-type anchors.

Baseline: ember + 2x luna (S07). A scale-up variant on haiku + 2x luna (S24) is given in (d), because haiku anchors the target Tasks most often: designSpec Task 1 in 92% of runs, Task 8 in 96%, Task 2 in 80%.

**(b) Schedule.**

| Item | Value |
|---|---|
| Trigger | each reviewer's phase-1 exit |
| Contents | the digest holds anchors from every peer that has finished at that moment; ember waits for both lunas before its phase 2 |
| Frequency | exactly one digest per reviewer per package (one exchange) |
| Maximum challenges | luna 2, ember 3 (haiku 1 in the haiku variant) |
| Size cap | digest at most 1,800 characters (3 challenges x 600 bytes) |
| Schema | `panel-msg/1` lines with `kind:"challenge"`, `from:"<peer rid>"`, `anchor`, `move`; no items |
| Phase-2 timeout | 45 s; on timeout the phase-1 report stands unchanged |

**(c) Transport.** Between-phase digest (plain files, written to a temp file then moved into place, so the write is atomic). The reasons:

- The phase-1 seal comes free: the process exited, so no compliance is needed.
- No live channel and no hooks, which makes it the most deterministic design.
- The digest file is the audit log.
- It gives the strongest independence guarantee.

It requires dropping `--no-session-persistence` from `run-reviewer.sh:48`, because `--resume` needs a stored session. Resume runs from the same cwd, `/tmp/evalsb/repo`. If resume fails for gateway models (UNVERIFIED, spike S2), phase 2 falls back to a fresh session given its own phase-1 report path plus the digest.

**(d) Time budget.**

Baseline ember + 2x luna (116 s, cap 157 s):

| Reviewer | Phase 1 end | Phase 2 | New end |
|---|---|---|---|
| luna A (first finisher, about 95 s) | 95 s | 6 s resume plus 2 x 2 x 6.4 s = 32 s | 127 s |
| luna B (slowest) | 116 s | 32 s | 148 s |
| ember | 41 s (idle until both lunas finish) | starts at 116 s; 6 s plus 3 x 2 x 3.2 s = 25 s | 141 s |

Critical path 148 s: **+28%**, with the 45 s timeout guaranteeing at most 116 + 45 = 161 s (+39%) only if luna overruns. The overrun guard is therefore a hard 35 s phase-2 timeout for luna, giving at most 151 s (+30%). Idle used: ember's 75 s wait covers its phase 2 start condition, and luna A's phase 2 runs inside luna B's phase 1.

Haiku variant (238 s, cap 322 s):

| Reviewer | Phase 2 | End |
|---|---|---|
| luna x2 | 2 challenges each, run inside haiku's phase-1 window | 116 + 32 = 148 s |
| haiku | 1 challenge at 238 s: 6 + 2 x 23 = 52 s | 290 s |

Critical path 290 s: **+22%**.

**(e) Contamination safeguards.**

- **Shared:** peer anchors (exact candidate quotes) plus a catalogue move.
- **Withheld:** peer claims, severities, verdicts and counts.
- **Independent first pass:** structural (a separate phase, sealed by process exit), so it can be audited byte for byte from `<rid>.p1.md`.
- **Blind-spot spread:** the peer's question is never sent, only the place, and the flipped move is by rule a *different* question from the one the peer's category implies. A peer's wrong blocker is therefore not repeated: the receiver is asked a different question, not to confirm.
- **Convergence alarms:**
  - (i) echo rate: the share of phase-2 findings that restate the peer's own claim on the same anchor (claim token Jaccard above 0.6 with the peer's claim); alarm above 30%.
  - (ii) the panel's ledger row count falling more than 20% below the isolated arm. A ledger-only signal, so it is usable in the product without ground truth.

**(f) Expected gain (collaboration share).** Model: P = P(a peer anchors the right sentence) x P(challenge selected and executed, 0.5-0.6) x P(correct conclusion kept and credited, 0.3-0.6).

| Issue | Anchor rate used | Low | High |
|---|---|---|---|
| B1 | ember designSpec Task 1, 52% | 0.03 | 0.15 |
| B2 | | 0.02 | 0.08 |
| B5 | ember designSpec Task 8, 33% (3 cheap near-misses) | 0.04 | 0.15 |
| I1 | | 0.02 | 0.08 |
| I4 | ember designSpec Task 12, 14% | 0.02 | 0.08 |
| I5 | ember designSpec Task 2, 46%; luna must grep the root; minor-drop risk | 0.04 | 0.15 |
| I6 | ember alias Task 6, 57%; M8 sibling sweep | 0.03 | 0.12 |
| B8 / B6 | | 0.01 / 0.02 | 0.05 / 0.08 |
| **Total /14 (ember + 2x luna)** | | **0.23** | **0.94** |
| **Haiku variant** | anchors about 2x as often | **0.40** | **1.60** |
| I7 (control /2) | | 0.05 | 0.20 |

Plus H share +0.2 to +0.6.

**(g) Effort.**

| Component | Lines |
|---|---|
| `run-reviewer.sh`: drop `--no-session-persistence`, capture `session_id` from the JSON result | about 5 |
| `phase2-digest.sh`: jq parse of blocks, category and keyword selection, style routing, surface filter | about 70 |
| Phase-2 launcher with timeout and resume or fresh fallback | about 25 |
| Block combiner: one findings-v1 block, renamed ids, origin tag | about 30 |
| Validation through the real parser (H2) | about 15 |
| **Total** | **about 145** |

No hooks are needed.

**(h) Failure modes and runbook.**

| Failure | Detection | Action |
|---|---|---|
| `--resume` fails on a gateway model | exit code not 0 or empty result | Fresh-session fallback (logged `resume_fallback`); costs about 10 s more |
| Phase 2 rewrites or withdraws phase-1 findings | the combiner keeps phase-1 lines verbatim; diff check | Phase-1 lines are immutable by construction |
| Phase-2 block malformed | H2 parser check | One re-ask, else phase-2 lines are dropped with a warning and phase 1 stands |
| Digest empty (ember produced only surface findings) | `challenges = 0` | Logged; the package behaves as isolated |
| Two blocks in one report (parser uses the last) | combiner unit test | Exactly one block emitted |
| Session storage grows on the host | disk check | Delete `~/.claude/projects/<sandbox>` sessions after the row is judged |

---

### Redesign 4: Flag-and-Adjudicate (one model flags checkable sentences, a different model must settle them)

**(a) Mechanism.** Every reviewer is told to *flag, not settle* certain sentences it meets while reading:

- ember (fast, reaches the target Tasks often) posts a **card** for each acceptance criterion or sentence containing every, all, only or complete, each command or grep criterion, and each mapping table. Each card carries the anchor and a **reading** move (M3, M4, M5, M6, M9).
- luna posts cards that need **search** moves (M1, M2, M7, M10) on sentences it reads.

Cards are routed to a different model, never back to the flagger. The adjudicator must answer the move with a finite check and its result, inside its own findings block. Ember is kept alive by a Stop hold, so it can adjudicate luna's search cards in its idle time. This answers the open question "is a mid-run message more valuable as a challenge than as shared findings?" with a challenge that has a mandatory form. Baseline: ember + luna (S13, the cost champion).

**(b) Schedule.**

| Item | Value |
|---|---|
| Ember posting | from its 3rd tool call, at most 4 cards |
| Luna posting | after its seal (from tool call 6), at most 1 search card |
| Delivery to luna | PostToolUse, only after its seal |
| Delivery to ember | PostToolUse while running, then the Stop hold for up to 50 s (until t ≤ 104 s) |
| Maximum adjudications | luna 2, ember 1 |
| Size cap | 600 bytes per card |
| Schema | `panel-msg/1` with `kind:"card"`, `anchor` required, `move` required, `to` set by the router |
| Deadline guard | no delivery after t = 105 s |

**(c) Transport.** Board plus hooks plus Stop hold. Cards need mid-run delivery to a running luna and a way to keep ember alive, and the board does both durably.

Cross-session `SendMessage` was considered because it has built-in reply addresses. It is the named fallback only if spike S1 shows that ember and luna call `SendMessage` reliably and that a held `-p` session receives messages. Even then it would lose the board audit log, so the board stays primary.

**(d) Time budget (per package, baseline ember + luna = 100 s, cap 135 s).**

| Reviewer | Baseline end | Added | New end |
|---|---|---|---|
| ember | 41 s | 4 card posts x 3.2 s = 13 s → 54 s; hold until a luna card arrives (about 60-80 s); 1 adjudication x 2 x 3.2 s = 6 s | at most 86 s (hold ends by 104 s at most) |
| luna (slowest) | 100 s | seal 6 s, 1 card post 6 s, 2 adjudications x 2 x 6.4 s = 26 s | worst 138 s, kept to 132 s by having luna post its card in the same turn as its seal; typical (1 adjudication) 119 s |

Critical path: typical **+19%**, worst **+32%**. Idle used: ember's 46-59 s idle window hosts the hold and its adjudication.

**(e) Contamination safeguards.**

- **Shared:** an anchor plus a required move.
- **Withheld:** the flagger's opinion. The card has no claim field and the flagger is told not to judge the sentence.
- **Independent first pass:** luna seals before receiving. Ember has no peer input before its own findings are complete, because luna's cards arrive after ember's report is sealed in its draft.
- **Blind-spot spread:** the adjudicator is a different model family by rule, and the move dictates the question, so the flagger's angle is not inherited.
- **Convergence alarms:**
  - (i) adjudication agreement: the share of cards where the adjudicator raises a finding; alarm above 90% (rubber-stamping) or below 5% (cards ignored);
  - (ii) pairwise Task Jaccard above 0.40 against the ember+luna baseline of 0.25.

**(f) Expected gain (collaboration share).** Model: P(flagger posts a card on the sentence: ember complies with posting 0.6-0.8, and the sentence is among its 4 cards 0.3-0.5) x P(adjudicator reaches the defect 0.3-0.5) x credit 0.5-0.8.

| Issue | Low | High | Through |
|---|---|---|---|
| B1 | 0.03 | 0.16 | T2, M3 card on an unbounded AC |
| B2 | 0.01 | 0.08 | T2 |
| I4 | 0.03 | 0.15 | T2, M4 card on a grep AC |
| B5 | 0.03 | 0.15 | T2 |
| I1 | 0.02 | 0.10 | T2 |
| B8 / B6 | 0.02 / 0.01 | 0.10 / 0.06 | T1 (luna search card to ember) |
| I5 | 0.01 | 0.08 | |
| I6 | 0 | 0.05 | |
| **Total /14** | **0.16** | **0.93** | |
| I7 (control /2) | 0 | 0.10 | |

Plus H share +0.2 to +0.5.

Note: the flagging step could be replaced by a deterministic sentence extractor. That would be a prompt and harness change, not collaboration; arm A1 bounds it.

**(g) Effort.** Board substrate (about 100 lines), plus router (move to style, flagger excluded, about 40), card validator (about 20), Stop hold with poll and timeout (about 30), brief text (about 20). **Total about 210 lines.**

**(h) Failure modes and runbook.**

| Failure | Detection | Action |
|---|---|---|
| ember never posts (gateway tool compliance) | `cards_sent = 0` | Above 50% of runs: the design is not viable on ember; stop the arm |
| Stop hook hold exceeds the hook timeout (UNVERIFIED default) | S0 measures it; hook config sets an explicit `timeout` | Lower the hold to the measured safe value |
| 8-continuation cap reached by repeated blocks | count of `stop_blocks` | At most 1 block per reviewer by design |
| Card overload pulls luna off its own review | luna's sealed findings per run below 1.0 | Lower the cap to 1 adjudication |
| Wrong blockers from adjudications | wrong blockers more than baseline + 1.0 | Fail the arm |

---

### Redesign 5: Coverage Deflection (fast cheap reviewers steer sonnet away from what is already covered)

**(a) Mechanism.** Every panel converges on the easy issues: B3 is found in 68 of 76 runs, I2 in 52 and I8 in 56 (`CR:498`). In ember + luna + sonnet, ember and luna finish long before sonnet, the slowest reviewer and the only one that reliably runs reverse-dependency sweeps.

When each fast reviewer exits, a harness watcher parses its findings-v1 block and posts a **coverage card** to sonnet:

- Tasks that already have a non-surface finding, keyed by (Task, category) with the counts.
- Tasks that have none.
- The instruction: "apply catalogue moves M1-M10 to the uncovered Tasks first; finish checks you have already started".

Sonnet's budget moves toward Tasks nobody covered, where the rare issues sit. ember and luna act as scouts, and their sealed results reshape sonnet's search mid-run. Baseline: ember + luna + sonnet (S14), the optional quality tier.

**(b) Schedule.**

| Item | Value |
|---|---|
| Trigger 1 | ember exit (about 41 s) |
| Trigger 2 | luna exit (about 102 s) |
| Delivery | sonnet's next PostToolUse (within about 14 s) |
| Frequency | 2 cards per package to sonnet; 0 to ember and luna |
| Size cap | 600 bytes per card |
| Schema | `panel-msg/1` with `kind:"coverage"`, `from:"watcher"`, `items` = up to 8 Task ids with counts and categories in a compact form `"T9:contradiction:2"` (Task ids, not ground-truth content) |
| Deadline guard | no card after t = 200 s |

Surface findings (path, hash, line-number claims) do not count as coverage. Otherwise the luna Task 12 artifact objection, present in 91% of luna runs on the control package, would mark Task 12 "covered" and steer sonnet away from I7.

**(c) Transport.** Board plus a hook in sonnet only. Cards are generated by the harness, so no model has to send anything. Sonnet is a Claude model, so hook delivery is the lowest-risk case.

**(d) Time budget (per package, baseline 225 s, cap 304 s).**

| Reviewer | Baseline end | Added | New end |
|---|---|---|---|
| ember, luna | 41 s, 102 s | none | unchanged |
| sonnet (slowest) | 225 s | 2 cards x 1 turn of re-planning (14 s) = 28 s; told "spend at most 2 extra tool calls", 2 x 14 s = 28 s | expected 253 s, worst 281 s |

Critical path: expected **+12%**, worst **+25%**. Idle used: none needed. Ember's and luna's runs already overlap sonnet's.

**(e) Contamination safeguards.**

- **Shared:** Task ids and category counts.
- **Withheld:** anchors, claims and severities.
- **Independent first pass:** sonnet receives nothing before t ≈ 41 s, by which point it has read the plan and source.md. Its findings before and after each card are separable by the transcript timestamps of its tool calls, which are logged in `metrics/<rid>.jsonl`.
- **Blind-spot spread:** counts do not transmit what the peers concluded, only where they were.
- **Convergence alarm:** a deflection alarm, not a convergence alarm, because this design deliberately *diverges* sonnet. Alarm if sonnet's anchored Tasks overlap the "covered" list by more than 50% (deflection ignored), or if the panel's union of anchored Tasks *shrinks* against the isolated baseline.

**(f) Expected gain (collaboration share).** Sonnet's isolated reach per run: I4 4 of 26, B5 2, I1 1, I7 7 of 26 clean (`investigation-designspec.md:124`; `investigation-patterns.md:132`). Deflection raises its time on designSpec Task 2 (8% of sonnet runs), Task 12 (23%) and alias Task 7 (27%).

| Issue | Low | High |
|---|---|---|
| I4 | 0.05 | 0.20 |
| I5 | 0.03 | 0.15 |
| B8 | 0.05 | 0.15 |
| B1 / B2 | 0.02 / 0.02 | 0.10 / 0.10 |
| B5 / I1 | 0.03 / 0.02 | 0.10 / 0.10 |
| B6 / I6 | 0.02 / 0.02 | 0.08 / 0.08 |
| **Total /14** | **0.26** | **1.06** |
| I7 (control /2) | -0.20 | +0.20 |

I7 can fall if Task 12 is miscounted as covered, which is why the surface filter exists. H share is +0.1 to +0.4, and H4 lowers measured I7 for sonnet panels by up to 2 in 9 credits.

**(g) Effort.** Board substrate, hook in sonnet only (about 60 lines), coverage watcher (poll every 2 s for finished reports, jq per-Task counts, surface filter, about 60). **Total about 120 lines.**

**(h) Failure modes and runbook.**

| Failure | Detection | Action |
|---|---|---|
| Deflection pushes sonnet off a Task where a peer's finding was a wrong blocker, so a real issue there is missed | the experiment's per-Task reach compared with S14 | Counts are by (Task, category), not by Task; review per-issue reach |
| Surface regex misses a surface claim | spot-check of the coverage audit | Extend the regex |
| sonnet ignores the cards | deflection alarm | Logged; gain goes to 0, with no harm |
| Cost: needs a sonnet panel (2.2x tokens of ember + 2x luna) | n/a | Use only where the quality tier is already chosen (`CR:428`) |

Grok is used in no design: its median of 790 s per review, and 2,109-3,897 s elapsed in its panels (`CR:314, :325`), cannot fit any cheap baseline's +35% window.

---

## 3. Comparison of the five redesigns

The gain columns are the collaboration share out of 14 per run, assuming the harness fixes H are applied to both arms. Add the H share (+0.2 to +0.6 for cheap panels) separately; it is not counted here.

| # | Redesign | Baseline (elapsed per package) | Elapsed overhead (expected / worst) | Output tokens overhead | Gain /14 low-high | I7 (control /2) | Contamination risk | Effort | Reliability |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Move Radar | ember + 2x luna (116 s) | +24% / +24% | +26% (about 5.6k) | 0.20-0.88 | 0.10-0.40 | Lowest: no peer content | about 230 LOC | High: no model action needed; depends on hooks firing (S0) |
| 2 | Idle-Shift Sweeper | ember + 2x luna (116 s) | +22% / +28% | +45% (about 9.6k) | 0.14-0.67 | 0.25-0.60 | Low-medium: repo facts, no conclusions | about 180 LOC | Medium: hooks, a second process, luna sealing compliance |
| 3 | Axis-Flip Challenge | ember + 2x luna (116 s); haiku variant (238 s) | +28% / +30%; variant +22% | +34% (about 7.2k) | 0.23-0.94; variant 0.40-1.60 | 0.05-0.20 | Low: anchors only, first pass sealed by process exit | about 145 LOC | Highest: no live channel; fallback is the phase-1 report; resume needs spike S2 |
| 4 | Flag-and-Adjudicate | ember + luna (100 s) | +19% / +32% | +36% (about 6.3k) | 0.16-0.93 | 0-0.10 | Medium: anchors routed between named peers | about 210 LOC | Medium-low: needs ember to post and luna to adjudicate; Stop hold |
| 5 | Coverage Deflection | ember + luna + sonnet (225 s) | +12% / +25% | +16% (about 7.6k) | 0.26-1.06 | -0.20 to +0.20 | Low: Task ids and counts only | about 120 LOC | Medium-high: harness-generated cards, Claude receiver; needs a sonnet panel |

Token overheads are output tokens, the study's metric. Hook injection and resume also raise input tokens, mostly as cache reads; these are recorded but not compared.

---

## 4. Recommended first experiment

**Choice.** Test **Redesign 3 (Axis-Flip)** and **Redesign 2 (Idle-Shift Sweeper)** first, on the decided default panel ember + 2x luna (`CR:428`, `HO2:288`).

- Redesign 3 has the highest reliability and the largest T2 reach on the cheap panel.
- Redesign 2 is the only cheap design with a strong I7 path (T1), and it uses idle time that is otherwise wasted.
- Redesign 1 is deferred: it is most at risk of being matched by a static checklist.
- Redesign 4 is deferred: two-way gateway compliance is unverified.
- Redesign 5 is deferred: it needs the 2.2x-cost sonnet tier and puts I7 at risk.

**Gate 0 (must pass before any arm runs; one package each).**

| Spike | What it checks |
|---|---|
| S0 | `--settings` PostToolUse and Stop hooks fire in `claude -p` for `muse-ember-1.0` and `gpt-6-luna`; the hook timeout and the hold behaviour; which sandbox project hooks are active |
| S2 | `--resume` works for both gateway models once `--no-session-persistence` is removed |
| S3 | Full-chain smoke test (reviewer, combiner, `superclaude review merge`, anonymiser, `judge-one.sh`) with 0 dropped findings lines, applying lesson `HO2:259` |

**Arms.** All arms use harness fixes H1-H4, and all are concurrent and interleaved per package.

| Arm | Description | Purpose |
|---|---|---|
| A0 | ember + 2x luna, isolated | Collaboration control |
| A1 | A0 plus the move catalogue M1-M10 appended to every brief, no communication | Separates "telling a model the moves" from "a peer's work triggering the moves" |
| A2 | Redesign 3, Axis-Flip | |
| A3 | Redesign 2, Idle-Shift Sweeper | |
| Reference only | Existing S07 (6 runs, old harness) | Compared with A0, estimates the H share; not concurrent, so labelled confounded |

**Runs.** 4 replicates per arm x 3 packages = 48 package-runs and 48 blind Opus judges.

- Judging uses `EVAL/tools/tmp-scripts/judge-one.sh` unchanged, on anonymised merged reports with `origin` keys and board references stripped, so the judge cannot tell which arm a report came from.
- Concurrency: at most 10 runs at once, at most 4 ember, `NOFALLBACK=1` (`HO2:236`).
- Estimated cost: about 1.25M reviewer output tokens. Wall time is about 25-30 minutes per replicate wave.

**Pre-registered decision rule.** A run = one panel on all three packages.

1. **Targeted reach (primary).** For each arm, count the runs that found at least one of B1, B2, B5, B6, B8, I1, I4, I5, I6 or I7. The historical cheap rate is 0 of 30 runs. A collaboration arm X **passes reach** if it has 2 or more of 4 runs **and** at least 2 more than A1.
2. **Catch.** Mean found /14 of X is at least A1 + 0.4 (permutation test reported; power is low at n=4, so this is a screening threshold, not a significance claim).
3. **Precision.** Mean wrong blockers on the defect-rich packages for X is at most A1 + 1.0.
4. **Elapsed time.** Median elapsed per package of X is at most 1.35 x A0's median, and no single package exceeds 1.5 x.
5. **Integrity.**
   - No board message or digest contains a ground-truth `plan_quote` substring of 12 characters or more (checked by grep against each `ground-truth.json`).
   - No reviewer transcript opens `.dev/reflect/`.
   - Convergence alarms fire in at most 1 of 12 packages.

**Outcomes.**

| Result | Decision |
|---|---|
| Both A2 and A3 pass 1-5 | Run a 6-run confirmation of the higher-catch arm (A2 on a tie, being more reliable), then its haiku + 2x luna variant |
| A1 within 0.3 of X on catch and within 1 run on reach | Collaboration adds nothing beyond the prompt; ship H plus the static catalogue and stop |
| A0 at or above S07 + 0.5 | Report the harness fixes as the main lever (independent of the collaboration decision) |
| Abort an arm during the run | 2 of its first 3 packages exceed 1.5 x elapsed, or its luna seal compliance (A3) is below 50% |

---

## 5. Requirements for the chosen designs (Redesign 3 Axis-Flip, Redesign 2 Idle-Shift Sweeper, and the shared substrate)

### 5.1 Harness preconditions (apply to every arm)

| Id | Requirement | Verification |
|---|---|---|
| R-01 | The reviewer brief names the absolute path of source.md next to the candidate path and asks the reviewer to read both. | grep the brief in `run-reviewer.sh`; 0 of 12 A0 transcripts lack a tool call naming source.md, or the miss is reported per model |
| R-02 | Each report is parsed at run time with the real findings parser. If any line would be dropped (anchor or anchor2 outside 12-200 characters, claim over 300, refs over 8, id over 16, bad severity, MINOR marked blocking), the harness re-asks once with the parser's error list. Remaining drops are recorded in `meta.json` as `dropped_lines`. | Unit test with a fixture report holding a 250-character anchor: re-ask is triggered and `dropped_lines` is recorded; S3 smoke shows 0 dropped lines |
| R-03 | For each package, the reviewer sandbox is a `git archive` of the commit the plan was written against, minus `.dev/tasks/done`, `.dev/eval-workspaces`, `.dev/research` and `.dev/reflect`. The base commit for each package is recorded in the manifest. | `ls /tmp/evalsb/<pkg>/repo/.dev/reflect` fails; the manifest lists 3 base SHAs; `refs/merge-guard.md` lacks the repaired line 146 text in the designSpec sandbox |
| R-04 | The findings-v1 block format and `superclaude review merge` are unchanged. Collaboration output reaches the merge only as additional lines in the reviewer's single findings-v1 block. | `merge` runs with the same arguments as `EVAL/analysis/merge-b11.sh`; every merged report lists the same reviewer ids as the resolution |
| R-05 | `PANEL_COLLAB=0` yields a launch command byte-identical to today's `run-reviewer.sh:48` except for R-01 and R-03. | diff of the generated command lines |

### 5.2 Shared message rules

| Id | Requirement | Verification |
|---|---|---|
| R-06 | Every message is a `panel-msg/1` JSON line of at most 600 bytes. The fields `claim`, `severity`, `blocking` and `category`, and any key not in the schema, are rejected and the line is not delivered. | Validator unit test: 6 bad fixtures rejected, 3 good ones accepted |
| R-07 | The `move` field takes only M1-M10. The catalogue text is frozen in one file with a recorded sha256, and contains no ground-truth `plan_quote` substring of 12 characters or more and no file path named in any `ground-truth.json` description. | Script check against the 3 `ground-truth.json` files; sha256 in the manifest |
| R-08 | Any `anchor` in a message is an exact substring of the candidate (after whitespace flattening), 12-200 characters, taken from a peer's own findings or the sweeper's own swept phrase, never from any file outside the sandbox and candidate. | Validator checks it is a substring of `candidate.md`; the integrity grep against ground truth (decision rule 5) |
| R-09 | Reviewers keep `--disallowedTools Edit Write NotebookEdit`. Helper scripts write only under `$BOARD`, and `$BOARD` is outside the sandbox repo and the candidate directory. | `git status` in the sandbox snapshot repo is clean after each run; the candidate's sha256 is unchanged |
| R-10 | Findings created after a reviewer received any peer message carry `"origin":"peer"`. Phase-1 or sealed findings carry `"origin":"own"`. The anonymiser strips `origin` before judging. | Combiner unit test; grep `merged-anon.md` for `origin` returns 0 |

### 5.3 Redesign 3: Axis-Flip Challenge

| Id | Requirement | Verification |
|---|---|---|
| R-11 | Phase 1 runs exactly the isolated brief. The phase-1 report is saved as `<rid>.p1.md` and never modified. | sha256 of `<rid>.p1.md` taken at phase-1 exit equals the value at judging |
| R-12 | The digest selects at most 2 challenges for luna and at most 3 for ember, only from peer findings with category `unpassable-check`, `contradiction` or `missing-requirement`, excluding claims that match the surface regex (artifact path, edit scope, hash, line number). | Unit test with fixture blocks; the digest includes no surface findings |
| R-13 | Each challenge pairs a peer anchor with a move chosen by the routing table: every/all/complete/only goes to M3 or M2; a command or grep to M4 or M7; a mapping or table to M5 or M6; a constraint to M8. Search moves go to ember and reading moves to luna. A challenge never goes back to the anchor's author. | Router unit test over 10 fixtures |
| R-14 | Phase 2 resumes the reviewer's own session with the digest. If resume fails, it starts a fresh session with the phase-1 report path plus the digest, and logs `resume_fallback`. | Spike S2; metrics count |
| R-15 | Phase-2 hard timeout is 35 s for luna and 45 s for ember. On timeout the phase-1 report is the final report. | Fault-injection test with `sleep` |
| R-16 | The final report holds exactly one findings-v1 block: phase-1 lines verbatim, then phase-2 lines with ids `P2-F<n>`, each validated by R-02. | Parser returns 1 block; line counts add up |

### 5.4 Redesign 2: Idle-Shift Sweeper

| Id | Requirement | Verification |
|---|---|---|
| R-17 | When ember's review exits, the harness starts an ember sweeper session with a brief limited to M1, M2 and M7 on the candidate's edited files and on its all/only sentences. The sweeper never receives ember's report. | Launcher test; the sweeper transcript contains no read of `$OUT/<ember rid>*` |
| R-18 | The sweeper posts at most 4 facts, `kind:"fact"`, each with at most 8 `items`, and produces no findings block. The sweeper is not passed to the merge. | Board count; resolution lists 3 reviewers |
| R-19 | The luna PostToolUse hook delivers peer facts only after `sealed/<rid>.jsonl` exists and after the reviewer's 6th tool call, asks for the seal once at call 6, and skips delivery with `seal_missing` if there is no seal by call 10. | Hook unit test with a simulated call counter |
| R-20 | Each luna acts on at most 3 facts. The hook delivers nothing after t = 125 s from panel start. The luna Stop hook holds at most 15 s and blocks at most once. | Metrics: `facts_delivered ≤ 3`, `stop_blocks ≤ 1`, `last_delivery_t ≤ 125` |

### 5.5 Board substrate, observability and elapsed-time target

| Id | Requirement | Verification |
|---|---|---|
| R-21 | Each reviewer gets its hooks only through a per-reviewer `--settings` JSON whose commands contain the absolute board path and the reviewer id. Hooks read nothing from the environment. | Generated settings inspected; S0 passes on ember and luna |
| R-22 | Hooks never fail the reviewer. On any hook error they print nothing, exit 0, and append to `metrics/<rid>.jsonl` with `hook_error`. | Fault injection: corrupt board line; the review completes and the error is logged |
| R-23 | Per package, the harness writes `collab.json` with these fields: arm, per-reviewer `msgs_sent`, `msgs_received`, `first_delivery_t`, `seal_t`, `seal_missing`, `resume_fallback`, `phase2_s`, `stop_blocks`, `hook_calls`, `hook_error`, `hook_ms_p95`, plus panel `elapsed_s`, `baseline_elapsed_s`, `overhead_pct`, `pairwise_task_jaccard`, `echo_rate`, `ledger_rows`. | JSON schema check on all 36 collaboration package-runs |
| R-24 | Elapsed-time target: per package, `elapsed_s ≤ 1.35 × median A0 elapsed for that package`. The error budget is 1 package in 12 per arm. Exceeding 1.5x on any package raises `SLO_BREACH`. | Summary script over `collab.json`; the decision rule uses it |
| R-25 | Alarms are computed without ground truth and logged per package. `CONVERGENCE` fires when `pairwise_task_jaccard` exceeds the isolated arm's mean + 0.15, or when `ledger_rows` falls more than 20% below the isolated arm. `ECHO` fires when `echo_rate` exceeds 30% (Redesign 3) or 60% (Redesign 2). `SEAL` fires when seal compliance is below 50%. | Summary script; a fixture with copied claims triggers `ECHO` |
| R-26 | The board directory (messages, sealed drafts, digests, metrics) is kept per row and package next to the reviewer outputs, and is never deleted. It is quarantined in place on contamination, following the study convention. | Directory present for every collaboration package-run |

### 5.6 Experiment conduct

| Id | Requirement | Verification |
|---|---|---|
| R-27 | Gate 0 spikes S0, S2 and S3 pass and are recorded before any arm runs. | Spike notes with transcripts in the eval workspace |
| R-28 | Arms A0-A3 run 4 replicates each over all 3 packages, interleaved per package, with `NOFALLBACK=1`, at most 10 concurrent runs and at most 4 ember. Model identity is checked per run as in `run-reviewer.sh:51-56`, including the sweeper and phase-2 sessions. | meta.json has `model_ok:true` for every session; scheduler log |
| R-29 | Each (arm, run, package) is judged once by the unchanged `judge-one.sh` on an anonymised merged report, with the per-batch API-error audit. | 48 score.json files; API-error audit shows 0 bad |
| R-30 | The decision rule of section 4 is committed to the eval workspace before the first arm runs and is applied unchanged. Results are reported with run-level values, permutation p-values and the n=4 power caveat. | Commit time of the rule file is earlier than the first run timestamp |

---

Not checked in this specification:

- Hook firing, hook timeout and `--resume` on gateway models are unverified; spikes S0 and S2 decide them.
- The time per turn and the ~6 s session start are medians and estimates, not measurements under hooks.
- Every gain range is an assumption-driven estimate built from near-miss counts, not data.

Risks:

- At n=4 per arm, only large effects separate from noise.
- The study showed that a single strong run regresses to the mean (`CR:424`).
