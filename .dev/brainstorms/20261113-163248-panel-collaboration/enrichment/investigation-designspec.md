# Investigation: why cheap panels missed GT1, GT2, GT5, GT6, GT9, GT10 on TASK-WF-designSpec-20261107-075614

Date: 2026-11-13. Read-only investigation.

- EVAL = `.dev/eval-workspaces/tasklist-review-panel/20261111-a1`
- Plan reviewed: `EVAL/TASK-WF-designSpec-20261107-075614/candidate.md` (200 lines, sha256 044809e3...)
- Spec given to reviewers: `.dev/tasks/done/TASK-WF-designSpec-20261107-075614/source.md` (378 lines)
- Ground truth: `EVAL/TASK-WF-designSpec-20261107-075614/ground-truth.json`
- Reviewer reports: `EVAL/<pkg>/reviews/combos/<row>/<rid>.md`, transcripts `<rid>.attempt<N>.json`
- Cheap sets (era source.md): S01, S03, S04, S05, S07, S10, S13, S24 = 30 runs, 98 reviewer reports (39 ember, 48 luna, 11 haiku).

Model ids in the transcripts: ember = `muse-ember-1.0`, luna = `gpt-6-luna`, haiku = `claude-haiku-5-5`, sonnet = `claude-sonnet-5-5`, grok = `grok-4.7`.

**A confound that affects every finding below.** The reviewers' repository (`/tmp/evalsb/repo`, HEAD `8c93e1d snap`) already contains the finished feature, including the executor's repairs:
- `src/superclaude/pr_submit/merge_guard.py:256` sets `record["disabled_cause"] = cause` for every skip, which repairs GT6.
- `refs/merge-guard.md:146` says "A halt with `terminal_halted` reason `draft_guard_unavailable` reports `unavailable`", which repairs GT5.
- `commands/pr-submit.md:81` has the heading `## Merge guard (`--merge-guard`)`, so the GT9 grep passes.
- `CHANGELOG.md:166` still says "The run-log event enum has 43 members". GT10 is the only defect still visible in the repo.

So a reviewer who checks the plan against the code finds the repaired code, and the check confirms the plan instead of exposing these defects.

## 1. The missed items: where they are and what reasoning finds them

### GT1 (unpassable AC, blocking in implement, cost both)
- plan_quote: "The file lists every exact-text pin and line-content rule found for O3"
- description: "Task 1 AC3 demands a provably complete inventory of every pin and line rule with no bounded method or stopping rule, so each review found new missing pins and Task 1 took five attempts, hit the retry ladder end and needed two operator-review halts before it was accepted."
- Location: candidate.md:38 (Task 1 AC3). The O3 instruction is at candidate.md:33.
- Conflicts with: no single sentence. The real outcome is in `progress.md:4-22`: T1 was blocked at every review, reached the retry-ladder end (`halt review=5 reason=ladder-end`), then hit two operator-review halts. `artifacts/retries/T1/review-5.md` still raises `F7.1 ... anchor="lists every exact-text pin and line-content rule found for O3" family=o3-pin-completeness`, which asks for one more test card.
- Reasoning needed: **satisfiability and stopping-rule reasoning about an acceptance criterion.** The reviewer has to ask "who decides that *every* pin was found, and by what bounded method?" Read on its own, the sentence looks reasonable. The defect only shows when you model a QA reviewer applying it adversarially.
- Rubric effect: the grading sentence in the review prompt ("An implementer who follows the stated text as written builds X, and X is wrong") pulls attention toward wrong builds. An open-ended inventory is not a wrong build; it produces an endless review loop. The rubric's "an acceptance criterion cannot pass" clause does cover it, but only when "cannot pass" is read as "cannot be shown to pass".

