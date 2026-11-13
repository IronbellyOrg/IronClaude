<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 4 (opus:devops) -->
<!-- Merge date: 2026-11-13T19:02:25Z -->

<!-- Source: Base (original, modified) - new title and reading guide per Change #1 (global decisions 1-2; named-share style of Variant 5 (sonnet:performance), V5:21-31) -->
# Requirements specification: reviewers that collaborate during the run on the tasklist review panel

Path abbreviations used throughout:

- `EVAL` = `.dev/eval-workspaces/tasklist-review-panel/20261111-a1`
- `BS` = `.dev/brainstorms/20261113-163248-panel-collaboration`
- `CR` = `EVAL/COMBO-REPORT.md`
- `HO2` = `.dev/eval-workspaces/tasklist-review-panel/HANDOFF-review-panel-unification-run2.md`
- `RR` = `EVAL/tools/run-reviewer.sh`

Issue labels follow `CR:401-417`: B1-B5 and I1-I5 are designSpec GT1-GT10 (so designSpec GT6 = I1), B6-B8 and I6 are alias GT1-GT4, and I7 and I8 are control GT1-GT2. The study's "found /14" metric covers only the two defect-rich packages: B1-B5 and I1-I5 (designSpec), plus B6-B8 and I6 (alias). I7 and I8 belong to the control package and are reported as "control /2". So in this specification, gains on I7 are always reported separately from gains out of 14.

Devops framing: each redesign is treated as a change shipped to a running service, and each gets the following:

- **Elapsed-time target.** Panel elapsed time per package must stay at or below 1.35 times its isolated baseline. For the four mid-run designs this target is audited by an error budget, not enforced by a kill (section 2.0, timing rules).
- **Kill switch.** One setting turns collaboration off and restores the isolated panel with the harness fixes (R-05).
- **Audit trail.** Every message exchanged is logged, so the exchange can be checked afterwards.
- **Alarms.** Each design has named alarms.
- **Runbook entries.** Each failure mode has an entry saying how it is detected and what to do.

**How to read this specification.**

The five redesigns, one per design family. The redesign numbers are kept from the base document; the slot order is the order of the experiment and of the comparison table.

| Slot | Family | Redesign | Panel | Named isolated baseline (planning value per package) |
|---|---|---|---|---|
| 1 | F1 Between-phase cross-examination | Redesign 3 Axis-Flip Challenge | ember + 2x luna | EL2, 116 s |
| 2 | F4 Searcher-to-reader fact relay | Redesign 2 Idle-Shift Sweeper | ember + 2x luna | EL2, 116 s |
| 3 | F3 Content-free coverage steering | Redesign 1 Move Radar | ember + 2x luna | EL2, 116 s |
| 4 | F6 Steering a running strong model | Redesign 5 Coverage Deflection | sonnet + 2x luna | SL2, 273.7 s |
| 5 | F7 Directed challenge | Redesign 4 Flag-and-Adjudicate | ember + 2x luna | EL2, 116 s |

Experiment arms (section 4). Every arm except A0 carries the harness fixes H1-H4.

| Arm | Content |
|---|---|
| A0 | ember + 2x luna on today's harness, run fresh (no harness fixes) |
| A1 | ember + 2x luna, isolated, with the harness fixes H1-H4. This is the isolated baseline every EL2 design is measured against (the base document called this arm "A0") |
| A2 | A1 plus the static move kit (catalogue M1-M10 in every brief), no communication |
| A3 | Redesign 3, Axis-Flip Challenge (F1) |
| A4 | Redesign 2, Idle-Shift Sweeper (F4) |
| A5 | Redesign 4, Flag-and-Adjudicate (F7) |
| A6 | Redesign 1, Move Radar (F3) |
| Stage 2 | A1-SL2 and A2-SL2 (the same two controls on sonnet + 2x luna) and F6-SL2 (Redesign 5, Coverage Deflection) |

Symbols, defined once and used with these meanings everywhere:

| Symbol | Meaning |
|---|---|
| B | Isolated panel elapsed time per package for a named baseline. Planning values come from `CR` (three-package elapsed divided by 3): EL2 116 s, HL2 238 s, SL2 273.7 s. |
| B_A1 | The measured per-package median elapsed time of arm A1 (isolated, with the harness fixes). It is the reference for the +35% cap, the phase-2 deadline and the hang guard. For stage 2 it is the A1-SL2 median. |
| B_f | The frozen B_A1 that Spike 4 writes into the per-package values file before any arm runs. Every in-run deadline (the finish signal, the phase-2 deadline T0 + 1.30 B_A1 and the hang guard T0 + 1.5 B_A1) is computed from this frozen value. |
| B_c | The concurrent A1 median measured during the experiment. The after-the-fact cap check uses B_c. |
| T0 | The launch time of one panel on one package (one row-package). |
| turn_p90 | The 90th percentile duration of one turn of the reviewer that sets the panel's elapsed time: luna on EL2, sonnet on SL2. Planning value 6.4 s (luna) and 14 s (sonnet), which are medians, not p90. |
| T_report_p90 | The 90th percentile duration of that reviewer's last turn, the one that writes the final report. Planning value 6.4 s for luna. Unmeasured; Spike 4 measures it. |
| k | For the mid-run designs F3, F4, F6 and F7: the number of items (injections, facts, requests or cards) one receiving reviewer acts on per package. Computed per package from the formula in section 2.0. Planning rows are given at k = 1 (central) and k = 2 (optimistic). |
| n | For F1: the number of challenges in one phase-2 launch, computed per launch attempt from the phase-2 box. |
| H | Harness share = A1 - A0: the gain from the harness fixes alone. |
| P | Prompting share = A2 - A1: the gain from telling reviewers the moves, with no communication. |
| C | Collaboration share = (design arm) - A2: the gain from the exchange itself. C is conditional on H being applied in both arms. |

H, P and C are always reported in separate columns and are never added together.

---

<!-- Source: Base (original, modified) - section 1 restructured per Change #2 (gate funnel: Variant 2 (opus:analyzer), V2:9-94; T2a/T2b: Variant 5 (sonnet:performance), V5:40; T1 complementarity: Variant 1 (opus:architect), V1:25-45 and V2:27) -->
## 1. Theories

All three theories from the seed brief are accepted, and each is refined against the evidence. The refinements matter for design. T1 is about **what the reviewer searches for**, not how much it searches, and the two halves of the missing move sit in different cheap models. T2 is about **which question is asked at the right place**, not how much the model thinks; it splits into T2a (right place, one question) and T2b (the place is never reached). T3 is a **harness confound**: collaboration cannot remove it, so every gain estimate below has to be separated from it.

Each miss is traced through a three-gate funnel: **exposure** (did the reviewer reach the evidence?), **question** (did it ask the question that exposes the defect?) and **survival** (did the finding survive the grading rules, the merge and the sandbox?). A defect is found only if all three gates pass. T1 and T2b block mostly the exposure gate, T2a the question gate, and T3 the survival gate (and, through the unnamed source.md, part of exposure).

### T1 (refined). Searches stay inside the files the plan names

Cheap models check the files and lines the plan names. They never search outward from those files: no reverse-dependency sweep ("which tests and docs reference the files this plan edits?") and no inventory sweep ("the plan says *all*/*only*: list what it covers and count the exceptions").

**Complementarity refinement.** The missing capability has two halves, held by different cheap models, and no single cheap model has both. *Searching beyond the plan*: haiku searches `tests/` in 81% of runs and ember in 49%. *Opening and reading an unfamiliar file whole*: luna does a median of 11 Reads per run, and it opens what it is pointed at: it read source.md in 48 of 48 control runs, where the tasks cite source sections, against 11 of 48 alias runs, where they do not (`investigation-alias-control.md` §2). So sharing a searcher's output (paths seen) with a reader should turn some seen-but-unopened files into opened files. A static checklist cannot copy this, which is why slot 2 (F4) exists.

| Evidence | Number | Source |
|---|---|---|
| Unnamed files touched per run | sonnet 3.1, grok 1.2, haiku 0.9, ember 0.8, luna 0.3 | `BS/enrichment/investigation-patterns.md:41-49` |
| Runs that touched a test file the plan does not name | sonnet 35%, grok 33%, ember 8%, luna 1%, haiku 0% | same |
| `tests/skills/test_worker_contract.py` opened on the control package | 0 of 176 ember/luna/haiku runs; 7 of the 8 runs that opened it found I7, against 0 of the 225 that did not | `investigation-patterns.md:43-46, :132` |
| Search volume is not the variable | haiku searches `tests/` in 81% of runs (5.2 recursive searches per run), yet in 5 of 11 cheap control runs `test_worker_contract.py` showed up in its grep output and it never opened the file | `investigation-patterns.md:55`; `investigation-alias-control.md:66` |
| CHANGELOG never reached | `CHANGELOG.md` touched by 1 of 233 designSpec runs; I5 never found | `investigation-patterns.md:134` |
| Universal claim never counted | 44 of 98 cheap alias reviewers saw the already-narrowed `refs/tiers.md:42` and none compared it with Task 7's "all other primitives" (B8) | `investigation-alias-control.md:67` |
| The two halves sit in different models | haiku searches `tests/` in 81% of runs, ember in 49%; luna does a median of 11 Reads per run; luna read source.md in 48 of 48 control runs against 11 of 48 alias runs | `investigation-patterns.md:19, :31-33`; `investigation-alias-control.md` §2 |

Explains I7, I5, B8 and B6 (primarily) and supports I6.

### T2 (refined). The reviewer anchors the right place but checks it along one axis only (T2a), or never reaches the place (T2b)

Cheap reviewers anchor the right sentence, ask one local question about it, and stop. The refinement is that this is **not a thinking-budget ceiling**. Within ember and luna, hard-issue hits do not rise between the lower-thinking and higher-thinking halves of runs: ember goes from 0.25 to 0.22 per run and luna stays at 0.09. For haiku the same comparison does rise, from 0.29 to 0.70 (`investigation-patterns.md:149-151`). A second axis has to be asked for explicitly.

The theory splits in two, because the halves need different cures:

- **T2a, right place, one question.** The reviewer anchors the right sentence and asks one question. A peer can supply the place (its own anchor) and a different question (a move) without supplying a conclusion. Issues: B5, I1, I5, and B6 (framing).
- **T2b, the region is never reached.** No cheap finding anchors the acceptance criterion or the other task where the defect sits, even when the surrounding Task is anchored. A peer's anchor cannot point there, because no peer anchors it either; only a sentence-level prompt or a request for an uncovered region can. Issues: B1, B2, I4, I6. Attention is also duplicated: luna anchors control Task 12 in 91% of runs, and 34% of its control findings are one artifact-path objection.

| Part | Evidence | Number | Source |
|---|---|---|---|
| T2a | Right anchor, inverted question on I5 | 16 cheap findings anchor the I5 sentence; all 16 say the grep over-matches; none asks where else the claim lives | `investigation-designspec.md:103` |
| T2a | One branch traced on B5 | 3 cheap findings on the exact B5 mapping; all traced only the mode-off case, none the halt path | `investigation-designspec.md:105` |
| T2a | One question asked on I1 | 1 haiku finding on the exact I1 row, asking a different question | `investigation-designspec.md:106` |
| T2a | Wrong framing of the right observation (B6) | luna read the `chains.md` `/model` lines and graded them "unclear exemption"; credit depended on framing them as "goal against test scope" | `investigation-alias-control.md:102` |
| T2b | Stopping rule never tested (B1, B2) | ember anchors Task 1 of designSpec in 52% of runs, yet the unbounded-inventory issue is matched in about 3%; no finding in any panel anchors O3/AC3 | `investigation-patterns.md:111, :140`; `investigation-designspec.md:104` |
| T2b | AC grep never read literally (I4) | 0 cheap findings on the acceptance criterion; only sonnet, in 4 of 26 runs | `investigation-designspec.md:107, :124` |
| T2b | Check stops after one task (I6) | cheap reviewers found the sibling defect B7 (Task 6 against the Constraint) and never repeated the check on Task 7 or Task 3 | `investigation-alias-control.md:69` |

Explains B1, B2, I4, I6 (T2b) and B5, I1 (T2a) primarily, and supports I5 (T2a) and B6.

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

Explains B5, I1, I4 and B8 (masking), I5 and I7 (filtering). It is a confound for every measured number. Removing the leak (H4) changes 0 on /14 for cheap panels, which never found I7; it only lowers measured I7 for sonnet panels, on control /2.

<!-- Source: Variant 2 (opus:analyzer), V2:81-94 (per-issue gate table), with exposure cells corrected by Variant 5's T2b (V5:40) and a "redesigns targeting the blocked gate" column - merged per Change #2 -->
### Gate funnel: which gate blocks each missed issue

| Issue | Gate A: exposure | Gate B: question | Gate C: survival | Redesigns aimed at the blocked gate |
|---|---|---|---|---|
| B1 | **fails** at the criterion (T2b): Task 1 is anchored in 52% of ember and 92% of haiku designSpec runs, AC3/O3 never | **fails**: no stopping-rule question | rubric favours "wrong build" | F7 (card on an unbounded criterion), F6; F1 only through the gap card (booked to P) |
| B2 | **fails** (T2b); needs source.md:341 | **fails**: task body scope against AC scope | source not opened (39% of ember runs; H1) | F7, F6; F1 gap card (P) |
| B5 | passes (T2a: 3 findings on the mapping); needs source.md:112 | **fails**: one input case only | **fails**: checkout repaired (H3) | F1, F7, F6 |
| B6 | passes: in the plan and `chains.md` | **fails**: framing | none | F4, F1, F3 (ember M2) |
| B8 | **fails**: no inventory of `model:` lines | partial | **fails**: `tiers.md:42` narrowed (H3) | F4 (count fact), F3 (ember M2), F1, F6 |
| I1 | passes in part (1 finding on the row); needs the source.md:200 against :206 table pair | **fails** | **fails**: checkout repaired (H3) | F1, F7, F6 |
| I4 | **fails** at the criterion (T2b): 0 cheap findings on Task 12 AC1 | **fails**: no literal reading | **fails**: the repaired heading passes (H3) | F7, F3 (ember M4), F6; F1 gap card (P) |
| I5 | **fails**: root files never searched (`CHANGELOG.md` touched in 1 of 233 runs) | **fails**: wrong direction (T2a, 16 anchors) | **fails**: "minor" drop | F4, F3 (ember M7), F1, F6 |
| I6 | **fails** (T2b): the check is never carried to Tasks 3 and 7 | **fails**: no propagation | none | F1 (`contradiction` -> M8 row), F7 |
| I7 (control) | **fails**: unnamed test file | needs a missing-task framing | Medium grade; the leak inflates other panels (H4) | F4, F3 (ember M1), F6 (control /2) |

The survival gate is closed only by the harness fixes H1-H4, never by collaboration; that is why every gain block reports H separately from C.

### Mapping of the ten missed issues to the theories

| Issue | Primary theory | Secondary | Generic move that finds it (catalogue id, section 2.0) |
|---|---|---|---|
| B1 (designSpec Task 1 AC3, unbounded "every") | T2b | T3b (rubric steers toward wrong builds) | M3 stopping rule |
| B2 (designSpec Task 1 scope against AC) | T2b | T3a (source.md skipped) | M9 scope compare |
| B5 (designSpec exit-report mapping after halts) | T2a | T3a (repaired ref) | M5 branch trace |
| B6 (alias aliases-only goal against test scope) | T1 | T2a (framing) | M10 claim against enforcing test |
| B8 (alias "all other primitives use aliases") | T1 | T3a (repaired tiers.md) | M2 universal-claim count |
| I1 (designSpec fold rows against the status mapping) | T2a | T3a (repaired code) | M6 producer/consumer against source.md |
| I4 (designSpec heading against case-sensitive grep) | T2b | T3a (repaired heading passes) | M4 literal AC check |
| I5 (designSpec stale "43 members" in CHANGELOG) | T1 | T2a, T3b (dropped as minor) | M7 other-direction sweep |
| I6 (alias user-guide text drops a constraint clause) | T2b | none | M8 constraint sweep across tasks |
| I7 (control: worker-contract test never updated) | T1 | T3b (missing task = Medium), leak | M1 reverse-dependency sweep |

---

<!-- Source: Base (original) -->
## 2. Five redesigns

### 2.0 Shared building blocks (used by several designs)

<!-- Source: Base (original, modified) - two columns added per Change #9 (observable signatures: INV-007 at debate/round3-V1.md:31 and debate/round3-V2.md:23; c ceilings: Variant 5 (sonnet:performance), V5:83-94, mapped to V4 ids; A-011) -->
**Move catalogue (frozen, generic).** These ten investigative moves come from the "needed move" columns of both missed-issue investigations, reworded so that none names a package, task number, file from ground truth, or ground-truth quote. They are the only instruction text a message may carry.

