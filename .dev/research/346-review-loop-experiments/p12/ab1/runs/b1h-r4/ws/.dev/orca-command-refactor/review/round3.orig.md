review: 3 of 3

# Re-review of the Orca worker-contract spec (round 3)

Command: `/sc:spec-panel --mode critique --focus requirements,architecture --re-review .dev/orca-command-refactor/review/round2.md --baseline .dev/orca-command-refactor/specs/history/spec-v2.md`, run as the re-review of the candidate spec. This worker made no revision and wrote no other file.

candidate: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md sha256 005c14750dde7985fd4ffcf42529a7b23cc2ca06ed4169b3ad679316a9e00f9a
baseline: .dev/orca-command-refactor/specs/history/spec-v2.md sha256 6f240e27e8d58d66b8256a439936eb55132bda0b917254aa463c5abc36931750 (the text round2.md reviewed; `candidate` in round2.md has the same hash)
prior: .dev/orca-command-refactor/review/round2.md sha256 879194e57071c774c3b349ae0985bdb6e4ef72a55bc30cf213be6a4971f7f408 (`review: 2 of 3`, `verdict: FAIL`; its VERIFY block at round2.md:2 confirmed N2 only)
reviewer model: claude-haiku-5-5
focus: requirements, architecture
rf-qa.md: not read. Neither `.claude/agents/rf-qa.md` (workspace) nor `~/.claude/agents/rf-qa.md` (sandbox home) exists, so the rules in the command's Review Loop section stand alone (Review Loop bullet 5).
Review count: this is review 3 of 3 (prior `review: 2 of 3` plus 1). This is the last review; open blocking findings escalate to the user (Review Loop bullet 4).

Candidate citations below are `candidate:N` (`specs/orca-worker-contract-spec.md`, line N). Baseline citations are `baseline:N` (`specs/history/spec-v2.md`, line N). Only line 86 differs between the two files apart from whitespace (checked with `diff -w`, see Step 1).

Process note: a scratch file was written to `/tmp/x` by mistake during the diff check. It was removed at once and is not used. The review used only sandbox paths.

## Step 1: evidence block

Roles, fixed by the file arguments: BASELINE = spec-v2.md, CANDIDATE = orca-worker-contract-spec.md. Command: `diff -w BASELINE CANDIDATE`. Output: one changed span, `86c86`.

Self-check (run before any finding, with `grep -cF`): the BEFORE line occurs once in BASELINE and zero or one time as a changed line in CANDIDATE. The AFTER line occurs once in CANDIDATE. The roles are therefore not swapped. The `<` and `>` prefixes are removed; the text is otherwise verbatim.

BEFORE (baseline, line 86):
````text
| init-lite | `--output <dir>` after P1 (the flag becomes directory-valued) [M2] | `.dev/superclaude/context-audit.md` or `--output` | Fresh dir per run (WC-6) [M2] | Per-run output directory (P1) [M2]: a retry writes a new `context-audit.md` and does not overwrite the first attempt's report | `cmd/init-lite.md:32`; `sk/sc-init-lite-protocol/SKILL.md:66,70`; `INV-A:55` |
````

AFTER (candidate, line 86):
````text
| init-lite | `--unattended --output <dir>/context-audit.md` after P1, with a fresh `<dir>` per run (`<dir>` is the WC-4 output directory, so the contract is `<dir>/return-contract.yaml`); standalone `--output <file>` is unchanged (SA-1) [N2] [M2] | `.dev/superclaude/context-audit.md` or `--output` | Fresh dir per run (WC-6) [M2] | Per-run output directory (P1) [M2]: a retry writes a new `context-audit.md` and does not overwrite the first attempt's report | `cmd/init-lite.md:32`; `sk/sc-init-lite-protocol/SKILL.md:66,70`; `INV-A:55` |
````

The reviser's changed span is the "Brief must pass" cell only (reviser report at `review/revise2.md:18-19,30`). No other line of the candidate changed.

## Prior blocking findings (round 2)

The VERIFY reply (`review/verify-2.md:13`, `confirmed: N2`) confirmed one blocking id. The VERIFY rule makes a rejected id a note, not a prior blocking finding. M2 and N1 were rejected (`review/verify-2.md:9-11`; `review/round2.md:2`). The round2 Reviser brief (`review/round2.md:164`) still lists M2, N1 and N2. That brief clause conflicts with the VERIFY block the same report carries, and the VERIFY rule governs it. This review follows the VERIFY block and names the override here (Review Loop bullet 7).

