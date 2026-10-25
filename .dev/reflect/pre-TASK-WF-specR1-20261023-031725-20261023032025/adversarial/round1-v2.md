## Position summary

Variant 2 is right that this plan is not ready, and right that three low card claims are not defects. It is wrong about how serious its own top two findings are, and it missed the two medium checks that actually fail a correct run or pass a wrong edit.

## Steelman of Variant 1

Variant 1 is the more complete card. It walks Tasks 5–9 in both directions and maps prior findings M-01 through M-18 in its self-audit. The two findings Variant 2 never filed are the ones that matter. Task 1 hashes every status-listed path outside the allow-list (`TASK-WF-specR1-20261023-031725.md:37`), and Task 9 then requires those hashes to be identical (`:183`) with no exemption for `.dev/reflect/`, `.dev/troubleshoot/`, or `.dev/workflow/`. Source exempts tooling paths only from the status comparison (`source.md:70`). A file already dirty under those roots, rewritten while the run is otherwise correct, fails `cmp`. Separately, the `gh pr list` acceptance locks `--repo` on every `gh pr` line and locks `--head` only on `gh pr create` (`TASK-WF-specR1-20261023-031725.md:128`). The stub prints a scripted count whatever arguments it gets (`:129`), so dropping `--head sync/framework` still passes runs (a)–(d). Source requires that head (`source.md:11`). Variant 1 also sees the trap in the dependency rule: `source.md:82` says Task 7 depends on the Codecov research task, not on the sync task, so a single-parent chain cannot contain both Task 6 and Task 7 without making one an ancestor of the other. The heredoc residual on the `<` check, the fail-closed reading of push-before-list, and the contract3 example for the directory scope hole are careful readings, not padding.

## Strengths claimed

1. The ancestor gap is literal. Task 8 depends on Task 7 (`TASK-WF-specR1-20261023-031725.md:153`), Task 7 on Task 2 (`:138`), Task 2 on Task 1 (`:46`). Task 5 depends on Task 4 (`:79`) and Task 6 on Task 3 (`:112`). Tasks 3–6 are not ancestors of Task 8 or Task 9. `source.md:82` requires the documentation and final-scope `Depends on` line to name a task that already has the earlier edits as ancestors. `TASK-WF-specR1-20261023-031725.md:31` saying tasks run in number order does not create that chain. `source.md:40` says to make real chains where order matters.
2. C3 is not a plan defect. `source.md:55` requires the `::warning` line to contain the word `advisory` and not contain `before merge`. Task 5's acceptance check does that (`TASK-WF-specR1-20261023-031725.md:96`). The current line is the one being replaced (`boundary-guard.yml:50`). A reword that omits `advisory` is a wrong edit under the source, not a correct edit the check unfairly fails.
3. The job-name check forbids the substring `required` (`TASK-WF-specR1-20261023-031725.md:95`). `source.md:23` forbids a file-wide search for that word because the checklist heading contains it. `source.md:55` does not ban it on the job name. `ci.py:19` and `ci.py:77` only require the name to contain `boundary`. An advisory name such as "not required" fails a correct edit. The current name is `Mechanical-merge boundary touched -- human review required` (`boundary-guard.yml:37`).
4. Task 7 says not to edit Task 2's file (`TASK-WF-specR1-20261023-031725.md:140`). The only acceptance check is that the `Decision:` count is still 1 (`:147`). `source.md:69` forbids appending to that file. An appended note with no second `Decision:` line passes. Variant 1 marked INF-057 covered. That is wrong.
5. On renames, recording both paths is not enough unless a new path outside the allow-list fails the scope check. `source.md:70` says renamed paths are recorded explicitly so they can fail. Variant 2 states that failure. Variant 1 stops at "emit both lines."

## Weaknesses in Variant 1

1. `ready_with_notes` contradicts Variant 1's own mediums. Cycle 1 was not ready on medium acceptance defects with zero highs (`source.md:51`, `source.md:53`, `source.md:67`). R1-1 and R1-2 are that same class.
2. R1-7 calls a reword without the word `advisory` correct. `source.md:55` says it is not. The check at `TASK-WF-specR1-20261023-031725.md:96` is the spec.
3. R1-12 says Task 9's positive check would catch a premature run. That check (`TASK-WF-specR1-20261023-031725.md:185`) does not gate Task 8. Task 8's acceptance (`:163-168`) never reads the workflow files, so a README written before Tasks 5 and 6 still passes.
4. R1-9 adds `scripts/README.md:30`. `source.md:81` names the leftover lines and does not include line 30. Line 30 is about retired local scripts and `uv build`, not the publish-pypi paragraph at lines 7–12. The plan's list (`TASK-WF-specR1-20261023-031725.md:176`) follows the source. Adding line 30 expands the spec.
5. R1-8 treats Task 9's "the comment is correct" as premature. `source.md:80` already tells Task 9 to record that conclusion and to have the user confirm it. The plan does both (`TASK-WF-specR1-20261023-031725.md:176`).
6. R1-3 requires a whole-document compare for `boundary-guard.yml`. `source.md:57` requires that compare for pull-sync and test.yml only. `fetch-depth: 0` (`boundary-guard.yml:43`) is unprotected, and that risk is real, but it is not the M-10 requirement.

