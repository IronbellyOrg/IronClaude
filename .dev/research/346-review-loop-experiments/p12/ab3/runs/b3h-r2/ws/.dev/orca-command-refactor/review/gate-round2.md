review: 2 of 3

# Re-review: orca-worker-contract-spec.md (gate loop, review 2 of 3)

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (sha256 `d33b89a08efc2ef08e5a0449828d8b35251424cc7d54958dac98f929b1383529`, 290 lines)
- baseline: `.dev/orca-command-refactor/specs/history/spec-g.md` (sha256 `06cb4bcd39e29ea26abacd7521abf23c5e125f1cefda82fb1736f725a01d24b0`, 290 lines)
- prior report: `.dev/orca-command-refactor/review/gate.md` (sha256 `51613c7ce3c7e81b11a07b8574bc685d7554a151415409af456f96a1f72868d2`), header `review: 1 of 3`, verdict FAIL, blocking ids RA-01 to RA-04
- reviewer model: claude-haiku-5-5
- command: `/sc:spec-panel --mode critique --focus requirements,architecture --re-review review/gate.md --baseline specs/history/spec-g.md`, run under the RE-REVIEW prompt of `document_review_loop_prompts.md` as the gate loop's re-review (GATE prompt, "Gate loop"; a FAIL here escalates, see the verdict)
- review number: N = 1 + 1 = 2 (prior header `review: 1 of 3`)
- sandbox note: all reads were inside the workspace or the sandbox home. One shell `ls` for `~/.claude/agents/` expanded `~` to the default shell home, which is outside the sandbox; it printed nothing and nothing was read or written there. `rf-qa.md` was not found at `ws/.claude/agents/rf-qa.md` or at the sandbox home `home/.claude/agents/rf-qa.md`, so its Process of the Fix Cycle steps 1-5 were not applied; the rules of the command's Review Loop section stand alone, as its bullet 5 allows. Citations into `src/`, `tests/`, `~/.claude/` and skill files are UNVERIFIED here.

## Coverage

- Read in full: the candidate (290 lines), the baseline (290 lines), `gate.md`, `README.md`, `command.md`, `document_review_loop_prompts.md`.
- Inventory lines checked: `inventory/commands-a.md:33-39` (table header and the adversarial, auggie-review and brainstorm rows), `inventory/commands-a.md:58-65` (facts that change verdicts), `inventory/commands-b.md:36`, `:49`, `:242`, `:245` (troubleshoot).
- Scope: the candidate differs from the baseline on five lines (`diff -w`, hunks 84c84, 142c142, 159c159, 199c199, 201c201). Findings below are on those lines, or are prior blockers. Prior medium and minor findings of `gate.md` are not re-graded here.
- Not covered: skill and command files outside the workspace (UNVERIFIED); any live Orca behaviour.

## Step 1: evidence block

Roles fixed by the file values: CANDIDATE = `specs/orca-worker-contract-spec.md`, BASELINE = `specs/history/spec-g.md`, PRIOR = `review/gate.md`. The command run was `diff -w BASELINE CANDIDATE`.

BEFORE (baseline), lines starting `<`:

```text
< | brainstorm | `--output <dir>`; never `--interactive` | `<output>/return-contract.yaml` | `--resume-from <seed-brief>` | None | `sk/sc-brainstorm-protocol/SKILL.md:134,335`; `cmd/brainstorm.md:59-63`; `INV-A:39` |
< A person who runs any `/sc:` command in a plain Claude session, inside or outside Orca, with or without Orca installed, must see exactly today's behaviour. This is a hard requirement on every phase.
< | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, init-lite (F-05), workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
< | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1. Record the results in the phase report; a failure here reopens section 1 |
< | P1 | AC-1.2 | 7.2 live check on each P1 command with `--unattended --output <dir>` | all steps pass |
```

AFTER (candidate), lines starting `>`:

