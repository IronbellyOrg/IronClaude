review: 3 of 3

# Spec-panel critique: Orca worker-contract spec (re-review, review 3 of 3)

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture --re-review .dev/orca-command-refactor/review/round2.md --baseline .dev/orca-command-refactor/specs/history/spec-v2.md`
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `2d14bcd06b4ba445afa8a700e4b20d34af0ab4a0f9ac87d402e2488534d77270` (285 lines)
- baseline: `.dev/orca-command-refactor/specs/history/spec-v2.md`, sha256 `00cb7b63ea6019f358ead17f8b721ad6058432fb1bebc97218c1af92404e5038` (285 lines; the same hash `round2.md:7` recorded for the candidate it reviewed)
- prior report: `.dev/orca-command-refactor/review/round2.md`, sha256 `d50a04132db1174c239d6688b995f74b25068d60f477c632bab51de43d3af662`, header `review: 2 of 3` (N = 3)
- reviewer model: claude-haiku-5-5
- review-loop prompt: RE-REVIEW prompt in `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full at `/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab2/runs/b2h-r1/home/.claude/rules/prompts/document_review_loop_prompts.md:36-49`), followed in order: roles, Step 1, review number, self-check, then the brief.
- rf-qa.md: neither `.claude/agents/rf-qa.md` in the workspace nor `~/.claude/agents/rf-qa.md` exists in this sandbox (the sandbox home holds only `rules/`). The re-check therefore follows the rules of the command's Review Loop section alone (UNVERIFIED that the rf-qa.md fix-cycle steps 1-5 agree).
- Review-loop position: this is the third and last review (`review: 3 of 3`). No fix cycle is started by this report.
- Scope: the candidate differs from the baseline only at spec:182 and spec:194 (Step 1 below). Findings are on those lines, plus the prior blocking finding N2-01. Nothing else was re-reviewed.

## Step 1: evidence block

