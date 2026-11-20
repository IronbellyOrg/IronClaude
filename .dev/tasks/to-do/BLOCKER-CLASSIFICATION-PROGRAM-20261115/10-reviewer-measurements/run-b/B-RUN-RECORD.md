# RUN-RECORD (letter B, /sc:reflect --mode pre)

Throwaway material (invented word-count tool). No decision about stage 4 is made here.
Folder: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/throwaway-medium-runs-20261117/B

## 1. Command, times, models, cost
- Invoked by the Skill tool as `/sc:reflect --mode pre` -> `Skill sc:reflect-protocol` with args:
  `--mode pre --spec /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/throwaway-medium-runs-20261117/B/wordcount-spec.md --tasklist /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/throwaway-medium-runs-20261117/B/wordcount-plan.md --output /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/throwaway-medium-runs-20261117/B/reflect-out/`
  Defaults left on: depth standard, tier auto, reviewers 3, t2-engine legacy. Nothing else was set.
- Start (command invoked): about 2026-11-17T05:58Z (folder/spec writing began 05:57:49Z). Command ended: 2026-11-17T06:28:30Z (REPORT.md and contract written). Wall clock about 30 min 40 s (the adversarial merge alone was 1,355,483 ms = 22 min 35 s per the harness).
- Models the run reported: my own session model claude-gw-tier1b[1m]. Reviewers were requested as sonnet, haiku, opus (Agent model override) and self-reported: reviewer-1 "claude-gw-tier1b[1m]", reviewer-2 "GPT-5.2" (requested haiku; mismatch), reviewer-3 "claude-gw-tier1a (Claude, Anthropic)". Blind calibrators and the adversarial orchestrator were requested as opus; the evidence validator as sonnet. Env aliases: opus=claude-gw-tier1a[1m], sonnet=claude-gw-tier1b[1m], haiku=claude-gw-tier2[1m]. The adversarial advocates ran on the session default model per the orchestrator's own report.
- Token or cost figure printed by the command: not printed. The harness reported per-agent subagent tokens (not printed by the command itself): reviewer-1 43,688; reviewer-2 31,946; reviewer-3 55,370; T1 calibrator 43,046; reviewer-card calibrators 41,415 / 41,733 / 45,986; adversarial orchestrator 318,663; evidence validator 67,498. Sum 689,345 subagent tokens (my own orchestration tokens not included, not reported).

