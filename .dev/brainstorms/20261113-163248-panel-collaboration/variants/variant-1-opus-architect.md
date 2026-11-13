# Requirements specification: tasklist review panel with reviewers that collaborate during their runs (variant 1, architect view)

Evidence keys used throughout (all paths relative to the worktree root):

| Key | Path |
|---|---|
| SEED | `.dev/brainstorms/20261113-163248-panel-collaboration/seed-brief.md` |
| INV-DS | `.dev/brainstorms/20261113-163248-panel-collaboration/enrichment/investigation-designspec.md` |
| INV-AC | `.dev/brainstorms/20261113-163248-panel-collaboration/enrichment/investigation-alias-control.md` |
| INV-PAT | `.dev/brainstorms/20261113-163248-panel-collaboration/enrichment/investigation-patterns.md` |
| RES | `.dev/brainstorms/20261113-163248-panel-collaboration/enrichment/research-light.md` |
| CR | `.dev/eval-workspaces/tasklist-review-panel/20261111-a1/COMBO-REPORT.md` |
| HO2 | `.dev/eval-workspaces/tasklist-review-panel/HANDOFF-review-panel-unification-run2.md` |
| RR | `.dev/eval-workspaces/tasklist-review-panel/20261111-a1/tools/run-reviewer.sh` |
| JO | `.dev/eval-workspaces/tasklist-review-panel/20261111-a1/tools/tmp-scripts/judge-one.sh` |

Issue labels follow CR:401-417: B1-B5 and I1-I5 are designSpec GT1-GT10, B6-B8 and I6 are alias GT1-GT4, and I7-I8 are control GT1-GT2. "Found /14" counts the two defect-rich packages (designSpec and alias). I7 is scored separately under "control found /2".

---

## 1. Theories

The three seed theories hold up against the evidence. I keep all three, sharpen T1 and T3, and fold a fourth candidate (reasoning budget, INV-PAT:147-151) into T2 as a modifier, not a separate cause. Thinking tokens explain haiku's variance, but hard-issue hits for ember and luna stay flat as thinking rises (ember 0.25 to 0.22, luna 0.09 to 0.09 per run, INV-PAT:151).

### Theory 1 (refined T1): the evidence set is bounded by the plan, and the two halves of the missing move sit in different models

Cheap reviewers check the files and lines the plan names. They never build an inventory of what a universal claim covers, and they never run a reverse-dependency sweep (who references the files this plan edits?). The refinement is that the missing capability has two halves, and different cheap models hold different halves:

- **Searching beyond the plan.** haiku and ember have this. haiku searches tests/ in 81% of runs and ember in 49% (INV-PAT:31-33).
- **Opening and reading an unfamiliar file whole.** luna has this: it does a median of 11 Reads per run (INV-PAT:19).

No single cheap model has both halves.

| Evidence | Number | Source |
|---|---|---|
| `tests/skills/test_worker_contract.py` opened by cheap control reviewers | 0 of 176 (ember 0/69, luna 0/82, haiku 0/25) | INV-PAT:43-45 |
| Runs that opened it and then reported I7 | 7 of 8 (sonnet 7, grok 1); 0 of the 225 runs that never opened it | INV-PAT:132 |
| haiku runs where the file appeared in grep or ls output but was never opened | 5 of 11 | INV-AC:66 |
| Files touched per run that the plan does not name | sonnet 3.1, haiku 0.9, ember 0.8, luna 0.3 | INV-PAT:43-47 |
| `CHANGELOG.md` touched (needed for I5) | 1 of 233 designSpec runs, and that run was grok | INV-PAT:134 |
| Cheap alias reviewers who saw the narrowed `refs/tiers.md:42` sentence without comparing it to Task 7's broader claim | 44 of 98 | INV-AC:67 |

- **Explains:** I7, I5, B8, and B6 through its repo route.
- **Partly explains:** I6.
- **What it predicts for collaboration:** sharing *search output* (paths seen) from a searcher with a *reader* should convert some seen-but-unopened files into opened files. This is a complementarity that collaboration can exploit and a single static checklist cannot.

### Theory 2 (accepted T2): right place, wrong question (one-axis analysis at the correct anchor)

Cheap reviewers often anchor the right sentence, ask one local question and stop. They do not trace other branches, the other direction of completeness, satisfiability, or the same constraint in other tasks.

| Evidence | Number | Source |
|---|---|---|
| Cheap findings anchored on the exact GT10 sentence | 16 (15 ember, 1 haiku); all ask "does the grep over-match", none ask "where else is the claim" | INV-DS:103 |
| GT5 near misses | 3 findings on the exact mapping; all trace only the mode-off case, none the halt path | INV-DS:105 |
| GT6 near miss | 1 (haiku g7-r1 M2, right row, different question) | INV-DS:106 |
| ember anchoring designSpec Task 1 | 52% of runs; the unbounded-inventory defect stated in 3%; 0 anchors on AC3/O3 in any panel | INV-PAT:111, :140; INV-DS:104 |
| Cheap reviewers who compared Task 6 mapping text against the Constraint (B7) but never repeated the check on Task 7 (I6) | several (luna h1-r2, luna g7-r2, ember h1-r4) | INV-AC:69 |
| luna reached B6's evidence (chains.md `/model` lines) but framed it as "unclear exemption" | 1 run | INV-AC:102 |

- **Explains:** B1, B2, B5, I1, I4, I5, I6.
- **Partly explains:** B6.
- **What it predicts for collaboration:** a peer's anchor tells another reviewer *where* attention already landed. Sending a *different generic move* to that region (not the peer's conclusion) should convert near misses. This is the strongest lever, because the cheap models already reach the right anchors.

### Theory 3 (refined T3): the evidence environment masks defects and the reporting filter drops the rest

The sandbox and the grading rules hide or suppress defects regardless of how the models collaborate. The refinement is that this is a confound every design must remove *before* measuring collaboration; collaboration cannot fix it.

| Mechanism | Evidence | Source |
|---|---|---|
| The checkout is taken after implementation, so repairs mask defects | `refs/merge-guard.md:146` repairs GT5 (B5); `merge_guard.py:256` repairs GT6 (I1); `commands/pr-submit.md:81` makes the GT9 (I4) grep pass; `refs/tiers.md:42` is already narrowed (B8); haiku and luna spend findings on "already exists" | INV-DS:14-20, :142; INV-AC:9, :73-91 |
| source.md is not named in the brief | 156 of 665 runs never referenced it (ember 39%, luna 22%); GT5 and GT6 need it | CR:373; INV-DS:79 |
| The grading rule and the report shape | An unstated requirement is graded Medium and there is no missing-task category. luna marks 72% of findings blocking at 1.75 findings per run. grok saw `CHANGELOG.md:166` and dropped it as "minor". All 7 true I7 findings were non-blocking | INV-PAT:61-65, :161; INV-DS:126; RR:15-17 |
| The merge drops long findings | Anchors over 200 or claims over 300 characters drop the finding; 49 blocking findings lost (luna 30, ember 33) | CR:292; HO2:162 |
| The `.dev/reflect` leak | `.dev/reflect/pre-design-20261108041729/REPORT.md` names I7; 2 of the 9 I7 credits read it (clean count 7) | INV-AC:125 |

