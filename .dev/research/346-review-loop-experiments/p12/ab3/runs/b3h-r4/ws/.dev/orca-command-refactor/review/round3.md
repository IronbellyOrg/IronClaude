review: 3 of 3

# /sc:spec-panel critique: orca-worker-contract-spec.md (re-review of round 2)

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines; the revised file, edited per `review/revise2.md`)
- candidate SHA-256: `2fadf1465791032cab449691f98fc1d6c0b5bd279da252336d54f84f58e6198f`
- baseline: `.dev/orca-command-refactor/specs/history/spec-v2.md` (285 lines), SHA-256 `0d68261e01a3ed1635c14612d194b7036278add2ee00b1558b4001bfcd42d22b` (equals the round-2 candidate hash at `.dev/orca-command-refactor/review/round2.md:6`)
- prior: `.dev/orca-command-refactor/review/round2.md` (`review: 2 of 3`, `verdict: FAIL`), SHA-256 `9cd22c186c959201677aed03392100be39bfd94b10ce4fd760942d76d1bbbea9`
- N = 2 + 1 = 3
- reviewer model: claude-haiku-5-5
- focus: requirements, architecture (Whittaker active per `command.md:83`)
- brief: RE-REVIEW prompt from `~/.claude/rules/prompts/document_review_loop_prompts.md` (sandbox home copy, read in full, `home/.claude/rules/prompts/document_review_loop_prompts.md:38-52`), with the re-review core (roles, Step 1, review number, self-check) applied first
- grading: CRITICAL or MAJOR is blocking only when the grading-check sentence holds with no further assumption; otherwise Medium (follow-up candidate). `origin=changed` means the finding sits on a line the revision changed against the baseline; `origin=unchanged` means it quotes a changed line that depends on it.
- review number: this is the third review of the loop. Per `command.md:261` and `command.md:263`, a FAIL here escalates to the user and no Reviser brief is written.

## Coverage

- Read in full: `command.md`, `.dev/orca-command-refactor/README.md` (`README.md:1-39`), the RE-REVIEW prompt file (`home/.claude/rules/prompts/document_review_loop_prompts.md:1-69`), the candidate (`specs/orca-worker-contract-spec.md:1-285`), the baseline (`specs/history/spec-v2.md`), and the prior report (`review/round2.md:1-153`).
- Inventory citations checked against the files in `inventory/`: `commands-a.md:35,55,60`; `commands-b.md:52,242,272`. Each was read and matches the way the spec cites it (details in the findings below).
- Not checkable in this sandbox: `sk/sc-workflow-protocol/refs/return-contract.md`, `sk/sc-adversarial-protocol/SKILL.md`, `sk/sc-troubleshoot-protocol/SKILL.md`, `cmd/*.md`, every `src/superclaude/...` path, `.dev/codegraph-migration/...` and `.dev/evals/...`. Any claim that depends on them is marked UNVERIFIED.
- Not used as evidence for this review: `review/round1.md`, `review/revise1.md`, `review/revise2.md`. Round-1 findings are carried only through `round2.md` (`round2.md:70-74`).
- Loop status: this is review 3 of 3. Two blocking findings are open (N-7, N-8), so the verdict is FAIL and the run escalates to the user.

## Step 1: evidence block

