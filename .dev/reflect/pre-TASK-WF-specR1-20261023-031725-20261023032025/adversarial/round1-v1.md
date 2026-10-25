## Position summary

Variant 1 (reviewer-1) is the stronger card on correctness and coverage. It is the only card that finds a way a correct run can fail the plan's own check (R1-1). I confirmed it: 48 untracked `.dev/reflect/` entries already sit in the git status baseline, and Task 1 hashes them (`TASK-...md:37`). It also finds the missing `gh pr list` argument check (R1-2) and the missing boundary-guard.yml whole-document comparison (R1-3). It audits the earlier M-01..M-18 findings, and it handles `-z` rename order correctly where Variant 2 gets it wrong.

Variant 2 is right on one thing Variant 1 under-rated. Source line 82 is not met literally by the Depends-on graph. I also concede that "ready_with_notes" understates Variant 1's own R1-1.

## Steelman of Variant 2

- **Source-literal reading of the Depends-on rule.** `source.md:82` asks that the last tasks' single `Depends on:` line "names a task that already has the earlier edits as ancestors". Task 8 depends on 7, which depends on 2, which depends on 1 (`TASK-...md:138,153`). Task 9 depends on 8. Tasks 3, 4, 5 and 6 are never ancestors. The plan covers this with prose at line 31 and in the task bodies. R2-1 treats that as a deviation from the written rule, and its recommendation, re-chaining, is concrete.
- **Cheap, mechanical fixes.** R2-5 hashes `t2-codecov-v4.md` before and after Task 7. R2-3 adds a rename rule.
- **C3 rejection is defensible.** `source.md:55` makes the word `advisory` a check on the warning line, and `TASK-...md:96` enforces it. Failing an executor who omits the word is the intended behaviour.
- **A decisive verdict.** "not_ready" reflects that at least two medium items need edits before execution.

## Strengths claimed

1. **R1-1: a correct run can fail Task 9.**
   - Task 1 hashes every baseline path outside the allowed folders (`TASK-...md:37`).
   - The tooling-output exemption (`:25`) is applied only to the status comparison (`:184`). The hash `cmp` at `:183` has no such exemption.
   - `git status --porcelain -uall -z` shows 48 `.dev/reflect/` entries in the baseline, so the exposure exists.
   - The reviewer-2 calibrator independently raised the same risk (`diff-analysis.md:8`).
2. **R1-2: nothing fails a `gh pr list` that has lost its filters.** The checks at `:128-133` require `--repo` on every `gh pr` line, but `--base` and `--head` only on `gh pr create`. The stub prints a scripted count whatever arguments it gets, so all four stub runs would pass. `source.md:10-11` fixes head and base. Variant 2 does not raise this.
3. **R1-3: no whole-document comparison for boundary-guard.yml.** Tasks 6 and 7 have one (`:125`, `:146`); Task 5 (`:93-106`) does not. Edits to `runs-on`, the `env` mapping, or the checkout `fetch-depth: 0` (`boundary-guard.yml:38-48`) would pass every Task 5 bullet. The local render sets `BASE_SHA` and `HEAD_SHA` by hand, so it cannot catch them.
4. **R1-6: rename handling is correct.** It says a rename yields the new and old path, each on its own line, with the old path recorded as `MISSING` if it no longer exists. Under `-z`, git emits the new path first, then the old one. Variant 2's R2-3 says "status, then old path, then new path", which reverses the order.
5. **R1-10: the `<` check is verified, not assumed.** I counted `<` in the base `pull-sync-framework.yml` and got 0. It also names a real residual risk: writing the PR body as a heredoc would put `<<` in the file.
6. **R1-4 matches R2-2.** Both find that the Task 9 scope check accepts any path under `.github/workflows/` (`:184`).
7. **Prior-finding audit.** Variant 1's self-audit accounts for M-01..M-18, including partial coverage of M-05 and M-10. Variant 2 has no equivalent.
8. **R1-5 (Decision-line format).** `files` contains `file`, so "names exactly one of `file` or `files`" (`:52`) is ambiguous. Variant 2 does not raise it.

## Weaknesses in Variant 2

1. **Wrong `-z` rename order in R2-3.** It prescribes "old path, then new path". With `-z`, git puts the new path first.
2. **It misses R1-1, R1-2 and R1-3.** The first two are cases where a wrong edit or a correct run gets the wrong verdict.
3. **R2-8 is outside the tasklist.** It corrects the coverage matrix, which is a reflect artifact, not a flaw in the plan under review.
4. **R2-7 dismisses C3 too fast.**
   - Line 84 says "advisory wording", while line 96 demands the literal word `advisory`.
   - An executor who writes "recommended" would follow line 84 and fail line 96.
   - Variant 2 itself suggests the optional fix.
