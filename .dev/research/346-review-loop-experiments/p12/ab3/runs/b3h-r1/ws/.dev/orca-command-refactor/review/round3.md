review: 3 of 3

# /sc:spec-panel critique report, round 3 (re-review)

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture --re-review .dev/orca-command-refactor/review/round2.md --baseline .dev/orca-command-refactor/specs/history/spec-v2.md`
- Prompt: RE-REVIEW prompt, read in full from the sandbox home copy of `~/.claude/rules/prompts/document_review_loop_prompts.md` (lines 38-51 for the prompt, 42-47 for the roles and Step 1).
- CANDIDATE: `specs/orca-worker-contract-spec.md`, sha256 `2a0ba05dc4158ae8fc6c4b9c265ce2ded840533c29031835d61d7c548122ac84`, 285 lines.
- BASELINE: `specs/history/spec-v2.md`, sha256 `e1f78b891d8bb255eebfc49ad5aa8456501e35c3ff87d61c58e99699e8350b62`, 285 lines. This is the text round 2 reviewed as its CANDIDATE (`review/round2.md:7`).
- PRIOR: `review/round2.md`, sha256 `534e61b63a29ca3fd86367717928ef983f3d3d98aeddd7132afd66fd194599b0`, header `review: 2 of 3` (`review/round2.md:1`). N is therefore 3.
- Reviewer model: claude-haiku-5-5 (Haiku 5.5), fresh context. The prior report was read as data.
- rf-qa.md: neither `.claude/agents/rf-qa.md` in the workspace nor `~/.claude/agents/rf-qa.md` in the sandbox home exists. Fix-cycle steps 1-5 could not be read, so the command's Review Loop rules stand alone.
- Cap check: the prior header is `review: 2 of 3` with `verdict: FAIL`, which is below the cap of 3 (`command.md:261`), so this review runs. It is the last review of this loop. Any blocking finding left open escalates to the user; no fourth review is run.
- Mode: re-review only. Nothing edited. Only this file was written.

## Coverage and verification limits

- Read in full: the candidate `specs/orca-worker-contract-spec.md:1-285`; the prior report `review/round2.md:1-167`; `README.md:1-39`; the prompts file (lines 1-69); the sandbox `command.md` review rules (`:256-265`), unattended section (`:455-465`) and spec-panel flags (`:22-26`).
- Baseline: compared with the candidate by `diff -w`. The two files have the same 285 lines and differ only at `:146`, `:182` and `:194`. Those three baseline lines were read in full.
- Inventory citations checked: `inventory/commands-a.md:35,60-61`; `inventory/commands-b.md:49,52,177-185,267-275`; `inventory/orca-capabilities.md:73,76-79`.
- UNVERIFIED: `src/superclaude/core/HOW-WE-WORK.md:171,249,254` (cited by SA-1 at `specs/orca-worker-contract-spec.md:146`; not in the workspace); `.dev/codegraph-migration/...` (cited at `:23` and `:194`; not in the workspace); every `cmd/` and `sk/` path. What `REPORT.md` contains is UNVERIFIED (see R3-03).

## Step 1: evidence block

`diff -w BASELINE CANDIDATE` gives three changed hunks: `146c146`, `182c182`, `194c194`. Changed lines are copied verbatim below.

BEFORE (baseline), lines starting `<`:

```text
< | SA-1 | Without `--unattended`, every prompt, approval gate, default flag value, output path and outward default stays as it is today, including the auggie-review PR posting default and every `AskUserQuestion`. | The routing guide sends people to these commands with these behaviours today (for example `--interactive` controls on cleanup and improve, interactive suite selection on cli-eval). | `src/superclaude/core/HOW-WE-WORK.md:171,249,254` |
< 3. `ORCA orchestration check --wait --types "worker_done,escalation,question" --timeout-ms 900000 --json` until `worker_done` arrives. **Pass:** exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path.
< | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-3 and 5-7 pass, with two P0 substitutes: in step 3 the report path is the file the command already writes and step 4 checks (troubleshoot `REPORT.md`, `INV-B:49`; workflow `return-contract.yaml`, `INV-B:52`; adversarial's contract, `INV-A:35,60`), since the WC-4 path arrives in P1; and step 4 runs only `test -s`, since the YAML assertion applies from P1 (`REPORT.md` is Markdown). Record the results in the phase report; a failure here reopens section 1 |
```

AFTER (candidate), lines starting `>`:

```text
> | SA-1 | Without `--unattended`, every prompt, approval gate, default flag value, output path and outward default stays as it is today, including the auggie-review PR posting default and every `AskUserQuestion`, except the two standalone file changes that SA-3 names (F-03). | The routing guide sends people to these commands with these behaviours today (for example `--interactive` controls on cleanup and improve, interactive suite selection on cli-eval). | `src/superclaude/core/HOW-WE-WORK.md:171,249,254` |
> 3. `ORCA orchestration check --wait --types "worker_done,escalation,question" --timeout-ms 900000 --json` until `worker_done` arrives. **Pass:** exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5 (R2-01: waived for troubleshoot in P0, because its `REPORT.md` has no `status` field, `INV-B:49`); its report path is the WC-4 contract path.
> | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-3 and 5-7 pass, with two P0 substitutes and the step 3 outcome waiver for troubleshoot (R2-01): in step 3 the report path is the file the command already writes and step 4 checks (troubleshoot `REPORT.md`, `INV-B:49`; workflow `return-contract.yaml`, `INV-B:52`; adversarial's contract, `INV-A:35,60`), since the WC-4 path arrives in P1; and step 4 runs only `test -s`, since the YAML assertion applies from P1 (`REPORT.md` is Markdown). Record the results in the phase report; a failure here reopens section 1 |
```

Changed lines by location (candidate line numbers): SA-1 `:146`, AC-0.4 step 3 `:182`, AC-0.4 row `:194`.

## Self-check (run before the verdict)

`grep -nF` was run for each quoted line, using its first 120 characters. Each AFTER quote was found in CANDIDATE at `:146`, `:182` and `:194`. Each BEFORE quote was found in BASELINE at `:146`, `:182` and `:194`. Roles were not swapped. This check is a prefix match, not a full-line match.

## Prior blocking findings (round 2 table, re-checked)

| id | round 2 status | round 3 status | evidence |
|---|---|---|---|
| F-01 | resolved | resolved | WC-4 (`specs/orca-worker-contract-spec.md:62`), init-lite (`:87`) and tdd (`:90`) are unchanged against this baseline. The file-valued directory rule still holds. Residual R2-02, R2-03 carried (see below). |
| F-02 | resolved | resolved | WC-4 (`:62`) names `--report-dir`, and §3.2 (`:120`) gives `<report-dir>/return-contract.yaml`. The sandbox `command.md:459-461` defines `--report-dir <dir>`, so the name matches. Both lines unchanged. Residual R2-05 carried. |
| F-03 | open | resolved | SA-1 (`:146`) now excepts "the two standalone file changes that SA-3 names". SA-3 (`:148`, unchanged) names the adversarial fixed name and the workflow contract. The adversarial row (`:83`, unchanged) is the change that SA-1 now excepts. The three texts list the same change. See the note on wording in m-04. |
| F-04 | resolved for the named defect | resolved | The step 3 outcome clause at `:182` is now handled by the R2-01 waiver. The P0 substitutes at `:194` are unchanged apart from the waiver cross-reference. |
| F-05 | resolved | resolved | AC-C1 (`:172`) is unchanged against this baseline. It still uses one `-e` per alternative. |
| F-06 | resolved for the two named cases | resolved | WC-11 (`:69`), §2.3 (`:73`) and init-lite (`:87`) are unchanged against this baseline. Residual R2-04 carried. |
| R2-01 | open (blocking) | resolved | `:182` now waives the outcome clause for troubleshoot in P0, by name, and gives the reason. `:194` cross-references the waiver. Step 3 for troubleshoot can now be evaluated. Residual: R3-03 (minor). |

Regressed: none. No prior blocking finding is regressed.

### F-03 (resolved)

- Round 2 required that SA-1, SA-3 and the adversarial row (`:83`) list the same set of changes, either by naming the adversarial exception in SA-1 or by gating the fixed name behind `--unattended`.
- The candidate took the first route. SA-1 (`:146`) excepts "the two standalone file changes that SA-3 names". SA-3 (`:148`) names the adversarial fixed name (`INV-A:35`) and the workflow contract. The adversarial row (`:83`) moves the standalone contract path, which SA-1 now excepts through the SA-3 reference.
- An implementer who reads SA-1 and then `:83` gets the same result: the adversarial contract path changes in a standalone run.

### R2-01 (resolved)

- Round 2 found that step 3 (`:182`) required a `status` match that a troubleshoot `REPORT.md` cannot supply (`commands-b.md:49` lists `REPORT.md` as the report and no contract).
- The candidate waives the outcome clause for troubleshoot in P0 by name (`:182`). The waiver is scoped to P0 and does not cover workflow or adversarial. Adversarial's position is open; see R3-01.

## Findings on changed lines (origin=changed)

### R3-01 (Medium): adversarial's P0 outcome check needs a `status` field the inventory does not show

- `specs/orca-worker-contract-spec.md:182` still requires, for the P0 run, that `--outcome` match "the contract's `status` under WC-5". The waiver at `:182` and the substitutes at `:194` cover troubleshoot only.
- The adversarial contract is the one `:194` checks. `inventory/commands-a.md:35` says the skill "names no filename" and lists no fields for the contract. Nothing in the workspace shows that it carries a `status` key. By contrast, the workflow contract is recorded with `status`, `plan_path` and `reflect_report_path` (`inventory/commands-b.md:272`, citing `sk/sc-workflow-protocol/refs/return-contract.md:3-19`).
- Grading check: an implementer who runs the adversarial P0 smoke test and finds no `status` key cannot evaluate the outcome clause, so the step is neither passed nor failed. That holds only if the existing contract lacks `status`, which the workspace does not show (UNVERIFIED). It needs that assumption, so it is Medium, not blocking.
- Recommendation: either check adversarial's P0 outcome against the body's first sentence, which WC-5 (`:63`) already requires, or waive the clause for adversarial in P0 by name, as R2-01 did for troubleshoot.

### R3-02 (Medium): the adversarial P0 report path is not known before dispatch

- `:194` substitutes "the file the command already writes" for the WC-4 path in step 3, and step 4 checks "adversarial's contract, `INV-A:35,60`".
- `inventory/commands-a.md:35` records real runs writing `<output>/adversarial/return-contract.yaml` and, in some runs, `<output>/adversarial/adversarial/return-contract.yaml`. The §3.1 adversarial row (`:83`) fixes the name only in P1. §2.3 (`:73`) requires the report path to be known before dispatch, and P0 cannot meet that for adversarial.
- Grading check: an implementer who runs `/sc:adversarial --compare <two files> --depth quick --output <dir>` must guess which of the two recorded locations the run used before step 4's `test -s` can run. That needs an assumption, so it is Medium.
- Recommendation: state how the P0 check locates the file, for example by finding the `return-contract.yaml` under `<dir>` and requiring exactly one match, or defer the adversarial path check until P1.

### R3-03 (minor): the troubleshoot waiver removes the only outcome check in P0

- `:182` waives the outcome clause for troubleshoot in P0. The waiver is named and the step is evaluable, so this is not blocking. A troubleshoot run whose body says failed but whose `--outcome` is succeeded passes P0 with no check. WC-5 (`:63`) already requires the first sentence of the body to state status and verdict, which could serve.
- The rationale "its `REPORT.md` has no `status` field, `INV-B:49`" cites `inventory/commands-b.md:49`. That line lists `REPORT.md` as the report and shows no return-contract column. It does not describe what `REPORT.md` contains, so the rationale is UNVERIFIED.
- Minor, because the waiver is explicit and no implementation produces a wrong outcome from it.

### m-04 (minor, carried; now a dependency of changed line `:146`)

- SA-1 (`:146`) calls both SA-3 items "two standalone file changes". The second, the workflow pre-creation STOP contract, is written only under `--unattended` (`:148`, and the workflow row at `:92`). In a standalone run it is not a file change at all.
- Harmless: no outcome changes, because a standalone run writes nothing there either way. Drop the word "standalone" from SA-1, or drop the second item from the list.

### m-05 (minor): review ids in normative text

- `:146`, `:182` and `:194` carry review ids (`F-03`, `R2-01`) inside normative spec text. Those ids mean something only to this loop and go stale once it closes. Keep them in the review files and remove them from the spec body.

## Findings on unchanged lines (origin=unchanged)

Carried from round 2 (`review/round2.md:91-124`). Their text is unchanged against this baseline (spec-v2), and none quotes a changed line that depends on it. Under the re-review rule (`command.md:262`, step 5) each is a minor note, not blocking. Listed under follow-up candidates.

- R2-02: WC-4 (`:62`), "written on every outcome" against "refused ... writes nothing".
- R2-03: WC-4 (`:62`), init-lite (`:87`) and tdd (`:90`), two dispatches sharing one directory and one contract name.
- R2-04: WC-11 (`:69`) and §2.3 (`:73`), a sequential retry of a fixed-path command.
- R2-05: §3.2 spec-panel row (`:120`), "add the directory flag" against the existing `--report-dir`.

Round 1 items F-07 to F-15 and m-01 to m-03 were not re-examined here, as in round 2.

## Guard Condition Boundary Table (changed guards only)

Triggered by the changed exception list (`:146`), the outcome waiver (`:182`) and the P0 substitutes (`:194`). Pipeline Dimensional Analysis is not triggered: the changed lines contain no multi-stage count flow.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| standalone exception list | SA-1 `:146` with SA-3 `:148` and row `:83` | Typical: standalone adversarial run, no `--unattended` | contract path | path changes | SA-1 excepts it through SA-3 | OK (F-03 resolved) |
| standalone exception list | SA-1 `:146` with SA-3 `:148` and row `:92` | Legitimate edge: standalone workflow run that stops before creation | no `--unattended` | nothing written | SA-3 limits the contract to `--unattended`; SA-1's "standalone file change" label is wrong | OK (m-04, minor) |
| outcome | `:182` | Typical: troubleshoot P0, `REPORT.md` | no contract `status` | cannot be evaluated | waived by name | OK (R3-03, minor on the rationale) |
| outcome | `:182` | Legitimate edge: adversarial P0 | contract `status` not shown in the inventory | cannot be evaluated | clause still in force, not waived | GAP (R3-01, Medium) |
| report path | `:194` | Legitimate edge: adversarial P0 | path varies (`INV-A:35`) | "the file the command already writes" with no locating rule | not specified | GAP (R3-02, Medium) |
| report path | `:194` | Typical: workflow P0 | `return-contract.yaml` (`INV-B:52`) | `test -s` | stated | OK |

## Summary

- Prior blocking: F-01, F-02, F-04, F-05 and F-06 are resolved, with no change at their lines. F-03 is resolved by the change at `:146`. R2-01 is resolved by the change at `:182` and `:194`. None is open or regressed.
- New blocking findings: none.
- Medium (follow-up): R3-01, R3-02.
- Minor: R3-03, m-04, m-05, and the unchanged-origin notes R2-02 to R2-05.
- Open blocking findings: none.
- Coverage line: scoped PASS: changed lines + prior blockers
- Reviser brief: none. Review 3 with no open blocking finding writes no brief.
- Whole-document assurance is not covered by this scoped PASS. The GATE prompt (`~/.claude/rules/prompts/document_review_loop_prompts.md`, lines 57-64) is run once after the loop's PASS, in a fresh context, as a separate gate review. This run did not run it.

## Follow-up candidates (Medium and minor, not blocking)

R2-02, R2-03, R2-04, R2-05, m-04, m-05, R3-01, R3-02, R3-03. Round 1 items F-07 to F-15 and m-01 to m-03 remain follow-up candidates and were not re-graded. The session that ran this review asks the user once whether to open an issue for them. None is created without the user's answer.

## Decisions made by this reviewer

| Decision | Options | Rationale |
|---|---|---|
| Review number | `review: 3 of 3` | Prior header `review: 2 of 3` plus 1 (`command.md:261`; prompt line 48). |
| F-03 | resolved / open | SA-1 now names the SA-3 set, so SA-1, SA-3 and `:83` list the same change. |
| R2-01 | resolved / open | The waiver at `:182` is explicit, and `:194` cross-references it. The step can be evaluated for troubleshoot. |
| R3-01, R3-02 | Medium / blocking | Each needs an assumption the workspace does not settle (whether the adversarial contract has `status`; which of two recorded paths a run uses). Medium. |
| R3-03 | minor / Medium | The waiver is explicit and produces no wrong implementation. Minor. |
| Unchanged-origin items | minor note / Medium | Their text is unchanged against this baseline and none quotes a changed dependent line, so they are minor notes under the re-review rule. |
| Ids | prior ids kept; new `R3-nn`, `m-05` | Each finding keeps its prior id; new findings get new ids, per the re-review output rule. |

verdict: PASS