| Id | Move (text sent to a reviewer) | Style that runs it best | Observable tool-call signature (F3 classifier) | c ceiling (V5 move) |
|---|---|---|---|---|
| M1 | For each file the plan edits, search `tests/`, `docs/` and the repo root for its path or key strings; open every test file the plan never names. | search (ember, haiku, sonnet) | a recursive `grep` over `tests/` whose pattern is a path or key string of a plan-edited file | 0.215 (G7; shares I5 with M7) |
| M2 | For each sentence that says all, only, every or none, list what it quantifies over and count the exceptions. | search | a Bash command that lists or counts matches across a directory (`grep -l`, `grep -c`, `find`, or a listing piped to `wc -l`) | 0.185 (G6) |
| M3 | For each acceptance criterion that says every, all or complete, state the finite check that proves it; if none exists, say so. | reading (luna, haiku) | unobservable | 0.050 (G1) |
| M4 | For each grep or command criterion, run it against the exact text the task tells the implementer to write, not the current file. | either | a Bash `grep` whose pattern string equals the pattern of a grep or command criterion quoted in the candidate | 0.200 (G5) |
| M5 | For each mapping or decision rule, trace every input value (each reason, each mode) through to its output. | reading | unobservable | 0.125 (G3) |
| M6 | For each value a consumer reads, find the producer row that writes it, in the source document, not the checkout. | reading | unobservable | 0.075 (G4) |
| M7 | When you checked a claim is not too broad, check the other direction: where else in the repository (root files included) is the same claim stated? | search | a repo-wide search from the repository root that includes root files (for example a recursive `grep` from `.` or a search naming a root-level file) | 0.140 (G8, shared with M8) |
| M8 | When a check fails for one task, apply the same check, clause by clause, to every other task. | reading | unobservable | 0.140 (G8, shared with M7) |
| M9 | Compare each task body's scope with its acceptance criterion's scope and with the source document's scope. | reading | unobservable | 0.050 (G2) |
| M10 | When the plan says a test enforces a rule, list what that test can actually fail on. | either | unobservable | none (V5 has no matching move) |

Two further checks are observable but are not moves: **source.md opened** (a Read of the package's source.md) and **unnamed test opened** (a Read of a test file not in the candidate's file list).

Rules for the last two columns:

- A move marked **unobservable** leaves no tool-call trace. It is never described as "not done by any panel member"; a message that sends it is a timed prompt, and its effect is booked to P.
- **c** is V5's chance that a cheap model which carries out the move on the right region writes a finding the blind judge credits, set at about half a sonnet-level chance. Over V5's eight moves c sums to 1.04, about SL2's measured hard reach per run, so it is a **reference ceiling, not a forecast**. It does not bound the gain rows in this specification: several high ends exceed a move's c, in every redesign that has such rows. Examples: F3's luna prompting rows (B5 0.15 against M5's 0.125, I1 0.10 against M6's 0.075); F4, F6 and F7 rows whose route delivers a located fact, a card or a request (F7's B1 0.16 against M3's 0.050); and F6's sonnet receiver (total high end 1.06 against the 1.04 sum). Every gain row is a planning value and is replaced by the arm's measured reach.
- For the never-found issues (B1, B2, I5, I6) no cheap-model rate exists. A gain row for them has low end 0 when its route is a prompt or an anchor-borne move; rows whose route delivers a located fact or a direct request (F4's I5 row, F6's rows) keep their planning low ends and are labelled planning.

<!-- Source: Base (original, modified) - message rules per Change #5 (Variant 2 (opus:analyzer), V2:116-131 located-quote and forbidden-key rules, X-007; INV-005 clause (1) of debate/round3-V2.md:21 as the only exception) -->
**Message schema `panel-msg/1`.** One JSON object per line. Serialised size is at most 600 bytes, and the reader rejects longer lines.

```json
{"v":"panel-msg/1","id":"m-r2-03","run":"<row>/<pkg>","from":"t4-1","to":"t3-1|*","t":1731500000123,
 "kind":"move|fact|challenge|card|coverage","move":"M1",
 "anchor":"<optional: 12-200 chars copied exactly from candidate.md>",
 "items":["<optional: up to 8 repo paths or path:line>"],"n":0}
```

Validation rules (R-06, R-08):

- **No free text in any message kind.** The forbidden keys are `claim`, `verdict`, `blocking`, `severity`, `category`, `note` and any key not in the schema above. The validator drops any line that contains one, and the line is never delivered. A message can therefore point (move, anchor, paths, count) but cannot conclude.
- **Located content only.** An `anchor` must be an exact substring of `candidate.md` (after whitespace flattening), 12-200 characters. Every entry in `items` must be a repository-relative path (optionally `:line`) that exists in the sandbox, except in `kind:"coverage"` lines (Redesign 5), whose `items` are Task ids of the candidate (`"T9"`), checked against the candidate's Task list.
- **The only exception (F7 cards).** A `kind:"card"` line posted by ember in Redesign 4 may also carry `category` and `severity`, and only as enum values of findings-v1 (never `claim`, never `blocking`). This is what lets F7 render a card in "finding form" without free text (Redesign 4).
- **Caps.** A card past ember's cap of 2k cards per package is rejected and logged `over_cap`.

<!-- Source: Base (original, modified) - writing, reading and seal rules per Change #6 (seal at V4:122, :286; fail closed on the seal and fail open on the review at debate/round2-V4.md:73-74; INV-012 at debate/round3-V1.md:39; INV-031) -->
**Board substrate (the transport for Redesigns 1, 2, 4 and 5).**

- **Location.** The harness creates `$BOARD/<row>/<pkg>/` outside the sandbox repo.
- **Writing.** Model-authored lines (ember's F7 cards, the F4 sweeper's facts) go only through one Bash helper on `PATH`, `panel-post`, which appends one validated line to `msgs/<rid>.jsonl` with an atomic write. Harness-authored lines (F3 injections, F6 requests, F1 digests) are written by the harness, not by a model.
- **Reading.** A `PostToolUse` hook prints new peer lines as `additionalContext`, capped at 1,500 characters per call. No design uses a `Stop` hold: a reviewer never waits for a peer, and an item that arrives after the receiver's last tool call is logged `late` and dropped (the package then counts as isolated for that reviewer).
- **Configuration.** Hooks are passed per reviewer with `--settings '<json>'`. The absolute board path and the reviewer id are written into the hook command string, so nothing depends on environment-variable inheritance, which is UNVERIFIED (`BS/enrichment/research-light.md:205-207`).
- **Why the board was chosen.** It delivers the same way for every model because delivery happens on the CLI side, not by the model calling a tool. It is durable, it is its own audit log, and it needs about 100 lines of bash (`research-light.md:157-207`).

**Independence: seals and peer tagging.**

- **Phase designs (F1) seal by process exit.** The phase-1 report exists as a file when the process exits, after its H2 re-ask; no model compliance is needed.
- **Mid-run designs (F3, F4, F6, F7) seal by a hook-side snapshot.** Immediately before the first delivery to a reviewer, the hook writes a snapshot of that reviewer's transcript under `$BOARD`, and the harness records its sha256 in `collab.json`. The seal fails closed and the review fails open: if the snapshot or its hash fails, the hook delivers nothing to that reviewer and logs `snapshot_missing`, and a hook error never kills a review (R-22). The snapshot seals a partial first pass (luna writes one findings block at the end), so mid-run C is measured at arm level only.
- **Mechanical peer tag.** In mid-run arms the harness tags a findings line `"origin":"peer"` when its anchor overlaps a delivered anchor by at least 12 characters, or when a delivered locator is in its refs, whatever the model wrote. Phase-2 lines in F1 are tagged `peer` by the combiner. All other lines are `"origin":"own"`.
- **What is not used.** Alarms built on "a reviewer's own sealed findings per run" cannot be computed from a transcript snapshot and are not used. The test "the snapshot timestamp precedes the first peer line" is kept as an integrity log only, because the same hook writes both.

<!-- Source: Base (original, modified) - shared convergence alarm per Change #7 (V4:234 and R-25 relative alarm; INV-004 text of debate/round3-V1.md:28; guard of debate/round2-V2.md:148; INV-018 at debate/round3-V1.md:41) -->
**Convergence alarm (shared by every design, computed without ground truth, R-25).**