```text
> | brainstorm | `--output <dir>`; never `--interactive` | `<output>/return-contract.yaml` | `--resume-from <seed-brief>` | Flag and `## Unattended mode` section only, in P1 (RA-03) | `sk/sc-brainstorm-protocol/SKILL.md:134,335`; `cmd/brainstorm.md:59-63`; `INV-A:39` |
> A person who runs any `/sc:` command in a plain Claude session, inside or outside Orca, with or without Orca installed, must see exactly today's behaviour. This is a hard requirement on every phase, with two named exceptions: the adversarial contract path that SA-3 names, and the documented defect fixes that SA-4 names (RA-04).
> | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, init-lite (F-05), workflow; brainstorm (flag and section only, RA-03) | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
> | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-3 and 5-7 pass, with step 3 applied to the command's existing report file (the "Report today" column of section 3.1) in place of the WC-4 contract, so its outcome is checked against that file's status under WC-5 (RA-01); step 4 uses the same existing report file, since the contract arrives in P1. Record the results in the phase report; a failure here reopens section 1 |
> | P1 | AC-1.2 | 7.2 live check on each P1 command except `load` (RA-02: load is never its own Task and writes no contract, so 7.2 cannot pass for it), with `--unattended --output <dir>` | all steps pass |
```

Self-check (run before the verdict): every AFTER line was found by `grep -nF` in the candidate at lines 84, 142, 159, 199 and 201, and every BEFORE line in the baseline at lines 84, 142, 159, 199 and 201. The roles are confirmed; no swap.

## Re-check of prior blocking findings (from gate.md)

| Id | Status | Basis |
|---|---|---|
| RA-01 | open | Step 3's WC-4 path clause was replaced (candidate `:199`), but step 4 still requires `test -s <contract>` and a YAML `status` read (`:188`) on "the command's existing report file", and the same row says the contract arrives in P1. For `/sc:troubleshoot` the default run writes REPORT.md and a contract only with `--caller task-unified` (`inventory/commands-b.md:242`). The defect is narrowed, not gone. See finding RA-01 below. |
| RA-02 | resolved | AC-1.2 now reads "each P1 command except `load`" (`:201`). `load` is excluded from the live check, which matches its no-Task, no-contract row (`:112`), AC-1.1 (`:200`) and P1 (`:159`). |
| RA-03 | resolved | Brainstorm is now in P1 with a flag and a `## Unattended mode` section (`:84`, `:159`). AC-1.1 (`:200`) and P1's flag scope now reach it. Its verdict "ready with default flags" (`inventory/commands-a.md:39`) does not conflict with that: the flag and section are additive. Medium note M-2 below. |
| RA-04 | resolved | Line `:142` now names the exceptions it allows (the SA-3 adversarial path and the SA-4 defect fixes), so it no longer contradicts SA-3's adversarial exception (`:148`). Medium note M-4 below covers what is left. |

## Findings on changed lines

### Blocking

**RA-01 (open; blocking; requirements, testability): AC-0.4 cannot pass for `/sc:troubleshoot` as written.** origin=changed (`spec:199`, quoting step 4 `spec:188`).

- Sentence: An implementer who runs AC-0.4 step 4 on `/sc:troubleshoot` takes "the command's existing report file" (`spec:199`), which is REPORT.md (`inventory/commands-b.md:242`, `report_path`). Step 4 then requires `test -s <contract>` and a YAML load with `d['status']` (`spec:188`). The inventory says `return-contract.yaml` is written only with `--caller task-unified` (`inventory/commands-b.md:242`), so a default P0 run has no contract, and no `status` field is stated for REPORT.md. The P0 gate for troubleshoot therefore cannot pass.
- Step 3 has the same defect in the revised clause: its outcome is "checked against that file's status under WC-5" (`spec:199`, WC-5 at `spec:63`), and no status field is stated for REPORT.md.
- Why open: the revision fixed step 3's path clause, which was the gate's sentence. It left step 4 unchanged, and step 4's YAML assertion contradicts the row's own premise that no contract exists in P0.
- Direction for the reviser: give troubleshoot's P0 check a status source the inventory names, or exclude troubleshoot from the P0 live check and use a P0 command that writes a contract (adversarial or workflow), or make step 4 apply only to commands that write a contract in P0. This is a direction only; the reviser decides the wording.

### Medium (follow-up candidates; not blocking)

**M-1 (line `:199`; carries RA-09, unchanged in substance): the P0 brief is defined to include `--unattended`, which P0 does not add.** Section 2.3 (`spec:73`) says the brief carries "the exact command line including `--unattended`". Step 1 of the live check uses "the brief per section 2.3" (`spec:185`). P0 makes no command edits (`spec:158`), and the flag arrives in P1 (`spec:159`). Whether a slash command rejects an unknown flag is UNVERIFIED (commands are prompt text), so the outcome is either a silent non-unattended run or a rejected launch. The spec does not say which. Medium, because no certain wrong outcome is stated.

**M-2 (lines `:84`, `:79`): brainstorm is now in the "Ready today" table but needs a P1 change.** Section 3.1 is headed "Ready today (10)" and says these rows "run as workers now if the brief uses the stated flags" (`spec:78-79`). The brainstorm row now names a P1 change (`spec:84`), and its "Brief must pass" cell does not list `--unattended`, which `spec:73` requires. No P0 run uses brainstorm (`spec:158`), so no wrong outcome in P0. Medium, as a label and count inconsistency.

