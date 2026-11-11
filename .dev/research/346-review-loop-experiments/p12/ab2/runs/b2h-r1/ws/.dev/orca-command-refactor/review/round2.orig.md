review: 2 of 3

# Spec-panel critique: Orca worker-contract spec (re-review, review 2 of 3)

- command: `/sc:spec-panel --mode critique --focus requirements,architecture --re-review .dev/orca-command-refactor/review/round1.md --baseline .dev/orca-command-refactor/specs/history/spec-v1.md`
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `00cb7b63ea6019f358ead17f8b721ad6058432fb1bebc97218c1af92404e5038`
- baseline: `.dev/orca-command-refactor/specs/history/spec-v1.md`, sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` (the same hash `round1.md:7` recorded for the candidate it reviewed, so the baseline is the text round 1 reviewed)
- prior report: `.dev/orca-command-refactor/review/round1.md`, sha256 `81f6066d63a891b9e0615c996583d04f7bcb11a27876e9c54590fb712106618b`, header `review: 1 of 3` (N = 2)
- reviewer model: claude-haiku-5-5
- review-loop prompt: RE-REVIEW prompt in `~/.claude/rules/prompts/document_review_loop_prompts.md`, read in full and followed in order (roles, Step 1, review number, self-check, then the brief).
- rf-qa.md: neither `.claude/agents/rf-qa.md` (workspace) nor `~/.claude/agents/rf-qa.md` exists in this sandbox. The re-check therefore follows the rules of the command's Review Loop section alone (UNVERIFIED that the rf-qa.md fix-cycle steps 1-5 agree).
- Scope: the candidate differs from the baseline only at spec:181, spec:182 and spec:194 (Step 1 below). Findings are on those lines; nothing else was re-reviewed.

## Step 1: evidence block

Command run from the repo root: `diff -w specs/history/spec-v1.md specs/orca-worker-contract-spec.md`. The two files have the same line count and the changes sit on lines 181, 182 and 194 of both. Changed lines, copied verbatim:

BEFORE (baseline):

```text
2. While it runs, `ORCA orchestration worker-show --dispatch <dispatch_id> --json` at least once per 5 minutes. **Pass:** `observation.agentWait` is never non-null (a non-null value means the worker is parked on a prompt only a person can answer, `[H:worker-show]` Notes).
3. `ORCA orchestration check --wait --types "worker_done,escalation,question" --timeout-ms 900000 --json` until `worker_done` arrives. **Pass:** exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path.
| P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1. Record the results in the phase report; a failure here reopens section 1 |
```

AFTER (candidate):

```text
2. While it runs, `ORCA orchestration worker-show --dispatch <dispatch_id> --json` at least once per 5 minutes; with step 3's 240 s waits, one `worker-show` runs between consecutive waits (F-02). **Pass:** `observation.agentWait` is never non-null (a non-null value means the worker is parked on a prompt only a person can answer, `[H:worker-show]` Notes).
3. Repeat `ORCA orchestration check --wait --types "worker_done,escalation,question" --timeout-ms 240000 --json`, running step 2's `worker-show` before each repeat, until `worker_done` arrives (F-02: a 900 s wait would leave no `worker-show` for up to 15 minutes; 240 s keeps the 4-minute bound of WC-10). On `question`, the coordinator answers with `ORCA orchestration reply --id <message_id> --body "<answer>"` (CAPS:63) only with an answer the brief or the person has given; otherwise it asks the person and invents no answer. On `escalation`, it records the escalation verbatim in the phase report and keeps looping; only `worker_done` ends the loop. **Pass:** exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path.
| P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-3 and 5-7 pass. In P0, since the contract arrives in P1 (F-03): step 4 is `test -s <report>` on the file the command already writes, with no YAML parse (for `/sc:troubleshoot` that file is `REPORT.md`, a markdown report, `INV-B:242`); the YAML key check in step 4 applies from P1. Step 3's outcome check in P0 reads the outcome from the report's first status line, and the phase report records that line as found, since its format is UNVERIFIED (the troubleshoot report template is not in the inventories). Record the results in the phase report; a failure here reopens section 1 |
```

Role check (self-check, `grep -nF` of each quoted line in its own file, run before any finding): every AFTER line was found in CANDIDATE at 181, 182 and 194, and every BEFORE line was found in BASELINE at 181, 182 and 194. The roles are not swapped.

## Prior blocking findings (from round1.md)

round1.md:2 (VERIFY block) confirmed only F-02 and F-03 as blocking. F-01 and F-04 were rejected and are kept as noted, unactioned; per the RE-REVIEW rule, a rejected id is a note, not a prior blocking finding. The Reviser brief at round1.md:240 still lists F-01 to F-04, which contradicts the VERIFY block that states the brief was narrowed; this report follows the VERIFY block. None of F-01 or F-04's cited lines (spec-v1 texts at spec:61, 76, 109, 112, 195, 200, 234, 265) is among the changed lines 181, 182 or 194, so their status is not affected by this revision.

| id | prior status | now | evidence |
|---|---|---|---|
| F-02 (7.2 heartbeat check cannot satisfy its own pass condition) | open, blocking (round1.md:31-38) | resolved | step 2 now pairs `worker-show` with 240 s waits (spec:181); step 3 uses `--timeout-ms 240000` and runs `worker-show` before each repeat (spec:182). The 900 s wait that left no `worker-show` for up to 15 minutes is gone. The `question` and `escalation` branches that round1 said were missing are added (spec:182). |
| F-03 (AC-0.4 applies a YAML contract check to a markdown report) | open, blocking (round1.md:40-46) | resolved | AC-0.4 (spec:194) now states that in P0 step 4 is `test -s <report>` with no YAML parse, that the YAML key check applies from P1, and that the P0 outcome comes from the report's first status line. The YAML-on-markdown defect is gone. The same P0 gate still has a separate blocking defect, N2-01 below, which sits on the changed line spec:182. |

Regressed: none. No finding was marked resolved in round1.md, so no prior finding can regress.
Open prior blocking findings: none.

## Findings on changed lines

### N2-01 (MAJOR label, blocking): the P0 gate AC-0.4 cannot pass as written, because step 3 requires the WC-4 contract path

- origin=changed (spec:182 is a changed line). Newly discovered in this review. The clause is older: it is unchanged from spec-v1.md:182, and round1 did not name it.
- Texts. spec:182, the step 3 pass condition: "**Pass:** exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path." spec:194, AC-0.4 P0: "steps 1-3 and 5-7 pass. In P0, since the contract arrives in P1 (F-03): step 4 is `test -s <report>` ...; Step 3's outcome check in P0 reads the outcome from the report's first status line ...". spec:158 defines P0 as "no command edits", and the P0 runs are the "ready" commands with the stated flags, which do not include `--unattended` (spec:81, spec:91). WC-4 writes the contract only "In unattended mode" (spec:62). The file the troubleshoot run writes is `REPORT.md` (spec:91; `.dev/orca-command-refactor/inventory/commands-b.md:242`, "`report_path` (REPORT.md)").
- Sentence. An implementer who runs AC-0.4 in P0 on `/sc:troubleshoot` follows spec:182 as written: the worker's `worker_done --report-path` must be the WC-4 contract path. No such contract exists in P0 (spec:194 says the contract arrives in P1), so the report path is `REPORT.md`, the clause fails, step 3 fails, AC-0.4 fails, and spec:194 says a P0 failure reopens section 1. This is wrong because the spec's own P0 scope (spec:158) makes the clause impossible to meet in the phase that tests the decision.
- Why the spec:194 override does not cover it. spec:194 overrides step 4 (the YAML parse) and the outcome source in step 3. It does not waive the path clause in step 3.
- Recommendation. In spec:194, add that the P0 report path is the command's existing report file (for troubleshoot, `REPORT.md`), so the path clause reads "the command's own report path" in P0 and "the WC-4 contract path" from P1. Alternatively move the path clause from spec:182 into the P1 checks only. Either way, the VERIFY step must confirm N2-01 before any revision.
- Priority: High. Quality-impact estimate: high (the P0 phase gate cannot pass as written).

### Medium findings on changed lines (follow-up candidates; not blocking)

- M2-01 (Medium): spec:182 says the loop continues on `escalation` and that "only `worker_done` ends the loop", with no overall deadline. A worker that escalates and never sends `worker_done` keeps the coordinator in the loop indefinitely. The text states no cap, so it is a missing restriction, Medium by the grading rule. Quality-impact estimate: low to medium.
- M2-02 (Medium): spec:182 says that on `question` the coordinator asks the person when it has no answer, but it does not say how the person's answer reaches the worker (a later `reply --id`), nor what the loop does while the question is pending. An implementer may leave the worker parked on `ask`. Undefined state, Medium. Reply mechanics are in `.dev/orca-command-refactor/inventory/orca-capabilities.md:63` (`reply --id <message_id>`).
- M2-03 (Medium): spec:194 takes the P0 outcome from "the report's first status line", and says its format is UNVERIFIED (the troubleshoot report template is not in the inventories, spec:194 text). The spec does not say what result the outcome check has when no status line exists or the status is not one of the WC-5 outcomes; it says only that the line is "recorded as found". Undefined edge case, Medium.
- M2-04 (Medium): spec:194 requires `test -s <report>` on "the file the command already writes" for all three P0 runs. For `/sc:adversarial --compare ... --output <dir>` the filename is not fixed (spec:83, "contract, but filename not fixed"), so `<report>` is not defined for that run. Medium: an undefined input, not a stated wrong outcome.

### Minor note (origin=unchanged, depends on a changed line)

- N2-02 (minor): spec:183, the general step 4 (unchanged), still reads as a YAML check for every phase. The P0 relaxation lives only in spec:194, so an implementer reading step 4 alone hits the YAML parse in P0. Note only.

## Guard Condition Boundary Table (guards on changed lines only, FR-8 to FR-10)

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| Step 3 wait return | spec:182 | Zero/Empty: no event within 240000 ms | none | repeat after `worker-show` | stated | OK |
| Step 3 question branch | spec:182 | Typical: `question` with an answer in the brief or from the person | `question` | `reply --id <message_id>` | stated; reply mechanics at orca-capabilities.md:63 | OK |
| Step 3 question branch | spec:182 | Typical: `question` with no answer | `question` | asks the person | no rule for delivering the later answer or for the pending question | GAP (M2-02) |
| Step 3 escalation branch | spec:182 | Maximum: escalation never resolves | `escalation` | keeps looping | no overall deadline | GAP (M2-01) |
| Step 3 pass | spec:182 | Typical: P0 run, `worker_done` arrives, no WC-4 contract | report path `REPORT.md` | pass clause fails | path clause requires the WC-4 contract path | GAP (N2-01, blocking) |
| P0 outcome | spec:194 | Zero/Empty: no status line in the report | no status line | undefined | "recorded as found" with no pass rule | GAP (M2-03) |
| P0 outcome | spec:194 | Sentinel: status outside the WC-5 outcomes | unknown status value | undefined | not stated | GAP (M2-03) |
| P0 step 4 | spec:194 | Zero/Empty: report missing or zero bytes | absent or 0 | `test -s` exits non-zero, run fails | stated by `test -s` | OK |
| P0 step 4 | spec:194 | Typical: troubleshoot | `REPORT.md` | `test -s` on that file | named at spec:91 and commands-b.md:242 | OK |
| P0 step 4 | spec:194 | Typical: adversarial | output dir, filename not fixed | undefined path | not stated | GAP (M2-04) |

Rows left out: the step 2 pass at spec:181 ("at least once per 5 minutes") was checked against the 240 s waits and needs no row (the gap between `worker-show` calls is at most about 240 s).

## Coverage

- Read in full: the candidate spec, the baseline spec-v1.md, round1.md, the RE-REVIEW prompt, command.md, and README.md.
- Checked against the inventories: commands-b.md:242 (troubleshoot `report_path` REPORT.md) and orca-capabilities.md:63 (`check --wait`, `reply --id`), :129-130 (`agentWait` means a prompt only a person can answer, so an `ask` to the coordinator does not set it; no conflict with spec:181).
- Not covered: the repository files the spec cites (outside the sandbox; UNVERIFIED), and the unchanged parts of the spec, which the re-review scope excludes.
- Not run: `make verify-sync`, `uv run pytest` and any Orca command (no repository or Orca in this sandbox).

## Follow-up candidates (Medium and minor; not blocking; not in the reviser brief)

The session that ran this review asks the user once whether to open issues for these. This worker creates none.

- M2-01 (escalation loop, no deadline), M2-02 (question answer delivery), M2-03 (P0 outcome from an unmapped status line), M2-04 (adversarial report path), N2-02 (unchanged step 4 reads as YAML in P0).

## Reviser brief

Blocking finding ids for this loop: N2-01. Revise only text that N2-01 names (spec:182 pass clause, and spec:194 where it states the P0 check). Rule restated from the command's review loop, step 6: revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id. Medium and minor findings are not part of this brief.

Brief clauses overridden: none.

This brief is for the reviser only after the VERIFY prompt has run on N2-01. If VERIFY does not confirm N2-01, no confirmed blocking finding remains and the loop ends with this review's PASS, per the VERIFY rule.

verdict: FAIL