- **Explains:** I1, B5, I4 and B8 (masking); I5 and I7 (filtering).
- **Effect on everything else:** it lowers every number.

### Issue-to-theory map

| Issue | Found by other panels (source.md era, 76 runs; CR:498) | Primary theory | Secondary | Generic move that finds it (catalogue in section 2.0) |
|---|---|---|---|---|
| B1 designSpec GT1 | 0 | T2 | T3 (grading frames "wrong build", not "unending verification") | M1 stopping rule |
| B2 designSpec GT2 | 0 | T2 | T1 (needs source.md:341 comparison) | M9 scope match |
| B5 designSpec GT5 | 3 | T2 | T3 (repaired ref, source.md skipped) | M7 every branch, M10 source-rule audit |
| B6 alias GT1 | 1 | T2 | T1 (repo route via chains.md) | M3 quantifier inventory |
| B8 alias GT3 | 1 | T1 | T3 (tiers.md:42 already narrowed) | M3 quantifier inventory |
| I1 designSpec GT6 | 3 | T2 | T3 (merge_guard.py:256 repaired) | M6 producer-consumer |
| I4 designSpec GT9 | 4 | T2 | T3 (implemented heading passes the grep) | M2 literal command |
| I5 designSpec GT10 | 0 | T1 | T2 (direction), T3 (minor dropped) | M5 other direction |
| I6 alias GT4 | 0 | T2 | none | M8 constraint sweep |
| I7 control GT1 | 9 (7 clean) | T1 | T3 (missing-task graded Medium; leak) | M4 reverse dependency |

---

## 2. Five redesigns

### 2.0 Shared scaffolding (built once; every design below is a policy on top of it)

The architect's choice is one small set of shared parts plus a policy per design. The alternative, five separate harnesses, would drift. Each design differs only in *who sends what kind of message, when, and how many*. The parts:

**Harness-fix bundle H (applies to every arm, including the isolated control).** These are the four named fixes. Their effect is reported separately from collaboration.

| Id | Fix | Where | Removes |
|---|---|---|---|
| H1 | Name `source.md` by absolute path in the brief, and require the reviewer to read it | RR:13-17 brief text | T3 source-blind runs |
| H2 | Before the merge, truncate `anchor`/`anchor2` to 200 and `claim` to 300 characters (a prefix of an exact quote is still an exact quote). Validate the block with the merge parser at run time and re-ask once if any line still drops | RR:50-57 plus a new pre-merge step | T3 merge drop (HO2:162) |
| H3 | Pre-implementation checkout: one sandbox per package at the plan's base commit (the parent of the first implement commit), recorded in the manifest | RR:48 `cd` target; manifest.md:10 | T3 masking |
| H4 | Remove `.dev/reflect/` from every sandbox | sandbox build | T3 leak |

The grading-rule problem (Medium for an unstated requirement) is **held constant** in every arm, so the experiment does not mix a rubric change with collaboration. It is listed as follow-up work in section 4.

**Move catalogue (`moves.json`, frozen before any run).** Hints exchanged between reviewers are always a catalogue id plus a scope (a task or section heading of the candidate). They are never free text. Every move applies to any plan.

| Id | Generic move (text shown to reviewers) |
|---|---|
| M1 | For each criterion that says every, all, complete or no remaining, state the finite check that proves it and who decides it is done. |
| M2 | Run or simulate each command or grep criterion against the exact text the task tells the implementer to write, not against the current file. |
| M3 | For each sentence with all, only, every or none, list what it ranges over and count the exceptions in the plan and the repo. |
| M4 | For each file the plan edits, search tests/ and docs for references to it; open every referencing file the plan never names; check that the plan's gate runs it. |
| M5 | When you checked that a check is not too broad, check that it is not too narrow: where else in the repo is the same claim or value stated? |
| M6 | For every value a mapping or reader consumes, find the step or table row that produces it, using the source document, not the checkout. |
| M7 | Trace each input case, halt reason or branch through a mapping, not only the first one you analysed. |
| M8 | Take each stated constraint and test every piece of text the plan dictates against all of its clauses, in every task. |
| M9 | Compare the scope in each task body with the scope of its acceptance criteria and with the scope in the source document. |
| M10 | Walk each rule in the source section a task implements and confirm that the plan carries it. |

Overfitting guard: the catalogue, brief additions and card templates must contain no file path, backticked identifier or task-specific term taken from the three candidates (a mechanical deny-list check, REQ-C2). The moves were *abstracted from* the missed-issue investigations, so the overfitting risk is real. Section 4 states the limit.

**Message envelope `panel-msg/1`** (one JSON line, no free-text field in any kind):

```json
{"v":"panel-msg/1","run":"<row>/<pkg>","from":"t4-1","seq":2,"ts":"2026-11-14T10:00:00Z","kind":"coverage|evidence|scout_map|request","scope":["Task 7"],"move":"M3","paths":[],"items":[]}
```

**Board.** `$PANEL_BOARD/<from>.jsonl` sits under `/tmp/panel-board/<row>/<pkg>/`, outside every sandbox and outside EVAL. There is one writer per file, appends are a single `>>` of one line, and every write goes through one validator. Receivers get unread lines through a `PostToolUse` hook that returns `additionalContext`, plus one final `Stop` hook check (RES:177-207).

**Deadline rule.** `PANEL_T0` is the launch time of the row-package. The harness passes `PANEL_FINISH_AT = T0 + 1.20 x B`, where B is the named baseline's per-package elapsed time. After that point the hook injects "finish now with what you have", the Stop hook never blocks, and the send helper refuses. The remaining 15% of B is headroom for writing the final report.

