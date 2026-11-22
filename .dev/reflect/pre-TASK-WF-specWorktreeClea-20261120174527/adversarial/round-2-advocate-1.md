# Round 2: Advocate for Variant 1 (analyzer lens), rebuttal

Citations: `PLAN` = `.dev/tasks/to-do/TASK-WF-specWorktreeClea-20261120-173546/TASK-WF-specWorktreeClea-20261120-173546.md`; `source.md` = the spec snapshot in the same folder; `branch-landed.sh` = `src/superclaude/skills/sc-closeout-protocol/scripts/branch-landed.sh`. Every line cited below was Read in this round.

## 1. Response to the opposing advocate's criticisms of variant 1

The opposing statement (round-1-advocate-2.md) holds only a summary and per-point verdicts. It credits variant 1 with C-001, C-005, C-006 and X-002, so its criticisms of variant 1 are of four kinds: what variant 1 did not raise (C-002, C-003, C-004), the missed Task 7 dependency, and, under A-001, that "verification timing is not explicitly defined". Responses:

1. **Missed Task 7 self-reference (C-001, X-002): conceded.** `PLAN:108` asks Task 7 to show "the script's removal reports 'kept' not an error", but Task 7 depends only on Task 6 (`PLAN:106`) and the verb bodies are stubs that "exit 64 with 'not built yet' until Tasks 11 and 12 fill them in" (`PLAN:45`). The removal pipeline is Task 11 (`PLAN:158`). This belongs in the merged C-001 finding.

2. **"Verification timing is not explicitly defined" (A-001, which bears on the C-001 grade): rejected as a reason to downgrade.** The plan itself shows the timing model. Every task carries its own "Acceptance criteria" block and a "Depends on" line (`PLAN:35`, `:43`, `:47`, `:57`, `:61`). More tellingly, the plan's author writes deferrals into early checks: "these refusals are asserted in Task 13's recorder tests" (`PLAN:49`), "the recorder test of Task 13 shows only read verbs" (`PLAN:63`), "the recorder test of Task 13 shows read verbs only" (`PLAN:76`), "asserted by the recorder test of Task 13" (`PLAN:85`). A deferral is only needed if checks are judged when each task ends. The executor named for a workflow plan, `/sc:implement`, describes itself as running "per-task spec-compliance QA" (its skill description in this session's skill list; the protocol file itself was not opened this round). So per-task timing is the operative model, and the checks that cannot be met at their own task's end without a declared deferral (`PLAN:62`, `:73`, `:108`, `:161`, `:174`) stay BLOCKING. The declared deferrals (`PLAN:49`, `:63`, `:76`, `:85`) I conceded in round 1 as less severe, and I keep that concession.

3. **Not raising C-002 (helper writes): conceded as a coverage gap, not as a blocker.** The side effects exist (section 3 below). Variant 1's silence is a missed Medium note, not a missed blocker, because the opposing advocate's own summary narrows the point: "fetch is conditional, temporary-file deletion does not establish data loss, and the spec also requires helper reuse", and it restates X-001 "as a requirement conflict rather than proven destructive behavior". Those words withdraw the Safety ground.

4. **Not raising C-003 (patch and bundle): conceded as a coverage gap.** Grade is Medium (section 3).

5. **Not raising C-004 (pull-request step): conceded in full.** `source.md:276` ends the acceptance list with "Finish with `/sc:pr-submit --monitor 3`" and `source.md:379` makes it step 7 of the plan of work. The plan's last task ends at the dry-run report and regression gate (`PLAN:263-274`). No task opens a pull request. Variant 2 deserves this point.

6. **C-006 (fallback conflict): the opponent agrees, and one counterpoint should be recorded.** The plan's chosen removal path (`orca worktree rm` for Orca-listed worktrees, `PLAN:158`) is the spec's default design (`source.md:95`), so the defect is not that the plan picked an unsafe path. The defect is that the proofs record, which Task 1 must fill with "the fallback of source section 11" for each item (`PLAN:33`, acceptance at `PLAN:36`), states item 2's fallback as item 1's. Item 1's fallback is "Use only `git worktree remove` ... and deregister from Orca" (`source.md:297`); item 2's is "Remove through Orca for the worktrees it lists" (`source.md:298`). With both NOT PROVEN (`PLAN:37`) they conflict, and `source.md:374` allows only "the fallback named in section 11 for that item" when a proof fails. Correcting the text either changes Task 11's removal path for Orca-listed worktrees or sends the conflict to the owner. Either way a required behaviour changes, so BLOCKING (Decision) holds.

