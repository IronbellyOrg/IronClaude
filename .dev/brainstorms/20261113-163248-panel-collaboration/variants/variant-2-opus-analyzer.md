# Requirements specification: reviewer collaboration during tasklist review panel runs (variant 2 of 5, analyzer lens)

> Date 2026-11-13. Read-only analysis; no file was edited. Path abbreviations: **EVAL** = `.dev/eval-workspaces/tasklist-review-panel/20261111-a1`, **ENR** = `.dev/brainstorms/20261113-163248-panel-collaboration/enrichment`, **CR** = `EVAL/COMBO-REPORT.md`. Issue labels follow CR:401-417 (B1-B5 and I1-I5 are designSpec GT1-GT10; B6-B8 and I6 are alias GT1-GT4; I7 and I8 are control GT1-GT2). "Found /14" counts the 14 issues on the two defect-rich packages. I7 is scored separately on the control package (/2). Timings are per package and come from the 3-package totals in CR divided by 3.

---

## 1. Theories

### 1.0 Method and the theory this variant rejects

Every miss was traced through a three-gate funnel: **exposure** (did the reviewer reach the evidence?), **question** (did it ask the question that exposes the defect?) and **survival** (did the finding survive the grading rules, the merge and the sandbox?). A defect is found only if all three gates pass. The three theories below each correspond to one gate, and each refines the seed's T1-T3.

One alternative theory is rejected as a primary cause: **reasoning budget** (cheap models think less). Across models, thinking tokens correlate with issues found (Spearman 0.64). Inside ember and luna, however, the hard-issue rate does not rise with thinking (ember 0.25 to 0.22, luna 0.09 to 0.09 hits per run, comparing the lower-thinking half of runs with the higher half). For haiku it does rise (0.29 to 0.70) (ENR/investigation-patterns.md §6, Theory A). Budget explains why haiku's results vary from run to run. It does not explain why ember and luna never get past their ceiling. Buying more tokens is therefore not the fix.

### 1.1 Theory A (refines T1): the search frontier is seeded only by the plan's own citations

**Statement.** Cheap reviewers build their list of places to look from what the plan cites: named files, named lines and cited source sections. Two kinds of evidence never get onto that list: (a) files that depend on the files the plan edits, and (b) paths that appeared in the reviewer's own tool output but were never opened. The deciding variable is not search volume but what the search is aimed at.

| Evidence | Number | Source |
|---|---|---|
| Files touched that the plan does not name, per run | ember 0.8, luna 0.3, haiku 0.9 vs sonnet 3.1, grok 1.2 | ENR/investigation-patterns.md §1 |
| Runs that touched a test file the plan does not name | ember 8%, luna 1%, haiku 0% vs sonnet 35%, grok 33% | same |
| `tests/skills/test_worker_contract.py` opened on the control package | cheap 0 of 176 (ember 0/69, luna 0/82, haiku 0/25); sonnet 7/26, grok 1/8 | same |
| Opening that file was close to decisive for I7 | 7 of 8 openers reported I7; 0 of 225 non-openers did | same §4 |
| The file was seen but not opened | 5 of 11 haiku control reviewers had it in grep or `ls` output and never opened it | ENR/investigation-alias-control.md §2 |
| Search volume is not the variable | haiku searches `tests/` in 81% of runs (5.2 recursive searches per run), but only inside the test file the plan names | ENR/investigation-patterns.md §6 Theory B |
| luna follows citations literally | luna read source.md in 48 of 48 control runs (where the tasks cite source sections) vs 11 of 48 alias runs (where they do not) | ENR/investigation-alias-control.md §2 table |
| Root files outside every sweep | `CHANGELOG.md` was touched in 1 of 233 designSpec runs, and I5 was never found | ENR/investigation-patterns.md §4 |
| The narrowed sentence was seen but not compared | 44 of 98 cheap alias reviewers saw the repaired `refs/tiers.md:42`; none compared it with Task 7's universal claim | ENR/investigation-alias-control.md §2 |

**Weakens it.** Even sonnet ran a reverse-dependency sweep in only 7 of 26 control runs, and none of B1, B2 or I4 needs a file outside the plan.

