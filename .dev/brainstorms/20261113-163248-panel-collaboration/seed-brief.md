---
topic: "Redesign the tasklist review panel so reviewer models communicate and collaborate DURING their runs to find issues they would not find alone"
domain: architecture
strategy: systematic
depth: deep
proposals_target: 5
handoff_target: none
created: 2026-11-13T16:32:48Z
---

# Seed Brief: panel-collaboration

Dialogue mode: non-interactive (no `--interactive`); the Clarify/Validate/Probe answers below come from the owner's request and the study record, not from live answers.

## Problem Statement

Reviewer models on the tasklist review panel run in isolation: each gets the same brief, reviews alone, and only a deterministic script merges their findings afterwards. Over 76 valid-era runs every panel found only about 2-2.5 of 14 known defects. Ten of the 16 known issues were never found by any run made only of the cheap models (ember, luna, haiku; 30 runs), and four were never found by any run at all. The owner wants five redesigns in which models exchange information while they are still reviewing, so one model's work changes where or how another looks.

## Known Context

- Evidence base: `.dev/eval-workspaces/tasklist-review-panel/20261111-a1/` (COMBO-REPORT.md final sections, analysis/allsets, analysis/issue-table, per-package ground-truth.json and reviewer reports), hand-off `HANDOFF-review-panel-unification-run2.md`.
- Never found by ember/luna/haiku-only panels (30 valid-era runs, sets S01, S03, S04, S05, S07, S10, S13, S24): B1, B2, B5, B6, B8, I1, I4, I5, I6, I7. Of these, other panels did find B5 (3 runs), B6 (1), B8 (1), I1 (3), I4 (4), I7 (9). Nobody ever found B1, B2, I5, I6 (computed from analysis/allsets 2026-11-13).
- Easy issues dominate: B3 (68 of 76 runs), I8 (56), I2 (52).
- Harness defects depress all numbers: the merge drops findings with anchors over 200 or claims over 300 characters (49 blocking findings lost); 156 of 665 runs never opened source.md; terra/sol often return empty reviews.
- Current timing baselines (elapsed, reviewers parallel, 3 packages): ember + 2x luna ~348 s, ember + luna ~300 s, haiku + 2x luna ~715 s, sonnet + 2x luna ~821 s (COMBO-REPORT final tables).
- Reviewers today run as headless `claude -p --model <raw gateway id>` sessions (tools/run-reviewer.sh); non-Claude models run through the same CLI via the gateway.

## Constraints

- Each redesign adds at most 35% to panel elapsed time versus its isolated baseline.
- Communication must be efficient and reliable; candidates to evaluate: Orca agent mail, Claude Code agent messaging (SendMessage / teams), the A2A protocol, plain JSON files. Simplicity and speed of implementation rank first.
- Must state when and how often agents communicate.
- Must show how each design keeps one model's blind spots from contaminating another (no anchoring on a peer's conclusions, no convergence onto the same easy issues).
- Must estimate the expected gain in issues found, grounded in the study data.
- Reviewers stay read-only; no reviewer sees ground truth; the deterministic merge contract (findings-v1, ledger) keeps working or is explicitly replaced.
- Models available: ember, luna, haiku (cheap core), sonnet, grok; Qwen and glm excluded; Opus reserved for judging.

## Success Criteria

- Five distinct redesigns, each with: communication schedule (when, how often, message size), transport choice with rationale, time budget arithmetic showing at most +35%, contamination safeguards, and a found-issue gain estimate tied to specific missed issues (B1-B8, I1-I8).
- Three evidence-based theories, from parallel investigation of reviewer reports and transcripts, explaining why ember/luna/haiku missed those issues; each redesign maps to at least one theory.
- A recommended first experiment that can be run on the existing three packages and scored with the existing blind judge.

## Open Questions

