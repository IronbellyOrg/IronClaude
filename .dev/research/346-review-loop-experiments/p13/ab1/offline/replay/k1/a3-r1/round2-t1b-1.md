review: 2 of 3

# Spec-panel critique, round 2 (re-review): Orca worker-contract spec

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture --re-review .dev/orca-command-refactor/review/round1.md --baseline .dev/orca-command-refactor/specs/history/spec-v1.md`
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (57973 bytes, 285 lines), sha256 `d1f34e4bb75f645e00e9b421dc8abdf0366d981ef45c7dfcc8f6689db8833a6a`
- baseline: `.dev/orca-command-refactor/specs/history/spec-v1.md` (57763 bytes, 285 lines), sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- prior report: `.dev/orca-command-refactor/review/round1.md`, sha256 `ff0e6de619be4ae8ae0c40f9d5036eaf36d59a2c18d2ddc13311f88cbef8f79c`; its header is `review: 1 of 3` and its last line is `verdict: FAIL`, so N = 1 + 1 = 2 and the cap check (prior at `review: 3` with FAIL) does not apply.
- reviewer model actually used: `claude-sonnet-5-5`
- prompt followed: RE-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:34-47`, read in full (file read at the sandbox path `home/.claude/rules/prompts/document_review_loop_prompts.md`). Roles are fixed by its table (`prompts:38-42`): CANDIDATE = the `@file`, BASELINE = `--baseline`, PRIOR = `--re-review`.
- brief clauses overridden: none. The brief neither widened scope nor graded a minor finding as blocking (`command.md:264`).
- mode notes (`command.md:261`): `--iterations` not given and ignored under `--re-review`; the Improve step is skipped; no revised specification is written.
- rf-qa re-check (`command.md:262`): `.claude/agents/rf-qa.md` (project) and `~/.claude/agents/rf-qa.md` are both absent from the sandbox, so steps 1-5 of its Fix Cycle Process were not read. The rules of `command.md:262` were applied standing alone: each prior blocking finding is decided by comparing its defect with the AFTER text only.

Citation shorthand: `spec:N` = line N of the candidate; `base:N` = line N of the baseline (line numbers are identical in both, because the revision added no line). `round1:N` = line N of the prior report. `revise1:N` = `.dev/orca-command-refactor/review/revise1.md`. `command.md:N` = the `/sc:spec-panel` definition; `prompts:N` = the review-loop prompts file.

## Step 1: evidence block (done before any finding)

Command run: `diff -w specs/history/spec-v1.md specs/orca-worker-contract-spec.md` from `.dev/orca-command-refactor/`. Four lines differ (182, 194, 195, 196); every other line is byte-identical outside whitespace.

### BEFORE (baseline), lines starting `<`

```text
182: 3. `ORCA orchestration check --wait --types "worker_done,escalation,question" --timeout-ms 900000 --json` until `worker_done` arrives. **Pass:** exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path.
194: | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1. Record the results in the phase report; a failure here reopens section 1 |
195: | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
196: | P1 | AC-1.2 | 7.2 live check on each P1 command with `--unattended --output <dir>` | all steps pass |
```

### AFTER (candidate), lines starting `>`

```text
182: 3. `ORCA orchestration check --wait --types "worker_done,escalation,question" --timeout-ms 900000 --json` until `worker_done` arrives. **Pass:** exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5 (in P0, the worker's own account of the result); its report path is the WC-4 contract path (in P0, the command's existing report file). [F1]
194: | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-3 and 5-7 pass, with step 3 read by its P0 wording; step 4 uses the command's existing report file, since the contract arrives in P1. [F1] Record the results in the phase report; a failure here reopens section 1 |
195: | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 except `load` (usage-line fix only, no contract; F2) has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
196: | P1 | AC-1.2 | 7.2 live check on each P1 command except `load` (F2) with `--unattended --output <dir>` | all steps pass |
```

(The line-number prefixes above are mine; the quoted text is the diff text without `<` / `>`.)

### Self-check (run before the verdict, `prompts:45`)

Each AFTER line (prefix stripped) was matched as a whole line with `grep -cxFf` against the candidate: 4 of 4 found. Each BEFORE line was matched against the baseline: 4 of 4 found. The BEFORE lines matched against the candidate: 0 of 4 found (correct, they were replaced). Roles are not swapped. The temporary match files were deleted afterwards; nothing else in the workspace was changed.