## 2. Updated assessment of variant 2 after its defence

Variant 2's coverage is stronger than I credited in round 1 on one point (C-004 is a true Missing finding) and weaker on two (its own advocate narrowed F2, and F3 rests on a misread scope sentence).

- **F1 (ordering): sound, and narrower than variant 1's.** Its unique Task 7 self-reference should be merged in.
- **F2 (helper writes): real facts, wrong grade.** After the defence, variant 2's own position is "a requirement conflict rather than proven destructive behavior". A requirement conflict is BLOCKING only if correcting it changes a named decision, required behaviour or acceptance check. Variant 2's fix ("prove it in a throwaway repo") cannot meet Task 1's acceptance check, which needs "the `MERGED` line for pull request 700 ... verbatim" (`PLAN:37`): a throwaway repository has no GitHub pull request 700, and the helper reads the repository from `origin` of the current directory (`branch-landed.sh:18`, `:80-90`). And the spec itself asks for the real run: "run the check on a merged and an open pull request" (`source.md:299`). So the fix would move the plan away from the spec, not toward it. Medium.
- **F3 (patch and bundle): real gap, wrong grade.** It relies on `source.md:374` to say the drop needed the owner. Read in place, that sentence is step 2 of the plan of work, "The decisions are made (section 8). If a proof in step 1 fails, use the fallback named in section 11 for that item; any other change goes back to Clay." Its scope is changes to the decided design and to proof fallbacks; patch and bundle is neither one of the 11 decisions (`source.md:226-238`) nor a section 11 item. Medium, with an owner question as follow-up.
- **F4 (pull-request step): BLOCKING holds** on the spec's own evidence (`source.md:276`, `:379`), under the Missing ground.
- **Self-reported confidence 0.95:** still higher than its grading supports, since two of its four BLOCKING grades come down to Medium.

## 3. New evidence, and the grade test for C-002 and C-003

### 3.1 C-002 (the landed-check helper writes) under the grading rule

Facts, read in `branch-landed.sh`:
- The `git fetch` runs only on the MERGED path. OPEN, CLOSED and NONE exit at `branch-landed.sh:107-108` and `:120-128` before the fetch at `:182`. So in Task 1 the fetch happens once (pull request 700, `PLAN:33`) and never for the missing number.
- The `rm -f` at `branch-landed.sh:40` deletes only the helper's own `mktemp` file made at `:99`, a file in the temp folder and not in any worktree.
- The header says the only write is the fetch, "which touches objects and FETCH_HEAD only" (`branch-landed.sh:32-33`). A plain `git fetch origin <branch>` may also update the remote-tracking ref `refs/remotes/origin/<branch>`; that is UNVERIFIED here (not run) and changes no grade, because no rule or acceptance check rests on that ref.

Test against each blocking ground:
- **Decision.** No named decision, required behaviour or acceptance check changes if the text is corrected. The spec requires reusing the helper (`source.md:32`, `:159`, `:375`) and running it on real pull requests (`source.md:299`). The dry-run invariant is defined in the spec itself as "the recorded commands contain no removal" (`source.md:256`); Task 20's matching check is "no removal, no terminal close, no archive and no push" (`PLAN:270`). A fetch is none of those. The plan's "never `rm`" is scoped to the script itself: "The script never deletes a file or folder itself" (`PLAN:21`), and the spec's recorder test covers "every command the script runs" (`source.md:255`), not a child's internals. Correcting the text would at most add the words "except the helper's fetch" to Task 1's "no write" sentence (`PLAN:33`).
- **Missing.** Nothing required is absent.
- **Safety.** Following the plan loses or exposes no data and crosses no declared boundary: the plan's safety constraint bans removal, moving, clearing, automation, terminal close and push to the evidence repo (`PLAN:19`), not a fetch, and the spec mandates the call.

Result: **Medium.** It is a real weakness in substance (Task 1's "needs no write" wording is untrue for one call, and the recorder answers `branch-landed.sh` from canned replies, `PLAN:45`, `:108`, so no test sees the child's commands), but nothing named rests on it. Follow-up candidate: document the helper's fetch in Task 1 and the dry-run report.

### 3.2 C-003 (patch and bundle) under the grading rule

Facts, read in `source.md`:
- The phrase is a parenthesis in "What is not saved": "`archive` by hand can still save them as a patch and a bundle" (`source.md:214`).
- The normative verb definition omits it: `archive` "Runs only the evidence step of section 7 on one worktree: copy, push, check against GitHub" (`source.md:83`).
- Section 7's seven steps (`source.md:186-192`) have no patch or bundle step, format or folder.
- The acceptance list (`source.md:246-276`) has no patch or bundle case; the archive group (`source.md:261-269`) names only the `.dev` save.
- The plan of work's build list names "the archive step with its secret check and `saved-paths.txt`" and nothing more (`source.md:375`).
- The plan discloses the gap and records it in the verb's help text (`PLAN:25`, `PLAN:170`).