Command run: `diff -w .dev/orca-command-refactor/specs/history/spec-v2.md .dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. Lines starting `<` are BEFORE (baseline, spec-v2). Lines starting `>` are AFTER (candidate). Each block is copied verbatim. 7 changed-line pairs, at candidate lines 61, 87, 159, 182, 183, 194 and 196. Both files have 285 lines, so the numbers match.

BEFORE (baseline), `<` lines:

```text
< | WC-3 | **Questions go to the coordinator, not to a local prompt.** When a gate would resolve as blocked and the worker session holds a preamble, the session may instead ask the coordinator once with the preamble's `ask` command, wait, then re-invoke or resume the command with the answer as a flag. An answer may supply only a value the user already gave, quoted in the brief (D4(a)); it never supplies a WC-9 outward flag or an implement Ruling (D2(a)) (R-1). On an `ask` timeout it resumes the same message ID and never creates a duplicate. No heartbeat is sent while blocked in `ask`. | Worker session | `CAPS:58-61` (`[H:ask]` lines 3-5, 23-24; `[G]` lines 80-82); `CAPS:64` (`[G:worker-contract]` lines 10-11) |
< | init-lite | `--output <file>` | `.dev/superclaude/context-audit.md` or `--output` | Re-run overwrites its marked report | Accepts `--unattended` as a no-op; section only, no gate or report change (P1, R-4) | `cmd/init-lite.md:32`; `sk/sc-init-lite-protocol/SKILL.md:66,70`; `INV-A:55` |
< | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 except `load` (a no-op where a command has no gate) (R-4); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only), brainstorm and init-lite (flag and section only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
< 3. `ORCA orchestration check --wait --types "worker_done,escalation,question" --timeout-ms 900000 --json` until `worker_done` arrives. **Pass:** exactly one `worker_done`; its `--outcome` matches the `status` in that report under WC-5; its report path is the WC-4 contract path, or in P0 the command's existing report file from §3.1 ("Report today") (R-2).
< 4. `test -s <contract>` and `uv run python -c "import sys, yaml; d = yaml.safe_load(open(sys.argv[1])); assert d['status'] in {'succeeded','partial','failed','blocked'}; assert d['command']" <contract>` (PyYAML is a declared dependency, `pyproject.toml:38`). **Pass:** both exit 0.
< | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1. Record the results in the phase report; a failure here reopens section 1 |
< | P1 | AC-1.2 | 7.2 live check on each P1 command with `--unattended --output <dir>` | all steps pass |
```

AFTER (candidate), `>` lines:

```text
> | WC-3 | **Questions go to the coordinator, not to a local prompt.** When a gate would resolve as blocked and the worker session holds a preamble, the session may instead ask the coordinator once with the preamble's `ask` command, wait, then re-invoke or resume the command with the answer as a flag. An answer supplies a flag value only when it quotes the user's own words for that value, and the coordinator then writes that flag into the brief (D4(a)); a coordinator's own "yes" supplies no flag (R-1, N-1). It never supplies an implement Ruling (D2(a)). On an `ask` timeout it resumes the same message ID and never creates a duplicate. No heartbeat is sent while blocked in `ask`. | Worker session | `CAPS:58-61` (`[H:ask]` lines 3-5, 23-24; `[G]` lines 80-82); `CAPS:64` (`[G:worker-contract]` lines 10-11) |
> | init-lite | `--output <file>` | `.dev/superclaude/context-audit.md` or `--output` | Re-run overwrites its marked report | Accepts `--unattended` as a no-op and adds `--output-dir <dir>` for the WC-4 contract (N-2); section only, no gate or report change (P1, R-4) | `cmd/init-lite.md:32`; `sk/sc-init-lite-protocol/SKILL.md:66,70`; `INV-A:55` |
> | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 except `load` (a no-op where a command has no gate) (R-4); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only), brainstorm and init-lite (flag and section only; init-lite also gets `--output-dir`, N-2); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
> 3. `ORCA orchestration check --wait --types "worker_done,escalation,question" --timeout-ms 900000 --json` until `worker_done` arrives. **Pass:** exactly one `worker_done`; its `--outcome` matches the `status` in that report under WC-5 (from P1; in P0, the rule in AC-0.4, R-2); its report path is the WC-4 contract path, or in P0 the command's existing report file from §3.1 ("Report today") (R-2).
> 4. `test -s <contract>` and `uv run python -c "import sys, yaml; d = yaml.safe_load(open(sys.argv[1])); assert d['status'] in {'succeeded','partial','failed','blocked'}; assert d['command']" <contract>` (PyYAML is a declared dependency, `pyproject.toml:38`). **Pass:** both exit 0. In P0 no contract exists, so this step is only `test -s <existing report file>` from §3.1, exit 0 (R-2).
> | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-3 and 5-7 pass; step 4 is `test -s` on the command's existing report file, since the contract arrives in P1. P0 outcome rule, because no contract exists (R-2): the expected `worker_done --outcome` is `succeeded` when that report file exists and is non-empty, and `failed` when it does not (the WC-5 rule for a missing report); the coordinator reads the report's first sentence for the verdict. Record the results in the phase report; a failure here reopens section 1 |
> | P1 | AC-1.2 | 7.2 live check on each P1 command with `--unattended --output <dir>` (init-lite: `--unattended --output-dir <dir>`, N-2) | all steps pass |
```

Self-check (role check, `command.md` RE-REVIEW core): each `>` line was grepped with `-F` in the candidate and each `<` line in the baseline. All 7 pairs (and both `<` lines of step 3 and 4) were found exactly once in their own file, so no role was swapped and the baseline and candidate are not inverted.

## Prior blocking findings (round 2)

Regressed: none. No finding marked resolved in `round2.md` (R-1, R-3, R-4, R-5) fails again on the AFTER text (checked against `spec:61`, `spec:62`, `spec:63`, `spec:76`, `spec:245`).

| Id | Status | Basis |
|---|---|---|
| R-2 | resolved for the stated defect; its P0 outcome rule now conflicts with WC-5 for non-success statuses of two commands, carried as N-7 (blocking) | Step 3 now names the P0 rule (`spec:182`), step 4 has a P0 pass (`spec:183`), and AC-0.4 gives a P0 outcome (`spec:194`). For the troubleshoot smoke run (no contract, `REPORT.md` non-empty) the acceptance check can now pass as written. The new rule's premise is false for workflow and adversarial (N-7). |
| N-1 | resolved | WC-3 now limits an answer that supplies a flag to the user's own quoted words, written into the brief by the coordinator (`spec:61`). D4(a) says the same (`spec:245`: an `ask` answer counts only when it quotes the user's own instruction, and a coordinator's own "yes" does not). The two texts agree on the answer that quotes new user words. The mechanism is carried as N-9 (Medium). |
| N-2 | resolved on the stated outcome; the init-lite row now gives a contract path (`--output-dir`, `spec:87`), so a successful unattended run writes a contract. The same cell still contradicts itself, carried as N-8 (blocking). | `spec:87` (adds `--output-dir <dir>` for the WC-4 contract); `spec:159` (init-lite also gets `--output-dir`); `spec:196` (AC-1.2 uses `--output-dir`); `inventory/commands-a.md:55` confirms the round-2 premise that init-lite writes no contract today. |

## === REQUIREMENTS ANALYSIS ===

### N-7. AC-0.4's P0 outcome rule conflicts with WC-5 for workflow and adversarial (origin=changed)

- Severity: MAJOR. Grade: BLOCKING (two stated texts contradict each other on the same input, and the contradiction yields a concrete wrong outcome). Origin: changed (`spec:194`), against the unchanged WC-5 (`spec:63`). Experts: Wiegers (testability of the P0 gate), Cockburn (acceptance scope), Whittaker (FR-2.3 sentinel collision: report-file existence used as the success sentinel).
- Locations: `specs/orca-worker-contract-spec.md:194` (AC-0.4, changed): "the expected `worker_done --outcome` is `succeeded` when that report file exists and is non-empty, and `failed` when it does not ... because no contract exists". `:63` (WC-5, unchanged): `--outcome succeeded` "only when the contract's `status` is `succeeded` or `partial`"; `failed` for `failed` or `blocked`.
- The premise of `:194` is false for two of the three AC-0.4 commands. Evidence: `inventory/commands-b.md:272` (workflow writes `.dev/tasks/to-do/<id>/return-contract.yaml` with `status`, "written on every post-creation outcome, including `failed`"; `commands-b.md:52` gives the same path at `--handoff none`); `inventory/commands-a.md:35` and `:60` (adversarial: the skill "requires the contract on every run"). Only troubleshoot has no contract by default (`inventory/commands-b.md:242`: "`return-contract.yaml` only when `--caller task-unified`").
- Issue: `:194` keys the P0 outcome on file existence and does not limit it to commands without a contract, so it applies to the workflow and adversarial contracts too. WC-5 keys the outcome on `status`. For the same contract the two texts give opposite results whenever `status` is `failed` or `blocked`.
- Grading sentence: "An implementer who runs AC-0.4 on `/sc:workflow "<small change>" --handoff none` in P0, where the run ends with `status: failed` in its contract (`inventory/commands-b.md:272`), follows `spec:194` (the report file exists and is non-empty, so `succeeded`) and `spec:63` (`status` is `failed`, so `failed`); the same input gives two outcomes, so the acceptance check either passes a failed run or reopens section 1 over a correct outcome."
- Consequence (concrete): a failed P0 workflow or adversarial run can be recorded as `succeeded` to satisfy step 3, or a correct `failed` report reopens section 1 (`spec:194`, "a failure here reopens section 1"). Both are wrong outcomes for the phase gate that the phase-0 decision test depends on (section 1.4, gap 1).
- Whittaker attack (FR-2.3, sentinel collision): "I can break this specification by a sentinel collision. The invariant at `spec:194` fails when the report file exists but records a failed run. Concrete attack: P0 `/sc:workflow` produces `return-contract.yaml` with `status: failed`; the file is non-empty; the rule expects `succeeded`; WC-5 (`spec:63`) sends `failed`; step 3 (`spec:182`) passes only if the worker sends `succeeded`." (Attack is on the stated text, not on a live run.)
- Recommendation for the reviser (cites N-7): state that the file-existence rule applies only when the command has no return contract; for a command whose existing report is a contract (workflow, adversarial), the P0 outcome is the WC-5 mapping of its `status`. Alternatively delete the "because no contract exists" premise and point AC-0.4 at WC-5 for all three commands, with the troubleshoot-only exception stated once. Cite N-7 on the added text.

### N-8. The init-lite row contradicts itself and WC-4 (origin=changed)

- Severity: MAJOR. Grade: BLOCKING (two stated texts in the same cell contradict each other on the same input; an acceptance criterion cannot pass under one of them). Origin: changed (`spec:87`), with dependencies `spec:62` (WC-4, unchanged), `spec:63` (WC-5, unchanged), `spec:159` (P1, changed), `spec:196` (AC-1.2, changed). Experts: Wiegers (row-to-requirement traceability), Nygard (success reported as failure), Cockburn (acceptance scope).
- Locations: `specs/orca-worker-contract-spec.md:87` (init-lite): "Accepts `--unattended` as a no-op and adds `--output-dir <dir>` for the WC-4 contract (N-2); section only, no gate or report change (P1, R-4)". `:62` (WC-4): "In unattended mode the command writes `<output-dir>/return-contract.yaml` ... It is written on success, failure, blocked and partial outcomes". `:159` (P1): "init-lite (flag and section only; init-lite also gets `--output-dir`, N-2)". `:196` (AC-1.2): "(init-lite: `--unattended --output-dir <dir>`, N-2)".
- Issue: the cell gives two instructions. "Adds `--output-dir`" and "the WC-4 contract" need a flag and a contract write. "Section only, no gate or report change" and "a no-op" say the command changes nothing beyond the section, so no flag and no contract file. `:159` says "flag and section only" and then names the extra `--output-dir`, so it also reads the flag as an addition beyond the section. The phrase "no report change" is wrong for a command that must now write `return-contract.yaml`.
- Grading sentence: "An implementer who follows `spec:87`'s 'section only, no gate or report change' adds the `## Unattended mode` section and no `--output-dir` flag, so `--unattended --output-dir <dir>` (AC-1.2, `spec:196`) is rejected at parse, no `return-contract.yaml` is written, WC-5 (`spec:63`) then sends `--outcome failed` for a run that succeeded, and AC-1.2 step 4 (`spec:183`) fails for init-lite; the same cell also says the flag is added, so the implementer cannot satisfy both."
- Consequence (concrete): the round-2 defect (success settled as failed, N-2) returns under the "section only" reading, and AC-1.2 cannot pass for init-lite as written.
- Recommendation for the reviser (cites N-8): in `spec:87` delete "no-op", "section only" and "no gate or report change"; state that init-lite accepts `--unattended` (no gate to resolve) and `--output-dir <dir>`, and writes the WC-4 contract there in unattended mode. Make `spec:159` list the same. Cite N-8 on the added text.