### GT2 (ambiguity, blocking, cost both)
- plan_quote: "on `SKILL.md`, `refs/state-machine.md`, `refs/loop-guard.md` and `src/superclaude/commands/pr-submit.md` that the later additive edits must avoid"
- description: Task 1 names four target files for O3, while AC3 says only "found for O3". Implement-time reviewers kept widening the scope (refs/ci-poll.md, refs/review-retrigger.md, the python package, folder-wide text tests), and that fed the same five-attempt loop.
- Location: candidate.md:33 (the scope, in the Task 1 body) against candidate.md:38 (AC3, "found for O3", no scope).
- Source: source.md:341 is narrower. It names `pr-submit.md` (argument-hint, Options table) and `SKILL.md` plus two named line-content rules, and says "grep before editing". The plan widened this to four files and "every".
- Reasoning needed: **comparing a task body with its own AC (scope drift between the instruction and the check), plus a plan-vs-source comparison** (source O3 is bounded; plan O3 is not). The GT1 stopping-rule reasoning is also needed to see why the gap matters.

### GT5 (ambiguity, blocking, cost extra_attempt)
- plan_quote: "Exit report (the `merge_guard` field mapping of `guard_status`, the held-exit list with the clear command"
- description: Task 8 defines the exit-report field only as the guard_status mapping. Under Task 3, no record at ordinal 3 gives `released`. Task 8 also drops the source rule that a `draft_guard_unavailable` halt reports `unavailable`, so the ref would report `released` after an engage halt.
- Location: candidate.md:124 (Task 8, the Exit report clause). candidate.md:61 is the Task 3 AC "no record at ordinal 3 (`released`)". candidate.md:129 has the halt `draft_guard_unavailable` "before any edit".
- Source rule dropped: source.md:112, last sentence: "A halt with reason `draft_guard_unavailable` reports `unavailable`." Also relevant are source.md:68 and the engage rows 3 and 8 (source.md:135, :140), which halt before any request event exists, so the fold returns `None`.
- Reasoning needed: **plan-vs-source comparison (a dropped rule) plus a cross-task trace.** The reviewer has to follow the engage halt path: HALT_UNAVAILABLE before `draft_guard_requested` means no guard record, so `guard_status` takes the no-record row and returns `released`. Then they must notice that Task 8 delegates the field entirely to that mapping.

### GT6 (contradiction, human acceptance, not blocking)
- plan_quote: "`settled(draft, skipped, already_draft)` gives `DISABLED` with `disabled_cause == \"already_draft\"`"
- description: Task 3 requires guard_status to return `user_override` for a DISABLED phase with cause user_override, but the fold rows it implements set `disabled_cause` only for already_draft.
- Location: candidate.md:56 ("implementing every row of the section 4.2 effect table", with field `disabled_cause`), candidate.md:60 (the fold AC, where only already_draft sets a cause), candidate.md:61 (`DISABLED` with `user_override` gives `user_override`).
- Source: source.md:200 (`settled(draft, skipped, already_draft)` → `disabled_cause = already_draft`) against source.md:206 (`settled(any, skipped, user_override)` → `phase = DISABLED`, `owned_draft = False`, with **no** cause), and source.md:112 (guard_status keys on cause `user_override`).
- Reasoning needed: **plan-vs-source comparison across two tables (the fold effect table against the status mapping).** The reviewer has to check that every input the mapping reads is written by some fold row. The plan alone does not show it, because "every row of the section 4.2 effect table" points into source.md.

### GT9 (contradiction, not blocking)
- plan_quote: "`grep -n \"merge-guard\" src/superclaude/commands/pr-submit.md` shows the argument-hint entry, the Options row and the section heading"
- description: Task 12 asks for a section named "Merge guard", but its AC checks the heading with a case-sensitive grep for `merge-guard`, which that heading cannot match.
- Location: candidate.md:182 (`a short "Merge guard" section`) against candidate.md:185 (the AC grep).
- Reasoning needed: **literal string matching of an AC command against a name given in the same task.** This is a within-task check, done mentally or by running the grep. It does not need source.md. Checking the repo works against finding it, because the implemented heading `## Merge guard (`--merge-guard`)` (pr-submit.md:81) passes the grep.