## 2. Artifacts (absolute paths)
- Inputs: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/throwaway-medium-runs-20261117/B/wordcount-spec.md ; /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/throwaway-medium-runs-20261117/B/wordcount-plan.md
- Report: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/throwaway-medium-runs-20261117/B/reflect-out/REPORT.md
- Contract: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/throwaway-medium-runs-20261117/B/reflect-out/return-contract.yaml ; audit log: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/throwaway-medium-runs-20261117/B/reflect-out/audit.log
- T1 card: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/throwaway-medium-runs-20261117/B/reflect-out/t1-card.md ; snapshot: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/throwaway-medium-runs-20261117/B/reflect-out/artifacts/input-snapshot.yaml ; matcher and matrix: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/throwaway-medium-runs-20261117/B/reflect-out/artifacts/match.py , /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/throwaway-medium-runs-20261117/B/reflect-out/artifacts/coverage-matrix.json
- Briefs: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/throwaway-medium-runs-20261117/B/reflect-out/reviewer-briefs/reviewer-{1,2,3}.md ; cards: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/throwaway-medium-runs-20261117/B/reflect-out/reviewer-cards/reviewer-{1,2,3}.md
- Merge: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/throwaway-medium-runs-20261117/B/reflect-out/adversarial/merged-verdict-card.md ; /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/throwaway-medium-runs-20261117/B/reflect-out/adversarial/merged-verdict.yaml (written by me from the merge contract) ; /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/throwaway-medium-runs-20261117/B/reflect-out/adversarial/adversarial/{return-contract.yaml,diff-analysis.md,debate-transcript.md,invariant-probe.md,base-selection.md,refactor-plan.md,merge-log.md,variant-1..3-original.md,evidence/EVIDENCE.md,evidence/tokenize-clash/code/*}
- Default output folder .dev/reflect/ was NOT used (my --output pointed into B). The global append .dev/reflect/runs.jsonl and the memory files (docs/memory/reflect/deviation-patterns-brainstorm-reflect-panel.md, .superclaude/memory/reflect/) were NOT written, to stay inside my folder (see section 6).

## 3. Verdict and counts (as the run states them)
- Merged verdict: FAIL, "on B1, B2 and B3". "Counts: 3 blocking; 8 Medium (7 against the plan, 1 review-pipeline follow-up, M8)." Plus 8 note bullets.
- Run status in REPORT.md / contract: partial (adversarial merge status partial, convergence 0.941, 16 of 17 points agreed, 1 unresolved cosmetic point; T1 card authored inline; calibrator_diversity degraded; memory persist skipped).
- Individual reviewer verdicts: reviewer-1 PASS (0 blocking, 4 Medium); reviewer-2 FAIL (1 blocking, 1 Medium); reviewer-3 FAIL (2 blocking, 5 Medium).
- Calibrated confidence: T1 card 0.64; reviewer cards 0.78 / 0.75 / 0.86. coverage_pct null, coverage_pct_union 0.5714 (8 of 14 inferred rows matched), coverage_degraded parsed-sparse, tier 2 forced. Evidence validator: 0 dropped, 6 caveats (listed in REPORT.md).
- I independently reproduced B1 (tokenize.py shadowed by the standard library under pytest: TypeError) in /tmp, removed afterwards. I did not re-run the B3 locale check (E2); the validator confirmed E2 text exists.

## 4. Medium list VERBATIM
Answer to the follow-up-issue question: NO issue created; nothing asked of the owner; the list is recorded here only.

### 4a. Merged card, "Follow-up candidates (Medium)" (copied from /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/throwaway-medium-runs-20261117/B/reflect-out/adversarial/merged-verdict-card.md lines 44-118)
## Follow-up candidates (Medium)

<!-- Source: Base original (Variant 3 M4) per Change #4; Variant 1 M1 merged per Change #4 -->
**M1. It is unclear whether `FILE` in the error messages is the literal word or the file's path.**
- Claim: `wordcount-spec.md:25-26` put `FILE` inside the quoted error text. The same word is a placeholder at `wordcount-spec.md:7-8`. The plan copies the text word for word (`wordcount-plan.md:26-27`), and T5 asserts these strings (`wordcount-plan.md:32`). A test written for one reading fails against the other.
- Why it is Medium: the plan matches the spec, and T4 and T5 come from the same plan, so they will agree with each other. The gap sits in the spec, and only its author can decide (A-003).
- Deviation class: spec gap (inherited).
- Raised by: reviewer-1 and reviewer-3.

<!-- Source: Base modified (Variant 3 M5) per Change #5; Variant 1 M3 merged per Change #5; invariant probe INV-005 per Change #5 -->
**M2. The word rules leave several choices open.**
- "Letters" is not defined as ASCII only or any Unicode letter, though the input is UTF-8 (`wordcount-spec.md:8`, `wordcount-spec.md:12`).
- Lowercasing could mean `lower()` or `casefold()` (`wordcount-spec.md:13`). Under `casefold()`, `ß` becomes `ss`, which changes the printed word (reviewer-1).
- A word is only letters, digits or apostrophes, so an underscore splits words. A tokenizer built on the regex `\w` would keep `_` and break that rule (reviewer-1, reviewer-3).
- The spec does not say whether the curly apostrophe counts as an apostrophe (`wordcount-spec.md:12`, `wordcount-spec.md:14`; reviewer-3).
- Lowercasing before or after splitting changes the words. `"İstanbul".lower()` adds a combining dot, so lowercase-then-split gives `['i', 'stanbul']` and split-then-lowercase gives one word (INV-005).
- Unicode normalization (NFC or NFD) is not stated (INV-005).
- Evidence: `wordcount-spec.md:12-14`, `wordcount-plan.md:8`.
- Why nothing named rests on it: `wordcount-plan.md:8` copies `wordcount-spec.md:12` faithfully, so the defect sits in the spec. The spec example and the plan's one named input are ASCII (`wordcount-spec.md:31`, `wordcount-plan.md:10`), and no acceptance check tests these cases.
- Deviation class: spec gap.
- Raised by: reviewer-1 and reviewer-3. The `İstanbul` and normalization parts come from the invariant probe, no reviewer.

<!-- Source: Base modified (Variant 3 M5) per Change #6; Variant 1 M4 merged per Change #6; invariant probe INV-006 per Change #6; assumption A-002 -->
**M3. Several error cases have no defined behaviour.**
- An omitted FILE argument (`wordcount-spec.md:8`, `wordcount-spec.md:25`). Whether "FILE missing" covers it is open (A-002). A default argparse parser would likely exit 2 (`variant-1-original.md:30`), but with its own usage message, not the spec's.
- Error precedence when FILE is unreadable and `--top` is invalid at the same time (`wordcount-spec.md:25-27`). Both exit 2; the messages differ.
- FILE is a directory (`IsADirectoryError`, INV-006).
- Why nothing named rests on it: no acceptance check tests these cases. The plan copies `wordcount-spec.md:25` at `wordcount-plan.md:26`, so the gap is inherited (A-002: MEDIUM either way).
- Deviation class: spec gap.
- Raised by: reviewer-1 and reviewer-3. The directory case comes from the invariant probe, no reviewer.

<!-- Source: invariant probe per Change #7 (INV-003, INV-004) -->
**M4. `--top` parsing has untested paths and loose edges.**
- argparse with `type=int` prints its own message for `--top abc` and for `--top` with no value ("expected one argument"). The exit code 2 matches `wordcount-spec.md:27`; the message does not.
- argparse accepts `--top -1`.
- `int()` accepts `3_0`, `+3`, ` 3` and `03`, so "positive integer" (`wordcount-spec.md:9`) does not settle these.
- `--top` given twice keeps the last value.
- One test per acceptance line (`wordcount-plan.md:32`) can leave these paths untested, even though `wordcount-plan.md:28` copies the rule.
- Evidence: `wordcount-spec.md:9`, `wordcount-spec.md:27`, `wordcount-plan.md:28`, `wordcount-plan.md:32`; INV-003, INV-004.
- Why it is Medium: the plan copies the spec's rule, and no named check uses these inputs. The probe graded both items MEDIUM.
- Deviation class: spec gap plus test thinness.
- Raised by: invariant probe, no reviewer.

<!-- Source: Base original (Variant 3 M2) per Change #8; evidence E3 -->
**M5. The test command does not say where to run it, and from the repository root it skips the plan's tests.**
- Claim: `wordcount-plan.md:32` gives `uv run pytest` with no path or folder. `pyproject.toml:107-108` sets `testpaths = ["tests"]`. E3: run from the repository root, pytest collects `tests/` and not `code/test_wordcount.py`. That run could pass without testing the plan.
- Why it is Medium: `wordcount-plan.md:4` names `code/` as the home of every target. Run from there, the command collects the plan's tests (E3; E1 collected 2 items). A worker who follows the plan's stated location gets a working run.
- Fix: write the test file into the command, `uv run pytest <abs>/code/test_wordcount.py`.
- Deviation class: plan-internal defect.
- Raised by: reviewer-3 only.

<!-- Source: invariant probe per Change #9 (INV-002); orchestrator adjudication in debate-transcript.md -->
**M6. The plan does not say that ties are sorted before the top-N cut.**
- Claim: `wordcount-plan.md:14-15` say `top_words` returns up to n pairs and orders ties, but not that the sort happens before the cut. On `zed sat the the the cat cat and` with N=3, cut-then-sort prints `the, cat, zed`, and sort-then-cut prints `the, cat, and`. On the spec example both print `the, cat, and`, so the example tests (`wordcount-plan.md:21`, `wordcount-plan.md:33`) cannot tell them apart.
- Why it is Medium: the spec's normative lines (`wordcount-spec.md:4`, `wordcount-spec.md:17`, `wordcount-spec.md:22`) state an ordering, not a rule at the cut. Only the note at `wordcount-spec.md:38` implies it. The gap starts in the spec (A-003). Closest call.
- Dissent: the reviewer-3 advocate graded it BLOCKING (Decision). If the spec owner treats `wordcount-spec.md:38` as normative, it blocks T2 (`wordcount-plan.md:14-15`) and its T5 test (`wordcount-plan.md:32`).
- Fix: in both documents, write "the top n of the fully sorted list", and add a test with a tie at the cut.
- Deviation class: spec gap.
- Raised by: invariant probe, no reviewer.

<!-- Source: invariant probe per Change #10 (INV-001); orchestrator adjudication in debate-transcript.md -->
**M7. The plan drops two spec qualifiers, so the planned tests can lose precision.**
- `wordcount-spec.md:17` says "One line per word on stdout". `wordcount-plan.md:20` says only "prints". A T5 test written from that line need not assert the stream.
- `wordcount-spec.md:28` says "Empty file (no words)". `wordcount-plan.md:22` says only "an empty file", so a file with only punctuation is not named.
- Why it is Medium: other plan lines already pin the behaviour. `wordcount-plan.md:26-28` name stderr for errors, so "prints" means stdout by contrast. `wordcount-plan.md:16` and `wordcount-plan.md:22` together give the spec's result for a punctuation-only file. Only test precision is lost.
- Grade split (advocates, targeted round): stdout: reviewer-1 MEDIUM, reviewer-2 MEDIUM, reviewer-3 NOTE. No words: reviewer-1 BLOCKING, reviewer-2 MEDIUM, reviewer-3 NOTE. Merged: MEDIUM for both.
- Deviation class: Drift (wording).
- Raised by: invariant probe, no reviewer.

<!-- Source: Variant 2 merged per Change #11 (Variant 2 M1 and its Round 2 rebuttal) -->
**M8. Review-pipeline follow-up, not counted in the plan verdict: the coverage matrix misses spec lines and mis-marks the tie rule.**
- Claim: the matrix (`reflect-out/artifacts/coverage-matrix.json`) has no rows for `wordcount-spec.md:7-8` (the invocation and FILE contract) or `wordcount-spec.md:32-38` (the example invocation and output). Its word-overlap matcher marked INF-009, the tie rule at `wordcount-spec.md:22`, as matched at a score of 0.7 (`coverage-matrix.json:68-75`), despite B3. INF-001 (`wordcount-spec.md:4`) was unmatched (`coverage-matrix.json:4-11`); that was the signal for B2.
- Why it is Medium and outside the verdict: the matrix belongs to the review, not the plan, so it is not a plan finding. Fixing it would change the matrix's own result and what a coverage-gated review can catch.
- Deviation class: not a deviation (review tooling).
- Raised by: reviewer-2 only.

### 4b. Reviewer-1 card Medium section (verbatim)

**M1. The placeholder `FILE` in the stderr messages is ambiguous.**
- The spec writes `wordcount: cannot read FILE` and `wordcount: FILE is not valid UTF-8` (`wordcount-spec.md:25`, `wordcount-spec.md:26`). The plan copies them verbatim (`wordcount-plan.md:26`, `wordcount-plan.md:27`). Neither says whether `FILE` is the literal word or the path argument.
- This is a real contract gap, and T5 asserts these strings (`wordcount-plan.md:32`).
- Nothing named depends on it. The same plan produces both the code and the tests, so it is likely to read the text the same way twice. Correcting it would clarify the wording and would not change any decision.

**M2. No `wordcount` command is created.**
- The spec describes a tool invoked as `wordcount FILE [--top N]` (`wordcount-spec.md:4`, `wordcount-spec.md:7`). The plan's only entry point is `code/main.py` (`wordcount-plan.md:19`, `wordcount-plan.md:25`). No task adds a script, console entry point or packaging.
- T3's acceptance line uses the name `wordcount` (`wordcount-plan.md:20`), but T3's target is `code/main.py` (`wordcount-plan.md:19`). The tests can reach the behaviour through `main.py` (`wordcount-plan.md:32`).
- I rate this Medium because the spec never specifies packaging. The behaviour is covered, and only the invocable name is unfulfilled.

**M3. Word and ordering rules are under-specified, and the plan drops one qualifier.**
- "Letters" is not defined as ASCII or Unicode (`wordcount-spec.md:12`). Underscore handling is not stated. A regex such as `\w+` would include `_`, which the spec's wording excludes. Curly apostrophes are also unaddressed.
- "Lowercase" does not say `lower()` or `casefold()` (`wordcount-spec.md:13`). For example, `ß` becomes `ss` under `casefold()`, which would change the printed words.
- The spec says ties are in "plain codepoint order of the lowercase word" (`wordcount-spec.md:22`). The plan says only "alphabetically by the lowercase word" (`wordcount-plan.md:15`). A locale-aware sort would be a plausible but wrong reading.
- These could cause wrong output on non-ASCII or underscore input. The spec example and the plan's acceptance lines use only ASCII letters (`wordcount-spec.md:31`, `wordcount-plan.md:10`), so no named acceptance check rests on them.

**M4. Two error cases are not covered.**
- FILE is required (`wordcount-spec.md:8`). Neither the spec's error section (`wordcount-spec.md:24-28`) nor the plan's T4 (`wordcount-plan.md:24-28`) says what happens when it is missing.
- No error precedence is given when FILE is unreadable and `--top` is invalid at the same time. The messages differ and both exit 2.
- A default argument parser would likely exit 2 for the missing FILE, which matches the spec's other error codes. The only visible effect of the precedence gap is which message appears first. No acceptance check depends on either case.

### 4c. Reviewer-2 card Medium section (verbatim)

**M1 — Requirement-bearing spans are missing from the coverage matrix**

- **Claim:** The matrix lists neither the invocation and required UTF-8 file contract at `wordcount-spec.md:7-8` nor the example invocation and expected-output span at `wordcount-spec.md:32-38`. Its example row references only the input text at line 31.
- **Evidence:** `wordcount-spec.md:7-8,31-38`; `wordcount-plan.md:20-21,26-27,33`.
- **Why nothing named rests on it:** The plan already contains the invocation, file-error handling, exact example output, and example test. Adding these matrix entries would correct the coverage inventory without changing those tasks or acceptance checks.

### 4d. Reviewer-3 card Medium section (verbatim)

**M1. The tasks have no stated order or dependencies, and two of them edit the same file.**
- Claim: T3 and T4 both target `code/main.py` (`wordcount-plan.md:19`, `wordcount-plan.md:25`). T3 uses T1's and T2's functions, and T5 depends on all of them, but no dependency is written down. Argument handling is also split: T3 owns the default of 10 (`wordcount-plan.md:20`) and T4 owns `--top` validation (`wordcount-plan.md:28`), so both edit the same parsing code. Run in parallel, T3 and T4 would conflict.
- Why nothing named rests on it: the listed order T1 to T5 is already a workable sequence, and running the tasks one at a time works.
- Fix: say "T3 needs T1 and T2; T4 runs after T3; T5 runs last", or merge T3 and T4.

**M2. The test command does not say where to run it, and from the repository root it skips these tests.**
- Claim: `wordcount-plan.md:32` gives `uv run pytest` with no path or working folder. The repository's `pyproject.toml:108` sets `testpaths = ["tests"]`. Run from the repository root, pytest runs the repo's own `tests/` suite and never picks up `code/test_wordcount.py`. That run could pass while not testing this plan at all.
- Why nothing named rests on it: any reasonable worker would add the file path. The plan's decisions stay the same; only the command changes.
- Fix: write `uv run pytest <abs>/code/test_wordcount.py`.

**M3. The plan drops the spec's "plain codepoint order" from the tie rule.**
- Claim: the spec orders tied words by "plain codepoint order of the lowercase word" (`wordcount-spec.md:22`). The plan says only "alphabetically by the lowercase word" (`wordcount-plan.md:15`). A worker could sort by locale (`locale.strxfrm`) instead, which gives a different order for non-English letters. A T5 test built only from the plan would not catch that.
- Why nothing named rests on it: Python's default `sorted` already sorts by codepoint, and the spec example uses only English letters.

**M4. It is unclear whether `FILE` in the error messages is the literal word or the file's path (verified from T1 observation 1).**
- Claim: `wordcount-spec.md:25-26` puts `FILE` inside the quoted error text. The same word is also a placeholder in `wordcount-spec.md:7-8`. The plan copies the text word for word (`wordcount-plan.md:26-27`). A test written for one reading fails against the other.
- Why nothing named rests on it: the plan matches the spec, and because T4 and T5 come from the same plan they will agree with each other. Only the spec's author can decide which reading is meant.

**M5. Several input cases have no defined behaviour (verified from T1 observations 2, 3 and 4).**
- Running with no FILE argument has no defined message (`wordcount-spec.md:8,25`).
- "letters" is not defined as English-only or any Unicode letter, even though the input is UTF-8 (`wordcount-spec.md:8,12`).
- Lowercasing could mean Python's `lower()` or `casefold()` (`wordcount-spec.md:13`).
- The spec does not say whether the curly apostrophe counts as an apostrophe (`wordcount-spec.md:12,14`).
- When the file is unreadable and `--top` is also invalid, the spec does not say which error wins (`wordcount-spec.md:25-27`).
- On underscores: a word is only letters, digits or apostrophes, so underscores split words. A tokenizer built on the regex `\w` would break that rule.
- Why nothing named rests on these: no acceptance check in the plan tests any of these cases.


## 5. Anything that looked wrong with the new rule
1. **A Medium that names a consequence the run elsewhere treats as blocking (B3 vs M6).** B3 (blocking, consequence "Decision"): "a locale-aware sort passes the plan's check and breaks the spec" because `wordcount-plan.md:15` "is itself an acceptance check". M6 (Medium): "On `zed sat the the the cat cat and` with N=3, cut-then-sort prints `the, cat, zed`, and sort-then-cut prints `the, cat, and`. On the spec example both print `the, cat, and`, so the example tests ... cannot tell them apart." The verdict line itself says: "Fixing B1 to B3 alone does not make the plan spec-conformant: M6 (the top-N tie cut) and M7 (the dropped qualifiers) still let wrong programs pass the planned checks." So the merged card says a Medium lets a wrong program pass the planned checks, which is the B3 consequence. Dissent recorded in the card: "the reviewer-3 advocate graded it BLOCKING (Decision)". The merge calls M6 the "Closest call". I did not decide which grade is right (UNVERIFIED either way).
2. **The Decision test, read literally, covers almost any fix.** B3's stated reason is that correcting `wordcount-plan.md:15` "changes that check". The same is true of M7 (`wordcount-plan.md:20` "prints" vs spec "on stdout") and M5 (`wordcount-plan.md:32` test command), which were graded Medium. The line between B3 and M5/M7 rests on the reviewers' judgement of how likely a wrong program is, not on the rule's wording. UNVERIFIED whether the owner wants that.
3. **Same defect, different grade per reviewer.** Tie order: reviewer-1 Medium, reviewer-2 Blocking ("Consequence test used: Missing"), reviewer-3 Medium. `wordcount` command: reviewer-1 Medium ("I rate this Medium because the spec never specifies packaging"), reviewer-3 Blocking ("Consequence test: Missing"), reviewer-2 none (said the plan "already contains the invocation"). Final grades came from the adversarial merge, after it re-graded reviewer-2's "Missing" to "Decision". Reviewer-1 returned PASS with 0 blocking while the merge found 3.
4. **A label used beside the grade.** Reviewer-2's card has a Deviations table whose row 1 reads "| 1 | Drift | `wordcount-plan.md:15` | ... | MEDIUM |" while the same card's `## Blocking findings` B1 is the same defect and its verdict is FAIL. The reflect-reviewer agent's output format has a Severity column (HIGH/MEDIUM/LOW), so a label sits next to the grade. The merge recorded it as a Note: "reviewer-2's deviations table contradicted its body".
5. **The new rule is not in the reflect skill or its reviewer agent.** `grep -c "follow-up candidates|consequence"` gives 0 matches in `/home/coder/.claude/agents/reflect-reviewer.md`; the skill folder `/home/coder/.claude/skills/sc-reflect-protocol` has 1 match, in refs/deviation-taxonomy.md (not checked what it says). `Medium`/"follow-up candidates" do not appear in SKILL.md output sections (I read it in full). The reviewers graded by the consequence test only because I copied the rule from the session output style into each reviewer prompt. A run without that paste would use the agent's own HIGH/MEDIUM/LOW severity and the 4-class deviation table. UNVERIFIED whether another install carries the rule elsewhere.
6. **Extra labels outside the rule.** The merged card tags each finding "Deviation class: Drift | spec gap | plan-internal defect | not a deviation" and names a class "spec gap (inherited)". "spec gap" and "plan-internal defect" are not in the four-class taxonomy of SKILL.md section 10, and a UC-1 (pre) run does not use deviation classes at all.
7. **A blocker with no named consequence:** none found. Every blocking entry names Decision or Missing and an affected action. B2 is labelled "Missing (and Decision)" (two tests at once).
8. **The Medium list holds an item about the review tooling, not the plan (M8).** It is marked "not counted in the plan verdict" but still sits in the follow-up list the owner would be asked about.
9. B1 is a defect I did not plant (the plan names a module `tokenize.py`); I reproduced the TypeError myself. B2, B3 and the open choices in M1 to M7 are likewise defects of my plain, honest drafting of the spec and plan, not planted.

## 6. Steps that failed, were skipped, simplified or refused
- Refusal by hook, exact message: `PreToolUse:Bash hook error: [~/.claude/hooks/block-bare-python.sh]: UV-ONLY BLOCK: this command runs bare `python3`. Use `uv run python ...` (or `uv pip ...` / `uvx ...`) instead, or `jq` to parse JSON.` I re-ran the same step with jq. Nothing else was refused.
- I created and removed an empty directory `B_dummy` in the worktree root in one command by mistake (mkdir then rmdir in the same call); nothing remains. A temporary folder /tmp/tokshadow_B was created for the B1 check and deleted.
- Wave 1B/1C: no requirements-analyst or root-cause-analyst agent was spawned; I wrote the T1 card inline ("hypothesis_source: inline-fallback" in t1-card.md). It was blind-calibrated (C = 0.64).
- Wave 0 step 0.3: adversarial skill presence checked by its being in the skill list, not by a `--help` probe call. Step 0.7: memory files not read (the one existing file is untracked in git status).
- Wave 5 memory persist, `.dev/reflect/runs.jsonl` append and `metrics.json` (section 15.1): not written; the first two are outside my folder, metrics.json I omitted. return-contract.yaml records `memory_persist: skipped-by-task-brief`.
- Calibrator class: all three classes were used by reviewers, so `calibrator_diversity: degraded` (opus used). Executor class unknown (nothing executed). `t2_vendor_diversity: single`.
- Wave 4 (adversarial merge) was run by one debate-orchestrator agent. Its own report: position-bias dual pass done in one context, not by two independent evaluators; one targeted extra debate round added to clear the invariant gate (INV-001, INV-002 were unaddressed HIGH-class at probe time); advocates ran on the session default model, not the reviewers' model classes; S-001 (card layout) stayed unresolved. Its contract status is partial.
- EV-1: the adversarial run wrote `merged-verdict-card.md`, not `<output>/adversarial/merged-verdict.yaml`. I wrote that yaml from its return contract (values copied; header comment says so).
- Evidence validator: 0 dropped (the protocol calls a zero-drop pass suspect); it counted "about 150 instances, about 60 distinct locations by hand", so citations_total is approximate; 6 caveats are in REPORT.md.
- Wave 6 (remediation) not offered (no --remediate). Wave 7 not applicable (UC-1). `--t2-engine` stayed legacy; the panel was never called.
- Reviewer-2 (requested haiku) self-reported GPT-5.2; model identity of that reviewer is UNVERIFIED.
- Follow-up-issue question: answered NO by the brief; no issue created, no gh call made.

## 7. Correction added after the owner asked "verify which model actually ran" (2026-11-17T06:32Z)
Method: for each subagent transcript in /tmp/claude-1000/-home-coder-workspaces-worktrees-IronClaude-brainstorm-reflect-panel/0f1875dd-6930-45b1-abe9-2b9c6f0a8d41/tasks/ I read the `message.model` field of every `assistant` line (the model that answered) and, for reviewer-2, the `requestedModel` field. Result:
- reviewer-1 (requested sonnet): answered by claude-sonnet-5-5 (the only model on its assistant lines; alias claude-gw-tier1b).
- reviewer-2 (requested haiku, alias claude-gw-tier2[1m]): answered by **gpt-6.1-sol** on all 7 assistant lines; `requestedModel` was claude-gw-tier2[1m]. The card's own self-report "GPT-5.2" is wrong about the version: the transcript says gpt-6.1-sol. So reviewer-2 was a non-Anthropic model.
- reviewer-3 (requested opus): claude-opus-5-5 (20 of 20 lines).
- T1 calibrator, the 3 card calibrators, the adversarial orchestrator and the other agent transcripts in that folder: claude-opus-5-5 only. Evidence validator: claude-sonnet-5-5.
- Not verified: my own session model (I am told claude-gw-tier1b[1m]; no transcript was read for it) and which model sits behind the gateway alias in any other run.
Effects on this record: (a) section 1 "mismatch" is confirmed and sharper (actual gpt-6.1-sol, self-reported GPT-5.2). (b) The contract field `t2_vendor_diversity: single` was wrong; it should be `multi` (one reviewer was a different vendor); I corrected reflect-out/return-contract.yaml, not the audit.log row (audit.log is append-only history and still says single, warn row at Wave 0). (c) The haiku class mapped to a GPT model, so reviewer-2's findings (the only reviewer to grade the tie order as blocking) came from a different vendor than the other two reviewers; this was not planned by the run and is not what the reviewer-spec rotation table describes. (d) Blind calibration was Anthropic opus for every card, so the calibrator was not disjoint in vendor from reviewers 1 and 3.

## 8. Follow-up asked by the owner: adversarial debate on whether M6 should be BLOCKING (2026-11-17T06:52Z)
Run by one debate-orchestrator agent (opus) through `Skill sc:adversarial-protocol`, Mode B, two advocates (opus "argue BLOCKING", sonnet "argue MEDIUM"), depth standard, source $PWD/m6-adjudication/m6-source.md (rule text, M6 and B3 verbatim). Output: $PWD/m6-adjudication/out/m6-adjudication-merged.md and $PWD/m6-adjudication/out/adversarial/ (variants, diff-analysis, debate-transcript, invariant-probe, base-selection, refactor-plan, merge-log, return-contract.yaml). Duration about 19.6 min (harness 1,177,788 ms); 263,473 subagent tokens.
Result as reported by the agent (I have not re-run its checks; the "2240 of 3360 reorderings" figure is UNVERIFIED by me):
- M6 final grade: BLOCKING (Decision), conditional: it drops to MEDIUM if the spec owner rules that a word's position in the file may decide a tie at the cut.
- B3 and M6 consistent after that; M7 "on stdout" MEDIUM; M7 "(no words)" unresolved (R-001: one advocate BLOCKING, one MEDIUM, both reject NOTE).
- Convergence 0.93 (14 of 15 points), status CONVERGED in its report, contract status partial; the advocate assigned MEDIUM moved to BLOCKING in Round 2; one extra round was added to clear the invariant gate.
- Simplified per the agent: diff analysis and scoring done by the orchestrator, both position-bias passes in one context, no library-doc check.
This does not change the verdict of the main run (FAIL). It changes the count if the owner accepts it: 4 blocking, 7 Medium. Section 5 item 1 above is answered by this debate; the owner has not ruled on the condition.

## 9. Owner ruling on the M6 condition (given in chat, 2026-11-17)
Owner said: "No, a words position in a file can't be the sole decision of a tie breaker."
Recorded effect: the condition in section 8 resolves against the MEDIUM side. M6 is BLOCKING (Decision) per the debate result. Counts on that basis: 4 blocking (B1, B2, B3, M6), 7 Medium. Verdict stays FAIL. The M7 "(no words)" point (R-001) is still unruled. The merged card and REPORT.md were not edited; they still show the earlier grade (3 blocking, 8 Medium).

## 10. Owner ruling on M7 "(no words)" (given in chat, 2026-11-17)
Owner said: "M7 - Blocking". Taken as covering the "(no words)" part (the open point R-001); the "on stdout" part stays MEDIUM, since the debate settled it and the owner did not change it (my reading, UNVERIFIED with the owner).
Counts on that basis: 5 blocking (B1, B2, B3, M6, M7 "(no words)"), 6 Medium (M1-M5, M8; M7 "on stdout" is part of a split item, so the Medium list is M1-M5, M7-stdout, M8). Verdict stays FAIL. REPORT.md and the merged card are unchanged and still show 3 blocking, 8 Medium.

## 11. Owner confirmation on M7 (given in chat, 2026-11-17)
Owner said: "Only half m7, not stdout". Confirmed: only "(no words)" is BLOCKING; "on stdout" stays MEDIUM. Section 10 reading is correct. Final counts: 5 blocking (B1, B2, B3, M6, M7 no-words), 7 Medium (M1-M5, M7 on-stdout, M8). Verdict FAIL. (Section 10's "6 Medium" is a miscount; 7 is right.)

## 12. Re-check after the owner said "workspace updated" (2026-11-18T16:12Z)
Re-read live files. Section 5 item 5 ("the rule is not in the reflect reviewer agent") is now OUT OF DATE, not wrong for the run: my run used the agent as it was on 2026-11-17 (0 matches then).
- /home/coder/.claude/agents/reflect-reviewer.md (modified 2026-11-18 06:21; same size, 17,536 bytes, as src/superclaude/agents/reflect-reviewer.md) now has a "## Review severity rule" section: blocking by Decision/Missing/Safety, Medium and Note defined, and the Deviations table Severity column (HIGH/MEDIUM/LOW) declared "a label, not the grade", with each row starting `Blocking (Decision):`, `Medium:` or `Note:`. This addresses my section 5 items 4 and 5 for the agent. Commits on this branch: 36ef53a70 "the reflect reviewer carries the review severity rule", 2d2f959a6, 7acce05f7 (stage 3b).
- Still not found: the skill file /home/coder/.claude/skills/sc-reflect-protocol/SKILL.md has no "follow-up candidates" or Medium output section (grep: 0 matches for "follow-up candidates|consequence test"; the only "Medium" hits are the old Severity table). So the skill's merge and REPORT steps would still not list Medium findings unless the orchestrator is told to. Section 5 item 6 (extra labels "spec gap", "plan-internal defect") not re-checked.
- Not re-run: no new reflect run was made, so whether the updated agent grades M6/B3 consistently is UNVERIFIED.