**M-3 (line `:84`, quoting `inventory/commands-a.md:39`): the row does not say that unattended brainstorm answers its own questions.** The inventory says the non-interactive dialogue "answers its own questions 'using best-available context'" (`inventory/commands-a.md:39`). The row resolves no gate and does not state that this auto-decided content is acceptable under WC-2 for a worker with no person. Medium.

**M-4 (line `:142`, against `:148` and `:149`): "the documented defect fixes that SA-4 names" is an open exception.** SA-3 still says "with one exception" (`spec:148`), and SA-4's test is "correct a documented defect" (`spec:149`). "Documented" is not defined, and the exception covers changes that are visible to a person (for example explain's added Write tool, `spec:108`). An implementer must judge, case by case, whether a standalone change is allowed. Medium.

**M-5 (line `:159`; carries RA-18): "F-05" is cited on a changed line and is defined nowhere.** `spec:159` cites "init-lite (F-05)". The id is undefined in the spec and inventories (gate.md RA-18, still open). Medium.

### Minor notes

- N-5 (lines `:84`, `:142`, `:159`, `:199`, `:201`): review tags such as "(RA-03)" are written into the spec body. They are the reviser's citations, as the reviser contract requires, but they refer to review ids the spec does not define. Remove them when the loop closes.

## Guard Condition Boundary Table (changed-line guards only)

Dimensional analysis (Pipeline, FR-17): not triggered by any changed line; no multi-stage count flow is changed.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| `command is load` | `spec:201` (AC-1.2) | Sentinel Value Match | `load` | true | Excluded from the 7.2 check; excluded from the contract name (`spec:200`) | OK |
| `command is load` | `spec:201` | Typical | `analyze` | false | 7.2 check with `--unattended --output <dir>` | OK |
| `command is load` | `spec:201` | Legitimate Edge Case | `brainstorm` (P1, `spec:84`, `spec:159`) | false | 7.2 check applies; its flag and section are added in P1 | OK |
| `existing report file` (step 4) | `spec:199`, `spec:188` | Zero/Empty | `/sc:troubleshoot` default run, no contract (`inventory/commands-b.md:242`) | false | Step 4 runs `test -s` and a YAML `status` check on REPORT.md; no `status` field is stated | GAP (blocking, RA-01) |
| `existing report file` (step 4) | `spec:199` | Typical | `/sc:workflow --handoff none`, post-creation contract (`spec:92`) | true | Step 4 applies to the existing contract | OK |
| `status under WC-5` (step 3) | `spec:199` | Zero/Empty | `/sc:troubleshoot` REPORT.md with no `status` | not determinable | No status to compare with `--outcome` | GAP (part of RA-01) |
| `documented defect` (SA-4 exception) | `spec:142`, `spec:149` | Legitimate Edge Case | explain's added Write tool (`spec:108`) | true | Exception applies | OK |
| `documented defect` (SA-4 exception) | `spec:142` | Typical | a standalone change with no inventory line | undefined | No rule says how to decide | GAP (Medium, M-4) |
| `--interactive` absent | `spec:84` (brainstorm) | Typical | default brief | false | Auto-proceeds (`inventory/commands-a.md:39`) | OK |

Classes left out: One/Minimal and Maximum/Overflow do not apply to command-name or status-presence guards; the rest are covered above.

## Unchanged prior findings

RA-05 to RA-18 and N-01 to N-04 from `gate.md` are on unchanged lines and are not re-graded here. Two of them are cited by changed lines and are carried as M-1 (RA-09) and M-5 (RA-18). Under the command's Review Loop bullet 3, the session that ran the review asks the user once whether to open an issue for the follow-up candidates: M-1 to M-5, N-5, RA-05 to RA-18 and N-01 to N-04. No issue is created without that answer.

## Coverage line

Not applicable: an open blocking finding exists, so the `scoped PASS: changed lines + prior blockers` line is not written.

## Escalation

GATE prompt, "Gate loop": a FAIL of this gate re-review escalates to the user with the open blocking findings. No second gate loop and no further review is started in this run. Open blocking finding for the user: RA-01.

## Reviser brief

Blocking ids: RA-01.

Restating the Review Loop bullet 6 for the reviser: revise only text a blocking finding names; add no rule, mechanism or section that a blocking finding does not call for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id. Medium and minor findings are not part of this brief and must not be edited under it.

verdict: FAIL