### GT10 (missing task, not blocking)
- plan_quote: "shows no remaining claim that the enum has 43 members, and `refs/loop-guard.md` names both new event values"
- description: "Task 2 updates the 43-member enum claim only in three files and plans no CHANGELOG.md edit, so the unreleased changelog entry still says the event enum has 43 members after the change."
- Location: candidate.md:49 (Task 2 AC3, a grep limited to `models.py`, `run_log.py`, `refs/loop-guard.md`). The edit list is at candidate.md:44.
- Repo: `CHANGELOG.md:166` "- The run-log event enum has 43 members (`sync_started`, `sync_concluded`)." At plan time this was CHANGELOG.md:145, per `artifacts/retries/T2/notes.md`. source.md never mentions CHANGELOG; source.md:175 lists only `models.py:3,24` and `run_log.py:117`.
- Reasoning needed: **plan-vs-repo enumeration.** The reviewer must run a repo-wide search for the stale claim, beyond the AC's three files and the spec's file list, and must include root-level docs.

## 2. What the cheap-model reviewers did

### 2a. Effort profile from the transcripts (all source.md-era rows on this package)
Medians are per reviewer report, taken from `result.num_turns`, `duration_ms`, the count of tool_use blocks and `usage.output_tokens`.

| model | n (cheap sets) | turns | wall | tool calls | opened source.md | touched implemented guard files | touched commands/pr-submit.md | output tokens |
|---|---|---|---|---|---|---|---|---|
| ember | 39 | 12 | 34 s | 11 | 64% (14 of 39 never named source.md in any tool call) | 82% | 35% | 9.8k |
| luna | 48 | 14 | 84 s | 11 | 100% | 33% (luna mostly uses `codegraph_node` by symbol, so this undercounts) | 8% | 4.1k |
| haiku | 11 | 8 | 220 s | 7 | 90% | 100% | 36% | 53k (mostly thinking) |
| sonnet (other sets, n=26) | | 15 | 223 s | 14 | 100% | 100% | 53% | 31k |
| grok (other sets, n=8) | | 46 | 998 s | 43 | 100% | 100% | 75% | 57k |

The 14 ember reports that never opened source.md: g6-luna2-ember2-r2/t2b-1, g6-r3/t2b-1, h1-haiku-luna2-ember2-r1/t2b-1 and t3-1, h1-r2/t2b-1, h1-r4/t2b-1, e3-ember2-luna/t2b-1, g5-ember2-luna-r3/t2b-1 and t3-1, b4-muse-ember-luna2/t2b-1, g1-ember-luna2-r1/t2b-1, e5-haiku-ember-luna/t2b-1, g9-ember-luna-r1/t2b-1, g9-r2/t2b-1. e3-ember2-luna/t2b-1.md says it outright: "Skipped: full-suite run and `./source.md` source verification." GT5 and GT6 both need source.md, so these reviewers could not find them.

No cheap reviewer in any cheap row named CHANGELOG in a tool call. Across all 819 transcripts on this package, only one reviewer did: grok in n3-muse-luna-grok-src (see section 3).

### 2b. Sample reports (2+ per model, different rows)

**ember g6-luna2-ember2-r1/t2b-1**: 31 s, 9 turns, 8 tools. It read the review prompt and source.md in full, then ran four Bash greps: imports in run_log/conflicts/recovery, `sed -n '100,140p' run_log.py`, `grep -n "43\|45" run_log.py`, and the test_skill_parse/merge_guard names. 3 findings: F1 Task 9 Wave 0 wording (GT3), F2 Tasks 7, 8 and 12 classification omits git verbs, F3 Task 2 test lengths unnamed. It never touched Task 1 O3, Task 8's exit report, the fold user_override row, the Task 12 heading or files outside the plan.

