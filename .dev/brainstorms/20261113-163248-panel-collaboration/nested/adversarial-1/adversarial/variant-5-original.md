# Requirements specification: tasklist review panel collaboration (variant 5, performance lens)

Lens: bottlenecks, scaling behaviour and cost-to-serve. Nothing was run for this variant; every number comes from the study files or is marked as an assumption.

**Evidence paths**

| Short name | Path |
|---|---|
| EVAL | `.dev/eval-workspaces/tasklist-review-panel/20261111-a1` |
| CR | `EVAL/COMBO-REPORT.md` |
| HO2 | `.dev/eval-workspaces/tasklist-review-panel/HANDOFF-review-panel-unification-run2.md` |
| BR | `.dev/brainstorms/20261113-163248-panel-collaboration` |
| INV-DS | `BR/enrichment/investigation-designspec.md` |
| INV-AC | `BR/enrichment/investigation-alias-control.md` |
| INV-PAT | `BR/enrichment/investigation-patterns.md` |
| RES | `BR/enrichment/research-light.md` |
| Launcher | `EVAL/tools/run-reviewer.sh` |

**Issue labels** follow CR:401-417. DS = designSpec package (B1-B5, I1-I5), AL = alias package (B6-B8, I6), DE = control package (I7, I8).

**The "hard ten"** are the issues no ember, luna or haiku panel found: B1, B2, B5, B6, B8, I1, I4, I5, I6, I7. Nine are in the 14 defect-rich issues. I7 is in the control package, so it is reported separately. "Per run" means one panel on all three packages.

**Isolated baseline panels** (per-package figures are the three-package figures in CR divided by 3, so confirm them against the per-run `wall_s` in the meta files):

| Name | Panel | Tokens per run (3 packages) | Elapsed per run (3 packages) | Per package | +35% cap per package |
|---|---|---|---|---|---|
| EL2 | ember + 2x luna (CR:331) | 63,644 | 348 s | 116 s | +40.6 s |
| HL2 | haiku + 2x luna (CR:319) | 191,018 | 715 s | 238 s | +83 s |
| SL2 | sonnet + 2x luna (CR:424) | 139,113 | 821 s | 274 s | +96 s |

---

## 1. Theories

I accept all three seed theories and sharpen each with the cost of the missing move. T2 is split in two, because the two halves need different cures.

| Theory | Verdict on the seed | Evidence (numbers) | What it explains |
|---|---|---|---|
| **T1. Search stops at the edge of the plan, though the missing sweeps are cheap** | Accept, refine | Files touched that the plan does not name, per run: sonnet 3.1, grok 1.2, haiku 0.9, ember 0.8, luna 0.3 (INV-PAT §1). Runs touching an unnamed test file: sonnet 35%, grok 33%, ember 8%, luna 1%, haiku 0%. `tests/skills/test_worker_contract.py`: 7 of the 8 DE runs that opened it reported I7, 0 of 225 others did, and 5 of 11 haiku control runs had it in grep output and never opened it (INV-AC §2). `CHANGELOG.md` was touched in 1 of 233 DS runs and I5 was never found (INV-PAT §4). 44 of 98 cheap alias reviewers saw the narrowed `tiers.md:42` and never compared it with Task 7 (INV-AC §2). | I7, B8, I5, part of B6, part of I6 |
| **T2. Right place, wrong question (T2a), and places nobody visits (T2b)** | Accept, split | **T2a, anchor right, one question asked.** 16 cheap findings sat on the I5 sentence and all asked "does the grep match too much" (INV-DS §2c). 3 findings analysed the B5 mapping but only for mode-off. 1 finding sat on the I1 row. **T2b, never reached.** Zero findings anchor DS Task 1 O3 or AC3 in any cheap row. I4 drew 0 findings on its AC, and only sonnet found it (4 of 26 runs). Attention is also duplicated: luna anchors DE Task 12 in 91% of runs and 34% of its DE findings are one artifact-path objection (INV-PAT §3). Thinking budget alone is not the fix: tokens track finds across models (Spearman 0.64), but within ember and luna the hard-issue rate is flat (ember 0.25 to 0.22, luna 0.09 to 0.09). | T2a: B5, I1, I5. T2b: B1, B2, I4, I6, part of B6 |
| **T3. The test setup hides defects, drops findings and ranks the survivors low** | Accept, quantify | The reviewer checkout is taken after the plans were implemented and repaired: B5 repaired at `refs/merge-guard.md:146`, I1 at `merge_guard.py:256`, I4 at `pr-submit.md:81`, B8 narrowed at `tiers.md:42`. `source.md` is not named in the brief: 156 of 665 runs never opened it (ember 81 of 209 = 39%, luna 49 of 222 = 22%, CR:373). The merge dropped 49 blocking findings (80 reviewer-level cases: ember 33, luna 30, HO2 D1). Grading puts unstated requirements at Medium and has no missing-task category: all 7 true I7 findings were non-blocking, luna marks 72% of findings blocking, and grok saw `CHANGELOG.md:166` and dropped it as minor (INV-DS §3). The sandbox still holds `.dev/reflect/pre-design-20261108041729/REPORT.md`, which names I7: 2 of 9 I7 credits read it, so 7 are clean. | B5, I1, I4, B8 (false reassurance), I5 (minor rule), I7 (category, leak), plus a measurement floor on every number |

**Which theory explains which miss**

| Issue | Primary | Also |
|---|---|---|
| B1, B2 | T2b | T3 (the grading sentence steers to wrong builds; 14 of 39 ember DS reports never opened `source.md`) |
| B5, I1 | T2a | T3 (code repaired, source unread) |
| I4 | T2b | T3 (the repaired heading makes a real grep pass) |
| I5 | T1 | T2a (16 anchors, wrong direction), T3 (minor rule) |
| B6 | T1 (claim vs test scope) | T2 (luna read `chains.md`, wrong angle) |
| B8 | T1 (inventory) | T3 |
| I6 | T2b (sweep a constraint across tasks; untested) | none |
| I7 | T1 | T3 |

**Performance reading of the theories.**
1. The missing moves cost little. One to four tool calls is about 3-13 s for ember and 6-26 s for luna, which is at most 22% of a median run. The omission is about priority, not budget.
2. A plan-level fact, such as "which files reference the files this plan edits", is the same for every reviewer. Computing it once and sharing it costs O(1) in the number of reviewers; each reviewer redoing it costs O(n).
3. Part of the gain does not need communication at all: harness fixes, and telling each reviewer which generic moves to apply. Section 3 therefore measures every design against a no-communication control.

---

## 2. Five redesigns

### 2.0 Shared substrate

#### 2.0.1 Timing facts used in every arithmetic block