## === ARCHITECTURE ANALYSIS ===

- No new architecture finding on a changed line that is not already a requirements finding above.
- N-7 is also an architecture point: after the revision the spec has two outcome mappings (existence-based in P0 at `spec:194`, status-based in WC-5 at `spec:63`), and the phase gate uses the first where the contract mapping is the one the coordinator reads from P1 on. The reviser's fix for N-7 removes the second mapping.
- A-1 (`spec:63`, `spec:263`: `partial` settles a Task as `succeeded`) is carried from round 1 unchanged. It stays Medium (see follow-up candidates).

## Guard Condition Boundary Table (guards on changed lines only, per re-review rule 5)

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| AC-0.4 P0 outcome | spec:194 | Zero/Empty | P0 troubleshoot, no contract, `REPORT.md` missing | failed | failed (the WC-5 rule for a missing report) | OK |
| AC-0.4 P0 outcome | spec:194 | Typical | P0 troubleshoot, no contract, `REPORT.md` non-empty | succeeded | succeeded; verdict from first sentence | OK |
| AC-0.4 P0 outcome vs WC-5 | spec:194 vs spec:63 | Sentinel Value Match | P0 workflow, contract `status: failed`, file non-empty | `succeeded` (AC-0.4) vs `failed` (WC-5) | two results | GAP (N-7) |
| AC-0.4 P0 outcome vs WC-5 | spec:194 vs spec:63 | Sentinel Value Match | P0 adversarial, contract `status: blocked`, file non-empty | `succeeded` (AC-0.4) vs `failed` (WC-5) | two results | GAP (N-7) |
| AC-0.4 P0 outcome vs WC-5 | spec:194 vs spec:63 | Legitimate Edge Case | P0 workflow, contract `status: partial` | `succeeded` (both) | succeeded | OK (A-1, Medium) |
| step 3 P0 pass | spec:182 | Typical | P0 troubleshoot success, outcome per AC-0.4 | matches | pass | OK |
| step 4 P0 pass | spec:183 | Zero/Empty | P0 report file exists but is 0 bytes | `test -s` exits 1 | step fails; AC-0.4 expects `failed` for it | OK |
| init-lite contract | spec:87 | Zero/Empty | `--unattended` with no `--output-dir` | no contract path; flag rejected or ignored (row unclear) | WC-5 sends `failed` | GAP (N-8) |
| init-lite contract vs WC-4 | spec:87 vs spec:62 | Typical | `--unattended --output-dir <dir>` on a successful run | "section only, no report change" vs "adds `--output-dir` for the contract" | two results | GAP (N-8) |
| init-lite flag | spec:87 | Legitimate Edge Case | `--unattended` on a command with no gate, the "no-op" reading | a contract is still written (WC-4) or not (row) | two results | GAP (N-8) |
| init-lite AC | spec:196 | Typical | `--unattended --output-dir <dir>` on init-lite | step 4 needs `d['command']` and a contract | depends on N-8 | GAP (N-8) |
| WC-3 flag supply | spec:61 | Typical | answer quotes the user's words for a flag; brief already dispatched | flag supplied by the coordinator's brief (`spec:61`) or by re-invocation with the answer (`spec:61`, first sentence) | mechanism not fixed | GAP (N-9, Medium) |
| WC-3 flag supply | spec:61 | Zero/Empty | coordinator's own "yes", no quote from the user | not supplied | refused | OK (R-1 fix) |