5. **R2-4 is stricter than the source.**
   - The job-name check at `:95` forbids the bare substring `required`, which would reject a valid name such as "advisory, not required".
   - `ci.py:19,77` match only on `boundary`.
   - `source.md:55` forbids the old phrase only on the warning line and the header, not on the job name.
   - It is a valid low point, but it fixes a defect Variant 1's version of the check does not need.
6. **"not_ready" rests on C6 plus mediums.** The Depends-chain finding is real, but the plan is not wrong about order. It is only unproven by the dependency graph.

## Concessions

- **Variant 2 is right on the Depends-on rule.**
  - I confirmed Task 8's ancestors are only 7, 2 and 1 and Task 9's are 8, 7, 2 and 1. Strictly, `source.md:82` is not met.
  - Variant 1 reached the same factual conclusion in R1-12 and still rated it low and optional.
  - Variant 1's mitigation (a precondition check on the t5, t6 and t7 logs) is weaker than a real chain.
- **Variant 1's verdict label is inconsistent with its own R1-1.** A plan where a correct run can fail the final check is arguably not ready until fixed.
- **R1-7 overstates.** The header instruction (`:82`) and the summary instruction (`:85`) already contain "advisory". Only the warning-line instruction at `:84` lacks the literal word.
- **R1-8 and R1-9 are weak.** The calibrator rated both low; R1-8 follows `source.md:80`.
- **R2-5 is a good catch.** Variant 1 missed it.
- **Variant 2 recommends making the Depends chain explicit, and that is the better fix.** Source line 40 also says "make real chains where order matters".

## Shared assumptions

- **A-001 (tasks run in number order): QUALIFY.** `/sc:implement` resuming at the first unfinished step is plausible, and line 31 states it. But a plan whose ordering rests only on a prose rule is exactly what source line 82 tried to avoid. Either add a real chain or add an explicit precondition check on the earlier logs.
- **A-002 (PATH-stubbed `git` works): ACCEPT.** The extracted body calls bare `git` (`pull-sync-framework.yml:89-109`), with no `command git` and no absolute path. The stub (`TASK-...md:129`) passes everything except `push` to the real git by absolute path. One residual risk: the body uses `date` and `git commit`, so the temp repo must have identity set, which `:129` requires.
- **A-003 (no finding is high): QUALIFY.** The severity taxonomy supports "no high". But R1-1 can stop a correct run at the last task, and the claim that the plan meets every spec item after fixes depends on R1-1, R1-2, R1-3 and the chain issue all being fixed.

## Per-point positions

| point | winner | one-line evidence |
|---|---|---|
| S-001 | V1 | V1's M-01..M-18 audit and wider finding set beat V2's smaller scope; count alone is not merit |
| C-001 | tie | Same defect and fix; `:184` allows any workflow path while `source.md:6` lists four. `source.md:39` is directory-level, so low-to-medium |
| C-002 | V2 | Source line 82 needs ancestors; Task 8's chain stops at 7→2→1 (`:138,153`). V1's optional check is weaker |
| C-003 | V1 | V1 gets `-z` order right (new then old) and keeps MISSING for old; V2 states the order backwards |
| C-004 | V1 (narrow) | `:84` says "advisory wording" but `:96` needs the literal word; V1 overstates for header and summary |
| C-005 | V1 | Base has 0 `<` characters (verified); V1 adds the heredoc risk |
| C-006 | tie | Both accept fail-closed; V1 traces run (d) at `:133`, but there is no disagreement on outcome |
| X-001 | tie | "ready_with_notes" understates V1's own R1-1; "not_ready" rests partly on a nominal chain issue and the lone pure-correctness block is R1-1 |
| X-002 | V2 | `source.md:82` is not literally met by the Depends graph; low-and-optional undersells it |
| X-003 | V1 (narrow) | The `:84` versus `:96` mismatch is real but low-severity; V2 is right the check itself is correct |

Files read: `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/tasks/to-do/TASK-WF-specR1-20261023-031725/TASK-WF-specR1-20261023-031725.md`, `source.md` beside it, `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.github/workflows/boundary-guard.yml`, `pull-sync-framework.yml`, and the three adversarial files under the `D` path.