| Quantity | Value | Source or assumption |
|---|---|---|
| Median wall time and turns | ember 41 s / 13, luna 102 s / 16, haiku 233 s / 10, sonnet 228 s / 16 | INV-PAT §1 |
| Seconds per turn | ember 3.2, luna 6.4, haiku 23, sonnet 14 | derived from the row above |
| Idle time of a fast reviewer while the slowest runs | ember about 75 s in EL2; luna about 120-160 s in HL2 and SL2 | derived |
| Extra output tokens per tool-only turn | ember 0.3k, luna 0.15k | ASSUMPTION; needs a spike |
| Hook cost per tool call | 0.1 s | ASSUMPTION; needs a spike |

Panel elapsed time is the slowest reviewer's path. Time a faster reviewer spends inside the slowest reviewer's window is free.

#### 2.0.2 Generic move catalog (shown to reviewers; applies to any plan)

Messages only ever carry a move code, a plan reference, a count, a command string or a repository fact. They never carry a verdict or a defect description. The catalog text must name no file, task or defect from the three packages (requirement C-6).

| Code | Move in plain words | Analysis only (never shown): issues it can trigger | c, central |
|---|---|---|---|
| G1 | For each criterion that says every, all, complete or no remaining, state the finite check or list that proves it. | B1 | 0.050 |
| G2 | Compare a task's instruction, its criteria and the source's matching section for the same scope. | B2 | 0.050 |
| G3 | For each mapping or rule the plan defines, list every input, branch and halt path and state the output for each. | B5 | 0.125 |
| G4 | For every value a rule reads, name the step that writes it, using the source, not the checkout. | I1 | 0.075 |
| G5 | Run each command or grep criterion against the exact text the task orders written. | I4 | 0.200 |
| G6 | For each all/only/every/no-other sentence the plan dictates, list what it covers and count the exceptions. | B8, B6 | 0.185 |
| G7 | For each file the plan edits, search the whole repo (tests, docs, root files) for references, open files the plan never names, and check the plan's gate runs them. | I7, I5 | 0.215 |
| G8 | Where you checked a claim one way, check the other (where else is it stated). Where you found a constraint breach in one task, run the same check on the sibling tasks. | I6, I5 | 0.140 |

**What c means.** It is the chance that a cheap model which carries out the move on the right region writes a finding the blind judge credits. I set it at about half of a sonnet-level chance, because sonnet finds 1.44 judged items per run against 0.65 for ember and 0.30 for luna (`EVAL/analysis/attrib.out`, via INV-PAT §4). The sum of c over the catalog is 1.04. That equals roughly the measured hard-issue reach of sonnet + 2x luna (about 1.0 per run: I7 in 3 runs, I4 in 2, B5 in 1 over 6 runs, CR:440). It is therefore a ceiling, not a forecast.

#### 2.0.3 Transport options (decision once, reused below)

| Option | Verdict | Reason |
|---|---|---|
| JSON board with a PostToolUse hook (inject) and a Stop hook (last check) | **Chosen for mid-run and end-of-run** | CLI-side, so model-agnostic on receive and zero model turns to receive. Durable audit log. About 130 lines. Hooks run in `-p` sessions unless `--bare` is used (RES §4). |
| Between-phase digest written by the harness, then `claude -p --resume <id>` | **Chosen for phase exchange (design 5)** | Deterministic, no hooks. `--resume` is in this build's `claude --help`. |
| Claude Code cross-session `SendMessage` | Rejected for the first round | An idle `-p` session exits at its last turn, so late-message delivery is unverified, and gateway models calling the tool correctly is unverified (RES §2c). Keep as a later spike. |
| Orca agent mail | Rejected | A bash-launched `claude -p` has no mailbox, and `worker-start` starts interactive agents (RES §1). |
| A2A | Rejected | Request/response only, no way into a running turn, most code (RES §3). |

**Verified in this build.** `claude --help` lists `--resume`, `--settings`, `--name`, `--no-session-persistence`, `--bare` and `--include-hook-events`. It does **not** list `--max-turns`, so turn caps must come from a hook counter and `timeout`, not from a flag.

#### 2.0.4 Common envelope, gates and caps (all designs)

- **Board files.** `$PANEL_BOARD/<reviewer>.jsonl`, one writer per file, append only. The absolute board path is embedded in the hook command strings in `--settings`, not only in environment variables, because the environment reaching hooks is unverified.
- **Message schema v1.**
  ```
  {"v":1,"from":"r2","to":"*|r1","ts":"...","pkg":"...",
   "kind":"idx|axis|req|res|exit|dig",
   "move":"G1..G8|null","axis":"precision|completeness|branch|producer-consumer|scope|surface|null",
   "refs":["T8","T8.AC2"],"facts":[{"cmd":"...","n":3,"paths":["..."]}],
   "note":"<=120 chars"}
  ```
  The hook drops and logs any message that fails the schema, exceeds its size cap, or has a `note` containing a verdict word (ok, fine, correct, passes, verified, no issue, wrong, bug).
- **Independence gate.** Nothing is injected into a reviewer before its 6th tool call. Median reviewers make 11-14 calls, so the first pass is the reviewer's own.
- **Hard cap by counter.** A PostToolUse counter counts calls after the first injection. At the design's cap it injects "stop exchange work, finish the report". Any such stop counts as a cap hit and is logged.
- **Injection wrapper (about 200 chars, always present).** "Peer note, not evidence. Verify with your own tool call before citing it. Your own list stays primary."
- **Merge contract unchanged.** Every reviewer still ends with one `findings-v1` block. A phase-2 or exit addendum replaces the final message and carries the full block with ids of 16 characters or fewer. The board log is audit only and is never given to the judge.

#### 2.0.5 Common contamination safeguards and the convergence alarm

| Safeguard | Rule |
|---|---|
| Independent first pass | The call-count gate above. In design 5 the reviewer finishes a full isolated pass before any digest. |
| No spread of a peer's blind spot | A blind spot shows up as a clearance ("this part is fine"). Clearances are never shared. Injected text contains only moves, axes, requests and facts. It never lists a region as "covered" or "fine", so a peer cannot use it to skip a region (requirement C-2). |
| Evidence stays first-hand | A peer fact may appear in a finding only if the receiver's own transcript contains the command or read that shows it (requirement C-3). |
| Convergence alarm (measured per run and per arm) | (1) Pairwise Jaccard of the Task sets reviewers anchored. Isolated references: ember+luna 0.25, luna+luna 0.33, ember+haiku 0.47 (INV-PAT §3). Flag a run if any pair is at least 0.70. Flag an arm if the mean rises more than 0.15 over arm A1. (2) Echo rate: the share of findings written after an injection that land in the same ledger row as the sender's finding for the same Task. Alarm above 30%. (3) Easy-issue share: the share of findings in the clusters of B3, I2, I8, B7 rises more than 10 points over A1. Three flagged runs out of six switch the arm off. |