- Do the missed issues need cross-document reasoning (plan vs source.md vs repo code), which isolated cheap models skip, or a different reading strategy within the plan?
- Can headless `claude -p` gateway sessions poll a file or mailbox mid-run, or must collaboration happen between phases of a run?
- Is a mid-run message more valuable as a challenge ("prove Task 1 AC3 is satisfiable") than as shared findings?
- How much does fixing the harness (source.md named in the brief, anchor limit) close the gap on its own, independent of collaboration?

## Enrichment Context

Full artifacts (read them; this is a summary): `enrichment/investigation-designspec.md`, `enrichment/investigation-alias-control.md`, `enrichment/investigation-patterns.md` (699 runs; scripts and tables in `enrichment/pc-patterns/`), `enrichment/research-light.md` (communication transports).

### Investigative patterns per model (valid era, medians per run; investigation-patterns.md)

| Model | Wall s | Thinking tokens | Search style | Notes |
|---|---|---|---|---|
| ember | 41 | 7.1k | greps the lines the plan cites; touches files via `ls`/`grep -n` | 46% of findings local single-section, 43% category "other", 21% about artifact path/hash/line numbers; anchors Task 1 in 52% of designSpec runs but states the real defect ~3% |
| luna | 102 | 3.6k | reads named files whole, almost never searches (4% of runs search tests/) | 1.75 findings/run, 72% marked blocking; repeats one objection (Task 12 artifact path) |
| haiku | 233 | 45.8k | searches tests/ in 81% of runs but only inside files the plan names | volume and shape near sonnet; more wrong blockers (0.65 vs 0.17) |
| sonnet | 228 | 22.9k | greps the whole repo for the feature; opens unnamed dependents (3.1 unnamed files/run vs luna 0.3) | the only model (plus grok once) to find I7 cleanly |
| grok | 790 | 48.5k | broad; saw CHANGELOG.md:166 (GT10) and dropped it as minor | slow |

Thinking tokens track issues found across models (Spearman 0.64), and within every model the higher-thinking half finds more.

### Three theories for why ember + luna + haiku never found B1, B2, B5, B6, B8, I1, I4, I5, I6, I7

- **T1 Plan-bounded search scope.** Cheap models only verify what the plan names. They never run a reverse-dependency sweep ("which tests and docs reference the files this plan edits?") or a universal-claim sweep ("the plan says 'all'/'only': list every file it covers and count the violators"). Evidence: `tests/skills/test_worker_contract.py` was opened in 0 of 176 cheap control runs; 7 of the 8 runs (sonnet/grok) that opened it found I7, 0 of 225 others did; 5 of 11 haiku runs had it in grep output and never opened it. B8 (alias "all other primitives use aliases") and I5/GT10 (stale "43 members" in CHANGELOG.md:166) need exactly this sweep. Explains I7, B8, B6, I5; partly I6.
- **T2 Right place, wrong question.** Cheap models anchor the right sentence but ask one local question and stop (shallow single pass). They do not trace every branch, test satisfiability or stopping rules, or check the other direction. Evidence: 16 cheap findings sat on the exact GT10 sentence but all asked "does the grep match too much", none "where else is this claim"; 3 findings analysed GT5's mapping but traced only the mode-off path; ember anchors Task 1 in 52% of runs yet no reviewer in any panel challenged Task 1 AC3's unbounded "complete inventory" (B1/B2 need "what finite check proves 'every'?"); GT9 was found only by sonnet comparing the AC's grep literally against the ordered heading text. Explains B1, B2, B5, I4, I5; partly I1.
- **T3 The evidence environment and grading rules hide or suppress defects.** The reviewer sandbox is a checkout taken after these plans were implemented and repaired: the fixes for GT5 (refs/merge-guard.md:146), GT6 (merge_guard.py:256) and GT9 (pr-submit.md:81) are already in the code, so a plan-vs-code check makes the plan look right; source.md is the only place the original rules live, and 14 of 39 ember designSpec reports never opened it. 44 of 98 cheap alias reviewers saw the already-narrowed tiers.md:42 and never compared it with Task 7's broader claim (B8). The brief grades an unstated requirement as Medium (non-blocking) and has no missing-task category; luna reports blocker-grade items only; grok dropped GT10 as minor. Contamination finding: the sandbox still holds `.dev/reflect/pre-design-20261108041729/REPORT.md`, which names I7; 2 of the 9 I7 credits read it (clean count 7). Explains I1, B5, I4 (checkout masks), I5 (minor rule), I7 (missing-task category); is a harness confound for all.