Test against each blocking ground:
- **Decision.** No acceptance check, named decision or build step of the spec rests on it; correcting it would add a capability, not change any decision the plan rests on.
- **Missing.** "Required ... named by the task, the template or the acceptance criteria": it is named only in an aside, with no acceptance case and no build step. Not a required deliverable in that sense.
- **Safety.** Leaving it out loses nothing: a worktree with tracked edits or later commits is always kept (`source.md:229`), so no data is removed unsaved.

Result: **Medium.** Real scope reduction made on the planner's authority, disclosed but not approved. Follow-up candidate: ask the owner whether to build it.

### 3.3 Missed by both cards: the OPEN answer is never proved

`source.md:299` says item 3 is proved by running the check "on a merged and an open pull request". Task 1 instead runs it on pull request 700 and "a number that does not exist, to see `MERGED` and `NONE`" (`PLAN:33`), and its acceptance check requires those two lines (`PLAN:37`). Correcting the text changes an acceptance check (OPEN in place of, or in addition to, NONE), so under the literal rule this is BLOCKING (Decision: acceptance check). Its practical consequence is small (the OPEN branch is still exercised from fixtures in Task 8, `PLAN:120`), and it is not a diff point between the cards, so I record it for the calibrator rather than as a variant 1 strength.

### 3.4 C-004 under the grading rule

The step is named by the spec's acceptance list (`source.md:276`) and its plan of work (`source.md:379`) and is absent from the plan (`PLAN:263-274`). That meets the Missing ground. BLOCKING.

## 4. Final positions

| Point | Final position | Grade | Confidence | Basis |
|---|---|---|---|---|
| C-001 (later-task dependencies) | Variant 1, merged with variant 2's Task 7 self-reference | BLOCKING (Decision: acceptance checks) on `PLAN:62`, `:73`, `:108`, `:161`, `:174`; declared deferrals (`PLAN:49`, `:63`, `:76`, `:85`) not blocking | High | Per-task timing shown by the plan's own deferral wording; missing collector tests (U-003) stay |
| C-002 (helper writes) | Variant 2 for coverage | Medium, not BLOCKING | High on the grade | Spec mandates the call (`source.md:299`); dry run defined as no removal (`source.md:256`); fetch only on MERGED (`branch-landed.sh:182`) |
| C-003 (patch and bundle) | Variant 2 for coverage | Medium, not BLOCKING | Medium-high | Aside only (`source.md:214`); verb definition, section 7 steps, acceptance list and build list omit it; plan discloses it (`PLAN:25`, `:170`) |
| C-004 (pull-request step) | Variant 2 | BLOCKING (Missing) | Medium-high | `source.md:276`, `:379`; absent from `PLAN:263-274` |
| C-005 (14 vs 15 rows) | Variant 1 | BLOCKING (wrong number in an acceptance check) | High | 15 rows at `source.md:314-328`; plan says 14 at `PLAN:253`, `:256` |
| C-006 (Task 1 fallback) | Variant 1 | BLOCKING (Decision: removal path and the proofs record) | Medium-high | `source.md:297` vs `:298`, `PLAN:33`, `source.md:374` |
| C-007 (coverage matrix) | Neither | n/a | High | Both cards cut off before it |
| X-001 (helper call a blocking safety problem?) | Neither card fully; variant 2 closer on coverage | Medium | High | Variant 2's own advocate reframed it as a requirement conflict, not destructive behaviour |
| X-002 (dependency extent) | Variant 1, plus variant 2's Task 7 | as C-001 | High | Union of both lists |
| A-001 (per-task checking) | QUALIFY | | High | Per-task timing holds (plan deferral wording, per-task acceptance blocks); declared deferrals are not defects |
| A-002 (BLOCKING applied equally) | QUALIFY | | High | Variant 1's three grades meet the rule; variant 2's F1 and F4 meet it, F2 and F3 are Medium; FAIL stands on C-001, C-004, C-005, C-006 |

Additional item for the calibrator, raised by neither card: Task 1 proves item 3 with MERGED and NONE, while the spec asks for a merged and an open pull request (`source.md:299` vs `PLAN:33`, `:37`); BLOCKING under the literal acceptance-check clause, small in practice.