#### 2.0.6 Gain model and the harness share

**Model.** Added hard issues per run (3 packages) is the sum over catalog moves of P(move executed on the right place) times c. Five assumptions, to be replaced by measurement:
1. The act rate a, the chance a reviewer follows an injected move within its cap, is 0.7 (0.5-0.85). Luna calls the Skill in 84% of runs (INV-PAT §1), so it follows instructions.
2. Executing within a shorter turn cap lowers quality: q = 0.6 for 3 turns or fewer, 0.8 for 4-8 turns.
3. The central estimate is the sum above; low is 0.25 times central and high is 2 times central.
4. The split between the 14-issue scale and the control (I7) uses G7's I7 share (0.175 of 0.215).
5. The "prompting share" in section 3 is my judgment: the part of a gain a static list of moves in the brief would also capture. Section 4 replaces it with a measurement.

**Harness share (applies equally to every design, measured as arm A1 against the historical EL2 runs):**

| Fix | Mechanism and assumption | Added /14 | Low-high |
|---|---|---|---|
| Pre-implementation checkout (T3) | Removes false reassurance on B5, I1, I4, B8 and the "feature already exists" distraction findings (haiku/luna F1/F3 in INV-DS §3). Assume +0.02 each on 4 issues. | +0.08 | 0.02-0.16 |
| `source.md` named in the brief | The 39% ember and 22% luna non-readers become readers; B5, I1 and B2 need the source. | +0.03 | 0.01-0.08 |
| Anchor and claim normalizer | 92 findings dropped over 264 merges, 49 of them blocking (HO2 D1), so about 0.19 blocking and 0.35 total per merge. Assume 2% match a not-yet-found hard issue. | +0.03 | 0.00-0.10 |
| Remove `.dev/reflect` | Leak removal does nothing for cheap panels (I7 is 0 in 30 runs). It would lower sonnet panels' I7 by about 2 of 9. | 0 | 0 |
| **Total** | | **+0.14** | **0.03-0.34** |

The control scale (I7) gets no harness gain for cheap panels. Its value is measurement validity.

---

### 2.1 Design 1: Claim-Index Relay

**(a) Mechanism and roles (baseline EL2).**
- **ember is the indexer.** After its 5th tool call (it has read `candidate.md` and `source.md`) it posts one index. The index has up to 12 entries, each a plan reference, a kind and a quote of at most 60 characters of plan text. Kinds are: universal sentence, command criterion, edit set, cross-task constraint, rule table. Nothing is judged.
- **luna x2 are consumers.** After their 6th call they receive the index with the wrapper. The wrapper pairs kinds with catalog moves: universal -> G1 and G6; command -> G5; edit set -> G7; constraint -> G8; rule table -> G3 and G4. They apply at least one move to an entry they have not examined. Their own list stays primary.
- ember keeps reviewing normally. sonnet, haiku and grok are not used.

**(b) Communication schedule**

| Item | Value |
|---|---|
| Trigger out | ember's 5th tool call, once |
| Trigger in | each luna's first tool call after call 6 |
| Messages per reviewer per package | ember 1 out, 0 in; each luna 0 out, 1 in |
| Size cap | post 1,200 chars (12 entries x 80 plus wrapper); injection = post + 200-char wrapper |
| Schema | `kind:"idx"`, `facts` empty, `refs` = Task refs, items `{t,k,q}` |
| Scaling with n reviewers | 1 sender and n-1 receivers: O(n) deliveries |

**(c) Transport.** Board with PostToolUse injection. The receive side costs no model turn and works for gateway models. ember's single post uses the Bash helper (one turn). A hook-built index would be cheaper, but regex cannot find "all/only" sentences reliably; ember's reading can.

**(d) Time budget (EL2, 116 s per package, cap +40.6 s)**

| Reviewer | Arithmetic | Result |
|---|---|---|
| ember (not critical) | 41 s + 1 post turn (3.2 s) + about 2 s to write the index | about 46 s, inside its 75 s idle window |
| luna (critical) | 4 extra turns x 6.4 s = 25.6 s, plus 14 hook calls x 0.1 s = 1.4 s | +27.0 s |
| Panel | 116 + 27.0 = 143 s | **+23.3%** |
| Tokens (per package) | ember 0.3k + 1.5k index = 1.8k; luna 2 x 4 x 0.15k = 1.2k | +3.0k on 21.2k = **+14%** |

**(e) Safeguards.** Gate: no delivery before call 6. The index lists kinds, not verdicts, so it carries no clearance. Herding risk: both lunas get the same list and may anchor only on it. The wrapper requires one move on an entry the luna did not examine and one region outside the index. Alarm: besides the common alarms, flag the arm if luna findings anchored on index entries exceed A1's rate for the same Tasks by more than 15 points.

**(f) Expected gain.**
- **Theories and issues targeted.** T1 and T2b through the universal, command, edit-set and constraint entries: B1, B5, B6, B8, I4, I5, I6, I7.
- **Move probabilities (P executed per run):** G1 0.20, G2 0.10, G3 0.05, G4 0.10, G5 0.30, G6 0.25, G7 0.25, G8 0.15. Sum 1.40.
- **Gain.** 0.20x0.05 + 0.10x0.05 + 0.05x0.125 + 0.10x0.075 + 0.30x0.20 + 0.25x0.185 + 0.25x0.215 + 0.15x0.14 = **0.21 total**. That is 0.17 on the 14-issue scale and 0.04 on the control (I7).
- **Range.** 14-issue scale 0.04-0.33; control 0.01-0.09.
- **Shares.** Harness share +0.14 (shown separately, not included above). Prompting share about 60% (0.10 of the 0.17). Net collaboration share about 0.07.

**(g) Effort.** Board layer about 130 lines (shared). Design increment about 40 lines: an index prompt for ember (about 20), a wrapper table and gating in the hook (about 20). Files: `panel-post.sh`, `panel-hook-post.sh`, `settings.tmpl.json`, edits to `run-reviewer.sh` (+25 lines) and the brief (+10 lines).

**(h) Failure modes.** ember skips `source.md` (39% of runs), so the index is thin: 1 of 3 outcomes is a bad index. ember posts after luna's call 6 and no one receives it: the harness logs "no delivery" and the run counts as isolated. luna ignores the wrapper (a about 0.3 chance). Both lunas pick the same move, so distinct coverage is lower than the sum above.

---

### 2.2 Design 2: Axis-Flip Relay

