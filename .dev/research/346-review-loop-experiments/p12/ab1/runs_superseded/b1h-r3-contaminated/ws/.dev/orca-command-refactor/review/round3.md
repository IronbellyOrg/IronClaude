review: 3 of 3
> verification (coordinator, VERIFY step VF3; verifier reply .dev/orca-command-refactor/review/verify-3.md): confirmed blocking ids: B2. Rejected, kept as noted, unactioned and not prior blocking findings for the next re-review: none. The Reviser brief below is narrowed to the confirmed ids.
> verification (coordinator): not yet run for this report. The VERIFY prompt still runs on the open blocking finding B2 (prompts file lines 53-59), then the loop escalates to the user. No REVISE prompt and no fourth review.

# /sc:spec-panel critique, re-review 3 of 3 (focus: requirements, architecture)

candidate: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md sha256 d7bacfaaecc8fff9a059e1e70fe785b1e6c52aecb2a57c161ca8d51cdcb3aa3c
baseline: .dev/orca-command-refactor/specs/history/spec-v2.md sha256 bddecb0d53d012639197cb333a623b97ec5dd535120f7fee296fb97a980e41db
prior: .dev/orca-command-refactor/review/round2.md sha256 11901954d0619034bec3e3248473f6011c98777269433aaeff831ac3655de386 (`review: 2 of 3`, `verdict: FAIL`)
reviewer model: claude-haiku-5-5
review number: N = 3 (prior header `review: 2 of 3`, `round2.md:1`)
baseline check: the baseline's hash equals the `candidate:` hash in the prior report (`round2.md:6`), so the text reviewed in review 2 is the baseline text.
inputs: candidate, baseline and prior were all readable and hashable; none is missing.
rf-qa.md: neither `.claude/agents/rf-qa.md` in the workspace nor `~/.claude/agents/rf-qa.md` exists in this sandbox, so the Process of the Fix Cycle steps were not applied; the Review Loop rules in this report stand alone (`command.md` Review Loop item 5).
re-review brief: `~/.claude/rules/prompts/document_review_loop_prompts.md` RE-REVIEW prompt, read in full (lines 38-51), with the VERIFY prompt (lines 53-59) and the rules for review 3 (`command.md:261`).
WORKER-CONTRACT.md: not read. `command.md:457` makes it a read only under `--unattended`, which this run does not use.
not read: the round1 and round1-a/b/c files, findings-1/2, revise1/2, verify-1/2 and the sibling run folders. They are not inputs named by the brief. The verification outcome of review 2 is taken from `round2.md:2`. `cmd/load.md` and `src/superclaude/` are not in the sandbox (UNVERIFIED).
not checkable here: `src/superclaude/` and the Orca guide (`[G]` sources). Inventory lines are checked only as quoted in `.dev/orca-command-refactor/inventory/`. Anything else is marked UNVERIFIED.

## Step 1: evidence block

Command: `diff -w` of the baseline against the candidate. Roles are fixed as above: BASELINE is `specs/history/spec-v2.md`, CANDIDATE is `specs/orca-worker-contract-spec.md`. The diff has three hunks, at candidate lines 112, 159 and 268 (`diff -w` exit 1). Changed lines copied verbatim:

BEFORE (baseline), lines starting with `<`:

```text
| load | no gate | status-only contract under `--unattended` (`status`, `command`; no `report_path`, as WC-4 allows) [M8] | n/a | none: use it as a step inside another worker's brief, not as its own Task; separately, `--checkpoint` is missing from its Usage line | `cmd/load.md:22,42-43,52,82`; `INV-B:31,57-65` | P1 (usage line only) |
| **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
| `/sc:load` handling | Add a report file; use it only inside another worker's brief | Use it inside a brief: its only output is context for the current session (`INV-B:65`). Under `--unattended` it writes a status-only contract with no report file [M8], which meets WC-4 and AC-1.1 without adding a report. Only its usage-line defect is fixed. |
```

AFTER (candidate), lines starting with `>`:

```text
| load | no gate | contract under `--unattended` with `status`, `command` and `artifacts: []` (no other file is written, so the list is empty; no `report_path`, as WC-4 allows) [B1] | n/a | none: use it as a step inside another worker's brief, not as its own Task; separately, `--checkpoint` is missing from its Usage line | `cmd/load.md:22,42-43,52,82`; `INV-B:31,57-65` | P1 (usage line; `## Unattended mode` section) [B1] |
| **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line, and the `## Unattended mode` section that AC-1.1 requires) [B1]; fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
| `/sc:load` handling | Add a report file; use it only inside another worker's brief | Use it inside a brief: its only output is context for the current session (`INV-B:65`). Under `--unattended` it writes a contract with `status`, `command` and `artifacts: []` and no report file [B1]. WC-4 requires `artifacts`, and an empty list meets it because load writes no file (`INV-B:65`). The P1 row adds the `## Unattended mode` section that AC-1.1 requires for load [B1]. Its usage-line defect is fixed too. |
```

Self-check (`grep -nF`, run before the verdict): each of the 3 AFTER lines is found in the candidate (1 match each); each of the 3 BEFORE lines is found in the baseline (1 match each) and in no line of the candidate (0 matches). No role was swapped, so Step 1 stands.

Other checks run: the AC-C1 self-test `printf 'orca orchestration worker-start\n' | grep -iE '\borca\b'` exits 0 and prints the line (spec:172). The M4/M9 WC-5 text, the M10 path rows and the M2 relay text are unchanged from the baseline, so their status below rests on unchanged lines.

## Prior blocking findings (from `round2.md:57-68`, with its Reviser brief at `round2.md:148-151`)

Prior blocking ids: M2, M4, M7, M8 (= B1 in round 2), M9, M10. Status: `resolved|open|regressed`.

| id | prior defect (round1.md) | status | basis in the candidate |
|---|---|---|---|
| M2 | WC-3 let a coordinator answer any gate, including the implement Ruling | resolved | The WC-3 relay text is unchanged (spec:61, not in the diff). It relays only for gates whose section 3 row names a flag and excludes the safety and authorization gates (spec:61). No changed line touches it. |
| M4 | A missing or unknown `status` became `succeeded`; the adversarial contract had two paths | resolved | WC-5 (spec:63) and the adversarial row (spec:83) are unchanged from the baseline, and both already carry the fix; AC-0.5 (spec:195) and AC-1.4 (spec:199) are unchanged. |
| M7 | AC-C1 could not fail | resolved | AC-C1 (spec:172) is unchanged; its self-test passes (run above). The whole-file exemptions are now on an unchanged line, so they are minor notes (R2-3 below). |
| M8 (= B1 in round 2) | The load row contradicted WC-4 and AC-1.1: `status`/`command` only, no `artifacts`, and the P1 text omitted the load section | resolved | The row now writes `status`, `command` and `artifacts: []` (spec:112), which matches WC-4 (spec:62). The Decisions row (spec:268) and the P1 row (spec:159) now agree with it and add the `## Unattended mode` section that AC-1.1 requires (spec:196). The three conflicting texts now agree. A new defect on the same row is recorded as B2 and R3-1 below; it is not a regression of M8. |
| M9 | WC-5 mapped a `done` or empty status to `succeeded` | resolved | Same text as M4: WC-5 (spec:63), AC-0.5 (spec:195); unchanged. |
| M10 | Workflow, research and cli-portify had no fixed contract path | resolved | Each row still names `<output-dir>/return-contract.yaml` with the new flag (spec:92, spec:105, spec:116; unchanged). AC-1.5 and AC-2.6 check the path (spec:200, spec:206; unchanged). |

Regressed: none. No changed line reopens the defect of a finding marked resolved.

## Blocking findings

### B2 (new in round 3, blocking, origin=changed). The load row forbids the Task that AC-1.2 requires for load