- **CONVERGENCE (own-line rule).** For each run, compute the mean pairwise Jaccard of the Task sets anchored by the reviewers, using `origin:"own"` lines only: phase-1 or pre-delivery findings, excluding P2-F lines and peer-tagged lines (logged as `own_line_jaccard`). The alarm fires when an arm's mean exceeds the A1 mean by more than 0.15 (isolated references: ember+luna 0.25 and luna+luna 0.33, `investigation-patterns.md:81-82`, so roughly above 0.40 and 0.48), or when the panel's ledger row count falls more than 20% below A1. `pairwise_task_jaccard` over all lines is still logged, as a descriptive figure only.
- **Independence guard.** An arm passes if CONVERGENCE fires in at most 2 of its 12 runs. In F1 own lines are sealed by process exit, so the alarm should fire at A1's rate; a higher rate is an integrity failure, not a design effect.
- **ECHO (per design, real-anchor slots only).** The share of receiver findings that restate the content of the slot they came from. Thresholds: above 30% in F1 (phase-2 claims against the peer's claim on the same anchor), above 60% in F4 (luna's peer-tagged findings whose anchor equals a fact's anchor). Gap-card and decoy slots are excluded because they have no peer claim.
- **Overlap alarm in F7.** `flag_finding_overlap` (the share of ember's cards whose anchor equals an anchor in ember's own final findings) above 50% **stops the arm and is reported**; it never changes the treatment partway through an arm.

<!-- Source: Base (original) -->
**Transports rejected for every design.**

| Transport | Why rejected |
|---|---|
| Orca mail | No per-reviewer mailbox for bash-launched `claude -p`; would need a `worker-start` rewrite. |
| A2A | No way to inject into a running turn; needs a server per reviewer. |
| Claude Code cross-session messaging | No durable audit file. Whether gateway models call `SendMessage` correctly is unverified. Behaviour after a `-p` session's last turn is unverified. `ListAgents` shows every session on the host (`research-light.md:115-123`). |

Cross-session messaging stays a spike-gated fallback for design 4 only.

**Reviewers stay read-only.** `--disallowedTools Edit Write NotebookEdit` is unchanged. The `panel-post` helper and the hooks (including the transcript snapshots) write only under `$BOARD`, outside `/tmp/evalsb/repo` and outside the candidate. Because Bash is unrestricted, this is enforced by audit (section 5.5).

<!-- Source: Base (original, modified) - kill switch per Change #19 (debate/round3-V4.md:57-63) -->
**Kill switch.** With `PANEL_COLLAB=0`, the harness passes no hooks, no helpers and no phase 2. It restores the isolated panel **with the harness fixes** (arm A1), not today's `RR` exactly: the launch command differs from `RR:48` only by R-01 and R-03, the removal of `--no-session-persistence`, stream-json on re-ask sessions and the common hang guard (R-05).

<!-- Source: Base (original, modified) - timing constants and baseline tables replaced by the panel timing rules per Change #8 (INV-001 and INV-008 text of debate/round3-V1.md:25, :32 with round3-V2.md:24 thresholds; round2-V1.md:139-147; round2-V2.md:176-187; round2-V3.md:162-168; round2-V4.md:104-109; round3-V4.md:24, :31; V5:411; round3-agenda.md:11-16) -->
**Timing constants.** Median wall time divided by median turns gives the time per turn:

| Model | Median wall | Median turns | Seconds per turn |
|---|---|---|---|
| ember | 41 s | 13 | 3.2 |
| luna | 102 s | 16 | 6.4 |
| haiku | 233 s | 10 | 23 |
| sonnet | 228 s | 16 | 14 |

Source: `investigation-patterns.md:19-23`. One move costs about 2 turns. A resumed `claude -p` start costs about 6 s and a fresh-session fallback about 16 s (both UNVERIFIED; measured in spikes S0 and S2). Hooks cost about 2 s per package (about 16 calls x 0.1 s, UNVERIFIED). These are medians; the rules below use the 90th percentiles turn_p90 and T_report_p90, which Spike 4 measures.

**Named isolated baselines per package.** Planning values are `CR` elapsed over 3 packages divided by 3. The slowest luna sets B on EL2. The per-package medians beside them were measured from historical runs without the harness fixes (`round3-agenda.md:11-16`, slowest reviewer per package-run); A1 carries the fixes and may be slower. The cap is checked per package against the measured A1 median B_A1, never against these planning values (R-24).

| Name | Panel | Planning B | Phase-2 deadline 1.30 B | +35% cap 1.35 B | Hang guard 1.5 B | Output tokens per package | designSpec median (min-max) | alias median (min-max) | control median (min-max) |
|---|---|---|---|---|---|---|---|---|---|
| EL2 | ember + 2x luna (S07) | 116 s (348/3) | 150.8 s | 156.6 s | 174 s | 21.2k | 100 s (92-123) | 120 s (98-171) | 122 s (86-155) |
| HL2 | haiku + 2x luna (S24) | 238 s (715/3) | 309.4 s | 321.3 s | 357 s | 63.7k | 220 s (159-305) | 238 s (230-285) | 226 s (163-297) |
| SL2 | sonnet + 2x luna | 273.7 s (821/3) | 355.8 s | 369.5 s | 410.6 s | 46.4k | 259 s (196-283) | 302 s (208-416) | 269 s (184-440) |

Sources: `CR:319, :331` and the seed brief's baselines (`seed-brief.md:25`); SL2 tokens 139,113/3 (V5:29). Spread inside one package (alias 98-171 s on EL2) is larger than any design's added time, so a single run is never compared with a planning number; per-package medians over an arm are.

**Panel timing rules (all designs).**

1. **Finish signal.** `PANEL_FINISH_AT = T0 + 1.35 B_f - turn_p90 - T_report_p90`. After it, the hook injects "finish now with what you have", no further item is delivered and the helpers refuse to post. At planning values (B = 116 s, turn and report 6.4 s) it is T0 + 143.8 s. The finish-signal bound is PANEL_FINISH_AT + turn_p90 + T_report_p90 = T0 + 1.35 B_f (156.6 s at B = 116 s): a reviewer that acts on "finish now" within one turn ends by then at p90.
2. **Count per receiver.** `k = max(0, min(2, floor((0.35 B_A1(pkg) - hooks - turn_p90 - T_report_p90) / (2 x turn_p90))))`, with hooks = 2 s. This equals floor((PANEL_FINISH_AT - T0 - B - hooks) / (2 x turn_p90)), so the planned end B + hooks + 2k x turn_p90 is at or under PANEL_FINISH_AT by construction and the signal never fires on the planned path. F6 uses the same rule with SL2's B and sonnet's turns. A package with k = 0 counts as isolated for that design, and that dilution is reported. Thresholds (hooks = 2 s, turn 6.4 s for luna, 14 s for sonnet):

   | Case | k = 2 needs T_report_p90 at most | k >= 1 needs T_report_p90 at most |
   |---|---|---|
   | EL2, B = 116 s (planning) | 6.6 s | 19.4 s |
   | EL2, B = 120 s (alias median) | 8.0 s | 20.8 s |
   | EL2, B = 122 s (control median) | 8.7 s | 21.5 s |
   | EL2, B = 100 s (designSpec median) | 1.0 s (so k = 2 is impossible there) | 13.8 s |
   | SL2, B = 273.7 s (F6, sonnet turn 14 s) | 23.8 s | 51.8 s |

   Worked values: B = 116 s with 6.4/6.4 gives k = floor(25.8/12.8) = 2 (planned end 143.6 s, at or under 143.8 s); with T_report_p90 = 11.0 s, k = floor(21.2/12.8) = 1 (planned end 130.8 s); B = 90 s gives k = 1. Because k = 2 needs luna's output-heavy final turn at p90 to be no longer than about one mean turn, **k = 1 is the central planning row and k = 2 the optimistic one**. Both are planning values that Spike 4's per-package k replaces.
3. **Three numbers for every mid-run design (F3, F4, F6, F7).** Each design states (i) the planned end, B + hooks + 2k x turn_p90; (ii) the finish-signal bound, T0 + 1.35 B_f; (iii) the enforced ceiling, a hang guard at T0 + 1.5 B_A1 whose firing kills the reviewer and counts as `SLO_BREACH` (174 s on EL2 at planning B; 410.6 s on SL2).
4. **What is enforced and what is audited.** For slots 2-5 (F4, F3, F6, F7) the +35% cap is **audited by the SLO budget (R-24), not enforced**: a design whose reviewers ignore "finish now" is caught by the error budget (1 package in 12 per arm) and, beyond 1.5 B_A1, by the hang guard. Only F1's phase-2 end is enforced by a process kill, at the phase-2 deadline T0 + 1.30 B_A1 (150.8 s on EL2 at planning B). No "worst" figure in this specification is a cap guarantee for F3, F4, F6 or F7.
5. **Baseline rule (five parts, with the per-slot slowdown and drift corrections).**
   - (a) The named baseline is B_A1, the per-package median of A1. Historical planning values appear only in arithmetic, labelled as planning, and every block is written as a formula in B so it rescales.
   - (b) In-run deadlines (PANEL_FINISH_AT, the phase-2 deadline, the hang guard) use the frozen B_f; the after-the-fact cap check uses the concurrent median B_c.
   - (c) The catalogue's own time counts against a design. Each design's ex-ante budget is B_A1 x (1 + s) + W, where s is the Spike-4 slowdown of that design's brief over A1, **measured on the critical-path role** (the reviewer that sets B, normally the slowest luna; in F4 the extra brief text goes to the sweeper and in F7 mostly to ember, both off the path). Per-slot limits s <= (0.35 B - W) / B, with W the slot's additive planning cost: F4 and F7 5.7% (W = 34 s, which includes one 6.4 s turn of slip), F3 11.2% (W = 27.6 s), F6 13.8% (W = 58 s = hooks 2 s + 4 x 14 s, the k = 2 additive cost, computed at B = 273.7 s: (95.8 - 58) / 273.7). For F1 the deadline is absolute, so the cap always holds, but at s >= 13.8% luna B starts at or after 132.0 s and gets n = 0. If a budget exceeds 1.35 B_A1, the design drops brief content until it fits. The full static kit alone is priced at about +29% elapsed (V5:411, UNVERIFIED).
   - (d) Cap check: per package, median elapsed at most 1.35 B_A1, and no package above 1.5 B_A1.
   - (e) Mid-run designs cannot be killed without losing the report; their bound is the count k plus the finish signal, and the SLO budget audits it.
   - Drift band: log `baseline_drift = B_c / B_f` per randomised block. Its lower edge is 1.30/1.35 = 0.963, below which F1's phase-2 deadline no longer sits under 1.35 B_c; the upper edge is 1.10. Package results from a block outside [0.963, 1.10] are reported but not used for the time verdict.
6. **Values file.** Spike 4 writes one values file per package (B_A1, turn_p90, T_report_p90, PANEL_FINISH_AT, k). It is committed with its sha256 before the first arm (R-30) and is never recomputed during an arm; drift is handled by the band above, not by changing k.
7. **Counterfactual truncation.** A1 and A2 log `finish_would_fire` (luna still running at PANEL_FINISH_AT, which A1 and A2 do not act on). The truncation rate in design arms is compared with it, not assumed equal.
8. **Baked settings.** T0, PANEL_FINISH_AT, the absolute board path and the reviewer id are written into each reviewer's `--settings` JSON hook commands. Hooks read nothing from the environment (R-21).
9. **Labelling.** Every "+x%" figure in this specification is valid only at its stated B and k (or n); Spike 4's values replace it.

<!-- Source: Base (original, modified) - harness bundle rewritten per Change #3 (Variant 1 (opus:architect), V1:102-111; INV-002 text of debate/round3-V1.md:26; INV-009, INV-010 at round3-V1.md:36-37; retry loop and hang guard at debate/round3-V4.md:42-47) -->
**Harness fixes H1-H4 (every arm except A0, including the isolated control A1).**

| Id | Fix | Removes |
|---|---|---|
| H1 | Name the absolute path of the package's source.md in the brief, next to the candidate path, and ask the reviewer to read both. | Source-blind runs (T3a) |
| H2 | Before the merge, truncate `anchor` and `anchor2` to 200 characters and `claim` to 300 (a prefix of an exact quote is still an exact quote). Validate the block with the real findings parser at run time. If any line would still be dropped, re-ask the reviewer once through `claude -p --resume`, and record the result. | The merge drop (T3b) |
| H3 | Review each package in a sandbox built from the commit the plan was written against (the parent of its first implementing commit), recorded in the manifest. | Masking by repaired code (T3a) |
| H4 | Remove `.dev/reflect/` (and the other leak directories listed in R-03) from every sandbox. | The I7 leak |

The grading rule (an unstated requirement is graded Medium) and the blind judge are **held constant** in every arm, sha256-pinned, so the experiment never mixes a rubric change with collaboration.

Rules that make H2 and the run lifecycle fit inside every time bound:

- **One phase-2 deadline.** In F1, one wall-clock deadline, T0 + 1.30 B_A1, covers every process that can write phase-2 lines: the resume or fresh fallback, the challenges and any H2 re-ask. A re-ask that cannot start with one start plus one turn left before the deadline is skipped; the invalid phase-2 lines are dropped and phase 1 stands. "Hard bound" in this specification always means this **phase-2** bound; panel elapsed is at most max(T1, T0 + 1.30 B_A1), where T1 is the slowest phase-1 end.
- **Re-ask accounting.** In A1 and in every design arm the H2 re-ask is logged as `reask_s`, and the cap check uses measured elapsed time that includes it.
- **Session persistence.** Every arm, A1 included, drops `--no-session-persistence` (`RR:48`), because every arm may re-ask through `--resume`.
- **Phase-1 seal after the re-ask.** The phase-1 H2 re-ask finishes before the seal. `<rid>.p1.md` is the post-re-ask phase-1 report; it is hashed at that point and used for sealed-report judging.
- **Retry loop.** `RR:61-64` re-runs a whole review on attempt 2 when the block or the model check fails, and `NOFALLBACK=1` does not disable it. `elapsed_s` sums all attempts, and `attempts` and `retry_s` are logged. In a collaboration arm, attempt 2 runs with `PANEL_COLLAB=0` for that reviewer, and the package counts as isolated for it (`retry_isolated`), so hooks never deliver twice.
- **Common hang guard.** Every arm, A1 included, kills a reviewer at T0 + 1.5 B_A1 and logs `hang_kill` (today A1 would keep `timeout 3000`, which would kill slow runs only in the design arms). On historical EL2 data the guard rarely binds: the largest alias run was 171 s against 1.5 x 120 = 180 s.

<!-- Source: Variant 5 (sonnet:performance), V5:141-153 (three shares, bottom-up H table) and V5:106, :433 (Spike 5) - merged per Change #4; H-C interaction kept from Base (V4:184) -->
**Three shares: H, P and C.** Every gain in this specification is split into three shares, each measured by one arm difference:

| Share | Definition | Measured by | What it contains |
|---|---|---|---|
| H (harness) | A1 - A0 | arm A1 against the fresh arm A0 | the effect of H1-H4 alone |
| P (prompting) | A2 - A1 | arm A2 (static move kit) against A1 | the effect of telling reviewers the moves, with no exchange. Gap-card findings in F1 and luna's injections in F3 are booked here. |
| C (collaboration) | design arm - A2 | each design arm against A2 | the effect of the exchange itself |

C is conditional on H: every collaboration estimate **assumes H is applied in both arms**, and H and C interact (moves M4 and M6 only pay off once H1 and H3 hold). Every gain block below therefore shows C and H in **separate columns and never sums them**.

Bottom-up H for the cheap panels, out of 14 per run (V5:147-151):

| Fix | Mechanism and assumption | Central | Low-high |
|---|---|---|---|
| H3 pre-implementation checkout | removes false reassurance on B5, I1, I4 and B8 and the "feature already exists" distraction findings; +0.02 on each of 4 issues | +0.08 | 0.02-0.16 |
| H1 source.md named in the brief | the 39% of ember and 22% of luna runs that never read it become readers; B5, I1 and B2 need the source | +0.03 | 0.01-0.08 |
| H2 anchor and claim normalizer | 92 findings dropped over 264 merges, 49 of them blocking; assume 2% match a not-yet-found hard issue | +0.03 | 0.00-0.10 |
| H4 remove `.dev/reflect` | does nothing for cheap panels (I7 is 0 in 30 runs); lowers measured I7 for sonnet panels by about 2 of 9 credits, a measurement correction reported on control /2 | 0 | 0 |
| **Total (cheap panels, EL2)** | | **+0.14** | **0.03-0.34** |

For SL2 no bottom-up table exists; its H share is carried as +0.1 to +0.4 per run, UNVERIFIED. Spike 5 re-scores the raw findings of the 30 cheap historical runs with the normalizer (judge calls only) and replaces the H2 row with a measured value.

<!-- Source: Variant 1 (opus:architect), V1:614 (REQ-S3) - act-rate rule merged per Change #20 (A-001) -->
**Act rates are planning values.** Every gain chain in section 2 multiplies by an act rate: the chance that a gateway model acts on an injected or delivered item (0.5-0.85 across the designs). No measurement supports these numbers. Each is labelled planning in its (f) block and is replaced by the act rate that spike REQ-S3 measures (section 4), including the act rate on "finish now", before any result is compared with a gain range (R-47).

---

<!-- Source: Variant 1 (opus:architect), debate/round3-V1.md:30 (distinctness triple, INV-006) and Variant 2 (opus:analyzer), debate/round3-V2.md:22 (move-only F3); F5 eviction from debate/round2-V4.md:32 - merged per Change #10 -->
### 2.1 Slate and distinctness criterion

**Criterion, stated once.** Each slot is a triple (content source, content form, delivery point). Two slots are distinct when they differ in at least 2 of the 3. The content sources are: harness-from-telemetry, harness-from-finished-findings, a dedicated helper session, and a reviewing peer.

| Slot | Family | Redesign | Content source | Content form | Delivery point |
|---|---|---|---|---|---|
| 1 | F1 | Redesign 3 Axis-Flip Challenge | finished findings | peer anchor + move | between phases |
| 2 | F4 | Redesign 2 Idle-Shift Sweeper | helper session | repo facts | mid-run |
| 3 | F3 | Redesign 1 Move Radar | telemetry | move name only | mid-run |
| 4 | F6 | Redesign 5 Coverage Deflection | finished findings | uncovered-Task requests | mid-run |
| 5 | F7 | Redesign 4 Flag-and-Adjudicate | reviewing peer | flagged sentence + finite check | mid-run |

**Pairwise check.** Every pair differs in at least 2 of the 3. The closest pairs are F1/F6 (form and delivery differ), F3/F6 (source and form differ) and F4/F7 (source and form differ). F3/F6 holds only because F3's injection names a **move only**, plus a Task only when the triggering tool call's path names one; if F3 named Tasks, F3 and F6 would share the form "move + Task" and differ in source alone (1 of 3).

**Families not in the slate.**

- **F5 (structural index / source-rule witness)** = (helper session, facts, mid-run), which differs from F4 in 0 of 3. Its mechanism is F4's (a searcher posts facts and a reader acts on them). Its target, the source-only rules B5, I1 and B2, survives as the witness sweep kind inside F4.
- **F2 (mid-run method relay)** = (reviewing peer, anchor or ref + move, mid-run), which differs from F7 in at most 1 of 3, so it cannot replace F6. I6, which F2 targeted, keeps a route through F1's `contradiction` -> M8 routing row.

---

<!-- Source: Base (original, modified) - Redesign 1 (F3, slot 3) rewritten inside its (a)-(h) skeleton per Change #13 (INV-006 move-only rule of debate/round3-V2.md:22; INV-007 at debate/round3-V1.md:31; Variant 1 (opus:architect) per-receiver hash order V1:148-231; Variant 5 (sonnet:performance) skip rule only (round2-V4.md:82); Variant 3 (haiku:backend) leak check on variable fields V3:88; refactor-plan global decision 5) -->
### Redesign 1: Move Radar (slot 3, family F3 Content-free coverage steering: coverage gaps from tool-call telemetry; reviewers author no messages)

**(a) Mechanism and model roles.** A `PostToolUse` hook in every reviewer logs each tool call (tool name plus command or path) to the board. A deterministic classifier (jq and regex) maps tool calls to catalogue moves using only the observable signatures of the catalogue (section 2.0): M1 (recursive grep over `tests/` with a plan-edited path), M2 (a listing or count across a directory), M4 (a grep whose pattern equals a criterion's pattern), M7 (a repo-wide search including root files), plus the two checks "source.md opened" and "unnamed test opened". M3, M5, M6, M8, M9 and M10 are unobservable.

At fixed checkpoints the hook injects into a reviewer **one move**, chosen by that reviewer's style:

| Reviewer | Moves it receives | What the injection may say | Share it is booked to |
|---|---|---|---|
| ember (searcher) | observable search moves: M1, M2, M7, M4 | "no panel member has done this yet", which telemetry can check | C (collaboration) |
| any reviewer whose transcript shows no Read of source.md | "open source.md" | "source.md has not been opened" | C |
| luna x2 (readers) | reading moves: M3, M5, M6, M9, M8, M10 | the move text only. These moves are unobservable, so this is a **timed static prompt**, never "not done by any panel member" | P (prompting) |

**The injection names a move only.** When the triggering tool call's path names a Task, that Task is written to `metrics/<rid>.jsonl`, never into the message. This keeps F3 distinct from F6 (section 2.1). Each receiver gets its gap list in a different order, from a hash of the receiver id, so the two lunas do not get the same move. A move a peer has already covered is never presented as a reason to skip anything; the message carries no coverage at all.

No model writes anything. The "communication" is ember's observed work changing what ember is asked to do next and what the panel is told about source.md; with almost no luna search signatures, ember's "not done" mostly reflects ember's own history, so F3's collaboration share may be near 0. Arm A6 against A2 is read as **"telemetry-timed kit against static kit"**. Baseline: EL2, ember + 2x luna (planning B = 116 s; measured B_A1).

**(b) Communication schedule.**

| Item | Value |
|---|---|
| Triggers | the first k of these checkpoints: ember after tool calls 6 and 10; luna after tool calls 8 and 12. The "source.md never opened" check is delivered at a reviewer's first checkpoint and counts as one of its k injections (no Stop-time injection, so no unbudgeted turns). |
| Frequency | at most k injections per reviewer per package |
| Messages per reviewer | k received, 0 sent (telemetry is automatic) |
| Size cap | 300 characters per injection (one move text, plus "no panel member has done this yet" for an observable move) |
| Schema | `panel-msg/1` with `kind:"move"`, `from:"radar"`, `move`; no anchor, no items, no Task |
| Deadline guard | no injection after T0 + 1.35 B_A1 - 47 s (110 s at planning B), and none after PANEL_FINISH_AT |

**(c) Transport.** Board plus hooks. It is the only transport where the model takes no action at all, so it works the same for ember, luna and haiku.

**(d) Time budget (EL2, planning B = 116 s, turn_p90 = T_report_p90 = 6.4 s).**

| Reviewer | Baseline end | Added | New end |
|---|---|---|---|
| ember | 41 s | k moves x 2 turns x 3.2 s = 6.4 s (k = 1) or 12.8 s (k = 2) | 47.4 s or 53.8 s, off the critical path |
| luna (slowest), k = 1 (central) | 116 s | hooks 2 s + 1 move x 2 x 6.4 s = 14.8 s | **130.8 s (+12.8%)** |
| luna (slowest), k = 2 (optimistic) | 116 s | hooks 2 s + 2 moves x 2 x 6.4 s = 27.6 s | **143.6 s (+23.8%)** |

The three numbers (section 2.0, timing rule 3), the same as Redesign 2:

- **Planned end:** 130.8 s (+12.8%) at k = 1, or 143.6 s (+23.8%) at k = 2, both at or under PANEL_FINISH_AT = 143.8 s.
- **Finish-signal bound:** T0 + 1.35 B_f = 156.6 s (+35.0%).
- **Enforced ceiling:** the hang guard at T0 + 1.5 B_A1 = 174 s (+50%), counted as `SLO_BREACH`.

The +35% cap is **audited by the SLO budget (R-24), not enforced**. The count k caps the planned path, but nothing makes a reviewer stop on time, so no figure above is a worst-case guarantee. Idle time used: ember's idle window hosts its moves.

**(e) Contamination safeguards.**

- **Shared:** move ids only (observable ones checked as not yet done), and the "source.md not opened" check.
- **Withheld:** every finding, anchor, path, count and Task.
- **Independent first pass:** no injection before tool call 6 (ember) or 8 (luna), so each reviewer has formed its own plan first; the hook-side snapshot is written before the first injection (section 2.0, seals).
- **Blind-spot spread:** impossible by construction, because no peer content is sent and no region is ever shown as covered.
- **Leak check:** the only variable field is the move id, so the 12-character leak check reduces to a lookup: any injected line whose text is not a catalogue move or the source.md check is a hard failure.
- **Convergence alarm (measurable):** the shared own-line rule of section 2.0 (own-line Task Jaccard above the A1 mean + 0.15, that is above about 0.40 for ember+luna and 0.48 for luna+luna, or ledger rows down more than 20%; pass if it fires in at most 2 of 12 runs). Logged per package in `collab.json`.

**(f) Expected gain.** Assumption: an injected move is executed in 50-80% of cases (a planning act rate that REQ-S3's measured act rate replaces), and executing it reaches the defect at a rate between the cheap near-miss rate and sonnet's rate. C is re-derived from **ember's search-move rows only**; luna's reading-move rows are booked to P. The k = 1 rows halve every k = 2 row (a planning assumption, replaced by logged delivered-injection counts).

| Issue | Route | Gross row at k = 2 (low-high) | Gross row at k = 1 (low-high) | Share |
|---|---|---|---|---|
| I4 | M4 to ember (mechanical; ember runs it in seconds) | 0.05-0.20 | 0.025-0.10 | C |
| I5 | M7 to ember (may still be dropped as minor) | 0.02-0.10 | 0.01-0.05 | C |
| B8 | M2 to ember | 0.03-0.10 | 0.015-0.05 | C |
| B6 | M2 to ember | 0.02-0.08 | 0.01-0.04 | C |
| **Ember rows, gross** | | **0.12-0.48** | **0.06-0.24** | |
| **C /14, net of the static kit** (the kit also tells ember these moves, so the low end is 0) | | **0-0.48** | **0-0.24** | C |
| B1 / B2 | M3, M9 to luna (the rubric still pulls away) | 0-0.05 each | 0-0.025 each | P |
| B5 / I1 | M5, M6 to luna | 0.05-0.15 / 0.03-0.10 | 0.025-0.075 / 0.015-0.05 | P |
| I6 | M8 to luna | 0-0.05 | 0-0.025 | P |
| **P /14 (luna rows)** | | **0.08-0.40** | **0.04-0.20** | P |

| Share | k = 2 | k = 1 | Column rule |
|---|---|---|---|
| C /14 (EL2) | 0-0.48 | 0-0.24 | collaboration |
| P /14 (luna injections, timed static prompt) | 0.08-0.40 | 0.04-0.20 | prompting share; never added to C |
| H /14 (EL2) | 0.03-0.34 (central 0.14) | same | harness share; never added to C |
| I7 (control /2), M1 to ember | 0.10-0.40 | 0.05-0.20 | collaboration, reported on control |

**(g) Effort.**

| Component | Lines |
|---|---|
| Board substrate (helper, PostToolUse hook and snapshot, settings generator, `run-reviewer.sh` changes) | about 100 |
| `radar-classify.sh` (about 60), gap selector (about 40), catalogue JSON (about 30) | about 130 |
| **Total** | **about 230** |

Files: `EVAL/tools/run-reviewer.sh`, new `EVAL/tools/panel/`.

**(h) Failure modes and runbook.**

| Failure | Detection | Action |
|---|---|---|
| Classifier mislabels a move, so a done move is re-injected | `radar.jsonl` audit, spot-check | Fix the regex; the extra cost is at most k moves |
| The gaps are always the same moves | catalogue usage histogram | Expected; it measures panel blind spots, so report it |
| A reviewer ignores the injection | move executed: no (from telemetry, observable moves only) | Logged; the gain falls toward the static kit (A2) |
| An injection carries anything other than a move id or the source.md check | leak-check lookup | Hard failure: quarantine the package-run in place |
| Hook not firing on gateway models | `hook_calls = 0` in metrics | Spike S0 gate; with the kill switch the run is isolated |
| Project hooks in the sandbox's tracked `.claude/settings.json` also fire | S0 lists active hooks | Confirm there is no conflicting `additionalContext` |
| A luna ignores "finish now" and runs past the bound | `finish_signal_t` against the reviewer's end; `hang_kill` | Counts against the SLO error budget (R-24); beyond 1.5 B_A1 it is `SLO_BREACH` |

---

<!-- Source: Base (original, modified) - Redesign 2 (F4, slot 2) rewritten inside its (a)-(h) skeleton per Change #12 (debate/round2-V4.md:65-78; Variant 2 (opus:analyzer) disjoint ranked locators V2:151-216 and witness kind (round2-V4.md:19); Variant 1 (opus:architect) harvest V1-R2; Variant 5 (sonnet:performance) first-hand rule and 10% stop V5:299; INV-008; INV-015, INV-016 at debate/round3-V4.md:49 and debate/round3-V3.md:27) -->
### Redesign 2: Idle-Shift Sweeper (slot 2, family F4 Searcher-to-reader fact relay: ember's idle time becomes a search service for the luna reviewers)

**(a) Mechanism and model roles.** Ember finishes its normal review at about 41 s. Its report is sealed because the process exits. The harness then starts a **second ember session**, the sweeper, with a sweeper brief: run moves M1, M2 and M7 against the candidate and the repo, and post **facts only**: path lists, counts, and `path:line` hits, with no judgement. One fact place may hold a **witness** fact instead: a source.md line with no counterpart in the plan, or a source.md table pair whose reader and writer sit in different tables (moves M6 or M9), checked against source.md, never against the checkout. The sweeper never sees ember's report.

A `PostToolUse` hook also **harvests** paths that appear in the sweeper's own tool output (grep and ls results) but that no reviewer has opened, so a located fact can reach the board without the sweeper having to post it. Facts are ranked as locators: unnamed test files first, then root-level documents, then others.

The two luna reviewers are read-driven followers: they open every file they are told about (`investigation-alias-control.md:60`). They receive the facts through the hook, open the listed files, and decide for themselves. This pairs the one cheap model that searches with the one that reads deeply (T1 complementarity): luna runs 0.2 recursive searches per run, ember runs 3.7. Facts are dealt to the two lunas disjointly by the balanced online deal: fact i (board append order) goes to luna (i + r) mod 2, with r a seeded coin logged as `deal_r`. Each luna acts on at most k facts.

Two rules keep facts from acting as conclusions:

- **No clearance.** A count fact with n = 0 ("0 files break the 'all' sentence") is never delivered as a count; it is rendered only as the command to re-run.
- **First-hand evidence.** Every fact carries its command string. A fact may be cited in a finding only after the receiver's own transcript has re-run the command or opened the path. If more than 10% of receivers' re-runs disagree with the fact, the arm stops.

Baseline: EL2, ember + 2x luna (planning B = 116 s; measured B_A1).

**(b) Communication schedule.**

| Item | Value |
|---|---|
| Trigger 1 | ember review exits, then the sweeper starts (about t = 41 s; the actual start is logged) |
| Trigger 2 | the sweeper posts each fact as found, and the harvest hook adds located paths from its output |
| Trigger 3 (delivery) | luna's PostToolUse hook delivers only once luna has made 6 or more tool calls and the hook-side transcript snapshot has been written and hashed (section 2.0, seals). No seal turn is asked of luna. If the snapshot fails, nothing is delivered (`snapshot_missing`). |
| Frequency | the sweeper posts at most 2k facts (one place may be a witness fact); each luna receives and acts on at most k |
| Messages per reviewer | sweeper: at most 2k sent; each luna: at most k received, 0 sent |
| Size cap | 600 bytes per fact; at most 8 paths |
| Schema | `panel-msg/1` with `kind:"fact"`, `move` ∈ {M1, M2, M7} (M6 or M9 for a witness fact), `anchor` (the plan phrase swept), `items` (paths or path:line), `n` (count, never delivered when 0) |
| Sweeper timeout | the sweeper is killed at T0 + (PANEL_FINISH_AT - T0 - 2 x turn_p90), which is T0 + 131.0 s at planning values, so its last fact can still be acted on before the finish signal |
| Deadline guard | nothing is delivered after PANEL_FINISH_AT (T0 + 143.8 s at planning values); no Stop hold; a fact that arrives after luna's last tool call is logged `late` and dropped, and the package counts as isolated for that luna |

**(c) Transport.** Board plus hooks: facts must reach luna mid-run, the transport must work the same across models (delivery is CLI-side, and luna makes about 1 Bash call per run, so it could not be relied on to fetch), and the facts form an audit log. A between-phase digest would add a full luna phase after 116 s.

**(d) Time budget (EL2, planning B = 116 s, turn_p90 = T_report_p90 = 6.4 s).**

| Reviewer | Baseline end | Added | New end |
|---|---|---|---|
| ember review | 41 s | none | 41 s |
| ember sweeper | not run | starts at about 41 s; 6 s start plus 10 turns x 3.2 s = 38 s | 79 s, off the critical path (inside ember's idle time) |
| luna (slowest), k = 1 (central) | 116 s | hooks 2 s + 1 fact x 2 turns x 6.4 s = 14.8 s | **130.8 s (+12.8%)** |
| luna (slowest), k = 2 (optimistic) | 116 s | hooks 2 s + 2 facts x 2 x 6.4 s = 27.6 s | **143.6 s (+23.8%)** |

The three numbers (section 2.0, timing rule 3):

- **Planned end:** 130.8 s (+12.8%) at k = 1, or 143.6 s (+23.8%) at k = 2. Both are at or under PANEL_FINISH_AT = 143.8 s, so the finish signal does not fire on the planned path.
- **Finish-signal bound:** T0 + 1.35 B_f = 156.6 s (+35.0%), reached only if luna acts on "finish now" within one turn and writes its report within T_report_p90.
- **Enforced ceiling:** the hang guard at T0 + 1.5 B_A1 = 174 s (+50%); a kill counts as `SLO_BREACH`.

The +35% cap is **audited by the SLO budget (R-24), not enforced**. No figure above is a worst-case guarantee. Idle used: ember's idle window (41-79 s) hosts the sweep, so the sweep itself adds no elapsed time. All values are valid only at B = 116 s and the stated k.

**(e) Contamination safeguards.**

- **Shared:** repo facts (paths, counts, line hits) from generic moves, each with its command string.
- **Withheld:** ember's findings, severities, claims and verdict. The sweeper is a fresh session that has never seen ember's report, so ember's conclusions cannot leak through it. Zero counts are never shown as counts.
- **Independent first pass:** the hook-side transcript snapshot is written and hashed before any delivery (fail closed), and findings that overlap a delivered anchor by 12 or more characters or cite a delivered locator are tagged `"origin":"peer"` by the harness.
- **Blind-spot spread:** facts carry no framing, so ember's habit of asking whether a grep over-matches (the I5 inversion) cannot be passed on. A wrong sweep is caught by the first-hand rule: the receiver must re-run it, and more than 10% mismatches stops the arm.
- **Convergence alarm (measurable):** the shared own-line rule of section 2.0 (own-line Task Jaccard above the A1 mean + 0.15, or ledger rows down more than 20%; pass if it fires in at most 2 of 12 runs).
- **ECHO (real-anchor slots only):** the share of luna's peer-tagged findings whose anchor equals a fact's anchor; alarm above 60%. Some echo is the intended effect; total echo means luna stopped its own review.

**(f) Expected gain.** Chains of assumptions per issue, out of 14 per run, planning values. The k = 2 rows are the base rows with the lunas receiving disjoint facts; the k = 1 rows halve every row, because each luna receives one fact instead of two. That halving is a planning assumption, replaced by the arm's logged delivered-fact counts. Every act-rate factor (for example "luna opens a listed file 0.6-0.8") is a planning value that REQ-S3's measured act rate replaces.

| Issue | Chain of assumptions | C at k = 2 (low-high) | C at k = 1 (low-high) |
|---|---|---|---|
| I5 | sweep lists the CHANGELOG line 0.3-0.6 x luna reports and keeps it 0.2-0.4 | 0.06-0.24 | 0.03-0.12 |
| B8 | M2 count computed 0.3-0.5 x linked to the Task sentence 0.2-0.4 | 0.06-0.20 | 0.03-0.10 |
| B6 | | 0.02-0.08 | 0.01-0.04 |
| B5, I1, I4 (through the witness fact) | | 0-0.05 each | 0-0.025 each |
| B1, B2, I6 | | 0 | 0 |
| **C /14** | | **0.14-0.67** | **0.07-0.34** |

| Share | k = 2 | k = 1 | Column rule |
|---|---|---|---|
| C /14 (EL2) | 0.14-0.67 | 0.07-0.34 | collaboration |
| P | none booked | none booked | prompting share |
| H /14 (EL2) | 0.03-0.34 (central 0.14) | same | harness share; never added to C |
| I7 (control /2): the sweeper lists `test_worker_contract.py` 0.7-0.9 x the luna that receives it opens it 0.6-0.8 x finds and reports it 0.4-0.7 (7 of 8 openers found it, but luna reports blocker-grade only); one luna receives the file under the disjoint deal | 0.17-0.50 | 0.09-0.25 | collaboration, reported on control |

**(g) Effort.** Board substrate (about 100 lines), plus sweeper brief text (about 25), a launcher hook that starts the sweeper after ember's exit (about 15), a fact validator (about 25) and the hook-side snapshot in place of `panel-seal` (about 15). **Total about 180 lines.** Files: `run-reviewer.sh`, a row launcher, `EVAL/tools/panel/`.

**(h) Failure modes and runbook.**

| Failure | Detection | Action |
|---|---|---|
| Snapshot not written or not hashed | `snapshot_missing` rate (`SNAPSHOT` alarm above 50% of luna runs) | Nothing is delivered to that luna (fail closed); the package counts as isolated for it; fix the hook before continuing the arm |
| Sweeper floods trivial facts | facts per run equal to the cap, low luna uptake | Tighten the brief: only files outside the plan's named list |
| Facts arrive after luna finished | `first_delivery_t` later than luna's last tool call | Logged `late` and dropped; the package counts as isolated for that luna |
| A receiver cites a fact it never re-ran | first-hand audit of hard-issue credits | The credit does not count as first-hand; re-run mismatch above 10% stops the arm |
| Ember's A1 run ends late (H1 makes it read source.md), so the sweeper starts late | logged sweeper start | Fewer facts arrive before the sweeper timeout; reported as dilution, never compensated by extending the timeout |
| Wrong blockers rise (luna grades every fact blocking) | wrong blockers more than A1 + 1.0 | Fail the arm (section 4 guards) |
| Sweeper's ember session misrouted | `model_ok` check on the sweeper's meta | The same identity audit as reviewers |
| A luna hangs | `hang_kill` at T0 + 1.5 B_A1 | Counts as `SLO_BREACH` against the error budget (R-24) |

---

<!-- Source: Base (original, modified) - Redesign 3 (F1, slot 1) rewritten inside its (a)-(h) skeleton per Change #11 (debate/round2-V4.md:45-63; INV-003 text of debate/round3-V1.md:27; INV-004 balanced deal of debate/round3-V2.md:21(3); INV-013, INV-014, INV-022 at debate/round3-V1.md:40 and debate/round3-V3.md:26; Variant 2 (opus:analyzer) `contradiction` row (round2-V2.md:13) and sealed-report judging (V2:517); Variant 5 (sonnet:performance) shadow variant V5:350-392) -->
### Redesign 3: Axis-Flip Challenge (slot 1, family F1 Between-phase cross-examination: peers' anchors come back with an "other axis" move)

**(a) Mechanism and model roles.** Phase 1 is the isolated review of arm A1, unchanged. Its sealed report is the first pass: `<rid>.p1.md`, written after any phase-1 H2 re-ask and hashed at that point. When a reviewer finishes, the harness parses the findings-v1 blocks of the peers that have finished so far. It selects peer findings whose category is `unpassable-check`, `contradiction` or `missing-requirement`. Surface findings are skipped: claims matching artifact path, hash or line-number patterns, which make up 21-23% of ember and luna findings (`investigation-patterns.md:73`).

For each selected finding it sends **only the anchor**, never the claim, paired with an axis-flip move. The move depends on the anchor's content, with one override by category:

| Anchor contains | Move sent |
|---|---|
| every, all, complete, only | M3 or M2 |
| a command or grep | M4 and M7 |
| a mapping or table | M5 and M6 |
| a constraint | M8 |
| (any text) when the peer's category is `contradiction` | M8 across all tasks (the only remaining I6 route) |

This is the "right place, wrong question" fix (T2a): ember anchored the I5 sentence 15 times and the B5 mapping once, and in each case asked one question. A different model now asks a different question at the same place. Phase 2 resumes the reviewer's own session (`claude -p --resume <session_id> "<digest>"`) and returns an addendum. The harness then concatenates phase-1 and phase-2 findings lines into **one** findings-v1 block, with phase-2 ids renamed `P2-F1`… and tagged `"origin":"peer"`. The findings-v1 merge contract is unchanged.

**Gap card (decoy).** Each challenge slot holds a gap card instead of a peer anchor with probability 1/3, seeded per receiver. A gap card is a verbatim candidate quote from a region that matches the routing regex and that no peer anchored, rendered exactly like a peer-anchor challenge; the digest never says which kind a slot is. With 2 slots, P(no gap card) = 4/9 and P(both) = 1/9. A gap card is harness extraction, not collaboration, so findings from gap slots are booked to P. It is also the only route to the T2b issues B1, B2 and I4, whose criteria no cheap peer anchors. Gap cards are built only where an eligible never-anchored region exists.

Roles:

- **luna x2** receive reading flips on ember's anchors (ember produces 4.19 findings per run and anchors designSpec Task 1 in 52% of runs, Task 2 in 46%, Task 8 in 33%). Ember's qualifying anchors are dealt to the two lunas disjointly by the balanced online deal: anchor i (in ember's block order, i = 0, 1, ...) goes to luna (i + r) mod 2, where r is a seeded 0/1 coin per run, logged as `deal_r`.
- **ember** receives search flips on luna's anchors.

Baseline: EL2, ember + 2x luna (planning B = 116 s; measured B_A1).

**HL2 shadow variant (V5-D5, as written; not an arm in the first experiment).** On haiku + 2x luna, haiku stays an isolated canary and never receives a digest. When both lunas finish (about 116 s), the harness resumes each luna with a digest built from the other luna's findings, at most 8 turns each, inside haiku's still-running window: 116 + 6 + 4 x 12.8 = 173.2 s < 238 s, so elapsed is +0%. The harness never waits for phase 2 more than 15 s past the slowest phase-1 reviewer, so the worst case is 253 s (+6.3%). Its gain is not carried here; it must be re-derived before an HL2 arm is planned.

**(b) Communication schedule.**

| Item | Value |
|---|---|
| Trigger | each reviewer's phase-1 exit (after its H2 re-ask) |
| Contents | the digest holds anchors from every peer that has finished at that moment; ember waits for both lunas before its phase 2 |
| Frequency | exactly one digest per reviewer per package (one exchange) |
| Challenges per reviewer | n = max(0, min(cap, floor((box - start_cost) / (2 x turn_p90)))), with cap = 2 for luna and 3 for ember; box = min(35, T0 + 1.30 B_f - t_launch); start_cost = 6 s for a resume, 16 s for the fresh fallback. n is recomputed before each launch attempt, so a failed resume re-renders the digest with a new n. If n = 0 no phase 2 is launched and phase 1 stands. |
| Messages per reviewer | 1 digest received, 0 sent (the harness authors the digest) |
| Size cap | digest at most 1,800 characters (3 challenges x 600 bytes) |
| Schema | `panel-msg/1` lines with `kind:"challenge"`, `from:"<peer rid>"` (or the same value for a gap card), `anchor`, `move`; no items |
| Phase-2 deadline | one wall-clock deadline T0 + 1.30 B_A1 for resume or fallback, challenges and any phase-2 re-ask; the process is killed there |
| Zero anchors | if no peer anchor qualifies, the package behaves as isolated for real slots; gap cards are still dealt where an eligible region exists, and ECHO is "not applicable" |

**(c) Transport.** Between-phase digest (plain files, written to a temp file then moved into place, so the write is atomic). The reasons:

- The phase-1 seal comes free: the process exited, so no compliance is needed.
- No live channel and no hooks, which makes it the most deterministic design.
- The digest file is the audit log.
- It gives the strongest independence guarantee.

It requires dropping `--no-session-persistence` from `RR:48`, which every arm now does (section 2.0, harness rules), because `--resume` needs a stored session. Resume runs from the same cwd, `/tmp/evalsb/repo`. If resume fails for gateway models (UNVERIFIED, spike S2), phase 2 falls back to a fresh session given its own phase-1 report path plus the digest, with n recomputed for the 16 s start.

Phase-2 and re-ask sessions run with `--output-format stream-json --verbose`, written to file as they stream. Today's command uses `--output-format json` (`RR:48`), which writes one result object only at exit (`RR:50`), so a killed process would leave nothing to salvage. The brief asks for one complete findings line after each challenge, and on a kill the combiner keeps every complete, parser-valid phase-2 line already streamed. The same `select(.type=="result")` filter works on stream-json read with `jq -s`. Spike S2 checks on luna that text streams before exit.

**(d) Time budget (EL2, planning B = 116 s; phase-2 deadline T0 + 1.30 B_A1 = 150.8 s).**

| Reviewer | Phase 1 end | Phase 2 (box, n) | New end |
|---|---|---|---|
| luna A (first finisher, about 95 s) | 95 s | box 35 s, n = 2: 6 s resume plus 2 x 2 x 6.4 s = 31.6 s | 126.6 s |
| luna B (slowest), turn_p90 = 6.4 s | 116 s | box 34.8 s, n = floor(28.8/12.8) = 2: 31.6 s | **147.6 s (+27.2%)** |
| luna B, whenever turn_p90 > 7.2 s | 116 s | n = 1: 6 + 12.8 = 18.8 s | 134.8 s (+16.2%) |
| luna B, resume failure detected at 2 s | 118 s (fallback launch) | box 32.8 s, n = floor((32.8 - 16)/12.8) = 1: 16 + 12.8 = 28.8 s | 146.8 s |
| ember | 41 s (idle until both lunas finish) | starts at 116 s; box 34.8 s, n = min(3, 4) = 3: 6 s plus 3 x 2 x 3.2 s = 25.2 s | 141.2 s |

- **Planned end:** 147.6 s (+27.2%) at n = 2, or 134.8 s (+16.2%) at n = 1. These are valid only at B = 116 s and the stated turn_p90.
- **Enforced phase-2 bound:** every phase-2 process is killed at T0 + 1.30 B_A1 = **150.8 s (+30.0%)**, whatever the model does. This is the only bound in the slate enforced by a kill. Panel elapsed is at most max(T1, 150.8 s), where T1 is the slowest phase-1 end; a phase-1 overrun is caught by the common hang guard at T0 + 1.5 B_A1 = 174 s (`SLO_BREACH`). A reviewer that starts phase 2 after 150.8 - 18.8 = 132.0 s gets n = 0.
- **Idle used:** ember's wait covers its phase-2 start condition, and luna A's phase 2 runs inside luna B's phase 1.

The drift band of section 2.0 matters most here: the 1.30 B_f deadline stays under the 1.35 B_c cap only while B_c >= 0.963 B_f.

**(e) Contamination safeguards.**

- **Shared:** peer anchors (exact candidate quotes) plus a catalogue move.
- **Withheld:** peer claims, severities, verdicts and counts.
- **Independent first pass:** structural (a separate phase, sealed by process exit after its H2 re-ask), so it can be audited byte for byte from `<rid>.p1.md`.
- **Decoys:** gap cards fill 1 slot in 3, so a receiver cannot read an anchor as "a peer found something here".
- **Blind-spot spread:** the peer's question is never sent, only the place, and the flipped move is by rule a *different* question from the one the peer's category implies. A peer's wrong blocker is therefore not repeated: the receiver is asked a different question, not to confirm.
- **Convergence alarm (measurable):** the shared own-line rule of section 2.0. CONVERGENCE uses only `origin:"own"` lines (phase-1 findings), so it should fire at A1's rate; the arm passes the independence guard if it fires in at most 2 of 12 runs, and the ledger row count must not fall more than 20% below A1. The balanced deal keeps the two lunas on disjoint ember anchors, so the design does not raise luna-luna overlap by construction.
- **ECHO (real-anchor slots only):** the share of phase-2 findings on real-anchor slots that restate the peer's own claim on the same anchor (claim token Jaccard above 0.6 with the peer's claim); alarm above 30%.
- **Sealed-report judging:** the merged phase-1 reports (the post-re-ask `p1.md` files) are judged separately under random labels, which gives a within-run estimate of C.

**(f) Expected gain.** Model: gain = P(a peer anchors the right sentence) x P(challenge selected and executed, 0.5-0.6) x P(correct conclusion kept and credited, 0.3-0.6). The act-rate factor (0.5-0.6) is a planning value that REQ-S3's measured act rate replaces. Values are planning values at n = 2 for both lunas on EL2.

Derivation from the base rows (V4 rows 0.23-0.94): the anchor routes to B1, B2 and I4 are removed, because no cheap peer anchors their criteria (T2b; they are reached only by the gap card, booked to P); the never-found I5 and I6 rows get low end 0 (no cheap-model rate exists for them; section 2.0, catalogue rules); decoy displacement multiplies the low end by 2/3.

| Issue | Anchor rate used | C low | C high |
|---|---|---|---|
| B5 | ember designSpec Task 8, 33% (3 cheap near-misses) | 0.04 | 0.15 |
| I1 | | 0.02 | 0.08 |
| I5 | ember designSpec Task 2, 46%; luna must grep the root; minor-drop risk | 0 | 0.15 |
| I6 | ember alias Task 6, 57%; `contradiction` -> M8 sibling sweep | 0 | 0.12 |
| B8 / B6 | | 0.01 / 0.02 | 0.05 / 0.08 |
| Subtotal | | 0.09 | 0.63 |
| **C /14, after decoy displacement (x 2/3 at the low end)** | | **0.06** | **0.63** |

| Share | Value | Column rule |
|---|---|---|
| C /14 (EL2) | 0.06-0.63 | collaboration |
| P from the gap-card route to B1, B2, I4 | 0-0.10 /14 | prompting share; never added to C |
| H /14 (EL2) | 0.03-0.34 (central 0.14) | harness share; never added to C |
| I7 (control /2) | 0.05-0.20 | collaboration, reported on control |

**(g) Effort.**

| Component | Lines |
|---|---|
| `run-reviewer.sh`: drop `--no-session-persistence`, capture `session_id` from the JSON result | about 5 |
| `phase2-digest.sh`: jq parse of blocks, category and keyword selection, style routing, surface filter | about 70 |
| Phase-2 launcher with timeout and resume or fresh fallback | about 25 |
| Block combiner: one findings-v1 block, renamed ids, origin tag | about 30 |
| Validation through the real parser (H2) | about 15 |
| stream-json capture for phase-2 and re-ask sessions, and per-line salvage on a kill | about 20 |
| **Total** | **about 165** |

No hooks are needed.

**(h) Failure modes and runbook.**

| Failure | Detection | Action |
|---|---|---|
| `--resume` fails on a gateway model | exit code not 0 or empty result | Fresh-session fallback (logged `resume_fallback`); n is recomputed with the 16 s start cost and the digest re-rendered; n = 0 means no launch |
| Phase 2 killed at the deadline | `phase2_timeout` | The combiner keeps every complete, parser-valid phase-2 line already streamed (`p2_lines_salvaged`) and drops the rest; phase 1 stands |
| Phase 2 rewrites or withdraws phase-1 findings | the combiner keeps phase-1 lines verbatim; diff check | Phase-1 lines are immutable by construction |
| Phase-2 block malformed | H2 parser check | One re-ask only if one start plus one turn fits before T0 + 1.30 B_A1; otherwise the invalid phase-2 lines are dropped with a warning and phase 1 stands |
| No qualifying peer anchor (ember produced only surface findings) | `challenges = 0` | Logged; the package behaves as isolated for real slots; ECHO is "not applicable" |
| Two blocks in one report (parser uses the last) | combiner unit test | Exactly one block emitted |
| Session storage grows on the host | disk check | Delete only the session ids recorded in that run's `collab.json`, after every concurrent run on that sandbox has ended; never delete the directory; check `git status` after the last such run |

---

<!-- Source: Base (original, modified) - Redesign 4 (F7, slot 5) re-based to EL2, one way, and rewritten inside its (a)-(h) skeleton per Change #15 (debate/round2-V4.md:28-43; INV-005 text of debate/round3-V2.md:21; INV-017, INV-018, INV-023; Variant 5 (sonnet:performance) first-hand rule C-3) -->
### Redesign 4: Flag-and-Adjudicate (slot 5, family F7 Directed challenge: one model flags checkable sentences, a different model must settle them)

**(a) Mechanism and model roles.** The design runs **one way** on EL2.

- **ember (flagger)** is told to *flag, not settle* certain sentences it meets while reading. From its 3rd tool call it posts a **card** for each acceptance criterion or sentence containing every, all, only or complete, each command or grep criterion, and each mapping table, at most 2k cards per package. Each card carries the anchor, a **reading** move (M3, M4, M5, M6, M9), and the `category` and `severity` enum values ember would give (the single R-06 exception; never `claim`, never `blocking`).
- **luna x2 (adjudicators)** receive the cards and must answer each with a finite check and its result, inside their own findings block. Lunas post no cards, and nobody is held at Stop.

**Dealing and form (within-arm contrast).** Card i is the i-th card ember posts (its board append index, i = 0, 1, ...). It goes to luna (i + r) mod 2. The harness renders it in **challenge form** (anchor plus the required finite check) when (i + floor(i/2) + c) is even, and in **finding form** (anchor plus ember's category and severity) otherwise. r and c are seeded 0/1 coins per run, logged as `deal_r` and `deal_c`. At k = 2 each luna gets exactly one card of each form, so each luna is its own control; at k = 1 the two lunas get opposite forms.

This is the slot that answers the seed's open question "is a mid-run message more valuable as a challenge than as shared findings?", and it answers it **within F7**, by comparing conversion between the two forms. Arm A5 against arm A4 does **not** answer it: the two arms compare two whole designs that differ in sender session, content source, move type and target issues. Baseline: EL2, ember + 2x luna (planning B = 116 s; measured B_A1).

**(b) Communication schedule.**

| Item | Value |
|---|---|
| Ember posting | from its 3rd tool call, at most 2k cards; a card past 2k is rejected and logged `over_cap` |
| Luna posting | none |
| Delivery to luna | PostToolUse, after luna's 6th tool call and after its hook-side snapshot is written and hashed (fail closed, `snapshot_missing`) |
| Adjudications per luna | at most k (one per card dealt to it) |
| Messages per reviewer | ember: at most 2k sent, 0 received; each luna: at most k received, 0 sent |
| Size cap | 600 bytes per card |
| Schema | `panel-msg/1` with `kind:"card"`, `anchor` required, `move` required, `category` and `severity` (enums, cards only), `to` set by the deal |
| Logged per slot | form, recipient, card Task, conversion (the receiver's line overlaps the card anchor by at least 12 characters), judge-credited conversion, uncredited conversion |
| Deadline guard | nothing is delivered after PANEL_FINISH_AT; no Stop hold; a card that arrives after the receiver's last tool call is logged `late` and dropped |

**(c) Transport.** Board plus hooks. Cards need mid-run delivery to a running luna, and the board does that durably with an audit log. No Stop hold is needed, because the design runs one way.

Cross-session `SendMessage` was considered because it has built-in reply addresses. It is the named fallback only if spike S1 shows that ember and luna call `SendMessage` reliably and that a `-p` session receives messages mid-run. Even then it would lose the board audit log, so the board stays primary.

**(d) Time budget (EL2, planning B = 116 s, turn_p90 = T_report_p90 = 6.4 s).**

| Reviewer | Baseline end | Added | New end |
|---|---|---|---|
| ember (flagger) | 41 s | 2k card posts x 3.2 s = 6.4 s (k = 1) or 12.8 s (k = 2) | 47.4 s or 53.8 s, off the critical path |
| luna (slowest), k = 1 (central) | 116 s | hooks 2 s + 1 adjudication x 2 turns x 6.4 s = 14.8 s | **130.8 s (+12.8%)** |
| luna (slowest), k = 2 (optimistic) | 116 s | hooks 2 s + 2 adjudications x 2 x 6.4 s = 27.6 s | **143.6 s (+23.8%)** |

The three numbers (section 2.0, timing rule 3), the same as Redesign 2:

- **Planned end:** 130.8 s (+12.8%) at k = 1, or 143.6 s (+23.8%) at k = 2, both at or under PANEL_FINISH_AT = 143.8 s.
- **Finish-signal bound:** T0 + 1.35 B_f = 156.6 s (+35.0%).
- **Enforced ceiling:** the hang guard at T0 + 1.5 B_A1 = 174 s (+50%), counted as `SLO_BREACH`.

The +35% cap is **audited by the SLO budget (R-24), not enforced**; no figure above is a worst-case guarantee. Idle used: ember's posts fall inside its own run, long before luna ends.

**(e) Contamination safeguards.**

- **Shared:** an anchor plus a required move (challenge form) or an anchor plus enum category and severity (finding form).
- **Withheld:** the flagger's claim and any free text; the card schema has no field for either.
- **Independent first pass:** each luna's hook-side snapshot is written before its first card (fail closed). Ember receives nothing.
- **Blind-spot spread:** the adjudicator is a different model family by rule, and the move dictates the question, so the flagger's angle is not inherited. A fact or count is never cited unless the receiver's own transcript ran the check (first-hand rule).
- **Convergence alarm (measurable):** the shared own-line rule of section 2.0 (own-line Task Jaccard above the A1 mean + 0.15, or ledger rows down more than 20%; pass if it fires in at most 2 of 12 runs).
- **Adjudication agreement:** the share of cards where the adjudicator raises a finding; alarm above 90% (rubber-stamping) or below 5% (cards ignored).
- **Flag-finding overlap:** `flag_finding_overlap` (the share of ember's cards whose anchor equals an anchor in ember's own final findings) above 50% means flags behave like findings; the arm **stops and is reported**, and the treatment is never changed partway through the arm.

**(f) Expected gain.** Model: P(flagger posts a card on the sentence: ember complies with posting 0.6-0.8, and the sentence is among its 2k cards 0.3-0.5) x P(adjudicator reaches the defect 0.3-0.5) x credit 0.5-0.8. Every act-rate factor here is a planning value that REQ-S3's measured act rate replaces. Derivation from the base rows (0.16-0.93): the luna search-card rows B8 and B6 are removed (no luna cards), and the never-found B1, B2 and I5 rows get low end 0 (no cheap-model rate exists for them; section 2.0, catalogue rules). The k = 1 rows halve every k = 2 row (planning, replaced by logged delivered-card counts).

| Issue | Through | C at k = 2 (low-high) | C at k = 1 (low-high) |
|---|---|---|---|
| B1 | T2b, M3 card on an unbounded AC | 0-0.16 | 0-0.08 |
| B2 | T2b | 0-0.08 | 0-0.04 |
| I4 | T2b, M4 card on a grep AC | 0.03-0.15 | 0.015-0.075 |
| B5 | T2a | 0.03-0.15 | 0.015-0.075 |
| I1 | T2a | 0.02-0.10 | 0.01-0.05 |
| I5 | | 0-0.08 | 0-0.04 |
| I6 | | 0-0.05 | 0-0.025 |
| **C /14** | | **0.08-0.77** | **0.04-0.39** |

| Share | k = 2 | k = 1 | Column rule |
|---|---|---|---|
| C /14 (EL2) | 0.08-0.77 | 0.04-0.39 | collaboration |
| P | none booked | none booked | prompting share |
| H /14 (EL2) | 0.03-0.34 (central 0.14) | same | harness share; never added to C |
| I7 (control /2) | 0-0.10 | 0-0.05 | collaboration, reported on control |

Every designSpec row (B1, B2, B5, I1, I4, I5) needs k >= 1 on designSpec, where the 100 s median allows k >= 1 only if T_report_p90 <= 13.8 s and makes k = 2 impossible. The B5 (Task 8), I1 and I4 (Task 12) rows also assume ember does not spend its cards on early Tasks; the logged card Task is the falsifier (if 2k or more flaggable sentences come before designSpec Task 8, these rows go toward 0).

**Pre-registered secondary analysis (form contrast).** Conversion by form, with a two-proportion test and the run-paired difference also reported. At 12 runs x 3 packages x 4 cards there are at most 144 cards, about 72 per form; fewer where k = 1.

Note: the flagging step could be replaced by a deterministic sentence extractor. That would be a prompt and harness change, not collaboration; arm A2 bounds it.

**(g) Effort.** Board substrate (about 100 lines), plus the deal and form renderer (in place of the base router, about 40), card validator with the enum exception and `over_cap` (about 20), brief text (about 20). The base's Stop hold (about 30) is dropped. **Total about 180 lines.**

**(h) Failure modes and runbook.**

| Failure | Detection | Action |
|---|---|---|
| ember never posts (gateway tool compliance) | `cards_sent = 0` | Above 50% of runs: the design is not viable on ember; stop the arm |
| Cards spent on early Tasks | logged card Task per slot | Report; the B5, I1 and I4 rows are falsified for that package |
| Flags behave like ember's own findings | `flag_finding_overlap` above 50% | Stop and report the arm; never add a decoy partway through |
| Card overload pulls luna off its own review | `ledger_rows` more than 20% below A1 (CONVERGENCE) | Report; k is fixed per package by the values file and is not changed during an arm |
| Snapshot not written | `snapshot_missing` | Nothing delivered to that luna; the package counts as isolated for it |
| Wrong blockers from adjudications | wrong blockers more than A1 + 1.0 | Fail the arm |
| A luna runs past the finish-signal bound | `finish_signal_t`, `hang_kill` | Counts against the SLO error budget (R-24); beyond 174 s it is `SLO_BREACH` |

---

<!-- Source: Base (original, modified) - Redesign 5 (F6, slot 4) re-based to SL2 and rewritten inside its (a)-(h) skeleton per Change #14 (debate/round2-V4.md:84-86; INV-006 at debate/round3-V1.md:30 and debate/round3-V4.md:29; INV-008; INV-021; Variant 1 (opus:architect) V1-R5 brief line; U-014 surface filter; refactor-plan global decision 4) -->
### Redesign 5: Coverage Deflection (slot 4, family F6 Steering a running strong model: fast cheap scouts steer sonnet toward what nobody has covered)

**(a) Mechanism and model roles.** Every panel converges on the easy issues: B3 is found in 68 of 76 runs, I2 in 52 and I8 in 56 (`CR:498`). In sonnet + 2x luna, the two lunas finish long before sonnet (about 102-110 s against 273.7 s), and sonnet is the slowest reviewer and the only one that reliably runs reverse-dependency sweeps.

The lunas act as **scouts**. When a luna exits, its findings block exists: its content is sealed by process exit on the sender side. A harness watcher parses that block into (Task, category) pairs of its **non-surface** findings and posts a **request card** to sonnet:

- requests for Tasks that have **no** peer finding, ranked first by the Tasks the lunas declared "not checked" in their reports;
- the instruction: "apply catalogue moves M1-M10 to these Tasks first; finish checks you have already started";
- the brief line (V1-R5) "peer coverage is not clearance: a Task a peer looked at is not cleared".

The card carries **no counts, no categories and no covered list**, because a covered count acts as a clearance signal. Coverage comes only from finished peers' findings, never from telemetry, and nothing is sent by `SendMessage`. Sonnet's budget moves toward Tasks nobody covered, where the rare issues sit. Baseline: SL2, sonnet + 2x luna (planning B = 273.7 s; measured A1-SL2 median), a seed baseline.

**(b) Communication schedule.**

| Item | Value |
|---|---|
| Trigger | each luna scout's exit (about 102-110 s) |
| Delivery | sonnet's next PostToolUse (within about one sonnet turn, 14 s), after sonnet's hook-side snapshot is written and hashed |
| Frequency | at most 2 cards per package to sonnet (one per luna exit); 0 to the lunas |
| Requests | each card lists at most k requests, with k computed per package from SL2's B and sonnet's turn_p90 and T_report_p90 (section 2.0); sonnet acts on at most k requests in total per package |
| Messages per reviewer | sonnet: at most 2 received, 0 sent; lunas: 0 received, 0 sent (the watcher authors the cards) |
| Size cap | 600 bytes per card |
| Schema | `panel-msg/1` with `kind:"coverage"`, `from:"watcher"`, `items` = up to k uncovered Task ids (`"T9"`), no counts, no categories |
| Deadline guard | nothing is delivered after PANEL_FINISH_AT (computed with sonnet's turns); no Stop hold |
| Run condition | the arm runs only if Spike 4 gives sonnet a T_report_p90 of at most 51.8 s (k >= 1) |

Surface findings (path, hash, line-number claims) do not count as coverage. Otherwise the luna Task 12 artifact objection, present in 91% of luna runs on the control package, would mark Task 12 "covered" and steer sonnet away from I7.

**(c) Transport.** Board plus a hook in sonnet only. Cards are generated by the harness, so no model has to send anything. Sonnet is a Claude model, so hook delivery is the lowest-risk case.

**(d) Time budget (SL2, planning B = 273.7 s, sonnet turn 14 s).**

| Reviewer | Baseline end | Added | New end |
|---|---|---|---|
| luna x2 (scouts) | about 102-110 s | none | unchanged |
| sonnet (slowest), k = 1 (central) | 273.7 s | hooks 2 s + 1 request x 2 turns x 14 s = 30 s | **303.7 s (+11.0%)** |
| sonnet (slowest), k = 2 (optimistic) | 273.7 s | hooks 2 s + 2 requests x 2 x 14 s = 58 s | **331.7 s (+21.2%)** |

The three numbers (section 2.0, timing rule 3):

- **Planned end:** 303.7 s (+11.0%) at k = 1, or 331.7 s (+21.2%) at k = 2.
- **Finish-signal bound:** T0 + 1.35 x 273.7 = 369.5 s (+35.0%).
- **Enforced ceiling:** the hang guard at T0 + 1.5 x 273.7 = 410.6 s (+50%), counted as `SLO_BREACH`.

k = 2 needs sonnet's T_report_p90 at most 23.8 s and k >= 1 needs at most 51.8 s; sonnet's final report turn is output-heavy (about 30k output tokens per run), so this is unmeasured and decides whether the arm runs. The +35% cap is **audited by the SLO budget (R-24), not enforced**. Idle used: none needed; the lunas' runs already overlap sonnet's.

**(e) Contamination safeguards.**

- **Shared:** uncovered Task ids only.
- **Withheld:** anchors, claims, severities, categories, counts and the covered list.
- **Independent first pass:** sonnet receives nothing before the first luna exits (about 102 s), by which point it has read the plan and source.md; its hook-side snapshot is written before the first card (fail closed, `snapshot_missing`). For the mechanical peer tag (section 2.0, seals) the delivered locator is the requested Task id: a later sonnet finding on a requested Task is tagged `peer`.
- **Blind-spot spread:** requests do not transmit what the peers concluded, only where nobody concluded anything; "peer coverage is not clearance" is in the brief.
- **Convergence alarm (measurable):** the shared own-line rule of section 2.0 applies, and in addition a **deflection alarm**, because this design deliberately *diverges* sonnet: alarm if sonnet's anchored Tasks overlap the Tasks the lunas covered by more than 50% (deflection ignored), or if the panel's union of anchored Tasks *shrinks* against A1-SL2.

**(f) Expected gain.** Sonnet's isolated reach per run: I4 4 of 26, B5 2, I1 1, I7 7 of 26 clean (`investigation-designspec.md:124`; `investigation-patterns.md:132`). Deflection raises its time on designSpec Task 2 (8% of sonnet runs), Task 12 (23%) and alias Task 7 (27%). The act rate on a request is a planning value that REQ-S3's measured act rate replaces.

Re-derivation for SL2 (planning). The base rows (low 0.26, high 1.06) were derived on ember + luna + sonnet with covered-count cards. On SL2 the scouts are two lunas (no ember) and the cards carry uncovered-Task requests only. So: high = the base rows, at k = 2; low = the base low rows x 0.5 (thinner luna-only coverage, at most one card per scout exit); k = 1 = the k = 2 row x 0.5. The stage-2 screen (section 4) decides.

| Issue | Base row (low-high) | C at k = 2 (low-high) | C at k = 1 (low-high) |
|---|---|---|---|
| I4 | 0.05-0.20 | 0.025-0.20 | 0.0125-0.10 |
| I5 | 0.03-0.15 | 0.015-0.15 | 0.0075-0.075 |
| B8 | 0.05-0.15 | 0.025-0.15 | 0.0125-0.075 |
| B1 / B2 | 0.02-0.10 each | 0.01-0.10 each | 0.005-0.05 each |
| B5 / I1 | 0.03-0.10 / 0.02-0.10 | 0.015-0.10 / 0.01-0.10 | 0.0075-0.05 / 0.005-0.05 |
| B6 / I6 | 0.02-0.08 each | 0.01-0.08 each | 0.005-0.04 each |
| **C /14** | 0.26-1.06 (not carried) | **0.13-1.06** | **0.07-0.53** |

| Share | k = 2 | k = 1 | Column rule |
|---|---|---|---|
| C /14 (SL2) | 0.13-1.06 | 0.07-0.53 | collaboration, planning |
| P | none booked | none booked | prompting share |
| H /14 (SL2) | +0.1 to +0.4, UNVERIFIED (no bottom-up SL2 table exists) | same | harness share; never added to C |
| I7 (control /2) | -0.20 to +0.20 | -0.20 to +0.20 | collaboration, reported on control |

I7 can fall if Task 12 is miscounted as covered, which is why the surface filter exists. H4 lowers measured I7 for sonnet panels by up to 2 in 9 credits; that is a measurement correction on control, not a loss.

**(g) Effort.** Board substrate, hook in sonnet only (about 60 lines), coverage watcher (poll every 2 s for finished reports, jq per-Task parse, surface filter, request ranking, about 60). **Total about 120 lines.**

**(h) Failure modes and runbook.**

| Failure | Detection | Action |
|---|---|---|
| Deflection pushes sonnet off a Task where a peer's finding was a wrong blocker, so a real issue there is missed | the experiment's per-Task reach compared with A1-SL2 | A Task counts as covered only by a non-surface finding; review per-issue reach |
| Surface regex misses a surface claim | spot-check of the coverage audit | Extend the regex |
| sonnet ignores the cards | deflection alarm | Logged; gain goes to 0, with no harm |
| sonnet's final report turn is too long for k >= 1 | Spike 4 T_report_p90 above 51.8 s | Do not run the F6 arm |
| sonnet runs past the finish-signal bound | `finish_signal_t`, `hang_kill` | Counts against the SLO error budget (R-24); beyond 410.6 s it is `SLO_BREACH` |
| Cost: needs a sonnet panel (2.2x tokens of ember + 2x luna) | n/a | Use only where the quality tier is already chosen (`CR:428`) |

Grok is used in no design: its median of 790 s per review, and 2,109-3,897 s elapsed in its panels (`CR:314, :325`), cannot fit any cheap baseline's +35% window.

---

<!-- Source: Base (original, modified) - comparison table rebuilt per Change #16 with Variant 5 (sonnet:performance) columns and rows (V5:400-413: net collaboration share, tokens per added issue, static-kit row, sonnet reference row) and the base's I7 column (V4:614-626) -->
## 3. Comparison of the five redesigns

Rows are in slot order; the base document's redesign numbers are kept in the second column. All gain columns are out of 14 per run (I7 on control /2), planning values, with the harness fixes applied to both arms. **C, P and H are separate shares and are never added together.** Times are per package at planning B (116 s for EL2, 273.7 s for SL2); every figure is valid only at its stated k (or n) and is replaced by Spike 4's per-package values. No column is a worst-case guarantee: for slots 2-5 the +35% cap is audited by the SLO budget (R-24), and only F1's phase-2 end is enforced by a kill.

| Slot | Redesign (family) | Panel and baseline | Planned elapsed, k = 1 / k = 2 (F1: n = 1 / n = 2) | Finish-signal bound | Enforced ceiling | C /14, k = 1 / k = 2 | P /14 | H /14 | I7 control /2, k = 1 / k = 2 | Output tokens overhead | Tokens per added issue | Contamination risk | Effort | Reliability |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Redesign 3 Axis-Flip Challenge (F1) | ember + 2x luna, EL2 (116 s) | 134.8 s (+16.2%) / 147.6 s (+27.2%) | none (between phases) | phase-2 kill at 150.8 s (+30.0%); phase-1 hang guard 174 s | 0.06-0.63 (at n = 2) | 0-0.10 (gap-card route) | 0.03-0.34 | 0.05-0.20 | +34% (about 7.2k) | about 63k | Low: anchors only, decoys, first pass sealed by process exit | about 165 LOC | Highest: no live channel; fallback is the phase-1 report; resume and streaming need spike S2 |
| 2 | Redesign 2 Idle-Shift Sweeper (F4) | ember + 2x luna, EL2 (116 s) | 130.8 s (+12.8%) / 143.6 s (+23.8%) | 156.6 s (+35.0%) | hang guard 174 s (+50%, `SLO_BREACH`) | 0.07-0.34 / 0.14-0.67 | none booked | 0.03-0.34 | 0.09-0.25 / 0.17-0.50 | +45% (about 9.6k) | about 71k | Low-medium: repo facts with commands, no conclusions, no zero counts | about 180 LOC | Medium: hooks, a second process, snapshot seal |
| 3 | Redesign 1 Move Radar (F3) | ember + 2x luna, EL2 (116 s) | 130.8 s (+12.8%) / 143.6 s (+23.8%) | 156.6 s (+35.0%) | hang guard 174 s (+50%, `SLO_BREACH`) | 0-0.24 / 0-0.48 | 0.04-0.20 / 0.08-0.40 (luna injections) | 0.03-0.34 | 0.05-0.20 / 0.10-0.40 | +26% (about 5.6k) | about 70k | Lowest: move ids only, no peer content | about 230 LOC | High: no model action needed; depends on hooks firing (S0) |
| 4 | Redesign 5 Coverage Deflection (F6) | sonnet + 2x luna, SL2 (273.7 s) | 303.7 s (+11.0%) / 331.7 s (+21.2%) | 369.5 s (+35.0%) | hang guard 410.6 s (+50%, `SLO_BREACH`) | 0.07-0.53 / 0.13-1.06 | none booked | +0.1 to +0.4 (UNVERIFIED) | -0.20 to +0.20 | not re-derived for SL2 (UNVERIFIED) | not computed | Low: uncovered Task ids only | about 120 LOC | Medium-high: harness-generated cards, Claude receiver; runs only if sonnet's T_report_p90 <= 51.8 s |
| 5 | Redesign 4 Flag-and-Adjudicate (F7) | ember + 2x luna, EL2 (116 s) | 130.8 s (+12.8%) / 143.6 s (+23.8%) | 156.6 s (+35.0%) | hang guard 174 s (+50%, `SLO_BREACH`) | 0.04-0.39 / 0.08-0.77 | none booked | 0.03-0.34 | 0-0.05 / 0-0.10 | not re-derived for EL2 one way (UNVERIFIED) | not computed | Medium: anchors routed to named peers; enum verdicts in finding form | about 180 LOC | Medium-low: needs ember to post cards |
| control | A2: static move kit, no exchange | ember + 2x luna, EL2 | about +29% (V5 estimate, UNVERIFIED) | n/a | hang guard 174 s | 0 by definition | 0.08-0.66 (V5 assumption, central 0.33) | 0.03-0.34 | about 0.07 (V5 assumption) | about +30% | about 57k | None | about 25 (brief only) | High |
| baseline | A1: isolated with H (EL2) | ember + 2x luna | B_A1 (planning 116 s) | n/a | hang guard 174 s | 0 | 0 | 0.03-0.34 (central 0.14) | 0 | 0% | n/a | None | about 70 (harness fixes) | High |
| baseline | A1-SL2: isolated with H; also the sonnet reference | sonnet + 2x luna | B_A1 of SL2 (planning 273.7 s); +136% against EL2 (821 against 348 s, three packages) | n/a | hang guard 410.6 s | 0 | 0 | +0.1 to +0.4 (UNVERIFIED) | historical 1.33 against 0.83 for EL2 | +119% against EL2 (139k against 64k per run) | about 150k (historical +0.50 /14 against EL2, p = 0.51) | None | 0 | High |

Notes:

- **Tokens per added issue** is a planning figure: output-token overhead per package x 3 packages / the midpoint of C at k = 2 (F1 at n = 2). It is not computed where the token overhead has not been re-derived for the design's current panel.
- **Output tokens overhead** for F1, F4 and F3 are the base document's estimates on EL2, made at two items per receiver (k = 2, or n = 2 for F1). Token overheads are output tokens, the study's metric. Hook injection and resume also raise input tokens, mostly as cache reads; these are recorded but not compared.
- **Reading the table.** The static kit (A2) may beat every exchange design on gross gain, because it gives every reviewer all the moves from the first second. An exchange design earns its place only if it beats A2 by the margin set in section 4. If none does, the right design is the cheapest one: the harness fixes plus the kit in the brief.

---

<!-- Source: Variant 2 (opus:analyzer) experiment plan (debate/round2-V2.md:118-148; V2:517, :531) with debate/round2-V4.md:90-96, the decision table and stage-2 screen of debate/round3-V2.md:30-32 (Variant 5 (sonnet:performance) screen, round2-V5.md:126-129), INV-005 secondary analysis and V5 block randomisation - merged per Change #17, replacing the base section 4 -->
## 4. Recommended first experiment

**Choice.** Run all five slots in one pre-registered plan: the four EL2 designs (F1, F4, F7, F3) in stage 1 on the decided default panel ember + 2x luna (`CR:428`, `HO2:288`), against two shared controls, and F6 in stage 2 on sonnet + 2x luna against its own controls. Every arm is compared with the static kit (A2), because the kit may capture most of the gain without any exchange.

**Gate 0 (must pass and be recorded before any arm runs; one package each).**

| Spike | What it checks |
|---|---|
| S0 | `--settings` PostToolUse hooks fire in `claude -p` for `muse-ember-1.0` and `gpt-6-luna`, the hook-side snapshot is written and hashed, the hook timeout, and which sandbox project hooks are active |
| S1 (only if F7 needs its fallback) | ember and luna call `SendMessage` reliably and a `-p` session receives messages mid-run |
| S2 | `--resume` works for both gateway models once `--no-session-persistence` is removed, and luna's phase-2 text streams to file before exit under `--output-format stream-json --verbose` |
| S3 | Full-chain smoke test (reviewer, combiner, `superclaude review merge`, anonymiser, `judge-one.sh`) with 0 dropped findings lines, applying lesson `HO2:259`; stream-json output parsed with `jq -s` through the same `RR:50-52` filters (`model_ok`, tokens) |
| REQ-S3 | Act rate: a PostToolUse `additionalContext` injected into a gateway-model session appears in the transcript and changes the next tool call (inject "run `ls /tmp/panel-probe`"; the next tool call runs it), for ember and luna; also the act rate on "finish now". The measured rates replace every planning act rate in section 2. |
| Spike 4 | Per package: B_A1, turn_p90 and T_report_p90 (luna for EL2, sonnet for SL2), PANEL_FINISH_AT and k, written to the values file with its sha256 (R-30); per-role end times and each design brief's slowdown s on the critical-path role |
| Spike 5 | Re-score the raw findings of the 30 cheap historical runs with the normalizer (judge calls only), to measure the H2 part of H |

**Arms.** All arms except A0 carry the harness fixes H1-H4. All arms in a stage run concurrently, in block-randomised order (each block is one replicate of every arm on all three packages), to cancel gateway load drift.

| Arm | Content | Runs | Measures |
|---|---|---|---|
| A0 | ember + 2x luna on today's harness, fresh | 4, plus the 6 historical S07 runs as context | H = A1 - A0 at the same time; gateway drift |
| A1 | ember + 2x luna, isolated, with H | 12 | the named baseline B_A1; the comparator for reach |
| A2 | A1 plus the static move kit (catalogue M1-M10 in every brief) | 12 | P = A2 - A1 |
| A3 | Redesign 3, Axis-Flip Challenge (F1) | 6, extended to 12 | C; plus sealed-report judging |
| A4 | Redesign 2, Idle-Shift Sweeper (F4) | 6, extended to 12 | C at arm level |
| A5 | Redesign 4, Flag-and-Adjudicate (F7); gated on the REQ-S3 act rate and `cards_sent > 0` in the spike | 6, extended to 12 | C; the within-arm form contrast |
| A6 | Redesign 1, Move Radar (F3) | 6, extended to 12 | C, read as "telemetry-timed kit against static kit" |
| Stage 2: A1-SL2, A2-SL2, F6-SL2 | sonnet + 2x luna: isolated with H; plus static kit; Redesign 5 Coverage Deflection (F6), run only if Spike 4 gives sonnet T_report_p90 <= 51.8 s | 12, 6, 6 extended to 12 | F6 against its own panel |

**Size.** Stage 1: at most 4 + 12 + 12 + 4 x 12 = 76 panel runs; 52 if every exchange arm stops at the interim look. Stage 2: at most 30. A run is one panel on all three packages.

**Conduct.** `NOFALLBACK=1`; at most 10 concurrent runs and at most 4 ember (`HO2:236`); `model_ok` checked on every session, including the sweeper and phase-2 sessions; the same blind judge (`EVAL/tools/tmp-scripts/judge-one.sh`, unchanged and sha256-pinned) on anonymised merged reports with `origin` keys and board references stripped and random labels, so the judge cannot tell which arm a report came from. For A3, the merged sealed phase-1 reports are also judged under separate random labels.

**Primary endpoint: target reach.** A run reaches the target if it has at least one credit on B1, B2, B5, B6, B8, I1, I4, I5 or I6, or on I7 on the control package. The historical cheap rate is 0 of 30 runs.

**Pre-registered decision rule (final look only).** Arm X is adopted for confirmation only if all of these hold:

1. **Reach against A1.** X beats A1 under a one-sided Fisher exact test at p < 0.05, using the threshold for the **observed** A1 reach:

   | Observed A1 reach (of 12) | X needs (of 12) | One-sided Fisher p | One run fewer gives |
   |---|---|---|---|
   | 0 | 4 | 495/10,626 = 0.047 | 3/12: 220/2,024 = 0.109 |
   | 1 | 6 | 11,880/346,104 = 0.034 | 5/12: 10,428/134,596 = 0.077 |
   | 2 | 7 | 58,432/1,307,504 = 0.045 | not stated |

2. **Reach against the kit.** X beats A2 by at least 4 reach runs at n = 12. Otherwise the gain is credited to the catalogue, not to communication.
3. **No loss.** Mean found /14 in X is at least A1 - 0.25; mean wrong blockers at most A1 + 1.0; mean control wrong blockers at most A1 + 0.5.
4. **Time.** Per package, the median elapsed is at most 1.35 B_A1, within the SLO error budget of R-24 (1 package in 12), and no package exceeds 1.5 B_A1.
5. **Independence.** CONVERGENCE (own-line rule) fires in at most 2 of 12 runs, and there are zero audit violations: no board message or digest contains a ground-truth `plan_quote` substring of 12 characters or more (grep against each `ground-truth.json`); no reviewer transcript opens `.dev/reflect/`; no free text in any message; the F3 leak lookup is clean.

**Interim look at 6 runs: futility only.** An exchange arm stops if its hard-issue credits are at or below A1's, or its median elapsed overhead exceeds +35%, or the convergence alarm fired in 3 or more of its 6 runs. A stopped arm is reported as not adopted. No arm can pass at the interim look, so there is only one efficacy look.

**Multiplicity.** Four exchange arms each tested at 0.05 give a familywise false-pass rate of at most 4 x 0.05 = 0.20 (Bonferroni bound). That is acceptable only because adoption also requires a **12-run confirmation on at least two new packages**: the move catalogue was abstracted from these three packages, so in-sample gains are optimistic.

**Stage-2 screen (F6).** SL2 already reached I7 in 3 of 6 historical runs, so the reach endpoint is nearly saturated there (at A1-SL2 6/12, X would need 11/12). F6 is screened instead on hard-issue credits per run: a one-sided permutation test against A1-SL2 at p < 0.05, and a margin over A2-SL2 of at least 1/3 of runs.

**Secondary analyses (pre-registered).** Found /14, real blocking, wrong blockers, control found /2, elapsed per package, output tokens, the alarms, and `finish_would_fire` in A1 and A2 against the design arms' truncation rate. Every arm's results table reports H, P and C in separate columns. For A5, conversion by card form (challenge against finding) with a two-proportion test and the run-paired difference, at most 144 cards.

**What this plan can and cannot detect.** H is carried at 0.03-0.34 /14 per run, almost all on reach issues (B5, I1, I4, B8, B2), so A1's own reach may be about 3-29% per run. With A1 at 1/12 or 2/12, an arm needs 6/12 or 7/12, which calls for C near the top of each slot's range. **The plan cannot detect the central estimates of any slot.** It is still run, as a screen: a large effect passes, the harness and kit shares H and P are measured either way, and the mechanism logs (deliveries, act rates, conversions) tell which designs are worth a larger test.

**Outcomes.**

| Result | Decision |
|---|---|
| X passes rules 1-5 | 12-run confirmation of X on at least two new packages before adoption |
| No exchange arm passes, but A2 beats A1 under rules 1 and 3-5 | Adopt the static kit with the harness fixes; stop the collaboration line |
| Nothing passes | Keep H1-H4 and stop |
| A1 against A0 | Reported as the harness share H, independently of the collaboration decision |
| Abort an arm during the run | Futility at the interim look; the R-24 error budget spent; `flag_finding_overlap` above 50% (A5); re-run mismatch above 10% (A4); `cards_sent = 0` in more than 50% of runs (A5); `SNAPSHOT` alarm (mid-run arms) |

The decision rule, the values file and the analysis script are committed before the first arm runs (R-30).

---

<!-- Source: Base (original, modified) - section 5 retitled and extended to all five redesigns per Change #18 (R-01..R-30 updated in place; R-31 onward added; Changes 3-17) -->
## 5. Requirements for the shared substrate and all five redesigns

Every requirement has an id and a verification entry. R-01..R-30 keep their base ids, updated in place; R-31 onward are new.

### 5.1 Harness preconditions (apply to every arm)

| Id | Requirement | Verification |
|---|---|---|
| R-01 | (H1) The reviewer brief names the absolute path of source.md next to the candidate path and asks the reviewer to read both. | grep the brief in `run-reviewer.sh`; 0 of 12 A1 transcripts lack a tool call naming source.md, or the miss is reported per model |
| R-02 | (H2) Before the merge, `anchor` and `anchor2` are truncated to 200 characters and `claim` to 300, keeping each an exact prefix of the original. The block is then parsed at run time with the real findings parser. If any line would still be dropped (anchor or anchor2 under 12 characters, refs over 8, id over 16, bad severity, MINOR marked blocking), the harness re-asks once through `claude -p --resume` with the parser's error list. The phase-1 re-ask finishes before the seal (R-11); in F1 a phase-2 re-ask runs only if one start plus one turn fits before T0 + 1.30 B_A1, otherwise the invalid phase-2 lines are dropped and phase 1 stands. Re-ask time is logged as `reask_s` in every arm, A1 included, and counts in `elapsed_s`. Remaining drops are recorded in `meta.json` as `dropped_lines`. The grading rule and the judge are unchanged and sha256-pinned. | Unit test with a fixture report holding a 250-character anchor: it is truncated, not dropped; a fixture with a bad severity triggers the re-ask and `dropped_lines` is recorded; S3 smoke shows 0 dropped lines; judge and brief grading text hash equal the pinned values |
| R-03 | (H3, H4) For each package, the reviewer sandbox is a `git archive` of the commit the plan was written against, minus `.dev/tasks/done`, `.dev/eval-workspaces`, `.dev/research` and `.dev/reflect`. The base commit for each package is recorded in the manifest. | `ls /tmp/evalsb/<pkg>/repo/.dev/reflect` fails; the manifest lists 3 base SHAs; `refs/merge-guard.md` lacks the repaired line 146 text in the designSpec sandbox |
| R-04 | The findings-v1 block format and `superclaude review merge` are unchanged. Collaboration output reaches the merge only as additional lines in the reviewer's single findings-v1 block. | `merge` runs with the same arguments as `EVAL/analysis/merge-b11.sh`; every merged report lists the same reviewer ids as the resolution |
| R-05 | `PANEL_COLLAB=0` yields a launch command byte-identical to today's `RR:48` except for these allowed differences: R-01 and R-03; removal of `--no-session-persistence`; `--output-format stream-json --verbose` on phase-2 and re-ask sessions; the common hang guard at T0 + 1.5 B_A1 (R-43). It restores the isolated panel **with the harness fixes** (arm A1), not today's panel. | diff of the generated command lines against `RR:48`, listing only the allowed differences |

### 5.2 Shared message rules

| Id | Requirement | Verification |
|---|---|---|
| R-06 | Every message is a `panel-msg/1` JSON line of at most 600 bytes with no free-text field in any kind. The keys `claim`, `verdict`, `blocking`, `severity`, `category` and `note`, and any key not in the schema, are rejected and the line is not delivered. Sole exception: a `kind:"card"` line from ember in Redesign 4 may carry `category` and `severity` as findings-v1 enum values, never `claim` or `blocking`. A card beyond ember's cap of 2k per package is rejected and logged `over_cap`. | Validator unit test: 6 bad fixtures rejected (including a `claim` on a card and a `category` on a non-card line), 3 good ones accepted, 1 enum-tagged ember card accepted, 1 card past 2k rejected with `over_cap` |
| R-07 | The `move` field takes only M1-M10. The catalogue text is frozen in one file with a recorded sha256, and contains no ground-truth `plan_quote` substring of 12 characters or more and no file path named in any `ground-truth.json` description. | Script check against the 3 `ground-truth.json` files; sha256 in the manifest |
| R-08 | Any `anchor` in a message is an exact substring of the candidate (after whitespace flattening), 12-200 characters, taken from a peer's own findings, ember's flagged sentence, a gap-card region or the sweeper's own swept phrase, never from any file outside the sandbox and candidate. Every `items` path exists in the sandbox. | Validator checks the anchor is a substring of `candidate.md` and each path exists; the integrity grep against ground truth (section 4, guards) |
| R-09 | Reviewers keep `--disallowedTools Edit Write NotebookEdit`. Helper scripts write only under `$BOARD`, and `$BOARD` is outside the sandbox repo and the candidate directory. | `git status` in the sandbox snapshot repo is clean after each run; the candidate's sha256 is unchanged |
| R-10 | In F1, phase-2 lines carry `"origin":"peer"` and phase-1 lines `"origin":"own"`. In mid-run arms the harness tags a line `peer` when its anchor overlaps a delivered anchor by at least 12 characters or a delivered locator is in its refs, whatever the model wrote; all other lines are `own`. Mid-run seals are hook-side transcript snapshots under `$BOARD` with sha256 recorded by the harness; a snapshot or hash failure delivers nothing and logs `snapshot_missing`. The anonymiser strips `origin` before judging. | Combiner and tagger unit tests (a fixture line with a 12-character overlap is tagged `peer`); fault injection on the snapshot write yields `snapshot_missing` and zero deliveries; grep `merged-anon.md` for `origin` returns 0 |

### 5.3 Redesign 3: Axis-Flip Challenge (F1)

| Id | Requirement | Verification |
|---|---|---|
| R-11 | Phase 1 runs exactly the A1 brief. Any phase-1 H2 re-ask finishes first; then the report is saved as `<rid>.p1.md`, hashed, and never modified. This post-re-ask file is the one used for sealed-report judging. | sha256 of `<rid>.p1.md` taken at the seal equals the value at judging; a fixture run with a phase-1 re-ask shows `p1.md` written after the re-ask |
| R-12 | The digest selects only from peer findings with category `unpassable-check`, `contradiction` or `missing-requirement`, excluding claims that match the surface regex (artifact path, edit scope, hash, line number). Ember's qualifying anchors are dealt to the two lunas by the balanced online deal (anchor i to luna (i + r) mod 2, `deal_r` logged). Each slot holds a gap card with probability 1/3, seeded per receiver, built only from an eligible never-anchored region, rendered identically to a peer-anchor challenge, with its kind withheld from the digest and logged as `slot_type`. With no qualifying anchor the package is isolated for real slots and ECHO is "not applicable". | Unit tests with fixture blocks: no surface findings in the digest; 4 qualifying anchors split 2/2; over 1,000 seeded draws the gap-card share is 1/3 within sampling error; the digest text carries no slot-type marker |
| R-13 | Each challenge pairs an anchor with a move chosen by the routing table: every/all/complete/only goes to M3 or M2; a command or grep to M4 or M7; a mapping or table to M5 or M6; a constraint to M8; a peer finding with category `contradiction` to M8 across all tasks. Search moves go to ember and reading moves to luna. A challenge never goes back to the anchor's author. | Router unit test over 10 fixtures, including a `contradiction` fixture |
| R-14 | Phase 2 resumes the reviewer's own session with the digest. If resume fails, it starts a fresh session with the phase-1 report path plus the digest, recomputes n with the 16 s start cost (R-15), re-renders the digest, and logs `resume_fallback`. | Spike S2; fault injection on the resume; metrics count |
| R-15 | Before each launch attempt the harness computes box = min(35, T0 + 1.30 B_f - t_launch) and n = max(0, min(cap, floor((box - start_cost) / (2 x turn_p90)))), with cap 2 for luna and 3 for ember and start_cost 6 s (resume) or 16 s (fresh fallback); n = 0 means no launch and phase 1 stands. One wall-clock deadline, T0 + 1.30 B_A1, covers resume or fallback, challenges and any phase-2 re-ask, and the process is killed there. Phase-2 and re-ask sessions run with `--output-format stream-json --verbose`, written to file as they stream; on a kill the combiner keeps every complete, parser-valid phase-2 line already streamed and drops the rest, logging `phase2_timeout` and `p2_lines_salvaged`. | Fault-injection test with `sleep`: the process dies at the deadline; a streamed fixture with 2 complete lines and 1 partial line keeps 2; unit test of n at planning values gives 2 (turn_p90 6.4 s), 1 (turn_p90 7.3 s), 1 (fallback launched at 118 s) and 0 (launch after 132.0 s) |
| R-16 | The final report holds exactly one findings-v1 block: phase-1 lines verbatim, then phase-2 lines with ids `P2-F<n>`, each validated by R-02. | Parser returns 1 block; line counts add up |

### 5.4 Redesign 2: Idle-Shift Sweeper (F4)

| Id | Requirement | Verification |
|---|---|---|
| R-17 | When ember's review exits, the harness starts an ember sweeper session with a brief limited to M1, M2 and M7 on the candidate's edited files and on its all/only sentences, plus at most one witness fact (M6 or M9 against source.md). The sweeper never receives ember's report. It is killed at T0 + (PANEL_FINISH_AT - T0 - 2 x turn_p90), and its actual start time is logged. | Launcher test; the sweeper transcript contains no read of `$OUT/<ember rid>*`; a timeout fixture kills the sweeper at the computed time |
| R-18 | The sweeper posts at most 2k facts, `kind:"fact"`, each with its command string and at most 8 `items`, and produces no findings block; a harvest hook adds paths seen in the sweeper's own output that no reviewer opened. A count fact with n = 0 is never delivered as a count; it is rendered only as the command to re-run. The sweeper is not passed to the merge. | Board count; resolution lists 3 reviewers; a fixture fact with n = 0 is rendered as its command only |
| R-19 | The luna PostToolUse hook delivers peer facts only after the reviewer's 6th tool call and after its hook-side transcript snapshot is written and hashed; no seal turn is asked of luna. If the snapshot or hash fails, nothing is delivered and `snapshot_missing` is logged. | Hook unit test with a simulated call counter and fault injection on the snapshot write |
| R-20 | Facts are dealt by the balanced online deal (fact i to luna (i + r) mod 2), and each luna receives and acts on at most k facts. Nothing is delivered after PANEL_FINISH_AT; there is no Stop hold; a fact arriving after the luna's last tool call is logged `late` and dropped. A fact may be cited only if the receiver's own transcript re-ran its command or opened its path; a re-run mismatch rate above 10% stops the arm. | Metrics: `facts_delivered <= k`, `stop_blocks = 0`, last delivery before `panel_finish_at`; first-hand audit script over hard-issue credits |

### 5.5 Board substrate, observability and elapsed-time target

<!-- Source: Base (original, modified) - read-only enforcement statement per Change #22 (V4 R-09; A-008) -->
**Read-only is enforced by audit, not by the tool list.** `--disallowedTools Edit Write NotebookEdit` blocks the editing tools, but Bash is unrestricted, so a reviewer could still write with a shell command. Read-only is therefore enforced by audit: the helpers write only under `$BOARD` (R-09); `git status` in the sandbox is clean after the last run on that sandbox; and the candidate's sha256 is unchanged.

| Id | Requirement | Verification |
|---|---|---|
| R-21 | Each reviewer gets its hooks only through a per-reviewer `--settings` JSON whose commands contain the absolute board path, the reviewer id, T0 and PANEL_FINISH_AT. Hooks read nothing from the environment. | Generated settings inspected; S0 passes on ember and luna; a run with the environment cleared still delivers a seeded message |
| R-22 | Hooks never fail the reviewer. On any hook error they print nothing, exit 0, and append to `metrics/<rid>.jsonl` with `hook_error`. | Fault injection: corrupt board line; the review completes and the error is logged |
| R-23 | Per package, the harness writes `collab.json` with these fields: arm, per-reviewer `msgs_sent`, `msgs_received`, `first_delivery_t`, `seal_t`, `resume_fallback`, `phase2_s`, `stop_blocks`, `hook_calls`, `hook_error`, `hook_ms_p95`, `reask_s`, `attempts`, `retry_s`, `retry_isolated`, `phase2_timeout`, `p2_lines_salvaged`, `n_planned`, `n_launched`, `k`, `panel_finish_at`, `finish_signal_t`, `finish_would_fire`, `hang_kill`, `snapshot_missing`, `late`, `over_cap`, plus per slot `slot_type`, `card_form`, `deal_r`, `deal_c`, plus panel `elapsed_s`, `baseline_elapsed_s`, `overhead_pct`, `own_line_jaccard`, `pairwise_task_jaccard` (descriptive only), `echo_rate`, `ledger_rows`, and the values-file sha256. | JSON schema check on every collaboration package-run and every A1 and A2 package-run |
| R-24 | Elapsed-time target: per package, `elapsed_s ≤ 1.35 × B_A1` for that package (B_A1 = the A1 median; the after-the-fact check uses the concurrent median B_c), where `elapsed_s` includes every retry attempt and every re-ask. The error budget is 1 package in 12 per arm; spending more than that stops the arm. A reviewer still running at T0 + 1.5 B_A1 is killed by the hang guard, and the package raises `SLO_BREACH`. For the mid-run designs (F3, F4, F6, F7) this budget is how the +35% cap is audited; it is not enforced by a kill. | Summary script over `collab.json`; the decision rule uses it |
| R-25 | Alarms are computed without ground truth and logged per package. `CONVERGENCE` fires when `own_line_jaccard` (Task-set Jaccard over `origin:"own"` lines only, excluding P2-F and peer-tagged lines) exceeds the A1 mean + 0.15, or when `ledger_rows` falls more than 20% below A1; an arm passes the independence guard if it fires in at most 2 of 12 runs. `ECHO` fires, on real-anchor slots only, when `echo_rate` exceeds 30% (Redesign 3) or 60% (Redesign 2). `SNAPSHOT` fires when `snapshot_missing` exceeds 50% of a mid-run arm's receiving reviewers. `flag_finding_overlap` above 50% (Redesign 4) stops and reports the arm without changing its treatment. `pairwise_task_jaccard` is logged as descriptive only. | Summary script; a fixture with copied claims triggers `ECHO`; a fixture where peer-tagged lines raise all-line Jaccard but not own-line Jaccard does not trigger `CONVERGENCE` |
| R-26 | The board directory (messages, transcript snapshots and their hashes, digests, metrics) is kept per row and package next to the reviewer outputs, and is never deleted. It is quarantined in place on contamination, following the study convention. | Directory present for every collaboration package-run |

### 5.6 Experiment conduct

| Id | Requirement | Verification |
|---|---|---|
| R-27 | Gate 0 spikes S0, S2, S3, REQ-S3, Spike 4 and Spike 5 (and S1 if F7's fallback is needed) pass and are recorded before any arm runs. | Spike notes with transcripts in the eval workspace |
| R-28 | Arms and run counts are those of section 4 (stage 1: A0 4; A1 and A2 12; A3-A6 6, extended to 12 unless stopped at the futility look; stage 2: A1-SL2 12, A2-SL2 6, F6-SL2 6 extended to 12), in block-randomised order, with `NOFALLBACK=1`, at most 10 concurrent runs and at most 4 ember. Model identity is checked per session as in `RR:51-56`, including the sweeper and phase-2 sessions. | meta.json has `model_ok:true` for every session; scheduler log shows the block order and the caps |
| R-29 | Each (arm, run, package) is judged once by the unchanged, sha256-pinned `judge-one.sh` on an anonymised merged report with random labels and with `origin` keys and board references stripped, with the per-batch API-error audit. For A3, the merged sealed phase-1 reports are also judged under separate random labels. | One score.json per (arm, run, package) plus one per A3 sealed report; API-error audit shows 0 bad |
| R-30 | Before the first arm runs, the decision rule of section 4, the analysis script (including the F7 secondary analysis) and the Spike 4 values file per package (B_A1, turn_p90, T_report_p90, PANEL_FINISH_AT, k) are committed to the eval workspace with their sha256. The values file is never recomputed during an arm. Results are reported with run-level values, Fisher and permutation p-values, H, P and C in separate columns, and the statement that the plan cannot detect the central estimates. | Commit time of the files is earlier than the first run timestamp; the values-file sha256 recorded in every `collab.json` matches the committed one |

<!-- Source: Base (original, modified) - new requirement subsections for Redesigns 1, 4 and 5 and for the shared timing guards per Change #18 (Changes 8, 13, 14, 15, 20; INV-011 at debate/round3-V1.md:38) -->
### 5.7 Redesign 1: Move Radar (F3)

| Id | Requirement | Verification |
|---|---|---|
| R-31 | The radar classifier maps tool calls to moves only through the observable signatures listed in the catalogue (M1, M2, M4, M7, "source.md opened", "unnamed test opened"). An unobservable move (M3, M5, M6, M8, M9, M10) is never described as "not done by any panel member". | Classifier unit test over a fixture transcript with one call per signature; grep of all injected texts finds "no panel member" only with M1, M2, M4 or M7 |
| R-32 | Each injection names one move id only (no Task, anchor, path or count); a Task inferred from the triggering path is written to `metrics/<rid>.jsonl` only. A reviewer receives at most k injections, at the first k of its checkpoints (ember after tool calls 6 and 10; luna after 8 and 12), with the "source.md never opened" check counted inside k; none after T0 + 1.35 B_A1 - 47 s or after PANEL_FINISH_AT. Each receiver's gap list is ordered by a hash of its reviewer id. | Leak lookup over every injected line (anything other than a catalogue move or the source.md check fails); metrics show injections per reviewer <= k and the last injection time |
| R-33 | Luna's reading-move injections are logged with `slot_type` "static" and their effect is booked to P in the results table; A6 against A2 is reported as "telemetry-timed kit against static kit". | Results table has the P column for A6 and the stated label |

### 5.8 Redesign 4: Flag-and-Adjudicate (F7)

| Id | Requirement | Verification |
|---|---|---|
| R-34 | Ember posts cards from its 3rd tool call, at most 2k per package, each with an anchor, a reading move (M3, M4, M5, M6, M9) and its `category` and `severity` enum values; a card past 2k is rejected and logged `over_cap`. Lunas post no cards, and no reviewer is held at Stop. | Board counts; validator test (R-06); `stop_blocks = 0` |
| R-35 | Card i (board append index) goes to luna (i + r) mod 2 and is rendered in challenge form (anchor plus required finite check) when (i + floor(i/2) + c) is even, otherwise in finding form (anchor plus ember's category and severity, never a claim); r and c are seeded 0/1 coins per run, logged as `deal_r` and `deal_c`. | Unit test: with r = c = 0 and i = 0..3, recipients are A, B, A, B and forms C, F, F, C; with c = 1 forms are F, C, C, F; at k = 2 each luna gets one card of each form |
| R-36 | Per card slot the harness logs form, recipient, card Task, conversion (the receiver's line overlaps the card anchor by at least 12 characters), judge-credited conversion and uncredited conversion. The secondary analysis (conversion by form, two-proportion test, run-paired difference) is pre-registered under R-30. | `collab.json` schema check; the committed analysis script |
| R-37 | `flag_finding_overlap` is computed per arm; above 50% the arm stops and is reported, and its treatment is never changed partway. If `cards_sent = 0` in more than 50% of runs, the arm stops. | Summary script over `collab.json` with fixtures for both stop conditions |

### 5.9 Redesign 5: Coverage Deflection (F6)

| Id | Requirement | Verification |
|---|---|---|
| R-38 | The watcher triggers on each luna scout's exit, parses that luna's findings block into (Task, category) pairs of non-surface findings (the surface regex excludes path, hash and line-number claims), and posts a card that requests only Tasks with no peer finding, ranked by the lunas' declared not-checked scope. Cards carry no counts, no categories and no covered list; no telemetry and no `SendMessage` are used. | Watcher unit test with fixture blocks: a Task covered only by a surface finding stays uncovered; the card contains Task ids only |
| R-39 | Each card lists at most k requests and sonnet acts on at most k in total per package, with k computed from SL2's B_A1 and sonnet's turn_p90 and T_report_p90. The F6 arm runs only if Spike 4 gives sonnet a T_report_p90 of at most 51.8 s. Sonnet's brief contains the line "peer coverage is not clearance". | Values file; brief grep; metrics of requests delivered and acted on |
| R-40 | A deflection alarm fires if sonnet's anchored Tasks overlap the Tasks the lunas covered by more than 50%, or if the panel's union of anchored Tasks shrinks against A1-SL2. | Summary script with a fixture for each condition |

### 5.10 Timing guards and run accounting (every arm)

| Id | Requirement | Verification |
|---|---|---|
| R-41 | `PANEL_FINISH_AT = T0 + 1.35 B_f - turn_p90 - T_report_p90` is baked into each reviewer's settings in every mid-run arm. After it, the hook injects "finish now with what you have", nothing more is delivered and the helpers refuse to post; the time is logged as `finish_signal_t`. A1 and A2 log `finish_would_fire` (a luna still running at PANEL_FINISH_AT) without acting on it. | Hook unit test with a clock fixture; `collab.json` fields present in every arm |
| R-42 | k = max(0, min(2, floor((0.35 B_A1(pkg) - 2 s - turn_p90 - T_report_p90) / (2 x turn_p90)))) per package, from the values file. A package with k = 0 counts as isolated for that design, and the dilution is reported. | Unit test: B = 116 s with 6.4/6.4 gives 2; T_report_p90 = 11.0 s gives 1; B = 100 s gives 1 only if T_report_p90 <= 13.8 s; SL2 with turn 14 s gives k >= 1 only if T_report_p90 <= 51.8 s |
| R-43 | Every arm, A1 included, kills a reviewer still running at T0 + 1.5 B_A1 and logs `hang_kill`; the package counts as `SLO_BREACH`. | Fault injection with a hung reviewer in A1 and in a design arm |
| R-44 | `elapsed_s` sums all attempts of the `RR:61-64` retry loop, with `attempts` and `retry_s` logged. In a collaboration arm, attempt 2 runs with `PANEL_COLLAB=0` for that reviewer and is logged `retry_isolated`. | Fault injection of a failed block check: two attempts summed; no delivery in attempt 2 |
| R-45 | Spike 4 measures each design brief's slowdown s over A1 on the critical-path role. A design whose budget B_A1 x (1 + s) + W exceeds 1.35 B_A1 drops brief content until it fits (limits: F4 and F7 5.7%, F3 11.2%, F6 13.8%). `baseline_drift = B_c / B_f` is logged per randomised block, and a block outside [0.963, 1.10] is reported but not used for the time verdict. | Spike 4 record; summary script |
| R-46 | Session cleanup deletes only the session ids recorded in that run's `collab.json`, after every concurrent run on that sandbox has ended, and never the session directory; `git status` in the sandbox is checked after the last such run. | Cleanup test with two concurrent runs on one sandbox: the other run's resume still succeeds |
| R-47 | Every act-rate factor used in a gain row (0.5-0.85) is a planning value; before results are compared with the gain ranges, it is replaced by the act rate REQ-S3 measured, including the act rate on "finish now". | The results report lists each measured act rate beside the planning factor it replaces |

---

<!-- Source: Variant 5 (sonnet:performance), V5:538-545 (itemised unverified list, S-006), with the base list (V4:750-759) and T_report_p90 from debate/round3-V2.md - merged per Change #21 -->
**Not checked in this specification: every unmeasured number, and what replaces it.**

| Unmeasured item | Where it is used | Value used here | Replaced by |
|---|---|---|---|
| T_report_p90 (luna's and sonnet's final report turn at p90) | PANEL_FINISH_AT, k, every mid-run time block, F6's run condition | 6.4 s for luna (the mean turn); none for sonnet | Spike 4 |
| turn_p90 per model | k, F1's n, every time block | luna 6.4 s, sonnet 14 s, ember 3.2 s (medians, not p90) | Spike 4 |
| Act rates of gateway models on injected or delivered items | every gain chain (0.5-0.85) | planning ranges per design | REQ-S3 |
| Act rate on "finish now" | whether the finish-signal bound holds | assumed within one turn | REQ-S3 |
| `--resume` on gateway model ids, and the 6 s resume and 16 s fallback start costs | F1, every H2 re-ask | 6 s and 16 s | S2 (and S0 for start times) |
| stream-json text arriving before exit on luna | F1 salvage on a kill | assumed | S2, S3 |
| Hooks firing, hook timeout, hook cost (about 0.1 s per call, 2 s per package), and hook commands needing nothing from the environment | every mid-run design | 2 s per package | S0, Spike 4 |
| Per-package B_A1 after the harness fixes | every cap, deadline and k | planning 116 s (EL2) and 273.7 s (SL2), three-package means without H; historical per-package medians 100-122 s on EL2 | Spike 4 and arm A1 |
| Elapsed cost of the static kit (about +29%) and of each design's brief | slowdown limits, A2 row | V5's estimate | Spike 4 |
| The k = 1 gain rows (each k = 2 row halved) | F3, F4, F7 gain blocks | planning halving | the arm's logged delivered-item counts |
| F6 gain re-derived for SL2 (low = base low x 0.5) | F6 gain block, §3 | 0.13-1.06 (k = 2), 0.07-0.53 (k = 1) | the stage-2 screen |
| H share for SL2 | F6, §3 | +0.1 to +0.4 | arm A1-SL2 against historical SL2 runs (no bottom-up table exists) |
| H2's part of H on cheap panels | H table | +0.03 (0.00-0.10) | Spike 5 |
| Token overheads of F6 on SL2 and F7 on EL2 one way | §3 | not re-derived | the arms' measured output tokens |
| c per move, P, and every gain range | catalogue, (f) blocks | judgment built from near-miss counts and sonnet's reach | the experiment; the sample (3 packages, 10 hard issues) cannot calibrate them |
| The base commit for each package's sandbox | H3 | not recorded in an obvious file for any of the three packages | manual resolution, recorded in the manifest (R-03) |

Risks:

- The plan cannot detect the central gain estimate of any slot (section 4); only large effects separate from noise at n = 12.
- The study showed that a single strong run regresses to the mean (`CR:424`).
- The move catalogue was abstracted from the same three packages, so in-sample gains are optimistic until confirmed on two new packages.