| Prior id | Status | Basis |
|---|---|---|
| N2 | resolved | The defect was that `--output` became directory-valued for every run (`round2.md:119`). `candidate:86` no longer says "the flag becomes directory-valued". The standalone form is now stated as `standalone --output <file> is unchanged (SA-1)`, which matches SA-1 (`candidate:147`) and the hard requirement at `candidate:143`. The new directory-style value under `--unattended` introduces a new finding, N3 below. N2 itself is resolved. |

Noted, not prior blocking (rejected in VERIFY; text status for information only):

| Id | Status | Basis |
|---|---|---|
| M2 | noted, unactioned | `candidate:86` still tags "Per-run output directory (P1) [M2]". P1 scope at `candidate:160` includes "the small fixes to ready commands", which covers init-lite. |
| N1 | noted, unactioned | Readiness wording is still inconsistent: `candidate:86` says "after P1" inside the 3.1 "Ready today" table. Carried as Medium follow-up F6 below. |

Regressed: none. No prior finding was marked resolved in round 2, so none can regress.

## New findings on changed lines

### N3 (blocking, origin=changed): the revised init-lite row makes `--output` a file under `--unattended`, but WC-4 defines `--output` as the output directory

- Location: `candidate:86` (changed line); conflicting text `candidate:62` (WC-4, unchanged); `candidate:73` (2.3, unchanged).
- Stated texts:
  - `candidate:62` (WC-4): "In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)." The only exception in WC-4 names a different contract path ("Where section 3 names a different fixed path for a command, that path is the contract path instead"). It does not allow `--output` to name a file.
  - `candidate:73` (2.3): the brief passes "the output directory, so the report path is known before dispatch (WC-4)".
  - `candidate:86`: "`--unattended --output <dir>/context-audit.md` ... (`<dir>` is the WC-4 output directory, so the contract is `<dir>/return-contract.yaml`)". Under this row the value passed by `--output` is a file, not a directory.
- Grading sentence: An implementer who follows `candidate:62` as written takes the value passed by `--output` as `<output-dir>`. For the init-lite brief that value is `<dir>/context-audit.md`, so the contract is written at `<dir>/context-audit.md/return-contract.yaml`. The coordinator opens `<dir>/return-contract.yaml`, as `candidate:86` and `candidate:73` direct it to. It finds no report, and `candidate:63` (WC-5) maps the missing report to `failed` for a run that did its work. Two stated texts contradict each other on what `--output` names for this command, and the only stated exception does not cover it.
- Origin: introduced by the revision that fixed N2. Round2's N2 recommendation (`round2.md:120`) suggested `--output <dir>/context-audit.md`, and the reviser followed it. That suggestion did not check the `--output` type against WC-4.
- Recommendation (either option; the reviser chooses and states which):
  - (a) Keep the directory form for `--unattended` runs only: `--unattended --output <dir>` under a fresh `<dir>` per run, with the file form unchanged for standalone runs (SA-1). The row then matches WC-4 without change to WC-4.
  - (b) Keep `--output <file>` in both modes, and add one init-lite entry to the WC-4 exception sentence, in the same form as the adversarial entry: the contract for init-lite is `<dirname of --output>/return-contract.yaml`.
  - Option (b) is preferred because it keeps one flag type per flag, which round2's N2 recommendation also wanted (`round2.md:120`). Either option must cite N3.
- Priority: High. Quality impact: the contract is written where the coordinator does not look, so a completed run is reported `failed`.
- Verification status: the finding quotes only `candidate:62`, `candidate:73` and `candidate:86`, all checkable in the workspace. Verified by reading those lines.

## Medium warnings (follow-up candidates; never fail this review)

- F6 (origin=changed, `candidate:86` against `candidate:79` and `candidate:160`): the init-lite row sits in the 3.1 table headed "Ready today (9)" (`candidate:78`), and `candidate:79` says these commands "run as workers now if the brief uses the stated flags". The same row says the `--unattended` flag arrives "after P1" (`candidate:86`), and P1 is `candidate:160`. An implementer who reads `candidate:79` dispatches init-lite today with `--unattended`, and one who reads `candidate:86` waits for P1. A guess is needed. This is the readiness wording the VERIFY block called inconsistent without a stated wrong outcome (`verify-2.md:11`). Medium. Fix: move init-lite to 3.2, or write "ready after P1" at `candidate:79`.
- Round2 F1-F5 (`round2.md:125-129`) are on lines this revision did not change (`candidate:140`, `candidate:111`, `candidate:186`, `candidate:218`). Under Review Loop bullet 5 they are origin=unchanged and minor notes unless they quote the changed line, and none does. They are not re-graded here and are carried as follow-up candidates by reference.
- Round1 notes M1, M3 and M5 (`round2.md:133-135`) are carried unchanged; their lines are unchanged.