- Origin: changed. The row quotes the changed line spec:112; the conflicting AC-1.2 is unchanged (spec:197). The same two texts are also in the baseline (`spec-v2.md:112` and `spec-v2.md:197`), so this is older than the round-3 edit and was not raised in round 2. Recorded now under the rule to record a severe defect found in re-review even if older.
- Stated texts:
  1. spec:112, load row: "use it as a step inside another worker's brief, not as its own Task".
  2. spec:159 (P1 scope) puts `load` in P1; spec:196 (AC-1.1) and spec:197 (AC-1.2) apply to "each P1 command", and AC-1.2 is "7.2 live check on each P1 command with `--unattended --output <dir>` | all steps pass".
  3. spec:179-180 (7.2): "For each command under test, the coordinator runs: 1. `ORCA orchestration task-create --spec "<brief per section 2.3>"`, then `worker-start`". Step 3 (spec:182) requires one `worker_done` whose report path is the WC-4 contract path.
  4. spec:167: "A phase passes only when every check in its block and every common check passes."
- Sentence that holds with no further assumption: an implementer who follows the load row never creates a Task for `/sc:load` (spec:112); AC-1.2 requires a 7.2 run on `load`, and 7.2 step 1 (spec:180) creates a Task for each command under test; so AC-1.2 cannot pass for `load` as written, and P1 cannot pass (spec:167).
- Grading: a stated text that an acceptance criterion cannot pass, and two stated texts that contradict each other, are both blocking under `command.md` Review Loop item 2 and the FIRST-REVIEW grading check (prompts file line 33).
- Experts: Wiegers (traceability from AC-1.2 to the row), Crispin (an acceptance check that cannot run as written), Whittaker (the gate is a contradiction the coordinator must resolve by guessing).
- Priority: High. Impact: the P1 phase cannot close, and the implementer must choose between running load as a Task (which the row forbids) and skipping the check (which AC-1.2 forbids).
- Recommendation (for the user at escalation; no Reviser brief at review 3): either allow load as its own Task and keep AC-1.2, or exempt load from 7.2 by name in AC-1.2 with the reason, and make the load row (spec:112), the P1 row (spec:159) and AC-1.1 (spec:196) say the same.

## Findings on changed lines (Medium; follow-up candidates, not blocking)

Medium findings never trigger a revision or fail the review (`command.md` Review Loop item 2).

- R3-1 (Medium, origin=changed, spec:112 and spec:268). WC-4 keys the contract path on `<output-dir>`, "the directory the coordinator passed (`--output` / `--output-dir`)" (spec:62). The load row names no directory. P1's generic "output flags for commands that lack one" (spec:159) covers adding a flag, but not which directory `load` writes to when it runs "as a step inside another worker's brief" (spec:112). If the implementer uses the outer worker's output directory, `load` writes `<outer>/return-contract.yaml`, the same WC-4 path as the outer command's contract, and overwrites it. The coordinator then reads `status: succeeded` from `load` in place of the outer command's status. The text does not say which directory is used, so this needs a guess, which makes it Medium under the FIRST-REVIEW grading check (prompts file line 33). Experts: Fowler (one contract path per worker), Whittaker (state collision), Nygard (wrong status read by the coordinator).
- R2-1 to R2-6 (round 2, now origin=unchanged; not re-graded). Their defect lines are unchanged in this round: R2-1 (spec:116), R2-2 (spec:195), R2-3 (spec:172), R2-4 (spec:61, spec:104), R2-5 (spec:61), R2-6 (spec:172). Under the rule that an unchanged-line finding is a minor note unless it quotes a changed line, they are minor notes here. None quotes spec:112, spec:159 or spec:268, so none is re-graded.

## Guard Condition Boundary Table (changed guards only; re-review scope)