**ember g5-ember2-luna-r2/t3-1**: 67 s, 25 turns, 24 tools. It read source.md, `models.py`, `merge_guard.py` (already implemented), `fsm.py`, `test_static_grep.py`, `set-draft-state.sh`, `refs/merge-guard.md` and `__init__.py`, and its last call was `grep -n "src/superclaude\|merge-guard\|Merge guard" commands/pr-submit.md`. That grep showed the implemented `## Merge guard (`--merge-guard`)` heading, so the GT9 check came back clean. 5 findings: F1 resume row 4 lacks target_sha (GT7), F2 Task 7 repo-resolution fallback, F3 held cycle rebind, F4 Task 1/13 `./artifacts` location, F5 Task 2 grep. **F5 is a near-miss on GT10.** Its anchor is the GT10 plan_quote ("shows no remaining claim that the enum has 43 members..."), but the claim is "A literal grep for 43 also matches legitimate ordinal comments, so the check over-reports". The reviewer said the grep is too broad, when the defect is that its file list is too narrow.

**luna g1-ember-luna2-r1/t3-1**: 113 s, 16 turns, 13 tools: Skill, the prompt, Read source.md, sha256, git status, 3× `codegraph_node`, Read `test_static_grep.py`, `test_worker_contract.py`, `SKILL.md` at offsets 270 and 309, then 1× `codegraph_node`. **0 findings, verdict PASS**: "I found no concrete wrong outcome or acceptance criterion that cannot be met."

**luna g9-ember-luna-r3/t4-1**: 73 s, 12 turns, 9 tools (Skill, prompt, Read source.md, sha256 plus git status, 5× `codegraph_node`). 1 finding, F1 blocking, on Task 9 Wave 0 (GT3). Its partner ember g9-r3/t2b-1 states the opposite of GT1/GT2 at line 9: "The plan correctly defers O1/O2/O3/O4 to Task 1 reading before protocol edits". It reads Task 1 as a strength.

**luna g6-luna2-ember2-r2/t4-1** and **luna g5-ember2-luna-r4/t4-1** are near-misses on GT5. Both anchor on the GT5 text or the field next to it. g6-r2 F1 (blocking) anchors on "the `merge_guard` field mapping of `guard_status`", which is the GT5 plan_quote. Its claim: "exit report ... map[s] its status through guard_status while also reporting a held guard when mode is off ... the mapping returns `off`". It analysed the same mapping for the mode-off + HELD case, not for the halt-without-record case. ember e3-ember2-luna/t2b-1 F2 reached the same mode-off conclusion without reading source.md.

