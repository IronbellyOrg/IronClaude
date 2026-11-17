# QA Report — Fix Cycle 1 Verification (operational and gate semantics)

**Topic:** review-panel run 2 task file, A.10.5 fix cycle 1
**Date:** 2026-11-14
**Phase:** fix-cycle (task-qualitative lens: fix-verification, operational and gate semantics)
**Fix cycle:** 1
**fix_authorization:** false (no file other than this report was edited)
**Drift baseline:** the consolidated findings' "Required fix" text is the baseline for this lens (BUILD-REQUEST GOAL not re-quoted), so AX-1 was applied against it and `drift-axis-inactive` is not claimed.
**Forbidden paths:** the run-1 task folder and the RUN2-QUEUED note were not opened, listed or searched.

---

## 1. O-1 (R1 versus /tmp scratch): RESOLVED

Evidence read: task file lines 171, 175, 183, 185, 199, 203, 205 in full or by ASSIGNMENT tail (Read and `grep -o` on the line), plus a `(R1)` census.

- R1 now exists in exactly 24 items (lines 171-205 odd, 209-219 odd; `grep -o '(R1)' | wc -l` = 24) and reads: "READ-ONLY in the repository, with two permitted kinds of writes ... Never check out, switch, pull, fetch, stash, commit, push, create a branch or write in the real repository. Exactly two kinds of writes are allowed: (1) your one output file in the task folder, and (2) scratch files under the one directory `/tmp/review-panel-run2-<item number>/` that your ASSIGNMENT names ... delete that directory before you return, and nothing is ever committed in the real repository. An assignment that names no scratch directory allows no scratch writes."
- Old wording is gone: Grep for `anywhere except|except your one output file|ONE explicit exception|review-panel-ref-test|overrides R1` = 0 matches.
- Each item that needs scratch names its own directory in its ASSIGNMENT, so a literal reader of R1 can still do the work:

| Item | Quoted ASSIGNMENT text | Literal R1 reader can complete it |
|---|---|---|
| 2.03 (l.175) | "use the scratch directory `/tmp/review-panel-run2-2.03/` for fixtures and delete it afterwards" | yes; D-1, D-2, D-11 reproductions run there |
| 2.07 (l.183) | "a script that needs scratch output may use the scratch directory `/tmp/review-panel-run2-2.07/`, deleted afterwards" | yes |
| 2.08 (l.185) | "use the scratch directory `/tmp/review-panel-run2-2.08/` if a scratch file is unavoidable and delete it afterwards" | yes |
| 2.15 (l.199) | "using the scratch directory `/tmp/review-panel-run2-2.15/` for fixtures and deleting it afterwards" | yes |
| 2.17 (l.203) | "use the scratch directory `/tmp/review-panel-run2-2.17/` for fixtures and delete it afterwards" | yes |
| 2.18 (l.205) | scratch directory `/tmp/review-panel-run2-2.18/`; `mkdir`, then `mktemp -d /tmp/review-panel-run2-2.18/ref-test.XXXXXXXX`, `git init`, `git -c user.name=t -c user.email=t@t commit --allow-empty -m init`, branch tests in two scratch repos, `rm -r /tmp/review-panel-run2-2.18` | yes; both scratch repos sit under the one named directory |

- 2.18 contradiction check: the item says "This is the ONE item whose scratch writes (the second permitted kind of write in rule R1) additionally include scratch git repositories ... R1's bans on commit, branch creation, checkout and every other write stay in force for the real repository and everywhere else". R1's commit and branch bans are scoped to "the real repository", and scratch writes are allowed under the named directory, so there is no contradiction. The closing clause "outside your output file and `/tmp/review-panel-run2-2.18/`" matches R1. The old "overrides R1" language is gone.
- Deletion versus paste: R1 deletes only the `/tmp` directory; evidence goes into the output file in the task folder (2.03 Ensuring: "reproduction commands and their output are quoted"; 2.18 Ensuring: the literal `cannot lock ref` output "is pasted into the research file, and the scratch directories were deleted"). Compatible.
- Other R1-like text outside Phase 2 (lines 228-326 and the Gate items) says "write only your output file" or "read-only"; none requires a scratch write, so no remaining conflict.