Size of the change: +210 bytes, 0 bytes deleted (57763 to 57973), matching `revise1:13-21`. The per-finding split in `revise1:17-21` (F1 138 bytes, F2 72 bytes) is consistent with the diff: F1 touched `spec:182` and `spec:194`, F2 touched `spec:195` and `spec:196`. I did not recount the split by line; the net total I did check by `wc -c` (57763 and 57973).

## What was covered, and what was not

Covered: the four changed lines; the prior blocking findings F1 and F2; every candidate line these four depend on (`spec:43`, `spec:62-63`, `spec:112`, `spec:139`, `spec:154`, `spec:158-159`, `spec:176`, `spec:180-186`, `spec:194-200`, `spec:265`, `spec:272`); the full set of mentions of `load` and of the "every command" quantifier in the candidate (grep over the whole file); and the byte accounting in `revise1`.

Not covered: lines unchanged against the baseline whose behaviour does not depend on a changed line. Round 1's Medium findings F3-F14 and notes N1-N8 are unchanged text and are carried forward untouched in the follow-up list below, neither re-opened nor closed (`command.md:259`). Whole-document assurance needs a separate, labelled first review (`command.md:262`); this report does not provide it.

Citation limits: I could read only the candidate, the baseline, the prior report, `revise1`, the README, the three inventories, the command definition and the prompts file. Any citation to a file outside the workspace (`CLAUDE.md`, `pyproject.toml`, `cmd/*`, `sk/*`, `EVIDENCE.md`, `.dev/codegraph-migration/**`) is UNVERIFIED here, and none of the verdicts below relies on one. Spec claims about the repository (for example that PyYAML is a declared dependency, `spec:183`) were not checked.

## Prior blocking findings

| Id | Prior status (round1) | Now | Basis (AFTER text only) |
|---|---|---|---|
| F1 | open (CRITICAL) | **resolved** | Step 3 of 7.2 at `spec:182` now carries a P0 reading for both of its clauses: the outcome is compared with "the worker's own account of the result" and the report path with "the command's existing report file". AC-0.4 at `spec:194` now says "step 3 read by its P0 wording". The contradiction round1 named, step 3 demanding the WC-4 contract path while P0 has "no command edits" (`spec:158`) and P1 creates the contract (`spec:159`), is gone: no clause that must pass in P0 now requires a contract file. The gate in `spec:154` can pass. The WC-4 wording is unchanged and applies from P1 on, because the parentheses name P0 only. Round1's own recommendation (`round1:115`) is applied in substance. |
| F2 | open (CRITICAL) | **resolved** | AC-1.1 at `spec:195` now quantifies "every command in sections 3.1-3.2 except `load` (usage-line fix only, no contract; F2)", and AC-1.2 at `spec:196` reads "each P1 command except `load` (F2)". `load` keeps its row (`spec:112`, "P1 (usage line only)") and its Decision (`spec:265`, "a report file would be an unrequested addition"). The test no longer asserts a section that `load` is specified not to carry, and the 7.2 live check no longer demands a contract from a command that writes none. `load` is also listed as not dispatchable on its own (`spec:112`, `spec:139`), so exempting it from the live check is consistent. No other acceptance row quantifies over sections 3.1-3.2 or over P1 commands (`spec:176`, `spec:197`, `spec:200` were read and do not). |

Regressed: none. Round1 marked no blocking finding resolved, so there was nothing that could regress; F1 and F2 were the only two blocking findings (`round1:109-123`, `round1:180`).

Open blocking findings after this review: none.

## Findings on changed lines (and the dependencies they touch)

Each carries `origin=changed|unchanged` (`command.md:262`). In a re-review the Guard Condition Boundary Table covers guards on changed lines only.

### Guard Condition Boundary Table (changed lines only; hard gate, `command.md:311-334`)