### Hints that could trigger each miss without giving the answer (from both missed-issue investigations)

| Issue | Investigative move needed | Hint a peer could send |
|---|---|---|
| B1, B2 (designSpec Task 1 AC3) | stopping-rule / satisfiability check | "For each criterion that says every/all/complete, state the finite check that proves it" |
| B5 (GT5) | trace every halt branch through the exit-report mapping vs source 4.1 | "What does the mapping return after each halt reason?" |
| I1 (GT6) | check every value the status mapping reads is written by some fold row, against source.md not the checkout | "Check producer/consumer pairs against source.md, not the code" |
| I4 (GT9) | compare an AC's literal grep with the text the task orders | "Run each grep criterion against the exact text the task tells you to write" |
| I5 (GT10) | other-direction sweep for a changed claim | "Where else in the repo is this claim stated?" |
| B6, B8 (alias) | universal-claim count; goal vs what the tests can fail on | "Count the files an 'all/only' sentence covers and how many break it" |
| I6 (alias GT4) | apply a constraint check found for one task to every other task | "You found a constraint violation in Task 6; apply the same check to Tasks 3 and 7" (untested: nobody ever found I6) |
| I7 (control GT1) | reverse-dependency search | "grep tests/ for the files the plan edits; open test files the plan never names" |

### Communication transports (research-light.md)

| Option | Fit for headless `claude -p` reviewers | Verdict |
|---|---|---|
| Orca agent mail | reviewers launched by bash have no mailbox; per-reviewer mailboxes need `worker-start`, which starts interactive agents | Rejected |
| Claude Code cross-session messaging | works between separate `claude -p` processes started with `--name` and `--settings '{"crossSessionInbound":"accept"}'`; delivered between tool calls during an active turn. Agent teams cannot spawn in `-p` mode | Possible; UNVERIFIED: arrival after a reviewer's last turn, and whether gateway models call the tool correctly |
| A2A protocol | HTTP request/response, no way into a running turn; needs a wrapper server per reviewer | Rejected (most effort) |
| JSON board | each reviewer appends to `$PANEL_BOARD/<id>.jsonl` via a Bash helper; a PostToolUse hook injects unread peer lines as `additionalContext` after each tool call; a Stop hook does a last check; about 40 lines of bash; durable audit log | Recommended for mid-run; UNVERIFIED that hooks inherit PANEL_BOARD/PANEL_ID |
| Between phases | harness writes one digest; phase 2 starts fresh with it, or `claude -p --resume <session_id> "<digest>"` | Recommended for phase exchange |

### Time budget facts

Panel elapsed time is set by the slowest reviewer (reviewers run in parallel). Median per run: ember ~41 s, luna ~102 s, haiku ~233 s, sonnet ~228 s. Isolated panel elapsed over 3 packages: ember + luna ~300 s, ember + 2x luna ~348 s, haiku + 2x luna ~715 s, sonnet + 2x luna ~821 s (COMBO-REPORT). A +35% cap on ember + 2x luna is about +40 s per package. The faster reviewers' idle time until the slowest finishes (e.g. ember idle ~60 s while luna works; ember and luna idle ~130-190 s while haiku works) can host collaboration without adding elapsed time.

### Harness confounds every redesign must account for

The 200/300-character merge drop (49 blocking findings lost), source.md not named in the brief (156 of 665 runs never opened it), the post-implementation checkout (masks GT5, GT6, GT9, B8), and the `.dev/reflect` leak (I7). A redesign's gain estimate must state which part is collaboration and which part is fixing these.