Notes (minor, not blocking, no fix cycle):
- 2.06 (l.181) tells the agent to run `uv run pytest tests/cli/reflect -p no:cacheprovider -q`. pytest `tmp_path` and Python bytecode write under `/tmp/pytest-of-*` and `__pycache__`, outside "exactly two kinds of writes". R1 itself says "pytest only ... when your assignment says so", so the intent is clear; the old R1 had the same property.
- 2.18 uses `mkdir /tmp/review-panel-run2-2.18` (fails with "File exists" on a retry after a partial run; `mkdir -p` is safer) and says `git init` / `git commit` "there" without `git -C <dir>`. A cwd mistake would run a commit in the real repository. Worth one clause; not blocking because R1 and the item both forbid it.

axis: none (all five axes applied; no axis-attributable defect). Result: O-1 RESOLVED in substance.

## 2. O-2 (ripgrep pattern): RESOLVED (one minor note)

Patterns I ran with the Grep tool on the task file (the executor's tool):

| Pattern | Result |
|---|---|
| `\[PENDING-ADJUDICATION` | normal result: 20 matching lines (count mode), no regex error |
| `\[PENDING-ADJUDICATION:` | normal result: 16 |
| `\[CONTRADICTION` | normal result: 3 matches (lines 448, 512, 604) |
| `\[PENDING-ADJUDICATION` on the (empty) `synthesis/` folder | `No matches found` (this is the "must return nothing" case of item 5.50: a clean empty result, distinguishable from an error) |
| `[PENDING-ADJUDICATION` (the old pattern) | `rg: regex parse error ... invalid character class range, the start must be <= the end` (reproduces the original defect) |

Sites verified in the task file (all six items named by O-2): 5.11 (l.336, pattern `\[PENDING-ADJUDICATION:`), 5.50 (l.439, two sites: agent prompt and executor check), 6.01 (l.448), 6.03 (l.454), 6.16 (l.482), 6.68 check 19 (l.604, also `\[CONTRADICTION`). Each carries "a Grep that errors is NOT a pass: rerun it until it returns a normal result or an empty result without an error message" (6 lines, 7 sites). A scan for other tag-shaped unescaped Grep patterns (`[UNVERIFIED]`, `[CODE-...]`, `[STALE DOC]`, `[HALT...]`) found none used as a Grep pattern (only prose mentions). The placeholder pattern `T[O]DO|T[B]D|FIX[M]E|PLACEHOLDER` is valid ripgrep and untouched.

End-to-end simulation: 5.11 counts markers per synthesis file with the escaped pattern (normal result); 5.50 fold agent and the executor re-check both use the escaped pattern, an empty result means pass, an error means rerun or log; 6.01 assembly self-check, 6.03/6.16 lens checklist c and 6.68 check 19 use the same escaped pattern. Because the escaped pattern is given literally in every site, an executor that copies it gets a normal result on the first run.

Loop bound: the "rerun it until" wording has no retry count. It cannot loop forever in practice because every one of the six items ends with the item-level exit "If unable to complete, log the specific blocker using the templated format in the ### Phase N Findings section ... then mark this item complete" (checked on lines 336, 439, 448, 454, 482, 604), and an error is not read as a pass. For the three sites inside verbatim QA-agent prompts (6.03, 6.16, 6.68) the exit sits in the executor part of the item, not in the agent prompt, so a QA agent facing a persistent tool outage has no stated stop other than its own turn limit.

Minor note (no fix cycle): add "at most 3 times, then report the Grep as FAILED in your findings" to the sentence. axis: none. Result: O-2 RESOLVED.

## 3. G-1 (false claim returns): finding closed in its main scenario, but the fix introduces a new blocking defect (N-1 below)

Items read in full: 6.54 (l.570), 6.55-6.57 (l.572-576, heads and tails), 6.58 (l.580), 6.59 (l.582), 6.60 (l.584), 6.61 (l.586), 6.62 (l.588), 6.63 (l.592), 6.64 (l.594), 6.67 (l.600); Gate 3/4 fix items 6.30 (l.512) and 6.45 (l.548) for the fix-log format.

Walk-through of the concrete scenario (Gate 4 removes false claim C; C still sits in research file R):
1. Gate 4 fix agent (6.45) removes C and logs it in `qa/qa-fidelity-fix-log-c1.md` (name verified at l.548; Gate 3 uses `qa/qa-fix-log.md`, l.512; c2 names at l.524 and l.560; consolidated names at l.510, 522, 546, 558, all match the names used in 6.54-6.57).
2. Gate 5 agent (all four prompts carry the `EARLIER-GATE REMOVALS` block, counted 4) reads those logs and consolidated findings. C is a source finding absent from the report. The agent may classify it JUSTIFIED-REMOVED only with the fix-log entry AND the code evidence; otherwise OMITTED.
3. 6.58 consolidation: JUSTIFIED-REMOVED check opens each cited entry and evidence; an entry without code evidence becomes an omission row (blocking if CRITICAL or IMPORTANT).
4. 6.59 / 6.64 fix agent: third disposition JUSTIFIED-REMOVED; "you MUST NOT re-add such a claim unless your own code evidence ... shows the evidence in that log is wrong"; every recovered claim is code-checked and the fix log carries `code-checked:`.
5. 6.60/6.61 (and 6.65/6.66) verifiers: CODE RECHECK; a recovered claim contradicted by code, or removed-as-false in a log whose evidence still holds, is STILL-OPEN; JUSTIFIED-REMOVED is OK only when entry and evidence exist and hold.
6. 6.62/6.67: `F_1`/`F_2` count it as open, so the cycle does not go green.

Answer to "can C come back with all gates green?": no for a code-fact claim. The fix agent is barred from re-adding it, and both verifiers re-check recovered claims against code. This part of G-1 is resolved.

Gaps found:
- Residual (minor): the Gate 3 and Gate 4 fix-log formats (6.30 "every finding ID, the change (section, one line before and after) and any finding not fixable"; 6.45 "finding ID, change, anything not fixable with the reason") do not require code evidence, yet JUSTIFIED-REMOVED needs "the code evidence that entry quotes". In practice the entry only has a finding ID, and the code evidence lives in the consolidated findings row, which the Gate 5 agents also read, so a sensible agent can follow the ID. As written, a removal whose log entry lacks code evidence is classed OMITTED (the sufficiency report's exact example), which is the safe direction (blocking, then re-check against code) but makes the new disposition rarely usable. One clause in 6.30/6.35/6.45/6.50 ("for every removal record the code evidence file:line") would close it.
- Residual (minor): 6.63 (cycle 2 consolidation, l.592) still lists "Proposed handling RECOVER or JUSTIFY" and was not updated for JUSTIFIED-REMOVED (6.58 and 6.64 were). 6.64 still allows the disposition, so no blocker.
- The gap raised by the sufficiency report's optional extra, "no claim removed in the Gate 3/4 fix logs reappears" in the 6.68 checklist, was deliberately not added; the verifiers' CODE RECHECK covers it for recovered claims.

See N-1 (section 8) for the new blocking defect in the code-recheck rule.

## 4. G-2 (enumeration completeness and load balance): mostly resolved; one new blocking defect (N-2 below)

Trace of Gate 5 from partition to shortfall rule:

| Step | Where | What happens | Check |
|---|---|---|---|
| a. Preconditions | 6.54 (l.570) | reads `qa/gate4-cycle-control.md`; HALT if Gate 4 halted | Gate 5 sits in Step 6.9 after Gate 4, so every input already exists |
| b. Partition | 6.54 | ONE read-only `wc -l` over research 01-24, web-01..04, `gaps-and-questions.md`, synth-01..10, `reviews/adversarial/*/ADJUDICATION-RESULT.md`; per-agent lines and share written to `qa/gate5-partition.md`; moves recorded there | `gaps-and-questions.md` is created at item 3.26 (l.288) in the task folder root, as 6.56 says; the debate results come from Phase 5 (17 lines mention the file name); all inputs exist before 6.54 runs |
| c. Spawn | 6.54-6.57 | four `rf-analyst` agents in ONE message, partition lists consistent (research 01-05/06-11/12-18/19-24; web 01-02/03-04; synth 05-07 / 04,09,10 / 01-03 / 08; debates to agent 1; gaps to agent 3): every research, web and synth file and the debate results are assigned exactly once | 4 agents, below the 20-agent limit |
| d. Enumeration | each prompt | `ENUMERATION FILE` `qa/qa-anti-omission-enumeration-<n>.md` (n=1..4), one numbered list per assigned file, each ending `COUNT <file name>: <n>`; per-file counts copied to the report as `### Per-File Counts` | file names identical in the Output field and the prompt of each item and in 6.58 (grep census: enumeration-1..4 twice each in 6.54-6.57, referenced in 6.58 together with `enumeration-<n>-rerun.md`); `gate5-partition.md` is spelled the same at all 7 sites |
| e. Recount | 6.58 (6) (i) | the consolidating executor picks three assigned files per agent (prefers the three largest by `wc -l`), recounts with read-only Grep or `wc`, writes `AGENT <n> FILE <name> ENUMERATED=<e> RECOUNT=<r>`; `e < 0.9 r`, a missing enumeration file or a missing COUNT line is blocking `P6A-RC-<n>`, counted in F_0, and that agent's partition is re-run in the item with `-rerun` output names | selection independent of the enumerating agent: yes |
| f. Cycle | 6.59-6.62 | see N-2 | |

Can the partition item run before the agents spawn with all inputs present? Yes: the partition check is the first action of 6.54, after the Gate 4 pass check, and the other three items are spawned in the same message as 6.54 (their texts say "in parallel with items 6.54 ...").

Is the 30 percent cap satisfiable? Four agents at no more than 30 percent each have 120 percent of capacity, and the item gives two moves: whole files from heaviest to lightest, and, when a single file alone keeps an agent over 30 percent, the second half of that file by line range. With about 45 inputs (24 research, 4 web, 1 gaps, 10 synth, debate results) no single file is plausibly above 60 percent, so it is satisfiable. If one file were above 60 percent, or the greedy move oscillated, the item has no terminal rule ("until no agent exceeds 30 percent"). Minor note: add "if the cap cannot be met, record the smallest achievable maximum share in `gate5-partition.md` and proceed".

Deviation from the letter of the required fix (c) ("state the line counts per agent in the item"): the fix measures them at execution because the research, synthesis and debate files do not exist at build time. I accept this: the item cannot know them, and the item states the measurement, the 30 percent cap and the logging obligation. Not a finding.

Minor notes on G-2 (not blocking):
- The recount compares an agent's count of distinct findings with a mechanical count of "rows, headings or numbered entries". Rows and headings are not distinct findings (header and separator rows, headings with no claim, one row holding several findings), so `e < 0.9 r` can fire on a correct enumeration, causing an unneeded rerun that consumes cycle budget. Define `r` (data rows plus bullet entries, excluding header and separator rows) and use the same unit in the COUNT line.
- The agent prompts say the list is "subject to the partition check recorded in `qa/gate5-partition.md`" but never tell the agent to read that file; 6.54 says to edit the lists "before they are passed" while every prompt says "pass verbatim". Add "Read `qa/gate5-partition.md` first and use the file list of your agent number" to each prompt so no in-place prompt edit is needed.
- 6.68 check 21 (l.604) counts "Gate 5 (4 anti-omission reports)" and does not mention the four enumeration files or `qa/gate5-partition.md`, so the new artifacts are not verified at final validation.

## 5. O-3 (staging guard), N-13 and the testing-N/A sentence: RESOLVED

O-3 (items at l.621, l.629, l.637, read in full):
- Placement: the nested check is in step 7.2 right after `git add .dev/tasks > /dev/null`, in the Post-Completion verification (l.629) and in the last re-stage item (l.637, run after each of the two `git add` calls). That covers every staging point in the task.
- Command validity: `git diff --cached --name-only | grep -E '(^|/)\.claude/'` is a valid read-only pipeline and valid ERE; `grep` exits 1 on no match, but the item judges the printed output ("MUST print nothing"), not the exit code. The root check `git diff --cached --name-only -- .claude` is kept.
- The guard is needed, not cosmetic: `git check-ignore -v` on a sample file under `<task folder>/.claude/agent-memory/` and `<task folder>/qa/.claude/agent-memory/` returned rc=1, so those nested paths are NOT ignored and `git add .dev/tasks` would stage a memory file written there. The two directories are currently empty (`find ... -path '*/.claude/*' -type f` printed nothing), and nothing is staged now (`git diff --cached --name-only` printed nothing).
- No accidental staging: the remedy is `git restore --staged <path>` (index only, valid for a newly added file), and the items say the empty directories are left in place. The only `git add` is `git add .dev/tasks`; every item forbids `git add` outside `.dev/tasks`.
- No commit or push anywhere: the only `git commit`/`git push` strings after line 220 are the prohibitions at l.621 and l.637 ("ensuring NO `git commit`, `git push`, `git fetch`, `git checkout`, `git stash`"); l.613 says the task "does NOT commit and does NOT push". The `git commit` in item 2.18 runs in a `/tmp` scratch repository (section 1).
- Minor note: the last sentence of 7.2 (l.621) still says "cannot be marked as done until the three checks are recorded" while the same item now records four results. Harmless; fix by saying "four".
- Minor note: `git diff --cached --name-only | grep` inspects the whole index, so a pre-staged tracked `.claude/settings.json` from another session would raise a false HALT. That outcome is conservative.

N-13: item 6.68 check 21 (l.604) reads "Gate 3 (13 lens reports (26 in split mode) plus consolidation)". The split rule exists: l.87 ("two instances each when the report exceeds 3000 lines"), l.450 (instance a/b split) and l.716 (instance b used only above 3000 lines), so 13 x 2 = 26 is consistent. RESOLVED.

Testing-N/A sentence: present at l.74 ("Testing requirements: not applicable (documentation-only research task; the only commands run are read-only recounts)."), inside the OWNER SCOPE CHANGE paragraph. It matches BUILD-REQUEST l.55 ("TESTING_REQUIREMENTS: N/A — documentation-only skill ... Research agents may run read-only recounts with `uv run python` and the reflect and review test suites with `-p no:cacheprovider` only where an item says so"). Minor note: "the only commands run are read-only recounts" ignores the scratch repositories of 2.18 and the staging in Phase 7, and BUILD-REQUEST also allows test-suite runs; the fix log already flags this. Not blocking. RESOLVED.

axis: none for O-3, N-13 and testing-N/A.

## 6. Concurrency check on the changed items

Gate 5 is still four agents in one message (items 6.54-6.57); 6.58 may spawn up to four reruns, one per agent, inside one item (at most four at once even if run in parallel); 6.59, 6.60, 6.61 and 6.64-6.66 spawn one each. No changed item raises concurrency above 20 subagents.

## 7. Weakened criteria and invented content in the changed items

- No criterion was weakened: every R1 prohibition on the real repository is kept; the Gate 5 "NO omission" criterion gained a stricter recount; `F_0`/`F_1` rules, the byte-exact halt strings (not edited) and the 2-cycle cap are intact.
- Invented content: none found. Every new file name (`gate5-partition.md`, `qa-anti-omission-enumeration-<n>.md`, `-rerun` names) is introduced where it is first produced and used consistently.

## 8. New defects introduced by the fix (blocking)

### N-1 (IMPORTANT, blocking, axis: AX-2 Contradictions): the "verify every recovered claim against code" rule cannot be met by non-code claims

Where: 6.59 (l.582) and 6.64 (l.594) fix-agent prompts, 6.60/6.61 and 6.65/6.66 CODE RECHECK, 6.62 (l.588) and 6.67 (l.600) cycle control.

Quoted text:
- 6.59: "every claim you DO recover must be checked by you against that code or E2 tip before you write it ...: a claim you cannot verify against code is tagged [UNVERIFIED] and goes to Open Questions instead".
- 6.60: "for EVERY RECOVERED entry re-verify the recovered claim against the code at HEAD ... or ... `git show` ... Write the line `RECOVERED_VERIFIED_AGAINST_CODE=<k> of <m>`".
- 6.62: "a recovered claim that a verifier reports as not verified against code is counted as open in `F_1`" (6.67 same for `F_2`).

Problem: the Gate 5 inputs include claims that are not statements about code or the E2 tip: web research findings (web-01 to web-04, synth-04 external findings, agents 1 and 2), conflict-log and debate outcomes (agent 1 prompt: "each conflict-log row of synth-06 and each debate result also check that its outcome is in Sections 6.12 and 7"), recommendations and design options (synth-05/07/09/10), and E1 run figures. A dropped finding of that kind is a legitimate blocking omission. Under the new text the fix agent must send it to Open Questions as [UNVERIFIED] instead of the section named in the finding (this contradicts the same prompt's "RECOVER it (add the dropped finding to the report section named in the finding ...)"), and each verifier must report it as not verified against code, which 6.62/6.67 count as open. So such an omission can never reach `F = 0`: it will stay open through both cycles and end in `[HALT-MONOTONICITY]` or the hard cap, with escalation to the user. Where all blocking omissions are of that kind, `F_1 >= F_0` fires at once. A debate outcome dropped from 6.12/7 is the clearest case.

Required fix (one rule, not new items): scope the rule to code-derived claims. In 6.59 and 6.64 say "a recovered claim about code, tests, scripts, configs or the E2 tip is checked against them (`code-checked:`); a recovered claim whose source is web research, a debate outcome, a design option or an E1 artifact is checked against that source (URL, ADJUDICATION-RESULT.md, artifact path:line) and is recorded as `source-checked: <citation>`; a claim that cannot be checked at all is tagged [UNVERIFIED] and ALSO stays in its section". In 6.60/6.61/6.65/6.66 define `m` as the number of recovered claims that are code-derived and let `k of m` count only those; in 6.62/6.67 count as open only a code-derived recovered claim not verified against code.

### N-2 (IMPORTANT, blocking, axis: AX-2 Contradictions): the `P6A-RC-<n>` recount finding has no defined life cycle after the rerun

Where: 6.58 (l.580) (6)(i) versus 6.59 (l.582), 6.60/6.61 (l.584, 586), 6.62 (l.588).

Quoted text:
- 6.58: a recount shortfall "is a blocking finding `P6A-RC-<n>` (Blocking Y, counted in F_0 like every blocking finding, so it counts against the cycle budget), and that agent's whole partition is then re-run in this item ... recording its result next to `P6A-RC-<n>`".
- 6.59 prompt: "rows `P6A-RC-<n>` (recount findings) are handled by the re-run in Item 6.58, not by you".
- 6.59 Ensuring: "every blocking omission ID appears in it as recovered, justified or justified-removed".
- 6.60/6.61: "For EVERY blocking omission decide RECOVERED-OK, JUSTIFIED-OK or STILL-OPEN".

Problem: the same `P6A-RC` row is blocking and counted in `F_0`, is excluded from the fix agent's duty, yet the Ensuring clause requires it in the fix log, and the verifiers have no rule for it (it was neither recovered nor justified; a successful rerun is not one of their three outcomes). A passing rerun does not close the row, so `F_1` can still count it; or the executor cannot mark 6.59 done. If the recount fires on every run (see the recount-noise note in section 4) the gate is blocked by an unfinished rule, not by an omission.

Required fix: in 6.58 state when `P6A-RC-<n>` is closed (rerun recount at least 0.9 r and the rerun report Complete), and write such closed rows into the consolidated file as `CLOSED-BY-RERUN` without counting them in `F_0` after the rerun; in 6.59 Ensuring say "every blocking omission ID except `P6A-RC` rows"; in 6.60/6.61 add "a `P6A-RC` row is RECOVERED-OK when the rerun result recorded next to it meets the rule, otherwise STILL-OPEN"; in 6.63 add JUSTIFIED-REMOVED to Proposed handling.

## Items Reviewed

| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | O-1: R1 allows the scratch writes that 2.03, 2.07, 2.08, 2.15, 2.17, 2.18 need | none | PASS | section 1; each item names its own `/tmp/review-panel-run2-<item>/`; 24 R1 sites; old wording 0 matches |
| 2 | O-1: no remaining contradiction R1 versus 2.18 git scratch repo; deletion versus paste | none | PASS | section 1; l.205 text; scratch repos under the one named directory |
| 3 | O-2: escaped patterns run without regex error (executed `\[PENDING-ADJUDICATION`, `\[CONTRADICTION`) | none | PASS | section 2; old pattern reproduces the rg parse error |
| 4 | O-2: "errors is NOT a pass" cannot loop forever | none | PASS (minor note) | six items each have the item-level blocker exit; no explicit retry count |
| 5 | G-1: Gate 4 removed claim cannot return with gates green (code-fact claim) | none | PASS | section 3 steps 1-6 |
| 6 | G-1: recovery check works for every kind of Gate 5 claim | AX-2 | FAIL | N-1: non-code claims (web, debate outcomes, design options) cannot satisfy the code recheck and count as open |
| 7 | G-1: Gate 3/4 fix logs carry the evidence JUSTIFIED-REMOVED needs | none | PASS (minor note) | fix-log formats at l.512, l.548 have no code-evidence field; consolidated findings are read as well |
| 8 | G-2: partition item runs before spawn with inputs present; names consistent | none | PASS | section 4 steps a-d; l.288 creates the gaps file; names consistent across items |
| 9 | G-2: 30 percent cap satisfiable | none | PASS (minor note) | four agents, two move types; no terminal rule for an extreme file |
| 10 | G-2: recount and shortfall rule lead to a coherent gate | AX-2 | FAIL | N-2: `P6A-RC` rows have no closing rule; Ensuring clause contradicts the fix agent prompt; verifiers have no outcome for them |
| 11 | O-3: guard placement, validity, no `.claude/` staging, no commit or push | none | PASS | section 5; `git check-ignore` rc=1 shows the guard is needed |
| 12 | N-13 and testing-N/A sentence | none | PASS (minor note) | l.604, l.87, l.450, l.716; l.74 versus BUILD-REQUEST l.55 |
| 13 | New-defect scan: weakened criteria, invented content, concurrency above 20 | none | PASS | sections 6 and 7 |
| 14 | New-defect scan: changed text versus untouched text | AX-2 | FAIL | N-1, N-2 (above); minor: l.621 "three checks" and 6.63 handling list |

## Summary
- Checks passed: 11 / 14
- Checks failed: 3 (two distinct blocking findings: N-1, N-2; row 14 repeats them)
- Critical issues: 0
- Blocking (IMPORTANT) issues: 2 (both new, both introduced in the G-1/G-2 fix text)
- Issues fixed in-place: 0 (fix_authorization: false)

Fix status of the seven findings: O-1 RESOLVED, O-2 RESOLVED, O-3 RESOLVED, N-13 RESOLVED, testing-N/A RESOLVED, G-1 resolved for its stated scenario but the fix introduces N-1, G-2 resolved for (a) and (c) but the recount rule introduces N-2 (it is only defined to the point of the rerun).

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| N-1 | IMPORTANT (blocking) | 6.59 l.582, 6.64 l.594, 6.60/6.61 l.584/586, 6.65/6.66, 6.62 l.588, 6.67 l.600 | "every recovered claim is code-checked, else [UNVERIFIED] to Open Questions; not verified against code counts as open" cannot be satisfied by web, debate-outcome, design-option or E1-artifact claims; contradicts "RECOVER ... into the section named" | scope the code check to code-derived claims, give other claims a `source-checked:` citation, define `m` and the open-count accordingly (section 8) |
| N-2 | IMPORTANT (blocking) | 6.58 l.580 (6)(i), 6.59 l.582 prompt and Ensuring, 6.60/6.61 | `P6A-RC-<n>` is blocking and in `F_0`, excluded from the fix agent, required in the fix log, and has no verifier outcome or closing rule after the rerun | define the closing rule and exclude closed rows from the F count; adjust Ensuring and verifier text (section 8) |
| m-1 | MINOR | the six items with the errored-Grep rule | no retry count | "at most 3 times, then report the Grep as FAILED" |
| m-2 | MINOR | 6.30/6.35/6.45/6.50 fix-log format | no code-evidence field, so JUSTIFIED-REMOVED is rarely usable as written | add "record the code evidence file:line for every removal" |
| m-3 | MINOR | 6.63 l.592 | Proposed handling omits JUSTIFIED-REMOVED | add it |
| m-4 | MINOR | 6.54 l.570 | no rule when the 30 percent cap cannot be met; prompts do not tell agents to read `gate5-partition.md`; "pass verbatim" versus editing lists | add the fallback and a "read `qa/gate5-partition.md`" sentence to each prompt |
| m-5 | MINOR | 6.58 recount | `r` (rows/headings) and `e` (distinct findings) differ in unit; false shortfalls | define one unit |
| m-6 | MINOR | 6.68 check 21 | enumeration files and `gate5-partition.md` not verified at final validation | add them |
| m-7 | MINOR | l.621 | "three checks" versus four results | say four |
| m-8 | MINOR | 2.18 l.205; l.74; 2.06 | `mkdir -p`, `git -C`; "only read-only recounts" overstated; pytest/bytecode writes outside R1's two kinds | one-clause tweaks |

## Actions Taken
None (fix_authorization: false). This report is the only file written.

## Inherited Structural Verdict — Reliance Audit (PR-04, INV-019)
The spawn prompt carried no `## Inherited Structural Verdict` block; standalone behaviour applied (independent re-checking). See Self-Audit.

## Self-Audit

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- None. No inherited verdict was supplied; every claim in this report rests on my own reads. I did not rely on the fix log (`qa/qa-qualitative-fix-log-cycle1.md`) for any fact; its claims were each re-checked against the task file.

**(b) Independent semantic checks (≥1 required, INV-019):**
- R1 text census and old-text removal -- Bash `grep -o '(R1)' | wc -l` = 24, Grep for the old phrases = 0 matches; ASSIGNMENT tails of 2.03, 2.07, 2.08, 2.15, 2.17, 2.18 read with `grep -o` and Read (l.175-205).
- Escaped-pattern execution -- Grep tool runs of `\[PENDING-ADJUDICATION`, `\[PENDING-ADJUDICATION:`, `\[CONTRADICTION` (normal results, 20/16/3), the same pattern on `synthesis/` (`No matches found`), and the old pattern (rg parse error reproduced).
- Escape clauses of the six pattern items -- Bash grep for "If unable to complete" on l.336, 439, 448, 454, 482, 604.
- Gate 5 trace from partition to shortfall -- Read of l.568-570, 578-588, 592-600 and head/tail of l.572-576; census of `qa-anti-omission-enumeration-*` and `gate5-partition` names; origin of `gaps-and-questions.md` (l.288).
- Gate 3/4 fix-log formats -- Bash extraction from l.512 and l.548 showed no code-evidence field; file names at l.510-560 match the names used in 6.54-6.57.
- Guard necessity -- `git check-ignore -v` on nested `.claude/agent-memory/x.md` paths returned rc=1 (not ignored); `find -path '*/.claude/*' -type f` empty; `git diff --cached` empty.
- Prohibited-command scan -- Bash grep of `git commit|git push|git restore|git add` after l.220: only prohibitions and the staged-only commands.
- Split-mode count -- l.87, l.450, l.716 versus l.604.
- N-1 and N-2 were found by reading 6.58-6.62 against the agent 1 and 4 prompts; they are not in any earlier report.

Why trust a FAIL with two findings: both are quoted from the file with line numbers and can be re-read in one Read each (l.580-588).

## Confidence
Verified: 13/14 | Unverifiable: 0 | Unchecked: 0 | Confidence: 92.9% (row 14 is a scan, counted verified on the lines read; the 1 of 14 not counted is row 9's extreme-file case, which was reasoned, not executed). Threshold note: the verdict is FAIL, so the 95 percent PASS gate is not needed.
Tool engagement: Read: 9 | Grep: 12 | Glob: 0 | Bash: 14 (read-only `grep`, `sed`, `wc`, `git check-ignore`, `git diff --cached`, `find`). Tavily/web: not used (no external lookup needed).

## Recommendations
- Send N-1 and N-2 to a fix cycle 2 (single fix agent) with the "Required fix" text above; they are edits to the prompts and Ensuring clauses of items 6.58-6.62 and 6.64-6.67, no new items. Minor notes m-1 to m-8 need no cycle.
- After the fix, re-verify only N-1 and N-2.

## QA Complete

VERDICT: FAIL