**(a) Mechanism and roles (baseline EL2).** This design attacks "right place, wrong question" (T2a). Every reviewer is asked, each time it settles a finding, to post where it looked and which axis it used. The harness answers with the complementary axis for that region.
- **ember, luna, luna** all post and all receive. ember's idle window pays for most flips.
- **Axis to move table (fixed):**

  | Axis the peer used | Move the receiver is asked to apply at the same reference |
  |---|---|
  | precision (does the check match too much) | G8, the other direction: where else is the claim stated |
  | completeness | G5, run the literal check on the exact text |
  | branch (one path traced) | G3, every other input, branch and halt path |
  | producer-consumer (one value) | G4, every other value the rule reads |
  | scope | G1, state the finite check for any every/all in the region |
  | surface (path, hash, line number) | never relayed; this avoids herding on the easy artifact-path finding (21% of ember findings) |

- The receiver states in its report whether the flip holds. It never receives the peer's claim, severity or blocking flag.

**(b) Communication schedule**

| Item | Value |
|---|---|
| Trigger out | each time the reviewer settles a finding, before moving on; the brief asks for `panel-post axis <ref> <axis>` |
| Trigger in | next tool call after a post from a different reviewer, after call 6 |
| Messages per reviewer per package | ember at most 3 out; luna at most 2 out; at most 2 injections in per reviewer |
| Size cap | post 160 chars; injection 160 chars + 200 wrapper |
| Schema | `kind:"axis"`, `axis`, `refs` (at most 2) |
| Scaling | ring: each post is injected into at most 1-2 peers; O(n) |
| Dedupe | a reference anchored by 2 or more reviewers is relayed once only |

**(c) Transport.** Board with PostToolUse injection, same reasons as design 1. Posts cost one Bash turn each. A hook cannot know which axis a model used, so the post must be model-authored.

**(d) Time budget (EL2)**

| Reviewer | Arithmetic | Result |
|---|---|---|
| ember (not critical) | 3 posts x 3.2 s + 5 flips x 3.2 s = 25.6 s; ends about 67 s, below luna's 102-116 s | no effect |
| luna (critical) | 2 posts x 6.4 s = 12.8 s; 3 flips x 6.4 s = 19.2 s; hooks 1.4 s | +33.4 s |
| Panel | 116 + 33.4 = 149.4 s | **+28.8%** (7 s below the cap) |
| Tokens (per package) | ember 0.9k posts + 1.5k flips; luna 2 x 5 turns x 0.15k = 1.5k | +3.9k on 21.2k = **+18%** |

**(e) Safeguards.** Messages carry an axis and a reference only. A peer's conclusion and its blind spot cannot travel. The receiver must flip to a different axis on the same region, never repeat the peer's axis, and must verify with its own tool call. Anchors that are not about the easy surface axis are the only ones relayed. Alarm: the echo rate (common alarm 2) is the one that matters most here. The test for the design failing is "findings after injection that merge into the sender's row" above 30%.

**(f) Expected gain.** Gain is computed region by region: P(some reviewer anchored the region) x 0.525 (delivered and acted, 0.75 x 0.7) x 0.5 (the table picks the right move half the time) x c at the anchor (c is higher at an anchor than a generic sweep).

| Issue | P(region anchored by at least 1 of 3) | c at the anchor | Contribution |
|---|---|---|---|
| B5 (DS Task 8) | 0.60 | 0.150 | 0.024 |
| I1 (DS Task 3) | 0.35 (assumed) | 0.125 | 0.012 |
| I5 (DS Task 2) | 0.52 | 0.175 | 0.024 |
| B1 (DS Task 1) | 0.61 | 0.100 | 0.016 |
| B2 (DS Task 1) | 0.61 | 0.075 | 0.012 |
| I4 (DS Task 12) | 0.18 | 0.275 | 0.013 |
| B6 (AL Task 6) | 0.77 | 0.125 | 0.025 |
| B8 (AL Task 7) | 0.24 | 0.175 | 0.011 |
| I6 (AL Task 7) | 0.24 | 0.060 | 0.004 |
| I7 (DE Task 12) | 0.95 | 0.150 | 0.037 |
| **Sum** | | | **0.18** |

(P anchored comes from the per-model anchor shares in INV-PAT §3.) That is 0.14 on the 14-issue scale and 0.04 on the control. Range: 14-issue 0.03-0.28; control 0.01-0.07. Prompting share about 35%, so the net collaboration share is about 0.09. This is the design that supplies information a static list cannot, namely where a peer actually looked.

**(g) Effort.** Shared board layer about 130 lines. Increment about 75 lines: axis table and flip wrapper (about 30), dedupe filter (about 20), post-compliance prompt (about 25).

**(h) Failure modes.** Models forget to post (compliance). Posts carry the wrong axis, so the flip is wrong. Reviewers spend turns on flips and write fewer own findings (watch ledger size). Luna's 6.4 s per turn is an average and a flip that needs two greps could push luna past +35%; the hook counter stops flips at 3.

---

### 2.3 Design 3: Sweep Desk

**(a) Mechanism and roles (baseline EL2).** This design hands the mechanical legwork of the sweeps to the fastest reviewer, which has 75 s of otherwise idle time.
- **luna x2 are requesters.** After call 6 a luna may post up to 2 sweep requests: a move code (G3, G4, G5, G6, G7 or G8) and up to 3 plan references. The hook expands the code into a fixed sweep template.
- **ember is the sweeper.** It finishes its own review normally (about 41 s), then its Stop hook keeps it alive: it polls for requests every 2 s until a deadline of 95 s from run start. It executes at most 3 requests (about 4 turns each), and posts a result card with the command strings and counts.
- Results are injected into the requesting luna's next tool call. Luna never waits for a result.

**(b) Communication schedule**

| Item | Value |
|---|---|
| Trigger out (luna) | after its 6th call; at most 2 requests |
| Trigger out (ember) | one result card per request, at most 3 per package |
| Trigger in (ember) | after each tool call and by polling in its Stop hook until 95 s |
| Trigger in (luna) | next tool call after the result lands; at most 3 injected turns of follow-up |
| Size cap | request 160 chars; result card 500 chars including the command string(s) and up to 5 paths; injection adds a 200-char wrapper |
| Schema | `kind:"req"` with `move`, `refs`; `kind:"res"` with `move`, `refs`, `facts:[{cmd,n,paths}]` |
| Scaling | star: at most 2(n-1) requests and 3 results; ember's load is capped at 3 requests regardless of n |

**(c) Transport.** Board with hooks. Cross-session messaging would be a natural fit for an idle sweeper, but an idle `-p` session exits at its last turn (RES §2c), so the Stop-hook wait loop is used instead.