Command run from the workspace root: `diff -w .dev/orca-command-refactor/specs/history/spec-v2.md .dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. The two files have the same line count (285) and the changes sit on lines 182 and 194 of both (`182c182`, `194c194`). Changed lines, copied verbatim:

BEFORE (baseline):

```text
3. Repeat `ORCA orchestration check --wait --types "worker_done,escalation,question" --timeout-ms 240000 --json`, running step 2's `worker-show` before each repeat, until `worker_done` arrives (F-02: a 900 s wait would leave no `worker-show` for up to 15 minutes; 240 s keeps the 4-minute bound of WC-10). On `question`, the coordinator answers with `ORCA orchestration reply --id <message_id> --body "<answer>"` (CAPS:63) only with an answer the brief or the person has given; otherwise it asks the person and invents no answer. On `escalation`, it records the escalation verbatim in the phase report and keeps looping; only `worker_done` ends the loop. **Pass:** exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path.
| P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-3 and 5-7 pass. In P0, since the contract arrives in P1 (F-03): step 4 is `test -s <report>` on the file the command already writes, with no YAML parse (for `/sc:troubleshoot` that file is `REPORT.md`, a markdown report, `INV-B:242`); the YAML key check in step 4 applies from P1. Step 3's outcome check in P0 reads the outcome from the report's first status line, and the phase report records that line as found, since its format is UNVERIFIED (the troubleshoot report template is not in the inventories). Record the results in the phase report; a failure here reopens section 1 |
```

AFTER (candidate):

```text
3. Repeat `ORCA orchestration check --wait --types "worker_done,escalation,question" --timeout-ms 240000 --json`, running step 2's `worker-show` before each repeat, until `worker_done` arrives (F-02: a 900 s wait would leave no `worker-show` for up to 15 minutes; 240 s keeps the 4-minute bound of WC-10). On `question`, the coordinator answers with `ORCA orchestration reply --id <message_id> --body "<answer>"` (CAPS:63) only with an answer the brief or the person has given; otherwise it asks the person and invents no answer. On `escalation`, it records the escalation verbatim in the phase report and keeps looping; only `worker_done` ends the loop. **Pass:** exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path from P1; in P0 it is the command's own report file (N2-01, see AC-0.4).
| P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-3 and 5-7 pass. In P0, since the contract arrives in P1 (F-03): step 4 is `test -s <report>` on the file the command already writes, with no YAML parse, and that file is the P0 report path step 3 checks (N2-01) (for `/sc:troubleshoot` that file is `REPORT.md`, a markdown report, `INV-B:242`); the YAML key check in step 4 applies from P1. Step 3's outcome check in P0 reads the outcome from the report's first status line, and the phase report records that line as found, since its format is UNVERIFIED (the troubleshoot report template is not in the inventories). Record the results in the phase report; a failure here reopens section 1 |
```

Role check (self-check, `grep -nF` run before any finding): each AFTER fragment ("its report path is the WC-4 contract path from P1; in P0 it is the command's own report file" and "that file is the P0 report path step 3 checks (N2-01)") is found in CANDIDATE at lines 182 and 194. Each BEFORE fragment ("its report path is the WC-4 contract path." and "with no YAML parse (for") is found in BASELINE at lines 182 and 194. The roles are not swapped. Only these two lines differ; line 183 (general step 4) and line 183's text are byte-identical in both files.

## Prior blocking findings (from round2.md)

round2.md:109 marks the report `verdict: FAIL` with one blocking finding, N2-01, which round2.md:2 records as confirmed by VERIFY (`.dev/orca-command-refactor/review/verify-2.md:9,21`). Round 2 marked F-02 and F-03 resolved (round2.md:41-44); under the RE-REVIEW rule they are re-checked below as well, since a resolved finding that fails again is `regressed`.

| id | prior status | now | evidence |
|---|---|---|---|
| N2-01 (P0 gate AC-0.4 cannot pass: step 3 requires the WC-4 contract path, which P0 does not produce) | open, blocking (round2.md:51-58) | resolved | The defect was the step 3 path clause in P0 (spec-v2 spec:182) combined with AC-0.4 (spec:194) saying the contract arrives only in P1. The candidate adds a P0 rule to the clause itself: "in P0 it is the command's own report file (N2-01, see AC-0.4)" (candidate spec:182), and AC-0.4 now says that "that file is the P0 report path step 3 checks (N2-01)" (candidate spec:194). The WC-4 contract path still applies from P1, and WC-4 itself is scoped to "In unattended mode" (spec:62), which P0 runs do not use (spec:79, spec:158-159, verify-2.md:9). The clause is therefore satisfiable in P0 for `/sc:workflow` (the contract at spec:92 is the command's own file) and for `/sc:troubleshoot` (`REPORT.md`, spec:91). The adversarial case is not fully defined; see M2-04 below, which is Medium and does not block. |
| F-02 (7.2 heartbeat check cannot satisfy its own pass condition) | resolved (round2.md:41) | still resolved, not regressed | candidate spec:181 still pairs `worker-show` with waits; spec:182 still uses `--timeout-ms 240000` and runs `worker-show` before each repeat (unchanged from spec-v2 except the path clause). |
| F-03 (AC-0.4 applies a YAML contract check to a markdown report) | resolved (round2.md:44) | still resolved, not regressed | candidate spec:194 still states "with no YAML parse" for P0 step 4 and that the YAML key check "applies from P1". |

Regressed: none. Open prior blocking findings: none.

## Findings on changed lines

Changed lines are spec:182 and spec:194. Findings below are on those lines; each keeps its id from round2.md where it carries over.

### M2-04 (Medium, carried, now also on changed line spec:182): the P0 adversarial report path is not defined

- origin=changed (the path clause at spec:182 is on a changed line, and spec:194 names the same file).
- Texts. spec:182 (candidate): "in P0 it is the command's own report file". spec:194 (candidate): "step 4 is `test -s <report>` on the file the command already writes". spec:83 (adversarial row): "contract, but filename not fixed". The inventory says the same: `.dev/orca-command-refactor/inventory/commands-a.md:35` ("the skill names no filename; real runs wrote `<output>/adversarial/return-contract.yaml`, sometimes `.../adversarial/adversarial/return-contract.yaml`"), and `.dev/orca-command-refactor/inventory/orca-capabilities.md:60` ("Workers in the earlier Orca run wrote it in two different places").
- Sentence. An implementer who runs the P0 adversarial check follows spec:182 and spec:194 as written: the `worker_done --report-path` must equal "the command's own report file", but the spec does not say which of the two observed paths applies, so the implementer must guess between them.
- Grade: Medium. The guess is the implementer's choice between two readings the inventory records, so the finding is a missing definition, not a stated text that causes harm, and an acceptance criterion's pass depends on a guess. Per the grading rule this is a follow-up candidate, not blocking.
- Recommendation (not required for PASS): in spec:194, name the adversarial contract path the P0 check uses, or state that the check reads the path the command reports in its own output.

### M2-01 (Medium, carried, spec:182): no overall deadline on the escalation loop

- origin=changed (spec:182).
- Text: "On `escalation`, it records the escalation verbatim in the phase report and keeps looping; only `worker_done` ends the loop." No cap is stated.
- Grade: Medium (a missing restriction, not a stated text that causes harm). Follow-up candidate.

### M2-02 (Medium, carried, spec:182): delivery of a later answer to a pending question is undefined

- origin=changed (spec:182).
- Text: "On `question`, the coordinator answers with `ORCA orchestration reply --id <message_id> ...` only with an answer the brief or the person has given; otherwise it asks the person and invents no answer." The text does not say how the person's later answer reaches the worker or what the loop does while the question is pending. Reply mechanics are at `orca-capabilities.md:63`.
- Grade: Medium (undefined state). Follow-up candidate.

### M2-03 (Medium, carried, spec:194): P0 outcome from the first status line has no rule for an absent or unmapped status

- origin=changed (spec:194).
- Text: "Step 3's outcome check in P0 reads the outcome from the report's first status line, and the phase report records that line as found, since its format is UNVERIFIED". The text gives no pass rule when no status line exists or the status is outside the WC-5 outcomes.
- Grade: Medium (undefined edge case). Follow-up candidate.

### Minor notes

- N2-02 (minor, carried, origin=unchanged, depends on changed line spec:194): spec:183, the general step 4, still reads as a YAML check for every phase; the P0 relaxation lives only in spec:194. Note only.
- N3-02 (minor, origin=unchanged, depends on changed line spec:182): the P0 troubleshoot report path is written as `REPORT.md` (spec:91, spec:194), with no directory. The inventory gives the default location as `.dev/troubleshoot/<slug>-<timestamp>/` (`commands-b.md:242`, citing `cmd/troubleshoot.md:56`). Because the P0 brief passes no output directory (spec:91 lists only "no `--fix`"), the path is known only after the run, while spec:73 says the brief's output directory makes "the report path known before dispatch". The P0 clause can still be met by reading the path after the run, so this is a note.

## Guard Condition Boundary Table (guards on changed lines only, FR-8 to FR-10)

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| Step 3 pass, path clause, P0 troubleshoot | spec:182 | Typical: P0 run, `worker_done` arrives | report path `REPORT.md` (`commands-b.md:242`) | path equals the command's own report file | stated; directory known only after the run (N3-02) | OK |
| Step 3 pass, path clause, P0 workflow | spec:182 | Typical: P0 run, `worker_done` arrives | `.dev/tasks/to-do/<id>/return-contract.yaml` (spec:92) | path equals the command's own report file | stated | OK |
| Step 3 pass, path clause, P0 adversarial | spec:182, spec:194 | Typical: P0 run, output path not fixed | two observed paths (`commands-a.md:35`) | undefined which path applies | not stated | GAP (M2-04) |
| Step 3 pass, path clause | spec:182 | Zero/Empty: no report file written | none | pass clause fails, run fails | stated by `test -s` at spec:194 | OK |
| Step 3 question branch | spec:182 | Typical: `question` with no answer | `question` | asks the person | no rule for delivering the later answer or the pending state | GAP (M2-02) |
| Step 3 escalation branch | spec:182 | Maximum: escalation never resolves | `escalation` | keeps looping | no overall deadline | GAP (M2-01) |
| P0 outcome | spec:194 | Zero/Empty: no status line in the report | no status line | undefined | "recorded as found", no pass rule | GAP (M2-03) |
| P0 outcome | spec:194 | Sentinel: status outside the WC-5 outcomes | unknown status value | undefined | not stated | GAP (M2-03) |
| P0 step 4 | spec:194 | Zero/Empty: report missing or zero bytes | absent or 0 | `test -s` exits non-zero, run fails | stated by `test -s` | OK |

Rows left out: the step 2 pass at spec:181 is unchanged and was checked against the 240 s waits in spec:182 (the gap between `worker-show` calls is at most about 240 s, so no row is needed). Rows for guards on unchanged lines are not in scope for a re-review.

## Coverage

- Read in full: the candidate spec (285 lines), the baseline spec-v2 (diff-compared, changed lines only), round2.md, verify-2.md, the RE-REVIEW prompt (`home/.claude/rules/prompts/document_review_loop_prompts.md`), command.md, and the workspace README.
- Checked against the inventories in this workspace copy: `commands-a.md:35` (adversarial filename), `orca-capabilities.md:60` (two adversarial contract locations), `commands-b.md:242` (troubleshoot `REPORT.md` and default directory). Note: verify-2.md:5 says `commands-b.md` is not in the workspace; in this copy it is present (323 lines), so those citations were checked directly here.
- Not covered: the repository files the spec cites (for example `cmd/troubleshoot.md`, `sk/sc-adversarial-protocol/SKILL.md`), which are outside the sandbox (UNVERIFIED); the rf-qa.md fix-cycle steps (file absent, see header); and the unchanged parts of the spec outside the re-review scope.
- Not run: `make verify-sync`, `uv run pytest`, and any Orca command (no repository or Orca in this sandbox).

## Follow-up candidates (Medium and minor; not blocking; not in a reviser brief)

The session that ran this review asks the user once whether to open issues for these. This worker creates none.

- M2-04 (adversarial P0 report path), M2-01 (escalation loop, no deadline), M2-02 (delivery of a later answer to a pending question), M2-03 (P0 outcome from an unmapped or absent status line), N2-02 (unchanged step 4 reads as YAML in P0), N3-02 (troubleshoot P0 report directory known only after the run).

## Reviser brief

Omitted: this is review 3 of 3 and the verdict is PASS, so no reviser brief is written (command Review Loop, step 6: the brief is omitted at `review: 3`). No VERIFY step is needed, because no blocking finding is open.

Coverage line: scoped PASS: changed lines + prior blockers. This is a scoped PASS, not whole-document assurance; a whole-document check needs a separate, labelled first review, whose blockers would be escalated and never start a fourth review.

verdict: PASS