Guards on changed lines: the load contract guard (spec:112 against WC-4 at spec:62) and the P1 load step (spec:159). Input classes that cannot occur are left out with a reason.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| load contract | spec:112 against spec:62 | Typical: load run as its own Task with the WC-4 path known before dispatch | Task created | row says no Task; AC-1.2 needs one | row (spec:112) and AC-1.2 (spec:197) conflict | GAP (B2, blocking) |
| load contract | spec:112 against spec:62 | Zero/Empty: no output directory passed | no `--output` or `--output-dir` | not decidable from the text | row names no directory; P1 (spec:159) adds a flag but not its value | GAP (R3-1, Medium) |
| load contract | spec:112 against spec:62 | Legitimate edge: load run as a step inside an outer worker's brief with the outer output directory | `<outer>/return-contract.yaml` | the outer contract is overwritten | spec:112 does not say which path load uses | GAP (R3-1, Medium) |
| load contract | spec:112 against spec:62 | Sentinel: `artifacts` is an empty list | `artifacts: []` | meets WC-4 | spec:62 requires the field; INV-B:65 says load writes no file | OK |
| load contract | spec:112 | Maximum/Overflow | not applicable | n/a | left out: load writes at most one contract file (INV-B:65) | n/a |

Synthesis gate (FR-10): every changed guard has a row or a stated reason for being left out.

## Expert findings (focus: requirements, architecture; Whittaker always active)

- Wiegers: B2 (AC-1.2 cannot pass for the row's `load` as written); R3-1 (no stated output directory for `load`).
- Adzic: B2 (no example of how `load` is tested as a worker step); no new finding on the other changed lines.
- Cockburn: no new finding; `load` has no actor goal on the changed lines.
- Fowler: R3-1 (two commands would share one contract path); the contract field set now matches WC-4 (spec:62).
- Newman, Hohpe: no new finding on changed lines.
- Nygard: R3-1 (the coordinator reads the wrong status).
- Crispin: B2 (the 7.2 check cannot be applied to a row that forbids a Task).
- Whittaker: R3-1, the collision of two contracts at one path; the M8 fix itself holds for every class in the table above except the two GAP rows.

## Noted, unactioned (not blocking; not re-graded)

These stay notes under the Review Loop (`round2.md:127-136`; rule in the re-review prompt, lines 56-57). None of them is on a changed line, so none is re-graded here.

- M1, M6, M11 (origin=unchanged). Not re-graded.
- M3 (WC-5 audit clause; unchanged line spec:63). The premise (`inventory/orca-capabilities.md:73`) is checkable only as quoted; the Orca guide `[G]` text is UNVERIFIED in this sandbox.
- M5 (AC-C1, now unchanged spec:172). Its substance is R2-3 above.
- M12 (spec-panel row, unchanged spec:120). `command.md:23` and `command.md:460` are not in this sandbox, so the premise is UNVERIFIED here.

## Verdict

Blocking findings open: 1 (B2, new in round 3). Prior blocking findings: M2, M4, M7, M9, M10 resolved; M8 (= B1) resolved; regressed: none.

Coverage: all 3 changed hunks (6 lines) of the diff; all six prior blocking ids; the Guard Condition Boundary Table for the two changed guards; the expert panel for focus requirements and architecture; the AC-C1 self-test; the sandbox citations for `INV-B:31,57-65` and `INV-B:65`, which were checked against `inventory/commands-b.md`. Not covered: `src/superclaude/`, the Orca guide, `cmd/load.md` and the other command files (not in the sandbox; UNVERIFIED).

Follow-up candidates (Medium and minor; the coordinator asks the user once whether to open issues for them; none were created by this review): R3-1, R2-1, R2-2, R2-3, R2-4, R2-5, R2-6, M3, M5, M12.

Escalation (review: 3 of 3, FAIL): no Reviser brief is written at review 3 (`command.md` Review Loop item 6). The coordinator runs the VERIFY prompt on B2 (prompts file lines 53-59) in a fresh context, with the candidate and the finding text only. If it is confirmed, the loop ends by escalating B2 to the user with the confirmed finding. If it is rejected, the verdict stays FAIL and the rejected id is noted, unactioned. No REVISE prompt and no fourth review are run.

verdict: FAIL