**(d) Time budget (EL2)**

| Reviewer | Arithmetic | Result |
|---|---|---|
| ember (not critical) | 41 s + 3 requests x (4 turns x 3.2 s + 3.2 s post) = 41 + 48.0 = 89 s, below the 95 s deadline and below luna's 102-116 s | no effect |
| luna (critical) | 2 requests x 6.4 s = 12.8 s; 3 follow-up turns x 6.4 s = 19.2 s; hooks 1.4 s | +33.4 s |
| Panel | 116 + 33.4 = 149.4 s | **+28.8%** |
| Tokens (per package) | luna posts 0.6k, follow-ups 0.9k; ember 15 turns x 0.3k = 4.5k | +6.0k on 21.2k = **+28%** |

Luna must never wait for a result. A 15 s wait would add 15 s and break the cap (48.4 s = +41.7%). The deadline for ember is a hard rule for the same reason.

**(e) Safeguards.** Only facts flow, never verdicts. Every result card carries its command string, so the receiver can re-run it in one turn, and must do so before citing the count (requirement C-3). A wrong sweep by ember (bad grep scope, for example) is the main way a blind spot could spread; the alarm measures how often a receiver's re-run differs from the card: more than 10% is a stop. The requester picks the move and the plan references; ember cannot widen the request.

**(f) Expected gain.** Sweeps are mechanical, so P(executed) is high for G5, G6, G7 and G8.
- **Move probabilities:** G3 0.10, G4 0.10, G5 0.30, G6 0.30, G7 0.30, G8 0.20. G1 and G2 are reasoning-only and cannot be swept (0).
- **Gain.** 0.10x0.125 + 0.10x0.075 + 0.30x0.20 + 0.30x0.185 + 0.30x0.215 + 0.20x0.14 = **0.23 total**: 0.18 on the 14-issue scale and 0.05 on the control.
- **Range.** 14-issue 0.04-0.35; control 0.01-0.10.
- **Targets.** T1 (B6, B8, I5, I7) and T2b (I4, I6). Prompting share about 40%, so net collaboration about 0.11.

**(g) Effort.** Board layer 130 lines (shared). Increment about 120 lines: request template expansion (about 40), ember's Stop-hook wait loop and deadline (about 50), result-card builder and re-run check (about 30).

**(h) Failure modes.** Lunas rarely run searches themselves (4% of runs search `tests/`, INV-PAT §1), so they may not post requests; the hook adds a one-line reminder at call 6, and the compliance rate is the number to measure first. ember's Stop-hook wait is the most complex piece (a hung wait costs the whole panel; guard with `timeout 95`). ember sometimes skips `source.md`, so G4-type sweeps against the source would be wrong. Results can arrive after the requester has finished: counted as lost, not retried.

---

### 2.4 Design 4: Exit Ticket

**(a) Mechanism and roles (baseline EL2).** The cheapest possible exchange: one swap at the very end.
- Each reviewer's final report includes one line: `moves: G1,G5 | regions: T1,T3,T8` (at most 120 chars). The Stop hook posts it with no model turn.
- At its own stop, each reviewer is shown the moves nobody has applied, and is told to apply exactly **one** more, chosen by cost class: ember gets a sweep (G7, G6 or G8); luna gets a reading move (G1, G3, G5, G4 or G2). The hook blocks the stop once, with the one move as the reason, and the reviewer then re-issues its report with any new findings.
- ember waits at most 70 s for peer tickets before its block, so it sees both lunas. Lunas wait 0 s.

**(b) Communication schedule**

| Item | Value |
|---|---|
| Trigger out | the reviewer's final message (the hook parses the `moves:` line; no extra turn) |
| Trigger in | the reviewer's own first Stop; the hook blocks once (the `stop_hook_active` guard prevents a loop) |
| Messages per reviewer per package | 1 ticket out, 1 digest in |
| Size cap | ticket 120 chars; digest 240 chars |
| Schema | `kind:"exit"` with `refs` = region list, `facts:[{"moves":[...]}]`; `kind:"dig"` with `move` |
| Extra turns | at most 3 per reviewer, enforced by the hook counter |
| Scaling | n tickets; each reviewer reads the other n-1 tickets (120 chars each): O(n²) characters but 480 chars at n = 5 |

**(c) Transport.** Board with the Stop hook only. No mid-run injection, so no risk of derailing a first pass. The research note documents the Stop-hook block with a continuation cap (RES §4).

**(d) Time budget (EL2)**