## Concessions

- Variant 2 missed R1-1 and R1-2. Those are the strongest mediums in either card. The hash bug is limited to paths already listed in the baseline status, not every file on disk under those roots (`TASK-WF-specR1-20261023-031725.md:37`), but for those paths it is real.
- Variant 2's example chain (Task 6 after Task 5, Task 8 after Task 6, Task 7 kept on Task 2) drops Task 7 from Task 8's ancestors. Task 8's Codecov bullet needs Task 7 (`TASK-WF-specR1-20261023-031725.md:157`). A chain that puts Task 6 and Task 7 in one line makes Task 7 depend on the sync task, which `source.md:82` forbids.
- R2-2 over-claims. `source.md:39` and `source.md:70` set the final check at directory level. `TASK-WF-specR1-20261023-031725.md:184` follows them. The contract3 risk (`source.md:46-47`) is real and low. Medium was wrong.
- Variant 2's self-audit says it checked M-01 through M-18 in one sentence. Variant 1 actually maps them. On coverage of prior findings, Variant 1 wins.
- R2-6 stops at "zero `<` characters" and misses Variant 1's heredoc false-fail. The commit step today has no `<` (`pull-sync-framework.yml:88-112`). A correct `<<` body would fail `TASK-WF-specR1-20261023-031725.md:128`. `source.md:75` is about placeholders surviving into commands, not about every `<` byte.

## Shared assumptions (A-001..A-003)

- A-001: REJECT. `TASK-WF-specR1-20261023-031725.md:31` asserts number order. `source.md:40` and `source.md:82` require the Depends graph itself. Neither card showed a runner that makes number order a safe substitute. Calling the gap "not a runtime hazard" is the assumption, not a fact.
- A-002: ACCEPT. The extracted commit step calls bare `git` only (`pull-sync-framework.yml:89-109`). No `command git`, no absolute git path. A PATH stub that execs the real git for every subcommand other than `push` matches this body.
- A-003: QUALIFY. No high finding is correct: neither card filed one. "Medium fixes applied, every spec item is met" is not. R1-1 and R1-2 are still open against `source.md:70` and `source.md:11`, and no single-parent chain satisfies both sentences of `source.md:82`.

## Per-point positions

| Point | Winner | Evidence |
|---|---|---|
| S-001 | V1 | V1 maps M-01..M-18; V2's self-audit is one sentence (`variant-2-original.md:129` vs `variant-1-original.md:196`). |
| C-001 | V2 | `source.md:39` and `:70` set a directory check; `TASK-WF-specR1-20261023-031725.md:184` follows it. Contract3 (`source.md:46`) is a low residual, not a medium spec break. |
| C-002 | V2 | Task 8's ancestors are 7, 2, 1 only (`:153`, `:138`, `:46`). `source.md:82` requires 5 and 6 in that set. V1's log bullet does not create ancestors. |
| C-003 | tie | V1's old-path `MISSING` rule fits `source.md:70`; V2's out-of-allow-list new path is what makes the check fail. Each card lacks the other's half. |
| C-004 | V2 | `source.md:55` requires the word `advisory`; `TASK-WF-specR1-20261023-031725.md:96` enforces it. Omitting the word is a wrong edit. |
| C-005 | V1 | Both want zero `<`. Only V1 names the `<<` heredoc false-fail against a base step that has no `<` (`pull-sync-framework.yml:88-112`). |
| C-006 | tie | Both accept C5. Standalone assignment (`TASK-WF-specR1-20261023-031725.md:117`) and run (d) (`:133`) match `source.md:65`. |
| X-001 | V2 | Not ready. V1's own R1-1 and R1-2 are the medium class `source.md:51` already refused. V2 reached the right verdict for the weaker reasons. |
| X-002 | V2 | The ancestor miss is real, so "optional" is wrong. Medium is the top of the range: the fix cannot be a naive re-chain without breaking `source.md:82`'s first sentence. |
| X-003 | V2 | C3 is not a defect. The acceptance check is the spec (`source.md:55`, `TASK-WF-specR1-20261023-031725.md:96`). |