**Explains:** I7, I5 and B8 directly. It explains B6 in part (the scored route ran through the `/model` rows in `refs/chains.md`) and I6 in part (the "frontier" there is the plan's other tasks).

**Implication for collaboration.** luna reliably opens what it is pointed at. A peer that supplies pointers can therefore move luna's frontier without changing luna's style. This is the strongest single argument for collaboration in the data.

### 1.2 Theory B (refines T2): one hypothesis per anchor, no enumeration, no propagation

**Statement.** Cheap reviewers often anchor the right sentence. They then test one question along one direction and stop. They do not enumerate input cases, test the other direction of a completeness claim, ask for a stopping rule, or carry a check that worked in one task over to the other tasks.

| Evidence | Number | Source |
|---|---|---|
| I5: right anchor, wrong direction | 16 cheap findings (15 ember, 1 haiku) sit on the I5 sentence; all ask "does the grep over-match", none ask "where else is the claim" | ENR/investigation-designspec.md §2c |
| B5: right mapping, one input case | 3 findings (luna g6-r2/t4-1, luna g5-r4/t4-1, ember e3/t2b-1) analyse the exact mapping but trace only the mode-off case, never the halt case | same |
| I1: right row, different question | 1 finding (haiku g7-r1 M2) | same |
| B1/B2: right task, no stopping-rule question | Task 1 is anchored in 52% of ember and 92% of haiku designSpec runs; the unbounded inventory is matched in 3%; no finding in any panel anchors O3 or AC3 | ENR/investigation-patterns.md §3, §5; ENR/investigation-designspec.md §2c |
| The same defect class is found next door | B3 (an AC with an undefined "any condition" scope) is found in 68 of 76 valid-era runs, but the check is never carried to Task 1 AC3's "every pin" | CR:498 |
| I6: a constraint check is never propagated | the sibling B7 comparison was made by luna h1-r2/t4-1 and luna g7-r2/t4-2 (both blocking) and by ember h1-r4/t3-1, and never repeated on Task 7 (candidate line 109) or Task 3 (line 66) | ENR/investigation-alias-control.md §2 |
| B6: observation present, framing wrong | luna g6-r3/t4-1 F2 saw the `/model` lines and graded them "unclear exemption" rather than goal-vs-test contradiction | same §3 |
| I4: no literal reading | 0 cheap findings on Task 12 AC1; only sonnet compared the grep with the ordered heading text (4 of 26) | ENR/investigation-designspec.md §3 |

**Weakens it.** Haiku performs in-plan checks at close to sonnet's level (B3 88% vs 100%) and still misses B1. Single-axis checking is therefore a habit of the whole model class, not a capacity limit.

**Explains:** B1, B2, B5, I4, I5 (direction), I6, B6 (framing), and I1 in part.

**Implication for collaboration.** What is missing is a second question asked at a known location. A peer can supply the location (its own anchor) and a different question (a generic move) without supplying a conclusion.

### 1.3 Theory C (refines T3): the sandbox and the report/merge contract hide, invert or erase detections

**Statement.** Even when exposure and question succeed, four harness properties suppress the finding:

1. The sandbox shows the repaired code, so plan-vs-code checks confirm the plan.
2. The brief never names source.md, so source-only rules go unseen.
3. The grading rule pushes missing tasks to Medium, and blocker-only reporters (luna) drop them.
4. The merge silently deletes long findings.

| Evidence | Number | Source |
|---|---|---|
| The checkout already contains the repairs | B5 at `refs/merge-guard.md:146`, I1 at `merge_guard.py:256`, I4 at `commands/pr-submit.md:81`, B8 at `refs/tiers.md:42`; `CHANGELOG.md:166` is the only defect left visible | ENR/investigation-designspec.md header; ENR/investigation-alias-control.md §1 |
| A code check confirmed a planted defect | ember g5-r2/t3-1 grepped `pr-submit.md`, saw the repaired heading, and the I4 check came back clean | ENR/investigation-designspec.md §2b |
| source.md not opened | 156 of 665 valid-era runs (ember 81/209 = 39%, luna 49/222 = 22%, haiku 15/75) | CR:373 |
| Merge drops | 49 blocking findings lost; dropped findings by model: ember 33, luna 30, haiku 7, sonnet 0 | CR:292 |
| Grading suppresses missing tasks | unstated requirements are graded Medium (`EVAL/tools/run-reviewer.sh:17`); all 7 true I7 findings were non-blocking; luna's findings are 72% blocking at 1.75 per run; grok saw `CHANGELOG.md:166` and dropped it as "minor" | ENR/investigation-patterns.md §2, §6 Theory C; ENR/investigation-designspec.md §3 |
| Crowding by surface findings | "already implemented / stale line" findings fill cheap reports (surface findings: ember 21%, luna 23%) | ENR/investigation-patterns.md §2 |
| Leak | `.dev/reflect/pre-design-20261108041729/REPORT.md` names I7; 2 of 9 I7 credits came after reading it; no cheap reviewer opened it | ENR/investigation-alias-control.md §3 |

**Explains:** I1, B5 and I4 (masking), B8 (masking), I5 (the "minor" drop) and I7 (category and leak). It also depresses every number in the study.

**Implication for collaboration.** Collaboration cannot fix this gate. Only harness fixes can: a pre-implementation checkout, naming source.md in the brief, a merge normalizer and removal of the leak. Every gain estimate below therefore reports the harness share (H) and the collaboration share (C) separately.

### 1.4 Which gate blocks each never-found issue

| Issue | Gate A: exposure | Gate B: question | Gate C: survival | Peer move that could open the blocked gate |
|---|---|---|---|---|
| B1 | in plan (Task 1 anchored 52-92%) | **fails**: no stopping-rule question | rubric favours "wrong build" | M3 stopping rule, M7 carried from B3 |
| B2 | needs source.md:341 | **fails**: body scope vs AC scope | source not opened (39% of ember) | M9 scope match |
| B5 | needs source.md:112 | **fails**: one input case only | **fails**: checkout repaired | M4 input enumeration, M8 against source |
| B6 | in plan and chains.md | **fails**: framing | none | M2 quantifier inventory, M7 |
| B8 | **fails**: no inventory of `model:` lines | partial | **fails**: tiers.md:42 narrowed | M2 |
| I1 | needs the source.md:200 vs :206 table pair | **fails** | **fails**: checkout repaired | M8 |
| I4 | in plan | **fails**: no literal reading | **fails**: checkout heading passes | M5 |
| I5 | **fails**: root files never searched | **fails**: wrong direction | **fails**: "minor" drop | M6 |
| I6 | in plan | **fails**: no propagation | none | M7 |
| I7 | **fails**: unnamed test file | needs a missing-task framing | Medium grade; leak inflates others | M1 |

---

## 2. Five redesigns

### 2.0 Shared building blocks (used by every redesign)

**Move catalog (fixed, plan-agnostic).** This is the only advice text that may ever travel between reviewers. Each move names a kind of check, never a defect.

| Id | Move | Catalog sentence delivered to the receiver |
|---|---|---|
| M1 | Reverse dependency | "List files in the repository (tests and docs included) that reference a file this plan edits; open any the plan never names and check whether a task or gate misses them." |
| M2 | Quantifier inventory | "For a sentence that says all, only, every or none about files or primitives, list the set it ranges over and count the members that break it." |
| M3 | Stopping rule | "For an acceptance criterion that says every, all, any or complete, state the finite check that proves it; if none exists, the criterion cannot be shown to pass." |
| M4 | Input enumeration | "For a rule, mapping or table, list every input case, including halts, errors and the no-record case, and trace what each returns." |
| M5 | Literal check | "Run or simulate each command in an acceptance criterion against the exact text the task tells the implementer to write, not against the current file." |
| M6 | Other direction | "For a count, number or name the plan changes, search the whole repository, root files included, for other places that state the old form." |
| M7 | Propagation | "Apply a check that produced a finding at one task to every other task and every other place the plan dictates similar text." |
| M8 | Producer and consumer | "For each value a mapping or check reads, find the source rule or table row that writes it, in the source document, not in the checked-out code." |
| M9 | Scope match | "Compare the scope in a task's instruction with the scope its acceptance criterion checks and with the source document's scope for that item." |

**Message schema `panel-msg/1`** (one JSON line, at most 400 bytes):

| Field | Rule |
|---|---|
| `v` | `"panel-msg/1"` |
| `run`, `pkg`, `from`, `seq` | run id, package id, sender reviewer id, sequence number from 1 |
| `t` | seconds since panel start |
| `kind` | `locator`, `challenge`, `propagate`, `coverage`, `witness` or `harvest` |
| `move` | `M1` to `M9` |
| `target.doc` | `candidate`, `source` or `repo` |
| `target.quote` | optional; at most 120 characters, copied verbatim from candidate.md or source.md, and checked to be present |
| `target.path`, `target.line` | optional; a repository-relative path that must exist in the sandbox, plus a line number |
| `scope` | optional; must match one of `Task <n>(,<n>)*`, `all tasks` or `all acceptance criteria` |
| Forbidden | `claim`, `severity`, `blocking`, `verdict`, any other key, any free text |

The receiver sees: "Peer move (M3, stopping rule): <catalog sentence>. Where: <quote or path:line>. Scope: <scope>. This is a place and a method, not a finding; decide yourself." Because no free text is allowed, a reviewer cannot transmit a conclusion. For the same reason, issue-specific text derived from ground truth cannot travel either.

**Natural seal (independence).** A reviewer's first complete report, the first time it stops, is its sealed independent pass. No peer content reaches a reviewer before its seal, except in D3 and the content-free mid-run note in D4. The sealed report is saved for attribution. Findings added after the seal use ids that start with `X` (allowed by the findings-v1 id rule at `src/superclaude/cli/review/findings.py:26`).

**Harness fixes** (prerequisites, H): (H1) name `/tmp/evalsb/cand/<pkg>/source.md` in the brief; (H2) a pre-merge normalizer that cuts an anchor longer than 200 characters to a verbatim substring of at most 200 characters, and a claim longer than 300 characters to 297 characters, recording each cut in a sidecar file, so `findings.py:104-120` drops nothing; (H3) a per-package sandbox built from the plan's base commit; (H4) `.dev/reflect/` excluded from the sandbox.

**Convergence alarm (common, measurable).** CI is the mean pairwise Jaccard of the sets of Tasks anchored by the panel's reviewers in the final reports for one package, computed as in ENR/investigation-patterns.md §3. Isolated references from that table: ember+luna 0.25, luna+luna 0.33, haiku+luna 0.23, luna+sonnet 0.21. A run raises the alarm if CI(run) minus CI of the same panel in the harness-fixed isolated arm is 0.15 or more, **or** if more than 50% of the run's X-findings merge (through `superclaude review merge` clustering) into the same ledger row as a sealed finding of the reviewer that triggered them (claim echo). An arm raises the alarm if it fires in more than 1 of 6 runs, or if the number of distinct issues ever found across the arm falls below the isolated arm's.

**Gain model.** P(find) = P(trigger exists) x P(message delivered and acted on) x P(defect stated and survives). The inputs come from the evidence above. Where no cheap model has ever executed a move, the low end assumes close to nothing happens. The harness share (H) per panel is estimated once:

| Harness fix | Effect on found /14 per run | Basis |
|---|---|---|
| H2 anchor normalizer | +0.05 to +0.15 | ember and luna lose about 0.15 dropped findings per reviewer-run (CR:292); most were on redundantly found issues |
| H1 source.md named | +0.0 to +0.1 directly | cheap reviewers who did read source still missed B5 and I1; this fix is mainly a prerequisite for M8 and M9 |
| H3 base-commit checkout | +0.05 to +0.3 | unmasks B5, I1, I4 and B8 for code checkers; removes "already implemented" crowding |
| H4 leak removal | 0 on /14; -0 to -0.33 on control for sonnet panels | 2 of 9 I7 credits were leaked; no cheap reviewer read the leak |
| **H total, cheap panels** | **+0.1 to +0.5** | the sum, rounded |

---

### D1. Frontier Relay (pointer sharing, aimed at Theory A)

**(a) Mechanism.** Panel: ember + 2x luna. **ember** is the *scout*. It does its normal review and also runs three bounded sweeps:

- M1: grep `tests/`, `docs/` and the repository root for each file the plan edits.
- M2: count the set behind each universal sentence about files.
- M6: search the whole repository, root included, for each old count or name the plan changes.

It posts each unexpected file or quote as a `locator`. A PostToolUse hook on every reviewer also **harvests** paths that appear in that reviewer's tool output but are never opened by any reviewer, as `harvest` lines, with no model action needed. This is aimed at haiku-style "seen not opened" misses. The two **luna** reviewers are *followers*. When a luna first stops, a Stop hook hands it up to 2 ranked locators: unnamed test files first (based on the 7-of-8 I7 evidence), then root docs, then others. The two lunas receive alternating ranks, so they never get the same file. Each luna opens its locators and reissues its complete report. No Opus or sonnet reviewer takes part. Opus is used only by the blind judge.

**(b) Schedule.**

| Item | Value |
|---|---|
| Send triggers | ember: after each sweep result (expected at 20-55 s); hook: after every tool call (harvest) |
| Delivery trigger | the receiver's first Stop (natural seal); one delivery only |
| Maximum sent per package | ember 6 locators; harvest 4 per package (all reviewers combined) |
| Maximum received per package | each luna 2 (time-guarded, see d); ember 2 harvest lines |
| Size cap | 400 bytes per line; rendered delivery at most 1,200 characters |
| Schema | `panel-msg/1`, kind `locator` or `harvest`, moves M1, M2, M6 |

**(c) Transport.** JSON board plus hooks. Each reviewer appends to `$BOARD/<rid>.jsonl` through a `panel-post` Bash helper that validates the line with `jq`. The PostToolUse hook harvests paths. The Stop hook delivers with `decision: "block"` and the messages as `reason`. Why this transport: receiving is model-agnostic, which matters because luna and ember are gateway models; the board is durable and doubles as an audit log; and the change is about 40 lines of bash at its core (ENR/research-light.md §4). Two reasons make it workable in this sandbox. Reviewers already load project hooks there (`/tmp/evalsb/repo/.claude/settings.json` registers PreToolUse hooks), and `--settings` adds the panel hooks. UNVERIFIED: whether the hooks receive the board path, and whether a Stop block in `-p` mode yields a reissued full report. Both need a spike (requirement R-20).

**(d) Time budget.** Baseline is the isolated panel ember + 2x luna: 348 s / 3 = **116 s per package** (CR:331). Cap: 116 x 1.35 = **156.6 s**.

| Reviewer | Phase-1 finish | Added work | Finish |
|---|---|---|---|
| ember | 41 s median | 4 sweep calls x 3.4 s plus posting, about 14 s | about 55 s (idle afterwards, off the critical path) |
| luna A | about 102 s | 2 locators x (Read 7 s + 4 s reasoning) + reissue the report 12 s = 34 s | about 136 s |
| luna B (slowest) | about 116 s | same 34 s | about 150 s |

Time guard: the number of locators delivered = min(2, floor((150 - t_stop - 12) / 11)), so a luna that stops at 135 s or later gets none. Expected elapsed time is about 150 s (**+29%**), with a worst case of about 156 s (+34%). ember's sweeps run inside the time the lunas take anyway, so they add no elapsed time.

**(e) Contamination safeguards.**

| Shared | Withheld |
|---|---|
| file paths and verbatim quotes, each tagged with a catalog move | every claim, severity, verdict and finding; the sealed reports; ember's opinion of a file |

How the defences work:

- **Independent first pass:** nothing is delivered before the receiver's first Stop.
- **Blind-spot spreading:** a locator carries no interpretation, so a sender's wrong reading (for example "the grep over-matches") cannot travel. Locators are ranked by file type, not by the sender's interest, and the two lunas receive disjoint locators.
- **Board access audit:** reviewers can find the board path through `env`, so every transcript is scanned for any command that touches the board outside `panel-post`. A hit quarantines the run.
- **Alarm:** the common CI and claim-echo alarm, plus a D1-specific check: the share of X-findings anchored on a delivered locator. This share is expected to be high. It raises an alarm only if it is also accompanied by a CI rise.

**(f) Expected gain (per run, out of 14; control /2 separately).**

| Target | Theory | Path | P low-high |
|---|---|---|---|
| I5 | A + B | ember M6 finds `CHANGELOG.md:166` (0.3-0.6), luna or ember reports it (0.3-0.5) | 0.08-0.30 |
| B8 | A | M2 count of `model:` lines (0.2-0.4), luna frames it as a contradiction (0.3-0.5) | 0.05-0.20 |
| B6 | A + B | M2 or M1 reaching the chains.md `/model` rows, framed as goal vs test | 0.02-0.08 |
| I7 (control) | A | M1 or harvest lists the test file (0.7-0.9), luna opens it (0.8), reports the missing update (0.3-0.6); two lunas | 0.25-0.60 /2 |

C = **+0.15 to +0.58 /14** (point estimate 0.3), plus +0.25 to +0.60 on control. H = +0.1 to +0.5. Assumptions: luna's pointer-following rate on source.md (48/48) carries over to locators; luna's habit of reporting mostly blockers halves its reporting of Medium findings. Nothing here reaches B1, B2, I4 or I6.

**(g) Effort.** `tools/panel/panel-post` (20 lines), `hook-harvest.sh` (35), `hook-stop.sh` (45: cursor, time guard, rendering), and `run-reviewer.sh` changes (+25: `--settings` hook JSON, board env, a fallback that takes the last assistant message containing findings-v1). The scout brief adds about 15 prompt lines. Total about **140 lines**.

**(h) Failure modes.**
- The hook does not receive the board path: no delivery, and the run behaves as isolated (fails closed).
- A blocked luna replies with an addendum instead of the full report: the fallback takes its sealed report, so the collaboration gain is lost but nothing breaks.
- ember skips the sweeps: it skipped source.md in 39% of runs, so expect partial compliance.
- A large test file read (more than 3,000 lines) pushes luna past the time guard.
- A reviewer reads the board directly: caught by the audit.

---

### D2. Axis-Flip Cross-Examination (challenges on peer anchors, aimed at Theory B)

**(a) Mechanism.** Panel: ember + 2x luna. Phase 1 is the unchanged isolated review. A deterministic digest builder reads each peer's findings-v1 block with `parse_block` (`src/superclaude/cli/review/findings.py:124`) and turns each peer finding into a **challenge**: the peer's anchor (where to look) plus a move that differs from the peer's axis (what else to ask). The move comes from a fixed flip table:

| Peer finding signal (harness-side, never shown to the receiver) | Moves sent | Evidence-based target |
|---|---|---|
| category `unpassable-check` | M3 on all acceptance criteria containing every, all, any or complete; M7 | B3 (68/76) carried to B1 |
| category `contradiction` | M7 (all tasks), M9 | B7 sibling carried to I6; B6 |
| anchor contains a command, grep or literal | M5, M6 | the 16 one-direction near-misses on I5; I4 |
| anchor inside a mapping, table or "returns/gives" rule | M4, M8 | the B5 (3) and I1 (1) near-misses |
| category `missing-requirement` | M1 | I7 |
| surface finding (path, hash, line numbers) | M2 on the nearest universal sentence in the same task, else none | moves attention off surface findings |

**ember** examines the lunas' anchors. Each **luna** examines ember's anchors and the other luna's anchors. Each reviewer is resumed with its digest and returns the complete report, keeping its phase-1 findings and adding X-findings.

**(b) Schedule.**

| Item | Value |
|---|---|
| Trigger | a reviewer has finished phase 1 **and** at least one report from a reviewer of a different model exists; the digest uses all peer reports available at that moment |
| How often | once per reviewer per package |
| Maximum received | 3 challenges per reviewer per package (1 per task; tasks the receiver did not anchor come first); 1 of the 3 is a decoy, chosen by a trigger regex on candidate.md at a place no peer flagged |
| Maximum sent | not applicable (harness-generated); each peer finding produces at most 1 challenge per receiver |
| Size cap | 400 bytes per challenge; digest at most 1,500 characters |
| Schema | `panel-msg/1`, kind `challenge` |

**(c) Transport.** Between-phase digest. The phase-2 run is `claude -p --resume <session_id> --model <id> "<digest>"`. This requires removing `--no-session-persistence` from `EVAL/tools/run-reviewer.sh:48`, the root cause that blocks resuming today. The fallback is a fresh session given the phase-1 report plus the digest. Why this transport: it is deterministic, needs no hooks and no unverified mid-turn behaviour, and the harness fully controls message content. Of the five designs it is the most reliable and the simplest to implement.

**(d) Time budget.** Baseline ember + 2x luna, **116 s per package**; cap 156.6 s.

| Reviewer | Phase-1 end | Phase 2 starts | Time box | End |
|---|---|---|---|---|
| ember | 41 s | at the first luna finish, about 102 s | min(35, 150 - start - 4) | at most about 141 s |
| luna A | about 102 s | 102 s (ember's report already exists) | same | at most about 141 s |
| luna B | about 116 s | 116 s | 30 s | at most about 150 s |

The 4 s covers the resume start-up. ember's 61 s idle window (41-102 s) is absorbed by the wait. Expected elapsed time is about 145 s (**+25%**), with a worst case of about 150 s (+29%). A phase 2 that times out keeps its phase-1 report.

**(e) Contamination safeguards.**

| Shared | Withheld |
|---|---|
| peer anchors (quotes from the candidate) plus a flipped move | peer claim, category, severity, blocking flag and verdict; whether a location came from a finding or is a decoy |

How the defences work:

- **Independent first pass:** phase 1 is fully isolated and saved.
- **Blind-spot spreading:** the flip table always sends a move **different** from the peer's axis, so the receiver is pushed onto the axis the peer missed, not toward the peer's conclusion. Decoys stop the receiver from inferring that "a peer found something here".
- **Spreading attention, not concentrating it:** the cap of one challenge per task, with tasks the receiver did not anchor first, spreads coverage instead of piling onto the easy B3 area.
- **Alarm:** the common CI and claim-echo alarm. Claim echo is measured exactly here: an X-finding that the merge clusters with the challenging peer's finding.

**(f) Expected gain (per run, out of 14).**

| Target | Theory | Path | P low-high |
|---|---|---|---|
| I5 | B | ember anchors the I5 sentence in 38% of designSpec reports (15/39); a luna runs M6 repo-wide (0.3-0.6) and reports it (0.4-0.6) | 0.05-0.25 |
| B1 | B | a peer's B3 `unpassable-check` produces M3 over all ACs; a luna isolates Task 1 AC3 among about 40 ACs | 0.05-0.25 |
| I4 | B | an anchored command AC gets M5 | 0.02-0.08 |
| B5 | B | an exit-report anchor (about 3% of reports) gets M4 or M8 | 0.01-0.05 |
| B2, I1, I6, B6, B8 | B | small single-step chains | 0.01-0.17 combined |
| I7 (control) | A | a missing-requirement anchor gets M1 | 0.05-0.20 /2 |

C = **+0.15 to +0.8 /14** (point estimate 0.35). The high end requires cheap models to carry out flipped moves at rates never observed; no cheap model has ever made the B1 move. H = +0.1 to +0.5.

**(g) Effort.** `tools/panel/digest.py` (90 lines: reuses `parse_block`, flip table, priority, decoy, rendering). `run-reviewer.sh` (+40: persist the session, capture `session_id` with `jq`, a phase-2 function with timeout and fallback). A panel driver to sequence the phases (+40). Total about **170 lines**. No hooks.

**(h) Failure modes.**
- `--resume` with gateway model ids is UNVERIFIED: use the fresh-session fallback, at higher token cost.
- The resumed session re-runs the `/sc:spec-panel` skill prompt: the phase-2 prompt must not start with a slash command.
- The time box cuts phase 2: the phase-1 report is kept.
- Wrong blockers rise: lunas grade 72% of findings blocking, and challenges invite new blockers. The decision rule (section 4) guards against this.

---

### D3. Pattern Propagation Relay (true mid-run, aimed at Theory B propagation)

**(a) Mechanism.** Panel: haiku + 2x luna. Whenever a reviewer records a finding produced by a comparison or constraint check, it immediately sends one `propagate` message: the move (M7, plus M3 or M9), the place where the check worked, and scope `all tasks`. The **lunas** finish around 102 s and are the main senders. Their messages reach **haiku**, which is still running until about 233 s and is the main receiver. haiku applies the propagated check to the other tasks. This is the only design with a peer-discovered trigger for I6: luna made the B7 sibling comparison in cheap rows and never carried it to Task 7 or Task 3. The two lunas also exchange messages with each other while both are still running.

**(b) Schedule.**

| Item | Value |
|---|---|
| Send trigger | right after the sender finalises a finding whose category is `contradiction` or `unpassable-check` (mid-run) |
| Delivery | between the receiver's tool calls, during its active turn |
| Maximum sent | 2 per reviewer per package |
| Maximum acted on | 2 per receiver per package; messages arriving after the receiver has begun its final report are ignored |
| Size cap | 400 bytes |
| Schema | `panel-msg/1` as a single JSON line in the SendMessage text, kind `propagate` |

**(c) Transport.** Claude Code cross-session messaging. Each `claude -p` is launched with `--name panel-<run>-<pkg>-<rid>` and `--settings '{"crossSessionInbound":"accept"}'`; senders call `SendMessage` (ENR/research-light.md §2c). Why this transport: it needs the least code (two flags plus prompt text) and delivers into a running turn with no hook. This design also serves as the panel's test of whether mid-run messaging is worth having. UNVERIFIED: whether gateway models call `SendMessage` with the right name, and what happens to messages sent to a session that has already exited. There is no send-side validation and no board audit log, so audit reads the `SendMessage` tool_use inputs from the transcripts.

**(d) Time budget.** Baseline is the isolated panel haiku + 2x luna: 715 s / 3 = **238 s per package** (CR:319). Cap 321 s.

| Reviewer | Isolated finish | Added | Finish |
|---|---|---|---|
| luna A / B | about 102 / 116 s | 2 sends (about 3 s each) + at most 2 luna-to-luna propagations x 10 s | at most about 140 s (off the critical path) |
| haiku | about 233 s (critical path) | at most 2 propagations x about 26 s per step (233 s / 9 tool calls) + 8 s | at most about 293 s |

Expected elapsed time is about 290 s (**+22%**), with a worst case of about 300 s (+26%). No harness-side time box is possible mid-run, so time overruns are measured; the stop rule is in section 4.

**(e) Contamination safeguards.**

| Shared | Withheld |
|---|---|
| move, the place where the check worked, scope | claim, severity, verdict; there is no seal, because delivery is mid-run |

How the defences work:

- **Independent first pass:** only partly protected. The receiver is told to finish its current check and to treat a propagation as an extra task, never as evidence. Its pre-message findings are identified by timestamp for attribution.
- **Blind-spot spreading:** propagation copies a *method* to other places, never a verdict about the original place.
- **Enforcement:** free text cannot be blocked at send time, so post-hoc transcript audit marks any message with non-schema content and excludes that run.
- **Alarm:** the common alarm, plus a check that the share of haiku's findings falling on tasks named in received messages stays at most 0.5.

**(f) Expected gain (per run, out of 14).**

| Target | Theory | Path | P low-high |
|---|---|---|---|
| I6 | B | a luna makes the B7 sibling comparison (B7 found in 2 of 5 haiku + 2x luna runs) (0.25-0.4) x delivered and acted on (0.5-0.8) x haiku carries it to Task 7 line 109 / Task 3 line 66 (0.2-0.5) | 0.03-0.16 |
| B1 | B | needs a luna B3 finding; luna's B3 rate is about 10% | 0.02-0.10 |
| B6, B8 | B | goal-vs-task contradictions propagated | 0.02-0.11 |
| I4 | B | literal-check propagation | 0.00-0.04 |

C = **+0.07 to +0.41 /14** (point estimate 0.2). It is low because haiku, not luna, finds most patterns, and haiku finds them late, after the lunas have exited. H = +0.1 to +0.4 (haiku has 7 dropped findings and skipped source.md in 15 of 75 runs).

**(g) Effort.** `run-reviewer.sh` (+3: `--name`, `--settings`). Prompt addendum with peer names and the message template (15 lines). Transcript audit script for `SendMessage` inputs (40). A 10-minute spike. Total about **60 lines**: the least code, but the most unverified.

**(h) Failure modes.**
- Gateway models misname peers or never send.
- `ListAgents` shows dozens of local sessions, so names must be unique per run.
- Sends to an exited session fail or silently start a new turn (UNVERIFIED).
- No durable log.
- haiku overruns the cap.
- Free text gets in, which is a contamination risk.

---

### D4. Coverage-Matrix Steering (content-free coordination, aimed at Theories A and B and at convergence)

**(a) Mechanism.** Panel: sonnet + 2x luna. Before the run, the harness builds the plan's **applicable cell matrix**: Task x move, using trigger regexes on candidate.md. Examples: an AC containing every/all/any/complete gets M3; an AC containing a command gets M5; a task that edits files gets M1; a sentence with all/only gets M2; a constraint quoted in dictated text gets M7. This gives about 25 cells per plan. Reviewers log each check they make with `panel-cover <Task> <Move>`.

- **Mid-run:** a PostToolUse hook tells each reviewer which cells peers have *already covered*. This is counts only, so it can be shared safely and steers reviewers away from duplicates.
- **At first Stop:** each **luna** is assigned 2 *uncovered* cells, chosen deterministically by hashing the reviewer id so the two lunas get disjoint cells. It may be blocked up to 3 times, which uses its idle window while sonnet runs.
- **sonnet**, the broad searcher (3.1 unnamed files per run), receives one block with 2 uncovered cells.

No finding, quote or path is ever exchanged.

**(b) Schedule.**

| Item | Value |
|---|---|
| Send | `panel-cover` after each check (reviewer-initiated); at most 30 cover lines per reviewer per package |
| Mid-run delivery | after each tool call, only when the covered set changed; at most 6 notes per reviewer per package |
| Stop delivery | luna: up to 3 blocks x 2 cells while t < 230 s; sonnet: 1 block x 2 cells while t < 300 s |
| Size cap | 300 bytes per note (cell ids only); 400 bytes per board line |
| Schema | `panel-msg/1`, kind `coverage` (fields `move`, `scope` = `Task <n>`; no target) |

**(c) Transport.** JSON board plus PostToolUse and Stop hooks, the same infrastructure as D1. Why: the content is computed by the hook, and gateway models only need to call one Bash helper. The Stop hook is the only mechanism that can keep a fast `-p` reviewer working inside the slow reviewer's idle window.

**(d) Time budget.** Baseline is the isolated panel sonnet + 2x luna: 821 s / 3 = **274 s per package** (CR:424). Cap 370 s.

| Reviewer | First Stop | Added | Finish |
|---|---|---|---|
| luna A / B | about 102 / 116 s | up to 3 blocks, cut off at 230 s | at most 240 s (off the critical path) |
| sonnet | about 228-274 s | 1 block, 2 cells, about 40 s; no block if t > 300 s | at most about 314 s |

Expected elapsed time is about 300 s (**+10%**), with a worst case of 314 s (+15%).

**(e) Contamination safeguards.**

| Shared | Withheld |
|---|---|
| which (Task, move) cells someone has checked | everything else: no quotes, paths, claims or findings |

How the defences work:

- **Independent first pass:** uncovered-cell assignments arrive only after the first Stop. The mid-run notes reveal coverage, not results.
- **Blind-spot spreading:** cannot happen, since nothing about content is shared. The mechanism exists to stop reviewers converging on the same cells.
- **Alarm:** CI must *fall*. The arm raises an alarm if CI rises at all, or if cell-log compliance (logged cells divided by distinct Tasks anchored) is below 0.5, because then the matrix is fiction.

**(f) Expected gain (per run, out of 14).**

| Target | Cell | P low-high (net of sonnet's own finds) |
|---|---|---|
| B1 | Task 1 x M3 | 0.05-0.20 |
| I5 | Task 2 x M6 | 0.03-0.15 |
| B8 | alias Task 7 x M2 | 0.03-0.12 |
| I6 | alias Task 7 x M7 | 0.02-0.10 |
| I4 | Task 12 x M5 (sonnet already 2 of 6) | 0.02-0.10 |
| B2 | Task 1 x M9 | 0.01-0.05 |

C = **+0.16 to +0.72 /14** (point estimate 0.3). H = +0.05 to +0.35 (sonnet has no merge drops, skipped source.md in only 1 of 63 runs and has the most to gain from H3; minus up to 0.33 on control from leak removal).

**(g) Effort.** `panel-cover` (20 lines), cell-matrix builder (40, regex), PostToolUse hook (35), Stop hook with hash assignment (50), `run-reviewer.sh` (+20). Total about **165 lines**, of which about 60 are shared with D1.

**(h) Failure modes.**
- luna does not log cells (luna makes only 1 Bash call per run).
- Regex cells miss the real defect class.
- The extended lunas add wrong blockers.
- sonnet ignores its block.
- Re-issued reports are truncated: same fallback as D1.

---

### D5. Source-Rule Witness (aimed at Theory C's source-blind gate, via Theory B)

**(a) Mechanism.** Panel: ember + luna + sonnet. **ember** acts as *witness* as well as reviewer. It runs one batched Bash sweep over source.md: for each normative sentence (one containing MUST, reports, sets, returns, gives, halts), it greps the plan for the sentence's key terms. It posts up to 5 `witness` locators of two kinds: source lines with no counterpart in the plan (M8 or M9), and source table pairs where a reader and its writer live in different tables (M8). **luna** and **sonnet** receive up to 3 witness locators each at their first Stop. They check them against source.md, never against the checkout, which already holds the repairs. This mechanises the move that found B5 for sonnet (`grep -n "unavailable" candidate.md`, ENR/investigation-designspec.md §3) and the table-against-table check that found I1 for grok.

**(b) Schedule.**

| Item | Value |
|---|---|
| Send | ember, after its sweep (expected at about 65 s) |
| Delivery | Stop-gated, once per receiver |
| Maximum | ember sends 5; each receiver gets at most 3 (luna and sonnet get different top-ranked lines where possible) |
| Size cap | 400 bytes per line |
| Schema | `panel-msg/1`, kind `witness`, `target.doc` = `source`, moves M8 or M9 |

**(c) Transport.** JSON board plus a Stop hook, reusing D1's code. Why: it shares D1's verified-or-not infrastructure, so it adds almost no new risk beyond D1.

**(d) Time budget.** Baseline is the isolated panel ember + luna + sonnet: 676 s / 3 = **225 s per package** (CR:320). Cap 304 s.

| Reviewer | First Stop | Added | Finish |
|---|---|---|---|
| ember | about 41 s | witness sweep about 20 s | about 65 s |
| luna | about 102 s | 3 x 10 s (source.md is already in its context) | about 132 s (off the critical path) |
| sonnet | about 225 s | min(3, floor((290 - t - 10) / 10)) locators, at most 35 s | at most about 260 s |

Expected elapsed time is about 255 s (**+13%**), with a worst case of about 262 s (+16%).

**(e) Contamination safeguards.**

| Shared | Withheld |
|---|---|
| source.md line numbers and verbatim source quotes, each with a move | ember's interpretation, every finding, every claim |

How the defences work:

- **Independent first pass:** Stop-gated delivery.
- **Blind-spot spreading:** source lines are a neutral reference rather than a peer opinion. The risk is that all receivers chase the same lines, which the per-receiver split limits.
- **Alarm:** the common alarm, plus a check that the share of X-findings citing a witnessed line that duplicate the sealed finding of another receiver stays at most 0.5.

**(f) Expected gain (per run, out of 14).**

| Target | Path | P low-high |
|---|---|---|
| B5 | the witness flags source.md:112's last sentence (0.2-0.4) x receiver states the halt case (0.3-0.6); S14 already found B5 once in 5 runs | 0.04-0.20 |
| I1 | the M8 table pair source.md:200 vs :206 vs :112 | 0.02-0.12 |
| B2 | M9: source O3 at source.md:341 vs the plan's four-file, "every" scope | 0.02-0.10 |

C = **+0.08 to +0.42 /14** (point estimate 0.2). H = +0.1 to +0.4. This design depends on H1, because ember skipped source.md in 39% of runs.

**(g) Effort.** If D1 exists: witness brief addendum (20 prompt lines), witness line kind (10 lines). Otherwise about 150 lines.

**(h) Failure modes.**
- ember's key-term grep floods the board with false "no counterpart" lines.
- ember skips source.md.
- sonnet re-checks against the repaired checkout despite the instruction, which H3 removes.
- A design aimed at Theory C is capped by Theory C fixes it does not itself make.

---

## 3. Comparison of the five redesigns

| Design | Baseline panel (s/pkg) | Elapsed overhead expected / worst | Output-token overhead | Collaboration gain C /14 low-high (point) | Harness gain H /14 | Control I7 gain /2 | Contamination risk | Effort (lines) | Reliability |
|---|---|---|---|---|---|---|---|---|---|
| D1 Frontier Relay | ember + 2x luna (116) | +29% / +34% | +28% (+6k on 21.2k) | 0.15-0.58 (0.3) | 0.1-0.5 | 0.25-0.60 | Low (paths only, Stop-gated) | ~140 | Medium: hook env and Stop-reissue UNVERIFIED; fails closed |
| D2 Axis-Flip Cross-Exam | ember + 2x luna (116) | +25% / +29% | +28% (+6k) | 0.15-0.8 (0.35) | 0.1-0.5 | 0.05-0.20 | Medium (peer anchors; decoys and flip mitigate) | ~170 | **High**: deterministic; `--resume` with gateway ids UNVERIFIED but has a fresh-session fallback |
| D3 Propagation Relay | haiku + 2x luna (238) | +22% / +26% | +20% (+13k on 63.7k) | 0.07-0.41 (0.2) | 0.1-0.4 | ~0 | Medium-high (mid-run, unvalidated sends) | ~60 | Low-medium: gateway `SendMessage` and exit semantics UNVERIFIED |
| D4 Coverage Matrix | sonnet + 2x luna (274) | +10% / +15% | +26% (+12k on 46.4k) | 0.16-0.72 (0.3) | 0.05-0.35 | ~0 (sonnet already 3/6) | **Lowest** (counts only) | ~165 | Medium-low: depends on reviewers logging cells |
| D5 Source Witness | ember + luna + sonnet (225) | +13% / +16% | +18% (+8.5k on 46.2k) | 0.08-0.42 (0.2) | 0.1-0.4 | ~0 | Low-medium | ~30 on top of D1 | Medium |

Reading: no design is expected to lift a panel past about 3 of 14 per run. The combined expectation for the default panel is 1.83 + H (about 0.3) + C (about 0.3), roughly 2.4/14. B2 and I6 stay mostly out of reach. The measurable win is **reach**: the target issues are at 0 of 30 cheap runs today, so any sustained non-zero rate on them is a real change. The second win is control I7 (D1).

---

## 4. Recommended first experiment

**Choice and rationale.** D2 is tested first because it is the most reliable and the most deterministic: it needs no hooks and no unverified mid-turn delivery. D1 is tested second because it has the strongest evidence-based mechanism (luna follows pointers; opening the test file was decisive in 7 of 8 cases). Both run on the default panel, ember + 2x luna (CR:428), so every arm differs from the others in exactly one factor. D3-D5 are deferred: D3 because of the unverified transport, D4 because of cell-logging compliance, and D5 because it depends on D1's infrastructure.

**Spike S0** (gate for A3 and A4, one control-package run each): confirm that

- `--resume` works with `gpt-6-luna` and `muse-ember-1.0`;
- the Stop and PostToolUse hooks fire in `-p` mode and receive the board path;
- a Stop block yields either a reissued findings-v1 report or a correct fallback;
- the board audit scan works.

If the Stop path fails, A4 runs D1 through D2's between-phase transport instead.

| Arm | Content | Runs (x 3 packages) | Measures |
|---|---|---|---|
| A0 | isolated, current harness | 4 fresh (plus the 6 historical S07 runs as context) | gateway drift; reference for H |
| A1 | isolated + harness fixes H1-H4 | 6 | H = A1 - A0; reference for all collaboration arms |
| A2 | A1 + the M1-M9 catalog in the brief, **no communication** | 6 | whether the advice content alone does the work |
| A3 | A1 + D2 cross-examination | 6 | C for D2; communication value = A3 - A2 |
| A4 | A1 + D1 frontier relay | 6 | C for D1; communication value = A4 - A2 |

Total: 28 panel runs, 84 row-packages, about 252 reviewer runs plus phase 2, and about 2.1M reviewer output tokens. Runs are interleaved in waves (one run of every arm per wave, in random order) to spread gateway drift. The study's caps apply: 10 concurrent, ember at most 4, `NOFALLBACK=1`, quarantine and a single re-run.

**Scoring.** The existing blind Opus judge (`EVAL/tools/tmp-scripts/judge-one.sh`, unchanged) scores every anonymised merged final report. For A3 and A4, the merged sealed reports (phase 1 only) are also judged under separate random labels, which gives a within-run attribution of C.

**Endpoints.**
- Primary T: the number of target issues found per run, counting B1, B2, B5, B6, B8, I1, I4, I5, I6 and I7 (I7 on control). Cheap-panel baseline: 0 of 30 runs.
- Secondary: found /14, real blocking /8, wrong blockers, control found /2 and control wrong blockers, elapsed time, output tokens, CI and claim echo.
- Mechanism endpoints, taken from transcripts and the board: designSpec runs with any finding anchored on candidate.md:38 (baseline 0 in all 106 runs); control runs that open an unnamed test file (cheap baseline 0/176); designSpec runs that touch `CHANGELOG.md` (baseline 1/233).

**Decision rule** (pre-registered; applied per collaboration arm X):

1. **Reach:** runs with T >= 1 in X beat A1 under a one-sided Fisher exact test with p < 0.05 (for example 4/6 vs 0/6 gives p = 0.030), **and** X beats A2 by at least 2 runs. Otherwise the gain is credited to the catalog, not to communication.
2. **No loss:** mean found /14 in X is at least A1 minus 0.25; mean wrong blockers is at most A1 + 1.0; mean control wrong blockers is at most A1 + 0.5.
3. **Time:** the median elapsed time per package is at most 1.35 x A1's median, and no package exceeds 1.5 x.
4. **Independence:** the convergence alarm fires in at most 1 of 6 runs; there are zero audit violations (board access outside the helper, any read of ground truth, free text in a message).
5. **Outcomes:**
   - If X passes 1-4, X goes to a 12-run confirmation **on at least two new packages** whose ground truth comes from implement history. The move catalog was derived from these three packages, so in-sample gains are optimistic.
   - If only A2 passes 1-3 against A1, adopt the static catalog and stop the collaboration line.
   - If nothing passes, keep H1-H4 and stop.

---

## 5. Requirements for the chosen designs (D2 primary, D1 secondary, plus prerequisites)

**Harness prerequisites**

- **R-1** The reviewer brief names `/tmp/evalsb/cand/<pkg>/source.md` and tells the reviewer to read it. *Test:* source.md appears in a tool call in at least 95% of A1-A4 reviewer transcripts.
- **R-2** A pre-merge normalizer cuts any anchor or anchor2 longer than 200 characters to a substring of at most 200 characters that `locate()` still finds in candidate.md, cuts any claim longer than 300 characters to at most 300, and records each cut in `<rid>.norm.json`. *Test:* across all runs, merge output reports 0 findings dropped for length, and every normalized anchor is located.
- **R-3** Each package's sandbox is a `git archive` of that plan's recorded base commit, excluding `.dev/tasks/done`, `.dev/eval-workspaces`, `.dev/research` and `.dev/reflect`. *Test:* `refs/merge-guard.md` contains no "`draft_guard_unavailable` reports `unavailable`" rule; `tests/skills/test_model_alias_policy.py` is absent from the alias sandbox; `.dev/reflect` is absent; base commit shas are listed in the manifest.
- **R-4** Reviewers never receive ground truth, other packages' reports, or EVAL paths. *Test:* a transcript scan finds 0 tool calls naming `ground-truth`, `EVAL/` or `arms/`.
- **R-5** The sandbox repository is unchanged by any run. *Test:* `git status --porcelain` in each sandbox is empty after every wave.
- **R-6** Each reviewer's report given to the merge is one findings-v1 report per reviewer per round, unchanged in format. Collaboration findings use ids `X1`-`X9`. *Test:* `superclaude review merge` parses every final report with `block ok true`; every new id matches `^X[0-9]$`.

**Messages and moves (shared by D1 and D2)**

- **R-7** Advice text is restricted to the nine catalog sentences M1-M9, stored in `tools/panel/moves.json`. *Test:* every delivered text equals a catalog sentence plus a target and scope rendered from the template.
- **R-8** Every message is valid `panel-msg/1`, at most 400 bytes, and contains no keys outside the schema. *Test:* a validator over all board and digest lines returns 0 rejects in accepted runs; rejected lines are logged and never delivered.
- **R-9** `target.quote` is a verbatim substring of candidate.md or source.md (located by `locate()`); `target.path` exists in the sandbox. *Test:* the validator checks both before a message is accepted.
- **R-10** No message carries a claim, severity, blocking flag or verdict. *Test:* follows from R-8; additionally a grep of delivered texts for the sender's claim strings finds 0 hits.
- **R-11** The sealed (first) report of each reviewer is stored before any peer content reaches it (D1, D2). *Test:* the seal file's timestamp precedes the first delivery timestamp for every reviewer.

**D2 Axis-Flip Cross-Examination**

- **R-12** `run-reviewer.sh` persists the session (removing `--no-session-persistence`) and records `session_id` in `meta.json`. *Test:* `meta.json` has a non-empty `session_id` for every phase-1 run.
- **R-13** A reviewer's phase 2 starts when it has finished phase 1 and at least one report from a reviewer of a different model exists; the digest uses all peer reports present at that moment. *Test:* the driver log shows the start time and the input report list for each phase 2.
- **R-14** The digest holds at most 3 challenges per receiver, at most 1 per task, with tasks the receiver did not anchor first, and exactly 1 decoy when 3 are sent. Moves come from the flip table in D2 (a). *Test:* a unit test of `digest.py` on the three packages' phase-1 reports checks caps, ordering, decoy count and the flip mapping.
- **R-15** Phase 2 runs with a time box of min(35 s, 150 s - start - 4 s) from panel start; on timeout, an invalid block or a missing findings-v1 block, the phase-1 report is used. *Test:* an injected timeout in a dry run produces the phase-1 report as final.
- **R-16** The phase-2 reply is the complete report: all phase-1 finding ids are present unchanged, followed by any X-findings. *Test:* a script compares the phase-1 ids with the final ids; any loss means the fallback to phase 1 is used and logged.
- **R-17** The phase-2 prompt does not start with a slash command. *Test:* a string check in the driver.

**D1 Frontier Relay**

- **R-18** The ember scout brief requires the M1, M2 and M6 sweeps and posting through `panel-post`, with at most 6 locators per package. *Test:* the board shows at most 6 ember locator lines per package; compliance rate is reported.
- **R-19** The PostToolUse harvest hook appends at most 4 `harvest` lines per package: repository paths seen in tool output that no reviewer has opened. Test files rank first. *Test:* a replay of a recorded transcript produces the expected harvest set.
- **R-20** The Stop hook delivers once per reviewer, at its first Stop, min(2, floor((150 - t_stop - 12) / 11)) locators. The two lunas receive disjoint locators. *Test:* hook unit tests over stop times of 100, 125 and 140 s give 2, 1 and 0 locators; the two lunas' sets do not overlap.
- **R-21** If the final result after a Stop block has no findings-v1 block, the harness uses the last assistant message in the transcript that has one. *Test:* an injected addendum-only reply yields the sealed report.
- **R-22** Hooks fail closed: with no board, no seal or an invalid line, they deliver nothing and the review behaves as isolated. *Test:* running with `PANEL_BOARD` unset leaves the output identical in shape to A1.
- **R-23** A transcript audit flags any tool call that touches the board directory other than through `panel-post`; a flagged run is quarantined and re-run once. *Test:* a planted `cat $PANEL_BOARD/...` call in a dry run is flagged.

**Measurement and decision**

- **R-24** For each run, CI (mean pairwise Task-set Jaccard) and claim echo (the share of X-findings that merge into the triggering peer's ledger row) are computed and compared with A1. *Test:* the script reproduces ENR/investigation-patterns.md §3's ember+luna value of 0.25 (within 0.02) on the historical rows.
- **R-25** Every final merged report, and for A3 and A4 every sealed-report merge, is scored by the unchanged blind judge under random labels. *Test:* score.json exists for each; labels are not derivable from arm names.
- **R-26** Elapsed time per package (first launch to last report), output tokens per reviewer including phase 2, and per-reviewer delivery counts are recorded in `meta.json` / `cost.json`. *Test:* fields are present for every run; the arm-level median elapsed time is computed from them.
- **R-27** The decision rule in section 4 is applied as written and its inputs (T counts, Fisher p, non-inferiority deltas, alarm counts, audit counts) are published in one table. *Test:* the table is reproducible by a committed script that reads only committed inputs (not `/tmp` copies; lesson H10 in `HANDOFF-review-panel-unification-run2.md`).
- **R-28** Gains are reported as H (A1 - A0), catalog content (A2 - A1), communication (A3 or A4 minus A2) and within-run C (final minus sealed), never as one combined number. *Test:* all four rows are present in the results table.

---

*Not checked by this variant:* whether hooks, `--resume` and cross-session messages behave as assumed for gateway models (all marked UNVERIFIED; spike S0 covers them); the plans' exact base commits; the per-step timings, which are medians from investigation-patterns.md and not measured per package. The gain probabilities are reasoned estimates from near-miss counts, not measured rates.