Input classes left out: Maximum/Overflow for the outcome status (enumerated string, no capacity bound); Maximum for AC-1.2 (no capacity bound).

Pipeline Dimensional Analysis: not triggered (no count stage changed; the WC-5 and AC-0.4 mappings are classifiers).
State Variable Registry: not triggered (`--focus correctness` is not active).

## Follow-up candidates (Medium and minor, not blocking)

No issue was created. This is a loop review; the list is recorded for the session that ran it to ask the user once per loop (`command.md:259`).

1. N-9 (Medium, origin=changed, quotes `spec:61`): WC-3's first sentence says the worker "re-invoke[s] or resume[s] the command with the answer as a flag", while the new clause says "the coordinator then writes that flag into the brief". A brief is fixed at dispatch, so the text does not say who passes the flag. The authorization condition is the same in both readings, so no outcome is forced. Needs a guess about the mechanism, so Medium.
2. N-3 (Medium, residual, quotes `spec:62`): WC-4's `<output-dir>` is "the directory the coordinator passed", but tdd still takes `--output <file>` (`spec:90`). The init-lite part of N-3 is now fixed by `spec:87` and `spec:159`. Two readings still give two contract paths for tdd.
3. N-10 (Medium, origin=unchanged, quotes `spec:92`): the workflow contract today carries `status`, `plan_path` and `reflect_report_path` (`inventory/commands-b.md:272`). WC-4 (`spec:62`) requires `command`, `report_path` and `artifacts` and says commands "add the missing ones", and AC-1.2 step 4 (`spec:183`) asserts `d['command']`. The workflow row does not name the missing fields, so the requirement is met only by the generic WC-4 rule. Medium, because WC-4 covers it.
4. N-4 (Medium, origin=unchanged, quotes `spec:63`): WC-5 sends `failed` for any status outside the four WC-4 values. The workflow status vocabulary is not in the inventory (`inventory/commands-b.md:272`), so a successful workflow run may be settled failed. UNVERIFIED (`sk/sc-workflow-protocol/refs/return-contract.md`, outside the sandbox).
5. N-5 (Medium, origin=changed, quotes `spec:61`): the parenthetical "it never supplies an implement Ruling (D2(a))" is unconditional. D2(b) (`spec:235`) would allow a relayed Ruling, and AC-4.1 (`spec:208`) contemplates one. The condition should be stated.
6. N-6 (Medium, origin=unchanged, quotes `spec:63`): round-1 R-8 still applies. Contracts are not scheduled for cleanup-audit (`spec:85`), index-repo (`spec:86`), release-split (`spec:89`), tdd (`spec:90`) and troubleshoot (`spec:91`, flag only). WC-4 is generic. It becomes blocking if the phase tables are read as the complete scope.
7. A-1 (Medium, origin=unchanged, `spec:63`, `spec:263`): `partial` settles a Task as `succeeded`. Carried from round 1.
8. Round-1 items R-6 to R-9 and A-2 to A-9 are carried and not re-graded in this review.

UNVERIFIED in this review: the contents of `sk/sc-workflow-protocol/refs/return-contract.md`, `sk/sc-adversarial-protocol/SKILL.md`, `sk/sc-troubleshoot-protocol/SKILL.md`, `cmd/*.md` and every `src/superclaude/...` path the spec cites; the workflow status vocabulary (N-4); whether `/sc:workflow` already has an output-directory flag (`spec:92`).

## Escalation

Verdict FAIL at review 3 of 3. The open blocking findings are N-7 (`spec:194` against `spec:63`) and N-8 (`spec:87` against `spec:62` and `spec:159`). Per `command.md:261` the loop stops here: the run escalates to the user with these two open blocking findings. No Reviser brief is written, because `command.md:263` omits it at `review: 3`, and no fourth review runs (`command.md:262`, `document_review_loop_prompts.md:15`).

verdict: FAIL
