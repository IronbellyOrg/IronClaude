# Investigation: why cheap panels miss alias GT1/GT3/GT4 and control GT1

Scope: era "source.md" only. EVAL = `.dev/eval-workspaces/tasklist-review-panel/20261111-a1`.
Cheap panels (ember/luna/haiku only): S01, S03, S04, S05, S07, S10, S13, S24.
Sections are appended as each is finished.

Issue ids: B6 = alias GT1, B8 = alias GT3, I6 = alias GT4, I7 = control GT1 (legend in `COMBO-REPORT.md` lines 412-416).

Important setup fact (affects every "check the repo" move below): reviewers ran with cwd `/tmp/evalsb/repo`, a `git archive` of the eval branch HEAD (`manifest.md` line 10; `tools/run-reviewer.sh` runs `cd /tmp/evalsb/repo && claude -p ...`). That HEAD is AFTER both packages were implemented and merged (#384 commits `4eb75698d`, `943246042`; #438 commit `54e21668f`). So the repo the reviewers could grep already contains `docs/reference/model-aliases.md`, `tests/skills/test_model_alias_policy.py`, the repaired `refs/tiers.md` sentence, and the already-updated `WRITE_VERB_CLASSIFICATION` table. The defects are still detectable, but a plan-vs-repo check sees the "after" state, not the "before" state the plan was written against.

## 1. The four missed items: what they are and where they conflict

### B6 = alias GT1 (contradiction, blocking in implement, cost: extra attempts 3 and 4)

- plan_quote: "Sections: what a primitive may name (plain aliases only; the issue-worker allow-list and why; the test tests/skills/test_model_alias_policy.py enforces it)"
- GT description: Task 6, echoing the Goal's "select models only through the plain aliases", tells the page to state an aliases-only rule that the test enforces, but the plan's own Task 5 makes the retry ladder select by slot variables, sprint returns slot model ids, Auggie takes `--model prism-b`, and the test only rejects full claude ids.
- Location in `candidate.md`: Goal line 15 ("select models only through the plain aliases ... a test with a documented allow-list enforces it"); Task 6 line 99 (the quoted section list). Conflicting plan text: Task 5 line 86 (primary ladder T3Model01/T2Model02/T1Model01 "now replaces the alias fallback ladder"; rung 1 non-Claude, rungs 0 and 2 GPT) and Task 6's own Known-consequences clause on the same line 99 (sprint suggester and slot ids, `src/superclaude/cli/sprint/aienv.py` lines 111-128). The test defined in Task 1 lines 34-37 checks only frontmatter `model:` lines, the `claude-gw-tier` text and `^claude-(opus|sonnet|haiku|fable)-\d` full ids, so it cannot "enforce" an aliases-only rule.
- Repo conflict (reviewer sandbox): `src/superclaude/commands/auggie-review.md`, `src/superclaude/skills/sc-auggie-review-protocol/SKILL.md` and `src/superclaude/core/HOW-WE-WORK.md` name `prism-b` (a non-alias model the test does not catch); `src/superclaude/cli/sprint/aienv.py` lines 101-104 docstring: "`T2Model01` rotates to `T2Model02` (returned as that slot's model id, e.g. `grok-4.7`)".
- Reasoning that finds it: cross-task contradiction (Goal/Task 6 universal claim vs Task 5 and Task 6's own Known-consequences) plus a claim-vs-test scope check ("does the Task 1 test actually enforce the rule Task 6 says it enforces?"). A repo grep for non-alias selectors strengthens it but is not required: the contradiction is fully inside the candidate.

### B8 = alias GT3 (contradiction, blocking in implement)

- plan_quote: "that the issue workers are the only primitives pinned to picker ids and all other primitives use aliases (docs/reference/model-aliases.md)"
- GT description: Task 7 mandates a sentence in tiers.md claiming all other primitives use aliases, which is false because most agent, skill and command files have no `model:` line and the policy test skips them.
- Location in `candidate.md`: Task 7 line 109. Conflicts inside the plan with Task 1 line 34 ("files without a `model:` line are skipped").
- Repo conflict (counted in the reviewer sandbox): 33 of 49 `src/superclaude/agents/*.md` have no `model:` line; only 1 of 86 `skills/*/SKILL.md` + `commands/*.md` files has one. The delivered repair is visible in the sandbox at `src/superclaude/skills/sc-issue-protocol/refs/tiers.md:42` ("Within the scope of `tests/skills/test_model_alias_policy.py`, ... the other agent, skill and command files that have a frontmatter `model:` line name an alias").
- Reasoning that finds it: plan-vs-repo fact check of a universal quantifier ("all other primitives"), i.e. count files with and without `model:`; or the in-plan cross-check against Task 1's skip rule. Both are quantifier-scope checks: the claim is broader than the test that backs it.

### I6 = alias GT4 (ambiguity, not blocking; never found by any of 106 runs)

- plan_quote: "in a ccsession tier workspace opus, sonnet and haiku map to claude-gw-tier1a, claude-gw-tier1b and claude-gw-tier2 once the launcher sets them; see docs/reference/model-aliases.md"
- GT description: Task 7's prescribed user-guide text omits the "today the workspace defaults file exports real model ids" half that the plan's mapping constraint requires of new mapping text.
- Location in `candidate.md`: Task 7 line 109 (brainstorm.md `--models` row text; commands.md "the same pointer"; tiers.md item 4). Conflicts with Constraint line 23: "New text that describes the mapping says it holds once the launcher sets the three variables; today the workspace defaults file exports real model ids for them." Task 3 line 66 has the same omission in the chains.md bullet (same pattern, not in GT).
- Reasoning that finds it: constraint-compliance sweep. Take each Constraint (lines 19-26) and test every verbatim text the plan dictates against it. The dictated text satisfies the first clause ("once the launcher sets them") and drops the second ("today ... real model ids"). A two-clause constraint where the plan honours one clause is the hardest pattern for a skim.

### I7 = control GT1 (missing task, not blocking in implement, cost: human acceptance)

- plan_quote: "`make verify-sync` and `make lint` exit 0 and the whole `tests/skills/test_issue_protocol.py` file passes; the outputs are saved to `./artifacts/t12-checks.log`."
- GT description: Tasks 2, 3, 5 rewrite or add `gh api` lines in refs/create.md, refs/labels.md, SKILL.md and issue-worker-t3.md but no task updates the exact-line classification table in `tests/skills/test_worker_contract.py`, and Task 12 gates only on `test_issue_protocol.py`, so two worker-contract tests stayed red.
- Location in `candidate.md`: gh-api edits in Task 1 line 34 (labels.md POST and read-back), Task 2 line 47 (create.md call rule and Wave 1), Task 3 line 60 (SKILL.md call rules lines 73-74), Task 5 line 85 (issue-worker-t3.md "Read-only GitHub access" bullet, line 27). The only test file named anywhere is `tests/skills/test_issue_protocol.py` (Tasks 7, 8, 12; gate at line 171). `source.md` section 3.2 (line 105) also names only `test_issue_protocol.py`, so the plan faithfully copies the source's omission: a plan-vs-source check cannot find it.
- Repo conflict: `tests/skills/test_worker_contract.py` `WRITE_VERB_CLASSIFICATION` (sandbox line 2016) keys entries by (file, verb, exact line text); `test_every_write_verb_hit_is_classified` (line 3169) and `test_classification_table_has_no_stale_entries` (line 3173) fail when a classified line changes. Commit `54e21668f` removed the old `issue-worker-t3.md` "Read-only GitHub access" line and old SKILL.md lines from this table, the fix the parent session had to make. The file mentions `sc-issue-protocol` or `issue-worker-t3` 21 times.
- Reasoning that finds it: missing-task detection by test-dependency discovery. For each file the plan edits, grep `tests/` for its path and ask whether the gate runs every test that reads it. Only a reviewer who leaves the candidate and searches the test tree reaches it.

## 2. What the cheap reviewers did (30 cheap runs, 98 reviewer reports per package)

Method: for every final report in the 30 cheap rows, the transcript `<rid>.attempt<N>.json` (N = `attempt` in `<rid>.meta.json`) was parsed for tool_use calls and tool_result text. "Saw X" means X appeared in a tool result.

### Aggregate tool use (per reviewer, mean)

| Package | Model | n | turns | tool calls (min-max) | Read | Bash | Grep/Glob tool | read source.md | ran pytest |
|---|---|---|---|---|---|---|---|---|---|
| alias | ember | 39 | 16.8 | 15.8 (6-63) | 2.3 | 13.4 | 0 | 8 | 7 |
| alias | luna | 48 | 20.1 | 17.4 (6-25) | 13.6 | 1.2 | 0 | 11 | 1 |
| alias | haiku | 11 | 10.6 | 9.6 (4-17) | 2.7 | 6.9 | 0 | 3 | 3 |
| control | ember | 39 | 13.9 | 12.9 (3-23) | 5.9 | 6.9 | 0 | 26 | 6 |
| control | luna | 48 | 15.9 | 13.4 (7-21) | 11.1 | 0.9 | 0 | 48 | 0 |
| control | haiku | 11 | 10.6 | 9.6 (5-25) | 3.4 | 4.5 | 0 | 9 | 2 |

Style per model:
- luna is a Read-driven follower: it opens every file the candidate names, one Read per file (often via `Skill sc:spec-panel` first, sometimes codegraph), almost never runs a search of its own (0.9-1.2 Bash calls). It reads source.md only when the candidate cites source sections (48/48 on control, whose tasks say "Source sections: Q1..."; 11/48 on alias, whose tasks never cite source sections).
- ember is a Bash grep-checker: targeted greps and `sed -n` on the lines the plan cites, checking each stated line number and string. Wide but shallow; heavy on "line N is stale" findings.
- haiku makes few calls (median under 10) but writes very long reports (42k-65k output tokens in the samples); it runs the widest single greps of the three (`grep -rln ... src tests docs`), so it is the cheap model most often exposed to the right file.

### Exposure without follow-up (near misses in the transcripts)

- I7: 6 of 98 cheap control reviewers had `test_worker_contract.py` appear in a tool result and none opened it: haiku 5 of 11 (h1-r2 t2-1, h1-r3 t2-1, e5 t4-1, g7-r1 t4-1, g7-r2 t4-1), luna 1 of 48 (g7-r1 t3-1, from `ls tests/skills`). The clearest case is haiku `h1-haiku-luna2-ember2-r2/t2-1`: it ran `grep -rln "issue-types\|issue-fields\|issue-field-values" src tests docs`, the output listed `tests/skills/test_worker_contract.py` next to `test_issue_protocol.py`, and the report (7 findings) never mentions it. The other haiku hits are `ls` listings of `tests/skills`. Nobody in a cheap row ever passed `worker_contract` as a tool input.
- B8: 44 of 98 cheap alias reviewers saw the repaired sandbox sentence at `refs/tiers.md:42` ("Within the scope of `tests/skills/test_model_alias_policy.py` ... that have a frontmatter `model:` line"), i.e. the narrowed version of the very sentence Task 7 dictates (ember 24/39, luna 11/48, haiku 9/11). None compared it with Task 7's broader wording. Several instead reported "tiers.md already carries the new wording, the edit has no target" (haiku g7-r2 t4-1 F5).
- B6: two cheap reports anchored on the Goal's aliases-only sentence but took the wrong angle. luna `g6-luna2-ember2-r3/t4-1` F2 (MAJOR, non-blocking, missing-requirement): "does not clarify whether existing issue-chain /model picker-ID lines are exempt from its alias-only policy". The judge ruled it "concerns issue-chain /model lines, not GT1". haiku `g7-haiku-luna2-r1/t4-1`: the Goal allows only opus/sonnet/haiku but Task 1 accepts inherit and omits fable (alias-list angle, not the slot or test-scope angle).
- I6: the sibling defect GT2 (Task 6 "outside one nothing is set" vs Constraint line 23 "today the defaults file exports real model ids") was raised in cheap rows by luna h1-r2 t4-1 (blocking), luna g7-r2 t4-2 (blocking), ember h1-r4 t3-1 (minor) and others. That is exactly the comparison that finds I6; none of them repeated it on Task 7's dictated text (line 109) or Task 3's bullet (line 66).

### What cheap reviewers anchored instead (sampled reports, findings blocks read)

The sandbox being post-implementation pulls cheap reviewers toward "the plan does not match today's tree" findings:

Alias:
- ember `g6-luna2-ember2-r2/t3-1` (35 turns, 34 tools, 31 Bash, read source.md, grepped `--model`): F1 blocking, TIER_TEXT_ALLOWED misses `src/superclaude/cli/review/data/`; F2, stale Task 9 line anchors. Verdict FAIL.
- ember `e3-ember2-luna/t2b-1` (16 turns, 14 Bash): F1 the same review-data allow-list gap; F2, Task 5 says four variables but lists five.
- luna `g6-luna2-ember2-r2/t4-2` (23 turns, 13 Read, codegraph): F1 Task 9 launcher line numbers wrong; F2 "outside one nothing is set" vs inherited environment (a GT2-adjacent point).
- luna `g1-ember-luna2-r1/t3-1` (26 turns, 19 Read): one finding only, stale launcher anchors.
- haiku `h1-haiku-luna2-ember2-r2/t2-1` (9 turns, 8 tools, 65k output tokens): 10 findings. Review-data allow-list gap; "six of seven named failures already pass"; pin order; reflect default consequence; defaults.sh contents; fable exclusion. None on B6/B8/I6.
- haiku `g7-haiku-luna2-r2/t4-1` (13 turns, 12 tools): 12 findings, mostly staleness ("underscore names are not in the tree", "both files already exist", RUNGS line numbers, `_DEFAULT_MODEL` at line 37 not 31).

Control:
- ember `g5-ember2-luna-r4/t2b-1` (24 turns, 23 tools, ran pytest 3x): PASS. Artifact path outside the allowed edit roots; stale test line; short `orgs/<owner>` form.
- ember `g6-luna2-ember2-r3/t3-1` (12 turns): PASS. Third-block value semantics; POST input path; stale lines; artifacts path; `--mode` row omits Test.
- luna `g9-ember-luna-r1/t4-1` (19 turns, 14 Read, 0 Bash): three CRITICAL contradictions (mode row vs Q7; `make sync-dev` vs no `.claude/` edits; artifact path outside edit roots).
- luna `g7-haiku-luna2-r1/t3-1` (22 turns, 19 Read; its `ls tests/skills` listed `test_worker_contract.py`): two-writes vs mode label and pushback; artifact path; GT2 read-back rule.
- haiku `h1-haiku-luna2-ember2-r2/t2-1` (8 turns, 7 tools incl. WebFetch): Task 8 revert criterion unpassable for Task 3; two-writes vs pushback; GT2; "much of the change already exists at HEAD"; maintainer `--repo <owner/repo>`. It missed I7 despite the grep output above.
- haiku `e5-haiku-ember-luna/t4-1` (8 turns, 7 tools): 13 findings, again the two-writes contradiction, revert criterion, "live checkout already has the target text", artifact path.

Pattern: cheap reviewers check the plan line by line against the files and lines it names (plan-to-named-file), plus within-plan contradictions between adjacent sentences. They do not (a) search for files the plan does not name, (b) test universal claims ("all", "only", "enforces") against an inventory, or (c) sweep a constraint across every task. The post-implementation sandbox makes (a) worse: every named file yields an easy "already done / stale line" finding, which fills the report.

## 3. The runs that did find B6, B8, I7

Finders taken from `gt_covered_any` in `arms/scoring/combos/<row>/<pkg>/*/score.json` over all source.md-era runs.

### B6 (alias GT1): 1 run, `b4-terra-luna-muse` (set S28, luna + terra + wonder)

- Merged report `combos/b4-terra-luna-muse/TASK-WF-makeTheAliasOnly-20261105-051649/merged-1.md`, members t2-1 = gpt-6.1-terra, t2b-1 = muse-wonder-1.0, t4-1 = gpt-6-luna. The judge credits L3.t4-1 F1 and L3.t2b-1 F4.
- luna t4-1 F1 (MAJOR, blocking, contradiction): "The plan leaves /model claude-gw-tier2 and /model claude-gw-tier1a selections in the issue-chain table, so the alias-only goal is violated while the proposed tests can still pass." Anchor: the Goal sentence; anchor2: Task 3's chains.md edit. Move: plan-vs-repo on a file the plan edits. It read `refs/chains.md` in full (sandbox lines 11-16 hold `/model claude-gw-tier2` and `/model claude-gw-tier1a`), saw that Task 3 removes only `--models`, and tied the leftover non-alias selections to the Goal and to the test's scope. Tools: 21 turns; read source.md; one `augment_code_search`; codegraph on aienv.py, retry.md, reflect commands.py; Reads of chains.md, retry.md, test_aienv.py and others.
- wonder t2b-1 F4 (MAJOR, non-blocking): no Task 1 test scans Agent-call model values, "so the enforced policy is narrower than the stated goal". Move: claim-vs-test scope check. 45 turns, about 40 Bash greps reproducing each Task 1 test by hand.
- The same luna observation was NOT credited in a cheap row: `g6-luna2-ember2-r3/t4-1` F2 read chains.md and raised the `/model` picker-ID lines but framed them as "does not clarify whether ... exempt" (missing-requirement, non-blocking). Credit turned on the framing "goal violated while the tests still pass" (contradiction plus test scope), not on the observation. luna can reach the evidence; it did not connect it to the goal-vs-test contradiction.

### B8 (alias GT3): 1 run, `g2-sonnet-ember-r3` (set S16, ember + sonnet)

- Merged members: t1b-1 = claude-sonnet-5-5, t2b-1 = muse-ember-1.0 (the ember block failed). Credited finding: sonnet t1b-1 F3 (MAJOR, non-blocking; credited at blocking through ledger row L1): "The added tiers.md sentence is false beside the allow-list that exempts all of sc-issue-protocol, whose chains.md rows tell the user to run /model claude-gw-tier ids."
- Move: inventory first. Its first repo call was `grep -rl "claude-gw-tier" src/superclaude` plus `grep -rnE "^model:" src/superclaude/agents ...` (full lists of tier-id text and `model:` lines), then it checked the universal sentence against those lists. It also read source.md and ran behavioral probes (a Python call of the aienv functions with tier-valued env). 15 turns. Its reason (tier-id text in chains.md) differs from GT's (files with no `model:` line), but both come from a quantifier-vs-inventory check. The chains.md `/model` rows are the shared evidence behind both the B6 find and the B8 find.

### I7 (control GT1): 9 source.md-era runs

| Row | Set | Finding reviewer | How `test_worker_contract.py` first reached it |
|---|---|---|---|
| h2-sonnet-luna2-ember2-r2 | S02 | sonnet t1b-1 F1 | Read `.dev/reflect/pre-design-20261108041729/REPORT.md` (LEAK, see below) |
| h2-sonnet-luna2-ember2-r4 | S02 | sonnet t1b-1 F1 | repo-wide grep for the old label wording across `src docs tests plugins` |
| b4-sonnet-luna2 | S06 | sonnet t1b-1 F1 | `grep -rn "sc:issue\|sc-issue" ... -l .` (every file that mentions the feature) |
| j1-sonnet-luna2-r1 | S06 | sonnet t1b-1 F1 | Read the same reflect REPORT.md (LEAK) |
| j1-sonnet-luna2-r2 | S06 | sonnet t1b-1 F1 | repo-wide grep for old wording and `orgs/` paths across `src plugins tests` |
| r2-sonnet-ember | S08 | sonnet t1b-1 F4 | `grep -rIl "sc:issue\|sc-issue" .` |
| n4-sonnet-ember | S11 | sonnet t1b-1 F3 | `grep -rIln "sc:issue" .` |
| r2-sonnet-src | S18 | sonnet t1b-1 F1 | `grep -rnI -l -e "/sc:issue" .` |
| r3-luna2-grok-src | S19 | grok-4.7 t4-2 F4 | a batched inspection script (greps across the repo) |

- 8 of 9 finds are by sonnet; the ninth is grok, not luna (the S19 luna members did not raise it). No luna, ember or haiku reviewer raised I7 in any run.
- The winning move in the 7 clean finds is a reverse-dependency sweep: list every file in the repo that mentions the feature (`sc:issue`, `issue-fields`, the old label wording), not only the files the plan names, then open the unexpected test file and see that it pins edited lines verbatim. The findings all say "exact-line table" or "pins by exact text", which is only visible after opening the file (inferred from the claim text; the opening Read was not traced call by call).
- LEAK: the sandbox is a `git archive` of HEAD minus `.dev/tasks/done`, `.dev/eval-workspaces` and `.dev/research` (`manifest.md` line 10), so it still contains `.dev/reflect/pre-design-20261108041729/REPORT.md`. That file is the original pre-implementation reflection of this very plan, and its line 23 says: "it never updates `tests/skills/test_worker_contract.py`, which will fail when the plan's tasks rewrite and add `gh api` lines". 6 control reviewers opened it (sonnet h2-r2, j1-r1, j1-r3, n5-superseded; wonder n4-superseded; glm r5). 2 of the 9 I7 credits (h2-r2, j1-r1) come after reading it. The clean I7 count is 7, all sonnet or grok. The alias equivalent, `.dev/reflect/pre-TASK-WF-makeTheAliasOnly-20261105-034531-20261105034821/REPORT.md`, reviews the FIRST plan and does not mention the B8 sentence or `test_worker_contract` (grep: 0 hits), so it does not leak B6/B8/I6.

## 4. Conclusions: the move each missed issue needs, and a hint that could trigger it

The hint must name a kind of check or a region to inspect, not the defect. Each hint below is phrased as a peer's mid-run note that a cheap reviewer could act on with one or two tool calls.

### B6 (alias GT1)

- Needed move: test a universal goal claim against (1) the plan's own later tasks and (2) the scope of the test that is said to enforce it. The evidence is inside the candidate (Goal line 15, Task 1 lines 34-37, Task 5 line 86, Task 6 line 99), and the repo route via chains.md `/model` rows is the one that actually scored.
- Cheap models get halfway: luna read chains.md and noticed the `/model` picker-ID lines but graded them "unclear exemption".
- Plausible hint: "The Goal and Task 6 state an 'only X' rule and say a test enforces it. Check what the Task 1 tests can actually fail on, and whether any task, or any file a task edits, keeps a selection outside X." This points at the claim-vs-test-scope comparison without naming slot variables, prism-b or chains.md.
- A weaker, framing-only hint for a reviewer that already has the observation: "If a file the plan edits keeps something the Goal forbids and no test catches it, grade it as Goal vs test contradiction, not as a missing clarification."

### B8 (alias GT3)

- Needed move: inventory check of a universal quantifier. Count which primitives actually have a `model:` line (33 of 49 agents and 85 of 86 skills/commands have none) or list the `claude-gw-tier` text, then compare with "all other primitives use aliases". The in-plan route is Task 1 line 34's skip rule.
- Cheap models did not run inventory greps on claims; 44 of 98 even saw the repaired narrower sentence and did not compare it.
- Plausible hint: "Task 7 dictates sentences with 'only' and 'all other'. For each such sentence, list the files it quantifies over and count the exceptions; compare with what the Task 1 tests skip." This hands over the method (quantifier vs inventory), not the result.

### I6 (alias GT4)

- Needed move: sweep each Constraint across every piece of verbatim text the plan dictates. Constraint line 23 has two clauses; the Task 7 (line 109) and Task 3 (line 66) texts honour only the first.
- Cheap models already make the matching comparison for Task 6 (the GT2 finds); they stop after one task.
- Plausible hint: "Someone found Task 6's mapping text conflicts with the Constraints. Check every other place the plan dictates mapping wording (other tasks, other files) against the same constraint, clause by clause." This is the strongest candidate for a peer hint, because it can be triggered by a peer's own GT2 finding without revealing I6. No run of 106 found I6, so this is untested.

### I7 (control GT1)

- Needed move: reverse-dependency sweep. For each edited file, grep the whole tree (especially `tests/`) for its path or for the feature's key strings, and ask whether the plan's gate (Task 12 line 171 runs only `test_issue_protocol.py`) covers every test that reads it. Plan-vs-source cannot find it (source.md 3.2 names only `test_issue_protocol.py`).
- Cheap models (haiku most of all) already run greps whose output lists `test_worker_contract.py` (5 of 11 haiku control reviewers), but never open an unfamiliar test file.
- Plausible hint: "Task 12 gates on a single test file. Grep `tests/` for the files Tasks 2, 3 and 5 edit and open any test file the plan never mentions." A sharper variant for a reviewer that already has the output: "Your grep listed test files the plan never names; open them before you finish."
- Caveat for evaluation: any future run must remove `.dev/reflect/` (at least `pre-design-20261108041729`) from the sandbox, or I7 hits remain partly a leak (2 of 9 here).

### Cross-cutting

- Three of four misses (B6, B8, I7) need the reviewer to look beyond the files the plan names: an inventory or reverse-dependency grep. The fourth (I6) needs a constraint-by-task sweep. Both are process moves, not model knowledge, which is why a short peer note on what to check is plausible; a peer handing over findings would turn the hint into the answer.
- The reviewer sandbox shows the post-implementation tree. It both hides some "before" evidence (tiers.md already narrowed, test table already updated) and floods cheap reviewers with "already done / stale line" findings. Reviewing against the plan's base commit would change what plan-vs-repo checks can find.