## Guard Condition Boundary Table (changed-line guards only, FR-8 to FR-10)

Pipeline Dimensional Analysis is not triggered: the changed line describes no multi-stage count-changing pipeline. Maximum/Overflow is not applicable: the changed line has no numeric threshold.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| init-lite output directory | `candidate:86` | Zero/Empty: `--unattended` with no `--output` | `""` | n/a | `candidate:73` requires the brief to pass the output directory | OK |
| init-lite output directory | `candidate:86` | Typical: `--unattended --output <dir>/context-audit.md` | file path | true | contract `<dir>/return-contract.yaml` per the row, but WC-4 (`candidate:62`) defines `--output` as a directory | GAP (N3, blocking) |
| init-lite output directory | `candidate:86` | Legitimate edge: `--unattended --output <dir>` (the WC-4 form) | directory | not stated | the row's syntax does not say whether init-lite accepts it; WC-4 implies it | GAP (N3, blocking) |
| init-lite standalone output | `candidate:86` | Typical: standalone `--output report.md` | `report.md` | true | "unchanged (SA-1)" (`candidate:147`) | OK (N2 resolved) |
| init-lite retry | `candidate:86` | Legitimate edge: `--retry-of` run with a fresh `<dir>` | new dir | true | new `context-audit.md`; first attempt kept (`candidate:86`, WC-6 at `candidate:64`); P1 schedules the fix (`candidate:160`) | OK (M2 noted; N1 readiness wording is F6) |

## Escalation and verdict

- Open blocking findings: N3. Resolved: N2. Regressed: none.
- This is review 3 of 3. No Reviser brief is written, because the run escalates at `review: 3` (Review Loop bullet 6).
- VERIFY: the VERIFY prompt has not been run on N3. This worker has no fresh-context verifier. The coordinator must run the VERIFY prompt on N3 with the finding text above before escalation (`document_review_loop_prompts.md`, VERIFY step). A reply that is missing or has no `confirmed:` line confirms N3 by default. If N3 is rejected, the verdict stays FAIL with no confirmed blocking finding, which counts as PASS (VERIFY rule). This report's verdict is FAIL before VERIFY.
- Escalate to the user with: N3 (open, blocking; options (a) and (b) above). F6 and the round-2 Medium items go to `follow-up candidates`; the session asks the user once whether to open an issue for them.

## Coverage

Read: all 309 lines of the candidate; `review/round2.md` in full, including its VERIFY block and Reviser brief; `review/verify-2.md` in full; `review/revise2.md` header and byte report (lines 1-30, 48); `inventory/commands-a.md:55` (init-lite row, for the `--output` form in the inventory: `context-audit.md` or `--output`, with no type given); the README at `.dev/orca-command-refactor/README.md`; the Review Loop prompts file (`home/.claude/rules/prompts/document_review_loop_prompts.md`).

Baseline: read through `diff -w` against the candidate. The diff shows one changed span (line 86), so the rest of spec-v2 is the same text as the candidate.

Ran: `sha256sum` on candidate, baseline and prior; `diff -w`; `grep -cF` self-check of the BEFORE and AFTER lines in their files; a check for `rf-qa.md` in the sandbox (absent).

UNVERIFIED: every `cmd/`, `sk/`, `src/`, `CAPS:`, `INV-B` and `cmd/init-lite.md` citation, because those files are outside the workspace. N3 depends only on the candidate text itself, so it does not rest on any UNVERIFIED citation. The round-2 finding N1 and the round-1 notes M1, M3 and M5 are carried as notes, not re-verified.

Counts: prior blocking findings checked: 1 (N2: 1 resolved, 0 open, 0 regressed). Rejected prior ids kept as notes: 2 (M2, N1). New blocking findings: 1 (N3). New Medium warnings: 1 (F6). Carried Medium warnings: 5 (round2 F1-F5, origin=unchanged, by reference). Carried notes: 3 (M1, M3, M5).

verdict: FAIL