Completed before synthesis. The changed lines introduce or alter three guards: the P0 reading of step 3 (`spec:182`, `spec:194`), and the `load` exemption in AC-1.1 and AC-1.2 (`spec:195-196`).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| `step3-p0-reading` | spec:182, spec:194 | Typical | P0 run of `/sc:troubleshoot`, no contract, `REPORT.md` written (INV-B:242, spec:91) | true | Outcome compared with the worker's own account; report path must be the existing report file; passes | OK |
| `step3-p0-reading` | spec:182, spec:194 | Typical | P0 run of `/sc:adversarial` or `/sc:workflow`, which already write their own contract files (spec:83, spec:92) | true | Same P0 reading; the existing report file is what the worker reports | OK |
| `step3-p0-reading` | spec:182, spec:159 | Legitimate Edge Case | first P1 run, where the contract exists (P1 creates it) | false | The P0 parentheses stop applying; the WC-4 wording governs from P1 on (spec:62, spec:159) | OK |
| `step3-p0-reading` | spec:182 | Zero/Empty | worker sends `worker_done` with no report path | unspecified | Not stated for P0 either; WC-5 says "no report exists" maps to `--outcome failed` (spec:63) | GAP (R2-3, minor) |
| `step4-p0` | spec:183, spec:194 | Typical | step 4 run on a markdown report such as `REPORT.md` | n/a | AC-0.4 lists steps 1-3 and 5-7 as the ones that must pass and says step 4 "uses the command's existing report file"; step 4's own pass condition (a YAML mapping with `status` and `command`, spec:183) cannot hold for a markdown file | GAP (R2-1, Medium) |
| `load-exemption` (AC-1.1) | spec:195, spec:112 | Typical | `load.md` carries no `## Unattended mode` section | true (exempt) | Test skips `load`; the assertion "no section-4 command has one" is untouched | OK |
| `load-exemption` (AC-1.1) | spec:195, spec:159 | Legitimate Edge Case | `load` receives the blanket P1 `--unattended` flag | unspecified | `spec:159` lists `load` in the blanket flag clause and in "usage line only"; no check tests the flag on `load` | GAP (R2-2, minor) |
| `load-exemption` (AC-1.2) | spec:196 | Zero/Empty | P1 command set with `load` removed | true | Set shrinks from 13 command edits to 12; every remaining command is a worker with a contract | OK |
| `load-exemption` (AC-1.2) | spec:196, spec:139 | Sentinel Value Match | another command whose row says "no contract" | false | None: `load` is the only P1 command whose row says no contract (spec:112, grep of spec) | OK |

Left out: `step3-p0-reading` One/Minimal and Maximum (a pass condition has no capacity); `step4-p0` Zero, One, Maximum, Sentinel and Edge (the guard is a single applicability question, one row covers it); `load-exemption` One/Minimal and Maximum (one named command, no capacity).

### Quantity Flow Diagram (FR-21, scoped to the changed AC-1.1 set; trigger: the count of commands differs between stages)

```text
[Source: 37 workers in sections 3.1 + 3.2]                       spec:78-125, round1:63-65
   --> [P1 blanket flag clause, spec:159]       expects 37 commands to accept --unattended   (unchanged)
   --> [AC-1.1, spec:195]   37 - 1 (load exempt) = 36 commands asserted to carry
                            `## Unattended mode` naming return-contract.yaml          [changed, F2]
   --> [AC-1.2, spec:196]   P1 live check: 13 P1 command edits - load = 12 commands     [changed, F2]
   --> [load, spec:112 + spec:265]  usage line only, no section, no contract          consistent with AC-1.1 and AC-1.2