**Convergence alarm (common, computed from the panel's own outputs, never from ground truth).**

- J = mean pairwise Jaccard of the task sets anchored by reviewers in one run.
- Isolated references: luna+luna 0.33, ember+luna 0.25, haiku+luna 0.23 (INV-PAT:81-85).
- **Alarm** when, over an arm, mean J exceeds its isolated reference by more than 0.15, OR the panel's distinct tasks anchored per run fall by more than 20% against the isolated arm, OR more than 50% of post-exchange findings cluster in the merge with a peer's pre-exchange finding (echo rate).

---

### 2.1 Redesign R1: Coverage board (move cards that steer peers away from what is already covered)

**(a) Mechanism.** Every reviewer reviews normally. At fixed points it posts a coverage card ("I ran move M on scope S"), never a result. The hook shows each reviewer a short table of peers' cards and the *gaps*: catalogue moves crossed with candidate regions that nobody has covered yet. A reviewer may take a gap, and is told that a region one peer covered with move M still needs a *different* move from someone else.

- Panel: ember + 2x luna (named baseline S07, CR:441).
- **ember** is the early scout. It is fast (41 s median, INV-PAT:19), so its cards arrive first and shape the lunas' second half.
- **luna** reads named files whole. It mostly receives gaps and spends one or two moves on them.

Target theory: T2 (a different move on the same region) and some T1 (gaps that point to M4 and M5).

**(b) Communication schedule.**

| Trigger | Who | Sends | Maximum |
|---|---|---|---|
| After the first read of the candidate and source.md, and at least 6 tool calls (first-pass gate) | each reviewer | 1 coverage card | 1 |
| After finishing each move it chose itself | each | 1 coverage card | ember 3 total, luna 2 total |
| Every tool call of the receiver | hook | unread peer cards plus a gap list (at most 5 region-move pairs) | injection of at most 600 characters |
| Stop (before PANEL_FINISH_AT) | Stop hook | block once if open gaps exist and none was taken | 1 per reviewer |

Per reviewer per package: at most 3 sent (ember) or 2 sent (luna). Each card is at most 300 bytes. Schema: `kind:"coverage"`, `scope` (at most 3 task ids), `move` (catalogue id).

**(c) Transport.** JSON board plus a PostToolUse hook, with a `panel-post` helper for sending. Receiving is handled by the CLI, so it does not depend on whether a gateway model remembers to poll (RES:177-207). Cross-session messaging was rejected for R1 because cards must reach several peers and leave an audit file. Orca mail has no per-reviewer mailbox for `claude -p` (RES:38-49), and A2A cannot inject into a running turn (RES:144-149).

**(d) Time budget.** Baseline S07 is ember + 2x luna, 348 s over 3 packages, so B = 116 s per package (CR:331). The cap is 1.35 x 116 = 156.6 s. Per-turn times: ember 41 s / 13 turns = 3.2 s; luna 102 s / 16 turns = 6.4 s (INV-PAT:19-20).

| Reviewer | Isolated end | Sending | Gap work | New end |
|---|---|---|---|---|
| ember | 41 s | 3 posts x 3.2 s = 10 s | 2 moves x 2 turns x 3.2 s = 13 s | 64 s (idle time absorbs it) |
| luna A | ~100 s | 2 x 6.4 s = 13 s | 1 move x 2 turns x 6.4 s = 13 s | ~126 s |
| luna B (critical path) | 116 s | 13 s | 13 s | **142 s = +22%** |

The hard limit is the finish signal at 1.20 x 116 = 139 s plus at most 17 s for the final report, which is 156 s or less.

**(e) Contamination safeguards.**

- **Shared:** move ids and scopes only.
- **Withheld:** claims, severities, blocking flags, anchors, and any "this is fine" statement (the schema has no field for one).
- **Independent first pass:** the hook delivers nothing until the receiver has made 6 tool calls and posted its own first card.
- **Blind-spot spread:** the danger is a peer's card on a region making the others skip it, as in ember's "correctly defers O1-O4", INV-DS:91. To prevent this, gaps are counted per region-move *pair*, a region covered by one move remains a gap for every other move, and cards cannot express approval.
- **Convergence:** common alarm, plus a per-run check that no catalogue move was run by all three reviewers on the same scope.

**(f) Expected gain.**

| Target | Theory | Assumption | Added per run (low-high) |
|---|---|---|---|
| I5 | T2, T1 | a gap nudge sends M5 to Task 2; conversion 0.1-0.3 | 0.05-0.15 |
| I4 | T2 | M2 taken on a command criterion in Task 12 in some runs; detection 0.3-0.5 once taken | 0.03-0.10 |
| B5, I1 | T2 | M7/M6 on mapping sections; cheap conversion rates under sonnet's (2/26, 1/26) | 0.02-0.08 |
| B6, B8 | T1 | M3 taken on "only/all" sentences | 0.00-0.05 |
| B1, B2 | T2 | M1/M9; never found by any model | 0.00-0.05 |
| **Collaboration share** | | | **+0.10 to +0.43** |
| Harness share (H1-H4, same for all designs) | T3 | see note below the table | +0.2 to +0.5 |
| **Total vs S07 1.83/14** | | | **2.1 to 2.8** |

Harness-share assumptions:

- **H1:** lifts source.md use to at least 95% but adds little on its own (+0.0 to 0.1).
- **H2:** recovers some of the 49 blocking findings that were dropped (+0.05 to 0.2).
- **H3:** removes the masks on B5, I1, I4 and B8, and the "already exists" noise (+0.1 to 0.2).
- **H4:** changes 0 on /14. It changes only sonnet-panel I7 credits on control.

**(g) Effort.**

| New or changed file | Rough lines |
|---|---|
| `moves.json` | 45 |
| `panel-post` helper | 30 |
| `hook-post.sh` | 50 |
| `hook-stop.sh` | 25 |
| policy file | 15 |
| RR edits (exports and `--settings`) | 15 |
| new `run-panel.sh` (launches one row-package with a shared board and T0) | 50 |
| brief text | 10 |
| `board-audit.py` | 120 |

Total about 360 lines, of which about 240 are shared with R2 and R4.

**(h) Failure modes.**

- Weaker models skip posting cards. Then there are no gaps and R1 behaves like the isolated panel.
- Cards are posted with invalid move ids. The helper rejects them and the run continues.
- Hook environment inheritance has not been verified (RES:206-207). A failure means silent non-delivery, so a spike is required.
- Cards act as "done" signals that end exploration early.
- The gap list nudges every luna to the same top gap. Mitigation: gaps are ordered differently per receiver, using a hash of the receiver id.

---

### 2.2 Redesign R2: Evidence trail (search exhaust from searchers, read by readers)

**(a) Mechanism.** A PostToolUse hook on every reviewer *automatically* logs the repo paths that appear in its tool output (grep -l, ls, rg results) and the paths it opened (Read, cat, sed). No model has to remember to send anything. Each receiver's hook computes "seen by a peer, opened by nobody, not named in the plan" and injects up to 8 such paths, test files and root-level docs first. Paths are split between receivers by hash, so each luna gets a different subset.

- Panel: haiku + 2x luna (named baseline S24, CR:458).
- **haiku** is the searcher. Its grep output listed `test_worker_contract.py` in 5 of 11 runs (INV-AC:66).
- **luna** is the reader. It opens files whole.
- **Variant:** ember + 2x luna, with ember as the searcher. This only works when M4 is in ember's brief, because the brief makes ember search tests/.

Target theory: T1, specifically the split between searching and reading.

**(b) Communication schedule.**

| Trigger | Who | Sends | Maximum |
|---|---|---|---|
| Every tool call (automatic) | hook of each reviewer | evidence line: paths seen, paths opened | 1 line per tool call, at most 16 paths, at most 1,200 bytes |
| Tool call of the receiver, once at least 5 calls are made (first-pass gate) | hook | at most 8 paths that are seen by a peer, opened by nobody, and not named in the plan | 3 injections per reviewer per package, each at most 600 characters |
| Stop (before PANEL_FINISH_AT) | Stop hook | block once if any injected path is still unopened | 1 |

Schema: `kind:"evidence"`, `paths` (seen), `items` (opened). There is no `move` field and no text.

**(c) Transport.** JSON board plus hooks. This is the only transport where *both* sending and receiving need no cooperation from the model, which matters because luna rarely uses Bash (1 call per run, INV-PAT:20). Cross-session messaging needs the sender to call a tool. A between-phase digest arrives too late, because luna would already have finished.

**(d) Time budget.** Baseline S24 is haiku + 2x luna, 715 s over 3 packages, so B = 238 s per package (CR:319). The cap is 321 s. Per-turn time: haiku 233 s / 10 = 23 s.

| Reviewer | Isolated end | Hook overhead | Extra opens | New end |
|---|---|---|---|---|
| luna A and B | ~110 s | about 2 s | 3 x 6.4 s = 19 s | ~131 s (idle until haiku finishes) |
| haiku (critical path) | 233 s | about 2 s | 2 x 23 s = 46 s | **281 s = +18%** |

The finish signal is at 1.20 x 238 = 286 s. Variant ember + 2x luna: luna B ends at 116 + 19 + 2 = 137 s, which is +18%.

**(e) Contamination safeguards.**

- **Shared:** repo-relative paths only.
- **Withheld:** file content, the reason a file was searched, and every judgment.
- **Independent first pass:** the gate is 5 tool calls, and the plan-named files are already read by then.
- **Blind-spot spread:** limited by construction. A path list carries no conclusion, and assigning paths by hash prevents all lunas opening the same file.
- **Measurable risk:** "trail tunnelling", where too many reads go to injected paths. Alarm if more than 40% of a reviewer's post-gate Reads are injected paths. Common convergence alarm also applies.

**(f) Expected gain.**

| Target | Theory | Assumption | Added per run |
|---|---|---|---|
| I7 (control /2) | T1 | P(test file in haiku output) 0.45 (5/11); P(luna opens it when injected) 0.7; P(reported once opened) 0.5-0.85 (sonnet 7/8, but luna reports Medium items rarely, T3) | **control +0.15 to +0.35** |
| I5 | T1 | needs a peer's repo-wide grep that includes root files; observed in 1 of 233 runs | 0.00-0.10 |
| B6, B8 | T1 | seen paths do not drive the quantifier comparison (44/98 already saw tiers.md) | 0.00-0.05 |
| **Collaboration share /14** | | | **+0.00 to +0.15** |
| Harness share | T3 | as in R1; H4 has no effect on cheap I7 (baseline 0) | +0.2 to +0.5 |
| **Total vs S24 2.2/14** | | | **2.4 to 2.85; control +0.15 to +0.35** |

**(g) Effort.** `hook-post.sh` gains a path extractor that only keeps paths existing in the sandbox (about 70 lines), plus the shared bus, `run-panel.sh` and the audit. Total about 300 lines, of which about 200 are shared.

**(h) Failure modes.**

- The path extractor misses paths in unusual outputs, such as codegraph JSON.
- Plan-named filtering fails on relative versus absolute forms. Fix: normalise paths against the sandbox root.
- haiku's slow turns cap it at 2 extra opens.
- luna opens the file but does not report a Medium missing-task item (T3 reporting filter).
- Paths that differ between per-package sandboxes (H3) must not mix. Fix: one board per package.

---

### 2.3 Redesign R3: Cross-examination round (resume with challenge cards built from peers' anchors)

**(a) Mechanism.** Phase 1 is the normal isolated review: unchanged brief, H1-H4, and the same catalogue text as the comparison arm. When a reviewer finishes phase 1, the harness parses its findings-v1 block with the merge parser and records only *which candidate regions it anchored and with which category*. Each reviewer is then resumed (same session, so no re-reading) with at most 3 challenge cards. A card is "run move M in region S".

- **Peer-anchor cards:** a region a *peer* anchored and this reviewer did not. The move is chosen to complement the peer's category: a peer `contradiction` or `other` leads to M5 or M7, and a peer `missing-requirement` leads to M1 or M2.
- **Gap card:** one region that nobody anchored, with the move chosen from text features of the candidate section by fixed regexes, such as "every|all|complete" leading to M1/M3, a backticked grep or pytest leading to M2, and "mapping|returns" leading to M7/M6.
- Phase 2 may only *add* findings. Phase 1 findings are frozen.
- Panel: ember + 2x luna (named baseline S07). ember is the first finisher and receives luna regions. Each luna receives ember's regions, which are dense (4.6 tasks anchored per run, INV-PAT:63), and the other luna's regions.

Target theory: T2 above all. The near-miss census (16 GT10, 3 GT5, 1 GT6) shows peers *are* anchoring the right regions, and the card sends a *different* move there.

**(b) Communication schedule.**

| Trigger | Who | Sends | Maximum |
|---|---|---|---|
| A reviewer's phase 1 ends and at least one peer's phase 1 has ended | harness `digest.py` | card file for that reviewer, built from all peer blocks finished so far | 1 digest per reviewer per package |
| Phase 2 (`claude -p --resume <session_id>`) | reviewer | additional findings in its own block, ids X1..Xn | 3 cards in, at most 5 new findings out |
| Last peer finishes after a reviewer's phase 2 started | none | late anchors are not delivered | none |

Card schema `panel-card/1`: `{"card":"C1","to":"t3-1","scope":["Task 2"],"move":"M5","origin":"peer-anchor|gap"}`, at most 200 bytes, at most 3 per reviewer.

**(c) Transport.** A between-phase digest plus `--resume`. Every delivery is done by the harness, so no hooks are needed, nothing depends on gateway tool use, and the most reliable option in RES:235-240 is used. It is chosen because R3's input is *finished findings blocks*, which only exist at phase ends.

Required change: RR:48 passes `--no-session-persistence`, which prevents `--resume`. The flag must be dropped for phase 1 in this arm, and the session id read from the JSON result.

**(d) Time budget.** Baseline S07, B = 116 s per package. The guarantee is built into the design: let T1 be the moment the last reviewer's phase 1 ends, which equals the isolated elapsed time of that run. No phase 2 may run past `1.35 x T1 - 2 s` (it is killed by `timeout` and falls back to the phase-1 report). Total elapsed is therefore at most 1.35 x T1 on every run, not just on average.

| Reviewer | Phase 1 end | Phase 2 starts | Phase 2 window | Ends |
|---|---|---|---|---|
| ember | 41 s | ~102 s (first luna done; idle time otherwise) | at most 38 s (~12 ember turns) | ~140 s |
| luna A | ~100 s | ~102 s (has ember's anchors) | at most 40 s (~6 turns) | ~142 s |
| luna B (critical path) | 116 s | 118 s (digest at most 2 s) | 156 - 118 = 38 s (~5-6 turns) | **at most 156 s = +34.5% hard; expected ~150 s = +29%** |

A slow luna B (for example 150 s) leaves earlier reviewers' phase 2 untouched. It still gets 0.35 x 150 = 52 s of its own window, because the window scales with T1.

**(e) Contamination safeguards.**

- **Shared:** region ids and move ids only.
- **Withheld:** peers' claims, anchors, severities, blocking flags and verdicts. The digest builder reads them only to compute regions, and they never leave the harness.
- **Independent first pass:** guaranteed. Phase 1 completes with no input at all, and its block is stored byte for byte before phase 2.
- **Blind-spot spread:** a peer's silence never becomes a card ("nobody flagged it" sends a gap card *toward* a region, never away). Cards come only from regions *some* reviewer anchored or *nobody* anchored, so they spread attention instead of narrowing it.
- **Measurable checks:** the echo-rate alarm (phase-2 findings clustered with a peer's phase-1 row, alarm above 50%), plus the common J alarm.

**(f) Expected gain.**

| Target | Theory | Assumption | Added per run |
|---|---|---|---|
| I5 | T2 | about 0.45 of cheap designSpec runs carry a GT10-region anchor (16 findings over 30 runs); a peer gets that region with M5; conversion 0.15-0.4 (repo-wide including root, then not dropped as minor) | 0.07-0.18 |
| B5 | T2, T3 | GT5-region anchor in about 0.1 of runs plus the "mapping" text-feature route; M7 with source.md; conversion 0.2-0.4 | 0.03-0.09 |
| I4 | T2, T3 | Task 12 command criterion chosen by M2 with probability 0.2-0.4; detection 0.3-0.5; H3 removes the false pass | 0.04-0.12 |
| I1 | T2 | M6 on Task 3 through the text-feature route; tabulation is hard for cheap models | 0.02-0.06 |
| I6 | T2 | needs a peer's B7-type anchor (B7 in 20 of 76 runs, CR:498), then M8 to another reviewer; never found by anyone | 0.00-0.08 |
| B1, B2, B6, B8 | T2, T1 | M1 or M3 through gap cards; never or once found | 0.00-0.10 |
| **Collaboration share /14** | | | **+0.15 to +0.6** |
| Harness share | T3 | as in R1 | +0.2 to +0.5 |
| **Total vs S07 1.83/14** | | | **2.2 to 2.9** |

The static catalogue arm (section 4, arm A2) measures how much of this a checklist in the brief would capture without any exchange. R3's specific claim is the *region pointer*, which a static checklist cannot supply.

**(g) Effort.**

| New or changed file | Rough lines |
|---|---|
| `digest.py`: parse blocks, locate anchors to sections, build cards, deny-list check | 90 |
| RR phase-2 path: resume, `timeout` set by T1, fall back to phase-1 report | 40 |
| `combine-blocks.sh`: merge phase-1 and phase-2 lines into **one** findings-v1 block, because the parser treats more than one block as invalid (HO2:336) | 35 |
| `run-panel.sh` with phase staggering | 60 |
| `moves.json` | 45 |
| audit additions | 40 |

Total about 310 lines, and no hooks.

**(h) Failure modes.**

- `--resume` has not been verified with gateway model ids (spike required).
- A resumed luna rewrites or restates phase-1 findings. Fix: combine-blocks keeps only X-prefixed new ids, and the audit counts duplicates.
- Card regions are wrong when anchors are not found in the candidate (46 unanchored rows, HO2:167). Fix: skip those findings.
- Phase 2 is killed at the cap, so its work is lost. This is a fail-open, and the run still counts.
- Resume replays the whole history as input tokens, which costs money but is not counted in the study's output-token metric.

---

### 2.4 Redesign R4: Scout and split (ember posts a structural map, the two lunas take fixed lenses)

**(a) Mechanism.** Division of labour is planned at launch, not emergent.

- **luna A** gets the "claims and checks" lens: M1, M2, M3, M9.
- **luna B** gets the "dependencies and directions" lens: M4, M5, M6, M7, M8, M10.
- Both still review the whole candidate first. The lens governs where their *remaining* turns go after the first pass.
- **ember**, the fastest, also reviews normally, and after its first pass (about 30 s) posts one **scout map**: a fact-only inventory of the candidate and repo. It lists regions whose criteria contain universal quantifiers, regions with command criteria, stated constraint ids, files the plan edits, and unnamed files that reference those edited files (from one `grep -rl`).
- The hook delivers the map to both lunas, and each luna works the items that match its lens.

Target theories: T1 (the referrer list) and T2 (each move is guaranteed to be run once per run).

**(b) Communication schedule.**

| Trigger | Who | Sends | Maximum |
|---|---|---|---|
| ember after 8 tool calls or 30 s, whichever is later | ember | 1 `scout_map` | 1 per package, at most 20 items, at most 1,200 bytes |
| Next tool call of each luna after the map exists, and after the first-pass gate of 6 calls | hook | the items matching that luna's lens | 1 injection, at most 800 characters |
| Stop | Stop hook | block once if no lens item was touched | 1 |

Item schema: `{"scope":"Task 1","feature":"quantifier|command|constraint|edited-file|unnamed-referrer","path":"<optional repo path>"}`. Features are an enum, and there are no judgments.

**(c) Transport.** JSON board plus hook. It is a one-to-many broadcast that must arrive mid-run. Cross-session messaging would need ember to call `SendMessage` twice with correct names, which is unverified for gateway models (RES:115-123).

**(d) Time budget.** Baseline S07, B = 116 s.

| Reviewer | Isolated end | Collaboration cost | New end |
|---|---|---|---|
| ember | 41 s | map building and posting about 2 turns plus 1 grep, 10 s | 51 s |
| luna A | ~100 s | lens moves about 4 turns (26 s); about half replace default reading, net +13-26 s | 113-126 s |
| luna B (critical path) | 116 s | net +13-26 s | **129-142 s = +11% to +22%** |

The finish signal is at 139 s, and the hard limit is about 156 s.

**(e) Contamination safeguards.**

- **Shared:** structural facts (which regions contain which textual features, and which files reference which).
- **Withheld:** any judgment and all of ember's findings.
- **Independent first pass:** the 6-call gate, and the lens applies only after the first pass.
- **Blind-spot spread:** possible if ember's map *misses* a feature, because the lunas may over-trust the map. Mitigation: the map is labelled "partial, not exhaustive", and each lens also tells the luna to scan the whole candidate for its features.
- **Lens over-specialisation:** a luna might stop raising out-of-lens defects (luna is the main control I8 finder at 63%, INV-PAT:127). Alarm: per-arm luna hit rate on easy issues (B3, I2, I8) falls more than 25% below the comparison arm. Common J alarm also applies; disjoint lenses should *lower* J.

**(f) Expected gain.**

| Target | Theory | Assumption | Added per run |
|---|---|---|---|
| I4 | T2 | luna A always runs M2 on command criteria; detection 0.3-0.5 per encounter, with Task 12 among several | 0.05-0.15 |
| B6, B8 | T1, T2 | luna A runs M3 on quantifier items; inventory greps are within luna's reach only through the map's referrer paths | 0.02-0.10 |
| I5 | T1, T2 | luna B runs M5; luna rarely searches (4%) | 0.03-0.12 |
| B5, I1 | T2 | luna B runs M7/M6 | 0.02-0.08 |
| B1, B2, I6 | T2 | M1, M9, M8 | 0.00-0.15 |
| Displacement | none | fewer default hits by a lensed luna | -0.00 to -0.10 |
| **Collaboration share /14** | | | **+0.05 to +0.45** |
| Harness share | T3 | as in R1 | +0.2 to +0.5 |
| **Total vs S07 1.83/14** | | | **2.1 to 2.8** |

I7 on control: the map's unnamed-referrer list can name `test_worker_contract.py` if ember's one `grep -rl` covers tests/. Estimate +0.05 to +0.2.

**(g) Effort.** The shared bus (about 240 lines, as in R1), plus a scout-map validator (30 lines), lens brief variants (20 lines) and a policy file (15 lines). Total about 305 lines.

**(h) Failure modes.**

- ember produces a malformed or empty map. The lunas then run their lenses unguided, which still works.
- ember's map is so late that the lunas have finished. ember is fast, but a slow ember run (63 tool calls in one alias run, INV-AC:52) delays it.
- The lens leads to shallow box-ticking of every M1 site, which raises wrong blockers. Grading stays under the existing rubric, and wrong blockers are watched.

---

### 2.5 Redesign R5: Sentinel requests (fast lunas hand their coverage and requests to a running sonnet)

**(a) Mechanism.** It reverses the usual direction: cheap reviewers scout for the strong one.

- Panel: sonnet + 2x luna (named baseline, the sonnet + 2x luna family, CR:424).
- The lunas finish in about 110 s while sonnet runs about 274 s.
- Just before its final answer, each luna sends sonnet **one** cross-session message. It names the regions it covered and makes at most 2 move requests for regions it marked "not checked". Reviewers already state what they covered, as in RR:15, "State what you covered".
- sonnet receives the message between tool calls, at about 45% of its run, and runs at most 2 requested moves.

Target theory: T2, by sending stopping-rule, literal and quantifier moves to the one model that already searches beyond the plan (T1-capable, 35% of runs open unnamed tests, INV-PAT:46).

**(b) Communication schedule.**

| Trigger | Who | Sends | Maximum |
|---|---|---|---|
| luna has written its findings block, before its final reply | each luna | 1 message, a fixed template: `PANEL-REQ v1 covered=<task ids> req=<M#>@<task id>[,<M#>@<task id>]` | 1 per luna, at most 300 characters, at most 2 requests |
| sonnet's next tool call after arrival | Claude Code | delivery (RES:93-96) | at most 2 messages |
| PostToolUse on `SendMessage` | hook | mirror the sent text to the board for audit | 1 per send |

**(c) Transport.** Claude Code cross-session messaging: `--name panel-<run>-<rid>` and `--settings '{"crossSessionInbound":"accept"}'` (RES:110-113). It is chosen because the receiver is a single, named, still-running Claude model, and it needs about 5 lines of launcher change. It is the riskiest transport here.

UNVERIFIED items:

- whether luna calls `SendMessage` correctly through the gateway;
- what happens if sonnet is in a long no-tool generation;
- names must be unique, because `ListAgents` shows every local session (RES:115-123).

**(d) Time budget.** B = 821 s / 3 = 274 s per package (CR:424); the cap is 370 s. Per-turn time: sonnet 228 s / 16 = 14 s.

| Reviewer | Isolated end | Collaboration cost | New end |
|---|---|---|---|
| luna A and B | ~110 s | 1 send turn, 6.4 s | ~116 s (idle) |
| sonnet (critical path) | 274 s | 2 requested moves x 2 turns x 14 s = 56 s | **330 s = +20%** |

The finish signal is at 1.20 x 274 = 329 s.

**(e) Contamination safeguards.**

- **Shared:** covered task ids and move requests.
- **Withheld:** luna's findings and verdict.
- **Independent first pass:** sonnet's first pass is about 45% complete before any message can arrive; the lunas receive nothing.
- **Blind-spot spread:** luna's "covered" list could make sonnet skip those regions. Mitigation: the brief tells sonnet that covered regions by a peer are not cleared, and requests only *add* moves.
- **Free-text leak:** the template is enforced by the helper text in the brief, but a model can still type free text into `SendMessage`. The board mirror lets the audit reject any run whose message is not template-shaped (REQ-A3), and those runs are scored separately. Common J alarm also applies.

**(f) Expected gain.**

| Target | Theory | Assumption | Added per run |
|---|---|---|---|
| I4 | T2 | sonnet already finds it in 2/6 family runs; a request for M2 on a command region raises that | 0.05-0.15 |
| B5, I1 | T2 | sonnet's existing 1/6 and plan-vs-source style; M7/M6 requests | 0.03-0.10 |
| I5 | T1, T2 | sonnet's repo greps excluded root files (INV-DS:127); an M5 request names "the repo", root included | 0.02-0.10 |
| B1, B2, B6, B8 | T2 | M1/M3 requests reach sonnet | 0.00-0.05 |
| **Collaboration share /14** | | | **+0.10 to +0.40** |
| Harness share for sonnet panels | T3 | sonnet already reads source.md (99%) and has no merge drops; H3 helps | +0.1 to +0.3 |
| **Total vs family 2.33/14** | | | **2.5 to 3.0** |

Control: H4 removes leak-assisted I7 credits (2 of 9 were in sonnet panels), so control may *fall* by up to 0.33.

**(g) Effort.**

| Change | Rough lines |
|---|---|
| RR flags | 5 |
| brief template text | 10 |
| SendMessage mirror hook | 15 |
| audit check | 30 |

Total about 60 lines plus a mandatory spike.

**(h) Failure modes.**

- luna never sends. Then the panel equals the isolated panel.
- The message arrives after sonnet has finished. The idle session may start a new turn and change the JSON result, which is unverified (RES:117-120).
- Held messages expire after 5 minutes.
- Session names collide with other local sessions.
- There is no durable record without the mirror hook.
- It only works on one machine.

---

## 3. Comparison of the five redesigns

The collaboration gain is on found /14 per run and excludes the harness share. The harness share (+0.2 to +0.5 for cheap panels, +0.1 to +0.3 for sonnet panels) is common to every design and is measured by arm A1 in section 4.

| Design | Base panel | Elapsed overhead (expected, hard cap) | Output tokens overhead | Collaboration gain /14 (low-high) | Control I7 gain | Contamination risk | Effort | Reliability |
|---|---|---|---|---|---|---|---|---|
| R1 Coverage board | ember + 2x luna (116 s) | +22%, finish signal at +20% | +21% to +28% | +0.10 to +0.43 | about 0 | Low (moves only); risk of a false "covered" | ~360 lines (240 shared) | Medium: depends on the models posting cards; hook environment unverified |
| R2 Evidence trail | haiku + 2x luna (238 s) | +18%, finish signal at +20% | +16% to +19% | +0.00 to +0.15 | **+0.15 to +0.35** | Very low (paths only, automatic) | ~300 lines (200 shared) | Medium-high: no model compliance needed; hook environment unverified |
| R3 Cross-examination | ember + 2x luna (116 s) | +29%, **hard at +35% per run** | +28% to +38% | **+0.15 to +0.6** | about 0 | Low (regions plus moves; frozen phase 1) | ~310 lines, no hooks | High: harness-mediated; `--resume` with gateway ids unverified |
| R4 Scout and split | ember + 2x luna (116 s) | +11% to +22%, finish signal at +20% | +19% to +28% | +0.05 to +0.45 | +0.05 to +0.2 | Medium (lunas may over-trust the map; lens tunnelling) | ~305 lines (240 shared) | Medium: depends on one ember map |
| R5 Sentinel requests | sonnet + 2x luna (274 s) | +20%, finish signal at +20% | +18% to +23% | +0.10 to +0.40 | 0 to -0.33 (leak removed) | Medium (free text possible in SendMessage) | ~60 lines | Low: end-of-turn and gateway tool use unverified |

Reading: R3 has the best ratio of expected gain to risk and the only per-run hard time guarantee. R2 is the only design aimed at I7, a missing-task issue that cheap panels have never found (0 of 6 S07 runs, CR:426). The two target different theories (T2 and T1), share no transport parts, and can be tested as separate arms. R1 and R4 depend on models posting, which is where weaker models already fail at instructions (the anchor limit was stated and still broken, HO2:195). R5 is cheapest to build but rests on two unverified behaviours.

---

## 4. Recommended first experiment

**Question.** On the three existing packages, does R3 or R2 find more than an isolated panel that gets the same harness fixes *and* the same move catalogue in its brief?

The catalogue arm is the control that separates "the exchange helps" from "the move list helps". Without it, any gain could be prompt content.

**Base panel for every arm:** ember + 2x luna. It is the replicated default (S07, n = 6, 1.83/14, CR:428), the cheapest to run, and the panel where cheap-model collaboration matters most. For R2 in this panel, ember is the searcher, which works because arm A2's brief already contains M4.

| Arm | Content | Runs (x 3 packages) | Purpose |
|---|---|---|---|
| A1 | Isolated, H1-H4 | 6 | Harness share, read descriptively against historical S07 |
| A2 | A1 plus the catalogue M1-M10 in the brief, isolated | 6 | Effect of the static move list |
| A3 | A2 plus R3 cross-examination | 6 | Collaboration share through T2 |
| A4 | A2 plus R2 evidence trail | 6 | Collaboration share through T1 |

**Scale.** 24 panel-runs, 216 reviewer runs and 72 blind judge calls. The estimate is about 1.6-1.9 million reviewer output tokens (64k per panel-run, x 1.0-1.4).

**Run conditions.**

- Interleave arms in a randomised order to spread gateway drift.
- Use `NOFALLBACK=1`, the existing model-identity check (RR:51-56) and the per-model concurrency caps (HO2:236).
- Run a one-package end-to-end smoke test per arm first: reviewer, combine, merge, anonymise, judge (HO2:259).

**Scoring.**

- JO runs unchanged: a blind Opus judge on `merged-anon.md` against ground truth.
- The anonymiser must also strip the `phase` and `move` keys and rename X-ids, so the judge cannot tell arms apart.
- Run the per-batch API-error audit as in the study (HO2:229, H7).
- Report AS-SCORED and an audit-clean view as before.

**Pre-registered metrics.**

- **Primary:** found /14 per run.
- **Secondary:**
  - target reach: runs with at least one credit on B1, B2, B5, B6, B8, I1, I4, I5, I6;
  - control I7 credit;
  - real blocking /8;
  - wrong blockers;
  - elapsed per package, measured against A1;
  - output tokens;
  - convergence alarm;
  - message and card audit.

**Decision rule** (fixed before the first run). The pre-checks must pass before an arm is judged at all.

| Arm | Adopted as the next panel design when |
|---|---|
| A3 or A4 (against A2) | (mean found /14 is at least 0.5 higher, one-sided permutation p at most 0.10) **OR** (target-reach runs are higher with Fisher one-sided p at most 0.10, for example 3 of 6 against 0 of 6) **OR**, for A4 only, (control I7 credits higher with Fisher one-sided p at most 0.10) |
| Same arm, guard conditions | median elapsed per package at most 1.35 x A1's median; wrong blockers no more than 1.0 above A2; convergence alarm off; 100% of cards and board lines schema-valid and deny-list clean |
| A2 against A1 | If A2 already matches A3 within 0.25, ship the static catalogue (zero transport code) and drop R3 |
| A1 against historical S07 | Descriptive only (different dates and CLI versions), reported as "harness share" with that caveat |
| Stop early | If A1 alone averages at least 3.0/14, rerun the gain estimates before building R1, R4 or R5 |

**Limits.**

- **Power:** with 6 runs per arm and found /14 spread of about 0.6 (S07 range 1-2), only effects of about 1.0 found per run are reliably detectable. The reach and I7 counts are more sensitive because their cheap baselines are near 0.
- **Overfitting:** the catalogue was abstracted from these same three packages. A gain here must be confirmed on a package the moves were not derived from before it is treated as general.

---

## 5. Requirements for the chosen designs

The chosen designs are R3 (primary) and R2 (second arm), plus the shared harness fixes and catalogue that both depend on.

### 5.1 Preconditions (spikes; each must pass before arms A3 or A4 run)

| Id | Requirement | Test |
|---|---|---|
| REQ-S1 | `claude -p --resume <session_id>` continues a phase-1 session for `muse-ember-1.0` and `gpt-6-luna`, and the resumed turn's main-thread `message.model` equals the requested id | One resume per model; observed model checked with the RR:51 jq expression |
| REQ-S2 | Hook commands started by a `claude -p` session see `PANEL_BOARD`, `PANEL_ID`, `PANEL_FINISH_AT` and `PANEL_T0` | Hook writes its environment to a file in a 1-tool session; all four present |
| REQ-S3 | PostToolUse `additionalContext` injected into a gateway-model session appears in the transcript and influences the next tool call | Inject "run `ls /tmp/panel-probe`"; the next tool call runs it, for each of ember and luna |

### 5.2 Harness fixes (all arms)

| Id | Requirement | Test |
|---|---|---|
| REQ-H1 | The reviewer brief names the absolute path of the package's `source.md` and instructs reading it before reviewing | grep of the brief for the path; transcript audit shows a Read or cat of source.md in at least 95% of runs |
| REQ-H2 | Before merge, every findings line has `anchor` and `anchor2` truncated to at most 200 and `claim` to at most 300 characters; the original block is kept beside the report | Merge stdout shows 0 dropped lines for anchor or claim length across all runs |
| REQ-H3 | After truncation the block is validated with the merge parser; if any line is still dropped, the reviewer is re-asked once through `--resume` and the result recorded | meta.json has `parse_dropped` and `reasked` fields; the count of runs with dropped lines after re-ask is reported |
| REQ-H4 | Each package is reviewed in its own sandbox at the plan's base commit (the parent of the first implement commit), and the commit is recorded in the manifest | The sandbox's recorded commit equals the manifest entry for each package |
| REQ-H5 | No sandbox contains `.dev/reflect/` | `find <sandbox> -path '*/.dev/reflect*'` prints nothing |
| REQ-H6 | Sandboxes still exclude `.dev/tasks/done`, `.dev/eval-workspaces` and `.dev/research` (manifest.md:10), and the board directory is outside every sandbox | find checks; board path prefix is `/tmp/panel-board/` |

### 5.3 Move catalogue (arms A2, A3, A4)

| Id | Requirement | Test |
|---|---|---|
| REQ-C1 | `moves.json` holds M1-M10 exactly as in section 2.0, is hashed in the manifest before the first run, and is identical in A2, A3 and A4 | sha256 matches the manifest in every run's brief |
| REQ-C2 | The catalogue, brief additions and card templates contain no file path, backticked identifier or task title taken from any of the three candidates | Deny-list built from the candidates' backticked tokens and paths; grep finds 0 hits |
| REQ-C3 | Reviewers never receive ground truth, judge output or other reviewers' report text | Transcript audit: 0 Reads of `ground-truth.json`, `score.json` or `reviews/` paths |

### 5.4 Cross-examination R3 (arm A3)

| Id | Requirement | Test |
|---|---|---|
| REQ-X1 | Phase 1 runs with the A2 brief and no peer input; its report and findings block are stored byte for byte before phase 2 starts | sha256 of the phase-1 report recorded before phase-2 launch; unchanged after |
| REQ-X2 | A reviewer's phase 2 starts only after its own phase 1 has ended and at least one peer's phase 1 has ended | Timestamps in meta.json |
| REQ-X3 | `digest.py` emits at most 3 cards per reviewer, each in schema `panel-card/1` with fields `card`, `to`, `scope` (candidate task or section ids), `move` (M1-M10) and `origin` (`peer-anchor` or `gap`), and no other fields | JSON-schema validation of every card file |
| REQ-X4 | Peer-anchor cards name regions a peer anchored and the receiver did not; at least one card per reviewer is a gap card when any unanchored region exists | Audit recomputes regions from the blocks |
| REQ-X5 | The move on a card is chosen by the fixed rules (peer category complement; candidate text features), never by a model | Unit test of `digest.py` on fixed blocks gives the expected cards |
| REQ-X6 | Every phase 2 is killed at `1.35 x T1 - 2 s` after panel launch, where T1 is the moment the last phase 1 ended; on kill the phase-1 report stands | Elapsed per package at most 1.35 x T1 in 100% of runs |
| REQ-X7 | Phase-2 findings use ids X1-X5 and may only add; `combine-blocks.sh` produces exactly one findings-v1 block containing all phase-1 lines unchanged plus the X lines, each X line carrying `"phase":2` | Parser finds 1 block; phase-1 lines byte-identical; X lines at most 5 |
| REQ-X8 | Echo-rate alarm: fewer than 50% of phase-2 findings cluster in the merge with a peer's phase-1 finding | Computed from the ledger members |

### 5.5 Evidence trail R2 (arm A4)

| Id | Requirement | Test |
|---|---|---|
| REQ-B1 | A PostToolUse hook on every reviewer appends one `panel-msg/1` line of `kind:"evidence"` per tool call to `$PANEL_BOARD/<rid>.jsonl`: paths seen (at most 16, existing in the sandbox) and paths opened; no other text | Board lines validate; every path exists in the sandbox |
| REQ-B2 | Each reviewer writes only its own board file; lines are appended with a single write of at most 1,200 bytes | Audit: sender field equals the file name; 0 lines over the limit |
| REQ-B3 | Delivery starts only after the receiver's 5th tool call; at most 3 injections per reviewer per package, each at most 8 paths and at most 600 characters, containing only paths seen by a peer, opened by no reviewer, and not named in the candidate | Transcript audit of the injected system reminders |
| REQ-B4 | Injected paths are split across receivers by a hash of the path, so no path is injected into more than one reviewer | Audit over the injection log |
| REQ-B5 | After `PANEL_FINISH_AT` (T0 + 1.20 x B) the hook injects only the finish notice, and the Stop hook never blocks; the Stop hook blocks at most once per reviewer | Hook logs; elapsed per package at most 1.35 x A1 median |
| REQ-B6 | Tunnelling alarm: no more than 40% of a reviewer's post-gate opens are injected paths | Computed from board lines |
| REQ-B7 | If the board directory is missing or a line fails validation, the hook prints nothing and exits 0 (the review continues isolated) | Fault-injection test: corrupt line, missing directory |

### 5.6 Merge, judge and audit (all arms)

| Id | Requirement | Test |
|---|---|---|
| REQ-M1 | The merge contract stays findings-v1 through `superclaude review merge`; the only additions are optional keys (`phase`, `move`), which the parser accepts as unknown keys (HO2:346) | Merge rc 0; ledger rows include phase-2 findings |
| REQ-M2 | The judge input `merged-anon.md` contains no `phase` or `move` key, no X-prefixed id and no arm name | grep of every `merged-anon.md` |
| REQ-M3 | JO runs unchanged (same prompt text, same model `claude-opus-5-5`) | sha256 of the judge brief template equals the study's |
| REQ-A1 | `board-audit.py` reports per run: schema validity, deny-list hits, injection counts, convergence J against the isolated reference, distinct tasks anchored, echo rate, and elapsed against the caps | One output file per row-package; aggregated in the result table |
| REQ-A2 | The convergence alarm (section 2.0) is computed per arm, and an arm with the alarm on cannot be adopted | Decision table includes the alarm column |
| REQ-A3 | A run with any schema-invalid card or board line, or any deny-list hit, is flagged EXCLUDE and reported in the audit-clean view | flags.tsv entries |
| REQ-A4 | meta.json records phase-1 and phase-2 wall time, tokens per phase, resume session id and cards received, and keeps `expected_model` unchanged on any retry (closes HO2:207 H2 for these arms) | Field presence check on every meta.json |

### 5.7 Experiment (section 4)

| Id | Requirement | Test |
|---|---|---|
| REQ-E1 | Arms A1-A4 each run 6 times on the three packages with ember + 2x luna, interleaved in a recorded random order | Run log order matches the pre-registered order file |
| REQ-E2 | The metrics and decision rule in section 4 are written to a pre-registration file and hashed before the first run | Hash recorded in the manifest before the first run's timestamp |
| REQ-E3 | A one-package end-to-end smoke test per arm (reviewer, combine, merge, anonymise, judge) passes before the arm's batch | Smoke-test log per arm |
| REQ-E4 | The result report gives A1 against historical S07 (labelled descriptive), A2 against A1, A3 against A2, and A4 against A2, each with run-level values, permutation or Fisher p-values, elapsed ratio, token ratio and the audit flags | Report sections present; numbers recomputed by a second script with 0 mismatches |

What I skipped or did not check: I did not run any of the three spikes (resume, hook environment, hook injection into gateway models), did not verify a `--max-turns` option (the time caps above use `timeout` instead), and did not determine each package's base commit. The gain ranges are estimates built from near-miss counts and stated conversion assumptions, not measurements.