**haiku e6-haiku-ember2/t4-1**: 207 s, 8 turns, 7 tools, 46.6k output tokens. Calls: prompt, sha256 plus ls, Read source.md, Read `merge_guard.py`, `git log -- merge_guard.py`, one batch script, `fsm` import grep. 9 findings, including GT7 (F1, blocking) and GT3 (F2). On Task 1 it found only F5, "The mint point is deferred to an open item" (O1, not O3). On Task 12 it found only F9, "Two forms of the clear command" (Task 12's clear-command AC, not the heading grep). F6 is "The checkout already tracks the module ... and the 43-member facts describe another base".

**haiku g7-haiku-luna2-r2/t4-1**: 301 s, 11 turns, 10 tools, 67k output tokens. Calls: Read source.md, then Bash greps of recovery.py `resolve_crash_window`, SKILL `push_completed`, the loop-guard enum text, fsm and `__init__` imports, failed push handling, `run_log.py` 108-128. 10 findings. F1: "The plan says to create and edit files and tests that already exist in the checked-out tree". Also GT7 (F2), GT3 (F3), and others. Nothing on O3, the exit report, user_override, the heading or CHANGELOG.

**haiku g7-haiku-luna2-r1/t4-1** is a near-miss on GT6. M2 anchors on the exact GT6 plan_quote ("`settled(draft, skipped, already_draft)` gives `DISABLED` with `disabled_cause == \"already_draft\"`"), but its claim is about mapping a `changed:false` draft settle. It did not check whether the user_override row sets a cause.

### 2c. Near-miss census across all 98 cheap reports
These counts come from the anchors and refs in the findings blocks.
- **GT10 area (Task 2 AC3 grep): 16 findings** (15 ember, 1 haiku: g7-r4 F6) anchor the GT10 sentence. All 16 say the grep over-matches the `# ... the 42nd-43rd ---` comment at `models.py:98`. None asks which other files carry the claim. The rows: g6-r1/t3-1, g6-r2/t2b-1, g6-r4/t2b-1 and t3-1, e6/t3-1, h1-r1/t3-1, h1-r2/t2b-1 and t3-1, h1-r4/t3-1, e3/t3-1, g5-r1/t2b-1, g5-r2/t3-1, g5-r4/t2b-1, g1-r2/t2b-1, g1-r4/t2b-1, g7-r4/t4-1.
- **GT1/GT2 area (Task 1): no finding in any row of any panel anchors O3 or AC3.** Cheap attention on Task 1 went to the `./artifacts` path against the git-status allowlist (about 10 ember findings), the O1 mint point (haiku e6 F5, h1-r3 M3, h1-r4 F6), the base-commit record (luna g6-r1/t4-2 F2, haiku e5 F6, r1-src F9), and O4 start-text versus byte-identical (about 8 findings). Several reviewers explicitly put O3 out of scope as "deferred": c2-haiku-grok/t4-1.md:14 "Not checked: the byte-level literal pins for O3 and O4", c5-glm-haiku/t4-1.md:64 "Those are O3 items for Task 1", r2-sonnet-ember/t4-1.md:15 (haiku) "Not covered: ... (the O2 and O3 contents)". Those three rows are outside the source.md era but show the same pattern.
- **GT5 area: 3 findings** (luna g6-r2/t4-1, luna g5-r4/t4-1, ember e3/t2b-1) on the same mapping, with a different conclusion (mode off + HELD → `off`).
- **GT6 area: 1 finding** (haiku g7-r1 M2), on the same row, with a different conclusion.
- **GT9 area: 0 findings.** Task 12 drew only dependency findings (ember g5-r1/t2b-1 F1, g1-r4/t2b-1 F1) and clear-command-form findings (haiku e6 F9, e5 F11, h1-r4 F4, r1-src F7).

## 3. Who found GT5, GT6 and GT9 in other panels, and how

Rows come from `EVAL/arms/scoring/combos/<row>/<pkg>/<arm>/score.json` `gt_covered_any`. The finder is attributed by matching the finding text in `reviews/combos/<row>/<rid>.md` against `<rid>.meta.json` `expected_model`, cross-checked against the merged-report member list (`EVAL/combos/<row>/<pkg>/merged-1.md`).

| GT | row (set) | finder | finding | investigative move |
|---|---|---|---|---|
| GT5 | b4-sonnet-luna2 (S06) | **sonnet** t1b-1 F7 | "The rule that a draft_guard_unavailable halt reports unavailable is not carried, and guard_status returns released when no guard record exists" (report line 65 quotes source 4.1) | Plan-vs-source. It went through source 4.1 rule by rule and checked each against the plan. It also ran `grep -n "unavailable" candidate.md` (tool call 14) to confirm the rule never appears in the plan. |
| GT5 | n5-sonnet-ember (S14) | **sonnet** t1b-1 F5 | "A draft_guard_unavailable halt after a failed first read leaves no guard record, so guard_status returns released" | A cross-task trace. It followed the engage read-failure path to "no record", then to the Task 3 no-record row. |
| GT5 (loose) | r2-sonnet-src (S18) | **haiku** t4-1 F9 | "A guard that never engaged reports released" (judge: loose, does not name the halt rule) | Read the Task 3 guard_status AC on its own and questioned what `released` means. |
| GT6 | h2-sonnet-luna2-ember2-r3 (S02) | **sonnet** t1b-1 F2 | report line 38: "The source fold row for `settled(any, skipped, user_override)` sets the phase to DISABLED but never says `disabled_cause = user_override`, yet guard_status keys on that cause" | Plan-vs-source, table against table (source 4.2 fold rows against the 4.1 mapping inputs). |
| GT6 | r3-luna2-grok-src (S19) | **grok** t4-2 F3 | report line 40 builds a row-by-row coverage table: "`settled(skipped, user_override)` / `disabled_cause` unset / status match needs `user_override` → GAP" | Systematic tabulation of each source effect row against the field it writes. 33 turns, 779 s. |
| GT6 | c3-luna-grok-src (S22) | **grok** t4-2 F2 | "The user-override settle never sets disabled_cause, so the status map does not report user_override." | Read the implemented `fold_draft_guard` and `_fold_settled` through `codegraph_node` (transcript steps 34 and 38). It noticed that the code sets the cause for every skip while the source table does not, and the thinking at step 36 says "the implementer therefore set disabled_cause for user_override even though the effect table did not explicitly require it. This confirms the gap." So the code diff against source revealed the gap here, even though the code itself was already repaired. 64 turns, 1005 s. |
| GT9 | b4-sonnet-luna2, j1-sonnet-luna2-r5, g2-sonnet-ember-r3, n4-sonnet-src (S06, S06, S16, S25) | **sonnet** t1b-1 in all four | e.g. j1-r5 F1: "A section headed \"Merge guard\" has no hyphen, so the criterion grep -n \"merge-guard\" cannot show the heading line" | Reads each AC command literally against the text the task asks for. g2 also ran `grep -n -i "merge.guard" commands/pr-submit.md; grep -n "^#.*[Mm]erge"`, saw the implemented heading carried the flag text, and still reported the plan defect, noting "The text also allows 'Merge guard (`--merge-guard`)', which passes". b4 says the same at report line 62. |

Observations:
- GT9 was found **only by sonnet** (4 of 26 sonnet reports). GT6 was found by sonnet once and grok twice. GT5 was found by sonnet twice, plus one loose haiku hit inside a sonnet-led panel. No luna or ember report found any of the three.
- The finders spent 190 to 1005 s each, against a cheap-panel median of 34 s (ember) and 84 s (luna).
- **GT10 was seen and dropped.** Grok in n3-muse-luna-grok-src/t4-2 (S23) ran `rg -n "len\(EventType\)|exactly 43|EXACTLY 43|43 members..."` repo-wide, got `CHANGELOG.md:166: - The run-log event enum has 43 members`, and Read `CHANGELOG.md` offset 150. Its thinking: "The CHANGELOG lists 43 members, but the plan omits updating it." Then: "A stale changelog is a missing documentation update, not a harmful omission. It is a minor issue that would not block the review." The final report does not mention it. The same happened in n3-muse-luna-grok (a non-source.md row).
- Sonnet g2-sonnet-ember-r3 also ran a repo-wide 43/45 grep, but scoped it to `src tests docs` (`--include=*.md ... src tests docs`). That scope excludes the root `CHANGELOG.md`, so it saw only 45-claims.
- GT1 and GT2 were never approached by any reviewer in any row: no anchor on candidate.md:33's O3 clause or on :38.

## 4. Conclusion: the move each missed issue needs, and whether a peer hint could trigger it

| GT | investigative move needed | why cheap reviewers did not make it (evidence) | peer hint that could plausibly trigger it without giving the answer |
|---|---|---|---|
| GT1 | Stopping-rule test on each AC: "can a QA reviewer ever be forced to say yes? Is 'every' bounded by a method or a list?" | Zero anchors on candidate.md:38 in any panel. Cheap reviewers read the O-items as good practice ("correctly defers O1/O2/O3/O4", g9-ember-luna-r3/t2b-1:9). The grading sentence steers toward wrong builds, not unending verification. | **Kind: rubric or lens hint, plausible.** For example: "For each AC that says *every*/*all*/*complete*, state the finite check that proves it." This names a class of AC, not Task 1. Expect it to also raise false positives on other "every" ACs (Task 3 AC2 "covers every row"), which are bounded by a table. The reviewer then has to tell bounded from unbounded, and that is the actual skill. |
| GT2 | Compare the scope in the Task 1 body (4 files) with AC3 ("found for O3", unscoped) and with source O3 (2 files, source.md:341). | Same blindness as GT1. 14 of 39 ember reports never opened source.md. No reviewer diffed the O-items against source.md:339-342. | **Kind: region pointer plus comparison verb, plausible.** "Compare Task 1's open items O1 to O4 with source.md's open-items list; check each AC states the same scope as its instruction." It points at a region and a method, not at the defect. One cheap reviewer making this move would also pull GT1 into view, since the two share a root. |
| GT5 | Plan-vs-source rule audit of source 4.1 (every sentence of the guard_status paragraph carried into Task 3/8?), or a path trace: engage halt → no record → `released`. | 3 cheap reviewers analysed the exact sentence (luna g6-r2 F1 *blocking*, luna g5-r4 F1, ember e3 F2) but only traced mode-off + HELD. None traced the halt path. ember e3 skipped source.md. The repo's `refs/merge-guard.md:146` already has the repaired rule, so code checks hide it. | **Kind: "trace another input" hint, highly plausible.** For example: "Your mode-off finding on the guard_status exit mapping: what does the mapping return after each halt reason in the engage table?" The cheap reviewers already had the right anchor and needed one more input case. This is the strongest hint candidate in the package. |
| GT6 | Table-coverage check: for each field the status mapping reads (`disabled_cause` values), find the fold row that writes it (source.md:200 against :206). | One haiku (g7-r1 M2) anchored the right row and asked a different question. ember/luna never tabulated fold rows against mapping inputs. The repaired code (`merge_guard.py:256`) masks the gap for anyone who checks code instead of source. | **Kind: method hint, plausible.** "Check that every value guard_status reads is written by some row of the source 4.2 fold table." This names a method and a table pair, not the missing assignment. Grok's success (a row-by-row GAP table, r3/t4-2:40) shows the move works once tabulation is prompted. Add "compare against source.md, not the checkout", because the checkout is already repaired. |
| GT9 | Run or simulate each AC's literal command against the text the task orders (heading "Merge guard" vs case-sensitive `merge-guard`). | 0 cheap findings on Task 12's AC1. The cheap reviewers who grep'd the real file (ember g5-r2/t3-1) saw the repaired heading and got a pass. Only sonnet (4/26) read the AC literally against the task text. | **Kind: method hint, highly plausible and cheap.** "For each grep/command AC, check that the text the task tells the implementer to write matches it literally, without relying on the current file." This is mechanical. ember and luna can run it in seconds, and the hint names no task. |
| GT10 | Repo-wide enumeration of the stale claim (`43 members`, `EXACTLY 43`), root files included, then compare with the AC's three-file list. | 16 cheap findings anchored GT10's sentence, but all inverted the question (the grep over-matches `models.py:98`). No cheap reviewer ran a repo-wide search. Sonnet's search excluded root files. Grok saw `CHANGELOG.md:166` and **dropped it as minor** ("not a harmful omission"). | **Kind: direction-flip hint, plausible.** "You checked that the Task 2 grep doesn't over-match. Check the other direction: where else in the repo does the 43 claim appear?" It points at completeness without naming CHANGELOG. Even if it is found, the severity rule in the prompt (Minor = note) may still drop it, as grok showed. A hint alone does not fix that; the report has to keep MINOR notes, and the scoring has to credit them. |

Cross-cutting causes, in order of impact:
1. **Repo contamination.** The sandbox checkout holds the repaired implementation, so a code check confirms GT5, GT6 and GT9 as fine. Haiku and luna spent findings on "the checkout already contains the feature" (h1-r1..r4/t2-1 F1/F3/F1, g7-r2..r4/t4-1 F1/F4/F4, g9-r1/t4-1 F1 *blocking*).
2. **Shallow source use by ember.** 36% of ember reports never opened source.md. GT5 and GT6 need it.
3. **Right anchor, wrong question.** GT10 (16×), GT5 (3×) and GT6 (1×) were anchored correctly but analysed along one axis. A peer hint that asks for the other axis (another input case, the other direction of completeness) is the cheapest fix, and it does not leak the answer.
4. **Rubric framing.** "Implementer builds X wrong" does not surface unbounded-verification ACs (GT1, GT2) and pushes doc-staleness (GT10) to MINOR, where reviewers drop it.