Divergence point: 37 (spec:159) vs 36 (AC-1.1). Handled: the exception is named on the changed line.
Remaining divergence, no consumer: spec:159 still says load accepts the flag; nothing tests it (R2-2).
```

The mismatch round1 named (36 vs 37 with an AC expecting 37) no longer exists for the two acceptance checks.

### New findings

**R2-1. Medium. origin=changed. Wiegers, Whittaker (Sequence Attack). AC-0.4 excludes step 4 from the steps that must pass, but does not say what step 4 does with a markdown report.** `spec:194` says "steps 1-3 and 5-7 pass ... step 4 uses the command's existing report file". Step 4 at `spec:183` runs `yaml.safe_load` and asserts `d['status']` and `d['command']`; for `/sc:troubleshoot` the existing report file is `REPORT.md` (`spec:91`), a markdown file, so the assertion cannot hold for it. Because step 4 is not in the must-pass list, AC-0.4 is passable as written (this is why it is Medium and not blocking). The risk is a guess: a coordinator who runs step 4 on `REPORT.md` and reads its failure as a failed AC-0.4 would stall the P0 gate that F1 just unblocked. Not blocking: the text does not force that reading. Follow-up: one clause saying step 4 in P0 is `test -s` on the report file only. Grading sentence: an implementer who follows the text as written passes AC-0.4 (step 4 is not required), so no wrong outcome follows without an assumption; Medium.

**R2-2. minor note. origin=unchanged (depends on the changed AC-1.1 line but does not quote it as the cause). Cockburn.** `spec:159` still lists `load` in the blanket "`--unattended` accepted by every command in sections 3.1 and 3.2" and in "WC-4 contract in unattended mode", while `spec:112` and `spec:265` say usage line only. `revise1:34` records this as deliberately left alone. The flag is described as a no-op where a command has no gate (`spec:159`), no acceptance check tests it for `load`, and `load` is not dispatched as a worker (`spec:112`, `spec:139`), so no implementer outcome is wrong. Note only.

**R2-3. minor note. origin=changed. Wiegers.** The P0 reading "the worker's own account of the result" (`spec:182`) points at no recorded artifact: the account sits in the worker's `worker_done` body (WC-5 says the first sentence states the status, `spec:63`), so the comparison of `--outcome` with that account is weak evidence that the outcome is true. This is the wording round1 itself recommended (`round1:115`), the P0 purpose is to observe that a direct run completes and reports (`spec:154`, `spec:272`), and step 3 still demands exactly one `worker_done`. Note only.

No new blocking finding. No older severe defect was newly discovered in the dependencies of the changed lines (`prompts:47`).

### Consistency of the AFTER text with the requirements that depend on it (PASS precondition, `prompts:45`)

- Section 6 gate (`spec:154`, "Later phases do not start until the earlier phase's checks in section 7 pass"): P0's AC-0.4 can now pass without a contract, so P1 can start. Consistent.
- P0 scope (`spec:158`, "no command edits") and P1 scope (`spec:159`, the contract arrives in P1): consistent with the P0 parentheses at `spec:182` and `spec:194`.
- WC-4 and WC-5 (`spec:62-63`): untouched; the P0 parentheses are additive qualifiers, not a second rule. SA-4's additive-edits rule (`spec:149`) and AC-C5 (`spec:176`) govern command files, not this spec text, and are unaffected.
- `load` row and Decision (`spec:112`, `spec:265`) and the list of non-dispatched commands (`spec:139`): consistent with the AC-1.1 and AC-1.2 exemption.
- Phase pass rule (`spec:166`, "A phase passes only when every check in its block and every common check passes"): AC-1.1 and AC-1.2 are now satisfiable for P1.

## Expert notes

- Wiegers and Adzic: both repairs are narrow qualifiers that restore testability of the two checks round1 found unpassable; the exemption of `load` is stated on the same line as the assertion, which is where a test author will read it.
- Whittaker (Sequence and Divergence attacks re-run on the changed lines): no ordering break remains between P0 and P1; the only residue is the step-4 applicability gap (R2-1), which sits behind an explicit must-pass list.
- Fowler, Nygard, Newman, Hohpe: no architecture text changed (`spec:13-39` and sections 2 and 4 are byte-identical to the baseline), so nothing in the architecture focus is re-opened.
- Disagreement: none on the verdict.

## Follow-up candidates (never trigger a revision, never fail the review, not in the Reviser brief)

- New in this round: Medium R2-1; minor R2-2, R2-3.
- Carried forward unchanged from round1 (not re-checked, unchanged text): Medium F3, F4, F5, F6, F7, F8, F9, F10, F11, F12, F13, F14; minor N1, N2, N3, N4, N5, N6, N7, N8 (`round1:129-166`).
- The issue offer (`command.md:260`): the session that ran this review is a worker whose reply is limited to the output path, so it asked nothing and created no issue. The list is recorded here for the coordinator to put to the user once.

## Reviser brief

None. No blocking finding is open, so no revision is called for (`command.md:263`).

coverage: scoped PASS: changed lines + prior blockers

verdict: PASS


## Findings block

```findings-v1
{"prior": "L1", "status": "resolved"}
{"prior": "L1", "status": "resolved"}
```