| Reviewer | Arithmetic | Result |
|---|---|---|
| ember (not critical) | 41 s + wait up to about 102 s for lunas' tickets + 3 turns x 3.2 s = about 112-126 s | below or tied with luna's extended end |
| luna (critical) | 3 turns x 6.4 s = 19.2 s; hook calls 1.4 s; ticket 0.5 s | +21.1 s |
| Panel | 116 + 21.1 = 137 s (ember's 126 s is below this) | **+18.2%** |
| Tokens (per package) | ember 3 x 0.3k = 0.9k; luna 2 x 3 x 0.15k = 0.9k; 3 ticket lines about 0.1k each | +2.1k on 21.2k = **+10%** |

**(e) Safeguards.** Tickets carry codes and regions covered, and the hook shows only the moves not yet applied. It never shows covered regions as a reason to skip. The extra move is assigned from a rotating permutation, so the three reviewers do not all pick the same move. Peers can only add a move; nothing a peer concluded is visible. Alarm: the share of runs in which all three reviewers end on the same extra move (should be 0 by construction) and the common alarms.

**(f) Expected gain.** One move per reviewer, about 0.26 of each catalog move per run, with q = 0.6 for the short cap: 0.26 x 1.04 x 0.6 = **0.16 total**: 0.13 on the 14-issue scale, 0.03 on the control. Range: 14-issue 0.03-0.26; control 0.01-0.05. Targets: all eight moves evenly, so mainly T1 and T2b by chance of selection. Prompting share about 60%, so net collaboration about 0.05. This design is mostly a reminder; its value is that it is cheap and safe.

**(g) Effort.** Board layer 130 lines (shared). Increment about 50 lines: ticket parser and union in the Stop hook (about 30), move assignment by cost class (about 20). Smallest of the five.

**(h) Failure modes.** The model omits or mangles the `moves:` line (the hook then treats it as "no moves applied" and logs it). A non-Claude model ignores the block reason. ember's 70 s wait overlaps with luna's stop; if luna finishes first ember gets only one ticket. At the very end a reviewer is tired: quality is lower (hence q = 0.6).

---

### 2.5 Design 5: Shadow Resume

**(a) Mechanism and roles (baseline HL2; variant on EL2).** This design uses the fastest reviewers' free time in the shadow of the slowest one.
- **Phase 1, isolated.** haiku, luna and luna run exactly as today. No messages.
- **haiku is the isolated canary.** It stays isolated for the whole run and never receives a digest, so it is a clean measure of what the exchange adds.
- **Phase 2, in haiku's shadow.** When both lunas are done (about 116 s), the harness builds a deterministic digest from the *other* luna's findings block and resumes each luna with `claude -p --resume <session_id>`. Each luna gets one digest and at most 8 turns. The harness replaces each luna's report with its phase-2 report.
- **Variant on EL2.** There is no slow member, so only ember is resumed after the lunas finish.
- sonnet is the shadow holder in the SL2 variant: lunas finish about 105 s, sonnet at about 228-274 s, so phase 2 is free there as well. grok is excluded: 790 s median would set the critical path at seven times the EL2 baseline.

**(b) Communication schedule**

| Item | Value |
|---|---|
| Trigger | both fast reviewers have finished phase 1; harness only, no model-authored message |
| Digest content | for each finding of the other luna: reference, an axis derived from its category (contradiction -> consistency, unpassable-check -> satisfiability, missing-requirement -> completeness, other -> other) and the moves line; plus the list of catalog moves nobody applied. No claim text, no severity, no blocking flag |
| Messages per reviewer per package | 1 digest in; phase-2 report out |
| Size cap | digest 800 chars |
| Schema | `kind:"dig"` with `for`, `items:[{ref,axis}]`, `unapplied:[...]` |
| Extra turns | at most 8 per resumed reviewer; hard `timeout 60` on phase 2 |
| Scaling | one digest per resumed reviewer; O(n) |

**(c) Transport.** Between-phase digest by the harness plus `--resume`. It needs no hooks and is deterministic. It requires dropping `--no-session-persistence` from the launcher and keeping the same working directory so the session can be found. `--resume` with a gateway model id is UNVERIFIED.

**(d) Time budget (HL2, 238 s per package, cap +83 s)**

| Step | Arithmetic | Result |
|---|---|---|
| Both lunas end phase 1 | about 116 s | |
| Digest build | about 1 s | |
| Resume start | about 3 s (ASSUMPTION) | |
| Phase 2 | 8 turns x 6.4 s = 51 s | lunas finish about 171 s |
| Panel end | haiku still runs until about 238 s | **+0%** |
| Rule | the harness never waits for phase 2 more than 15 s past the slowest phase-1 reviewer; late phase-2 work is dropped and phase 1 is kept | worst case +15 s = +6% of 238 s |
| Tokens (per package) | 2 lunas x 8 turns x 0.15k = 2.4k, plus addenda 2 x 0.6k = 1.2k | +3.6k on 63.7k = **+5.7%** |

EL2 variant: ember phase 2 starts at about 116 + 1 + 3 = 120 s, then 8 turns x 3.2 s = 25.6 s, so the panel ends about 146 s: **+25.5%**; tokens +3.0k on 21.2k = +14%.

**(e) Safeguards.** Each luna finishes a full isolated first pass before it sees anything, so its independent list exists. The digest carries axes and references, no conclusions or clearances. The canary haiku never sees any digest, so its findings are the clean reference and the echo measure compares luna's phase-2 findings with haiku's. Receivers must verify with their own tool calls. Alarm: common alarms; additionally, flag if phase-2 findings that merge into haiku's rows exceed phase-1's share by more than 10 points (which would mean convergence rather than discovery).

**(f) Expected gain (on HL2).** Each luna runs 8 turns: about 2 moves each, so about 2.6 distinct moves per run after overlap: P(executed) about 0.33 per move with q = 0.8: 0.33 x 1.04 x 0.8 = **0.27 total**: 0.23 on the 14-issue scale, 0.05 on the control. Range: 14-issue 0.06-0.46; control 0.01-0.09. EL2 variant (ember only): about 0.14 total. Targets: all eight moves, through T1 and T2b. Prompting share about 60%, so net collaboration about 0.14 of the 0.23. This has the best elapsed time and the best cost per issue, once `--resume` is verified.

**(g) Effort.** Board layer not needed. Increment about 120 lines: digest builder (about 70), phase wrapper with `timeout` and report replacement (about 40), resume prompt (about 10), plus launcher edits. Roughly 160 lines including launcher changes.

**(h) Failure modes.** `--resume` with a non-Claude gateway id fails; session storage is tied to the working directory (`/tmp/evalsb/repo`); a resumed luna already has its own conclusions and may simply re-state them (a no-op phase 2). If haiku finishes early (below 100 s), the 15 s rule is what protects the cap. Only useful when a slow member exists.

---

## 3. Comparison table

All figures are per package against the named isolated baseline, with the harness fixes applied to both sides. Gain is on the 14-issue scale; control (I7) is the second figure. Low-high is 0.25x to 2x of central. "Net collaboration" removes the part a static list of moves would also capture.

| Redesign | Baseline | Elapsed overhead | Output tokens overhead | Gain central /14 (low-high) | Control I7 central (low-high) | Net collaboration share /14 | Contamination risk | Effort (new lines) | Reliability | Output tokens per added issue (3 pkgs) |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 Claim-Index Relay | EL2 | +23.3% | +14% | 0.17 (0.04-0.33) | 0.04 (0.01-0.09) | 0.07 | Medium (herding on a shared list) | about 170 | Medium | about 53k |
| 2 Axis-Flip Relay | EL2 | +28.8% | +18% | 0.14 (0.03-0.28) | 0.04 (0.01-0.07) | 0.09 | Low-Medium (axes only; echo is the risk) | about 205 | Medium-Low (post compliance) | about 84k |
| 3 Sweep Desk | EL2 | +28.8% | +28% | 0.18 (0.04-0.35) | 0.05 (0.01-0.10) | 0.11 | Low (facts with commands) | about 250 | Low-Medium (wait loop, compliance) | about 100k |
| 4 Exit Ticket | EL2 | +18.2% | +10% | 0.13 (0.03-0.26) | 0.03 (0.01-0.05) | 0.05 | Low | about 180 | **High** | about 48k |
| 5 Shadow Resume | HL2 (EL2 variant +25.5% / +14%) | **+0%** (HL2) | +5.7% (HL2) | 0.23 (0.06-0.46) | 0.05 (0.01-0.09) | 0.14 | Low-Medium (digest read after own pass; canary) | about 160 | Medium-High once `--resume` is verified | about 47k |
| Control A2: static move kit, no exchange (not a redesign) | EL2 | +29% | +30% | 0.33 (0.08-0.66), assumption | 0.07 | 0 by definition | None | about 25 (brief only) | High | about 57k |
| Reference: sonnet + 2x luna, no redesign | | +136% (821 vs 348 s) | +119% (139k vs 64k) | +0.50 measured (2.33 vs 1.83, p = 0.51) | 1.33 vs 0.83 | n/a | none | 0 | High | about 150k |
| Harness fixes alone (shown separately in 2.0.6) | EL2 | about 0% | about 0% | +0.14 (0.03-0.34) | 0 | n/a | none | about 70 | High | about 0 |

Effort counts the 130-line shared board layer for designs 1-4 (design 5 does not need it), plus the increment from 2.1-2.5. Harness fixes (about 70 lines) are counted separately and are needed by every arm. The figures for tokens per added issue use the per-package token overhead x 3 divided by the central 14-issue gain; they are low-confidence.

**Reading the table.**
1. The static kit (A2) is estimated to beat every exchange design on gross gain, because it assigns all eight moves from the first second and spends ember's idle time. Communication earns its place only if it beats A2 by the margin set in section 4.
2. If no exchange arm beats A2, the right design is the cheapest one: put the kit in the brief, with fixed slot assignments.
3. Design 5 has the lowest cost to serve once `--resume` is verified, but it needs a panel with a slow member.

---

## 4. Recommended first experiment

**Scope.** Three existing packages (DS, AL, DE), existing blind Opus judge per (row, package) against hidden ground truth, existing `findings-v1` merge and ledger. Reviewer models: ember, luna, luna. Opus only judges. Panel EL2 (design 5 on HL2 is a second stage).

**Spikes first (about half a day, no scoring):**
1. Do hook commands see the board path (embedded in `--settings`, not environment)? Does a PostToolUse `additionalContext` string reach ember and luna (gateway models) and appear in the next turn? Use `--include-hook-events`.
2. Does a Stop hook `decision:"block"` work in `-p` mode with gateway models, with the `stop_hook_active` guard?
3. Does `claude -p --resume <id>` work with gateway ids and without `--no-session-persistence`?
4. Measure real seconds per turn and tokens per tool-only turn for ember and luna, and replace the assumptions in 2.0.1.
5. Re-score the raw findings of the 30 cheap runs with the anchor normalizer. This costs judge calls only and tells how much the 200-character drop hid.

**Arms (same fixed harness; reviewers run with `NOFALLBACK=1`; model identity audited on every run):**

| Arm | What it is | Purpose | Runs |
|---|---|---|---|
| A0 | Historical EL2 on the old harness (6 runs, CR:441) | Harness share = A1 minus A0 | none new |
| A1 | EL2, harness fixes, isolated | Contemporaneous control | 12 |
| A2 | A1 plus static move kit: G1-G8 in the brief, fixed slots (ember G5-G8, luna-a G1 and G3, luna-b G2 and G4) | Separates "telling them the moves" from communication | 12 |
| A3 | Design 4, Exit Ticket | Cheapest exchange | 6, extended to 12 if it passes the interim look |
| A4 | Design 3, Sweep Desk | Idle-lane legwork | 6, extended to 12 |
| A5 | Design 2, Axis-Flip Relay | Targets T2a | 6, extended to 12 |

Designs 1 and 5 are deferred: design 1's value is mostly in A2 plus A4, and design 5 needs an HL2 baseline and the `--resume` spike.

**Cost.** One run is three package runs. Maximum 60 runs x 3 = 180 package runs = 540 reviewer runs; about 4.5M output tokens (A1 about 63.6k per run, A2 about 83k, A3 about 70k, A4 about 82k, A5 about 75k). If all three exchange arms stop at the interim look: 378 reviewer runs. Concurrency as in the study: 10 total, ember at most 4. Block-randomize run order (each block is one replicate of every arm on all three packages) to cancel gateway load drift. About 4-5 hours of wall time plus judging.

**Metrics (all from the existing judge on the merged ledger, plus the raw-union rescoring):**
- **Primary: hard-issue credits per run** (the ten hard issues, summed over three packages).
- Secondary: found /14, control found /2, real blocking, wrong blockers, elapsed per package (median of the slowest reviewer plus any phase), reviewer output tokens, convergence alarms.

**Interim look at 6 runs.** Stop an arm if its hard credits are at or below A1's, or its median elapsed overhead exceeds +35%, or the convergence alarm fired in 3 or more of 6 runs.

**Decision rule (set before running).** Adopt arm X only if all hold at the final look:
1. Hard credits per run exceed A2's by at least 0.25, with one-sided permutation p at most 0.10, or X has at least 4 runs with a hard credit against at most 1 for A2 (Fisher p at most 0.10).
2. Wrong blockers per run are not more than 0.5 above A2's and real blocking is not lower.
3. Median elapsed per package is at most 1.35 times A1's.
4. The convergence alarm fired in at most 25% of X's runs.
5. At least 90% of hard credits carry first-hand evidence (the receiver's own transcript contains the command).

If no exchange arm passes but A2 beats A1 by at least 0.25 on hard credits, adopt A2 alone (the kit, no communication). If A2 does not beat A1, and A1 does not beat A0 by more than noise, then neither the harness nor the prompting nor the exchange moves the numbers at this size, and the gap is model-bound. Power note: baseline hard credits are 0 in 30 runs; with 12 runs, 4 or more hard-credit runs against 0 gives Fisher p about 0.04, so only effects of about +0.3 hard credits per run or more are reliably detected.

**What the experiment answers from the open questions in the seed brief.**
- Cross-document reasoning vs reading strategy: A2 against A1 (moves vs no moves).
- Can headless sessions poll mid-run: spikes 1 and 2.
- Challenge vs shared findings: arm A5 (axis, no findings) against A4 (facts).
- How much the harness closes alone: A1 against A0.

---

## 5. Requirements

**H. Harness fixes (every arm)**

| ID | Requirement | Test |
|---|---|---|
| H-1 | The reviewer brief names the absolute path of `source.md` for the package and tells the reviewer to read it first. | Transcript has a tool call naming `source.md` in at least 98% of runs (baseline 77% of 665 runs). A run that fails is re-run once. |
| H-2 | A normalizer copies each report before merge and truncates `anchor` and `anchor2` to their first 200 characters (still an exact substring of the candidate) and `claim` to 300. Originals stay unedited. `findings-v1` and `superclaude review merge` are unchanged. | Unit test: a 250-character anchor yields one finding with a 200-character anchor and a non-null span. Zero findings dropped for length across all arm runs. |
| H-3 | The reviewer sandbox is built from each plan's base commit (the parent of its first implementing commit; resolution per package is UNVERIFIED), with `.dev/tasks`, `.dev/eval-workspaces`, `.dev/research`, `.dev/reflect` and `.dev/brainstorms` removed. The base sha is written to the manifest. | `find /tmp/evalsb/repo -path '*/.dev/reflect*'` is empty. For DS the repaired `draft_guard_unavailable` sentence is absent from `refs/merge-guard.md`; for AL the narrowed `tiers.md` sentence is absent; for DE the worker-contract table lacks the new entries. |
| H-4 | The brief asks for MINOR notes to be written into the findings block with severity MINOR and blocking false. | At least one MINOR finding in 50% or more of runs, and the judge scores any severity. |
| H-5 | The launcher validates each report with the real parser and logs dropped lines instead of the presence-only `BLOCK_OK`. | Dropped-line count logged per run, 0 after H-2. |
| H-6 | The judge also scores the union of raw reviewer findings, not only the merged ledger. | Both scores stored for every run. |

**B. Board and hooks**

| ID | Requirement | Test |
|---|---|---|
| B-1 | The transport is the JSON board with PostToolUse and Stop hooks passed through `--settings`, plus the between-phase digest for design 5. No cross-session messaging, Orca mail or A2A in the first experiment. | Launcher and settings inspected. |
| B-2 | The board path is embedded in the hook command strings. | A run with the environment cleared still delivers a seeded message. |
| B-3 | One writer per file, append only, `jq -c` validated. | No malformed line in any board file across all runs. |
| B-4 | Hook cost is at most 150 ms per tool call at p95. | Measured in spike 4. |
| B-5 | Hooks print nothing when there is nothing new. | Zero empty injections in the transcript. |
| B-6 | Board files are kept per run as the audit log. | Present for every run of every exchange arm. |

**S. Schema and caps**

| ID | Requirement | Test |
|---|---|---|
| S-1 | Messages follow schema v1; the hook drops and logs any that fail it or whose `note` contains a verdict word. | Seeded bad messages are dropped. |
| S-2 | Size caps: idx 1,200; axis 160; req 160; res 500; exit 120; exit digest 240; phase digest 800 characters. | Board logs never exceed them. |
| S-3 | Per-reviewer per-package message caps: design 4 one out and one in; design 3 luna two out and three in, ember three results; design 2 ember three out, luna two out, two in each; design 1 one index; design 5 one digest. | Hook counter enforced; logs never exceed. |
| S-4 | Extra-turn caps: 3 (designs 2, 3 and 4 per reviewer), 8 (design 5). | Hook counter stops exchange work at the cap and logs the stop. |

**C. Independence and contamination**

| ID | Requirement | Test |
|---|---|---|
| C-1 | Nothing is injected before the reviewer's 6th tool call. | No injection timestamp earlier than call 6. |
| C-2 | Injected text contains only moves, axes, references, requests and facts, never a region marked covered or fine. | Grep of injected text for ok, fine, correct, passes, verified, no issue returns nothing. |
| C-3 | A finding that uses a peer's fact has a matching command in the reviewer's own transcript. | At least 90% of hard-issue credits pass this audit. |
| C-4 | The three convergence alarms of 2.0.5 are computed for every run and every arm and reported in the results table. | Script `convergence-alarm.py` (about 110 lines) produces one row per run. |
| C-5 | Design 5 keeps haiku isolated; in the EL2 arms, A1 is the isolation reference. | Haiku transcripts contain no injected text. |
| C-6 | The move catalog text names no file, task or defect from the three packages, and is applicable to a plan that is not one of them. | A grep of the catalog for the package-specific tokens listed offline by the harness author returns nothing; two other completed plans (`.dev/tasks/done`, no ground truth) are run once as a behaviour check (moves used, findings per run). |

**Design-specific**

| ID | Requirement | Test |
|---|---|---|
| D4-1 | Exit Ticket: the Stop hook parses the `moves:` line, writes the ticket without a model turn, assigns one move by cost class using a rotating permutation, and blocks the stop once. ember waits at most 70 s for peers' tickets; luna waits 0 s. | Median panel elapsed per package at most 1.35 times A1's (about 157 s on EL2). No run ends on a block loop. |
| D3-1 | Sweep Desk: requests expand to fixed sweep templates; ember stops taking requests at 95 s from run start and handles at most 3; luna never waits for a result; every result card includes its command string. | ember finishes by 100 s in 95% of runs; panel elapsed overhead at most +35%; receivers' re-run mismatch rate at most 10%. |
| D2-1 | Axis-Flip: relay follows the fixed axis table; the surface axis is never relayed; a reference anchored by two or more reviewers is relayed once. | Board logs contain no `surface` relay; echo rate at most 30%. |
| D1-1 (stage 2) | Claim-Index: ember posts one index of at most 12 entries after its 5th call; lunas receive it after their 6th. | Index posted in at least 90% of runs. |
| D5-1 (stage 2) | Shadow Resume: phase 2 runs only while a slower reviewer is still running; it is killed 15 s after the slowest phase-1 reviewer ends; the digest comes from the harness. | Panel elapsed overhead at most +6% on HL2; `--resume` works with the gateway id (spike 3). |

**E. Evaluation**

| ID | Requirement | Test |
|---|---|---|
| E-1 | Arms, run counts, block randomization and concurrency caps as in section 4. | Run log shows the order and the caps. |
| E-2 | `NOFALLBACK=1`; observed model equals expected model on 100% of runs; any run with an API error is quarantined and re-run once (as in HO2 H1-H12). | Identity audit script returns 0 mismatches. |
| E-3 | The blind judge is the existing Opus judge, unchanged; labels are random; the judge never sees the board, ground truth is hidden from reviewers. | Judge inputs list contains only the merged, anonymised report. |
| E-4 | The decision rule in section 4 is written into the manifest before the first run. | Manifest timestamp earlier than the first arm run. |
| E-5 | The results table reports three shares per arm: harness (A1 minus A0), prompting (A2 minus A1), collaboration (arm minus A2). | Table present with all three columns. |
| E-6 | Elapsed overhead is computed from per-run wall time of the slowest reviewer plus any phase, as medians against A1. | Script output matches the meta files. |

**Known unverified items (resolve before relying on any number above)**
- Per-package baselines are three-package figures divided by 3.
- Seconds per turn and tokens per turn are derived from medians.
- Hook cost of 0.1 s per call, the 3 s resume start and the act rate a = 0.7 are assumptions.
- Hooks inheriting the board path, `additionalContext` reaching gateway models, Stop-hook blocks in `-p` mode, and `--resume` with gateway ids are untested.
- `--max-turns` is not in this build's help.
- The base commit for H-3 is not recorded in an obvious file for any of the three packages.
- All c, P and prompting-share numbers are my judgment. The sample (3 packages, 10 hard issues) cannot calibrate them; the experiment is what does.
